#!/usr/bin/env python3
"""Turn the owner's decisions in the doubt queue into rules.

  applica_decisioni.py --pkg PKG --coda coda_dubbi.csv [--data 2026-10-09] [--prova]

Reads the queue (semicolon CSV written by dubbi.py and filled by the owner in
the 'decisione' column) and appends to regole_geografiche.json:

  slug            one page                     -> rule modo 'unica'
  slug1+slug2     both pages (boundary)        -> rule modo 'doppia_confine'
                                                  (only with --consenti-confine: DEC-107)
  tratto          depends on the stretch       -> rule modo 'tratto'
  nessuna         no active page               -> rule modo 'senza_pagina'
  ok              accept the proposal          -> as above, from 'proposta'
  ignora          not a doubt about the map    -> closed, no rule
  (empty)         still open                   -> skipped

A decision that belongs to the gazetteer (the owner's table, which wins over
every other file per AGENTS.md) never becomes a rule: it is written to
modifiche_gazetteer.csv next to the queue, to be applied in the table and the
gazetteer rebuilt. A zone rule that contradicts the gazetteer's zu_code is
refused for the same reason. --prova checks everything and writes nothing.
"""
import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from qngeo import _read, norm, package_root, rules_path  # noqa: E402



def parse(dec, row, active):
    d = dec.strip().lower()
    if d == 'ok':
        d = (row['proposta'] or '').strip().lower()
        if not d:
            raise ValueError('ok senza proposta: scrivere la pagina')
    if d == 'ignora':
        return 'ignora', []
    if d == 'tratto':
        return 'tratto', [p for p in row['opzioni'].split('+') if p in active]
    if d == 'nessuna':
        return 'senza_pagina', []
    pages = [p.strip() for p in d.split('+') if p.strip()]
    bad = [p for p in pages if p not in active]
    if bad:
        raise ValueError(f'pagine non attive o inesistenti: {bad}')
    return ('unica' if len(pages) == 1 else 'doppia_confine'), sorted(pages)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--coda', required=True, type=Path)
    ap.add_argument('--data', default=datetime.date.today().isoformat())
    ap.add_argument('--prova', action='store_true')
    ap.add_argument('--consenti-confine', action='store_true',
                    help='accetta slug1+slug2 (doppia assegnazione): solo dopo che DEC-107 e\' decisa')
    a = ap.parse_args()
    gaz = _read(package_root(a.pkg) / 'input' / 'gazetteer_qn.json')
    active = {z['publication_zone_id'] for z in gaz['publication_zones'] if z['is_page']}
    zu = {}
    for n in gaz['neighbourhoods']:
        for c in (n['zu_code'] or '').replace(';', ' ').split():
            zu.setdefault(c.upper(), set()).add(n['publication_zone_id'])
    RULES = rules_path()
    store = json.loads(RULES.read_text(encoding='utf-8'))
    rules, closed = store['regole'], store.setdefault('chiusi', [])
    known = {r['dubbio'] for r in rules} | {c['dubbio'] for c in closed}
    nxt = max([int(r['id'].split('-')[1]) for r in rules] or [0]) + 1
    added, closed_now, gaz_changes, errors = [], [], [], []
    with a.coda.open(encoding='utf-8-sig', newline='') as h:
        for row in csv.DictReader(h, delimiter=';'):
            dec = (row.get('decisione') or '').strip()
            if not dec or row['id_dubbio'] in known:
                continue
            try:
                modo, pages = parse(dec, row, active)
            except ValueError as exc:
                errors.append(f"{row['id_dubbio']}: {exc}")
                continue
            if modo == 'doppia_confine' and not a.consenti_confine:
                errors.append(f"{row['id_dubbio']}: doppia assegnazione sospesa finche' DEC-107 e' aperta "
                              f"(--consenti-confine dopo la decisione)")
                continue
            reason = (row.get('note') or '').strip() or f"decisione owner sulla coda dubbi ({row['base_proposta'][:160]})"
            if modo == 'ignora':
                closed_now.append({'dubbio': row['id_dubbio'], 'motivo': reason, 'deciso_da': 'owner', 'data': a.data})
                continue
            if row['si_applica_in'].startswith('gazetteer') and (
                    modo == 'senza_pagina' or '+'.join(pages) == (row['proposta'] or '').strip().lower()):
                # Confirms what the owner's table already says: close it, no rule.
                closed_now.append({'dubbio': row['id_dubbio'], 'motivo': 'confermata la tabella del gazetteer',
                                   'deciso_da': 'owner', 'data': a.data})
                continue
            if row['si_applica_in'].startswith('gazetteer'):
                gaz_changes.append({'dubbio': row['id_dubbio'], 'localita': row['chiave'], 'decisione': dec,
                                    'pagine': '+'.join(pages), 'note': reason})
                continue
            kind, key = row['tipo_regola'], row['chiave']
            if kind == 'zona' and key.upper() in zu and set(pages) != zu[key.upper()]:
                errors.append(f"{row['id_dubbio']}: contraddice il gazetteer (zu_code {key} -> {sorted(zu[key.upper()])}); "
                              f"cambiare la tabella dell'owner, non una regola")
                continue
            if kind == 'luogo':
                key = norm(key)
            added.append({'id': f'R-{nxt:04d}', 'tipo': kind, 'chiave': key, 'pagine': pages, 'modo': modo,
                          'motivo': reason, 'deciso_da': 'owner', 'data': a.data, 'dubbio': row['id_dubbio']})
            nxt += 1
    report = {'regole_nuove': len(added), 'chiusi_nuovi': len(closed_now),
              'modifiche_gazetteer': len(gaz_changes), 'errori': errors}
    if errors or a.prova:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        sys.exit(1 if errors else 0)
    rules.extend(added)
    closed.extend(closed_now)
    RULES.write_text(json.dumps(store, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    if gaz_changes:
        out = a.coda.with_name('modifiche_gazetteer.csv')
        with out.open('w', encoding='utf-8-sig', newline='') as h:
            w = csv.DictWriter(h, fieldnames=list(gaz_changes[0]), delimiter=';')
            w.writeheader()
            w.writerows(gaz_changes)
        report['file_modifiche_gazetteer'] = str(out)
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

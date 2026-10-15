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
every other file per AGENTS.md) never becomes a rule: when it matches what the
table already resolves it closes the doubt, otherwise it is written to
modifiche_gazetteer.csv next to the queue, to be applied in the table and the
gazetteer rebuilt. A zone rule that contradicts the gazetteer's zu_code is
refused for the same reason. A row C-R-nnnn (a rule contested in stage 2,
listed by dubbi.py --decisioni) replaces rule R-nnnn: the old rule stays in the
file as history, marked sostituita_da. --prova checks everything and writes
nothing.
"""
import argparse
import csv
import datetime
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from qngeo import _read, norm, package_root, rules_path  # noqa: E402

CONTESTED = 'C-'


def parse(dec, row, active):
    d = dec.strip().lower()
    if d == 'ok':
        d = (row.get('proposta') or '').strip().lower()
        if not d:
            raise ValueError('ok senza proposta: scrivere la pagina')
    if d == 'ignora':
        return 'ignora', []
    if d == 'tratto':
        if (row.get('tipo_regola') or '') != 'strada':
            raise ValueError("'tratto' vale solo per una strada (README: TRATTO = strade lunghe)")
        return 'tratto', [p for p in (row.get('opzioni') or '').split('+') if p in active]
    if d == 'nessuna':
        return 'senza_pagina', []
    pages = [p.strip() for p in d.split('+') if p.strip()]
    bad = [p for p in pages if p not in active]
    if bad:
        raise ValueError(f'pagine non attive o inesistenti: {bad}')
    if len(set(pages)) != len(pages):
        raise ValueError(f'pagina ripetuta: {pages}')
    if len(pages) > 2:
        raise ValueError(f'una regola di confine ha esattamente due pagine (DEC-107), non {len(pages)}')
    return ('unica' if len(pages) == 1 else 'doppia_confine'), sorted(pages)


IMMUTABLE = ('tipo_regola', 'chiave', 'si_applica_in')


def gazetteer_index(gaz):
    """What the owner's table resolves today: alias -> pages, zu_code -> pages."""
    import re
    alias, zu = {}, {}
    for n in gaz['neighbourhoods']:
        for a in [n['name_display']] + [x for x in re.split(r'[;|]', n.get('aliases') or '') if x.strip()]:
            if norm(a):
                alias.setdefault(norm(a), set()).add(n['publication_zone_id'])
        for c in (n['zu_code'] or '').replace(';', ' ').split():
            zu.setdefault(c.upper(), set()).add(n['publication_zone_id'])
    for z in gaz['publication_zones']:
        alias.setdefault(norm(z['name_display']), set()).add(z['publication_zone_id'])
    return alias, zu


def table_says(row, alias, zu, active):
    """Pages the gazetteer resolves the row's key to, for a row that belongs to the table."""
    if (row.get('tipo_regola') or '') == 'zona':
        return zu.get((row.get('chiave') or '').upper(), set())
    return alias.get(norm(row.get('chiave') or ''), set())


def write_atomic(path: Path, text: str):
    tmp = path.with_suffix(path.suffix + f'.{os.getpid()}.tmp')
    tmp.write_text(text, encoding='utf-8')
    os.replace(tmp, path)


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
    alias, zu = gazetteer_index(gaz)
    RULES = rules_path()
    # One writer at a time: the file is the memory of every applied decision.
    lock = RULES.with_suffix(RULES.suffix + '.lock')
    try:
        import fcntl
    except ImportError:
        fcntl = None
    with lock.open('a+') as lf:
        if fcntl:
            fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            run(a, active, alias, zu, RULES)
        finally:
            if fcntl:
                fcntl.flock(lf, fcntl.LOCK_UN)


def run(a, active, alias, zu, RULES):
    store = json.loads(RULES.read_text(encoding='utf-8'))
    rules, closed = store['regole'], store.setdefault('chiusi', [])
    known = {r['dubbio'] for r in rules} | {c['dubbio'] for c in closed}
    by_id = {r['id']: r for r in rules}
    live_keys = {(r['tipo'], r['chiave']): r['id'] for r in rules if not r.get('sostituita_da')}
    nxt = max([int(r['id'].split('-')[1]) for r in rules] or [0]) + 1
    added, closed_now, gaz_changes, errors, replaced = [], [], [], [], {}
    seen_rows = {}
    with a.coda.open(encoding='utf-8-sig', newline='') as h:
        for row in csv.DictReader(h, delimiter=';'):
            did = (row.get('id_dubbio') or '').strip()
            dec = (row.get('decisione') or '').strip()
            if not did or not dec or did in known:
                continue
            # The same doubt twice in one queue: rows identical in decision and
            # immutable fields are one; any other repetition is an error.
            shape = (dec.lower(),) + tuple((row.get(k) or '').strip().lower() for k in IMMUTABLE)
            if did in seen_rows:
                if seen_rows[did] != shape:
                    errors.append(f"{did}: righe duplicate che non coincidono (decisione, tipo, chiave o destinazione)")
                continue
            seen_rows[did] = shape
            try:
                modo, pages = parse(dec, row, active)
            except ValueError as exc:
                errors.append(f"{did}: {exc}")
                continue
            if modo == 'doppia_confine' and not a.consenti_confine:
                errors.append(f"{did}: doppia assegnazione sospesa finche' DEC-107 e' aperta "
                              f"(--consenti-confine dopo la decisione)")
                continue
            reason = (row.get('note') or '').strip() or f"decisione owner sulla coda dubbi ({(row.get('base_proposta') or '')[:160]})"
            if modo == 'ignora':
                closed_now.append({'dubbio': did, 'motivo': reason, 'deciso_da': 'owner', 'data': a.data})
                continue
            if (row.get('si_applica_in') or '').startswith('gazetteer'):
                # Compared with what the table resolves today, never with the queue's proposal.
                current = table_says(row, alias, zu, active)
                same = (not (current & active)) if modo == 'senza_pagina' else (set(pages) == current)
                if same:
                    closed_now.append({'dubbio': did, 'motivo': 'confermata la tabella del gazetteer',
                                       'deciso_da': 'owner', 'data': a.data})
                else:
                    gaz_changes.append({'dubbio': did, 'localita': row.get('chiave') or '', 'decisione': dec,
                                        'pagine': '+'.join(pages), 'oggi': '+'.join(sorted(current)) or '-', 'note': reason})
                continue
            kind, key = row.get('tipo_regola') or '', row.get('chiave') or ''
            if kind not in ('zona', 'strada', 'luogo'):
                errors.append(f"{did}: tipo_regola {kind!r} non ammesso per una regola")
                continue
            if kind == 'zona' and key.upper() in zu and set(pages) != zu[key.upper()]:
                errors.append(f"{did}: contraddice il gazetteer (zu_code {key} -> {sorted(zu[key.upper()])}); "
                              f"cambiare la tabella dell'owner, non una regola")
                continue
            key = key.upper() if kind == 'zona' else norm(key)
            old = None
            if did.startswith(CONTESTED):
                old = by_id.get(did[len(CONTESTED):])
                if not old or old.get('sostituita_da'):
                    errors.append(f"{did}: la regola contestata non esiste o e' gia' stata sostituita")
                    continue
                if (kind, key) != (old['tipo'], old['chiave']):
                    # A replacement rules the same place as the rule it replaces.
                    errors.append(f"{did}: la riga dice {kind} {key!r} ma la regola {old['id']} e' {old['tipo']} {old['chiave']!r}")
                    continue
            holder = live_keys.get((kind, key))
            if holder and holder != (old or {}).get('id'):
                errors.append(f"{did}: esiste gia' la regola {holder} per {kind} {key!r}: contestarla (riga C-{holder}), non duplicarla")
                continue
            rid = f'R-{nxt:04d}'
            rule = {'id': rid, 'tipo': kind, 'chiave': key, 'pagine': pages, 'modo': modo,
                    'motivo': reason, 'deciso_da': 'owner', 'data': a.data, 'dubbio': did}
            if old:
                rule['sostituisce'] = old['id']
                replaced[old['id']] = rid
            added.append(rule)
            live_keys[(kind, key)] = rid
            nxt += 1
    report = {'regole_nuove': len(added), 'regole_sostituite': len(replaced), 'chiusi_nuovi': len(closed_now),
              'modifiche_gazetteer': len(gaz_changes), 'errori': errors}
    if errors or a.prova:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        sys.exit(1 if errors else 0)
    for r in rules:
        if r['id'] in replaced:
            r['sostituita_da'] = replaced[r['id']]
    rules.extend(added)
    closed.extend(closed_now)
    write_atomic(RULES, json.dumps(store, ensure_ascii=False, indent=1) + '\n')
    # The gazetteer change list reflects this run only: rewritten, or removed when empty.
    out = a.coda.with_name('modifiche_gazetteer.csv')
    if gaz_changes:
        import io
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(gaz_changes[0]), delimiter=';', lineterminator='\r\n')
        w.writeheader()
        w.writerows(gaz_changes)
        write_atomic(out, '\ufeff' + buf.getvalue())
        report['file_modifiche_gazetteer'] = str(out)
    elif out.is_file():
        out.unlink()
        report['file_modifiche_gazetteer'] = 'rimosso: nessuna modifica in questa esecuzione'
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()

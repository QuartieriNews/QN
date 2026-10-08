#!/usr/bin/env python3
"""Check stage-2 decisions against the review protocol before they are counted.

  valida.py decisioni.jsonl [--pkg PKG]

Structural rules come from 02_ISTRUZIONI and aggregate_qn.py (cardinality,
active pages); the traceability rules are this process's own
(PROTOCOLLO_REVISIONE.md): every assigned page must follow from a place
marked as used with an effective role and a resolution that names it.
Exit 1 with one line per problem; exit 0 prints a summary.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import _read, package_root  # noqa: E402

STATUSES = {'U', 'M', 'T', 'D', 'I', 'F'}
EFFECTIVE = {'intervento', 'sede_evento', 'tratto', 'territorio_destinatari', 'alternativa_di_progetto'}
ROLES = EFFECTIVE | {'sede_istituzionale', 'provenienza', 'confronto_o_esempio', 'nome_di_opera',
                     'contesto', 'ipotesi_incerta'}
DOUBTS = {'senza_tratto_o_civico', 'raccordo_qn_da_verificare', 'sedi_parziali', 'sede_da_riscontrare',
          'trascrizione_dubbia', 'sede_non_indicata', 'riferimenti_discordanti'}


def check(d, active):
    p = []
    e, pages = d.get('esito'), d.get('pagine')
    if e not in STATUSES:
        return [f"esito {e!r} non ammesso"]
    if not isinstance(pages, list) or len(pages) != len(set(pages)):
        p.append('pagine deve essere una lista senza ripetizioni')
        pages = []
    if set(pages) - active:
        p.append(f"pagine non attive o inesistenti: {sorted(set(pages) - active)}")
    if (e == 'U' and len(pages) != 1) or (e == 'M' and len(pages) < 2) or (e in 'TDIF' and pages):
        p.append(f"cardinalita' non valida per {e}: {pages}")
    for k in ('motivo', 'fatto'):
        if not str(d.get(k, '')).strip():
            p.append(f"{k} vuoto")
    luoghi = d.get('luoghi') or []
    for l in luoghi:
        if l.get('ruolo') not in ROLES:
            p.append(f"ruolo non ammesso: {l.get('ruolo')!r} ({l.get('testo')})")
    supported = collections.defaultdict(list)
    for l in luoghi:
        if l.get('usato') and l.get('ruolo') in EFFECTIVE:
            for pg in (l.get('risoluzione') or {}).get('pagine', []):
                supported[pg].append(l.get('testo'))
    for pg in pages:
        if pg not in supported:
            p.append(f"pagina {pg} senza un luogo effettivo usato che la risolva")
    if e == 'M':
        used = [l for l in luoghi if l.get('usato') and l.get('ruolo') in EFFECTIVE]
        if len(used) < 2:
            p.append('M richiede almeno due luoghi effettivi')
    if e == 'D':
        if d.get('tipo_dubbio') not in DOUBTS:
            p.append(f"tipo_dubbio non ammesso: {d.get('tipo_dubbio')!r}")
        if not str(d.get('verifica_necessaria', '')).strip():
            p.append('D senza verifica_necessaria')
    if e == 'T' and not str(d.get('portata', '')).strip():
        p.append('T senza portata motivata')
    if e == 'I' and not str(d.get('verifica_necessaria', '')).strip():
        p.append('I senza indicazione di cosa manca (verifica_necessaria)')
    if d.get('confidenza') not in ('alta', 'media', 'bassa'):
        p.append('confidenza mancante')
    return p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('decisioni')
    ap.add_argument('--pkg')
    a = ap.parse_args()
    gaz = _read(package_root(a.pkg) / 'input' / 'gazetteer_qn.json')
    active = {z['publication_zone_id'] for z in gaz['publication_zones'] if z['is_page']}
    seen, problems, count = set(), [], collections.Counter()
    for n, line in enumerate(Path(a.decisioni).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"riga {n}: JSON non valido ({exc})")
            continue
        if d.get('id') in seen:
            problems.append(f"{d.get('id')}: ID ripetuto")
        seen.add(d.get('id'))
        count[d.get('esito')] += 1
        problems += [f"{d.get('id')}: {x}" for x in check(d, active)]
    if problems:
        print('\n'.join(problems))
        sys.exit(1)
    print(json.dumps({'decisioni': len(seen), 'esiti': dict(count), 'problemi': 0}))


if __name__ == '__main__':
    main()

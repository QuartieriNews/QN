#!/usr/bin/env python3
"""Check stage-2 decisions against the review protocol before they are counted.

  valida.py decisioni.jsonl [--pkg PKG]

Structural rules come from 02_ISTRUZIONI and aggregate_qn.py (cardinality,
active pages); the traceability rules are this process's own
(PROTOCOLLO_REVISIONE.md): every assigned page must follow from a place
marked as used with an effective role and a resolution that names it.
Since DEC-106 every decision states livello_portata (quartiere, municipio,
citta) besides its pages. Exit 1 with one line per problem; exit 0 prints a summary.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import _read, load_rules, package_root, rules_path  # noqa: E402

STATUSES = {'U', 'M', 'T', 'D', 'I', 'F'}
EFFECTIVE = {'intervento', 'sede_evento', 'tratto', 'territorio_destinatari', 'alternativa_di_progetto'}
ROLES = EFFECTIVE | {'sede_istituzionale', 'provenienza', 'confronto_o_esempio', 'nome_di_opera',
                     'contesto', 'ipotesi_incerta'}
LEVELS = {'quartiere', 'municipio', 'citta'}
DOUBTS = {'senza_tratto_o_civico', 'raccordo_qn_da_verificare', 'sedi_parziali', 'sede_da_riscontrare',
          'trascrizione_dubbia', 'sede_non_indicata', 'riferimenti_discordanti'}


def check(d, active, require_level=False, rules=None, ids=None):
    """Problems of one decision. `rules` maps rule id -> rule (the snapshot the
    reviewer worked with); `ids` is the set of record ids of the package."""
    p = []
    rules = rules or {}
    if not isinstance(d.get('id'), str) or not d['id'].strip():
        return ['id mancante']
    if ids is not None and d['id'] not in ids:
        p.append('id non presente fra le schede del pacchetto')
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
            ris = l.get('risoluzione') or {}
            if ris.get('pagine'):
                # Repeatable or it is not a resolution (protocol: "risoluzione ripetibile").
                if not str(ris.get('metodo') or '').strip() or not any(
                        str(ris.get(k) or '').strip() for k in ('query', 'riferimento', 'regola')):
                    p.append(f"risoluzione non ripetibile per {l.get('testo')!r}: servono metodo e query, riferimento o regola")
            if ris.get('regola'):
                rule = rules.get(ris['regola'])
                if not rule:
                    p.append(f"regola {ris['regola']} citata ma non presente in regole_geografiche.json")
                else:
                    # The cited rule decides the pages: a stretch rule allows a subset, the others the same set.
                    got, want = set(ris.get('pagine') or []), set(rule.get('pagine') or [])
                    if not (got <= want if rule.get('modo') == 'tratto' else got == want):
                        p.append(f"regola {ris['regola']} ({rule.get('modo')}) assegna {sorted(want)}, la risoluzione dice {sorted(got)}")
            for pg in ris.get('pagine', []):
                supported[pg].append(l.get('testo'))
    for pg in pages:
        if pg not in supported:
            p.append(f"pagina {pg} senza un luogo effettivo usato che la risolva")
    if e == 'M':
        used = [l for l in luoghi if l.get('usato') and l.get('ruolo') in EFFECTIVE]
        # Only a cited doppia_confine rule with these very pages makes M of one place.
        boundary = any(rules.get((l.get('risoluzione') or {}).get('regola'), {}).get('modo') == 'doppia_confine'
                       and set(rules[(l.get('risoluzione') or {})['regola']]['pagine']) == set(pages) for l in used)
        if len(used) < 2 and not boundary:
            p.append('M richiede almeno due luoghi effettivi (o una regola doppia_confine citata con le stesse pagine)')
    level = d.get('livello_portata')
    if level is not None or require_level:
        if level not in LEVELS:
            p.append(f"livello_portata non ammesso: {level!r}")
        elif e == 'T' and level == 'quartiere':
            p.append('T con livello_portata quartiere: contraddizione')
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
    ap.add_argument('--senza-livello', action='store_true',
                    help='decisioni anteriori a DEC-106 (prova cieca del 2026-10-08): livello_portata non richiesto')
    a = ap.parse_args()
    pkg = package_root(a.pkg)
    gaz = _read(pkg / 'input' / 'gazetteer_qn.json')
    active = {z['publication_zone_id'] for z in gaz['publication_zones'] if z['is_page']}
    ids = {json.loads(l)['id'] for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines() if l.strip()}
    rules = {r['id']: r for r in load_rules(rules_path())}
    seen, problems, count = set(), [], collections.Counter()
    for n, line in enumerate(Path(a.decisioni).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"riga {n}: JSON non valido ({exc})")
            continue
        if not isinstance(d.get('id'), str) or not d['id'].strip():
            problems.append(f"riga {n}: id mancante")
            continue
        if d['id'] in seen:
            problems.append(f"{d['id']}: ID ripetuto")
        seen.add(d['id'])
        count[d.get('esito')] += 1
        problems += [f"{d.get('id')}: {x}" for x in check(d, active, require_level=not a.senza_livello, rules=rules, ids=ids)]
    if problems:
        print('\n'.join(problems))
        sys.exit(1)
    print(json.dumps({'decisioni': len(seen), 'esiti': dict(count), 'problemi': 0}))


if __name__ == '__main__':
    main()

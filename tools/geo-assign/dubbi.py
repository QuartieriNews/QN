#!/usr/bin/env python3
"""Find every place where the QN geography is in doubt, grouped by place, for the owner.

The owner decides each doubt once; applica_decisioni.py turns the decision into
a rule (regole_geografiche.json) that the tools apply from then on, citing it.
Rerunning this script after the rules shows how many doubts are left: the
queue is meant to shrink towards zero.

  dubbi.py --pkg PKG --evidenze DIR/evidenze.jsonl --out coda_dubbi.csv

Reads the corpus only through stage-1 evidence (blind: no benchmark, no
historical decisions). Writes a semicolon-separated CSV for Excel in Italian
(source titles included: it is a working file, not for the public repository,
DEC-102) and a JSON twin. Doubt kinds:

  ZONA      urban zone whose QN page the sources disagree on, or have none
  LUOGO     a place named by the source (locality) against the page of the
            street it is on, within the same record
  STRADA    short street (<= 1.5 km) on more than one page: boundary or not
  TRATTO    long street on several pages: the default is "depends on the
            stretch"; listed so frequent ones can get a rule
  SENZA     QN locality routed to an inactive page (Agro Romano)
  C-R-nnnn  a rule a stage-2 reviewer contested in nota_geografia (--decisioni):
            the owner confirms it (ignora) or replaces it

The queue carries source titles, so --out must be outside the repository.
"""
import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import ROMAN as ROMAN_N, _metres, _segments, norm, package_root, rules_path  # noqa: E402
from stage1 import Stage1  # noqa: E402

SHORT_M = 1500
REPO = Path(__file__).resolve().parents[2]
RULE_ID = re.compile(r'\bR-\d{4}\b')


def fuori_dal_repository(path: Path) -> bool:
    """The queue carries source titles (DEC-102): it never lands in the worktree."""
    try:
        Path(path).resolve().relative_to(REPO)
    except ValueError:
        return True
    return False
COLUMNS = ['id_dubbio', 'tipo', 'luogo', 'municipio', 'opzioni', 'proposta', 'base_proposta',
           'schede', 'esempi', 'si_applica_in', 'tipo_regola', 'chiave', 'decisione', 'note']
HELP = ("decisione: uno slug (es. cinecitta) = una pagina; slug1+slug2 = entrambe "
        "(confine); tratto = dipende dal tratto; nessuna = luogo senza pagina attiva; "
        "ok = accetta la proposta; ignora = non e' un dubbio sulla mappa (falso allarme); "
        "vuoto = ancora aperto")


def road_length(at, key):
    return sum(_metres(a, b) for a, b in _segments(at._geom(key)))


def load_ev(path):
    return [json.loads(l) for l in Path(path).read_text(encoding='utf-8').splitlines() if l.strip()]


def build(pkg, evidence, seeds=None, decisions=None):
    s1 = Stage1(pkg)
    at = s1.at
    rows = {json.loads(l)['id']: json.loads(l) for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines() if l.strip()}
    decided_streets = {r['chiave'] for r in at.rules if r['tipo'] == 'strada'}
    decided_places = {r['chiave'] for r in at.rules if r['tipo'] == 'luogo'}
    rules_file = rules_path()
    store = json.loads(rules_file.read_text(encoding='utf-8')) if rules_file.is_file() else {}
    closed = {c['dubbio'] for c in store.get('chiusi', [])}
    # Every rule ever written, replaced ones included: their doubt stays decided.
    decided = closed | {r['dubbio'] for r in store.get('regole', [])}
    cross = json.loads((Path(__file__).resolve().parent / 'zone_qn_cross.json').read_text())['zone']
    out = []

    def example(ids):
        ids = sorted(ids)
        return ' | '.join(f"{i}: {rows[i]['titolo'][:70]}" for i in ids[:3])

    # who touches what
    zone_hits = collections.defaultdict(set)
    street_hits = collections.defaultdict(set)
    conflict = collections.defaultdict(set)
    inactive_hits = collections.defaultdict(set)
    for ev in evidence:
        i = ev['id']
        if rows[i]['in_stock'] != 1:
            continue
        for m in ev['menzioni']:
            if m['tipo'] == 'localita' and not m.get('scartata') and not set(m['pagine']) & at.active:
                inactive_hits[m['norm']].add(i)
            if m['tipo'] == 'strada' and len(m['chiavi']) == 1 and m.get('risoluzione'):
                pc = m.get('punto_civico') or {}
                if pc.get('trovato') and len({p for pt in pc['punti'] for p in pt['pagine']}) == 1:
                    continue        # the civic point settles this mention: no doubt about the street
                res = m['risoluzione'][0]
                for z in res['zone']:
                    zone_hits[str(z['code_zu']).upper()].add(i)
                ps = set(res.get('pagine_nel_municipio') or res['pagine']) & at.active
                if len(ps) > 1:
                    street_hits[res['chiave']].add(i)
        # A locality and a street read together ("piazza dei Tribuni, Quadraro",
        # "via X (Montagnola)"): same luoghi segment, or the locality within 40
        # characters after the street. Two places far apart in the text are a
        # multi-site record, not a doubt about the map.
        r = rows[i]
        mun = sorted(set(re.findall(r'\b[IVX]+\b', (r['municipio'] or '') + ' ' + (r['municipio_documento'] or ''))))
        units = [(seg, True) for seg in (r['luoghi'] or '').split(';') if seg.strip()]
        units += [(t, False) for t in (r['titolo'], r['sintesi'])]
        for text, whole in units:
            locs = [m for m in s1.localities(text, 'x', whole_segment=whole) if not m['scartata']]
            if not locs:
                continue
            for h in at.match_streets(text, mun):
                if len(h['chiavi']) != 1:
                    continue
                key = h['chiavi'][0]
                sp = set(at.strada(key, mun)['pagine']) & at.active
                if len(sp) != 1:
                    continue
                near = text if whole else text[h['span'][1]:h['span'][1] + 40]
                for m in locs:
                    lp = set(m['pagine']) & at.active
                    if lp and not lp & sp and m['testo'] in near and m['norm'] not in decided_places and key not in decided_streets:
                        conflict[(key, m['norm'])].add(i)

    # ZONA: every zone where the sources disagree or are silent
    for a in at.urban:
        code = str(a.props['code_zu']).upper()
        pages, source = at.zone_pages[code]
        gz = sorted(at.zu_pages.get(code, ()))
        own = a.props.get('qn_pages') or []
        cr = cross.get(code)
        named = sorted(at.loc.get(norm(a.props['denominazione']), set()))
        candidates = sorted(set(gz) | set(own) | set(cr or []) | set(named))
        inside = collections.Counter()
        if not candidates:
            # No source names a page: sample a grid inside the zone and read the
            # toponymic subdivision of each point, so the owner has options.
            x0, y0, x1, y1 = a.bbox
            for gx in range(1, 9):
                for gy in range(1, 9):
                    x, y = x0 + (x1 - x0) * gx / 9, y0 + (y1 - y0) * gy / 9
                    if a.contains(x, y):
                        inside.update(at.punto(y, x)['pagine'] or ['?'])
            candidates = sorted(p for p in inside if p != '?')
        disagree = len({tuple(sorted(x)) for x in (gz, own, cr or [], named) if x}) > 1
        if source.startswith('regola') or (source == 'gazetteer zu_code' and not disagree):
            continue
        if not (disagree or len(pages) != 1 or source == 'zone_qn_cross.json'):
            continue
        if source == 'gazetteer zu_code':
            prop, base, where = '+'.join(gz), 'gazetteer zu_code (tabella owner): prevale', 'gazetteer (gia deciso)'
        elif named and len(named) == 1:
            prop, base, where = named[0], f"localita QN omonima della zona ({a.props['denominazione']})", 'regole_geografiche'
        elif cr and len(cr) == 1:
            prop, base, where = cr[0], 'tabella cross storica (configurazione)', 'regole_geografiche'
        elif inside:
            top = inside.most_common(1)[0]
            share = top[1] / sum(inside.values())
            prop = top[0] if top[0] != '?' and share >= .8 else ''
            if prop and prop not in at.active:
                prop = 'nessuna'
            base = 'nessuna fonte: punti campionati nella zona per suddivisione toponomastica -> ' + \
                ', '.join(f'{p} {n}' for p, n in inside.most_common())
            where = 'regole_geografiche'
        else:
            prop, base, where = '', 'nessuna fonte univoca: decidere o lasciare per punto', 'regole_geografiche'
        zmun = ROMAN_N[int(a.props.get('municipi') or 0)] if str(a.props.get('municipi', '')).isdigit() else ''
        foreign = [p for p in candidates if zmun and at.page_mun.get(p) and zmun not in at.page_mun[p]]
        if foreign:
            base += f"; ATTENZIONE pagine di un altro municipio (zona nel {zmun}): {foreign}"
        out.append({'id_dubbio': f'Z-{code}', 'tipo': 'ZONA', 'luogo': f"zona urbanistica {code} {a.props['denominazione']}",
                    'municipio': str(a.props.get('municipi', '')), 'opzioni': '+'.join(candidates) or '-',
                    'proposta': prop, 'base_proposta': base + f"; fonti: gazetteer={gz or '-'} urban={own or '-'} cross={cr or '-'} nome={named or '-'}",
                    'schede': len(zone_hits.get(code, ())), 'esempi': example(zone_hits.get(code, ())),
                    'si_applica_in': where, 'tipo_regola': 'zona', 'chiave': code})

    # LUOGO: named locality against the street's page, same record
    for (key, loc), ids in conflict.items():
        sp = sorted(at.strada(key)['pagine'])
        lp = sorted(at.loc[loc] & at.active)
        out.append({'id_dubbio': f"L-{norm(key).replace(' ', '-')}--{loc.replace(' ', '-')}", 'tipo': 'LUOGO',
                    'luogo': f"{at.roads[key]['name'].lower()} citata con la localita {loc}",
                    'municipio': ','.join(at.roads[key]['municipi']), 'opzioni': '+'.join(sorted(set(sp) | set(lp))),
                    'proposta': lp[0] if len(lp) == 1 else '',
                    'base_proposta': f"la localita nominata prevale sulla zona (protocollo); strada -> {sp}, localita -> {lp}",
                    'schede': len(ids), 'esempi': example(ids), 'si_applica_in': 'regole_geografiche',
                    'tipo_regola': 'strada', 'chiave': key})

    # STRADA / TRATTO
    for key, ids in street_hits.items():
        if key in decided_streets:
            continue
        res = at.strada(key)
        length = road_length(at, key)
        fr = collections.Counter()
        for z in res['zone']:
            if len(z['pagine']) == 1:
                fr[z['pagine'][0]] += z['frazione']
            else:
                cv = {p: n for p, n in z.get('campioni_vertici', {}).items() if p != '?'}
                for p, n in cv.items():
                    fr[p] += z['frazione'] * n / sum(cv.values())
        pages = sorted(set(res.get('pagine_nel_municipio') or res['pagine']) & at.active)
        top = fr.most_common()
        short = length <= SHORT_M
        if short:
            share = top[0][1] / max(1e-9, sum(v for _, v in top)) if top else 0
            prop = top[0][0] if share >= .8 else '+'.join(p for p, _ in top[:2]) if share >= .35 else ''
            base = f"lunghezza {length:.0f} m; " + ('quote per zona: ' + ', '.join(f'{p} {v:.0%}' for p, v in top)
                                                    if top else 'campioni non conclusivi: guardare la mappa')
        else:
            prop, base = 'tratto', f"strada lunga {length / 1000:.1f} km su {len(pages)} pagine"
        out.append({'id_dubbio': f"S-{key.replace(' ', '-')}", 'tipo': 'STRADA' if short else 'TRATTO',
                    'luogo': res['nome'].lower(), 'municipio': ','.join(res['municipi']), 'opzioni': '+'.join(pages),
                    'proposta': prop, 'base_proposta': base, 'schede': len(ids), 'esempi': example(ids),
                    'si_applica_in': 'regole_geografiche', 'tipo_regola': 'strada', 'chiave': key})

    # SENZA: localities routed to an inactive page
    for loc, ids in inactive_hits.items():
        if loc in decided_places:
            continue
        out.append({'id_dubbio': f"N-{loc.replace(' ', '-')}", 'tipo': 'SENZA', 'luogo': f"localita {loc}",
                    'municipio': ','.join(sorted({v['municipio'] for v in at.loc_info.get(loc, [])})),
                    'opzioni': '+'.join(sorted(at.loc[loc])), 'proposta': 'nessuna',
                    'base_proposta': 'il gazetteer la instrada a una pagina non attiva: resta F salvo cambio della tabella',
                    'schede': len(ids), 'esempi': example(ids), 'si_applica_in': 'gazetteer (tabella owner)',
                    'tipo_regola': 'localita', 'chiave': loc})

    # Seeds: doubts found by reading (blind test arbitration), where the
    # place is named only by an outside source, so no text pattern finds it.
    for seed_file in seeds or []:
        for sd in json.loads(Path(seed_file).read_text(encoding='utf-8'))['dubbi']:
            out.append({'tipo': 'LUOGO', 'schede': len(sd.get('esempi_id', [])), 'esempi': example(sd.get('esempi_id', [])),
                        **{k: v for k, v in sd.items() if k != 'esempi_id'}})
    # Contested rules: a stage-2 decision that cites R-nnnn in nota_geografia
    # reopens it for the owner (protocol §6); the rule stays applied meanwhile.
    contested = collections.defaultdict(list)
    for d in decisions or []:
        for rid in RULE_ID.findall(d.get('nota_geografia') or ''):
            contested[rid].append((d.get('id'), (d.get('nota_geografia') or '')[:100]))
    kind_of = {'zona': 'ZONA', 'strada': 'STRADA', 'luogo': 'LUOGO'}
    for r in at.rules:
        if r['id'] not in contested:
            continue
        ids = [i for i, _ in contested[r['id']] if i in rows]
        out.append({'id_dubbio': f"C-{r['id']}", 'tipo': kind_of[r['tipo']],
                    'luogo': f"regola {r['id']} contestata in fase 2: {r['tipo']} {r['chiave']} -> {'+'.join(r['pagine']) or 'nessuna'} ({r['modo']})",
                    'municipio': '', 'opzioni': '+'.join(r['pagine']) or '-', 'proposta': '',
                    'base_proposta': 'contestata: ' + ' | '.join(f"{i}: {n}" for i, n in contested[r['id']]),
                    'schede': len(ids), 'esempi': example(ids), 'si_applica_in': 'regole_geografiche',
                    'tipo_regola': r['tipo'], 'chiave': r['chiave']})
    out = [r for r in out if r['id_dubbio'] not in decided]
    order = {'ZONA': 0, 'LUOGO': 1, 'STRADA': 2, 'SENZA': 3, 'TRATTO': 4}
    out.sort(key=lambda r: (order[r['tipo']], -r['schede'], r['id_dubbio']))
    for r in out:
        r.setdefault('decisione', '')
        r.setdefault('note', '')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--evidenze', required=True)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--semi', nargs='*', help='JSON files of seeded doubts (runs/*/semi_dubbi.json)')
    ap.add_argument('--decisioni', nargs='*', help='stage-2 decisioni.jsonl: rules contested in nota_geografia reopen')
    a = ap.parse_args()
    if not fuori_dal_repository(a.out):
        raise SystemExit('la coda contiene titoli delle fonti: --out deve stare fuori dal repository (DEC-102)')
    decisions = [d for f in (a.decisioni or []) for d in load_ev(f)]
    rows = build(package_root(a.pkg), load_ev(a.evidenze), a.semi, decisions)
    with a.out.open('w', encoding='utf-8-sig', newline='') as h:
        w = csv.DictWriter(h, fieldnames=COLUMNS, delimiter=';')
        w.writeheader()
        w.writerows(rows)
    a.out.with_suffix('.json').write_text(json.dumps({'istruzioni': HELP, 'dubbi': rows}, ensure_ascii=False, indent=1), encoding='utf-8')
    by = collections.Counter(r['tipo'] for r in rows)
    sch = collections.Counter()
    for r in rows:
        sch[r['tipo']] += r['schede']
    print(json.dumps({'dubbi_aperti': len(rows), 'per_tipo': dict(by), 'schede_coinvolte_per_tipo': dict(sch),
                      'out': str(a.out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

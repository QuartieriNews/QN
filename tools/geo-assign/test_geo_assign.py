#!/usr/bin/env python3
"""Executable acceptance for tools/geo-assign.

Pure checks run everywhere. Checks that need the Metodo QN package run only
when QN_PKG points at it (the package is not redistributed here, DEC-102),
and use the teaching cases of 03_CASI_RAGIONATI.md, never the held-out sample.

  python3 tools/geo-assign/test_geo_assign.py
"""
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qngeo  # noqa: E402
import valida  # noqa: E402

failures = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else f' -- {detail}'))
    if not cond:
        failures.append(name)


# ---- pure
check('norm folds accents, apostrophes, case', qngeo.norm("Campo de’ Fiori, Città") == 'campo de fiori citta')
sq = {'type': 'Polygon', 'coordinates': [[[0, 0], [4, 0], [4, 4], [0, 4], [0, 0]], [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]]}
a = qngeo.Area({}, sq)
check('point in polygon', a.contains(3, 3))
check('point in hole is outside', not a.contains(1.5, 1.5))
check('point outside', not a.contains(5, 5))
check('segment intersection', qngeo._seg_intersection((0, 0), (2, 2), (0, 2), (2, 0)) == (1.0, 1.0))
check('parallel segments do not intersect', qngeo._seg_intersection((0, 0), (1, 0), (0, 1), (1, 1)) is None)
cache = json.loads((HERE / 'zone_qn_cross.json').read_text())
check('cross table is versioned with provenance', cache.get('_versione') and cache.get('_provenienza'))

active = {'centocelle', 'nomentano'}
good = {'id': 'X', 'esito': 'U', 'pagine': ['centocelle'], 'fatto': 'f', 'motivo': 'm', 'confidenza': 'alta',
        'luoghi': [{'testo': 'via x', 'ruolo': 'intervento', 'usato': True, 'risoluzione': {'pagine': ['centocelle']}}]}
check('T-valida: well-formed U passes', valida.check(good, active) == [], valida.check(good, active))
check('T-valida: U page must follow from a used effective place',
      any('senza un luogo effettivo' in p for p in valida.check({**good, 'luoghi': [{**good['luoghi'][0], 'ruolo': 'provenienza'}]}, active)))
check('T-valida: D with pages rejected', any('cardinalita' in p for p in valida.check({**good, 'esito': 'D', 'tipo_dubbio': 'sede_da_riscontrare', 'verifica_necessaria': 'v'}, active)))
check('T-valida: D needs a known doubt type', any('tipo_dubbio' in p for p in valida.check({**good, 'esito': 'D', 'pagine': [], 'tipo_dubbio': 'boh', 'verifica_necessaria': 'v'}, active)))
check('T-valida: T needs a reason of scope', any('portata' in p for p in valida.check({**good, 'esito': 'T', 'pagine': []}, active)))
two = {**good, 'esito': 'M', 'pagine': ['centocelle', 'nomentano']}
check('T-valida: M needs two effective places', any('M richiede' in p or 'nomentano' in p for p in valida.check(two, active)))

# ---- package-backed (teaching cases only)
pkg = os.environ.get('QN_PKG')
if pkg and (Path(pkg) / 'cartografia' / 'road_index.json').is_file():
    import stage1
    at = qngeo.atlas(pkg)
    s1 = stage1.Stage1(Path(pkg))
    rows = {r['id']: r for r in stage1.load_input(Path(pkg))}

    def run(i):
        ev = s1.evidence(rows[i], [])
        return ev, s1.propose(rows[i], ev)

    x = at.incrocio('viale palmiro togliatti', 'via prenestina')
    check('N1887 crossing Togliatti-Prenestina is located geometrically in Centocelle',
          x['trovato'] and x['pagine'] == ['centocelle'], x.get('pagine'))
    ev, p = run('N2863')
    keys = {k for m in ev['menzioni'] if m['tipo'] == 'strada' for k in m['chiavi']}
    check('N2863 "via Aversa" in the title is read as via Raffaele Aversa', keys == {'via raffaele aversa'}, keys)
    check('weak surname form needs a visible end of name',
          at.match_streets('via di Porta San Paolo') == [] or all(
              'porta' not in h['variante'].split()[-1:] for h in at.match_streets('via di Porta San Paolo')))
    ev, p = run('N3129')
    check('N3129 locality inside a street name routed elsewhere is flagged',
          bool(ev['indizi'].get('localita_nel_nome_strada')) and p['priorita_revisione'] == 'alta')
    ev, p = run('N3519')
    check('N3519 "Ponte" inside "Torretta di Ponte Emilio" is not the Ponte rione',
          'centro-storico' not in p['pagine_proposte'], p['pagine_proposte'])
    ev, p = run('N2150')
    check('N2150 long road without tract is proposed D, pages left as candidates',
          p['esito_proposto'] == 'D' and not p['pagine_proposte'] and p['candidate'], p)
    ev, p = run('N1870')
    check('N1870 service of the whole Municipio is never auto-assigned without review',
          p['esito_proposto'] != 'U' or p['priorita_revisione'] == 'alta', p)
else:
    print('SKIP package-backed checks (set QN_PKG to the Metodo_QN package)')

print('ALL PASS' if not failures else f'{len(failures)} FAILED')
sys.exit(1 if failures else 0)

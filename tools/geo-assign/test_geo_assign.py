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
check('T-valida DEC-106: level of scope required from now on', any('livello_portata' in p for p in valida.check(good, active, require_level=True)))
check('T-valida DEC-106: a desk open day keeps its page and a municipal level',
      valida.check({**good, 'livello_portata': 'municipio'}, active, require_level=True) == [])
check('T-valida DEC-106: T cannot be of neighbourhood scope',
      any('contraddizione' in p for p in valida.check({**good, 'esito': 'T', 'pagine': [], 'portata': 'x', 'livello_portata': 'quartiere'}, active)))
edge = {**two, 'luoghi': [{'testo': 'via dei cerchi', 'ruolo': 'intervento', 'usato': True,
                                         'risoluzione': {'pagine': ['centocelle', 'nomentano'], 'regola': 'R-0003'}}]}
check('T-valida: a cited boundary rule allows M on one place', valida.check(edge, active) == [], valida.check(edge, active))

# ---- package-backed (teaching cases only)
# Deterministic: no live WFS and an empty civic cache during the tests.
import tempfile as _tf
os.environ['QN_RETE'] = '0'
os.environ['QN_CACHE'] = str(Path(_tf.mkdtemp()) / 'civici.json')
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
    ev, p = run('N0311')
    check('DEC-106: desk open day keeps the desk page with a municipal level',
          p['esito_proposto'] == 'U' and p['pagine_proposte'] == ['torre-angela'] and p['livello_proposto'] == 'municipio', p)
    ev, p = run('N0308')
    check('DEC-106: a council convocation gives the level, not the seat page',
          p['esito_proposto'] == 'T?' and not p['pagine_proposte'] and p['livello_proposto'] == 'municipio', p)
    ev, p = run('N2749')
    check('DEC-106: a norm on the centro storico is city news', p['esito_proposto'] == 'T?' and p['livello_proposto'] == 'citta', p)
    ev, p = run('N1870')
    check('N1870 service of the whole Municipio is never auto-assigned without review',
          p['esito_proposto'] != 'U' or p['priorita_revisione'] == 'alta', p)
    # ---- owner rules loop (temporary rules file: the real one is never touched)
    import csv
    import subprocess
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    rules = tmp / 'regole.json'
    rules.write_text(json.dumps({'regole': [], 'chiusi': []}))
    queue = tmp / 'coda.csv'
    cols = ['id_dubbio', 'tipo', 'luogo', 'municipio', 'opzioni', 'proposta', 'base_proposta', 'schede', 'esempi',
            'si_applica_in', 'tipo_regola', 'chiave', 'decisione', 'note']
    base = dict.fromkeys(cols, '')

    def write_queue(items):
        with queue.open('w', encoding='utf-8-sig', newline='') as h:
            w = csv.DictWriter(h, fieldnames=cols, delimiter=';')
            w.writeheader()
            w.writerows({**base, **it} for it in items)

    def apply(extra=()):
        extra = list(extra)
        env = {**os.environ, 'QN_REGOLE': str(rules)}
        return subprocess.run([sys.executable, str(HERE / 'applica_decisioni.py'), '--coda', str(queue), '--data', '2026-10-09']
                              + extra,
                              env=env, capture_output=True, text=True)

    write_queue([{'id_dubbio': 'Z-11E', 'tipo_regola': 'zona', 'chiave': '11E', 'si_applica_in': 'regole_geografiche',
                  'opzioni': 'ardeatino+montagnola', 'decisione': 'montagnola'}])
    res = apply()
    check('a zone rule contradicting the gazetteer zu_code is refused', res.returncode == 1 and 'gazetteer' in res.stdout, res.stdout)
    write_queue([{'id_dubbio': 'L-monte-del-grano', 'tipo_regola': 'luogo', 'chiave': 'monte del grano',
                  'si_applica_in': 'regole_geografiche', 'proposta': 'tuscolano-quadraro', 'decisione': 'ok'},
                 {'id_dubbio': 'S-via-dei-cerchi', 'tipo_regola': 'strada', 'chiave': 'via dei cerchi',
                  'si_applica_in': 'regole_geografiche', 'decisione': 'centro-storico+testaccio'},
                 {'id_dubbio': 'G-monti', 'tipo_regola': 'localita', 'chiave': 'monti',
                  'si_applica_in': 'gazetteer (tabella owner)', 'decisione': 'centro-storico'},
                 {'id_dubbio': 'L-falso', 'decisione': 'ignora'}])
    res = apply()
    check('DEC-107 open: a two-page decision is refused without --consenti-confine',
          res.returncode == 1 and 'DEC-107' in res.stdout, res.stdout)
    res = apply(['--consenti-confine'])
    stored = json.loads(rules.read_text())
    check('owner decisions become cited rules, a false alarm is closed',
          res.returncode == 0 and [r['modo'] for r in stored['regole']] == ['unica', 'doppia_confine']
          and stored['chiusi'][0]['dubbio'] == 'L-falso', res.stdout + res.stderr)
    check('a locality -> page change goes to the gazetteer table, never to a rule',
          (tmp / 'modifiche_gazetteer.csv').is_file() and all(r['dubbio'] != 'G-monti' for r in stored['regole']))
    check('a decided doubt is not applied twice', json.loads(apply(['--consenti-confine']).stdout)['regole_nuove'] == 0)
    os.environ['QN_REGOLE'] = str(rules)
    s1r = stage1.Stage1(Path(pkg))
    ev = s1r.evidence(rows['N3303'], [])
    p = s1r.propose(rows['N3303'], ev)
    check('a boundary rule assigns both pages of via dei Cerchi', set(p['pagine_proposte']) == {'centro-storico', 'testaccio'}, p)
    ev = s1r.evidence(rows['N0026'], [])
    check('a place rule is read as evidence and cited', any(m.get('regola') == 'R-0001' for m in ev['menzioni']))
    del os.environ['QN_REGOLE']
else:
    print('SKIP package-backed checks (set QN_PKG to the Metodo_QN package)')

print('ALL PASS' if not failures else f'{len(failures)} FAILED')
sys.exit(1 if failures else 0)

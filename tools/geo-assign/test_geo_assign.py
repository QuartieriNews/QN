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

# Codex review of PR #15, lotto 1 (15 October): boundary, crossings, cache, coreference, packets.
import tempfile as _tf
_deg = 0.0001                     # about 8 m east-west, 11 m north-south at Rome
check('boundary distance is zero on the edge and grows inside',
      qngeo._boundary_distance_m(0, 2, [[[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]]]) == 0
      and qngeo._boundary_distance_m(2 * _deg, 2 * _deg, [[[(0, 0), (4 * _deg, 0), (4 * _deg, 4 * _deg), (0, 4 * _deg), (0, 0)]]]) > 10)
# two zones side by side: the point 4 m from the shared edge is a boundary case
atl = qngeo.Atlas.__new__(qngeo.Atlas)
west = {'type': 'Polygon', 'coordinates': [[[12.5, 41.9], [12.501, 41.9], [12.501, 41.901], [12.5, 41.901], [12.5, 41.9]]]}
east = {'type': 'Polygon', 'coordinates': [[[12.501, 41.9], [12.502, 41.9], [12.502, 41.901], [12.501, 41.901], [12.501, 41.9]]]}
atl.urban = [qngeo.Area({'code_zu': '1A'}, west), qngeo.Area({'code_zu': '1B'}, east)]
atl.topo, atl.loc = [], {}
atl.zone_pages = {'1A': (['ovest'], 'test'), '1B': (['est'], 'test')}
pt = atl.punto(41.9005, 12.50095)
check('DEC-107: a point a few metres from the zone edge reports the pages across it',
      pt['pagine'] == ['ovest'] and pt.get('confine', {}).get('pagine_vicine') == ['est'] and pt['confine']['metri'] < 15, pt)
check('a point well inside its zone carries no boundary mark', 'confine' not in atl.punto(41.9005, 12.5005))
# a side street stopping 10 m short of a long road: found whichever order is asked
longroad = [((12.50, 41.90), (12.52, 41.90))]
side = [((12.51, 41.9001), (12.51, 41.902))]
d1, d2 = qngeo._closest_approach(longroad, side), qngeo._closest_approach(side, longroad)
check('crossing fallback is symmetric', d1 and d2 and abs(d1[0] - d2[0]) < 1e-6 and d1[0] < 15, (d1, d2))
# oblique segment: the metric distance equals the minimum over a dense sampling of the segment
_a, _b, _pt = (12.50, 41.90), (12.51, 41.91), (12.5052, 41.9048)
_d, _c = qngeo._pt_seg(_pt, _a, _b)
_brute = min(qngeo._metres(_pt, (_a[0] + k / 20000 * (_b[0] - _a[0]), _a[1] + k / 20000 * (_b[1] - _a[1]))) for k in range(20001))
check('point-segment distance is computed in local metres on oblique segments', abs(_d - _brute) < 0.05, (_d, _brute))
# cache: two writers, both entries survive, file always parseable
cpath = Path(_tf.mkdtemp()) / 'civici.json'
qngeo._cache_put(cpath, 'A|1', {'punti': []})
qngeo._cache_put(cpath, 'B|2', {'punti': []})
check('cache writes merge and replace atomically', set(json.loads(cpath.read_text())) == {'A|1', 'B|2'} and not list(cpath.parent.glob('*.tmp')))
empty = Path(_tf.mkdtemp()) / 'vuota.json'
empty.write_text('')
check('an empty cache file is an empty cache, as the README promises', qngeo._cache_read(empty) == {})
import stage1
m1 = {'variante': 'via aversa', 'livello_normalizzazione': 2, 'chiavi': ['via aversa']}
m2 = {'variante': 'via raffaele aversa', 'livello_normalizzazione': 0, 'chiavi': ['via raffaele aversa']}
m3 = {'variante': 'via giuseppe aversa', 'livello_normalizzazione': 0, 'chiavi': ['via giuseppe aversa']}
stage1.coreference([m1, m2])
check('a short form with one compatible full name is resolved', m1.get('coreferenza') == 'via raffaele aversa')
m1 = {'variante': 'via aversa', 'livello_normalizzazione': 2, 'chiavi': ['via aversa']}
stage1.coreference([m1, m2, m3])
check('two compatible full names stay an ambiguity, never the last one met',
      'coreferenza' not in m1 and m1.get('coreferenza_ambigua') == ['via giuseppe aversa', 'via raffaele aversa'], m1)
# proposal: ambiguous alias, approximated civic and boundary point are candidates, not evidence
s1 = stage1.Stage1.__new__(stage1.Stage1)
s1.at = type('A', (), {'active': {'ovest', 'est', 'nord'}})()
row = {'id': 'T1', 'titolo': 'Lavori in corso', 'sintesi': '', 'luoghi': ''}
cues = {'portata': [], 'multisede': [], 'tratto': [], 'sede_istituzionale': [], 'organo_o_sportello': [], 'municipi_nominati': []}
ev = {'menzioni': [{'tipo': 'localita', 'scartata': None, 'pagine': ['ovest', 'est'], 'campi': ['titolo'], 'supporto': 'forte'}],
      'incroci': [], 'indizi': cues, 'luoghi_non_risolti': []}
p = s1.propose(row, ev)
check('gazetteer on_ambiguous: an alias on two pages is D with both as candidates, not M',
      p['esito_proposto'] == 'D' and p['pagine_proposte'] == [] and p['candidate'] == ['est', 'ovest'], p)
civ = {'tipo': 'strada', 'scartata': None, 'campi': ['luoghi'], 'supporto': 'forte', 'chiavi': ['via x'], 'civico': 10,
       'risoluzione': [{'pagine': ['ovest'], 'zone_senza_pagina': []}],
       'punto_civico': {'trovato': True, 'punti': [{'pagine': ['ovest'], 'approssimato': 'civico 10 assente, usato 12 sullo stesso lato'}]}}
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('an approximated civic never makes a U on its own', p['esito_proposto'] == 'D' and p['candidate'] == ['ovest'], p)
civ['punto_civico'] = {'trovato': True, 'punti': [{'pagine': ['ovest'], 'confine': {'metri': 4.0, 'pagine_vicine': ['est']}}]}
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('DEC-107: a civic on the boundary is D with both pages as candidates', p['esito_proposto'] == 'D' and p['candidate'] == ['est', 'ovest'], p)
xing = {'strade': ['via a', 'via b'], 'pagine': ['ovest'], 'esatto': True, 'punti': [{'lat': 0, 'lon': 0, 'pagine': ['ovest'], 'base': 'b', 'confine': {'metri': 2.0, 'pagine_vicine': ['est']}}]}
p = s1.propose(row, {**ev, 'menzioni': [], 'incroci': [xing]})
check('DEC-107: a crossing on the boundary is D, not U', p['esito_proposto'] == 'D' and p['candidate'] == ['est', 'ovest'], p)
civ['punto_civico'] = {'trovato': True, 'punti': [{'pagine': ['ovest'], 'discordanza': True}]}
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('a civic whose cartographies disagree is a doubt to read, not a U', p['esito_proposto'] == 'D' and p['candidate'] == ['ovest'], p)
civ['punto_civico'] = {'trovato': True, 'punti': [{'pagine': ['ovest']}, {'pagine': ['est']}]}
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('exact civic points on two pages are D with both candidates, not the whole street',
      p['esito_proposto'] == 'D' and p['candidate'] == ['est', 'ovest'], p)
civ['punto_civico'] = {}
civ['risoluzione'] = [{'pagine': [], 'pagine_geometria': ['ovest'], 'zone_senza_pagina': [], 'regola': {'id': 'R-0007', 'modo': 'senza_pagina'}}]
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('an owner rule senza_pagina is applied and cited, never a U', p['esito_proposto'] != 'U' and any('R-0007' in r for r in p['ragioni']), p)
civ['punto_civico'] = {'trovato': True, 'punti': [{'pagine': ['ovest']}]}
p = s1.propose(row, {**ev, 'menzioni': [civ]})
check('senza_pagina on the street comes before a found civic point', p['esito_proposto'] != 'U' and any('R-0007' in r for r in p['ragioni']), p)
lr = {'tipo': 'luogo_regola', 'scartata': None, 'pagine': [], 'regola': 'R-0008', 'modo': 'senza_pagina', 'campi': ['titolo'], 'supporto': 'forte'}
p = s1.propose(row, {**ev, 'menzioni': [lr]})
check('a place rule senza_pagina is recognised and cited, not "nessun luogo riconosciuto"',
      p['esito_proposto'] == 'F?' and any('R-0008' in r for r in p['ragioni']), p)
check('"all\'altezza" survives normalisation in the crossing cue',
      stage1.CROSS.search(qngeo.norm("via A all'altezza della via B")) and stage1.CROSS.search(qngeo.norm('via A altezza di via B')))
xing3 = {'strade': ['via a', 'via b'], 'pagine': ['ovest'], 'esatto': False, 'distanza_m': 42.0,
         'punti': [{'lat': 0, 'lon': 0, 'pagine': ['ovest'], 'base': 'b'}]}
p = s1.propose(row, {**ev, 'menzioni': [], 'incroci': [xing3]})
check('a crossing the stradario does not contain is a lead (D), not a U', p['esito_proposto'] == 'D' and p['candidate'] == ['ovest'] and '42.0 m' in p['ragioni'][0], p)
xing2 = {'strade': ['via a', 'via b'], 'pagine': ['est', 'ovest'], 'esatto': True,
         'punti': [{'lat': 0, 'lon': 0, 'pagine': ['ovest'], 'base': 'b'}, {'lat': 1, 'lon': 1, 'pagine': ['est'], 'base': 'b'}]}
p = s1.propose(row, {**ev, 'menzioni': [], 'incroci': [xing2]})
check('roads meeting twice on two pages give D with both candidates, never ?', p['esito_proposto'] == 'D' and p['candidate'] == ['est', 'ovest'], p)
# packets: a place rule serialises, and the workspace is rebuilt on retry
import pacchetti
import subprocess
pm = pacchetti._mention({'tipo': 'luogo_regola', 'testo': 'monte del grano', 'campi': ['titolo'], 'supporto': 'forte',
                         'pagine': ['tuscolano-quadraro'], 'regola': 'R-0001', 'modo': 'unica'})
check('DEC-106: a place-rule mention is serialised with its rule, no street keys',
      pm.get('regola') == 'R-0001' and pm.get('pagine_regola') == ['tuscolano-quadraro'] and 'chiavi_stradario' not in pm, pm)
sm = pacchetti._mention({'tipo': 'strada', 'testo': 'via dei cerchi', 'campi': ['luoghi'], 'supporto': 'forte', 'chiavi': ['via dei cerchi'],
                         'civico': 5, 'punto_civico': {'trovato': True, 'fonte': 'copia offline', 'punti': [
                             {'id_civico': 1, 'pagine': ['centro-storico'], 'base': 'b', 'discordanza': True,
                              'zona_urbanistica': [{'code_zu': '1X', 'nome': 'Z', 'pagine': ['centro-storico']}],
                              'suddivisione': [{'tipo': 'Rione', 'nome': 'Ripa'}]}]},
                         'risoluzione': [{'chiave': 'via dei cerchi', 'municipi': ['I'], 'pagine': ['centro-storico', 'testaccio'],
                                          'pagine_geometria': ['centro-storico'], 'zone': [], 'zone_senza_pagina': [],
                                          'regola': {'id': 'R-0003', 'modo': 'doppia_confine'}}]})
check('DEC-106: the street rule id and the two cartographies of a discordant point reach the reader',
      sm['strada'][0].get('regola') == {'id': 'R-0003', 'modo': 'doppia_confine'} and sm['strada'][0]['pagine_geometria'] == ['centro-storico']
      and sm['civico_punti'][0]['discordanza'] and sm['civico_punti'][0]['suddivisione'] == [('Rione', 'Ripa')], sm)
sm2 = pacchetti._point({'pagine': ['a'], 'base': 'b', 'lat': 41.9, 'lon': 12.5, 'discordanza': True,
                        'zona_urbanistica': [{'code_zu': '1X', 'nome': 'Z', 'pagine': ['a'], 'fonte_raccordo': 'zone_qn_cross.json'}], 'suddivisione': []})
check('the source of each zone -> page link reaches the reader of a discordant point', sm2['zona_urbanistica'][0][3] == 'zone_qn_cross.json', sm2)
fake = Path(_tf.mkdtemp())
(fake / 'cartografia').mkdir(); (fake / 'cartografia' / 'road_index.json').write_text('[]')
(fake / 'cartografia' / 'marker_v1').write_text('1')
(fake / 'input').mkdir()
frow = {k: '' for k in pacchetti.FIELDS}; frow['id'] = 'N1'
(fake / 'input' / 'schede_input.jsonl').write_text(json.dumps(frow) + '\n')
fev = {'id': 'N1', 'municipi_contesto': [], 'menzioni': [], 'incroci': [], 'luoghi_non_risolti': [], 'indizi': {},
       'stessa_vicenda': [], 'proposta': {}}
work = Path(_tf.mkdtemp())
(work / 'ev.jsonl').write_text(json.dumps(fev) + '\n')
(work / 'ids.json').write_text(json.dumps({'ids': ['N1']}))
out = work / 'cieco'

def packets(lotti):
    return subprocess.run([sys.executable, str(HERE / 'pacchetti.py'), '--pkg', str(fake), '--evidenze', str(work / 'ev.jsonl'),
                           '--ids-file', str(work / 'ids.json'), '--lotti', str(lotti), '--out', str(out)],
                          capture_output=True, text=True)
r1 = packets(3)
(fake / 'cartografia' / 'marker_v1').unlink(); (fake / 'cartografia' / 'marker_v2').write_text('2')
r2 = packets(1)
check('packets: a retry rebuilds the blind copy and drops packets of the previous batch count',
      r1.returncode == 0 and r2.returncode == 0 and sorted(f.name for f in out.glob('lotto_*.jsonl')) == ['lotto_1.jsonl']
      and (out / 'pkg' / 'cartografia' / 'marker_v2').is_file() and not (out / 'pkg' / 'cartografia' / 'marker_v1').exists(),
      r1.stderr + r2.stderr)
check('DEC-106: the owner rules travel with the tools of the blind workspace',
      (out / 'strumenti' / 'regole_geografiche.json').is_file()
      and (out / 'strumenti' / 'regole_geografiche.json').read_bytes() == (HERE / 'regole_geografiche.json').read_bytes())
snap = {'regole': [{'id': 'R-9999', 'tipo': 'zona', 'chiave': '1A', 'pagine': ['x'], 'modo': 'unica', 'deciso_da': 'o', 'data': 'd', 'dubbio': 'q'}], 'chiusi': []}
(work / 'regole_geografiche.json').write_text(json.dumps(snap))
r3 = packets(1)
check('DEC-106: the rules snapshot left by stage 1 wins over the current file',
      r3.returncode == 0 and json.loads((out / 'strumenti' / 'regole_geografiche.json').read_text()) == snap
      and 'istantanea' in r3.stdout, r3.stdout + r3.stderr)
# qngeo: a street rule senza_pagina empties the pages and keeps the geometry for audit
atl2 = qngeo.Atlas.__new__(qngeo.Atlas)
atl2.roads = {'via x': {'key': 'via x', 'name': 'VIA X', 'municipi': ['I'], 'zones': [{'code': '1A', 'name': 'Z', 'fraction': 1.0}]}}
atl2.zone_pages = {'1A': (['ovest'], 'test')}
atl2.rules = [{'id': 'R-0007', 'tipo': 'strada', 'chiave': 'via x', 'pagine': [], 'modo': 'senza_pagina', 'deciso_da': 'o', 'data': 'd', 'dubbio': 'q'}]
atl2.page_mun, atl2._strada_cache = {}, {}
r = atl2.strada('via x')
check('qngeo applies a senza_pagina rule: no pages, geometry kept, rule cited',
      r['pagine'] == [] and r['pagine_geometria'] == ['ovest'] and r['regola']['id'] == 'R-0007', r)
atl2._build_street_trie()
hits = atl2.match_streets('via x, 2026-2027') + atl2.match_streets('via x, 12/05/2026')
check('a year or a date after the street name is not a civic number', hits and all(h['civico'] is None for h in hits), hits)
check('a plain civic number after a comma is still read', atl2.match_streets('via x, 17')[0]['civico'] == 17)

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

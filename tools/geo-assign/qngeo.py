#!/usr/bin/env python3
"""Offline QN geography: streets, civics, intersections, points -> QN pages.

Standard library only. Reads the cartography and gazetteer of the
"Metodo QN" package (path in --pkg or QN_PKG); never writes there, never
calls the network. Every answer carries the identifiers it rests on (road
key, zone code, toponymic subdivision, coordinates) so that a decision can
cite the query instead of "Geoportale" in general (Metodo QN §9, §13).

Two questions stay separate (Metodo QN §5): where a place is (zones,
subdivisions, point) and which QN page that place maps to (gazetteer).

CLI (JSON on stdout):
  qngeo.py strada "via raffaele aversa" [--mun IX]
  qngeo.py civico "via cassia" 472
  qngeo.py incrocio "viale palmiro togliatti" "via prenestina"
  qngeo.py punto 41.89 12.47
  qngeo.py localita "quarticciolo"
  qngeo.py pagine
"""
from __future__ import annotations

import argparse
import ast
import collections
import json
import math
import os
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
         'XI', 'XII', 'XIII', 'XIV', 'XV']
STREET_PREFIXES = {'via', 'viale', 'piazza', 'piazzale', 'largo', 'vicolo',
                   'corso', 'lungotevere', 'circonvallazione', 'salita',
                   'discesa', 'lungomare', 'piazzetta', 'borgo', 'clivo',
                   'passeggiata', 'galleria', 'scalinata', 'strada', 'vicolo',
                   'rampa', 'ponte', 'traversa', 'stradone', 'vialetto'}
WEAK_FOLLOWERS = {'n', 'numero', 'civico', 'civici', 'km', 'tra', 'fra', 'da', 'dal', 'dall', 'dalla',
                  'all', 'al', 'alla', 'lato', 'altezza', 'angolo', 'fronte', 'sede', 'scuola', 'municipio',
                  'presso', 'aula', 'area', 'cap', 'senza', 'parco', 'in', 'ed', 'e', 'con', 'dove',
                  'incrocio', 'direzione', 'strada', 'piazza', 'via', 'viale', 'largo', 'per', 'che',
                  'sono', 'nel', 'nella', 'a', 'ad', 'o', 'oppure', 'verso', 'fino', 'si', 'non', 'nei',
                  'sul', 'sulla', 'il', 'la', 'le', 'i', 'gli', 'lo', 'dove', 'quartiere', 'zona'}
ARTICLES = re.compile(r'\b(di|del|della|dei|degli|delle|dell|de|la|le|lo|il|l|d)\b')


def norm(s) -> str:
    """Comparison key: ASCII, lower case, alphanumerics separated by one space."""
    s = unicodedata.normalize('NFKD', str(s or '').replace('’', "'").replace('‘', "'"))
    s = s.encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def noart(k: str) -> str:
    return re.sub(' +', ' ', ARTICLES.sub('', k)).strip()


def package_root(explicit: str | None = None) -> Path:
    root = Path(explicit or os.environ.get('QN_PKG', ''))
    if not (root / 'cartografia' / 'road_index.json').is_file():
        raise SystemExit('Package not found: pass --pkg or set QN_PKG to the '
                         'Metodo_QN_per_Claude_Code folder')
    return root


def _read(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def _lit(v):
    return ast.literal_eval(v) if isinstance(v, str) else v


# ---------------------------------------------------------------- geometry
def _rings(geom):
    t, c = geom['type'], geom['coordinates']
    polys = [c] if t == 'Polygon' else c if t == 'MultiPolygon' else []
    return [[[(p[0], p[1]) for p in ring] for ring in poly] for poly in polys]


def _in_ring(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-300) + xi:
            inside = not inside
        j = i
    return inside


class Area:
    def __init__(self, props, geom):
        self.props = props
        self.polys = _rings(geom)
        xs = [p[0] for poly in self.polys for p in poly[0]]
        ys = [p[1] for poly in self.polys for p in poly[0]]
        self.bbox = (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)

    def contains(self, x, y):
        b = self.bbox
        if not (b[0] <= x <= b[2] and b[1] <= y <= b[3]):
            return False
        for poly in self.polys:
            if _in_ring(x, y, poly[0]) and not any(_in_ring(x, y, h) for h in poly[1:]):
                return True
        return False


def _segments(geom):
    t, c = geom['type'], geom['coordinates']
    lines = [c] if t == 'LineString' else c if t == 'MultiLineString' else []
    for line in lines:
        for a, b in zip(line, line[1:]):
            yield (a[0], a[1]), (b[0], b[1])


def _seg_intersection(p, p2, q, q2):
    r = (p2[0] - p[0], p2[1] - p[1])
    s = (q2[0] - q[0], q2[1] - q[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-18:
        return None
    t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / den
    u = ((q[0] - p[0]) * r[1] - (q[1] - p[1]) * r[0]) / den
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (p[0] + t * r[0], p[1] + t * r[1])
    return None


def _pt_seg(pt, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / L))
    c = (a[0] + t * dx, a[1] + t * dy)
    return _metres(pt, c), c


def _metres(a, b):
    # Equirectangular approximation at Rome's latitude: enough to compare
    # distances of a few hundred metres; not used for any boundary decision.
    kx = 111320 * math.cos(math.radians(41.9))
    return math.hypot((a[0] - b[0]) * kx, (a[1] - b[1]) * 110540)


# ---------------------------------------------------------------- the atlas
class Atlas:
    def __init__(self, pkg: Path):
        self.pkg = pkg
        carto = pkg / 'cartografia'
        self.gaz = _read(pkg / 'input' / 'gazetteer_qn.json')
        self.pages = {p['publication_zone_id']: p for p in self.gaz['publication_zones']}
        self.active = {k for k, p in self.pages.items() if p['is_page']}
        self.roads = {}
        for r in _read(carto / 'road_index.json'):
            self.roads[r['key']] = {
                'key': r['key'], 'name': r['name'],
                'municipi': [ROMAN[i] for i in _lit(r['municipi']) if 0 < i < len(ROMAN)],
                'zones': _lit(r['zones']), 'unmapped': _lit(r['unmapped_zones']),
                '_geom': r['geometry']}
        cross = _read(Path(__file__).resolve().parent / 'zone_qn_cross.json')['zone']
        self.zone_pages = {}            # code_zu -> (pages, source)
        self.urban = []
        for f in _read(carto / 'urban_mapped.json'):
            props = _lit(f['properties'])
            code = str(props['code_zu']).upper()
            own = props.get('qn_pages') or []
            self.zone_pages[code] = (own, 'urban_mapped') if own and code not in cross else \
                (cross[code], 'zone_qn_cross.json') if code in cross else ([], 'nessuna')
            self.urban.append(Area(props, _lit(f['geometry'])))
        self.topo = [Area(f['properties'], f['geometry'])
                     for f in _read(carto / 'topo.geojson')['features']]
        self.civics = collections.defaultdict(list)
        for f in _read(carto / 'civics_v2.geojson')['features']:
            p = f['properties']
            self.civics[(norm(p['TOPONIMO']), int(p['NUMERO_CIVICO']))].append(
                {'id_civico': p.get('ID_CIVICO'), 'lettera': p.get('LETTERA'),
                 'coord': f['geometry']['coordinates'][:2], 'layer': 'DIPCUL:GeoromaCiviciLocator'})
        for key, items in _read(carto / 'spatial_evidence.json')['civics'].items():
            name, num = key.rsplit('|', 1)
            for it in items:
                p = it['properties']
                k = (norm(name), int(num))
                if not any(c['id_civico'] == p.get('ID_CIVICO') for c in self.civics[k]):
                    self.civics[k].append({'id_civico': p.get('ID_CIVICO'), 'lettera': p.get('LETTERA'),
                                           'coord': it['coordinates'][:2],
                                           'layer': 'DIPCUL:GeoromaCiviciLocator'})
        self._strada_cache = {}
        self._build_localities()
        self._build_street_trie()

    # ------------------------------------------------ gazetteer localities
    def _build_localities(self):
        self.loc = collections.defaultdict(set)      # norm alias -> pages
        self.loc_info = collections.defaultdict(list)
        for n in self.gaz['neighbourhoods']:
            for a in [n['name_display']] + [x for x in re.split(r'[;|]', n['aliases']) if x.strip()]:
                k = norm(a)
                if k:
                    self.loc[k].add(n['publication_zone_id'])
                    self.loc_info[k].append({'neighbourhood_id': n['neighbourhood_id'],
                                             'page': n['publication_zone_id'],
                                             'municipio': n['municipality_code'],
                                             'zu_code': n['zu_code']})
        for k, p in self.pages.items():
            self.loc[norm(p['name_display'])].add(k)
        self.zu_pages = collections.defaultdict(set)
        for n in self.gaz['neighbourhoods']:
            for code in re.split(r'[;|, ]+', n['zu_code'] or ''):
                if code:
                    self.zu_pages[code.upper()].add(n['publication_zone_id'])
        self.page_mun = collections.defaultdict(set)
        for n in self.gaz['neighbourhoods']:
            self.page_mun[n['publication_zone_id']].update(
                re.findall(r'\b[IVX]+\b', n['municipality_code'] + ';' + n['spans_municipalities']))
        for k, p in self.pages.items():
            self.page_mun[k].update(re.findall(r'\b[IVX]+\b', p['primary_municipality'] + ';' + p['spans_municipalities']))

    def localita(self, name):
        k = norm(name)
        return {'query': name, 'norm': k, 'pagine': sorted(self.loc.get(k, ())),
                'voci': self.loc_info.get(k, []),
                'pagine_attive': sorted(self.loc.get(k, set()) & self.active)}

    # ------------------------------------------------ street names
    def _build_street_trie(self):
        variants = collections.defaultdict(dict)   # variant -> {key: level}

        def add(v, key, level):
            if v:
                variants[v][key] = min(level, variants[v].get(key, level))
        for k in self.roads:
            add(k, k, 0)
            add(noart(k), k, 0)
            w = k.split()
            if w[0] in {'via', 'viale', 'piazza', 'piazzale'}:
                alt = {'via': 'viale', 'viale': 'via', 'piazza': 'piazzale', 'piazzale': 'piazza'}[w[0]]
                add(alt + ' ' + ' '.join(w[1:]), k, 1)
            if len(w) >= 3 and w[0] in STREET_PREFIXES:
                # initial + surname, surname only: weaker forms (level 2), kept
                # only when nothing stronger matches and recorded as such.
                add(w[0] + ' ' + w[1][0] + ' ' + ' '.join(w[2:]), k, 2)
                for n in range(1, min(4, len(w) - 1)):
                    tail = w[-n:]
                    if len(''.join(tail)) >= 5 and tail[0] not in {'di', 'del', 'della', 'san', 'santa'}:
                        add(w[0] + ' ' + ' '.join(tail), k, 2)
        self.variants = variants
        trie = {}
        for v, keys in variants.items():
            node = trie
            for tok in v.split():
                node = node.setdefault(tok, {})
            node['$'] = v
        self.trie = trie

    def match_streets(self, text, municipi=()):
        """Longest-match street mentions with civic numbers. Ambiguity is kept,
        never resolved by picking the first key (Metodo QN §7)."""
        toks = [(m.group(), m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9]+', _ascii(text))]
        words = [t[0].lower() for t in toks]
        hits, i = [], 0
        while i < len(words):
            if words[i] not in STREET_PREFIXES:
                i += 1
                continue
            node, found = self.trie, []
            for j in range(i, len(words)):
                if words[j] not in node:
                    break
                node = node[words[j]]
                if '$' in node:
                    found.append((j + 1, node['$']))
            # article-insensitive retry ("via del passo del turchino")
            if not found:
                stripped = [(j, w) for j, w in enumerate(words[i:], i) if not ARTICLES.fullmatch(w)]
                node = self.trie
                for j, w in stripped:
                    if w not in node:
                        break
                    node = node[w]
                    if '$' in node:
                        found.append((j + 1, node['$']))
            if not found:
                i += 1
                continue
            end, var = max(found, key=lambda x: x[0])
            levels = self.variants[var]
            best = min(levels.values())
            # A weak form (swapped prefix, initial, surname only) counts only
            # when the name visibly ends there: civic, punctuation, connector.
            # "via di Porta San Paolo" is not "via Porta" + noise.
            if best and end < len(words):
                gap = _ascii(text)[toks[end - 1][2]:toks[end][1]]
                if not (re.search(r'[,;:.()]', gap) or words[end].isdigit() or words[end] in WEAK_FOLLOWERS):
                    i += 1
                    continue
            keys = sorted(k for k, lv in levels.items() if lv == best)
            narrowed = keys
            if len(keys) > 1 and municipi:
                within = [k for k in keys if set(self.roads[k]['municipi']) & set(municipi)]
                if within:
                    narrowed = within
            civic = None
            m = re.match(r'\s*,?\s*(?:n\.?\s*|numero\s+|civico\s+|civ\.\s*)?(\d{1,5})(?![\d/.]*\s*(?:euro|anni|metri|mq|%|gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre))',
                         _ascii(text)[toks[end - 1][2]:])
            if m and not re.match(r'\s*\d{4}\s*[-–]', _ascii(text)[toks[end - 1][2]:]):
                civic = int(m.group(1))
            hits.append({'testo': text[toks[i][1]:toks[end - 1][2]], 'variante': var,
                         'livello_normalizzazione': best, 'chiavi': narrowed,
                         'chiavi_prima_del_municipio': keys if narrowed != keys else None,
                         'civico': civic, 'span': [toks[i][1], toks[end - 1][2]]})
            i = end
        return hits

    # ------------------------------------------------ resolution
    def strada(self, key, municipi=()):
        """Pages a street touches. Zones mapped to one page count directly; for
        zones with no page or several, the street's own vertices inside them
        are classified point by point (rione, zone, toponymic quartiere)."""
        ck = (key, tuple(sorted(municipi)))
        if ck in self._strada_cache:
            return json.loads(self._strada_cache[ck])
        out = self._strada(key, municipi)
        self._strada_cache[ck] = json.dumps(out)
        return out

    def _strada(self, key, municipi):
        r = self.roads[key]
        zones = list(r['zones'])
        if any(z.get('fraction', 1) > .9 for z in zones):
            zones = [z for z in zones if z.get('fraction', 1) >= .03]
        pages, detail, unresolved = set(), [], []
        verts = None
        for z in zones:
            code = str(z['code']).upper()
            zp, src = self.zone_pages.get(code, (z.get('qn_pages') or [], 'road_index'))
            item = {'code_zu': z['code'], 'nome': z['name'], 'frazione': round(z.get('fraction', 1), 3),
                    'pagine': zp, 'fonte_raccordo': src}
            if len(zp) != 1:
                if verts is None:
                    verts = self._vertices(key)
                sub = collections.Counter()
                for x, y in verts:
                    pt = self.punto(y, x)
                    if any(str(u['code_zu']).upper() == code for u in pt['zona_urbanistica']):
                        sub.update(pt['pagine'] if len(pt['pagine']) == 1 else ['?'])
                item['campioni_vertici'] = dict(sub)
                zp = [p for p in sub if p != '?'] or zp
                if not zp:
                    unresolved.append(z['name'])
            pages.update(zp)
            detail.append(item)
        out = {'chiave': key, 'nome': r['name'], 'municipi': r['municipi'], 'zone': detail,
               'zone_senza_pagina': unresolved, 'pagine': sorted(pages),
               'layer': 'DIPPC:stradario_municipio x DIPPC:rc_zone_urbanistiche (+ DIPSER:SuddivisioniToponomastica)'}
        if municipi and len(pages) > 1:
            kept = sorted(p for p in pages if self.page_mun[p] & set(municipi))
            if kept and len(kept) < len(pages):
                out['pagine_nel_municipio'] = kept
        return out

    def _vertices(self, key, limit=60):
        pts = []
        for a, b in _segments(self._geom(key)):
            pts.append(a)
            pts.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        step = max(1, len(pts) // limit)
        return pts[::step]

    def civico(self, key_or_name, num):
        k = norm(key_or_name)
        found = self.civics.get((k, int(num))) or self.civics.get((noart(k), int(num)))
        if not found:
            return {'query': [key_or_name, num], 'trovato': False,
                    'nota': 'civico assente dalla copia offline: serve DIPCUL:GeoromaCiviciLocator (rete)'}
        res = {'query': [key_or_name, num], 'trovato': True, 'punti': []}
        for c in found:
            res['punti'].append({**c, **self.punto(c['coord'][1], c['coord'][0])})
        return res

    def punto(self, lat, lon):
        x, y = float(lon), float(lat)
        urb = [a.props for a in self.urban if a.contains(x, y)]
        top = [a.props for a in self.topo if a.contains(x, y)]
        via_topo = set()
        for t in top:
            via_topo |= self.loc.get(norm(t['DESCRIZIONE']), set())
        via_zone = set()
        for u in urb:
            via_zone |= set(self.zone_pages.get(str(u.get('code_zu', '')).upper(), ([], ''))[0])
        # A rione is finer than an urban zone, a toponymic quartiere is coarser
        # (Collatino spans several QN pages): rione first, then the urban
        # zone, then the quartiere. Disagreement is reported, not hidden.
        rione = {p for t in top if t['TIPOLOGIA'] == 'Rione' for p in self.loc.get(norm(t['DESCRIZIONE']), ())}
        if len(rione) == 1:
            pages, basis = rione, 'rione -> gazetteer'
        elif len(via_zone) == 1:
            pages, basis = via_zone, 'zona urbanistica -> pagine QN'
        elif len(via_topo) == 1:
            pages, basis = via_topo, 'suddivisione toponomastica -> gazetteer'
        else:
            pages, basis = via_topo | via_zone, 'piu pagine possibili: serve contesto'
        return {'lat': y, 'lon': x,
                'zona_urbanistica': [{'code_zu': u.get('code_zu'), 'nome': u.get('denominazione'),
                                      'pagine': self.zone_pages[str(u.get('code_zu')).upper()][0],
                                      'fonte_raccordo': self.zone_pages[str(u.get('code_zu')).upper()][1]} for u in urb],
                'suddivisione': [{'tipo': t['TIPOLOGIA'], 'nome': t['DESCRIZIONE'],
                                  'codice': t.get('CODICE_SUDDIVISIONE')} for t in top],
                'pagine': sorted(pages), 'base': basis,
                'discordanza': bool(via_topo and via_zone and not (via_topo & via_zone))}

    @lru_cache(maxsize=4096)
    def _geom(self, key):
        return _lit(self.roads[key]['_geom'])

    def incrocio(self, key_a, key_b, tol_m=60):
        sa, sb = list(_segments(self._geom(key_a))), list(_segments(self._geom(key_b)))
        pts = []
        for a1, a2 in sa:
            ax0, ax1 = sorted((a1[0], a2[0])); ay0, ay1 = sorted((a1[1], a2[1]))
            for b1, b2 in sb:
                if max(b1[0], b2[0]) < ax0 or min(b1[0], b2[0]) > ax1 or max(b1[1], b2[1]) < ay0 or min(b1[1], b2[1]) > ay1:
                    continue
                p = _seg_intersection(a1, a2, b1, b2)
                if p:
                    pts.append(p)
        exact = bool(pts)
        if not pts:
            best = None
            for a1, a2 in sa:
                for v in (a1, a2):
                    for b1, b2 in sb:
                        d, c = _pt_seg(v, b1, b2)
                        if best is None or d < best[0]:
                            best = (d, ((v[0] + c[0]) / 2, (v[1] + c[1]) / 2))
            if best and best[0] <= tol_m:
                pts = [best[1]]
        if not pts:
            return {'strade': [key_a, key_b], 'trovato': False,
                    'nota': 'le due strade non si toccano nella copia dello stradario'}
        # Several crossings (roads meeting twice) are reported separately.
        clusters = []
        for p in pts:
            for c in clusters:
                if _metres(p, c[0]) < 150:
                    c.append(p)
                    break
            else:
                clusters.append([p])
        out = []
        for c in clusters:
            x = sum(p[0] for p in c) / len(c)
            y = sum(p[1] for p in c) / len(c)
            out.append(self.punto(y, x))
        return {'strade': [key_a, key_b], 'trovato': True, 'esatto': exact, 'punti': out,
                'pagine': sorted({p for o in out for p in o['pagine']})}


def _ascii(s):
    # Same length as the input so spans stay valid.
    return ''.join(c if ord(c) < 128 else (unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()[:1] or ' ')
                   for c in str(s or ''))


@lru_cache(maxsize=2)
def atlas(pkg: str) -> Atlas:
    return Atlas(Path(pkg))


def _resolve_key(at: Atlas, text):
    k = norm(text)
    if k in at.roads:
        return [k]
    hits = at.match_streets(text)
    return hits[0]['chiavi'] if hits else []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('strada'); s.add_argument('testo'); s.add_argument('--mun', nargs='*', default=[])
    c = sub.add_parser('civico'); c.add_argument('via'); c.add_argument('numero', type=int)
    i = sub.add_parser('incrocio'); i.add_argument('via_a'); i.add_argument('via_b')
    p = sub.add_parser('punto'); p.add_argument('lat', type=float); p.add_argument('lon', type=float)
    l = sub.add_parser('localita'); l.add_argument('nome')
    sub.add_parser('pagine')
    a = ap.parse_args(argv)
    at = atlas(str(package_root(a.pkg)))
    if a.cmd == 'strada':
        hits = at.match_streets(a.testo, a.mun) or [{'chiavi': _resolve_key(at, a.testo), 'testo': a.testo}]
        out = [{**h, 'risoluzione': [at.strada(k, a.mun) for k in h['chiavi']]} for h in hits]
    elif a.cmd == 'civico':
        keys = _resolve_key(at, a.via)
        out = [at.civico(at.roads[k]['name'], a.numero) for k in keys] or {'errore': 'strada non trovata'}
    elif a.cmd == 'incrocio':
        ka, kb = _resolve_key(at, a.via_a), _resolve_key(at, a.via_b)
        out = [at.incrocio(x, y) for x in ka for y in kb] or {'errore': 'strada non trovata', 'a': ka, 'b': kb}
    elif a.cmd == 'punto':
        out = at.punto(a.lat, a.lon)
    elif a.cmd == 'localita':
        out = at.localita(a.nome)
    else:
        out = [{'slug': k, 'nome': p['name_display'], 'attiva': p['is_page'],
                'municipio': p['primary_municipality']} for k, p in sorted(at.pages.items())]
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == '__main__':
    main()

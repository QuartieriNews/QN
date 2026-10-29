# Metodo 2: dove OpenStreetMap non dà un toponimo, usa (a) le Suddivisioni toponomastiche ufficiali del Geoportale,
# (b) il toponimo del gazetteer più vicino nello stesso municipio ufficiale (stima), più le coordinate dei luoghi di culture.roma.it.
import sys, json, re, unicodedata, math, collections
import openpyxl
from openpyxl.styles import Font
S, UNICO, GAZ = sys.argv[1], sys.argv[2], sys.argv[3]
gz = json.load(open(GAZ)); SUD = json.load(open(f'{S}/geo/suddivisioni.json'))['features']; MUN = json.load(open(f'{S}/geo/municipi.json'))['features']
GP = [p for p in json.load(open(f'{S}/geo/gazetteer_punti.json')) if p.get('lat')]
LUOGHI = json.load(open(f'{S}/culture/luoghi.json')) if __import__('os').path.exists(f'{S}/culture/luoghi.json') else {}
cul = {x['url']: x for x in json.load(open(f'{S}/culture/items.json')) if not x.get('seed')}
def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode().lower(); s = re.sub(r"\bs\.\s*", 'san ', s); return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]+', ' ', s)).strip()
names = {}
for n in gz['neighbourhoods']:
    for a in [n['name_display']] + re.split(r'[;|/]', n.get('aliases') or ''):
        if norm(a): names.setdefault(norm(a), n); names.setdefault(norm(a).replace(' ', ''), n)
zones = {z['publication_zone_id']: z for z in gz['publication_zones']}
for z in gz['publication_zones']: names.setdefault(norm(z['name_display']), {'neighbourhood_id': None, 'name_display': z['name_display'], 'publication_zone_id': z['publication_zone_id'], 'municipality_code': z['primary_municipality'], 'publishable': z['is_page']})
def match_name(c0, mun):
    forms = [norm(c0), norm(c0).replace(' ', '')]
    for part in re.split(r'\s*[-–/]\s*|\s+e\s+', c0): forms += [norm(part), norm(part).replace(' ', '')]
    w = norm(c0).split()
    for k in range(len(w) - 1, 0, -1): forms.append(' '.join(w[:k]))
    forms.append(re.sub(r'^(quartiere|rione|zona|borgata|lido di) ', '', norm(c0)))
    if norm(c0) == 'europa': forms.append('eur')
    for f in forms:
        n = names.get(f)
        if n and n.get('publishable', True) and (not mun or not n.get('municipality_code') or n['municipality_code'] == mun): return n
    return None
def _pip(x, y, poly):
    inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i][:2]; x2, y2 = poly[(i + 1) % n][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-300) + x1: inside = not inside
    return inside
def inside(lat, lon, geom):
    if not geom: return False
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    return any(_pip(float(lon), float(lat), p[0]) and not any(_pip(float(lon), float(lat), h) for h in p[1:]) for p in polys if p and p[0])
def municipio(lat, lon):
    return next((f['properties'].get('numero_rom') for f in MUN if inside(lat, lon, f['geometry'])), None)
def suddivisione(lat, lon):
    return next((f['properties'] for f in SUD if inside(lat, lon, f['geometry'])), None)
def dist(lat1, lon1, lat2, lon2):
    p = math.pi / 180; a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a))
def nearest(lat, lon, mun):
    best = None
    for p in GP:
        if not p['pubblicabile'] or p['tipo'] != 'toponimo': continue
        if mun and p['municipio'] and p['municipio'] != mun: continue
        d = dist(float(lat), float(lon), p['lat'], p['lon'])
        if best is None or d < best[0]: best = (d, p)
    return best
wb = openpyxl.load_workbook(UNICO); ws = wb['Eventi unificati']; h = [c.value for c in ws[1]]; g = lambda r, k: r[h.index(k)]
for col in ('zona_qn_metodo2', 'zona_qn_metodo2_nome', 'metodo2', 'suddivisione_ufficiale'):
    if col not in h: ws.cell(1, len(h) + 1, col).font = Font(bold=True); h.append(col)
stats = collections.Counter(); sudd_stats = collections.Counter()
for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
    r = list(r); f = g(r, 'fonte'); lat, lon = g(r, 'lat'), g(r, 'lon')
    # coordinate del luogo di culture.roma.it se mancano o se la riga è stata geocodificata per indirizzo
    if f.startswith('Comune'):
        vu = (cul.get(g(r, 'url')) or {}).get('venueUrl'); L = LUOGHI.get(vu) or {}
        if L.get('lat') and (not lat or 'indirizzo geocodificato' in str(g(r, 'geo_metodo') or '')):
            lat, lon = L['lat'], L['lon']; ws.cell(i, h.index('lat') + 1, lat); ws.cell(i, h.index('lon') + 1, lon)
            ws.cell(i, h.index('geo_metodo') + 1, 'coordinate del luogo su culture.roma.it'); ws.cell(i, h.index('geo_nota') + 1, None)
            m = municipio(lat, lon); ws.cell(i, h.index('municipio_assegnato') + 1, m)
    sd = suddivisione(lat, lon) if lat and lon else None
    ws.cell(i, h.index('suddivisione_ufficiale') + 1, f"{sd['TIPOLOGIA']} {sd['DESCRIZIONE']} ({sd['CODICE_NOME']})" if sd else None)
    if sd: sudd_stats[sd['TIPOLOGIA']] += 1
    if g(r, 'zona_qn') or not lat or not lon: stats['già assegnato' if g(r, 'zona_qn') else 'senza punto'] += 1; continue
    mun = g(r, 'municipio_assegnato') or municipio(lat, lon)
    if not mun: stats['fuori Roma'] += 1; continue
    n = match_name(sd['DESCRIZIONE'], mun) if sd else None
    if n:
        ws.cell(i, h.index('zona_qn_metodo2') + 1, n['publication_zone_id']); ws.cell(i, h.index('zona_qn_metodo2_nome') + 1, zones.get(n['publication_zone_id'], {}).get('name_display'))
        ws.cell(i, h.index('metodo2') + 1, f"suddivisione toponomastica ufficiale: {sd['TIPOLOGIA']} {sd['DESCRIZIONE']}"); stats['suddivisione ufficiale'] += 1; continue
    b = nearest(lat, lon, mun)
    if b and b[0] <= 2.0:
        d, p = b; ws.cell(i, h.index('zona_qn_metodo2') + 1, p['zona']); ws.cell(i, h.index('zona_qn_metodo2_nome') + 1, zones.get(p['zona'], {}).get('name_display'))
        ws.cell(i, h.index('metodo2') + 1, f"stima: toponimo più vicino '{p['nome']}' a {d:.1f} km" + (f"; suddivisione ufficiale '{sd['DESCRIZIONE']}' non nel gazetteer" if sd else '; nessuna suddivisione ufficiale con geometria')); stats['toponimo più vicino (stima)'] += 1
    else:
        ws.cell(i, h.index('metodo2') + 1, 'nessun toponimo entro 2 km' + (f"; suddivisione ufficiale '{sd['DESCRIZIONE']}' non nel gazetteer" if sd else '')); stats['non risolto'] += 1
wb.save(UNICO)
print(dict(stats)); print('suddivisioni trovate per tipo', dict(sudd_stats))

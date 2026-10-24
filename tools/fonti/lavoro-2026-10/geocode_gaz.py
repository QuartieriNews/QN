# Geocodifica i toponimi del gazetteer (Nominatim, 1 richiesta/s) e li valida nel municipio ufficiale.
import sys, json, time, os, urllib.request, urllib.parse, re
S, GAZ = sys.argv[1], sys.argv[2]
gz = json.load(open(GAZ)); MUN = json.load(open(f'{S}/geo/municipi.json'))['features']
UA = 'QuartieriNews-eventi/1.0 (contatto: redazione)'
CACHE = f'{S}/geo/cache.json'; cache = json.load(open(CACHE))
def call(url):
    if url in cache: return cache[url]
    for t in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30) as r: d = json.loads(r.read().decode())
            cache[url] = d; time.sleep(1.1); return d
        except Exception as e: time.sleep(3)
    return []
def _pip(x, y, poly):
    inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i][:2]; x2, y2 = poly[(i + 1) % n][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-300) + x1: inside = not inside
    return inside
def mun_of(lat, lon):
    for f in MUN:
        g_ = f['geometry']; polys = g_['coordinates'] if g_['type'] == 'MultiPolygon' else [g_['coordinates']]
        for p in polys:
            if _pip(float(lon), float(lat), p[0]) and not any(_pip(float(lon), float(lat), h) for h in p[1:]): return f['properties'].get('numero_rom')
    return None
out = []
items = [(n['neighbourhood_id'], n['name_display'], n['municipality_code'], n['publication_zone_id'], n['publishable'], 'toponimo') for n in gz['neighbourhoods']] + [(z['publication_zone_id'], z['name_display'], z['primary_municipality'], z['publication_zone_id'], z['is_page'], 'pagina') for z in gz['publication_zones']]
for i, (nid, name, mun, zone, pub, kind) in enumerate(items):
    q = re.sub(r'\s*\(.*?\)', '', name)
    res = None
    for query in (f'{q}, Roma', f'{q}, Municipio Roma {mun}, Roma' if mun else None):
        if not query: continue
        d = call('https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': query, 'format': 'jsonv2', 'limit': 5, 'countrycodes': 'it', 'accept-language': 'it'}))
        for x in (d if isinstance(d, list) else []):
            m = mun_of(x['lat'], x['lon'])
            if m and (not mun or m == mun or '/' in str(mun)): res = {'lat': float(x['lat']), 'lon': float(x['lon']), 'osm_type': x.get('type'), 'osm_class': x.get('class'), 'display': x.get('display_name'), 'mun_poligono': m}; break
        if res: break
    out.append({'id': nid, 'nome': name, 'municipio': mun, 'zona': zone, 'pubblicabile': pub, 'tipo': kind, **(res or {'lat': None})})
    if i % 40 == 0: print(i, name, '->', (res or {}).get('display', 'NON TROVATO')[:60] if res else 'NON TROVATO', flush=True); json.dump(cache, open(CACHE, 'w'), ensure_ascii=False)
json.dump(cache, open(CACHE, 'w'), ensure_ascii=False); json.dump(out, open(f'{S}/geo/gazetteer_punti.json', 'w'), ensure_ascii=False, indent=1)
print('DONE', sum(1 for o in out if o['lat']), '/', len(out))

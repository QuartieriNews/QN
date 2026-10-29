# Geocodifica con Nominatim (1 richiesta/s, cache): reverse sui punti, ricerca sugli indirizzi.
import sys, re, json, time, os, urllib.request, urllib.parse
import openpyxl
S, UNICO = sys.argv[1], sys.argv[2]
UA = 'QuartieriNews-eventi/1.0 (contatto: redazione)'
CACHE = f'{S}/geo/cache.json'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def call(url):
    if url in cache: return cache[url]
    for t in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'it'})
            with urllib.request.urlopen(req, timeout=30) as r: d = json.loads(r.read().decode())
            cache[url] = d; time.sleep(1.1); return d
        except Exception as e:
            time.sleep(3 * (t + 1)); err = str(e)
    cache[url] = {'error': err[:100]}; return cache[url]
def save(): json.dump(cache, open(CACHE, 'w'), ensure_ascii=False)
def reverse(lat, lon):
    return call(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2&zoom=18&addressdetails=1&accept-language=it')
def search(street=None, city='Roma', q=None):
    p = {'format': 'jsonv2', 'limit': 1, 'addressdetails': 1, 'accept-language': 'it', 'countrycodes': 'it'}
    if q: p['q'] = q
    else: p['street'] = street; p['city'] = city
    return call('https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(p))
from parse_dove import parse_dove, VIE
wb = openpyxl.load_workbook(UNICO); ws = wb['Eventi unificati']; h = [c.value for c in ws[1]]; g = lambda r, k: r[h.index(k)]
points, addrs = {}, {}
for r in ws.iter_rows(min_row=2, values_only=True):
    f = g(r, 'fonte')
    if g(r, 'lat') and g(r, 'lon'):
        points[f'{round(float(g(r,"lat")),5)},{round(float(g(r,"lon")),5)}'] = None
    elif f.startswith('Comune') and g(r, 'indirizzo'):
        addrs[('street', g(r, 'indirizzo'), 'Roma')] = None
    elif f.startswith('Romatoday') and g(r, 'luogo'):
        st, town, venue = parse_dove(g(r, 'luogo'))
        if st and 'non disponibile' not in st.lower(): addrs[('street', st, town or 'Roma')] = None
        elif venue and venue.lower() not in ('roma', ''): addrs[('q', venue + ', Roma', '')] = None  # nome del luogo
    elif f == 'Facebook' and (g(r, 'indirizzo') or g(r, 'luogo')):
        addrs[('q', (g(r, 'indirizzo') or g(r, 'luogo')) + ', Roma', '')] = None
rt = wb['Romatoday → sorgente']; rh = [c.value for c in rt[1]]
for rr in rt.iter_rows(min_row=2, values_only=True):
    dv = rr[rh.index('dove')]
    if not dv: continue
    st, town, venue = parse_dove(dv)
    if st and 'non disponibile' not in st.lower(): addrs[('street', st, town or 'Roma')] = None
    elif venue and venue.lower() not in ('roma', ''): addrs[('q', venue + ', Roma', '')] = None
print('punti', len(points), 'indirizzi', len(addrs), flush=True)
out = {'points': {}, 'addrs': {}}
for i, k in enumerate(points):
    lat, lon = k.split(','); d = reverse(lat, lon); out['points'][k] = d.get('address') if isinstance(d, dict) else None
    if i % 25 == 0: print('punto', i, k, (d.get('address') or {}).get('suburb') if isinstance(d, dict) else d, flush=True); save()
for i, (kind, a, town) in enumerate(addrs):
    if kind == 'street':
        d = search(street=a, city=town)
        if not d: d = search(street=re.sub(r',\s*\S+$', '', a), city=town)          # senza civico
        if not d: d = search(q=f'{a}, {town}')                                        # ricerca libera
        if not d and town == 'Roma': d = search(q=f'{re.sub(r",\s*\S+$", "", a)}, Roma')
    else:
        d = search(q=a)
    key = f'{kind}|{a}|{town}'
    out['addrs'][key] = ({'lat': d[0]['lat'], 'lon': d[0]['lon'], 'type': d[0].get('type'), 'display': d[0].get('display_name'), 'address': d[0].get('address')} if isinstance(d, list) and d else None)
    if i % 25 == 0: print('indirizzo', i, key, (out['addrs'][key] or {}).get('display', 'NON TROVATO')[:60] if out['addrs'][key] else 'NON TROVATO', flush=True); save()
save(); json.dump(out, open(f'{S}/geo/geo.json', 'w'), ensure_ascii=False, indent=1)
print('DONE punti', sum(1 for v in out['points'].values() if v), '/', len(points), 'indirizzi', sum(1 for v in out['addrs'].values() if v), '/', len(addrs))

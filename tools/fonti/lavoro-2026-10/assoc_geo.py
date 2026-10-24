import json,sys,re,time,os,urllib.request,urllib.parse
S=sys.argv[1]; pages=json.load(open(f'{S}/assoc/pages_enriched.json'))
CACHE=f'{S}/geo/cache.json'; cache=json.load(open(CACHE)); UA='QuartieriNews-eventi/1.0 (contatto: redazione)'
MUN=json.load(open(f'{S}/geo/municipi.json'))['features']; SUD=json.load(open(f'{S}/geo/suddivisioni.json'))['features']
def _pip(x,y,poly):
    inside=False; n=len(poly)
    for i in range(n):
        x1,y1=poly[i][:2]; x2,y2=poly[(i+1)%n][:2]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1+1e-300)+x1: inside=not inside
    return inside
def inside(lat,lon,g):
    polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    return any(_pip(float(lon),float(lat),p[0]) and not any(_pip(float(lon),float(lat),h) for h in p[1:]) for p in polys if p and p[0])
def call(url):
    if url in cache: return cache[url]
    for t in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=30) as r: d=json.loads(r.read().decode())
            cache[url]=d; time.sleep(1.1); return d
        except Exception: time.sleep(3)
    return None
out={}; n=0
for p in pages:
    d=p.get('dati') or {}; a=d.get('address') or ''
    if not a or not re.search(r'\d',a) and ',' not in a: continue
    if re.fullmatch(r'\s*Rome, Italy(, \d{5})?\s*',a): continue
    q=a.replace(', Italy','').replace('Rome','Roma')
    m=re.search(r'maps\.google\.com/maps\?q=([\d.]+)%2C([\d.]+)',' '.join(d.get('websites') or []))
    if m: lat,lon=float(m.group(1)),float(m.group(2)); src='coordinate Facebook'
    else:
        r=call('https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','limit':1,'countrycodes':'it','accept-language':'it'}))
        if not r: continue
        lat,lon=float(r[0]['lat']),float(r[0]['lon']); src='geocodifica OSM dell\'indirizzo'
    mun=next((f['properties'].get('numero_rom') for f in MUN if inside(lat,lon,f['geometry'])),None)
    sd=next((f['properties'] for f in SUD if inside(lat,lon,f['geometry'])),None)
    out[p['url']]={'lat':lat,'lon':lon,'fonte':src,'municipio':mun,'suddivisione':f"{sd['TIPOLOGIA']} {sd['DESCRIZIONE']}" if sd else None,'sudd_nome':sd['DESCRIZIONE'] if sd else None}
    n+=1
    if n%50==0: print(n,flush=True); json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{S}/assoc/geo.json','w'),ensure_ascii=False,indent=1)
import collections; print('geocodificate',len(out),'in Roma',sum(1 for v in out.values() if v['municipio']),collections.Counter(v['municipio'] for v in out.values()).most_common(16))

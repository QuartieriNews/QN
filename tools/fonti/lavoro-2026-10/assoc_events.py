# Aggrega gli eventi futuri letti da unseenuser/fb-events (assoc/events_data/*.json) per pagina -> assoc/events.json
import json,sys,re,glob,collections
S=sys.argv[1]
MUN=json.load(open(f'{S}/geo/municipi.json'))['features']; SUD=json.load(open(f'{S}/geo/suddivisioni.json'))['features']
def _pip(x,y,poly):
    ins=False; n=len(poly)
    for i in range(n):
        x1,y1=poly[i][:2]; x2,y2=poly[(i+1)%n][:2]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1+1e-12)+x1: ins=not ins
    return ins
def inside(lat,lon,g):
    polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    return any(_pip(lon,lat,p[0]) and not any(_pip(lon,lat,h) for h in p[1:]) for p in polys)
def slug(u): return re.sub(r'^https?://(www\.|m\.)?facebook\.com/','',str(u or '')).strip('/').lower().split('?')[0]
def f(v):
    if v in (None,'None',''): return None
    return v
pages=json.load(open(f'{S}/assoc/pages.json')); byslug={slug(p['url']):p['url'] for p in pages}
for p in pages:
    d=p.get('dati') or {}
    if d.get('pageId'): byslug[str(d['pageId'])]=p['url']
ev=collections.defaultdict(list); seen=set(); n=0
for fn in sorted(glob.glob(f'{S}/assoc/events_data/*.json')):
    for it in json.load(open(fn)):
        q=(it.get('_metadata') or {}).get('query'); u=byslug.get(slug(q))
        if not u or it.get('id') in seen: continue
        seen.add(it['id']); n+=1
        lat,lon=f(it.get('latitude')),f(it.get('longitude')); mun=sd=None
        if lat and lon:
            lat,lon=float(lat),float(lon)
            mun=next((x['properties'].get('numero_rom') for x in MUN if inside(lat,lon,x['geometry'])),None)
            s=next((x['properties'] for x in SUD if inside(lat,lon,x['geometry'])),None); sd=s['DESCRIZIONE'] if s else None
        ev[u].append({'id':it['id'],'url':it.get('url'),'nome':it.get('name'),'inizio':f(it.get('start_utc')),'luogo':f(it.get('location_name')),'indirizzo':f(it.get('address')),'citta':f(it.get('city')),'online':str(it.get('is_online'))=='True','lat':lat,'lon':lon,'municipio':mun,'suddivisione':sd,'host':', '.join(h.get('name','') for h in (it.get('hosts') or []) if isinstance(h,dict)) or f(it.get('host_context_text')),'biglietti':f(it.get('ticket_url')),'interessati':f(it.get('interested_count')),'partecipano':f(it.get('going_count'))})
out={}
for u,L in ev.items():
    L.sort(key=lambda e:e['inizio'] or '')
    roma=[e for e in L if e['municipio']]
    out[u]={'eventi_futuri':len(L),'in_roma':len(roma),'online':sum(1 for e in L if e['online']),'prossimo':L[0]['inizio'],'ultimo':L[-1]['inizio'],'municipi':sorted({e['municipio'] for e in roma}),'municipio_prevalente':collections.Counter(e['municipio'] for e in roma).most_common(1)[0][0] if roma else None,'suddivisione_prevalente':collections.Counter(e['suddivisione'] for e in roma if e['suddivisione']).most_common(1)[0][0] if any(e['suddivisione'] for e in roma) else None,'lat':roma[0]['lat'] if roma else None,'lon':roma[0]['lon'] if roma else None,'eventi':L}
json.dump(out,open(f'{S}/assoc/events.json','w'),ensure_ascii=False,indent=1)
print('eventi',n,'pagine con eventi futuri',len(out),'eventi in Roma',sum(v['in_roma'] for v in out.values()))

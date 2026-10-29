# Istituti comprensivi (anagrafe MIUR) e mercati rionali (dati aperti Roma Capitale): geocodifica -> Municipio, suddivisione, zona QN
import json,csv,re,sys,time,urllib.request,urllib.parse,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
CACHE=f'{S}/geo/cache.json'; cache=json.load(open(CACHE)); UA='QuartieriNews-eventi/1.0 (contatto: redazione)'
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
def geocode(q):
    if q in cache: return cache[q]
    url='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','limit':1,'countrycodes':'it','accept-language':'it'})
    d=None
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=30) as r: d=json.loads(r.read().decode()); break
        except Exception: time.sleep(3)
    cache[q]=d; time.sleep(1.1); return d
def place(lat,lon):
    mun=next((f['properties'].get('numero_rom') for f in MUN if inside(lat,lon,f['geometry'])),None)
    sd=next((f['properties'] for f in SUD if inside(lat,lon,f['geometry'])),None)
    return mun,(sd['DESCRIZIONE'] if sd else None),(f"{sd['TIPOLOGIA']} {sd['DESCRIZIONE']}" if sd else None)
def main():
    out=[]
    rows=list(csv.DictReader(open(f'{S}/mirate/scuole.csv',encoding='utf-8',errors='replace')))
    ic=[r for r in rows if r['DESCRIZIONECOMUNE'].strip().upper()=='ROMA' and ('ISTITUTO COMPRENSIVO' in r['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].upper())]
    for r in ic:
        addr=f"{r['INDIRIZZOSCUOLA'].title()}, {r['CAPSCUOLA']} Roma"; d=geocode(addr)
        rec={'tipo':'istituto_comprensivo','nome':r['DENOMINAZIONESCUOLA'].title().replace('I.C.','IC'),'indirizzo':addr,'sito':re.sub(r'^https?//','https://',r['SITOWEBSCUOLA'].strip()) if r['SITOWEBSCUOLA'].strip() else None,'email':r['INDIRIZZOEMAILSCUOLA'].lower() or None,'origine':'anagrafe scuole statali MIUR 2026/27'}
        if d: lat,lon=float(d[0]['lat']),float(d[0]['lon']); rec.update(dict(zip(('municipio','sudd_nome','suddivisione'),place(lat,lon))),lat=lat,lon=lon)
        out.append(rec)
    m=list(csv.DictReader(open(f'{S}/mirate/mercati.csv',encoding='latin-1'),delimiter=';'))
    for r in m:
        addr=f"{r['INDIRIZZO'].strip()} {r['Civico'].strip()}, Roma".replace(' ,',','); d=geocode(addr)
        rec={'tipo':'mercato_rionale','nome':f"Mercato {r['Nome_Mercato'].strip()}",'indirizzo':addr,'sito':None,'email':None,'municipio_dichiarato':r['Municipio'].strip(),'origine':'dati aperti Roma Capitale, mercati rionali'}
        if d: lat,lon=float(d[0]['lat']),float(d[0]['lon']); rec.update(dict(zip(('municipio','sudd_nome','suddivisione'),place(lat,lon))),lat=lat,lon=lon)
        out.append(rec)
    json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{S}/mirate/liste.json','w'),ensure_ascii=False,indent=1)
    print('voci',len(out),'geocodificate',sum(1 for r in out if r.get('lat')),'in Roma',sum(1 for r in out if r.get('municipio')), collections.Counter(r['tipo'] for r in out))
if __name__=='__main__': main()

# Geografia degli enti: indirizzo dalla pagina Facebook (coordinate se presenti) o dal sito verificato -> Municipio, suddivisione, zona QN
import json,sys,re,glob,os
S=sys.argv[1]; W=f'{S}/runts/work'; sys.path.insert(0,f'{S}/scripts')
from mirate_liste import geocode,place,cache,CACHE
FB=json.load(open(f'{W}/fb.json'))['per_ente']; V=json.load(open(f'{W}/sites_all.json'))
def key(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
P={}
for f in glob.glob(f'{W}/fb_pages/*.json'):
    for it in json.load(open(f)):
        for k in ('inputUrl','url','facebookUrl','pageUrl'):
            if it.get(k): P.setdefault(key(it[k]),it)
        if it.get('pageId'): P.setdefault(str(it['pageId']),it)
out=json.load(open(f'{W}/geo.json')) if os.path.exists(f'{W}/geo.json') else {}
n=0
E=json.load(open(f'{W}/enti.json'))
for e in E:
    cf=e['cf']
    if cf in out: continue
    p=P.get(key((FB.get(cf) or {}).get('facebook'))) or {}
    a=p.get('address') or ''; src=None; lat=lon=None
    m=re.search(r'maps\.google\.com/maps\?q=([\d.]+)%2C([\d.]+)',' '.join(p.get('websites') or []))
    if m: lat,lon=float(m.group(1)),float(m.group(2)); src='coordinate della pagina Facebook'
    elif a and re.search(r'\d',a) and not re.fullmatch(r'\s*Rome, Italy(, \d{5})?\s*',a):
        g=geocode(a.replace(', Italy','').replace('Rome','Roma')); 
        if g: lat,lon=float(g[0]['lat']),float(g[0]['lon']); src='indirizzo della pagina Facebook (OSM)'
    if lat is None and (V.get(cf) or {}).get('indirizzo_dal_sito'):
        a=V[cf]['indirizzo_dal_sito']; g=geocode(a)
        if g: lat,lon=float(g[0]['lat']),float(g[0]['lon']); src='indirizzo dal sito (OSM)'
    if lat is None: continue
    mun,sd,sdf=place(lat,lon); out[cf]={'lat':lat,'lon':lon,'fonte':src,'indirizzo':a or None,'municipio':mun,'sudd_nome':sd,'suddivisione':sdf}
    n+=1
    if n%100==0: print(n,flush=True); json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{W}/geo.json','w'),ensure_ascii=False)
json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{W}/geo.json','w'),ensure_ascii=False,indent=1)
print('geocodificati',len(out),'in Roma',sum(1 for v in out.values() if v['municipio']))

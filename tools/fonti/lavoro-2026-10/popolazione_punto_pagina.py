# Punto (lat, lon) -> pagina QN: zona urbanistica ufficiale (155) e toponimo del gazetteer più vicino fra quelli di quella zona;
# zona urbanistica senza toponimi: toponimo più vicino nello stesso Municipio. Stessa geografia degli abitanti (assegna2.py).
import json,math,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); PAGES={z['publication_zone_id'] for z in gz['publication_zones'] if z['is_page']}
zu_of={n['neighbourhood_id']:n['zu_code'].upper() for n in gz['neighbourhoods'] if n.get('zu_code')}
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def rings(g): return g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
def bbox(g):
    xs=[p[0] for poly in rings(g) for r in poly for p in r]; ys=[p[1] for poly in rings(g) for r in poly for p in r]; return min(xs),min(ys),max(xs),max(ys)
def pip(x,y,r):
    c=False; j=len(r)-1
    for i in range(len(r)):
        xi,yi=r[i][:2]; xj,yj=r[j][:2]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi+1e-15)+xi: c=not c
        j=i
    return c
def inside(x,y,g): return any(pip(x,y,poly[0]) and not any(pip(x,y,h) for h in poly[1:]) for poly in rings(g))
ZU=[(f['properties']['code_zu'].upper(),f['properties']['denominazione'],ROM[int(f['properties']['municipi'])-1],bbox(f['geometry']),f['geometry']) for f in json.load(open(f'{S}/popolazione/zu.json'))['features']]
def find_zu(x,y): return next(((c,n,m) for c,n,m,b,g in ZU if b[0]<=x<=b[2] and b[1]<=y<=b[3] and inside(x,y,g)),None)
PT=[p for p in json.load(open(f'{S}/geo/gazetteer_punti.json')) if p.get('lat') and p.get('zona') in PAGES]
CAND=collections.defaultdict(list)
for p in PT:
    z=find_zu(p['lon'],p['lat'])
    if z: CAND[z[0]].append(p)
    if zu_of.get(p['id']) and (not z or zu_of[p['id']]!=z[0]): CAND[zu_of[p['id']]].append(p)
def d2(p,x,y): return (p['lat']-y)**2+((p['lon']-x)*math.cos(math.radians(y)))**2
def pagina(lat,lon):
    """-> (pagina QN, Municipio) o (None, None) fuori dal Comune"""
    try: y,x=float(lat),float(lon)
    except (TypeError,ValueError): return None,None
    z=find_zu(x,y)
    if not z: return None,None
    c=CAND.get(z[0]) or [p for p in PT if p.get('mun_poligono')==z[2]] or PT
    return min(c,key=lambda p:d2(p,x,y))['zona'],z[2]

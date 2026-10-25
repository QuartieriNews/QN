# Abitanti per pagina QN, metodo 2: griglia statistica di Roma Capitale (celle di 1 km, «abitanti»),
# ogni cella in 5x5 punti; ogni punto -> zona urbanistica ufficiale (155) -> toponimo del gazetteer più vicino
# fra quelli che stanno in quella zona urbanistica (o che il gazetteer collega al suo codice ZU);
# zona urbanistica senza toponimi: toponimo più vicino nello stesso Municipio.
import json,math,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); pages={z['publication_zone_id'] for z in gz['publication_zones'] if z['is_page']}
zu_of={n['neighbourhood_id']:n['zu_code'].upper() for n in gz['neighbourhoods'] if n.get('zu_code')}
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
ZU=[(f['properties']['code_zu'].upper(),f['properties']['denominazione'],f['properties']['municipi'],bbox(f['geometry']),f['geometry']) for f in json.load(open(f'{S}/popolazione/zu.json'))['features']]
def find_zu(x,y): return next(((c,n,m) for c,n,m,b,g in ZU if b[0]<=x<=b[2] and b[1]<=y<=b[3] and inside(x,y,g)),None)
PT=[p for p in json.load(open(f'{S}/geo/gazetteer_punti.json')) if p.get('lat') and p.get('zona') in pages]
cand=collections.defaultdict(list)
for p in PT:
    z=find_zu(p['lon'],p['lat'])
    if z: cand[z[0]].append(p)
    if zu_of.get(p['id']) and (not z or zu_of[p['id']]!=z[0]): cand[zu_of[p['id']]].append(p)
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def d2(p,x,y): return (p['lat']-y)**2+((p['lon']-x)*math.cos(math.radians(y)))**2
pop=collections.Counter(); zupop=collections.Counter(); zuname={}; metodo=collections.Counter(); fuori=0
for f in json.load(open(f'{S}/popolazione/griglia.json'))['features']:
    ab=f['properties']['abitanti'] or 0
    if not ab: continue
    x0,y0,x1,y1=bbox(f['geometry']); pts=[]
    for i in range(5):
        for j in range(5):
            x=x0+(i+.5)*(x1-x0)/5; y=y0+(j+.5)*(y1-y0)/5; z=find_zu(x,y)
            if not z: continue
            c=cand.get(z[0])
            if c: metodo['toponimo nella zona urbanistica']+=1
            else: c=[p for p in PT if p.get('mun_poligono')==ROM[int(z[2])-1]] or PT; metodo['toponimo nel Municipio']+=1
            pts.append((min(c,key=lambda p:d2(p,x,y))['zona'],z[0])); zuname[z[0]]=z[1]
    if not pts: fuori+=ab; continue
    for zona,zu in pts: pop[zona]+=ab/len(pts); zupop[(zu,zona)]+=ab/len(pts)
print('abitanti assegnati',round(sum(pop.values())),'fuori',fuori,dict(metodo),'ZU senza toponimi',sorted(z for z,_,_,_,_ in ZU if not cand.get(z)))
json.dump({z:round(v) for z,v in pop.items()},open(f'{S}/popolazione/abitanti_pagina.json','w'),indent=0)
json.dump([[zu,zuname.get(zu),zona,round(v)] for (zu,zona),v in sorted(zupop.items())],open(f'{S}/popolazione/zu_pagina.json','w'))

import json,sys,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,f'{S}/popolazione'); sys.path.insert(0,f'{S}/supplementare')
from punto_pagina import pagina
from noti import nota
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
def tipo(t):
    a=t.get('amenity'); 
    if a=='place_of_worship':
        return 'parrocchia o chiesa cattolica' if t.get('denomination') in ('catholic','roman_catholic') or (t.get('religion')=='christian' and not t.get('denomination')) else 'comunità religiosa'
    if a in ('community_centre','social_centre','youth_centre') or t.get('social_facility'): return 'centro sociale, anziani o di quartiere'
    if a in ('arts_centre','theatre','events_venue','library'): return 'luogo culturale (teatro, biblioteca, centro arti)'
    if t.get('club')=='scout': return 'scout'
    if t.get('club')=='sport' or t.get('leisure')=='sports_centre': return 'sport'
    return 'associazione'
out=[]
for e in json.load(open(f'{S}/supplementare/osm.json'))['elements']:
    t=e.get('tags',{}); n=t.get('name')
    if not n: continue
    la=e.get('lat') or e.get('center',{}).get('lat'); lo=e.get('lon') or e.get('center',{}).get('lon')
    z,m=pagina(la,lo)
    if z not in T: continue
    ty=tipo(t)
    if ty=='parrocchia o chiesa cattolica' and t.get('building')=='chapel': continue
    sito=t.get('website') or t.get('contact:website') or t.get('url'); fb=t.get('contact:facebook') or t.get('facebook')
    ind=' '.join(x for x in (t.get('addr:street'),t.get('addr:housenumber')) if x) or None
    out.append({'nome':n,'tipo':ty,'pagina':z,'municipio':m,'indirizzo':ind,'sito':sito,'facebook':fb,'telefono':t.get('phone') or t.get('contact:phone'),'email':t.get('email') or t.get('contact:email'),
                'lat':la,'lon':lo,'origine':'OpenStreetMap','osm':f"https://www.openstreetmap.org/{e['type']}/{e['id']}",'gia_nota':nota(n,sito,fb,la,lo)})
json.dump(out,open(f'{S}/supplementare/osm_target.json','w'),ensure_ascii=False,indent=0)
print(len(out),'nuove',sum(1 for o in out if not o['gia_nota'])); print(collections.Counter((o['tipo'],bool(o['gia_nota'])) for o in out).most_common())

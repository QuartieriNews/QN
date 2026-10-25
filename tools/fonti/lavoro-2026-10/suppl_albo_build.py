# Albo della cittadinanza attiva di Roma Capitale -> organizzazioni con sede nelle pagine deboli
import json,sys,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,f'{S}/popolazione'); sys.path.insert(0,f'{S}/supplementare'); sys.path.insert(0,f'{S}/scripts')
from punto_pagina import pagina
from noti import nota
from mirate_liste import geocode,cache,CACHE
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
out=[]; st=collections.Counter()
for o in json.load(open(f'{S}/supplementare/albo/albo_cittadinanza.json')):
    la,lo=o['lat'],o['lon']
    if not la or abs(la-42.1564178)<1e-4:
        g=geocode(f"{o['indirizzo']}, Roma") if o['indirizzo'] else None
        la,lo=(float(g[0]['lat']),float(g[0]['lon'])) if g else (None,None); st['geocodificate']+=1
    z,m=pagina(la,lo)
    if z not in T: st['fuori dalle pagine deboli o senza sede']+=1; continue
    out.append({'nome':o['nome'],'tipo':'comitato di quartiere o civico' if 'omitat' in o['nome'] else 'associazione','pagina':z,'municipio':m,'indirizzo':o['indirizzo'],'lat':la,'lon':lo,
                'origine':'Albo della cittadinanza attiva (Roma Capitale)','scheda':f"https://www.comune.roma.it/web/it/partecipa-albo-cittadinanza-attiva.page?contentId={o['id']}",'gia_nota':nota(o['nome'],lat=la,lon=lo)})
json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
json.dump(out,open(f'{S}/supplementare/albo_target.json','w'),ensure_ascii=False,indent=0)
print(dict(st),len(out),'nuove',sum(1 for o in out if not o['gia_nota'])); print([(o['nome'],o['pagina']) for o in out])

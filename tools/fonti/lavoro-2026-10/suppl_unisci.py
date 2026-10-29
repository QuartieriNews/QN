# Lista supplementare: OpenStreetMap + Google Maps + albo della cittadinanza attiva + ricerca Google + annuario diocesano + albi municipali,
# doppioni uniti (stesso sito, stessa pagina Facebook, o nome simile a meno di 250 m), segnata se già nota.
import json,re,sys,math,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/supplementare'); sys.path.insert(0,f'{S}/popolazione'); sys.path.insert(0,f'{S}/scripts')
from noti import nota,toks,dom,fbk
from punto_pagina import pagina
from mirate_liste import geocode,cache,CACHE
T={r['id']:r for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
R=[]
for f in ('osm_target','maps_target','albo_target'): R+=json.load(open(f'{S}/supplementare/{f}.json'))
for g in json.load(open(f'{S}/supplementare/google_cand.json')):
    R.append({'nome':g['nome'],'tipo':'comitato di quartiere o civico' if g['ricerca']=='comitato' and re.search(r'(?i)comitat|cdq',g['nome']) else 'associazione','pagina':g['pagina'],'municipio':T[g['pagina']]['municipio'],
              'sito':g['url'] if g['canale']=='sito' else None,'facebook':g['url'] if g['canale']=='pagina Facebook' else None,'instagram':g['url'] if g['canale']=='Instagram' else None,
              'gruppo_facebook':g['url'] if g['canale']=='gruppo Facebook' else None,'origine':'ricerca Google','zona_da':g['zona_da'],'descrizione':g['descrizione'],'gia_nota':g['gia_nota']})
for p in json.load(open(f'{S}/supplementare/parrocchie.json')):
    if not p.get('indirizzo'): continue
    gg=geocode(p['indirizzo'].replace('–',',')); la,lo=(float(gg[0]['lat']),float(gg[0]['lon'])) if gg else (None,None); z,m=pagina(la,lo)
    if z in T: R.append({'nome':'Parrocchia '+p['nome'],'tipo':'parrocchia o chiesa cattolica','pagina':z,'municipio':m,'indirizzo':p['indirizzo'],'sito':p['sito'],'telefono':p['telefono'],'email':p['email'],'lat':la,'lon':lo,'origine':'Annuario Diocesi di Roma','gia_nota':nota(p['nome'],p['sito'],lat=la,lon=lo)})
json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
def dm(a,b):
    if not (a.get('lat') and b.get('lat')): return 9e9
    return math.hypot((a['lat']-b['lat'])*111000,(a['lon']-b['lon'])*111000*math.cos(math.radians(a['lat'])))
G=[]   # gruppi uniti
for r in R:
    d,k,t=dom(r.get('sito')),fbk(r.get('facebook')),toks(r['nome'])
    hit=None
    for g in G:
        if (d and d in g['_dom']) or (k and k in g['_fb']): hit=g; break
        if t and any((len(t&tt)/len(t|tt)>=0.6 and (dm(r,x)<250 or (not r.get('lat') or not x.get('lat')) and r['pagina']==x['pagina'])) for tt,x in g['_t']): hit=g; break
    if not hit:
        hit={'_dom':set(),'_fb':set(),'_t':[],'righe':[]}; G.append(hit)
    hit['righe'].append(r); hit['_t'].append((t,r))
    if d: hit['_dom'].add(d)
    if k: hit['_fb'].add(k)
PRI=['Google Maps','Albo della cittadinanza attiva (Roma Capitale)','Annuario Diocesi di Roma','OpenStreetMap','ricerca Google']
out=[]
for g in G:
    rr=sorted(g['righe'],key=lambda r:PRI.index(r['origine']))
    def first(k): return next((r.get(k) for r in rr if r.get(k)),None)
    o={'nome':first('nome'),'tipo':first('tipo'),'pagina':rr[0]['pagina'],'municipio':first('municipio'),'indirizzo':first('indirizzo'),'sito':first('sito'),'facebook':first('facebook'),'instagram':first('instagram'),
       'gruppo_facebook':first('gruppo_facebook'),'telefono':first('telefono'),'email':first('email'),'lat':first('lat'),'lon':first('lon'),'categoria_google':first('categoria_google'),
       'origini':' + '.join(sorted({r['origine'] for r in rr},key=PRI.index)),'n_origini':len({r['origine'] for r in rr}),'gia_nota':first('gia_nota'),
       'collegamento':first('maps') or first('osm') or first('scheda'),'descrizione':first('descrizione')}
    out.append(o)
json.dump(out,open(f'{S}/supplementare/lista.json','w'),ensure_ascii=False,indent=0)
print('righe',len(R),'soggetti',len(out),'nuovi',sum(1 for o in out if not o['gia_nota']))
print(collections.Counter(o['tipo'] for o in out if not o['gia_nota']).most_common())
print('con sito',sum(1 for o in out if not o['gia_nota'] and o['sito']),'con facebook',sum(1 for o in out if not o['gia_nota'] and o['facebook']),'in piu origini',sum(1 for o in out if o['n_origini']>1))

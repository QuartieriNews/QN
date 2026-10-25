# Tutti gli eventi futuri noti al 24 ottobre 2026, assegnati alle pagine QN -> eventi.json per la pagina HTML
import json,re,sys,glob,unicodedata,collections,openpyxl
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/scripts')
from mirate_liste import place
TODAY='2026-10-25'
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); zones={z['publication_zone_id']:z for z in gz['publication_zones']}
pages={z:p for z,p in zones.items() if p.get('is_page')}
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
names={}
for n in gz['neighbourhoods']:
    for a in [n['name_display']]+re.split(r'[;|/]',n.get('aliases') or ''):
        if norm(a): names.setdefault(norm(a),n)
for z in gz['publication_zones']: names.setdefault(norm(z['name_display']),{'publication_zone_id':z['publication_zone_id'],'municipality_code':z['primary_municipality'],'publishable':z['is_page']})
def match(sd,mun):
    if not sd: return None
    c=norm(re.sub(r'^(quartiere|rione|zona|suburbio|borgata) ','',sd,flags=re.I)); w=c.split()
    for f in [c]+[' '.join(w[:k]) for k in range(len(w)-1,0,-1)]:
        n=names.get(f)
        if n and n.get('publishable',True) and (not mun or not n.get('municipality_code') or n['municipality_code']==mun): return n['publication_zone_id']
    return None
def zone_ll(lat,lon):
    try: lat,lon=float(lat),float(lon)
    except (TypeError,ValueError): return None,None
    mun,sd,_=place(lat,lon); return match(sd,mun),mun
NAMES5={k:v for k,v in names.items() if len(k)>=6 and v.get('publishable',True) and k not in ('centro','roma','italia','parco','villa')}
def zone_from_text(t):
    tt=' '+norm(t)+' '; best=None
    for k,n in NAMES5.items():
        if f' {k} ' in tt and (best is None or len(k)>len(best[0])): best=(k,n)
    if not best: return None,None
    z=best[1]['publication_zone_id']; return (z if z in pages else None), best[1].get('municipality_code')
def s(v): v=None if v in (None,'None','') else str(v).strip(); return v
ev=[]; seen=set(); stat=collections.Counter()
def add(src,t,d1,d2,ora,luogo,ind,org,url,z,mun,fonte_url=None,gratis=None,o=None):
    t=s(t); d1=s(d1); d2=s(d2) or d1
    if not t or not d1: stat['senza titolo o data']+=1; return
    d1=d1[:16].replace('T',' '); d2=(d2 or d1)[:16].replace('T',' ')
    if max(d1[:10],d2[:10])<TODAY: stat['passati']+=1; return
    k=(norm(t)[:45],d1[:10])
    if k in seen: stat['doppioni']+=1; return
    seen.add(k)
    if z not in pages: z=None
    if not ora and len(d1)>10 and d1[11:16]!='00:00': ora=d1[11:16]
    ev.append({'z':z,'m':mun or (pages[z]['primary_municipality'] if z else None),'t':t[:160],'d1':d1[:10],'d2':d2[:10],'ora':s(ora),'luogo':s(luogo),'ind':s(ind),'org':s(org),'url':s(fonte_url) or s(url),'src':src,'free':gratis,'o':o or src})
    stat[src]+=1
# 1. culture.roma.it per differenza (le più fresche)
for r in (json.loads(l) for l in open(f'{S}/culture_delta/delta.jsonl')):
    z,m=zone_ll(r.get('lat'),r.get('lon')); add('culture.roma.it',r['titolo'],r.get('inizio'),r.get('fine'),r.get('orario'),r.get('luogo'),r.get('indirizzo'),r.get('a_cura_di'),r['url'],z,m or r.get('municipio'),r.get('sito'),'gratuito' if r.get('gratuito') else None,o='culture.roma.it: lettura per differenza 20-24 ott')
# 2. foglio unificato (righe principali)
wb=openpyxl.load_workbook('/mnt/user-data/outputs/eventi_unico.xlsx',read_only=True); ws=wb['Eventi unificati']; rr=list(ws.iter_rows(values_only=True)); h=rr[0]
SRC={'Comune':'culture.roma.it','Facebook':'Facebook','Romatoday':'Roma Today','Fonte locale':'sito della fonte'}
for row in rr[1:]:
    r=dict(zip(h,row))
    if r.get('riga_principale_proposta') not in ('sì',None): continue
    src=next((v for k,v in SRC.items() if str(r['fonte']).startswith(k)),'altro')
    z=s(r.get('zona_qn')) or s(r.get('zona_qn_metodo2')); m=s(r.get('municipio_assegnato'))
    url=s(r.get('link_fonte_diretta')) or (None if src=='Roma Today' else s(r.get('url')))
    o={'culture.roma.it':'culture.roma.it: lettura completa 20 ott','Facebook':'Facebook: eventi raccolti a mano dall\'owner','Roma Today':'Roma Today: lettura una tantum','sito della fonte':'siti delle fonti: lettura diretta 13-31 ott'}.get(src,src)
    add(src,r['nome'],r['inizio'],r['fine'],None,r['luogo'],r['indirizzo'],r['organizzatore'],url,z,m,o=o)
# 3. schema.org dai siti delle fonti
sched={e['id']:e for e in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']}
for r in json.load(open(f'{S}/siti/eventi_siti_tutti.json')):
    if r['prova']!='jsonld': continue
    e=sched.get(r['fonte_id'],{}); add('sito della fonte',r['evento'],r['inizio'],r['fine'],None,r.get('luogo') or e.get('nome'),r.get('indirizzo') or e.get('indirizzo'),r['fonte'],r.get('url') or r['pagina'],e.get('zona'),e.get('municipio'),o='siti delle fonti: lettore automatico 24 ott')
# 4. eventi Facebook delle pagine (censimento associazioni)
for u,v in json.load(open(f'{S}/assoc/events.json')).items():
    for x in v['eventi']:
        add('Facebook',x['nome'],x['inizio'],None,None,x['luogo'],x['indirizzo'],x['host'],x['url'],match(x.get('suddivisione'),x.get('municipio')),x.get('municipio'),o='Facebook: pagine del censimento associazioni')
# 5. eventi Facebook degli enti RUNTS
def key(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
for f in sorted(glob.glob(f'{S}/runts/work/fb_events/*.json')):
    for x in json.load(open(f)):
        if key((x.get('_metadata') or {}).get('query'))=='feverup' or str(x.get('is_past'))=='True': continue
        if 'Rome' not in str(x.get('city') or '') and 'Roma' not in str(x.get('address') or ''): continue
        z,m=zone_ll(x.get('latitude'),x.get('longitude'))
        add('Facebook',x.get('name'),x.get('start_utc'),None,None,x.get('location_name'),x.get('address'),', '.join(x.get('host_names') or []) if isinstance(x.get('host_names'),list) else x.get('host_names'),x.get('url'),z,m,o='Facebook: pagine degli enti RUNTS')
# 6. scoperta per parole chiave
wb=openpyxl.load_workbook('/mnt/user-data/outputs/facebook_scoperta_organizzatori.xlsx',read_only=True); rr=list(wb['Eventi'].iter_rows(values_only=True)); h=rr[0]
for row in rr[1:]:
    r=dict(zip(h,row))
    if r.get('online') or not r.get('municipio'): continue
    add('Facebook',r['nome'],r['inizio'],None,None,r['luogo'],None,r['organizzatori'],r['url'],r.get('zona_qn'),r.get('municipio'),o='Facebook: ricerca per parole chiave')
# 7. fonti nuove dalla ricerca «evento / eventi / festa + quartiere» (24 ottobre): siti letti e pagine Facebook
import os
RQ=f'{S}/ricerca_quartieri'
OTHERC=re.compile(r'\b(Mestre|Venezia|Milano|Torino|Bologna|Napoli|Firenze|Genova|Trieste|Verona|Padova|Bari|Palermo|Catania|Frascati|Fiumicino|Ostia Antica|Tivoli|Latina|Viterbo|Rieti|Frosinone|Cervara di Roma)\b')
EVW=re.compile(r'\b(evento|eventi|festa|sagra|concerto|spettacolo|mostra|incontro|presentazione|laboratorio|visita|passeggiata|torneo|mercatino|cinema|proiezione|teatro|reading|conferenza|festival|rassegna|apertura|inaugurazione)\b',re.I)
if os.path.exists(f'{RQ}/fonti_lette.json'):
    FIL=json.load(open(f'{RQ}/filtro.json')) if os.path.exists(f'{RQ}/filtro.json') else {}
    for r in json.load(open(f'{RQ}/fonti_lette.json')):
        if r['fonte'] in FIL: continue
        z=match(r.get('sudd_nome'),r.get('municipio')) if r.get('sudd_nome') else None; m=r.get('municipio')
        # solo l'indirizzo della fonte assegna la pagina: il quartiere della ricerca che l'ha trovata non basta
        for x in r['eventi']:
            dv=x['prova']!='jsonld'
            zx,mx=(zone_from_text(x['evento']) if dv else (z,m))
            if OTHERC.search(x['evento']) or (dv and not EVW.search(x['evento'])): continue
            add('sito della fonte',x['evento'],x['inizio'],x.get('fine'),None,x.get('luogo') or (None if dv else r.get('nome')),x.get('indirizzo') or (None if dv else r.get('indirizzo')),r.get('nome'),x.get('url') or x['pagina'],zx,mx,o='ricerca evento+quartiere: siti nuovi'+(' (blocchi datati)' if dv else ''))
            if dv and ev and ev[-1]['t']==str(x['evento']).strip()[:160]: ev[-1]['dv']=True
for f in sorted(glob.glob(f'{RQ}/fb_events_*.json')):
    for x in json.load(open(f)):
        if str(x.get('is_past'))=='True' or ('Rome' not in str(x.get('city') or '') and 'Roma' not in str(x.get('address') or '')): continue
        z,m=zone_ll(x.get('latitude'),x.get('longitude'))
        add('Facebook',x.get('name'),x.get('start_utc'),None,None,x.get('location_name'),x.get('address'),', '.join(x.get('host_names') or []) if isinstance(x.get('host_names'),list) else x.get('host_names'),x.get('url'),z,m,o='ricerca evento+quartiere: pagine Facebook nuove')
# 8. eventi annunciati nei post Facebook (ultimi post di 3.977 pagine; estrazione dal testo, da verificare)
PE=f'{S}/post_eventi/eventi_post_futuri.json'
if os.path.exists(PE):
    for x in json.load(open(PE)):
        n0=len(ev)
        add('Facebook (post)',x.get('titolo') or (x.get('testo') or '')[:90],x['inizio'],x['fine'],x.get('ora'),x.get('luogo'),None,x.get('fonte'),x.get('url_post'),x.get('zona'),x.get('municipio'),o='post Facebook: '+str(x.get('lotto')))
        if len(ev)>n0:
            ev[-1]['dp']=True
            if x.get('ricorrente'): ev[-1]['ric']=x['ricorrente']
ev.sort(key=lambda e:(e['d1'],e['ora'] or '',e['t']))
P=[{'id':z,'nome':p['name_display'],'mun':p['primary_municipality']} for z,p in sorted(pages.items(),key=lambda kv:kv[1]['name_display'])]
json.dump({'oggi':TODAY,'pagine':P,'eventi':ev},open(f'{S}/pagina_eventi/eventi.json','w'),ensure_ascii=False,separators=(',',':'))
c=collections.Counter(e['z'] for e in ev)
print(dict(stat)); print('eventi',len(ev),'con pagina QN',sum(1 for e in ev if e['z']),'senza',sum(1 for e in ev if not e['z']),'pagine con almeno un evento',sum(1 for p in P if c.get(p['id'])),'a zero',sum(1 for p in P if not c.get(p['id'])),'>=10',sum(1 for p in P if c.get(p['id'],0)>=10))

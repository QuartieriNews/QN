# Tutti gli eventi futuri noti al 24 ottobre 2026, assegnati alle pagine QN -> eventi.json per la pagina HTML
import json,re,sys,glob,unicodedata,collections,openpyxl,os,ast,urllib.parse
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
GEO=os.environ.get('GEO','zu')   # zona urbanistica + toponimo più vicino, la geografia degli abitanti (pagina pubblicata dal 25 ottobre, decisione dell'owner); «sudd»: suddivisioni toponomastiche
if GEO=='zu':
    sys.path.insert(0,f'{S}/popolazione'); from punto_pagina import pagina as _pagina
def zone_ll(lat,lon):
    try: lat,lon=float(lat),float(lon)
    except (TypeError,ValueError): return None,None
    if GEO=='zu': return _pagina(lat,lon)
    mun,sd,_=place(lat,lon); return match(sd,mun),mun
NAMES5={k:v for k,v in names.items() if len(k)>=6 and v.get('publishable',True) and k not in ('centro','roma','italia','parco','villa')}
def zone_from_text(t):
    tt=' '+norm(t)+' '; best=None
    for k,n in NAMES5.items():
        if f' {k} ' in tt and (best is None or len(k)>len(best[0])): best=(k,n)
    if not best: return None,None
    z=best[1]['publication_zone_id']; return (z if z in pages else None), best[1].get('municipality_code')
def s(v): v=None if v in (None,'None','') else str(v).strip(); return v
CITYNEWS=re.compile(r'(^|\.)(romatoday\.it|citynews\.it|today\.it)$')   # Roma Today e Citynews: solo la lettura una tantum autorizzata (DEC-026)
PROVT=re.compile(r"(?<!Via )(?<!Viale )(?<!Piazza )(?<!Largo )(?<!Via di )\b(Albano Laziale|Albano|Marino|Frascati|Ciampino|Castel Gandolfo|Genzano|Ariccia|Rocca di Papa|Rocca Priora|Grottaferrata|Monte Porzio|Monte Compatri|Fiumicino|Guidonia|Tivoli|Monterotondo|Pomezia|Ardea|Anzio|Nettuno|Velletri|Ladispoli|Cerveteri|Bracciano|Mentana|Fonte Nuova|Zagarolo|Palestrina|Colleferro|Valmontone|Lariano|Nemi|Formello|Sacrofano|Campagnano|Anguillara|Trevignano|Santa Marinella|Civitavecchia|Subiaco)\b")
ev=[]; seen={}; stat=collections.Counter()
def add(src,t,d1,d2,ora,luogo,ind,org,url,z,mun,fonte_url=None,gratis=None,o=None):
    t=s(t); d1=s(d1); d2=s(d2) or d1
    if not t or not d1: stat['senza titolo o data']+=1; return
    d1=d1[:16].replace('T',' '); d2=(d2 or d1)[:16].replace('T',' ')
    if max(d1[:10],d2[:10])<TODAY: stat['passati']+=1; return
    if re.search(r'comune\.[a-z-]+\.rm\.it',str(url or '')+str(fonte_url or '')): stat['fuori Roma (sito di un altro comune)']+=1; return
    if src!='Roma Today' and any(CITYNEWS.search(urllib.parse.urlsplit(str(u or '')).netloc.lower()) for u in (url,fonte_url)): stat['Roma Today fuori dalla lettura autorizzata (DEC-026)']+=1; return
    lu=f"{luogo or ''} {ind or ''}"
    if PROVT.search(lu) and not re.search(r'\b(Roma|Rome)\b',lu): stat['fuori Roma (luogo in un comune della provincia)']+=1; return
    cap=re.findall(r'(?<![\d.])(\d{5})(?!\d)',f"{luogo or ''} {ind or ''}")
    if cap and not any('00100'<=c<='00199' for c in cap): stat['fuori Roma (CAP)']+=1; return   # widget di eventi altrui (AICP: eventi negli Stati Uniti), Fever all'estero
    k=(norm(t)[:45],d1[:10])
    if k in seen:   # doppione: completa i campi vuoti del gemello già tenuto (leva L06)
        stat['doppioni']+=1; g=ev[seen[k]]
        for f_,v_ in (('ind',s(ind)),('org',s(org)),('ora',s(ora)),('luogo',s(luogo))):
            if not g.get(f_) and v_: g[f_]=v_; stat['doppioni: campo completato']+=1
        if not g['z'] and z in pages: g['z']=z; g['m']=g['m'] or mun or pages[z]['primary_municipality']; stat['doppioni: pagina completata']+=1
        return
    seen[k]=len(ev)
    if z not in pages: z=None
    if not ora and len(d1)>10 and d1[11:16]!='00:00': ora=d1[11:16]
    ev.append({'z':z,'m':mun or (pages[z]['primary_municipality'] if z else None),'t':t[:160],'d1':d1[:10],'d2':d2[:10],'ora':s(ora),'luogo':s(luogo),'ind':s(ind),'org':s(org),'url':s(fonte_url) or s(url),'src':src,'free':gratis,'o':o or src})
    stat[src]+=1
# 1. culture.roma.it per differenza (le più fresche)
for r in (json.loads(l) for f in sorted(glob.glob(f'{S}/culture_delta/delta*.jsonl')) for l in open(f)):
    z,m=zone_ll(r.get('lat'),r.get('lon')); add('culture.roma.it',r['titolo'],r.get('inizio'),r.get('fine'),r.get('orario'),r.get('luogo'),r.get('indirizzo'),r.get('a_cura_di'),r['url'],z,m or r.get('municipio'),r.get('sito'),'gratuito' if r.get('gratuito') else None,o='culture.roma.it: lettura per differenza 20-24 ott')
# 2. foglio unificato (righe principali)
wb=openpyxl.load_workbook('/mnt/user-data/outputs/eventi_unico.xlsx',read_only=True); ws=wb['Eventi unificati']; rr=list(ws.iter_rows(values_only=True)); h=rr[0]
SRC={'Comune':'culture.roma.it','Facebook':'Facebook','Romatoday':'Roma Today','Fonte locale':'sito della fonte'}
for row in rr[1:]:
    r=dict(zip(h,row))
    if r.get('riga_principale_proposta') not in ('sì',None): continue
    src=next((v for k,v in SRC.items() if str(r['fonte']).startswith(k)),'altro')
    z=s(r.get('zona_qn')) or s(r.get('zona_qn_metodo2')); m=s(r.get('municipio_assegnato'))
    if GEO=='zu' and r.get('lat'): z,m=zone_ll(r['lat'],r['lon'])
    url=s(r.get('link_fonte_diretta')) or (None if src=='Roma Today' else s(r.get('url')))
    o={'culture.roma.it':'culture.roma.it: lettura completa 20 ott','Facebook':'Facebook: eventi raccolti a mano dall\'owner','Roma Today':'Roma Today: lettura una tantum','sito della fonte':'siti delle fonti: lettura diretta 13-31 ott'}.get(src,src)
    add(src,r['nome'],r['inizio'],r['fine'],None,r['luogo'],r['indirizzo'],r['organizzatore'],url,z,m,o=o)
# 3. schema.org dai siti delle fonti
sched={e['id']:e for e in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']}
for r in json.load(open(f'{S}/siti/eventi_siti_tutti.json')):
    if r['prova']!='jsonld' or 'AICP' in str(r.get('fonte')): continue   # AICP: il sito riporta un widget di eventi di tutto il mondo
    e=sched.get(r['fonte_id'],{})
    if GEO=='zu' and e.get('lat'): e={**e,**dict(zip(('zona','municipio'),zone_ll(e['lat'],e['lon'])))}
    add('sito della fonte',r['evento'],r['inizio'],r['fine'],None,r.get('luogo') or e.get('nome'),r.get('indirizzo') or e.get('indirizzo'),r['fonte'],r.get('url') or r['pagina'],e.get('zona'),e.get('municipio'),o='siti delle fonti: lettore automatico 24 ott')
# 4. eventi Facebook delle pagine (censimento associazioni)
for u,v in json.load(open(f'{S}/assoc/events.json')).items():
    for x in v['eventi']:
        add('Facebook',x['nome'],x['inizio'],None,None,x['luogo'],x['indirizzo'],x['host'],x['url'],*(zone_ll(x['lat'],x['lon']) if GEO=='zu' and x.get('lat') else (match(x.get('suddivisione'),x.get('municipio')),x.get('municipio'))),o='Facebook: pagine del censimento associazioni')
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
        if GEO=='zu' and r.get('lat'): z,m=zone_ll(r['lat'],r['lon'])
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
# 8. eventi annunciati nei post Facebook (ultimi post di 4.204 pagine; estrazione dal testo, da verificare)
PE=f'{S}/post_eventi/eventi_post_futuri.json'
FBLL={}   # pagina Facebook -> coordinate della sede (wiki fonti-eventi), per gli annunci assegnati dalla sede della fonte
for f in sched.values():
    for u in (f.get('canali') or {}).get('facebook') or []:
        if f.get('lat') and key(u): FBLL.setdefault(key(u),(f['lat'],f['lon']))
if os.path.exists(PE):
    for x in json.load(open(PE)):
        if GEO=='zu' and x.get('zona_metodo') in ('sede della fonte',None) and FBLL.get(x.get('pagina')):
            z,m=zone_ll(*FBLL[x['pagina']])
            if z: x={**x,'zona':z,'municipio':m}
        n0=len(ev)
        add('Facebook (post)',x.get('titolo') or (x.get('testo') or '')[:90],x['inizio'],x['fine'],x.get('ora'),x.get('luogo'),None,x.get('fonte'),x.get('url_post'),x.get('zona'),x.get('municipio'),o='post Facebook: '+str(x.get('lotto')))
        if len(ev)>n0:
            ev[-1]['dp']=True
            if x.get('ricorrente'): ev[-1]['ric']=x['ricorrente']
# 9. lista supplementare per le pagine deboli (25 ottobre): post Facebook e siti dei soggetti nuovi (da verificare)
PS=f'{S}/supplementare/eventi_suppl.json'
if os.path.exists(PS):
    for x in json.load(open(PS)):
        n0=len(ev); post=x['canale']=='Facebook (post)'
        add('Facebook (post)' if post else 'sito della fonte',x.get('titolo') or (x.get('testo') or '')[:90],x['inizio'],x['fine'],x.get('ora'),x.get('luogo'),None,x.get('fonte'),x.get('url'),x.get('zona'),x.get('municipio'),o='lista supplementare: '+x['canale'])
        if len(ev)>n0:
            if post:
                ev[-1]['dp']=True
                if x.get('ricorrente'): ev[-1]['ric']=x['ricorrente']
            elif x.get('prova')!='jsonld': ev[-1]['dv']=True
# 10. Biblioteche di Roma (agenda dell'OPAC, 25 ottobre): un evento schema.org per appuntamento, con la sede
PB=f'{S}/promotori/biblioteche_eventi.json'
if os.path.exists(PB):
    BIB={}
    for b in json.load(open(f'{S}/mirate/bib.json')):
        c=str(b.get('sito') or '').rstrip('/').split('/')[-1]
        if b.get('lat'): BIB[c]=(b['lat'],b['lon'],b.get('indirizzo'))
    for x in json.load(open(PB)):
        if x.get('sotto_eventi'): stat['biblioteche: news ombrello (gli appuntamenti sono a parte)']+=1; continue
        codes=[c for c in x.get('codici_sede') or [] if c in BIB]
        la,lo,ind=BIB[codes[0]] if codes else (None,None,None)
        z,m=zone_ll(la,lo) if codes else (None,None)
        om=re.search(r'ore\s+(\d{1,2})[:.](\d{2})',x.get('quando') or '')
        add('sito della fonte',x['titolo'],x['inizio'],x['fine'],f"{int(om.group(1)):02d}:{om.group(2)}" if om else None,(x.get('sedi') or [None])[0],ind,(x.get('sedi') or ['Biblioteche di Roma'])[0],x['url'],z,m,o='Biblioteche di Roma: agenda (OPAC)')
# 11. eventi futuri delle pagine Facebook mai lette (25 ottobre): lista supplementare e promotori
for f in sorted(glob.glob(f'{S}/promotori/fbevents_ev_*.json')):
    for x in json.load(open(f)):
        if str(x.get('is_past'))=='True' or ('Rome' not in str(x.get('city') or '') and 'Roma' not in str(x.get('address') or '')): continue
        z,m=zone_ll(x.get('latitude'),x.get('longitude'))
        hn=x.get('host_names'); hn=', '.join(hn) if isinstance(hn,list) else (', '.join(ast.literal_eval(hn)) if isinstance(hn,str) and hn.startswith('[') else hn)
        add('Facebook',x.get('name'),x.get('start_utc'),None,None,x.get('location_name'),x.get('address'),hn,x.get('url'),z,m,o='Facebook: pagine mai lette (lista supplementare e promotori)')
# 12. feed iCal e REST dei siti delle fonti (26 ottobre, leve L18/L20/L51): Teatri in Comune, The Events Calendar, Events Manager
PF=f'{S}/feed/feed_eventi.json'
if os.path.exists(PF):
    for x in json.load(open(PF)):
        z,m=(x['zona'],x['municipio']) if x.get('zona') else (zone_ll(x['lat'],x['lon']) if x.get('lat') else zone_from_text(x.get('luogo') or ''))
        add('sito della fonte',x['titolo'],x['inizio'],x['fine'],x.get('ora'),x.get('luogo'),None,x.get('org'),x.get('url'),z,m,o='feed iCal e REST dei siti (26 ott)')
# 12 b. fonti gratuite della sera del 26 ottobre (leve L19, L56, L11, L48, L57, L59): pagine evento schema.org dei tipi «evento» di
# WordPress, link esterni dei post, feed RSS di enti (candidati), VisitLazio. ilparioli.it escluso (aggregatore, verifica di L05/L19).
PG=f'{S}/feed/fonti_gratis.json'
if os.path.exists(PG):
    SEDE={}
    for f_ in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']:
        for u_ in (f_.get('canali') or {}).get('sito') or []:
            h_=re.sub(r'^https?://(www\.)?','',u_).split('/')[0].lower()
            if f_.get('lat') and h_ not in SEDE: SEDE[h_]=(f_['lat'],f_['lon'])
    SEDE_UNICA={'bioparco.it','ambrajovinelli.org','teatroghione.it','teatrodidocumenti.org','scuolamusicatestaccio.it','cometaoff.it'}   # siti di un luogo solo
    ORIG={'tipi evento WordPress':'siti: tipi evento di WordPress (26 ott)','link dei post':'siti: pagine ufficiali linkate dai post (26 ott)','feed RSS di enti':'feed RSS di enti (26 ott)','VisitLazio':'VisitLazio (26 ott)'}
    for x in json.load(open(PG)):
        h_=x['host'].replace('www.','')
        if h_=='ilparioli.it': stat['fonti gratuite: aggregatore escluso']+=1; continue
        z,m=zone_from_text(f"{x.get('luogo') or ''} {x.get('indirizzo') or ''}")
        if not z and h_ in SEDE_UNICA and h_ in SEDE: z,m=zone_ll(*SEDE[h_])
        if x['canale']!='VisitLazio' and not z and not (x.get('luogo') or x.get('indirizzo')) and h_ not in SEDE_UNICA: stat['fonti gratuite: senza luogo né sede unica']+=1; continue
        add('sito della fonte',x['titolo'],x['inizio'],x.get('fine'),x.get('ora'),x.get('luogo'),x.get('indirizzo'),x.get('org'),x.get('url'),z,m,o=ORIG.get(x['canale'],x['canale']))
        if x.get('dv') and ev and ev[-1]['url']==x.get('url'): ev[-1]['dv']=True
# 13. recupero geografico degli eventi senza pagina (26 ottobre, leve L01 e L02): luogo già visto con una sola pagina;
# indirizzo con civico geocodificato con Nominatim (cache, un'interrogazione al secondo, © OpenStreetMap contributors, ODbL).
# Le schede di Roma Today restano senza pagina (DEC-026 aperta).
import time,urllib.request,urllib.parse
GEN=re.compile(r'^(teatro|location|scuola primaria|rome, italy|roma|sede|online|parrocchia|biblioteca|centro|piazza|via)\b',re.I)
visti=collections.defaultdict(set)
for e in ev:
    if e['z'] and e.get('luogo') and len(norm(e['luogo']))>=8 and not GEN.match(e['luogo'].strip()): visti[norm(e['luogo'])].add(e['z'])
CIV=re.compile(r"\b(via|viale|piazza|piazzale|largo|lungotevere|vicolo|corso|circonvallazione)\s+([^,\d\n]{3,60}?),?\s*(?:n\.?\s*)?(\d{1,4}[a-z]?)\b",re.I)
CP=f'{S}/geo/cache_eventi.json'; GC=json.load(open(CP)) if os.path.exists(CP) else {}
UA="QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"; tlast=[0]
def nominatim(street):
    k=street.lower()
    if k not in GC:
        w=tlast[0]+1.1-time.time()
        if w>0: time.sleep(w)
        tlast[0]=time.time()
        q=urllib.parse.urlencode({'street':street,'city':'Roma','countrycodes':'it','format':'jsonv2','limit':1,'addressdetails':1})
        try:
            with urllib.request.urlopen(urllib.request.Request('https://nominatim.openstreetmap.org/search?'+q,headers={'User-Agent':UA}),timeout=30) as r: d=json.loads(r.read().decode())
            GC[k]=d[0] if d else None
        except Exception: GC[k]=None
    return GC[k]
LUOGHI={}   # gazetteer dei luoghi (leva L03): luoghi di culture.roma.it e biblioteche, nome -> coordinate
for v_ in json.load(open('/mnt/user-data/outputs/culture_luoghi.json')).values():
    for n_ in [v_.get('titolo') or ''] + (v_.get('titolo') or '').split(' - ')[:1]:
        if len(norm(n_))>=10 and v_.get('lat'): LUOGHI.setdefault(norm(n_),(v_['lat'],v_['lon']))
for b_ in json.load(open(f'{S}/mirate/bib.json')):
    c_=str(b_.get('sito') or '').rstrip('/').split('/')[-1]
    if c_ in BIB and len(norm(b_['nome']))>=8: LUOGHI.setdefault(norm('biblioteca '+b_['nome']),BIB[c_][:2]); LUOGHI.setdefault(norm(b_['nome']),BIB[c_][:2])
for e in ev:
    if e['z'] or e['src']=='Roma Today': continue
    lu=norm(e.get('luogo'))
    if lu in visti and len(visti[lu])==1: e['z']=next(iter(visti[lu])); e['m']=e['m'] or pages[e['z']]['primary_municipality']; stat['recupero: luogo già visto']+=1; continue
    hit=next((LUOGHI[k_] for k_ in ([lu]+[k for k in LUOGHI if len(k)>=14 and f' {k} ' in f' {lu} ']) if k_ in LUOGHI),None) if lu else None
    if hit:
        z,mun=zone_ll(*hit)
        if z: e['z']=z; e['m']=mun or e['m']; stat['recupero: luogo noto per nome']+=1; continue
    txt=f"{e.get('luogo') or ''} {e.get('ind') or ''}"
    if PROVT.search(txt) or not CIV.search(txt): continue
    m=CIV.search(txt); r=nominatim(f"{m.group(1)} {m.group(2).strip()} {m.group(3)}")
    if not r or r.get('addresstype') in ('road','city','suburb','quarter','neighbourhood','administrative','county','state','village','town'): stat['recupero: indirizzo non risolto']+=1; continue
    z,mun=zone_ll(r['lat'],r['lon'])
    if z: e['z']=z; e['m']=mun or e['m']; stat['recupero: indirizzo geocodificato']+=1
    else: stat['recupero: fuori dal Comune']+=1
json.dump(GC,open(CP,'w'),ensure_ascii=False)
ev.sort(key=lambda e:(e['d1'],e['ora'] or '',e['t']))
P=[{'id':z,'nome':p['name_display'],'mun':p['primary_municipality']} for z,p in sorted(pages.items(),key=lambda kv:kv[1]['name_display'])]
for f in (('eventi.json','eventi_zu.json') if GEO=='zu' else ('eventi_sudd.json',)):   # eventi_zu.json resta per il confronto con gli abitanti
    json.dump({'oggi':TODAY,'pagine':P,'eventi':ev},open(f'{S}/pagina_eventi/{f}','w'),ensure_ascii=False,separators=(',',':'))
c=collections.Counter(e['z'] for e in ev)
print(dict(stat)); print('eventi',len(ev),'con pagina QN',sum(1 for e in ev if e['z']),'senza',sum(1 for e in ev if not e['z']),'pagine con almeno un evento',sum(1 for p in P if c.get(p['id'])),'a zero',sum(1 for p in P if not c.get(p['id'])),'>=10',sum(1 for p in P if c.get(p['id'],0)>=10))

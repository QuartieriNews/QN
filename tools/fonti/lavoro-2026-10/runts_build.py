# Enti del terzo settore di Roma (RUNTS): presenza web, attività, eventi, geografia, verdetto come fonte di eventi -> xlsx
import json,sys,re,glob,os,collections,unicodedata
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S,OUT=sys.argv[1:3]; W=f'{S}/runts/work'
E=json.load(open(f'{W}/enti.json')); M=json.load(open(f'{W}/match.json')); V=json.load(open(f'{W}/sites_all.json'))
FBJ=json.load(open(f'{W}/fb.json')); FB=FBJ['per_ente']; SHARED=FBJ['condivise']
G=json.load(open(f'{W}/geo.json')) if os.path.exists(f'{W}/geo.json') else {}
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); zones={z['publication_zone_id']:z for z in gz['publication_zones']}
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
EV=collections.defaultdict(list)
for f in glob.glob(f'{W}/fb_events/*.json'):
    for it in json.load(open(f)):
        q=(it.get('_metadata') or {}).get('query'); EV[key(q)].append(it)
PO=collections.defaultdict(list); POERR=set()
for f in glob.glob(f'{W}/fb_posts/*.json'):
    for it in json.load(open(f)):
        k=key(it.get('inputUrl'))
        if it.get('error'): POERR.add(k)
        else: PO[k].append(it)
LETTE_EV=set(json.load(open(f'{W}/fb_events_lette.json'))) if os.path.exists(f'{W}/fb_events_lette.json') else set()
LETTE_PO=set(json.load(open(f'{W}/fb_posts_lette.json'))) if os.path.exists(f'{W}/fb_posts_lette.json') else set()
MESI=r'gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre'
DATA=re.compile(r'(\b\d{1,2}\s*(?:'+MESI+r')\b|\b\d{1,2}[/.]\d{1,2}(?:[/.]\d{2,4})?\b|\bore\s+\d{1,2}[.:,]?\d{0,2}\b|\balle\s+\d{1,2}[.:,]?\d{0,2}\b)',re.I)
EVENTO=re.compile(r'\b(evento|eventi|incontro|presentazione|festa|laboratori?o?|concerto|mostra|spettacolo|assemblea|conferenza|seminario|workshop|visita guidata|passeggiata|torneo|proiezione|cineforum|reading|dibattito|iniziativa|appuntamento|vi aspettiamo|ti aspettiamo|open day|mercatino|inaugurazione|convegno|giornata|manifestazione|presidio|corteo|raccolta)\b',re.I)
# soggetti già noti
def slug(u): return key(u)
cens={}
if os.path.exists(f'{S}/assoc/rows.json'):
    for r in json.load(open(f'{S}/assoc/rows.json')): cens[slug(r['url_pagina'])]=r.get('verdetto')
sched=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
wiki_by_name={}; wiki_by_fb={}
for e in sched:
    for a in [e['nome']]+e['alias']: wiki_by_name[norm(a)]=e
    for k in e['chiavi']:
        if k.startswith('fb-page:'): wiki_by_fb[k[8:]]=e
# temi dal nome
TEMI=[('cultura e spettacolo',r'teatr|musica|music|cinema|film|arte\b|arti\b|artist|cultur|danza|coro|corale|band|orchestr|letter|libr|poesi|fotograf|museo|festival|spettacol|accademia|canto|jazz|opera\b|lirica|circo|scena|compagnia'),
      ('quartiere e cittadinanza',r'quartier|comitato|cittadin|rione|borgata|municipio|retake|decoro|orti?\b|giardin|parco|villa |piazza|territor|comunit|social street|condomin'),
      ('sport',r'sport|calcio|basket|volley|pallavol|nuoto|tennis|atletic|ciclism|bici|running|podis|palestr|yoga|arti marziali|karate|judo|rugby|scherma|vela|canoa|equitaz|dilettantistic|polisportiv|\bssd\b|\basd\b'),
      ('ambiente e animali',r'ambient|ecolog|natura|green|verde|clima|animal|cani|gatti|felin|canil|zampa|lav\b|enpa|legambiente|wwf|bosco|fiume|tevere|riserva'),
      ('educazione e giovani',r'scuol|educa|giovan|ragazz|bambin|infanzia|minori|famigli|genitori|student|formazion|doposcuola|ludoteca|scout|oratorio'),
      ('sociale e salute',r'malat|pazient|salute|sanit|ospedal|disabil|handicap|autism|down\b|sclerosi|tumor|cancro|alzheimer|diabet|cuore|onco|dipendenz|alcol|carcer|detenut|senza dimora|poveri|caritas|banco aliment|mensa|assistenza|cura\b|anzian|hospice|psico|mentale|sordi|ciechi|ipovedent|donatori|sangue|avis|croce'),
      ('migranti e internazionale',r'migrant|rifugiat|stranier|intercultur|internaz|cooperazion|solidariet|africa|asia|america|palestin|ucrain|siria|peru|brasil|cina|india|bangla|filippin|romen|polacc|mondo|world|international|global|sviluppo'),
      ('religione',r'parrocch|chiesa|cattolic|cristian|evangel|islam|ebraic|buddh|religio|diocesi|missionar|suore|frati|francescan|salesian|gesuit|caritas'),
      ('lavoro e impresa sociale',r'cooperativ|impresa sociale|lavoro|inserimento|occupaz|servizi|consorzio|\bsrl\b')]
def temi(n):
    t=[k for k,rx in TEMI if re.search(rx,n,re.I)]; return t or ['altro']
NAZ=re.compile(r'\b(nazionale|italiana|italiani|italia|internazionale|europea|europe|federazione|confederazione|consiglio nazionale)\b',re.I)
LOCALE=re.compile(r'\b(roma|romano|romana|quartiere|municipio|rione|borgata|comitato|parrocchia|biblioteca|centro anziani)\b',re.I)
EMS=json.load(open(f'{W}/emails_sito.json')) if os.path.exists(f'{W}/emails_sito.json') else {}
FREE=re.compile(r'@(gmail|googlemail|libero|hotmail|outlook|live|yahoo|tiscali|alice|virgilio|icloud|me|fastwebnet|tin|inwind|email|katamail|aruba|msn)\.',re.I)
PEC=re.compile(r'(@pec\.|\.pec\.|@legalmail|@postecert|@arubapec|@pecditta|@cert\.|@pec[a-z]*\.|^pec[._@])',re.I)
GEN=re.compile(r'^(info|informazioni|segreteria|segretario|associazione|contatti|contatto|contact|staff|presidenza|presidente|direzione|amministrazione|ufficio|posta|mail|hello|ciao|sede|org|organizzazione|redazione|accoglienza|volontari|volontariato|soci)\b',re.I)
IMP=re.compile(r'^(eventi|events|evento|comunicazione|ufficiostampa|ufficio\.stampa|stampa|press|media|cultura|programmazione|prenotazioni|biglietteria|teatro|spettacoli)\b',re.I)
def pick_emails(site,site_emails,fb_email,name_core):
    dom=re.sub(r'^https?://(www\.)?','',site or '').split('/')[0].lower()
    toks=[t for t in norm(name_core).split() if len(t)>3]
    cands={}
    def add(e,src,base):
        e=e.lower().strip()
        if e in cands: cands[e]['score']=max(cands[e]['score'],base); cands[e]['fonti'].add(src); return
        cands[e]={'score':base,'fonti':{src}}
    fbe=[x.strip().lower() for x in re.split(r'[;,\s]+',str(fb_email or '')) if '@' in x]
    for e in site_emails+fbe:
        local,_,edom=e.partition('@'); same=bool(dom) and (edom==dom or edom.endswith('.'+dom) or dom.endswith('.'+edom))
        src='sito' if e in site_emails else 'pagina Facebook'
        if PEC.search(e): add(e,src,-1); continue
        namey=any(t in norm(local).replace(' ','') for t in toks)
        if same: base=100 if GEN.match(local) else 90 if IMP.match(local) else 75
        elif FREE.search(e): base=70 if (namey or GEN.match(local)) else 55
        elif namey: base=65    # dominio diverso ma col nome dell'ente (sito precedente, rete)
        else: base=20          # dominio di terzi trovato sul sito: non è dell'ente
        if e in fbe: base+=10
        add(e,src,base)
    good=sorted([(v['score'],e) for e,v in cands.items() if v['score']>=55],key=lambda x:(-x[0],x[1]))
    pec=next((e for e,v in cands.items() if v['score']==-1),None)
    if not good: return None,[],None,pec
    prim=good[0][1]; altre=[e for sc,e in good[1:] if IMP.match(e.split('@')[0]) or sc>=75][:2]
    return prim,altre,' + '.join(sorted(cands[prim]['fonti'])),pec
rows=[]; stats=collections.Counter(); evrows=[]
for e in E:
    cf=e['cf']; m=M.get(cf,{}); v=V.get(cf,{}); f=FB.get(cf) or {}; fu=f.get('facebook'); fk=key(fu)
    p=(P.get(fk) or {}) if fk else {}; evs=EV.get(fk,[]) if fk else []; pos=PO.get(fk,[]) if fk else []; g=G.get(cf,{})
    fut=[x for x in evs if str(x.get('is_past'))!='True']
    from_roma=[x for x in fut if 'Rome' in str(x.get('city') or '') or 'Roma' in str(x.get('address') or '')]
    pe=[x for x in pos if DATA.search(x.get('text') or '') and EVENTO.search(x.get('text') or '')]
    last_post=max((x.get('time') or '' for x in pos),default='')[:10] or None
    sito=v.get('sito'); ig=(v.get('instagram_dal_sito') if sito else None) or m.get('instagram')
    mun=g.get('municipio'); zona=match(g.get('sudd_nome'),mun) if g else None
    tm=temi(e['denominazione']+' '+str(p.get('category') or '')+' '+' '.join(p.get('categories') or []))
    known=wiki_by_fb.get(fk) or wiki_by_name.get(norm(e['core'])) or wiki_by_name.get(norm(e['denominazione']))
    cv=cens.get(fk)
    page_err=bool(p.get('error'))
    presenza='sito e Facebook' if sito and fu and not page_err else 'solo sito' if sito else 'solo Facebook' if fu and not page_err else 'Facebook non disponibile' if fu else 'nessuna presenza web trovata'
    # verdetto
    nd=v.get('date_future') or 0; n6=v.get('date_6_mesi') or 0
    if from_roma: vd,mo='rientra: eventi futuri su Facebook',f"{len(from_roma)} eventi futuri a Roma (prossimo {min(str(x.get('start_utc'))[:10] for x in from_roma)})"
    elif nd>=2: vd,mo='rientra: calendario sul sito',f"{nd} date future sul sito"
    elif len(pe)>=2: vd,mo='rientra: annuncia eventi nei post Facebook',f"{len(pe)} post con data e annuncio negli ultimi sei mesi"
    elif n6>=3: vd,mo='rientra: attiva negli ultimi 6 mesi (sito)',f"{n6} date negli ultimi sei mesi sul sito"
    elif nd==1 or len(pe)==1 or n6 in (1,2): vd,mo='da verificare: un solo segnale di eventi',('1 data futura sul sito' if nd==1 else '1 post di annuncio' if len(pe)==1 else f'{n6} date recenti sul sito')
    elif v.get('pagina_eventi'): vd,mo='da verificare: pagina eventi sul sito senza date leggibili',v['pagina_eventi']
    elif fut: vd,mo='da valutare: eventi futuri fuori Roma o online',f"{len(fut)} eventi futuri, nessuno a Roma"
    elif pos: vd,mo='attiva su Facebook, senza annunci di eventi',f"{len(pos)} post negli ultimi sei mesi (ultimo {last_post})"
    elif presenza=='nessuna presenza web trovata': vd,mo='nessuna presenza web trovata','nessun sito verificato né pagina Facebook riconosciuta'
    elif sito or fu: vd,mo='presente sul web, nessun segnale di eventi','sito o pagina senza date, eventi o post recenti'
    else: vd,mo='nessuna presenza web trovata',''
    if vd.startswith(('rientra','da verificare')) and ('lavoro e impresa sociale' in tm and len(tm)==1): vd,mo='servizio o impresa sociale: '+vd,mo
    if vd.startswith('rientra') and NAZ.search(e['denominazione']) and not LOCALE.search(e['denominazione']) and not zona: vd='rientra (ente nazionale o tematico: controllare il radicamento locale)'
    stats[vd]+=1
    dove=[]
    if v.get('pagina_eventi'): dove.append(v['pagina_eventi'])
    elif sito: dove.append(sito)
    if fu and not page_err:
        dove.append(fu+'&sk=events' if 'profile.php' in fu else fu.rstrip('/')+'/events')
    r={'codice_fiscale':cf,'denominazione':e['denominazione'],'sezione_runts':e['sezione'],'5x1000':e['x5'],'iscrizione':e['data'],'temi':', '.join(tm),
       'presenza_web':presenza,'verdetto':vd,'motivo':mo,'dove_cercare':' · '.join(dove) or None,
       'sito':sito,'sito_prova':v.get('sito_prova'),'sito_trovato_con':v.get('sito_trovato_con'),'sito_pagina_eventi':v.get('pagina_eventi'),'sito_date_future':v.get('date_future'),'sito_date_6_mesi':v.get('date_6_mesi'),'sito_ultima_data':v.get('ultima_data'),
       'facebook':fu,'facebook_origine':f.get('facebook_origine'),'facebook_condivisa':'sì' if fk in SHARED else None,'facebook_categoria':p.get('category'),'facebook_follower':p.get('followers'),'facebook_creata':p.get('creation_date'),
       'fb_eventi_futuri':len(fut) if fk and fk in LETTE_EV else None,'fb_eventi_futuri_roma':len(from_roma) if fk and fk in LETTE_EV else None,'fb_post_6_mesi':len(pos) if fk and fk in LETTE_PO else None,'fb_post_con_eventi':len(pe) if fk and fk in LETTE_PO else None,'fb_ultimo_post':last_post,
       'instagram':ig,'telefono':p.get('phone'),
       'indirizzo':g.get('indirizzo') or v.get('indirizzo_dal_sito'),'municipio':mun,'suddivisione_ufficiale':g.get('suddivisione'),'zona_qn':zona,'zona_qn_nome':zones[zona]['name_display'] if zona else None,'geo_fonte':g.get('fonte'),'lat':g.get('lat'),'lon':g.get('lon'),
       'gia_nella_wiki':known['id'] if known else None,'nel_censimento_24_ott':cv,'risultati_google':m.get('risultati')}
    em=EMS.get(cf) or {}
    prim,altre,efonte,pec=pick_emails(sito,em.get('sito_email') or [],p.get('email'),e['core'])
    r['email_principale']=prim; r['email_altre']=', '.join(altre) or None; r['email_fonte']=efonte; r['pec']=pec
    rows.append(r)
    for x in from_roma: evrows.append([cf,e['denominazione'],x.get('name'),str(x.get('start_utc') or '')[:16].replace('T',' '),x.get('location_name'),x.get('address'),x.get('url')])
cols=list(rows[0].keys()); EC=['email_principale','email_altre','email_fonte','pec']; cols=[c for c in cols if c not in EC]; i=cols.index('dove_cercare')+1; cols=cols[:i]+EC+cols[i:]
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Enti'; ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for r in rows: ws.append([r[c] for c in cols])
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=45 if c in ('denominazione','dove_cercare','motivo','sito','facebook','verdetto') else 14
ws.freeze_panes='C2'
wr=wb.create_sheet('Riepilogo'); wr.append(['misura','valore'])
for c in wr[1]: c.font=Font(bold=True)
def add(k,v): wr.append([k,v])
add('enti nel file RUNTS',len(rows))
for k,v in collections.Counter(r['presenza_web'] for r in rows).most_common(): add('presenza web: '+k,v)
add('siti verificati (codice fiscale o nome nella pagina)',sum(1 for r in rows if r['sito']))
add('pagine Facebook',sum(1 for r in rows if r['facebook'])); add('profili Instagram',sum(1 for r in rows if r['instagram']))
add('con Municipio',sum(1 for r in rows if r['municipio'])); add('con pagina QN',sum(1 for r in rows if r['zona_qn']))
add('con email principale',sum(1 for r in rows if r['email_principale'])); add('  di cui sul dominio del sito',sum(1 for r in rows if r['email_principale'] and r['sito'] and r['email_principale'].split('@')[1] in r['sito'])); add('con email in più (eventi, stampa, comunicazione)',sum(1 for r in rows if r['email_altre'])); add('con PEC trovata',sum(1 for r in rows if r['pec']))
add('già nella wiki delle fonti',sum(1 for r in rows if r['gia_nella_wiki'])); add('già nel censimento del 24 ottobre',sum(1 for r in rows if r['nel_censimento_24_ott']))
wr.append([])
wr.append(['verdetto','enti'])
for k,v in stats.most_common(): add(k,v)
wr.append([]); wr.append(['sezione RUNTS','enti','con presenza web','rientrano'])
for s,n in collections.Counter(r['sezione_runts'] for r in rows).most_common():
    wr.append([s,n,sum(1 for r in rows if r['sezione_runts']==s and r['presenza_web']!='nessuna presenza web trovata'),sum(1 for r in rows if r['sezione_runts']==s and r['verdetto'].startswith('rientra'))])
wr.append([]); wr.append(['tema (dal nome e dalla categoria Facebook)','enti','rientrano'])
tc=collections.Counter(t for r in rows for t in r['temi'].split(', '))
for t,n in tc.most_common(): wr.append([t,n,sum(1 for r in rows if t in r['temi'].split(', ') and r['verdetto'].startswith('rientra'))])
wr.append([]); wr.append(['municipio','enti','rientrano'])
for mn in ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']:
    wr.append([mn,sum(1 for r in rows if r['municipio']==mn),sum(1 for r in rows if r['municipio']==mn and r['verdetto'].startswith('rientra'))])
wr.column_dimensions['A'].width=60
we=wb.create_sheet('Eventi futuri Facebook'); we.append(['codice_fiscale','ente','evento','inizio','luogo','indirizzo','url'])
for c in we[1]: c.font=Font(bold=True)
for x in sorted(evrows,key=lambda x:x[3]): we.append(x)
for i,w in enumerate([14,40,50,16,30,40,45],1): we.column_dimensions[get_column_letter(i)].width=w
wb.save(OUT); json.dump(rows,open(f'{W}/rows.json','w'),ensure_ascii=False)
print(len(rows),stats.most_common()); print('zone QN con enti che rientrano',len({r['zona_qn'] for r in rows if r['zona_qn'] and r['verdetto'].startswith('rientra')}))

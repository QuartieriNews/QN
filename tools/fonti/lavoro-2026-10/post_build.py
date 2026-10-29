# Eventi annunciati nei post Facebook di tutte le pagine lette: estrazione, unione dei doppioni, pagina QN della fonte -> xlsx + json
import json,re,glob,sys,collections,unicodedata,openpyxl
from datetime import date
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/post_eventi'; sys.path.insert(0,P)
from estrai import estrai,norm
TODAY=date(2026,10,25)
def key(u):
    u=str(u or '')
    m=re.search(r'profile\.php\?id=(\d+)',u)
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:p/|people/[^/]+/)?([^/?#]+)',u)
    if not m: return None
    s=m.group(1).lower(); m2=re.search(r'-(\d{8,})/?$',s); return m2.group(1) if m2 else s
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); pages={z['publication_zone_id']:z for z in gz['publication_zones'] if z.get('is_page')}
info={}
wb=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v4.xlsx',read_only=True); rr=list(wb.worksheets[0].iter_rows(values_only=True)); h=rr[0]
for r in rr[1:]:
    d=dict(zip(h,r)); k=key(d.get('facebook'))
    if k: info.setdefault(k,{'nome':d['nome'],'zona':d.get('zona_qn'),'mun':d.get('municipio'),'origine':'registro ('+str(d.get('origine'))+')','decisione':d.get('decisione'),
                             'zona_da_ricerca':bool(re.search(r'fonti_mirate|ricerca_quartieri',str(d.get('origine'))))})   # la zona è quella della ricerca, non la sede
for r in json.load(open(f'{S}/runts/work/rows.json')):
    k=key(r.get('facebook'))
    if k: info.setdefault(k,{'nome':r['denominazione'],'zona':r.get('zona_qn'),'mun':r.get('municipio'),'origine':'censimento RUNTS','decisione':r['verdetto']})
for r in json.load(open(f'{S}/assoc/rows.json')):
    k=key(str(r.get('url_pagina')).replace('facebook.com/','www.facebook.com/'))
    if k: info.setdefault(k,{'nome':r['nome'],'zona':r.get('zona_qn'),'mun':r.get('municipio'),'origine':'censimento associazioni','decisione':r.get('verdetto')})
# titolo umano delle pagine Facebook già lette: serve a riconoscere una pagina che non è del soggetto a cui il censimento l'ha attribuita
FBT={}
for f in glob.glob(f'{S}/runts/work/fb_pages/*.json')+glob.glob(f'{S}/assoc/pages_data/*.json')+glob.glob(f'{S}/owner_pagine/pages_*.json')+glob.glob(f'{S}/promotori/fbpages_*.json'):
    for x in json.load(open(f)):
        if isinstance(x,dict) and x.get('title'):
            for u in (x.get('facebookUrl'),x.get('pageUrl'),x.get('inputUrl')):
                if key(u): FBT.setdefault(key(u),x['title'])
STOPW=set('associazione ass asd aps odv onlus ets centro circolo comitato di del della dei degli delle e il la lo le gli i in roma parrocchia chiesa san santa santo culturale sportiva quartiere sociale per a da al alla impresa srl cooperativa ente nazionale italia italiana'.split())
def rnorm(x): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',re.sub(r'([a-z])([A-Z])',r'\1 \2',str(x or ''))).encode('ascii','ignore').decode().lower())).strip()
def initials(x,keep_small):
    small={'di','del','della','delle','dei','degli','e','la','il','lo','le','gli','i','per','a','da','in','al','alla','of','the','and'}
    return ''.join(w[0] for w in rnorm(x).split() if w and (keep_small or w not in small))
def related(a,b):   # stesso soggetto? parole, nomi attaccati (camelCase), sigle (AVO, CSP, ANDOS…)
    if not rnorm(a) or not rnorm(b): return True
    ca,cb=rnorm(a).replace(' ',''),rnorm(b).replace(' ','')
    ta=[w for w in rnorm(a).split() if w not in STOPW and len(w)>=4]; tb=[w for w in rnorm(b).split() if w not in STOPW and len(w)>=3]
    if any(w in cb for w in ta) or any(w in ca for w in tb) or ca in cb or cb in ca: return True
    for x,y in ((a,cb),(b,ca)):
        for ks in (False,True):
            ini=initials(x,ks)
            if len(ini)>=3 and any(ini[i:i+n] in y for n in range(min(len(ini),5),2,-1) for i in range(len(ini)-n+1)): return True
    return False
files={'censimento RUNTS':glob.glob(f'{S}/runts/work/fb_posts/*.json'),'censimento associazioni':glob.glob(f'{S}/assoc/posts_data/*.json'),'pagine verificate dall’owner':glob.glob(f'{P}/owner_*.json'),'secondo giro':glob.glob(f'{P}/giro2/posts_*.json')}
G2={}   # secondo giro (25 ottobre): pagine salvate mai lette, lotto per origine
for k,v in (json.load(open(f'{P}/giro2/giro2_pagine.json')).items() if glob.glob(f'{P}/giro2/giro2_pagine.json') else []):
    o=v[1]; G2[k]='secondo giro: '+('fonti mirate e ricerca quartieri (registro v4)' if o.startswith('registro v4') else 'pagine nuove della ricerca quartieri' if o.startswith('ricerca') else o)
st=collections.Counter(); ev={}; pages_read=collections.defaultdict(set); posts_per=collections.Counter()
for lot0,fs in files.items():
    for f in sorted(fs):
        for p in json.load(open(f)):
            k=key(p.get('inputUrl') or p.get('facebookUrl') or p.get('url'))
            if not k: continue
            lot=G2.get(k,'secondo giro: altro') if fs is files['secondo giro'] else lot0
            pages_read[lot].add(k)
            if p.get('error') or not p.get('text') or not p.get('time'): continue
            posts_per[(lot,k)]+=1
            if posts_per[(lot,k)]>15: continue      # al massimo gli ultimi 15 post per pagina
            st[lot+': post letti']+=1
            e=estrai(p['text'],p['time'],TODAY)
            if not e: continue
            st[lot+': post con un evento']+=1
            i=info.get(k,{})
            tit=FBT.get(k) or p.get('pageName')
            if i and tit and not related(i.get('nome'),tit) and not related(i.get('nome'),p.get('pageName')):
                st['post di una pagina diversa dal soggetto del censimento']+=1
                i={'nome':tit,'origine':'pagina Facebook diversa dal soggetto a cui era attribuita'}   # la sede di quel soggetto non vale
            kk=(k,norm(e['titolo'] or '')[:40],e['inizio'] if not e['ricorrente'] else e['ricorrente'])
            if kk in ev:
                ev[kk]['ripetizioni']+=1; ev[kk]['ora']=ev[kk]['ora'] or e['ora']; ev[kk]['luogo']=ev[kk]['luogo'] or e['luogo']; continue
            ev[kk]={**e,'pagina':k,'fonte':i.get('nome') or p.get('pageName') or k,'zona':i.get('zona'),'zona_da_ricerca':i.get('zona_da_ricerca',False),'testo_pieno':re.sub(r'\s+',' ',p['text'])[:600],'municipio':i.get('mun'),'origine_fonte':i.get('origine') or lot,'lotto':lot,'url_post':p.get('url'),'ripetizioni':1}
E=list(ev.values())
def nrm(x): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(x or '')).encode('ascii','ignore').decode().lower())).strip()
NM={}
for n in gz['neighbourhoods']:
    for a in [n['name_display']]+re.split(r'[;|/]',n.get('aliases') or ''):
        if len(nrm(a))>=6 and n.get('publishable',True) is not False and nrm(a) not in ('centro','parco','villa','italia'): NM.setdefault(nrm(a),n)
for z in gz['publication_zones']:
    if z.get('is_page') and len(nrm(z['name_display']))>=5: NM.setdefault(nrm(z['name_display']),{'publication_zone_id':z['publication_zone_id'],'municipality_code':z['primary_municipality']})
STREET=re.compile(r"\b(?:via|viale|v\.le|piazza|p\.zza|piazzale|largo|vicolo|lungotevere|circonvallazione|corso|borgo|salita|clivo|stazione|fermata)\s+(?:(?:d[ei]|degli|della|delle|del|dell'|di|san|santa|santo|ss\.?)\s+){0,3}[\w'’]+(?:\s+[A-Z][\w'’]+){0,3}",re.I)
def zone_text(t):
    t=STREET.sub(' ',str(t or ''))      # un nome di strada non dice il quartiere (via dei Monti di San Paolo non è a San Paolo)
    tt=' '+nrm(t)+' '; best=None
    for k,n in NM.items():
        if f' {k} ' in tt and (best is None or len(k)>len(best[0])): best=(k,n)
    return (best[1]['publication_zone_id'],best[1].get('municipality_code')) if best else (None,None)
fut=[e for e in E if e['fine']>=TODAY.isoformat()]
for e in fut:
    zt,mt=zone_text((e.get('luogo') or '')+' '+(e.get('titolo') or ''))
    if zt in pages and zt!=e['zona']: e['zona_metodo']='luogo nominato nel post'; e['zona']=zt; e['municipio']=mt or pages[zt]['primary_municipality']
    elif e['zona'] and e['zona_da_ricerca'] and zt!=e['zona'] and zone_text(e['fonte']+' '+e['testo_pieno'])[0]!=e['zona']:
        e['zona_metodo']=None; e['zona']=None       # fonte trovata cercando il quartiere: vale solo se il nome o il post lo nominano
    elif e['zona_da_ricerca'] and e['zona']: e['zona_metodo']='quartiere nominato dalla fonte'
    else: e['zona_metodo']='sede della fonte' if e['zona'] else None
    e['zona']=e['zona'] if e['zona'] in pages else None
for e in E: e.pop('testo_pieno',None); e.pop('zona_da_ricerca',None)
json.dump(fut,open(f'{P}/eventi_post_futuri.json','w'),ensure_ascii=False,indent=1)
wbo=openpyxl.Workbook(); w=wbo.active; w.title='Riepilogo'; w.append(['misura','valore'])
for c in w[1]: c.font=Font(bold=True)
for lot in pages_read: w.append([f'{lot}: pagine lette',len(pages_read[lot])])
for k,v in st.items(): w.append([k,v])
w.append(['eventi distinti annunciati (doppioni uniti)',len(E)]); w.append(['  di cui futuri (dal 25 ottobre)',len(fut)]); w.append(['  futuri ricorrenti (ogni settimana)',sum(1 for e in fut if e['ricorrente'])])
w.append(['  futuri con pagina QN',sum(1 for e in fut if e['zona'])]); w.append(['pagine Facebook con almeno un evento futuro',len({e['pagina'] for e in fut})]); w.append(['pagine QN toccate',len({e['zona'] for e in fut if e['zona']})])
w.column_dimensions['A'].width=60
cols=['inizio','fine','ora','ricorrente','titolo','luogo','fonte','zona','zona_metodo','municipio','origine_fonte','ripetizioni','data_post','url_post','testo']
for name,L in (('Eventi futuri',sorted(fut,key=lambda e:(e['inizio'],e['fonte']))),('Tutti gli annunci',sorted(E,key=lambda e:(e['inizio'],e['fonte'])))):
    ws=wbo.create_sheet(name); ws.append(cols)
    for c in ws[1]: c.font=Font(bold=True)
    for e in L: ws.append([e.get(c) for c in cols])
    for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=45 if c in ('titolo','luogo','fonte','testo','url_post') else 12
    ws.freeze_panes='A2'
wbo.save('/mnt/user-data/outputs/eventi_dai_post_facebook.xlsx')
print(dict(st)); print({l:len(v) for l,v in pages_read.items()}); print('annunci distinti',len(E),'futuri',len(fut),'ricorrenti',sum(1 for e in fut if e['ricorrente']),'con pagina QN',sum(1 for e in fut if e['zona']),'pagine fb',len({e['pagina'] for e in fut}),'pagine QN',len({e['zona'] for e in fut if e['zona']}))

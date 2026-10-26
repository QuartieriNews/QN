# Campione per il controllo di qualità della pagina «Eventi dei quartieri»: eventi stratificati per canale, ciascuno con il testo
# della sua fonte (post del pool, descrizione dell'evento Facebook, pagina del sito riletta con robots.txt). Roma Today escluso (DEC-026).
import json,re,random,collections,os,sys,time,html as H,urllib.parse,glob,openpyxl
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
E=json.load(open(f'{S}/pagina_eventi/eventi.json')); EV=E['eventi']
for i,e in enumerate(EV): e['_i']=i
def strato(e):
    o=e.get('o') or ''
    if e['src']=='Roma Today': return None
    if o.startswith("Facebook: eventi raccolti a mano"): return 'eventi Facebook raccolti dall\'owner'
    if e['src']=='Facebook': return 'eventi Facebook delle pagine'
    if e['src']=='Facebook (post)': return 'annunci nei post Facebook'
    if e['src']=='culture.roma.it': return 'culture.roma.it'
    if o.startswith('feed iCal'): return 'feed dei siti'
    if o.startswith('Biblioteche'): return 'agenda Biblioteche di Roma'
    return 'pagine dei siti'
QUOTA={'eventi Facebook raccolti dall\'owner':25,'eventi Facebook delle pagine':20,'annunci nei post Facebook':35,'culture.roma.it':20,'pagine dei siti':25,'feed dei siti':15,'agenda Biblioteche di Roma':15}
per=collections.defaultdict(list)
for e in EV:
    s=strato(e)
    if s: per[s].append(e)
random.seed(20261026); camp=[]
for s,q in QUOTA.items(): camp+= [dict(e,strato=s) for e in random.sample(per[s],min(q,len(per[s])))]
# testi delle fonti
def pkey(u):   # i link permalink.php distinguono il post solo nella query (story_fbid): tagliarla li confondeva tutti
    u=str(u or ''); return u if 'permalink.php' in u else u.split('?')[0]
POST={}
for f in (f'{S}/l08_verifica/pool2.json',f'{S}/supplementare/posts_EaMAj9lFGNABIgkRP.json',f'{S}/post_eventi/acilia_posts.json'):
    for x in json.load(open(f)):
        if x.get('text') and x.get('url'): POST[pkey(x['url'])]=x['text']
FBX=[]
wb=openpyxl.load_workbook('/mnt/user-data/outputs/eventi_unico.xlsx',read_only=True); rr=list(wb['Facebook'].iter_rows(values_only=True)); h=rr[0]
for r in rr[1:]:
    d=dict(zip(h,r)); FBX.append({'url':d.get('url'),'nome':d.get('name'),'inizio':str(d.get('utcStartDate') or '')[:10],'testo':' · '.join(str(d.get(k) or '') for k in ('name','dateTimeSentence','location.name','address','description'))})
for f in glob.glob(f'{S}/runts/work/fb_events/*.json')+glob.glob(f'{S}/promotori/fbevents_ev_*.json')+[f'{S}/assoc/check_events.json',f'{S}/assoc/test_events.json']:
    try: d=json.load(open(f))
    except Exception: continue
    for x in d if isinstance(d,list) else []:
        if isinstance(x,dict) and x.get('name'):
            FBX.append({'url':x.get('url'),'nome':x.get('name'),'inizio':str(x.get('start_utc') or x.get('utcStartDate') or '')[:10],
                        'testo':' · '.join(str(x.get(k) or '') for k in ('name','day_time_sentence','location_name','address','description'))})
def nkey(s): return re.sub(r'[^a-z0-9]','',str(s or '').lower())[:30]
FBI={}
for x in FBX:
    FBI.setdefault(x['url'],x); FBI.setdefault((nkey(x['nome']),x['inizio']),x)
wb2=openpyxl.load_workbook('/mnt/user-data/outputs/facebook_scoperta_organizzatori.xlsx',read_only=True); r2=list(wb2['Eventi'].iter_rows(values_only=True)); h2=r2[0]
for r in r2[1:]:
    d=dict(zip(h2,r)); FBX.append({'url':d.get('url'),'nome':d.get('nome'),'inizio':str(d.get('inizio') or '')[:10],'testo':' · '.join(str(v) for v in d.values() if v)})
FBI={}
for x in FBX:
    FBI.setdefault(x['url'],x); FBI.setdefault((nkey(x['nome']),x['inizio']),x)
PRIMA={e['_i']:e for e in json.load(open(f'{S}/qualita/campione.json'))} if os.path.exists(f'{S}/qualita/campione.json') else {}
ROB={}; last={}
def pagina(u):
    h=urllib.parse.urlsplit(u).netloc
    if ls.NEVER.search(u): return None,'canale non letto (social o aggregatore)'
    def pace(_=None):
        w=last.get(h,0)+1.0-time.time()
        if w>0: time.sleep(w)
        last[h]=time.time()
    if not ls.robots_allows(u,lambda x: ls.fetch(x,timeout=20),ROB,pace): return None,'robots.txt vieta'
    pace()
    try: doc=ls.fetch(u,timeout=25)
    except Exception as ex: return None,f'pagina non raggiungibile ({type(ex).__name__} {getattr(ex,"code","")})'
    t=re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)\b.*?</\1>',' ',doc)))).strip()
    ld=' '.join(re.findall(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>',doc))[:3000]
    return (t[:6000]+(' [schema.org] '+ld if ld else '')),'pagina riletta'
st=collections.Counter()
for e in camp:
    s=e['strato']; u=e.get('url') or ''
    txt,how=None,None
    pr=PRIMA.get(e['_i'])
    if pr and pr['fonte_testo'] and not s.startswith('eventi Facebook'): e['fonte_testo'],e['fonte_come']=pr['fonte_testo'],pr['fonte_come']; st[(s,pr['fonte_come'])]+=1; continue
    if s=='annunci nei post Facebook':
        txt=POST.get(pkey(u)); how='testo del post' if txt else 'post non trovato nel pool'
    elif s.startswith('eventi Facebook'):
        x=FBI.get(u) or FBI.get((nkey(e['t']),e['d1'][:10]))
        txt=x['testo'] if x else None; how='dati dell\'evento Facebook (Apify)' if x else 'evento Facebook non trovato nei dati'
    elif u.startswith('http'):
        txt,how=pagina(u)
    else: how='senza link'
    e['fonte_testo']=(txt or '')[:6000]; e['fonte_come']=how; st[(s,how)]+=1
json.dump(camp,open(f'{S}/qualita/campione.json','w'),ensure_ascii=False,indent=0)
for k,v in sorted(st.items()): print(v,k)
print('campione',len(camp),'con testo',sum(1 for e in camp if e['fonte_testo']))

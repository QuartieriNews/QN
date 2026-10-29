# Prova del canale: per ogni promotore con un sito, si leggono home, pagina eventi (dichiarata o trovata nei link della home)
# e feed RSS del sito, e si cerca se gli eventi futuri già noti del promotore ci compaiono (titolo + data).
# robots.txt rispettato (lettore dei siti), una richiesta al secondo per host, nessun testo conservato fuori dallo scratch.
import sys,json,re,time,gzip,collections,datetime,unicodedata,urllib.parse,html as H,threading
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
sys.path.insert(0,f'{S}/promotori')
PLATHOST=re.compile(open(f'{S}/promotori/finale.py').read().split("PLATHOST=re.compile(r'")[1].split("')")[0])
CITY=re.compile(r'(^|\.)(romatoday\.it|citynews\.it|today\.it)$')
TODAY=datetime.date(2026,10,26)
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#:]+)',str(u or '').strip().lower()); return m.group(1) if m else None
P=json.load(open(f'{S}/promotori/promotori_finale.json'))
W={f['id']:f for f in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']}
# siti da provare: sito del promotore, siti e pagine eventi dello schedario
plan={}   # host -> {'root':url,'pagine':[urls],'promotori':[keys]}
def add(p,u,kind):
    h=host(u)
    if not h or PLATHOST.search(h) or CITY.search(h) or ls.NEVER.search(h): return
    if not str(u).startswith('http'): u='https://'+str(u).lstrip('/')
    d=plan.setdefault(h,{'root':None,'pagine':[],'promotori':[]})
    if kind=='sito' and not d['root']: d['root']=u
    if kind=='pagina' and u not in d['pagine']: d['pagine'].append(u)
    if p['key'] not in d['promotori']: d['promotori'].append(p['key'])
for p in P:
    if p.get('sito'): add(p,p['sito'],'sito')
    w=W.get(p.get('wiki')) or {}
    for u in (w.get('canali') or {}).get('sito') or []: add(p,u,'sito')
    for d in w.get('dove_cercare') or []:
        if d['cosa'] in ('pagina eventi del sito','pagina letta alla fonte (calendario)'): add(p,d['url'],'pagina')
        elif d['cosa']=='sito': add(p,d['url'],'sito')
for h,d in plan.items():
    if not d['root']: d['root']=f"https://{h}/" if not d['pagine'] else '{0.scheme}://{0.netloc}/'.format(urllib.parse.urlsplit(d['pagine'][0]))
print('host da provare',len(plan),'promotori',len({k for d in plan.values() for k in d['promotori']}),flush=True)
KW=[(3,r'event|calendar|agenda|programm|appuntament|cartellon|stagion|spettacol|concert|mostre|rassegn|in-scena|whats-on|prossim'),(2,r'attivit|iniziativ|incontr|laborator|corsi|news|notizi|avvis|comunicat|blog|articol|bacheca')]
A=re.compile(r'<a\b[^>]*?href\s*=\s*["\']([^"\'#]+)["\'][^>]*>(.*?)</a>',re.I|re.S)
RSS=re.compile(r'<link\b[^>]*type=["\']application/(?:rss|atom)\+xml["\'][^>]*>',re.I)
def links(base,doc,h):
    out={}
    for href,txt in A.findall(doc):
        u=urllib.parse.urljoin(base,H.unescape(href.strip()))
        if not u.startswith('http') or host(u)!=h: continue
        if re.search(r'\.(pdf|jpe?g|png|gif|zip|docx?|xlsx?|mp[34])($|\?)|wp-login|/feed/?$|/tag/|/author/|mailto:|tel:',u,re.I): continue
        t=re.sub(r'<[^>]+>',' ',txt).lower(); path=urllib.parse.urlsplit(u).path.lower()
        sc=0
        for w,rx in KW:
            if re.search(rx,path): sc=max(sc,w+1)
            elif re.search(rx,t): sc=max(sc,w)
        if path.count('/')>4: sc-=1   # un articolo singolo, non la pagina indice
        if sc>0: out[u]=max(out.get(u,0),sc)
    return sorted(out,key=lambda u:(-out[u],len(u)))
def rss_link(base,doc):
    for tag in RSS.findall(doc):
        m=re.search(r'href=["\']([^"\']+)',tag)
        if m and 'comments' not in m.group(1): return urllib.parse.urljoin(base,H.unescape(m.group(1)))
def plain(doc):
    doc=re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>',' ',doc)
    return re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',doc))).strip()
LOCK=threading.Lock(); ROB={}; out=gzip.open(f'{S}/canali/pagine.jsonl.gz','at'); done=set()
try:
    for l in gzip.open(f'{S}/canali/pagine.jsonl.gz','rt'): done.add(json.loads(l)['host'])
except Exception: pass
def work(h):
    d=plan[h]; last=[0.0]; res={'host':h,'docs':[],'errori':[],'robots_vieta':0}
    def pace(_=None):
        w=last[0]+1.0-time.time()
        if w>0: time.sleep(w)
        last[0]=time.time()
    def get(u,kind):
        if not ls.robots_allows(u,lambda x: ls.fetch(x,timeout=20),ROB,pace): res['robots_vieta']+=1; return None
        pace()
        try: doc=ls.fetch(u,timeout=20)
        except Exception as e: res['errori'].append([kind,u,type(e).__name__+':'+str(getattr(e,'code',''))]); return None
        return doc
    home=get(d['root'],'home'); pagine=list(d['pagine'])
    if home:
        txt=plain(home)
        res['docs'].append({'kind':'home','url':d['root'],'testo':txt[:150000],'righe':ls.read_page({'id':h,'nome':h},d['root'],home,TODAY,90),
                            'dinamico':len(txt)<600 or bool(re.search(r'wix\.com|squarespace|__NEXT_DATA__|id="root"></div>|id="app"></div>',home[:200000]))})
        for u in links(d['root'],home,h):
            if len(pagine)>=2: break
            if u.rstrip('/')!=d['root'].rstrip('/') and u not in pagine: pagine.append(u)
        r=rss_link(d['root'],home)
        if not r and re.search(r'wp-content|wp-json',home): r=urllib.parse.urljoin(d['root'],'/feed/')
        if r:
            doc=get(r,'rss')
            if doc and re.search(r'<(rss|feed)\b',doc[:3000]):
                items=[]
                for it in re.findall(r'(?is)<(?:item|entry)\b.*?</(?:item|entry)>',doc)[:30]:
                    g=lambda t:(re.search(rf'(?is)<{t}\b[^>]*>(.*?)</{t}>',it) or [None,''])[1]
                    tx=lambda s: plain(re.sub(r'<!\[CDATA\[|\]\]>','',s))
                    items.append({'titolo':tx(g('title'))[:200],'data':tx(g('pubDate') or g('published') or g('updated'))[:40],'testo':tx(g('content:encoded') or g('description') or g('summary') or g('content'))[:3000]})
                res['docs'].append({'kind':'rss','url':r,'items':items})
    for u in pagine[:3]:
        doc=get(u,'pagina')
        if doc: res['docs'].append({'kind':'pagina','url':u,'testo':plain(doc)[:150000],'righe':ls.read_page({'id':h,'nome':h},u,doc,TODAY,90)})
    with LOCK: out.write(json.dumps(res,ensure_ascii=False)+'\n'); out.flush()
todo=[h for h in plan if h not in done]
print('da leggere',len(todo),flush=True)
t0=time.time(); n=[0]
def run(h):
    try: work(h)
    except Exception as e:
        with LOCK: out.write(json.dumps({'host':h,'docs':[],'errori':[['crash','',repr(e)[:200]]],'robots_vieta':0})+'\n'); out.flush()
    n[0]+=1
    if n[0]%50==0: print(n[0],'host',round(time.time()-t0),'s',flush=True)
with ThreadPoolExecutor(12) as ex: list(ex.map(run,todo))
out.close(); json.dump(plan,open(f'{S}/canali/piano.json','w'),ensure_ascii=False)
print('fine',round(time.time()-t0),'s')

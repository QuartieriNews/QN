# Secondo giro (0 $) sui promotori che restano su Facebook: varianti dell'indirizzo per i siti non raggiungibili,
# ricerca interna di WordPress per i titoli degli eventi noti, elenco dei siti in JavaScript da aprire con il browser.
# robots.txt rispettato, una richiesta al secondo per host; un 401/403 è un rifiuto e non si aggira.
import sys,json,re,time,gzip,collections,datetime,urllib.parse,threading,html as H
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
exec(open(f'{S}/canali/assegna.py').read().split('out=[]; st=collections.Counter()')[0])   # dati, norm, toks, match
src=open(f'{S}/canali/prova_canale.py').read()
exec(src[src.index('KW=['):src.index('LOCK=threading.Lock()')])   # links, rss_link, plain
R=json.load(open(f'{S}/canali/regola_promotori.json')); Pk={p['key']:p for p in P}
WP={h.removeprefix('www.') for h in json.load(open(f'{S}/canali/wp_hosts.json'))}
fb=[r for r in R if r['canale'] in ('eventi Facebook','post Facebook') and r['host_provato']]
var,wp,dyn=set(),collections.defaultdict(list),set()
for r in fb:
    h=r['host_provato']; pg=pages.get(h) or {}
    p=Pk[r['key']]
    evs=[E[i] for i in p['eventi_idx'] if max(E[i]['d1'],E[i].get('d2') or E[i]['d1'])>=str(TODAY)]
    if not r['sito_letto'] and not r['robots_vieta'] and not any(e[2].startswith('HTTPError:40') for e in pg.get('errori',[])): var.add(h)
    elif r['sito_dinamico']: dyn.add(h)
    if r['sito_letto'] and (h in WP or any(d['kind']=='rss' and re.search(r'/feed/?$',d['url']) for d in pg.get('docs',[]))):
        wp[h]+= [ev for ev in evs if len(toks(ev['t']))>=2][:3]
print('varianti',len(var),'wordpress',len(wp),'eventi da cercare',sum(len(v) for v in wp.values()),'dinamici',len(dyn),flush=True)
json.dump(sorted(dyn),open(f'{S}/canali/dinamici.json','w'))
ROB={}; LOCK=threading.Lock(); out=gzip.open(f'{S}/canali/pagine2.jsonl.gz','wt')
def work(h):
    last=[0.0]; res={'host':h,'docs':[],'errori':[],'robots_vieta':0,'giro':'secondo'}
    def pace(_=None):
        w=last[0]+1.0-time.time()
        if w>0: time.sleep(w)
        last[0]=time.time()
    def get(u,kind):
        if not ls.robots_allows(u,lambda x: ls.fetch(x,timeout=20),ROB,pace): res['robots_vieta']+=1; return None
        pace()
        try: return ls.fetch(u,timeout=20)
        except Exception as e: res['errori'].append([kind,u,type(e).__name__+':'+str(getattr(e,'code',''))]); return None
    if h in var:
        for root in (f'https://www.{h}/',f'http://{h}/',f'http://www.{h}/'):
            home=get(root,'variante')
            if not home: continue
            res['docs'].append({'kind':'home','url':root,'testo':plain(home)[:150000],'righe':ls.read_page({'id':h,'nome':h},root,home,TODAY,90),
                                'dinamico':len(plain(home))<600})
            for u in links(root,home,host(root) or h)[:2]:
                doc=get(u,'pagina')
                if doc: res['docs'].append({'kind':'pagina','url':u,'testo':plain(doc)[:150000],'righe':ls.read_page({'id':h,'nome':h},u,doc,TODAY,90)})
            break
    seen=set()
    for ev in wp.get(h,[]):
        q=' '.join(sorted(toks(ev['t']),key=len,reverse=True)[:3])
        base=(pages.get(h) or {}).get('docs',[{}])[0].get('url') or f'https://{h}/'
        api=urllib.parse.urljoin(base,'/wp-json/wp/v2/search?per_page=5&search='+urllib.parse.quote(q))
        doc=get(api,'wp_search')
        try: hits=json.loads(doc) if doc else []
        except Exception: hits=[]
        if not isinstance(hits,list): continue
        tk=toks(ev['t'])
        for it in hits[:5]:
            u=it.get('url') if isinstance(it,dict) else None
            if not u or u in seen or host(u)!=host(base): continue
            if len(tk & set(norm(it.get('title','')).split()))/len(tk)<0.5: continue
            seen.add(u); d2=get(u,'pagina_trovata')
            if d2: res['docs'].append({'kind':'pagina','url':u,'testo':plain(d2)[:150000],'righe':ls.read_page({'id':h,'nome':h},u,d2,TODAY,90),'via':'ricerca WordPress'})
            break
    with LOCK: out.write(json.dumps(res,ensure_ascii=False)+'\n'); out.flush()
hosts=sorted(var|set(wp))
t0=time.time()
with ThreadPoolExecutor(12) as ex: list(ex.map(work,hosts))
out.close(); print('fine',len(hosts),round(time.time()-t0),'s')

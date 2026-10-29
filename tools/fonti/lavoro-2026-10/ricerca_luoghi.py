# Punto 3 nell'ordine giusto: per i 176 eventi senza fonte, prima i luoghi noti nello schedario (pagina del luogo letta), poi i candidati Google già verificati.
import json,re,sys,unicodedata,html,urllib.request,collections,time
from concurrent.futures import ThreadPoolExecutor
S=sys.argv[1]
sched=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
STOP={'roma','via','piazza','di','del','della','dei','delle','il','la','le','lo','e','a','in','al','alla','con','per','un','una','the','of','and','al','mostra','evento','concerto','spettacolo','teatro','museo','festival','presentazione','libro','incontro'}
def toks(s): return [t for t in norm(s).split() if len(t)>3 and t not in STOP]
byname={}
for e in sched:
    for a in [e['nome']]+e['alias']: byname[norm(a)]=e
meta=json.load(open(f'{S}/ricerca/eventi_verificati.json'))
pages=collections.defaultdict(list)
for r in json.load(open(f'{S}/siti/eventi_siti_tutti.json')): pages[r['fonte_id']].append(r)
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-eventi/1.0 (+contatto: redazione)'
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'text/html'}),timeout=25) as r: return r.read(1500000).decode('utf-8','replace')
def venue_of(m):
    l=norm(m['luogo']); 
    if not l: return None
    if l in byname: return byname[l]
    w=l.split()
    for k in range(len(w),1,-1):
        if ' '.join(w[:k]) in byname: return byname[' '.join(w[:k])]
    return None
def work(m):
    v=venue_of(m); m['luogo_nello_schedario']=v['id'] if v else None; m['luogo_nome_schedario']=v['nome'] if v else None
    if not v: return m
    tt=toks(m['nome']); 
    if not tt: return m
    # 1) righe già lette dal lettore dei siti
    for r in pages.get(v['id'],[]):
        hit=sum(1 for t in tt if t in norm(r['evento']))
        if hit>=max(2,int(0.6*len(tt))): m['fonte_luogo']=r['url'] or r['pagina']; m['fonte_luogo_prova']=f"pagina del luogo letta ({r['prova']}): {hit}/{len(tt)} parole"; return m
    # 2) la pagina da controllare del luogo, letta ora
    dove=[d['url'] for d in v['dove_cercare'] if not re.search(r'facebook|instagram',d['url'])]
    for u in dove[:2]:
        try: d=fetch(u)
        except Exception: continue
        txt=norm(html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d,flags=re.S))))
        hit=sum(1 for t in tt if t in txt)
        if hit>=max(2,int(0.6*len(tt))): m['fonte_luogo']=u; m['fonte_luogo_prova']=f"pagina del luogo: {hit}/{len(tt)} parole del titolo"; return m
        m['fonte_luogo_prova']=f"pagina del luogo letta, {hit}/{len(tt)} parole"
    return m
with ThreadPoolExecutor(max_workers=6) as ex: res=list(ex.map(work,meta))
json.dump(res,open(f'{S}/ricerca/eventi_luoghi.json','w'),ensure_ascii=False,indent=1)
print('eventi',len(res),'con luogo nello schedario',sum(1 for m in res if m['luogo_nello_schedario']),'trovati sul sito del luogo',sum(1 for m in res if m.get('fonte_luogo')),'| già con fonte da Google',sum(1 for m in res if m.get('fonte_trovata')))

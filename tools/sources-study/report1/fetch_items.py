# Re-downloads the Report 1 item pages of a textual source from its June inventory CSV
# (feasibility note §9.6, Report 1): <fonte>_items/<slug>.html, one request every DELAY seconds.
import csv, os, re, sys, time, requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
S=os.environ['QN_NET']
fonte, csvname, key, delay = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
base = sys.argv[5] if len(sys.argv)>5 else ''
out=f'{S}/{fonte}_items'; os.makedirs(out,exist_ok=True)
os.makedirs(f'{S}/logs',exist_ok=True); log=open(f'{S}/logs/fetch_{fonte}.log','a')
def say(*a): print(*a,file=log,flush=True)
from page_checks import rifiuto

rows=list(csv.DictReader(open(f'{S}/deliver/{csvname}',encoding='utf-8')))
seen=set(); ok=err=skip=0
for i,r in enumerate(rows):
    u=r[key].strip()
    if not u: continue
    u = base+u if base and not u.startswith('http') else u
    if u in seen: continue
    seen.add(u)
    slug=re.sub(r'[^A-Za-z0-9]+','_',u.rstrip('/').split('/')[-1])[:120] or f'item{i}'
    f=f'{out}/{slug}.html'
    if os.path.exists(f) and os.path.getsize(f)>500:
        if not rifiuto(open(f,encoding='utf-8',errors='replace').read()): skip+=1; continue
        os.remove(f); say(f'CACHE RIFIUTATA, riscarico {u}')   # una pagina di blocco in cache non e' un item
    d=''
    for t in range(3):
        try:
            rr=requests.get(u,headers=H,timeout=90)
            if rr.status_code==200:
                bad=rifiuto(rr.text)
                if bad: say(f'SCARTATA ({bad}) {u}'); break
                d=rr.text; break
            say(f'HTTP {rr.status_code} {u}')
        except Exception as e: say(f'ERR {type(e).__name__} {u}')
        time.sleep(3)
    if d: open(f,'w',encoding='utf-8').write(d); ok+=1
    else: err+=1; say(f'FAIL {u}')
    if (ok+err)%25==0: say(f'{ok} ok, {err} falliti, {skip} gia presenti  {time.strftime("%H:%M:%S")}')
    time.sleep(delay)
say(f'DONE {fonte}: {ok} scaricati, {err} falliti, {skip} gia presenti, {len(seen)} url unici')
print(f'DONE {fonte}: {ok} ok, {err} falliti, {skip} skip')
sys.exit(1 if err else 0)   # item irrecuperati: raccolta incompleta, dichiarata con il codice di uscita

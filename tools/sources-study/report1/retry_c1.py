# Polite retry of the Questura items that answered with the block page (feasibility note §9.6).
# One request every 90 s, and it stops after five consecutive refusals: the point is to find out
# whether the block was our own fetch rate, not to get around a source that is saying no.
# No IP change, no header games, no evasion.
import csv, os, re, time, requests, sys
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
sys.path.insert(0, os.environ['QN_NET']+'/report1')
from page_checks import rifiuto  # the fetcher uses the same rule
S=os.environ['QN_NET']
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'it-IT,it;q=0.9'}
os.makedirs(S+'/logs',exist_ok=True); log=open(S+'/logs/retry_c1.log','a')
def say(*a): print(*a,file=log,flush=True)
rows=list(csv.DictReader(open(S+'/deliver/C1_2026-06_items.csv',encoding='utf-8')))
ok=blocchi=consecutivi=0
say(f'INIZIO {time.strftime("%H:%M:%S")} — {len(rows)} item, uno ogni 90 s')
for r in rows:
    u=r['url'].strip()
    slug=re.sub(r'[^A-Za-z0-9]+','_',u.rstrip('/').split('/')[-1])[:120]
    f=f'{S}/C1_items/{slug}.html'
    if os.path.exists(f) and os.path.getsize(f)>500:
        if not rifiuto(open(f,encoding='utf-8',errors='replace').read()): continue
        os.remove(f); say(f'CACHE RIFIUTATA, ritento {slug[:50]}')
    try:
        rr=requests.get(u,headers=H,timeout=90)
        bad=rifiuto(rr.text) if rr.status_code==200 else f'HTTP {rr.status_code}'
    except Exception as e:
        bad=f'{type(e).__name__}'; rr=None
    if bad:
        blocchi+=1; consecutivi+=1; say(f'RIFIUTATA ({bad}) {slug[:50]}')
        if consecutivi>=5:
            say(f'FERMO dopo {consecutivi} rifiuti consecutivi: la fonte sta negando l\'accesso, non e\' il ritmo. {ok} recuperate, {blocchi} rifiutate.')
            break
    else:
        open(f,'w',encoding='utf-8').write(rr.text); ok+=1; consecutivi=0
        say(f'OK {slug[:50]}')
    time.sleep(90)
say(f'FINE {time.strftime("%H:%M:%S")}: {ok} recuperate, {blocchi} rifiutate')
sys.exit(1 if blocchi else 0)

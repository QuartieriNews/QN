# Ritmi e prezzi per il costo mensile (costi.py): prezzi degli attori letti dal listino via API (fascia del piano dell'account),
# post al giorno per pagina dalle esecuzioni di facebook-posts-scraper, eventi futuri per lettura da unseenuser/fb-events.
# Il token sta in un file fuori dal repository e non si stampa mai.
import json,re,datetime,collections,statistics,urllib.request
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
T=open(f'{S}/secrets/apify_org').read().strip()
def get(p):
    req=urllib.request.Request('https://api.apify.com/v2/'+p,headers={'Authorization':'Bearer '+T})
    return json.load(urllib.request.urlopen(req,timeout=300))
tier=get('users/me')['data']['plan']['tier']
for a in ('apify~facebook-posts-scraper','unseenuser~fb-events'):
    ev=get(f'acts/{a}')['data']['pricingInfos'][-1]['pricingPerEvent']['actorChargeEvents']
    print(a,tier,{k:v['eventTieredPricingUsd'][tier]['tieredEventPriceUsd'] for k,v in ev.items() if v.get('eventTieredPricingUsd')})
def key(u):
    m=re.search(r'facebook\.com/(?:profile\.php\?id=(\d+)|(?:pg/)?([^/?#]+))',str(u or ''),re.I)
    return (m.group(1) or m.group(2)).lower() if m else None
# post: ultime 20 esecuzioni, campi pagina e data soltanto
runs=[]
for r in get('acts/apify~facebook-posts-scraper/runs?desc=1&limit=20')['data']['items']:
    rd=get(f"actor-runs/{r['id']}")['data']; inp=get(f"key-value-stores/{rd['defaultKeyValueStoreId']}/records/INPUT")
    items=[]; off=0
    while True:
        b=get(f"datasets/{rd['defaultDatasetId']}/items?clean=true&format=json&fields=facebookUrl,inputUrl,time&limit=5000&offset={off}"); items+=b; off+=len(b)
        if len(b)<5000: break
    runs.append({'start':rd['startedAt'],'pages':[u.get('url') if isinstance(u,dict) else u for u in inp.get('startUrls') or []],'limit':inp.get('resultsLimit'),'newer':inp.get('onlyPostsNewerThan'),'items':items})
rate={}
for r in sorted(runs,key=lambda r:r['start']):   # l'esecuzione più recente vince
    end=datetime.datetime.fromisoformat(r['start'][:19]); win=(end-datetime.datetime.fromisoformat(r['newer'])).days
    by=collections.defaultdict(list)
    for it in r['items']:
        k=key(it.get('inputUrl') or it.get('facebookUrl'))
        if k and it.get('time'): by[k].append(datetime.datetime.fromisoformat(it['time'][:19]))
    for u in r['pages']:
        k=key(u)
        if not k: continue
        ts=sorted(by.get(k,[]))
        rate[k]=(len(ts)/max((end-ts[0]).total_seconds()/86400,1),'troncato',win) if len(ts)>=r['limit'] else (len(ts)/win,'completo',win)
v=[x[0] for x in rate.values()]
print('pagine',len(v),'media',round(statistics.mean(v),3),'mediana',round(statistics.median(v),3))
json.dump({k:list(x) for k,x in rate.items()},open(f'{S}/canali/apify/ritmo_post.json','w'))
# eventi: esecuzioni con almeno 100 pagine, esclusa quella interrotta con 2.515 eventi da 556 pagine
pag=ev=0
for r in get('acts/unseenuser~fb-events/runs?desc=1&limit=20')['data']['items']:
    rd=get(f"actor-runs/{r['id']}")['data']; inp=get(f"key-value-stores/{rd['defaultKeyValueStoreId']}/records/INPUT")
    n=(rd.get('chargedEventCounts') or {}).get('apify-default-dataset-item',0)
    if len(inp.get('pageUrls') or [])>=100 and n<2000: pag+=len(inp['pageUrls']); ev+=n
print('letture di pagine',pag,'eventi',ev,'per lettura',round(ev/pag,3))

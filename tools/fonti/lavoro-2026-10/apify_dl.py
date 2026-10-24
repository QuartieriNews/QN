# Scarica tutti gli item di un dataset Apify (paginato) in un file JSON. Uso: apify_dl.py <datasetId> <out> ; token da $S/secrets/apify_org
import json,sys,os,urllib.request
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T=open(f'{S}/secrets/apify_org').read().strip()
ds,out=sys.argv[1:3]; items=[]; off=0
while True:
    u=f'https://api.apify.com/v2/datasets/{ds}/items?clean=true&format=json&limit=1000&offset={off}'
    with urllib.request.urlopen(urllib.request.Request(u,headers={'Authorization':'Bearer '+T}),timeout=120) as r: page=json.loads(r.read().decode())
    items+=page
    if len(page)<1000: break
    off+=1000
json.dump(items,open(out,'w'),ensure_ascii=False); print(ds,len(items))

# Unisce pages.json con tutti i dataset del pages-scraper (assoc/pages_data/*.json) -> pages_enriched.json
import json,sys,re,glob
S=sys.argv[1]; pages=json.load(open(f'{S}/assoc/pages.json'))
def slug(u): return re.sub(r'^https?://(www\.|m\.)?facebook\.com/','',str(u or '')).strip('/').lower().split('?')[0]
by={}
for f in sorted(glob.glob(f'{S}/assoc/pages_data/*.json')):
    for it in json.load(open(f)):
        for k in ('url','facebookUrl','pageUrl','inputUrl'):
            if it.get(k): by.setdefault(slug(it[k]),it)
        if it.get('pageId'): by.setdefault(str(it['pageId']),it)
n=0
for p in pages:
    d=by.get(slug(p['url'])); p['dati']=d
    if d: n+=1
json.dump(pages,open(f'{S}/assoc/pages_enriched.json','w'),ensure_ascii=False)
print('pagine',len(pages),'con dati',n,'errore',sum(1 for p in pages if p.get('dati') and p['dati'].get('error')))

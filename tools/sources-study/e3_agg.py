import csv,re,json,collections,random,datetime as dt
from geo_lookup import localise,zones
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
MONTHS={m:i+1 for i,m in enumerate(['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])}
import sys
# e3_items.py scrive E3_all_text.tsv (gia' le sole voci trovate per giugno): qui si filtra per data
rows=[r for r in csv.DictReader(open('E3_all_text.tsv',encoding='utf-8'),delimiter='\t') if (r.get('date') or '').startswith('2026-06')]
if not rows: sys.exit('e3_agg: nessun item di giugno in E3_all_text.tsv: raccolta vuota o fallita')
n=len(rows); bym=collections.Counter(); multi=0; inter=0
for r in rows:
    ms=set(re.findall(r'Municipio ([IVX]+)',r['meta_municipio']))
    if 'ntermunicipale' in r['meta_municipio']: inter+=1
    if len(ms)>1: multi+=1
    for m in ms: bym[m]+=1
    r['muns']=';'.join(sorted(ms,key=lambda x:ROM.index(x))); r.update(localise(r['title']+' '+r['text'])); zt=zones(r['title']); r['zona_titolo']=next(iter(zt)) if len(zt)==1 else ''
res={'items_mese':n,'con_municipio_meta':sum(1 for r in rows if r['muns']),'quota_municipio_meta':round(100*sum(1 for r in rows if r['muns'])/n,1),'multi_municipio':multi,'intermunicipale':inter,'per_municipio_meta':{m:bym[m] for m in ROM},'quota_toponimo':round(100*sum(1 for r in rows if r['toponimo'])/n,1),'quota_zona_testo':round(100*sum(1 for r in rows if r['zona'])/n,1),'ambigui':sum(1 for r in rows if r['tier']=='ambiguous'),'con_periodo':sum(1 for r in rows if r['meta_periodo']),'strutture_top':dict(collections.Counter(r['meta_struttura'] for r in rows).most_common(8)),'tematiche_top':dict(collections.Counter(t for r in rows for t in r['meta_tematica'].split(';') if t).most_common(10)),'con_testo':sum(1 for r in rows if len(r['text'])>200)}
# future window from the whole listing (published since 26 May): parse meta_periodo of items since 1 July? we only have text for June items; for the window use listing pages 1..8 items? -> not fetched; mark as not measured here
json.dump(res,open('deliver/summary_E3.json','w'),ensure_ascii=False,indent=1); print(json.dumps(res,ensure_ascii=False))
with open('deliver/E3_2026-06_items.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fonte','url_rel','data_pubblicazione','municipi_meta','struttura','tematica','periodo','municipio_det_testo','zona_det_testo','zona_det_titolo','tier','toponimo'])
    for r in rows: w.writerow(['E3',r['url'].replace('https://www.comune.roma.it/web/it/',''),r['date'],r['muns'],r['meta_struttura'],r['meta_tematica'],r['meta_periodo'],r['municipio'],r['zona'],r['zona_titolo'],r['tier'],'sì' if r['toponimo'] else 'no'])
random.seed('2026-06-E3'); samp=random.sample(sorted(rows,key=lambda r:(r['date'],r['url'])),min(5,len(rows)))
with open('deliver/E3_audit_sample.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fonte','seed','url','data','municipi_meta','zona_det_testo']); [w.writerow(['E3','2026-06-E3',r['url'],r['date'],r['muns'],r['zona']]) for r in samp]
print('E3 AGG DONE')

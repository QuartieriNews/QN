import csv,re,json,collections,random,os,time,datetime as dt
from geo_lookup import localise,zones
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def mtime_rome(f): return time.strftime('%Y-%m-%d %H:%M',time.localtime(os.path.getmtime(f)+2*3600))
MONTHS={m:i+1 for i,m in enumerate(['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])}
items=list(csv.DictReader(open('A1_june_text.tsv'),delimiter='\t'))
news={}; ids={}
for r in items:
    (news if r['kind']=='news' else ids).setdefault(r['url'],r)
# municipi per item: from listing 'municipi' field (news) or mun_filter (ids)
def muns(r):
    if r['kind']=='news':
        s=set(re.findall(r'Municipio ([IVX]+)',r['municipi'])); 
        if 'Intermunicipale' in r['municipi'] or r['mun_filter']=='intermunicipale': s.add('INTER')
        return s
    return {r['mun_filter'].replace('municipio_','').upper()} if r['mun_filter']!='intermunicipale' else {'INTER'}
res={}
for kind,coll in (('news',news),('ids',ids)):
    n=len(coll); bym=collections.Counter()
    for r in coll.values():
        r.update(localise(r['title']+' '+r['text'])); ms=muns(r); r['muns']=';'.join(sorted(ms,key=lambda x: ROM.index(x) if x in ROM else 99))
        for m in ms: bym[m]+=1
        zt=zones(r['title']); r['zona_titolo']=next(iter(zt)) if len(zt)==1 else ''
    tem=collections.Counter(t for r in coll.values() for t in r['tematica'].split(';') if t)
    conv=sum(1 for r in coll.values() if re.search(r'convocazion',r['title'],re.I))
    res[kind]={'items_distinti_giugno':n,'per_municipio':{m:bym[m] for m in ROM},'intermunicipale':bym['INTER'],'multi_municipio':sum(1 for r in coll.values() if len(muns(r))>1),'quota_toponimo':round(100*sum(1 for r in coll.values() if r['toponimo'])/n,1) if n else None,'quota_zona_testo':round(100*sum(1 for r in coll.values() if r['zona'])/n,1) if n else None,'quota_zona_titolo':round(100*sum(1 for r in coll.values() if r['zona_titolo'])/n,1) if n else None,'ambigui_testo':sum(1 for r in coll.values() if r['tier']=='ambiguous'),'convocazioni':conv,'tematiche_top':dict(tem.most_common(12)),'con_testo':sum(1 for r in coll.values() if len(r['text'])>200)}
# per-Municipio totals A1 = news attributed + ids
res['per_municipio_totale']={m:res['news']['per_municipio'][m]+res['ids']['per_municipio'][m] for m in ROM}
res['lettura']=mtime_rome('A1_news.tsv'); res['listing']='https://www.comune.roma.it/web/it/notizie.page?mun=<municipio>&pagina=N ; https://www.comune.roma.it/web/it/informazioni-di-servizio.page?mun=<municipio>&pagina=N'; res['paginazione_completa']='sì (ogni filtro percorso fino alla prima pagina con data < 2026-06-01)'
# --- A1 (IDS convocazioni) x A2 (CMC/MMC) match: same Municipio + seduta date + organ ---
import html as _h
sed={}
for t in ('CMC','MMC'):
    for f in ([f'A2_jun_{t}.json']+(['A2_jun_MMC_2.json'] if t=='MMC' else [])):
        for x in json.load(open(f))['elencoAtti']:
            s=_h.unescape(re.sub(r'<[^>]+>',' ',(x.get('dtRpr') or '')+' '+(x.get('dscStrOrg') or '')))
            m=re.search(r'\((\d{2})/(\d{2})/(\d{4})\)',s) or re.search(r'Seduta del (\d{2})/(\d{2})/(\d{4})',s)
            sed[x['idDoc']]=(t,f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else '')
a2=[r for r in csv.DictReader(open('A2_rows_final.tsv'),delimiter='\t') if r['tipologia'] in ('CMC','MMC')]
idx=collections.defaultdict(list)
for r in a2:
    t,d=sed.get(r['idDoc'],(r['tipologia'],'')); idx[(r['mun_final'],d,t)].append(r)
matched=0; dubbi=0; unmatched=0; pairs=[]; kinds=collections.Counter()
for r in ids.values():
    if not re.search(r'convocazion',r['title'],re.I): continue
    m=re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})',r['title']); d=f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}" if m and m.group(2).lower() in MONTHS else ''
    mun=r['mun_filter'].replace('municipio_','').upper()
    if re.search(r'giunta',r['title'],re.I): kinds['giunta']+=1; r['ragione']='convocazione di Giunta: tipologia non presente in Atti Web'; unmatched+=1; continue
    kind='CMC' if re.search(r'consiglio',r['title'],re.I) else 'MMC'; kinds[kind]+=1
    c=idx.get((mun,d,kind),[])
    if c: matched+=1; r['gemello']=c[0]['url']; r['ragione']=f'stessa seduta {d}, Municipio {mun}, {"Consiglio" if kind=="CMC" else "Commissione"}: avviso A1 / atto A2 {kind}'; pairs.append((r['url'],c[0]['url'],r['ragione']))
    elif not d: dubbi+=1; r['ragione']="dubbio: data della seduta non nel titolo dell'avviso"
    else:
        other=idx.get((mun,d,'MMC' if kind=='CMC' else 'CMC'),[])
        if other: dubbi+=1; r['gemello']=other[0]['url']; r['ragione']=f'dubbio: stessa data {d} e Municipio {mun}, organo diverso in A2'
        else: unmatched+=1; r['ragione']=f'nessun atto A2 con seduta {d} per il Municipio {mun}'
res['convocazioni_A1_ids_vs_A2']={'ids_convocazioni_giugno':sum(1 for r in ids.values() if re.search(r'convocazion',r['title'],re.I)),'per_organo':dict(kinds),'gemello_certo_in_A2':matched,'dubbi':dubbi,'senza_gemello':unmatched}
json.dump(res,open('deliver/summary_A1.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in res.items() if k not in ('listing',)},ensure_ascii=False)[:3000])
with open('deliver/A1_2026-06_items.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fonte','tipo','url','data_pubblicazione','municipi','tematica','municipio_det_testo','zona_det_testo','zona_det_titolo','tier','toponimo','formato','gemello','ragione'])
    for kind,coll in (('news',news),('ids',ids)):
        for r in coll.values(): w.writerow(['A1',kind,r['url'],r['date'],r['muns'],r['tematica'],r['municipio'],r['zona'],r['zona_titolo'],r['tier'],'sì' if r['toponimo'] else 'no','HTML',r.get('gemello',''),r.get('ragione','')])
random.seed('2026-06-A1'); allr=list(news.values())+list(ids.values()); samp=random.sample(allr,5)
with open('deliver/A1_audit_sample.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['fonte','seed','tipo','url','data','municipi','zona_det_testo']); [w.writerow(['A1','2026-06-A1',r['kind'],r['url'],r['date'],r['muns'],r['zona']]) for r in samp]
with open('deliver/A1_A2_convocazioni_pairs.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['A1_url','A2_url','ragione']); w.writerows(pairs)
print('A1 AGG DONE')

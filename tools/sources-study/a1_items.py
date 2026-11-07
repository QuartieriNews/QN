import csv,re,html,os,time,requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s))).strip()
os.makedirs('A1_items',exist_ok=True)
news={}; 
for r in csv.DictReader(open('A1_news.tsv'),delimiter='\t'):
    if r['date'].startswith('2026-06'): news.setdefault(r['url'],r)
ids={}
for r in csv.DictReader(open('A1_ids.tsv'),delimiter='\t'):
    if r['date'].startswith('2026-06'): ids.setdefault(r['url'],r)
falliti=[]
log=open('a1_items.log','a'); print('news',len(news),'ids',len(ids),file=log,flush=True)
out=csv.writer(open('A1_june_text.tsv','w',newline=''),delimiter='\t'); out.writerow(['kind','url','date','title','tematica','municipi','mun_filter','text','estrattore','meta_municipio'])
for kind,coll in (('news',news),('ids',ids)):
    for k,(u,r) in enumerate(coll.items()):
        f='A1_items/'+re.sub(r'[^A-Za-z0-9]+','_',u.split('/web/it/')[-1])[:120]+'.html'
        d=''
        if os.path.exists(f) and os.path.getsize(f)>0: d=open(f,encoding='utf-8',errors='replace').read()
        else:
            for t in range(3):
                try:
                    rr=requests.get(u,headers=H,timeout=90)
                    if rr.status_code==200: d=rr.text; open(f,'w',encoding='utf-8').write(d); break
                except Exception: time.sleep(3)
            if not d: falliti.append(u); print('FETCH FAILED',u,file=log,flush=True)   # non e' un item vuoto: e' un fetch mancato
        # pagine servite senza charset: requests le decodifica come ISO-8859-1 -> ripara il mojibake
        if 'Ã' in d and 'charset' not in d[:2000].lower():
            try: d=d.encode('latin-1').decode('utf-8')
            except (UnicodeEncodeError,UnicodeDecodeError): pass
        ma=re.search(r'<article>(.*?)</article>',d,flags=re.S)
        if ma: seg=ma.group(1)   # informazioni di servizio: corpo dentro <article>
        else:
            mh=re.search(r'<h2 class="u-text-h2[^"]*">',d)   # notizie: dal titolo h2 in poi
            seg=d[mh.start():] if mh else d
            ends=[p for p in (seg.find(mk) for mk in ('Progetti in evidenza','class="Share','Condividi','<footer')) if p>0]
            seg=seg[:min(ends)] if ends else seg
        t=clean(re.sub(r'<script.*?</script>|<style.*?</style>','',seg,flags=re.S))[:15000]
        tem=r.get('tematica','')
        if not tem:
            mt=re.search(r'<meta name="search:tematica" content="([^"]*)"',d); tem=html.unescape(mt.group(1)).replace('§',';') if mt else ''
        mm=re.search(r'<meta name="search:municipio" content="([^"]*)"',d); meta_mun=html.unescape(mm.group(1)) if mm else ''
        out.writerow([kind,u,r['date'],r['title'],tem,r.get('municipi','') or meta_mun,r['mun_filter'],t,'article' if ma else 'h2','sì' if mm else 'no'])
        if (k+1)%25==0: print(kind,k+1,file=log,flush=True)
print('DONE',file=log,flush=True)
if falliti:
    print(f'DONE WITH {len(falliti)} FETCH FAILURES: censimento incompleto',file=log,flush=True)
    import sys; sys.exit(1)

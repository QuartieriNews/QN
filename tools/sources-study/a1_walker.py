import re,html,csv,time,os,sys,requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
MONTHS={m:i+1 for i,m in enumerate(['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])}
def iso(s):
    m=re.match(r'(\d{1,2}) (\w+) (\d{4})',s.strip()); return f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}" if m and m.group(2) in MONTHS else ''
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s))).strip()
def get(url):
    for t in range(3):
        try:
            r=requests.get(url,headers=H,timeout=90)
            if r.status_code==200: return r.text
        except Exception as e: pass
        time.sleep(3)
    return ''
MUNS=['municipio_'+x for x in ['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv']]+['intermunicipale']
STOP='2026-06-01'
os.makedirs('A1_pages',exist_ok=True)
news=csv.writer(open('A1_news.tsv','w',newline=''),delimiter='\t'); news.writerow(['mun_filter','page','date','title','url','tematica','municipi'])
ids=csv.writer(open('A1_ids.tsv','w',newline=''),delimiter='\t'); ids.writerow(['mun_filter','page','date','title','url'])
log=open('a1_walker.log','a')
for mun in MUNS:
    # news
    for p in range(1,200):
        url=f'https://www.comune.roma.it/web/it/notizie.page?mun={mun}&pagina={p}'; d=get(url); open(f'A1_pages/news_{mun}_{p}.html','w').write(d)
        items=re.findall(r'<div class="Grid-cell List-content">\s*<p class="List-category">(.*?)</p>\s*<p class="List-date">(.*?)</p>\s*<p class="List-title">\s*<a href="([^"]+)">(.*?)</a>',d,flags=re.S)
        if not items: print(mun,'news page',p,'no items -> stop',file=log,flush=True); break
        dates=[]
        for cat,dt,u,t in items:
            di=iso(clean(dt)); dates.append(di)
            tem=';'.join(clean(x) for x in re.findall(r'temat=[^"]+">(.*?)</a>',cat)); mm=';'.join(clean(x) for x in re.findall(r'mun=[^"]+">(.*?)</a>',cat))
            news.writerow([mun,p,di,clean(t),'https://www.comune.roma.it'+u,tem,mm])
        print(mun,'news p',p,len(items),min(dates),max(dates),file=log,flush=True)
        if min(dates)<STOP: break
    # informazioni di servizio
    for p in range(1,200):
        url=f'https://www.comune.roma.it/web/it/informazioni-di-servizio.page?mun={mun}&pagina={p}'; d=get(url); open(f'A1_pages/ids_{mun}_{p}.html','w').write(d)
        items=re.findall(r'<p class="List-date">(.*?)</p>\s*<p class="List-title">\s*<a href="([^"]*informazione-di-servizio\.page\?contentId=[^"]+)">(.*?)</a>',d,flags=re.S)
        if not items:
            items=[(dt,u,t) for dt,u,t in re.findall(r'(\d{1,2} \w+ \d{4})</[^>]+>\s*(?:<[^>]+>\s*)*<a href="([^"]*informazione-di-servizio\.page\?contentId=[^"]+)"[^>]*>(.*?)</a>',d,flags=re.S)]
        if not items: print(mun,'ids page',p,'no items -> stop',file=log,flush=True); break
        dates=[]
        for dt,u,t in items:
            di=iso(clean(dt)); dates.append(di); ids.writerow([mun,p,di,clean(t),'https://www.comune.roma.it'+u if u.startswith('/') else u])
        print(mun,'ids p',p,len(items),min(dates),max(dates),file=log,flush=True)
        if min(dates)<STOP: break
print('DONE',file=log,flush=True)

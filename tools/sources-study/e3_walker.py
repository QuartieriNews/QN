import re,html,os,time,csv,requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
MONTHS={m:i+1 for i,m in enumerate(['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])}
def iso(s):
    m=re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})',s)
    return f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}" if m and m.group(2).lower() in MONTHS else ''
os.makedirs('E3_pages',exist_ok=True)
log=open('e3_walker.log','a'); rows=[]; stop=False
for p in range(1,160):
    f=f'E3_pages/p{p}.html'
    if os.path.exists(f) and os.path.getsize(f)>0: d=open(f,encoding='utf-8',errors='replace').read()
    else:
        d=''
        for t in range(3):
            try:
                r=requests.get('https://www.comune.roma.it/web/it/eventi.page',params={'pagina':p},headers=H,timeout=90)
                if r.status_code==200 and 'List-title' in r.text: d=r.text; open(f,'w',encoding='utf-8').write(d); break
            except Exception: pass
            time.sleep(3)
    items=re.findall(r'<div class="Grid-cell List-content">\s*<p class="List-category">(.*?)</p>\s*<p class="List-date">([^<]*)</p>\s*<p class="List-title">\s*<a href="([^"]*)">(.*?)</a>',d,flags=re.S)
    if not items: print('page',p,'NO ITEMS',file=log,flush=True); break
    dates=[]
    for cat,dt,href,title in items:
        di=iso(dt); dates.append(di)
        tem=';'.join(html.unescape(x.strip()) for x in re.findall(r'>([^<]+)</a>',cat))
        rows.append({'page':p,'date':di,'title':html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',title))).strip(),'url':'https://www.comune.roma.it'+href,'tematica':tem})
    print('page',p,len(items),min(dates),max(dates),file=log,flush=True)
    if min(dates)<'2026-06-01': break
    time.sleep(0.7)
with open('E3_listing.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['page','date','title','url','tematica'],delimiter='\t'); w.writeheader(); w.writerows(rows)
print('DONE',len(rows),file=log,flush=True)

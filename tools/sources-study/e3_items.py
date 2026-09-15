import csv,re,html,os,time,requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s))).strip()
os.makedirs('E3_items',exist_ok=True)
rows={}
for r in csv.DictReader(open('E3_listing.tsv'),delimiter='\t'):
    rows.setdefault(r['url'],r)
log=open('e3_items.log','a'); print('june items',len(rows),file=log,flush=True)
out=csv.writer(open('E3_all_text.tsv','w',newline=''),delimiter='\t'); out.writerow(['url','date','title','tematica','meta_municipio','meta_periodo','meta_data','meta_struttura','meta_tematica','text'])
for k,(u,r) in enumerate(rows.items()):
    f='E3_items/'+re.sub(r'[^A-Za-z0-9]+','_',u.split('/web/it/')[-1])[:120]+'.html'; d=''
    if os.path.exists(f) and os.path.getsize(f)>0: d=open(f,encoding='utf-8',errors='replace').read()
    else:
        for t in range(3):
            try:
                rr=requests.get(u,headers=H,timeout=90)
                if rr.status_code==200: d=rr.text; open(f,'w',encoding='utf-8').write(d); break
            except Exception: time.sleep(3)
    if 'Ã' in d and 'charset' not in d[:2000].lower():
        try: d=d.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError,UnicodeDecodeError): pass
    def meta(n):
        m=re.search(r'<meta name="search:'+n+r'" content="([^"]*)"',d); return html.unescape(m.group(1)) if m else ''
    ma=re.search(r'<article>(.*?)</article>',d,flags=re.S)
    if ma: seg=ma.group(1)
    else:
        mh=re.search(r'<h2 class="u-text-h2[^"]*">',d) or re.search(r'<div class="Grid-cell u-sizeFull u-md-size3of4[^"]*"><h2>',d)
        seg=d[mh.start():] if mh else d
        ends=[p for p in (seg.find(mk) for mk in ('Progetti in evidenza','class="Share','Condividi','<footer')) if p>0]
        seg=seg[:min(ends)] if ends else seg
    t=clean(re.sub(r'<script.*?</script>|<style.*?</style>','',seg,flags=re.S))[:6000]
    out.writerow([u,r['date'],r['title'],r['tematica'],meta('municipio'),meta('periodo'),meta('data'),meta('struttura'),meta('tematica').replace('§',';'),t])
    if (k+1)%25==0: print(k+1,file=log,flush=True)
print('DONE',file=log,flush=True)

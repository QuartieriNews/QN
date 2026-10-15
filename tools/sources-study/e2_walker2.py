import json,re,html,csv,time,sys,os,requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
items=[]
for p in range(1,11): items+=json.load(open(f'E2_rec_p{p}.json'))
def grab(pat,s,flags=re.S):
    m=re.search(pat,s,flags); return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',m.group(1)))).strip() if m else ''
out=open('E2_recent_events.tsv','w',newline=''); w=csv.writer(out,delimiter='\t')
w.writerow(['id','published','link','title','municipio_terms','dates','orario','luogo','indirizzo','municipio_page','manifestazione','gratuito','http'])
os.makedirs('E2_items_recent',exist_ok=True)
falliti=0
for k,it in enumerate(items):
    f=f"E2_items_recent/{it['id']}.html"
    try:
        if os.path.exists(f) and os.path.getsize(f)>0: d=open(f,encoding='utf-8',errors='replace').read(); code=200
        else:
            r=requests.get(it['link'],headers=H,timeout=60); code=r.status_code; d=r.text; open(f,'w',encoding='utf-8').write(d)
    except Exception as e:
        w.writerow([it['id'],it['date'],it['link'],it['title']['rendered'],'|'.join(map(str,it.get('municipio') or [])),'','','','','','','',f'ERR {e}']); out.flush(); falliti+=1; continue
    if code!=200: falliti+=1   # risposta non 200: item mancante, non vuoto
    dates=grab(r'class=dates>(.*?)</span>',d); orario=grab(r'class=page_orario>(.*?)</span>',d)
    luogo=grab(r'class=luogo_title>(.*?)</span>',d); ind=grab(r'class=location>(.*?)</span>',d)
    mun=grab(r'class=municipio_title>(.*?)</span>',d); man=grab(r'class=page_manifestazione>(.*?)</p>',d)
    grat='sì' if re.search(r'class="etichetta gratuito"',d) else ''
    w.writerow([it['id'],it['date'],it['link'],html.unescape(it['title']['rendered']),'|'.join(map(str,it.get('municipio') or [])),dates,orario,luogo,ind,mun,man,grat,code]); out.flush()
    if (k+1)%50==0: print(k+1,'done',time.strftime('%H:%M:%S'),flush=True)
print('DONE',len(items),'falliti',falliti)
sys.exit(1 if falliti else 0)

import json,sys,re,time,html,urllib.request,hashlib,os
S=sys.argv[1]; urls=json.load(open(f'{S}/culture/venue_urls.json')); out={}
UA='Mozilla/5.0 QuartieriNews-eventi/1.0 (+contatto: redazione)'
for i,u in enumerate(urls):
    f=f'{S}/culture/luoghi/{hashlib.md5(u.encode()).hexdigest()}.html'
    try:
        if os.path.exists(f): d=open(f,encoding='utf-8',errors='replace').read()
        else:
            with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40) as r: d=r.read().decode('utf-8','replace')
            open(f,'w',encoding='utf-8').write(d); time.sleep(1.0)
        m=re.search(r'LatLng\((4[12]\.\d+),\s*(1[12]\.\d+)\)',d); a=re.search(r'class="location"[^>]*>(.*?)<',d,re.S) or re.search(r'<p class="page_map"[^>]*>(.*?)</p>',d,re.S)
        t=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',d)))
        addr=re.search(r'\b((?:Via|Viale|Piazza|Piazzale|Largo|Corso|Lungotevere|Vicolo|Borgo|Circonvallazione)\s[^.;)]{3,60}?,\s*\d+[A-Za-z/]*)',t)
        tt=re.search(r'<title>(.*?)</title>',d,re.S)
        out[u]={'lat':float(m.group(1)) if m else None,'lon':float(m.group(2)) if m else None,'indirizzo':addr.group(1) if addr else None,'titolo':html.unescape(tt.group(1)).replace(' - Culture','').strip() if tt else None}
    except Exception as e: out[u]={'errore':str(e)[:80]}
    if i%20==0: print(i,u,out[u],flush=True)
json.dump(out,open(f'{S}/culture/luoghi.json','w'),ensure_ascii=False,indent=1); print('DONE',sum(1 for v in out.values() if v.get('lat')),'/',len(out))

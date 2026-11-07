# RomaTV (tenant ac104) census of June 2026: pages each catalogue by reference date until before 20 May 2026.
import json, os, time, datetime as dt, csv, re, requests
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
B='https://api-ovp.streamcloud.it/garavot/ac104/api/v1/contents/search_frontend'
H={'Accept':'application/json','Content-Type':'application/json','Origin':'https://streaming.comune.roma.it','Referer':'https://streaming.comune.roma.it/'}
CATS=['Municipio I','Municipio II','Municipio III','Municipio IV','Municipio V','Municipio VI','Municipio VII','Municipio VIII','Municipio IX','Municipio X','Municipio XI','Municipio XII','Municipio XIII','Municipio XIV','Municipio XV','Commissioni Capitoline','Assemblee Capitoline']
os.makedirs('rtv/cat',exist_ok=True)
summary={}; nreq=0
incompleti=[]
for cat in CATS:
    page=1; items=[]; total=None
    while True:
        body={"page":page,"pageSize":100,"filters":{"discriminator":None,"catalog":[cat]},"sortBy":[{"sortField":"ReferenceDate","direction":"Descending"}],"includeAggregations":False}
        r=None
        for tentativo in range(3):   # errori transitori (HTTP o rete): tre tentativi con attesa crescente
            try:
                r=requests.post(B,json=body,headers=H,timeout=180); nreq+=1
                if r.status_code==200: break
                print(cat,'HTTP',r.status_code,r.text[:200])
            except requests.RequestException as e:
                r=None; print(cat,'RETE',type(e).__name__)
            time.sleep(5*(tentativo+1))
        if r is None or r.status_code!=200:
            print(cat,'-> catalogo incompleto'); incompleti.append(cat); break
        d=r.json()['data']
        if total is None: total=d.get('totalCount')
        its=d.get('items') or []
        items+=its
        dates=[it.get('referenceDate') for it in its if it.get('referenceDate')]
        if not its or not d.get('hasNext') or (dates and min(dates)[:10]<'2026-05-20') or page>=40: break
        page+=1; time.sleep(0.3)
    json.dump(items,open(f'rtv/cat/{cat.replace(" ","_")}.json','w'),ensure_ascii=False)
    june=[it for it in items if (it.get('referenceDate') or '')[:7]=='2026-06']
    pub_june=[it for it in items if (it.get('insertDate') or '')[:7]=='2026-06']
    summary[cat]={'totale_catalogo':total,'letti':len(items),'pagine':page,'giugno_per_data_seduta':len(june),'giugno_per_data_pubblicazione':len(pub_june),'con_speech_to_text':sum(1 for it in june if 'SpeechToTextTrack' in (it.get('trackTypes') or []))}
    print(cat, summary[cat], flush=True)
print('requests', nreq)
json.dump(summary,open('rtv/census_summary.json','w'),ensure_ascii=False,indent=1)
if incompleti:
    print('CATALOGHI INCOMPLETI:',incompleti); import sys; sys.exit(1)

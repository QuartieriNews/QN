import time
import json,re,html,os,random,csv,requests,fitz
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
B='https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/'
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s or ''))).strip()
def load(c):
    if c=='DDS':
        a=[]; 
        for fr in (0,500): a+=json.load(open(f'A2_tip/DDS_full_{fr}.json'))['elencoAtti']
        return a
    return json.load(open(f'A2_tip/{c}.json')).get('elencoAtti') or []
def key(a): 
    d=clean(a.get('dtRpr'))[:10]; return (d[6:10]+d[3:5]+d[0:2], a.get('urlFile') or '')
os.makedirs('A2_deep',exist_ok=True)
picks=[]
# DDS 10
dds=sorted(load('DDS'),key=key); random.seed('2026-06-DDS'); picks+=[('DDS',a) for a in random.sample(dds,10)]
# central candidates: territorial in object or proposed by a Municipio structure
from geo_lookup import localise
cand=[]
for c in ('GCD','AY','AZ','ACD','GCM'):
    for a in load(c):
        L=localise(clean(a.get('oggetto'))); org=clean(a.get('dscStrOrg'))
        if L['municipio'] or L['zona'] or 'MUNICIPIO' in org.upper(): cand.append((c,a,L,org))
print('candidati centrali',len(cand),{c:sum(1 for x in cand if x[0]==c) for c in ('GCD','AY','AZ','ACD','GCM')})
cs=sorted(cand,key=lambda x:(x[0],)+key(x[1])); random.seed('2026-06-centrali'); picks+=[(c,a) for c,a,L,org in random.sample(cs,5)]
for c in ('CPC','CPV'):
    lst=sorted(load(c),key=key); random.seed('2026-06-'+c); picks+=[(c,a) for a in random.sample(lst,5)]
# SO: the 2 with territory + 1 seeded; CID 1; MCD 1; OCD 1
so=load('SO'); so_t=[a for a in so if localise(clean(a.get('oggetto')))['municipio'] or localise(clean(a.get('oggetto')))['zona']]
random.seed('2026-06-SO'); picks+=[('SO',a) for a in so_t]+[('SO',random.choice([a for a in so if a not in so_t]))]
random.seed('2026-06-CID'); picks+=[('CID',random.choice(load('CID')))]
picks+=[('MCD',load('MCD')[0]),('OCD',load('OCD')[0])]
rows=[]
for i,(c,a) in enumerate(picks):
    u=B+(a.get('urlFile') or ''); f=f'A2_deep/{i:02d}_{c}.pdf'
    if not os.path.exists(f):
        try:
            time.sleep(1.3)   # Atti Web: una richiesta ogni 1,3 s (HANDOFF §2)
            r=requests.get(u,headers=H,timeout=120); open(f,'wb').write(r.content)
        except Exception as e: print('DL ERR',c,e); continue
    try:
        doc=fitz.open(f); pages=doc.page_count; txt='\n'.join(p.get_text() for p in doc); doc.close()
    except Exception as e: pages=0; txt=''; print('PDF ERR',c,f,str(e)[:80])
    open(f.replace('.pdf','.txt'),'w').write(txt)
    verdict='TESTO' if len(txt.strip())>200 else 'SCANSIONE'
    rows.append({'i':i,'tip':c,'url':u,'data':clean(a.get('dtRpr'))[:10],'struttura':clean(a.get('dscStrOrg'))[:70],'oggetto':clean(a.get('oggetto'))[:220],'pagine':pages,'caratteri':len(txt.strip()),'esito':verdict,'size':os.path.getsize(f)})
    print(i,c,verdict,pages,len(txt.strip()),os.path.getsize(f),'|',rows[-1]['struttura'][:40],'|',rows[-1]['oggetto'][:90],flush=True)
json.dump(rows,open('A2_deep/pdf_rows.json','w'),ensure_ascii=False,indent=1)
print('TOTAL PDF',len(rows),'testo',sum(1 for r in rows if r['esito']=='TESTO'))

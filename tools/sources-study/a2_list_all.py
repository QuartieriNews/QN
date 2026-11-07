# Builds A2_all/_list.tsv (name, url, formato, data) for all June acts (A2 municipal, DDS, central), weeks 8–28 first.
import csv, re, os, datetime
S=os.environ['QN_NET']; os.makedirs(S+'/A2_all',exist_ok=True)
def par2(u):
    m=re.search(r'par2=([^&]+)',u); return m.group(1) if m else None
def wkr(d):
    try: dt=datetime.datetime.strptime(d[:10],'%d/%m/%Y').date()
    except Exception: return None
    return 2 if 8<=dt.day<=14 else 3 if 15<=dt.day<=21 else 4 if 22<=dt.day<=28 else None
items=[]
for fn,kind in (('A2_2026-06_items.csv','A2'),('A2_DDS_2026-06_items.csv','DDS'),('A2_centrali_2026-06_items.csv','CEN')):
    for r in csv.DictReader(open(f'{S}/deliver/{fn}',encoding='utf-8')):
        mun=(r.get('municipio') or r.get('municipio_gruppo_PL') or r.get('municipio_det_oggetto') or 'X').replace('/','-')[:12]
        items.append((0 if wkr(r['data_repertorio']) else 1, r['data_repertorio'], kind, r['tipologia'], mun, r['url'], r.get('formato','')))
items.sort(); n=0
with open(S+'/A2_all/_list.tsv','w') as f:
    for p,d,kind,tip,mun,u,fmt in items:
        pid=par2(u)
        if not pid: continue
        f.write(f"{kind}_{tip}_{mun}_{re.sub(r'[^A-Za-z0-9]','',pid)}\t{u}\t{fmt}\t{d}\n"); n+=1
print(n,'atti in elenco, settimane 8-28 prima:',sum(1 for i in items if i[0]==0))

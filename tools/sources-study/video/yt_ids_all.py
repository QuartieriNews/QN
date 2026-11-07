# Builds video/all_ids.txt: June YouTube videos without a caption file yet, weeks 8–28 first.
import csv, os, datetime
S=os.environ['QN_NET']
def wk(d):
    try: dt=datetime.date.fromisoformat(d[:10])
    except Exception: return None
    return 2 if 8<=dt.day<=14 else 3 if 15<=dt.day<=21 else 4 if 22<=dt.day<=28 else None
ids=[]
for r in csv.DictReader(open(S+'/video/deliver_video/A4_youtube_giugno2026_censimento.csv',encoding='utf-8')):
    if os.path.exists(f"{S}/video/caps/{r['id']}.it.json3"): continue
    if r.get('live','').strip().lower() in ('sì','si','true','1'): continue
    ids.append((0 if wk(r['data_seduta']) else 1, r['data_seduta'], r['id']))
ids.sort(); open(S+'/video/all_ids.txt','w').write('\n'.join(i for _,_,i in ids)+'\n'); print(len(ids),'video da recuperare')

# Builds video/rtv/audio/_list_w2w4.tsv (AudioOnly smil URL, guid8, week, date, territory, hours) for the
# RomaTV commission recordings of 8–28 June 2026 without a platform transcript (feasibility note §9.6).
import json, glob, csv, datetime, os
S=os.environ['QN_NET']; smil={}
for f in glob.glob(S+'/video/rtv/cat/*.json'):
    for it in json.load(open(f)):
        for sf in (it.get('smilFiles') or []):
            if sf.get('smilFileType')=='AudioOnly' and it.get('guid'): smil[it['guid']]=sf['url']
def wk(d):
    try: dt=datetime.date.fromisoformat(d[:10])
    except Exception: return None
    if (dt.year,dt.month)!=(2026,6): return None
    return 2 if 8<=dt.day<=14 else 3 if 15<=dt.day<=21 else 4 if 22<=dt.day<=28 else None
rows=[]
for r in csv.DictReader(open(S+'/video/deliver_video/A3_romatv_giugno2026_censimento.csv',encoding='utf-8')):
    w=wk(r['data_seduta']); org=r['organo']+' '+r['tipo']
    if not w or 'onsigli' in org or 'ssemble' in org: continue
    if r['trascrizione_piattaforma'].strip().lower() in ('sì','si','yes','true','1'): continue
    u=smil.get(r['guid'])
    if u: rows.append((w,r['data_seduta'],u,r['guid'][:8],r['territorio'],round(int(r['durata_s'] or 0)/3600,2)))
rows.sort(); os.makedirs(S+'/video/rtv/audio',exist_ok=True)
with open(S+'/video/rtv/audio/_list_w2w4.tsv','w') as f:
    for w,d,u,g8,t,h in rows: f.write(f'{u}\t{g8}\t{w}\t{d}\t{t}\t{h}\n')
print(len(rows),'registrazioni,',round(sum(r[5] for r in rows),1),'ore')

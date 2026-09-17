# Stratified sample of Report 1 candidate news for the Codex control C2 (method §4.3): fixed seed,
# quotas by source and by deduplication outcome, so the sample cannot be picked to look good.
import csv, os, random, collections
S=os.environ['QN_NET']; R=S+'/report1'
rows=list(csv.DictReader(open(R+'/db/notizie_candidate.csv',encoding='utf-8')))
rnd=random.Random('2026-06-C2')
# Quotas: at least 5 per source and one per deduplication outcome, then filled to 40 at random.
per_fonte=collections.defaultdict(list); per_stato=collections.defaultdict(list)
for r in rows:
    per_fonte[r['fonte']].append(r); per_stato[r['dedup_stato']].append(r)
scelte={}
for fonte,rs in sorted(per_fonte.items()):
    for r in rnd.sample(rs, min(5, len(rs))): scelte[r['id']]=r
for stato,rs in sorted(per_stato.items()):
    for r in rnd.sample(rs, min(5, len(rs))): scelte[r['id']]=r
resto=[r for r in rows if r['id'] not in scelte]
for r in rnd.sample(resto, max(0, 40-len(scelte))): scelte[r['id']]=r
camp=[scelte[k] for k in sorted(scelte)]
campi=['id','fonte','documento_id','titolo','sintesi','tipo','luoghi','municipio','municipio_testo','zona','tier_localizzazione','toponimo_da_verificare','evidenza_url','evidenza_locale','data_fatto','data_pubblicazione','qualita','dedup_stato','gemello_id','ragione_dedup','note']
with open(R+'/db/campione_c2.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=campi,extrasaction='ignore'); w.writeheader(); w.writerows(camp)
print(len(camp),'notizie nel campione, seed 2026-06-C2')
print('per fonte:',dict(collections.Counter(r['fonte'] for r in camp)))
print('per esito dedup:',dict(collections.Counter(r['dedup_stato'] for r in camp)))

import json, glob, re, datetime as dt, csv, sys
MESI={'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12,
      'gen':1,'feb':2,'mar':3,'apr':4,'mag':5,'giu':6,'lug':7,'ago':8,'set':9,'sett':9,'ott':10,'nov':11,'dic':12}
def title_date(t):
    s=t.lower()
    m=re.search(r'(\d{1,2})[\s\.\-/]+(\d{1,2})[\s\.\-/]+(20\d{2}|\d{2})\b', s)
    if m:
        d,mo,y=int(m.group(1)),int(m.group(2)),int(m.group(3)); y = y+2000 if y<100 else y
        try: return dt.date(y,mo,d).isoformat(), 'numeric'
        except: pass
    for m in re.finditer(r'(\d{1,2})[°ºo]?\s*(?:di\s+)?([a-z]{3,9})\.?\s*(20\d{2})?', s):
        if m.group(2) in MESI:
            d=int(m.group(1)); mo=MESI[m.group(2)]; y=int(m.group(3)) if m.group(3) else None
            try:
                if y: return dt.date(y,mo,d).isoformat(), 'text'
                return f'????-{mo:02d}-{d:02d}', 'text_noyear'
            except: pass
    m=re.search(r'\b([a-z]{3,9})\s+(20\d{2})\b', s)
    if m and m.group(1) in MESI:
        return f'{m.group(2)}-{MESI[m.group(1)]:02d}-??', 'month'
    return '', ''
rows=[]; stats={}
for f in sorted(glob.glob('yt_flat_*_*.json')):
    m=re.match(r'yt_flat_(\w+)_(videos|streams)\.json', f); ch,tab=m.group(1),m.group(2)
    try: d=json.load(open(f))
    except Exception as e: stats[(ch,tab)]=('ERR',str(e)[:40]); continue
    if not d: stats[(ch,tab)]=("EMPTY",0); continue
    ents=d.get("entries") or []
    stats[(ch,tab)]=(d.get('channel'), len(ents))
    for e in ents:
        ts=e.get('timestamp'); ad=dt.datetime.utcfromtimestamp(ts).date().isoformat() if ts else ''
        td,kind=title_date(e.get('title') or '')
        rows.append(dict(ch=ch,tab=tab,channel=d.get('channel'),id=e['id'],title=e.get('title'),duration=e.get('duration'),approx_date=ad,title_date=td,title_date_kind=kind,live_status=e.get('live_status'),views=e.get('view_count')))
for k,v in stats.items(): print(k,v)
print('total rows', len(rows))
def is_june(r):
    if r['title_date'].startswith('2026-06'): return 'title'
    if r['title_date'].startswith('????-06') and r['approx_date'][:7] in ('2026-05','2026-06','2026-07'): return 'title_noyear'
    if not r['title_date'] and r['approx_date'][:7]=='2026-06': return 'approx'
    if r['approx_date'][:7]=='2026-06' and r['title_date'] and not r['title_date'].startswith('2026-06') and not r['title_date'].startswith('????'): return 'approx_only_titlediff'
    return ''
june=[]
for r in rows:
    j=is_june(r)
    if j: r['june_basis']=j; june.append(r)
# oldest approx date per channel to see coverage
cov={}
for r in rows:
    if r['approx_date']:
        k=(r['ch'],r['tab']); cov[k]=min(cov.get(k,'9999'), r['approx_date'])
print('oldest approx date per channel/tab:', cov)
from collections import Counter
print('june rows', len(june), Counter((r['ch'],r['june_basis']) for r in june))
if not rows: sys.exit('yt_parse_flat: nessuna riga nei dump yt_flat_*: vuoti o non validi (blocco anti-bot?)')
with open('yt_all_rows.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())+['june_basis'], delimiter='\t'); w.writeheader()
    for r in rows: w.writerow(r)
if not june: sys.exit('yt_parse_flat: nessun video di giugno nei dump: niente da scrivere')
with open('yt_june_candidates.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=list(june[0].keys()), delimiter='\t'); w.writeheader()
    for r in june: w.writerow(r)

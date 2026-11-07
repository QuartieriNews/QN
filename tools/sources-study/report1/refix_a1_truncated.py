# Re-extracts the A1 items that hit the old 6.000-character cap of a1_items.py, in place and
# without renumbering: the batches already read point at these ids, so the ids must not move.
import csv, re, html, os, sys
S=os.environ['QN_NET']; R=S+'/report1'
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s))).strip()
def body(d):
    ma=re.search(r'<article>(.*?)</article>',d,flags=re.S)
    if ma: return ma.group(1)
    mh=re.search(r'<h2 class="u-text-h2[^"]*">',d)
    seg=d[mh.start():] if mh else d
    ends=[p for p in (seg.find(mk) for mk in ('Progetti in evidenza','class="Share','Condividi','<footer')) if p>0]
    return seg[:min(ends)] if ends else seg
man=list(csv.DictReader(open(R+'/manifest_report1.csv',encoding='utf-8')))
by_url={r['url']:r for r in man if r['fonte']=='A1'}
fixed=[]
for r in csv.DictReader(open(S+'/A1_june_text.tsv',encoding='utf-8'),delimiter='\t'):
    if len(r['text'])<5990: continue
    row=by_url.get(r['url'])
    if not row: print('NON ABBINATO',r['url']); continue
    f=S+'/A1_items/'+re.sub(r'[^A-Za-z0-9]+','_',r['url'].split('/web/it/')[-1])[:120]+'.html'
    if not os.path.exists(f): print('HTML MANCANTE',row['id']); continue
    d=open(f,encoding='utf-8',errors='replace').read()
    if 'Ã' in d and 'charset' not in d[:2000].lower():
        try: d=d.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError,UnicodeDecodeError): pass
    t=clean(re.sub(r'<script.*?</script>|<style.*?</style>','',body(d),flags=re.S))[:15000]
    old=os.path.getsize(f'{R}/texts/{row["id"]}.txt')
    open(f'{R}/texts/{row["id"]}.txt','w').write(t)
    row['caratteri']=str(len(t)); fixed.append((row['id'],old,len(t)))
keys=list(man[0].keys())
with open(R+'/manifest_report1.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(man)
for i,o,n in fixed: print(f'{i}: {o} -> {n} caratteri')
open(R+'/batches/_da_rileggere.txt','w').write('\n'.join(i for i,_,_ in fixed)+'\n')
print(len(fixed),'item rigenerati; da rileggere:',[i for i,_,_ in fixed])

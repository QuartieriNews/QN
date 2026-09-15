# Clean-text extraction and manifest for the Report 1 textual sources (A1, C1, C2, C4, E2, E3):
# item HTML files -> report1/texts/<id>.txt and report1/manifest_report1.csv (feasibility note §9.6, Report 1).
import os, re, csv, html, glob
S=os.environ['QN_NET']; R=S+'/report1'; os.makedirs(R+'/texts',exist_ok=True)
from html.parser import HTMLParser
class P(HTMLParser):
    SKIP={'script','style','noscript','nav','header','footer','svg','form','button','iframe'}
    def __init__(s): super().__init__(); s.out=[]; s.skip=0; s.main=[]; s.inmain=0
    def handle_starttag(s,t,a):
        if t in s.SKIP: s.skip+=1
        if t in ('main','article'): s.inmain+=1
        if t in ('p','br','div','li','h1','h2','h3','h4','tr'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in s.SKIP and s.skip: s.skip-=1
        if t in ('main','article') and s.inmain: s.inmain-=1
    def handle_data(s,d):
        if s.skip: return
        s.out.append(d)
        if s.inmain: s.main.append(d)
def canon(raw):
    m=re.search(r'rel=["\']?canonical["\']?\s+href=["\']?([^"\' >]+)',raw) or re.search(r'property=["\']og:url["\']\s+content=["\']([^"\']+)',raw)
    return m.group(1) if m else ''
def extract(path):
    raw=open(path,'rb').read().decode('utf-8','ignore'); p=P(); p.feed(raw)
    txt=''.join(p.main) if len(''.join(p.main))>300 else ''.join(p.out)
    txt=html.unescape(txt); txt=re.sub(r'[ \t\r\f\v]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt).strip()
    m=re.search(r'<title>(.*?)</title>',raw,re.S|re.I); title=html.unescape(re.sub(r'\s+',' ',m.group(1))).strip() if m else ''
    return title, txt[:15000], canon(raw)
man=[]
for r in csv.DictReader(open(S+'/A1_june_text.tsv',encoding='utf-8'),delimiter='\t'):
    fid=f'A1_{len(man)+1:03d}'; open(f'{R}/texts/{fid}.txt','w').write(r['text'][:15000])
    man.append({'id':fid,'fonte':'A1','tipo':r['kind'],'url':r['url'],'data_pubblicazione':r['date'],'titolo':r['title'],'municipi_meta':r['municipi'],'tematica':r['tematica'],'caratteri':len(r['text']),'abbinato':'sì'})
def rows(fn): return list(csv.DictReader(open(f'{S}/deliver/{fn}',encoding='utf-8')))
meta={'C1':(rows('C1_2026-06_items.csv'),'url'),'C2':(rows('C2_2026-06_items.csv'),'url'),'C4':(rows('C4_2026-06_items.csv'),'url'),'C5':(rows('C5_2026-06_items.csv'),'url'),'E2':(rows('E2_2026-06_items.csv'),'url'),'E3':(rows('E3_2026-06_items.csv'),'url_rel')}
# The item files are named by report1/fetch_items.py, which truncates the slug to 120 characters
# and keeps the URL's percent-encoding ("%C3%A0" -> "c3_a0"). Recomputing that same transformation
# from the inventory URL matches exactly; substring matching missed every long or accented slug.
def slug_of(u):
    return re.sub(r'[^A-Za-z0-9]+','_',u.rstrip('/').split('/')[-1])[:120]
for fonte,folder in (('C1','C1_items'),('C2','C2_items'),('C4','C4_items'),('C5','C5_items'),('E2','E2_items'),('E3','E3_items')):
    mrows,key=meta[fonte]; k=0
    by_slug={}
    for r in mrows: by_slug.setdefault(slug_of(r[key]),r)
    for f in sorted(glob.glob(f'{S}/{folder}/*.html')):
        title,txt,c=extract(f); base=os.path.basename(f)[:-5]; tail=c.rstrip('/').split('/')[-1] if c else ''
        mrow=by_slug.get(base) or next((r for r in mrows if (tail and tail in r[key]) or base in r[key] or base.replace('_','-') in r[key]), None)
        if fonte=='E3' and mrow is None: continue
        k+=1; fid=f'{fonte}_{k:03d}'; open(f'{R}/texts/{fid}.txt','w').write(txt); mrow=mrow or {}
        man.append({'id':fid,'fonte':fonte,'tipo':'','url':mrow.get('url') or mrow.get('url_rel') or c or base,'data_pubblicazione':mrow.get('data_pubblicazione',''),'data_evento_inizio':mrow.get('data_evento_inizio',''),'data_evento_fine':mrow.get('data_evento_fine',''),'titolo':title,'municipi_meta':mrow.get('municipio_det') or mrow.get('municipio') or mrow.get('municipi_meta',''),'tematica':mrow.get('tema') or mrow.get('tematica',''),'caratteri':len(txt),'abbinato':'sì' if mrow else 'no'})
keys=['id','fonte','tipo','url','data_pubblicazione','data_evento_inizio','data_evento_fine','titolo','municipi_meta','tematica','caratteri','abbinato']
with open(R+'/manifest_report1.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore'); w.writeheader(); w.writerows(man)
import collections; print(len(man),'item',collections.Counter(m['fonte'] for m in man),'non abbinati',sum(1 for m in man if m['abbinato']=='no'))

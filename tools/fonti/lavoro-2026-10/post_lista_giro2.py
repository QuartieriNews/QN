# Pagine Facebook salvate i cui post non sono mai stati letti (né tentati): ingresso del secondo giro
import json,re,glob,openpyxl,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
def key(u):
    u=str(u or '')
    m=re.search(r'profile\.php\?id=(\d+)',u)
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:p/|people/[^/]+/)?([^/?#]+)',u)
    if not m: return None
    s=m.group(1).lower(); m2=re.search(r'-(\d{8,})/?$',s); return m2.group(1) if m2 else s
def urls_in(o):
    if isinstance(o,dict):
        for v in o.values(): yield from urls_in(v)
    elif isinstance(o,list):
        for v in o: yield from urls_in(v)
    elif isinstance(o,str) and 'facebook.com' in o: yield o
read=set()
for f in glob.glob(f'{S}/runts/work/fb_posts/*.json')+glob.glob(f'{S}/assoc/posts_data/*.json')+glob.glob(f'{S}/post_eventi/owner_*.json'):
    for p in json.load(open(f)):
        k=key(p.get('inputUrl') or p.get('facebookUrl') or p.get('url'))
        if k: read.add(k)
tried=set()
for f in [f'{S}/runts/work/fb_urls_post.json',f'{S}/runts/work/fb_urls_post_mancanti.json']+glob.glob(f'{S}/runts/work/in_fbpo*.json')+glob.glob(f'{S}/assoc/in_posts*.json'):
    try: tried|={key(u) for u in urls_in(json.load(open(f)))}
    except Exception as e: print('skip',f,e)
SKIP=('scartare','servizio o professione','tematico non locale','fuori Roma')
cand={}   # chiave -> (url, origine, verdetto)
wb=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v4.xlsx',read_only=True); rr=list(wb.worksheets[0].iter_rows(values_only=True)); h=rr[0]
for r in rr[1:]:
    d=dict(zip(h,r)); k=key(d.get('facebook'))
    if k and d.get('decisione')!='scartare': cand.setdefault(k,(d['facebook'],'registro v4: '+str(d.get('origine')),d.get('decisione')))
for r in json.load(open(f'{S}/runts/work/rows.json')):
    k=key(r.get('facebook'))
    if k: cand.setdefault(k,(r['facebook'],'censimento RUNTS',r['verdetto']))
for r in json.load(open(f'{S}/assoc/rows.json')):
    u=str(r.get('url_pagina')).replace('facebook.com/','www.facebook.com/'); u=u if u.startswith('http') else 'https://'+u.lstrip('/')
    k=key(u)
    if k and not str(r.get('verdetto')).startswith(SKIP): cand.setdefault(k,(u,'censimento associazioni',r.get('verdetto')))
fn=json.load(open(f'{S}/ricerca_quartieri/fb_nuove.json'))
for u in urls_in(fn):
    k=key(u)
    if k: cand.setdefault(k,(u,'ricerca evento + quartiere','pagina nuova'))
BAD={'events','groups','pages','watch','share','sharer','sharer.php','photo.php','story.php','permalink.php','login','hashtag','marketplace','profile.php'}
todo={k:v for k,v in cand.items() if k not in read and k not in tried and k not in BAD and not k.isdigit() or (k.isdigit() and k not in read and k not in tried)}
print('salvate',len(cand),'lette',len(read&set(cand)),'tentate senza esito',len((tried-read)&set(cand)),'da leggere',len(todo))
print(collections.Counter(v[1] for v in todo.values()).most_common())
json.dump(todo,open(f'{S}/post_eventi/giro2/da_leggere.json','w'),ensure_ascii=False,indent=0)

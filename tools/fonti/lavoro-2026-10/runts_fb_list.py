# Elenco delle pagine Facebook da leggere: quella linkata dal sito verificato vince su quella trovata da Google
import json,sys,re,collections
S=sys.argv[1]; W=f'{S}/runts/work'
M=json.load(open(f'{W}/match.json')); V=json.load(open(f'{W}/sites.json')) if __import__('os').path.exists(f'{W}/sites.json') else {}
def key(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
fb={}; src=collections.Counter()
for cf,m in M.items():
    v=V.get(cf,{})
    u=v.get('facebook_dal_sito') if v.get('sito') else None
    if u: fb[cf]=(u,'linkata dal sito verificato'); src['sito']+=1
    elif m.get('facebook'): fb[cf]=(m['facebook'],'ricerca Google (nome nel titolo)'); src['google']+=1
by=collections.defaultdict(list)
for cf,(u,s) in fb.items(): by[key(u)].append(cf)
shared={k:v for k,v in by.items() if len(v)>1}
urls=sorted({u for u,_ in fb.values()})
json.dump({'per_ente':{cf:{'facebook':u,'facebook_origine':s} for cf,(u,s) in fb.items()},'condivise':shared},open(f'{W}/fb.json','w'),ensure_ascii=False,indent=1)
json.dump(urls,open(f'{W}/fb_urls.json','w'))
print('enti con facebook',len(fb),dict(src),'pagine distinte',len(urls),'pagine condivise da più enti',len(shared))

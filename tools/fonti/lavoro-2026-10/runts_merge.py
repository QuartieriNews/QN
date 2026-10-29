# Unisce le verifiche dei siti (ricerca per nome, sito indicato da Facebook, ricerca per codice fiscale) e ricostruisce le pagine Facebook per ente
import json,sys,os,re,collections
S=sys.argv[1]; W=f'{S}/runts/work'
allv={}; orig={}
for f,lab in (('sites.json','ricerca per nome'),('sites_fb.json','sito indicato dalla pagina Facebook'),('sites_cf.json','ricerca per codice fiscale')):
    if not os.path.exists(f'{W}/{f}'): continue
    for cf,v in json.load(open(f'{W}/{f}')).items():
        if v.get('sito') and not (allv.get(cf) or {}).get('sito'): v['sito_trovato_con']=lab; allv[cf]=v
        elif cf not in allv: allv[cf]=v
json.dump(allv,open(f'{W}/sites_all.json','w'),ensure_ascii=False,indent=1)
M=json.load(open(f'{W}/match.json')); extra=json.load(open(f'{W}/fb_da_cf.json')) if os.path.exists(f'{W}/fb_da_cf.json') else {}
fb={}; src=collections.Counter()
for cf in M:
    v=allv.get(cf,{}); u=v.get('facebook_dal_sito') if v.get('sito') else None
    if u: fb[cf]={'facebook':u,'facebook_origine':'linkata dal sito verificato'}; src['sito']+=1
    elif M[cf].get('facebook'): fb[cf]={'facebook':M[cf]['facebook'],'facebook_origine':'ricerca Google (nome nel titolo della pagina)'}; src['google']+=1
    elif cf in extra: fb[cf]={'facebook':extra[cf],'facebook_origine':'ricerca per codice fiscale'}; src['cf']+=1
def key(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
by=collections.defaultdict(list)
for cf,f in fb.items(): by[key(f['facebook'])].append(cf)
json.dump({'per_ente':fb,'condivise':{k:v for k,v in by.items() if len(v)>1}},open(f'{W}/fb.json','w'),ensure_ascii=False,indent=1)
read_ev={key(l.strip()) for l in open(f'{W}/fb_events_visitate.txt') if l.strip()}
read_po=set(json.load(open(f'{W}/fb_posts_lette_reali.json')))
json.dump(sorted(read_ev),open(f'{W}/fb_events_lette.json','w')); json.dump(sorted(read_po),open(f'{W}/fb_posts_lette.json','w'))
print('siti verificati',sum(1 for v in allv.values() if v.get('sito')),collections.Counter(v.get('sito_trovato_con') for v in allv.values() if v.get('sito')),'| facebook',len(fb),dict(src))

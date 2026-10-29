# Promotori degli eventi della pagina «Eventi dei quartieri»: chi organizza ogni evento (host Facebook, «a cura di»
# di culture.roma.it, pagina del post, sito della fonte), collegato a wiki, censimenti e profili Facebook già letti.
import json,re,glob,collections,unicodedata,openpyxl,ast,sys
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'

def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
def fbk(u):
    u=str(u or '')
    m=re.search(r'profile\.php\?id=(\d+)',u)
    if m: return m.group(1)
    m=re.match(r'(?:https?://)?(?:www\.|m\.|web\.|it-it\.)?facebook\.com/(?:p/|people/[^/]+/)?([^/?#]+)',u)
    if not m: return None
    k=m.group(1).lower(); m2=re.search(r'-(\d{8,})/?$',k)
    k=m2.group(1) if m2 else k
    return None if k in ('groups','events','pages','watch','share','sharer','story.php','permalink.php','photo.php','hashtag','profile.php','reel','media') else k
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#]+)',str(u or '').strip().lower()); return m.group(1) if m else None
def ukey(u):   # chiave di un URL: la query resta quando identifica l'oggetto (permalink.php?story_fbid=…, profile.php?id=…)
    u=str(u or '').strip()
    return u.rstrip('/') if re.search(r'\.php\?|[?&](story_fbid|id|fbid|v)=',u) else u.split('?')[0].rstrip('/')
def lit(v):
    if isinstance(v,(list,dict)): return v
    try: return ast.literal_eval(v) if isinstance(v,str) and v[:1] in '[{' else v
    except Exception: return v

E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']

# ---- indici degli eventi grezzi per URL: organizzatori con link e immagine ----
RAW={}
def put(url,**kw):
    if url: RAW.setdefault(ukey(url),{}).update({k:v for k,v in kw.items() if v})
for f in glob.glob(f'{S}/runts/work/fb_events/*.json')+glob.glob(f'{S}/ricerca_quartieri/fb_events_*.json')+glob.glob(f'{P}/fbevents_ev_*.json'):
    for x in json.load(open(f)):
        hs=lit(x.get('hosts')) or []
        put(x.get('url'),hosts=[{'name':h.get('name'),'url':h.get('url')} for h in hs if isinstance(h,dict)],image=x.get('cover_photo_url'))
wb=openpyxl.load_workbook('/mnt/user-data/outputs/eventi_unico.xlsx',read_only=True); ws=wb['Eventi unificati']; rr=ws.iter_rows(values_only=True); h=next(rr)
for r in rr:
    d=dict(zip(h,r))
    for u in (d.get('url'),d.get('link_fonte_diretta')): put(u,org=d.get('organizzatore'),image=d.get('immagine'))
for u,v in json.load(open(f'{S}/assoc/events.json')).items():
    for x in v['eventi']: put(x.get('url'),org=x.get('host'),host_page=u)
for l in open(f'{S}/culture_delta/delta.jsonl'):
    r=json.loads(l); put(r.get('url'),org=r.get('a_cura_di'),email=r.get('email'),telefono=r.get('telefono'),sito=r.get('sito'))
POSTS={}
for f in glob.glob(f'{S}/runts/work/fb_posts/*.json')+glob.glob(f'{S}/assoc/posts_data/*.json')+glob.glob(f'{S}/post_eventi/owner_*.json')+glob.glob(f'{S}/post_eventi/giro2/posts_*.json')+glob.glob(f'{S}/supplementare/posts_*.json'):
    for x in json.load(open(f)):
        if not x.get('url'): continue
        med=lit(x.get('media')) or []
        img=None
        for m in med if isinstance(med,list) else []:
            if isinstance(m,dict):
                img=m.get('photo_image',{}).get('uri') if isinstance(m.get('photo_image'),dict) else None
                img=img or m.get('thumbnail') or (m.get('image') or {}).get('uri') if isinstance(m.get('image'),dict) else img or m.get('thumbnail')
                if img: break
        POSTS[ukey(x['url'])]={'page':x.get('inputUrl') or x.get('facebookUrl'),'pageName':x.get('pageName'),'image':img}

# ---- profili delle pagine Facebook già letti (censimenti, pagine dell'owner) ----
FBP={}
for f in glob.glob(f'{S}/runts/work/fb_pages/*.json')+glob.glob(f'{S}/assoc/pages_data/*.json')+glob.glob(f'{S}/owner_pagine/pages_*.json')+glob.glob(f'{P}/fbpages_*.json'):
    for x in json.load(open(f)):
        if not isinstance(x,dict) or not (x.get('title') or x.get('pageName')): continue
        for u in (x.get('facebookUrl'),x.get('pageUrl'),x.get('inputUrl')):
            k=fbk(u)
            if k: FBP.setdefault(k,x)
        for i in (x.get('pageId'),x.get('facebookId')):
            if i: FBP.setdefault(str(i),x)
W=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
WFB={}; WN={}
for w in W:
    for k in w.get('chiavi') or []:
        if k.startswith('fb-page:'): WFB.setdefault(k[8:].lower(),w)
    for u in (w.get('canali') or {}).get('facebook') or []:
        if fbk(u): WFB.setdefault(fbk(u),w)
    for n in [w['nome']]+(w.get('alias') or []):
        if norm(n): WN.setdefault(norm(n),w)
RU={};RUN={}
for r in json.load(open(f'{S}/runts/work/rows.json')):
    if fbk(r.get('facebook')): RU.setdefault(fbk(r['facebook']),r)
    RUN.setdefault(norm(r['denominazione']),r)
AS={};ASN={}
for r in json.load(open(f'{S}/assoc/rows.json')):
    if fbk(r.get('url_pagina')): AS.setdefault(fbk(r['url_pagina']),r)
    ASN.setdefault(norm(r['nome']),r)
SU={};SUN={}
for o in json.load(open(f'{S}/supplementare/lista.json')):
    if fbk(o.get('facebook')): SU.setdefault(fbk(o['facebook']),o)
    SUN.setdefault(norm(o['nome']),o)

# ---- eventi -> promotori ----
def split_org(s):
    parts=[p.strip() for p in re.split(r', |; ',str(s)) if p.strip()]; out=[]
    for p in parts:
        if out and (p[:1].isdigit() or p[:1].islower()): out[-1]+=', '+p
        else: out.append(p)
    return out
PR={}; ev_pr=[]
def key_for(name,fb=None):
    k=fbk(fb)
    return ('fb:'+k) if k else ('n:'+norm(name))
PLATF=re.compile(r'^(www\.)?(facebook|instagram|youtube|tiktok|linktr)\.(com|ee)$',re.I)
def add(name,fb,e,ruolo,via):
    if name and PLATF.match(str(name).strip()): name=None   # il nome di una piattaforma non è un promotore
    if not name and not fb: return None
    k=key_for(name,fb)
    p=PR.setdefault(k,{'key':k,'nomi':collections.Counter(),'fb':fb if fbk(fb) else None,'eventi':[],'ruoli':collections.Counter(),'via':collections.Counter()})
    if name: p['nomi'][str(name).strip()]+=1
    p['eventi'].append(e['i']); p['ruoli'][ruolo]+=1; p['via'][via]+=1
    return k
for i,e in enumerate(E):
    e['i']=i; u=ukey(e.get('url')); raw=RAW.get(u,{}); post=POSTS.get(u); ks=[]
    if post:
        ks.append(add(post.get('pageName') or e.get('org'),post.get('page'),e,'pagina che annuncia','post Facebook'))
    elif raw.get('hosts'):
        for j,hh in enumerate(raw['hosts']): ks.append(add(hh.get('name'),hh.get('url'),e,'organizzatore' if j==0 else 'co-organizzatore','evento Facebook (host)'))
    elif e.get('org'):
        names=split_org(e['org']) if e['src']=='Facebook' or '; ' in str(e['org']) else [e['org']]
        for j,n in enumerate(names): ks.append(add(n,None,e,'organizzatore' if j==0 else 'co-organizzatore',{'culture.roma.it':'culture.roma.it «a cura di»','sito della fonte':'sito della fonte','Facebook':'evento Facebook (nome)','Facebook (post)':'post Facebook','Roma Today':'Roma Today (promotore)'}.get(e['src'],e['src'])))
    ev_pr.append([k for k in ks if k])
# un nome senza link che coincide con un promotore con pagina Facebook: stesso promotore
byname={}
for k,p in PR.items():
    if k.startswith('fb:'):
        for n in p['nomi']: byname.setdefault(norm(n),k)
for k in [k for k in PR if k.startswith('n:')]:
    t=byname.get(k[2:])
    if t:
        a=PR.pop(k); b=PR[t]; b['nomi'].update(a['nomi']); b['eventi']+=a['eventi']; b['ruoli'].update(a['ruoli']); b['via'].update(a['via'])
        for lst in ev_pr: lst[:]=[t if x==k else x for x in lst]

# ---- collegamenti e dati già raccolti ----
for k,p in PR.items():
    fk=k[3:] if k.startswith('fb:') else None; nm=p['nomi'].most_common(1)[0][0] if p['nomi'] else fk; p['nome']=nm; nn=norm(nm)
    w=(WFB.get(fk) if fk else None) or WN.get(nn)
    prof=FBP.get(fk) if fk else None
    if not prof and w:
        for u in (w.get('canali') or {}).get('facebook') or []:
            prof=prof or FBP.get(fbk(u))
    ru=(RU.get(fk) if fk else None) or RUN.get(nn); asr=(AS.get(fk) if fk else None) or ASN.get(nn); su=(SU.get(fk) if fk else None) or SUN.get(nn)
    p['wiki']=w['id'] if w else None
    p['link']={'wiki':bool(w),'profilo_facebook':bool(prof),'runts':bool(ru),'censimento_associazioni':bool(asr),'lista_supplementare':bool(su)}
    p['_w'],p['_prof'],p['_ru'],p['_as'],p['_su']=w,prof,ru,asr,su
    evs=[E[i] for i in p['eventi']]
    p['n_eventi']=len(set(p['eventi'])); p['src']=collections.Counter(e['src'] for e in evs)
    p['pagine_qn']=collections.Counter(e['z'] for e in evs if e.get('z')); p['municipi']=collections.Counter(e['m'] for e in evs if e.get('m'))
    p['contatti_evento']={'email':{RAW.get(ukey(e.get('url')),{}).get('email') for e in evs}-{None},
                          'telefono':{RAW.get(ukey(e.get('url')),{}).get('telefono') for e in evs}-{None},
                          'sito':{RAW.get(ukey(e.get('url')),{}).get('sito') for e in evs}-{None}}
json.dump({'eventi_promotori':ev_pr},open(f'{P}/eventi_promotori.json','w'))
import pickle; pickle.dump({'PR':PR,'RAW':RAW,'POSTS':POSTS},open(f'{P}/base.pkl','wb'))
c=collections.Counter()
for p in PR.values():
    for kk,v in p['link'].items(): c[kk]+=v
print('promotori',len(PR),'con pagina Facebook',sum(1 for k in PR if k.startswith('fb:')),dict(c))
print('eventi senza promotore',sum(1 for l in ev_pr if not l))
print('per numero di eventi',collections.Counter(min(p['n_eventi'],10) for p in PR.values()))

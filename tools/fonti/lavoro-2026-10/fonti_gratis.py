# Leve gratuite del 26 ottobre (sera), un lettore solo: tipi «evento» di WordPress con le pagine evento in schema.org (L19, L56),
# link esterni dei post verso le pagine ufficiali (L11), feed RSS di Tor Vergata, ASL Roma 3 e Caritas (L48, L57), VisitLazio (L59),
# Parco dell'Appia (residuo L51), avvisi parrocchiali in prova su poche parrocchie (L43). Robots.txt rispettato sull'URL esatto, una
# richiesta al secondo per host, campi di contatto e testi delle persone mai conservati; Roma Today, social e biglietterie mai letti.
import json,re,sys,time,html,glob,datetime,collections,threading,urllib.request,urllib.parse
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
sys.path.insert(0,f'{S}/post_eventi'); import estrai as X
TODAY=datetime.date(2026,10,26); ORIZ=90
UA=ls.UA
NEVER=re.compile(r'(^|\.)(romatoday\.it|citynews\.it|today\.it|facebook\.com|fb\.me|instagram\.com|tiktok\.com|x\.com|twitter\.com|youtube\.com|youtu\.be|linkedin\.com|whatsapp\.com|wa\.me|t\.me|'
                 r'eventbrite\.[a-z.]+|ticketone\.it|vivaticket\.(it|com)|dice\.fm|ticketmaster\.it|ticketsms\.it|xceed\.me|feverup\.com|linktr\.ee|bit\.ly|forms\.gle|docs\.google\.com|gofund\.me|mailchi\.mp)$')
PRIV=re.compile(r'\b(defunt\w*|esequie|funeral\w*|lutto|intenzion\w*|battesim\w*|matrimon\w*|cresim\w*|prima comunion\w*|confession\w*|colloqui\w*|ricoverat\w*)\b',re.I)
def host(u): return urllib.parse.urlsplit(u).netloc.lower().split(':')[0]
lock=threading.Lock(); last={}; robots={}; st=collections.Counter()
def wait(h):
    with lock:
        w=last.get(h,0)+1.0-time.time(); last[h]=max(time.time(),last.get(h,0)+1.0)
    if w>0: time.sleep(w)
def get(u,accept='text/html,application/json,*/*;q=0.5'):
    h=host(u)
    if NEVER.search(h): raise ValueError('host escluso')
    with lock: cache=robots
    if not ls.robots_allows(u,lambda x: _raw(x),cache,wait): raise PermissionError('robots.txt')
    wait(h); return _raw(u,accept)
def _raw(u,accept='text/plain,*/*'):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':accept})
    with urllib.request.urlopen(req,timeout=30) as r: return r.read(4_000_000).decode('utf-8','replace')
out=[]
def keep(r,canale,org,dv=False):
    if not r.get('evento') or not r.get('inizio'): return
    if PRIV.search(r['evento']): st['riti o persone private']+=1; return
    out.append({'host':host(r.get('pagina') or r.get('url') or ''),'canale':canale,'titolo':html.unescape(r['evento'])[:160],'inizio':r['inizio'][:16],'fine':(r.get('fine') or '')[:10] or None,
                'ora':(r['inizio'][11:16] if len(r['inizio'])>10 and r['inizio'][11:16]!='00:00' else None),'luogo':r.get('luogo'),'indirizzo':r.get('indirizzo'),'org':org,
                'url':r.get('url') or r.get('pagina'),'dv':dv})
def jsonld_pages(urls,canale,org_of):
    def one(u):
        try: doc=get(u)
        except Exception as e: st[f'{canale}: non letta ({type(e).__name__})']+=1; return
        rows=ls.read_page({'id':canale,'nome':org_of(u)},u,doc,TODAY,ORIZ,solo_jsonld=True)
        st[f'{canale}: pagine lette']+=1
        for r in rows: keep(r,canale,org_of(u))
    with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,urls))
# --- L19/L56: tipi evento di WordPress (non Tribe: già nei feed) -> pagine evento in schema.org
CPT={}
for f in ('after.jsonl','tutti.jsonl'):
    for l in open(f'{S}/giro3_feed/out/{f}'):
        r=json.loads(l); h=r['host']
        for k,v in r.items():
            m=re.match(r'cpt_(.+?)_(nuovi|modificati)_30gg$',k)
            if m and v and m.group(1)!='tribe_events': CPT.setdefault(h,set()).add(m.group(1))
        if r.get('cpt') and r.get('cpt_30gg'):
            for t in r['cpt']:
                if t!='tribe_events': CPT.setdefault(h,set()).add(t)
NAZ=re.compile(r'(auroraeventi\.net|murialdo\.taa\.it|archeoclubitalia\.org|nomostrek\.com|togethernetwork\.org|usacli\.it|komen\.it)$')   # enti nazionali o fuori Roma (verifica di L19)
links=[]
def list_cpt(h):
    for t in sorted(CPT[h]):
        u=f'https://{h if h.startswith("www.") or h.count(".")>1 else h}/wp-json/wp/v2/{t}?per_page=40&orderby=date&order=desc&_fields=link,date,modified'
        try: d=json.loads(get(u,'application/json'))
        except Exception as e: st['tipi evento: elenco non letto']+=1; continue
        for x in d if isinstance(d,list) else []:
            if str(x.get('date') or '')[:10]>=str(TODAY-datetime.timedelta(days=120)) and x.get('link'): links.append(x['link'])
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(list_cpt,[h for h in CPT if not NAZ.search(h)]))
st['tipi evento: host']=len(CPT); st['tipi evento: pagine evento']=len(links)
SEAT={}
for f in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']:
    for u in (f.get('canali') or {}).get('sito') or []:
        SEAT.setdefault(host(u).replace('www.',''),f['nome'])
org_of=lambda u: SEAT.get(host(u).replace('www.',''),host(u).replace('www.',''))
jsonld_pages(links[:600],'tipi evento WordPress',org_of)
# --- L11: link esterni dei post con un evento futuro
F=json.load(open(f'{S}/post_eventi/eventi_post_futuri.json')); want={x['url_post'] for x in F if x.get('url_post')}
ext=set()
for f in glob.glob(f'{S}/runts/work/fb_posts/*.json')+glob.glob(f'{S}/assoc/posts_data/*.json')+glob.glob(f'{S}/post_eventi/owner_*.json')+glob.glob(f'{S}/post_eventi/giro2/posts_*.json')+glob.glob(f'{S}/supplementare/posts_*.json'):
    for p in json.load(open(f)):
        if isinstance(p,dict) and p.get('url') in want and p.get('link','').startswith('http') and not NEVER.search(host(p['link'])): ext.add(p['link'])
st['link dei post: pagine']=len(ext)
jsonld_pages(sorted(ext),'link dei post',org_of)
# --- L48/L57: feed RSS di Tor Vergata, ASL Roma 3, Caritas: notizie con una data futura e parole da evento -> candidati
RSS={'https://web.uniroma2.it/it/rss/eventi/2026/10':'Università di Roma Tor Vergata','https://web.uniroma2.it/it/rss/eventi/2026/11':'Università di Roma Tor Vergata',
     'https://web.uniroma2.it/it/rss/eventi/2026/12':'Università di Roma Tor Vergata','https://www.aslroma3.it/feed/':'ASL Roma 3','https://www.caritasroma.it/feed/':'Caritas di Roma'}
for u,org in RSS.items():
    try: x=get(u,'application/rss+xml,application/xml,text/xml')
    except Exception as e: st['rss: non letto']+=1; continue
    for it in re.findall(r'<item>(.*?)</item>',x,re.S):
        g=lambda t: html.unescape(re.sub(r'<!\[CDATA\[|\]\]>|<[^>]+>',' ',(re.search(rf'<{t}>(.*?)</{t}>',it,re.S) or [None,''])[1])).strip()
        tit,desc,link=g('title'),g('description'),g('link')
        ds=[d for d in ls.dates_in_block(f'{tit} {desc}',TODAY) if TODAY<=d<=TODAY+datetime.timedelta(days=ORIZ)]
        if not ds or not X.EVENTO.search(f'{tit} {desc}'): st['rss: notizia senza data futura o senza evento']+=1; continue
        keep({'evento':tit,'inizio':ds[0].isoformat(),'fine':ds[-1].isoformat() if len(ds)>1 else None,'url':link},'feed RSS di enti',org,dv=True)
# --- L59: VisitLazio, eventi schema.org con sede nel Comune di Roma
try:
    doc=get('https://www.visitlazio.com/eventi/')
    for r in ls.read_page({'id':'visitlazio','nome':'VisitLazio'},'https://www.visitlazio.com/eventi/',doc,TODAY,ORIZ,solo_jsonld=True):
        a=f"{r.get('luogo') or ''} {r.get('indirizzo') or ''}"
        caps=re.findall(r'\b(\d{5})\b',a)
        if (caps and all('00100'<=c<='00199' for c in caps)) or (not caps and re.search(r'\bRoma\b',a) and not X.OTHERC.search(a)): keep(r,'VisitLazio',r.get('luogo') or 'VisitLazio')
        else: st['VisitLazio: fuori Roma']+=1
except Exception as e: st['VisitLazio: non letta']+=1
# --- residuo L51: calendario del Parco regionale dell'Appia Antica (The Events Calendar)
for u in ('https://eventi.parcoappiaantica.it/?post_type=tribe_events&ical=1','https://eventi.parcoappiaantica.it/eventi/?ical=1'):
    try: txt=get(u,'text/calendar')
    except Exception: continue
    if 'BEGIN:VCALENDAR' not in txt: continue
    ev=None; serie=set()
    for line in re.sub(r'\r?\n[ \t]','',txt).split('\n'):
        line=line.rstrip('\r')
        if line=='BEGIN:VEVENT': ev={}
        elif line=='END:VEVENT' and ev is not None:
            m=re.match(r'(\d{4})(\d{2})(\d{2})(?:T(\d{2})(\d{2}))?',ev.get('DTSTART',''))
            if m and ev.get('SUMMARY'):
                d1=f'{m.group(1)}-{m.group(2)}-{m.group(3)}'; k=re.sub(r'\W','',ev['SUMMARY'].lower())[:40]
                if TODAY.isoformat()<=d1<=(TODAY+datetime.timedelta(days=ORIZ)).isoformat() and k not in serie:
                    serie.add(k); keep({'evento':ev['SUMMARY'].replace('\\,',','),'inizio':d1+(f'T{m.group(4)}:{m.group(5)}' if m.group(4) else ''),'luogo':(ev.get('LOCATION') or 'Parco regionale dell\'Appia Antica').replace('\\,',','),'url':ev.get('URL')},'Parco dell\'Appia Antica','Parco regionale dell\'Appia Antica')
            ev=None
        elif ev is not None and ':' in line:
            k,v=line.split(':',1); ev[k.split(';')[0].upper()]=v.strip()
    break
# --- L43 in prova: pagina avvisi, notiziario o calendario di parrocchie fuori dal centro
W=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
par=[f for f in W if re.search(r'parrocch',f['nome'],re.I) and (f.get('canali') or {}).get('sito') and f.get('municipio') not in (None,'I','II')]
par=sorted(par,key=lambda f:f['id'])[:16]
AVV=re.compile(r'href=["\']([^"\']+)["\'][^>]*>[^<]{0,40}\b(avvisi|notiziario|foglio|calendario|appuntamenti|agenda|bollettino|settimana)\b',re.I)
def parrocchia(f):
    home=f['canali']['sito'][0]
    try: d=get(home)
    except Exception: st['avvisi: home non letta']+=1; return
    m=AVV.search(d); u=urllib.parse.urljoin(home,html.unescape(m.group(1))) if m else None
    if not u or host(u).replace('www.','')!=host(home).replace('www.',''): st['avvisi: nessuna pagina avvisi']+=1; return
    try: d2=get(u)
    except Exception: st['avvisi: pagina non letta']+=1; return
    rows=[r for r in ls.read_page({'id':f['id'],'nome':f['nome']},u,d2,TODAY,45) if X.EVENTO.search(r['evento']) and not re.fullmatch(r'\W*(s\.?\s*)?messa\b.*',r['evento'],re.I)]
    st['avvisi: pagine lette']+=1
    for r in rows[:15]: keep(r,'avvisi parrocchiali (prova)',f['nome'],dv=True)
with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(parrocchia,par))
json.dump(out,open(f'{S}/feed/fonti_gratis.json','w'),ensure_ascii=False,indent=0)
print(dict(st)); print('righe',len(out),collections.Counter(r['canale'] for r in out))

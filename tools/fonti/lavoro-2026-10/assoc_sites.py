# Legge i siti web delle pagine (gratis): pagina eventi/calendario, JSON-LD Event, date viste; geocodifica gli indirizzi.
import json,sys,re,html,time,os,urllib.request,urllib.parse,gzip,ssl,collections
from concurrent.futures import ThreadPoolExecutor
from datetime import date
S=sys.argv[1]; pages=json.load(open(f'{S}/assoc/pages_enriched.json'))
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-eventi/1.0 (+contatto: redazione)'
TODAY=date(2026,10,24); SIX=date(2026,4,24)
SOCIAL=re.compile(r'(facebook\.com|instagram\.com|tiktok\.com|youtube\.com|linkedin\.com|x\.com|twitter\.com|maps\.google|goo\.gl|linktr\.ee|wa\.me|t\.me|telegram)',re.I)
EVWORDS=re.compile(r'/(eventi|events|event|calendario|calendar|agenda|programma|appuntamenti|iniziative|attivita|attività|news|notizie|stagione|spettacoli|corsi)(/|\.|$|\?)',re.I)
MESI='gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre'
M={m:i+1 for i,m in enumerate(MESI.split('|'))}
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept-Language':'it-IT,it;q=0.9','Accept':'text/html,*/*'})
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(2_500_000)
        if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        return r.geturl(), b.decode('utf-8','replace')
def ld_events(d):
    out=[]
    for mm in re.finditer(r'<script[^>]+ld\+json[^>]*>(.*?)</script>',d,re.S|re.I):
        try: j=json.loads(mm.group(1).strip())
        except Exception:
            try: j=json.loads(re.sub(r',\s*([}\]])',r'\1',mm.group(1).strip()))
            except Exception: continue
        st=[j]
        while st:
            o=st.pop()
            if isinstance(o,dict):
                t=o.get('@type'); t=t if isinstance(t,str) else (t[0] if isinstance(t,list) and t else '')
                if t and 'Event' in t and o.get('startDate'): out.append(str(o.get('startDate'))[:10])
                st.extend(v for v in o.values() if isinstance(v,(dict,list)))
            elif isinstance(o,list): st.extend(o)
    return out
def dates_in_text(t):
    ds=set()
    for m in re.finditer(r'\b(\d{1,2})\s+('+MESI+r')\s+(\d{4})',t,re.I):
        try: ds.add(date(int(m.group(3)),M[m.group(2).lower()],int(m.group(1))))
        except Exception: pass
    for m in re.finditer(r'\b(\d{1,2})[/.](\d{1,2})[/.](20\d{2})\b',t):
        try: ds.add(date(int(m.group(3)),int(m.group(2)),int(m.group(1))))
        except Exception: pass
    for m in re.finditer(r'\b(20\d{2})-(\d{2})-(\d{2})\b',t):
        try: ds.add(date(int(m.group(1)),int(m.group(2)),int(m.group(3))))
        except Exception: pass
    return ds
def site_of(p):
    d=p.get('dati') or {}
    cands=[d.get('website')]+list(d.get('websites') or [])
    for c in cands:
        if c and c.startswith('http') and not SOCIAL.search(c): return c
    return None
def work(p):
    u=site_of(p)
    if not u: return None
    r={'sito':u}
    try: final,d=fetch(u)
    except Exception as e: r['esito']='non raggiungibile: '+str(e)[:60]; return r
    r['esito']='letto'; r['sito_finale']=final
    base=re.match(r'https?://[^/]+',final).group(0)
    links=[]
    for l in re.findall(r'href=["\']([^"\'#]+)',d):
        l=urllib.parse.urljoin(final,l)
        if l.startswith(base) and EVWORDS.search(l) and l not in links: links.append(l)
    r['pagina_eventi']=links[0] if links else None
    evs=ld_events(d); txt=html.unescape(re.sub(r'\s+',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d,flags=re.S)))
    ds=dates_in_text(re.sub(r'<[^>]+>',' ',txt))
    if links:
        try:
            _,d2=fetch(links[0]); evs+=ld_events(d2); ds|=dates_in_text(html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d2,flags=re.S))))
        except Exception: pass
    evd=set()
    for e in evs:
        try: evd.add(date.fromisoformat(e))
        except Exception: pass
    alld=ds|evd
    r['jsonld_eventi']=len(evs); r['eventi_jsonld_futuri']=sum(1 for x in evd if x>=TODAY); r['eventi_jsonld_6mesi']=sum(1 for x in evd if SIX<=x<TODAY)
    r['date_future_nel_sito']=sum(1 for x in alld if TODAY<=x<=date(2027,12,31)); r['date_ultimi_6_mesi']=sum(1 for x in alld if SIX<=x<TODAY)
    r['ultima_data_vista']=max((x for x in alld if x<=date(2027,12,31)),default=None).isoformat() if alld else None
    return r
targets=[p for p in pages if site_of(p)]
print('siti da leggere',len(targets),flush=True)
res={}
with ThreadPoolExecutor(max_workers=8) as ex:
    for p,r in zip(targets,ex.map(work,targets)):
        res[p['url']]=r
        if len(res)%50==0: print(len(res),flush=True)
json.dump(res,open(f'{S}/assoc/sites.json','w'),ensure_ascii=False,indent=1)
c=collections.Counter(r['esito'].split(':')[0] for r in res.values() if r); print('esiti',c)
print('con pagina eventi',sum(1 for r in res.values() if r and r.get('pagina_eventi')),'| con JSON-LD Event',sum(1 for r in res.values() if r and r.get('jsonld_eventi')),'| con date future',sum(1 for r in res.values() if r and r.get('date_future_nel_sito')),'| con date ultimi 6 mesi',sum(1 for r in res.values() if r and r.get('date_ultimi_6_mesi')))

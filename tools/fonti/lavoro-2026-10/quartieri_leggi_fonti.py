# Lettura delle fonti nuove (siti) trovate con «evento + quartiere»: robots.txt rispettato, pagina eventi, eventi schema.org e blocchi datati, indirizzo
import json,re,sys,html,gzip,urllib.request,urllib.parse,urllib.robotparser,collections,time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; D=f'{S}/ricerca_quartieri'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
sys.path.insert(0,f'{S}/scripts'); from mirate_liste import geocode,place,cache,CACHE
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-fonti/1.0 (+contatto redazione)'
TODAY=date(2026,10,24)
EVW=re.compile(r'/(eventi|events|event|calendario|calendar|agenda|programma|appuntamenti|iniziative|attivita|stagione|spettacoli|news|notizie)(/|\.|$|\?)',re.I)
ADDR=re.compile(r"((?:Via|Viale|V\.le|Piazza|P\.zza|Largo|Piazzale|Vicolo|Lungotevere|Circonvallazione|Corso|Borgo|Salita)\s+[A-Za-zÀ-ÿ'’.\s]{2,50}?,?\s*(?:n\.?\s*)?\d+[A-Za-z]?)[\s,–-]*(00[01]\d\d)\s*[-–,]?\s*Roma",re.I)
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept-Language':'it-IT,it;q=0.9','Accept':'text/html,*/*'})
    with urllib.request.urlopen(req,timeout=20) as r:
        b=r.read(2_000_000)
        if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        return r.geturl(),b.decode('utf-8','replace')
def robots_ok(u):
    p=urllib.parse.urlsplit(u); rp=urllib.robotparser.RobotFileParser()
    try:
        _,txt=fetch(f'{p.scheme}://{p.netloc}/robots.txt'); rp.parse(txt.splitlines())
    except Exception: return True
    return rp.can_fetch('*',u) and rp.can_fetch(UA,u)
def text(d): return html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>',' ',d,flags=re.S|re.I)))
def work(src):
    urls=src['url_esempio'].split(' · '); home='https://'+src['fonte']
    out={'fonte':src['fonte'],'categoria':src['categoria'],'pagine_qn':src['pagine_qn'],'ricerche':src['ricerche'],'eventi':[],'lette':[]}
    if re.search(r'(^|\.)(romatoday\.it|citynews\.it|today\.it)$',src['fonte']): out['esito']='non letto: Roma Today, licenza Citynews (DEC-026)'; return out
    if not robots_ok(home): out['esito']='robots.txt vieta la lettura'; return out
    fonte={'id':'Q-'+src['fonte'],'nome':src['fonte']}
    todo=list(dict.fromkeys([home]+urls[:2])); seen=set()
    for u in todo:
        if u in seen or len(out['lette'])>=4: continue
        seen.add(u)
        if not robots_ok(u): continue
        try: final,d=fetch(u)
        except Exception as e: out.setdefault('errori',[]).append(str(e)[:60]); continue
        out['lette'].append(final)
        if u==home:
            m=re.search(r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)',d,re.I) or re.search(r'<title>(.*?)</title>',d,re.S|re.I)
            out['nome']=html.unescape(re.sub(r'\s+',' ',m.group(1))).strip()[:90] if m else src['fonte']
            fonte['nome']=out['nome']
            links=[urllib.parse.urljoin(final,l) for l in re.findall(r'href=["\']([^"\'#]+)',d)]
            base=re.match(r'https?://[^/]+',final).group(0)
            ev=[l for l in dict.fromkeys(links) if l.startswith(base) and EVW.search(l[len(base):])]
            if ev: out['pagina_eventi']=ev[0]; todo.append(ev[0])
            out['facebook']=next((re.sub(r'[?#].*$','',l).rstrip('/') for l in links if re.match(r'https?://(www\.)?facebook\.com/(?!sharer|share|dialog|plugins|tr\b|events/|groups/)[^/]+',l)),None)
        t=text(d)
        if not out.get('indirizzo'):
            a=ADDR.search(t)
            if a: out['indirizzo']=f"{re.sub(r'\s+',' ',a.group(1)).strip()}, {a.group(2)} Roma"
        for r in ls.read_page(fonte,final,d,TODAY,90):
            if r['prova']=='data nel testo' and len(r['evento'])<25: continue
            out['eventi'].append(r)
    k=set(); ev=[]
    for r in out['eventi']:
        kk=(r['evento'][:60],r['inizio'])
        if kk not in k: k.add(kk); ev.append(r)
    out['eventi']=ev[:40]; out['esito']='letto' if out['lette'] else 'non raggiungibile'
    return out
if __name__=='__main__':
    dom=json.load(open(f'{D}/domini.json'))
    import os
    prev=json.load(open(f'{D}/fonti_lette.json')) if os.path.exists(f'{D}/fonti_lette.json') else []
    done={r['fonte'] for r in prev}
    todo=[d for d in dom if d['categoria'] in ('sito','istituzionale') and d['gia_nota']=='no' and d['fonte'] not in done]
    print('fonti nuove da leggere',len(todo),flush=True)
    with ThreadPoolExecutor(max_workers=12) as ex: res=list(ex.map(work,todo))
    new=res; res=prev+res
    for r in new:
        if r.get('indirizzo'):
            g=geocode(r['indirizzo'])
            if g:
                lat,lon=float(g[0]['lat']),float(g[0]['lon']); m,sd,_=place(lat,lon); r.update(lat=lat,lon=lon,municipio=m,sudd_nome=sd)
    json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(res,open(f'{D}/fonti_lette.json','w'),ensure_ascii=False,indent=1)
    c=collections.Counter(r['esito'] for r in res); print(dict(c),'con eventi schema.org',sum(1 for r in res if any(e['prova']=='jsonld' for e in r['eventi'])),'con date future',sum(1 for r in res if r['eventi']),'eventi',sum(len(r['eventi']) for r in res))

# Per ogni evento senza fonte: tiene i candidati Google non aggregatori, legge la pagina e verifica che il titolo compaia.
import json,re,sys,unicodedata,urllib.request,urllib.parse,html,ssl,collections
from concurrent.futures import ThreadPoolExecutor
S=sys.argv[1]
meta=json.load(open(f'{S}/ricerca/eventi_con_candidati.json'))
AGG2=re.compile(r'(spotlightapp|vibeloop|eventivicino|araundapp|zazoom|roma-o-matic|experience-app|initaly\.it|cittando|romalike|funweek|lazioeventi|cosasuccedearoma|trovasagre|oazis\.app|iltaccodibacco|ezrome|revenews|universinet|aboutartonline|solomente|eventa\.it|concerti\.it|romatoday|facebook|instagram|eventbrite|dice\.fm|ticket|wikipedia|google|tiktok|youtube|linkedin|twitter|x\.com|roma\.repubblica|messaggero|corriere|ansa|rainews|turismoroma|060608|comune\.roma|culture\.roma|artribune|exibart|arte\.it|mymovies|teatro\.it|teatrionline|rockol|romaweekend|fanpage|leggo|iltempo|abitarearoma|virgilio|paginegialle|visitlazio|romasette|agenziastampa|adnkronos|askanews|dire\.it|quotidiano|giornale|notizie|news|magazine|blog|eventi\.|-eventi|eventiroma|romaeventi|allevents|evensi|2night|zero\.eu|songkick|bandsintown|residentadvisor|xceed|clubbing|viagogo|stubhub)',re.I)
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-eventi/1.0 (+contatto: redazione)'
def norm(s): return re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())
def toks(s): return [t for t in norm(s).split() if len(t)>3 and t not in ('della','delle','degli','dell','nella','nelle','roma','2026','2027','con','per','alla','alle','presso','evento','mostra','concerto')]
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'text/html'})
    with urllib.request.urlopen(req,timeout=25) as r: return r.read(1500000).decode('utf-8','replace')
def work(m):
    cands=[c for c in m.get('candidati',[]) if not AGG2.search(c['url'])][:3]
    tt=toks(m['nome']); out=[]
    for c in cands:
        try: d=fetch(c['url'])
        except Exception as e: c['verifica']='non raggiungibile'; out.append(c); continue
        txt=norm(html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d,flags=re.S))))
        hit=sum(1 for t in tt if t in txt); c['verifica']=f'{hit}/{len(tt)} parole del titolo nella pagina'; c['conferma']= bool(tt) and hit>=max(2,int(0.6*len(tt)))
        jl='application/ld+json' in d and '"Event"' in d; c['jsonld_event']=jl
        out.append(c)
    m['candidati_verificati']=out
    m['fonte_trovata']=next((c['url'] for c in out if c.get('conferma')),None)
    return m
with ThreadPoolExecutor(max_workers=8) as ex: res=list(ex.map(work,meta))
json.dump(res,open(f'{S}/ricerca/eventi_verificati.json','w'),ensure_ascii=False,indent=1)
print('eventi',len(res),'con candidato non aggregatore',sum(1 for m in res if m['candidati_verificati']),'fonte confermata',sum(1 for m in res if m['fonte_trovata']))
print(collections.Counter(urllib.parse.urlsplit(m['fonte_trovata']).netloc for m in res if m['fonte_trovata']).most_common(20))

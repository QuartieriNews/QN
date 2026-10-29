# Verifica dei siti candidati: la pagina deve contenere il codice fiscale o il nome dell'ente. Dal sito verificato: social, indirizzo con CAP, segnali di eventi.
import json,sys,re,html,gzip,urllib.request,urllib.parse,unicodedata,collections
from concurrent.futures import ThreadPoolExecutor
from datetime import date
S=sys.argv[1]; W=f'{S}/runts/work'
E={e['cf']:e for e in json.load(open(f'{W}/enti.json'))}; MF=sys.argv[2] if len(sys.argv)>2 else 'match.json'; OUTF=sys.argv[3] if len(sys.argv)>3 else 'sites.json'; M=json.load(open(f'{W}/{MF}'))
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-fonti/1.0 (+contatto redazione)'
TODAY=date(2026,10,24); SIX=date(2026,4,24)
MESI='gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre'; MN={m:i+1 for i,m in enumerate(MESI.split('|'))}
EVWORDS=re.compile(r'/(eventi|events|event|calendario|calendar|agenda|programma|appuntamenti|iniziative|attivita|attività|news|notizie|stagione|spettacoli|corsi|laboratori)(/|\.|$|\?)',re.I)
GENERIC={'associazione','culturale','sportiva','comitato','centro','gruppo','circolo','roma','di','del','della','dei','delle','il','la','le','lo','e','per','a','in','con','onlus','amici','fondazione','italia','italiana','nazionale','provinciale','regionale','lazio','sezione','territoriale','aps','odv','ets','asd','cooperativa','sociale','impresa','promozione','volontariato'}
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept-Language':'it-IT,it;q=0.9','Accept':'text/html,*/*'})
    with urllib.request.urlopen(req,timeout=20) as r:
        b=r.read(2_000_000)
        if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        return r.geturl(), b.decode('utf-8','replace')
def fbclean(l):
    m=re.match(r'https?://(?:www\.|m\.|it-it\.)?facebook\.com/profile\.php\?(?:.*&)?id=(\d+)',l)
    if m: return f'https://www.facebook.com/profile.php?id={m.group(1)}'
    l=re.sub(r'[?#].*$','',l).rstrip('/'); l=re.sub(r'facebook\.com/(?:pg|pages)/','facebook.com/',l); l=re.sub(r'^https?://(?:m\.|it-it\.)?facebook','https://www.facebook',l).replace('http://www.','https://www.')
    if re.search(r'facebook\.com/profile\.php$',l): return None
    return l
def text(d): return html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>',' ',d,flags=re.S|re.I)))
def dates(t):
    ds=set()
    for m in re.finditer(r'\b(\d{1,2})\s+('+MESI+r')\s+(\d{4})',t,re.I):
        try: ds.add(date(int(m.group(3)),MN[m.group(2).lower()],int(m.group(1))))
        except Exception: pass
    for m in re.finditer(r'\b(\d{1,2})[/.](\d{1,2})[/.](20\d{2})\b',t):
        try: ds.add(date(int(m.group(3)),int(m.group(2)),int(m.group(1))))
        except Exception: pass
    return ds
def ld_event_dates(d):
    out=[]
    for mm in re.finditer(r'<script[^>]+ld\+json[^>]*>(.*?)</script>',d,re.S|re.I):
        for m in re.finditer(r'"@type"\s*:\s*"(\w*Event)".*?"startDate"\s*:\s*"(\d{4}-\d{2}-\d{2})',mm.group(1),re.S):
            try: out.append(date.fromisoformat(m.group(2)))
            except Exception: pass
    return out
ADDR=re.compile(r"((?:Via|Viale|V\.le|Piazza|P\.zza|Largo|Piazzale|Vicolo|Lungotevere|Circonvallazione|Corso|Borgo|Salita)\s+[A-Za-zÀ-ÿ'’.\s]{2,50}?,?\s*(?:n\.?\s*)?\d+[A-Za-z]?(?:/[A-Za-z0-9]+)?)[\s,–-]*(00[01]\d\d)\s*[-–,]?\s*Roma",re.I)
def verify(cf):
    e=E[cf]; m=M[cf]; out={'cf':cf}
    sig=[t for t in norm(e['core']).split() if t not in GENERIC and len(t)>1]; cn=norm(e['core'])
    for c in m['siti_candidati'][:4]:
        tries=[(c['sito'],'home')]+([(c['pagina'],'pagina')] if c['pagina'].rstrip('/')!=c['sito'] else [])
        for u,kind in tries:
            try: final,d=fetch(u)
            except Exception as ex: out.setdefault('errori',[]).append(f'{u}: {str(ex)[:50]}'); continue
            t=text(d); tn=norm(t); tc=tn.replace(' ','')
            cf_in = cf in re.sub(r'\D','',t)
            name_in = (cn and len(cn)>=6 and cn in tn) or (sig and not e['generico'] and sum(1 for x in sig if x in tn.split() or (len(x)>3 and x in tc))/len(sig)>=0.8)
            dom_ok = c['punteggio_dominio']>=0.5
            prova=None
            if kind=='home' and cf_in: prova='codice fiscale nella home del sito'
            elif dom_ok and cf_in: prova='codice fiscale nella pagina, dominio col nome'
            elif dom_ok and name_in and not e['generico']: prova='dominio col nome e nome nella pagina'
            if not prova: continue
            base=re.match(r'https?://[^/]+',final).group(0)
            out.update(sito=base,sito_prova=prova,sito_letto=final)
            links=[urllib.parse.urljoin(final,l) for l in re.findall(r'href=["\']([^"\'#]+)',d)]
            out['facebook_dal_sito']=next((fbclean(l) for l in links if re.match(r'https?://(www\.|m\.|it-it\.)?facebook\.com/(?!sharer|share|dialog|plugins|tr\b|events/|groups/|hashtag/|policy|privacy)[^/]+',l) and fbclean(l)),None)
            out['instagram_dal_sito']=next((re.sub(r'[?#].*$','',l).rstrip('/') for l in links if re.match(r'https?://(www\.)?instagram\.com/(?!p/|reel/|explore/)[^/]+',l)),None)
            a=ADDR.search(t); out['indirizzo_dal_sito']=f"{re.sub(r'\s+',' ',a.group(1)).strip()}, {a.group(2)} Roma" if a else None
            ev=[l for l in links if l.startswith(base) and EVWORDS.search(l)]
            out['pagina_eventi']=ev[0] if ev else None
            ds=dates(t); ld=ld_event_dates(d)
            if ev:
                try:
                    _,d2=fetch(ev[0]); t2=text(d2); ds|=dates(t2); ld+=ld_event_dates(d2)
                    if not out['indirizzo_dal_sito']:
                        a=ADDR.search(t2); out['indirizzo_dal_sito']=f"{re.sub(r'\s+',' ',a.group(1)).strip()}, {a.group(2)} Roma" if a else None
                except Exception: pass
            alld=set(ds)|set(ld)
            out['date_future']=sum(1 for x in alld if TODAY<=x<=date(2027,12,31)); out['date_6_mesi']=sum(1 for x in alld if SIX<=x<TODAY)
            out['eventi_jsonld']=len(ld); out['ultima_data']=max((x for x in alld if x<=date(2027,12,31)),default=None)
            out['ultima_data']=out['ultima_data'].isoformat() if out['ultima_data'] else None
            return out
    return out
todo=[cf for cf,m in M.items() if m['siti_candidati']]
print('enti con siti candidati',len(todo),flush=True)
res={}
with ThreadPoolExecutor(max_workers=24) as ex:
    for i,r in enumerate(ex.map(verify,todo)):
        res[r['cf']]=r
        if i%250==0: print(i,flush=True)
json.dump(res,open(f'{W}/{OUTF}','w'),ensure_ascii=False,indent=1)
ok=[r for r in res.values() if r.get('sito')]
print('siti verificati',len(ok),collections.Counter(r['sito_prova'] for r in ok),'con pagina eventi',sum(1 for r in ok if r.get('pagina_eventi')),'date future',sum(1 for r in ok if r.get('date_future')),'date 6 mesi',sum(1 for r in ok if r.get('date_6_mesi')),'fb dal sito',sum(1 for r in ok if r.get('facebook_dal_sito')),'indirizzo',sum(1 for r in ok if r.get('indirizzo_dal_sito')))

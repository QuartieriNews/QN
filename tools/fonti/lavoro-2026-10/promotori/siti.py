# Lettura dei siti dei promotori e dei canali degli eventi: anagrafica (descrizione, email, telefono, social) e posizione
# sulla diffusione (robots.txt, riserva TDM, clausole di note legali e termini d'uso). Una richiesta al secondo per host,
# robots.txt rispettato; i social e Roma Today non si leggono (termini Meta, licenza Citynews: DEC-026).
import json,re,urllib.request,urllib.parse,urllib.robotparser,gzip,time,html,collections,sys,ssl
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
UA="QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
NOFETCH=re.compile(r'(^|\.)(facebook\.com|fb\.me|instagram\.com|romatoday\.it|citynews|twitter\.com|x\.com|tiktok\.com|youtube\.com|linkedin\.com|google\.[a-z.]+|goo\.gl|linktr\.ee|wa\.me|whatsapp\.com)$')
def fetch(url,timeout=25,maxb=2_000_000):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'text/html,application/xhtml+xml,*/*;q=0.5','Accept-Language':'it-IT,it;q=0.9'})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        b=r.read(maxb)
        if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        cs=r.headers.get_content_charset() or (re.search(rb'charset=["\']?([\w-]+)',b[:3000]) or [None,b'utf-8'])[1].decode('ascii','ignore') or 'utf-8'
        try: t=b.decode(cs,'replace')
        except LookupError: t=b.decode('utf-8','replace')
        return r.geturl(),r.status,t
def text(d): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style|noscript|svg)[^>]*>.*?</\1>',' ',d,flags=re.S|re.I))))
def meta(d,name):
    m=re.search(r'<meta[^>]+(?:name|property)=["\']'+re.escape(name)+r'["\'][^>]*content=["\']([^"\']*)',d,re.I) or re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']'+re.escape(name)+r'["\']',d,re.I)
    return html.unescape(m.group(1)).strip() if m else None
EMAIL=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
SOCIAL={'facebook':r'facebook\.com/(?!sharer|share|dialog|plugins|tr\b|events/|groups/|hashtag)[^"\'\s<>?#]+','instagram':r'instagram\.com/(?!p/|reel/|explore)[^"\'\s<>?#/]+','youtube':r'youtube\.com/(?:@|channel/|c/|user/)[^"\'\s<>?#]+',
        'x':r'(?:twitter|x)\.com/(?!share|intent|home)[^"\'\s<>?#/]+','tiktok':r'tiktok\.com/@[^"\'\s<>?#/]+','linkedin':r'linkedin\.com/(?:company|in|school)/[^"\'\s<>?#/]+','telegram':r't\.me/[^"\'\s<>?#/]+'}
LINKS={'contatti':r'(^|/)(contatt\w*|contact(s|-us|o)?|dove-siamo|dovesiamo|recapiti)(/|$|\.html?$|\.php$)','chi_siamo':r'(^|/)(chi-?siamo|about(-us)?|la-nostra-storia|storia|mission|presentazione|l-?associazione|chi-e|cosa-facciamo|identita|la-parrocchia|il-comitato)(/|$|\.html?$|\.php$)','legale':r'(^|/)(note-?legali|legal\w*|termini\w*|condizioni\w*|terms\w*|copyright|disclaimer|crediti|credits|informazioni-legali|uso-del-sito|avvertenze)(/|$|\.html?$|\.php$)'}
CLAUSE={'riproduzione vietata':r"(è|e'|resta|risulta)?\s*(espressamente\s+|severamente\s+|assolutamente\s+)?vietat[ao]\s+(la|ogni|qualsiasi|qualunque)?\s*(riproduzione|copia|diffusione|pubblicazione|utilizzo|duplicazione)|riproduzione\s+(anche\s+parziale\s+)?(è\s+)?(vietata|riservata|non\s+consentita|proibita)|non\s+(è|e')\s+(consentit[ao]|permess[ao])\s+(la\s+)?(riproduzione|copia|diffusione|pubblicazione)|divieto\s+di\s+(riproduzione|copia|diffusione)|may\s+not\s+be\s+(reproduced|copied|republished)|reproduction\s+(is\s+)?(prohibited|forbidden)|senza\s+(il\s+)?(previo\s+|preventivo\s+)?(consenso|autorizzazione)\s+(scritt[ao]|espress[ao])?",
        'raccolta automatica vietata':r"scraping|estrazione\s+(automatica|sistematica)|text\s+and\s+data\s+mining|\bTDM\b|riserva\s+(dei\s+diritti\s+)?di\s+estrazione|data\s+mining|robot|crawler|spider",
        'licenza aperta':r"creative\s*commons|\bCC[ -]BY\b|licenza\s+(aperta|IODL|CC)|IODL|open\s*data|riutilizzo\s+(dei\s+contenuti\s+)?(è\s+)?(consentito|libero)|liberamente\s+(riproducibil|utilizzabil)",
        'diritti riservati (generico)':r"tutti\s+i\s+diritti\s+(sono\s+)?riservati|all\s+rights\s+reserved|©|&copy;|copyright"}
AIBOTS=('gptbot','ccbot','google-extended','claudebot','anthropic-ai','perplexitybot','bytespider','chatgpt-user','omgilibot','facebookbot','meta-externalagent','applebot-extended','amazonbot')
def robots_info(base):
    out={'robots':'assente','vieta_tutto':False,'bot_ia_bloccati':[]}
    try:
        _,st,t=fetch(base+'/robots.txt',timeout=15,maxb=300_000)
        if st!=200 or '<html' in t[:500].lower(): return out,None
        out['robots']='presente'; rp=urllib.robotparser.RobotFileParser(); rp.parse(t.splitlines())
        out['vieta_tutto']=not rp.can_fetch('*',base+'/') or not rp.can_fetch(UA,base+'/')
        cur=[]
        for l in t.splitlines():
            l=l.split('#')[0].strip(); low=l.lower()
            if low.startswith('user-agent:'): cur.append(low.split(':',1)[1].strip())
            elif low.startswith('disallow:'):
                if l.split(':',1)[1].strip()=='/':
                    out['bot_ia_bloccati']+= [a for a in cur if a in AIBOTS]
            elif low.startswith('allow:') or not low: pass
            if low.startswith(('disallow','allow')) and False: cur=[]
            if not low: cur=[]
        out['bot_ia_bloccati']=sorted(set(out['bot_ia_bloccati']))
        return out,rp
    except Exception: return out,None
def clauses(t,where,out):
    for k,rx in CLAUSE.items():
        for m in re.finditer(rx,t,re.I):
            s=t[max(0,m.start()-160):m.end()+160].strip()
            if k=='raccolta automatica vietata' and not re.search(r"vietat|non\s+(è|e')\s+consentit|proibit|riserv|divieto|prohibit|not\s+permitted|opt.?out",s,re.I): continue
            if k=='riproduzione vietata' and re.search(r"cookie|dati\s+personali|privacy",s,re.I) and not re.search(r"contenut|testi|immagin|foto|materiale|sito",s,re.I): continue
            out.setdefault(k,[]).append({'dove':where,'testo':s[:420]})
            break
def work(h):
    base='https://'+h; res={'host':h,'pagine':[],'errori':[]}
    if NOFETCH.search(h): res['esito']='non letto (piattaforma o licenza)'; return res
    rb,rp=robots_info(base); res.update(rb)
    def ok(u): return rp is None or rp.can_fetch(UA,u)
    if not ok(base+'/'): res['esito']='robots.txt vieta la lettura'; return res
    try: final,st,d=fetch(base+'/')
    except Exception as e:
        try: base='http://'+h; final,st,d=fetch(base+'/')
        except Exception as e2: res['esito']='non raggiungibile'; res['errori'].append(str(e2)[:80]); return res
    res['pagine'].append(final); t=text(d)
    res['titolo']=(re.search(r'<title[^>]*>(.*?)</title>',d,re.S|re.I) or [None,None])[1]
    res['titolo']=html.unescape(re.sub(r'\s+',' ',res['titolo'])).strip()[:200] if res['titolo'] else None
    res['descrizione_meta']=meta(d,'description'); res['og_description']=meta(d,'og:description'); res['og_site_name']=meta(d,'og:site_name')
    res['tdm_meta']=meta(d,'tdm-reservation'); res['robots_meta']=meta(d,'robots')
    hrefs=[urllib.parse.urljoin(final,x) for x in re.findall(r'href=["\']([^"\'#]+)',d)]
    res['email']=sorted({m.lower().strip('.') for m in EMAIL.findall(' '.join(hrefs)+' '+t) if not re.search(r'\.(png|jpe?g|gif|webp|svg)$|example|sentry|wixpress|@2x|domain\.com',m,re.I)})[:12]
    res['telefono']=sorted({re.sub(r'[^\d+]','',x) for x in re.findall(r'tel:([+\d\s./-]{6,})',d)})[:5]
    res['social']={k:sorted({re.sub(r'[/?#].*$','',m.split('.com/')[-1].split('t.me/')[-1]) for m in re.findall(rx,d,re.I)})[:3] for k,rx in SOCIAL.items()}
    res['social']={k:v for k,v in res['social'].items() if v}
    clauses(t[-4000:],'piè di pagina',res.setdefault('clausole',{}))
    basehost=urllib.parse.urlsplit(final).netloc
    pick={}
    for u in dict.fromkeys(hrefs):
        if urllib.parse.urlsplit(u).netloc!=basehost or re.search(r'\.(css|js|png|jpe?g|gif|svg|webp|pdf|ico|xml)(\?|$)|wp-content|wp-includes|/feed',u,re.I): continue
        path=urllib.parse.urlsplit(u).path.lower()
        for k,rx in LINKS.items():
            if k not in pick and re.search(rx,path): pick[k]=u
    for k,u in pick.items():
        if not ok(u): continue
        time.sleep(1)
        try: f2,st2,d2=fetch(u)
        except Exception as e: res['errori'].append(f'{k}: {str(e)[:60]}'); continue
        res['pagine'].append(f2); t2=text(d2)
        res['email']=sorted(set(res['email'])|{m.lower().strip('.') for m in EMAIL.findall(d2) if not re.search(r'\.(png|jpe?g|gif|webp|svg)$|example|sentry|wixpress',m,re.I)})[:15]
        if k=='chi_siamo':
            ps=[html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',x))).strip() for x in re.findall(r'<p[^>]*>(.*?)</p>',d2,re.S|re.I)]
            ps=[p for p in ps if len(p)>60 and not re.search(r'cookie|privacy|acceptButton|[{}]|javascript',p,re.I)]
            res['testo_chi_siamo']=' '.join(ps)[:2000] or meta(d2,'description')
        if k=='legale': clauses(t2,'note legali o termini: '+f2,res['clausole'])
    time.sleep(1)
    try:
        _,st3,t3=fetch(base+'/.well-known/tdmrep.json',timeout=10,maxb=50_000)
        res['tdmrep']=st3==200 and t3.strip().startswith(('[','{'))
    except Exception: res['tdmrep']=False
    res['esito']='letto'
    return res
if __name__=='__main__':
    hosts=json.load(open(f'{P}/hosts.json'))
    done={}
    try: done={r['host']:r for r in json.load(open(f'{P}/siti_letti.json'))}
    except Exception: pass
    todo=[h for h in hosts if h not in done]
    print('host da leggere',len(todo),flush=True)
    with ThreadPoolExecutor(max_workers=16) as ex: res=list(ex.map(work,todo))
    allr=list(done.values())+res
    json.dump(allr,open(f'{P}/siti_letti.json','w'),ensure_ascii=False,indent=0)
    print(collections.Counter(r['esito'] for r in allr))

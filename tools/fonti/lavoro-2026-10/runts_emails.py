# Email ufficiali degli enti: dal sito verificato (home + pagina contatti) e dalla pagina Facebook letta. Gratis.
import json,sys,re,html,gzip,glob,urllib.request,urllib.parse,collections
from concurrent.futures import ThreadPoolExecutor
S=sys.argv[1]; W=f'{S}/runts/work'
V=json.load(open(f'{W}/sites_all.json')); FB=json.load(open(f'{W}/fb.json'))['per_ente']; E=json.load(open(f'{W}/enti.json'))
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-fonti/1.0 (+contatto redazione)'
EMAIL=re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
BAD=re.compile(r'(example|esempio|sentry|wixpress|wix\.com|domain\.|yourdomain|tuodominio|email\.com$|\.png$|\.jpg$|\.jpeg$|\.gif$|\.webp$|\.svg$|@2x|u00|godaddy|squarespace|jimdo|wordpress\.com$|noreply|no-reply|donotreply|mailer-daemon|privacy@iubenda|iubenda)',re.I)
CONTACT=re.compile(r'(contatt|contact|chi-?siamo|about|dove-?siamo|info|segreteria|associazione)',re.I)
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept-Language':'it-IT,it;q=0.9','Accept':'text/html,*/*'})
    with urllib.request.urlopen(req,timeout=20) as r:
        b=r.read(1_500_000)
        if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        return r.geturl(), b.decode('utf-8','replace')
def cf_decode(h):
    try:
        k=int(h[:2],16); return ''.join(chr(int(h[i:i+2],16)^k) for i in range(2,len(h),2))
    except Exception: return None
def emails_in(d):
    found=[]
    for m in re.finditer(r'mailto:([^"\'?>\s]+)',d,re.I): found.append(urllib.parse.unquote(m.group(1)))
    for m in re.finditer(r'data-cfemail="([0-9a-f]+)"',d): 
        x=cf_decode(m.group(1)); 
        if x: found.append(x)
    t=html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d,flags=re.S|re.I)))
    t=re.sub(r'\s*\[\s*at\s*\]\s*|\s*\(\s*at\s*\)\s*|\s+at\s+(?=[a-z0-9.-]+\.[a-z]{2,}\b)','@',t,flags=re.I).replace('[dot]','.').replace('(dot)','.')
    found+=EMAIL.findall(t)
    out=[]
    for e in found:
        e=e.strip().strip('.,;:').lower()
        if EMAIL.fullmatch(e) and not BAD.search(e) and e not in out: out.append(e)
    return out
def work(cf):
    v=V.get(cf) or {}; site=v.get('sito'); res={'cf':cf,'sito_email':[],'pagine_lette':[]}
    if not site: return res
    try:
        final,d=fetch(site); res['pagine_lette'].append(final); res['sito_email']+=emails_in(d)
        base=re.match(r'https?://[^/]+',final).group(0)
        links=[urllib.parse.urljoin(final,l) for l in re.findall(r'href=["\']([^"\'#]+)',d)]
        cont=[l for l in dict.fromkeys(links) if l.startswith(base) and CONTACT.search(l.split(base,1)[1])][:2]
        for c in cont:
            try:
                _,d2=fetch(c); res['pagine_lette'].append(c)
                for e in emails_in(d2):
                    if e not in res['sito_email']: res['sito_email'].append(e)
            except Exception: pass
    except Exception as ex: res['errore']=str(ex)[:60]
    return res
todo=[e['cf'] for e in E if (V.get(e['cf']) or {}).get('sito')]
print('siti da leggere per le email',len(todo),flush=True)
out={}
with ThreadPoolExecutor(max_workers=24) as ex:
    for i,r in enumerate(ex.map(work,todo)):
        out[r['cf']]=r
        if i%500==0: print(i,flush=True)
json.dump(out,open(f'{W}/emails_sito.json','w'),ensure_ascii=False,indent=1)
print('siti con almeno una email',sum(1 for r in out.values() if r['sito_email']))

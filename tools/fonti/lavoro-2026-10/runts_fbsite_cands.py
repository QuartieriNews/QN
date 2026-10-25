# Candidati sito dalle pagine Facebook lette, per gli enti senza sito verificato -> match_fbsiti.json (stesso formato di match.json)
import json,sys,re,glob,urllib.parse
S=sys.argv[1]; W=f'{S}/runts/work'
FB=json.load(open(f'{W}/fb.json'))['per_ente']; V=json.load(open(f'{W}/sites.json'))
SOCIAL=re.compile(r'(facebook|instagram|tiktok|youtube|youtu\.be|linkedin|twitter|x\.com|wa\.me|t\.me|linktr\.ee|maps\.google|goo\.gl|bit\.ly|google\.com|paypal|gofundme|eventbrite)',re.I)
def key(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
P={}
for f in glob.glob(f'{W}/fb_pages/*.json'):
    for it in json.load(open(f)):
        for k in ('inputUrl','url','facebookUrl','pageUrl'):
            if it.get(k): P.setdefault(key(it[k]),it)
out={}
for cf,f in FB.items():
    if (V.get(cf) or {}).get('sito'): continue
    p=P.get(key(f['facebook'])) or {}
    ws=[w for w in ([p.get('website')]+list(p.get('websites') or [])) if w and isinstance(w,str) and not SOCIAL.search(w)]
    c=[]
    for w in dict.fromkeys(ws):
        if not w.startswith('http'): w='https://'+w.strip('/')
        host=urllib.parse.urlsplit(w).netloc.lower().replace('www.','')
        if host: c.append({'sito':f'https://{host}','pagina':w,'titolo':'sito indicato dalla pagina Facebook','punteggio':1.0,'punteggio_dominio':1.0})
    if c: out[cf]={'siti_candidati':c[:2]}
json.dump(out,open(f'{W}/match_fbsiti.json','w'),ensure_ascii=False,indent=1); print('enti con sito indicato da Facebook da verificare',len(out))

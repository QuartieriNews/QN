# Secondo giro: risultati della ricerca per codice fiscale -> candidati sito (da verificare) e pagine Facebook
import json,sys,re,glob,urllib.parse,collections,importlib.util
S=sys.argv[1]; W=f'{S}/runts/work'
spec=importlib.util.spec_from_file_location('mt',f'{W}/match.py')
src=open(f'{W}/match.py').read(); AGG=re.compile(re.search(r"AGG=re\.compile\(r'(.*?)',re\.I\)",src).group(1),re.I)
E={e['cf']:e for e in json.load(open(f'{W}/enti.json'))}
G={}
for f in glob.glob(f'{W}/g2_*.json'):
    for r in json.load(open(f)):
        q=r['searchQuery']['term'] if isinstance(r.get('searchQuery'),dict) else r.get('searchQuery')
        G.setdefault(q.strip('"'),[]).extend(r.get('organicResults') or [])
GENERIC={'associazione','culturale','sportiva','comitato','centro','gruppo','circolo','roma','di','del','della','dei','delle','il','la','le','lo','e','per','a','in','con','onlus','amici','fondazione','italia','italiana','nazionale','provinciale','regionale','lazio','sezione','territoriale','aps','odv','ets','asd','cooperativa','sociale','impresa','promozione','volontariato'}
import unicodedata
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
out={}; fbc={}; c=collections.Counter()
for cf,rs in G.items():
    e=E.get(cf)
    if not e: continue
    c['con risultati']+=bool(rs)
    sig=[t for t in norm(e['core']).split() if t not in GENERIC and len(t)>1]
    cands=[]
    for o in rs[:10]:
        u=o.get('url') or ''; host=urllib.parse.urlsplit(u).netloc.lower().replace('www.','')
        m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/([^/?#]+)/?$',u)
        if m and m.group(1).lower() not in ('events','groups','pages','people','profile.php','share'): fbc.setdefault(cf,f'https://www.facebook.com/{m.group(1)}'); continue
        if not host or AGG.search(host) or 'facebook' in host or 'instagram' in host: continue
        dn=re.sub(r'\.(it|com|org|eu|net|info)$','',host).replace('-','').replace('.','')
        sd=sum(1 for t in sig if len(t)>3 and t in dn)/len(sig) if sig else 0
        cands.append({'sito':f'https://{host}','pagina':u,'titolo':o.get('title'),'punteggio':1.0,'punteggio_dominio':max(sd,0.5) if sd>0 else 0.0})
    seen=set(); cands=[x for x in cands if not (x['sito'] in seen or seen.add(x['sito']))]
    if cands: out[cf]={'siti_candidati':cands[:4]}
json.dump(out,open(f'{W}/match_cf.json','w'),ensure_ascii=False,indent=1); json.dump(fbc,open(f'{W}/fb_da_cf.json','w'),ensure_ascii=False,indent=1)
print(dict(c),'enti con siti candidati',len(out),'facebook trovati per codice fiscale',len(fbc))

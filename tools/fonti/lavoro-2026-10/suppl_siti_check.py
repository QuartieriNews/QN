# Lettura dei siti dei candidati nuovi della lista supplementare (lettore della ricerca per quartiere: robots.txt rispettato,
# pagina eventi, eventi schema.org e blocchi datati, link alla pagina Facebook del sito)
import json,sys,re
from concurrent.futures import ThreadPoolExecutor
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,f'{S}/ricerca_quartieri'); sys.argv=['x']
import leggi_fonti as LF
L=json.load(open(f'{S}/supplementare/lista.json'))
def host(u): m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#]+)',str(u).strip().lower()); return m.group(1) if m else None
todo={}
for o in L:
    if o['gia_nota'] or not o.get('sito'): continue
    h=host(o['sito'])
    if not h or re.search(r'facebook|instagram|google|wikipedia|youtube|comune\.roma|chiesacattolica|parrocchiemap|linktr',h): continue
    todo.setdefault(h,{'fonte':h,'categoria':o['tipo'],'pagine_qn':o['pagina'],'ricerche':1,'url_esempio':o['sito'] if o['sito'].startswith('http') else 'https://'+o['sito']})
print('siti da leggere',len(todo),flush=True)
with ThreadPoolExecutor(max_workers=12) as ex: res=list(ex.map(LF.work,todo.values()))
json.dump(res,open(f'{S}/supplementare/siti_letti.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(r['esito'] for r in res),'con eventi schema.org',sum(1 for r in res if any(e['prova']=='jsonld' for e in r['eventi'])),'con date future',sum(1 for r in res if r['eventi']),'facebook trovati',sum(1 for r in res if r.get('facebook')))

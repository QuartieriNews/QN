# Biblioteche di Roma: dalla pagina elenco alle schede (nome, indirizzo) -> geocodifica -> mirate/bib.json
import re,sys,json,html,time,urllib.request
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/scripts')
from mirate_liste import geocode,place,cache,CACHE
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-fonti/1.0 (contatto redazione)'
lst=open(f'{S}/mirate/bib/list.html',encoding='utf-8',errors='replace').read()
links=sorted(set(re.findall(r'href="(https://www\.bibliotechediroma\.it/opac/library/[^"]+)"',lst)))
out=[]
for u in links:
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40) as r: d=r.read().decode('utf-8','replace')
    except Exception as e: print('x',u,str(e)[:50]); continue
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',d,flags=re.S))))
    name=html.unescape(re.search(r'<title>(.*?)</title>',d,re.S).group(1)).split('|')[0].strip() if re.search(r'<title>',d) else u.split('/')[-2]
    m=re.search(r'((?:Via|Viale|Largo|Piazza|Piazzale|Lungotevere|Vicolo|Corso)\s[A-Za-zÀ-ÿ\'’.\s]{3,60}?,?\s*\d+[A-Za-z]?)\b',t)
    addr=m.group(1).strip() if m else None
    rec={'tipo':'biblioteca','nome':name,'indirizzo':addr,'sito':u,'origine':'elenco Biblioteche di Roma (bibliotechediroma.it)'}
    if addr:
        g=geocode(f'{addr}, Roma')
        if g: lat,lon=float(g[0]['lat']),float(g[0]['lon']); rec.update(dict(zip(('municipio','sudd_nome','suddivisione'),place(lat,lon))),lat=lat,lon=lon)
    out.append(rec); time.sleep(1)
json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{S}/mirate/bib.json','w'),ensure_ascii=False,indent=1)
print('biblioteche',len(out),'con indirizzo',sum(1 for r in out if r['indirizzo']),'in Roma',sum(1 for r in out if r.get('municipio')))

# Elenchi ufficiali dei centri sociali anziani (PDF di comune.roma.it): nome, indirizzo, Municipio -> geocodifica -> mirate/csa.json
import re,sys,json,glob,subprocess,time,urllib.request,urllib.parse
S=sys.argv[1]; sys.path.insert(0,f'{S}/scripts')
from mirate_liste import geocode,place,cache,CACHE   # riusa cache e poligoni
ADDR=re.compile(r"^((?:Via|Viale|Largo|Piazza|Piazzale|Vicolo|Lungotevere|Circonvallazione|Strada|Corso|Borgo)\s+[A-Za-zÀ-ÿ'’.\s]+?(?:,\s*)?(?:\d+[A-Za-z]?|s\.?n\.?c\.?|snc))\b",re.I)
MUNRX=re.compile(r'MUNICIPIO\s+(?:ROMA\s+)?([IVX]+)\b',re.I)
out=[]
for f in sorted(glob.glob(f'{S}/mirate/csa/*.bin')):
    txt=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
    m=MUNRX.search(txt); mun=m.group(1).upper() if m else None
    prev=''
    for line in txt.splitlines():
        cols=[c for c in re.split(r'\s{2,}',line.strip()) if c]
        idx=next((i for i,c in enumerate(cols) if ADDR.match(c)),None)
        if idx is None: prev=cols[-1] if cols and not re.search(r'elenco|centri|municipio|indirizzo|telefono|quartiere|nome|\d{5} roma',line,re.I) else prev; continue
        name=cols[idx-1] if idx>0 else prev
        if not name or re.search(r'^\d|^roma$|^via |^viale ',name,re.I): prev=''; continue
        addr=re.sub(r'\s+',' ',ADDR.match(cols[idx]).group(1)).strip(); q=f'{addr}, Roma'
        rec={'tipo':'centro_anziani','nome':f'Centro sociale anziani {name.title()}','indirizzo':addr,'municipio_dichiarato':mun,'origine':'elenco ufficiale CSA di Municipio (comune.roma.it)','file':f.split('/')[-1]}
        d=geocode(q)
        if d: lat,lon=float(d[0]['lat']),float(d[0]['lon']); rec.update(dict(zip(('municipio','sudd_nome','suddivisione'),place(lat,lon))),lat=lat,lon=lon)
        out.append(rec); prev=''
json.dump(cache,open(CACHE,'w'),ensure_ascii=False); json.dump(out,open(f'{S}/mirate/csa.json','w'),ensure_ascii=False,indent=1)
print('centri',len(out),'geocodificati',sum(1 for r in out if r.get('lat')))
for r in out[:6]: print(' ',r['nome'],'|',r['indirizzo'],'|',r.get('municipio'),r.get('sudd_nome'))

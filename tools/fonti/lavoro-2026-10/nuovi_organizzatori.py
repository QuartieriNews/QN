# Dagli eventi Facebook letti per scoperta (keywords unseenuser + search apify) -> organizzatori distinti, confronto con lo schedario, geografia -> xlsx
import json,sys,re,glob,collections,unicodedata,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S=sys.argv[1]; OUT=sys.argv[2]
sys.path.insert(0,f'{S}/scripts')
MUN=json.load(open(f'{S}/geo/municipi.json'))['features']; SUD=json.load(open(f'{S}/geo/suddivisioni.json'))['features']
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); zones={z['publication_zone_id']:z for z in gz['publication_zones']}
def _pip(x,y,poly):
    ins=False; n=len(poly)
    for i in range(n):
        x1,y1=poly[i][:2]; x2,y2=poly[(i+1)%n][:2]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1+1e-12)+x1: ins=not ins
    return ins
def inside(lat,lon,g):
    polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    return any(_pip(lon,lat,p[0]) and not any(_pip(lon,lat,h) for h in p[1:]) for p in polys)
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
names={}
for n in gz['neighbourhoods']:
    for a in [n['name_display']]+re.split(r'[;|/]',n.get('aliases') or ''):
        if norm(a): names.setdefault(norm(a),n)
for z in gz['publication_zones']: names.setdefault(norm(z['name_display']),{'publication_zone_id':z['publication_zone_id'],'municipality_code':z['primary_municipality'],'publishable':z['is_page']})
def match(sd,mun):
    if not sd: return None
    c=norm(re.sub(r'^(quartiere|rione|zona|suburbio|borgata) ','',sd,flags=re.I)); w=c.split()
    for f in [c]+[' '.join(w[:k]) for k in range(len(w)-1,0,-1)]:
        n=names.get(f)
        if n and n.get('publishable',True) and (not mun or not n.get('municipality_code') or n['municipality_code']==mun): return n['publication_zone_id']
    return None
sched=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
known={}; fbkeys={}
for e in sched:
    for a in [e['nome']]+e['alias']: known[norm(a)]=e
    for k in e['chiavi']:
        if k.startswith('fb-page:'): fbkeys[k[8:]]=e
ev={}
for f in glob.glob(f'{S}/assoc/events_data/keywords_*.json')+glob.glob(f'{S}/assoc/events_data/fbsearch_*.json'):
    for i in json.load(open(f)):
        if not i.get('id') or i.get('id') in ev: continue
        if str(i.get('isPast') or i.get('is_past'))=='True': continue
        # due formati: unseenuser (snake) e apify (camel)
        if 'start_utc' in i:
            hosts=[(h.get('name'),h.get('url') or (f"https://www.facebook.com/{h['id']}" if h.get('id') else None)) for h in (i.get('hosts') or []) if isinstance(h,dict)]
            e={'id':i['id'],'nome':i.get('name'),'inizio':i.get('start_utc'),'lat':i.get('latitude'),'lon':i.get('longitude'),'luogo':i.get('location_name'),'citta':i.get('city'),'online':str(i.get('is_online'))=='True','url':i.get('url'),'origine':'parole chiave (unseenuser)'}
        else:
            loc=i.get('location') or {}
            hosts=[(h.get('name'),h.get('url')) for h in (i.get('organizators') or i.get('organizedBy') or []) if isinstance(h,dict)]
            e={'id':i['id'],'nome':i.get('name'),'inizio':i.get('utcStartDate') or i.get('startTime'),'lat':loc.get('latitude'),'lon':loc.get('longitude'),'luogo':loc.get('name'),'citta':loc.get('city'),'online':bool(i.get('isOnline')),'url':i.get('url'),'origine':'ricerca Facebook (apify)'}
        e['hosts']=[h for h in hosts if h[0]]
        try: lat,lon=float(e['lat']),float(e['lon'])
        except (TypeError,ValueError): lat=lon=None
        e['municipio']=next((x['properties'].get('numero_rom') for x in MUN if inside(lat,lon,x['geometry'])),None) if lat else None
        s=next((x['properties'] for x in SUD if inside(lat,lon,x['geometry'])),None) if lat else None
        e['zona']=match(s['DESCRIZIONE'],e['municipio']) if s else None
        ev[e['id']]=e
org=collections.defaultdict(lambda:{'eventi':[],'url':None})
for e in ev.values():
    for n,u in e['hosts']:
        o=org[n]; o['eventi'].append(e); o['url']=o['url'] or u
rows=[]
for n,o in org.items():
    slug=str(o['url'] or '').rstrip('/').split('/')[-1].lower()
    k=known.get(norm(n)) or fbkeys.get(slug)
    es=sorted(o['eventi'],key=lambda e:e['inizio'] or ''); roma=[e for e in es if e['municipio']]
    mun=collections.Counter(e['municipio'] for e in roma).most_common(1); zona=collections.Counter(e['zona'] for e in roma if e['zona']).most_common(1)
    rows.append({'organizzatore':n,'pagina_facebook':o['url'],'nello_schedario':k['id'] if k else 'NO (nuovo)','verdetto_schedario':(k.get('censimento') or {}).get('verdetto') if k else None,'decisione_registro':(k.get('registro') or {}).get('decisione') if k else None,
                 'eventi_futuri':len(es),'in_roma':len(roma),'online':sum(1 for e in es if e['online']),'prossimo':(es[0]['inizio'] or '')[:10],'municipio':mun[0][0] if mun else None,'zona_qn':zona[0][0] if zona else None,'zona_qn_nome':zones[zona[0][0]]['name_display'] if zona else None,
                 'luoghi':' · '.join(sorted({e['luogo'] for e in roma if e['luogo']})[:4]),'origine':' · '.join(sorted({e['origine'] for e in es})),'dove_cercare':(o['url'].rstrip('/')+'/events') if o['url'] else None})
rows.sort(key=lambda r:(r['nello_schedario']!='NO (nuovo)',-r['in_roma'],-r['eventi_futuri']))
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Organizzatori'; cols=list(rows[0].keys()); ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for r in rows: ws.append([r[c] for c in cols])
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=45 if c in ('organizzatore','pagina_facebook','luoghi','dove_cercare') else 16
ws.freeze_panes='A2'
we=wb.create_sheet('Eventi'); ec=['nome','inizio','luogo','citta','municipio','zona_qn','online','organizzatori','url','origine']; we.append(ec)
for c in we[1]: c.font=Font(bold=True)
for e in sorted(ev.values(),key=lambda e:e['inizio'] or ''): we.append([e['nome'],(e['inizio'] or '')[:16],e['luogo'],e['citta'],e['municipio'],e['zona'],'sì' if e['online'] else None,'; '.join(h[0] for h in e['hosts']),e['url'],e['origine']])
for i,c in enumerate(ec,1): we.column_dimensions[get_column_letter(i)].width=45 if c in ('nome','luogo','organizzatori','url') else 14
wr=wb.create_sheet('Riepilogo'); wr.append(['misura','valore'])
for c in wr[1]: c.font=Font(bold=True)
nuovi=[r for r in rows if r['nello_schedario']=='NO (nuovo)']
for k,v in [('eventi futuri distinti',len(ev)),('eventi a Roma (Municipio assegnato)',sum(1 for e in ev.values() if e['municipio'])),('con pagina QN',sum(1 for e in ev.values() if e['zona'])),('organizzatori distinti',len(rows)),('organizzatori nuovi rispetto allo schedario',len(nuovi)),('nuovi con almeno 2 eventi a Roma',sum(1 for r in nuovi if r['in_roma']>=2)),('zone QN con eventi',len({e['zona'] for e in ev.values() if e['zona']}))]: wr.append([k,v])
wr.column_dimensions['A'].width=50
wb.save(OUT); print({r[0]:r[1] for r in wr.iter_rows(min_row=2,values_only=True)})

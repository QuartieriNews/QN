# Simulazione geografica: se ogni ente facesse un evento nella pagina QN della sua sede, come cambierebbe la distribuzione degli eventi futuri per pagina?
import json,sys,collections,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S,OUT=sys.argv[1:3]; W=f'{S}/runts/work'
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); pages={z['publication_zone_id']:z for z in gz['publication_zones'] if z.get('is_page')}
# oggi: tutti gli eventi futuri noti al 24 ottobre (stessa base della pagina HTML: foglio unificato, culture.roma.it per differenza, siti, Facebook)
oggi=collections.Counter(e['z'] for e in json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi'] if e['z'] in pages)
R=json.load(open(f'{W}/rows.json'))
A=collections.Counter(r['zona_qn'] for r in R if r['zona_qn'] in pages and r['verdetto'].startswith('rientra'))
B=collections.Counter(r['zona_qn'] for r in R if r['zona_qn'] in pages and r['verdetto'].startswith(('rientra','da verificare')))
C=collections.Counter(r['zona_qn'] for r in R if r['zona_qn'] in pages and r['presenza_web']!='nessuna presenza web trovata')
import re
def fk(u):
    m=re.match(r'https?://(?:www\.)?facebook\.com/profile\.php\?id=(\d+)',u or '')
    if m: return m.group(1)
    m=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people/[^/]+/)?([^/?#]+)',u or ''); return m.group(1).lower() if m else None
runts_fb={fk(r['facebook']) for r in R if r['facebook'] and r['verdetto'].startswith('rientra')}
CE=json.load(open(f'{S}/assoc/rows.json'))
Dc=collections.Counter(r.get('zona_qn') for r in CE if r.get('zona_qn') in pages and str(r.get('verdetto','')).startswith('rientra') and fk(str(r['url_pagina']).replace('facebook.com/','www.facebook.com/')) not in runts_fb)
senza_geo={k:sum(1 for r in R if r['verdetto'].startswith(k) and not r['zona_qn']) for k in ('rientra','da verificare')}
def fascia(n): return '0' if n==0 else '1-4' if n<5 else '5-9' if n<10 else '10+'
deb=json.load(open(f'{S}/mirate/pagine_deboli.json'))
rows=[]
for z,p in pages.items():
    o=oggi.get(z,0); rows.append({'zona_qn':z,'pagina':p['name_display'],'municipio':p['primary_municipality'],'debole_al_24_ott':'sì' if z in deb else None,
        'eventi_futuri_oggi':o,'enti_rientrano':A.get(z,0),'enti_rientrano_o_da_verificare':B.get(z,0),'enti_con_presenza_web':C.get(z,0),
        'censimento_fb_rientrano':Dc.get(z,0),'scenario_A':o+A.get(z,0),'scenario_B':o+B.get(z,0),'scenario_C':o+A.get(z,0)+Dc.get(z,0),'fascia_oggi':fascia(o),'fascia_A':fascia(o+A.get(z,0)),'fascia_B':fascia(o+B.get(z,0)),'fascia_C':fascia(o+A.get(z,0)+Dc.get(z,0))})
rows.sort(key=lambda r:(r['eventi_futuri_oggi'],r['scenario_A'],r['pagina']))
F=['0','1-4','5-9','10+']
dist={k:collections.Counter(r[k] for r in rows) for k in ('fascia_oggi','fascia_A','fascia_B','fascia_C')}
out=openpyxl.Workbook(); w=out.active; w.title='Riepilogo'
w.append(['Simulazione: ogni ente fa un evento nella pagina QN della sua sede (24 ottobre 2026)']); w['A1'].font=Font(bold=True)
w.append(['Oggi = eventi futuri noti al 24 ottobre (foglio unificato, culture.roma.it per differenza, siti delle fonti, Facebook; stessa base della pagina HTML). Scenario A = più un evento per ogni ente RUNTS che rientra. Scenario B = più un evento anche per gli enti da verificare. Scenario C = A più le pagine Facebook del censimento del 24 ottobre che rientrano (senza doppioni).'])
w.append([]); w.append(['eventi futuri per pagina','pagine oggi','pagine scenario A','pagine scenario B','pagine scenario C'])
for c in w[4]: c.font=Font(bold=True)
for f in F: w.append([f,dist['fascia_oggi'][f],dist['fascia_A'][f],dist['fascia_B'][f],dist['fascia_C'][f]])
w.append([]); w.append(['pagine deboli (58, meno di 5 eventi il 24 ott)','oggi','scenario A','scenario B','scenario C'])
for c in w[w.max_row]: c.font=Font(bold=True)
dr=[r for r in rows if r['debole_al_24_ott']]
w.append(['ancora a zero',sum(1 for r in dr if r['eventi_futuri_oggi']==0),sum(1 for r in dr if r['scenario_A']==0),sum(1 for r in dr if r['scenario_B']==0),sum(1 for r in dr if r['scenario_C']==0)])
w.append(['ancora sotto 5',sum(1 for r in dr if r['eventi_futuri_oggi']<5),sum(1 for r in dr if r['scenario_A']<5),sum(1 for r in dr if r['scenario_B']<5),sum(1 for r in dr if r['scenario_C']<5)])
w.append(['arrivano a 10 o più',sum(1 for r in dr if r['eventi_futuri_oggi']>=10),sum(1 for r in dr if r['scenario_A']>=10),sum(1 for r in dr if r['scenario_B']>=10),sum(1 for r in dr if r['scenario_C']>=10)])
w.append([]); w.append(['enti che rientrano senza pagina QN (non contati)',senza_geo['rientra']]); w.append(['enti da verificare senza pagina QN (non contati)',senza_geo['da verificare']])
w.column_dimensions['A'].width=60
p=out.create_sheet('Per pagina'); cols=list(rows[0].keys()); p.append(cols)
for c in p[1]: c.font=Font(bold=True)
for r in rows: p.append([r[c] for c in cols])
for i,c in enumerate(cols,1): p.column_dimensions[get_column_letter(i)].width=22 if c=='pagina' else 14
p.freeze_panes='C2'
out.save(OUT)
print({k:dict(v) for k,v in dist.items()}); print('deboli a zero oggi/A/B/C',[sum(1 for r in dr if r[k]==0) for k in ('eventi_futuri_oggi','scenario_A','scenario_B','scenario_C')],'sotto 5',[sum(1 for r in dr if r[k]<5) for k in ('eventi_futuri_oggi','scenario_A','scenario_B','scenario_C')],'10+',[sum(1 for r in dr if r[k]>=10) for k in ('eventi_futuri_oggi','scenario_A','scenario_B','scenario_C')]); print('senza pagina QN',senza_geo)
json.dump(rows,open(f'{W}/simula.json','w'),ensure_ascii=False)

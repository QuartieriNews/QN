# Foglio della ricerca «evento / eventi / festa + quartiere» e registro fonti v4 (candidate nuove)
import json,re,glob,collections,unicodedata,openpyxl,sys
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; D=f'{S}/ricerca_quartieri'
rows=json.load(open(f'{D}/risultati.json')); dom=json.load(open(f'{D}/domini.json')); lette={r['fonte']:r for r in json.load(open(f'{D}/fonti_lette.json'))}
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); pages={z['publication_zone_id']:z for z in gz['publication_zones'] if z.get('is_page')}
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
FBE=collections.defaultdict(list)
for f in glob.glob(f'{D}/fb_events_*.json'):
    for x in json.load(open(f)):
        q=(x.get('_metadata') or {}).get('query') or ''
        m=re.search(r'profile\.php\?id=(\d+)',q) or re.search(r'facebook\.com/([^/?#]+)',q); FBE[m.group(1).lower() if m else q].append(x)
weak=json.load(open(f'{S}/mirate/pagine_deboli.json'))
out=[]
for d in dom:
    r=lette.get(d['fonte'],{}); slug=d['fonte'][3:] if d['fonte'].startswith('fb:') else None
    fe=[x for x in FBE.get(slug,[]) if str(x.get('is_past'))!='True'] if slug else []
    z=match(r.get('sudd_nome'),r.get('municipio')) if r.get('sudd_nome') else None
    zq=[x for x in d['pagine_qn'].split(', ') if x]
    zona=z or (zq[0] if len(set(zq))==1 else None); zmet='indirizzo della fonte' if z else ('unica pagina cercata' if zona else None)
    ej=sum(1 for e in r.get('eventi',[]) if e['prova']=='jsonld'); eb=len(r.get('eventi',[]))-ej
    if d['categoria'] in ('sito','istituzionale') and d['gia_nota']=='no':
        ver='candidata: eventi strutturati sul sito' if ej else 'candidata: date future sul sito' if eb else 'candidata: pagina eventi sul sito' if r.get('pagina_eventi') else ('robots.txt vieta la lettura' if r.get('esito','').startswith('robots') else 'nessun segnale di eventi' if r.get('esito')=='letto' else 'non raggiungibile' if r else 'non letta')
    elif d['categoria']=='Facebook: pagina' and d['gia_nota']=='no':
        ver='candidata: eventi futuri su Facebook' if fe else 'pagina Facebook senza eventi futuri'
    elif d['gia_nota']=='sì': ver='già nota'
    else: ver={'aggregatore di eventi':'aggregatore: non letto (licenza)','testata o blog':'testata o blog: fonte di notizie, non letta','commerciale (sale, catering, location)':'servizio commerciale: escluso','Facebook: gruppo':'gruppo Facebook: non leggibile','Instagram':'profilo Instagram: da valutare a mano'}.get(d['categoria'],d['categoria'])
    out.append({**d,'nome':r.get('nome'),'verdetto':ver,'pagina_eventi':r.get('pagina_eventi'),'eventi_strutturati':ej or None,'blocchi_datati':eb or None,'fb_eventi_futuri':len(fe) or None,
                'facebook_dal_sito':r.get('facebook'),'indirizzo':r.get('indirizzo'),'municipio':r.get('municipio') or (pages[zona]['primary_municipality'] if zona else None),'zona_qn':zona,'zona_metodo':zmet,'pagina_debole':'sì' if zona in weak else None})
FIL=json.load(open(f'{D}/filtro.json')) if __import__('os').path.exists(f'{D}/filtro.json') else {}
for o in out:
    if o['fonte'] in FIL and o['verdetto'].startswith('candidata'): o['verdetto']='escluso: '+FIL[o['fonte']]
st=collections.Counter(o['verdetto'] for o in out)
wb=openpyxl.Workbook(); w=wb.active; w.title='Riepilogo'; w.append(['misura','valore'])
for c in w[1]: c.font=Font(bold=True)
qs=sorted({r['query'] for r in rows})
for k,v in [('ricerche (evento, eventi, festa + nome del quartiere, 89 pagine, nomi doppi separati)',len(qs)),('risultati letti',len(rows)),('fonti distinte',len(out))]+[(f'categoria: {k}',v) for k,v in collections.Counter(o['categoria'] for o in out).most_common()]+[('',None)]+[(f'verdetto: {k}',v) for k,v in st.most_common()]: w.append([k,v])
cand=[o for o in out if o['verdetto'].startswith('candidata')]
w.append([]); w.append(['candidate con pagina QN',sum(1 for o in cand if o['zona_qn'])]); w.append(['candidate su pagine deboli (meno di 5 eventi al 24 ott)',sum(1 for o in cand if o['pagina_debole'])])
w.column_dimensions['A'].width=80
cols=['fonte','nome','categoria','verdetto','gia_nota','ricerche','risultati','pagine_qn','zona_qn','zona_metodo','municipio','pagina_debole','pagina_eventi','eventi_strutturati','blocchi_datati','fb_eventi_futuri','facebook_dal_sito','indirizzo','url_esempio','titolo_esempio']
ws=wb.create_sheet('Fonti'); ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for o in sorted(out,key=lambda o:(not o['verdetto'].startswith('candidata'),o['categoria'],-o['ricerche'])): ws.append([o.get(c) for c in cols])
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=40 if c in ('fonte','nome','verdetto','url_esempio','titolo_esempio','pagina_eventi','pagine_qn') else 13
ws.freeze_panes='B2'
wr=wb.create_sheet('Risultati'); rc=['query','pagine_qn','posizione','categoria','gia_nota','dominio','url','titolo','snippet']; wr.append(rc)
for c in wr[1]: c.font=Font(bold=True)
for r in rows: wr.append([r[c] for c in rc])
wp=wb.create_sheet('Per pagina QN'); wp.append(['zona_qn','pagina','municipio','debole','fonti candidate nuove','con eventi futuri'])
for c in wp[1]: c.font=Font(bold=True)
for z,p in sorted(pages.items(),key=lambda kv:kv[1]['name_display']):
    cz=[o for o in cand if o['zona_qn']==z]; wp.append([z,p['name_display'],p['primary_municipality'],'sì' if z in weak else None,len(cz),sum(1 for o in cz if o['eventi_strutturati'] or o['blocchi_datati'] or o['fb_eventi_futuri'])])
wb.save('/mnt/user-data/outputs/fonti_ricerca_quartieri.xlsx'); json.dump(out,open(f'{D}/fonti_classificate.json','w'),ensure_ascii=False)
# registro v4
rw=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v3.xlsx'); rs=rw.worksheets[0]; h=[c.value for c in rs[1]]
last=max(int(str(r[h.index('chiave')].value).split('-')[1]) for r in rs.iter_rows(min_row=2) if r[h.index('chiave')].value)
TIPO={'sito':'organizzatore','istituzionale':'istituzione','Facebook: pagina':'organizzatore'}
n=0
for o in cand:
    last+=1; fb=None; link=None
    if o['fonte'].startswith('fb:'):
        s=o['fonte'][3:]; fb=f'https://www.facebook.com/profile.php?id={s}' if s.isdigit() else f'https://www.facebook.com/{s}'
        dove=fb+('&sk=events' if s.isdigit() else '/events'); nome=o['titolo_esempio'].split(' | ')[0].split(' (@')[0][:80] if o['titolo_esempio'] else s
        nome=re.sub(r'\s*\|\s*Rome.*$','',nome)
    else:
        link='https://'+o['fonte']; dove=o['pagina_eventi'] or link; nome=o['nome'] or o['fonte']; fb=o['facebook_dal_sito']
    vals={'chiave':f'FE-{last:04d}','decisione':'candidata','nome':nome,'tipo':TIPO.get(o['categoria'],'altro'),'zona_qn':o['zona_qn'],'municipio':o['municipio'],'sotto_soglia':'sì' if o['pagina_debole'] else None,
          'canale':'facebook' if o['fonte'].startswith('fb:') else 'sito','link':link,'facebook':fb,'instagram':None,'origine':'ricerca_quartieri_2026-10-24','eventi_visti':(o['eventi_strutturati'] or 0)+(o['blocchi_datati'] or 0)+(o['fb_eventi_futuri'] or 0) or None,
          'motivo':o['verdetto']+(f" · zona: {o['zona_metodo']}" if o['zona_metodo'] else ''),'dove_cercare':dove}
    rs.append([vals.get(c) for c in h]); n+=1
rw.save('/mnt/user-data/outputs/registro_fonti_v4.xlsx')
print(dict(st)); print('candidate',len(cand),'nel registro v4',n,'con zona',sum(1 for o in cand if o['zona_qn']),'su pagine deboli',sum(1 for o in cand if o['pagina_debole']))

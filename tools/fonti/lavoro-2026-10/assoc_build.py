import json,sys,re,unicodedata,collections
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S,GAZ,OUT,REG=sys.argv[1:5]
pages=json.load(open(f'{S}/assoc/pages_enriched.json')); sites=json.load(open(f'{S}/assoc/sites.json')); geo=json.load(open(f'{S}/assoc/geo.json')); evs=json.load(open(f'{S}/assoc/events.json')) if __import__('os').path.exists(f'{S}/assoc/events.json') else {}; posts=json.load(open(f'{S}/assoc/posts.json')) if __import__('os').path.exists(f'{S}/assoc/posts.json') else {}
gz=json.load(open(GAZ)); zones={z['publication_zone_id']:z for z in gz['publication_zones']}
def norm(s):
    s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower(); s=re.sub(r"\bs\.\s*",'san ',s); return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
names={}
for n in gz['neighbourhoods']:
    for a in [n['name_display']]+re.split(r'[;|/]',n.get('aliases') or ''):
        if norm(a): names.setdefault(norm(a),n); names.setdefault(norm(a).replace(' ',''),n)
for z in gz['publication_zones']: names.setdefault(norm(z['name_display']),{'publication_zone_id':z['publication_zone_id'],'municipality_code':z['primary_municipality'],'publishable':z['is_page']})
def match(c0,mun):
    if not c0: return None
    forms=[norm(c0),norm(c0).replace(' ','')]
    for part in re.split(r'\s*[-–/]\s*|\s+e\s+',c0): forms+=[norm(part),norm(part).replace(' ','')]
    w=norm(c0).split()
    for k in range(len(w)-1,0,-1): forms.append(' '.join(w[:k]))
    forms.append(re.sub(r'^(quartiere|rione|zona|borgata|lido di) ','',norm(c0)))
    if norm(c0)=='europa': forms.append('eur')
    for f in forms:
        n=names.get(f)
        if n and n.get('publishable',True) and (not mun or not n.get('municipality_code') or n['municipality_code']==mun): return n['publication_zone_id']
    return None
reg=openpyxl.load_workbook(REG).worksheets[0]; rr=list(reg.iter_rows(values_only=True)); rh=rr[0]
def slug(u): return re.sub(r'^https?://(www\.)?facebook\.com/','',str(u or '')).strip('/').lower()
regby={slug(r[rh.index('facebook')]):r for r in rr[1:] if r[rh.index('facebook')]}
SERVIZI=re.compile(r'psych|psico|medical|health|lawyer|legal|tax|consult|business service|labor union|trade union|trade association|professional association|insurance|product/service|^company$|travel agent|property|counsel|plumbing|florist|beauty|pet service|shopping|retail|tutor|genealog|computer training|dentist|veterinar|accountant|real estate|finance|bank|software|marketing|advertising',re.I)
COMUNITA=re.compile(r'nonprofit|non-profit|community|cultural|education|school|arts|theat|library|religio|church|parish|sport|event planner|charity|social service|ngo|environment|youth|social club|music school|cinema|art gallery|performing|circus|museum|organization|organisation|amateur sports|dance|recreation|public and government|government',re.I)
POLITICA=re.compile(r'politic',re.I)
NAZ=re.compile(r'\b(nazionale|italiana|italiani|italia|internazionale|europea|europe|federazione|sindacato|ordine dei|consiglio nazionale|confederazione)\b',re.I)
LOCALE=re.compile(r'\b(roma|quartiere|municipio|rione|borgata|zona|comitato|parrocchia|biblioteca|centro anziani|pro loco|istituto comprensivo|scuola)\b',re.I)
rows=[]; stats=collections.Counter()
for p in pages:
    d=p.get('dati'); st=sites.get(p['url']) or {}; g=geo.get(p['url']) or {}
    r={'url_pagina':p['url'],'nome':p['nome'],'tipo_facebook':p['tipo'],'nel_registro_13_ott':(regby.get(slug(p['url'])) or [None]*len(rh))[rh.index('decisione')] if slug(p['url']) in regby else None}
    if not d: r['stato']='non letta'; r['verdetto']='da leggere'; r['motivo']='pagina non restituita dal lettore Apify'; rows.append(r); stats[r['verdetto']]+=1; continue
    if d.get('error'): r['stato']='pagina non disponibile'; r['verdetto']='scartare'; r['motivo']='Facebook: contenuto non disponibile o rimosso'; rows.append(r); stats[r['verdetto']]+=1; continue
    r['stato']='letta'
    cat=d.get('category') or ''; r.update({'categoria_facebook':cat,'follower':d.get('followers'),'pagina_creata':d.get('creation_date'),'email':d.get('email'),'telefono':d.get('phone'),'indirizzo':d.get('address'),'intro':(d.get('intro') or '')[:200]})
    r.update({'sito':st.get('sito'),'sito_esito':st.get('esito'),'sito_pagina_eventi':st.get('pagina_eventi'),'sito_eventi_jsonld':st.get('jsonld_eventi'),'sito_date_future':st.get('date_future_nel_sito'),'sito_date_ultimi_6_mesi':st.get('date_ultimi_6_mesi'),'sito_ultima_data':st.get('ultima_data_vista')})
    e=evs.get(p['url']) or {}
    if not g and e.get('municipio_prevalente'): g={'lat':e['lat'],'lon':e['lon'],'fonte':'coordinate degli eventi Facebook','municipio':e['municipio_prevalente'],'suddivisione':None,'sudd_nome':e.get('suddivisione_prevalente')}
    mun=g.get('municipio'); sd=g.get('sudd_nome'); zona=match(sd,mun) if sd else None
    po=posts.get(p['url']) or {}
    r.update({'fb_post_6_mesi':po.get('post') if p['url'] in posts else None,'fb_ultimo_post':(po.get('ultimo') or '')[:10] or None,'fb_post_con_eventi':po.get('post_eventi') if p['url'] in posts else None,'fb_post_esempio':(po.get('esempi') or [None])[0]})
    r.update({'fb_eventi_futuri':e.get('eventi_futuri',0) if evs else None,'fb_eventi_in_roma':e.get('in_roma') if e else None,'fb_prossimo_evento':(e.get('prossimo') or '')[:10] or None,'fb_municipi_eventi':', '.join(e.get('municipi') or []) or None})
    r.update({'lat':g.get('lat'),'lon':g.get('lon'),'geo_fonte':g.get('fonte'),'municipio':mun,'suddivisione_ufficiale':g.get('suddivisione'),'zona_qn':zona,'zona_qn_nome':zones.get(zona,{}).get('name_display') if zona else None})
    fuori = bool(g) and not mun
    addr=(d.get('address') or '')
    if fuori and 'Rome' not in addr: v,m='fuori Roma',f"indirizzo fuori dai Municipi: {addr[:60]}"
    elif SERVIZI.search(cat) and not (st.get('date_future_nel_sito') or st.get('pagina_eventi')): v,m='servizio o professione','categoria Facebook di servizio o professione, nessun calendario sul sito'
    elif POLITICA.search(cat): v,m='da valutare: politica','organizzazione politica: iniziative pubbliche sì, propaganda no (decisione editoriale)'
    elif NAZ.search(p['nome']) and not LOCALE.search(p['nome']) and not zona: v,m='tematico non locale','nome di ente nazionale o tematico senza radicamento di quartiere'
    elif e.get('in_roma'): v,m='rientra: eventi futuri su Facebook',f"{e['in_roma']} eventi futuri a Roma sulla pagina Facebook (prossimo {(e.get('prossimo') or '')[:10]})"
    elif e.get('eventi_futuri'): v,m='da valutare: eventi futuri fuori Roma o online',f"{e['eventi_futuri']} eventi futuri su Facebook, nessuno localizzato a Roma"
    elif COMUNITA.search(cat) or 'Local business' in cat or 'Event' in cat:
        if st.get('date_future_nel_sito') or st.get('eventi_jsonld_futuri'): v,m='rientra: attiva, calendario sul sito','il sito mostra date future'
        elif st.get('date_ultimi_6_mesi'): v,m='rientra: attiva negli ultimi 6 mesi (sito)','il sito mostra date degli ultimi sei mesi'
        elif st.get('pagina_eventi'): v,m='rientra: pagina eventi sul sito, attività da verificare','sito con sezione eventi ma senza date leggibili'
        elif po.get('post_eventi'): v,m='rientra: annuncia eventi nei post Facebook',f"{po['post_eventi']} post con data e annuncio di evento negli ultimi 6 mesi (ultimo post {(po.get('ultimo') or '')[:10]})"
        elif 'Local business' in cat and po.get('post'): v,m='locale: attiva su Facebook, senza annunci di eventi',f"attività commerciale; {po['post']} post negli ultimi 6 mesi, nessuno con data e annuncio"
        elif 'Local business' in cat: v,m='locale: solo se organizza eventi','attività commerciale; nessun evento futuro né post recente su Facebook'
        elif po.get('post'): v,m='attiva su Facebook, senza annunci di eventi',f"{po['post']} post negli ultimi 6 mesi, nessuno con data e annuncio di evento; nessuna data sul sito"
        elif evs: v,m='dormiente: nessun evento futuro, nessun post recente, nessun calendario sul sito','soggetto di comunità; nessun evento futuro né post negli ultimi 6 mesi sulla pagina Facebook, nessuna data sul sito'
        else: v,m='rientra: verificare eventi Facebook','soggetto di comunità senza sito leggibile; la prova sta negli eventi Facebook (lettura Apify)'
    elif po.get('post_eventi'): v,m='da valutare: annuncia eventi nei post Facebook',f"categoria {cat}; {po['post_eventi']} post con data e annuncio di evento negli ultimi 6 mesi"
    else: v,m='da valutare',f'categoria non classificata: {cat}'
    r['verdetto'],r['motivo']=v,m
    dove=[]
    if st.get('pagina_eventi'): dove.append(st['pagina_eventi'])
    elif st.get('sito'): dove.append(st['sito'])
    sl=slug(p['url']); dove.append(f'https://www.facebook.com/{sl}/events' if not re.fullmatch(r'\d+',sl) else f'https://www.facebook.com/profile.php?id={sl}&sk=events')
    r['dove_cercare']=' · '.join(dove)
    rows.append(r); stats[v]+=1
cols=['url_pagina','nome','tipo_facebook','stato','verdetto','motivo','dove_cercare','fb_eventi_futuri','fb_eventi_in_roma','fb_prossimo_evento','fb_municipi_eventi','fb_post_6_mesi','fb_ultimo_post','fb_post_con_eventi','fb_post_esempio','municipio','zona_qn','zona_qn_nome','suddivisione_ufficiale','indirizzo','categoria_facebook','follower','pagina_creata','email','telefono','sito','sito_esito','sito_pagina_eventi','sito_date_future','sito_date_ultimi_6_mesi','sito_ultima_data','sito_eventi_jsonld','lat','lon','geo_fonte','nel_registro_13_ott','intro']
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Pagine'; ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for r in rows: ws.append([r.get(c) for c in cols])
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=50 if c in ('dove_cercare','motivo','nome','url_pagina') else 18
ws.freeze_panes='A2'
wr=wb.create_sheet('Riepilogo'); wr.append(['verdetto','pagine']); 
for c in wr[1]: c.font=Font(bold=True)
for k,v in stats.most_common(): wr.append([k,v])
wr.append([]); wr.append(['municipio (pagine lette e geocodificate)','pagine','di cui rientrano']); 
bym=collections.Counter(r.get('municipio') for r in rows if r.get('municipio')); bymr=collections.Counter(r.get('municipio') for r in rows if r.get('municipio') and str(r.get('verdetto','')).startswith('rientra'))
for m in ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']: wr.append([m,bym.get(m,0),bymr.get(m,0)])
wr.column_dimensions['A'].width=55
we=wb.create_sheet('Eventi futuri Facebook'); we.append(['pagina','nome_pagina','evento','inizio','luogo','indirizzo','municipio','suddivisione_ufficiale','online','host','biglietti','interessati','partecipano','url_evento'])
for c in we[1]: c.font=Font(bold=True)
nm={p['url']:p['nome'] for p in pages}
for u,e in sorted(evs.items(), key=lambda kv: kv[1]['prossimo'] or ''):
    for x in e['eventi']: we.append([u,nm.get(u),x['nome'],(x['inizio'] or '')[:16].replace('T',' '),x['luogo'],x['indirizzo'],x['municipio'],x['suddivisione'],'sì' if x['online'] else None,x['host'],x['biglietti'],x['interessati'],x['partecipano'],x['url']])
for i,w in enumerate([40,35,45,16,30,40,10,25,8,35,30,10,10,45],1): we.column_dimensions[get_column_letter(i)].width=w
we.freeze_panes='A2'
wn=wb.create_sheet('Da leggere (Apify)'); wn.append(['url_pagina','nome','tipo_facebook'])
for r in rows:
    if r['stato'].startswith('non letta'): wn.append([r['url_pagina'],r['nome'],r['tipo_facebook']])
wn.column_dimensions['A'].width=55; wn.column_dimensions['B'].width=50
wb.save(OUT); print(stats.most_common()); print('rientrano per municipio:',sorted(bymr.items())); print('zone QN coperte dalle pagine che rientrano:',len({r.get('zona_qn') for r in rows if r.get('zona_qn') and str(r.get('verdetto','')).startswith('rientra')}))
json.dump(rows,open(f'{S}/assoc/rows.json','w'),ensure_ascii=False,indent=1)

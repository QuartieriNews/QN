# Foglio dei promotori (Drive): anagrafica completa, categorie, lacune per pagina debole, posizione sulla diffusione, metodo
import json,re,collections,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
R=json.load(open(f'{P}/promotori_finale.json')); E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
GZ=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); PAGES={z['publication_zone_id']:z['name_display'] for z in GZ['publication_zones'] if z['is_page']}
TG=json.load(open(f'{S}/supplementare/pagine_target.json')); T={r['id'] for r in TG}
L=json.load(open(f'{S}/supplementare/lista.json'))
SL={r['host']:r for r in json.load(open(f'{P}/siti_letti.json'))}
IDEE=json.load(open(f'{P}/idee.json')) if __import__('os').path.exists(f'{P}/idee.json') else []
wb=openpyxl.Workbook(); bold=Font(bold=True)
def sheet(title,cols,rows,widths=None,first=False):
    ws=wb.active if first else wb.create_sheet(title); ws.title=title; ws.append(cols)
    for c in ws[1]: c.font=bold
    for r in rows: ws.append([', '.join(map(str,v)) if isinstance(v,(list,tuple,set)) else (json.dumps(v,ensure_ascii=False) if isinstance(v,dict) else v) for v in r])
    for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(c,16)
    ws.freeze_panes='B2'; ws.auto_filter.ref=ws.dimensions
    return ws
cols=['nome','categoria','sottocategoria','ambito','descrizione_breve','descrizione_lunga','attivita','pubblico','n_eventi','in_pagine_deboli','pagine_qn','municipi',
      'email_principale','email_altre','pec','telefono','sito','facebook','instagram','youtube','x','tiktok','linkedin','indirizzo','zona_sede','municipio_sede',
      'follower','sezione_runts','temi_runts','codice_fiscale','categorie_facebook','categoria_google','diffusione','diffusione_prova','diffusione_testo','bot_ia_bloccati',
      'wiki','canali_da_ricerca','via','src','altri_nomi','autodescrizione_fonte','categoria_da']
W={'nome':40,'descrizione_breve':60,'descrizione_lunga':90,'email_principale':32,'email_altre':40,'sito':36,'facebook':36,'instagram':30,'indirizzo':40,'diffusione_testo':60,'diffusione_prova':40,'pagine_qn':30}
rows=[]
for r in sorted(R,key=lambda r:(-r['n_eventi'],r['nome'].lower())):
    d=dict(r); d['email_principale']=r['email'][0] if r['email'] else None; d['email_altre']=r['email'][1:4]
    d['pagine_qn']=', '.join(f"{PAGES.get(z,z)} ({n})" for z,n in sorted(r['pagine_qn'].items(),key=lambda kv:-kv[1])); d['municipi']=', '.join(f"{m} ({n})" for m,n in sorted(r['municipi'].items(),key=lambda kv:-kv[1]))
    d['zona_sede']=PAGES.get(r.get('zona_sede'),r.get('zona_sede'))
    rows.append([d.get(c) for c in cols])
ws=sheet('Promotori',cols,rows,W,first=True)
for row in ws.iter_rows(min_row=2):
    row[cols.index('descrizione_lunga')].alignment=Alignment(wrap_text=False)
# categorie
cat=collections.defaultdict(list)
for r in R: cat[r['categoria']].append(r)
crow=[]
for c,rs in sorted(cat.items(),key=lambda kv:-sum(r['n_eventi'] for r in kv[1])):
    ev=sum(r['n_eventi'] for r in rs); evw=sum(r['in_pagine_deboli'] for r in rs)
    crow.append([c,len(rs),ev,round(ev/len(rs),1),evw,f"{100*evw//ev if ev else 0}%",sum(1 for r in rs if r.get('zona_sede') in T),
                 f"{100*sum(1 for r in rs if r['email'])//len(rs)}%",f"{100*sum(1 for r in rs if r.get('sito'))//len(rs)}%",f"{100*sum(1 for r in rs if r.get('facebook'))//len(rs)}%",
                 ', '.join(f"{k} {v}" for k,v in collections.Counter(s for r in rs for s in [r['sottocategoria']] if s).most_common(4)),
                 ', '.join(f"{k} {v}" for k,v in collections.Counter(r['diffusione'] for r in rs).most_common(3))])
sheet('Categorie',['categoria','promotori','eventi','eventi per promotore','eventi nelle 41 pagine deboli','quota pagine deboli','promotori con sede in pagina debole','con email','con sito','con Facebook','sottocategorie principali','diffusione'],crow,{'categoria':42,'sottocategorie principali':60,'diffusione':60})
# pagine deboli x categorie: chi c'è (lista supplementare) e chi produce eventi (promotori)
TYPMAP={'comitato di quartiere o civico':'Comitati di quartiere e reti civiche','parrocchia o chiesa cattolica':'Parrocchie e realtà religiose','comunità religiosa':'Parrocchie e realtà religiose',
        'centro anziani':'Centri sociali, centri anziani e spazi di comunità','centro sociale, anziani o di quartiere':'Centri sociali, centri anziani e spazi di comunità',
        'luogo culturale (teatro, biblioteca, centro arti)':'Teatri, cinema e spazi di spettacolo','sport':'Sport e movimento','scout':'Associazioni culturali e artistiche','associazione':'Associazioni culturali e artistiche'}
prow=[]; MAIN=['Associazioni culturali e artistiche','Parrocchie e realtà religiose','Comitati di quartiere e reti civiche','Centri sociali, centri anziani e spazi di comunità',
               'Sport e movimento','Teatri, cinema e spazi di spettacolo','Istituzioni pubbliche','Terzo settore sociale e sanitario']
for t in sorted(TG,key=lambda r:-r['mancanti_a_quartiere_attivo']):
    z=t['id']; act=collections.Counter(); exi=collections.Counter()
    for r in R:
        if r['pagine_qn'].get(z): act[r['categoria']]+=1
    for o in L:
        if o['pagina']==z: exi[TYPMAP.get(o['tipo'],'Associazioni culturali e artistiche')]+=1
    prow.append([t['pagina'],t['municipio'],t['abitanti_stimati'],t['eventi'],t['mancanti_a_quartiere_attivo']]+[f"{act.get(m,0)} / {exi.get(m,0)}" for m in MAIN])
tot_act=collections.Counter(); tot_exi=collections.Counter()
for t in TG:
    z=t['id']
    for r in R:
        if r['pagine_qn'].get(z): tot_act[r['categoria']]+=1
    for o in L:
        if o['pagina']==z: tot_exi[TYPMAP.get(o['tipo'],'Associazioni culturali e artistiche')]+=1
quota={}
for c,rs in cat.items():
    ev=sum(r['n_eventi'] for r in rs); quota[c]=round(100*sum(r['in_pagine_deboli'] for r in rs)/ev) if ev else 0
json.dump({'categorie':MAIN,'attivi':dict(tot_act),'esistenti':dict(tot_exi),'quota_eventi_in_pagine_deboli':quota},open(f'{P}/deboli_categorie.json','w'),ensure_ascii=False,indent=1)
sheet('Pagine deboli x categorie',['pagina','municipio','abitanti','eventi','mancanti per quartiere attivo']+[f'{m} (attivi / esistenti)' for m in MAIN],prow,{'pagina':22})
# diffusione per fonte o canale
import sys; sys.path.insert(0,P); import diritti as D
drow=[]
for h,sr in sorted(SL.items()):
    lab,prova,testo=D.position(sr)
    drow.append([h,sr.get('esito'),lab,prova,testo,sr.get('robots'),'sì' if sr.get('vieta_tutto') else 'no',', '.join(sr.get('bot_ia_bloccati') or []),'sì' if (sr.get('tdm_meta')=='1' or sr.get('tdmrep')) else 'no','; '.join(sr.get('clausole') or {})])
for h,(lab,prova,why) in D.MANUALE.items():
    if not any(x[0]==h or x[0].endswith('.'+h) for x in drow): drow.append([h,'caso documentato',lab,prova,why,None,None,None,None,None])
sheet('Diffusione per fonte',['host','esito lettura','posizione','dove','testo della clausola','robots.txt','robots vieta tutto','bot IA bloccati','riserva TDM','clausole trovate'],drow,{'host':32,'dove':40,'testo della clausola':90})
if IDEE: sheet('Ricerche integrative',list(IDEE[0].keys()),[list(i.values()) for i in IDEE],{'idea':40,'perché':70,'esito':60})
m=wb.create_sheet('Metodo')
for t in [f'Promotori: chi organizza i {format(len(E),",").replace(",",".")} eventi futuri della pagina «Eventi dei quartieri» (25 ottobre 2026): host degli eventi Facebook (con il link alla pagina), pagina che annuncia nel post, «a cura di» di culture.roma.it, la sede per l\'agenda delle Biblioteche di Roma, la fonte per i siti; co-organizzatori separati; Roma Today senza promotore dichiarato escluso.',
          'Dati: profili Facebook già letti (censimenti, pagine dell\'owner) e letti ora per le pagine mancanti; RUNTS (email, PEC, temi, sezione); censimento associazioni; lista supplementare; contatti per evento di culture.roma.it; siti letti ora (homepage, contatti, chi siamo, note legali; robots.txt rispettato); ricerca Google dei canali per chi non ne aveva.',
          'Email: prima quelle del profilo Facebook o del RUNTS, poi quelle del sito con lo stesso dominio, poi le caselle personali (gmail, libero…); escluse caselle tecniche e segnaposto. PEC a parte.',
          'Categorie: 17 macro-categorie con sottocategoria, da regole sul nome, poi categorie Facebook o Google, tipo nel registro, temi RUNTS; «categoria_da» dice quale segnale ha deciso.',
          'Descrizione breve: scritta da regole con le nostre etichette (forma giuridica, sede, attività prevalenti dai titoli degli eventi e dalla presentazione, pubblico); va nella wiki. Descrizione lunga: identità, sede, attività, temi RUNTS, eventi nel calendario, presenza online e, tra virgolette, come il soggetto si presenta (profilo Facebook o sito): resta su Drive (DEC-102, DEC-109).',
          'Diffusione: dal sito del promotore (clausole nelle note legali o nel piè di pagina, robots.txt, riserva di estrazione TDM); per chi ha solo Facebook valgono i termini di Meta; Roma Today richiede licenza (DEC-026). I fatti di un evento (cosa, quando, dove) non sono protetti dal diritto d\'autore: lo sono i testi e le immagini, e una banca dati da estrazioni sistematiche.',
          'Pagine deboli x categorie: per ogni pagina, promotori attivi nel calendario / soggetti esistenti trovati nella lista supplementare, per categoria.']:
    m.append([t])
m.column_dimensions['A'].width=180
wb.save('/mnt/user-data/outputs/promotori_eventi.xlsx')
print('ok',len(R))

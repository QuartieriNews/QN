# Foglio della lista supplementare per le pagine QN deboli
import json,re,sys,collections,openpyxl
from openpyxl.styles import Font,PatternFill
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/supplementare')
from noti import fbk,toks
src=open(f'{S}/supplementare/eventi_suppl.py').read(); exec(src[src.index('ENTE=re.compile'):src.index('for o in L:')])   # ENTE, soggetto
L=json.load(open(f'{S}/supplementare/lista.json')); E=json.load(open(f'{S}/supplementare/eventi_suppl.json'))
T={r['id']:r for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}
nev=collections.Counter(e['fonte'] for e in E)
for o in L: o['ente']=soggetto(o); o['eventi_futuri_trovati']=nev.get(o['nome'],0)
N=[o for o in L if not o['gia_nota'] and o['ente']]
wb=openpyxl.Workbook(); w=wb.active; w.title='Riepilogo per pagina'
TY=['comitato di quartiere o civico','associazione','parrocchia o chiesa cattolica','centro anziani','centro sociale, anziani o di quartiere','luogo culturale (teatro, biblioteca, centro arti)','sport','scout','comunità religiosa']
hdr=['pagina','municipio','abitanti_stimati','eventi_prima','mancanti_a_quartiere_attivo','soggetti_nuovi']+TY+['con_facebook','con_sito','con_eventi_futuri','eventi_futuri_trovati']
w.append(hdr)
for c in w[1]: c.font=Font(bold=True)
for z,r in sorted(T.items(),key=lambda kv:-kv[1]['mancanti_a_quartiere_attivo']):
    n=[o for o in N if o['pagina']==z]; ct=collections.Counter(o['tipo'] for o in n)
    w.append([r['pagina'],r['municipio'],r['abitanti_stimati'],r['eventi'],r['mancanti_a_quartiere_attivo'],len(n)]+[ct.get(t,0) for t in TY]+
             [sum(1 for o in n if o.get('facebook')),sum(1 for o in n if o.get('sito')),sum(1 for o in n if o['eventi_futuri_trovati']),sum(1 for e in E if e['zona']==z)])
for i,c in enumerate(hdr,1): w.column_dimensions[get_column_letter(i)].width=22 if i==1 else 13
w.freeze_panes='B2'
s=wb.create_sheet('Soggetti')
cols=['nome','tipo','pagina','municipio','indirizzo','sito','facebook','instagram','gruppo_facebook','telefono','email','eventi_futuri_trovati','origini','gia_nota','ente','categoria_google','collegamento','descrizione','lat','lon']
s.append(cols)
for c in s[1]: c.font=Font(bold=True)
for o in sorted(L,key=lambda o:(o['pagina'],bool(o['gia_nota']),TY.index(o['tipo']) if o['tipo'] in TY else 99,o['nome'])):
    s.append([('sì' if o.get(c) is True else 'no' if o.get(c) is False else o.get(c)) if c=='ente' else o.get(c) for c in cols])
    if o['gia_nota']:
        for c in s[s.max_row]: c.font=Font(color='888888')
for i,c in enumerate(cols,1): s.column_dimensions[get_column_letter(i)].width=40 if c in ('nome','indirizzo','sito','facebook','descrizione','collegamento','gia_nota') else 16
s.freeze_panes='B2'; s.auto_filter.ref=s.dimensions
e=wb.create_sheet('Eventi trovati'); ec=['inizio','fine','ora','ricorrente','titolo','luogo','fonte','tipo_fonte','zona','zona_metodo','canale','url','testo']
e.append(ec)
for c in e[1]: c.font=Font(bold=True)
for x in sorted(E,key=lambda x:(x['inizio'],x['fonte'])): e.append([x.get(c) for c in ec])
for i,c in enumerate(ec,1): e.column_dimensions[get_column_letter(i)].width=45 if c in ('titolo','luogo','fonte','url','testo') else 14
a=wb.create_sheet('Albi municipali'); a.append(['nome','municipio','indirizzo','attivita','origine','trovato_nella_lista'])
for c in a[1]: c.font=Font(bold=True)
idx=[(toks(o['nome']),o) for o in L]
for r in json.load(open(f'{S}/supplementare/albo/albi_municipali.json')):
    t=toks(r['nome']); hit=next((o for tt,o in idx if t and len(t&tt)/len(t|tt)>=0.6),None)
    a.append([r['nome'],r['municipio'],r.get('indirizzo'),r.get('attivita'),r['origine'],(hit['nome']+' ('+hit['pagina']+')') if hit else None])
a.column_dimensions['A'].width=50; a.column_dimensions['E'].width=50; a.column_dimensions['F'].width=50
m=wb.create_sheet('Metodo')
for t in ['Pagine: le 41 pagine QN sotto la mediana di eventi ogni 10.000 abitanti (foglio eventi_per_abitanti.xlsx).',
          'OpenStreetMap: luoghi di culto, centri sociali, culturali e per anziani, associazioni, circoli, scout, biblioteche, teatri nel Comune di Roma (Overpass).',
          'Google Maps: «associazione», «centro anziani», «comitato di quartiere», «centro culturale», «parrocchia» + toponimo, in 69 punti delle 41 pagine; tolte le attività commerciali.',
          'Albo della cittadinanza attiva di Roma Capitale (comune.roma.it), albi e registri delle associazioni dei Municipi III, IV e VII (PDF), annuario della Diocesi di Roma (22 schede: il sito chiede un captcha dopo poche pagine, la lettura si è fermata lì).',
          'Ricerca Google: «"comitato di quartiere" <toponimo> Roma» e «associazione <toponimo> Roma eventi» per i 207 toponimi delle 41 pagine; tenuti solo risultati con il toponimo nel titolo o nella descrizione e una parola da ente.',
          'Pagina QN: dalle coordinate (zona urbanistica e toponimo più vicino); per i risultati Google, il toponimo cercato.',
          'Doppioni uniti fra le fonti per sito, pagina Facebook o nome simile a meno di 250 m; «gia_nota» indica una fonte già nella wiki fonti-eventi, nel registro v4 o nel censimento RUNTS.',
          '«ente» = no: risultato Google che non sembra un ente (articolo, blog, testata); restano nella lista ma non contano.',
          'Eventi trovati: post Facebook degli ultimi 45 giorni (fino a 15 per pagina) e siti letti rispettando il robots.txt, con gli stessi filtri dell\'estrattore dei post; da verificare prima di pubblicare.']:
    m.append([t])
m.column_dimensions['A'].width=170
wb.save('/mnt/user-data/outputs/lista_supplementare_quartieri_deboli.xlsx')
print('soggetti',len(L),'nuovi enti',len(N),'eventi',len(E))

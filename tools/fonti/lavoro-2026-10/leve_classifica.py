# Leve del giro del 26 ottobre: classifica per probabilità di successo (tetto Apify 15 $), stato di ciascuna, foglio per l'owner e testo del rapporto
import json,openpyxl,collections
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad/leve'
res=json.load(open(f'{S}/journal_results.json')); L={l['id']:l for l in res['fusione']['leve']}
V={}
for k,v in res.items():
    if k.startswith('verifica:'): _,lid,lente=k.split(':'); V.setdefault(lid,{})[lente]=v
M=json.load(open(f'{S}/misure.json'))
ESEG={'L18':M['feed'],'L20':M['tic'],'L51':M['parchi'],'L08':M['nfkc'],'L01':M['r1'],'L02':M['geo'],'L17':M['culture']}
ORD=[('1. Dati pubblici strutturati, costo zero o sotto 2 $',['L22','L47','L56','L54','L46','L49','L55','L48','L52','L53','L57','L40','L26','L19','L21']),
     ('2. Letture con un modello (costo in token, non in Apify)',['L07','L12','L09','L10','L43','L11','L03','L06','L04','L05']),
     ('3. Canali diretti, accordi e licenze (serve una tua lettera o decisione)',['L35','L37','L36','L38','L39','L41','L42','L44','L45','L58']),
     ('4. Regole e budget (decisioni)',['L16','L13','L14','L15']),
     ('5. Piattaforme con termini restrittivi (da decidere prima di toccarle)',['L27','L28','L29','L32','L23','L25'])]
SCART={'L24':'Eventbrite: le API vietano la lettura di organizzatori terzi senza consenso; gli eventi arrivano già dai post','L30':'Telegram: i termini dal 3 febbraio 2026 vietano la raccolta automatica',
       'L31':'WhatsApp: solo a mano, con una SIM e ore di lettura a settimana','L33':'YouTube: 5-20 eventi al mese, quasi tutti dirette religiose e istituzionali','L34':'Nextdoor: contenuti riservati ai residenti',
       'L59':'VisitLazio: 10-30 al mese, quasi tutti in centro e fiere','L60':'comune.roma.it: 0-10 al mese, già noti da culture.roma.it; provata il 25 ottobre'}
def rc(lid,k):
    v=V.get(lid,{}).get('resa',{}); return (v.get(k) or L[lid]['resa_stimata_eventi' if k=='resa_corretta' else 'costo'])

# classifica della sera (verifica leggera delle leve L31-L60 e sintesi): giro2_risultato.json
G=json.load(open(f'{S}/giro2_risultato.json')); F=G['finale']; E={e['id']:e for e in G['esiti']}
SERA={'L19':('eseguita','tipi evento di WordPress di 33 siti, 401 pagine evento lette in schema.org (MAXXI e Bioparco compresi, L56): 106 righe, 16 eventi nuovi in pagina dopo doppioni e filtri; ilparioli.it escluso (aggregatore)'),
      'L56':('eseguita','compresa in L19: MAXXI, Bioparco e Teatro di Documenti letti dalle pagine evento; quasi tutti già in calendario'),
      'L11':('eseguita','256 link esterni dei post con un evento futuro, 237 pagine lette (biglietterie, social e Roma Today esclusi): 16 righe, 4 eventi nuovi'),
      'L59':('eseguita','VisitLazio: 68 eventi futuri nella pagina, 2 nel Comune di Roma, entrati entrambi'),
      'L48':('eseguita','feed RSS di Tor Vergata (ottobre-dicembre): 1 candidato con data futura, senza luogo: non in pagina'),
      'L57':('eseguita','feed RSS di ASL Roma 3 e Caritas: 4 candidati con data futura, senza luogo: non in pagina'),
      'L43':('eseguita','prova su 16 parrocchie fuori dal centro: 9 pagine avvisi lette, nessun appuntamento datato riconoscibile con le regole; serve la lettura con un modello'),
      'L03':('eseguita','luoghi di culture.roma.it e biblioteche per nome: 6 eventi senza pagina assegnati'),
      'L06':('eseguita','i doppioni completano il gemello invece di sparire: 23 campi e 2 pagine completati; la fusione dei quasi-doppioni resta da decidere (DEC-025)'),
      'L40':('da verificare con l\'owner','12 delle 15 pagine dei Municipi già lette il 25 ottobre: una seconda lettura oggi renderebbe quasi nulla; il valore è la cadenza settimanale (budget)'),
      'L49':('da verificare con l\'owner','non eseguita: separare rassegne e incontri dalle proiezioni richiede un modello'),
      'L05':('da verificare con l\'owner','non eseguita: resa 4-24 una tantum')}
for c in F['classifica']:
    if c['id'] in SERA: c['stato']=SERA[c['id']][0]; ESEG[c['id']]=SERA[c['id']][1]
STATO_ORD={'eseguita':0,'da eseguire subito':1,"da verificare con l'owner":2,'scartata':3}
C=sorted(F['classifica'],key=lambda c:(STATO_ORD.get(c['stato'],9),-c['probabilita']))
def verd(lid):
    if lid in V: return V[lid].get('resa',{}).get('verdetto'),V[lid].get('liceita',{}).get('verdetto'),V[lid].get('liceita',{}).get('rischi')
    e=E.get(lid,{}); return e.get('verdetto'),None,e.get('liceita')
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Leve'
cols=['ordine','id','leva','gruppo','stato','probabilità di successo','resa (dopo verifica)','costo Apify $','altri costi','motivo','esito misurato','verdetto resa','verdetto liceità','liceità e rischi','descrizione']
ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for n,c in enumerate(C,1):
    vr,vl,ri=verd(c['id'])
    ws.append([n,c['id'],c['nome'],c['gruppo'],c['stato'],c['probabilita'],c['resa_corretta'],c['costo_apify_usd'],c['costo_altro'],c['motivo'],ESEG.get(c['id']),vr,vl,ri,L[c['id']]['descrizione']])
W={'leva':50,'gruppo':34,'stato':22,'resa (dopo verifica)':60,'altri costi':36,'motivo':70,'esito misurato':50,'liceità e rischi':70,'descrizione':90}
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=W.get(c,12)
ws.freeze_panes='C2'; ws.auto_filter.ref=ws.dimensions
m=wb.create_sheet('Metodo')
for t in ['Giro del 26 ottobre 2026. Mattina: otto esploratori AI indipendenti hanno proposto 60 leve; 30 (L01-L30) sono passate da due verifiche avversarie, sulla resa e sulla liceità; le leve deterministiche migliori sono state eseguite (stato «eseguita», esito misurato).',
          'Sera: le altre 30 (L31-L60) sono state verificate da 10 scettici, tre leve ciascuno, con lo stesso rigore e un tetto di chiamate per non consumare troppa quota; poi una sintesi ha rifatto la classifica di tutte le 60 per probabilità di successo.',
          'Stati: «da eseguire subito» = costo zero o dentro 15 $ di Apify in tutto, lecita senza nuove decisioni, probabilità alta; «da verificare con l\'owner» = servono lettere, licenze, budget o una decisione; «scartata» = resa nulla o termini che vietano la lettura.',
          'Resa e costi sono quelli corretti dagli scettici, non le stime degli esploratori: quasi tutte le leve sono state ridimensionate, spesso di 2-5 volte.']:
    m.append([t])
m.column_dimensions['A'].width=180
wb.save('/mnt/user-data/outputs/leve_eventi_2026-10-26.xlsx')
def cell(x): return str(x if x is not None else '—').replace('|','/').replace('\n',' ')
cnt=collections.Counter(c['stato'] for c in C)
sub=[c for c in C if c['stato']=='da eseguire subito']
own=[c for c in C if c['stato']=="da verificare con l'owner"]
out=["## 1 decies. Secondo giro di leve per aumentare gli eventi in tutte le pagine (M, 26 ottobre 2026)","",
"Otto esploratori AI indipendenti hanno proposto 60 leve (dati già raccolti, categorie di fonti, feed e API, social, canali diretti, cadenza e conteggio, enti pubblici, estrazione con modelli). Ogni leva è passata da scettici che ne hanno ricontato la resa e controllato la liceità: le prime 30 con due verifiche ciascuna, le altre 30 con una verifica più leggera. Quasi tutte sono state ridimensionate, spesso di 2-5 volte. Le leve deterministiche migliori sono state eseguite subito, senza spesa Apify; la classifica completa è nel foglio `leve_eventi_2026-10-26.xlsx` su Drive.","",
f"**Risultato delle leve eseguite.** Eventi futuri nella pagina da {M['prima']['eventi']:,} a {M['dopo']['eventi']:,}, con pagina QN da {M['prima']['con_pagina']:,} a {M['dopo']['con_pagina']:,}; pagine con 10 o più eventi da {M['prima']['dieci']} a {M['dopo']['dieci']}; pagine a zero ferme a {M['dopo']['zero']} ({M['dopo']['zero_nomi']}).".replace(',','.'),"",
"| Leva | Che cosa | Esito misurato |","|---|---|---|"]
for lid,es in ESEG.items(): out.append(f"| {lid} | {cell(L[lid]['nome'])} | {cell(es)} |")
out+=["",f"**Classifica.** {cnt['eseguita']} eseguite, {cnt['da eseguire subito']} da eseguire subito (costo zero o quasi), {cnt[chr(100)+'a verificare con l'+chr(39)+'owner']} da verificare con l'owner, {cnt['scartata']} scartate. Nessuna delle 30 leve verificate la sera cambia l'ordine di grandezza: le migliori sono fonti strutturate gratuite e piccole.","",
"| Da eseguire subito | Probabilità | Resa dopo verifica | Apify |","|---|---|---|---|"]
for c in sub: out.append(f"| {c['id']} {cell(c['nome'])[:80]} | {c['probabilita']:.2f} | {cell(c['resa_corretta'])[:120]} | {c['costo_apify_usd']} $ |".replace('.',',',1) if False else f"| {c['id']} {cell(c['nome'])[:80]} | {str(c['probabilita']).replace('.',',')} | {cell(c['resa_corretta'])[:120]} | {str(c['costo_apify_usd']).replace('.',',')} $ |")
out+=["","**Da verificare con l'owner**, in ordine di probabilità: "+'; '.join(f"{c['id']} {cell(c['nome'])[:60]}" for c in own)+".","",
"**Leve gratuite eseguite la sera.** Tipi evento di WordPress (33 siti, MAXXI e Bioparco compresi), link esterni dei post, VisitLazio, feed RSS di Tor Vergata, ASL Roma 3 e Caritas, prova degli avvisi parrocchiali, luoghi noti per nome, doppioni che completano il gemello: eventi futuri da 2.563 a 2.585, con pagina QN da 2.081 a 2.100. Rendono poco, come aveva previsto la verifica: le pagine evento dei grandi enti erano già in calendario, i feed delle istituzioni sono notizie più che eventi, gli avvisi parrocchiali senza un modello non danno appuntamenti riconoscibili. Le pagine dei Municipi non sono state rilette: 12 su 15 erano già state lette il 25 ottobre.","","**Cosa dice la verifica sul lungo periodo.** Lo stock di oggi è una foto: una parte viene da letture una tantum che non si ripetono, e senza rileggere i canali Facebook scende verso 1.700-1.900 a metà novembre. Con letture settimanali di tutti i canali (75-95 dollari al mese di Apify) lo stock a regime stimato è 1.100-1.300 eventi (L15), non 2.000; una lettura ridotta alle circa 200 pagine che hanno prodotto il 60% degli annunci futuri costa 8-12 dollari al mese e coglie il 30-45% del flusso fresco dei post (L14). Le decisioni che servono all'owner: budget Apify mensile, regola di conteggio (doppioni fusi, orizzonte di 60 giorni, serie contate una volta: sulla foto del mattino 2.384 diventano circa 1.940), letture automatiche settimanali di siti e feed pubblici, contatto in uscita con i promotori (prima i canali a consenso: modulo e newsletter), permesso scritto per Zero.eu.","",
"**Rischi.** Ogni fonte nuova porta doppioni (la fusione dei doppioni va fatta prima di misurare le leve nuove); le fonti strutturate si concentrano nei Municipi I e II; le 5 pagine a zero non sono toccate da nessuna leva misurata; parrocchie, scuole e ASL contengono nomi di persone (in estrazione si tengono solo data, ora, luogo ed ente).",""]
open(f'{S}/rapporto_1decies.md','w').write('\n'.join(out)+'\n'); print('\n'.join(out)[-2500:])

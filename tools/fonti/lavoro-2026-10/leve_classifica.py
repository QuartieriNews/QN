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
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Leve'
cols=['ordine','id','leva','gruppo','stato','esito misurato','resa stimata (dopo verifica)','costo','verdetto resa','verdetto liceità','rischi','decisione necessaria','descrizione']
ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
rows=[]; n=0
for lid,es in ESEG.items():
    n+=1; rows.append([n,lid,L[lid]['nome'],'eseguita il 26 ottobre','eseguita',es,rc(lid,'resa_corretta'),rc(lid,'costo_corretto'),V.get(lid,{}).get('resa',{}).get('verdetto'),V.get(lid,{}).get('liceita',{}).get('verdetto'),V.get(lid,{}).get('liceita',{}).get('rischi'),L[lid].get('decisioni_necessarie'),L[lid]['descrizione']])
for g,ids in ORD:
    for lid in ids:
        n+=1; rows.append([n,lid,L[lid]['nome'],g,'da verificare (owner)',None,rc(lid,'resa_corretta'),rc(lid,'costo_corretto'),V.get(lid,{}).get('resa',{}).get('verdetto'),V.get(lid,{}).get('liceita',{}).get('verdetto'),V.get(lid,{}).get('liceita',{}).get('rischi'),L[lid].get('decisioni_necessarie'),L[lid]['descrizione']])
for lid,why in SCART.items():
    n+=1; rows.append([n,lid,L[lid]['nome'],'scartata','scartata',why,rc(lid,'resa_corretta'),rc(lid,'costo_corretto'),V.get(lid,{}).get('resa',{}).get('verdetto'),V.get(lid,{}).get('liceita',{}).get('verdetto'),None,None,L[lid]['descrizione']])
for r in rows: ws.append(r)
W={'leva':50,'gruppo':40,'stato':20,'esito misurato':50,'resa stimata (dopo verifica)':70,'costo':40,'rischi':70,'decisione necessaria':40,'descrizione':90}
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=W.get(c,12)
ws.freeze_panes='C2'; ws.auto_filter.ref=ws.dimensions
m=wb.create_sheet('Metodo')
for t in ['Giro del 26 ottobre 2026: otto esploratori AI indipendenti (dati già raccolti, categorie di fonti, feed e API, social, canali diretti, cadenza e conteggio, enti pubblici, estrazione con modelli) hanno proposto 60 leve; 30 sono passate da due verifiche avversarie (resa e liceità) prima che il giro fosse fermato per limiti di quota; le altre 30 hanno solo la stima dell\'esploratore.',
          'Classifica: per probabilità di successo con un tetto di 15 $ di Apify. Eseguite subito le leve deterministiche su dati già nostri o su feed pubblici strutturati; da verificare con l\'owner tutte le altre, raggruppate per tipo; scartate quelle con resa nulla o termini che vietano la lettura.',
          'Le colonne «resa stimata» e «costo» riportano la correzione dello scettico quando c\'è, altrimenti la stima dell\'esploratore (le leve L31-L60 non sono state verificate).']:
    m.append([t])
m.column_dimensions['A'].width=180
wb.save('/mnt/user-data/outputs/leve_eventi_2026-10-26.xlsx')
# testo del rapporto
def cell(x): return str(x or '—').replace('|','/').replace('\n',' ')
out=[f"## 1 decies. Secondo giro di leve per aumentare gli eventi in tutte le pagine (M, 26 ottobre 2026)","",
"Otto esploratori AI indipendenti hanno proposto 60 leve (dati già raccolti, categorie di fonti, feed e API, social, canali diretti, cadenza e conteggio, enti pubblici, estrazione con modelli); 30 sono passate da due verifiche avversarie, sulla resa e sulla liceità, prima che il giro fosse fermato per limiti di quota. Classifica per probabilità di successo con un tetto di 15 dollari di Apify: eseguite subito le leve deterministiche su dati già nostri o su feed pubblici strutturati (0 dollari spesi); le altre stanno nel foglio `leve_eventi_2026-10-26.xlsx` su Drive, da verificare con l'owner.","",
f"**Risultato delle leve eseguite.** Eventi futuri nella pagina da {M['prima']['eventi']:,} a {M['dopo']['eventi']:,}, con pagina QN da {M['prima']['con_pagina']:,} a {M['dopo']['con_pagina']:,}; pagine con 10 o più eventi da {M['prima']['dieci']} a {M['dopo']['dieci']}; pagine a zero ferme a {M['dopo']['zero']} ({M['dopo']['zero_nomi']}).".replace(',','.'),"",
"| Leva | Che cosa | Esito misurato |","|---|---|---|"]
for lid,es in ESEG.items(): out.append(f"| {lid} | {cell(L[lid]['nome'])} | {cell(es)} |")
out+=["","**Leve da verificare con l'owner**, in ordine di probabilità di successo (resa e costo come corretti dallo scettico, dove c'è stata la verifica):",""]
for g,ids in ORD:
    out.append(f"- **{g}:** "+'; '.join(f"{lid} {cell(L[lid]['nome'])[:70]} ({cell(rc(lid,'resa_corretta'))[:90]}; {cell(rc(lid,'costo_corretto'))[:50]})" for lid in ids))
out+=["","**Scartate:** "+'; '.join(f"{lid} {why}" for lid,why in SCART.items())+".",""]
open(f'{S}/rapporto_1decies.md','w').write('\n'.join(out)+'\n'); print('\n'.join(out)[:1500])

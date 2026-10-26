# promotori_dove_cercare_2026-10-26.xlsx (Drive): i 1.246 promotori con la regola, il riepilogo e i costi mensili.
import json,collections,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
R=json.load(open(f'{S}/canali/regola_promotori.json')); P=json.load(open(f'{S}/promotori/promotori_finale.json'))
W=json.load(open(f'{S}/canali/promotori_wiki.json')); C=json.load(open(f'{S}/canali/costi.json'))
nuovi={e['id'] for e in json.load(open(f'{S}/wiki_out_v6/fonti_eventi.json'))['fonti'] if e['id'].startswith('S-PR-')}
ORD=['feed del sito','calendario del sito (schema.org)','pagina eventi del sito','notizie del sito (RSS)','agenda Biblioteche di Roma','culture.roma.it','eventi Facebook','post Facebook','Instagram (non letto)','solo aggregatore','nessun canale']
def it(n,d=0): return f"{n:,.{d}f}".replace(',','X').replace('.',',').replace('X','.')
wb=openpyxl.Workbook(); B=Font(bold=True); HF=PatternFill('solid',fgColor='DDEBF7')
def head(ws,h,w):
    ws.append(h)
    for c in ws[1]: c.font=B; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
    for i,x in enumerate(w,1): ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width=x
    ws.freeze_panes='A2'
# Promotori
ws=wb.active; ws.title='Promotori'
head(ws,['promotore','categoria','eventi ott 2026','eventi futuri noti','canale da leggere','prova','eventi ritrovati sul sito (titolo e data)','eventi ritrovati (solo titolo)','date future sul sito','pagina da leggere','controllo (cadenza lenta)','stato del sito','sito','facebook','instagram','id schedario','voce nuova (registro v6)'],
     [40,30,9,9,26,12,11,11,9,50,18,20,32,40,32,13,11])
def stato(x):
    if not x['host_provato']: return 'nessun sito'
    if x['robots_vieta'] and not x['sito_letto']: return 'robots.txt vieta'
    if not x['sito_letto']: return 'non raggiungibile'
    return 'letto (JavaScript)' if x['sito_dinamico'] else 'letto'
for x,p,w in sorted(zip(R,P,W),key=lambda t:(ORD.index(t[0]['canale']),-t[1]['n_eventi'],t[1]['nome'].lower())):
    ws.append([p['nome'],p.get('categoria'),p['n_eventi'],x['futuri_noti'],x['canale'],x['prova'],x['confermati'] or None,(x['trovati']-x['confermati']) or None,x['date_testo']+x['jsonld'] or None,
               x['pagina'],x['controllo'],stato(x),p.get('sito'),x['facebook'] or p.get('facebook'),p.get('instagram'),w['id'],'sì' if w['id'] in nuovi else None])
# Riepilogo
ws=wb.create_sheet('Riepilogo per canale'); head(ws,['canale da leggere','prova','promotori','eventi ott 2026','eventi futuri noti','costo'],[34,22,11,11,11,40])
g=collections.defaultdict(lambda:[0,0,0])
for x in R: k=(x['canale'],x['prova']); g[k][0]+=1; g[k][1]+=x['n_eventi']; g[k][2]+=x['futuri_noti']
COST={'eventi Facebook':'Apify, a evento letto','post Facebook':'Apify, a post','Instagram (non letto)':'non letto (Apify, a post, se si decide)'}
for k in sorted(g,key=lambda k:(ORD.index(k[0]),k[1])): ws.append([k[0],k[1],*g[k],COST.get(k[0],'0 $ (lettura diretta)' if k[0] not in ('solo aggregatore','nessun canale') else '—')])
ws.append([]); ws.append(['totale','',len(R),sum(x['n_eventi'] for x in R),sum(x['futuri_noti'] for x in R),'un evento con più promotori conta per ciascuno'])
# Costi
ws=wb.create_sheet('Costi mensili'); head(ws,['scenario','cadenza','pagine Facebook: eventi','pagine Facebook: post','$ eventi','$ post','$ avvii','controllo: pagine (post / eventi)','$ controllo','$ totale al mese'],[44,16,14,14,10,10,10,16,12,14])
DESC={'tutto Facebook':'Oggi: ogni promotore con pagina Facebook letto su Facebook (eventi e post)','regola':'Regola provata: canale gratuito dove c\'è la prova (storico o confermato), Facebook per gli altri','regola + probabili':'Regola provata + i siti «probabili» letti al posto di Facebook'}
for k,v in C['scenari'].items():
    sc,cad=k.split(' · '); ws.append([DESC[sc],cad,v['pagine_eventi'],v['pagine_post'],v['usd_eventi'],v['usd_post'],v['usd_avvii'],f"{v['controllo_pagine_post']} / {v['controllo_pagine_eventi']}",v['usd_controllo'],v['usd_totale']])
ws.append([]); 
for l in ["Siti, feed, notizie RSS, culture.roma.it e Biblioteche di Roma: 0 $ di Apify a qualsiasi cadenza (lettura diretta, robots.txt rispettato, una richiesta al secondo per sito).",
          "Post Facebook: si paga ogni post letto (0,004 $ + 0,001 $ di filtro data), non ogni lettura: con il filtro «solo post dal giorno prima» leggere ogni giorno o ogni settimana costa quasi uguale.",
          "Eventi Facebook: si paga ogni evento futuro restituito (0,003 $) a ogni lettura: è la sola voce che cresce con la cadenza.",
          "Controllo: per chi ha un canale gratuito che non porta tutti i suoi eventi, Facebook a cadenza lenta (incluso nei totali). Gli eventi Facebook una volta al mese costano pochi centesimi; i post invece si pagano a post, quindi il controllo sui post costa come leggerli ogni giorno.",
          "Piano Apify dell'account: Starter, 29 $ al mese con 29 $ di consumo incluso; tetto mensile 200 $. Ciclo in corso 24 ottobre - 23 novembre: 177,76 $ già consumati dai censimenti di ottobre.",
          "Non inclusi: scoperta di promotori nuovi per parole chiave su Facebook (circa 1 $ a trimestre); Instagram, oggi non letto (17 promotori)."]:
    ws.append([l])
# Prezzi e misure
ws=wb.create_sheet('Prezzi e misure'); head(ws,['voce','valore','fonte'],[50,16,80])
for r in [['post Facebook (apify/facebook-posts-scraper), fascia BRONZE','0,004 $ a post','listino dell\'attore letto via API il 26 ottobre 2026'],
          ['filtro data sui post','0,001 $ a post','idem'],['avvio di un\'esecuzione','0,001 $','idem'],
          ['eventi Facebook (unseenuser/fb-events), fascia BRONZE','0,003 $ a evento','idem; verificato: 48 eventi = 0,144 $ il 25 ottobre'],
          ['post al giorno per pagina (media)',it(C['post_media'],3),'4.016 pagine lette il 24-25 ottobre (finestre di 45 giorni e 6 mesi; pagine troncate stimate dagli ultimi post)'],
          ['post al giorno per pagina (mediana)','0,033','idem'],
          ['eventi futuri per pagina a ogni lettura',it(C['eventi_per_lettura'],3),'4.813 letture di pagine, 24-25 ottobre (esclusa un\'esecuzione anomala interrotta)'],
          ['siti letti nella prova del canale','847 su 942','26 ottobre: home, pagina eventi (dichiarata o trovata), feed RSS; secondo giro con varianti dell\'indirizzo, ricerca WordPress, browser per i siti in JavaScript'],
          ['siti con robots.txt che vieta','35 + 17 nel secondo giro','saltati, mai letti']]: ws.append(r)
# Leggimi
ws=wb.create_sheet('Leggimi',0); ws.column_dimensions['A'].width=150
tot=collections.Counter(); 
for x in R: tot['gratis' if x['canale'] not in ('eventi Facebook','post Facebook','Instagram (non letto)','solo aggregatore','nessun canale') and x['prova'] in ('storico','confermato') else ('prob' if x['prova']=='probabile' else x['canale'])]+=1
for l in ["Promotori degli eventi: dove cercare i prossimi eventi e quanto costa (26 ottobre 2026)","",
          f"1.246 promotori (chi ha organizzato almeno un evento della pagina «Eventi dei quartieri»). Canale gratuito con prova: {tot['gratis']}; gratuito probabile: {tot['prob']}; eventi Facebook: {tot['eventi Facebook']}; post Facebook: {tot['post Facebook']}; solo Instagram: {tot['Instagram (non letto)']}; solo aggregatore: {tot['solo aggregatore']}; nessun canale proprio: {tot['nessun canale']}.",
          "Regola: per ogni promotore il canale più economico che porta i suoi eventi, nell'ordine feed del sito, calendario schema.org, pagina eventi del sito, notizie del sito (RSS), agende già lette ogni giorno (culture.roma.it, Biblioteche di Roma), eventi Facebook, post Facebook.",
          "Prova: storico = a ottobre gli eventi sono già arrivati da quel canale; confermato = il 26 ottobre il sito portava eventi noti del promotore (titolo e data vicini, oppure il titolo intero); probabile = il sito pubblica date future ma nessuno degli eventi noti; solo pagina = pagina Facebook senza eventi letti finora.",
          "Controllo: canale da guardare una volta al mese quando quello gratuito non porta tutti gli eventi del promotore.",
          "Nessun canale proprio: soprattutto persone (artisti, guide) e co-organizzatori senza pagina: i loro eventi arrivano dalle pagine dei luoghi che li ospitano.",
          "Un campione di 25 riscontri «confermato» è stato controllato a mano: 24 veri, 1 falso (una data di un anno passato senza anno, ora esclusa).",
          "Voci nuove: 139 promotori che non avevano una voce nello schedario entrano nel registro v6 come candidati (chiave PR-…); la decisione tenere/scartare resta all'owner (DEC-024).",
          "Contatti, testi e titoli degli eventi non sono in questo foglio."]:
    ws.append([l])
ws['A1'].font=Font(bold=True,size=13)
wb.save('/mnt/user-data/outputs/promotori_dove_cercare_2026-10-26.xlsx'); print('ok')

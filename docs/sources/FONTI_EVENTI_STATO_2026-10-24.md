# Fonti eventi — stato al 24 ottobre 2026 e flusso continuo proposto

Rapporto di lavoro del builder (DEC-104) sul blocco eventi: cosa è stato letto, cosa è
stato trovato, cosa è pronto nel repository e cosa aspetta una decisione dell'owner. Ogni
numero è **M** (misurato) salvo dove è scritto **S** (stimato). I dati per evento e per
pagina (titoli, testi di presentazione) stanno su Drive e nell'anteprima privata, non qui
(DEC-022, DEC-109): `eventi_unico.xlsx`, `associazioni_fonti.xlsx`,
`eventi_senza_fonte_ricerca.xlsx`.

## 1. Dove siamo

| Cosa | Stato | Dove |
|---|---|---|
| Foglio unificato degli eventi di ottobre 2026 (Facebook via Apify, culture.roma.it, Roma Today, lettura diretta 13-31 ottobre) | 1.957 righe, geografia a due metodi, rintracciabilità, doppioni segnalati, colonna `riga_principale_proposta` (DEC-025 aperta) | Drive / anteprima |
| Wiki delle fonti eventi | 2.405 fonti (807 nel registro v2, 598 candidate dal censimento del 24 ottobre), pagine per Municipio e per pagina QN, «dove cercare» per ogni fonte, 181 fusioni proposte | `docs/wiki/fonti-eventi/` |
| Registro fonti versione 2 | 370 voci del 13 ottobre più 445 candidate della ricerca mirata per le 58 pagine QN deboli, ciascuna con tipo, zona, canale e dove cercare; decisione «candidata» | Drive (`registro_fonti_v2_pagine_deboli.xlsx`), ingresso del build della wiki |
| Censimento di 1.169 pagine Facebook di associazioni | letto al 99,9%: dati di pagina, eventi futuri, post degli ultimi sei mesi, sito, indirizzo geocodificato, verdetto automatico | `censimento-pagine.md` + foglio su Drive |
| Lettura settimanale dei siti delle fonti | strumento pronto e testato (`tools/fonti/leggi_eventi_siti.py`, T-LS-1..5); prima prova fatta sulle 809 fonti con un sito (§4 bis) | repository |
| Ricerca uno a uno dei 176 eventi senza fonte | fatta in due passaggi (sito del luogo nel registro, poi ricerca web): 30 fonti dirette trovate, `link_fonte_diretta` compilato | fogli su Drive |
| Decisioni aperte | DEC-024 (censimento → registro, Facebook come canale), DEC-025 (precedenza fra fonti) | `decisions/` |

## 1 bis. Fonti mirate per le 58 pagine QN deboli (M, 24 ottobre 2026)

Perimetro: le 89 pagine del gazetteer con meno di cinque eventi futuri nel foglio (31 a
zero, 27 fra uno e quattro). Metodo: per ogni pagina una ricerca per tipo di fonte
(parrocchia, centro anziani, comitato di quartiere, biblioteca, centro culturale, istituto
comprensivo, associazione; pro loco e consorzio per le 17 pagine di frontiera), 423 ricerche
Google via Apify (1,06 $), risultati tenuti solo se il nome del quartiere e la parola del
tipo compaiono nel titolo e il dominio non è un elenco, un aggregatore o una testata; più
quattro elenchi istituzionali letti per intero e geocodificati: centri sociali anziani dai
PDF ufficiali dei Municipi III, IV, X, XI, XII (39), biblioteche dall'elenco di Biblioteche
di Roma (45), istituti comprensivi dall'anagrafe MIUR 2026/27 (177), mercati rionali dai
dati aperti di Roma Capitale (69). Esito nel foglio `fonti_mirate_pagine_deboli.xlsx`.

| Misura | Valore |
|---|---|
| Candidate per le 58 pagine | 463 (sito 284, pagina Facebook 159, solo indirizzo 20); 443 con un indirizzo da controllare |
| Per tipo | istituti comprensivi 110 · comitati 72 · parrocchie 65 · centri anziani 61 · associazioni 39 · biblioteche 34 · centri culturali 31 · pro loco e consorzi 15 · mercati 13 |
| Pagine con almeno tre fonti (wiki + nuove) | 56 su 58; scoperte Dragona-Dragoncello (0) e Muratella (1) |
| Nuove nel registro v2 | 445 (17 coincidevano con voci del 13 ottobre) |

Limiti: le liste ufficiali dei centri anziani esistono solo per cinque Municipi; la
diocesi (parrocchie) e Overpass (OpenStreetMap) non sono raggiungibili dall'ambiente, le
parrocchie vengono dalla ricerca. Le candidate sono da leggere una volta a mano: la
ricerca garantisce il nome del quartiere nel titolo, non che la fonte pubblichi eventi.

## 2. Cosa ha detto il censimento delle pagine Facebook (M)

| Misura | Pagine |
|---|---|
| Pagine fornite | 1.169 |
| Lette (dati di pagina) | 1.131; non disponibili 37; non restituite 1 |
| Con eventi futuri su Facebook | 19 (60 eventi, 42 a Roma) — verificato con un secondo lettore su 12 pagine grandi: solo eventi passati |
| Con post negli ultimi sei mesi (lette 734 pagine senza eventi futuri) | 335; di cui 186 con almeno un post datato che annuncia un evento |
| Con un sito | 823; raggiungibili 602; con sezione eventi 277; con date future leggibili 83; con date negli ultimi sei mesi 178 |
| Con Municipio assegnato | 787 (indirizzo Facebook 778, geocodifica OSM 31, coordinate degli eventi 3); con pagina QN 672 |
| Verdetto «rientra» | 390 (eventi futuri FB 11 · calendario sul sito 57 · date recenti sul sito 81 · pagina eventi sul sito 103 · annunci nei post 138) |
| «locale» (attività commerciali) | 54 · «da valutare» 157 (24 politiche) · «attiva senza annunci» 110 · dormienti 275 · servizi/tematiche/fuori Roma/non disponibili 182 |

Lettura: queste associazioni **non usano gli eventi Facebook**; annunciano nei post o sul
sito. La prova di attività più economica e più affidabile è il sito (sezione eventi), la
seconda sono i post. Il lettore di eventi Facebook per pagina costa 0,18 $ per 1.169 pagine
e serve come controllo, non come scoperta.

## 3. Cosa ha detto la ricerca uno a uno dei 176 eventi senza fonte (M)

168 schede Roma Today, 7 culture.roma.it, 1 Facebook. Una ricerca Google per evento (titolo
+ luogo + Roma), esclusi gli aggregatori noti, i primi tre candidati letti e confermati se
almeno il 60% delle parole del titolo compare nella pagina.

| Esito | Eventi |
|---|---|
| Nessuna pagina non-aggregatore che citi l'evento | 127 |
| Sito terzo da verificare a mano | 30 |
| Menzione di terzi (stampa, blog, cataloghi editoriali) | 8 |
| Altro aggregatore con scheda strutturata | 7 |
| Fonte primaria probabile (sito del luogo o dell'ente) | 4 |

Secondo passaggio, nell'ordine giusto: per i 132 eventi il cui luogo è nel registro, il
sito del luogo (la pagina già letta dal lettore dei siti, altrimenti la pagina da
controllare dello schedario) è stato cercato per le parole del titolo: 26 eventi ritrovati
sul sito del luogo (musei civici, Colosseo, MACRO, Villa Giulia, Palazzo Bonaparte), contro
i 4 della ricerca web. Esito finale: 30 con fonte diretta (`link_fonte_diretta` compilato
nel foglio unificato, metodo in `fonte_diretta_metodo`), 27 con un sito terzo da verificare a
mano, 81 con il luogo noto ma l'evento assente dal suo sito, 37 senza luogo noto né traccia.

Conferma la lettura del 23 ottobre: per queste schede la fonte primaria di norma **non
esiste sul web** come pagina dell'evento; l'organizzatore comunica per comunicato stampa, pagina
Facebook (post) o non comunica affatto. La ricerca ha anche censito gli altri aggregatori
che Google propone per Roma (spotlightapp.eu, vibeloop.it, eventivicino.it, araundapp.it,
roma-o-matic.com, estateromana.com, bibliotechediroma.it): due sono fonti istituzionali da
aggiungere al registro (Estate Romana, Biblioteche di Roma), gli altri sono aggregatori da
valutare per licenza prima di ogni lettura.

## 4. Flusso continuo proposto (per canale)

| Canale | Come | Cadenza | Costo (S) | Stato |
|---|---|---|---|---|
| Siti delle fonti (809 con un sito, 277 con sezione eventi) | `tools/fonti/leggi_eventi_siti.py` sullo schedario; schema.org Event come prova forte, date nel testo come candidati; uscita fuori dal repository | settimanale | 0 $ | pronto; prima prova fatta (§4 bis) |
| culture.roma.it | `tools/fonti/leggi_culture_roma.py`: API WordPress (`event_calendar`, `modified_after`) letta per differenza, scheda letta per ogni voce nuova o modificata, stato in un file fuori dal repository | ogni 2 giorni | 0 $ | pronto e provato (§4 ter) |
| Facebook, pagine note | `unseenuser/fb-events` con `pageUrls` di tutte le pagine del registro e del censimento, `onlyUpcoming` | ogni 2 settimane | ~0,5 $ | provato il 24 ottobre; schedulazione dipende da DEC-024 Q3 |
| Facebook, scoperta | lettura per parole chiave (89 nomi di pagina QN + termini generici); organizzatori nuovi → censimento | mensile | ~1 $ | provato il 24 ottobre: rende pochissimo (§5); da tenere solo come controllo |
| Facebook, post delle pagine | `apify/facebook-posts-scraper` sulle pagine «attive senza eventi» (10 post, ultimi 30 giorni) | mensile | ~3 $ | provato il 24 ottobre (2.985 post) |
| Roma Today | nessuna lettura regolare: robots.txt e licenza Citynews («nessun canale senza licenza») | — | — | chiuso salvo licenza |
| Il workflow n8n `scrape-fb-events-rome.json` | export nel repository: `active: false`, schedulazione ogni due notti alle 3 (`0 0 3 */2 * *`), ricerca «Italy Roma» con 200 eventi al massimo, scrittura in Firestore `roma-pipeline` / `facebook-posts` / `events` e nel foglio «QuartieriNews _ Events and Posts File»: nomi di produzione, nessun prefisso `staging_`; arricchimento con OpenAI. Sul conto Apify dell'organizzazione non c'è nessuna schedulazione né run precedente al 24 ottobre: se gira, gira dal vecchio conto. La ricerca «Italy Roma» è il canale che il 24 ottobre ha reso meno di tutti (§5) | — | — | da verificare dall'owner su n8n (gira? con quale conto?); sostituto candidato: lettura per pagine note |

Regola comune: ogni lettura produce righe con `fonte_id` dello schedario, così gli eventi
nuovi si contano per fonte e per pagina QN e la wiki si aggiorna dai conteggi, mai dai testi.

## 4 bis. Prima prova della lettura dei siti (M, 24 ottobre 2026)

`tools/fonti/leggi_eventi_siti.py` su tutte le fonti dello schedario con una pagina da
leggere, orizzonte 60 giorni, otto processi in parallelo per host diversi. Esito nel foglio
`eventi_siti_prova_2026-10-24.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Fonti con una pagina da leggere | 809; lette 675; non raggiungibili 137 |
| Fonti con eventi schema.org nei prossimi 60 giorni (prova forte) | 12, per 157 eventi (teatri e un paio di associazioni) |
| Fonti con date nel testo (candidati da leggere a mano) | 196, per 1.089 blocchi datati |
| Costo | 0 $ |

Lettura: i siti delle fonti romane raramente pubblicano eventi strutturati; la lettura
settimanale produce poche righe certe e molte righe candidate, che una persona (o un
passaggio di lettura con modello) deve confermare. Il valore della lettura automatica è
dire **quali** fonti hanno pubblicato qualcosa di datato questa settimana, non estrarne
la scheda. Dei 137 siti non raggiungibili, 61 sono domini che non esistono più (il nome non
si risolve: indirizzi vecchi lasciati sulle pagine Facebook), 26 chiudono la connessione, 23
hanno certificati non validi, 11 rispondono 403: da togliere o correggere nel registro, non
da riprovare.

## 4 ter. Prima lettura per differenza di culture.roma.it (M, 24 ottobre 2026)

`tools/fonti/leggi_culture_roma.py` dal punto zero del 20 ottobre (la lettura completa con
Apify). Esito nel foglio `culture_roma_delta_2026-10-24.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Schede modificate o pubblicate dal 20 ottobre | 74 (43 nuove, 31 modificate), tutte lette, 0 errori |
| Con date lette | 74; con fine da oggi in poi 72 |
| Con «a cura di» (organizzatore) | 69; con sito esterno 73; con coordinate 67; con Municipio 65 |
| Costo e tempo | 0 $; circa due minuti a una richiesta al secondo |

Lettura: quattro giorni di agenda valgono 43 schede nuove, cioè circa dieci al giorno, quasi
tutte con organizzatore e sito: è il canale a più alto rendimento per euro speso e il
primo da mettere in calendario. Gli organizzatori «a cura di» delle schede nuove sono il
modo naturale di scoprire fonti nuove (§5): entrano nel censimento come candidate.

## 5. Scoperta di organizzatori nuovi su Facebook per parole chiave (M)

Due lettori, stesso giorno: `unseenuser/fb-events` con 109 parole chiave (89 nomi di pagina
QN + 20 termini generici) e `apify/facebook-events-scraper` con 30 ricerche (lo stesso
meccanismo del workflow n8n di produzione, che usa «Italy Roma»), 150 eventi al massimo per
ricerca. Esito nel foglio `facebook_scoperta_organizzatori.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Eventi futuri distinti trovati (i due lettori insieme) | 95 |
| A Roma (Municipio assegnato dalle coordinate) | 60; con pagina QN 49; zone QN toccate 21 |
| Organizzatori distinti | 99; nuovi rispetto allo schedario 75; nuovi con almeno due eventi a Roma 0 |
| Costo | 0,19 $ + 0,98 $ |

Lettura: **la ricerca per parole chiave su Facebook non scopre quasi nulla**. Il motore di
ricerca eventi di Facebook risponde con poche decine di risultati per termine, molti passati
o fuori Roma; con 139 ricerche si trovano 60 eventi romani, cioè meno di quanti ne produce
in un mese una sola fonte media del registro. Lo stesso vale per la pagina «eventi della
città» (3 risultati). Per la scoperta di organizzatori nuovi restano tre strade che
funzionano: gli organizzatori citati dagli eventi già letti (culture.roma.it «a cura di»,
host degli eventi Facebook delle pagine note), gli elenchi istituzionali (albo delle
associazioni dei Municipi, Biblioteche di Roma, Estate Romana) e le liste raccolte a mano
dall'owner come quella del 24 ottobre. Il workflow n8n di produzione, che si affida alla
ricerca «Italy Roma», va considerato un canale debole: conferma, non scoperta.

## 6. Problemi rilevati

1. **Facebook eventi ≠ attività.** Il verdetto «dormiente» basato sui soli eventi Facebook
   avrebbe scartato 186 pagine attive: la lettura dei post ha corretto il tiro. Ogni
   giudizio di attività deve usare almeno due segnali (sito, post, eventi).
2. **Gli aggregatori si copiano.** La ricerca Google per evento restituisce quasi solo altri
   aggregatori; la rintracciabilità alla fonte non migliora cercando di più, migliora solo
   leggendo prima la fonte (sito, pagina Facebook dell'organizzatore).
3. **Identità delle fonti.** 72 candidate del censimento coincidono con voci del registro
   per URL Facebook; altre coincidono per nome con grafie diverse e restano doppie finché
   una persona non le fonde (regola della wiki: le fusioni dubbie non si fanno). La wiki
   genera ora `fusioni-proposte.md`: 85 coppie da decidere.
4. **Geografia dai soli indirizzi Facebook.** 778 pagine hanno coordinate da Facebook, ma
   l'indirizzo di una pagina è la sede, non il luogo degli eventi; per 3 pagine la geografia
   viene dagli eventi. Il Metodo QN (`tools/geo-assign/qngeo.py punto`) non è stato usato
   perché il pacchetto cartografico sta su Drive (`_ZZ Metodo QN`) e non nel repository:
   portarlo nell'ambiente è il passo per rendere la geografia degli eventi uguale a quella
   delle notizie.
5. **Doppioni.** 132 gruppi, 324 righe secondarie con la regola proposta (DEC-025 a): contando
   solo le righe principali le pagine QN con almeno dieci eventi futuri scendono da 23 a 20.

## 7. Prossimi passi, in ordine

1. Owner: DEC-023, DEC-024, DEC-025, DEC-026; verificare su n8n se il workflow Facebook gira
   e con quale conto Apify.
2. Decidere le candidate del registro v2 (445 della ricerca mirata, 598 del censimento)
   secondo DEC-024 Q1; aggiungere Estate Romana come fonte istituzionale.
3. Mettere in calendario la lettura settimanale dei siti (§4) e misurare per quattro settimane
   quante fonti producono davvero; poi rileggere le candidate «pagina eventi senza date».
4. Scrivere la lettura per differenza di culture.roma.it.
5. Portare il pacchetto Metodo QN nell'ambiente e riassegnare la geografia degli eventi con
   `qngeo.py punto`.
6. Rimisurare a fine novembre: eventi futuri per pagina QN con le sole righe principali.

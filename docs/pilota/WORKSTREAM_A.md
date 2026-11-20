# Workstream A · Amministrazione: il brief

Stato: la raccolta, PR A2 (15 novembre 2026). Le regole del canale stanno in
`docs/pilota/CONTRATTI.md`, sezione 7, «A · Amministrazione», e le scelte dell'owner in
DEC-036 e DEC-037: qui non si ripetono, si rimanda. Questo documento dice che cosa si
costruisce, con quali mezzi e come si prova; la sessione che costruisce i flussi parte da qui.
Se una regola cambia, cambia là, e qui si corregge solo il rimando.

## 1. Scopo e confini

A porta al blocco «Dal Municipio» (`institutional`) i fatti delle sedute registrate dei
Municipi I, V e X, delle commissioni capitoline e dell'Assemblea capitolina, presi solo dalla
seduta aperta (DEC-031, punto 2A; DEC-105). Legge le sedute future, dal 1° novembre 2026,
partendo da quelle già pubblicate; lo storico non si ricostruisce (DEC-036, punto 1). Il canale
si apre a passi, come B (#36): fino alle PR della lettura, della geografia, delle classi
editoriali, della scrittura e della seconda verifica non scrive elementi, solo quello che
CONTRATTI, sezione 7 A, elenca. Tutto gira in staging: flussi `staging_A_*` su n8n Cloud e la
cartella privata `QN Hub / 30 Staging pilota 2026-11 / A Amministrazione/` su Drive; la
produzione non si tocca (`CLAUDE.md`). Restano fuori dal workstream: il registro fonti
(coordinatore), il gazetteer (si cambia solo con il suo build), il sito (`tools/site/`, che
riceverà la proiezione con A5) e lo storico degli atti (D).

## 2. Fonti e copertura delle tre pagine

Ore di giugno 2026 per data della seduta, dai CSV A3 e A4 di `tools/sources-study/handoff_data/`
(le ore per riga della tabella 3.2 di `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md` non tornano
con i CSV; i totali sì: valgono i CSV).

| Pagina | Organo | Fonte | Testo | Ore al mese |
|---|---|---|---|---|
| Acilia (X) | Consiglio del Municipio X | RomaTV, catalogo `Municipio X` | trascrizione della piattaforma | 4,0 |
| Acilia (X) | commissioni del Municipio X | RomaTV, `Municipio X` | nostra | 12,1 |
| Centocelle (V) | Consiglio del Municipio V | RomaTV, `Municipio V` | trascrizione della piattaforma | 8,8 |
| Centocelle (V) | commissioni del Municipio V | RomaTV, `Municipio V` | nostra | 18,3 |
| Prati (I) | Consiglio e commissioni del Municipio I | YouTube, canale `UCEZtd0d0UV5e8ZCWkNOiNjw` | nostra, dall'audio preso con un Actor di Apify (DEC-037) | 42,1 (3,5 + 38,6) |
| tutte e tre | commissioni capitoline | RomaTV, `Commissioni Capitoline` | nostra | 51,6 |
| tutte e tre | Assemblea capitolina | RomaTV, `Assemblee Capitoline` | nostra | 41,3 |

Da trascrivere noi: 30,4 ore municipali di V e X, 42,1 del Municipio I, 51,6 capitoline e
41,3 dell'Assemblea, 165,4 ore al mese (sezione 7). Quali fatti capitolini si tengono lo dice
DEC-036, punto 4.

- **Trascrizione della piattaforma:** solo i Consigli municipali (82 su 86 in giugno, su tutti
  i Municipi). Il 14 novembre l'avevano le parti dei Consigli del V pubblicate il 10 e il
  12 novembre; un Consiglio del X di fine ottobre non l'aveva. Nessuna commissione, municipale o capitolina.
- **Le altre piattaforme:** il catalogo `Municipio I` di RomaTV ha due voci, del 2021. I canali
  YouTube del V (senza sedute dopo il 12 giugno 2026) e del X (fermo da febbraio 2025) non si leggono.
  L'Assemblea è anche sul canale YouTube di Roma Capitale: non si legge (sezione 9, doppioni).
- **RomaTV al 14 novembre** (sonda 918): 244 voci del V, 681 del X, 5.615 commissioni
  capitoline, 498 voci dell'Assemblea. Ritmo: commissioni del V quasi ogni giorno; del X circa un
  giorno lavorativo su due (9 su 16 fra il 23 ottobre e il 13 novembre; 10 su 22 a giugno), per
  lo più da 30 a 50 minuti e fino a un'ora e mezza, più i Consigli; commissioni capitoline circa
  4 al giorno nei giorni di seduta (da 1 a 8 a giugno), da 15 a 95 minuti; l'Assemblea 2–3 volte a settimana, da 1 a 6 ore, spesso in parti (la più lunga vista:
  5 ore e 51). Alcuni titoli capitolini sono generici.
- **Ritardo di pubblicazione,** giugno, RomaTV: mediana 0 giorni, 387 su 496 entro 7, massimo
  94; commissioni capitoline 73 su 75 lo stesso giorno (massimo 5); Assemblea 7 su 7 lo stesso
  giorno; Municipio X 9 su 16 lo stesso giorno (massimo 8); i Consigli del V del 4–18 giugno
  usciti tutti il 10 luglio, da 22 a 36 giorni dopo. Novembre: un Consiglio del X uscito 16
  giorni dopo, le capitoline entro poche ore. YouTube del I: lo stesso giorno (15 su 15 nel feed
  di settembre). Quando compare il WebVTT rispetto alla pubblicazione non è misurato: lo prende
  lo sguardo indietro di 100 giorni dell'elenco (CONTRATTI, sezione 7 A, «Raccolta»).
- **Prati.** Il 14 novembre, da n8n, il feed rispondeva e la pagina del video dava la pagina
  di consenso UE, senza tracce dei sottotitoli: per DEC-036, punto 3, era un segnale di blocco,
  e `www.youtube.com` si è fermato. Dal 15 novembre vale DEC-037: l'elenco dei video e
  l'audio vengono da Actor di Apify e il testo dalla nostra trascrizione; n8n non chiede più
  niente a YouTube. La prova degli Actor del 20 novembre (sezione 6) ha scelto quello
  dell'elenco; l'audio no: quella notte YouTube ha bloccato tutti e due gli Actor dell'audio, su
  due video. Finché l'audio non arriva, A3 costruisce e prova con fixture, e Prati resta senza
  testo.

## 3. I mezzi

Stato al 14 novembre 2026; le righe su YouTube e Apify sono del 15 (DEC-037) e del 19–20 (la
prova degli Actor, sezione 6). Gli id delle esecuzioni sono quelli delle sonde
(`staging_A_sonda_*` e `staging_A_prova_apify*`, spente dopo le corse di prova).

| Mezzo | Stato | Note |
|---|---|---|
| n8n Cloud, piano Starter (`quartierinews.app.n8n.cloud`) | PRESENTE | nodo Code con `require('crypto')` (AES-128-CBC), `Buffer`, `setTimeout`, `this.helpers.httpRequest` (testo o `arraybuffer`, risposta intera, errori HTTP senza eccezione; su n8n 2.x il nodo gira nel task runner, dove un file con `'use strict'` non ha `this` e `helpers` è una variabile globale: `code-nodes/source-guard.js`, esecuzione 1337); niente `process` (916); niente `URL` né il modulo `url` (non dalle sonde: commit 2e6a288, `code-nodes/news-collect.js`); altri moduli non provati, non si usano |
| RomaTV raggiunto da n8n | PRESENTE | elenco (`search_frontend`), WebVTT, JSON del parlato, playlist, chiave e segmenti rispondono 200 (918, 921); l'elenco e la chiave sono stati chiesti sempre con `Origin` e `Referer` del portale, e se servono non è provato; WebVTT, JSON del parlato, playlist e segmenti hanno risposto senza (sezione 4, la strada dell'audio, passo 3) |
| `www.youtube.com` da n8n | NON SI USA (DEC-037) | il 14/11: feed 200, pagina del video = pagina di consenso UE (918); dal 15/11 l'elenco e l'audio vengono da Apify, senza nessuna chiave di Google (sezione 2) |
| Apify da n8n, per l'elenco e l'audio di YouTube | PRESENTE; letture e cancellazioni provate il 19–20/11, l'avvio di una corsa da n8n no | su n8n c'è la credenziale Apify del canale C, «Bearer Auth account» (`staging_C_fb_events_fetch`); il 14/11 l'API di n8n non la poteva usare e l'editor dell'owner non cambiava i nodi che la usano (`workflows/README.md`); il 15/11 una sonda del coordinatore ha creato dall'API un flusso `staging_` con un nodo che la riferisce (mai eseguito, cancellato subito): un flusso nuovo fatto dall'API la può riferire. Il 19/11 la prima corsa che la usa, la sonda `staging_A_prova_apify` (spenta), ha avuto da Apify 401 `user-or-token-not-found` (esecuzioni 2003 e 2004): la chiave salvata non valeva più. L'owner l'ha rimessa la sera stessa; la stessa sonda (2007) ha letto il conto, che è quello del collegamento ad Apify delle sessioni, e le sue corse. Il 20/11 le sonde `staging_A_prova_apify_*` (spente) l'hanno usata per leggere le corse della prova e per cancellarne gli storage (sezione 6). Resta da riprovare la modifica dei nodi che già la usano in `staging_C_fb_events_fetch`, che tocca al canale C. Gli Actor: sezione 7; la prova: sezione 6 |
| Riserva fuori da Apify, per l'audio di YouTube | DALL'OWNER, sulle opzioni del builder | DEC-037, punto 3; finché non c'è, la riserva è un secondo Actor (sezione 9). Il 20/11 YouTube ha bloccato tutti e due gli Actor dell'audio (sezione 6) |
| Credenziale «OpenAI account» (`openAiApi`) | PRESENTE | condivisa dall'owner il 14/11 col progetto dei flussi `staging_`; `gpt-4o-mini-transcribe` e `whisper-1` rispondono 200 su un M4A di 10 minuti (921) |
| Credenziale «Google Drive account» (`googleDriveOAuth2Api`) | PRESENTE; via API PROVATA il 15/11 (sezione 8, punto 3) | condivisa il 14/11; c'è una quota di richieste al minuto (D si è fermato il 13/11). POST e PUT con la credenziale provati sui nodi `openAiApi` il 14/11 (918, 921) e su un nodo Drive il 15/11 (`staging_A_confronto`), dopo che le sessioni precedenti avevano visto il contrario (`PASSAGGIO_2026-11-12.md`, sezione 5) |
| Cartella Drive `A Amministrazione/` | PRESENTE | sotto `30 Staging pilota 2026-11`; gli id di questa cartella e delle sottocartelle sono nel passaggio `PASSAGGIO_2026-11-14_canale-A.md`, nella cartella di passaggio, non nel repository |
| Sottocartelle di CONTRATTI, sezione 7 A | PRESENTI, vuote (create il 14/11) | `registrazioni/`, `temporanei/`, `originali/`, `letture/`, `costi/`; i loro id vanno nel nodo «Inizio» dei flussi |
| Data table di n8n | PRESENTE | la licenza le ha (`GET /data-tables` 200), nessuna creata; le Variables no (403); i dati statici si salvano solo a fine corsa di produzione |
| API pubblica di n8n dal sandbox | PRESENTE | la chiave la mette il proxy (sezione 8) |
| GitHub | PRESENTE | solo come `QN-Builder` e solo per il coordinatore (DEC-029; CONTRATTI, sezione 4) |
| Gazetteer | PRESENTE | `raw.githubusercontent.com/QuartieriNews/QN/<commit>/gazetteer/gazetteer.json` risponde 200 dal sandbox; da n8n si prova in A5 |
| Prototipo dell'audio, `hls-audio.js` | PRESENTE, fuori dal repository | provato in locale con ffprobe e su n8n (921); sta nella cartella di passaggio (`30 Staging pilota 2026-11/`), con la sua prova locale, il codice della sonda e le note delle sonde, nessun testo delle fonti; entra in A3 con i test |
| Modello del flusso d'errore | PRESENTE | `staging_D_avviso`, che scrive solo nella cartella di D |
| Data table `staging_A_registrazioni` | PRESENTE (16/11) | creata dall'API con le colonne di `COLUMNS` e le due righe delle prese; l'id è nel passaggio di A2 su n8n |
| Nodi Code della sezione 5, con i test | quelli di A2 FATTI, provati con dati inventati; gli altri DA COSTRUIRE | A2 (sezione 5); A3–A5 |
| `staging_A_elenco` | PRESENTE per RomaTV, spento (16/11) | provato il 16/11 sulle versioni che hanno portato a quella esportata: 1341 (i controlli di `robots.txt` e 87 righe nuove), 1344 (righe già presenti), 1347 (una riga ricreata); 1348, sulla versione 2026-11-16.4 (la presa tenuta da un'altra corsa: attesa, poi presa; i nodi della presa sono gli stessi della versione esportata, a parte la riga `deferred_rows` di `recording-state.js`, che la presa non usa; la versione esportata aggiunge `deferred_rows` e toglie il riprovare ad «Aggiorna scheda», il tetto delle schede c'era già); 1350, sulla versione 2026-11-16.5 (una riga nuova con la scheda nuova, una ricreata con la scheda aggiornata, una cambiata, una seduta nuova vera); 1355, sulla versione esportata 2026-11-16.6, che ha i nodi Code di `main` dopo la #58, a parte l'orario, la scadenza di prova e il salvataggio delle corse riuscite (quattro cataloghi completi, sei sedute nuove). Il salto della fonte, con la presa tenuta oltre l'attesa, non è provato su n8n. Le corse riuscite non si salvano su n8n: ne resta il registro in `letture/` |
| `staging_A_testo`, poi `staging_A_lettura` e `staging_A_elementi` | DA COSTRUIRE | A3–A5 |
| `staging_A_avviso` | PRESENTE, acceso (16/11) | provato con un errore forzato; esportato in `workflows/` |
| Fixture dei test | DA COSTRUIRE | byte e testi inventati (DEC-109), mai presi da una fonte |
| Credenziali condivise e DEC-036 | DALL'OWNER, fatto il 14/11 | |
| Chiave di un servizio Whisper più economico, per il confronto dei modelli | DALL'OWNER, se il confronto lo prova | DEC-037, punto 4; sezione 6 |
| Chiave di un modello di un'altra famiglia, per la seconda verifica di DEC-015 | DALL'OWNER, con A5, se la PR di A5 la propone | la seconda verifica vale nel pilota (DEC-042); quali modelli la fanno lo propone A5, con l'indipendenza di DEC-015; su n8n oggi c'è solo OpenAI |
| Foglio della coda di revisione | DALL'OWNER, con A5 | non esiste su Drive |
| Piano n8n superiore | DALL'OWNER, solo se serve | se le corse chiamate da un altro flusso contano, A non sta nel piano già con A2 e A3: la domanda arriva con la misura di A2 (sezione 4) |

## 4. Architettura su n8n

| Flusso | Trigger | Ingresso | Uscita | Cartella |
|---|---|---|---|---|
| `staging_A_elenco` | orario, quello di CONTRATTI, sezione 7 A, «Raccolta» | i quattro cataloghi RomaTV; l'elenco dei video del canale del I da un Actor di Apify, quando la credenziale Apify è usabile (sezione 3) | righe `nuova` nella Data table, schede delle registrazioni, risposte come arrivano, registro della corsa, la spesa della corsa di Apify dell'elenco | `registrazioni/`, `originali/`, `letture/`, `costi/` |
| `staging_A_testo` | chiamato dall'elenco a fine corsa, e da sé stesso finché c'è lavoro, senza aspettare la fine; al massimo 8 corse al giorno (sotto, «Esecuzioni») | le registrazioni prese dalla Data table, una dopo l'altra, finché il budget di tempo non è finito | testo intero a pezzi, confini, testo della seduta aperta, le spese di ogni registrazione in ogni corsa | `temporanei/`, `originali/`, `costi/`, `letture/` |
| `staging_A_lettura` (A4) | chiamato dal testo a fine corsa, senza aspettare la fine, quando nella Data table c'è almeno una riga in `confini_fissati` senza una presa viva; prende con la presa quelle righe, una dopo l'altra, anche quelle rimaste da una corsa di testo morta prima di chiamarlo | il testo della seduta aperta | i fatti candidati | `letture/` |
| `staging_A_elementi` (A5) | da fissare in A5 | le letture | gli elementi | `A Amministrazione/` |
| `staging_A_avviso` | `errorWorkflow` di ogni `staging_A_*` | l'errore | `AVVISO_A_<ora UTC>.json`, senza testo | `letture/` |

**Lo stato** sta in una Data table, `staging_A_registrazioni`, una riga per registrazione: il
`recording_ref`, lo stato, il motivo di uno scarto, catalogo o canale, `municipality_code`, ora
di riferimento, durata, se c'è la trascrizione della piattaforma, la prima parte della seduta
quando è divisa, il segmento da cui riprendere, i tentativi, la presa e, per un video di
YouTube, l'id della corsa di Apify e del suo storage. Mai un testo. La scheda in
`registrazioni/` copia lo stato quando cambia (CONTRATTI, sezione 7 A). Nella stessa tabella
stanno le righe delle prese (`lease:romatv`, `lease:youtube`), quelle degli host
(`host:<nome>`: se è fermo e fino a quando, gli errori di fila, il giorno dell'ultimo controllo di
`robots.txt`) e quelle di YouTube (`fonte:youtube_elenco`, il suo stato e l'ultimo giorno riuscito;
`fonte:youtube_audio`, i video del giorno). Le colonne sono `COLUMNS` di
`code-nodes/recording-state.js`.

| Stato | Lo mette | Vuol dire |
|---|---|---|
| `nuova` | elenco | vista e dentro il perimetro |
| `testo_in_corso` | testo | pezzi del testo intero in `temporanei/`; la riga dice da quale segmento riprendere, i file lo confermano (sotto, «La ripresa del testo») |
| `testo_completo` | testo | testo intero in `temporanei/`; se c'è già il testo della seduta aperta in `originali/`, il confine è fatto (sotto, «La ripresa del confine») |
| `confini_fissati` | testo | testo della seduta aperta in `originali/`; niente più in `temporanei/` |
| `letta` | lettura (A4) | fatti candidati in `letture/` |
| `scartata` | elenco o testo | fuori perimetro, confine non fissabile, video di YouTube uscito dalla finestra senza testo: il motivo è nella riga; niente in `temporanei/`. Un video di YouTube di cui non si ottengono né l'audio né i sottotitoli non si scarta e non va in `errore`: resta `nuova`, con l'avviso, e si riprova nelle corse dopo finché è dentro la finestra (DEC-037, punto 3). Ogni quanto si riprova lo stesso video e si avvisa, e se una ripresa conta fra i 5 video al giorno, lo fissa la PR del testo (A3), con i test (T-A3-22) |
| `errore` | qualunque flusso | tre tentativi falliti; parte l'avviso; la riga tiene lo stato da cui è caduta. Si riparte solo a mano, da quello stato, con i campi che dà la fase `restart` di `recording-state.js`, e per un video di YouTube solo dopo che la pulizia del giorno ne ha cancellato lo storage su Apify (sotto, «La pulizia»): caduta durante il testo, i suoi file in `temporanei/` si cancellano subito e si riparte dal primo segmento; caduta in lettura o negli elementi, si riparte da `confini_fissati` o da `letta`, con il testo della seduta aperta che è già in `originali/` |

**La presa.** Una corsa scrive nella riga il proprio id di esecuzione e una scadenza (ora più 5
minuti) solo se la riga è libera o la presa è scaduta, poi rilegge la riga e lavora solo se la
presa letta è la sua. Il «solo se» sta nella scrittura stessa: l'aggiornamento del nodo Data table
porta la condizione, che `recording-state.js` dà con i campi (`claim`: `presa_fino_ms` passata, o
per il rinnovo `presa_id` uguale; `release`: `presa_id` uguale), con «Must Match: All Conditions»
(`where.match`; il nodo parte da «Any»). Le righe delle prese delle fonti si scrivono libere
quando si crea la tabella (`LEASE_SEED`); quelle delle registrazioni nascono con le colonne della
presa. Una riga si legge per `ref`, una per voce, mai con un elenco che il nodo tronca a 50
righe. Se il filtro si applica nello stesso aggiornamento lo verifica la prima prova su n8n.
L'elenco di YouTube tiene `lease:youtube` per tutta la sua attesa della corsa dell'Actor, al più
20 minuti («I limiti misurati»), e la rinnova a ogni giro dell'attesa, che non supera il minuto. Ogni passo rinnova la scadenza; a fine corsa la presa si lascia. Due corse
non lavorano sulla stessa registrazione, e una corsa morta libera la riga in 5 minuti. Lo stesso
meccanismo, su una riga per fonte (`lease:romatv`, `lease:youtube`), tiene una richiesta alla
volta per fonte anche fra flussi diversi (CONTRATTI, sezione 7 A, «Raccolta»). La sua grana è la
corsa, non la richiesta: un nodo Code non legge né scrive una Data table (nessuna sonda lo
prova), lo fa il nodo Data table, che prende la presa prima del giro sulla fonte, la rinnova a
ogni pezzo e la lascia alla fine; una corsa di testo la tiene quindi fino a 4 minuti. Chi la
trova presa: l'elenco aspetta, con un nodo Wait, al più fino alla scadenza della presa
(5 minuti), poi salta quella fonte in quella corsa e lo scrive nel registro (lo sguardo indietro
di 100 giorni recupera alla corsa dopo); il testo non comincia e finisce pulito, perché lo
richiama l'elenco a fine corsa. L'ordine di scrittura è: file su Drive, poi la riga; un file
già presente con lo stesso nome si sostituisce (specifica v2.5, fase 5.2), così una ripresa non
lascia doppioni. La riga di una registrazione si scrive con un upsert sul suo `ref`, così la
stessa registrazione due volte in una corsa dà una riga sola. Uno stop di un host o dell'elenco
di YouTube dà il suo avviso subito, scritto prima della riga (`AVVISO_A_<ora>_<host>.json`,
`…_youtube_elenco.json`); un elenco letto incompleto dà `AVVISO_A_<ora>_elenchi.json` a fine
corsa, tranne quando l'host era già fermo.

**La ripresa del testo.** Per il testo comandano i file, non la riga, che dice solo da dove
cominciare a guardare. Prima di chiamare OpenAI per una registrazione, una corsa elenca i file
dei suoi pezzi in `temporanei/` (la strada dell'audio, passo 7) e comincia dal primo pezzo
che non ha il suo file con il modello in uso. Un testo ha un modello solo, perché
`transcript_source` è uno e entra nel `source_hash` (CONTRATTI, sezione 7 A): se ci sono pezzi di
un altro modello, perché A4 ha cambiato modello mentre la registrazione era in
`testo_in_corso`, la corsa li cancella per sempre, dopo il controllo delle spese qui sotto, e
il testo riparte dal primo pezzo. Il cambio costa al più il testo già fatto delle
registrazioni in corso in quel momento. Un testo ha anche una fonte sola: se la trascrizione
della piattaforma compare mentre la registrazione è in `testo_in_corso`, la corsa, dopo lo stesso
controllo delle spese, cancella per sempre i pezzi e usa quella, che non costa (CONTRATTI,
sezione 7 A, «Testo»). La spesa già fatta resta in `costi/`, non se ne fa altra, e
`transcript_source` è quello della piattaforma; un testo già in `testo_completo` o oltre resta il
nostro (T-A2-05). Poi elenca le spese della registrazione in `costi/`: per ogni
esecuzione che ha scritto pezzi senza scrivere le sue spese, le scrive lei, con l'id di
quell'esecuzione e l'uso letto nei file dei pezzi. Lo stesso controllo delle spese viene prima
di ogni cancellazione in `temporanei/`. Così una corsa che muore dopo il file di un pezzo e
prima della riga non fa ripetere la spesa dei pezzi già scritti, e le sue spese non si
perdono; una spesa già scritta ha lo stesso nome e si sostituisce, non si conta due volte. Resta
un caso: una corsa che muore fra la risposta di OpenAI e il file del pezzo fa rifare quel
pezzo, e la prima spesa non arriva in `costi/`. È al più un pezzo di 60 secondi, meno di un
centesimo di dollaro (0,003 $ con `gpt-4o-mini-transcribe`, 0,006 $ con `whisper-1`, ai prezzi
di CONTRATTI, sezione 7 A, «Costi»).

**La ripresa del confine.** Anche dopo il testo, nessun passo che spende o cancella si fida della
riga: prima lascia un file con un nome che dipende solo da che cosa è, e una corsa riparte dai
file (sezione 5, «Il confine»).
- Ogni chiamata del modello del confine scrive subito la risposta e l'uso in un suo file di
  `temporanei/`, con un nome che dipende solo dalla registrazione, dal modello e dall'inizio del
  tratto letto. Una corsa che trova quel file non rifà la chiamata, e il controllo delle spese
  legge questi file come quelli dei pezzi. Come per i pezzi, una corsa che muore fra la risposta
  e il file fa rifare quella sola chiamata, e quella spesa non arriva in `costi/`: i token di un
  tratto.
- Il testo della seduta aperta va in `originali/` con un nome che dipende solo dalla
  registrazione, ed è il segno che il confine è fatto. Una corsa che lo trova per una riga ancora
  in `testo_in_corso` o `testo_completo` non chiede audio, non chiama OpenAI e non rifà il
  confine: fa il controllo delle spese, cancella per sempre quello che resta della registrazione
  in `temporanei/` e mette la riga in `confini_fissati`. Così una corsa che muore dopo quel file
  e prima della riga non fa ripetere niente, anche se ha già cancellato una parte dei pezzi.

**La pulizia.** Una registrazione che si ferma prima del confine non lascia testo in
`temporanei/` (CONTRATTI, sezione 7 A, «Confine della seduta»). Quando il testo mette una riga in
`errore`, o la scarta, cancella per sempre i suoi file di `temporanei/`, dopo il controllo delle
spese. La prima corsa di testo di ogni giorno di Roma elenca `temporanei/` e cancella per sempre i
file di ogni registrazione che non è in `testo_in_corso` o `testo_completo`, o che non ha una
riga, saltando le righe con una presa viva. Così un file sfuggito a una cancellazione, per
esempio con Drive che non risponde proprio mentre la riga va in `errore`, non resta più di un
giorno. La pulizia la fa il testo e non l'elenco perché legge l'uso nei file dei pezzi, che
hanno il testo: i dati delle esecuzioni del testo non si salvano (sotto, «Dati delle
esecuzioni»). La stessa pulizia cancella su Apify lo storage delle corse di YouTube di ogni
riga che non è in `testo_in_corso`, o che non ha una riga: quello di una riga finita in
`errore` o `scartata`, e quello rimasto dopo un testo completo. Finché la riga è in
`testo_in_corso` lo storage resta, anche dopo una corsa morta, perché la corsa dopo riprende
dal pezzo seguente senza un'altra corsa dell'Actor (DEC-037, punto 2; T-A3-22).
Ripartire a mano una registrazione caduta durante il testo la rimette in `nuova`, dal primo
segmento: la spesa si rifà, al più circa 0,6 $ con `gpt-4o-mini-transcribe` per le
3,5 ore della prova dell'Assemblea (sezione 6), sotto la soglia di DEC-036, punto 6. Una caduta
dopo il confine riparte dallo stato da cui è caduta, senza audio e senza trascrizione.

**I limiti misurati.**
- `executionTimeout`: n8n Cloud taglia a 300 secondi un flusso che lo imposta, insieme ai
  sotto-workflow che chiama e aspetta (CONTRATTI, sezione 2, D: prova del 12 novembre 2026);
  senza, una corsa dura ore (D, esecuzione 762: 2 ore e 12). I flussi che toccano l'audio
  impostano 300 e tengono un budget di tempo nel codice di 4 minuti, come `readingBudget` di
  `code-nodes/archive-record.js`: la corsa si ferma pulita al budget, con la riga che dice da
  dove riprendere. Quanto audio ci sta lo misura A3: con le pause della riga «Raccolta» lo
  scarico da solo prende da 8 a 10 minuti per ora di audio, e la trascrizione si aggiunge,
  quindi meno dei 30 minuti per corsa stimati all'apertura: circa 20–25.
- Catene: il testo chiama sé stesso e la lettura senza aspettare che finiscano (nodo Execute
  Workflow con l'attesa spenta), così ogni corsa ha i suoi 300 secondi e una catena non muore
  dentro quelli della prima corsa. A2 lo prova con una sonda, `staging_A_sonda_catena`: un
  flusso a 300 secondi che si chiama due volte senza aspettare; l'ultima corsa deve finire
  oltre i 300 secondi della prima. Provato il 16 novembre 2026 (esecuzioni 1330, 1331, 1333):
  tre corse da 200 secondi, l'ultima finita 602 secondi dopo l'inizio della prima, nessuna
  tagliata. Su n8n 2.x un flusso chiamato deve essere acceso: la 1329, partita dall'orario, si è
  fermata alla propria chiamata, fatta a sonda già spenta, con «Workflow is not active and
  cannot be executed»; `staging_A_testo`
  resta quindi acceso, anche se parte solo da chiamata.
- Esecuzioni, misurate da A2 il 16 novembre 2026: il contatore del piano letto dall'owner è
  salito da 268 a 273 per tre corse da trigger (1329, 1330 della sonda; 1332, il flusso B) e
  due chiamate senza aspettare (1331, 1333). Fino alla lettura, l'API elenca dal 9 novembre 534
  esecuzioni salvate: 191 da trigger, webhook o errore e 343 corse di D chiamate aspettando
  (`waitForSubWorkflow: true`). Le esecuzioni dell'istanza cominciano il 9 novembre; il
  ragionamento vale se il periodo del contatore, quello della fatturazione, comprende tutto il
  9–16 novembre (la data in cui riparte si legge nel pannello del piano). Se queste contassero, il contatore non
  potrebbe essere a 268:
  non entrano nel contatore (la differenza fra 191 e 268 sono esecuzioni cancellate o non
  salvate, che l'API non elenca). Una corsa chiamata conta quindi quando chi la chiama non la aspetta, cioè ogni
  corsa del testo e della lettura. L'owner ha deciso il 16 novembre 2026 che l'obiettivo di 500
  corse per A, scritto all'apertura, non vale più: il limite è il piano di 2.500, comune a tutti
  i canali, con il margine per gli altri; il tetto del testo lo fissa A3 sul tempo misurato, e
  il contatore del piano si legge ogni mese. Il conto che segue è quello dell'apertura.
- Esecuzioni: 2.500 al mese sul piano Starter, con B e D. Oggi B e D fanno 25–29 corse al
  giorno da trigger e circa 49 corse chiamate da un altro flusso (sotto-workflow): 750–870 al
  mese se le seconde non contano, 2.220–2.340 se contano. Obiettivo di A: al massimo 500 corse
  che contano. Conto di giugno: elenco 240 (8 corse al giorno, da trigger). Testo: una corsa
  prende più registrazioni in fila finché il budget non è finito, e le 123,3 ore di RomaTV a
  20–25 minuti per corsa fanno 300–370 corse; con una registrazione per corsa, la riserva se
  una corsa non
  riesce a prenderne più di una, 350–430 corse per 117 registrazioni (304 a 30 minuti per
  corsa, dal CSV A3). I testi senza audio (20 Consigli con la trascrizione della piattaforma)
  entrano nelle stesse corse. I 77 video del I non sono più testi senza audio (DEC-037): sono
  altre 42,1 ore da trascrivere, 165,4 in tutto. Alla resa di RomaTV sarebbero altre 100–125
  corse al mese; ma il loro audio arriva da Apify in un file, senza le pause dei segmenti, e
  quante corse servono lo misura A3. Il testo è chiamato dall'elenco e da sé stesso: è un
  sotto-workflow.
  - Se le corse chiamate non contano (insights: 143 di produzione contro 382 salvate, 245
    chiamate; non provato), di A conta solo l'elenco, 240, e con B e D si arriva a 990–1.110:
    il piano basta.
  - Se contano, B e D lasciano 160–280 corse: l'elenco da solo ne prende 240 e il testo non ci
    sta più. A non sta nel piano già con A2 e A3, non solo con A4 e A5. A2 lo misura per primo,
    con la sonda della catena (il contatore del piano prima e dopo un numero noto di corse,
    letto dall'owner nel pannello di n8n se l'API non lo dà), prima di accendere l'elenco a
    orario; se contano, la domanda sul piano va all'owner allora (sezione 9).
  - Il tetto del testo veniva dall'obiettivo: 500 − 240 = 260 corse al mese, cioè 8 al giorno.
    Superato dalla decisione dell'owner del 16 novembre (sopra): lo rifissa A3 sul tempo
    misurato. Con 8 corse da 20–25 minuti si trascrivono 80–100 ore al mese, meno delle
    123,3 di giugno di RomaTV, e molto meno delle 165,4 con il Municipio I: anche questo va
    nella domanda all'owner.
- Binari e memoria: un binario costruito in base64 in un nodo Code resta nel JSON
  dell'esecuzione, senza id, e ogni nodo che lo passa ne fa una copia (921: 12,4 MB di base64
  per 9,3 MB di M4A, nel nodo «Audio» e di nuovo in «Di nuovo 1»; 919: 44 MB di esecuzione per
  due binari da 5,5 MB su tre nodi). Fra il nodo Code e il nodo HTTP di OpenAI passa un pezzo
  alla volta, ma n8n tiene l'uscita di ogni giro del ciclo fino alla fine della corsa: una corsa
  di 30 pezzi tiene circa 30 × 1,24 MB, circa 37 MB di base64, più le copie. Un nodo dopo
  l'invio a OpenAI non porta avanti il binario. La memoria per esecuzione del piano Starter non
  è misurata: la misura la prova dell'Assemblea (sezione 6).
- Dati delle esecuzioni: per testo, lettura ed elementi `saveDataSuccessExecution` e
  `saveDataErrorExecution` sono `none`, `saveManualExecutions` e `saveExecutionProgress` sono
  `false` (DEC-036, punto 5; CONTRATTI, sezione 7 A, «Testo»: l'audio non si scrive mai su
  Drive né su n8n). Un errore si legge dall'avviso di `staging_A_avviso`, con flusso, nodo,
  messaggio e ora; l'id dell'esecuzione può mancare, perché l'esecuzione non si salva.
  Nessun nodo di esito porta un campione di testo (la sonda 921 lo faceva; quell'esecuzione
  è cancellata).
- L'elenco di YouTube (`youtube-list.js`, come `apify-run.js` per C). La richiesta che avvia la
  corsa dell'Actor porta il suo tempo massimo, 15 minuti, il tetto dei video chiesti e quello della
  spesa: alla prova del 20 novembre Apify non ha tenuto al tetto dei video l'Actor scelto, che si
  paga a evento (80 voci addebitate con un tetto di 75); il tetto che un Actor a evento rispetta è
  quello della spesa (`maxTotalChargeUsd`, T-A2-16), sopra una finestra piena al prezzo della prova
  (sezione 7). Secondo la documentazione di Apify, al tetto della spesa la corsa si interrompe
  (`ABORTED`): è una corsa fallita (T-A2-10); alla prova nessuna corsa l'ha raggiunto, e il suo
  comportamento non è ancora misurato. Il flusso la aspetta al più
  20 minuti e ne scrive la spesa dopo che si è assestata. L'id della corsa va nella riga
  `fonte:youtube_elenco` appena parte, e lì resta finché la corsa non si legge: se l'esecuzione
  muore, o la corsa aspetta ancora dopo 20 minuti, la corsa dopo la riprende, con la sua spesa,
  prima di avviarne un'altra, anche con l'elenco fermo (riprendere non chiede niente a YouTube).
  Una corsa che aspetta ancora dopo 20 minuti lascia l'elenco non letto in quella corsa: il
  registro lo dice incompleto, con il motivo, e parte l'avviso; conta nella serie come una corsa
  fallita, ma il suo id resta nella riga e la sua spesa si scrive quando la corsa si legge.
  Cinque di fila fermano l'elenco con il suo avviso, e la corsa resta da riprendere finché Apify
  non la chiude o non la si interrompe su Apify.
  Vanno in `lost`, e contano come corsa fallita, solo un avvio che Apify rifiuta (400, 402, 404:
  senza file di costo, perché non c'è una corsa), una corsa ripresa che Apify non ha più (con un
  file di costo dai valori `null`) e uno stato che non si conosce (il suo file di costo porta la
  corsa come Apify l'ha data). Un blocco dell'API (401, 403, 429) ferma Apify con il suo avviso e
  non conta nella serie; un errore del server lascia l'id nella riga per la corsa dopo. Restano tre casi rari: un'esecuzione che muore fra l'avvio della
  corsa e la scrittura del suo id lascia una corsa senza file di costo, come per C
  (`workflows/README.md`); una corsa ripresa e sparita dopo che il suo file di costo era già
  scritto ne sostituisce la spesa con `null`; un'esecuzione che muore durante l'attesa libera
  `lease:youtube` dopo 5 minuti, e una corsa lasciata dopo 20 minuti la lascia a fine corsa,
  mentre l'Actor può lavorare ancora: per questo A3 non avvia un Actor di YouTube finché
  `fonte:youtube_elenco` ha un `apify_run_id` (T-A3-22).
  Alla prova l'Actor ha dato i video dal più recente (il criterio di «Raccolta» lo presuppone).
  Dal 1° al 19 novembre il canale ne ha pubblicati 55 in 19 giorni, 2,9 al giorno, più di giugno
  (2,6 al giorno, circa 257 in 100 giorni): a finestra piena sarebbero circa 290, dentro i 300,
  con poco margine; è una stima, perché la prova ha coperto la finestra di quel giorno (19 giorni).
  Se il ritmo sale, l'elenco esce incompleto con il suo avviso, e il tetto si rivede.
- Le schede e le righe di una corsa dell'elenco si scrivono dopo l'ultimo rinnovo della presa,
  al più 25 nuove e 25 cambiate per corsa: un file su Drive ha preso circa 3 secondi
  (esecuzione 1341), così la scrittura sta dentro la presa. Le altre le scrive la corsa dopo, che
  le ritrova; il registro le elenca (`deferred_rows`). Accade dopo un fermo lungo o alla prima
  corsa. Una scheda che Drive non scrive ferma la corsa, con l'avviso, senza riprovare: la corsa
  dopo ritrova le schede per nome e riscrive le righe.
- Le risposte dell'elenco in `originali/` (CONTRATTI, sezione 7 A, «Raccolta»): lettura del
  builder, del 16 novembre, che l'owner conferma con il merge. Ci vanno le risposte che
  `source-guard.js` giudica dati (`ok`), con il corpo JSON come n8n lo ha letto e riscritto;
  una risposta che ferma l'host o lascia l'elenco incompleto resta nel registro e nell'avviso,
  con il suo motivo.
- Prove con un trigger a orario: ogni corsa di prova ha una scadenza scritta nel codice, perché
  lo spegnimento via API arriva tardi (l'esecuzione 922 è partita un minuto dopo la 921).

**La strada dell'audio** (sonde 919 e 921, prototipo `hls-audio.js`):
1. Dalla voce dell'elenco, il file SMIL `AudioOnly` su `ovp2-live.akamaized.net`;
   `<smil>/playlist.m3u8` dà la playlist principale (`BANDWIDTH=48000`), che dà la chunklist.
2. Chunklist: segmenti `.aac` da 10 secondi, un `EXT-X-KEY` per segmento, la stessa chiave e un
   IV diverso per segmento (163 su 163). L'IV si legge dalla playlist: la sonda 919, con l'IV del
   primo segmento per tutti, ha trovato l'ID3 in 1 segmento su 36.
3. Chiave: 16 byte da `api-ovp.streamcloud.it`; una volta per registrazione e per indirizzo
   distinto, mai riusata per un'altra registrazione. Le sonde hanno mandato `Origin` e `Referer` del portale, come
   fa il lettore, alla chiave e all'elenco, mai senza: se servono non è provato. A2 (elenco) e
   A3 (chiave) provano una volta senza: se rispondono, non si mandano; se no, la PR che lo
   misura scrive in CONTRATTI, sezione 7 A, che le richieste portano `Origin` e `Referer` del
   portale, come ha accettato l'owner con «come fa il lettore» (DEC-036, punto 2).
4. Segmenti uno alla volta, in ordine: AES-128-CBC con il loro IV, poi via il tag ID3, poi le
   trame ADTS (sincronia `0xFFF1`, 48 kHz, mono). Bitrate vero circa 124 kbps. In n8n, 60
   segmenti (10 minuti) si sono scaricati e decifrati in 27 secondi, con una pausa di 0,1
   secondi; con le pause della riga «Raccolta» ci vogliono da 8 a 10 minuti per ora di audio.
5. Ogni 6 segmenti (60 secondi) un M4A costruito nel nodo Code, senza ricodifica: circa 0,93 MB
   al minuto, lontano dal limite di 25 MB per richiesta di OpenAI. L'ADTS grezzo OpenAI lo
   rifiuta, anche rinominato.
6. `gpt-4o-mini-transcribe` su ogni pezzo, che prende come tempo il suo inizio. Su 10 minuti: 15
   secondi, 6.000 token audio e 1.756 in uscita, nessun tempo interno; `whisper-1` con
   `verbose_json`: 27 secondi, 80 segmenti con i tempi, 601 secondi fatturati.
7. Ogni pezzo trascritto va subito in un suo file di `temporanei/`, con un nome che dipende
   solo dalla registrazione, dal modello di trascrizione e dal numero del pezzo: il testo con i
   tempi, l'uso restituito da OpenAI e l'id dell'esecuzione. Alla fine della corsa l'uso dei pezzi che ha scritto diventa
   le spese della registrazione in quella corsa, in `costi/` (riga «Costi»); poi la riga
   avanza. Se una corsa muore a metà, la successiva riparte dai file (sezione 4, «La ripresa
   del testo»). Sono circa sei scritture al minuto su Drive: A3 misura che stiano nella quota
   per minuto della credenziale (sezione 3). L'audio non si scrive mai.
8. A testo completo, il confine (sezione 5, A3) taglia la seduta aperta, che va in `originali/`
   (il segno che il confine è fatto: sezione 4, «La ripresa del confine»),
   e, dopo il controllo delle spese (sezione 4, «La ripresa del testo»), i file della
   registrazione in `temporanei/` si cancellano per sempre: il nodo Google Drive
   di n8n con la cancellazione definitiva (`deletePermanently`), mai il cestino, dove un file
   resta circa 30 giorni con le sue revisioni; poi la riga va in `confini_fissati`. Il connettore Drive delle sessioni sa solo
   spostare nel cestino: in `temporanei/` cancella solo n8n.

## 5. Ordine di costruzione

Una PR di A alla volta nel giro di revisione (protocollo, sezione 2, punto 3). Ogni PR porta i
suoi nodi Code (una fonte, due contesti: `code-nodes/README.md`), i test con la riga in
`package.json`, e l'esportazione dei flussi in un commit separato. I nomi dei file nuovi sono
proposte: li fissa la PR che li porta.

| PR | Che cosa | Nodi Code e test | Su n8n e Drive |
|---|---|---|---|
| A1 apertura (questa), in due PR perché insieme passano le 1.000 righe (protocollo, sezione 2, punto 4) | A1a: CONTRATTI, sezioni 5, 6 e 7 A; DEC-036; questo brief. A1b: il nodo e i test | A1b: `institutional-identity.js`, `tests/test_institutional_identity.js` | niente |
| A2 raccolta, in due PR perché insieme passano di molto le 1.000 righe (protocollo, sezione 2, punto 4) | elenco dei cataloghi e, per YouTube, dei video del canale da un Actor di Apify (DEC-037), schede, stato, presa, stop delle fonti, controllo di `robots.txt`. A2a: i nodi e i test. A2b: il flusso, costruito sui nodi già rivisti, con la sua esportazione | A2a: `source-guard.js`, `romatv-list.js`, `youtube-list.js`, `recording-state.js`, con i loro test (T-A2-01…T-A2-13). A2b: T-A2-14 in `tests/test_workflow_exports.js` | A2a: niente. A2b: Data table; `staging_A_elenco`; `staging_A_avviso`; le sonde della sezione 6 |
| A3 testo | la strada dell'audio di RomaTV; l'audio di YouTube da un Actor di Apify, con la riserva e, per ultimi, i sottotitoli automatici (DEC-037, punto 3); i pezzi da 60 secondi; i testi della piattaforma (JSON del parlato, WebVTT di riserva) e i sottotitoli di YouTube in una forma sola con i tempi; il confine della seduta; le spese | `hls-audio.js` (dal prototipo nella cartella di passaggio, sezione 3), `youtube-audio.js`, `recording-text.js`, `session-boundary.js` | `staging_A_testo` |
| A4 lettura | i fatti candidati secondo `tools/sources-study/report2/SPECIFICA_VIDEO.md`, con l'evidenza `[mm:ss]`, in `letture/`, senza il riscontro con atti e notizie (sotto, «Il riscontro»); il modello di trascrizione si fissa qui, dopo il confronto (sezione 6) | il nodo della lettura | `staging_A_lettura` |
| A5 elementi | il riscontro con atti e notizie (sotto); geografia con una porta JS della risoluzione del gazetteer sui luoghi estratti; classi editoriali di `institutional` dal build del gazetteer; seconda verifica di DEC-015; coda di revisione; proiezione per il prototipo | la porta del gazetteer, la scrittura dell'elemento | `staging_A_elementi`; gli elementi in `A Amministrazione/` |

**Il confine (A3).** `session-boundary.js` cerca nel testo con i tempi gli atti formali di
`SPECIFICA_NOMI_E_TERRITORIO.md`, sezione 2, e ne ricava gli intervalli della seduta aperta.
Dove le formule mancano o si contraddicono, un modello legge solo i tratti intorno ai candidati
(costo nella riga della lettura, sezione 7). Le parti di una seduta divisa si legano in ordine
(lo stato alla fine di una parte è lo stato all'inizio della successiva, e una parte aspetta la
precedente) solo quando la fonte le dichiara: stesso catalogo, organo e giorno di Roma; titoli
che dicono la parte («parte 1», «I parte», «seconda parte») con numeri che si seguono; nessuna
sovrapposizione, cioè la parte dopo comincia dopo la fine della precedente (ora di riferimento
più durata). Stesso organo e stesso giorno non bastano. Lettura del builder (A2,
`code-nodes/romatv-list.js`): l'organo è quello che il portale dà (`governmentBody`), se no il
titolo senza la parte, come pubblicato; due registrazioni hanno lo stesso organo quando questo
coincide senza maiuscole, spazi e punteggiatura. Un video di YouTube non si lega mai: sta a sé. A giugno, con l'organo come lo dà il
CSV A3, 127 gruppi di catalogo, organo e giorno su 300 hanno più di una registrazione, e in 118
coppie consecutive la seconda comincia prima che finisca la prima: per esempio due commissioni
del X del 9 giugno, alle 13:00 per 68 minuti e alle 14:00. Ogni altra registrazione sta a sé.
Lettura del builder: comincia fuori seduta, e la seduta si apre al primo atto formale, come una
ripresa non dichiarata (`SPECIFICA_NOMI_E_TERRITORIO.md`, sezione 2). Così un dubbio costa al più
il primo tratto di una parte non legata, mai materiale di prima dell'apertura. Il registro della
corsa dice quali registrazioni dello stesso organo e giorno non si sono legate, e perché. Una
parte aspetta la precedente solo finché questa può finire: se la precedente è `scartata` o in
`errore`, la successiva non aspetta più, si fa come una registrazione a sé, e il registro lo
dice; se la precedente riparte a mano più tardi, la successiva resta com'è. Se il confine non si
fissa: DEC-036, punto 5. Le spese del modello che legge i tratti intorno ai candidati vanno in
`costi/` come quelle della trascrizione (CONTRATTI, sezione 7 A, «Costi»), e ogni sua risposta va
prima in un file (sezione 4, «La ripresa del confine»).

**Il riscontro (A4 e A5).** `novita_rispetto_agli_atti` di `SPECIFICA_VIDEO.md` (l'emendamento del
16 settembre) vale `solo dal parlato` solo quando il fatto non compare in nessun atto e in nessuna notizia
già estratta. Nello studio il riscontro era sugli atti di un mese chiuso; nel pilota gli atti
(canale D) e le notizie (canale B) arrivano anche dopo la lettura, che parte appena il confine è
fissato. Per questo A4 non fa il riscontro e non scrive quel campo. Lo fa A5, sugli atti e sulle
notizie che ci sono in quel momento, e scrive la data del riscontro e su quale materiale è
fatto, come chiede la specifica. Un `solo dal parlato` resta provvisorio, e A5 lo rifà quando D
o B aggiungono atti o notizie. Quante volte, per quanto tempo e con quale test lo fissa la PR di
A5.

## 6. Prove

**Test unitari** (CI, `npm test`), con fixture inventate; un id per caso nel nome del test.

A1: T-A1-01…T-A1-19 in `tests/test_institutional_identity.js`: identità, nomi dei file,
colonne della coda, ora e durata, `source_hash`, l'adattatore di n8n.

A2 (T-A2-01…T-A2-13 con A2a; T-A2-14 con A2b; T-A2-15 e T-A2-16 con la prova degli Actor del 20 novembre):
- T-A2-01 una pagina di catalogo: guid in minuscolo, titolo come pubblicato, ora di riferimento
  con offset portata in UTC, durata `hh:mm:ss.fffffff` in secondi, trascrizione della
  piattaforma riconosciuta dalle tracce, SMIL solo audio.
- T-A2-02 `municipality_code` dal catalogo: una voce di `Municipio X` intitolata «Commissione IV …»
  ha X; i cataloghi capitolini non danno un Municipio.
- T-A2-03 l'inizio: una seduta alle 00:30 del 1° novembre di Roma entra, una del 31 ottobre no.
- T-A2-04 la finestra (CONTRATTI, sezione 7 A, «Raccolta»): le pagine si fermano alla prima voce
  di una seduta di più di 100 giorni prima o anteriore al 1° novembre; una pubblicazione tardiva
  entra, anche a 51 e a 94 giorni dalla seduta, una a 101 no; una voce già vista non dà una
  seconda riga.
- T-A2-05 la trascrizione della piattaforma aggiunta dopo: la scheda si aggiorna; se il nostro
  testo non è iniziato si usa quella, se è in corso si passa a quella (T-A3-19), se è fatto
  resta il nostro, senza seconda spesa.
- T-A2-06 seduta divisa (sezione 5, «Il confine»): due parti dichiarate dai titoli, in ordine e
  senza sovrapposizione, si legano. Restano separate, e il registro le elenca: due registrazioni
  dello stesso organo e giorno senza parti dichiarate; due parti che si sovrappongono, come la
  coppia del 9 giugno, con dati inventati; una «seconda parte» senza la prima.
- T-A2-07 gli stop di RomaTV della riga «Raccolta», uno per caso: l'host si ferma, parte
  l'avviso, e riparte solo quando l'owner lo dice; un errore del server lascia la voce per la
  corsa dopo, cinque di fila fermano l'host fino al giorno dopo.
- T-A2-08 `robots.txt` cambiato rispetto al 14 novembre, o illeggibile dove si leggeva, nella
  lettura di CONTRATTI, sezione 7 A, «Raccolta»: l'host si ferma e parte l'avviso.
- T-A2-09 elenco di YouTube da un Actor di Apify (DEC-037, punto 2), con un Apify finto:
  `youtube:<id>` solo per un id di 11 caratteri; `source_id` è il canale; si tengono i video
  dentro la finestra di T-A2-04, e un video già visto non dà una seconda riga; un elenco che
  non arriva a coprire la finestra è incompleto, con il motivo e l'avviso; la corsa
  dell'elenco ha il suo file di costo.
- T-A2-10 gli stop della riga «Raccolta» su Apify, uno per caso: un 401, 403 o 429 dell'API
  di Apify ferma Apify, parte l'avviso, e riparte solo quando l'owner lo dice, come per
  RomaTV (T-A2-07); una corsa fallita dell'Actor dell'elenco lascia l'elenco non letto in
  quella corsa e ha il suo file di costo, e cinque di fila fermano l'elenco fino al giorno
  dopo, con l'avviso; una corsa lasciata perché aspetta ancora dopo 20 minuti lascia anche lei
  l'elenco non letto in quella corsa e conta nella serie, con il suo id che resta nella riga e
  senza file di costo finché non si legge; con Apify fermo nessuna richiesta parte; nessuna richiesta va a YouTube, né
  al sito né all'interfaccia ufficiale; ogni richiesta di n8n porta lo user agent dichiarato.
- T-A2-12 il ritmo della riga «Raccolta», con un orologio finto: le pause minime per host,
  dalla fine di una risposta alla richiesta seguente (5 secondi agli host di RomaTV, 1 a quello
  dei media), una richiesta alla volta per fonte, e per YouTube la cadenza dell'elenco che
  fissa A2, un video alla volta e al più 5 video per giorno di Roma (`youtube-list.js`); le pause
  stanno in `source-guard.js`, che dà il ritmo anche ai segmenti di A3, e la richiesta alla volta
  nella presa (`recording-state.js`).
- T-A2-11 la presa: due corse sulla stessa riga, una sola lavora; una presa scaduta si riprende;
  gli stati cambiano solo lungo la tabella della sezione 4. La presa di una fonte tenuta dal
  testo: l'elenco aspetta al più fino alla scadenza, poi salta la fonte e lo scrive nel
  registro; il testo che la trova presa non comincia.
- T-A2-14 (A2b: arriva con il flusso, non con i nodi) esportazione di `staging_A_elenco`
  (`tests/test_workflow_exports.js`): i nodi Code identici ai file; `fetch` riceve un item per esecuzione; ogni scrittura della presa e
  di una riga porta il suo `where`, con «Must Match» preso da `where.match`; una riga si legge per
  `ref`; il file dell'avviso viene prima della riga dell'host o dell'elenco; ogni nodo HTTP verso
  Apify viene dopo `may`, porta lo user agent dichiarato e passa la risposta ad `answer`; da
  `poll`, `leave` scrive la lettura nel registro e lo stato dell'elenco nella sua riga, con l'id
  della corsa, e finisce la corsa, e `lost` passa dalla fase `lost`; `poll` riceve la riga
  dell'elenco (`list_row`) e `lost`, per uno stato che non si conosce, la corsa (`run`); un blocco
  o un errore del server dell'API di Apify non arriva mai a `lost`.
- T-A2-13 il tetto delle pagine (CONTRATTI, sezione 7 A, «Raccolta»): un catalogo che ripete
  una pagina, le cui date risalgono da una pagina all'altra, o che in 4 pagine non esce dalla
  finestra di T-A2-04 si ferma, mai oltre la quarta richiesta; il registro
  lo dice incompleto, con il motivo, e parte l'avviso; gli altri cataloghi della corsa si
  leggono.
- T-A2-15 una voce di errore dell'Actor dell'elenco (la forma che ne dà la sua pagina, `error`,
  `input`, `note`; alla prova non ne è uscita nessuna) non è un video: resta fuori, con il suo
  motivo, e un elenco che ha solo voci così non copre la finestra. Limite noto: una corsa riuscita
  con solo voci di errore è un elenco letto e incompleto, con l'avviso di ogni corsa, non una corsa
  fallita, quindi non conta nei cinque di fila e ne azzera la serie. Uno Short dentro la finestra
  si tiene, come ogni video della finestra (CONTRATTI, sezione 7 A, «Raccolta»; la domanda è nella
  sezione 9).
- T-A2-16 la richiesta che avvia la corsa dell'elenco porta il tempo massimo, il tetto dei video e
  il tetto della spesa, sopra una finestra piena al prezzo della prova (sezione 7); l'Actor è
  quello scelto alla prova (`LIST_ACTOR`) e il suo ingresso nomina il canale per id, senza un
  indirizzo di YouTube.

A3:
- T-A3-01 playlist con un IV per segmento; senza IV, il numero di sequenza (RFC 8216); la chiave
  una volta per registrazione e per indirizzo, mai riusata per un'altra registrazione.
- T-A3-02 decifratura AES-128-CBC andata e ritorno; un IV sbagliato guasta la testa del
  segmento: senza ID3 né sincronia ADTS in testa il segmento è un errore, non audio.
- T-A3-03 via il tag ID3 (dimensione syncsafe); un segmento senza ID3 resta com'è.
- T-A3-04 trame ADTS: sincronia, indice di frequenza 3 = 48 kHz, mono, lunghezze; una trama
  tronca in fondo si scarta e si conta.
- T-A3-05 struttura dell'M4A: `ftyp`, `moov` (con `esds`, `stts`, `stsz`, `stco`), `mdat`;
  durata = trame × 1024 / 48.000; un pezzo resta sotto 25 MB.
- T-A3-06 pezzi da 6 segmenti con tempi 0, 60, 120…; l'ultimo corto; un segmento fallito ferma
  il pezzo senza buchi silenziosi.
- T-A3-07 JSON del parlato e WebVTT nella stessa forma con i tempi; `transcript_source` giusto.
- T-A3-08 sottotitoli di YouTube, l'ultima riserva di DEC-037, punto 3, nella stessa forma;
  `youtube_asr`.
- T-A3-09 confine: apertura, sospensione, ripresa e chiusura a minuti inventati; resta solo la
  seduta aperta; del resto esistenza, minuto e durata.
- T-A3-10 ripresa non dichiarata: dal primo atto formale, con atto, minuto e motivo scritti;
  «sospesa» come argomento non sospende; «fuori verbale» non sospende.
- T-A3-11 seduta divisa: la seconda parte di una seduta legata comincia aperta se la prima finisce
  aperta; una registrazione non legata comincia fuori seduta fino al primo atto formale; con la
  prima parte `scartata` o in `errore` la seconda non aspetta e si fa a sé, con il registro.
- T-A3-12 confine non fissabile: niente testo, `temporanei/` vuota con la cancellazione
  definitiva, `scartata`.
- T-A3-13 file di costo: uno per quantità con il suo prezzo e la sua `unita`, i token di
  `gpt-4o-mini-transcribe` e i secondi di `whisper-1`, in dollari (`usd` e `prezzo_usd`), il
  nome `costo_openai_<id>.json` e i campi della riga «Costi»; le due quantità del modello del
  confine a ogni sua chiamata; lo stesso id non conta due volte; una ripresa non ripete la spesa
  di un tratto fatto.
- T-A3-14 budget di tempo: la corsa si ferma pulita e la successiva riparte dal segmento giusto.
- T-A3-15 nessun testo nei registri e nelle spese: una parola marcatrice della fixture non
  compare.
- T-A3-16 esportazione di `staging_A_testo` (`tests/test_workflow_exports.js`): ogni nodo
  Google Drive che cancella ha `deletePermanently`; `executionTimeout` 300; i quattro
  `settings` dei dati della sezione 4; le chiamate a sé stesso e alla lettura senza attesa.
- T-A3-17 la ripresa del testo (sezione 4), con un Drive e un OpenAI finti: la corsa muore
  dopo il file di un pezzo, dopo le spese, prima della riga. La corsa dopo non chiama OpenAI per
  un pezzo che ha il suo file, scrive le spese mancanti con l'id della corsa morta, e una spesa
  già scritta non si conta due volte. Morta prima del file, il pezzo si rifà una volta sola.
- T-A3-18 la pulizia (sezione 4): una riga che va in `errore` o `scartata` lascia `temporanei/`
  senza i suoi file, dopo il controllo delle spese; la pulizia del giorno cancella i file di una
  riga in `errore`, `scartata` o senza riga, salta una riga con la presa viva e lascia quelli di
  `testo_in_corso` e `testo_completo`; la ripartenza a mano di una riga caduta durante il testo
  riparte dal primo segmento, quella di una riga caduta in lettura o negli elementi riparte da
  `confini_fissati` o da `letta`, senza chiedere audio né trascrizione.
- T-A3-19 il modello e la fonte dei pezzi (sezione 4, «La ripresa del testo»): con pezzi di
  `gpt-4o-mini-transcribe` in `temporanei/` e il modello in uso cambiato, la corsa scrive le
  spese mancanti, cancella quei pezzi e riparte dal primo; un testo finito ha i pezzi di un
  modello solo e un solo `transcript_source`; con lo stesso modello, la ripresa di T-A3-17. Con
  la trascrizione della piattaforma comparsa in `testo_in_corso`, la corsa scrive le spese
  mancanti, cancella i pezzi e usa quella, senza chiamare OpenAI, con il `transcript_source`
  della piattaforma. Un testo già in `testo_completo` o oltre non si tocca.
- T-A3-20 il passaggio alla lettura (sezione 4, tabella dei flussi): la corsa di testo muore dopo
  aver messo una riga in `confini_fissati` e prima di chiamare la lettura; la corsa di testo
  dopo chiama la lettura, che prende quella riga; una riga presa da una lettura viva non si
  prende due volte.
- T-A3-21 la ripresa del confine (sezione 4), con un Drive e un OpenAI finti: la corsa muore
  dopo il file di una chiamata del modello del confine; la corsa dopo non rifà quella chiamata
  e ne scrive la spesa una volta, con l'id della corsa morta. La corsa muore dopo il testo della
  seduta aperta in `originali/` e prima della riga, con i pezzi cancellati tutti, in parte o per
  niente; la corsa dopo non chiede audio, non chiama OpenAI, fa il controllo delle spese,
  cancella i file rimasti e mette la riga in `confini_fissati`.
- T-A3-22 l'audio di YouTube (DEC-037, punti 2 e 3), con un Apify finto: l'Actor principale
  riuscito dà il testo con `asr:<modello>`; fallito il principale, la riserva (fallita vuol
  dire almeno: una corsa che non finisce riuscita, e un audio più corto del video; CONTRATTI,
  sezione 7 A, «Raccolta»); falliti tutti e due, i sottotitoli automatici, con `youtube_asr`;
  se non arriva niente il video resta `nuova`, senza passare a `errore`, con l'avviso, e si
  riprova nelle corse dopo, con la cadenza e il conto fra i 5 video che fissa A3; uscito
  dalla finestra senza testo, il testo lo mette in `scartata`, con
  il motivo. Un 401, 403 o 429 dell'API di Apify ferma Apify e non conta come corsa fallita.
  Il ritmo e il tetto sono quelli di T-A2-12. Lo storage della corsa su Apify resta finché
  la riga è in `testo_in_corso`, con il suo id nella riga: una corsa di testo morta a metà
  riprende dal pezzo seguente, senza un'altra corsa dell'Actor e senza una seconda spesa. Si
  cancella quando il testo è completo e dopo un fallimento dell'Actor; quello di una riga
  finita in `errore` o `scartata`, o rimasto senza riga, lo cancella la pulizia del giorno.
  Nessun Actor di YouTube parte finché `fonte:youtube_elenco` ha un `apify_run_id` (sezione 4).
  Ogni corsa di Apify, anche fallita, ha il suo file di costo (CONTRATTI, sezione 7 A,
  «Costi»), e nessuna richiesta porta cookie o un login.

**Prove in staging** su n8n, con fonti vere e tutto privato: niente di queste prove entra nel
repository. Totale atteso circa 1,2 € più la corsa dell'elenco di YouTube, tetto 2 €, dentro
la delega di DEC-036, punto 6. La prova degli Actor del 20 novembre è costata 0,0955 $ in cinque
corse (righe qui sotto; i file in `costi/`).

| Prova | Che cosa dimostra | Costo atteso |
|---|---|---|
| Un Consiglio del V con la trascrizione della piattaforma | JSON del parlato, confine su parole con i tempi | 0 € |
| Una commissione del X | la strada dell'audio intera, pezzi, spesa | 0,07 € (30 minuti) |
| Una commissione capitolina | catalogo capitolino, nessun Municipio dal titolo | 0,10 € (45 minuti) |
| Una parte dell'Assemblea di 3 ore o più | memoria per esecuzione e tempo, ripresa su più corse | 0,50 € (3,5 ore) |
| L'elenco del canale del Municipio I con un Actor di Apify, dal 20 novembre, con la spesa prevista dichiarata prima (DEC-037, punto 6) | che l'elenco copra la finestra di 100 giorni; quali ore dà per un video; tempo e costo vero della corsa. **Fatta il 20 novembre** (corsa `yZRVmUUAhfftEY7QU`, avviata dal collegamento ad Apify della sessione, sullo stesso conto di n8n): `grow_media/youtube-channel-video-scraper` con l'ingresso di `youtube-list.js`, 80 video chiesti, 13 secondi. I video vengono dal più recente; 55 stanno nella finestra di quel giorno (19 giorni, dal 1° novembre) e 25 sono di prima: la copre; la finestra di 100 giorni è una stima (sezione 4). L'ora è la pubblicazione, in UTC al secondo (`date`); l'Actor non dà un inizio di diretta (nessun campo), e nessun video era in diretta o programmato alla corsa (`liveBroadcastContent` `none`). La durata è in secondi (`durationSeconds`). Fra i video lunghi l'Actor dà anche due Short su 80 (sezione 9), e non tiene il tetto `maxItems` (T-A2-16). Lo storage della corsa si è cancellato dopo la lettura | 0,01605 $: 80 voci a 0,0002 $ e l'avvio |
| Uno o due video del Municipio I con i due Actor di Apify, dal 20 novembre, con la spesa prevista dichiarata prima (DEC-037, punto 6) | qualità dell'audio (traccia e bitrate), durata intera, tempo e costo vero della corsa; quale Actor è il principale e quale la riserva. **Fatta il 20 novembre su due video** (49 e 20 minuti), una corsa alla volta, fra le 00:08 e le 00:19 UTC, avviate dal collegamento ad Apify della sessione come l'elenco, sullo stesso conto: la prova era stata preparata così mentre la chiave di n8n non valeva ancora (sezione 3); n8n ne ha letto le corse e cancellato gli storage. YouTube ha bloccato tutte e quattro le corse. `datapipe/youtube-video-downloader` ha avuto il controllo anti-bot («Sign in to confirm you're not a bot») sul primo video e un 403 sui dati del secondo; `lurkapi/youtube-to-mp3-audio-downloader` ha avuto «YouTube is still blocking this video» sul primo (39 secondi) e «temporarily blocked the audio transfer» sul secondo, dopo 8 minuti di tentativi. Le corse finiscono `SUCCEEDED` anche senza audio: il fallimento si legge nella voce del dataset (per T-A3-22). Si pagano anche fallite, perché tutti e due gli Actor fanno pagare l'uso della piattaforma oltre agli eventi; se il tetto della spesa conti anche l'uso non si è visto: nessuna corsa l'ha raggiunto. Nessun audio è stato salvato; gli storage delle cinque corse della prova sono cancellati e verificati (sonda `staging_A_prova_apify_pulizia`). Qualità, durata, principale e riserva restano da misurare (sezione 9) | 0,0794 $ in quattro corse senza audio, contro i 0,5 € previsti |
| La stessa registrazione rifatta | nessun file doppio, nessuna spesa doppia | 0 € |
| Un errore forzato | `staging_A_avviso` scrive l'avviso in `letture/`, anche con i dati degli errori non salvati | 0 € |
| Un nodo Drive con la credenziale, creato con POST e cambiato con PUT, che scrive in `letture/` (fatta il 15 novembre, con il confronto dei modelli) | la credenziale Drive regge sui flussi fatti dall'API (sezione 8, punto 3) | 0 € |
| `staging_A_sonda_catena` (A2) | i 300 secondi non passano a una corsa chiamata senza attesa; se le corse chiamate contano nel piano (sezione 4) | 0 € |
| Elenco (A2) e chiave (A3) senza `Origin` e `Referer`, una volta | se servono (sezione 4, la strada dell'audio, passo 3) | 0 € |
| Chiusura | `temporanei/` vuota e nessun suo file nel cestino (`trashed = true`); nessuna esecuzione con dati di audio o testo su n8n; nessuno storage di corsa rimasto su Apify | 0 € |

**Il confronto dei modelli,** prima di A4, sugli intervalli della seduta aperta già fissati di
tre registrazioni delle prove: `whisper-1` (`verbose_json`) e `gpt-transcribe` contro il testo
di `gpt-4o-mini-transcribe` in `originali/`, tetto 1 € in tutto (con `whisper-1` 2 ore sono
circa 0,7 €; il prezzo di `gpt-transcribe` si legge prima di provarlo, e se non ci sta si
riducono le ore). Date di spegnimento lette dall'API di OpenAI (`/v1/models`) il 14 novembre,
sonda 918: `gpt-4o-mini-transcribe` e `whisper-1` il 26 febbraio 2027, a circa tre mesi e mezzo
dall'inizio; `gpt-4.1-mini` il 14 gennaio 2027; `gpt-5-mini` l'11 dicembre 2026; nessuna data
per `gpt-transcribe`, `gpt-live-transcribe` e `gpt-realtime-whisper`. DEC-037, punto 4,
allarga il confronto. Entrano i servizi più economici basati su Whisper (per esempio
`whisper-large-v3-turbo` di Groq: il prezzo si legge prima, e serve una chiave dall'owner).
Ogni modello si prova con e senza una guida dei nomi, corta, fatta con l'ordine del giorno
della seduta (atti del canale D) e con i luoghi principali del Municipio nel gazetteer. Si
giudica prima sulla correttezza dei nomi di luogo (vie, piazze, luoghi del Municipio), poi sul
resto, poi sul costo. Il tetto resta 1 € (le eccezioni dell'owner sono in DEC-044): se le prove in
più non ci stanno, si riducono le ore.
A4 fissa un modello che non si spenga a pilota in corso, scelto in quell'ordine. Si misurano
parole, quota di testo ripetuto (a giugno 57 registrazioni su 318
oltre il 10 %), grana dei tempi, nomi del gazetteer riconosciuti, tempo e spesa. In `letture/`
vanno solo i numeri. I testi degli altri modelli sono testo della seduta aperta e vanno in
`originali/`, accanto all'altro, con il modello nel nome; per quelle tre registrazioni la
lettura usa il testo del modello fissato. Il modello fissato vale per i testi che cominciano
dopo, e per quelli in corso (sezione 4, «La ripresa del testo»). Un testo già finito, cioè in
`testo_completo` o oltre, resta com'è e si legge con il suo testo: il suo `transcript_source`
dice il modello, e la lettura lo accetta. Ritrascrivere i testi finiti con il modello nuovo è una
scelta di spesa: sotto i 5 € la fa il builder e la registra, da 5 € in su decide l'owner (DEC-036,
punto 6).

## 7. Costi previsti per mese

Stime in euro per confrontarle con la quota, al cambio di 0,92 € per dollaro di
`docs/sources/TRIAL_LEDGER.md`. Il registro delle spese resta in dollari, e il coordinatore
converte il totale del mese con il tasso della BCE (CONTRATTI, sezione 5; DEC-035).

| Voce | Base | € al mese |
|---|---|---|
| Trascrizione nostra | 165,4 ore, con le 42,1 del Municipio I (DEC-037), a 0,157 $ l'ora (misura di giugno: 318 registrazioni, 227,7 ore, 35,76 $) | circa 24 |
| Apify, per l'audio di YouTube | 77 video e 42,1 ore a giugno, ai prezzi di listino letti il 15 novembre e riletti uguali il 19: 0,006 $ a video (`datapipe/youtube-video-downloader`) o 0,002 $ al minuto (`lurkapi/youtube-to-mp3-audio-downloader`), più 0,00005 $ per GB di memoria all'avvio. Alla prova (sezione 6) tutti e due hanno fatto pagare anche l'uso della piattaforma: una corsa senza audio è costata da 0,004 a 0,055 $, e quanto aggiunge l'uso a una corsa riuscita non è misurato | da 0,4 a 4,6, più l'uso |
| Lettura e confine | circa 178 ore di testo (nostro e della piattaforma; di YouTube solo in ultima riserva) con un modello di fascia media, al prezzo di `gpt-4.1-mini`, che si spegne il 14 gennaio 2027 (sezione 6): il prezzo si rilegge con il modello che sceglie A4 | 2–3 |
| Apify, per l'elenco di YouTube | `grow_media/youtube-channel-video-scraper`, scelto alla prova (sezione 6): 0,0002 $ a video, più 0,00005 $ per GB di memoria all'avvio, senza l'uso della piattaforma (prova: 0,01605 $ per 80 video). Una corsa al giorno, una seconda se la prima non riesce, con al più 300 video (A2; CONTRATTI, sezione 7 A, «Raccolta»): a finestra piena circa 9.000 video al mese, circa 1,8 $, sotto la soglia di 0,60 $ ogni 1.000 video (DEC-036, punto 6) | circa 1,7 |
| Imprevisti | 20 % | da 6 a 7 |
| Totale | | da circa 34 a circa 40, sopra la quota di A di 33 € (CONTRATTI, sezione 5) |

Fuori dalla stima restano voci note, tutte verso l'alto:
- i Consigli del V e del X che l'elenco vede senza la trascrizione della piattaforma passano
  alla nostra (CONTRATTI, sezione 7 A, «Testo»; T-A2-05), come il Consiglio del X di fine
  ottobre: fino a 12,8 ore, circa 1,9 €;
- le commissioni capitoline di novembre vanno più forte di giugno: 9,3 ore in 3 giorni
  lavorativi, circa 65 al mese contro 51,6, circa 1,9 € in più;
- gli imprevisti al 40 % invece del 20, per le trascrizioni da rifare (a giugno 57
  registrazioni su 318 con più del 10 % di testo ripetuto, sezione 6): da 6 a 7 € in più;
- la scrittura e la seconda verifica di A5: si fissano con A5, su quanto resta della quota;
- l'uso della piattaforma che gli Actor dell'audio fanno pagare, e le loro corse fallite
  (tabella).

Con le prime tre la stima arriva a circa 43–50 €, sopra la quota. Lo dicono le spese vere del primo mese, nei file di `costi/`: il coordinatore avvisa
l'owner quando la quota di A o il totale del pilota passano il 50 % e l'80 % (DEC-037,
punto 6), e quando la quota di 33 € è superata, anche se il totale del pilota resta sotto i
50 € (regola di questo brief, più stretta di CONTRATTI, sezione 5, che applica DEC-031,
punto 6, al totale). Nessuna di queste soglie ferma un flusso.
I testi della piattaforma non costano; i sottotitoli di ultima riserva costano la sola corsa
di Apify. `whisper-1` per tutto (0,006 $ al
minuto) farebbe circa 55 €, più del doppio: fuori quota. Una
tantum, questo mese: le prove in staging (tetto 2 €) e il confronto (tetto 1 €, con le eccezioni
di DEC-044). La spesa è una
stima dall'uso che OpenAI restituisce (CONTRATTI, sezione 7 A, «Costi»); la somma del mese la fa
il coordinatore.

**A regime** (stima del builder, DEC-037, Contesto): con i 15 Municipi, le commissioni
capitoline e l'Assemblea, a giugno le ore da trascrivere noi sarebbero circa 410 al mese
(RomaTV circa 330, YouTube circa 80; altre 77 ore di Consigli le trascrive già la
piattaforma), circa 80 € al mese per il canale A al modello di oggi e con il prezzo di Apify
a video (circa 90 con quello al minuto), prima della scrittura e senza l'uso della piattaforma
che gli Actor dell'audio fanno pagare; l'elenco di YouTube aggiunge circa 1,7 € al mese per
canale letto. Il grosso è la trascrizione, non Apify.

## 8. Come si lavora su n8n da una sessione

1. **Accesso.** API pubblica `https://quartierinews.app.n8n.cloud/api/v1` dal sandbox, con
   l'header `X-N8N-API-KEY: dummy`: la chiave vera la mette il proxy. Si scrivono solo flussi
   `staging_`; i flussi di produzione e quelli «Roma Pipeline» si leggono e basta.
2. **Creare.** `POST /workflows` con nodi, collegamenti e `settings`. Le credenziali per id,
   come nelle esportazioni: «OpenAI account» e «Google Drive account», con gli id del passaggio
   `PASSAGGIO_2026-11-14_canale-A.md`. `settings` ammessi: `executionOrder`, `saveManualExecutions`,
   `saveDataSuccessExecution`, `saveDataErrorExecution`, `saveExecutionProgress`,
   `callerPolicy`, `callerIds`, `timezone` (`Europe/Rome`), `errorWorkflow` (l'id di
   `staging_A_avviso`), `executionTimeout`.
3. **Cambiare.** `PUT /workflows/{id}`. Dal 14 novembre POST e PUT funzionano sui nodi
   `openAiApi` con credenziale, perché le credenziali sono condivise col progetto (918, 921);
   le sessioni precedenti avevano visto che la query di un nodo Drive con credenziale cambia solo
   ricreando il flusso con POST, con un id nuovo (`PASSAGGIO_2026-11-12.md`, sezione 5). Il 15
   novembre un nodo Drive con la credenziale «Google Drive account», creato con POST e cambiato
   con PUT in un flusso `staging_A`, ha scritto in `letture/` (`staging_A_confronto`, passaggio
   `PASSAGGIO_2026-11-15_confronto-trascrittori.md`): regge. Prima del PUT, nessuna esecuzione in
   corso (`GET /executions?status=running`); dopo, un flusso attivo si spegne e si riaccende.
4. **Accendere e spegnere.** `POST /workflows/{id}/activate` e `/deactivate`. `staging_A_avviso`
   resta sempre acceso: n8n non chiama un flusso d'errore spento.
5. **Provare.** L'API non ha un comando per far partire un flusso. Si mette un trigger a orario
   `* * * * *` e nel nodo «Inizio» una scadenza scritta nel codice, pochi minuti avanti: dopo, la
   corsa esce senza fare niente. Si accende, si spegne appena parte la prima esecuzione.
6. **Osservare.** `GET /executions?workflowId=…`, e `GET /executions/{id}?includeData=true`
   solo tramite un aiutante (`CLAUDE.md`, «Consumption»): salva i dati grezzi nello scratchpad e
   risponde con i numeri. Il testo di una seduta non entra mai nella chat.
7. **Cancellare.** Con i `settings` della sezione 4 un'esecuzione con audio o testo non si
   salva. Se una ne resta, come 919, 921 e 922, fatte prima di queste regole, si cancella con
   `DELETE /executions/{id}` appena vista, senza scaricarne i dati (DEC-036, punto 5).
8. **Data table e cartelle.** La Data table si crea una volta, dall'API se l'endpoint lo
   permette, se no la crea l'owner nell'editor. Le sottocartelle ci sono già (sezione 3); i loro
   id vanno nell'«Inizio». I file grandi li muove solo n8n (CONTRATTI, sezione 3).
9. **Esportare.** `GET /workflows/{id}` e `workflows/<nome>.json` con la ricetta di
   `PASSAGGIO_2026-11-12.md` su Drive, appendice B: i campi del Download dell'editor, senza
   `staticData`, salvo `active`, `versionId` e le chiavi dei nodi, che si prendono come le dà n8n
   (`workflows/README.md`, T-WF-attivo). I nodi Code identici byte per byte ai file di `code-nodes/`
   (`tests/test_workflow_exports.js`); `workflow_version` dell'«Inizio» cambia a ogni modifica.
10. **Chiudere.** Flussi di prova spenti, nessuna esecuzione con audio o testo su n8n,
    `temporanei/` vuota e senza file nel cestino (`trashed = true`), nessuno storage di corsa
    rimasto su Apify; il passaggio
    `PASSAGGIO_<data>.md` nella cartella di passaggio (`CLAUDE.md`, «Consumption»).

## 9. Punti aperti

| Punto | Chi decide | Quando |
|---|---|---|
| Deciso il 18 novembre 2026: DEC-014…021 sono nel registro così come decise a settembre, con i chiarimenti dell'owner (PR #67), e la seconda verifica di DEC-015 vale nel pilota (DEC-042) | owner | fatto |
| I valori di `editorial_class` per `institutional`: si aggiungono con il build del gazetteer (CONTRATTI, sezione 2) | il builder propone, l'owner decide | A5 |
| Come una pagina pilota mostra i fatti di livello città e di livello Municipio (DEC-106, DEC-006); come un elemento porta più pagine e la portata | owner | A5 |
| Immagini degli elementi: nessuna regola decisa per questo blocco (DEC-101 è per gli eventi) | owner | A5 |
| Citazioni testuali del parlato | owner | A4 |
| Atti capitolini (ordini del giorno, convocazioni) per verificare i fatti: fuori da DEC-033, che copre gli atti dei Municipi I, V e X | owner | A4 |
| Prati: deciso con DEC-037 (15 novembre). Il testo viene dall'audio; l'elenco e l'audio da Apify. L'elenco è provato (20 novembre, sezione 6); l'audio no: YouTube ha bloccato tutti e due gli Actor, su due video. Un'altra prova di giorno, una corsa per Actor, avviata da n8n come vuole DEC-037, punto 2, con la spesa dichiarata prima | builder | dal 20 novembre |
| Gli Actor di Apify per YouTube: quello dell'elenco è scelto (`grow_media/youtube-channel-video-scraper`, `LIST_ACTOR` di `youtube-list.js`, con i suoi campi in `ACTOR_FIELDS` e `actorInput`; 20 novembre, sezione 6), e la credenziale Apify è usabile da una corsa di un flusso `staging_A` (sezione 3). Restano, per l'audio, principale e riserva, dopo una prova che riesca; come arrivano i sottotitoli di ultima riserva; per A3, che una corsa dell'audio riuscita senza audio è una corsa fallita (sezione 6) e che anche quella si paga. La cadenza dell'elenco l'ha fissata A2 (CONTRATTI, sezione 7 A, «Raccolta») | builder | prima di A3 |
| La riserva fuori da Apify (un programma su un computer con connessione di casa, o un servizio di un'altra azienda): il builder porta le opzioni, con costi e manutenzione (DEC-037, punto 3). Il 20 novembre YouTube ha bloccato tutti e due gli Actor dell'audio (sezione 6): se una prova di giorno non riesce, resta la riserva fuori da Apify, o un altro Actor da provare | owner | prima che A3 vada a regime |
| L'audio di un video intero di YouTube su n8n: memoria per esecuzione, formato e divisione in pezzi; come si trova lo storage di una corsa di Apify rimasto senza riga | builder | A3 |
| Che cosa il servizio di trascrizione conserva dell'audio che riceve, di RomaTV e di YouTube: le sue condizioni si leggono prima di fissare il modello (DEC-037, punto 2) | il builder legge; l'owner se serve una scelta | A4 |
| Come si riconosce che due registrazioni di piattaforme diverse sono la stessa seduta. Quale apre il fatto lo dice già CONTRATTI, sezione 7 A, righe «Elemento» e «Identità»: la prima in cui il fatto è letto; le altre sono provenienza | builder | A5 |
| L'ora di riferimento di un video di YouTube: fissata da A2, l'inizio della diretta quando l'Actor lo dà, se no la pubblicazione (CONTRATTI, sezione 7 A, «Raccolta»). L'Actor scelto non la dà: vale la pubblicazione (`youtube-list.js`, `ACTOR_FIELDS`). Con `videoType` `long` non si sa se l'Actor elenchi anche la scheda delle dirette del canale; a giugno lì non c'era nessun video (CSV A4) | builder | fatto il 20 novembre |
| Gli Short del canale: CONTRATTI, sezione 7 A, «Raccolta», tiene ogni video della finestra, e `youtube-list.js` li tiene. Ma il perimetro sono le sedute (DEC-036, punto 4), e uno Short non lo è: nell'elenco del 20 novembre 2 voci su 80 (49 e 9 secondi, `type` `short`), date dall'Actor anche chiedendo i video lunghi. Lettura del builder da scrivere in «Raccolta» con una PR di CONTRATTI: uno Short non è una seduta, non entra e non copre la finestra; poi il codice (T-A2-15) | builder; l'owner con il merge | con la prossima PR di CONTRATTI |
| Il modello di trascrizione e quello della lettura: `gpt-4o-mini-transcribe` e `whisper-1` si spengono il 26 febbraio 2027, `gpt-4.1-mini` il 14 gennaio 2027 (API di OpenAI, sonda 918; sezione 6). A4 sceglie un modello che non si spenga a pilota in corso | builder; l'owner se il cambio costa 5 € o più | A4 |
| Il piano a regime, con tutti i Municipi: a giugno circa 340–350 ore da trascrivere, 800–1.050 corse di testo a 20–25 minuti per corsa, circa 1.800–2.150 con l'elenco, B e D, prima di C (`docs/sources/FATTIBILITA_RICOSTRUZIONE_2026-06.md`); le leve sono corse di testo più lunghe, il testo fuori da n8n, un piano superiore. A3 misura quante corse costa una seduta | il builder misura, l'owner decide | prima di allargare oltre i Municipi del pilota |
| `Origin` e `Referer` del portale nelle richieste all'elenco e alla chiave: se servono, la PR che lo misura lo scrive in CONTRATTI, sezione 7 A | builder | A2 (elenco), A3 (chiave) |
| La stima di spesa con le voci che ne restano fuori arriva a circa 43–50 €, con l'elenco di YouTube, sopra la quota di 33 € (sezione 7) | il coordinatore, sulle spese del primo mese; l'owner se si va oltre | fine del primo mese |
| File del repository che hanno già testo di notizie preso dalle fonti: `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md`, sezione 6 («Possibili notizie»), e `docs/wiki/`. Segnalati, non toccati qui | owner | ora |

# Workstream A · Amministrazione: il brief

Stato: apertura del canale, PR A1 (14 novembre 2026). Le regole del canale stanno in
`docs/pilota/CONTRATTI.md`, sezione 7, «A · Amministrazione», e le scelte dell'owner in
DEC-036: qui non si ripetono, si rimanda. Questo documento dice che cosa si costruisce, con
quali mezzi e come si prova; la sessione che costruisce i flussi parte da qui. Se una regola
cambia, cambia là, e qui si corregge solo il rimando.

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
| Prati (I) | Consiglio e commissioni del Municipio I | YouTube, canale `UCEZtd0d0UV5e8ZCWkNOiNjw` | sottotitoli automatici di YouTube: oggi non ottenibili (pagina di consenso, sotto) | 42,1 (3,5 + 38,6) |
| tutte e tre | commissioni capitoline | RomaTV, `Commissioni Capitoline` | nostra | 51,6 |
| tutte e tre | Assemblea capitolina | RomaTV, `Assemblee Capitoline` | nostra | 41,3 |

Da trascrivere noi: 30,4 ore municipali, 51,6 capitoline e 41,3 dell'Assemblea, 123,3 ore al
mese (sezione 7). Quali fatti capitolini si tengono lo dice DEC-036, punto 4.

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
  lo sguardo indietro di 40 giorni dell'elenco (CONTRATTI, sezione 7 A, «Raccolta»).
- **Prati al 14 novembre:** da n8n il feed risponde; la pagina del video dà la pagina di
  consenso UE, senza tracce dei sottotitoli. Per DEC-036, punto 3, e per la riga «Raccolta» è
  il primo segnale di blocco: `www.youtube.com` è fermo da allora, e l'owner lo sa con A1 (corpo
  della PR e rapporto). Non si prova un'altra strada, né in A3 né dopo: A2 costruisce e prova
  con fixture la lettura del feed, ma nessun flusso chiede niente a YouTube finché l'owner non
  fa ripartire l'host a mano, e Prati resta senza testo finché l'owner non decide (sezione 9).

## 3. I mezzi

Stato al 14 novembre 2026. Gli id delle esecuzioni sono quelli delle sonde (`staging_A_sonda_*`,
spente dopo le corse di prova).

| Mezzo | Stato | Note |
|---|---|---|
| n8n Cloud, piano Starter (`quartierinews.app.n8n.cloud`) | PRESENTE | nodo Code con `require('crypto')` (AES-128-CBC), `Buffer`, `setTimeout`, `this.helpers.httpRequest` (testo o `arraybuffer`, risposta intera, errori HTTP senza eccezione); niente `process` (916); niente `URL` né il modulo `url` (non dalle sonde: commit 2e6a288, `code-nodes/news-collect.js`); altri moduli non provati, non si usano |
| RomaTV raggiunto da n8n | PRESENTE | elenco (`search_frontend`), WebVTT, JSON del parlato, playlist, chiave e segmenti rispondono 200 (918, 921); l'elenco e la chiave sono stati chiesti sempre con `Origin` e `Referer` del portale, e se servono non è provato; WebVTT, JSON del parlato, playlist e segmenti hanno risposto senza (sezione 4, la strada dell'audio, passo 3) |
| YouTube raggiunto da n8n | FERMO dal 14/11 | feed 200; pagina del video = pagina di consenso UE (918): primo segnale di blocco (sezione 2); riparte solo quando l'owner lo dice (CONTRATTI, sezione 7 A, «Raccolta») |
| Credenziale «OpenAI account» (`openAiApi`) | PRESENTE | condivisa dall'owner il 14/11 col progetto dei flussi `staging_`; `gpt-4o-mini-transcribe` e `whisper-1` rispondono 200 su un M4A di 10 minuti (921) |
| Credenziale «Google Drive account» (`googleDriveOAuth2Api`) | PRESENTE; via API DA PROVARE (A2) | condivisa il 14/11; c'è una quota di richieste al minuto (D si è fermato il 13/11). POST e PUT con la credenziale sono provati solo su nodi `openAiApi` (918, 921); per un nodo Drive le sessioni precedenti hanno visto il contrario (`PASSAGGIO_2026-11-12.md`, sezione 5): sezione 8, punto 3 |
| Cartella Drive `A Amministrazione/` | PRESENTE | sotto `30 Staging pilota 2026-11`; gli id di questa cartella e delle sottocartelle sono nel passaggio `PASSAGGIO_2026-11-14_canale-A.md`, nella cartella di passaggio, non nel repository |
| Sottocartelle di CONTRATTI, sezione 7 A | PRESENTI, vuote (create il 14/11) | `registrazioni/`, `temporanei/`, `originali/`, `letture/`, `costi/`; i loro id vanno nel nodo «Inizio» dei flussi |
| Data table di n8n | PRESENTE | la licenza le ha (`GET /data-tables` 200), nessuna creata; le Variables no (403); i dati statici si salvano solo a fine corsa di produzione |
| API pubblica di n8n dal sandbox | PRESENTE | la chiave la mette il proxy (sezione 8) |
| GitHub | PRESENTE | solo come `QN-Builder` e solo per il coordinatore (DEC-029; CONTRATTI, sezione 4) |
| Gazetteer | PRESENTE | `raw.githubusercontent.com/QuartieriNews/QN/<commit>/gazetteer/gazetteer.json` risponde 200 dal sandbox; da n8n si prova in A5 |
| Prototipo dell'audio, `hls-audio.js` | PRESENTE, fuori dal repository | provato in locale con ffprobe e su n8n (921); sta nella cartella di passaggio (`30 Staging pilota 2026-11/`), con la sua prova locale, il codice della sonda e le note delle sonde, nessun testo delle fonti; entra in A3 con i test |
| Modello del flusso d'errore | PRESENTE | `staging_D_avviso`, che scrive solo nella cartella di D |
| Data table `staging_A_registrazioni` | DA COSTRUIRE | A2 (sezione 4) |
| Nodi Code della sezione 5, con i test | DA COSTRUIRE | A2–A5 |
| `staging_A_elenco`, `staging_A_testo`, poi `staging_A_lettura` e `staging_A_elementi` | DA COSTRUIRE | A2–A5 |
| `staging_A_avviso` | DA COSTRUIRE | A2; sempre attivo |
| Fixture dei test | DA COSTRUIRE | byte e testi inventati (DEC-109), mai presi da una fonte |
| Credenziali condivise e DEC-036 | DALL'OWNER, fatto il 14/11 | |
| Chiave di un modello di un'altra famiglia, per la seconda verifica di DEC-015 | DALL'OWNER, con A5 | solo se l'owner dice che DEC-015 vale per il pilota (sezione 9); su n8n oggi c'è solo OpenAI |
| Foglio della coda di revisione | DALL'OWNER, con A5 | non esiste su Drive |
| Piano n8n superiore | DALL'OWNER, solo se serve | se le corse chiamate da un altro flusso contano, A non sta nel piano già con A2 e A3: la domanda arriva con la misura di A2 (sezione 4) |

## 4. Architettura su n8n

| Flusso | Trigger | Ingresso | Uscita | Cartella |
|---|---|---|---|---|
| `staging_A_elenco` | orario, quello di CONTRATTI, sezione 7 A, «Raccolta» | i quattro cataloghi RomaTV; il feed del canale del I solo quando l'owner fa ripartire YouTube (sezione 2) | righe `nuova` nella Data table, schede delle registrazioni, risposte come arrivano, registro della corsa | `registrazioni/`, `originali/`, `letture/` |
| `staging_A_testo` | chiamato dall'elenco a fine corsa, e da sé stesso finché c'è lavoro, senza aspettare la fine; al massimo 8 corse al giorno (sotto, «Esecuzioni») | le registrazioni prese dalla Data table, una dopo l'altra, finché il budget di tempo non è finito | testo intero a pezzi, confini, testo della seduta aperta, le spese di ogni registrazione in ogni corsa | `temporanei/`, `originali/`, `costi/`, `letture/` |
| `staging_A_lettura` (A4) | chiamato dal testo, senza aspettare la fine, quando una registrazione arriva a `confini_fissati` | il testo della seduta aperta | i fatti candidati | `letture/` |
| `staging_A_elementi` (A5) | da fissare in A5 | le letture | gli elementi | `A Amministrazione/` |
| `staging_A_avviso` | `errorWorkflow` di ogni `staging_A_*` | l'errore | `AVVISO_A_<ora UTC>.json`, senza testo | `letture/` |

**Lo stato** sta in una Data table, `staging_A_registrazioni`, una riga per registrazione: il
`recording_ref`, lo stato, il motivo di uno scarto, catalogo o canale, `municipality_code`, ora
di riferimento, durata, se c'è la trascrizione della piattaforma, la prima parte della seduta
quando è divisa, il segmento da cui riprendere, i tentativi, la presa. Mai un testo. La
scheda in `registrazioni/` copia lo stato quando cambia (CONTRATTI, sezione 7 A).

| Stato | Lo mette | Vuol dire |
|---|---|---|
| `nuova` | elenco | vista e dentro il perimetro |
| `testo_in_corso` | testo | pezzi del testo intero in `temporanei/`; la riga dice da quale segmento riprendere |
| `testo_completo` | testo | testo intero in `temporanei/` |
| `confini_fissati` | testo | testo della seduta aperta in `originali/`; niente più in `temporanei/` |
| `letta` | lettura (A4) | fatti candidati in `letture/` |
| `scartata` | elenco o testo | fuori perimetro, confine non fissabile, testo di YouTube non ottenibile: il motivo è nella riga |
| `errore` | qualunque flusso | tre tentativi falliti; parte l'avviso; si riparte solo a mano |

**La presa.** Una corsa scrive nella riga il proprio id di esecuzione e una scadenza (ora più 5
minuti) solo se la riga è libera o la presa è scaduta, poi rilegge la riga e lavora solo se la
presa letta è la sua. Ogni passo rinnova la scadenza; a fine corsa la presa si lascia. Due corse
non lavorano sulla stessa registrazione, e una corsa morta libera la riga in 5 minuti. Lo stesso
meccanismo, su una riga per fonte (`lease:romatv`, `lease:youtube`), tiene una richiesta alla
volta per fonte anche fra flussi diversi (CONTRATTI, sezione 7 A, «Raccolta»). La sua grana è la
corsa, non la richiesta: un nodo Code non legge né scrive una Data table (nessuna sonda lo
prova), lo fa il nodo Data table, che prende la presa prima del giro sulla fonte, la rinnova a
ogni pezzo e la lascia alla fine; una corsa di testo la tiene quindi fino a 4 minuti. Chi la
trova presa: l'elenco aspetta, con un nodo Wait, al più fino alla scadenza della presa
(5 minuti), poi salta quella fonte in quella corsa e lo scrive nel registro (lo sguardo indietro
di 40 giorni recupera alla corsa dopo); il testo non comincia e finisce pulito, perché lo
richiama l'elenco a fine corsa. L'ordine di scrittura è: file su Drive, poi la riga; un file
già presente con lo stesso nome si sostituisce (specifica v2.5, fase 5.2), così una ripresa non
lascia doppioni.

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
  oltre i 300 secondi della prima.
- Esecuzioni: 2.500 al mese sul piano Starter, con B e D. Oggi B e D fanno 25–29 corse al
  giorno da trigger e circa 49 corse chiamate da un altro flusso (sotto-workflow): 750–870 al
  mese se le seconde non contano, 2.220–2.340 se contano. Obiettivo di A: al massimo 500 corse
  che contano. Conto di giugno: elenco 240 (8 corse al giorno, da trigger). Testo: una corsa
  prende più registrazioni in fila finché il budget non è finito, e 123,3 ore a 20–25 minuti
  per corsa fanno 300–370 corse; con una registrazione per corsa, la riserva se una corsa non
  riesce a prenderne più di una, 350–430 corse per 117 registrazioni (304 a 30 minuti per
  corsa, dal CSV A3). I testi senza audio (20 Consigli con la trascrizione della piattaforma; i
  77 video del I, se YouTube riparte) entrano nelle stesse corse. Il testo è chiamato
  dall'elenco e da sé stesso: è un sotto-workflow.
  - Se le corse chiamate non contano (insights: 143 di produzione contro 382 salvate, 245
    chiamate; non provato), di A conta solo l'elenco, 240, e con B e D si arriva a 990–1.110:
    il piano basta.
  - Se contano, B e D lasciano 160–280 corse: l'elenco da solo ne prende 240 e il testo non ci
    sta più. A non sta nel piano già con A2 e A3, non solo con A4 e A5. A2 lo misura per primo,
    con la sonda della catena (il contatore del piano prima e dopo un numero noto di corse,
    letto dall'owner nel pannello di n8n se l'API non lo dà), prima di accendere l'elenco a
    orario; se contano, la domanda sul piano va all'owner allora (sezione 9).
  - Il tetto del testo viene dall'obiettivo: 500 − 240 = 260 corse al mese, cioè 8 al giorno.
    Vale finché A2 non dimostra che le corse chiamate non contano; allora lo rifissa A3 sul
    tempo misurato. Con 8 corse da 20–25 minuti si trascrivono 80–100 ore al mese, meno delle
    123,3 di giugno: anche questo va nella domanda all'owner.
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
  `false` (DEC-036, punto 5; CONTRATTI, sezione 7 A, «Testo»: l'audio non si scrive mai). Un
  errore si legge dall'avviso di `staging_A_avviso`, con flusso, nodo, messaggio e ora; l'id
  dell'esecuzione può mancare, perché l'esecuzione non si salva. Nessun nodo di esito porta un
  campione di testo (la sonda 921 lo faceva; quell'esecuzione è cancellata).
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
7. Il testo dei pezzi della corsa va in un file di `temporanei/`; l'uso restituito da OpenAI
   diventa le spese della registrazione in quella corsa, in `costi/` (riga «Costi»); la riga avanza. L'audio
   non si scrive mai.
8. A testo completo, il confine (sezione 5, A3) taglia la seduta aperta, che va in `originali/`,
   e i file della registrazione in `temporanei/` si cancellano per sempre: il nodo Google Drive
   di n8n con la cancellazione definitiva (`deletePermanently`), mai il cestino, dove un file
   resta circa 30 giorni con le sue revisioni. Il connettore Drive delle sessioni sa solo
   spostare nel cestino: in `temporanei/` cancella solo n8n.

## 5. Ordine di costruzione

Una PR alla volta nel giro di revisione (protocollo, sezione 2). Ogni PR porta i suoi nodi Code
(una fonte, due contesti: `code-nodes/README.md`), i test con la riga in `package.json`, e
l'esportazione dei flussi in un commit separato. I nomi dei file nuovi sono proposte: li fissa
la PR che li porta.

| PR | Che cosa | Nodi Code e test | Su n8n e Drive |
|---|---|---|---|
| A1 apertura (questa), in due PR perché insieme passano le 1.000 righe (protocollo, sezione 2, punto 4) | A1a: CONTRATTI, sezioni 5, 6 e 7 A; DEC-036; questo brief. A1b: il nodo e i test | A1b: `institutional-identity.js`, `tests/test_institutional_identity.js` | niente |
| A2 raccolta | elenco dei cataloghi e del feed, schede, stato, presa, stop delle fonti, controllo di `robots.txt` | `romatv-list.js`, `youtube-list.js`, `recording-state.js` | Data table; `staging_A_elenco`; `staging_A_avviso`; le sonde della sezione 6 |
| A3 testo | la strada dell'audio; i pezzi da 60 secondi; i testi della piattaforma (JSON del parlato, WebVTT di riserva) e i sottotitoli di YouTube in una forma sola con i tempi; il confine della seduta; le spese | `hls-audio.js` (dal prototipo nella cartella di passaggio, sezione 3), `recording-text.js`, `session-boundary.js` | `staging_A_testo` |
| A4 lettura | i fatti candidati secondo `tools/sources-study/report2/SPECIFICA_VIDEO.md`, con l'evidenza `[mm:ss]`, in `letture/`; il modello di trascrizione si fissa qui, dopo il confronto (sezione 6) | il nodo della lettura | `staging_A_lettura` |
| A5 elementi | geografia con una porta JS della risoluzione del gazetteer sui luoghi estratti; classi editoriali di `institutional` dal build del gazetteer; seconda verifica di DEC-015; coda di revisione; proiezione per il prototipo | la porta del gazetteer, la scrittura dell'elemento | `staging_A_elementi`; gli elementi in `A Amministrazione/` |

**Il confine (A3).** `session-boundary.js` cerca nel testo con i tempi gli atti formali di
`SPECIFICA_NOMI_E_TERRITORIO.md`, sezione 2, e ne ricava gli intervalli della seduta aperta.
Dove le formule mancano o si contraddicono, un modello legge solo i tratti intorno ai candidati
(costo nella riga della lettura, sezione 7). Le parti di una seduta divisa si legano in ordine:
lo stato alla fine di una parte è lo stato all'inizio della successiva, e una parte aspetta la
precedente. Se il confine non si fissa: DEC-036, punto 5.

## 6. Prove

**Test unitari** (CI, `npm test`), con fixture inventate; un id per caso nel nome del test.

A1: T-A1-01…T-A1-19 in `tests/test_institutional_identity.js`: identità, nomi dei file,
colonne della coda, ora e durata, `source_hash`, l'adattatore di n8n.

A2:
- T-A2-01 una pagina di catalogo: guid in minuscolo, titolo come pubblicato, ora di riferimento
  con offset portata in UTC, durata `hh:mm:ss.fffffff` in secondi, trascrizione della
  piattaforma riconosciuta dalle tracce, SMIL solo audio.
- T-A2-02 `municipality_code` dal catalogo: una voce di `Municipio X` intitolata «Commissione IV …»
  ha X; i cataloghi capitolini non danno un Municipio.
- T-A2-03 l'inizio: una seduta alle 00:30 del 1° novembre di Roma entra, una del 31 ottobre no.
- T-A2-04 la finestra di 40 giorni: le pagine si fermano alla prima voce più vecchia; una
  pubblicazione tardiva entra; una voce già vista non dà una seconda riga.
- T-A2-05 la trascrizione della piattaforma aggiunta dopo: la scheda si aggiorna; se il nostro
  testo non è iniziato si usa quella, se è fatto resta il nostro, senza seconda spesa.
- T-A2-06 seduta divisa: le parti (stesso catalogo, organo e giorno di Roma) si legano, in ordine.
- T-A2-07 gli stop di RomaTV della riga «Raccolta», uno per caso: l'host si ferma, parte
  l'avviso, e riparte solo quando l'owner lo dice; un errore del server lascia la voce per la
  corsa dopo, cinque di fila fermano l'host fino al giorno dopo.
- T-A2-08 `robots.txt` cambiato rispetto al 14 novembre, o illeggibile dove si leggeva: l'host
  si ferma e parte l'avviso.
- T-A2-09 feed di YouTube: `youtube:<id>` solo per un id di 11 caratteri; `source_id` è il canale.
- T-A2-10 gli stop della riga «Raccolta» e di DEC-036, punto 3, su YouTube, uno per caso,
  compreso il rinvio al controllo anti-bot su un altro host: l'host si ferma, parte l'avviso, e
  riparte solo quando l'owner lo dice, come per RomaTV (T-A2-07), mai da solo il giorno dopo;
  con l'host fermo nessuna richiesta parte; ogni richiesta porta lo user agent dichiarato.
- T-A2-12 il ritmo della riga «Raccolta», con un orologio finto: le pause minime per host,
  dalla fine di una risposta alla richiesta seguente (5 secondi agli host di RomaTV, 1 a quello
  dei media, 60 a YouTube), una richiesta alla volta per fonte, e il tetto di 30 richieste di
  YouTube per giorno di Roma; lo stesso modulo dà il ritmo ai segmenti di A3.
- T-A2-11 la presa: due corse sulla stessa riga, una sola lavora; una presa scaduta si riprende;
  gli stati cambiano solo lungo la tabella della sezione 4. La presa di una fonte tenuta dal
  testo: l'elenco aspetta al più fino alla scadenza, poi salta la fonte e lo scrive nel
  registro; il testo che la trova presa non comincia.

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
- T-A3-08 sottotitoli di YouTube nella stessa forma; `youtube_asr`.
- T-A3-09 confine: apertura, sospensione, ripresa e chiusura a minuti inventati; resta solo la
  seduta aperta; del resto esistenza, minuto e durata.
- T-A3-10 ripresa non dichiarata: dal primo atto formale, con atto, minuto e motivo scritti;
  «sospesa» come argomento non sospende; «fuori verbale» non sospende.
- T-A3-11 seduta divisa: la seconda parte comincia aperta se la prima finisce aperta.
- T-A3-12 confine non fissabile: niente testo, `temporanei/` vuota con la cancellazione
  definitiva, `scartata`.
- T-A3-13 file di costo: uno per quantità con il suo prezzo e la sua `unita`, i token di
  `gpt-4o-mini-transcribe` e i secondi di `whisper-1`, 0,92 € per dollaro, i campi della riga
  «Costi»; una ripresa non ripete la spesa di un tratto fatto.
- T-A3-14 budget di tempo: la corsa si ferma pulita e la successiva riparte dal segmento giusto.
- T-A3-15 nessun testo nei registri e nelle spese: una parola marcatrice della fixture non
  compare.
- T-A3-16 esportazione di `staging_A_testo` (`tests/test_workflow_exports.js`): ogni nodo
  Google Drive che cancella ha `deletePermanently`; `executionTimeout` 300; i quattro
  `settings` dei dati della sezione 4; le chiamate a sé stesso e alla lettura senza attesa.

**Prove in staging** su n8n, con fonti vere e tutto privato: niente di queste prove entra nel
repository. Totale atteso circa 0,7 €, tetto 2 €, dentro la delega di DEC-036, punto 6.

| Prova | Che cosa dimostra | Costo atteso |
|---|---|---|
| Un Consiglio del V con la trascrizione della piattaforma | JSON del parlato, confine su parole con i tempi | 0 € |
| Una commissione del X | la strada dell'audio intera, pezzi, spesa | 0,07 € (30 minuti) |
| Una commissione capitolina | catalogo capitolino, nessun Municipio dal titolo | 0,10 € (45 minuti) |
| Una parte dell'Assemblea di 3 ore o più | memoria per esecuzione e tempo, ripresa su più corse | 0,50 € (3,5 ore) |
| Un video del Municipio I, solo se l'owner fa ripartire YouTube (sezione 2) | feed e sottotitoli dentro DEC-036, punto 3, o lo stop | 0 € |
| La stessa registrazione rifatta | nessun file doppio, nessuna spesa doppia | 0 € |
| Un errore forzato | `staging_A_avviso` scrive l'avviso in `letture/`, anche con i dati degli errori non salvati | 0 € |
| Un nodo Drive con la credenziale, creato con POST e cambiato con PUT, che scrive in `letture/` (A2) | la credenziale Drive regge sui flussi fatti dall'API (sezione 8, punto 3) | 0 € |
| `staging_A_sonda_catena` (A2) | i 300 secondi non passano a una corsa chiamata senza attesa; se le corse chiamate contano nel piano (sezione 4) | 0 € |
| Elenco (A2) e chiave (A3) senza `Origin` e `Referer`, una volta | se servono (sezione 4, la strada dell'audio, passo 3) | 0 € |
| Chiusura | `temporanei/` vuota e nessun suo file nel cestino (`trashed = true`); nessuna esecuzione con dati di audio o testo su n8n | 0 € |

**Il confronto dei modelli,** prima di A4, sugli intervalli della seduta aperta già fissati di
tre registrazioni delle prove: `whisper-1` (`verbose_json`) e `gpt-transcribe` contro il testo
di `gpt-4o-mini-transcribe` in `originali/`, tetto 1 € in tutto (con `whisper-1` 2 ore sono
circa 0,7 €; il prezzo di `gpt-transcribe` si legge prima di provarlo, e se non ci sta si
riducono le ore). Date di spegnimento lette dall'API di OpenAI (`/v1/models`) il 14 novembre,
sonda 918: `gpt-4o-mini-transcribe` e `whisper-1` il 26 febbraio 2027, a circa tre mesi e mezzo
dall'inizio; `gpt-4.1-mini` il 14 gennaio 2027; `gpt-5-mini` l'11 dicembre 2026; nessuna data
per `gpt-transcribe`, `gpt-live-transcribe` e `gpt-realtime-whisper`. A4 fissa un modello che
non si spenga a pilota in corso; il costo più basso vale solo fra `gpt-4o-mini-transcribe` e
`whisper-1`. Si misurano parole, quota di testo ripetuto (a giugno 57 registrazioni su 318
oltre il 10 %), grana dei tempi, nomi del gazetteer riconosciuti, tempo e spesa. In `letture/`
vanno solo i numeri. I testi degli altri modelli sono testo della seduta aperta e vanno in
`originali/`, accanto all'altro, con il modello nel nome; la lettura usa solo quello del
modello fissato.

## 7. Costi previsti per mese

| Voce | Base | € al mese |
|---|---|---|
| Trascrizione nostra | 123,3 ore a 0,157 $ l'ora (misura di giugno: 318 registrazioni, 227,7 ore, 35,76 $), 0,92 € per dollaro | circa 18 |
| Lettura e confine | circa 178 ore di testo (nostro, della piattaforma, di YouTube) con un modello di fascia media, al prezzo di `gpt-4.1-mini`, che si spegne il 14 gennaio 2027 (sezione 6): il prezzo si rilegge con il modello che sceglie A4 | 2–3 |
| Imprevisti | 20 % | circa 4 |
| Totale | | circa 25, nella quota di A di 27 € (CONTRATTI, sezione 5) |

Fuori dalla stima restano voci note, tutte verso l'alto:
- i Consigli del V e del X che l'elenco vede senza la trascrizione della piattaforma passano
  alla nostra (CONTRATTI, sezione 7 A, «Testo»; T-A2-05), come il Consiglio del X di fine
  ottobre: fino a 12,8 ore, circa 1,9 €;
- le commissioni capitoline di novembre vanno più forte di giugno: 9,3 ore in 3 giorni
  lavorativi, circa 65 al mese contro 51,6, circa 1,9 € in più;
- gli imprevisti al 40 % invece del 20, per le trascrizioni da rifare (a giugno 57
  registrazioni su 318 con più del 10 % di testo ripetuto, sezione 6): circa 4 € in più;
- la scrittura e la seconda verifica di A5: si fissano con A5, su quanto resta della quota.

Con le prime tre la stima arriva a circa 33 €, sopra la quota. Lo dicono le spese vere del primo
mese, nei file di `costi/`; se passano 27 €, il coordinatore lo dice all'owner, anche se il
totale del pilota resta sotto i 50 € (regola di questo brief, più stretta di CONTRATTI, sezione
5, che applica DEC-031, punto 6, al totale). I testi della piattaforma e i sottotitoli non costano.
`whisper-1` per tutto (0,006 $ al minuto) farebbe circa 41 €, più del doppio: fuori quota. Una
tantum, questo mese: le prove in staging (tetto 2 €) e il confronto (tetto 1 €). La spesa è una
stima dall'uso che OpenAI restituisce (CONTRATTI, sezione 7 A, «Costi»); la somma del mese la fa
il coordinatore.

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
   sui nodi Google Drive non è provato, e le sessioni precedenti hanno visto che la query di un
   nodo Drive con credenziale cambia solo ricreando il flusso con POST, con un id nuovo
   (`PASSAGGIO_2026-11-12.md`, sezione 5). A2 prova un nodo Drive con la credenziale
   «Google Drive account» in un flusso `staging_A`: creato con POST, cambiato con PUT, che scrive in
   `letture/`; finché non regge, i flussi non ci contano. Prima del PUT, nessuna esecuzione in
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
   `staticData`. I nodi Code identici byte per byte ai file di `code-nodes/`
   (`tests/test_workflow_exports.js`); `workflow_version` dell'«Inizio» cambia a ogni modifica.
10. **Chiudere.** Flussi di prova spenti, nessuna esecuzione con audio o testo su n8n,
    `temporanei/` vuota e senza file nel cestino (`trashed = true`); il passaggio
    `PASSAGGIO_<data>.md` nella cartella di passaggio (`CLAUDE.md`, «Consumption»).

## 9. Punti aperti

| Punto | Chi decide | Quando |
|---|---|---|
| DEC-014..DEC-021 sono citate come decise su `main` (DEC-022, DEC-034, DEC-108) ma stanno solo nel branch non unito `claude/quartieri-news-strategic-review-tzkl78`: DEC-015 (seconda verifica con un'altra AI, coda manuale, campione stratificato), DEC-014 (almeno 5 elementi di Amministrazione per pagina), DEC-020 (versioni e sospensione di un elemento). Valgono per il pilota? | owner | prima di A5 |
| I valori di `editorial_class` per `institutional`: si aggiungono con il build del gazetteer (CONTRATTI, sezione 2) | il builder propone, l'owner decide | A5 |
| Come una pagina pilota mostra i fatti di livello città e di livello Municipio (DEC-106, DEC-006); come un elemento porta più pagine e la portata | owner | A5 |
| Immagini degli elementi: nessuna regola decisa per questo blocco (DEC-101 è per gli eventi) | owner | A5 |
| Citazioni testuali del parlato | owner | A4 |
| Atti capitolini (ordini del giorno, convocazioni) per verificare i fatti: fuori da DEC-033, che copre gli atti dei Municipi I, V e X | owner | A4 |
| Prati: la pagina di consenso UE del 14 novembre ha fermato `www.youtube.com` (sezione 2). Se e come riprovare il feed e i sottotitoli, dentro DEC-036, punto 3; finché l'owner non decide, Prati resta senza testo | owner, avvisato con A1 | ora |
| Come si riconosce che due registrazioni di piattaforme diverse sono la stessa seduta. Quale apre il fatto lo dice già CONTRATTI, sezione 7 A, righe «Elemento» e «Identità»: la prima in cui il fatto è letto; le altre sono provenienza | builder | A5 |
| L'ora di riferimento di un video di YouTube: il feed dà solo la pubblicazione | builder | A2 |
| Il modello di trascrizione e quello della lettura: `gpt-4o-mini-transcribe` e `whisper-1` si spengono il 26 febbraio 2027, `gpt-4.1-mini` il 14 gennaio 2027 (API di OpenAI, sonda 918; sezione 6). A4 sceglie un modello che non si spenga a pilota in corso | builder; l'owner se il cambio costa 5 € o più | A4 |
| Se le corse chiamate da un altro flusso contano nel piano: se contano, A non ci sta già con A2 e A3 (sezione 4), e servono il piano superiore o meno corse | il builder misura, l'owner decide il piano | A2, prima di accendere l'elenco a orario |
| `Origin` e `Referer` del portale nelle richieste all'elenco e alla chiave: se servono, la PR che lo misura lo scrive in CONTRATTI, sezione 7 A | builder | A2 (elenco), A3 (chiave) |
| La stima di spesa con le voci che ne restano fuori arriva a circa 33 €, sopra la quota di 27 € (sezione 7) | il coordinatore, sulle spese del primo mese; l'owner se si va oltre | fine del primo mese |
| File del repository che hanno già testo di notizie preso dalle fonti: `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md`, sezione 6 («Possibili notizie»), e `docs/wiki/`. Segnalati, non toccati qui | owner | ora |

# DEC-033 — Lettura degli atti di Atti Web per lo storico del pilota

Status: DECIDED (9 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: nothing.

Context:
- Il workstream D (DEC-031) costruisce lo storico privato di DEC-023 scaricando atti e
  documenti dei municipi del pilota. Gli atti dei Municipi stanno su Atti Web,
  `https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/`.
- `docs/pilota/CONTRATTI.md`, sezione 6, chiede di controllare `robots.txt` e condizioni
  d'uso prima di leggere un sito. Il 9 novembre 2026, alle 21:44 UTC,
  `https://www.comune.roma.it/robots.txt` ha risposto con un rinvio (302) alla pagina di
  login SSO del Comune: le regole del sito non si possono leggere. Il builder non ha
  scaricato niente.
- Le condizioni d'uso, lette lo stesso giorno alle 23:00 UTC
  (`https://www.comune.roma.it/web/it/note-legali.page`): i diritti sui contenuti
  appartengono a Roma Capitale; non c'è una licenza di riuso e non c'è una regola
  sull'accesso automatico. Atti Web risponde senza login. Lo storico è privato e non
  ridistribuisce i documenti.
- Il 15 settembre 2026 l'owner aveva già autorizzato una lettura di approfondimento di Atti
  Web per lo studio delle fonti (Drive, `QN Hub / 20 Packages / Fonti 2026-06`,
  `README_Fonti_2026-06.md`: «approfondimento A2 autorizzato dall'owner»).

Question: con le regole del sito non leggibili, il workstream D legge gli atti di Atti Web?

Options:
A. **CHOSEN.** Sì, come a settembre: lettura lenta, solo nello staging su Drive, con data e
   perimetro dell'autorizzazione scritti nel registro. Prima la PR che fissa `archive_id` e i
   tipi di documento.
B. Prima si cercano gli atti su dati.comune.roma.it o in un altro canale aperto con licenza
   chiara; finché non si trova, D resta fermo.
C. D aspetta.

Claude recommendation: A. È la stessa autorizzazione di settembre, sugli stessi atti pubblici
e per un archivio privato; B resta utile in parallelo, ma da sola ferma il workstream.

Owner's words, 9 novembre 2026, fra le opzioni poste dal builder: «Autorizzo come a settembre».
Dopo la prima revisione di Codex, sulle note legali lette: «Confermo»; sul periodo: «Dal 1°
gennaio 2026, max 300/giorno».

## Regola

1. **Perimetro.** Gli atti di Atti Web dei Municipi X, V e I (le pagine pilota di DEC-031)
   dal 1° gennaio 2026 al giorno della lettura: l'elenco delle tipologie, l'elenco degli atti e i
   loro PDF.
   Nient'altro del sito. In pratica:
   - si interroga la ricerca degli atti con il filtro sulla data di repertorio (`dtRpr`),
     l'unico che il portale accetta (`docs/sources/A2_ATTIWEB_TIPOLOGIE.md`, sezione 2), dal
     1° dicembre 2025 al giorno della lettura. Il mese in più serve alle convocazioni
     protocollate prima di una seduta di gennaio;
   - la ricerca si fa una tipologia alla volta (il parametro `tipologia`), per tutte le
     tipologie che il portale elenca all'inizio della lettura (`caricaListaTipologie.action`;
     48 codici il 15 settembre, nella sezione 3 dello stesso documento). Il portale non filtra
     per struttura, e anche le tipologie degli organi centrali contengono atti di strutture
     municipali (sezione 3, `ACD`): limitarsi alle tipologie del Municipio ne perderebbe.
     Se l'elenco delle tipologie non si legge, la lettura non parte. L'errore «Index: 0,
     Size: 0» vale come tipologia vuota nel periodo (sezione 2) solo se la stessa tipologia,
     interrogata sull'intervallo storico, restituisce atti (sezione 7.1); altrimenti è un dato
     mancante (al 15 settembre, `XMO`): la lettura lo scrive nel registro e si dichiara
     incompleta, invece di contare la tipologia come vuota;
   - per ogni tipologia le pagine si leggono da 500 righe finché si arriva al totale
     dichiarato dall'API;
   - la data del record (`data_documento`) è `dtSeduta` quando c'è, altrimenti `dtRpr`;
   - si tengono gli atti dei tre Municipi con `data_documento` fra il 1° gennaio 2026 e il
     giorno della lettura: tutti e due i limiti valgono sulla stessa data che il record
     conserva. Un atto è dei tre Municipi quando `dscStrOrg` nomina una struttura del
     Municipio: «MUNIC…», poi «ROMA» se c'è, poi il numero romano, la forma che lo studio di
     settembre ha riconosciuto su tutte le 1.426 righe delle tipologie municipali
     (`tools/sources-study/a2_tipologie.py`). Il numero si confronta per intero: X non è IX
     né XI. Gli atti dei gruppi della Polizia Locale (`P.L. - <numero> GRUPPO …`, nella
     tipologia `DDS`) non sono di una struttura del Municipio e restano fuori da questa
     decisione: includerli è una scelta a parte. Il codice di D verifica l'abbinamento con
     i suoi test. Una convocazione per una seduta futura resta fuori e si prende
     a una lettura successiva, quando la seduta è passata.
2. **Ritmo.** Una richiesta alla volta, almeno 5 secondi fra due richieste e al massimo 300
   documenti al giorno.
3. **Dove.** Solo nello staging privato su Drive, `D Storico/originali/`. Nessun atto, testo o
   elenco entra su GitHub (DEC-109).
4. **Stop.** Al primo segnale di blocco (403, 429, captcha, rinvio al login sulle pagine degli
   atti) la lettura si ferma e non si aggira; si avvisa l'owner.
5. **Registro.** La riga di Atti Web nel registro fonti riporta la data di questa decisione e
   il perimetro del punto 1.
6. **Prima la PR di D.** I record dello storico si scrivono solo dopo la PR che fissa la forma
   di `archive_id` e i valori di `tipo` (`docs/pilota/CONTRATTI.md`, «Lo storico»).
7. **Nomi.** Negli atti vale DEC-105; gli originali restano privati.

Impact:
- **Workstream D.** Può partire dopo la PR del punto 6.
- **Registro fonti.** Una nota sulla riga di Atti Web.
- Nessun cambiamento a pipeline di produzione, gazetteer, prompt o CI.

Decided by: owner · Date: 9 novembre 2026 · Affected components: workstream D, registro fonti
(riga Atti Web), `D Storico/` nello staging su Drive.

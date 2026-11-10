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

Qui stanno le scelte. Il modo di leggere il portale (le tipologie, le pagine, le date, a
quale Municipio appartiene un atto, la chiave del documento, le versioni) sta nella sezione
«Lo storico» di `docs/pilota/CONTRATTI.md` e in `code-nodes/archive-record.js` con i suoi
test, che arrivano con la PR del punto 7. Si correggono con una PR, senza una decisione
nuova, purché restino dentro queste regole.

1. **Perimetro.** Gli atti di Atti Web delle strutture dei Municipi X, V e I (le pagine
   pilota di DEC-031), di qualunque tipologia del portale, con data dal 1° gennaio 2026 al
   giorno della lettura: l'elenco degli atti e i loro PDF. Nient'altro del sito. Gli atti dei
   gruppi della Polizia Locale non sono di una struttura del Municipio e restano fuori:
   includerli è una scelta a parte.
2. **Ritmo.** Una richiesta alla volta, almeno 5 secondi fra due richieste e al massimo 300
   documenti al giorno.
3. **Dove.** Solo nello staging privato su Drive, `D Storico/originali/`. Nessun atto, testo o
   elenco entra su GitHub (DEC-109).
4. **Stop.** Al primo segnale di blocco (403, 429, captcha, rinvio al login sulle pagine degli
   atti) la lettura si ferma e non si aggira; si avvisa l'owner.
5. **Completezza dichiarata.** Una lettura non si dichiara completa se qualcosa non si è
   potuto leggere o verificare: lo scrive nel registro, e la lettura successiva riprende lo
   stesso intervallo. Lo storico non perde e non sovrascrive niente: un documento cambiato
   alla fonte diventa una versione nuova.
6. **Registro.** La riga di Atti Web nel registro fonti riporta la data di questa decisione e
   il perimetro del punto 1.
7. **Prima la PR di D.** I record dello storico si scrivono solo dopo la PR che fissa la forma
   di `archive_id`, i valori di `tipo` e il modo di leggere il portale
   (`docs/pilota/CONTRATTI.md`, «Lo storico»).
8. **Nomi.** Negli atti vale DEC-105; gli originali restano privati.

Impact:
- **Workstream D.** Può partire dopo la PR del punto 7.
- **Registro fonti.** Una nota sulla riga di Atti Web.
- Nessun cambiamento a pipeline di produzione, gazetteer, prompt o CI.

Decided by: owner · Date: 9 novembre 2026 · Affected components: workstream D, registro fonti
(riga Atti Web), `D Storico/` nello staging su Drive.

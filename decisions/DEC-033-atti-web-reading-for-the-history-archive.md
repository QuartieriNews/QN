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

## Regola

1. **Perimetro.** Gli atti di Atti Web dei Municipi X, V e I (le pagine pilota di DEC-031):
   l'elenco degli atti e i loro PDF. Nient'altro del sito.
2. **Ritmo.** Una richiesta alla volta e almeno 5 secondi fra due richieste (il «lento» di
   questa decisione nei numeri proposti dal builder).
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

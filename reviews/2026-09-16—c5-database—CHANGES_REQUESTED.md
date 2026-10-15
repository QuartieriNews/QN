Di seguito il controllo C5, **solo su codice e schema**, senza ripetere i difetti già noti da audit umano.

## 1) Difetti del programma che producono numeri sbagliati/instabili

1) **[BLOCCANTE] Scrittura file Report 2 non protetta**
- **Righe:** `build_db.py` 462–464 (write `report2/coppie_parlato_scritto.csv`)
- **Problema:** anche se `report2/out_video` non esiste, il codice prova comunque a scrivere sotto `report2/`.
- **Effetto:** crash in ambienti “solo Report 1”; run non ripetibile.
- **Peso:** alto (blocco esecuzione).

2) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Scelta “lotto più recente” basata su confronto lessicografico fragile**
- **Righe:** 70, 73–75 (Lotti `L*_notizie.csv`), 197–199 (`[BX]*_atti.csv`)
- **Problema:** confronta stringhe (`L9` vs `L10`) e usa `[:3]`; se naming non è rigidamente zero-padded, vince il lotto sbagliato.
- **Effetto:** rimangono letture vecchie, scartate quelle nuove.
- **Peso:** medio/alto (può cambiare molte righe).

3) **[BLOCCANTE] Dedup non applica davvero la regola “2 su 3”**
- **Righe:** 406–408, 411–414
- **Problema:** il codice richiede sempre **data+luogo**; solo poi valuta oggetto. Quindi casi “data+oggetto” o “luogo+oggetto” non diventano mai `dubbio`.
- **Effetto:** sottostima di dubbi/duplicati; impatta anche `gemelli_scritti` (usa le stesse funzioni di match).
- **Peso:** alto sui numeri principali.

4) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Tie-break §4.1 non implementato**
- **Righe:** 386–417 (ordine confronto e scelta del “capo”)
- **Problema:** `prima_fonte` dipende dall’ordine in lista (`gruppo`), non da timestamp → ordine fonti → URL.
- **Effetto:** `prima_fonte` errata; con dedup “a catena” può cambiare anche l’esito netto su casi borderline.
- **Peso:** medio/alto.

5) **[DA CORREGGERE PRIMA DELLA CONSEGNA] `settimana` calcolata con data sbagliata**
- **Righe:** 117 (R1 notizie), 283 e 305 (video documenti/notizie)
- **Problema:** usa `data_fatto`/`data_seduta` invece di `data_pubblicazione` (schema 1.2 e 1.3).
- **Effetto:** tabelle `territori` e lacune settimanali distorte.
- **Peso:** medio (non sul KPI novità, ma su territoriali sì).

6) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Fonte notizia R1 presa dal CSV lettore, non dal documento**
- **Righe:** 107 (`'fonte': r['fonte']`)
- **Problema:** se il lettore sbaglia `fonte`, non c’è correzione da `documento_id`.
- **Effetto:** blocco errato (Amministrazione/Cronaca/Eventi), dedup errata, conteggi per fonte falsati.
- **Peso:** medio.

7) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Campi integrazione Report2 mai valorizzati**
- **Righe:** 116, 246, 304 (inizializzati vuoti), nessun punto successivo li riempie
- **Problema:** `integra_gemello_id` e `campi_integrati` restano sempre vuoti.
- **Effetto:** impossibile misurare il contributo informativo dei duplicati Report 2 (richiesta esplicita dello schema).
- **Peso:** alto sul valore analitico del Report 2.

8) **[DA CORREGGERE PRIMA DELLA CONSEGNA] `vicende.confidenza` dipende dall’ultima riga processata**
- **Righe:** 487
- **Problema:** sovrascrive ogni volta (`alta`/`bassa`) senza aggregazione robusta.
- **Effetto:** confidenza vicende instabile e potenzialmente sbagliata.
- **Peso:** medio.

9) **[DA CORREGGERE PRIMA DELLA CONSEGNA] ID documenti video fragile**
- **Righe:** 265, 325
- **Problema:** `j['item_id'].split('_')[1]` assume formato rigido; possibili collisioni/sovrascritture in `documenti`.
- **Effetto:** perdita silenziosa di documenti/notizie.
- **Peso:** medio (alto se naming eterogeneo).

10) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Metadato `fonti.report` errato per A3/A4**
- **Righe:** 537
- **Problema:** solo A2 marcata report `2`; A3/A4 finiscono `1`.
- **Effetto:** query/report per provenienza sbagliati.
- **Peso:** basso/medio (metadato, ma ufficiale).

11) **[VA BENE] Determinismo operativo**
- **Righe:** 68, 196, 319 (`sorted(glob)`), 395–399 (seed fisso)
- **Nota:** buona base di ripetibilità (al netto dei bug sopra).

---

## 2) Lo schema regge? (e dove perde informazione)

1) **[BLOCCANTE] Cardinalità dedup insufficiente (`gemello_id` singolo)**
- **Schema:** righe 86–87 (`notizie_candidate.gemello_id`)
- **Problema:** una notizia può avere più gemelli, ma lo schema ne ammette uno.
- **Conseguenza:** si perde struttura reale dei legami; per audit serve tabella N↔N dedicata.

2) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Mancanza tabella “accostamenti parlato-scritto” nello schema**
- **Codice:** 462–464 scrive CSV esterno `coppie_parlato_scritto.csv`
- **Problema:** informazione chiave fuori dalle 5 tabelle.
- **Conseguenza:** DB non autosufficiente per ricostruire il KPI novità.

3) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Drift schema↔codice su nomi colonne**
- **Schema:** riga 71 (`notizie_candidate.titolo`), riga 104 (`vicende.titolo`)
- **Codice:** 573–574 usa `titolo_anonimizzato`
- **Conseguenza:** client conformi allo schema non leggono i CSV prodotti.

4) **[DA DICHIARARE NEL RAPPORTO] Regola localizzazione in schema non allineata al codice**
- **Schema:** 152–155 (municipio fonte prevale)
- **Codice:** 90–92 (se testo ha municipio, prevale il testo)
- **Conseguenza:** incompatibilità metodologica; dedup luogo e territori cambiano.

5) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Vicende non auditabili secondo regola 3**
- **Schema:** 145–149 richiede legame esplicito (atto/seduta/procedimento)
- **Problema:** nello schema manca dove salvare **quale evidenza** ha fondato il legame.
- **Conseguenza:** `confidenza` non verificabile ex post.

---

## 3) Asimmetria unità di confronto (fatto vs documento): fix concreto senza rifare tutto

1) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Aggiungere una tabella ponte “fatti”**
- Nuova tabella minima: `fatti.csv` con `fatto_id`, `documento_id`, `notizia_id`, `seq`, `titolo_fatto`, `data_fatto`, `luogo_norm`, `evidenza_locale`.
- Per il parlato: 1 notizia = 1 fatto (copiato).
- Per lo scritto (atti/verbali): generare **più fatti per documento** con split automatico su pattern numerati (`punto 1`, `1)`, `ODG`, ecc.) nei campi già letti (`contenuto`/`oggetto_sintetico`), senza rilettura manuale.
- Confronto parlato↔scritto fatto-su-fatto; mantenere le tabelle correnti in parallelo.

Impatto: riduce falso “nuovo” da mismatch di granularità senza rifare i lettori.

---

## 4) Confronto esaustivo + dedup a catena: scelta difendibile?

1) **[DA DICHIARARE NEL RAPPORTO] Difendibile solo se separi chiaramente gli usi**
- Dedup a catena = resa netta (`unica/duplicato/dubbio`).
- Esaustivo parlato-scritto = copertura del parlato (`gemelli_scritti`).

2) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Oggi è una semi-bomba**
- Perché convivono nello stesso oggetto `notizie` e nei flussi a valle (es. `vicende`) senza barriera semantica.
- Serve separare output/metriche in modo esplicito (tabella accostamenti + regole di consumo).

---

## 5) Cosa farei prima di consegnare (ordine per impatto sui numeri)

1) **[BLOCCANTE] Correggere matching dedup (`2 su 3`) + tie-break §4.1** (righe 406–417).  
2) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Introdurre unità “fatto” per scritto** (almeno split automatico verbali/atti) e ricalcolare `gemelli_scritti`.  
3) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Sistemare selezione lotto più recente** (parse numerico lotto, non stringa).  
4) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Allineare `settimana` a data_pubblicazione** e rigenerare `territori`.  
5) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Popolare `integra_gemello_id/campi_integrati`** per rendere visibile il contributo Report 2.  
6) **[DA CORREGGERE PRIMA DELLA CONSEGNA] Hardening I/O e ID video** (niente crash se manca `report2`, ID robusti).  
7) **[DA DICHIARARE NEL RAPPORTO] Dichiarare tutte le deviazioni schema↔codice residue** (localizzazione, campionamento, colonne).  

Se vuoi, nel prossimo passaggio ti preparo una **checklist di test di regressione** (10 test) direttamente mappata a questi rilievi.

---
Controllo C5, modello gpt-5.3-codex, effort high, token 16508 in / 19378 out, 2026-09-16T10:35:53.241Z

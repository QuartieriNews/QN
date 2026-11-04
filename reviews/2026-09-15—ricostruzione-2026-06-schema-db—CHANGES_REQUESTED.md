# Controllo C1 — schema del database della ricostruzione di giugno 2026

Verdetto del revisore: **CHANGES_REQUESTED** (11 rilievi bloccanti, 1 non bloccante).
Revisore: Codex, `gpt-5.3-codex`, effort `high`, Responses API con `store: false`.
Data: 15 settembre 2026, 20:17 (Europe/Rome). Costo stimato: 0,16 € (13.377 token in
/ 11.079 out, listino stimato del ledger).

## Cosa è stato rivisto e contro cosa

Oggetto: `docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md` nella versione proposta
(commit precedente a questo). Riferimenti allegati alla richiesta:
`docs/sources/SOURCE_STUDY_METHOD.md` (regole §4.1–§4.3),
`tools/sources-study/lotto_opus5/SPECIFICA.md` (schemi di output collaudati),
`docs/sources/FATTIBILITA_RICOSTRUZIONE_2026-06.md` §9.6 (piano, consegne, controlli).
Mandato: `tools/sources-study/` (richiesta C1), eseguito con
`tools/sources-study/codex_check.js`.

Criteri di accettazione esercitati: nessuno eseguibile — il controllo precede
l'estrazione e l'oggetto è un documento di schema. `tests/test_guards.py` e
`tests/test_parse_duration.js` passano sul commit che applica le correzioni.

## Risposta ai rilievi, uno per uno

Tutti e dodici i rilievi sono **accettati**; due con una variante dichiarata (4, 8).
Nessuna rifiuta.

| # | Rilievo | Esito | Dove |
|---|---|---|---|
| 1 | La soglia dei 300 item era enunciata e poi contraddetta dagli Eventi (511) | accettato | §2 regola 2, riscritta: soglia applicata senza eccezioni, Cronaca intero mese, Eventi a campione |
| 2 | Campionamento senza frame ordinato né minimo per coppia | accettato | §2 regola 2: frame data → ordine fonti → URL, minimo 60 per coppia, seed `2026-06-E2xE3` |
| 3 | Il tie-break §4.1 vuole il timestamp, lo schema aveva la sola data | accettato | `documenti.timestamp_pubblicazione`, primo criterio del tie-break |
| 4 | Progressivo a 3 cifre insufficiente | accettato con variante | 4 cifre, non 5: il volume massimo del mese è 2.669 (A2). La variante è dichiarata nella colonna |
| 5 | `base_url` citato in `documenti` ma assente in `fonti` | accettato | colonna `base_url` in `fonti.csv` |
| 6 | Mancavano formato e difficoltà tecniche per item, che il Report 2 deve misurare | accettato | `formato_item`, `metodo_estrazione`, `ocr_incerto`, `trascrizione_incerta` |
| 7 | Report 1 e Report 2 separabili solo per fonte | accettato | `report_origine` in `documenti`, ereditato in `notizie_candidate` |
| 8 | La vicenda legata allo stesso `tipo` perde gli approfondimenti | accettato con variante | vincolo sul tipo tolto; resta obbligatorio il legame esplicito nel testo e si aggiunge `vicende.confidenza`, perché senza un vincolo il collegamento diventa somiglianza tematica |
| 9 | La non-riscrittura del Report 1 nascondeva le integrazioni | accettato | `integra_gemello_id`, `campi_integrati`; le viste nette scartano i duplicati che non integrano nulla |
| 10 | Il titolo copiato dalla pagina può contenere nomi (DEC-102) | accettato | `titolo_anonimizzato`; il titolo grezzo resta nello scratchpad |
| 11 | Il ripiego `tools/sources-study/session_b/out/` viola DEC-104 regola 2 | accettato | ripiego rimosso: Drive, altrimenti scratchpad e consegna dichiarata incompleta. Vedi la nota sotto |
| 12 | `prima_fonte` indecidibile sui dubbi; base di `settimana` non detta | accettato | `prima_fonte = non applicabile` sui dubbi; `settimana` da `data_pubblicazione` in Europe/Rome |

**Nota sul rilievo 11.** Il ripiego dentro il repository non era un'invenzione dello
schema: lo prescrive `tools/sources-study/HANDOFF.md` §2, scritto dalla sessione A. Il
rilievo resta fondato — DEC-104 è DECIDED e il repository è pubblico — e vince sulla
consegna, che non può allargare una decisione. Verificato inoltre che il connettore
Drive risponde e che la cartella `Fonti 2026-06/` è raggiungibile e già popolata: il
ripiego non serve in questa sessione. L'HANDOFF è un documento di lavoro della sessione
A, non una decisione; non lo correggo qui per non toccare il passaggio di consegne a
metà lavoro, ma la regola che vale è quella dello schema.

## Residui

Nessun residuo aperto dal revisore. Non marco questo lavoro APPROVED: il verdetto è del
revisore e la fusione è dell'owner (CLAUDE.md, AGENTS.md). Le correzioni applicate
tornano al revisore nel controllo C2, che vede lo schema in esercizio su un campione del
Report 1.

## Testo integrale del controllo

CHANGES_REQUESTED

1. **Bloccante** — `docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §2 regola 2: la regola di estensione dedup è in contraddizione con `SOURCE_STUDY_METHOD.md` §4.1 perché scrive “sotto i 300 item per blocco” ma riporta Eventi=511 e imposta comunque una dedup “misurata” non conforme alla soglia/campionamento; **correzione**: riscrivere la frase imponendo testualmente “intero mese solo se blocco ≤300 (o fonte unica), altrimenti campione ≥60 per coppia di fonti”.

2. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §2 regola 2: sul campionamento dedup mancano frame ordinato e regola minima per coppia richiesti da §4.1 (oggi ci sono solo seed E2/E3); **correzione**: aggiungere in una riga che il frame è ordinato per data→ordine fonti→URL e che la numerosità minima è 60 item per coppia, con seed registrato.

3. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.2 (`documenti.data_pubblicazione`) e §1.3 (`notizie_candidate.data_pubblicazione`): avete solo la data (AAAA-MM-GG), ma il tie-break §4.1 richiede timestamp completo quando disponibile, quindi due esecuzioni possono divergere; **correzione**: aggiungere un campo `timestamp_pubblicazione` (ISO con ora e timezone) opzionale ma prioritario nel tie-break.

4. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.2 colonna `id`: il formato `<fonte>_<progressivo a 3 cifre>` non regge volumi >999 (A2 nelle 3 settimane è già 1.056), quindi produce collisioni; **correzione**: portare il progressivo ad almeno 4 cifre (meglio 5) o usare un ID stabile non limitato.

5. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.2 colonna `url`: si cita un `base_url` in `fonti`, ma `fonti.csv` non ha quella colonna, quindi la regola è ineseguibile; **correzione**: aggiungere `base_url` in `fonti.csv` (opzionale) oppure imporre URL assoluti in `documenti.csv`.

6. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.2–§1.3 rispetto a `SOURCE_STUDY_METHOD.md` §4.2 e al bisogno Report 2: mancano campi per distinguere OCR/trascrizione e qualità tecnica per item (necessari per “difficoltà introdotte da OCR, trascrizioni, toponimi”) e manca il formato per item; **correzione**: aggiungere in `documenti.csv` almeno `formato_item`, `metodo_estrazione` (nativo/OCR/trascrizione), `ocr_incerto`, `trascrizione_incerta`.

7. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.3/§1.4: non c’è un campo `report_origine` a livello riga (documento/notizia), e `fonti.report` a livello fonte non basta a separare in modo robusto Report 1 vs Report 2 nelle analisi comparative; **correzione**: aggiungere `report_origine` obbligatorio (`1` o `2`) in `documenti.csv` e derivarlo in `notizie_candidate.csv`.

8. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §2 regola 3: la definizione di vicenda (“stesso tipo” + legame esplicito) è troppo restrittiva e perde casi reali di approfondimento con tipo diverso (es. evoluzione della stessa vicenda); **correzione**: togliere il vincolo rigido “stesso tipo” e basare il linking su stesso fatto/procedimento con continuità temporale, marcando il livello di confidenza.

9. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §2 regola 5: “Report 2 non riscrive Report 1” è corretto come vincolo, ma così formulato perde l’informazione di eventuali integrazioni/correzioni emerse dopo (restano su una riga duplicata che può essere esclusa nelle viste nette); **correzione**: mantenere la non-riscrittura ma aggiungere un campo/tabella di integrazione (`integra_gemello_id`, `campi_integrati`) collegato al gemello.

10. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.2 colonna `titolo` vs §3 “nessun nome di persona”: salvare il titolo pagina “as is” può includere nomi propri e violare DEC-102; **correzione**: rendere il campo esplicitamente anonimizzato (`titolo_anonimizzato`) o imporre redazione dei nomi prima del salvataggio.

11. **Bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1 (path fallback): il fallback `tools/sources-study/session_b/out/` è dentro il repository e viola DEC-104 se applicato alla lettera; **correzione**: spostare il fallback in un percorso esterno al repo pubblico (stesso perimetro Drive o directory locale extra-repo) e tenere nel repo solo riferimenti/aggregati.

12. **Non bloccante** — `...RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, §1.3 `prima_fonte` e §1.2/§1.3 `settimana`: è ambiguo cosa valorizzare per `prima_fonte` quando `dedup_stato = dubbio` e su quale data calcolare `settimana`; **correzione**: specificare “settimana da data_pubblicazione Europe/Rome” e ammettere `prima_fonte = non applicabile` per i dubbi.

Nota di allineamento (corretta): cutoff di giugno e gestione del gruppo “senza data” sono coerenti con `SOURCE_STUDY_METHOD.md` §4.1, quindi qui non propongo modifiche.

---
Controllo C1, modello gpt-5.3-codex, effort high, token 13377 in / 11079 out, 2026-09-15T18:17:53.961Z

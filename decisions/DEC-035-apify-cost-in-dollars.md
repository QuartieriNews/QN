# DEC-035 — Il costo Apify si registra in dollari e si converte in euro a fine mese

Status: DECIDED (14 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: nothing.

Context:
- Il budget del pilota è in euro (DEC-031, punto 6), e il coordinatore lo applica al totale
  del mese (`docs/pilota/CONTRATTI.md`, sezione 5).
- Apify addebita in dollari, e una corsa dichiara la sua spesa in dollari (`usageTotalUsd`).
  `staging_C_fb_events_fetch` la scrive nel registro delle spese così come la dichiara, nel
  campo `usd` (`code-nodes/apify-run.js`, PR #51).
- La revisione di Codex della PR #51 ha osservato che il registro non dice come quei dollari
  diventano euro: sommarli alle spese in euro darebbe un totale sbagliato.

Question: in che valuta si registra la spesa di una corsa Apify, e come entra nel totale del
mese in euro?

Options (A e B poste dal builder il 13 novembre; C è la prima strada indicata da Codex nel
thread della PR #51):
A. In dollari, come Apify la dichiara; il coordinatore converte in euro il totale del mese con
   il tasso di cambio della BCE di fine mese.
B. In dollari, con un tasso di cambio fisso.
C. In euro in ogni voce, convertita al momento della corsa, con il tasso e la sua data accanto.

Claude recommendation: A. Il registro resta la copia di quello che Apify addebita, e la
conversione si fa una volta, sul totale, con un tasso pubblico; un tasso fisso si allontana dal
cambio vero quando il dollaro si muove.
Codex recommendation (PR #51): C, oppure un contratto esplicito di valuta e conversione prima che
il registro entri nel totale del budget.

Decision: A.
- Una spesa Apify entra nel registro in dollari, nel campo `usd`, con la cifra che Apify
  dichiara.
- A fine mese il coordinatore somma i dollari del mese e li converte in euro con il tasso di
  riferimento euro/dollaro della BCE dell'ultimo giorno del mese per cui la BCE lo pubblica.
  Scrive il tasso e la sua data accanto al totale, poi applica DEC-031, punto 6.
- Nessun tasso fisso.

Impact: il registro delle spese del canale C resta com'è; il totale del mese del coordinatore ha
una conversione in più, con il tasso e la data scritti accanto.

Decided by: Owner · Date: 14 novembre 2026 · Affected components: `docs/pilota/CONTRATTI.md`
(sezione 5), `code-nodes/apify-run.js` (`costEntry`), il totale del mese del coordinatore.

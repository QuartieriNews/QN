# DEC-042 — La seconda verifica di DEC-015 vale già nel pilota privato

Status: DECIDED (18 novembre 2026, owner nella sessione del coordinatore)
Applica DEC-015 al pilota privato; non sostituisce DEC-015 né altre decisioni.
Blocks: niente. Ogni canale del pilota che scrive elementi pubblicabili porta la seconda
verifica prima di scriverli (Regola, punto 2).

Question: DEC-015 vuole che un contenuto si pubblichi da solo solo quando lo passano due AI
funzionalmente indipendenti, la prima che lo produce e la seconda che lo verifica sulla fonte.
Vale già nel pilota privato (DEC-031), o solo dal lancio pubblico?

Contesto:
- DEC-015 è nel registro con la PR che porta su `main` DEC-014…021, così come sono state decise
  l'11 settembre 2026: con la stessa risposta del 18 novembre l'owner le ha fatte entrare «come sono».
- Il pilota la cita come aperta: `docs/pilota/CONTRATTI.md`, sezione 7 A, mette la seconda
  verifica di DEC-015 fra le PR successive di A «se l'owner la conferma per il pilota», e
  `docs/pilota/WORKSTREAM_A.md` lega a questa scelta la chiave di un modello di un'altra
  famiglia, con A5.

Options:
A. **CHOSEN.** Vale già nel pilota privato: nessun elemento del pilota diventa pubblicabile senza
   la seconda verifica.
B. Vale dal lancio pubblico: nel pilota basta la prima AI con i controlli deterministici.

Claude recommendation: nessuna. Il coordinatore ha posto le due opzioni, con il costo in più
della seconda chiamata a un modello per ogni elemento.

Owner's words, 18 novembre 2026, al coordinatore, alla domanda «Il secondo controllo dell'AI
vale già nel pilota privato, dove costa un po' di più?»: «Sì, e il controllo vale già nel
pilota».

## Regola

1. Nel pilota privato vale DEC-015, «Rule», per ogni blocco: un elemento è pubblicabile solo se
   lo passano la prima AI, la seconda AI e i controlli deterministici; nel dubbio va in coda o,
   dove il canale non ha ancora una coda, non si pubblica.
2. Un canale che non ha ancora la seconda verifica non scrive elementi pubblicabili finché la
   PR che la porta non è unita. Quali modelli, quali soglie e quale spesa lo propone quella PR
   (DEC-015: «Models, providers and thresholds are defined during development»), dentro la
   quota del canale (`docs/pilota/CONTRATTI.md`, sezione 5).
3. L'indipendenza funzionale di DEC-015 vale anche nel pilota: la seconda verifica legge la
   fonte originale, non il testo della prima AI soltanto.

Impact:
- **Amministrazione (A).** La seconda verifica entra con A5; serve la chiave di un modello di un'altra famiglia
  (`docs/pilota/WORKSTREAM_A.md`, sezione 3).
- **Notizie (B).** La seconda verifica di DEC-108 per le notizie (CONTRATTI, sezione 7 B) segue questa
  regola.
- **Eventi (C) e gli altri canali.** Il coordinatore controlla, canale per canale, se oggi scrive elementi
  pubblicabili senza seconda verifica, e lo riporta all'owner prima di riaccenderlo.
- **Costi.** Una chiamata in più per ogni elemento: la stima entra nella PR di ogni canale.

Decided by: owner · Date: 18 novembre 2026 · Affected components: tutti i canali del pilota,
`docs/pilota/CONTRATTI.md`, `docs/pilota/WORKSTREAM_A.md`

# DEC-025 — Precedenza fra le fonti per lo stesso evento (doppioni)

Status: DECIDED (9 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: nothing.

Context:
- Il foglio unificato di ottobre 2026 (`eventi_unico.xlsx`, Drive) ha 1.957 righe da
  quattro aggregatori e 97 gruppi di doppioni (127 righe in eccesso), riconosciuti con
  criteri stretti: titolo quasi identico e date compatibili, oppure titolo simile con stessa
  data e luogo. I gruppi sono segnalati (`gruppo_doppione`, `doppione_di`), non risolti.
- Il pilota ha due canali di eventi (`docs/pilota/CONTRATTI.md`, sezione 7): Facebook e le
  pagine web dei siti del registro. Lo stesso evento può arrivare da tutti e due, e il canale
  «pagine web» non scrive elementi finché questa decisione non dice quale fonte comanda.
- La bozza di questa decisione era nella PR #21, non unita. Questo file la sostituisce.

Question: quale fonte prevale per i campi dell'evento (titolo, date, luogo, link) quando lo
stesso evento compare in più fonti?

Options:
A. **CHOSEN.** Precedenza per vicinanza alla fonte primaria: lettura diretta alla fonte >
   sito dell'organizzatore linkato > culture.roma.it > Facebook > Roma Today. I campi
   mancanti nella fonte che comanda si prendono dalla successiva (coordinate da Facebook,
   Municipio da culture.roma.it).
B. Precedenza per completezza: comanda la fonte con più campi compilati, a parità l'ordine
   di A.
C. Nessuna precedenza: i doppioni restano segnalati e la scelta è del redattore, uno per uno.

Claude recommendation: A. È la stessa scala della rintracciabilità già misurata
(`rintracciabile_alla_fonte`) e rende la regola verificabile da un test; B premia le fonti
più prolisse, non le più affidabili.

Owner's words, 9 novembre 2026, fra le opzioni poste dal builder: «Vince la fonte più vicina».

## Regola

1. **Ordine.** Per lo stesso evento comanda la fonte più vicina a quella primaria: la pagina
   dell'organizzatore letta direttamente (nel pilota, il canale `web_event` sul sito
   dell'organizzatore) > il sito dell'organizzatore linkato da un'altra fonte >
   culture.roma.it > Facebook (`fb_event`) > Roma Today.
2. **Campi mancanti.** Un campo vuoto nella fonte che comanda si prende dalla successiva
   nell'ordine che lo ha; il file dice da quale fonte viene ogni campo preso così.
3. **Niente si cancella.** La fonte che comanda dà l'elemento pubblicato. Le altre restano,
   segnate come doppioni di quell'elemento, e non si pubblicano da sole.
4. **Lo stesso evento.** Lo si riconosce con i criteri stretti del foglio di ottobre: titolo
   quasi identico e date compatibili, oppure titolo simile con stessa data e luogo. In caso
   di dubbio l'elemento va in coda, non si fonde.
5. **Si verifica con un test.** La fusione è un code node del flusso, con i suoi test, prima
   che un secondo canale di eventi scriva elementi.

Impact:
- **Pilota.** Il canale `web_event` può scrivere elementi quando la fusione del punto 5 è nel
  flusso; `docs/pilota/CONTRATTI.md`, sezione 7, si aggiorna con la PR che la porta.
- **Foglio di ottobre.** Con questa regola le 127 righe in eccesso diventano secondarie, e i
  conteggi per pagina (DEC-014) si calcolano sulle sole righe principali, quindi scendono.
- **PR #21.** La sua bozza di DEC-025 si toglie quando la #21 viene divisa.

Decided by: owner · Date: 9 novembre 2026 · Affected components: il flusso degli eventi del
pilota (fusione fra canali), `docs/pilota/CONTRATTI.md` sezione 7, `eventi_unico.xlsx`
(colonna `riga_principale`), la scheda dei doppioni della wiki delle fonti eventi.

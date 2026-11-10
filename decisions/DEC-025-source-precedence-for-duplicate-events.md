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
Sull'identità, alla domanda posta dopo la prima revisione di Codex: «Resta quella già
pubblicata».

## Regola

Qui stanno le scelte. Il modo di applicarle (come si riconosce lo stesso evento, quali campi
si prendono e come, che cosa succede in coda) sta nella sezione 7 di
`docs/pilota/CONTRATTI.md` e in `code-nodes/merge-duplicate-events.js` con i suoi test, che
arrivano con la PR della fusione. Si correggono con una PR, senza una decisione nuova, purché
restino dentro queste regole.

1. **Ordine.** Per lo stesso evento comanda la fonte più vicina a quella primaria: il sito
   dell'organizzatore (nel pilota, il canale `web_event`) > culture.roma.it > Facebook
   (`fb_event`) > Roma Today. La pagina letta direttamente e quella raggiunta da un link di
   un'altra fonte hanno lo stesso grado, perché sono tutte e due il sito dell'organizzatore:
   questo precisa i primi due gradi dell'opzione A. Il risultato non dipende dall'ordine di
   arrivo. Il «titolo» della domanda è il nome dell'evento alla fonte; il `title`
   dell'articolo lo scriviamo sempre noi e resta fuori dalla fusione
   (`docs/pilota/CONTRATTI.md`, sezione 2).
2. **Campi mancanti.** Un campo vuoto nella fonte che comanda si prende da una fonte
   successiva che lo ha, e il file dice da quale fonte viene ogni campo preso così. Tre
   limiti:
   - Roma Today dà solo titolo, link e ora, come indice di terzi (DEC-108); nessun altro
     campo si prende da lì;
   - la geografia non si copia: si prendono solo le prove del luogo, e zona e municipio si
     ricalcolano con il gazetteer, che vince su ogni documento. Questo precisa l'esempio
     dell'opzione A («Municipio da culture.roma.it»). Una geografia verificata a mano
     (`human_verified`) non si ricalcola (`docs/pilota/CONTRATTI.md`, sezione 2);
   - i campi che vanno insieme (inizio e fine, latitudine e longitudine) vengono dalla
     stessa fonte.
3. **Identità.** Resta l'identità dell'elemento dello stesso evento scritto per primo, che sia
   pubblicato, in coda o solo scritto (specifica v2.5, fase 2.1: l'identità non cambia): la
   risposta dell'owner («Resta quella già pubblicata») vale così anche per gli elementi non
   ancora pubblicati. Da chi comanda l'elemento prende i campi, non l'identità. Le altre
   copie restano, ciascuna con il suo `content_id`, e indicano l'elemento che resta; niente
   si cancella e le copie non si pubblicano da sole.
4. **Nel dubbio non si fonde.** Si fondono da soli solo due elementi che sono certamente lo
   stesso evento, con criteri almeno stretti quanto quelli del foglio di ottobre
   (`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21). Ogni caso dubbio o non previsto va
   nella coda di revisione e non si fonde: due eventi pubblicati entrambi sono un difetto
   minore di un evento vero nascosto. Allargare i criteri, cioè far fondere da soli casi
   che oggi vanno in coda, è una decisione dell'owner.
5. **Si verifica con un test.** La fusione è un code node del flusso, con i suoi test, prima
   che un secondo canale di eventi scriva elementi.

Impact:
- **Pilota.** Il canale `web_event` può scrivere elementi quando la fusione del punto 5 è nel
  flusso; `docs/pilota/CONTRATTI.md`, sezione 7, si aggiorna con la PR che la porta.
- **Foglio di ottobre.** Le 127 righe in eccesso si dividono fra fuse e in coda secondo i
  criteri della sezione 7; i conteggi per pagina (DEC-014) si ricalcolano sulle righe
  principali dopo aver fatto girare la fusione sul foglio.
- **PR #21.** La sua bozza di DEC-025 si toglie quando la #21 viene divisa.

Decided by: owner · Date: 9 novembre 2026 · Affected components: il flusso degli eventi del
pilota (fusione fra canali), `docs/pilota/CONTRATTI.md` sezione 7, `eventi_unico.xlsx`
(colonna `riga_principale`), la scheda dei doppioni della wiki delle fonti eventi.

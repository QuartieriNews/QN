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

1. **Ordine.** Per lo stesso evento comanda la fonte più vicina a quella primaria: la pagina
   dell'organizzatore letta direttamente (nel pilota, il canale `web_event` sul sito
   dell'organizzatore) > il sito dell'organizzatore linkato da un'altra fonte >
   culture.roma.it > Facebook (`fb_event`) > Roma Today.
   Il «titolo» della domanda è il nome dell'evento alla fonte (`pilot.source_title`): il
   `title` dell'articolo lo scriviamo sempre noi e resta fuori dalla fusione
   (`docs/pilota/CONTRATTI.md`, sezione 2).
2. **Campi mancanti.** Un campo vuoto nella fonte che comanda si prende dalla successiva
   nell'ordine che lo ha e che può darlo, e il file dice da quale fonte viene ogni campo preso
   così. Due limiti:
   - Roma Today dà solo titolo, link e ora, come indice di terzi (DEC-108); nessun altro
     campo si prende da lì;
   - la geografia non si copia: dalle altre fonti si prendono solo le prove del luogo
     (sede, indirizzo, coordinate), e zona e municipio si ricalcolano con il gazetteer, che
     vince su ogni documento. Questo precisa l'esempio dell'opzione A («Municipio da
     culture.roma.it»), che copiato alla lettera metterebbe un'etichetta della fonte al
     posto del calcolo canonico.
3. **Identità.** Un elemento già pubblicato tiene il suo `content_id` anche quando arriva una
   fonte che comanda (specifica v2.5, fase 2.1: l'identità non cambia): da quella fonte
   prende i campi, non l'identità. Se le fonti arrivano insieme, l'identità è quella della
   fonte che comanda. Ogni altra copia tiene il proprio `content_id` e punta all'elemento
   pubblicato; niente si cancella e le copie non si pubblicano da sole, quindi le righe della
   coda di revisione restano legate alla loro chiave.
4. **Lo stesso evento.** Si usano i criteri stretti del foglio di ottobre
   (`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21), così:
   - titoli normalizzati: scomposizione Unicode NFKD, via i caratteri non ASCII, minuscole,
     ogni segno che non è lettera o cifra diventa spazio, via le parole di due lettere o meno
     e le parole vuote dello script;
   - somiglianza: la maggiore fra la sovrapposizione delle parole (Jaccard) e il rapporto di
     `difflib.SequenceMatcher` sui titoli normalizzati; se uno dei due titoli normalizzati è
     vuoto (solo caratteri non ASCII o parole brevi) la somiglianza vale 0, come nello
     script, e la coppia non si fonde mai da sola;
   - date: il giorno di inizio a Roma e, se la fine è data dalla fonte, il giorno di fine;
     due eventi sono compatibili se i loro intervalli si toccano;
   - **stesso evento** se la somiglianza è almeno 0,85 e le date sono compatibili, oppure
     se è almeno 0,72 con lo stesso giorno di inizio e un luogo in comune per almeno metà
     delle parole;
   - **in coda, senza fondere**: una somiglianza almeno 0,72 con date compatibili che non
     basta per i casi sopra; un evento senza data; una serie confrontata con un evento
     singolo o con un'altra serie; due eventi che soddisfano i casi sopra ma con orari di
     inizio distanti più di 60 minuti (per esempio la replica pomeridiana e quella serale).
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

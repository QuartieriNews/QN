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

1. **Ordine.** Per lo stesso evento comanda la fonte più vicina a quella primaria: il sito
   dell'organizzatore (nel pilota, il canale `web_event`) > culture.roma.it > Facebook
   (`fb_event`) > Roma Today. La pagina letta direttamente e quella raggiunta da un link di
   un'altra fonte hanno lo stesso grado: sono tutte e due il sito dell'organizzatore, e il
   file canonico non registra come ci si è arrivati. Questo precisa i primi due gradi
   dell'opzione A. A parità di grado comanda la pagina propria dell'evento rispetto a un
   elenco (il segnale `identity_from_listing` in `quality.review_flags`), poi il `content_id`
   in ordine alfabetico, così il
   risultato non dipende dall'ordine di arrivo.
   Il «titolo» della domanda è il nome dell'evento alla fonte: il campo `event_name`
   dell'evento sorgente, che il file canonico conserva in `pilot.source_title`. I due canali
   lo scrivono (`docs/pilota/CONTRATTI.md`, sezione 7, aggiornata con il codice della
   fusione); i file già scritti senza quel campo lo ricevono dagli originali prima che la
   fusione giri, e un file che non lo ha ferma la fusione con un errore invece di non
   trovare doppioni. Il `title` dell'articolo lo scriviamo sempre noi e resta fuori dalla
   fusione (`docs/pilota/CONTRATTI.md`, sezione 2).
2. **Campi mancanti.** Un campo vuoto nella fonte che comanda si prende dalla successiva
   nell'ordine che lo ha e che può darlo, e il file dice da quale fonte viene ogni campo preso
   così: in `pilot.filled_from`, un oggetto che per ogni campo preso così dà il suo percorso
   (per esempio `event.latitude`) e il `content_id` dell'elemento da cui viene. La sezione 7
   di `docs/pilota/CONTRATTI.md` lo elenca con il codice della fusione, prima che la fusione
   scriva un file. Due limiti:
   - Roma Today dà solo titolo, link e ora, come indice di terzi (DEC-108); nessun altro
     campo si prende da lì;
   - la geografia non si copia: dalle altre fonti si prendono solo le prove del luogo
     (sede, indirizzo, coordinate), e zona e municipio si ricalcolano con il gazetteer, che
     vince su ogni documento. Questo precisa l'esempio dell'opzione A («Municipio da
     culture.roma.it»), che copiato alla lettera metterebbe un'etichetta della fonte al
     posto del calcolo canonico.
3. **Identità.** Fra gli elementi dello stesso evento resta l'identità di quello scritto per
   primo, che sia pubblicato, in coda o solo scritto nella cartella del canale (specifica
   v2.5, fase 2.1: l'identità non cambia). L'ordine lo dà `pilot.first_written_at`, l'ora UTC
   della prima scrittura del file, che poi non cambia; i file già scritti senza quel campo lo
   ricevono dall'ora di creazione del file su Drive prima che la fusione giri. A parità di
   `first_written_at` resta l'identità della fonte che comanda, con lo spareggio della
   regola 1.
   L'elemento che resta prende i campi dalla fonte che comanda, non l'identità. Ogni altra
   copia tiene il proprio `content_id` e il proprio file, con `pilot.duplicate_of` che punta
   all'elemento che resta; niente si cancella e le copie non si pubblicano da sole. Una riga
   della coda di revisione di una copia resta legata alla sua chiave e si chiude come doppione
   dell'elemento che resta.
4. **Lo stesso evento.** Si usano i criteri stretti del foglio di ottobre
   (`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21), così:
   - titoli normalizzati: scomposizione Unicode NFKD, via i caratteri non ASCII, minuscole,
     ogni segno che non è lettera o cifra diventa spazio, via le parole di due lettere o meno
     e le parole vuote dello script;
   - identificativi corti: un numero di una o due cifre, un numero romano scritto con I, V e
     X, o una lettera sola, tranne le parole e le elisioni italiane di una lettera (a, e, i,
     o; c, d, l). Escono dal confronto con le parole brevi, ma se i due titoli, o i due luoghi,
     non hanno gli stessi identificativi («Corso 1» e «Corso 2», «IX» e «XI», «Sala A» e
     «Sala B») la coppia non si fonde da sola;
   - somiglianza: la maggiore fra la sovrapposizione delle parole (Jaccard) e il rapporto di
     `difflib.SequenceMatcher` sui titoli normalizzati; se uno dei due titoli normalizzati è
     vuoto (solo caratteri non ASCII o parole brevi) la somiglianza vale 0, come nello
     script, e la coppia non si fonde mai da sola;
   - date: il giorno di inizio a Roma e, se la fine è data dalla fonte, il giorno di fine;
     due eventi sono compatibili se i loro intervalli si toccano;
   - luoghi che coincidono: tutti e due noti, con almeno metà delle parole in comune dopo la
     stessa normalizzazione (Jaccard almeno 0,5) e, se tutti e due hanno le coordinate, a non
     più di 1 km. Un luogo che manca, due luoghi con meno parole in comune («Biblioteca
     Esempio» e «Biblioteca Altrove») o coordinate più lontane non bastano per fondere;
   - **stesso evento** se i luoghi coincidono, gli identificativi corti sono gli stessi, gli
     orari di inizio, quando tutti e due li hanno, distano al massimo 60 minuti, e la
     somiglianza è almeno 0,85 con date compatibili oppure almeno 0,72 con lo stesso giorno di
     inizio. Il controllo sui luoghi è più stretto dello script di ottobre: un titolo generico
     («Open Day») non basta, e due eventi senza luogo (per esempio online) vanno in coda;
   - **in coda, senza fondere**: ogni altra coppia con somiglianza almeno 0,72 e date
     compatibili, per esempio la replica pomeridiana e quella serale; un evento senza data;
     una serie confrontata con un evento singolo o con un'altra serie;
   - **gruppi**: tre o più elementi si fondono solo se ogni coppia del gruppo è lo stesso
     evento. Se due elementi dello stesso gruppo vanno in coda fra loro, va in coda tutto il
     gruppo, così una catena di somiglianze non fonde due eventi che fra loro non lo sono.
5. **Si verifica con un test.** La fusione è un code node del flusso, con i suoi test, prima
   che un secondo canale di eventi scriva elementi.

Impact:
- **Pilota.** Il canale `web_event` può scrivere elementi quando la fusione del punto 5 è nel
  flusso; `docs/pilota/CONTRATTI.md`, sezione 7, si aggiorna con la PR che la porta
  (`source_title`, `first_written_at`, `filled_from` e gli altri campi della fusione).
- **Foglio di ottobre.** Con questa regola le 127 righe in eccesso diventano secondarie, e i
  conteggi per pagina (DEC-014) si calcolano sulle sole righe principali, quindi scendono.
- **PR #21.** La sua bozza di DEC-025 si toglie quando la #21 viene divisa.

Decided by: owner · Date: 9 novembre 2026 · Affected components: il flusso degli eventi del
pilota (fusione fra canali), `docs/pilota/CONTRATTI.md` sezione 7, `eventi_unico.xlsx`
(colonna `riga_principale`), la scheda dei doppioni della wiki delle fonti eventi.

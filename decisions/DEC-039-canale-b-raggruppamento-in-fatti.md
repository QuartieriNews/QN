# DEC-039 — Canale B: le scelte sul raggruppamento delle notizie in fatti

Status: DECIDED (15 novembre 2026, owner nella sessione del workstream B, sui consigli del
builder; punti 1, 2 e 3 per il pilota privato confermati dall'owner il 17 novembre 2026, punti 4
e 5 decisi dall'owner il 18 novembre 2026)
Punto 2 superato in parte da DEC-040 (16 novembre 2026): una scheda che fa nomi non si aggiunge
da sola a un fatto in cui un'altra scheda fa nomi. Il resto di questa decisione resta valido.
Blocks: niente per il pilota privato. Prima del lancio pubblico del blocco «Notizie» serve una
decisione a sé su che cosa diventa un dubbio (punto 3). Una notizia che non è cronaca si pubblica
solo dopo la regola del punto 5.

Question: il progetto del raggruppamento dei record di B in fatti lascia all'owner cinque scelte
(`docs/pilota/B_RAGGRUPPAMENTO.md`, sezione 10). Che cosa vale per il pilota privato?

Contesto:
- Il canale B raccoglie i record delle fonti, e `code-nodes/news-fact.js` dice che cosa
  permettono le fonti di un fatto (`docs/pilota/CONTRATTI.md`, sezione 7, «B · Notizie»).
  Manca il passo in mezzo, che dice quali record raccontano lo stesso fatto: senza, un fatto
  di stampa non arriva al secondo editore di DEC-108 e un comunicato di riepilogo non si
  divide nei suoi fatti (DEC-034, R-C01).
- Il progetto descrive quel passo e pone le cinque scelte, ciascuna con il consiglio del
  builder. La 1 e la 2 servono prima della prova in staging; la 3, la 4 e la 5 dopo.
- I due errori del raggruppamento non pesano uguale (progetto, sezione 1): fondere due fatti
  diversi può rendere pubblicabile un fatto e dargli una fonte che non ne ha scritto;
  dividere un fatto dà due articoli sullo stesso fatto. Le scelte 2 e 3 partono da qui.

Options, una per scelta, come le pone il progetto:
1. **La pagina di ogni record nuovo** della Questura, dei Carabinieri e di Abitare a Roma:
   leggerla, con circa 30 richieste al giorno in più, o restare all'elenco e al feed, dove
   un riepilogo della Questura si legge dal solo titolo.
2. **Quando due notizie si fondono da sole:** con due dettagli concordi, la regola che la
   prova di giugno usava fra comunicati e testate (`tools/cronaca-prova/ISTRUZIONI_AVANTI.md`),
   o con uno, quella che usava per i titoli delle testate chiuse
   (`tools/cronaca-prova/ISTRUZIONI_CHIUSE.md`).
3. **Che cosa diventa un dubbio:** (a) una riga nella coda di revisione, con due decisioni
   nuove e un ritmo quotidiano per le notizie; (b) il fatto in dubbio non si pubblica e
   compare in un elenco del giorno, e nessuno lo scioglie.
4. **L'indice delle testate chiuse:** quale indice, quando aprirlo e con quale spesa.
5. **Le notizie che non sono cronaca,** circa due terzi dei record delle testate: portarle
   nel blocco Notizie, o tenerle ferme.

Claude recommendation (progetto, sezione 10): 1, leggere la pagina; 2, due dettagli, con le
condizioni della prova, e rivedere la regola dopo; 3, (b) per il pilota privato e (a) prima
del lancio; 4, aprire l'indice dopo la prova, con una PR a sé; 5, tenerle ferme fino al primo
mese di cronaca.

Owner's words, 15 novembre 2026, nella sessione del workstream B: «Scegli tu le scelte
migliori». Le scelte sono quindi quelle che il builder consigliava, prese dall'owner per
delega: l'owner le conferma con il merge di questa entry, salvo i punti 4 e 5, che ha deciso
il 18 novembre (sotto). Dove un punto va oltre il consiglio
scritto nel progetto lo dice: è una lettura del builder.

Owner's words, 17 novembre 2026, al coordinatore: «Scelte 1, 2 e 3 di B_RAGGRUPPAMENTO.md: 1 sì;
2 due dettagli, da rivedere dopo la prova; 3 (b) per il pilota privato, (a) prima del lancio
ancora aperta.» Per i punti 1, 2 e 3 la delega del 15 novembre diventa una scelta espressa.

Owner's words, 18 novembre 2026, al coordinatore.
- Punto 4. Alla domanda su come avere titolo, link e ora delle testate chiuse, con le opzioni
  «Provare GDELT, gratis» (consigliata), «Dopo la prova delle notizie» e «Un servizio a
  pagamento»: «1 e 3 , valutiamo anche abbonamentj a pagamento e utilizzo del browser». Poi, letta
  la ricerca su indici, servizi e abbonamenti, fra «Prova gratis, poi scegli» (consigliata), «Solo
  Google News», «Subito un servizio a pagamento» e «Nessuno per ora», l'owner ha scelto «Prova
  gratis, poi scegli», così descritta: «Nel pilota privato uso Google News e GDELT solo per titolo,
  link e ora, con poche richieste; tu apri una prova gratuita di un servizio a pagamento; tra due
  settimane ti porto i numeri dei tre e decidi se pagare. Spesa oggi: zero.»
- Punto 5. Fra «Ferme per il primo mese» (consigliata), «Solo alcuni temi utili» e «Tutte, da
  subito», l'owner ha scelto «Tutte, da subito», così descritta: «Servono temi e una regola di
  pubblicazione per ciascuno prima di partire: più lavoro e più rischio di errori visibili.»
Per i punti 4 e 5 la delega del 15 novembre non vale più.

## Regola

1. **La pagina di ogni record nuovo si legge,** per la Questura, i Carabinieri e Abitare a
   Roma. Valgono le regole della raccolta (CONTRATTI, sezione 7 B, «Raccolta», e sezione 6
   per `robots.txt` e le condizioni d'uso). Il Faro Online ha già il testo intero nel feed.
   La lettura arriva con una PR di B: finché non è unita, la raccolta legge solo l'elenco o
   il feed.
   - Lettura del builder: «ogni» comprende il record la cui pagina non si è salvata in una
     corsa, che resta da leggere; come, lo fissa quella PR (CONTRATTI, sezione 7 B,
     «Raccolta»).
   - Lettura del builder: senza la pagina un comunicato non ha la data del fatto, e resta
     in dubbio quasi sempre (progetto, sezione 5, «Dubbio», e sezione 10, scelta 1). La
     replica della prova rilegge record raccolti dal 10 novembre, che la pagina non
     l'hanno comunque (progetto, sezione 8, punto 2): il suo rapporto conta a parte i
     dubbi dei fatti ufficiali, e la terza condizione del punto 2 si legge con quel conto.
     L'ordine fra la PR delle pagine e la prova lo propone B.
2. **Due notizie si fondono da sole con due dettagli concordi,** oltre al tipo, al luogo e
   alle date (progetto, sezione 5, «Certa»).
   - La prova in staging (progetto, sezione 8) va bene a tre condizioni: almeno il 95% delle
     fusioni automatiche è giusto; nessuna fusione sbagliata rende pubblicabile un fatto o
     gli dà una fonte che non ne ha scritto; i dubbi restano sotto il 10% delle schede di
     cronaca.
   - La regola si rivede dopo la prova. Se le fusioni sbagliano, si stringe.
   - Allargarla, cioè far fondere da soli casi che vanno in dubbio, resta una decisione
     dell'owner, come per gli eventi (DEC-025, regola 4).
   - Lettura del builder: i punti 2 e 3 valgono sulla sezione 5 del progetto com'è dopo la
     revisione della PR #57, cambiata dopo la scelta dell'owner. Tre cose sono diverse da
     allora, e l'owner le conferma con il merge. Un aggiornamento che non dice il giorno
     del suo fatto si aggiunge da solo, con le prove, a qualunque distanza: erano 60
     giorni. Se il giorno del fatto c'è in una sola delle due schede vale anche il
     confronto con il giorno di pubblicazione dell'altra. Un aggiornamento o un comunicato
     senza la data del fatto che non trova il suo fatto fra i dieci candidati resta in
     dubbio, dove prima apriva un fatto suo.
3. **Nel pilota privato un fatto in dubbio non si pubblica,** nemmeno se è ufficiale, e
   compare in un elenco del giorno: l'opzione (b). Nel pilota nessuno scioglie i dubbi.
   Che cosa vale prima del lancio pubblico resta aperto (owner, 17 novembre 2026). Il builder
   consiglia l'opzione (a): nella coda (`docs/REVIEW_QUEUE.md`) due decisioni per i dubbi di
   raggruppamento, «stesso fatto di …» e «fatto diverso», e un ritmo per le notizie, che DEC-034
   chiede già («Blocks»). La porta una decisione a sé.
   - Lettura del builder: vale anche per un aggiornamento finito in dubbio. Resta staccato
     dal suo fatto, che tiene il `case_status` di prima, finché il dubbio non è sciolto
     (progetto, sezione 5). R-C04, che DEC-034 fa valere già nel pilota privato, vuole che
     gli sviluppi arrivino al fatto: finché la coda non c'è, per un aggiornamento in dubbio
     questo resta indietro. È una delle ragioni per cui la coda serve prima del lancio.
4. **Il secondo editore dalle testate chiuse si sceglie dopo una prova gratuita di tre fonti:**
   Google News e GDELT, nel pilota privato, solo per titolo, link e ora, con poche richieste
   (DEC-108), e un servizio a pagamento in prova gratuita. Dopo due settimane il coordinatore porta
   all'owner i numeri dei tre, e l'owner decide se pagare. La misura arriva con una PR di B, che
   dichiara prima le richieste e la spesa. Finché non c'è, B non ha una fonte `news_index`, e sono
   pubblicabili quasi solo i fatti ufficiali.
   - Il servizio a pagamento provato è GNews, con la chiave del piano gratuito aperta dall'owner il
     18 novembre 2026. Sugli ultimi 30 giorni, in italiano, ha dato in tutto 6 articoli su Acilia,
     16 su Centocelle e 54 su «Prati Roma», questi quasi tutti fuori tema; con il paese limitato
     all'Italia, 3 per quartiere, tutti del Corriere. Negli articoli restituiti (al più 10 per
     ricerca con il piano gratuito) non c'erano RomaToday, Il Messaggero né Ostia TV. Google News,
     cercando «<quartiere> Roma» sugli ultimi 30 giorni, ha dato 38, 43 e 39 voci, con RomaToday
     per tutti e tre, Ostia TV per Acilia e Il Messaggero per Centocelle e Prati.
   - Lettura del coordinatore: con questi numeri GNews non serve, e un altro servizio a pagamento
     entra nella misura solo se una sua prova mostra le testate di Roma.
   - Lettura del coordinatore: «la testata», cioè il nome dell'editore, si legge con titolo, link e
     ora perché DEC-108 conta gli editori; il testo dell'articolo non si legge mai.
   - Lettura del coordinatore: leggere un giornale a pagamento con un browser automatico e un
     abbonamento, che l'owner aveva chiesto di valutare, è escluso. La dichiarazione di Il
     Messaggero sul text and data mining vieta l'uso automatico dei contenuti e dice che «I divieti
     ... si applicano anche ad Utenti abbonati, sia consumer che professionali».
   - Lettura del coordinatore: i termini di Google non danno un permesso esplicito per l'uso
     automatico della ricerca di Google News, che può smettere di rispondere senza preavviso. Per
     questo la misura usa poche richieste, e Google News non è la scelta finale.
5. **Le notizie che non sono cronaca entrano nel blocco Notizie del pilota da subito.** Il blocco
   le comprende; per pubblicarle servono temi e una regola di pubblicazione per ciascuno (le parole
   dell'opzione scelta). DEC-034 e DEC-108 restano la regola della cronaca: questo punto allarga il
   blocco oltre la cronaca senza cambiare i loro testi.
   - Lettura del coordinatore: i temi e le regole li propone il progetto di B e l'owner li approva
     prima che una di queste notizie si pubblichi. Fino ad allora la raccolta le tiene, con la loro
     scheda, e non le pubblica: «da subito» vuol dire che entrano nel blocco, non che si pubblicano
     senza regola.

Impact:
- `docs/pilota/CONTRATTI.md`, sezione 7 B: l'apertura e le righe «Raccolta» (punto 1),
  «Pubblicabile» (punto 3), «Raggruppamento» e «Costi»; sezione 3: le Data table di un
  workstream e la cartella `prove/`; sezione 5: una frase dice che la tabella delle quote
  comprende già i due spostamenti. È una lettura del builder, non una scelta dell'owner, e
  nessuna quota cambia: quella di B resta 8 €. La frase è stata letta tre volte come se le
  cifre fossero quelle di prima.
- `docs/pilota/B_RAGGRUPPAMENTO.md`: la sezione 10 rimanda a questa entry; la sezione 8
  rimanda al punto 2 per le condizioni della prova, e la sezione 11 dice dove sono le righe
  di CONTRATTI.
- Codice: `code-nodes/news-group.js`, che arriva con la PR B-R1 (progetto, sezione 9),
  applica i punti 2, 3 e 5; la stessa PR porta a questa entry i rimandi alle scelte 2, 3(b)
  e 5 nel nodo e nei test. La lettura delle pagine (punto 1) e la misura degli indici (punto 4)
  arrivano con PR di B. Il punto 5 com'è dal 18 novembre cambia il nodo: oggi ferma le notizie
  che non sono cronaca, e le porterà avanti con la regola dei temi, in una PR di B.
- `docs/REVIEW_QUEUE.md` non cambia ora: cambia con la decisione del punto 3, prima del
  lancio.
- DEC-034, DEC-108 e DEC-025 restano invariate. Nessun cambiamento a gazetteer, prompt, n8n
  di produzione, lane gate o CI.

Decided by: owner · Date: 15 novembre 2026; 17 e 18 novembre 2026 · Affected components: canale B del pilota,
`docs/pilota/CONTRATTI.md` (sezioni 3, 5 e 7 B), `docs/pilota/B_RAGGRUPPAMENTO.md`,
`code-nodes/news-group.js`, `code-nodes/news-collect.js` (punto 1), `docs/REVIEW_QUEUE.md`
(prima del lancio).

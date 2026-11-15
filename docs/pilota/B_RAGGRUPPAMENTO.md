# Workstream B · Notizie: il raggruppamento dei record in fatti

Stato: progetto, 15 novembre 2026. Nessun codice: arriva con le PR della sezione 9. Le regole
stanno altrove e qui si rimanda: elemento, identità, capofila e pubblicabilità in
`docs/pilota/CONTRATTI.md`, sezione 7, «B · Notizie»; le regole della cronaca in DEC-034 (R-C01,
R-C02, R-C04, R-C06, R-C08) e DEC-108; la fase 3, P-03 e P-09 in
`docs/sources/CRONACA_PROCESSO_2026-10.md`. Se una regola cambia, cambia là. Gli esempi sono
inventati; i numeri sono conteggi dello staging, senza testi (CONTRATTI, sezione 3).

## 1. Che cosa fa

Riceve i record della raccolta e dice quali raccontano lo stesso fatto: divide un record che ne
contiene più di uno (R-C01) e riconosce lo stesso fatto in fonti e giorni diversi, con i suoi
aggiornamenti (P-09). Il risultato va a `code-nodes/news-fact.js`, che ne ricava categoria,
capofila e attribuzioni. Non fa geografia, filtro né scrittura (fasi 4–7), e non scrive elementi
né righe della coda.

I due errori non pesano uguale. Due fatti diversi fusi in uno possono contare come due editori,
diventare pubblicabili (DEC-108) e attribuire il fatto a una testata che non ne ha scritto. Un
fatto diviso in due dà due articoli sullo stesso fatto. Il primo è il peggiore: una fusione è
automatica solo con le prove, il resto va in dubbio.

## 2. Che cosa entra

| Che cosa | Da dove | Note |
|---|---|---|
| I record | `B Notizie/letture/notizie_righe_<inizio>.json` (`code-nodes/news-parse.js`) | tutti i file con lavoro in sospeso, non solo quello dell'ultima corsa (sezione 6). Il passo 1 sistema due campi. Manca `source_channel`, che `news-fact.js` chiede: viene da `SOURCES` di `news-collect.js`, per la fonte in cui il record è stato letto. E `source_id` è quello della fonte letta, che per Il Faro Online è l'host del feed (`cdn.ilfaroonline.it`) e non quello del sito: il passo 1 mette al suo posto l'host dell'URL del record (`sourceIdFromUrl` di `news-identity.js`), come vuole CONTRATTI, sezione 2, perché da `source_id` `news-fact.js` ricava gli editori e le attribuzioni. La fonte letta resta nel record, in `page` (il nome del file in `originali/`): il canale viene sempre da lì, e un record già preparato, preparato di nuovo, dà lo stesso risultato. Se l'host dell'URL non è quello della fonte letta, né un suo sottodominio, né il dominio di cui la fonte letta è un sottodominio, il record si ferma (`fermo`, con il motivo) invece di diventare un altro editore: una proposta del builder |
| Il testo | `B Notizie/originali/`, la risposta in cui il record è stato letto | oggi Il Faro Online ha il testo intero nel feed, Abitare a Roma una descrizione di circa 150 caratteri, l'elenco dei Carabinieri un sunto di circa 200, la Questura solo il titolo. Con la scelta 1, il testo della pagina |
| I fatti | la tabella dei fatti (sezione 3), tutta: due delle ricerche della sezione 5 non hanno limite di giorni | un fatto `in_dubbio` può essere candidato, un fatto `unito` no. Quante righe legge un passaggio e in quanto tempo lo misura la prova (sezione 8); come caricare solo i fatti che servono, quando la tabella cresce, lo fissa B-R2 |

Dall'11 al 14 novembre 2026: circa 60 record nuovi al giorno (29 di Abitare a Roma, 28 di Il Faro
Online, 2–3 della Questura, meno di uno dei Carabinieri). Dai titoli, è cronaca circa un terzo dei
record delle due testate, forse meno, e quasi tutti quelli della Questura. I record della Questura
non hanno data: `news-parse.js` non ne legge (in una sonda del 15 novembre l'elenco mostrava un
giorno per voce: da verificare). Le testate chiuse non entrano: B non ha una fonte `news_index`
(scelta 4).

## 3. Che cosa esce

- **Le schede,** una per fatto letto in un record, con l'id del record (l'URL canonico di
  `code-nodes/news-identity.js`) e il posto `n` del fatto, come lo fissa CONTRATTI, riga
  «Identità». Campi, nessuno con nomi di persona (i nomi sono dei passi dopo: DEC-108, punto 2;
  DEC-034, punto 5):
  - `ambito`: `cronaca` o `non_cronaca`; `tipo`: l'elenco di `tools/cronaca-prova/ISTRUZIONI_CHIUSE.md`;
  - `data_fatto`: il giorno di Roma in cui il fatto è avvenuto, non quello del comunicato (R-C08), o
    vuota;
  - `luoghi`: ognuno con il testo della fonte e il livello (`via`, `luogo`, `quartiere`, `altro`);
    la geografia è della fase 4, con R-C06;
  - `dettagli`: ognuno con un genere e un valore. `eta` e `persone` sono numeri interi (gli anni,
    quante persone); `oggetto` e `mezzo` un testo breve. Due dettagli sono uguali quando hanno lo
    stesso genere e lo stesso valore: i numeri come numeri, i testi normalizzati come quelli dei
    luoghi (senza maiuscole, accenti, punteggiatura e spazi ripetuti); `oggetto` e `mezzo` valgono
    come un genere solo, perché la stessa cosa si trova scritta nei due modi. Un valore in un'altra
    forma («due», «2 persone») è una risposta fuori forma (sezione 6). Due parole diverse per la
    stessa cosa («auto», «vettura») non sono uguali: la scheda allora non si fonde da sola, va in
    dubbio;
  - `case_status` e `persone`, i segnali dei casi di DEC-034, punto 5, come la scheda della fase 2;
  - `aggiornamento`: vuoto, o `convalida`, `scarcerazione`, `processo`, `sentenza`, `indagini`, `altro`.
    Una scheda con `aggiornamento` è di cronaca e porta il `tipo` e la `data_fatto` del fatto a cui
    l'aggiornamento si riferisce, non quelli della convalida o della sentenza (R-C01: l'aggiornamento
    è dello stesso fatto);
  - `sintesi`: una riga.
- **I fatti,** uno per gruppo: il `content_id` di CONTRATTI sulla scheda che lo ha aperto;
  `aperto_il`, l'istante UTC della prima scrittura, che non cambia; lo stato (`aperto`,
  `in_dubbio`, `unito`); i record, con il ruolo `apre`, `stesso_fatto` o `aggiornamento` (una
  scheda con `aggiornamento`). I record sono nella forma che `news-fact.js` legge: il nodo non cambia.
- **I dubbi.** Un fatto `in_dubbio` porta i `content_id` dei candidati (nessuno, se è in dubbio per
  una lista tagliata: sezione 5) e riceve `duplicate_doubt` e
  `requires_review`, i segnali degli eventi (CONTRATTI, «La fusione dei doppioni»). Non si pubblica
  finché il dubbio non è sciolto (scelta 3).
- **Le spese** del modello, un file per spesa in `B Notizie/costi/` (CONTRATTI, sezione 5).

Finché il canale non scrive elementi, schede e risposte del modello stanno nella Data table
`staging_B_schede`, i fatti in `staging_B_fatti`, il rapporto di una prova in `B Notizie/prove/`.
Nessun file `roma__nws__…json`, nessuna riga nella coda, niente sul sito.

## 4. Che cosa è deterministico e che cosa chiede un modello

| Passo | Chi | Che cosa |
|---|---|---|
| 1 Preparazione | codice | il lavoro in sospeso, nell'ordine di lettura (sezione 5): `source_channel`, `source_id` dall'URL del record, id del record, giorno di Roma |
| 2 Schede | **modello** | da titolo e testo di un record, le sue schede. Il codice controlla la forma: un valore fuori elenco, una data impossibile o un record senza schede sono una risposta fuori forma, che si richiede e alla terza corsa ferma il record (`fermo`, con il motivo: sezione 6), mai indovinati |
| 3 Candidati | codice | per ogni scheda di cronaca, i fatti con cui potrebbe coincidere (sezione 5) |
| 4 Giudizio | **modello** | per una scheda con candidati, una chiamata: per ogni candidato `stesso`, `forse` o `diverso`; per `stesso` le prove, cioè la scheda del fatto, il luogo e i dettagli che coincidono |
| 5 Verifica e posto | codice | con le regole della sezione 5: la scheda si aggiunge a un fatto, ne apre uno o resta in dubbio |
| 6 Fonti del fatto | codice, `news-fact.js` | categoria, pubblicabile, capofila, attribuzioni, come oggi |

Il modello legge e propone, il codice decide. Ogni regola sta nel codice con un test.

Come fornitore di modelli su n8n c'è solo OpenAI (`docs/pilota/WORKSTREAM_A.md`, sezione 3). Il
modello lo fissa B-R2 (sezione 9): piccolo, e che non si spenga prima della fine del pilota (le date
da `/v1/models`, come per A). Fa schede e giudizi, con due prompt di record in `prompts/` ed esempi
inventati.

## 5. Le regole del confronto

- **Candidati:** i fatti con una scheda di cronaca di un tipo della stessa famiglia (una tabella nel
  nodo, con i test: per esempio furto, rapina e truffa insieme), cercati in tre modi:
  - **per data:** con la data del fatto in tutte e due le schede, al più 3 giorni (P-09); altrimenti
    al più 7 giorni fra le date di pubblicazione: la prova di giugno cercava da 7 giorni prima del
    comunicato a 5 dopo (`ISTRUZIONI_AVANTI.md`), qui nei due versi perché si confrontano anche due
    testate. Un record senza ora di pubblicazione usa il giorno della corsa che lo ha visto per primo
    (`retrieved_at`). Se la data del fatto c'è in una sola delle due schede, si confronta anche con
    il giorno di pubblicazione dell'altra, con gli stessi 7 giorni: una proposta del builder, per il
    comunicato che arriva tardi ma dice il giorno del fatto (P-03). Il giorno di pubblicazione di una
    scheda con `aggiornamento` non entra in nessuno di questi confronti, perché un aggiornamento esce
    dopo il suo fatto (R-C08: la data è quella del fatto): quella scheda si confronta per data solo
    con la sua `data_fatto`;
  - **per luogo, senza limite di giorni:** i fatti con lo stesso luogo di livello `via` o `luogo`
    (testi normalizzati uguali). Un comunicato arriva anche giorni o mesi dopo il fatto (P-03, R-C08):
    così ritrova il fatto che la stampa ha già scritto;
  - **tutti i fatti già nella tabella, senza limite di giorni,** in due casi: quando la scheda ha un
    `aggiornamento`, perché un aggiornamento deve ritrovare il suo fatto anche dopo mesi (R-C01,
    R-C04); e quando è di una fonte ufficiale e non ha la data del fatto, perché il giorno di un
    comunicato non dice quando il fatto è avvenuto (P-03).

  Al più 10 candidati, scelti con quello che il codice sa già confrontare, guardando di ogni fatto
  la scheda che ha più cose uguali: prima i fatti che possono essere certi (qui sotto: lo stesso
  luogo di livello `via` o `luogo` e le date a posto); poi gli altri, prima quelli con più cose uguali
  (lo stesso luogo ne conta una, ogni dettaglio uguale una) e, a parità, prima quelli trovati per
  data; poi i più vicini per data; infine in ordine di `content_id`. Così un fatto che ha le prove
  non esce dalla lista per far posto a fatti solo più recenti, e i fatti vecchi di un luogo dove ne
  accadono molti non tolgono il posto a quelli dei giorni vicini. Il tetto di 10 e quest'ordine sono
  proposte del builder, senza una fonte. Dove il codice non ha niente da confrontare (nessun luogo
  di livello `via` o `luogo`, nessun dettaglio uguale) decide la vicinanza per data, che per un
  aggiornamento o un comunicato lontani dal loro fatto dice poco: oltre i 10 quel fatto non arriva al
  passo 4. Per questo, per una scheda che cerca fra tutti i fatti, una lista tagliata non basta a
  dire «diverso» (qui sotto, «Dubbio»); la prova conta le liste tagliate (sezione 8). Le date sono
  giorni di Roma.
- **Certa,** la scheda si aggiunge da sola: il modello dice `stesso` e il codice trova, nella scheda
  e nella scheda del fatto che il modello cita, la stessa famiglia di tipo, lo stesso luogo di
  livello `via` o `luogo` (testi normalizzati uguali; un quartiere non basta; una strada lunga qui non
  si riconosce, e la prova conta le fusioni fatte su una via), i dettagli che la regola chiede con
  lo stesso valore, e le date a posto. Le date sono a posto in due casi: le due schede stanno nella
  finestra della ricerca per data; oppure la scheda ha un `aggiornamento` senza la data del fatto e
  la scheda citata viene prima di lei, a qualunque distanza (la data del fatto della scheda citata
  o, se manca, il giorno del suo record non è dopo il giorno del record dell'aggiornamento), perché
  un aggiornamento si aggancia al suo fatto (R-C01). Un aggiornamento che dice il giorno del suo
  fatto vale come le altre schede: conta la finestra. Fuori da questi due casi niente è certo, e la
  scheda va in dubbio: quando ha trovato il fatto solo per luogo, quando è un comunicato senza la
  data del fatto lontano dal suo fatto, quando la scheda citata è un aggiornamento senza la data del
  fatto. Quanti dettagli è la scelta 2. Una scheda le cui date vengono solo da `retrieved_at` non è
  mai certa. Il codice controlla che le prove ci siano, non che il modello abbia ragione: quello lo
  misura la prova (sezione 8).
- **Dubbio:** un `stesso` senza prove verificate, o un `forse`; anche una scheda certa con due fatti,
  perché un ponte non fonde due fatti da solo. E una scheda che cerca fra tutti i fatti (un
  aggiornamento, un comunicato senza la data del fatto) quando la lista dei candidati è stata
  tagliata e nessuno dei dieci è `stesso` o `forse`: i fatti rimasti fuori non li ha giudicati
  nessuno, e il suo può essere fra quelli (R-C01). Apre il suo fatto in dubbio, con il motivo
  `lista_tagliata` e senza candidati.
- **Diverso:** nessun candidato, o `diverso` per tutti, salvo la lista tagliata qui sopra. La scheda
  apre un fatto suo.
- **La scheda in dubbio** apre il suo fatto, `in_dubbio`. I candidati vanno avanti: a differenza
  degli eventi (`merge_deferred`), il dubbio ferma solo chi è in dubbio. Vale anche per un
  aggiornamento: finito in dubbio, non aggiorna il suo fatto finché il dubbio non è sciolto (R-C04
  vuole che gli sviluppi arrivino al fatto: scelta 3).
- **L'ordine di lettura:** le schede prendono posto nell'ordine dei file (`<inizio>`), poi del record
  nel file, poi di `n`. Le schede prendono posto solo fino al primo lavoro, in quest'ordine, che
  aspetta ancora una risposta del modello: un record senza schede, o una scheda con candidati senza
  un giudizio salvato; i passi 2 e 4 possono intanto salvare le risposte di quelli dopo. Così
  l'ordine è lo stesso comunque le corse si dividano il lavoro, e decide chi apre il fatto; la
  capofila la sceglie `news-fact.js` con la sua regola (CONTRATTI 7 B, «Capofila»). Un record tiene
  il suo posto finché le corse della sezione 6 non lo fermano: fino ad allora gli altri aspettano.
  Un record `fermo` non trattiene più gli altri: ripartito a mano, è l'unico che prende posto fuori
  ordine, e può trovare il suo fatto già aperto da un record venuto dopo. Il `content_id` di quel
  fatto resta quello dato: un'identità assegnata non cambia (CONTRATTI, sezione 2).
- **Due fatti che diventano uno,** quando un dubbio si scioglie: resta quello con l'`aperto_il` più
  vecchio, a pari istante il primo per `content_id`, con il suo `content_id`; l'altro riceve
  `duplicate_of` e non si pubblica. Un comunicato che arriva dopo la stampa si aggiunge al fatto e ne
  diventa la capofila (`news-fact.js`); il `content_id` resta.
- **Le schede `non_cronaca`** si scrivono e si fermano lì: aspettano la scelta 5.

**Esempio inventato.** Il comunicato di un ente racconta due interventi in un quartiere immaginario:
l'incendio di un garage in via dei Mandorli Finti, con due persone di 70 anni soccorse, e il recupero
di un'auto rubata. Dà le schede 1 e 2. Il giorno dopo una testata aperta scrive dell'incendio di un
garage in via dei Mandorli Finti e di due settantenni soccorsi. Il modello dice `stesso` per il
fatto della scheda 1 e cita la via, «2 persone» e «70 anni», che il codice trova in tutte e due le
schede: certa. Il fatto resta `qn:roma:nws:<chiave del comunicato>-f1`, con due fonti.

## 6. Corse ripetute, interrotte o insieme

- **Il lavoro in sospeso** è un record senza schede o una scheda di cronaca senza posto in un fatto;
  una scheda `non_cronaca` non prende posto (sezione 5) e non è lavoro in sospeso. Un record
  `fermo` non lo è: compare nel rapporto e riparte solo a mano, e la ripartenza riporta il segnalibro
  (qui sotto) al suo file. Una risposta fuori forma conta come una risposta che manca: non si salva,
  e la chiamata si rifà alla corsa dopo. Una risposta che manca, o fuori forma, in tre corse che
  hanno mandato la chiamata ferma il record (`fermo`) o, al passo 4, manda la scheda in dubbio: così
  niente trattiene gli altri per sempre, e una risposta sbagliata una volta sola non cambia chi apre
  un fatto. Le corse che non hanno mandato la chiamata (budget finito, presa occupata) non contano.
- Le risposte del modello si salvano prima di mettere le schede al loro posto: le schede di un
  record, e il giudizio di una scheda con la lista a cui risponde, cioè i candidati e, di ognuno, le
  schede mostrate al modello. Una corsa che ritrova la stessa lista usa il giudizio salvato: rifatta
  sugli stessi record, non chiama il modello e dà gli stessi fatti. Un candidato che nel frattempo
  ha preso una scheda in più non è più la stessa lista: il giudizio salvato non vale, e si chiede
  di nuovo.
- Una corsa interrotta lascia quello che ha scritto; la corsa dopo riparte dal file più vecchio con
  lavoro in sospeso, che un segnalibro nella tabella dei fatti tiene aggiornato (i `fermo` non
  contano), così una corsa non rilegge tutti i file dal 10 novembre. Nessun record si perde, nemmeno
  quando il modello non ha risposto o la corsa ha trovato la presa occupata; si ripaga solo la
  chiamata in corso al momento dell'interruzione.
- Gira un raggruppamento alla volta, con una presa nella tabella dei fatti che scade dopo 5 minuti e
  si rinnova a ogni scheda messa al suo posto, come in A (`WORKSTREAM_A.md`, sezione 4). Il flusso è
  suo, mai dentro l'esecuzione della raccolta: se è la raccolta a chiamarlo, lo chiama senza
  aspettarlo, e un suo errore non la ferma. Imposta i 300 secondi e smette di prendere lavoro a 4
  minuti dall'inizio dell'esecuzione, come i flussi di A («I limiti misurati»); quello che non ci sta
  va alla corsa dopo.
- Un testo cambiato alla fonte oggi non si vede: `news-parse.js` non rilegge un URL già visto. Il
  raggruppamento lavora sul record come è stato letto la prima volta; accorgersi delle modifiche
  tocca a un passo successivo (CONTRATTI, sezione 2, dice che cosa cambia allora).
- Cinque risposte di fila mancate o fuori forma fermano i passi 2 e 4, con l'avviso; ripartono quando il
  coordinatore li riaccende, e il lavoro in sospeso si riprende.
- **Esecuzioni di n8n.** Il piano Starter ne ha 2.500 al mese, già strette (`WORKSTREAM_A.md`,
  sezione 4). La prova mette più file in un'esecuzione, circa una per giorno di dati: una trentina
  in tutto. In esercizio ogni avvio è una corsa: chiamato dalla raccolta ogni ora, circa 720 al
  mese se le corse chiamate contano (lo misura A2), o a orario ogni 3 ore, 240. Lo fissa B-R2 con
  quella misura. Se le corse chiamate contano, tutte e due le strade portano il piano oltre le
  2.500 insieme ad A (`WORKSTREAM_A.md`, sezione 4): la domanda sul piano della sezione 9 di
  `WORKSTREAM_A.md` comprende anche B.

## 7. Costo

Circa 60 chiamate al giorno per le schede (una per record, da circa 1.500 token in entrata e 150 in
uscita) e una ventina per i giudizi (circa 1.600 e 100: di solito uno per scheda di cronaca, perché
quasi tutte hanno candidati): al mese circa 3,7 milioni di token in entrata e 0,3 in uscita. Al
listino di `gpt-4.1-mini` (0,40 $ e 1,60 $ per milione, letto il 15 novembre 2026) sono circa 2 $,
circa 1,8 €, sugli 8 € della quota di B (CONTRATTI, sezione 5: la tabella comprende già gli
spostamenti del 14 e del 15 novembre), che paga anche la scrittura. È solo un riferimento: quel
modello si spegne il 14 gennaio 2027 (`WORKSTREAM_A.md`, sezione 6), e B-R2 rilegge il prezzo del
suo. La lettura delle pagine (scelta 1) aggiunge qualche decina di centesimi.

## 8. La prova in staging, senza pubblicare

La prova scrive solo nelle due Data table, in `B Notizie/prove/` e in `B Notizie/costi/`: niente
elementi, righe della coda o file del sito, e `staging_B_notizie_raccolta` non si tocca.

1. **Nel repository, senza rete:** `tests/test_news_group.js`, con record e risposte del modello
   inventati: finestre (anche a cavallo del cambio dell'ora), famiglie, candidati trovati per luogo o
   perché già nella tabella, un aggiornamento che si aggancia al suo fatto dopo mesi, un comunicato
   senza data del fatto che va in dubbio, la scelta dei 10 che tiene il fatto con le prove e quello
   dei giorni vicini, una lista tagliata che manda in dubbio chi cerca fra tutti i fatti, il giorno
   di un aggiornamento che non vale come giorno del fatto, dettagli uguali per valore e non per
   forma, `source_id` dall'URL del record e il canale dalla fonte letta, certa, dubbio e diverso,
   prove
   citate che non ci sono, luoghi solo di quartiere, date solo da `retrieved_at`, un ponte, l'ordine,
   id stabili, `-f<n>` fisso, record rimasti indietro, ripresa, risposte fuori forma; una scheda o un
   giudizio mancati, o arrivati fuori forma, e poi ripresi danno gli stessi fatti di una corsa pulita.
2. **La replica:** `staging_B_raggruppamento`, avviato solo a mano, rilegge nell'ordine di lettura i file
   `notizie_righe_` dal 10 novembre fino a un ultimo file fissato prima di partire, su tabelle vuote.
   Il rapporto: schede, fatti, dubbi (quanti di un fatto ufficiale, quanti di un aggiornamento e
   quanti per una lista tagliata),
   fusioni fatte su una via, candidati trovati solo per luogo o solo perché già nella tabella (e
   quanti finiti in dubbio), schede a cui il tetto di 10 ha tolto candidati, righe della tabella
   lette da un passaggio e il suo tempo, l'aggiornamento più lontano agganciato, categorie di
   `news-fact.js`, chiamate e spesa. La replica ha pochi giorni di dati: un aggiornamento o un
   comunicato arrivati dopo mesi li provano solo i test del punto 1.
3. **La stessa replica un'altra volta,** sulle stesse tabelle: nessuna chiamata, gli stessi fatti.
4. **La ripresa:** svuotata solo `staging_B_fatti`, una replica interrotta a metà e ripresa, con le
   risposte salvate: nessuna chiamata, gli stessi fatti della 2.
5. **La misura,** da un revisore che non ha costruito il flusso (un subagent con il rapporto e gli
   originali su Drive): ogni fusione automatica, ogni dubbio, e 50 coppie dello stesso tipo, nella
   finestra, non fuse. Nel passaggio solo i numeri.

Spesa massima dichiarata: 1 €; la replica si ferma se la supera. L'esito proposto (scelta 2): almeno
il 95% delle fusioni automatiche giuste; nessuna fusione sbagliata che renda pubblicabile un fatto o
gli dia una fonte che non ne ha scritto; dubbi sotto il 10% delle schede di cronaca. Se le fusioni
sbagliano, la regola si stringe; non si allarga.

Che cosa mostrerà comunque: pochi fatti di stampa arrivano a due editori, perché a giugno la seconda
fonte era quasi sempre una testata chiusa (`CRONACA_PROCESSO_2026-10.md`, sezione 4.6).

## 9. Ordine di costruzione

| PR | Che cosa | Modello |
|---|---|---|
| B-R1 | `code-nodes/news-group.js` con `tests/test_news_group.js`: i passi 1, 3 e 5 e il controllo delle risposte | no |
| contratti | del coordinatore: le righe di CONTRATTI che B-R2 usa (sezione 11). Viene prima di B-R2 | |
| B-R2 | i due prompt, il flusso della prova (esportato in `workflows/`), le Data table; la prova della sezione 8; l'avvio in esercizio (sezione 6) solo dopo la prova | sì, in staging |
| dopo | i dubbi nella coda (scelta 3), poi geografia, filtro, scrittura e verifica | |

## 10. Le scelte dell'owner

1. **Leggere la pagina di ogni record nuovo** della Questura, dei Carabinieri e di Abitare a Roma:
   circa 30 richieste al giorno, con le regole della raccolta. Senza, un riepilogo della Questura si
   legge dal solo titolo, senza data e senza dividerlo nei suoi fatti (R-C01); una sua scheda non è
   quasi mai certa, e il fatto ufficiale resta in dubbio (con la 3(b), non si pubblica) se il modello
   la trova simile a un fatto della stampa o se la lista dei suoi candidati è tagliata, cioè quasi
   sempre (sezione 5, «Dubbio»). Il builder consiglia sì.
2. **Quando due notizie si fondono da sole.** La prova di giugno aveva due regole «certa»: due
   dettagli concordi fra comunicati e testate (`ISTRUZIONI_AVANTI.md`), uno solo per i titoli delle
   testate chiuse (`ISTRUZIONI_CHIUSE.md`), con circa un abbinamento debole su dieci (`CRONACA_PROCESSO`,
   sezione 4.6). Più fusioni automatiche vogliono una decisione dell'owner, come per gli eventi
   (DEC-025, regola 4). Il builder consiglia due dettagli, con le soglie della sezione 8, e di
   rivederla dopo la prova.
3. **Che cosa diventa un dubbio quando si pubblicherà:** (a) una riga nella coda, con due decisioni
   nuove («stesso fatto di …», «fatto diverso») e un ritmo quotidiano per le notizie, che la coda oggi
   non ha (DEC-034, «Blocks»; `docs/REVIEW_QUEUE.md`); oppure (b) un fatto in dubbio, anche ufficiale, non si
   pubblica e compare in un elenco del giorno, e nessuno lo scioglie: anche un aggiornamento finito in
   dubbio resta staccato dal suo fatto (sezione 5). Per la prova non serve. Il builder consiglia (b)
   per il pilota privato e (a) prima del lancio.
4. **Quale indice delle testate chiuse, e a che costo.** DEC-108 le ammette come solo titolo, link e
   ora presi da un indice terzo, e le conta come secondo editore; quale indice e con quale spesa è
   ancora da decidere (`CRONACA_PROCESSO_2026-10.md`, sezione 7, punto 4). Senza, saranno pubblicabili
   quasi solo i fatti ufficiali. Il builder consiglia di aprirlo dopo la prova, con una PR sua.
5. **Le notizie che non sono cronaca,** circa due terzi dei record delle testate: il blocco Notizie del
   pilota le porta? DEC-034 e DEC-108 parlano di cronaca; per le altre servono temi e una regola di
   pubblicazione. Il builder consiglia di tenerle ferme fino al primo mese di cronaca.

## 11. Che cosa chiede ai contratti

Questo documento non cambia CONTRATTI. Le righe che servono le propone al coordinatore il passaggio
della sessione (`PASSAGGIO_2026-11-15_B-raggruppamento.md`, nella cartella di passaggio): il
raggruppamento in 7 B; la lettura delle pagine, se l'owner la sceglie; le Data table di B e `prove/`
nella sezione 3; i file di spesa di B; i segnali presi dagli eventi; `source_channel` e `source_id`
nei record.

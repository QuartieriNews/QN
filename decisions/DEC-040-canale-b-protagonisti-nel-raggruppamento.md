# DEC-040 — Canale B: i protagonisti nel raggruppamento delle notizie

Status: DECIDED (16 novembre 2026, owner nella sessione del coordinatore, sul consiglio del builder)
Supersedes in part: DEC-039, punto 2, nel solo caso in cui fanno nomi sia la scheda in arrivo sia
una scheda del fatto: lì le prove del punto 2 non bastano più per la fusione automatica. DEC-039
resta invariata e non si riapre; riceve un rimando sotto la riga `Status:` (`decisions/README.md`,
regola 2). Per tutto il resto DEC-039 resta in vigore.
Blocks: niente. Chiude la domanda che teneva aperto un rilievo P1 di Codex sulla PR #57 (il
progetto del raggruppamento).

Question: le schede del raggruppamento non hanno nomi di persona
(`docs/pilota/B_RAGGRUPPAMENTO.md`, sezione 3). Due fatti diversi con lo stesso tipo, luogo,
giorno e gli stessi dettagli si fondono allora da soli, anche quando gli articoli nominano
persone diverse. Come entra il confronto delle persone nel raggruppamento, senza tenere i nomi
dove non devono stare?

Contesto:
- R-C01 definisce il fatto con luogo, data e protagonisti (DEC-034, punto 1). Il progetto
  confronta tipo, luogo, date e dettagli; i nomi sono dei passi dopo (DEC-108, punto 2;
  DEC-034, punto 5).
- Fondere due fatti diversi è l'errore grave del raggruppamento (progetto, sezione 1): può far
  sembrare riportato da due editori un fatto che ogni testata ha raccontato per conto suo, e
  renderlo pubblicabile (DEC-108, punto 1).
- I comunicati della Questura e dei Carabinieri di norma non nominano nessuno. Le testate
  nominano soprattutto le vittime e i casi noti. Quanto spesso, non è misurato.
- Il modello legge già, di ogni record, il testo che la raccolta ha (progetto, sezione 2), per
  farne le schede. La domanda è che cosa si salva e che cosa si confronta, non che cosa legge il
  fornitore.

Options:
1. **Un'impronta al posto del nome.** Il codice salva, per ogni nome, un codice che non si può
   rileggere, e confronta i codici. Resta un dato personale nelle tabelle di staging, forse da
   portare al parere legale; e riesce male, perché le testate scrivono lo stesso nome in modi
   diversi.
2. **Solo il segnale «fa nomi».** La scheda dice se l'articolo fa nomi, un sì o un no. Se lo
   dicono tutti e due gli articoli, il sistema non li unisce da solo: vanno fra i dubbi. Nessun
   dato personale, regola semplice. Il prezzo: un fatto in cui due testate nominano la stessa
   persona resta fermo, e nel pilota nessun nome letto sulla stampa arriva alla pubblicazione.
3. **Il confronto lo fa il modello sui due testi.** Al momento di unirli una chiamata in più dice
   solo se i due testi nominano persone diverse, e nessun nome si salva. Riconosce la stessa
   persona scritta in due modi. Costa una chiamata per ogni fusione, è più lavoro, e il codice
   non può verificare la risposta.
4. **Non cambiare,** e vedere nella prova in staging se succede. Un caso raro può non capitare
   nei giorni della prova, e il rilievo di Codex resta aperto.

Claude recommendation: la 2 per il pilota privato. Si parte prudenti e si misura. Se quei dubbi
risultano troppi, o se l'owner vuole provare già nel pilota la pubblicazione dei nomi, si passa
alla 3.

Codex recommendation (PR #57, rilievo P1 sulla sezione 3 del progetto): tenere per i protagonisti
nominati un segnale di confronto che non si pubblica, oppure mandare questi casi in dubbio.

Owner's words, 16 novembre 2026, nella sessione del coordinatore: «1 B, 2 la 2, 3 A, 4 B», a
quattro domande numerate. «2 la 2» risponde alla seconda, «come teniamo conto delle persone senza
conservare i nomi?», con le quattro opzioni qui sopra.

## Regola

1. **Ogni scheda dice se fa nomi:** un sì o un no, e nient'altro. Nelle schede non entra nessun
   nome, nessuna iniziale e nessuna impronta di un nome.
2. **Se lo dicono tutte e due, niente fusione automatica:** la scheda in arrivo non si aggiunge
   da sola al fatto e va in dubbio (progetto, sezione 5). Nel pilota privato un fatto in dubbio
   non si pubblica (DEC-039, punto 3).
3. **La prova in staging conta questi dubbi a parte,** e la regola si rivede dopo la prova. Il
   passo dopo, se i dubbi sono troppi o se l'owner vuole provare nel pilota i nomi di DEC-108,
   punto 2, è l'opzione 3. Sceglierlo resta una decisione dell'owner, come ogni allargamento
   della fusione automatica (DEC-039, punto 2).

Letture del builder, che l'owner conferma con il merge di questa entry:
- «Fa nomi» si legge scheda per scheda: il record indica per nome almeno una persona coinvolta
  nel fatto di quella scheda, cioè un protagonista di R-C01. In un record con più fatti ogni
  scheda risponde per il suo. Vale come nome anche il solo cognome o le sole iniziali: anche
  così due articoli possono indicare persone diverse, ed è la lettura che stringe. Con questa
  lettura il prezzo cresce: resta fermo anche un fatto in cui due testate danno le iniziali
  della stessa persona. Non conta chi il fatto lo comunica o lo commenta.
- Il sì o il no lo dà il modello quando fa le schede, e il codice ne controlla solo la forma
  (progetto, sezione 4). Dove passa il confine lo dicono il progetto e il prompt delle schede,
  con esempi inventati; se il modello lo rispetta lo misura la prova. Lo stesso vale per un
  nome nel testo libero della scheda (`sintesi`): lo vieta il prompt, il codice non lo riconosce.
- Il segnale vale sul testo che il modello legge del record, non sull'articolo intero. Oggi è
  l'articolo intero solo per Il Faro Online; per Abitare a Roma sono il titolo e una descrizione
  di circa 150 caratteri, finché le pagine non si leggono (progetto, sezione 2; DEC-039,
  punto 1). Un nome che sta solo nel resto dell'articolo non si vede, e la regola non scatta.
  La replica della prova rilegge record senza pagina: nel suo conto mancano i nomi che stanno
  solo nelle pagine.
- «Tutti e due» si legge: la scheda in arrivo e almeno una scheda già nel fatto. Con un fatto
  che ha più schede basta che una di loro faccia nomi, anche se non è quella che il modello cita.
- Il segnale non dice se i nomi sono gli stessi. Quando solo una delle due parti fa nomi, o
  nessuna, la regola non entra nel giudizio di quella scheda, e la fusione segue DEC-039,
  punto 2.
- La regola vale per ogni scheda in arrivo, di qualunque fonte: la domanda parlava di due
  articoli e, nel prezzo, di due testate. Prende anche tre casi che la domanda non diceva. Un
  aggiornamento che fa nomi (convalida, scarcerazione, sentenza) non si aggancia da solo a un
  fatto in cui una scheda fa nomi: resta in dubbio e staccato dal suo fatto, e nel pilota quello
  sviluppo, anche se favorevole all'interessato, non arriva al fatto come R-C04 chiede (DEC-039,
  punto 3). Un secondo articolo della stessa testata che fa nomi va in dubbio come quello di
  un'altra. Un comunicato che fa nomi, arrivato dopo un articolo che ne fa, va in dubbio e non
  si pubblica, anche se è ufficiale. Farli passare da soli è un allargamento: resta una
  decisione dell'owner (DEC-039, punto 2).
- Che cosa segue da un dubbio di questa regola lo dice il progetto (sezione 5): in dubbio va la
  scheda in arrivo, che apre un fatto suo, e il fatto già aperto va avanti. Com'è oggi la
  sezione 5, una scheda arrivata dopo che il modello giudica `stesso` per tutti e due i fatti è
  un ponte e va in dubbio anche lei, che faccia nomi o no: così un comunicato arrivato dopo due
  articoli che fanno nomi non si pubblica. È un prezzo in più, che la domanda non diceva; se e
  come ridurlo lo dice la revisione del progetto.
- «A parte», nel punto 3, è una lettura del builder di «si misura»: un conto in più nel
  rapporto della prova. Questi dubbi contano anche nella terza condizione di DEC-039, punto 2
  (i dubbi sotto il 10% delle schede di cronaca), che questa entry non cambia. «Troppi» non ha
  una soglia: lo dice l'owner sui numeri della prova.
- Questa entry supera DEC-039 solo nel punto 2 e solo quando fanno nomi la scheda in arrivo e
  una scheda del fatto, nel verso che stringe: il resto di DEC-039 vale com'è.

Impact:
- `docs/pilota/B_RAGGRUPPAMENTO.md`: un campo in più nella scheda (sezione 3), una condizione in
  «Certa» (sezione 5), un tipo di dubbio in più nel rapporto della prova (sezione 8). Li porta
  la revisione del progetto del workstream B, sulla PR #57.
- Codice: `code-nodes/news-group.js` e `tests/test_news_group.js`, che arrivano con la PR B-R1;
  il prompt delle schede, che arriva con la PR B-R2.
- `docs/pilota/CONTRATTI.md`, sezione 7 B, «Raggruppamento»: il rimando a questa entry.
- DEC-039 riceve il rimando sotto la riga `Status:`. DEC-108 e DEC-034 restano invariate. Con
  questa entry non cambiano gazetteer, prompt esistenti, n8n di produzione, lane gate o CI.

Decided by: owner · Date: 16 novembre 2026 · Affected components: canale B del pilota,
`docs/pilota/B_RAGGRUPPAMENTO.md`, `code-nodes/news-group.js`, `docs/pilota/CONTRATTI.md`
(sezione 7 B), DEC-039.

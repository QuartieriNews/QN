# DEC-043 — Canale B: come si fissa la regola del raggruppamento

Status: DECIDED (16 novembre 2026, owner nella sessione del workstream B; registrata dal
coordinatore il 18 novembre 2026)
Non sostituisce nessuna entry. Si affianca a DEC-039, punto 2, e a DEC-040, che restano come sono.
Blocks: niente. La prova in staging del raggruppamento (`docs/pilota/B_RAGGRUPPAMENTO.md`,
sezione 8) la applica; il flusso e i prompt arrivano con B-R2.

Question: la regola che dice quando due notizie si fondono da sole si costruisce prima nei
dettagli, cercando i casi difficili a tavolino, oppure si parte da una regola semplice e la si
misura sui casi veri della prova?

Contesto:
- Il raggruppamento può sbagliare in due modi (progetto, sezione 1, e sezione 10,
  scelta 7). Una regola troppo stretta non
  riconosce la stessa notizia scritta da due testate: il fatto di stampa resta con un editore solo
  e non si pubblica (DEC-108, punto 1). Una regola troppo larga fonde notizie diverse: è l'errore
  grave, perché si vede e toglie serietà al progetto.
- La regola d'esercizio è quella della sezione 5 del progetto, con i due dettagli concordi della
  scelta 2 (DEC-039, punto 2) e il segnale dei nomi (DEC-040). Durante la revisione del progetto
  sulla PR #57 si cercavano altri modi di stringere o di allargare i candidati, e ognuno chiedeva
  una scelta dell'owner (DEC-039, punto 2: allargare è dell'owner).
- Il 16 novembre la scelta dell'owner è arrivata a fine sessione (passaggio del builder, «In una
  riga»). Il testo della domanda e delle opzioni non è nei passaggi su Drive: le opzioni qui sotto
  sono la ricostruzione del coordinatore dal progetto (sezione 10, scelta 7) e dal passaggio del
  builder (`PASSAGGIO_2026-11-16_B-revisione-unica-consegna.md`, sezione 6, punto 4).

Options (ricostruite, vedi sopra):
1. **Prima la regola completa:** studiare e scrivere prima della prova i casi difficili, con una
   regola più complicata.
2. **CHOSEN. Prima il buon senso, poi i numeri:** partire dalla regola della sezione 5, farla
   girare nella prova accanto a una regola opposta, molto larga, e decidere dopo sui casi veri.

Claude recommendation: nessuna fra opzioni scritte. Le parole dell'owner («vai avanti con la tua
intuizione migliore») rispondono al builder di B; che cosa avesse proposto, i passaggi non lo
dicono. La regola di confronto larga viene dalle parole dell'owner.

Owner's words, 16 novembre 2026, nella sessione del workstream B, copiate dal builder nel suo
passaggio (sezione 6, punto 4; i tagli […] sono del builder): «io suggerisco di fare una scelta di
buon senso, e poi verificare ai fatti il peso della scelta […] vai avanti con la tua intuizione
migliore e poi verifichiamo dopo con casi concreti cosa succede […] usiamo un metodo piu probabile
e teniamo un metodo contrario per vedere i risultati nell altro estremo e capiremo effettivamente
gli effetti di ogni scelta».

## Regola

1. **Si parte con la regola di buon senso:** la regola d'esercizio è quella della sezione 5 del
   progetto (DEC-039, punto 2; DEC-040). Prima della prova non si costruisce una regola più
   complicata.
2. **Nella prova gira accanto una regola di confronto, all'altro estremo:** la stessa replica, sugli
   stessi record, rifà i fatti con una regola larga, per cui basta il luogo di quartiere e nessun
   dettaglio (progetto, sezione 8, punto 2). I suoi fatti stanno a parte e non sono mai
   pubblicabili. Come riusa le schede e i giudizi, e la spesa, li dice il progetto (sezioni 7 e 8).
3. **La misura conta che cosa cambia fra le due:** per ogni fusione fatta solo dalla regola larga,
   se è la stessa notizia che la regola d'esercizio perde o due notizie diverse fuse; e quali fatti
   diventano pubblicabili con una sola delle due (progetto, sezione 8, punto 5).
4. **Dopo la prova l'owner sceglie sui numeri:** tenere la regola, allargarla o stringerla. La
   scelta sta dentro DEC-039, punto 2, che resta com'è: le tre condizioni della prova, se le
   fusioni sbagliano la regola si stringe, e allargarla è dell'owner.

Letture del builder di B, dal suo passaggio (sezione 6, punto 4), che l'owner conferma con il
merge di questa entry:
- «L'altro estremo» è letto come il quartiere senza dettagli: più largo di così
  (solo il tipo e le date) unirebbe fatti di quartieri diversi, e non direbbe niente di utile.
- La regola di confronto tiene i nomi (DEC-040), il ponte e la lista tagliata, e sceglie i
  candidati come quella d'esercizio: cambia solo quando una scheda è certa.
- Un'osservazione dell'owner va corretta: «per uscire, la notizia deve esser associata almeno a
  due fonti». Vale per la stampa; un fatto ufficiale esce con una fonte sola (DEC-108).
  Così la regola stretta fa perdere soprattutto i fatti di stampa che avrebbero raggiunto due
  testate.
- Per B-R2: ogni tabella dei fatti va legata alla sua regola, perché il nodo rifiuta le righe
  dell'altra ma su una tabella vuota non può saperlo; e il prompt dei giudizi deve lasciar citare
  un luogo di livello `quartiere`, o la regola larga non fonde niente in più.

Letture del coordinatore, che l'owner conferma con il merge di questa entry:
- «Un metodo più probabile» è la regola d'esercizio, e «un metodo contrario» è la regola larga
  della sezione 8, come le ha scritte il builder di B nel progetto.
- Le tre condizioni di DEC-039, punto 2, valgono per la regola d'esercizio: i numeri della regola
  di confronto servono a vedere che cosa cambierebbe, non a dire se la prova è andata bene.
- La regola di confronto vale solo nella prova: non entra in esercizio e non scrive niente di
  pubblicabile, nemmeno in staging (CONTRATTI, sezione 7 B, «Raggruppamento»).
- Un limite che la prova ha, e che le parole non dicevano: le due regole scelgono i dieci
  candidati allo stesso modo, così oltre i dieci la regola larga risulta un po' meno larga di
  quanto è (progetto, sezione 8, punto 5).

Impact:
- `docs/pilota/B_RAGGRUPPAMENTO.md`: la riga «Stato» nomina le scelte del 16 novembre e le loro
  entry; la sezione 10 rimanda a questa entry per la scelta 7; la sezione 8, punto 2, la cita
  accanto alla «settima scelta», e la fine della sezione 8 la nomina per che cosa succede alla
  regola dopo la prova.
- `docs/pilota/CONTRATTI.md`, sezione 7 B, «Raggruppamento»: il rimando a questa entry accanto a
  DEC-039 e DEC-040. La tabella `staging_B_fatti_confronto` c'è già (sezione 3 e sezione 7 B).
- Codice: nessun cambio. `code-nodes/news-group.js` ha già le due regole (`REGOLE`) e dice che un
  fatto della regola di confronto non è mai pubblicabile, con i test T-B-R1-13 e T-B-R1-21; il
  flusso della prova e i prompt arrivano con B-R2.
- DEC-039, DEC-040, DEC-108 e DEC-034 restano invariate. Nessun cambio a gazetteer, prompt, n8n di
  produzione, lane gate o CI.

Decided by: owner · Date: 16 novembre 2026 · Affected components: canale B del pilota,
`docs/pilota/B_RAGGRUPPAMENTO.md` (sezioni 8 e 10), `docs/pilota/CONTRATTI.md` (sezione 7 B),
`code-nodes/news-group.js` (`REGOLE`, `groupingAllows`, senza cambi).

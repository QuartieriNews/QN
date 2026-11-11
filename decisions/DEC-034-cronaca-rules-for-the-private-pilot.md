# DEC-034 — Le regole della cronaca per il pilota privato (canale B)

Status: DECIDED (11 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: la pubblicazione dei casi che R-C05 manda in coda manuale, finché `docs/REVIEW_QUEUE.md`
non dà alle notizie una priorità o un tempo («What changes when the other blocks arrive»):
R-C08 chiede di pubblicare entro 48 ore, e la coda oggi si rivede una volta alla settimana.

Context:
- Il contratto del pilota ha già una regola sull'unità: lo stesso fatto raccontato da più
  testate resta un fatto solo, e il `content_id` identifica l'elemento pubblicato, non il
  record della fonte (CONTRATTI, sezione 2). DEC-108 fissa quando la stampa entra e il
  secondo editore.
- Le altre regole della cronaca stanno in `docs/sources/CRONACA_PROCESSO_2026-10.md`,
  sezione 3, R-C01…R-C11, come proposte del builder: «Diventano regole quando l'owner le
  adotta», e quelle segnate ⚖ solo dopo il parere legale. Il canale B ne ha bisogno
  prima di scrivere elementi. Le prime due servono già alla sua forma:
  - un comunicato di riepilogo dà più fatti (R-C01);
  - quale fonte è il capofila del fatto (R-C02).
- La PR del canale B (#36) segna il capofila come da decidere, e intanto il canale
  raccoglie solo gli originali.

Question: quali regole R-C valgono per il pilota privato, prima del parere legale?

Options:
A. Adottare come regole di lavoro del pilota privato R-C01, R-C02, R-C04–R-C08 e R-C10;
   R-C09 dopo il primo mese di dati; R-C03 e le altre regole segnate ⚖ restano fuori
   finché il legale non si è espresso. Il capofila di un fatto è la fonte ufficiale, se
   c'è; altrimenti la prima testata aperta.
B. Adottare solo R-C01 e R-C02, e decidere le altre una alla volta, quando il canale
   arriva ai passi che le usano (scrittura, nomi, coda).
C. Nessuna regola nuova: il canale B resta alla raccolta degli originali fino al parere
   legale.

Claude recommendation: A. Il sito è privato, e le regole proposte sono quelle che lo
studio di ottobre ha già messo alla prova sui dati di giugno. B rallenta senza ridurre il
rischio, perché le regole si usano tutte nella stessa corsa. C ferma B per una scelta che
riguarda il lancio pubblico, non il pilota.

Impact:
- `docs/pilota/CONTRATTI.md`, sezione 7, «B · Notizie»: il capofila e la divisione dei
  riepiloghi diventano regole del canale.
- I passi del canale che scrivono elementi (geografia, filtro, scrittura, verifica)
  partono dalle PR successive.

Owner's answer (sessione del builder, 11 novembre 2026): «Quasi tutte», l'opzione A, dopo
che il builder ha spiegato ogni regola a parole e la ha messa a confronto con le decisioni
già prese (DEC-016, DEC-020, DEC-108).

Decision (opzione A, con due chiarimenti del builder accettati dall'owner nella stessa
domanda):
1. **Regole di lavoro del pilota privato da subito:** R-C01, R-C02, R-C04, R-C05, R-C06,
   R-C07, R-C08 e R-C10. Un comunicato di riepilogo dà un elemento per fatto (R-C01). Il
   capofila di un fatto è la fonte ufficiale, se c'è; altrimenti la prima testata aperta
   che lo riporta (R-C02). Di R-C10 vale la parte decisa: nessuna foto di persone né foto
   prese dalle testate. La scelta fra un'immagine generata (la mappa del luogo) e nessuna
   immagine resta aperta (baseline §2.D, come dice R-C10): finché non è decisa, il canale non
   mette immagini.
2. **R-C09** dopo il primo mese di dati, con N fissato dall'owner.
3. **Al parere legale:** di R-C03 solo l'uso di titoli ed estratti delle testate (scrivere
   con parole proprie, citando e linkando le testate, è già DEC-108); di R-C11 la procedura
   per le richieste di deindicizzazione (le correzioni sono già DEC-020).
4. **Primo chiarimento.** Il testo dell'opzione A diceva che le regole segnate ⚖ restano
   fuori, ma ne includeva due (R-C04 e R-C05). Vale questo: R-C04 e R-C05 entrano subito,
   perché aggiungono solo prudenza; il parere legale potrà renderle più strette.
5. **Secondo chiarimento.** R-C05 vale dentro DEC-108, in due punti:
   - per i nomi letti sulla stampa vale DEC-108, punto 2 (due editori diversi, adulto
     arrestato o indagato, presunzione di innocenza, verifica della seconda AI,
     attribuzione), non «mai in automatico»;
   - le identità che DEC-108 toglie sempre (minori coinvolti in un procedimento penale o
     come vittime o testimoni, vittime di violenza sessuale) le toglie la pipeline, senza
     coda, come dice DEC-108. Tutti gli altri casi di R-C05 e di DEC-016, che DEC-108 lascia
     invariata per le fonti ufficiali, restano in coda manuale: i minori negli altri casi, le
     vittime adulte, i testimoni, i familiari, le persone coinvolte in suicidi o tentati
     suicidi, i dati sanitari e gli altri dati sensibili.

Decided by: Owner · Date: 11 novembre 2026 · Affected components: canale B del pilota, `docs/pilota/CONTRATTI.md`,
`docs/REVIEW_QUEUE.md` (la priorità delle notizie, Blocks).

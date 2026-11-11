# DEC-034 — Le regole della cronaca per il pilota privato (canale B)

Status: OPEN (10 novembre 2026, bozza del builder)
Blocks: il canale B «Notizie» che scrive elementi (`docs/pilota/CONTRATTI.md`, sezione 7). La
raccolta degli originali nello staging non dipende da questa decisione.

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

Decided by: — · Date: — · Affected components: canale B del pilota, `docs/pilota/CONTRATTI.md`.

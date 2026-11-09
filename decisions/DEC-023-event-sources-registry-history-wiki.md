# DEC-023 — Le fonti degli eventi: registro, storico e wiki generata

Status: DECIDED (8 novembre 2026, owner nella sessione del builder, dopo il Consiglio Strategico del 7 novembre)
Integra: DEC-022, senza cambiarla. La wiki di giugno resta com'è (`docs/wiki/`); questa
entrata decide come si chiude la fase fonti e dove sta ciascuna parte del suo risultato.
Blocks: nothing.

Question: perché il progetto funzioni al meglio, la fase fonti deve concludersi con una wiki
esaustiva divisa in due parti, il «Dove» (le informazioni su dove cercare) e lo storico (le
informazioni già raccolte)? È l'approccio migliore, ci sono modalità migliori?

Contesto:
- La PR #21 (bozza) porta la wiki delle fonti degli eventi di ottobre 2026: uno schedario di
  5.238 fonti, 1.246 promotori e circa 400 fusioni proposte, pagine generate, circa 383.000
  righe in tutto. Ci sono anche i lettori, il validatore e il generatore. Una prima bozza di
  questa entrata chiedeva soltanto se quella wiki fosse un ramo della wiki di contesto.
- Gli ingressi del generatore non sono su Drive. Il registro fonti v5/v6 del 25–26 ottobre
  esisteva solo nelle sessioni del builder ed è andato perso. Lo schedario della #21 ne
  conserva 1.745 voci (chiave, decisione, canale, tipo, zona, municipio) e, per tutte le
  fonti, canali e «dove cercare». Le note libere dell'owner non ci sono.
- Consiglio Strategico del 7 novembre (livello 2, tre passaggi): convergenza debole, stessa
  raccomandazione da entrambi i membri, Operator REVISE e stratega MAINTAIN. L'esaustività
  misura quante fonti sono catalogate, non quanto servono: solo 19 pagine Facebook di
  associazioni su 1.169 pubblicano eventi futuri su Facebook.

Options:
A. **CHOSEN, con le precisazioni dell'owner.** Al posto di una wiki esaustiva, tre componenti
   distinte: registro canonico del «Dove», storico privato, wiki come vista generata.
B. La wiki in due parti, tutta nel repository, come nella #21.
C. Tutto su Drive, e nel repository solo il codice.

Owner's words, 8 novembre 2026: «sono d accordo con le tre componenti. D accordo ad arrivare
ad una copertura minima, passare alla fase successiva mentre il sistema continua ad
accumulare dati per non perdere tempo prezioso e chiudere i due cicli. Lasciare il grosso su
Drive per non appesantire Github.» Sulla soglia di copertura, 9 novembre: «non avendo nessuna
pagina live non me ne preoccuperei piu di tanto, sappiamo che nei quartieri dove non c'è
materiale sufficiente, io allarghero i blocchi con altri quartieri limitrofi.»

## Regola

1. **Il registro del «Dove»** dice chi produce informazioni e dove guardare. Ha una sola fonte
   di verità, un foglio Google su Drive. La wiki ne è una vista. Stato, data dell'ultimo
   controllo e priorità valgono solo per le fonti attive.
2. **Lo storico** è l'archivio di quanto raccolto: privato, su Drive, in sola aggiunta.
   Lo schema minimo vale da subito: id stabile, fonte, data, municipio, tipo, URL e
   provenienza; dato originale, dato derivato ed etichetta nostra restano distinti; ci sono
   una regola di correzione e una copia di riserva.
3. **Il grosso sta su Drive:** schedario, pagine generate, storico, script di lavoro e
   documenti lunghi. Nel repository vanno codice e test (con esempi inventati), le decisioni
   e una sintesi del processo con i numeri.
4. **La fase fonti non si chiude per esaustività.** Si passa subito alla fase successiva,
   mentre lo storico accumula dati. Due cicli di raccolta misurano copertura e resa delle
   fonti, ma non bloccano niente. Dove un quartiere ha poco materiale, la sua pagina allarga
   i blocchi ai quartieri vicini, per scelta dell'owner.

Impact:
- PR #21: la wiki generata, lo schedario e gli script di lavoro vanno su Drive. Lettori,
  validatore e generatore arrivano in PR piccole. DEC-024, DEC-025 e DEC-026 restano da
  decidere.
- Drive: il registro si ricostruisce dalla #21 come foglio Google; lo storico ha la sua cartella.
- Nessun cambiamento a pipeline, gazetteer, prompt o n8n.

Decided by: owner · Date: 8 novembre 2026 · Affected components: `docs/wiki/fonti-eventi/`
(PR #21), `tools/wiki/build_fonti_eventi.py`, `tools/fonti/`, registro fonti su Drive, DEC-022.

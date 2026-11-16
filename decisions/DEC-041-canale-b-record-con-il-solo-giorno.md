# DEC-041 — Canale B: il posto di un record con il solo giorno nell'ordine di pubblicazione

Status: DECIDED (16 novembre 2026, owner nella sessione del coordinatore, sul consiglio del builder)
Blocks: niente.

Question: nell'ordine di pubblicazione dei record di un fatto, dove sta un record di cui la
fonte dà il solo giorno, rispetto a quelli che hanno anche l'ora?

Contesto:
- `docs/pilota/CONTRATTI.md`, sezione 7 B, «Capofila», com'era prima di questa entry: i record
  di un fatto stavano «in ordine di pubblicazione: un record senza ora viene dopo gli altri, e a
  pari ora vale l'ordine di arrivo». La riga `source_hash` dice: «Se la fonte dà solo il giorno,
  l'ora è il giorno». La riga «Capofila» è stata scritta quando un record aveva un istante o
  niente.
- L'elenco della Questura dà per ogni voce il solo giorno; i Carabinieri e le testate danno
  anche l'ora. Oggi `code-nodes/news-parse.js` quel giorno non lo legge, e un record della
  Questura è senza data: lo leggerà una PR del workstream B.
- L'ordine sceglie la capofila fra due fonti ufficiali, la prima testata aperta di R-C02 se una
  testata desse il solo giorno, e l'ordine delle attribuzioni. Non cambia la categoria del
  fatto, né se è pubblicabile, né gli editori.

Options:
- A. Conta il giorno di Roma; nello stesso giorno, il record con il solo giorno viene dopo
  quelli che hanno l'ora.
- B. Il record con il solo giorno viene sempre dopo tutti quelli che hanno l'ora, di qualunque
  giorno.
- C. Conta il giorno di Roma; nello stesso giorno, il record con il solo giorno viene prima di
  quelli che hanno l'ora.

Claude recommendation: A, del builder del workstream B e del coordinatore. Fra giorni diversi
segue dalla riga `source_hash` (il giorno è l'ora di quel record) e da «in ordine di
pubblicazione»; B metterebbe un comunicato di ieri dopo uno di oggi. Nello stesso giorno resta
da scegliere fra «dopo» (A, come «un record senza ora viene dopo gli altri») e «prima» (C, che
nessun file appoggia).

Owner's words, 16 novembre 2026, nella sessione del coordinatore: «1 B, 2 la 2, 3 A, 4 B», a
quattro domande numerate. «3 A» risponde alla terza, «dove va un comunicato che dice solo il
giorno?», con le tre opzioni qui sopra. Con la A l'owner ha visto due esempi: Questura del 13 e
Carabinieri del 14, prima la Questura; tutti e due del 14, prima i Carabinieri.

## Regola

Nell'ordine di pubblicazione dei record di un fatto:

1. i record si ordinano per giorno di Roma;
2. nello stesso giorno, quelli che hanno l'ora stanno in ordine di ora, e un record che ha il
   solo giorno viene dopo di loro;
3. un record senza data viene dopo tutti gli altri, come prima di questa entry;
4. a parità, cioè due record con la stessa ora, due con il solo stesso giorno o due senza data,
   vale l'ordine di arrivo, come prima di questa entry.

Letture del builder, che l'owner conferma con il merge di questa entry:
- La domanda parlava di un comunicato, fra due fonti ufficiali. I punti 1 e 2 valgono per ogni
  record, perché l'ordine di pubblicazione è uno solo: anche per una testata che desse il solo
  giorno, che nello stesso giorno verrebbe dopo le testate con l'ora, e allora non sarebbe lei
  la prima testata aperta di R-C02. Oggi nessuna testata dà il solo giorno.
- I punti 3 e 4 non erano nella domanda: sono la riga «Capofila» com'era, che la scelta non
  tocca.
- Il giorno di un record con l'ora è il giorno di Roma di quell'istante; il giorno di un record
  con il solo giorno è quello che la fonte scrive.

Impact:
- `docs/pilota/CONTRATTI.md`, sezione 7 B, «Capofila»: la frase sull'ordine.
- Codice: `code-nodes/news-fact.js`, che oggi accetta un istante o nessuna data (un record
  senza data va dopo gli altri) e ferma un fatto con un record che ha il giorno solo. Il giorno
  solo lo accetta e lo ordina la PR del workstream B su `news-parse.js`, con i test: finché non
  è unita, la regola non ha un caso a cui applicarsi.
- DEC-034 e DEC-108 restano invariate: la capofila è sempre quella di R-C02. Nessun cambiamento
  a gazetteer, prompt, n8n di produzione, lane gate o CI.

Decided by: owner · Date: 16 novembre 2026 · Affected components: canale B del pilota,
`docs/pilota/CONTRATTI.md` (sezione 7 B), `code-nodes/news-fact.js`, `code-nodes/news-parse.js`.

# Criterio per giudicare se due righe sono lo stesso fatto

Serve a chi audita la deduplicazione. Nasce corretto dopo un rilievo di chi l'ha applicato per primo.

## La regola

Due righe sono **lo stesso fatto** quando **nessuna delle due aggiunge qualcosa all'altra** che un
lettore chiamerebbe notizia.

La prima formulazione diceva «la seconda non aggiunge niente alla prima», ed era **asimmetrica
applicata a coppie che non hanno un ordine**: in un caso reale il parere di commissione del 15 giugno
non aggiungeva niente alla delibera del 16, ma la delibera aggiungeva molto al parere — e il giudizio
si rovesciava a seconda di quale riga si chiamasse «seconda». Il revisore ha dichiarato la
convenzione che aveva scelto invece di nasconderla, che è la ragione per cui il difetto si è visto.

Quindi: si guarda in **tutte e due le direzioni**. Se una delle due porta un fatto che l'altra non
ha — un esito di voto, una cifra, una data, un luogo — **non sono lo stesso fatto**, e la riga più
ricca non va persa.

## Quello che non basta

- **Lo stesso tema non basta.** «Il cantiere è fermo» e «il cantiere è stato avviato» hanno lo stesso
  tema e sono fatti opposti.
- **Lo stesso luogo non basta.** Un toponimo largo — un quartiere, un lungomare — mette insieme
  fatti che non c'entrano niente: è il meccanismo che genera più falsi accostamenti.
- **La stessa causa non basta.** Un nubifragio produce quattro avvisi di chiusura strada e una
  discussione sull'amianto: stessa causa, fatti diversi.
- **L'annuncio non è l'esito.** «Il Consiglio discuterà la mozione X» e «il Consiglio ha respinto la
  mozione X con quattro favorevoli» condividono quasi tutte le parole e non sono lo stesso fatto. È
  l'errore più frequente del nostro accostamento automatico: nove su dodici.

## Come si guarda

**Aprendo il documento, non confrontando le sintesi.** Ogni atto produce **una sola riga**, la cui
sintesi racconta **un punto solo** dell'ordine del giorno: un fatto che nel verbale è il terzo punto
non compare in quella sintesi. Misurato: giudicare a occhio sulle sintesi dava una precisione del
31% dove la lettura dei testi integrali ne dava il 52%, e in tre dei sei gemelli veri di un altro
campione la sintesi parlava d'altro.

## Dove non si decide

Si scrive **incerto** e si dice che cosa manca. Un incerto onesto vale più di una scelta a caso, e i
casi incerti sono quelli da cui si impara dove la regola non arriva.

## Come si apre un documento

Non ricostruire la regola: `report2/testo_documento.py` restituisce il testo integrale di un
documento a partire dal suo `documento_id`, e dice da dove l'ha preso.

```python
import os; os.environ.setdefault('QN_NET', '<cartella dei dati>')
from testo_documento import testo
t, fonte = testo('A2_0333')      # oppure 'A3_028' per una registrazione
```

Copre 3.393 documenti su 3.394. L'unico scoperto è un comunicato dei Carabinieri, la cui fonte
rimanda alla pagina-vetrina invece che al testo: è un difetto dichiarato, non un buco del programma.

Due revisori hanno perso tempo a ricostruire questa regola da soli, ciascuno a modo suo. Il secondo
l'ha scritta bene e ora sta qui.

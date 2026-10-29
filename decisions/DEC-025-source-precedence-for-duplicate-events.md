# DEC-025 — Precedenza fra le fonti per lo stesso evento (doppioni)

Status: OPEN (OWNER_DECISION_REQUIRED)
Blocks: la riga principale nel foglio unificato degli eventi; la regola di
pubblicazione «un evento, una scheda» nel flusso continuo.

Context: il foglio unificato di ottobre 2026 (`eventi_unico.xlsx`, Drive) ha 1.957
righe da quattro aggregatori e 97 gruppi di doppioni (127 righe in eccesso) con criteri
stretti: titolo quasi identico e date compatibili, oppure titolo simile con stessa data e
luogo. Oggi i gruppi sono segnalati (`gruppo_doppione`, `doppione_di`), non risolti: non
esiste una regola che dica quale riga comanda quando lo stesso evento arriva da più fonti.

Question: quale fonte prevale per i campi dell'evento (titolo, date, luogo, link) quando
lo stesso evento compare in più fonti?
  Options:
  a) precedenza per vicinanza alla fonte primaria: lettura diretta alla fonte > sito
     dell'organizzatore linkato > culture.roma.it > Facebook > Roma Today; i campi
     mancanti nella riga che comanda si prendono dalla successiva (coordinate da Facebook,
     Municipio da culture.roma.it);
  b) precedenza per completezza: comanda la riga con più campi compilati, a parità l'ordine
     di a);
  c) nessuna precedenza: il foglio resta con i gruppi segnalati e la scelta è del redattore
     riga per riga.
  Claude recommendation: a). È la stessa scala della rintracciabilità già misurata
  (`rintracciabile_alla_fonte`) e rende la regola verificabile da un test; b) premia gli
  aggregatori più prolissi, non i più affidabili.

Impact: con a) 127 righe diventano secondarie e i conteggi per pagina QN (DEC-014:
almeno dieci eventi futuri per pagina) si calcolano sulle sole righe principali, quindi
scendono; oggi 23 pagine superano la soglia contando anche i doppioni.

Decided by: — · Date: — · Affected components: `eventi_unico.xlsx` (colonna
`riga_principale`), la scheda dei doppioni in `docs/wiki/fonti-eventi/aggregatori.md`,
il flusso continuo quando esisterà.

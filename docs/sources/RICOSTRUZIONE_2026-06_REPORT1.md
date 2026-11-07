# Ricostruzione di giugno 2026 — Report 1: le fonti testuali

Consegna del 17 settembre 2026 (nota di fattibilità §9.6). Perimetro: le fonti **testuali** di
giugno 2026 — avvisi e notizie dei quindici Municipi (A1), cronaca di Questura, Carabinieri,
Vigili del fuoco e Roma Capitale (C1, C2, C4, C5), agenda eventi di `culture.roma.it` (E2) e
agenda eventi di `comune.roma.it` (E3). Atti e video sono il Report 2.

Metodo: `SOURCE_STUDY_METHOD.md` §4. Schema del database: `RICOSTRUZIONE_2026-06_SCHEMA_DB.md`,
rivisto da Codex al controllo C1. Lettura: `tools/sources-study/report1/SPECIFICA_LETTURA.md`.
Controlli del revisore: C1 sullo schema, C2 su un campione del risultato, entrambi archiviati in
`reviews/` con la risposta a ogni rilievo. Dati per item su Drive, `QN Hub / 20 Packages /
Fonti 2026-06/` (DEC-102, DEC-104): nel repository stanno solo gli aggregati.

## 1. In breve

| Misura | Valore |
|---|---|
| Item censiti nel mese | 985 |
| Item con testo leggibile | 898 (91%) |
| Item letti | 985 (gli 87 senza testo sono stati letti e dichiarati vuoti) |
| Notizie candidate | 1.227 |
| **Resa netta dopo deduplicazione** | **882–1.158** (72%–94% delle candidate) |
| Municipi con almeno una notizia | 15 su 15 |
| Notizie con Municipio | 1.131 su 1.227 (92%) |
| Notizie con zona del gazetteer | 448, su 63 zone distinte |
| Notizie senza data del fatto | 151 (12%) |
| Vicende (due o più notizie sullo stesso fatto) | 218 |

La resa è un intervallo perché il metodo lo impone: i **dubbi** — stesso luogo e stessa data, ma
oggetto non accertato — sono contati come distinti nel minimo e come duplicati nel massimo.

## 2. Che cosa danno davvero queste fonti

**Annunci, non cronaca.** Delle 1.075 notizie con entrambe le date, **896 sono pubblicate prima
del fatto**, con una mediana di **sette giorni di anticipo**; 120 lo stesso giorno, solo 59 dopo.
Le fonti testuali di Roma Capitale non raccontano quello che è successo: annunciano quello che
succederà. Per un giornale di quartiere è un vantaggio (si può programmare) e un limite (nessuna
verifica di ciò che è poi accaduto davvero).

**Tre quarti sono eventi culturali.** Sulle notizie nette: 748 eventi, 226 avvisi, 60 convegni,
54 ordini del giorno, 46 altro, 8 arresti, 6 delibere, 3 sopralluoghi. L'attività amministrativa
deliberativa — delibere, mozioni, risoluzioni — è quasi assente dalle fonti testuali: sta negli
atti, che sono il Report 2.

**La copertura territoriale c'è, ma è sbilanciata.** Tutti e quindici i Municipi hanno notizie.

| Municipio | Notizie | | Municipio | Notizie |
|---|---|---|---|---|
| I | 158 | | IX | 46 |
| II | 141 | | X | 55 |
| III | 41 | | XI | 71 |
| IV | 54 | | XII | 47 |
| V | 89 | | XIII | 68 |
| VI | 83 | | XIV | 59 |
| VII | 97 | | XV | 56 |
| VIII | 63 | | non localizzate | 87 |

Il Municipio I ha quasi quattro volte le notizie del III. Lo squilibrio non è del nostro metodo:
è la concentrazione dell'offerta culturale nel centro, più la maggiore attività comunicativa di
alcuni Municipi.

**Filtro 8–28 giugno** (le tre settimane del Report 2, per data di pubblicazione): 834 notizie
nette, di cui A1 339, E2 381, E3 111, C5 3.

## 3. Quanto si sovrappongono le fonti

Misurato sull'intero mese, non stimato su un campione (§6).

| Coppia | Duplicati | Dubbi |
|---|---|---|
| A1 × A1 (fra Municipi diversi) | 35 | 65 |
| E2 × E2 (interna) | 22 | 175 |
| **E2 × E3** (le due agende eventi) | **8** | 23 |
| C5 × C5 | 3 | — |
| E3 × E3 | — | 12 |

**Il risultato più importante, e il più controintuitivo.** Chi ha letto E3 aveva l'impressione
che l'84% delle sue schede fosse già su E2, perché promosse dallo stesso circuito culturale —
Sovrintendenza, Zètema, Musei Civici, Teatro di Roma. La misura dice altro: **8 duplicati certi e
23 dubbi su 640 notizie**, al massimo il 5%. Le due agende attingono allo stesso mondo ma
elencano in larga parte eventi **diversi**.

Questo numero va però letto come un **limite inferiore**: due lettori diversi scrivono titoli
diversi per lo stesso evento, e la condizione sull'oggetto confronta titoli e toponimi
normalizzati. Un confronto più permissivo troverebbe altre coppie. La direzione della conclusione
regge — le due agende non sono l'una il doppione dell'altra — ma la cifra esatta no.

**La sovrapposizione fra Questura e Carabinieri non è misurabile** su questo corpus: le due fonti
non sono leggibili (§4). È la lacuna più seria del Report 1, perché la cronaca è il blocco dove
la duplicazione fra enti è attesa più alta.

**Un caso che vale una regola.** Lo stesso avviso sui servizi 0–3 anni è stato ripubblicato da
sei Municipi diversi. Il metodo lo tratta come **sei fatti distinti**, perché il luogo cambia, ed
è la risposta giusta per un giornale di quartiere: l'avviso del Municipio VII non è la notizia
del Municipio II. Una deduplicazione ingenua avrebbe cancellato cinque notizie vere.

## 4. Che cosa manca, e perché

**La cronaca è in gran parte inaccessibile.** Su 109 item censiti, 22 hanno testo.

| Fonte | Item | Esito |
|---|---|---|
| C1 Questura | 79 | 12 leggibili. 67 rispondono con la pagina "Accesso negato", servita con codice HTTP 200 |
| C2 Carabinieri | 20 | **0 leggibili**: l'URL del singolo comunicato rimanda alla pagina-vetrina "Comunicati Stampa" |
| C4 Vigili del fuoco | 8 | tutti leggibili |
| C5 Roma Capitale | 2 | tutti leggibili |

Il blocco è stato ritentato con una richiesta ogni 90 secondi, per verificare se il rifiuto
dipendesse dal nostro ritmo: cinque richieste, cinque rifiuti, e il processo si è fermato da sé.
**Non era il ritmo.** Nessun tentativo di aggiramento è stato fatto né va fatto: per lo studio
questa *è* la risposta sulla utilizzabilità di quelle fonti da parte di QN.

Gli inventari restano completi (URL, titolo, data, Municipio), quindi i **conteggi** del mese
reggono per tutte e quattro le fonti di cronaca; manca il **testo**, e con esso le notizie
candidate e la misura di sovrapposizione.

**Non tentato**: E1 (il formato dei filtri non è stato trovato nel tempo previsto dal piano).

## 5. Difetti delle fonti, che una pipeline automatica deve aspettarsi

Trovati leggendo, non ipotizzati.

- **La data di pubblicazione non è stabile.** Confermato su due fonti indipendenti, A1 ed E3:
  pagine che risultano pubblicate a giugno ma sono state aggiornate a luglio o ad agosto, con
  contenuti che alla data dichiarata non esistevano; pagine con due date diverse al loro interno.
  Tocca in pieno la misura di tempestività: la colonna `disponibilita` dello schema esiste per
  questo.
- **Contraddizioni interne**, dichiarate e mai risolte d'ufficio: titolo e corpo con date diverse,
  un festival gratuito con biglietti a pagamento, sei cortometraggi annunciati e cinque elencati,
  un deposito attribuito a due aziende diverse, capienze in conflitto, la stessa sede scritta in
  quattro modi.
- **Caratteri corrotti nella fonte**, non nell'estrazione: verificato sui byte dell'HTML
  scaricato. Il portale sostituisce con `¿` le lettere accentate in certi contesti e **non
  rappresenta affatto gli alfabeti non latini** (una parola ebraica arriva come otto `¿`).
- **Pagine di prova pubblicate in produzione** (`test rox 1` sull'agenda eventi).
- **Refusi sistematici**: un centinaio annotati uno per uno, dai nomi di via alle cifre.
- **Il Municipio dichiarato dalla fonte non è il luogo della notizia.** Su A1 il tag di categoria
  del portale arriva a elencare tutti e quindici i Municipi su una singola pagina. Chi costruisce
  una pipeline su questo campo, senza leggere il testo, sbaglia la localizzazione.

## 6. Una nota sul metodo, per il prossimo studio

Il metodo (§4.1) prescrive, sopra i 300 item, un campione di almeno 60 item per coppia di fonti,
perché **assume che il confronto lo faccia una persona**. Il nostro confronto è deterministico e
costa nulla, quindi è stato eseguito sull'intero mese e la resa è *misurata*. Il campione
prescritto è stato calcolato lo stesso, sulle stesse righe, per non modificare in silenzio il
metodo.

I due numeri divergono in modo rilevante: sul campione di 60 notizie la duplicazione del blocco
Eventi risulterebbe intorno al 10% con 27 dubbi su 60, mentre sull'intero blocco i duplicati
certi sono pochissimi. **Un campione di 60 notizie non basta a stimare la resa netta di un blocco
su questo corpus.** Dove la deduplicazione è automatica, conviene misurarla tutta.

## 7. Incertezze dichiarate

- 151 notizie (12%) **senza data del fatto**: i testi dicono "nei giorni scorsi", "questa
  mattina", "prossimamente". Mai dedotta dalla data di pubblicazione.
- 442 notizie con **toponimo da verificare**: storpiature, doppie grafie della stessa sede,
  toponimi che il gazetteer non risolve, Municipio della fonte in contrasto con i luoghi del testo.
- 687 notizie **senza zona** del gazetteer: il testo nomina luoghi che il gazetteer non copre
  (soprattutto indirizzi civici e sedi private).
- 276 **dubbi** di deduplicazione, che è il motivo dell'intervallo di resa.
- Tre residui del controllo C2 non corretti e dichiarati nel rapporto del revisore: tre evidenze
  più corte della sintesi, un titolo d'opera anonimizzato per errore, una nota di lettura che dice
  "deduplicazione rinviata" quando ormai è stata fatta.

## 8. Decisioni editoriali applicate in attesa dell'owner

Registro completo con esempi in `tools/sources-study/session_b/DECISIONI_OWNER.md`. In sintesi,
DEC-102 protegge **le persone in quanto persone coinvolte nel fatto**; restano alla lettera i
toponimi e i nomi di sede, i titoli delle opere e i loro autori, le organizzazioni, e i nomi nelle
**intitolazioni e commemorazioni**, dove la persona è l'oggetto pubblico del fatto e toglierla
rende la notizia incomprensibile. Tutte reversibili senza rileggere nulla.

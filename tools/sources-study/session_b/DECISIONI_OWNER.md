# Decisioni editoriali da porre all'owner

Si accumulano qui man mano che emergono dalla lettura e partono **raggruppate**, un solo
messaggio per consegna (nota di fattibilità §9.6). Ognuna porta esempi reali e la **scelta di
default** che applico da sola se l'owner non risponde: il canale di notifica push verso di lui
non è recapitabile (`STATO.md` §6), quindi una decisione sospesa fermerebbe lo studio, e il
piano vieta che la sua assenza costi tempo.

Stato: `aperta` finché l'owner non risponde; `applicata` quando il default è già in esercizio.

---

## D1 — Nomi di persona dentro toponimi e titoli di opere (Report 1)

Stato: **aperta**, default già applicato.

**Il conflitto.** DEC-102 tiene i nomi di persona fuori dagli output, e la specifica di lettura
impone i toponimi *come compaiono nel testo*, perché è su quelli che lavora il gazetteer. A Roma
le due regole si scontrano di continuo: moltissime strade, sedi e sale portano il nome di una
persona.

**Esempi reali dal lotto E2 (50 schede di giugno):** `Teatro all'aperto Ettore Scola`,
`Largo Marcello Mastroianni` (17 occorrenze), `Via Bruno Cirino` (4), `Casa Moravia`,
`Girolamo Induno`, `Cardinal Bessarione`. Titoli di opere: `Blue Velvet`, `Easy Rider`,
`Frankenstein Junior`, `Emilia Pérez`, `Nuovo Cinema Paradiso`.

**Default applicato.** I nomi di persona *in quanto persone* — registi, attori, curatori,
relatori, amministratori — sono sostituiti dal ruolo, sempre e ovunque. I nomi dentro un
**toponimo** o dentro il **titolo ufficiale di un'opera o di una sede** si riportano invece
verbatim.

**Perché.** DEC-102 protegge i dati personali di chi compare nelle notizie; `Largo Marcello
Mastroianni` non è un dato personale, è un luogo, e cancellarlo distruggerebbe la
localizzazione, cioè lo scopo dello studio. Un titolo di film è un'opera, non una persona.

**Se l'owner decide diversamente**: la rilettura non serve. I toponimi restano nella colonna
`luoghi` e i titoli nella `sintesi`, quindi una sostituzione successiva è una passata
automatica sui CSV, non un nuovo giro di lettura.

**Verifica fatta.** Controllo sui campi scritti dal modello nel lotto E2: nessun nome di persona
in quanto persona. Le occorrenze trovate sono tutte toponimi o titoli.

---

## D2 — I confini di DEC-102: URL, organizzazioni, autori delle opere

Stato: **aperta**, default già applicato. Nasce da quattro casi isolati dal lettore dei lotti
L17–L18, che li ha dichiarati invece di deciderli in silenzio.

### D2.a — L'URL dell'evidenza contiene a volte un nome di persona nello slug

**Default: l'URL resta intero.** È l'indirizzo pubblico della pagina ufficiale ed è il solo modo
di verificare la notizia; mutilarlo renderebbe l'evidenza inservibile e con essa tutto il
metodo, che poggia sulla verificabilità. DEC-102 tiene fuori i *dati di fonte redistribuiti*,
non gli indirizzi delle pagine pubbliche a cui la decisione stessa impone di rimandare
("every item credits its organiser and links back").

### D2.b — Nomi di gruppi musicali e di collettivi

**Default: restano alla lettera.** Il lettore li aveva resi con il ruolo, come i solisti: è la
scelta più prudente ma è sbagliata, e la correggo. Un gruppo o un collettivo è
un'**organizzazione**, non una persona, e DEC-102 prescrive di accreditare l'organizzatore.
Renderlo generico cancellerebbe l'unica informazione che identifica l'evento. Tre righe da
rivedere (E2_096, E2_074, E2_334).

### D2.c — Autori delle opere messe in scena o proiettate

**Default: restano alla lettera.** Il nome dell'autore di un'opera è attribuzione
bibliografica, non un dato personale di qualcuno coinvolto nel fatto. Un cartellone che
annuncia un classico teatrale reso come "un dramma di un drammaturgo" non informa nessuno.
Restano con il ruolo, invece, le persone *presenti al fatto*: chi dirige, recita, cura,
modera, presenta.

### D2.d — Il blocco di rassegna ripetuto in coda a decine di pagine

**Default confermato: contesto in `note`, non una riga per pagina.** Il lettore lo ha trovato
in coda a 47 pagine di un lotto e 46 dell'altro. Generarne una riga per pagina avrebbe prodotto
novanta notizie identiche e falsato ogni conteggio di copertura. È la scelta giusta.

### Regola generale che le tiene insieme

DEC-102 protegge **le persone in quanto persone coinvolte nel fatto**. Non copre i luoghi, le
organizzazioni, i titoli delle opere, i loro autori, né gli indirizzi delle pagine pubbliche.
Dove il confine resta incerto il lettore riporta alla lettera e lo dichiara in `note`: una
dichiarazione si corregge con una passata sui CSV, un'informazione cancellata si recupera solo
rileggendo.

**Se l'owner decide diversamente**: nessuna rilettura. Tutte e quattro le scelte sono
reversibili con una passata automatica, perché i valori interessati stanno in colonne dedicate
o sono annotati riga per riga.

---

## D3 — Quando la persona *è* la notizia: intitolazioni e commemorazioni

Stato: **aperta**, default già applicato. Nasce dal lettore dei lotti L02–L03, che ha segnalato
i casi in cui applicare DEC-102 alla lettera **costa la notizia**.

**Il caso.** Un avviso municipale annuncia una statua dedicata a un attore. La persona non è
qualcuno *coinvolto* nel fatto: è **l'oggetto pubblico della commemorazione**. Resa con
perifrasi, la notizia diventa "una statua dedicata a un attore" e non informa più nessuno: non
si sa a chi, non si sa perché, non è verificabile. Stessa cosa per una fondazione che porta il
nome dell'artista, per una targa, per un'intitolazione di una sala o di un premio.

**Esempi dal lotto**: `A1_056` (statua e fondazione intitolate a un attore), `A1_011` (nome
della fondazione omesso), `A1_128` (titolo di film che coincide con il nome di una persona).

**Default applicato.** Quando il fatto *è* la dedica — statue, targhe, intitolazioni, premi,
fondazioni — il nome **resta alla lettera**. Restano con il ruolo le persone coinvolte nel
fatto: chi delibera l'intitolazione, chi la presenta, chi parla alla cerimonia.

**Corollario sull'evidenza.** Lo stesso lettore aveva iniziato a **troncare la frase di
evidenza** prima dei nomi (`A1_012`, `A1_008`). Un'evidenza tagliata non sostiene più la
notizia, e l'evidenza è la garanzia su cui poggia l'intero metodo. Regola: dentro
`evidenza_locale` il nome si sostituisce con il ruolo **dentro la frase**, senza accorciarla.

**Perché in generale.** DEC-102 nasce per non ridistribuire dati personali raccolti dalle
fonti. Non nasce per rendere incomprensibili le notizie pubbliche su commemorazioni pubbliche.
Una regola di tutela che cancella l'oggetto della notizia non tutela nessuno: produce solo un
database che non si può leggere.

**Se l'owner decide diversamente**: nessuna rilettura. I nomi interessati stanno in righe
annotate una per una nei file dei problemi, e la sostituzione è una passata sui CSV.

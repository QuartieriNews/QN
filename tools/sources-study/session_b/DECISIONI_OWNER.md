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

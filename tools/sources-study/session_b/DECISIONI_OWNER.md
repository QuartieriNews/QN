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

---

## D4 — Ditta individuale il cui nome è il nome di una persona

Stato: **aperta**, default applicato. Nasce dal lettore degli atti B01–B03, che ha isolato il caso
invece di risolverlo in silenzio.

**Il caso.** Un atto municipale riporta la richiesta di un P.A.M.A. da parte di una **ditta
individuale**, la cui denominazione coincide con il nome della persona fisica che è anche parte del
procedimento. Le regole già decise si contraddicono: D2.b dice che le **organizzazioni** restano
alla lettera (e una ditta lo è); D1 dice che le **persone coinvolte nel fatto** diventano il ruolo
(e il richiedente lo è). Il lettore ha applicato la regola di chiusura — nel dubbio riporta e
dichiara — ed è l'unico nome di persona fisica rimasto nei tre lotti.

**Default che applico: il nome va tolto.** Dove la denominazione di una ditta individuale coincide
con il nome di una persona che è anche parte del procedimento, **vince la persona**: diventa "una
ditta individuale". DEC-102 esiste per non ridistribuire i dati personali di chi compare nelle
fonti, e una ditta individuale non ha un nome diverso da quello del suo titolare — chiamarla
"organizzazione" sarebbe un cavillo che svuota la tutela proprio nel caso in cui serve. Restano
alla lettera le società con denominazione propria, anche quando contiene un cognome.

**Costo della scelta**: si perde l'identificazione del richiedente in un atto amministrativo
pubblico. È accettabile: il Report 1 e il Report 2 misurano che cosa le fonti offrono a un
giornale di quartiere, non tengono un registro di chi presenta pratiche.

**Se l'owner decide diversamente**: una riga, corretta senza rileggere nulla.

## D5 — il numero civico di una sede pubblica (aperta, 16 settembre)

**Il problema.** La regola di ri-identificazione vieta i numeri civici, perché un civico più una
via individuano un'abitazione e quindi una persona. Tre lettori diversi, indipendentemente, hanno
segnalato lo stesso effetto collaterale: applicata alla lettera, la regola toglie il civico anche a
**sedi pubbliche** — uno sportello anagrafico, un'aula consiliare, una scuola, un immobile comunale
messo a bando — dove non c'è nessuna persona da proteggere.

**Il costo, misurato su un caso reale.** In una seduta del Municipio V si discutono due immobili
comunali contigui sulla stessa via: uno con contratto firmato, l'altro con affidamento revocato.
Senza i civici **diventano indistinguibili per indirizzo**, e il lettore ha dovuto distinguerli per
esito e destinazione. Lo stesso vale per gli open day della carta d'identità, dove il civico è
l'informazione che serve al lettore per andarci.

**Raccomandazione.** Tenere il civico quando individua una **sede di un ente pubblico o un immobile
pubblico** (municipio, anagrafe, scuola, biblioteca, impianto, immobile a bando): lì il civico è
l'indirizzo di un servizio, non di una persona. Toglierlo quando individua un'abitazione, il
recapito di un richiedente o di un privato coinvolto in un procedimento — cioè il caso per cui la
regola esiste.

**Perché la decisione è dell'owner e non mia.** La regola oggi è uniforme e quindi facile da
verificare; l'eccezione introduce un giudizio («questa sede è pubblica?») che qualcuno deve
esercitare riga per riga. È un baratto fra precisione e verificabilità, e sta all'owner sceglierlo.
Fino alla decisione i lettori continuano ad applicare il divieto senza eccezioni, dichiarandolo.

## D6 — Il territorio degli atti `CEN_`

**Aperta il 16 settembre 2026.**

Negli atti delle commissioni capitoline (`CEN_CPC_*`, `CEN_CPV_*`) il segmento del nome che somiglia
a un Municipio è **un segnaposto della fonte, non il territorio**. Il territorio vero, quando c'è,
si legge dall'oggetto: «Parco Archeologico di Centocelle» dice Municipio V, «via Giorgio Ribotta»
dice Municipio IX.

La specifica impone che un valore dedotto non sia mai scritto come letto, e un lettore l'ha
applicata alla lettera: `municipio = non verificato` su **9 righe su 14**, anche dove il toponimo
rende il Municipio ovvio. La regola è giusta e il costo è reale: quelle righe non entrano in nessuna
statistica per Municipio, e il Report 2 ne ha diverse.

**Le due strade.**
1. **Restare alla lettera**: `non verificato` dove l'atto non dichiara il territorio. Nessuna
   deduzione entra nei dati; le statistiche per Municipio perdono le righe capitoline.
2. **Dedurre dal toponimo dichiarandolo**: il territorio si ricava dal gazetteer a partire dai
   luoghi nominati, e una colonna dice che è una deduzione nostra e non una lettura. È la stessa
   cosa che il database già fa con `tier_localizzazione`.

**Raccomandazione**: la seconda, perché la deduzione resta visibile e reversibile, e perché il
gazetteer che la fa è lo stesso già usato per tutte le altre fonti. Ma è una decisione sul dato
pubblicato, non una scelta tecnica, e non la prendo io.

**Finché non è decisa** i lettori restano alla lettera (strada 1): è la più prudente e non crea
dati che poi andrebbero disfatti.

## D7 — La registrazione che continua dopo la fine della seduta

**Aperta il 16 settembre 2026. Non è una decisione sui nostri file: quelli sono già a posto.**

In una registrazione pubblicata dalla piattaforma istituzionale il flusso **prosegue per circa tredici
minuti dopo la chiusura dei lavori**, con parlato privato di natura personale catturato a microfono
aperto, del tutto estraneo alla seduta. Non è un difetto di trascrizione: è la fonte che ha
pubblicato oltre la chiusura.

Il lettore non ha fatto entrare nulla nei nostri file, **nemmeno anonimizzato**, e nel proprio log
non ha riprodotto né il contenuto né gli identificativi. Dalla nostra parte è chiuso.

**Quello che resta è una scelta dell'owner, e non la prendo io**: quel materiale è **ancora online**,
pubblicato dall'amministrazione, e riguarda persone che non sapevano di essere registrate.

Le strade sono tre, e hanno costi diversi:
1. **Segnalare a chi gestisce la piattaforma**, indicando la registrazione e il minutaggio. È la cosa
   che protegge le persone, ed è anche un atto che ci identifica come chi ha guardato.
2. **Dirlo nel rapporto senza identificare la registrazione**, come difetto di sistema: protegge le
   persone dal nostro lato, non le toglie da lì.
3. **Non fare nulla.** Sconsigliato: sapere e tacere è una scelta anche quella.

**Raccomandazione**: la prima, con la seconda come conseguenza — nel rapporto il caso si racconta
senza identificare l'item, e la segnalazione la fa l'owner, non lo studio. Una segnalazione va
mandata da chi ha un nome e un indirizzo, non da una sessione automatica.

**Finché non decide**, il caso resta nel rapporto in forma non identificante e nessuno viene
contattato.

**Aggiornamento del 16 settembre, ore 13:10Z — non è più un caso isolato.** Un secondo lettore ha
trovato in un'altra registrazione **venti minuti di microfono aperto durante una sospensione**, con
conversazioni private di consiglieri e di pubblico, in parte mascherate dalla pipeline della
piattaforma e in parte no. Anche qui il lettore ha rimosso tutto e non ha riprodotto nulla nel log.

**Terzo caso, ore 13:58Z**: ventidue parole di conversazione privata dopo la chiusura dichiarata,
in coda a un'altra registrazione ancora. Il lettore le ha rimosse senza riprodurle. E un dato che
serve a non gonfiare il conto: un altro lettore ha **cercato esplicitamente** microfoni aperti e
parlato oltre la chiusura in tutti e dieci i propri item — compresi trentacinque minuti muti — e non
ne ha trovati. Da qui in avanti i mandati chiedono di cercarlo e di **dichiarare anche quando non
c'è**: tre casi valgono solo se si sa in quanti item si è guardato.

Tre casi su 305 registrazioni lette non fanno una frequenza, ma cambiano la natura della decisione:
il primo poteva essere un incidente, due sono un **modo in cui la fonte pubblica sistematicamente
più di quello che intende pubblicare** — e nel secondo caso non è nemmeno «dopo la fine»: è dentro
la seduta, in una pausa che tutti in aula considerano privata. La raccomandazione non cambia (la
segnalazione la fa l'owner), ma vale ora per una prassi, non per un item.

# Cronaca: processo, regole, problemi da risolvere — ottobre 2026

Richiesta dell'owner (10 ottobre 2026): «immaginare un processo per farlo, delle regole e
poi provare a vedere se preso un mese dell'anno, quanti nuovi articoli arriveremmo a
produrre con una tabella che abbia il numero delle notizie trovate, e su quanti e quali
giornali erano riportate. Poi bisogna capire che processo seguire per assicurare all'AI
l'accesso alle fonti […] Insomma iniziare sul definire tutti i problemi da risolvere con
delle possibili soluzioni.»

Questo documento è un'analisi del builder, non una decisione. Ciò che cambia il perimetro
deciso è raccolto in §7 come `OWNER_DECISION_REQUIRED` e nella bozza
`decisions/DEC-108-press-in-cronaca.md` (DECIDED l'11 ottobre per l'MVP, §4.5–4.6). Le righe per fatto, con titoli e link
delle testate, stanno nel foglio `cronaca_giugno_2026_testate.xlsx`, da caricare su Drive
(`QN Hub / 20 Packages / Fonti 2026-06`). Qui restano procedure e conteggi (DEC-102,
DEC-104).

## 1 Che cosa è già deciso

- **Perimetro delle fonti.** La pipeline Cronaca della baseline (v0.6 §2.D) parte dalle sei
  fonti ufficiali di sicurezza e giustizia: Questura/Polizia di Stato, Carabinieri,
  Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza. Le testate giornalistiche
  non sono una fonte prevista. Il 9 ottobre l'owner ha confermato «Solo fonti ufficiali» per
  la tabella di giugno. Questa analisi misura le testate perché l'owner lo ha chiesto, ma
  il loro uso era allora una scelta aperta (DEC-108, decisa l'11 ottobre: §4.5–4.6).
- **Nomi.** DEC-016, opzione B: i nomi presenti nelle fonti ufficiali si riproducono in
  automatico, con verifica della seconda AI. Minori, vittime, testimoni, familiari e dati
  sensibili vanno in coda manuale. La capacità «nomi» resta spenta fino al parere legale
  (baseline §4.1).
- **Pubblicazione.** Pubblicazione automatica con doppio controllo AI (DEC-015). Correzioni
  dirette con tracciabilità interna (DEC-020). Golden set Cronaca di 30 comunicati e gate
  G0 prima di cablare la pubblicazione (baseline §2.D).
- **Obiettivo.** Almeno 1 contenuto di Cronaca per ognuna delle 89 pagine (DEC-014), con il
  ripiego della pagina sottile ancora da definire (DEC-006, OPEN).
- **Geografia.** Il protocollo di assegnazione e i livelli di portata quartiere, municipio e
  città valgono anche per la cronaca (DEC-106).

## 2 Il processo proposto

Ogni fase ha un'uscita verificabile. Le fasi 1, 2 e 4 sono già state eseguite a mano su
giugno 2026 per la tabella del 9 ottobre. La fase 3 è stata provata in questa analisi,
sui titoli delle testate (§4).

| Fase | Che cosa fa | Uscita | Chi o che cosa |
|---|---|---|---|
| 1 Raccolta | legge le fonti ammesse dai canali ammessi (§5): pagine ufficiali, feed, liste stampa; se DEC-108 lo consente, i titoli delle testate come segnale | comunicato o segnale grezzo, con URL e data | adattatore per fonte |
| 2 Scheda di fatto | divide il comunicato in fatti: un comunicato con sette arresti dà sette schede | scheda: fatto, data del fatto, luoghi, persone (flag), `case_status`, fonte | AI, con controllo sulla fonte |
| 3 Fusione | riconosce lo stesso fatto fra fonti diverse e fra giorni diversi (aggiornamenti) | `fatto_id` unico e catena di aggiornamenti | regole di confronto più AI |
| 4 Geografia | applica il protocollo di assegnazione, con il luogo del fatto (non la sede del reparto che opera) | esito U/M/T/D/I/F, pagine, livello | `stage1.py`, revisore, regole dell'owner |
| 5 Filtro editoriale | decide se il fatto è pubblicabile e dove (§3); instrada i casi sensibili | pubblicabile / coda / escluso, con motivo | AI e regole |
| 6 Verifica | controlla ogni affermazione contro la fonte primaria; per i fatti scoperti dalla stampa vale la regola di conferma (§3 R-C02) | esito della verifica | seconda AI (DEC-015) |
| 7 Redazione | scrive la notizia breve in parole proprie, dai fatti verificati, con fonte e link | testo L1, titolo, fonte citata | AI |
| 8 Pubblicazione e vita | pubblica; aggiorna `case_status` quando arrivano sviluppi; gestisce rettifiche e richieste di deindicizzazione | versione pubblicata, storico interno | publisher, coda (DEC-020) |

La fase 3 è nuova rispetto alla baseline. Senza di essa lo stesso arresto, letto nel
comunicato della Questura e in tre testate, produrrebbe quattro notizie.

## 3 Regole editoriali proposte

Sono proposte del builder. Diventano regole quando l'owner le adotta, e alcune
(segnate ⚖) solo dopo il parere legale (D12).

- **R-C01 · Un fatto, una scheda.** Il fatto è l'unità: un evento con luogo, data e
  protagonisti. Un'operazione su più luoghi è un fatto con più luoghi (esito M). Un
  comunicato di riepilogo produce tante schede quanti sono i fatti riconoscibili. Gli
  aggiornamenti successivi (convalida, scarcerazione, sentenza) si agganciano al fatto,
  non ne creano uno nuovo.
- **R-C02 · Fonte primaria e conferma.** Ogni notizia pubblicata ha una fonte
  primaria citata con link. Fonte primaria: un ente ufficiale (comunicato, nota alla
  stampa) oppure, se DEC-108 lo ammette, una testata citata come tale. Un fatto scoperto
  solo dalla stampa si pubblica (a) dopo conferma ufficiale, oppure (b) se è riportato da
  almeno due testate indipendenti e attribuito («secondo Abitare a Roma e Roma Daily News…»). Due
  articoli della stessa agenzia ripresa da più siti contano come una sola fonte.
- **R-C03 · Parole proprie, nessuna ripresa.** QN scrive dai fatti, non riassume
  l'articolo di un altro. Niente frasi, titoli o foto delle testate. Il link
  all'articolo è ammesso come riferimento; un estratto non lo è finché il legale non si
  è espresso (art. 43-bis e art. 101 l. 633/1941, §6 P-07). ⚖
- **R-C04 · Presunzione di innocenza.** Si scrive «arrestato», «denunciato», «indagato»,
  mai «il ladro» o «lo spacciatore» per una persona non condannata. `case_status` è
  visibile e aggiornato. Gli sviluppi favorevoli all'interessato (scarcerazione,
  archiviazione, assoluzione) si pubblicano con la stessa evidenza. ⚖
- **R-C05 · Persone.** Si applica DEC-016. Per nessuna fonte, ufficiale o di stampa: nomi o
  dettagli che identificano minori (anche come autori), vittime di reati sessuali,
  persone coinvolte in suicidi o tentati suicidi, dati sanitari. Questi casi vanno
  sempre in coda manuale. Un nome letto solo su una testata non si riproduce in
  automatico: DEC-016 copre solo le fonti ufficiali. ⚖
- **R-C06 · Luogo del fatto.** Il luogo è quello dove il fatto è avvenuto, non quello
  della caserma o del commissariato che ha operato né la residenza dell'arrestato. «Zona
  Tuscolana» senza altri elementi vale come strada lunga e dà D (protocollo, casi
  frequenti).
- **R-C07 · Soglia di pubblicazione.** Va su una pagina-quartiere un fatto localizzato
  che tocca chi ci vive: reati con luogo, incidenti con feriti o chiusure, incendi,
  crolli, controlli con esiti, sgomberi, soccorsi rilevanti. Vanno a livello città
  (T) le operazioni senza luogo, i servizi e le campagne. Fuori dal Comune (F): esclusi.
  I fatti senza esito e senza luogo (un controllo «a campione» senza risultati) non si
  pubblicano.
- **R-C08 · Tempestività.** Si pubblica entro 48 ore dalla fonte primaria. Un fatto più
  vecchio di 7 giorni entra solo come sviluppo di un fatto già pubblicato. La Questura
  pubblica spesso riepiloghi giorni dopo i fatti: la data visibile è quella del fatto,
  non quella del comunicato.
- **R-C09 · Equilibrio della pagina.** La cronaca non deve diventare la voce dominante di
  un quartiere. Proposta: nella pagina, al massimo un fatto di cronaca ogni N contenuti
  degli altri blocchi; per un numero eccessivo, un riepilogo settimanale per quartiere.
  Il valore di N è da fissare con l'owner dopo il primo mese.
- **R-C10 · Immagini.** Nessuna foto di persone né foto prese dalle testate. Immagine
  generata (mappa del luogo) o nessuna immagine: è la decisione ancora aperta di baseline §2.D.
- **R-C11 · Rettifica e deindicizzazione.** Le richieste si gestiscono con DEC-020. Le
  richieste di deindicizzazione da parte di chi è stato prosciolto o assolto hanno una
  procedura scritta e un tempo massimo di risposta. ⚖

## 4 La prova su giugno 2026

### 4.1 Come è stata fatta

Mese: giugno 2026. È lo stesso della tabella del 9 ottobre: i fatti ufficiali erano già
divisi in schede e assegnati alle pagine. Due passate, entrambe senza aprire articoli.
Strumenti e istruzioni di lettura: `tools/cronaca-prova/`. Conteggi:
`tools/cronaca-prova/runs/2026-10-10/riepilogo.json`.

- **In avanti, dai fatti ufficiali alle testate.**
  - I fatti: i 177 nel Comune di Roma pubblicati a giugno da Questura, Carabinieri, Vigili
    del Fuoco e Polizia Locale (le 196 schede meno le 19 fuori Roma).
  - La ricerca: per ogni fatto, al massimo due ricerche web limitate a 20 domini di
    testate. Il confronto usa solo titolo, URL e riassunto della ricerca.
  - Corrispondenza `certa`: tipo, luogo, due dettagli e data compatibili. Altrimenti
    `probabile`.
  - Copertura: 131 fatti cercati, con 170 ricerche. Restano senza ricerca 46 fatti (35
    della Questura), per il tetto di ricerche del turno.
  - Limiti: la ricerca non vede Corriere, Repubblica e Rai News. RomaToday e Il
    Messaggero non mettono la data nell'URL, quindi le loro corrispondenze restano per
    lo più `probabile`.
- **Inversa, dalle testate aperte ai fatti.**
  - Il censimento: tutti i titoli di giugno delle sei testate che non escludono gli
    agenti AI, 5.030 in tutto (Dire 1.212, Roma Daily News 1.158, Il Tempo 1.107,
    Abitare a Roma 776, Il Faro Online 702, VignaClaraBlog 75).
  - Il filtro: per sezione o parola chiave, 659 candidati.
  - La lettura dei titoli: 387 sono cronaca nel Comune di Roma e formano 272 fatti. Gli
    altri sono 128 fuori Roma, 119 non cronaca e 25 cronaca giudiziaria su fatti
    precedenti.
  - Il confronto: ogni fatto è stato confrontato con i fatti ufficiali dei giorni
    vicini, con la pagina QN presa dal luogo nel titolo (`qngeo.py`, senza rete).

Il lavoro è stato fatto da agenti, uno per lotto. Il builder ha controllato a campione
otto righe della passata in avanti. Nessuna revisione umana completa: i numeri sono stime da
confermare, non conteggi certificati.

### 4.2 Notizie uniche e numero di testate

A giugno le notizie uniche di cronaca nel Comune di Roma sono **387**: 177 dalle fonti
ufficiali e 210 trovate solo sulle testate aperte. Per 341 di queste il numero di testate
è stato contato: i 131 fatti ufficiali cercati e le 210 notizie delle testate aperte. Per
ogni notizia le testate trovate nelle due passate sono unite.

| Su quante testate | Notizie ufficiali | Notizie solo dei giornali | Totale |
|---|---|---|---|
| nessuna (solo la fonte ufficiale) | 40 | — | 40 |
| 1 | 32 | 154 | 186 |
| 2 | 27 | 43 | 70 |
| 3 | 15 | 11 | 26 |
| 4 | 11 | 1 | 12 |
| 5 o più | 6 | 1 | 7 |
| **totale** | **131** | **210** | **341** |

- **Notizie ufficiali:** le testate sono cercate fra una ventina di testate.
- **Notizie solo dei giornali:** le testate sono contate solo fra le sei aperte. Il conto
  è quindi un minimo: la stessa notizia può essere anche su RomaToday o sul Messaggero.
- **Il massimo:** 10 testate, per l'operazione della Digos del 16 giugno.
- **Fatti ufficiali senza ricerca:** sono 46. Per loro le testate vengono solo dalla
  passata inversa (27 con nessuna, 15 con una, 3 con due, 1 con tre) e non sono in
  tabella.

**Verifica sulle 154 notizie viste su una sola testata aperta.** Il numero è gonfiato dal
modo di contare: le notizie dei giornali sono contate solo fra le sei testate aperte.

- **Il campione:** 43 di queste notizie, estratte in proporzione alle testate con seed
  20261010, cercate su 20 domini con 54 ricerche
  (`tools/cronaca-prova/runs/2026-10-10/verifica_testata_unica.json`).
- **L'esito:** 37 su 43 (86%) sono uscite anche su altre testate, 20 con corrispondenza
  certa. Il totale per notizia diventa: 1 testata 6, 2 testate 24, 3 testate 5, 4 testate
  4, 5 o più 4.
- **Chi le riprende:** RomaToday ne ha 34 su 43. Seguono Il Messaggero (8), Fanpage (6),
  Leggo (5) e ANSA (3).

Le notizie davvero di una sola testata sono quindi una minoranza: circa il 14%,
fra il 4% e il 24% con l'incertezza del campione. La cronaca locale circola fra le
testate quasi quanto quella nazionale. RomaToday è il nodo che la riprende quasi tutta.

Il dettaglio della sola passata in avanti, senza unire le testate trovate dalla passata
inversa:

| Testate che riportano il fatto | Fatti (corrispondenza certa o probabile) | Fatti (solo certa) |
|---|---|---|
| nessuna | 42 | 79 |
| 1 | 33 | 39 |
| 2 | 30 | 10 |
| 3 | 14 | 2 |
| 4 o più | 12 | 1 |
| **fatti cercati** | **131** | **131** |

Quasi sette fatti ufficiali su dieci (89 su 131) compaiono su almeno una testata, con
2,2 testate in media. Con la sola corrispondenza certa sono 52. La ripresa cambia molto
per fonte:

| Fonte | Cercati | Ripresi |
|---|---|---|
| Carabinieri | 16 | 15 |
| Polizia Locale | 8 | 8 |
| Questura | 101 | 65 |
| Vigili del Fuoco | 6 | 1 |

Per esito geografico: U 53/78, D 17/25, T 10/12, M 5/8, I 4/8.

### 4.3 Quali testate

| Testata | Fatti ufficiali ripresi (certa o probabile / certa) | Fatti di cronaca romana a giugno (censimento) | …di cui senza fatto ufficiale corrispondente |
|---|---|---|---|
| RomaToday | 60 / 18 | non censibile | — |
| Abitare a Roma | 58 / 16 | 234 | 175 |
| Il Messaggero | 16 / 1 | non censibile | — |
| ANSA | 12 / 12 | non censibile | — |
| Fanpage | 9 / 2 | non censibile | — |
| Il Faro Online | 9 / 7 | 46 | 40 |
| RomaIT | 7 / 1 | — | — |
| Roma Daily News | 4 / 0 | 56 | 45 |
| Agenzia Nova | 4 / 0 | non censibile | — |
| LaPresse, Adnkronos | 3 / 3, 3 / 0 | — | — |
| Il Tempo | 2 / 2 | 11 | 9 |
| Dire | 2 / 1 | 7 | 5 |
| Leggo, Sky TG24, Affaritaliani | 2 ciascuna | — | — |
| VignaClaraBlog | 1 / 1 | 11 | 8 |
| il Giornale, il Fatto Quotidiano | 1 ciascuna | — | — |
| Corriere Roma, Repubblica Roma, Rai News | non visibili alla ricerca | — | — |

Due fonti dominano la cronaca romana: RomaToday fra le testate chiuse agli agenti AI,
Abitare a Roma fra quelle aperte. Riprendono un numero simile di fatti ufficiali (60 e 58).

### 4.4 Quello che le fonti ufficiali pubbliche non dicono

Dei 272 fatti di cronaca romana sulle sei testate aperte, 62 corrispondono a un fatto
ufficiale (49 con certezza). **210, il 77%, non hanno un fatto corrispondente sui siti
ufficiali.** Il conto riguarda solo sei testate, perché le testate chiuse non si possono
censire, quindi è un minimo.

- **Per tipo:** furti 29, controlli 27, aggressioni 26, incidenti 24, rapine 18, incendi
  16, sequestri 14, droga 12, morti 11, altro 33.
- **Per geografia:** 138 a livello di quartiere con una pagina, 11 di municipio, 25 di
  città, 36 dubbi (strade lunghe, luoghi non chiari).
- **Per numero di testate:** 56 sono riportati da almeno due delle sei testate aperte.
- **Ente citato nel titolo:** in 45 casi il titolo nomina Carabinieri, Polizia o un altro
  ente. Probabilmente vengono da comunicazioni ufficiali mandate ai giornalisti e non
  pubblicate sul web: le liste stampa di §5.3.
- **Morti:** gli 11 casi della categoria vanno tutti in coda (R-C05).

Dati da verificare emersi dalla prova:

- CR-C1_074-3 (Ponte di Nona, comunicato del 3 giugno) compare su ANSA e Abitare a Roma
  con data 7 febbraio 2026.
- CR-C2_093-1 riguarda una truffa del 21 aprile, con l'arresto avvenuto a Napoli.

La data del comunicato non è sempre la data del fatto (R-C08).

### 4.5 Quanti articoli in un mese

Un fatto produce un articolo. «Presenze» sono gli articoli sommati sulle pagine (un fatto
M conta su più pagine). L'obiettivo di DEC-014 è almeno 1 fatto di cronaca per ciascuna
delle 89 pagine.

| Scenario (DEC-108) | Fatti a giugno | Presenze sulle pagine | Pagine con almeno 1 |
|---|---|---|---|
| A · fonti ufficiali pubbliche, come la tabella del 9 ottobre | 177 | 134 | 48 |
| A + liste stampa degli enti | non misurabile da fuori; indizio: 45 fatti della stampa citano un ente | — | — |
| B · testate aperte come segnale, pubblicate solo dopo conferma | fino a 177 + 210 = 387 | fino a 134 + 138 = 272 | fino a 62 |
| C · in più i fatti su due testate aperte, senza conferma | 177 + 56 = 233 | 134 + 43 = 177 | 54 |
| testate chiuse (RomaToday, Il Messaggero, Corriere…) | non misurabili senza licenza | — | — |

Il limite superiore di B dipende da quanti fatti un ente conferma, e oggi non si sa.

Che cosa dicono questi numeri:

- **Il volume.** Le testate aperte più che raddoppiano il numero di fatti, ma le pagine
  raggiunte passano solo da 48 a 62. La cronaca si concentra dove già c'è: Ostia, Esquilino e
  Centro hanno già comunicati ufficiali.
- **L'obiettivo di DEC-014.** In nessuno scenario misurato tutte le 89 pagine hanno un
  fatto di cronaca a giugno: ne restano almeno 27 a zero. Il ripiego della pagina
  sottile (DEC-006) serve comunque. Per decidere conviene misurare tre mesi, non uno.
- **La concentrazione.** Abitare a Roma da sola porta 175 dei 210 fatti in più.
  Dipendere da una testata di zona è un rischio: copertura diseguale fra i Municipi,
  rapporto commerciale con un concorrente (P-19).

### 4.6 Giugno con la regola delle due fonti (11 ottobre)

Dopo la decisione di DEC-108 per l'MVP, l'owner ha chiesto di rifare il mese con il flusso
deciso, controllando che la raccolta prenda tutto e non si blocchi:

- **regola:** è pubblicabile un fatto ufficiale, oppure un fatto riportato da almeno due
  editori diversi, di cui almeno una testata aperta da cui si possa scrivere;
- **risultato voluto:** una tabella con le notizie di giugno per quartiere.

Strumenti: `tools/cronaca-prova/` (passi 8–12 del README). Conteggi:
`tools/cronaca-prova/runs/2026-10-11/`. Il foglio per quartiere, con i fatti, è su Drive.

**Raccolta ufficiale.** Il raccoglitore ha letto gli elenchi di giugno di tutte e sei le
fonti e ha scaricato ogni comunicato.

| Fonte | Comunicati | Elenco | Durata |
|---|---|---|---|
| Questura | 79 | 33 pagine | 7,5 minuti, una richiesta ogni 4 secondi |
| Carabinieri | 20 | 151 comunicati nazionali | |
| Vigili del Fuoco | 8 | | |
| Polizia Locale | 2 | | |
| Procura | 0 | | |
| Guardia di Finanza | 0 | 128 notizie nazionali | |

- **Completezza e blocchi:** 109 comunicati, gli stessi 109 dell'inventario di settembre,
  URL per URL. Zero rifiuti, zero errori. Ogni pagina è stata controllata: non è una
  pagina di blocco, ha il testo del comunicato.
- **Altre categorie della Questura:** il sito ne ha cinque oltre a «I fatti del giorno», ma
  nessuna con comunicati di giugno.
- **Errore trovato e corretto:** il parser della Polizia Locale leggeva le notizie in
  evidenza del portale invece dell'elenco del Corpo. In più la paginazione del sito non
  funziona: pagina 2 restituisce la pagina 1.

**Testate aperte.**
- Il censimento resta quello di §4.1: 5.030 titoli e 272 fatti.
- Dei fatti che il titolo non localizzava (72) sono stati letti 94 articoli. Con il testo:
  - 23 fatti hanno ora una pagina;
  - 11 toccano più quartieri e contano su ciascuno;
  - 7 risultano fuori dal Comune.
- Due fatti doppi sono stati uniti.

**Testate chiuse, solo titolo, link e ora.**
- **Fonte:** i file grezzi di GDELT dal 29 maggio al 3 luglio, 3.456 file da 15 minuti,
  nessuno mancante.
- **Quanto copre GDELT:** dove si può confrontare con il censimento completo ritrova il 70%
  degli articoli di Il Tempo e il 77% di Dire. Non copre Abitare a Roma e VignaClaraBlog,
  che però sono censite per intero.
- **Il filtro:** 2.023 titoli candidati alla cronaca romana. I principali: RomaToday 546,
  Il Messaggero 470, Corriere Roma 294, ANSA 237, Repubblica Roma 139.
- **La lettura dei titoli:**
  - 1.093 sono cronaca a Roma;
  - 757 di questi vanno su fatti già noti: 169 ufficiali e 588 delle testate aperte;
  - 336 formano fatti visti solo sulle testate chiuse: 155 nel periodo, 8 doppi fusi fra
    finestre vicine, 96 di giugno.

**Risultato.**

| Fatti di giugno a Roma | Numero |
|---|---|
| da fonti ufficiali | 177 |
| dai giornali con almeno due editori, scrivibili | 175 |
| **pubblicabili in tutto** | **352** |
| dai giornali con un solo editore (non pubblicati) | 27 |
| solo testate chiuse, almeno due editori (non scrivibili) | 22 |
| solo testate chiuse, un editore | 74 |

Fra i 175 fatti dei giornali con almeno due editori:
- **la seconda fonte:** in 166 viene da una testata chiusa (RomaToday in 149) e solo in 9
  da un'altra testata aperta (misura presa dal foglio dei fatti su Drive l'11 ottobre, non
  da un file versionato; dal 15 ottobre `riepilogo.json` la scrive come `seconda_fonte`);
- **il livello:** 151 hanno una pagina, gli altri sono di livello città, municipio o
  dubbi.

**Pagine.**
- **Copertura:** 48 pagine su 89 hanno almeno un fatto con le sole fonti ufficiali; con la
  regola delle due fonti diventano **64**.
- **Presenze:** salgono da 134 a 299.
- **Pagine coperte solo grazie ai giornali (16):** Laurentino, Appio Latino, Colli Aniene,
  Bravetta, Colli Portuensi, Magliana, Prima Porta, Spinaceto, Torrino, Cesano, Colle
  Prenestino, Corviale, Rebibbia, San Basilio, Settecamini, Torrevecchia.
- **Pagine ancora scoperte (25):** Ardeatino, Bufalotta, Casal Lumbroso, Casal Palocco,
  Castel di Leva, Dragona-Dragoncello, Garbatella, Giardino di Roma, Infernetto, La
  Giustiniana, La Rustica, La Storta, Marcigliana, Massimina, Montagnola, Morena,
  Muratella, Olgiata, Pisana, Romanina, Selva Candida, Torraccia, Trigoria,
  Tuscolano-Quadraro, Vitinia.
- **Altre soglie:** se bastasse una fonte le pagine sarebbero 65; contando anche le chiuse
  non scrivibili, sempre 65.
- **Lettura:** le pagine scoperte sono quasi tutte periferiche. Sono soprattutto nel sud e
  nell'ovest (Municipi X 4, VIII 3, IX 3, XV 3, XII 2), più alcune a nord-est e sud-est (III,
  IV, V, VII). Qui il limite non è la regola delle due fonti: con una fonte sola si
  coprirebbe una pagina in più. Di quei quartieri a giugno non ha scritto quasi nessuno.
  Servono il ripiego della pagina sottile (DEC-006) o fonti di altro tipo (comitati,
  Municipi).

**Qualità e limiti.**
- **Controllo a campione (manuale, non calcolato dai run):** su 10 fatti «due fonti» con
  una testata chiusa, 9 abbinamenti sono lo stesso fatto. Uno è debole (un automobilista denunciato abbinato a un articolo
  su cento multe nella ZTL): il margine d'errore è intorno al 10%.
- **Solo titoli:** abbinamenti e luoghi delle testate chiuse vengono dai titoli e dal
  testo degli URL.
- **Copertura di GDELT incompleta:** qualche fatto con due fonti vere è contato con una.
- **Corriere e Repubblica:** entrano solo tramite GDELT.
- **Fatti vicini:** le scelte fra due fatti simili negli stessi giorni sono annotate dai
  lettori.
- **Dati di dettaglio:** le righe per fatto, con titoli e link, sono nel foglio su Drive.

### 4.7 Settembre 2026: raccolta ripetuta, lettura rinviata (13 ottobre)

L'owner ha chiesto di ripetere su settembre la misura di §4.6 (passi 8–12 del README di
`tools/cronaca-prova`), con `QN_MESE=2026-09` e la finestra 1–30 settembre. La raccolta
(passi 8–9 e censimento delle testate aperte) è stata fatta per intero e senza blocchi; la
lettura dei titoli e l'abbinamento (passi 10–12) non sono stati fatti, perché il pacchetto
«Metodo QN» (`QN_PKG`), che assegna la pagina QN alle notizie, non è su Drive in
`QN Hub / 20 Packages / Fonti 2026-06` né nell'ambiente. Senza di esso nessun fatto di
settembre ha una pagina, e la tabella per quartiere non si può comporre. Conteggi:
`tools/cronaca-prova/runs/2026-09/`. Titoli, link e testi: Drive, `Fonti 2026-09`.

**Raccolta ufficiale.** Lo stesso raccoglitore di giugno, sui sei elenchi di settembre.

| Fonte | Giugno | Settembre | Elenco | Durata |
|---|---|---|---|---|
| Questura | 79 | 81 | 13 pagine | 6,8 minuti, una richiesta ogni 4 secondi |
| Carabinieri | 20 | 19 | 164 comunicati nazionali | |
| Vigili del Fuoco | 8 | 6 | | |
| Polizia Locale | 2 | 0 | | |
| Procura | 0 | 0 | | |
| Guardia di Finanza | 0 | 5 | 113 notizie nazionali | |
| **Totale** | **109** | **111** | | |

- **Completezza e blocchi:** 111 comunicati scaricati, 0 rifiutati, 0 errori. Ogni pagina è
  stata controllata: non è una pagina di blocco, ha il testo del comunicato. La Guardia di
  Finanza, che a giugno non aveva comunicati romani, ne ha 5 a settembre; la Polizia Locale
  nessuno.
- **Errore trovato e corretto:** nella prima passata il sito dei Carabinieri ha servito, con
  codice 200, la pagina «Il sistema è temporaneamente non disponibile» per una pagina di elenco e
  per due comunicati. Il raccoglitore non la riconosceva: l'elenco si è fermato a 5 pagine (80
  comunicati nazionali, 8 romani) e i due comunicati sono risultati «testo troppo corto». Ora
  quella pagina vale come rifiuto temporaneo (ritentativo con attesa, poi rifiuto dichiarato); la
  seconda passata ha letto 9 pagine, 164 comunicati nazionali, 19 romani, tutti scaricati.
- **Giorni con almeno un comunicato:** 30 su 30.

**Testate aperte (censimento, passi 1–2).**

| Testata | Titoli giugno | Titoli settembre | Candidati cronaca settembre |
|---|---|---|---|
| Abitare a Roma | 776 | 779 | 306 |
| VignaClaraBlog | 75 | 111 | 12 |
| Dire | 1.212 | 1.227 | 31 |
| Roma Daily News | 1.158 | 1.247 | 127 |
| Il Faro Online | 702 | 1.040 | 234 |
| Il Tempo | 1.107 | 697 | 35 |
| **Totale** | **5.030** | **5.101** | **745** |

I candidati sono il risultato del filtro largo (`filtro.py`): la classe vera (cronaca a Roma,
fuori Roma, non cronaca) la dà la lettura, non eseguita. A giugno dai 5.030 titoli il filtro e
la lettura avevano dato 272 fatti di cronaca romana.

**Testate chiuse, solo titolo, link e ora.**
- **Fonte:** i file grezzi di GDELT dal 29 agosto al 3 ottobre, 3.456 file da 15 minuti,
  0 mancanti; 72.807 righe delle testate seguite.
- **Quanto copre GDELT** a settembre, contro il censimento completo delle testate aperte:
  Il Tempo 539 su 697 (77%), Dire 977 su 1.227 (80%), Il Faro Online 187 su 1.040 (18%), Roma Daily News 53 su 1.247 (4%); Abitare a Roma e VignaClaraBlog non compaiono in GDELT, ma sono censite per intero. Per Il Tempo GDELT ha più indirizzi (737) del censimento dalle sitemap giornaliere (697): a settembre le sitemap di Il Tempo non sono complete.
- **Il filtro:** 2.009 titoli candidati alla cronaca romana nella finestra, 1.704 con
  data di settembre. I principali: RomaToday 529, Il Messaggero 458, Corriere della Sera Roma 290, ANSA 218, la Repubblica Roma 138. A giugno erano 2.023.
- **La lettura dei titoli** (ISTRUZIONI_CHIUSE, FUSIONI, LUOGHI) non è stata fatta: vedi sopra.

**Confronto giugno/settembre, per quanto si può dire senza la lettura.**

| | Giugno | Settembre |
|---|---|---|
| comunicati ufficiali | 109 | 111 |
| titoli delle sei testate aperte | 5.030 | 5.101 |
| candidati cronaca sulle aperte (filtro) | 659 | 745 |
| titoli chiusi candidati (GDELT + filtro) | 2.023 | 2.009 |
| fatti pubblicabili | 352 | non misurato |
| pagine coperte | 64 / 89 | non misurato |
| pagine scoperte | 25 | non misurato |

- **Fatti pubblicabili, pagine coperte e scoperte** di settembre si misurano solo dopo la
  lettura con `QN_PKG`: la raccolta è pronta su Drive e i lotti si preparano con gli stessi
  comandi di giugno. Il giudizio sulle 25 pagine scoperte resta quello di §4.6, da confermare
  su tre mesi.
- **Che cosa dice già la raccolta:** le fonti ufficiali danno 111 comunicati contro 109 (Questura 81 contro 79, Carabinieri 19 contro 20, Vigili del Fuoco 6 contro 8, Guardia di Finanza 5 contro 0); le testate aperte producono lo stesso volume (5.101 titoli contro 5.030) con più candidati al filtro (745 contro 659, per la crescita di Il Faro Online e Roma Daily News); le testate chiuse danno lo stesso ordine di grandezza (2.009 candidati contro 2.023). La materia prima di settembre non è più povera di quella di giugno; se la lettura confermasse le stesse proporzioni, i fatti pubblicabili sarebbero dell'ordine dei 350 e le pagine coperte intorno ai due terzi. È un'attesa, non una misura.

## 5 Accesso dell'AI alle fonti

### 5.1 Principio

QN non aggira nessuna barriera. Non supera paywall, non usa account in automatico
(DEC-102). Non dichiara un user agent finto, non usa proxy residenziali per
cambiare indirizzo, non risolve captcha e non usa browser automatizzati travestiti da
persone. Rispetta il robots.txt e le riserve di estrazione di testo e dati (TDM)
anche quando sono rivolte ad agenti con un altro nome. Un canale chiuso resta chiuso:
si cerca un canale aperto o una licenza. Non è solo prudenza: l'elusione delle misure
tecniche di protezione è vietata (artt. 102-quater e 171-ter l. 633/1941), e una
riserva TDM espressa esclude l'estrazione per fini commerciali (art. 70-quater, dalla
direttiva UE 2019/790 art. 4). Sono punti da confermare nel parere legale, non pareri.

### 5.2 Che cosa si vede oggi (sondaggio del 9–10 ottobre 2026)

Sondaggio sulla pagina della sezione romana o di cronaca e sul robots.txt di ogni
testata, con un user agent dichiarato. I dati grezzi sono su Drive.

| Testata | Esclude gli agenti AI nel robots.txt | Riserva TDM dichiarata | Abbonamento o paywall | Barriera osservata | Canale lecito per un agente AI oggi |
|---|---|---|---|---|---|
| RomaToday | sì (ClaudeBot, GPTBot, anthropic-ai e altri) | sì (TDMRep) | sì | — | nessuno senza licenza; solo titolo e link da un motore di ricerca |
| Il Messaggero | sì | — | sì | — | come sopra |
| Corriere della Sera Roma | sì | sì | sì | rifiutato anche dal motore di ricerca dell'agente | nessuno |
| la Repubblica Roma | sì (anthropic-ai, GPTBot, CCBot) | — | sì | rifiutato dal motore di ricerca dell'agente | nessuno |
| Leggo | sì | — | sì | — | titolo e link da motore di ricerca |
| ANSA | sì | — | in parte | — | titolo e link; abbonamento d'agenzia |
| Agenzia Nova | sì; `Content-Signal: ai-train=no`, dichiarato riserva ex art. 4 dir. 2019/790 | sì | — | 403 (Cloudflare) | abbonamento d'agenzia |
| Today.it | sì | sì | sì | — | nessuno senza licenza |
| Fanpage | — | — | — | 403 a ogni richiesta | nessuno |
| Il Tempo | no | no | in parte | — | sitemap giornaliere |
| Dire | no | no | in parte | — | API pubblica del sito, feed Roma |
| Roma Daily News | no | no | no | API esclusa dal robots.txt | sitemap |
| Il Faro Online | no | no | no | API esclusa dal robots.txt | sitemap |
| Abitare a Roma | no | no | no | — | API pubblica del sito |
| VignaClaraBlog | no | no | no | — | API pubblica del sito |
| Il Corriere della Città | no | no | no | — | inattivo a giugno (1 articolo) |

Altri canali provati:

- Google News RSS: escluso dal robots.txt per tutti i robot (`Disallow: /`) e per nome agli
  agenti AI. Non usato.
- GDELT, indice aperto di notizie: da questo ambiente risponde 429 (troppe richieste da un
  indirizzo condiviso). Non usato.
- La ricerca web dell'agente restituisce titolo, URL e un breve riassunto, ma non
  vede corriere.it, repubblica.it e rainews.it. Ha anche un tetto di ricerche per
  turno.

Le testate che coprono di più la cronaca romana sono chiuse agli agenti AI. Le aperte
sono testate piccole o di zona. Il quadro dell'accesso si legge quindi testata per
testata, non in blocco.

### 5.3 Canali di accesso possibili, dal più pulito

1. **Liste stampa degli enti ufficiali.** Questura, Comando provinciale dei Carabinieri,
   Vigili del Fuoco, Polizia Locale e Procura mandano note e comunicati ai giornalisti per
   email, e il sito pubblico ne mostra solo una parte. L'accesso richiede di solito una
   testata registrata con un direttore responsabile: la registrazione è già nel percorso
   legale della baseline (I). È il guadagno più grande e il più lecito: aumenta i fatti
   ufficiali senza toccare le testate.
2. **Fonti ufficiali aggiuntive.** Prefettura, Roma Capitale (Polizia Locale per gruppo
   municipale, protezione civile), Roma Mobilità e Atac per incidenti e chiusure, i 15
   Municipi. Procura e Guardia di Finanza, a giugno, non avevano comunicati romani
   leggibili sul web: da verificare se pubblicano altrove.
3. **Testate aperte, solo metadati.** Titolo, data e link dai canali che il robots.txt
   ammette (sitemap, feed, API pubblica), come segnale che un fatto esiste. Meglio ancora
   con un accordo scritto con la testata: costa una lettera, toglie ogni dubbio e può
   diventare uno scambio (link e citazione in cambio dell'uso).
4. **Licenze.** Abbonamento a un'agenzia (ANSA, Dire, Nova, Adnkronos, LaPresse: servizi
   regionali Lazio) con clausola che ammetta il trattamento automatico. Oppure un servizio
   di rassegna stampa che ha già le licenze degli editori. Da chiedere: prezzo, e se la
   licenza copre l'uso da parte di un sistema AI.
5. **Motori e indici di notizie via API.** API di ricerca a pagamento (Bing, Brave, Google
   Programmable Search) o GDELT da un indirizzo non condiviso. Danno titolo, URL e data,
   con condizioni d'uso esplicite. Servono a scoprire e a contare, non a scrivere.
6. **Lettura umana.** L'owner, o un collaboratore, legge le testate in abbonamento e
   inserisce in coda il fatto con il link (raccolta manuale, DEC-102). L'AI riceve la
   segnalazione umana, non l'articolo. Le condizioni dell'abbonamento personale vanno
   lette: spesso escludono l'uso commerciale del contenuto, non la conoscenza del
   fatto.
7. **Nessuna delle precedenti.** Si resta sulle fonti ufficiali pubbliche, con il
   ripiego della pagina sottile (DEC-006).

## 6 Problemi da risolvere e possibili soluzioni

Ogni problema ha un numero, le soluzioni possibili e chi decide. «Builder» vuol dire che
il problema si risolve costruendo; «owner» che serve una scelta; «legale» che serve il
parere (D12).

| # | Problema | Soluzioni possibili | Chi |
|---|---|---|---|
| P-01 | **Perimetro delle fonti.** La baseline prevede solo fonti ufficiali; la stampa è una scelta aperta. | Le quattro opzioni di DEC-108 (solo ufficiali; stampa come segnale; stampa come fonte citata; contenuti in licenza). | owner |
| P-02 | **Copertura ufficiale insufficiente e diseguale.** A giugno i fatti ufficiali arrivano a 48 pagine su 89 (§4.5), e l'obiettivo è 1 per pagina. | Liste stampa degli enti (testata registrata); fonti ufficiali aggiuntive (§5.3); stampa come segnale (DEC-108 B); riepilogo municipale come ripiego (DEC-006); obiettivo misurato su tre mesi, non su uno. | owner, builder |
| P-03 | **Il sito pubblico della Questura è un sottoinsieme, con ritardo.** Molti comunicati sono riepiloghi di più giorni. Alcuni riportano fatti di mesi prima o fuori Roma (§4.4). | Data del fatto distinta da data del comunicato (R-C08); lista stampa per avere le note del giorno; misura del ritardo medio per fonte; controllo della data contro la stampa quando c'è. | builder |
| P-04 | **Procura e Guardia di Finanza a zero a giugno.** | Verificare dove pubblicano (sito, social, liste stampa); se restano a zero, toglierle dalle sei fonti attese e dirlo. | builder |
| P-05 | **Paywall.** Le testate maggiori sono in abbonamento. | Mai aggirare. Solo metadati (titolo, link) da canali ammessi; lettura umana con segnalazione (§5.3 n. 6); licenza (n. 4). | owner |
| P-06 | **Esclusione degli agenti AI e protezioni anti-bot.** Le testate maggiori escludono gli agenti AI nel robots.txt; due rispondono 403 a ogni richiesta; Google News esclude tutti. | Rispettare sempre, anche verso agenti con altro nome; user agent onesto e ritmo lento sulle testate aperte; accordo scritto; licenze o API con condizioni d'uso esplicite. | owner, builder |
| P-07 | **Diritti sui testi delle testate.** «Riproduzione sistematica di notizie a fine di lucro» è illecita per un periodico (art. 101 l. 633/1941); estratti online soggetti al diritto degli editori (art. 43-bis); riserve TDM (art. 70-quater). | Scrivere dai fatti verificati con parole proprie; solo link alle testate; parere legale su quando una notizia scoperta dalla stampa e confermata altrove resta un uso lecito. | legale |
| P-08 | **Verifica.** Le testate sbagliano o divergono sui dettagli; un fatto ripreso da cinque siti può avere una sola origine (agenzia o comunicato). | Regola R-C02 (conferma ufficiale, o due fonti indipendenti dove ammesso); riconoscere le riprese d'agenzia; seconda AI sui fatti (DEC-015); `case_status` visibile. | builder, owner |
| P-09 | **Lo stesso fatto in più fonti e più giorni.** | Fase 3 di fusione: confronto su tipo, luogo, data ±3 giorni, dettagli (età, numero di persone, oggetto); `fatto_id` e catena degli aggiornamenti; in dubbio, coda. | builder |
| P-10 | **Luogo.** Sede del reparto scambiata per luogo del fatto; «zona Tuscolana»; fatti senza luogo. | Protocollo di assegnazione e livelli (DEC-106); R-C06; esito D quando il luogo è una strada lunga; T per i fatti cittadini. | builder |
| P-11 | **Persone e casi sensibili.** Minori, vittime, suicidi, dati sanitari; nomi che compaiono solo sulla stampa. | DEC-016 e R-C05; coda manuale; i nomi letti solo sulla stampa non si riproducono in automatico. | legale, owner |
| P-12 | **Presunzione di innocenza e sviluppi.** Gli enti comunicano meno dopo il d.lgs. 188/2021; arresti poi non convalidati; assoluzioni. | R-C04; aggiornamento di `case_status`; pubblicazione degli sviluppi favorevoli; deindicizzazione su richiesta (R-C11). | legale, builder |
| P-13 | **Rettifiche.** | DEC-020; procedura con tempi; storico interno delle versioni. | owner |
| P-14 | **Immagini.** Nessuna fonte lecita chiara per la cronaca. | Mappa generata o nessuna immagine (baseline §2.D, decisione aperta). | owner |
| P-15 | **Cronaca che domina la pagina.** Un quartiere letto solo attraverso reati e incidenti peggiora la percezione e la fiducia. | R-C09 (tetto e riepilogo); ordine dei blocchi; misura dopo il primo mese. | owner |
| P-16 | **Costo e tempo.** Ogni fatto richiede lettura, fusione, geografia, scrittura e verifica. | Misurare i minuti per caso nella thin slice; automatizzare fusione e geografia; coda solo per i casi sensibili e i dubbi. | builder |
| P-17 | **Responsabilità editoriale.** Liste stampa, rettifiche e cronaca richiedono una testata registrata e un direttore responsabile. | Registrazione già prevista nel percorso legale (I); anticiparla se si sceglie A o B. | owner, legale |
| P-18 | **Misurabilità.** Le testate maggiori non si possono censire da un agente AI; la ricerca web ha un tetto e non vede tre testate. | Misura sulle testate aperte (completa) più campione via ricerca (parziale), dichiarati come tali; un'API di ricerca a pagamento o GDELT da un indirizzo proprio per una misura completa. | builder |
| P-19 | **Rapporto con le testate locali.** Sono le fonti più ricche e anche concorrenti. | Accordo di citazione e link; scambio di visibilità; nessuna ripresa senza accordo. | owner |

## 7 OWNER_DECISION_REQUIRED

1. **Ruolo della stampa nella Cronaca:** DEC-108, quattro opzioni. Raccomandazione del
   builder: A subito; B quando ci sono la testata registrata e il permesso scritto delle
   testate aperte; C e D solo dopo il parere legale. **Deciso dall'owner l'11 ottobre per
   l'MVP:** opzione C (fatto su due testate, articolo con parole proprie e testate citate)
   e nomi presi dai giornali con l'opzione B; la posizione per il lancio pubblico resta da
   decidere (DEC-108).
2. **Registrazione della testata, da anticipare?** Serve per le liste stampa degli enti
   (§5.3 n. 1), che sono il canale più ricco e più pulito. Oggi la registrazione sta nel
   percorso legale (I) della fase 2.
3. **Regole R-C01…R-C11 (§3):** adottarle, modificarle o rinviarle. Quelle segnate ⚖
   entrano nel pacchetto per il legale (D12), insieme a tre domande nuove:
   - art. 101 l. 633/1941: un fatto scoperto dalla stampa e confermato da un ente può
     diventare una notizia di QN?
   - art. 43-bis: i link e i titoli delle testate sono ammessi?
   - le riserve TDM e le esclusioni degli agenti AI vincolano anche un sistema che non
     usa quei nomi di agente?
4. **Seconda parte della prova.** Due possibilità:
   - completare la passata in avanti sui fatti rimasti senza ricerca: basta un tuo
     messaggio, perché il tetto di ricerche vale per turno;
   - misurare in modo completo le testate chiuse con un'API di ricerca a pagamento o con
     GDELT da un indirizzo proprio: costo e canale li decidi tu.
5. **Esclusioni di principio:** confermare che QN non legge in automatico le testate
   che escludono gli agenti AI o riservano il TDM, salvo licenza (§5.1). È la posizione
   tenuta in questa prova.

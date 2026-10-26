# Notizie di quartiere nei dati già raccolti: rilettura a ritroso (M, 26 ottobre 2026)

La domanda dell'owner. Fra il 20 e il 26 ottobre abbiamo letto migliaia di pagine Facebook, siti e feed di associazioni,
comitati, enti e luoghi per trovare eventi. Molte di quelle fonti sono state scartate perché non ne avevano. Fra tutto quel
materiale, comprese le fonti scartate, c'erano notizie utili agli altri blocchi del sito? Si escludono giornali e testate,
non si fa nessuna lettura nuova e non si usa Apify.

Il materiale resta su Drive, perché porta testi delle fonti (DEC-022, DEC-109): `notizie_dai_dati_2026-10-26.xlsx`, con le
sintesi scritte da noi e il link alla fonte. Qui stanno solo il metodo, i numeri e i nomi delle organizzazioni.

## 1. Che cosa è stato riletto

- **Post Facebook: 12.550.** Sono gli ultimi 10-15 post delle pagine lette a ottobre: censimento RUNTS, censimento delle
  associazioni, pagine verificate dall'owner, secondo giro, lista supplementare, Acilia. Coprono 2.521 pagine, comprese le
  pagine dormienti e quelle senza eventi.
- **Notizie dei siti: 4.146.** Sono le voci dei feed delle notizie di 455 siti (528 feed letti nella prova del canale del 26
  ottobre).
- **Fuori.** Sono stati scartati:
  - 318 voci di testate e media;
  - 1.642 testi troppo corti;
  - 319 doppioni.
- **Finestra.** Dal 24 aprile al 25 ottobre 2026: 1.917 voci più vecchie restano fuori. Restano 14.779 voci.

Le voci sono state passate in quattro passaggi, tutti fatti da modelli AI, sullo stesso testo già in casa:

1. **Smistamento** di tutte le 14.779 voci. Per ognuna: se è utile, per quale blocco, con un punteggio da 0 a 5. Le voci
   saltate al primo passaggio (171) sono state riprese da un secondo lettore, e nessuna è rimasta fuori.
2. **Scheda** per le 1.090 voci utili con punteggio almeno 3. La scheda contiene:
   - blocco e tema;
   - origine (fatto della fonte, rilancio di un ente pubblico, rilancio di un giornale);
   - luogo e attualità;
   - eventuali elementi sensibili;
   - una sintesi di al massimo 30 parole, scritta da noi.
3. **Verifica scettica** delle 478 schede con punteggio almeno 4. Un secondo modello rilegge il testo originale e scarta
   promozioni, semplici annunci di eventi, rilanci di giornali, fatti non locali o superati, e schede che travisano il testo.
4. **Fusione** dello stesso fatto letto da fonti diverse.

Un campione di 18 notizie confermate è stato controllato a mano: le sintesi sono fedeli e non riprendono il testo della fonte.

## 2. Che cosa c'era

**Lo smistamento delle 14.779 voci:**

| Esito | Voci |
|---|---|
| promozione o altro | 5.712 |
| non locale (nazionale o di altre città) | 4.601 |
| solo evento (resta nel blocco Eventi) | 2.843 |
| servizio o avviso utile | 559 |
| notizia di quartiere | 404 |
| segnalazione o tema dei residenti | 338 |
| rilancio di una testata, senza fatti propri | 168 |
| istituzionale | 154 |

**Il risultato:**
- Notizie confermate dalla verifica: 402, pari a 347 fatti diversi dopo la fusione (44 fatti letti da più fonti).
- Altre schede utili, non verificate o declassate: 521, nel foglio come «da vedere».
- Le confermate sono recenti: 237 di ottobre, 255 negli ultimi trenta giorni.
- 309 su 402 hanno un luogo preciso (una via, un parco, una scuola, un ufficio).
- 346 su 402 sono fatti o posizioni della fonte stessa e 48 sono rilanci di comunicati di enti pubblici. Solo 4 riprendono un
  giornale aggiungendo fatti propri; i rilanci puri di giornali sono rimasti fuori.

| Blocco | Notizie confermate | di cui di ottobre |
|---|---|---|
| Notizie di quartiere | 154 | 82 |
| Segnalazioni e temi dei residenti | 124 | 68 |
| Servizi e avvisi utili | 85 | 55 |
| Istituzionale | 39 | 32 |

| Tema | Confermate |
|---|---|
| ambiente e verde | 69 |
| mobilità e trasporti | 55 |
| lavori e cantieri | 36 |
| sicurezza e emergenze | 34 |
| rifiuti e decoro | 32 |
| casa e urbanistica | 31 |
| aperture e chiusure | 31 |
| sanità e salute | 24 |
| servizi, bandi e scadenze | 21 |
| scuola | 19 |
| solidarietà e sociale | 19 |
| attivismo e partecipazione | 11 |
| municipio e istituzioni | 9 |
| altri | 11 |

**Geografia.** La pagina QN è stata assegnata così:
- dal luogo del fatto, quando contiene un toponimo del gazetteer: 221 notizie;
- dal municipio nominato: 24;
- dalla sede della fonte: 92. Questa è un'ipotesi da verificare, perché un eletto o un ente cittadino parla anche di luoghi
  lontani dalla sua sede;
- di tutta la città: 12;
- senza assegnazione: 53.

**Copertura delle pagine.**
- 75 delle 89 pagine QN hanno almeno una notizia confermata.
- Le 22 pagine con meno di cinque eventi ne hanno 56, distribuite su 15 di loro. Fra le cinque pagine senza eventi: Vitinia
  ne ha 5, Lunghezza 2, La Rustica 1, La Storta 0 confermate (2 da vedere), Marcigliana nessuna.
- Senza notizie confermate restano 15 pagine: Aurelio, Bravetta, Casal Lumbroso, Castel di Leva, Cesano, Colli Aniene,
  Infernetto, La Storta, Marcigliana, Massimina, Muratella, Nomentano, Olgiata, Portuense, Roma Nord.

**Voci sensibili.** 30 confermate toccano minori, salute, persone decedute o persone nominate. Sono segnate nel foglio e non
vanno pubblicate senza la coda manuale.

## 3. Chi produce le notizie

Le fonti scartate per gli eventi e quelle senza notizie non coincidono. «Con eventi» vuol dire che la fonte ha dato almeno un
evento alla pagina «Eventi dei quartieri», come promotore o nello schedario. L'incrocio sulle 2.820 fonti rilette (pagine
Facebook e siti):

| | con notizie confermate | solo notizie da vedere | nessuna notizia | totale |
|---|---|---|---|---|
| fonti con eventi | 91 | 82 | 749 | 922 |
| fonti senza eventi | 111 | 127 | 1.660 | 1.898 |

Che cosa dice:
- **La maggior parte delle fonti scartate per gli eventi è vuota anche di notizie:** 1.660 su 1.898, l'87%. Sono pagine con
  post di promozione, nazionali o di altre città, o ferme.
- **Una parte delle scartate invece porta notizie:** 111 con notizie confermate e 127 con notizie da vedere.
- **Metà delle notizie confermate viene da fonti che non hanno dato eventi:** 217 su 402, da 111 organizzazioni sulle 194 che
  ne producono. L'altra metà viene da fonti che danno anche eventi.
- **I comitati di quartiere sono il caso più netto:** 36 comitati su 52 non hanno dato eventi, ma portano 91 delle loro 136
  notizie.
- **Il confronto riguarda solo le fonti di cui avevamo post o feed.** Gli enti senza pagina o con la pagina non accessibile
  non si potevano rileggere.

| Tipo di fonte | Organizzazioni (di cui senza eventi) | Notizie confermate (di cui da fonti senza eventi) |
|---|---|---|
| comitati di quartiere e di cittadini | 52 (36) | 136 (91) |
| associazioni per il verde e l'ambiente | 12 (8) | 39 (18) |
| municipi ed eletti (pagine ufficiali, sindaco, assessori, presidenti) | 10 (4) | 30 (17) |
| enti pubblici e culturali | 7 (0) | 14 (0) |
| pagine di cittadini sui trasporti | 1 (0) | 8 (0) |
| parrocchie e realtà religiose | 4 (0) | 6 (0) |
| scuole | 2 (0) | 2 (0) |
| sport | 1 (0) | 3 (0) |
| altre associazioni e realtà sociali (centri anziani, reti di accoglienza, associazioni di zona) | 105 (63) | 164 (91) |
| totale | 194 (111) | 402 (217) |

Le fonti più ricche, per tipo:
- **Comitati di quartiere.**
  - Comitato di Quartiere Casalotti, Casal Selce, Selva Candida, Selva Nera;
  - CdQ La Romanina;
  - Comitato di Quartiere di Trigoria;
  - Comitato di Quartiere Nuova Tor Tre Teste Attiva;
  - Comitato di Quartiere Castelverde di Roma;
  - Comitato Colli D'Oro;
  - Comitato di quartiere La Voce di Galla Placidia San Polo Cluniacensi;
  - Associazione CdQ Villaggio Prenestino;
  - CdQ Vitinia;
  - Comitato Valle Galeria Libera.
- **Verde e ambiente.**
  - Bosco Caffarella APS;
  - Associazione per Villa Pamphilj;
  - Associazione Gentes Villaggio Giuliano Dalmata;
  - Circolo Garbatella di Legambiente;
  - Associazione Parco della Torre di Tormarancia.
- **Enti pubblici e culturali.**
  - Roma Capitale;
  - Zètema;
  - Parco archeologico del Colosseo;
  - Sovrintendenza Capitolina;
  - Fondazione Musica per Roma.
- **Municipi.** Le pagine ufficiali dei Municipi I, III, IV, XII e XIII.
- **Realtà sociali.**
  - Casale Alba Due;
  - Caro Corviale - Comunità e accoglienza;
  - centri anziani di Ottavia e di Vigna Murata.

## 4. Che cosa vuol dire per gli altri blocchi

- **Segnalazioni e temi dei residenti.** I comitati di quartiere sono la fonte principale. Raccontano commissioni ottenute,
  degrado, verde, viabilità, sicurezza, e hanno quasi sempre un luogo preciso. Sono 52 fonti già nello schedario o nel
  censimento: un elenco pronto per il blocco, senza leggere i gruppi Facebook.
- **Notizie di quartiere.** Arrivano soprattutto dalle associazioni dei parchi (restauri, riaperture, manutenzione), dai
  comitati e dalle realtà sociali (aperture e chiusure di servizi di zona).
- **Servizi e avvisi utili.** Vengono dagli enti pubblici e culturali: chiusure, riaperture, servizi nuovi di Roma Capitale,
  campagne della ASL con luogo e data.
- **Istituzionale.** Le pagine dei Municipi e degli eletti annunciano consigli e commissioni, con l'ordine dei lavori. Sono un
  segnale: la fonte primaria resta l'atto ufficiale.
- **Cadenza.** Le stesse letture che servono agli eventi (§1 undecies del rapporto delle fonti) portano anche queste notizie
  senza costo aggiuntivo di lettura: post e feed sono già pagati o gratuiti. Serve solo il passaggio di smistamento e scheda.

## 5. Limiti

- È una fotografia. Per ogni pagina ci sono gli ultimi 10-15 post, quindi i mesi più lontani sono sottorappresentati, e non è
  un flusso.
- La geografia presa dalla sede della fonte (92 notizie) va verificata. 53 notizie non hanno una pagina.
- Il giudizio è di modelli AI con una verifica scettica e un campione controllato a mano, non di una redazione.
- I gruppi Facebook di quartiere (blocco Conversazione) non sono stati letti.

## 6. OWNER_DECISION_REQUIRED

**Fonti non giornalistiche per i blocchi Notizie e Segnalazioni.** La baseline costruisce la cronaca su sei fonti ufficiali e
DEC-108 ammette la stampa citata. Nessuna decisione dice se un post di un comitato o di un'associazione possa essere la fonte
di una notizia o di una segnalazione pubblicata. Opzioni:

- **(a)** solo come segnale, pubblicato dopo una conferma ufficiale o di stampa;
- **(b)** come fonte citata, con il nome e il link della fonte e le regole di DEC-108 su nomi e presunzione di innocenza;
- **(c)** come fonte citata solo nel blocco Segnalazioni dei residenti, presentata come voce del comitato e non come fatto
  accertato.

Il builder non sceglie.

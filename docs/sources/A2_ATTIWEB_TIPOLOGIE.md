# A2 Atti Web — selezione delle tipologie, filtri applicati e verifica delle categorie centrali

| Campo | Valore |
|---|---|
| Stato | Nota di verifica richiesta dall'owner il 15 settembre 2026, dopo il rapporto intermedio. **Le conclusioni sulla copertura di A2 restano provvisorie** finché l'approfondimento di §6 non è deciso ed eseguito |
| Cosa corregge | Il rapporto intermedio dichiara "17 tipologie" per A2: le tipologie interrogate il 15 settembre (mattina) sono **16**, 15 con risultati e 1 con errore del portale (§2). Il numero 1.426 è la somma dei 15 codici con risultati e non cambia |
| Letture | 15 settembre 2026: interrogazioni originali 10:42–10:47; sweep di tutte le tipologie 12:05–12:20; esempi e controlli 12:20–12:40 (Europe/Rome) |
| Dati per item | Drive `QN Hub / 20 Packages / Fonti 2026-06/`: `A2_DDS_2026-06_items_compact_part1..4.csv`, `A2_centrali_2026-06_items_compact_part1..2.csv` (URL, date, struttura, esiti del lookup; nessun oggetto integrale, nessun nome) |
| Stato del dato | M = misurato sul portale con URL e ora; S = stimato, con l'ipotesi; — = mancante |

## 1. Come sono state selezionate le tipologie il 15 settembre (mattina)

Il menu "Tipologia" del portale è servito dall'API `data/filtro-dati!caricaListaTipologie.action`
e contiene **48 codici** più la voce aggregata "Tutte le tipologie". Il 15 settembre ho scelto i
codici la cui denominazione contiene "del Municipio" o "Municipi", cioè l'**organo emittente
municipale**, e li ho interrogati uno per uno: CMD, GMD, CMC, MMC, DMS, PMO, PMT, GMT, GMM, CMZ,
CMY, CMR, CMV, GMV, MMV, DMK (16 codici). Tre tipologie municipali sono rimaste fuori (KMD, WMD,
XMO: commissioni straordinarie del Municipio) e tutte le tipologie degli organi centrali sono
state escluse a priori. Il criterio era l'organo, non il territorio interessato: l'obiezione
dell'owner è fondata e §4 misura quanto le categorie centrali contengono per i quartieri.

## 2. Filtri effettivamente applicati, campo data e percorso fino ai 1.426 atti

- **Endpoint**: `POST https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/data/filtro-dati!cerca.action`
  con parametri nella query string: `tipologia=<codice>`, `dtRprDa=2026-06-01`, `dtRprA=2026-06-30`,
  `hitCountRicerca=1`, `firstResult=0` (poi `500` per MMC), `itemsPerPage=500` (massimo accettato).
  Nessun filtro su struttura, ente, argomento, oggetto, sottotipologia; il portale restituisce
  `flgTutti=N`. Le date in formato italiano (`01/06/2026`) producono un errore Struts: solo il
  formato ISO funziona.
- **Campo data**: `dtRpr`, la **data di repertorio** dell'atto (colonna "Data" dell'interfaccia,
  campo `dtRpr` nel controller AngularJS). L'API espone anche `dtProt` (protocollo) e `dtSeduta`
  (seduta): con lo stesso intervallo restituiscono un errore del server (verificato alle 12:15 su
  CMD e GCD); `annoAttoDa/A=2026` restituisce 9.935 per CMD, incompatibile con i conteggi mensili,
  significato non chiarito: non usato. Il portale **non espone una data di pubblicazione**, e le
  pubblicazioni tardive esistono: DMS è passata da 191 (10:42) a **193** (12:10) atti con data
  di repertorio di giugno nello stesso giorno. Per il metodo §4.1 il conteggio va annotato: il
  numero di giugno può crescere dopo la lettura.
- **Percorso**: 16 richieste → 15 risposte JSON e 1 errore (DMK) → righe di `elencoAtti`:
  CMC 55, CMD 42, CMR 44, CMV 24, CMY 8, CMZ 32, DMS 191, GMD 32, GMM 15, GMT 32, GMV 25, MMC 516
  (500 + 16), MMV 407, PMO 2, PMT 1 = **1.426**; per ogni codice `total` dichiarato = righe
  ricevute; `idDoc` e URL univoci 1.426; nessuna deduplicazione, nessuna esclusione; tutte le
  `dtRpr` cadono in giugno; Municipio ricavato dal campo `dscStrOrg` per 1.426 su 1.426. URL del
  PDF: `showPdfDoc?fun=deliberazioniAtti&par1=<tipologia base64>&par2=<idDoc base64>`.
- **Errore del portale = risultato vuoto**: la stessa interrogazione su un giorno senza atti (CMD,
  7 giugno) produce l'errore Struts "Index: 0, Size: 0". Nella tabella di §3 "errore" è quindi
  letto come "senza risultati nel periodo", con la controprova dell'intervallo lungo dove fatta.

## 3. Tabella completa delle 48 tipologie

Sweep del 15 settembre 2026 (12:05–12:20), stesso filtro di §2, `itemsPerPage=200`; per DDS
lettura completa (921). "Terr." = atti del campione con Municipio o zona riconosciuti
deterministicamente nell'oggetto (lookup del gazetteer più "Municipio N"), su n letti.

| Codice | Denominazione ufficiale | Organo emittente | 15/09 mattina | Sweep 15/09 | Giugno 2026 | Terr. | Nello studio | Motivazione |
|---|---|---|---|---|---|---|---|---|
| CMC | Convocazioni del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 55 | 29/55 | sì | organo municipale |
| CPC | Convocazioni delle Commissioni Capitoline | Commissioni dell'Assemblea Capitolina | non interrogata | con risultati | 99 | 0/99 | da decidere (§6) | oggetto senza toponimi; ordine del giorno nel PDF |
| MMC | Convocazioni delle Commissioni Consiliari del Municipio | Commissioni del Consiglio del Municipio | interrogata | con risultati | 516 | 7/200 | sì | organo municipale |
| KD | Deliberazioni del Commissario / Straordinario del Consiglio Comunale | Commissario (Comune di Roma, pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico, nessun atto nel 2026 |
| KCD | Deliberazioni del Commissario / Straordinario dell'Assemblea Capitolina | Commissario straordinario | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| WCD | Deliberazioni del Commissario / Straordinario della Giunta Capitolina | Commissario straordinario | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| WD | Deliberazioni del Commissario / Straordinario della Giunta Comunale | Commissario (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| MD | Deliberazioni del Commissario Acta del Consiglio Comunale | Commissario ad acta (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| MCD | Deliberazioni del Commissario Acta dell'Assemblea Capitolina | Commissario ad acta | non interrogata | con risultati | 2 | 0/2 | no | nessun riferimento territoriale |
| OCD | Deliberazioni del Commissario Acta della Giunta Capitolina | Commissario ad acta | non interrogata | con risultati | 1 | 0/1 | no | idem |
| OD | Deliberazioni del Commissario Acta della Giunta Comunale | Commissario ad acta (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| PD | Deliberazioni del Commissario Straordinario di Governo per il piano di rientro | Commissario di Governo | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| KID | Deliberazioni del Commissario delle Istituzioni | Commissario delle Istituzioni | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| CD | Deliberazioni del Consiglio Comunale | Consiglio Comunale (pre 2010) | non interrogata | senza risultati (2.642 atti 2000–2026, 381 nel 2005) | 0 | — | no | archivio storico |
| CMD | Deliberazioni del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 42 | 7/42 | sì | organo municipale |
| CID | Deliberazioni del Consiglio di Amministrazione delle Istituzioni | CdA delle Istituzioni (biblioteche e simili) | non interrogata | con risultati | 12 | 0/12 | no | nessun riferimento territoriale nell'oggetto |
| ACD | Deliberazioni dell'Assemblea Capitolina | Assemblea Capitolina | non interrogata | con risultati | 17 | 4 proposte da strutture municipali; 2/17 con zona | da decidere (§6) | ricaduta territoriale in alcuni atti (§4) |
| KMD | Deliberazioni della Commissione Straordinaria del Consiglio del Municipio | Commissione straordinaria (Municipio commissariato) | non interrogata | senza risultati (52 atti 2010–2026) | 0 | — | no | nessun atto nel periodo |
| WMD | Deliberazioni della Commissione Straordinaria della Giunta del Municipio | Commissione straordinaria | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| GCD | Deliberazioni della Giunta Capitolina | Giunta Capitolina | non interrogata | con risultati | 36 | 12/36 | da decidere (§6) | un terzo con Municipio o zona nell'oggetto (§4) |
| GD | Deliberazioni della Giunta Comunale | Giunta Comunale (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| GMD | Deliberazioni della Giunta del Municipio | Giunta del Municipio | interrogata | con risultati | 32 | 16/32 | sì | organo municipale |
| DDS | Determinazioni Dirigenziali | Dirigenti: nel portale solo i Gruppi territoriali della Polizia Locale (discipline di traffico) | non interrogata | con risultati | **921** | 187/921 (Municipio), 151 (zona); Municipio dal gruppo 921/921 | da decidere (§6) | atti a livello di strada, 9 Municipi su 15 (§4) |
| DMS | Determinazioni Dirigenziali del Municipio | Dirigenti del Municipio | interrogata | con risultati | 191 → 193 | 70/193 | sì | organo municipale |
| PMT | Direttive del Presidente del Municipio | Presidente del Municipio | interrogata | con risultati | 1 | 0/1 | sì | organo municipale |
| GMT | Direttive della Giunta del Municipio | Giunta del Municipio | interrogata | con risultati | 32 | 11/32 | sì | organo municipale |
| PS | Disposizioni del Presidente dell'Assemblea Capitolina | Presidente dell'Assemblea Capitolina | non interrogata | senza risultati (107 atti 2010–2026) | 0 | — | no | nessun atto nel periodo; atti organizzativi |
| GCM | Memorie della Giunta Capitolina | Giunta Capitolina | non interrogata | con risultati | 14 | 3/14 | da decidere (§6) | ricaduta territoriale in alcuni atti (§4) |
| GMM | Memorie della Giunta del Municipio | Giunta del Municipio | interrogata | con risultati | 15 | 5/15 | sì | organo municipale |
| CZ | Mozioni del Consiglio Comunale | Consiglio Comunale (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| CMZ | Mozioni del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 32 | 12/32 | sì | organo municipale |
| AZ | Mozioni dell'Assemblea Capitolina | Assemblea Capitolina | non interrogata | con risultati | 20 | 5/20 | da decidere (§6) | un quarto con Municipio o zona (§4) |
| XO | Ordinanze del Commissario / Straordinario | Commissario straordinario | non interrogata | senza risultati | 0 | — | no | nessun atto nel periodo |
| TO | Ordinanze del Commissario Delegato per l'emergenza del traffico | Commissario delegato | non interrogata | senza risultati (7 atti 2000–2026) | 0 | — | no | nessun atto nel periodo |
| PMO | Ordinanze del Presidente del Municipio | Presidente del Municipio | interrogata | con risultati | 2 | 2/2 | sì | organo municipale |
| SO | Ordinanze del Sindaco | Sindaco | non interrogata | con risultati | 17 | 2/17 | da decidere (§6) | per lo più incarichi e organizzazione; 2 con riferimento territoriale |
| XMO | Ordinanze della Commissione Straordinaria del Municipio | Commissione straordinaria | non interrogata | senza risultati (errore anche su 2010–2026) | 0 | — | no | nessun atto trovato |
| AY | Ordini Del Giorno dell'Assemblea Capitolina | Assemblea Capitolina | non interrogata | con risultati | 85 | 21/85 | da decidere (§6) | un quarto con Municipio o zona (§4) |
| CY | Ordini del Giorno del Consiglio Comunale | Consiglio Comunale (pre 2010) | non interrogata | senza risultati | 0 | — | no | archivio storico |
| CMY | Ordini del Giorno del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 8 | 2/8 | sì | organo municipale |
| CPL | Relazioni delle Commissioni Capitoline | Commissioni dell'Assemblea Capitolina | non interrogata | senza risultati (1 atto 2010–2026) | 0 | — | no | tipologia quasi vuota |
| CMR | Risoluzioni del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 44 | 17/44 | sì | organo municipale |
| DDK | Verbali Conferenza Servizi | Conferenze dei servizi (dirigenti) | non interrogata | senza risultati (19 atti 2010–2026) | 0 | — | no | nessun atto nel periodo |
| DMK | Verbali Conferenza Servizi Municipi | Conferenze dei servizi dei Municipi | interrogata | senza risultati (28 atti 2010–2026) | 0 | — | no | il 15/09 mattina l'errore non era stato riconosciuto come risultato vuoto |
| CMV | Verbali del Consiglio del Municipio | Consiglio del Municipio | interrogata | con risultati | 24 | 3/24 | sì | organo municipale |
| GMV | Verbali della Giunta del Municipio | Giunta del Municipio | interrogata | con risultati | 25 | 7/25 | sì | organo municipale |
| CPV | Verbali delle Commissioni Capitoline | Commissioni dell'Assemblea Capitolina | non interrogata | con risultati | 19 | 5/19 (solo Municipio) | da decidere (§6) | ordine del giorno nel PDF |
| MMV | Verbali delle Commissioni Consiliari del Municipio | Commissioni del Consiglio del Municipio | interrogata | con risultati | 407 | 24/200 | sì | organo municipale |

Riepilogo: 16 interrogate il 15/09 mattina (15 con risultati, 1 senza); nello sweep 28 codici con
risultati a giugno e 20 senza; 15 codici entrano nel conteggio di 1.426; 8 codici centrali con
risultati sono "da decidere" (CPC, ACD, GCD, DDS, GCM, AZ, SO, AY, più CPV: 9 con CPV).

## 4. Le categorie centrali contengono informazioni per i quartieri? (verifica su esempi reali)

Organo emittente e territorio interessato sono cose diverse: un atto della Giunta Capitolina può
riguardare una strada di un Municipio. Misura sull'oggetto di tutti gli atti di giugno delle
tipologie centrali con risultati (M), esempi senza nomi di persona; gli URL sono nei CSV su Drive.

| Codice | Giugno | Con Municipio o zona nell'oggetto | Esempi reali (oggetto abbreviato) |
|---|---|---|---|
| DDS | 921 | 187 Municipio, 151 zona; **921 su 921 attribuibili a un Municipio dal Gruppo di Polizia Locale emittente** | "Via Molise – via di San Basilio, D.D.T. provvisoria, manifestazione, 04/06/2026" (I Gruppo Centro Storico); "Viale di Trastevere, D.D.T. provvisoria, lavori di scavo e posa cavi, Direzione Tecnica Municipio Roma I"; "Via di San Basilio, installazione varco ZTL, dal 22/06 al 06/07/2026"; "Viale Carlo Felice – piazza di Porta San Giovanni, celebrazione del Corpus Domini" |
| GCD | 36 | 12 Municipio, 8 zona | "Approvazione dei progetti definitivi delle opere di urbanizzazione primaria, Print 6-6a Pietralata" (Municipio IV); "Manutenzione straordinaria delle coperture degli edifici ERP, complesso in via F. Gon…" (Tor Vergata, VI); "Riconoscimento dell'interesse pubblico di un project financing" (Parioli-Flaminio, II) |
| AY | 85 | 21 | quattro ordini del giorno collegati alla proposta di deliberazione 55/2026 sulla trasformazione urbana della Montagnola (VIII) |
| AZ | 20 | 5 | intitolazione di uno slargo a Fidene (III); interventi nelle aree di via Carlo Felice (I); bando per l'ex Stardust Village al Torrino (IX); sperimentazione estiva a Ostia (X) |
| ACD | 17 | 2 zona; 4 atti proposti da strutture municipali | "Soppressione di parte del mercato Monteverde Vecchio di via G.B. Niccolini e creazione del mercato plateatico attrezzato" (Municipio XII); "Ambito territoriale di riqualificazione e recupero edilizio in zona piazzale Caduti della Montagnola" (VIII); tre riconoscimenti di debiti fuori bilancio dei Municipi IV, VI, VII |
| GCM | 14 | 3 | "Evento Vespa 2026, 25–28 giugno, Foro Italico e Centro Storico"; "sede temporanea del distaccamento dei Vigili del Fuoco di Ostia"; "Santa Cecilia a Massenzio" |
| SO | 17 | 2 | ordinanze su incarichi dirigenziali (anche di un Municipio) e un aggiornamento di ordinanze precedenti con riferimento alla Storta (XV): rilevanza di quartiere bassa |
| CPV | 19 | 5 Municipio, 0 zona | verbali di commissioni capitoline che citano i Municipi (sportelli dei Municipi, pareri su proposte) |
| CPC | 99 | 0 | convocazioni delle commissioni capitoline: l'oggetto indica commissione, data e ora; gli argomenti sono nel PDF |
| CID, MCD, OCD | 15 | 0 | nessun riferimento territoriale |

**DDS in dettaglio (M)**. Tutte le 921 determinazioni di giugno sono dei Gruppi territoriali della
Polizia Locale (verificato anche su maggio 2026: 1.084, stessi 13 gruppi; gennaio 2026: 742, primi
200 tutti P.L.): discipline di traffico provvisorie per lavori e cantieri (≈ 250), riprese
cinematografiche (≈ 77), manifestazioni ed eventi (≈ 65), altro (≈ 529; classificazione per parole
chiave, S). Sono atti a livello di strada, con date di validità nell'oggetto. Per Municipio, dal
gruppo emittente: I 295 (Centro Storico 231, Prati 64), II 155, III 76, V 74, VI 50, VII 62, XI 68,
XIV 75, XV 66; **nessun atto per IV, VIII, IX, X, XII, XIII** (i gruppi Tiburtino, Tintoretto, Eur,
Mare, Monteverde, Aurelio non pubblicano su Atti Web né a maggio né a giugno). Il gazetteer
riconosce la zona solo nel 16% degli oggetti perché le vie non sono nel gazetteer: la
localizzazione a quartiere richiederebbe un dizionario di vie (non previsto dal metodo).

Conclusione provvisoria: sì, le categorie centrali contengono atti rilevanti per i quartieri.
Il contributo maggiore è DDS (avvisi di viabilità a livello di strada, 9 Municipi), un genere
diverso dalle delibere e vicino alle informazioni di servizio; GCD, AY, AZ, ACD e GCM contribuiscono
insieme circa 45 atti al mese con riferimento territoriale (12 + 21 + 5 + 4 + 3, M sull'oggetto);
SO, CPC, CPV, CID hanno rilevanza bassa o non misurabile dall'oggetto.

## 5. Cosa cambia per il rapporto intermedio

- Il conteggio A2 di 1.426 vale per le **15 tipologie degli organi municipali** e resta corretto
  come tale (DMS ora 193: +2 pubblicazioni tardive). La copertura A2 e la resa del blocco
  Amministrazione restano **provvisorie**: con DDS e gli atti centrali con riferimento
  territoriale la resa lorda di giugno passerebbe da 1.426 a circa 2.390 (1.426 + 921 + ≈ 45, S),
  con una diversa composizione (avvisi di viabilità) e con sei Municipi senza DDS.
- La deduplicazione Amministrazione di §5 del rapporto non cambia (le convocazioni A1↔A2 sono
  municipali); DDS andrebbe confrontata con le informazioni di servizio di A1 (chiusure stradali)
  nell'approfondimento.
- Il rapporto e la scheda A2 del registro rimandano a questa nota e dichiarano le conclusioni
  provvisorie; il numero "17" è corretto in 16.

## 6. Approfondimento limitato proposto (decisione dell'owner)

Nessuna lettura integrale dell'archivio. Costo stimato 0 € (nessuna chiamata AI); tempo Operator
≈ 2 h in tutto; tutto riproducibile con i filtri di §2.

1. **DDS come voce separata "A2-DDS, discipline di traffico"** (già letta a livello di oggetto per
   giugno e maggio): aprire 10 PDF (seed `2026-06-DDS`) per verificare testo/scansione e leggere le
   date di validità; confrontare 30 atti con le informazioni di servizio A1 dello stesso Municipio
   per misurare i doppioni (chiusure stradali annunciate anche dal Municipio). Decide se DDS entra
   nel blocco Amministrazione o alimenta un genere "viabilità" per le pagine dei quartieri con
   9 Municipi coperti.
2. **GCD, AY, AZ, ACD, GCM: i 45 atti di giugno con riferimento territoriale** (già individuati):
   controllo umano degli oggetti sul campione (`A2_centrali_2026-06_items_compact_part1..2.csv`) e apertura
   di 5 PDF per la prova testo/scansione. Decide se entrano come "atti centrali con ricaduta
   territoriale" (≈ 45 al mese, S).
3. **CPC e CPV: 5 PDF ciascuno** (seed `2026-06-CPC`, `2026-06-CPV`) per vedere se gli ordini del
   giorno delle commissioni capitoline contengono punti di quartiere; oggi non è misurabile
   dall'oggetto.
4. **SO, CID, MCD, OCD**: nessun approfondimento; restano fuori con la motivazione di §3.
5. **Tipologie storiche e commissariali senza atti nel 2026**: escluse; ricontrollo solo se un
   Municipio viene commissariato (KMD, WMD, XMO).

Fino alla decisione, il registro e il rapporto contano A2 con i 15 codici municipali e dichiarano
il resto come "da decidere".

# Registro fonti — template (S2-01)

Una scheda per fonte, compilata secondo `docs/sources/SOURCE_STUDY_METHOD.md` (M-0.3). Nel
repository stanno solo aggregati e metriche; i dati per item e il campione di originali
stanno su Drive, `QN Hub / 20 Packages / Fonti 2026-06/` (metodo §4.2, DEC-104: loop di
sviluppo AI con i campioni fuori dal repository). Nessun testo integrale e nessun dato per item
nel repository; nei dati su Drive i nomi delle persone seguono DEC-105 (scritti quando sono
pertinenti al fatto; fino al 17 settembre 2026 la regola era «nessun nome di persona»). Ogni numero è marcato **M** (misurato), **S** (stimato) o **—** (mancante).

Stato: **livello 1 compilato** (A1, A2, C1–C6, E1, E2) con le letture del 15 settembre 2026,
10:24–11:06 Europe/Rome; evidenze e URL nel rapporto intermedio
`docs/sources/SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md`. Le raccomandazioni sono provvisorie
fino alla consegna finale (S2-05). Livello 2: E3, A3 e A4 compilate il 15 settembre (pomeriggio; A3 censita dopo l'apertura degli host, A4 con campione completato: `VIDEO_RICOGNIZIONE_2026-06.md`); R1: scheda da compilare.

| Campo | Valori ammessi / note |
|---|---|
| `id` | codice del metodo §2 (A1, A2, …, C1–C6, E1–E3, R1) |
| `blocco` | amministrazione · cronaca · eventi |
| `ente` | nome dell'ente o del portale |
| `sezione` | URL della pagina di elenco o del feed usato per il conteggio |
| `territorio` | città · Municipio N · quartiere |
| `argomenti` | tag liberi, pochi |
| `accesso` | web aperto · feed RSS · login · API |
| `formati` | HTML · PDF testo · PDF scansione · audio · video (più valori) |
| `riuso` | pagina licenza/termini trovata (sì/no), cosa dice in una riga, link; "da verificare (L11)" se manca |
| `mese` | 2026-06 (o 2026-05 con motivo) |
| `item_mese` | conteggio (M) — data e ora della lettura, paginazione completa sì/no |
| `frequenza` | item per settimana (M) |
| `ritardo_mediano_giorni` | fra fatto e pubblicazione, dove la data del fatto è nel testo (M o —) |
| `anticipo_eventi_giorni` | solo eventi: mediana fra pubblicazione e data dell'evento (M) |
| `eventi_futuri_30gg` | solo eventi: eventi con data nei 30 giorni dalla lettura (M) |
| `quota_toponimo` | % item con toponimo (M) |
| `quota_zona` | % item assegnabili deterministicamente a una delle 89 zone (M) |
| `quota_municipio` | % item assegnabili almeno al Municipio (M) |
| `duplicati` | % item già pubblicati da un'altra fonte del blocco; intervallo min–max se ci sono dubbi (M o S con n del campione) |
| `contributo_unico` | % item non presenti altrove (M o S) |
| `estrazione` | esito della prova: testo ottenuto sì/no; qualità leggibile / con errori / inutilizzabile |
| `costo_item` | tempo e costo per item dalla prova (M) |
| `intervento_umano` | minuti per item prevedibili (S) |
| `raccomandazione` | usare · integrare · riserva · escludere, con la ragione e la condizione che la cambierebbe |
| `drive` | link alla cartella dei dati per item e del campione |

## Schede

Drive per tutte le schede: `QN Hub / 20 Packages / Fonti 2026-06/`
(https://drive.google.com/drive/folders/1JQYkyES0zAGBNtiekXkVgWCS0Ee1RrIa). Frequenza = item
del mese / 4,29 settimane. Rapporto = `docs/sources/SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md`.

### A1 — Roma Capitale, portale istituzionale: notizie e informazioni di servizio dei Municipi

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Roma Capitale, portale istituzionale (`www.comune.roma.it`) |
| `sezione` | `https://www.comune.roma.it/web/it/notizie.page?mun=municipio_<n>&pagina=N` e `https://www.comune.roma.it/web/it/informazioni-di-servizio.page?mun=municipio_<n>&pagina=N` (15 filtri più `intermunicipale`) |
| `territorio` | Municipio (tag o filtro del portale); quartiere quando il testo lo cita |
| `argomenti` | eventi e attività gratuite, sociale, cultura, scuola, anagrafe, verde e viabilità; convocazioni di Consiglio e Giunta fra le informazioni di servizio |
| `accesso` | web aperto |
| `formati` | HTML |
| `riuso` | pagina trovata: sì, `https://www.comune.roma.it/web/it/note-legali.page`: copyright di Roma Capitale, nessuna licenza di riuso; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **365** (M): 135 notizie + 230 informazioni di servizio; lettura 15 settembre 2026 10:54; paginazione completa sì |
| `frequenza` | 85,2 per settimana (M) |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 62,5% (M; notizie 82,2%, informazioni di servizio 50,9%) |
| `quota_zona` | 32,9% dal testo, 37,8% con il titolo (M) |
| `quota_municipio` | 100% (M, dal portale) |
| `duplicati` | 35 avvisi di convocazione con gemello certo in A2 e 12 dubbi su 365 (9,6–12,9%, M per la classe delle convocazioni); 0 su 60 nel campione del resto (S, seed `2026-06-A1xA2`) |
| `contributo_unico` | 87–90% (318–330 item; M/S come sopra) |
| `estrazione` | testo ottenuto sì per tutti i 365; leggibile dopo la correzione del markup degli avvisi e della codifica (rapporto §6) |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | 1–2 min per item (S) |
| `raccomandazione` | usare: volume e Municipio certo; cambierebbe con un esito negativo di L11 |
| `drive` | `A1_2026-06_items_compact.csv`, `A1_A2_convocazioni_pairs_compact.csv`, `A1xA2_campione60_compact.csv` |

### A2 — Atti Web (Delibere e Atti), Municipi

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Roma Capitale, Delibere e Atti Web |
| `sezione` | `https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/` (API `data/filtro-dati!cerca.action`, filtro per tipologia e data di repertorio); 15 tipologie degli organi municipali su 48: tabella completa e categorie centrali in `docs/sources/A2_ATTIWEB_TIPOLOGIE.md` |
| `territorio` | Municipio (struttura dell'atto), tutti i 15 |
| `argomenti` | delibere e atti politici (208), convocazioni di Consiglio e Commissioni (571), verbali (456), determinazioni dirigenziali (191) |
| `accesso` | web aperto, API JSON non documentata |
| `formati` | PDF testo (10 su 18 provati), PDF scansione (8 su 18) |
| `riuso` | come A1 (stesso portale): da verificare (L11) |
| `mese` | 2026-06 (data di repertorio: il portale non espone la data di pubblicazione) |
| `item_mese` | **1.426** (M, 15 tipologie municipali); lettura 15 settembre 2026 10:42; paginazione completa sì (totale API = letti); alle 12:10 DMS 193 invece di 191 (pubblicazioni tardive). Fuori conteggio, da decidere: DDS 921 (discipline di traffico della Polizia Locale, 9 Municipi) e ≈ 45 atti centrali con riferimento territoriale |
| `frequenza` | 332,7 per settimana (M) |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 12,2% nell'oggetto (M) |
| `quota_zona` | 8,6% nell'oggetto (M) |
| `quota_municipio` | 100% (M, dalla struttura) |
| `duplicati` | 35 atti di convocazione con gemello certo in A1 e 12 dubbi su 1.426 (2,5–3,3%, M per la classe); 0 nel campione del resto (S) |
| `contributo_unico` | 96,7–97,5% (M/S) |
| `estrazione` | prova T2 parziale: 18 PDF, testo ottenuto in 10, leggibile; 8 scansioni inutilizzabili senza OCR (rapporto §6). Campione di 120 PDF (15 settembre, 8 per Municipio, seed `2026-06-A2-pdf`): 69 testuali e 51 scansioni (M), 332 pagine di cui 114 scansionate; le scansioni dipendono dal Municipio (III, IV, VI, VIII, IX, XI, XIII: 50 su 57), non dalla tipologia. OCR locale a 0 €: Tesseract 5.3.4 con lingua italiana (dai repository di sistema, installato il 15 settembre sera) 2,9 s a pagina a 300 dpi con spaziatura conservata; RapidOCR (PyPI) 5,3 s a pagina, perde spazi e righe nelle pagine dense; accordo fra i due su 5 pagine: 63–97% delle parole di Tesseract ritrovate, media 80% (`ocr_confronto_tesseract_rapidocr.json`) |
| `costo_item` | 0,00 €; meno di 2 s per PDF (M) |
| `intervento_umano` | 3–5 min per atto testuale, oltre 10 min per scansione senza OCR (S) |
| `raccomandazione` | **provvisoria**: usare come fonte di record degli atti municipali; perimetro sulle categorie centrali da decidere (`docs/sources/A2_ATTIWEB_TIPOLOGIE.md` §6, approfondimento §7: DDS coerenti con il Municipio del gruppo 10 su 10, circa 20 possibili notizie al mese dagli atti centrali); cambierebbe se l'OCR delle scansioni risultasse inutilizzabile (T2 da completare) |
| `drive` | `A2_2026-06_items_compact_part1..3.csv`; categorie centrali: `A2_DDS_2026-06_items_compact_part1..4.csv` (nel repository in due parti, `handoff_data/…_part1..2.csv`), `A2_centrali_2026-06_items_compact_part1..2.csv`; campione di 120 PDF (testo/scansione, pagine): `A2_pdf_campione120.csv`, `summary_A2_pdf_campione120.json` |

### C1 — Questura di Roma, archivio comunicati

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Polizia di Stato, Questura di Roma |
| `sezione` | `https://questure.poliziadistato.it/it/Roma/archivio/category/5730dc9d86cad683338531/<p>/` (giugno = pagine 17–25) |
| `territorio` | città e provincia; quartiere nel 27% |
| `argomenti` | arresti, sequestri, controlli, spaccio |
| `accesso` | web aperto |
| `formati` | HTML |
| `riuso` | piè di pagina con licenza CC BY-NC-ND 2.5 collegata a `www.poliziadistato.it`, pagina non leggibile dall'ambiente; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **79** (M); lettura 15 settembre 2026 10:34; paginazione completa sì |
| `frequenza` | 18,4 per settimana (M) |
| `ritardo_mediano_giorni` | 1 (M, n=10; 69 item senza data del fatto) |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 81,0% (M) |
| `quota_zona` | 26,6% (M) |
| `quota_municipio` | 27,8% (M) |
| `duplicati` | 0 certi, 1 dubbio (con C2) su 79: 0–1,3% (M, intero mese) |
| `contributo_unico` | 98,7–100% (M) |
| `estrazione` | testo ottenuto sì (79/79), leggibile; nomi di persona nel 62% (euristica). Lettura del 15 settembre; alla raccolta del Report 1 (17–18 settembre) 67 comunicati su 79 erano serviti come pagina «Accesso negato» con codice 200: 12 leggibili (`RICOSTRUZIONE_2026-06_REPORT1.md` §4), valore che prevale |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | 1–2 min per item (S) |
| `raccomandazione` | usare; cambierebbe se la licenza BY-NC-ND fosse confermata per i testi (L11) |
| `drive` | `C1_2026-06_items.csv`, `cronaca_dedup_campione.csv` |

### C2 — Carabinieri, comunicati stampa (Roma e provincia)

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Arma dei Carabinieri, Comando Provinciale di Roma |
| `sezione` | `https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa?d=202606` (+ `!page/page/2..8`); filtro Roma = fonte "Comando Provinciale di Roma" o luogo "(RM)" |
| `territorio` | città e provincia; quartiere nel 30% |
| `argomenti` | arresti, spaccio, controlli |
| `accesso` | web aperto |
| `formati` | HTML |
| `riuso` | pagina "Note legali" trovata: licenza SIAE del sito, nessuna clausola di riuso dei comunicati; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **20** su 151 nazionali (M); lettura 15 settembre 2026 10:36; paginazione completa sì |
| `frequenza` | 4,7 per settimana (M) |
| `ritardo_mediano_giorni` | 1 (M, n=11 su 20) |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 65,0% (M) |
| `quota_zona` | 30,0% (M) |
| `quota_municipio` | 30,0% (M) |
| `duplicati` | 0 certi, 1 dubbio (con C1) su 20: 0–5% (M) |
| `contributo_unico` | 95–100% (M) |
| `estrazione` | testo ottenuto sì (20/20), leggibile; timestamp completo di pubblicazione disponibile; nomi nel 70%. Lettura del 15 settembre dalle pagine di elenco; alla raccolta del Report 1 l'URL del singolo comunicato rimandava alla pagina-vetrina: 0 leggibili (`RICOSTRUZIONE_2026-06_REPORT1.md` §4), valore che prevale |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | 1–2 min per item (S) |
| `raccomandazione` | integrare; cambierebbe con un volume o una localizzazione maggiori |
| `drive` | `C2_2026-06_items.csv` |

### C3 — Procura di Roma, news e comunicati

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Procura della Repubblica di Roma |
| `sezione` | `https://procura-roma.giustizia.it/it/news_e_comunicati.page?frame5_item=1..5` |
| `territorio` | città |
| `argomenti` | circolari e modalità di servizio (21 su 22), 1 comunicato |
| `accesso` | web aperto |
| `formati` | HTML, PDF allegati (non provati) |
| `riuso` | pagina trovata: sì, `https://procura-roma.giustizia.it/it/note_legali.page`: solo uso personale, riproduzione con citazione della fonte, vietato l'uso commerciale; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **0** (M); 22 item in archivio dal 2017, 4 nel 2026; lettura 15 settembre 2026 10:32; paginazione completa sì |
| `frequenza` | 0 (M) |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — (nessun item) |
| `quota_zona` | — |
| `quota_municipio` | — |
| `duplicati` | — |
| `contributo_unico` | — |
| `estrazione` | non provata (nessun item del mese) |
| `costo_item` | — |
| `intervento_umano` | — |
| `raccomandazione` | escludere dalla Cronaca; cambierebbe con comunicati regolari |
| `drive` | — |

### C4 — Vigili del Fuoco, Comando di Roma

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Corpo Nazionale dei Vigili del Fuoco, Comando di Roma |
| `sezione` | `https://www.vigilfuoco.it/comando-vvf-roma/notizie-dal-territorio?provincia=244&data[min]=2026-06-01&data[max]=2026-06-30` (RSS disponibile) |
| `territorio` | città e provincia |
| `argomenti` | incendi, soccorsi, interventi |
| `accesso` | web aperto, feed RSS |
| `formati` | HTML |
| `riuso` | pagina trovata: sì, `https://www.vigilfuoco.it/note-legali`: **CC BY 4.0** con citazione della fonte |
| `mese` | 2026-06 |
| `item_mese` | **8** (M); lettura 15 settembre 2026 10:32; paginazione completa sì (una pagina) |
| `frequenza` | 1,9 per settimana (M) |
| `ritardo_mediano_giorni` | 0 (M, n=5 su 8) |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 37,5% (M) |
| `quota_zona` | 25,0% (M) |
| `quota_municipio` | 25,0% (M) |
| `duplicati` | 0 su 8 (M) |
| `contributo_unico` | 100% (M) |
| `estrazione` | testo ottenuto sì (8/8), leggibile |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | 1–2 min per item (S) |
| `raccomandazione` | integrare (licenza chiara); cambierebbe con un volume maggiore |
| `drive` | `C4_C5_2026-06_items.csv` |

### C5 — Polizia Locale di Roma Capitale, notizie

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Roma Capitale, Corpo di Polizia Locale (portale istituzionale, filtro per struttura) |
| `sezione` | `https://www.comune.roma.it/web/it/notizie.page?struttura=str_sg&pagina=1..6` |
| `territorio` | città |
| `argomenti` | controlli, viabilità, comunicazioni del Corpo |
| `accesso` | web aperto |
| `formati` | HTML |
| `riuso` | come A1: da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **2** (M); 53 in archivio 2018–2026; lettura 15 settembre 2026 10:49; paginazione completa sì |
| `frequenza` | 0,5 per settimana (M) |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | 0% (M) |
| `quota_zona` | 0% (M) |
| `quota_municipio` | 0% (M) |
| `duplicati` | 0 su 2 (M) |
| `contributo_unico` | 100% (M) |
| `estrazione` | testo ottenuto sì (2/2), leggibile |
| `costo_item` | 0,00 € (M) |
| `intervento_umano` | 1–2 min per item (S) |
| `raccomandazione` | riserva, da leggere come filtro di A1; cambierebbe con un volume maggiore |
| `drive` | `C4_C5_2026-06_items.csv` |

### C6 — Guardia di Finanza, Comando Regionale Lazio / Comando Provinciale Roma

| Campo | Valore |
|---|---|
| `blocco` | cronaca |
| `ente` | Guardia di Finanza |
| `sezione` | `https://www.gdf.gov.it/it/gdf-comunica/notizie-ed-eventi/comunicati-stampa/territorio/comando-regionale-lazio/` (elenco vuoto senza JavaScript: conteggio dalla REST API `https://www.gdf.gov.it/++api++/@search` con `reparti_correlati` del Comando Provinciale Roma) |
| `territorio` | città e regione |
| `argomenti` | sequestri, frodi, controlli economici |
| `accesso` | web aperto, API Plone |
| `formati` | HTML |
| `riuso` | pagina trovata: sì, `https://www.gdf.gov.it/it/note-legali`: copyright su marchi e segni distintivi, nessuna clausola sul riuso dei comunicati; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **0** Comando Provinciale Roma (M); 3 nel Lazio; Roma 38 nel 2026 e 84 in archivio; lettura 15 settembre 2026 10:50; paginazione completa sì (API) |
| `frequenza` | 0 a giugno; ≈ 3 al mese nel 2026 (S) |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — (nessun item del mese) |
| `quota_zona` | — |
| `quota_municipio` | — |
| `duplicati` | — |
| `contributo_unico` | — |
| `estrazione` | elenco e metadati ottenuti via API; testo non provato (nessun item del mese) |
| `costo_item` | — |
| `intervento_umano` | — |
| `raccomandazione` | riserva; cambierebbe con una frequenza stabile e comunicati localizzabili |
| `drive` | — |

### E1 — 060608, manifestazioni ed eventi

| Campo | Valore |
|---|---|
| `blocco` | eventi |
| `ente` | Roma Capitale / Zètema, portale 060608 |
| `sezione` | `https://060608.comune.roma.it/eventi` e `…/rss`: applicazione Next.js che carica elenco e feed da `https://ws.comune.roma.it/060608/api/` |
| `territorio` | città e Municipi (da verificare) |
| `argomenti` | eventi, mostre, spettacoli |
| `accesso` | web aperto; l'host dei dati `ws.comune.roma.it` non era consentito la mattina del 15 settembre (**accesso mancante** nel rapporto §2, §11); alle 17:26 risponde: API `POST /060608/api/public/entita/ricerca?page=N` (JSON con categoria, date, indirizzo, coordinate e zona toponomastica; 57.132 entità di tutte le categorie), filtri per categoria e calendario da individuare (quattro formati provati senza risultati) |
| `formati` | HTML, RSS (non letti) |
| `riuso` | link "Disclaimer" nel piè di pagina, non letto; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | — (accesso mancante; lettura tentata 15 settembre 2026 10:24–10:29) |
| `frequenza` | — |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | — |
| `eventi_futuri_30gg` | — |
| `quota_toponimo` | — |
| `quota_zona` | — |
| `quota_municipio` | — |
| `duplicati` | — |
| `contributo_unico` | — |
| `estrazione` | non eseguibile |
| `costo_item` | — |
| `intervento_umano` | — |
| `raccomandazione` | host ora raggiungibile: ripetere la lettura con i filtri di categoria e data (1–2 ore, 0 €) prima di decidere; fino ad allora coprire con E2 ed E3 |
| `drive` | — |

### E2 — culture.roma.it (Roma Culture)

| Campo | Valore |
|---|---|
| `blocco` | eventi |
| `ente` | Roma Capitale, Dipartimento Attività Culturali (culture.roma.it) |
| `sezione` | `https://culture.roma.it/wp-json/wp/v2/event_calendar?per_page=100&page=N&after=2026-06-01T00:00:00&before=2026-07-01T00:00:00` più la pagina di ogni appuntamento (date, luogo, Municipio) |
| `territorio` | Municipio (tassonomia del portale) e luogo con indirizzo |
| `argomenti` | cultura, spettacolo, biblioteche, mostre; 293 su 407 gratuiti |
| `accesso` | web aperto, REST WordPress |
| `formati` | HTML, JSON |
| `riuso` | pagina trovata: `https://culture.roma.it/esclusione-dalle-responsabilita/`, solo esclusione di responsabilità, nessuna clausola di riuso; da verificare (L11) |
| `mese` | 2026-06 |
| `item_mese` | **407** (M); lettura 15 settembre 2026 10:37; paginazione completa sì (`X-WP-Total` 407) |
| `frequenza` | 95,0 per settimana (M) |
| `ritardo_mediano_giorni` | n/a |
| `anticipo_eventi_giorni` | 17 (M; quartili 9–30; 6 pubblicati dopo l'evento) |
| `eventi_futuri_30gg` | 189 con data fra il 15 settembre e il 15 ottobre 2026 (M, limite inferiore: fra i 917 pubblicati dal 1° luglio; lettura 11:05) |
| `quota_toponimo` | 37,8% (M) |
| `quota_zona` | 30,0% (M) |
| `quota_municipio` | 97,5% (M, tassonomia del portale; 10 senza) |
| `duplicati` | — (unica fonte Eventi leggibile: deduplicazione non eseguibile) |
| `contributo_unico` | — |
| `estrazione` | testo e dati strutturati ottenuti sì (407/407), leggibili |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | meno di 1 min per item (S) |
| `raccomandazione` | usare; gap per Municipio (XV 0, XII 2, IX 7 a giugno) da coprire con E1/E3 |
| `drive` | `E2_2026-06_items.csv`, `E2_futuri_30gg.csv` |

### E3 — Roma Capitale, portale istituzionale: agenda eventi (livello 2)

| Campo | Valore |
|---|---|
| `blocco` | eventi |
| `ente` | Roma Capitale, portale istituzionale (`www.comune.roma.it`), sezione "Tutti gli eventi" |
| `sezione` | `https://www.comune.roma.it/web/it/eventi.page?pagina=N` (10 per pagina, ordinata per data di pubblicazione; faccette `mun=municipio_<n>`, `temat=`, `struttura=`); scheda evento con `search:municipio`, `search:periodo`, `search:data`, `search:tematica` |
| `territorio` | Municipio (tag del portale, 66% degli item); quartiere quando il testo lo cita |
| `argomenti` | cultura, musica ("Roma in musica 2026": 66 su 104), mostre, cinema, teatro |
| `accesso` | web aperto |
| `formati` | HTML |
| `riuso` | come A1 (stesso portale): da verificare (L11) |
| `mese` | 2026-06 (data di pubblicazione `search:data`) |
| `item_mese` | **104** (M); lettura 15 settembre 2026 12:25 (elenco) e 12:40 (schede); paginazione completa sì (pagine 1–19) |
| `frequenza` | 24,3 per settimana (M) |
| `ritardo_mediano_giorni` | n/a |
| `anticipo_eventi_giorni` | — (periodo dell'evento in testo libero: non calcolato) |
| `eventi_futuri_30gg` | 36 con periodo fra il 15 settembre e il 15 ottobre 2026 (S: parsing del testo libero, fra i 190 appuntamenti pubblicati dal 26 maggio; 32 senza tag di Municipio; limite inferiore) |
| `quota_toponimo` | 52,9% (M) |
| `quota_zona` | 35,6% (M) |
| `quota_municipio` | 66,3% (M, tag del portale; 35 senza) |
| `duplicati` | 7 certi e 1 dubbio con E2 su 104 (6,7–7,7%; M per titolo normalizzato sull'intero mese, limite inferiore) |
| `contributo_unico` | 92–93% (M, limite superiore) |
| `estrazione` | testo e metadati ottenuti sì (104/104), leggibili |
| `costo_item` | 0,00 €; 1–3 s per pagina (M) |
| `intervento_umano` | meno di 1 min per item; il periodo va normalizzato a mano o con regole (S) |
| `raccomandazione` | integrare: seconda fonte Eventi a costo zero; cambierebbe se E1 diventasse leggibile con dati strutturati |
| `drive` | `E3_2026-06_items.csv`, `eventi_E3xE2_candidati.csv` |

### A3 — RomaTV, streaming delle commissioni e dei Consigli (livello 2)

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Roma Capitale, Web TV "RomaTV" (`streaming.comune.roma.it`, applicazione "Mediaportal" su piattaforma esterna; API `api-ovp.streamcloud.it/garavot/ac104`) |
| `sezione` | cataloghi per Municipio (14: tutti tranne il I, che usa YouTube) più "Commissioni Capitoline" e "Assemblee Capitoline"; ricerca `contents/search_frontend` con filtro per catalogo e ordinamento per data di seduta |
| `territorio` | Municipio (catalogo, 100%); quartiere solo dal parlato |
| `argomenti` | commissioni municipali (305 a giugno), Consigli municipali (86), Commissioni Capitoline (75, 16 organi), Assemblee (7) |
| `accesso` | web aperto, API senza login; **fino alle 16:00 del 15 settembre bloccato dal proxy** (host `*.streamcloud.it`), consentito dall'owner alle 16:02; media (`ac104mp.streamcloud.it`, `ovp2-live.akamaized.net`) consentiti dalle 17:09: stream HLS audio-only (48 kbps dichiarati) cifrato AES-128 con chiave sull'host API, scaricabile a segmenti (≈ 45–50 MB e ≈ 5–6 minuti di rete per ora di audio, M su 2 registrazioni; durata dell'audio uguale a quella del catalogo) |
| `formati` | video (stream), metadati JSON (titolo, descrizione, data di seduta, data di pubblicazione, durata, organo per le commissioni capitoline), trascrizione automatica WebVTT per i Consigli municipali |
| `riuso` | condizioni del portale non lette (involucro non renderizzabile qui): da verificare (L11) |
| `mese` | 2026-06 (data di seduta `referenceDate`; la data di pubblicazione `insertDate` è disponibile per tutte) |
| `item_mese` | **496** (M): Municipi 414 (II 67, III 65, VIII 58, XII 58, XV 45, XI 40, V 39, X 16, IX 12, VII 6, VI 5, IV 2, XIII 1, XIV 0), Commissioni Capitoline 75, Assemblee 7; 404,8 ore; lettura 15 settembre 2026 16:10 (30 richieste); 38 voci pubblicate a giugno su sedute di altri mesi non contate |
| `frequenza` | 115 registrazioni per settimana (M); sedute spesso spezzate in più video |
| `ritardo_mediano_giorni` | **0** (M, 496 voci): 302 entro 1 giorno, 387 entro 7, massimo 94 |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — (dal parlato: toponimi presenti in 7 trascrizioni su 7 lette, deformati dall'ASR) |
| `quota_zona` | — |
| `quota_municipio` | 100% (M, catalogo) |
| `duplicati` | con A4: i Municipi V e IX pubblicano su entrambe le piattaforme (V 39 su RomaTV e 9 su YouTube; IX 12 e 37): stesse sedute, non misurate voce per voce; con A2: stessa seduta del verbale, non duplicato |
| `contributo_unico` | alto (S) per i 7 Municipi senza YouTube e per le Commissioni Capitoline: unica registrazione pubblica; 18 possibili notizie dai 7 Consigli letti (5 senza verbale in Atti Web), nessuna in A1 oltre agli ordini del giorno delle convocazioni (1 sovrapposizione parziale) |
| `estrazione` | metadati per tutte le voci; testo solo dalle 82 trascrizioni della piattaforma (Consigli): blocchi WebVTT di ~10 parole, 68–122 parole al minuto, nomi e toponimi deformati, appelli nominali fino a un quarto del testo; il JSON del riconoscimento (parola, tempi, confidenza) è leggibile dall'host media: confidenza media per parola 0,897 (mediana 0,918, quota sotto 0,7 in media 5,1%, 82 Consigli, 418.151 parole, M; `A3_speech_confidenza_giugno.csv`); commissioni senza testo, audio scaricabile |
| `costo_item` | 0,00 € per metadati e trascrizioni esistenti; tempo macchina 1–3 s per pagina di 100 voci |
| `intervento_umano` | 10–25 minuti per seduta con trascrizione (S; di più per i Consigli lunghi con libera discussione); per le commissioni non stimabile senza audio |
| `raccomandazione` | fonte candidata per i Municipi senza YouTube e per le Commissioni Capitoline (metadati completi, ritardo zero); il testo delle commissioni dipende dall'audio (host) e da T1; nessuna integrazione approvata automaticamente |
| `drive` | `A3_romatv_giugno2026_censimento_part1..6.csv`, `A3_campione_selezione.csv`, `summary_A3_romatv.json`, `A3_romatv_accesso_2026-06.csv` (stato precedente) |

### A4 — Canali YouTube dei Municipi (livello 2)

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Municipi I (`MUNICIPIO ROMA I CENTRO`), V (`Municipio Roma V`), IX (`Municipio Roma Nove`), XIV (`Municipio Roma XIV Monte Mario`, senza sedute); Roma Capitale (dirette dell'Assemblea Capitolina, fuori perimetro) |
| `sezione` | elenchi `videos`/`streams` dei canali (identificativi in `A4_canali_youtube_stato.csv`) |
| `territorio` | Municipio (canale, 100%); quartiere solo dal parlato (trascrizione) |
| `argomenti` | commissioni municipali (mobilità e lavori pubblici, urbanistica e ambiente, sociale, scuola e cultura, commercio, trasparenza e bilancio), Consigli |
| `accesso` | web aperto per elenchi e metadati; media bloccati (`googlevideo.com`); controllo anti-bot di YouTube sull'IP di uscita dopo circa 20 letture per video in 5 minuti (§2 e §7 della nota) |
| `formati` | video; sottotitoli automatici italiani (json3) per 22 video su 22 letti; nessun sottotitolo redatto; descrizione con ordine del giorno in parte dei video |
| `riuso` | termini di YouTube; contenuti istituzionali: da verificare (L11) |
| `mese` | 2026-06 (data della seduta nel titolo; data di pubblicazione misurata per 12 video su 131) |
| `item_mese` | **131** (M): 107 commissioni municipali (I 64, IX 34, V 9), 16 Consigli municipali (I 13, IX 3), 8 dirette dell'Assemblea Capitolina; 135,5 ore, di cui 82,1 di commissioni; lettura 15 settembre 2026 15:06–15:12 (elenchi) |
| `frequenza` | 25 commissioni per settimana sui tre canali (M); Municipio V muto dopo il 12 giugno |
| `ritardo_mediano_giorni` | 0 per il Municipio I e 1 per il IX sugli ultimi 15 video di ciascun canale (feed RSS, settembre, M); a giugno letto per 12 video (9 del V entro 1 giorno dal feed RSS, uno del I lo stesso giorno, uno del IX dopo 5 giorni, uno del IX dopo 62 giorni): stima S per il mese |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — (dal parlato: toponimi presenti in 15 trascrizioni su 16 lette, deformati dall'ASR; assenti nella seduta di analisi delle determine) |
| `quota_zona` | — |
| `quota_municipio` | 100% (M, canale) |
| `duplicati` | con A2: 101 commissioni su 107 hanno un verbale dello stesso giorno nello stesso Municipio (M), 51 della stessa commissione (28 certi per link, 23 per nome: stima, 2 errori su 4 verificati); il video è il contenuto, il verbale l'atto: non sono duplicati ma la stessa seduta |
| `contributo_unico` | alto (S): nelle 15 sedute di giugno analizzate 26 possibili notizie, 25 assenti da A1 e dalla Cronaca; sovrapposizione con A1 in 1 caso su 26; tre pareri capitolini (norme tecniche, librerie, animali) attraversano più Municipi nelle stesse settimane |
| `estrazione` | testo dalle trascrizioni automatiche (15 del campione più 1 di luglio scaricate e lette), 112–140 parole al minuto (13 in una seduta con 33 minuti di sospensione); nomi propri e toponimi inaffidabili |
| `costo_item` | 0,00 € per il testo; tempo macchina 10–40 s per video con esito intermittente |
| `intervento_umano` | 10–15 minuti per seduta per lettura, confronto con gli atti e verifica dei nomi (S) |
| `raccomandazione` | fonte candidata per i Municipi I e IX, subordinata alla misura della data di pubblicazione e alla verifica dei nomi; V parziale; nessuna integrazione approvata automaticamente |
| `drive` | `A4_youtube_giugno2026_censimento.csv` (in due parti), `A4_canali_youtube_stato.csv`, `A4_campione_selezione.csv`, `summary_A4_youtube.json`, `A4_rss_ritardo_pubblicazione_2026-09-15.csv` |

## Canali della prova della Cronaca (DEC-108, ottobre 2026)

DEC-108 ammette la stampa come fonte citata e tocca questo registro: le schede qui sopra restano
quelle dello studio di settembre; i canali usati dalla prova della Cronaca (`tools/cronaca-prova/`,
README passi 1, 8 e 9) sono questi. Robots.txt, riserve TDM e barriere osservate, testata per
testata, stanno nel sondaggio di `CRONACA_PROCESSO_2026-10.md` §5.2; qui il canale e il limite.

| Fonte | Canale usato | Che cosa si prende | Limite |
|---|---|---|---|
| C1–C6 (Questura, Carabinieri, Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza) | pagine di elenco e comunicati (`fonti_ufficiali.py`) | comunicato intero, nella cartella di lavoro | una richiesta ogni 4 s alla Questura, ogni 2 s agli altri; pagine di blocco servite con 200 contate come rifiuto; stop dopo cinque rifiuti di fila |
| Abitare a Roma, VignaClaraBlog, Dire | API pubblica WordPress del sito (`censimento.py`) | titolo, data, categorie, link | una richiesta al secondo, user agent dichiarato; solo metadati |
| Roma Daily News, Il Faro Online | sitemap (l'API è esclusa dal robots.txt) | titolo, data, link | come sopra |
| Il Tempo | sitemap giornaliere | titolo, data, sezione, link | come sopra; solo i giorni del mese |
| Testate che escludono gli agenti AI (RomaToday, Il Messaggero, Corriere Roma, Repubblica Roma, Leggo, ANSA, Agenzia Nova, Today.it e le altre di §5.2) | file grezzi di GDELT, indice aperto (`gdelt_titoli.py`) | titolo, link e ora dall'indice; la pagina dell'articolo non si apre mai | i file da 15 minuti si scaricano uno a uno; l'API di ricerca di GDELT non si usa |
| Testi degli articoli delle testate aperte | pagina dell'articolo (`testi_aperti.py`) | testo, nella cartella di lavoro | solo per le notizie che il titolo non localizza; tetto `QN_MAX_TESTI` per esecuzione |

Nel repository restano i conteggi (`tools/cronaca-prova/runs/`); titoli, testi e link per item
stanno nella cartella di lavoro e su Drive (DEC-102, DEC-104).

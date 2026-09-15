# Registro fonti — template (S2-01)

Una scheda per fonte, compilata secondo `docs/sources/SOURCE_STUDY_METHOD.md` (M-0.3). Nel
repository stanno solo aggregati e metriche; i dati per item e il campione di originali
stanno su Drive, `QN Hub / 20 Packages / Fonti 2026-06/` (metodo §4.2, DEC-104: loop di
sviluppo AI con i campioni fuori dal repository). Nessun nome di persona, nessun testo
integrale. Ogni numero è marcato **M** (misurato), **S** (stimato) o **—** (mancante).

Stato: **livello 1 compilato** (A1, A2, C1–C6, E1, E2) con le letture del 15 settembre 2026,
10:24–11:06 Europe/Rome; evidenze e URL nel rapporto intermedio
`docs/sources/SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md`. Le raccomandazioni sono provvisorie
fino alla consegna finale (S2-05). Livello 2: E3, A3 e A4 compilate il 15 settembre (pomeriggio; A3 con accesso bloccato, A4 con campione in corso: `VIDEO_RICOGNIZIONE_2026-06.md`); R1: scheda da compilare.

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
| `estrazione` | prova T2 parziale: 18 PDF, testo ottenuto in 10, leggibile; 8 scansioni inutilizzabili senza OCR (rapporto §6) |
| `costo_item` | 0,00 €; meno di 2 s per PDF (M) |
| `intervento_umano` | 3–5 min per atto testuale, oltre 10 min per scansione senza OCR (S) |
| `raccomandazione` | **provvisoria**: usare come fonte di record degli atti municipali; perimetro sulle categorie centrali da decidere (`docs/sources/A2_ATTIWEB_TIPOLOGIE.md` §6, approfondimento §7: DDS coerenti con il Municipio del gruppo 10 su 10, circa 20 possibili notizie al mese dagli atti centrali); cambierebbe se l'OCR delle scansioni risultasse inutilizzabile (T2 da completare) |
| `drive` | `A2_2026-06_items_compact_part1..3.csv`; categorie centrali: `A2_DDS_2026-06_items_compact_part1..4.csv`, `A2_centrali_2026-06_items_compact_part1..2.csv` |

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
| `estrazione` | testo ottenuto sì (79/79), leggibile; nomi di persona nel 62% (euristica) |
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
| `estrazione` | testo ottenuto sì (20/20), leggibile; timestamp completo di pubblicazione disponibile; nomi nel 70% |
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
| `accesso` | web aperto, ma l'host dei dati non è consentito dall'ambiente: **accesso mancante** (rapporto §2, §11) |
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
| `raccomandazione` | decisione dell'owner: consentire `ws.comune.roma.it` e ripetere la lettura; altrimenti escludere e coprire con E2 ed E3 |
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

### A3 — RomaTV, streaming delle commissioni (livello 2)

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Roma Capitale, Web TV "RomaTV" (`streaming.comune.roma.it`, applicazione "Mediaportal" su piattaforma esterna) |
| `sezione` | cataloghi per Municipio (II, III, VIII, X, XI, XII, XV) e catalogo delle Commissioni Capitoline: URL in `A3_romatv_accesso_2026-06.csv` (Drive); dirette `portal/watch/live/<id>` per i Municipi II e V |
| `territorio` | Municipio (catalogo); quartiere solo dal parlato |
| `argomenti` | sedute delle commissioni municipali e capitoline |
| `accesso` | **bloccato**: l'involucro HTML è raggiungibile, ma cataloghi, ricerche, identità e media sono su `api-ovp.streamcloud.it`, `identity-ovp.streamcloud.it`, `ac103mp.streamcloud.it` (CONNECT rifiutato dal proxy, 15 settembre 2026 15:00) |
| `formati` | video (stream), metadati JSON via API; il bundle espone un endpoint `timedmetadata/last_speechtotext` (trascrizioni automatiche possibili, non verificate) |
| `riuso` | — (condizioni non leggibili) |
| `mese` | 2026-06 |
| `item_mese` | **—** (accesso bloccato); *Next Step* dichiara 75–184 video per Municipio e 246 per le Commissioni Capitoline nel primo trimestre 2026 (dato dell'owner, non verificato) |
| `frequenza` | — |
| `ritardo_mediano_giorni` | — |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — |
| `quota_zona` | — |
| `quota_municipio` | — (100% atteso dal catalogo) |
| `duplicati` | — |
| `contributo_unico` | — |
| `estrazione` | non eseguibile |
| `costo_item` | — |
| `intervento_umano` | — |
| `raccomandazione` | da decidere dopo l'apertura degli host: senza cataloghi né media la fonte non è valutabile; copre 7 Municipi e le Commissioni Capitoline che non hanno altra registrazione pubblica |
| `drive` | `A3_romatv_accesso_2026-06.csv` |

### A4 — Canali YouTube dei Municipi (livello 2)

| Campo | Valore |
|---|---|
| `blocco` | amministrazione |
| `ente` | Municipi I (`MUNICIPIO ROMA I CENTRO`), V (`Municipio Roma V`), IX (`Municipio Roma Nove`), XIV (`Municipio Roma XIV Monte Mario`, senza sedute); Roma Capitale (dirette dell'Assemblea Capitolina, fuori perimetro) |
| `sezione` | elenchi `videos`/`streams` dei canali (identificativi in `A4_canali_youtube_stato.csv`) |
| `territorio` | Municipio (canale, 100%); quartiere solo dal parlato (trascrizione) |
| `argomenti` | commissioni municipali (mobilità e lavori pubblici, urbanistica e ambiente, sociale, scuola e cultura, commercio, trasparenza e bilancio), Consigli |
| `accesso` | web aperto per elenchi e metadati; media bloccati (`googlevideo.com`); controllo anti-bot di YouTube sull'IP di uscita dopo circa 20 letture per video in 5 minuti (§2 e §7 della nota) |
| `formati` | video; sottotitoli automatici italiani (json3) per 12 video su 12 letti; nessun sottotitolo redatto; descrizione con ordine del giorno in parte dei video |
| `riuso` | termini di YouTube; contenuti istituzionali: da verificare (L11) |
| `mese` | 2026-06 (data della seduta nel titolo; data di pubblicazione misurata solo per 2 video) |
| `item_mese` | **131** (M): 107 commissioni municipali (I 64, IX 34, V 9), 16 Consigli municipali (I 13, IX 3), 8 dirette dell'Assemblea Capitolina; 135,5 ore, di cui 82,1 di commissioni; lettura 15 settembre 2026 15:06–15:12 (elenchi) |
| `frequenza` | 25 commissioni per settimana sui tre canali (M); Municipio V muto dopo il 12 giugno |
| `ritardo_mediano_giorni` | — (pubblicazione letta per 2 video: 0 e 62 giorni) |
| `anticipo_eventi_giorni` | n/a |
| `eventi_futuri_30gg` | n/a |
| `quota_toponimo` | — (dal parlato: toponimi presenti in 4 trascrizioni su 4 lette, deformati dall'ASR) |
| `quota_zona` | — |
| `quota_municipio` | 100% (M, canale) |
| `duplicati` | con A2: 101 commissioni su 107 hanno un verbale dello stesso giorno nello stesso Municipio (M), 51 della stessa commissione (28 certi per link, 23 per nome: stima, 1 errore su 3 verificati); il video è il contenuto, il verbale l'atto: non sono duplicati ma la stessa seduta |
| `contributo_unico` | alto (S): nelle 9 sedute di giugno analizzate 17 possibili notizie, 16 assenti da A1 e dalla Cronaca; sovrapposizione con A1 in 1 caso su 17 |
| `estrazione` | testo dalle trascrizioni automatiche (9 del campione più 1 di luglio scaricate e lette), 112–138 parole al minuto; nomi propri e toponimi inaffidabili |
| `costo_item` | 0,00 € per il testo; tempo macchina 10–40 s per video con esito intermittente |
| `intervento_umano` | 10–15 minuti per seduta per lettura, confronto con gli atti e verifica dei nomi (S) |
| `raccomandazione` | fonte candidata per i Municipi I e IX, subordinata alla misura della data di pubblicazione e alla verifica dei nomi; V parziale; nessuna integrazione approvata automaticamente |
| `drive` | `A4_youtube_giugno2026_censimento.csv`, `A4_canali_youtube_stato.csv`, `A4_campione_selezione.csv`, `summary_A4_youtube.json` |

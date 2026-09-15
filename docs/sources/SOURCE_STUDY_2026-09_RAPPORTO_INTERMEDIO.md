# Studio delle fonti — rapporto intermedio dopo il livello 1 (15 settembre 2026)

| Campo | Valore |
|---|---|
| Stato | **Rapporto intermedio** previsto dal metodo M-0.3 (§8.5) dopo la lettura del livello 1 (A1, A2, C1–C6, E1, E2). Non è la consegna finale (P0-S2-05): mancano il livello 2, la previsione dei costi con i tre scenari e le raccomandazioni definitive. Nessun controllo di Codex su questo rapporto (metodo §8.4: nessun ciclo intermedio salvo problemi sostanziali) |
| Metodo | `docs/sources/SOURCE_STUDY_METHOD.md` M-0.3, applicato senza modifiche; le osservazioni sul metodo emerse dai dati sono in §10 come proposte, non applicate |
| Sessione | 15 settembre 2026, Operator: 10:24–12:00 circa (Europe/Rome), letture delle fonti 10:24–11:06; pomeriggio 12:05–13:00 circa: verifica A2 e lettura di E3 (livello 2) |
| Dati per item e campione | Drive `QN Hub / 20 Packages / Fonti 2026-06/` (https://drive.google.com/drive/folders/1JQYkyES0zAGBNtiekXkVgWCS0Ee1RrIa), un CSV per fonte, senza nomi di persona né testi integrali (metodo §4.2); indice nel `README_Fonti_2026-06.md` della cartella |
| Schede | `docs/sources/SOURCE_REGISTRY.md`, una scheda per fonte del livello 1 |
| Verifica A2 | `docs/sources/A2_ATTIWEB_TIPOLOGIE.md` (15 settembre, pomeriggio, su richiesta dell'owner): tabella delle 48 tipologie, filtri, percorso ai 1.426 atti, esempi delle categorie centrali; §7 approfondimento circoscritto (31 PDF letti, 46 candidati classificati). **Le conclusioni sulla copertura di A2 sono provvisorie** (§3, §5, §10) |
| Video (A3, A4) | `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md` (15 settembre, dalle 14:55, su richiesta dell'owner): YouTube censito (131 registrazioni di giugno), RomaTV censito dopo l'apertura degli host (496), campione di 15 YouTube più 7 RomaTV, tutte lette (22 sedute di giugno più una di luglio): 44 possibili notizie, 1 sovrapposizione piena e 2 parziali con A1 |
| Spesa | 0,00 € in questa sessione; nessuna chiamata AI; `docs/sources/TRIAL_LEDGER.md` |
| Stato del dato | ogni numero è marcato **M** (misurato, con URL e ora della lettura), **S** (stimato, con l'ipotesi) o **—** (mancante) |

## 1. Esito in breve

- **Accesso**: tutti i domini del metodo §6 sono raggiungibili; un PDF di Atti Web è stato scaricato e letto; il feed di 060608 **non** è leggibile perché la pagina è un'applicazione Next.js che carica elenco e RSS da `ws.comune.roma.it`, host non consentito dall'ambiente. E1 è "accesso mancante" (§2).
- **Conteggi di giugno 2026 (M)**: A1 365 item (135 notizie + 230 informazioni di servizio); A2 1.426 atti delle 15 tipologie degli organi municipali (copertura provvisoria: le 33 tipologie restanti, fra cui 921 determinazioni di traffico della Polizia Locale, sono in `docs/sources/A2_ATTIWEB_TIPOLOGIE.md`); C1 79; C2 20 (su 151 nazionali); C3 0; C4 8; C5 2; C6 0 (Comando Provinciale di Roma; 3 nel Lazio); E2 407 appuntamenti pubblicati, 189 con data nei 30 giorni dalla lettura (limite inferiore). Dettaglio in §3.
- **Localizzazione (M)**: Municipio noto per il 100% di A1 e A2 (dal portale), per il 97,5% di E2 (tassonomia del portale), per il 25–30% della Cronaca (dal testo); zona deterministica per il 26–41% degli item con testo (§4).
- **Sovrapposizioni (M/S)**: Cronaca 0 duplicati certi e 1 dubbio su 109 item; Amministrazione 35 coppie certe e 12 dubbie fra avvisi di convocazione (A1) e atti di convocazione (A2), 0 su 60 nel campione del resto; Eventi non valutabile con una sola fonte leggibile (§5).
- **Formati**: HTML leggibile con parser locali per tutte le fonti lette; Atti Web è PDF, e 8 dei 18 PDF provati sono scansioni senza testo (§6). OCR non eseguito (nessuno strumento locale, AI ferma).
- **Blocchi**: `ws.comune.roma.it` (E1); `www.poliziadistato.it` (pagina della licenza della Questura); `developers.openai.com` (listino per il ledger). T1, T3, T4 e T5 restano ferme (§9, §11).
- **Livello 2**: serve, ma solo in parte: E3 letto il 15 settembre pomeriggio (104 appuntamenti a giugno, 66% con Municipio, 7 duplicati certi con E2), A3 e A4 limitati ai cataloghi finché le prove video sono ferme, R1 non necessario (§10).

## 2. Verifica dell'accesso (metodo §6)

Letture dall'ambiente Claude Code con `curl` attraverso il proxy dell'ambiente, 15 settembre 2026 dalle 10:24 (Europe/Rome). "CONNECT 403" è la risposta del proxy per un host fuori dall'elenco consentito.

| Dominio / risorsa | URL letto | Esito | Ora |
|---|---|---|---|
| `www.comune.roma.it` | `https://www.comune.roma.it/web/it/municipio-i.page` | 200, HTML 156 KB | 10:24 |
| `comune.roma.it` (apex) | `https://comune.roma.it/web/it/municipio-i.page` | redirect a `www`, 200 | 10:24 |
| `streaming.comune.roma.it` | `https://streaming.comune.roma.it/portal/` | 200 | 10:24 |
| `060608.comune.roma.it` | `https://060608.comune.roma.it/eventi` | 200, HTML 101 KB: applicazione Next.js, elenco vuoto senza le chiamate a `ws.comune.roma.it` | 10:24 |
| feed RSS 060608 | `https://060608.comune.roma.it/rss` | 200 ma `text/html` 69 KB (pagina applicativa, non XML); i feed sono serviti da `https://ws.comune.roma.it/060608/api/` | 10:25 |
| `ws.comune.roma.it` | API 060608 | **CONNECT 403** (host non consentito) | 10:29 |
| `www.060608.it` | `https://www.060608.it/` | **CONNECT 403** (dominio non richiesto in §6; ridondante) | 10:24 |
| `culture.roma.it` | `https://culture.roma.it/` | 200 | 10:24 |
| `questure.poliziadistato.it` | `https://questure.poliziadistato.it/it/Roma` | 200 | 10:24 |
| `www.carabinieri.it` | `…/in-vostro-aiuto/informazioni/comunicati-stampa` | 200 | 10:24 |
| `procura-roma.giustizia.it` | `…/it/news_e_comunicati.page` | 200 | 10:24 |
| `www.vigilfuoco.it` | `…/comando-vvf-roma/interventi-roma` | 200 | 10:24 |
| `www.gdf.gov.it` | `…/comunicati-stampa/territorio/comando-regionale-lazio/` | 200, 1,1 MB; elenco vuoto senza JavaScript, letto dalla REST API Plone `++api++/@search` | 10:24 |
| `www.youtube.com` | `https://www.youtube.com/` | 200 (solo verifica; A4 è livello 2) | 10:24 |
| `consiglio.regione.lazio.it`, `www.regione.lazio.it` | home | 200 (R1, riserva) | 10:24 |
| `pypi.org` | `https://pypi.org/simple/pypdf/` | 200; installati `pypdf`, `PyMuPDF` e `cffi` (senza `cffi` l'import di `pypdf` fallisce nell'ambiente) | 10:24 |
| PDF Atti Web | `https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/showPdfDoc?fun=deliberazioniAtti&par1=Q01E&par2=MTAxNjU=` | 200, 117.165 byte, testo estratto (§6) | 10:43 |
| `www.poliziadistato.it` | pagina della licenza collegata dal piè di pagina della Questura | **CONNECT 403** | 10:50 |
| `developers.openai.com` | listino prezzi (per il ledger) | non raggiungibile | 11:00 |
| controllo | `https://example.com/` | CONNECT 403 (atteso: fuori elenco) | 10:24 |

Esito: accesso risolto per A1, A2, A3 (catalogo), C1–C6, E2, E3, R1; **E1 accesso mancante** finché `ws.comune.roma.it` non è consentito (§11).

## 3. Conteggi di giugno 2026 per fonte (M)

Regole del metodo §4.1: item con data di pubblicazione fra il 1° e il 30 giugno 2026 (Europe/Rome); per Atti Web la data di repertorio dell'atto, perché il portale non espone una data di pubblicazione. Settimane di giugno: 30/7 = 4,29.

| Fonte | Item giugno | Per settimana | Elenco usato | Paginazione completa | Lettura | Formato |
|---|---|---|---|---|---|---|
| A1 Roma Capitale, Municipi | **365** (135 notizie + 230 informazioni di servizio) | 85,2 | `https://www.comune.roma.it/web/it/notizie.page?mun=municipio_<n>&pagina=N` e `…/informazioni-di-servizio.page?mun=municipio_<n>&pagina=N`, 15 filtri più `intermunicipale` | sì: ogni filtro percorso fino alla prima pagina con data anteriore al 1° giugno | 10:54 | HTML |
| A2 Atti Web, Municipi | **1.426** | 332,7 | `POST https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/data/filtro-dati!cerca.action?tipologia=<T>&dtRprDa=2026-06-01&dtRprA=2026-06-30&itemsPerPage=500`, 16 tipologie interrogate (15 con risultati, DMK senza; selezione per organo municipale: `docs/sources/A2_ATTIWEB_TIPOLOGIE.md`) | sì: totale dichiarato dall'API = letti (MMC 516 in due pagine); alle 12:10 DMS era 193 (+2 pubblicazioni tardive con data di giugno) | 10:42 | PDF (testo o scansione) |
| C1 Questura di Roma | **79** | 18,4 | `https://questure.poliziadistato.it/it/Roma/archivio/category/5730dc9d86cad683338531/<p>/`, giugno = pagine 17–25 | sì (pagine 15–27 lette) | 10:34 | HTML |
| C2 Carabinieri | **20** (su 151 nazionali) | 4,7 | `https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa?d=202606` e `!page/page/2..8`; Roma = fonte "Comando Provinciale di Roma" o luogo "(RM)" | sì (8 pagine) | 10:36 | HTML |
| C3 Procura di Roma | **0** (22 item in archivio dal 2017, 4 nel 2026: 21 avvisi e 1 comunicato) | 0 | `https://procura-roma.giustizia.it/it/news_e_comunicati.page?frame5_item=1..5` | sì (intero archivio) | 10:32 | HTML, PDF allegati |
| C4 Vigili del Fuoco, Comando Roma | **8** | 1,9 | `https://www.vigilfuoco.it/comando-vvf-roma/notizie-dal-territorio?provincia=244&data[min]=2026-06-01&data[max]=2026-06-30` | sì (una pagina) | 10:32 | HTML |
| C5 Polizia Locale | **2** (53 item in archivio 2018–2026) | 0,5 | `https://www.comune.roma.it/web/it/notizie.page?struttura=str_sg&pagina=1..6` | sì (6 pagine) | 10:49 | HTML |
| C6 Guardia di Finanza | **0** Comando Provinciale Roma (3 Lazio; Roma: 38 nel 2026, 84 in archivio) | 0 | `https://www.gdf.gov.it/++api++/@search?portal_type=News Item&reparti_correlati=<uid Comando Provinciale Roma>&effective 2026-06` | sì (API, `items_total`) | 10:50 | HTML (Plone) |
| E1 060608 | **—** accesso mancante | — | `https://060608.comune.roma.it/eventi` (elenco e RSS da `ws.comune.roma.it`) | — | 10:24 | — |
| E2 culture.roma.it | **407** pubblicati a giugno; **189** con data fra il 15 settembre e il 15 ottobre (limite inferiore: fra i 917 pubblicati dal 1° luglio) | 95,0 | `https://culture.roma.it/wp-json/wp/v2/event_calendar?per_page=100&page=1..5&after=2026-06-01T00:00:00&before=2026-07-01T00:00:00` | sì (`X-WP-Total` 407 = letti) | 10:37 (futuri 11:05) | HTML + JSON |
| E3 Roma Capitale, agenda eventi (livello 2) | **104** pubblicati a giugno (data `search:data` della pagina); **36** con periodo nei 30 giorni dal 15 settembre (S: periodo in testo libero, fra i 190 pubblicati dal 26 maggio; limite inferiore) | 24,3 | `https://www.comune.roma.it/web/it/eventi.page?pagina=N` (10 per pagina, ordinata per data di pubblicazione; faccette `mun=`, `temat=`, `struttura=`) | sì (pagine 1–19 fino alla prima data anteriore al 1° giugno) | 12:25 (pagine), 12:40 (schede) | HTML |

Copertura per Municipio (M). A1 notizie: una notizia con più tag di Municipio è contata in ciascuno (22 su 135); A1 informazioni di servizio: filtro dell'elenco; A2: struttura dell'atto; Cronaca: solo gli item localizzati a Municipio dal testo (C1+C2+C4); E2: tassonomia del portale.

| Municipio | A1 notizie | A1 inf. servizio | A2 atti | Cronaca localizzata | E2 giugno | E2 futuri 30 gg |
|---|---|---|---|---|---|---|
| I | 19 | 11 | 119 | 4 | 86 | 42 |
| II | 18 | 10 | 37 | 1 | 41 | 29 |
| III | 15 | 11 | 19 | 0 | 13 | 4 |
| IV | 11 | 5 | 19 | 2 | 31 | 1 |
| V | 24 | 15 | 125 | 2 | 27 | 36 |
| VI | 11 | 22 | 98 | 8 | 39 | 8 |
| VII | 25 | 14 | 109 | 2 | 42 | 4 |
| VIII | 18 | 11 | 137 | 1 | 25 | 1 |
| IX | 13 | 18 | 99 | 1 | 7 | 2 |
| X | 11 | 18 | 72 | 4 | 17 | 0 |
| XI | 22 | 11 | 81 | 1 | 20 | 1 |
| XII | 11 | 19 | 122 | 1 | 2 | 1 |
| XIII | 7 | 38 | 102 | 0 | 19 | 9 |
| XIV | 12 | 13 | 113 | 2 | 28 | 12 |
| XV | 26 | 14 | 174 | 1 | 0 | 16 |
| non attribuiti | 1 intermunicipale | 0 | 0 | 79 (C1 57, C2 14, C4 6, C5 2) | 10 | 23 |

E3 (livello 2, tag `search:municipio` del portale, 69 su 104): I 20, II 9, III 2, IV 1, V 7, VI 4, VII 5, VIII 5, IX 2, X 4, XI 1, XII 3, XIII 2, XIV 4, XV 3; 2 appuntamenti con più Municipi; 35 senza tag (per lo più mostre e spettacoli in sedi centrali). Tematiche: 66 dei 104 sono appuntamenti di "Roma in musica 2026".

A2 per gruppo (M): delibere e atti politici 208 (CMD 42, GMD 32, GMT 32, GMM 15, CMZ 32, CMY 8, CMR 44, PMO 2, PMT 1), convocazioni 571 (CMC 55, MMC 516), verbali 456 (CMV 24, GMV 25, MMV 407), determinazioni 191 (DMS). I quattro Municipi con meno atti a giugno: III 19, IV 19, II 37, X 72.

Zone più frequenti (M, lookup deterministico): E2 tor-bella-monaca 39, tor-cervara 29, ostia 16, pigneto-torpignattara 10, san-lorenzo 7; C1 tor-vergata 2, tor-bella-monaca 2, ostia 2, centro-storico 2 e 13 zone con 1 item; A1 notizie: 55 item con zona, disperse su 30 zone.

**A3 e A4 (livello 2, 15 settembre pomeriggio, M)**: RomaTV, letta dopo che l'owner ha consentito gli host `*.streamcloud.it` (16:02): 496 registrazioni di giugno per 404,8 ore (14 Municipi, Commissioni Capitoline 75, Assemblee 7), date di seduta e pubblicazione per tutte (ritardo mediano 0), 82 trascrizioni automatiche della piattaforma (solo Consigli). YouTube: 131 registrazioni con data di giugno nel titolo (Municipio I 77, IX 37, V 9, Assemblea Capitolina 8), di cui 107 commissioni municipali per 82,1 ore; sottotitoli automatici in 22 video su 22 letti; data di pubblicazione letta per 12. Campione letto per intero (15 commissioni YouTube e 7 Consigli RomaTV, 22 sedute di giugno): 44 possibili notizie, 41 assenti da A1 e dalla Cronaca; tre pareri capitolini (norme tecniche del piano regolatore, librerie, Regolamento animali) attraversano più Municipi nelle stesse settimane. Dettagli, campione e analisi in `VIDEO_RICOGNIZIONE_2026-06.md`.

## 4. Localizzabilità (M)

Lookup deterministico sul testo con le regole di `tests/zone_distribution.py` (nomi e alias del gazetteer, stoplist, `never_substring`) più il riconoscimento di "Municipio N". Quote sugli item del mese.

| Fonte | Toponimo nel testo | Zona (89) dal testo | Municipio | Ambigui (più zone) | Note |
|---|---|---|---|---|---|
| A1 | 62,5% (notizie 82,2; inf. servizio 50,9) | 32,9% (notizie 40,7; inf. servizio 28,3); 37,8% contando anche il titolo | 100% dal portale (tag o filtro) | 73 | il lookup sul testo assegna un Municipio diverso dal tag in pochi avvisi che citano indirizzi di uffici altrove: fa fede il portale |
| A2 | 12,2% (solo oggetto dell'atto) | 8,6% | 100% dalla struttura | — | il corpo dell'atto è nel PDF (§6) |
| C1 | 81,0% | 26,6% | 27,8% | 31 | nomi di persona nel 62,0% (euristica) |
| C2 | 65,0% | 30,0% | 30,0% | 7 | nomi nel 70,0% |
| C4 | 37,5% | 25,0% | 25,0% | 0 | 8 item |
| C5 | 0% | 0% | 0% | 0 | 2 item cittadini |
| E2 | 37,8% | 30,0% | 97,5% dalla tassonomia del portale (10 senza) | 14 | luogo presente nel 99,8%, indirizzo nel 95,8% |
| E3 | 52,9% | 35,6% | 66,3% dal tag del portale | 9 | il periodo dell'evento è testo libero ("3 e 4 luglio", "fino al 10 settembre") |

Ritardo mediano fra fatto e pubblicazione, dove la data del fatto è nel testo (M): C1 1 giorno (n=10 su 79; 69 senza data del fatto), C2 1 giorno (n=11 su 20), C4 0 giorni (n=5 su 8); A1, A2 —. Eventi (E2): anticipo mediano fra pubblicazione e data dell'evento 17 giorni (quartili 9–30; 6 pubblicati dopo l'evento); 73 eventi su più giorni.

## 5. Sovrapposizioni e resa netta (metodo §4.1)

**Cronaca** (C1+C2+C4+C5 = 109 item, intero mese, M). Duplicati certi 0; dubbi 1: Carabinieri e Questura del 6 giugno, Ostia, arresti per spaccio, forze diverse, persone e numeri diversi, fatto verosimilmente distinto ma con le tre condizioni soddisfatte alla lettera (URL nel file `cronaca_dedup_campione.csv` su Drive, con 10 coppie giudicate distinte). Resa lorda 109; netta 108–109; contributo unico C1 78–79, C2 19–20, C4 8, C5 2.

**Amministrazione** (A1+A2 = 1.791 item, oltre la soglia di 300: la regola prevede campioni di almeno 60 item per coppia, resa stimata). Perimetro A2 provvisorio: solo le 15 tipologie municipali; le categorie centrali con riferimento territoriale (`docs/sources/A2_ATTIWEB_TIPOLOGIE.md` §4–§6) non sono ancora nel conteggio.
- Classe delle convocazioni, intero mese (M): 58 avvisi di convocazione fra le informazioni di servizio A1 (53 di Consiglio, 5 di Giunta); 35 hanno un gemello certo in A2 (atto CMC della stessa seduta, stesso Municipio); 12 sono dubbi (la data della seduta non è nel titolo dell'avviso: Municipi IV, IX, XII, XIV); 11 senza gemello (5 di Giunta, tipologia assente in Atti Web; 6 di Consiglio dei Municipi II e VI senza atto con quella seduta). Coppie in `A1_A2_convocazioni_pairs_compact.csv`.
- Resto di A1 contro A2 (S): campione di 60 item A1 non di convocazione, seed `2026-06-A1xA2`, frame ordinato per data, tipo (notizie prima delle informazioni di servizio) e URL; per ciascuno il miglior atto A2 dello stesso Municipio per parole chiave (Jaccard fra titolo e oggetto), giudicato dall'Operator: **0 stesso fatto** (miglior candidato 0,33, una convocazione di Giunta contro un verbale di Giunta di data diversa). Limite: un atto il cui oggetto è formulato in modo diverso dalla notizia sfugge al criterio; una verifica umana sul campione resta possibile con il file `A1xA2_campione60_compact.csv`.
- Resa lorda 1.791; duplicati certi 35; dubbi 12; netta 1.744–1.756. L'attribuzione al primo che pubblica (avviso o atto) non è stata calcolata coppia per coppia: cambia la ripartizione del contributo unico fra A1 (318–330) e A2, non la resa netta.

**Eventi** (E2+E3 = 511 item, oltre la soglia di 300; confronto sull'intero mese per titolo normalizzato, M come limite inferiore). Duplicati certi 7 (1 titolo identico, 6 titoli simili giudicati stesso evento dall'Operator: mostre e rassegne pubblicate da entrambi i portali), dubbi 1 (un concerto di "Roma in musica" contro una pagina di culture.roma.it con titolo simile). Resa lorda 511; netta 503–504; contributo unico E3 96–97 su 104 (92–93%). Coppie in `eventi_E3xE2_candidati.csv`. Limite: un evento pubblicato con titoli diversi dai due portali sfugge al confronto. E1 resta fuori (accesso mancante).

## 6. Formati, estrazione e prova T2 (metodo §5)

- **HTML** (A1, C1, C2, C4, C5, E2): testo e date estratti con parser locali per tutti gli item del mese, non solo i 20 previsti (A1 365, C1 79, C2 20, C4 8, C5 2, E2 407): esito sì, qualità leggibile. Due errori sistematici trovati e corretti prima del calcolo delle quote: le informazioni di servizio del portale usano un markup diverso dalle notizie (corpo in `<article>`, nessun `h2` di titolo), per cui la prima estrazione conteneva il menu del sito e non l'avviso; le stesse pagine sono servite senza `charset` e vanno ridecodificate in UTF-8.
- **JSON/API**: A2 (Struts, date ISO obbligatorie nel filtro: il formato italiano dà errore), C6 (Plone REST), E2 (WordPress REST più pagina evento per date, luogo e Municipio).
- **PDF, prova T2 parziale su A2** (M): 18 PDF, 8 scelti per coprire le tipologie e 10 estratti con seed `2026-06-A2`; estrazione locale con PyMuPDF e pypdf. **10 con testo** (714–30.381 caratteri; DMS 4/4, CMC 2/2, MMV 1/3, MMC 2/4, CMD 1/2) e **8 scansioni** senza testo (CMD 1, GMD 1, GMM 1, CMV 1, MMC 2, MMV 2): quota scansioni 44% (S, n=18). Tempo: meno di 2 s per PDF fra download ed estrazione; costo 0,00 €. OCR non eseguito: `tesseract` assente, modello visivo fermo (§9). Le convocazioni e le determinazioni sono testo; verbali e delibere sono spesso scansioni.
- **C3**: allegati PDF non provati (nessun item a giugno).
- **Costo per item** (M): 0,00 €; tempo macchina 1–3 s per pagina HTML (tempi di risposta misurati 1,0–3,4 s), meno di 2 s per PDF. **Intervento umano prevedibile** (S): notizie e avvisi 1–2 min per item (verifica del Municipio e del tema); atti 3–5 min se testo, oltre 10 min se scansione senza OCR; cronaca 1–2 min (localizzazione e rimozione dei nomi); eventi meno di 1 min (dati strutturati).

## 7. Riuso e licenze (evidenze per L11)

| Fonte | Pagina trovata | Cosa dice | Stato |
|---|---|---|---|
| A1, A2, C5, E3 (comune.roma.it) | sì, `https://www.comune.roma.it/web/it/note-legali.page` | "Copyright: i diritti sui contenuti appartengono a Roma Capitale"; nessuna licenza di riuso indicata; autorizzazione scritta per il marchio | da verificare (L11) |
| C1 Questura | piè di pagina con licenza Creative Commons BY-NC-ND 2.5 collegata a `www.poliziadistato.it` | pagina della licenza non leggibile dall'ambiente (CONNECT 403); se confermata, vieta uso commerciale e opere derivate | da verificare (L11), bloccante per il riuso testuale |
| C2 Carabinieri | sì, pagina "Note legali" del sito | indica una licenza SIAE del sito; nessuna clausola di riuso dei comunicati | da verificare (L11) |
| C3 Procura | sì, `https://procura-roma.giustizia.it/it/note_legali.page` | "solo per uso personale"; riproduzione dei testi consentita con citazione della fonte; vietato l'uso commerciale | da verificare (L11), restrittiva |
| C4 Vigili del Fuoco | sì, `https://www.vigilfuoco.it/note-legali` | contenuti testuali e documentali (comunicati, notizie) con licenza **CC BY 4.0**, citando la fonte e l'indirizzo della pagina | sì |
| C6 Guardia di Finanza | sì, `https://www.gdf.gov.it/it/note-legali` | copyright su marchi e segni distintivi; nessuna clausola sul riuso dei comunicati | da verificare (L11) |
| E1 060608 | pagina con link "Disclaimer" nel piè di pagina (non letto: contenuti serviti da `ws.comune.roma.it`) | — | da verificare (L11) |
| E2 culture.roma.it | sì, `https://culture.roma.it/esclusione-dalle-responsabilita/` (letta alle 11:52) | clausola di esclusione della responsabilità sull'esattezza delle informazioni; nessuna clausola di riuso; nessuna pagina di licenza trovata | da verificare (L11) |

## 8. Difficoltà incontrate

1. **E1**: elenco e RSS di 060608 vivono su `ws.comune.roma.it`, non nel dominio consentito; senza quell'host la fonte è illeggibile.
2. **A1**: due markup diversi (notizie e informazioni di servizio) e pagine senza `charset`; la prima estrazione degli avvisi conteneva il menu del portale (tutti i 15 Municipi nel testo) e la quota di localizzazione era falsata; corretto e ricalcolato. Le notizie hanno tag di più Municipi (22 su 135) e una categoria "intermunicipale".
3. **A2**: portale AngularJS; l'elenco viene da un'API Struts che accetta solo date ISO e al massimo 500 item per pagina (MMC 516: seconda pagina); il Municipio va ricavato dal campo struttura ("MUNIC.", "MUN.", "MUNICIPIO ROMA"); nessuna data di pubblicazione, solo la data di repertorio.
4. **C1**: alcune pagine dell'archivio tornano vuote alla prima richiesta (ripetute con successo); il piè di pagina rimanda alla licenza su un dominio bloccato.
5. **C2**: elenco nazionale con filtro mensile `?d=AAAAMM`; Roma si isola con la fonte "Comando Provinciale di Roma" o il luogo "(RM)".
6. **C6**: pagina HTML vuota senza JavaScript; conteggio possibile solo dalla REST API Plone con l'identificativo del reparto.
7. **E2**: WordPress REST espone la data di pubblicazione ma non quella dell'evento, letta dalla pagina di ogni appuntamento (917 pagine per la finestra futura).
8. **PDF**: `pypdf` non importava per una dipendenza mancante (`cffi`), installata da PyPI; nessun OCR disponibile.
9. **Ambiente**: i CSV per item sono stati caricati su Drive a blocchi (limiti di lettura dello strumento); un nome di persona in una motivazione di deduplicazione è stato rimosso prima del caricamento.
10. **Metodo, regola (c) per la Cronaca**: "stesso tipo di fatto" aggrega operazioni diverse di forze diverse nello stesso giorno e nello stesso luogo (il caso dubbio di §5). Non modificato: proposta in §10.
11. **A3 RomaTV**: applicazione che carica cataloghi e media da host esterni (`*.streamcloud.it`), consentiti dall'owner nel pomeriggio; il bundle indica un tenant di prova, quello di Roma (`ac104`) è stato trovato per tentativi; i media restano su host non consentiti.
12. **A4 YouTube**: la pagina `watch` reindirizza al controllo anti-bot; i metadati per video passano solo da alcuni client di `yt-dlp` e, dopo una ventina di letture in pochi minuti, ogni richiesta (player e sottotitoli) riceve il controllo anti-bot o 429: il recupero delle trascrizioni procede a ritmo forzato; i media sono bloccati (nessuna verifica sull'audio).

## 9. Tempo impiegato e costi

| Voce | Valore | Stato |
|---|---|---|
| Operator, sessione del 15 settembre | 10:24–12:00 circa (Europe/Rome), 1 h 35 min, di cui letture e parser 10:24–11:06, poi controlli, Drive e questo rapporto; pomeriggio 12:05–13:00 circa (≈ 1 h): verifica A2 richiesta dall'owner e lettura di E3 | M (orari), S (ripartizione) |
| Richieste HTTP | ≈ 2.100 (elenchi, item, PDF, API) | S |
| Spesa | 0,00 € nella sessione; totale ledger 0,86 € (S), residuo 49,14 € sui 50 € | M/S (`docs/sources/TRIAL_LEDGER.md`) |
| Chiamate AI | nessuna; T1, T3, T4 ferme (chiave non confermata); T5 ferma (S0, S1-02); T2 eseguita solo per la parte locale | M |

## 10. Decisione sul livello 2 e raccomandazioni provvisorie

Raccomandazioni per fonte (provvisorie: la consegna finale le conferma dopo il livello 2 e la verifica dell'owner sul campione).

| Fonte | Raccomandazione | Ragione | Condizione che la cambierebbe |
|---|---|---|---|
| A1 | usare | 365 item/mese, Municipio certo, HTML leggibile, 40% delle notizie a zona | licenza (L11) |
| A2 | usare come fonte di record degli atti (provvisorio) | 1.426 atti/mese delle tipologie municipali, Municipio certo | 44% di scansioni: senza OCR (T2 da completare) verbali e delibere restano oggetto e PDF; perimetro da decidere sulle categorie centrali (DDS 921/mese, ≈ 45 atti centrali con territorio): `docs/sources/A2_ATTIWEB_TIPOLOGIE.md` §6 |
| C1 | usare | 79 item/mese, toponimo nell'81% | licenza BY-NC-ND se confermata (L11) |
| C2 | integrare | 20 item/mese, localizzazione 30% | — |
| C3 | escludere dalla Cronaca | 0 item a giugno, 22 in nove anni, quasi solo circolari | comparsa di comunicati regolari |
| C4 | integrare | 8 item/mese, CC BY 4.0 | — |
| C5 | riserva, come filtro di A1 | 2 item/mese; vive sul portale di A1 (filtro per struttura) | — |
| C6 | riserva | 0 a giugno; 38 nel 2026 (≈ 3/mese) | frequenza stabile e localizzabile |
| E1 | accesso mancante | host non consentito | apertura di `ws.comune.roma.it` |
| E2 | usare | 407/mese, 97,5% a Municipio, 30% a zona | gap per Municipio (XV 0, XII 2, IX 7 a giugno) |
| E3 (livello 2) | integrare | 104/mese sullo stesso portale di A1, 66% con Municipio, 7% già in E2 | copre poco i Municipi deboli di E2 (XV 3, XII 3, IX 2 a giugno); la finestra futura richiede il parsing del periodo in testo libero |
| A3 (livello 2) | fonte candidata (provvisorio) | 496 registrazioni/mese con date strutturate e ritardo zero; 82 trascrizioni della piattaforma (Consigli); unica registrazione per 7 Municipi e per le Commissioni Capitoline; 18 possibili notizie da 7 Consigli letti | commissioni senza testo finché audio e T1 restano fermi; riuso da verificare |
| A4 (livello 2) | fonte candidata per I e IX (provvisorio) | 107 commissioni/mese, trascrizioni automatiche a costo zero, contenuti assenti dagli atti; 26 possibili notizie da 15 sedute lette | data di pubblicazione misurata solo per 12 video; nomi e toponimi inaffidabili nell'ASR; sedute quasi vuote; V parziale; nessuna integrazione automatica |

**Livello 2**: sì, limitato. E3 (`comune.roma.it/web/it/eventi.page`) è stato letto il 15 settembre pomeriggio (scheda nel registro): stesso portale e stesso accesso di A1, costo zero, seconda fonte Eventi finché E1 è bloccato; A3 e A4 solo per i cataloghi (numero e durata delle commissioni per Municipio), perché le prove video T1 restano ferme; R1 non serve per i tre blocchi.

**Gap dichiarati (M)**: la Cronaca istituzionale localizzabile a Municipio è di 30 item al mese in tutto (0 per III e XIII): non regge da sola pagine di quartiere e la consegna finale deve presentare all'owner le alternative del metodo §5 (bacino, minimi, fallback al Municipio: DEC-006, fallback al Municipio per pagine sottili). Eventi: XV senza appuntamenti a giugno (16 nei 30 giorni), XII e IX molto sotto gli altri.

**Proposte sul metodo, non applicate**: (a) per la Cronaca aggiungere alla regola (c) "stessa forza o stessi numeri (arresti, sequestri)" per non fondere operazioni distinte; (b) per l'Amministrazione trattare le convocazioni A1↔A2 come duplicati strutturali (stessa seduta) e non campionarle; (c) per gli Eventi contare la finestra futura sull'intero archivio con data evento, non solo sulle pubblicazioni recenti (il 189 è un limite inferiore).

## 11. Cosa impedisce concretamente di procedere

1. **`ws.comune.roma.it`** non è fra i domini consentiti: senza, E1 resta "accesso mancante" e la deduplicazione Eventi non è eseguibile (owner: aggiunta alla politica di rete; le sessioni avviate dopo la modifica lo vedono).
2. Già noto (metodo §7): senza la conferma scritta sulla chiave OpenAI o la rotazione verificata restano ferme T1, T3, T4 e l'OCR delle scansioni di A2; T5 attende S0 e S1-02.
3. **Media di RomaTV** (`ac104mp.streamcloud.it`, `ovp2-live.akamaized.net`) non consentiti: le commissioni di A3 hanno metadati ma non testo (l'API è stata consentita alle 16:02).
4. **Controllo anti-bot di YouTube sull'IP di uscita**: rallenta a ore metadati e trascrizioni di A4; la verifica sull'audio richiede file depositati dall'owner (metodo §5).

Nient'altro blocca il livello 1; la collocazione dei dati per item su Drive (metodo §4.2, residuo) è usata come proposta e non blocca.

## 12. Campione per il controllo (metodo §4.3)

Su Drive `Fonti 2026-06/`: `audit_campione_5_per_fonte.csv` (5 item per fonte, seed `2026-06-<fonte>`); `localizzazione_campione_per_blocco.csv` (fino a 10 a zona e 10 a Municipio o non localizzati per blocco, seed `2026-06-loc-<blocco>`, numerosità effettiva dichiarata per categoria); `cronaca_dedup_campione.csv` (1 dubbio + 10 distinti); `A1_A2_convocazioni_pairs_compact.csv` (35 coppie certe); `A1xA2_campione60_compact.csv` (60 item, 0 duplicati). Campionamento: `random` di Python 3.11, `random.seed(seed); random.sample(frame, k)`, frame ordinato per data di pubblicazione, ordine delle fonti, URL.

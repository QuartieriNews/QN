# Quartieri News — Impianto di progetto (Project Baseline) v0.6

| Campo | Valore |
|---|---|
| Stato | **Owner-approved baseline** (revisione dell'owner completata l'11 settembre 2026 sulla v0.6). Impianto scritto dall'Operator (Claude) e verificato da Codex (Technical Council) in sei iterazioni; le correzioni della sesta sono applicate e non riverificate (§7); il Technical Council non viene riaperto su questa baseline. Non è il project plan: è l'impianto da cui deriverà il piano con timeline definitiva, dopo le misure e le decisioni di §6 |
| Data | 11 settembre 2026 (baseline approvata) · file di record: `docs/PROJECT_BASELINE.md` |
| Base | Decisioni DEC-014…DEC-021 (le otto decisioni dell'11 settembre 2026) (11 settembre), DEC-101…104 (decisioni storiche: immagini, fonti, revisione, governance), DEC-006 (fallback per pagine sottili, residuo aperto) residua; Round 2 e Reconciliation; stato reale del repository e di Drive verificato oggi |
| Unità di stima | Ore dell'owner a 30 h/settimana; ogni intervallo è una stima dichiarata, non una misura. Le misure esistenti sono citate come tali |
| Etichette | **D** decisione da prendere · **M** misura da ottenere · **R** rischio/difficoltà principale |

## 0. Come leggere

Il piano è organizzato per **flussi di lavoro** (§2), non per fasi: ogni flusso ha cosa fare, stima, difficoltà e decisioni. Le fasi e il calendario (§4) sono una proposta di sequenza derivata dai vincoli già decisi (verifica eventi prima, thin slice subito dopo, lancio con 89 pagine e tre blocchi). Le decisioni (§3) sono raccolte in un unico registro con il momento in cui vanno prese. Il documento è pensato per essere espanso flusso per flusso in un piano con WBS e timeline, dopo le tre misure che oggi mancano (§5).

## 1. Punto di partenza: cosa esiste, dove sono le informazioni, cosa possiamo davvero fare

**Nel repository (`quartierinews/qn`)** — l'unica fonte con governance: gazetteer completo (440 quartieri, 91 zone, 89 pagine, generatore con invarianti; 37 controlli eseguiti oggi in `test_guards.py`, mentre il brief ne dichiara 38: incoerenza documentale minore da allineare), prompt di geografia ed editoriale con due golden set (30 + 40 item), coda di revisione specificata (Google Sheet), venue registry (5 KB, seed), un solo code node (`parse-duration`), l'export n8n del workflow Events **pre-refactor** (23 nodi: Apify → tre filtri IF (id evento, Roma e futuro, esistenza in Firestore) → Firestore → Drive → Sheets; nessuna guardia v2.5 a due livelli, nessuna coda, nessun filtro editoriale), il loop di sviluppo (lane gate, test, Council), 25 decisioni (DEC-001…021 (decisioni di prodotto) di prodotto, DEC-101…104 (decisioni storiche: immagini, fonti, revisione, governance) storiche). **Non esiste**: il sito, alcun publisher, alcuna pipeline per Amministrazione, Cronaca o Conversation, il canale Posts, il modulo newsletter, le pagine legali, gli strumenti di misura, la seconda AI di verifica, il versioning dei contenuti.

**Infrastruttura attiva** — VPS Aruba (n8n self-hosted, ~78 €/anno), progetto Google Cloud `roma-pipeline` (Firestore, Drive, service account), Google Sheets, Apify (a consumo, ~1,4 $ per 107 eventi), dominio `quartierinews.it` registrato, API OpenAI. Budget storico su Drive: circa 2.400 € spesi (VPS, smartphone, SIM, due lotti di trascrizione video delle commissioni, due lavori Upwork di scraping di pagine e gruppi Facebook).

**Su Drive (cartella "Progetto Quartieri News")** — materiale di lavoro senza governance, in parte superato dal repository: *Next Step* (inventario delle fonti per Municipio: canali YouTube e streaming RomaTV per 11 Municipi, Atti&Verbali per 4 con volume basso e marcati RISK, commissioni capitoline; ~1.800 video/verbali nei primi tre mesi 2026; lista di 20+ feed RSS e siti: Questura, Comune, Regione, ANSA, RomaToday, 060608; flussi ideali per notizie, eventi, approfondimenti, immagini), *UX e Design* (struttura della pagina quartiere: header con logo dedicato, blocchi, gerarchia HP → Municipio → quartiere; sistema di tag a tre tipi; valutazione di plugin WordPress ClassifAI/TaxoPress), *Idee QN* (newsletter tematica, "Spiegato bene", dossier demografici, dominî per Paese), *Mappa dei Quartieri* (superata dal gazetteer), *FB groups – Quarters* e `facebook.xlsx` (censimento pagine e gruppi), *Enti Terzo Settore Roma*, *Ricerca Fonti Notizie*, *Articoli/Post Esempi*, cartelle per Municipio, *QN Hub* (00 Governance … 40 Decisions, con il log decisioni migrato su GitHub).

**Cosa possiamo davvero fare oggi**: (a) misurare — eventi per pagina fuori agosto, resa delle fonti istituzionali, tasso di eccezione — con la pipeline e i dati esistenti, senza costruire nulla di nuovo; (b) costruire per PR nel loop Claude→Codex→owner, con cablaggio manuale in n8n a carico dell'owner; (c) usare Drive come archivio di lavoro, non come fonte di regole. **Cosa non possiamo fare**: automazione autenticata su Facebook (posizione DEC-102 (posizione sulle fonti)), scraping dei gruppi senza verifica di accessibilità e regole, pubblicazione senza le pagine legali di base.

**R0 — Sicurezza, da chiudere prima di ogni altra cosa.** Il documento Drive *Foglio Info Tecniche* contiene in chiaro credenziali Aruba, la chiave privata del service account Google Cloud, una chiave API OpenAI e un token GitHub. Vanno **ruotati subito** e spostati in un gestore di segreti (o nelle credenziali n8n e nei secret di GitHub), e il documento va svuotato. Costo: 1–2 h. Non è opzionale: il repository lavora per PR pubbliche di processo e le chiavi in un doc condivisibile sono l'esposizione più grave del progetto oggi.

## 2. Flussi di lavoro

Per ogni flusso: obiettivo · cosa fare · stima (ore owner, pre-lancio) · difficoltà (R) · decisioni (D) · misure (M).

### A. Fonti e dati: inventario, verifica, diritto d'uso
- **Obiettivo**: sapere, prima di costruire, quanto ogni fonte rende per pagina e a quali condizioni.
- **Cosa fare**: (1) verifica pre-lancio eventi (DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio), prima attività): 4 settimane non agostane di raccolta con il workflow attuale, conteggi per pagina e per Municipio con `zone_distribution.py`, quota localizzabile, vita media; (2) inventario fonti Amministrazione per i 15 Municipi + Roma Capitale a partire da *Next Step*: dove pubblicano (video, verbali, albo, comunicati), anticipo, ritardo, formato, licenza; (3) le sei fonti di Cronaca (Questura/Polizia di Stato, Carabinieri, Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza): volume mensile, quota con toponimo, quota con nomi; (4) i 91 gruppi Facebook: pubblico/privato, regole, leggibilità senza login; (5) registro fonti unico (`source registry`) con campo licenza/termini; (6) chiusura dei residui del pacchetto Events a carico dell'owner: i 5 indirizzi `confidence: verify` del golden set geografico, Colle del Sole (DEC-002 (Colle del Sole)), le cinque verifiche di DEC-003 (1–3 h in tutto).
- **Stima**: 40–70 h (di cui 6–8 verifica eventi, 20–40 inventario Amministrazione, 3–5 Cronaca, 3–5 gruppi, 8–12 registro).
- **R**: le fonti istituzionali sono 16 siti eterogenei; i video delle commissioni richiedono trascrizione (costo e qualità ignoti: i due lotti "Vincenzo" sono l'unica esperienza); 4 Municipi hanno solo verbali scarsi (RISK in *Next Step*); i feed di testate terze sono esclusi per diritti (tesi §14.2).
- **D**: quali fonti Amministrazione sono "di record" per l'MVP (video vs verbali vs comunicati); trascrizione interna (Whisper/API) vs servizio; cosa fare dei 4 Municipi a bassa resa.
- **M**: eventi/pagina non agostani; resa per Municipio; costo per ora di video trascritta.

### B. Pipeline Eventi: refactor v2.5 e canale Posts
- **Obiettivo**: portare l'unico workflow esistente allo stato specificato (17 cambi) e prepararne il gemello per i post.
- **Cosa fare**: consolidare la spec v2.5 (workplan esistente); implementare per PR: URL raccolti manualmente, guardie a due livelli, venue registry, filtro editoriale, ricorrenze, TTL, coda, immagini e card generata (DEC-101 (policy immagini)), run report, schedule; chiudere DEC-001 (tour commerciali a pagamento), DEC-004 (cap eventi per run in produzione); **Gate G0 (già fissato dal brief, non opzionale)**: i due golden set (30 editoriali, 40 geografici) eseguiti e superati contro i prompt prima che una qualunque uscita sia cablata alla pubblicazione; lo stesso gate, con golden set propri, vale per C e D. Poi il canale Posts (page registry, JSON canonico condiviso) solo se scatta il criterio D5.
- **Criterio operativo proposto per D5** (da confermare dall'owner, coerente con DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio)): al termine di A1, per ogni pagina si conta lo stock di eventi futuri con le fonti iniziali più il fallback nella forma scelta in D4. Se ogni pagina raggiunge dieci, Posts resta post-lancio. Se una o più pagine restano sotto, si allargano prima ricerca e fonti extra-Facebook per due settimane; se dopo l'allargamento **anche una sola pagina** resta sotto dieci eventi futuri con il fallback (DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio): il pavimento vale per ogni pagina), il canale Posts diventa dipendenza del lancio, costruito a partire dalle pagine e dai gruppi del Municipio di quella pagina (Municipio X è il caso atteso), e la fase 2 assorbe 50–150 h in più.
- **Stima**: spec 15–25 h; refactor 12–20 PR-equivalenti → 100–300 h (l'ampiezza dipende dalle ore per PR, non misurate); Posts 6–10 PR → 50–150 h.
- **R**: ore per PR-equivalente ignote (PR #8: 9 cicli, 83 finding); cablaggio n8n manuale; Apify e Facebook cambiano senza preavviso; il canale Posts ha sei difetti aperti noti.
- **D**: D5 con il criterio sopra; ordine Posts vs newsletter (owner: dopo il lancio); DEC-001 (tour commerciali a pagamento) tour commerciali; DEC-004 (cap eventi per run in produzione) cap.
- **M**: ore per PR sui primi tre PR del refactor (costo zero).

### C. Pipeline Amministrazione (thin slice → completa)
- **Obiettivo**: il blocco "cuore distintivo" con 5 record per pagina, generati con doppio controllo AI.
- **Cosa fare**: thin slice su 2–3 Municipi eterogenei in staging (seconda attività, DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio)): adattatori per 2–3 formati, classificazione (tema, luogo, commissione), localizzazione al Municipio/quartiere, generazione L0 (scheda) e L1 (notizia breve) con `uncertain`, golden set 30 item e gate G0 prima della pubblicazione, misura di eccezioni e minuti per caso; poi estensione a 16 fonti, storia interna facoltativa (DEC-018 (architettura URL e migrazione ai domini)).
- **Stima**: thin slice 60–100 h (di cui costruzione 40–70, calibrazione e golden set 20–30); estensione 80–150 h; totale 140–250 h.
- **R**: un claim sbagliato in un testo istituzionale non ha registro dove finire (costo per eccezione scende solo con i prompt); commissioni multitematiche fuori MVP; trascrizione audio come collo di bottiglia di costo; formati PDF scansionati.
- **D**: livello di dettaglio della notizia L1 (scheda strutturata vs articolo); regola per commissioni multitematiche (owner: fuori MVP); provider dei modelli.
- **M**: tasso di eccezione e minuti per caso per tipologia; errori materiali su campione.

### D. Pipeline Cronaca
- **Obiettivo**: 1 record per pagina da fonti ufficiali di sicurezza e giustizia, con la regola DEC-016 (nomi in Cronaca da fonti ufficiali) sui nomi.
- **Cosa fare**: adattatori per le sei fonti di §2.A (Questura/Polizia di Stato, Carabinieri, Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza; feed o pagine); flag persona con instradamento in coda per minori, vittime, testimoni, familiari, dati sensibili; `case_status` visibile; localizzazione; generazione con verifica sulla fonte; sospensione e rettifica per item (DEC-020 (correzioni dirette con tracciabilità interna)); **golden set Cronaca** (30 comunicati classificati a mano: toponimo, persone, categoria sensibile, `case_status`) e gate G0 prima del cablaggio alla pubblicazione.
- **Stima**: 75–135 h (di cui golden set e calibrazione 15–25).
- **R**: esposizione legale (domande 4–6 della Reconciliation); comunicati concentrati su poche zone; immagini per la cronaca (nessuna fonte lecita chiara: *Next Step* ipotizza screenshot di mappe).
- **D**: policy immagini per Cronaca (mappa generata vs nessuna immagine); attivazione della capacità "nomi" solo dopo il parere.
- **M**: comunicati/mese con toponimo e con identificativi.

### E. Publishing, CMS e sito (89 pagine)
- **Obiettivo**: il sito pubblico con 89 + 15 + 1 pagine, URL per quartiere (DEC-018 (architettura URL e migrazione ai domini)), identità canonica dei contenuti, fallback al render, pagine legali e di metodologia (DEC-019 (disclosure generale dell'AI)).
- **Cosa fare**: scegliere l'architettura (D-E1); modello dati dei contenuti con `content_id`, quartiere principale, `geo_level`, `municipality_code`, versioni (DEC-020 (correzioni dirette con tracciabilità interna)); publisher dal corpus (Firestore → sito); template pagina quartiere/Municipio/home; fallback Municipio o limitrofi (DEC-006 (fallback per pagine sottili, residuo aperto) residua; tabella di adiacenza se limitrofi); pagina commerciale (DEC-021 (configurazione pubblicitaria)); sitemap, redirect futuri 1:1.
- **Stima**: 120–250 h (la scelta E1 sposta l'intervallo: un CMS con tema custom sta nella parte alta per i vincoli di identità canonica e fallback; un generatore statico dal corpus nella parte bassa ma richiede un backend minimo per moduli).
- **R**: decisione difficile da invertire (identità, URL); 89 pagine sottili se il fallback è mal presentato; hosting e prestazioni con immagini locali (DEC-101 (policy immagini)); manutenzione di un CMS con plugin vs codice proprio.
- **D-E1 = D2 (prima di costruire)**: WordPress con tema/plugin custom · generatore statico o SSR leggero (Astro/Eleventy o equivalente) alimentato da Firestore con moduli su funzioni serverless · CMS headless + frontend. Criteri: identità canonica e fallback nativi nel modello, costo di manutenzione nelle 30 ore, migrazione a 89 domini, newsletter e analytics, competenze disponibili. **Valutazione del Technical Council (Operator e Codex, convergente)**: l'opzione corpus-driven (statico/SSR leggero) ha il miglior rapporto coerenza/controllabilità con DEC-015 (doppio controllo AI), DEC-018 (URL), DEC-020 (correzioni) e con un solo operatore: fallback e provenienza si implementano in modo deterministico al render, superficie d'attacco ridotta, migrazione 1:1 facilitata; il costo è costruire il contorno (moduli, preview, strumenti operativi minimi). WordPress resta competitivo solo se l'editing manuale supera quanto DEC-015 (pubblicazione automatica con doppio controllo AI) prevede; headless ha senso con una redazione multiutente, fuori dal perimetro MVP. La decisione resta dell'owner.
- **Pacchetto condizionale se D4 = limitrofi** (oggi non esiste: DEC-006 (fallback per pagine sottili, residuo aperto) residua): (1) fonte dell'adiacenza: geometrie delle zone urbanistiche di Roma Capitale (open data) intersecate con le 89 pagine, oppure compilazione manuale nel workbook master del gazetteer; (2) regole: relazione simmetrica, anche fra Municipi diversi, massimo 4–6 vicini per pagina ordinati per confine condiviso, nessuna pagina senza vicini; (3) generazione in `build_gazetteer.py` con invarianti e controlli in `test_guards.py` (simmetria, nessun auto-riferimento, copertura); (4) regola di render: eventi propri, poi vicini, poi Municipio, con provenienza visibile. Stima 12–25 h, sul percorso critico subito dopo D4. Se D4 = Municipio: zero ore aggiuntive (`municipality_code` esiste già su ogni item).
- **D**: hosting (VPS Aruba vs piattaforma statica/serverless); forma del fallback (D4); sezioni vs flusso (D13, su prototipo interno prima del lancio).

### F. UX, UI e branding
- **Obiettivo**: una pagina quartiere che renda comprensibile la provenienza geografica (requisito deciso) e un brand con identità per testata dentro il gruppo QN (DEC-018 (architettura URL e migrazione ai domini)).
- **Cosa fare**: (1) brand: nome confermato (`quartierinews.it`), logo di gruppo e regola per i loghi "dedicati" per quartiere (*UX e Design*), palette e tipografia, tono di voce (già nei principi editoriali); (2) UX: architettura dell'informazione (home, Municipio, quartiere, articolo, evento, metodologia, commerciale, segnalazioni), wireframe della pagina quartiere con i tre blocchi + Conversation opzionale, tre varianti di presentazione geografica (sezioni / flusso / ibrido) per il test di usabilità; (3) UI: design system minimo (componenti card evento/notizia/atto, badge di provenienza, blocco pubblicitario standard DEC-021 (configurazione pubblicitaria)), mobile-first; (4) test di usabilità con 5–8 residenti su prototipo.
- **Stima**: 60–120 h se fatto in casa con strumenti standard; 30–50 h owner + 1.500–4.000 € se logo e design system sono commissionati.
- **R**: brand "per testata" moltiplicato per 89 senza un sistema generativo diventa insostenibile; il sito deve funzionare con pagine sottili nei primi mesi; nessun contenuto reale per prototipare finché C e D non producono output.
- **D**: in casa vs designer esterno; logo per quartiere generato da sistema vs unico logo di gruppo con variante testuale; presentazione geografica (dopo il test).
- **M**: esito del test di usabilità (comprensione della provenienza; tempo per trovare un evento).

### G. Newsletter e moduli
- **Obiettivo**: al lancio raccolta e conservazione consensi (email, quartiere, nome facoltativo, iscrizioni multiple, disiscrizione globale); invio dopo il lancio.
- **Cosa fare**: modulo con doppio opt-in e log dei consensi; archivio iscritti con quartiere; dopo il lancio: composizione settimanale per quartiere dal corpus, invio, metriche.
- **Stima**: modulo e archivio 20–40 h; motore di invio post-lancio 40–80 h.
- **R**: privacy prima della raccolta (gate di capacità); deliverabilità; personalizzazione solo del saluto.
- **D**: strumento di invio (servizio ESP vs invio proprio) e dove vive l'archivio iscritti (ESP vs Firestore con export); nome della newsletter (facoltativo).

### H. Sistemi di controllo: qualità, sicurezza, operazioni
- **Obiettivo**: rendere operativo DEC-015 (pubblicazione automatica con doppio controllo AI) e DEC-020 (correzioni dirette con tracciabilità interna) e proteggere l'infrastruttura.
- **Cosa fare**: seconda AI di verifica con accesso alla fonte e prompt di record versionati; coda manuale unica per tutti i blocchi (evoluzione del Google Sheet o strumento dedicato) con motivi strutturati; campione stratificato settimanale e tassonomia degli errori con registro; versioning e sospensione per item; run report e monitoraggio (fonti che cambiano formato, job falliti, staleness); backup di Firestore e Drive; gestione dei segreti (R0), account e permessi; regola "nessun cambio in n8n senza export in PR".
- **Stima**: 60–110 h (seconda AI 25–40; coda e campione 15–25; versioning 10–20; monitoraggio, backup, segreti 10–25).
- **R**: la seconda AI costa a ogni item e va misurata (falsi positivi in coda = ore dell'owner); un solo operatore per tutto; n8n self-hosted da aggiornare e proteggere.
- **D14, due rami stimati**: *n8n resta self-hosted* → pacchetto di hardening del VPS (aggiornamenti n8n e sistema, HTTPS con certificato, firewall, backup dei workflow e delle credenziali, utente non privilegiato): 6–12 h una tantum + 0,5 h/settimana; *migrazione a n8n Cloud* → export e reimport dei workflow, ricreazione credenziali (Firestore, Drive, Sheets, Apify, OpenAI), endpoint e schedule, test di regressione sul run report, dismissione del VPS: 8–15 h una tantum + canone (indicativamente 20–50 €/mese) e meno manutenzione. Da decidere prima del refactor B perché le PR successive cablano sull'istanza scelta.
- **D**: strumento della coda (Sheet vs app minima); provider e indipendenza funzionale delle due AI; D14 come sopra.
- **M**: incidenza delle eccezioni per blocco; errori materiali su campione.

### I. Legale e compliance
- **Obiettivo**: pubblicare lecitamente il sito nel suo complesso e attivare ogni capacità solo dopo la sua verifica (DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio)).
- **Cosa fare**: parere scritto sulle 13 questioni della Reconciliation §8 con priorità: rettifica su richiesta vs correzione silenziosa (DEC-020 (correzioni dirette con tracciabilità interna)), regola sui nomi (DEC-016 (nomi in Cronaca da fonti ufficiali)), disclosure per contenuto (DEC-019 (disclosure generale dell'AI)), campagne gratuite come pubblicità (DEC-021 (configurazione pubblicitaria)), newsletter e consenso, analytics; pagine: privacy, cookie, contatti, segnalazioni e correzioni, metodologia AI, note legali (editore/responsabile); registrazione testata e ROC quando dovuti.
- **Stima**: 15–30 h owner + 1.500–5.000 € di onorario; 2–6 settimane in parallelo.
- **R**: un obbligo incompatibile con DEC-016 (nomi in Cronaca), DEC-019 (disclosure AI), DEC-020 (correzioni) cambia il modello di revisione e le ore ricorrenti; l'esposizione personale dell'owner finché la forma societaria non è scelta.
- **D**: forma societaria/editoriale e responsabile; studio legale.

### J. Misura, analytics e commerciale
- **Obiettivo**: misurare i due KPI primari e il ritorno (DEC-017 (KPI e guardrail)) e avere la pagina commerciale con campagne gratuite.
- **Cosa fare**: analytics con identificatore di prima parte, esclusione traffico interno/bot, per pagina e per rete; conteggi newsletter; cruscotto mensile; selezione offline di 5–10 attività per le campagne gratuite; registro interno delle campagne; materiali per la prima vendita.
- **Stima**: 20–40 h pre-lancio; 3–5 h/settimana post-lancio (commerciale).
- **R**: consenso per analytics (domanda legale 13); traffico iniziale troppo frammentato per leggere per pagina.
- **D**: strumento analytics (senza cookie vs GA4 con consenso); prezzi e formati (nei sei mesi dopo).

### K. Governance del progetto e tooling di sviluppo
- **Obiettivo**: far reggere il loop a un solo operatore per 4–8 mesi.
- **Cosa fare**: consolidare lo stato in `docs/` (il brief strategico è fermo alla situazione pre-decisioni); un `PROJECT_PLAN.md` versionato con milestone e misure; diario del tempo per PR e per attività (è la misura che decide fra 3,5 e 12 mesi); staging `staging_` per tutto; cadenza di revisione mensile del piano.
- **Regola operativa per il tetto di quattro cicli per PR (DEC-012 (corsie come livelli di attenzione, tetto di quattro cicli per PR))**: ogni PR è dimensionata per chiudere in tre cicli al massimo (un solo cambio, sezione della spec citata, test eseguibili inclusi); al terzo ciclo senza convergenza il builder si ferma, divide il cambio in PR più piccole o porta il punto controverso all'owner come `OWNER_DECISION_REQUIRED`, invece di tentare il quarto ciclo; M2 registra per ogni PR anche il numero di cicli, e una PR fermata dal tetto conta come scenario alto nella ristima di §6 anche se le ore sono nella banda centrale.
- **Stima**: 10–20 h iniziali + 1 h/settimana.
- **R**: il loop Claude→Codex→owner è l'unica capacità di sviluppo; il tetto di quattro cicli per PR e i finding numerosi rendono il ritmo il rischio numero uno del calendario.
- **D**: se e quando cercare uno sviluppatore o un socio (fuori dal piano; registrato).

## 3. Registro delle decisioni da prendere

| # | Decisione | Quando | Flusso | Reversibilità |
|---|---|---|---|---|
| D1 | Rotazione e custodia dei segreti (R0) | Subito | H | — |
| D2 | Architettura del sito e publisher (CMS vs statico vs headless) e hosting | Prima di costruire E (ottobre) | E | Bassa |
| D3 | Fonti "di record" per Amministrazione e modalità di trascrizione | Dopo l'inventario A (ottobre) | A/C | Media |
| D4 | Forma del fallback eventi (Municipio vs limitrofi) — DEC-006 (fallback per pagine sottili, residuo aperto) residua | Dopo la verifica A (ottobre–novembre) | E | Media |
| D5 | Canale Posts come dipendenza del lancio (criterio in §2.B) | Dopo la verifica A e l'eventuale allargamento delle fonti | B | Alta |
| D6 | DEC-001 (tour commerciali a pagamento) tour commerciali; DEC-004 (cap eventi per run in produzione) cap produzione | Prima di attivare il filtro / lo schedule | B | Alta |
| D7 | Provider e modelli delle due AI, criterio di indipendenza funzionale | Durante la thin slice C | C/H | Alta |
| D8 | Brand: in casa vs esterno; logo unico vs sistema per quartiere | Fine fase 0 (inizio ottobre); esecuzione in fase 1 | F | Media |
| D9 | Strumento della coda manuale | Prima della thin slice | H | Alta |
| D10 | Strumento newsletter (ESP) e sede dell'archivio iscritti | Prima del modulo (gennaio) | G | Media |
| D11 | Strumento analytics | Prima del lancio | J | Alta |
| D12 | Forma societaria/editoriale, responsabile, studio legale | Ottobre (avvio parere) | I | Bassa |
| D13 | Presentazione geografica (sezioni vs flusso) | Prima del lancio, su prototipo interno (gennaio–febbraio); riesame dopo il test di usabilità post-lancio | F/E | Alta |
| D14 | n8n self-hosted vs Cloud | Prima del refactor B | H | Media |
| D15 | Ordine Posts vs motore newsletter dopo il lancio | Post-lancio | B/G | Alta |

## 4. Sequenza, carico e tempi (proposta)

Metodo: le ore per fase sono la **somma delle stime dei flussi di §2**; il carico è fissato a **30 ore/settimana** e la durata di ogni fase deriva dalle ore centrali divise per 30, con un'eccezione: la fase 0 dura **4 settimane di calendario** perché A1 richiede quattro settimane osservate di raccolta (tempo di attesa, non di lavoro); le sue 90 ore si distribuiscono su quelle quattro settimane a 22,5 h/settimana. **Sovrapposizione fase 0/fase 1**: le 7,5 h/settimana rimanenti della fase 0 sono già lavoro di fase 1 (progettazione della seconda AI e della coda, preparazione della thin slice), che quindi parte in sovrapposizione fin dalla prima settimana di fase 0 a carico ridotto e passa a 30 h/settimana piene quando la fase 0 si chiude; le 30 h in sovrapposizione (7,5 × 4) sono comprese nelle 240 h della fase 1, che a 30 h piene ne richiede altre 7 settimane. La sovrapposizione non anticipa alcuna decisione di fase 0: in quelle ore si preparano i pacchetti decisionali e il design, non le scelte. Le date sono quindi bande, non impegni, finché M2 e M3 non sono misurate. Rispetto al Round 2: le 960 h centrali dell'Operator riguardavano il solo sviluppo pre-lancio; questo piano somma anche popolamento, fonti, legale, brand, controlli e governance, e arriva a 1.170 h centrali. La banda prudente 4–8 mesi del Round 2 vale solo se M2 misura nella parte bassa.

**Scelta per la fase 2** (il caso centrale eccedeva le 30 ore): la fase si allunga a 22 settimane a 30 ore e il **test di usabilità con residenti passa dopo il lancio** (ammesso da DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio): i problemi di interfaccia non bloccano); prima del lancio F consegna brand, architettura dell'informazione, design system minimo e le tre varianti di presentazione geografica su prototipo, e D13 si prende su prototipo interno.

| Fase | Contenuto (flussi) | Uscita e gate | Ore (somma) | Durata a 30 h (centrale) | Periodo centrale |
|---|---|---|---|---|---|
| 0 · Misurare e decidere | R0/D1; A1 verifica eventi (4 settimane osservate); A2–A6 inventario fonti e residui; avvio parere (I); spec v2.5 (B); K impianto; D2, D3, D8, D9, D12, D14 | Conteggi per pagina; decisioni di fase 0 prese; spec consolidata | 80–130 | 4 settimane di calendario (90 h) | metà set – metà ott 2026 |
| 1 · Thin slice e motore | C thin slice; H seconda AI + coda; B primi 3 PR con diario ore; F brand e architettura dell'informazione; E modello dati e D2 applicata; D4, D5, D7 | **G0 Events** (golden set superati); eccezioni e minuti per caso misurati; ore per PR misurate; **ristima del calendario** | 160–285 | 7 settimane a 30 h + 30 h in sovrapposizione con la fase 0 | metà set (a carico ridotto) / metà ott – inizio dic 2026 |
| 2 · Costruire | B refactor restante (+ Posts se D5); C estensione a 16 fonti; D Cronaca con golden set; E sito e publisher (+ adiacenza se D4 = limitrofi); G modulo newsletter; I pagine legali; J analytics; F UI e prototipo; H versioning, monitoraggio, backup; D10, D11, D13 | Staging completo su 89 pagine con contenuti reali; **G0 per C e D, e G0 Events rieseguito sulla versione finale effettivamente cablata alla pubblicazione**; gate legali di §4.1 superati o capacità disattivate | 420–935 (+50–150 con Posts; +12–25 con adiacenza) | 22 settimane | dic 2026 – apr 2027 |
| 3 · Popolare e lanciare | Popolamento (stock Events a ridosso del lancio); campagne gratuite (J); verifica degli 8 requisiti; code di tutti i flussi; go-live | **Gate numerico per pagina**: 89/89 con ≥ 5 Amministrazione, ≥ 1 Cronaca, ≥ 10 eventi futuri (con fallback), provenienza e link alla fonte su ogni item; gli altri sette requisiti di DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio) verificati; MVP online; inizio dei sei mesi di misura | 125–230 | 6 settimane | mag – fine giu 2027 |
| Post-lancio | Motore newsletter o Posts (D15); test di usabilità; dossier; commerciale | KPI al sesto mese | 30 h/sett. | — | da giu 2027 |

**Totale pre-lancio: 785–1.580 ore, cioè 26–53 settimane (6–12 mesi)**; centrale 1.170 h = 39 settimane (tabella sotto); **con entrambi i rami condizionali attivi (D5 Posts e D4 limitrofi): 847–1.755 h, fino a circa 59 settimane**. Finestra di lancio: **fine marzo 2027** (bassa), **fine giugno 2027** (centrale), **fine settembre 2027** (alta), inclusa la settimana di attesa di A1. Con Posts come dipendenza (D5) ogni data slitta di 2–5 settimane; con l'adiacenza (D4 = limitrofi) di una.

**Assegnazione delle 30 ore per settimana (caso centrale).** Ore/settimana per flusso in ogni fase; le ore per fase sono ore/settimana × settimane. La fase 0 usa 22,5 h/settimana per 4 settimane (= 90 h): le altre 7,5 h/settimana sono di fase 1, che parte in sovrapposizione; da fase 1 in poi la somma è 30 per costruzione.

| Flusso | Fase 0 (4 sett., 22,5 h/sett. + 7,5 di fase 1) | Fase 1 (7 sett. piene + 30 h in sovrapposizione) | Fase 2 (22 sett.) | Fase 3 (6 sett.) |
|---|---|---|---|---|
| A Fonti e dati | 11 | 0,5 | — | 0,5 |
| B Pipeline Eventi | 5 (spec) | 5,5 | 7 | 0,5 |
| C Amministrazione | — | 10 | 5 | 1 |
| D Cronaca | — | — | 4,5 | 0,5 |
| E Sito e publisher | — | 1,5 | 7,5 | 2,5 |
| F UX/UI/brand | — | 4,5 | 1,5 | 0,5 |
| G Newsletter | — | — | 1,5 | — |
| H Controlli e sicurezza | 1,5 | 5,5 | 1 | 1,5 |
| I Legale | 2 | 0,5 | 0,5 | 0,5 |
| J Misura e commerciale | — | — | 0,5 | 3 |
| K Governance | 3 | 2 | 1 | 1 |
| Popolamento e verifica di lancio | — | — | — | 18,5 |
| **Totale (h/sett.)** | **22,5** (+7,5 di fase 1) | **30** | **30** | **30** |
| **Ore di fase (centrale)** | **90** | **240** | **660** | **180** |

**Percorso critico.** A1 (conteggi eventi) → D4/D5 (fallback, Posts) → B refactor completo → E publisher e fallback al render → popolamento Events a ridosso del lancio → go-live. In parallelo, anch'esso vincolante: C thin slice → D7 (provider e indipendenza) → C estensione → contenuti reali per E ed F. Il parere legale (I) non è sul percorso critico del sito, ma è sul percorso di ogni capacità gated (§4.1). G0 (golden set) sta su entrambi i rami prima di ogni cablaggio alla pubblicazione.

### 4.1 Gate legali di capacità

Traduzione operativa di DEC-014 ("ogni verifica blocca solo la capacità cui si riferisce"): la capacità si attiva quando esiste il parere e l'owner ha adottato (o modificato) la regola; altrimenti resta disattivata e il lancio procede senza.

| Capacità | Regola già assunta | Questione legale (Reconciliation §8) | Gate: prima di | Se il parere è incompatibile |
|---|---|---|---|---|
| Sito nel suo complesso | — | 1 status editoriale e responsabile; 2 informative; 7 immagini (DEC-101 (policy immagini)) | Go-live | Adempimenti da completare: bloccano il lancio |
| Cronaca con nomi | DEC-016 (nomi in Cronaca da fonti ufficiali) | 4, 5, 6 | Attivazione della pipeline Cronaca in produzione | Cronaca senza identificativi o revisione per item |
| Correzione silenziosa e rettifica su richiesta | DEC-020 (correzioni dirette con tracciabilità interna) | 6 | Go-live (procedura di rettifica definita) | Nota di rettifica su richiesta |
| Disclosure AI generale | DEC-019 (disclosure generale dell'AI) | 3 | Go-live (pagina di metodologia) | Etichetta per contenuto |
| Raccolta newsletter | DEC-017 (KPI e guardrail)/G | 8 privacy e consenso | Attivazione del modulo | Modulo disattivato al lancio (requisito 6 non soddisfatto → lancio slitta) |
| Conversation | — | 9 gruppi Facebook, estratti e link | Attivazione del blocco | Blocco assente (opzionale per DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio)) |
| Campagne gratuite e pagina commerciale | DEC-021 (configurazione pubblicitaria) | 12 pubblicità e etichettatura | Pubblicazione della prima campagna | Spazi vuoti al lancio |
| Pubblicità politica | DEC-021 (configurazione pubblicitaria) | 10 | Accettazione della prima richiesta | Resta inattiva |
| Analytics | DEC-017 (KPI e guardrail) | 13 consenso | Attivazione della misura | Strumento senza cookie o banner di consenso |

### 4.2 Dipendenze esterne e tempi di attesa

| Dipendenza | Lead time | Da avviare | Milestone che blocca |
|---|---|---|---|
| Parere legale sulle 13 questioni | 2–6 settimane dopo l'incarico | Ottobre 2026 (D12) | Gate di §4.1; attivazione Cronaca (fase 2) |
| Designer esterno (se D8 = esterno) | 4–8 settimane per logo e design system | Novembre 2026 | UI del sito (fase 2) |
| Servizio o modello di trascrizione video | 1–2 settimane di prova su un lotto | Ottobre 2026 (D3) | Thin slice C |
| ESP newsletter e configurazione dominio (SPF/DKIM) | 1 settimana | Gennaio 2027 (D10) | Modulo G |
| Hosting/piattaforma del sito | 1 settimana | Con D2 | Primo deploy di staging E |
| Registrazione testata / ROC / forma societaria | 2–8 settimane | Con D12 | Go-live (se dovuti) |

## 5. Difficoltà principali (in ordine di impatto sul calendario)

1. **Ritmo del loop di sviluppo** (K/B): unica capacità costruttiva; ore per PR ignote; misura nei primi tre PR.
2. **Resa e forma delle fonti istituzionali** (A/C): 16 siti eterogenei, video da trascrivere, 4 Municipi scarsi; decide se i 5 record per pagina sono raggiungibili senza fallback al Municipio.
3. **Offerta di eventi per pagina** (A/B): Municipio X a zero; 72/89 pagine vuote in agosto; il fallback redistribuisce, non crea; il canale Posts può diventare dipendenza.
4. **Architettura del sito difficile da invertire** (E): identità canonica, URL, fallback e migrazione a 89 domini vanno decisi una volta.
5. **Costo e precisione del doppio controllo AI** (H): falsi positivi in coda consumano le 30 ore; nessuna misura fino alla thin slice.
6. **Esposizione legale delle regole già assunte** (I): nomi, correzioni silenziose, disclosure; un obbligo incompatibile cambia il modello.
7. **Brand e UX con contenuti sottili** (F): 89 pagine che devono sembrare vive con 5/1/10 record e provenienza mista.
8. **Sicurezza operativa** (H/R0): segreti esposti, un solo account, n8n self-hosted.

## 6. Cosa serve per arrivare al project plan con timeline

Tre misure e nove decisioni, tutte in fase 0–1: **M1** eventi per pagina non agostani (6–8 h, ottobre); **M2** ore per PR-equivalente (primi tre PR, novembre); **M3** tasso di eccezione e minuti per caso della thin slice (dicembre); **D1, D2, D3, D8, D9, D12, D14** entro ottobre (D9 e D14 condizionano rispettivamente la thin slice e i primi PR del refactor, quindi la fase 1); **D4 e D5** subito dopo M1 (novembre), perché aprono rami che valgono rispettivamente +12–25 h e +50–150 h: finché non sono chiuse la timeline resta condizionale su quei due rami. Con questi, il piano definitivo sostituisce gli intervalli con date e assegna le 30 ore per settimana ai flussi.

**Criteri di ristima a fine fase 1** (soglie proposte, allineate alle ipotesi 8/12/15 h per PR del Round 2 e alle soglie di eccezione di §4.3 del Round 2):

| Misura | Scenario basso | Scenario centrale | Scenario alto |
|---|---|---|---|
| M2 ore per PR-equivalente (media dei primi tre PR del refactor) e cicli per PR | ≤ 8 h e ≤ 2 cicli | 8–12 h e ≤ 3 cicli | > 12 h, oppure una PR fermata dal tetto di DEC-012 (corsie come livelli di attenzione, tetto di quattro cicli per PR): ricalcolo di B, C, D, E con il valore misurato e PR più piccole |
| M3 tasso di eccezione della thin slice / minuti per caso | ≤ 15% e ≤ 5 min | 15–30% e 5–8 min | > 30% o > 8 min: rivedere prompt e seconda AI prima di estendere C |
| M1 pagine con ≥ 10 eventi futuri (fonti iniziali + fallback D4) | 89/89 già con le fonti iniziali | 89/89 solo dopo l'allargamento delle fonti | anche una sola pagina sotto dopo l'allargamento: Posts dipendenza (D5) |

Lo scenario risultante è il peggiore fra i tre; le date di §4 si aggiornano di conseguenza e il piano definitivo le riporta come impegno.

## 7. Esito della verifica con Codex (Technical Council)

Sei iterazioni con `gpt-5.3-codex` (Responses API, reasoning high), ciascuna con il piano, l'evidence pack (stato del repository, decisioni, infrastruttura senza segreti) e lo scambio precedente. Ogni finding è stato accettato e applicato; a ogni iterazione Codex ha confermato che nessun punto precedente restava aperto.

| Iterazione | Finding di Codex | Esito |
|---|---|---|
| 1 (v0.1) | 2 fatti minori; stime per fase incoerenti con i flussi; D9/D14 fuori dai prerequisiti; carico settimanale e percorso critico mancanti; gate legali di capacità mancanti; dipendenze esterne | Tutti accettati → v0.2 |
| 2 (v0.2) | Fase 3 incoerente (207 > 180 h); scelta per la fase 2 sospesa; gate golden set assente; 5 indirizzi da verificare; criterio D5 | Tutti accettati → v0.3 |
| 3 (v0.3) | Golden set Cronaca non stimato; pacchetto condizionale D4 = limitrofi; "nessuna guardia"; 960/1.170; D8; soglie di ristima | Tutti accettati → v0.4 |
| 4 (v0.4) | Fase 0 di 3 settimane vs 4 osservate; criterio D5 per pagina (DEC-014 (perimetro pubblico 89 pagine e requisiti di lancio)); ramo D14 n8n Cloud; sei fonti Cronaca; "cinque" decisioni; D13; gate numerico 5/1/10 | Tutti accettati → v0.5 |
| 5 (v0.5) | D4 e D5 mancanti fra i prerequisiti del piano definitivo (§6); carico della fase 0 non coerente con le 4 settimane; stato del documento | Tutti accettati → v0.6 |
| 6 (v0.6) | Somma della fase 2 = 29,5 (IMPORTANTE); regola operativa per il tetto di quattro cicli per PR di DEC-012 (IMPORTANTE); totale con i rami condizionali; G0 Events da rieseguire sulla versione cablata; segnaposto in §7 | Tutti accettati e applicati in questa v0.6, **non riverificati** (iterazioni autorizzate esaurite) |

Convergenze esplicite di Codex: aderenza a DEC-014…021 (le otto decisioni dell'11 settembre 2026) e DEC-101…104 (decisioni storiche: immagini, fonti, revisione, governance), fotografia dello stato reale, R0 sui segreti, gate G0 e gate legali per capacità, misure M1–M3 e ristima, percorso critico e dipendenze esterne, valutazione tecnica su D2 (opzione corpus-driven la più coerente; decisione dell'owner). Verdetto formale all'ultima iterazione verificata (sesta): NON ACCORDO per i due punti IMPORTANTI sopra, ora applicati. Andamento: i finding sono passati da sei aperti (iterazione 1) a due, tutti su porzioni aggiunte nell'iterazione precedente; nessun finding ha mai riguardato il perimetro, le decisioni o la struttura per flussi.

## Appendice A — Avvio operativo della Fase 0

Fase 0 = 4 settimane di calendario da metà settembre a metà ottobre 2026, 22,5 h/settimana di fase 0 più 7,5 h/settimana di fase 1 in sovrapposizione. Questa appendice trasforma la fase in attività assegnate, con l'uscita attesa di ogni settimana. **Nessuna decisione di §3 è presa qui**: per ognuna si prepara un pacchetto decisionale (fatti, criteri, opzioni, costo di ciascuna) e la scelta resta all'owner nella settimana indicata.

### A.1 Chi fa cosa

| Ruolo | Attività della fase 0 |
|---|---|
| Owner | R0 rotazione dei segreti; raccolta manuale degli URL evento (A1); lettura e classificazione delle fonti (A2–A4); incarico allo studio legale (I); decisioni di fase 0 sui pacchetti; cablaggio e run in n8n; diario del tempo |
| Builder (Claude, per PR nel loop con Codex) | Baseline in `docs/` (questo file); consolidamento della spec v2.5 (B); template del registro fonti e del diario del tempo in `docs/`; script e istruzioni per i conteggi A1; pacchetti decisionali D2, D3, D9, D14 come documenti in `docs/decision-packs/` (senza raccomandazione oltre quanto già in §2); design della seconda AI e della coda (fase 1 in sovrapposizione) |
| Codex | Revisione delle PR del builder; non è riaperto come Technical Council sulla baseline |
| Studio legale | Parere sulle 13 questioni (Reconciliation §8), avviato in settimana 1–2 |

### A.2 Calendario settimana per settimana

| Settimana | Fase 0 (22,5 h) | Fase 1 in sovrapposizione (7,5 h) | Uscita della settimana |
|---|---|---|---|
| 1 (metà set) | **R0**: rotazione di credenziali Aruba, chiave del service account Google Cloud, chiave OpenAI, token GitHub; nuove chiavi solo nelle credenziali n8n e nei secret GitHub o in un gestore di segreti; documento Drive svuotato; verifica che nessun altro documento le contenga (1–2 h). **A1 settimana 1**: raccolta URL su tutta Roma con finestra di 30 giorni, run del workflow attuale in `staging_`, export del run report (2 h). **A2**: template del registro fonti (fonte, Municipio, tipo, URL, formato, anticipo, ritardo, licenza, note) e prime 3 fonti Amministrazione lette per intero (6 h). **I**: pacchetto per lo studio legale (13 questioni, decisioni DEC-016 nomi in Cronaca, DEC-019 disclosure AI, DEC-020 correzioni, DEC-021 pubblicità, pagine previste) e richiesta di preventivo (3 h). **K**: baseline committata; diario del tempo avviato (data, flusso, PR, ore, cicli) (2 h) | Lettura di `docs/REVIEW_QUEUE.md` e di DEC-103 (modello di revisione coda + campione) e DEC-015 (pubblicazione automatica con doppio controllo AI); schema della coda unica per tutti i blocchi (motivi strutturati, campi minimi) come bozza | Segreti ruotati; primo run A1; registro fonti aperto; pacchetto legale inviato; diario attivo |
| 2 | **A1 settimana 2** (2 h). **A2**: 5 Municipi coperti; per ognuno resa attesa (item/mese), formato, anticipo (8 h). **D3, raccolta fatti**: prova di trascrizione di un lotto di 3 video di commissione con due modalità (servizio e modello locale/API), costo e qualità per ora di video, senza scegliere (4 h). **B**: PR di consolidamento della spec v2.5 aperta dal builder sul workplan esistente (revisione owner 3 h). **D14, raccolta fatti**: versione n8n installata, stato aggiornamenti, backup esistenti, confronto di costo self-hosted/Cloud (2 h). **D12**: preventivi ricevuti, scelta dello studio (1,5 h) | Bozza del prompt di record della seconda AI di verifica (input: item + fonte; output: esito, motivo, campi controllati) e dei controlli deterministici; nessun provider scelto | Metà inventario Amministrazione; fatti per D3 e D14 raccolti; spec in revisione; studio legale scelto |
| 3 | **A1 settimana 3** (2 h). **A2**: 15 Municipi + Roma Capitale coperti (8 h). **A3**: sei fonti Cronaca, comunicati di un mese contati, quota con toponimo e con nomi (3 h). **A4**: 91 gruppi Facebook: pubblico/privato, regole, leggibilità senza login (3 h). **A6**: 5 indirizzi `confidence: verify`, Colle del Sole (DEC-002), verifiche di DEC-003 (2 h). **B**: revisione Codex della spec, risposte del builder (2 h). **D2 e D9, pacchetti**: il builder consegna i pacchetti decisionali (criteri di §2.E e §2.H compilati con i fatti: costi di hosting, competenze, effort del "contorno", strumento della coda); l'owner li legge (1,5 h) | Design della thin slice C: quali 2–3 Municipi (eterogenei per formato: video, verbali, comunicati), golden set da 30 item da costruire, misure da raccogliere (eccezioni, minuti per caso, errori materiali) | Inventario fonti completo; Cronaca e gruppi misurati; residui Events chiusi; pacchetti D2 e D9 in mano all'owner |
| 4 (metà ott) | **A1 settimana 4 e conteggi**: `zone_distribution.py` sui quattro run, tabella per pagina e per Municipio di eventi futuri distinti con fonti iniziali e con fallback al Municipio (unica forma calcolabile senza tabella di adiacenza), quota localizzabile, vita media (4 h). **A5**: registro fonti unico consolidato in `docs/` con licenza/termini per fonte (4 h). **Decisioni di fase 0**: D1 (già eseguita in settimana 1), D2, D3, D8, D9, D12, D14 prese dall'owner sui pacchetti; ciascuna scritta in `decisions/` come nuova entry (5 h). **Spec v2.5** approvata e mergiata (2 h). **Ristima**: aggiornamento di §4 con i conteggi M1 e le decisioni (2 h) | Avvio della thin slice C sul Municipio scelto per primo; prima PR del refactor Events pianificata (M2 parte da qui) | **Uscita di fase 0**: conteggi M1 per pagina; sei decisioni prese e scritte; spec consolidata; registro fonti; pacchetto legale in lavorazione |

### A.3 Pacchetti decisionali di fase 0 (contenuto richiesto, non la scelta)

| Decisione | Cosa contiene il pacchetto | Chi lo prepara |
|---|---|---|
| D2 architettura sito e hosting | Criteri di §2.E con i fatti: costo e manutenzione di ciascuna opzione sul VPS esistente e su piattaforme statiche/serverless; effort del "contorno" (moduli, preview, funzioni) per l'opzione corpus-driven; requisiti di identità canonica, fallback e migrazione (DEC-018 architettura URL, DEC-020 correzioni) tradotti in verifiche per ciascuna opzione; competenze disponibili | Builder |
| D3 fonti di record Amministrazione e trascrizione | Registro fonti A2 con resa per Municipio; risultato della prova di trascrizione (costo/ora, qualità, tempo); i 4 Municipi a bassa resa con le alternative osservate | Owner (fatti) + builder (tabella) |
| D8 brand | Le tre opzioni di §2.F (in casa; designer per logo e design system; sistema generativo per i loghi di quartiere) con costo, tempi di attesa e cosa serve prima della fase 2 | Builder |
| D9 strumento della coda | Sheet attuale esteso vs app minima: campi richiesti da DEC-015 (pubblicazione automatica con doppio controllo AI), volume atteso dalla thin slice, costo di costruzione, come si misura il campione stratificato | Builder |
| D12 forma societaria e studio legale | Preventivi; opzioni indicate dagli studi contattati; cosa blocca il go-live | Owner |
| D14 n8n self-hosted vs Cloud | Fatti di settimana 2; i due rami stimati di §2.H; impatto sul refactor B | Builder |

### A.4 Cosa NON si fa in fase 0

Nessuna costruzione del sito, del publisher o delle pipeline nuove; nessuna scelta di provider AI (D7 è di fase 1); nessuna forma del fallback (D4) né dipendenza Posts (D5): entrambe seguono i conteggi M1 e l'eventuale allargamento delle fonti in fase 1; nessun test di usabilità; nessuna modifica in n8n senza export in PR (`workflows/README.md`).

# Quartieri News — Fase 0: piano esecutivo (candidato)

| Campo | Valore |
|---|---|
| Stato | **Candidato** — versione B-0.2, sottoposta alla review 2 di 3 del Technical Council (Claude Operator ↔ Codex reviewer). Non è approvato dall'owner; non sostituisce la baseline; non è il piano definitivo dell'intero progetto |
| Baseline di riferimento | `docs/PROJECT_BASELINE.md` — Impianto di progetto v0.6, "Owner-approved baseline (11 settembre 2026)", commit `7873b11` sulla branch `claude/quartieri-news-strategic-review-tzkl78` (non ancora su `main`, §1) |
| Perimetro | Riga "0 · Misurare e decidere" della baseline §4 e Appendice A; mandato dell'owner del 14 settembre 2026 |
| Registro delle review | `reviews/2026-09-14—cycle1—phase-0-execution—AGREEMENT_WITH_NON-BLOCKING_RESIDUALS.md` e i file successivi della stessa serie (§10) |
| Convenzioni di stato | **FATTO VERIFICATO** (letto nel repository o su Drive) · **DICHIARAZIONE DELL'OWNER** · **IPOTESI** · **DA VERIFICARE** |
| Ore | Le stime della baseline, indicative. Il tempo di attesa (le quattro settimane osservate di A1) è distinto dal lavoro attivo |

## 0. Come leggere

La Fase 0 "misura e decide": non costruisce sito, publisher né pipeline (baseline A.4). Il
documento elenca gli step concordati (§3), le sottotask con esecutore, verificatore e
criterio di accettazione (§4), le dipendenze reali e il parallelismo (§5), le decisioni e
le autorizzazioni dell'owner con il momento in cui servono (§6), il gate di chiusura (§7),
il primo gruppo di task avviabile dopo l'approvazione (§8), le contraddizioni isolate (§9)
e il registro delle review (§10). Ogni DEC è citata con la descrizione del registro
canonico `decisions/`; il testo delle decisioni non è ripetuto qui.

## 1. Basi verificate e stato di partenza

- **Baseline.** FATTO VERIFICATO: `docs/PROJECT_BASELINE.md` v0.6 esiste al commit `7873b11`
  (autore Riccardo Benvenuti, 11 settembre 2026) sulla branch
  `claude/quartieri-news-strategic-review-tzkl78`, insieme alle decisioni DEC-014…DEC-021 e
  alle modifiche a DEC-006 e DEC-103 (commit `9fcb896`). Nessuna delle due è su `main` e non
  esiste una pull request. Il file `QN_Impianto_di_Progetto_v0.6.md` citato dal mandato non è
  stato trovato su Drive per titolo: la corrispondenza con il commit `7873b11`, incluse le
  "correzioni finali autorizzate", è DA VERIFICARE dall'owner. Questo piano usa il testo del
  commit `7873b11`.
- **Il Council sulla baseline è chiuso** (sei iterazioni; baseline §7: le correzioni della
  sesta applicate e non riverificate). Nulla qui lo riapre; l'approvazione dell'owner non
  è trasformata in un accordo retroattivo di Codex.
- **Repository.** FATTO VERIFICATO al 14 settembre 2026: `origin/main` = `1459812`; suite
  verdi (`test_guards.py` 37 controlli, `test_parse_duration.js` 58, `test_council.js` 273,
  `test_lane_gate.js` 123, `test_workflow_safety.js` 13); un solo code node; export n8n
  pre-refactor (23 nodi, arricchimento di localizzazione con il prompt che
  `docs/WORKFLOW_FIXES.md` §1.1 giudica inattendibile); `tests/samples/` vuota per regola.
- **Specifica Eventi.** FATTO VERIFICATO: su Drive `QN Hub / 10 Specifications` esiste
  `Quartieri_News_FB_Events_Workflow_Specification_v2_5.docx`, "Version 2.5 — consolidation
  of version 2.4 with release 1.4.4", "Prepared 28 August 2026", stato "Ready for direct
  implementation", con T01–T45 e la migrazione di schema "flagged for owner sign-off"
  (DEC-005, modalità di migrazione allo schema 2.0, OPEN). README, AGENTS.md e
  PROJECT_BRIEF la trattano come contratto. Vedi §9.1.
- **Sicurezza.** DICHIARAZIONE DELL'OWNER: il file con le credenziali è stato cancellato da
  Drive e scaricato sul PC. FATTO VERIFICATO: una ricerca per titolo su Drive non trova
  *Foglio Info Tecniche* (il cestino non è verificabile). La rotazione NON è documentata:
  R0/D1 resta aperto ed è il primo blocco (§8).
- **Materiale Drive** (evidenza di lavoro, non regole). FATTO VERIFICATO per metadati:
  *Next Step* (22 giugno 2026), *UX e Design*, *Idee QN*, *FB groups – Quarters*,
  `facebook.xlsx`, *Ricerca Fonti Notizie Quartieri Roma*, *Gruppi Facebook* (foglio, 10
  settembre 2026), QN Hub (Operating Model v1.1, Specification Review Mandate, template dei
  report, pacchetto Events 1.4.5).
- **Non trovati** nel repository né su Drive per titolo: la "Round 2 Reconciliation" (13
  questioni legali e 8 requisiti di lancio citati da DEC-014, DEC-016, DEC-017 e dalla
  baseline §4.1, che ne nomina 12: manca la questione 11); l'evidence pack del Council
  precedente. DA VERIFICARE (§9.3).
- **Strumento del Technical Council.** FATTO VERIFICATO: le sei iterazioni sulla baseline
  hanno usato `gpt-5.3-codex` via Responses API (baseline §7); lo stesso collegamento è
  usato per questo incarico. Il tool `council/` resta riservato allo Strategic Council
  (DEC-008, modello AI a tre livelli: il critico strategico è `gpt-5.6-sol`, mai Codex).

## 2. Perimetro della Fase 0

**Dentro**: sicurezza (R0/D1); M1 (eventi per pagina su quattro settimane non agostane);
inventario e verifica delle fonti Amministrazione, Cronaca e gruppi; registro fonti unico;
residui del pacchetto Eventi (DEC-002 Colle del Sole; DEC-003 cinque indirizzi da
verificare); specifica Eventi v2.5 (§3, S4, due letture); avvio del percorso legale e D12;
pacchetti e decisioni D2, D3, D8, D9, D14; documentazione e governance della fase;
preparazione — non costruzione — della Fase 1 in sovrapposizione (7,5 h/settimana,
baseline A.2).

**Fuori** (baseline A.4 e mandato §3): costruzione di sito, publisher o pipeline nuove;
refactor Eventi (Fase 1–2; M2 si misura sui primi tre PR del refactor); provider AI (D7);
forma del fallback (D4) e dipendenza Posts (D5), da decidere dopo M1 e l'eventuale
allargamento delle fonti; DEC-001 (tour guidati commerciali a pagamento) e DEC-004
(valore di produzione di `max_events_per_run`), da chiudere prima di attivare filtro e
schedule (D6); test di usabilità; qualunque modifica in n8n senza export in PR
(`workflows/README.md`).

## 3. Macro-step concordati (Livello A, review 1: AGREEMENT WITH NON-BLOCKING RESIDUALS)

Per ogni step: obiettivo · input · output · dipendenze effettive · parallelismo ·
responsabile (esecutore / verificatore) · criterio di completamento · owner.

### S0 — Sicurezza: rotazione e custodia dei segreti (R0 / D1)
- **Obiettivo**: chiudere R0 (baseline §1): le quattro credenziali esposte (Aruba, chiave
  privata del service account Google Cloud, chiave API OpenAI, token GitHub) ruotate e
  custodite solo nelle credenziali n8n, nei secret GitHub o in un gestore di segreti; il
  documento esposto rimosso; operatività con le nuove credenziali verificata.
- **Input**: elenco delle credenziali di R0 (nomi, mai valori); la dichiarazione dell'owner.
- **Output**: voce D1 in `decisions/` (per credenziale: nome, data di rotazione, sede di
  custodia per tipo, stato della copia locale); credenziali aggiornate in n8n e
  nell'ambiente di esecuzione dell'Operator (la rotazione della chiave OpenAI invalida
  quella del Council, quella del token GitHub l'accesso dell'Operator al repository).
- **Dipendenze effettive**: nessuna a monte. A valle: primo run in staging di S1; ogni PR
  e ogni chiamata del Council dopo la rotazione.
- **Parallelismo**: per prima, settimana 1 (1–2 h owner); tutto ciò che non usa credenziali
  parte lo stesso giorno.
- **Responsabile**: owner (esecuzione); Operator (verifica di evidenze senza segreti).
- **Criterio di completamento** (gate minimo, review 1 finding 2): voce D1 DECIDED su
  `main`; le vecchie credenziali non funzionano più; documento Drive rimosso; un run di
  staging e una chiamata del Council riusciti con le nuove credenziali. Il secret scanning
  del repository (P0-S0-05) è una verifica raccomandata, fuori dal gate.
- **Owner**: azione (rotazione) e decisione D1 (sede di custodia).

### S1 — M1: misura degli eventi per pagina su quattro settimane non agostane (A1)
- **Obiettivo**: M1 (baseline §6): eventi futuri distinti per pagina e per Municipio con le
  fonti iniziali e con il fallback al Municipio, quota localizzabile, vita media; è la
  verifica pre-lancio che DEC-014 (perimetro pubblico dell'MVP: 89 pagine, tre blocchi,
  stock minimi con fallback) mette per prima e che DEC-006 (fallback al Municipio per pagine
  sottili, residuo aperto) vincola alle settimane non agostane.
- **Input**: workflow pre-refactor in `staging_`; raccolta manuale settimanale degli URL
  (DEC-102, posizione sulle fonti e sulla raccolta: manuale, nessuna automazione
  autenticata); `tests/zone_distribution.py`; credenziali ruotate (S0).
- **Output**: nota di metodo M1; quattro export settimanali su Drive (dati grezzi mai nel
  repository: DEC-102 e DEC-104, loop di sviluppo AI con i campioni fuori dal repository);
  tabella per pagina e Municipio in `docs/` (soli conteggi); lettura dello scenario M1
  secondo la tabella di ristima della baseline §6, senza prendere D4 né D5.
- **Metodo** (concordato come metodo, non come progetto: review 1): i conteggi usano i
  livelli deterministici di `zone_distribution.py` sugli export grezzi — `exact` più
  `field_contains` come pavimento, più `text_contains` come soffitto — e non il campo di
  zona del prompt pre-refactor. Il fallback al Municipio è calcolabile solo per gli eventi
  localizzati deterministicamente. La quota localizzabile è stimata con una localizzazione
  manuale di un campione casuale di eventi non localizzati (~15/settimana, ~2 h owner in
  totale). M1 in Fase 0 dà una banda, non un conteggio risolto: la baseline §6 la legge così.
- **Dipendenze effettive**: S0 → primo run in staging; il quarto run → tabella. Attesa di
  quattro settimane, non lavoro.
- **Parallelismo**: cadenza settimanale (2 h owner) in parallelo a tutto.
- **Responsabile**: owner (URL, run, export, campione); Operator (metodo, conteggi, PR);
  Codex (review delle PR).
- **Criterio di completamento**: quattro run registrati (data, URL, eventi); tabella su
  `main` con metodo dichiarato; scenario letto. Fuori: D4, D5, allargamento delle fonti.
- **Owner**: autorizzazione ai quattro run Apify (servizio esistente).

### S2 — Fonti: inventario, verifica e registro unico (A2–A5)
- **Obiettivo**: quanto ogni fonte rende per pagina e a quali condizioni (baseline §2.A):
  Amministrazione (15 Municipi + Roma Capitale), le sei fonti di Cronaca, i gruppi Facebook
  censiti; registro fonti unico con licenza/termini.
- **Input**: *Next Step*, *FB groups – Quarters*, `facebook.xlsx`, *Gruppi Facebook* (numero
  di gruppi DA VERIFICARE sul foglio: la baseline dice 91), *Ricerca Fonti Notizie*.
- **Output**: template del registro; inventario Amministrazione (16 enti) con resa attesa;
  tabella Cronaca (sei fonti × volume, quota con toponimo, quota con nomi); tabella gruppi
  (pubblico/privato, regole, leggibilità senza login); registro consolidato in `docs/`
  senza dati personali (repository pubblico, DEC-104).
- **Dipendenze effettive**: template (settimana 1) → letture; inventario Amministrazione
  → D3. La tabella gruppi serve alla questione legale 9 ma non blocca S5.
- **Parallelismo**: letture distribuite sulle settimane 1–3 (owner), in parallelo a S1;
  consolidamento in settimana 4.
- **Responsabile**: owner (lettura e classificazione); Operator (template, consolidamento);
  Codex (review); l'owner verifica la completezza.
- **Criterio di completamento**: registro su `main` con una riga per fonte prevista al
  lancio e licenza valorizzata o "da verificare" motivata; tabelle Cronaca e gruppi
  complete; i quattro Municipi a bassa resa nominati con le alternative osservate.
- **Owner**: nessuna decisione (D3 è in S6); nessuna spesa.

### S3 — Residui del pacchetto Eventi (A6): DEC-002 e DEC-003
- **Obiettivo**: chiudere DEC-002 (Colle del Sole: chiave di lookup ambigua fra Municipio VI
  e XI) e DEC-003 (cinque indirizzi del golden set geografico marcati `confidence: verify`).
  La baseline §2.A(6) le elenca come tre voci; sono due (residuo MINOR, §9.5).
- **Input**: `tests/golden_set_geographic.json`; DEC-002; DEC-003; workbook master
  `gazetteer/Rome_Neighbourhood_Gazetteer_EN.xlsx`; evidenza dagli export di S1 se presente.
- **Output**: DEC-002 DECIDED; DEC-003 chiusa; PR con golden set aggiornato e, per DEC-002
  A o B, edit del workbook e rebuild (mai a mano sui generati) con `test_guards.py` verde.
- **Dipendenze effettive**: decisione e verifiche dell'owner → PR. L'evidenza di S1 è utile,
  non necessaria (DEC-002 prevede C).
- **Parallelismo**: indipendente; la baseline la colloca in settimana 3.
- **Responsabile**: owner (verifiche, decisione); Operator (PR); Codex (review).
- **Criterio di completamento**: le due voci aggiornate su `main`; golden set senza
  `confidence: verify`; build e 37 controlli verdi.
- **Owner**: decisione DEC-002; azione DEC-003.

### S4 — Specifica Eventi v2.5: consolidamento (default) o sign-off più delta (B)
Biforcato esplicitamente (review 1, finding 1). La scelta è dell'owner all'approvazione del
piano (§6); finché non è tracciata vale la **lettura A**, cioè la baseline.
- **Lettura A — default (baseline §2.B, §4, A.2)**: consolidamento della spec Eventi con PR
  aperta dal builder, review di Codex, approvazione e merge dell'owner (15–25 h). Poiché la
  v2.5 del 28 agosto esiste ed è consolidata sul workplan (§1), il lavoro di Fase 0 sotto
  questa lettura è la versione successiva della spec che integra il delta delle decisioni
  dell'11 settembre — DEC-014 (perimetro pubblico: fallback al render come requisito di
  lancio), DEC-015 (pubblicazione automatica con doppio controllo AI e coda di eccezione:
  Part I §9), DEC-018 (architettura URL e identità dei contenuti: Part III), DEC-020
  (correzioni: modifica diretta con tracciabilità interna: versioning per item) — più
  DEC-005 decisa. Sotto-questione da confermare con la scelta: la sede del sorgente della
  spec consolidata (repository come sorgente e Drive come copia pubblicata, oppure solo
  Drive come README oggi prevede per i documenti normativi): la baseline prevede una PR,
  che presuppone un sorgente nel repository.
- **Lettura B — solo su indicazione esplicita e tracciata dell'owner**: sign-off della v2.5
  così com'è (DEC-005 decisa) più un delta documentato "DEC → sezione → modifica richiesta →
  prima di quale PR del refactor", applicato dalla prima PR del refactor in Fase 1.
- **Input**: la docx v2.5; `docs/SPEC_V25_WORKPLAN.md`; DEC-005; DEC-014…021.
- **Output**: A: spec consolidata approvata e mergiata + DEC-005; B: DEC-005 + delta su `main`.
- **Dipendenze effettive**: nessuna a monte. A valle: le prime PR del refactor (Fase 1).
- **Parallelismo**: Operator nelle settimane 1–3; revisione owner ~3 h (A.2 settimana 2);
  Codex sulla PR.
- **Responsabile**: Operator; owner (scelta della lettura, DEC-005, approvazione); Codex.
- **Criterio di completamento**: DEC-005 su `main`; per A: spec consolidata mergiata e
  copia su Drive; per B: delta su `main` con ogni voce che cita DEC e sezione.
- **Owner**: scelta della lettura; DEC-005; approvazione della spec (A).

### S5 — Avvio del percorso legale (I, D12)
- **Obiettivo**: incarico per il parere scritto sulle 13 questioni della Reconciliation §8
  con le priorità di DEC-014 (le verifiche legali bloccano solo la capacità cui si
  riferiscono), DEC-016 (Cronaca: nomi presenti nelle fonti ufficiali), DEC-019 (disclosure
  generale dell'AI, nessuna etichetta per contenuto), DEC-020 (correzioni dirette con
  tracciabilità interna), DEC-021 (configurazione pubblicitaria dell'MVP); decisione D12
  (forma societaria/editoriale, responsabile, studio legale).
- **Input**: le DEC; il testo delle 13 questioni e degli 8 requisiti di lancio (DA
  VERIFICARE: §9.3).
- **Output**: pacchetto legale; preventivi; D12 decisa; incarico conferito con data attesa
  (lead time 2–6 settimane); tabella di tracciamento questione → capacità → gate.
- **Dipendenze effettive**: localizzazione della Reconciliation → pacchetto → preventivi →
  D12 → incarico. Il parere arriva in Fase 1–2 e non è nel gate (baseline §4.2).
- **Parallelismo**: settimane 1–2 pacchetto e preventivi; D12 in settimana 2–4.
- **Responsabile**: Operator (bozza del pacchetto, tabella); owner (contatti, preventivi,
  D12, incarico).
- **Criterio di completamento**: D12 DECIDED su `main`; pacchetto inviato; incarico
  conferito con data attesa; tabella su `main`.
- **Owner**: decisione D12; autorizzazione di spesa (onorario stimato 1.500–5.000 €).

### S6 — Pacchetti decisionali e decisioni di Fase 0: D2, D3, D8, D9, D14
- **Obiettivo**: per ciascuna decisione il pacchetto della baseline A.3 (fatti, criteri,
  opzioni, costo di ciascuna), consegnato in tempo per la sessione decisionale di
  settimana 4; ogni decisione scritta in `decisions/`.
- **D2** (architettura sito/publisher e hosting): criteri §2.E con fatti di costo e
  manutenzione; effort del "contorno"; DEC-018 e DEC-020 tradotte in verifiche per opzione;
  competenze. La valutazione tecnica convergente del Council (baseline §2.E) si riporta,
  non si riapre. Prepara l'Operator. Decisione: settimana 4.
- **D3** (fonti di record Amministrazione e trascrizione): registro A2 con resa per
  Municipio (S2); prova di trascrizione di 3 video in due modalità; i quattro Municipi a
  bassa resa. Fatti dell'owner, tabella dell'Operator. Decisione: settimana 4. La prova
  può comportare spesa: autorizzazione preventiva.
- **D8** (brand: in casa vs esterno; logo unico vs sistema per quartiere): le tre opzioni
  §2.F con costo, tempi di attesa e cosa serve prima della Fase 2. Prepara l'Operator.
  Decisione: fine Fase 0; esecuzione in Fase 1.
- **D9** (strumento della coda manuale): Sheet esteso vs app minima; campi richiesti da
  DEC-015; volume stimato; costo; misura del campione stratificato. Prepara l'Operator con
  la bozza di schema di S8. Decisione: settimana 4 (condiziona la thin slice).
- **D14** (n8n self-hosted vs Cloud): fotografia reale dell'infrastruttura (§9.2), fatti di
  settimana 2, i due rami stimati §2.H, impatto sul refactor. Fatti dell'owner, pacchetto
  dell'Operator. Decisione: settimana 4, prima del refactor B.
- **Dipendenze effettive**: D3 ← S2 e prova; D9 ← S8-01; D14 ← fotografia n8n; D2 e D8 ←
  fatti di costo.
- **Parallelismo**: pacchetti nelle settimane 2–3; decisioni accorpate in settimana 4.
- **Responsabile**: Operator (pacchetti, bozze DEC); owner (fatti D3/D14, decisioni);
  Codex (review delle PR dei pacchetti).
- **Criterio di completamento**: cinque DEC DECIDED su `main` con opzioni, raccomandazione,
  impatto e `Blocks:`; nessuna decisione per omissione.
- **Owner**: cinque decisioni; autorizzazione alla prova di trascrizione.

### S7 — Governance e documentazione della fase (K)
- **Obiettivo**: baseline e decisioni dell'11 settembre su `main`; documenti allineati;
  diario del tempo attivo; metodo di M2 e M3 pronto; disciplina `staging_`; revisione
  mensile; piano esecutivo approvato. Regola operativa per il tetto di quattro cicli
  (DEC-012, corsie come livelli di attenzione dell'owner; baseline §2.K): ogni PR
  dimensionata per chiudere in tre cicli.
- **Input**: branch dell'11 settembre; `docs/strategic-council/PROJECT_BRIEF.md` (fermo al
  31 agosto); `docs/START_HERE.md` §6 e `docs/NEXT_SESSION_BRIEF.md` (dicono che la spec
  v2.5 manca); README (37 vs 38 controlli).
- **Output**: PR della baseline e delle DEC-014…021; PR di questo piano e del registro; PR
  di allineamento (pointer, non copie); diario del tempo (foglio in QN Hub/00 Governance,
  snapshot mensile in `docs/`); note di metodo M2 e M3; proposta di ristima di §4 della
  baseline a fine fase, come candidato.
- **Dipendenze effettive**: il merge della baseline su `main` precede il merge di ogni
  documento che cita DEC-014…021 (vincolo di ordine di merge, review 1 finding 3: la
  stesura in branch è parallela dalla settimana 1); la ristima ← S1 e S6.
- **Parallelismo**: settimana 1 per PR, diario, template; continuo per il resto.
- **Responsabile**: Operator (PR); owner (merge, diario); Codex (review).
- **Criterio di completamento**: baseline, DEC-014…021 e piano su `main`; diario con
  quattro settimane; M2/M3 su `main`; documenti allineati.
- **Owner**: merge; approvazione del piano.

### S8 — Preparazione della Fase 1 in sovrapposizione (7,5 h/settimana) — non costruzione
- **Obiettivo**: quanto la baseline A.2 assegna alla Fase 1 in sovrapposizione: schema
  della coda unica (bozza; DEC-103, modello di revisione coda + campione settimanale, e
  DEC-015); prompt di record della seconda AI e controlli deterministici (bozza, nessun
  provider: D7 è di Fase 1); design della thin slice C.
- **Output**: tre bozze in `docs/`, marcate come tali; fuori dal gate.
- **Dipendenze effettive**: S8-01 → D9; design della thin slice ← S2 e D3.
- **Responsabile**: Operator; Codex sulle PR; nessuna decisione dell'owner.
- **Criterio di completamento**: bozze su `main`, citate da D9. Confine: nessun prompt
  cablato, nessun workflow, nessun provider.

## 4. Sottotask (Livello B)

Colonne: ID · Azione · Esecutore · Verificatore · Input · Dipendenze · Output atteso ·
Criterio di accettazione · Evidenza (dove) · Owner (decisione/autorizzazione). Sedi:
`docs/measures/`, `docs/sources/`, `docs/decision-packs/`, `docs/legal/`, `docs/drafts/`
sono sottocartelle nuove del prefisso GREEN `docs/` (corsia calcolata dal gate; ogni PR è
unita dall'owner). I dati grezzi e i documenti riservati stanno su Drive (QN Hub), mai nel
repository pubblico.

### S0 — Sicurezza
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S0-01 | Inventario delle credenziali esposte: nome, servizio, sedi d'uso (n8n, ambiente dell'Operator, PC, altro); mai i valori | owner | Operator (sulla lista) | baseline §1 R0 | — | lista nella bozza DEC | quattro credenziali con tutte le sedi d'uso | bozza DEC in branch | — |
| P0-S0-02 | Rotazione: revoca delle vecchie ed emissione delle nuove; custodia in gestore di segreti, credenziali n8n o secret GitHub | owner | Operator (funzionale, S0-03) | S0-01 | S0-01 | credenziali nuove custodite | le vecchie non funzionano più; le nuove sì | data e sede per credenziale nella DEC | azione D1 |
| P0-S0-03 | Aggiornamento delle sedi d'uso (credenziali n8n; ambiente di esecuzione dell'Operator: chiave OpenAI del Council, token GitHub) e verifica funzionale | owner | Operator | S0-02 | S0-02 | un run di staging e una chiamata del Council riusciti | entrambi riusciti con le nuove credenziali | log del run (Drive staging); registro del Council | — |
| P0-S0-04 | Bonifica documentale: documento Drive svuotato o cestinato e cestino svuotato; copia locale eliminata o cifrata dopo la migrazione; ricerca su Drive di altri documenti con credenziali (esito, senza valori) | owner | Operator (ricerca per titolo) | S0-01 | — | esito nella DEC | nessun documento Drive con credenziali in chiaro | DEC | — |
| P0-S0-05 | Verifica raccomandata (fuori gate): secret scanning GitHub del repository e ricerca nella cronologia git per pattern, senza stampare valori | Operator | owner | repository | — | esito nella DEC | nessun alert aperto, o alert tracciati | DEC | — |
| P0-S0-06 | Voce DEC D1: sede di custodia dei segreti, regola "mai in documenti condivisibili", chi detiene cosa; PR e merge | Operator (bozza) | Codex (PR) | S0-01…05 | S0-02, S0-03, S0-04 | DEC DECIDED su `main` | formato di `decisions/README.md`; `Blocks:` valorizzato | `decisions/` | decisione D1 |

### S1 — M1
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S1-01 | Nota di metodo M1: evento futuro distinto, finestra 30 giorni, livelli deterministici, pavimento/soffitto, fallback al Municipio, campione manuale, vita media, formato della tabella, limiti | Operator | Codex (PR) | baseline §2.A(1), §6; `zone_distribution.py`; DEC-006 (regola non agostana) | — | `docs/measures/M1_METHOD.md` | ogni voce definita; nessun dato personale | `main` | — |
| P0-S1-02 | Staging: cartelle Drive e collezioni Firestore `staging_`, copia del workflow con le credenziali nuove, prova su 5 URL; export del workflow di staging in PR se la struttura cambia (`workflows/README.md`) | owner | Operator | S0-03 | S0-03 | staging pronto | la prova scrive solo in `staging_` | export + log | — |
| P0-S1-03…06 | Settimane 1–4: raccolta URL (Facebook Events, area Roma, finestra 30 giorni, snippet → Sheet), run in staging, export grezzo su Drive, riga nel diario | owner | Operator (conteggio) | S1-02 per il run | S1-02 | quattro export datati | ogni export con data, numero URL, numero eventi | Drive (cartella M1 o staging) | autorizzazione ai run Apify |
| P0-S1-07 | Campione manuale: ~15 eventi/settimana non localizzati dal deterministico, zona assegnata a mano o "non localizzabile" | owner | Operator | S1-03… | — | foglio del campione | ~60 righe con esito | Drive | — |
| P0-S1-08 | Conteggi: `zone_distribution.py` sui quattro export (scaricati localmente, mai committati); tabella per pagina (89) e Municipio (15): pavimento, soffitto, fallback, quota localizzabile stimata, vita media | Operator | Codex (PR) | S1-06, S1-07 | S1-06 | `docs/measures/M1_EVENTS_PER_PAGE.md` | 89 + 15 righe; metodo citato; soli conteggi | `main` | — |
| P0-S1-09 | Lettura dello scenario M1 (tabella di ristima della baseline §6) e input per D4/D5 di Fase 1 | Operator | owner | S1-08 | S1-08 | sezione nella stessa PR | scenario dichiarato con i numeri; nessuna decisione presa | `main` | — |

### S2 — Fonti
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S2-01 | Template del registro fonti: colonne (fonte, blocco, Municipio, tipo, URL, formato, cadenza, anticipo, ritardo, licenza/termini, resa attesa, note), valori ammessi per licenza, regola "nessun dato personale" | Operator | Codex (PR) | baseline §2.A(2)(5) | — | `docs/sources/SOURCE_REGISTRY.md` con istruzioni | colonne e valori definiti | `main` | — |
| P0-S2-02 | Inventario Amministrazione: 15 Municipi + Roma Capitale, in tre lotti (3 → 8 → 16): canali, URL, formato, cadenza, anticipo/ritardo, licenza, resa attesa/mese | owner | Operator (completezza) | *Next Step*; S2-01 | S2-01 | righe nel registro | 16 enti; i quattro a bassa resa con alternative | `main` (PR per lotto o a fine) | — |
| P0-S2-03 | Cronaca: sei fonti (Questura/Polizia di Stato, Carabinieri, Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza), un mese di comunicati contato: volume, quota con toponimo, quota con nomi | owner | Operator | S2-01 | — | tabella nel registro | sei fonti × tre numeri | `main` | — |
| P0-S2-04 | Gruppi Facebook: dal foglio *Gruppi Facebook*: conteggio verificato, pubblico/privato, regole, leggibilità senza login; nessun dato personale | owner | Operator | S2-01 | — | tabella nel registro | ogni gruppo censito classificato | `main` | — |
| P0-S2-05 | Registro unico consolidato con licenza/termini per fonte | Operator | Codex (PR) | S2-02…04 | S2-02…04 | registro su `main` | una riga per fonte prevista al lancio; licenza valorizzata o "da verificare" motivata | `main` | — |

### S3 — Residui Eventi
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S3-01 | DEC-003: verifica dei cinque indirizzi (mappa o campo) e valori attesi | owner | Operator | golden set | — | cinque valori | confermati o corretti | DEC-003 aggiornata | azione |
| P0-S3-02 | DEC-002: decisione A/B/C sull'evidenza (eventi ai due luoghi negli export di S1, se presenti; altrimenti C) | owner | Operator | DEC-002; export S1 | — | DEC-002 DECIDED | opzione motivata | `decisions/` | decisione |
| P0-S3-03 | PR: golden set aggiornato; per A/B edit del workbook master e rebuild; `test_guards.py` verde | Operator | Codex | S3-01, S3-02 | S3-01, S3-02 | PR mergiata | nessun `confidence: verify`; build e 37 controlli verdi | `main` | merge |

### S4 — Specifica Eventi
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S4-01 | DEC-005 (migrazione allo schema 2.0): decisione sull'entry esistente | owner | — | DEC-005 | — | DEC-005 DECIDED | — | `decisions/` | decisione |
| P0-S4-02 | Delta DEC-014…021 → spec: tabella DEC → sezione → modifica richiesta → prima di quale PR del refactor (serve a entrambe le letture) | Operator | Codex (PR) | docx v2.5; DEC-014, 015, 018, 020 | — | `docs/SPEC_V25_DELTA_DEC_014_021.md` | ogni voce cita DEC e sezione | `main` | conferma della lettura |
| P0-S4-03 | Lettura A (default): consolidamento della spec — sorgente della versione successiva nella sede scelta, delta integrato, PR aperta dal builder, review Codex, risposte, approvazione e merge dell'owner; copia su Drive `10 Specifications` | Operator | Codex (PR); owner (approvazione) | S4-01, S4-02; docx v2.5 | S4-02; scelta della sede | spec consolidata approvata | nessun restatement di regole che vivono in `gazetteer.json` (regola della spec); tutte le voci del delta integrate | `main` + Drive | approvazione |
| P0-S4-04 | Lettura B (solo se indicata dall'owner): sign-off della v2.5 così com'è registrato in `decisions/` con DEC-005; il delta S4-02 resta l'input della prima PR del refactor | owner | Operator | S4-01, S4-02 | S4-02 | sign-off registrato | — | `decisions/` | indicazione esplicita |

### S5 — Legale
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S5-01 | Localizzazione della Round 2 Reconciliation (13 questioni, 8 requisiti) e deposito in una sede di record (QN Hub/00 Governance; o `docs/strategic-council/` se senza dati personali) | owner | Operator | — | — | documento reperibile | le 13 questioni e gli 8 requisiti leggibili | sede scelta | azione |
| P0-S5-02 | Pacchetto legale: 13 questioni con priorità; decisioni assunte come ipotesi di rischio (DEC-016, 019, 020, 021); pagine previste; tabella capacità → gate (baseline §4.1) | Operator | owner | S5-01; DEC | S5-01 | `docs/legal/LEGAL_PACK_2026-09.md` (Drive se riservato) | completo e letto dall'owner | `main` o Drive | — |
| P0-S5-03 | Richiesta di preventivi a 2–3 studi | owner | — | S5-02 | S5-02 | preventivi | almeno due ricevuti | Drive (riservato) | — |
| P0-S5-04 | Pacchetto D12: forma societaria/editoriale, responsabile, studio; cosa blocca il go-live | owner (fatti) + Operator (tabella) | owner | S5-03 | S5-03 | `docs/decision-packs/D12.md` | opzioni con costi e tempi | `main` | — |
| P0-S5-05 | D12: decisione e autorizzazione di spesa | owner | — | S5-04 | S5-04 | DEC DECIDED | — | `decisions/` | decisione + autorizzazione |
| P0-S5-06 | Incarico conferito; data attesa del parere; tabella di tracciamento questione → capacità → gate | owner (incarico) + Operator (tabella) | owner | S5-05 | S5-05 | lettera d'incarico (Drive riservato); tabella | data attesa registrata | Drive + `main` | — |

### S6 — Pacchetti decisionali
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S6-01 | Fotografia n8n: istanze esistenti (VPS Aruba, progetto Cloud), dove gira il workflow definitivo, versione, aggiornamenti, backup, costi correnti | owner | Operator | §9.2 | — | fatti nel pacchetto D14 | le tre fonti contraddittorie riconciliate | `docs/decision-packs/D14.md` | — |
| P0-S6-02 | Pacchetto D14: i due rami di baseline §2.H con i fatti; impatto sul refactor | Operator | Codex (PR) | S6-01 | S6-01 | pacchetto | criteri e costi per ramo | `main` | — |
| P0-S6-03 | Pacchetto D2: criteri §2.E con fatti di costo e manutenzione; effort del "contorno"; DEC-018 e DEC-020 come verifiche; competenze | Operator | Codex (PR) | baseline §2.E | — | `docs/decision-packs/D2.md` | ogni opzione valutata su ogni criterio | `main` | — |
| P0-S6-04 | Prova di trascrizione: 3 video di commissione × 2 modalità; costo e qualità per ora di video | owner | Operator (tabella) | S2-02 (video scelti) | autorizzazione | risultati | numeri per modalità | `docs/decision-packs/D3.md` | autorizzazione di spesa |
| P0-S6-05 | Pacchetto D3: registro A2, prova, i quattro Municipi a bassa resa | Operator | Codex (PR) | S2-05, S6-04 | S2-05, S6-04 | pacchetto | — | `main` | — |
| P0-S6-06 | Pacchetto D8: le tre opzioni §2.F con costo, attesa, cosa serve prima della Fase 2 | Operator | Codex (PR) | baseline §2.F | — | `docs/decision-packs/D8.md` | — | `main` | — |
| P0-S6-07 | Pacchetto D9: Sheet esteso vs app minima; campi DEC-015; volume stimato; costo; campione stratificato | Operator | Codex (PR) | S8-01 | S8-01 | `docs/decision-packs/D9.md` | — | `main` | — |
| P0-S6-08 | Sessione decisionale (settimana 4): D2, D3, D8, D9, D14 — bozze DEC dell'Operator, decisione dell'owner, PR, merge | owner | Codex (PR) | S6-02…07 | tutti i pacchetti | cinque DEC DECIDED | formato del registro; `Blocks:` valorizzato | `main` | decisioni |

### S7 — Governance
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S7-01 | PR della branch dell'11 settembre (baseline + DEC-014…021) verso `main` | Operator (apre) | Codex; owner (merge) | branch esistente | — | merge | su `main` | `main` | merge |
| P0-S7-02 | PR di questo piano e del registro delle review, dopo l'approvazione dell'owner | Operator | Codex; owner | questo documento | approvazione; S7-01 (ordine di merge) | merge | su `main` | `main` | approvazione + merge |
| P0-S7-03 | Allineamento documenti: `docs/START_HERE.md` §6, `docs/NEXT_SESSION_BRIEF.md`, README (37/38), `PROJECT_BRIEF.md` — pointer, non copie | Operator | Codex (PR) | S7-01 | S7-01 (ordine di merge) | PR | nessun documento dichiara la spec mancante; il brief cita DEC-014…021 | `main` | — |
| P0-S7-04 | Diario del tempo: foglio in QN Hub/00 Governance (data, flusso, attività/PR, ore, cicli, note); snapshot mensile in `docs/measures/` | owner (compila) + Operator (template) | owner | — | — | foglio attivo | quattro settimane compilate a fine fase | Drive + `main` | — |
| P0-S7-05 | Note di metodo M2 (ore e cicli per PR sui primi tre PR del refactor) e M3 (tasso di eccezione e minuti per caso della thin slice) con le soglie della baseline §6 | Operator | Codex (PR) | baseline §6 | — | `docs/measures/M2_M3_METHOD.md` | misure, sede, soglie definite | `main` | — |
| P0-S7-06 | Proposta di ristima di §4 della baseline (candidato; la baseline non si modifica senza approvazione) | Operator | owner | S1-09, S6-08 | S1-09, S6-08 | documento candidato | consegnato | branch/PR | decisione |
| P0-S7-07 | Cadenza mensile di revisione del piano; prima revisione a fine Fase 0 | owner | — | — | — | data fissata | — | diario | — |

### S8 — Preparazione Fase 1
| ID | Azione | Esecutore | Verificatore | Input | Dipendenze | Output | Accettazione | Evidenza | Owner |
|---|---|---|---|---|---|---|---|---|---|
| P0-S8-01 | Bozza dello schema della coda unica per tutti i blocchi (motivi strutturati, campi minimi) | Operator | Codex (PR) | `docs/REVIEW_QUEUE.md`, DEC-103, DEC-015 | — | `docs/drafts/QUEUE_SCHEMA_DRAFT.md` | marcata bozza; input di D9 | `main` | — |
| P0-S8-02 | Bozza del prompt di record della seconda AI di verifica e dei controlli deterministici (nessun provider) | Operator | Codex (PR) | DEC-015 | — | `docs/drafts/VERIFIER_PROMPT_DRAFT.md` | marcata bozza; nessun cablaggio | `main` | — |
| P0-S8-03 | Design della thin slice C: 2–3 Municipi eterogenei, golden set da 30 item, misure | Operator | Codex (PR) | S2-05; D3 | S2-05 | `docs/drafts/THIN_SLICE_DESIGN.md` | marcata bozza | `main` | — |

## 5. Dipendenze effettive, ordine di merge e parallelismo

Vincoli reali: S0 → primo run in staging (S1-02) e credenziali dell'Operator (S0-03);
quarto run → tabella M1 (S1-08); S2-02 → D3; Reconciliation (S5-01) → pacchetto legale →
preventivi → D12 → incarico; S8-01 → D9; fotografia n8n (S6-01) → D14; tutti i pacchetti →
sessione decisionale (S6-08); S1-09 e S6-08 → ristima (S7-06); S4 (lettura scelta) → prime
PR del refactor (Fase 1, fuori).

Vincolo di ordine di merge (non di stesura): la PR della baseline (S7-01) va unita a `main`
prima di ogni documento che cita DEC-014…021; la stesura di tutto procede in branch dalla
settimana 1.

Preferenze di sequenza (non vincoli): l'ordine settimanale dell'Appendice A.2 per S2; S3 in
settimana 3.

| Banda | Owner (22,5 h/sett. di Fase 0) | Operator | In attesa |
|---|---|---|---|
| Settimana 1 | S0 (1–2 h); S1-03 raccolta URL; S1-02 staging dopo S0; S2-02 lotto 1; S5-01 Reconciliation; S7-04 diario | S0-06 bozza D1; S1-01 metodo; S2-01 template; S4-02 delta; S5-02 pacchetto legale; S7-01 PR baseline; S7-05 M2/M3; S8-01 | — |
| Settimana 2 | S1-04; S2-02 lotto 2; S6-01 fotografia n8n; S6-04 prova trascrizione (se autorizzata); S5-03 preventivi; revisione della spec (S4) | S4-03 (A) o S4-04 (B); S6-02 D14; S6-03 D2; S6-06 D8; S8-02 | parere: non ancora |
| Settimana 3 | S1-05; S2-02 lotto 3; S2-03 Cronaca; S2-04 gruppi; S3-01/02; S1-07 campione | S3-03 PR; S6-05 D3; S6-07 D9; S7-03 allineamento; S8-03 | — |
| Settimana 4 | S1-06; S6-08 decisioni; S5-05 D12; S4-01 DEC-005; S7-07 | S1-08/09 conteggi; S2-05 registro; S6-08 bozze DEC; S7-06 ristima | incarico legale conferito (S5-06) |

## 6. Decisioni e autorizzazioni dell'owner, con il momento

| Quando | Cosa | Preparato da |
|---|---|---|
| All'approvazione di questo piano | Approvazione del piano; conferma della corrispondenza baseline ↔ commit `7873b11`; **scelta della lettura di S4** (A default / B) e della sede del sorgente della spec; localizzazione della Reconciliation; autorizzazione ai quattro run Apify; conferma dello stato reale di n8n (per il pacchetto D14) | Operator (questo documento) |
| Settimana 1 | **D1** (esecuzione della rotazione; decisione sulla sede di custodia) — blocco di sicurezza | owner; bozza DEC dell'Operator |
| Settimana 2 | Autorizzazione alla prova di trascrizione se a pagamento (D3); scelta dello studio da interpellare (D12, prima parte) | Operator (pacchetto legale); owner (preventivi) |
| Settimana 2–4 | **DEC-005** (migrazione allo schema 2.0); approvazione della spec consolidata se lettura A | Operator |
| Settimana 3 | **DEC-002** (Colle del Sole); **DEC-003** (cinque indirizzi) | owner (verifiche) |
| Settimana 4 | **D2, D3, D8, D9, D14** in una sessione; **D12** con autorizzazione di spesa per l'incarico; lettura della proposta di ristima | Operator (pacchetti e bozze DEC) |
| Merge | Ogni PR della fase (l'owner unisce; DEC-012, DEC-013) | — |

Nessuna scelta è chiesta senza pacchetto: ogni riga sopra rimanda a una sottotask che lo
produce.

## 7. Gate di chiusura della Fase 0

1. D1 DECIDED su `main`; vecchie credenziali revocate; documento esposto rimosso;
   operatività con le nuove credenziali verificata (S0).
2. Tabella M1 su `main` (89 pagine, 15 Municipi, quattro settimane osservate) con nota di
   metodo e scenario letto (S1).
3. Registro fonti unico su `main` con licenza/termini per fonte; tabelle Cronaca e gruppi
   (S2).
4. DEC-002 e DEC-003 chiuse; golden set corretto; build e controlli verdi (S3).
5. DEC-005 decisa; secondo la lettura scelta: spec consolidata approvata e mergiata (A) o
   sign-off registrato più delta su `main` (B) (S4).
6. D12 decisa; incarico legale conferito con data attesa del parere; tabella di
   tracciamento su `main` (S5).
7. D2, D3, D8, D9, D14 DECIDED su `main` (S6).
8. Baseline, DEC-014…021 e piano esecutivo su `main`; diario con quattro settimane; metodo
   M2/M3 su `main`; documenti allineati (S7).
9. Proposta di ristima di §4 consegnata all'owner come candidato (S7-06).

Fuori dal gate: S8 (bozze), D4, D5, D7, DEC-001, DEC-004, il parere legale, il secret
scanning (raccomandato).

## 8. Primo gruppo di task dopo l'approvazione

**Blocco di sicurezza** (prima di ogni run in staging e prima che l'Operator riprenda a
lavorare con le credenziali attuali): P0-S0-01…04 (owner, 1–2 h), P0-S0-03 aggiornamento
delle credenziali negli ambienti degli agenti, P0-S0-06 bozza e decisione D1.

**In parallelo, lo stesso giorno, senza credenziali**: P0-S1-03 raccolta URL settimana 1
(owner); P0-S2-01 template e P0-S2-02 lotto 1 (Operator, owner); P0-S1-01 metodo M1
(Operator); P0-S4-02 delta (Operator); P0-S5-01 localizzazione della Reconciliation (owner)
e P0-S5-02 pacchetto legale (Operator); P0-S7-01 PR della baseline (Operator apre, owner
unisce); P0-S7-04 diario (owner); P0-S7-05 metodo M2/M3 e P0-S8-01 (Operator).

**Dopo S0**: P0-S1-02 staging e primo run.

**Autorizzazioni da dare con l'approvazione**: quattro run Apify (servizio esistente);
prova di trascrizione a pagamento (D3, settimana 2); incarico legale al momento di D12.
Nessun altro servizio a pagamento, nessun incarico a terzi, nessuna modifica in produzione
è prevista in Fase 0.

## 9. Contraddizioni materiali isolate e residui

9.1 **Specifica v2.5**: già consolidata (docx del 28 agosto, contratto per README, AGENTS.md,
PROJECT_BRIEF) vs "consolidamento" assegnato alla Fase 0 dalla baseline (§2.B, §4, A.2).
Trattata con la biforcazione di S4 (lettura A default = baseline; B su indicazione
dell'owner). Impatto: sotto A, 15–25 h producono la versione successiva con il delta delle
decisioni dell'11 settembre e va scelta la sede del sorgente; sotto B, ore inferiori e il
delta si applica in Fase 1.

9.2 **n8n Cloud o self-hosted**: spec v2.5 e README dicono n8n Cloud (istanza
`quartierinews.app.n8n.cloud`, progetto condiviso); baseline §1 dice VPS Aruba
self-hosted; l'inbox del Technical Council del 14 settembre (PR #14) dice Cloud Starter.
Letture possibili (review 1): prevale la baseline (self-hosted), oppure coesistenza o
trasferimento già avviato verso Cloud. Impatto: il pacchetto D14 parte dalla fotografia
verificata (P0-S6-01); la domanda potrebbe diventare "quale istanza tenere". Non blocca la
pianificazione.

9.3 **Round 2 Reconciliation non disponibile** (13 questioni legali, 8 requisiti di
lancio; la baseline §4.1 ne nomina 12, manca la 11). Impatto: S5 non completa il pacchetto
legale senza; gate 6 dipende dalla localizzazione (P0-S5-01). Nessuna lettura alternativa:
serve l'owner.

9.4 **Baseline e DEC-014…021 non su `main`**: la loro PR (P0-S7-01) precede nell'ordine di
merge ogni documento che le cita, questo incluso.

9.5 **Minori**: DEC-003 citata due volte come voci distinte nella baseline §2.A(6); 37 vs
38 controlli (README vs START_HERE); PROJECT_BRIEF fermo al 31 agosto. Segnalati e
trattati da P0-S7-03; la baseline non è modificata.

## 10. Registro delle review del Council

| Review | Versione esaminata | Verdetto di Codex | Finding | Esito |
|---|---|---|---|---|
| 1 (Livello A, step) | proposal A-0.1, sha256 `fc8b953d…` | AGREEMENT WITH NON-BLOCKING RESIDUALS | 2 IMPORTANT (S4 biforcazione; gate S0), 1 MINOR (S7a) | tutti accettati e applicati in B-0.2; controverifica nella review 2 |
| 2 (Livello B, sottotask) | questo documento, B-0.2 | — | — | — |
| 3 (versione candidata finale) | — | — | — | — |

I report per ciclo sono in `reviews/` con il nome `2026-09-14—cycleN—phase-0-execution—<verdetto>.md`
(DEC-007, dove si archivia una code review: la PR è l'archivio; `reviews/` resta la sede
dei report non legati a una PR — questo Council non è una PR).

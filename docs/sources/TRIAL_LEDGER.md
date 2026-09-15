# Ledger delle prove preliminari (S2-06)

Tetto autorizzato dall'owner il 14 settembre 2026: **50 € complessivi**, tutto incluso
(chiamate AI, ripetizioni, conversioni, imposte). Nessun abbonamento, nessuna ricarica
automatica. Lo studio si ferma prima di superare il tetto e presenta risultati, lacune e
motivazione di un'eventuale richiesta. T6 (quattro raccolte settimanali) non è coperta: è
preventivata e richiede un'autorizzazione successiva sulla previsione.

Regola fail-closed (metodo §7): T1, T3 e T4 sono bloccate finché l'owner non conferma per
iscritto che la chiave OpenAI dell'ambiente è distinta da quella esposta in R0, o la
rotazione è completata e verificata. Al 15 settembre 2026 la rotazione non è avvenuta:
T1, T3, T4 e T5 restano ferme; nessuna chiamata AI è stata fatta nella sessione del 15
settembre.

**Costi API dei controlli Codex** (richiesta dell'owner del 15 settembre): i token sono
quelli registrati nei report in `reviews/` (usage della Responses API, `store: false`); il
prezzo unitario è **stimato** da listini di terze parti raggiunti con la ricerca web
(1,75 $/M token in ingresso, 14,00 $/M in uscita, reasoning incluso nell'uscita; il listino
ufficiale `developers.openai.com` non è raggiungibile dall'ambiente) e convertito a
0,92 €/$ (ipotesi prudente). I due controlli del metodo dello studio sono a carico del tetto;
le tre review del piano di Fase 0 sono riportate per completezza (stesso mezzo, step
precedente) e contate anch'esse a carico del tetto finché l'owner non indica altrimenti.

| Data | Prova | Quantità | Costo (€) | Residuo (€) | Note |
|---|---|---|---|---|---|
| 2026-09-14 | Codex, review piano Fase 0 ciclo 1 (`gpt-5.3-codex`) | 36.284 in / 11.780 out | 0,21 (S) | 49,79 | `reviews/2026-09-14—cycle1—phase-0-execution—…` |
| 2026-09-14 | Codex, review piano Fase 0 ciclo 2 | 42.882 in / 9.841 out | 0,20 (S) | 49,59 | `reviews/2026-09-14—cycle2—phase-0-execution—…` |
| 2026-09-14 | Codex, review piano Fase 0 ciclo 3 | 46.375 in / 9.573 out | 0,20 (S) | 49,39 | `reviews/2026-09-14—cycle3—phase-0-execution—…` |
| 2026-09-14 | Codex, controllo metodo fonti 1 (M-0.1) | 13.262 in / 9.668 out | 0,15 (S) | 49,24 | `reviews/2026-09-14—sources-study-method—NO_AGREEMENT.md` |
| 2026-09-14 | Codex, controllo metodo fonti 2 (M-0.2) | 12.680 in / 6.020 out | 0,10 (S) | 49,14 | `reviews/2026-09-14—sources-study-method-v2—AGREEMENT_WITH_NON-BLOCKING_RESIDUALS.md` |
| 2026-09-15 | T2 (parziale): estrazione testo da 18 PDF di Atti Web con PyMuPDF/pypdf locali | 18 PDF, 10 con testo, 8 scansioni; nessun OCR eseguito | 0,00 | 49,14 | `docs/sources/SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md` §6; OCR (T2 parte scansioni) non eseguito: richiede chiave AI (bloccata) o `tesseract` (assente) |
| 2026-09-15 | Letture HTML/RSS/API del livello 1 (fetch e parser locali) | ≈ 2.100 richieste HTTP | 0,00 | 49,14 | nessun servizio a pagamento |
| 2026-09-15 | Verifica A2: sweep delle 48 tipologie di Atti Web, DDS di giugno e maggio, controlli; letture E3 (livello 2) | ≈ 330 richieste HTTP | 0,00 | 49,14 | nessun servizio a pagamento; `docs/sources/A2_ATTIWEB_TIPOLOGIE.md` |
| 2026-09-15 | Approfondimento A2 autorizzato dall'owner: 31 PDF (10 DDS, 5 centrali, 5 CPC, 5 CPV, 3 SO, CID, MCD, OCD) letti in locale, 14 controlli API | ≈ 60 richieste HTTP | 0,00 | 49,14 | nessun servizio a pagamento; nota A2 §7 |
| 2026-09-15 | Ricognizione video A3/A4: elenchi di 13 canali YouTube (5.273 voci), letture per video e sottotitoli automatici (16 validi, campione completato), 3 liste e 77 PDF di Atti Web; RomaTV censita via API dopo l'apertura degli host (496 voci, 7 trascrizioni WebVTT) | ≈ 60 letture di elenchi, ≈ 105 letture per video, ≈ 40 tentativi di sottotitoli, ≈ 100 richieste Atti Web, ≈ 70 richieste RomaTV | 0,00 | 49,14 | nessun servizio a pagamento; `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md` |
| 2026-09-15 | Misure per l'analisi di fattibilità (pomeriggio, dopo l'apertura degli host media): 82 JSON del riconoscimento vocale di RomaTV (≈ 40 MB), 3 stream audio a segmenti (≈ 470 segmenti, ≈ 70 MB) e chiave AES; 120 PDF di Atti Web (campione con seed); OCR locale RapidOCR su 3 pagine; sonde E1 (23 chunk JS, 8 chiamate API); ricerca web dei listini | ≈ 650 richieste HTTP, 2 installazioni da PyPI | 0,00 | 49,14 | nessun servizio a pagamento, nessuna chiamata AI; `docs/sources/FATTIBILITA_RICOSTRUZIONE_2026-06.md` §1.3 |
| 2026-09-15 | Strumenti di verifica per il preventivo aggiornato: Tesseract 5.3.4 con lingua italiana installato dai repository di sistema; confronto con RapidOCR su 5 pagine scansionate; terzo stream audio RomaTV (Consiglio del XV) in download a segmenti | 1 installazione di sistema, ≈ 500 richieste HTTP | 0,00 | 49,14 | nessun servizio a pagamento, nessuna chiamata AI; `FATTIBILITA_RICOSTRUZIONE_2026-06.md` §8.1 |
| 2026-09-15 | Misure sui vincoli dell'ambiente per il calendario minimo (§8.4 della nota di fattibilità): log della sessione (turni, attese, compattazioni), metadati di sessione (quota, consumo), tempi di scaricamento ricavati dai segmenti audio già presenti, pagina della documentazione di Claude Code | 1 lettura web, nessuna richiesta alle fonti | 0,00 | 49,14 | nessun servizio a pagamento, nessuna chiamata AI; `FATTIBILITA_RICOSTRUZIONE_2026-06.md` §8.3.1, §8.4, §8.5 |
| 2026-09-15 | Lotto di misura su Opus 5 (richiesta dell'owner): due subagenti in parallelo, 10 trascrizioni di Consigli RomaTV e 30 atti di Atti Web (13 con OCR Tesseract locale), 18 minuti di orologio, 56 notizie candidate; quota Max: finestra di 5 ore da 40% a 43%, settimana da 2% a 3% (letture dell'owner) | 40 item, 0 richieste alle fonti | 0,00 | 49,14 | nessun servizio a pagamento, nessuna chiamata AI esterna; utilizzo incluso nell'abbonamento; `FATTIBILITA_RICOSTRUZIONE_2026-06.md` §9.3 |
| 2026-09-15 | Verifica della nuova chiave OpenAI (sola lettura, solo codice HTTP) e controllo Codex C1: schema del database e regole di collegamento, prima dell'estrazione (`gpt-5.3-codex`, effort high, `store: false`) | 1 richiesta di verifica (HTTP 200); 13.377 in / 11.079 out | 0,16 (S) | 77,84 | `reviews/2026-09-15—ricostruzione-2026-06-schema-db—CHANGES_REQUESTED.md`; 11 rilievi bloccanti e 1 non bloccante, tutti accettati |

Totale speso: **1,02 € (stimato)**; residuo **77,84 €** sul tetto complessivo di **78,86 €**
(50 € iniziali più l'aumento di 28,86 € autorizzato dall'owner la sera del 15 settembre per
l'esecuzione una tantum di giugno 2026: trascrizioni, seconda AI, verifiche, ripetizioni e
controlli Codex compresi; nessun "extra usage"; nessun automatismo mensile). Nessuna prova a pagamento eseguita
dall'Operator; nessun abbonamento.

## Controlli Codex: conclusi e previsti (aggiornato il 15 settembre, sera)

| Controllo | Stato | Costo (€) | Evidenza |
|---|---|---|---|
| Review del piano di Fase 0, cicli 1–3 (14 settembre) | concluso | 0,61 | `reviews/2026-09-14—cycle1..3—phase-0-execution—…` |
| Controllo del metodo fonti M-0.1 e M-0.2 (14 settembre) | concluso | 0,25 | `reviews/2026-09-14—sources-study-method…` |
| C1: schema del database e regole di collegamento e deduplicazione, prima dell'estrazione | **concluso** il 15 settembre, CHANGES_REQUESTED, 12 rilievi accettati | 0,16 | `reviews/2026-09-15—ricostruzione-2026-06-schema-db—CHANGES_REQUESTED.md` |
| C2: campione del Report 1 (notizie candidate con evidenze, copertura, tempestività) | previsto, giorno 2 | ≈ 0,3–0,5 | `reviews/` |
| C3: campione del Report 2 (atti e video: nuove informazioni, deduplicazione, localizzazione) | previsto, giorno 4–5 | ≈ 0,3–0,5 | `reviews/` |
| C4: consegna finale (rapporto, aggregati, lacune, costi effettivi) | previsto, giorno 5 | ≈ 0,3–0,5 | `reviews/` |
| C5: revisione della PR dei rapporti | previsto, giorno 5 | ≈ 0,2 | PR |

I cinque controlli previsti valgono ≈ 2 € dentro il tetto di 78 €. Usano la nuova chiave OpenAI
dopo la verifica di funzionamento, eseguita il 15 settembre alle 20:07 con esito HTTP 200
(`tools/sources-study/session_b/STATO.md`); il segreto non è stato mostrato né registrato.
Lo strumento dei controlli è `tools/sources-study/codex_check.js`: è il revisore tecnico, distinto
da `council/cli.js`, che DEC-008 fissa sul modello di ragionamento e che rifiuta i modelli di
codice per costruzione.

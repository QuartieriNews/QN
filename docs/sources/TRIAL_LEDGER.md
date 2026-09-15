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

Totale speso: **0,86 € (stimato)**; residuo **49,14 €**. Nessuna prova a pagamento eseguita
dall'Operator; nessun abbonamento.

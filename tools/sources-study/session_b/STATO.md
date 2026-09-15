# STATO — sessione B (Opus 5), ricostruzione una tantum di giugno 2026

Stato operativo della sessione B. Aggiornato a ogni passo rilevante; la conversazione non è
stato, questo file sì.

## 1. Verifica della chiave OpenAI (HANDOFF §2, §4.1)

| Controllo | Esito |
|---|---|
| Variabile `OPENAI_API_KEY` presente nell'ambiente | sì |
| Codice HTTP di `GET https://api.openai.com/v1/models` | 200 |
| Orario del controllo | 15 settembre 2026, 20:07 (Europe/Rome) — 18:07 UTC |

Il valore della chiave non è stato stampato, registrato, hashato né citato in alcuna forma,
qui o altrove. È stato usato solo come intestazione `Authorization` della richiesta di verifica,
il cui output è stato ridotto al solo codice HTTP.

Conseguenza: le chiamate a pagamento previste dal piano sono sbloccate, entro il tetto e con
la prova T1 di misura del prezzo effettivo prima di qualunque lotto di trascrizione
(HANDOFF §4.4). Nessuna chiamata a pagamento è ancora stata effettuata in questa sessione.

## 2. Budget

| Voce | Valore |
|---|---|
| Tetto complessivo | 78,86 € |
| Speso prima della sessione B | 0,86 € |
| Speso nella sessione B | 0,00 € |
| Disponibile | 78,00 € |

Nessun "extra usage", nessun abbonamento, nessun automatismo mensile: studio una tantum.

## 3. Quota Opus

Al massimo 2 subagenti Opus in parallelo oltre alla sessione principale. Lettura della pagina
Utilizzo da chiedere all'owner alla fine del primo giorno pieno (HANDOFF §2); letture della
sessione A in `quota_sessione_A.md`.

## 4. Avanzamento

| Passo (HANDOFF §4) | Stato |
|---|---|
| 0. Setup ambiente di lavoro | in corso |
| 1. Verifica chiave + primo commit di STATO.md | fatto |
| 2. Recuperi lenti (RomaTV, YouTube, Atti Web) | da avviare |
| 3. Report 1 — consegna 17 settembre ore 19:00 | da avviare |
| 4. Report 2 — consegna 20 settembre ore 19:00 | non iniziato |

## 5. Registro

- 15/09 20:07 — verifica chiave: presente, HTTP 200.
- 15/09 20:17 — controllo Codex C1 concluso, CHANGES_REQUESTED, 12 rilievi accettati, 0,16 €.
- 15/09 20:40 — canale di notifica push verificato non disponibile (§6).

## 6. Avvisi all'owner: canale push non disponibile (15 settembre, 20:30–20:40)

L'owner ha chiesto di ricevere una notifica sull'app Claude del cellulare quando serve
davvero una sua risposta. **Non è recapitabile da questa sessione**, e la causa è strutturale.

| Prova | Esito |
|---|---|
| Strumento di notifica diretto | "Mobile push requested", nessuna consegna |
| Routine `trig_01AumwmAXm4KtQxGuNYnh7kS` con `push` ed `email`, prima accensione (`cse_013YbniMrRaLLCbxszJbk9y4`, 20:33:15 → 20:33:34) | sessione conclusa con le etichette `routine_notify_push` e `routine_notify_email`, nessuna consegna |
| Stessa Routine, seconda accensione con contenuto che richiede una decisione (`cse_013b6EbYyZyhRfCWjEPT3n4g`, 20:35:12 → 20:35:29) | idem, nessuna consegna |

Causa: il recapito al telefono passa da Remote Control, che collega l'app a una sessione di
Claude Code in esecuzione sulla macchina dell'owner. Questa è una sessione cloud e non ha una
sessione locale a cui agganciarsi. Le notifiche dell'app dell'owner erano già attive: non era
una sua impostazione mancante. La seconda prova esclude anche l'ipotesi che il filtro
"degno di nota" stesse sopprimendo un avviso senza decisione dentro.

Conseguenze operative, fino a indicazione contraria dell'owner:

- Ogni richiesta all'owner vive **in chat e in questo file**, mai solo nella conversazione.
- Un blocco che richiede l'owner resta fermo finché non si riaffaccia. I recuperi lenti e il
  lavoro indipendente non si fermano: si ferma solo ciò che dipende dalla sua risposta.
- Per questo ogni richiesta porta con sé la **scelta di default** che applico da solo, come
  chiede il piano (§9.6): una richiesta senza default trasformerebbe l'assenza dell'owner in
  un'interruzione dello studio.
- La Routine resta creata ma inerte: non ha pianificazione e non parte da sola. Va cancellata
  o riusata solo se il canale diventasse disponibile.

Resta aperto per l'owner, senza urgenza: una Routine oraria di presidio creata da lui da
`claude.ai/code/routines` renderebbe robusto il presidio notturno (la creazione di Routine
ricorrenti da dentro la sessione è negata dal controllo permessi, "Unauthorized Persistence").
Non serve al recapito delle notifiche, serve a tenere viva la VM e a riavviare i recuperi.

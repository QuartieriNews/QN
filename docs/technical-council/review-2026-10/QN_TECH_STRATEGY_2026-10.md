# QN TECH STRATEGY — ottobre 2026

> **STATO: BOZZA DEL MEMBRO CLAUDE.** Diventa documento del Consiglio solo dopo la review indipendente di OpenAI/Codex (`COUNCIL_REVIEW_CODEX_2026-10.md`), il confronto (`COUNCIL_DEBATE_2026-10.md`) e le decisioni (`QN_COUNCIL_DECISIONS_2026-10.md`). Le sezioni marcate ⚑ sono quelle su cui Claude si aspetta disaccordo. Nulla qui è autorizzazione: Riccardo decide (DEC‑008, DEC‑012).

## CURRENT ARCHITECTURE — come funziona QN oggi (16 ott 2026)

- **Pipeline eventi:** Apify → n8n Cloud, workflow *Scrape FB Events Rome* (23 nodi, 1 code node) → Firestore/Drive `staging_`. Gazetteer Python (440 quartieri → 89 pagine) = contratto. Prompt geo ed editoriale in markdown, incollati in n8n. **Nessuna pagina pubblica. WordPress non esiste.**
- **AI loop:** Claude Code builder (abbonamento) → PR → Codex (app GitHub) review → Riccardo merge. Strategic Council via `council/cli.js` → `gpt‑5.6‑sol` (usato una volta). Lane gate advisor in CI. AUTO‑GREEN spento. Identità builder/owner condivise (DEC‑013).
- **Stato del lavoro:** ultimo merge su `main` 2 set; PR #15 (studio fonti, 249 commit) aperta; PR #14 (57 alert) aperta e mai revisionata. Sei decisioni di prodotto aperte (DEC‑001…006) bloccano l'attivazione.
- **Misura:** ~3.900 righe di governance e test; ~1.200 di pipeline.

## TARGET ARCHITECTURE — come dovrebbe funzionare

Gli stessi componenti, nessuno in più:

```
Apify / API / web ──► n8n Cloud (scheduling, HTTP, credenziali, scritture)
                        │  logica in code-nodes/*.js testati fuori da n8n
                        │  modelli via HTTP/Model node + JSON schema (Haiku default, frontier fallback)
                        ▼
                  Firestore (staging_ → prod) ──► WordPress (quando esiste)
GitHub = verità versionata · Drive = spec · decisions/ = decisioni
Claude Code ──MCP n8n (staging, per‑workflow)──► legge esecuzioni, modifica staging, esporta JSON in PR
Codex = review nativa su PR · Riccardo = merge + promozione + decisioni
```

Regole che lo tengono semplice: **n8n runner, non cervello** · **deterministico salvo classificazione/geo/enrichment** · **nessun nodo Agent in pipeline** · **prompt e schema nel repo, modello sostituibile**.

## NOW (≤5)
1. Chiudere PR #14 senza merge (DEC‑007), con questa review come residuo; cancellare duplicati e stub.
2. Adottare `docs/autonomy/SECURITY_BASELINE.md` (12 regole, sotto) e ridurre l'app Codex a read + PR review.
3. **P1** — n8n MCP in sola lettura sul workflow staging; Claude legge esecuzioni fallite e propone fix in PR.
4. **P2** — Classificazione/triage/geo‑zona su Haiku 5.5 in shadow mode su 100–200 record etichettati.
5. ⚑ **Governance freeze** fino alla prima pagina pubblica (da scrivere come DEC‑014 se Riccardo concorda).

## NEXT (≤5)
1. P1 stadio 2: write sul solo workflow staging + execute manual + export JSON automatico in PR.
2. **P3** — code‑node‑first: un nodo di logica (dedup/hash) in `code-nodes/` con test; poi gli altri.
3. Model strategy in produzione: Haiku default, frontier su bassa confidenza, coda umana (DEC‑103).
4. Chiudere DEC‑001/004, revisionare PR #15 (non tecnico, ma è il vero blocco).
5. Service account e chiavi con scadenza (R3).

## WATCH (monitorare, zero tempo ora)
Agents API e computer use · Claude Managed Agents dynamic workflows · browser/computer‑use SDK · n8n Agent queue / Builder / verification · WIF/OIDC · Decisions API oltre P2 · nuovi modelli builder/reviewer (arrivano con l'abbonamento) · AUP Anthropic 12 nov (Riccardo) · firma della cronologia agentica.

## DROP (fuori dal backlog)
I 36 alert "version floor" · 006 capacità · 027 · IP allowlist · benchmark builder/reviewer "su 5–10 task" · "agent boundary pack" come progetto · file duplicati e spuri.

## DO NOT BUILD
- Orchestrazione custom di agenti (queue, handoff, retry layer): n8n e i provider la danno già, e QN non ne ha bisogno.
- Un secondo reviewer "esecutivo" (worktree, browser, Guardian).
- Un harness Codex / Agents API attorno al reviewer.
- Nuovo tooling di governance (gate, collector, manifest, AUTO‑GREEN) prima di dati reali.
- Un benchmark continuo dei modelli.
- Browser/computer use in pipeline.

## AGENT AUTONOMY TARGET
- **Current safe level:** L4 sul codice (PR pronte, Riccardo merge) · L1 su n8n solo dopo P1.
- **Next target (90 gg):** L3 su staging n8n (testa e corregge da sola, bounded: cicli max, budget, nessuna credenziale prod).
- **Massimo medio termine (12 mesi):** L4 ovunque; L5 solo per categorie nominate su dati reali, con identità separata ripristinata (DEC‑013) e nuova DEC RED con consenso Claude + Codex. L6: no.

## SECURITY BASELINE (sintesi delle 12 regole; testo completo in `COUNCIL_REVIEW_CLAUDE_2026-10.md` §8)
1 staging ≠ prod, sempre · 2 minimo privilegio per ruolo · 3 service account con scadenza, niente credenziali personali · 4 rete allowlist · 5 idempotenza + fail‑closed · 6 la cronologia non autorizza · 7 modello pinnato/dichiarato · 8 ultima stable + boundary pack di 6 test prima di scrivere · 9 nessun plugin/Mod/skill non approvato · 10 config illeggibile = non parte · 11 browser read‑only, no computer use · 12 audit, budget, emergency stop (revoca client/token); Riccardo fa ogni merge e promozione.

## COST STRATEGY
- Costi fissi = abbonamenti già pagati (Claude, ChatGPT/Codex, n8n Cloud, Apify). Non aggiungerne.
- Costi variabili = API di pipeline: Haiku per i task chiusi, prefisso cacheable (istruzioni + lista zone), frontier solo in fallback. Budget mensile sul lato provider; `/usage` quando serve.
- Il costo più alto è il tempo di Riccardo: ogni ciclo di governance e ogni copia‑incolla di log lo consuma. P1 e il freeze sono le due misure con più ROI.

## MODEL STRATEGY
Coding: modello dell'abbonamento, dichiarato in `CLAUDE.md`. Architettura: idem + Council tier 2–3 (`gpt‑5.6‑sol` pinnato). Review: Codex app. Classificazione/triage/dedup: Haiku 5.5 (P2 confronta Luna/Decisions). Geo‑zona: Haiku → fallback frontier sotto soglia → coda umana. Enrichment: Sonnet 5.5. Browser/computer use: nessuno. Caching: prefisso stabile. Pinning: ID esatti dove chiamiamo noi l'API; cambio = riga in `prompts/CHANGELOG.md`.

## N8N STRATEGY ⚑
1. Resta il core engine? **Sì, come runner.** 2. Perché: owner non tecnico, managed, know‑how già investito, un solo workflow. 3. Alternative: codice custom su scheduler (seria, con trigger sotto), Make/Pipedream (no), agent platform (no). 4. Deve fare: trigger, HTTP, credenziali, scritture, retry, fallback model, MCP verso Claude. 5. Non deve fare: logica in Function/Set sparse, nodi Agent con tool, decisioni editoriali, promozione autonoma. 6. Funzioni agentiche native usate: fallback model; MCP server; verifica. 7. Non usate: Agent node, Agent queue, Agent Builder, Chat Hub. 8. Custom evitati: retry layer, handoff, queue, backup (export via MCP). 9. Dipendenza: media (tutto il know‑how). 10. Costo di sostituzione: 2–4 settimane di builder per un workflow; **trigger di riconsiderazione:** terzo workflow, o >50 % della logica in code nodes, o >1 h/settimana di Riccardo a incollare JSON.

## CLAUDE STRATEGY
Fa: builder, debugging, refactoring, architettura (Operator nel Council), sviluppo code nodes e workflow via MCP staging, generazione test, manutenzione, coordinamento ≤3 sub‑agent. Non fa: merge, promozione a prod, credenziali, modifica gazetteer generato, browser con credenziali reali, plugin/Mods, bypass permessi. Autonomia massima: L4 codice / L3 staging n8n. Serve approvazione: ogni PR (Riccardo), ogni scrittura fuori staging. Serve Codex: ogni PR. Serve Riccardo: tutto ciò che è in HUMAN ROLE.

## OPENAI/CODEX STRATEGY ⚑
Fa: review indipendente su PR (codice, sicurezza, classificazione di lane, difetti), seconda opinione tecnica nel Technical Council. Non fa: harness, browser verification, worktree execution, Guardian, strategia (quella è `gpt‑5.6‑sol`, DEC‑008). L'indipendenza vale il costo **solo finché il costo è un commento `@codex review`**. Permesso dell'app ridotto a read + review.

## HUMAN ROLE — Riccardo
- **AI CAN DO:** leggere repo/log/workflow staging; scrivere codice e test su branch; aprire PR; rispondere alle review; benchmark shadow; export JSON.
- **AI CAN DO + REPORT:** modifiche al workflow staging via MCP; esecuzioni manuali in staging; cicli bug→fix bounded; report di costo/usage.
- **AI CAN PREPARE:** bozze di DEC; proposte di modello/prompt (con changelog); proposte di promozione a prod; modifiche a baseline e lane list.
- **RICCARDO MUST DECIDE:** merge; promozione a produzione; credenziali e permessi; attivazione del pipeline pubblico; ogni DEC (prodotto, editoriale, governance, vendor); cambio di livello di autonomia; AUP/legale; budget; emergency stop.

## SAVING ESTIMATE (ri‑stima; dettagli in review §7)
- **MVP:** vs sviluppatore freelance ≈ **–50 %** già oggi; l'architettura proposta aggiunge ≈ –5 punti. Le vecchie stime (25–35 %) sottostimavano l'attuale.
- **Manutenzione annuale:** ≈ –45 % oggi → ≈ –65 % col proposto (confidence media).
- **Operativo/editoriale (tempo di Riccardo):** ≈ 0 oggi → ≈ **–45 %** col proposto (P1 + modelli economici + freeze). È il saving che decide se QN è sostenibile per un owner part‑time.

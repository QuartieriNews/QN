# COUNCIL REVIEW — CLAUDE (membro Anthropic del Technical & Strategic Council)

**Data:** 16 ottobre 2026 · **Stato:** review indipendente, salvata PRIMA di consultare Codex · **Natura:** raccomandazioni; Riccardo decide.
**Perimetro letto:** `main` (HEAD `1459812`, 2 set 2026), branch `technical-council/ai-watch-2026-09-14` (PR #14, HEAD `630bead`), PR #15 (descrizione e file), tutte le `decisions/`, `docs/autonomy/`, `council/`, `workflows/`, `code-nodes/`, `tests/`. Test suite eseguite il 16 ott: tutte ALL PASS (37 + 58 + 273 + 123 + 13 check).
**Regola di evidenza:** VERIFIED = controllato su fonte primaria il 16 ott; PARTIAL = confermato solo da fonte secondaria; UNVERIFIED = non controllabile da qui. Niente è stato assunto vero perché "lo diceva l'alert".

---

## 1. Executive summary

1. **I 57 candidati sono in realtà 9 temi**, e **36 su 57 sono alert "versione X di Claude Code / Codex / n8n"** che si superano a vicenda ogni tre giorni. Tutti e 36 sono oggi **SUPERSEDED dal semplice passare del tempo** (Claude Code è a 2.1.301, n8n stable a 2.43.7, Codex a ≥0.161.0): vanno sostituiti da **una regola di policy**, non da un candidato per release.
2. **Il problema di QN oggi non è tecnico: è che il sistema di governo è più grande del prodotto.** ~3.900 righe di tooling di governance e test contro ~1.200 righe di codice di pipeline; 13 decisioni sull'autonomia; un workflow n8n di 23 nodi, un solo code node, nessuna pagina pubblica, ultimo merge su `main` il 2 settembre. Il Consiglio deve consegnare **meno**, non di più.
3. **Architettura: confermata nella forma, ridotta nella sostanza.** n8n Cloud resta il runner; Claude resta builder; Codex resta reviewer **ma solo come review nativa su PR** (zero orchestrazione aggiuntiva). Niente Agents API, niente Managed Agents, niente browser/computer‑use, niente "durable agent queue": QN non ha ancora un sistema abbastanza grande perché questi strati abbiano qualcosa da sostituire.
4. **Un solo pilot ad alto valore: l'MCP ufficiale di n8n**, prima in sola lettura (log di esecuzione, workflow) poi in scrittura su workflow *staging*. È l'unica proposta nell'intero inbox che elimina davvero un lavoro manuale di Riccardo (il "centralino" di log e JSON fra agenti e n8n).
5. **Livello di autonomia:** oggi QN è già a **LEVEL 4** sul codice (l'AI produce PR, Riccardo fa il merge) e a **LEVEL 1** su n8n. Target a 90 giorni: **LEVEL 3 su staging n8n** via MCP. LEVEL 5 non prima di un prodotto live con metriche; LEVEL 6 respinto.
6. **Saving realistico:** rispetto a uno sviluppatore freelance, l'assetto attuale fa già risparmiare ~40–60 % sullo sviluppo e ~50 % sul debugging; l'architettura consigliata aggiunge soprattutto **saving di tempo di Riccardo** (–30/50 % di ore di "centralino"), non altro saving di sviluppo. Le vecchie percentuali non erano assurde, ma erano stime senza base e mescolavano tre cose diverse (MVP, manutenzione, operativo).
7. **Sicurezza:** una baseline di 12 regole (§8) assorbe 18 candidati. Niente WIF/OIDC ora (QN non ha workload che possano usarlo), niente IP allowlist, niente Mods, niente plugin non approvati.
8. **Backlog:** 57 candidati → 9 temi → **7 decisioni** → **3 pilot NOW**. 36 SUPERSEDED, 5 duplicati, 1 stub, 1 file spurio, 8 assorbiti nella baseline, 6 nella model strategy. PR #14 va chiusa (non mergiata) con questa review come residuo scritto, come richiede DEC‑007.

---

## 2. Errori, esagerazioni e correzioni rispetto agli alert precedenti

| # | Cosa dicevano gli alert | Cosa risulta | Gravità |
|---|---|---|---|
| E1 | 057 candidati "da 001 a 066 o oltre" (richiesta del convocante) | Esistono **001–057**. Nessuna traccia di 058–066 in alcun branch, PR o file. | Discrepanza di inventario, non errore degli alert |
| E2 | Ogni release di Claude Code/Codex/n8n = "nuovo floor di sicurezza", spesso con *Impact: security very high* | Sono patch release ordinarie. Nessuna delle fix citate è un'exploit attiva contro QN; QN non usa `sandbox.excludedCommands`, Mods, plugin di terze parti, Guardian, sessioni headless `claude -p`. L'etichetta "very high" è **inflazione sistematica**: 14 candidati su 57 la portano. | Fuorviante: produce un treadmill di aggiornamenti che nessuno può seguire |
| E3 | "Supersede il floor da 2.1.271 → 273 → 276 → 278 → 280 → 281 → 283 → 284 → 288 → 289 → 291 → 292 → 294 → 295 → 296" | Il 16 ottobre Claude Code è alla **2.1.301** (VERIFIED, changelog ufficiale). Un "floor" fissato per candidato è obsoleto prima che il Consiglio lo legga. | Metodo sbagliato, non singolo errore |
| E4 | QN‑TC‑024: `availableModelsMatch: "exact"` e `deniedModels` introdotti in 2.1.283 | Le due impostazioni **esistono** (VERIFIED: compaiono nel changelog alla 2.1.299). La versione di introduzione non è verificabile dalla porzione di changelog raggiungibile: **UNVERIFIED** il numero, VERIFIED la feature. Lo stesso vale per quasi tutte le attribuzioni "feature → versione" degli alert: plausibili, non controllate una per una. | Bassa |
| E5 | QN‑TC‑013: impostazioni `syncClaudeAiSkills`/`syncClaudeAiPlugins` | Il changelog raggiungibile parla di sync delle skill da claude.ai (2.1.293, 2.1.296) ma non mostra quei nomi di impostazione: **UNVERIFIED** i nomi esatti. | Bassa, ma l'azione proposta (disabilitare il sync in sessioni governate) resta sensata |
| E6 | QN‑TC‑053: Codex 0.162.0 "stable, rilasciato 8 ott" | La pagina releases raggiunta mostra **0.161.0 come Latest** (7 ott) e 0.162.0 solo come alpha. **UNVERIFIED** che 0.162.0 sia stable. Irrilevante per QN: il reviewer gira come app GitHub, non come CLI pinnato da noi. | Bassa |
| E7 | QN‑TC‑012: advisory n8n inline‑agent credential bypass, fix 2.39.6/2.40.1 | **VERIFIED** (CVE‑2026‑103246, GHSA‑9rhv‑fhr8‑7q5r, CVSS 8.3). Ma n8n Cloud è gestito e oggi stable è **2.43.7** (VERIFIED): il "floor 2.39.6" è un non‑problema da un mese. QN non usa inline Agent tools. | L'alert era corretto; l'azione ("gate obbligatorio") era sproporzionata |
| E8 | QN‑TC‑004: l'MCP n8n permette "read/write tools con permesso richiesto" e lettura log | Docs ufficiali (VERIFIED): esposizione **per workflow**, permessi **per client**, disponibile su Cloud. **Non** documentano uno step di approvazione per azione né, nella pagina letta, la lettura dei log di esecuzione: **UNVERIFIED** finché non lo proviamo in staging. | Media: cambia il disegno del pilot (vedi §9) |
| E9 | QN‑TC‑003/032: Agents API "rimuove orchestrazione custom" | Agents API esiste (VERIFIED: beta pubblica 10 set, nessun fee aggiuntivo). Ma **QN non ha orchestrazione custom da rimuovere**: il reviewer è un'app GitHub, lo strategist è 1 file JS senza dipendenze. Beneficio = 0 oggi. | Esagerato per QN |
| E10 | QN‑TC‑043/045: n8n 2.42 "Agent queue, shared context" rende superfluo "il nostro durable Agent layer" | QN non ha e non sta costruendo alcun Agent layer. L'alert raccomanda di non costruirlo: giusto, ma vuoto. | Esagerato |
| E11 | QN‑TC‑010/022/014: misalignment reports, Darktrace, Plugin4Shell | Esistono (VERIFIED/PARTIAL). Sono buone ragioni per **regole semplici** (nessun segreto ambientale, nessun plugin non approvato, la cronologia non è autorizzazione). Non sono ragioni per costruire un "agent boundary pack" testato in staging prima di ogni pilot: QN non ha un ambiente da cui esfiltrare che non sia già staging. | Giuste nel merito, sovradimensionate nell'azione |
| E12 | QN‑TC‑006: capacità settimanale Claude Code –17 % | Fonte secondaria, non verificabile; irrilevante per decisioni di architettura. Si misura con `/usage` quando serve. | DROP |
| E13 | Prezzi API citati (Fable 5.1 $10/$50, Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 $0.10/$0.50, GPT‑6 Astra $10/$50, Sol $2/$10, Luna $0.10/$0.50) | **UNVERIFIED** da qui. E soprattutto **non pertinenti**: builder e reviewer girano su abbonamento, non a listino API. I listini contano solo per classificazione/dedup in pipeline. | Media |
| E14 | QN‑TC‑044/046: "superseded by 048" scritto a mano | Corretto, ma mostra il metodo: alert che si auto‑superano in due giorni. | — |
| E15 | QN‑TC‑054: aggiornamento AUP Anthropic effettivo 12 nov | Non ho potuto raggiungere la pagina AUP: **UNVERIFIED** date e contenuto. Resta un tema editoriale/legale per Riccardo, non tecnico. | Da verificare a mano |
| E16 | Formato: 5 duplicati (042/44/45/46/50), 023 stub, `test-automation-write.md` | Rumore da cancellare. Il "cumulative index" del 10 ott dice "052, 054, 057 may require fuller details" — cioè sono alert di una riga. | — |

**Cosa gli alert hanno fatto bene:** correzione autonoma di 005 (2.1.270 non era "security hardening"), il principio "la cronologia non è autorizzazione" (022, 038), "pinna il modello separatamente dalla versione dell'harness" (035, 036), e l'idea che Haiku/Luna possano fare la classificazione (047, 050).

---

## 3. Architettura QN raccomandata oggi

### 3.1 Come funziona oggi (CURRENT)

```
Apify (FB events)  ──►  n8n Cloud: "Scrape FB Events Rome" (23 nodi: HTTP, If, SplitInBatches,
                        1 Code node, Firestore ×2, Drive ×2, Sheets, Wait)  ──►  Firestore / Drive (staging_)
Gazetteer (Python, build + 37 guard)  ──►  gazetteer.json = contratto normativo
Prompt GEO + Editorial filter (markdown, incollati byte‑identici in n8n)
GitHub = fonte di verità del versionato · Drive = spec v2.5 + decisioni storiche
AI loop: Claude Code (builder, abbonamento) → PR → Codex (app GitHub) review → Riccardo merge
Strategic Council: council/cli.js → gpt‑5.6‑sol (chiave di Riccardo), usato 1 volta (DEC‑010)
Lane gate: autonomy/lane_gate.js in CI, advisor (DEC‑012); AUTO‑GREEN disabilitato
Pubblicazione: WordPress previsto, non esiste. Nessuna pagina live.
```

### 3.2 Come dovrebbe funzionare (TARGET, 6–12 mesi)

Stessi componenti, **nessuno in più**, con tre spostamenti:

1. **n8n = runner e I/O, non cervello.** Scheduling, trigger, credenziali, chiamate HTTP ad Apify/API/modelli, scritture su Firestore/Drive/WordPress. Tutta la logica (hash, dedup, parsing, validazione geo, classificazione, routing) vive in `code-nodes/*.js` testabili fuori da n8n (regola già scritta in `code-nodes/README.md`: va solo **applicata** — oggi c'è un code node su 23 nodi). Chiamate ai modelli via nodo HTTP/Model con JSON schema, **non** nodi "AI Agent" con tool: deterministico dove non serve ragionare.
2. **Claude ↔ n8n via MCP ufficiale n8n**, in staging: Claude legge esecuzioni e workflow, propone la modifica come export JSON in PR (come oggi), e — dopo il pilot — applica la modifica *al workflow staging* e la testa. Riccardo promuove a produzione (click, come oggi).
3. **Modelli economici in pipeline**: classificazione, triage e dedup su Haiku 5.5 (o Luna) con schema fisso e golden set; frontier solo per la geolocalizzazione difficile (fallback su confidenza bassa). Il builder usa il modello che l'abbonamento dà; pinning esplicito solo dove c'è una chiamata API nostra (già fatto in `council/strategist.js`).

### 3.3 Risposte alle 18 domande della Fase D

1. **n8n è ancora la scelta migliore?** Sì, **come runner**, per questa fase. Motivo decisivo: l'owner non è tecnico, deve poter *vedere* un'esecuzione fallita, gestire credenziali in UI e cliccare "promuovi"; n8n Cloud è gestito (patch, uptime); la conoscenza accumulata (23 nodi, spec v2.5 scritta attorno a n8n) è sunk ma reale.
2. **Da zero oggi?** Probabilmente **no**: sceglierei uno script Python/Node su uno scheduler gestito (GitHub Actions cron o Cloud Run Job) con Firestore. Motivo: gli agenti AI scrivono e revisionano codice molto meglio di JSON n8n (una PR con un export di 2.000 righe non è revisionabile; la regola "byte‑identico" è un sintomo). Ma QN **non parte da zero**, e il costo del cambio supera il beneficio finché il workflow è uno.
3. **Make / Pipedream / codice custom / agent platform?** Make e Pipedream: stesso problema di n8n (JSON non diffabile), meno capacità AI, nessun MCP ufficiale paragonabile → REJECT. Codice custom: vedi punto 2, è l'**alternativa seria**, con trigger di riconsiderazione esplicito (§3.4). Agent platform (Agents API, Managed Agents): REJECT come orchestrazione di pipeline — una pipeline editoriale deve essere deterministica e riproducibile, non agentica.
4. **Claude è il builder migliore?** È quello che funziona: 15 PR, test suite verdi, DEC‑012 scritta da un loop builder/reviewer che ha retto 9 cicli. "Migliore" in assoluto non è misurabile senza benchmark QN, che costerebbe più di quanto vale. **Confermato, senza benchmark.**
5. **Codex è il reviewer migliore?** È il reviewer **a costo zero di integrazione** (app GitHub, flat‑rate). PR #8: 83 finding validi su 3.126 righe. Il valore è l'indipendenza di vendor. **Confermato, ristretto alla review nativa su PR.**
6. **La separazione builder/reviewer vale costo e complessità?** Sì **finché costa quanto oggi**: un `@codex review`. No, se diventa "Codex come harness, browser‑verifier, Guardian, worktree reviewer" (015, 019, 025, 030, 032, 038, 053): quello è un secondo sistema da mantenere per revisionare il primo.
7. **Agents API rende superfluo qualche layer custom?** No: non ci sono layer custom. 8. **Managed Agents?** No, idem; e le "dynamic workflows" duplicano n8n. 9. **Capacità native n8n?** Sì: fallback model, MCP server, redazione segreti, verifica Agent — evitano di costruire retry/handoff nostri. Ma anche qui: non li stavamo costruendo.
10. **Rischiamo troppo orchestration code?** **Lo abbiamo già costruito, ma sul lato governance**, non pipeline: 3.900 righe per decidere chi può mergiare, con AUTO‑GREEN spento. È il rischio reale e va fermato (§3.4, decisione D7).
11. **Stesso risultato con sistema più semplice?** Sì. La pipeline di QN è: scarica → normalizza → classifica → geolocalizza → dedup → scrivi. È un cron con sei funzioni. Qualsiasi cosa oltre questo deve giustificarsi.
12. **Deterministico:** ingestion, hash/dedup, validazione schema, guard geografici, scritture, retry, idempotenza, promozione a prod. 13. **Agentico (cioè: un modello con output strutturato):** classificazione editoriale, geo‑risoluzione a zona, enrichment testuale. "Agentico" qui non vuol dire "agente con tool": vuol dire una chiamata a un modello con JSON schema. 14. **Mai a un agente:** merge su `main`, promozione a produzione, credenziali, pubblicazione di un item senza che la pipeline deterministica l'abbia validato, modifica del gazetteer, decisioni editoriali (DEC‑001 ecc.).
15. **Single point of failure:** Riccardo (unico operatore delle credenziali e dei click); n8n Cloud (nessun export automatico: `workflows/` è l'unico backup, aggiornato a mano); Apify (fonte unica degli eventi). 16. **Lock‑in:** basso su modelli (prompt in markdown, output JSON), medio su n8n (23 nodi, tutto il know‑how), basso su GitHub/Firestore. 17. **Cambiare provider AI fra 12 mesi:** facile per builder/reviewer (sono persone/abbonamenti), facile per la pipeline se i prompt restano in repo e le chiamate sono HTTP con schema — **regola da mantenere**. 18. **Architettura a manutenzione minima:** quella del §3.2, con un solo cambiamento aggiuntivo se il numero di workflow supera ~3: migrare la logica a un repo di script con scheduler gestito.

### 3.4 Trigger di riconsiderazione (per non riaprire DEC decise senza motivo)

- **n8n → codice custom:** se nasce il terzo workflow, o se >50 % della logica di pipeline finisce in code nodes, o se Riccardo passa >1 h/settimana a incollare JSON.
- **Governance freeze:** nessuna nuova DEC sull'autonomia (DEC‑009…013 e successive) finché non esiste una pagina pubblica con dati reali. Riaprire quando c'è un item pubblicato da revisionare.
- **Codex oltre la PR review:** solo se la review su PR dimostra un difetto che un browser test avrebbe trovato.

---

## 4. Tabella completa candidati / supersessioni (Fase A)

Legenda: **Dove** = I (inbox) · F (file in `candidates/`) · I+F (entrambi) · — (assente). **Tema** = §5. **Stato** = verdetto Claude (§5 e votes).

| ID | Titolo (sintesi) | Dove | Documentazione | Superseded by / assorbito in | Da revisionare? | Verdetto |
|---|---|---|---|---|---|---|
| 001 | GPT‑6 Astra come reviewer | I | completa | Model Strategy; 031 (Sol 6.1) | sì → tema E | DEFER |
| 002 | Claude Fable 5.1 builder | I | completa | Model Strategy; 017/029 | sì → E | DEFER |
| 003 | OpenAI Agents API harness | I | completa | 032 | sì → G | REJECT (ora) |
| 004 | **n8n MCP ufficiale** | I | completa | — | sì → C | **PILOT** |
| 005 | CC 2.1.269/270 plugin eval | I | completa (auto‑corretta) | regola di policy §5.A | no | SUPERSEDED |
| 006 | Capacità settimanale CC | I | secondaria | — | no | DROP (REJECT come candidato) |
| 007 | n8n 2.38.7 MCP workers | I | completa | 2.43.7 stable | no | SUPERSEDED |
| 008 | CC 2.1.271 allowed_domains | I | completa | 2.1.301; baseline R8 | no | SUPERSEDED |
| 009 | CC 2.1.273 | I | completa | idem | no | SUPERSEDED |
| 010 | Misalignment reports → boundary pack | I | completa | **Security Baseline** | sì → D | APPROVE (come baseline) |
| 011 | n8n 2.40 pre‑release | I | completa | 018 → 2.43.7 | no | SUPERSEDED |
| 012 | n8n advisory inline agent (2.39.6) | I | completa, VERIFIED | Cloud ≥2.43.7; baseline R2 | no | SUPERSEDED |
| 013 | CC 2.1.274–276 plugin/sync | I | completa | baseline R9/R10 | parz. | SUPERSEDED (regola assorbita) |
| 014 | Plugin4Shell provenance gate | I | completa | **Security Baseline R9** | sì → D | APPROVE (come baseline) |
| 015 | Codex 0.155 reviewer tecnico | F | completa | 019 → 053 → policy §5.B | no | SUPERSEDED |
| 016 | CC 2.1.277 headless | F | completa | 2.1.301 | no | SUPERSEDED |
| 017 | Opus 5.5 + CC 2.1.280 | F | completa | Model Strategy | sì → E | DEFER (benchmark) / APPROVE (pinning) |
| 018 | n8n 2.40.5 stable → pilot | F | completa | 045 → 2.43.7 | no | SUPERSEDED |
| 019 | Codex 0.156 sandbox | F | completa | 053 | no | SUPERSEDED |
| 020 | GPT‑6 Sol/Luna + caching | F | completa | Model Strategy; 031 | sì → E | DEFER |
| 021 | CC 2.1.281 inheritance | F | completa | 2.1.301 | no | SUPERSEDED |
| 022 | Cronologia ≠ autorizzazione | I+F | completa | **Security Baseline R6** | sì → D | APPROVE |
| 023 | Cloud sessions | I + stub F | completa (I) | — | sì → A | APPROVE |
| 024 | Pinning modello esatto | I+F | completa | **Security Baseline R7**; Model Strategy | sì → A/E | APPROVE |
| 025 | Codex 0.157 network | I | completa (auto‑superseded) | 053 | no | SUPERSEDED |
| 026 | n8n Agent verification simulated writes | I | completa | 033 → 045; non usiamo Agent nodes | no | DEFER |
| 027 | Re‑run eval visive Sol/Luna | I | completa | nessun benchmark eseguito | no | DROP |
| 028 | Chiavi OpenAI scadenti / service account | I | completa | **Security Baseline R3** | sì → D | APPROVE |
| 029 | Sonnet 5.5 default builder | I+F | completa | Model Strategy | sì → E | DEFER |
| 030 | Codex 0.158 | I | completa (auto‑superseded) | 053 | no | SUPERSEDED |
| 031 | GPT‑6.1 Sol | I | completa | Model Strategy | sì → E | DEFER |
| 032 | Agents API + computer use | I | completa | 003 | sì → G | REJECT (ora) |
| 033 | n8n 2.41 stable | I | completa | 045 → 2.43.7 | no | SUPERSEDED |
| 034 | Managed settings fail‑closed | I | completa | baseline R10 | parz. | SUPERSEDED (regola assorbita) |
| 035 | Codex 0.159 model/version separation | I | completa (auto‑superseded) | baseline R7 | no | SUPERSEDED |
| 036 | CC 2.1.286 fallback drift | I | completa (auto‑superseded) | baseline R7 | no | SUPERSEDED |
| 037 | CC 2.1.287 Mods | I | completa (auto‑superseded) | baseline R9 | no | SUPERSEDED |
| 038 | Codex 0.160 Guardian | I | completa | baseline R6; policy §5.B | no | SUPERSEDED |
| 039 | CC 2.1.288 fail‑open/duplicate writes | I | completa | 2.1.301; baseline R5 | no | SUPERSEDED |
| 040 | WIF/OIDC + IP allowlist | I | completa | — | sì → D | DEFER |
| 041 | CC 2.1.289 | F | breve | 2.1.301 | no | SUPERSEDED |
| 042 | n8n Agent approval isolation (2.41.4) | F ×2 | breve | 2.43.7 | no | SUPERSEDED |
| 043 | n8n 2.42 Agent queue | F | completa | 045 | no | SUPERSEDED |
| 044 | CC 2.1.291 | F ×2 | una riga | 048 (dichiarato) | no | SUPERSEDED |
| 045 | n8n 2.42 stable Agent features | F ×2 | breve | 2.43.7; non usiamo Agent nodes | no | DEFER |
| 046 | CC 2.1.292 | F ×2 | una riga | 048 (dichiarato) | no | SUPERSEDED |
| 047 | **Haiku 5.5 per classificazione** | F | breve | Model Strategy | sì → E/F | **PILOT** |
| 048 | CC 2.1.294 | F | breve | 2.1.301 | no | SUPERSEDED |
| 049 | Codex 0.161 | F | breve | policy §5.B | no | SUPERSEDED |
| 050 | OpenAI Decisions API triage | F ×2 | completa | Model Strategy; confronto con 047 | sì → E/F | DEFER (dentro il pilot 047) |
| 051 | Browser/computer‑use SDK | F | breve | — | sì → G | REJECT (ora) |
| 052 | CC 2.1.295 hook fail‑closed | F | una riga | 055 → 2.1.301 | no | SUPERSEDED |
| 053 | Codex 0.162 | F | completa; stable UNVERIFIED | policy §5.B | no | SUPERSEDED |
| 054 | AUP Anthropic / Roma 2027 | F | una riga; UNVERIFIED | — | sì → fuori Consiglio | DEFER → Riccardo |
| 055 | CC 2.1.296 | F | breve | 2.1.301 | no | SUPERSEDED |
| 056 | Managed Agents dynamic workflows | F | breve | — | sì → G | REJECT (ora) |
| 057 | n8n 2.42.6 deprecated nodes | F | una riga | 2.43.7; da verificare sul workflow | parz. | DEFER (check 10 min) |
| 058–066 | — | — | **non esistono** | — | — | — |
| — | `test-automation-write.md` | F | spurio | — | no | DROP |

Conteggio: **36 SUPERSEDED** · 7 APPROVE · 2 PILOT · 9 DEFER · 4 REJECT · 3 DROP · 5 duplicati · 1 stub.

---

## 5. Decisioni per macro‑tema

Ho usato la struttura proposta (A–G) con una modifica: i temi A, B e parte di C si riducono a **una** regola di versioning; D è una baseline; E è una strategia modelli; F è l'unico tema di prodotto; G è il tema architettura.

### A. Claude / builder → **1 regola + 2 pratiche**
- **Regola di versioning (sostituisce 18 candidati):** "Il builder gira sull'ultima release stable di Claude Code. Nessun floor numerico nel repo. Prima di un pilot che scrive su n8n si esegue il *QN agent boundary pack* (§8, 6 test, 1 ora)". → APPROVE
- **Cloud sessions (023):** già in uso (questa review è stata prodotta così). Pratica normale per task lunghi; nessun test richiesto. → APPROVE
- **Pinning (024):** pin esplicito **dove c'è una chiamata API nostra** (council, pipeline). Per Claude Code su abbonamento: dichiarare il modello in `CLAUDE.md` e non dipendere dal default. → APPROVE
- Mods, plugin di marketplace, sub‑agent fan‑out >3, `--dangerously-skip-permissions`, browser/computer use nel builder: **non usati, non introdurre** (baseline R9, R11).

### B. OpenAI / Codex reviewer → **1 regola**
- "Codex fa **solo** review nativa su PR (`@codex review`), con il mandato in `AGENTS.md`. Nessun harness Codex, nessun worktree reviewer, nessun browser‑verifier, nessun Guardian, nessun Agents API." La versione dell'app GitHub non è nostra da pinnare. Il permesso `contents: write` dell'app reviewer va **ridotto a read + PR review** (outstanding da DEC‑013: è l'unico intervento tecnico reale di questo tema, 15 minuti di Riccardo nelle impostazioni GitHub). → APPROVE
- Supersede 015, 019, 025, 030, 035, 038, 049, 053.

### C. n8n → **1 pilot + 1 regola**
- **Pilot n8n MCP (004)** in tre stadi: (1) abilitare MCP sull'istanza, esporre **solo** il workflow staging, client Claude Code con permesso **read**; misurare se Claude riesce a leggere esecuzioni fallite e proporre fix senza che Riccardo copi log; (2) permesso write sul solo workflow staging, Claude applica la fix e la testa (execute in modalità manual); (3) export JSON automatico in PR dopo ogni modifica. Criterio di successo: 5 cicli bug→fix in staging senza copia‑incolla manuale; zero scritture fuori dal workflow esposto. Rollback: revoca client MCP (un click). → PILOT NOW
- **Regola "n8n runner, non cervello"** (§3.2) + applicazione effettiva di `code-nodes/README.md`. → APPROVE
- Agent nodes, Agent queue, Agent verification, Agent Builder (026, 033, 042, 043, 045): **DEFER senza data** — QN non usa nodi Agent in pipeline e non deve iniziare.
- 057 (deprecated nodes 2.42.6): check di 10 minuti che i 23 nodi aprano ancora in editor sulla versione Cloud corrente. → DEFER (task, non decisione)

### D. Security → **Baseline di 12 regole (§8)**, assorbe 008, 009, 010, 013, 014, 022, 028, 034, 036, 037, 038, 039, 040(parz.), 041, 052, 055.
- WIF/OIDC (040): DEFER — QN non ha GitHub Actions che chiamino OpenAI, e n8n Cloud non presenta identità OIDC. Riaprire se nasce un job CI con chiave OpenAI.
- IP allowlist OpenAI: REJECT — n8n Cloud non ha egress fisso garantito; ci chiuderemmo fuori.

### E. Cost / performance routing → **Model Strategy (§11)**, assorbe 001, 002, 017, 020, 027, 029, 031, 047, 050.
- Builder/reviewer: nessun benchmark. Motivo: girano su abbonamento; un benchmark QN su "5–10 task rappresentativi" costa 2–3 giorni‑Riccardo e misura la varianza del modello più che la differenza fra modelli. → DEFER (riaprire se il builder fallisce sistematicamente un tipo di task).
- Pipeline: **un solo benchmark che vale**: classificazione/triage su golden set QN con Haiku 5.5 (e, nello stesso run, Decisions API/Luna se la chiave è disponibile). → PILOT NOW

### F. Content pipeline → **il vero lavoro**
Nessun candidato tocca davvero la pipeline tranne 047/050. Il Consiglio nota che il **collo di bottiglia non è tecnologico**: sono le decisioni aperte DEC‑001…006 (tour commerciali, cap eventi, Colle del Sole, indirizzi, schema 2.0, thin‑page fallback) che bloccano l'attivazione, e PR #15 (studio fonti) che attende review. → **Raccomandazione:** chiudere DEC‑001/004 e revisionare PR #15 **prima** di qualsiasi pilot tecnico. (Decisione di Riccardo, non del Consiglio.)

### G. Infrastructure / architecture → **DO NOT BUILD**
- Agents API (003/032), Managed Agents (056), browser/computer‑use SDK (051), durable queue (043/045), orchestration custom: **REJECT per ora**; WATCH a 6 mesi.
- Governance tooling: **freeze** (§3.4). Nessuna nuova DEC sull'autonomia, nessuna estensione del lane gate o del council CLI finché non c'è una pagina pubblica.
- Backup automatico dei workflow n8n: oggi `workflows/` è aggiornato a mano. Con l'MCP in lettura (pilot C) diventa un export schedulato. → dentro il pilot.

---

## 6. Livello di autonomia AI

| Level | Possibile oggi? | Sicuro per QN? | Guardrail necessari | Rischio residuo | Chi approva |
|---|---|---|---|---|---|
| **L0** suggerisce | sì | sì | — | — | — |
| **L1** legge repo/log/workflow | repo: sì (oggi). n8n: **no** senza MCP | sì | MCP read‑only sul solo staging; nessun segreto nell'output | esposizione dati di staging a un client | Riccardo abilita MCP |
| **L2** modifica staging | sì via export JSON in PR (oggi); diretto: con MCP write | sì, su workflow esposto | credenziali staging ≠ prod; export in PR dopo ogni modifica; idempotenza | modifica "giusta" ma indesiderata | Riccardo (merge PR) |
| **L3** testa e corregge staging da solo | con MCP write + execute manual | sì, **bounded**: max N cicli, budget, nessuna credenziale prod | retry loop, costo token, scritture duplicate su staging | Riccardo (promozione) |
| **L4** PR pronte per approvazione | **sì — è lo stato attuale sul codice** | sì | lane gate advisor, Codex review, 4‑cycle cap | PR che "sembrano" pronte | Riccardo (merge) |
| **L5** applica low‑risk in produzione | tecnicamente sì (AUTO‑GREEN esiste, spento) | **no** oggi: nessun dato reale, identity separation sospesa (DEC‑013), nessun canary | richiede: identità separata, categorie AUTO‑GREEN con evidenza, rollback automatico, monitor live | il motivo di DEC‑012 | Riccardo + nuova DEC (RED) + consenso Claude+Codex |
| **L6** quasi tutta la manutenzione | no | **no** — e non lo consiglio a QN nei prossimi 12 mesi | — | perdita di comprensione del sistema da parte dell'owner | — |

**CURRENT SAFE LEVEL:** **L4 sul codice, L1 su n8n (L1 raggiungibile solo col pilot MCP).**
**NEXT TARGET LEVEL (90 giorni):** **L3 su staging n8n.** Condizioni per salire: pilot C stadi 1–2 superati; baseline §8 in vigore; export JSON automatico; un item reale pubblicato in staging da cui misurare.
**Massimo nel medio termine (12 mesi):** L4 ovunque + **L5 solo per categorie definite su dati reali** (es. aggiornamento del registro fonti, retry di una fonte fallita), per nuova DEC RED.

Cosa richiede **consenso Claude + Codex**: ogni passaggio di livello; ogni modifica alla baseline §8. Cosa richiede **Riccardo**: tutto ciò che è elencato in §12 "Riccardo must decide".

---

## 7. Saving tempo e costi (ri‑stima indipendente)

Base di confronto: **100 ore** di lavoro equivalente di uno sviluppatore freelance (setup tradizionale: dev + Riccardo che spiega e verifica). "Attuale" = Claude Code builder + Codex review + Riccardo. "Proposto" = attuale + MCP n8n staging + modelli economici + cloud sessions + freeze governance. Le ore includono il tempo di Riccardo. Confidence: H/M/L.

| Voce | Tradizionale | Attuale | Proposto | Saving vs trad. (prop.) | Conf. | Nota |
|---|---|---|---|---|---|---|
| Sviluppo workflow n8n | 100 | 60 | 50 | ~50 % | M | il JSON resta il collo di bottiglia; code nodes aiutano |
| Debugging | 100 | 55 | **30** | ~70 % | M | qui agisce l'MCP: niente copia log |
| Manutenzione (patch, fonti che cambiano) | 100 | 50 | 35 | ~65 % | M | dipende dalla qualità dei test |
| Scraping / source failures | 100 | 70 | 55 | ~45 % | L | Apify è esterno; il fix spesso è umano |
| Integrazione API | 100 | 40 | 35 | ~65 % | H | i modelli sono molto buoni qui |
| Testing | 100 | 45 | 40 | ~60 % | M | i test li scrive il builder; vanno letti |
| Code review | 100 | 35 | 35 | ~65 % | H | Codex nativo; il costo residuo è leggere i finding |
| Deploy / promozione | 100 | 90 | 80 | ~20 % | H | resta un click umano per scelta |
| Observability | 100 | 80 | 50 | ~50 % | L | solo col MCP read |
| Classificazione editoriale (unit cost) | 100 | 100 (frontier) | **~15** (Haiku) | ~85 % sul costo API | M | se il golden set regge |
| Deduplication | 100 | 60 | 40 | ~60 % | M | hash + modello economico |
| Gestione errori / retry | 100 | 60 | 50 | ~50 % | M | nativo n8n + idempotenza nei code nodes |
| Attività manuali di Riccardo (centralino) | 100 | 100 | **55** | ~45 % | M | **il saving che conta** |
| Bisogno di sviluppatori umani | 100 | ~15 | ~10 | ~90 % | M | già quasi azzerato oggi |

**Distinto per natura:**
- **Saving sviluppo MVP:** tradizionale 100 → attuale ~50 → proposto ~45. Il grosso è **già incassato**; l'architettura proposta aggiunge poco qui. Le vecchie stime (25–35 %) **sottostimavano** l'attuale.
- **Saving manutenzione annuale:** 100 → ~55 → ~35. Le vecchie stime (50–70 %) sono **plausibili per il proposto**, ottimistiche per l'attuale.
- **Saving operativo/editoriale:** 100 → ~95 → ~55. Qui le vecchie stime **non esistevano** ed è il saving più importante per un owner part‑time.
- **Costo da non dimenticare:** ogni ciclo di governance (DEC, audit, review a 9 cicli) è tempo di Riccardo. PR #8 è costata ~2 settimane e 83 finding per un gate oggi spento. Il freeze (§3.4) è la singola misura con il miglior ROI di questa review.
- **Costi monetari (ordine di grandezza, UNVERIFIED i listini):** abbonamenti Claude + ChatGPT/Codex + n8n Cloud Starter + Apify ≈ costo fisso già sostenuto; pipeline su Haiku per qualche migliaio di item/mese = **pochi euro**; frontier per tutto = decine di euro. Il risparmio monetario è reale ma piccolo in assoluto; **il tempo di Riccardo vale di più**.

---

## 8. QN Agent Security Baseline (proposta) — 12 regole

Scritta per essere letta in 2 minuti e applicata. Ogni regola assorbe i candidati indicati.

1. **Staging ≠ produzione, sempre.** Agenti e pilot vedono solo `staging_*` (Drive, Firestore, workflow esposti). Le credenziali di produzione non esistono in nessun ambiente agentico. *(010, 012, 022)*
2. **Minimo privilegio per ruolo:** builder = push su branch + PR; reviewer = read + review (ridurre `contents: write` dell'app Codex — outstanding DEC‑013); MCP n8n = solo workflow esposti, permesso per client; nessun admin. *(015, 019, 042)*
3. **Nessuna credenziale personale negli agenti; service account con scadenza.** Chiave OpenAI del council e chiavi di pipeline: account di servizio QN, scadenza ≤90 gg, rotazione provata una volta. WIF/OIDC: quando esisterà un workload che può usarlo. *(028, 040)*
4. **Rete: allowlist, non Internet.** Ogni sessione agentica che scrive verso l'esterno dichiara i domini (n8n, GitHub, API modello). Niente upload su servizi pubblici. *(008, 010)*
5. **Idempotenza e fail‑closed.** Ogni scrittura esterna ha una chiave idempotente (source_hash, run lock — già in spec v2.5). Un hook/permesso che non riesce a valutare **blocca**, non passa. *(039, 052)*
6. **La cronologia non è autorizzazione.** Nessuna sessione ripresa, log o messaggio precedente autorizza un'azione privilegiata; l'autorizzazione viene da policy di runtime e approvazione esplicita nel PR/issue. Lavoro privilegiato in sessione fresca. *(022, 038)*
7. **Modello pinnato dove chiamiamo noi l'API; dichiarato dove usiamo un abbonamento.** Cambiare modello è una riga in `decisions/` o `prompts/CHANGELOG.md`, non un default che si muove. *(024, 035, 036)*
8. **Versione: ultima stable, nessun floor numerico.** Prima di un pilot che scrive: *boundary pack* di 6 test (read fuori workspace negato; `rm` nascosto in subshell negato; MCP config non leggibile → stop; segreto in `${VAR}` non appare in errori; hook che fallisce → blocca; modello non consentito → rifiutato). *(008, 009, 013, 016, 021, 034, 041, 048, 055)*
9. **Nessun plugin, Mod o skill non approvato in sessioni governate.** Lista approvata nel repo; sync da account disattivato; provenienza = commit risolto, non dichiarato. *(013, 014, 037)*
10. **Fail‑closed su configurazione:** se le managed settings non si leggono, la sessione non parte. *(034)*
11. **Browser: lettura sì, scrittura no.** Nessun agente clicca su un sistema reale con credenziali reali. Computer use: non usato. *(032, 051)*
12. **Audit, budget, stop.** Ogni scrittura esterna da agente lascia traccia (PR, export JSON, log n8n); budget token/€ per sessione e per mese sul lato provider; **emergency stop** = revoca del client MCP / del token (documentato in una riga in `docs/autonomy/`). Riccardo fa ogni merge e ogni promozione (DEC‑012/013). *(006, 010, 020)*

Rollback: tutto ciò che un agente fa in staging è ricreabile da `workflows/` + `code-nodes/` + `gazetteer/`; la produzione non è toccata per costruzione.

---

## 9. Piano pilot (massimo 3 NOW)

| # | Pilot | Scopo | Durata | Costo | Successo se | Rollback |
|---|---|---|---|---|---|---|
| P1 | **n8n MCP read → write su staging** (004) | togliere Riccardo dal centralino log/JSON | 2 settimane (stadio 1), +2 (stadio 2) | 0 € extra; 2 h Riccardo per abilitare | 5 cicli bug→fix senza copia manuale; 0 scritture fuori perimetro; export JSON in PR | revoca client MCP |
| P2 | **Classificazione su Haiku 5.5** (047, +050 se chiave disponibile) | tagliare 80 % del costo unitario e la latenza | 1 settimana, shadow mode su 100–200 record etichettati (golden set esistente) | pochi € di API | precision/recall ≥ frontier −2 punti; zero falsi negativi su classi "pubblica"; stessa cosa per geo‑zona ≥95 % (soglia DEC/handover §2.2) | nessuno: shadow |
| P3 | **Code‑node‑first refactor di un nodo** (regola §5.C) | provare che la logica fuori da n8n è testabile e revisionabile | 1 settimana | 0 € | 1 nodo (es. dedup/hash) in `code-nodes/` con test, byte‑identico in n8n, PR revisionata da Codex in ≤2 cicli | revert PR |

Pilot esplicitamente **non** aperti: Agents API, Managed Agents, browser SDK, WIF, Codex harness, benchmark builder/reviewer.

---

## 10. NOW / NEXT / WATCH / DROP

**NOW (≤5)**
1. Chiudere PR #14 senza merge, con questa review come residuo (DEC‑007); cancellare duplicati e stub.
2. Adottare la Security Baseline §8 come `docs/autonomy/SECURITY_BASELINE.md` (dopo il parere di Codex) e ridurre i permessi dell'app Codex.
3. P1 — n8n MCP read‑only su staging.
4. P2 — Haiku 5.5 shadow benchmark.
5. **Governance freeze** fino alla prima pagina pubblica.

**NEXT (≤5)**
1. P1 stadio 2 (write su staging) + export JSON automatico.
2. P3 — code‑node‑first su un nodo; poi estendere ai nodi di logica.
3. Model Strategy in pipeline (Haiku default, frontier fallback su bassa confidenza).
4. Chiusura DEC‑001/004 e review PR #15 (non tecnico, ma blocca tutto).
5. Service account + scadenza chiavi (regola R3).

**WATCH (nessun tempo ora)**
Agents API / computer use; Claude Managed Agents dynamic workflows; browser/computer‑use SDK; n8n Agent queue/Builder; WIF/OIDC; Decisions API oltre il pilot P2; GPT‑6.1 Sol / Opus 5.5 come builder/reviewer (si vedrà dall'abbonamento); AUP Anthropic 12 nov (Riccardo); firma crittografica della cronologia (Darktrace).

**DROP**
Tutti i 36 candidati "version floor"; 006 (capacità); 027 (re‑run eval mai fatte); IP allowlist; benchmark Astra/Fable/Opus/Sonnet "su 5–10 task"; "agent boundary pack" come progetto separato (è il test R8); `test-automation-write.md`; i 5 file duplicati.

---

## 11. Model strategy (sintesi; Fase O)

| Uso | Modello | Perché |
|---|---|---|
| Coding quotidiano | quello dell'abbonamento Claude Code (oggi default Opus/Sonnet 5.5) | nessun benchmark QN vale il suo costo |
| Architettura / decisioni | stesso + Strategic Council (`gpt-5.6-sol` pinnato, DEC‑008) solo per tier 2–3 | già costruito, costo per domanda |
| Review | Codex app GitHub (modello scelto da OpenAI; non nostro) | indipendenza di vendor a costo zero |
| Classificazione / triage / dedup | **Haiku 5.5** con JSON schema; Decisions API/Luna da confrontare in P2 | 10–50× più economico; task chiuso |
| Geo‑risoluzione a zona | Haiku prima; fallback a Sonnet/Opus su confidenza < soglia | qualità 95 % è il requisito (handover §2.2) |
| Enrichment testuale | Sonnet 5.5 | costo/qualità |
| Browser / computer use | **nessuno** | non in architettura |
| Escalation | confidenza bassa → modello superiore → coda di review umana (DEC‑103) | mai pubblicazione automatica su dubbio |
| Fallback provider | nodo n8n primary/fallback (nativo ≥2.40) con prompt identico | sostituibilità |
| Quando NON usare frontier | tutto ciò che ha uno schema fisso e un golden set | — |
| Prompt caching | prefisso stabile (istruzioni + gazetteer zone list) in ogni chiamata; misurare hit‑rate in P2 | riduce costo e latenza |

Pinning: ID esatti nei nodi HTTP/Model e in `council/strategist.js`; cambio = riga in `prompts/CHANGELOG.md`.

---

## 12. Questioni aperte

1. **Cosa espone davvero l'MCP n8n su Cloud Starter** (log di esecuzione? permessi read‑only per client?) — si scopre solo abilitandolo (P1 stadio 1).
2. **Il permesso `contents: write` dell'app Codex** si può ridurre senza perdere la review? (test di 15 minuti).
3. **Chiave OpenAI per P2** (Decisions API): è di Riccardo; senza, P2 confronta solo Haiku vs frontier.
4. **Trigger n8n → codice custom** (§3.4): Riccardo accetta la soglia "terzo workflow / >50 % logica in code nodes"?
5. **Governance freeze**: è una decisione RED (tocca DEC‑009…013 per congelamento, non per modifica). Va scritta come DEC‑014 se Riccardo la vuole.
6. **AUP Anthropic / Roma 2027** (054): non verificato, non tecnico; Riccardo lo legge prima del 12 novembre.
7. **Sistemi di controllo** di cui QN **non** ha bisogno e che la review precedente dava per scontati: benchmark continui dei modelli, regression pack a ogni release, agent boundary pack come progetto. Se Codex dissente, è un disaccordo di *risk tolerance*, non fattuale.

## 13. Questioni sulle quali voglio esplicitamente il parere di OpenAI/Codex

1. **n8n o codice custom?** Codex revisiona il JSON n8n da settembre: trova le PR di workflow revisionabili? Confermerebbe n8n o spingerebbe verso codice con scheduler?
2. **Il valore della sua stessa indipendenza:** la review nativa su PR basta, o un reviewer che *esegue* (worktree, browser) trova difetti che la lettura non trova? Evidenza da PR #1–#13.
3. **Governance freeze:** eccesso di cautela o la cosa giusta?
4. **Livello di autonomia:** L3 su staging in 90 giorni è troppo o troppo poco?
5. **Haiku per classificazione geo:** la soglia 95 % di zona è raggiungibile con un modello piccolo + gazetteer, o serve frontier?
6. **La mia stima di saving** (§7), in particolare "sviluppo MVP già incassato".
7. **Baseline §8:** quali delle 12 regole toglierebbe, e quale manca.
8. **Dove Claude ha torto**, esplicitamente.

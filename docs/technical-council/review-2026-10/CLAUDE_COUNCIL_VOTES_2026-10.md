# CLAUDE COUNCIL VOTES — ottobre 2026

Voti per **tema**, non per candidato (i 57 candidati sono mappati ai temi in `COUNCIL_REVIEW_CLAUDE_2026-10.md` §4). Stati ammessi: APPROVE · PILOT · DEFER · REJECT · SUPERSEDED. Salvato prima di consultare Codex; non sarà modificato per convergere.

| # | Tema | Candidati | Claude vote | Conf. | Motivazione breve | Confronto OpenAI? |
|---|---|---|---|---|---|---|
| T1 | Regola di versioning "ultima stable, nessun floor numerico" + boundary pack di 6 test prima di pilot che scrivono (sostituisce tutti gli alert di release Claude Code / Codex / n8n) | 005, 007, 008, 009, 011, 012, 013, 015, 016, 018, 019, 021, 025, 030, 033, 034, 035, 036, 037, 038, 039, 041, 042, 043, 044, 046, 048, 049, 052, 053, 055 | **SUPERSEDED** (i candidati) / **APPROVE** (la regola) | 90 | CC 2.1.301, n8n 2.43.7, Codex ≥0.161 il 16 ott: ogni floor è già vecchio; i test retenuti valgono, i numeri no | sì, breve |
| T2 | Architettura: n8n Cloud resta runner e I/O; logica in `code-nodes/`; nessun nodo Agent in pipeline; trigger di riconsiderazione verso codice custom | 026, 033, 045, 057 (DEFER) + §3 | **APPROVE** | 70 | sunk learning + owner non tecnico + managed; ma il JSON non è revisionabile: regola code‑node‑first obbligatoria | **sì, centrale** |
| T3 | Pilot n8n MCP ufficiale: read su staging → write su workflow esposto → export JSON automatico | 004 | **PILOT** | 85 | unica proposta che elimina lavoro manuale reale di Riccardo; rollback a un click; docs ufficiali verificate (esposizione per workflow, permessi per client) | sì |
| T4 | Claude builder: confermato senza benchmark; cloud sessions come pratica; modello dichiarato/pinnato | 002, 017, 023, 024, 029 | **APPROVE** (023, 024) / **DEFER** (benchmark 002, 017, 029) | 80 | funziona, è su abbonamento, un benchmark QN costa più di quanto rende | sì, breve |
| T5 | Codex reviewer: solo review nativa su PR; ridurre `contents: write` dell'app; nessun harness/worktree/browser/Guardian | 001, 015, 019, 025, 030, 031, 035, 038, 049, 053 | **APPROVE** (ruolo ristretto) / **REJECT** (estensioni) | 75 | indipendenza a costo zero; ogni estensione è un secondo sistema da mantenere | **sì, centrale** (Codex giudica sé stesso: serve la sua evidenza) |
| T6 | Security Baseline a 12 regole (`docs/autonomy/SECURITY_BASELINE.md`) | 010, 014, 022, 028, 034, 040(parz.), + tutti i "security floor" | **APPROVE** | 85 | assorbe 18 candidati in 2 minuti di lettura; nulla di nuovo da costruire tranne ridurre un permesso GitHub | sì |
| T7 | WIF/OIDC e IP allowlist OpenAI | 040 | **DEFER** (WIF) / **REJECT** (IP allowlist) | 80 | nessun workload QN può presentare OIDC; n8n Cloud senza egress fisso | no |
| T8 | Model strategy in pipeline: Haiku 5.5 (o Luna/Decisions) per classificazione, triage, dedup; frontier solo fallback | 047, 050, 020, 027 | **PILOT** (047) / **DEFER** (050 dentro P2) / **REJECT** (027) | 80 | task chiusi con golden set esistente; 10–50× più economico; shadow mode senza rischio | sì (soglia 95 % geo) |
| T9 | Managed/agent platform: Agents API, computer use, Managed Agents dynamic workflows, browser SDK, durable Agent queue | 003, 032, 051, 056, 043 | **REJECT** (ora) → WATCH 6 mesi | 85 | QN non ha orchestrazione da sostituire; una pipeline editoriale deve essere deterministica | sì, breve |
| T10 | Governance freeze: nessuna nuova DEC sull'autonomia né estensione di lane gate/council CLI fino alla prima pagina pubblica | — (emergente) | **APPROVE** | 75 | 3.900 righe di governance vs 1.200 di pipeline; ultimo merge 2 set; AUTO‑GREEN spento per decisione | **sì, centrale** (risk tolerance) |
| T11 | Livello di autonomia: CURRENT L4 codice / L1 n8n; NEXT L3 staging n8n a 90 gg; L5 solo per categorie su dati reali con nuova DEC; L6 respinto | — | **APPROVE** | 80 | coerente con DEC‑012/013; l'MCP è il prerequisito di L2–L3 | sì |
| T12 | Capacità/costo abbonamenti | 006 | **REJECT** (come candidato) | 90 | si misura con `/usage` quando serve; non è una decisione di architettura | no |
| T13 | AUP Anthropic / Roma 2027 | 054 | **DEFER** → Riccardo | 60 | non verificato, non tecnico, scadenza 12 nov (UNVERIFIED) | no |
| T14 | Pulizia inbox: chiudere PR #14 senza merge, cancellare duplicati/stub, questa review come residuo (DEC‑007) | 042/44/45/46/50 dup, 023 stub, `test-automation-write.md` | **APPROVE** | 95 | igiene | no |

**Riepilogo:** 36 candidati SUPERSEDED · 7 APPROVE · 2 PILOT · 9 DEFER · 4 REJECT · 3 DROP · 5 duplicati · 1 stub · 058–066 inesistenti.
**Pilot NOW:** P1 n8n MCP · P2 Haiku classificazione · P3 code‑node‑first.
**Temi su cui il confronto con OpenAI è decisivo:** T2 (n8n vs codice), T5 (valore dell'indipendenza di Codex), T10 (governance freeze).

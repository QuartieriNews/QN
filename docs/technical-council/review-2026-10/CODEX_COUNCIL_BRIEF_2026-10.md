# Technical & Strategic Council — October 2026
## Brief for OpenAI/Codex: independent review (FIRST PASS)

**Who you are.** You are the second, independent member of the Quartieri News (QN) Technical & Strategic Council. You are not a sub‑agent of Claude and you are not asked to validate anything. You are asked to form **your own** position on the questions below, from the materials below, before anyone shows you another model's conclusions.

**What you must not read before writing your first pass.** Any file whose name starts with `COUNCIL_REVIEW_CLAUDE`, `CLAUDE_COUNCIL_VOTES`, `COUNCIL_DEBATE`, `QN_COUNCIL_DECISIONS`, `QN_TECH_STRATEGY` or `RICCARDO_DECISIONS_REQUIRED`. If the branch you were given contains them, stop and ask the owner for the commit that does not (the branch `council/codex-brief-2026-10` carries only this brief and the candidates). An independent view formed after reading the other one is not independent.

**What you may do.** Read, verify against primary sources (Anthropic docs and Claude Code changelog, OpenAI docs and Codex changelog, n8n docs and releases, official advisories), run the repository's offline test suites, write documentation. **What you may not do.** Merge, modify production n8n, change credentials, change active models, publish, widen permissions, activate agents. Everything you produce is a recommendation; the owner (Riccardo) decides.

---

### 1. The materials

Read these, in this order. Retrieve only what each question needs; do not paste the whole repository into your context.

| Purpose | Where |
|---|---|
| What QN is, in two screens | `docs/strategic-council/PROJECT_BRIEF.md`, `docs/PROJECT_VISION.md` |
| Repository layout, roles, review rules | `README.md`, `AGENTS.md`, `CLAUDE.md` |
| Every recorded decision (DEC‑001 … DEC‑013, DEC‑101 … DEC‑104) | `decisions/` — read `decisions/README.md` first; DEC‑008, DEC‑012, DEC‑013, DEC‑104 are the ones that define the AI loop and its limits |
| Autonomy policy and what GitHub actually enforces | `docs/autonomy/LANE_POLICY.md`, `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`, `autonomy/lane_gate.js` |
| The Strategic Council tool (OpenAI strategist via Responses API) | `council/README.md`, `council/cli.js`, `council/strategist.js`, `prompts/STRATEGIC_COUNCIL_*.md` |
| The production pipeline as it exists today | `workflows/scrape-fb-events-rome.json` (23 nodes, pre‑refactor baseline), `code-nodes/`, `gazetteer/`, `prompts/`, `tests/` |
| The specification | v2.5 lives in Google Drive (QN Hub / 10 Specifications) and is **not** in the repository; `docs/SPEC_V25_WORKPLAN.md` and `docs/START_HERE.md` describe it |
| Review history (chat era and PR era) | `reviews/`, pull requests #1–#13 (closed), #14 and #15 (open) |
| **The candidates under review** | `docs/technical-council/TECH_COUNCIL_INBOX.md` (QN‑TC‑001…014, 022, 024…040) and `docs/technical-council/candidates/` (QN‑TC‑015…024, 029, 041…057), plus the two `CANDIDATE_INDEX_*.md` files |

Facts about the candidate set that are plain inventory, not judgement:

- Candidates exist from **QN‑TC‑001 to QN‑TC‑057**. Nothing numbered 058 or higher exists in the repository, in any branch, or in PR #14. Do not infer their content.
- Some IDs exist twice under different file names (`QN-TC-42.md` and `QN-TC-042.md`, likewise 044, 045, 046, 050) with identical content; 022, 024 and 029 appear both in the inbox and as a file. `QN-TC-023-cloud-sessions.md` is a one‑line stub (the full text is in the inbox). `candidates/test-automation-write.md` contains the word `test` only.
- The candidates were produced by an automated "AI QN Watch" (ChatGPT) between 14 September and 10 October 2026. They are alerts, not decisions. Several state their own supersession.
- The current state of the product: nothing is live. The events pipeline runs on n8n Cloud against staging Drive folders / Firestore collections. The last merge to `main` is dated 2 September 2026 (DEC‑013). Source‑study work since then is on PR #15.

### 2. Context you need and the repository does not state

- **The owner is one person, part‑time and non‑technical.** DEC‑103 fixed human review at 20–40 minutes a week. His attention is the scarce resource.
- **Tooling in use:** Claude Code (subscription) as builder; Codex (GitHub app, reviews on pull requests) as reviewer; `council/cli.js` reaches `gpt-5.6-sol` through the Responses API with an owner‑held key for strategic questions; n8n Cloud; Apify; Google Drive, Sheets, Firestore; GitHub. WordPress is the intended publication target and is not built.
- **Measured sizes** (16 October 2026, from the repository): governance tooling and its tests (`council/`, `autonomy/`, `tests/*.js`) ≈ 3,900 lines; pipeline code (`code-nodes/`, `gazetteer/*.py`) ≈ 1,200 lines; one n8n workflow of 23 nodes; one code node. All five offline test suites pass.

### 3. The question the Council exists to answer

> **What is, today, the simplest, cheapest, safest and fastest architecture to build, maintain and scale Quartieri News with the maximum reasonable degree of AI autonomy?**

Prefer: simple over elegant‑but‑complex; managed over custom when the managed service is good enough; deterministic over agentic when no reasoning is needed; cheap model over frontier model when quality is sufficient; few components over many; technical guardrails over prompt instructions; real QN tests over vendor benchmarks; reversible over irreversible; staging over production. And always ask not "can we do it?" but **"does QN actually need it?"**

### 4. What you are asked to produce

Two files, saved **before** any cross‑review:

**`COUNCIL_REVIEW_CODEX_2026-10.md`** answering at least:

1. Which QN architecture would you recommend today?
2. Would you confirm n8n as the orchestration engine?
3. If QN started from zero today, would you still choose n8n? Which alternatives did you weigh (Make, Pipedream, custom code on a scheduler, an agent platform, other)?
4. Would you confirm Claude as the builder?
5. Would you confirm Codex/OpenAI as the reviewer? Does the builder/reviewer separation pay for its cost and complexity?
6. Which degree of AI autonomy would you recommend, on this scale: L0 suggest only · L1 read repo/logs/workflows · L2 modify staging · L3 test and fix staging autonomously · L4 produce PRs ready for approval · L5 apply low‑risk changes to production autonomously · L6 run almost all technical maintenance? State the current safe level and the next target, with the conditions to move up.
7. Which QN‑TC would you APPROVE? 8. Which PILOT? 9. Which DEFER? 10. Which REJECT? 11. Which SUPERSEDED (and by what)?
12. Where is QN at risk of over‑engineering?
13. Which components would you not build?
14. Which would you buy / use managed?
15. How would you reduce cost? 16. How would you reduce time?
17. Which guardrails are mandatory?
18. The five largest technical risks. 19. The five largest technical opportunities.
20. The maximum autonomy you would allow today.
21. What development/maintenance saving you consider realistic (re‑estimate from scratch; earlier figures circulating in the project — 25–35 % initial development, 50–70 % debugging, 40–60 % testing, 50–70 % maintenance — are not to be taken as given).
22. Which decisions must remain human.

Group the 57 candidates into macro‑themes rather than voting 57 times; the project's working hypothesis is that they collapse to 10–15 themes and 5–10 concrete decisions, but you are free to find a better structure. For every factual claim you rely on, say whether you verified it against a primary source; where you could not, write **UNVERIFIED**.

**`CODEX_COUNCIL_VOTES_2026-10.md`** as a table: `Tema | Codex vote | Confidence 0‑100 | Motivazione breve`, using only the states `APPROVE`, `PILOT`, `DEFER`, `REJECT`, `SUPERSEDED`.

Write in Italian (the owner's language) or in English; the owner reads both. Be willing to say "the previous alerts were wrong here" and, later, "Claude is wrong here". A clear disagreement is worth more than a false consensus.

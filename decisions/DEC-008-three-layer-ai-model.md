# DEC-008 — Three-layer AI operating model

Status: DECIDED

Rule: Quartieri News runs on three distinct AI layers, separated by job rather
than by capability.

1. **Strategic Council** — Claude Code (Claude Opus) as Operator / Product
   Architect, plus GPT-5.6 Sol as Systems Strategist. Deliberately
   non-technical-first: it challenges what to build, sequencing, cost and risk
   trade-offs, reversibility, level of detail, hidden assumptions and
   second-order effects, before design or implementation begins.
2. **Technical Council** — Claude Code plus Codex.
3. **Code review** — Claude Code plus Codex, the loop already recorded in
   DEC-104 and DEC-007.

The strategic critic is the **general reasoning** model `gpt-5.6-sol`, reached
through the OpenAI Responses API, never Codex. A coding model asked to critique
strategy would collapse layers 1 and 2 into one voice, and the second opinion
the Council exists to obtain would stop being independent. `council/strategist.js`
refuses a Codex model rather than relying on documentation alone.

Independence rule, binding on layer 1: for every new strategic question Claude
and GPT form their first view independently. Neither receives the other's first
answer before its own exists. Only then does cross-review begin. The separation
must remain visible and auditable, not merely intended.

Entering Strategic Council mode does not edit production code, design an
implementation, merge, deploy, or decide anything.

Only the owner decides. Model agreement is evidence, never authority; a council
result carries a `OWNER_DECISION_REQUIRED` flag and no numeric confidence score.

This does not reopen DEC-104 or DEC-007. DEC-104 fixed the build/review loop and
its roles; DEC-007 fixed where a code review is archived. Both stand unchanged.
DEC-008 adds a layer above them and names the model that occupies it.

Impact: `CLAUDE.md` (Strategic Council mode routing), `council/`,
`docs/strategic-council/`, `prompts/STRATEGIC_COUNCIL_*.md`. No pipeline,
gazetteer, prompt-of-record or n8n behaviour changes.

Decided by: Owner · Date: 31 August 2026 · Affected: CLAUDE.md, council/,
docs/strategic-council/, prompts/, DEC-104 and DEC-007 (unchanged, referenced).

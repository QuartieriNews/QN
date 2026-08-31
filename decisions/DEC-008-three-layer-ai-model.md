# DEC-008 — Three-layer AI operating model

Status: DECIDED
Blocks: nothing now — this entry gated the Strategic Council MVP (Issue #5),
which is implemented in the same change that records it.

Question: the project runs one AI loop, in which Claude builds and Codex reviews
(DEC-104). That loop judges code that is already being written. Should a layer
exist above it to challenge *what* is worth building, and if so, which model
occupies it?

Options:
A. One loop. Strategic questions are answered inside the build/review loop by
   the same two models.
B. A separate strategic layer, with Codex as the critic — one fewer vendor and
   one fewer prompt to maintain.
C. A separate strategic layer, with a general reasoning model as the critic.

Claude recommendation: C. Under A there is no independent challenge to the
framing of a question, only to the code that answers it. B looks cheaper but
gives the critic's seat to the model that already reviews the implementation:
the second opinion stops being independent, and a coding model is optimised for
whether code is correct rather than whether it should exist. The cost of C,
stated plainly, is a second vendor, a second key, and a per-question spend the
owner controls.

ChatGPT recommendation: not sought; this was decided before the Council existed.

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
pins that model rather than defaulting to it: running the Council on another
model would widen this entry silently, and widening it is a new owner decision.

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
gazetteer, prompt-of-record or n8n behaviour changes. Recurring cost: one
OpenAI key and a per-question spend the owner controls; no minimum commitment.

Decided by: Owner · Date: 31 August 2026 · Affected: CLAUDE.md, council/,
docs/strategic-council/, prompts/, DEC-104 and DEC-007 (unchanged, referenced).

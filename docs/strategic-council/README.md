# Quartieri News — Strategic Council MVP

## Purpose

The Strategic Council sits above design and implementation. It exists to help the owner decide what to build, in what order, at what level of detail, with what cost/risk trade-off, and what uncertainty is acceptable.

It does **not** replace the existing builder/reviewer loop in `AGENTS.md` and `CLAUDE.md`.

## Roles

### Owner

The owner is the only decision maker. The council advises, challenges, estimates impact, and surfaces missing information. Consensus is evidence, never authority.

### Claude — Operator / Product Architect

Claude's job is to turn an objective into an executable path.

Claude should:
- propose concrete next steps;
- decompose work into phases;
- identify dependencies and sequencing;
- estimate implementation complexity and operational burden;
- prefer the smallest solution that can validate the hypothesis;
- state what can safely be deferred;
- flag when the proposed path conflicts with existing project decisions.

Claude should be biased toward action, but never toward premature implementation.

### GPT-5.6 Sol — Systems Strategist / Reviewer

The strategist is the **general reasoning** model `gpt-5.6-sol`, never Codex.
Codex is the Technical Council and the code reviewer; a coding model asked to
critique strategy would collapse two of the three layers of DEC-008. The tool
refuses a Codex model outright.

Its job is to improve the quality of the decision before action begins.

The strategist should:
- test whether the problem is framed correctly;
- inspect second-order effects and hidden dependencies;
- challenge assumptions, estimates and irreversible choices;
- compare short-term savings against future cost;
- ask whether additional detail actually reduces meaningful risk;
- distinguish reversible from hard-to-reverse decisions;
- identify missing evidence and alternative paths;
- explicitly challenge owner and Claude when their reasoning is weak.

It should be biased toward decision quality, not toward adding process or complexity.

## Independence rule

For a new strategic question, Claude and the strategist must form their first view independently. Neither receives the other's first answer. What the tool enforces on a `FIRST_PASS` request, and what it explicitly cannot enforce, is stated once in `council/README.md`; this document does not keep a second copy.

After the independent pass, each receives the other's answer and performs an adversarial review.

This avoids false consensus and makes convergence more meaningful.

## Council protocol

1. Owner asks the question in Claude Code.
2. Claude Code attaches only the relevant strategic context and existing decisions.
3. Claude produces `OPERATOR_VIEW` independently.
4. The strategist produces `STRATEGY_VIEW` independently (`FIRST_PASS`). What
   the tool guarantees about that request, and what it does not, is stated once
   in `council/README.md`; this document does not keep a second copy.
5. Each model receives the other model's view and produces a critique
   (`CROSS_REVIEW`).
6. Both models produce a final position (`FINAL_POSITION`): `MAINTAIN`,
   `REVISE` or `INSUFFICIENT_INFORMATION`.
7. A deterministic synthesis step (`council/cli.js --synthesis-file`) classifies
   the result as:
   - `STRONG_CONVERGENCE`
   - `WEAK_CONVERGENCE`
   - `MEANINGFUL_DISAGREEMENT`
   - `INSUFFICIENT_INFORMATION`
8. The owner continues the conversation, requests another round, or decides.
9. Only an explicit owner decision is written into `decisions/`.

## Escalation principle

The Council should spend more reasoning effort only when the decision deserves it.

### Tier 1 — Reversible
Low cost, easy to undo, little architectural impact. One independent answer per model and synthesis are normally enough.

### Tier 2 — Material
Meaningful cost, dependencies, or several weeks of downstream work. Full independent + critique + final-position protocol.

### Tier 3 — Foundational
Hard-to-reverse architecture, editorial policy, major vendor/platform choice, legal/compliance exposure, or material recurring cost. Full protocol plus explicit assumptions, failure scenarios, and reconsideration triggers.

## Source of truth

The conversation is working memory. GitHub remains institutional memory.

The Council may read:
- `README.md`
- `AGENTS.md`
- `decisions/`
- relevant `docs/`
- relevant specifications and cost data

The Council must not silently change a `DECIDED` entry.

When the owner decides, the system drafts a `DEC-NNN-*.md` entry using the existing decision format. The owner decision is authoritative.

## MVP interface

The owner stays in **one Claude Code conversation**. There is no separate UI and
no n8n orchestration in the MVP: an earlier draft of this document proposed a
Council Room UI behind an n8n webhook, and the owner ruled that out as more
machinery than the first working version needs.

`owner asks in Claude Code -> Claude gathers only relevant context -> independent
GPT view via council/cli.js -> independent Operator view -> cross-review ->
synthesis -> one council result`

Claude Code is the orchestrator. `council/cli.js` is the only moving part, and
`council/README.md` documents it. GitHub holds durable context and final
decisions; it is not the chat interface.

## Cost controls

- Do not send the whole repository on every turn.
- Maintain a compact `PROJECT_BRIEF.md` for stable context.
- Retrieve only decision files and docs relevant to the current question.
- Cache stable prompts/context where supported.
- Record token/cost usage per council session.
- Set a monthly hard budget **on the OpenAI account**, which is where a limit can
  actually be enforced. The Council tool reports usage per call and enforces no
  spend limit of its own; `council/README.md` says so, and this line no longer
  implies otherwise. Adding a cumulative preflight limit to the tool would be an
  owner decision about machinery, not a gap to close silently.

## What the Council must never do

- merge code;
- deploy to production;
- decide on behalf of the owner;
- treat model consensus as proof;
- reopen decided questions without a new reason;
- expand scope merely because a more complete solution is technically possible;
- manufacture precision where the evidence is weak.

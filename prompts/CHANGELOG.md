# Prompt changelog

One entry per prompt change, newest first. Every entry states: date, prompt file, what
changed, why, and which revision integer it bumps (`generation_revision` or
`geo_logic_revision`). The revision values in production must match the top of this file.

Current state — 28 August 2026:

| Prompt family | File | Revision | Set by |
|---|---|---|---|
| Geography (both passes) | `PROMPT_GEO_BLOCK.md` | `geo_logic_revision` = 5 | Spec v2.5 (resolution method replaced) |
| Editorial classification | `EDITORIAL_FILTER.md` | — (gated by `editorial_pass_enabled`) | Release 1.4.3–1.4.5 |
| Article generation | stored in n8n / Drive config | `generation_revision` = 4 | Spec v2.4, unchanged in v2.5 |

Open item blocking the editorial prompt going live: the commercial-guided-tours decision
(`tests/golden_set_editorial.json → known_gap`, Drive decision log D-001).

---

## 31 August 2026 — Strategic Council role prompts added

Files: `STRATEGIC_COUNCIL_CLAUDE.md` (Operator / Product Architect),
`STRATEGIC_COUNCIL_CHATGPT.md` (Systems Strategist).

What changed: both role prompts are new, and the strategist prompt gained a line
stating that it is the general reasoning model rather than the project's coding
model, so the reader of the prompt sees the boundary DEC-008 draws.

Why: the Strategic Council MVP (DEC-008, Issue #5). The strategist prompt is
read from this repository at call time and sent as the request instructions, so
it is a prompt of record and belongs in this log.

Revision bumped: **none, and none applies.** The revision integers this log
tracks — `generation_revision` and `geo_logic_revision` — belong to the article
generation and geography passes of the events pipeline. Council role prompts sit
outside that pipeline: they affect no published item, no gazetteer resolution
and nothing in n8n. Introducing a third revision integer for them would be a
contract change, and therefore an owner decision, not a side effect of this
change. Until such a decision exists, Council prompt changes are versioned by
their entry here and by the commit that made them.

---

## 31 August 2026 — Council role prompts state a cross-review output

Files: `prompts/STRATEGIC_COUNCIL_CHATGPT.md`, `prompts/STRATEGIC_COUNCIL_CLAUDE.md`

What changed: both cross-review sections now say what to return, under a
`### CROSS_REVIEW` heading, in the same shape as their first-pass sections.

Why: the cross-review had instructions but no stated output, so a refusal there
returned ordinary prose and nothing could tell it from a critique. The final
stage requires only that the exchange be nonempty, so a council could conclude
without the adversarial step that makes its convergence mean anything. The tool
now requires the heading on a `CROSS_REVIEW` response, which it can only do if
the prompt of record asks for one.

Revision bumped: none, and none applies — for the reason given in the entry
above; Council prompts sit outside the pipeline revision integers.

---

_No pipeline prompt changes yet after the v2.5 consolidation._

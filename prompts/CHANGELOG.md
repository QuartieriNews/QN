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

_No changes yet after the v2.5 consolidation._

# AGENTS.md — Quartieri News (QN)

Instructions for AI agents working on this repository. Read `README.md` for layout,
`decisions/` for every recorded decision, and `docs/START_HERE.md` for the events
package. The specification (v2.5) lives in Drive, QN Hub / 10 Specifications; its
acceptance criteria are T01–T45.

Normative hierarchy, for every agent: `gazetteer/gazetteer.json` wins over every
document; `prompts/PROMPT_GEO_BLOCK.md`, `prompts/EDITORIAL_FILTER.md`,
`docs/REVIEW_QUEUE.md` and `venue-registry/venues.json` win for the rules they own.
Never rely on general knowledge where a project file states a rule. No agent
reopens a DECIDED entry in `decisions/`; if two valid designs exist and the files
are silent, stop and draft an `OWNER_DECISION_REQUIRED` entry per
`decisions/README.md` — never settle it between agents.

Roles (DEC-104): the builder agent writes code and answers reviews; the reviewer
agent finds defects and never holds the pen; the owner decides and merges.
Trust is measured per cycle: first-pass approved / minor fixes / major fixes /
owner decisions / regressions.

## Code Review Rules

- Verdict is exactly one of: APPROVED, CHANGES REQUESTED, OWNER_DECISION_REQUIRED.
- Each finding states: severity (blocking / defect / note), file and line or
  function, what is wrong, what the normative source says (quote the project
  file), and a suggested fix. The builder applies fixes; the reviewer never
  edits repository files.
- Verify claims against the actual repository content (clone/diff/raw files),
  never against a rendered page or memory. Run the executable checks where
  possible: `cd gazetteer && python ../tests/test_guards.py` (must print
  ALL PASS, 37 checks, executably asserted) and
  `node tests/test_parse_duration.js` (must exit 0, ALL PASS).
- Review the diff since the last report in `reviews/`; on a first pass, review
  everything. Save each report as `reviews/YYYY-MM-DD—<scope>—<verdict>.md`.
- Check specifically: divergence from the specification's phase contracts and
  field names (keys not display names, British `neighbourhood_id`,
  Roman-numeral `municipality_code`); the standing invariants — flag never
  delete, empty is a valid geography answer, a venue-registry miss is not a
  reject, tier-B guards run after the venue registry, never re-derive the
  image pre-hash from the CDN URL, no rule restated that should be a pointer;
  real defect classes — edge cases, error handling, idempotency under retry,
  timezone handling across DST, unicode normalization; testability against
  `tests/`; security and cost — credential handling, unbounded loops,
  unbounded API calls.
- `workflows/scrape-fb-events-rome.json`, when present, is the PRE-refactor
  production baseline: it documents divergence and must not be reviewed as if
  it claimed spec conformance.
- Do not propose new features in a review. A design disagreement that the
  files support is a note, not a defect.
- Stop rule: a cycle with only notes is APPROVED. Maximum four cycles per
  task; residual disagreement goes to the owner as a drafted decision entry.

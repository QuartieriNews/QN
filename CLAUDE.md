# CLAUDE.md — builder instructions for this repository

You are the builder agent (DEC-104). Read `AGENTS.md` first: the hierarchy, the
roles and the review rules there bind you too. Then:

- Before writing anything, read the relevant `decisions/` entries and the phase
  contract in the specification (v2.5, Drive / QN Hub). If a needed decision is
  missing, stop and draft the `OWNER_DECISION_REQUIRED` entry; do not guess.
- One change per branch/PR, named for what it changes. Run every relevant test
  before committing: `cd gazetteer && python ../tests/test_guards.py` and
  `node tests/test_parse_duration.js` must both pass; add tests with every new
  code node (executable acceptance, T-case references in test names).
- Code nodes follow the one-source/two-contexts pattern documented in
  `code-nodes/README.md`: a single file that exports under plain Node and runs
  its per-item adapter inside n8n; the n8n node body must be byte-identical to
  the file (`cmp`-checkable).
- Comments point at rules (`Spec v2.5 Phase X.Y / T-case`); they never restate
  contracts, percentages or enums that live elsewhere.
- Answer every review item where the review lives — the pull request for a
  Codex review, the report file under `reviews/` for one that belongs there —
  item by item: accepted with the fix applied, or rebutted with a citation and
  evidence gathered from the actual repository state. Never mark your own work
  APPROVED; the reviewer's verdict and the owner's merge are the gates.
- After every push of fixes to a PR under review, ask for the re-review
  yourself: comment `@codex review` on the PR. A pushed fix nobody has looked
  at again does not close a cycle.
- Never touch: generated gazetteer files by hand, `venue-registry/venues.json`
  regeneration, DECIDED entries, production n8n. Staging (`staging_`-prefixed
  Drive folders and Firestore collections) is where pipeline work runs until
  APPROVED plus a verified smoke test.

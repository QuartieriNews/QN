# reviews/

Historical memory of the chat era, when a review had nowhere else to live, plus
the home of review reports tied to no pull request. A Codex review of a PR is
archived by the PR itself — see the Code Review Rules in `AGENTS.md`, which own
this rule (`decisions/DEC-007`); do not copy such a review here.

Naming: `YYYY-MM-DD—<scope>—<verdict>.md`.
Template: Drive → QN Hub → 30 Reviews → *Review Report — Template*.

The report must state what it reviewed against (spec version + `gazetteer.json`), the
numbered defect list, and which acceptance criteria were exercised (T-cases,
`test_guards.py` exit code, golden sets). A review that cites memory instead of the files
is invalid.

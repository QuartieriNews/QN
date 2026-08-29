# reviews/

Review reports written by the review AI, one per pull request, before merge.

Naming: `PR-<number>—<verdict>.md` (e.g. `PR-7—approve-with-notes.md`).
Template: Drive → QN Hub → 30 Reviews → *Review Report — Template*.

The report must state what it reviewed against (spec version + `gazetteer.json`), the
numbered defect list, and which acceptance criteria were exercised (T-cases,
`test_guards.py` exit code, golden sets). A review that cites memory instead of the files
is invalid.

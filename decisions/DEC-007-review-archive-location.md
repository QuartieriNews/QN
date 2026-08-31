# DEC-007 — Where a code review is archived

Status: DECIDED

Rule: option A, with a clause. The pull request is the archive of a code review:
findings, builder answers and the verdict live in its threads, attached to the diff
they judge, and are not copied into `reviews/`. `reviews/` keeps the era-chat
reports as historical memory and remains the home of reports tied to no PR.

Clause: a pull request closed without merging, where the work or the review taught
something worth keeping, leaves that behind in writing — a note in `reviews/` or a
decision entry. Closing a PR is what discards its threads, so this is the one case
where the archive needs a hand. It answers the cost named in the recommendation
below: the review of a PR that never merges is otherwise easy to lose track of.

Question: Codex now reviews pull requests natively in this repository, so a review
no longer has to be transcribed into a file to exist. Does the pull request become
the archive of a code review, or do committed reports in `reviews/` remain the
archive?

This supersedes context, not rule text, of DEC-104 (DECIDED, 29 August 2026): that
entry records the loop as "ChatGPT reviews (mandate in
reviews/REVIEW_MANDATE_CODE.md)" and keeps the repository public because "a public
repo is what lets the reviewing AI read it from a flat-rate chat session at zero
marginal cost". Reviewing from a chat session is what made a committed report the
only durable record. That premise no longer holds; DEC-104 is not re-asked here,
and its parts 1–3 stand.

Options:
A. The PR is the archive. Findings, builder answers and the verdict live in its
   threads, attached to the diff they judge. `reviews/` keeps the era-chat reports
   as historical memory and remains the home of reports tied to no PR.
B. Committed reports remain the archive. Every Codex review is transcribed into
   `reviews/` before merge, as today.
C. Both: the PR carries the review, and a short report is still committed per cycle
   as an offline-readable index.

Claude recommendation: A. A transcribed review is a second copy of something the PR
already holds, and the repository's own standing invariant is that a rule — or a
record — is not copied where a pointer will do. B keeps a manual transcription step
whose only original purpose was durability that the PR now provides. C pays the
transcription cost of B for a convenience that the PR list already gives. The cost
of A is real and should be named: the archive then depends on GitHub and on Codex's
retention, and a review of a closed-without-merge PR is easy to lose track of.

ChatGPT recommendation: none on the substance. Codex reviewed the PR carrying this
change and raised one blocking finding — that the archive could not move without a
decision entry recorded here — which is why this entry exists. It did not argue for
any of A, B or C; on the fixed head it returned no further findings.

Impact: AGENTS.md Code Review Rules, CLAUDE.md builder rules, README.md (the
`reviews/` layout row, PR convention 4, and the "merge without a review report"
invariant), reviews/README.md. No code, test or pipeline behaviour.

Decided by: Owner · Date: 31 August 2026 · Affected: AGENTS.md, CLAUDE.md,
README.md, reviews/README.md, DEC-104 (context only). The rule text was merged in
PR #3 before this entry was decided; the clause and this status land separately.

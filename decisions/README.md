# decisions/

The decision log of Quartieri News. **A decision exists only if it is written here.**
This folder replaced the Drive decision log on 29 August 2026 (DEC-104), because both
AIs in the development loop must be able to read every decision on every cycle.

Rules:

1. One file per decision, named `DEC-NNN-short-slug.md`. Numbers 001–099 are open or
   product decisions; 101+ are recorded decisions imported from the project history.
2. Status is `OPEN` or `DECIDED`. A decided entry is **never deleted and never re-asked**;
   if circumstances change, a new decision supersedes it. **Recording a supersession takes
   two links, not one**: the new entry says which entries it supersedes and in what part,
   and it adds a one-line pointer under the `Status:` line of each entry it supersedes,
   naming itself as the entry that now carries current policy. The pointer is navigation
   metadata; the historical clauses are never rewritten to match what replaced them.
   Without it a reader who opens the older entry alone sees `DECIDED` and no sign that it
   was superseded — which is how withdrawn policy gets acted on.

   This binds supersessions recorded from now on. One earlier case is left as it stands:
   DEC-007 supersedes the *context* of DEC-104 and says so, while DEC-104's rules are
   unaffected, so DEC-104 carries no pointer. Adding one is an owner decision about an
   entry no finding has shown to mislead, not a gap in this rule.
3. Only the owner decides. The AIs may recommend, estimate impact, and must stop and
   raise `OWNER_DECISION_REQUIRED` instead of debating — see the Operating Model in
   Drive, QN Hub / 00 Governance.
4. An open decision that blocks work says what it blocks in its `Blocks:` line.

Template: see any DEC file. Required fields: Status, Question, Options, Recommendation
(each AI, if any), Impact, Blocks, Decided by, Date, Affected components.

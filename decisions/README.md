# decisions/

The decision log of Quartieri News. **A decision exists only if it is written here.**
This folder replaced the Drive decision log on 29 August 2026 (DEC-104), because both
AIs in the development loop must be able to read every decision on every cycle.

Rules:

1. One file per decision, named `DEC-NNN-short-slug.md`. Numbers 001–099 are open or
   product decisions; 101+ are recorded decisions imported from the project history.
2. Status is `OPEN` or `DECIDED`. A decided entry is **never deleted and never re-asked**;
   if circumstances change, a new decision supersedes it and links back.
3. Only the owner decides. The AIs may recommend, estimate impact, and must stop and
   raise `OWNER_DECISION_REQUIRED` instead of debating — see the Operating Model in
   Drive, QN Hub / 00 Governance.
4. An open decision that blocks work says what it blocks in its `Blocks:` line.

Template: see any DEC file. Required fields: Status, Question, Options, Recommendation
(each AI, if any), Impact, Blocks, Decided by, Date, Affected components.

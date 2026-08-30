# DEC-005 — Schema 2.0 migration mode

Status: OPEN (recorded in spec v2.5 Part III, awaiting owner sign-off)
Blocks: nothing operationally; formal sign-off item

Question: accept the migration decision recorded in spec v2.5 — schema_version
1.0 → 2.0 with no bulk rewrite; 1.0 records migrate through the geo_logic_revision
bump when next touched; consumers of untouched 1.0 files apply the rename table.

Options:
A. Accept as recorded (recommended by Claude; the registry decision table already
   owns exactly this job, and a migration script would be a second writer).
B. Require a one-off migration script instead.

Impact: near-zero today (corpus is small and pre-publication); defines the standing
pattern for every future breaking change.

Decided by: — · Date: — · Affected: Part III of the specification.

# DEC-015 — Automatic publication with dual AI control and an exception queue

Status: DECIDED
Supersedes in part: DEC-103 (unchanged and not reopened; the clauses this entry
supersedes, qualifies and leaves intact are listed below).

Question: under which model are the contents of every block published and controlled,
given that DEC-103 fixes for Events a reject queue plus a weekly sample of 20 published
and 10 auto-excluded items, one reviewer at 20–40 minutes per week, and fixes only in
the registries?

Options:
A. Extend DEC-103 informally to the new blocks.
B. **CHOSEN.** A new model: automation by default, dual AI control, an exception queue,
   a sample stratified by content type, an error taxonomy, per-item traceability and
   corrections.
C. Human pre-publication review of every content.

Claude recommendation: in Rounds 1–2 the Council asked that the extension to the new
blocks be an explicit decision, not an informal extension (Round 1 §11.4b; Round 2
§8.3); model B is consistent with `docs/PROJECT_VISION.md` §5–6.

ChatGPT recommendation: the same (Round 2, part B: "DEC-103 must not be extended
informally").

## Rule

- Automation by default, human intervention by exception; no pre-publication review
  per content.
- First AI, production and classification: if a necessary element is ambiguous (the
  neighbourhood included) the content is not published and goes to the manual queue.
- Second AI, verification, functionally independent of the first: it consults the
  original source and checks correspondence, data, dates, temporal validity, geography
  and sensitive elements; in doubt it sends the item to the queue.
- Automatic publication only when both AIs pass and the deterministic checks succeed.
- The owner reviews every blocked item and samples the published ones; manual decisions
  are recorded and reused to improve prompts, rules and criteria.
- Errors: **critical** (wrong person, false attribution, wrong judicial status,
  sensitive information not in the source, harmful datum) — zero tolerance and a
  pipeline check; **material** (changes the meaning or usefulness of the content) — at
  most one per 50 sampled items; **minor** — recorded and corrected.
- The sample covers automatically published content and is stratified by content type,
  so that Events do not crowd out Amministrazione and Cronaca.
- Models, providers and thresholds are defined during development. The decided
  requirement is the functional independence of production and verification. A first
  set of items may be checked in full during development, not in steady state.

## Sampling baseline (owner's precision, 11 September 2026)

The weekly 20+10 sample inherited from DEC-103 is a **provisional technical baseline for
Events**. It is not a KPI, not a launch requirement, and not a rule automatically extended
to every block. The sampling of automatically published content is stratified by type
and may be recalibrated during development on the observed volume and errors. The
guardrails are confirmed: zero critical errors and at most one material error per 50
sampled items (DEC-017).

## DEC-103 clauses

Superseded: "every fix lands in the gazetteer, the venue registry or the source registry,
never in the individual item" — for content corrections and rectifications concerning
persons, which are per item with internal traceability (DEC-020); and the scope limited
to Events — this model covers every block.

Qualified, not cancelled: the weekly sample of 20 published and 10 auto-excluded items
remains the reference size as the provisional Events baseline above, with its
composition now stratified by type — the owner has not declared its size or cadence
superseded; "one reviewer, 20–40 min/week" remains the Events baseline and is no longer
read as a total budget (the owner's 30 hours per week are the total, with no automatic
thresholds: DEC-017).

Intact: the reject queue sorted by structured reason; the recording of manual decisions;
geographic fixes in the registries.

Impact: `docs/REVIEW_QUEUE.md`; `prompts/` (new prompts of record for generation and
verification, with changelog); `gazetteer.json → review`; the specification of the new
blocks. Visible legal question: whether the model satisfies the exemption of art. 50(4)
AI Act (DEC-019).

Blocks: nothing (this entry unblocks the specification of the Institutional and Cronaca
blocks and of post-launch sampling).

Decided by: Owner · Date: 11 September 2026 (Strategic Council Round 2 Reconciliation,
owner confirmation) · Affected: DEC-103 (pointer), `docs/REVIEW_QUEUE.md`, `prompts/`,
spec v2.5 Part I §9.

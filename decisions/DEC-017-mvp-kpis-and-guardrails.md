# DEC-017 — KPIs and guardrails of the MVP

Status: DECIDED

Question: by which indicators is the MVP judged six months after the public launch?

Options:
A. A package of metrics with payment qualifiers and territorial thresholds (Rounds 1–2).
B. **CHOSEN.** Two primary KPIs, two secondary indicators of direction, two guardrails,
   no automatic qualifiers.

Claude recommendation: A as measuring instruments; the owner chooses B and keeps the
qualifiers as private observations, not thresholds.

ChatGPT recommendation: the same.

## Rule

Primary KPIs:
1. at least 1,000 monthly unique users on the whole network in the sixth month after
   the public launch;
2. at least one real advertising payment within six months — a binary datum, judged by
   the owner in its context, without automatic qualifiers.

Secondary indicators of direction, not binding: share of new users who return on a
later day within 30 days (25% as a provisional reference); unique and active newsletter
subscribers (300 at six months as a stretch), counting unique addresses and per-
neighbourhood subscriptions separately.

Guardrails: at most one material error per 50 sampled items and zero critical errors
(DEC-015); incidence of content sent to manual review.

Measures net of internal traffic, bots and tests; provenance when useful; monthly
observation, judgement in the sixth month. No automatic thresholds on the owner's
workload: the 30 hours per week are the total available time, prioritised by the owner.

Excluded: 300 unique users at month 4; at least five neighbourhoods with 30
subscribers; correction within 48 hours; payment at 70% or more of a price list;
non-personal contact; a minimum number of prospects; other territorial thresholds.
The 20+10 sample is a provisional technical baseline (DEC-015), not a KPI.

Impact: measuring instruments with a first-party identifier (legal question on consent:
Round 2 Reconciliation §8, point 13); free campaigns (DEC-021) are not counted in KPI 2.

Blocks: nothing (this entry unblocks the measurement instrumentation at launch).

Decided by: Owner · Date: 11 September 2026 (Strategic Council Round 2 Reconciliation,
owner confirmation) · Affected: site (analytics), newsletter (counts),
`docs/REVIEW_QUEUE.md` (sample).

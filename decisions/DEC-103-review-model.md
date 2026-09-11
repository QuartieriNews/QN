# DEC-103 — Review model: queue + weekly sample

Status: DECIDED (release 1.4.3)
Superseded in part by DEC-015 and DEC-020 — see DEC-015 for the current publication
and sampling model of every block and DEC-020 for the current correction policy. This
entry is the historical record of the decision taken; its clauses are unchanged. The
reject queue, the 20+10 sample as the provisional Events baseline and the registry
fixes for geographic corrections remain in force.

Rule: human review targets the reject queue (sorted by structured reason) plus a
weekly sample of 20 published and 10 auto-excluded items; every fix lands in the
gazetteer, the venue registry or the source registry, never in the individual item.
Supersedes mandatory per-item review of spec ≤ 2.4. Constraint honoured: one
reviewer, 20–40 min/week.

Decided by: Owner · Date: August 2026 (release 1.4.3) · Affected: Part I §9,
REVIEW_QUEUE.md, gazetteer.json → review.

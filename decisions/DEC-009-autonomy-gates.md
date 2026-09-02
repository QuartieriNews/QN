# DEC-009 — GREEN / AMBER / RED autonomy gates

Status: DECIDED

Question: may agents continue execution autonomously, and merge their own work
automatically in a narrowly defined lane, without an AI thereby converting a new
judgement call into an implicit owner decision?

Options: not recorded. This entry states the decision reached rather than the
alternatives weighed; the three lanes below are the answer, not a menu.

Recommendation: none recorded. No separate AI recommendation was captured for this
entry — it records the owner's decision directly.

Impact: repository governance, the builder/reviewer development loop, merge policy, and
future GitHub rules and actions, as listed in the closing line. It supplements DEC-104's
builder/reviewer/owner separation and DEC-008's three-layer AI model without reopening
either.

Blocks: nothing. The implementation this entry authorises is a separate change, to be
defined and reviewed in its own pull request.

*The five fields above were added after the entry was decided, under explicit owner
authorisation, to meet the format `decisions/README.md` requires. They restate what the
entry already contained and state plainly where nothing was recorded. No substantive
clause was changed.*

Rule: Quartieri News distinguishes **decision authority** from **execution authority**. The owner remains the only authority for product, strategic and normative decisions, but agents may continue execution and, in a narrowly defined GREEN lane, may merge work automatically when every mechanical gate is satisfied.

The purpose is to allow useful unattended work — including overnight work — without allowing an AI to convert a new judgement call into an implicit owner decision.

## GREEN — autonomous through merge

A change is GREEN only when all of the following are true:

- it implements or fixes behaviour already authorised by a DECIDED decision, accepted specification or owner-approved task;
- it does not create or alter a product, editorial, governance, architecture, vendor/platform or material recurring-cost decision;
- the work is reasonably reversible and does not introduce a new hard-to-reverse commitment;
- it does not modify a protected/normative area designated by the implementation of this decision;
- all required automated tests/checks pass on the exact head commit;
- the independent code-review gate is clean on that exact head commit;
- there are no unresolved blocking review findings or `OWNER_DECISION_REQUIRED` conditions;
- the deterministic merge gate can prove the conditions above rather than relying on the builder's judgement alone.

A GREEN change may be merged automatically. Auto-merge is an execution of a decision already made; it is not a new decision.

## AMBER — autonomous preparation, owner merge

A change is AMBER when implementation can proceed under existing decisions but the impact is material enough that the owner should see the final result before it reaches `main`.

Typical AMBER cases include substantial refactors, broad operational changes, high blast-radius modifications, difficult-but-not-foundational reversibility, or other cases explicitly designated by repository policy.

Agents may design, implement, test and review AMBER work autonomously. The final merge requires the owner.

## RED — owner decision required

A change is RED when it requires a new judgement or changes an existing normative commitment, including a new or superseding DEC, strategic/product scope, editorial policy, governance, foundational architecture, material vendor/platform choice, significant recurring cost/risk, or another hard-to-reverse commitment.

RED work stops at `OWNER_DECISION_REQUIRED` before the system silently chooses among valid alternatives. Agents may gather evidence, compare options and recommend a path, but only the owner decides.

A PR that changes this autonomy policy or its protected normative rules is itself RED.

## Escalation rule

Uncertainty always escalates autonomy; it never expands it.

- If GREEN cannot be proven, treat the work as AMBER.
- If AMBER reveals a new decision, treat it as RED.
- Agents may escalate GREEN → AMBER → RED autonomously.
- Agents must not downgrade AMBER or RED merely to preserve unattended execution. A downgrade that changes the required owner involvement is an owner decision.

## Merge-gate principle

GREEN auto-merge must be controlled by a deterministic gate, not by Claude deciding that its own work is safe. At minimum the implementation must verify the exact reviewed commit, required test/check status, unresolved blocking findings, owner-decision flags, and protected/normative path restrictions.

Roles are assigned by DEC-104 and are not restated here. What this entry adds is that neither role may self-approve its own work.

If the available Codex GitHub integration cannot produce a machine-verifiable approval state, the implementation must choose a conservative auditable signal or keep that work AMBER; it must not weaken the independent-review requirement simply to enable auto-merge.

## Production boundary

Permission to auto-merge GREEN work into `main` does **not** by itself authorise automatic deployment to production, modification of production n8n, credentials, external paid services, or other operational actions that are governed separately. Those require their own existing authorisation.

## Operating goal

When the owner is absent, independent GREEN tasks should be able to continue through build → tests → Codex review → corrections → re-review → merge → next authorised task. AMBER and RED work must not block unrelated GREEN work when those tasks can safely proceed independently.

This decision supplements DEC-104's builder/reviewer/owner separation and DEC-008's three-layer AI model; it does not reopen them.

Decided by: Owner · Date: 31 August 2026 · Affected: repository governance, Claude/Codex development loop, merge policy, future GitHub rules/actions. Implementation details to be defined and reviewed in a dedicated PR.
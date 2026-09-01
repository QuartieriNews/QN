# The reinforced technical control

The final audit RED requires, and AMBER may request. DEC-010 decided its shape;
`LANE_POLICY` §10 states the rules; this document is how it is run.

## What it is, and what it is not

Two audits of the same final head: Claude in a fresh context, Codex separately, neither
seeing the other's result before producing its own, any finding blocking the merge.

It is **separated defence in depth. It is not independence, and the word is not used
for it.** Both auditors are language models working from shared mandates, shared tests
and the same repository; they can miss the same thing for the same reason. What the
separation buys is narrower and real: the fresh context removes the builder's
anchoring — the things it convinced itself were fine while writing them — and the
sealed collection removes the first report's influence on the second. Neither removes
correlation, and no arrangement of these two auditors would.

Claiming more than that would be the failure this whole design exists to prevent: model
agreement is evidence, never authority (DEC-008).

## Procedure

1. **Freeze the head.** The audit is of one commit `H`. Record it in full, with the base
   `B` and the policy version.
2. **Claude audits in a fresh context** — a session that did not build the change. It is
   given the authorised requirement, the repository and the diff. It is *not* given the
   builder's reasoning, its pull-request comments, or its account of why a choice was
   made. A diff alone is under-informed; the requirement and the repository are part of
   the input.
3. **Codex audits the same head separately**, under the mandate read from the **default
   branch** — never the version in the pull request, which is the case
   `LANE_POLICY` §4 makes `PROHIBITED`.
4. **Collect before publishing.** A pull-request comment is visible to both auditors, so
   publishing the first report influences the second. Both are produced, then both are
   posted.
5. **Any finding against `H` blocks the merge.**
6. **Any change to the head invalidates both reports.** They are evidence about a
   commit, not about a pull request.

## Cycles

Each remediation that produces a new head consumes one of the four review cycles in
`AGENTS.md`, and the audit is **not exempt**. Reaching the cap stops automation and
escalates to the owner.

This is expected to be the common outcome rather than a rare one, and it is not a
defect to tune away: an audit that finds something is the control working. Changing the
cap is a governance decision on measured data, not an implementation choice.

## What it cannot establish

That the change is correct; that the tests are adequate; that no vulnerability exists;
that two reports finding nothing means nothing is there. The audit raises the cost of a
defect surviving to `main`. It does not make `main` safe, and the owner's approval on a
RED change remains a judgement, not a formality.

# DEC-010 — How the autonomy gates are implemented

Status: DECIDED
Superseded in part by DEC-012 — see DEC-012 for current autonomy policy. This entry
is the historical record of the decision taken; its clauses are unchanged.
Identity separation suspended in part by DEC-013 — see DEC-013 for the current
identity state.
Supplements: DEC-009 (unchanged, not reopened). DEC-009 defines the three lanes and
the merge-gate principle; this entry fixes the questions its implementation raised
and that the files could not settle between agents.

Question: DEC-009 requires a deterministic gate rather than Claude deciding its own
work is safe, and requires the independent code-review gate to be clean on the exact
head commit. Two of its conditions turned out not to be obtainable as written, and a
third state was missing. Who computes a lane; what Codex's confirmation can mean
given what its integration actually emits; and whether a category exists that the
owner's own approval may not clear.

Options considered, and what the Council found:

A. **Who classifies.** Either Claude classifies and the gate checks disqualifiers, or
   the gate computes the lane and Claude's declaration is checked against it. The
   Strategic Council (Claude as Operator, `gpt-5.6-sol` as strategist, tier 3) reached
   the second independently on both sides: DEC-009's own requirement that the gate
   *prove* the conditions rather than rely on the builder's judgement is only met if
   the gate is the thing that computes the answer.

B. **What Codex confirms.** Codex's GitHub integration emits a review object carrying
   findings, or a comment saying it found no major issues. It emits no lane, no reason
   code, no policy version and no structured verdict of any kind. Reading its clean
   comment as agreement with a classification would convert silence into consent on
   exactly the question a second opinion was wanted for. Both Council members singled
   out that reading as the one to refuse outright.

C. **A category above RED.** Some conditions — a credential in the diff, a diff that
   is incomplete but presented as complete, an attempt to make the privileged
   evaluator execute code the pull request controls — are not made safe by an owner
   saying yes. DEC-009 had no state for them, and adding one silently would itself
   have been an agent widening governance.

Rule, in three parts.

1. **The gate is the only positive classifier.** It computes the lane from the final
   head commit, the complete diff and trusted metadata. Claude declares a proposed
   lane with its reason; the gate recomputes and a mismatch is a hard block and a
   recorded incident, never a negotiation. **No agent may promote a change to a more
   autonomous lane. Any agent may escalate one.** GREEN therefore means *pre-authorised
   by policy*, never "the model considered it low risk".

2. **Codex is a veto, not an authoriser.** Its mandate covers the correctness of the
   declared classification as well as the code, and a wrong-looking classification is
   a blocking finding. A clean Codex review is the absence of an objection and is
   never evidence that the classification was evaluated or agreed. Codex evidence that
   is missing, stale, ambiguous or unreadable blocks GREEN.

3. **`PROHIBITED` exists and owner approval does not clear it.** Such a condition is
   corrected or investigated before the work may proceed at all. The conditions are
   listed in `docs/autonomy/LANE_POLICY.md`; adding one is a change to this entry.

Also decided, and recorded here because later work depends on them: the four-cycle
review cap in `AGENTS.md` stands for now and audits are not exempt from it — changing
it is a separate governance decision on real data; the agents' operating identity is
separated from the owner's account and reduced to the permissions each role needs;
the GREEN allowlist starts empty or extremely restrictive and widens only on concrete
evidence; anything not provably GREEN is never auto-merged; AMBER requires the owner;
RED requires the owner plus the reinforced technical control; incomplete evidence
stops the process rather than defaulting to a lane; lane and readiness stay separate
outputs; Issue #7 covers the merge gate only and overnight orchestration is out of it;
and no real auto-merge happens before reliable CI, shadow mode, replay validation and
a supervised canary exist.

The reinforced technical control for RED is two audits of the same final head — Claude
in a fresh context, Codex separately, neither seeing the other's result before
producing its own, any finding on that head blocking the merge. It is **separated
defence in depth, not a guarantee of independence**: both are language models under
shared mandates and tests, and the repository must not claim otherwise. It is
available for AMBER on request.

Claude recommendation: as above. Formed as Operator before the strategist was called,
per DEC-008's independence rule.

ChatGPT recommendation: `gpt-5.6-sol` reached the same three answers independently and
held its position through cross-review (tier 3, `xhigh`, synthesis
`WEAK_CONVERGENCE`, no material disagreement).

Impact: `docs/autonomy/LANE_POLICY.md` is created as the normative classification
policy. Later changes add the deterministic gate, its offline tests, continuous
integration, the identity separation runbook and the audit protocol. No pipeline,
gazetteer, prompt or n8n behaviour changes, and no existing prompt of record is
altered. This entry has no effect until DEC-009 itself is on `main`; it is on branch
`governance/autonomy-gates` and lands in its own owner-controlled pull request, so
that the approved decision text reaches `main` unmodified by any implementation.

Blocks: nothing. It unblocks the Issue #7 implementation, which could not proceed
while these three questions were open.

A pull request that changes this entry, `docs/autonomy/LANE_POLICY.md`, the protected
surfaces or the GREEN allowlist is RED, per DEC-009.

Decided by: Owner · Date: 1 September 2026 · Affected: decisions/, docs/autonomy/,
Issue #7 specification, AGENTS.md review mandate (Codex's classification duty),
future .github/ and merge-gate work. DEC-009, DEC-104, DEC-008 and DEC-007 stand
unchanged and are referenced, not reopened.

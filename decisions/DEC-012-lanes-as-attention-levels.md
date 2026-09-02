# DEC-012 — Lanes are levels of owner attention; auto-merge is withdrawn

Status: DECIDED
Supersedes in part: DEC-009, DEC-010, DEC-011 (each unchanged and not reopened; the
clauses this entry replaces are listed below).
Identity separation suspended in part by DEC-013 — see DEC-013 for the current
identity state. Everything else in this entry stands.

Question: DEC-009 set out to let an agent merge its own work unattended in a narrow
GREEN lane, and DEC-010 and DEC-011 answered the questions that implementing it
raised. The implementation — pull request #8 — reached 3,126 added lines and nine
Codex review cycles producing 83 findings, every one verified and accepted, none
rebutted, and never a clean review on its head. Two senior architectural assessments
in fresh context, run independently and each without sight of the other's conclusions,
returned the same reading: most of that code exists to make a machine safe to merge
without the owner, and the finding rate tracked the surface rewritten in the previous
cycle rather than any residual defect density. The question this entry answers is
whether unattended merge is the right goal for this phase at all.

Options:
A. Continue the implementation as designed, closing findings cycle by cycle until a
   clean review is reached.
B. Keep unattended merge as the goal but split the work and rebuild the gate smaller,
   so each pull request is reviewable on its own.
C. **CHOSEN.** Withdraw unattended merge as a goal of this phase. The owner merges every
   pull request, and the lanes become levels of owner attention rather than of autonomy.

Claude recommendation: B, formed before the assessments below and superseded by them.
The measured evidence — the finding rate tracking the surface rewritten in the previous
cycle rather than any residual defect density — argued against A, but the recommendation
still assumed unattended merge was worth building towards.

ChatGPT recommendation: not sought at this stage. The Strategic Council was convened on
the original specification (recorded in DEC-010); this entry answers what the
implementation then demonstrated, which is a technical question rather than a strategic
one.

Senior assessment: two architectural reviews in fresh context, each without sight of the
other's conclusions or of the builder's, reached the same reading independently — that
most of the implementation existed to make a machine safe to merge without the owner,
and that the generative mechanism was the builder writing the specification, the code
and the tests. Convergence between two independent readings is evidence, not authority;
the owner decided.

Impact: `autonomy/lane_gate.js` reads git rather than an asserted snapshot and emits
facts rather than a bare lane; `docs/autonomy/LANE_POLICY.md` and
`IDENTITY_AND_PERMISSIONS.md` state that the result is advice and not a boundary;
`docs/autonomy/FINAL_AUDIT.md` is not created; `.github/workflows/checks.yml` is the
repository's first CI; `AGENTS.md` gains the classification-review duty. Issue #7 is
superseded. No pipeline, gazetteer, prompt or n8n behaviour changes, and no repository
setting is changed by the pull request that implements this.

Blocks: nothing. It unblocks the v1 implementation, which could not proceed while the
question of whether unattended merge was the goal remained open.

## Rule

**Auto-merge is not a goal of this phase. The owner performs every merge.**

The system no longer tries to prove that a pull request is safe enough to merge
without the owner. Its job is to tell the owner, quickly and from facts the pull
request did not write, how much attention that pull request needs.

**Lanes are levels of owner attention, not levels of autonomy.** Every pull request is
merged by the owner. The lane is computed by `autonomy/lane_gate.js` from the git diff
between base and head; it is a floor, not a verdict: the builder may declare a higher
lane in the pull request body, never a lower one, and the gate does not read the
declaration.

**GREEN — low attention.** No protected surface is touched; every changed path is
inside the GREEN prefix list; every file is added or modified; no new top-level path;
no unusual file kind; the change is within the size cap. GREEN says the diff can be
read quickly. It authorises nothing: the owner still merges, and only with checks
green and no open review finding.

**AMBER — read before merging.** Everything that is neither GREEN nor RED. The owner
reads the diff and the review threads before merging.

**RED — conscious decision.** At least one of: a protected surface is touched; a new
top-level path appears; a file of unusual kind (symlink, submodule, mode change);
the pull request comes from another repository. RED says
the change alters what the system is, not only what it does. The owner reads it in
full, may request a fresh-context senior assessment before deciding, and records any
new decision in `decisions/` before the merge or with it.

**Uncertainty escalates, never relaxes.** A gate that cannot compute a lane reports RED
with the reason.

**The gate is an advisor, not a control.** Its result is not a security boundary against
a hostile builder, and no lane authorises a merge. GitHub runs a `pull_request` workflow
from the pull request's own ref, so a pull request that changes the workflow can
influence the run that reports its own lane; taking the classifier from the base commit
narrows this and does not close it. **That limitation is accepted for this phase rather
than closed with a trusted external workflow or other enforcement machinery**, because
every change to `.github/**` is RED, reaches the owner, is read, and is merged by the
owner — who is the person the report is for. A report an author could tamper with is
still useful to a reader looking at the diff; it is not a gate, and nothing in this
repository may claim it is one.

**There is no machine-readable escalation.** Any agent may ask for more owner attention
in a review or a comment, and the owner may treat any pull request as RED. The
classifier does not try to represent that, so it holds no rule it cannot compute from
the diff. The GREEN prefix list and the protected-surface list live in
`autonomy/lane_gate.js`; changing either is RED.

## AUTO-GREEN — provided for, and disabled

A fourth concept exists in the architecture and has **no authorised categories**, so no
pull request can auto-merge under it. This is intentional and is not a defect of v1.

The v1 must allow AUTO-GREEN categories to be activated later by adding or changing
**only the corresponding policy** — without redesigning the RED / AMBER / GREEN lanes,
the identity model, the lane gate or the review process. To that end the gate emits
structured facts rather than a bare lane: gate version, lane, the rules that fired and
the paths that fired them, and per changed file the status, the old and new path where
relevant, source and destination modes, additions and deletions, and an explicit binary
flag; plus new top-level paths, fork provenance, and a summary of the diff. A future
AUTO-GREEN policy consumes those facts plus whatever external signals it needs.

Nothing dedicated to auto-merge is built now: no eligibility function, no privileged
collector, no readiness manifest, no atomicity machinery.

**Activating AUTO-GREEN is itself a RED change and requires a new owner decision** taken
on the evidence of pull requests actually developed under this entry — not on argument.
An adversarial review of a candidate AUTO-GREEN definition was carried out before this
entry and is retained as input to that future decision; its mitigations are deliberately
not implemented now.

## Which clauses are superseded

**DEC-009.** The decision/execution distinction, the escalation rule and the production
boundary stand. Superseded: "A GREEN change may be merged automatically"; the
merge-gate principle in so far as it requires a gate that proves conditions in order to
merge; and the operating goal of unattended merge. What survives of the merge-gate
principle is its reason: the builder does not decide that its own work is safe. Under
this entry the owner decides, and the gate only reports.

**DEC-010.** Part 1 stands in substance — the gate computes the lane and no
declaration lowers it. Part 2 stands: the reviewer is a veto, never an authoriser, and
a clean review is the absence of an objection. The four-cycle cap, the identity
separation, the restrictive GREEN list and "incomplete evidence never defaults to a
lower lane" all stand. Superseded: part 3, `PROHIBITED` as a distinct state — its
conditions are met by other means, and a category the owner's approval cannot clear has
no work to do when the owner performs every merge; the reinforced two-audit control as a
mandatory mechanism, replaced by a senior assessment the owner may request; the separate
readiness output; and the shadow-mode, replay and canary programme, which was a
precondition for auto-merge.

**DEC-011.** §1 stands: the workflow check parses YAML with `yaml@2.9.0` rather than
matching text. §2 stands: fork pull requests are refused in v1 and classified RED; its
reconsideration trigger stands. §3's rule stands — reaching four cycles means autonomy
stops and the owner intervenes — but its mechanism is superseded: no gate reads owner
comments for an exception naming a head. The cap is a process rule in `AGENTS.md`, kept
by the builder and visible to the owner in the pull request timeline.

DEC-104, DEC-008 and DEC-007 stand unchanged and are referenced, not reopened.

## The four-cycle rule

Unchanged in meaning and removed from the gate. After four review cycles without
convergence the builder stops and says so, because at that point the likely cause is
larger than a list of bugs: over-complexity, an unstable specification, or a technical
approach that needs revisiting. It does not mean a pull request is ready after four
cycles. The owner then routes the work — a senior design assessment, a redesign, or
closing it.

Pull request #8 is the worked example. Stopping at cycle five was right; granting the
exception was the mistake, and it cost five further cycles that produced valid findings
without approaching a clean review.

## Record of what pull request #8 established

Kept here because closing a pull request discards its threads, and `AGENTS.md` requires
the lesson to survive in `reviews/` or a decision entry.

Findings per cycle: 15, 13, 8, 14, 9, 7, 4, 7, 6. The first build was roughly 1,570
added lines; the remaining 1,556 were the response to review. The reviewed surface grew
from 798 to 3,126 lines and never shrank. From cycle 6 onward, 16 of 24 findings landed
in a 388-line suite guarding an 86-line workflow, rewritten three times. Four defects
were in the tests themselves, including a fixture that placed one audit record under
both keys while asserting that two distinct ones were required.

The generative mechanism, stated so it is recognisable next time: the builder wrote the
specification, the code and the tests, and the reviewer's mandate is to compare code to
the specification — so every sentence added to the policy to record a fix became the
citation for the next finding. The newest code carried the defects.

Not a defect of the review loop: 83 valid findings on 3,126 lines is the loop working.
The defect was continuing to grow the artefact instead of stopping to ask whether it
was the right artefact.

## Amended after the review-cycle cap

The four-cycle cap was reached on the pull request implementing this entry, and the
owner intervened, which is what the cap is for. The three clauses above about the gate
being an advisor, the accepted workflow limitation and the absence of machine-readable
escalation are that intervention: an owner decision taken after the cap, not a
continuation of the builder's own loop.

The claim that the builder does not have "the ability to change the workflow that
classifies it" is withdrawn from `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`. It was not
true, and the owner decided not to build the infrastructure that would make it true.

## The v1 GREEN baseline

A final audit of the merged state asked what DEC-010's "starts empty or extremely
restrictive" amounts to in practice, since nothing recorded the answer. It does now, by
owner decision: **v1 starts with the GREEN prefixes `docs/` and `reviews/`**, subject to
the protected surfaces and control filenames, which are evaluated first and win. This is
the approved baseline, not a widening of DEC-010's clause and not a step towards
AUTO-GREEN, whose category list stays empty. **Any widening of the prefixes is RED and
requires a new owner decision.**

The same audit found that the older autonomy entries carried no sign of having been
superseded, and that three files the repository treats as authority — the first and third
items of the reading order in `docs/START_HERE.md`, and the review folder's own rules —
were inside a GREEN prefix without being protected. Both are corrected without touching a
historical clause: the superseded entries gain a pointer under `Status:`, and the three
files join the protected list.

Decided by: Owner · Date: 1-2 September 2026 · Affected: `decisions/`, `docs/autonomy/`,
`autonomy/lane_gate.js`, `.github/`, `tests/`, `AGENTS.md`, Issue #7 (whose acceptance
criteria are auto-merge criteria and which this entry supersedes), pull request #8
(closed unmerged, branch retained).

# Lane policy — how a pull request is classified

The normative classification policy for the autonomy gates. DEC-009 defines the three
lanes and forbids weakening the independent review to obtain auto-merge; DEC-010 fixes
who computes a lane, what Codex's review can mean, and the category that owner approval
does not clear. This file states the rules a machine applies; it does not restate the
decisions, and where it and a DEC entry disagree, the DEC entry wins.

**Scope.** This policy governs changes to this repository. It says nothing about n8n,
credentials, external paid services or GitHub administration: those are governed
separately and DEC-009's production boundary is unchanged. A merge into `main` deploys
nothing and never authorises an operational action.

**Changing this file is RED.** So is changing the protected surfaces or the GREEN
allowlist below.

## 1. Two outputs, never one

Every evaluation produces **a lane** and **a readiness**, and they are different kinds
of fact.

- The **lane** is policy: who may merge this change, and under what assurance. It is a
  property of the diff and the authorisation, and it is durable.
- **Readiness** is transient: whether the evidence needed right now is present and
  current. Pending checks, a missing review, a rate-limited API, a merge conflict, a
  base that has moved.

A readiness failure **blocks and is retried. It never changes the lane.** Conflating
them is what makes an unattended loop stop on latency as though it had hit a policy
wall, and it is the single most common way a gate of this kind goes wrong.

## 2. Evaluation order

Computed in this order, on the final head commit. The first state that applies wins,
and a later condition can never lower an earlier one.

1. **`PROHIBITED`** — a condition that owner approval does not clear (§4).
2. **`UNCLASSIFIED`** — classification could not be performed (§5).
3. **`RED`** — a protected surface is touched, or an agent escalated to RED (§6).
4. **`GREEN`** — the whole pull request satisfies every predicate of exactly one
   approved allowlist category (§7).
5. **`AMBER`** — everything else.

AMBER is the residue, not a judgement. Nothing has to decide whether a change is
"significant": if it is not provably GREEN and not RED, it is AMBER, and AMBER means
the owner merges it.

| Lane | Who merges | Assurance |
|---|---|---|
| GREEN | the gate, automatically | required checks, clean review, allowlist predicates |
| AMBER | the owner | required checks, clean review |
| RED | the owner | the above plus the reinforced control (§9) |

## 3. Who may move a lane

- **The gate computes the lane.** It is the only positive classifier.
- **Claude declares** a proposed lane and a reason. The declaration is planning
  metadata and an audit trail: the gate recomputes from the final diff regardless, and
  a declaration that disagrees with the computed lane is a **hard block and a recorded
  incident**. A declaration made before development is never carried forward; the final
  diff is classified from scratch.
- **No agent may promote.** Neither Claude nor Codex can move a change to a more
  autonomous lane, and no sequence of agent statements can produce GREEN.
- **Any agent may escalate**, and an escalation is sticky: it cannot be undone by the
  agent that raised it or by any other agent. Only the owner clears it.

GREEN means *pre-authorised by this policy*. It never means that a model considered the
change small, safe or low-risk.

## 4. `PROHIBITED`

Not a lane. The work does not proceed — in any lane, with or without approval — until
the condition is corrected or investigated. Owner approval does not clear it, which is
why the list is short, mechanical, and changed only by a decision entry.

- A credential, private key or token appears in the diff.
- The changed-file set is incomplete but was presented as complete — truncated
  pagination, a partial API response, an enumeration that failed silently.
- The change would cause the privileged evaluator to execute, import or otherwise
  consume code, workflow definitions or artefacts the pull request controls.
- The pull request modifies the review mandate, the gate, or the policy under which it
  is itself being evaluated **and** that modified version would be the one applied.

The last one is the self-referential case: a pull request touching
`reviews/REVIEW_MANDATE_CODE.md`, `AGENTS.md` or this file is reviewed and classified
under the **default branch** version, never its own. If the evaluator cannot demonstrate
that it used the default-branch version, the state is `PROHIBITED`, not RED.

## 5. `UNCLASSIFIED`

Classification did not happen, so no lane is asserted. This is **not** AMBER: AMBER
means the owner approves the change, and an owner cannot approve a diff that was never
fully enumerated, nor rule out a RED trigger inside the part that was not read.

Reached when the diff, the metadata or the required evidence is incomplete or
untrustworthy — a truncated file list, an unavailable API, an unresolvable commit
reference, a check-run set that could not be read, or evidence computed under a policy
version other than the current one.

`UNCLASSIFIED` blocks and is retried; if it persists, it escalates to the owner as a
fault, not as a change awaiting approval.

## 6. Protected surfaces — always RED

Evaluated against **both the old and the new path** of every change, so a protected file
cannot become GREEN by being renamed, and against the resolved target of any symlink.

- `.github/**` — workflows, actions, CODEOWNERS, any configuration that runs with
  repository credentials.
- The merge gate's source, its tests, the required-check manifest, the GREEN allowlist,
  and this file.
- `decisions/**`, `AGENTS.md`, `CLAUDE.md`, `reviews/REVIEW_MANDATE_CODE.md` — the
  governance and review machinery.
- `prompts/**`, `docs/REVIEW_QUEUE.md`, `venue-registry/venues.json`, `gazetteer/**` —
  the normative hierarchy of `AGENTS.md`, including the workbook and every generated
  artefact.
- `workflows/**`, `code-nodes/**` — what runs, or is certified to run, in production.
- `council/**` — the Strategic Council tool (DEC-008).
- `requirements.txt` and any dependency manifest or lockfile.
- `.gitignore` — it can hide a file from every rule above.

Anything not classified by this list and not inside an approved GREEN category is AMBER.
A **new top-level path** is never GREEN: unknown surfaces fail closed.

## 7. The GREEN allowlist

**The allowlist is empty.** No category is approved, so no pull request can currently be
GREEN, and that is the intended state until evidence exists.

A category is added only by owner decision, and only after historical replay,
shadow-mode classification and adversarial fixtures show it holds. Each category names:
its path predicates; its structural invariants and the validator that checks them; its
magnitude limits; and whether it may be combined with another category.

Rules that hold for every category:

- **The whole pull request must satisfy one single category.** Per-file rules that each
  pass do not make a pull request GREEN: a change can satisfy every file-level predicate
  and still break an invariant that spans files.
- **Categories do not combine.** Two approved categories in one pull request are not an
  approved category unless that exact combination has been approved.
- Fail closed on renames, case-only changes, symlinks, submodules, mode and
  executable-bit changes, binary or unparseable content, and any file the validator
  cannot read.
- The pull request originates in this repository, not a fork; it targets the default
  branch; its author is the automation identity.
- It links one owner-authorised task, and that authorisation cannot be created or
  altered by the pull request being evaluated.

**Magnitude limits are policy, not fact.** File and line counts are measurable exactly;
which count is *safe* is a judgement the owner makes when approving the category.

## 8. What this policy does not prove

Stated here so that no later document implies otherwise. The criteria establish that a
pull request lies **inside an authorised perimeter**. They do not establish that the
change is intrinsically low-risk, and no addition to them would.

Not determinable from a diff: whether a change alters behaviour; whether an
ordinary-looking edit has architectural or security consequences; whether prose is a
typo or a policy change; whether data is factually correct or safe to publish; whether
tests cover what changed; the absence of a vulnerability; whether a linked task honestly
describes the diff; whether successive changes are slicing one large change into small
ones; whether repository state still matches production.

Two consequences the gate cannot absorb, and which stay with the owner:

- **Cumulative drift.** Individually GREEN changes can accumulate into exactly the
  change that would have been called significant if presented at once. No per-pull-request
  rule can see this. Each approved category is reviewed periodically for what it has
  actually admitted.
- **Correlated blindness.** Claude and Codex are language models under shared mandates
  and shared tests. Their agreement is evidence, never authority (DEC-008), and it is an
  argument for a narrow allowlist rather than for trusting the pair.

## 9. Evidence, and what invalidates it

Three commits, and they are not interchangeable: **`H`**, the head that was reviewed and
directly tested; **`B`**, the base against which compatibility was established; **`M`**,
the merge result GitHub generates. `M` is never `H`. A requirement that the gate evaluate
"the commit that will be merged" cannot be satisfied and must not be written.

- Review and head checks bind to `H`. Compatibility evidence binds to `H+B`.
- Every artefact records `H` in full, `B`, and the policy version under which it was
  computed. An abbreviated commit reference is resolved to a unique full SHA or it is
  not evidence.
- A push invalidates everything. A base movement invalidates compatibility evidence.
- A clean review must be the latest completed review for `H` **and** later than the
  most recent review request; a finding on `H`, or an unanswered request, blocks.
  Findings on an earlier head are superseded by a clean review of `H` — the builder
  never resolves its own threads to clear a signal.
- Evidence carried in mutable places — a pull request body, a comment, a thread state —
  is re-read and re-bound at decision time, never trusted from an earlier read.
- Merging must be atomic with the evidence: strict enforcement that `B` is current, or a
  merge queue. **Without one of these, no lane auto-merges.**

## 10. The reinforced control (RED)

Mandatory for RED, available for AMBER when the owner asks.

1. Claude audits the final head in a **fresh context** — given the authorised
   requirement, the repository and the diff, and not the builder's conclusions.
2. Codex audits the same head separately.
3. Both use mandates read from the **default branch**, never from the pull request.
4. **Neither sees the other's result before producing its own.** Because a pull request
   comment is visible to both, the reports are collected and only then published.
5. Any finding against that head blocks the merge.
6. Any change to the head invalidates both reports.

It is **separated defence in depth, not independence**. A fresh context removes the
builder's anchoring — the things it convinced itself were fine while writing them — and
removes nothing of the shared-model correlation. The word "independent" is not used for
it anywhere.

## 11. Cycles, stopping and the kill switch

- The four-cycle cap in `AGENTS.md` applies, and **audits are not exempt**. Every
  remediation that produces a new head consumes a cycle.
- At the cap, automation stops and the work escalates to the owner. Reaching the cap is
  a normal outcome, not a failure to route around.
- Under this cap most autonomous work escalates rather than merges. That is the
  intended behaviour and not a defect to be tuned away; changing the cap is a governance
  decision on measured data.
- A kill switch disables auto-merge immediately. It is readable by the gate before any
  other evaluation, it fails closed when it cannot be read, and it is **not** writable by
  the automation identity — a control the automation can clear is not a control.

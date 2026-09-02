# DEC-013 — The technical identity separation is suspended; owner merge returns to a process rule

Status: DECIDED
Supersedes in part: DEC-010 and DEC-012 (each unchanged and not reopened; the clauses
this entry suspends are listed below).

Question: DEC-010 decided that the agents' operating identity is separated from the
owner's account, and DEC-012 restated that the separation stands. It was then built and
tested: a builder account `QN-Builder` was created, given write access, and used to open
a pull request the owner merged. It bought a real approval gate — see below for its exact
bound. It also turned out to cost more per cycle than the phase can spend — the review integration is authorised per requesting
GitHub account, so the builder could not obtain the code review its own pull requests
need. The question this entry answers is whether a separate builder account is worth its
operating cost in this phase.

Options:
A. Keep the separation and pay the cost — connect a review account for `QN-Builder`, so
   the builder can request its own reviews.
B. **CHOSEN.** Suspend the technical separation for this phase. One account operates the
   repository; the conceptual division of builder, reviewer and owner stands, and the
   owner still performs every merge, as the process rule it has always been.
C. Abandon identity separation as a principle.

Claude recommendation: none sought. The owner took this decision on the operating
evidence below; the builder's part was to run the test and report what it cost.

ChatGPT recommendation: not sought. This is an operating-cost decision for the phase,
not a strategic or technical question of the kind DEC-008 routes to the Council.

Impact: `docs/autonomy/IDENTITY_AND_PERMISSIONS.md` is rewritten to describe the state
that exists rather than the state that was planned. No decision entry is rewritten; the
two this suspends gain a pointer. No change to `autonomy/lane_gate.js`, to
`.github/workflows/**`, to the lane rules, the size caps, the GREEN prefixes, the
protected surfaces, or AUTO-GREEN. `AGENTS.md` is unchanged: its role division is
conceptual and this entry does not touch it. No pipeline, gazetteer, prompt or n8n
behaviour changes.

Blocks: nothing.

## Rule

**The separation of the agents' GitHub identity from the owner's is suspended for this
phase, and is not withdrawn as a principle.** It is future hardening, to be taken up
again when the phase can absorb its cost — not a requirement the current state fails to
meet.

**The owner performs every merge. This is a process rule and not a guarantee — it never
was one.** One account holds owner permissions and the agent operates through it, so
GitHub cannot tell them apart and cannot withhold a merge from the agent. What prevents
an agent merge is that the agent is not authorised to merge, and nothing else. Under the
separation the platform withheld an *unapproved* merge and no more, so what is lost with
it is the approval gate, not an owner-only merge that was never enforced.

That distinction is the whole content of this entry, and the repository states it in one
form everywhere: **no file may describe owner merge as enforced while the identities are
shared.** DEC-012 already withdrew one claim of a control that did not exist; this is the
same class of error and is not to be repeated in the other direction.

## What is suspended

- **DEC-010**, in the clause "the agents' operating identity is separated from the
  owner's account and reduced to the permissions each role needs". The reduction of the
  *reviewer* app to review-only permissions is unaffected by this entry and remains
  outstanding.
- **DEC-012**, in so far as it lists the identity separation among the DEC-010 clauses
  that stand. Everything else DEC-012 decided is untouched — lanes as levels of owner
  attention, the gate as an advisor, the four-cycle cap, the v1 GREEN baseline, and
  AUTO-GREEN provided for and disabled.

  One consequence of that entry needs saying rather than leaving implied. DEC-012
  promises that an AUTO-GREEN category can be activated later by changing **only the
  corresponding policy**, without redesigning the identity model. The design is not
  redesigned here, only its implementation suspended — but a policy alone cannot
  activate anything while the account that would merge under it is the owner's.
  **Restoring the identity separation is therefore a precondition of any future
  AUTO-GREEN decision**, which DEC-012 already requires to be RED and taken on evidence.
- The requirement of one approving review, which existed to make owner *approval* a
  platform rule. With a single account it cannot do that: GitHub forbids approving one's
  own pull request, and with owner and builder on the same account the rule blocks every
  pull request opened through that account whichever conceptual role opened it, unless a
  distinct eligible identity approves it — and while one account holds both roles there
  is none. Required approving reviews are **0** in the current ruleset.

## What is unchanged

Every guardrail that does not depend on two accounts:

- a pull request is required; no direct push to the default branch;
- `suites` and `lane` are required checks;
- the branch must be up to date with `main` before merging;
- conversation resolution is required;
- `merge` is the only permitted merge method;
- force push to the default branch is blocked;
- the ruleset bypass list is empty;
- RED / AMBER / GREEN remain levels of owner attention (DEC-012);
- four review cycles without convergence stops the work (DEC-012);
- the reviewer is a veto, not an authoriser (DEC-010 part 2);
- the reviewer never authors a change (`AGENTS.md`, DEC-104);
- AUTO-GREEN has no authorised categories and nothing can auto-merge (DEC-012);
- the owner decides and merges (DEC-104, `AGENTS.md`).

The ruleset state above is the owner's record of the settings as configured on the date
of this entry. No agent reads or changes a repository setting, and the entry does not
claim to have verified it.

## What the test established, and why it was still withdrawn

Recorded because the evidence cost two pull requests to obtain and would otherwise be
lost with their threads.

**The approval gate holds against the builder.** `QN-Builder` was created, given write
access, and opened pull request #12 from the branch of the closed #11. Before any owner
approval it attempted one merge and GitHub refused it:

```
PUT /repos/QuartieriNews/QN/pulls/12/merge → 405
Repository rule violations found
At least 1 approving review is required by reviewers with write access.
```

**What that shows is bounded, and the bound matters.** The builder could not merge its
own *unapproved* pull request. It does not show that the owner had to perform the merge:
`QN-Builder` held write access, and the rule that fired requires an approving review, not
an owner-executed merge — so after the owner approved, nothing tested here would have
stopped the builder from merging. The owner merged #12 as `c15a6b8` under the process
rule, not because GitHub would have refused a second attempt.

DEC-010 listed "merge to the default branch" among what the builder must not have, and
`docs/autonomy/IDENTITY_AND_PERMISSIONS.md` claimed the approving-review requirement
would make owner merge "a platform rule rather than a habit". Neither is what was
verified, and GitHub has no merge-only permission to withhold from an identity that must
still push its own branch. **Owner-executed merge was a process rule under the separation
too**; what the separation buys is the approval gate, which is real and which one shared
account cannot have.

**Two costs made it not worth keeping in this phase.** First, the review integration
authorises per requesting GitHub account: `@codex review` from `QN-Builder` returned a
prompt to connect an account rather than a review, so the builder could not obtain the
review its own pull requests require, and the verdict had to be requested from the owner
identity — which is the separation leaking back. Second, the approval requirement that
gave the separation its value also blocks the owner's own pull requests, so with one
account the repository could not merge at all until the requirement was removed.

**Getting there also cost a pull request to nothing.** #11 carried the same head, the
same diff and a clean review, and was closed unmerged only because the owner account
cannot approve its own pull request. The head was reopened as #12 with no commit
rewritten. Nothing was lost, and the sequence is the worked example of what the
separation costs to operate.

Decided by: Owner · Date: 2 September 2026 · Affected: `decisions/DEC-010`,
`decisions/DEC-012` (pointers only), `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`, the
`main` ruleset, pull requests #11 (closed unmerged) and #12 (merged as `c15a6b8`), and
the `QN-Builder` account (write access removed). DEC-104, DEC-009, DEC-011, DEC-008 and
DEC-007 stand unchanged and are referenced, not reopened.

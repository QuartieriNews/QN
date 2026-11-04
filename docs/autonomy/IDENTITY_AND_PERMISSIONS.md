# Identity and permissions

The controls in this file are the ones that actually constrain an agent. The lane gate
is advice; GitHub is enforcement. Everything here is the owner's to do — no agent
changes a repository setting.

## The state as it is

Three identities act on this repository. Which account each one writes under is the fact
the rest of this file depends on, so it is stated as a table rather than as prose that
has to quantify over all of them:

| Acts as | Writes under | GitHub sees |
|---|---|---|
| **Owner** | the owner's account | `author_association: OWNER` |
| **Builder** | the machine account `QN-Builder`, through the Claude app (DEC-029) | `author_association: COLLABORATOR` — distinguishable from the owner |
| **Reviewer** | the reviewer app's own identity | `author_association: NONE` — distinguishable |

The builder row is the one that changed. Until 4 November 2026 the builder wrote under the
owner's account, with the owner's credentials, so anything it wrote was recorded as the
owner writing it and it could not produce evidence *about* the owner — an authorisation,
an approval. Since DEC-029 it writes as `QN-Builder`; the check of that is recorded below.
The reviewer row is why a review finding is distinguishable from an owner comment at all.

Before DEC-029 the history held one exception to the old builder row, the test recorded
below: `QN-Builder` opened pull request #12 and commented on it under its own identity.
Its write access was withdrawn after that test and given back for DEC-029.

**"The owner merges" is a process rule, not a control.** Once all enforced repository
requirements are satisfied, GitHub does not stop the builder from merging: before DEC-029
because builder and owner acted through the same account, since DEC-029 because
`QN-Builder` holds write access and no rule requires an approving review. The
owner-executed merge rule is a process rule, not an identity-based platform control. The
builder is not authorised to merge, and that is what the rule rests on (DEC-013; DEC-029,
point 3).

**Required approving reviews are 0.** The requirement made owner *approval* a platform
rule, which it can do only with two identities. In the tested workflow, pull requests
opened through the shared account could not satisfy it: the author cannot approve its own
pull request, and the reviewer workflow did not supply an approving review — Codex is a
veto and a reviewer, not an authoriser (DEC-013).

## What GitHub enforces today

The `main` ruleset is the owner's record, and DEC-013 holds it: what is enforced and what
is only a process rule, verified against the live ruleset on 2 September 2026. It is not
restated here — the configuration is owner-controlled, and a second copy of that list
could only go stale.

Two properties of it belong in front of any reader of this file:

- **A bypass actor voids every enforced row.** DEC-013 records the bypass list as empty.
- **The owner performing the merge is not enforced**, and neither is the review-cycle
  cap. Both are process rules, kept by the builder and visible to the owner in the pull
  request timeline.

## The builder can change the workflow that classifies it, and in v1 that is accepted

GitHub runs a `pull_request` workflow from the pull request's own ref, so a pull request
touching `.github/**` influences the run that reports its own lane. This file once
claimed the opposite; the claim was false and is withdrawn. The owner decided not to
build a trusted external workflow to make it true (DEC-012). What stands in its place is
not machinery: a change to `.github/**` is RED, the owner reads it, and the owner merges
it. **The lane result is advice to the owner, never a boundary against the builder.**

## What the identity test established, and what it did not

A builder account, `QN-Builder`, was created and given write access. It opened pull
request #12 and, before any approval, attempted one merge to `main`. GitHub refused it:

```
PUT /repos/QuartieriNews/QN/pulls/12/merge → 405
Repository rule violations found
At least 1 approving review is required by reviewers with write access.
```

**What that establishes: the approval gate holds against the builder.** It could not
merge its own unapproved pull request, and the reason GitHub gave is the missing
approving review.

**What it does not establish: that the owner had to perform the merge.** `QN-Builder`
held write access, and the rule that fired requires an approving review — not an
owner-executed merge. Once the owner had approved, nothing tested here would have
stopped the builder from merging. The owner merged #12 as `c15a6b8` because that is the
process rule, not because the configuration under test would have refused the builder a
second time.

The distinction matters because this file used to promise the opposite: that requiring
one approving review "makes owner merge a platform rule rather than a habit". It makes
owner *approval* a platform rule. **Owner-executed merge was not enforced by the
configuration that was tested**, and this file claims nothing about configurations that
were not. DEC-010 listed "merge to the default branch" among what the builder must not
have; what the test verified is the approval gate, not that clause.

## The check of 4 November 2026 (DEC-029, point 5)

Pull request #22, the first after the switch, was opened by the builder session of 4
November 2026 through the REST API. What GitHub records, read back through the same API:

| What | GitHub shows |
|---|---|
| Author of pull request #22 | `QN-Builder`, `author_association: COLLABORATOR` |
| App the pull request was written through | `performed_via_github_app`: `claude`, owner `anthropics` |
| Push that created `ops/github-protocollo` (13:27:18 UTC) | actor `QN-Builder`, `branch_creation` |
| Permissions of the session's credential on QN | `pull`, `triage`, `push`; no `maintain`, no `admin` |
| The eight commits of the pull request | author and committer `claude` (`noreply@anthropic.com`), signature `verified: true` |

**What that shows.** The two writes of that session, the push and the pull request, reach
GitHub as `QN-Builder` through the Claude app, distinguishable from the owner. The
credential behind them has no admin role, so it is not the owner's (DEC-029, points 1
and 3).

**What it does not show.**
- **Who wrote the commits.** Author and committer are written by the client, and GitHub
  links them to the account that owns the address, here `claude`: neither `QN-Builder`
  nor the owner. The valid signature belongs to that identity. Who pushed the commits is
  the push row, not the commit.
- **That every agent write goes through `QN-Builder`.** The check covers one session's
  push and pull request. Comments, replies and review requests had not been made yet,
  and the other client that wrote on GitHub before, the weekly watch job through the
  ChatGPT/Codex connector, was not checked.
- **That the review integration accepts `@codex review` from `QN-Builder`.** Not tried:
  the first review of #22 starts when it is marked ready for review, without a request.
- **That `QN-Builder` cannot merge.** Not tried, and not to be tried. With write access
  and no required approving review, nothing checked here would stop it; the owner's merge
  stays a process rule (DEC-029, point 3).

## Why the separation was withdrawn

Not because it failed. The review integration authorises per requesting GitHub account,
so `@codex review` from `QN-Builder` returned a prompt to connect an account rather than
a review: the builder could not obtain the review its own pull requests require, and the
verdict had to come from the owner identity. Getting there also cost pull request #11,
closed unmerged with a clean review on the same head, only because the owner account
cannot approve its own pull request.

## Future hardening — not a requirement of this phase

Separating the identities is deferred rather than dropped (DEC-013). It becomes worth
doing when the phase can absorb a second account's review setup. What it would need,
when it is taken up again:

| Identity | Needs | Must not have |
|---|---|---|
| **Owner** | everything, including a ruleset bypass if the owner keeps one as an emergency valve | to be reachable from an unattended session: these credentials must never be in an agent's environment |
| **Builder** | push to non-default branches; open and update pull requests; read checks | merge to the default branch; ruleset bypass; admin |
| **Reviewer** | read the repository; post reviews and comments | `contents: write`, which the installed app holds and which reviewing does not need |

The builder row is an intent, and GitHub expresses only part of it. There is no
path-scoped write, so a builder can always *propose* a change to a protected file on its
own branch — that is fine. What the configuration under test enforced is that the builder
could not merge an **unapproved** pull request and could not bypass the rules. It did not
stop the builder from merging an approved one; whether another configuration would is
untested and is not claimed here.

So restoring the separation buys back the approval gate — an approving review the builder
cannot supply for itself — and restores the value of the approving-review requirement,
which the tested workflow could not satisfy from a shared account. Owner-*executed* merge
is a separate question: the configuration that was tested did not enforce it, and nothing here
designs one that would.

Two things remain outstanding whenever it is resumed: a builder identity with a review
account of its own — a GitHub App is preferable to a machine account, for scoped
permissions, auditable installation and revocation on its own — and restoring the
approving-review requirement. **Reducing the reviewer app to review-only permissions does
not depend on any of this and is still outstanding.**

An unverified control is not a control: whenever the separation is restored, verify it
the way it was verified above, and record what the result does and does not show.

## Not here

Merge queues and AUTO-GREEN activation belong to a future AUTO-GREEN decision, not to
this phase: they exist to make a merge atomic with its evidence, and nothing merges
without the owner reading it (DEC-012). Any such decision has the identity separation as
a precondition (DEC-013).

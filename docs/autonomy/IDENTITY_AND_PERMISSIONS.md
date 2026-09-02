# Identity and permissions

The controls in this file are the ones that actually constrain an agent. The lane gate
is advice; GitHub is enforcement. Everything here is the owner's to do — no agent
changes a repository setting.

## The state as it is

One GitHub account, the owner's, operates this repository. Every commit, pull request,
comment and merge in its history was made under that account, so GitHub cannot tell the
owner and the agent apart: every agent comment carries `author_association: OWNER`.

**"The owner merges" is therefore a process rule, not a control.** The agent holds the
owner's credentials and is technically able to merge; what stops it is that it is not
authorised to, and nothing else. A separated builder identity was built and tested and
then withdrawn — see below — so this is the state by decision (DEC-013), not by omission.

The same shape has a consequence worth stating plainly: an agent cannot produce evidence
*about* the owner — an authorisation, an approval — because anything it writes is
recorded as the owner writing it.

**Required approving reviews are 0.** The requirement existed only to make owner merge a
platform rule, which it can do only with two identities: GitHub forbids approving one's
own pull request, so with a single account it blocked the owner's pull requests instead
of the agent's (DEC-013).

## What GitHub enforces today

The owner's record of the `main` ruleset as configured on 2 September 2026. No agent
reads or writes a repository setting, so this list is the owner's statement of it and
not a verified reading:

| Enforced | |
|---|---|
| a pull request is required | no direct push to `main` |
| `suites` and `lane` | required checks |
| branch up to date with `main` | before merging |
| conversation resolution | required |
| `merge` | the only permitted merge method |
| force push to `main` | blocked |
| bypass list | empty |

**A bypass actor voids every row above.** The list is empty, and the owner's own bypass
is the emergency valve, subject to the credential rule in the table further down.

What is *not* enforced, and is a process rule instead: that the owner performs the
merge, and the review cycle cap. Both are kept by the builder and visible to the owner in
the pull request timeline.

## The builder can change the workflow that classifies it, and in v1 that is accepted

GitHub runs a `pull_request` workflow from the pull request's own ref, so a pull request
touching `.github/**` influences the run that reports its own lane. This file once
claimed the opposite; the claim was false and is withdrawn. The owner decided not to
build a trusted external workflow to make it true (DEC-012). What stands in its place is
not machinery: a change to `.github/**` is RED, the owner reads it, and the owner merges
it. **The lane result is advice to the owner, never a boundary against the builder.**

## The separation was built, tested and withdrawn

Recorded because it is the answer to the verification this file used to ask for, and
because the cost is the reason it is not in force.

A builder account, `QN-Builder`, was created and given write access. It opened pull
request #12 and, before any owner approval, attempted one merge to `main`. GitHub
refused it:

```
PUT /repos/QuartieriNews/QN/pulls/12/merge → 405
Repository rule violations found
At least 1 approving review is required by reviewers with write access.
```

That is the verification: a builder identity attempting one merge to the default branch,
and failing. The owner then merged #12 as `c15a6b8`. **The technical separation works.**

It was withdrawn for operating cost, not because it failed. The review integration
authorises per requesting GitHub account, so `@codex review` from `QN-Builder` returned a
prompt to connect an account rather than a review: the builder could not obtain the
review its own pull requests require, and the verdict had to come from the owner
identity. Getting there also cost pull request #11, closed unmerged with a clean review
on the same head, only because the owner account cannot approve its own pull request.
`QN-Builder` no longer has write access to this repository.

## Future hardening — not a requirement of this phase

Separating the identities is the way to make owner merge enforceable, and it is deferred
rather than dropped (DEC-013). It becomes worth doing when the phase can absorb a second
account's review setup. What it would need, when it is taken up again:

| Identity | Needs | Must not have |
|---|---|---|
| **Owner** | everything, including ruleset bypass as the emergency valve | to be reachable from an unattended session: these credentials must never be in an agent's environment |
| **Builder** | push to non-default branches; open and update pull requests; read checks | merge to the default branch; ruleset bypass; admin |
| **Reviewer** | read the repository; post reviews and comments | `contents: write`, which the installed app holds and which reviewing does not need |

GitHub offers no path-scoped write, so a builder can always *propose* a change to a
protected file on its own branch. That is fine. The enforceable controls are that it
cannot merge it and cannot bypass the rules.

Two things remain outstanding whenever it is resumed: a builder identity with a review
account of its own — a GitHub App is preferable to a machine account, for scoped
permissions, auditable installation and revocation on its own — and restoring the
approving-review requirement, which only has an effect once the builder is a second
identity. **Reducing the reviewer app to review-only permissions does not depend on any
of this and is still outstanding.**

An unverified control is not a control: whenever the separation is restored, verify it
the way it was verified above.

## Not here

Merge queues and AUTO-GREEN activation belong to a future AUTO-GREEN decision, not to
this phase: they exist to make a merge atomic with its evidence, and nothing merges
without the owner reading it (DEC-012).

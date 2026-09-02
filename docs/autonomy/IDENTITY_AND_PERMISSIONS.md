# Identity and permissions

The controls in this file are the ones that actually constrain an agent. The lane gate
is advice; GitHub is enforcement. Everything here is the owner's to do — no agent
changes a repository setting.

## The state that makes the rest necessary

Every commit, pull request, comment and merge in this repository's history was made
under the owner's single GitHub account. The builder acts with the owner's credentials,
so GitHub cannot presently tell the owner and the agent apart: every agent comment
carries `author_association: OWNER`. **"The owner merges" is therefore a convention, not
a control, until the identities are separated.**

This has a consequence worth stating plainly: an agent cannot produce evidence *about*
the owner — an authorisation, an approval — because anything it writes is recorded as
the owner writing it.

## What each identity needs

| Identity | Needs | Must not have |
|---|---|---|
| **Owner** | everything, including ruleset bypass as the emergency valve | to be reachable from an unattended session: these credentials must never be in an agent's environment |
| **Builder** | push to non-default branches; open and update pull requests; read checks | merge to the default branch; ruleset bypass; admin |
| **Reviewer** | read the repository; post reviews and comments | `contents: write`, which the installed app holds and which reviewing does not need |

GitHub offers no path-scoped write, so the builder can always *propose* a change to a
protected file on its own branch. That is fine. The enforceable controls are that it
cannot merge it and cannot bypass the rules.

**The builder can change the workflow that classifies it, and in v1 that is accepted.**
GitHub runs a `pull_request` workflow from the pull request's own ref, so a pull request
touching `.github/**` influences the run that reports its own lane. This file previously
claimed the opposite; the claim was false and is withdrawn. The owner decided not to
build a trusted external workflow to make it true (DEC-012). What stands in its place is
not machinery: a change to `.github/**` is RED, the owner reads it, and the owner merges
it. **The lane result is advice to the owner, never a boundary against the builder.**

## The changes, in order

1. **Create a builder identity** — a GitHub App is preferable to a machine account:
   scoped permissions, auditable installation, revocable on its own.
2. **Remove the bypass actor.** The `main-pr-only` ruleset holds a `RepositoryRole` with
   permanent bypass. **A bypass actor voids every row above.** Keep the owner's own
   bypass, subject to the credential rule.
3. **Require one approving review.** GitHub forbids approving one's own pull request, so
   with the builder on its own identity this makes owner merge a platform rule rather
   than a habit. This is the single highest-value change here.
4. **Require the `suites` and `lane` checks.** CI existing is not CI being required.
5. **Reduce the reviewer app to review-only permissions.**

Verify by having the builder identity attempt one merge to the default branch. It must
fail. An unverified control is not a control.

## Not here

Merge queues, up-to-date-branch enforcement, a single merge method and auto-merge
activation belong to a future AUTO-GREEN decision, not to this phase: they exist to make
a merge atomic with its evidence, and nothing merges without the owner reading it
(DEC-012).

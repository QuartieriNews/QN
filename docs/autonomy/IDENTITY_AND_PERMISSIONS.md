# Identity, permissions and the ruleset

What must be true of GitHub before any lane can auto-merge. The rules are DEC-009 and
DEC-010; this is the runbook that makes them enforceable rather than promised.

**None of it is configured yet, and the gate assumes none of it.** Until the checks in
§4 pass, `mergeAtomicity` is not `strict_base` or `merge_queue`, so `autoMergeAllowed`
is false for every input regardless of everything else.

## 1. Why identity comes first

Every commit, pull request, comment and merge in this repository's history was authored
by the owner's account. An agent acting on GitHub was therefore indistinguishable from
the owner, and GitHub recorded no difference between the two after the fact.

That makes "AMBER and RED are merged only by the owner" a convention the agent is
trusted to honour rather than a control the platform enforces — and no amount of policy
text repairs it, because the platform has nothing to enforce against. Separating the
identities is what converts every other rule here from a promise into a mechanism.

## 2. The identities

| Identity | Needs | Must not have |
|---|---|---|
| **Owner** | everything, including ruleset bypass as the emergency valve | to be reachable from an unattended session — its credentials are the one thing that must never be in an agent's environment |
| **Builder automation** | push to non-default branches; open and update pull requests; read checks | merge to the default branch; ruleset bypass; admin; the ability to change the trusted evaluator on the default branch |
| **Codex reviewer** | read the repository; post reviews and comments | `contents: write`, which the installed app currently holds and which reviewing does not need (`AGENTS.md` already says the role, not the capability, decides — this makes the capability match the role) |

GitHub does not offer path-scoped write for an identity: the builder can always *propose*
a change to a protected file on its own branch, and that is fine. The enforceable
controls are that it cannot merge it, cannot bypass the rules, and cannot alter the
workflow that judges it on the default branch.

## 3. Ruleset changes

Ordered. **The order is a safety property, not a preference** — see the warning below.

### A — identity

1. Create the builder automation identity (a GitHub App is preferable to a machine
   account: scoped permissions, auditable installation, revocable independently).
2. Remove the `RepositoryRole` holding permanent bypass, or prove the automation
   identity can neither hold nor inherit it. **A bypass actor voids every row below.**
3. Keep the owner's bypass, subject to the credential rule in §2.
4. Reduce the Codex app's permissions to review-only.

### B — atomicity

5. **Require status checks to pass**, listing the `suites` check and the gate's own
   check. The ruleset currently requires none, so the gate has nothing to read.
6. **Require branches to be up to date before merging**, or enable the **merge queue**.
   This is the atomicity guarantee: without it the merge result is built on a base
   nothing tested (`LANE_POLICY` §9).
7. **Require conversation resolution before merging.**
8. **Restrict merge methods to one.** Merge commit matches the existing history and
   keeps `H` as a parent of `M`. With three methods enabled the relation between `H`
   and `M` changes shape per merge, and the evidence means something different each
   time.
9. If required approving reviews is ever raised above zero, also enable **dismiss stale
   approvals on push** and **require approval of the most recent push**. Both are inert
   at zero and become holes the moment it is raised.

### C — activation, at canary time only

10. `allow_update_branch = true`.
11. `allow_auto_merge = true`.

> **Do not reorder C before B.** Enabling auto-merge while no check is required makes
> GitHub's native auto-merge available with nothing to wait for, which is an immediate
> merge. It is the only step in this runbook that causes harm by being taken early.

## 4. Verification before activation

Each of these is checked and recorded, not assumed:

- no bypass actor is an automation identity;
- the `suites` and gate checks are required, and are produced only by a workflow on the
  default branch that the automation identity cannot modify;
- force-push and branch deletion remain blocked on the default branch;
- the merge method is the single configured one;
- the kill switch is readable by the gate and not writable by the automation identity.

Only when all of them hold may the snapshot carry `mergeAtomicity: 'strict_base'` or
`'merge_queue'`. Nothing else in the system needs to change for auto-merge to become
possible, and nothing else needs to change to take it away again.

# Lane policy

The rules `autonomy/lane_gate.js` applies, and the limits of what they establish.
Normative source: DEC-012. Where this file and DEC-012 disagree, DEC-012 wins.

## What a lane is

A lane is **how much attention a pull request needs from the owner**, not how much
autonomy an agent has. The owner merges every pull request. No lane authorises a merge,
and the gate cannot perform one: it has no credentials and no write path.

The lane is a **floor**. The builder states an expected lane in the pull request body;
the gate does not read it. A builder may argue for more owner attention than the gate
computed, never for less. Where the two disagree, the reviewer treats the discrepancy as
a finding about the builder's judgement (`AGENTS.md`).

| Lane | Meaning |
|---|---|
| **GREEN** | Low attention. The diff can be read quickly. |
| **AMBER** | Read the diff and the review threads before merging. |
| **RED** | This changes what the system is, not only what it does. Decide consciously. |

## How the gate decides

From `git diff --raw -z` and `git diff --numstat -z` between base and head, plus
`git ls-tree` on the base for the top-level inventory. Nothing is supplied by a caller
and nothing is asserted by an agent.

**RED** if any of these fired, and the result names which and on which paths:

| Rule | Fires when |
|---|---|
| `PROTECTED_SURFACE` | a path — old or new — is under a protected surface |
| `CONTROL_FILE` | a basename at any depth is a control file |
| `NEW_TOP_LEVEL` | a path's first segment is not in the base tree |
| `UNUSUAL_FILE_KIND` | a symlink, a submodule, or a change of file mode |
| `FORK` | the pull request comes from a fork (DEC-011 §2) |
| `ESCALATED` | the builder or the reviewer escalated it |
| `UNCLASSIFIABLE` | a fact is missing, or a path is not a shape git produces |

**GREEN** if nothing above fired and every one of these holds: every path is under a
GREEN prefix; every status is `A` or `M`; no file is binary; at most `maxFiles` files;
at most `maxLines` lines added and deleted together. **AMBER** otherwise, naming which
of those conditions failed.

Protected-surface and control-file matching is case-folded, so `Docs/Autonomy/` is
protected. Top-level novelty is case-**sensitive**, so `Docs/` beside an existing `docs/`
is a new path and therefore RED.

The lists themselves — protected surfaces, control filenames, GREEN prefixes, the size
caps — live in `autonomy/lane_gate.js`, in one place, and changing any of them is RED.

## Uncertainty escalates, never relaxes

An absent fact is a collector that did not run, not one that found nothing. Facts that
are missing or of the wrong type produce RED with `UNCLASSIFIABLE`, never a lower lane.
Any agent may escalate a lane; none may lower one.

## What this does not establish

- **That a GREEN change is correct.** GREEN is a statement about *where* a change
  landed and how large it is. It says nothing about whether the change is right.
- **That the protected list is complete.** A document under `docs/` that becomes
  normative is GREEN until it is added to the protected list. Adding it is the
  mechanism, and adding it is RED.
- **Cumulative drift.** Each pull request is classified alone. Ten GREEN pull requests
  are not a GREEN change. Under owner merge the owner is the mitigation.
- **Anything about the review.** The gate does not read check runs, reviews, comments or
  labels. Whether CI is green and whether the reviewer has open findings are shown by
  GitHub on the pull request, where the owner is already looking.

## AUTO-GREEN

Provided for by DEC-012, with no authorised categories: nothing can auto-merge. The gate
reports `autoGreen: {enabled: false, categories: []}` so a reader can see the capability
exists and is off.

The gate emits structured facts — per file the status, both paths where relevant, source
and destination modes, additions, deletions and an explicit binary flag; plus new
top-level paths, fork provenance, the rules that fired and a summary — so that a future
AUTO-GREEN policy can be added as a separate consumer of those facts. Activating one is
itself RED and requires a new owner decision taken on real pull-request data.

## The review-cycle cap

Four cycles, in `AGENTS.md`, kept by the builder and visible to the owner in the pull
request timeline. The gate does not count them and does not read owner comments.
Reaching four without convergence means autonomy stops and the owner decides what the
work needs; it does not mean the pull request is ready (DEC-012).

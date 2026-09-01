# autonomy/ — the deterministic lane gate

The gate that classifies a pull request into a lane. The rules it applies are
`docs/autonomy/LANE_POLICY.md`; the decisions behind them are DEC-009 (the lanes) and
DEC-010 (who classifies, what Codex confirms, and `PROHIBITED`). This file covers the
shape of the code, not the policy — where the two disagree, the policy wins, and where
the policy and a DEC entry disagree, the DEC entry wins.

## What it is

One pure function. `classify(snapshot, policy)` takes a plain object describing a pull
request and returns the lane, the readiness, the reasons and whether a real auto-merge
is permitted. It performs **no I/O**: no network, no filesystem, no clock, no
credentials. It cannot merge anything, and it cannot be made to by any input.

That is the whole point of the boundary. Collecting the snapshot is privileged work
that talks to GitHub; deciding what the snapshot means is not, and keeping the decision
in a pure function is what makes it testable against fixtures, replayable over
historical pull requests, and impossible to subvert through the data it is given.

```js
const { classify } = require('./autonomy/lane_gate.js');
const result = classify(snapshot);        // the only entry point production uses
```

`classify` takes **no policy argument**. A caller able to supply its own allowlist could
grant itself GREEN, which is the promotion DEC-010 forbids any agent from performing, so
the shipped allowlist is frozen and unreachable from outside. `classifyUnderPolicy` is
the fixture seam for tests and for replaying a candidate category against history; every
result it produces is stamped `policySource: 'injected'`, so an outcome reached under a
synthetic allowlist can never be mistaken for one the shipped policy allows.

## What it returns

| Field | Meaning |
|---|---|
| `lane` | `PROHIBITED`, `UNCLASSIFIED`, `RED`, `GREEN` or `AMBER` — evaluated in that order |
| `readiness` | `READY`, or a comma-joined list of blockers. **Never changes the lane** |
| `reasons` | why, in words, for the audit record |
| `declarationMismatch` | an agent declared a lane the gate did not compute |
| `autoMergeAllowed` | a conjunction, false by default; no single condition grants it |
| `policyVersion`, `policySource`, `headSha`, `baseSha` | what was judged, and under which rules |

`autoMergeAllowed` is the only field that authorises anything, and it requires all of:
lane GREEN, readiness READY, a readable kill switch that is off, an atomic merge mode,
and a declaration bound to this exact head. Any of them missing yields false.

## The shipped state is the safe state

The GREEN allowlist is **empty**, so `classify` cannot currently return an
auto-mergeable result for any input. That is the owner's decision, not a placeholder:
a category is added only after historical replay, shadow classification and adversarial
fixtures show it holds. Until then the gate is an advisory classifier.

## Tests

```bash
node tests/test_lane_gate.js       # must print ALL PASS and exit 0
```

Dependency-free and offline, like the rest of `tests/`. The suite covers the acceptance
criteria of Issue #7 (named `T-#N`) and the adversarial cases the Strategic Council
identified: renaming a protected file out of its surface, case-only differences,
symlinks pointing into a protected directory, submodules, binaries, mode changes, a
truncated file list reported as complete, an abbreviated SHA, evidence computed under
another policy version, a check that passed on a different commit, a check from an
untrusted producer, an empty required-check set, a clean review older than the latest
review request, two approved categories combined, and a declaration that disagrees with
what the gate computed.

No test performs a real auto-merge. None could: the function has no way to.

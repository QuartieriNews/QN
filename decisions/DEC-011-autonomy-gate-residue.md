# DEC-011 — Three questions the autonomy-gate review could not settle

Status: OPEN
Blocks: closing the Issue #7 implementation (pull request #8). The gate, the policy and
the CI are built and their defects fixed; these three are not defects and no further
review cycle closes them.

Raised after five Codex review cycles on pull request #8 — one more than `AGENTS.md`
allows, granted by the owner for this change specifically. Fifty-nine findings across
the five cycles, every one verified against the repository and accepted; none rebutted.
The three below are what remains, and they remain because they are choices rather than
mistakes.

## 1. A regular expression is not a YAML parser

`tests/test_workflow_safety.js` asserts that no pull-request-controlled text reaches a
shell — Issue #7's acceptance criterion 10, which is a property of the workflow file
rather than of any running code.

It has been extended four times to recognise one more spelling of a `run` key: quoted,
then a spaced colon, then flow mappings, then counting keys independently of the
extractor so an unparsed shape fails rather than passes. The fifth cycle defeated that
too: `"run"` is a valid double-quoted YAML key that decodes to `run`, and both the
extractor and the counter see neither. The same applies to permissions — `"write"`
resolves to write access and reads as absent.

This is not a gap in the pattern. YAML decodes escapes, and any text-matching approach
is one encoding away from being wrong, silently and in the direction of passing.

- **A.** Constrain the workflow to a canonical subset the suite fully parses, and refuse
  any file that does not match that grammar. No dependency; the cost is that workflows
  must stay in a restricted form, and the grammar is one more thing to maintain
  correctly. **Recommended.**
- **B.** Add a YAML parser dependency for the Node test suites. Correct by construction,
  and it ends the repository's dependency-free tooling — `council/` states that property
  explicitly, and `requirements.txt` is the only manifest today.
- **C.** Accept the residual risk and document it: the assertion is best-effort against
  a workflow only this project's agents write.

## 2. Fork pull requests can never be ready

`.github/workflows/checks.yml` is push- and merge-queue-triggered, so a fork's pull
request receives no check run at all. The lane policy requires passing required checks
for AMBER and RED as well as GREEN, so the gate reports `BLOCKED_TESTS` for every fork
pull request, permanently.

The earlier claim that this was harmless — forks can never be GREEN and the owner merges
them under the reinforced control — was wrong in a way worth naming: the owner would be
merging with the gate saying *blocked*, which is exactly the state the whole design says
must never be routine.

- **A.** Add an unprivileged fork-triggered job under a **different check name**, so it
  cannot collide with the trusted `suites` run on a same-repository commit. **Recommended.**
- **B.** Change the readiness contract so fork pull requests do not require the manifest,
  and say plainly in the policy that a fork is merged on the owner's judgement with no
  automated evidence.
- **C.** Refuse fork pull requests as a matter of policy while the repository has no
  external contributors.

## 3. How an exception to the review-cycle cap is granted

The gate now refuses to authorise a change at or past the four-cycle cap unless an owner
exception names that exact head (`ownerCycleException`). What the code cannot decide is
how such an exception is *granted and evidenced*: this one arrived as a chat message to
the builder, which no gate can read and no audit trail records.

There is also a number worth deciding on rather than inheriting. Findings per cycle ran
15, 13, 8, 14, 9 — no clear convergence within five cycles, on a change of this kind.
`AGENTS.md` sets four; whether four is right for governance-sized work is a question the
data now speaks to.

- **A.** An exception is an owner comment on the pull request naming the head SHA, which
  the collector reads and binds. Auditable, and it keeps the grant where the work is.
  **Recommended.**
- **B.** An owner-applied label, simpler to read and weaker to attribute.
- **C.** Raise the cap for this class of change, which is a change to `AGENTS.md` and
  therefore RED in its own right.

## What is not in question

None of the fifty-nine findings is disputed, and none of them is waiting on this entry.
The reviewer and the builder agree on every one; what is open is only what should be
built next, which is the owner's to say.

Decided by: — · Date: — · Affected: `tests/test_workflow_safety.js`,
`.github/workflows/checks.yml`, `docs/autonomy/LANE_POLICY.md`, `AGENTS.md`, pull
request #8.

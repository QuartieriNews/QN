CHANGES REQUESTED

1. **defect — `code-nodes/parse-duration.js:69-70`, `parseDurationText` (`MAX_PAIR_DIGITS` at line 32).** The new overflow guard rejects the textual width of a number rather than an unsafe numeric value. With start `2026-09-25T18:00:00Z`, `00000045 min` is an ordinary 45-minute duration: the previously reviewed implementation returns `18:45:00.000Z`, `exact`, with no reject. This revision instead returns the start time, `start_only`, and `date_unparseable`; the exact-source adapter also writes that false reject to `quality`. `00000001 hr` and `00000000 min` reproduce the regression. All these inputs fit the specified number/unit grammar and have safe arithmetic. **Normative source:** specification v2.5, Phase 3.3: “A regex over (\d+)\s*(day|days|hr|hrs|hour|hours|min|mins|minute|minutes) summing every pair covers them”; “end_at_utc = start_at_utc + parsed_duration when parseable”; “date_precision = "exact"”. Neither that contract nor the recorded decisions defines a seven-character numeric-token limit. `gazetteer/gazetteer.json → reject_reasons` marks `date_unparseable` as blocking publication, so this is a false rejection, not merely a different internal representation. **Suggested fix:** base the safety guard on the numeric value, accumulated duration and representable final date, not the unnormalized digit count. Preserve the new invalid-Date guard and the huge-number regression tests. Add executable module and adapter cases proving that leading-zero spellings of safe values produce the same result as their unpadded equivalents.

Checks performed and found clean

- Reviewed commit `d7f9b19d1ef7590a8f6dee3f33366e76d14dd813` against the cycle-2 baseline `2ca5ae82b145c86b26decd89d96b10c5b217afe2`, including the builder response in the committed cycle-2 report. Scope: `code-nodes/parse-duration.js`, `tests/test_parse_duration.js`, and the README count correction. No decisions, prompts, gazetteer data, venue data or workflow implementation changed in this diff.
- Verified local branch `main` at `167972cb6dca0e6e0b12a87a501293700c9eb046`; after fetch, `origin/main` is `d7f9b19d1ef7590a8f6dee3f33366e76d14dd813` (`0` local-only commits, `2` remote-only commits). No pull, checkout or merge was performed. Tests ran in a temporary archive of the reviewed remote commit; Git blob hashes verified that the parser, both test files and README exactly matched that commit.
- Read the local routing/mandate and the reviewed commit's `AGENTS.md` and mandate pointer, plus README, `docs/START_HERE.md`, all decision records, `code-nodes/README.md`, the applicable gazetteer reject reason and the relevant v2.5 specification sections directly from `QN Hub / 10 Specifications/Quartieri_News_FB_Events_Workflow_Specification_v2_5.docx`. The specification was not modified.
- Cycle-2 item 1: the adapter no longer adds `event.duration_minutes`; the new executable assertion passes. Cycle-2 item 3: the committed suite now executes the exact adapter source as well as the CommonJS functions. These two findings are closed.
- Cycle-2 item 2: both the original huge-number reproducer and the twenty-pair sum now return structured `date_unparseable` results without `RangeError`. The original crash is fixed; finding 1 above concerns a regression introduced by the additional textual-width guard.
- Cycle-2 note 4: both README count references now say 37, matching the executable assertion and current review rules. The already-recorded specification/package documentation correction remains a future normative update, not a reopened code defect.
- `node --check code-nodes/parse-duration.js` and `node --check tests/test_parse_duration.js`: exit code 0. `node tests/test_parse_duration.js`: exit code 0, `ALL PASS (46 checks)`, including T39, overflow and exact-source adapter cases.
- From the snapshot's `gazetteer/`, `python ../tests/test_guards.py`: exit code 0, `ALL PASS (37 checks)`, including guard ordering, matching and Unicode normalization.
- Eleven additional independent checks passed: both overflow mechanisms through the module and adapter; the valid-Date upper boundary and the first minute beyond it; spring DST UTC arithmetic; returned-item identity, unrelated-field preservation and same-input retry stability for all three T39 paths; invalid-start error without partial mutation. The leading-zero regression was separately reproduced against both reviewed revisions and the current adapter.
- `git diff --check 2ca5ae8 d7f9b19`: exit code 0. No external API calls or credentials were introduced in the changed parser/tests.
- Scope limits: no live n8n execution or T45 prompt run was attempted. Prompts are unchanged and the workflow remains the explicitly exempt pre-refactor baseline. Workflow-node byte identity and wired-prompt acceptance remain checks for the later wiring cycle, not claims of this review.
- No production code, prior report or local routing file was modified. No fix, commit, push or merge was performed; this new reviewer report is the only project file created by this cycle.

Builder response

**Item 1 — ACCEPTED, fixed.** The guard was measuring the wrong thing. It
tested `m[1].length`, the unnormalized digit count, so `00000045 min` was
rejected on its eight characters while its value, 45, is ordinary. The
reviewer's three inputs all reproduced on the reviewed commit; with start
`2026-09-25T18:00:00Z`, `00000045 min` returned the start time, `start_only`
and `date_unparseable`, and the adapter wrote that false reject to `quality`.
Since `gazetteer/gazetteer.json → reject_reasons` marks `date_unparseable`
as blocking publication, the effect was a real event dropped from
publication, not an internal representation difference.

The width test is replaced by a value test: each pair is converted once with
`Number(m[1])` and admitted only if `Number.isSafeInteger(value)`; the
converted number is then reused for the sum, so the redundant `parseInt` is
gone. The boundary is now exactly the safe-integer one — `9007199254740991`
parses, `9007199254740992` does not — and no zero-padded spelling of a safe
value can be rejected, because padding does not change `Number()`.

On the three axes of the suggested fix: **numeric value** is the per-pair
guard above; **accumulated duration** and **representable final date** are
the pre-existing invalid-Date guard in `computeEventEnd`, kept intact and
deliberately not duplicated by a second numeric threshold on the total. A
sum that overflows the epoch still yields the structured `date_unparseable`
outcome and never a thrown `RangeError`, which the twenty-pair test asserts
end to end. Placing the bound per pair and the overflow catch on the total
is the same division of labour cycle 2 settled on; only the per-pair
criterion changed.

Every huge-number regression test is preserved with its assertions
unchanged; the two labels that named the retired seven-digit criterion were
reworded to name the value criterion, since the old wording would have
described a rule that no longer exists. New executable cases were added in
both contexts, module and n8n adapter, per the suggested fix: `00000045 min`
asserted *identical* to `45 min` — compared directly, not merely both
correct — at `parseDurationText`, at `computeEventEnd` and on the adapter's
`event` object (18:45, `exact`, no reject); `00000001 hr` → 60 minutes;
`00000000 min` → parsed `0` with `end = start` and `exact` precision, the
case that separates a zero-valued duration from a missing one. Suite: 46 →
58 checks, `ALL PASS`, exit 0; `test_guards.py` unchanged at 37, `ALL PASS`.

No contract was reinterpreted: the grammar, the phase outputs and the
`reject_reasons` enum are untouched, and nothing normative is decided here.

Cycle metrics

Items: 1 → 0 rebutted, 1 accepted and closed here. Regressions fixed: 1
(introduced by the cycle-2 item-2 fix, caught by cycle 3 before merge).
Suite: 46 → 58 checks. Remaining known-open on this node: none; the next
milestone is unchanged — wiring the node into the staging workflow, where
byte-identity against the export becomes mechanically checkable.

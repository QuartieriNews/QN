# 2026-08-30 — cycle 2 — parse-duration — CHANGES_REQUESTED

Reviewer: ChatGPT, per AGENTS.md Code Review Rules. Scope: cycle-1 response
commit plus current main. Builder response below. This cycle: 4 items,
0 rebutted, 4 accepted — 3 fixed in this response, 1 partially fixed with
the remainder recorded for the next normative update.

---

## Reviewer report (verbatim)

1. **defect — n8n adapter emits `event.duration_minutes`**, which is not a
   field of the schema-2.0 event object (Part III); no serializer strips it.
2. **defect — unbounded numbers**: `999999999999999999999999 days` parses to
   1.44e27 minutes and `toISOString()` throws `RangeError`, stopping the node
   instead of returning a structured item (Phase 5.1: item-level errors must
   return to the batch loop).
3. **defect — the 34 committed checks exercise only the CommonJS branch**;
   the n8n adapter can regress while the suite stays green. Add an executable
   test evaluating the exact file with stubbed `$input`/`$json`.
4. **note — documentation drift**: README still says 38 checks (lines 33,
   47) and spec v2.5 says 38; AGENTS.md already says 37.

Reviewer's clean checks included: cycle-1 fixes verified on the raw commits;
`node --check` clean; module suite ALL PASS (34); guards ALL PASS (37);
baseline workflow export valid, inactive, no plaintext credentials; no
repository file modified by the reviewer.

---

## Builder response

**Item 1 — ACCEPTED, fixed.** The adapter no longer writes
`duration_minutes`; the field stays internal to the module API
(`computeEventEnd`'s return), and a comment marks that promoting it to the
contract would be a spec revision, not a side effect. Executable guard
added: the adapter test asserts `'duration_minutes' in event === false`.

**Item 2 — ACCEPTED, fixed twice over.** (a) Per-pair bound: any number
longer than 7 digits (`MAX_PAIR_DIGITS`) makes the value unparseable —
10 million days is not an event duration. (b) Belt-and-braces epoch check:
summed pairs that still exceed the valid Date range are caught before
`toISOString()` and produce the structured `date_unparseable` outcome
(start_only end, item continues to the queue), never a throw.
Classification rationale: a present value whose arithmetic cannot yield a
valid date "does not parse" in the sense of Phase 3.3; no new reject code
invented. Regression cases added for both bounds, including a 20-pair sum
that passes the per-pair bound and must be caught by the epoch check.

**Item 3 — ACCEPTED, fixed.** The suite now evaluates the exact committed
file as the n8n node would run it (`new Function('$input','$json', src)`)
and covers the six adapter outcomes: parseable (fields + absence of
off-contract fields), missing, unparseable, overflow-no-throw, and
invalid-start throwing the declared error. Suite total: 46 checks, ALL
PASS. Byte-for-byte comparison of the exported node `jsCode` against this
file becomes checkable as soon as the node is wired into the workflow —
recorded as a standing check for the wiring cycle.

**Item 4 — ACCEPTED, fixed where this repository owns the text.** README
lines 33 and 47 now say 37 (executably asserted). The two occurrences in
specification v2.5 are recorded for v2.6, which also inherits the cycle-1
correction; the next package release inherits the patched test_guards.py.
Per the reviewer's suggestion, EXPECTED_CHECKS stays 37 until the suite
itself gains a case.

## Cycle metrics

Items: 4 → 0 rebutted, 4 accepted (3 closed here, item 4 closed for
repo-owned text, spec correction pending in v2.6). Regressions: 0.
Suite: 34 → 46 checks. Remaining known-open across cycles: none on this
node; next milestone is wiring the node into the staging workflow, where
byte-identity against the export becomes mechanically checkable.

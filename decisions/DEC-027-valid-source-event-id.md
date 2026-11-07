# DEC-027 — What a valid `source_event_id` is

Status: DECIDED (29 October 2026, owner in the builder session, on the question put by the builder)
Blocks: nothing since 29 October 2026. While open it blocked pull request #20 (native
Codex review of 29 October 2026, finding P1).

Question: Spec v2.5 Phase 1.3 says «Reject items without a valid source_event_id» and
gives no format. The first implementation of `code-nodes/dedupe-source-events.js`
accepted any scalar that is non-blank after trimming, so `false` or `Infinity` passed
as ids. What is a valid `source_event_id`?

Options:
A. Any scalar that is non-blank after trimming (the first implementation).
B. **CHOSEN.** A string that is non-blank after trimming, or an integer number, taken in
   its decimal form. Booleans, non-integer or non-finite numbers, objects and arrays are
   not valid ids.
C. Digits only after trimming (the shape of Facebook event ids): the strictest, but tied
   to one source; a source with alphanumeric ids would lose every item.

Claude recommendation: B.

Codex (reviewer, native review of pull request #20, 29 October 2026): finding P1 — the
node settled the ambiguity without a decision entry; asks for the owner's contract
before one interpretation is encoded and tested.

## Rule

A valid `source_event_id` is either a string that is not empty after trimming (its
normalized form is the trimmed string) or an integer number (its normalized form is the
decimal string). Anything else is not a valid id, and the item is rejected under Phase 1.3.

Builder's reading of "integer", stated so the owner can widen it with a new entry: only
integers JavaScript represents exactly (`Number.isSafeInteger`) count. A larger integer
has already lost digits when the JSON was parsed, so two different events could arrive
with the same number.

Impact: `normalizeSourceEventId()` in `code-nodes/dedupe-source-events.js` and its tests
(`tests/test_dedupe_source_events.js`, cases named DEC-027). Items with an invalid id are
counted in `rejected_missing_source_event_id`. Ids are still compared in normalized form,
so `" 7 "`, `7` and `"7"` remain one id. No workflow is wired to the node yet.

Decided by: owner · Date: 29 October 2026 · Affected components:
`code-nodes/dedupe-source-events.js`, `tests/test_dedupe_source_events.js`, Spec v2.5
Phase 1.3.

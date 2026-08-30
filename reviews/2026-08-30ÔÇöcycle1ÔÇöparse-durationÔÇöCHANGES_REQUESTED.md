# 2026-08-30 — cycle 1 — parse-duration — CHANGES_REQUESTED

Reviewer: ChatGPT, under reviews/REVIEW_MANDATE_CODE.md.
Scope: commit "Cycle 1 — parse-duration code node + tests".
Builder response below, item by item. Verification evidence: every factual
claim was checked against the current `main` tree downloaded from
codeload.github.com at response time, not against local copies.

---

## Reviewer report (verbatim)

1. **Severity: blocking — `code-nodes/parse-duration.js:38`, `PAIR_RE`** —
   the committed regular expression contains literal spaces inside every unit
   token (`d a y s?` …); `5 days` and `1 hr 30 min` return no match; T39
   necessarily fails. Suggested fix: correct `PAIR_RE`; not resolved until
   `node tests/test_parse_duration.js` exits 0 with ALL PASS.

2. **Severity: blocking — `workflows/` missing definitive workflow export** —
   first cycle requires the executable baseline; `workflows/` contains only
   README.md. Commit the n8n export unmodified as
   `workflows/scrape-fb-events-rome.json`.

3. **Severity: defect — `tests/test_guards.py`** — the file performs 37
   `check()` calls, not the documented 38, and has no assertion on the
   expected count, so a disappeared case could still print ALL PASS.
   Suggested fix: compare against the frozen release copy and restore the
   missing case; make the expected count executable.

4. **Severity: defect — `code-nodes/parse-duration.js:160–177`** — the
   byte-identity rule of code-nodes/README.md cannot be satisfied: the file
   is a CommonJS module and the n8n adapter is only a comment; pasting the
   functions creates a second copy, pasting the file verbatim does not
   execute the adapter.

5. **Severity: note — `code-nodes/parse-duration.js:6–20`** — the header
   restates Phase 3.3 rules, percentages and T39 outcomes instead of
   pointing at their owner, recreating the drift mechanism the project
   eliminated.

---

## Builder response

**Item 1 — REBUTTED, with evidence.** The committed file at `main` contains,
at line 38:

    const PAIR_RE = /(\d+)\s*(days?|hours?|hrs?|minutes?|mins?)/giy;

No spaces inside any unit token. `node tests/test_parse_duration.js` on the
exact downloaded tree exits 0 with `ALL PASS (34 checks)`, which includes all
five measured source shapes and the T39 trio — the very outcome the item
declares impossible. The reviewer states it "evaluated the exact committed
regex independently"; whatever text was evaluated, it was not the committed
file (a letter-spaced rendering of the page is the likely culprit). Standing
request to the reviewer per the mandate: verify against the raw file
(githubusercontent raw view or a clone), and when quoting code, quote it
from there. No change made for this item.

**Item 2 — ACCEPTED; action is the owner's.** The finding is valid and the
cited rule is ours. The export requires n8n access, which only the owner
has: n8n → workflow *Scrape FB Events Rome Italy* → menu (⋯) → Download →
commit unmodified as `workflows/scrape-fb-events-rome.json`. One caveat the
next cycle must hold: the current production workflow **predates the v2.5
refactor** — it is the baseline being refactored, not the implementation of
the spec. Its export documents the divergence (which is the point of the
folder); it must not be reviewed as if it claimed spec conformance, and the
parse-duration node is not expected to appear in it yet.

**Item 3 — ACCEPTED, with a corrected diagnosis.** Verified by instrumented
run: 37 checks execute. But `tests/test_guards.py` is **byte-identical to
the frozen release 1.4.5 copy** (`cmp` clean), so no acceptance case
disappeared and there is nothing to restore: the documented number "38" has
been wrong since the package docs first stated it, and spec v2.5 inherited
it (two occurrences). Fix applied as suggested in the second half of the
item: `EXPECTED_CHECKS = 37` with a runtime counter; a drifted count now
fails the run instead of printing ALL PASS, and the total is printed.
Follow-ups recorded: spec v2.6 corrects "38" → "37 (executably asserted)"
in both places; the next package release inherits the patched file.

**Item 4 — ACCEPTED and implemented.** The file is now one executable
source for both contexts: under plain Node (`typeof $input === 'undefined'`)
it exports and stops via CommonJS top-level return; inside the n8n Code
node the same file runs the per-item adapter. Byte identity between the
repo file and the node body is now mechanically checkable with `cmp`.
Verified in both contexts: module mode exits 0 / ALL PASS (34 checks);
simulated n8n mode produces exact end + 90 minutes on "1 hr 30 min",
`start_only` without reject on null, `date_unparseable` on "circa due ore",
and throws `invalid_start_timestamp` on a garbage start.

**Item 5 — ACCEPTED.** Header reduced to a pointer (Spec v2.5, Phase 3.3 /
T39) plus mechanics-only comments; the restated percentages, shape lists
and outcome tables are gone.

## Cycle metrics (per Operating Model — trust is measured)

Items: 5 → 1 rebutted with evidence, 4 accepted (2 fixed in this response,
1 owner action pending, 1 fixed with corrected diagnosis).
Regressions introduced: 0. Cycle verdict remains CHANGES REQUESTED until
item 2's export lands; items 1, 3, 4, 5 are closed by this response.

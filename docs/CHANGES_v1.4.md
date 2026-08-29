# Changes — v1.3 → v1.4 (and v1.4.1)

21 August 2026. Corrections after an external review of the v1.3 package. Every point below
was verified by running the code, not by re-reading the documents.

The uncomfortable summary: **the two worst defects were introduced in v1.3, not inherited.**
Both were in the parts v1.3 added, and both would have shipped.

---

## Breaking changes

| # | Change | What breaks |
|---|---|---|
| 1 | `venue_unresolved` is terminal, not a registry miss | Any implementation of v1.3's `WORKFLOW_FIXES` §2.11 queues almost every event before the alias lookup or the model runs. |
| 2 | Guards split into tier A / tier B, with tier B after the venue registry | Code running all five guards up front blocks human-resolved venues forever. |
| 3 | `name_coordinate_mismatch` rule replaced entirely | The v1.3 rule rejects valid Rome records. Any implementation of it must be discarded, not adjusted. |
| 4 | Editorial filter test order: `explicit_promotion` first | A v1.3-ordered classifier publishes most promotions. |
| 5 | `verification_status` → `geo_verification_status` in reconciliation | A literal implementation writes an orphan field and leaves the real one empty. |
| 6 | `municipality_code` added to the stored contract | Not breaking today; a corpus migration if added after the institutional block starts collecting. |

---

## 1. Blocking defects

### 1.1 `venue_unresolved` had two incompatible meanings

`WORKFLOW_FIXES.md` §2.11 said *a miss is `venue_unresolved`*. The resolution order in
`GAZETTEER_README.md` §3 said a registry miss continues to the alias lookup and then the
model. Both were in the same package.

`location.id` was present in **106 of 107** measured records. Under the first reading,
essentially every event at a not-yet-registered venue goes to the review queue on day one —
on a system whose entire review budget is twenty minutes a week. That is not a degraded
mode; it is a stopped system.

**Fixed:** a registry miss continues to the next step and is not a reject.
`venue_unresolved` fires only when `location.id` is present, is not in the registry, **and**
neither the alias lookup nor the model resolved the item.

### 1.2 The editorial filter could never reach its own exclusion

*Introduced in v1.3.* The three tests were ordered `identified_content` →
`substitutability` → `explicit_promotion`, with test 1 stopping on a hit.

Most promotions carry exactly what test 1 looks for. `"Rome Sunset Photography Experience
by XYZ"` has a company, a title and a theme: it stopped at test 1 as `local_interest` and
never reached the exclusion. The main editorial addition of v1.3 was neutralised by its own
ordering.

**Fixed:** `explicit_promotion` is a **gate that runs first**. A named seller is still a
seller — identified content distinguishes an occasion from routine programming, and cannot
distinguish an occasion from a product, because products have names too.

### 1.3 The name/coordinate guard rejected valid records

*Introduced in v1.3.* The rule read the text after the last comma of `location.name` as a
geographic tail and rejected anything not on an allowlist.

But `location.name` is a **venue name**, not an address. The text after its comma is
usually a room, a floor or a street. Running the shipped implementation:

```
Teatro Argentina, Sala Squarzina      -> name_coord_mismatch
Casa del Municipio, Sala Consiliare   -> name_coord_mismatch
```

Both are plausible real records. A guard that fires on valid records is worse than no
guard: it removes the item silently and irreversibly, and the reject queue shows a
plausible-looking reason.

**Fixed**, as two different rules for two different fields:

- **`location.city`** is genuinely composite — measured as `"Rome, NY, United States"`,
  `"Brighton and Hove, United Kingdom"`. Allowlist on the comma tail, as before.
- **`location.name`** gets a blocklist of foreign place markers compared against **whole
  comma-delimited segments**. No tail parsing. A blocklist fails open, which is the correct
  direction for an unbounded field where the bounding box and centroid guards also apply.

The first replacement attempt used a substring test and rejected `"London Pub"` — the same
defect one level down. The negative test caught it before it shipped, which is the point of
§4 below.

### 1.4 `geo_level = municipality` was not routable

The contract said a municipality-level item carries an empty `publication_zone_id` and that
the layout would use `geo_level` for the fallback — while storing no field saying *which*
municipality.

That is a rule with no output field, which is one of the project's own named principles,
and it would have surfaced only after the institutional block had collected a corpus. That
is a migration, not a fix.

**Fixed:** `municipality_code` is stored on every item. Derived from the zone's
`primary_municipality` at zone level; the only routing key there is at municipality level.

---

## 2. Ordering and contract corrections

**Guards now run in two tiers.** Tier A — bounding box, centroid blocklist,
`placeType: CITY` — asks whether the coordinate is usable at all and runs before everything.
Tier B — name/coordinate, `countryCode` null — asks whether the record is suspicious, and
runs **after the venue registry**, because a registry hit has already answered that
question.

v1.3 ran all five up front, which meant a venue a person had resolved stayed blocked
forever if its records kept arriving with `countryCode: null`. It also made v1.3's own
claim — that such a record would be "caught by the venue registry once reviewed" —
unreachable.

**`verification_status` → `geo_verification_status`** in the double-pass reconciliation, in
both the config and `PROMPT_GEO_BLOCK.md`. Everything else in the package used the longer
name; a literal implementation would have written an orphan field and left the real one
empty, violating I5.

**The cross-block contract was overstated.** v1.3 claimed `editorial_class` and
`content_type` were already the common, non-retrofittable contract for all four page
blocks. They are not: both enums are events-specific. What is genuinely common is the
*shape* — every item carries a geographic level, a freshness field, and some editorial
classification whose value set belongs to its block. Field names shared, enums extended per
block. Corrected in `PROJECT_VISION.md` and the config rather than by inventing enums for
blocks that have not been designed.

**Build and runtime now share one `norm()`.** v1.3 compared with `casefold()` in the build
and stripped accents at runtime, so the build's guarantee that a future collision fails the
build was false — `Città Test` and `Citta Test` were two keys for the build and one at
runtime. The documented behaviour (*strip punctuation, collapse spaces*) was also not
implemented: `"S. Angelo"` normalised to `s␣␣angelo`, and 30 keys in the current gazetteer
had the same problem. One function now, used by both, tested for agreement.

**Reject reasons carry `blocks_publication`.** `no_image` and `duplicate_suspected` do not
stop publication; mixing them with true rejects distorted the weekly sort, which is the one
number the week's work is prioritised on. `no_description` and `no_image` also have
producing rules now — v1.3 left them as dead counters.

**Online events have one rule instead of three mentions.** The README made it deterministic,
the prompt asked the model, and the findings had already measured `isOnline` as unreliable.
Now: online **only if** `isOnline` is true **and** there are no coordinates **and** there is
no `location.id`; result is an empty zone with `geo_level = city` and **no reject**. The
model is not asked, because it cannot see any of those fields.

**The review queue carries structural keys.** v1.3 said the deciding reason for Sheets was
that a fix applies in the same gesture with no bridge — then carried a write key for
`venue` only. Added: `source_id` (page/group id, which is also where the posts channel's
page registry starts filling), `matched_neighbourhood_id`, and an editable `fix_key`. Each
`fix_target` now names what it writes and against which key.

**The discarded sample has a defined store.** v1.3 said both *nothing is deleted, excluded
items go to the queue* and *wrongly discarded items never appear at all*. Reconciled:
`editorial_uncertain` goes into the working queue; `commercial_routine`, `promotion` and
venue-blacklist skips are written to the archive with `decision = auto_excluded` and are
never shown to the reviewer in bulk. That log is what the 10 weekly discards are sampled
from — and without it the editorial filter had no sensor at all, which is the state v1.3
shipped in while claiming otherwise.

---

## 3. Overstated claims, withdrawn

**The definition of done is a stop rule, not a proof.** The minimum satisfying it is 19/20
twice; 38/40 is compatible with a true accuracy between roughly 84% and 99% at 95%
confidence, and zero misses in 20 discards does not exclude a real error rate near 15%.
Twenty a week is what one reviewer can do, so the sample size is not what changes — the
claim is.

**The occurrence-count threshold was invented.** v1.3 stated that a count above ~20 leans
commercial and that community series run 8–12 dates. Neither number came from the data: the
sample holds 11 series in 107 records, 8 `WEEKLY` and 3 `CUSTOM`, none classified. Withdrawn.
Record `occurrence_count`, correlate it against the review archive after a few weeks, then
decide whether it is a usable prior.

**August cannot calibrate the fallback threshold.** The Handover said so in §5 and then told
the developer to run `zone_distribution.py` to calibrate it in §7. The next step now says
what that run actually gives: an exercise of the script and an exploratory floor.

**`zone_distribution.py` reported a tier called "strong" and told you to decide on it.** A
substring hit on `location.name = "Teatro Prati"` counted the same as an exact alias match,
while the production resolver does exact matching only — so the number was optimistic
relative to the thing it was standing in for. Three tiers now: `exact` (what production
does), `field_contains`, `text_contains`. Read `exact` as the floor and the total as the
ceiling.

---

## 4. Documentation propagation

Everything below was stale in v1.3 — the same class of defect v1.3 claimed to have
eliminated, and the likeliest way for a fixed bug to return, since a developer copies from
whichever document they opened.

- `zone_not_published` was `lookup` in the builder and still `validation` in
  `WORKFLOW_FIXES.md` §2.12 and `GAZETTEER_README.md` §5.
- `WORKFLOW_FIXES.md` §2.6 still listed four guards and called them all numeric
  comparisons.
- The Handover's deliverables table still labelled `gazetteer.json`, `PROMPT_GEO_BLOCK.md`
  and `GAZETTEER_README.md` as v1.2, and referred to nine spec changes where the file lists
  thirteen.
- `WORKFLOW_FIXES.md` §2.1 carried an example with `geo_logic_revision: "1.2"`.

---

## 5. New file

`test_guards.py` — guards and matching, tested in **both** directions.

v1.3's verification section listed only cases where a guard fired correctly. That is why
`name_coord_mismatch` shipped rejecting valid venues: nothing in the package asked whether
a guard stayed silent when it should. The negative half of this suite immediately caught a
second-order recurrence of the same bug in the replacement rule.

```
python test_guards.py      # exits non-zero on any failure
```

35 checks: 10 that must reject, 13 that must NOT, 2 on guard ordering around a registry
hit, 4 on the matching tiers, 6 on build/runtime normalisation agreement. Re-count them
from the run, not from this line.

---

## 6. Verification

- `build_gazetteer.py` runs clean: 440 neighbourhoods, 91 zones, 89 pages, 29 non-publishable.
- The regenerated Italian export is unchanged against the v1.3 output.
- Build and runtime `norm()` agree on every tested string, and produce no double spaces.
- With runtime normalisation applied in the build, `Colle del Sole` is still the only
  ambiguous key — aligning the two did not introduce a collision.
- `test_guards.py`: 35 checks, all passing.
- The four v1.3 false positives (`Teatro Argentina, Sala Squarzina`, `Casa del Municipio,
  Sala Consiliare`, `Libreria Tuba, Via del Pigneto 39`, `London Pub`) now pass the guards;
  `London, U.K.`, `Waterloo` and `Florence, Tuscany, Italy` are still rejected.

---

## 7. What was deliberately left alone

- **`SOURCE_DATA_FINDINGS.md`**, still unchanged. It is a measurement on a date.
- **The 102 corrections, the 7 open questions, the 89 zones.**
- **The enums for the other three blocks.** Naming what is not yet designed is what caused
  the overstatement in §2; the fix was to describe the contract accurately, not to design
  the blocks.
- **The gazetteer write-back.** `fix_target = gazetteer` still ends with a person editing
  the master workbook. A script writing into the master would create a second master — the
  defect the fifth principle exists to prevent. v1.4 only makes the row and the string
  unambiguous.


---

## 8. v1.4.1 — documentation sync

No functional change. A second review of the v1.4 package found five places where a
document still described v1.3 behaviour. All were propagation failures, not new defects,
and one of them was blocking.

| # | File | Was | Now |
|---|---|---|---|
| 1 | `PROMPT_GEO_BLOCK.md` | The v1.3 comma-tail rule for `location.name` **and** `location.city` | The two v1.4 rules: allowlist tail on `city`, whole-segment blocklist on `name` |
| 2 | `WORKFLOW_FIXES.md` §2.12 table | `venue_unresolved` fires on a registry miss | Terminal, after alias and model both fail |
| 3 | `WORKFLOW_FIXES.md` §2.14 | Every excluded item goes to the queue | Only `editorial_uncertain`; the rest to the archive as `auto_excluded` |
| 4 | `gazetteer.json` `reject_reasons[].meaning` | The old comma-tail definition | Points at `guards.name_coordinate_mismatch` — one definition, not two |
| 5 | `PROJECT_HANDOVER.md` | "read the strong column"; two files labelled v1.3 | `exact` as floor; labels corrected |

Also: `CHANGES_v1.4.md` claimed 29 tests where `test_guards.py` runs 35.

**#1 was blocking.** `PROMPT_GEO_BLOCK.md` is the file a developer pastes into the
workflow. Following it would have reintroduced, verbatim, the guard that rejects
`"Teatro Argentina, Sala Squarzina"` — the defect v1.4 exists to fix.

### The pattern, which is worth more than the five fixes

Three review rounds, three different sets of defects, and by v1.4 the residue is
**entirely documentation propagation**. That is a structural signal, not a diligence
problem: the same rule is currently written out in full in three or four places, so a
change has three or four chances to be missed.

The rules themselves already have a single home — `gazetteer.json`, generated from code.
The remaining duplication is in prose. The durable fix is for the Markdown to *point at*
the JSON rather than restate it: `PROMPT_GEO_BLOCK.md` should say "the rule is in
`guards.name_coordinate_mismatch`" and explain **why** it is what it is, rather than
paraphrasing **what** it is. Explanation does not go stale. Restatement does.

That refactor is not part of v1.4.1, which changes nothing but the stale text. It is the
right thing to do before `START_HERE.md` is written — otherwise the index gains a fifth
place for the same rule to drift.

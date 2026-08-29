# START HERE

**Quartieri News — Events module · release 1.4.3 · 21 August 2026**

**This file is the only place a version number lives.** Individual documents no longer
carry one. Six review rounds produced defects, and by the last three the defects were
almost entirely stale version markers and rules restated in four places — a hand-maintained
number in every header is a rule with no output field, which is precisely what the rest of
this project forbids. One number, here.

Read this page first. It takes three minutes and tells you where everything else is.

**Continuing in a new conversation?** Read `NEXT_SESSION_BRIEF.md` instead — it carries the
open task, the open decisions and the measured facts, so the work is not repeated.

---

## 1. What this is

Automated collection of public events in Rome, published across 89 neighbourhood pages
covering all 15 municipalities.

**Events are one block of four** on each page — the others are municipal and city-council
assemblies, local news, and conversation from neighbourhood groups. Only the events block
is specified here. What a page displays is decided at **layout time** from stored fields,
never at ingestion.

---

## 2. Reading order

| # | File | Why | Pages |
|---|---|---|---|
| 0 | `NEXT_SESSION_BRIEF.md` | The open task and the three open decisions. Only if you are picking the work back up | 4 |
| 1 | `PROJECT_VISION.md` | Why the project exists, and what is deliberately undecided | 4 |
| 2 | `PROJECT_HANDOVER.md` | Every decision taken, with its reason | 8 |
| 3 | `SOURCE_DATA_FINDINGS.md` | What the source data actually does, measured. The evidence under everything else | 3 |
| 4 | `WORKFLOW_FIXES.md` | The defect list and the 13 changes the specification needs | 8 |
| 5 | `PROMPT_GEO_BLOCK.md` | The geography prompt and the validation code — **this is pasted into the workflow** | 5 |
| 6 | `EDITORIAL_FILTER.md` | What counts as a locally useful event, with the prompt | 4 |
| 7 | `REVIEW_QUEUE.md` | Where human review happens, and the definition of done | 3 |
| 8 | `GAZETTEER_README.md` | Data model and the eight invariants. Reference, not narrative | 6 |

Changelogs (`CHANGES_v1.2/1.3/1.4.md`) are history. Read them only to understand why
something is the way it is.

---

## 3. Where each rule lives — one place each

The recurring defect in this project's history has been the same rule written out in three
or four documents and updated in two. **`gazetteer.json` is the contract.** It is generated
from `build_gazetteer.py`, which is where the configuration is edited. The Markdown explains
*why* a rule exists; when the two disagree, **the JSON wins**.

| Rule | Lives in |
|---|---|
| The 440 neighbourhoods and 91 zones | `Rome_Neighbourhood_Gazetteer_EN.xlsx` (master, the only editable data file) |
| Resolution order, precedence, double pass | `gazetteer.json → resolution` |
| Guards, tiers, thresholds, blocklists | `gazetteer.json → guards` |
| Editorial filter tests and enums | `gazetteer.json → editorial` |
| Review queue schema, weekly sample, done | `gazetteer.json → review` |
| Reject reason enum | `gazetteer.json → reject_reasons` |
| The 89 allowed prompt values | `prompt_list_publication_zones.txt` (generated) |
| Venue records | `venues.json` — **learned at runtime, never regenerated** |
| Expected editorial verdicts | `golden_set_editorial.json` — 30 hand-classified items |
| Expected zones | `golden_set_geographic.json` — 40 hand-marked items |
| Italian wording of the export | `it_strings.json` |

---

## 4. Run it before reading further

```bash
python build_gazetteer.py     # regenerates gazetteer.json, the prompt list, the IT export
python test_guards.py         # 38 checks, both directions. Exits non-zero on failure
python zone_distribution.py sample_107_direct_urls.json
```

Then, before either prompt is wired to publication, run it against the golden sets:
`golden_set_editorial.json` (30 items, expected class / basis / content_type) and
`golden_set_geographic.json` (40 items, expected zone and geo_basis, including 9 that must
come back empty). Both carry their own pass thresholds. A disagreement is evidence the
**prompt** is unclear before it is evidence the model is wrong.

Expected: 440 neighbourhoods, 91 zones, 89 pages, 29 non-publishable; all tests passing.

The build **fails rather than warns** on a duplicate id, an unjoinable zone, a new
undeclared ambiguous lookup key, or a stoplist entry that is not a real key.

---

## 5. Five things that must not be got wrong

Each one shipped as a defect in an earlier revision and was found by review or by running
the code. They are the expensive ones.

1. **Empty is a correct answer.** A model forced to always name a zone produces no rejects
   to review and silent errors on live pages. The whole operating model depends on the
   model being allowed to say *unknown*.
2. **A venue-registry miss is not a reject.** It continues to the alias lookup and the
   model. `venue_unresolved` is terminal — registry, alias and model all failed.
   `location.id` is present on 106 of 107 records; reading a miss as a reject queues the
   entire corpus on day one.
3. **The editorial filter checks `explicit_promotion` first.** Promotions carry company
   names, titles and themes, so any test for "identified content" placed before the
   exclusion lets them through.
4. **Guards run in two tiers.** Coordinate validity before everything; suspicion signals
   *after* the venue registry, because a venue a person already resolved is not made
   suspicious by a missing country code.
5. **`is_page` and `resolvable` are real booleans.** Comparing against `"TRUE"` rejects
   every event silently.

---

## 6. What is not in this package, and who owes it

| Missing | Owner |
|---|---|
| **Specification v2.5** — v2.4 is in this package but predates release 1.4.4 entirely. See `SPEC_V25_WORKPLAN.md` | Next session. **Do not implement from v2.4 as it stands.** |
| The n8n workflow export | Developer |
| The generated event card (fallback when there is no image, and after a takedown) | Developer |
| **A decision on commercial guided tours** — ~20% of the sample. See `golden_set_editorial.json → known_gap` | Riccardo, before the filter goes live |
| Boundary check on 5 addresses in `golden_set_geographic.json` (`confidence: verify`) | Riccardo |
| The one canonical JSON shared by Events and Posts | Open architectural task |

---

## 7. Known and accepted

- **Distribution is unmeasured.** In the 107-event August sample, deterministic matching
  placed 31 and Municipio X got zero. That is expected — the model does the geographic work
  — but the real distribution across 89 pages needs weeks of live data. Do not reduce the
  zone count on August numbers.
- **The venue registry's payoff is unproven.** 8 of 157 `location.id` values carried more
  than one event, none inside the largest sample. Cheap infrastructure whose return must be
  measured over months, not the highest-leverage item remaining.
- **Discovery is manual**, one to two times a week. It is the real cost of the system and
  the part that does not scale to other cities. Accepted knowingly for phase one.
- **Images are downloaded and republished**, with the copyright exposure accepted and five
  mitigations required (`PROJECT_HANDOVER.md` §2.15).
- **`Colle del Sole`** is the one ambiguous lookup key in 440 rows. Until it is resolved,
  it rejects rather than guesses.

# Changes — v1.1 → v1.2

20 August 2026. What was changed in the handover package, why, and what breaks.

---

## Breaking changes

Three. Anything written against v1.1 must be updated.

| # | Change | What breaks |
|---|---|---|
| 1 | `is_page` and `resolvable` are real booleans, not `"TRUE"` / `"FALSE"` | Any `z.is_page === "TRUE"` comparison now matches nothing and rejects every event. The validation snippet in `PROMPT_GEO_BLOCK.md` v1.1 was exactly this. |
| 2 | `resolution.allowed_values` removed from `gazetteer.json` | Derive the list from `publication_zones` filtered on `is_page === true`. It existed in three places; one copy is enough and three guarantee drift. |
| 3 | `prompt_list_publication_zones.txt` no longer carries `(Municipio X)` | Nothing consumes it programmatically, but a prompt still holding the old list contradicts the validator — which is the bug this fixes. |

---

## 1. Defects fixed

**1.1 The prompt list contradicted the validator.** The list gave the model
`Acilia  (Municipio X)`; the validation code compared against `Acilia`. A model correctly
obeying *use the exact spelling from the list* would have been rejected as
`zone_not_in_list`. The list is now generated from the JSON and carries names only.

**1.2 The gazetteer joined on a display name.** `neighbourhoods[].publication_zone` was
`"Centro Storico"` — a display string — while invariant I2 says the display name is not a
key. `publication_zone_id` added to every row, in the workbook and in the JSON. The display
name stays, as display.

**1.3 29 neighbourhoods have no page.** 28 map to `Agro Romano`, one to `Other`, and
neither is `is_page = true`. A correct alias hit on Corcolle, Fiorano or Torricola produced
a real place with nowhere to publish — and would have been logged as `zone_not_in_list`,
which is false and would have put a non-bug at the top of the weekly reject sort. New code
`zone_not_published`, new invariant I6, and `publishable` derived on every row so the case
is visible in the data rather than discovered in the queue.

**1.4 `resolvable = false` was ambiguous.** Acilia, Ostia, Monteverde, Laurentino and
Trigoria are containers as neighbourhoods and valid publication zones at the same time.
Invariant I1 read literally — *a container is never a resolvable value* — would have
rejected *ad Acilia*, the commonest phrasing in Municipio X. Now split: I1 for the
neighbourhood level, I1b for the zone level, with the behaviour spelled out
(`neighbourhood_id = null`, zone resolved).

**1.5 Ambiguity had no defined behaviour.** `Colle del Sole` is the only lookup key in 440
rows that matches two neighbourhoods with different pages. An exact-match lookup would have
taken whichever came first. Now `reject_reason = ambiguous_alias`, and
`build_gazetteer.py` fails the build if a new ambiguous key appears without being declared.

**1.6 Two editable masters.** The English and Italian workbooks held the same data, both
looked editable, and had already diverged on the name of the key column
(`neighbourhood_id` vs `neighborhood_id`). English is now the master, Italian a read-only
export, each with a first sheet saying so, and `build_gazetteer.py` regenerates everything
derived.

**1.7 The open-questions list in the handover was wrong.** It named
Sallustiano/Ludovisi — which are on the `corrections` sheet with `status = corrected` — and
omitted Trionfale, the Trigoria/Laurentino/Maglianella containers and the
`municipality_code` normalisation. The handover now reproduces the sheet, which is the
authority.

---

## 2. Decisions closed

Five items that were open, now written into the files so the developer does not have to
ask.

**2.1 The double pass is conditional, not removed.** One pass when `geo_basis` is
`explicit_address` or `explicit_zone`; two independent passes when it is `inferred` or
`unknown`, or when there was no venue hit and no street address. Disagreement is
`ai_disagreement`, not a tiebreak. The alternative — two passes on everything — doubles the
AI cost across the whole volume to protect a segment `geo_basis` already isolates. Promote
to always-double if the weekly sample shows single-pass accuracy below 95%.
→ `PROMPT_GEO_BLOCK.md`, `gazetteer.json → resolution.double_pass`

**2.2 The pre-Apify filter is a throttle.** *Known → never scrape again* saves the money
and breaks the corpus: a URL never re-fetched can never produce a new `source_hash`, so
postponements, venue changes and cancellations become invisible. Replaced by a TTL that
tightens as the event approaches, a permanent skip only once an event has ended, a
`max_refreshes_per_run` bound, and *missing on refresh is a flag, never a delete*.
→ `WORKFLOW_FIXES.md` §2.8

**2.3 `human_verified` ships now.** `geo_verification_status`, `human_verified_at`,
`human_verified_by`, `geo_conflict`; precedence
`human_verified > venue_registry > alias > ai`; survives a `geo_logic_revision` bump; a
disagreeing lookup logs a conflict instead of overwriting.
→ `WORKFLOW_FIXES.md` §2.1, `gazetteer.json → resolution.precedence`

**2.4 Recurring events: one article, many occurrences.** Series-level `content_id`,
updatable `occurrences[]`, `effective_end` from the last non-cancelled occurrence. Resolves
the one-`source_event_id`-to-52-dates conflict instead of working around it.
→ `WORKFLOW_FIXES.md` §2.5

**2.5 The venue registry is a separate store.** Keyed on `location.id`, in `venues.json` /
Firestore — **not** inside `gazetteer.json`, because that file is regenerated from the
workbook and a merge would erase every learned venue on the first rebuild. Consulted after
`human_verified` and before the alias lookup; a miss is `venue_unresolved`, which one
review makes permanent.
→ `venues.json`, `GAZETTEER_README.md` §9

**2.6 The neighbourhood level is stored when known.** The model still chooses among 89
zones. But an alias or venue hit that knows the finer level stores both
`publication_zone_id` and `neighbourhood_id`. `null` when the zone came from the model.
→ `gazetteer.json → resolution.store`

---

## 3. New files

| File | Why |
|---|---|
| `build_gazetteer.py` | Makes "one master, generated copies" enforceable instead of aspirational. Rebuilds the JSON and the prompt list, and **fails** on a duplicate id, an unjoinable zone, or a new undeclared ambiguous key. |
| `venues.json` | Venue registry schema, rules and seed record. Separate lifecycle from the gazetteer. |
| `zone_distribution.py` | Resolves a sample against the 89 zones and prints every page, including the empty ones. The empty ones are the finding. |
| `CHANGES_v1.2.md` | This file. |

---

## 4. New reject reasons

`reject_reasons` is now a list of objects carrying a `layer`, because the weekly sort is
only useful if the top entry points at something fixable.

| Code | Layer | Fires when |
|---|---|---|
| `venue_unresolved` | lookup | `location.id` present, not yet in the registry |
| `ambiguous_alias` | lookup | The matched name belongs to two neighbourhoods |
| `zone_not_published` | validation | Real place, zone is not a page |
| `ai_disagreement` | validation | The two independent passes disagreed |

---

## 5. What was deliberately left alone

- **`SOURCE_DATA_FINDINGS.md`** is unchanged. It is a record of measurement on a specific
  date and editing it would weaken it.
- **The 102 corrections and the 7 open questions.** Those are editorial decisions, not
  mine to close.
- **The 89 zones themselves.** No zone was added, removed or regrouped. Whether 89 pages is
  the right number is a product question, and `zone_distribution.py` is how it gets
  answered — with data, not with an opinion.
- **The deferred street register.** Still deferred, still the documented fallback, still
  reopened by the same trigger: zone accuracy materially below 95% on the weekly sample.

---

## 6. Verification

Everything below was checked against the files rather than asserted:

- 440 neighbourhoods, 91 zones, 89 with `is_page = true`.
- The prompt list, `publication_zones[is_page]` and the old `allowed_values` agree exactly
  once the bracketed municipality is stripped — the bug was formatting, not content.
- Every `publication_zone` joins; no orphans.
- 29 neighbourhoods route to a non-page zone.
- Exactly one ambiguous lookup key across name and alias space: `Colle del Sole`.
- Seven rows carry `resolvable = false`; five of them name a valid publication zone.
- 82 of 440 rows carry at least one alias — the starting point for the learning loop.
- The two workbooks contained identical id sets before the split into master and export.

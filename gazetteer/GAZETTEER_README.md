# Rome Neighbourhood Gazetteer

Canonical reference for resolving Rome place names to publication pages. Replaces the
ad-hoc neighbourhood list currently embedded in the AI prompt.

**Scope:** all of Rome, 15 municipalities, **89 published pages**.

**Files**

| File | Role |
|---|---|
| `Rome_Neighbourhood_Gazetteer_EN.xlsx` | **Master. The only editable file.** Sheets: `gazetteer`, `publication_zones`, `corrections`, `open_questions`, `legend`. |
| `build_gazetteer.py` | Regenerates everything below from the master. Run it after every edit. |
| `gazetteer.json` | Generated. Data plus the resolution policy, guards and reject-reason enum. |
| `prompt_list_publication_zones.txt` | Generated. The 89 allowed values, ready to paste into the prompt. |
| `Mappa_Quartieri_Normalizzata.xlsx` | **Export**, Italian metadata. Read-only, and now genuinely generated — see §7. |
| `it_strings.json` | Translation memory, English → Italian. Hand-maintained; the one place to fix a wording in the export. |
| `venues.json` | Venue registry keyed on Facebook `location.id`. **Learned at runtime — not generated.** See §9. |
| `PROMPT_GEO_BLOCK.md` | Drop-in replacement for the geography section of the prompt, plus the validation code. |
| `EDITORIAL_FILTER.md` | What counts as a locally useful event. The rule behind `not_an_event`. |
| `REVIEW_QUEUE.md` | Where human review physically happens, and the definition of done. |
| `zone_distribution.py` | Counts events per zone on a sample. Run this before building anything else. |

Place names stay in Italian — they are proper nouns. Only metadata is in English.

---

## 1. Data model

Two levels, deliberately separate.

**Neighbourhood** — a fact about the world. Where the event actually is.
**Publication zone** — an editorial decision. Which page the event appears on.

Many neighbourhoods map to one zone: Dragona, Dragoncello and Bagnoletto all publish to
`dragona-dragoncello`. Regrouping is a config change, not a data migration.

**The model resolves straight to the publication zone.** Asking it to choose among 440
toponyms is a harder question than the site needs answered; 89 coarse areas is the right
granularity. But the neighbourhood level is **stored whenever it is known
deterministically** — from the venue registry or an alias match — because it costs nothing
and maps, search and any future sub-page will want it.

### `gazetteer` — 440 rows

| Column | Notes |
|---|---|
| `neighbourhood_id` | Stable slug. **This is the key.** Store this, never the display name. |
| `name_display` | Reader-facing name. |
| `aliases` | Pipe-separated alternative spellings. **Grows with every error you fix** — see §5. |
| `municipality_code` | Roman numerals `I`–`XV`. Empty = outside Rome or unassigned. |
| `spans_municipalities` | Only where a neighbourhood genuinely straddles two (currently: Quadraro). |
| `publication_zone` | Display name of the page. Human-readable only. |
| `publication_zone_id` | **The join key.** New in v1.2. |
| `zu_code` | Official Roma Capitale urban-zone code where a match exists (e.g. `13B`). |
| `population` | From the city dataset. Use it to judge which pages can stand alone. |
| `resolvable` | `false` = container **at the neighbourhood level**; see I1. |
| `status` | `unchanged` / `corrected` / `added` relative to the source file. |

In the JSON each row also carries `publishable`, derived from its zone's `is_page`. 29 rows
are `false` — see I6.

### `publication_zones` — 91 rows, **89 with `is_page = true`**

`Agro Romano` (spans 8 municipalities) and `Other` are catch-all containers, not pages.

---

## 2. Invariants

Not style preferences. Breaking any of these reintroduces a defect present in the source
data.

**I1 — A container is never a resolvable neighbourhood.**
`Acilia` contains `Acilia Nord` and `Acilia Sud`. Offering all three as parallel
neighbourhood options produces different answers for the same address across runs. Seven
rows carry `resolvable = false`.

**I1b — but `resolvable` says nothing about the zone.**
Acilia, Ostia, Monteverde, Laurentino and Trigoria are non-resolvable neighbourhoods *and*
valid publication zones. A post that says *ad Acilia* must resolve to zone `acilia` with
`neighbourhood_id = null`. An implementation that reads I1 as "reject Acilia" rejects the
commonest phrasing in Municipio X.

**I2 — The display name is not a key.**
Two distinct places are both called Colle del Sole (Municipio VI and XI). Join on
`neighbourhood_id` and `publication_zone_id`. Until v1.2 the gazetteer itself broke this,
joining neighbourhood to zone by display name.

**I3 — Empty is a correct answer.**
The old prompt said `NEVER leave municipio, urban_zone, or neighborhood empty`. That line
is gone. It mandated a confident guess, and it made the reject queue impossible: a model
that always answers produces no rejects to review, only silent errors on live pages.

**I4 — A closed list is only a constraint if it is validated.**
Check the returned value against the list in code. Without that check the model will
eventually return `Ostia Lido` or `Centro Storico Nord` and it will go live.

**I5 — Record how, not just what.**
`geo_basis` distinguishes a stated address from a context inference. They have very
different error rates and must be countable separately. `geo_verification_status`
distinguishes both from *a person decided*.

**I6 — A resolved place is not necessarily a publishable one.**
28 neighbourhoods map to `Agro Romano` and one to `Other`. A correct alias hit on Corcolle
or Fiorano yields a real place with no page to sit on. That is `zone_not_published`, a
different failure from `zone_not_in_list`, and it must have its own counter — otherwise it
distorts the top reject reason, which is the number the weekly work is prioritised on.

**I7 — Ambiguity is a reject, not a coin flip.**
One lookup key today matches two neighbourhoods with different pages. On more than one
match: empty, `reject_reason = ambiguous_alias`. `build_gazetteer.py` fails the build if a
new ambiguous key appears without being declared in the config.

*Corrected in v1.3:* the build checked ambiguity over neighbourhood names and aliases only,
while the runtime index also contains the 91 zone display names. A zone name colliding with
an unrelated neighbourhood would have passed the build and become a coin flip in
production. The check now covers all three key spaces. (No such collision exists today —
`Colle del Sole` remains the only ambiguous key either way.)

**I8 — A key in a description is not a key in a location field.** *New in v1.3.*
`prati`, `talenti`, `eur`, `marconi` and `morena` are ordinary Italian words, a price token
and a surname. Matched inside free text they produce confident false positives, and those
false positives land in the one number that decides whether 89 pages are executable.
`free_text_stoplist` in the JSON lists the keys that are matchable in `location.name`,
`streetAddress`, `address` — where a string is a place by construction — and not in a title
or a description. A minimum key length is not a substitute: it excludes `EUR` and `AXA`,
two real zones, while still admitting every common word of five letters or more.

---

## 3. Resolution order

0. **`human_verified`** — set by a person. Wins over everything, survives every
   recomputation. Stop.
1. **Mode** — online event → zone empty. Stop.
2. **Guards, tier A** — bounding box, centroid blocklist, `placeType: CITY`. Is the
   coordinate usable at all. See §4.
3. **Venue registry** — `location.id` → zone. A hit skips the model entirely, **and skips
   tier B**. A miss is not a reject: it continues to step 3b. See §9.
3b. **Guards, tier B** — name/coordinate contradiction, `countryCode` null. Suspicion
   signals, which a registry hit has already answered.
4. **Alias lookup** — exact match against `gazetteer.aliases` and `name_display`. A hit on a
   neighbourhood whose zone is not a page stops here with `zone_not_published` — it does
   **not** fall through to the model. Corrected in v1.3; the check used to sit after the
   model, where it could never fire.
5. **Model, pass 1** — closed list of the 89 zones, empty permitted, `geo_basis` returned.
6. **Model, pass 2** — only when pass 1 returned `inferred` or `unknown`, or when there was
   no venue hit and no street address. Independent, then reconciled. See
   `PROMPT_GEO_BLOCK.md`.
7. **Validation** — value must be in the list; a non-page zone is `zone_not_published`; an
   `inferred` zone with no stated location is rejected.

Steps 2, 3 and 7 are the load-bearing ones, and their hit rate rises every week the reject
queue is worked. The model sits between deterministic layers on both sides.

---

## 4. Guards (in `gazetteer.json → guards`)

Coordinates from the Facebook API are not always trustworthy. All four checks are numeric
comparisons — no polygons, no street register, no geocoding service.

- **Rome bounding box.** Coordinates outside it → `outside_rome`, whatever the model said.
- **Centroid blocklist.** Unrelated events share identical coordinates representing the
  city, not a venue. Four pairs observed so far, listed in the JSON. Resolving them yields
  a confident wrong answer in the historic centre. **Extend the list whenever a coordinate
  pair recurs across unrelated events.**
- **`placeType: CITY`** → city known, area not. Force empty.
- **Name/coordinate contradiction** → `name_coord_mismatch`. A *string* comparison, tier B,
  and rewritten in v1.4 because the v1.3 rule rejected valid records. `location.city` is
  composite, so an allowlist on its comma tail is right. `location.name` is a venue name —
  the text after its comma is a room or a floor — so it gets a blocklist of foreign markers
  compared against **whole comma-delimited segments**. `"Teatro Argentina, Sala Squarzina"`
  passes; so does `"London Pub"`; `"London, U.K."` and a bare `"Waterloo"` do not.
- **`countryCode` null with coordinates present** → `country_code_missing`. In v1.2 this
  guard had an action and no reject code, so it was uncountable in the weekly sort — which
  is the number the week's work is prioritised on.

---

## 5. Operating model

Review the **reject queue**, not the publication queue. Cost then scales with errors rather
than with volume, and falls as the system improves.

**Every reject carries a `reject_reason`** from the enum in `gazetteer.json`. Sort by
frequency each week and attack the top one. Without a structured reason this is reading,
not debugging, and it never converges. The enum now separates lookup failures
(`venue_unresolved`, `ambiguous_alias`, `zone_not_published`) from validation failures
(`zone_not_in_list`, `ai_disagreement`, `zone_unknown`) precisely so the sort points at a
fixable thing. From v1.4 each entry also carries `blocks_publication`: `no_image` and
`duplicate_suspected` are flags that appear in the queue without stopping publication, and
mixing them with true rejects distorted the same sort.

**Every fix goes into the gazetteer or the venue registry, not into the item.** Correcting
one event solves one event. Adding the street as an `alias`, or the `location.id` as a
venue record, solves every future event at that address. This is how the 99% is reached — a
gazetteer that fattens on each error, not more prompt engineering.

**Human corrections survive recomputation.** A zone set by a person carries
`geo_verification_status: human_verified` with `human_verified_at` and `human_verified_by`,
and wins over any later recalculation, including a `geo_logic_revision` bump. If a later
alias or venue lookup disagrees, set `geo_conflict = true` and log it — never overwrite.
The conflict is a signal that the gazetteer is wrong, which is exactly the thing worth
knowing.

**Sample 20 published items and 10 discarded ones per week, from the first published
week.** The reject queue shows false negatives — things blocked that should have passed. It
never shows false positives: events published on the wrong page, which do not block because
the system is confident. Nor does it show what the editorial filter removed *wrongly*,
which leaves no trace anywhere. Two questions, one per sample: *is the zone right?* and
*was this genuinely not worth publishing?*

The queue itself lives in a Google Sheet with a defined schema — see `REVIEW_QUEUE.md`,
which also states the definition of done for this block.

Only 82 of the 440 rows currently carry an alias. Early on, expect the reject queue to be
dominated by alias misses. That is the system working as designed, not a defect.

Above 95% the approach holds. Around 70%, you learn it from 80 checks instead of from
eighty wrong pages.

---

## 6. What changed from the source file

102 corrections, itemised with reasons on the `corrections` sheet.

- **Three duplicate names resolved.** Colle del Sole split into two ids; Trionfale's
  inconsistent Municipio I row removed; Quadraro merged into one row spanning V and VII.
- **Seven containers marked non-resolvable** — Acilia, Ostia, Monteverde, Trigoria,
  Laurentino, Maglianella, Other.
- **Five rows in the wrong municipality or zone.** Igea, Miani and Parco di Monte Mario
  moved from Municipio I to XIV. Sallustiano and Ludovisi kept in Municipio I but
  reassigned to zones that belong to it.
- **Three missing Municipio X entries added** — Ostia Nord (41,894 residents), Ostia Sud
  (35,282) and San Francesco were in the city population dataset but absent from the
  resolution list. The first two are the most populous zones in that municipality.
- **Municipality codes** converted from `Municipio 1..15` to Roman numerals.
- **Orthography normalised** — `Conca D'oro` → `Conca d'Oro`, `S. Angelo` → `Sant'Angelo`,
  `Tor De' Schiavi` → `Tor de' Schiavi`. Original spellings preserved in `aliases`.

Seven items were left open; see `open_questions`. They need an editorial decision. The
authoritative list is the sheet itself: Trionfale, Colle del Sole ×2, Agro Romano, the five
Municipio X toponyms without a ZU code, the Trigoria/Laurentino/Maglianella containers, and
the `municipality_code` normalisation. Sallustiano and Ludovisi are **not** open — they were
corrected and appear on the `corrections` sheet.

### What changed in the last documentation sync

Documentation only, no functional change. Five places still described v1.3 behaviour: the
name/coordinate rule in `PROMPT_GEO_BLOCK.md`, the `venue_unresolved` row in the
`WORKFLOW_FIXES.md` table, the editorial-discard routing in the same file, the
`reject_reasons[].meaning` string for `name_coord_mismatch`, and two stale labels in the
handover. Plus the sentence in §9 above, found on a later pass.

### What changed in v1.4

- Guards split into tier A (coordinate validity, first) and tier B (suspicion, after the
  venue registry).
- `name_coordinate_mismatch` rewritten as two rules — the v1.3 version rejected valid
  venues.
- `venue_unresolved` made terminal; a registry miss is not a reject.
- `municipality_code` added to the stored contract.
- `explicit_promotion` promoted to the first editorial test.
- One shared `norm()` for build and runtime; `blocks_publication` on every reject reason;
  a single deterministic rule for online events.
- `test_guards.py` added — both directions, 35 checks.

### What changed in v1.3

- `zone_not_published` moved from post-model validation to the alias lookup, where the case
  can actually occur.
- `country_code_missing` added: the guard existed in v1.2 with no reject code.
- `name_coord_mismatch` given an implementable rule (comma-tail allowlist, plus any tail
  that is itself a gazetteer key).
- `free_text_stoplist` added, and invariant I8 with it.
- The build's ambiguity check extended to the zone display names (I7).
- `geo_level`, `editorial_class`, `editorial_basis`, `content_type` and `date_precision`
  added to the stored contract; `next_occurrence` derived on series.
- `editorial` and `review` sections added to `gazetteer.json`.
- The Italian export is now genuinely generated, with `it_strings.json` as the translation
  memory. The regenerated file was verified identical, row for row, to the hand-built one.
- `venue_nature` and `editorial_override` added to the venue record.

### What changed in v1.2

- `publication_zone_id` added to every neighbourhood row. The neighbourhood → zone join no
  longer runs on a display name (I2).
- `is_page` and `resolvable` are real booleans, not the strings `"TRUE"` / `"FALSE"`.
  **Any code comparing against `"TRUE"` will now reject everything.**
- `resolution.allowed_values` removed. The list is derived from
  `publication_zones[is_page = true]`; there is one copy of it, not three.
- `prompt_list_publication_zones.txt` no longer carries `(Municipio X)` after each name —
  the previous list contradicted the validator.
- Reject reasons extended: `zone_not_published`, `ambiguous_alias`, `ai_disagreement`,
  `venue_unresolved`. Each entry now carries the layer it fires in.
- `resolution.double_pass`, `resolution.precedence` and
  `resolution.verification_status_values` added — the double-pass decision is now written
  down instead of implied.
- `resolution.lookup` added: ambiguous keys, container semantics, unpublished zones.
- Venue registry split into `venues.json` (§9).
- The Italian workbook is an export; the English one is the master. The key column in the
  Italian file was `neighborhood_id` and is now `neighbourhood_id`.

---

## 7. Regenerating

The workbook is the master. After editing it:

```bash
python build_gazetteer.py
```

This rewrites `gazetteer.json`, `prompt_list_publication_zones.txt` **and**
`Mappa_Quartieri_Normalizzata.xlsx`. Never hand-edit any of them — otherwise the copies
drift and none of them is authoritative.

*Corrected in v1.3:* the MASTER sheet has claimed since v1.2 that the script rebuilt the
Italian export. It did not. The claim is now true. Italian wording lives in
`it_strings.json`, a small hand-maintained English → Italian memory; the build reports any
string it could not translate rather than silently emitting English, and the regenerated
export was checked row-for-row against the hand-built one before this was adopted.

The build **fails** rather than warns on: a duplicate id, a `publication_zone` that does
not join, a `publication_zone_id` that disagrees with the join, a new ambiguous lookup key
(now checked across zone names too), or a `free_text_stoplist` entry that is not a real
lookup key. A generator that silently produces a broken corpus is worse than no generator.

The resolution policy, the guards and the reject-reason enum are not in the workbook. They
are code-level configuration and live in the `CONFIG` block at the top of the build script.

Consumers of the JSON:

1. The extraction prompt — `publication_zones` filtered on `is_page = true`.
2. The validation step — same list, plus `guards` and `reject_reasons`.
3. The alias lookup.
4. The site, for the neighbourhood → page grouping.

One source, four consumers. This is the precondition for both ingestion workflows —
Facebook Events and Facebook Posts — writing into the same corpus.

---

## 8. Known distribution risk

Across three live samples, Facebook event supply for Rome was heavily concentrated in
Municipio I and II. With 89 pages the likely failure mode is not total volume but
distribution: a handful of pages full and most of them nearly empty.

This is measurable **now**, before anything further is built:

```bash
python zone_distribution.py sample.json --csv distribution.csv
```

It resolves an existing sample against the zones and prints every page including the empty
ones. It determines whether 89 pages is executable as planned or whether thin pages need a
fallback to municipality-level content — which is a product decision, and one the developer
needs before starting, not after.

---

## 9. Venue registry — separate on purpose

`location.id` was present in 106 of 107 measured records and stable across events at the
same place. A registry keyed on it resolves a venue once and forever: no fuzzy name
matching, no accent handling, no spelling variants, and no AI call.

It lives in `venues.json`, **not** in `gazetteer.json`, for one reason: venue records are
learned at runtime, and `gazetteer.json` is regenerated from the workbook. Merging them
would erase every learned venue on the first rebuild. `build_gazetteer.py` never touches
`venues.json`.

The write path is a Firestore collection; the JSON is the export the workflow and the site
**An unknown `location.id` is not an error, and on its own it is not a reject either.** A
registry miss simply continues to the tier-B guards, the alias lookup and the model, any of
which may resolve the item. `venue_unresolved` is **terminal**: it fires only when the
registry, the alias lookup and the model have all failed. Then it is not a failure but an
invitation — one review makes every future event at that address free.

Reading the miss itself as the reject would queue almost the entire corpus on day one:
`location.id` was present in 106 of 107 measured records, and none of them is in the
registry yet.

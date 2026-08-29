# Workflow Fixes

**21 August 2026.** Concrete defect list for both ingestion workflows, plus the
changes the specification document needs. Ordered by severity within each section.

Items marked **[decided]** were open in the previous revision and now have an answer that
the developer can implement without asking. Items marked **[new in v1.3]** were found on
review of the v1.2 package.

---

## 1. `Process FB Post (Sub-workflow)` — n8n

### 1.1 The geography prompt mandates invention — **blocking**

```
NEVER leave municipio, urban_zone, or neighborhood empty for Rome addresses
If exact match is uncertain, choose the MOST LIKELY and widely recognized area
```

This is an instruction to guess, and it contradicts the project's stated principle that a
null is better than an invented location. It also makes the reject-queue operating model
impossible: a model that always answers produces no rejects to review, only silent errors
on live pages.

Aggravating factors:

- The allowed list holds ~250 entries. Agreement collapses as the option set grows.
- It contains `Acilia`, `Acilia Nord` **and** `Acilia Sud` — overlapping values that
  guarantee inconsistent output for the same address.
- `municipio` and `urban_zone` are free text with no enumeration. The schema example gives
  `"urban_zone": "Centro Storico"`, which is not an official urban zone name — the model
  learns from it.
- Nothing records **how** the geography was obtained, so a certain value cannot be told
  from a guess downstream.

**Fix:** replace the whole section with `PROMPT_GEO_BLOCK.md`, and add the validation code
that follows it.

### 1.2 The image URL is requested from the model — **bug**

The output schema contains `"image_url": "https://scontent.xx.fbcdn.net/v/t39..."` — with
an ellipsis, which actively teaches the model to truncate. `Download Image` then reads from
`output.image_url`.

Facebook image URLs are hundreds of characters long with signing tokens. The model will
corrupt them, not always visibly.

**Fix:** take the image URL from the scraper's post object. Remove the field from the AI
schema entirely.

### 1.3 Double `JSON.stringify` — **bug**

`Build Event Record` returns `event_json` already serialised. The Sheets node then writes
`{{ JSON.stringify($json.event_json) }}`, stringifying a string. The sheet receives escaped
quotes throughout.

**Fix:** `{{ $json.event_json }}`.

### 1.4 `Download Image` has no guard — **bug**

If the post has no image the node receives `url: ""` and the item fails. Roughly 10% of
records have no image.

**Fix:** an IF before it, or `onError: continue`.

### 1.5 The post is saved before classification — **durability defect**

Flow order is `Doc Exists?` → `Save All Posts` → `Classify`. A transient OpenAI failure
leaves the post recorded as seen, and `Skip Existing` excludes it permanently.

This is the same claim-before-commit problem the main specification solves with
claim → write → commit ordering.

**Fix:** either classify first and save on success, or save with `status: "pending"` and
promote to `"processed"` at the end, reprocessing pending records on later runs.

### 1.6 No event-level deduplication

The key is `postId`. A page announces the same sagra three times — launch, reminder,
day-of — producing three posts, three rows, three articles.

**Fix:** a soft key on `normalise(title) + start_date + location` that flags rather than
deletes.

### 1.7 Posts are never re-read

`Skip Existing` closes the door on first sight. Facebook posts get **edited** — a
postponement is written into the original post, not a new one.

**Fix:** a hash of the post text, mirroring the `source_hash` mechanism in the events
pipeline.

---

## 2. Events pipeline — changes against spec v2.3

### 2.1 `human_verified` is missing from the enums — **blocking** — **[decided]**

Human review is mandatory by design, but the contract had no field to record its outcome.
Neither `method` nor `verification_status` had a value meaning *a person decided*.

**Fix, to implement now:**

```json
{
  "publication_zone_id": "acilia",
  "neighbourhood_id": "acilia-nord",
  "geo_basis": "explicit_address",
  "geo_verification_status": "human_verified",
  "human_verified_at": "2026-08-20T10:14:00Z",
  "human_verified_by": "riccardo",
  "geo_logic_revision": "1.4",
  "geo_conflict": false
}
```

`geo_verification_status` enum, in `gazetteer.json → resolution.verification_status_values`:
`human_verified`, `deterministic_venue`, `deterministic_alias`, `ai_agreement`,
`ai_single_pass`, `unresolved`.

**Stickiness rule:** `human_verified` wins over every recomputation and survives a
`geo_logic_revision` bump. Precedence is `human_verified > venue_registry > alias > ai`.

**Conflict rule:** if a later alias or venue lookup disagrees with a `human_verified` value,
set `geo_conflict = true` and log it. Never overwrite. The conflict means the gazetteer is
probably wrong, which is worth more than the individual item.

### 2.2 `neighborhood_slug` is missing from the Firestore registry — **[decided]**

The registry carries `municipality_code` only. Without the zone, "how many events did zone
X have in the last 60 days" requires opening the Drive JSONs one by one — and that query is
the basis for deciding what each page displays.

**Fix:** store `publication_zone_id` **and** `neighbourhood_id` on the registry record.
`neighbourhood_id` is filled only when known deterministically (venue registry or alias
match), `null` when the zone came from the model. It costs one field and it is the level
maps, search and any future sub-page will need.

Note the field name: `publication_zone_id`, not the display name. The gazetteer itself
joined on display names until v1.2; do not reintroduce that.

### 2.3 `max_events_per_run: 50` is a test limit not marked as one

It sits in the workflow configuration beside production settings, and the owner sign-off
checklist has no item requiring it be raised before the schedule is activated.

**Fix:** a sign-off checklist line, plus `cap_reached: true|false` in the run report. If
`returned_by_source` equals the cap, the run almost certainly truncated silently.

### 2.4 Date handling — **[new in v1.3: the parser is now specified]**

v1.2 declared a `duration` parser necessary and did not say what it should do, which left
the defect it was meant to close still open. Two decisions are required, not one: how to
parse the free text, and what to do when it is absent — `duration` was null in **45 of 107**
records.

**Parser.** `duration` is free text of a small number of shapes, all observed:
`"5 days"`, `"1 hr 30 min"`, `"2 hrs"`, `"45 min"`, `"1 day"`. A regex over
`(\d+)\s*(day|days|hr|hrs|hour|hours|min|mins|minute|minutes)` summing every pair covers
them. Anything that does not match is unparseable — do not attempt to be clever with
natural language.

```
end_at_utc     = start_at_utc + parsed_duration     when parseable
date_precision = "exact"

end_at_utc     = start_at_utc                        when duration is null
date_precision = "start_only"

reject_reason  = date_unparseable                    when duration is present and
                                                     does not parse
```

**`date_precision` is the new field**, and it is the point. Without it, an event with no
duration is indistinguishable from a one-minute event, and the layout hides it at midnight
on its start date. With it, the layout knows the end time is an assumption and can keep the
item visible for the rest of the day.

Note the asymmetry: a **missing** duration is normal and must not reject — 42% of records —
while a **present but unparseable** duration is a real signal that the parser needs
extending, and should be counted.

- Never derive absolute times from `dateTimeSentence` — it renders in arbitrary timezones
  (a Rome event appeared with SAST).
- Without this, multi-day events are treated as finished after day one: the exact defect
  the v1.1→v2.x correction was meant to prevent, reintroduced by the source.

### 2.5 Recurring events — **[decided]**

11 of 107 records carry `hasChildEvents`, with child counts up to 52. One article per
occurrence is not the answer; neither is one article with a single date.

**Decision: one canonical article per series, with an occurrence list.**

```json
{
  "content_id": "fbev-1234567890-series",
  "series": {
    "is_series": true,
    "frequency": "WEEKLY",
    "source_event_id": "1234567890",
    "occurrence_count": 52,
    "first_start_at_utc": "2026-09-05T18:00:00Z",
    "last_start_at_utc": "2027-08-28T18:00:00Z"
  },
  "occurrences": [
    { "start_at_utc": "2026-09-05T18:00:00Z", "end_at_utc": "2026-09-05T20:00:00Z", "status": "scheduled" },
    { "start_at_utc": "2026-09-12T18:00:00Z", "end_at_utc": "2026-09-12T20:00:00Z", "status": "scheduled" }
  ]
}
```

Consequences the developer must implement, not infer:

- `content_id` gets one stable id for the series. This resolves the
  one-`source_event_id`-to-52-dates conflict rather than working around it.
- `occurrences[]` is sorted ascending and is **updatable**: a cancelled or moved date sets
  `status` on that entry, it is not deleted.
- `effective_end` for the article is the last non-cancelled occurrence, so the series does
  not disappear from the site after the first date.
- **`next_occurrence` — new in v1.3.** Derived: the earliest non-cancelled occurrence at or
  after now, recomputed on each run. `effective_end` solves the data model; it does not
  solve the display. A yoga series with 52 occurrences, in a block ordered by publication
  date, either pins to the top forever or never appears at all. `next_occurrence` is what
  the events block sorts on, and it is also the field the layout reads when deciding
  whether a page has enough zone-level content or should fall back to municipality level.
  A series whose occurrences are all in the past has `next_occurrence = null` and drops out
  by the same rule as a finished single event.
- The page renders "every Saturday" or the next three dates from `occurrences[]`. Both come
  from the same field.
- `duration` was present and parseable on **all 11** recurring records in the sample, so
  per-occurrence end times are obtainable.

### 2.6 Deterministic guards, in two tiers — **[revised in v1.4]**

Configuration in `gazetteer.json → guards`. **They are not all numeric comparisons**, and
they do not all run in the same place. v1.2 and v1.3 both said otherwise.

| Tier | Guard | Kind | Runs |
|---|---|---|---|
| A | Rome bounding box | numeric | before everything |
| A | Centroid blocklist | numeric | before everything |
| A | `placeType: CITY` | string equality | before everything |
| B | Name/coordinate contradiction | string | **after the venue registry** |
| B | `countryCode` null with coordinates | null check | **after the venue registry** |

**Why the split.** Tier A asks whether the coordinate is usable at all; nothing downstream
can repair a coordinate in Milan. Tier B asks whether the record is suspicious — a question
a venue-registry hit has already answered. Running tier B first, as v1.3 did, meant a venue
a person had resolved stayed blocked forever if its records kept arriving with
`countryCode: null`, contradicting the registry's premise and making v1.3's own claim that
such a record would be "caught by the venue registry once reviewed" unreachable.

**The name/coordinate rule was also wrong**, not just misplaced. v1.3 read the text after
the last comma of `location.name` as a geographic tail. But `location.name` is a **venue
name**: the tail is usually a room, a floor or a street number. On review the rule rejected
`"Teatro Argentina, Sala Squarzina"` and `"Casa del Municipio, Sala Consiliare"`. Now split:

- **`location.city`** — genuinely composite (`"Rome, NY, United States"`). Allowlist on the
  tail after the last comma.
- **`location.name`** — split on commas, reject only if a **whole segment** matches
  `foreign_place_markers`. Not a substring test: that first attempt rejected `"London Pub"`.
  A blocklist here fails open, which is the right direction for an unbounded field.

`test_guards.py` checks both directions. The negative half is the one that matters.

### 2.7 Field corrections from measured behaviour

- `cost_type` defaults to `unknown`; `booking_url` from `ticketsInfo.buyUrl`.
  `paidContent` and `ticketsInfo.price` are unusable.
- `is_rome` from `location.countryCode` plus coordinates — **never** from the description
  text. `location.city` is null in 88 of 107 records and composite when present.
- Soft duplicate key `location.id + utcStartDate`, flagging only.
- Venue gazetteer keyed on `location.id`, not on venue names — see 2.11.

### 2.8 Pre-Apify filter: a throttle, not an exclusion — **cost** — **[decided]**

Apify bills per event returned, not per new event, and a 30-day window collected weekly
re-bills the same event roughly four times.

The previous formulation — *known → never call Apify again* — would have saved the money
and broken the corpus. Facebook events get **postponed, moved, cancelled, re-priced**, and
a URL that is never re-fetched can never produce a new `source_hash`. The point of
`source_hash` is to notice changes; a permanent skip removes the only thing that can feed
it.

**Fix: a refresh TTL, not a blocklist.**

```json
{
  "refresh_policy": {
    "never_seen":                   { "action": "scrape" },
    "starts_within_72h":            { "ttl_hours": 24 },
    "starts_within_7d":             { "ttl_hours": 72 },
    "starts_later_than_7d":         { "ttl_hours": 168 },
    "series_parent":                { "ttl_hours": 168 },
    "already_ended":                { "action": "skip_permanently" },
    "cancelled_or_404_on_refresh":  { "action": "flag, do not delete" },
    "max_refreshes_per_run":        60
  }
}
```

Rationale for the shape: the nearer an event is, the more expensive a stale record is —
someone turns up on the wrong evening. A month-out event can be checked weekly. An event
that has already ended never needs checking again, and that is where most of the saving
comes from, not from skipping upcoming events.

`max_refreshes_per_run` bounds the bill even if the TTL logic misfires; the run report must
carry `scraped_new`, `scraped_refresh` and `skipped_fresh` so the ratio is visible rather
than inferred from the invoice.

**Missing on refresh is a flag, never a delete.** An event that 404s may be cancelled, may
be a privacy change, may be a Facebook glitch. Set `source_status: "unreachable"` with a
timestamp and let a person decide.

### 2.9 Discovery strategy must be recorded

`discovery_strategy: manual_url_collection`, with `collected_at` per batch and a run-report
warning when the most recent collection is older than N days. Otherwise a missed week is
discovered by looking at the site rather than at a counter.

### 2.10 Archive the raw JSON for all Rome events

Including those outside the current publication scope, and including those resolving to
`Agro Romano` or `Other`. A few KB on Drive, and a Facebook event from three months ago
cannot be re-scraped. This is what allows a new page to launch with history rather than
empty — and it is the holding pen for `zone_not_published` items if a future page covers
them.

### 2.11 Venue registry on `location.id` — **[decided]**

`location.id` was present in 106 of 107 records with a location and stable across events at
the same place. A registry keyed on it resolves a venue once and forever: no fuzzy name
matching, no accent handling, no AI call.

**It does not live in `gazetteer.json`.** That file is regenerated from the workbook;
merging the two would erase every learned venue on the first rebuild. Schema and rules are
in `venues.json`; the write path is a Firestore collection, the JSON is the export the
workflow and the site read.

Position in the resolution order: after `human_verified` and the tier-A guards, before the
tier-B guards and the alias lookup.

**A registry miss is NOT a reject — corrected in v1.4.** The sentence this replaces said
"a miss is `venue_unresolved`". Read literally, with `location.id` present in **106 of 107**
records, every event at an unregistered venue would have gone to the queue before the alias
lookup or the model ever ran — the entire corpus, on day one, on a system whose review
budget is twenty minutes a week.

A miss simply continues to the next step. `venue_unresolved` is **terminal**: it fires only
when `location.id` is present, is not in the registry, **and** neither the alias lookup nor
the model resolved the item. Then it is not an error but an invitation — one review makes
every future event at that address free.

### 2.12 Reject reasons: four new codes

`gazetteer.json → reject_reasons` is now a list of objects with a `layer`, because the
weekly sort is only useful if the top reason points at a fixable thing.

| Code | Layer | Fires when |
|---|---|---|
| `venue_unresolved` | lookup | TERMINAL: `location.id` present, not in the registry, **and** alias lookup and model both failed. A registry miss alone is not a reject — see §2.11. |
| `ambiguous_alias` | lookup | The matched name belongs to two neighbourhoods (Colle del Sole) |
| `zone_not_published` | **lookup** | Real place, but its zone is not a page (Agro Romano, Other). Fires on an alias hit, not after the model — the model only ever sees the 89 pages. |
| `ai_disagreement` | validation | The two independent passes returned different zones |

`zone_not_published` matters more than it looks: **29 of the 440 neighbourhoods** map to a
non-page zone. Without its own code those land under `zone_not_in_list`, which is false and
would put a non-bug at the top of the weekly queue.

### 2.13 The geographic double pass is conditional — **[decided]**

Two independent passes stay, but they are spent where they are needed:

- **One pass** when `geo_basis` is `explicit_address` or `explicit_zone`.
- **Two passes** when it is `inferred` or `unknown`, and always when there was no
  venue-registry hit and no street address on the record (`location.streetAddress` was null
  in 94 of 107).

The second pass must be independent — same closed list, no sight of the first answer.
Disagreement is `ai_disagreement`, not a tiebreak.

Reopen and promote to always-double if the weekly sample shows single-pass accuracy below
95% on `explicit_address` items. Full table in `PROMPT_GEO_BLOCK.md`.

### 2.14 The editorial filter has a rule — **[new in v1.3]**

`not_an_event` has been in the reject enum since v1.1 with nothing that could produce it. A
reject code with no rule is a counter that stays at zero while the thing it names goes to
the page — and the sample contained photo shoots, guided tours and cruises.

The rule, the prompt and the calibration procedure are in `EDITORIAL_FILTER.md`; the
contract is in `gazetteer.json → editorial`. What the developer implements:

- A **separate AI pass** from geography, not a merged one. Two judgements with different
  error rates must be countable separately (I5).
- Three returned fields: `editorial_class`, `editorial_basis`, `content_type`.
- `uncertain` is a permitted answer and produces `reject_reason = editorial_uncertain`.
  A queue item, not a discard.
- Two new reject codes: `commercial_routine` and `editorial_uncertain`.
- `venue_nature` on the venue record, passed to the classifier as **context, not as a
  shortcut**. Only an explicit `editorial_override` of `whitelist` or `blacklist` skips the
  call, and both are human acts.
- **Nothing is deleted, but not everything reaches the working queue.** `editorial_uncertain`
  goes into the queue — the classifier could not decide, so a person should.
  `commercial_routine`, `promotion` and venue-`blacklist` skips are written to the archive
  tab with `decision = auto_excluded`. Putting a few hundred routine items in front of the
  reviewer each week would destroy the twenty-minute budget the whole design is built
  around. That archive log is the store the ten weekly discards are sampled from, and it is
  the editorial filter's only sensor — see `REVIEW_QUEUE.md`.

The failure mode to design against: this filter fails silently in the one direction the
reject queue cannot show. The queue records what was excluded, never what was excluded
wrongly. That is what the ten sampled discards per week are for (§2.16).

### 2.15 `geo_level` on every item — **[new in v1.3]**

`neighbourhood` · `zone` · `municipality` · `city`. Set by the ingesting block, never by the
model. The events pipeline writes `neighbourhood` when `neighbourhood_id` is known and
`zone` otherwise.

It costs one field today and it is the field the page layout needs in order to fill a thin
block with municipality-level content without anything being relabelled. The other planned
blocks do not resolve to a neighbourhood and must not be forced to: a municipal commission
sits at municipality level by nature, and inventing a neighbourhood for it would write an
invented fact into the corpus — which is the one thing the whole design refuses to do.

**The fallback happens at render time, from stored fields. An item is never re-resolved to
a coarser zone.**

### 2.16 The review queue has an address — **[new in v1.3]**

The operating model has always said *review the reject queue*. It never said where. Full
schema in `REVIEW_QUEUE.md`; contract in `gazetteer.json → review`.

- One Google Sheet, two tabs (`queue`, `archive`), one row per item, a `block` column and
  filter views — **not** one tab per block.
- Five editable columns only: `decision`, `decided_zone`, `fix_target`, `fix_key`, `fix_note`. `fix_key` carries the alias string when `fix_target = gazetteer`; the id columns already carry the key for the other targets.
- `fix_target` ∈ `gazetteer` · `venue` · `source` · `none`. Without this column the stated
  principle *every fix goes into the gazetteer, not into the item* has nowhere to happen.
- n8n appends; the queue tab is never sorted or reordered in place, because the write-back
  matches on `content_id`.
- Decided rows are **moved to `archive` by the workflow, never deleted**. The archive is the
  only record of human judgement in the system.
- `decided_at` distinguishes *not yet decided* from *decided and not yet written back*.

**Weekly sample: 20 published items and 10 discarded ones.** The second is new and is the
only sensor the editorial filter has.

**Definition of done for this block**, so the move to the posts channel is not decided on a
feeling: two consecutive non-August weeks at or above 95% zone accuracy on the published
sample, a stable and understood top reject reason, and no item in the discarded sample
judged wrongly excluded two weeks running.

### 2.17 Image handling — **[decided in v1.4.2]**

CDN URLs carry `oh=`, `oe=` and `_nc_ohc=` signing parameters and expire. Linking is not an
option; the original image is downloaded and served locally. Policy and rationale in
`PROJECT_HANDOVER.md` §2.15. What the pipeline must do:

- Download on first ingestion, store at **card resolution**, not original size.
- Fields: `image_local_path`, `source_image_url`, `image_fetched_at`, `image_removed`
  (boolean, default false), `image_credit` (organiser name as displayed).
- **Never re-derive the pre-hash from the CDN URL.** The signing parameters change on every
  fetch, so a URL-sensitive `source_hash` reports a change on every run. Normalise the URL
  out of the hash, as already specified in §2.2.
- `image_removed = true` falls back to the generated card. **It does not delete the
  article** — flag, never delete, as everywhere else.
- Skip watermarked or obviously commercial stock assets. This is a judgement the editorial
  classifier already makes on the item as a whole; an item classified `promotion` never
  reaches image download anyway.
- **The generated card is not optional.** `no_image` fires on roughly 10% of records
  (flag-only, does not block publication), and the same card is what `image_removed`
  falls back to. Title, date, neighbourhood, consistent styling.

---

## 3. Convergence of the two workflows

The Posts sub-workflow writes a flat record to **Google Sheets**; the Events pipeline
writes canonical JSON to **Drive** with `content_id`, `source_hash` and revisions. Time
formats diverge too: `start_date` + `time` as separate strings without timezone, versus
`start_at_utc`.

Two corpora with no shared identity cannot feed the same page.

Both should write the canonical JSON contract, with `source_channel` distinguishing
`fb_event` from `fb_post`. This is cheapest to do now, while the corpus is small — and
since posts are the channel that reaches small local organisers, this is not the secondary
branch.

The shared gazetteer (`gazetteer.json`) is the precondition: one source for the prompt
list, the validation, the alias lookup and the site grouping. `venues.json` sits beside it
with a different lifecycle, and `build_gazetteer.py` is the only thing that writes the
generated files.

**One structural note for the posts channel**, worth knowing before it is started rather
than during: `location.id` does not exist on a post, so the venue registry — the highest
cost-benefit layer in the events chain — has no counterpart. What a post does carry is the
**publishing page**, and a page is almost always tied to one area: the parish on via X
posts about via X. A **page registry** keyed on page id, resolved once by a person, is the
deterministic layer that replaces the venue registry there, and it probably covers the
majority of posts without an AI call.

---

## 4. Spec changes required for v2.4

1. Geography section replaced by `PROMPT_GEO_BLOCK.md` (§1.1, §2.13).
2. `geo_verification_status` enum with `human_verified`, plus the stickiness and conflict
   rules (§2.1).
3. `publication_zone_id` and `neighbourhood_id` on the Firestore registry (§2.2).
4. Recurring-event contract: series + `occurrences[]` (§2.5).
5. Refresh policy replacing the pre-Apify blocklist (§2.8).
6. Venue registry as a separate store (§2.11).
7. Reject-reason enum extended, with layers (§2.12).
8. `discovery_strategy: manual_url_collection` recorded as a first-class field (§2.9).
9. Part I §8: the position on platform terms. **No longer a placeholder** — the text is in
   `PROJECT_HANDOVER.md` §2.16 and should be pasted in verbatim.

Four more for v2.4, from v1.3:

10. `duration` parser plus the `date_precision` field, and `next_occurrence` on series
    (§2.4, §2.5).
11. The editorial classification pass, its three fields and its two new reject codes
    (§2.14).
12. `geo_level` on every item, and the statement that the layout falls back at render time
    (§2.15).
13. The review queue schema and the weekly two-sample review (§2.16).

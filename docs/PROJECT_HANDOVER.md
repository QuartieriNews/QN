# Quartieri News — Events Module: Project Handover

**Date:** 21 August 2026 · **Release version:** see `START_HERE.md`
**Purpose:** carry the decisions and evidence from a long working session into a fresh
conversation, without carrying the conversation itself.

Read this first. `PROJECT_VISION.md` explains what the whole thing is for and why several
decisions here look the way they do. `SOURCE_DATA_FINDINGS.md` holds the measured evidence,
and `WORKFLOW_FIXES.md` the concrete defect list. The gazetteer files are the deliverable.

**What changed in v1.4:** an external review of the v1.3 package found four blocking
defects and a dozen smaller ones. All are fixed; see `CHANGES_v1.4.md` and §3.4. The most
serious were self-inflicted in v1.3, not inherited: the editorial filter ran its exclusion
last and could never reach it, and the name/coordinate guard rejected valid Rome venues.

**What changed in v1.3:** the events module is one block of four on each neighbourhood
page, and this revision makes that explicit (§1, §2.12). The editorial filter now has a
rule (§2.13). The review queue has an address and a definition of done (§2.14). Six defects
found on review of the v1.2 package are fixed (§3.3). See `CHANGES_v1.3.md` for the diff.

---

## 1. What this module is

Automated collection of public events in Rome from Facebook, enriched and published across
**89 neighbourhood pages** covering all 15 municipalities.

**Events are one block of a neighbourhood page, not the page.** Three more are planned —
municipal and city-council assemblies, local news, and conversation from neighbourhood
Facebook groups — and what each page displays is decided at **layout time**, from stored
fields, not at ingestion. Two consequences run through the rest of this document:

- A page is not empty because its events block is thin. The old framing of the
  distribution risk (§5.1) was sharper than the real one.
- Every item must carry enough for the layout to choose later: `geo_level`,
  `content_type`, `editorial_class` and a freshness field. One field each, and none of them
  retrofittable.

The blocks have deliberately different geographic natures. An event has an address; a
municipal commission is municipality-level **by nature** and must not be given an invented
neighbourhood. `geo_level` exists so a thin page can borrow coarser content at render time
without anything being relabelled as more precise than it is.

`PROJECT_VISION.md` carries the full picture and the parts that are not yet decided.

Two ingestion channels feed one corpus:

- **Facebook Events** — the structured event objects, via an Apify actor.
- **Facebook Posts** — events announced as ordinary page posts and never created as
  Facebook Events. A separate n8n sub-workflow reads a curated list of pages.

They currently write different schemas to different stores. Convergence on one canonical
JSON is the main outstanding architectural task.

---

## 2. Decisions taken, and why

### 2.1 Scope is all of Rome, first phase

15 municipalities, 89 published pages. Not a Municipio X pilot.

*Consequence:* geography coverage becomes the binding constraint — every unresolved event
is an event that appears on no page at all. The neighbourhood-level list (440 rows) is too
fine for the model; the site only needs the 89 zones.

### 2.2 Geography is resolved by the model, directly to the publication zone

Deterministic geocoding (street register, polygons, point-in-polygon) was evaluated and
**deliberately deferred**. Rationale: 89 coarse areas is a much easier question than 250
toponyms, and the approach was tested informally with acceptable results.

*Guardrails that were kept*, because they are numeric comparisons rather than geometry:
Rome bounding box, centroid blocklist, `placeType: CITY`, name/coordinate contradiction.
All four live in `gazetteer.json → guards`.

*Reopen this decision if* the weekly sample (§2.4) shows zone accuracy materially below
95%. The street register of Roma Capitale is open data and remains the fallback.

### 2.3 Discovery is a manual weekly task

Apify's search-based discovery proved unreliable for this purpose. Keyword search returns
Rome NY and Rome GA; the anonymous `explore` feed is ranked by popularity and skews to
large commercial and tourist events.

**The chosen model:** open Facebook Events while logged in, set the location and a **30-day
custom date range**, scroll, and run a console snippet that collects the event URLs into a
Google Sheet. Apify then extracts from those direct URLs, which produce markedly better
data (§ findings).

**Cadence, decided in v1.4.2: one to two times a week, more often in busy periods** —
September, the run-up to Christmas, spring — always covering roughly the month ahead. Not a
fixed weekly ritual: supply is seasonal and the collection should follow it.

**Collection and refresh are independent, and the cost follows the refresh.** Collection
discovers *new* events; a higher cadence finds them sooner, and those are events that would
have been billed anyway a few days later. Refresh re-extracts events already on the list
and runs on the TTL schedule (§2.6) regardless of when a person last collected. So moving
from once to twice a week adds close to nothing.

The dependency runs the other way round, and it is worth stating plainly: *without* the TTL
every run resends the whole list to Apify, and then — and only then — does cadence multiply
the bill directly. The TTL is what decouples the two.

One reason the higher cadence earns its place, beyond preference: an event published three
days before it happens is the one a weekly collection is most likely to miss altogether.
Those are also the events a reader most needs. The refresh TTL cannot help there — it only
watches URLs already known — so late-published events are a *discovery* gap, and collection
frequency is the only thing that closes it.

This is a deliberate division: **discovery is human, extraction is automatic.** It is not a
stopgap. It should be recorded in the spec as `discovery_strategy: manual_url_collection`,
with `collected_at` per batch and a run-report warning when the last collection is stale —
staleness threshold **10 days**, loose enough not to nag at the lower cadence and tight
enough to catch a genuinely missed period.

*Not chosen:* an agent that logs into Facebook and collects URLs automatically. That is
authenticated automation, prohibited by the platform terms, and the account at risk is a
personal one. The position on source terms is written down in §2.16.

*Kept as a low-cost safety net:* `explore/it-rome` in parallel, so a missed week still
yields something.

### 2.4 Review targets the reject queue, not the publication queue

Not every published article is read. Instead:

- Items that **fail** a check land in a reject queue with a structured `reject_reason`.
- Those are reviewed, and each fix goes **into the gazetteer as an alias, or into the venue
  registry as a `location.id` record**, not into the individual item — so the cost of
  debugging falls over time.
- A human-set zone carries `human_verified` and survives recomputation (§2.7).

**Plus 20 randomly sampled published items per week, from the first published week.** The
reject queue shows false negatives only. Events published on the wrong page do not block,
because the system is confident. The weekly sample is the only sensor for those.

### 2.5 Cost model

Apify charges **per event returned, not per new event**. A 30-day window collected weekly
re-bills the same event roughly four times. Measured reference: 107 events cost 1.40 $ at
the 13 $/1,000 base rate.

The filter that avoids re-billing known events is load-bearing — but it is a **throttle,
not an exclusion** (§2.6).

### 2.6 The pre-Apify filter is a refresh TTL — *new in v1.2*

*Known → never scrape again* would have saved the money and broken the corpus: Facebook
events get postponed, moved, cancelled and re-priced, and a URL that is never re-fetched
can never produce a new `source_hash`. A permanent skip disables the only mechanism that
notices change.

Replaced by a TTL that tightens as the event approaches — 24h inside three days, 72h inside
a week, weekly beyond that — plus a permanent skip once an event has ended, which is where
most of the saving actually comes from. Missing on refresh is a flag, never a delete. Full
policy in `WORKFLOW_FIXES.md` §2.8.

### 2.7 `human_verified` ships in the first version — *new in v1.2*

A person's decision must survive every recomputation, including a `geo_logic_revision`
bump. Precedence: `human_verified > venue_registry > alias > ai`. A later lookup that
disagrees sets `geo_conflict = true` and is logged; it never overwrites. Contract in
`WORKFLOW_FIXES.md` §2.1.

### 2.8 The geographic double pass is conditional — *new in v1.2*

Two independent passes stay, and are spent where they earn their cost: one pass when
`geo_basis` is `explicit_address` or `explicit_zone`, two when it is `inferred` or
`unknown`, or when there was no venue hit and no street address. Disagreement is a reject
(`ai_disagreement`), not a tiebreak. Promote to always-double if the weekly sample shows
single-pass accuracy below 95%. Table in `PROMPT_GEO_BLOCK.md`.

### 2.9 Recurring events: one article, many occurrences — *new in v1.2*

11% of the sample carries `hasChildEvents`, up to 52 occurrences. The representation is one
canonical article per series with an updatable `occurrences[]` array, a series-level
`content_id`, and `effective_end` taken from the last non-cancelled occurrence. Schema in
`WORKFLOW_FIXES.md` §2.5.

### 2.10 The venue registry is a separate store — *new in v1.2*

`location.id` resolves a venue once and forever. It lives in `venues.json` / Firestore,
**not** inside `gazetteer.json`, because the gazetteer is regenerated from the workbook and
a merge would erase everything the system has learned. `GAZETTEER_README.md` §9.

### 2.11 The neighbourhood level is stored when it is known — *new in v1.2*

The model still chooses among 89 zones only. But when the finer level is known
deterministically — venue registry or alias match — both `publication_zone_id` and
`neighbourhood_id` are stored. It costs one field today and it is what maps, search and any
future sub-page will need.

### 2.12 `geo_level`, and the fallback happens at render time — *new in v1.3*

`neighbourhood` · `zone` · `municipality` · `city`, set by the ingesting block, never by the
model. A page short of zone-level content pulls municipality-level content to fill the
block — a rendering decision taken from stored fields. **An item is never re-resolved to a
coarser zone**, because that would write a false fact into the corpus to solve a display
problem.

### 2.13 The editorial filter has a rule — *new in v1.3*

`not_an_event` sat in the reject enum from v1.1 with nothing that could produce it, while
the sample contained photo shoots, tours and cruises.

The discriminator is **not** recurrence. A pub's Thursday karaoke and the same pub's gig by
a named band are both recurring-venue content and only one is an event; a weekly market and
a monthly committee meeting recur and are among the most valuable items on the site. The
test is whether the item has **identified content** — a band, an author, a title, a theme —
with substitutability and explicit promotion as secondary tests. Price is not a criterion
in either direction.

Three fields returned by a separate pass: `editorial_class`, `editorial_basis`,
`content_type`. `uncertain` is permitted and produces a queue item, not a discard.
`venue_nature` is context passed to the classifier, not a shortcut past it — a permanent
verdict on a neighbourhood pub would discard its real gigs.

Filter **wide** at first: in a low-density area a strict filter empties the block, and a
wrongly excluded event is invisible. Full rule and prompt in `EDITORIAL_FILTER.md`.

### 2.14 The review queue has an address, and the block has a definition of done — *new in v1.3*

One Google Sheet, two tabs, one row per item, a `block` column and filter views — not one
tab per block, which is four schemas that diverge on the first field added to one of them.
Four editable columns; `fix_target` among them, because *every fix goes into the gazetteer,
not into the item* otherwise has nowhere to happen. Decided rows are archived by the
workflow, never deleted: that archive is the only record of human judgement in the system.

**Weekly: 20 published items and 10 discarded ones.** The second sample is new, and is the
only sensor the editorial filter has — the queue shows what was excluded, never what was
excluded wrongly.

**Done** = two consecutive non-August weeks at or above 95% zone accuracy on the published
sample, a stable and understood top reject reason, and nothing in the discarded sample
judged wrongly excluded two weeks running. Written down now so the move to the posts
channel is not decided on a feeling. Schema in `REVIEW_QUEUE.md`.

---

### 2.15 Images are archived and republished — *decided, v1.4.2*

Facebook CDN URLs carry signing parameters that expire, so a linked image becomes a broken
image within weeks. The decision is to **download and serve a local copy of the original
event image**, accepting the copyright exposure that comes with it.

*This is a knowing risk, not an oversight.* The image belongs to the organiser or their
photographer. In practice objections to a local news site republishing an event flyer are
rare, and most aggregators operate the same way — but a due-diligence lawyer will raise it,
and earlier than the platform-terms question, because it is easier to see. It should be
presented as a considered trade-off rather than discovered.

**Five mitigations, all cheap, all required.** They do not remove the exposure; they make
the position defensible and make removal instant.

1. **Always credit and link.** Organiser name visible on the card, and a link to the source
   event on every item. An unattributed copy is a much worse position than an attributed one.
2. **Store provenance.** `source_image_url` and `image_fetched_at` on every item, so any
   image can be traced to what it came from and when.
3. **Serve reduced resolution.** Card-sized, not the original file. Use at thumbnail scale
   interferes far less with whatever market the image has.
4. **A takedown route that works.** A visible contact address, and an `image_removed`
   boolean on the item — removal sets a flag and falls back to the generated card, it does
   not delete the article. One field, and a request is honoured in minutes.
5. **Skip the obvious traps.** Watermarked images, stock photography, and anything that is
   clearly a commercial promotional asset rather than an event flyer.

*Reopen this if* a takedown request arrives, or before any funding round — at which point
the fallback already exists in mitigation 4: a generated card with title, date and
neighbourhood. Building that fallback is not optional, because it is also what shows on the
10% of records that have no image at all.

### 2.16 Position on sources — *decided, v1.4.2*

The specification's Part I §8 placeholder is filled. The position, in full:

> Quartieri News collects publicly visible event information from Facebook. Event URLs are
> gathered manually by a person, one to two times a week and more often in busy periods,
> covering roughly the month ahead. No automated agent logs into the platform and no
> authenticated automation is used. Extraction runs on those URLs through a third-party
> service. Every item credits its organiser and links back to the source. Source data is
> not resold or redistributed as a dataset. Removal requests are honoured on receipt via
> the contact address published on the site.

Short, accurate, and enough. An investor finding an empty placeholder here assumes the
worst; one finding three defensible paragraphs moves on.

## 3. Corrections to the v1.1 package

### 3.1 Documentary inconsistencies, now resolved

**Open questions.** The previous handover listed the seven open items as Colle del Sole,
Sallustiano/Ludovisi, five Municipio X toponyms and Agro Romano. The `open_questions` sheet
says something else, and the sheet is right. The authoritative list:

1. Trionfale — a marginal portion borders Municipio I; confirm the single assignment or
   populate `spans_municipalities`.
2. Colle del Sole (Municipio VI) — confirm the place exists as recorded.
3. Colle del Sole (Municipio XI) — same. Until then it is the one ambiguous lookup key in
   the whole gazetteer.
4. Agro Romano — `is_page = false`. Split per municipality, or keep as a catch-all?
5. The five Municipio X toponyms with no official ZU code: Giardino di Roma, La Lingua,
   Madonnetta, Stagni di Ostia, Lido di Castel Fusano.
6. Trigoria / Laurentino / Maglianella — marked `resolvable = false` by analogy with Acilia
   and Ostia. Confirm, or set back to true.
7. `municipality_code` normalisation to Roman numerals — confirm.

**Sallustiano and Ludovisi are not open.** They were corrected (to Esquilino-Termini and
Centro Storico respectively) and appear on the `corrections` sheet with
`status = corrected`.

**Master file.** Two workbooks held the same data and both looked editable — and had
already diverged on the name of the key column (`neighbourhood_id` in English,
`neighborhood_id` in Italian). Resolved: `Rome_Neighbourhood_Gazetteer_EN.xlsx` is the
master, `Mappa_Quartieri_Normalizzata.xlsx` is a read-only export, both carry a first sheet
saying which is which, and `build_gazetteer.py` regenerates the derived files.

### 3.2 Defects found in the v1.1 package

1. **The prompt list contradicted the validator.** The 89 values were formatted
   `Acilia  (Municipio X)` while the validation code compared against `Acilia`. A model
   obeying *use the exact spelling from the list* would have been rejected. The list is now
   generated from `gazetteer.json` and carries names only.
2. **The gazetteer joined on a display name**, violating its own invariant I2.
   `publication_zone_id` added to every row.
3. **29 neighbourhoods map to a zone that is not a page** (28 Agro Romano, 1 Other). A
   correct alias hit on Corcolle or Fiorano produced a real place with nowhere to publish,
   and would have been counted as `zone_not_in_list` — a false reading at the top of the
   weekly queue. New code: `zone_not_published`.
4. **`resolvable = false` was ambiguous.** Acilia, Ostia, Monteverde, Laurentino and
   Trigoria are containers as neighbourhoods *and* valid publication zones. Read
   literally, invariant I1 would have rejected *ad Acilia* — the commonest phrasing in
   Municipio X. Now stated explicitly as I1b.
5. **Booleans were strings.** `is_page` and `resolvable` were `"TRUE"` / `"FALSE"`; they
   are real booleans in v1.2. Any code comparing against `"TRUE"` must be updated.
6. **Ambiguity had no defined behaviour.** Colle del Sole matched two neighbourhoods with
   different pages and the lookup would have taken the first. Now `ambiguous_alias`, and
   the build fails if a new ambiguous key appears undeclared.

### 3.3 Defects found in the v1.2 package

1. **`zone_not_published` was checked where it could never fire.** The validator tested the
   model's output against the page list — but the model is only ever given the 89 pages, so
   it cannot return Agro Romano. The real case is an alias hit on Corcolle or Fiorano, at
   step 3. The check moved to the lookup.
2. **A guard with no reject code.** `countryCode` null with coordinates said *route to the
   reject queue* and named no reason, so it landed under some other code and corrupted the
   weekly sort — the number the week's work is prioritised on. Now `country_code_missing`.
3. **A guard with no implementable rule.** §4 called all four guards numeric comparisons;
   `name_coord_mismatch` requires knowing that "Waterloo" is not in Rome. It now has a
   comma-tail allowlist, plus the clause that any tail which is itself a gazetteer key
   passes — without which `"Palazzo dei Congressi, EUR"` was rejected in testing.
4. **A reject code with no rule.** `not_an_event` could not be produced by anything. See
   §2.13.
5. **The `duration` parser was declared necessary and never specified**, leaving the defect
   it was meant to close still open — a three-day sagra finishing after day one. Parser,
   plus `date_precision = start_only` for the 45 of 107 records with no duration at all,
   in `WORKFLOW_FIXES.md` §2.4.
6. **The build's ambiguity check was narrower than the runtime index.** It covered
   neighbourhood names and aliases; the index also holds 91 zone display names. A future
   collision would have passed the build and become a silent coin flip. (No such collision
   exists today.)

Two smaller ones, fixed in the same pass: the MASTER sheet claimed `build_gazetteer.py`
regenerated the Italian export and it did not — it now does, with `it_strings.json` as the
translation memory, verified row-for-row against the hand-built file; and
`zone_distribution.py` guarded free-text matching with a `len < 5` rule that excluded EUR
and AXA while still admitting *prati*, *talenti* and *marconi*.

---

### 3.4 Defects found in the v1.3 package

Four blocking, found by an external review and confirmed by running the code.

1. **`venue_unresolved` had two incompatible meanings.** `WORKFLOW_FIXES` said a registry
   miss *is* the reject; the resolution order says a miss continues to the alias lookup and
   the model. With `location.id` present in 106 of 107 records, the first reading queues
   essentially the whole corpus on day one. Now terminal: it fires only when the registry,
   the alias lookup and the model have all failed.
2. **The editorial filter ran its exclusion last.** `explicit_promotion` sat after
   `identified_content`, and most promotions carry a company, a title and a theme —
   *"Rome Sunset Photography Experience by XYZ"* stopped at test 1 as `local_interest`. The
   exclusion is now a gate that runs first. This one was introduced in v1.3.
3. **The name/coordinate guard rejected valid records.** It read the text after the last
   comma of `location.name` as a geographic tail, but that field is a venue name and the
   tail is usually a room or a floor: `"Teatro Argentina, Sala Squarzina"` was rejected.
   Split into an allowlist on `location.city` and a whole-segment blocklist on
   `location.name`. Also introduced in v1.3.
4. **`geo_level = municipality` was not routable.** The stored contract had no
   `municipality_code`, so an item with an empty zone could not be placed on Municipio VII
   rather than X — a rule with no output field, and a corpus migration once the
   institutional block exists.

And, in the same pass: the guards now run in two tiers so a registry-resolved venue is not
blocked by a suspicion signal; `verification_status` renamed to `geo_verification_status`
in the double-pass reconciliation; the build and the runtime now share one normalisation
function, so I7's guarantee is real; `zone_not_published` propagated to the two documents
that still called it a validation failure; reject reasons carry `blocks_publication`;
`no_description`, `no_image` and `duplicate_suspected` given producing rules or marked
flag-only; online events given one deterministic rule instead of three contradictory
mentions; and the invented "8–12 dates" community-series range withdrawn.

**The lesson worth keeping**, beyond the individual fixes: v1.3's verification section
listed only tests where a guard fired correctly. `test_guards.py` now tests both
directions, and its negative half immediately caught a second-order version of the same bug
— the first replacement rule rejected `"London Pub"`.

## 4. Deliverables in hand

| File | Status |
|---|---|
| `Rome_Neighbourhood_Gazetteer_EN.xlsx` | **Master.** 440 neighbourhoods, 91 zones (89 pages), 102 corrections, 7 open questions, `publication_zone_id` added. |
| `Mappa_Quartieri_Normalizzata.xlsx` | **Export.** Italian metadata, read-only. |
| `build_gazetteer.py` | Regenerates the JSON, the prompt list and the Italian export. Fails the build on a broken invariant. |
| `test_guards.py` | **New in v1.4.** Guards and matching, tested in both directions. The negative half is the one v1.3 was missing. |
| `gazetteer.json` | Data plus `resolution` (precedence, order of operations, double-pass, lookup), `guards` in two tiers, `editorial`, `review`, `reject_reasons` with layers and `blocks_publication`. |
| `venues.json` | New. Venue registry schema keyed on `location.id`, separate lifecycle. |
| `prompt_list_publication_zones.txt` | Generated. 89 values, names only. |
| `PROMPT_GEO_BLOCK.md` | Prompt, resolution order, online rule, conditional double pass, validation code. |
| `GAZETTEER_README.md` | Data model, eight invariants, resolution order, operating model, venue registry. |
| `START_HERE.md` | **Read first.** Release manifest, reading order, and the five things that must not be got wrong. |
| `sample_107_direct_urls.json` | The raw Apify sample. Input for `zone_distribution.py` and for the editorial calibration. |
| `zone_distribution.py` | Per-zone event count on a sample — run it first. Three match tiers: `exact`, `field_contains`, `text_contains`. |
| `SOURCE_DATA_FINDINGS.md` | Unchanged. Measured behaviour of the Apify actor. |
| `WORKFLOW_FIXES.md` | Defect list plus the thirteen spec changes for v2.4. |
| `PROJECT_VISION.md` | **New.** What the project is for, the four blocks, and what is not yet decided. |
| `EDITORIAL_FILTER.md` | **New.** What counts as a locally useful event, with the prompt. |
| `REVIEW_QUEUE.md` | **New.** The Google Sheet schema and the definition of done. |
| `it_strings.json` | **New.** English → Italian translation memory for the export. |
| `CHANGES_v1.2.md` | What changed against the v1.1 package. |
| `CHANGES_v1.3.md` | **New.** What changed in this revision and what breaks. |

The spec document (`Quartieri News FB Events Workflow Specification v2.3`) has **not** been
updated. `WORKFLOW_FIXES.md` §4 lists the thirteen changes it needs.

---

## 5. Open questions

Ordered by how much they block other work.

1. **Distribution across the 89 pages.** Across three samples, supply was heavily
   concentrated in Municipio I and II. **Measurable today**, with `zone_distribution.py` on
   the existing 107-event sample. Read the `exact` column as a floor and the total as a
   ceiling: only `exact` matches what the production resolver does, and a distribution that
   holds up only on free-text matches is not one to plan around.

   Reframed in v1.3: with four blocks per page this is no longer "is the site viable",
   it is "at what threshold does the events block fall back to municipality level". Still
   worth measuring first, and still cheap — but it now calibrates a parameter rather than
   gating the project. Note also that the sample is from mid-August; the thresholds
   themselves should be set on a normal week, not this one.

3. **The seven gazetteer open questions** — listed in §3.1 above. Only Colle del Sole
   blocks anything technical: until it is resolved, one lookup key is ambiguous by design.

4. **Automated review agent.** Discussed, not decided. If added, it should run *after* the
   deterministic checks, be allowed to return `uncertain`, flag rather than rewrite, and
   record `review_agent_revision` in the JSON. It roughly doubles the AI cost per article —
   and the conditional double pass (§2.8) already spends part of that budget where the
   errors are.

5. **How courses are displayed.** A ten-lesson course is neither promotion nor an event in
   the ordinary sense. `content_type: course` exists so the decision can be taken later on
   a corpus that still contains them; nothing else about them is decided.

---

## 6. Principles carried over from the spec

The original spec's philosophy held up under scrutiny and should be preserved:

- Shortcuts belong in the pipeline, never in the stored data.
- A null is better than an invented value.
- A rule with no output field is not a rule.
- Deferred capabilities are documented, not deleted.
- **A filter that removes things must be sampled, not just logged** *(new in v1.3)*. A
  reject queue shows what was blocked. It cannot show what was blocked wrongly, and it
  cannot show what was published wrongly. Only sampling shows either — which is why the
  weekly review has two samples and not one.

The place the v1.1 implementation violated this — `NEVER leave municipio, urban_zone, or
neighborhood empty` — is removed in `PROMPT_GEO_BLOCK.md`. A fifth principle earned its
place in v1.2: **one master, generated copies**. A hand-edited derivative is a second master
that nobody declared.

---

## 7. Suggested next steps

0. **Run `zone_distribution.py` on the 107-event sample.** Ten minutes, costs nothing, and
   exercises the script. Read the `exact` column as a floor. It does **not** calibrate the
   fallback threshold — that needs a normal week, as §5.1 says; v1.3 claimed both things in
   two different places.

0b. **Calibrate the editorial filter on 30 hand-classified items** from the same sample
   before wiring it in (`EDITORIAL_FILTER.md`). Half a day, and the disagreements are the
   examples that go into the prompt.
1. Apply the prompt replacement and the validation code (`PROMPT_GEO_BLOCK.md`), including
   the conditional double pass.
2. Fix the six defects in the Posts sub-workflow (`WORKFLOW_FIXES.md` §1).
3. Implement the refresh TTL in place of the pre-Apify blocklist (§2.8).
4. Add the venue registry lookup on `location.id` (§2.11). Cheap infrastructure whose
   payoff must be measured over months rather than assumed — earlier revisions called it
   the highest-leverage item remaining, and the measured repeat rate does not support that.
   See `SOURCE_DATA_FINDINGS.md` §9.1.
5. Implement `human_verified` with the stickiness and conflict rules (§2.1).
6. Implement the recurring-event contract (§2.5).
7. Implement the editorial classification pass and its two new reject codes
   (`WORKFLOW_FIXES.md` §2.14).
8. Build the review sheet and the write-back workflow (`REVIEW_QUEUE.md`). Nothing above is
   measurable until this exists.
9. Update the spec to v2.4 with the thirteen changes in `WORKFLOW_FIXES.md` §4.

0 and 0b are immediate. 1–4 are independent and can proceed in parallel. 8 should not be
left until last: it is the only thing that turns any of the rest into a number.

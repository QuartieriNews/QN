# Changes — v1.2 → v1.3

20 August 2026. What was changed in the handover package, why, and what breaks.

---

## Breaking changes

Two. Anything written against v1.2 must be updated.

| # | Change | What breaks |
|---|---|---|
| 1 | `zone_not_published` moved from post-model validation to the alias lookup | Code that only tests the model's output for a non-page zone never fires. The real case — an alias hit on Corcolle, Fiorano, Torricola — falls through to the model and is logged as `zone_unknown`, hiding a case that has its own counter for a reason (I6). |
| 2 | Three new reject codes: `country_code_missing`, `commercial_routine`, `editorial_uncertain` | Any consumer with a closed enum of reject reasons rejects or drops these. The weekly sort must include them or it under-reports. |

Non-breaking but worth knowing: `Mappa_Quartieri_Normalizzata.xlsx` is now **overwritten**
by `build_gazetteer.py`. It was already documented as read-only; from v1.3 that is enforced
rather than requested.

---

## 1. Context that reframes the package

The events module is **one block of four** on each neighbourhood page — alongside municipal
and city-council assemblies, local news, and conversation from neighbourhood groups — and
what a page displays is decided at **layout time**, not at ingestion.

This does not change the pipeline. It changes two readings of it:

- The distribution risk (§8 of the README) was framed as *is the site viable with 89
  pages*. With four blocks it is *at what threshold does the events block fall back to
  municipality level* — a parameter, not a gate.
- Every item must now carry enough for the layout to choose later. Hence `geo_level`,
  `content_type`, `editorial_class` and `date_precision`: one field each, none of them
  retrofittable onto a corpus already collected.

`PROJECT_VISION.md` is new and carries this whole picture, including what is deliberately
not decided yet.

---

## 2. Defects fixed

**2.1 `zone_not_published` was checked where it could never fire.** The validation code
tested the model's returned zone against the page list. The model is only ever given the 89
pages, so it cannot return `Agro Romano`. The case that actually occurs is an alias hit at
step 3 on one of the 29 neighbourhoods that route to a non-page zone. Moved to the lookup,
with the code in `PROMPT_GEO_BLOCK.md`. The post-model check stays as a belt-and-braces
guard in case the prompt list is ever built from the wrong filter.

**2.2 A guard with an action and no reject code.** `country_code_null_with_coordinates`
said *route to the reject queue* and named no reason. In production that item lands under
whatever code follows, corrupting the weekly sort — which is the one number the week's work
is prioritised on. Now `country_code_missing`.

**2.3 A guard with no implementable rule.** README §4 described all four guards as numeric
comparisons. `name_coord_mismatch` requires knowing that "Waterloo" is not in Rome, which
is not arithmetic. The rule is now: take the text after the last comma in `location.name`
or `location.city`, normalise, and accept it only if it appears in `accepted_tails` **or is
itself a gazetteer lookup key**.

An allowlist rather than a blocklist, because a list of foreign toponyms is unbounded and
fails open. The second clause was added after testing: `"Palazzo dei Congressi, EUR"` has
the tail `EUR`, which is a publication zone, and the allowlist alone rejected it.

**2.4 A reject code with no rule.** `not_an_event` has been in the enum since v1.1 with
nothing that could produce it, while the measured sample contained photo shoots, guided
tours and cruises. A reject code with no rule is a counter that stays at zero while the
thing it names goes to the page. See §3.

**2.5 The `duration` parser was declared necessary and never specified.** That left the
defect it was meant to close still open — a three-day sagra treated as finished after day
one. Now specified, with the second decision that was missing: `duration` is null in **45
of 107** records, so a missing duration must not reject. `date_precision = start_only`
records that the end time is an assumption, so the layout does not hide the item at
midnight. A present-but-unparseable duration still rejects, because that one is a signal
the parser needs extending.

**2.6 The build's ambiguity check was narrower than the runtime index.** It covered
neighbourhood names and aliases; the runtime index also contains the 91 zone display names.
A future collision between a zone name and an unrelated neighbourhood would have passed the
build and become a silent coin flip, against I7. Now checked across all three key spaces.
No such collision exists today — `Colle del Sole` remains the only ambiguous key either way.

**2.7 Free-text matching was guarded by key length.** `zone_distribution.py` skipped keys
shorter than five characters. That excluded `EUR` and `AXA` — two real zones, one of them
in Municipio X — while still admitting `prati`, `talenti`, `marconi`, `morena` and
`centro storico`, which are ordinary Italian words, a price token and a surname. The false
positives landed in the one number meant to decide a product question. Replaced by
`free_text_stoplist` plus two-tier matching, and new invariant **I8**.

**2.8 The MASTER sheet described a build step that did not exist.** It has said since v1.2
that `build_gazetteer.py` rebuilds the Italian export. It did not, and the two workbooks had
already diverged once — on the name of the key column. The script now generates it, with
`it_strings.json` as a hand-maintained translation memory, and reports any string it could
not translate instead of silently emitting English. The regenerated file was verified
identical row-for-row to the hand-built one before this was adopted.

---

## 3. The editorial filter — new

Full rule, prompt and calibration procedure in `EDITORIAL_FILTER.md`; contract in
`gazetteer.json → editorial`.

**Recurrence is not the axis.** Filtering on `hasChildEvents` catches a pub's Thursday
karaoke and misses the same pub's Friday DJ published as a one-off — identical in nature.
In the other direction it discards the weekly farmers' market, the monthly committee
meeting and the library reading group, which are among the most valuable items on the site
precisely because a reader can *use* a standing appointment.

**The test is identified content.** A proper noun or a specific subject — a band, an
author, a title, a theme. A named band in a neighbourhood pub is an event, free entry or
not, and whether or not that pub books a band every Friday. Substitutability and explicit
promotion are secondary tests. **Price is not a criterion in either direction**; `paidContent`
was false on all 187 measured records including a ticketed concert.

Three fields from a **separate pass** — not merged with geography, so the two error rates
stay countable (I5): `editorial_class`, `editorial_basis`, `content_type`.

`uncertain` is a permitted answer and produces a queue item, not a discard, for the same
reason an empty `publication_zone` is permitted: a classifier that always decides produces
nothing to review, only silent errors.

`venue_nature` is added to the venue record as **context passed to the classifier, not a
shortcut past it**. A neighbourhood pub hosts both its ordinary programming and real gigs; a
permanent verdict on the venue discards the gigs. Only an explicit `editorial_override` —
`whitelist` for community venues, `blacklist` earned by three promotions — skips the call.

**Start wide.** In a low-density area a strict filter empties the block, and a wrongly
excluded event leaves no trace. Tighten only on evidence from the published sample.

---

## 4. The review queue — new

`REVIEW_QUEUE.md`; contract in `gazetteer.json → review`.

The operating model has always said *review the reject queue*. It never said where, which
made it the part of the architecture most likely not to get built.

**Google Sheets**, chosen against Notion and against a custom interface on three
constraints: one reviewer, twenty minutes a week, often from a phone. The deciding reason is
that the sheet is the same medium in which the fix is applied — the gazetteer master is a
workbook, so a missing alias is a cell, not a bridge to build.

**One tab with a `block` column and filter views, not one tab per block.** Four tabs is four
schemas that diverge on the first field added to one of them, four write nodes and four
read-back workflows.

The structural fix differs by block — `alias`/`venue` for events, `page → area` for posts,
nothing for institutional items — which is the one thing that would have broken a shared
schema. Resolved with four generic `fix_target` values and the detail in free text.

Load-bearing details: the queue tab is never sorted in place (the write-back matches on
`content_id`); decided rows are **archived, never deleted**, because that archive is the only
record of human judgement in the system and the only dataset the editorial filter could ever
be evaluated against; `decided_at` distinguishes *undecided* from *decided and not written
back*.

**The weekly sample gains a second half: 10 discarded items** alongside the 20 published
ones. The editorial filter fails in the one direction the queue cannot show — it records
what was excluded, never what was excluded wrongly. A parish sagra at the oratory bar,
classified `commercial_routine`, simply disappears.

**Definition of done for the events block**, written before the work starts: two consecutive
non-August weeks at or above 95% zone accuracy on the published sample, a stable and
understood top reject reason, and nothing in the discarded sample judged wrongly excluded
two weeks running.

---

## 5. New fields

| Field | Where | Why |
|---|---|---|
| `geo_level` | every item | `neighbourhood`/`zone`/`municipality`/`city`. The layout's fallback ladder. Set by the block, never by the model. |
| `editorial_class` | every item | `local_interest`/`commercial_routine`/`promotion`/`uncertain` |
| `editorial_basis` | every item | Why the classifier decided. Makes the queue sortable by cause. |
| `content_type` | every item | `event`/`recurring_appointment`/`course` |
| `date_precision` | every item | `exact`/`start_only`. Whether the end time is known or assumed. |
| `next_occurrence` | series | Derived. Without it a 52-occurrence series either pins to the top of the block forever or never appears. |
| `venue_nature` | venue record | Context for the classifier. |
| `editorial_override` | venue record | `none`/`whitelist`/`blacklist`. The only venue-level shortcut. |
| `promotion_count` | venue record | How a blacklist is earned rather than assumed. |

---

## 6. New files

| File | Why |
|---|---|
| `PROJECT_VISION.md` | The non-technical picture: what the project is for, the four blocks, the operating philosophy, and an explicit list of what is decided, what is open and what has not been thought about yet. |
| `EDITORIAL_FILTER.md` | The rule behind `not_an_event`, the prompt, and the 30-item calibration. |
| `REVIEW_QUEUE.md` | The Google Sheet schema, the working method, the two-sample weekly review, the definition of done. |
| `it_strings.json` | English → Italian translation memory. The one place to fix wording in the export. |
| `CHANGES_v1.3.md` | This file. |

---

## 7. What was deliberately left alone

- **`SOURCE_DATA_FINDINGS.md`** is still unchanged. It is a record of measurement on a
  specific date and editing it would weaken it.
- **The 102 corrections and the 7 open questions.** Editorial decisions, not mine to close.
- **The 89 zones.** No zone added, removed or regrouped.
- **The deferred street register.** Still deferred, same reopening trigger.
- **The other three blocks.** Named in `PROJECT_VISION.md` so that this package can be read
  correctly, and not designed. Their geography is easier than events' and their risks are
  different in kind — the news block raises editorial-responsibility questions that
  automation does not answer.

---

## 8. Verification

Checked against the files rather than asserted:

- 440 neighbourhoods, 91 zones, 89 with `is_page = true` — unchanged from v1.2.
- The build runs clean and fails as designed: a deliberate bad `free_text_stoplist` entry
  was rejected with a named error.
- The regenerated `Mappa_Quartieri_Normalizzata.xlsx` is **identical row-for-row** to the
  hand-built v1.2 export across all five data sheets.
- Exactly one ambiguous lookup key across the full three-way key space: `Colle del Sole`.
- Every guard fires on a constructed sample: bounding box, centroid, `placeType: CITY`,
  name/coordinate tail, `countryCode` null.
- `"Palazzo dei Congressi, EUR"` resolves to `EUR` rather than being rejected — the false
  positive that the gazetteer-key clause was added to fix.
- A description containing *talenti*, *EUR* and *prati* produces no zone match, where v1.2's
  length rule would have matched all three.

# Review queue — where human review physically happens

Configuration in `gazetteer.json → review`. Release version: see `START_HERE.md`.

**Corrected in v1.4:** the queue carried no structured target for two of the four
`fix_target` values, so the claim that a fix applies "in the same gesture, no bridge to
build" held for venues and for nothing else. And the discarded sample had no defined store
to be drawn from.

The operating model has always said *review the reject queue*. Until now the queue had no
address. This is the one part of the architecture that needs an interface, which makes it
the part most likely not to get built.

---

## The constraints that decide the tool

One reviewer. Twenty to forty minutes, once a week. Often from a phone.

That excludes almost everything. It does not exclude a spreadsheet.

**Google Sheets.** It already exists in the stack, n8n writes to it natively, it works on a
phone, and — the deciding reason — **the sheet is the same medium in which the fix is
applied**. A resolved `venue_unresolved` is a row in `venues.json`; a missing alias is a
cell in `Rome_Neighbourhood_Gazetteer_EN.xlsx`. Same gesture, no bridge to build.

*Considered and deferred:* Notion — better mobile app, multiple views over one database,
editorial notes alongside; but a slower and more temperamental write path from n8n, and it
behaves badly in large batches. Right when the queue stops being one person's.

*Considered and rejected for now:* a custom review interface. An item and three buttons
would be the fastest thing to use, but the gain over a well-built sheet is marginal while
the reviewer is one person, and the development time is needed elsewhere. It becomes right
when there is more than one reviewer.

---

## One file, one tab, one `block` column

All blocks — events, institutional, news, conversation — write to the **same tab**, with a
`block` column, and are worked through **filter views**.

Not one tab per block. Four tabs means four schemas that diverge on the first field added
to one of them, four n8n write nodes and four read-back workflows. A filter view gives the
same working experience — open "events", see only events — with one of each.

The exception, and the only thing that would have broken a shared schema, is the structural
fix: `alias` and `venue` for events, `page → area` for posts, nothing for institutional
items. Solved with four generic values in `fix_target` and the detail in free text. Four
values are memorable; fifteen are a dropdown you have to read, and reading the dropdown is
what turns twenty minutes into an hour.

---

## Schema

Two tabs: `queue` and `archive`, identical columns.

**Written by n8n, read-only for the reviewer**

| Column | Notes |
|---|---|
| `content_id` | The join key for the write-back. |
| `block` | `events` · `institutional` · `news` · `conversation`. |
| `source_channel` | `fb_event` · `fb_post` · … |
| `title` | |
| `excerpt` | First ~200 characters of the description. Enough to judge, short enough to scan. |
| `venue_name` | As last seen. Never a key. |
| `location_id` | Facebook `location.id`. The write key for `fix_target = venue`. |
| `source_id` | The publishing page or group id. The write key for `fix_target = source` — and the beginning of the page registry the posts channel will need. |
| `matched_neighbourhood_id` | Which gazetteer row the lookup hit, if any. The write key for `fix_target = gazetteer`. |
| `when` | Start date, or the next occurrence for a series. |
| `reject_reason` | From the enum. The column the queue is sorted by. |
| `editorial_class` | `local_interest` · `commercial_routine` · `promotion` · `uncertain`. |
| `editorial_basis` | Why the classifier decided. |
| `ai_zone` | What the model returned, including when it was rejected. |
| `geo_basis` | `explicit_address` · `explicit_zone` · `inferred` · `unknown`. |
| `source_url` | The one link the reviewer opens when the excerpt is not enough. |
| `queued_at` | |

**Filled by the reviewer — five columns, no more**

| Column | Values |
|---|---|
| `decision` | `publish` · `discard` · `fix_zone` · `skip` |
| `decided_zone` | Dropdown of the 89 zones. Only used with `fix_zone`. |
| `fix_target` | `gazetteer` · `venue` · `source` · `none` |
| `fix_key` | The alias string to add, when `fix_target = gazetteer`. Empty otherwise — the id columns above already carry the key. |
| `fix_note` | Free text, for the human reader. Never parsed. |

**What each `fix_target` writes**, so the write-back is deterministic rather than a person
re-reading a note:

| `fix_target` | Key | Effect |
|---|---|---|
| `venue` | `location_id` + `decided_zone` | Upsert into `venues.json` / Firestore `venues`. |
| `gazetteer` | `matched_neighbourhood_id` (or `decided_zone` when nothing matched) + `fix_key` | Append `fix_key` to that row's `aliases` in the master workbook, then re-run the build. |
| `source` | `source_id` + `decided_zone` | Upsert into the page registry. |
| `none` | — | The decision is about this item only. |

The gazetteer path is the one that still ends in a human editing the workbook, because the
workbook is the master and a script that writes to it would be a second one. What v1.4 adds
is that the *row* and the *string* are unambiguous.

**Filled by the write-back workflow**

`decided_at` · `decided_by`

---

## Rules

**n8n appends. Never sort or reorder the queue tab in place.** The write-back matches on
`content_id`, and manual reordering is how that breaks silently. Use filter views, which
change what you see without moving anything.

**Decided rows are moved to `archive` by the workflow, never deleted by hand.** The archive
is the only record of human judgement in the entire system, and the only dataset against
which the editorial filter can ever be evaluated or a future classifier calibrated.
Discarding it would be the most expensive mistake available in this part of the project.

**`decided_at` is not optional.** Without it, *not yet decided* and *decided but not yet
written back* are indistinguishable, and a failed write-back is invisible. It also measures
the lag between ingestion and decision, which is the number that says whether the queue is
converging or growing.

**Every decision asks a second question:** does this fix belong in the gazetteer, the venue
registry or the source registry? A fix applied to the item alone solves one item. This is
the whole reason `fix_target` exists — without it the stated operating model has nowhere to
happen, and the same correction comes back next week.

---

## Working it

Sort by `reject_reason` and work one reason at a time. Twenty `venue_unresolved` in a row
are decided far faster than twenty mixed items, because the question is the same each time
and the context stays loaded.

Expect `venue_unresolved` and alias misses to dominate early. Only 82 of the 440 gazetteer
rows currently carry an alias. That is the system working as designed, not a defect — and
each of those decisions is permanent.

---

## The weekly sample

Separate from the queue, and not optional.

- **20 published items.** One question: *is the zone right?*
- **10 discarded items.** One question: *was this genuinely not worth publishing?*

### Where the discarded items live

v1.3 said both *nothing is deleted, an excluded item goes to the queue* and *wrongly
discarded items never appear at all*. Those cannot both be true. The reconciliation, and
the reason both sentences felt right:

**`editorial_uncertain` goes into the working queue.** The classifier could not decide, so a
person should.

**`commercial_routine`, `promotion`, and venue `blacklist` skips do not.** Putting a few
hundred routine items in front of the reviewer every week would destroy the twenty-minute
budget, which is the constraint the whole design is built around. They are written to the
archive tab with `decision = auto_excluded`, never dropped.

That log is the store the 10 are sampled from. It is not the working queue and it must
exist — without it the editorial filter has no sensor at all, which is the state v1.3
actually shipped in while claiming otherwise.

Start with the first published week, not once the system feels stable.

---

## Definition of done for the events block

A stop rule, written down before the work starts, because otherwise the decision to move on
to the posts channel gets taken on a feeling.

**It is a stop rule, not a proof — be precise about this.** The minimum that satisfies the
criteria below is 19/20 twice, and 38/40 is compatible with a true accuracy anywhere from
roughly 84% to 99% at 95% confidence. Zero misses in 20 sampled discards likewise does not
exclude a real error rate near 15%. Twenty a week is what one reviewer can actually do, so
the sample size is not the thing to change — the claim is. Do not report this as evidence
that the resolver reached 95%; report it as the point at which continuing to polish this
block stopped being the best use of the next week.

The Facebook Events block is closed when:

1. **Two consecutive non-August weeks** show zone accuracy at or above 95% on the 20-item
   published sample.
2. The **top reject reason is stable** across those two weeks and understood — not
   necessarily fixed, but not a mystery.
3. **No item in the discarded sample is judged wrongly excluded two weeks running.**

August is excluded deliberately. The 107-event sample behind every number in this package
was collected in the deadest week of the Italian calendar.

---

## What changes when the other blocks arrive

Nothing structural — that is the point of the `block` column. One thing will need
attention, and it is worth knowing in advance rather than discovering it:

**News has a relevance window of hours, not days.** It cannot wait for Saturday morning.
When that block arrives, the queue will need a priority or an SLA per block — but only the
`block` column is required for that, and it is there from the start. The file does not need
rebuilding.

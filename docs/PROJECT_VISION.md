# Quartieri News — Vision and Context

*Release version and file list: `START_HERE.md`.*

Every other document in this package answers *how*. This one answers *why*, and it exists
because several decisions in those documents look arbitrary — or look like over-engineering
— unless you can see the whole shape of the thing.

It is deliberately not a specification. Nothing here is binding on the implementation.
Where something is undecided it says so, because a vision document that quietly presents
guesses as plans is worse than no vision document.

---

## 1. What is being built

A hyperlocal news site for Rome, organised into **89 neighbourhood pages** covering all 15
municipalities. Each page answers one question for the person who lives there: *what is
happening where I live?*

The premise is not that this information does not exist. It is that it exists in **fifteen
places, none of which anyone checks**: a committee's Facebook page, the municipality's
notice board, a parish newsletter, a local paper's regional feed, a residents' group, a
school circular. The work of assembling it is currently done by each resident, badly, or
not at all.

The product is the assembly. Not the reporting.

---

## 2. The page, not the feed

A neighbourhood page is built from **blocks**, not from a single stream. Four are planned:

| Block | What it carries | Where it comes from |
|---|---|---|
| **Events** | Concerts, markets, festivals, meetings, courses | Facebook Events + Facebook posts |
| **Institutional** | Municipal and city-council commissions, assemblies, resolutions | Official published sources |
| **News** | Local reporting relevant to the area | Press sources |
| **Conversation** | What residents are discussing | Neighbourhood Facebook groups |

Three things follow from this, and they explain most of what looks odd elsewhere.

**A block can be empty without the page being empty.** This is why the question "are 89
pages too many for the event volume?" has a different answer than it first appears. Events
alone would leave eighty pages bare; four blocks do not.

**What each page shows is decided at layout time, not at ingestion time.** The pipeline's
job is to place an item correctly and record enough about it that the layout can choose
later — hence `geo_level`, `municipality_code`, `content_type`, `editorial_class` and a
freshness field rather than a single "publish here" flag.

*Stated precisely, because v1.3 overstated it:* what is common across blocks and genuinely
not retrofittable is the **shape** — every item carries a geographic level, a freshness
field and some editorial classification. The **value sets** are block-specific and only the
events ones exist today. A municipal resolution is not `commercial_routine` and a news item
is not a `course`. The enums extend per block; the field names do not change.

**The blocks have incompatible geographic natures, on purpose.** An event has an address. A
municipal commission is municipality-level by nature and has no neighbourhood — forcing one
would write an invented fact into the corpus. News often carries an exact address.
Conversation is native to the group, which is native to the area. The `geo_level` ladder
(`neighbourhood → zone → municipality → city`) exists so a thin page can borrow coarser
content at render time without anything being re-labelled as more precise than it is.

---

## 3. Why the Events block is being built first

Not because it is the most valuable — it is not. The Institutional block is probably more
defensible: the sources are official and published, there is no platform-terms question, no
image-rights question, and it fills every page of a municipality at once.

Events are first because they are the **hardest geography problem in the set**, and
geography is the shared infrastructure. A Facebook event carries a venue that may not
resolve, coordinates that may be a city centroid, a name that may contradict its
coordinates, and a description in any language. Solving placement here means the gazetteer,
the guards, the venue registry, the reject queue and the review discipline exist and are
tested before three more blocks depend on them.

The order is: build the hard case first, on the block where a mistake is cheapest.

---

## 4. Where the corpus comes from, and what that costs

**Discovery is human. Extraction is automatic.** Once a week, a person opens Facebook
Events while logged in, sets the area and a 30-day window, and collects the URLs. Apify
then extracts from those direct URLs.

This is a deliberate division, not a stopgap, and it is worth being honest about both
sides:

- Direct URLs return systematically better records than keyword search, which for an
  English word like "rome" returns Rome NY and Rome GA.
- Authenticated automated collection is prohibited by the platform's terms, and the account
  at risk would be a personal one.
- **The cost of the whole system is not the AI and not Apify.** 107 events billed $1.40.
  The cost is the weekly hour. It is also the one part that does not scale to other cities
  and the one single point of failure: a missed week is a hole in the corpus.

That last point should be stated plainly in any investor-facing material rather than
discovered there. It is a real constraint of the current design, accepted knowingly for the
first phase.

The **Posts channel** — events announced as ordinary page posts by committees, parishes,
associations and the municipality — matters more than its position in the build order
suggests. Small local organisers usually do not create Facebook Events. They write a post.
That channel is where the genuinely hyperlocal supply lives, and it has a different shape:
no `location.id`, so no venue registry, but a *publishing page* that is almost always tied
to one area. The equivalent deterministic layer there is a **page registry** rather than a
venue registry.

---

## 5. The operating philosophy

Four principles carried from the original specification, and one added in v1.2. They are
not style preferences; each of them is a defect that was found and closed.

- **Shortcuts belong in the pipeline, never in the stored data.** A convenience taken at
  ingestion becomes a permanent falsehood.
- **A null is better than an invented value.** The single most consequential line removed
  from v1.1 was an instruction to always guess a neighbourhood.
- **A rule with no output field is not a rule.** If nothing records that a rule fired, the
  rule cannot be measured and will silently stop working.
- **Deferred capabilities are documented, not deleted.** The deterministic street register
  was evaluated and deferred, with the trigger to reopen it written down.
- **One master, generated copies.** A hand-edited derivative is a second master that nobody
  declared. Two workbooks had already diverged on the name of the key column before anyone
  noticed.

A sixth is added in v1.3, and it is the reason for the review queue's shape:

- **A filter that removes things must be sampled, not just logged.** The reject queue shows
  what was blocked. It cannot show what was blocked *wrongly*, and it cannot show what was
  published wrongly. Only sampling shows either.

### Cost scales with errors, not with volume

The system is reviewed at the **reject queue**, not the publication queue. Every reject
carries a structured reason; the weekly job is to sort by frequency and attack the top one.
And every fix goes into the **gazetteer, the venue registry or the source registry** — not
into the individual item. Correcting one event solves one event; adding the street as an
alias solves every future event on that street.

This is the whole economic argument. Review cost falls as the system learns, instead of
rising with volume. It only works if the fix has somewhere structural to go, which is why
the review sheet has a `fix_target` column at all.

---

## 6. What is decided, what is open, what is not yet thought about

Being explicit about which is which is the point of this section.

**Decided and written into the files.** The gazetteer and its 89 zones; resolution order;
the guards; the conditional double pass; `human_verified` precedence; recurring events as
one article with many occurrences; the venue registry as a separate store; the refresh TTL;
the editorial filter's criteria; the review queue's shape and its definition of done. And,
in v1.4.2, the two non-technical ones that had been open longest:

- **Images.** Original event images are downloaded and served locally, with the exposure
  knowingly accepted and five mitigations required: credit and link on every item, stored
  provenance, reduced resolution, a working takedown route backed by an `image_removed`
  flag, and no watermarked or clearly commercial assets. The generated-card fallback is
  built regardless, because 10% of records carry no image at all.
- **Sources.** Collection is manual, one to two times a week and more often in busy
  periods, covering the month ahead. No authenticated automation. Every item credits its
  organiser and links back. The full statement is in `PROJECT_HANDOVER.md` §2.16.

**Open, and blocking something.**

1. **Distribution across the 89 pages.** Measurable today with `zone_distribution.py` on
   the existing sample. It determines whether thin pages need a municipality fallback in
   the first version or the second.
2. **Seven gazetteer questions** on the `open_questions` sheet. Only Colle del Sole blocks
   anything technical.

**Open, and not yet blocking.**

- **Courses.** Enrolment-based multi-session items are neither promotion nor events. They
  are useful and need a different presentation. Undecided; for now they must simply not be
  discarded indistinguishably.
- **An automated review agent.** Discussed, not decided. If added it should run after the
  deterministic checks, be allowed to return `uncertain`, and flag rather than rewrite.
- **Editorial responsibility.** The News block will eventually raise questions — naming
  individuals, presumption of innocence, right to erasure — that automation does not answer
  and that require a named human editor. Worth knowing now; not worth solving now.

**Not yet thought about, and named here so it is not mistaken for settled.** Revenue.
Publishing cadence and whether pages update continuously or on a schedule. How a reader
finds their page. Whether the site has any human-written content at all. Expansion beyond
Rome, which is currently an ambition rather than a plan — and which the manual discovery
step directly constrains.

---

## 7. How to read the rest of the package

| Read this | For |
|---|---|
| `PROJECT_HANDOVER.md` | Every decision taken, with its reason. Start here. |
| `SOURCE_DATA_FINDINGS.md` | What the source data actually does, measured. The evidence under most decisions. |
| `GAZETTEER_README.md` | The data model and the eight invariants. |
| `PROMPT_GEO_BLOCK.md` | The geography prompt and the validation code. |
| `EDITORIAL_FILTER.md` | What counts as a locally useful event. |
| `REVIEW_QUEUE.md` | Where human review physically happens. |
| `WORKFLOW_FIXES.md` | The defect list and the spec changes still outstanding. |
| `CHANGES_v1.3.md` | What changed in this revision and what it breaks. |

One caution about `SOURCE_DATA_FINDINGS.md`: it is a measurement taken on a single day in
mid-August, the deadest week of the Italian year. The field fill rates are probably
representative. The geographic and thematic composition almost certainly is not, and
probably understates local community activity — which is the very thing this project
exists to surface.

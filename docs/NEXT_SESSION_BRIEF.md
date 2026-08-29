# Next session — what to do, and what is already decided

**For a fresh conversation. Written 22 August 2026, at the end of the session that produced
release 1.4.4 of the events package.**

Read this first, then `START_HERE.md`. Everything else in the package is reference.

---

## 1. The one task

**Consolidate the technical specification.**

The specification exists and is **in this package**: *"QUARTIERI NEWS — TECHNICAL
IMPLEMENTATION SPECIFICATION — Facebook Events Workflow Refactoring"*, version **2.4**,
7 August 2026, 16,964 words in five parts, produced across six iterations with two external
technical reviews incorporated.

It is better than the 1.4.4 package assumed. It carries the registry claim/commit
lifecycle, the `source_hash` canonicalisation, the deterministic Drive upsert and the run
lock — none of which any 1.4.4 document covers — and it reaches the same design principle
independently: *no shortcut may produce a wrong stored value, only a missing one, marked
for review*. **Consolidation must not flatten it.** `SPEC_V25_WORKPLAN.md` lists what has
to survive.

**That v2.4 predates all the work in release 1.4.4 and contains none of it.** Do not
confuse it with the "v2.4" referred to in `WORKFLOW_FIXES.md` §4, which means *the version
that will exist once the 13 changes are applied*. To avoid a collision, the consolidated
document should be numbered **v2.5**.

### What to upload to the new conversation

**Just this zip.** The v2.4 specification is now inside it, in two forms: the original
`Quartieri_News_FB_Events_Workflow_Specification_v2_4.docx` and `spec_v24.md`, a pandoc
conversion that is greppable and does not need the original to work with.

`SPEC_V25_WORKPLAN.md` maps every one of the 17 changes onto the section of v2.4 it lands
in, lists what v2.4 already gets right and must survive, and gives the field-by-field
contract migration. Read it before opening the spec.

Optionally add `UX e Design` and `Next Step` from Google Drive, folder *Progetto Quartieri
News*, if the site structure and tag taxonomy are to be folded in.

### The rule that matters more than the consolidation

The consolidated spec must **point at `gazetteer.json` for every rule, not restate it.**

Six review rounds produced defects, and by the last three they were almost entirely the
same rule written in four documents and updated in two. The Markdown should explain *why* a
rule exists; the JSON is *what* it is. A spec that paraphrases the rules becomes a
fourteenth place for them to drift.

---

## 2. The 13 changes, from `WORKFLOW_FIXES.md` §4

1. Replace the geography section with `PROMPT_GEO_BLOCK.md`.
2. Add `geo_verification_status` and the `human_verified` persistence and conflict rules.
3. Add `publication_zone_id` and `neighbourhood_id` to the Firestore venue registry.
4. Handle recurring events as a series plus `occurrences[]`.
5. Replace the pre-Apify blocklist with the refresh TTL policy.
6. Introduce the separate venue registry.
7. Extend the reject-reason enum, with layers.
8. Record `discovery_strategy: manual_url_collection` as a first-class field.
9. **No longer a placeholder** — the position on sources is written and is in
   `PROJECT_HANDOVER.md` §2.16. Paste it in verbatim.
10. Add the `duration` parser, `date_precision` and `next_occurrence`.
11. Add the editorial classification pass, its three fields and its two new reject codes.
12. Add `geo_level` to every item and state that the geographic fallback happens at render
    time.
13. Formalise the review queue schema and the two-sample weekly check.

Plus, from release 1.4.2–1.4.4 and not in that list:

14. `municipality_code` on every item — without it a municipality-level item is not
    routable.
15. Image policy: images downloaded and served locally, with the five mitigations
    (`PROJECT_HANDOVER.md` §2.15). The generated fallback card is **not optional**.
16. Collection cadence: one to two times a week, more in busy periods, month ahead.
    Staleness warning at 10 days.
17. The `never_substring` list, found by running the real sample.

---

## 3. A contract mismatch to resolve during consolidation

Spotted while locating the old spec, and not yet reconciled. Its Part III canonical
contract has a `geography` object built like this:

```
urban_zone · neighborhood_name · neighborhood_slug · confidence (numeric) · method
```

Release 1.4.4 replaced all of it:

| Spec v2.4 | Release 1.4.4 | Why |
|---|---|---|
| `urban_zone` | `publication_zone_id` | The display name is not a key (invariant I2) |
| `neighborhood_slug` | `neighbourhood_id` | British spelling is now the master; the two workbooks had already diverged on this |
| `confidence` (numeric) | `geo_basis` + `geo_verification_status` | A number nobody can act on, replaced by two countable categories (I5) |
| `method` | `geo_verification_status` | Same field, defined values |
| — | `geo_level`, `municipality_code` | New. Required by the layout fallback |

**This is not cosmetic.** It changes Firestore documents, the canonical JSON on Drive, and
the future WordPress publisher. Decide during consolidation whether existing records are
migrated or the schema version is bumped and old records left as they are — the corpus is
small enough today that either is cheap, and it will not stay that way.

---

## 4. Three decisions still open, all Riccardo's

**4.1 Commercial guided tours — the significant one.** Roughly 20 of the 107 sampled events
are paid guided visits from operators such as Laboratorio 104, Bellezze di Roma and
bellaroma.info: Terme di Caracalla, Palazzo Doria Pamphilj, Galleria Borghese, Villa Blanc.

Under `EDITORIAL_FILTER.md` as written, the promotion gate runs first and classifies all of
them `promotion`. That removes a fifth of the corpus.

*For publishing them:* real culture in real places; it fills Centro Storico and Testaccio.
*Against:* tourist supply rather than neighbourhood life; not what an Acilia resident is
missing; the category where the site most resembles any other aggregator.

Once decided, the block goes into `golden_set_editorial.json` and the rule into the prompt.
See `golden_set_editorial.json → known_gap`.

**4.2 `Colle del Sole`.** The only ambiguous lookup key in 440 rows — two places with the
same name, in Municipio VI and XI. Until it is resolved the lookup rejects rather than
guesses. A two-minute editorial decision: do both places exist as recorded?

**4.3 The five addresses marked `confidence: verify`** in `golden_set_geographic.json`.
Boundary checks on a map, needed before those items can be scored.

---

## 5. What is already done, so it is not redone

- Gazetteer: 440 neighbourhoods, 91 zones, 89 pages, 102 corrections. Master workbook plus
  a generator that fails the build on a broken invariant.
- Geographic resolution: order of operations, two guard tiers, conditional double pass,
  validation code, prompt.
- Editorial filter: criteria, execution order, prompt, three output fields.
- Review queue: Google Sheet schema, structural fix keys, two-sample weekly review,
  definition of done.
- Two golden sets: 30 hand-classified editorial items, 40 hand-marked geographic items with
  trap cases.
- `test_guards.py`: 38 checks, both directions.
- The 107-event sample, shipped with the package.
- Images and source position: decided, written up.

**Do not reopen the architecture.** Six review rounds have passed and the last one found
only stale documentation. The remaining risk is in implementation and in the numbers that
come out of running it, not in the design.

---

## 6. Measured facts worth carrying, because they are counter-intuitive

- **Municipio X: zero events in 107.** Not one resolved to Acilia, Ostia, Casal Palocco,
  Infernetto, Dragona, Vitinia, Giardino di Roma or Torrino. The strongest argument there
  is for the Facebook **Posts** channel: the neighbourhoods this project exists for do not
  use Facebook Events at all.
- **The venue registry repeats far less than assumed.** 8 of 157 `location.id` values
  carried more than one event; zero inside the 107-event sample. Cheap infrastructure whose
  payoff must be measured over months — not, as earlier revisions claimed, the
  highest-leverage item remaining.
- **Deterministic matching alone places 31 of 107, only 2 by exact match.** Expected — the
  model does the geographic work — but the alias layer contributes almost nothing today.
- **Guards stop about 17%** of the sample. Real weekly review load from day one.
- Everything above comes from **one day in mid-August**, the deadest week of the Italian
  year. Field fill rates are probably representative; geographic and thematic composition
  almost certainly is not.

---

## 7. After the spec

In order, and not before:

1. Spec v2.5 consolidated.
2. Hand over to the developer. `START_HERE.md` §6 lists what he owes and what is missing;
   the earlier note on what to share and what to withhold still applies — and tell him
   directly which parts of his own previous work are now wrong: the geography prompt
   section, any `=== "TRUE"` boolean comparison, and the pre-Apify blocklist.
3. Run the two golden sets against the prompts before either is wired to publication.
4. Then, and only then, the **Posts** channel — where the equivalent of the venue registry
   is a *page* registry keyed on the publishing page id, since `location.id` does not exist
   on a post. That registry is already being seeded: `source_id` is a column in the review
   queue.

# Spec v2.5 — work plan

**Written 22 August 2026, after reading the v2.4 specification (16,964 words, five parts).**
This maps every change onto the section of v2.4 it lands in, so the consolidation session
does not have to rediscover the structure.

`spec_v24.md` — a pandoc conversion of the original `.docx` — ships with the package so the
text is greppable and the original is not needed to work.

---

## The numbering trap, first

The uploaded document **is** version 2.4, dated 7 August 2026, superseding 2.3, 2.2, 2.1,
2.0 and 1.1. It predates every decision in release 1.4.4 and contains none of them.

`WORKFLOW_FIXES.md` §4 says "the thirteen changes the spec needs to become v2.4". Written
before anyone checked what the spec was actually numbered. **The consolidated document is
v2.5.**

---

## What v2.4 already gets right, and must survive

Read this before changing anything. Several v2.4 rules are better than what the 1.4.4
package assumes, and consolidation must not flatten them.

- **The design principle is the same one.** *"Wherever a shortcut was taken, it was taken in
  the pipeline and never in the data. No shortcut is allowed to produce a wrong stored
  value — only a missing one, marked for review."* Identical philosophy, arrived at
  independently.
- **Confidence is assigned by the workflow, never self-reported by a model** (Corrections
  carried over from 1.1). This anticipates `geo_basis` and is arguably stated more sharply.
- **`source_hash` canonicalisation** with an ordered key/value array and an explicit
  exclusion list. The package assumes this exists; it does here, in §2.2.
- **The registry claim/commit lifecycle** and the run lock as *enforcement, not
  instruction* (§4.2, §2.4, §2.5). Nothing in the 1.4.4 package covers this and it must
  not be lost.
- **The deterministic upsert on Drive**, including the "registry lost the file ID" repair
  case (§5.2).
- **Part V — four deferred capabilities, each with its reactivation trigger.** D2 is
  deterministic geocoding, the same deferral the package documents.
- **`content_id` excludes municipality and neighbourhood deliberately** (§2.1) — geography
  can be recomputed, identity cannot change. This is invariant I2 reached from another
  direction, and it is right.

---

## The changes, mapped to sections

### A. Geography — the largest single edit

| # | Change | Lands in |
|---|---|---|
| 1 | Replace the geography section with `PROMPT_GEO_BLOCK.md` | §3.2 entirely (3.2.1–3.2.4) |
| 12 | `geo_level` on every item; fallback at render time | §3.2, Part III geography block |
| 14 | `municipality_code` on every item | Part III geography block |
| 2 | `geo_verification_status`, `human_verified` persistence and conflict | §3.2.4, Part III, Firestore contract |

v2.4 §3.2 runs: `is_rome` → deterministic alias match → two independent AI passes →
reconciliation. The shape is right and the package refines it. What changes:

- **Two passes always → conditional.** v2.4 spends two passes on everything; 1.4.4 spends
  the second only on `inferred`/`unknown`, or when there is no venue hit and no street
  address.
- **The venue registry is inserted** between the alias match and the model. It does not
  exist in v2.4 at all.
- **Guards split into two tiers**, with the suspicion tier *after* the venue registry.
  v2.4 has the bounding box (§5.2 of Part I) but not the centroid blocklist, the
  `placeType: CITY` check or the name/coordinate rule.
- **The area list moves.** v2.4 Part I §5.1 asks the owner to supply a canonical area list
  as a Sheet or embedded config. That list now exists, is generated, and is
  `prompt_list_publication_zones.txt`. Replace the request with a pointer.
- **`urban_zone` / `neighborhood_slug` / numeric `confidence` / `method` are replaced.**
  See the contract table below.

### B. The canonical contract — Part III

| v2.4 field | v2.5 | Why |
|---|---|---|
| `geography.urban_zone` | `publication_zone_id` | The display name is not a key (I2) |
| `geography.neighborhood_slug` | `neighbourhood_id` | British spelling is the master; the two workbooks had already diverged on exactly this |
| `geography.neighborhood_name` | derived, display only | |
| `geography.confidence` (0–1) | `geo_basis` + `geo_verification_status` | A number nobody can act on, replaced by two countable categories (I5) |
| `geography.method` | `geo_verification_status` | Same intent, closed value set |
| — | `geo_level`, `municipality_code` | New. Required for the layout fallback and for municipality-level routing |
| `quality.requires_review` | keep, plus `reject_reason` | v2.4 has the boolean; the package adds the structured reason and its layer |
| `media[].copyright_status` | keep, plus the image fields | See D below |
| — | `editorial_class`, `editorial_basis`, `content_type` | New pass |
| — | `date_precision`, `next_occurrence` | New |
| — | `occurrences[]` | New |

**Decide explicitly:** bump `schema_version` to 1.1 and leave existing records, or migrate.
The corpus is small enough today that either is cheap. It will not stay that way.

### C. New capabilities with no home in v2.4

| # | Change | Where it goes |
|---|---|---|
| 3, 6 | Venue registry, keyed on `location.id` | New sub-phase in Phase 3, before §3.2.2; new Firestore collection in Part III |
| 4, 10 | Recurring events as series + `occurrences[]`; `duration` parser, `date_precision`, `next_occurrence` | §3.3 (which currently handles date/mode/cost semantics) |
| 5 | Refresh TTL replacing the pre-Apify blocklist | §1.3/§1.4 and §2.5 registry decision table |
| 7 | Extended reject-reason enum with layers and `blocks_publication` | §5.1 validation, and Part III `quality` |
| 11 | Editorial classification pass | New sub-phase in Phase 4, before article generation — do not generate an article for an item that will be excluded |
| 13 | Review queue schema and the two-sample weekly check | Part IV, alongside the acceptance matrix |
| 8 | `discovery_strategy: manual_url_collection` | Part III `source` block, and Part I |
| 16 | Collection cadence 1–2×/week, staleness warning at 10 days | Part I §7, with the run report in §5.5 |

### D. Owner decisions v2.4 asks for and that are now answered

Part I is largely a list of things the owner must supply. Several are no longer open, and
leaving the questions in place invites the developer to ask for what already exists.

| v2.4 asks for | Answer |
|---|---|
| §5.1 Canonical area list | `prompt_list_publication_zones.txt`, generated. 89 values |
| §5.2 Scope bounding box | In `gazetteer.json → guards.rome_bbox`, plus four more guards |
| §7 8–12 test event URLs | Superseded: the full 107-event sample ships with the package, plus two golden sets |
| §8 Content rights and source terms | **Decided.** Images: `PROJECT_HANDOVER.md` §2.15. Sources: §2.16, verbatim text ready to paste. This is change #9 and #15 |
| §9 Editorial review capacity | Answered: `REVIEW_QUEUE.md`, 20–40 minutes weekly, one reviewer, 20 published + 10 discarded sampled |
| §10 Publication granularity — *stays open* | Still open, but reframed: with four blocks per page it is a render-time fallback threshold, not a decision about how many pages exist |
| §6.1 Controlled topic list | Unchanged, still owner input |

### E. Structural rule for the whole document

**Point at `gazetteer.json`; do not restate it.**

Six review rounds produced defects, and the last three found almost nothing but the same
rule written in four documents and updated in two. v2.4 currently embeds geographic rules
in prose. In v2.5 those sections should say *the rule is in `guards.name_coordinate_mismatch`*
and then explain **why** it exists. Explanation does not go stale; restatement does.

The same applies to the 89 values, the reject enum and the editorial criteria.

---

## Suggested order of work

1. Part III first. The contract determines everything upstream, and the field mapping above
   is the part most likely to be got wrong quietly.
2. Then §3.2, the largest edit.
3. Then the new sub-phases: venue registry, editorial pass, recurrence, TTL.
4. Then Part I — mostly deletions, replacing answered questions with pointers.
5. Part IV last: the acceptance matrix has 40 cases and several will need rewriting once
   the contract changes. The two golden sets should be added here as acceptance gates.
6. Part V unchanged. D2 remains deferred with the same trigger.

Keep the document's existing voice and structure. It is well written and the developer has
already read it once; a wholesale restructure costs him a re-read for no gain.

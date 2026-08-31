# Quartieri News — project brief

Stable strategic context for the Council, so a question does not have to carry
the whole repository. Keep it short: when it stops fitting on a screen or two it
has become a second copy of something else and should point instead.

This brief is background, never authority. Where it disagrees with
`gazetteer/gazetteer.json`, a `decisions/` entry or the specification, those win
— see the normative hierarchy in `AGENTS.md`.

**Last reviewed:** 31 August 2026 (events package 1.4.5 / specification v2.5).

## What the product is

A hyperlocal news platform for Rome: 89 neighbourhood pages covering all 15
municipalities. The first live surface is neighbourhood event listings, built by
an automated pipeline that acquires events, decides where they belong
geographically, filters them editorially, and publishes what survives.

Nothing is live yet. The pipeline runs against staging; the site does not exist
in public form.

## Where things stand

- **Specification v2.5** (Drive, QN Hub / 10 Specifications) is the contract, with
  acceptance criteria T01–T45. Events package release 1.4.5.
- **The gazetteer is built and authoritative**: 440 neighbourhoods, 91 zones, 89
  publication pages. `gazetteer/gazetteer.json` outranks every document.
- **Production is n8n Cloud**; this repository mirrors and certifies what runs
  there. Pushing here deploys nothing. Pipeline work runs against `staging_`
  Drive folders and Firestore collections until reviewed.
- **The development loop is the working part**: Claude builds, Codex reviews on
  the pull request, the owner decides and merges (DEC-104, DEC-007, DEC-008).
  `main` is protected; everything goes through a PR.
- **Four open decisions gate different things**, and none is technical. Their
  own `Blocks:` lines are authoritative: DEC-001 (commercial guided tours) gates
  editorial filter activation; DEC-004 (production event cap) gates schedule
  activation; DEC-002 (Colle del Sole) and DEC-003 (five addresses to verify)
  gate scoring of the geographic golden set. They are not interchangeable, and
  sequencing around the wrong one wastes a cycle.

## Constraints that shape most answers

- **One owner, part-time.** DEC-103 fixed human review at roughly 20–40 minutes
  a week. Any proposal whose cost is the owner's attention is expensive.
- **Cost is real and small.** Model calls, n8n Cloud and storage are the running
  costs; a recurring cost is worth much more scrutiny than a one-off one.
- **The repository is public** and carries no personal data. Raw sampled source
  data lives only in the Drive release packages (DEC-102, DEC-104).
- **August data is unrepresentative.** The 107-URL sample was collected in the
  deadest week of the Roman year; 72 of 89 pages were empty. Do not size
  anything on it (DEC-006).
- **Editorial trust is the asset.** A wrong neighbourhood or a promotional item
  published as news costs more than a missed event. The standing invariants that
  follow from this are not restated here — they are owned by
  `gazetteer/gazetteer.json`, `prompts/PROMPT_GEO_BLOCK.md` and
  `venue-registry/venues.json`, and a copy in this brief would drift from them.
  Retrieve those files when a question turns on one.

## Where the decisions live

`decisions/` is the log; a decision exists only if written there. DECIDED
entries are never reopened — if circumstances changed, a new entry supersedes
and links back.

Open and worth knowing before answering most product questions: DEC-001
(commercial tours, ~19% of the sampled corpus), DEC-002, DEC-003, DEC-004,
DEC-005 (schema 2.0 sign-off), DEC-006 (thin-page fallback). Read the entry
rather than this line when what it blocks matters.

## Questions the Council is for

Sequencing and scope: what to build next, what to defer, when a second city
stops being hypothetical, how much design a phase deserves before it is built,
which manual step is worth automating, what evidence would justify activating
the pipeline. Not: how to implement something already decided — that is Builder
and Technical Council work.

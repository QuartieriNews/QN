# DEC-022 — Wiki di contesto: schedario, diario e pagine generate

Status: DECIDED (23 October 2026, owner in the builder session, confirmed on the question put by the builder)
Blocks: nothing since 23 October 2026. While open it blocked the merge of pull request
#17, keeping `docs/wiki/` and `tools/wiki/` in the repository, any extension of the wiki
and any pipeline read of it.

Numbering: this entry was opened as DEC-014; it was renumbered on 23 October 2026
because DEC-014…DEC-021 are the eight owner decisions of 11 September 2026 cited in
`docs/PHASE_0_EXECUTION.md` (pull request #15) and not yet written as files. DEC-022
is the next free number in the 001–099 range (`decisions/README.md`, rule 1).

Question: the June 2026 source study produced per-item records with places,
municipality, zone and thread ids. Should Quartieri News keep a *context wiki*
built from them — a registry of places, actors and threads (schedario), a dated
diary of items attached to those entries, and generated per-municipio pages — as
the memory that gives the institutional and news blocks their context?

Two questions are folded into one here, and the second decides the first:

1. **Keep the wiki, and where** (options A–C below).
2. **The DEC-109 reading.** DEC-109 keeps per-item inventories in the repository with
   «never a text, a title or a person's name taken from a source». `diario.json` carries,
   for every item, a one-line `titolo` and the source URL; the titles are the ones the
   study's readers wrote (the `titolo` column of the study's `Report*_notizie_*.csv`),
   and the pages name people where the study's readers kept them (DEC-105: no
   automatic anonymisation, names kept when pertinent to the fact). The Codex review
   of this pull request (cycle 1, 23 October 2026) reads DEC-109 as excluding those
   titles and names from the repository. If the owner agrees, option A is not
   available as committed: the per-item data move to Drive (B) or the titles leave the
   repository and the pages become lists of dates and URLs. If the owner reads the
   study's titles as the readers' own labels, DEC-109 is honoured as is and this entry
   records the reading.

Options:
A. **Keep it as proposed** (`docs/wiki/`, built by `tools/wiki/`): structured
   data first, prose only as a rendering; identity merges/splits decided by a
   person; names as the study kept them (DEC-105); no source text in the repo
   (DEC-109, under the reading in question 2). Extend with May 2026 from the owner's
   machine, then month by month.
B. Keep only the structured data (`schedario.json`, `diario.json`) on Drive, not
   in the repository, and regenerate pages on demand.
C. Do not build a wiki now; revisit after the first public page.

Claude recommendation: A, with two conditions. First, the thread grouping
inherited from the study (same date and place) is a starting point, not a
judgement: 81 of 472 open threads have low coherence and must be split by a
reader before the pipeline relies on them. Second, the wiki stays a back-office
for context lines under news items — it is not a fifth block and not a page of
its own until the four blocks exist. On question 2 the recommendation is the
readers'-labels reading, because the titles are the study's rewrites, not source
text; but that is the owner's reading to give, and until it is given the pull
request is not merged.

Codex (reviewer, cycle 1 of pull request #17, 23 October 2026): verdict
OWNER_DECISION_REQUIRED; reads DEC-109 and DEC-105 boundary 1 as excluding the
committed `diario.json` titles and the names in the pages; asks that the decision
precede the artefacts.

Impact: new top-level path `tools/wiki/` (RED under DEC-012: new top-level
path), `docs/wiki/` (~4 MB of derived data). No pipeline, gazetteer, prompt or
n8n behaviour changes. The pull request carries the artefacts together with this
entry so that the owner decides on the real pages; nothing merges before the decision.

Decision (owner, 23 October 2026). Question 1: **A**, the wiki is kept as proposed,
in `docs/wiki/` built by `tools/wiki/`, with the two conditions of the recommendation
(low-coherence threads are split by a reader before the pipeline relies on them; the
wiki is a back-office for context lines, not a fifth block). Question 2: the one-line
titles written by the study's readers are the readers' own labels, not source text;
DEC-109 is honoured as committed. The same decision draws the line for pull request #18:
the titles of a newspaper's own pages (Roma Today) are source text and leave the
repository; that dataset stays only in the private preview and on Drive.

Owner's words, put to the owner as a yes/no on the builder's recommendation and
confirmed: «i titoli riscritti vanno bene, quindi la 17 può passare; i titoli di Roma
Today no, quindi dalla 18 va tolto il file dei dati, che resta solo nell'anteprima
privata.»

Decided by: Owner · Date: 23 October 2026 · Affected: docs/wiki/, tools/wiki/,
DEC-109 (reading recorded, entry unchanged), DEC-105 (applied as decided, no
anonymisation added), pull request #18 (`tools/site/events_2026-10.json` removed).

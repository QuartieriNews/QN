# DEC-014 — Wiki di contesto: schedario, diario e pagine generate

Status: OPEN — OWNER_DECISION_REQUIRED
Blocks: nothing today. It gates whether `docs/wiki/` is kept, how it grows
(May 2026 and the monthly runs) and whether the pipeline may consult it.

Question: the June 2026 source study produced per-item records with places,
municipality, zone and thread ids. Should Quartieri News keep a *context wiki*
built from them — a registry of places, actors and threads (schedario), a dated
diary of items attached to those entries, and generated per-municipio pages — as
the memory that gives the institutional and news blocks their context?

Options:
A. **Keep it as proposed** (`docs/wiki/`, built by `tools/wiki/`): structured
   data first, prose only as a rendering; identity merges/splits decided by a
   person; people only in a public role (DEC-105); no source text in the repo
   (DEC-109). Extend with May 2026 from the owner's machine, then month by month.
B. Keep only the structured data (`schedario.json`, `diario.json`) on Drive, not
   in the repository, and regenerate pages on demand.
C. Do not build a wiki now; revisit after the first public page.

Claude recommendation: A, with two conditions. First, the thread grouping
inherited from the study (same date and place) is a starting point, not a
judgement: 81 of 472 open threads have low coherence and must be split by a
reader before the pipeline relies on them. Second, the wiki stays a back-office
for context lines under news items — it is not a fifth block and not a page of
its own until the four blocks exist.

ChatGPT recommendation: (to be added on first review cycle)

Impact: new top-level path `tools/wiki/` (RED under DEC-012: new top-level
path), `docs/wiki/` (~4 MB of derived data). No pipeline, gazetteer, prompt or
n8n behaviour changes. One question the owner must settle: whether the study's
one-line titles count as "inventories without source text" under DEC-109 (the
build assumes yes; the titles are the study's own rewrites, anonymised).

Decided by: — · Date: — · Affected: docs/wiki/, tools/wiki/, DEC-109 (reading),
DEC-105 (applied).

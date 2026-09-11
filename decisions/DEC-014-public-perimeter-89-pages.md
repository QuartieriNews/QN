# DEC-014 — Public perimeter of the MVP: 89 pages, three blocks, minimum stocks with fallback

Status: DECIDED
Closes in part: DEC-006 (fallback yes/no; the form of the fallback stays open there).

Question: what is the public perimeter of the Quartieri News MVP, and what minimum
content must every page show at launch?

Options:
A. **CHOSEN.** All 89 pages at launch, with Amministrazione, Cronaca and Eventi as
   required blocks and Conversation optional; minimum visible stocks 5/1/10/2 per page
   with a geographic fallback for events.
B. Public launch staggered by block.
C. Public launch staggered by Municipio or by source readiness.
D. Depth vs. base pages as a natural experiment.

Claude recommendation: in Round 2 the Council kept B, C and D as comparable
alternatives without choosing one. The owner chose A (response of 11 September 2026)
as the public configuration; B–D remain contingency plans at the owner's discretion,
not alternatives the Council still proposes.

ChatGPT recommendation: as above; neither perspective chose.

## Rule

- The 89 zones are the canonical editorial units. The ~440 gazetteer toponyms serve
  recognition and never generate editions of their own.
- The public launch comprises all 89 pages. Development, population and calibration may
  proceed internally by Municipio; this is a working method, not a public rollout.
- Amministrazione, Cronaca and Eventi are required blocks. Conversation is optional and
  the first section to sacrifice.
- Minimum visible stocks per page: 5 Amministrazione items, 1 Cronaca item, 10 future
  events (a floor, not a ceiling), Conversation where the already-censused groups
  provide it. Amministrazione and Cronaca accumulate; events are a perishable stock.
- When a neighbourhood has fewer than ten events of its own, the section is completed
  from a wider pool — the whole Municipio or the adjacent neighbourhoods; which one is
  decided at UI design time on real data (DEC-006 residual). The geographic provenance
  of every item is always understandable. An event is one canonical content shown on
  several pages: 890 is the number of visible placements at launch, not of unique events.
- Before launch, verify that the initial sources plus the fallback reach the floor on
  every page. If they do not, widen the search or the sources; the Posts channel
  (events derived from group posts) then becomes a launch dependency.
- Launch requirements are the eight listed in the owner's response ("Requisiti minimi
  per il lancio"), as registered in the Round 2 Reconciliation §5.

## Order of the two pre-launch activities

1. Pre-launch verification of event availability and of the fallback — first, because it
   is short and decides whether Posts or other additional sources become a launch
   dependency.
2. Thin slice of Amministrazione on 2–3 Municipi in staging — immediately after.

The two may overlap when they do not compete for the same operating time.

## Legal verifications and the launch

The open legal questions (Round 2 Reconciliation §8) are not, as a set, pre-launch
gates. Each verification blocks or modifies only the capability it refers to: newsletter
privacy before data collection; Conversation before that block is activated; political
advertising before the first political campaign is accepted. The operating rules the
owner has already assumed on names (DEC-016), AI disclosure (DEC-019) and corrections
(DEC-020) are active risk assumptions, to be modified if the legal opinion finds
incompatible obligations. What must be completed before launch is the set of
requirements indispensable to publish the site as a whole lawfully.

Impact: closes DEC-006 in the part it asked ("enable the municipality-level fallback for
thin zone pages in the first site version?" — yes, as a launch requirement); the residual
DEC-006 did not pose and the owner deferred (Municipio vs. adjacent neighbourhoods;
section vs. single flow; geographic presentation) stays open there. DEC-006's rule on
non-August counts stays in force and coincides with the pre-launch verification.
Replaces the Round 2 reading of the unique-events requirement (~150 unique live events
with Municipio sharing, not 890). Does not touch DEC-101 or DEC-102; the `Blocks:` lines
of DEC-001 and DEC-004 are unchanged.

Blocks: nothing (this entry unblocks the launch configuration and the sizing of the
initial population).

Decided by: Owner · Date: 11 September 2026 (Strategic Council Round 2 Reconciliation,
owner confirmation) · Affected: `docs/strategic-council/PROJECT_BRIEF.md` (perimeter),
DEC-006 (pointer), site and render-time fallback, `gazetteer.json` (an adjacency table
only if the "adjacent neighbourhoods" form is chosen).

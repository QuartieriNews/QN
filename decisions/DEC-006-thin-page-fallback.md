# DEC-006 — Municipality fallback for thin pages in site v1

Status: OPEN (residual only)
Closed in part by DEC-014 — the question below is answered yes: the fallback is a launch
requirement (11 September 2026). What stays open here is only the residual DEC-014
records as deferred: Municipio vs. adjacent neighbourhoods, section vs. single flow,
geographic presentation — decided at UI design time on real data.
Blocks: site layout decision only; not the pipeline

Question: enable the municipality-level render-time fallback for thin zone pages in
the first site version?

Rule already fixed by spec v2.5, Part I §10: decide on per-zone counts from the first
non-August weeks of live data (run report `resolved_by_zone`), never on the August
sample (72/89 pages empty in the deadest week of the year). Do not reduce the zone
count on August numbers.

Decided by: — · Date: — · Affected: site layout; reads geo_level + municipality_code.

## Residual after DEC-014

Decided (DEC-014, not to be re-asked here): a fallback exists in the first site version;
ten future events per page is the floor; provenance is always understandable; an event
is one canonical content shown on several pages.

Still open: the form of the fallback — whole Municipio or adjacent neighbourhoods (an
adjacency table does not exist in the gazetteer and would have to be built); a separate
section or a single flow; the geographic presentation. The rule above on non-August
counts is unchanged and coincides with the pre-launch verification DEC-014 orders first.

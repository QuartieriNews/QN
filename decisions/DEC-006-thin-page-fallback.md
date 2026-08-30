# DEC-006 — Municipality fallback for thin pages in site v1

Status: OPEN
Blocks: site layout decision only; not the pipeline

Question: enable the municipality-level render-time fallback for thin zone pages in
the first site version?

Rule already fixed by spec v2.5, Part I §10: decide on per-zone counts from the first
non-August weeks of live data (run report `resolved_by_zone`), never on the August
sample (72/89 pages empty in the deadest week of the year). Do not reduce the zone
count on August numbers.

Decided by: — · Date: — · Affected: site layout; reads geo_level + municipality_code.

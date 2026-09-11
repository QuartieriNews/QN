# DEC-018 — URL architecture, content identity and the future migration to neighbourhood domains

Status: DECIDED

Question: how are URLs and content identities organised at launch, and how will the
migration to neighbourhood domains happen?

Options: a single central domain with per-neighbourhood URLs and a later one-to-one
migration (**CHOSEN**); separate domains from day one; a single domain with no planned
migration.

Claude recommendation: coincides with the Round 2 "hard to reverse" technical
requirement (§6.5): canonical identity and URL strategy before publication.

ChatGPT recommendation: the same ("canonical strategy before publication").

## Rule

- One central domain with URLs organised by neighbourhood
  (`quartierinews.it/acilia/`, `quartierinews.it/acilia/articolo-x`).
- Every content has a permanent internal identity, one main neighbourhood and one
  canonical URL. When it appears on several pages, the cards link to the same content;
  no indexable copies.
- Autonomous domains (`acilia.news`) are bought and activated in a later phase, with a
  one-to-one correspondence and permanent redirects, without double indexing. Strong
  brand autonomy per masthead, with the QN group membership evident.
- Articles, stories and dossiers: an article has its own URL; an optional, minimal
  internal story links the articles of the same affair; a dossier is a possible public
  page outside the MVP. A new development produces a new linked article; a correction
  modifies the existing one (DEC-020). This arrangement is provisional and will be
  re-examined.

Impact: site, publisher, `content_id` (spec v2.5 already excludes Municipio and
neighbourhood from the identity), optional story data model.

Blocks: nothing (this entry unblocks the construction of the site and the publisher).

Decided by: Owner · Date: 11 September 2026 (Strategic Council Round 2 Reconciliation,
owner confirmation) · Affected: site, spec v2.5 Part III (identity), future domains.

# DEC-101 — Images: download and serve locally

Status: DECIDED (release 1.4.2)

Rule: the source event image is downloaded at first ingestion and served locally at
card resolution, with five required mitigations (credit + source link; stored
provenance; reduced resolution; working takedown route via image_removed falling back
to the generated card; no watermarked/commercial assets). The generated fallback card
is mandatory. Supersedes the "never public" rule of spec ≤ 2.4.

Decided by: Owner · Date: August 2026 (release 1.4.2) · Affected: Phase 3.1, Part I §8,
media block of the canonical contract. Rationale: docs/PROJECT_HANDOVER.md §2.15.

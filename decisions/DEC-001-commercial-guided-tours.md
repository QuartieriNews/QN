# DEC-001 — Commercial guided tours

Status: OPEN
Blocks: editorial filter activation (spec v2.5, Phase 3.5)

Question: paid guided tours (~20 of 107 sampled events, ~19% of the corpus) are
classified `promotion` by the editorial gate as written. Publish or exclude?

Options:
A. Exclude — they are commercial products; the gate stands as written.
B. Publish as local_interest — they are genuinely things to do in the neighbourhood;
   add an explicit carve-out rule to EDITORIAL_FILTER.md.
C. Publish with a cap or label (e.g. max N per zone per week) — needs a new mechanism.

Claude recommendation: B, on the spec's own "start wide" principle (exclude only what
is clearly ordinary commercial programming; a fifth of the corpus is too much signal
to discard before measuring). C only if the published sample later shows tour spam.

ChatGPT recommendation: (to be added on first review cycle)

Impact: ~19% of acquired events; the placeholder block in
`tests/golden_set_editorial.json → known_gap` becomes scoreable once decided.

Decided by: — · Date: — · Affected: EDITORIAL_FILTER.md, golden_set_editorial.json,
Phase 3.5.

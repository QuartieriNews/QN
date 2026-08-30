# DEC-104 — AI development loop: repo public, samples out, decisions in

Status: DECIDED

Rule, three parts:
1. The decision log lives in this repository (`decisions/`), because both AIs in the
   development loop must read every decision on every cycle without connectors. The
   Drive decision log becomes a pointer to this folder.
2. Raw sampled source data (tests/samples/) is removed from the repository and lives
   only in the release packages on Drive (QN Hub / 20 Packages), per DEC-102. Scripts
   that need a sample take it as a local path argument.
3. The repository stays public: with personal data removed it contains only code,
   reference data and conventions, and a public repo is what lets the reviewing AI
   read it from a flat-rate chat session at zero marginal cost.

Roles under this model: Claude builds, ChatGPT reviews (mandate in
reviews/REVIEW_MANDATE_CODE.md), the owner decides (this folder) and operates the
hands-on steps (n8n, credentials, deploy clicks). Trust grows on measured numbers
(first-pass approval rate, regressions), not on declarations.

Decided by: Owner · Date: 29 August 2026 · Affected: repository layout, Operating
Model v1.1 (Drive), review workflow.

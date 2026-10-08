# QN-TC-045 — n8n 2.42 stable Agent features

Status: Candidate for staging pilot only; no implementation approved.

What changed: In October 2026 n8n 2.42 became stable. By October 7 the stable release was 2.42.4. The line includes Agent queue persistence and related session improvements discussed in QN-TC-043.

Why QN: May reduce custom engineering for long-running Agent orchestration in n8n.

Benefit: Faster implementation, fewer moving parts and better resilience if testing confirms the features.

Risks: Cloud plan/version differences and ambiguous state after retries.

Impact: Architecture high; security medium; cost medium potential; speed high potential.

Proposed action: Verify QN Cloud's runtime and feature availability. Test no-write session recovery and state isolation in staging. Council Claude and OpenAI must independently approve any production work.

Evidence: https://github.com/n8n-io/n8n/releases/tag/n8n%402.42.4

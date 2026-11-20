# QN-TC-047 — Haiku 5.5 pricing for QN classification

Status: CANDIDATE — independent Claude + OpenAI review required; no implementation authorized.

What changed: Anthropic launched Haiku 5.5 on 7 October 2026, with a 1M-token context window, 128K max output, and input/output prices of $0.10/$0.50 per million tokens for prompts up to 100K. Prices are five times greater for prompts above 100K. Sonnet 5.5 prompt-cache reads dropped from $0.20 to $0.10 per million tokens.

Why QN: Potential cheaper municipality/neighborhood classification, event triage and source routing; more economical cached Sonnet developer prompts.

Expected benefit: Significant latency and unit-cost reduction on high-volume small tasks, to be benchmarked.

Risks: Misclassification, greater prices above 100K, changed token accounting and adaptive-thinking response handling.

Impact: cost high; speed high; architecture medium; security low to medium.

Proposed action: Shadow-mode benchmark of 100-200 labeled QN records versus current pipeline; measure precision, recall, routing errors, latency and billed cost. No automatic publication. Independently review with both council models before any change.

Evidence: https://www.anthropic.com/claude-haiku-5-5 and https://platform.claude.com/docs/en/models/haiku-5-5/overview

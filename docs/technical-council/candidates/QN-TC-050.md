# QN-TC-050 — OpenAI Decisions API for lightweight QN content triage

**Status:** CANDIDATE — independent Claude + OpenAI review; NOT authorization to implement.

**What changed (2026-10-06, newly assessed 2026-10-08):** The public-beta Decisions API evaluates text/images as typed predicate, choice or score questions, with claimed roughly 10x response speed compared with the Responses API. Available on gpt-6-luna only. Base price is $0.10 per million input tokens, with no output-token charge; long-context and regional multipliers may apply.

**Why QN:** High-volume intake needs initial locality, municipality, news/event relevance and review-priority classification, not always full prose generation.

**Expected benefit:** Lower latency and cost for structured, reversible routing decisions.

**Risks:** Beta API instability; miscalibrated probabilities; missing important stories through false negatives. It is not a fact-checker and must not automatically publish or permanently discard content.

**Impact:** architecture medium; cost high potential saving; speed very high potential; security low-medium.

**Proposed action:** Run a shadow-only, labeled 100-200-record QN trial, comparing decisions with existing rules and Haiku 5.5. Track false negatives, calibration, effective bill and latency. Route uncertain items to fuller review. Claude and OpenAI must independently validate before any workflow changes.

**Evidence:** https://developers.openai.com/api/docs/changelog and https://developers.openai.com/api/docs/guides/decisions

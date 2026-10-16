# QN-TC-020 — GPT-6 Sol/Luna and improved prompt caching reshape the economics of the QN OpenAI lane

**Status:** NEW — CANDIDATE FOR MODEL-ROUTING + COST BENCHMARK / COUNCIL REVIEW  
**Area:** OpenAI models, reviewer lane, API cost, persistent agents, caching, speed  
**Impact:** architecture **medium**; security/quality **medium**; cost **very high**; speed **high**

## What changed
OpenAI released **GPT-6 Sol and GPT-6 Luna** as lower-cost GPT-6 models. API list pricing is **$2/M input and $10/M output for GPT-6 Sol**, and **$0.10/M input and $0.50/M output for GPT-6 Luna** — 50% below the promotional GPT-5.6 Sol/Luna prices cited by OpenAI. Both are available in Codex and via the API as `gpt-6-sol` and `gpt-6-luna`; GPT-6 Astra remains OpenAI's highest-capability GPT-6 model.

OpenAI also introduced an improved GPT-6 prompt-caching system aimed at persistent agents and long conversations. Eligible shared prefixes reused within a 30-minute window can receive discounts of up to **90% on cached input-token reads**. New tooling includes a Prompt Caching Dashboard and cache-miss diagnostics; developers can use explicit cache breakpoints, adjust reasoning effort, and change tool availability in ways designed to preserve reusable context instead of invalidating the whole cache.

OpenAI's published evaluations show Sol and Luna improving materially over their GPT-5.6 predecessors in coding, business workflows and computer use at lower cost. Those are vendor evaluations and are not a substitute for a QN-specific benchmark.

## Why it matters for QN
QN-TC-001 currently frames **GPT-6 Astra** as the OpenAI reviewer/automation candidate. Sol and Luna introduce a potentially better economic structure: QN may not need the most expensive model for every review, log triage or routine agent turn.

A possible future pattern is **Astra for the hardest/highest-risk reviews, Sol for most strong reviewer work, and Luna only for low-risk/high-volume tasks** — but only if QN-specific tests show that the cheaper tiers preserve the independent-review quality the Council requires.

The caching changes matter separately because QN's planned long-running agents repeatedly carry the same project instructions, tool schemas, workflow definitions and repository context. Better cache reuse could materially reduce the cost and latency of persistent OpenAI sessions and make background forks/subagents more economical.

## Expected benefit
- Potentially large reduction in OpenAI review/automation API spend without abandoning the GPT-6 family.
- More room for repeated review/test loops and parallel low-risk tasks.
- Faster persistent-agent turns when stable project/tool context is cached.
- Better cost observability through cache-hit dashboards and diagnostics.
- A more deliberate model-escalation policy instead of using Astra indiscriminately.

## Risks / unknowns
- OpenAI's benchmark and cost-per-task claims are not QN-specific.
- A cheaper reviewer that misses architectural, security or logic defects would be a false economy.
- Multi-model routing can reduce reproducibility unless the selected model/effort level is logged and pinned per task class.
- Cache savings depend on keeping reusable prefixes stable; frequent prompt/tool-schema churn can erase the benefit.
- Cached context still needs the same data-minimization and secret-handling discipline as uncached context.

## Proposed action
Do **not** replace the QN reviewer baseline automatically. Ask Claude + OpenAI to independently review a reversible benchmark that expands QN-TC-001 from a simple Astra comparison into a **three-tier GPT-6 test**:

1. Run the same 5–10 representative QN review/debug/automation tasks through **Astra, Sol and Luna** where appropriate.
2. Measure defect detection, correctness, reviewer disagreement with Claude, repair turns, elapsed time, token usage and effective cost.
3. Test whether Sol can cover the normal reviewer lane while reserving Astra for escalations; use Luna only for tasks whose failure cannot authorize or conceal a production change.
4. Explicitly log/pin model and reasoning effort so Council decisions remain reproducible.
5. In one persistent-agent/API test, hold QN instructions/tool schemas stable, instrument cache-hit rate and compare cost/latency before and after explicit cache optimization.
6. Keep production writes and final promotion outside the cheaper-model routing experiment.

Only if both Council members agree on the measured quality/cost trade-off should QN adopt a tiered OpenAI routing policy or caching-specific architecture changes.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://openai.com/index/introducing-gpt-6-sol-and-luna/
- https://openai.com/index/better-prompt-caching-for-gpt-6/
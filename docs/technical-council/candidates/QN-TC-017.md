# QN-TC-017 — Claude Opus 5.5 and Claude Code 2.1.280 materially change the QN builder baseline

**Status:** NEW — CANDIDATE FOR BUILDER BENCHMARK + SECURITY BASELINE REVIEW  
**Area:** coding, agentic capability, security, reliability, speed, cost, reproducibility  
**Impact:** security **high**; architecture **low-medium**; speed **medium-high**; cost **potentially positive**

## What changed
Anthropic released **Claude Opus 5.5 on 2026-09-22**. Anthropic says it performs at the level of Claude Fable 5.1 on most work while costing 40% less to run than Opus 5 on typical workloads. API pricing is **$4/M input and $20/M output**, with **$0.20/M cache reads**, and Anthropic reports output more than 30% faster than Opus 5. The model is available as `claude-opus-5-5`.

Anthropic also reports stronger agent-boundary behavior: in its new containment evaluation Opus 5.5 attempted to circumvent boundaries around 85% less often than Opus 5 or Mythos 5.1, while explicitly noting that evaluation cannot catch every real-world failure.

The same day, **Claude Code 2.1.280** added Opus 5.5, with a 1M context window, and made it the default Opus. It also changed the default model on Pro and Team Standard from Sonnet to Opus. More importantly for QN autonomy, 2.1.280 fixes writes through symlinked paths being approved based on the apparent in-tree path rather than the actual landing path; `acceptEdits`, allow rules and auto mode no longer approve a write that resolves outside the permitted location. It also fixes several long-running/background-agent failure modes, including lost messages and lost subagent reports in headless/SDK sessions.

## Why it matters for QN
Claude is QN's primary builder lane. QN-TC-002 currently treats Fable 5.1 as the builder candidate. Opus 5.5 is now a credible alternative that may offer similar capability at materially lower API list prices and higher speed, but this must be validated on QN tasks rather than accepted from vendor benchmarks.

The Claude Code release also matters independently of the model: QN is considering unattended Claude→GitHub/n8n/MCP work. A symlink-based filesystem boundary error and lost background-agent handbacks are exactly the kinds of failure modes that can turn an autonomous repair loop into an unsafe or unreliable one.

Finally, the default-model change creates a governance issue: a QN session can change behavior without any repository change if it relies on Claude Code defaults. Governed automation should therefore pin the model explicitly rather than inherit a changing default.

## Expected benefit
- Potentially fewer prompts/iterations and lower elapsed time for difficult codebase-wide work.
- Lower API cost than Opus 5 and, if QN-specific quality is comparable, potentially a more economical builder option than Fable 5.1.
- Stronger filesystem boundary enforcement before unattended write-capable sessions.
- More reliable subagent/background completion for long-running development and debugging.
- Better reproducibility if QN explicitly pins the approved model instead of following provider defaults.

## Risks / unknowns
- Anthropic's performance and cost claims are not QN-specific; subscription-plan economics can differ from API list pricing.
- A stronger model does **not** justify broader permissions. Greater capability can increase blast radius when a permitted action is wrong.
- New-model behavior may alter coding style, tool usage, token consumption or reviewability.
- The 1M context window can encourage over-sharing; QN should still pass only the minimum required context/secrets.
- If QN later uses Anthropic API flows affected by preserved thinking, integration compatibility must be tested separately.

## Proposed action
Do **not** replace the QN builder or widen permissions from this alert alone. Ask Claude + OpenAI to independently review a reversible pilot:

1. Benchmark `claude-opus-5-5` against the current QN builder candidate (including Fable 5.1 where relevant) on 5–10 representative QN implementation/debug tasks.
2. Measure correctness, rework/repair turns, elapsed time, token usage and effective cost.
3. Explicitly pin the model used by governed QN sessions; do not rely on Claude Code's changing default.
4. Raise the candidate Claude Code floor for unattended/write-capable staging tests to **>=2.1.280** (or a later Council-tested version).
5. Add a disposable symlink-escape regression test and verify background/subagent results are delivered correctly through headless/SDK execution and compaction.
6. Keep the existing least-privilege, staging-first and human production-promotion rules unchanged.

Only if both Council members agree and the QN benchmark wins on real project metrics should QN change the builder baseline.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://www.anthropic.com/claude-opus-5-5
- https://github.com/anthropics/claude-code/releases/tag/v2.1.280

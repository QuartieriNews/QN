# QN-TC-029 — Claude Sonnet 5.5 + Claude Code 2.1.284

**Status:** CANDIDATE FOR COUNCIL REVIEW — no implementation authority  
**Date:** 2026-09-29  
**Area:** builder model, coding agents, computer use, MCP/plugins, governed permissions  
**Impact:** architecture **medium**; security **high-positive**; cost **potentially high-positive**; speed **high-positive**

## What changed
Anthropic released Claude Sonnet 5.5 on 2026-09-28 and made it the default Sonnet in Claude Code 2.1.284. Anthropic lists pricing at $2/M input, $10/M output and $0.20/M cache reads, reports 30%+ faster output than Sonnet 5, and reports up to 30% lower cost per task for most work. Anthropic continues to position Opus 5.5 for the hardest open-ended work.

Claude Code 2.1.284 also adds one-time approval for reads outside the workspace, spend-limit visibility, stronger MCP reconnect/managed-policy handling, approval for external symlinked project rules, stricter managed plugin permission behavior, corrected MCP elicitation blocking, and additional sandbox/workflow hardening.

## Why it matters for QN
Claude is QN's builder lane. Sonnet 5.5 may be a faster and cheaper default for routine QN coding, tests, documentation, n8n support and browser work, with Opus reserved for difficult architecture/debugging. Version 2.1.284 also strengthens controls relevant to unattended builder pilots.

## Expected benefit
Potentially lower build cost, faster iteration, stronger computer-use performance, and a safer governed builder environment.

## Risks / unknowns
Anthropic's benchmark and cost claims require QN-specific validation. High reasoning settings can change the economics. Because Sonnet 5.5 becomes the upstream default, QN should retain exact model pinning until the Council approves a change.

## Proposed action
Claude + OpenAI should independently review a QN benchmark of Sonnet 5.5 against the current builder candidate, including coding and visual/browser tasks. Measure correctness, repair cycles, latency, token use and cost. Separately test the 2.1.284 permission/MCP/plugin controls. Consider Claude Code >=2.1.284 as the new unattended-pilot floor only if those tests pass. Do not change the production model or permissions before independent Council confirmation.

## Evidence
- https://www.anthropic.com/claude-sonnet-5-5
- https://github.com/anthropics/claude-code/releases/tag/v2.1.284

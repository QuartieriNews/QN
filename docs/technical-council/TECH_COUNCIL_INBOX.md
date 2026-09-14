# Quartieri News — Technical Council Inbox

> **Governance:** every item in this file is a **candidate for independent review by Claude + OpenAI**. Nothing here authorizes implementation in production. Council outcome should be one of: `APPROVE`, `PILOT`, `DEFER`, `REJECT`.

Last updated: 2026-09-14

## QN-TC-001 — GPT-6 Astra as OpenAI reviewer / automation agent

**Status:** CANDIDATE — council review required  
**Area:** speed, quality, cost, agentic capability

### What changed
OpenAI released GPT-6 Astra with a 1.05M-token context window, 128k max output, API pricing of $10/M input and $50/M output, and materially stronger results on computer use and AutomationBench than GPT-5.6 Sol in OpenAI's published evals.

### Why it may matter for QN
QN's OpenAI lane is intended to review, test and independently challenge Claude's implementation work. Astra may improve end-to-end review, browser/computer validation and automation tasks.

### Expected benefit
Potential reduction in review iterations and better independent detection of workflow/code issues.

### Risks / unknowns
Vendor benchmarks are not QN-specific. Higher token price can make indiscriminate use expensive. Need a QN-specific A/B test before changing the default model.

### Proposed action
Run a controlled QN benchmark on 5–10 representative tasks versus the current OpenAI model. Measure correctness, iterations, latency and cost. Do not migrate globally without council confirmation.

### Evidence
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://openai.com/index/gpt-6-astra/

---

## QN-TC-002 — Claude Fable 5.1 as builder candidate

**Status:** CANDIDATE — council review required  
**Area:** coding, long-running agents, cost

### What changed
Anthropic released Claude Fable 5.1 on 2026-09-01. Anthropic positions it for long-running coding and agentic work. API pricing is $10/M input and $50/M output; cache reads are $0.25/M, with Anthropic estimating materially lower cost for cache-heavy/agentic workloads.

### Why it may matter for QN
Claude is QN's primary builder lane. Fable 5.1 may improve codebase-wide work, debugging, browser use and long sessions while lowering effective cost when cache reuse is high.

### Expected benefit
Fewer repair cycles, stronger long-horizon implementation, potentially lower effective cost in agentic sessions.

### Risks / unknowns
Anthropic's claims need QN-specific validation. Subscription/API limits and real usage economics may differ from published examples.

### Proposed action
Benchmark Fable 5.1 on the same QN task set used for OpenAI comparison. Keep Claude as builder only if it wins on real QN metrics, not brand preference.

### Evidence
- https://www.anthropic.com/claude/fable

---

## QN-TC-003 — OpenAI Agents API as managed agent harness

**Status:** CANDIDATE FOR PILOT — council review required  
**Area:** architecture, speed, maintenance, cost

### What changed
OpenAI launched the Agents API in public beta on 2026-09-10. It exposes the Codex agent harness as a managed service with long-running sessions, automatic context compaction, tool use, MCP support, subagents and optional hosted sandboxes. OpenAI states there is no separate Agents API fee beyond model/tool/environment usage.

### Why it may matter for QN
QN would otherwise need to build or maintain more orchestration glue around long-running OpenAI agents. The managed harness could remove part of that engineering burden while still allowing QN to keep execution boundaries and tools under its control.

### Expected benefit
Less custom orchestration code, easier long sessions, simpler subagent parallelism, lower maintenance overhead.

### Risks / unknowns
Public beta; API may change. Vendor lock-in and operating cost need measurement. Permissions and data boundaries remain QN's responsibility.

### Proposed action
Pilot only in staging on a non-critical QN workflow. Compare against current Codex/OpenAI process for quality, retries, elapsed time and total cost. Do not architect QN around the beta yet.

### Evidence
- https://openai.com/index/introducing-the-agents-api/

---

## QN-TC-004 — n8n official MCP for direct build/debug/test loops

**Status:** CANDIDATE FOR PILOT — council review required  
**Area:** architecture, speed, maintenance, security

### What changed
n8n's official MCP can let compatible AI clients inspect selected workflows, create/edit workflows and data tables, validate them, run tests, read execution logs and iterate on failures. n8n explicitly documents the loop: generate → validate → execute → read error → fix → rerun. Access can be restricted to exposed workflows and read/write tools can require permission.

### Why it may matter for QN
This removes much of the manual handoff between QN's AI agents and n8n. It directly targets the current build/debug loop where a human otherwise relays logs and workflow changes.

### Expected benefit
Largest likely saving in debugging and maintenance. Could materially reduce the human 'centralino' role between Claude/OpenAI and n8n.

### Risks / unknowns
Giving write access to a production automation platform increases blast radius. Needs staging, least privilege, version rollback and an explicit prohibition on agents changing their own permission boundaries.

### Proposed action
Pilot n8n MCP in **staging/read-only first**, then allow writes only to staging workflows. Production promotion remains outside the agent's autonomous authority until the council approves a permission model.

### Evidence
- https://n8n.io/mcp/
- https://blog.n8n.io/n8n-mcp-server/

---

## QN-TC-005 — Claude Code 2.1.269 plugin evals / workflow concurrency; 2.1.270 regression fix

**Status:** CANDIDATE — council review required  
**Area:** quality assurance, observability, speed

### What changed
Claude Code 2.1.269 added `claude plugin eval`, reproducible plugin evaluation reports, and a configurable workflow concurrency limit up to 256 agents. Version 2.1.270 then fixed a regression where read-only Git commands could unexpectedly ask for permission during long sessions.

### Important correction to the previous alert
The earlier alert characterized 2.1.270 as a broad security/permission-hardening release. The verified 2.1.270 release note supports a much narrower claim: it fixes the read-only Git permission regression. The technically useful QN feature here is primarily **2.1.269's plugin eval / workflow tooling**, not a broad new security boundary.

### Why it may matter for QN
QN can use repeatable evals to test whether a Claude skill/plugin actually improves builder performance and to catch regressions before rollout. Controlled parallel agents can also speed independent implementation/test tasks.

### Expected benefit
Better evidence-based plugin/skill decisions; less subjective 'it seems better' evaluation; some development-time reduction from parallel work.

### Risks / unknowns
Parallelism can multiply token usage and errors. Plugin evals measure what the test suite captures, not overall production safety.

### Proposed action
Adopt plugin evals for any QN-specific Claude skill/plugin before production use. Keep agent concurrency low (e.g. 2–5) until QN has real cost/reliability data.

### Evidence
- https://github.com/anthropics/claude-code/releases/tag/v2.1.269
- https://github.com/anthropics/claude-code/releases/tag/v2.1.270

---

## QN-TC-006 — Claude Code weekly capacity changes effective 2026-09-14

**Status:** NEW TODAY — CANDIDATE FOR COST/CAPACITY REVIEW  
**Area:** cost, speed, capacity planning

### What changed
From 2026-09-14, Anthropic's temporary Claude Code weekly boost of 50% ends and is replaced by a permanent 25% increase over the original standard baseline for Pro, Max, Team and seat-based Enterprise plans. Relative to the capacity users had during the temporary boost, this is about **17% less weekly Claude Code capacity** (150 → 125 on an indexed baseline of 100).

### Why it matters for QN
QN currently relies heavily on Claude for builder work. A lower effective weekly ceiling can slow intense development weeks or push more work into paid overage/API usage. This is especially relevant before deciding whether the current Max plan is sufficient for sustained QN development.

### Expected benefit of acting
Better capacity planning and lower risk of builder work stopping mid-sprint. It also creates a reason to deliberately route suitable review/debug tasks to OpenAI instead of consuming Claude quota by default.

### Risks / unknowns
Anthropic has not published fixed token numbers for all plan ceilings; actual consumption varies with model, context length and task complexity. The practical effect on QN must be measured from `/usage`, not inferred only from percentages.

### Proposed action
For the next 2 weeks, record QN-only Claude Code usage and note any limit hits. Do **not** upgrade the plan yet. If QN repeatedly exhausts weekly capacity, council should compare: (a) higher Claude allowance, (b) extra usage/API, or (c) shifting suitable review/debug workload to OpenAI.

### Evidence
- Anthropic announcement via official ClaudeDevs account on 2026-08-29, widely quoted with the clarification that the new level is ~17% below the temporary boosted level.
- Secondary confirmation: https://www.macobserver.com/news/anthropic-raises-claude-code-weekly-limits-by-25-for-paid-plans/

---

## QN-TC-007 — n8n 2.38.7 fixes MCP toolkit execution on workers

**Status:** MONITOR — no immediate QN change proposed  
**Area:** reliability, scale

### What changed
n8n 2.38.7 (2026-09-11) includes a core fix to execute MCP toolkit members on workers.

### Why it may matter for QN
This is relevant if QN later runs n8n in worker/queue mode or at higher scale. It supports the broader direction of using MCP with distributed execution.

### Expected benefit
Improved MCP reliability in worker-based deployments.

### Risks / unknowns
QN is currently on n8n Cloud Starter, so this may require no user action and may have no immediate practical effect.

### Proposed action
No architecture change. Confirm the n8n Cloud version before any MCP pilot; require at least a version that includes this fix.

### Evidence
- https://github.com/n8n-io/n8n/releases/tag/n8n%402.38.7

---

# Council review checklist

For each candidate, Claude and OpenAI should independently answer:

1. Is the underlying factual claim verified by a first-party source?
2. Does this materially improve QN versus the current stack/process?
3. What exact QN problem does it solve?
4. What is the smallest reversible pilot?
5. What new failure/security/cost modes does it introduce?
6. What measurable success criterion would justify adoption?
7. Verdict: `APPROVE`, `PILOT`, `DEFER`, or `REJECT`.

No candidate moves to implementation solely because it appears in this inbox.
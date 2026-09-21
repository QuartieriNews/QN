# QN-TC-016 — Claude Code 2.1.277 hardens headless failure handling and compound-command sandbox boundaries

**Status:** NEW — CANDIDATE FOR AUTONOMY SECURITY / RELIABILITY REVIEW  
**Area:** security, sandboxing, headless agents, subagents, reliability  
**Impact:** security **medium-high** for autonomous execution; architecture **low**; reliability **medium-high**; speed **low-medium**; cost **negligible**

## What changed
Anthropic released Claude Code **2.1.277 on 2026-09-18**. Several changes are directly relevant to a future unattended QN builder/repair loop:

- A `sandbox.excludedCommands` glob could previously exempt an **entire compound Bash command** when only one component matched. Claude Code now requires every component to match before the compound command is excluded from the sandbox.
- `claude -p` and Agent SDK sessions that hit an internal error could hang without returning a result. They now report the error and exit with **code 1**, giving a supervisor/orchestrator a reliable failure signal.
- Subagent results are now explicitly framed as subagent output before reaching the main agent, reducing the chance that text produced by a subagent is interpreted as session-level instructions.
- The release adds native `AGENTS.md` fallback support only when a project has **no `CLAUDE.md`**.

Anthropic then released **2.1.278 on 2026-09-19**. Its main change is that API/Enterprise/Bedrock/Vertex/Foundry/gateway auto mode defaults to a server-side classifier whose classifier overhead is not billed. This may matter later if QN runs Claude through those deployment modes, but it is not the main reason for this candidate.

## Why it matters for QN
QN is designing progressively more autonomous Claude workflows, including headless/agentic work and eventual controlled interaction with n8n/GitHub. In that model, two properties matter independently of model quality: a command that is partly exempt must not accidentally escape the sandbox as a whole, and an internal agent failure must produce a machine-readable failure instead of leaving an orchestration loop hanging.

The `AGENTS.md` addition does **not** require a QN instruction-layout migration. QN already has `CLAUDE.md`, and that file explicitly tells Claude to read `AGENTS.md` first. The new fallback therefore does not silently change QN's current instruction source.

A repository search on 2026-09-21 found no current QN use of `sandbox.excludedCommands`, so this is a **future-autonomy prerequisite**, not evidence of a current exploit or incident.

## Expected benefit
- More trustworthy sandbox boundaries for compound shell commands in future autonomous/headless sessions.
- Cleaner fail-closed orchestration: an internal Claude failure can stop/retry a job on non-zero exit instead of hanging indefinitely.
- Lower prompt-instruction confusion between main-agent and subagent output.
- No need to redesign QN's existing `CLAUDE.md` → `AGENTS.md` instruction hierarchy.

## Risks / unknowns
- The sandbox fix only protects configurations that actually use Claude Code sandboxing correctly; it is not a substitute for least-privilege GitHub/n8n credentials or network restrictions.
- QN does not currently use `sandbox.excludedCommands`, so the immediate benefit is limited until unattended execution is introduced.
- Exit code 1 improves supervision but QN still needs explicit retry/circuit-breaker rules; blindly retrying every internal error could create loops or unnecessary spend.
- The 2.1.278 server-side classifier billing change may be irrelevant while QN uses subscription-based Claude Code rather than API/Enterprise deployment.

## Proposed action
Do **not** change production or the current n8n workflow from this alert. Ask Claude + OpenAI to independently review whether the future QN unattended/headless pilot should require a tested Claude Code build **>=2.1.278** and add two small acceptance tests before autonomous execution is enabled:

1. **Compound-command sandbox test:** construct a harmless compound Bash command where only one component matches an `excludedCommands` rule and verify the other component remains sandboxed/subject to permission controls.
2. **Headless failure-propagation test:** force a controlled failure in a disposable `claude -p` / Agent SDK session and verify the supervising process receives a non-zero exit, stops safely, and does not continue into write/deploy steps.

Also verify that QN keeps its current explicit instruction chain (`CLAUDE.md` exists and points to `AGENTS.md`) rather than migrating merely because the new fallback exists. If QN later adopts API/Enterprise auto mode, separately measure whether 2.1.278's server-side classifier reduces billed overhead in practice.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://github.com/anthropics/claude-code/releases/tag/v2.1.277
- https://github.com/anthropics/claude-code/releases/tag/v2.1.278
- QN `CLAUDE.md` (explicitly reads `AGENTS.md` first; staging/no-production boundary)
- QN repository search on 2026-09-21: no `sandbox.excludedCommands` occurrence found

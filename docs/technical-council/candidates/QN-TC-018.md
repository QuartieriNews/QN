# QN-TC-018 — n8n 2.40.5 is now stable, triggering the previously deferred QN 2.40 staging pilot

**Status:** NEW — CANDIDATE TO ACTIVATE STAGING PILOT / COUNCIL REVIEW  
**Area:** n8n, AI agents, MCP, workflow editing, resilience, security  
**Impact:** security **medium-high**; architecture **low**; reliability **high**; speed **medium**; cost **low-medium**

## What changed
The QN Council inbox previously tracked n8n 2.40.x while it was pre-release and proposed waiting until the line reached stable/Cloud before testing its AI-agent changes. That trigger has now occurred: GitHub marks **n8n 2.40.5 as the stable release**, dated 2026-09-21.

The 2.40 line contains several changes directly relevant to QN's proposed agent-operated workflow model: support for a **fallback model alongside the primary model** on AI nodes; model/trust boundaries around external tool results; preservation of node settings, positions and error routes through AI Assistant edits; execution of MCP toolkit members on workers; broader secret redaction; and reliability fixes around provider streams, queue jobs and workflow publication.

The next 2.41.0 line is already visible as a pre-release, so this candidate deliberately targets the stable 2.40.5 baseline rather than chasing the newest pre-release.

## Why it matters for QN
QN-TC-011 proposed a staging pilot only after n8n 2.40 became stable. This is therefore not just another release note: the explicit condition for that pilot has been met at the upstream release level.

The relevant QN use case is Claude/OpenAI inspecting and eventually editing n8n workflows. A fallback model can reduce single-provider interruption; preserved workflow structure makes AI-assisted edits safer; and external-tool trust boundaries add defense-in-depth against instructions arriving through MCP/tool outputs.

QN uses n8n Cloud, so the upstream stable tag does not prove that the specific QN Cloud instance has already been rolled forward. Instance-version verification remains a prerequisite.

## Expected benefit
- Ability to run the previously deferred 2.40 staging tests on a stable upstream baseline.
- Lower risk that an AI Assistant edit silently damages unrelated retry/error-route/node configuration.
- Better continuity when a primary model is unavailable or rate-limited.
- Additional prompt-injection defense around external tool/MCP content.
- Improved worker/MCP and long-running execution reliability.

## Risks / unknowns
- Stable upstream does not guarantee that QN Cloud is already on 2.40.5.
- A fallback model can change behavior as well as restore availability; outputs may differ across providers.
- Trust boundaries reduce but do not eliminate prompt injection.
- AI workflow edits still require versioning, diff inspection, tests and rollback.
- n8n 2.41.0 is pre-release and should not be adopted merely because it is newer.

## Proposed action
Do **not** change QN production automatically. Ask Claude + OpenAI to confirm that QN-TC-011 can move from "wait for stable" to a **staging pilot** once the actual QN Cloud instance is confirmed on **>=2.40.5** (or a later stable version containing the same fixes).

The reversible pilot should test:

1. **Primary/fallback:** force the primary model to fail and verify the fallback takes over predictably; record latency, cost and output differences.
2. **Safe workflow round-trip:** make an unrelated AI Assistant edit to a workflow with retries, credentials, node positions and error routes; verify the diff contains only the intended change.
3. **Untrusted tool content:** feed an adversarial MCP/tool result and verify it is bounded as external/untrusted content rather than accepted as higher-priority instructions.
4. **MCP/worker reliability:** run a representative MCP tool workflow and confirm expected execution/logging behavior.
5. Keep production promotion outside autonomous agent authority.

If the QN Cloud instance has not yet received 2.40.5+, wait for the managed rollout rather than bypassing Cloud stability controls.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://github.com/n8n-io/n8n/releases/tag/n8n%402.40.0
- https://github.com/n8n-io/n8n/releases/tag/n8n%402.40.5

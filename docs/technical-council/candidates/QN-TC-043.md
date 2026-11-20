# QN-TC-043 — n8n 2.42 prerelease may remove the need for custom Agent persistence and handoff glue

**Status:** CANDIDATE — ARCHITECTURE WATCH; DEFER IMPLEMENTATION UNTIL STABLE  
**Area:** n8n Agents, durable orchestration, shared context, approvals, identity, cost  
**Impact:** architecture **high positive potential**; speed **high positive potential**; security **medium-high**; cost **low-to-medium positive potential**

## What changed
The n8n 2.42.0 prerelease adds a durable Agent message-queue foundation, shared Agent context access, connection of Preview/integrations to the Agent queue, queued-message controls, approval settings for Agent channel actions, owner-scoped Agent preview sessions, checks of credentials against the person running a workflow, a write lock in Agent Builder, and publishing-user attribution on triggered executions. The same release also adds prompt caching to the Anthropic Message operation.

## Why it matters for QN
QN has been considering long-running/self-correcting Agent workflows and Claude/OpenAI handoffs around n8n. Native durable queueing, shared context and identity-aware execution could replace part of the custom state, retry and handoff layer we would otherwise build ourselves.

## Expected benefit
Potentially less glue code and fewer handoff/reconnect failures, clearer action ownership, safer approval flows and lower repeated-prompt cost for Anthropic calls.

## Risks / unknowns
2.42 is still marked pre-release. Queue replay can duplicate external writes if idempotency is weak; shared context can cause data/privilege bleed; credential checks tied to the running person may complicate unattended service execution; and feature exposure may differ by n8n Cloud plan.

## Proposed action
Do not move QN production to 2.42 yet. Avoid investing heavily in a custom durable Agent queue/shared-context layer unless urgently needed. Once 2.42 reaches a stable QN Cloud release, run one staging pilot that resumes a no-write Agent across reload/reconnect, verifies owner isolation and approval identity, tests queue replay/idempotency, verifies runner-credential semantics, checks shared-context isolation, and measures Anthropic prompt-cache savings. Only after independent Claude + OpenAI confirmation should this influence the production architecture.

## Evidence
- https://github.com/n8n-io/n8n/releases/tag/n8n%402.42.0

This candidate is review material only and does not authorize implementation.

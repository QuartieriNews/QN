# QN-TC-019 — Codex 0.156.0 closes sandbox gaps and improves worktree/usage controls for the QN reviewer lane

**Status:** NEW — CANDIDATE FOR REVIEWER SECURITY BASELINE UPDATE / COUNCIL REVIEW  
**Area:** security, reviewer isolation, worktrees, observability, MCP, cost tracking  
**Impact:** security **high**; architecture **low**; reliability **medium**; speed **low-medium**; cost **low**

## What changed
OpenAI released **Codex 0.156.0 on 2026-09-22**. The release closes several sandbox isolation gaps, including non-loopback inbound connections in the Windows offline sandbox, privileged Linux/macOS socket cases, and writes through read-only macOS file handles.

It also makes **worktree support enabled by default** for agent command-center sessions, adds a `/usage` analytics view for account usage, token totals and plugin/skill activity, improves MCP OAuth recovery when discovery temporarily returns HTTP 503, and includes additional permission/profile hardening such as invalidating cached Guardian approvals when permission scope widens without scoring.

## Why it matters for QN
QN-TC-015 already proposed turning the Codex reviewer rule from a prompt-only convention into a technical least-privilege boundary. Version 0.156.0 is a better candidate floor for that pilot because it directly fixes sandbox isolation issues and makes disposable worktree-based review easier to operate.

The `/usage` analytics view is also useful for the Council: QN can measure the real cost and activity of the reviewer lane, including plugin/skill usage, rather than deciding from anecdotal impressions.

## Expected benefit
- Stronger isolation for the reviewer before it receives broader repository context or tool access.
- Easier disposable worktree sessions for reproducible review/testing without touching the main working tree.
- Better usage/cost observability for deciding how much review work should remain with Codex versus Claude.
- More resilient MCP authentication during transient provider failures.
- A cleaner technical foundation for enforcing “reviewer does not hold the pen.”

## Risks / unknowns
- A worktree is not itself a remote-permission boundary; Codex could still push or mutate external systems if credentials/tools allow it.
- Sandbox fixes show that previous versions had isolation gaps, so QN still needs acceptance tests rather than trusting version numbers alone.
- Auto-review/Guardian does not equal a truly read-only GitHub or n8n role.
- More instrumentation can show token/plugin activity but does not by itself prevent unsafe actions.

## Proposed action
Do **not** expand Codex permissions from this release alone. Ask Claude + OpenAI to independently review whether **Codex >=0.156.0** should supersede the >=0.155.1 floor proposed in QN-TC-015 for the disposable reviewer pilot.

Pilot acceptance criteria:

1. Run Codex in a disposable worktree/sandbox and confirm it can read the repository/diff, execute the review/test suite and post review comments.
2. Confirm it cannot commit, push, merge or write to production n8n/other production systems under the reviewer credential/profile.
3. Exercise the sandbox boundary cases relevant to the QN host OS and verify failure is closed and explicit.
4. Capture `/usage` data for token totals and plugin/skill activity to establish a reviewer cost/behavior baseline.
5. Verify MCP auth recovery does not silently broaden permissions after a transient login/discovery failure.
6. Only after both Council members approve the results should DEC-104 / `AGENTS.md` be changed to encode the reviewer restriction technically.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://github.com/openai/codex/releases/tag/rust-v0.156.0

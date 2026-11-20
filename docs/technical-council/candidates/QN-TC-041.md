# QN-TC-041 — Claude Code 2.1.289 policy-composition hardening

**Status:** CANDIDATE  
**Area:** managed policy, Mods/plugins, MCP, filesystem, unattended sessions  
**Impact:** security **very high**; reliability **high**; architecture **low**; cost **negligible**; speed **neutral**

## What changed
Claude Code 2.1.289 fixes policy-composition issues across managed deny/ask rules, Mods/plugins, symlinked IDE reads, sandbox command parsing, and organization-managed MCP sign-in tool descriptions.

## Why it matters for QN
QN plans to combine managed policy, MCP, plugins/Mods, filesystem restrictions and unattended execution. Lower-level approvals must never weaken higher-level boundaries.

## Expected benefit
Stronger defense-in-depth and safer unattended builder sessions.

## Risks / unknowns
The known fixes do not prove every interaction between policy layers is safe. Mods remain privileged and should stay disabled by default.

## Proposed action
Ask Claude + OpenAI to independently review Claude Code >=2.1.289 as the candidate floor. Retain regression tests for layered policy behavior before any production permission change.

## Evidence
- https://github.com/anthropics/claude-code/releases/tag/v2.1.289

Review material only; no implementation approval.

# QN-TC-053 — Codex 0.162.0: reviewer sandbox and Guardian hardening

**Status:** CANDIDATE for independent Claude + OpenAI technical council review — NOT approved for deployment.
**Detected:** 2026-10-09; **release:** 2026-10-08.

## What changed
OpenAI released Codex 0.162.0 stable. It fixes Linux sandbox startup with multiple denied paths; rejects writable sandbox-construction executables; prevents ripgrep configuration from weakening deny-glob masks; and includes work on preserving user restrictions during Guardian handoffs and preventing Guardian Decisions API keys from being forwarded to environments. It also adds managed Git worktree creation/listing from trusted local projects when enabled and opt-in ranked tool search for Code Mode.

## Why it matters for QN
The independent OpenAI reviewer will inspect Claude's work without permission to modify production, GitHub main, or n8n workflows. Robust sandbox denied-path enforcement and preserved Guardian user restrictions are directly relevant to separating builder and reviewer privileges.

## Expected benefit
Reduced accidental privilege leakage and better review isolation; potentially simpler disposable parallel review worktrees.

## Risks and limitations
Patch claims need verification in QN's runtime. Worktree creation is a write-capable operation and should be disabled for review-only lanes until reviewed. Server defaults can change between sessions, so explicit model/version selection remains necessary. Guardian checks cannot substitute external role/credential restrictions.

## Impact
Architecture: LOW; Security: HIGH; Cost: NEUTRAL/VARIABLE; Speed: LOW-MEDIUM positive potential; Reliability: MEDIUM positive potential.

## Proposed action (NOT implementation approval)
Supersede QN-TC-049's Codex 0.161.0 baseline with >=0.162.0 only as a staging reviewer candidate. Test denied paths (including multiple paths), bypass attempts via ripgrep configs, modified sandbox executables, restricted Guardian handoffs, reconnect, credential isolation, model pinning, no Git worktree writes/commits/push, and no n8n production write. Obtain separate Claude and OpenAI verdicts before an upgrade.

## Evidence
https://github.com/openai/codex/releases/tag/rust-v0.162.0

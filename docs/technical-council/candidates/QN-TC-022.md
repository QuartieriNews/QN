# QN-TC-022 — Agent conversation-history integrity becomes a QN trust boundary

**Status:** HIGH-PRIORITY SECURITY CANDIDATE — council review required; no implementation authority  
**Date:** 2026-09-25  
**Area:** security, coding agents, local state, MCP/plugins, unattended execution  
**Impact:** architecture **medium**; security **very high**; cost **low**; speed **low-medium**

## What changed
On 2026-09-24 Darktrace published research, after responsible disclosure to Anthropic, OpenAI and AWS on 2026-08-18, showing that several major agentic coding harnesses accept locally stored conversation history without cryptographic validation that the claimed prior model/user/tool messages are authentic. Darktrace reproduced the issue with Claude Code, OpenAI Codex, AWS Kiro-CLI and Pi.

The issue requires an attacker or compromised local component to gain write access to the agent's stored state first; it is not a standalone remote exploit. The important architectural point is that fabricated historical turns can then influence later agent decisions because the harness treats the stored transcript as trusted context. Darktrace recommends provider-side signing and verification of historical messages, which QN cannot implement on its own.

## Why it matters for QN
QN is considering long-running Claude/Codex sessions, MCP/plugin installation, session resume/teleport, subagents and eventually write-capable staging work. Conversation history therefore must not become an implicit authorization source. A compromised dependency that can alter local agent state should not be able to manufacture a prior approval and have that approval accepted during a later privileged run.

## Expected benefit
Treating resumable history as untrusted state would reduce the chance that a compromised package/plugin can turn local state access into a privileged QN action. It also makes the authority model clearer: permissions come from runtime policy, scoped credentials and explicit approval gates, not from what an old transcript claims happened.

## Risks / unknowns
There is currently no user-side mechanism that can cryptographically prove the authenticity of every historical turn across the affected harnesses. Starting privileged work from fresh sessions can reduce continuity and may cost extra tokens/time. Cloud-hosted sessions may reduce exposure to local workstation tampering but should not be assumed immune without provider guarantees.

## Proposed action
Ask Claude and OpenAI to independently review a fresh-session rule for privileged QN work:

1. Production-impacting or credential-bearing actions must derive authority from explicit runtime policy/approval, never from prior conversational claims.
2. Do not resume a mutable local transcript into a higher-privilege execution context.
3. Prefer fresh or ephemeral sessions for write-capable staging or any future production-adjacent task; persist durable task state in reviewed repository files/issues rather than relying on agent history as the source of truth.
4. Separate plugin/MCP/package installation from privileged agent execution.
5. Keep production credentials unavailable to developer/local sessions and use scoped, short-lived credentials where possible.
6. Monitor provider releases for authenticated/signed history and re-evaluate once Anthropic/OpenAI ship a verifiable fix.

No new production access or autonomy is authorized by this candidate.

## Evidence / sources
- Darktrace research, 2026-09-24: https://www.darktrace.com/blog/hijacking-agentic-harnesses-to-attack-an-organization

# QN-TC-024 — Claude Code 2.1.283 adds exact model pinning and stronger governed-session controls

**Status:** CANDIDATE FOR COUNCIL REVIEW — no implementation authority  
**Date:** 2026-09-28  
**Area:** model governance, autonomous coding, MCP/plugins, sandboxing  
**Impact:** architecture **low-medium**; security **high**; cost **negligible**; speed **low-positive**

## What changed
Anthropic released Claude Code **2.1.283** on 2026-09-25. It adds two managed settings directly relevant to QN governance:

- `availableModelsMatch: "exact"`, so an allowlisted model entry authorizes only the exact model version named rather than automatically admitting later releases;
- `deniedModels`, so specific models can be explicitly blocked even if a broader allowlist would otherwise permit them.

The same release adds `/doctor prompt-audit` to audit CLAUDE.md files, skills, agents and commands for prompting patterns written for older models. It also changes managed sandbox parsing so that if one nested sandbox value is invalid, that value fails closed while the rest of the managed sandbox block continues to apply.

For Claude cloud sessions, 2.1.283 also fixes a server-restart recovery bug where an already-finished step could be repeated, including duplicate comments or pushes.

## Why it matters for QN
QN's governance rule is that a new model or materially new agent configuration should be reviewed before it enters a governed builder workflow. Exact model pinning can turn that rule from a convention into an enforceable technical control. The sandbox fail-closed behavior and duplicate-side-effect fix are also relevant to the planned remote/unattended Claude builder lane.

## Expected benefit
- Prevent silent model drift in governed QN sessions.
- Make model upgrades deliberate and reproducible.
- Catch stale prompt/config assumptions before model migrations.
- Reduce risk that one malformed sandbox setting disables broader protections.
- Lower risk of duplicate GitHub side effects after cloud-session recovery.

## Risks / unknowns
- Exact pinning can delay beneficial model updates until QN explicitly approves them.
- A pinned model still needs QN-specific evals and does not guarantee safe behavior.
- Prompt-audit is advisory; it does not replace tests.
- Cloud-session recovery still requires idempotent workflows for sensitive writes.

## Proposed action
Ask Claude + OpenAI to independently review whether governed QN sessions should adopt exact model pinning and an explicit denylist. If both agree, test in staging:
1. pin the current approved Claude model exactly and verify a newly available model remains blocked;
2. add one denied model and confirm it cannot be selected;
3. run `/doctor prompt-audit` on QN instructions before any model migration;
4. inject one invalid nested sandbox setting and verify the remainder of the managed sandbox remains active;
5. in a disposable cloud-session test, simulate interruption/recovery and confirm no duplicate push/comment side effect occurs.

Do not change production permissions or default models until the Council confirms the test results.

## Evidence
- https://github.com/anthropics/claude-code/releases/tag/v2.1.283

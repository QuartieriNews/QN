# QN-TC-015 — Codex 0.155.x strengthens approval evidence; QN reviewer permissions should become technical, not prompt-only

**Status:** NEW — CANDIDATE FOR REVIEWER SECURITY HARDENING / COUNCIL REVIEW  
**Area:** security, reviewer governance, MCP, authorization, reliability  
**Impact:** security **high**; architecture **low**; reliability **medium**; speed **low-medium**; cost **negligible**

## What changed
OpenAI released Codex CLI **0.155.0 on 2026-09-17** and the stable patch **0.155.1 on 2026-09-18**. The 0.155.0 release materially strengthens the authorization/review layer used around agent actions: automatic approval reviews preserve the complete action plus authorization evidence more reliably, retry transient review failures, and distinguish review-system failures from findings that an action is actually unsafe. The same release improves MCP OAuth-expiry reporting and includes additional sandbox/credential hardening; 0.155.1 is the small stable follow-up patch on top of that line.

Separately, OpenAI's current security guidance explicitly recommends moving Codex users away from **full-access mode** toward **auto-review mode** for high-capability workflows. Auto-review evaluates actions requiring elevated permissions before execution and can block requests that present significant destructive risk; OpenAI also recommends sandboxing/isolation, scoped permission profiles and monitoring of agent actions.

## Why it matters for QN
QN's existing governance already says the Codex reviewer **finds defects and never holds the pen**, while the owner decides and merges. However, `AGENTS.md` currently records that the reviewer app **technically holds write permissions** and relies on the role rule not to use them except for review/comments.

That creates a mismatch with the security direction already emerging from the QN Council: a prompt or role instruction should not be the only boundary when a capability can be denied technically. The stronger Codex approval/review controls make this a good moment to test whether the reviewer lane can be least-privilege by construction rather than merely by convention.

## Expected benefit
- Makes the reviewer/builder separation enforceable at the capability layer, not only in prose.
- Reduces the chance that a reviewer session accidentally commits, pushes, merges or performs an unintended write through MCP/tools.
- Improves auditability because approvals carry more complete action/authorization evidence.
- Reduces false or ambiguous review failures by separating unsafe-action findings from approval-service failures.

## Risks / unknowns
- A stricter reviewer profile may block legitimate reproducibility steps if tests need temporary filesystem writes, generated artefacts or disposable worktrees.
- Auto-review is not equivalent to a fully read-only capability model; the exact GitHub/MCP permissions still need to be tested.
- The PR-review integration must still be able to post comments/reviews while being unable to mutate repository content.
- Security controls can add friction or latency, so QN should measure whether the reviewer still completes the normal test/review loop reliably.

## Proposed action
Do **not** change production or DEC-104 from this alert alone. Ask Claude + OpenAI to independently review a small, reversible pilot using **Codex >=0.155.1** on a disposable QN branch/PR:

1. Run Codex in auto-review / least-privilege mode rather than full-access where supported.
2. Confirm the reviewer can read the repository and diff, run the QN review/test suite, and post PR review comments.
3. Confirm it cannot commit, push, merge, alter protected repository files, or write to production n8n/other production systems.
4. If tests require local writes, confine them to a disposable sandbox/worktree and keep remote GitHub/n8n mutation permissions denied.
5. Capture approval evidence and failure modes during the test.
6. If the pilot passes and both Council members agree, update DEC-104 / `AGENTS.md` so the reviewer rule is enforced technically rather than relying on the current statement that write capability exists but must not be used.

This item is **review material only** and does not authorize implementation.

## Evidence
- https://github.com/openai/codex/releases/tag/rust-v0.155.0
- https://github.com/openai/codex/releases/tag/rust-v0.155.1
- https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/
- QN `AGENTS.md` (DEC-104 reviewer role and current technical write-permission note)

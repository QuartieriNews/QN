# QN-TC-021 — Claude Code 2.1.281 hardens policy inheritance, MCP/plugin validation and unattended execution

**Status:** CANDIDATE FOR COUNCIL REVIEW — no implementation authority  
**Date:** 2026-09-24  
**Area:** security, MCP/plugins, autonomous coding, scheduled/headless sessions, reliability  
**Impact:** architecture **low**; security **high**; cost **negligible**; speed/reliability **medium-high**

## What changed
Anthropic released Claude Code **2.1.281** on 2026-09-23. The release contains several changes directly relevant to QN's planned Claude → MCP → n8n/GitHub workflow:

- `claude plugin validate` now detects MCP entries that would be silently dropped, undeclared `${user_config.*}` references and insecure MCP URLs.
- Workspace/security restrictions supplied through `--setting-sources` / SDK `settingSources` are now inherited by spawned teammates, `/bg`, `claude agents`, and `--worktree --tmux` sessions instead of being lost when child sessions start.
- `claude --bg` no longer starts project hooks in a directory that has not passed workspace trust; unattended starts fail/exit rather than silently running there.
- A recursive `rm` whose target is produced only by command substitution (for example `rm -rf "$(pwd)"`) now prompts even under auto / dangerously-skip-permissions conditions unless an explicit override disables the protection. NUL-containing permission rules no longer expand into wildcard matches, and additional sandbox `excludedCommands` matching gaps were fixed.
- MCP hooks on blocking events such as `PreToolUse` now wait for the MCP server connection instead of being skipped while the server is still connecting.
- Several headless/remote reliability bugs were fixed: infinite turn retry despite `--max-turns`, lost/altered resume history, prompt-cache loss around MCP reconnects, duplicated tool calls after proxy stream events, stalled SDK MCP handshakes, scheduled cloud turns missing newly available tools/MCP changes before their first tool call, and scheduled task `/loop` wakeups retrying every second after delivery failure.

## Why it matters for QN
QN is evaluating a governed autonomous builder lane in which Claude may spawn subagents/worktrees, use MCP tools, inspect or edit workflows, and eventually perform staging-only repairs. In that model, a parent session being correctly restricted is not enough if child/background sessions can lose the same policy. Version 2.1.281 specifically closes that inheritance gap and strengthens preflight validation of the MCP/plugin surface.

It also reduces two failure classes that matter for unattended operation: destructive shell edge cases escaping expected prompts, and an orchestrator mistaking retries/duplicate tool calls/stale scheduled context for successful work.

## Expected benefit
- More reproducible least-privilege policy across the full Claude agent tree, not only the root session.
- Earlier detection of malformed or insecure MCP/plugin configuration before a QN run starts.
- Lower probability of destructive filesystem commands executing without the intended gate.
- More reliable headless/scheduled sessions and less risk of duplicate side effects after proxy/MCP failures.
- Better confidence that staging tests reflect the same restrictions future child agents will actually receive.

## Risks / unknowns
- This remains product hardening, not proof that unattended production writes are safe.
- New policy features can still regress in later versions; a version floor must be paired with regression tests, not treated as a permanent guarantee.
- MCP URL-mode elicitation was also added in this release, so browser-based flows can be initiated by compatible MCP servers. QN should treat this as an additional capability surface and allow it only where the server and destination are approved.
- The release is one day old; QN should not make it the production baseline solely because it is newest.

## Proposed action
Ask Claude and OpenAI to independently review whether QN should **supersede the unattended-Claude pilot floor from >=2.1.280 to >=2.1.281**. If both agree, run a small staging-only regression pack before changing any governed baseline:

1. Start a parent session with restricted `settingSources`; spawn `/bg`, an agent and a worktree session; verify the restrictions are identical in every child.
2. Attempt to launch a background session from an untrusted workspace and verify it cannot run project hooks unattended.
3. Run `claude plugin validate` against QN's approved MCP/plugin configuration and fail the pilot on insecure URLs, silently dropped entries or undeclared user-config references.
4. Exercise command-substitution `rm`, malformed/NUL permission rules and sandbox exclusions; verify prompts/denials match policy.
5. Hold the MCP server connection during a blocking hook and verify the hook waits rather than being skipped.
6. In a disposable environment, simulate a proxy/MCP interruption and confirm there are no duplicated write/tool side effects and `--max-turns` is respected.
7. Treat MCP URL elicitation as denied by default unless the server and target flow are explicitly Council-approved.

No production permission expansion, n8n write access, or autonomous deployment is authorized by this candidate. Implementation should be considered only after independent Claude + OpenAI Council confirmation.

## Evidence / sources
- Anthropic Claude Code v2.1.281 release notes (2026-09-23): https://github.com/anthropics/claude-code/releases/tag/v2.1.281

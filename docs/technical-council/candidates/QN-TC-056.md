# QN-TC-056: Dynamic workflows for Claude Managed Agents

Released October 9, 2026 (beta). Review candidate only: independent Claude and OpenAI approval required before implementation.

What changed: A Managed Agents agent can create a multiphase workflow involving parallel agents, with observable progress and spending limits.

Why QN matters: Potential managed alternative to hand-built multi-agent processing for source comparison and article classification; overlaps with n8n queue/orchestration roadmap.

Expected benefit: Less development overhead and faster batch work.

Risks: Beta maturity, vendor dependence, parallel token cost and inconsistent editorial quality. This is not automatically a Claude Code feature; multiple Claude agents do not count as independent OpenAI oversight.

Impact: Architecture medium-high; security medium; cost uncertain; speed positive potential.

Proposed action: Compare alternatives, then consider a budget-limited, read-only staging experiment. Preserve independent Claude + OpenAI council verdict before changing any architecture.

Evidence: https://platform.claude.com/docs/en/release-notes/overview

# QN-TC-049 — Codex 0.161.0

Status: Candidate for separate Claude and OpenAI review. No implementation approved.

What changed: OpenAI released Codex 0.161.0 on October 7, 2026. Its model catalog defaults and session-management behavior changed.

Why it matters for QN: The OpenAI code-review process should be reproducible and explicitly versioned.

Expected benefit: More consistent review sessions.

Risk: Unplanned model or settings changes.

Impact: Architecture low, security medium, cost variable, speed medium.

Proposed action: Compare staging review quality and consistency before considering an upgrade. Require independent council confirmation.

Evidence: https://github.com/openai/codex/releases/tag/rust-v0.161.0

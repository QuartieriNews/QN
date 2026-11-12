# QN-TC-042 — n8n Agent approval isolation

Status: Candidate; review required by Claude and OpenAI, no implementation approved.

What changed: A September 30, 2026 n8n advisory described an Agent conversation and approval-access issue for users of a shared project. The vendor fixed it in 2.41.4 and later.

Why QN: Human approval in future Agent workflows depends on correctly isolating conversations and users.

Benefit: More trustworthy approval workflows.

Risks: This control is only one part of a larger authorization design; n8n Cloud version should be confirmed.

Impact: Security high; architecture low; cost neutral; speed low.

Proposed action: Verify the current n8n Cloud release and perform an isolated two-user staging approval test. Do not use new production approvals until both council reviewers confirm.

Evidence: https://github.com/advisories/GHSA-p3pg-xw4f-m72c

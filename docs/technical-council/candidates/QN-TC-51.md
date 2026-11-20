# QN-TC-051 — Browser and computer use SDK toolsets

**Status:** CANDIDATE / DEFER pending technical comparison; independent Claude + OpenAI review needed.

**What changed (2026-10-07):** Anthropic Python and TypeScript SDKs now have beta browser/computer toolset classes. Applications provide their own browser or desktop actions; the SDK operates the tool loop and supports configured URL/file policies and approval callbacks.

**Why QN:** Could simplify an isolated browser test runner for n8n UI and source validation, but overlaps functionality under consideration from n8n and OpenAI Agents API.

**Expected benefit:** Less custom orchestration code and clearer callback-based controls.

**Risks:** A click can create a real external change, and an approval callback cannot infer the effect from tool arguments alone. URL checks alone are insufficient for redirects. Isolated browser, limited network access, no live credentials and explicit approvals remain necessary.

**Impact:** architecture medium; security medium-high; cost unknown; speed medium potential.

**Proposed action:** Compare against n8n 2.42/2.43 and OpenAI Agents API before building anything. If needed, test a throwaway read-only browser worker without production accounts. No adoption without independent Claude + OpenAI decision.

**Evidence:** https://platform.claude.com/docs/en/release-notes/overview and https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk

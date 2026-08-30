# DEC-004 — Production value for max_events_per_run

Status: OPEN
Blocks: schedule activation (not development)

Question: `max_events_per_run: 50` is a test limit. Set the production value before
the schedule is activated.

Guidance: the weekly collection covers roughly a month ahead; the August sample was
107 URLs. The cap must exceed a normal collection with margin. The run report carries
`cap_reached` — if it fires, the run truncated silently.

Claude recommendation: 300 for the first scheduled weeks, revisit on run-report data.

Decided by: — · Date: — · Affected: workflow configuration (Phase 1.1).

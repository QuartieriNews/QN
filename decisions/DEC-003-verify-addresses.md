# DEC-003 — Five golden-set addresses marked confidence: verify

Status: OPEN
Blocks: scoring of the geographic golden set

Question: five items in `tests/golden_set_geographic.json` carry
`confidence: verify` — their expected zone was marked from imperfect knowledge.
Confirm or correct each before the set is used as ground truth.

Action, not options: the owner (or anyone with local knowledge) checks the five
addresses and edits the expected values. A golden set scored against unverified
expectations measures nothing.

Impact: 5 of 40 items (12.5% of the geographic ground truth).

Decided by: — · Date: — · Affected: golden_set_geographic.json.

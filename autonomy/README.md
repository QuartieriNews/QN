# autonomy/

`lane_gate.js` — the lane advisor. One file, two layers: a pure `classify` over a facts
object, and a git layer that produces that object. It has no credentials, performs no
merge, and does not read what any agent claims about the change it is classifying.

    node autonomy/lane_gate.js --base <sha> --head <sha> [--fork] [--escalated]

Writes the facts as JSON to stdout, and a table to `$GITHUB_STEP_SUMMARY` when set.
Exit status is 0 whenever the classification succeeded, whatever the lane: the lane is
advice to the owner, not a verdict on the pull request. A failure to classify is RED
with `UNCLASSIFIABLE`, not an error code.

The rules and their limits are in `docs/autonomy/LANE_POLICY.md`; the decision is
DEC-012. Tests: `node tests/test_lane_gate.js`.

In CI the classifier is taken from the base branch, never from the pull request, so a
change to the gate is not classified by itself.

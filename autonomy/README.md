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

In CI the classifier is taken from the pull request's exact base commit, not from the
pull request and not from the branch tip, so a change to the gate is not classified by
itself and the same pull request classifies the same way twice.

The one exception is the bootstrap: the pull request that first introduces the gate has
no gate at its base commit, so it classifies itself. The step says which copy it used, so
that case is visible rather than assumed. Once that pull request has merged, a fallback
in normal operation means the base commit is not the one that was expected.

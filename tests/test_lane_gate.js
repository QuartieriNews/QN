'use strict';

/**
 * Executable acceptance for the deterministic lane gate.
 *
 * Offline and dependency-free, like every suite in this folder: the gate is a pure
 * function, so no call is made and no key is needed. Cases marked T-#N are the
 * acceptance criteria enumerated in Issue #7; the rest are the adversarial cases the
 * Strategic Council identified as the ways a path rule is defeated without being
 * violated (LANE_POLICY §6, §7, §9).
 *
 * No test performs a real auto-merge; the gate cannot, having no I/O.
 */

const { classify, classifyUnderPolicy, resolveSymlinkTarget, PROTECTED_SURFACES,
        LANE, READY, POLICY_VERSION } = require('../autonomy/lane_gate.js');

let checks = 0;
let failed = 0;

function ok(name, condition) {
  checks += 1;
  if (condition) {
    console.log(`  ok   ${name}`);
  } else {
    failed += 1;
    console.log(`  FAIL ${name}`);
  }
}

const HEAD = 'a'.repeat(40);
const BASE = 'b'.repeat(40);
const OTHER = 'c'.repeat(40);

/** A snapshot with every condition satisfied, so each test can spoil exactly one. */
function goodSnapshot(overrides = {}) {
  const snap = Object.assign({
    policyVersion: POLICY_VERSION,
    headSha: HEAD,
    baseSha: BASE,
    baseRef: 'main',
    defaultBranch: 'main',
    isFork: false,
    authorIsAutomationIdentity: true,
    topLevelInventory: { baseSha: BASE, paths: ['docs', 'tests', 'autonomy', 'council'] },
    reviewCycles: 1,
    files: [{ status: 'modified', path: 'docs/notes/example.md', additions: 3, deletions: 1 }],
    filesComplete: true,
    filesTruncated: false,
    secretsDetected: false,
    evaluatorConsumesPullRequestCode: false,
    mandateSource: 'default_branch',
    ownerDecisionRequired: false,
    authorization: { taskId: 'issue-7', ownerAuthorised: true, mutableByThisPullRequest: false },
    requiredChecks: ['suites'],
    checkRuns: [{ name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true,
                  completedAt: '2026-09-01T16:00:00Z' }],
    review: {
      cleanForHead: true,
      reviewedSha: HEAD,
      laterThanLatestRequest: true,
      blockingFindingsOnHead: 0,
    },
    mergeable: true,
    baseIsCurrent: true,
    mergeAtomicity: 'strict_base',
    killSwitch: { readable: true, autoMergeDisabled: false },
    categoryValidation: { validator: 'docs-notes-v1', headSha: HEAD, passed: true },
    declaration: { lane: LANE.GREEN, headSha: HEAD, reason: 'inside the docs-notes category' },
    escalations: [],
  }, overrides);
  snap.files = stated(snap.files);
  return snap;
}

/**
 * File kinds are required evidence (LANE_POLICY §7), so the baseline states them all.
 * A test that wants an unstated kind deletes it explicitly, which is the only way the
 * omission is ever exercised.
 */
function stated(files) {
  return (files || []).map((f) => Object.assign(
    { isSymlink: false, isSubmodule: false, isBinary: false, modeChanged: false,
      isDependencyManifest: false, unreadable: false, additions: 1, deletions: 0 }, f));
}

/** A policy with one approved category, used only to prove GREEN is reachable at all. */
const POLICY_WITH_CATEGORY = {
  greenAllowlist: [
    { name: 'docs-notes', validator: 'docs-notes-v1', paths: ['docs/notes/'],
      limits: { maxFiles: 5, maxAdditions: 50 } },
  ],
};

// ---------------------------------------------------------------- shipped safe state

{
  // The shipped entry point takes no policy: a caller that could supply an allowlist
  // could grant itself GREEN, which is the promotion DEC-010 forbids.
  const r = classify(goodSnapshot());
  ok('T-1 shipped policy: an otherwise perfect PR is AMBER, never GREEN', r.lane === LANE.AMBER);
  ok('T-1 shipped policy: auto-merge withheld', r.autoMergeAllowed === false);
  ok('T-1 shipped policy stamps its source', r.policySource === 'shipped');
}

// ---------------------------------------------------------------------------- GREEN

{
  const r = classifyUnderPolicy(goodSnapshot(), POLICY_WITH_CATEGORY);
  ok('T-1 GREEN when every signal is present and bound to the same head', r.lane === LANE.GREEN);
  ok('T-1 GREEN with all conditions met would permit auto-merge', r.wouldAutoMergeUnderPolicy === true);
  ok('T-1 a fixture policy never authorises a real merge', r.autoMergeAllowed === false);
  ok('T-1 GREEN is READY', r.readiness === READY);
}

// -------------------------------------------------------- T-2 stale / absent review

{
  const r = classifyUnderPolicy(goodSnapshot({ review: { cleanForHead: true, reviewedSha: OTHER, laterThanLatestRequest: true, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 review of a different SHA blocks', r.readiness.includes('BLOCKED_STALE_REVIEW'));
  ok('T-2 stale review withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ review: { cleanForHead: false, reviewedSha: HEAD, laterThanLatestRequest: true, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 absence of a clean review is never clean', r.readiness.includes('BLOCKED_REVIEW'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ review: { cleanForHead: true, reviewedSha: HEAD, laterThanLatestRequest: false, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 clean review older than the latest review request blocks', r.readiness.includes('BLOCKED_REVIEW'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ review: { cleanForHead: true, reviewedSha: HEAD, laterThanLatestRequest: true, blockingFindingsOnHead: 2 } }), POLICY_WITH_CATEGORY);
  ok('T-2 findings on the current head block', r.readiness.includes('BLOCKED_REVIEW'));
}

// ------------------------------------------------------------------- T-3 test state

{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [{ name: 'suites', headSha: HEAD, conclusion: 'failure', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' }] }), POLICY_WITH_CATEGORY);
  ok('T-3 failing required check blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [] }), POLICY_WITH_CATEGORY);
  ok('T-3 missing required check blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ requiredChecks: [] }), POLICY_WITH_CATEGORY);
  ok('T-3 empty required-check set does not pass vacuously', r.readiness.includes('BLOCKED_TESTS'));
  ok('T-3 empty required-check set withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [{ name: 'suites', headSha: OTHER, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' }] }), POLICY_WITH_CATEGORY);
  ok('T-3 a check that passed on another commit is not evidence for this head', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [{ name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: false, completedAt: '2026-09-01T16:00:00Z' }] }), POLICY_WITH_CATEGORY);
  ok('T-3 a check from an untrusted producer is not evidence', r.readiness.includes('BLOCKED_TESTS'));
}

// ------------------------------------- several check runs sharing one name on one head

// GitHub emits a check run per triggering event and per re-run, so one name can carry
// several runs on a single commit. Selecting one arbitrarily is how a run that executed
// nothing becomes evidence that the suite passed.
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'skipped', trustedProducer: true, completedAt: '2026-09-01T15:58:39Z' },
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:58:40Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a skipped duplicate does not defeat a later success', r.readiness === READY);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:58:39Z' },
    { name: 'suites', headSha: HEAD, conclusion: 'skipped', trustedProducer: true, completedAt: '2026-09-01T15:58:40Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a skipped run that is the latest is not a pass', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'failure', trustedProducer: true, completedAt: '2026-09-01T15:00:00Z' },
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:30:00Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a re-run that succeeded after failing is a pass', r.readiness === READY);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' },
    { name: 'suites', headSha: HEAD, conclusion: 'skipped', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('duplicate runs without timestamps are ambiguous and block', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const at = '2026-09-01T15:58:40Z';
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
    { name: 'suites', headSha: HEAD, conclusion: 'failure', trustedProducer: true, completedAt: at },
  ] }), POLICY_WITH_CATEGORY);
  ok('a tie between runs that disagree blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const at = '2026-09-01T15:58:40Z';
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
  ] }), POLICY_WITH_CATEGORY);
  ok('a tie between runs that agree is not ambiguous', r.readiness === READY);
}

// --------------------------------------------------------- T-4 protected surfaces

for (const path of ['AGENTS.md', 'decisions/DEC-001-x.md', 'prompts/EDITORIAL_FILTER.md',
                    'gazetteer/gazetteer.json', '.github/workflows/ci.yml', 'requirements.txt',
                    'council/cli.js', 'venue-registry/venues.json', '.gitignore',
                    'docs/autonomy/LANE_POLICY.md', 'autonomy/lane_gate.js']) {
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path, additions: 1, deletions: 0 }],
    mandateSource: 'default_branch',
  }), POLICY_WITH_CATEGORY);
  ok(`T-4 protected surface is RED: ${path}`, r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-4 / T-8 RED never auto-merges', r.autoMergeAllowed === false);
}
{
  // Renaming a protected file out of its surface must not launder it.
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'renamed', path: 'docs/notes/agents.md', previousPath: 'AGENTS.md', additions: 0, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('rename out of a protected surface is still RED', r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'Decisions/DEC-001-x.md', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('case-only path difference does not escape a protected surface', r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'added', path: 'docs/notes/link.md', symlinkTarget: '../../prompts/EDITORIAL_FILTER.md', isSymlink: true, additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a symlink pointing into a protected surface is RED', r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'added', path: 'newthing/file.md', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a new top-level path fails closed to RED', r.lane === LANE.RED);
}

// ------------------------------------------------- T-5 owner decision cannot be GREEN

{
  const r = classifyUnderPolicy(goodSnapshot({ ownerDecisionRequired: true }), POLICY_WITH_CATEGORY);
  ok('T-5 an open OWNER_DECISION_REQUIRED is RED', r.lane === LANE.RED);
  ok('T-5 an open OWNER_DECISION_REQUIRED never auto-merges', r.autoMergeAllowed === false);
}

// ------------------------------------------- T-6 unknown or missing data fails closed

{
  const r = classifyUnderPolicy(goodSnapshot({ filesComplete: false }), POLICY_WITH_CATEGORY);
  ok('T-6 an incomplete file set is UNCLASSIFIED, not AMBER', r.lane === LANE.UNCLASSIFIED);
  ok('T-6 UNCLASSIFIED never auto-merges', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ headSha: 'a1b2c3d4e5' }), POLICY_WITH_CATEGORY);
  ok('T-6 an abbreviated head SHA is not evidence', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ policyVersion: '0' }), POLICY_WITH_CATEGORY);
  ok('T-6 evidence under another policy version is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ files: [{ status: 'modified', path: 'docs/notes/a.md', unreadable: true }] }), POLICY_WITH_CATEGORY);
  ok('T-6 an unreadable file is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ filesTruncated: true }), POLICY_WITH_CATEGORY);
  ok('a truncated list reported as complete is PROHIBITED', r.lane === LANE.PROHIBITED);
}

// ------------------------------------------------------------- T-7 AMBER never merges

{
  const r = classifyUnderPolicy(goodSnapshot({ files: [{ status: 'modified', path: 'docs/other/x.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-7 outside every category the lane is AMBER', r.lane === LANE.AMBER);
  ok('T-7 AMBER never auto-merges', r.autoMergeAllowed === false);
}

// ------------------------------ T-9 the builder cannot self-approve around the gate

{
  const r = classifyUnderPolicy(goodSnapshot({ declaration: { lane: LANE.GREEN, headSha: HEAD, reason: 'declared' },
    files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-9 declaring GREEN over a protected change does not produce GREEN', r.lane === LANE.RED);
  ok('T-9 a declaration disagreeing with the computed lane is recorded', r.declarationMismatch === true);
  ok('T-9 a mismatched declaration withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ declaration: undefined }), POLICY_WITH_CATEGORY);
  ok('T-9 a missing declaration is not agreement', r.wouldAutoMergeUnderPolicy === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ declaration: { lane: LANE.GREEN, headSha: OTHER, reason: 'declared' } }), POLICY_WITH_CATEGORY);
  ok('T-9 a declaration bound to another head does not count', r.wouldAutoMergeUnderPolicy === false);
}

// ------------------------------------------- T-10 the evaluator never runs PR code

{
  const r = classifyUnderPolicy(goodSnapshot({ evaluatorConsumesPullRequestCode: true }), POLICY_WITH_CATEGORY);
  ok('T-10 consuming pull-request-controlled code is PROHIBITED', r.lane === LANE.PROHIBITED);
  ok('T-10 PROHIBITED never auto-merges', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }],
    mandateSource: 'pull_request',
  }), POLICY_WITH_CATEGORY);
  ok('a PR rewriting its own mandate under its own version is PROHIBITED', r.lane === LANE.PROHIBITED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ secretsDetected: true }), POLICY_WITH_CATEGORY);
  ok('a credential in the diff is PROHIBITED, not owner-approvable', r.lane === LANE.PROHIBITED);
}

// ------------------------------------------------------- merge atomicity and switch

{
  const r = classifyUnderPolicy(goodSnapshot({ mergeAtomicity: 'none' }), POLICY_WITH_CATEGORY);
  ok('without atomic merge enforcement GREEN withholds auto-merge',
     r.lane === LANE.GREEN && r.wouldAutoMergeUnderPolicy === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ mergeAtomicity: 'merge_queue' }), POLICY_WITH_CATEGORY);
  ok('a merge queue satisfies atomicity', r.wouldAutoMergeUnderPolicy === true);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ killSwitch: { readable: false, autoMergeDisabled: false } }), POLICY_WITH_CATEGORY);
  ok('an unreadable kill switch fails closed', r.wouldAutoMergeUnderPolicy === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ killSwitch: { readable: true, autoMergeDisabled: true } }), POLICY_WITH_CATEGORY);
  ok('the kill switch stops auto-merge without changing the lane',
     r.lane === LANE.GREEN && r.wouldAutoMergeUnderPolicy === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ baseIsCurrent: false }), POLICY_WITH_CATEGORY);
  ok('a base that has moved blocks readiness, not the lane', r.lane === LANE.GREEN && r.readiness.includes('BLOCKED_STALE_BASE'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ mergeable: false }), POLICY_WITH_CATEGORY);
  ok('a merge conflict blocks readiness, not the lane', r.lane === LANE.GREEN && r.readiness.includes('BLOCKED_MERGE_CONFLICT'));
}

// ------------------------------------------------------- category composition rules

{
  const twoCategories = { greenAllowlist: [
    { name: 'docs-notes', validator: 'docs-notes-v1', paths: ['docs/notes/'], limits: {} },
    { name: 'tests', validator: 'docs-notes-v1', paths: ['tests/'], limits: {} },
  ] };
  const r = classifyUnderPolicy(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', additions: 1, deletions: 0 },
    { status: 'modified', path: 'tests/t.js', additions: 1, deletions: 0 },
  ] }), twoCategories);
  ok('two approved categories in one PR are not an approved category', r.lane === LANE.AMBER);
}
for (const [label, files] of [
  ['additions', [{ status: 'modified', path: 'docs/notes/a.md', additions: 999, deletions: 0 }]],
  ['file count', Array.from({ length: 6 }, (_, i) =>
    ({ status: 'modified', path: `docs/notes/f${i}.md`, additions: 1, deletions: 0 }))],
]) {
  const under = classifyUnderPolicy(goodSnapshot({ files }), POLICY_WITH_CATEGORY);
  ok(`exceeding the ${label} limit is AMBER`, under.lane === LANE.AMBER);
}
{
  // The boundary itself, so the limit is proven to be enforced rather than present.
  const at = classifyUnderPolicy(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', additions: 50, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('a change exactly at the addition limit is still GREEN', at.lane === LANE.GREEN);
}
for (const kind of ['isSubmodule', 'isBinary', 'modeChanged']) {
  const file = { status: 'modified', path: 'docs/notes/a.md', additions: 1, deletions: 0 };
  file[kind] = true;
  const r = classifyUnderPolicy(goodSnapshot({ files: [file] }), POLICY_WITH_CATEGORY);
  ok(`a file that is ${kind} fails closed out of GREEN`, r.lane === LANE.AMBER);
}
{
  // A symlink with a target that resolves inside the category is still not GREEN: the
  // kind fails closed on its own, independently of where it points.
  const r = classifyUnderPolicy(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', isSymlink: true,
      symlinkTarget: 'b.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('a symlink pointing inside its own category is still not GREEN', r.lane === LANE.AMBER);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', isSymlink: true, additions: 1, deletions: 0 }] }),
    POLICY_WITH_CATEGORY);
  ok('a symlink with no stated target is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  // Refused outright since DEC-011; before that it was merely never GREEN.
  const r = classifyUnderPolicy(goodSnapshot({ isFork: true }), POLICY_WITH_CATEGORY);
  ok('a fork pull request is never GREEN', r.lane !== LANE.GREEN);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ authorIsAutomationIdentity: false }), POLICY_WITH_CATEGORY);
  ok('an author that is not the automation identity is never GREEN', r.lane === LANE.AMBER);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ authorization: { taskId: 'x', mutableByThisPullRequest: true } }), POLICY_WITH_CATEGORY);
  ok('an authorisation this PR could alter is not authorisation', r.lane === LANE.AMBER);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ baseRef: 'release' }), POLICY_WITH_CATEGORY);
  ok('a PR not targeting the default branch is never GREEN', r.lane === LANE.AMBER);
}

// ------------------------------------------ cycle 1: evidence must be stated, not absent

// Every one of these was a field whose *absence* previously read as though it had been
// checked. `x === true` used to reject lets an omitted field through; the policy sends
// unstated evidence to UNCLASSIFIED instead (LANE_POLICY §5).
for (const [field, value] of [['secretsDetected', undefined], ['filesTruncated', undefined],
                              ['evaluatorConsumesPullRequestCode', undefined],
                              ['isFork', undefined], ['isFork', 'no']]) {
  const snap = goodSnapshot();
  if (value === undefined) delete snap[field]; else snap[field] = value;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok(`unstated ${field} is UNCLASSIFIED, not a pass`, r.lane === LANE.UNCLASSIFIED);
}
{
  const snap = goodSnapshot();
  delete snap.ownerDecisionRequired;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok('an unreported owner-decision condition is RED', r.lane === LANE.RED);
}

// ------------------------------------------------- cycle 1: the changed-file set itself

{
  const r = classifyUnderPolicy(goodSnapshot({ files: [{ status: 'modified' }] }), POLICY_WITH_CATEGORY);
  ok('a changed file with no repository path is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ files: [] }), POLICY_WITH_CATEGORY);
  ok('an empty changed-file set is UNCLASSIFIED, never vacuously GREEN', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'renamed', path: 'docs/notes/b.md', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a rename stating no previous path is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}

// ------------------------------------------------------ cycle 1: symlinks are relative

ok('a relative symlink target resolves against the link directory',
   resolveSymlinkTarget('docs/notes/link.md', '../../prompts/EDITORIAL_FILTER.md') === 'prompts/editorial_filter.md');
ok('a same-directory target resolves beside the link',
   resolveSymlinkTarget('docs/notes/link.md', 'other.md') === 'docs/notes/other.md');
ok('a target escaping the repository root does not resolve',
   resolveSymlinkTarget('docs/link.md', '../../../etc/passwd') === null);
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'added', path: 'docs/notes/link.md', symlinkTarget: '../../../outside', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('an unresolvable symlink target is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}

// -------------------------------------- cycle 1: the gate's own attestations are RED

for (const path of ['tests/test_lane_gate.js', 'tests/test_workflow_safety.js']) {
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path, additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok(`a change to the gate's own suite is RED: ${path}`, r.lane === LANE.RED);
}

// -------------------------------- cycle 1: a manifest is a manifest wherever it sits

for (const path of ['docs/package.json', 'tools/package-lock.json', 'sub/dir/go.sum',
                    'nested/Cargo.toml', 'a/b/yarn.lock']) {
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path, additions: 1, deletions: 0 }],
    topLevelInventory: { baseSha: BASE, paths: ['docs', 'tests', 'autonomy', 'council', 'tools', 'sub', 'nested', 'a'] },
  }), POLICY_WITH_CATEGORY);
  ok(`a dependency manifest outside the root is RED: ${path}`, r.lane === LANE.RED);
}

// ---------------------------------------- cycle 1: authorisation must be positive

for (const [label, authorization] of [
  ['an empty object', {}],
  ['no owner signal', { taskId: 'x', mutableByThisPullRequest: false }],
  ['no immutability statement', { taskId: 'x', ownerAuthorised: true }],
  ['a blank task id', { taskId: '  ', ownerAuthorised: true, mutableByThisPullRequest: false }],
]) {
  const r = classifyUnderPolicy(goodSnapshot({ authorization }), POLICY_WITH_CATEGORY);
  ok(`authorisation with ${label} is not authorisation`, r.lane === LANE.AMBER);
}

// ------------------------------------------ cycle 1: every escalation is honoured

{
  const r = classifyUnderPolicy(goodSnapshot({
    escalations: [{ toLane: LANE.AMBER, by: 'codex', reason: 'behaviour change' }],
  }), POLICY_WITH_CATEGORY);
  ok('an escalation to AMBER suppresses a computed GREEN', r.lane === LANE.AMBER);
  ok('an escalation to AMBER withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    escalations: [{ toLane: LANE.RED, by: 'claude', reason: 'touches governance' }],
  }), POLICY_WITH_CATEGORY);
  ok('an escalation to RED produces RED', r.lane === LANE.RED);
}

// ------------------------------------ cycle 1: the blocking-findings signal must exist

for (const [label, blockingFindingsOnHead] of [
  ['omitted', undefined], ['negative', -1], ['non-numeric', 'none'], ['fractional', 1.5],
]) {
  const review = { cleanForHead: true, reviewedSha: HEAD, laterThanLatestRequest: true };
  if (blockingFindingsOnHead !== undefined) review.blockingFindingsOnHead = blockingFindingsOnHead;
  const r = classifyUnderPolicy(goodSnapshot({ review }), POLICY_WITH_CATEGORY);
  ok(`a ${label} blocking-findings count blocks`, r.readiness.includes('BLOCKED_REVIEW'));
}

// ------------------------------------------- cycle 1: a declaration carries its reason

for (const [label, declaration] of [
  ['no reason', { lane: LANE.GREEN, headSha: HEAD }],
  ['a blank reason', { lane: LANE.GREEN, headSha: HEAD, reason: '   ' }],
  ['a non-string reason', { lane: LANE.GREEN, headSha: HEAD, reason: 42 }],
]) {
  const r = classifyUnderPolicy(goodSnapshot({ declaration }), POLICY_WITH_CATEGORY);
  ok(`a declaration with ${label} does not agree`, r.wouldAutoMergeUnderPolicy === false);
}

// ------------------------------- cycle 1: a caller cannot substitute its own allowlist

{
  const r = classifyUnderPolicy(goodSnapshot(), POLICY_WITH_CATEGORY);
  ok('a result reached under an injected policy says so', r.policySource === 'injected');
}
{
  // The same snapshot that is GREEN under a fixture is AMBER under what ships.
  ok('the shipped entry point cannot be handed an allowlist', classify.length === 1);
  const r = classify(goodSnapshot());
  ok('the shipped policy yields no GREEN for a snapshot a fixture makes GREEN',
     r.lane === LANE.AMBER && r.autoMergeAllowed === false);
}
{
  let threw = false;
  try { classifyUnderPolicy(goodSnapshot(), {}); } catch (e) { threw = /greenAllowlist/.test(e.message); }
  ok('the fixture seam refuses a policy with no allowlist', threw);
}

// ------------------------------- cycle 2: the remaining unstated-evidence gaps

for (const kind of ['isSymlink', 'isSubmodule', 'isBinary', 'modeChanged']) {
  const snap = goodSnapshot();
  delete snap.files[0][kind];
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok(`an unstated ${kind} is UNCLASSIFIED, not falsy-and-fine`, r.lane === LANE.UNCLASSIFIED);
}
{
  const snap = goodSnapshot();
  delete snap.escalations;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok('an unstated escalation list is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ escalations: [{ toLane: 'AMBER' }] }), POLICY_WITH_CATEGORY);
  ok('a malformed escalation record is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}

// ----------------------------------------- cycle 2: an absolute symlink target is external

ok('an absolute symlink target does not resolve',
   resolveSymlinkTarget('docs/notes/link.md', '/etc/passwd') === null);
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'added', path: 'docs/notes/link.md', symlinkTarget: '/etc/passwd',
              additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a change carrying an absolute symlink target is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}

// ------------------------------------- cycle 2: manifests the name list had missed

for (const path of ['docs/composer.json', 'docs/composer.lock', 'a/uv.lock',
                    'b/gradle.lockfile', 'c/something.lock', 'd/pnpm-lock.yaml']) {
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path, additions: 1, deletions: 0 }],
    topLevelInventory: { baseSha: BASE, paths: ['docs', 'a', 'b', 'c', 'd'] },
  }), POLICY_WITH_CATEGORY);
  ok(`a dependency manifest or lockfile is RED: ${path}`, r.lane === LANE.RED);
}

// -------------------------------- cycle 2: a rename introduces its destination

{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'renamed', path: 'newthing/x.md', previousPath: 'docs/notes/x.md',
              additions: 0, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a rename into a new top-level path is RED', r.lane === LANE.RED);
}

// --------------------------- cycle 2: readiness binds to the policy's own manifest

{
  const r = classifyUnderPolicy(goodSnapshot({
    requiredChecks: ['unrelated-lint'],
    checkRuns: [{ name: 'unrelated-lint', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' }],
  }), POLICY_WITH_CATEGORY);
  ok('a ruleset naming only an unrelated check does not satisfy the manifest',
     r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ requiredChecks: [] }), POLICY_WITH_CATEGORY);
  ok('a ruleset requiring nothing blocks on the manifest', r.readiness.includes('BLOCKED_TESTS:manifest'));
}

// ------------------------------------------- cycle 2: the kill switch cannot crash

for (const [label, killSwitch] of [['null', null], ['a string', 'off'], ['omitted', undefined]]) {
  const snap = goodSnapshot();
  if (killSwitch === undefined) delete snap.killSwitch; else snap.killSwitch = killSwitch;
  let threw = false;
  let r = null;
  try { r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY); } catch (e) { threw = true; }
  ok(`a kill switch that is ${label} fails closed without throwing`,
     !threw && r.wouldAutoMergeUnderPolicy === false);
}

// ------------------------- cycle 2: an injected policy authorises nothing, ever

{
  const r = classifyUnderPolicy(goodSnapshot(), POLICY_WITH_CATEGORY);
  ok('an injected policy never sets the authorising field', r.autoMergeAllowed === false);
  ok('an injected policy reports its replay outcome separately',
     r.wouldAutoMergeUnderPolicy === true);
}
{
  const r = classify(goodSnapshot());
  ok('a shipped result carries no replay field to confuse a consumer',
     r.wouldAutoMergeUnderPolicy === undefined);
}

// ------------------------------------ cycle 3: evidence the earlier passes had missed

{
  const r = classifyUnderPolicy(goodSnapshot({
    escalations: [{ toLane: 'PURPLE', by: 'agent', reason: 'uncertain' }],
  }), POLICY_WITH_CATEGORY);
  ok('an escalation naming an unsupported lane is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
for (const [label, patch] of [
  ['omitted additions', { additions: undefined }],
  ['negative additions', { additions: -5 }],
  ['non-integer deletions', { deletions: 'lots' }],
  ['fractional additions', { additions: 2.5 }],
]) {
  const snap = goodSnapshot();
  Object.assign(snap.files[0], patch);
  if (patch.additions === undefined) delete snap.files[0].additions;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok(`${label} is UNCLASSIFIED, so no magnitude limit is satisfied by default`,
     r.lane === LANE.UNCLASSIFIED);
}
{
  const snap = goodSnapshot();
  delete snap.files[0].unreadable;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok('unstated readability is UNCLASSIFIED, not proof the file was read',
     r.lane === LANE.UNCLASSIFIED);
}
for (const [label, checkRuns] of [['an object', { a: 1 }], ['a scalar', 'ok'], ['omitted', undefined]]) {
  const snap = goodSnapshot();
  if (checkRuns === undefined) delete snap.checkRuns; else snap.checkRuns = checkRuns;
  let threw = false;
  let r = null;
  try { r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY); } catch (e) { threw = true; }
  ok(`a check-run collection that is ${label} fails closed without throwing`,
     !threw && r.lane === LANE.UNCLASSIFIED);
}

// ----------------------------- cycle 3: control files bind wherever they sit

for (const path of ['docs/AGENTS.md', 'docs/.gitignore', 'a/b/CLAUDE.md',
                    'sub/LANE_POLICY.md']) {
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path }],
    topLevelInventory: { baseSha: BASE, paths: ['docs', 'a', 'sub'] },
  }), POLICY_WITH_CATEGORY);
  ok(`a scoped control file is RED at any depth: ${path}`, r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'docs/AGENTS.md' }],
    mandateSource: 'pull_request',
  }), POLICY_WITH_CATEGORY);
  ok('a scoped mandate applied from the pull request is PROHIBITED', r.lane === LANE.PROHIBITED);
}

// --------------------- cycle 3: the replay seam cannot weaken the check manifest

{
  const r = classifyUnderPolicy(goodSnapshot({
    requiredChecks: ['unrelated'],
    checkRuns: [{ name: 'unrelated', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T16:00:00Z' }],
  }), { greenAllowlist: POLICY_WITH_CATEGORY.greenAllowlist, requiredChecks: ['unrelated'] });
  ok('a replay policy naming its own manifest does not become ready',
     r.readiness.includes('BLOCKED_TESTS'));
}

// ------------------------------ cycle 3: the exported tables are copies, and frozen

{
  const before = PROTECTED_SURFACES.length;
  let threw = false;
  try { PROTECTED_SURFACES.splice(0); } catch (e) { threw = true; }
  ok('the exported protected list refuses mutation', threw || PROTECTED_SURFACES.length === before);
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'autonomy/lane_gate.js' }],
  }), POLICY_WITH_CATEGORY);
  ok('a consumer cannot empty the classifier\'s own protected table', r.lane === LANE.RED);
}

// --------------------------- cycle 5: status, binding, cycles and the reinforced audit

for (const [label, patch] of [['omitted', {}], ['misspelled', { status: 'renmaed' }]]) {
  const snap = goodSnapshot();
  if (label === 'omitted') delete snap.files[0].status; else Object.assign(snap.files[0], patch);
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok(`a ${label} file status is UNCLASSIFIED`, r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', previousPath: 'docs/notes/b.md' }] }),
    POLICY_WITH_CATEGORY);
  ok('a previous path on a non-rename contradicts the status', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    topLevelInventory: { baseSha: OTHER, paths: ['docs'] },
  }), POLICY_WITH_CATEGORY);
  ok('an inventory not bound to the base commit is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ checkRuns: [
    { name: 'suites', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: 0 }] }),
    POLICY_WITH_CATEGORY);
  ok('a numeric completion time is not a timestamp', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    declaration: { lane: LANE.AMBER, headSha: HEAD, reason: 'thought it was amber' },
  }), POLICY_WITH_CATEGORY);
  ok('a declaration mismatch blocks readiness, not merely the permission',
     r.readiness.includes('BLOCKED_DECLARATION_MISMATCH'));
}
{
  const snap = goodSnapshot();
  delete snap.reviewCycles;
  const r = classifyUnderPolicy(snap, POLICY_WITH_CATEGORY);
  ok('an unstated review-cycle count blocks', r.readiness.includes('BLOCKED_CYCLES'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({ reviewCycles: 4 }), POLICY_WITH_CATEGORY);
  ok('reaching the cycle cap blocks automation', r.readiness.includes('BLOCKED_CYCLE_CAP'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    reviewCycles: 5,
    ownerCycleException: { headSha: HEAD, grantedByOwner: true,
                           source: 'pull_request_comment', commentId: 5497674423,
                           commentBody: `Authorising one further cycle for head ${HEAD}.` },
  }), POLICY_WITH_CATEGORY);
  ok('an owner exception bound to this head clears the cap', r.readiness === READY);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    reviewCycles: 5,
    ownerCycleException: { headSha: OTHER, grantedByOwner: true,
                           source: 'pull_request_comment', commentId: 1,
                           commentBody: `Authorising one further cycle for head ${OTHER}.` },
  }), POLICY_WITH_CATEGORY);
  ok('an exception bound to another head does not carry over',
     r.readiness.includes('BLOCKED_CYCLE_CAP'));
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md' }],
  }), POLICY_WITH_CATEGORY);
  ok('RED without the reinforced audit is not ready',
     r.lane === LANE.RED && r.readiness.includes('BLOCKED_REINFORCED_AUDIT'));
}
{
  const audit = { headSha: HEAD, baseSha: BASE, policyVersion: POLICY_VERSION,
                  mandateSource: 'default_branch', sealedBeforePublication: true,
                  freshContext: true, findings: 0 };
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md' }],
    declaration: { lane: LANE.RED, headSha: HEAD, reason: 'governance' },
    reinforcedAudit: { claude: audit, codex: audit },
  }), POLICY_WITH_CATEGORY);
  ok('RED with two fully bound sealed audits is ready', r.readiness === READY);
}
{
  const audit = { headSha: HEAD, baseSha: BASE, policyVersion: POLICY_VERSION,
                  mandateSource: 'default_branch', sealedBeforePublication: false,
                  freshContext: true, findings: 0 };
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md' }],
    declaration: { lane: LANE.RED, headSha: HEAD, reason: 'governance' },
    reinforcedAudit: { claude: audit, codex: audit },
  }), POLICY_WITH_CATEGORY);
  ok('an audit published before the other was collected is not separated',
     r.readiness.includes('BLOCKED_REINFORCED_AUDIT'));
}

// ------------------------------------------- DEC-011: forks, and how a cap is lifted

{
  const r = classifyUnderPolicy(goodSnapshot({ isFork: true }), POLICY_WITH_CATEGORY);
  ok('a fork pull request is RED, not merely non-GREEN', r.lane === LANE.RED);
  ok('a fork pull request never auto-merges', r.wouldAutoMergeUnderPolicy === false);
}
{
  // Unready by rule rather than by the accident of having no check run: the same head
  // can acquire a trusted check through another ref, and READY is the owner-merge state.
  const audit = { headSha: HEAD, baseSha: BASE, policyVersion: POLICY_VERSION,
                  mandateSource: 'default_branch', sealedBeforePublication: true,
                  freshContext: true, findings: 0 };
  const r = classifyUnderPolicy(goodSnapshot({
    isFork: true,
    declaration: { lane: LANE.RED, headSha: HEAD, reason: 'fork' },
    reinforcedAudit: { claude: audit, codex: audit },
  }), POLICY_WITH_CATEGORY);
  ok('a fork with otherwise complete evidence is still not ready',
     r.readiness.includes('BLOCKED_FORK_REFUSED'));
}
for (const [label, exception] of [
  ['granted only in chat', { headSha: HEAD, grantedByOwner: true }],
  ['from an unattributable source', { headSha: HEAD, grantedByOwner: true, source: 'label' }],
  ['naming no comment', { headSha: HEAD, grantedByOwner: true, source: 'pull_request_comment',
                          commentBody: `head ${HEAD}` }],
  ['whose comment names no SHA', { headSha: HEAD, grantedByOwner: true, commentId: 2,
                                   source: 'pull_request_comment',
                                   commentBody: 'please proceed with 2 more cycles' }],
  ['whose comment names another head', { headSha: HEAD, grantedByOwner: true, commentId: 3,
                                         source: 'pull_request_comment',
                                         commentBody: `authorised for ${OTHER}` }],
  ['not granted by the owner', { headSha: HEAD, grantedByOwner: false,
                                 source: 'pull_request_comment', commentId: 1 }],
]) {
  const r = classifyUnderPolicy(goodSnapshot({ reviewCycles: 5, ownerCycleException: exception }),
                                POLICY_WITH_CATEGORY);
  ok(`an exception ${label} does not lift the cap`, r.readiness.includes('BLOCKED_CYCLE_CAP'));
}

// ------------------------------- cycle 8: bindings a collector could have supplied

for (const [label, missing] of [['the base', 'baseSha'], ['the policy version', 'policyVersion'],
                                ['a fresh context', 'freshContext']]) {
  const audit = { headSha: HEAD, baseSha: BASE, policyVersion: POLICY_VERSION,
                  mandateSource: 'default_branch', sealedBeforePublication: true,
                  freshContext: true, findings: 0 };
  delete audit[missing];
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md' }],
    declaration: { lane: LANE.RED, headSha: HEAD, reason: 'governance' },
    reinforcedAudit: { claude: audit, codex: audit },
  }), POLICY_WITH_CATEGORY);
  ok(`an audit recording no ${label} is not the reinforced control`,
     r.readiness.includes('BLOCKED_REINFORCED_AUDIT'));
}
{
  // Case is folded for protected matching, where it is conservative, and preserved here,
  // where folding would let an existing `docs/` cover a newly added `Docs/`.
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'added', path: 'Docs/notes/example.md' }],
  }), POLICY_WITH_CATEGORY);
  ok('a case-variant top-level path is new, and therefore RED', r.lane === LANE.RED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({
    files: [{ status: 'renamed', path: 'Docs/x.md', previousPath: 'docs/notes/x.md' }],
  }), POLICY_WITH_CATEGORY);
  ok('a rename into a case-variant top level is RED too', r.lane === LANE.RED);
}

// ---------------------------------------------------------------- ordering and shape

{
  const r = classifyUnderPolicy(goodSnapshot({ secretsDetected: true, filesComplete: false,
    files: [{ status: 'modified', path: 'AGENTS.md' }] }), POLICY_WITH_CATEGORY);
  ok('PROHIBITED is evaluated before every other state', r.lane === LANE.PROHIBITED);
}
{
  const r = classifyUnderPolicy(goodSnapshot({ filesComplete: false,
    files: [{ status: 'modified', path: 'AGENTS.md' }] }), POLICY_WITH_CATEGORY);
  ok('UNCLASSIFIED is evaluated before RED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classify(goodSnapshot());
  ok('every result carries the policy version', r.policyVersion === POLICY_VERSION);
  ok('every result carries the full head SHA it judged', r.headSha === HEAD);
  ok('every result carries the base SHA', r.baseSha === BASE);
  ok('every result states its reasons', Array.isArray(r.reasons) && r.reasons.length > 0);
}
{
  let threw = false;
  try { classify(null); } catch (e) { threw = /snapshot is required/.test(e.message); }
  ok('a missing snapshot throws rather than classifying', threw);
}

console.log('');
if (failed > 0) {
  console.log(`FAILED (${failed} of ${checks} checks)`);
  process.exit(1);
}
console.log(`ALL PASS (${checks} checks)`);

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

const { classify, LANE, READY, POLICY_VERSION } = require('../autonomy/lane_gate.js');

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
  return Object.assign({
    policyVersion: POLICY_VERSION,
    headSha: HEAD,
    baseSha: BASE,
    baseRef: 'main',
    defaultBranch: 'main',
    isFork: false,
    authorIsAutomationIdentity: true,
    knownTopLevelPaths: ['docs', 'tests', 'autonomy', 'council'],
    files: [{ status: 'modified', path: 'docs/notes/example.md', additions: 3, deletions: 1 }],
    filesComplete: true,
    filesTruncated: false,
    secretsDetected: false,
    evaluatorConsumesPullRequestCode: false,
    mandateSource: 'default_branch',
    ownerDecisionRequired: false,
    authorization: { taskId: 'issue-7', mutableByThisPullRequest: false },
    requiredChecks: ['tests'],
    checkRuns: [{ name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true }],
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
    declaration: { lane: LANE.GREEN, headSha: HEAD },
    escalations: [],
  }, overrides);
}

/** A policy with one approved category, used only to prove GREEN is reachable at all. */
const POLICY_WITH_CATEGORY = {
  greenAllowlist: [
    { name: 'docs-notes', paths: ['docs/notes/'], limits: { maxFiles: 5, maxAdditions: 50 } },
  ],
};

// ---------------------------------------------------------------- shipped safe state

{
  const r = classify(goodSnapshot());
  ok('T-1 empty allowlist: an otherwise perfect PR is AMBER, never GREEN', r.lane === LANE.AMBER);
  ok('T-1 empty allowlist: auto-merge withheld', r.autoMergeAllowed === false);
}

// ---------------------------------------------------------------------------- GREEN

{
  const r = classify(goodSnapshot(), POLICY_WITH_CATEGORY);
  ok('T-1 GREEN when every signal is present and bound to the same head', r.lane === LANE.GREEN);
  ok('T-1 GREEN with all conditions met permits auto-merge', r.autoMergeAllowed === true);
  ok('T-1 GREEN is READY', r.readiness === READY);
}

// -------------------------------------------------------- T-2 stale / absent review

{
  const r = classify(goodSnapshot({ review: { cleanForHead: true, reviewedSha: OTHER, laterThanLatestRequest: true, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 review of a different SHA blocks', r.readiness.includes('BLOCKED_STALE_REVIEW'));
  ok('T-2 stale review withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ review: { cleanForHead: false, reviewedSha: HEAD, laterThanLatestRequest: true, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 absence of a clean review is never clean', r.readiness.includes('BLOCKED_REVIEW'));
}
{
  const r = classify(goodSnapshot({ review: { cleanForHead: true, reviewedSha: HEAD, laterThanLatestRequest: false, blockingFindingsOnHead: 0 } }), POLICY_WITH_CATEGORY);
  ok('T-2 clean review older than the latest review request blocks', r.readiness.includes('BLOCKED_REVIEW'));
}
{
  const r = classify(goodSnapshot({ review: { cleanForHead: true, reviewedSha: HEAD, laterThanLatestRequest: true, blockingFindingsOnHead: 2 } }), POLICY_WITH_CATEGORY);
  ok('T-2 findings on the current head block', r.readiness.includes('BLOCKED_REVIEW'));
}

// ------------------------------------------------------------------- T-3 test state

{
  const r = classify(goodSnapshot({ checkRuns: [{ name: 'tests', headSha: HEAD, conclusion: 'failure', trustedProducer: true }] }), POLICY_WITH_CATEGORY);
  ok('T-3 failing required check blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classify(goodSnapshot({ checkRuns: [] }), POLICY_WITH_CATEGORY);
  ok('T-3 missing required check blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classify(goodSnapshot({ requiredChecks: [] }), POLICY_WITH_CATEGORY);
  ok('T-3 empty required-check set does not pass vacuously', r.readiness.includes('BLOCKED_TESTS'));
  ok('T-3 empty required-check set withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ checkRuns: [{ name: 'tests', headSha: OTHER, conclusion: 'success', trustedProducer: true }] }), POLICY_WITH_CATEGORY);
  ok('T-3 a check that passed on another commit is not evidence for this head', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classify(goodSnapshot({ checkRuns: [{ name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: false }] }), POLICY_WITH_CATEGORY);
  ok('T-3 a check from an untrusted producer is not evidence', r.readiness.includes('BLOCKED_TESTS'));
}

// ------------------------------------- several check runs sharing one name on one head

// GitHub emits a check run per triggering event and per re-run, so one name can carry
// several runs on a single commit. Selecting one arbitrarily is how a run that executed
// nothing becomes evidence that the suite passed.
{
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'skipped', trustedProducer: true, completedAt: '2026-09-01T15:58:39Z' },
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:58:40Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a skipped duplicate does not defeat a later success', r.readiness === READY);
}
{
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:58:39Z' },
    { name: 'tests', headSha: HEAD, conclusion: 'skipped', trustedProducer: true, completedAt: '2026-09-01T15:58:40Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a skipped run that is the latest is not a pass', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'failure', trustedProducer: true, completedAt: '2026-09-01T15:00:00Z' },
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: '2026-09-01T15:30:00Z' },
  ] }), POLICY_WITH_CATEGORY);
  ok('a re-run that succeeded after failing is a pass', r.readiness === READY);
}
{
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true },
    { name: 'tests', headSha: HEAD, conclusion: 'skipped', trustedProducer: true },
  ] }), POLICY_WITH_CATEGORY);
  ok('duplicate runs without timestamps are ambiguous and block', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const at = '2026-09-01T15:58:40Z';
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
    { name: 'tests', headSha: HEAD, conclusion: 'failure', trustedProducer: true, completedAt: at },
  ] }), POLICY_WITH_CATEGORY);
  ok('a tie between runs that disagree blocks', r.readiness.includes('BLOCKED_TESTS'));
}
{
  const at = '2026-09-01T15:58:40Z';
  const r = classify(goodSnapshot({ checkRuns: [
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
    { name: 'tests', headSha: HEAD, conclusion: 'success', trustedProducer: true, completedAt: at },
  ] }), POLICY_WITH_CATEGORY);
  ok('a tie between runs that agree is not ambiguous', r.readiness === READY);
}

// --------------------------------------------------------- T-4 protected surfaces

for (const path of ['AGENTS.md', 'decisions/DEC-001-x.md', 'prompts/EDITORIAL_FILTER.md',
                    'gazetteer/gazetteer.json', '.github/workflows/ci.yml', 'requirements.txt',
                    'council/cli.js', 'venue-registry/venues.json', '.gitignore',
                    'docs/autonomy/LANE_POLICY.md', 'autonomy/lane_gate.js']) {
  const r = classify(goodSnapshot({
    files: [{ status: 'modified', path, additions: 1, deletions: 0 }],
    mandateSource: 'default_branch',
  }), POLICY_WITH_CATEGORY);
  ok(`T-4 protected surface is RED: ${path}`, r.lane === LANE.RED);
}
{
  const r = classify(goodSnapshot({ files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-4 / T-8 RED never auto-merges', r.autoMergeAllowed === false);
}
{
  // Renaming a protected file out of its surface must not launder it.
  const r = classify(goodSnapshot({
    files: [{ status: 'renamed', path: 'docs/notes/agents.md', previousPath: 'AGENTS.md', additions: 0, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('rename out of a protected surface is still RED', r.lane === LANE.RED);
}
{
  const r = classify(goodSnapshot({
    files: [{ status: 'modified', path: 'Decisions/DEC-001-x.md', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('case-only path difference does not escape a protected surface', r.lane === LANE.RED);
}
{
  const r = classify(goodSnapshot({
    files: [{ status: 'added', path: 'docs/notes/link.md', symlinkTarget: 'prompts/EDITORIAL_FILTER.md', isSymlink: true, additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a symlink pointing into a protected surface is RED', r.lane === LANE.RED);
}
{
  const r = classify(goodSnapshot({
    files: [{ status: 'added', path: 'newthing/file.md', additions: 1, deletions: 0 }],
  }), POLICY_WITH_CATEGORY);
  ok('a new top-level path fails closed to RED', r.lane === LANE.RED);
}

// ------------------------------------------------- T-5 owner decision cannot be GREEN

{
  const r = classify(goodSnapshot({ ownerDecisionRequired: true }), POLICY_WITH_CATEGORY);
  ok('T-5 an open OWNER_DECISION_REQUIRED is RED', r.lane === LANE.RED);
  ok('T-5 an open OWNER_DECISION_REQUIRED never auto-merges', r.autoMergeAllowed === false);
}

// ------------------------------------------- T-6 unknown or missing data fails closed

{
  const r = classify(goodSnapshot({ filesComplete: false }), POLICY_WITH_CATEGORY);
  ok('T-6 an incomplete file set is UNCLASSIFIED, not AMBER', r.lane === LANE.UNCLASSIFIED);
  ok('T-6 UNCLASSIFIED never auto-merges', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ headSha: 'a1b2c3d4e5' }), POLICY_WITH_CATEGORY);
  ok('T-6 an abbreviated head SHA is not evidence', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classify(goodSnapshot({ policyVersion: '0' }), POLICY_WITH_CATEGORY);
  ok('T-6 evidence under another policy version is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classify(goodSnapshot({ files: [{ status: 'modified', path: 'docs/notes/a.md', unreadable: true }] }), POLICY_WITH_CATEGORY);
  ok('T-6 an unreadable file is UNCLASSIFIED', r.lane === LANE.UNCLASSIFIED);
}
{
  const r = classify(goodSnapshot({ filesTruncated: true }), POLICY_WITH_CATEGORY);
  ok('a truncated list reported as complete is PROHIBITED', r.lane === LANE.PROHIBITED);
}

// ------------------------------------------------------------- T-7 AMBER never merges

{
  const r = classify(goodSnapshot({ files: [{ status: 'modified', path: 'docs/other/x.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-7 outside every category the lane is AMBER', r.lane === LANE.AMBER);
  ok('T-7 AMBER never auto-merges', r.autoMergeAllowed === false);
}

// ------------------------------ T-9 the builder cannot self-approve around the gate

{
  const r = classify(goodSnapshot({ declaration: { lane: LANE.GREEN, headSha: HEAD },
    files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }] }), POLICY_WITH_CATEGORY);
  ok('T-9 declaring GREEN over a protected change does not produce GREEN', r.lane === LANE.RED);
  ok('T-9 a declaration disagreeing with the computed lane is recorded', r.declarationMismatch === true);
  ok('T-9 a mismatched declaration withholds auto-merge', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ declaration: undefined }), POLICY_WITH_CATEGORY);
  ok('T-9 a missing declaration is not agreement', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ declaration: { lane: LANE.GREEN, headSha: OTHER } }), POLICY_WITH_CATEGORY);
  ok('T-9 a declaration bound to another head does not count', r.autoMergeAllowed === false);
}

// ------------------------------------------- T-10 the evaluator never runs PR code

{
  const r = classify(goodSnapshot({ evaluatorConsumesPullRequestCode: true }), POLICY_WITH_CATEGORY);
  ok('T-10 consuming pull-request-controlled code is PROHIBITED', r.lane === LANE.PROHIBITED);
  ok('T-10 PROHIBITED never auto-merges', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({
    files: [{ status: 'modified', path: 'AGENTS.md', additions: 1, deletions: 0 }],
    mandateSource: 'pull_request',
  }), POLICY_WITH_CATEGORY);
  ok('a PR rewriting its own mandate under its own version is PROHIBITED', r.lane === LANE.PROHIBITED);
}
{
  const r = classify(goodSnapshot({ secretsDetected: true }), POLICY_WITH_CATEGORY);
  ok('a credential in the diff is PROHIBITED, not owner-approvable', r.lane === LANE.PROHIBITED);
}

// ------------------------------------------------------- merge atomicity and switch

{
  const r = classify(goodSnapshot({ mergeAtomicity: 'none' }), POLICY_WITH_CATEGORY);
  ok('without atomic merge enforcement GREEN withholds auto-merge', r.lane === LANE.GREEN && r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ mergeAtomicity: 'merge_queue' }), POLICY_WITH_CATEGORY);
  ok('a merge queue satisfies atomicity', r.autoMergeAllowed === true);
}
{
  const r = classify(goodSnapshot({ killSwitch: { readable: false, autoMergeDisabled: false } }), POLICY_WITH_CATEGORY);
  ok('an unreadable kill switch fails closed', r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ killSwitch: { readable: true, autoMergeDisabled: true } }), POLICY_WITH_CATEGORY);
  ok('the kill switch stops auto-merge without changing the lane', r.lane === LANE.GREEN && r.autoMergeAllowed === false);
}
{
  const r = classify(goodSnapshot({ baseIsCurrent: false }), POLICY_WITH_CATEGORY);
  ok('a base that has moved blocks readiness, not the lane', r.lane === LANE.GREEN && r.readiness.includes('BLOCKED_STALE_BASE'));
}
{
  const r = classify(goodSnapshot({ mergeable: false }), POLICY_WITH_CATEGORY);
  ok('a merge conflict blocks readiness, not the lane', r.lane === LANE.GREEN && r.readiness.includes('BLOCKED_MERGE_CONFLICT'));
}

// ------------------------------------------------------- category composition rules

{
  const twoCategories = { greenAllowlist: [
    { name: 'docs-notes', paths: ['docs/notes/'], limits: {} },
    { name: 'tests', paths: ['tests/'], limits: {} },
  ] };
  const r = classify(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', additions: 1, deletions: 0 },
    { status: 'modified', path: 'tests/t.js', additions: 1, deletions: 0 },
  ] }), twoCategories);
  ok('two approved categories in one PR are not an approved category', r.lane === LANE.AMBER);
}
{
  const r = classify(goodSnapshot({ files: [
    { status: 'modified', path: 'docs/notes/a.md', additions: 999, deletions: 0 },
  ] }), POLICY_WITH_CATEGORY);
  ok('exceeding a category limit is AMBER', r.lane === LANE.AMBER);
}
for (const kind of ['isSymlink', 'isSubmodule', 'isBinary', 'modeChanged']) {
  const file = { status: 'modified', path: 'docs/notes/a.md', additions: 1, deletions: 0 };
  file[kind] = true;
  const r = classify(goodSnapshot({ files: [file] }), POLICY_WITH_CATEGORY);
  ok(`a file that is ${kind} fails closed out of GREEN`, r.lane === LANE.AMBER);
}
{
  const r = classify(goodSnapshot({ isFork: true }), POLICY_WITH_CATEGORY);
  ok('a fork pull request is never GREEN', r.lane === LANE.AMBER);
}
{
  const r = classify(goodSnapshot({ authorIsAutomationIdentity: false }), POLICY_WITH_CATEGORY);
  ok('an author that is not the automation identity is never GREEN', r.lane === LANE.AMBER);
}
{
  const r = classify(goodSnapshot({ authorization: { taskId: 'x', mutableByThisPullRequest: true } }), POLICY_WITH_CATEGORY);
  ok('an authorisation this PR could alter is not authorisation', r.lane === LANE.AMBER);
}
{
  const r = classify(goodSnapshot({ baseRef: 'release' }), POLICY_WITH_CATEGORY);
  ok('a PR not targeting the default branch is never GREEN', r.lane === LANE.AMBER);
}

// ---------------------------------------------------------------- ordering and shape

{
  const r = classify(goodSnapshot({ secretsDetected: true, filesComplete: false,
    files: [{ status: 'modified', path: 'AGENTS.md' }] }), POLICY_WITH_CATEGORY);
  ok('PROHIBITED is evaluated before every other state', r.lane === LANE.PROHIBITED);
}
{
  const r = classify(goodSnapshot({ filesComplete: false,
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

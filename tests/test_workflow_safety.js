'use strict';

/**
 * Executable acceptance for the workflow files themselves (Issue #7, acceptance 10).
 *
 * That criterion — that privileged logic never executes pull-request-supplied code or
 * secrets in its trusted context — is a static property of the YAML, so it is asserted
 * by reading the workflow definitions rather than by running one.
 *
 * **It parses YAML (DEC-011)** rather than matching its text, which five review cycles
 * established as the only correct approach: escapes decode, and every pattern was one
 * encoding away from passing something it should have refused.
 *
 * **It decides rather than analyses.** Three further cycles were spent teaching this
 * suite to judge which interpolations were safe — parsing GitHub expression syntax with
 * a pattern that stopped at the first `}`, then chasing the shell constructs that
 * re-execute a value: command substitution, backticks, arithmetic, process substitution,
 * prompt expansion. Each fix admitted the next construct, and one was wrong in both
 * directions at once.
 *
 * The workflow needs none of that latitude, so the rules are now closed questions with
 * a yes or no answer: no expression reaches a shell, no expression enters `env` unless
 * it is one of a few approved whole forms, and the one script that carries the checkout
 * binding is compared in full against the script it must be. What cannot be decided by
 * looking is refused. A workflow that genuinely needs more is a decision to take, not a
 * pattern to widen.
 */

const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

const WORKFLOWS = path.join(__dirname, '..', '.github', 'workflows');

/**
 * The complete expressions a workflow may carry, in a checkout `ref` or an `env` value.
 * Matched whole, never searched: a scalar merely *containing* an approved token —
 * `${{ github.sha && github.event.before }}` — evaluates to something else entirely.
 */
const APPROVED_EXPRESSIONS = [
  '${{ github.sha }}',
  '${{ github.event.merge_group.head_sha || github.sha }}',
  '${{ github.event.pull_request.head.sha }}',
];

/**
 * The verifier, in full. It is the only script permitted to carry the checkout binding,
 * and it is compared whole. Matching `EXPECTED_SHA`, `git rev-parse` and a comparison
 * operator anywhere was satisfied by decoys that compared nothing — three attempts at
 * this assertion were fooled the same way before it became an equality test.
 */
const APPROVED_VERIFIER_SCRIPT = `
actual="$(git rev-parse HEAD)"
if [ "$actual" != "$EXPECTED_SHA" ]; then
  echo "checked out $actual but the head under test is $EXPECTED_SHA" >&2
  exit 1
fi
echo "tested commit: $actual"
`;

let checks = 0;
let failed = 0;

function ok(name, condition) {
  checks += 1;
  if (condition) console.log(`  ok   ${name}`);
  else { failed += 1; console.log(`  FAIL ${name}`); }
}

function canonical(text) {
  return String(text === undefined || text === null ? '' : text).trim().replace(/\s+/g, ' ');
}

function isApprovedExpression(value) {
  return APPROVED_EXPRESSIONS.map(canonical).includes(canonical(value));
}

/** Walk a parsed document, yielding every [pathSegments, scalar] pair. */
function* walk(node, trail = []) {
  if (Array.isArray(node)) {
    for (let i = 0; i < node.length; i += 1) yield* walk(node[i], trail.concat(i));
  } else if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) yield* walk(v, trail.concat(k));
  } else {
    yield [trail, node];
  }
}

function jobs(doc) {
  return Object.entries((doc && doc.jobs) || {}).filter(([, j]) => j && typeof j === 'object');
}

function steps(doc) {
  return jobs(doc).flatMap(([name, job]) =>
    (Array.isArray(job.steps) ? job.steps : []).map((step) => [name, job, step]));
}

/** Every resolved `run:` scalar, wherever a step sits and however the key was written. */
function runScripts(doc) {
  const out = [];
  for (const [trail, value] of walk(doc)) {
    if (trail[trail.length - 1] === 'run' && typeof value === 'string') out.push(value);
  }
  return out;
}

/**
 * The two places an expression may appear: a checkout step's `with.ref`, and an `env`
 * value. Anywhere else — `shell`, `if`, `uses`, a step name — it is refused.
 */
function allowedExpressionLocation(trail) {
  const last = trail[trail.length - 1];
  const prev = trail[trail.length - 2];
  if (prev === 'env') return 'env';
  if (last === 'ref' && prev === 'with') return 'ref';
  return null;
}

/** Every `env` value in the document, as [name, value]. */
function envValues(doc) {
  const out = [];
  for (const [trail, value] of walk(doc)) {
    const i = trail.lastIndexOf('env');
    if (i !== -1 && i === trail.length - 2) out.push([String(trail[i + 1]), String(value)]);
  }
  return out;
}

/**
 * Token permissions are the file-level declaration and each job's, and nothing else.
 * Treating any trail containing `permissions` as a grant read `env: { permissions:
 * write }` and a reusable-workflow input of that name as write access.
 */
function permissionScopes(doc) {
  const out = [];
  if (doc && doc.permissions !== undefined) out.push(doc.permissions);
  for (const [, job] of jobs(doc)) if (job.permissions !== undefined) out.push(job.permissions);
  return out;
}

function grantsWrite(scope) {
  if (typeof scope === 'string') return /^write(-all)?$/.test(scope);
  if (scope && typeof scope === 'object') {
    return Object.values(scope).some((v) => /^write$/.test(String(v)));
  }
  return false;
}

/**
 * Any use of the credential context, not merely a named member of it. `toJSON(secrets)`
 * and a bare `${{ secrets }}` consume the whole thing while matching no `secrets.`
 * token, and `github[format('to{0}', 'ken')]` reaches the job credential without
 * spelling it — so computed access to `github` is refused as unprovable by inspection.
 */
function referencesCredential(text) {
  const t = String(text);
  return /\bsecrets\b/.test(t) || /\bgithub\s*\.\s*token\b/.test(t) || /\bgithub\s*\[/.test(t);
}

const files = fs.existsSync(WORKFLOWS)
  ? fs.readdirSync(WORKFLOWS).filter((f) => /\.ya?ml$/.test(f))
  : [];

ok('at least one workflow exists to check', files.length > 0);

for (const file of files) {
  const text = fs.readFileSync(path.join(WORKFLOWS, file), 'utf8');
  let doc = null;
  try {
    // Duplicate keys are an error rather than last-one-wins: two `permissions` blocks
    // would otherwise let the harmless one be the visible answer.
    doc = YAML.parse(text, { uniqueKeys: true, strict: true });
  } catch (e) {
    doc = null;
  }
  ok(`${file}: parses as YAML`, doc !== null);
  if (!doc) continue;

  const source = JSON.stringify(doc);

  // `pull_request_target` runs with a write-capable token in the base repository's
  // context. Nothing here needs it, and it is the sharpest edge in a public repository.
  ok(`${file}: does not use pull_request_target`,
     !Object.prototype.hasOwnProperty.call(doc.on || {}, 'pull_request_target'));

  ok(`${file}: declares permissions`, doc.permissions !== undefined);
  ok(`${file}: grants no write permission`, !permissionScopes(doc).some(grantsWrite));
  ok(`${file}: references no credential`, !referencesCredential(source));

  // `secrets: inherit` hands the called workflow every secret the caller holds while
  // naming none of them, so no check over names can see it.
  ok(`${file}: inherits no secrets into a reusable workflow`,
     !jobs(doc).some(([, job]) => job.secrets === 'inherit'));

  // A local composite action carries its own run steps, which this suite does not walk.
  // Refused until it does, rather than trusted unread.
  ok(`${file}: calls no local composite action`,
     !steps(doc).some(([, , st]) => typeof st.uses === 'string' && st.uses.startsWith('./')));

  // An expression may appear in exactly two places, and must be an approved whole form
  // in both. Listing the places it may *not* appear was the earlier shape, and it missed
  // `shell:` — where a commit message can choose the command that runs the script while
  // no expression appears in the script itself. Naming the permitted locations is a
  // closed question; naming the forbidden ones never finishes.
  const misplaced = [];
  for (const [trail, value] of walk(doc)) {
    if (typeof value !== 'string' || !value.includes('${{')) continue;
    const where = allowedExpressionLocation(trail);
    if (!where || !isApprovedExpression(value)) misplaced.push(`${trail.join('.')} = ${value}`);
  }
  ok(`${file}: every expression is an approved form in a permitted location`,
     misplaced.length === 0);

  // External actions run with the repository token, so a mutable tag is a second author
  // of this evidence.
  const unpinned = steps(doc).filter(([, , st]) =>
    typeof st.uses === 'string' && !st.uses.startsWith('./') &&
    !/@[0-9a-f]{40}$/i.test(st.uses));
  ok(`${file}: every external action is pinned to an immutable commit`, unpinned.length === 0);

  // Each checkout is judged on its own `with`, not on a `ref` some other step carries.
  const checkouts = steps(doc).filter(([, , st]) =>
    typeof st.uses === 'string' && /^actions\/checkout(@|$)/.test(st.uses));
  for (const [jobName, job, step] of checkouts) {
    const w = step.with || {};
    const ref = w.ref === undefined ? '' : String(w.ref);
    ok(`${file}: checkout in ${jobName} names an approved head expression`,
       isApprovedExpression(ref));
    ok(`${file}: checkout in ${jobName} does not persist credentials`,
       w['persist-credentials'] === false);
    const verifiers = (Array.isArray(job.steps) ? job.steps : []).filter((st) =>
      String((st.env || {}).EXPECTED_SHA) === ref &&
      canonical(st.run) === canonical(APPROVED_VERIFIER_SCRIPT));
    ok(`${file}: the checkout in ${jobName} is verified by the approved script`,
       verifiers.length > 0);
  }

  // A merge queue evaluates a commit of its own; without this trigger the queued commit
  // never receives the required check (docs/autonomy/IDENTITY_AND_PERMISSIONS.md §3).
  ok(`${file}: runs for merge-queue commits`,
     Object.prototype.hasOwnProperty.call(doc.on || {}, 'merge_group'));

  // Fork pull requests are refused in v1 (DEC-011), so no workflow runs on one.
  ok(`${file}: does not run on pull_request events`,
     !Object.prototype.hasOwnProperty.call(doc.on || {}, 'pull_request'));
}

// ---------------------------------------------------------------- the rules themselves

// The parser earns its place on these: every one passed a text-matching predecessor.
{
  const escaped = YAML.parse('steps:\n  - { "r\\u0075n": "echo hello" }');
  ok('an escaped run key decodes and is seen', runScripts(escaped).length === 1);
}
{
  const escaped = YAML.parse('permissions:\n  contents: "wr\\u0069te"');
  ok('an escaped write permission decodes', permissionScopes(escaped).some(grantsWrite));
}
{
  const flow = YAML.parse('steps: [{ run: "echo hi" }]');
  ok('a flow-style step is read like any other', runScripts(flow).length === 1);
}
{
  let threw = false;
  try {
    YAML.parse('permissions:\n  contents: read\npermissions:\n  contents: write',
               { uniqueKeys: true });
  } catch (e) { threw = true; }
  ok('a duplicate key is an error, not a silent override', threw);
}

// Expressions in a run script are refused whatever their shape, which is why no shape
// has to be understood. Each of these defeated a previous version of this suite.
for (const [label, script] of [
  ['a nested format() call', "echo ${{ format('{0}', github.event.pull_request.title) }}"],
  ['a compound expression', 'echo ${{ github.sha && github.head_ref }}'],
  ['the workflow name', 'echo ${{ github.workflow }}'],
  ['a bare branch name', 'echo ${{ github.head_ref }}'],
]) {
  ok(`an expression in a run script is refused: ${label}`, script.includes('${{'));
}
ok('a script with no expression is fine', !'node tests/test_lane_gate.js'.includes('${{'));

// Shell constructs no longer need classifying, because no untrusted value can be there
// to execute. These are the four that were chased across four cycles.
for (const script of ['eval "$MESSAGE"', 'echo "$((MESSAGE))"', 'cat <($MESSAGE)',
                      'echo "${MESSAGE@P}"']) {
  ok(`no rule is needed for: ${script}`, !script.includes('${{'));
}

for (const [label, text] of [
  ['the whole credential context', '${{ toJSON(secrets) }}'],
  ['a bare credential context', '${{ secrets }}'],
  ['computed access to github', "${{ github[format('to{0}', 'ken')] }}"],
  ['the job credential', '${{ github.token }}'],
  ['bracket-form access', "${{ secrets['TOKEN'] }}"],
]) {
  ok(`credential use is detected: ${label}`, referencesCredential(text));
}
ok('an ordinary context is not a credential', !referencesCredential('${{ github.sha }}'));

for (const [label, expr] of [
  ['an approved head expression', '${{ github.sha }}'],
  ['the merge-queue form', '${{ github.event.merge_group.head_sha || github.sha }}'],
]) {
  ok(`accepted: ${label}`, isApprovedExpression(expr));
}
for (const [label, expr] of [
  ['a scalar merely containing one', '${{ github.sha && github.event.before }}'],
  ['the base commit', '${{ github.event.pull_request.base.sha }}'],
  ['an untrusted title', '${{ github.event.pull_request.title }}'],
  ['nothing at all', ''],
]) {
  ok(`refused: ${label}`, !isApprovedExpression(expr));
}
{
  const decoy = 'git rev-parse HEAD >/dev/null; if [ x != y ]; then :; fi; echo "$EXPECTED_SHA"';
  ok('a decoy verifier does not equal the approved script',
     canonical(decoy) !== canonical(APPROVED_VERIFIER_SCRIPT));
}
{
  const doc = YAML.parse('jobs:\n  a:\n    uses: ./.github/workflows/x.yml\n    secrets: inherit');
  ok('an inherited-secrets job is detected', jobs(doc).some(([, j]) => j.secrets === 'inherit'));
}
{
  const doc = YAML.parse('permissions:\n  contents: read\njobs:\n  a:\n    env:\n      permissions: write');
  ok('an unrelated key named permissions is not a token grant',
     !permissionScopes(doc).some(grantsWrite));
}
{
  const doc = YAML.parse('permissions:\n  contents: read\njobs:\n  a:\n    permissions: write-all');
  ok('a job widening the token is a grant', permissionScopes(doc).some(grantsWrite));
}
{
  const doc = YAML.parse([
    'jobs:', '  a:', '    steps:',
    '      - env:', '          MESSAGE: ${{ github.event.head_commit.message }}',
    '        run: echo hi',
  ].join('\n'));
  const bad = envValues(doc).filter(([, v]) => v.includes('${{') && !isApprovedExpression(v));
  ok('untrusted text in env is refused before any script can reach it', bad.length === 1);
}
{
  // The shell selector: no expression in the script, nothing in env, and the commit
  // message still chooses the command that runs it.
  const doc = YAML.parse([
    'jobs:', '  a:', '    steps:',
    '      - run: echo ok',
    '        shell: ${{ github.event.head_commit.message }} {0}',
  ].join('\n'));
  const misplaced = [];
  for (const [trail, value] of walk(doc)) {
    if (typeof value === 'string' && value.includes('${{') && !allowedExpressionLocation(trail)) {
      misplaced.push(trail.join('.'));
    }
  }
  ok('an expression in a shell selector is refused', misplaced.length === 1);
}
for (const [label, trail] of [
  ['an env value', ['jobs', 'a', 'steps', 0, 'env', 'EXPECTED_SHA']],
  ['a checkout ref', ['jobs', 'a', 'steps', 0, 'with', 'ref']],
]) {
  ok(`a permitted location: ${label}`, allowedExpressionLocation(trail) !== null);
}
for (const [label, trail] of [
  ['a shell selector', ['jobs', 'a', 'steps', 0, 'shell']],
  ['a condition', ['jobs', 'a', 'steps', 0, 'if']],
  ['a step name', ['jobs', 'a', 'steps', 0, 'name']],
  ['an action reference', ['jobs', 'a', 'steps', 0, 'uses']],
]) {
  ok(`a forbidden location: ${label}`, allowedExpressionLocation(trail) === null);
}
for (const [label, uses] of [
  ['a tag', 'actions/checkout@v4'],
  ['a branch', 'actions/checkout@main'],
  ['a short SHA', 'actions/checkout@11d5960'],
]) {
  ok(`an unpinned action is refused: ${label}`, !/@[0-9a-f]{40}$/i.test(uses));
}
ok('a full-SHA pin is accepted',
   /@[0-9a-f]{40}$/i.test('actions/checkout@11d5960a326750d5838078e36cf38b85af677262'));

console.log('');
if (failed > 0) {
  console.log(`FAILED (${failed} of ${checks} checks)`);
  process.exit(1);
}
console.log(`ALL PASS (${checks} checks)`);

'use strict';

/**
 * Executable acceptance for the workflow files themselves (Issue #7, acceptance 10).
 *
 * That criterion — that privileged logic never executes pull-request-supplied code or
 * secrets in its trusted context — is a static property of the YAML, not a runtime one,
 * so it is asserted here by reading the workflow definitions rather than by running one.
 *
 * **This suite parses YAML (DEC-011).** Five review cycles established that matching
 * text cannot do it: the extractor was extended for quoted keys, then a spaced colon,
 * then flow mappings, then to count keys independently so an unparsed shape would fail —
 * and `"run"` decoded past all of it, as `"write"` decoded past the
 * permissions check. YAML resolves escapes; a pattern over its source text does not, and
 * every failure was in the direction of passing. The owner chose correctness of the
 * check over the repository's dependency-free tooling, so this file needs `npm ci` while
 * every other suite still needs nothing.
 */

const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

const WORKFLOWS = path.join(__dirname, '..', '.github', 'workflows');

/**
 * Contexts whose value a pull request cannot influence, and which are therefore safe to
 * interpolate into a shell. An allowlist, because a denylist cannot be defeated only by
 * the spellings someone remembered: a branch name, a title, a body and a label are all
 * attacker-chosen. `github.token` is absent deliberately — it is the job credential.
 */
const IMMUTABLE_CONTEXTS = [
  'github.sha', 'github.repository', 'github.repository_owner', 'github.run_id',
  'github.run_number', 'github.run_attempt', 'github.job',
  'github.event_name', 'github.api_url', 'github.server_url', 'github.workspace',
  'github.action', 'github.action_path',
  // Machine-generated commit identifiers, not text a pull request writes.
  'github.event.merge_group.head_sha', 'github.event.pull_request.head.sha',
];
// `github.workflow` is deliberately absent: it resolves to the workflow's own `name`,
// which a pull request editing the file chooses, metacharacters included.

/**
 * Shell constructs that execute a string as code. Command substitution of a fixed
 * command — `$(git rev-parse HEAD)` — is ordinary and not listed: what matters is
 * handing a *value* back to a shell.
 */
const RE_EVALUATION = /(^|[\s;&|(])(eval|source|\.)\s|(^|[\s;&|(])(ba|z|k)?sh\s+-c\b/;

/** A value that carries a context a pull request can influence. */
function isTainted(value) {
  return expressions(value).some((expr) =>
    contextsIn(expr).some((ref) =>
      !IMMUTABLE_CONTEXTS.some((c) => ref === c || ref.startsWith(`${c}.`))));
}

/**
 * Environment variables whose value carries untrusted text, at any level. Routing such
 * a value through `env` is the recommended mitigation; the residual risk is a step that
 * then feeds the variable back to a shell.
 */
function taintedEnvNames(doc) {
  const names = new Set();
  for (const [trail, value] of walk(doc)) {
    const i = trail.lastIndexOf('env');
    if (i !== -1 && i === trail.length - 2 && isTainted(value)) names.add(String(trail[i + 1]));
  }
  return names;
}

/** Every job in a parsed workflow, as [name, job] pairs. */
function jobs(doc) {
  return Object.entries((doc && doc.jobs) || {}).filter(([, j]) => j && typeof j === 'object');
}

/** Every step of every job. */
function steps(doc) {
  return jobs(doc).flatMap(([name, job]) =>
    (Array.isArray(job.steps) ? job.steps : []).map((step) => [name, job, step]));
}

/**
 * Token permissions are the file-level declaration and each job's, and nothing else.
 * Treating any trail containing `permissions` as a grant reported `env: { permissions:
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

let checks = 0;
let failed = 0;

function ok(name, condition) {
  checks += 1;
  if (condition) console.log(`  ok   ${name}`);
  else { failed += 1; console.log(`  FAIL ${name}`); }
}

/** Walk a parsed document, yielding every [pathSegments, value] pair. */
function* walk(node, trail = []) {
  if (Array.isArray(node)) {
    for (let i = 0; i < node.length; i += 1) yield* walk(node[i], trail.concat(i));
  } else if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) yield* walk(v, trail.concat(k));
  } else {
    yield [trail, node];
  }
}

/** Every resolved `run:` scalar, wherever a step sits and however the key was written. */
function runScripts(doc) {
  const out = [];
  for (const [trail, value] of walk(doc)) {
    if (trail[trail.length - 1] === 'run' && typeof value === 'string') out.push(value);
  }
  return out;
}

/** Every `${{ ... }}` expression in a fragment. */
function expressions(fragment) {
  return [...String(fragment).matchAll(/\$\{\{([^}]*)\}\}/g)].map((m) => m[1].trim());
}

/** Every context reference inside one expression, not merely the one it starts with. */
function contextsIn(expression) {
  return [...String(expression).matchAll(
    /\b(github|secrets|env|inputs|needs|vars|steps|job|runner|matrix)((?:\s*\.\s*[A-Za-z0-9_-]+|\s*\[[^\]]*\])*)/g
  )].map((m) => (m[1] + m[2]).replace(/\s+/g, ''));
}

function referencesCredential(text) {
  const t = String(text);
  return /\bsecrets\s*(\.|\[)/.test(t) || /\bgithub\s*\.\s*token\b/.test(t) ||
         /\bgithub\s*\[\s*['"]token['"]\s*\]/.test(t);
}

const files = fs.existsSync(WORKFLOWS)
  ? fs.readdirSync(WORKFLOWS).filter((f) => /\.ya?ml$/.test(f))
  : [];

ok('at least one workflow exists to check', files.length > 0);

for (const file of files) {
  const text = fs.readFileSync(path.join(WORKFLOWS, file), 'utf8');
  let doc = null;
  let parseError = null;
  try {
    // Duplicate keys are an error rather than a last-one-wins silent override: two
    // `permissions` blocks would otherwise let the harmless one be the visible answer.
    doc = YAML.parse(text, { uniqueKeys: true, strict: true });
  } catch (e) {
    parseError = e;
  }
  ok(`${file}: parses as YAML`, parseError === null && doc !== null);
  if (!doc) continue;

  const source = JSON.stringify(doc);

  // `pull_request_target` runs with a write-capable token in the base repository's
  // context. Nothing here needs it, and it is the sharpest edge in a public repository.
  ok(`${file}: does not use pull_request_target`,
     !Object.prototype.hasOwnProperty.call(doc.on || {}, 'pull_request_target'));

  ok(`${file}: declares permissions`, doc.permissions !== undefined);
  ok(`${file}: grants no write permission`, !permissionScopes(doc).some(grantsWrite));

  ok(`${file}: references no credential`, !referencesCredential(source));

  // `secrets: inherit` hands the called workflow every secret the caller holds, and
  // names none of them, so no textual check can see it.
  ok(`${file}: inherits no secrets into a reusable workflow`,
     !jobs(doc).some(([, job]) => job.secrets === 'inherit'));

  // A local composite action carries its own run steps, which this suite does not walk.
  // Refused until it does, rather than trusted unread.
  ok(`${file}: calls no local composite action`,
     !steps(doc).some(([, , st]) => typeof st.uses === 'string' && st.uses.startsWith('./')));

  // Untrusted text — a title, a body, a branch name — interpolated into a shell is
  // command injection. Values reach `run:` through `env:` instead, so a run script may
  // name only contexts a pull request cannot influence.
  const offending = [];
  for (const script of runScripts(doc)) {
    for (const expr of expressions(script)) {
      const refs = contextsIn(expr);
      if (refs.length === 0) { offending.push(expr); continue; }
      for (const ref of refs) {
        if (!IMMUTABLE_CONTEXTS.some((c) => ref === c || ref.startsWith(`${c}.`))) {
          offending.push(`${expr} (via ${ref})`);
        }
      }
    }
  }
  ok(`${file}: no mutable context is interpolated into a run script`, offending.length === 0);

  // Routing an untrusted value through `env` is the mitigation, not the end of it: a
  // step can still hand the variable back to a shell to execute. Re-evaluation is
  // refused outright, which is simpler than tracing taint and fails in the safe
  // direction.
  const tainted = taintedEnvNames(doc);
  const reEvaluated = runScripts(doc).filter((script) =>
    RE_EVALUATION.test(script) ||
    [...tainted].some((n) => new RegExp(`[\`$]\\(?\\{?${n}\\b`).test(script)));
  ok(`${file}: no run script re-evaluates untrusted text as code`, reEvaluated.length === 0);

  // The merge-ref trap: a checkout naming no ref takes the event default, which for a
  // pull request is a synthetic merge commit that attests nothing about H.
  // Each checkout is judged on its own `with`, not on a `ref` some other step happens to
  // carry: collecting them globally let a checkout with no ref inherit another's.
  const checkouts = steps(doc).filter(([, , st]) =>
    typeof st.uses === 'string' && /^actions\/checkout(@|$)/.test(st.uses));
  for (const [jobName, job, step] of checkouts) {
    const w = step.with || {};
    const ref = w.ref === undefined ? '' : String(w.ref);
    const namesHead =
      /github\.sha|merge_group\.head_sha|pull_request\.head\.sha/.test(ref) &&
      !/\bbase\.sha\b/.test(ref);
    ok(`${file}: checkout in ${jobName} names the head under test`, namesHead);
    ok(`${file}: checkout in ${jobName} does not persist credentials`,
       w['persist-credentials'] === false);
    const verifiers = (Array.isArray(job.steps) ? job.steps : [])
      .map((st) => (st.env || {}).EXPECTED_SHA)
      .filter((v) => v !== undefined).map(String);
    ok(`${file}: the SHA verified in ${jobName} is the one checked out`,
       verifiers.length > 0 && verifiers.includes(ref));
  }

  // A merge queue evaluates a commit of its own; without this trigger the queued commit
  // never receives the required check (docs/autonomy/IDENTITY_AND_PERMISSIONS.md §3).
  ok(`${file}: runs for merge-queue commits`,
     Object.prototype.hasOwnProperty.call(doc.on || {}, 'merge_group'));

  // Fork pull requests are refused in v1 (DEC-011), so no workflow may run on one.
  ok(`${file}: does not run on pull_request events`,
     !Object.prototype.hasOwnProperty.call(doc.on || {}, 'pull_request'));
}

// The parser is the point of this suite, so the evasions that defeated its predecessors
// are asserted directly. Each of these passed every text-matching version.
{
  const escaped = YAML.parse('steps:\n  - { "r\\u0075n": "echo ${{ github.head_ref }}" }');
  ok('an escaped run key decodes and is seen', runScripts(escaped).length === 1);
  ok('its mutable context is then visible',
     contextsIn(expressions(runScripts(escaped)[0])[0]).includes('github.head_ref'));
}
{
  const escaped = YAML.parse('permissions:\n  contents: "wr\\u0069te"');
  ok('an escaped write permission decodes', permissionScopes(escaped).some(grantsWrite));
}
{
  const flow = YAML.parse('steps: [{ run: "echo ${{ github.actor }}" }]');
  ok('a flow-style step is read like any other', runScripts(flow).length === 1);
}
{
  let threw = false;
  try { YAML.parse('permissions:\n  contents: read\npermissions:\n  contents: write',
                   { uniqueKeys: true }); } catch (e) { threw = true; }
  ok('a duplicate key is an error, not a silent override', threw);
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
for (const script of ['eval "$MESSAGE"', 'sh -c "$MESSAGE"', 'bash -c "$X"',
                      'zsh -c "$X"', '. /dev/stdin']) {
  ok(`re-evaluation is refused: ${script}`, RE_EVALUATION.test(script));
}
for (const script of ['node tests/test_lane_gate.js', 'actual="$(git rev-parse HEAD)"']) {
  ok(`an ordinary script is not re-evaluation: ${script}`, !RE_EVALUATION.test(script));
}
{
  // The shape the finding described: untrusted text parked in env, then executed.
  const doc = YAML.parse([
    'jobs:', '  a:', '    steps:',
    '      - env:', '          MESSAGE: ${{ github.event.head_commit.message }}',
    '        run: eval "$MESSAGE"',
  ].join('\n'));
  ok('an untrusted env value is recognised as tainted',
     taintedEnvNames(doc).has('MESSAGE'));
  ok('and executing it is refused', RE_EVALUATION.test(runScripts(doc)[0]));
}
{
  const doc = YAML.parse([
    'jobs:', '  a:', '    steps:',
    '      - env:', '          SAFE: ${{ github.sha }}', '        run: echo "$SAFE"',
  ].join('\n'));
  ok('an immutable env value is not tainted', !taintedEnvNames(doc).has('SAFE'));
}
ok('the workflow name is not an immutable context',
   !IMMUTABLE_CONTEXTS.includes('github.workflow'));
ok('the job credential counts as a credential', referencesCredential('${{ github.token }}'));
ok('bracket-form credential access counts', referencesCredential("${{ secrets['TOKEN'] }}"));
ok('a compound expression exposes every context it names',
   contextsIn('github.sha && github.head_ref').includes('github.head_ref'));

console.log('');
if (failed > 0) {
  console.log(`FAILED (${failed} of ${checks} checks)`);
  process.exit(1);
}
console.log(`ALL PASS (${checks} checks)`);

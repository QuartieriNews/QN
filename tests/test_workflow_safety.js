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
  'github.run_number', 'github.run_attempt', 'github.job', 'github.workflow',
  'github.event_name', 'github.api_url', 'github.server_url', 'github.workspace',
  'github.action', 'github.action_path',
];

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

/** Every resolved permission value, top-level or per job. */
function permissionValues(doc) {
  const out = [];
  for (const [trail, value] of walk(doc)) {
    if (trail.includes('permissions')) out.push(String(value));
  }
  // `permissions: write-all` is a scalar rather than a mapping, so walk() yields it with
  // 'permissions' as the last segment; both shapes land in the same list.
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
  const writes = permissionValues(doc).filter((v) => /^write(-all)?$/.test(v));
  ok(`${file}: grants no write permission`, writes.length === 0);

  ok(`${file}: references no credential`, !referencesCredential(source));

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

  // The merge-ref trap: a checkout naming no ref takes the event default, which for a
  // pull request is a synthetic merge commit that attests nothing about H.
  if (/actions\/checkout/.test(source)) {
    const refs = [];
    const expected = [];
    for (const [trail, value] of walk(doc)) {
      if (trail[trail.length - 1] === 'ref') refs.push(String(value));
      if (trail[trail.length - 1] === 'EXPECTED_SHA') expected.push(String(value));
    }
    const namesHead = refs.length > 0 && refs.every(
      (r) => /github\.sha|merge_group\.head_sha|pull_request\.head\.sha/.test(r) &&
             !/\bbase\.sha\b/.test(r));
    ok(`${file}: checkout names the head under test`, namesHead);
    ok(`${file}: the verified SHA is the one checked out`,
       expected.length > 0 && expected.every((e) => refs.includes(e)));
    ok(`${file}: checkout does not persist credentials`,
       /"persist-credentials":false/.test(source.replace(/\s/g, '')));
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
  ok('an escaped write permission decodes',
     permissionValues(escaped).some((v) => v === 'write'));
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

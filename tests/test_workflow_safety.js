/**
 * test_workflow_safety.js — structural assertions about .github/workflows/checks.yml.
 *
 * Six questions, each answerable from the parsed document rather than from matching
 * text. DEC-011 §1: a regular expression is not a YAML parser, and any text-matching
 * approach is one encoding away from being wrong in the direction of passing.
 *
 * This suite deliberately does not try to be a GitHub Actions security scanner. It
 * asserts the properties the owner relies on when reading a check result, and nothing
 * more (DEC-012).
 *
 * Run:  node tests/test_workflow_safety.js   (needs `npm ci`; exit 0 and "ALL PASS")
 */

'use strict';

const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

const WORKFLOW = path.join(__dirname, '..', '.github', 'workflows', 'checks.yml');

let failures = 0;
let checks = 0;

function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) {
    console.log(`  ok   ${label}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`);
  }
}

const source = fs.readFileSync(WORKFLOW, 'utf8');

console.log('The file is a workflow this suite actually read');
let doc = null;
let parseError = null;
try { doc = YAML.parse(source); } catch (e) { parseError = e.message; }
check('parses as YAML', parseError, null);
check('has jobs', doc && typeof doc.jobs === 'object' && Object.keys(doc.jobs).length > 0, true);

const jobs = Object.values((doc && doc.jobs) || {});
const steps = jobs.flatMap((job) => (Array.isArray(job.steps) ? job.steps : []));

/** Every string value in the parsed document — comments are not part of its meaning. */
function strings(node) {
  if (typeof node === 'string') return [node];
  if (Array.isArray(node)) return node.flatMap(strings);
  if (node && typeof node === 'object') {
    return Object.entries(node).flatMap(([k, v]) => [String(k), ...strings(v)]);
  }
  return [];
}

console.log('');
console.log('It cannot run with the permissions of the branch it tests');
{
  // `on:` parses as the boolean true in YAML 1.1; the parser gives us both spellings.
  const triggers = Object.keys((doc && (doc.on || doc[true])) || {});
  check('triggers are the two declared', triggers.sort(), ['pull_request', 'push']);
  check('no pull_request_target trigger', triggers.includes('pull_request_target'), false);
}
check('the token is read-only for the whole file', doc && doc.permissions, { contents: 'read' });
check('no job widens the file-level permissions',
  jobs.filter((job) => job.permissions !== undefined).length, 0);

console.log('');
console.log('The lane job is told the two facts it cannot compute from the diff');
{
  const laneJob = (doc && doc.jobs && doc.jobs.lane) || {};
  const classify = (laneJob.steps || []).find((s) => typeof s.run === 'string' && s.run.includes('gate.js'));
  const env = (classify && classify.env) || {};
  check('fork provenance and escalation are both supplied',
    ['LANE_FORK', 'LANE_ESCALATED'].filter((k) => !(k in env)), []);
  check('and both are passed to the classifier',
    ['--fork', '--escalated'].filter((f) => !classify.run.includes(f)), []);
}

console.log('');
console.log('It has nothing to leak and nothing to be injected with');
check('the secrets context appears in no value of the document',
  strings(doc).filter((v) => /\bsecrets\b/.test(v)), []);
check('no job inherits secrets', jobs.filter((job) => job.secrets !== undefined).length, 0);
check('every action is pinned to a full commit',
  steps.filter((s) => typeof s.uses === 'string' && !/@[0-9a-f]{40}$/.test(s.uses))
    .map((s) => s.uses), []);
check('no expression is interpolated into a shell script',
  steps.filter((s) => typeof s.run === 'string' && s.run.includes('${{'))
    .map((s) => s.name || '(unnamed step)'), []);

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

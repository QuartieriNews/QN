'use strict';

/**
 * Executable acceptance for the workflow files themselves (Issue #7, acceptance 10).
 *
 * That criterion — that privileged logic never executes pull-request-supplied code or
 * secrets in its trusted context — is a static property of the YAML, not a runtime
 * one. A unit test of the gate cannot establish it, so it is asserted here by reading
 * the workflow definitions. Offline and dependency-free: this parses text, it does not
 * run a workflow.
 */

const fs = require('fs');
const path = require('path');

const WORKFLOWS = path.join(__dirname, '..', '.github', 'workflows');

let checks = 0;
let failed = 0;

function ok(name, condition) {
  checks += 1;
  if (condition) console.log(`  ok   ${name}`);
  else { failed += 1; console.log(`  FAIL ${name}`); }
}

const files = fs.existsSync(WORKFLOWS)
  ? fs.readdirSync(WORKFLOWS).filter((f) => /\.ya?ml$/.test(f))
  : [];

ok('at least one workflow exists to check', files.length > 0);

for (const file of files) {
  const text = fs.readFileSync(path.join(WORKFLOWS, file), 'utf8');
  const code = text.split('\n').filter((l) => !/^\s*#/.test(l)).join('\n');

  // `pull_request_target` runs with a write-capable token in the base repository's
  // context. Nothing here needs it, and it is the single sharpest edge in a public
  // repository.
  ok(`${file}: does not use pull_request_target`, !/pull_request_target/.test(code));

  // A workflow that checks out PR code must not also hold write.
  ok(`${file}: declares permissions`, /^permissions:/m.test(code));
  ok(`${file}: grants no write permission`, !/:\s*write\b/.test(code));

  ok(`${file}: does not reference secrets`, !/\bsecrets\./.test(code));

  // Untrusted text — a title, a body, a branch name — interpolated into a shell is
  // command injection. Values reach `run:` through `env:` instead.
  const runBlocks = code.split(/^\s*(?:-\s*)?(?:name:.*\n\s*)?run:\s*\|?/m).slice(1);
  const injected = runBlocks.filter((b) => /\$\{\{\s*github\.event\./.test(b.split(/^\s*-\s/m)[0]));
  ok(`${file}: no github.event value is interpolated into a run block`, injected.length === 0);

  // The merge-ref trap: checking out a pull request must name the head explicitly.
  if (/actions\/checkout/.test(code)) {
    // The merge-ref trap: a checkout that names no ref takes the event's default, which
    // for a pull request is a synthetic merge commit that attests nothing about H.
    ok(`${file}: checkout names a commit explicitly`,
       /ref:\s*\$\{\{\s*github\.(sha|event\.pull_request\.head\.sha)/.test(code));
    ok(`${file}: checkout does not persist credentials`,
       /persist-credentials:\s*false/.test(code));
  }
}

console.log('');
if (failed > 0) {
  console.log(`FAILED (${failed} of ${checks} checks)`);
  process.exit(1);
}
console.log(`ALL PASS (${checks} checks)`);

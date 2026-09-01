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

/**
 * Contexts whose value cannot be influenced by a pull request, and which are therefore
 * safe to interpolate into a shell. Everything else is refused rather than enumerated
 * as dangerous: a branch name, a title, a body and a label are all attacker-chosen, and
 * an allowlist cannot be defeated by finding a spelling the denylist forgot.
 */
const IMMUTABLE_CONTEXTS = [
  'github.sha', 'github.repository', 'github.repository_owner', 'github.run_id',
  'github.run_number', 'github.run_attempt', 'github.job', 'github.workflow',
  'github.event_name', 'github.api_url', 'github.server_url', 'github.workspace',
  'github.action', 'github.action_path',
];
// `github.token` is a credential, not an immutable value: interpolating it into a shell
// exposes the job's own token and defeats the workflow's stated "no secrets" property,
// so it is classified alongside `secrets.*` rather than allowed.

let checks = 0;
let failed = 0;

function ok(name, condition) {
  checks += 1;
  if (condition) console.log(`  ok   ${name}`);
  else { failed += 1; console.log(`  FAIL ${name}`); }
}

/**
 * Every `run:` scalar in a workflow, inline or block. Splitting the file on the token
 * would fold neighbouring steps together; indentation is what actually delimits a block
 * scalar, so it is what this follows.
 */
function runBlocks(text) {
  const lines = text.split('\n');
  const blocks = [];
  for (let i = 0; i < lines.length; i += 1) {
    // Valid YAML spells the key several ways: quoted, and with space before the colon.
    // Recognising only the bare form left `- "run": ...` invisible to every assertion.
    const m = lines[i].match(/^(\s*)(?:-\s*)?["']?run["']?\s*:\s*(.*)$/);
    if (!m) continue;
    const indent = m[1].length;
    const inline = m[2].trim();
    if (inline !== '' && !/^[|>][-+]?$/.test(inline)) {
      blocks.push(inline);
      continue;
    }
    const body = [];
    for (let j = i + 1; j < lines.length; j += 1) {
      if (lines[j].trim() === '') { body.push(''); continue; }
      const lead = lines[j].match(/^(\s*)/)[1].length;
      if (lead <= indent) break;
      body.push(lines[j]);
    }
    blocks.push(body.join('\n'));
  }
  return blocks;
}

/**
 * Every place a `run` key appears, however it is spelled — block, quoted, spaced,
 * or inside a flow mapping. Counting them independently of the extractor is what makes
 * an unparsed shape fail rather than pass: a spelling the extractor cannot read is
 * refused, instead of being silently exempt from every assertion below.
 */
function runKeyOccurrences(text) {
  return [...text.matchAll(/(?:^|[\s{,])["']?run["']?\s*:/gm)].length;
}

/** Every `${{ ... }}` expression in a fragment, with its inner text. */
function expressions(fragment) {
  return [...fragment.matchAll(/\$\{\{([^}]*)\}\}/g)].map((m) => m[1].trim());
}

function referencesSecrets(text) {
  // Both spellings of the same access — `secrets.NAME` and `secrets['NAME']` — and the
  // job credential, which is a secret whatever its permissions currently are.
  return /\bsecrets\s*(\.|\[)/.test(text) || /\bgithub\s*\.\s*token\b/.test(text) ||
         /\bgithub\s*\[\s*['\"]token['\"]\s*\]/.test(text);
}

/** Every `context.path` reference inside one expression, not merely its first. */
function contextsIn(expression) {
  return [...String(expression).matchAll(/\b(github|secrets|env|inputs|needs|vars|steps|job|runner|matrix)((?:\s*\.\s*[A-Za-z0-9_-]+|\s*\[[^\]]*\])*)/g)]
    .map((m) => (m[1] + m[2]).replace(/\s+/g, ''));
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

  ok(`${file}: declares permissions`, /^permissions:/m.test(code));
  // Quoted scalars are valid YAML: `contents: "write"` and `permissions: "write-all"`
  // both grant writes and both evaded an unquoted-only pattern.
  const unquoted = code.replace(/["']([^"'\n]*)["']/g, '$1');
  ok(`${file}: grants no write permission`, !/:\s*write(-all)?\b/.test(unquoted));
  ok(`${file}: does not reference secrets`, !referencesSecrets(code));

  // Untrusted text — a title, a body, a branch name — interpolated into a shell is
  // command injection. Values reach `run:` through `env:` instead, so a run block may
  // name only contexts a pull request cannot influence.
  // Every context an expression names must be immutable, not merely the one it starts
  // with: `${{ github.sha && github.head_ref }}` begins safely and ends attacker-chosen.
  const offending = [];
  for (const block of runBlocks(code)) {
    for (const expr of expressions(block)) {
      const refs = contextsIn(expr);
      if (refs.length === 0) { offending.push(expr); continue; }
      for (const ref of refs) {
        if (!IMMUTABLE_CONTEXTS.some((c) => ref === c || ref.startsWith(`${c}.`))) {
          offending.push(`${expr} (via ${ref})`);
        }
      }
    }
  }
  ok(`${file}: no mutable context is interpolated into a run block`, offending.length === 0);

  // Refuse what cannot be parsed. Every previous fix here added one more spelling to a
  // regex — quoted keys, then spaced colons, then flow mappings — and the next shape
  // would have passed unread. A run key the extractor did not capture fails instead.
  ok(`${file}: every run block was actually read`,
     runBlocks(code).length === runKeyOccurrences(code));

  // The merge-ref trap: a checkout that names no ref takes the event's default, which
  // for a pull request is a synthetic merge commit that attests nothing about H.
  if (/actions\/checkout/.test(code)) {
    // Naming *a* sha is not enough: `github.event.pull_request.base.sha` would test the
    // base while satisfying a looser assertion. Only head-bearing expressions qualify.
    const checkoutRef = (code.match(/ref:\s*(\$\{\{[^}]*\}\})/) || [])[1] || '';
    const expected = (code.match(/EXPECTED_SHA:\s*(\$\{\{[^}]*\}\})/) || [])[1] || '';
    const namesHead = /github\.sha|merge_group\.head_sha|pull_request\.head\.sha/.test(checkoutRef) &&
                      !/\bbase\.sha\b/.test(checkoutRef);
    ok(`${file}: checkout names the head under test`, namesHead);
    ok(`${file}: the verified SHA is the one checked out`,
       expected !== '' && expected === checkoutRef);
    ok(`${file}: checkout does not persist credentials`,
       /persist-credentials:\s*false/.test(code));
  }

  // A merge queue evaluates a commit of its own. Without this trigger the queued commit
  // never receives the required check, so the queue can never satisfy it
  // (docs/autonomy/IDENTITY_AND_PERMISSIONS.md §3).
  if (/^on:/m.test(code)) {
    ok(`${file}: runs for merge-queue commits`, /^\s*merge_group:/m.test(code));
  }
}

// The extractor itself, since every assertion above rests on it seeing whole blocks.
{
  const sample = [
    'jobs:', '  a:', '    steps:', '      - run: echo one',
    '      - name: two', '        run: |', '          echo ${{ github.head_ref }}',
    '      - "run": echo ${{ github.event.pull_request.title }}',
    '      - run : echo ${{ github.actor }}',
    '      - uses: actions/checkout@v4',
  ].join('\n');
  const blocks = runBlocks(sample);
  ok('the run extractor finds an inline block', blocks.some((b) => b.includes('echo one')));
  ok('the run extractor finds a literal block', blocks.some((b) => b.includes('github.head_ref')));
  ok('the run extractor stops at the next step',
     !blocks.some((b) => b.includes('actions/checkout')));
  ok('the run extractor sees a quoted key',
     blocks.some((b) => b.includes('pull_request.title')));
  ok('the run extractor sees a spaced colon', blocks.some((b) => b.includes('github.actor')));
  ok('a mutable context in a run block is detected',
     expressions(blocks.join('\n')).includes('github.head_ref'));
}
ok('bracket-form secret access is detected', referencesSecrets("echo ${{ secrets['TOKEN'] }}"));
ok('dot-form secret access is detected', referencesSecrets('echo ${{ secrets.TOKEN }}'));
ok('the job credential counts as a secret', referencesSecrets('echo ${{ github.token }}'));
ok('bracket-form job credential counts as a secret', referencesSecrets("echo ${{ github['token'] }}"));
ok('a compound expression exposes every context it names',
   contextsIn('github.sha && github.head_ref').includes('github.head_ref'));
ok('a compound expression still reports the safe one too',
   contextsIn('github.sha && github.head_ref').includes('github.sha'));
{
  // A flow-style step is valid YAML the line extractor cannot read; the counter must
  // notice rather than let it through unexamined.
  const flow = 'jobs:\n  a:\n    steps:\n      - { run: "echo ${{ github.head_ref }}" }';
  ok('an unparsed flow-style run key is detected as unread',
     runBlocks(flow).length !== runKeyOccurrences(flow));
}
ok('a quoted write permission is detected',
   /:\s*write\b/.test('contents: "write"'.replace(/["']([^"'\n]*)["']/g, '$1')));
ok('write-all is detected',
   /:\s*write(-all)?\b/.test('permissions: "write-all"'.replace(/["']([^"'\n]*)["']/g, '$1')));

console.log('');
if (failed > 0) {
  console.log(`FAILED (${failed} of ${checks} checks)`);
  process.exit(1);
}
console.log(`ALL PASS (${checks} checks)`);

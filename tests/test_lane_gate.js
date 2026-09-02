/**
 * test_lane_gate.js — executable acceptance for autonomy/lane_gate.js.
 *
 * Two layers, tested separately: the pure classifier over literal file facts, and
 * the parsers that turn `git diff -z` output into those facts. The parser cases are
 * verbatim output captured from git for a rename, a binary file, a symlink and a
 * mode change — the four shapes a hand-rolled reader gets wrong.
 *
 * Covers DEC-012: lanes are owner-attention levels, RED wins over everything, an
 * absent fact is never a false one, and no lane authorises a merge.
 *
 * Run:  node tests/test_lane_gate.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const gate = require(path.join(__dirname, '..', 'autonomy', 'lane_gate.js'));
const { classify, parseRawZ, parseNumstatZ, mergeFacts, LANE } = gate;

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

/** A plain modified text file; overrides express exactly what a case is about. */
function file(overrides) {
  return Object.assign({
    status: 'M',
    path: 'docs/note.md',
    previousPath: null,
    srcMode: '100644',
    dstMode: '100644',
    additions: 1,
    deletions: 0,
    binary: false,
  }, overrides);
}

function facts(files, overrides) {
  return Object.assign({
    files,
    baseTopLevel: ['docs', 'reviews', 'decisions', 'autonomy', 'tests', 'AGENTS.md', 'README.md'],
    headRepoId: '1',
    baseRepoId: '1',
  }, overrides);
}

const lane = (files, overrides) => classify(facts(files, overrides)).lane;
const rules = (files, overrides) => classify(facts(files, overrides)).reasons.map((r) => r.rule);

console.log('The three lanes on ordinary changes');
check('docs edit is GREEN', lane([file({})]), LANE.GREEN);
check('reviews report is GREEN', lane([file({ path: 'reviews/2026-01-01-x.md', status: 'A' })]), LANE.GREEN);
check('decision entry is RED', lane([file({ path: 'decisions/DEC-013-x.md', status: 'A' })]), LANE.RED);
check('gate itself is RED', lane([file({ path: 'autonomy/lane_gate.js' })]), LANE.RED);
check('gate tests are RED', lane([file({ path: 'tests/test_lane_gate.js' })]), LANE.RED);
check('workflow is RED', lane([file({ path: '.github/workflows/checks.yml' })]), LANE.RED);
check('policy is RED', lane([file({ path: 'docs/autonomy/LANE_POLICY.md' })]), LANE.RED);
check('agent instructions in docs are RED', lane([file({ path: 'docs/START_HERE.md' })]), LANE.RED);
check('council brief is RED', lane([file({ path: 'docs/strategic-council/PROJECT_BRIEF.md' })]), LANE.RED);
check('reviewer mandate is RED', lane([file({ path: 'reviews/REVIEW_MANDATE_CODE.md' })]), LANE.RED);
check('production code is RED', lane([file({ path: 'code-nodes/parse-duration.js' })]), LANE.RED);
check('outside every green prefix is AMBER', lane([file({ path: 'README.md' })]), LANE.AMBER);

console.log('');
console.log('RED wins, and says why');
check('protected surface names its rule',
  rules([file({ path: 'decisions/DEC-013-x.md' })]), ['PROTECTED_SURFACE']);
check('one RED file makes a whole GREEN batch RED',
  lane([file({}), file({ path: 'AGENTS.md' })]), LANE.RED);
check('protected match is case-folded',
  lane([file({ path: 'Docs/Autonomy/LANE_POLICY.md' })]), LANE.RED);
check('control file is protected at any depth',
  rules([file({ path: 'docs/sub/package.json' })]), ['CONTROL_FILE']);
check('control file is case-folded',
  lane([file({ path: 'docs/Claude.md' })]), LANE.RED);

console.log('');
console.log('A rename is a claim about two paths (both are checked)');
check('renaming out of a protected surface is RED',
  lane([file({ status: 'R', path: 'docs/x.md', previousPath: 'decisions/DEC-001-x.md' })]), LANE.RED);
check('renaming into a protected surface is RED',
  lane([file({ status: 'R', path: 'decisions/DEC-001-x.md', previousPath: 'docs/x.md' })]), LANE.RED);
check('an ordinary rename inside docs is only AMBER',
  rules([file({ status: 'R', path: 'docs/b.md', previousPath: 'docs/a.md' })]),
  ['STATUS_NOT_ADD_OR_MODIFY']);

console.log('');
console.log('New top-level paths are RED, and novelty is case-sensitive');
check('a new top-level directory is RED',
  rules([file({ path: 'scripts/deploy.sh', status: 'A' })]), ['NEW_TOP_LEVEL']);
check('an existing top-level directory is not new',
  lane([file({ path: 'docs/x.md', status: 'A' })]), LANE.GREEN);
check('a case variant of an existing top level is new',
  rules([file({ path: 'Docs/x.md', status: 'A' })]), ['NEW_TOP_LEVEL']);

console.log('');
console.log('Unusual file kinds are RED');
check('symlink is RED', rules([file({ status: 'A', srcMode: '000000', dstMode: '120000' })]),
  ['UNUSUAL_FILE_KIND']);
check('submodule is RED', rules([file({ status: 'A', srcMode: '000000', dstMode: '160000' })]),
  ['UNUSUAL_FILE_KIND']);
check('gaining the executable bit is RED',
  rules([file({ srcMode: '100644', dstMode: '100755' })]), ['UNUSUAL_FILE_KIND']);
check('deleting an ordinary file is not an unusual kind',
  rules([file({ status: 'D', srcMode: '100644', dstMode: '000000' })]),
  ['STATUS_NOT_ADD_OR_MODIFY']);

console.log('');
console.log('A fork is two repository identities that differ, not one that is a fork');
check('different repository identities are RED',
  rules([file({})], { headRepoId: '2' }), ['FORK']);
check('the same identity is not a fork', lane([file({})], { headRepoId: '1' }), LANE.GREEN);
check('a missing head identity is UNCLASSIFIABLE, not "not a fork"',
  rules([file({})], { headRepoId: undefined }), ['UNCLASSIFIABLE']);
check('an empty base identity is UNCLASSIFIABLE',
  rules([file({})], { baseRepoId: '' }), ['UNCLASSIFIABLE']);
check('the reason names which identity was unstated',
  classify(facts([file({})], { baseRepoId: undefined })).reasons[0].detail.includes('baseRepoId'),
  true);
check('FORK is reported alongside the other rules that fired',
  rules([file({ path: 'decisions/DEC-013-x.md' })], { headRepoId: '2' }),
  ['PROTECTED_SURFACE', 'FORK']);

console.log('');
console.log('GREEN is a conjunction, and every failure is named');
check('too many files is AMBER',
  rules(Array.from({ length: gate.GREEN_LIMITS.maxFiles + 1 },
    (_, i) => file({ path: `docs/f${i}.md` }))), ['TOO_MANY_FILES']);
check('too many lines is AMBER',
  rules([file({ additions: gate.GREEN_LIMITS.maxLines, deletions: 1 })]), ['TOO_MANY_LINES']);
check('exactly at the line cap is still GREEN',
  lane([file({ additions: gate.GREEN_LIMITS.maxLines, deletions: 0 })]), LANE.GREEN);
check('deletions count towards the cap as much as additions',
  rules([file({ additions: 0, deletions: gate.GREEN_LIMITS.maxLines + 1 })]), ['TOO_MANY_LINES']);
check('a binary file is never GREEN', rules([file({ binary: true })]), ['BINARY']);
check('a binary file reported as zero lines is still not GREEN',
  rules([file({ binary: true, additions: 0, deletions: 0 })]), ['BINARY']);
check('several green failures are all reported',
  rules([file({ path: 'README.md', status: 'D', srcMode: '100644', dstMode: '000000' })]),
  ['OUTSIDE_GREEN_PREFIXES', 'STATUS_NOT_ADD_OR_MODIFY']);

console.log('');
console.log('An absent fact is never a false one (DEC-012)');
check('missing files list is RED', classify({ baseTopLevel: [] }).lane, LANE.RED);
check('missing base inventory is RED', classify({ files: [] }).lane, LANE.RED);
check('facts of the wrong type are RED', classify({ files: 'docs/x.md', baseTopLevel: [] }).lane, LANE.RED);
check('an empty diff is not RED', lane([]), LANE.GREEN);
check('a path with a parent segment is unclassifiable',
  rules([file({ path: 'docs/../autonomy/lane_gate.js' })]), ['UNCLASSIFIABLE']);
check('an absolute path is unclassifiable', rules([file({ path: '/etc/passwd' })]), ['UNCLASSIFIABLE']);
check('an empty path is unclassifiable', rules([file({ path: '' })]), ['UNCLASSIFIABLE']);

console.log('');
console.log('Cycle 1: what the head must not be able to tell the gate');
check('CODEOWNERS in docs/ is a control file, not a GREEN docs change',
  rules([file({ path: 'docs/CODEOWNERS', status: 'A' })]), ['CONTROL_FILE']);
check('CODEOWNERS at the root is a control file',
  rules([file({ path: 'CODEOWNERS', status: 'A' })]), ['CONTROL_FILE', 'NEW_TOP_LEVEL']);
check('CODEOWNERS under .github/ is caught by the surface and the filename',
  lane([file({ path: '.github/CODEOWNERS', status: 'A' })]), LANE.RED);
check('a .gitattributes is a control file wherever it appears',
  rules([file({ path: 'docs/.gitattributes', status: 'A' })]), ['CONTROL_FILE']);
check('the attack that reached GREEN now reaches RED',
  lane([file({ path: 'docs/.gitattributes', status: 'A' }),
        file({ path: 'docs/payload.md', status: 'A' })]), LANE.RED);
{
  // Every field the schema declares, deleted one at a time.
  const required = ['status', 'path', 'srcMode', 'dstMode', 'additions', 'deletions', 'binary'];
  for (const field of required) {
    const broken = file({});
    delete broken[field];
    check(`an omitted \`${field}\` is UNCLASSIFIABLE, not GREEN`,
      rules([broken]), ['UNCLASSIFIABLE']);
  }
  const mistyped = file({ additions: '3' });
  check('a count that is a string is UNCLASSIFIABLE', rules([mistyped]), ['UNCLASSIFIABLE']);
  check('an omitted repository identity is UNCLASSIFIABLE, not false',
    classify({ files: [file({})], baseTopLevel: ['docs'], baseRepoId: '1' }).reasons
      .map((r) => r.rule), ['UNCLASSIFIABLE']);
  check('the reason names which fact was unstated',
    classify(facts([(() => { const f = file({}); delete f.binary; return f; })()]))
      .reasons[0].detail.includes('files[0].binary'), true);
}
check('a pathname cannot close its own code span or open a row',
  gate.displayPath('docs/a`b|c\nd.md'), 'docs/a\\x60b\\x7cc\\x0ad.md');
check('a backslash in a pathname is escaped before anything else',
  gate.displayPath('docs/a\\b.md'), 'docs/a\\\\b.md');

console.log('');
console.log('Cycle 2: the rendered summary, not just the string that feeds it');
{
  // A backslash is literal inside a code span, so an escaped backtick still closes it.
  // The assertion is on the row a reader sees, not on the value that feeds it.
  const nasty = 'docs/a`b|c\nd.md';
  const res = classify(facts([file({ status: 'A', path: nasty, srcMode: '000000' })]));
  const rendered = gate.renderMarkdown(res);
  const rows = rendered.split('\n').filter((l) => l.startsWith('| A |'));
  check('the file row is one row', rows.length, 1);
  check('the row has exactly four cells', rows[0].split('|').length - 2, 4);
  check('the path cell opens and closes exactly one code span',
    (rows[0].split('|')[2].match(/`/g) || []).length, 2);
  check('no path puts a raw newline into the summary', rendered.includes(nasty), false);
}

console.log('');
console.log('Cycle 2: a rename must state the path it came from');
check('an R record without its source is UNCLASSIFIABLE',
  rules([file({ status: 'R', path: 'docs/b.md', previousPath: null })]), ['UNCLASSIFIABLE']);
check('an R record with an empty source is UNCLASSIFIABLE',
  rules([file({ status: 'R', path: 'docs/b.md', previousPath: '' })]), ['UNCLASSIFIABLE']);
check('a rename cannot lose a protected source and fall to AMBER',
  lane([file({ status: 'R', path: 'docs/b.md', previousPath: 'decisions/DEC-001-x.md' })]), LANE.RED);
check('a status that carries no source must not state one',
  rules([file({ status: 'M', previousPath: 'docs/other.md' })]), ['UNCLASSIFIABLE']);
check('a C record is held to the same rule as an R record',
  rules([file({ status: 'C', path: 'docs/b.md', previousPath: null })]), ['UNCLASSIFIABLE']);

console.log('');
console.log('Cycle 2: a diff that could not be read still reports what was known');
{
  const cross = gate.unclassifiable('could not read the diff: boom',
    { headRepoId: '2', baseRepoId: '1' });
  check('the lane is RED', cross.lane, LANE.RED);
  check('the rule that fired is kept alongside the failure',
    cross.reasons.map((r) => r.rule), ['UNCLASSIFIABLE', 'FORK']);
  check('provenance that was stated is carried through',
    [cross.isFork, cross.headRepoId, cross.baseRepoId], [true, '2', '1']);
  const same = gate.unclassifiable('boom', { headRepoId: '1', baseRepoId: '1' });
  check('and a same-repository failure does not claim a fork',
    [same.reasons.map((r) => r.rule), same.isFork], [['UNCLASSIFIABLE'], false]);
  const unknown = gate.unclassifiable('boom', {});
  check('an unknown provenance is not reported as a fork',
    [unknown.isFork, unknown.headRepoId], [false, null]);
}

console.log('');
console.log('Verification phase: a bad record must not break the result that reports it');
check('a null file record is UNCLASSIFIABLE, not an exception', (() => {
  try { return rules([null]); } catch (e) { return `threw: ${e.constructor.name}`; }
})(), ['UNCLASSIFIABLE']);
check('an undefined file record is UNCLASSIFIABLE, not an exception', (() => {
  try { return rules([undefined]); } catch (e) { return `threw: ${e.constructor.name}`; }
})(), ['UNCLASSIFIABLE']);
check('a record that is not an object at all is UNCLASSIFIABLE',
  rules(['docs/x.md']), ['UNCLASSIFIABLE']);
{
  const res = classify(facts([null, file({})]));
  check('the summary counts what was supplied and dereferences only what it can',
    res.summary, { files: 2, additions: 1, deletions: 0 });
  check('the malformed record is reported as supplied, not hidden', res.files[0], null);
}

console.log('');
console.log('Verification phase: a flag that takes a value has no truthy default');
{
  const parse = (argv) => Object.fromEntries(gate.parseArgs(argv));
  check('an empty value stays empty, and does not become "true"',
    parse(['--base-repo-id', '', '--head-repo-id', '']),
    { 'base-repo-id': '', 'head-repo-id': '' });
  check('a flag followed by another flag has no value',
    parse(['--base-repo-id', '--head-repo-id', '7']),
    { 'base-repo-id': null, 'head-repo-id': '7' });
  check('a trailing flag has no value', parse(['--head-repo-id']), { 'head-repo-id': null });
  check('an ordinary value is unchanged',
    parse(['--base', 'abc', '--head', 'def']), { base: 'abc', head: 'def' });
  check('an empty identity is UNCLASSIFIABLE once classified',
    rules([file({})], { headRepoId: '', baseRepoId: '' }), ['UNCLASSIFIABLE']);
  check('a null identity is UNCLASSIFIABLE once classified',
    rules([file({})], { headRepoId: null }), ['UNCLASSIFIABLE']);
}

console.log('');
console.log('Verification cycle 2: the error path must render, not only classify');
{
  // classify already refuses these; the summary they produce must also survive being
  // rendered, because the rendered table is what the owner actually reads.
  const render = (record) => {
    const res = classify(facts([record]));
    try {
      return [res.lane, gate.renderMarkdown(res).split('\n').filter((l) => l.startsWith('| ')).pop()];
    } catch (e) {
      return [res.lane, `threw: ${e.constructor.name}`];
    }
  };
  check('a null record renders as unreadable',
    render(null), [LANE.RED, '| — | _unreadable record_ | — | — |']);
  check('an undefined record renders as unreadable',
    render(undefined), [LANE.RED, '| — | _unreadable record_ | — | — |']);
  check('a record that is a string renders as unreadable',
    render('docs/x.md'), [LANE.RED, '| — | _unreadable record_ | — | — |']);
  check('a record missing its fields renders them as absent, not as "undefined"',
    render({ status: 'A' }), [LANE.RED, '| A | `—` | —→— | +0 −0 |']);
  check('a valid record is unchanged by the guard',
    render(file({ path: 'docs/a.md', additions: 2, deletions: 1 })),
    [LANE.GREEN, '| M | `docs/a.md` | 100644→100644 | +2 −1 |']);
  check('the malformed record is still in the JSON as supplied',
    classify(facts([null])).files[0], null);
}

console.log('');
console.log('No lane authorises a merge, and AUTO-GREEN has no categories');
{
  const green = classify(facts([file({})]));
  check('AUTO-GREEN is disabled', green.autoGreen, { enabled: false, categories: [] });
  check('the result carries no merge authorisation',
    Object.keys(green).some((k) => /merge/i.test(k)), false);
  check('the shipped AUTO-GREEN category list is empty', gate.AUTO_GREEN_CATEGORIES.length, 0);
}
check('exported tables cannot be emptied through the public API', (() => {
  try { gate.PROTECTED_SURFACES.splice(0); } catch (e) { /* frozen */ }
  return lane([file({ path: 'decisions/DEC-013-x.md' })]);
})(), LANE.RED);

console.log('');
console.log('The facts contract DEC-012 requires of the output');
{
  const out = classify(facts([file({ status: 'R', path: 'docs/b.md', previousPath: 'docs/a.md' })]));
  check('output carries the gate version', typeof out.gateVersion, 'string');
  check('output carries the summary',
    out.summary, { files: 1, additions: 1, deletions: 0 });
  check('output carries every field a later policy needs',
    Object.keys(out.files[0]).sort(),
    ['additions', 'binary', 'deletions', 'dstMode', 'path', 'previousPath', 'srcMode', 'status']);
  check('output carries fork provenance and new top-level paths',
    [out.isFork, out.headRepoId, out.baseRepoId, Array.isArray(out.newTopLevel)],
    [false, '1', '1', true]);
}

console.log('');
console.log('Parsers, on output captured verbatim from git');
{
  // git diff --raw -z: rename, binary add, symlink add, mode change.
  const raw = ':000000 100644 0000000 0f49c4a A\0docs/blob.md\0'
    + ':000000 120000 0000000 8fdda3d A\0docs/link.md\0'
    + ':100644 100644 587be6b 587be6b R100\0docs/old-name.md\0docs/new-name.md\0'
    + ':100644 100755 b68fde2 b68fde2 M\0reviews/r.md\0';
  const parsed = parseRawZ(raw);
  check('four records parsed', parsed.length, 4);
  check('a rename resolves both of its paths',
    [parsed[2].status, parsed[2].previousPath, parsed[2].path],
    ['R', 'docs/old-name.md', 'docs/new-name.md']);
  check('a rename does not consume the record after it', parsed[3].path, 'reviews/r.md');
  check('symlink mode survives parsing', parsed[1].dstMode, '120000');
  check('a mode change survives parsing', [parsed[3].srcMode, parsed[3].dstMode], ['100644', '100755']);
  check('an unexpected record throws rather than being skipped', (() => {
    try { parseRawZ('not a raw record\0'); return 'no throw'; } catch (e) { return 'threw'; }
  })(), 'threw');

  // git diff --numstat -z: "-" marks binary; renames put the paths in later fields.
  const numstat = '-\t-\tdocs/blob.md\0' + '1\t0\tdocs/link.md\0'
    + '0\t0\t\0docs/old-name.md\0docs/new-name.md\0' + '0\t0\treviews/r.md\0';
  const counts = parseNumstatZ(numstat);
  check('four count records parsed', counts.length, 4);
  check('a binary file is flagged, not counted as zero',
    [counts[0].binary, counts[0].additions, counts[0].deletions], [true, 0, 0]);
  check('a rename takes its destination path', [counts[2].path, counts[2].binary],
    ['docs/new-name.md', false]);
  check('a text file keeps its counts', [counts[1].additions, counts[1].deletions], [1, 0]);

  // A tab is a valid character in a Git pathname and `-z` does not quote it.
  const tabbed = parseNumstatZ('1\t0\tdocs/a\tb.md\0');
  check('a tab inside a pathname is not a field separator',
    [tabbed.length, tabbed[0].path, tabbed[0].additions], [1, 'docs/a\tb.md', 1]);
  check('a record with too few tabs throws rather than being read short', (() => {
    try { parseNumstatZ('1\0'); return 'no throw'; } catch (e) { return 'threw'; }
  })(), 'threw');

  const merged = mergeFacts(parsed, counts);
  check('merging pairs every record', merged.length, 4);
  check('the binary flag reaches the classifier', merged[0].binary, true);
  check('these four real shapes classify RED',
    classify(facts(merged)).reasons.map((r) => r.rule), ['UNUSUAL_FILE_KIND']);
  check('a missing count record throws rather than defaulting', (() => {
    try { mergeFacts(parsed, counts.slice(1)); return 'no throw'; } catch (e) { return 'threw'; }
  })(), 'threw');
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

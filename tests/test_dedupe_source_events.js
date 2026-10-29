/**
 * test_dedupe_source_events.js — executable acceptance for
 * code-nodes/dedupe-source-events.js (Spec v2.5 Phase 1.3; case T25). Covers
 * BOTH contexts of the one-source file, and checks that the inlined
 * hashed-field count agrees with compute-source-hash.js on the same inputs.
 *
 * Run:  node tests/test_dedupe_source_events.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const { dedupeSourceEvents, normalizeSourceEventId, countNonEmptyHashedFields } =
  require(path.join(__dirname, '..', 'code-nodes', 'dedupe-source-events.js'));
const hashNode = require(path.join(__dirname, '..', 'code-nodes', 'compute-source-hash.js'));

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

function ev(id, fields) {
  return Object.assign({ source_event_id: id, event_name: 'E' + id, location: {}, organizer: {} }, fields || {});
}
const ids = (r) => r.items.map((i) => i.source_event_id);

console.log('normalizeSourceEventId');
check('trimmed string', normalizeSourceEventId(' 123 '), '123');
check('number -> string', normalizeSourceEventId(123), '123');
check('blank -> null', normalizeSourceEventId('   '), null);
check('null/undefined -> null', [normalizeSourceEventId(null), normalizeSourceEventId(undefined)], [null, null]);
check('object -> null', normalizeSourceEventId({ id: 1 }), null);

console.log('DEC-027 — what a valid source_event_id is');
check('DEC-027 alphanumeric string kept', normalizeSourceEventId(' ev-12a '), 'ev-12a');
check('DEC-027 boolean -> null', [normalizeSourceEventId(false), normalizeSourceEventId(true)], [null, null]);
check('DEC-027 non-finite number -> null', [normalizeSourceEventId(Infinity), normalizeSourceEventId(-Infinity), normalizeSourceEventId(NaN)], [null, null, null]);
check('DEC-027 non-integer number -> null', normalizeSourceEventId(1.5), null);
check('DEC-027 integer beyond the safe range -> null', normalizeSourceEventId(2 ** 53), null);
check('DEC-027 array -> null', normalizeSourceEventId(['1']), null);
{
  const r = dedupeSourceEvents([ev(false), ev(Infinity), ev(1.5), ev('8')]);
  check('DEC-027 invalid ids are counted as rejected, not deduplicated', r.report, { returned_by_source: 4, rejected_missing_source_event_id: 3, duplicate_source_ids_removed: 0, kept: 1 });
}

console.log('T25 — same source_event_id twice in the dataset');
{
  const r = dedupeSourceEvents([ev('1'), ev('2'), ev('1'), ev('3')]);
  check('one item per id', ids(r), ['1', '2', '3']);
  check('duplicate counted once', r.report.duplicate_source_ids_removed, 1);
  check('report totals', r.report, { returned_by_source: 4, rejected_missing_source_event_id: 0, duplicate_source_ids_removed: 1, kept: 3 });
}
{
  const r = dedupeSourceEvents([ev('7'), ev(' 7 '), ev(7)]);
  check('ids normalized before comparison (" 7 ", 7, "7" are one)', r.items.map((i) => normalizeSourceEventId(i.source_event_id)), ['7']);
  check('the kept payload is the original (last on tie: the number 7)', r.items[0].source_event_id, 7);
  check('two duplicates removed', r.report.duplicate_source_ids_removed, 2);
}

console.log('Tie-break — keep the more complete record');
{
  const partial = ev('9', { source_description: '' });
  const complete = ev('9', { source_description: 'Testo', location: { name: 'Posto', city: 'Roma' } });
  const r1 = dedupeSourceEvents([partial, complete]);
  check('complete after partial -> complete kept', r1.items[0].source_description, 'Testo');
  const r2 = dedupeSourceEvents([complete, partial]);
  check('complete before partial -> complete still kept', r2.items[0].source_description, 'Testo');
}
{
  const a = ev('5', { source_description: 'prima' });
  const b = ev('5', { source_description: 'ultima' });
  const r = dedupeSourceEvents([a, b]);
  check('equal completeness -> last occurrence kept', r.items[0].source_description, 'ultima');
}
{
  const a = ev('6', { source_description: '   ' });
  const b = ev('6', { source_description: 'x' });
  const r = dedupeSourceEvents([b, a]);
  check('whitespace-only does not count as a field (b wins despite order)', r.items[0].source_description, 'x');
}

console.log('Items without a valid source_event_id are rejected, never deduplicated');
{
  const r = dedupeSourceEvents([ev(null), ev(''), ev('  '), ev('1'), { event_name: 'no id' }]);
  check('kept only the valid one', ids(r), ['1']);
  check('rejected count', r.report.rejected_missing_source_event_id, 4);
  check('rejections are not duplicates', r.report.duplicate_source_ids_removed, 0);
}

console.log('Order and robustness');
check('kept order = first appearance of each id', ids(dedupeSourceEvents([ev('b'), ev('a'), ev('b'), ev('c'), ev('a')])), ['b', 'a', 'c']);
check('empty dataset', dedupeSourceEvents([]), { items: [], report: { returned_by_source: 0, rejected_missing_source_event_id: 0, duplicate_source_ids_removed: 0, kept: 0 } });
check('non-array input treated as empty', dedupeSourceEvents(null).report.returned_by_source, 0);
check('null entries are rejected, not thrown on', dedupeSourceEvents([null, ev('1')]).report.rejected_missing_source_event_id, 1);
check('kept items are the original objects (no copy, no mutation)', (() => { const x = ev('1'); return dedupeSourceEvents([x]).items[0] === x; })(), true);

console.log('Inlined hashed-field count agrees with compute-source-hash.js');
{
  const cases = [
    {},
    ev('1'),
    ev('2', { source_description: '  ', cost_raw: 0, booking_url_raw: false }),
    ev('3', { location: { latitude: 'n/a', longitude: '12.5', name: { x: 1 } }, end_at_utc: 'TBD' }),
    ev('4', { source_image_url: 'not a url', organizer: { name: ' ' }, location: { latitude: -0.0000001 } }),
    ev('5', { event_name: null, source_description: undefined, location: null }),
    ev('6', { location: { latitude: '   ', longitude: { a: 1 } } }), // PR #19 cycle 1: empty, not 0.000000
    ev('7', { location: { latitude: [12.5], longitude: ' 12.5 ' } }),
  ];
  for (const c of cases) {
    check(`agree on ${JSON.stringify(c).slice(0, 60)}`, countNonEmptyHashedFields(c), hashNode.countNonEmptyHashedFields(c));
  }
}

console.log('n8n adapter branch — exact committed file, stubbed $input (Run Once for All Items)');
const src = fs.readFileSync(path.join(__dirname, '..', 'code-nodes', 'dedupe-source-events.js'), 'utf8');
function runNode(jsons) {
  const logs = [];
  const fn = new Function('$input', 'console', src);
  const out = fn({ all: () => jsons.map((json) => ({ json })) }, { log: (m) => logs.push(m) });
  return { out, logs };
}
{
  const { out, logs } = runNode([ev('1'), ev('2', { source_description: 'a' }), ev('2', { source_description: 'ab', cost_raw: '5' }), ev('')]);
  check('adapter returns n8n items {json}', out.map((i) => i.json.source_event_id), ['1', '2']);
  check('adapter keeps the more complete duplicate', out[1].json.cost_raw, '5');
  check('adapter logs the report once', logs.length, 1);
  check('adapter log carries the counts', JSON.parse(logs[0].replace(/^dedupe-source-events /, '')),
    { returned_by_source: 4, rejected_missing_source_event_id: 1, duplicate_source_ids_removed: 1, kept: 2 });
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

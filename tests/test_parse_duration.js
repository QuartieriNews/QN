/**
 * test_parse_duration.js — executable acceptance for code-nodes/parse-duration.js.
 * Covers BOTH contexts of the one-source file: the CommonJS module branch and
 * the n8n adapter branch, evaluated from the exact committed file with stubbed
 * $input/$json (cycle-2 review, item 3). Overflow bounds per cycle-2, item 2.
 *
 * Covers spec v2.5 Phase 3.3 and acceptance case T39, the five measured source
 * shapes (SOURCE_DATA_FINDINGS), and the traps a lax parser fails: partial
 * matches inside decimals, leftover text, bare numbers, bare units.
 *
 * Run:  node tests/test_parse_duration.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const { parseDurationText, computeEventEnd } =
  require(path.join(__dirname, '..', 'code-nodes', 'parse-duration.js'));

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

console.log('parseDurationText — the five measured source shapes');
check('"5 days"',        parseDurationText('5 days'),        { status: 'parsed', minutes: 7200 });
check('"1 hr 30 min"',   parseDurationText('1 hr 30 min'),   { status: 'parsed', minutes: 90 });
check('"2 hrs"',         parseDurationText('2 hrs'),         { status: 'parsed', minutes: 120 });
check('"45 min"',        parseDurationText('45 min'),        { status: 'parsed', minutes: 45 });
check('"1 day"',         parseDurationText('1 day'),         { status: 'parsed', minutes: 1440 });

console.log('parseDurationText — unit variants and shape tolerance');
check('"1 hour"',        parseDurationText('1 hour'),        { status: 'parsed', minutes: 60 });
check('"2 hours"',       parseDurationText('2 hours'),       { status: 'parsed', minutes: 120 });
check('"90 minutes"',    parseDurationText('90 minutes'),    { status: 'parsed', minutes: 90 });
check('"3 mins"',        parseDurationText('3 mins'),        { status: 'parsed', minutes: 3 });
check('"45min" (no space)',      parseDurationText('45min'), { status: 'parsed', minutes: 45 });
check('"  2 hrs  " (padding)',   parseDurationText('  2 hrs  '), { status: 'parsed', minutes: 120 });
check('"1 HR 30 MIN" (case)',    parseDurationText('1 HR 30 MIN'), { status: 'parsed', minutes: 90 });
check('"1 day 2 hrs" (mixed sum)', parseDurationText('1 day 2 hrs'), { status: 'parsed', minutes: 1560 });
check('"0 min" (zero, literal)',   parseDurationText('0 min'), { status: 'parsed', minutes: 0 });

console.log('parseDurationText — missing vs unparseable (the asymmetry that matters)');
check('null',            parseDurationText(null),      { status: 'missing', minutes: null });
check('undefined',       parseDurationText(undefined), { status: 'missing', minutes: null });
check('"" (empty)',      parseDurationText(''),        { status: 'missing', minutes: null });
check('"   " (blank)',   parseDurationText('   '),     { status: 'missing', minutes: null });
check('"circa due ore" (T39)', parseDurationText('circa due ore'), { status: 'unparseable', minutes: null });
check('"1.5 hrs" (decimal must NOT half-match)', parseDurationText('1.5 hrs'), { status: 'unparseable', minutes: null });
check('"2 hrs approx" (leftover text)', parseDurationText('2 hrs approx'), { status: 'unparseable', minutes: null });
check('"about 2 hrs" (leading text)',   parseDurationText('about 2 hrs'), { status: 'unparseable', minutes: null });
check('"30" (bare number)',  parseDurationText('30'),   { status: 'unparseable', minutes: null });
check('"min" (bare unit)',   parseDurationText('min'),  { status: 'unparseable', minutes: null });
check('"2h" (unlisted unit)', parseDurationText('2h'),  { status: 'unparseable', minutes: null });
check('"due ore" (words)',   parseDurationText('due ore'), { status: 'unparseable', minutes: null });
check('non-string (number 90)', parseDurationText(90),  { status: 'unparseable', minutes: null });

console.log('computeEventEnd — the three T39 outcomes');
check('parseable -> exact end',
  computeEventEnd('2026-09-25T18:00:00Z', '1 hr 30 min'),
  { ok: true, end_at_utc: '2026-09-25T19:30:00.000Z', date_precision: 'exact',
    reject_reason: null, duration_minutes: 90, error: null });
check('missing -> start_only, NO reject',
  computeEventEnd('2026-09-25T18:00:00Z', null),
  { ok: true, end_at_utc: '2026-09-25T18:00:00.000Z', date_precision: 'start_only',
    reject_reason: null, duration_minutes: null, error: null });
check('unparseable present -> date_unparseable, counted',
  computeEventEnd('2026-09-25T18:00:00Z', 'circa due ore'),
  { ok: true, end_at_utc: '2026-09-25T18:00:00.000Z', date_precision: 'start_only',
    reject_reason: 'date_unparseable', duration_minutes: null, error: null });

console.log('computeEventEnd — UTC arithmetic across the Europe/Rome DST boundary');
// Rome leaves DST on 2026-10-25 at 03:00 CEST -> 02:00 CET. UTC must not care.
check('start 2026-10-24T23:00Z + 300 min = 04:00Z (UTC unaffected by DST)',
  computeEventEnd('2026-10-24T23:00:00Z', '5 hrs').end_at_utc,
  '2026-10-25T04:00:00.000Z');
check('multi-day span across DST, "5 days"',
  computeEventEnd('2026-10-23T18:00:00Z', '5 days').end_at_utc,
  '2026-10-28T18:00:00.000Z');

console.log('bounds and overflow — untrusted numbers must stay structured (cycle-2, item 2)');
check('"999999999999999999999999 days" (not a safe integer) -> unparseable',
  parseDurationText('999999999999999999999999 days'),
  { status: 'unparseable', minutes: null });
check('"9999999 days" (safe integer, in range) still parses',
  parseDurationText('9999999 days'),
  { status: 'parsed', minutes: 9999999 * 1440 });
const hugeSum = Array(20).fill('9999999 days').join(' ');
check('20×"9999999 days" parses numerically (bound is per pair)',
  parseDurationText(hugeSum).status, 'parsed');
check('…but computeEventEnd catches the out-of-range epoch -> date_unparseable, no throw',
  computeEventEnd('2026-09-25T18:00:00Z', hugeSum),
  { ok: true, end_at_utc: '2026-09-25T18:00:00.000Z', date_precision: 'start_only',
    reject_reason: 'date_unparseable', duration_minutes: null, error: null });

console.log('zero-padded numbers — the value bound must not reject them (cycle-3)');
// Cycle-3 reproducer: the old width bound counted characters, so a zero-padded
// number in range was rejected and the item took a spurious date_unparseable.
check('"00000045 min" parses as 45 (was rejected by the width bound)',
  parseDurationText('00000045 min'), { status: 'parsed', minutes: 45 });
check('"00000045 min" is identical to "45 min"',
  parseDurationText('00000045 min'), parseDurationText('45 min'));
check('computeEventEnd("00000045 min") -> 18:45, exact, no reject',
  computeEventEnd('2026-09-25T18:00:00Z', '00000045 min'),
  { ok: true, end_at_utc: '2026-09-25T18:45:00.000Z', date_precision: 'exact',
    reject_reason: null, duration_minutes: 45, error: null });
check('computeEventEnd("00000045 min") is identical to computeEventEnd("45 min")',
  computeEventEnd('2026-09-25T18:00:00Z', '00000045 min'),
  computeEventEnd('2026-09-25T18:00:00Z', '45 min'));
check('"00000001 hr" -> 60 minutes',
  parseDurationText('00000001 hr'), { status: 'parsed', minutes: 60 });
check('computeEventEnd("00000001 hr") -> 19:00, exact',
  computeEventEnd('2026-09-25T18:00:00Z', '00000001 hr'),
  { ok: true, end_at_utc: '2026-09-25T19:00:00.000Z', date_precision: 'exact',
    reject_reason: null, duration_minutes: 60, error: null });
check('"00000000 min" -> parsed 0, not unparseable',
  parseDurationText('00000000 min'), { status: 'parsed', minutes: 0 });
check('computeEventEnd("00000000 min") -> end = start, exact, no reject',
  computeEventEnd('2026-09-25T18:00:00Z', '00000000 min'),
  { ok: true, end_at_utc: '2026-09-25T18:00:00.000Z', date_precision: 'exact',
    reject_reason: null, duration_minutes: 0, error: null });

console.log('computeEventEnd — invalid start stays distinct from date_unparseable');
check('garbage start -> invalid_start_timestamp',
  computeEventEnd('not-a-date', '2 hrs'),
  { ok: false, end_at_utc: null, date_precision: null,
    reject_reason: null, duration_minutes: null, error: 'invalid_start_timestamp' });
check('null start -> invalid_start_timestamp',
  computeEventEnd(null, '2 hrs').error, 'invalid_start_timestamp');

console.log('n8n adapter branch — exact committed file, stubbed $input/$json (cycle-2, item 3)');
const fs = require('fs');
const src = fs.readFileSync(path.join(__dirname, '..', 'code-nodes', 'parse-duration.js'), 'utf8');
function runNode(json) {
  const item = { json };
  const fn = new Function('$input', '$json', src);
  return fn({ item }, json);
}
{
  const out = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '1 hr 30 min', event: {}, quality: {} });
  check('adapter parseable -> exact end on event', out.json.event.end_at_utc, '2026-09-25T19:30:00.000Z');
  check('adapter parseable -> date_precision exact', out.json.event.date_precision, 'exact');
  check('adapter emits NO duration_minutes (off-contract, cycle-2 item 1)',
    'duration_minutes' in out.json.event, false);
  check('adapter parseable -> no reject', out.json.quality.reject_reason || null, null);
}
{
  const out = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: null, event: {}, quality: {} });
  check('adapter missing -> start_only, no reject',
    [out.json.event.date_precision, out.json.quality.reject_reason || null], ['start_only', null]);
}
{
  const out = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: 'circa due ore', event: {}, quality: {} });
  check('adapter unparseable -> date_unparseable on quality',
    out.json.quality.reject_reason, 'date_unparseable');
}
{
  const out = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '999999999999999999999999 days', event: {}, quality: {} });
  check('adapter overflow -> structured item, NO throw (cycle-2 item 2)',
    [out.json.event.date_precision, out.json.quality.reject_reason], ['start_only', 'date_unparseable']);
}
{
  // cycle-3: the zero-padded cases must hold in the adapter branch too.
  const padded = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '00000045 min', event: {}, quality: {} });
  const plain  = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '45 min', event: {}, quality: {} });
  check('adapter "00000045 min" -> 18:45, exact, no reject',
    [padded.json.event.end_at_utc, padded.json.event.date_precision, padded.json.quality.reject_reason || null],
    ['2026-09-25T18:45:00.000Z', 'exact', null]);
  check('adapter "00000045 min" event is identical to "45 min"',
    padded.json.event, plain.json.event);
  const hr = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '00000001 hr', event: {}, quality: {} });
  check('adapter "00000001 hr" -> 19:00 (60 minutes), exact',
    [hr.json.event.end_at_utc, hr.json.event.date_precision], ['2026-09-25T19:00:00.000Z', 'exact']);
  const zero = runNode({ start_at_utc: '2026-09-25T18:00:00Z', duration_raw: '00000000 min', event: {}, quality: {} });
  check('adapter "00000000 min" -> end = start, exact, no reject',
    [zero.json.event.end_at_utc, zero.json.event.date_precision, zero.json.quality.reject_reason || null],
    ['2026-09-25T18:00:00.000Z', 'exact', null]);
}
{
  let threw = null;
  try { runNode({ start_at_utc: 'not-a-date', duration_raw: '2 hrs', event: {}, quality: {} }); }
  catch (e) { threw = e.message; }
  check('adapter invalid start -> throws declared invalid_start_timestamp', threw, 'invalid_start_timestamp');
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

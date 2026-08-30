/**
 * test_parse_duration.js — executable acceptance for code-nodes/parse-duration.js.
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

console.log('computeEventEnd — invalid start stays distinct from date_unparseable');
check('garbage start -> invalid_start_timestamp',
  computeEventEnd('not-a-date', '2 hrs'),
  { ok: false, end_at_utc: null, date_precision: null,
    reject_reason: null, duration_minutes: null, error: 'invalid_start_timestamp' });
check('null start -> invalid_start_timestamp',
  computeEventEnd(null, '2 hrs').error, 'invalid_start_timestamp');

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

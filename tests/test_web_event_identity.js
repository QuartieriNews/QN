/**
 * test_web_event_identity.js — executable acceptance for
 * code-nodes/web-event-identity.js (docs/pilota/CONTRATTI.md, section 7, channel
 * "Eventi dalle pagine web"; Spec v2.5 T17 for the Rome day). Covers BOTH contexts
 * of the one-source file: the CommonJS module branch and the n8n adapter branch,
 * evaluated from the exact committed file with stubbed $input/$json/require.
 * Every URL and title is invented (DEC-109).
 *
 * Run:  node tests/test_web_event_identity.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'web-event-identity.js');
const { canonicalUrl, romeDate, normalizeTitle, webEventIdentity } = require(FILE);

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

function throws(label, fn, message) {
  checks += 1;
  try {
    fn();
  } catch (e) {
    if (e.message === message) {
      console.log(`  ok   ${label}`);
      return;
    }
    failures += 1;
    console.log(`  FAIL ${label}\n       expected error ${message}\n       got      ${e.message}`);
    return;
  }
  failures += 1;
  console.log(`  FAIL ${label}\n       expected error ${message}\n       got no error`);
}

console.log('canonical URL — one page, one string');
check('scheme, host case, www, default port, fragment, trailing slash, tracking, order',
  canonicalUrl('HTTP://WWW.Esempio-Associazione.it:80/Eventi/Concerto/?utm_source=fb&b=2&a=1&fbclid=XYZ#programma'),
  'https://esempio-associazione.it/Eventi/Concerto?a=1&b=2');
check('the path keeps its case (servers may distinguish it)',
  canonicalUrl('https://esempio.it/Eventi/A'), 'https://esempio.it/Eventi/A');
check('the root path stays a slash', canonicalUrl('https://www.esempio.it/'), 'https://esempio.it/');
check('repeated parameters keep their values, sorted', canonicalUrl('https://esempio.it/e?id=2&id=1'), 'https://esempio.it/e?id=1&id=2');
check('an explicit port 80 on https is not the default and stays', canonicalUrl('https://esempio.it:80/e'), 'https://esempio.it:80/e');
check('the default port of each scheme goes', [canonicalUrl('https://esempio.it:443/e'), canonicalUrl('http://esempio.it:80/e')], ['https://esempio.it/e', 'https://esempio.it/e']);
check('a non-default port survives the upgrade to https', canonicalUrl('http://esempio.it:8080/e'), 'https://esempio.it:8080/e');
check('http on port 443 stays distinct from https', canonicalUrl('http://esempio.it:443/e') === canonicalUrl('https://esempio.it/e'), false);
throws('an empty URL is refused', () => canonicalUrl('  '), 'url_missing');
throws('a malformed URL is refused', () => canonicalUrl('not a url'), 'url_invalid');
throws('a non-web scheme is refused', () => canonicalUrl('mailto:info@esempio.it'), 'url_not_http');

console.log('Rome day — T17 across both 2026 clock changes');
check('T17 autumn: 22:30Z on 24 Oct is 25 Oct in Rome', romeDate('2026-10-24T22:30:00Z'), '2026-10-25');
check('T17 autumn: 23:30Z on 25 Oct is 26 Oct in Rome', romeDate('2026-10-25T23:30:00Z'), '2026-10-26');
check('T17 spring: 22:30Z on 28 Mar is still 28 Mar in Rome', romeDate('2026-03-28T22:30:00Z'), '2026-03-28');
check('T17 spring: 22:30Z on 29 Mar is 30 Mar in Rome', romeDate('2026-03-29T22:30:00Z'), '2026-03-30');
throws('an instant without an offset is refused', () => romeDate('2026-10-24T22:30:00'), 'start_invalid');
throws('30 February is refused, not moved to 2 March', () => romeDate('2026-02-30T12:00:00Z'), 'start_invalid');
throws('29 February of a common year is refused', () => romeDate('2026-02-29T12:00:00Z'), 'start_invalid');
check('29 February of a leap year is accepted', romeDate('2028-02-29T12:00:00Z'), '2028-02-29');
throws('hour 24 is refused', () => romeDate('2026-03-01T24:00:00Z'), 'start_invalid');
check('an offset other than Z is honoured', romeDate('2026-10-25T00:30:00+02:00'), '2026-10-25');
check('the Rome day has the exact shape YYYY-MM-DD', /^\d{4}-\d{2}-\d{2}$/.test(romeDate('2026-01-05T08:00:00Z')), true);

console.log('title — Unicode NFC, case and whitespace');
check('composed and decomposed è give one string', normalizeTitle('Caffè letterario'), normalizeTitle('Caffè  letterario'));
check('case and spaces collapse', normalizeTitle('  Festa   DI quartiere '), 'festa di quartiere');
throws('an empty title is refused', () => normalizeTitle('   '), 'title_missing');

console.log('identity — a page of its own wins, and it is stable');
const detail = { detail_url: 'https://www.esempio.it/eventi/festa/?utm_campaign=x', start_at_utc: '2026-11-14T15:00:00Z', title: 'Festa di quartiere' };
const a = webEventIdentity(detail);
check('content_id shape', /^qn:roma:evt:web:[0-9a-f]{16}$/.test(a.content_id), true);
check('file name carries the same key', a.canonical_file_name, `roma__evt__web__${a.content_id.slice(-16)}.json`);
check('not from a listing', a.identity_from_listing, false);
check('same page in another spelling, same identity',
  webEventIdentity({ detail_url: 'http://esempio.it/eventi/festa#info' }).content_id, a.content_id);
check('a new date or title on the same page keeps the identity (source_hash changes instead)',
  webEventIdentity(Object.assign({}, detail, { start_at_utc: '2026-11-21T15:00:00Z', title: 'Festa (rinviata)' })).content_id, a.content_id);
check('a series carries the -series suffix and the same file name',
  [webEventIdentity(Object.assign({}, detail, { is_series: true })).content_id, webEventIdentity(Object.assign({}, detail, { is_series: true })).canonical_file_name],
  [a.content_id + '-series', a.canonical_file_name]);

console.log('identity — an event that only appears in a listing');
const listed = { listing_url: 'https://esempio.it/calendario?mese=11', start_at_utc: '2026-10-24T22:30:00Z', title: 'Caffè letterario' };
const b = webEventIdentity(listed);
check('flagged as from a listing', b.identity_from_listing, true);
check('decomposed title and another URL spelling give the same identity',
  webEventIdentity({ listing_url: 'https://WWW.esempio.it/calendario/?mese=11&utm_medium=x', start_at_utc: '2026-10-24T22:30:00Z', title: ' caffè LETTERARIO ' }).content_id, b.content_id);
check('the Rome day, not the UTC day, enters the key',
  webEventIdentity(Object.assign({}, listed, { start_at_utc: '2026-10-25T07:00:00Z' })).content_id, b.content_id);
check('a | inside the URL or the title cannot make two listings collide',
  webEventIdentity({ listing_url: 'https://x.test/a', start_at_utc: '2026-01-01T12:00:00Z', title: 'x|2026-01-02|y' }).content_id ===
  webEventIdentity({ listing_url: 'https://x.test/a|2026-01-01|x', start_at_utc: '2026-01-02T12:00:00Z', title: 'y' }).content_id, false);
check('two events on the same listing page and day stay distinct',
  webEventIdentity(Object.assign({}, listed, { title: 'Torneo di scacchi' })).content_id === b.content_id, false);
throws('a listing event without a title is refused', () => webEventIdentity({ listing_url: listed.listing_url, start_at_utc: listed.start_at_utc }), 'title_missing');
throws('a listing event without a date is refused', () => webEventIdentity({ listing_url: listed.listing_url, title: 'X' }), 'start_invalid');
throws('no page at all is refused', () => webEventIdentity({ title: 'X', start_at_utc: listed.start_at_utc }), 'url_missing');

console.log('n8n adapter branch — exact committed file, stubbed $input/$json/require');
const src = fs.readFileSync(FILE, 'utf8');
function runNode(json) {
  const item = { json };
  const fn = new Function('$input', '$json', 'require', src);
  return fn({ item }, json, require);
}
{
  const out = runNode({ detail_url: detail.detail_url, start_at_utc: detail.start_at_utc, event_name: detail.title });
  check('adapter writes the module content_id', out.json.content_id, a.content_id);
  check('adapter writes the canonical file name', out.json.canonical_file_name, a.canonical_file_name);
  check('adapter adds no flag for a page of its own', out.json.quality, undefined);
  const lst = runNode({ listing_url: listed.listing_url, start_at_utc: listed.start_at_utc, event_name: listed.title, quality: { review_flags: ['pilot_night_run'] } });
  check('adapter flags a listing identity and keeps earlier flags', lst.json.quality.review_flags, ['pilot_night_run', 'identity_from_listing']);
  const twice = runNode(lst.json);
  check('adapter does not repeat the flag on a retry', twice.json.quality.review_flags, ['pilot_night_run', 'identity_from_listing']);
  checks += 1;
  try {
    runNode({ event_name: 'X' });
    failures += 1;
    console.log('  FAIL adapter fails an item with no page\n       got no error');
  } catch (e) {
    console.log('  ok   adapter fails an item with no page');
  }
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-identity.js: the content_id and file name of a
 * news fact, its source_hash, idempotency and normalization (docs/pilota/CONTRATTI.md,
 * section 7, «B · Notizie»), the same canonical URL as code-nodes/web-event-identity.js,
 * and the n8n adapter evaluated from the exact committed file with stubbed
 * $input/$json/require. Every URL and text is invented (DEC-109, DEC-031 point 4).
 *
 * Run:  node tests/test_news_identity.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'news-identity.js');
const m = require(FILE);
const web = require(path.join(__dirname, '..', 'code-nodes', 'web-event-identity.js'));

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

function thrown(fn) {
  try { fn(); return null; } catch (e) { return e.message; }
}

const URL_A = 'https://www.esempio-inventato.it/notizie/2026/11/fatto-uno/';
const LEAD = { title: 'Titolo inventato', text: 'Testo inventato di un fatto.', published_at_utc: '2026-11-10T09:30:00Z', place: 'Via Inventata 1' };

console.log('identity: CONTRATTI section 7, B · Notizie');
const one = m.newsIdentity({ opening_url: URL_A });
check('form of the content_id', /^qn:roma:nws:[0-9a-f]{16}$/.test(one.content_id), true);
check('the file name follows the id', one.canonical_file_name, one.content_id.replace(/^qn:/, '').split(':').join('__') + '.json');
check('the same URL twice gives the same id (idempotent)', m.newsIdentity({ opening_url: URL_A }), one);
check('tracking parameters take no part',
  m.newsIdentity({ opening_url: URL_A + '?utm_source=x&fbclid=y' }).content_id, one.content_id);
check('www, a trailing slash and a fragment take no part',
  m.newsIdentity({ opening_url: 'https://esempio-inventato.it/notizie/2026/11/fatto-uno#sopra' }).content_id, one.content_id);
check('the order of the other parameters takes no part',
  m.newsIdentity({ opening_url: 'https://esempio-inventato.it/n?b=2&a=1' }).content_id,
  m.newsIdentity({ opening_url: 'https://esempio-inventato.it/n?a=1&b=2' }).content_id);
check('another page is another fact', m.newsIdentity({ opening_url: URL_A + 'altro' }).content_id !== one.content_id, true);
check('a record with several facts: the fact index is a suffix', m.newsIdentity({ opening_url: URL_A, fact_index: 2 }).content_id, one.content_id + '-f2');
check('and in the file name', m.newsIdentity({ opening_url: URL_A, fact_index: 2 }).canonical_file_name, one.canonical_file_name.replace('.json', '-f2.json'));
check('a fact index of 0 is refused', thrown(() => m.newsIdentity({ opening_url: URL_A, fact_index: 0 })), 'fact_index_invalid');
check('a fact index that is not a whole number is refused', thrown(() => m.newsIdentity({ opening_url: URL_A, fact_index: '2' })), 'fact_index_invalid');
check('no URL, no id', thrown(() => m.newsIdentity({ opening_url: ' ' })), 'url_missing');
check('a URL that is not http is refused', thrown(() => m.newsIdentity({ opening_url: 'ftp://esempio-inventato.it/x' })), 'url_not_http');
check('geography and registro_id take no part: only the URL and the fact index are read',
  m.newsIdentity({ opening_url: URL_A, publication_zone_id: 'acilia', registro_id: 'S-0001' }), one);
check('source_id is the host, lowercase, without www', m.sourceIdFromUrl('https://WWW.Esempio-Inventato.IT/x'), 'esempio-inventato.it');

console.log('the canonical URL is the one of web events');
for (const u of [URL_A, 'http://www.esempio-inventato.it:8080/a/?z=1&utm_medium=m&a=2#f', 'http://esempio-inventato.it:443/x',
  'https://esempio-inventato.it/', 'HTTPS://Esempio-Inventato.it/Percorso/Maiuscolo']) {
  check(`same canonical URL: ${u}`, m.canonicalUrl(u), web.canonicalUrl(u));
}
check('same list of tracking parameters', String(m.TRACKING_PARAM), String(web.TRACKING_PARAM));

console.log('source_hash: the lead record');
const h = m.newsSourceHash(LEAD);
check('a 64-digit SHA-256', /^[0-9a-f]{64}$/.test(h), true);
check('the same record twice gives the same hash', m.newsSourceHash(Object.assign({}, LEAD)), h);
check('spaces at the edges and inside are normalised', m.newsSourceHash(Object.assign({}, LEAD, { text: '  Testo   inventato di un\nfatto. ' })), h);
check('one instant written with an offset is the same instant',
  m.newsSourceHash(Object.assign({}, LEAD, { published_at_utc: '2026-11-10T10:30:00+01:00' })), h);
check('a changed text changes the hash', m.newsSourceHash(Object.assign({}, LEAD, { text: 'Altro testo inventato.' })) !== h, true);
check('a changed place changes the hash', m.newsSourceHash(Object.assign({}, LEAD, { place: 'Piazza Inventata' })) !== h, true);
check('a source that gives only the day is read as the day', m.normalizePublished('2026-11-10'), '2026-11-10');
check('the instant is written in one form', m.normalizePublished('2026-11-10T10:30+01:00'), '2026-11-10T09:30:00.000Z');
check('30 February is refused', thrown(() => m.normalizePublished('2026-02-30')), 'published_invalid');
check('hour 25 is refused', thrown(() => m.normalizePublished('2026-11-10T25:00:00Z')), 'published_invalid');
check('an instant without an offset is refused', thrown(() => m.normalizePublished('2026-11-10T09:30:00')), 'published_invalid');
check('the content_id does not change when the source changes',
  m.newsIdentity({ opening_url: URL_A }).content_id, one.content_id);
check('the fields stay apart: moving text between title and text changes the hash',
  m.newsSourceHash({ title: 'a b', text: 'c', published_at_utc: '2026-11-10', place: '' }) !==
  m.newsSourceHash({ title: 'a', text: 'b c', published_at_utc: '2026-11-10', place: '' }), true);

console.log('n8n adapter — exact committed file, stubbed $input/$json/require');
const src = fs.readFileSync(FILE, 'utf8');
function runNode(json) {
  const item = { json };
  return new Function('$input', '$json', 'require', src)({ item }, json, require);
}
{
  const out = runNode({ opening_url: URL_A, lead: LEAD });
  check('the adapter adds the module identity', [out.json.content_id, out.json.canonical_file_name], [one.content_id, one.canonical_file_name]);
  check('and the source_id and source_hash', [out.json.source_id, out.json.source_hash], ['esempio-inventato.it', h]);
  check('the other fields are untouched', out.json.lead, LEAD);
  check('an item without a usable URL fails', thrown(() => runNode({ lead: LEAD })), 'url_missing');
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

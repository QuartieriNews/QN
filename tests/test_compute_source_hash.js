/**
 * test_compute_source_hash.js — executable acceptance for
 * code-nodes/compute-source-hash.js (Spec v2.5 Phase 2.2; cases T20, T21; the
 * Phase 1.3 tie-break count). Covers BOTH contexts of the one-source file: the
 * CommonJS module branch and the n8n adapter branch, evaluated from the exact
 * committed file with stubbed $input/$json/require.
 *
 * Run:  node tests/test_compute_source_hash.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const {
  HASH_FIELDS, buildHashInput, computeSourceHash, countNonEmptyHashedFields, hashInputValue,
} = require(path.join(__dirname, '..', 'code-nodes', 'compute-source-hash.js'));

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

/** The Phase 1.3 example record, with the values a real scrape fills in. */
function sample(overrides) {
  const base = {
    source_event_id: '123456789',
    source_url: 'https://facebook.com/events/123456789',
    source_name: 'Facebook',
    event_name: 'Festa di quartiere',
    source_description: 'Musica dal vivo e stand gastronomici',
    start_at_utc: '2026-07-25T18:00:00Z',
    end_at_utc: null,
    duration_raw: null,
    is_online_source_flag: false,
    is_cancelled_source_flag: false,
    location: {
      name: 'Parco della Caffarella',
      address: 'Via Latina, Roma',
      city: 'Roma',
      country_code: 'IT',
      latitude: 41.8689,
      longitude: 12.5247,
    },
    organizer: { name: 'Comitato di quartiere' },
    source_image_url: 'https://scontent.xx.fbcdn.net/v/t1.6435_n.jpg?_nc_ohc=AbC&oh=00_Af&oe=68F',
    cost_raw: null,
    booking_url_raw: null,
    retrieved_at: '2026-07-24T08:30:00Z',
  };
  const s = JSON.parse(JSON.stringify(base));
  for (const [k, v] of Object.entries(overrides || {})) {
    if (k.includes('.')) {
      const [a, b] = k.split('.');
      s[a][b] = v;
    } else {
      s[k] = v;
    }
  }
  return s;
}

console.log('Phase 2.2 — field order and serialization are the contract');
check('14 fields in the spec order', HASH_FIELDS, [
  'event_name', 'source_description', 'start_at_utc', 'end_at_utc',
  'location.name', 'location.address', 'location.city', 'location.country_code',
  'location.latitude', 'location.longitude', 'organizer.name', 'source_image_url',
  'cost_raw', 'booking_url_raw',
]);
check('hash input is an array of pairs, not an object', Array.isArray(buildHashInput(sample())), true);
check('every pair value is a string', buildHashInput(sample()).every(([, v]) => typeof v === 'string'), true);
{
  const expected = 'sha256:' + crypto.createHash('sha256')
    .update(JSON.stringify(buildHashInput(sample())), 'utf8').digest('hex');
  check('hash = "sha256:" + SHA-256 of JSON.stringify(pair array)', computeSourceHash(sample()), expected);
  check('hash is lowercase hex, 64 chars', /^sha256:[0-9a-f]{64}$/.test(computeSourceHash(sample())), true);
}
check('excluded fields do not move the hash (retrieved_at, source_url, flags)',
  computeSourceHash(sample({ retrieved_at: '2030-01-01T00:00:00Z', source_url: 'x', is_cancelled_source_flag: true })),
  computeSourceHash(sample()));
check('a hashed field does move the hash',
  computeSourceHash(sample({ event_name: 'Altro titolo' })) === computeSourceHash(sample()), false);

console.log('T20 — identical source twice, and a whitespace-only variant');
check('same input twice -> same hash', computeSourceHash(sample()), computeSourceHash(sample()));
check('leading/trailing/inner whitespace runs -> same hash',
  computeSourceHash(sample({ event_name: '  Festa   di\n\tquartiere ', 'location.name': 'Parco  della Caffarella ' })),
  computeSourceHash(sample()));
check('NFC vs NFD composition -> same hash',
  computeSourceHash(sample({ event_name: 'Caffé letterario' })),
  computeSourceHash(sample({ event_name: 'Caffé letterario' })));
check('null, undefined, "" are indistinguishable (end_at_utc)',
  [computeSourceHash(sample({ end_at_utc: undefined })), computeSourceHash(sample({ end_at_utc: '' }))],
  [computeSourceHash(sample({ end_at_utc: null })), computeSourceHash(sample({ end_at_utc: null }))]);
check('null, undefined, "" are indistinguishable (cost_raw / booking_url_raw)',
  computeSourceHash(sample({ cost_raw: '', booking_url_raw: undefined })),
  computeSourceHash(sample()));
check('key order of the source object is irrelevant',
  computeSourceHash({ location: { city: 'Roma', name: 'A' }, event_name: 'E' }),
  computeSourceHash({ event_name: 'E', location: { name: 'A', city: 'Roma' } }));

console.log('T21 — same image, new CDN signing parameters');
check('query string discarded: origin + pathname only',
  hashInputValue('source_image_url', 'https://scontent.xx.fbcdn.net/v/t1.6435_n.jpg?_nc_ohc=AbC&oh=00_Af&oe=68F'),
  'https://scontent.xx.fbcdn.net/v/t1.6435_n.jpg');
check('re-signed URL -> hash unchanged',
  computeSourceHash(sample({ source_image_url: 'https://scontent.xx.fbcdn.net/v/t1.6435_n.jpg?_nc_ohc=ZZZ&oh=11_Bg&oe=70A&stp=dst' })),
  computeSourceHash(sample()));
check('different image path -> hash changes',
  computeSourceHash(sample({ source_image_url: 'https://scontent.xx.fbcdn.net/v/other.jpg' })) === computeSourceHash(sample()), false);
check('fragment discarded too', hashInputValue('source_image_url', 'https://h.example/p.jpg#x'), 'https://h.example/p.jpg');
check('non-URL value falls back to the string rule, deterministically',
  hashInputValue('source_image_url', '  not a url  '), 'not a url');

console.log('Timestamps — UTC, second precision, Z, no milliseconds');
check('offset form normalizes to Z', hashInputValue('start_at_utc', '2026-07-25T20:00:00+02:00'), '2026-07-25T18:00:00Z');
check('milliseconds dropped', hashInputValue('start_at_utc', '2026-07-25T18:00:00.123Z'), '2026-07-25T18:00:00Z');
check('already canonical stays identical', hashInputValue('start_at_utc', '2026-07-25T18:00:00Z'), '2026-07-25T18:00:00Z');
check('equivalent instants -> same hash',
  computeSourceHash(sample({ start_at_utc: '2026-07-25T20:00:00.000+02:00' })), computeSourceHash(sample()));
check('unparseable timestamp hashes as its trimmed string (no throw)', hashInputValue('end_at_utc', ' TBD '), 'TBD');

console.log('Coordinates — fixed decimal, six places');
check('number rounded to six places', hashInputValue('location.latitude', 41.86891234), '41.868912');
check('integer padded to six places', hashInputValue('location.longitude', 12), '12.000000');
check('numeric string accepted', hashInputValue('location.latitude', ' 41.8689 '), '41.868900');
check('non-numeric string -> empty', hashInputValue('location.latitude', 'n/a'), '');
check('negative zero normalized', hashInputValue('location.latitude', -0.0000001), '0.000000');
check('float noise beyond six places does not move the hash',
  computeSourceHash(sample({ 'location.latitude': 41.8689000000001 })), computeSourceHash(sample()));
check('seventh-place difference rounds away', hashInputValue('location.latitude', 41.8689004), '41.868900');

console.log('Scalars and non-scalars');
check('number in a string field -> its string', hashInputValue('cost_raw', 10), '10');
check('boolean in a string field -> its string', hashInputValue('cost_raw', false), 'false');
check('object in a string field -> empty', hashInputValue('event_name', { a: 1 }), '');
check('missing location block -> all location fields empty, no throw',
  buildHashInput({ event_name: 'E' }).filter(([k]) => k.startsWith('location.')).every(([, v]) => v === ''), true);
check('non-object source -> hash of all-empty pairs', computeSourceHash(null), computeSourceHash({}));

console.log('Phase 1.3 tie-break — non-empty hashed fields');
check('sample counts 11 of 14 (end, cost, booking empty)', countNonEmptyHashedFields(sample()), 11);
check('whitespace-only counts as empty', countNonEmptyHashedFields(sample({ event_name: '   ' })), 10);
check('empty object counts 0', countNonEmptyHashedFields({}), 0);

console.log('n8n adapter branch — exact committed file, stubbed $input/$json/require');
const src = fs.readFileSync(path.join(__dirname, '..', 'code-nodes', 'compute-source-hash.js'), 'utf8');
function runNode(json) {
  const item = { json };
  const fn = new Function('$input', '$json', 'require', src);
  return fn({ item }, json, require);
}
{
  const json = sample();
  const out = runNode(json);
  check('adapter writes source.source_hash equal to the module result', out.json.source.source_hash, computeSourceHash(sample()));
  check('adapter returns the same item', out.json === json, true);
  check('adapter leaves the hashed fields untouched', out.json.event_name, 'Festa di quartiere');
  const again = runNode(sample({ source_image_url: 'https://scontent.xx.fbcdn.net/v/t1.6435_n.jpg?oh=NEW&oe=NEW' }));
  check('adapter T21: re-signed image -> same stored hash', again.json.source.source_hash, out.json.source.source_hash);
  const withSource = runNode(Object.assign(sample(), { source: { source_name: 'Facebook' } }));
  check('adapter preserves an existing source block', withSource.json.source.source_name, 'Facebook');
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

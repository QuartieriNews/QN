/**
 * test_merge_duplicate_events.js — executable acceptance for
 * code-nodes/merge-duplicate-events.js (DEC-025, rules 1-4; same-event criteria of the
 * October 2026 sheet, tools/fonti/lavoro-2026-10/doppioni.py on PR #21). Covers BOTH
 * contexts of the one-source file. Expected similarities were computed with CPython's
 * difflib on the same normalization and are written here, so the suite needs no Python.
 * Every title, venue and URL is invented (DEC-109).
 *
 * Run:  node tests/test_merge_duplicate_events.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'merge-duplicate-events.js');
const { PRECEDENCE, tokens, similarity, compare, mergeDuplicateEvents } = require(FILE);

let failures = 0;
let checks = 0;
function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) console.log(`  ok   ${label}`);
  else { failures += 1; console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`); }
}

console.log('normalization and similarity match CPython (October sheet)');
const PY = [
  ["Festa di Quartiere 2026", "FESTA DEL QUARTIERE – 2026", ["festa", "quartiere", "2026"], ["festa", "quartiere", "2026"], 1.0],
  ["Caffè letterario «Ritratti»", "Caffe letterario: Ritratti!", ["caffe", "letterario", "ritratti"], ["caffe", "letterario", "ritratti"], 1.0],
  ["Concerto jazz al Charity Café", "Jazz night con il quartetto", ["jazz", "charity", "cafe"], ["jazz", "night", "quartetto"], 0.540540540541],
  ["Mercatino dell'usato", "Mercatino solidale di Natale", ["mercatino", "dell", "usato"], ["mercatino", "solidale", "natale"], 0.666666666667],
  ["Ciclo di letture: La signora Dalloway", "Circolo di lettura - La Signora Dalloway", ["ciclo", "letture", "signora", "dalloway"], ["circolo", "lettura", "signora", "dalloway"], 0.935483870968],
  ["a«b c»d", "ab cd", [], [], 0],
  ["Straße Fest", "Strasse fest", ["strae", "fest"], ["strasse", "fest"], 0.909090909091]
];
for (const [a, b, ta, tb, s] of PY) {
  check(`tokens of ${JSON.stringify(a)}`, tokens(a), ta);
  check(`similarity ${JSON.stringify(a)} ~ ${JSON.stringify(b)}`, Math.round(similarity(tokens(a), tokens(b)) * 1e9) / 1e9, Math.round(s * 1e9) / 1e9);
}

function ev(id, type, title, start, extra) {
  const e = Object.assign({
    schema_version: '2.0', content_id: id, source: { type, url: `https://esempio.it/${id}` },
    article: { title }, pilot: { source_title: title },
    event: { start_at_utc: start, end_at_utc: null, date_precision: 'start_only', venue: 'Sala Comune Esempio' },
    geography: { municipality_code: null }, quality: { requires_review: false, reject_reason: null, review_flags: [] },
    lifecycle: { status: 'active' },
  }, extra || {});
  return e;
}

console.log('same event, DEC-025 rule 4 (the October criteria)');
const f = (d) => ({
  title: tokens(d.pilot.source_title), venue: new Set(tokens(d.event.venue)),
  start: d.event.start_at_utc.slice(0, 10), end: d.event.start_at_utc.slice(0, 10),
});
check('near-identical title on the same day is the same event',
  compare(f(ev('a', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z')), f(ev('b', 'facebook_event', 'FESTA DEL QUARTIERE – 2026', '2026-11-14T15:00:00Z'))), 'same');
check('near-identical title on another day is not',
  compare(f(ev('a', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z')), f(ev('b', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-28T15:00:00Z'))), null);
check('a near-identical title is the same event even with another venue name (first October criterion)',
  compare(f(ev('a', 'web_page', 'Ciclo di letture: La signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: 'Biblioteca Esempio' } })),
          f(ev('b', 'facebook_event', 'Circolo di lettura - La Signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: 'Libreria Altrove' } }))), 'same');
check('similar title, same day and venue is the same event',
  compare(f(ev('a', 'web_page', 'Ciclo di letture: La signora Dalloway', '2026-11-14T17:00:00Z')),
          f(ev('b', 'facebook_event', 'Circolo di lettura - La Signora Dalloway', '2026-11-14T17:00:00Z'))), 'same');
check('a weakly similar title on the same day is not the same event',
  compare(f(ev('a', 'web_page', 'Mercatino dell\'usato', '2026-11-14T09:00:00Z')), f(ev('b', 'facebook_event', 'Mercatino solidale di Natale', '2026-11-14T09:00:00Z'))), null);

console.log('precedence and filling, DEC-025 rules 1-3');
{
  const web = ev('qn:roma:evt:web:aaaa', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', date_precision: 'start_only', venue: 'Sala Comune Esempio', latitude: null, longitude: null } });
  const fb = ev('qn:roma:evt:facebook:1', 'facebook_event', 'FESTA DEL QUARTIERE – 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', date_precision: 'start_only', venue: 'Sala Comune Esempio', latitude: 41.9, longitude: 12.5 } });
  const other = ev('qn:roma:evt:facebook:2', 'facebook_event', 'Torneo di scacchi', '2026-11-14T15:00:00Z');
  const out = mergeDuplicateEvents([fb, other, web]);
  const byId = Object.fromEntries(out.map((d) => [d.content_id, d]));
  check('the web page of the organiser comes before Facebook', PRECEDENCE.indexOf('web_page') < PRECEDENCE.indexOf('facebook_event'), true);
  check('the main element is the web page', byId['qn:roma:evt:facebook:1'].pilot.duplicate_of, 'qn:roma:evt:web:aaaa');
  check('the main element lists its duplicates', byId['qn:roma:evt:web:aaaa'].pilot.duplicates, ['qn:roma:evt:facebook:1']);
  check('coordinates missing on the web page come from Facebook',
    [byId['qn:roma:evt:web:aaaa'].event.latitude, byId['qn:roma:evt:web:aaaa'].event.longitude], [41.9, 12.5]);
  check('the main element says where each filled field came from',
    byId['qn:roma:evt:web:aaaa'].pilot.filled_from, { 'event.latitude': 'qn:roma:evt:facebook:1', 'event.longitude': 'qn:roma:evt:facebook:1' });
  check('the secondary copy stays, flagged, nothing deleted', [out.length, byId['qn:roma:evt:facebook:1'].quality.review_flags], [3, ['duplicate_suspected']]);
  check('an unrelated event is untouched', [byId['qn:roma:evt:facebook:2'].pilot.duplicate_of, byId['qn:roma:evt:facebook:2'].quality.review_flags], [undefined, []]);
  check('the input documents are not modified', fb.pilot.duplicate_of, undefined);
  const again = mergeDuplicateEvents([web, fb, other]);
  check('the result does not depend on input order',
    again.find((d) => d.content_id === 'qn:roma:evt:facebook:1').pilot.duplicate_of, 'qn:roma:evt:web:aaaa');
}

console.log('geography and Roma Today, DEC-025 rule 2');
{
  const web = ev('w1', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: null, longitude: null } });
  const cul = ev('c1', 'culture_roma', 'Festa di quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.9, longitude: 12.5 },
      geography: { municipality_code: 'V', publication_zone_id: 'centocelle' } });
  const rt = ev('r1', 'roma_today', 'Festa di quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', booking_url: 'https://esempio.it/biglietti' } });
  const out = mergeDuplicateEvents([web, cul, rt]);
  const w = out.find((d) => d.content_id === 'w1');
  check('the municipality of another source is never copied', w.geography.municipality_code, null);
  check('coordinates move, and the place is marked for the gazetteer to resolve again', [w.event.latitude, w.pilot.geo_recompute], [41.9, true]);
  check('Roma Today gives no field, even one nobody else has', w.event.booking_url, undefined);
}

console.log('identity, DEC-025 rule 3');
{
  const fb = ev('qn:roma:evt:facebook:9', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { pilot: { source_title: 'Festa di Quartiere 2026', first_published_at: '2026-11-10T08:00:00Z' },
      event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Esempio' } });
  const web = ev('qn:roma:evt:web:bbbb', 'web_page', 'Festa di quartiere 2026', '2026-11-14T16:00:00Z',
    { event: { start_at_utc: '2026-11-14T16:00:00Z', venue: 'Sala Comune Esempio' } });
  const out = mergeDuplicateEvents([web, fb]);
  const e = out.find((d) => d.content_id === 'qn:roma:evt:facebook:9');
  check('the element already published keeps its content_id', out.find((d) => d.content_id === 'qn:roma:evt:web:bbbb').pilot.duplicate_of, 'qn:roma:evt:facebook:9');
  check('it takes the leading source\'s fields', [e.event.start_at_utc, e.event.venue, e.pilot.lead], ['2026-11-14T16:00:00Z', 'Sala Comune Esempio', 'qn:roma:evt:web:bbbb']);
  check('and says where they came from', e.pilot.filled_from['event.start_at_utc'], 'qn:roma:evt:web:bbbb');
  check('nothing published yet: the leading source gives the identity',
    mergeDuplicateEvents([Object.assign({}, fb, { pilot: { source_title: 'Festa di Quartiere 2026' } }), web])
      .find((d) => d.content_id === 'qn:roma:evt:facebook:9').pilot.duplicate_of, 'qn:roma:evt:web:bbbb');
}

console.log('doubt goes to the queue, DEC-025 rule 4');
{
  const a = ev('u1', 'web_page', 'Festa di Quartiere 2026', null, { event: { start_at_utc: null, venue: 'Sala Esempio' } });
  const b = ev('u2', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  const out = mergeDuplicateEvents([a, b]);
  check('an undated event is not merged, both go to the queue', out.map((d) => [d.pilot.duplicate_of, d.quality.review_flags]),
    [[undefined, ['duplicate_doubt']], [undefined, ['duplicate_doubt']]]);
  const s = ev('s1', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { series: { is_series: true, next_occurrence: '2026-11-14T15:00:00Z' } });
  const out2 = mergeDuplicateEvents([s, b]);
  check('a series against a single event is not merged', out2.map((d) => d.pilot.duplicate_of), [undefined, undefined]);
}
console.log('doubt goes to the queue, DEC-025 rule 4');
{
  // similarity 0.808511 in CPython: above 0.72, below 0.85, and the venues differ
  const a = ev('x1', 'web_page', 'Laboratorio di origami', '2026-11-14T17:00:00Z', {
    event: { start_at_utc: '2026-11-14T17:00:00Z', date_precision: 'start_only', venue: 'Biblioteca Esempio' } });
  const b = ev('x2', 'facebook_event', 'Laboratorio di origami e kirigami', '2026-11-14T17:00:00Z', {
    event: { start_at_utc: '2026-11-14T17:00:00Z', date_precision: 'start_only', venue: 'Libreria Altrove' } });
  check('the pair sits in the doubt band', Math.round(similarity(tokens(a.pilot.source_title), tokens(b.pilot.source_title)) * 1e6) / 1e6, 0.808511);
  const out = mergeDuplicateEvents([a, b]);
  check('similar title, same day, different venue: not merged', out.map((d) => d.pilot.duplicate_of), [undefined, undefined]);
  check('both are flagged for review instead', out.map((d) => [d.quality.review_flags, d.quality.requires_review]),
    [[['duplicate_doubt'], true], [['duplicate_doubt'], true]]);
}

console.log('n8n adapter branch — exact committed file, stubbed $input/require');
{
  const src = fs.readFileSync(FILE, 'utf8');
  const fn = new Function('$input', 'require', src);
  const items = [ev('w', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z'),
                 ev('f', 'facebook_event', 'FESTA DEL QUARTIERE – 2026', '2026-11-14T15:00:00Z')].map((json) => ({ json }));
  const out = fn({ all: () => items }, require);
  check('adapter returns one item per input', out.length, 2);
  check('adapter marks the Facebook copy as the duplicate', out[1].json.pilot.duplicate_of, 'w');
}

console.log('');
if (failures === 0) { console.log(`ALL PASS (${checks} checks)`); process.exit(0); }
console.log(`${failures} of ${checks} checks FAILED`);
process.exit(1);

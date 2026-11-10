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
const { PRECEDENCE, tokens, identifiers, similarity, features, compare, mergeDuplicateEvents } = require(FILE);

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
  ["Mercatino dell'usato", "Mercatino solidale di Natale", ["mercatino", "dell", "usato"], ["mercatino", "solidale", "natale"], 0.577777777778],
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
    article: { title }, pilot: { source_title: title, first_written_at: '2026-11-10T08:00:00Z' },
    event: { start_at_utc: start, end_at_utc: null, date_precision: 'start_only', venue: 'Sala Comune Esempio' },
    geography: { municipality_code: null }, quality: { requires_review: false, reject_reason: null, review_flags: [] },
    lifecycle: { status: 'active' },
  }, extra || {});
  return e;
}

console.log('same event, DEC-025 rule 4 (the October criteria)');
const f = features;
check('near-identical title on the same day is the same event',
  compare(f(ev('a', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z')), f(ev('b', 'facebook_event', 'FESTA DEL QUARTIERE – 2026', '2026-11-14T15:00:00Z'))), 'same');
check('near-identical title on another day is not',
  compare(f(ev('a', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z')), f(ev('b', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-28T15:00:00Z'))), null);
check('a near-identical title at two venues with no word in common goes to the queue (DEC-025 rule 4)',
  compare(f(ev('a', 'web_page', 'Ciclo di letture: La signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: 'Biblioteca Esempio' } })),
          f(ev('b', 'facebook_event', 'Circolo di lettura - La Signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: 'Libreria Altrove' } }))), 'doubt');
check('a near-identical title with one venue unknown goes to the queue: the places must coincide (DEC-025 rule 4)',
  compare(f(ev('a', 'web_page', 'Ciclo di letture: La signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: 'Biblioteca Esempio' } })),
          f(ev('b', 'facebook_event', 'Circolo di lettura - La Signora Dalloway', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: null } }))), 'doubt');
check('two places that share only one generic word do not coincide',
  compare(f(ev('a', 'web_page', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Biblioteca Esempio' } })),
          f(ev('b', 'facebook_event', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Biblioteca Altrove' } }))), 'doubt');
check('two events with no place (online) go to the queue',
  compare(f(ev('a', 'web_page', 'Incontro online sul quartiere', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: null } })),
          f(ev('b', 'facebook_event', 'Incontro online sul quartiere', '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue: null } }))), 'doubt');
check('similar title, same day and venue is the same event',
  compare(f(ev('a', 'web_page', 'Ciclo di letture: La signora Dalloway', '2026-11-14T17:00:00Z')),
          f(ev('b', 'facebook_event', 'Circolo di lettura - La Signora Dalloway', '2026-11-14T17:00:00Z'))), 'same');
check('a weakly similar title on the same day is not the same event',
  compare(f(ev('a', 'web_page', 'Mercatino dell\'usato', '2026-11-14T09:00:00Z')), f(ev('b', 'facebook_event', 'Mercatino solidale di Natale', '2026-11-14T09:00:00Z'))), null);

console.log('the source title, DEC-025 rule 1');
{
  const thrown = (docs) => { try { mergeDuplicateEvents(docs); return null; } catch (e) { return e.message; } };
  const noName = ev('qn:roma:evt:facebook:9', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { pilot: {} });
  check('a file without pilot.source_title stops the merge and names the file',
    /qn:roma:evt:facebook:9: pilot\.source_title missing/.test(thrown([noName]) || ''), true);
  const ours = ev('qn:roma:evt:web:b', 'web_page', 'Mercatino solidale di Natale', '2026-11-14T15:00:00Z',
    { article: { title: 'Festa di Quartiere 2026' } });
  const fb = ev('qn:roma:evt:facebook:8', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  check('our article title takes no part in the match',
    mergeDuplicateEvents([ours, fb]).some((d) => d.pilot.duplicate_of), false);
}

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
  const webV = Object.assign({}, web, { geography: { municipality_code: 'V', publication_zone_id: 'centocelle', geo_verification_status: 'human_verified' } });
  const v = mergeDuplicateEvents([webV, cul]).find((d) => d.content_id === 'w1');
  check('a human_verified geography takes no location evidence and is not recalculated', [v.event.latitude, v.pilot.geo_recompute, v.geography.publication_zone_id], [null, undefined, 'centocelle']);
  check('different evidence sends it to the queue', [v.quality.review_flags.includes('geo_verified_conflict'), v.quality.requires_review], [true, true]);
}

console.log('identity, DEC-025 rule 3');
{
  const fb = ev('qn:roma:evt:facebook:9', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-09T08:00:00Z' },
      event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Esempio' } });
  const web = ev('qn:roma:evt:web:bbbb', 'web_page', 'Festa di quartiere 2026', '2026-11-14T16:00:00Z',
    { event: { start_at_utc: '2026-11-14T16:00:00Z', venue: 'Sala Comune Esempio' } });
  const out = mergeDuplicateEvents([web, fb]);
  const e = out.find((d) => d.content_id === 'qn:roma:evt:facebook:9');
  check('the element written first keeps its content_id, even below the lead', out.find((d) => d.content_id === 'qn:roma:evt:web:bbbb').pilot.duplicate_of, 'qn:roma:evt:facebook:9');
  check('it takes the leading source\'s fields', [e.event.start_at_utc, e.event.venue, e.pilot.lead], ['2026-11-14T16:00:00Z', 'Sala Comune Esempio', 'qn:roma:evt:web:bbbb']);
  check('and says where they came from', e.pilot.filled_from['event.start_at_utc'], 'qn:roma:evt:web:bbbb');
  check('written at the same time: the leading source gives the identity',
    mergeDuplicateEvents([Object.assign({}, fb, { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-10T08:00:00Z' } }), web])
      .find((d) => d.content_id === 'qn:roma:evt:facebook:9').pilot.duplicate_of, 'qn:roma:evt:web:bbbb');
}

console.log('doubt goes to the queue, DEC-025 rule 4');
{
  const a = ev('u1', 'web_page', 'Festa di Quartiere 2026', null, { event: { start_at_utc: null, venue: 'Sala Esempio' } });
  const b = ev('u2', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  const out = mergeDuplicateEvents([a, b]);
  check('an undated event is not merged, both go to the queue', out.map((d) => [d.pilot.duplicate_of, d.quality.review_flags]),
    [[undefined, ['duplicate_doubt']], [undefined, ['duplicate_doubt']]]);
  const m1 = ev('m1', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z');
  const m2 = ev('m2', 'facebook_event', 'Il piccolo principe', '2026-11-14T19:30:00Z');
  check('the same title on the same day, hours apart: two performances, sent to the queue',
    mergeDuplicateEvents([m1, m2]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags]),
    [[undefined, ['duplicate_doubt']], [undefined, ['duplicate_doubt']]]);
  const n1 = ev('n1', 'web_page', 'Il piccolo principe', '2026-11-14T19:00:00Z');
  check('within 60 minutes it is the same event', mergeDuplicateEvents([n1, m2])[1].pilot.duplicate_of, 'n1');
  const o1 = ev('o1', 'web_page', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Scuola Primaria Esempio' } });
  const o2 = ev('o2', 'facebook_event', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Palestra Altrove' } });
  check('a generic title at two different places on the same day is not merged (venues in conflict)',
    mergeDuplicateEvents([o1, o2]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags]),
    [[undefined, ['duplicate_doubt']], [undefined, ['duplicate_doubt']]]);
  const c1 = ev('c1', 'web_page', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Scuola Esempio', latitude: 41.89, longitude: 12.49 } });
  const c2 = ev('c2', 'facebook_event', 'Open Day', '2026-11-14T08:00:00Z', { event: { start_at_utc: '2026-11-14T08:00:00Z', venue: 'Scuola Esempio', latitude: 41.92, longitude: 12.49 } });
  check('the same venue name more than 1 km apart is a conflict too', mergeDuplicateEvents([c1, c2])[1].pilot.duplicate_of, undefined);
  const c3 = Object.assign({}, c2, { event: Object.assign({}, c2.event, { latitude: 41.8905 }) });
  check('the same venue a few metres apart is the same event', mergeDuplicateEvents([c1, c3])[1].pilot.duplicate_of, 'c1');
  const j1 = ev('j1', 'web_page', '\u6625\u306e\u7948\u308a', '2026-11-14T15:00:00Z');
  const j2 = ev('j2', 'facebook_event', '\u590f\u306e\u591c', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Palestra Altrove' } });
  check('titles that normalize to nothing never merge, and at different places they do not wait either',
    mergeDuplicateEvents([j1, j2]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags]), [[undefined, []], [undefined, []]]);
  const j3 = ev('j3', 'facebook_event', '\u6625\u306e\u7948\u308a', '2026-11-14T15:00:00Z');
  check('two empty normalized titles on the same day at the same place go to the queue',
    mergeDuplicateEvents([j1, j3]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags]), [[undefined, ['duplicate_doubt']], [undefined, ['duplicate_doubt']]]);
  const t1 = ev('t1', 'web_page', 'Il piccolo principe', '2026-11-14T00:00:00Z',
    { quality: { requires_review: false, reject_reason: null, review_flags: ['start_time_unknown'] } });
  check('a source that gives the day without the time is not merged, it waits',
    mergeDuplicateEvents([t1, n1]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags.includes('duplicate_doubt')]), [[undefined, true], [undefined, true]]);
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

console.log('fields that go together, and an element still in the queue, DEC-025 rules 2-3');
{
  // the Facebook copy was written first, so it keeps its identity; the web page leads
  const fb = ev('qn:roma:evt:facebook:5', 'facebook_event', 'Il piccolo principe', '2026-11-14T18:00:00Z',
    { pilot: { source_title: 'Il piccolo principe', first_written_at: '2026-11-09T08:00:00Z' },
      event: { start_at_utc: '2026-11-14T18:00:00Z', end_at_utc: '2026-11-14T18:30:00Z', date_precision: 'exact', venue: 'Sala Comune Esempio', latitude: 41.9 } });
  const web = ev('qn:roma:evt:web:cccc', 'web_page', 'Il piccolo principe', '2026-11-14T19:00:00Z',
    { event: { start_at_utc: '2026-11-14T19:00:00Z', end_at_utc: null, date_precision: 'start_only', venue: 'Sala Comune Esempio' } });
  const e = mergeDuplicateEvents([fb, web]).find((d) => d.content_id === 'qn:roma:evt:facebook:5');
  check('the times move as one: the lead\'s start without an end never meets the copy\'s end',
    [e.event.start_at_utc, e.event.end_at_utc, e.event.date_precision], ['2026-11-14T19:00:00Z', null, 'start_only']);
  const half = ev('h1', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.9, longitude: null } });
  const onlyLat = ev('h2', 'culture_roma', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.95, longitude: null } });
  const both = ev('h3', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.901, longitude: 12.5 } });
  const h = mergeDuplicateEvents([half, onlyLat, both]).find((d) => d.content_id === 'h1');
  check('latitude and longitude come from one source, the first that has both',
    [h.event.latitude, h.event.longitude, h.pilot.filled_from['event.latitude'], h.pilot.filled_from['event.longitude']], [41.901, 12.5, 'h3', 'h3']);
  const queued = Object.assign({}, fb, { pilot: Object.assign({}, fb.pilot, { review_pending: true }) });
  const out = mergeDuplicateEvents([queued, web]);
  const q = out.find((d) => d.content_id === 'qn:roma:evt:facebook:5');
  check('an element whose queue row is undecided keeps the fields the reviewer sees',
    [q.event.start_at_utc, q.event.end_at_utc, q.quality.review_flags.includes('merge_deferred')], ['2026-11-14T18:00:00Z', '2026-11-14T18:30:00Z', true]);
  check('and the group is still recorded', out.find((d) => d.content_id === 'qn:roma:evt:web:cccc').pilot.duplicate_of, 'qn:roma:evt:facebook:5');
}

console.log('reruns, order and unforeseen inputs (Codex review of #30)');
{
  check('similarity is the same in both orders (CPython: 0.6923 one way, 0.7692 the other)',
    [similarity(tokens('foxtrot alpha'), tokens('foxtrot opera')), similarity(tokens('foxtrot opera'), tokens('foxtrot alpha'))].map((x) => Math.round(x * 1e6) / 1e6), [0.692308, 0.692308]);
  const x1 = ev('o1', 'web_page', 'foxtrot alpha', '2026-11-14T15:00:00Z');
  const x2 = ev('o2', 'facebook_event', 'foxtrot opera', '2026-11-14T15:00:00Z');
  check('and so is the outcome', [mergeDuplicateEvents([x1, x2]).map((d) => d.pilot.duplicate_of), mergeDuplicateEvents([x2, x1]).map((d) => d.pilot.duplicate_of)], [[undefined, undefined], [undefined, undefined]]);

  const stale = ev('s9', 'facebook_event', 'Il piccolo principe', '2026-11-14T19:30:00Z',
    { pilot: { source_title: 'Il piccolo principe', first_written_at: '2026-11-10T08:00:00Z', duplicate_of: 's8' },
      quality: { requires_review: false, reject_reason: null, review_flags: ['duplicate_suspected'] } });
  const now = ev('s8', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z',
    { pilot: { source_title: 'Il piccolo principe', first_written_at: '2026-11-10T08:00:00Z', duplicates: ['s9'], lead: 's8' } });
  const re = mergeDuplicateEvents([now, stale]);
  check('a pair that no longer matches loses the old links, so the evening show is visible again',
    re.map((d) => [d.pilot.duplicate_of, d.pilot.duplicates, d.quality.review_flags.includes('duplicate_suspected')]), [[undefined, undefined, false], [undefined, undefined, false]]);
  check('and goes to the queue as a doubt', re.map((d) => d.quality.review_flags.includes('duplicate_doubt')), [true, true]);

  const first = mergeDuplicateEvents([
    ev('p1', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: null, longitude: null } }),
    ev('p2', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.9, longitude: 12.5 } })]);
  const second = mergeDuplicateEvents(first);
  check('a rerun keeps the provenance of fields filled on the first run', second.find((d) => d.content_id === 'p1').pilot.filled_from,
    { 'event.latitude': 'p2', 'event.longitude': 'p2' });
  check('and gives the same links', second.map((d) => d.pilot.duplicate_of), first.map((d) => d.pilot.duplicate_of));

  const g1 = ev('c1', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z');
  const g2 = ev('c2', 'facebook_event', 'Il piccolo principe', '2026-11-14T15:00:00Z');
  const g3 = ev('c3', 'facebook_event', 'Il piccolo principe', '2026-11-14T18:00:00Z');
  const grp = mergeDuplicateEvents([g1, g2, g3]);
  check('a doubtful third copy keeps the pair unmerged: the whole group waits',
    grp.map((d) => [d.pilot.duplicate_of, d.quality.review_flags.includes('duplicate_doubt')]), [[undefined, true], [undefined, true], [undefined, true]]);

  const unknown = ev('u9', 'giornale_locale', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  const fbk = ev('u8', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  check('a source with no rank is not merged, it waits',
    mergeDuplicateEvents([unknown, fbk]).map((d) => [d.pilot.duplicate_of, d.quality.review_flags.includes('duplicate_doubt')]), [[undefined, true], [undefined, true]]);

  const thrown = (docs) => { try { mergeDuplicateEvents(docs); return null; } catch (e) { return e.message; } };
  check('a blank source title stops the merge', /b9: pilot\.source_title missing/.test(thrown([ev('b9', 'facebook_event', '   ', '2026-11-14T15:00:00Z')]) || ''), true);
  const bad = (w) => ev('w9', 'facebook_event', 'Festa', '2026-11-14T15:00:00Z', { pilot: { source_title: 'Festa', first_written_at: w } });
  check('30 February is not a first-written time', /w9: pilot\.first_written_at/.test(thrown([bad('2026-02-30T08:00:00Z')]) || ''), true);
  check('nor is hour 99', /w9: pilot\.first_written_at/.test(thrown([bad('2026-11-10T99:99:99Z')]) || ''), true);
  check('a real instant with milliseconds is', thrown([bad('2026-11-10T08:00:00.123Z')]), null);
}

console.log('second Codex review of #30: instants, review state, Roma Today, the link');
{
  const a = ev('t1', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-10T08:00:00.123Z' } });
  const b = ev('t2', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-10T08:00:00Z' } });
  check('first_written_at is compared as an instant: 08:00:00Z is before 08:00:00.123Z', mergeDuplicateEvents([a, b]).find((d) => d.content_id === 't1').pilot.duplicate_of, 't2');

  const m1 = ev('r1', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z');
  const m2 = ev('r2', 'facebook_event', 'Il piccolo principe', '2026-11-14T19:30:00Z');
  const once = mergeDuplicateEvents([m1, m2]);
  check('a doubt the merge raised sets requires_review', once.map((d) => d.quality.requires_review), [true, true]);
  const moved = once.map((d) => (d.content_id === 'r2' ? Object.assign({}, d, { pilot: Object.assign({}, d.pilot, { source_title: 'Torneo di scacchi' }) }) : d));
  check('when the pair is no longer related, the review the merge raised is withdrawn',
    mergeDuplicateEvents(moved).map((d) => [d.quality.requires_review, d.quality.review_flags.includes('duplicate_doubt')]), [[false, false], [false, false]]);
  const other = Object.assign({}, m2, { quality: { requires_review: true, reject_reason: null, review_flags: [] } });
  const kept = mergeDuplicateEvents(mergeDuplicateEvents([m1, other]).map((d) => (d.content_id === 'r2' ? Object.assign({}, d, { pilot: Object.assign({}, d.pilot, { source_title: 'Torneo di scacchi' }) }) : d)));
  check('a review another phase asked for stays', kept.find((d) => d.content_id === 'r2').quality.requires_review, true);
  const geo = { municipality_code: 'V', publication_zone_id: 'centocelle', geo_verification_status: 'human_verified' };
  const hv = ev('g1', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { geography: geo,
    pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-09T08:00:00Z' }, event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: null, longitude: null } });
  const wc = ev('g2', 'culture_roma', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', latitude: 41.9, longitude: 12.5 } });
  const c1 = mergeDuplicateEvents([hv, wc]);
  check('a geography conflict raises a review', c1.find((d) => d.content_id === 'g1').quality.review_flags.includes('geo_verified_conflict'), true);
  const c2 = mergeDuplicateEvents([c1.find((d) => d.content_id === 'g1')]);
  check('and is cleared when the conflict is gone', [c2[0].quality.review_flags.includes('geo_verified_conflict'), c2[0].quality.requires_review], [false, false]);

  const rt1 = ev('qn:roma:evt:rt:b', 'roma_today', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-09T08:00:00Z' }, event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio' } });
  const rt2 = ev('qn:roma:evt:rt:a', 'roma_today', 'Festa di Quartiere 2026', '2026-11-14T15:30:00Z',
    { event: { start_at_utc: '2026-11-14T15:30:00Z', venue: 'Sala Comune Esempio Due', address: 'Via Inventata 1', latitude: 41.9, longitude: 12.5 } });
  const rt = mergeDuplicateEvents([rt1, rt2]).find((d) => d.content_id === 'qn:roma:evt:rt:b');
  check('a Roma Today lead gives the time', rt.event.start_at_utc, '2026-11-14T15:30:00Z');
  check('but no place', [rt.event.venue, rt.event.address, rt.event.latitude], ['Sala Comune Esempio', undefined, undefined]);

  const fbOld = ev('qn:roma:evt:facebook:4', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { pilot: { source_title: 'Festa di Quartiere 2026', first_written_at: '2026-11-09T08:00:00Z' }, event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', booking_url: 'https://esempio.it/fb-biglietti' } });
  const webLead = ev('qn:roma:evt:web:dddd', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', booking_url: 'https://esempio.it/biglietti' } });
  const kept2 = mergeDuplicateEvents([fbOld, webLead]).find((d) => d.content_id === 'qn:roma:evt:facebook:4');
  check('the element keeps its identity and its own source', [kept2.content_id, kept2.source.type], ['qn:roma:evt:facebook:4', 'facebook_event']);
  check('and publishes the lead\'s link and booking link', [kept2.pilot.lead_url, kept2.event.booking_url], ['https://esempio.it/qn:roma:evt:web:dddd', 'https://esempio.it/biglietti']);
  check('a rerun after the pair splits drops the lead link',
    mergeDuplicateEvents([kept2]).map((d) => [d.pilot.lead_url, d.pilot.filled_from && d.pilot.filled_from['pilot.lead_url']]), [[undefined, undefined]]);
}

console.log('third Codex review of #30: long Roman numerals, review ownership, refreshed fields');
{
  check('a Roman numeral of any length is an identifier', [...identifiers('Festival cinema XXVI')], ['xxvi']);
  const e25 = ev('x25', 'web_page', 'Festival cinema XXV', '2026-11-14T15:00:00Z');
  const e26 = ev('x26', 'facebook_event', 'Festival cinema XXVI', '2026-11-14T15:00:00Z');
  check('«XXV» and «XXVI» are two editions, not one', compare(f(e25), f(e26)), 'doubt');

  const m1 = ev('k1', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z',
    { quality: { requires_review: false, reject_reason: null, review_flags: ['identity_from_listing'] } });
  const m2 = ev('k2', 'facebook_event', 'Il piccolo principe', '2026-11-14T19:30:00Z');
  const split = (docs) => docs.map((d) => (d.content_id === 'k2' ? Object.assign({}, d, { pilot: Object.assign({}, d.pilot, { source_title: 'Torneo di scacchi' }) }) : d));
  const once = mergeDuplicateEvents([m1, m2]);
  check('a flag that was already there does not keep the merge\'s review alive',
    mergeDuplicateEvents(split(once)).find((d) => d.content_id === 'k1').quality.requires_review, false);
  const later = once.map((d) => (d.content_id === 'k1' ? Object.assign({}, d, { quality: Object.assign({}, d.quality, { review_flags: d.quality.review_flags.concat('zone_unknown') }) }) : d));
  check('a reason another phase adds afterwards keeps the review',
    mergeDuplicateEvents(split(later)).find((d) => d.content_id === 'k1').quality.requires_review, true);

  const web = ev('w5', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio' } });
  const fb10 = ev('f5', 'facebook_event', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z', { event: { start_at_utc: '2026-11-14T15:00:00Z', venue: 'Sala Comune Esempio', price_text: '10 euro' } });
  const first = mergeDuplicateEvents([web, fb10]);
  check('the first run takes the price from Facebook', first.find((d) => d.content_id === 'w5').event.price_text, '10 euro');
  const changed = first.map((d) => (d.content_id === 'f5' ? Object.assign({}, d, { event: Object.assign({}, d.event, { price_text: '20 euro' }) }) : d));
  const again = mergeDuplicateEvents(changed).find((d) => d.content_id === 'w5');
  check('a rerun takes the donor\'s current value, with its provenance', [again.event.price_text, again.pilot.filled_from['event.price_text']], ['20 euro', 'f5']);
  const alone = mergeDuplicateEvents([first.find((d) => d.content_id === 'w5')])[0];
  check('when the pair splits, a filled field goes back to the element\'s own value', [alone.event.price_text, alone.pilot.filled_from, alone.pilot.native], [null, undefined, undefined]);

  const fbOld = ev('qn:roma:evt:facebook:6', 'facebook_event', 'Il piccolo principe', '2026-11-14T18:00:00Z',
    { pilot: { source_title: 'Il piccolo principe', first_written_at: '2026-11-09T08:00:00Z' }, event: { start_at_utc: '2026-11-14T18:00:00Z', venue: 'Sala Comune Esempio' } });
  const lead = ev('qn:roma:evt:web:eeee', 'web_page', 'Il piccolo principe', '2026-11-14T18:30:00Z', { event: { start_at_utc: '2026-11-14T18:30:00Z', venue: 'Sala Comune Esempio' } });
  const merged = mergeDuplicateEvents([fbOld, lead]).find((d) => d.content_id === 'qn:roma:evt:facebook:6');
  check('the lead\'s time replaces the element\'s', merged.event.start_at_utc, '2026-11-14T18:30:00Z');
  check('and the element\'s own time comes back when the pair splits', mergeDuplicateEvents([merged])[0].event.start_at_utc, '2026-11-14T18:00:00Z');
}

console.log('short identifiers, DEC-025 rule 4');
{
  check('numbers, Roman numerals and single letters are identifiers', [...identifiers('Corso 1 - IX edizione, Sala B')].sort(), ['1', 'b', 'ix']);
  check('one-letter Italian words and elisions are not', [...identifiers("L'arte e i giochi a Roma, c'è posto")], []);
  const at = (id, type, title, venue) => ev(id, type, title, '2026-11-14T17:00:00Z', { event: { start_at_utc: '2026-11-14T17:00:00Z', venue } });
  check('«Corso 1» and «Corso 2» are not merged', compare(f(at('a', 'web_page', 'Corso di ceramica 1', 'Sala Comune Esempio')), f(at('b', 'facebook_event', 'Corso di ceramica 2', 'Sala Comune Esempio'))), 'doubt');
  check('«IX» and «XI» are not merged', compare(f(at('a', 'web_page', 'Rassegna corale IX', 'Sala Comune Esempio')), f(at('b', 'facebook_event', 'Rassegna corale XI', 'Sala Comune Esempio'))), 'doubt');
  check('«Sala A» and «Sala B» are not the same place', compare(f(at('a', 'web_page', 'Laboratorio di ceramica', 'Centro Esempio Sala A')), f(at('b', 'facebook_event', 'Laboratorio di ceramica', 'Centro Esempio Sala B'))), 'doubt');
  check('the same identifiers still merge', compare(f(at('a', 'web_page', 'Corso di ceramica 1', 'Sala Comune Esempio')), f(at('b', 'facebook_event', 'CORSO DI CERAMICA – 1', 'Sala Comune Esempio'))), 'same');
  check('an elision is not an identifier', compare(f(at('a', 'web_page', "L'Open Day della scuola", 'Scuola Esempio')), f(at('b', 'facebook_event', 'Open Day della scuola', 'Scuola Esempio'))), 'same');
}

console.log('precedence inside a rank and whole groups, DEC-025 rules 1 and 4');
{
  check('the organiser site is one rank, read directly or reached through a link', PRECEDENCE, ['web_page', 'culture_roma', 'facebook_event', 'roma_today']);
  const own = ev('qn:roma:evt:web:zzzz', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z');
  const list = ev('qn:roma:evt:web:aaaa', 'web_page', 'Festa di Quartiere 2026', '2026-11-14T15:00:00Z',
    { quality: { requires_review: false, reject_reason: null, review_flags: ['identity_from_listing'] } });
  const out = mergeDuplicateEvents([list, own]);
  check('inside a rank the event\'s own page leads a listing, whatever the content_id', out.find((d) => d.content_id === 'qn:roma:evt:web:aaaa').pilot.duplicate_of, 'qn:roma:evt:web:zzzz');
  check('and the order of arrival does not change it', mergeDuplicateEvents([own, list]).find((d) => d.content_id === 'qn:roma:evt:web:aaaa').pilot.duplicate_of, 'qn:roma:evt:web:zzzz');
  const g1 = ev('g1', 'web_page', 'Il piccolo principe', '2026-11-14T15:00:00Z');
  const g2 = ev('g2', 'facebook_event', 'Il piccolo principe', '2026-11-14T15:40:00Z');
  const g3 = ev('g3', 'facebook_event', 'Il piccolo principe', '2026-11-14T16:20:00Z');
  const chain = mergeDuplicateEvents([g1, g2, g3]);
  check('a chain of same-event pairs whose ends are not the same event is not merged', chain.map((d) => d.pilot.duplicate_of), [undefined, undefined, undefined]);
  check('the whole group goes to the queue', chain.map((d) => [d.quality.review_flags, d.quality.requires_review]),
    [[['duplicate_doubt'], true], [['duplicate_doubt'], true], [['duplicate_doubt'], true]]);
  const noWritten = ev('qn:roma:evt:facebook:7', 'facebook_event', 'Festa', '2026-11-14T15:00:00Z', { pilot: { source_title: 'Festa' } });
  let msg = null; try { mergeDuplicateEvents([noWritten]); } catch (e) { msg = e.message; }
  check('a file without pilot.first_written_at stops the merge and names the file', /qn:roma:evt:facebook:7: pilot\.first_written_at missing/.test(msg || ''), true);
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

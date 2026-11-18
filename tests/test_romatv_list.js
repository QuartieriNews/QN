#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/romatv-list.js: the request of a page of a RomaTV
 * catalogue, what an entry brings, the window, when the reading of a catalogue stops, and the
 * parts of split sittings (docs/pilota/CONTRATTI.md, section 7, «A · Amministrazione», rows Fonti,
 * Raccolta and Registrazione; docs/pilota/WORKSTREAM_A.md, section 5, «Il confine»). Cases
 * T-A2-01…T-A2-04, T-A2-06 and T-A2-13 of WORKSTREAM_A.md, section 6. The n8n adapter is evaluated
 * from the exact committed file. Every guid, title and date is invented (DEC-109).
 *
 * Run:  node tests/test_romatv_list.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'romatv-list.js');
const m = require(FILE);
const src = fs.readFileSync(FILE, 'utf8');

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
const thrown = (fn) => { try { fn(); return null; } catch (e) { return e.message; } };

// Invented guids: a counter in the last group of a UUID shape.
const guid = (n) => `a1b2c3d4-0000-4000-8000-${String(n).padStart(12, '0')}`;
const entry = (o) => Object.assign({
  guid: guid(o.n), title: o.title || `Commissione inventata ${o.n}`, referenceDate: o.ref, insertDate: o.insert || o.ref,
  duration: o.duration || '00:40:00.0000000', contentType: o.ctype || 'Video', tracks: o.tracks || [],
  smilFiles: o.smil === undefined ? [{ smilFileType: 'AudioOnly', url: `https://ovp2-live.akamaized.net/inventato/${o.n}.smil/` }] : o.smil,
}, o.extra || {});
const page = (items, hasNext) => ({ data: { totalCount: 999, hasNext: hasNext !== false, items } });
const NOW = '2026-11-16T10:00:00Z';

console.log('the request of a page');
{
  const r = m.pageRequest('Municipio X', 2, false);
  check('a POST to the API, newest sitting first, one catalogue by name, 100 a page',
    [r.url, r.method, r.body.page, r.body.pageSize, r.body.filters.catalog, r.body.sortBy[0], r.expects],
    [m.API, 'POST', 2, 100, ['Municipio X'], { sortField: 'ReferenceDate', direction: 'Descending' }, 'json']);
  check('no portal headers unless asked', [Object.keys(r.headers).sort(), Object.keys(m.pageRequest('Municipio X', 1, true).headers).sort()],
    [['Accept', 'Content-Type'], ['Accept', 'Content-Type', 'Origin', 'Referer']]);
  check('only the four catalogues', [m.CATALOGS.map((c) => c.catalogo), thrown(() => m.pageRequest('Municipio I', 1))],
    [['Municipio V', 'Municipio X', 'Commissioni Capitoline', 'Assemblee Capitoline'], 'catalog_unknown: Municipio I']);
}

console.log('T-A2-01 — one page of a catalogue');
{
  const speech = [{ trackType: 'SpeechToTextTrack', speechToTextTrackSource: 'https://ac104mp.streamcloud.it/speech/inventato.json',
    speechToTextTrackWebVtt: 'https://streaming.comune.roma.it/webvtt/inventato.vtt' }];
  const e = m.readEntry(entry({ n: 1, title: '  Consiglio inventato  del Municipio ', ref: '2026-11-12T15:30:00+01:00', insert: '2026-11-13T09:00:12.123+01:00',
    duration: '02:25:07.5000000', tracks: speech }), 'Municipio X');
  check('T-A2-01 the guid in lower case, as the reference', m.readEntry(entry({ n: 2, ref: '2026-11-12T10:00:00+01:00', extra: { guid: guid(2).toUpperCase() } }), 'Municipio X').rec.recording_ref,
    `romatv:${guid(2)}`);
  check('T-A2-01 the title as published', e.rec.titolo, '  Consiglio inventato  del Municipio ');
  check('T-A2-01 the reference with its offset, in UTC to the second', [e.rec.ora_riferimento_utc, e.rec.ora_pubblicazione_utc],
    ['2026-11-12T14:30:00Z', '2026-11-13T08:00:12Z']);
  check('T-A2-01 the duration hh:mm:ss.fffffff in whole seconds', e.rec.durata_secondi, 2 * 3600 + 25 * 60 + 7);
  check('T-A2-01 the platform transcript recognised from its track, with its two addresses',
    [e.rec.trascrizione_piattaforma, e.rec.parlato_url, e.rec.vtt_url], [true, speech[0].speechToTextTrackSource, speech[0].speechToTextTrackWebVtt]);
  check('T-A2-01 no transcript track: none', m.readEntry(entry({ n: 3, ref: '2026-11-12T10:00:00+01:00', tracks: [{ trackType: 'VideoTrack' }] }), 'Municipio X').rec.trascrizione_piattaforma, false);
  check('T-A2-01 the audio-only SMIL, without its final slash', e.rec.audio_url, 'https://ovp2-live.akamaized.net/inventato/1.smil');
  check('T-A2-01 a SMIL of another kind is not the audio',
    m.readEntry(entry({ n: 4, ref: '2026-11-12T10:00:00+01:00', smil: [{ smilFileType: 'Video', url: 'https://ovp2-live.akamaized.net/v.smil' }] }), 'Municipio X').rec.audio_url, null);
  check('T-A2-01 the page of a video and of a commission; another content type has none',
    [e.rec.url, m.readEntry(entry({ n: 5, ref: '2026-11-12T10:00:00+01:00', ctype: 'Commission' }), 'Commissioni Capitoline').rec.url,
      m.readEntry(entry({ n: 6, ref: '2026-11-12T10:00:00+01:00', ctype: 'Live' }), 'Municipio X').rec.url],
    [`https://streaming.comune.roma.it/portal/watch/vod/${guid(1)}`, `https://streaming.comune.roma.it/portal/watch/commission/${guid(5)}`, null]);
  check('T-A2-01 an entry without a usable guid, offset or duration is not kept, with its reason',
    [m.readEntry(entry({ n: 7, ref: '2026-11-12T10:00:00+01:00', extra: { guid: `{${guid(7)}}` } }), 'Municipio X').reason,
      m.readEntry(entry({ n: 8, ref: '2026-11-12T10:00:00' }), 'Municipio X').reason,
      m.readEntry(entry({ n: 9, ref: '2026-11-12T10:00:00+01:00', duration: '40 minuti' }), 'Municipio X').reason],
    ['guid_invalid', 'reference_date_invalid', 'duration_invalid']);
  check('T-A2-01 a duration of zero is not yet a recording', m.readEntry(entry({ n: 14, ref: '2026-11-12T10:00:00+01:00', duration: '00:00:00.0000000' }), 'Municipio X').reason,
    'duration_invalid');
  check('T-A2-01 a day that does not exist is refused', m.utcSecond('2026-02-30T10:00:00+01:00'), null);
}

console.log('T-A2-02 — the Municipality from the catalogue');
{
  const x = m.readEntry(entry({ n: 10, title: 'Commissione IV inventata', ref: '2026-11-12T10:00:00+01:00' }), 'Municipio X').rec;
  check('T-A2-02 an entry of «Municipio X» titled «Commissione IV …» is of the X', x.municipality_code, 'X');
  check('T-A2-02 the capitoline catalogues give no Municipality',
    ['Commissioni Capitoline', 'Assemblee Capitoline'].map((c) => m.readEntry(entry({ n: 11, title: 'Commissione V inventata', ref: '2026-11-12T10:00:00+01:00' }), c).rec.municipality_code),
    [null, null]);
  check('T-A2-02 the organ is the portal\'s when it gives one, else the title without its part, as published',
    [m.readEntry(entry({ n: 12, ref: '2026-11-12T10:00:00+01:00', title: 'x', extra: { governmentBody: ' Consiglio inventato ' } }), 'Municipio V').rec.organo,
      m.readEntry(entry({ n: 13, ref: '2026-11-12T10:00:00+01:00', title: 'Consiglio Inventato del 9/11 - parte II' }), 'Municipio V').rec.organo,
      m.readEntry(entry({ n: 15, ref: '2026-11-12T10:00:00+01:00', title: 'Consiglio Inventato (parte III)' }), 'Municipio V').rec.organo],
    ['Consiglio inventato', 'Consiglio Inventato del 9/11', 'Consiglio Inventato']);
  check('T-A2-02 its key is folded, for the binding of parts',
    m.readEntry(entry({ n: 16, ref: '2026-11-12T10:00:00+01:00', title: 'Consiglio Inventato - parte II' }), 'Municipio V').rec.organo_chiave, 'consiglioinventato');
}

console.log('T-A2-03 — the first day');
check('T-A2-03 a sitting at 00:30 of 1 November in Rome enters', m.inWindow(m.utcSecond('2026-11-01T00:30:00+01:00'), NOW), true);
check('T-A2-03 the same instant written in UTC enters', m.inWindow('2026-10-31T23:30:00Z', NOW), true);
check('T-A2-03 a sitting of 31 October in Rome does not', m.inWindow(m.utcSecond('2026-10-31T23:30:00+01:00'), NOW), false);

console.log('T-A2-04 — the window of 100 days');
{
  const late = '2027-03-01T10:00:00Z';
  const daysBefore = (d) => new Date(Date.parse(late) - d * 86400000).toISOString().slice(0, 19) + 'Z';
  check('T-A2-04 a late publication enters at 51 and at 94 days from the sitting, not at 101',
    [m.inWindow(daysBefore(51), late), m.inWindow(daysBefore(94), late), m.inWindow(daysBefore(100), late), m.inWindow(daysBefore(101), late)],
    [true, true, true, false]);
  const r = m.readPage(m.startReading('Municipio V'), page([
    entry({ n: 20, ref: '2026-11-15T10:00:00+01:00' }), entry({ n: 21, ref: '2026-11-02T10:00:00+01:00' }),
    entry({ n: 22, ref: '2026-10-30T10:00:00+01:00' }), entry({ n: 23, ref: '2026-11-03T10:00:00+01:00' }),
  ]), NOW);
  check('T-A2-04 the pages stop at the first entry of a sitting outside the window',
    [r.records.map((x) => x.recording_ref.slice(-2)), r.done, r.complete, r.reason, r.next_page], [['20', '21'], true, true, 'left the window', null]);
  const keep = m.readPage(m.startReading('Municipio V'), page([entry({ n: 24, ref: '2026-11-15T10:00:00+01:00', extra: { guid: 'x' } }), entry({ n: 25, ref: '2026-11-14T10:00:00+01:00' })]), NOW);
  check('T-A2-04 an entry that cannot be kept is listed and the page goes on', [keep.skipped, keep.records.length, keep.next_page],
    [[{ guid: 'x', reason: 'guid_invalid' }], 1, 2]);
  const end = m.readPage(m.startReading('Municipio V'), page([entry({ n: 26, ref: '2026-11-15T10:00:00+01:00' })], false), NOW);
  check('T-A2-04 the end of the catalogue inside the window is a complete reading', [end.complete, end.reason], [true, 'end of the catalogue']);
  const twice = m.readPage(m.startReading('Municipio V'), page([entry({ n: 27, ref: '2026-11-15T10:00:00+01:00' }), entry({ n: 27, ref: '2026-11-15T10:00:00+01:00' })]), NOW);
  check('T-A2-04 the same entry twice in a page is kept once, the other listed',
    [twice.records.length, twice.skipped, twice.done], [1, [{ guid: guid(27), reason: 'repeated in the page' }], false]);
  check('T-A2-04 a now that is not an instant is an error, never an empty window',
    [thrown(() => m.readPage(m.startReading('Municipio V'), page([]), undefined)), thrown(() => m.inWindow('2026-11-15T10:00:00Z', '16/11/2026'))],
    ['now must be a UTC instant', 'now must be a UTC instant']);
}

console.log('T-A2-13 — the cap of the pages');
{
  let r = m.startReading('Commissioni Capitoline');
  const day = (d, n) => entry({ n, ref: `2026-11-${String(d).padStart(2, '0')}T10:00:00+01:00` });
  const requests = [];
  for (let p = 1; !r.done; p++) {
    requests.push(m.pageRequest(r.catalogo, r.next_page).body.page);
    r = m.readPage(r, page([day(16 - p, p * 10), day(16 - p, p * 10 + 1)]), NOW);
  }
  check('T-A2-13 four pages without leaving the window: incomplete, never a fifth request',
    [requests, r.complete, r.reason, r.next_page], [[1, 2, 3, 4], false, '4 pages without leaving the window', null]);
  check('T-A2-13 a fifth page cannot be asked', thrown(() => m.pageRequest('Commissioni Capitoline', 5)), 'page_invalid');
  check('T-A2-13 a reading that is done reads no other page', thrown(() => m.readPage(r, page([]), NOW)), 'reading_done');
  const one = m.readPage(m.startReading('Municipio X'), page([day(15, 100), day(14, 101)]), NOW);
  const rep = m.readPage(one, page([day(13, 101), day(12, 102)]), NOW);
  check('T-A2-13 a page that repeats an entry already read stops the catalogue, incomplete',
    [rep.complete, rep.reason, rep.records.length], [false, 'page 2 repeats entries already read in this run', 2]);
  const rise = m.readPage(one, page([day(15, 103), day(10, 104)]), NOW);
  check('T-A2-13 dates that rise from one page to the next stop it, incomplete',
    [rise.complete, rise.reason, rise.records.length], [false, 'the dates of the sittings rise from page 1 to page 2', 2]);
  check('T-A2-13 an answer without its list stops it, incomplete', m.readPage(m.startReading('Municipio X'), { error: 'x' }, NOW).reason,
    'answer without a list of entries');
  check('T-A2-13 an empty first page stops it, incomplete, even if the portal says it is the end',
    [m.readPage(m.startReading('Municipio X'), page([], false), NOW).reason, m.readPage(m.startReading('Municipio X'), page([]), NOW).complete],
    ['empty first page', false]);
  check('T-A2-13 an empty page with more to come stops it, incomplete; with no more, it is the end',
    [m.readPage(one, page([]), NOW).reason, m.readPage(one, page([], false), NOW).complete], ['empty page 2 with more to come', true]);
  const failed = m.readFailure(one, { outcome: 'server_error', reason: 'HTTP 503' });
  check('T-A2-13 a page not read stops the catalogue, incomplete, with the verdict', [failed.complete, failed.reason, failed.records.length],
    [false, 'page 2 not read: server_error (HTTP 503)', 2]);
  // The run goes on with the next catalogue: its reading starts on its own.
  const other = m.readPage(m.startReading('Assemblee Capitoline'), page([day(15, 105)], false), NOW);
  check('T-A2-13 a catalogue stopped does not stop the next one: its reading starts on its own', [rep.done, other.complete, other.records.length], [true, true, 1]);
}

console.log('T-A2-06 — split sittings');
{
  const rec = (n, title, ref, dur, extra) => m.readEntry(entry({ n, title, ref, duration: dur || '01:00:00.0000000', extra }), 'Municipio V').rec;
  check('T-A2-06 the forms of a declared part',
    ['Consiglio inventato parte 1', 'Consiglio inventato - I parte', 'Consiglio inventato seconda parte', 'Consiglio inventato (parte III)',
      'Consiglio inventato 2ª parte', 'Commissione IV inventata', 'Consiglio inventato'].map((t) => m.partOf(t).part),
    [1, 1, 2, 3, 2, null, null]);
  check('T-A2-06 the part goes, the organ stays: the Roman numeral of a commission is not a part',
    [m.partOf('Commissione IV inventata - parte 2').base, m.partOf('Commissione IV inventata').base], ['commissioneivinventata', 'commissioneivinventata']);
  const sp1 = rec(40, 'Commissione Lavori / Mobilità dell\'Ente - parte 1', '2026-11-09T15:00:00+01:00', '01:00:00.0000000');
  const sp2 = rec(41, 'COMMISSIONE lavori Mobilità dell’ Ente – parte 2', '2026-11-09T16:05:00+01:00');
  check('T-A2-06 the same organ written with other capitals, spaces or punctuation is the same organ: its parts are bound',
    [sp1.organo_chiave === sp2.organo_chiave, m.linkParts([sp1, sp2]).links, m.linkParts([sp1, sp2]).unbound],
    [true, { [sp2.recording_ref]: { parte_precedente: sp1.recording_ref, prima_parte: sp1.recording_ref } }, []]);
  check('T-A2-06 another word is another organ', m.partOf('Commissione Lavori e Mobilità - parte 2').base === sp1.organo_chiave, false);
  const p1 = rec(30, 'Consiglio inventato parte 1', '2026-11-09T09:00:00+01:00', '01:00:00.0000000');
  const p2 = rec(31, 'Consiglio inventato parte 2', '2026-11-09T10:05:00+01:00', '01:00:00.0000000');
  const p3 = rec(32, 'Consiglio inventato terza parte', '2026-11-09T11:10:00+01:00');
  const bound = m.linkParts([p3, p1, p2]);
  check('T-A2-06 parts declared by the titles, in order and without overlap, are bound',
    bound.links, { [p2.recording_ref]: { parte_precedente: p1.recording_ref, prima_parte: p1.recording_ref },
      [p3.recording_ref]: { parte_precedente: p2.recording_ref, prima_parte: p1.recording_ref } });
  check('T-A2-06 and nothing is left unbound', bound.unbound, []);
  const a = rec(33, 'Commissione inventata', '2026-11-09T13:00:00+01:00', '01:08:00.0000000');
  const b = rec(34, 'Commissione inventata', '2026-11-09T14:00:00+01:00');
  const plain = m.linkParts([a, b]);
  check('T-A2-06 two recordings of the same organ and day without declared parts stay apart, listed',
    [plain.links, plain.unbound], [{}, [{ refs: [a.recording_ref, b.recording_ref].sort(), reason: 'no part declared' }]]);
  const o1 = rec(35, 'Commissione inventata parte 1', '2026-11-09T13:00:00+01:00', '01:08:00.0000000');
  const o2 = rec(36, 'Commissione inventata parte 2', '2026-11-09T14:00:00+01:00');
  const over = m.linkParts([o1, o2]);
  check('T-A2-06 two parts that overlap stay apart, listed',
    [over.links, over.unbound], [{}, [{ refs: [o2.recording_ref], reason: 'part 2 starts before part 1 ends' }]]);
  const s2 = rec(37, 'Assemblea inventata seconda parte', '2026-11-10T15:00:00+01:00');
  check('T-A2-06 a «seconda parte» without the first stands alone, listed',
    m.linkParts([s2]), { records: [s2], links: {}, unbound: [{ refs: [s2.recording_ref], reason: 'part 2 without part 1 before it' }], duplicates: [] });
  const q1 = rec(38, 'Consiglio inventato parte 1', '2026-11-11T09:00:00+01:00');
  const q3 = rec(39, 'Consiglio inventato parte 3', '2026-11-11T12:00:00+01:00');
  check('T-A2-06 a number missing breaks the chain', m.linkParts([q1, q3]).unbound, [{ refs: [q3.recording_ref], reason: 'part 3 without part 2 before it' }]);
  const d1 = rec(40, 'Consiglio inventato parte 1', '2026-11-12T09:00:00+01:00');
  const d2 = rec(41, 'Consiglio inventato parte 1', '2026-11-12T11:00:00+01:00');
  check('T-A2-06 a part declared twice binds nothing', [m.linkParts([d1, d2]).links, m.linkParts([d1, d2]).unbound],
    [{}, [{ refs: [d1.recording_ref, d2.recording_ref].sort(), reason: 'part 1 declared twice' }]]);
  const other = rec(42, 'Consiglio inventato parte 2', '2026-11-10T10:05:00+01:00');
  check('T-A2-06 another day of Rome is another sitting', m.linkParts([p1, other]).links, {});
  const cap = m.readEntry(entry({ n: 43, title: 'Consiglio inventato parte 2', ref: '2026-11-09T10:05:00+01:00' }), 'Commissioni Capitoline').rec;
  check('T-A2-06 another catalogue is another sitting', m.linkParts([p1, cap]).links, {});
  check('T-A2-06 one recording with its first part alone needs no link', m.linkParts([p1]), { records: [p1], links: {}, unbound: [], duplicates: [] });
  const twice = m.linkParts([p1, cap, p1]);
  check('a recording twice in the run, from a page or two catalogues, is kept once and listed', [twice.records.length, twice.duplicates], [2, [p1.recording_ref]]);
  const video = { recording_ref: 'youtube:Vid00000001', ora_riferimento_utc: '2026-11-09T10:00:00Z', numero_parte: null };
  check('a video of YouTube is never bound, and never listed as unbound', [m.linkParts([video, Object.assign({}, video, { recording_ref: 'youtube:Vid00000002' })]).unbound], [[]]);
}

console.log('the n8n adapter');
function runNode(json) {
  return new Function('$input', '$json', 'require', 'URL', 'URLSearchParams', 'process', 'module', src)(
    { item: { json } }, json, require, undefined, undefined, undefined, undefined);
}
{
  const a = runNode({ stage: 'request', catalogo: 'Municipio V', portal_headers: false });
  check('request: a new reading starts at page 1', [a.json.reading.next_page, a.json.request.body.page], [1, 1]);
  const b = runNode({ stage: 'page', reading: a.json.reading, now: NOW, verdict: { outcome: 'ok', reason: null },
    answer: { statusCode: 200, body: page([entry({ n: 50, ref: '2026-11-15T10:00:00+01:00' })]) } });
  check('page: the reading moves on to page 2', [b.json.reading.next_page, b.json.reading.records.length], [2, 1]);
  const c = runNode({ stage: 'request', reading: b.json.reading });
  check('request: the next page of the same reading', c.json.request.body.page, 2);
  const skipped = runNode({ stage: 'page', reading: b.json.reading, now: NOW, verdict: { outcome: 'skipped', reason: 'host stopped', host_stopped: true }, answer: null });
  check('page: a request that did not bring a page stops the reading with its verdict, not as an answer without a list',
    [skipped.json.reading.complete, skipped.json.reading.reason, skipped.json.reading.host_stopped], [false, 'page 2 not read: skipped (host stopped)', true]);
  const d = runNode({ stage: 'links', records: b.json.reading.records });
  check('links: the records once, links and unbound', [d.json.records.length, d.json.links, d.json.unbound], [1, {}, []]);
  check('an unknown stage fails', thrown(() => runNode({ stage: 'x' })), 'romatv-list.js: unknown stage "x"');
}

console.log('what the node may use inside n8n');
const code = src.replace(/\/\*[\s\S]*?\*\/|\/\/.*$/gm, '');
check('no URL global', /\bURL\b|URLSearchParams/.test(code), false);
check('no process', /\bprocess\b/.test(code), false);
check('no module required', code.match(/require\('[^']+'\)/g), null);

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

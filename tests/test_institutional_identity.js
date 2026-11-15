#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/institutional-identity.js: the recording reference and
 * its file name, the content_id and file name of a fact, source_channel and source_id, the
 * UTC instant and the duration, and the source_hash in the form of Spec v2.5 Phase 2.2
 * (docs/pilota/CONTRATTI.md, section 7, «A · Amministrazione»). Cases T-A1-01…T-A1-19, the ids
 * of PR A1 in the scheme of docs/pilota/WORKSTREAM_A.md, section 6.
 * The n8n adapter is evaluated from the exact committed file with stubbed $input/$json/require.
 * Every guid, video id, channel id and title is invented (DEC-109, DEC-031 point 4).
 *
 * Run:  node tests/test_institutional_identity.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const FILE = path.join(__dirname, '..', 'code-nodes', 'institutional-identity.js');
const m = require(FILE);
const spec22 = require(path.join(__dirname, '..', 'code-nodes', 'compute-source-hash.js'));

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

const sha256 = (t) => crypto.createHash('sha256').update(t, 'utf8').digest('hex');

// Invented identifiers: a UUID-shaped guid, an 11-character video id, a channel id of UC + 22.
const GUID = '3f2a9c4e-7b1d-4e8a-9c2f-0a1b2c3d4e5f';
const GUID_2 = '0d9e8f7a-6b5c-4d3e-8f2a-1b0c9d8e7f6a';
const VIDEO = 'Ab3_-xY9zQ0';
const CHANNEL = 'UCabcdefghijKLMNOPQRST_-';
const REF = `romatv:${GUID}`;
const YT_REF = `youtube:${VIDEO}`;
const TEXT_HASH = sha256('Testo inventato della seduta aperta.');
const FIELDS = {
  recording_ref: REF,
  title: 'Commissione inventata, seduta di prova',
  reference_at: '2026-11-13T12:40:00+01:00',
  duration_s: '00:45:10.5000000',
  transcript_source: 'asr:gpt-4o-mini-transcribe',
  transcript_sha256: TEXT_HASH,
};
const KEY = sha256(REF).slice(0, 16);

console.log('T-A1-01 — content_id form (CONTRATTI section 7 A, row Identità)');
check('T-A1-01 the key is the first 16 hex of the SHA-256 of the reference', m.keyOf(REF), KEY);
check('T-A1-01 content_id = qn:roma:ins:<key>-f<n>', m.contentId(REF, 1), `qn:roma:ins:${KEY}-f1`);
check('T-A1-01 the form', /^qn:roma:ins:[0-9a-f]{16}-f[1-9][0-9]*$/.test(m.contentId(REF, 7)), true);
check('T-A1-01 -f<n> is always there, -f1 included', m.contentId(REF, 1).endsWith('-f1'), true);
check('T-A1-01 two facts of one recording share the key and differ by n',
  [m.contentId(REF, 2).slice(0, -3), m.contentId(REF, 3).slice(0, -3), m.contentId(REF, 2) !== m.contentId(REF, 3)],
  [`qn:roma:ins:${KEY}`, `qn:roma:ins:${KEY}`, true]);
check('T-A1-01 another recording is another key', m.keyOf(`romatv:${GUID_2}`) !== KEY, true);
check('T-A1-01 a YouTube recording has its own key', m.contentId(YT_REF, 1), `qn:roma:ins:${sha256(YT_REF).slice(0, 16)}-f1`);

console.log('T-A1-02 — file names (rows File and Registrazione)');
check('T-A1-02 the element file follows the content_id', m.fileName(m.contentId(REF, 4)), `roma__ins__${KEY}-f4.json`);
check('T-A1-02 the file name is the content_id without qn:, colons as __',
  m.fileName(m.contentId(REF, 12)), m.contentId(REF, 12).replace(/^qn:/, '').split(':').join('__') + '.json');
check('T-A1-02 the RomaTV record file', m.recordingFileName(REF), `romatv__${GUID}.json`);
check('T-A1-02 the YouTube record file', m.recordingFileName(YT_REF), `youtube__${VIDEO}.json`);
check('T-A1-02 the record file of an uppercase reference is the lowercase one',
  m.recordingFileName(`romatv:${GUID.toUpperCase()}`), `romatv__${GUID}.json`);
for (const bad of [`qn:roma:nws:${KEY}-f1`, `qn:roma:ins:${KEY}`, `qn:roma:ins:${KEY}-f0`, `qn:roma:ins:${KEY}-f01`,
  `qn:roma:ins:${KEY.toUpperCase()}-f1`, `qn:roma:ins:${KEY.slice(1)}-f1`, `qn:roma:ins:${KEY}-f99999999999999999`, 7, null]) {
  check(`T-A1-02 no file name for ${JSON.stringify(bad)}`, thrown(() => m.fileName(bad)), 'content_id_invalid');
}

console.log('T-A1-03 — recording reference: canonical form');
check('T-A1-03 RomaTV: romatv:<guid>', m.recordingRef('romatv', GUID), REF);
check('T-A1-03 a guid in uppercase is written in lowercase', m.recordingRef('romatv', GUID.toUpperCase()), REF);
check('T-A1-03 mixed case too', m.recordingRef('romatv', '3F2a9C4e-7B1d-4E8a-9C2f-0A1b2C3d4E5f'), REF);
check('T-A1-03 one recording, one key, whatever the case of its guid',
  m.keyOf(`romatv:${GUID.toUpperCase()}`), KEY);
check('T-A1-03 YouTube: youtube:<id>', m.recordingRef('youtube', VIDEO), YT_REF);
check('T-A1-03 a YouTube id keeps its case: another case is another video',
  m.recordingRef('youtube', VIDEO.toLowerCase()) !== YT_REF, true);
check('T-A1-03 _ and - are id characters', m.recordingRef('youtube', '-_aaaaaaaaa'), 'youtube:-_aaaaaaaaa');
check('T-A1-03 canonicalRef reads a stored reference back', m.canonicalRef(`romatv:${GUID.toUpperCase()}`), REF);

console.log('T-A1-04 — recording reference: refusals');
for (const [label, id] of [['braces', `{${GUID}}`], ['urn prefix', `urn:uuid:${GUID}`], ['no hyphens', GUID.replace(/-/g, '')],
  ['one digit short', GUID.slice(1)], ['a non-hex digit', GUID.replace('f', 'g')], ['spaces around', ` ${GUID} `],
  ['hyphens moved', '3f2a9c4e7-b1d-4e8a-9c2f-0a1b2c3d4e5f'], ['empty', ''], ['a number', 42], ['absent', undefined]]) {
  check(`T-A1-04 RomaTV guid refused: ${label}`, thrown(() => m.recordingRef('romatv', id)), 'guid_invalid');
}
for (const [label, id] of [['10 characters', VIDEO.slice(1)], ['12 characters', VIDEO + 'a'], ['a dot', 'Ab3.-xY9zQ0'],
  ['a space', 'Ab3 -xY9zQ0'], ['a watch URL', `https://www.youtube.com/watch?v=${VIDEO}`], ['absent', null]]) {
  check(`T-A1-04 YouTube id refused: ${label}`, thrown(() => m.recordingRef('youtube', id)), 'video_id_invalid');
}
for (const p of ['RomaTV', 'YOUTUBE', 'facebook', '', undefined, 'toString', '__proto__']) {
  check(`T-A1-04 platform refused: ${JSON.stringify(p)}`, thrown(() => m.recordingRef(p, GUID)), 'platform_invalid');
}
for (const ref of [GUID, `RomaTV:${GUID}`, `romatv:{${GUID}}`, `romatv: ${GUID}`, `youtube:${VIDEO}x`, `vimeo:${VIDEO}`,
  `romatv:${GUID}\n`, '', null, 12]) {
  check(`T-A1-04 no key from ${JSON.stringify(ref)}`, thrown(() => m.keyOf(ref)), 'ref_invalid');
}

console.log('T-A1-05 — n: the place of the fact, an integer from 1');
check('T-A1-05 n = 1', m.contentId(REF, 1).endsWith('-f1'), true);
check('T-A1-05 any whole n, 100 and beyond too', m.contentId(REF, 120), `qn:roma:ins:${KEY}-f120`);
for (const n of [0, -1, -0, 1.5, '2', '1', NaN, Infinity, null, undefined, 2 ** 53, [1], true]) {
  check(`T-A1-05 n refused: ${Object.is(n, -0) ? '-0' : String(n)} (${typeof n})`, thrown(() => m.contentId(REF, n)), 'n_invalid');
}
check('T-A1-05 a bad reference is refused before any id', thrown(() => m.contentId(`romatv:${GUID}x`, 1)), 'ref_invalid');

console.log('T-A1-06 — geography and registro_id never enter the id');
check('T-A1-06 contentId reads two arguments: the reference and n', m.contentId.length, 2);
check('T-A1-06 anything else passed is ignored',
  m.contentId(REF, 3, { publication_zone_id: 'zona-inventata', municipality_code: 'V', registro_id: 'S-0000' }),
  m.contentId(REF, 3));
check('T-A1-06 the key reads the reference alone', m.keyOf.length, 1);

console.log('T-A1-07 — source_channel and source_id (row Colonne della coda)');
check('T-A1-07 source_channel of RomaTV', m.sourceChannel('romatv'), 'inst_romatv');
check('T-A1-07 source_channel of YouTube', m.sourceChannel('youtube'), 'inst_youtube');
check('T-A1-07 source_id of RomaTV is the portal host', m.sourceId('romatv'), 'streaming.comune.roma.it');
check('T-A1-07 whatever channel id comes with it', m.sourceId('romatv', CHANNEL), m.ROMATV_HOST);
check('T-A1-07 source_id of YouTube is the channel id, as given', m.sourceId('youtube', CHANNEL), CHANNEL);
for (const [label, c] of [['21 characters after UC', CHANNEL.slice(0, -1)], ['23 characters after UC', CHANNEL + 'a'],
  ['lowercase uc', 'uc' + CHANNEL.slice(2)], ['a handle', '@canale-inventato'], ['absent', undefined],
  ['a channel URL', `https://www.youtube.com/channel/${CHANNEL}`]]) {
  check(`T-A1-07 YouTube channel id refused: ${label}`, thrown(() => m.sourceId('youtube', c)), 'channel_id_invalid');
}
check('T-A1-07 unknown platform', [thrown(() => m.sourceChannel('web')), thrown(() => m.sourceId('web', CHANNEL))],
  ['platform_invalid', 'platform_invalid']);

console.log('T-A1-08 — UTC to the second');
check('T-A1-08 the RomaTV form with +01:00', m.toUtcSecond('2026-11-13T12:40:00+01:00'), '2026-11-13T11:40:00Z');
check('T-A1-08 Z stays as it is', m.toUtcSecond('2026-11-13T11:40:00Z'), '2026-11-13T11:40:00Z');
check('T-A1-08 Z with milliseconds: the fraction goes', m.toUtcSecond('2026-11-13T11:40:00.987Z'), '2026-11-13T11:40:00Z');
check('T-A1-08 seven decimals too', m.toUtcSecond('2026-11-13T12:40:59.9999999+01:00'), '2026-11-13T11:40:59Z');
check('T-A1-08 minutes without seconds', m.toUtcSecond('2026-11-13T12:40+01:00'), '2026-11-13T11:40:00Z');
check('T-A1-08 an offset without colon', m.toUtcSecond('2026-11-13T12:40:00+0100'), '2026-11-13T11:40:00Z');
check('T-A1-08 a negative offset', m.toUtcSecond('2026-11-13T06:40:00-05:00'), '2026-11-13T11:40:00Z');
check('T-A1-08 an offset in minutes', m.toUtcSecond('2026-11-13T17:10:00+05:30'), '2026-11-13T11:40:00Z');
check('T-A1-08 the Rome day and the UTC day can differ (the start of 1 November)',
  m.toUtcSecond('2026-11-01T00:30:00+01:00'), '2026-10-31T23:30:00Z');
check('T-A1-08 across the end of a year', m.toUtcSecond('2027-01-01T00:15:00+01:00'), '2026-12-31T23:15:00Z');
check('T-A1-08 the same as the timestamp rule of compute-source-hash.js',
  ['2026-11-13T12:40:00+01:00', '2026-11-13T11:40:00.987Z', '2026-10-25T02:30:00+02:00'].map(m.toUtcSecond),
  ['2026-11-13T12:40:00+01:00', '2026-11-13T11:40:00.987Z', '2026-10-25T02:30:00+02:00'].map((v) => spec22.hashInputValue('start_at_utc', v)));

console.log('T-A1-09 — UTC across the last Sunday of October (25 October 2026)');
check('T-A1-09 the day before, summer time', m.toUtcSecond('2026-10-24T12:40:00+02:00'), '2026-10-24T10:40:00Z');
check('T-A1-09 the day after, winter time', m.toUtcSecond('2026-10-26T12:40:00+01:00'), '2026-10-26T11:40:00Z');
check('T-A1-09 02:30 in Rome happens twice: first with +02:00', m.toUtcSecond('2026-10-25T02:30:00+02:00'), '2026-10-25T00:30:00Z');
check('T-A1-09 then with +01:00, an hour later', m.toUtcSecond('2026-10-25T02:30:00+01:00'), '2026-10-25T01:30:00Z');
check('T-A1-09 the last spring change too (29 March 2026)', m.toUtcSecond('2026-03-29T03:30:00+02:00'), '2026-03-29T01:30:00Z');

console.log('T-A1-10 — UTC: refusals');
for (const v of ['2026-11-13T12:40:00', '2026-11-13 12:40:00+01:00', '2026-11-13', '2026-02-30T10:00:00Z',
  '2026-11-13T24:00:00Z', '2026-11-13T12:60:00Z', '2026-11-13T12:40:60Z', '2026-11-13T12:40:00+24:00',
  '2026-11-13T12:40:00+01:60', '2026-11-13t12:40:00z', ' 2026-11-13T12:40:00Z', '13/11/2026 12:40', '', null, 1763034000000]) {
  check(`T-A1-10 refused: ${JSON.stringify(v)}`, thrown(() => m.toUtcSecond(v)), 'time_invalid');
}
check('T-A1-10 29 February of a leap year is a day', m.toUtcSecond('2028-02-29T10:00:00Z'), '2028-02-29T10:00:00Z');

console.log('T-A1-11 — duration in whole seconds');
check('T-A1-11 the RomaTV form', m.durationSeconds('02:25:13.1234567'), 2 * 3600 + 25 * 60 + 13);
check('T-A1-11 rounded down, never up', m.durationSeconds('00:45:10.9999999'), 2710);
check('T-A1-11 without a fraction', m.durationSeconds('00:45:10'), 2710);
check('T-A1-11 a plain number', m.durationSeconds(2710), 2710);
check('T-A1-11 a plain number with a fraction, rounded down', m.durationSeconds(2710.99), 2710);
check('T-A1-11 a string of digits', m.durationSeconds('2710'), 2710);
check('T-A1-11 zero', [m.durationSeconds(0), m.durationSeconds('00:00:00.0000000')], [0, 0]);
for (const v of ['2:25:13', '02:60:00', '02:25:60', '1.02:25:13', '02:25:13.12345678', '-00:00:01', -1, NaN, Infinity,
  '1e3', ' 2710', '', null, undefined, {}, 2 ** 60]) {
  check(`T-A1-11 refused: ${String(v)} (${typeof v})`, thrown(() => m.durationSeconds(v)), 'duration_invalid');
}

console.log('T-A1-12 — source_hash: the form of Spec v2.5 Phase 2.2, not the bare hex of B');
const H = m.sourceHash(FIELDS);
check('T-A1-12 sha256:<64 hex>', /^sha256:[0-9a-f]{64}$/.test(H), true);
check('T-A1-12 not the bare form of news-identity.js', /^[0-9a-f]{64}$/.test(H), false);
check('T-A1-12 the hash of the JSON of the ordered pair array', H, 'sha256:' + sha256(JSON.stringify([
  ['recording_ref', REF], ['title', FIELDS.title], ['reference_at', '2026-11-13T11:40:00Z'], ['duration_s', '2710'],
  ['transcript_source', 'asr:gpt-4o-mini-transcribe'], ['transcript_sha256', TEXT_HASH]])));
check('T-A1-12 the pair array, never an object', m.buildHashInput(FIELDS).every((p) => Array.isArray(p) && p.length === 2), true);
check('T-A1-12 the fields and their order', m.HASH_FIELDS,
  ['recording_ref', 'title', 'reference_at', 'duration_s', 'transcript_source', 'transcript_sha256']);
check('T-A1-12 the same `sha256:` prefix as compute-source-hash.js', H.slice(0, 7), spec22.computeSourceHash({}).slice(0, 7));
check('T-A1-12 the same form as compute-source-hash.js: sha256: and 64 lowercase hex',
  [H, spec22.computeSourceHash({})].map((h) => /^sha256:[0-9a-f]{64}$/.test(h)), [true, true]);

console.log('T-A1-13 — normalisation');
const with_ = (o) => m.sourceHash(Object.assign({}, FIELDS, o));
check('T-A1-13 spaces at the edges and inside the title', with_({ title: '  Commissione   inventata,\tseduta\ndi prova ' }), H);
check('T-A1-13 NFC: a decomposed accent is the composed one',
  with_({ title: 'Seduta di prova sulla città' }), with_({ title: 'Seduta di prova sulla città' }));
check('T-A1-13 the string rule is the one of compute-source-hash.js',
  ['  a   b\n', 'é', '\t'].map(m.canonicalText), ['  a   b\n', 'é', '\t'].map((v) => spec22.hashInputValue('event_name', v)));
check('T-A1-13 the same instant with Z or with its offset', with_({ reference_at: '2026-11-13T11:40:00Z' }), H);
check('T-A1-13 the same duration as a number, as digits or as RomaTV writes it',
  [with_({ duration_s: 2710 }), with_({ duration_s: '2710' }), with_({ duration_s: '00:45:10' })], [H, H, H]);
check('T-A1-13 the reference in uppercase', with_({ recording_ref: `romatv:${GUID.toUpperCase()}` }), H);
check('T-A1-13 the transcript digest in uppercase', with_({ transcript_sha256: TEXT_HASH.toUpperCase() }), H);
check('T-A1-13 a changed title changes the hash', with_({ title: 'Altra commissione inventata' }) !== H, true);
check('T-A1-13 a changed text changes the hash', with_({ transcript_sha256: sha256('Altro testo inventato.') }) !== H, true);
check('T-A1-13 another transcript source changes the hash', with_({ transcript_source: 'asr:whisper-1' }) !== H, true);
check('T-A1-13 another duration changes the hash', with_({ duration_s: 2711 }) !== H, true);
check('T-A1-13 another instant changes the hash', with_({ reference_at: '2026-11-13T12:41:00+01:00' }) !== H, true);

console.log('T-A1-14 — null is the empty string');
for (const f of ['title', 'reference_at', 'duration_s', 'transcript_source', 'transcript_sha256']) {
  const nul = with_({ [f]: null });
  check(`T-A1-14 ${f}: null, absent, empty and blank hash alike`,
    [m.sourceHash(Object.assign({}, FIELDS, { [f]: undefined })), with_({ [f]: '' }), with_({ [f]: '  ' })], [nul, nul, nul]);
}
check('T-A1-14 the hash input of an absent field is the empty string',
  m.buildHashInput({ recording_ref: REF }), m.HASH_FIELDS.map((f) => [f, f === 'recording_ref' ? REF : '']));
check('T-A1-14 a duration of 0 is a value, not an absence', with_({ duration_s: 0 }) !== with_({ duration_s: null }), true);
check('T-A1-14 the reference is never absent: null and empty are refused alike',
  [thrown(() => with_({ recording_ref: null })), thrown(() => with_({ recording_ref: '' })), thrown(() => m.sourceHash({}))],
  ['ref_invalid', 'ref_invalid', 'ref_invalid']);

console.log('T-A1-15 — the order of the fields matters');
{
  check('T-A1-15 the module emits the pairs in the contract order', m.buildHashInput(FIELDS).map(([k]) => k),
    ['recording_ref', 'title', 'reference_at', 'duration_s', 'transcript_source', 'transcript_sha256']);
  check('T-A1-15 the order of the keys of the input object takes no part',
    m.sourceHash({ transcript_sha256: TEXT_HASH, transcript_source: FIELDS.transcript_source, duration_s: FIELDS.duration_s,
      reference_at: FIELDS.reference_at, title: FIELDS.title, recording_ref: REF }), H);
  check('T-A1-15 the fields stay apart: text moved between two fields changes the hash',
    with_({ title: 'asr:whisper-1', transcript_source: null }) !== with_({ title: null, transcript_source: 'asr:whisper-1' }), true);
}

console.log('T-A1-16 — transcript_source and transcript_sha256');
for (const s of ['platform_speech', 'platform_vtt', 'youtube_asr', 'asr:gpt-4o-mini-transcribe', 'asr:whisper-1']) {
  check(`T-A1-16 accepted: ${s}`, m.buildHashInput(Object.assign({}, FIELDS, { transcript_source: s }))[4], ['transcript_source', s]);
}
for (const s of ['asr', 'asr:', 'asr:Whisper-1', 'asr: whisper-1', 'platform', 'youtube', 'vtt', 'ASR:whisper-1', 7]) {
  check(`T-A1-16 refused: ${JSON.stringify(s)}`, thrown(() => with_({ transcript_source: s })),
    typeof s === 'string' ? 'transcript_source_invalid' : 'text_not_string');
}
for (const s of [TEXT_HASH.slice(1), TEXT_HASH + '0', 'sha256:' + TEXT_HASH, TEXT_HASH.replace(/^./, 'g')]) {
  check(`T-A1-16 digest refused: ${s.slice(0, 12)}… (${s.length})`, thrown(() => with_({ transcript_sha256: s })), 'transcript_sha256_invalid');
}
check('T-A1-16 a title that is not text is refused', thrown(() => with_({ title: 12 })), 'text_not_string');
check('T-A1-16 an impossible instant is refused, never hashed as text', thrown(() => with_({ reference_at: '2026-02-30T10:00:00Z' })), 'time_invalid');
check('T-A1-16 a duration that is not of its form is refused', thrown(() => with_({ duration_s: '45 minuti' })), 'duration_invalid');

console.log('T-A1-17 — idempotency');
check('T-A1-17 the same recording twice, the same reference, key and id',
  [m.recordingRef('romatv', GUID), m.keyOf(REF), m.contentId(REF, 2)],
  [m.recordingRef('romatv', GUID), m.keyOf(REF), m.contentId(REF, 2)]);
check('T-A1-17 a canonical reference read back is itself', m.canonicalRef(m.canonicalRef(REF)), REF);
check('T-A1-17 the same fields twice, the same hash', m.sourceHash(Object.assign({}, FIELDS)), H);
check('T-A1-17 the hash input fed back gives the same hash',
  m.sourceHash(Object.fromEntries(m.buildHashInput(FIELDS))), H);
check('T-A1-17 a UTC instant converted again is unchanged', m.toUtcSecond(m.toUtcSecond('2026-11-13T12:40:00+01:00')), '2026-11-13T11:40:00Z');
check('T-A1-17 the content_id does not change when the source changes',
  [m.contentId(REF, 1), with_({ title: 'Titolo corretto inventato' }) !== H], [`qn:roma:ins:${KEY}-f1`, true]);

console.log('T-A1-18 — the n8n adapter: exact committed file, stubbed $input/$json/require');
const src = fs.readFileSync(FILE, 'utf8');
function runNode(json) {
  const item = { json };
  // The n8n Code node has neither URL, URLSearchParams nor process: the adapter runs without them.
  return new Function('$input', '$json', 'require', 'URL', 'URLSearchParams', 'process', 'module', src)(
    { item }, json, require, undefined, undefined, undefined, undefined);
}
{
  const romatv = { platform: 'romatv', id: GUID.toUpperCase(), title: FIELDS.title, reference_at: FIELDS.reference_at,
    duration_s: '00:45:10.5000000', transcript_source: FIELDS.transcript_source, transcript_sha256: TEXT_HASH, n: 3 };
  const out = runNode(Object.assign({}, romatv));
  check('T-A1-18 RomaTV: the reference and the record file',
    [out.json.recording_ref, out.json.recording_file_name], [REF, `romatv__${GUID}.json`]);
  check('T-A1-18 RomaTV: the queue columns', [out.json.source_channel, out.json.source_id], ['inst_romatv', 'streaming.comune.roma.it']);
  check('T-A1-18 RomaTV: the source_hash of the module', out.json.source_hash, H);
  check('T-A1-18 RomaTV: content_id and file name when n is given',
    [out.json.content_id, out.json.file_name], [m.contentId(REF, 3), m.fileName(m.contentId(REF, 3))]);
  check('T-A1-18 the fields read are left as they came', [out.json.id, out.json.duration_s, out.json.n], [GUID.toUpperCase(), '00:45:10.5000000', 3]);
  check('T-A1-18 the adapter adds these fields and no other', Object.keys(out.json).filter((k) => !(k in romatv)).sort(),
    ['content_id', 'file_name', 'recording_file_name', 'recording_ref', 'source_channel', 'source_hash', 'source_id']);
  const listed = runNode({ platform: 'romatv', id: GUID, title: FIELDS.title, reference_at: FIELDS.reference_at,
    duration_s: '00:45:10.5000000', transcript_source: null, transcript_sha256: null });
  check('T-A1-18 without n there is no content_id and no file name',
    ['content_id' in listed.json, 'file_name' in listed.json], [false, false]);
  check('T-A1-18 n null is n not given', 'content_id' in runNode(Object.assign({}, romatv, { n: null })).json, false);
  check('T-A1-18 without a transcript (null) the hash reads the transcript fields as empty', listed.json.source_hash,
    m.sourceHash({ recording_ref: REF, title: FIELDS.title, reference_at: FIELDS.reference_at, duration_s: 2710 }));
  const noTextHash = Object.assign({}, romatv);
  delete noTextHash.transcript_sha256;
  check('T-A1-18 a hashed key left off the item hashes as empty, as null does (CONTRATTI 7 A, source_hash)',
    runNode(noTextHash).json.source_hash, runNode(Object.assign({}, romatv, { transcript_sha256: null })).json.source_hash);
  check('T-A1-18 an item as listed, without the transcript keys, hashes as the one with nulls',
    runNode({ platform: 'romatv', id: GUID, title: FIELDS.title, reference_at: FIELDS.reference_at,
      duration_s: '00:45:10.5000000' }).json.source_hash, listed.json.source_hash);
  check('T-A1-18 only the keys of HASH_FIELDS are read, not the Italian names of the record of registrazioni/',
    runNode({ platform: 'romatv', id: GUID, titolo: FIELDS.title, ora_riferimento_utc: '2026-11-13T11:40:00Z',
      durata_secondi: 2710 }).json.source_hash, m.sourceHash({ recording_ref: REF }));
  const yt = runNode({ platform: 'youtube', id: VIDEO, channel_id: CHANNEL, title: 'Commissione inventata su YouTube',
    reference_at: '2026-11-12T09:00:00Z', duration_s: 1800, transcript_source: 'youtube_asr', transcript_sha256: TEXT_HASH, n: 1 });
  check('T-A1-18 YouTube: reference, record file, queue columns, content_id',
    [yt.json.recording_ref, yt.json.recording_file_name, yt.json.source_channel, yt.json.source_id, yt.json.content_id],
    [YT_REF, `youtube__${VIDEO}.json`, 'inst_youtube', CHANNEL, m.contentId(YT_REF, 1)]);
  check('T-A1-18 YouTube without a channel id fails',
    thrown(() => runNode({ platform: 'youtube', id: VIDEO, title: 'x' })), 'channel_id_invalid');
  check('T-A1-18 an item without a usable guid fails', thrown(() => runNode({ platform: 'romatv', id: `{${GUID}}` })), 'guid_invalid');
  check('T-A1-18 an n read as text from a sheet fails, it is never converted',
    thrown(() => runNode(Object.assign({}, romatv, { n: '3' }))), 'n_invalid');
  const failing = Object.assign({}, romatv, { n: 0 });
  check('T-A1-18 n = 0 fails', thrown(() => runNode(failing)), 'n_invalid');
  check('T-A1-18 a failing item is left untouched', ['recording_ref' in failing, 'source_hash' in failing], [false, false]);
}

console.log('T-A1-19 — what the node may use inside n8n');
const code = src.replace(/\/\*[\s\S]*?\*\/|\/\/.*$/gm, '');
check('T-A1-19 no URL global', /\bURL\b|URLSearchParams/.test(code), false);
check('T-A1-19 no process', /\bprocess\b/.test(code), false);
check('T-A1-19 the only module required is crypto', code.match(/require\('[^']+'\)/g), ["require('crypto')"]);

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

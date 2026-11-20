#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/recording-state.js: the columns of the Data table, the row
 * of a recording and the moves of its state, the lease, what a listing changes in a row, the
 * record of registrazioni/, the register of a run and its alert (docs/pilota/CONTRATTI.md,
 * section 7, «A · Amministrazione»; docs/pilota/WORKSTREAM_A.md, section 4). Cases T-A2-05 and
 * T-A2-11 of WORKSTREAM_A.md, section 6, and the rows and records of T-A2-01, T-A2-04, T-A2-06
 * and T-A2-09. The n8n adapter is evaluated from the exact committed file. Every guid, video id,
 * title and date is invented (DEC-109).
 *
 * Run:  node tests/test_recording_state.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'recording-state.js');
const s = require(FILE);
const src = fs.readFileSync(FILE, 'utf8');
const list = require(path.join(__dirname, '..', 'code-nodes', 'romatv-list.js'));
const yt = require(path.join(__dirname, '..', 'code-nodes', 'youtube-list.js'));
const identity = require(path.join(__dirname, '..', 'code-nodes', 'institutional-identity.js'));

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

const NOW = '2026-11-16T10:00:00Z';
const T = Date.parse(NOW);
const GUID = 'b2c3d4e5-0000-4000-8000-000000000001';
const MARK = 'Parolamarcatrice';
const raw = (o) => Object.assign({ guid: GUID, title: `Commissione ${MARK} inventata`, referenceDate: '2026-11-12T10:00:00+01:00',
  insertDate: '2026-11-12T13:00:00+01:00', duration: '00:45:00.0000000', contentType: 'Video', tracks: [],
  smilFiles: [{ smilFileType: 'AudioOnly', url: 'https://ovp2-live.akamaized.net/inventato.smil/' }] }, o || {});
const rec = (o) => list.readEntry(raw(o), 'Municipio X').rec;
const VIDEO = 'Inv3ntato_0';
const ytRec = yt.readVideo({ id: VIDEO, channelId: yt.CHANNEL_ID, channelName: 'Canale inventato', title: `Seduta ${MARK}`,
  date: '2026-11-13T18:00:00Z', durationSeconds: 5400 }).rec;

console.log('the Data table and the row of a recording');
{
  const names = s.COLUMN_NAMES;
  check('every column once, of an n8n type', [new Set(names).size === names.length, s.COLUMNS.every((c) => ['string', 'number', 'boolean'].includes(c.type))], [true, true]);
  const row = s.newRow(rec(), null, NOW);
  check('T-A2-01 a new row uses only the columns of the table', Object.keys(row).filter((k) => !names.includes(k)), []);
  check('T-A2-01 a new row of RomaTV', [row.ref, row.tipo, row.stato, row.source_channel, row.source_id, row.catalogo, row.municipality_code, row.durata_secondi],
    [`romatv:${GUID}`, 'registrazione', 'nuova', 'inst_romatv', 'streaming.comune.roma.it', 'Municipio X', 'X', 2700]);
  check('T-A2-01 the row agrees with institutional-identity.js on the queue columns',
    [row.source_channel, row.source_id], [identity.sourceChannel('romatv'), identity.sourceId('romatv')]);
  const yrow = s.newRow(ytRec, null, NOW);
  check('T-A2-09 a new row of YouTube: the channel is the source', [yrow.ref, yrow.source_channel, yrow.source_id, yrow.municipality_code, yrow.catalogo],
    [`youtube:${VIDEO}`, identity.sourceChannel('youtube'), identity.sourceId('youtube', yt.CHANNEL_ID), 'I', '']);
  check('a reference of another form gives no row', thrown(() => s.newRow(Object.assign({}, rec(), { recording_ref: `romatv:${GUID.toUpperCase()}` }), null, NOW)), 'ref_invalid');
  check('the rows that are not recordings', [s.LEASE_ROWS, s.hostRef('api-ovp.streamcloud.it'), s.sourceRef('youtube_elenco')],
    [['lease:romatv', 'lease:youtube'], 'host:api-ovp.streamcloud.it', 'fonte:youtube_elenco']);
  check('the lease rows are written with the table, free, with only its columns',
    [s.LEASE_SEED.map((r) => [r.ref, r.presa_fino_ms]), s.LEASE_SEED.every((r) => Object.keys(r).every((k) => names.includes(k)))],
    [[['lease:romatv', 0], ['lease:youtube', 0]], true]);
}

console.log('the moves of the state (WORKSTREAM_A, section 4)');
{
  const row = s.newRow(rec(), null, NOW);
  check('the states of the table', s.STATES, ['nuova', 'testo_in_corso', 'testo_completo', 'confini_fissati', 'letta', 'scartata', 'errore']);
  check('forward along the table',
    [s.canMove('nuova', 'testo_in_corso'), s.canMove('testo_in_corso', 'testo_completo'), s.canMove('testo_completo', 'confini_fissati'), s.canMove('confini_fissati', 'letta')],
    [true, true, true, true]);
  check('a recording found in originali/ goes to confini_fissati from the text states', [s.canMove('testo_in_corso', 'confini_fissati'), s.canMove('nuova', 'confini_fissati')], [true, true]);
  check('never backwards, never out of scartata', [s.canMove('testo_completo', 'nuova'), s.canMove('letta', 'confini_fissati'), s.canMove('scartata', 'nuova'), s.canMove('scartata', 'errore')],
    [false, false, false, false]);
  check('scartata only by the list or the text, before the boundary', [s.canMove('nuova', 'scartata'), s.canMove('testo_completo', 'scartata'), s.canMove('confini_fissati', 'scartata')], [true, true, false]);
  check('a move that is not in the table fails', thrown(() => s.move(row, 'letta', NOW)), 'move_invalid: nuova -> letta');
  check('errore leaves only by a restart by hand', [s.canMove('errore', 'nuova'), thrown(() => s.restart(row, NOW))], [false, 'restart_only_from_errore']);
  let r = Object.assign(s.move(row, 'testo_in_corso', NOW), { segmento_ripresa: 42 });
  r = s.failAttempt(r, NOW, 'x');
  r = s.failAttempt(r, NOW, 'x');
  check('two failed attempts keep the state', [r.stato, r.tentativi], ['testo_in_corso', 2]);
  r = s.failAttempt(r, NOW, 'tre tentativi');
  check('the third goes to errore, keeping where it fell', [r.stato, r.stato_prima_errore, r.tentativi, r.motivo], ['errore', 'testo_in_corso', 3, 'tre tentativi']);
  const back = s.restart(Object.assign({}, r, { apify_run_id: 'run1', apify_storage_id: 'st1', transcript_source: 'asr:x' }), NOW);
  check('a fall during the text restarts from nuova and the first segment', [back.stato, back.segmento_ripresa, back.tentativi], ['nuova', 0, 0]);
  check('and forgets its text and its Apify run', [back.transcript_source, back.apify_run_id, back.apify_storage_id], ['', '', '']);
  check('after the restart a failure is the first again', s.failAttempt(back, NOW, 'x').stato, 'nuova');
  const fellReading = s.restart(Object.assign({}, row, { stato: 'errore', stato_prima_errore: 'confini_fissati', segmento_ripresa: 99 }), NOW);
  check('a fall after the boundary restarts from where it fell', [fellReading.stato, fellReading.segmento_ripresa], ['confini_fissati', 99]);
  check('a restart from letta goes back to letta', s.restart(Object.assign({}, row, { stato: 'errore', stato_prima_errore: 'letta' }), NOW).stato, 'letta');
}

console.log('T-A2-11 — the lease');
{
  const free = Object.assign({}, s.LEASE_SEED[0]);
  const a = s.claim(free, 101, T, 'list', false);
  check('T-A2-11 a free lease is taken for five minutes', [a.action, a.fields], ['take', { presa_id: '101', presa_fino_ms: T + 5 * 60000 }]);
  check('T-A2-11 the write carries its condition, all of it: the lease free or run out',
    a.where, { match: 'allConditions', conditions: [{ keyName: 'ref', condition: 'eq', keyValue: 'lease:romatv' }, { keyName: 'presa_fino_ms', condition: 'lte', keyValue: T }] });
  const held = Object.assign({}, free, a.fields);
  check('T-A2-11 the run that wrote it holds it; another does not', [s.holds(held, 101, T + 1000), s.holds(held, 102, T + 1000)], [true, false]);
  const b = s.claim(held, 102, T + 60000, 'list', false);
  check('T-A2-11 the list that finds it held waits, at most until it runs out', [b.action, b.wait_ms], ['wait', 4 * 60000]);
  check('T-A2-11 after the wait, still held: the list leaves the source for this run', s.claim(held, 102, T + 60000, 'list', true).action, 'skip');
  check('T-A2-11 the text that finds it held does not start', s.claim(held, 103, T + 60000, 'text', false).action, 'no_start');
  check('T-A2-11 a lease that ran out is taken again', [s.claim(held, 102, T + 5 * 60000, 'list', false).action, s.holds(held, 101, T + 5 * 60000)], ['take', false]);
  // A table that applies the condition of an update, as the Data table node's filter does, with
  // its «Must Match».
  const table = { row: Object.assign({}, free) };
  const test = (row, w) => (w.condition === 'eq' ? row[w.keyName] === w.keyValue : row[w.keyName] <= w.keyValue);
  const update = (c) => {
    const ok = c.where.match === 'allConditions' ? c.where.conditions.every((w) => test(table.row, w)) : c.where.conditions.some((w) => test(table.row, w));
    if (ok) Object.assign(table.row, c.fields);
    return ok;
  };
  const read = () => Object.assign({}, table.row);
  // Both runs read the lease free; then A writes and reads back, then B writes and reads back.
  const ca = s.claim(read(), 301, T, 'list', false);
  const cb = s.claim(read(), 302, T, 'text', false);
  const order1 = [update(ca), s.holds(read(), 301, T), update(cb), s.holds(read(), 302, T)];
  check('T-A2-11 two runs on the same row, A writes and reads before B: only A works', order1, [true, true, false, false]);
  table.row = Object.assign({}, free);
  const order2 = [update(ca), update(cb), s.holds(read(), 301, T), s.holds(read(), 302, T)];
  check('T-A2-11 both write before reading: the second write finds the lease taken, only A works', order2, [true, false, true, false]);
  const renew = s.claim(read(), 301, T + 4 * 60000, 'list', false);
  check('T-A2-11 the run that holds it renews it at each step, on its own lease only',
    [renew.fields.presa_fino_ms, renew.where.conditions[1], update(renew)], [T + 9 * 60000, { keyName: 'presa_id', condition: 'eq', keyValue: '301' }, true]);
  check('T-A2-11 a renewal by a run that lost the lease writes nothing',
    update({ fields: s.leaseFields(302, T + 4 * 60000), where: { match: 'allConditions', conditions: [{ keyName: 'ref', condition: 'eq', keyValue: 'lease:romatv' }, { keyName: 'presa_id', condition: 'eq', keyValue: '302' }] } }), false);
  // A's lease runs out, B takes it, then A leaves what it read: the release carries its condition.
  table.row = Object.assign({}, free, s.leaseFields(401, T));
  const late = T + 6 * 60000;
  update(s.claim(read(), 402, late, 'list', false));
  check('T-A2-11 a release by a run whose lease ran out and was taken writes nothing', [update(s.release(read(), 401)), read().presa_id], [false, '402']);
  check('T-A2-11 the release of the run that holds it leaves the lease free', [update(s.release(read(), 402)), s.leaseFree(read(), late)], [true, true]);
  // The same lease on the row of a recording (WORKSTREAM_A, section 4, «La presa»).
  table.row = s.newRow(rec(), null, NOW);
  const r1 = s.claim(read(), 501, T, 'text', false);
  const r2 = s.claim(read(), 502, T, 'text', false);
  check('T-A2-11 on the row of a recording too, only one of two runs works', [update(r1), update(r2), s.holds(read(), 501, T), s.holds(read(), 502, T)],
    [true, false, true, false]);
  check('T-A2-11 a lease row with no end, and a run with no id, are errors',
    [thrown(() => s.claim({ ref: 'lease:romatv', presa_fino_ms: '' }, 1, T, 'list', false)), thrown(() => s.claim(free, undefined, T, 'list', false)),
      thrown(() => s.holds(free, '', T))],
    ['lease_row_invalid', 'execution_id_missing', 'execution_id_missing']);
  check('T-A2-11 a lease row that does not exist is an error, not a free lease', thrown(() => s.claim(undefined, 1, T, 'text', false)), 'lease_row_missing');
}

console.log('T-A2-05 — the platform transcript added later');
{
  const speech = [{ trackType: 'SpeechToTextTrack', speechToTextTrackSource: 'https://ac104mp.streamcloud.it/speech/inventato.json' }];
  const later = rec({ tracks: speech });
  const at = (stato, extra) => Object.assign(s.newRow(rec(), null, NOW), { stato }, extra || {});
  const u = s.listingUpdate(at('nuova'), later, null, NOW);
  check('T-A2-05 the row and its record are updated', [u.update.trascrizione_piattaforma, u.update.parlato_url, u.record], [true, speech[0].speechToTextTrackSource, true]);
  const withIt = (stato, extra) => Object.assign(at(stato, extra), u.update);
  check('T-A2-05 our text not started: the platform\'s is used', s.textPlan(withIt('nuova')), 'platform');
  check('T-A2-05 our text in progress: it switches to the platform\'s (T-A3-19)', s.textPlan(withIt('testo_in_corso')), 'switch_to_platform');
  check('T-A2-05 our text done: it stays ours, with no second spend',
    ['testo_completo', 'confini_fissati', 'letta'].map((st) => s.textPlan(withIt(st, { transcript_source: 'asr:gpt-4o-mini-transcribe' }))), ['keep', 'keep', 'keep']);
  check('T-A2-05 even without its transcript_source',
    ['testo_completo', 'confini_fissati', 'letta'].map((st) => s.textPlan(withIt(st))), ['keep', 'keep', 'keep']);
  check('T-A2-05 a row discarded or in error makes no text', [s.textPlan(withIt('scartata')), s.textPlan(withIt('errore'))], ['none', 'none']);
  const vtt = rec({ tracks: [{ trackType: 'SpeechToTextTrack', speechToTextTrackSource: speech[0].speechToTextTrackSource,
    speechToTextTrackWebVtt: 'https://streaming.comune.roma.it/webvtt/inventato.vtt' }] });
  check('T-A2-05 the WebVTT that appears after the speech JSON enters the row too',
    s.listingUpdate(withIt('nuova'), vtt, null, NOW).update, { vtt_url: 'https://streaming.comune.roma.it/webvtt/inventato.vtt', aggiornata_utc: NOW });
  check('T-A2-05 the record says the platform has its transcript even when the text stays ours',
    s.listingUpdate(at('testo_completo', { transcript_source: 'asr:x' }), later, null, NOW).update.trascrizione_piattaforma, true);
  check('T-A2-05 without a platform transcript the text is ours', s.textPlan(at('nuova')), 'ours');
}

console.log('T-A2-04, T-A2-06 — a recording seen again');
{
  const row = s.newRow(rec(), null, NOW);
  check('T-A2-04 an entry already seen gives no second row, and changes nothing', s.listingUpdate(row, rec(), null, NOW), { update: null, record: false });
  check('T-A2-04 a title changed later does not change the row', s.listingUpdate(row, rec({ title: 'Titolo cambiato' }), null, NOW).update, null);
  const link = { prima_parte: 'romatv:b2c3d4e5-0000-4000-8000-000000000000', parte_precedente: 'romatv:b2c3d4e5-0000-4000-8000-000000000000' };
  check('T-A2-06 the link of a part changes while the row is nuova', s.listingUpdate(row, rec(), link, NOW).update.prima_parte, link.prima_parte);
  check('T-A2-06 once the text has started the link stays as it was', s.listingUpdate(Object.assign({}, row, { stato: 'testo_in_corso' }), rec(), link, NOW).update, null);
  const linked = Object.assign({}, row, link);
  check('T-A2-06 a run that does not see the part before takes no link away', s.listingUpdate(linked, rec(), {}, NOW).update, null);
}

console.log('the record of registrazioni/ (CONTRATTI 7 A, row Registrazione)');
{
  const r = s.record(s.newRow(rec(), null, NOW));
  check('the fields of a RomaTV record, in order', Object.keys(r),
    ['schema_version', 'recording_ref', 'source_channel', 'source_id', 'catalogo', 'organo', 'municipality_code', 'titolo', 'ora_riferimento_utc',
      'ora_pubblicazione_utc', 'durata_secondi', 'trascrizione_piattaforma', 'url', 'stato']);
  check('its values', [r.schema_version, r.titolo, r.ora_riferimento_utc, r.url, r.stato],
    ['pilot-recording-0.1', `Commissione ${MARK} inventata`, '2026-11-12T09:00:00Z', `https://streaming.comune.roma.it/portal/watch/vod/${GUID}`, 'nuova']);
  const y = s.record(s.newRow(ytRec, null, NOW));
  check('a YouTube record names its channel, not a catalogue', ['canale' in y, 'catalogo' in y, y.canale, y.url],
    [true, false, 'Canale inventato', `https://www.youtube.com/watch?v=${VIDEO}`]);
  check('a record without a page has no url', 'url' in s.record(s.newRow(rec({ contentType: 'Live' }), null, NOW)), false);
  const part = s.record(s.newRow(rec({ title: 'Consiglio inventato parte 2' }), { prima_parte: 'romatv:x', parte_precedente: 'romatv:x' }, NOW));
  check('a part records its number and its link', part.parte, { numero: 2, prima_parte: 'romatv:x', parte_precedente: 'romatv:x' });
  check('the file name, as institutional-identity.js', [s.recordFileName(`romatv:${GUID}`), s.recordFileName(`youtube:${VIDEO}`)],
    [identity.recordingFileName(`romatv:${GUID}`), identity.recordingFileName(`youtube:${VIDEO}`)]);
}

console.log('the register and the alert');
{
  let reading = list.startReading('Municipio X');
  reading = list.readPage(reading, { data: { hasNext: true, items: [raw()] } }, NOW);
  const run = { workflow: 'staging_A_elenco', execution_id: '9', started_at: NOW, finished_at: NOW, user_agent: 'ua', readings: [reading],
    new_rows: [`romatv:${GUID}`], updated_rows: [], unbound: [], stopped_now: [], skipped_sources: [] };
  const log = s.runLog(run);
  check('the register says how each catalogue was read', log.readings, [{ fonte: 'romatv', catalogo: 'Municipio X', pages: 1, complete: null, reason: null, host_stopped: false, in_window: 1, skipped: [] }]);
  check('T-A3-15 no title and no text in the register', JSON.stringify(log).includes(MARK), false);
  check('the register lists the rows a run leaves to the next one, and none when it leaves none',
    [s.runLog(Object.assign({}, run, { deferred: [`romatv:${GUID}`] })).deferred_rows, log.deferred_rows], [[`romatv:${GUID}`], []]);
  check('a run that read every list whole has no alert', s.runAlert(Object.assign({}, log, { readings: [] })), null);
  const done = list.readPage(list.startReading('Municipio V'), { error: 'x' }, NOW);
  const alert = s.runAlert(s.runLog(Object.assign({}, run, { readings: [done] })));
  check('an incomplete list gives an alert, named as those of staging_A_avviso',
    [alert.name, alert.body.incompleti], ['AVVISO_A_20261116T100000Z_elenchi.json', [{ fonte: 'romatv', catalogo: 'Municipio V', reason: 'answer without a list of entries' }]]);
  const skippedReading = list.readFailure(list.startReading('Municipio X'), { outcome: 'skipped', reason: 'host stopped', host_stopped: true });
  check('a list not read because its host is already stopped is in the register, with no second alert',
    [s.runAlert(s.runLog(Object.assign({}, run, { readings: [skippedReading] }))), s.runLog(Object.assign({}, run, { readings: [skippedReading] })).readings[0].host_stopped],
    [null, true]);
  const unchecked = list.readFailure(list.startReading('Municipio X'), { outcome: 'skipped', reason: 'robots.txt not checked today', host_stopped: false });
  check('a list not read because robots.txt is not checked today gives its alert', !!s.runAlert(s.runLog(Object.assign({}, run, { readings: [unchecked] }))), true);
  const ytList = yt.readDataset([], NOW);
  check('T-A2-09 an incomplete list of YouTube gives an alert that names it',
    s.runAlert(s.runLog(Object.assign({}, run, { readings: [ytList] }))).body.incompleti, [{ fonte: 'youtube', catalogo: null, reason: 'empty list' }]);
  check('a source left for the lease is in the register, with no alert',
    [s.runAlert(s.runLog(Object.assign({}, run, { readings: [], skipped_sources: [{ fonte: 'romatv', reason: 'lease held' }] }))),
      s.runLog(Object.assign({}, run, { skipped_sources: [{ fonte: 'romatv', reason: 'lease held' }] })).skipped_sources.length], [null, 1]);
}

console.log('the n8n adapter');
function runNode(json) {
  return new Function('$input', '$json', 'require', 'URL', 'URLSearchParams', 'process', 'module', src)(
    { item: { json } }, json, require, undefined, undefined, undefined, undefined);
}
{
  const first = runNode({ stage: 'listing', rec: rec(), link: null, row: null });
  check('listing: a recording never seen is written with an upsert on its ref, with its record',
    [first.json.action, first.json.where, first.json.record_file_name, JSON.parse(first.json.record).stato],
    ['upsert', { match: 'allConditions', conditions: [{ keyName: 'ref', condition: 'eq', keyValue: `romatv:${GUID}` }] }, `romatv__${GUID}.json`, 'nuova']);
  const again = runNode({ stage: 'listing', rec: rec(), link: null, row: first.json.fields });
  check('T-A2-04 listing: the same recording seen again gives nothing', [again.json.action, again.json.record], ['none', null]);
  // The same recording twice in a run, both read before either is written: an upsert on the ref
  // gives one row.
  const rows = new Map();
  for (const out of [runNode({ stage: 'listing', rec: rec(), row: null }), runNode({ stage: 'listing', rec: rec(), row: null })]) {
    const key = out.json.where.conditions[0].keyValue;
    rows.set(key, Object.assign({}, rows.get(key) || {}, out.json.fields));
  }
  check('T-A2-04 listing: the same recording twice in a run gives one row', rows.size, 1);
  check('listing: a row of another ref is an error, never a second row',
    thrown(() => runNode({ stage: 'listing', rec: rec(), link: null, row: { ref: 'romatv:b2c3d4e5-0000-4000-8000-000000000009' } })),
    `listing_row_of_another_ref: romatv:b2c3d4e5-0000-4000-8000-000000000009 for romatv:${GUID}`);
  const update = runNode({ stage: 'listing', rec: rec({ tracks: [{ trackType: 'SpeechToTextTrack', speechToTextTrackSource: 'https://ac104mp.streamcloud.it/speech/x.json' }] }), row: first.json.fields });
  check('listing: an update carries its ref, for the upsert', [update.json.action, update.json.fields.ref], ['upsert', `romatv:${GUID}`]);
  const restarted = runNode({ stage: 'restart', row: Object.assign({}, first.json.fields, { stato: 'errore', stato_prima_errore: 'testo_in_corso', tentativi: 3 }) });
  check('restart: the restart by hand, from its stage', [restarted.json.fields.stato, restarted.json.fields.tentativi], ['nuova', 0]);
  check('restart: the state changes, so the record of registrazioni/ is written again, and the row by its ref',
    [restarted.json.record_file_name, JSON.parse(restarted.json.record).stato, JSON.parse(restarted.json.record).recording_ref, restarted.json.where],
    [`romatv__${GUID}.json`, 'nuova', `romatv:${GUID}`, { match: 'allConditions', conditions: [{ keyName: 'ref', condition: 'eq', keyValue: `romatv:${GUID}` }] }]);
  check('restart: a row without its ref, or not in errore, writes nothing',
    [thrown(() => runNode({ stage: 'restart', row: { stato: 'errore' } })), thrown(() => runNode({ stage: 'restart', row: first.json.fields }))],
    ['ref_invalid', 'restart_only_from_errore']);
  const lease = runNode({ stage: 'claim', lease_row: s.LEASE_SEED[0], execution_id: 7, who: 'list' });
  check('claim: a free lease is taken by this execution', [lease.json.lease.action, lease.json.lease.fields.presa_id], ['take', '7']);
  const rel = runNode({ stage: 'release', lease_row: Object.assign({}, s.LEASE_SEED[0], lease.json.lease.fields), execution_id: 7 });
  check('release: the fields and the condition from its stage', [rel.json.release.fields, rel.json.release.where.conditions[1]],
    [{ presa_id: '', presa_fino_ms: 0 }, { keyName: 'presa_id', condition: 'eq', keyValue: '7' }]);
  check('holds: the lease read back', runNode({ stage: 'holds', lease_row: lease.json.lease.fields, execution_id: 7 }).json.lease_ours, true);
  const logged = runNode({ stage: 'log', run: { workflow: 'staging_A_elenco', started_at: NOW, readings: [], stopped_now: [], skipped_sources: [] } });
  check('log: the register file of the run', [logged.json.log_file_name, logged.json.alert], ['elenco_20261116T100000Z.json', null]);
  check('an unknown stage fails', thrown(() => runNode({ stage: 'x' })), 'recording-state.js: unknown stage "x"');
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

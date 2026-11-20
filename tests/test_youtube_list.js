#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/youtube-list.js: the list of the videos of the Municipio I
 * channel from an Actor of Apify (DEC-037, points 2 and 3; docs/pilota/CONTRATTI.md, section 7,
 * «A · Amministrazione», rows Fonti, Raccolta, Registrazione and Costi). Cases T-A2-09, T-A2-10 and
 * T-A2-12 of docs/pilota/WORKSTREAM_A.md, section 6, on an invented Actor and a fake clock: no
 * call to Apify. The n8n adapter is evaluated from the exact committed file. Every video id, title
 * and date is invented (DEC-109).
 *
 * Run:  node tests/test_youtube_list.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'youtube-list.js');
const y = require(FILE);
const src = fs.readFileSync(FILE, 'utf8');
const state = require(path.join(__dirname, '..', 'code-nodes', 'recording-state.js'));
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

const NOW = '2026-11-16T19:10:00Z'; // 20:10 in Rome
const ago = (now, ms) => new Date(Date.parse(now) - ms).toISOString().slice(0, 19) + 'Z';
// Invented video ids of 11 characters, and an invented Actor's items.
const vid = (n) => `Vid${String(n).padStart(8, '0')}`;
// The form of an item of LIST_ACTOR (WORKSTREAM_A, section 6, the trial of 20 November 2026).
const item = (n, o) => Object.assign({ id: vid(n), url: `https://www.youtube.com/watch?v=${vid(n)}`, channelId: y.CHANNEL_ID,
  channelName: 'Canale inventato', title: `Seduta inventata ${n}`, date: '2026-11-13T18:00:00Z', durationSeconds: 3723, duration: '01:02:03',
  type: 'video' }, o || {});
const run = (status, o) => Object.assign({ id: `run${status}`, actId: 'inventato~elenco', status, startedAt: ago(NOW, 600000),
  finishedAt: ago(NOW, 60000), usageTotalUsd: 0.0123 }, o || {});

console.log('T-A2-09 — one video of the list');
{
  const v = y.readVideo(item(1));
  check('T-A2-09 youtube:<id> for an id of 11 characters', [v.ok, v.rec.recording_ref], [true, `youtube:${vid(1)}`]);
  check('T-A2-09 the reference agrees with institutional-identity.js', v.rec.recording_ref, identity.recordingRef('youtube', vid(1)));
  check('T-A2-09 no reference for an id of another length or form',
    [y.readVideo(item(2, { id: 'Vid12345', url: null })).reason, y.readVideo(item(3, { id: `${vid(3)}x`, url: null })).reason, y.readVideo(item(4, { id: 'Vid0000000!', url: null })).reason],
    ['video_id_invalid', 'video_id_invalid', 'video_id_invalid']);
  check('T-A2-09 the id read from `id` or from the address, also when `id` is something else',
    [y.readVideo({ id: vid(5), date: NOW, durationSeconds: 60 }).rec.recording_ref,
      y.readVideo({ id: 'item-0001', url: `https://www.youtube.com/watch?v=${vid(6)}&t=1`, date: NOW, durationSeconds: 60 }).rec.recording_ref,
      y.readVideo({ url: `https://youtu.be/${vid(7)}`, date: NOW, durationSeconds: 60 }).rec.recording_ref,
      y.readVideo({ url: `https://www.youtube.com/live/${vid(8)}?si=x`, date: NOW, durationSeconds: 60 }).rec.recording_ref],
    [`youtube:${vid(5)}`, `youtube:${vid(6)}`, `youtube:${vid(7)}`, `youtube:${vid(8)}`]);
  check('T-A2-09 source_id is the channel; the Municipality comes from the channel', [v.rec.source_id, v.rec.municipality_code], [y.CHANNEL_ID, 'I']);
  check('T-A2-09 a video of another channel is not kept', y.readVideo(item(9, { channelId: 'UCinventatoinventato000' })).reason, 'other_channel');
  check('T-A2-09 the Actor gives no start of a live broadcast: the reference is the publication, whatever else the item carries',
    [y.ACTOR_FIELDS.live_start, y.readVideo(item(10, { liveStreamingDetails: { actualStartTime: '2026-11-13T15:00:00+01:00' }, actualStartTime: '2026-11-13T14:00:00Z' })).rec.ora_riferimento_utc,
      v.rec.ora_riferimento_utc, v.rec.ora_pubblicazione_utc],
    [[], '2026-11-13T18:00:00Z', '2026-11-13T18:00:00Z', '2026-11-13T18:00:00Z']);
  check('T-A2-09 a publication with its offset is brought to UTC to the second',
    [y.readVideo(item(18, { date: '2026-11-13T15:00:00+01:00' })).rec.ora_riferimento_utc, y.utcSecond('2026-11-13T15:00:00.123-0230')],
    ['2026-11-13T14:00:00Z', '2026-11-13T17:30:00Z']);
  check('T-A2-09 a date without its offset, a day that does not exist or the hour 24 are not dates',
    [y.readVideo(item(11, { date: '2026-11-13 18:00' })).reason, y.utcSecond('2026-02-30T10:00:00Z'), y.utcSecond('2026-11-13T24:00:00Z')],
    ['date_invalid', null, null]);
  check('T-A2-09 the duration as seconds, h:mm:ss, m:ss or ISO 8601',
    [3723, '1:02:03', '62:03', 'PT1H2M3S', '3723'].map((d) => y.seconds(d)), [3723, 3723, 3723, 3723, 3723]);
  check('T-A2-09 a duration of zero is not yet a recording', [0, '0', '0:00', 'PT0S'].map((d) => y.seconds(d)), [null, null, null, null]);
  check('T-A2-09 the page of the video for the reader', v.rec.url, `https://www.youtube.com/watch?v=${vid(1)}`);
  check('T-A2-09 the duration from durationSeconds, else from duration', [v.rec.durata_secondi, y.readVideo(item(12, { durationSeconds: undefined })).rec.durata_secondi],
    [3723, 3723]);
  check('T-A2-09 the duration as the Actor writes it, hh:mm:ss', y.readVideo(item(13, { durationSeconds: undefined, duration: '00:17:21' })).rec.durata_secondi, 1041);
  check('T-A2-09 a Short of the window is kept, as every video of the window (CONTRATTI 7 A, «Raccolta»; the question: WORKSTREAM_A, section 9)',
    [y.readVideo(item(15, { type: 'short', durationSeconds: 49 })).ok, y.readDataset([item(17, { type: 'short', date: '2026-10-30T10:00:00Z' })], NOW).complete],
    [true, true]);
  const err = { error: 'invented error', input: 'invented', note: 'invented note' };
  check('T-A2-15 an error item of the Actor is no video, with its own reason', y.readVideo(err), { ok: false, reason: 'actor_error', id: null });
  check('T-A2-15 a list of error items only is incomplete; one beside the videos is listed and changes nothing else',
    [y.readDataset([err], NOW).reason, y.readDataset([err, item(14, { date: '2026-10-30T10:00:00Z' })], NOW).complete,
      y.readDataset([err, item(14, { date: '2026-10-30T10:00:00Z' })], NOW).skipped],
    ['no valid video in the list', true, [{ id: null, reason: 'actor_error' }]]);
}

console.log('T-A2-09 — the videos of the window, and whether the list covers it');
{
  const items = [item(20, { date: '2026-11-15T10:00:00Z' }), item(21, { date: '2026-11-02T10:00:00Z' }),
    item(20, { date: '2026-11-15T10:00:00Z' }), item(22, { date: '2026-10-30T10:00:00Z' }), item(23, { id: 'x', url: null })];
  const d = y.readDataset(items, NOW);
  check('T-A2-09 the videos inside the window are kept, each once', d.records.map((r) => r.recording_ref), [`youtube:${vid(20)}`, `youtube:${vid(21)}`]);
  check('T-A2-09 the others are listed with their reason', d.skipped, [{ id: vid(20), reason: 'repeated in the list' }, { id: 'x', reason: 'video_id_invalid' }]);
  check('T-A2-09 a list with a video from before the start of the window covers it', [d.complete, d.reason], [true, null]);
  check('T-A2-09 the same list without that video does not, however short it is',
    [y.readDataset(items.filter((x) => x.id !== vid(22)), NOW).complete, y.readDataset(items.filter((x) => x.id !== vid(22)), NOW).reason],
    [false, 'the list does not reach the start of the window']);
  check('T-A2-09 an empty list and a list of nothing valid are incomplete, with their reason',
    [y.readDataset([], NOW).reason, y.readDataset([item(24, { date: 'ieri' })], NOW).reason], ['empty list', 'no valid video in the list']);
  const late = '2027-03-01T10:00:00Z';
  check('T-A2-09 past 1 November the window is 100 days: a video at 100 days is in, one at 101 out',
    [y.inWindow(ago(late, 100 * 86400000), late), y.inWindow(ago(late, 101 * 86400000), late)], [true, false]);
  const row = state.newRow(d.records[0], null, NOW);
  check('T-A2-09 a video already seen gives no second row', state.listingUpdate(row, d.records[0], null, NOW).update, null);
}

console.log('T-A2-09 — the run of the list: its limits and its cost file');
{
  const st = y.startRequest('inventato~elenco', NOW);
  check('T-A2-16 the request that starts the run carries its timeout, the cap of its items and the cap of its charge', [st.url, st.method, st.asked],
    ['https://api.apify.com/v2/acts/inventato~elenco/runs?timeout=900&maxItems=68&maxTotalChargeUsd=0.1', 'POST', 68]);
  check('T-A2-16 the charge cap stays above a full window at the price of the trial (WORKSTREAM_A, section 7)',
    y.MAX_CHARGE_USD >= y.MAX_VIDEOS * 0.0002 + 0.00005, true);
  check('T-A2-16 the Actor of the trial is a valid name for the request, its input the body',
    [y.startRequest(y.LIST_ACTOR, NOW).url.startsWith('https://api.apify.com/v2/acts/grow_media~youtube-channel-video-scraper/runs?'), y.startRequest(y.LIST_ACTOR, NOW).body],
    [true, y.actorInput(NOW)]);
  check('an actor that is not of the form user~name is refused', thrown(() => y.startRequest('https://evil.invalid', NOW)), 'actor_invalid');
  check('T-A2-09 a running run is waited for 20 minutes from its start, then left in the row for the next run',
    [y.pollDecision(run('RUNNING', { startedAt: ago(NOW, 60000) }), NOW).next, y.pollDecision(run('RUNNING', { startedAt: ago(NOW, 21 * 60000) }), NOW).next,
      y.pollDecision(run('RUNNING', { startedAt: null }), NOW).next],
    ['wait', 'leave', 'leave']);
  check('T-A2-09 only a state that is not known is lost', [y.pollDecision({ status: 'STRANO' }, NOW).next, y.pollDecision(undefined, NOW).next], ['lost', 'lost']);
  check('T-A2-09 and its reason names the state, not the cause', [y.pollDecision({ status: 'STRANO' }, NOW).reason, y.pollDecision(undefined, NOW).reason], ['status "STRANO"', 'status null']);
  check('T-A2-09 a run that just ended is read again for its settled cost, then read',
    [y.pollDecision(run('SUCCEEDED', { finishedAt: ago(NOW, 5000) }), NOW).next, y.pollDecision(run('SUCCEEDED'), NOW).next, y.pollDecision(run('FAILED'), NOW).next],
    ['settle', 'read', 'read']);
  check('T-A2-09 a finished run with no end time is read 20 minutes after its start, or at once without a start',
    [y.pollDecision(run('SUCCEEDED', { finishedAt: null, startedAt: ago(NOW, 60000) }), NOW).next, y.pollDecision(run('SUCCEEDED', { finishedAt: null, startedAt: ago(NOW, 3 * 3600000) }), NOW).next,
      y.pollDecision(run('FAILED', { finishedAt: null, startedAt: null }), NOW).next],
    ['settle', 'read', 'read']);
  check('T-A2-09 without a start a run that just ended still waits for its settled cost, also with an end a moment ahead of this clock; an end far in the future does not hold it',
    [y.pollDecision(run('SUCCEEDED', { startedAt: null, finishedAt: ago(NOW, 5000) }), NOW).next, y.pollDecision(run('SUCCEEDED', { startedAt: null, finishedAt: ago(NOW, 60000) }), NOW).next,
      y.pollDecision(run('SUCCEEDED', { startedAt: null, finishedAt: ago(NOW, -2000) }), NOW).next, y.pollDecision(run('FAILED', { startedAt: null, finishedAt: ago(NOW, -3600000) }), NOW).next],
    ['settle', 'read', 'settle', 'read']);
  check('T-A2-10 a run not finished never reaches its list or its cost',
    [thrown(() => y.finishedRun(run('RUNNING'), NOW)), thrown(() => y.finishedRun(run('SUCCEEDED', { finishedAt: ago(NOW, 5000) }), NOW))],
    ['run_not_finished: RUNNING', 'run_not_finished: SUCCEEDED']);
  check('T-A2-10 nor does a run left still waiting', thrown(() => y.finishedRun(run('RUNNING', { startedAt: ago(NOW, 21 * 60000) }), NOW)), 'run_not_finished: RUNNING');
  const ok = y.costEntry(run('SUCCEEDED'), 40);
  check('T-A2-09 a run that succeeded: its videos and Apify\'s own total in dollars',
    [ok.workstream, ok.servizio, ok.unita, ok.quantita, ok.usd, ok.recording_ref, y.costFileName(ok)],
    ['A', 'apify', 'video_elencati', 40, 0.0123, null, 'costo_apify_runSUCCEEDED.json']);
  const ko = y.costEntry(run('FAILED'), 0);
  check('T-A2-10 a failed run has its file too, with the quantity unknown, never zero', [ko.quantita, ko.usd, ko.status], [null, 0.0123, 'FAILED']);
  check('a run without its declared total records null', y.costEntry(run('SUCCEEDED', { usageTotalUsd: undefined }), 1).usd, null);
}

console.log('T-A2-10 — the stops of the list, and a run left behind');
{
  let s = {};
  const flags = [];
  for (let i = 1; i <= 5; i++) {
    const r = y.afterListRun(s, run('FAILED'), NOW, null);
    s = r.state;
    flags.push([r.read, s.errori_di_fila, r.stopped_now]);
  }
  check('T-A2-10 a failed run leaves the list unread in this run; five in a row stop it',
    flags, [[false, 1, false], [false, 2, false], [false, 3, false], [false, 4, false], [false, 5, true]]);
  check('T-A2-10 until the next day of Rome', [s.fermo, s.fermo_fino, y.listPlan(s, '2026-11-16T20:00:00Z').action], ['giorno', '2026-11-17', 'none']);
  check('T-A2-10 the next day the list is asked again', y.listPlan(s, '2026-11-17T18:30:00Z').action, 'start');
  const recovered = y.afterListRun(s, run('SUCCEEDED'), '2026-11-17T18:30:00Z', y.readDataset([item(30, { date: '2026-10-30T10:00:00Z' })], '2026-11-17T18:30:00Z'));
  check('T-A2-10 a run that succeeds after it ends the streak', [recovered.state.errori_di_fila, recovered.state.fermo], [0, '']);
  check('T-A2-10 ABORTED and TIMED-OUT are failed runs as well', ['ABORTED', 'TIMED-OUT'].map((st) => y.afterListRun({}, run(st), NOW, null).state.errori_di_fila), [1, 1]);
  check('T-A2-10 a list stopped by the owner, or with a stop written by hand, is not asked',
    [y.listPlan({ fermo: 'owner' }, NOW).action, y.listPlan({ fermo: 'si' }, NOW).action, y.listPlan({ fermo: 'giorno', fermo_fino: '17/11' }, NOW).action],
    ['none', 'none', 'none']);
  check('T-A2-10 a run that succeeded with a dataset not read: the list is not read, the day not done, the failure counted',
    (() => { const r = y.afterListRun({ errori_di_fila: 2 }, run('SUCCEEDED'), NOW, null); return [r.read, r.state.ultimo_ok_giorno, r.state.errori_di_fila, r.reason]; })(),
    [false, '', 3, 'dataset not read']);
  check('T-A2-10 a run started and never read (the execution died): its id in the row, the next run resumes it first',
    [y.startedFields({ id: 'runXabc123' }), y.listPlan({ apify_run_id: 'runXabc123', ultimo_ok_giorno: '2026-11-16' }, NOW)],
    [{ apify_run_id: 'runXabc123' }, { action: 'resume', run_id: 'runXabc123' }]);
  check('T-A2-10 an id that is not an Apify run id is never written',
    [thrown(() => y.startedFields({ data: { id: 'r1' } })), thrown(() => y.startedFields({ id: 'r1/../x' })), thrown(() => y.startedFields({ id: '' }))],
    ['run: an Apify run with its id required', 'run: an Apify run with its id required', 'run: an Apify run with its id required']);
  check('T-A2-10 once read, the id leaves the row', y.afterListRun({ apify_run_id: 'runXabc123' }, run('FAILED'), NOW, null).state.apify_run_id, '');
  check('T-A2-10 a run in the row is resumed also with the list stopped, for a day or by the owner',
    [y.listPlan({ apify_run_id: 'runXabc123', fermo: 'giorno', fermo_fino: '2026-11-17' }, NOW).action, y.listPlan({ apify_run_id: 'runXabc123', fermo: 'owner' }, NOW).action],
    ['resume', 'resume']);
  // A run Apify keeps waiting: left at each run of the flow, its list not read each time.
  let left = { apify_run_id: 'runStuck1234', ultimo_ok_giorno: '2026-11-15' };
  const leftSeen = [];
  for (let i = 0; i < 5; i++) {
    const r = y.afterListLeft(left, { id: 'runStuck1234', status: 'RUNNING' }, 'run still waiting', '2026-11-16T18:40:00Z');
    left = r.state;
    leftSeen.push([y.listPlan(left, '2026-11-16T20:40:00Z').action, left.apify_run_id, left.errori_di_fila, r.read, r.stopped_now]);
  }
  check('T-A2-10 a run left still waiting keeps its id in the row and counts each time; five in a row stop the list, and the run is still resumed',
    leftSeen, [1, 2, 3, 4, 5].map((n) => ['resume', 'runStuck1234', n, false, n === 5]));
  check('T-A2-10 the day done before it is not touched', left.ultimo_ok_giorno, '2026-11-15');
  check('T-A2-10 the next day the stop has run out: a list not read then is the first of a new streak, with no stop',
    (() => { const r = y.afterListLeft(left, { id: 'runStuck1234', status: 'RUNNING' }, 'run still waiting', '2026-11-17T18:40:00Z'); return [r.state.fermo, r.state.fermo_fino, r.state.errori_di_fila, r.stopped_now]; })(),
    ['', '', 1, false]);
  check('T-A2-10 once Apify ends that run well, its list is read and its id leaves the row',
    (() => { const r = y.afterListRun(left, run('SUCCEEDED'), '2026-11-17T18:40:00Z', y.readDataset([item(33, { date: '2026-10-30T10:00:00Z' })], '2026-11-17T18:40:00Z')); return [r.state.apify_run_id, r.read, r.state.errori_di_fila]; })(),
    ['', true, 0]);
  check('T-A2-10 once Apify closes that run it is read as any other, and its id leaves the row',
    (() => { const r = y.afterListRun(left, run('ABORTED'), '2026-11-16T20:40:00Z', null); return [r.state.apify_run_id, r.read, r.stopped_now]; })(), ['', false, false]);
  check('T-A2-10 the id kept is that of the run, also when the copy of the row has none; an id no Apify run has is never written',
    [y.afterListLeft({}, { id: 'runStuck1234' }, 'run still waiting', NOW).state.apify_run_id, thrown(() => y.afterListLeft({}, { id: '' }, 'run still waiting', NOW)),
      thrown(() => y.afterListLeft({}, undefined, 'run still waiting', NOW))],
    ['runStuck1234', 'run: an Apify run with its id required', 'run: an Apify run with its id required']);
  // A resumed run that cannot be read (gone from Apify, a state unknown): each time a failure that
  // takes the id out of the row; the next runs start the list again, and five in a row stop it.
  let lost = { apify_run_id: 'runGone12345' };
  const seen = [];
  for (let i = 0; i < 5; i++) {
    const plan = y.listPlan(lost, '2026-11-16T18:40:00Z');
    const r = y.afterListFailure(lost, plan.action === 'resume' ? 'resumed run: HTTP 404' : 'run FAILED', '2026-11-16T18:40:00Z');
    lost = r.state;
    seen.push([plan.action, r.state.apify_run_id, r.stopped_now]);
  }
  check('T-A2-10 a resumed run that cannot be read leaves the row and counts; five in a row stop the list',
    seen, [['resume', '', false], ['start', '', false], ['start', '', false], ['start', '', false], ['start', '', true]]);
  check('T-A2-10 and the next day the list starts again', y.listPlan(lost, '2026-11-17T18:40:00Z').action, 'start');
  const day = y.afterListRun({}, run('SUCCEEDED', { startedAt: '2026-11-16T20:05:00Z' }), '2026-11-17T06:10:00Z', y.readDataset([item(32, { date: '2026-10-30T10:00:00Z' })], '2026-11-17T06:10:00Z'));
  check('T-A2-12 a run of the 21:00 of the 16th read the next morning closes the 16th, not the 17th',
    [day.state.ultimo_ok_giorno, y.listPlan(day.state, '2026-11-17T18:40:00Z').action], ['2026-11-16', 'start']);
}

console.log('T-A2-12 — the cadence of the list and the five videos a day, with a fake clock');
{
  const complete = y.readDataset([item(31, { date: '2026-10-30T10:00:00Z' })], NOW);
  check('T-A2-12 not asked before 19:00 in Rome', y.listPlan({}, '2026-11-16T17:00:00Z').action, 'none');
  check('T-A2-12 asked in the first run from 19:00', y.listPlan({}, '2026-11-16T18:35:00Z').action, 'start');
  const done = y.afterListRun({}, run('SUCCEEDED'), '2026-11-16T18:40:00Z', complete).state;
  check('T-A2-12 once a complete list is read, not asked again that day', y.listPlan(done, '2026-11-16T20:35:00Z').action, 'none');
  const short = y.afterListRun({}, run('SUCCEEDED'), '2026-11-16T18:40:00Z', y.readDataset([], NOW)).state;
  check('T-A2-12 an incomplete list is asked again in the 21:00 run', y.listPlan(short, '2026-11-16T20:35:00Z').action, 'start');
  check('T-A2-12 a failed run too', y.listPlan(y.afterListRun({}, run('FAILED'), '2026-11-16T18:40:00Z', null).state, '2026-11-16T20:35:00Z').action, 'start');
  check('T-A2-12 the days of the window ask for the videos they need',
    [y.videosToAsk('2026-11-16T19:00:00Z'), y.videosToAsk('2027-01-15T19:00:00Z'), y.videosToAsk('2027-05-01T19:00:00Z')], [68, 248, 300]);
  check('T-A2-12 the input of the Actor names the channel by its id and how many of its newest long videos', y.actorInput(NOW),
    { channelId: y.CHANNEL_ID, maxResults: 68, videoType: 'long', sortOrder: 'latest' });
  let slot = {};
  const taken = [];
  for (let i = 0; i < 6; i++) {
    const t = y.takeVideoSlot(slot, NOW);
    taken.push(t.ok);
    if (t.ok) slot = t.fields;
  }
  check('T-A2-12 at most five videos a day of Rome', taken, [true, true, true, true, true, false]);
  check('T-A2-12 the next day of Rome counts again', y.takeVideoSlot(slot, '2026-11-16T23:30:00Z').fields, { giorno: '2026-11-17', conteggio_giorno: 1 });
}

console.log('the n8n adapter');
function runNode(json) {
  return new Function('$input', '$json', 'require', 'URL', 'URLSearchParams', 'process', 'module', src)(
    { item: { json } }, json, require, undefined, undefined, undefined, undefined);
}
{
  const plan = runNode({ stage: 'plan', list_row: { apify_run_id: 'runY' }, actor: 'inventato~elenco' });
  check('plan: a run left behind is resumed, and no new run starts', [plan.json.plan.action, plan.json.start], ['resume', null]);
  const real = new Date().toISOString();
  const okRun = run('SUCCEEDED', { startedAt: ago(real, 600000), finishedAt: ago(real, 60000) });
  const ok = runNode({ stage: 'dataset', run: okRun, items: [item(1, { date: ago(real, 3600000) }), item(2, { date: '2026-10-30T10:00:00Z' })], list_row: {} });
  check('dataset: the recordings, the cost file, and the items not carried on',
    [ok.json.list.records.length, ok.json.list.complete, ok.json.cost_file_name, JSON.parse(ok.json.cost_file).quantita, 'items' in ok.json], [1, true, 'costo_apify_runSUCCEEDED.json', 2, false]);
  const ko = runNode({ stage: 'dataset', run: run('FAILED', { startedAt: ago(real, 600000), finishedAt: ago(real, 60000) }), list_row: { errori_di_fila: 4 } });
  check('dataset: the fifth failed run, its list not read, its cost file and the alert of the stop',
    [ko.json.list.complete, ko.json.list_state.errori_di_fila, ko.json.list_stopped_now, /^AVVISO_A_.*_youtube_elenco\.json$/.test(ko.json.alert.name), JSON.parse(ko.json.cost_file).quantita],
    [false, 5, true, true, null]);
  check('dataset: a run still running is an error, with no cost written',
    thrown(() => runNode({ stage: 'dataset', run: run('RUNNING', { startedAt: real }), list_row: {} })), 'run_not_finished: RUNNING');
  check('slot: the five videos of the day, from its stage', runNode({ stage: 'slot', slot_row: {} }).json.slot.ok, true);
  const unreadDs = runNode({ stage: 'dataset', run: okRun, items: { error: 'x' }, list_row: {} });
  check('dataset: a dataset not read gives an incomplete reading for the register and the alert, and counts',
    [unreadDs.json.list.complete, unreadDs.json.list.reason, unreadDs.json.list_state.errori_di_fila, JSON.parse(unreadDs.json.cost_file).quantita],
    [false, 'list not read: dataset not read', 1, null]);
  check('dataset: that reading reaches the alert of the run',
    state.runAlert(state.runLog({ workflow: 'w', started_at: NOW, finished_at: NOW, readings: [unreadDs.json.list] })).body.incompleti,
    [{ fonte: 'youtube', catalogo: null, reason: 'list not read: dataset not read' }]);
  const gone = runNode({ stage: 'lost', cause: 'run_gone', run_id: 'runGone12345', reason: 'HTTP 404', list_row: { apify_run_id: 'runGone12345', errori_di_fila: 4 } });
  check('lost: a run that cannot be read: out of the row, the fifth failure stops the list with its alert, its cost file with nulls',
    [gone.json.list_state.apify_run_id, gone.json.list_stopped_now, !!gone.json.alert, gone.json.cost_file_name, JSON.parse(gone.json.cost_file).usd],
    ['', true, true, 'costo_apify_runGone12345.json', null]);
  const refused = runNode({ stage: 'lost', cause: 'start_refused', reason: 'HTTP 402', list_row: {} });
  check('lost: a start that Apify refused counts, with no cost file (no run was made)',
    [refused.json.list_state.errori_di_fila, refused.json.cost, refused.json.list.reason], [1, null, 'list not read: start_refused: HTTP 402']);
  check('lost: a block or a server error of the API is not a cause, and a run gone needs its id',
    [thrown(() => runNode({ stage: 'lost', cause: 'block', list_row: {} })), thrown(() => runNode({ stage: 'lost', cause: 'run_gone', list_row: {} }))],
    ['lost_cause_invalid: "block"', 'lost: the id of the run required']);
  check('started: the run id for the list\'s row', runNode({ stage: 'started', run: { id: 'runXabc123' } }).json.fields, { apify_run_id: 'runXabc123' });
  const pollNext = (r) => runNode({ stage: 'poll', run: r, list_row: {} }).json.next;
  const leftRun = run('RUNNING', { id: 'runStuck1234', startedAt: ago(real, 21 * 60000), finishedAt: null, usageTotalUsd: 0.01 });
  check('poll: wait, settle, read, leave and lost, from its stage',
    [pollNext(run('RUNNING', { startedAt: ago(real, 60000) })), pollNext(run('SUCCEEDED', { startedAt: ago(real, 600000), finishedAt: real })), pollNext(okRun),
      pollNext(leftRun), pollNext({ id: 'runStrano123', status: 'STRANO' })],
    ['wait', 'settle', 'read', 'leave', 'lost']);
  check('poll: a run waited for writes the decision and nothing else',
    Object.keys(runNode({ stage: 'poll', run: run('RUNNING', { startedAt: ago(real, 60000) }), list_row: {} }).json).sort(), ['list_row', 'next', 'reason', 'run', 'stage']);
  const left1 = runNode({ stage: 'poll', run: leftRun, list_row: { apify_run_id: 'runStuck1234', errori_di_fila: 3, ultimo_ok_giorno: '2026-11-15' } });
  check('poll: a run left still waiting gives its list as not read, counts, keeps its id in the row and writes no cost',
    [left1.json.next, left1.json.list.complete, left1.json.list.reason, left1.json.list_reason === left1.json.reason, left1.json.list_state.apify_run_id,
      left1.json.list_state.errori_di_fila, left1.json.list_stopped_now, left1.json.alert, left1.json.cost, left1.json.cost_file_name, left1.json.cost_file],
    ['leave', false, 'list not read: run still waiting after 20 minutes, or without a start time: left for the next run', true, 'runStuck1234', 4, false, null, null, null, null]);
  check('poll: that reading reaches the alert of the run',
    state.runAlert(state.runLog({ workflow: 'w', started_at: NOW, finished_at: NOW, readings: [left1.json.list] })).body.incompleti,
    [{ fonte: 'youtube', catalogo: null, reason: left1.json.list.reason }]);
  const left5 = runNode({ stage: 'poll', run: leftRun, list_row: left1.json.list_state });
  check('poll: the fifth in a row stops the list with its alert, and the run left is still the one resumed',
    [left5.json.list_state.errori_di_fila, left5.json.list_stopped_now, /^AVVISO_A_.*_youtube_elenco\.json$/.test(left5.json.alert.name), y.listPlan(left5.json.list_state, real)],
    [5, true, true, { action: 'resume', run_id: 'runStuck1234' }]);
  check('poll: a run left with an id no Apify run has is an error',
    thrown(() => runNode({ stage: 'poll', run: run('RUNNING', { id: 'r1/../x', startedAt: ago(real, 21 * 60000) }), list_row: {} })), 'run: an Apify run with its id required');
  const strangeRun = { id: 'runStrano123', actId: 'inventato~elenco', status: 'PAUSED', startedAt: ago(real, 3600000), usageTotalUsd: 0.2 };
  const strange = runNode({ stage: 'lost', cause: 'state_unknown', run_id: 'runStrano123', reason: y.pollDecision(strangeRun, real).reason, run: strangeRun,
    list_row: { apify_run_id: 'runStrano123' } });
  check('lost: a run in a state unknown counts and leaves the row; its cost file keeps what Apify declared, and the cause is said once',
    [strange.json.list_state.apify_run_id, strange.json.list_state.errori_di_fila, strange.json.list.reason, strange.json.cost_file_name]
      .concat(['usd', 'status', 'actor', 'quantita'].map((k) => JSON.parse(strange.json.cost_file)[k])),
    ['', 1, 'list not read: state_unknown: status "PAUSED"', 'costo_apify_runStrano123.json', 0.2, 'PAUSED', 'inventato~elenco', null]);
  check('lost: the cost of another run, or a state that is not a text, is never written for this one',
    [JSON.parse(runNode({ stage: 'lost', cause: 'state_unknown', run_id: 'runStrano123', run: { id: 'runAltro12345', status: 'PAUSED', usageTotalUsd: 9 }, list_row: {} }).json.cost_file).usd,
      JSON.parse(runNode({ stage: 'lost', cause: 'state_unknown', run_id: 'runStrano123', run: { id: 'runStrano123', status: { a: 1 }, usageTotalUsd: 0.2 }, list_row: {} }).json.cost_file).status,
      JSON.parse(runNode({ stage: 'lost', cause: 'run_gone', run_id: 'runStrano123', run: strangeRun, list_row: {} }).json.cost_file).usd],
    [null, null, null]);
}

console.log('what the node may use inside n8n, and no request to YouTube');
const code = src.replace(/\/\*[\s\S]*?\*\/|\/\/.*$/gm, '');
check('no URL global', /\bURL\b|URLSearchParams/.test(code), false);
check('no process', /\bprocess\b/.test(code), false);
check('no module required', code.match(/require\('[^']+'\)/g), null);
check('T-A2-10 the node makes no request', /httpRequest|helpers/.test(code), false);
check('T-A2-10 the input of the Actor names the channel by its id, no address of YouTube', JSON.stringify(y.actorInput(NOW)).includes('youtube.com'), false);

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

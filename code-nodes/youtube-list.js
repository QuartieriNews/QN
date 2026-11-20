/**
 * youtube-list.js — workstream A: the list of the videos of the Municipio I channel from an
 * Actor of Apify (DEC-037, points 2 and 3) — when a run asks for it and how many videos, the
 * request that starts the Actor's run with its own limits, the wait for it, what a video brings
 * (read as the record of registrazioni/ needs it), whether the list covers the window, the cost
 * file of the run, the streak of failed runs that stops the list, a run left behind by a dead
 * execution, and the five videos a day the audio may take. The rules are in
 * docs/pilota/CONTRATTI.md, section 7 («A · Amministrazione», rows Fonti, Raccolta,
 * Registrazione and Costi); this file does not restate them. n8n asks nothing of YouTube: the
 * Apify calls are HTTP Request nodes with the Apify credential, each after source-guard.js says
 * Apify may be asked ('may') and judged by it after ('answer'); a stopped Apify never reaches the
 * stages here. Acceptance: tests/test_youtube_list.js (T-A2-09, T-A2-10, T-A2-12, T-A2-15, T-A2-16).
 *
 * The Actor of the list is LIST_ACTOR, chosen at the trial of 20 November 2026 (WORKSTREAM_A,
 * sections 6 and 7): actorInput is its input and ACTOR_FIELDS the fields its items have; the
 * tests run on invented items of that form.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item") the same file runs
 * its adapter. `stage` on the item says which step it takes:
 *   - 'plan': whether this run starts the list, resumes a run left behind, or does nothing;
 *   - 'poll': whether to wait for the run, read it, or stop waiting; a run left still waiting
 *     gives its list as not read in this run, counted, with its id kept in the row;
 *   - 'dataset': the finished run and its items become the recordings of the window, the cost
 *     entry, the list's new state and, when it stops, its alert;
 *   - 'lost': a start Apify refused, a resumed run Apify does not have, or a run in a state no
 *     list here knows (LOST_CAUSES), counted as a failed run, with the cost file of a run that has
 *     an id. A block or a server error of the Apify API is not lost: it stops Apify
 *     (source-guard.js), or leaves the run's id in the row for the next run (WORKSTREAM_A,
 *     section 4);
 *   - 'slot': whether the audio may take one more video today.
 */
'use strict';

/** CONTRATTI section 7 (A), rows Fonti and Registrazione (`municipality_code`). */
const CHANNEL_ID = 'UCEZtd0d0UV5e8ZCWkNOiNjw';
const MUNICIPALITY = 'I';
/** CONTRATTI section 7 (A), row Raccolta: the window, the cadence, the number of videos. */
const WINDOW_DAYS = 100;
const FIRST_DAY_START = '2026-10-31T23:00:00Z'; // 1 November 2026, 00:00 in Rome
const DAY_MS = 24 * 3600 * 1000;
const LIST_FROM_HOUR = 19;
const MAX_VIDEOS = 300;
const PER_DAY = 3;
const MARGIN = 20;
const RUNS_FAILED_TO_STOP = 5;
/** DEC-037, point 2. */
const VIDEOS_PER_DAY = 5;
/** The limits of one run of the list, as code-nodes/apify-run.js has them for channel C: Apify
 *  stops the run at RUN_TIMEOUT_S, the flow stops waiting at MAX_WAIT_MS from its start, and a
 *  cost is read SETTLE_MS after the run ends. No cap of the charge: what a run is charged above
 *  its `maxItems` shows in its cost file (DEC-037, point 6; WORKSTREAM_A, section 4). */
const RUN_TIMEOUT_S = 900;
const MAX_WAIT_MS = 20 * 60 * 1000;
const SETTLE_MS = 15 * 1000;
const WAITING = ['READY', 'RUNNING', 'TIMING-OUT', 'ABORTING'];
const FAILED = ['FAILED', 'ABORTED', 'TIMED-OUT'];
const LOST_CAUSES = Object.freeze(['start_refused', 'run_gone', 'state_unknown']);

const ROME = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23' });
function instant(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(v) || Number.isNaN(Date.parse(v))) {
    throw new Error('now must be a UTC instant');
  }
  return v;
}
function rome(iso) {
  const p = Object.fromEntries(ROME.formatToParts(new Date(instant(iso))).map((x) => [x.type, x.value]));
  return { day: `${p.year}-${p.month}-${p.day}`, hour: Number(p.hour) };
}
function nextDay(day) {
  const d = new Date(`${day}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + 1);
  return d.toISOString().slice(0, 10);
}

const windowStartMs = (now) => Math.max(Date.parse(instant(now)) - WINDOW_DAYS * DAY_MS, Date.parse(FIRST_DAY_START));
const inWindow = (referenceUtc, now) => {
  const t = Date.parse(referenceUtc);
  return !Number.isNaN(t) && t >= windowStartMs(now);
};

/** T-A2-12: how many videos a run asks for. */
function videosToAsk(now) {
  const days = Math.max(1, Math.ceil((Date.parse(now) - windowStartMs(now)) / DAY_MS));
  return Math.min(MAX_VIDEOS, days * PER_DAY + MARGIN);
}

/** The list Actor (see the head of this file), as the Apify API names it. */
const LIST_ACTOR = 'grow_media~youtube-channel-video-scraper';

/** T-A2-12: the input of LIST_ACTOR — the channel by its id, its newest long videos first, as many
 *  as a run asks for. The Actor takes one `videoType` a run; its Shorts listing of this channel was
 *  empty at the trial, and its long listing carries the short videos (WORKSTREAM_A, section 9). */
function actorInput(now) {
  return { channelId: CHANNEL_ID, maxResults: videosToAsk(now), videoType: 'long', sortOrder: 'latest' };
}

/** T-A2-16: an Actor the flow names must be LIST_ACTOR; no other is ever started. */
function listActor(actor) {
  if (actor !== undefined && actor !== null && actor !== LIST_ACTOR) throw new Error('actor_not_list_actor');
  return LIST_ACTOR;
}

/** T-A2-16: the request that starts a run of LIST_ACTOR, with the run's timeout and the cap of
 *  its results in the request itself (WORKSTREAM_A, section 4). */
function startRequest(now) {
  const n = videosToAsk(now);
  return { url: `https://api.apify.com/v2/acts/${LIST_ACTOR}/runs?timeout=${RUN_TIMEOUT_S}&maxItems=${n}`, method: 'POST', body: actorInput(now), asked: n };
}

/** The fields an item of LIST_ACTOR is read from, first valid one wins (see the head of this file).
 *  It gives no start of a live broadcast (WORKSTREAM_A, section 6): the reference of its videos is
 *  their publication (CONTRATTI section 7 (A), row Raccolta). */
const ACTOR_FIELDS = Object.freeze({
  id: ['id'], url: ['url'], channel: ['channelId'], channel_name: ['channelName'],
  published: ['date'], live_start: [], duration: ['durationSeconds', 'duration'],
});
const first = (raw, names) => names.map((n) => raw[n]).find((v) => v !== undefined && v !== null && v !== '');
const VIDEO_ID = /^[A-Za-z0-9_-]{11}$/;
const idFromUrl = (u) => (/(?:[?&]v=|youtu\.be\/|\/live\/|\/shorts\/)([A-Za-z0-9_-]{11})(?:[?&#/]|$)/.exec(typeof u === 'string' ? u : '') || [])[1];

const INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(?:(Z)|([+-])(\d{2}):?(\d{2}))$/;
/** An instant with its offset, in UTC to the second, as romatv-list.js, utcSecond. */
function utcSecond(value) {
  const m = typeof value === 'string' ? INSTANT.exec(value) : null;
  if (!m) return null;
  const [y, mo, d, h, mi] = [1, 2, 3, 4, 5].map((i) => Number(m[i]));
  const s = m[6] === undefined ? 0 : Number(m[6]);
  const [oh, om] = m[7] ? [0, 0] : [Number(m[9]), Number(m[10])];
  const t = new Date(0);
  t.setUTCFullYear(y, mo - 1, d);
  if (t.getUTCFullYear() !== y || t.getUTCMonth() !== mo - 1 || t.getUTCDate() !== d || h > 23 || mi > 59 || s > 59 || oh > 23 || om > 59) return null;
  t.setUTCHours(h, mi, s, 0);
  return new Date(t.getTime() - (m[8] === '-' ? -1 : 1) * (oh * 60 + om) * 60000).toISOString().slice(0, 19) + 'Z';
}

/** A duration in whole seconds: a number of seconds, `h:mm:ss`, `m:ss` or ISO 8601 (`PT1H2M3S`);
 *  none for zero, which is not yet a recording (a live still on, a video not yet processed). */
function seconds(v) {
  let secs = null;
  if (typeof v === 'number') secs = v >= 0 && Number.isFinite(v) ? Math.floor(v) : null;
  else if (typeof v === 'string') {
    let m;
    if (/^\d+$/.test(v)) secs = Number(v);
    else if ((m = /^(\d+):([0-5]\d):([0-5]\d)$/.exec(v))) secs = Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]);
    else if ((m = /^(\d+):([0-5]\d)$/.exec(v))) secs = Number(m[1]) * 60 + Number(m[2]);
    else if ((m = /^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/.exec(v)) && (m[1] || m[2] || m[3])) {
      secs = Number(m[1] || 0) * 3600 + Number(m[2] || 0) * 60 + Number(m[3] || 0);
    }
  }
  return secs > 0 ? secs : null;
}

/** T-A2-09: one item of the Actor as the channel keeps it, or the reason it is not kept. The
 *  reference of a video: CONTRATTI section 7 (A), row Raccolta. A video of YouTube is never bound
 *  as a part of a split sitting (WORKSTREAM_A, section 5, «Il confine»). */
function readVideo(raw) {
  const it = raw && typeof raw === 'object' ? raw : {};
  const id = ACTOR_FIELDS.id.map((n) => it[n]).concat(ACTOR_FIELDS.url.map((n) => idFromUrl(it[n]))).find((v) => typeof v === 'string' && VIDEO_ID.test(v));
  // T-A2-15: the Actor's own error item, in the place of a video.
  if (!id && typeof it.error === 'string' && it.error) return { ok: false, reason: 'actor_error', id: null };
  if (!id) {
    const shown = first(it, ACTOR_FIELDS.id);
    return { ok: false, reason: 'video_id_invalid', id: typeof shown === 'string' ? shown.slice(0, 40) : null };
  }
  const channel = first(it, ACTOR_FIELDS.channel);
  if (channel !== undefined && channel !== CHANNEL_ID) return { ok: false, reason: 'other_channel', id };
  const published = utcSecond(first(it, ACTOR_FIELDS.published));
  const live = utcSecond(first(it, ACTOR_FIELDS.live_start));
  if (!published && !live) return { ok: false, reason: 'date_invalid', id };
  const duration = seconds(first(it, ACTOR_FIELDS.duration));
  if (duration === null) return { ok: false, reason: 'duration_invalid', id };
  const title = typeof it.title === 'string' ? it.title : '';
  const name = first(it, ACTOR_FIELDS.channel_name);
  return { ok: true, rec: {
    recording_ref: `youtube:${id}`, piattaforma: 'youtube', canale: typeof name === 'string' ? name : '', source_id: CHANNEL_ID,
    municipality_code: MUNICIPALITY, organo: title.trim(), titolo: title, numero_parte: null,
    ora_riferimento_utc: live || published, ora_pubblicazione_utc: published || '', durata_secondi: duration,
    trascrizione_piattaforma: false, url: `https://www.youtube.com/watch?v=${id}`,
  } };
}

/** T-A2-09: the items of a finished run of the Actor, by the builder's reading of CONTRATTI
 *  section 7 (A), row Raccolta, on when the list covers the window. */
function readDataset(items, now) {
  const records = [];
  const skipped = [];
  const seen = new Set();
  let beyond = 0;
  for (const raw of items) {
    const v = readVideo(raw);
    if (!v.ok) { skipped.push({ id: v.id, reason: v.reason }); continue; }
    if (seen.has(v.rec.recording_ref)) { skipped.push({ id: v.rec.recording_ref.slice(8), reason: 'repeated in the list' }); continue; }
    seen.add(v.rec.recording_ref);
    if (inWindow(v.rec.ora_riferimento_utc, now)) records.push(v.rec); else beyond += 1;
  }
  const reason = beyond > 0 ? null : !items.length ? 'empty list' : !records.length ? 'no valid video in the list'
    : 'the list does not reach the start of the window';
  return { fonte: 'youtube', records, skipped, complete: beyond > 0, reason };
}

/** Whether to wait for a run, read it, leave it for the next run, or count it lost: as
 *  apify-run.js, pollDecision, with the limits of the list. A run read is finished and its cost
 *  settled, or MAX_WAIT_MS from its start have passed; without a start time only an end time
 *  SETTLE_MS fresh makes it wait. A run still waiting after MAX_WAIT_MS is left: its id stays in
 *  the row and the next run resumes it, cost included (afterListLeft). Only a state that no list
 *  here knows goes to 'lost' (`state_unknown`). */
function pollDecision(run, now) {
  const status = run && typeof run.status === 'string' ? run.status : null;
  const started = Date.parse(run && run.startedAt);
  const late = Number.isNaN(started) || Date.parse(now) - started >= MAX_WAIT_MS;
  if (status === 'SUCCEEDED' || FAILED.includes(status)) {
    const sinceEnd = Date.parse(now) - Date.parse(run.finishedAt);
    if (!late && (Number.isNaN(sinceEnd) || sinceEnd < SETTLE_MS)) return { next: 'settle', reason: null };
    if (Number.isNaN(started) && sinceEnd > -MAX_WAIT_MS && sinceEnd < SETTLE_MS) return { next: 'settle', reason: null };
    return { next: 'read', reason: null };
  }
  if (WAITING.includes(status)) {
    if (late) return { next: 'leave', reason: 'run still waiting after 20 minutes, or without a start time: left for the next run' };
    return { next: 'wait', reason: null };
  }
  return { next: 'lost', reason: `status ${JSON.stringify(status)}` };
}

/** A run the stage 'dataset' may take: finished, with its cost settled. */
function finishedRun(run, now) {
  if (!run || typeof run.id !== 'string' || !run.id) throw new Error('run: an Apify run with its id required');
  if (pollDecision(run, now).next !== 'read') throw new Error(`run_not_finished: ${run.status}`);
  return run;
}

/** CONTRATTI section 7 (A), row Costi: the cost entry of a run of the list Actor, failed or not,
 *  in the form of code-nodes/apify-run.js; a run that cannot be read has its id and nulls. */
function costEntry(run, count) {
  const usd = typeof run.usageTotalUsd === 'number' && Number.isFinite(run.usageTotalUsd) ? run.usageTotalUsd : null;
  return { workstream: 'A', servizio: 'apify', actor: run.actId || null, run_id: run.id, recording_ref: null,
    started_at: run.startedAt || null, finished_at: run.finishedAt || null, status: run.status || null,
    unita: 'video_elencati', quantita: run.status === 'SUCCEEDED' && Number.isInteger(count) && count >= 0 ? count : null, usd };
}
const costFileName = (entry) => `costo_apify_${String(entry.run_id).replace(/[^A-Za-z0-9_-]/g, '_')}.json`;

/** The list's own state, in its row of the Data table (`fonte:youtube_elenco`). A stop is read as
 *  in source-guard.js, isStopped: anything but `giorno` with a valid day is a stop by the owner. */
function listState(row) {
  const r = row || {};
  return { fermo: r.fermo || '', fermo_fino: r.fermo_fino || '', errori_di_fila: Number(r.errori_di_fila) || 0,
    ultimo_ok_giorno: r.ultimo_ok_giorno || '', apify_run_id: r.apify_run_id || '', motivo: r.motivo || '' };
}
function listStopped(s, day) {
  if (!s.fermo) return false;
  if (s.fermo === 'giorno' && /^\d{4}-\d{2}-\d{2}$/.test(s.fermo_fino)) return day < s.fermo_fino;
  return true;
}

/** T-A2-12: what this run does with the list. A run left in the row (by an execution that died,
 *  or still waiting) is resumed for its cost and its list before any new run, also with the list
 *  stopped: resuming asks nothing of YouTube (WORKSTREAM_A, section 4). Then the cadence of
 *  CONTRATTI section 7 (A), row Raccolta. */
function listPlan(row, now) {
  const s = listState(row);
  const { day, hour } = rome(now);
  if (s.apify_run_id) return { action: 'resume', run_id: s.apify_run_id };
  if (listStopped(s, day)) return { action: 'none', run_id: null };
  return { action: hour >= LIST_FROM_HOUR && s.ultimo_ok_giorno !== day ? 'start' : 'none', run_id: null };
}

/** The field the flow writes in the list's row as soon as a run starts, before waiting for it. */
function startedFields(run) {
  if (!run || typeof run.id !== 'string' || !/^[A-Za-z0-9]{6,40}$/.test(run.id)) throw new Error('run: an Apify run with its id required');
  return { apify_run_id: run.id };
}

/** T-A2-09, T-A2-10: the list's new state after a finished run (its id leaves the row). A run that
 *  failed leaves the list unread and counts in the streak; RUNS_FAILED_TO_STOP in a row stop it
 *  until the next day of Rome. A run that succeeded ends the streak; the day is done only when its
 *  list covered the window, so an incomplete list is asked again in a later run of the day. */
function afterListRun(row, run, now, dataset) {
  if (run.status === 'SUCCEEDED' && dataset) {
    const s = lifted(listState(row), now);
    s.apify_run_id = '';
    s.errori_di_fila = 0;
    // The day done is the day of Rome the run started (a run resumed the next morning closes the
    // evening before, not the new day).
    if (dataset.complete) s.ultimo_ok_giorno = rome(utcSecond(run.startedAt) || now).day;
    return { state: s, read: true, stopped_now: false, reason: null };
  }
  return afterListFailure(row, run.status === 'SUCCEEDED' ? 'dataset not read' : `run ${run.status}`, now);
}

function lifted(s, now) {
  const { day } = rome(now);
  if (s.fermo === 'giorno' && /^\d{4}-\d{2}-\d{2}$/.test(s.fermo_fino) && day >= s.fermo_fino) {
    Object.assign(s, { fermo: '', fermo_fino: '', errori_di_fila: 0, motivo: '' });
  }
  return s;
}

/** A list that was not read: a failed run, a dataset not read, a run that cannot be read, a
 *  start Apify refused or a run left still waiting. The failure counts in the streak. The run's
 *  id leaves the row, except that of a run left (`leftRunId`), which the next run resumes. */
function afterListFailure(row, reason, now, leftRunId) {
  const s = lifted(listState(row), now);
  const { day } = rome(now);
  s.apify_run_id = leftRunId || '';
  s.errori_di_fila += 1;
  if (s.errori_di_fila >= RUNS_FAILED_TO_STOP && !listStopped(s, day)) {
    Object.assign(s, { fermo: 'giorno', fermo_fino: nextDay(day), motivo: `${now} ${RUNS_FAILED_TO_STOP} failed runs of the list in a row` });
    return { state: s, read: false, stopped_now: true, reason };
  }
  return { state: s, read: false, stopped_now: false, reason };
}

/** T-A2-10: a run left still waiting (pollDecision, 'leave'). Its list is not read in this run,
 *  which counts as a failed run does (WORKSTREAM_A, section 4); its id stays in the row, taken
 *  from the run and checked as when it was first written, whatever the copy of the row says. */
function afterListLeft(row, run, reason, now) {
  return afterListFailure(row, reason, now, startedFields(run).apify_run_id);
}

/** The reading of a list not read, for the register and the alert (recording-state.js, runLog). */
const unread = (reason) => ({ fonte: 'youtube', records: [], skipped: [], complete: false, reason: `list not read: ${reason}` });

const stamp = (iso) => new Date(iso).toISOString().slice(0, 19).replace(/[-:]/g, '') + 'Z';
/** The alert of the list stopped now, named as those of staging_A_avviso. */
function stopAlert(state, now) {
  return { name: `AVVISO_A_${stamp(now)}_youtube_elenco.json`,
    body: { avviso: 'il canale A ha fermato l\'elenco di YouTube: avvisare l\'owner (CONTRATTI, sezione 7 A, «Raccolta»)',
      fonte: 'youtube_elenco', fermo: state.fermo, fermo_fino: state.fermo_fino, motivo: state.motivo, alle: now } };
}

/** T-A2-12: whether the audio may take one more video today (`fonte:youtube_audio`), and the
 *  counter it writes when it does. */
function takeVideoSlot(row, now) {
  const { day } = rome(now);
  const r = row || {};
  const count = r.giorno === day ? Number(r.conteggio_giorno) || 0 : 0;
  if (count >= VIDEOS_PER_DAY) return { ok: false, fields: null };
  return { ok: true, fields: { giorno: day, conteggio_giorno: count + 1 } };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { CHANNEL_ID, MUNICIPALITY, WINDOW_DAYS, LIST_FROM_HOUR, MAX_VIDEOS, PER_DAY, MARGIN, RUNS_FAILED_TO_STOP,
    VIDEOS_PER_DAY, RUN_TIMEOUT_S, MAX_WAIT_MS, SETTLE_MS, WAITING, FAILED, LOST_CAUSES, LIST_ACTOR, ACTOR_FIELDS, rome, windowStartMs, inWindow, videosToAsk,
    actorInput, listActor, startRequest, utcSecond, seconds, readVideo, readDataset, pollDecision, finishedRun, costEntry, costFileName, listState,
    listPlan, startedFields, afterListRun, afterListFailure, afterListLeft, stopAlert, takeVideoSlot };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. 'plan' reads `list_row` and, if the flow
 * names one, `actor`, which must be LIST_ACTOR whatever the plan, and writes `plan` and, to start,
 * `start` (the request) and `asked`; 'started' reads `run` and writes
 * `fields` (the run's id for the list's row); 'poll' reads `run` and writes `next` and `reason`,
 * and to leave the run it reads `list_row` too; 'dataset' reads `run`, `items` (the dataset of a
 * run that succeeded, when it could be read) and `list_row`; 'lost' reads `cause` (LOST_CAUSES),
 * `run_id` (none for a start refused), `reason`, `list_row` and, for a state unknown, `run` as
 * Apify gave it. 'dataset', 'lost' and a 'poll' that leaves the run write `list` (a reading,
 * incomplete when not read), `list_state`, `list_stopped_now`, `alert` and `cost`,
 * `cost_file_name` and `cost_file`: those of a run with an id, null for a run left (its cost is
 * read with the run) and for a start refused. 'slot' reads `slot_row` and writes `slot`. */
const now = new Date().toISOString();
if ($json.stage === 'plan') {
  listActor($json.actor);
  const plan = listPlan($json.list_row, now);
  const start = plan.action === 'start' ? startRequest(now) : null;
  Object.assign($json, { plan, start, asked: start ? start.asked : null });
  return $input.item;
}
if ($json.stage === 'started') {
  $json.fields = startedFields($json.run);
  return $input.item;
}
if ($json.stage === 'poll') {
  const decision = pollDecision($json.run, now);
  Object.assign($json, decision);
  if (decision.next === 'leave') {
    const after = afterListLeft($json.list_row, $json.run, decision.reason, now);
    Object.assign($json, { list: unread(decision.reason), list_state: after.state, list_stopped_now: after.stopped_now,
      list_reason: decision.reason, alert: after.stopped_now ? stopAlert(after.state, now) : null,
      cost: null, cost_file_name: null, cost_file: null });
  }
  return $input.item;
}
if ($json.stage === 'dataset') {
  const run = finishedRun($json.run, now);
  const items = run.status === 'SUCCEEDED' && Array.isArray($json.items) ? $json.items : null;
  const read = items ? readDataset(items, now) : null;
  const after = afterListRun($json.list_row, run, now, read);
  const cost = costEntry(run, items ? items.length : null);
  Object.assign($json, { list: read || unread(after.reason), list_state: after.state, list_stopped_now: after.stopped_now,
    list_reason: after.reason, alert: after.stopped_now ? stopAlert(after.state, now) : null,
    cost, cost_file_name: costFileName(cost), cost_file: JSON.stringify(cost, null, 2) + '\n' });
  delete $json.items;
  return $input.item;
}
if ($json.stage === 'lost') {
  if (!LOST_CAUSES.includes($json.cause)) throw new Error(`lost_cause_invalid: ${JSON.stringify($json.cause)}`);
  if ($json.cause !== 'start_refused' && !$json.run_id) throw new Error('lost: the id of the run required');
  const reason = `${$json.cause}${$json.reason ? `: ${String($json.reason).slice(0, 200)}` : ''}`;
  const after = afterListFailure($json.list_row, reason, now);
  // A run in a state unknown answered: its cost entry is the run as Apify gave it.
  const answered = $json.cause === 'state_unknown' && $json.run && $json.run.id === String($json.run_id);
  const lostRun = answered ? Object.assign({}, $json.run, { status: typeof $json.run.status === 'string' ? $json.run.status : null })
    : { id: String($json.run_id), status: null };
  const cost = $json.cause !== 'start_refused' ? costEntry(lostRun, null) : null;
  Object.assign($json, { list: unread(reason), list_state: after.state, list_stopped_now: after.stopped_now, list_reason: reason,
    alert: after.stopped_now ? stopAlert(after.state, now) : null,
    cost, cost_file_name: cost ? costFileName(cost) : null, cost_file: cost ? JSON.stringify(cost, null, 2) + '\n' : null });
  return $input.item;
}
if ($json.stage === 'slot') {
  $json.slot = takeVideoSlot($json.slot_row, now);
  return $input.item;
}
throw new Error(`youtube-list.js: unknown stage ${JSON.stringify($json.stage)}`);

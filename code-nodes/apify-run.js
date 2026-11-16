/**
 * apify-run.js — workstream C: one paid Apify run of the Facebook events reader, from the request
 * to its cost. It closes the defects that the review of PR #48 found in staging_C_fb_events_fetch
 * (workflows/README.md): a run that does not end SUCCEEDED never reaches the dataset, the run and
 * the wait for it have an end, and every run that ends, failed or not, leaves its settled cost
 * (docs/pilota/CONTRATTI.md, «Costi»). A retried
 * request is still not recognised: that needs a record visible to a second execution while the first
 * runs, and stays in the list of workflows/README.md.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item", JavaScript) the same
 * file runs its adapter. `stage` on the item says which step it takes:
 *   - 'input': the webhook body becomes the Apify input, within its caps, or the request for a
 *     saved dataset that takes the place of a run (workflows/README.md, «Prova senza Apify»);
 *   - 'poll': the state of the run says whether to wait, read the dataset or stop;
 *   - 'cost': the finished run becomes one cost entry;
 *   - 'fixture': the saved dataset, read from its file, becomes the events a run would have given.
 */
'use strict';

/** The caps of a request, as the workflow had them before this file. */
const MAX_URLS = 60;
const MAX_EVENTS_PER_URL = 5;
/** The run's own timeout, set when the workflow starts it: Apify stops the paid run at this
 *  point, as TIMED-OUT. */
const APIFY_TIMEOUT_S = 3600;
/** How long the workflow waits for one run before it stops: past the run's own timeout, so the
 *  last state it reads is Apify's. */
const MAX_WAIT_MS = 75 * 60 * 1000;
/** Apify's costs settle a few seconds after a run ends: a run that ended more recently is read
 *  again before its cost is written. */
const SETTLE_MS = 15 * 1000;
/** Apify's run states: the waiting ones include the two in transition to an end, which have no
 *  `finishedAt` yet and stay under MAX_WAIT_MS. */
const WAITING = ['READY', 'RUNNING', 'TIMING-OUT', 'ABORTING'];
const FAILED = ['FAILED', 'ABORTED', 'TIMED-OUT'];

/** Stage 'input': the Apify input of one request; one outside the caps stops before any paid call. */
function buildInput(body) {
  const b = body || {};
  const urls = Array.isArray(b.startUrls) ? b.startUrls : [];
  const clean = [...new Set(urls.map((u) => String(u).trim()).filter((u) => /^https:\/\/(www\.)?facebook\.com\//.test(u)))];
  if (clean.length === 0 || clean.length > MAX_URLS) throw new Error(`startUrls: 1 to ${MAX_URLS} facebook.com URLs required`);
  const maxEvents = Math.min(Math.max(parseInt(b.maxEvents || MAX_EVENTS_PER_URL, 10) || MAX_EVENTS_PER_URL, 1), MAX_EVENTS_PER_URL);
  return { apifyInput: { startUrls: clean.map((url) => ({ url })), maxEvents } };
}

/** Stage 'poll': `next` is 'wait', 'settle', 'read' or 'stop'. A run that ended less than
 *  SETTLE_MS ago is read again first; then only SUCCEEDED reads the dataset, and a failed run stops
 *  after its cost is written. A run still waiting past MAX_WAIT_MS from its start stops too. */
function pollDecision(run, now) {
  const status = run && typeof run.status === 'string' ? run.status : null;
  if (status === 'SUCCEEDED' || (status && FAILED.includes(status))) {
    const finished = Date.parse(run.finishedAt);
    if (Number.isNaN(finished) || Date.parse(now) - finished < SETTLE_MS) return { next: 'settle', reason: null };
    return status === 'SUCCEEDED' ? { next: 'read', reason: null } : { next: 'stop', reason: `run ${status}` };
  }
  if (status && WAITING.includes(status)) {
    const started = Date.parse(run.startedAt);
    if (Number.isNaN(started)) return { next: 'stop', reason: 'run without a start time' };
    if (Date.parse(now) - started >= MAX_WAIT_MS) return { next: 'stop', reason: 'run still waiting after 75 minutes' };
    return { next: 'wait', reason: null };
  }
  return { next: 'stop', reason: `run state ${JSON.stringify(status)}` };
}

/** Stage 'cost': one cost entry of the run (CONTRATTI.md, «Costi»). `usd` is Apify's own total,
 *  in the currency Apify charges (DEC-035); a run that reports none is recorded with `usd: null`,
 *  never with a guessed value. */
function costEntry(run, events) {
  if (!run || typeof run.id !== 'string' || !run.id) throw new Error('run: an Apify run with its id required');
  const usd = typeof run.usageTotalUsd === 'number' && Number.isFinite(run.usageTotalUsd) ? run.usageTotalUsd : null;
  return {
    workstream: 'C', servizio: 'apify', actor: run.actId || null, run_id: run.id,
    started_at: run.startedAt || null, finished_at: run.finishedAt || null, status: run.status || null,
    unita: 'eventi', quantita: Number.isInteger(events) && events >= 0 ? events : null, usd,
  };
}

/** The file of one cost entry: Drive cannot append to `costi.jsonl`, so each entry is a file of
 *  its own (CONTRATTI.md, «Costi»). */
function costFileName(entry) {
  return `costo_apify_${String(entry.run_id).replace(/[^A-Za-z0-9_-]/g, '_')}.json`;
}

/** A saved dataset stands for one run, so it gives at most the events one run can give. */
const MAX_FIXTURE_EVENTS = MAX_URLS * MAX_EVENTS_PER_URL;
const DRIVE_FILE_ID = /^[A-Za-z0-9_-]{20,200}$/;

/** Stage 'input': a body with `fixture` asks for a saved dataset and never reaches Apify; any other
 *  body is a run, within its caps. A body that asks for both stops before any call. */
function buildRequest(body) {
  const b = body || {};
  if (b.fixture === undefined) return buildInput(b);
  if (b.startUrls !== undefined) throw new Error('a request is startUrls or fixture, never both');
  const f = b.fixture !== null && typeof b.fixture === 'object' ? b.fixture : {};
  const fileId = typeof f.file_id === 'string' ? f.file_id.trim() : '';
  if (!DRIVE_FILE_ID.test(fileId)) throw new Error('fixture.file_id: the id of a Drive file required');
  const limit = f.limit === undefined ? MAX_FIXTURE_EVENTS : Number(f.limit);
  if (!Number.isInteger(limit) || limit < 1 || limit > MAX_FIXTURE_EVENTS) throw new Error(`fixture.limit: 1 to ${MAX_FIXTURE_EVENTS}`);
  return { fixture: { file_id: fileId, limit } };
}

/** Stage 'fixture': the file holds a dataset as Apify gives it, a JSON array of events; its first
 *  `limit` events go on where the events of a run would. Any other content stops. */
function fixtureEvents(data, fixture) {
  if (!Array.isArray(data) || data.length === 0) throw new Error('fixture: the file must hold a non-empty JSON array of events');
  if (!data.every((e) => e !== null && typeof e === 'object' && !Array.isArray(e))) throw new Error('fixture: every element of the file must be an event object');
  const f = fixture || {};
  const limit = Number.isInteger(f.limit) && f.limit >= 1 ? Math.min(f.limit, MAX_FIXTURE_EVENTS) : MAX_FIXTURE_EVENTS;
  const events = data.slice(0, limit);
  return { events, fixture: { file_id: typeof f.file_id === 'string' ? f.file_id : null, limit, events: events.length, in_file: data.length } };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { MAX_URLS, MAX_EVENTS_PER_URL, APIFY_TIMEOUT_S, MAX_WAIT_MS, SETTLE_MS, WAITING, FAILED, buildInput, pollDecision, costEntry,
    costFileName, MAX_FIXTURE_EVENTS, buildRequest, fixtureEvents };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. */
if ($json.stage === 'input') {
  return { json: buildRequest($json.body) };
}
if ($json.stage === 'fixture') {
  return { json: fixtureEvents($json.data, $json.fixture) };
}
if ($json.stage === 'poll') {
  Object.assign($json, pollDecision($json.data, new Date().toISOString()));
  return $input.item;
}
if ($json.stage === 'cost') {
  const entry = costEntry($json.run, $json.events);
  const name = costFileName(entry);
  const content = JSON.stringify(entry, null, 2) + '\n';
  return { json: { cost: entry, cost_file_name: name },
    binary: { data: { data: Buffer.from(content, 'utf8').toString('base64'), mimeType: 'application/json', fileName: name } } };
}
throw new Error(`apify-run.js: unknown stage ${JSON.stringify($json.stage)}`);

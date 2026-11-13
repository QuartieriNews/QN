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
 *   - 'input': the webhook body becomes the Apify input, within its caps;
 *   - 'poll': the state of the run says whether to wait, read the dataset or stop;
 *   - 'cost': the finished run becomes one cost entry.
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

/** Stage 'cost': one cost entry of the run (CONTRATTI.md, «Costi»). `usd` is Apify's own total;
 *  a run that reports none is recorded with `usd: null`, never with a guessed value. */
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

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { MAX_URLS, MAX_EVENTS_PER_URL, APIFY_TIMEOUT_S, MAX_WAIT_MS, SETTLE_MS, WAITING, FAILED, buildInput, pollDecision, costEntry,
    costFileName };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. */
if ($json.stage === 'input') {
  return { json: buildInput($json.body) };
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

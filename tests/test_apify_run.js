#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/apify-run.js: the request caps, the decision on each state
 * of an Apify run (only SUCCEEDED reads the dataset, the wait ends after 60 minutes) and the cost
 * entry of a run (docs/pilota/CONTRATTI.md, «Costi»; the defects of workflows/README.md), and the
 * n8n adapter evaluated from the exact committed file with stubbed $input/$json. Every URL and id
 * is invented (DEC-109).
 *
 * Run:  node tests/test_apify_run.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'apify-run.js');
const m = require(FILE);

let failures = 0;
let checks = 0;
function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) console.log(`  ok   ${label}`);
  else { failures += 1; console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`); }
}
function thrown(fn) { try { fn(); return null; } catch (e) { return e.message; } }

const PAGE = 'https://www.facebook.com/pagina-inventata/events';

console.log('input: the caps of a request');
check('facebook URLs, trimmed and without repeats', m.buildInput({ startUrls: [` ${PAGE} `, PAGE, 'https://example.invalid/x'] }),
  { apifyInput: { startUrls: [{ url: PAGE }], maxEvents: 5 } });
check('maxEvents is kept between 1 and 5', [m.buildInput({ startUrls: [PAGE], maxEvents: 9 }).apifyInput.maxEvents,
  m.buildInput({ startUrls: [PAGE], maxEvents: 0 }).apifyInput.maxEvents, m.buildInput({ startUrls: [PAGE], maxEvents: 2 }).apifyInput.maxEvents], [5, 5, 2]);
check('no facebook URL stops before any paid call', /startUrls/.test(thrown(() => m.buildInput({ startUrls: ['https://example.invalid/x'] })) || ''), true);
check('more than 60 URLs stop', /startUrls/.test(thrown(() => m.buildInput({ startUrls: Array.from({ length: 61 }, (_, i) => `${PAGE}?p=${i}`) })) || ''), true);
check('a missing body stops', /startUrls/.test(thrown(() => m.buildInput(undefined)) || ''), true);

console.log('poll: only SUCCEEDED reads the dataset, costs settle, and the wait ends');
const T0 = '2026-11-13T01:00:00.000Z';
const END = '2026-11-13T01:04:00.000Z';
check('SUCCEEDED, settled, reads the dataset', m.pollDecision({ status: 'SUCCEEDED', startedAt: T0, finishedAt: END }, '2026-11-13T01:05:00Z'), { next: 'read', reason: null });
check('SUCCEEDED less than 15 seconds ago is read again first', m.pollDecision({ status: 'SUCCEEDED', startedAt: T0, finishedAt: END }, '2026-11-13T01:04:10Z'), { next: 'settle', reason: null });
check('an ended run without its end time is read again', m.pollDecision({ status: 'SUCCEEDED', startedAt: T0 }, '2026-11-13T01:05:00Z').next, 'settle');
for (const s of ['FAILED', 'ABORTED', 'TIMED-OUT', 'TIMING-OUT', 'ABORTING']) {
  check(`${s} stops, never reads a partial dataset`, m.pollDecision({ status: s, startedAt: T0, finishedAt: END }, '2026-11-13T01:05:00Z'), { next: 'stop', reason: `run ${s}` });
}
check('a failed run settles too, so its cost is the final one', m.pollDecision({ status: 'FAILED', startedAt: T0, finishedAt: END }, '2026-11-13T01:04:05Z').next, 'settle');
check('RUNNING within 75 minutes waits', m.pollDecision({ status: 'RUNNING', startedAt: T0 }, '2026-11-13T02:14:59Z'), { next: 'wait', reason: null });
check('READY waits', m.pollDecision({ status: 'READY', startedAt: T0 }, '2026-11-13T01:10:00Z').next, 'wait');
check('still running at 75 minutes stops', m.pollDecision({ status: 'RUNNING', startedAt: T0 }, '2026-11-13T02:15:00Z'),
  { next: 'stop', reason: 'run still waiting after 75 minutes' });
check('the wait outlasts the run\'s own timeout', m.MAX_WAIT_MS > m.APIFY_TIMEOUT_S * 1000, true);
check('a waiting run without a start time stops', m.pollDecision({ status: 'RUNNING' }, '2026-11-13T01:10:00Z').next, 'stop');
check('an unknown state stops', m.pollDecision({ status: 'PAUSED', startedAt: T0 }, '2026-11-13T01:10:00Z').next, 'stop');
check('no run at all stops', m.pollDecision(undefined, '2026-11-13T01:10:00Z').next, 'stop');

console.log('cost: one entry per run (CONTRATTI «Costi»)');
const RUN = { id: 'runInventato01', actId: 'attoreInventato', status: 'SUCCEEDED', startedAt: T0, finishedAt: '2026-11-13T01:04:00.000Z', usageTotalUsd: 0.18 };
check('the entry of a run', m.costEntry(RUN, 18), { workstream: 'C', servizio: 'apify', actor: 'attoreInventato', run_id: 'runInventato01',
  started_at: T0, finished_at: '2026-11-13T01:04:00.000Z', status: 'SUCCEEDED', unita: 'eventi', quantita: 18, usd: 0.18 });
check('a run that reports no cost is recorded with usd null', m.costEntry(Object.assign({}, RUN, { usageTotalUsd: undefined }), 0).usd, null);
check('a count that is not a whole number is null', m.costEntry(RUN, -1).quantita, null);
check('a run without its id is an error', /run/.test(thrown(() => m.costEntry({ status: 'SUCCEEDED' }, 1)) || ''), true);
check('the file of an entry is named after its run, safely', m.costFileName({ run_id: 'run/../x' }), 'costo_apify_run____x.json');

console.log('n8n adapter, from the exact committed file');
{
  const src = fs.readFileSync(FILE, 'utf8');
  const run = (json) => { const item = { json }; return new Function('$input', '$json', 'require', 'module', src)({ item }, json, require, { exports: {} }); };
  check('input: the Apify input', run({ stage: 'input', body: { startUrls: [PAGE] } }).json, { apifyInput: { startUrls: [{ url: PAGE }], maxEvents: 5 } });
  const polled = run({ stage: 'poll', data: { status: 'FAILED', startedAt: T0, finishedAt: '2026-11-13T00:00:00.000Z' } }).json;
  check('poll: the decision added to the run', [polled.next, polled.reason, polled.data.status], ['stop', 'run FAILED', 'FAILED']);
  const c = run({ stage: 'cost', run: RUN, events: 18 });
  check('cost: the entry and its file', [c.json.cost_file_name, c.binary.data.fileName, c.binary.data.mimeType],
    ['costo_apify_runInventato01.json', 'costo_apify_runInventato01.json', 'application/json']);
  check('cost: the file holds the entry', JSON.parse(Buffer.from(c.binary.data.data, 'base64').toString('utf8')), m.costEntry(RUN, 18));
  check('an unknown stage is an error', /unknown stage/.test(thrown(() => run({ stage: 'x' })) || ''), true);
}

console.log(failures ? `\n${failures} FAILED of ${checks}` : `\nALL PASS (${checks} checks)`);
process.exit(failures ? 1 : 0);

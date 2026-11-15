#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/canonical-write.js: the canonical write of channel C one call
 * at a time and the same after a retry (workflows/README.md, «The canonical write»), with the
 * T-cases of specification v2.5 it answers (T02, T03, T23, T24, T27, T28, T29), and the n8n adapter
 * evaluated from the exact committed file with a stubbed $input. A small Drive in memory plays the
 * calls through every stage. Every name, id and event is invented (DEC-109).
 *
 * Run:  node tests/test_canonical_write.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const FILE = path.join(__dirname, '..', 'code-nodes', 'canonical-write.js');
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

const W = 'staging_C_write_canonical';
const U = 'staging_C_update_canonical';
const T0 = '2026-11-16T09:00:00.000Z';
const doc = (id, extra) => JSON.stringify(Object.assign({ content_id: `qn:roma:evt:facebook:${id}`, event: { name: 'Evento inventato' } }, extra || {}));
const fb = (id, extra) => ({ name: `roma__evt__facebook__${id}.json`, content: doc(id, extra) });
const md5 = (s) => crypto.createHash('md5').update(Buffer.from(s, 'utf8')).digest('hex');
const req = (files, over) => Object.assign({ workflow: W, execution_id: '501', started_at: T0, files }, over || {});

console.log('request: what a call may write, checked before anything is written');
{
  const r = m.request(req([fb('1001'), fb('1002')]));
  check('the reservation is named for the day, the start and the execution', r.reservation_name, 'prenotazione_2026-11-16_20261116T090000Z_501.json');
  check('the reservation lists the names, never the content', r.reservation, { workflow: W, execution_id: '501', started_at: T0, files: ['roma__evt__facebook__1001.json', 'roma__evt__facebook__1002.json'] });
  check('the reservations read again: today\'s and yesterday\'s, reservations and outcomes', r.reservations_query,
    "(name contains 'prenotazione_2026-11-16_' or name contains 'esito_2026-11-16_' or name contains 'prenotazione_2026-11-15_' or name contains 'esito_2026-11-15_')");
  check('yesterday across the new year', /prenotazione_2025-12-31_/.test(m.request(req([fb('1')], { started_at: '2026-01-01T00:30:00.000Z' })).reservations_query), true);
  check('the write takes only Facebook names', /bad file name/.test(thrown(() => m.request(req([{ name: 'roma__evt__web__abc.json', content: '{}' }]))) || ''), true);
  check('the update takes the other canonical names too', m.request(req([{ name: 'roma__evt__web__abc-series.json', content: '{}' }], { workflow: U })).names, ['roma__evt__web__abc-series.json']);
  check('the write takes 1 to 100 files', [thrown(() => m.request(req([]))), thrown(() => m.request(req(Array.from({ length: 101 }, (_, i) => fb(String(i))))))],
    ['files: 1 to 100 required', 'files: 1 to 100 required']);
  check('the update takes up to 300', [m.request(req(Array.from({ length: 300 }, (_, i) => fb(String(i))), { workflow: U })).names.length,
    thrown(() => m.request(req(Array.from({ length: 301 }, (_, i) => fb(String(i))), { workflow: U })))], [300, 'files: 1 to 300 required']);
  check('a name listed twice stops the call', thrown(() => m.request(req([fb('7'), fb('7')]))), 'file listed twice: roma__evt__facebook__7.json');
  check('content must be the text of the file', /content must be the text/.test(thrown(() => m.request(req([{ name: 'roma__evt__facebook__7.json', content: { a: 1 } }]))) || ''), true);
  check('content that is not JSON stops the call', /is not JSON/.test(thrown(() => m.request(req([{ name: 'roma__evt__facebook__7.json', content: '{' }]))) || ''), true);
  check('a JSON array is not a canonical file', /not a JSON object/.test(thrown(() => m.request(req([{ name: 'roma__evt__facebook__7.json', content: '[]' }]))) || ''), true);
  check('another workflow is not a writer', /not one of the canonical writers/.test(thrown(() => m.request(req([fb('7')], { workflow: 'staging_C_fusion' }))) || ''), true);
  check('30 February is not a start', /UTC instant/.test(thrown(() => m.request(req([fb('7')], { started_at: '2026-02-30T09:00:00.000Z' }))) || ''), true);
  check('an execution id with a space is refused', /execution_id/.test(thrown(() => m.request(req([fb('7')], { execution_id: '5 01' }))) || ''), true);
}

console.log('turn: one call writes at a time (T27, T28)');
{
  const R = (id, at, exe) => ({ id, name: `prenotazione_2026-11-16_20261116T0900${String(at).padStart(2, '0')}Z_${exe}.json`, createdTime: `2026-11-16T09:00:${String(at).padStart(2, '0')}.000Z` });
  const E = (rid) => ({ id: `o${rid}`, name: `esito_2026-11-16_20261116T090000Z_${rid}.json`, createdTime: '2026-11-16T09:01:00.000Z' });
  const a = R('idA', 1, '501');
  const b = R('idB', 2, '502');
  check('T27: of two calls that overlap, the first goes on', m.turn({ reservations: [b, a], mine: 'idA' }), { holds: true, busy: [], stale: [], reason: null });
  check('T27: the second stops, naming the first', m.turn({ reservations: [a, b], mine: 'idB' }), { holds: false, busy: [a.name], stale: [], reason: 'an earlier write has no outcome yet' });
  check('an earlier call with its outcome does not stop the next', m.turn({ reservations: [a, b, E('idA')], mine: 'idB' }).holds, true);
  check('a stopped call writes its outcome too, so it holds nobody', m.turn({ reservations: [a, b, R('idC', 3, '503'), E('idA'), E('idB')], mine: 'idC' }).holds, true);
  const same = [Object.assign({}, a, { createdTime: b.createdTime }), b];
  check('written in the same instant: the Drive id decides, the same for both', [m.turn({ reservations: same, mine: 'idA' }).holds, m.turn({ reservations: same.slice().reverse(), mine: 'idB' }).holds], [true, false]);
  const old = { id: 'idOld', name: 'prenotazione_2026-11-16_20261116T060000Z_499.json', createdTime: '2026-11-16T07:00:01.000Z' };
  const mine = { id: 'idM', name: 'prenotazione_2026-11-16_20261116T090001Z_510.json', createdTime: '2026-11-16T09:00:01.000Z' };
  check('T28: a reservation without outcome holds no more after 120 minutes, and is named stale', m.turn({ reservations: [old, mine], mine: 'idM' }), { holds: true, busy: [], stale: [old.name], reason: null });
  check('T28: one second short of 120 minutes it still holds', m.turn({ reservations: [Object.assign({}, old, { createdTime: '2026-11-16T07:00:02.000Z' }), mine], mine: 'idM' }).holds, false);
  check('a call that does not see its own reservation yet stops, and its outcome frees the next', m.turn({ reservations: [a], mine: 'idB' }),
    { holds: false, busy: [], stale: [], reason: 'the call\'s own reservation is not listed yet' });
  const late = { id: 'idL', name: 'prenotazione_2026-11-16_20261116T090002Z_511.json', createdTime: '2026-11-16T09:00:02.000Z' };
  const lateOld = { id: 'idOld', name: old.name, createdTime: old.createdTime };
  check('T28: a stale call that writes its outcome late does not free the one that went on after it',
    m.turn({ reservations: [lateOld, mine, late, { id: 'oOld', name: 'esito_2026-11-16_20261116T060000Z_idOld.json', createdTime: '2026-11-16T09:00:03.000Z' }], mine: 'idL' }),
    { holds: false, busy: [mine.name], stale: [], reason: 'an earlier write has no outcome yet' });
  check('a reservation without its time is an error', /without the time/.test(thrown(() => m.turn({ reservations: [{ id: 'x', name: a.name }, b], mine: 'idB' })) || ''), true);
  check('other names in the folder are not reservations', m.turn({ reservations: [{ id: 'z', name: 'appunti.txt' }, { name: 'esito_bad.json' }, b], mine: 'idB' }).holds, true);
}

console.log('plan: each file by its exact name (phase 5.2)');
const SCR = { id: 'SCR', name: 'scritture', mimeType: 'application/vnd.google-apps.folder', createdTime: '2026-11-15T15:57:00.578Z' };
{
  const f = fb('2001');
  const g = fb('2002');
  const h = fb('2003');
  const listing = [
    { id: 'F1', name: f.name, createdTime: '2026-11-10T10:00:00.000Z', md5Checksum: md5(f.content) },
    { id: 'G1', name: g.name, createdTime: '2026-11-10T10:00:00.000Z', md5Checksum: md5('{"old":true}') },
    SCR,
  ];
  const p = m.plan({ files: [f, g, h], listing });
  check('T02: the same bytes are left unchanged, nothing is written', [p[0].action, p[0].file_id, p[0].content], ['unchanged', 'F1', null]);
  check('T03: other bytes update the file found by name, never a second file', [p[1].action, p[1].file_id], ['update', 'G1']);
  check('no file of that name: it is created', [p[2].action, p[2].file_id, p[2].content === h.content], ['create', null, true]);
  const dup = [
    { id: 'D2', name: g.name, createdTime: '2026-11-11T10:00:00.000Z', md5Checksum: md5(g.content) },
    { id: 'D1', name: g.name, createdTime: '2026-11-10T10:00:00.000Z', md5Checksum: md5('{"old":true}') },
    { id: 'D3', name: g.name, createdTime: '2026-11-12T10:00:00.000Z' },
  ];
  check('T24: two or more of the same name: the oldest is written, the others are listed, never moved', m.plan({ files: [g], listing: dup.concat(SCR) })[0],
    { name: g.name, action: 'update', file_id: 'D1', duplicates: ['D2', 'D3'], content: g.content });
  check('a listing without the MD5 counts as changed', m.plan({ files: [f], listing: [SCR, { id: 'F1', name: f.name, createdTime: '2026-11-10T10:00:00.000Z' }] })[0].action, 'update');
  check('the MD5 is compared without case', m.plan({ files: [f], listing: [SCR, { id: 'F1', name: f.name, md5Checksum: md5(f.content).toUpperCase() }] })[0].action, 'unchanged');
  check('several of the same name without their times stop the call', /not all with the time/.test(thrown(() => m.plan({ files: [g], listing: [SCR, { id: 'a', name: g.name }, { id: 'b', name: g.name }] })) || ''), true);
  check('a name that only looks like it is not the same file', m.plan({ files: [f], listing: [SCR, { id: 'X', name: f.name.replace('.json', ' (1).json') }] })[0].action, 'create');
  const docOld = { id: 'GDOC', name: g.name, mimeType: 'application/vnd.google-apps.document', createdTime: '2026-11-01T10:00:00.000Z' };
  const jsonNew = { id: 'J1', name: g.name, mimeType: 'application/json', createdTime: '2026-11-05T10:00:00.000Z', md5Checksum: md5('{}') };
  check('an older Google Doc of the same name is never the file written: the JSON is, the Doc is a duplicate',
    m.plan({ files: [g], listing: [SCR, docOld, jsonNew] })[0], { name: g.name, action: 'update', file_id: 'J1', duplicates: ['GDOC'], content: g.content });
  check('only a Google Drive file of that name: the file fails, no second file appears', m.plan({ files: [g], listing: [SCR, docOld, { id: 'SC', name: g.name, mimeType: 'application/vnd.google-apps.shortcut' }] })[0],
    { name: g.name, action: 'failed', file_id: null, duplicates: ['GDOC', 'SC'], content: null, error: 'only a Google Drive file of this name in C Eventi' });
  check('a listing that does not show scritture/ is not the listing of C Eventi: no file becomes a creation',
    [[{}], [{ error: 'Drive 503' }], [{ stage: 'turn', turn: { holds: true } }], [{ id: 'x', name: 'scritture', mimeType: 'application/json' }]]
      .every((l) => /not the listing of C Eventi/.test(thrown(() => m.plan({ files: [g], listing: l })) || '')), true);
  check('a folder of that name counts the same way', m.plan({ files: [g], listing: [SCR, { id: 'FD', name: g.name, mimeType: 'application/vnd.google-apps.folder' }] })[0].action, 'failed');
}

console.log('outcome: what the call did, written next to its reservation and sent back');
{
  const base = { workflow: W, execution_id: '501', started_at: T0, finished_at: '2026-11-16T09:00:30.000Z', reservation_id: 'idA', names: ['a.json', 'b.json', 'c.json'] };
  const stop = m.outcome(Object.assign({}, base, { turn: { holds: false, busy: ['prenotazione_x.json'], stale: [] }, results: [] }));
  check('a stopped call: 409, no files, the reservation that holds it', [stop.status_code, stop.esito.status, stop.esito.files, stop.esito.busy], [409, 'stopped', [], ['prenotazione_x.json']]);
  check('the outcome is named for the reservation it closes', stop.esito_name, 'esito_2026-11-16_20261116T090000Z_idA.json');
  const ok = m.outcome(Object.assign({}, base, { turn: { holds: true, busy: [], stale: [] }, results: [
    { name: 'c.json', action: 'unchanged', file_id: 'C1', duplicates: [] },
    { name: 'a.json', action: 'created', file_id: 'A1', duplicates: [] },
    { name: 'b.json', action: 'updated', file_id: 'B1', duplicates: ['B2'] },
    {}] }));
  check('written: 200, file by file in the order of the call', [ok.status_code, ok.esito.status, ok.esito.files.map((x) => `${x.name}:${x.action}:${x.file_id}`)],
    [200, 'written', ['a.json:created:A1', 'b.json:updated:B1', 'c.json:unchanged:C1']]);
  check('T24: the duplicates are reported with the warning', ok.esito.warnings, ['duplicate_canonical_files_detected']);
  check('the counts', ok.esito.counts, { created: 1, updated: 1, unchanged: 1, failed: 0 });
  const bad = m.outcome(Object.assign({}, base, { turn: { holds: true, busy: [], stale: [] }, results: [
    { name: 'a.json', action: 'created', file_id: '', duplicates: [] },
    { name: 'b.json', action: 'failed', file_id: 'B1', duplicates: [], error: 'Drive 500' }] }));
  check('phase 5.2: a creation whose Drive id was not captured is a failure', bad.esito.files[0], { name: 'a.json', action: 'failed', file_id: null, duplicates: [], error: 'the Drive id of the file was not captured' });
  check('T29: a failed write is recorded, the call is incomplete (500)', [bad.status_code, bad.esito.status, bad.esito.files[1].error], [500, 'incomplete', 'Drive 500']);
  check('a file with no result is a failure too', bad.esito.files[2].error, 'no result from the write');
  const all = (extra) => [{ name: 'a.json', action: 'created', file_id: 'A' }, { name: 'b.json', action: 'unchanged', file_id: 'B' }, { name: 'c.json', action: 'unchanged', file_id: 'C' }].concat(extra || []);
  const odd = m.outcome(Object.assign({}, base, { turn: { holds: true }, results: all([{ name: 'z.json', action: 'created', file_id: 'Z' }]) }));
  check('a result for a file the call did not ask for: still an outcome, incomplete, naming it', [odd.status_code, odd.esito.status, odd.esito.unexpected], [500, 'incomplete', ['z.json']]);
  const twice = m.outcome(Object.assign({}, base, { turn: { holds: true }, results: all([{ name: 'a.json', action: 'created', file_id: 'A2' }]) }));
  check('two results for one file: that file failed, the outcome still written', [twice.status_code, twice.esito.files[0].error], [500, 'two results for this file']);
  check('the text "null" a Set node makes of a missing id is not an id', m.outcome(Object.assign({}, base, { turn: { holds: true }, results: [{ name: 'a.json', action: 'created', file_id: 'null' }] })).esito.files[0].error, 'the Drive id of the file was not captured');
  const before = m.outcome(Object.assign({}, base, { failure: 'Drive 503 on the reading again' }));
  check('a step that fails before the turn: the call stops with the error, 500', [before.status_code, before.esito.status, before.esito.stopped, before.esito.files], [500, 'stopped', 'Drive 503 on the reading again', []]);
  const after = m.outcome(Object.assign({}, base, { failure: 'Drive 503 on the listing', turn: { holds: true, busy: [], stale: [] }, results: [] }));
  check('a step that fails after the turn, before any canonical write: every file failed, 500', [after.status_code, after.esito.status, after.esito.counts.failed, after.esito.files[0].error], [500, 'incomplete', 3, 'Drive 503 on the listing']);
  check('a stop of the turn says why', m.outcome(Object.assign({}, base, { turn: { holds: false, busy: [], stale: [], reason: 'the call\'s own reservation is not listed yet' } })).esito.stopped, 'the call\'s own reservation is not listed yet');
  const late = m.outcome(Object.assign({}, base, { finished_at: '2026-11-16T11:00:00.000Z', turn: { holds: true }, results: [{ name: 'a.json', action: 'created', file_id: 'A' }, { name: 'b.json', action: 'created', file_id: 'B' }, { name: 'c.json', action: 'created', file_id: 'C' }] }));
  check('T28: a call that ran past 120 minutes says so', late.esito.warnings, ['lock_ownership_lost']);
}

console.log('the calls played through a Drive in memory');
{
  // A folder: create gives a new id even for a name that exists, as Drive does.
  let clock = Date.parse('2026-11-16T09:00:00.000Z');
  let seq = 0;
  const drive = { canon: [SCR], scritture: [] };
  const canonical = () => drive.canon.filter((x) => x.name.startsWith('roma__evt__')).length;
  const create = (folder, name, content) => { seq += 1; clock += 1000; const f = { id: `id${seq}`, name, createdTime: new Date(clock).toISOString(), md5Checksum: md5(content), content }; drive[folder].push(f); return f; };
  const update = (id, content) => { const f = drive.canon.find((x) => x.id === id); f.content = content; f.md5Checksum = md5(content); return f; };
  // One call, cut where the workflow has its pause after the reservation.
  const reserve = (files, exe, workflow) => {
    const r = m.request({ workflow: workflow || U, execution_id: exe, started_at: new Date(clock).toISOString(), files });
    return { r, res: create('scritture', r.reservation_name, JSON.stringify(r.reservation)) };
  };
  const finish = ({ r, res }) => {
    const tr = m.turn({ reservations: drive.scritture.map(({ id, name, createdTime }) => ({ id, name, createdTime })), mine: res.id });
    const results = [];
    if (tr.holds) {
      for (const p of m.plan({ files: r.files, listing: drive.canon })) {
        if (p.action === 'create') results.push({ name: p.name, action: 'created', file_id: create('canon', p.name, p.content).id, duplicates: p.duplicates });
        else if (p.action === 'update') results.push({ name: p.name, action: 'updated', file_id: update(p.file_id, p.content).id, duplicates: p.duplicates });
        else results.push({ name: p.name, action: 'unchanged', file_id: p.file_id, duplicates: p.duplicates });
      }
    }
    const o = m.outcome({ workflow: r.reservation.workflow, execution_id: r.reservation.execution_id, started_at: r.reservation.started_at,
      finished_at: new Date(clock).toISOString(), reservation_id: res.id, names: r.names, turn: tr, results });
    create('scritture', o.esito_name, JSON.stringify(o.esito));
    return o;
  };
  const x = fb('3001');
  const y = fb('3002');
  const first = finish(reserve([x, y], '601'));
  check('a first call creates its files', [first.status_code, first.esito.counts], [200, { created: 2, updated: 0, unchanged: 0, failed: 0 }]);
  const again = finish(reserve([x, y], '602'));
  check('T02: the same call retried writes nothing, and no second file appears', [again.esito.counts, canonical()], [{ created: 0, updated: 0, unchanged: 2, failed: 0 }, 2]);
  const p1 = reserve([fb('3003')], '603');
  const p2 = reserve([fb('3003', { event: { name: 'Altro testo' } })], '604', W);
  const o2 = finish(p2);
  const o1 = finish(p1);
  check('T27: two calls at the same time for a new name, a write and an update: one writes, the other stops', [o1.status_code, o2.status_code], [200, 409]);
  check('and Drive holds one file of that name', drive.canon.filter((f) => f.name === 'roma__evt__facebook__3003.json').length, 1);
  const retry = finish(reserve([fb('3003', { event: { name: 'Altro testo' } })], '605', W));
  check('the stopped call retried afterwards updates that file', [retry.status_code, retry.esito.files[0].action, canonical()], [200, 'updated', 3]);
  // T29: Drive refuses one upload; the call is incomplete, its outcome frees the next, and a retry writes only what is missing.
  const realCreate = create;
  let refuse = 'roma__evt__facebook__3005.json';
  const finishFailing = (call) => {
    const tr = m.turn({ reservations: drive.scritture.map(({ id, name, createdTime }) => ({ id, name, createdTime })), mine: call.res.id });
    const results = m.plan({ files: call.r.files, listing: drive.canon }).map((p) => (p.name === refuse
      ? { name: p.name, action: 'failed', file_id: '', duplicates: p.duplicates, error: 'Drive 500' }
      : { name: p.name, action: 'created', file_id: realCreate('canon', p.name, p.content).id, duplicates: p.duplicates }));
    const o = m.outcome({ workflow: U, execution_id: call.r.reservation.execution_id, started_at: call.r.reservation.started_at,
      finished_at: new Date(clock).toISOString(), reservation_id: call.res.id, names: call.r.names, turn: tr, results });
    realCreate('scritture', o.esito_name, JSON.stringify(o.esito));
    return o;
  };
  const broken = finishFailing(reserve([fb('3004'), fb('3005')], '606'));
  check('T29: one upload refused: 500, the other file written', [broken.status_code, broken.esito.counts], [500, { created: 1, updated: 0, unchanged: 0, failed: 1 }]);
  refuse = null;
  const healed = finish(reserve([fb('3004'), fb('3005')], '607'));
  check('T29: the next call goes on, and its retry writes only what is missing', [healed.status_code, healed.esito.files.map((f) => f.action)], [200, ['unchanged', 'created']]);
}

console.log('n8n adapter, from the exact committed file');
{
  const src = fs.readFileSync(FILE, 'utf8');
  const run = (...jsons) => new Function('$input', 'require', 'module', src)({ all: () => jsons.map((json) => ({ json })) }, require, { exports: {} });
  const r = run({ stage: 'request', workflow: W, execution_id: '701', started_at: T0, files: [fb('4001')] });
  check('request: the item keeps its fields and gains the reservation', [r.length, r[0].json.stage, r[0].json.reservation_name, r[0].json.names], [1, 'request', 'prenotazione_2026-11-16_20261116T090000Z_701.json', ['roma__evt__facebook__4001.json']]);
  const t = run({ stage: 'turn', reservation_id: 'idA', reservations: [{ id: 'idA', name: 'prenotazione_2026-11-16_20261116T090000Z_701.json', createdTime: T0 }, {}] });
  check('turn: the decision, without the list read again', [t[0].json.turn, 'reservations' in t[0].json], [{ holds: true, busy: [], stale: [], reason: null }, false]);
  const a = fb('4002');
  const b = fb('4003');
  const p = run({ stage: 'plan', files: [a, b], listing: [SCR, { id: 'B1', name: b.name, createdTime: T0, md5Checksum: md5(b.content) }, {}] });
  check('plan: one item per file, a binary only for a file to write', p.map((it) => [it.json.name, it.json.action, !!it.binary]), [[a.name, 'create', true], [b.name, 'unchanged', false]]);
  const gp = run({ stage: 'plan', files: [a], listing: [SCR, { id: 'GD', name: a.name, mimeType: 'application/vnd.google-apps.document' }] });
  check('plan: a file that cannot be written carries its reason, and no binary', [gp[0].json.action, gp[0].json.error, !!gp[0].binary], ['failed', 'only a Google Drive file of this name in C Eventi', false]);
  check('plan: the binary is the file as sent', [Buffer.from(p[0].binary.data.data, 'base64').toString('utf8'), p[0].binary.data.fileName, p[0].binary.data.mimeType], [a.content, a.name, 'application/json']);
  const o = run({ stage: 'outcome', workflow: W, execution_id: '701', started_at: T0, finished_at: T0, reservation_id: 'idA', names: [a.name], turn: { holds: true }, results: [{ name: a.name, action: 'created', file_id: 'A1', duplicates: [] }] });
  check('outcome: the answer and its file name', [o[0].json.status_code, o[0].json.esito_name], [200, 'esito_2026-11-16_20261116T090000Z_idA.json']);
  check('an unknown stage is an error', /unknown stage/.test(thrown(() => run({ stage: 'x' })) || ''), true);
  check('two items at once are an error', /one item expected/.test(thrown(() => run({ stage: 'request' }, { stage: 'request' })) || ''), true);
}

console.log(failures ? `\n${failures} FAILED of ${checks}` : `\nALL PASS (${checks} checks)`);
process.exit(failures ? 1 : 0);

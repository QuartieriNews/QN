/**
 * canonical-write.js — workstream C: the canonical files of `C Eventi/`, as staging_C_write_canonical
 * and staging_C_update_canonical write them, one call at a time and the same after a retry. It closes
 * two defects of workflows/README.md: a retried call uploaded the same file name again, and two calls
 * at the same time both uploaded a name not yet on Drive.
 *
 * The write of each file is the deterministic upsert of specification v2.5, phase 5.2 (T23, T24),
 * and a file whose bytes are already on Drive is left as it is (T02). One call writes at a time
 * (specification v2.5, Part I, 4.1; T27), with the reservation of the Atti Web download
 * (docs/pilota/CONTRATTI.md, «Lo storico»; `reservationHolds` in archive-record.js), written in
 * `C Eventi/scritture/`, which the two workflows share. A reservation without its outcome stops
 * holding after the specification's `run_lock_max_age_minutes`, counted from the reservation, as
 * there is no heartbeat (T28). A reading, a step of this code or a Drive write that fails after the
 * reservation is recorded in the outcome, which frees the calls after it (T29). A call that dies
 * outright holds them until then: so does a failure in a node with no error route, a reservation
 * Drive saved without n8n hearing of it, or an outcome that cannot be saved. The workflow does the
 * requests: workflows/README.md, «The canonical write».
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for All Items", JavaScript) the same
 * file runs its adapter on one item. `stage` on that item says which step it takes:
 *   - 'request': the files of the call are checked and its reservation is prepared;
 *   - 'turn': the reservations read again after it say whether the call goes on;
 *   - 'plan': the listing of `C Eventi/` gives each file its write, one item per file;
 *   - 'outcome': the results of the writes, or the stop, become the outcome and the answer.
 */
'use strict';

const crypto = require('crypto');

/** What each workflow accepts, as the workflows had it before this file. */
const FLOWS = Object.freeze({
  staging_C_write_canonical: Object.freeze({ max: 100, name: /^roma__evt__facebook__\d+\.json$/ }),
  staging_C_update_canonical: Object.freeze({ max: 300, name: /^roma__evt__[a-z0-9_.-]+\.json$/ }),
});
/** Specification v2.5, Part I, 4.2: `run_lock_max_age_minutes`. */
const HOLD_MS = 120 * 60 * 1000;
/** Specification v2.5, phase 5.2 and T28: the warnings of the run report. */
const DUPLICATES = 'duplicate_canonical_files_detected';
const LOST = 'lock_ownership_lost';
const ID = /^[A-Za-z0-9_-]+$/;
const RESERVATION = /^prenotazione_(\d{4}-\d{2}-\d{2})_(\d{8}T\d{6}Z)_([A-Za-z0-9_-]+)\.json$/;
const OUTCOME = /^esito_(\d{4}-\d{2}-\d{2})_(\d{8}T\d{6}Z)_([A-Za-z0-9_-]+)\.json$/;
const ACTIONS = ['created', 'updated', 'unchanged', 'failed'];
/** Drive's own files (Docs, folders, shortcuts): never the canonical file, whatever their name. */
const GOOGLE = 'application/vnd.google-apps.';
/** The folder of the reservations is a child of `C Eventi/`: a listing that does not show it is not
 *  the listing of the folder, and must never turn every file into a creation. */
const RESERVATIONS_FOLDER = 'scritture';

/** A UTC instant written as n8n and Drive write it, or null: no 30 February, no hour 24. */
function utcInstant(s) {
  const m = typeof s === 'string' && /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d{1,3})?Z$/.exec(s);
  if (!m) return null;
  const t = Date.parse(s);
  if (!Number.isFinite(t)) return null;
  const d = new Date(t);
  const same = [d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate(), d.getUTCHours(), d.getUTCMinutes(), d.getUTCSeconds()]
    .every((v, i) => v === Number(m[i + 1]));
  return same ? t : null;
}

const day = (t) => new Date(t).toISOString().slice(0, 10);
const stamp = (t) => new Date(t).toISOString().slice(0, 19).replace(/[-:]/g, '') + 'Z';
const byTimeThenId = (a, b) => a.at - b.at || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
const md5 = (text) => crypto.createHash('md5').update(Buffer.from(text, 'utf8')).digest('hex');

/** Stage 'request': the files of one call, checked before anything is written, and the reservation
 *  it writes first. The reservation lists names only, never the content of a file. */
function request({ workflow, execution_id, started_at, files }) {
  const rule = FLOWS[workflow];
  if (!rule) throw new Error(`workflow ${JSON.stringify(workflow)} is not one of the canonical writers`);
  if (typeof execution_id !== 'string' || !ID.test(execution_id)) throw new Error('execution_id must be the id of the n8n execution');
  const t = utcInstant(started_at);
  if (t === null) throw new Error('started_at must be a UTC instant');
  if (!Array.isArray(files) || files.length === 0 || files.length > rule.max) throw new Error(`files: 1 to ${rule.max} required`);
  const seen = new Set();
  const clean = files.map((f) => {
    const name = f && f.name;
    if (typeof name !== 'string' || !rule.name.test(name)) throw new Error('bad file name: ' + name);
    if (seen.has(name)) throw new Error('file listed twice: ' + name);
    seen.add(name);
    if (typeof f.content !== 'string') throw new Error(`${name}: content must be the text of the file`);
    let doc;
    try { doc = JSON.parse(f.content); } catch (e) { throw new Error(`${name}: content is not JSON`); }
    if (!doc || typeof doc !== 'object' || Array.isArray(doc)) throw new Error(`${name}: content is not a JSON object`);
    return { name, content: f.content };
  });
  const names = clean.map((f) => f.name);
  const today = day(t);
  const yesterday = day(t - 24 * 3600 * 1000);
  const kinds = [`prenotazione_${today}_`, `esito_${today}_`, `prenotazione_${yesterday}_`, `esito_${yesterday}_`];
  return {
    files: clean,
    names,
    reservation_name: `prenotazione_${today}_${stamp(t)}_${execution_id}.json`,
    reservation: { workflow, execution_id, started_at, files: names },
    // Today's and yesterday's reservations and outcomes cover the HOLD_MS before this call.
    reservations_query: `(${kinds.map((k) => `name contains '${k}'`).join(' or ')})`,
  };
}

/** Stage 'turn': after writing its reservation, a call reads the reservations and outcomes again
 *  (`{ id, name, createdTime }`) and finds its own by the Drive id of the file it wrote (`mine`).
 *  It goes on only if every reservation written before its own, in Drive's order, has its outcome
 *  or is older than HOLD_MS: of two calls that overlap, the second stops before any canonical
 *  write (T27). One without its outcome past HOLD_MS is `stale` and holds no more (T28). A call
 *  that does not see its own reservation yet stops too: it has written nothing canonical, and its
 *  outcome frees the calls after it. */
function turn({ reservations, mine }) {
  if (!Array.isArray(reservations)) throw new Error('reservations must list the reservations and outcomes read again');
  if (typeof mine !== 'string' || !ID.test(mine)) throw new Error('mine must be the Drive id of the call\'s reservation');
  const finished = new Set();
  const rows = new Map();
  for (const r of reservations) {
    const name = r && typeof r.name === 'string' ? r.name : '';
    const out = OUTCOME.exec(name);
    if (out) { finished.add(out[3]); continue; }
    if (!RESERVATION.test(name)) continue;
    const id = String(r.id || '');
    const at = Date.parse(r.createdTime);
    if (!ID.test(id)) throw new Error(`reservation ${name} without its Drive id`);
    if (!Number.isFinite(at)) throw new Error(`reservation ${name} without the time it was written`);
    rows.set(id, { id, name, at });
  }
  const order = [...rows.values()].sort(byTimeThenId);
  const idx = order.findIndex((r) => r.id === mine);
  if (idx < 0) return { holds: false, busy: [], stale: [], reason: 'the call\'s own reservation is not listed yet' };
  const open = order.slice(0, idx).filter((r) => !finished.has(r.id));
  const busy = open.filter((r) => order[idx].at - r.at < HOLD_MS).map((r) => r.name);
  const stale = open.filter((r) => order[idx].at - r.at >= HOLD_MS).map((r) => r.name);
  return { holds: busy.length === 0, busy, stale, reason: busy.length ? 'an earlier write has no outcome yet' : null };
}

/** Stage 'plan': each file of the call against the listing of `C Eventi/` (`{ id, name,
 *  createdTime, md5Checksum }`), by its exact name (phase 5.2). No file of that name: `create`.
 *  Otherwise the oldest by `createdTime` is the one written, the others are `duplicates`, never
 *  moved or deleted (T24); `unchanged` when its MD5 is the file's, so a retried call writes nothing
 *  (T02), `update` otherwise (T03). A listing without the MD5 counts as changed. A Drive file of the
 *  same name (GOOGLE) is never the one written: it is one of the duplicates, and when it is the only
 *  file of that name the file `failed`, so that no second file appears. A listing without
 *  RESERVATIONS_FOLDER stops the call before any canonical write. */
function plan({ files, listing }) {
  if (!Array.isArray(files) || files.length === 0) throw new Error('files must list the files of the call');
  if (!Array.isArray(listing)) throw new Error('listing must list the files of C Eventi');
  if (!listing.some((f) => f && f.name === RESERVATIONS_FOLDER && f.mimeType === GOOGLE + 'folder')) {
    throw new Error(`the listing does not show ${RESERVATIONS_FOLDER}/: it is not the listing of C Eventi`);
  }
  const byName = new Map();
  for (const f of listing) {
    if (!f || typeof f.name !== 'string') continue;
    if (!ID.test(String(f.id || ''))) throw new Error(`${f.name}: a listed file without its Drive id`);
    if (!byName.has(f.name)) byName.set(f.name, []);
    byName.get(f.name).push({ id: String(f.id), at: Date.parse(f.createdTime), md5: f.md5Checksum,
      google: typeof f.mimeType === 'string' && f.mimeType.startsWith(GOOGLE) });
  }
  return files.map(({ name, content }) => {
    const all = (byName.get(name) || []).slice().sort(byTimeThenId);
    const same = all.filter((x) => !x.google);
    const others = all.filter((x) => x.google).map((x) => x.id);
    if (same.length === 0 && others.length > 0) {
      return { name, action: 'failed', file_id: null, duplicates: others, content: null, error: 'only a Google Drive file of this name in C Eventi' };
    }
    if (same.length === 0) return { name, action: 'create', file_id: null, duplicates: [], content };
    if (same.length > 1 && same.some((x) => !Number.isFinite(x.at))) {
      throw new Error(`${name}: ${same.length} files of this name, not all with the time they were written`);
    }
    const [oldest, ...rest] = same;
    const duplicates = rest.map((x) => x.id).concat(others);
    if (typeof oldest.md5 === 'string' && oldest.md5.toLowerCase() === md5(content)) {
      return { name, action: 'unchanged', file_id: oldest.id, duplicates, content: null };
    }
    return { name, action: 'update', file_id: oldest.id, duplicates, content };
  });
}

/** Stage 'outcome': what a call did, file by file in the order of the call, written in
 *  `C Eventi/scritture/` next to its reservation and sent back as the answer. A call stopped by its
 *  turn has no files (409). `failure` is the error of a step that failed after the reservation:
 *  before the turn the call stops, after it every file is a failure, since the steps that can fail
 *  there come before any canonical write (500). A created or updated file without its Drive id is a
 *  failure (phase 5.2, step 3), and a failure leaves the call `incomplete` (500): a retry writes
 *  only what is missing. Once the reservation is known nothing here throws on the results, so that
 *  the outcome is always written. */
function outcome({ workflow, execution_id, started_at, finished_at, reservation_id, names, turn: tr, results, failure }) {
  const t0 = utcInstant(started_at);
  const t1 = utcInstant(finished_at);
  if (t0 === null || t1 === null) throw new Error('started_at and finished_at must be UTC instants');
  if (typeof reservation_id !== 'string' || !ID.test(reservation_id)) throw new Error('reservation_id must be the Drive id of the call\'s reservation');
  if (!Array.isArray(names) || names.length === 0) throw new Error('names must list the files of the call');
  const failed = typeof failure === 'string' && failure.trim() ? failure.trim() : null;
  if (!failed && (!tr || typeof tr.holds !== 'boolean')) throw new Error('turn must say whether the call held its turn');
  const esito_name = `esito_${day(t0)}_${stamp(t0)}_${reservation_id}.json`;
  const head = { workflow, execution_id, started_at, finished_at, reservation_id, busy: (tr && tr.busy) || [], stale: (tr && tr.stale) || [] };
  const counts = (files) => Object.fromEntries(ACTIONS.map((a) => [a, files.filter((f) => f.action === a).length]));
  const stop = (why, code) => ({ esito_name, status_code: code,
    esito: Object.assign(head, { status: 'stopped', stopped: why, files: [], counts: counts([]), warnings: [] }) });
  if (failed && !(tr && tr.holds === true)) return stop(failed, 500);
  if (!failed && !tr.holds) return stop(tr.reason || 'an earlier write has no outcome yet', 409);
  const byName = new Map();
  const twice = new Set();
  const unexpected = [];
  for (const r of failed || !Array.isArray(results) ? [] : results) {
    if (!r || typeof r.name !== 'string') continue; // the empty item of a branch that wrote nothing
    if (!names.includes(r.name)) unexpected.push(r.name);
    else if (byName.has(r.name)) twice.add(r.name);
    else byName.set(r.name, r);
  }
  const files = names.map((name) => {
    const r = byName.get(name);
    const duplicates = r && Array.isArray(r.duplicates) ? r.duplicates.map(String) : [];
    if (failed) return { name, action: 'failed', file_id: null, duplicates, error: failed };
    if (twice.has(name)) return { name, action: 'failed', file_id: null, duplicates, error: 'two results for this file' };
    if (!r) return { name, action: 'failed', file_id: null, duplicates, error: 'no result from the write' };
    if (!ACTIONS.includes(r.action)) return { name, action: 'failed', file_id: null, duplicates, error: `unknown action ${r.action}` };
    // A Set node turns a missing id into the text "null" or "undefined": neither is an id.
    const file_id = typeof r.file_id === 'string' && ID.test(r.file_id) && !['null', 'undefined'].includes(r.file_id) ? r.file_id : null;
    if (r.action === 'failed') return { name, action: 'failed', file_id, duplicates, error: String(r.error || 'the write failed') };
    if (!file_id) return { name, action: 'failed', file_id: null, duplicates, error: 'the Drive id of the file was not captured' };
    return { name, action: r.action, file_id, duplicates };
  });
  const n = counts(files);
  const warnings = [];
  if (files.some((f) => f.duplicates.length > 0)) warnings.push(DUPLICATES);
  if (t1 - t0 >= HOLD_MS) warnings.push(LOST);
  const bad = n.failed > 0 || unexpected.length > 0;
  const esito = Object.assign(head, { status: bad ? 'incomplete' : 'written', stopped: null, files, counts: n, warnings });
  if (unexpected.length) esito.unexpected = unexpected;
  return { esito_name, status_code: bad ? 500 : 200, esito };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { FLOWS, HOLD_MS, DUPLICATES, LOST, utcInstant, md5, request, turn, plan, outcome };
  return;
}

/* n8n Code node, "Run Once for All Items" — one item in, its stage out (see the header). */
const items = $input.all();
if (items.length !== 1) throw new Error(`one item expected, ${items.length} received`);
const j = items[0].json;
if (j.stage === 'request') return [{ json: Object.assign({}, j, request(j)) }];
if (j.stage === 'turn') {
  const out = Object.assign({}, j, { turn: turn({ reservations: (j.reservations || []).filter((r) => r && r.name), mine: j.reservation_id }) });
  delete out.reservations;
  return [{ json: out }];
}
if (j.stage === 'plan') {
  return plan(j).map((p) => {
    const json = { name: p.name, action: p.action, file_id: p.file_id, duplicates: p.duplicates };
    if (p.error) json.error = p.error;
    if (p.content === null) return { json };
    return { json, binary: { data: { data: Buffer.from(p.content, 'utf8').toString('base64'), mimeType: 'application/json', fileName: p.name } } };
  });
}
if (j.stage === 'outcome') return [{ json: outcome(j) }];
throw new Error(`unknown stage ${JSON.stringify(j.stage)}`);

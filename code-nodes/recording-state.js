/**
 * recording-state.js — workstream A: the state of the collection in the Data table
 * `staging_A_registrazioni` — its columns, the row of a recording and how its state may change,
 * the lease that keeps one run on a row and one request at a time on a source, what a listing
 * changes in a row already there, the record of registrazioni/, the register of a run and the
 * alert. The rules are in docs/pilota/CONTRATTI.md, section 7 («A · Amministrazione», rows
 * Registrazione, Raccolta and Testo) and docs/pilota/WORKSTREAM_A.md, section 4 («Lo stato», «La
 * presa», «La pulizia»); this file does not restate them. A row never holds a text.
 * Acceptance: tests/test_recording_state.js (T-A2-05, T-A2-11, and the rows, the record, the
 * register and the alert of T-A2-01, T-A2-06 and T-A2-09).
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item") the same file runs
 * its adapter. A Code node reads and writes no Data table: the Data table nodes do, with the
 * fields this file computes. `stage` on the item says which step it takes:
 *   - 'claim': whether this run takes a lease, waits for it or leaves the source, and the
 *     condition its write carries;
 *   - 'holds': whether the lease read back is this run's;
 *   - 'release': the fields and the condition that leave this run's lease;
 *   - 'listing': a recording of the list against its row (the row to write, or nothing), and its
 *     record of registrazioni/;
 *   - 'restart': the restart by hand of a row in `errore`;
 *   - 'log': the register of the run and, when a list was read incomplete, the alert. The alert of
 *     a host or a list stopped is written when it stops (source-guard.js, youtube-list.js).
 */
'use strict';

/** The columns of the Data table, one row per recording and one per source, host or lease (the
 *  `ref` forms below); n8n types. */
const COLUMNS = Object.freeze([
  ['ref', 'string'], ['tipo', 'string'], ['stato', 'string'], ['stato_prima_errore', 'string'], ['motivo', 'string'],
  ['piattaforma', 'string'], ['source_channel', 'string'], ['source_id', 'string'], ['catalogo', 'string'], ['canale', 'string'],
  ['organo', 'string'], ['municipality_code', 'string'], ['titolo', 'string'], ['url', 'string'],
  ['ora_riferimento_utc', 'string'], ['ora_pubblicazione_utc', 'string'], ['durata_secondi', 'number'],
  ['trascrizione_piattaforma', 'boolean'], ['numero_parte', 'number'], ['prima_parte', 'string'], ['parte_precedente', 'string'],
  ['audio_url', 'string'], ['parlato_url', 'string'], ['vtt_url', 'string'], ['transcript_source', 'string'],
  ['segmento_ripresa', 'number'], ['tentativi', 'number'], ['presa_id', 'string'], ['presa_fino_ms', 'number'],
  ['apify_run_id', 'string'], ['apify_storage_id', 'string'],
  ['fermo', 'string'], ['fermo_fino', 'string'], ['errori_di_fila', 'number'], ['robots_giorno', 'string'],
  ['giorno', 'string'], ['conteggio_giorno', 'number'], ['ultimo_ok_giorno', 'string'], ['aggiornata_utc', 'string'],
].map(([name, type]) => Object.freeze({ name, type })));
const COLUMN_NAMES = COLUMNS.map((c) => c.name);

/** The rows that are not recordings: a lease per source, a host, a source's own counters. */
const LEASE_ROWS = Object.freeze(['lease:romatv', 'lease:youtube']);
const hostRef = (host) => `host:${host}`;
const sourceRef = (name) => `fonte:${name}`;
const RECORDING_REF = /^(romatv:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|youtube:[A-Za-z0-9_-]{11})$/;

/** WORKSTREAM_A, section 4, «Lo stato»: the states and the moves between them. A state that
 *  moves to itself records progress; `nuova` reaches `confini_fissati` when the text of the open
 *  sitting is already in originali/ (section 4, «La ripresa del confine»), as after a restart by
 *  hand; `errore` leaves only by restart below. */
const STATES = Object.freeze(['nuova', 'testo_in_corso', 'testo_completo', 'confini_fissati', 'letta', 'scartata', 'errore']);
const MOVES = Object.freeze({
  nuova: ['nuova', 'testo_in_corso', 'testo_completo', 'confini_fissati', 'scartata', 'errore'],
  testo_in_corso: ['testo_in_corso', 'testo_completo', 'confini_fissati', 'scartata', 'errore'],
  testo_completo: ['confini_fissati', 'scartata', 'errore'],
  confini_fissati: ['letta', 'errore'],
  letta: ['errore'],
  scartata: [],
  errore: [],
});
const ATTEMPTS_TO_ERROR = 3;
const LEASE_MS = 5 * 60 * 1000;

function canMove(from, to) {
  return Object.prototype.hasOwnProperty.call(MOVES, from) && MOVES[from].includes(to);
}

/** A row moved to `to`, or an error for a move the table does not have. */
function move(row, to, now, motivo) {
  if (!canMove(row.stato, to)) throw new Error(`move_invalid: ${row.stato} -> ${to}`);
  const r = Object.assign({}, row, { stato: to, aggiornata_utc: now });
  if (to === 'errore') r.stato_prima_errore = row.stato;
  if (to === 'errore' || to === 'scartata') r.motivo = motivo || row.motivo || '';
  if (to !== 'errore') r.tentativi = 0;
  return r;
}

/** A failed attempt on a row: the third in a row sends it to `errore`, keeping where it fell. */
function failAttempt(row, now, motivo) {
  const tentativi = (Number(row.tentativi) || 0) + 1;
  if (tentativi >= ATTEMPTS_TO_ERROR) return Object.assign(move(row, 'errore', now, motivo), { tentativi });
  return Object.assign({}, row, { tentativi, motivo: motivo || '', aggiornata_utc: now });
}

/** The restart by hand of a row in `errore` (WORKSTREAM_A, section 4, «Lo stato» and «La
 *  pulizia»). Back to `nuova` the row also forgets its text and its Apify run, whose storage the
 *  daily cleaning may already have deleted. */
function restart(row, now) {
  if (row.stato !== 'errore') throw new Error('restart_only_from_errore');
  const from = row.stato_prima_errore;
  const back = from === 'confini_fissati' || from === 'letta' ? from : 'nuova';
  const r = Object.assign({}, row, { stato: back, stato_prima_errore: '', motivo: '', tentativi: 0, aggiornata_utc: now });
  if (back === 'nuova') Object.assign(r, { segmento_ripresa: 0, transcript_source: '', apify_run_id: '', apify_storage_id: '' });
  return r;
}

/** WORKSTREAM_A, section 4, «La presa». A lease is free when its end has passed (a lease never
 *  taken, or left, has 0): the same test as the condition of the write. */
const leaseFree = (row, nowMs) => Number(row.presa_fino_ms) <= nowMs;
const execOf = (execId) => {
  if ((typeof execId !== 'string' && typeof execId !== 'number') || String(execId).trim() === '' || String(execId) === 'undefined') {
    throw new Error('execution_id_missing');
  }
  return String(execId);
};
/** The fields a run writes to take, or renew, a lease it may take. */
const leaseFields = (execId, nowMs) => ({ presa_id: execOf(execId), presa_fino_ms: nowMs + LEASE_MS });
/** Whether the lease read back after writing it is this run's: only then does the run work. */
const holds = (row, execId, nowMs) => !!row && row.presa_id === execOf(execId) && Number(row.presa_fino_ms) > nowMs;
/** The condition of a write on a lease: every condition must hold (the Data table node's «Must
 *  Match: All Conditions»; its default is «Any»). */
const allOf = (...conditions) => ({ match: 'allConditions', conditions });
const byRef = (ref) => ({ keyName: 'ref', condition: 'eq', keyValue: ref });
const byExec = (execId) => ({ keyName: 'presa_id', condition: 'eq', keyValue: execOf(execId) });

/** A row a lease can be taken on: a source's lease row or a recording's row, with its end as a
 *  number. Anything else is an error, never a free lease. */
function leaseRow(row) {
  const ref = row && row.ref;
  if (!LEASE_ROWS.includes(ref) && !RECORDING_REF.test(ref || '')) throw new Error('lease_row_missing');
  if (row.presa_fino_ms === '' || row.presa_fino_ms === null || !Number.isFinite(Number(row.presa_fino_ms))) throw new Error('lease_row_invalid');
  return row;
}

/** The fields and the condition that leave a lease: only the run that holds it leaves it, in the
 *  write itself. */
function release(row, execId) {
  leaseRow(row);
  return { fields: { presa_id: '', presa_fino_ms: 0 }, where: allOf(byRef(row.ref), byExec(execId)) };
}

/** T-A2-11: what a run does with a lease row (WORKSTREAM_A, section 4, «La presa»). `where` is
 *  the condition the Data table update carries, so that the write itself happens only on a lease
 *  free or run out (a free row has `presa_fino_ms` 0), or, to renew it, on this run's own lease;
 *  the run then reads the row back (`holds`). The list (`waiting` false) waits for a lease held by
 *  another run, at most until it runs out, then (`waiting` true) leaves the source for this run;
 *  the text does not start. The lease rows exist from the creation of the table (LEASE_SEED). */
function claim(row, execId, nowMs, who, waiting) {
  leaseRow(row);
  if (holds(row, execId, nowMs)) {
    return { action: 'take', fields: leaseFields(execId, nowMs), where: allOf(byRef(row.ref), byExec(execId)), wait_ms: 0 };
  }
  if (leaseFree(row, nowMs)) {
    return { action: 'take', fields: leaseFields(execId, nowMs),
      where: allOf(byRef(row.ref), { keyName: 'presa_fino_ms', condition: 'lte', keyValue: nowMs }), wait_ms: 0 };
  }
  if (who === 'list' && !waiting) return { action: 'wait', fields: null, where: null, wait_ms: Math.min(LEASE_MS, Number(row.presa_fino_ms) - nowMs) };
  return { action: who === 'list' ? 'skip' : 'no_start', fields: null, where: null, wait_ms: 0 };
}
/* (the lease rows of the sources are written with the table: LEASE_SEED; a recording's row has its
 * lease columns from newRow.) */

/** The lease rows written once, when the table is created. */
const LEASE_SEED = Object.freeze(LEASE_ROWS.map((ref) => Object.freeze({ ref, tipo: 'presa', presa_id: '', presa_fino_ms: 0 })));

/** The record file of a recording (CONTRATTI section 7 (A), row Registrazione), as
 *  institutional-identity.js, recordingFileName. */
function recordFileName(ref) {
  if (!RECORDING_REF.test(ref)) throw new Error('ref_invalid');
  return ref.replace(':', '__') + '.json';
}

const SOURCE = { romatv: { source_channel: 'inst_romatv', source_id: 'streaming.comune.roma.it' } };

/** The row of a recording seen for the first time, from what the list read (romatv-list.js,
 *  readEntry; youtube-list.js, readVideo) and the link of its part, if any. */
function newRow(rec, link, now) {
  if (!RECORDING_REF.test(rec.recording_ref)) throw new Error('ref_invalid');
  const src = rec.piattaforma === 'youtube' ? { source_channel: 'inst_youtube', source_id: rec.source_id } : SOURCE.romatv;
  const l = link || {};
  return {
    ref: rec.recording_ref, tipo: 'registrazione', stato: 'nuova', stato_prima_errore: '', motivo: '',
    piattaforma: rec.piattaforma, source_channel: src.source_channel, source_id: src.source_id,
    catalogo: rec.catalogo || '', canale: rec.canale || '', organo: rec.organo || '', municipality_code: rec.municipality_code || '',
    titolo: rec.titolo || '', url: rec.url || '', ora_riferimento_utc: rec.ora_riferimento_utc,
    ora_pubblicazione_utc: rec.ora_pubblicazione_utc || '', durata_secondi: rec.durata_secondi,
    trascrizione_piattaforma: rec.trascrizione_piattaforma === true, numero_parte: rec.numero_parte || 0,
    prima_parte: l.prima_parte || '', parte_precedente: l.parte_precedente || '',
    audio_url: rec.audio_url || '', parlato_url: rec.parlato_url || '', vtt_url: rec.vtt_url || '', transcript_source: '',
    segmento_ripresa: 0, tentativi: 0, presa_id: '', presa_fino_ms: 0, apify_run_id: '', apify_storage_id: '',
    aggiornata_utc: now,
  };
}

/** T-A2-05 (WORKSTREAM_A, section 4, «La ripresa del testo»): where the text of a recording
 *  comes from. 'none' for a row that makes no text. */
function textPlan(row) {
  if (['testo_completo', 'confini_fissati', 'letta'].includes(row.stato)) return 'keep';
  if (!['nuova', 'testo_in_corso'].includes(row.stato)) return 'none';
  if (row.trascrizione_piattaforma === true) return row.stato === 'testo_in_corso' ? 'switch_to_platform' : 'platform';
  return 'ours';
}

/** A recording of the list against its row: what changes (null for nothing), and whether its
 *  record must be written again (CONTRATTI section 7 (A), row Registrazione). A platform
 *  transcript, or one of its two addresses, that appears is recorded at any state (T-A2-05). A
 *  link of a part is written while the row is `nuova`, and a run that does not see the part
 *  before never takes a link away (T-A2-06). Nothing else a later listing says changes a row. */
function listingUpdate(row, rec, link, now) {
  const update = {};
  if (rec.trascrizione_piattaforma === true && row.trascrizione_piattaforma !== true) update.trascrizione_piattaforma = true;
  for (const k of ['parlato_url', 'vtt_url']) if (rec[k] && !row[k]) update[k] = rec[k];
  const l = link || {};
  if (row.stato === 'nuova' && l.prima_parte && (l.prima_parte !== row.prima_parte || l.parte_precedente !== row.parte_precedente)) {
    Object.assign(update, { prima_parte: l.prima_parte, parte_precedente: l.parte_precedente });
  }
  if (!Object.keys(update).length) return { update: null, record: false };
  update.aggiornata_utc = now;
  return { update, record: true };
}

/** CONTRATTI section 7 (A), row Registrazione: the record of registrazioni/, from the row. */
function record(row) {
  const r = { schema_version: 'pilot-recording-0.1', recording_ref: row.ref, source_channel: row.source_channel, source_id: row.source_id };
  if (row.piattaforma === 'youtube') r.canale = row.canale || null; else r.catalogo = row.catalogo;
  Object.assign(r, { organo: row.organo, municipality_code: row.municipality_code || null, titolo: row.titolo,
    ora_riferimento_utc: row.ora_riferimento_utc, ora_pubblicazione_utc: row.ora_pubblicazione_utc || null,
    durata_secondi: row.durata_secondi, trascrizione_piattaforma: row.trascrizione_piattaforma === true });
  if (row.url) r.url = row.url;
  if (row.numero_parte) {
    r.parte = { numero: row.numero_parte, prima_parte: row.prima_parte || null, parte_precedente: row.parte_precedente || null };
  }
  r.stato = row.stato;
  return r;
}

const stamp = (iso) => new Date(iso).toISOString().slice(0, 19).replace(/[-:]/g, '') + 'Z';

/** The register of a run in letture/ (CONTRATTI section 7 (A), row Raccolta): refs, counts and
 *  reasons, never a title or a text. */
function runLog(run) {
  const keep = (x) => ({ fonte: x.fonte || 'romatv', catalogo: x.catalogo || null, pages: x.page === undefined ? null : x.page,
    complete: x.complete, reason: x.reason, host_stopped: x.host_stopped === true, in_window: x.records.length, skipped: x.skipped });
  return {
    workflow: run.workflow, execution_id: run.execution_id || null, started_at: run.started_at, finished_at: run.finished_at,
    user_agent: run.user_agent, portal_headers: run.portal_headers === true,
    robots: run.robots || [], hosts: run.hosts || [], readings: (run.readings || []).map(keep),
    new_rows: run.new_rows || [], updated_rows: run.updated_rows || [], deferred_rows: run.deferred || [], unbound_parts: run.unbound || [],
    without_url: run.without_url || [], skipped_sources: run.skipped_sources || [], stopped_now: run.stopped_now || [],
  };
}

/** The alert of a run that read a list incomplete; null when there is none. A source left for a
 *  lease, and a list not read because its host is already stopped (its stop had its own alert),
 *  are in the register only (WORKSTREAM_A, section 4, «La presa»). */
function runAlert(log) {
  const incomplete = log.readings.filter((x) => x.complete === false && !x.host_stopped)
    .map((x) => ({ fonte: x.fonte, catalogo: x.catalogo, reason: x.reason }));
  if (!incomplete.length) return null;
  return {
    name: `AVVISO_A_${stamp(log.finished_at)}_elenchi.json`,
    body: { avviso: 'la raccolta del canale A ha letto un elenco incompleto: avvisare l\'owner (CONTRATTI, sezione 7 A, «Raccolta»)',
      workflow: log.workflow, esecuzione: log.execution_id, alle: log.finished_at, incompleti: incomplete },
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { COLUMNS, COLUMN_NAMES, LEASE_ROWS, LEASE_SEED, hostRef, sourceRef, STATES, MOVES, ATTEMPTS_TO_ERROR, LEASE_MS, canMove, move,
    failAttempt, restart, leaseFree, leaseFields, holds, release, claim, recordFileName, newRow, textPlan, listingUpdate, record,
    runLog, runAlert };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. 'claim' reads `lease_row`, `execution_id`,
 * `who` and `waiting` and writes `lease` ({ action, fields, where, wait_ms }); 'holds' reads
 * `lease_row` and `execution_id`; 'release' reads the same and writes `release` ({ fields, where });
 * every `where` is { match, conditions } for the Data table update; 'listing' reads `rec`, `link` and `row` (the row read for the
 * same ref, if any) and writes `action` ('upsert' or 'none'), `where`, `fields`, `record_file_name`
 * and `record`: an upsert on `ref`, so that the same recording twice in a run gives one row;
 * 'restart' reads `row` and writes `fields`, `where`, `record_file_name` and `record`, as 'listing'
 * does: a state that changes changes the record; 'log' reads `run` and writes `log`,
 * `log_file_name` and `alert`. */
const nowMs = Date.now();
const nowIso = new Date(nowMs).toISOString();
if ($json.stage === 'claim') {
  Object.assign($json, { lease: claim($json.lease_row, $json.execution_id, nowMs, $json.who, $json.waiting === true) });
  return $input.item;
}
if ($json.stage === 'holds') {
  $json.lease_ours = holds($json.lease_row, $json.execution_id, nowMs);
  return $input.item;
}
if ($json.stage === 'release') {
  $json.release = release($json.lease_row, $json.execution_id);
  return $input.item;
}
if ($json.stage === 'listing') {
  const ref = $json.rec.recording_ref;
  const row = $json.row && $json.row.ref ? $json.row : null;
  if (row && row.ref !== ref) throw new Error(`listing_row_of_another_ref: ${row.ref} for ${ref}`);
  let fields = null;
  if (!row) {
    fields = newRow($json.rec, $json.link, nowIso);
  } else {
    const u = listingUpdate(row, $json.rec, $json.link, nowIso);
    if (u.update) fields = Object.assign({ ref }, u.update);
  }
  const full = fields ? Object.assign({}, row || {}, fields) : null;
  Object.assign($json, { action: fields ? 'upsert' : 'none', where: fields ? allOf(byRef(ref)) : null,
    fields, record_file_name: recordFileName(ref), record: full ? JSON.stringify(record(full), null, 2) + '\n' : null });
  return $input.item;
}
if ($json.stage === 'restart') {
  const fields = restart($json.row, nowIso);
  Object.assign($json, { fields, where: allOf(byRef(fields.ref)), record_file_name: recordFileName(fields.ref),
    record: JSON.stringify(record(fields), null, 2) + '\n' });
  return $input.item;
}
if ($json.stage === 'log') {
  const log = runLog(Object.assign({}, $json.run, { finished_at: nowIso }));
  Object.assign($json, { log, log_file_name: `elenco_${stamp(log.started_at)}.json`, alert: runAlert(log) });
  return $input.item;
}
throw new Error(`recording-state.js: unknown stage ${JSON.stringify($json.stage)}`);

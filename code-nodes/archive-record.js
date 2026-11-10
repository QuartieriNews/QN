/**
 * archive-record.js — workstream D, the Atti Web reading of DEC-033: one row of the
 * portal's search becomes one record of the private history archive (DEC-023, rule 2).
 * It fixes what docs/pilota/CONTRATTI.md («Lo storico») leaves to the PR that opens D:
 * the form of `archive_id` and the values of `tipo`; tests/test_archive_record.js holds
 * the idempotency and normalization cases.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): this exact file is both the Node
 * module the tests require() and the full text of the n8n Code node ("Run Once for Each
 * Item"). The staging workflow uses it twice, byte-identical:
 *   - on a search row (with `tipologia` and `reading_day` set by the workflow) it adds
 *     `archive`: the identity, the perimeter verdict and the PDF link;
 *   - on the same item after the download (`download` and `existing` set) it adds the
 *     `record` to append, or `record: null` when the archive already holds that original.
 * Pacing and the daily cap (DEC-033, rule 2) belong to the workflow, not to this node.
 */

'use strict';

/** A site's `source_id` is its host, lowercase, without `www.` (CONTRATTI.md, section 2). */
const SOURCE_ID = 'comune.roma.it';
const PREFIX = 'qn:roma:arc:';
const PDF_URL = 'https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/showPdfDoc?fun=deliberazioniAtti';

/** The values of `tipo`: every tipologia of the portal's menu on 15 September 2026
 *  (docs/sources/A2_ATTIWEB_TIPOLOGIE.md, section 3), all read (CONTRATTI.md, «Lo storico»). */
const TIPI = Object.freeze(['CMC', 'CPC', 'MMC', 'KD', 'KCD', 'WCD', 'WD', 'MD', 'MCD', 'OCD',
  'OD', 'PD', 'KID', 'CD', 'CMD', 'CID', 'ACD', 'KMD', 'WMD', 'GCD', 'GD', 'GMD', 'DDS', 'DMS',
  'PMT', 'GMT', 'PS', 'GCM', 'GMM', 'CZ', 'CMZ', 'AZ', 'XO', 'TO', 'PMO', 'SO', 'XMO', 'AY', 'CY',
  'CMY', 'CPL', 'CMR', 'DDK', 'DMK', 'CMV', 'GMV', 'CPV', 'MMV']);

/** DEC-033, rule 1: the pilot Municipi and the first day of the period. */
const MUNICIPI = Object.freeze(['X', 'V', 'I']);
const PERIOD_START = '2026-01-01';

const ROMANI = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
  'XIII', 'XIV', 'XV'];

/** CONTRATTI.md, «Lo storico»: Unicode NFC, trimmed, inner whitespace collapsed to one
 *  space. A whole non-negative number (a JSON key) is read as its decimal string. */
function normalizeKey(v) {
  if (typeof v === 'number' && Number.isSafeInteger(v) && v >= 0) v = String(v);
  if (typeof v !== 'string') return '';
  return v.normalize('NFC').trim().replace(/\s+/g, ' ');
}

/** `qn:roma:arc:<source_id>:<tipologia>:<idDoc>` — the pair the portal itself uses to
 *  address the document (`par1`, `par2` of the PDF link). The prefix is a constant; no
 *  geography and no `registro_id` take part. Anything else stops the run: an id is
 *  permanent, so a key in an unexpected shape is never turned into one. */
function archiveId(tipologia, idDoc) {
  const tipo = normalizeKey(tipologia);
  const key = normalizeKey(idDoc);
  if (!TIPI.includes(tipo)) throw new Error(`tipologia ${JSON.stringify(tipologia)} is not a value of tipo`);
  if (!/^[0-9]+$/.test(key)) throw new Error(`idDoc ${JSON.stringify(idDoc)} is not the numeric key the portal gives`);
  return `${PREFIX}${SOURCE_ID}:${tipo}:${key}`;
}

/** CONTRATTI.md «Lo storico», reading Atti Web: the tipologie the portal lists at the
 *  start of a reading, in a fixed order. A list that did not read stops the reading before
 *  it starts; a code that is not a value of `tipo` stops it too, until a PR adds it here. */
function planTipologie(menu) {
  if (!Array.isArray(menu) || menu.length === 0) throw new Error('the list of tipologie did not read: the reading does not start');
  const codes = [...new Set(menu.map(normalizeKey))];
  const unknown = codes.filter((c) => !TIPI.includes(c));
  if (unknown.length) throw new Error(`tipologie not in tipo: ${unknown.join(', ')}`);
  return codes.sort((a, b) => TIPI.indexOf(a) - TIPI.indexOf(b));
}

/** CONTRATTI.md «Lo storico» (DEC-033 rule 5), late publication: the passes over one
 *  tipologia (each `{ total, rows }`) count when the last two give the same total and the
 *  same set of idDoc; at most three passes. The rows are merged by idDoc within the
 *  tipologia either way, and `complete` says what the registry records. */
function mergePasses(passes) {
  if (!Array.isArray(passes) || passes.length === 0 || passes.length > 3) {
    throw new Error('one to three passes over a tipologia (CONTRATTI.md, «Lo storico»)');
  }
  const ids = (p) => new Set((p.rows || []).map((r) => normalizeKey(r.idDoc)));
  const byId = new Map();
  for (const p of passes) for (const r of p.rows || []) byId.set(normalizeKey(r.idDoc), r);
  const [a, b] = passes.slice(-2);
  const stable = passes.length >= 2 && a.total === b.total &&
    ids(a).size === ids(b).size && [...ids(a)].every((x) => ids(b).has(x));
  return { complete: stable, needs_another_pass: !stable && passes.length < 3, rows: [...byId.values()] };
}

/** `roma__arc__comune.roma.it__CMD__123`: the stem of the record and original file names. */
function fileStem(id) {
  if (typeof id !== 'string' || !id.startsWith(PREFIX)) throw new Error(`not an archive_id: ${JSON.stringify(id)}`);
  return id.slice('qn:'.length).split(':').join('__');
}

function pdfUrl(tipologia, idDoc) {
  const b64 = (s) => Buffer.from(s, 'utf8').toString('base64');
  return `${PDF_URL}&par1=${b64(normalizeKey(tipologia))}&par2=${b64(normalizeKey(idDoc))}`;
}

function validDay(y, m, d) {
  const t = new Date(Date.UTC(y, m - 1, d));
  return t.getUTCFullYear() === y && t.getUTCMonth() === m - 1 && t.getUTCDate() === d;
}

const ROME_DAY = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit',
});

function romeDayOf(ms) {
  const p = Object.fromEntries(ROME_DAY.formatToParts(new Date(ms)).map((x) => [x.type, x.value]));
  return `${p.year}-${p.month}-${p.day}`;
}

const pad = (n) => String(n).padStart(2, '0');

/** A date field of the portal as a Rome day (YYYY-MM-DD), or null when empty. A day
 *  written as such is kept as written; an instant (with Z or an offset, or epoch
 *  milliseconds) is converted to Europe/Rome first, as everywhere else in the pilot
 *  (Spec v2.5 T17). Any other shape stops the run, naming the field. */
function sourceDay(v, field) {
  if (v === null || v === undefined || v === '') return null;
  const bad = () => new Error(`${field}: unreadable date ${JSON.stringify(v)}`);
  if (typeof v === 'number') {
    if (!Number.isSafeInteger(v) || v < 1e11) throw bad();
    return romeDayOf(v);
  }
  if (typeof v !== 'string') throw bad();
  const s = v.trim();
  if (s === '') return null;
  let m = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(Z|[+-]\d{2}:?\d{2})?)?$/.exec(s);
  if (m) {
    const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
    if (!validDay(y, mo, d)) throw bad();
    if (m[4] !== undefined && (Number(m[4]) > 23 || Number(m[5]) > 59 || Number(m[6] || 0) > 59)) throw bad();
    if (!m[7]) return `${m[1]}-${m[2]}-${m[3]}`;
    const offset = m[7] === 'Z' ? 'Z' : `${m[7].slice(0, 3)}:${m[7].slice(-2)}`;
    const ms = Date.parse(`${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:${m[6] || '00'}${offset}`);
    if (Number.isNaN(ms)) throw bad();
    return romeDayOf(ms);
  }
  m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})(?: (\d{1,2}):(\d{2})(?::(\d{2}))?)?$/.exec(s);
  if (m) {
    const [d, mo, y] = [Number(m[1]), Number(m[2]), Number(m[3])];
    if (!validDay(y, mo, d)) throw bad();
    if (m[4] !== undefined && (Number(m[4]) > 23 || Number(m[5]) > 59 || Number(m[6] || 0) > 59)) throw bad();
    return `${y}-${pad(mo)}-${pad(d)}`;
  }
  throw bad();
}

/** CONTRATTI.md «Lo storico»: `dtSeduta` when there is one, otherwise `dtRpr`; the record keeps
 *  which of the two it took. A row without `dtRpr` is not a row of that search. */
function dataDocumento(row) {
  const rpr = sourceDay(row.dtRpr, 'dtRpr');
  if (!rpr) throw new Error('dtRpr missing: the search filters on it (CONTRATTI.md, «Lo storico»)');
  const seduta = sourceDay(row.dtSeduta, 'dtSeduta');
  return seduta ? { day: seduta, from: 'dtSeduta' } : { day: rpr, from: 'dtRpr' };
}

/** The Municipio structure named by `dscStrOrg` (CONTRATTI.md «Lo storico», DEC-033 rule 1:
 *  «MUNIC…», «ROMA» when present, the Roman numeral compared whole), as the canonical
 *  `municipality_code`; null when it names none, or more than one. */
function municipalityCode(dscStrOrg) {
  const s = normalizeKey(dscStrOrg).toUpperCase();
  const found = new Set();
  for (const m of s.matchAll(/\bMUNIC\w*\.?\s*(?:ROMA\s*)?([IVX]+)\b/g)) {
    if (ROMANI.includes(m[1])) found.add(m[1]);
  }
  return found.size === 1 ? [...found][0] : null;
}

/** DEC-033, rule 1: the territorial groups of the Polizia Locale are not a Municipio structure. */
const isPoliziaLocale = (dscStrOrg) => /^P\.\s*L\.?\s*-/.test(normalizeKey(dscStrOrg).toUpperCase());

/** Stage 1: one search row (with `tipologia` set by the workflow) on `readingDay`.
 *  `keep` false carries the reason; a row kept today may still be skipped downstream
 *  when its `archive_id` is already in the archive. */
function describeRow(row, readingDay) {
  if (typeof readingDay !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(readingDay) ||
      !validDay(...readingDay.split('-').map(Number))) {
    throw new Error(`reading_day ${JSON.stringify(readingDay)} is not a YYYY-MM-DD day`);
  }
  const id = archiveId(row.tipologia, row.idDoc);
  const { day, from } = dataDocumento(row);
  const code = municipalityCode(row.dscStrOrg);
  let reason = null;
  if (code === null) reason = isPoliziaLocale(row.dscStrOrg) ? 'polizia_locale' : 'municipio_non_letto';
  else if (!MUNICIPI.includes(code)) reason = 'fuori_dai_municipi';
  else if (day < PERIOD_START) reason = 'prima_del_periodo';
  else if (day > readingDay) reason = 'data_futura'; // read again once the day has passed
  return {
    archive_id: id,
    tipo: normalizeKey(row.tipologia),
    keep: reason === null,
    reason,
    data_documento: day,
    data_documento_da: from,
    municipality_code: code,
    pdf_url: pdfUrl(row.tipologia, row.idDoc),
    file_stem: fileStem(id),
  };
}

/** Stage 2: the record to append for a downloaded original, or null when the latest
 *  version already holds the same file (CONTRATTI.md, «Lo storico»: same SHA-256, no new
 *  row). `existing` lists the versions already in the archive for this `archive_id`. */
function archiveRecord(archive, download, existing) {
  if (!archive || !archive.keep) throw new Error('only a kept row becomes a record');
  if (!download || !/^[0-9a-f]{64}$/.test(download.sha256 || '')) throw new Error('download.sha256 must be 64 hex digits');
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(download.retrieved_at || '')) {
    throw new Error('download.retrieved_at must be a UTC instant');
  }
  if (typeof download.workflow !== 'string' || !download.workflow.startsWith('staging_')) {
    throw new Error('download.workflow must name the staging_ workflow');
  }
  if (typeof download.elenco !== 'string' || !download.elenco.startsWith('originali/')) {
    throw new Error('download.elenco must be the saved search page in originali/');
  }
  // Absent is not empty: without the versions already written, a v1 could be written twice.
  if (!Array.isArray(existing)) throw new Error('existing must list the versions already in the archive ([] for none)');
  let latest = null;
  for (const r of existing) {
    if (!r || r.archive_id !== archive.archive_id) throw new Error(`existing record of another archive_id: ${r && r.archive_id}`);
    if (!Number.isInteger(r.versione) || r.versione < 1) throw new Error(`existing record with versione ${JSON.stringify(r.versione)}`);
    if (latest && r.versione === latest.versione) throw new Error(`two existing records with versione ${r.versione}`);
    if (!latest || r.versione > latest.versione) latest = r;
  }
  if (latest && latest.originale_sha256 === download.sha256) return null;
  const record = {
    archive_id: archive.archive_id,
    versione: latest ? latest.versione + 1 : 1,
    source_id: SOURCE_ID,
    registro_id: download.registro_id || null,
    source_url: archive.pdf_url,
    data_documento: archive.data_documento,
    municipality_code: archive.municipality_code,
    tipo: archive.tipo,
    provenienza: {
      url: download.url || archive.pdf_url,
      retrieved_at: download.retrieved_at,
      workflow: download.workflow,
      workflow_version: download.workflow_version || null,
      elenco: download.elenco,
      data_documento_da: archive.data_documento_da,
    },
    originale: `originali/${archive.file_stem}__${download.sha256.slice(0, 16)}.pdf`,
    originale_sha256: download.sha256,
    derivato: null,
    etichette: [],
    costo: null,
  };
  if (latest) record.motivo = 'originale cambiato alla fonte';
  return record;
}

function recordFileName(record) {
  return `${fileStem(record.archive_id)}__v${record.versione}.json`;
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = {
    SOURCE_ID, TIPI, MUNICIPI, PERIOD_START, normalizeKey, archiveId, planTipologie, mergePasses, fileStem, pdfUrl,
    sourceDay, dataDocumento, municipalityCode, describeRow, archiveRecord, recordFileName,
  };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter (see the header). */
if ($json.download) {
  const record = archiveRecord($json.archive, $json.download, $json.existing);
  $json.record = record;
  $json.record_file_name = record ? recordFileName(record) : null;
} else {
  $json.archive = describeRow($json, $json.reading_day);
}
return $input.item;

/**
 * archive-record.js — workstream D, the Atti Web reading of DEC-033: one row of the
 * portal's search becomes one record of the private history archive (DEC-023, rule 2).
 * It fixes what docs/pilota/CONTRATTI.md («Lo storico») leaves to the PR that opens D:
 * the form of `archive_id` and the values of `tipo`; tests/test_archive_record.js holds
 * the idempotency and normalization cases.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): this exact file is both the Node
 * module the tests require() and the full text of the n8n Code node ("Run Once for Each
 * Item"). The staging workflows use it in several nodes, byte-identical; `stage` on the item
 * says which step it takes:
 *   - 'plan': the menu answer becomes the tipologie to read;
 *   - 'pass': the answers of one pass over a tipologia become a pass and the pages to save;
 *   - 'close': the passes over a tipologia are merged and each row is described;
 *   - 'log': the closed tipologie become the register of the reading and its kept rows;
 *   - 'select': the kept rows become today's downloads, within the day's cap;
 *   - 'pdf': the answer to a PDF link is checked before it is hashed;
 *   - 'record' (or no stage, with `download` and `existing` set): it adds the `record` to
 *     append, or `record: null` when the archive already holds that original;
 *   - 'download_log': the outcomes of a download run become its register;
 *   - no stage, a search row: it adds `archive` (identity, perimeter verdict, PDF link).
 * The requests and the pause between them belong to the workflow (DEC-033, rule 2); the node
 * refuses a daily cap above the rule.
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
  // Every tipologia is read (DEC-033 rule 5): a menu that lacks a known one would make an
  // incomplete reading look complete, so it stops the reading too.
  const missing = TIPI.filter((c) => !codes.includes(c));
  if (missing.length) throw new Error(`menu without known tipologie: ${missing.join(', ')}: the reading does not start`);
  return codes.sort((a, b) => TIPI.indexOf(a) - TIPI.indexOf(b));
}

/** CONTRATTI.md «Lo storico» (DEC-033 rule 5), late publication: the passes over one
 *  tipologia (each `{ total, rows }`) count when the last two give the same total and the
 *  same set of idDoc; at most three passes. An empty response is `{ total: 0, rows: [],
 *  historical_total }`, with the acts the same tipologia returns over the historical
 *  interval («Risposta vuota»). The rows are merged by idDoc within the tipologia either
 *  way, and `complete` says what the registry records. */
function mergePasses(passes) {
  if (!Array.isArray(passes) || passes.length === 0 || passes.length > 3) {
    throw new Error('one to three passes over a tipologia (CONTRATTI.md, «Lo storico»)');
  }
  const ids = (p) => new Set((p.rows || []).map((r) => normalizeKey(r.idDoc)).filter((k) => /^[0-9]+$/.test(k)));
  const byId = new Map();
  for (const p of passes) for (const r of p.rows || []) byId.set(normalizeKey(r.idDoc), r);
  // A pass is whole when it holds exactly the rows it declares, each with a valid idDoc of its
  // own: a truncated pagination, or a row that cannot be read, is never complete, however stable.
  const whole = (p) => Number.isSafeInteger(p.total) && p.total >= 0 && Array.isArray(p.rows) &&
    p.rows.length === p.total && ids(p).size === p.total;
  // An empty response is an empty tipologia only when the historical interval returns acts;
  // otherwise it is missing data, and another pass would not change it.
  for (const p of passes) {
    if (p && p.total === 0 && !(Number.isSafeInteger(p.historical_total) && p.historical_total >= 0)) {
      throw new Error('an empty pass carries historical_total (CONTRATTI.md, «Lo storico», «Risposta vuota»)');
    }
  }
  const missing = passes.some((p) => p.total === 0 && p.historical_total === 0);
  const [a, b] = passes.slice(-2);
  const stable = !missing && passes.length >= 2 && whole(a) && whole(b) && a.total === b.total &&
    [...ids(a)].every((x) => ids(b).has(x));
  return { complete: stable, needs_another_pass: !stable && !missing && passes.length < 3, rows: [...byId.values()] };
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

/** A real UTC instant written as YYYY-MM-DDTHH:MM:SS(.fff)Z: no 30 February, no hour 25. */
function utcInstant(v) {
  const m = typeof v === 'string' && /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?Z$/.exec(v);
  if (!m) return false;
  const [y, mo, d, h, mi, se] = m.slice(1, 7).map(Number);
  return validDay(y, mo, d) && h < 24 && mi < 60 && se < 60;
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
  let s = v.trim();
  if (s === '') return null;
  // The convocations give `dtRpr` as two dates, `01/12/2025<br>(04/12/2025)<br>`: the first is
  // the repertorio date the search filters on, as the source study read it; the one in
  // brackets takes no part. Any other markup stays unreadable.
  const two = /^(\d{1,2}\/\d{1,2}\/\d{4})<br\s*\/?>\s*\(\d{1,2}\/\d{1,2}\/\d{4}\)(?:<br\s*\/?>)?$/i.exec(s);
  if (two) s = two[1];
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
  // A bracketed «(EX MUNICIPIO …)» is the former Municipio, not a second issuer (CONTRATTI.md «Lo storico»).
  const s = normalizeKey(dscStrOrg).toUpperCase().replace(/\(\s*EX\b[^)]*\)/g, ' ');
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

/** Lowercase SHA-256 as a string: a regex alone would accept a one-element array. */
const isSha256 = (v) => typeof v === 'string' && /^[0-9a-f]{64}$/.test(v);

/** Stage 2: the record to append for a downloaded original, or null when the latest
 *  version already holds the same file (CONTRATTI.md, «Lo storico»: same SHA-256, no new
 *  row). `existing` lists the versions already in the archive for this `archive_id`. */
function archiveRecord(archive, download, existing) {
  if (!archive || !archive.keep) throw new Error('only a kept row becomes a record');
  if (!download || !isSha256(download.sha256)) throw new Error('download.sha256 must be 64 hex digits');
  if (!utcInstant(download.retrieved_at)) {
    throw new Error('download.retrieved_at must be a UTC instant');
  }
  if (typeof download.workflow !== 'string' || !download.workflow.startsWith('staging_')) {
    throw new Error('download.workflow must name the staging_ workflow');
  }
  // A record is written once and never rewritten: provenance missing now stays missing.
  if (typeof download.workflow_version !== 'string' || !download.workflow_version.trim()) {
    throw new Error('download.workflow_version must name the version of the staging_ workflow');
  }
  if (typeof download.elenco !== 'string' || !download.elenco.startsWith('originali/')) {
    throw new Error('download.elenco must be the saved search page in originali/');
  }
  // Absent is not empty: without the versions already written, a v1 could be written twice.
  if (!Array.isArray(existing)) throw new Error('existing must list the versions already in the archive ([] for none)');
  let latest = null;
  const seen = new Set();
  for (const r of existing) {
    if (!r || r.archive_id !== archive.archive_id) throw new Error(`existing record of another archive_id: ${r && r.archive_id}`);
    if (!Number.isInteger(r.versione) || r.versione < 1) throw new Error(`existing record with versione ${JSON.stringify(r.versione)}`);
    // The hash decides whether a reading adds a version: without it a change would be invented.
    if (!isSha256(r.originale_sha256)) throw new Error(`existing record v${r.versione} without a valid originale_sha256`);
    if (seen.has(r.versione)) throw new Error(`two existing records with versione ${r.versione}`);
    seen.add(r.versione);
    if (!latest || r.versione > latest.versione) latest = r;
  }
  // Versions go up by one from 1: a gap means a truncated listing, not a history to build on.
  if (latest && seen.size !== latest.versione) throw new Error(`existing versions are not 1 to ${latest.versione}: the listing is incomplete`);
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
      workflow_version: download.workflow_version,
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

/* ----- the reading: menu, pages, passes, reading log (CONTRATTI.md «Lo storico») --------- */

/** The search filters on `dtRpr` from this day to the reading day (CONTRATTI.md, «Lo storico»). */
const SEARCH_START = '2025-12-01';
/** Rows per page of the search: the most the portal accepts (docs/sources/A2_ATTIWEB_TIPOLOGIE.md, §2). */
const PAGE_SIZE = 500;
/** DEC-033, rule 2: the most documents read in a day. */
const MAX_PER_DAY = 300;
/** The portal's answer for a search with no rows (docs/sources/A2_ATTIWEB_TIPOLOGIE.md, §7.1). */
const EMPTY_ANSWER = /Index:\s*0,\s*Size:\s*0/;

const isDay = (v) => typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && validDay(...v.split('-').map(Number));
const bodyText = (res) => (typeof res.body === 'string' ? res.body : JSON.stringify(res.body === undefined ? null : res.body));

/** The codes of the menu answer (`caricaListaTipologie`): its first list, the combined codes
 *  (with a comma) left out, as in the source study. What does not read stops the reading. */
function menuCodes(answer) {
  let a = answer;
  if (typeof a === 'string') {
    try { a = JSON.parse(a); } catch (e) { a = null; }
  }
  const list = a && typeof a === 'object' ? Object.values(a).find(Array.isArray) : null;
  if (!list) throw new Error('the list of tipologie did not read: the reading does not start');
  return list.map((x) => (x && typeof x.codice === 'string' ? x.codice : '')).filter((c) => c && !c.includes(','));
}

/** Stage 'plan': the full answer of the menu request becomes the tipologie to read; a block
 *  on it stops the reading before it starts (DEC-033, rule 4). */
function planFromMenu(response) {
  const signal = blockSignal(response);
  if (signal) throw new Error(`blocked (${signal}): the reading stops (DEC-033, rule 4)`);
  return planTipologie(menuCodes(response.body));
}

/** DEC-033, rule 4: the signal on one answer (`{ statusCode, headers, body }`, redirects not
 *  followed) that stops the reading, or null. Any redirect counts: the login page is one. */
function blockSignal(res) {
  if (!res || typeof res !== 'object') return 'no answer';
  const code = Number(res.statusCode);
  if (code === 401 || code === 403 || code === 429) return `HTTP ${code}`;
  if (code >= 300 && code < 400) {
    const h = res.headers || {};
    return `redirect to ${h.location || h.Location || '(no location)'}`;
  }
  const body = bodyText(res);
  if (/captcha/i.test(body)) return 'captcha';
  if (/<input[^>]+type=["']?password/i.test(body)) return 'login page';
  return null;
}

/** One answer of the search: its rows and the total it declares, the empty answer, or an
 *  error, which leaves the pass incomplete. */
function parseSearch(res) {
  let body = res.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch (e) {
      return EMPTY_ANSWER.test(res.body) ? { kind: 'empty' } : { kind: 'error', detail: `HTTP ${res.statusCode}: not JSON` };
    }
  }
  if (!body || !Array.isArray(body.elencoAtti)) return { kind: 'error', detail: `HTTP ${res.statusCode}: no elencoAtti` };
  const total = Number(body.total);
  if (!Number.isSafeInteger(total) || total < 0) return { kind: 'error', detail: 'the declared total is not a whole number' };
  return { kind: 'rows', total, rows: body.elencoAtti };
}

/** The saved page of the search, in originali/: one file per page, pass and reading day. */
function elencoFileName(readingDay, tipologia, pass, page) {
  return `attiweb_elenco_${readingDay}_${normalizeKey(tipologia)}_p${pass}_${page}.json`;
}

/** Stage 'pass': the answers of one pass over a tipologia, in page order, become a pass for
 *  `mergePasses` (`pass_result`: `pass` is the pass's number); each row carries its tipologia
 *  and the saved page it came from, and `files` are the pages to save under those names. A first answer that is the empty one asks for the
 *  check over the historical interval (`needs_historical`), whose total the pass then carries. */
function searchPass({ tipologia, reading_day, pass, pages, historical }) {
  const tipo = normalizeKey(tipologia);
  if (!TIPI.includes(tipo)) throw new Error(`tipologia ${JSON.stringify(tipologia)} is not a value of tipo`);
  if (!isDay(reading_day)) throw new Error(`reading_day ${JSON.stringify(reading_day)} is not a YYYY-MM-DD day`);
  if (!Number.isInteger(pass) || pass < 1 || pass > 3) throw new Error('pass is 1, 2 or 3 (CONTRATTI.md, «Lo storico»)');
  if (!Array.isArray(pages) || pages.length === 0) throw new Error('a pass has at least one answer');
  for (const res of pages.concat(historical ? [historical] : [])) {
    const signal = blockSignal(res);
    if (signal) throw new Error(`blocked (${signal}): the reading stops (DEC-033, rule 4)`);
  }
  const files = pages.map((res, i) => ({ name: elencoFileName(reading_day, tipo, pass, i), body: bodyText(res) }));
  const parsed = pages.map(parseSearch);
  if (parsed[0].kind === 'empty' && parsed.every((x) => x.kind === 'empty')) {
    if (!historical) return { needs_historical: true, files, pass_result: null };
    const h = parseSearch(historical);
    return { needs_historical: false, files, pass_result: { total: 0, rows: [], historical_total: h.kind === 'rows' ? h.total : 0 } };
  }
  // The page after a full last page can be the empty answer: it ends the pass, it is not an error.
  let last = parsed.length;
  while (last > 1 && parsed[last - 1].kind === 'empty') last -= 1;
  const bad = parsed.slice(0, last).find((x) => x.kind !== 'rows');
  if (bad) return { needs_historical: false, files, pass_result: { total: null, rows: [], error: bad.detail || 'an empty answer between pages' } };
  const total = parsed[0].total;
  if (parsed.slice(0, last).some((x) => x.total !== total)) {
    return { needs_historical: false, files, pass_result: { total: null, rows: [], error: 'the declared total changed between pages' } };
  }
  const rows = [];
  parsed.slice(0, last).forEach((x, i) => {
    for (const r of x.rows) rows.push(Object.assign({}, r, { tipologia: tipo, elenco: `originali/${files[i].name}` }));
  });
  return { needs_historical: false, files, pass_result: { total, rows } };
}

/** Stage 'close': the passes over one tipologia, merged (`mergePasses`), and each row described
 *  (`describeRow`). A row that cannot become a record is counted, never written. */
function closeTipologia({ tipologia, reading_day, passes }) {
  const tipo = normalizeKey(tipologia);
  if (!TIPI.includes(tipo)) throw new Error(`tipologia ${JSON.stringify(tipologia)} is not a value of tipo`);
  if (!isDay(reading_day)) throw new Error(`reading_day ${JSON.stringify(reading_day)} is not a YYYY-MM-DD day`);
  const merged = mergePasses(passes);
  const kept = [];
  const left_out = {};
  for (const r of merged.rows) {
    let a;
    try {
      a = describeRow(Object.assign({}, r, { tipologia: tipo }), reading_day);
    } catch (e) {
      a = { keep: false, reason: 'riga_illeggibile' };
    }
    if (a.keep) kept.push({ archive: a, elenco: r.elenco });
    else left_out[a.reason] = (left_out[a.reason] || 0) + 1;
  }
  const lastPass = passes[passes.length - 1];
  return {
    tipologia: tipo,
    complete: merged.complete,
    needs_another_pass: merged.needs_another_pass,
    passes: passes.length,
    total: lastPass && Number.isSafeInteger(lastPass.total) ? lastPass.total : null,
    missing_data: passes.some((x) => x && x.total === 0 && x.historical_total === 0),
    errors: passes.map((x) => x && x.error).filter(Boolean),
    kept,
    left_out,
  };
}

/** `20261110T201500Z` from a UTC instant: the time part of the reading's file names. */
const compactInstant = (v) => v.slice(0, 19).replace(/[-:]/g, '') + 'Z';

/** Stage 'log': the register of one reading (DEC-033, rule 5), from the closed tipologie. The
 *  reading is complete only when every value of `tipo` was read and is complete; `righe` are the
 *  kept rows for the download workflow. */
function readingLog({ reading_day, started_at, finished_at, workflow, workflow_version, tipologie }) {
  if (!isDay(reading_day)) throw new Error(`reading_day ${JSON.stringify(reading_day)} is not a YYYY-MM-DD day`);
  if (!utcInstant(started_at) || !utcInstant(finished_at)) throw new Error('started_at and finished_at must be UTC instants');
  if (typeof workflow !== 'string' || !workflow.startsWith('staging_')) throw new Error('workflow must name the staging_ workflow');
  if (typeof workflow_version !== 'string' || !workflow_version.trim()) throw new Error('workflow_version must name the version');
  if (!Array.isArray(tipologie)) throw new Error('tipologie must list the closed tipologie');
  const byTipo = new Map();
  for (const t of tipologie) {
    if (!t || !TIPI.includes(t.tipologia)) throw new Error(`a closed tipologia that is not a value of tipo: ${t && t.tipologia}`);
    if (byTipo.has(t.tipologia)) throw new Error(`tipologia ${t.tipologia} closed twice`);
    byTipo.set(t.tipologia, t);
  }
  const unread = TIPI.filter((c) => !byTipo.has(c));
  const rows = TIPI.filter((c) => byTipo.has(c)).map((c) => {
    const t = byTipo.get(c);
    return { tipologia: c, complete: t.complete === true, passes: t.passes, total: t.total,
      missing_data: t.missing_data === true, errors: t.errors || [], kept: (t.kept || []).length, left_out: t.left_out || {} };
  });
  const incomplete = rows.filter((r) => !r.complete).map((r) => r.tipologia).concat(unread);
  const seen = new Set();
  const righe = [];
  for (const c of TIPI) {
    for (const k of (byTipo.get(c) || {}).kept || []) {
      if (seen.has(k.archive.archive_id)) continue;
      seen.add(k.archive.archive_id);
      righe.push(k);
    }
  }
  const stamp = compactInstant(started_at);
  return {
    log_file_name: `attiweb_lettura_${stamp}.json`,
    righe_file_name: `attiweb_righe_${stamp}.json`,
    log: {
      source_id: SOURCE_ID, reading_day, started_at, finished_at, workflow, workflow_version,
      periodo: { dtRpr_da: SEARCH_START, dtRpr_a: reading_day, data_documento_da: PERIOD_START },
      municipi: MUNICIPI.slice(),
      complete: incomplete.length === 0,
      incomplete,
      unread,
      kept_total: righe.length,
      tipologie: rows,
    },
    righe,
  };
}

/** The register of one download run: its name carries the day and how many documents it read. */
function downloadLogName(readingDay, count, startedAt) {
  if (!isDay(readingDay)) throw new Error(`reading_day ${JSON.stringify(readingDay)} is not a YYYY-MM-DD day`);
  if (!Number.isSafeInteger(count) || count < 0) throw new Error('count must be a whole number');
  if (!utcInstant(startedAt)) throw new Error('started_at must be a UTC instant');
  return `attiweb_download_${readingDay}_n${count}_${compactInstant(startedAt)}.json`;
}

/** What the download runs of a day already read, from the names of their registers. */
function downloadedToday(names, readingDay) {
  if (!Array.isArray(names)) throw new Error('names must list the download registers ([] for none)');
  if (!isDay(readingDay)) throw new Error(`reading_day ${JSON.stringify(readingDay)} is not a YYYY-MM-DD day`);
  let n = 0;
  for (const name of names) {
    const mm = typeof name === 'string' && /^attiweb_download_(\d{4}-\d{2}-\d{2})_n(\d+)_\d{8}T\d{6}Z\.json$/.exec(name);
    if (mm && mm[1] === readingDay) n += Number(mm[2]);
  }
  return n;
}

/** Stage 'select': today's downloads from the kept rows of the latest reading, those whose
 *  `archive_id` has no record in the archive yet, within the day's cap (DEC-033, rule 2) and
 *  the run's own limit. `existing_names` are the file names in `D Storico/`; `downloaded_today`
 *  what earlier runs of the day already read. */
function selectDownloads({ righe, existing_names, downloaded_today, cap, run_limit }) {
  if (!Array.isArray(righe)) throw new Error('righe must list the kept rows of a reading');
  if (!Array.isArray(existing_names)) throw new Error('existing_names must list the files in D Storico/ ([] for none)');
  if (!Number.isSafeInteger(downloaded_today) || downloaded_today < 0) throw new Error('downloaded_today must be a whole number');
  if (!Number.isSafeInteger(cap) || cap < 0 || cap > MAX_PER_DAY) throw new Error(`cap must be a whole number from 0 to ${MAX_PER_DAY} (DEC-033, rule 2)`);
  const recorded = new Set();
  for (const n of existing_names) {
    const mm = typeof n === 'string' && /^(.+)__v[1-9][0-9]*\.json$/.exec(n);
    if (mm) recorded.add(mm[1]);
  }
  const limit = run_limit === undefined ? cap : run_limit;
  if (!Number.isSafeInteger(limit) || limit < 0) throw new Error('run_limit must be a whole number');
  const room = Math.max(0, Math.min(limit, cap - downloaded_today));
  const out = [];
  const seen = new Set();
  for (const r of righe) {
    if (out.length >= room) break;
    if (!r || !r.archive || !r.archive.keep || typeof r.archive.file_stem !== 'string') throw new Error('a row of righe without its archive');
    if (recorded.has(r.archive.file_stem) || seen.has(r.archive.file_stem)) continue;
    seen.add(r.archive.file_stem);
    out.push(r);
  }
  return out;
}

/** Stage 'download_log': the register of one download run, from the outcome of each document
 *  it read (`{ archive_id, written, reason }`); its name carries the day and the count. */
function downloadLog({ reading_day, started_at, finished_at, workflow, workflow_version, esiti }) {
  if (!utcInstant(finished_at)) throw new Error('finished_at must be a UTC instant');
  if (typeof workflow !== 'string' || !workflow.startsWith('staging_')) throw new Error('workflow must name the staging_ workflow');
  if (typeof workflow_version !== 'string' || !workflow_version.trim()) throw new Error('workflow_version must name the version');
  if (!Array.isArray(esiti)) throw new Error('esiti must list the documents read');
  const read = esiti.filter((e) => e && typeof e.archive_id === 'string');
  if (read.length !== esiti.length) throw new Error('an outcome without its archive_id');
  return {
    name: downloadLogName(reading_day, read.length, started_at),
    log: {
      source_id: SOURCE_ID, reading_day, started_at, finished_at, workflow, workflow_version,
      read: read.length,
      written: read.filter((e) => e.written === true).length,
      not_written: read.filter((e) => e.written !== true).map((e) => ({ archive_id: e.archive_id, reason: e.reason || null })),
    },
  };
}

/** Stage 'pdf': the answer to a PDF link (`{ statusCode, headers }`, the binary's MIME type and
 *  extension, whether it has content) is an original to hash, a block that stops the reading, or
 *  something else, which is counted and not written. The portal sends its PDFs as
 *  `application/octet-stream` with a `.pdf` file name. */
function checkPdf({ response, mime, file_extension, has_content }) {
  const signal = blockSignal(Object.assign({ body: '' }, response));
  if (signal) throw new Error(`blocked (${signal}): the reading stops (DEC-033, rule 4)`);
  if (Number(response.statusCode) !== 200) return { ok: false, reason: `HTTP ${response.statusCode}` };
  const pdf = mime === 'application/pdf' || (mime === 'application/octet-stream' && String(file_extension).toLowerCase() === 'pdf');
  if (!pdf) return { ok: false, reason: `not a PDF: ${mime}` };
  if (has_content !== true) return { ok: false, reason: 'empty file' };
  return { ok: true, reason: null };
}

function recordFileName(record) {
  return `${fileStem(record.archive_id)}__v${record.versione}.json`;
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = {
    SOURCE_ID, TIPI, MUNICIPI, PERIOD_START, SEARCH_START, PAGE_SIZE, MAX_PER_DAY, normalizeKey, archiveId,
    planTipologie, mergePasses, fileStem, pdfUrl, sourceDay, dataDocumento, municipalityCode, describeRow,
    archiveRecord, recordFileName, menuCodes, blockSignal, parseSearch, elencoFileName, searchPass,
    closeTipologia, readingLog, selectDownloads, checkPdf, planFromMenu, downloadLogName, downloadedToday,
    downloadLog,
  };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter (see the header). */
if ($json.stage === 'plan') {
  $json.tipologie = planFromMenu($json.response);
  delete $json.response;
} else if ($json.stage === 'pass') {
  Object.assign($json, searchPass($json));
  delete $json.pages;
  delete $json.historical;
} else if ($json.stage === 'close') {
  $json.result = closeTipologia($json);
  delete $json.passes;
} else if ($json.stage === 'log') {
  Object.assign($json, readingLog($json));
  delete $json.tipologie;
} else if ($json.stage === 'select') {
  const downloaded_today = downloadedToday(($json.download_log_names || []).filter(Boolean), $json.reading_day);
  $json.downloaded_today = downloaded_today;
  $json.downloads = selectDownloads(Object.assign({}, $json, {
    existing_names: ($json.existing_names || []).filter(Boolean), downloaded_today }));
  delete $json.righe;
  delete $json.existing_names;
} else if ($json.stage === 'pdf') {
  // n8n gives the size in `bytes`, and as text in `fileSize` ("45.3 kB"): only whether it is zero matters.
  const bin = ($input.item.binary || {}).data || {};
  const size = String(bin.fileSize === undefined ? '' : bin.fileSize).trim();
  const has_content = bin.bytes !== undefined ? Number(bin.bytes) > 0 : size !== '' && !/^0(\.0+)?\s*[kMG]?B$/i.test(size);
  $json.pdf = checkPdf({ response: $json.response, mime: bin.mimeType, file_extension: bin.fileExtension, has_content });
} else if ($json.stage === 'download_log') {
  Object.assign($json, downloadLog($json));
  delete $json.esiti;
} else if ($json.stage === 'record' || $json.download) {
  const record = archiveRecord($json.archive, $json.download, $json.existing);
  $json.record = record;
  $json.record_file_name = record ? recordFileName(record) : null;
} else {
  $json.archive = describeRow($json, $json.reading_day);
}
return $input.item;

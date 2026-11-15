/**
 * romatv-list.js — workstream A: the list of the RomaTV catalogues — the request of one page,
 * what a page brings (the recordings inside the window, read as the record of registrazioni/
 * needs them), when the reading of a catalogue stops and why, and which parts of a split sitting
 * are bound in order. The rules are in docs/pilota/CONTRATTI.md, section 7 («A · Amministrazione»,
 * rows Fonti, Raccolta and Registrazione) and docs/pilota/WORKSTREAM_A.md, section 5 («Il
 * confine», the parts); this file does not restate them. The requests themselves and their pause
 * belong to source-guard.js. Acceptance: tests/test_romatv_list.js (T-A2-01…T-A2-04, T-A2-06,
 * T-A2-13).
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item") the same file runs
 * its adapter. `stage` on the item says which step it takes:
 *   - 'request': the request of a page of a catalogue, for source-guard.js;
 *   - 'page': one answer read into the catalogue's reading, and whether another page follows;
 *   - 'links': over all the recordings of the run, the parts of split sittings and their links.
 */
'use strict';

/** CONTRATTI section 7 (A), rows Fonti and Registrazione (`municipality_code`). */
const API = 'https://api-ovp.streamcloud.it/garavot/ac104/api/v1/contents/search_frontend';
const PORTAL = 'https://streaming.comune.roma.it';
const CATALOGS = Object.freeze([
  Object.freeze({ catalogo: 'Municipio V', municipality_code: 'V' }),
  Object.freeze({ catalogo: 'Municipio X', municipality_code: 'X' }),
  Object.freeze({ catalogo: 'Commissioni Capitoline', municipality_code: null }),
  Object.freeze({ catalogo: 'Assemblee Capitoline', municipality_code: null }),
]);
/** CONTRATTI section 7 (A), row Raccolta: pages, their cap, the window and the first day. */
const PAGE_SIZE = 100;
const MAX_PAGES = 4;
const WINDOW_DAYS = 100;
const FIRST_DAY = '2026-11-01';
const DAY_MS = 24 * 3600 * 1000;

const UUID = /^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$/;
const ROME_DAY = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' });
const romeDay = (ms) => ROME_DAY.format(new Date(ms));

function catalogOf(name) {
  const c = CATALOGS.find((x) => x.catalogo === name);
  if (!c) throw new Error(`catalog_unknown: ${name}`);
  return c;
}

/** The request of one page (1…MAX_PAGES), sorted by the date of the sitting, newest first. The
 *  portal's headers go only when the flow asks for them (DEC-036, point 2; WORKSTREAM_A, section 4,
 *  the road of the audio, step 3). */
function pageRequest(catalogo, page, portalHeaders) {
  catalogOf(catalogo);
  if (!Number.isInteger(page) || page < 1 || page > MAX_PAGES) throw new Error('page_invalid');
  const headers = { Accept: 'application/json', 'Content-Type': 'application/json' };
  if (portalHeaders === true) Object.assign(headers, { Origin: PORTAL, Referer: `${PORTAL}/` });
  return { url: API, method: 'POST', expects: 'json', headers,
    body: { page, pageSize: PAGE_SIZE, filters: { discriminator: null, catalog: [catalogo] },
      sortBy: [{ sortField: 'ReferenceDate', direction: 'Descending' }], includeAggregations: false } };
}

const INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(?:(Z)|([+-])(\d{2}):?(\d{2}))$/;
/** An instant with its offset, in UTC to the second; one without an offset is refused, never
 *  read in a guessed zone (as institutional-identity.js, toUtcSecond). */
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

/** RomaTV's duration, `hh:mm:ss.fffffff`, in whole seconds; none for zero, which is not yet a
 *  recording (it enters with a later list, when it has its duration). */
function durationSeconds(value) {
  const m = typeof value === 'string' ? /^(\d{2,}):([0-5]\d):([0-5]\d)(?:\.\d{1,7})?$/.exec(value) : null;
  const secs = m ? Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]) : 0;
  return secs > 0 ? secs : null;
}

function instant(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(v) || Number.isNaN(Date.parse(v))) {
    throw new Error('now must be a UTC instant');
  }
  return v;
}

/** T-A2-03, T-A2-04: whether a sitting is inside the window at `now` (CONTRATTI section 7 (A),
 *  row Raccolta). */
function inWindow(referenceUtc, now) {
  const ref = Date.parse(referenceUtc);
  return !Number.isNaN(ref) && ref >= Date.parse(instant(now)) - WINDOW_DAYS * DAY_MS && romeDay(ref) >= FIRST_DAY;
}

const ORDINALS = { prima: 1, primo: 1, seconda: 2, secondo: 2, terza: 3, terzo: 3, quarta: 4, quarto: 4, quinta: 5, quinto: 5, sesta: 6, sesto: 6 };
const ROMAN = { i: 1, ii: 2, iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10 };
const PART_FORMS = [
  /\bparte\s+(\d{1,2}|[ivx]{1,4}|prima|seconda|terza|quarta|quinta|sesta)\b/i,
  /\b(\d{1,2}|[ivx]{1,4})\s*(?:a|ª|°|º)?\s+parte\b/i,
  /\b(prima|seconda|terza|quarta|quinta|sesta|primo|secondo|terzo|quarto|quinto|sesto)\s+parte\b/i,
];
const numberOf = (w) => {
  const k = w.toLowerCase();
  if (/^\d+$/.test(k)) return Number(k);
  return ROMAN[k] || ORDINALS[k] || null;
};
const fold = (t) => t.normalize('NFC').toLowerCase().replace(/[\p{P}\s]+/gu, '');
const tidy = (t) => t.replace(/\(\s*\)/g, ' ').replace(/^[\s\-–—:,;.]+|[\s\-–—:,;.]+$/g, '').replace(/\s+/g, ' ');

/** WORKSTREAM_A, section 5, «Il confine»: the part a title declares, the title without it as
 *  published (`rest`) and the same folded (`base`), the key of the organ when the portal gives
 *  none. A title that declares no part has `part: null`. */
function partOf(title) {
  const t = typeof title === 'string' ? title.normalize('NFC') : '';
  for (const re of PART_FORMS) {
    const m = re.exec(t);
    if (m) {
      const n = numberOf(m[1]);
      const rest = tidy(t.slice(0, m.index) + ' ' + t.slice(m.index + m[0].length));
      if (n) return { part: n, rest, base: fold(rest) };
    }
  }
  return { part: null, rest: tidy(t), base: fold(t) };
}

/** T-A2-01, T-A2-02: one entry of a page as the channel keeps it (CONTRATTI section 7 (A), row
 *  Registrazione; the organ: WORKSTREAM_A, section 5, «Il confine»), or the reason it is not kept. */
function readEntry(raw, catalogo) {
  const c = catalogOf(catalogo);
  const it = raw && typeof raw === 'object' ? raw : {};
  if (typeof it.guid !== 'string' || !UUID.test(it.guid)) return { ok: false, reason: 'guid_invalid', guid: typeof it.guid === 'string' ? it.guid : null };
  const guid = it.guid.toLowerCase();
  const reference = utcSecond(it.referenceDate);
  if (!reference) return { ok: false, reason: 'reference_date_invalid', guid };
  const duration = durationSeconds(it.duration);
  if (duration === null) return { ok: false, reason: 'duration_invalid', guid };
  const tracks = Array.isArray(it.tracks) ? it.tracks : [];
  const speech = tracks.find((t) => t && t.trackType === 'SpeechToTextTrack' && (t.speechToTextTrackSource || t.speechToTextTrackWebVtt));
  const smil = (Array.isArray(it.smilFiles) ? it.smilFiles : []).find((s) => s && s.smilFileType === 'AudioOnly' && typeof s.url === 'string');
  const route = it.contentType === 'Video' ? 'vod' : it.contentType === 'Commission' ? 'commission' : null;
  const title = typeof it.title === 'string' ? it.title : '';
  const { part, rest } = partOf(title);
  const body = typeof it.governmentBody === 'string' && it.governmentBody.trim() ? it.governmentBody.trim() : null;
  return { ok: true, rec: {
    recording_ref: `romatv:${guid}`, piattaforma: 'romatv', catalogo, municipality_code: c.municipality_code,
    organo: body || rest, organo_chiave: fold(body || rest), titolo: title, numero_parte: part,
    ora_riferimento_utc: reference, ora_pubblicazione_utc: utcSecond(it.insertDate), durata_secondi: duration,
    trascrizione_piattaforma: !!speech,
    parlato_url: speech && typeof speech.speechToTextTrackSource === 'string' ? speech.speechToTextTrackSource : null,
    vtt_url: speech && typeof speech.speechToTextTrackWebVtt === 'string' ? speech.speechToTextTrackWebVtt : null,
    audio_url: smil ? smil.url.replace(/\/+$/, '') : null,
    url: route ? `${PORTAL}/portal/watch/${route}/${guid}` : null, content_type: typeof it.contentType === 'string' ? it.contentType : null,
  } };
}

/** The reading of one catalogue in a run, before its first page. */
function startReading(catalogo) {
  catalogOf(catalogo);
  return { catalogo, page: 0, next_page: 1, done: false, complete: null, reason: null, guids: [], last_ms: null,
    records: [], skipped: [] };
}

/** T-A2-04, T-A2-13: one page's answer body read into the reading (a copy is returned), by the
 *  stops of CONTRATTI section 7 (A), row Raccolta, with the builder's reading there on empty pages.
 *  Entries that cannot be kept, or that a page gives twice, are listed with their reason. */
function readPage(reading, body, now) {
  instant(now);
  const r = JSON.parse(JSON.stringify(reading));
  if (r.done) throw new Error('reading_done');
  r.page = r.next_page;
  const stop = (complete, reason) => Object.assign(r, { done: true, complete, reason, next_page: null });
  const data = body && typeof body === 'object' ? body.data : null;
  const items = data && Array.isArray(data.items) ? data.items : null;
  if (!items) return stop(false, 'answer without a list of entries');
  if (!items.length) {
    if (r.page === 1) return stop(false, 'empty first page');
    return data.hasNext === false ? stop(true, 'end of the catalogue') : stop(false, `empty page ${r.page} with more to come`);
  }
  if (items.some((it) => it && typeof it.guid === 'string' && r.guids.includes(it.guid.toLowerCase()))) {
    return stop(false, `page ${r.page} repeats entries already read in this run`);
  }
  const times = items.map((it) => Date.parse(utcSecond(it && it.referenceDate) || '')).filter((t) => !Number.isNaN(t));
  if (r.last_ms !== null && times.length && Math.max(...times) > r.last_ms) {
    return stop(false, `the dates of the sittings rise from page ${r.page - 1} to page ${r.page}`);
  }
  for (const it of items) {
    if (it && typeof it.guid === 'string') {
      if (r.guids.includes(it.guid.toLowerCase())) { r.skipped.push({ guid: it.guid.toLowerCase(), reason: 'repeated in the page' }); continue; }
      r.guids.push(it.guid.toLowerCase());
    }
    const e = readEntry(it, r.catalogo);
    if (!e.ok) { r.skipped.push({ guid: e.guid, reason: e.reason }); continue; }
    if (!inWindow(e.rec.ora_riferimento_utc, now)) return stop(true, 'left the window');
    r.records.push(e.rec);
  }
  if (times.length) r.last_ms = Math.min(...times);
  if (data.hasNext === false) return stop(true, 'end of the catalogue');
  if (r.page >= MAX_PAGES) return stop(false, `${MAX_PAGES} pages without leaving the window`);
  r.next_page = r.page + 1;
  return r;
}

/** The reading stopped by a request that did not bring a page (source-guard.js, its verdict). A
 *  request not made because the host was already stopped is `host_stopped`: its stop had its
 *  alert. One not made because robots.txt is not checked today is not. */
function readFailure(reading, v) {
  const r = JSON.parse(JSON.stringify(reading));
  if (r.done) throw new Error('reading_done');
  return Object.assign(r, { page: r.next_page, done: true, complete: false, next_page: null, host_stopped: !!v && v.outcome === 'skipped' && v.host_stopped === true,
    reason: `page ${r.next_page} not read: ${v && v.outcome ? v.outcome : 'no verdict'}${v && v.reason ? ` (${v.reason})` : ''}` });
}

/** T-A2-06: the links of the parts of split sittings among the RomaTV recordings of a run, by
 *  WORKSTREAM_A, section 5, «Il confine». The recordings of the same organ and day that did not
 *  bind are listed with the reason; a recording twice in the run (a page, two catalogues) is kept once in `records` and listed. */
function linkParts(records) {
  const groups = new Map();
  const seen = new Set();
  const duplicates = [];
  const once = [];
  for (const rec of records || []) {
    if (!rec || !rec.recording_ref) continue;
    if (seen.has(rec.recording_ref)) { duplicates.push(rec.recording_ref); continue; }
    seen.add(rec.recording_ref);
    once.push(rec);
    if (!rec.organo_chiave) continue;
    const key = `${rec.catalogo}\u0000${rec.organo_chiave}\u0000${romeDay(Date.parse(rec.ora_riferimento_utc))}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(rec);
  }
  const links = {};
  const unbound = [];
  for (const group of groups.values()) {
    if (group.length < 2 && !(group.length === 1 && group[0].numero_parte > 1)) continue;
    const declared = group.filter((r) => r.numero_parte);
    const plain = group.filter((r) => !r.numero_parte);
    if (plain.length && group.length > 1) unbound.push({ refs: plain.map((r) => r.recording_ref).sort(), reason: 'no part declared' });
    const byN = new Map();
    for (const r of declared) byN.set(r.numero_parte, (byN.get(r.numero_parte) || []).concat([r]));
    for (const [n, rs] of byN) {
      if (rs.length > 1) unbound.push({ refs: rs.map((r) => r.recording_ref).sort(), reason: `part ${n} declared twice` });
    }
    const first = byN.get(1);
    let prev = first && first.length === 1 ? first[0] : null;
    let chainBroken = !prev;
    const ns = [...byN.keys()].filter((n) => n > 1).sort((a, b) => a - b);
    for (const n of ns) {
      const rs = byN.get(n);
      if (rs.length > 1) { chainBroken = true; continue; }
      const r = rs[0];
      const reason = chainBroken || !prev || prev.numero_parte !== n - 1 ? `part ${n} without part ${n - 1} before it`
        : Date.parse(r.ora_riferimento_utc) < Date.parse(prev.ora_riferimento_utc) + prev.durata_secondi * 1000
          ? `part ${n} starts before part ${n - 1} ends` : null;
      if (reason) {
        unbound.push({ refs: [r.recording_ref], reason });
        chainBroken = true;
        continue;
      }
      links[r.recording_ref] = { parte_precedente: prev.recording_ref, prima_parte: (links[prev.recording_ref] || { prima_parte: prev.recording_ref }).prima_parte };
      prev = r;
    }
  }
  return { records: once, links, unbound, duplicates };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { API, PORTAL, CATALOGS, PAGE_SIZE, MAX_PAGES, WINDOW_DAYS, FIRST_DAY, pageRequest, utcSecond, durationSeconds,
    inWindow, partOf, readEntry, startReading, readPage, readFailure, linkParts };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. 'request' reads `reading` (or starts one
 * for `catalogo`) and `portal_headers`, and writes `request`; 'page' reads `reading`, the
 * `verdict` and `answer` of source-guard.js and `now`, and writes `reading`: a request that did
 * not bring a page stops the reading with its verdict; 'links' reads `records` and writes them once
 * each, with `links`, `unbound` and `duplicates`. */
if ($json.stage === 'request') {
  const reading = $json.reading || startReading($json.catalogo);
  Object.assign($json, { reading, request: pageRequest(reading.catalogo, reading.next_page, $json.portal_headers === true) });
  return $input.item;
}
if ($json.stage === 'page') {
  const v = $json.verdict;
  $json.reading = v && v.outcome === 'ok' ? readPage($json.reading, ($json.answer || {}).body, $json.now) : readFailure($json.reading, v);
  return $input.item;
}
if ($json.stage === 'links') {
  Object.assign($json, linkParts($json.records));
  return $input.item;
}
throw new Error(`romatv-list.js: unknown stage ${JSON.stringify($json.stage)}`);

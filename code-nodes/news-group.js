/**
 * news-group.js — workstream B: which records tell the same fact. This part carries step 1 of
 * docs/pilota/B_RAGGRUPPAMENTO.md (preparation) and the check of the model's answer of step 2;
 * steps 3 to 5, the check of step 4 and what the grouping adds to news-fact.js come with the
 * next parts of B-R1 (section 9). The rules are in that document, sections 2, 3 and 6, and in
 * docs/pilota/CONTRATTI.md, section 7 («B · Notizie»); this file does not restate them.
 * The model reads and proposes, this code decides (section 4).
 *
 * The canonical URL and `validInstant` are copies of
 * news-identity.js and news-fact.js, because an n8n Code node cannot require another file;
 * tests/test_news_group.js keeps them byte-equal.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so
 * the tail exports and stops; inside the n8n Code node ("Run Once for Each Item", JavaScript)
 * the same file runs its per-item adapter.
 */
'use strict';

/* ----- copies kept byte-equal by the tests ------------------------------- */

/** Query parameters that track a visit and never identify a page. */
const TRACKING_PARAM = /^(utm_[a-z0-9_]+|fbclid|gclid|dclid|msclkid|mc_cid|mc_eid|_ga|_gl)$/i;

/** The characters the WHATWG URL standard percent-encodes in an http(s) path: C0 controls,
 *  space, `"`, `<`, `>`, `^`, `` ` ``, `{`, `}`, DEL and everything outside ASCII. Any other
 *  character, `%` included, is kept as it is. `^` follows the current standard, as Node 24
 *  does; older parsers keep it. */
const PATH_ENCODE = /[\u0000-\u0020"<>^`{}\u007f-\u{10ffff}]/u;
/** An unpaired UTF-16 surrogate, which the URL standard reads as U+FFFD. */
const LONE_SURROGATE = /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/g;

/** application/x-www-form-urlencoded, the serialization of URLSearchParams. */
function formEncode(s) {
  return encodeURIComponent(s).replace(/[!'()~]/g, (c) => '%' + c.charCodeAt(0).toString(16).toUpperCase()).replace(/%20/g, '+');
}

/** The forgiving decoding of URLSearchParams: `+` is a space, a `%` not followed by two hex
 *  digits stays as it is, and bytes that are not UTF-8 become U+FFFD. */
function formDecode(s) {
  const bytes = [];
  const t = s.replace(/\+/g, ' ');
  for (let i = 0; i < t.length; i += 1) {
    if (t[i] === '%' && /^[0-9A-Fa-f]{2}$/.test(t.slice(i + 1, i + 3))) {
      bytes.push(parseInt(t.slice(i + 1, i + 3), 16));
      i += 2;
    } else {
      const cp = t.codePointAt(i);
      const ch = String.fromCodePoint(cp);
      if (cp > 0xffff) i += 1;
      for (const b of Buffer.from(ch, 'utf8')) bytes.push(b);
    }
  }
  return Buffer.from(bytes).toString('utf8');
}

/** The canonical form of an http(s) URL, read with patterns: the n8n Code node has no `URL`
 *  global and no `url` module. tests/test_web_event_identity.js checks it against the WHATWG
 *  parser; what that parser would rewrite in ways a pattern cannot follow is refused rather
 *  than guessed: a host that is not plain ASCII, and a literal IP address. */
function canonicalUrl(raw) {
  if (typeof raw !== 'string' || raw.trim() === '') throw new Error('url_missing');
  // Unpaired surrogates become U+FFFD first, as the conversion of the argument to a string of
  // Unicode scalar values does before the standard's parser runs; then whitespace at both ends,
  // Unicode spaces included (the reading before this file did the same); then the standard
  // drops C0 controls and spaces at both ends, and tabs and line breaks anywhere.
  const input = raw.replace(LONE_SURROGATE, '\uFFFD').trim().replace(/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g, '').replace(/[\t\n\r]/g, '');
  const sm = /^([A-Za-z][A-Za-z0-9+.-]*):/.exec(input);
  if (!sm) throw new Error('url_invalid');
  let scheme = sm[1].toLowerCase();
  if (scheme !== 'http' && scheme !== 'https') throw new Error('url_not_http');
  // For http(s) the standard accepts any run of slashes or backslashes after the scheme, none
  // included: `https:esempio.it`, `https:/esempio.it` and `https:\\esempio.it` are one URL.
  const m = /^[A-Za-z][A-Za-z0-9+.-]*:[/\\]*([^/?#\\]*)([^?#]*)(?:\?([^#]*))?(?:#[\s\S]*)?$/.exec(input);
  if (!m) throw new Error('url_invalid');
  const hm = /^([^:@[\]]+)(?::(\d*))?$/.exec(m[1]);
  if (!hm) throw new Error('url_invalid');
  let host = hm[1].toLowerCase();
  // ASCII the standard keeps as it is in a host; `%`, which it would decode, is refused.
  if (!/^[a-z0-9.\-_~!$&'()*+,;=`{}"]+$/.test(host)) throw new Error('url_invalid');
  // A last label that is a number makes the host an IPv4 address to the WHATWG parser.
  const last = host.replace(/\.$/, '').split('.').pop();
  // An empty last label (the host ends in more than one dot) is not a number: the host stays a
  // domain, as the standard reads it.
  if (/^(\d+|0x[0-9a-f]*)$/.test(last)) throw new Error('url_invalid');
  let port = hm[2] === undefined || hm[2] === '' ? '' : String(Number(hm[2]));
  if (port !== '' && Number(port) > 65535) throw new Error('url_invalid');
  // The default port of the original scheme goes. An explicit port is part of the identity,
  // and http on 443 stays http: upgrading it would make the port vanish and merge two addresses.
  if ((scheme === 'http' && port === '80') || (scheme === 'https' && port === '443')) port = '';
  if (!(scheme === 'http' && port === '443')) scheme = 'https';
  host = host.replace(/^www\.(?=.)/, ''); // a host that is only `www.` keeps it, as the standard does
  const segments = [];
  for (const seg of m[2].replace(/\\/g, '/').split('/').slice(1)) {
    if (seg === '.' || seg.toLowerCase() === '%2e') continue;
    if (seg === '..' || /^(\.|%2e)(\.|%2e)$/i.test(seg)) { segments.pop(); continue; }
    segments.push([...seg].map((c) => (PATH_ENCODE.test(c) ? encodeURIComponent(c) : c)).join(''));
  }
  const path = ('/' + segments.join('/')).replace(/\/+$/, '') || '/';
  const kept = (m[3] === undefined ? [] : m[3].split('&'))
    .filter((pair) => pair !== '')
    .map((pair) => {
      const i = pair.indexOf('=');
      return i < 0 ? [formDecode(pair), ''] : [formDecode(pair.slice(0, i)), formDecode(pair.slice(i + 1))];
    })
    .filter(([k]) => !TRACKING_PARAM.test(k))
    .sort((a, b) => (a[0] === b[0] ? (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0) : a[0] < b[0] ? -1 : 1));
  const query = kept.map(([k, v]) => `${formEncode(k)}=${formEncode(v)}`).join('&');
  return `${scheme}://${host}${port ? ':' + port : ''}${path}${query ? '?' + query : ''}`;
}

const ISO_INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,3})?)?(?:Z|[+-](\d{2}):(\d{2}))$/;

/** An ISO instant that names a real day and time: `Date.parse` alone moves 30 February to
 *  2 March. */
function validInstant(v) {
  const m = typeof v === 'string' ? ISO_INSTANT.exec(v) : null;
  if (!m) return false;
  const [y, mo, d, h, mi, s] = [m[1], m[2], m[3], m[4], m[5], m[6] || '0'].map(Number);
  const day = new Date(Date.UTC(y, mo - 1, d));
  const sameDay = day.getUTCFullYear() === y && day.getUTCMonth() === mo - 1 && day.getUTCDate() === d;
  const offOk = m[7] === undefined || (Number(m[7]) <= 23 && Number(m[8]) <= 59);
  return sameDay && h <= 23 && mi <= 59 && s <= 59 && offOk;
}

/* ----- the tables of this step ------------------------------------------ */

/** The channel of each source read, as `SOURCES` of news-collect.js gives it; the tests keep
 *  the two equal. The channel always comes from the source the record was read in. */
const SOURCE_CHANNELS = Object.freeze({
  'questure.poliziadistato.it': 'news_official',
  'carabinieri.it': 'news_official',
  'abitarearoma.it': 'news_press',
  'cdn.ilfaroonline.it': 'news_press',
});

/** The values of `tipo`: the list of tools/cronaca-prova/ISTRUZIONI_CHIUSE.md. */
const TIPI = ['arresto', 'rapina', 'furto', 'aggressione', 'droga', 'truffa', 'incidente', 'incendio', 'soccorso',
  'morte', 'controlli', 'sgombero', 'sequestro', 'altro'];
const AMBITI = ['cronaca', 'non_cronaca'];
const LIVELLI = ['via', 'luogo', 'quartiere', 'altro'];
const GENERI = ['eta', 'persone', 'oggetto', 'mezzo'];
const AGGIORNAMENTI = ['convalida', 'scarcerazione', 'processo', 'sentenza', 'indagini', 'altro'];
const SCHEDA_KEYS = ['ambito', 'tipo', 'data_fatto', 'luoghi', 'dettagli', 'case_status', 'persone', 'fa_nomi',
  'aggiornamento', 'sintesi'];

const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

/* ----- days of Rome -------------------------------------------------------- */

const ROME_DAY = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' });

/** The day in Rome of a UTC instant, `YYYY-MM-DD` (section 5: dates are days of Rome). */
function romeDay(instant) {
  const parts = {};
  for (const p of ROME_DAY.formatToParts(new Date(Date.parse(instant)))) parts[p.type] = p.value;
  return `${parts.year}-${parts.month}-${parts.day}`;
}

const ISO_DAY = /^(\d{4})-(\d{2})-(\d{2})$/;

/** A `YYYY-MM-DD` that names a real day. */
function validDay(v) {
  const m = typeof v === 'string' ? ISO_DAY.exec(v) : null;
  if (!m) return false;
  const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const t = new Date(Date.UTC(y, mo - 1, d));
  return t.getUTCFullYear() === y && t.getUTCMonth() === mo - 1 && t.getUTCDate() === d;
}

/* ----- step 1: preparation -------------------------------------------------- */

const PAGE = /^originali\/notizie_(.+)_(\d{8}T\d{6}Z)_(\d+)\.(xml|html|json)$/;
const RIGHE = /^notizie_righe_(\d{8}T\d{6}Z)\.json$/;

/** Step 1 for one record (section 2, «I record»): channel from the source read, `source_id`
 *  from the URL of the record, the record id, the day of Rome. A record that does not read
 *  stops (`fermo`) with its motive, never guessed. Preparing a prepared record gives the same. */
function prepareRecord(record, inizio, index) {
  const base = { inizio, index };
  const unreadable = !record || typeof record !== 'object' || Array.isArray(record)
    || (record.stato === 'fermo' && record.motivo === 'record_illeggibile' && !has(record, 'url'));
  if (unreadable) return Object.assign(base, { stato: 'fermo', motivo: 'record_illeggibile' });
  const stop = (motivo, extra) => Object.assign({}, record, base, extra || {}, { stato: 'fermo', motivo });
  let recordId;
  try { recordId = canonicalUrl(record.url); } catch (e) { return stop('url_illeggibile'); }
  const page = typeof record.page === 'string' ? PAGE.exec(record.page) : null;
  if (!page) return stop('pagina_mancante', { record_id: recordId });
  // The page and the records file come from the same run (news-collect.js names both with its
  // start): a page of another run would put the record out of the reading order (section 5).
  if (page[2] !== inizio) return stop('pagina_di_altra_corsa', { record_id: recordId });
  const read = page[1];
  if (!has(SOURCE_CHANNELS, read)) return stop('fonte_sconosciuta', { record_id: recordId });
  const channel = SOURCE_CHANNELS[read];
  if (record.source_channel !== undefined && record.source_channel !== null && record.source_channel !== channel) {
    return stop('canale_diverso', { record_id: recordId });
  }
  const host = /^https?:\/\/([^/:?#]+)/.exec(recordId)[1];
  const related = host === read || host.endsWith('.' + read) || read.endsWith('.' + host);
  if (!host.includes('.') || !related) return stop('host_diverso', { record_id: recordId });
  let giorno;
  let fromRetrieved = false;
  if (record.published_at_utc !== null && record.published_at_utc !== undefined) {
    if (!validInstant(record.published_at_utc)) return stop('data_illeggibile', { record_id: recordId });
    giorno = romeDay(record.published_at_utc);
  } else if (validInstant(record.retrieved_at)) {
    giorno = romeDay(record.retrieved_at);
    fromRetrieved = true;
  } else {
    return stop('data_illeggibile', { record_id: recordId });
  }
  const out = Object.assign({}, record, base, { source_id: host, source_channel: channel, record_id: recordId, giorno,
    giorno_da_retrieved: fromRetrieved, stato: 'pronto' });
  delete out.motivo;
  delete out.primo;
  return out;
}

/** Step 1 for one file of records, `notizie_righe_<inizio>.json` (news-parse.js). */
function prepareFile({ name, records }) {
  const m = RIGHE.exec(name || '');
  if (!m) throw new Error(`not a records file: ${name}`);
  if (!Array.isArray(records)) throw new Error(`records missing: ${name}`);
  return records.map((r, i) => prepareRecord(r, m[1], i));
}

/** Step 1 for every file with pending work (section 2). A record whose id is already prepared
 *  earlier in the reading order (file `<inizio>`, then place in the file: section 5), the same
 *  page with its query written otherwise, stops (`record_ripetuto`, with the first one): one
 *  record id has one set of schede (section 3). The records come back in reading order,
 *  whatever the order of the list of files. */
function prepareFiles(files) {
  if (!Array.isArray(files)) throw new Error('files_missing');
  const prepared = files.flatMap(prepareFile);
  const before = (a, b) => a.inizio < b.inizio || (a.inizio === b.inizio && a.index < b.index);
  const first = new Map();
  for (const r of prepared) {
    if (r.stato !== 'pronto') continue;
    const seen = first.get(r.record_id);
    if (!seen || before(r, seen)) first.set(r.record_id, r);
  }
  return prepared.slice().sort((a, b) => (before(a, b) ? -1 : before(b, a) ? 1 : 0)).map((r) => {
    if (r.stato !== 'pronto') return r;
    const seen = first.get(r.record_id);
    if (seen === r) return r;
    return Object.assign({}, r, { stato: 'fermo', motivo: 'record_ripetuto', primo: { inizio: seen.inizio, index: seen.index } });
  });
}

/* ----- step 2: the check of the schede ------------------------------------ */

const plainObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const shortText = (v, max) => typeof v === 'string' && v.trim() !== '' && v.length <= max && !/[\r\n]/.test(v);
/** Text compared as section 3 says: no case, accents, punctuation or repeated spaces. */
function normKey(v) {
  return String(v).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
}

/** A text compared with others (a place, a detail): it must keep a letter or a digit once
 *  normalized, or two marks of punctuation would be «the same place». */
const comparable = (v, max) => shortText(v, max) && normKey(v) !== '';

/** A detail as the model writes it, or null when it is out of form (section 3, `dettagli`). */
function checkDetail(d) {
  if (!plainObject(d) || Object.keys(d).some((k) => k !== 'genere' && k !== 'valore')) return null;
  if (!GENERI.includes(d.genere)) return null;
  if (d.genere === 'eta') return Number.isSafeInteger(d.valore) && d.valore >= 0 && d.valore <= 130 ? { genere: 'eta', valore: d.valore } : null;
  if (d.genere === 'persone') return Number.isSafeInteger(d.valore) && d.valore >= 1 ? { genere: 'persone', valore: d.valore } : null;
  return comparable(d.valore, 80) ? { genere: d.genere, valore: d.valore.trim() } : null;
}

/** One scheda as the model writes it, or a motive when it is out of form. */
function checkOneScheda(s, record) {
  if (!plainObject(s)) return 'scheda_non_oggetto';
  const extra = Object.keys(s).find((k) => !SCHEDA_KEYS.includes(k));
  if (extra) return `campo_sconosciuto:${extra}`;
  if (!AMBITI.includes(s.ambito)) return 'ambito';
  if (s.fa_nomi !== true && s.fa_nomi !== false) return 'fa_nomi';
  if (!shortText(s.sintesi, 300)) return 'sintesi';
  const cronaca = s.ambito === 'cronaca';
  if (cronaca ? !TIPI.includes(s.tipo) : (s.tipo !== undefined && s.tipo !== null)) return 'tipo';
  const agg = s.aggiornamento === undefined || s.aggiornamento === null || s.aggiornamento === '' ? null : s.aggiornamento;
  if (agg !== null && (!cronaca || !AGGIORNAMENTI.includes(agg))) return 'aggiornamento';
  const df = s.data_fatto === undefined || s.data_fatto === null || s.data_fatto === '' ? null : s.data_fatto;
  // An impossible date: not a day, or a fact after the day of the record that tells it.
  if (df !== null && (!validDay(df) || df > record.giorno)) return 'data_fatto';
  const luoghi = s.luoghi === undefined || s.luoghi === null ? [] : s.luoghi;
  if (!Array.isArray(luoghi)) return 'luoghi';
  for (const l of luoghi) {
    if (!plainObject(l) || Object.keys(l).some((k) => k !== 'testo' && k !== 'livello')) return 'luoghi';
    if (!comparable(l.testo, 120) || !LIVELLI.includes(l.livello)) return 'luoghi';
  }
  const dettagli = s.dettagli === undefined || s.dettagli === null ? [] : s.dettagli;
  if (!Array.isArray(dettagli)) return 'dettagli';
  const checked = dettagli.map(checkDetail);
  if (checked.some((d) => d === null)) return 'dettagli';
  // The signals of DEC-034 point 5: `persone` is a flag (CRONACA_PROCESSO_2026-10.md, phase 2).
  // The values of `case_status` come with the prompt of B-R2 (section 9); until they are fixed
  // only an empty one passes, so no free text, and no name, enters a scheda.
  if (s.case_status !== undefined && s.case_status !== null) return 'case_status';
  const p = s.persone;
  if (p !== undefined && p !== null && typeof p !== 'boolean') return 'persone';
  return {
    ambito: s.ambito,
    tipo: cronaca ? s.tipo : null,
    data_fatto: df,
    luoghi: luoghi.map((l) => ({ testo: l.testo.trim(), livello: l.livello })),
    dettagli: checked,
    case_status: s.case_status === undefined ? null : s.case_status,
    persone: p === undefined ? null : p,
    fa_nomi: s.fa_nomi,
    aggiornamento: agg,
    sintesi: s.sintesi.trim(),
  };
}

/** Step 2, the code's part (section 4): the model's answer for one prepared record becomes its
 *  schede, each with its place `n` (`withRecord` adds the record's id), or
 *  `{ ok: false, motivo }` for an answer out of form, which is not saved (section 6). */
function checkSchede(risposta, record) {
  if (!record || record.stato !== 'pronto') throw new Error('record_not_prepared');
  if (!plainObject(risposta) || !Array.isArray(risposta.schede) || Object.keys(risposta).length !== 1) return { ok: false, motivo: 'forma' };
  if (risposta.schede.length === 0) return { ok: false, motivo: 'nessuna_scheda' };
  const schede = [];
  for (let i = 0; i < risposta.schede.length; i += 1) {
    const s = checkOneScheda(risposta.schede[i], record);
    if (typeof s === 'string') return { ok: false, motivo: `scheda_${i + 1}:${s}` };
    schede.push(Object.assign(s, { n: i + 1 }));
  }
  return { ok: true, schede };
}

/** A checked scheda with what the next steps read of its record. */
function withRecord(s, record, total) {
  return Object.assign({
    scheda_id: `${record.record_id}#${s.n}`,
    record_id: record.record_id,
    url: record.url,
    source_id: record.source_id,
    source_channel: record.source_channel,
    published_at_utc: record.published_at_utc || null,
    retrieved_at: record.retrieved_at || null,
    agency: record.agency === true,
    categories: Array.isArray(record.categories) ? record.categories : [],
    giorno: record.giorno,
    giorno_da_retrieved: record.giorno_da_retrieved,
    n_schede: total,
  }, s);
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { TRACKING_PARAM, PAGE, comparable, PATH_ENCODE, LONE_SURROGATE, formEncode, formDecode,
    canonicalUrl, ISO_INSTANT, validInstant, SOURCE_CHANNELS, TIPI, AMBITI, LIVELLI, GENERI, AGGIORNAMENTI, romeDay,
    validDay, prepareRecord, prepareFile, prepareFiles, checkSchede, withRecord, normKey };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. `stage` says which part runs;
 * an item that does not read fails, it is never given a guessed result. */
const stage = $json.stage;
if (stage === 'prepare') {
  $json.records = prepareFiles($json.files);
} else if (stage === 'check_schede') {
  const check = checkSchede($json.risposta, $json.record);
  $json.check = check.ok ? { ok: true, schede: check.schede.map((s) => withRecord(s, $json.record, check.schede.length)) } : check;
} else {
  throw new Error(`stage_unknown: ${stage}`);
}
return $input.item;

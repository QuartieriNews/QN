/**
 * news-group.js — workstream B: which records tell the same fact. This part carries steps 1 and
 * 3 of docs/pilota/B_RAGGRUPPAMENTO.md (preparation, candidates) and the check of the model's
 * answers of steps 2 and 4; step 5 and what the grouping adds to news-fact.js come with the last
 * part of B-R1 (section 9). The rules are in that document, sections 2, 3, 5 and 6, and in
 * docs/pilota/CONTRATTI.md, section 7 («B · Notizie»); this file does not restate them.
 * The model reads and proposes, this code decides (section 4).
 *
 * Three tables of this file are builder proposals that the document asks for without fixing
 * them (section 5): the families of `tipo` (FAMIGLIE), the cap of 10 candidates and the three
 * schede shown per candidate. Each has its test in tests/test_news_group.js.
 *
 * The identity code (canonical URL, content_id) and `validInstant` are copies of
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
  if (!record || typeof record !== 'object' || Array.isArray(record)) return Object.assign(base, { stato: 'fermo', motivo: 'record_illeggibile' });
  const stop = (motivo, extra) => Object.assign({}, record, base, extra || {}, { stato: 'fermo', motivo });
  let recordId;
  try { recordId = canonicalUrl(record.url); } catch (e) { return stop('url_illeggibile'); }
  const page = typeof record.page === 'string' ? PAGE.exec(record.page) : null;
  if (!page) return stop('pagina_mancante', { record_id: recordId });
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
  return out;
}

/** Step 1 for one file of records, `notizie_righe_<inizio>.json` (news-parse.js). */
function prepareFile({ name, records }) {
  const m = RIGHE.exec(name || '');
  if (!m) throw new Error(`not a records file: ${name}`);
  if (!Array.isArray(records)) throw new Error(`records missing: ${name}`);
  return records.map((r, i) => prepareRecord(r, m[1], i));
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
 *  schede, each with the record's id and its place `n`, or `{ ok: false, motivo }` for an
 *  answer out of form, which is not saved (section 6). */
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

/* ----- comparisons ---------------------------------------------------------- */

/** The families of `tipo` (builder proposal, B_RAGGRUPPAMENTO.md section 5, «Candidati»): two
 *  types are of the same family when one group holds both. The groups overlap, because an
 *  official release says «arresto» where the press names the offence. `altro` is only its own
 *  family: a fact the model could not type is never certain with a typed one. */
const FAMIGLIE = Object.freeze({
  patrimonio: ['furto', 'rapina', 'truffa', 'arresto'],
  persona: ['aggressione', 'rapina', 'morte', 'arresto'],
  droga: ['droga', 'sequestro', 'controlli', 'arresto'],
  strada: ['incidente', 'soccorso', 'morte'],
  fuoco: ['incendio', 'soccorso', 'morte'],
  ordine: ['sgombero', 'controlli', 'sequestro', 'arresto'],
});
const VERDETTI = ['stesso', 'forse', 'diverso'];

/** Candidate search: days around the fact (P-09), days between publications (section 5). */
const FINESTRA_FATTO = 3;
const FINESTRA_PUBBLICAZIONE = 7;
/** Builder proposals of section 5: candidates per scheda, schede shown per candidate. */
const MAX_CANDIDATI = 10;
const SCHEDE_MOSTRATE = 3;

/** A day as a number of days, for distances between days. */
function dayNumber(day) {
  const m = ISO_DAY.exec(day);
  return Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])) / 86400000;
}


function sameFamily(a, b) {
  if (!a || !b) return false;
  if (a === b) return true;
  return Object.values(FAMIGLIE).some((g) => g.includes(a) && g.includes(b));
}

/** The key of a detail: `oggetto` and `mezzo` are one kind (section 3). */
function detailKey(d) {
  const kind = d.genere === 'mezzo' ? 'oggetto' : d.genere;
  return `${kind}:${typeof d.valore === 'number' ? String(d.valore) : normKey(d.valore)}`;
}

/** The places of two schede that are the same, at the given levels: normalized texts. */
function sharedPlaces(a, b, livelli) {
  const keys = (s) => s.luoghi.filter((l) => livelli.includes(l.livello)).map((l) => normKey(l.testo)).filter((k) => k !== '');
  const mine = new Set(keys(a));
  return [...new Set(keys(b))].filter((k) => mine.has(k));
}

function sharedDetails(a, b) {
  const keys = (s) => s.dettagli.map(detailKey).filter((k) => !k.endsWith(':'));
  const mine = new Set(keys(a));
  return [...new Set(keys(b))].filter((k) => mine.has(k));
}

/** What the code can already compare (section 5): the same place at `via` or `luogo` counts
 *  one, each equal detail one. */
function sameThings(a, b) {
  return (sharedPlaces(a, b, ['via', 'luogo']).length ? 1 : 0) + sharedDetails(a, b).length;
}

/** The publication day of a scheda in the date search: none for an update (R-C08). */
const pubDay = (s) => (s.aggiornamento ? null : s.giorno);
const pubClean = (s) => !s.giorno_da_retrieved;
const within = (x, y, n) => Math.abs(dayNumber(x) - dayNumber(y)) <= n;

/** The date search of section 5 for one pair: `any` when the window holds, `clean` when it holds
 *  without a day taken from `retrieved_at`. */
function dateWindow(a, b) {
  if (a.data_fatto && b.data_fatto) {
    const ok = within(a.data_fatto, b.data_fatto, FINESTRA_FATTO);
    return { any: ok, clean: ok };
  }
  let any = false;
  let clean = false;
  const note = (ok, isClean) => { if (ok) { any = true; if (isClean) clean = true; } };
  const pa = pubDay(a);
  const pb = pubDay(b);
  if (pa && pb) note(within(pa, pb, FINESTRA_PUBBLICAZIONE), pubClean(a) && pubClean(b));
  if (a.data_fatto && pb) note(within(a.data_fatto, pb, FINESTRA_PUBBLICAZIONE), pubClean(b));
  if (b.data_fatto && pa) note(within(b.data_fatto, pa, FINESTRA_PUBBLICAZIONE), pubClean(a));
  return { any, clean };
}

/** «Le date a posto» of section 5, «Certa», for the incoming scheda `s` and the cited one `t`:
 *  the date window without days from `retrieved_at`, or an update without the day of its fact
 *  whose cited scheda comes before it. */
function datesInPlace(s, t) {
  if (dateWindow(s, t).clean) return true;
  if (!s.aggiornamento || s.data_fatto || s.giorno_da_retrieved) return false;
  if (t.data_fatto) return t.data_fatto <= s.giorno;
  if (t.aggiornamento || t.giorno_da_retrieved) return false;
  return t.giorno <= s.giorno;
}

/** The day of a scheda for «i più vicini per data»: the day of the fact, else its publication. */
const refDay = (s) => s.data_fatto || pubDay(s);

/* ----- step 3: candidates --------------------------------------------------- */

/* The identity of a fact: copies of news-identity.js, kept byte-equal by the tests. */
const crypto = require('crypto');

const sha256 = (text) => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

/** CONTRATTI.md section 7 (B): one fact, one id. `fact_index` is set only when one source
 *  record holds several facts, and then it is the fact's place in that record, from 1. */
function newsIdentity({ opening_url, fact_index }) {
  const key = sha256(canonicalUrl(opening_url)).slice(0, 16);
  let suffix = '';
  if (fact_index !== undefined && fact_index !== null) {
    if (!Number.isSafeInteger(fact_index) || fact_index < 1) throw new Error('fact_index_invalid');
    suffix = `-f${fact_index}`;
  }
  return {
    content_id: `qn:roma:nws:${key}${suffix}`,
    canonical_file_name: `roma__nws__${key}${suffix}.json`,
  };
}

/** The content_id of the fact a scheda opens: `-f<n>` when its record holds more than one
 *  scheda, fixed at the first division (CONTRATTI.md section 7 B, «Identità»). */
function factId(scheda) {
  return newsIdentity({ opening_url: scheda.url, fact_index: scheda.n_schede > 1 ? scheda.n : null }).content_id;
}

/** Whether a scheda looks among all the facts of the table (section 5, third way). */
function searchesAll(s) {
  return Boolean(s.aggiornamento) || (s.source_channel === 'news_official' && !s.data_fatto);
}

/** A fact without a date (section 5, third way): no scheda says the day of the fact, because
 *  it was opened by a release without it or an update that does not say it. A press scheda
 *  without the day of its fact has its day of publication, which the date search reads. */
function undatedFact(fact) {
  return fact.schede.every((t) => !t.data_fatto && (Boolean(t.aggiornamento) || t.source_channel === 'news_official'));
}

/** The day of the first record of a fact. */
function firstDay(fact) {
  return fact.schede.map((t) => t.giorno).sort()[0];
}

/** A fact without a date is «nel limite» of a scheda (section 5, «La lista tagliata»). */
function inLimit(s, fact) {
  const first = firstDay(fact);
  if (s.data_fatto) return s.data_fatto <= first;
  return dayNumber(s.giorno) - dayNumber(first) <= FINESTRA_PUBBLICAZIONE;
}

/** The schede of a candidate the model sees: the one that opened the fact and the two with more
 *  things equal, at equal count the first by `scheda_id`. */
function shownSchede(s, fact) {
  const opener = fact.schede.find((t) => t.ruolo === 'apre') || fact.schede[0];
  const others = fact.schede.filter((t) => t !== opener)
    .map((t) => ({ t, k: sameThings(s, t) }))
    .sort((x, y) => (y.k - x.k) || (x.t.scheda_id < y.t.scheda_id ? -1 : x.t.scheda_id > y.t.scheda_id ? 1 : 0))
    .slice(0, SCHEDE_MOSTRATE - 1)
    .map((x) => x.t);
  return [opener, ...others];
}

/** Step 3 (section 5, «Candidati» and «La lista tagliata»): for one scheda of cronaca, the facts
 *  it may be, at most MAX_CANDIDATI, each with the schede the model sees, and whether the cut
 *  list sends the scheda in doubt (`tagliata`). Facts holding a scheda of the same record are
 *  never candidates: the facts of one record are different facts (R-C01). */
function candidates(s, facts) {
  if (s.ambito !== 'cronaca') throw new Error('not_cronaca');
  const all = searchesAll(s);
  const found = [];
  for (const f of facts) {
    if (f.stato === 'unito') continue;
    if (f.schede.some((t) => t.record_id === s.record_id)) continue;
    const cron = f.schede.filter((t) => t.ambito === 'cronaca');
    const fam = cron.filter((t) => sameFamily(s.tipo, t.tipo));
    const byDate = fam.some((t) => dateWindow(s, t).any);
    const byPlace = fam.some((t) => sharedPlaces(s, t, ['via', 'luogo']).length > 0);
    const undated = undatedFact(f);
    const byUndated = undated && fam.length > 0;
    const byAll = s.aggiornamento ? cron.length > 0 : all && fam.length > 0;
    if (!(byDate || byPlace || byUndated || byAll)) continue;
    const pool = s.aggiornamento ? cron : fam;
    const best = Math.max(0, ...pool.map((t) => sameThings(s, t)));
    const maybeCertain = fam.some((t) => sharedPlaces(s, t, ['via', 'luogo']).length > 0 && datesInPlace(s, t));
    const mine = refDay(s);
    const dists = pool.map((t) => refDay(t)).filter((d) => d && mine).map((d) => Math.abs(dayNumber(d) - dayNumber(mine)));
    found.push({
      fact: f,
      maybeCertain,
      best,
      tier: byDate ? 0 : fam.length > 0 ? 1 : 2,
      dist: dists.length ? Math.min(...dists) : Infinity,
      undated,
      trovato: { data: byDate, luogo: byPlace, senza_data: byUndated, tutti: byAll },
    });
  }
  found.sort((a, b) => (Number(b.maybeCertain) - Number(a.maybeCertain)) || (b.best - a.best) || (a.tier - b.tier) ||
    (a.dist - b.dist) || (a.fact.content_id < b.fact.content_id ? -1 : a.fact.content_id > b.fact.content_id ? 1 : 0));
  const kept = found.slice(0, MAX_CANDIDATI);
  const left = found.slice(MAX_CANDIDATI);
  const tagliata = left.some((c) => all || (c.undated && inLimit(s, c.fact)));
  return {
    scheda_id: s.scheda_id,
    candidati: kept.map((c) => ({ content_id: c.fact.content_id, mostrate: shownSchede(s, c.fact), trovato: c.trovato })),
    esclusi: left.length,
    tagliata,
  };
}

/** The key of a list a judgment answers: the candidates and, of each, the schede shown. A saved
 *  judgment counts only for the same key (section 6). */
function listKey(lista) {
  return JSON.stringify(lista.candidati.map((c) => [c.content_id, c.mostrate.map((t) => t.scheda_id).sort()])
    .sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)));
}

/* ----- step 4: the check of a judgment ---------------------------------- */

/** Step 4, the code's part: the model's judgment for one list, `{ ok: true, giudizi }` keyed by
 *  content_id, or `{ ok: false, motivo }` for an answer out of form. Every candidate has one
 *  verdict, and `stesso` carries its proof: the cited scheda, the place, the details. */
function checkGiudizio(risposta, lista) {
  if (!plainObject(risposta) || !Array.isArray(risposta.giudizi) || Object.keys(risposta).length !== 1) return { ok: false, motivo: 'forma' };
  const want = new Set(lista.candidati.map((c) => c.content_id));
  const giudizi = {};
  for (const g of risposta.giudizi) {
    if (!plainObject(g) || !want.has(g.content_id) || has(giudizi, g.content_id)) return { ok: false, motivo: 'candidati' };
    if (Object.keys(g).some((k) => !['content_id', 'verdetto', 'prove'].includes(k))) return { ok: false, motivo: 'forma' };
    if (!VERDETTI.includes(g.verdetto)) return { ok: false, motivo: 'verdetto' };
    if (g.verdetto !== 'stesso') {
      if (g.prove !== undefined && g.prove !== null) return { ok: false, motivo: 'prove' };
      giudizi[g.content_id] = { verdetto: g.verdetto };
      continue;
    }
    const p = g.prove;
    if (!plainObject(p) || Object.keys(p).some((k) => !['scheda_id', 'luogo', 'dettagli'].includes(k))) return { ok: false, motivo: 'prove' };
    if (typeof p.scheda_id !== 'string') return { ok: false, motivo: 'prove' };
    if (p.luogo !== null && p.luogo !== undefined && !comparable(p.luogo, 120)) return { ok: false, motivo: 'prove' };
    const det = p.dettagli === undefined || p.dettagli === null ? [] : p.dettagli;
    if (!Array.isArray(det)) return { ok: false, motivo: 'prove' };
    const checked = det.map(checkDetail);
    if (checked.some((d) => d === null)) return { ok: false, motivo: 'prove' };
    giudizi[g.content_id] = { verdetto: 'stesso', prove: { scheda_id: p.scheda_id, luogo: p.luogo || null, dettagli: checked } };
  }
  if (Object.keys(giudizi).length !== want.size) return { ok: false, motivo: 'candidati' };
  return { ok: true, giudizi };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { TRACKING_PARAM, PAGE, comparable, PATH_ENCODE, LONE_SURROGATE, formEncode, formDecode,
    canonicalUrl, sha256, newsIdentity, ISO_INSTANT, validInstant, SOURCE_CHANNELS, TIPI, FAMIGLIE, AMBITI, LIVELLI,
    GENERI, AGGIORNAMENTI, VERDETTI, FINESTRA_FATTO, FINESTRA_PUBBLICAZIONE, MAX_CANDIDATI, SCHEDE_MOSTRATE, romeDay,
    validDay, undatedFact, inLimit, prepareRecord, prepareFile, checkSchede, withRecord, factId, normKey, sameFamily,
    detailKey, sharedPlaces, sharedDetails, sameThings, dateWindow, datesInPlace, candidates, listKey, checkGiudizio };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. `stage` says which part runs;
 * an item that does not read fails, it is never given a guessed result. */
const stage = $json.stage;
if (stage === 'prepare') {
  $json.records = ($json.files || []).flatMap(prepareFile);
} else if (stage === 'check_schede') {
  $json.check = checkSchede($json.risposta, $json.record);
} else if (stage === 'check_giudizio') {
  $json.check = checkGiudizio($json.risposta, $json.lista);
} else {
  throw new Error(`stage_unknown: ${stage}`);
}
return $input.item;

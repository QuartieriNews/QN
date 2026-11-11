/**
 * news-fact.js — workstream B: what the sources of one news fact allow. From the records
 * grouped in a fact it gives the category of the fact, whether it may be published, its
 * lead source (capofila), the publishers it counts and the sources the article cites
 * (`attribuzioni`). The rules are DEC-108, DEC-034 (R-C02) and
 * docs/sources/CRONACA_PROCESSO_2026-10.md, section 4.6; docs/pilota/CONTRATTI.md, section 7
 * («B · Notizie»), says how the channel applies them. This file does not restate them.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for Each
 * Item", JavaScript) the same file runs its per-item adapter.
 */
'use strict';

/** The values of `source_channel` for news (CONTRATTI.md section 7, B, «Colonne della coda»). */
const CHANNELS = ['news_official', 'news_press', 'news_index'];
/** The categories of a fact (CONTRATTI.md section 7, B, «Pubblicabile»), and the ones that
 *  may be published. */
const CATEGORIES = ['ufficiale', 'stampa_due_fonti', 'stampa_una_fonte', 'chiuse_due_fonti', 'chiuse_una_fonte'];
const PUBLISHABLE = ['ufficiale', 'stampa_due_fonti'];

/** The publisher of an outlet, by host without `www.` (a subdomain takes its domain's): two
 *  outlets of one group count once. An outlet that is not listed is its own publisher. */
const PUBLISHERS = {
  'romatoday.it': 'Citynews', 'today.it': 'Citynews',
  'ilmessaggero.it': 'Caltagirone', 'leggo.it': 'Caltagirone',
  'ilgiornale.it': 'Angelucci', 'iltempo.it': 'Angelucci',
  'corriere.it': 'RCS', 'repubblica.it': 'GEDI', 'ilfattoquotidiano.it': 'SEIF', 'fanpage.it': 'Ciaopeople',
  'rainews.it': 'RAI', 'tg24.sky.it': 'Sky', 'affaritaliani.it': 'Affaritaliani', 'romait.it': 'RomaIT',
  'ansa.it': 'ANSA', 'adnkronos.com': 'Adnkronos', 'agenzianova.com': 'Agenzia Nova', 'lapresse.it': 'LaPresse',
  'dire.it': 'Dire', 'askanews.it': 'Askanews', 'agi.it': 'AGI', 'italpress.com': 'Italpress',
  'abitarearoma.it': 'Abitare a Roma', 'ilfaroonline.it': 'Il Faro Online', 'romadailynews.it': 'Roma Daily News',
  'vignaclarablog.it': 'VignaClaraBlog',
};

/** The categories that mark an agency dispatch: the same pattern as `AGENCY` in news-parse.js,
 *  which tests/test_news_fact.js keeps equal. A dispatch counts as its agency, wherever it is
 *  published (R-C02: the same dispatch on several sites is one source). */
const AGENCY = /^(adnkronos|ansa|italpress|agenzia dire|dire|askanews|agi|agenzia nova|lapresse)$/i;
/** The publisher of each agency, the same name as in PUBLISHERS. */
const AGENCY_PUBLISHER = {
  adnkronos: 'Adnkronos', ansa: 'ANSA', italpress: 'Italpress', 'agenzia dire': 'Dire', dire: 'Dire',
  askanews: 'Askanews', agi: 'AGI', 'agenzia nova': 'Agenzia Nova', lapresse: 'LaPresse',
};

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

/** A host as the key of PUBLISHERS: lower case, without `www.`. */
function hostKey(sourceId) {
  return String(sourceId).trim().toLowerCase().replace(/^www\./, '');
}

/** The publisher of an outlet: its host, then each parent domain down to two labels. */
function outletPublisher(sourceId) {
  const labels = hostKey(sourceId).split('.');
  for (let i = 0; i + 2 <= labels.length; i += 1) {
    const domain = labels.slice(i).join('.');
    if (Object.prototype.hasOwnProperty.call(PUBLISHERS, domain)) return PUBLISHERS[domain];
  }
  return hostKey(sourceId);
}

/** The publisher a press record counts as: its agency for a dispatch, otherwise its outlet's.
 *  An official record is not a publisher (null). */
function publisherOf(record) {
  if (record.source_channel === 'news_official') return null;
  if (record.agency) {
    const cat = (record.categories || []).find((c) => typeof c === 'string' && AGENCY.test(c.trim()));
    if (cat) return AGENCY_PUBLISHER[cat.trim().toLowerCase()];
  }
  return outletPublisher(record.source_id);
}

/** A record as this step reads it; anything else stops the fact, it is never guessed. */
function checkRecord(r, i) {
  if (!r || typeof r !== 'object') throw new Error(`record_invalid: ${i}`);
  if (typeof r.source_id !== 'string' || r.source_id.trim() === '') throw new Error(`record_invalid: ${i} source_id`);
  if (typeof r.url !== 'string' || !/^https?:\/\/[^/?#\s]+/i.test(r.url.trim())) throw new Error(`record_invalid: ${i} url`);
  if (!CHANNELS.includes(r.source_channel)) throw new Error(`record_invalid: ${i} source_channel`);
  const t = r.published_at_utc;
  if (t !== null && t !== undefined && !validInstant(t)) {
    throw new Error(`record_invalid: ${i} published_at_utc`);
  }
}

/** The records in the order of publication: the ones without a time after the others, and
 *  equal times in the order they came. */
function chronological(records) {
  return records
    .map((r, i) => ({ r, i, t: r.published_at_utc ? Date.parse(r.published_at_utc) : Infinity }))
    .sort((a, b) => (a.t - b.t) || (a.i - b.i))
    .map((x) => x.r);
}

/** What the sources of one fact allow: `records` are the records grouped in it. */
function factSources(records) {
  if (!Array.isArray(records) || records.length === 0) throw new Error('records_missing');
  records.forEach(checkRecord);
  const ordered = chronological(records);
  const publishers = [...new Set(ordered.map(publisherOf).filter((p) => p !== null))].sort();
  const official = ordered.filter((r) => r.source_channel === 'news_official');
  const open = ordered.filter((r) => r.source_channel === 'news_press');
  let categoria;
  if (official.length) categoria = 'ufficiale';
  else if (open.length) categoria = publishers.length >= 2 ? 'stampa_due_fonti' : 'stampa_una_fonte';
  else categoria = publishers.length >= 2 ? 'chiuse_due_fonti' : 'chiuse_una_fonte';
  const lead = official[0] || open[0] || null;
  const seen = new Set();
  const attribuzioni = [];
  for (const r of ordered) {
    const key = hostKey(r.source_id);
    if (seen.has(key)) continue;
    seen.add(key);
    attribuzioni.push({ source_id: key, source_channel: r.source_channel, publisher: publisherOf(r), url: r.url.trim(),
      published_at_utc: r.published_at_utc || null });
  }
  return {
    categoria,
    pubblicabile: PUBLISHABLE.includes(categoria),
    editori: publishers,
    capofila: lead ? { source_id: hostKey(lead.source_id), source_channel: lead.source_channel, url: lead.url.trim() } : null,
    attribuzioni,
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { CHANNELS, CATEGORIES, PUBLISHABLE, PUBLISHERS, AGENCY, AGENCY_PUBLISHER, hostKey, outletPublisher,
    publisherOf, validInstant, chronological, factSources };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. Reads the records grouped in
 * one fact (`records`); an item whose records do not read fails, it is never given a guessed
 * category. */
const res = factSources($json.records);
$json.attribuzioni = res.attribuzioni;
$json.pubblicazione = { categoria: res.categoria, pubblicabile: res.pubblicabile, editori: res.editori, capofila: res.capofila };
return $input.item;

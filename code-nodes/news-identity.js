/**
 * news-identity.js — workstream B: the identity of a news fact (its content_id and
 * canonical file name), its source_hash and the source_id of the page it came from. The
 * rules are in docs/pilota/CONTRATTI.md, section 7 («B · Notizie»); this file does not
 * restate them. The URL is made canonical with the rules of web-event-identity.js, and
 * tests/test_news_identity.js checks that the two never part.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for Each
 * Item", JavaScript) the same file runs its per-item adapter. `crypto` is one of the
 * Node built-ins n8n Cloud exposes to the Code node.
 */
'use strict';
const crypto = require('crypto');

/** Query parameters that track a visit and never identify a page. */
const TRACKING_PARAM = /^(utm_[a-z0-9_]+|fbclid|gclid|dclid|msclkid|mc_cid|mc_eid|_ga|_gl)$/i;

function canonicalUrl(raw) {
  if (typeof raw !== 'string' || raw.trim() === '') throw new Error('url_missing');
  let u;
  try {
    u = new URL(raw.trim());
  } catch (e) {
    throw new Error('url_invalid');
  }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') throw new Error('url_not_http');
  // As in web-event-identity.js: an explicit port is part of the identity, and http on
  // 443 stays http so that the port does not vanish.
  if (!(u.protocol === 'http:' && u.port === '443')) u.protocol = 'https:';
  u.hostname = u.hostname.toLowerCase().replace(/^www\./, '');
  u.hash = '';
  u.pathname = u.pathname.replace(/\/+$/, '') || '/';
  const kept = [...u.searchParams.entries()]
    .filter(([k]) => !TRACKING_PARAM.test(k))
    .sort((a, b) => (a[0] === b[0] ? (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0) : a[0] < b[0] ? -1 : 1));
  u.search = '';
  for (const [k, v] of kept) u.searchParams.append(k, v);
  return u.toString();
}

/** A site's `source_id` is its host, lowercase, without `www.` (CONTRATTI.md, section 2). */
function sourceIdFromUrl(raw) {
  return new URL(canonicalUrl(raw)).hostname;
}

const sha256 = (text) => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

/** CONTRATTI.md section 7 (B): one fact, one id. `fact_index` is set only when one source
 *  record holds several facts, and then it is the fact's place in that record (1 to 99). */
function newsIdentity({ opening_url, fact_index }) {
  const key = sha256(canonicalUrl(opening_url)).slice(0, 16);
  let suffix = '';
  if (fact_index !== undefined && fact_index !== null) {
    if (!Number.isInteger(fact_index) || fact_index < 1 || fact_index > 99) throw new Error('fact_index_invalid');
    suffix = `-f${fact_index}`;
  }
  return {
    content_id: `qn:roma:nws:${key}${suffix}`,
    canonical_file_name: `roma__nws__${key}${suffix}.json`,
  };
}

/** NFC, trimmed, inner whitespace collapsed; absent is the empty string. */
function normalizeText(v) {
  if (v === undefined || v === null) return '';
  if (typeof v !== 'string') throw new Error('text_not_string');
  return v.normalize('NFC').trim().replace(/\s+/g, ' ');
}

const ISO_INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(Z|[+-](\d{2}):?(\d{2}))$/;
const ISO_DAY = /^(\d{4})-(\d{2})-(\d{2})$/;

function validDay(y, mo, d) {
  const t = new Date(Date.UTC(y, mo - 1, d));
  return t.getUTCFullYear() === y && t.getUTCMonth() === mo - 1 && t.getUTCDate() === d;
}

/** The publication time as one string: a UTC instant written with Z and milliseconds, or the
 *  day alone when the source gives no time (`date_precision: day`). An impossible date is
 *  refused, never repaired into another day. */
function normalizePublished(v) {
  if (typeof v !== 'string') throw new Error('published_invalid');
  let m = ISO_DAY.exec(v);
  if (m) {
    if (!validDay(Number(m[1]), Number(m[2]), Number(m[3]))) throw new Error('published_invalid');
    return v;
  }
  m = ISO_INSTANT.exec(v);
  if (!m) throw new Error('published_invalid');
  const [y, mo, d, h, mi, s] = [m[1], m[2], m[3], m[4], m[5], m[6] || '0'].map(Number);
  const offOk = m[7] === 'Z' || (Number(m[8]) <= 23 && Number(m[9]) <= 59);
  if (!validDay(y, mo, d) || h > 23 || mi > 59 || s > 59 || !offOk) throw new Error('published_invalid');
  return new Date(Date.parse(v)).toISOString();
}

/** CONTRATTI.md section 7 (B): what the lead record of a fact says. It changes when the
 *  source changes; the content_id does not. */
function newsSourceHash({ title, text, published_at_utc, place }) {
  // A JSON array keeps the fields apart whatever characters they contain.
  return sha256(JSON.stringify([normalizeText(title), normalizeText(text), normalizePublished(published_at_utc),
    normalizeText(place)]));
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { TRACKING_PARAM, canonicalUrl, sourceIdFromUrl, newsIdentity, normalizeText, normalizePublished,
    newsSourceHash };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. Reads the URL of the
 * record that opened the fact, its fact index and the lead record (`lead`: title, text,
 * published_at_utc, place); an item without a usable identity fails, it is never given a
 * guessed one. */
const id = newsIdentity({ opening_url: $json.opening_url, fact_index: $json.fact_index });
$json.content_id = id.content_id;
$json.canonical_file_name = id.canonical_file_name;
$json.source_id = sourceIdFromUrl($json.opening_url);
$json.source_hash = newsSourceHash($json.lead || {});
return $input.item;

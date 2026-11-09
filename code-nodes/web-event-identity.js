/**
 * web-event-identity.js — the identity of an event read from a web page: its
 * content_id, its canonical file name and whether the identity comes from a
 * listing page. The rules are in docs/pilota/CONTRATTI.md, section 7 (channel
 * "Eventi dalle pagine web"); this file does not restate them.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input`
 * is undefined, so the tail exports and stops; inside the n8n Code node ("Run
 * Once for Each Item", JavaScript) the same file runs its per-item adapter.
 * `crypto` is one of the Node built-ins n8n Cloud exposes to the Code node.
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
  // The URL parser already drops the default port of the original scheme, so a
  // port still present is explicit and part of the identity. http on 443 stays
  // http: upgrading it would make the port vanish and merge two addresses.
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

const ISO_INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(Z|[+-](\d{2}):?(\d{2}))$/;

/** Strict ISO 8601 instant with an offset: an impossible calendar date (30 February)
 *  is refused, never repaired into another day. */
function parseInstant(value) {
  const m = typeof value === 'string' ? ISO_INSTANT.exec(value) : null;
  if (!m) throw new Error('start_invalid');
  const [y, mo, d, h, mi, s] = [m[1], m[2], m[3], m[4], m[5], m[6] || '0'].map(Number);
  const leap = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const offOk = m[7] === 'Z' || (Number(m[8]) <= 23 && Number(m[9]) <= 59);
  if (mo < 1 || mo > 12 || d < 1 || d > days[mo - 1] || h > 23 || mi > 59 || s > 59 || !offOk) {
    throw new Error('start_invalid');
  }
  const ms = Date.parse(value);
  if (Number.isNaN(ms)) throw new Error('start_invalid');
  return new Date(ms);
}

/** The calendar day in Rome of a UTC instant (Spec v2.5 T17: UTC to Europe/Rome),
 *  built from the formatter's parts so no locale decides the order of the fields. */
function romeDate(startAtUtc) {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(parseInstant(startAtUtc));
  const get = (type) => parts.find((p) => p.type === type).value;
  return `${get('year')}-${get('month')}-${get('day')}`;
}

/** Unicode NFC, lower case, whitespace collapsed: one title, one string. */
function normalizeTitle(title) {
  if (typeof title !== 'string') throw new Error('title_missing');
  const t = title.normalize('NFC').toLowerCase().replace(/\s+/g, ' ').trim();
  if (t === '') throw new Error('title_missing');
  return t;
}

function sha16(text) {
  return crypto.createHash('sha256').update(text, 'utf8').digest('hex').slice(0, 16);
}

function webEventIdentity(ev) {
  const e = ev || {};
  let input;
  let fromListing;
  if (typeof e.detail_url === 'string' && e.detail_url.trim() !== '') {
    input = canonicalUrl(e.detail_url);
    fromListing = false;
  } else {
    // A JSON array keeps the three fields apart whatever characters they contain.
    input = JSON.stringify([canonicalUrl(e.listing_url), romeDate(e.start_at_utc), normalizeTitle(e.title)]);
    fromListing = true;
  }
  const key = sha16(input);
  return {
    content_id: `qn:roma:evt:web:${key}` + (e.is_series ? '-series' : ''),
    canonical_file_name: `roma__evt__web__${key}.json`,
    identity_from_listing: fromListing,
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { canonicalUrl, parseInstant, romeDate, normalizeTitle, webEventIdentity, TRACKING_PARAM };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. Reads the
 * extracted event (detail_url, listing_url, start_at_utc, event_name, is_series)
 * and writes the identity; an item without a usable identity fails, it is never
 * given a guessed one. */
const id = webEventIdentity({
  detail_url: $json.detail_url,
  listing_url: $json.listing_url,
  start_at_utc: $json.start_at_utc,
  title: $json.event_name,
  is_series: !!$json.is_series,
});
$json.content_id = id.content_id;
$json.canonical_file_name = id.canonical_file_name;
if (id.identity_from_listing) {
  const q = Object.assign({ review_flags: [] }, $json.quality);
  if (!q.review_flags.includes('identity_from_listing')) q.review_flags = q.review_flags.concat('identity_from_listing');
  $json.quality = q;
}
return $input.item;

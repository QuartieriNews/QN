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
  u.protocol = 'https:';
  u.hostname = u.hostname.toLowerCase().replace(/^www\./, '');
  if (u.port === '80' || u.port === '443') u.port = '';
  u.hash = '';
  u.pathname = u.pathname.replace(/\/+$/, '') || '/';
  const kept = [...u.searchParams.entries()]
    .filter(([k]) => !TRACKING_PARAM.test(k))
    .sort((a, b) => (a[0] === b[0] ? (a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0) : a[0] < b[0] ? -1 : 1));
  u.search = '';
  for (const [k, v] of kept) u.searchParams.append(k, v);
  return u.toString();
}

/** The calendar day in Rome of a UTC instant (Spec v2.5 T17: UTC to Europe/Rome). */
function romeDate(startAtUtc) {
  const ms = Date.parse(startAtUtc);
  if (typeof startAtUtc !== 'string' || !/(Z|[+-]\d\d:?\d\d)$/.test(startAtUtc) || Number.isNaN(ms)) {
    throw new Error('start_invalid');
  }
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(new Date(ms));
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
    input = `${canonicalUrl(e.listing_url)}|${romeDate(e.start_at_utc)}|${normalizeTitle(e.title)}`;
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
  module.exports = { canonicalUrl, romeDate, normalizeTitle, webEventIdentity, TRACKING_PARAM };
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

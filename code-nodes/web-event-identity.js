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
  // Whitespace at both ends goes first, Unicode spaces included (the reading before this file
  // did the same); then the standard drops C0 controls and spaces at both ends, and tabs and
  // line breaks anywhere.
  const input = raw.trim().replace(/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g, '').replace(/[\t\n\r]/g, '').replace(LONE_SURROGATE, '\uFFFD');
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
  if (last === '' || /^(\d+|0x[0-9a-f]*)$/.test(last)) throw new Error('url_invalid');
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

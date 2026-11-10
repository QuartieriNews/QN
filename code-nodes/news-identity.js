/**
 * news-identity.js — workstream B: the identity of a news fact (its content_id and
 * canonical file name), its source_hash and the source_id of the page it came from. The
 * rules are in docs/pilota/CONTRATTI.md, section 7 («B · Notizie»); this file does not
 * restate them. The URL is made canonical with the rules and the code of
 * web-event-identity.js, read with patterns because the n8n Code node has no `URL`
 * global; tests/test_news_identity.js checks that the two never part.
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

/** The characters the WHATWG parser percent-encodes in an http(s) path: C0 controls, space,
 *  `"`, `<`, `>`, `` ` ``, `{`, `}`, DEL and everything outside ASCII. Any other character,
 *  `%` included, is kept as it is. */
const PATH_ENCODE = /[\u0000- "<>`{}\u007f-\u{10ffff}]/u;

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
  const input = raw.trim().replace(/[\t\n\r]/g, '');
  const sm = /^([A-Za-z][A-Za-z0-9+.-]*):/.exec(input);
  if (!sm) throw new Error('url_invalid');
  let scheme = sm[1].toLowerCase();
  if (scheme !== 'http' && scheme !== 'https') throw new Error('url_not_http');
  const m = /^[A-Za-z][A-Za-z0-9+.-]*:\/\/([^/?#\\]*)([^?#]*)(?:\?([^#]*))?(?:#.*)?$/.exec(input);
  if (!m) throw new Error('url_invalid');
  const hm = /^([^:@[\]]+)(?::(\d*))?$/.exec(m[1]);
  if (!hm) throw new Error('url_invalid');
  let host = hm[1].toLowerCase();
  if (!/^[a-z0-9.-]+$/.test(host)) throw new Error('url_invalid');
  // A last label that is a number makes the host an IPv4 address to the WHATWG parser.
  const last = host.replace(/\.$/, '').split('.').pop();
  if (last === '' || /^(\d+|0x[0-9a-f]*)$/.test(last)) throw new Error('url_invalid');
  let port = hm[2] === undefined || hm[2] === '' ? '' : String(Number(hm[2]));
  if (port !== '' && Number(port) > 65535) throw new Error('url_invalid');
  // The default port of the original scheme goes. An explicit port is part of the identity,
  // and http on 443 stays http: upgrading it would make the port vanish and merge two addresses.
  if ((scheme === 'http' && port === '80') || (scheme === 'https' && port === '443')) port = '';
  if (!(scheme === 'http' && port === '443')) scheme = 'https';
  host = host.replace(/^www\./, '');
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

/** A site's `source_id` is its host, lowercase, without `www.` (CONTRATTI.md, section 2). */
function sourceIdFromUrl(raw) {
  return /^https?:\/\/([^/:?#]+)/.exec(canonicalUrl(raw))[1];
}

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

/** CONTRATTI.md section 7 (B): what the record that opened a fact says. It changes when the
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

/**
 * compute-source-hash.js — implements Spec v2.5, Phase 2.2 (acceptance cases
 * T20, T21) and the hashed-field count that Phase 1.3's tie-break reads. The
 * contract — the 14 fields, their order, the canonicalization rules — lives in
 * the spec; this file does not restate it. The spec requires exactly one Code
 * node for this, reused everywhere: this is that node.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md, pattern from
 * parse-duration.js): this exact file is both the Node module the tests
 * require() AND the full text pasted into the n8n Code node ("Run Once for
 * Each Item", JavaScript). Under plain Node `$input` is undefined, so the tail
 * exports and stops; inside n8n it runs the per-item adapter.
 *
 * `crypto` is a Node built-in and is one of the two modules n8n Cloud exposes
 * to the Code node (n8n docs, Code node → "Using external libraries"); no
 * NODE_FUNCTION_ALLOW_BUILTIN setting is needed there.
 */

'use strict';

const crypto = require('crypto');

/** Hash input fields, in the spec's order. Dotted names are paths into the
 *  Phase 1.3 internal source object. The order is the contract: changing it
 *  changes every stored hash, so it is a spec revision, never a tidy-up. */
const HASH_FIELDS = [
  'event_name',
  'source_description',
  'start_at_utc',
  'end_at_utc',
  'location.name',
  'location.address',
  'location.city',
  'location.country_code',
  'location.latitude',
  'location.longitude',
  'organizer.name',
  'source_image_url',
  'cost_raw',
  'booking_url_raw',
];

const TIMESTAMP_FIELDS = new Set(['start_at_utc', 'end_at_utc']);
const COORDINATE_FIELDS = new Set(['location.latitude', 'location.longitude']);
const URL_FIELDS = new Set(['source_image_url']);

function getPath(obj, dotted) {
  let cur = obj;
  for (const part of dotted.split('.')) {
    if (cur === null || cur === undefined || typeof cur !== 'object') return undefined;
    cur = cur[part];
  }
  return cur;
}

/** Spec string rule: NFC, trim, every whitespace run → one space. */
function canonicalString(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'object') return ''; // not a scalar: nothing stable to hash
  return String(value).normalize('NFC').trim().replace(/\s+/g, ' ');
}

/** Spec timestamp rule: UTC, second precision, "Z", no milliseconds.
 *  A value that does not parse as a date is canonicalized as a plain string
 *  rather than thrown on: the hash must stay deterministic for whatever the
 *  source sent, and Phase 1.4 has already refused unparseable starts. */
function canonicalTimestamp(value) {
  const s = canonicalString(value);
  if (s === '') return '';
  const ms = Date.parse(s);
  if (Number.isNaN(ms)) return s;
  return new Date(ms).toISOString().replace(/\.\d{3}Z$/, 'Z');
}

/** Spec number rule: fixed decimal, coordinates rounded to six places.
 *  Numeric strings are accepted (the scraper is not guaranteed to type them);
 *  anything non-finite is empty, like a missing value. */
function canonicalCoordinate(value) {
  if (typeof value !== 'number') {
    // String rule first: whatever canonicalizes to empty (null, whitespace, a
    // non-scalar) stays empty and never becomes the number 0 (cycle-1, item 2).
    const s = canonicalString(value);
    if (s === '') return '';
    value = Number(s);
  }
  const n = value;
  if (!Number.isFinite(n)) return '';
  const fixed = n.toFixed(6);
  return fixed === '-0.000000' ? '0.000000' : fixed;
}

/** Spec image-URL rule: origin + pathname, whole query string discarded (T21).
 *  A value that is not an absolute URL falls back to the string rule, so a
 *  malformed value still hashes deterministically instead of failing the item. */
function canonicalUrl(value) {
  const s = canonicalString(value);
  if (s === '') return '';
  try {
    const u = new URL(s);
    return u.origin + u.pathname;
  } catch (e) {
    return s;
  }
}

/** The hash-input representation of one field. */
function hashInputValue(field, value) {
  if (TIMESTAMP_FIELDS.has(field)) return canonicalTimestamp(value);
  if (COORDINATE_FIELDS.has(field)) return canonicalCoordinate(value);
  if (URL_FIELDS.has(field)) return canonicalUrl(value);
  return canonicalString(value);
}

/**
 * The ordered pair array the spec says to serialize — never an object.
 * @param {object} source - Phase 1.3 internal source object
 * @returns {Array<[string, string]>}
 */
function buildHashInput(source) {
  const src = source && typeof source === 'object' ? source : {};
  return HASH_FIELDS.map((f) => [f, hashInputValue(f, getPath(src, f))]);
}

/**
 * @param {object} source - Phase 1.3 internal source object
 * @returns {string} "sha256:<hex>"
 */
function computeSourceHash(source) {
  const serialized = JSON.stringify(buildHashInput(source));
  return 'sha256:' + crypto.createHash('sha256').update(serialized, 'utf8').digest('hex');
}

/** Phase 1.3 tie-break input: how many hashed fields are non-empty after
 *  canonicalization. Counted on the same representation as the hash, so a
 *  whitespace-only value counts as empty here too. */
function countNonEmptyHashedFields(source) {
  return buildHashInput(source).filter(([, v]) => v !== '').length;
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = {
    HASH_FIELDS, buildHashInput, computeSourceHash, countNonEmptyHashedFields, hashInputValue,
  };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter.
 * Reads the Phase 1.3 source object on the item and writes the hash where the
 * canonical contract keeps it (Part III, source.source_hash). Nothing else on
 * the item is touched; the registry comparison happens downstream (Phase 2.4). */
$json.source = Object.assign({}, $json.source, {
  source_hash: computeSourceHash($json),
});
return $input.item;

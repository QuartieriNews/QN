/**
 * dedupe-source-events.js — implements Spec v2.5, Phase 1.3 (acceptance case
 * T25): reject items without a valid source_event_id, deduplicate the full
 * dataset by normalized source_event_id before the batch loop, tie-break on
 * the count of non-empty hashed fields (Phase 2.2 list), then on the last
 * occurrence in dataset order. The contract lives in the spec; this file does
 * not restate it.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): this exact file is both the
 * Node module the tests require() AND the full text pasted into the n8n Code
 * node — here "Run Once for All Items", because the rule is a property of the
 * whole dataset, not of one item. Under plain Node `$input` is undefined, so
 * the tail exports and stops; inside n8n it runs the dataset adapter.
 *
 * The tie-break count comes from compute-source-hash.js so that "non-empty"
 * means the same thing here as in the hash. n8n's Code node cannot require a
 * sibling file, so the count function is inlined below and must stay
 * byte-equivalent in behaviour to countNonEmptyHashedFields() there; the test
 * suite checks the two agree on the same inputs.
 */

'use strict';

/* --- inlined from compute-source-hash.js (Phase 2.2): the hashed-field count --- */
const HASH_FIELDS = [
  'event_name', 'source_description', 'start_at_utc', 'end_at_utc',
  'location.name', 'location.address', 'location.city', 'location.country_code',
  'location.latitude', 'location.longitude', 'organizer.name', 'source_image_url',
  'cost_raw', 'booking_url_raw',
];
const COORDINATE_FIELDS = new Set(['location.latitude', 'location.longitude']);

function getPath(obj, dotted) {
  let cur = obj;
  for (const part of dotted.split('.')) {
    if (cur === null || cur === undefined || typeof cur !== 'object') return undefined;
    cur = cur[part];
  }
  return cur;
}

function isEmptyHashedValue(field, value) {
  if (value === null || value === undefined || value === '') return true;
  if (typeof value === 'object') return true;
  if (COORDINATE_FIELDS.has(field)) {
    // String rule first, as in canonicalCoordinate there: a value that trims to
    // empty stays empty and never becomes Number('') === 0 (PR #19, cycle 1).
    const n = typeof value === 'number' ? value
      : (String(value).trim() === '' ? NaN : Number(String(value).trim()));
    return !Number.isFinite(n);
  }
  return String(value).trim() === '';
}

function countNonEmptyHashedFields(source) {
  const src = source && typeof source === 'object' ? source : {};
  return HASH_FIELDS.filter((f) => !isEmptyHashedValue(f, getPath(src, f))).length;
}
/* --- end inlined section --- */

/** Normalized source_event_id, or null when the value is not a valid id.
 *  What "valid" means is decisions/DEC-027. */
function normalizeSourceEventId(value) {
  if (typeof value === 'string') {
    const s = value.trim();
    return s === '' ? null : s;
  }
  if (Number.isSafeInteger(value)) return String(value);
  return null;
}

/**
 * @param {object[]} items - Phase 1.3 internal source objects, in dataset order
 * @returns {{items: object[], report: {returned_by_source: number,
 *   rejected_missing_source_event_id: number, duplicate_source_ids_removed: number,
 *   kept: number}}}
 * Kept items are returned in order of first appearance of their id; for a
 * duplicated id the kept payload is the most complete one, last occurrence on a tie.
 */
function dedupeSourceEvents(items) {
  const list = Array.isArray(items) ? items : [];
  const byId = new Map();
  let rejected = 0;
  let duplicates = 0;
  for (const item of list) {
    const id = normalizeSourceEventId(item && item.source_event_id);
    if (id === null) {
      rejected += 1;
      continue;
    }
    const score = countNonEmptyHashedFields(item);
    const prev = byId.get(id);
    if (!prev) {
      byId.set(id, { item, score });
      continue;
    }
    duplicates += 1;
    if (score >= prev.score) {
      byId.set(id, { item, score }); // later occurrence wins a tie (spec: "keep the last")
    }
  }
  const kept = Array.from(byId.values()).map((e) => e.item);
  return {
    items: kept,
    report: {
      returned_by_source: list.length,
      rejected_missing_source_event_id: rejected,
      duplicate_source_ids_removed: duplicates,
      kept: kept.length,
    },
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { dedupeSourceEvents, normalizeSourceEventId, countNonEmptyHashedFields };
  return;
}

/* n8n Code node, "Run Once for All Items" — the dataset adapter.
 * Emits only the deduplicated items, so nothing downstream can see a
 * duplicate. The counts are logged here; the run report (Phase 5) reads
 * duplicate_source_ids_removed from the node's output difference or from this
 * log line — wiring that is a Phase 5 task, not this node's. */
const result = dedupeSourceEvents($input.all().map((it) => it.json));
console.log('dedupe-source-events ' + JSON.stringify(result.report));
return result.items.map((json) => ({ json }));

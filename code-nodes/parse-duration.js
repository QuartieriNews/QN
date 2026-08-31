/**
 * parse-duration.js — implements Spec v2.5, Phase 3.3 (acceptance case T39).
 * The contract lives there; this file does not restate it.
 *
 * ONE SOURCE, TWO CONTEXTS (cycle-1 review, item 4): this exact file is both
 * the Node module the tests require() AND the full text pasted into the n8n
 * Code node ("Run Once for Each Item", JavaScript). The tail detects the
 * context: under plain Node, `$input` is undefined, so it exports and stops
 * (top-level `return` is legal in CommonJS — the module wrapper is a
 * function, same as n8n's). Inside n8n it runs the per-item adapter instead.
 * Byte identity between repo and node is therefore checkable with `cmp`.
 */

'use strict';

/** Minutes per accepted unit token. Integers only, by design. */
const UNIT_MINUTES = {
  day: 1440, days: 1440,
  hr: 60, hrs: 60, hour: 60, hours: 60,
  min: 1, mins: 1, minute: 1, minutes: 1,
};

/** One number+unit pair, e.g. "5 days", "45min". Longer alternatives first:
 *  "minutes?" before "mins?", otherwise "mins?" consumes the "min" of
 *  "minutes" and the leftover "utes" voids the parse. Sticky flag: each
 *  match must start exactly where the previous token ended. */
const PAIR_RE = /(\d+)\s*(days?|hours?|hrs?|minutes?|mins?)/giy;

/**
 * Parse the raw `duration` field.
 * @param {*} durationText - raw source value (string, null, undefined, …)
 * @returns {{status: 'parsed'|'missing'|'unparseable', minutes: number|null}}
 * Strict whole-input rule: the entire string must be number+unit pairs
 * separated by whitespace. No partial credit — "1.5 hrs" must not half-match
 * as "5 hrs", leftover text voids the parse.
 */
function parseDurationText(durationText) {
  if (durationText === null || durationText === undefined) {
    return { status: 'missing', minutes: null };
  }
  if (typeof durationText !== 'string') {
    return { status: 'unparseable', minutes: null };
  }
  const text = durationText.trim();
  if (text === '') {
    return { status: 'missing', minutes: null };
  }

  let total = 0;
  let pairs = 0;
  let pos = 0;
  const lower = text.toLowerCase();
  while (pos < lower.length) {
    const ws = /\s+/y;
    ws.lastIndex = pos;
    if (ws.exec(lower)) pos = ws.lastIndex;
    if (pos >= lower.length) break;

    PAIR_RE.lastIndex = pos;
    const m = PAIR_RE.exec(lower);
    if (!m || m.index !== pos) {
      return { status: 'unparseable', minutes: null };
    }
    // Bound untrusted numbers by VALUE (cycle-2 item 2, narrowed by cycle-3):
    // what cannot be summed exactly is unparseable. Digit width was the wrong
    // proxy — it rejected zero-padded numbers that are perfectly in range.
    const value = Number(m[1]);
    if (!Number.isSafeInteger(value)) {
      return { status: 'unparseable', minutes: null };
    }
    const unit = m[2];
    if (!(unit in UNIT_MINUTES)) {
      return { status: 'unparseable', minutes: null }; // defensive; regex prevents this
    }
    total += value * UNIT_MINUTES[unit];
    pairs += 1;
    pos = PAIR_RE.lastIndex;
  }

  if (pairs === 0) {
    return { status: 'unparseable', minutes: null };
  }
  return { status: 'parsed', minutes: total };
}

/**
 * Compute the event-end fields of the canonical contract (Phase 3.3).
 * @param {string} startAtUtc - ISO 8601 UTC start, validated upstream;
 *   garbage is still refused, as 'invalid_start_timestamp' — a Phase 5.1
 *   hard-error condition, deliberately distinct from 'date_unparseable'.
 * @param {*} durationText - raw source `duration` field.
 * All arithmetic is UTC epoch milliseconds; DST cannot affect it.
 */
function computeEventEnd(startAtUtc, durationText) {
  const startMs = Date.parse(startAtUtc);
  if (typeof startAtUtc !== 'string' || Number.isNaN(startMs)) {
    return {
      ok: false, end_at_utc: null, date_precision: null,
      reject_reason: null, duration_minutes: null,
      error: 'invalid_start_timestamp',
    };
  }

  const parsed = parseDurationText(durationText);

  if (parsed.status === 'missing') {
    return {
      ok: true,
      end_at_utc: new Date(startMs).toISOString(),
      date_precision: 'start_only',
      reject_reason: null,
      duration_minutes: null,
      error: null,
    };
  }

  if (parsed.status === 'unparseable') {
    return {
      ok: true, // the item continues; the reject routes it to the review queue
      end_at_utc: new Date(startMs).toISOString(),
      date_precision: 'start_only',
      reject_reason: 'date_unparseable',
      duration_minutes: null,
      error: null,
    };
  }

  const end = new Date(startMs + parsed.minutes * 60000);
  if (Number.isNaN(end.getTime())) {
    // Summed pairs can still exceed the valid Date range; an untrusted value
    // must yield a structured item, never a thrown RangeError (cycle-2, item 2).
    return {
      ok: true,
      end_at_utc: new Date(startMs).toISOString(),
      date_precision: 'start_only',
      reject_reason: 'date_unparseable',
      duration_minutes: null,
      error: null,
    };
  }

  return {
    ok: true,
    end_at_utc: end.toISOString(),
    date_precision: 'exact',
    reject_reason: null,
    duration_minutes: parsed.minutes,
    error: null,
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { parseDurationText, computeEventEnd, UNIT_MINUTES };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter. */
const r = computeEventEnd($json.start_at_utc, $json.duration_raw);
if (!r.ok) {
  // hard error path (Phase 5.1): invalid start must fail the item, not pass silently
  throw new Error(r.error);
}
$json.event = Object.assign({}, $json.event, {
  end_at_utc: r.end_at_utc,
  date_precision: r.date_precision,
});
// duration_minutes stays internal to the module API: it is not a field of the
// schema-2.0 event object (Part III), so the adapter must not emit it (cycle-2,
// item 1). Adding it to the contract would be a spec revision, not a side effect.
if (r.reject_reason) {
  $json.quality = Object.assign({}, $json.quality, {
    reject_reason: r.reject_reason, // 'date_unparseable' — counted, queued, never deleted
  });
}
return $input.item;

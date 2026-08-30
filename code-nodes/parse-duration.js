/**
 * parse-duration.js — Phase 3.3 of the specification (v2.5).
 *
 * Parses the Facebook `duration` free-text field and computes the event end.
 *
 * Normative behaviour (spec v2.5, Phase 3.3; acceptance case T39):
 *   - duration parseable  -> end_at_utc = start + duration, date_precision "exact"
 *   - duration missing    -> end_at_utc = start,            date_precision "start_only",
 *                            NO reject (missing is normal: 42% of measured records)
 *   - duration present but unparseable -> reject_reason "date_unparseable"
 *     (a real signal that the parser needs extending; it is counted)
 *
 * Observed shapes (SOURCE_DATA_FINDINGS): "5 days", "1 hr 30 min", "2 hrs",
 * "45 min", "1 day". The spec mandates a strict sum of number+unit pairs and
 * forbids natural-language cleverness. Strictness here is deliberate:
 * "1.5 hrs" must NOT partially match as "5 hrs" — any text that is not
 * entirely number+unit pairs is unparseable.
 *
 * All arithmetic is in UTC epoch milliseconds; DST cannot affect it. Display
 * times in Europe/Rome are derived elsewhere (Phase 3.3, first bullet).
 *
 * Plain module, no dependencies: runnable in an n8n Code node and in
 * `node tests/test_parse_duration.js`.
 */

'use strict';

/** Minutes per accepted unit. Only the shapes the source actually produces. */
const UNIT_MINUTES = {
  day: 1440, days: 1440,
  hr: 60, hrs: 60, hour: 60, hours: 60,
  min: 1, mins: 1, minute: 1, minutes: 1,
};

/** One number+unit pair, e.g. "5 days", "45min". Integers only, by design.
 *  Longer alternatives first: "minutes?" before "mins?", otherwise "mins?"
 *  consumes the "min" of "minutes" and the leftover "utes" voids the parse. */
const PAIR_RE = /(\d+)\s*(days?|hours?|hrs?|minutes?|mins?)/giy;

/**
 * Parse the raw `duration` field.
 *
 * @param {*} durationText - the raw source value (string, null, undefined, …)
 * @returns {{status: 'parsed'|'missing'|'unparseable', minutes: number|null}}
 *   status 'missing'     for null/undefined/empty/whitespace-only input;
 *   status 'parsed'      with total minutes when the WHOLE string is
 *                        number+unit pairs separated by whitespace;
 *   status 'unparseable' for anything else (decimals, foreign words,
 *                        leftover text, bare numbers, bare units).
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

  // Tokenize strictly: from left to right, consume number+unit pairs and the
  // whitespace between them. Anything left over makes the whole string
  // unparseable — no partial credit, per the spec's "do not be clever".
  let total = 0;
  let pairs = 0;
  let pos = 0;
  const lower = text.toLowerCase();
  while (pos < lower.length) {
    // skip inter-pair whitespace
    const ws = /\s+/y;
    ws.lastIndex = pos;
    const wsMatch = ws.exec(lower);
    if (wsMatch) pos = ws.lastIndex;
    if (pos >= lower.length) break;

    PAIR_RE.lastIndex = pos;
    const m = PAIR_RE.exec(lower);
    if (!m || m.index !== pos) {
      return { status: 'unparseable', minutes: null };
    }
    const unit = m[2];
    if (!(unit in UNIT_MINUTES)) {
      return { status: 'unparseable', minutes: null }; // defensive; regex should prevent this
    }
    total += parseInt(m[1], 10) * UNIT_MINUTES[unit];
    pairs += 1;
    pos = PAIR_RE.lastIndex;
  }

  if (pairs === 0) {
    return { status: 'unparseable', minutes: null };
  }
  return { status: 'parsed', minutes: total };
}

/**
 * Compute the event-end fields for the canonical contract.
 *
 * @param {string} startAtUtc - ISO 8601 UTC start (e.g. "2026-09-25T18:00:00Z"),
 *   already validated upstream; this function still refuses garbage defensively.
 * @param {*} durationText - the raw source `duration` field.
 * @returns {{
 *   ok: boolean,
 *   end_at_utc: string|null,
 *   date_precision: 'exact'|'start_only'|null,
 *   reject_reason: string|null,
 *   duration_minutes: number|null,
 *   error: string|null
 * }}
 *   ok:false with error 'invalid_start_timestamp' when the start does not
 *   parse — that is a Phase 5.1 hard-error condition, not date_unparseable,
 *   and the two must stay distinct in the counters.
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

  return {
    ok: true,
    end_at_utc: new Date(startMs + parsed.minutes * 60000).toISOString(),
    date_precision: 'exact',
    reject_reason: null,
    duration_minutes: parsed.minutes,
    error: null,
  };
}

module.exports = { parseDurationText, computeEventEnd, UNIT_MINUTES };

/* ---------------------------------------------------------------------------
 * n8n Code node usage (JavaScript, "Run Once for Each Item"):
 *
 *   const { computeEventEnd } = ... // paste the two functions above the loop,
 *                                   // byte-identical to this file (README rule)
 *   const r = computeEventEnd($json.start_at_utc, $json.duration_raw);
 *   if (!r.ok) throw new Error(r.error);            // hard error path, Phase 5.1
 *   $json.event = Object.assign({}, $json.event, {
 *     end_at_utc: r.end_at_utc,
 *     date_precision: r.date_precision,
 *   });
 *   if (r.reject_reason) $json.quality = Object.assign({}, $json.quality, {
 *     reject_reason: r.reject_reason,               // 'date_unparseable', counted
 *   });
 *   return $json;
 * ------------------------------------------------------------------------- */

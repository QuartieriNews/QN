/**
 * institutional-identity.js — workstream A: the reference and file name of a recording, the
 * identity of a fact read in it (its content_id and file name), the queue columns
 * source_channel and source_id, and the source_hash. The rules are in docs/pilota/CONTRATTI.md,
 * section 7 («A · Amministrazione», rows Identità, File, `source_hash`, Colonne della coda,
 * Registrazione); the hash form is Spec v2.5 Phase 2.2, as in compute-source-hash.js. This
 * file does not restate them. Acceptance: tests/test_institutional_identity.js.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so
 * the tail exports and stops; inside the n8n Code node ("Run Once for Each Item", JavaScript)
 * the same file runs its per-item adapter. `crypto` is one of the Node built-ins n8n Cloud
 * exposes to the Code node; the file uses neither `process` nor `URL`, which it does not have.
 */
'use strict';
const crypto = require('crypto');

/** CONTRATTI section 7 (A), row Colonne della coda. */
const ROMATV_HOST = 'streaming.comune.roma.it';

const UUID = /^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$/;
const VIDEO_ID = /^[A-Za-z0-9_-]{11}$/;
const CHANNEL_ID = /^UC[A-Za-z0-9_-]{22}$/;
const CONTENT_ID = /^qn:roma:ins:([0-9a-f]{16})-f([1-9][0-9]*)$/;

const sha256 = (text) => crypto.createHash('sha256').update(text, 'utf8').digest('hex');

function platformOf(platform) {
  if (platform === 'romatv' || platform === 'youtube') return platform;
  throw new Error('platform_invalid');
}

/** CONTRATTI section 7 (A), row Identità: the recording reference (T-A1-03, T-A1-04). */
function recordingRef(platform, id) {
  if (platformOf(platform) === 'romatv') {
    if (typeof id !== 'string' || !UUID.test(id)) throw new Error('guid_invalid');
    return `romatv:${id.toLowerCase()}`;
  }
  if (typeof id !== 'string' || !VIDEO_ID.test(id)) throw new Error('video_id_invalid');
  return `youtube:${id}`;
}

/** A reference read back from a record or an item, in its canonical form. */
function canonicalRef(ref) {
  const m = typeof ref === 'string' ? /^(romatv|youtube):([\s\S]*)$/.exec(ref) : null;
  if (!m) throw new Error('ref_invalid');
  try {
    return recordingRef(m[1], m[2]);
  } catch (e) {
    throw new Error('ref_invalid');
  }
}

/** CONTRATTI section 7 (A), row Identità: the key of the recording a fact was first read in. */
function keyOf(ref) {
  return sha256(canonicalRef(ref)).slice(0, 16);
}

/** CONTRATTI section 7 (A), row Identità (T-A1-05, T-A1-06): two arguments and no more. */
function contentId(ref, n) {
  if (!Number.isSafeInteger(n) || n < 1) throw new Error('n_invalid');
  return `qn:roma:ins:${keyOf(ref)}-f${n}`;
}

/** CONTRATTI section 7 (A), row File. */
function fileName(id) {
  const m = typeof id === 'string' ? CONTENT_ID.exec(id) : null;
  if (!m || !Number.isSafeInteger(Number(m[2]))) throw new Error('content_id_invalid');
  return `roma__ins__${m[1]}-f${m[2]}.json`;
}

/** CONTRATTI section 7 (A), row Registrazione: the record's file in `registrazioni/`. */
function recordingFileName(ref) {
  return canonicalRef(ref).replace(':', '__') + '.json';
}

/** CONTRATTI section 7 (A), row Colonne della coda. */
function sourceChannel(platform) {
  return `inst_${platformOf(platform)}`;
}

/** CONTRATTI section 7 (A), row Colonne della coda (T-A1-07). */
function sourceId(platform, channelId) {
  if (platformOf(platform) === 'romatv') return ROMATV_HOST;
  if (typeof channelId !== 'string' || !CHANNEL_ID.test(channelId)) throw new Error('channel_id_invalid');
  return channelId;
}

const INSTANT = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(?:(Z)|([+-])(\d{2}):?(\d{2}))$/;

/** Spec v2.5 Phase 2.2, timestamps, as compute-source-hash.js (T-A1-08…T-A1-10). An instant
 *  without an offset is refused, never read in a guessed zone. */
function toUtcSecond(value) {
  const m = typeof value === 'string' ? INSTANT.exec(value) : null;
  if (!m) throw new Error('time_invalid');
  const [y, mo, d, h, mi] = [1, 2, 3, 4, 5].map((i) => Number(m[i]));
  const s = m[6] === undefined ? 0 : Number(m[6]);
  const [oh, om] = m[7] ? [0, 0] : [Number(m[9]), Number(m[10])];
  const t = new Date(0);
  t.setUTCFullYear(y, mo - 1, d); // not Date.UTC, which reads years below 100 as 19xx
  const dayOk = t.getUTCFullYear() === y && t.getUTCMonth() === mo - 1 && t.getUTCDate() === d;
  if (!dayOk || h > 23 || mi > 59 || s > 59 || oh > 23 || om > 59) throw new Error('time_invalid');
  t.setUTCHours(h, mi, s, 0);
  const utc = new Date(t.getTime() - (m[8] === '-' ? -1 : 1) * (oh * 60 + om) * 60000);
  return utc.toISOString().slice(0, 19) + 'Z';
}

const TIMESPAN = /^(\d{2}):([0-5]\d):([0-5]\d)(?:\.\d{1,7})?$/;

/** CONTRATTI section 7 (A), row `source_hash`: the duration in whole seconds (T-A1-11). It
 *  reads RomaTV's `hh:mm:ss.fffffff` and a plain number of seconds, number or digits. */
function durationSeconds(value) {
  let secs = NaN;
  if (typeof value === 'number') {
    secs = value >= 0 ? Math.floor(value) : NaN;
  } else if (typeof value === 'string') {
    const m = TIMESPAN.exec(value);
    if (m) secs = Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]);
    else if (/^\d+(?:\.\d+)?$/.test(value)) secs = Math.floor(Number(value));
  }
  if (!Number.isSafeInteger(secs)) throw new Error('duration_invalid');
  return secs + 0; // -0 from Math.floor(-0) is 0
}

/** Spec v2.5 Phase 2.2, strings, as compute-source-hash.js (T-A1-13, T-A1-14). */
function canonicalText(v) {
  if (v === undefined || v === null) return '';
  if (typeof v !== 'string') throw new Error('text_not_string');
  return v.normalize('NFC').trim().replace(/\s+/g, ' ');
}

/** CONTRATTI section 7 (A), row `source_hash`. The keys and their order enter every stored
 *  hash: changing either is a contract change, never a tidy-up (T-A1-12, T-A1-15). */
const HASH_FIELDS = ['recording_ref', 'title', 'reference_at', 'duration_s', 'transcript_source', 'transcript_sha256'];

const TRANSCRIPT_SOURCE = /^(platform_speech|platform_vtt|youtube_asr|asr:[a-z0-9][a-z0-9._-]*)$/;

/** The hash-input form of one field: the string rule first, then the field's own form. A
 *  present value that is not of its form is refused. The reference is always required. */
function hashValue(field, value) {
  if (field === 'duration_s' && typeof value === 'number') return String(durationSeconds(value));
  if (field === 'recording_ref') return canonicalRef(typeof value === 'string' ? canonicalText(value) : value);
  const s = canonicalText(value);
  if (s === '' || field === 'title') return s;
  if (field === 'reference_at') return toUtcSecond(s);
  if (field === 'duration_s') return String(durationSeconds(s));
  if (field === 'transcript_source') {
    if (!TRANSCRIPT_SOURCE.test(s)) throw new Error('transcript_source_invalid');
    return s;
  }
  if (!/^[0-9A-Fa-f]{64}$/.test(s)) throw new Error('transcript_sha256_invalid');
  return s.toLowerCase();
}

/** The ordered pair array Spec v2.5 Phase 2.2 serializes, never an object. */
function buildHashInput(fields) {
  const f = fields && typeof fields === 'object' ? fields : {};
  return HASH_FIELDS.map((k) => [k, hashValue(k, f[k])]);
}

/** CONTRATTI section 7 (A), row `source_hash`; form `sha256:<hex>` (Spec v2.5 Phase 2.2). */
function sourceHash(fields) {
  return 'sha256:' + sha256(JSON.stringify(buildHashInput(fields)));
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { ROMATV_HOST, HASH_FIELDS, recordingRef, canonicalRef, keyOf, contentId, fileName,
    recordingFileName, sourceChannel, sourceId, toUtcSecond, durationSeconds, canonicalText, buildHashInput,
    sourceHash };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the per-item adapter (T-A1-18). It reads
 * `platform` (`romatv` or `youtube`), `id` (the guid or the video id), `channel_id` (YouTube
 * only), `n` (only once a reading has fixed it) and the hashed fields under the keys of
 * HASH_FIELDS other than `recording_ref`, which it computes. Each of those keys must be on the
 * item, null when it has no value yet: a key under another name fails instead of hashing as
 * empty. An item without a usable identity fails, it is never given a guessed one. Everything
 * is computed before the item is touched. */
const ref = recordingRef($json.platform, $json.id);
const out = {
  recording_ref: ref,
  recording_file_name: recordingFileName(ref),
  source_channel: sourceChannel($json.platform),
  source_id: sourceId($json.platform, $json.channel_id),
};
const hashed = { recording_ref: ref };
for (const k of HASH_FIELDS) {
  if (k === 'recording_ref') continue;
  if ($json[k] === undefined) throw new Error('hash_field_missing');
  hashed[k] = $json[k];
}
out.source_hash = sourceHash(hashed);
if ($json.n !== undefined && $json.n !== null) {
  out.content_id = contentId(ref, $json.n);
  out.file_name = fileName(out.content_id);
}
Object.assign($json, out);
return $input.item;

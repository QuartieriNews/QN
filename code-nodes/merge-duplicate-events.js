/**
 * merge-duplicate-events.js — DEC-025: the same event from several sources becomes one
 * published element. Same-event recognition reuses the strict criteria of the October
 * 2026 unified sheet (`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21); precedence,
 * filling and the fate of secondary copies follow DEC-025, rules 1-4. The thresholds
 * and the stopword list are that script's, carried here unchanged.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for
 * All Items", JavaScript) the same file runs its adapter on the whole batch.
 */
'use strict';

/** DEC-025 rule 1, nearest source first. Unknown types rank last. */
const PRECEDENCE = ['web_page', 'web_page_linked', 'culture_roma', 'facebook_event', 'roma_today'];

/** Fields another copy may fill when the element lacks them (DEC-025 rule 2). Geography
 *  is never among them: only location evidence moves, and the gazetteer resolves again. */
const FILLABLE = [
  'event.venue', 'event.address', 'event.latitude', 'event.longitude', 'event.booking_url',
  'event.price_text', 'event.organizer_name',
];
const LOCATION = new Set(['event.venue', 'event.address', 'event.latitude', 'event.longitude']);

/** DEC-025 rule 4: starts further apart than this are not merged on their own. */
const START_TOLERANCE_MS = 60 * 60 * 1000;

/** Sources that may give no FILLABLE field: Roma Today is a third-party index only
 *  (DEC-025 rule 2, DEC-108). */
const NO_FILL = new Set(['roma_today']);

/** What the leading source gives an element that keeps another identity (DEC-025 rule 3). */
const LEAD_FIELDS = [
  'event.start_at_utc', 'event.end_at_utc', 'event.effective_end_utc', 'event.date_precision',
  'event.venue', 'event.address', 'event.latitude', 'event.longitude', 'pilot.source_title',
];

const STOP = new Set(('a al alla alle allo ai agli di del della delle dello dei degli da dal dalla dalle in nel ' +
  'nella nelle con su per tra fra e ed il lo la le i gli un una uno the of and at teatro roma edizione ' +
  'spettacolo concerto evento mostra festival live presentazione libro visita guidata').split(' '));

/** Port of Python difflib.SequenceMatcher(None, a, b).ratio(), checked against CPython. */
function ratio(a, b) {
  const b2j = new Map();
  for (let j = 0; j < b.length; j++) {
    const c = b[j];
    if (!b2j.has(c)) b2j.set(c, []);
    b2j.get(c).push(j);
  }
  if (b.length >= 200) {
    const ntest = Math.floor(b.length / 100) + 1;
    for (const [c, idx] of [...b2j]) if (idx.length > ntest) b2j.delete(c);
  }
  function longest(alo, ahi, blo, bhi) {
    let besti = alo, bestj = blo, bestsize = 0;
    let j2len = new Map();
    for (let i = alo; i < ahi; i++) {
      const newj2len = new Map();
      for (const j of b2j.get(a[i]) || []) {
        if (j < blo) continue;
        if (j >= bhi) break;
        const k = (j2len.get(j - 1) || 0) + 1;
        newj2len.set(j, k);
        if (k > bestsize) { besti = i - k + 1; bestj = j - k + 1; bestsize = k; }
      }
      j2len = newj2len;
    }
    while (besti > alo && bestj > blo && a[besti - 1] === b[bestj - 1]) { besti--; bestj--; bestsize++; }
    while (besti + bestsize < ahi && bestj + bestsize < bhi && a[besti + bestsize] === b[bestj + bestsize]) bestsize++;
    return [besti, bestj, bestsize];
  }
  let matches = 0;
  const queue = [[0, a.length, 0, b.length]];
  while (queue.length) {
    const [alo, ahi, blo, bhi] = queue.pop();
    const [i, j, k] = longest(alo, ahi, blo, bhi);
    if (k) {
      matches += k;
      if (alo < i && blo < j) queue.push([alo, i, blo, j]);
      if (i + k < ahi && j + k < bhi) queue.push([i + k, ahi, j + k, bhi]);
    }
  }
  const t = a.length + b.length;
  return t ? (2 * matches) / t : 1;
}

/** The October sheet's normalization: NFKD, no diacritics, lower case, words of 3+
 *  letters or digits outside the stopword list. */
function tokens(s) {
  // Python's encode('ascii', 'ignore'): every non-ASCII code point is dropped, not spaced.
  const t = String(s || '').normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toLowerCase()
    .replace(/[^a-z0-9 ]+/g, ' ');
  return t.split(' ').filter((w) => w.length > 2 && !STOP.has(w));
}

function similarity(ta, tb) {
  if (!ta.length || !tb.length) return 0;
  const A = new Set(ta), B = new Set(tb);
  let inter = 0;
  for (const w of A) if (B.has(w)) inter += 1;
  const j = inter / (A.size + B.size - inter);
  return Math.max(j, ratio(ta.join(' '), tb.join(' ')));
}

function romeDay(instant) {
  if (typeof instant !== 'string' || !/(Z|[+-]\d\d:?\d\d)$/.test(instant) || Number.isNaN(Date.parse(instant))) return null;
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(new Date(Date.parse(instant)));
  const get = (type) => parts.find((p) => p.type === type).value;
  return `${get('year')}-${get('month')}-${get('day')}`;
}

function get(obj, dotted) {
  return dotted.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
}
function set(obj, dotted, value) {
  const keys = dotted.split('.');
  let o = obj;
  for (const k of keys.slice(0, -1)) o = o[k] = Object.assign({}, o[k]);
  o[keys[keys.length - 1]] = value;
}
const empty = (v) => v === undefined || v === null || v === '';

function features(doc) {
  const ev = doc.event || {};
  const start = romeDay(ev.start_at_utc);
  const end = ev.date_precision === 'exact' ? romeDay(ev.end_at_utc) : null;
  return {
    title: tokens((doc.pilot && doc.pilot.source_title) || (doc.article && doc.article.title)),
    venue: new Set(tokens(ev.venue)),
    start,
    end: end || start,
    series: !!(doc.series && doc.series.is_series !== false),
    startMs: typeof ev.start_at_utc === 'string' ? Date.parse(ev.start_at_utc) : NaN,
    lat: typeof ev.latitude === 'number' ? ev.latitude : null,
    lng: typeof ev.longitude === 'number' ? ev.longitude : null,
  };
}

/** Great-circle distance in metres (haversine). */
function metres(fa, fb) {
  const r = (d) => (d * Math.PI) / 180;
  const a = Math.sin(r(fb.lat - fa.lat) / 2) ** 2 +
    Math.cos(r(fa.lat)) * Math.cos(r(fb.lat)) * Math.sin(r(fb.lng - fa.lng) / 2) ** 2;
  return 2 * 6371000 * Math.asin(Math.sqrt(a));
}

/** DEC-025 rule 4: both places known and nothing in common, or more than 1 km apart. */
function venuesConflict(fa, fb, inter) {
  if (fa.venue.size && fb.venue.size && inter === 0) return true;
  if (fa.lat !== null && fa.lng !== null && fb.lat !== null && fb.lng !== null) return metres(fa, fb) > 1000;
  return false;
}

/** 'same' (the October criteria), 'doubt' (DEC-025 rule 4 sends it to the queue
 *  without merging) or null. */
function compare(fa, fb) {
  const s = similarity(fa.title, fb.title);
  if (s < 0.72) return null;
  if (!fa.start || !fb.start) return 'doubt'; // an undated event is never merged
  const ov = fa.start <= fb.end && fb.start <= fa.end;
  if (!ov) return null;
  if (fa.series || fb.series) return 'doubt'; // a series against anything: a person decides
  const inter = [...fa.venue].filter((w) => fb.venue.has(w)).length;
  const vs = fa.venue.size && fb.venue.size ? inter / (fa.venue.size + fb.venue.size - inter) : 0;
  if (s >= 0.85 || (fa.start === fb.start && vs >= 0.5)) {
    // Enough to merge, but the places disagree: a person decides (DEC-025 rule 4).
    if (venuesConflict(fa, fb, inter)) return 'doubt';
    // Same title, same day, hours apart: two performances until a person says otherwise.
    const gap = Math.abs(fa.startMs - fb.startMs);
    return Number.isNaN(gap) || gap <= START_TOLERANCE_MS ? 'same' : 'doubt';
  }
  return 'doubt';
}

function rank(doc) {
  const i = PRECEDENCE.indexOf(doc.source && doc.source.type);
  return i < 0 ? PRECEDENCE.length : i;
}

function addFlag(doc, flag) {
  const q = Object.assign({ review_flags: [] }, doc.quality);
  if (!q.review_flags.includes(flag)) q.review_flags = q.review_flags.concat(flag);
  doc.quality = q;
}

function mergeDuplicateEvents(docs) {
  const out = docs.map((d) => JSON.parse(JSON.stringify(d)));
  const feats = out.map(features);
  const parent = out.map((_, i) => i);
  const find = (x) => { while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; } return x; };
  for (let i = 0; i < out.length; i++) {
    for (let j = i + 1; j < out.length; j++) {
      const c = compare(feats[i], feats[j]);
      if (c === 'same') parent[find(i)] = find(j);
      else if (c === 'doubt') {
        for (const k of [i, j]) {
          addFlag(out[k], 'duplicate_doubt');
          out[k].quality.requires_review = true;
        }
      }
    }
  }
  const groups = new Map();
  out.forEach((_, i) => { const r = find(i); if (!groups.has(r)) groups.set(r, []); groups.get(r).push(i); });
  for (const members of groups.values()) {
    if (members.length < 2) continue;
    const byRank = members.slice().sort((a, b) => rank(out[a]) - rank(out[b]) ||
      String(out[a].content_id).localeCompare(String(out[b].content_id)));
    const lead = byRank[0];
    // DEC-025 rule 3: an element already published keeps its identity.
    const published = members.filter((k) => out[k].pilot && out[k].pilot.first_published_at)
      .sort((a, b) => String(out[a].pilot.first_published_at).localeCompare(String(out[b].pilot.first_published_at)));
    const keep = published.length ? published[0] : lead;
    const element = out[keep];
    const filled = {};
    let moved = false;
    if (keep !== lead) {
      for (const path of LEAD_FIELDS) {
        const v = get(out[lead], path);
        if (!empty(v) && JSON.stringify(v) !== JSON.stringify(get(element, path))) {
          set(element, path, v);
          filled[path] = out[lead].content_id;
          if (LOCATION.has(path)) moved = true;
        }
      }
    }
    const donors = byRank.filter((k) => k !== keep && !NO_FILL.has(out[k].source && out[k].source.type));
    for (const path of FILLABLE) {
      if (!empty(get(element, path))) continue;
      const d = donors.find((k) => !empty(get(out[k], path)));
      if (d !== undefined) {
        set(element, path, get(out[d], path));
        filled[path] = out[d].content_id;
        if (LOCATION.has(path)) moved = true;
      }
    }
    element.pilot = Object.assign({}, element.pilot, {
      lead: out[lead].content_id,
      duplicates: members.filter((k) => k !== keep).map((k) => out[k].content_id).sort(),
      filled_from: filled,
    });
    if (moved) element.pilot.geo_recompute = true; // the gazetteer resolves the new place
    for (const k of members) {
      if (k === keep) continue;
      out[k].pilot = Object.assign({}, out[k].pilot, { duplicate_of: element.content_id });
      addFlag(out[k], 'duplicate_suspected');
    }
  }
  return out;
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { PRECEDENCE, FILLABLE, NO_FILL, LEAD_FIELDS, ratio, tokens, similarity, compare, mergeDuplicateEvents };
  return;
}

/* n8n Code node, "Run Once for All Items" — the batch adapter: every canonical
 * event of the run in, the same events out with the DEC-025 fields set. */
return mergeDuplicateEvents($input.all().map((it) => it.json)).map((json) => ({ json }));

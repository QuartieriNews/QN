/**
 * merge-duplicate-events.js — DEC-025: the same event from several sources becomes one
 * published element. Same-event recognition reuses the strict criteria of the October
 * 2026 unified sheet (`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21). Precedence,
 * filling and identity follow DEC-025, rules 1-3; the way the same event is recognised
 * and what goes to the queue (rule 4) are spelled out in docs/pilota/CONTRATTI.md,
 * section 7. The thresholds and the stopword list are the October script's.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for
 * All Items", JavaScript) the same file runs its adapter on the whole batch.
 */
'use strict';

/** DEC-025 rule 1, nearest source first: the organiser's site is one rank, read directly
 *  or reached through a link. Unknown types rank last. */
const PRECEDENCE = ['web_page', 'culture_roma', 'facebook_event', 'roma_today'];

/** Fields another copy may fill when the element lacks them (DEC-025 rule 2). Geography
 *  is never among them: only location evidence moves, and the gazetteer resolves again. */
const FILLABLE = [
  'event.venue', 'event.address', 'event.latitude', 'event.longitude', 'event.booking_url',
  'event.price_text', 'event.organizer_name',
];
const LOCATION = new Set(['event.venue', 'event.address', 'event.latitude', 'event.longitude']);

/** CONTRATTI.md section 7 (DEC-025 rule 4): starts further apart than this are not
 *  merged on their own. */
const START_TOLERANCE_MS = 60 * 60 * 1000;

/** DEC-025 rule 2: fields that go together come from one source. A unit is present in a
 *  file when its first field is (for times, the start) or, for coordinates, both are. */
const UNITS = [
  ['event.start_at_utc', 'event.end_at_utc', 'event.effective_end_utc', 'event.date_precision'],
  ['event.latitude', 'event.longitude'],
];
function units(paths) {
  const out = [];
  const seen = new Set();
  for (const p of paths) {
    if (seen.has(p)) continue;
    const u = (UNITS.find((g) => g.includes(p)) || [p]).filter((x) => paths.includes(x));
    u.forEach((x) => seen.add(x));
    out.push(u);
  }
  return out;
}

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

function words(s) {
  // Python's encode('ascii', 'ignore'): every non-ASCII code point is dropped, not spaced.
  return String(s || '').normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toLowerCase()
    .replace(/[^a-z0-9 ]+/g, ' ').split(' ').filter((w) => w !== '');
}

/** The October sheet's normalization: NFKD, no diacritics, lower case, words of 3+
 *  letters or digits outside the stopword list. */
function tokens(s) {
  return words(s).filter((w) => w.length > 2 && !STOP.has(w));
}

/** CONTRATTI.md section 7 (DEC-025 rule 4), short identifiers: among the words the
 *  normalization drops, a number of one or two digits, a Roman numeral in I, V and X, or
 *  a single letter, except the one-letter Italian words and elisions. */
const NOT_IDENTIFIERS = new Set(['a', 'e', 'i', 'o', 'c', 'd', 'l']);
function identifiers(s) {
  return new Set(words(s).filter((w) => w.length <= 2 && !NOT_IDENTIFIERS.has(w) &&
    (/^[0-9]{1,2}$/.test(w) || /^(x{0,2})(ix|iv|v?i{0,2})$/.test(w) || /^[a-z]$/.test(w))));
}
const sameSet = (a, b) => a.size === b.size && [...a].every((x) => b.has(x));

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
  // DEC-025 rule 1: the name at the source, never our article title. A file without it
  // would silently match nothing, so it stops the merge instead.
  if (typeof (doc.pilot && doc.pilot.source_title) !== 'string') {
    throw new Error(`${doc.content_id}: pilot.source_title missing (DEC-025 rule 1)`);
  }
  // DEC-025 rule 3: the order of first writing decides which identity stays.
  const written = doc.pilot.first_written_at;
  if (typeof written !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(written)) {
    throw new Error(`${doc.content_id}: pilot.first_written_at missing (DEC-025 rule 3)`);
  }
  const ev = doc.event || {};
  const start = romeDay(ev.start_at_utc);
  const end = ev.date_precision === 'exact' ? romeDay(ev.end_at_utc) : null;
  return {
    title: tokens(doc.pilot.source_title),
    titleIds: identifiers(doc.pilot.source_title),
    venue: new Set(tokens(ev.venue)),
    venueIds: identifiers(ev.venue),
    start,
    end: end || start,
    series: !!(doc.series && doc.series.is_series !== false),
    noTime: (((doc.quality || {}).review_flags) || []).includes('start_time_unknown'),
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

/** CONTRATTI.md section 7 (DEC-025 rule 4): both places known, at least half of their
 *  words in common, the same short identifiers, and no more than 1 km apart when both
 *  have coordinates. */
function placesCoincide(fa, fb) {
  if (!fa.venue.size || !fb.venue.size) return false;
  const inter = [...fa.venue].filter((w) => fb.venue.has(w)).length;
  if (inter / (fa.venue.size + fb.venue.size - inter) < 0.5) return false;
  if (!sameSet(fa.venueIds, fb.venueIds)) return false;
  if (fa.lat !== null && fa.lng !== null && fb.lat !== null && fb.lng !== null) return metres(fa, fb) <= 1000;
  return true;
}

/** 'same' (the October criteria), 'doubt' (CONTRATTI.md section 7 sends it to the queue
 *  without merging) or null. */
function compare(fa, fb) {
  if (!fa.title.length || !fb.title.length) {
    // An empty normalized title never merges; on the same day at the same place it waits.
    return fa.start && fa.start === fb.start && placesCoincide(fa, fb) ? 'doubt' : null;
  }
  const s = similarity(fa.title, fb.title);
  if (s < 0.72) return null;
  if (!fa.start || !fb.start) return 'doubt'; // an undated event is never merged
  const ov = fa.start <= fb.end && fb.start <= fa.end;
  if (!ov) return null;
  if (fa.series || fb.series) return 'doubt'; // a series against anything: a person decides
  if (s < 0.85 && fa.start !== fb.start) return 'doubt';
  if (!placesCoincide(fa, fb)) return 'doubt';
  if (!sameSet(fa.titleIds, fb.titleIds)) return 'doubt'; // «Corso 1» and «Corso 2»
  if (fa.noTime || fb.noTime) return 'doubt'; // a day without a time cannot be matched to a performance
  // Same title, same day, hours apart: two performances until a person says otherwise.
  const gap = Math.abs(fa.startMs - fb.startMs);
  return Number.isNaN(gap) || gap <= START_TOLERANCE_MS ? 'same' : 'doubt';
}

function rank(doc) {
  const i = PRECEDENCE.indexOf(doc.source && doc.source.type);
  return i < 0 ? PRECEDENCE.length : i;
}

/** DEC-025 rule 1, the tie-break inside a rank: an event's own page before a listing,
 *  then content_id, so the result never depends on the order of arrival. */
const fromListing = (doc) => (((doc.quality || {}).review_flags || []).includes('identity_from_listing') ? 1 : 0);
function byPrecedence(a, b) {
  return rank(a) - rank(b) || fromListing(a) - fromListing(b) ||
    String(a.content_id).localeCompare(String(b.content_id));
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
  const verdict = new Map();
  const doubt = (k) => { addFlag(out[k], 'duplicate_doubt'); out[k].quality.requires_review = true; };
  for (let i = 0; i < out.length; i++) {
    for (let j = i + 1; j < out.length; j++) {
      const c = compare(feats[i], feats[j]);
      verdict.set(`${i},${j}`, c);
      if (c === 'same') parent[find(i)] = find(j);
      else if (c === 'doubt') { doubt(i); doubt(j); }
    }
  }
  const groups = new Map();
  out.forEach((_, i) => { const r = find(i); if (!groups.has(r)) groups.set(r, []); groups.get(r).push(i); });
  for (const members of groups.values()) {
    if (members.length < 2) continue;
    // CONTRATTI.md section 7 (DEC-025 rule 4), groups: every pair must be the same event,
    // or the whole group waits.
    const pairs = members.flatMap((a, x) => members.slice(x + 1).map((b) => verdict.get(`${Math.min(a, b)},${Math.max(a, b)}`)));
    if (!pairs.every((c) => c === 'same')) { members.forEach(doubt); continue; }
    const byRank = members.slice().sort((a, b) => byPrecedence(out[a], out[b]));
    const lead = byRank[0];
    // DEC-025 rule 3: the element written first keeps its identity; a tie goes to the lead.
    const keep = byRank.slice().sort((a, b) =>
      out[a].pilot.first_written_at.localeCompare(out[b].pilot.first_written_at) ||
      byRank.indexOf(a) - byRank.indexOf(b))[0];
    const element = out[keep];
    const filled = {};
    let moved = false;
    // DEC-025 rule 2: a human_verified geography is never recalculated, so no location
    // evidence moves into it; different evidence sends the element to the queue instead.
    const verified = ((element.geography || {}).geo_verification_status) === 'human_verified';
    const present = (doc, u) => (u[0] === 'event.start_at_utc' ? !empty(get(doc, u[0])) : u.every((p) => !empty(get(doc, p))));
    const same = (a, b, u) => u.every((p) => JSON.stringify(get(a, p)) === JSON.stringify(get(b, p)));
    const take = (u, from) => {
      if (verified && u.some((p) => LOCATION.has(p))) {
        if (!same(element, out[from], u)) {
          addFlag(element, 'geo_verified_conflict');
          element.quality.requires_review = true;
        }
        return;
      }
      for (const p of u) { set(element, p, get(out[from], p)); filled[p] = out[from].content_id; }
      if (u.some((p) => LOCATION.has(p))) moved = true;
    };
    // An element whose queue row is still undecided keeps the fields the reviewer sees;
    // the merge records the group and fills the fields at the first run after the decision.
    const pending = !!(element.pilot && element.pilot.review_pending);
    if (pending) addFlag(element, 'merge_deferred');
    if (!pending && keep !== lead) {
      for (const u of units(LEAD_FIELDS)) {
        if (present(out[lead], u) && !same(element, out[lead], u)) take(u, lead);
      }
    }
    const donors = byRank.filter((k) => k !== keep && !NO_FILL.has(out[k].source && out[k].source.type));
    if (!pending) {
      for (const u of units(FILLABLE)) {
        if (present(element, u)) continue;
        const d = donors.find((k) => present(out[k], u));
        if (d !== undefined) take(u, d);
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
  module.exports = {
    PRECEDENCE, FILLABLE, NO_FILL, LEAD_FIELDS, ratio, tokens, identifiers, similarity, features, compare,
    mergeDuplicateEvents,
  };
  return;
}

/* n8n Code node, "Run Once for All Items" — the batch adapter: every canonical
 * event of the run in, the same events out with the DEC-025 fields set. */
return mergeDuplicateEvents($input.all().map((it) => it.json)).map((json) => ({ json }));

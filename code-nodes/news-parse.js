/**
 * news-parse.js — workstream B: the pages a collection run saved become source records
 * (URL, title, publication time, categories), and only the records not seen before go on.
 * The rules are in docs/pilota/CONTRATTI.md, section 7 («B · Notizie»); this file does not
 * restate them. It writes no news element: the records are the input of the steps that
 * the next PRs add (geography, editorial filter, our own writing).
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for Each
 * Item") the same file runs its adapter, keeping the URLs already seen in the workflow's
 * static data. The n8n Code node has no `URL` global, so URLs are read with patterns.
 */
'use strict';

/** How many URLs the index of what was seen keeps, the newest last. */
const SEEN_MAX = 5000;
/** Categories that mark an agency dispatch, which never counts as an independent publisher
 *  (CONTRATTI.md section 7, B, «Pubblicabile»). */
const AGENCY = /^(adnkronos|ansa|italpress|agenzia dire|dire|askanews|agi|agenzia nova|lapresse)$/i;

const MONTHS = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 };

function decodeEntities(s) {
  return s
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&quot;/g, '"').replace(/&apos;|&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
}

/** Visible text of a fragment: tags dropped, entities decoded, whitespace collapsed. */
function text(fragment) {
  return decodeEntities(String(fragment).replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1').replace(/<[^>]*>/g, ' '))
    .replace(/\s+/g, ' ').trim();
}

/** RFC 822 dates of RSS (`Tue, 10 Nov 2026 20:19:10 +0000`) as a UTC instant, or null when the
 *  date does not read: a record without a time is kept, never given a guessed one. */
function rfc822(v) {
  const m = typeof v === 'string' &&
    /^\s*(?:[A-Za-z]{3},\s*)?(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})\s+(\d{2}):(\d{2})(?::(\d{2}))?\s+(GMT|UTC|Z|[+-]\d{4})\s*$/.exec(v);
  if (!m) return null;
  const mo = MONTHS[m[2].toLowerCase()];
  const [d, y, h, mi, s] = [m[1], m[3], m[4], m[5], m[6] || '0'].map(Number);
  if (!mo || h > 23 || mi > 59 || s > 59) return null;
  const t = new Date(Date.UTC(y, mo - 1, d, h, mi, s));
  if (t.getUTCDate() !== d || t.getUTCMonth() !== mo - 1) return null;
  let off = 0;
  if (/^[+-]\d{4}$/.test(m[7])) {
    const sign = m[7][0] === '-' ? -1 : 1;
    off = sign * (Number(m[7].slice(1, 3)) * 60 + Number(m[7].slice(3, 5)));
  }
  return new Date(t.getTime() - off * 60000).toISOString();
}

function absolute(href, origin) {
  const h = decodeEntities(href.trim());
  if (/^https?:\/\//i.test(h)) return h;
  if (h.startsWith('/')) return origin.replace(/\/+$/, '') + h;
  return null;
}

/** The items of an RSS 2.0 feed. */
function parseRss(xml) {
  if (typeof xml !== 'string' || !/<rss[\s>]/i.test(xml)) throw new Error('not an RSS feed');
  const out = [];
  for (const m of xml.matchAll(/<item[\s>]([\s\S]*?)<\/item>/gi)) {
    const it = m[1];
    const tag = (name) => { const t = new RegExp(`<${name}[^>]*>([\\s\\S]*?)<\\/${name}>`, 'i').exec(it); return t ? text(t[1]) : null; };
    const link = tag('link') || tag('guid');
    if (!link || !/^https?:\/\//i.test(link)) continue;
    const categories = [...it.matchAll(/<category[^>]*>([\s\S]*?)<\/category>/gi)].map((c) => text(c[1])).filter(Boolean);
    out.push({ url: link, title: tag('title') || '', published_at_utc: rfc822(tag('pubDate')), categories,
      agency: categories.some((c) => AGENCY.test(c)) });
  }
  return out;
}

/** The releases of the Questura listing: an `elenco_notizie` block each, with its link and
 *  title. The listing gives no date: the record has none until a later step reads it. */
function parseQuesturaListing(html, origin) {
  if (typeof html !== 'string') throw new Error('not a listing page');
  const out = [];
  for (const m of html.matchAll(/<div class="elenco_notizie[^"]*">[\s\S]*?<h3>\s*<a href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi)) {
    const url = absolute(m[1], origin);
    if (!url) continue;
    out.push({ url, title: text(m[2]), published_at_utc: null, categories: [], agency: false });
  }
  return out;
}

/** The parser of each source (news-collect.js, SOURCES); a source without one is skipped. */
const PARSERS = {
  'questure.poliziadistato.it': (body) => parseQuesturaListing(body, 'https://questure.poliziadistato.it'),
  'abitarearoma.it': parseRss,
  'cdn.ilfaroonline.it': parseRss,
};

/** Stage 'records': the files a run saved (`{ name, body }`, named `notizie_<source>_<start>_<n>`)
 *  become the records not seen before, with the index of what was seen. A page that does not
 *  parse is counted, never read as «nothing new». */
function newRecords({ files, seen, retrieved_at }) {
  if (!Array.isArray(files)) throw new Error('files must list the pages saved by the run');
  const index = Array.isArray(seen) ? seen.slice() : [];
  const known = new Set(index);
  const records = [];
  const outcome = [];
  for (const f of files) {
    const m = /^notizie_(.+)_(\d{8}T\d{6}Z)_(\d+)\.(xml|html|json)$/.exec((f && f.name) || '');
    if (!m) throw new Error(`a file that is not a collection page: ${f && f.name}`);
    const source_id = m[1];
    const parse = PARSERS[source_id];
    if (!parse) { outcome.push({ source_id, outcome: 'no parser' }); continue; }
    let items;
    try {
      items = parse(f.body);
    } catch (e) {
      outcome.push({ source_id, outcome: 'unreadable', reason: e.message });
      continue;
    }
    if (items.length === 0) { outcome.push({ source_id, outcome: 'unreadable', reason: 'no items' }); continue; }
    let fresh = 0;
    for (const it of items) {
      const key = it.url.replace(/#.*$/, '').replace(/\/+$/, '').toLowerCase();
      if (known.has(key)) continue;
      known.add(key);
      index.push(key);
      fresh += 1;
      records.push(Object.assign({ source_id, page: `originali/${f.name}`, retrieved_at: retrieved_at || null }, it));
    }
    outcome.push({ source_id, outcome: 'read', items: items.length, new: fresh });
  }
  return { records, seen: index.slice(-SEEN_MAX), outcome };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { SEEN_MAX, AGENCY, decodeEntities, text, rfc822, parseRss, parseQuesturaListing, PARSERS, newRecords };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter: the index of what was seen lives in
 * the workflow's static data, saved by n8n after a production run. */
const store = $getWorkflowStaticData('global');
const res = newRecords({ files: $json.files, seen: store.news_seen, retrieved_at: $json.now });
store.news_seen = res.seen;
$json.records = res.records;
$json.records_outcome = res.outcome;
$json.records_file_name = res.records.length ? String($json.log_file_name).replace(/^notizie_/, 'notizie_righe_') : null;
return $input.item;

#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-parse.js: the pages saved by a collection run of
 * channel B become source records (docs/pilota/CONTRATTI.md, section 7, «B · Notizie»): RSS
 * 2.0 with RFC 822 dates, the Questura listing, agency dispatches marked, only what was not
 * seen before, a page that does not parse counted, and the n8n adapter evaluated from the
 * exact committed file with stubbed $input/$json/$getWorkflowStaticData. Every feed, listing,
 * title and URL is invented (DEC-109, DEC-031 point 4).
 *
 * Run:  node tests/test_news_parse.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'news-parse.js');
const m = require(FILE);

let failures = 0;
let checks = 0;

function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) {
    console.log(`  ok   ${label}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`);
  }
}

function thrown(fn) {
  try { fn(); return null; } catch (e) { return e.message; }
}

const RSS = `<?xml version="1.0"?><rss version="2.0"><channel><title>Testata inventata</title>
<item><title>Primo titolo &amp; inventato</title><link>https://www.esempio-inventato.it/primo/</link>
<pubDate>Tue, 10 Nov 2026 20:19:10 +0000</pubDate><category><![CDATA[Cronaca]]></category><description><![CDATA[<p>Testo</p>]]></description></item>
<item><title><![CDATA[Secondo titolo]]></title><link>https://www.esempio-inventato.it/secondo/</link>
<pubDate>Tue, 10 Nov 2026 21:00:00 +0100</pubDate><category>AdnKronos</category></item>
<item><title>Senza link</title></item>
</channel></rss>`;
const LISTING = `<div class="lst lst-notizie"><div class="elenco_notizie notizia"><span class="label label-primary">I fatti del giorno</span>
<h3><a href="/it/Roma/articolo/111aaa">Comunicato inventato uno</a></h3><div class="content"><p><em>x</em></p></div></div>
<div class="elenco_notizie notizia"><span class="label">I fatti del giorno</span><h3><a href="https://questure.poliziadistato.it/it/Roma/articolo/222bbb">Comunicato inventato &quot;due&quot;</a></h3></div></div>`;

console.log('RSS 2.0');
const items = m.parseRss(RSS);
check('the items with a link, in order', items.map((i) => i.url), ['https://www.esempio-inventato.it/primo/', 'https://www.esempio-inventato.it/secondo/']);
check('entities and CDATA are read', items.map((i) => i.title), ['Primo titolo & inventato', 'Secondo titolo']);
check('the RFC 822 date as a UTC instant', items[0].published_at_utc, '2026-11-10T20:19:10.000Z');
check('an offset is applied (Spec v2.5 T17: one instant, one value)', items[1].published_at_utc, '2026-11-10T20:00:00.000Z');
check('categories are kept', items[0].categories, ['Cronaca']);
check('an agency dispatch is marked', items.map((i) => i.agency), [false, true]);
check('a date that does not read is null, not guessed', m.rfc822('31 Feb 2026 10:00:00 +0000'), null);
check('nor is hour 25', m.rfc822('Tue, 10 Nov 2026 25:00:00 +0000'), null);
check('GMT is UTC', m.rfc822('Tue, 10 Nov 2026 08:00:00 GMT'), '2026-11-10T08:00:00.000Z');
check('a page that is not RSS is refused', thrown(() => m.parseRss('<html></html>')), 'not an RSS feed');

console.log('the Questura listing');
const rel = m.parseQuesturaListing(LISTING, 'https://questure.poliziadistato.it');
check('one record per release, the link made absolute', rel.map((r) => r.url),
  ['https://questure.poliziadistato.it/it/Roma/articolo/111aaa', 'https://questure.poliziadistato.it/it/Roma/articolo/222bbb']);
check('titles read as text', rel.map((r) => r.title), ['Comunicato inventato uno', 'Comunicato inventato "due"']);
check('the listing gives no date: none is guessed', rel.map((r) => r.published_at_utc), [null, null]);

console.log('records: only what was not seen before');
const files = [
  { name: 'notizie_cdn.ilfaroonline.it_20261110T220700Z.xml', body: RSS },
  { name: 'notizie_questure.poliziadistato.it_20261110T220700Z.html', body: LISTING },
  { name: 'notizie_carabinieri.it_20261110T220700Z.html', body: '<html></html>' },
];
const first = m.newRecords({ files, seen: [], retrieved_at: '2026-11-10T22:07:00Z' });
check('the first run gives every record', first.records.length, 4);
check('each record names its source and its saved page', [first.records[0].source_id, first.records[0].page],
  ['cdn.ilfaroonline.it', 'originali/notizie_cdn.ilfaroonline.it_20261110T220700Z.xml']);
check('a source without a parser is said so', first.outcome.find((o) => o.source_id === 'carabinieri.it').outcome, 'no parser');
const second = m.newRecords({ files, seen: first.seen, retrieved_at: '2026-11-10T23:07:00Z' });
check('the next run with the same pages gives nothing new', second.records.length, 0);
check('and says it read them', second.outcome.filter((o) => o.outcome === 'read').map((o) => o.new), [0, 0]);
check('a trailing slash or a fragment is the same URL',
  m.newRecords({ files: [{ name: 'notizie_cdn.ilfaroonline.it_20261110T230700Z.xml', body: RSS.replace('/primo/', '/primo#x') }], seen: first.seen }).records.length, 0);
const broken = m.newRecords({ files: [{ name: 'notizie_abitarearoma.it_20261110T220700Z.xml', body: '<html>non è un feed</html>' }], seen: [] });
check('a page that does not parse is counted, never read as nothing new', broken.outcome[0].outcome, 'unreadable');
const empty = m.newRecords({ files: [{ name: 'notizie_abitarearoma.it_20261110T220700Z.xml', body: '<rss></rss>' }], seen: [] });
check('a feed without items is unreadable too', empty.outcome[0].reason, 'no items');
check('a file that is not a collection page is a workflow error', /not a collection page/.test(thrown(() => m.newRecords({ files: [{ name: 'altro.json', body: '' }] })) || ''), true);
const many = Array.from({ length: m.SEEN_MAX + 10 }, (_, i) => `https://esempio-inventato.it/${i}`);
check('the index keeps the newest URLs', m.newRecords({ files: [], seen: many }).seen.length, m.SEEN_MAX);
check('the node does not use the URL global, which n8n does not have', /new URL\(/.test(fs.readFileSync(FILE, 'utf8')), false);

console.log('n8n adapter — exact committed file, stubbed $input/$json/$getWorkflowStaticData');
const src = fs.readFileSync(FILE, 'utf8');
const store = {};
function runNode(json) {
  const item = { json };
  return new Function('$input', '$json', 'require', '$getWorkflowStaticData', 'URL', 'URLSearchParams', src)(
    { item }, json, require, () => store, undefined, undefined);
}
{
  const out = runNode({ files, now: '2026-11-10T22:07:00Z', log_file_name: 'notizie_20261110T220700Z.json' });
  check('the adapter adds the records and the file to write', [out.json.records.length, out.json.records_file_name], [4, 'notizie_righe_20261110T220700Z.json']);
  check('the index is kept in the static data', store.news_seen.length, 4);
  const again = runNode({ files, now: '2026-11-10T23:07:00Z', log_file_name: 'notizie_20261110T230700Z.json' });
  check('nothing new, no file', [again.json.records.length, again.json.records_file_name], [0, null]);
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

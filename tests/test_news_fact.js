#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-fact.js: the category of a news fact, whether it
 * may be published, its lead source (capofila), the publishers it counts and the sources it
 * cites (docs/pilota/CONTRATTI.md, section 7, «B · Notizie»; DEC-108; DEC-034, R-C02;
 * docs/sources/CRONACA_PROCESSO_2026-10.md, section 4.6), the agency pattern kept equal to
 * news-parse.js, and the n8n adapter evaluated from the exact committed file with stubbed
 * $input/$json. Every URL and text is invented (DEC-109, DEC-031 point 4); the hosts are the
 * outlets the rules name, with invented paths.
 *
 * Run:  node tests/test_news_fact.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'news-fact.js');
const m = require(FILE);
const parse = require(path.join(__dirname, '..', 'code-nodes', 'news-parse.js'));

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

/** A record as the grouping step hands it over; `p` is the invented path. */
function rec(source_id, source_channel, p, published_at_utc, extra) {
  return Object.assign({ source_id, source_channel, url: `https://${source_id}/${p}`, published_at_utc, categories: [], agency: false }, extra || {});
}

const QUESTURA = (t) => rec('questure.poliziadistato.it', 'news_official', 'roma/fatto-inventato', t);
const CARABINIERI = (t) => rec('carabinieri.it', 'news_official', 'comunicato-inventato', t);
const ABITARE = (t, extra) => rec('abitarearoma.it', 'news_press', 'fatto-inventato/', t, extra);
const FARO = (t, extra) => rec('cdn.ilfaroonline.it', 'news_press', 'fatto-inventato/', t, extra);
const ROMATODAY = (t) => rec('romatoday.it', 'news_index', 'cronaca/fatto-inventato.html', t);
const TODAY = (t) => rec('today.it', 'news_index', 'fatto-inventato.html', t);
const MESSAGGERO = (t) => rec('ilmessaggero.it', 'news_index', 'roma/fatto-inventato.html', t);
const T1 = '2026-11-10T08:00:00Z';
const T2 = '2026-11-10T09:00:00Z';
const T3 = '2026-11-10T10:00:00Z';

console.log('categories (CRONACA_PROCESSO §4.6, CONTRATTI section 7 B «Pubblicabile»)');
{
  const r = m.factSources([QUESTURA(T2)]);
  check('an official fact alone is «ufficiale» and may be published', [r.categoria, r.pubblicabile], ['ufficiale', true]);
  check('an official source is not a publisher', r.editori, []);
}
{
  const r = m.factSources([ABITARE(T1), FARO(T2)]);
  check('two open outlets of two publishers: «stampa_due_fonti», publishable', [r.categoria, r.pubblicabile], ['stampa_due_fonti', true]);
  check('…and both publishers are counted, sorted', r.editori, ['Abitare a Roma', 'Il Faro Online']);
}
{
  const r = m.factSources([ROMATODAY(T1), ABITARE(T2)]);
  check('an open outlet and a closed one of another publisher: «stampa_due_fonti»', r.categoria, 'stampa_due_fonti');
}
{
  const r = m.factSources([ABITARE(T1)]);
  check('one open outlet alone: «stampa_una_fonte», not published', [r.categoria, r.pubblicabile], ['stampa_una_fonte', false]);
}
{
  const r = m.factSources([ROMATODAY(T1), MESSAGGERO(T2)]);
  check('closed outlets only, two publishers: «chiuse_due_fonti», not published (nothing to write from)',
    [r.categoria, r.pubblicabile], ['chiuse_due_fonti', false]);
}
{
  const r = m.factSources([ROMATODAY(T1), TODAY(T2)]);
  check('two outlets of one group count once: «chiuse_una_fonte»', [r.categoria, r.editori], ['chiuse_una_fonte', ['Citynews']]);
}
{
  const r = m.factSources([ABITARE(T1), ROMATODAY(T2), TODAY(T3)]);
  check('one group seen twice beside an open outlet still makes two publishers', r.editori, ['Abitare a Roma', 'Citynews']);
}
{
  const all = [[QUESTURA(T1)], [ABITARE(T1), FARO(T2)], [ABITARE(T1)], [ROMATODAY(T1), MESSAGGERO(T2)], [ROMATODAY(T1)]];
  check('every category is one of CATEGORIES, and only two may be published',
    [all.every((x) => m.CATEGORIES.includes(m.factSources(x).categoria)), m.PUBLISHABLE], [true, ['ufficiale', 'stampa_due_fonti']]);
}

console.log('agency dispatches (R-C02: the same dispatch on several sites is one source)');
{
  const ansa = { agency: true, categories: ['Cronaca', 'ANSA'] };
  const r = m.factSources([ABITARE(T1, ansa), FARO(T2, ansa)]);
  check('the same agency on two open sites is one publisher: «stampa_una_fonte»', [r.categoria, r.editori], ['stampa_una_fonte', ['ANSA']]);
}
{
  const r = m.factSources([FARO(T1, { agency: true, categories: [' ansa '] }), rec('ansa.it', 'news_index', 'lazio/fatto.html', T2)]);
  check('a dispatch and the agency\'s own site are one publisher', r.editori, ['ANSA']);
}
{
  const r = m.factSources([ABITARE(T1), FARO(T2, { agency: true, categories: ['Agenzia Dire'] })]);
  check('an outlet\'s own article and an agency dispatch are two publishers', [r.categoria, r.editori], ['stampa_due_fonti', ['Abitare a Roma', 'Dire']]);
}
{
  const r = m.factSources([FARO(T1, { agency: true, categories: ['Cronaca'] })]);
  check('a record marked as a dispatch with no agency category counts as its outlet', r.editori, ['Il Faro Online']);
}
check('the agency pattern is the one of news-parse.js', String(m.AGENCY), String(parse.AGENCY));
check('every agency of the table matches the pattern, and has a publisher',
  Object.keys(m.AGENCY_PUBLISHER).every((a) => m.AGENCY.test(a) && typeof m.AGENCY_PUBLISHER[a] === 'string'), true);
check('every alternative of the pattern is in the table',
  /\^\((.*)\)\$/.exec(m.AGENCY.source)[1].split('|').every((a) => Object.prototype.hasOwnProperty.call(m.AGENCY_PUBLISHER, a)), true);
check('an agency counts with the same name as its own site', [m.AGENCY_PUBLISHER.ansa, m.outletPublisher('ansa.it'),
  m.AGENCY_PUBLISHER['agenzia dire'], m.outletPublisher('dire.it')], ['ANSA', 'ANSA', 'Dire', 'Dire']);

console.log('publishers of outlets');
check('a subdomain takes its domain\'s publisher', [m.outletPublisher('roma.corriere.it'), m.outletPublisher('cdn.ilfaroonline.it')], ['RCS', 'Il Faro Online']);
check('a host with www. and in capitals is the same outlet', m.outletPublisher('WWW.RomaToday.it'), 'Citynews');
check('an outlet that is not listed is its own publisher', m.outletPublisher('www.testata-inventata.it'), 'testata-inventata.it');
check('a listed name is never matched on the last label alone', m.outletPublisher('it'), 'it');

console.log('capofila (DEC-034, R-C02)');
{
  const r = m.factSources([ABITARE(T1), QUESTURA(T3), FARO(T2)]);
  check('the official source leads, even when the press was first', r.capofila,
    { source_id: 'questure.poliziadistato.it', source_channel: 'news_official', url: 'https://questure.poliziadistato.it/roma/fatto-inventato' });
}
{
  const r = m.factSources([CARABINIERI(T3), QUESTURA(T2)]);
  check('between two official sources, the first published leads', r.capofila.source_id, 'questure.poliziadistato.it');
}
{
  const r = m.factSources([ROMATODAY(T1), FARO(T3), ABITARE(T2)]);
  check('without an official source, the first open outlet leads, never a closed one', r.capofila.source_id, 'abitarearoma.it');
}
{
  const r = m.factSources([ROMATODAY(T1), MESSAGGERO(T2)]);
  check('closed outlets only: no capofila', r.capofila, null);
}
{
  const r = m.factSources([ABITARE(null), FARO(T2)]);
  check('a record without a time comes after the timed ones', r.capofila.source_id, 'cdn.ilfaroonline.it');
}
{
  const r = m.factSources([FARO(T2), ABITARE(T2)]);
  check('equal times keep the order the records came in', r.capofila.source_id, 'cdn.ilfaroonline.it');
}
{
  const r = m.factSources([ABITARE('2026-11-10T10:30:00+01:00'), FARO('2026-11-10T09:45:00Z')]);
  check('times with an offset are compared as instants', r.capofila.source_id, 'abitarearoma.it');
}

console.log('attribuzioni (CONTRATTI section 2)');
{
  const r = m.factSources([FARO(T3), ABITARE(T2), QUESTURA(T1), ABITARE(T3, { url: 'https://abitarearoma.it/aggiornamento-inventato/' })]);
  check('one entry per source, in the order of publication, with its first record', r.attribuzioni, [
    { source_id: 'questure.poliziadistato.it', source_channel: 'news_official', publisher: null, url: 'https://questure.poliziadistato.it/roma/fatto-inventato', published_at_utc: T1 },
    { source_id: 'abitarearoma.it', source_channel: 'news_press', publisher: 'Abitare a Roma', url: 'https://abitarearoma.it/fatto-inventato/', published_at_utc: T2 },
    { source_id: 'cdn.ilfaroonline.it', source_channel: 'news_press', publisher: 'Il Faro Online', url: 'https://cdn.ilfaroonline.it/fatto-inventato/', published_at_utc: T3 },
  ]);
}
{
  const r = m.factSources([ROMATODAY(T1), ABITARE(T2)]);
  check('a closed outlet is cited too: it counts and is linked (DEC-108)', r.attribuzioni.map((a) => a.source_channel), ['news_index', 'news_press']);
}

console.log('idempotency');
{
  const a = m.factSources([ABITARE(T1), ROMATODAY(T2), FARO(T3)]);
  const b = m.factSources([FARO(T3), ROMATODAY(T2), ABITARE(T1)]);
  check('the same records in another order give the same result', JSON.stringify(a), JSON.stringify(b));
  const input = [ABITARE(T1), FARO(T2)];
  const copy = JSON.stringify(input);
  m.factSources(input);
  check('the input is not changed', JSON.stringify(input), copy);
}

console.log('records that do not read stop the fact');
check('no records', thrown(() => m.factSources([])), 'records_missing');
check('records not in a list', thrown(() => m.factSources(null)), 'records_missing');
check('a record that is not an object', thrown(() => m.factSources([ABITARE(T1), null])), 'record_invalid: 1');
check('a record without source_id', thrown(() => m.factSources([Object.assign(ABITARE(T1), { source_id: ' ' })])), 'record_invalid: 0 source_id');
check('a record without an http(s) URL', thrown(() => m.factSources([Object.assign(ABITARE(T1), { url: 'ftp://x/y' })])), 'record_invalid: 0 url');
check('a channel that is not a news channel', thrown(() => m.factSources([Object.assign(ABITARE(T1), { source_channel: 'fb_event' })])), 'record_invalid: 0 source_channel');
check('a time that is not an ISO instant', thrown(() => m.factSources([ABITARE('10/11/2026 09:00')])), 'record_invalid: 0 published_at_utc');
check('a time that is not a real day', thrown(() => m.factSources([ABITARE('2026-13-40T09:00:00Z')])), 'record_invalid: 0 published_at_utc');
check('30 February is not moved to March', thrown(() => m.factSources([ABITARE('2026-02-30T09:00:00Z')])), 'record_invalid: 0 published_at_utc');
check('an hour past 23 is not the next day', thrown(() => m.factSources([ABITARE('2026-11-10T24:00:00Z')])), 'record_invalid: 0 published_at_utc');
check('an offset past 23:59 does not read', thrown(() => m.factSources([ABITARE('2026-11-10T09:00:00+24:00')])), 'record_invalid: 0 published_at_utc');
check('29 February of a leap year reads', m.validInstant('2028-02-29T09:00:00.5Z'), true);

console.log('n8n adapter, from the exact committed file');
{
  const src = fs.readFileSync(FILE, 'utf8');
  const item = { json: { records: [ROMATODAY(T1), ABITARE(T2)], other: 'kept' } };
  const run = new Function('$input', '$json', 'require', 'module', src);
  const out = run({ item }, item.json, require, { exports: {} });
  check('the adapter returns the item', out === item, true);
  check('…with the sources the article cites', item.json.attribuzioni.map((a) => a.source_id), ['romatoday.it', 'abitarearoma.it']);
  check('…and what they allow', item.json.pubblicazione, { categoria: 'stampa_due_fonti', pubblicabile: true,
    editori: ['Abitare a Roma', 'Citynews'], capofila: { source_id: 'abitarearoma.it', source_channel: 'news_press', url: 'https://abitarearoma.it/fatto-inventato/' } });
  check('…keeping the other fields', item.json.other, 'kept');
  const bad = { json: { records: [] } };
  check('an item whose records do not read fails', thrown(() => run({ item: bad }, bad.json, require, { exports: {} })), 'records_missing');
}

console.log(failures ? `\n${failures} FAILED of ${checks}` : `\nALL PASS (${checks} checks)`);
process.exit(failures ? 1 : 0);

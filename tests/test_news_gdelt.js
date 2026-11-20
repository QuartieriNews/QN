#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-gdelt.js: the two-week measure of GDELT as the
 * third-party index of channel B (docs/pilota/CONTRATTI.md, section 7, «B · Notizie», row «Misura
 * GDELT»; DEC-039, point 4; DEC-108): the copies kept equal to news-collect.js, the searches and
 * the gazetteer they come from, robots.txt once a Rome day (Spec v2.5 T17), the windows, the
 * answers that stop the host, the rows (title, link, hour, site, search: never the article), the
 * register and the alert, the n8n adapter evaluated from the exact committed file with stubbed
 * $input/$json/$getWorkflowStaticData, the flow exported in workflows/, the runs in a row with a 429
 * (DEC-045) or a server error, the end of the measure and the state kept until the files are written.
 * Every article, title and link is invented (DEC-109, DEC-031 point 4). T-B-G1-nn name the cases.
 *
 * Run:  node tests/test_news_gdelt.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const ROOT = path.join(__dirname, '..');
const FILE = path.join(ROOT, 'code-nodes', 'news-gdelt.js');
const m = require(FILE);
const collect = require(path.join(ROOT, 'code-nodes', 'news-collect.js'));

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

/* ----- T-B-G1-01 the copies -------------------------------------------------- */

console.log('T-B-G1-01 the copies stay byte-equal to news-collect.js');
/** The text of a top-level declaration: a function to its closing brace, a constant to the first
 *  line that ends with a semicolon. */
function chunk(text, name) {
  const lines = text.split('\n');
  const start = lines.findIndex((l) => l.startsWith(`function ${name}(`) || l.startsWith(`const ${name} = `));
  if (start < 0) return null;
  const isFn = lines[start].startsWith('function ');
  let end = start;
  while (end < lines.length && !(isFn ? lines[end] === '}' : /;\s*$/.test(lines[end]))) end += 1;
  return lines.slice(start, end + 1).join('\n');
}
const OWN = fs.readFileSync(FILE, 'utf8');
const COLLECT = fs.readFileSync(path.join(ROOT, 'code-nodes', 'news-collect.js'), 'utf8');
for (const name of ['USER_AGENT', 'AGENT_TOKENS', 'ERRORS_TO_STOP', 'urlParts', 'ROME_DAY', 'romeDay', 'compactInstant', 'bodyText',
  'statusOf', 'failure', 'instant', 'parseRobots', 'ruleMatches', 'groupAllows', 'robotsVerdict', 'hostOf', 'pathOf',
  'resolveLocation', 'LOGIN', 'CHALLENGE', 'isHtml', 'titleAndHeading', 'blockSignal']) {
  check(`T-B-G1-01 ${name} is the text of news-collect.js`, chunk(OWN, name) !== null && chunk(OWN, name) === chunk(COLLECT, name), true);
}
check('T-B-G1-01 the same user agent as the collection', m.USER_AGENT, collect.USER_AGENT);

/* ----- T-B-G1-02 the searches ------------------------------------------------ */

console.log('T-B-G1-02 the searches: the pilot pages from the gazetteer, the outlets of DEC-108');
const GAZ = JSON.parse(fs.readFileSync(path.join(ROOT, 'gazetteer', 'gazetteer.json'), 'utf8'));
const PILOT = ['acilia', 'centocelle', 'prati']; // CONTRATTI.md section 1
check('T-B-G1-02 one page search per pilot page, with the search query of the gazetteer', m.PAGES.map((p) => [p.zone, p.query]),
  PILOT.map((id) => { const z = GAZ.publication_zones.find((x) => x.publication_zone_id === id); return [id, z && z.search_queries]; }));
check('T-B-G1-02 every pilot page is a page of the gazetteer', PILOT.every((id) => GAZ.publication_zones.some((z) => z.publication_zone_id === id && z.is_page === true)), true);
check('T-B-G1-02 the eight closed outlets of DEC-108, by domain', m.OUTLETS.filter((o) => o.closed).map((o) => o.domain),
  ['romatoday.it', 'ilmessaggero.it', 'ansa.it', 'corriere.it', 'repubblica.it', 'leggo.it', 'today.it', 'agenzianova.com']);
check('T-B-G1-02 the two open outlets are press sources of the collection', m.OUTLETS.filter((o) => !o.closed).map((o) =>
  collect.SOURCES.some((s) => s.channel === 'news_press' && (s.source_id === o.domain || s.source_id.endsWith('.' + o.domain)))), [true, true]);
const S = m.searches();
check('T-B-G1-02 thirteen searches a run, pages first', [S.length, S.slice(0, 3).map((q) => q.id)], [13, ['pagina:acilia', 'pagina:centocelle', 'pagina:prati']]);
check('T-B-G1-02 a page search is its query in Italian, an outlet search its domain',
  [S[0].query, S[3].query, S[3].domain], ['Acilia sourcelang:italian', 'domain:romatoday.it', 'romatoday.it']);
const U = m.searchUrl('Acilia sourcelang:italian', Date.parse('2026-11-19T21:45:00Z'), Date.parse('2026-11-19T23:45:00Z'));
check('T-B-G1-02 the request: the list of articles in JSON, at most 250, the window in the service\'s form', U,
  'https://api.gdeltproject.org/api/v2/doc/doc?query=Acilia%20sourcelang%3Aitalian&mode=artlist&format=json&maxrecords=250&sort=datedesc&startdatetime=20261119214500&enddatetime=20261119234500');
check('T-B-G1-02 the order turns by one place every two hours: in thirteen runs each search is asked first once',
  new Set(Array.from({ length: 13 }, (_, k) => m.searchOrder(new Date(Date.parse('2026-11-20T00:37:00Z') + k * 7200000).toISOString())[0].id)).size, 13);
check('T-B-G1-02 the only host is the search service', [m.HOST, /^https:\/\/api\.gdeltproject\.org\//.test(m.API_URL), m.ROBOTS_URL],
  ['api.gdeltproject.org', true, 'https://api.gdeltproject.org/robots.txt']);

/* ----- T-B-G1-03 the plan ---------------------------------------------------- */

console.log('T-B-G1-03 robots.txt once a Rome day, none after a stop or after the end');
const NOW = '2026-11-20T00:05:12.345Z';
const p0 = m.planRun({ state: undefined, now: NOW });
check('T-B-G1-03 a first run reads robots.txt', p0.robots, [{ source_id: 'api.gdeltproject.org', url: 'https://api.gdeltproject.org/robots.txt' }]);
const NO_ROBOTS = { statusCode: 404, headers: { 'content-type': 'text/html' }, body: '<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1></body></html>', error: '' };
const r0 = m.afterRobots({ state: p0.state, now: NOW, answers: [NO_ROBOTS] });
const reqOf = (id) => r0.requests.find((x) => x.id === id);
check('T-B-G1-03 the same Rome day reads it no more', m.planRun({ state: r0.state, now: '2026-11-20T22:30:00Z' }).robots, []);
// T17: 23:30 UTC of 20 November is 00:30 of 21 November in Rome.
check('T-B-G1-03 T17 a new Rome day reads it again, even before the UTC day changes', m.planRun({ state: r0.state, now: '2026-11-20T23:30:00Z' }).robots.length, 1);
const stoppedState = JSON.parse(JSON.stringify(r0.state));
stoppedState.host.stopped = { at: NOW, reason: 'HTTP 403' };
check('T-B-G1-03 a stopped host is not read', m.planRun({ state: stoppedState, now: '2026-11-21T00:05:00Z' }).robots, []);
check('now must be a UTC instant', thrown(() => m.planRun({ state: undefined, now: '2026-11-20 00:05' })), 'now must be a UTC instant');

/* ----- T-B-G1-04 robots.txt -------------------------------------------------- */

console.log('T-B-G1-04 the answer to robots.txt');
const rob = (a) => m.afterRobots({ state: p0.state, now: NOW, answers: [a] });
check('T-B-G1-04 404: no robots.txt, the host is allowed and the run has its searches',
  [r0.events[0].outcome, r0.events[0].reason, r0.requests.length], ['allowed', 'no robots.txt (HTTP 404)', 13]);
check('T-B-G1-04 410 is no robots.txt too', rob({ statusCode: 410, headers: {}, body: '' }).requests.length, 13);
check('T-B-G1-04 rules that allow the search path', rob({ statusCode: 200, headers: { 'content-type': 'text/plain' }, body: 'User-agent: *\nDisallow: /data/\n' }).requests.length, 13);
const dis = rob({ statusCode: 200, headers: { 'content-type': 'text/plain' }, body: 'User-agent: *\nDisallow: /api/\n' });
check('T-B-G1-04 rules that disallow it stop the host', [dis.requests.length, dis.state.host.stopped.reason, dis.stopped_now.length], [0, 'robots.txt disallows the search', 1]);
check('T-B-G1-04 a group of AI agents that disallows it applies to us too',
  rob({ statusCode: 200, headers: {}, body: 'User-agent: *\nAllow: /\n\nUser-agent: ClaudeBot\nDisallow: /\n' }).state.host.stopped.reason, 'robots.txt disallows the search');
check('T-B-G1-04 an HTML page where the rules should be stops it',
  rob({ statusCode: 200, headers: { 'content-type': 'text/plain' }, body: '<!DOCTYPE html><html><body>pagina</body></html>' }).state.host.stopped.reason,
  'robots.txt unreadable: an HTML page instead of the rules');
check('T-B-G1-04 403 and 401 stop it', [403, 401].map((c) => rob({ statusCode: c, headers: {}, body: '' }).state.host.stopped.reason),
  ['robots.txt: HTTP 403', 'robots.txt: HTTP 401']);
const r429 = rob({ statusCode: 429, headers: {}, body: 'Please limit requests to one every 5 seconds.' });
check('T-B-G1-04 T-B-G1-11 a 429 to robots.txt ends the run without stopping the host (owner, 20 November 2026)',
  [r429.events[0].outcome, r429.events[0].reason, r429.requests.length, r429.state.host.stopped, r429.stopped_now, r429.state.host.throttled_run],
  ['throttled', 'robots.txt: HTTP 429', 0, null, [], NOW]);
const movedIn = rob({ statusCode: 301, headers: { location: '/robots.txt?x=1' }, body: '' });
check('T-B-G1-04 a move within the host leaves the host unread this run', [movedIn.events[0].outcome, movedIn.requests.length, movedIn.state.host.stopped], ['moved', 0, null]);
check('T-B-G1-04 a redirect to another host stops it', rob({ statusCode: 302, headers: { location: 'https://altro-inventato.example/robots.txt' }, body: '' }).state.host.stopped.reason,
  'robots.txt: redirect to https://altro-inventato.example/robots.txt');
const err500 = rob({ statusCode: 503, headers: {}, body: '' });
check('T-B-G1-04 T-B-G1-12 a server error leaves it unread in this run, for the close to count', [err500.events[0].outcome, err500.requests.length, err500.events[0].server_error,
  err500.state.host.unread_run, err500.state.host.stopped], ['error', 0, true, NOW, null]);
const tOut = rob({ statusCode: null, headers: {}, body: '', error: 'timeout of 60000ms exceeded' });
check('T-B-G1-04 T-B-G1-12 no answer at all counts the same', [tOut.events[0].reason, tOut.events[0].server_error], ['robots.txt: timeout of 60000ms exceeded', true]);
check('T-B-G1-04 a crawl delay longer than the pause becomes the pause',
  rob({ statusCode: 200, headers: {}, body: 'User-agent: *\nCrawl-delay: 30\n' }).requests[0].wait_ms, 30000);
check('T-B-G1-04 the pause is never shorter than PAUSE_MS', [m.PAUSE_MS, r0.requests[0].wait_ms], [10000, 10000]);
check('T-B-G1-04 a robots.txt read earlier today keeps the host allowed', m.afterRobots({ state: r0.state, now: '2026-11-20T02:37:00Z', answers: [] }).requests.length, 13);

/* ----- T-B-G1-05 the windows ------------------------------------------------- */

console.log('T-B-G1-05 the windows of the searches');
const byId = (list, id) => list.find((x) => x.id === id);
check('T-B-G1-05 a first window starts where the measure starts and ends a step of the service behind the run',
  [reqOf('pagina:acilia').from, reqOf('pagina:acilia').until, reqOf('pagina:acilia').lost_from, m.START_UTC], ['2026-11-19T21:00:00Z', '2026-11-19T23:45:00Z', null, '2026-11-19T21:00:00Z']);
check('T-B-G1-05 a search never read keeps the start of the measure, run after run',
  [byId(m.windows(r0.state, '2026-11-20T10:37:00.000Z', 10000), 'testata:ansa.it').from, byId(m.windows(r0.state, '2026-11-20T10:37:00.000Z', 10000), 'testata:ansa.it').until],
  ['2026-11-19T21:00:00Z', '2026-11-20T10:15:00Z']);
const never = byId(m.windows(r0.state, '2026-11-21T02:37:00.000Z', 10000), 'pagina:prati');
check('T-B-G1-05 a search never read for more than a day names the part over a day', [never.from, never.until, never.lost_from],
  ['2026-11-20T02:15:00Z', '2026-11-21T02:15:00Z', '2026-11-19T21:00:00Z']);
const after = JSON.parse(JSON.stringify(r0.state));
after.until['pagina:acilia'] = '2026-11-19T23:45:00Z';
const w2 = byId(m.windows(after, '2026-11-20T02:37:00.000Z', 10000), 'pagina:acilia');
check('T-B-G1-05 the next window starts where the last one read ended', [w2.from, w2.until], ['2026-11-19T23:45:00Z', '2026-11-20T02:15:00Z']);
const late = JSON.parse(JSON.stringify(r0.state));
late.until['pagina:acilia'] = '2026-11-17T23:45:00Z';
const w3 = byId(m.windows(late, '2026-11-20T02:37:00.000Z', 10000), 'pagina:acilia');
check('T-B-G1-05 a window longer than a day keeps its last day and names the part left out', [w3.from, w3.until, w3.lost_from],
  ['2026-11-19T02:15:00Z', '2026-11-20T02:15:00Z', '2026-11-17T23:45:00Z']);
const same = JSON.parse(JSON.stringify(r0.state));
for (const q of S) same.until[q.id] = '2026-11-20T02:15:00Z';
check('T-B-G1-05 a search already read to the end of the window is not asked', m.windows(same, '2026-11-20T02:37:00.000Z', 10000).length, 0);
const nearEnd = JSON.parse(JSON.stringify(r0.state));
for (const q of S) nearEnd.until[q.id] = '2026-12-03T21:45:00Z';
const w4 = m.windows(nearEnd, '2026-12-04T01:37:00.000Z', 10000);
check('T-B-G1-05 no window goes past the end of the measure', [w4.length, w4[0].until], [13, m.END_UTC]);
const over = JSON.parse(JSON.stringify(r0.state));
for (const q of S) over.until[q.id] = m.END_UTC;
const pOver = m.planRun({ state: over, now: '2026-12-04T03:37:00.000Z' });
check('T-B-G1-05 T-B-G1-13 after the end a run asks nothing, not even robots.txt', [pOver.ended, pOver.robots, m.afterRobots({ state: over, now: '2026-12-04T03:37:00.000Z', answers: [] }).requests],
  [true, [], []]);
const lastRun = m.planRun({ state: nearEnd, now: '2026-12-04T00:37:00.000Z' });
check('T-B-G1-05 T-B-G1-13 the run that closes the last window comes before ASK_UNTIL_UTC', [lastRun.ended, byId(m.afterRobots({ state: nearEnd, now: '2026-12-04T00:37:00.000Z', answers: [NO_ROBOTS] }).requests, 'pagina:acilia').until],
  [false, m.END_UTC]);
const stuck = JSON.parse(JSON.stringify(nearEnd));
stuck.until['pagina:acilia'] = '2026-12-01T00:00:00Z';
check('T-B-G1-05 T-B-G1-13 a window that could never be read is not asked after the end', [m.planRun({ state: stuck, now: '2027-01-15T10:37:00.000Z' }).ended,
  m.planRun({ state: stuck, now: '2027-01-15T10:37:00.000Z' }).robots, m.afterRobots({ state: stuck, now: '2027-01-15T10:37:00.000Z', answers: [NO_ROBOTS] }).requests], [true, [], []]);
check('T-B-G1-05 the end is midnight of 4 December 2026 in Rome', new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', dateStyle: 'short', timeStyle: 'short' }).format(new Date(m.END_UTC)),
  '04/12/26, 00:00');

/* ----- T-B-G1-06 before each search ------------------------------------------ */

console.log('T-B-G1-06 a search is not sent once the host has stopped');
const req = reqOf('pagina:acilia');
check('T-B-G1-06 a host that answers is asked', m.beforeRequest({ state: r0.state, request: req }).skip, false);
const sk = m.beforeRequest({ state: stoppedState, request: req });
check('T-B-G1-06 a stopped host is not asked, and the search says why', [sk.skip, sk.result.outcome, sk.result.reason, sk.result.id], [true, 'skipped', 'host stopped: HTTP 403', 'pagina:acilia']);

/* ----- T-B-G1-07 one answer -------------------------------------------------- */

console.log('T-B-G1-07 one answer: the stops, the rows, the counts');
const json = (doc, extra) => Object.assign({ statusCode: 200, headers: { 'content-type': 'application/json; charset=utf-8' }, body: JSON.stringify(doc), error: '' }, extra);
const art = (url, title, seendate) => ({ url, url_mobile: '', title, seendate, socialimage: 'https://img.example/x.jpg', domain: 'x', language: 'Italian', sourcecountry: 'Italy' });
const ans = (request, answer, state) => m.afterAnswer({ state: state || r0.state, now: NOW, request, answer });
const s429 = ans(req, { statusCode: 429, headers: { 'content-type': 'text/html' }, body: 'Please limit requests to one every 5 seconds.', error: '' });
check('T-B-G1-07 T-B-G1-11 a 429 ends the run and stops nothing (owner, 20 November 2026)',
  [s429.result.outcome, s429.result.reason, s429.state.host.stopped, s429.state.host.throttled_run], ['throttled', 'HTTP 429', null, NOW]);
const skip429 = m.beforeRequest({ state: s429.state, request: r0.requests[1] });
check('T-B-G1-07 T-B-G1-11 the next search of the run is then not sent, and says why', [skip429.skip, skip429.result.reason], [true, 'HTTP 429 earlier in this run']);
check('T-B-G1-07 T-B-G1-11 a search of another run is sent', m.beforeRequest({ state: s429.state, request: Object.assign({}, r0.requests[1], { run: '2026-11-20T02:37:00.000Z' }) }).skip, false);
const s403 = ans(req, { statusCode: 403, headers: {}, body: '' });
check('T-B-G1-07 T-B-G1-11 any other block signal stops the host at once', [s403.result.outcome, s403.state.host.stopped.reason], ['stopped', 'HTTP 403']);
check('T-B-G1-07 403 and 401 stop it too', [403, 401].map((c) => ans(req, { statusCode: c, headers: {}, body: '' }).result.outcome), ['stopped', 'stopped']);
check('T-B-G1-07 a challenge page served with 200 stops it',
  ans(req, { statusCode: 200, headers: { 'content-type': 'text/html' }, body: '<html><div class="g-recaptcha"></div></html>' }).result.reason, 'captcha');
check('T-B-G1-07 a redirect to another host stops it',
  ans(req, { statusCode: 302, headers: { location: 'https://accesso-inventato.example/login' }, body: '' }).result.outcome, 'stopped');
const mv = ans(req, { statusCode: 301, headers: { location: '/api/v2/doc/doc?x=1' }, body: '' });
check('T-B-G1-07 a move within the host is recorded, not a stop, and the window stays', [mv.result.outcome, mv.state.host.stopped], ['moved', null]);
const s502 = ans(req, { statusCode: 502, headers: {}, body: '' });
const skip502 = m.beforeRequest({ state: s502.state, request: r0.requests[1] });
check('T-B-G1-07 T-B-G1-12 a server error leaves the host unread for the rest of its run, and stops nothing',
  [s502.result.outcome, s502.result.server_error, s502.state.host.stopped, skip502.skip, skip502.result.reason], ['error', true, null, true, 'host not read in this run: HTTP 502']);
const s404 = ans(req, { statusCode: 404, headers: {}, body: '' });
check('T-B-G1-07 another error of a search is recorded and the run goes on', [s404.result.outcome, s404.result.server_error, m.beforeRequest({ state: s404.state, request: r0.requests[1] }).skip],
  ['error', undefined, false]);
const notJson = ans(req, { statusCode: 200, headers: { 'content-type': 'text/html' }, body: 'Your search contained an invented error.\n' });
check('T-B-G1-07 a sentence of the service instead of JSON is unreadable, with its first words', [notJson.result.outcome, notJson.result.excerpt, notJson.state.host.stopped],
  ['unreadable', 'Your search contained an invented error.', null]);
check('T-B-G1-07 a list of articles that is not a list is unreadable', ans(req, json({ articles: {} })).result.outcome, 'unreadable');
const empty = ans(req, json({}));
check('T-B-G1-07 {} is a search with no article', [empty.result.outcome, empty.result.returned, empty.result.kept, empty.result.rows], ['read', 0, 0, []]);
const page = ans(reqOf('pagina:centocelle'), json({ articles: [
  art('https://www.romatoday.it/cronaca/fatto-inventato-1.html', '  Un   titolo inventato ', '20261119T230000Z'),
  art('https://roma.corriere.it/notizie/fatto-inventato-2.shtml', 'Altro titolo inventato', '20261119T231500Z'),
  art('https://sito-inventato.example/3', '', '20261119T220000Z'),
  art('https://www.romatoday.it/cronaca/fatto-inventato-1.html', 'Un titolo inventato', '20261119T230000Z'),
  art('https://www.romatoday.it/vecchio-inventato.html', 'Fuori finestra', '20261119T205959Z'),
  art('https://www.romatoday.it/al-limite-inventato.html', 'Al limite', '20261119T234500Z'),
  art('ftp://sito-inventato.example/4', 'Senza link', '20261119T230000Z'),
  art('https://sito-inventato.example/5', 'Senza ora', '2026-11-19 23:00'),
] }));
check('T-B-G1-07 the counts of a page search', [page.result.outcome, page.result.returned, page.result.kept, page.result.outside_window, page.result.malformed, page.result.without_title, page.result.truncated],
  ['read', 8, 3, 2, 2, 1, false]);
check('T-B-G1-07 a row has the link, the title, GDELT\'s hour and the site, and nothing else', page.result.rows,
  [{ url: 'https://www.romatoday.it/cronaca/fatto-inventato-1.html', title: 'Un titolo inventato', seen_at_utc: '2026-11-19T23:00:00Z', source_id: 'romatoday.it' },
    { url: 'https://roma.corriere.it/notizie/fatto-inventato-2.shtml', title: 'Altro titolo inventato', seen_at_utc: '2026-11-19T23:15:00Z', source_id: 'roma.corriere.it' },
    { url: 'https://sito-inventato.example/3', title: '', seen_at_utc: '2026-11-19T22:00:00Z', source_id: 'sito-inventato.example' }]);
check('T-B-G1-07 the rows of a page search counted by outlet', page.result.per_outlet, { 'romatoday.it': 1, 'corriere.it': 1, other: 1 });
const outlet = ans(reqOf('testata:today.it'), json({ articles: [
  art('https://www.today.it/attualita/inventato.html', 'Titolo inventato', '20261119T230000Z'),
  art('https://www.romatoday.it/cronaca/inventato.html', 'Titolo inventato', '20261119T230000Z'),
] }));
check('T-B-G1-07 an outlet search keeps its own site and counts another', [outlet.result.kept, outlet.result.other_site, outlet.result.rows[0].source_id], [1, 1, 'today.it']);
check('T-B-G1-07 a subdomain is its outlet', ans(reqOf('testata:corriere.it'), json({ articles: [art('https://roma.corriere.it/x-inventato', 't', '20261119T230000Z')] })).result.kept, 1);
const many = [];
for (let i = 0; i < m.MAX_RECORDS; i += 1) many.push(art(`https://www.ansa.it/inventato/${i}.html`, `t${i}`, '20261119T230000Z'));
check('T-B-G1-07 an answer of MAX_RECORDS articles is marked as cut', ans(reqOf('testata:ansa.it'), json({ articles: many })).result.truncated, true);
check('T-B-G1-07 an answer for an unknown search is an error', /unknown search/.test(thrown(() => ans({ id: 'testata:altro.it', from: req.from, until: req.until, url: req.url }, json({ articles: [art('https://altro.it/x', 't', '20261119T230000Z')] }))) || ''), true);

/* ----- T-B-G1-08 the close of a run ------------------------------------------ */

console.log('T-B-G1-08 the close: windows, rows file, register, alert');
const outcomes = [page.result, outlet.result, notJson.result, empty.result,
  Object.assign({}, s403.result, { id: 'testata:leggo.it' }), sk.result && Object.assign({}, sk.result, { id: 'testata:agenzianova.com' })];
const dupe = ans(reqOf('testata:romatoday.it'), json({ articles: [art('https://www.romatoday.it/cronaca/fatto-inventato-1.html', 'Un titolo inventato', '20261119T230000Z')] })).result;
outcomes.push(dupe);
const fixedResults = outcomes.map((r, i) => (i === 2 ? Object.assign({}, r, { id: 'testata:ansa.it' }) : i === 3 ? Object.assign({}, r, { id: 'testata:repubblica.it' }) : r));
const closed = m.closeRun({ state: r0.state, now: '2026-11-20T00:11:00.000Z', started_at: NOW, results: fixedResults, robots_events: r0.events, robots_stopped: [], ended: false });
check('T-B-G1-08 only the searches read move their window',
  Object.keys(closed.state.until).sort(), ['pagina:centocelle', 'testata:repubblica.it', 'testata:romatoday.it', 'testata:today.it']);
check('T-B-G1-08 one row per link, with every search that found it, by hour', closed.rows.map((r) => [r.seen_at_utc, r.source_id, r.searches]),
  [['2026-11-19T22:00:00Z', 'sito-inventato.example', ['pagina:centocelle']],
    ['2026-11-19T23:00:00Z', 'romatoday.it', ['pagina:centocelle', 'testata:romatoday.it']],
    ['2026-11-19T23:00:00Z', 'today.it', ['testata:today.it']],
    ['2026-11-19T23:15:00Z', 'roma.corriere.it', ['pagina:centocelle']]]);
check('T-B-G1-08 the files of the run are named by its start', [closed.rows_file_name, closed.log_file_name, closed.alert_file_name],
  ['gdelt_righe_20261120T000512Z.json', 'gdelt_20261120T000512Z.json', 'AVVISO_gdelt_20261120T000512Z.json']);
check('T-B-G1-08 the register names the flow, the spend and every outcome, and carries no title',
  [closed.log.workflow, closed.log.spend_eur, closed.log.requests.map((r) => r.outcome), closed.log.requests.some((r) => 'rows' in r), JSON.stringify(closed.log).includes('titolo inventato')],
  ['staging_B_gdelt_misura', 0, ['read', 'read', 'unreadable', 'read', 'stopped', 'skipped', 'read'], false, false]);
check('T-B-G1-08 the register says where the measure ends and the stop', [closed.log.measure_end, closed.log.stopped_now, closed.log.rows],
  [m.END_UTC, [{ source_id: 'api.gdeltproject.org', reason: 'HTTP 403' }], 4]);
const quiet = m.closeRun({ state: r0.state, now: '2026-11-20T00:11:00.000Z', started_at: NOW, results: [empty.result], robots_events: [], robots_stopped: [] });
check('T-B-G1-08 a run without stops and without rows writes only its register', [quiet.rows_file_name, quiet.alert_file_name, quiet.log_file_name],
  [null, null, 'gdelt_20261120T000512Z.json']);
const cut = byId(m.windows(r0.state, '2026-11-21T02:37:00.000Z', 10000), 'pagina:prati');
const cutClose = m.closeRun({ state: r0.state, now: '2026-11-21T02:40:00.000Z', started_at: '2026-11-21T02:37:00.000Z',
  results: [Object.assign({}, m.beforeRequest({ state: stoppedState, request: cut }).result)], robots_events: [], robots_stopped: [] });
check('T-B-G1-08 a part left out of a window is named in the register once: the start moves past it, read or not',
  [cutClose.log.requests[0].lost_from, cutClose.log.requests[0].outcome, cutClose.state.until['pagina:prati'],
    byId(m.windows(cutClose.state, '2026-11-21T02:37:00.000Z', 10000), 'pagina:prati').lost_from],
  ['2026-11-19T21:00:00Z', 'skipped', '2026-11-20T02:15:00Z', null]);
check('T-B-G1-08 a stop at robots.txt makes the alert too',
  m.closeRun({ state: dis.state, now: NOW, started_at: NOW, results: [], robots_events: dis.events, robots_stopped: dis.stopped_now }).alert_file_name, 'AVVISO_gdelt_20261120T000512Z.json');
check('T-B-G1-08 an outcome of an unknown search is an error',
  /unknown search/.test(thrown(() => m.closeRun({ state: r0.state, now: NOW, started_at: NOW, results: [{ id: 'x', outcome: 'read' }] })) || ''), true);

/* ----- T-B-G1-09 the n8n adapter --------------------------------------------- */

console.log('T-B-G1-09 n8n adapter — exact committed file, stubbed $input/$json/$getWorkflowStaticData');
const src = fs.readFileSync(FILE, 'utf8');
const store = {};
function runNode(j) {
  const item = { json: j };
  // n8n's Code node has neither URL nor URLSearchParams: the adapter runs without them.
  return new Function('$input', '$json', 'require', '$getWorkflowStaticData', 'URL', 'URLSearchParams', src)(
    { item }, j, require, () => store, undefined, undefined);
}
{
  store.news_gdelt_pending = { leftover: true };
  const p = runNode({ stage: 'plan', now: NOW });
  check('T-B-G1-09 T-B-G1-14 plan: robots.txt to read, the state saved, the state a failed run left aside dropped',
    [p.json.robots.length, p.json.ended, store.news_gdelt.host.robots_day, 'news_gdelt_pending' in store], [1, false, null, false]);
  const r = runNode({ stage: 'robots', now: NOW, answers: [NO_ROBOTS] });
  check('T-B-G1-09 robots: the searches, the answers dropped', [r.json.requests.length, r.json.answers, r.json.requests[0].stage, r.json.requests[0].run], [13, undefined, 'before', NOW]);
  const acilia = r.json.requests.find((x) => x.id === 'pagina:acilia');
  const b = runNode(Object.assign({}, acilia));
  check('T-B-G1-09 before: a search to send keeps its request', [b.json.skip, b.json.url === acilia.url], [false, true]);
  const a = runNode({ stage: 'answer', now: NOW, request: b.json, statusCode: 200, headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ articles: [art('https://www.romatoday.it/inventato.html', 'Titolo inventato', '20261119T230000Z')] }), error: '' });
  check('T-B-G1-09 answer: the outcome only, the body dropped', [a.json.outcome, a.json.kept, 'body' in a.json, 'request' in a.json], ['read', 1, false, false]);
  const other = r.json.requests.filter((x) => x.id !== 'pagina:acilia');
  const stop = runNode({ stage: 'answer', now: NOW, request: other[0], statusCode: 429, headers: {}, body: '', error: '' });
  const b2 = runNode(Object.assign({}, other[1]));
  check('T-B-G1-09 a 429 persists between nodes: the next search of the run is skipped', [stop.json.outcome, b2.json.skip, b2.json.outcome, 'url' in b2.json], ['throttled', true, 'skipped', false]);
  const c = runNode({ stage: 'close', now: '2026-11-20T00:11:00.000Z', started_at: NOW, results: [a.json, stop.json, b2.json], robots_events: r.json.robots_events,
    robots_stopped: [], ended: false, workflow_version: 'prova-inventata' });
  check('T-B-G1-09 close: the files of the run, the results dropped', [c.json.rows.length, c.json.rows_file_name, c.json.log_file_name, c.json.alert_file_name, c.json.results, c.json.log.workflow_version],
    [1, 'gdelt_righe_20261120T000512Z.json', 'gdelt_20261120T000512Z.json', null, undefined, 'prova-inventata']);
  check('T-B-G1-09 T-B-G1-14 close: the state of the run waits apart, the flow keeps its own until the files are written',
    [store.news_gdelt.until, store.news_gdelt_pending.until, store.news_gdelt_pending.host.throttled_runs], [{}, { 'pagina:acilia': '2026-11-19T23:45:00Z' }, 1]);
  const k = runNode({ stage: 'commit' });
  check('T-B-G1-09 T-B-G1-14 commit: after the files, the state of the run is the state of the flow',
    [k.json.committed, store.news_gdelt.until, store.news_gdelt.host.throttled_runs, store.news_gdelt.host.throttled_run, 'news_gdelt_pending' in store],
    [true, { 'pagina:acilia': '2026-11-19T23:45:00Z' }, 1, null, false]);
  store.news_gdelt.host.throttled_runs = m.THROTTLED_RUNS_TO_STOP - 1;
  const sixthClose = runNode({ stage: 'close', now: '2026-11-20T02:40:00.000Z', started_at: '2026-11-20T02:37:00.000Z',
    results: [{ id: 'pagina:prati', from: m.START_UTC, until: '2026-11-20T02:15:00Z', lost_from: null, status: 429, outcome: 'throttled', reason: 'HTTP 429' }],
    robots_events: [], robots_stopped: [], ended: false, workflow_version: 'prova-inventata' });
  check('T-B-G1-09 T-B-G1-14 a stop decided at the close holds at once, before the files and the commit',
    [sixthClose.json.alert_file_name, store.news_gdelt.host.stopped && store.news_gdelt.host.stopped.reason, store.news_gdelt.host.throttled_runs, 'news_gdelt_pending' in store],
    ['AVVISO_gdelt_20261120T023700Z.json', 'HTTP 429 in 6 runs in a row', 5, true]);
  delete store.news_gdelt_pending;
  check('T-B-G1-09 an unknown stage is a workflow error', /unknown stage/.test(thrown(() => runNode({ stage: 'altro' })) || ''), true);
}
check('T-B-G1-09 the node does not use the URL global, which n8n does not have', /new URL\(/.test(src), false);

/* ----- T-B-G1-10 the flow exported ------------------------------------------- */

console.log('T-B-G1-10 staging_B_gdelt_misura and staging_B_avviso as exported');
const W = JSON.parse(fs.readFileSync(path.join(ROOT, 'workflows', 'staging_B_gdelt_misura.json'), 'utf8'));
const A = JSON.parse(fs.readFileSync(path.join(ROOT, 'workflows', 'staging_B_avviso.json'), 'utf8'));
const node = (w, name) => w.nodes.find((n) => n.name === name);
const to = (w, name, out) => (((w.connections[name] || {}).main || [])[out || 0] || []).map((x) => x.node).join();
check('T-B-G1-10 every Code node of the flow is news-gdelt.js', W.nodes.filter((n) => n.type === 'n8n-nodes-base.code').map((n) => [n.name, n.parameters.jsCode === src]),
  [['Piano', true], ['Dopo robots', true], ['Prima', true], ['Dopo la risposta', true], ['Chiusura', true], ['Conferma', true]]);
const trig = W.nodes.filter((n) => /Trigger$|webhook$/i.test(n.type));
check('T-B-G1-10 one trigger, the schedule of the contract, and no webhook', trig.map((n) => [n.type, n.parameters.rule.interval[0].expression]),
  [['n8n-nodes-base.scheduleTrigger', '37 1-23/2 * * *']]);
check('T-B-G1-10 the settings: Rome time, no data of a successful run, the error flow of B',
  [W.settings.timezone, W.settings.saveDataSuccessExecution, W.settings.saveManualExecutions, W.settings.errorWorkflow], ['Europe/Rome', 'none', false, A.id]);
const inizio = Object.fromEntries(node(W, 'Inizio').parameters.assignments.assignments.map((x) => [x.name, x.value]));
const chiusura = Object.fromEntries(node(W, 'Prepara chiusura').parameters.assignments.assignments.map((x) => [x.name, x.value]));
check('T-B-G1-10 the version of the flow reaches the register (WORKSTREAM_A, section 8, point 9)',
  [typeof inizio.workflow_version === 'string' && inizio.workflow_version.length > 0, chiusura.workflow_version], [true, "={{ $('Inizio').first().json.workflow_version }}"]);
const https = W.nodes.filter((n) => n.type === 'n8n-nodes-base.httpRequest');
check('T-B-G1-10 every request declares the user agent, follows no redirect and keeps the answer whatever its status',
  https.map((n) => [n.name, n.parameters.headerParameters.parameters[0].value === m.USER_AGENT, n.parameters.options.redirect.redirect.followRedirects,
    n.parameters.options.response.response.neverError, n.onError, n.retryOnFail || false]),
  [['robots.txt', true, false, true, 'continueRegularOutput', false], ['Ricerca', true, false, true, 'continueRegularOutput', false]]);
check('T-B-G1-10 the loop: each search goes through «Prima», and only one to send waits and is sent',
  [to(W, 'Ricerche', 1), to(W, 'Prima'), to(W, 'Da chiedere?', 0), to(W, 'Da chiedere?', 1), to(W, 'Attesa'), to(W, 'Ricerca'), to(W, 'Risposta'), to(W, 'Dopo la risposta')],
  ['Prima', 'Da chiedere?', 'Attesa', 'Ricerche', 'Ricerca', 'Risposta', 'Dopo la risposta', 'Ricerche']);
check('T-B-G1-10 «Da chiedere?» sends a search only when «Prima» says so', node(W, 'Da chiedere?').parameters.conditions.conditions[0].leftValue, '={{ $json.skip === false }}');
check('T-B-G1-10 the pause is the one the code gives', node(W, 'Attesa').parameters.amount, '={{ $json.wait_ms / 1000 }}');
check('T-B-G1-10 T-B-G1-14 the files are written one after the other, rows, register, alert, and only then the state is committed',
  [to(W, 'Ricerche', 0), to(W, 'Esiti'), to(W, 'Prepara chiusura'), to(W, 'Chiusura'), to(W, 'Righe?', 0), to(W, 'Righe?', 1), to(W, 'Salva righe'),
    to(W, 'Registro?', 0), to(W, 'Registro?', 1), to(W, 'Salva registro'), to(W, 'Avviso?', 0), to(W, 'Avviso?', 1), to(W, 'Salva avviso'), to(W, 'Prepara conferma')],
  ['Esiti', 'Prepara chiusura', 'Chiusura', 'Righe?', 'Testo righe', 'Registro?', 'Registro?', 'Testo registro', 'Avviso?', 'Avviso?', 'Testo avviso',
    'Prepara conferma', 'Prepara conferma', 'Conferma']);
check('T-B-G1-10 T-B-G1-14 the files read what «Chiusura» gave, whatever node comes before',
  ['Righe?', 'Registro?', 'Avviso?'].map((n) => node(W, n).parameters.conditions.conditions[0].leftValue),
  ["={{ $('Chiusura').first().json.rows_file_name }}", "={{ $('Chiusura').first().json.log_file_name }}", "={{ $('Chiusura').first().json.alert_file_name }}"]);
const drives = W.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive').concat(A.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive'));
check('T-B-G1-10 every file goes to B Notizie/letture/, with the Google Drive credential', drives.map((n) => [n.name, n.parameters.folderId.value, n.credentials.googleDriveOAuth2Api.id]),
  [['Salva righe', '1CPtWeMWYd3LthCyocObAAIegVyW5iiJ0', '7nJkjb7aldPHyXv4'], ['Salva registro', '1CPtWeMWYd3LthCyocObAAIegVyW5iiJ0', '7nJkjb7aldPHyXv4'],
    ['Salva avviso', '1CPtWeMWYd3LthCyocObAAIegVyW5iiJ0', '7nJkjb7aldPHyXv4'], ['Salva avviso', '1CPtWeMWYd3LthCyocObAAIegVyW5iiJ0', '7nJkjb7aldPHyXv4']]);
check('T-B-G1-10 T-B-G1-14 every Drive node of the flow retries as the B collection does',
  W.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive').map((n) => [n.retryOnFail, n.maxTries, n.waitBetweenTries]), [[true, 5, 5000], [true, 5, 5000], [true, 5, 5000]]);
check('T-B-G1-10 the error flow of B starts from an error and writes its alert', [A.name, A.nodes[0].type, to(A, 'Errore'), to(A, 'Avviso'), to(A, 'File avviso')],
  ['staging_B_avviso', 'n8n-nodes-base.errorTrigger', 'Avviso', 'File avviso', 'Salva avviso']);
check('T-B-G1-10 the error flow is exported on: n8n does not call an error flow that is off', A.active, true);
check('T-B-G1-10 the exports carry the id and the versionId n8n gave them', [typeof W.id, /^[0-9a-f-]{36}$/.test(W.versionId), /^[0-9a-f-]{36}$/.test(A.versionId)], ['string', true, true]);

/* ----- runs one after the other ----------------------------------------------- */

const runAt = (k) => new Date(Date.parse('2026-11-20T00:37:00.000Z') + k * 2 * 3600 * 1000).toISOString();
/** One run: robots.txt already read today unless given; every search sent answers `answer` (a status,
 *  or an answer object). */
function oneRun(state, k, answer, robotsAnswer) {
  const now = runAt(k);
  const ro = m.afterRobots({ state, now, answers: robotsAnswer ? [robotsAnswer] : [] });
  let st = ro.state;
  const results = [];
  for (const q of ro.requests) {
    const b = m.beforeRequest({ state: st, request: q });
    st = b.state;
    if (b.skip) { results.push(b.result); continue; }
    const res = typeof answer === 'object' ? answer : answer === 200 ? json({}) : { statusCode: answer, headers: {}, body: '' };
    const a = m.afterAnswer({ state: st, now, request: q, answer: res });
    st = a.state;
    results.push(a.result);
  }
  return m.closeRun({ state: st, now, started_at: now, results, robots_events: ro.events, robots_stopped: ro.stopped_now });
}

/* ----- T-B-G1-11 the runs in a row with a 429 --------------------------------- */

console.log('T-B-G1-11 a 429 ends the run; six runs in a row with one stop the host (DEC-045, the owner, 20 November 2026)');
let run = { state: r0.state };
for (let k = 0; k < m.THROTTLED_RUNS_TO_STOP - 1; k += 1) run = oneRun(run.state, k, 429);
check('T-B-G1-11 five runs in a row with a 429: counted, the host still asks, no alert',
  [run.state.host.throttled_runs, run.state.host.stopped, run.alert_file_name, run.log.throttled, run.log.throttled_runs, run.log.requests.filter((x) => x.outcome === 'throttled').length,
    run.log.requests.filter((x) => x.outcome === 'skipped').length], [5, null, null, true, 5, 1, 12]);
check('T-B-G1-11 a throttled search keeps its window: the next run asks it from where it was never read, the start of the measure',
  byId(m.windows(run.state, runAt(5), 10000), 'pagina:acilia').from, m.START_UTC);
check('T-B-G1-11 the first search turns: five runs, five searches met the 429 first',
  new Set([0, 1, 2, 3, 4].map((k) => m.searchOrder(runAt(k))[0].id)).size, 5);
const reset = oneRun(run.state, 5, 200);
check('T-B-G1-11 a run that asks and has no 429 sets the count back to zero', [reset.state.host.throttled_runs, reset.log.throttled, Object.keys(reset.state.until).length], [0, false, 13]);
check('T-B-G1-11 the windows that the 429s left unread are all read, from the start of the measure', reset.log.requests.map((x) => [x.outcome, x.from]).filter((x) => x[0] !== 'read' || x[1] !== m.START_UTC), []);
const idle = m.closeRun({ state: run.state, now: runAt(5), started_at: runAt(5), results: [], robots_events: [], robots_stopped: [] });
check('T-B-G1-11 a run that asks nothing has no 429 either: it breaks the series', idle.state.host.throttled_runs, 0);
const sixth = oneRun(run.state, 5, 429);
check('T-B-G1-11 the sixth run in a row with a 429 stops the host, with the alert',
  [sixth.state.host.stopped.reason, sixth.log.stopped_now, sixth.alert_file_name, sixth.alert.stopped_now],
  ['HTTP 429 in 6 runs in a row', [{ source_id: 'api.gdeltproject.org', reason: 'HTTP 429 in 6 runs in a row' }], `AVVISO_gdelt_${runAt(5).slice(0, 19).replace(/[-:]/g, '')}Z.json`,
    [{ source_id: 'api.gdeltproject.org', reason: 'HTTP 429 in 6 runs in a row' }]]);
check('T-B-G1-11 after the stop no run asks anything', [m.planRun({ state: sixth.state, now: runAt(6) }).robots, m.afterRobots({ state: sixth.state, now: runAt(6), answers: [] }).requests], [[], []]);
const viaRobots = oneRun(run.state, 5, 200, { statusCode: 429, headers: {}, body: '' });
check('T-B-G1-11 a 429 to robots.txt counts as a run with a 429', [viaRobots.state.host.stopped && viaRobots.state.host.stopped.reason, viaRobots.log.requests.length],
  ['HTTP 429 in 6 runs in a row', 0]);
check('T-B-G1-11 the count is THROTTLED_RUNS_TO_STOP, the owner\'s six', m.THROTTLED_RUNS_TO_STOP, 6);

/* ----- T-B-G1-12 server errors and no answer, per run -------------------------- */

console.log('T-B-G1-12 a server error or no answer leaves the host unread in its run; five runs in a row stop it (CONTRATTI 7 B, «Raccolta»)');
const e1 = oneRun(r0.state, 0, 503);
check('T-B-G1-12 a run whose first search has a 503: the host is not read in the rest of the run, not stopped, one run counted',
  [e1.state.host.stopped, e1.log.server_error, e1.log.error_runs, e1.log.requests.filter((x) => x.outcome === 'skipped').length,
    e1.log.requests.find((x) => x.outcome === 'skipped').reason], [null, true, 1, 12, 'host not read in this run: HTTP 503']);
let er = { state: r0.state };
for (let k = 0; k < m.ERRORS_TO_STOP - 1; k += 1) er = oneRun(er.state, k, { statusCode: null, headers: {}, body: '', error: 'timeout of 60000ms exceeded' });
check('T-B-G1-12 four runs in a row without an answer: counted, not stopped', [er.state.host.errors_in_row, er.state.host.stopped], [4, null]);
check('T-B-G1-12 a run that asks without a server error sets the count back to zero', oneRun(er.state, 4, 404).state.host.errors_in_row, 0);
check('T-B-G1-12 a run that asks nothing breaks the series too', m.closeRun({ state: er.state, now: runAt(4), started_at: runAt(4), results: [], robots_events: [],
  robots_stopped: [] }).state.host.errors_in_row, 0);
const fifth = oneRun(er.state, 4, 500);
check('T-B-G1-12 the fifth run in a row stops the host, with the alert', [fifth.state.host.stopped.reason, fifth.alert_file_name !== null],
  ['a server error or no answer in 5 runs in a row', true]);
const robots5xx = m.afterRobots({ state: er.state, now: runAt(4), answers: [{ statusCode: 502, headers: {}, body: '' }] });
check('T-B-G1-12 a server error to robots.txt counts the same', m.closeRun({ state: robots5xx.state, now: runAt(4), started_at: runAt(4), results: [],
  robots_events: robots5xx.events, robots_stopped: [] }).state.host.stopped.reason, 'a server error or no answer in 5 runs in a row');

/* ----- T-B-G1-13 the end of the measure ------------------------------------------ */

console.log('T-B-G1-13 after the end a run writes one notice the first time, then nothing');
const endState = JSON.parse(JSON.stringify(r0.state));
for (const q of S) endState.until[q.id] = m.END_UTC;
endState.until['testata:ansa.it'] = '2026-12-02T10:15:00Z';
const fin1 = m.closeRun({ state: endState, now: '2026-12-04T02:38:00.000Z', started_at: '2026-12-04T02:37:00.000Z', results: [], robots_events: [], robots_stopped: [], ended: true, workflow_version: 'v' });
check('T-B-G1-13 the first ended run writes only the notice, with the windows never read',
  [fin1.log_file_name, fin1.rows_file_name, fin1.alert_file_name, fin1.alert.windows_not_read, /spegne/.test(fin1.alert.avviso), fin1.state.over_notice],
  [null, null, 'AVVISO_gdelt_fine_20261204T023700Z.json', [{ id: 'testata:ansa.it', from: '2026-12-02T10:15:00Z', until: m.END_UTC }], true, '2026-12-04T02:38:00.000Z']);
const fin2 = m.closeRun({ state: fin1.state, now: '2026-12-04T04:38:00.000Z', started_at: '2026-12-04T04:37:00.000Z', results: [], robots_events: [], robots_stopped: [], ended: true });
check('T-B-G1-13 the runs after it write nothing', [fin2.log_file_name, fin2.rows_file_name, fin2.alert_file_name], [null, null, null]);
check('T-B-G1-13 the measure is over from ASK_UNTIL_UTC, two hours after its end', [m.ASK_UNTIL_UTC, Date.parse(m.ASK_UNTIL_UTC) - Date.parse(m.END_UTC)], ['2026-12-04T01:00:00Z', 2 * 3600 * 1000]);

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

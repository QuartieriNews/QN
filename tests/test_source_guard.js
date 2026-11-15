#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/source-guard.js: the hosts the channel may ask, the user
 * agent, the pause after an answer, the answers that stop a host, the streak of server errors,
 * the daily robots.txt check (docs/pilota/CONTRATTI.md, section 7, «A · Amministrazione», rows
 * Fonti and Raccolta). Cases T-A2-07, T-A2-08, T-A2-10 and T-A2-12 of docs/pilota/WORKSTREAM_A.md,
 * section 6. The n8n adapter is evaluated from the exact committed file with a fake
 * this.helpers.httpRequest and a fake setTimeout. Every answer is invented (DEC-109).
 *
 * Run:  node tests/test_source_guard.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'source-guard.js');
const g = require(FILE);
const src = fs.readFileSync(FILE, 'utf8');

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
const thrown = (fn) => { try { fn(); return null; } catch (e) { return e.message; } };

const API = 'https://api-ovp.streamcloud.it/garavot/ac104/api/v1/contents/search_frontend';
const PORTAL = 'streaming.comune.roma.it';
const MEDIA = 'ovp2-live.akamaized.net';
const NOW = '2026-11-16T10:00:00Z';
const json = (body, code) => ({ statusCode: code || 200, headers: { 'content-type': 'application/json' }, body });
const html = (body) => ({ statusCode: 200, headers: { 'content-type': 'text/html' }, body });
const outcome = (res, url, expects) => g.verdict(res, url || API, expects || 'json').outcome;

console.log('T-A2-07 — the answers that stop a RomaTV host, one per case');
for (const code of [401, 403, 429]) {
  check(`T-A2-07 HTTP ${code} stops the host`, outcome({ statusCode: code, headers: {}, body: '' }), 'block');
}
check('T-A2-07 a captcha page stops the host',
  outcome(html('<html><div class="g-recaptcha"></div></html>')), 'block');
check('T-A2-07 a sign-in page stops the host',
  outcome(html('<html><form><input type="password"></form></html>')), 'block');
check('T-A2-07 an HTML page served with 200 where the list sends data stops the host',
  g.verdict(html('<!doctype html><html><body>Mediaportal</body></html>'), API, 'json'),
  { outcome: 'block', reason: 'HTML page where the source sends data' });
check('T-A2-07 an HTML page where a playlist or a segment is expected stops the host too',
  [outcome(html('<html></html>'), `https://${MEDIA}/x/playlist.m3u8`, 'text'), outcome({ statusCode: 200, headers: { 'content-type': 'text/html' }, body: Buffer.from('x') }, `https://${MEDIA}/x/s.aac`, 'binary')],
  ['block', 'block']);
check('T-A2-07 a redirect to another host stops the host',
  g.verdict({ statusCode: 302, headers: { Location: 'https://consent.example.invalid/?continue=1' }, body: '' }, API, 'json'),
  { outcome: 'block', reason: 'redirect to another host: consent.example.invalid' });
check('T-A2-07 a redirect without a location stops the host', outcome({ statusCode: 301, headers: {}, body: '' }), 'block');
check('T-A2-07 a redirect within the host to a consent or sign-in page stops it',
  outcome({ statusCode: 302, headers: { location: '/consent?x=1' }, body: '' }), 'block');
check('T-A2-07 a redirect within the host to another path does not stop it; the entry stays unread',
  outcome({ statusCode: 302, headers: { location: '/garavot/ac104/api/v2/x' }, body: '' }), 'other');
check('T-A2-07 a server error and a request without an answer count as server errors',
  [outcome({ statusCode: 503, headers: {}, body: '' }), outcome({ error: 'ETIMEDOUT' }), outcome(null)], ['server_error', 'server_error', 'server_error']);
check('T-A2-07 a 404 is neither a block nor a server error', outcome({ statusCode: 404, headers: {}, body: '' }), 'other');
check('T-A2-07 a captcha or an anti-bot check stops the host whatever its status',
  [503, 404, 200].map((code) => outcome({ statusCode: code, headers: { 'content-type': 'text/html' }, body: '<html><script src="/cdn-cgi/challenge-platform/x.js"></script></html>' })),
  ['block', 'block', 'block']);
check('T-A2-07 a sign-in page with 400 stops the host',
  g.verdict({ statusCode: 400, headers: { 'content-type': 'text/html' }, body: '<html><input type="password"></html>' }, API, 'json'), { outcome: 'block', reason: 'login page' });
check('T-A2-07 an HTML page in a binary body is still an HTML page',
  outcome({ statusCode: 200, headers: {}, body: Buffer.from('<!doctype html><html><body>x</body></html>') }, `https://${MEDIA}/x/s.aac`, 'binary'), 'block');
check('T-A2-07 a JSON answer that is null is not data', [outcome({ statusCode: 200, headers: {}, body: 'null' }), outcome({ statusCode: 200, headers: {}, body: null })],
  ['other', 'other']);
check('T-A2-07 a redirect to another scheme stops the host', outcome({ statusCode: 302, headers: { location: 'ftp://x.invalid/a' }, body: '' }), 'block');
check('T-A2-10 a 201 with its JSON (the start of an Apify run) is an answer', outcome(json({ data: { id: 'r' } }, 201), 'https://api.apify.com/v2/acts/a~b/runs'), 'ok');
check('T-A2-07 a list answer that is not JSON is not data', outcome({ statusCode: 200, headers: { 'content-type': 'text/plain' }, body: 'x' }), 'other');
check('T-A2-07 a JSON answer, object or text, is data',
  [outcome(json({ data: { items: [] } })), outcome({ statusCode: 200, headers: {}, body: '{"data":{}}' })], ['ok', 'ok']);
check('T-A2-07 the words of a JSON answer never stop a host',
  outcome(json({ data: { items: [{ title: 'login captcha accesso negato <html>' }] } })), 'ok');
{
  const after = g.afterVerdict({}, { outcome: 'block', reason: 'HTTP 403' }, NOW);
  check('T-A2-07 a block stops the host until the owner says', [after.state.fermo, after.stopped_now, /HTTP 403/.test(after.state.motivo)], ['owner', true, true]);
  check('T-A2-07 the host stays stopped on the following days', [g.isStopped(after.state, NOW), g.isStopped(after.state, '2026-12-20T10:00:00Z')], [true, true]);
  check('T-A2-07 a stopped host is not read', g.mayRead('api-ovp.streamcloud.it', after.state, NOW), false);
  check('T-A2-07 it starts again only when the owner empties the stop in its row',
    g.isStopped(Object.assign({}, after.state, { fermo: '' }), NOW), false);
  check('T-A2-07 any other value written by hand in the stop is a stop by the owner',
    ['si', 'Owner', 'owner ', 'x'].map((f) => [g.isStopped({ fermo: f }, NOW), g.mayRead('api-ovp.streamcloud.it', { fermo: f, robots_giorno: '2026-11-16' }, NOW)]),
    [[true, false], [true, false], [true, false], [true, false]]);
  check('T-A2-07 a stop for a streak with a day in another form is a stop by the owner', g.isStopped({ fermo: 'giorno', fermo_fino: '17/11/2026' }, '2027-01-01T10:00:00Z'), true);
  let four = {};
  for (let i = 0; i < 4; i++) four = g.afterVerdict(four, { outcome: 'server_error' }, NOW).state;
  const blocked = g.afterVerdict(four, { outcome: 'block', reason: 'HTTP 403' }, NOW).state;
  check('T-A2-07 a block ends the streak, so that a restart by the owner starts from zero',
    [blocked.errori_di_fila, g.afterVerdict(Object.assign({}, blocked, { fermo: '' }), { outcome: 'server_error' }, NOW).state.fermo], [0, '']);
  check('T-A2-07 a second block on a stopped host does not count as a new stop',
    g.afterVerdict(after.state, { outcome: 'block', reason: 'HTTP 429' }, NOW).stopped_now, false);
}
{
  let s = {};
  const flags = [];
  for (let i = 1; i <= 5; i++) {
    const r = g.afterVerdict(s, { outcome: 'server_error', reason: 'HTTP 500' }, NOW);
    s = r.state;
    flags.push([s.errori_di_fila, r.stopped_now, g.isStopped(s, NOW)]);
  }
  check('T-A2-07 a server error counts in the streak (the entry stays for the next run: romatv-list.js, readFailure); five in a row stop the host',
    flags, [[1, false, false], [2, false, false], [3, false, false], [4, false, false], [5, true, true]]);
  check('T-A2-07 the stop for a streak lasts until the next day of Rome', [s.fermo, s.fermo_fino], ['giorno', '2026-11-17']);
  check('T-A2-07 at 23:30 in Rome it is still the same day', g.isStopped(s, '2026-11-16T22:30:00Z'), true);
  check('T-A2-07 at 00:30 in Rome the next day it is lifted', g.isStopped(s, '2026-11-16T23:30:00Z'), false);
  let dst = {};
  for (let i = 0; i < 5; i++) dst = g.afterVerdict(dst, { outcome: 'server_error' }, '2027-03-28T21:30:00Z').state;
  check('T-A2-07 the day of Rome across the change of hour: a stop at 23:30 of 28 March 2027 ends on the 29th',
    [dst.fermo_fino, g.isStopped(dst, '2027-03-28T21:59:00Z'), g.isStopped(dst, '2027-03-28T22:01:00Z')], ['2027-03-29', true, false]);
  check('T-A2-07 when it is lifted the streak starts from zero',
    g.afterVerdict(s, { outcome: 'server_error', reason: 'HTTP 500' }, '2026-11-17T08:00:00Z').state.errori_di_fila, 1);
  let t = {};
  for (const o of ['server_error', 'server_error', 'ok', 'server_error']) t = g.afterVerdict(t, { outcome: o }, NOW).state;
  check('T-A2-07 an answer that is not a server error ends the streak', t.errori_di_fila, 1);
  let u = {};
  for (const o of ['server_error', 'server_error', 'other']) u = g.afterVerdict(u, { outcome: o }, NOW).state;
  check('T-A2-07 a 404 ends the streak as well', u.errori_di_fila, 0);
}

console.log('T-A2-08 — robots.txt against the rules of 14 November 2026');
const text = (body, code) => ({ statusCode: code || 200, headers: { 'content-type': 'text/plain' }, body });
{
  const ok = g.afterRobots(PORTAL, {}, text('User-agent: *\nAllow: /\n'), NOW);
  check('T-A2-08 the portal with its rules of 14 November: checked for today, read', [ok.kind, ok.read, ok.stopped_now, ok.state.robots_giorno],
    ['allow_all', true, false, '2026-11-16']);
  check('T-A2-08 comments and an empty Disallow are still nothing disallowed',
    g.afterRobots(PORTAL, {}, text('# rules\nUser-agent: *\nDisallow:\n'), NOW).kind, 'allow_all');
  const changed = g.afterRobots(PORTAL, {}, text('User-agent: *\nDisallow: /portal/\n'), NOW);
  check('T-A2-08 rules that appear where there were none stop the host until the owner says',
    [changed.kind, changed.read, changed.stopped_now, changed.state.fermo], ['rules', false, true, 'owner']);
  check('T-A2-08 a crawl delay that appears is a change too', g.afterRobots(PORTAL, {}, text('User-agent: *\nCrawl-delay: 10\n'), NOW).stopped_now, true);
  check('T-A2-08 an HTML page or a 404 where the rules were read stop the host',
    [g.afterRobots(PORTAL, {}, html('<html><body>x</body></html>'), NOW).stopped_now, g.afterRobots(PORTAL, {}, text('', 404), NOW).stopped_now], [true, true]);
  const down = g.afterRobots(PORTAL, {}, text('', 503), NOW);
  check('T-A2-08 a server error on rules that were readable: not checked today, not read, one in the streak, not stopped',
    [down.kind, down.read, down.stopped_now, down.state.robots_giorno, down.state.errori_di_fila, down.state.fermo], ['unreadable', false, false, '', 1, '']);
  const api = g.afterRobots('api-ovp.streamcloud.it', {}, text('Service Unavailable', 503), NOW);
  check('T-A2-08 the API with its 503 of 14 November: checked, read', [api.kind, api.read, api.state.robots_giorno], ['unreadable', true, '2026-11-16']);
  check('T-A2-08 the API without an answer is still unreadable', g.afterRobots('api-ovp.streamcloud.it', {}, { error: 'ETIMEDOUT' }, NOW).read, true);
  check('T-A2-08 rules that become readable on the API stop it until the owner says',
    g.afterRobots('api-ovp.streamcloud.it', {}, text('User-agent: *\nAllow: /\n'), NOW).state.fermo, 'owner');
  check('T-A2-08 the media host with its HTML page: checked; with rules: stopped',
    [g.afterRobots(MEDIA, {}, html('<html><body>Wowza</body></html>'), NOW).read, g.afterRobots(MEDIA, {}, text('User-agent: *\nDisallow: /\n'), NOW).stopped_now],
    [true, true]);
  check('T-A2-08 a block signal on robots.txt stops the host', g.afterRobots(PORTAL, {}, text('', 403), NOW).state.fermo, 'owner');
  check('T-A2-08 once a day: due before the check, not after it, due again the next day',
    [g.robotsDue(PORTAL, {}, NOW), g.robotsDue(PORTAL, ok.state, NOW), g.robotsDue(PORTAL, ok.state, '2026-11-17T06:00:00Z')], [true, false, true]);
  check('T-A2-08 a site is read only on the day it was checked',
    [g.mayRead(PORTAL, {}, NOW), g.mayRead(PORTAL, ok.state, NOW), g.mayRead(PORTAL, ok.state, '2026-11-17T06:00:00Z')], [false, true, false]);
  check('T-A2-08 a stopped host is not due for its check', g.robotsDue(PORTAL, changed.state, NOW), false);
  check('T-A2-08 a captcha or a sign-in page in place of the media host\'s page stops it',
    [g.afterRobots(MEDIA, {}, html('<html><div class="g-recaptcha"></div></html>'), NOW).state.fermo, g.afterRobots(MEDIA, {}, html('<html><input type="password"></html>'), NOW).state.fermo],
    ['owner', 'owner']);
  check('T-A2-08 a redirect of robots.txt, even within the host, is a change',
    g.afterRobots(PORTAL, {}, { statusCode: 301, headers: { location: '/robots.txt/' }, body: '' }, NOW).kind, 'moved');
  const again = g.afterRobots(PORTAL, Object.assign({}, changed.state, { fermo: '' }), text('User-agent: *\nDisallow: /portal/\n'), NOW);
  check('T-A2-08 a stop for changed rules comes back if the owner only empties it: it is lifted with a PR on HOSTS',
    [again.state.fermo, again.stopped_now], ['owner', true]);
}

console.log('T-A2-10 — Apify, and no request to YouTube');
for (const code of [401, 403, 429]) {
  const v = g.verdict({ statusCode: code, headers: {}, body: '' }, 'https://api.apify.com/v2/acts/x/runs', 'json');
  check(`T-A2-10 HTTP ${code} from the Apify API stops Apify until the owner says`, g.afterVerdict({}, v, NOW).state.fermo, 'owner');
}
check('T-A2-10 a stopped Apify may not be asked', g.mayRead('api.apify.com', { fermo: 'owner' }, NOW), false);
check('T-A2-10 Apify is a service with a key: no robots.txt check', [g.robotsDue('api.apify.com', {}, NOW), g.mayRead('api.apify.com', {}, NOW)], [false, true]);
check('T-A2-10 its robots.txt is never judged', thrown(() => g.afterRobots('api.apify.com', {}, text('x'), NOW)), 'no robots.txt check for api.apify.com');
for (const u of ['https://www.youtube.com/watch?v=AAAAAAAAAAA', 'https://youtube.com/feeds/videos.xml', 'https://i.ytimg.com/x.jpg',
  'https://www.youtube.com/api/timedtext', 'https://identity-ovp.streamcloud.it/', 'http://streaming.comune.roma.it/']) {
  check(`T-A2-10 no request goes to ${u.replace(/^https?:\/\//, '').split('/')[0]}${u.startsWith('http:') ? ' over http' : ''}`,
    /^host_not_allowed/.test(thrown(() => g.requestOptions({ url: u })) || ''), true);
}
{
  const o = g.requestOptions({ url: API, method: 'POST', body: { page: 1 }, headers: { Accept: 'application/json', 'Content-Type': 'application/json' } });
  check('T-A2-10 every request the guard builds carries the declared user agent and follows no redirect',
    [o.headers['User-Agent'], o.disableFollowRedirect, o.returnFullResponse, o.ignoreHttpStatusErrors], [g.USER_AGENT, true, true, true]);
  check('T-A2-10 no cookie, no login, no other user agent',
    ['Cookie', 'Authorization', 'User-Agent', 'X-Forwarded-For'].map((h) => thrown(() => g.requestOptions({ url: API, headers: { [h]: 'x' } }))),
    ['header_not_allowed: Cookie', 'header_not_allowed: Authorization', 'header_not_allowed: User-Agent', 'header_not_allowed: X-Forwarded-For']);
  check('T-A2-10 the user agent is that of channel B', g.USER_AGENT, require(path.join(__dirname, '..', 'code-nodes', 'news-collect.js')).USER_AGENT);
  check('T-A2-08 a robots.txt request is only the robots.txt of its host',
    [thrown(() => g.requestOptions({ url: API, robots: true })), thrown(() => g.requestOptions({ url: 'https://api-ovp.streamcloud.it/robots.txt', robots: true }))],
    ['robots_request_not_robots_txt', null]);
  check('T-A2-10 the portal headers only with the portal values',
    [Object.keys(g.requestOptions({ url: API, headers: g.PORTAL_HEADERS }).headers).sort(), thrown(() => g.requestOptions({ url: API, headers: { Origin: 'https://example.invalid' } }))],
    [['Origin', 'Referer', 'User-Agent'], 'header_not_allowed: Origin']);
}

console.log('T-A2-12 — the pause per host, with a fake clock');
{
  const end = 1_000_000;
  check('T-A2-12 five seconds to the API, from the end of its last answer', [g.waitMs('api-ovp.streamcloud.it', end, end), g.waitMs('api-ovp.streamcloud.it', end, end + 3000), g.waitMs('api-ovp.streamcloud.it', end, end + 6000)],
    [5000, 2000, 0]);
  check('T-A2-12 five seconds to the portal and to the speech host', [g.waitMs(PORTAL, end, end + 1000), g.waitMs('ac104mp.streamcloud.it', end, end + 1000)], [4000, 4000]);
  check('T-A2-12 one second to the media host', [g.waitMs(MEDIA, end, end), g.waitMs(MEDIA, end, end + 400)], [1000, 600]);
  check('T-A2-12 the first request of a run waits the whole pause', [g.waitMs('api-ovp.streamcloud.it', NaN, end), g.waitMs(MEDIA, undefined, end)], [5000, 1000]);
  const T = Date.parse(NOW);
  check('T-A2-12 an end that is null, empty, zero, false, in seconds or a text gives the whole pause',
    [null, '', 0, false, Math.floor((T - 1000) / 1000), String(T - 1000)].map((v) => g.waitMs('api-ovp.streamcloud.it', v, T)), [5000, 5000, 5000, 5000, 5000, 5000]);
  check('T-A2-12 an end in the future gives the whole pause, never more',
    [g.waitMs('api-ovp.streamcloud.it', T + 120000, T), g.waitMs('api-ovp.streamcloud.it', T - 1000, T)], [5000, 4000]);
  check('T-A2-12 a request and its pause end inside the 60 seconds of a Code node',
    Math.max(...Object.values(g.HOSTS).map((h) => h.pause_ms)) + g.TIMEOUT_MS < 60000, true);
}

console.log('T-A2-12 — the n8n adapter');
function runNode(json, answer) {
  const calls = [];
  const waits = [];
  const helpers = { httpRequest: async (o) => { calls.push(o); if (answer instanceof Error) throw answer; return answer; } };
  const ctx = { helpers };
  const fn = new Function('$input', '$json', 'require', 'URL', 'URLSearchParams', 'process', 'module', 'setTimeout', src);
  let out;
  try {
    out = fn.call(ctx, { item: { json } }, json, require, undefined, undefined, undefined, undefined, (cb, ms) => { waits.push(ms); cb(); });
  } catch (e) {
    return Promise.reject(e);
  }
  return Promise.resolve(out).then((item) => ({ item, calls, waits }));
}
const day = g.romeDay(new Date().toISOString());
const checked = { robots_giorno: day };
const tests = [
  runNode({ stage: 'fetch', request: { url: API, method: 'POST', body: { page: 1 }, expects: 'json' }, host_state: checked },
    json({ data: { items: [] } })).then(({ item, calls, waits }) => {
    check('T-A2-12 fetch: one request, after the whole pause, with the declared user agent',
      [calls.length, waits.length === 1 && waits[0] > 4900 && waits[0] <= 5000, calls[0].headers['User-Agent']], [1, true, g.USER_AGENT]);
    check('T-A2-12 fetch: the verdict, the answer kept and the end of the answer',
      [item.json.verdict.outcome, item.json.answer.statusCode, Number.isFinite(item.json.last_end_ms)], ['ok', 200, true]);
  }),
  runNode({ stage: 'fetch', request: { url: API, method: 'POST', body: {}, expects: 'json' }, host_state: checked, last_end_ms: Date.now() - 10000 },
    json({})).then(({ waits }) => check('T-A2-12 fetch: no wait when the pause has passed', waits.length, 0)),
  runNode({ stage: 'fetch', request: { url: API, expects: 'json' }, host_state: { fermo: 'owner', robots_giorno: day } }, json({}))
    .then(({ item, calls }) => check('T-A2-07 fetch: a stopped host is not asked, and the verdict says it is stopped',
      [calls.length, item.json.verdict.outcome, item.json.verdict.host_stopped], [0, 'skipped', true])),
  runNode({ stage: 'fetch', request: { url: API, expects: 'json' }, host_state: {} }, json({}))
    .then(({ item, calls }) => check('T-A2-08 fetch: a host not checked today is not asked, and it is not called stopped',
      [calls.length, item.json.verdict.host_stopped], [0, false])),
  runNode({ stage: 'fetch', request: { url: 'https://api-ovp.streamcloud.it/robots.txt', robots: true }, host_state: {} }, text('x', 503))
    .then(({ item, calls }) => check('T-A2-08 fetch: robots.txt is asked before the check of the day, and judged by the robots stage',
      [calls.length, item.json.verdict, item.json.answer.statusCode], [1, null, 503])),
  runNode({ stage: 'fetch', request: { url: API, expects: 'json' }, host_state: checked }, new Error('socket hang up'))
    .then(({ item }) => check('T-A2-07 fetch: a request that fails is a server error in the streak',
      [item.json.verdict.outcome, item.json.host_state.errori_di_fila], ['server_error', 1])),
  runNode({ stage: 'fetch', request: { url: API, expects: 'json' }, host_state: checked }, { statusCode: 403, headers: { 'set-cookie': 'a=b' }, body: '' })
    .then(({ item }) => check('T-A2-07 fetch: a 403 stops the host in this run, and no cookie is kept',
      [item.json.stopped_now, item.json.host_state.fermo, Object.keys(item.json.answer.headers)], [true, 'owner', ['content-type', 'location']])),
  runNode({ stage: 'answer', url: 'https://api.apify.com/v2/acts/x/runs', answer: { statusCode: 429, headers: { 'set-cookie': 'a=b' }, body: '' }, host_state: {} })
    .then(({ item, calls }) => check('T-A2-10 answer: a 429 from the Apify node stops Apify with its alert, asks nothing and keeps no cookie',
      [item.json.host_state.fermo, calls.length, !!item.json.alert, Object.keys(item.json.answer.headers)], ['owner', 0, true, ['content-type', 'location']])),
  runNode({ stage: 'may', host: 'api.apify.com', host_state: { fermo: 'owner' } })
    .then(({ item, calls }) => check('T-A2-10 may: with Apify stopped the stage before the Apify node says no',
      [item.json.may_read, calls.length], [false, 0])),
  runNode({ stage: 'may', host: 'api.apify.com', host_state: {} })
    .then(({ item }) => check('T-A2-10 may: Apify not stopped may be asked', item.json.may_read, true)),
  runNode({ stage: 'fetch', workflow: 'staging_A_elenco', request: { url: API, expects: 'json' }, host_state: checked }, { statusCode: 429, headers: {}, body: '' })
    .then(({ item }) => {
      check('T-A2-07 fetch: the stop gives its alert at once, with the answer that stops',
        [item.json.alert.name.startsWith('AVVISO_A_') && item.json.alert.name.endsWith('_api-ovp.streamcloud.it.json'), item.json.alert.body.host, item.json.alert.body.workflow],
        [true, 'api-ovp.streamcloud.it', 'staging_A_elenco']);
    }),
  runNode({ stage: 'fetch', request: { url: API, expects: 'json' }, host_state: checked }, json({}))
    .then(({ item }) => check('T-A2-07 fetch: no stop, no alert', item.json.alert, null)),
  runNode({ stage: 'robots', host: MEDIA, host_state: {}, answer: text('User-agent: *\nDisallow: /\n') })
    .then(({ item }) => check('T-A2-08 robots: a change stops the host with its alert', [item.json.stopped_now, !!item.json.alert], [true, true])),
  runNode({ stage: 'fetch', request: { url: API, robots: true }, host_state: {} }, json({}))
    .then(() => check('T-A2-08 fetch: a robots flag on another path is refused', 'no error', 'an error'),
      (e) => check('T-A2-08 fetch: a robots flag on another path is refused', e.message, 'robots_request_not_robots_txt')),
];

console.log('what the node may use inside n8n');
const code = src.replace(/\/\*[\s\S]*?\*\/|\/\/.*$/gm, '');
check('no URL global', /\bURL\b|URLSearchParams/.test(code), false);
check('no process', /\bprocess\b/.test(code), false);
check('no module required', code.match(/require\('[^']+'\)/g), null);

Promise.all(tests).then(() => {
  console.log('');
  if (failures === 0) {
    console.log(`ALL PASS (${checks} checks)`);
    process.exit(0);
  } else {
    console.log(`${failures} of ${checks} checks FAILED`);
    process.exit(1);
  }
}, (e) => { console.log(`FAIL ${e.stack}`); process.exit(1); });

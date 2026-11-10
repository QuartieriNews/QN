#!/usr/bin/env node
/**
 * Executable acceptance for code-nodes/news-collect.js: the hourly collection of channel B
 * (docs/pilota/CONTRATTI.md, section 7, «B · Notizie»: «Fonti», «Raccolta», «Originali»):
 * robots.txt once a day per host and its matching, the answers that stop a host, the
 * files and register of a run, Rome days (Spec v2.5 T17), and the n8n adapter evaluated
 * from the exact committed file with stubbed $input/$json/$getWorkflowStaticData. Every
 * robots file and page is invented (DEC-109, DEC-031 point 4).
 *
 * Run:  node tests/test_news_collect.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');
const FILE = path.join(__dirname, '..', 'code-nodes', 'news-collect.js');
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

console.log('robots.txt: groups and matching (RFC 9309)');
const ROBOTS_FEEDS = 'User-agent: *\nDisallow: /Feeds/\n';
const ROBOTS_CDN = 'User-agent: *\nDisallow: /\nAllow: */feed\nAllow: /*?feed=\n';
const ROBOTS_DELAY = 'User-agent: *\nDisallow: /feed/\nCrawl-delay: 10\n';
const ROBOTS_AI = 'User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nUser-agent: ClaudeBot\nDisallow: /\n';
check('a listing outside /Feeds/ is allowed', m.robotsVerdict(ROBOTS_FEEDS, '/in-vostro-aiuto/informazioni/comunicati-stampa').allowed, true);
check('the feed under /Feeds/ is not', m.robotsVerdict(ROBOTS_FEEDS, '/Feeds/comunicati').allowed, false);
check('"Disallow: /" with "Allow: */feed" allows the feed', m.robotsVerdict(ROBOTS_CDN, '/feed/').allowed, true);
check('and nothing else', m.robotsVerdict(ROBOTS_CDN, '/articolo-inventato/').allowed, false);
check('a Disallowed feed path is refused, with its crawl delay', m.robotsVerdict(ROBOTS_DELAY, '/feed/'), { allowed: false, crawl_delay: 10 });
check('a group of AI agents that disallows everything applies to us too', m.robotsVerdict(ROBOTS_AI, '/feed/').allowed, false);
check('a group named for us wins over "*"',
  m.robotsVerdict('User-agent: *\nDisallow: /\n\nUser-agent: QuartieriNews\nAllow: /feed/\n', '/feed/').allowed, true);
check('the longest rule wins', m.robotsVerdict('User-agent: *\nDisallow: /a\nAllow: /a/b\n', '/a/b/c').allowed, true);
check('on a tie Allow wins', m.robotsVerdict('User-agent: *\nDisallow: /a\nAllow: /a\n', '/a').allowed, true);
check('$ anchors the end', [m.ruleMatches('/x$', '/x'), m.ruleMatches('/x$', '/xy')], [true, false]);
check('an empty Disallow allows everything', m.robotsVerdict('User-agent: *\nDisallow:\n', '/qualsiasi').allowed, true);
check('no group at all allows the path', m.robotsVerdict('# nulla\n', '/feed/').allowed, true);
check('comments are ignored', m.robotsVerdict('User-agent: * # tutti\nDisallow: /feed/ # no\n', '/feed/').allowed, false);

console.log('answers that stop a host (CONTRATTI section 7, B, «Raccolta»)');
const ok = (body, type) => ({ statusCode: 200, headers: { 'content-type': type || 'application/rss+xml' }, body });
check('403', m.blockSignal({ statusCode: 403, body: '' }), 'HTTP 403');
check('429', m.blockSignal({ statusCode: 429, body: '' }), 'HTTP 429');
check('401', m.blockSignal({ statusCode: 401, body: '' }), 'HTTP 401');
check('a redirect to another host', m.blockSignal({ statusCode: 302, headers: { location: 'https://sso.esempio-inventato.it/x' }, body: '' }, 'https://esempio-inventato.it/feed/'),
  'redirect to https://sso.esempio-inventato.it/x');
check('a redirect within the host is not a block', m.blockSignal({ statusCode: 301, headers: { location: '/feed/' }, body: '' }, 'https://esempio-inventato.it/feed'), null);
check('a redirect within the host to a sign-in page is', m.blockSignal({ statusCode: 302, headers: { location: '/accedi?next=/feed' }, body: '' }, 'https://esempio-inventato.it/feed'),
  'redirect to /accedi?next=/feed');
check('a relative redirect is resolved against the page asked for', m.resolveLocation('altro', 'https://esempio-inventato.it/a/b'), 'https://esempio-inventato.it/a/altro');
check('a challenge page', m.blockSignal(ok('<html><div class="g-recaptcha" data-sitekey="x"></div></html>', 'text/html')), 'captcha');
check('a feed whose news mentions a captcha is not a block', m.blockSignal(ok('<rss><item><title>Il captcha inventato</title></item></rss>')), null);
check('nor is a long listing that mentions «accesso negato» in a title',
  m.blockSignal(ok('<html><title>Notizie</title><h3>Accesso negato inventato</h3>' + '<p>riga inventata</p>'.repeat(200) + '</html>', 'text/html')), null);
check('a login form', m.blockSignal(ok('<html><form><input type="password"></form></html>', 'text/html')), 'login page');
check('a block page served with 200', m.blockSignal(ok('<html><h1>Accesso negato</h1></html>', 'text/html')), 'block page');
check('a short page that says so is one too', m.blockSignal(ok('<html><p>Accesso negato</p></html>', 'text/html')), 'block page');
check('a feed is not a block', m.blockSignal(ok('<rss><channel><item><title>Inventato</title></item></channel></rss>')), null);

check('groups naming the same agent are merged before the longest rule (RFC 9309)',
  m.robotsVerdict('User-agent: *\nDisallow: /private\n\nUser-agent: *\nAllow: /private/public\n', '/private/public').allowed, true);

console.log('a run: plan, robots, pages');
const NOW = '2026-11-10T22:07:00Z';
const LATER = '2026-11-10T22:08:30Z';
const plan = m.planRun({ state: undefined, now: NOW });
check('the first run reads robots.txt of every source', plan.robots.map((r) => r.source_id), m.SOURCES.map((s) => s.source_id));
check('robots.txt is at the origin of the page', plan.robots[1].url, 'https://www.carabinieri.it/robots.txt');
const answers = [
  { source_id: 'questure.poliziadistato.it', statusCode: 200, body: 'User-agent: *\nDisallow: /sendemail/\n' },
  { source_id: 'carabinieri.it', statusCode: 200, body: ROBOTS_FEEDS },
  { source_id: 'abitarearoma.it', statusCode: 200, body: 'User-agent: *\nDisallow: /wp/wp-admin/\n' },
  { source_id: 'cdn.ilfaroonline.it', statusCode: 200, body: ROBOTS_CDN },
];
const r1 = m.afterRobots({ state: plan.state, now: NOW, answers });
check('every source allowed: a page each, at least 5 s apart', r1.pages.map((p) => [p.source_id, p.wait_ms]),
  m.SOURCES.map((s) => [s.source_id, 5000]));
check('the same day robots.txt is not read again', m.planRun({ state: r1.state, now: LATER }).robots, []);
check('the next Rome day it is (23:30 UTC on 10 Nov is 11 Nov in Rome)',
  m.planRun({ state: r1.state, now: '2026-11-10T23:30:00Z' }).robots.length, 4);
const disallow = m.afterRobots({ state: plan.state, now: NOW, answers: [Object.assign({}, answers[2], { body: 'User-agent: *\nDisallow: /feed/\n' })] });
check('a robots.txt that disallows the page stops the host', [disallow.state.hosts['abitarearoma.it'].stopped.reason, disallow.pages.map((p) => p.source_id)],
  ['robots.txt disallows the page', []]);
const redirect = m.afterRobots({ state: plan.state, now: NOW, answers: [{ source_id: 'carabinieri.it', statusCode: 302, headers: { location: 'https://x.invalid/login' }, body: '' }] });
check('a robots.txt that redirects stops the host', /robots.txt: redirect/.test(redirect.state.hosts['carabinieri.it'].stopped.reason), true);
const missing = m.afterRobots({ state: plan.state, now: NOW, answers: [{ source_id: 'carabinieri.it', statusCode: 404, body: '' }] });
check('a robots.txt that does not read stops the host too', missing.state.hosts['carabinieri.it'].stopped.reason, 'robots.txt: HTTP 404');
check('every robots answer is in the register, the allowed ones too', r1.events.map((e) => [e.source_id, e.outcome]),
  m.SOURCES.map((x) => [x.source_id, 'allowed']));
check('a robots.txt moved within its host leaves the host unread this run, not stopped',
  (() => { const r = m.afterRobots({ state: plan.state, now: NOW, answers: [{ source_id: 'abitarearoma.it', statusCode: 301, headers: { location: 'https://abitarearoma.it/robots.txt/' }, body: '' }] });
    return [r.state.hosts['abitarearoma.it'].stopped, r.pages.length, r.events[0].outcome]; })(), [null, 0, 'moved']);
check('a stop in robots is reported for the coordinator', disallow.stopped_now, [{ source_id: 'abitarearoma.it', reason: 'robots.txt disallows the page' }]);
check('a host stopped once is not asked again', m.planRun({ state: disallow.state, now: '2026-11-12T08:00:00Z' }).robots.some((r) => r.source_id === 'abitarearoma.it'), false);
check('a crawl delay longer than 5 s is kept',
  m.afterRobots({ state: plan.state, now: NOW, answers: [Object.assign({}, answers[2], { body: 'User-agent: *\nCrawl-delay: 10\n' })] }).pages[0].wait_ms, 10000);
check('an answer for an unknown source is a workflow error', /unknown source/.test(thrown(() => m.afterRobots({ state: plan.state, now: NOW, answers: [{ source_id: 'x', statusCode: 200, body: '' }] })) || ''), true);

const pages = m.afterPages({ state: r1.state, now: LATER, started_at: NOW, answers: [
  Object.assign({ source_id: 'abitarearoma.it' }, ok('<rss></rss>')),
  { source_id: 'questure.poliziadistato.it', statusCode: 200, headers: { 'content-type': 'text/html' }, body: '<html><title>Accesso negato</title></html>' },
  { source_id: 'carabinieri.it', statusCode: 503, headers: {}, body: '' },
] });
check('a page read is saved under its host, the start of the run and its number', pages.files.map((f) => f.name), ['notizie_abitarearoma.it_20261110T220700Z_1.xml']);
const two = m.afterPages({ state: r1.state, now: LATER, started_at: NOW, answers: [
  Object.assign({ source_id: 'abitarearoma.it' }, ok('<rss>1</rss>')), Object.assign({ source_id: 'abitarearoma.it' }, ok('<rss>2</rss>')),
  Object.assign({ source_id: 'cdn.ilfaroonline.it' }, ok('<rss>3</rss>'))] });
check('two answers of one host in a run never share a file', two.files.map((f) => f.name),
  ['notizie_abitarearoma.it_20261110T220700Z_1.xml', 'notizie_abitarearoma.it_20261110T220700Z_2.xml', 'notizie_cdn.ilfaroonline.it_20261110T220700Z_1.xml']);
check('a block page stops its host', pages.state.hosts['questure.poliziadistato.it'].stopped.reason, 'block page');
check('a server error is counted, not a stop', [pages.state.hosts['carabinieri.it'].stopped, pages.state.hosts['carabinieri.it'].errors_in_row], [null, 1]);
check('the register names the run and every outcome', [pages.log_file_name, pages.log.hosts.map((h) => h.outcome)],
  ['notizie_20261110T220700Z.json', ['saved', 'stopped', 'error']]);
check('the register lists the hosts stopped', pages.log.stopped.map((s) => s.source_id), ['questure.poliziadistato.it']);
check('a host stopped in this run is reported apart, with an alert file', [pages.log.stopped_now.map((x) => x.source_id), pages.alert_file_name],
  [['questure.poliziadistato.it'], 'AVVISO_notizie_20261110T220700Z.json']);
check('a run without stops writes no alert', m.afterPages({ state: r1.state, now: LATER, started_at: NOW, answers: [] }).alert_file_name, null);
const moved = m.afterPages({ state: r1.state, now: LATER, started_at: NOW, answers: [{ source_id: 'abitarearoma.it', statusCode: 301, headers: { location: '/feed/' }, body: '' }] });
check('a page moved within its host is recorded, not a stop', [moved.log.hosts[0].outcome, moved.state.hosts['abitarearoma.it'].stopped], ['moved', null]);
let streak = r1.state;
for (const code of [500, 500, 404, 500, 500]) streak = m.afterPages({ state: streak, now: LATER, started_at: NOW, answers: [{ source_id: 'carabinieri.it', statusCode: code, body: '' }] }).state;
check('an answer that is not a server error breaks the streak', [streak.hosts['carabinieri.it'].stopped, streak.hosts['carabinieri.it'].errors_in_row], [null, 2]);
let st = r1.state;
for (let i = 0; i < m.ERRORS_TO_STOP; i += 1) st = m.afterPages({ state: st, now: LATER, started_at: NOW, answers: [{ source_id: 'carabinieri.it', statusCode: 500, body: '' }] }).state;
check('five server errors in a row stop the host', st.hosts['carabinieri.it'].stopped.reason, '5 server errors in a row');
const reset = m.afterPages({ state: pages.state, now: LATER, started_at: NOW, answers: [Object.assign({ source_id: 'carabinieri.it' }, ok('<html></html>', 'text/html'))] });
check('a good answer resets the count', reset.state.hosts['carabinieri.it'].errors_in_row, 0);
check('an HTML page is saved as html', reset.files[0].name.endsWith('.html'), true);
check('now must be a UTC instant', thrown(() => m.planRun({ state: undefined, now: '2026-11-10 22:07' })), 'now must be a UTC instant');
check('the user agent declares who reads', /QuartieriNews/.test(m.USER_AGENT), true);

check('origin and path without the URL global', m.urlParts('https://WWW.Esempio-Inventato.it/a/b?c=1'), { origin: 'https://www.esempio-inventato.it', pathname: '/a/b' });
check('an origin without a path has the root path', m.urlParts('https://esempio-inventato.it').pathname, '/');
check('the node does not use the URL global, which n8n does not have', /new URL\(/.test(fs.readFileSync(FILE, 'utf8')), false);

console.log('n8n adapter — exact committed file, stubbed $input/$json/$getWorkflowStaticData');
const src = fs.readFileSync(FILE, 'utf8');
const store = {};
function runNode(json) {
  const item = { json };
  // n8n's Code node has neither URL nor URLSearchParams: the adapter runs without them.
  return new Function('$input', '$json', 'require', '$getWorkflowStaticData', 'URL', 'URLSearchParams', src)(
    { item }, json, require, () => store, undefined, undefined);
}
{
  const p = runNode({ stage: 'plan', now: NOW });
  check('plan: the robots requests, the state saved', [p.json.robots.length, Object.keys(store.news_collect.hosts).length], [4, 4]);
  const r = runNode({ stage: 'robots', now: NOW, answers });
  check('robots: the pages, the answers dropped', [r.json.pages.length, r.json.answers], [4, undefined]);
  const g = runNode({ stage: 'pages', now: LATER, started_at: NOW, answers: [Object.assign({ source_id: 'abitarearoma.it' }, ok('<rss></rss>'))], robots_events: [] });
  check('pages: the files and the register', [g.json.files.length, g.json.log_file_name], [1, 'notizie_20261110T220700Z.json']);
  check('the state persists between nodes', store.news_collect.hosts['abitarearoma.it'].robots_day, '2026-11-10');
  check('an unknown stage is a workflow error', /unknown stage/.test(thrown(() => runNode({ stage: 'altro' })) || ''), true);
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

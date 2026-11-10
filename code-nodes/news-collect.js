/**
 * news-collect.js — workstream B, the hourly collection of the news sources: which
 * requests a run makes, what robots.txt allows, which answers stop a host, and which
 * files and register the run writes. The rules are in docs/pilota/CONTRATTI.md,
 * section 7 («B · Notizie», rows «Fonti», «Raccolta», «Originali»); this file does not
 * restate them. It writes no news element: the channel only collects originals until
 * the next PRs arrive.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is
 * undefined, so the tail exports and stops; inside the n8n Code node ("Run Once for Each
 * Item") the same file runs its adapter, keeping the state of the hosts in the
 * workflow's static data. `stage` on the item says which step it takes:
 *   - 'plan': the robots.txt to read before this run's pages;
 *   - 'robots': their answers become the hosts allowed and the pages to request;
 *   - 'pages': the answers become the files to save in originali/ and the run's register.
 * The requests and the pause between them belong to the workflow.
 */
'use strict';

/** CONTRATTI.md section 7 (B), «Fonti al 10 novembre 2026». */
const SOURCES = Object.freeze([
  { source_id: 'questure.poliziadistato.it', channel: 'news_official',
    url: 'https://questure.poliziadistato.it/it/Roma/archivio/category/5730dc9d86cad683338531/1/' },
  { source_id: 'carabinieri.it', channel: 'news_official',
    url: 'https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa' },
  { source_id: 'abitarearoma.it', channel: 'news_press', url: 'https://abitarearoma.it/feed/' },
  { source_id: 'cdn.ilfaroonline.it', channel: 'news_press', url: 'https://cdn.ilfaroonline.it/feed/' },
]);

/** The user agent the requests declare, the token robots.txt groups are matched on, and the
 *  AI agents whose groups apply to us as well: the most restrictive group wins. */
const USER_AGENT = 'QuartieriNews-staging/0.1 (+https://quartierinews.it)';
const AGENT_TOKENS = Object.freeze(['quartierinews', 'gptbot', 'chatgpt-user', 'claudebot', 'claude-web', 'anthropic-ai',
  'ccbot', 'google-extended', 'perplexitybot', 'bytespider']);
/** After this many server errors or timeouts in a row a host stops too. */
const ERRORS_TO_STOP = 5;

/** Origin and path of an http(s) URL. The n8n Code node has no `URL` global and no `url`
 *  module, so the two parts are read with a pattern. */
function urlParts(u) {
  const m = typeof u === 'string' && /^(https?:\/\/[^/?#]+)(\/[^?#]*)?/i.exec(u);
  if (!m) throw new Error(`not an http(s) URL: ${JSON.stringify(u)}`);
  return { origin: m[1].toLowerCase(), pathname: m[2] || '/' };
}

const ROME_DAY = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' });
const romeDay = (iso) => ROME_DAY.format(new Date(iso));
const compactInstant = (iso) => new Date(iso).toISOString().slice(0, 19).replace(/[-:]/g, '') + 'Z';
const bodyText = (res) => (typeof res.body === 'string' ? res.body : JSON.stringify(res.body === undefined ? null : res.body));
/** The status of an answer; a request that got none (a timeout, a refused connection: the
 *  workflow passes them on with `error`) has NaN. */
const statusOf = (res) => (res.error || res.statusCode === null || res.statusCode === undefined || res.statusCode === '' ? NaN : Number(res.statusCode));
/** What a run records for an answer that is not a page. */
const failure = (res) => (res.error ? String(res.error) : `HTTP ${res.statusCode}`);

function instant(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(v) || Number.isNaN(Date.parse(v))) {
    throw new Error('now must be a UTC instant');
  }
  return v;
}

/** Robots.txt as groups: each with its agents (lower case) and its Allow/Disallow rules. */
function parseRobots(text) {
  if (typeof text !== 'string') throw new Error('robots_unreadable');
  const groups = [];
  let current = null;
  let lastWasAgent = false;
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, '').trim();
    if (!line) continue;
    const m = /^([A-Za-z-]+)\s*:\s*(.*)$/.exec(line);
    if (!m) continue;
    const key = m[1].toLowerCase();
    const value = m[2].trim();
    if (key === 'user-agent') {
      if (!lastWasAgent) { current = { agents: [], rules: [] }; groups.push(current); }
      current.agents.push(value.toLowerCase());
      lastWasAgent = true;
    } else {
      lastWasAgent = false;
      if (!current) continue;
      if (key === 'allow' || key === 'disallow') current.rules.push({ allow: key === 'allow', path: value });
      if (key === 'crawl-delay') current.crawl_delay = Number(value);
    }
  }
  return groups;
}

/** RFC 9309 matching: `*` is any sequence, a final `$` anchors the end. */
function ruleMatches(rulePath, path) {
  if (rulePath === '') return false;
  const anchored = rulePath.endsWith('$');
  const body = anchored ? rulePath.slice(0, -1) : rulePath;
  const re = new RegExp('^' + body.split('*').map((p) => p.replace(/[.+?^${}()|[\]\\]/g, '\\$&')).join('.*') + (anchored ? '$' : ''));
  return re.test(path);
}

/** Whether one group allows a path: the longest matching rule wins, Allow on a tie. */
function groupAllows(group, path) {
  let best = null;
  for (const r of group.rules) {
    if (!ruleMatches(r.path, path)) continue;
    const len = r.path.replace(/\$$/, '').length;
    if (!best || len > best.len || (len === best.len && r.allow)) best = { len, allow: r.allow };
  }
  return best ? best.allow : true;
}

/** What robots.txt says for us on a path. The rules of every group naming the same agent
 *  count as one group (RFC 9309); the groups that name us, else `*`, apply, and so does the
 *  group of every AI agent: the path is allowed only if all of them allow it. */
function robotsVerdict(text, path) {
  const groups = parseRobots(text);
  const merged = (token) => {
    const gs = groups.filter((g) => g.agents.includes(token));
    if (!gs.length) return null;
    const delays = gs.map((g) => g.crawl_delay).filter((d) => Number.isFinite(d) && d > 0);
    return { rules: [].concat(...gs.map((g) => g.rules)), crawl_delay: delays.length ? Math.max(...delays) : undefined };
  };
  const apply = [merged('quartierinews') || merged('*')]
    .concat(AGENT_TOKENS.filter((t) => t !== 'quartierinews').map(merged)).filter(Boolean);
  const allowed = apply.every((g) => groupAllows(g, path));
  const delays = apply.map((g) => g.crawl_delay).filter((d) => Number.isFinite(d) && d > 0);
  return { allowed, crawl_delay: delays.length ? Math.max(...delays) : null };
}

const hostOf = (u) => ((/^https?:\/\/([^/?#:]+)/i.exec(u || '') || [])[1] || '').toLowerCase();
const pathOf = (u) => (/^https?:\/\/[^/?#]+([^#]*)/i.exec(u || '') || [])[1] || '';
/** A redirect target, made absolute against the URL that was asked for. */
function resolveLocation(loc, requested) {
  if (/^https?:\/\//i.test(loc)) return loc;
  if (loc.startsWith('//')) return (/^(https?:)/i.exec(requested) || ['', 'https:'])[1] + loc;
  if (loc.startsWith('/')) return urlParts(requested).origin + loc;
  return urlParts(requested).origin + urlParts(requested).pathname.replace(/[^/]*$/, '') + loc;
}
/** A path that is a sign-in page, wherever the redirect goes. */
const LOGIN = /(^|[/._?=&-])(login|logon|signin|sign-in|sso|auth|oauth|accedi)([/._?=&-]|$)/i;
/** The marks a challenge page carries in its structure, not in the text of the news. */
const CHALLENGE = /class=["'][^"']*\b(g-recaptcha|h-captcha|cf-turnstile)\b|id=["']?(challenge-form|captcha)\b|recaptcha\/api\.js|hcaptcha\.com\/1\/api\.js|challenges\.cloudflare\.com/i;

const isHtml = (res) => /html/i.test(String((res.headers || {})['content-type'] || '')) || /^\s*(<!doctype html|<html)/i.test(bodyText(res));
const titleAndHeading = (body) => [(/<title[^>]*>([\s\S]*?)<\/title>/i.exec(body) || [])[1], (/<h1[^>]*>([\s\S]*?)<\/h1>/i.exec(body) || [])[1]]
  .filter(Boolean).join(' ').replace(/<[^>]*>/g, ' ');

/** CONTRATTI.md section 7 (B), «Raccolta»: the signal on one answer to `requested` that stops a
 *  host, or null. A redirect stops it when it leaves the host or leads to a sign-in page; within
 *  the host it is a move, which the run records. A feed is judged by its status alone: the text
 *  of the news never stops a host. */
function blockSignal(res, requested) {
  if (!res || typeof res !== 'object') return 'no answer';
  const code = Number(res.statusCode);
  if (code === 401 || code === 403 || code === 429) return `HTTP ${code}`;
  if (code >= 300 && code < 400) {
    const h = res.headers || {};
    const loc = String(h.location || h.Location || '');
    if (!loc) return 'redirect without a location';
    const target = requested ? resolveLocation(loc, requested) : loc;
    if (!requested || hostOf(target) !== hostOf(requested) || LOGIN.test(pathOf(target))) return `redirect to ${loc}`;
    return null;
  }
  if (!isHtml(res)) return null;
  const body = bodyText(res);
  if (CHALLENGE.test(body)) return 'captcha';
  if (/<input[^>]+type=["']?password/i.test(body)) return 'login page';
  if (/\b(accesso\s+negato|access\s+denied|forbidden)\b/i.test(titleAndHeading(body))) return 'block page';
  // A block page is short; a listing that only mentions those words in a title is not.
  const visible = body.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  if (visible.length < 1500 && /\b(accesso\s+negato|access\s+denied)\b/i.test(visible)) return 'block page';
  return null;
}

function freshState(state) {
  const s = state && typeof state === 'object' ? JSON.parse(JSON.stringify(state)) : {};
  s.hosts = s.hosts && typeof s.hosts === 'object' ? s.hosts : {};
  for (const src of SOURCES) {
    s.hosts[src.source_id] = Object.assign({ stopped: null, robots_day: null, robots_allowed: null, errors_in_row: 0 },
      s.hosts[src.source_id]);
  }
  return s;
}

/** Stage 'plan': the robots.txt to read before this run's pages (once a day per host). */
function planRun({ state, now }) {
  const day = romeDay(instant(now));
  const s = freshState(state);
  const robots = SOURCES.filter((src) => !s.hosts[src.source_id].stopped && s.hosts[src.source_id].robots_day !== day)
    .map((src) => ({ source_id: src.source_id, url: `${urlParts(src.url).origin}/robots.txt` }));
  return { state: s, robots };
}

/** Stage 'robots': the answers to robots.txt (`{ source_id, statusCode, headers, body, error }`)
 *  update the hosts; the pages of the hosts allowed today are the requests of the run. Every
 *  answer is an event of the register. A robots.txt that moved within its host, a server error
 *  or no answer at all leave the host unread for this run, not stopped (the last two count in
 *  its streak); an HTML page where the rules should be is never read as rules. */
function afterRobots({ state, now, answers }) {
  const day = romeDay(instant(now));
  const s = freshState(state);
  const events = [];
  const stopped_now = [];
  const stop = (id, reason) => { s.hosts[id].stopped = { at: now, reason }; stopped_now.push({ source_id: id, reason }); };
  for (const a of answers || []) {
    const h = s.hosts[a.source_id];
    const src = SOURCES.find((x) => x.source_id === a.source_id);
    if (!h || !src) throw new Error(`robots answer for an unknown source: ${a.source_id}`);
    const url = `${urlParts(src.url).origin}/robots.txt`;
    const code = statusOf(a);
    // The rules are plain text, whatever type the server declares: only a body that is an HTML
    // document is judged as a page; the comments of a robots.txt never stop a host.
    const htmlPage = code === 200 && /<!doctype\s+html|<html[\s>]|<body[\s>]/i.test(bodyText(a));
    const signal = blockSignal(code !== 200 ? a
      : htmlPage ? Object.assign({}, a, { headers: Object.assign({}, a.headers, { 'content-type': 'text/html' }) })
        : Object.assign({}, a, { body: '' }), url);
    let outcome;
    let reason = null;
    if (signal) {
      stop(a.source_id, `robots.txt: ${signal}`);
      outcome = 'stopped';
    } else if (code >= 300 && code < 400) {
      outcome = 'moved';
      reason = `moved to ${(a.headers || {}).location || ''}`;
    } else if (code >= 500 || !Number.isFinite(code)) {
      h.errors_in_row = (h.errors_in_row || 0) + 1;
      if (h.errors_in_row >= ERRORS_TO_STOP) stop(a.source_id, `robots.txt: ${ERRORS_TO_STOP} server errors in a row`);
      outcome = h.stopped ? 'stopped' : 'error';
      reason = `robots.txt: ${failure(a)}`;
    } else if (code !== 200) {
      stop(a.source_id, `robots.txt: HTTP ${a.statusCode}`);
      outcome = 'stopped';
    } else if (htmlPage) {
      stop(a.source_id, 'robots.txt unreadable: an HTML page instead of the rules');
      outcome = 'stopped';
    } else {
      h.errors_in_row = 0;
      let v = null;
      try {
        v = robotsVerdict(bodyText(a), urlParts(src.url).pathname);
      } catch (e) {
        stop(a.source_id, 'robots.txt unreadable');
      }
      if (v) {
        h.robots_day = day;
        h.robots_allowed = v.allowed;
        h.crawl_delay = v.crawl_delay;
        if (!v.allowed) stop(a.source_id, 'robots.txt disallows the page');
      }
      outcome = h.stopped ? 'stopped' : 'allowed';
    }
    events.push({ source_id: a.source_id, url, status: Number.isFinite(code) ? code : null, outcome,
      reason: h.stopped ? h.stopped.reason : reason });
  }
  const pages = SOURCES.filter((src) => {
    const h = s.hosts[src.source_id];
    return !h.stopped && h.robots_day === day && h.robots_allowed === true;
  }).map((src) => ({ source_id: src.source_id, url: src.url, wait_ms: Math.max(5000, (s.hosts[src.source_id].crawl_delay || 0) * 1000) }));
  return { state: s, pages, events, stopped_now };
}

/** Stage 'pages': the answers to the pages become the files to save and the run's register,
 *  with the hosts that stopped in this run apart (`stopped_now`), for the coordinator. */
function afterPages({ state, now, started_at, answers, robots_events, robots_stopped }) {
  instant(now);
  instant(started_at);
  const s = freshState(state);
  const stamp = compactInstant(started_at);
  const files = [];
  const hosts = [];
  const stopped_now = Array.isArray(robots_stopped) ? robots_stopped.slice() : [];
  const seq = {};
  for (const a of answers || []) {
    const h = s.hosts[a.source_id];
    const src = SOURCES.find((x) => x.source_id === a.source_id);
    if (!h || !src) throw new Error(`page answer for an unknown source: ${a.source_id}`);
    seq[a.source_id] = (seq[a.source_id] || 0) + 1;
    const signal = blockSignal(a, src.url);
    const code = statusOf(a);
    let outcome;
    if (signal) {
      h.stopped = { at: now, reason: signal };
      stopped_now.push({ source_id: a.source_id, reason: signal });
      outcome = { source_id: a.source_id, status: code, outcome: 'stopped', reason: signal };
    } else if (code === 200) {
      h.errors_in_row = 0;
      const type = String((a.headers || {})['content-type'] || '');
      const ext = /xml|rss|atom/i.test(type) ? 'xml' : /json/i.test(type) ? 'json' : 'html';
      // One file per answer: the number of the host's answer in the run keeps every name apart.
      const name = `notizie_${a.source_id}_${stamp}_${seq[a.source_id]}.${ext}`;
      files.push({ name, body: bodyText(a) });
      outcome = { source_id: a.source_id, status: code, outcome: 'saved', file: `originali/${name}` };
    } else if (code >= 500 || !Number.isFinite(code)) {
      // Only server errors and timeouts make a streak; any other answer breaks it.
      h.errors_in_row = (h.errors_in_row || 0) + 1;
      if (h.errors_in_row >= ERRORS_TO_STOP) {
        h.stopped = { at: now, reason: `${ERRORS_TO_STOP} server errors in a row` };
        stopped_now.push({ source_id: a.source_id, reason: h.stopped.reason });
      }
      outcome = { source_id: a.source_id, status: Number.isFinite(code) ? code : null, outcome: h.stopped ? 'stopped' : 'error',
        reason: h.stopped ? h.stopped.reason : failure(a) };
    } else {
      h.errors_in_row = 0;
      const moved = code >= 300 && code < 400;
      outcome = { source_id: a.source_id, status: code, outcome: moved ? 'moved' : 'error',
        reason: moved ? `moved to ${(a.headers || {}).location || ''}` : `HTTP ${a.statusCode}` };
    }
    hosts.push(outcome);
  }
  const stopped = Object.entries(s.hosts).filter(([, h]) => h.stopped).map(([id, h]) => ({ source_id: id, since: h.stopped.at, reason: h.stopped.reason }));
  return {
    state: s,
    files,
    log_file_name: `notizie_${stamp}.json`,
    alert_file_name: stopped_now.length ? `AVVISO_notizie_${stamp}.json` : null,
    log: { workflow: 'staging_B_notizie_raccolta', started_at, finished_at: now, user_agent: USER_AGENT,
      robots: robots_events || [], hosts, stopped_now, stopped },
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { SOURCES, USER_AGENT, AGENT_TOKENS, ERRORS_TO_STOP, urlParts, parseRobots, ruleMatches, groupAllows,
    robotsVerdict, resolveLocation, blockSignal, planRun, afterRobots, afterPages };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter: the state of the hosts lives in the
 * workflow's static data, saved by n8n after a production run. */
const store = $getWorkflowStaticData('global');
let out;
if ($json.stage === 'plan') {
  out = planRun({ state: store.news_collect, now: $json.now });
  $json.robots = out.robots;
} else if ($json.stage === 'robots') {
  out = afterRobots({ state: store.news_collect, now: $json.now, answers: $json.answers });
  $json.pages = out.pages;
  $json.robots_events = out.events;
  $json.robots_stopped = out.stopped_now;
  delete $json.answers;
} else if ($json.stage === 'pages') {
  out = afterPages({ state: store.news_collect, now: $json.now, started_at: $json.started_at, answers: $json.answers,
    robots_events: $json.robots_events, robots_stopped: $json.robots_stopped });
  $json.files = out.files;
  $json.log_file_name = out.log_file_name;
  $json.alert_file_name = out.alert_file_name;
  $json.log = out.log;
  delete $json.answers;
} else {
  throw new Error(`unknown stage ${JSON.stringify($json.stage)}`);
}
store.news_collect = out.state;
return $input.item;

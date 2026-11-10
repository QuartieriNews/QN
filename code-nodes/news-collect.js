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

/** What robots.txt says for us on a path: the groups that name one of our tokens, else `*`,
 *  plus every AI agent's group; the path is allowed only if all of them allow it. */
function robotsVerdict(text, path) {
  const groups = parseRobots(text);
  const named = groups.filter((g) => g.agents.some((a) => AGENT_TOKENS.includes(a)));
  const star = groups.filter((g) => g.agents.includes('*'));
  const ours = named.filter((g) => g.agents.includes('quartierinews'));
  const apply = (ours.length ? ours : star).concat(named.filter((g) => !g.agents.includes('quartierinews')));
  const allowed = apply.every((g) => groupAllows(g, path));
  const delays = apply.map((g) => g.crawl_delay).filter((d) => Number.isFinite(d) && d > 0);
  return { allowed, crawl_delay: delays.length ? Math.max(...delays) : null };
}

/** CONTRATTI.md section 7 (B), «Raccolta»: the signal on one answer that stops a host, or null. */
function blockSignal(res) {
  if (!res || typeof res !== 'object') return 'no answer';
  const code = Number(res.statusCode);
  if (code === 401 || code === 403 || code === 429) return `HTTP ${code}`;
  if (code >= 300 && code < 400) {
    const h = res.headers || {};
    return `redirect to ${h.location || h.Location || '(no location)'}`;
  }
  const body = bodyText(res);
  if (/captcha/i.test(body)) return 'captcha';
  if (/<input[^>]+type=["']?password/i.test(body)) return 'login page';
  if (/accesso\s+negato|access\s+denied/i.test(body)) return 'block page';
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

/** Stage 'robots': the answers to robots.txt (`{ source_id, statusCode, headers, body }`) update
 *  the hosts; the pages of the hosts allowed today are the requests of the run. */
function afterRobots({ state, now, answers }) {
  const day = romeDay(instant(now));
  const s = freshState(state);
  const events = [];
  for (const a of answers || []) {
    const h = s.hosts[a.source_id];
    const src = SOURCES.find((x) => x.source_id === a.source_id);
    if (!h || !src) throw new Error(`robots answer for an unknown source: ${a.source_id}`);
    const signal = blockSignal(Object.assign({}, a, { body: Number(a.statusCode) === 200 ? '' : bodyText(a) }));
    if (signal || Number(a.statusCode) !== 200) {
      h.stopped = { at: now, reason: `robots.txt: ${signal || `HTTP ${a.statusCode}`}` };
      events.push({ source_id: a.source_id, event: 'stopped', reason: h.stopped.reason });
      continue;
    }
    let v;
    try {
      v = robotsVerdict(bodyText(a), urlParts(src.url).pathname);
    } catch (e) {
      h.stopped = { at: now, reason: 'robots.txt unreadable' };
      events.push({ source_id: a.source_id, event: 'stopped', reason: h.stopped.reason });
      continue;
    }
    h.robots_day = day;
    h.robots_allowed = v.allowed;
    h.crawl_delay = v.crawl_delay;
    if (!v.allowed) {
      h.stopped = { at: now, reason: 'robots.txt disallows the page' };
      events.push({ source_id: a.source_id, event: 'stopped', reason: h.stopped.reason });
    }
  }
  const pages = SOURCES.filter((src) => {
    const h = s.hosts[src.source_id];
    return !h.stopped && h.robots_day === day && h.robots_allowed === true;
  }).map((src) => ({ source_id: src.source_id, url: src.url, wait_ms: Math.max(5000, (s.hosts[src.source_id].crawl_delay || 0) * 1000) }));
  return { state: s, pages, events };
}

/** Stage 'pages': the answers to the pages become the files to save and the run's register. */
function afterPages({ state, now, started_at, answers, robots_events }) {
  instant(now);
  instant(started_at);
  const s = freshState(state);
  const stamp = compactInstant(started_at);
  const files = [];
  const hosts = [];
  const seq = {};
  for (const a of answers || []) {
    const h = s.hosts[a.source_id];
    if (!h) throw new Error(`page answer for an unknown source: ${a.source_id}`);
    seq[a.source_id] = (seq[a.source_id] || 0) + 1;
    const signal = blockSignal(a);
    const code = Number(a.statusCode);
    let outcome;
    if (signal) {
      h.stopped = { at: now, reason: signal };
      outcome = { source_id: a.source_id, status: code, outcome: 'stopped', reason: signal };
    } else if (code === 200) {
      h.errors_in_row = 0;
      const type = String((a.headers || {})['content-type'] || '');
      const ext = /xml|rss|atom/i.test(type) ? 'xml' : /json/i.test(type) ? 'json' : 'html';
      // One file per answer: the number of the host's answer in the run keeps every name apart.
      const name = `notizie_${a.source_id}_${stamp}_${seq[a.source_id]}.${ext}`;
      files.push({ name, body: bodyText(a) });
      outcome = { source_id: a.source_id, status: code, outcome: 'saved', file: `originali/${name}` };
    } else {
      h.errors_in_row = (h.errors_in_row || 0) + 1;
      if (code >= 500 || !Number.isFinite(code)) {
        if (h.errors_in_row >= ERRORS_TO_STOP) h.stopped = { at: now, reason: `${ERRORS_TO_STOP} errors in a row` };
      }
      outcome = { source_id: a.source_id, status: Number.isFinite(code) ? code : null, outcome: h.stopped ? 'stopped' : 'error',
        reason: h.stopped ? h.stopped.reason : `HTTP ${a.statusCode}` };
    }
    hosts.push(outcome);
  }
  const stopped = Object.entries(s.hosts).filter(([, h]) => h.stopped).map(([id, h]) => ({ source_id: id, since: h.stopped.at, reason: h.stopped.reason }));
  return {
    state: s,
    files,
    log_file_name: `notizie_${stamp}.json`,
    log: { workflow: 'staging_B_notizie_raccolta', started_at, finished_at: now, user_agent: USER_AGENT,
      robots: robots_events || [], hosts, stopped },
  };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { SOURCES, USER_AGENT, AGENT_TOKENS, ERRORS_TO_STOP, urlParts, parseRobots, ruleMatches, groupAllows,
    robotsVerdict, blockSignal, planRun, afterRobots, afterPages };
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
  delete $json.answers;
} else if ($json.stage === 'pages') {
  out = afterPages({ state: store.news_collect, now: $json.now, started_at: $json.started_at, answers: $json.answers,
    robots_events: $json.robots_events });
  $json.files = out.files;
  $json.log_file_name = out.log_file_name;
  $json.log = out.log;
  delete $json.answers;
} else {
  throw new Error(`unknown stage ${JSON.stringify($json.stage)}`);
}
store.news_collect = out.state;
return $input.item;

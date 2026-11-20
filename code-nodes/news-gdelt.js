/**
 * news-gdelt.js — workstream B, the two-week measure of GDELT as the third-party index of the
 * closed outlets (DEC-039, point 4; DEC-108): which searches a run asks GDELT's search service
 * for, what robots.txt allows, which answers stop the host, and which rows, register and alert a
 * run writes. The rules are in docs/pilota/CONTRATTI.md, section 7 («B · Notizie», row «Misura
 * GDELT»); this file does not restate them. It keeps title, link, hour and domain of each article
 * and the search that found it, never the article; nothing it writes enters the grouping.
 *
 * The robots.txt reading and the answers that stop a host are copies of news-collect.js, because
 * an n8n Code node cannot require another file; tests/test_news_gdelt.js keeps them byte-equal.
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item") the same file runs
 * its adapter, keeping the state of the host and of each search in the workflow's static data.
 * `stage` on the item says which step it takes:
 *   - 'plan': the robots.txt to read before this run's searches (once a Rome day);
 *   - 'robots': its answer, and the searches of the run with their windows;
 *   - 'before': before each search, whether the host stopped, answered 429 or went unanswered
 *     earlier in the run;
 *   - 'answer': one answer becomes its rows and its outcome;
 *   - 'close': the outcomes become the run's rows file, register and alert, and the state the run
 *     leaves, kept apart until
 *   - 'commit': after the files are on Drive, that state becomes the state of the flow.
 * The requests, the pause before each and the files belong to the workflow.
 */
'use strict';

/** The search service and its host (CONTRATTI.md section 7 B, «Misura GDELT»). */
const HOST = 'api.gdeltproject.org';
const API_URL = 'https://api.gdeltproject.org/api/v2/doc/doc';
const API_PATH = '/api/v2/doc/doc';
const ROBOTS_URL = 'https://api.gdeltproject.org/robots.txt';

/** The pilot pages (CONTRATTI.md section 1) with the search query that gazetteer/gazetteer.json
 *  gives each (`publication_zones[].search_queries`); the tests keep them equal to the gazetteer. */
const PAGES = Object.freeze([
  Object.freeze({ zone: 'acilia', query: 'Acilia' }),
  Object.freeze({ zone: 'centocelle', query: 'Centocelle' }),
  Object.freeze({ zone: 'prati', query: 'Prati' }),
]);
/** The language of a page search, as the service names it (CONTRATTI.md section 7 B, «Misura GDELT»). */
const LANGUAGE = 'italian';
/** The outlets searched by domain: those DEC-108 reads only from a third-party index (`closed`), and
 *  the two open outlets of the collection (CONTRATTI.md section 7 B, «Fonti al 10 novembre 2026»),
 *  whose own feeds tell how much of them the index sees. */
const OUTLETS = Object.freeze([
  Object.freeze({ domain: 'romatoday.it', closed: true }),
  Object.freeze({ domain: 'ilmessaggero.it', closed: true }),
  Object.freeze({ domain: 'ansa.it', closed: true }),
  Object.freeze({ domain: 'corriere.it', closed: true }),
  Object.freeze({ domain: 'repubblica.it', closed: true }),
  Object.freeze({ domain: 'leggo.it', closed: true }),
  Object.freeze({ domain: 'today.it', closed: true, exact: true }),
  Object.freeze({ domain: 'agenzianova.com', closed: true }),
  Object.freeze({ domain: 'abitarearoma.it', closed: false }),
  Object.freeze({ domain: 'ilfaroonline.it', closed: false }),
]);

/** The numbers of CONTRATTI.md section 7 B, «Misura GDELT»: the pause before each request, the
 *  most articles one answer gives, the step at which the service adds coverage and how far behind
 *  the run stays, the longest window, where the measure starts and ends, and the instant from which
 *  a run asks nothing. */
const PAUSE_MS = 10000;
const MAX_RECORDS = 250;
const SLOT_MS = 15 * 60 * 1000;
const LAG_MS = 15 * 60 * 1000;
const MAX_WINDOW_MS = 24 * 60 * 60 * 1000;
const START_UTC = '2026-11-19T21:00:00Z';
const END_UTC = '2026-12-03T23:00:00Z';
const ASK_UNTIL_UTC = '2026-12-04T01:00:00Z';
/** How many runs in a row with a 429 stop the host (DEC-045, the owner's choice of 20 November 2026),
 *  and with a server error or no answer (CONTRATTI.md section 7 B, «Raccolta»: ERRORS_TO_STOP). */
const THROTTLED_RUNS_TO_STOP = 6;

/* ----- copies of news-collect.js, kept byte-equal by the tests ------------ */

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
    } else if (key === 'allow' || key === 'disallow' || key === 'crawl-delay') {
      lastWasAgent = false;
      if (!current) continue;
      if (key === 'crawl-delay') current.crawl_delay = Number(value);
      else current.rules.push({ allow: key === 'allow', path: value });
    }
    // Any other record (Sitemap and the like) neither ends a group nor starts one (RFC 9309, 2.2.4).
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


/* ----- the searches and their windows ------------------------------------ */

const isoOf = (ms) => new Date(ms).toISOString().slice(0, 19) + 'Z';
/** The service's form of an instant, `YYYYMMDDHHMMSS` in UTC. */
const serviceStamp = (ms) => new Date(ms).toISOString().slice(0, 19).replace(/[-:T]/g, '');
/** A host as CONTRATTI.md section 2 writes `source_id`: lower case, without `www.`. */
const siteOf = (u) => hostOf(u).replace(/^www\./, '');
const belongsTo = (site, domain) => site === domain || site.endsWith('.' + domain);
const RUN_MS = 2 * 60 * 60 * 1000;

/** Every search, page searches first: its id, the query sent and, for an outlet, its domain. The
 *  service's `domain:` matches every name that ends with the domain, subdomains (the Rome sections of
 *  an outlet) and other sites alike, and the rows keep only the outlet and its subdomains; an outlet
 *  whose domain ends the names of other outlets (OUTLETS, `exact`) is searched with `domainis:`. */
function searches() {
  return PAGES.map((p) => ({ id: `pagina:${p.zone}`, query: `${/\s/.test(p.query) ? `"${p.query}"` : p.query} sourcelang:${LANGUAGE}` }))
    .concat(OUTLETS.map((o) => ({ id: `testata:${o.domain}`, query: `${o.exact ? 'domainis' : 'domain'}:${o.domain}`, domain: o.domain })));
}

/** The searches in the order a run asks them: the list turned by one place every two hours, so the
 *  search a 429 or a missing answer leaves unasked is among the first in a later run. */
function searchOrder(now) {
  const list = searches();
  const k = Math.floor(Date.parse(now) / RUN_MS) % list.length;
  return list.slice(k).concat(list.slice(0, k));
}

/** The request of a window. The service takes articles «after» its start and «before» its end, and
 *  does not say whether an instant on the edge is in: the request starts a second early, and the
 *  answer keeps only `from <= seen < until` (afterAnswer), so an article on an edge between two
 *  windows is in one of them. */
function searchUrl(query, fromMs, untilMs) {
  return `${API_URL}?query=${encodeURIComponent(query)}&mode=artlist&format=json&maxrecords=${MAX_RECORDS}` +
    `&sort=datedesc&startdatetime=${serviceStamp(fromMs - 1000)}&enddatetime=${serviceStamp(untilMs)}`;
}

/** The window of each search: from where it was last read (from START_UTC for a search never read)
 *  to the last step of the service LAG_MS behind `now`, never past END_UTC. A window longer than
 *  MAX_WINDOW_MS keeps its last part, and the part left out is named (`lost_from`); closeRun moves the
 *  start past it, so a part is named once. `run`, the start of the run, goes with each request. */
function windows(s, now, pauseMs, run) {
  const end = Math.min(Math.floor(Date.parse(now) / SLOT_MS) * SLOT_MS - LAG_MS, Date.parse(END_UTC));
  const out = [];
  for (const q of searchOrder(now)) {
    let from = Date.parse(s.until[q.id] || START_UTC);
    let lost_from = null;
    if (end - from > MAX_WINDOW_MS) { lost_from = isoOf(from); from = end - MAX_WINDOW_MS; }
    if (end <= from) continue;
    out.push({ stage: 'before', id: q.id, url: searchUrl(q.query, from, end), from: isoOf(from), until: isoOf(end), lost_from, wait_ms: pauseMs, run: run || null });
  }
  return out;
}

function freshState(state) {
  const s = state && typeof state === 'object' ? JSON.parse(JSON.stringify(state)) : {};
  s.host = Object.assign({ stopped: null, robots_day: null, robots_allowed: null, errors_in_row: 0, throttled_runs: 0,
    throttled_run: null, unread_run: null, unread_reason: null }, s.host);
  s.until = s.until && typeof s.until === 'object' ? s.until : {};
  s.over_notice = s.over_notice || null;
  return s;
}

/** From ASK_UNTIL_UTC a run asks nothing: the run that closes the last window comes before it. */
const measureOver = (now) => Date.parse(now) >= Date.parse(ASK_UNTIL_UTC);

/** Stage 'plan': the robots.txt to read before this run's searches, once a Rome day, unless the host
 *  is stopped or the measure is over. */
function planRun({ state, now }) {
  const day = romeDay(instant(now));
  const s = freshState(state);
  const ended = measureOver(now);
  const robots = !s.host.stopped && !ended && s.host.robots_day !== day ? [{ source_id: HOST, url: ROBOTS_URL }] : [];
  return { state: s, robots, ended };
}

/** Stage 'robots': the answer to robots.txt (`{ statusCode, headers, body, error }`, or none when it
 *  was read earlier today) updates the host; when the host is allowed today the searches of the run
 *  are the requests. robots.txt is read as news-collect.js reads it, with the differences that the
 *  contract states: an answer 404 or 410 means the host has no robots.txt (RFC 9309, 2.3.1.3), a 429
 *  ends the run instead of stopping the host, and a server error or no answer leaves the host unread
 *  in the run, counted by closeRun. `now` is the run, as `started_at` is in closeRun. */
function afterRobots({ state, now, answers }) {
  const day = romeDay(instant(now));
  const s = freshState(state);
  const h = s.host;
  const events = [];
  const stopped_now = [];
  const stop = (reason) => { h.stopped = { at: now, reason }; stopped_now.push({ source_id: HOST, reason }); };
  for (const a of answers || []) {
    const code = statusOf(a);
    if (code === 429) {
      h.throttled_run = now;
      events.push({ source_id: HOST, url: ROBOTS_URL, status: 429, outcome: 'throttled', reason: 'robots.txt: HTTP 429' });
      continue;
    }
    // An HTML document is a page whatever type it is served with; one served as HTML that holds no rule
    // is a page too, never an empty set of rules that allows everything.
    const htmlPage = code === 200 && (/<!doctype\s+html|<html[\s>]|<body[\s>]/i.test(bodyText(a)) ||
      (/html/i.test(String((a.headers || {})['content-type'] || '')) && parseRobots(bodyText(a)).length === 0));
    const signal = blockSignal(code !== 200 ? a
      : htmlPage ? Object.assign({}, a, { headers: Object.assign({}, a.headers, { 'content-type': 'text/html' }) })
        : Object.assign({}, a, { body: '' }), ROBOTS_URL);
    let outcome;
    let reason = null;
    let server_error = false;
    if (signal) {
      stop(`robots.txt: ${signal}`);
      outcome = 'stopped';
    } else if (code >= 300 && code < 400) {
      outcome = 'moved';
      reason = `moved to ${(a.headers || {}).location || ''}`;
    } else if (code >= 500 || !Number.isFinite(code)) {
      h.unread_run = now;
      h.unread_reason = `robots.txt: ${failure(a)}`;
      outcome = 'error';
      reason = h.unread_reason;
      server_error = true;
    } else if (code === 404 || code === 410) {
      Object.assign(h, { robots_day: day, robots_allowed: true, crawl_delay: null });
      outcome = 'allowed';
      reason = `no robots.txt (HTTP ${code})`;
    } else if (code !== 200) {
      stop(`robots.txt: HTTP ${a.statusCode}`);
      outcome = 'stopped';
    } else if (htmlPage) {
      stop('robots.txt unreadable: an HTML page instead of the rules');
      outcome = 'stopped';
    } else {
      let v = null;
      try {
        v = robotsVerdict(bodyText(a), API_PATH);
      } catch (e) {
        stop('robots.txt unreadable');
      }
      if (v) {
        Object.assign(h, { robots_day: day, robots_allowed: v.allowed, crawl_delay: v.crawl_delay });
        if (!v.allowed) stop('robots.txt disallows the search');
      }
      outcome = h.stopped ? 'stopped' : 'allowed';
    }
    events.push(Object.assign({ source_id: HOST, url: ROBOTS_URL, status: Number.isFinite(code) ? code : null, outcome,
      reason: h.stopped ? h.stopped.reason : reason }, server_error ? { server_error } : {}));
  }
  const allowed = !h.stopped && !measureOver(now) && h.throttled_run !== now && h.unread_run !== now &&
    h.robots_day === day && h.robots_allowed === true;
  const requests = allowed ? windows(s, now, Math.max(PAUSE_MS, (h.crawl_delay || 0) * 1000), now) : [];
  return { state: s, requests, events, stopped_now };
}

/** Stage 'before': a search is not sent once the host has stopped, earlier in this run too, nor after
 *  a 429 or a server error or no answer earlier in its run. */
function beforeRequest({ state, request }) {
  const s = freshState(state);
  const h = s.host;
  const run = request.run || null;
  const reason = h.stopped ? `host stopped: ${h.stopped.reason}`
    : run && h.throttled_run === run ? 'HTTP 429 earlier in this run'
      : run && h.unread_run === run ? `host not read in this run: ${h.unread_reason}` : null;
  if (!reason) return { state: s, skip: false };
  return { state: s, skip: true, result: { id: request.id, from: request.from, until: request.until, lost_from: request.lost_from || null,
    status: null, outcome: 'skipped', reason } };
}

/** The instant of an article, from the service's `seendate` (`YYYYMMDDTHHMMSSZ`), or null. */
function seenAt(v) {
  const m = /^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z$/.exec(typeof v === 'string' ? v : '');
  if (!m) return null;
  const iso = `${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:${m[6]}Z`;
  return Number.isNaN(Date.parse(iso)) || isoOf(Date.parse(iso)) !== iso ? null : iso;
}

/** Stage 'answer': one answer to a search (`{ statusCode, headers, body, error }`) becomes its outcome
 *  and its rows. A 429, a server error or no answer end the requests of its run (`request.run`) and
 *  stop nothing: closeRun counts them. A row has only `url`, `title`, `seen_at_utc` and `source_id`; an
 *  article outside the window, of another site in an outlet search, or without a link or an instant
 *  is counted, not kept. */
function afterAnswer({ state, now, request, answer }) {
  instant(now);
  const s = freshState(state);
  const h = s.host;
  const a = answer || {};
  const code = statusOf(a);
  const result = { id: request.id, from: request.from, until: request.until, lost_from: request.lost_from || null,
    status: Number.isFinite(code) ? code : null };
  if (code === 429) {
    h.throttled_run = request.run || null;
    return { state: s, result: Object.assign(result, { outcome: 'throttled', reason: 'HTTP 429' }) };
  }
  const signal = blockSignal(a, request.url);
  if (signal) {
    h.stopped = { at: now, reason: signal };
    return { state: s, result: Object.assign(result, { outcome: 'stopped', reason: signal }) };
  }
  if (code >= 500 || !Number.isFinite(code)) {
    h.unread_run = request.run || null;
    h.unread_reason = failure(a);
    return { state: s, result: Object.assign(result, { outcome: 'error', reason: failure(a), server_error: true }) };
  }
  if (code !== 200) {
    const moved = code >= 300 && code < 400;
    return { state: s, result: Object.assign(result, { outcome: moved ? 'moved' : 'error',
      reason: moved ? `moved to ${(a.headers || {}).location || ''}` : `HTTP ${a.statusCode}` }) };
  }
  let doc;
  try {
    doc = JSON.parse(bodyText(a));
  } catch (e) {
    doc = undefined;
  }
  if (!doc || typeof doc !== 'object' || Array.isArray(doc) || (doc.articles !== undefined && !Array.isArray(doc.articles))) {
    // The service answers a query it does not take with a sentence of its own, not with JSON.
    return { state: s, result: Object.assign(result, { outcome: 'unreadable', reason: 'not the JSON of a search',
      excerpt: bodyText(a).replace(/\s+/g, ' ').trim().slice(0, 200) }) };
  }
  const articles = doc.articles || [];
  const search = searches().find((q) => q.id === request.id);
  if (!search) throw new Error(`an answer for an unknown search: ${request.id}`);
  const fromMs = Date.parse(request.from);
  const untilMs = Date.parse(request.until);
  const counts = { returned: articles.length, kept: 0, outside_window: 0, other_site: 0, malformed: 0, without_title: 0 };
  const per_outlet = {};
  const rows = [];
  const seen = new Set();
  for (const art of articles) {
    const url = art && typeof art.url === 'string' && /^https?:\/\/[^/?#\s]+/i.test(art.url.trim()) ? art.url.trim() : null;
    const at = art ? seenAt(art.seendate) : null;
    if (!url || !at) { counts.malformed += 1; continue; }
    const t = Date.parse(at);
    if (t < fromMs || t >= untilMs) { counts.outside_window += 1; continue; }
    const site = siteOf(url);
    if (search.domain && !belongsTo(site, search.domain)) { counts.other_site += 1; continue; }
    if (seen.has(url)) continue;
    seen.add(url);
    const title = typeof art.title === 'string' ? art.title.replace(/\s+/g, ' ').trim() : '';
    if (!title) counts.without_title += 1;
    rows.push({ url, title, seen_at_utc: at, source_id: site });
    const outlet = OUTLETS.find((o) => belongsTo(site, o.domain));
    const key = outlet ? outlet.domain : 'other';
    per_outlet[key] = (per_outlet[key] || 0) + 1;
  }
  counts.kept = rows.length;
  return { state: s, result: Object.assign(result, { outcome: 'read', reason: null }, counts,
    { truncated: articles.length >= MAX_RECORDS, per_outlet, rows }) };
}

/** Stage 'close': the outcomes of the run (`results`) move the window of each search that was read
 *  (and, for one left unread, its start past a part named as lost), and become the rows file, one
 *  row per link with the searches that found it, the register and, when the host stopped in this run,
 *  the alert. A run with a 429 adds one to the runs in a row with a 429, a run with a server error or
 *  no answer one to the runs in a row with one; the THROTTLED_RUNS_TO_STOP-th and the
 *  ERRORS_TO_STOP-th stop the host; every run without one, one that asked nothing too, sets that
 *  count back to zero: the runs are in a row. A run of an ended measure writes one notice the first time
 *  and nothing after. The state returned is for 'commit', after the files are written. */
function closeRun({ state, now, started_at, results, robots_events, robots_stopped, ended, workflow_version }) {
  instant(now);
  instant(started_at);
  const s = freshState(state);
  const h = s.host;
  const stamp = compactInstant(started_at);
  const nothing = { state: s, rows: [], rows_file_name: null, log_file_name: null, log: null, alert_file_name: null, alert: null };
  if (ended) {
    if (s.over_notice) return nothing;
    s.over_notice = now;
    const left = searches().filter((q) => !s.until[q.id] || Date.parse(s.until[q.id]) < Date.parse(END_UTC))
      .map((q) => ({ id: q.id, from: s.until[q.id] || START_UTC, until: END_UTC }));
    return Object.assign(nothing, { alert_file_name: `AVVISO_gdelt_fine_${stamp}.json`,
      alert: { avviso: 'la misura di GDELT è finita: il coordinatore spegne staging_B_gdelt_misura', workflow: 'staging_B_gdelt_misura',
        workflow_version: workflow_version || null, measure_end: END_UTC, at: now, windows_not_read: left } });
  }
  const byUrl = new Map();
  const requests = [];
  const stopped_now = Array.isArray(robots_stopped) ? robots_stopped.slice() : [];
  const events = robots_events || [];
  const throttled = events.some((e) => e && e.outcome === 'throttled') || (results || []).some((r) => r && r.outcome === 'throttled');
  const errored = events.some((e) => e && e.server_error) || (results || []).some((r) => r && r.server_error);
  for (const r of results || []) {
    if (!r || typeof r.id !== 'string' || !searches().some((q) => q.id === r.id)) throw new Error(`an outcome for an unknown search: ${r && r.id}`);
    if (r.outcome === 'read') s.until[r.id] = r.until;
    else if (r.lost_from) s.until[r.id] = r.from;
    if (r.outcome === 'stopped') stopped_now.push({ source_id: HOST, reason: r.reason });
    for (const row of r.rows || []) {
      const prev = byUrl.get(row.url);
      if (prev) { if (!prev.searches.includes(r.id)) prev.searches.push(r.id); } else byUrl.set(row.url, Object.assign({}, row, { searches: [r.id] }));
    }
    requests.push(Object.assign({}, r, { rows: undefined }));
  }
  const count = (key, hit, limit, reason) => {
    if (hit) {
      h[key] = (h[key] || 0) + 1;
      if (!h.stopped && h[key] >= limit) { h.stopped = { at: now, reason }; stopped_now.push({ source_id: HOST, reason }); }
    } else {
      h[key] = 0;
    }
  };
  count('throttled_runs', throttled, THROTTLED_RUNS_TO_STOP, `HTTP 429 in ${THROTTLED_RUNS_TO_STOP} runs in a row`);
  count('errors_in_row', errored, ERRORS_TO_STOP, `a server error or no answer in ${ERRORS_TO_STOP} runs in a row`);
  if (h.throttled_run === started_at) h.throttled_run = null;
  if (h.unread_run === started_at) { h.unread_run = null; h.unread_reason = null; }
  const previous_write_failure = Array.isArray(s.write_failures) && s.write_failures.length ? s.write_failures : null;
  delete s.write_failures;
  const rows = [...byUrl.values()].sort((x, y) => (x.seen_at_utc < y.seen_at_utc ? -1 : x.seen_at_utc > y.seen_at_utc ? 1 : x.url < y.url ? -1 : x.url > y.url ? 1 : 0));
  return {
    state: s,
    rows,
    rows_file_name: rows.length ? `gdelt_righe_${stamp}.json` : null,
    log_file_name: `gdelt_${stamp}.json`,
    alert_file_name: stopped_now.length || previous_write_failure ? `AVVISO_gdelt_${stamp}.json` : null,
    alert: stopped_now.length || previous_write_failure ? { avviso: [stopped_now.length ? 'host fermato in questa corsa' : null,
      previous_write_failure ? 'i file di una corsa precedente non sono stati scritti' : null].filter(Boolean).join('; ') + ': avvisare il coordinatore',
    stopped_now, previous_write_failure, started_at } : null,
    log: { workflow: 'staging_B_gdelt_misura', workflow_version: workflow_version || null, started_at, finished_at: now,
      user_agent: USER_AGENT, host: HOST, measure_start: START_UTC, measure_end: END_UTC, spend_eur: 0, robots: events,
      requests: requests.map((r) => JSON.parse(JSON.stringify(r))), rows: rows.length, throttled, server_error: errored,
      throttled_runs: h.throttled_runs, error_runs: h.errors_in_row, previous_write_failure, stopped_now,
      stopped: h.stopped ? { source_id: HOST, since: h.stopped.at, reason: h.stopped.reason } : null },
  };
}

/** Stage 'commit', after the files of the run (`failed`: the ones a Drive node did not write). Only
 *  when the rows and the register are written does the state the run left (`pending`) become the
 *  state of the flow; otherwise the flow keeps its own, with the stops already in it, and the next
 *  run reads the windows again. A file not written is named in the state, and the next run's
 *  register and alert say so. */
function commitRun({ state, pending, failed, started_at, now }) {
  const lost = Array.isArray(failed) ? failed.filter((f) => typeof f === 'string' && f) : [];
  const keep = !pending || lost.includes('righe') || lost.includes('registro');
  const s = freshState(keep ? state : pending);
  if (keep && pending && pending.host && pending.host.stopped && !s.host.stopped) s.host.stopped = pending.host.stopped;
  if (lost.length) s.write_failures = (Array.isArray(s.write_failures) ? s.write_failures : []).concat([{ run: started_at || null, files: lost, at: now || null }]);
  return { state: s, committed: !keep };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { HOST, API_URL, API_PATH, ROBOTS_URL, PAGES, LANGUAGE, OUTLETS, PAUSE_MS, MAX_RECORDS, SLOT_MS, LAG_MS,
    MAX_WINDOW_MS, START_UTC, END_UTC, ASK_UNTIL_UTC, THROTTLED_RUNS_TO_STOP, USER_AGENT, AGENT_TOKENS, ERRORS_TO_STOP, urlParts,
    parseRobots, ruleMatches, groupAllows, robotsVerdict, resolveLocation, blockSignal, searches, searchOrder, searchUrl, windows,
    seenAt, planRun, afterRobots, beforeRequest, afterAnswer, closeRun, commitRun };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter: the state of the host and of each search
 * lives in the workflow's static data, saved by n8n when an execution ends. The search being sent
 * waits in `news_gdelt_request` from 'before' to 'answer'. The state a run leaves waits in
 * `news_gdelt_pending` until 'commit', after the files: the Drive nodes go on when they fail, so the
 * execution ends and its static data is saved, and commitRun decides what of the run holds; the
 * stops, the one decided at the close too, and the marks of the run hold at once. */
const store = $getWorkflowStaticData('global');
let out;
if ($json.stage === 'plan') {
  delete store.news_gdelt_pending;
  delete store.news_gdelt_request;
  out = planRun({ state: store.news_gdelt, now: $json.now });
  $json.robots = out.robots;
  $json.ended = out.ended;
  store.news_gdelt = out.state;
} else if ($json.stage === 'robots') {
  out = afterRobots({ state: store.news_gdelt, now: $json.now, answers: $json.answers });
  $json.requests = out.requests;
  $json.robots_events = out.events;
  $json.robots_stopped = out.stopped_now;
  delete $json.answers;
  store.news_gdelt = out.state;
} else if ($json.stage === 'before') {
  out = beforeRequest({ state: store.news_gdelt, request: $json });
  delete store.news_gdelt_request;
  if (out.skip) {
    for (const k of Object.keys($json)) delete $json[k];
    Object.assign($json, out.result, { skip: true });
  } else {
    $json.skip = false;
    // The search about to be sent: its answer is judged against it, with no lookup of an earlier node.
    store.news_gdelt_request = { id: $json.id, url: $json.url, from: $json.from, until: $json.until, lost_from: $json.lost_from || null, run: $json.run || null };
  }
  store.news_gdelt = out.state;
} else if ($json.stage === 'answer') {
  const request = store.news_gdelt_request;
  if (!request) throw new Error('an answer with no search sent before it');
  delete store.news_gdelt_request;
  out = afterAnswer({ state: store.news_gdelt, now: $json.now, request,
    answer: { statusCode: $json.statusCode, headers: $json.headers, body: $json.body, error: $json.error } });
  for (const k of Object.keys($json)) delete $json[k];
  Object.assign($json, out.result);
  store.news_gdelt = out.state;
} else if ($json.stage === 'close') {
  out = closeRun({ state: store.news_gdelt, now: $json.now, started_at: $json.started_at, results: $json.results,
    robots_events: $json.robots_events, robots_stopped: $json.robots_stopped, ended: $json.ended, workflow_version: $json.workflow_version });
  for (const k of ['rows', 'rows_file_name', 'log_file_name', 'log', 'alert_file_name', 'alert']) $json[k] = out[k];
  delete $json.results;
  store.news_gdelt_pending = out.state;
  // A stop decided here holds at once, as a stop by a signal does: files that fail leave the run to
  // be read again, never the host to be asked again.
  if (out.state.host.stopped && !store.news_gdelt.host.stopped) store.news_gdelt.host.stopped = out.state.host.stopped;
} else if ($json.stage === 'commit') {
  out = commitRun({ state: store.news_gdelt, pending: store.news_gdelt_pending, failed: $json.failed, started_at: $json.started_at, now: $json.now });
  store.news_gdelt = out.state;
  delete store.news_gdelt_pending;
  $json.committed = out.committed;
} else {
  throw new Error(`unknown stage ${JSON.stringify($json.stage)}`);
}
return $input.item;

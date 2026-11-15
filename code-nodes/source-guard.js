/**
 * source-guard.js — workstream A: what guards every request the channel makes to its sources —
 * the hosts it may ask, the one user agent, the pause after an answer, the answers that stop a
 * host, the streak of server errors, the daily check of robots.txt against the rules read on
 * 14 November 2026, the state of a host between runs and the alert of a stop. The rules are in
 * docs/pilota/CONTRATTI.md, section 7 («A · Amministrazione», rows Fonti and Raccolta), DEC-036
 * point 2 and DEC-037 point 2; this file does not restate them. The state of a host lives in a
 * row of the Data table (recording-state.js). Acceptance: tests/test_source_guard.js (T-A2-07,
 * T-A2-08, T-A2-10, T-A2-12).
 *
 * ONE SOURCE, TWO CONTEXTS (code-nodes/README.md): under plain Node `$input` is undefined, so the
 * tail exports and stops; inside the n8n Code node ("Run Once for Each Item") the same file runs
 * its adapter. `stage` on the item says which step it takes:
 *   - 'may': whether a host may be asked now, before an HTTP Request node asks it (the Apify
 *     nodes, which need the credential);
 *   - 'fetch': one request, after the pause its host needs, and the verdict on its answer; the
 *     node gets one item per execution, so that pause and request stay inside its 60 seconds;
 *   - 'answer': the verdict on an answer an HTTP Request node got, and the host's new state;
 *   - 'robots': the verdict on a robots.txt answer, and the host's new state.
 * A stage that stops a host gives the alert to write before the host's row (WORKSTREAM_A,
 * section 4, «La presa»: the file first, then the row).
 */
'use strict';

/** CONTRATTI section 7 (A), row Raccolta: the one user agent, that of code-nodes/news-collect.js. */
const USER_AGENT = 'QuartieriNews-staging/0.1 (+https://quartierinews.it)';
const ERRORS_TO_STOP = 5;
/** A request and its pause end before the 60 seconds of an n8n Code node (WORKSTREAM_A, section 6). */
const TIMEOUT_MS = 45000;
const DAY_MS = 24 * 3600 * 1000;

/** The hosts the channel may ask (CONTRATTI section 7 (A), rows Fonti and Raccolta): the pause
 *  after an answer and the kind of robots.txt read on 14 November 2026. `robots: null` is a
 *  service with a key, not a site. Any other host is refused. A stop for changed rules is lifted
 *  by changing `robots` here, in a PR: emptying the stop in the row stops the host again at its
 *  next check. */
const HOSTS = Object.freeze({
  'api-ovp.streamcloud.it': Object.freeze({ source: 'romatv', pause_ms: 5000, robots: 'unreadable' }),
  'streaming.comune.roma.it': Object.freeze({ source: 'romatv', pause_ms: 5000, robots: 'allow_all' }),
  'ac104mp.streamcloud.it': Object.freeze({ source: 'romatv', pause_ms: 5000, robots: 'allow_all' }),
  'ovp2-live.akamaized.net': Object.freeze({ source: 'romatv', pause_ms: 1000, robots: 'html' }),
  'api.apify.com': Object.freeze({ source: 'apify', pause_ms: 0, robots: null }),
});
/** The only extra headers a request may carry: those of the portal's player (DEC-036, point 2). */
const PORTAL_HEADERS = Object.freeze({ Origin: 'https://streaming.comune.roma.it', Referer: 'https://streaming.comune.roma.it/' });

const ROME_DAY = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' });
const romeDay = (iso) => ROME_DAY.format(new Date(iso));
const DAY = /^\d{4}-\d{2}-\d{2}$/;
/** The day after `day` (YYYY-MM-DD), counted on the calendar, not in hours. */
function nextDay(day) {
  const d = new Date(`${day}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + 1);
  return d.toISOString().slice(0, 10);
}
function instant(v) {
  if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(v) || Number.isNaN(Date.parse(v))) {
    throw new Error('now must be a UTC instant');
  }
  return v;
}

const hostOf = (u) => ((/^https:\/\/([^/?#:]+)(?::\d+)?(?:[/?#]|$)/i.exec(u || '') || [])[1] || '').toLowerCase();
const pathOf = (u) => (/^https:\/\/[^/?#]+(\/[^?#]*)?/i.exec(u || '') || [])[1] || '/';

/** The host of a URL the channel may ask, or an error: only https, only HOSTS. */
function allowedHost(url) {
  const host = hostOf(url);
  if (!host || !Object.prototype.hasOwnProperty.call(HOSTS, host)) throw new Error(`host_not_allowed: ${host || url}`);
  return host;
}

/** The options of one request for this.helpers.httpRequest: the declared user agent and no
 *  other, no cookie and no login (DEC-037, point 2), the portal's headers only with their own
 *  values, no redirect followed (one to another host stops the host). A robots.txt request is
 *  only the robots.txt of its host. */
function requestOptions(req) {
  const r = req || {};
  allowedHost(r.url);
  if (r.robots === true && pathOf(r.url) !== '/robots.txt') throw new Error('robots_request_not_robots_txt');
  const headers = {};
  for (const [k, v] of Object.entries(r.headers || {})) {
    if (/^(origin|referer)$/i.test(k)) {
      const name = /^origin$/i.test(k) ? 'Origin' : 'Referer';
      if (v !== PORTAL_HEADERS[name]) throw new Error(`header_not_allowed: ${k}`);
      headers[name] = v;
    } else if (/^(accept|content-type)$/i.test(k)) {
      headers[k] = v;
    } else {
      throw new Error(`header_not_allowed: ${k}`);
    }
  }
  headers['User-Agent'] = USER_AGENT;
  const o = { method: r.method || 'GET', url: r.url, headers, returnFullResponse: true, ignoreHttpStatusErrors: true,
    disableFollowRedirect: true, timeout: TIMEOUT_MS };
  if (r.body !== undefined) { o.body = r.body; o.json = true; }
  if (r.encoding) o.encoding = r.encoding;
  return o;
}

/** T-A2-12: how long to wait before the next request to `host`, from the end of the last answer
 *  of the run. An end that is unknown or not plausible (not a positive time of the last day, or
 *  later than now) gives the whole pause; never more than the pause. */
function waitMs(host, lastEndMs, nowMs) {
  const pause = (HOSTS[host] || { pause_ms: 0 }).pause_ms;
  const known = typeof lastEndMs === 'number' && lastEndMs > nowMs - DAY_MS && lastEndMs <= nowMs;
  if (!known) return pause;
  return Math.min(pause, Math.max(0, lastEndMs + pause - nowMs));
}

const bodyText = (res) => {
  const b = res.body;
  if (typeof b === 'string') return b;
  if (b === undefined || b === null) return '';
  if (typeof Buffer !== 'undefined' && Buffer.isBuffer(b)) return b.subarray(0, 4096).toString('latin1');
  return JSON.stringify(b);
};
const header = (res, name) => {
  const h = res.headers || {};
  const k = Object.keys(h).find((x) => x.toLowerCase() === name);
  return k === undefined ? '' : String(h[k]);
};
const isHtml = (res) => /html/i.test(header(res, 'content-type')) || /^\s*(<!doctype html|<html[\s>])/i.test(bodyText(res));
const LOGIN = /(^|[/._?=&-])(login|logon|signin|sign-in|sso|auth|oauth|accedi|consent)([/._?=&-]|$)/i;
/** The marks of a challenge in the structure of a page (as code-nodes/news-collect.js), and of a
 *  sign-in form. */
const CHALLENGE = /class=["'][^"']*\b(g-recaptcha|h-captcha|cf-turnstile)\b|id=["']?(challenge-form|captcha)\b|recaptcha\/api\.js|hcaptcha\.com\/1\/api\.js|challenges\.cloudflare\.com|\/cdn-cgi\/challenge-platform\//i;
const PASSWORD = /<input[^>]+type=["']?password/i;

/** A page that is a challenge or a sign-in, whatever its status. */
function challengeOf(res) {
  if (!isHtml(res)) return null;
  const body = bodyText(res);
  if (CHALLENGE.test(body)) return 'captcha or anti-bot check';
  if (PASSWORD.test(body)) return 'login page';
  return null;
}

/** CONTRATTI section 7 (A), row Raccolta: the verdict on one answer to `url`, which was to bring
 *  `expects` ('json', 'text' or 'binary': always data). `outcome` is 'ok', 'block' (the host
 *  stops until the owner says), 'server_error' (the item stays unread and counts in the streak)
 *  or 'other' (the item stays unread; the streak ends). */
function verdict(res, url, expects) {
  if (!res || typeof res !== 'object' || res.error || res.statusCode === undefined || res.statusCode === null || res.statusCode === '') {
    return { outcome: 'server_error', reason: `no answer${res && res.error ? `: ${String(res.error).slice(0, 200)}` : ''}` };
  }
  const code = Number(res.statusCode);
  if (code === 401 || code === 403 || code === 429) return { outcome: 'block', reason: `HTTP ${code}` };
  if (code >= 300 && code < 400) {
    const loc = header(res, 'location');
    if (!loc) return { outcome: 'block', reason: 'redirect without a location' };
    if (/^[a-z][a-z0-9+.-]*:/i.test(loc) && !/^https?:\/\//i.test(loc)) return { outcome: 'block', reason: `redirect to ${loc.slice(0, 100)}` };
    const target = /^https?:\/\//i.test(loc) ? loc.replace(/^http:/i, 'https:') : loc.startsWith('//') ? `https:${loc}` : null;
    const toHost = target ? hostOf(target) : hostOf(url);
    if (toHost !== hostOf(url)) return { outcome: 'block', reason: `redirect to another host: ${toHost || loc.slice(0, 100)}` };
    if (LOGIN.test(loc)) return { outcome: 'block', reason: 'redirect to a sign-in or consent page' };
    return { outcome: 'other', reason: `HTTP ${code} within the host` };
  }
  const challenge = challengeOf(res);
  if (challenge) return { outcome: 'block', reason: challenge };
  if (code >= 500) return { outcome: 'server_error', reason: `HTTP ${code}` };
  if (code < 200 || code >= 300) return { outcome: 'other', reason: `HTTP ${code}` };
  if (code === 200 && isHtml(res)) return { outcome: 'block', reason: 'HTML page where the source sends data' };
  if (expects === 'json') {
    let v = res.body;
    if (typeof v === 'string') { try { v = JSON.parse(v); } catch (e) { v = null; } }
    if (v === null || typeof v !== 'object') return { outcome: 'other', reason: 'not JSON' };
  }
  return { outcome: 'ok', reason: null };
}

/** The state of a host, from its row of the Data table (recording-state.js, host rows). */
function hostState(row) {
  const r = row || {};
  return { fermo: r.fermo || '', fermo_fino: r.fermo_fino || '', errori_di_fila: Number(r.errori_di_fila) || 0,
    robots_giorno: r.robots_giorno || '', motivo: r.motivo || '' };
}

/** Whether a host is stopped now (CONTRATTI section 7 (A), row Raccolta). Any non-empty `fermo`
 *  other than `giorno` with a valid day, written by hand or not, is a stop by the owner. */
function isStopped(state, now) {
  const s = hostState(state);
  if (!s.fermo) return false;
  if (s.fermo === 'giorno' && DAY.test(s.fermo_fino)) return romeDay(instant(now)) < s.fermo_fino;
  return true;
}

/** A stop for a streak that has run out is lifted, and its streak with it. */
function current(state, now) {
  const s = hostState(state);
  if (s.fermo === 'giorno' && DAY.test(s.fermo_fino) && !isStopped(s, now)) {
    return Object.assign(s, { fermo: '', fermo_fino: '', errori_di_fila: 0, motivo: '' });
  }
  return s;
}

/** The host's new state after a verdict. `stopped_now` is set only by the answer that stops it. */
function afterVerdict(state, v, now) {
  const s = current(state, now);
  if (isStopped(s, now)) return { state: s, stopped_now: false };
  if (v.outcome === 'block') {
    return { state: Object.assign(s, { fermo: 'owner', fermo_fino: '', errori_di_fila: 0, motivo: `${now} ${v.reason}` }), stopped_now: true };
  }
  if (v.outcome === 'server_error') {
    s.errori_di_fila += 1;
    if (s.errori_di_fila >= ERRORS_TO_STOP) {
      Object.assign(s, { fermo: 'giorno', fermo_fino: nextDay(romeDay(instant(now))), motivo: `${now} ${ERRORS_TO_STOP} server errors in a row` });
      return { state: s, stopped_now: true };
    }
    return { state: s, stopped_now: false };
  }
  s.errori_di_fila = 0;
  return { state: s, stopped_now: false };
}

/** What a robots.txt answer is: 'allow_all' (rules that disallow nothing), 'rules' (anything
 *  else a robots.txt can say), 'html' (a page instead of the rules), 'absent' (a 4xx), 'moved'
 *  (a redirect within the host), 'unreadable' (a server error or no answer) or 'blocked' (a
 *  block signal: also a challenge or a sign-in page in place of the rules). */
function robotsKind(res, url) {
  const v = verdict(res, url, 'text');
  if (v.outcome === 'server_error') return 'unreadable';
  if (v.outcome === 'block' && v.reason !== 'HTML page where the source sends data') return 'blocked';
  const code = Number(res.statusCode);
  if (code >= 300 && code < 400) return 'moved';
  if (code !== 200) return 'absent';
  if (/<!doctype\s+html|<html[\s>]|<body[\s>]/i.test(bodyText(res))) return 'html';
  const restrictive = bodyText(res).split(/\r?\n/).map((l) => l.replace(/#.*$/, '').trim()).some((l) => {
    const m = /^([A-Za-z-]+)\s*:\s*(.*)$/.exec(l);
    if (!m) return false;
    const k = m[1].toLowerCase();
    return (k === 'disallow' && m[2].trim() !== '') || k === 'crawl-delay';
  });
  return restrictive ? 'rules' : 'allow_all';
}

/** T-A2-08: the daily check of one host, against CONTRATTI section 7 (A), row Raccolta (the
 *  builder's reading of an unreadable robots.txt is there). The same kind as on 14 November marks
 *  the day checked and, when it is an answer of the host and not its expected server error, ends
 *  the streak of server errors; any other kind stops the host until the owner says. */
function afterRobots(host, state, res, now) {
  const base = (HOSTS[host] || {}).robots;
  if (!base) throw new Error(`no robots.txt check for ${host}`);
  const s = current(state, now);
  const kind = robotsKind(res, `https://${host}/robots.txt`);
  if (kind === base) {
    s.robots_giorno = romeDay(instant(now));
    if (kind !== 'unreadable' && !isStopped(s, now)) s.errori_di_fila = 0;
    return { state: s, read: !isStopped(s, now), stopped_now: false, kind };
  }
  if (kind === 'unreadable') {
    const after = afterVerdict(s, { outcome: 'server_error', reason: 'robots.txt' }, now);
    return { state: after.state, read: false, stopped_now: after.stopped_now, kind };
  }
  if (isStopped(s, now) && s.fermo !== 'giorno') return { state: s, read: false, stopped_now: false, kind };
  Object.assign(s, { fermo: 'owner', fermo_fino: '', errori_di_fila: 0, motivo: `${now} robots.txt changed since 14 November 2026: ${base} -> ${kind}` });
  return { state: s, read: false, stopped_now: true, kind };
}

/** Whether a host needs its robots.txt checked before it is read today. */
function robotsDue(host, state, now) {
  return HOSTS[host].robots !== null && !isStopped(state, now) && hostState(state).robots_giorno !== romeDay(instant(now));
}

/** Whether a host may be read now: not stopped and, for a site, checked today. */
function mayRead(host, state, now) {
  if (!Object.prototype.hasOwnProperty.call(HOSTS, host) || isStopped(state, now)) return false;
  return HOSTS[host].robots === null || hostState(state).robots_giorno === romeDay(instant(now));
}

/** What a run keeps of an answer: the status, two headers and the body; never cookies. */
function keptAnswer(res) {
  if (!res || res.error || res.statusCode === undefined || res.statusCode === null) {
    return { statusCode: null, headers: {}, body: null, error: res && res.error ? String(res.error).slice(0, 200) : 'no answer' };
  }
  return { statusCode: res.statusCode, headers: { 'content-type': header(res, 'content-type'), location: header(res, 'location') }, body: res.body };
}

const stamp = (iso) => new Date(iso).toISOString().slice(0, 19).replace(/[-:]/g, '') + 'Z';
/** The alert of a host stopped now, named as those of staging_A_avviso; without a text of a source. */
function stopAlert(host, state, now, workflow) {
  return { name: `AVVISO_A_${stamp(now)}_${host.replace(/[^a-z0-9.-]/g, '_')}.json`,
    body: { avviso: 'il canale A ha fermato un host: avvisare l\'owner (CONTRATTI, sezione 7 A, «Raccolta»)', workflow: workflow || null,
      host, fermo: state.fermo, fermo_fino: state.fermo_fino || null, motivo: state.motivo, alle: now } };
}

/* ----- context switch: module under plain Node, adapter inside n8n ------- */

if (typeof $input === 'undefined') {
  module.exports = { USER_AGENT, ERRORS_TO_STOP, TIMEOUT_MS, HOSTS, PORTAL_HEADERS, romeDay, nextDay, hostOf, allowedHost,
    requestOptions, waitMs, verdict, hostState, isStopped, current, afterVerdict, robotsKind, afterRobots, robotsDue, mayRead,
    keptAnswer, stopAlert };
  return;
}

/* n8n Code node, "Run Once for Each Item" — the adapter. 'may' reads `host` and `host_state` and
 * writes `may_read`. 'fetch' reads `request` ({ url, method, body, headers, expects, encoding,
 * robots }), `host_state` (the host's row) and `last_end_ms` (the end of the run's last answer,
 * if any); it writes `answer`, `verdict` (null for robots.txt, judged by 'robots'), `host_state`,
 * `stopped_now`, `alert` and `last_end_ms`. A stopped host, or a site not checked today, is not
 * asked. 'answer' reads `url`, `expects`, `answer` and `host_state`; 'robots' reads `host`,
 * `host_state` and `answer`. Every stage that stops a host writes `alert`. */
const now = () => new Date().toISOString();
const withAlert = (host, after) => (after.stopped_now ? stopAlert(host, after.state, now(), $json.workflow) : null);
if ($json.stage === 'may') {
  $json.may_read = mayRead(allowedHost(`https://${$json.host}/`), $json.host_state, now());
  return $input.item;
}
if ($json.stage === 'fetch') {
  const req = $json.request || {};
  const host = allowedHost(req.url);
  const options = requestOptions(req);
  if (isStopped($json.host_state, now()) || (req.robots !== true && !mayRead(host, $json.host_state, now()))) {
    const stopped = isStopped($json.host_state, now());
    Object.assign($json, { answer: null, verdict: { outcome: 'skipped', reason: stopped ? 'host stopped' : 'robots.txt not checked today', host_stopped: stopped },
      stopped_now: false, alert: null });
    return $input.item;
  }
  return (async () => {
    const wait = waitMs(host, $json.last_end_ms, Date.now());
    if (wait > 0) await new Promise((r) => setTimeout(r, wait));
    let res;
    try {
      res = await this.helpers.httpRequest(options);
    } catch (e) {
      res = { error: e && e.message ? e.message : 'request failed' };
    }
    const end = Date.now();
    const kept = keptAnswer(res);
    const v = req.robots === true ? null : verdict(kept, req.url, req.expects || 'json');
    const after = v ? afterVerdict($json.host_state, v, now()) : { state: current($json.host_state, now()), stopped_now: false };
    Object.assign($json, { answer: kept, verdict: v, host_state: after.state, stopped_now: after.stopped_now, alert: withAlert(host, after),
      last_end_ms: end });
    return $input.item;
  })();
}
if ($json.stage === 'answer') {
  const host = allowedHost($json.url);
  const kept = keptAnswer($json.answer);
  const v = verdict(kept, $json.url, $json.expects || 'json');
  const after = afterVerdict($json.host_state, v, now());
  Object.assign($json, { answer: kept, verdict: v, host_state: after.state, stopped_now: after.stopped_now, alert: withAlert(host, after) });
  return $input.item;
}
if ($json.stage === 'robots') {
  const host = allowedHost(`https://${$json.host}/robots.txt`);
  const r = afterRobots(host, $json.host_state, $json.answer, now());
  Object.assign($json, { host_state: r.state, robots_read: r.read, stopped_now: r.stopped_now, robots_kind: r.kind, alert: withAlert(host, r) });
  return $input.item;
}
throw new Error(`source-guard.js: unknown stage ${JSON.stringify($json.stage)}`);

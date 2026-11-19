#!/usr/bin/env node
/**
 * The n8n exports in workflows/ against the rule of code-nodes/README.md (CLAUDE.md): a Code
 * node whose text is a file of code-nodes/ (it opens with that file's header line, "name.js —")
 * must be byte-identical to the file. An export never carries staticData: a workflow's static
 * data holds the state of its runs (URLs seen, hosts stopped), and source data stays out of
 * the repository (DEC-109).
 *
 * The Atti Web workflows (staging_D_attiweb_*) run one execution at a time (DEC-033, rule 2;
 * CONTRATTI.md, «Lo storico»): no webhook, each sub-workflow callable only by its one caller,
 * no n8n timeout, and the reading starts no tipologia past its 20 hours.
 *
 * The weekly backup chooses its records by name in the workflow, not with Drive's search, and
 * never marks an empty copy complete (CONTRATTI.md, «Copia di riserva»).
 *
 * Run:  node tests/test_workflow_exports.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DIR = path.join(ROOT, 'workflows');
const CODE = path.join(ROOT, 'code-nodes');

let failures = 0;
let checks = 0;

function check(label, ok, detail) {
  checks += 1;
  if (ok) {
    console.log(`  ok   ${label}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${label}${detail ? `\n       ${detail}` : ''}`);
  }
}

const files = fs.readdirSync(DIR).filter((f) => f.endsWith('.json')).sort();
for (const f of files) {
  const wf = JSON.parse(fs.readFileSync(path.join(DIR, f), 'utf8'));
  check(`${f}: no staticData in the export`, !Object.prototype.hasOwnProperty.call(wf, 'staticData'));
  for (const n of wf.nodes || []) {
    if (n.type !== 'n8n-nodes-base.code') continue;
    const js = (n.parameters || {}).jsCode || '';
    const m = /^\/\*\*\s*\n \* ([a-z0-9-]+\.js) —/.exec(js);
    if (!m) continue;
    const file = path.join(CODE, m[1]);
    const exists = fs.existsSync(file);
    check(`${f}: node "${n.name}" is code-nodes/${m[1]}, byte for byte`, exists && fs.readFileSync(file, 'utf8') === js,
      exists ? 'the node text differs from the file' : 'the file does not exist');
  }
}

// The Apify run of staging_C_fb_events_fetch (code-nodes/apify-run.js; workflows/README.md): only a
// SUCCEEDED run reaches the dataset, the wait ends, and every run writes its cost.
{
  const F = JSON.parse(fs.readFileSync(path.join(DIR, 'staging_C_fb_events_fetch.json'), 'utf8'));
  const to = (name, out) => (((F.connections[name] || {}).main || [])[out || 0] || []).map((x) => x.node).join();
  const node = (name) => F.nodes.find((n) => n.name === name);
  const apify = fs.readFileSync(path.join(CODE, 'apify-run.js'), 'utf8');
  check('C fetch: the request, the check of the run, the cost and the saved dataset run apify-run.js',
    ['Build Apify input', 'Controlla corsa', 'Costo', 'Eventi di prova'].every((nm) => node(nm) && node(nm).parameters.jsCode === apify));
  // T-C-costo: a Drive node without a credential fails at its first write (workflows/README.md).
  const drive = F.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive');
  check('T-C-costo: every Drive node of C fetch, «Carica costo» too, carries the Google Drive credential',
    drive.length === 3 && drive.some((n) => n.name === 'Carica costo') &&
    drive.every((n) => ((n.credentials || {}).googleDriveOAuth2Api || {}).id === '7nJkjb7aldPHyXv4'));
  check('C fetch: the run state goes to the check, never straight to the dataset', to('Get run') === 'Prepara controllo' && to('Prepara controllo') === 'Controlla corsa');
  check('C fetch: only a run to read reaches the dataset',
    Object.entries(F.connections).filter(([, v]) => (v.main || []).some((br) => (br || []).some((x) => x.node === 'Get dataset items'))).map(([k]) => k).join() === 'Da leggere?');
  // The owner's choice of 14 November 2026 (PR #51): the cost of a run that succeeded comes after
  // its dataset, with the count of its events, and does not wait for the upload of the original.
  // A Merge in append mode runs with one input when the other stays empty (tried on n8n Cloud on
  // 14 November 2026), so an empty dataset, which gives no item, still reaches the cost.
  const merge = node('Dopo il dataset') || { parameters: {} };
  const into = (name, out) => (((F.connections[name] || {}).main || [])[out || 0] || []).map((x) => `${x.node}#${x.index}`).join();
  check('C fetch: the cost waits for the dataset, and an empty dataset still reaches it',
    merge.type === 'n8n-nodes-base.merge' && (merge.parameters.mode || 'append') === 'append' &&
    into('Da leggere?', 0) === 'Get dataset items#0,Dopo il dataset#0' && into('Get dataset items') === 'To JSON file#0,Dopo il dataset#1' &&
    to('Dopo il dataset') === 'Prepara costo' && !F.connections['Upload to C Eventi originali']);
  check('C fetch: the cost of a run that succeeded is written once, whatever its events',
    node('Prepara costo').executeOnce === true);
  const eventsExpr = (node('Prepara costo').parameters.assignments.assignments.find((a) => a.name === 'events') || {}).value || '';
  const events = (items) => {
    try { return new Function('$', `return (${eventsExpr.replace(/^=\{\{/, '').replace(/\}\}$/, '')});`)(() => ({ all: () => items })); } catch (e) { return e.message; }
  };
  check('C fetch: an empty dataset counts 0 events', events([]) === 0);
  check('C fetch: a dataset counts its events', events([{ json: { id: 'e1' } }, { json: { id: 'e2' } }]) === 2);
  check('C fetch: a run that just ended is read again after a pause, for its settled cost',
    to('Da leggere?', 1) === 'Da assestare?' && to('Da assestare?', 0) === 'Attesa costo' && to('Attesa costo') === 'Get run' && node('Attesa costo').parameters.amount >= 15);
  check('C fetch: a run to wait waits; any other writes its cost and then stops with an error',
    to('Da assestare?', 1) === 'Da aspettare?' && to('Da aspettare?', 0) === 'Wait' && to('Da aspettare?', 1) === 'Prepara costo errore' &&
    to('Prepara costo errore') === 'Costo' && to('Carica costo') === 'Era un errore?' && to('Era un errore?', 0) === 'Ferma' &&
    node('Ferma').type === 'n8n-nodes-base.stopAndError');
  check('C fetch: the error says why the run stopped', /\$\('Controlla corsa'\)\.last\(\)\.json\.reason/.test(node('Ferma').parameters.errorMessage));
  check('C fetch: a failed run records its events as unknown, never zero',
    !node('Prepara costo errore').parameters.assignments.assignments.some((a) => a.name === 'events'));
  check('C fetch: the cost file', to('Prepara costo') === 'Costo' && to('Costo') === 'Carica costo');
  // apify-run.js, APIFY_TIMEOUT_S: Apify stops the run at its own timeout, so the wait reads its last state.
  const start = (node('Start Apify run') || {}).parameters || {};
  let timeout = null;
  try { timeout = new URL(String(start.url).replace(/^=/, '')).searchParams.getAll('timeout').join(); } catch (e) { timeout = e.message; }
  check('C fetch: the run starts with its own timeout, APIFY_TIMEOUT_S of apify-run.js',
    timeout === String(require(path.join(CODE, 'apify-run.js')).APIFY_TIMEOUT_S) && !start.sendQuery,
    `timeout in the URL: ${timeout || 'none'}; query parameters set apart from the URL: ${Boolean(start.sendQuery)}`);
  // «Prova senza Apify» (workflows/README.md): a request for a saved dataset takes its own branch
  // before any paid call, and its events reach the original exactly where a run's would.
  const reach = (from, out) => {
    const seen = new Set();
    const queue = (((F.connections[from] || {}).main || [])[out] || []).map((x) => x.node);
    while (queue.length) {
      const n = queue.shift();
      if (seen.has(n)) continue;
      seen.add(n);
      for (const br of ((F.connections[n] || {}).main || [])) for (const x of br || []) queue.push(x.node);
    }
    return seen;
  };
  check('C fetch: every request meets the choice between a run and a saved dataset before any paid call',
    to('Build Apify input') === 'Prova?' && to('Prova?', 1) === 'Start Apify run' && to('Prova?', 0) === 'Scarica prova');
  const from = (target) => Object.entries(F.connections).flatMap(([src, c]) =>
    ((c || {}).main || []).flatMap((br, i) => (br || []).filter((x) => x.node === target).map(() => `${src}#${i}`)));
  check('C fetch: «Start Apify run» has one way in, the run side of «Prova?»',
    from('Start Apify run').join() === 'Prova?#1', from('Start Apify run').join());
  const mod = require(path.join(CODE, 'apify-run.js'));
  const cond = (((node('Prova?') || {}).parameters || {}).conditions || {}).conditions || [];
  check('C fetch: «Prova?» asks whether buildRequest gave a fixture',
    cond.length === 1 && cond[0].leftValue === '={{ $json.fixture !== undefined }}' && cond[0].operator.operation === 'true' &&
    mod.buildRequest({ fixture: { file_id: '1AbCdEfGhIjKlMnOpQrStUvWxYz_inventato' } }).fixture !== undefined &&
    mod.buildRequest({ startUrls: ['https://www.facebook.com/pagina-inventata/events'] }).fixture === undefined,
    JSON.stringify(cond.map((c) => [c.leftValue, c.operator && c.operator.operation])));
  const prep = Object.fromEntries((((node('Prepara prova') || {}).parameters || {}).assignments || { assignments: [] })
    .assignments.map((a) => [a.name, a.value]));
  check('C fetch: the saved dataset is downloaded by the id buildRequest checked, and read in stage fixture',
    ((node('Scarica prova') || {}).parameters || {}).fileId?.value === '={{ $json.fixture.file_id }}' &&
    prep.stage === 'fixture' && prep.fixture === "={{ $('Build Apify input').first().json.fixture }}", JSON.stringify(prep));
  const fixturePath = reach('Prova?', 0);
  check('C fetch: a saved dataset reaches the original and never Apify or the cost register',
    fixturePath.has('Upload to C Eventi originali') &&
    ['Start Apify run', 'Wait', 'Get run', 'Get dataset items', 'Dopo il dataset', 'Prepara costo', 'Costo', 'Carica costo']
      .every((nm) => !fixturePath.has(nm)), [...fixturePath].join(', '));
  check('C fetch: the saved events reach the original one per item, like a dataset',
    to('Eventi di prova') === 'Un evento per riga' && node('Un evento per riga').parameters.fieldToSplitOut === 'events' &&
    to('Un evento per riga') === 'To JSON file');
  check('C fetch: the original written from a saved dataset says so in its name',
    /\$\('Build Apify input'\)\.first\(\)\.json\.fixture \? '_prova' : ''/.test(node('To JSON file').parameters.options.fileName));
}

// DEC-033, rule 2: one stream of requests to Atti Web. The reading starts only from its daily
// schedule, and each sub-workflow answers only the workflow that calls it.
const load = (name) => JSON.parse(fs.readFileSync(path.join(DIR, `${name}.json`), 'utf8'));
const D = { list: load('staging_D_attiweb_list'), tipologia: load('staging_D_attiweb_tipologia'),
  pass: load('staging_D_attiweb_pass'), download: load('staging_D_attiweb_download') };
for (const [k, wf] of Object.entries(D)) {
  check(`${wf.name}: no webhook`, !wf.nodes.some((n) => n.type === 'n8n-nodes-base.webhook'));
}
check('the reading starts only from its schedule',
  D.list.nodes.filter((n) => /Trigger$/.test(n.type)).map((n) => n.type).join() === 'n8n-nodes-base.scheduleTrigger');
// Pins the start of the night chosen in workflows/README.md, «Atti Web»: one run at a time
// (CONTRATTI.md, «Una corsa alla volta») also through the change of time, and away from 05:00 UTC.
const dSchedule = D.list.nodes.find((n) => n.type === 'n8n-nodes-base.scheduleTrigger');
check('D schedule: the reading starts at 1:13, Rome time', D.list.settings.timezone === 'Europe/Rome' &&
  JSON.stringify(dSchedule.parameters.rule) === JSON.stringify({ interval: [{ field: 'cronExpression', expression: '13 1 * * *' }] }));
// CONTRATTI.md, «Una corsa alla volta»: two scheduled runs never overlap because the reading starts
// no tipologia past 20 hours. n8n's own timeout is not used: n8n Cloud cuts any value to 5 minutes
// (test of 12 November 2026), and sub-workflows stop with it.
const D_ALL = [D.list, D.tipologia, D.pass, D.download];
check('no D workflow sets an n8n execution timeout', D_ALL.every((wf) => !('executionTimeout' in (wf.settings || {}))));
const byName = (wf, name) => wf.nodes.find((n) => n.name === name);
const next = (wf, name, out) => (((wf.connections[name] || {}).main || [])[out || 0] || []).map((x) => x.node);
check('each tipologia goes first to the 20-hour check', next(D.list, 'Tipologie', 1).join() === 'Prepara tempo');
const prep = byName(D.list, 'Prepara tempo');
check('the check is the budget stage of archive-record.js', !!prep && prep.parameters.includeOtherFields === true &&
  prep.parameters.assignments.assignments.some((a) => a.name === 'stage' && a.value === 'budget') &&
  next(D.list, 'Prepara tempo').join() === 'Tempo' && byName(D.list, 'Tempo').parameters.jsCode === fs.readFileSync(path.join(CODE, 'archive-record.js'), 'utf8'));
const gate = byName(D.list, 'Entro le 20 ore?');
check('in time the tipologia is read; past 20 hours it goes back to the loop closed unread',
  next(D.list, 'Tempo').join() === 'Entro le 20 ore?' && gate.parameters.conditions.conditions.length === 1 &&
  gate.parameters.conditions.conditions[0].leftValue === '={{ $json.in_time }}' &&
  next(D.list, 'Entro le 20 ore?', 0).join() === 'Pausa' && next(D.list, 'Entro le 20 ore?', 1).join() === 'Tipologie');
const leadsTo = (wf, target) => Object.entries(wf.connections)
  .filter(([, v]) => (v.main || []).some((br) => (br || []).some((x) => x.node === target))).map(([k]) => k).join();
check('only the check leads to the pause before a tipologia', leadsTo(D.list, 'Pausa') === 'Entro le 20 ore?');
// The same check before the second and third pass and before the download: after the last check
// at most one pass or the download is left (CONTRATTI.md, «Una corsa alla volta»).
const archiveCode = fs.readFileSync(path.join(CODE, 'archive-record.js'), 'utf8');
const gateOk = (wf, suffix, pause, closed) => {
  const p = byName(wf, `Prepara tempo ${suffix}`);
  const g = byName(wf, `Entro le 20 ore? ${suffix}`);
  return !!p && !!g && p.parameters.assignments.assignments.some((a) => a.name === 'stage' && a.value === 'budget') &&
    p.parameters.assignments.assignments.some((a) => a.name === 'started_at') &&
    next(wf, `Prepara tempo ${suffix}`).join() === `Tempo ${suffix}` && byName(wf, `Tempo ${suffix}`).parameters.jsCode === archiveCode &&
    next(wf, `Tempo ${suffix}`).join() === `Entro le 20 ore? ${suffix}` && g.parameters.conditions.conditions[0].leftValue === '={{ $json.in_time }}' &&
    next(wf, `Entro le 20 ore? ${suffix}`, 0).join() === pause && next(wf, `Entro le 20 ore? ${suffix}`, 1).join() === closed &&
    leadsTo(wf, pause) === `Entro le 20 ore? ${suffix}`;
};
check('before the second pass the tipologia checks the 20 hours, and past them closes what it read', gateOk(D.tipologia, '2', 'Pausa 2', 'Esito tipologia'));
check('before the third pass, the same', gateOk(D.tipologia, '3', 'Pausa 3', 'Esito tipologia'));
check('before the download the reading checks the 20 hours, and past them does not download', gateOk(D.list, 'download', 'Pausa download', ''));
check('the passes after a check take only their own fields', ['Passata 2', 'Passata 3'].every((nm) => byName(D.tipologia, nm).parameters.includeOtherFields === false));
for (const k of ['tipologia', 'pass', 'download']) {
  const trig = D[k].nodes.filter((n) => n.type === 'n8n-nodes-base.executeWorkflowTrigger');
  check(`${D[k].name} starts from its sub-workflow trigger`, trig.length === 1 && ((D[k].connections[trig[0].name] || {}).main || [[]])[0].length === 1);
}
for (const [k, caller] of [['tipologia', 'list'], ['pass', 'tipologia'], ['download', 'list']]) {
  check(`${D[k].name} answers only ${D[caller].name}`,
    D[k].settings.callerPolicy === 'workflowsFromAList' && String(D[k].settings.callerIds) === D[caller].id);
}
const calls = (wf) => wf.nodes.filter((n) => n.type === 'n8n-nodes-base.executeWorkflow').map((n) => n.parameters.workflowId.value);
check('the reading calls the tipologia and the download it names', calls(D.list).sort().join() === [D.tipologia.id, D.download.id].sort().join());
check('the tipologia calls the pass it names', calls(D.tipologia).every((id) => id === D.pass.id) && calls(D.tipologia).length > 0);

// The download's run limit: absent means the default, an explicit 0 stays 0.
const inizio = D.download.nodes.find((n) => n.name === 'Inizio').parameters.assignments.assignments.find((a) => a.name === 'run_limit');
const runLimit = (json) => new Function('$json', `return (${inizio.value.replace(/^=\{\{/, '').replace(/\}\}$/, '')});`)(json);
check('the download keeps an explicit run_limit of 0', runLimit({ run_limit: 0 }) === 0);
check('the download takes the default run_limit when none is given', runLimit({}) === 50 && runLimit({ run_limit: null }) === 50);
check('the download keeps the run_limit the reading passes', runLimit({ run_limit: 300 }) === 300);

// The weekly backup (CONTRATTI.md, «Copia di riserva»): the records are every file of the
// archive whose name ends in __v<n>.json, chosen in the workflow rather than by Drive's search,
// which matches only the start of the words of a name; a run with no record never writes
// COMPLETA.json.
{
  const R = JSON.parse(fs.readFileSync(path.join(DIR, 'staging_D_riserva.json'), 'utf8'));
  const node = (name) => R.nodes.find((n) => n.name === name);
  const next = (name) => ((R.connections[name] || {}).main || []).map((o) => (o || []).map((t) => t.node));
  check('backup: the record listing does not filter by name in Drive', !/name contains/.test(node('Record').parameters.queryString));
  const keep = node('Solo record');
  const cond = keep && keep.parameters.conditions.conditions[0];
  const rx = cond && new RegExp(cond.rightValue);
  check('backup: the records are chosen by name in the workflow, right after the listing',
    !!keep && keep.type === 'n8n-nodes-base.filter' && next('Record')[0].join() === 'Solo record' && next('Solo record')[0].join() === 'Mancanti');
  check('backup: the name rule keeps the records and nothing else',
    !!rx && rx.test('roma__arc__comune.roma.it__CMC__5750__v1.json') && rx.test('x__v12.json') &&
    !rx.test('attiweb_lettura_20261111T031300Z.json') && !rx.test('x__v1.json.bak') && !rx.test('x__vx.json'));
  check('backup: COMPLETA.json is written only on the branch where records were found',
    next('Una volta')[0].join() === 'Ci sono record?' && next('Ci sono record?')[0].join() === 'Testo segno' &&
    next('Ci sono record?')[1].join() === 'Nessun record' && node('Nessun record').type === 'n8n-nodes-base.stopAndError');
  check('backup: a stop reaches the alert workflow', R.settings.errorWorkflow === 'mFrh9UN4BVbhZAHz');
}

// The owner's pace for Atti Web (CONTRATTI.md, «Il ritmo del pilota»): 15 seconds between two
// requests to the portal, 100 documents a day. The menu, the run's first request, follows none.
{
  const waits = { list: ['Pausa', 'Pausa download'], tipologia: ['Pausa 2', 'Pausa 3'], pass: ['Pausa storico'], download: ['Pausa'] };
  for (const [k, names] of Object.entries(waits)) {
    for (const name of names) {
      const n = D[k].nodes.find((x) => x.name === name);
      check(`${D[k].name}: "${name}" waits at least 15 seconds between two portal requests`, !!n && n.type === 'n8n-nodes-base.wait' && Number(n.parameters.amount) >= 15 && !n.parameters.unit);
    }
  }
  // The menu is the first request of a run: the schedule starts it, and only Inizio comes before.
  const into = (wf, name) => Object.entries(wf.connections).filter(([, v]) => (v.main || []).some((o) => (o || []).some((t) => t.node === name))).map(([k]) => k);
  check('the menu, the first request of a run, follows only the start of the run', into(D.list, 'Menu').join() === 'Inizio' && into(D.list, 'Inizio').join() === 'Ogni giorno');
  const cerca = D.pass.nodes.find((x) => x.name === 'Cerca');
  check('the pages of a search are at least 15 seconds apart', Number(cerca.parameters.options.pagination.pagination.requestInterval) >= 15000);
  const value = (wf, node, field) => wf.nodes.find((x) => x.name === node).parameters.assignments.assignments.find((a) => a.name === field).value;
  check('the reading downloads at most 100 documents a run', Number(value(D.list, 'Limite del giro', 'run_limit')) <= 100);
  check('the day is capped at 100 documents', Number(value(D.download, 'Inizio', 'cap')) <= 100);
}

// T-A2-14: staging_A_elenco, RomaTV (WORKSTREAM_A, section 4, «La presa» and «I limiti misurati»;
// CONTRATTI section 7 A, «Raccolta»). The Code nodes are the files (checked above); here, how the
// workflow wires them.
{
  const E = load('staging_A_elenco');
  const AV = load('staging_A_avviso');
  const node = (name) => E.nodes.find((n) => n.name === name);
  const out = (name, o) => (((E.connections[name] || {}).main || [])[o || 0] || []).map((x) => x.node);
  const into = (name) => Object.entries(E.connections)
    .filter(([, v]) => (v.main || []).some((br) => (br || []).some((x) => x.node === name))).map(([k]) => k);
  const file = (f) => fs.readFileSync(path.join(CODE, f), 'utf8');
  const codeOf = (f) => E.nodes.filter((n) => n.type === 'n8n-nodes-base.code' && n.parameters.jsCode === file(f)).map((n) => n.name).sort();
  const val = (nm, field) => (node(nm).parameters.assignments.assignments.find((a) => a.name === field) || {}).value;
  const expr = (v, scope) => new Function(...Object.keys(scope), `return (${String(v).replace(/^=\{\{/, '').replace(/\}\}$/, '')});`)(...Object.values(scope));
  const guard = require(path.join(CODE, 'source-guard.js'));
  const list = require(path.join(CODE, 'romatv-list.js'));
  const state = require(path.join(CODE, 'recording-state.js'));

  check('elenco: every Code node is one of the three files, run once for each item',
    E.nodes.filter((n) => n.type === 'n8n-nodes-base.code').every((n) => n.parameters.mode === 'runOnceForEachItem' &&
      ['recording-state.js', 'romatv-list.js', 'source-guard.js'].some((f) => n.parameters.jsCode === file(f))));
  check('elenco: the requests go only through source-guard.js, fetch (no HTTP Request node)',
    !E.nodes.some((n) => /httpRequest|webhook|executeWorkflow/.test(n.type)) &&
    codeOf('source-guard.js').join() === ['Controlla robots', 'Guardia pagina', 'Regole', 'Si legge?'].sort().join());

  // `fetch` gets one item per execution: back from each fetch node to the one item of «Stato host»,
  // only nodes that pass one item on as one item.
  const oneToOne = (start) => {
    const seen = new Set();
    const todo = [start];
    while (todo.length) {
      const nm = todo.pop();
      if (seen.has(nm) || nm === 'Stato host') continue;
      seen.add(nm);
      const n = node(nm);
      if (nm !== start && !['n8n-nodes-base.set', 'n8n-nodes-base.if', 'n8n-nodes-base.code'].includes(n.type)) return `${nm} (${n.type})`;
      if (n.type === 'n8n-nodes-base.set' && n.parameters.mode !== 'manual') return `${nm} (raw)`;
      todo.push(...into(nm));
    }
    return seen.has('Altro host?') ? true : 'no path from Stato host';
  };
  check('elenco: fetch gets one item per execution (robots.txt)', oneToOne('Controlla robots') === true, String(oneToOne('Controlla robots')));
  check('elenco: fetch gets one item per execution (pages)', oneToOne('Guardia pagina') === true, String(oneToOne('Guardia pagina')));
  check('elenco: the one item starts from «Stato host», run once', node('Stato host').executeOnce === true);

  // Every write of a lease or of a recording's row carries the condition its code node gave, with
  // «Must Match» from where.match; the conditions are as many as the code gives.
  const writes = E.nodes.filter((n) => n.type === 'n8n-nodes-base.dataTable' && ['update', 'upsert'].includes(n.parameters.operation));
  const fromWhere = (n, src, k) => n.parameters.matchType === `={{ ${src}.match }}` && n.parameters.filters.conditions.length === k &&
    n.parameters.filters.conditions.every((c, i) => c.keyName === `={{ ${src}.conditions[${i}].keyName }}` &&
      c.condition === `={{ ${src}.conditions[${i}].condition }}` && c.keyValue === `={{ ${src}.conditions[${i}].keyValue }}`);
  const claimWhere = state.claim(state.LEASE_SEED[0], 'x', 1, 'list', false).where.conditions.length;
  const releaseWhere = state.release(state.LEASE_SEED[0], 'x').where.conditions.length;
  const WANT = {
    'Scrivi presa': ["$('Prendi?').item.json.lease.where", claimWhere], 'Scrivi presa 2': ["$('Prendi? 2').item.json.lease.where", claimWhere],
    'Rinnova: scrivi': ["$('Rinnova: prende?').item.json.lease.where", claimWhere],
    'Scrivi lascia': ["$('Lascia').item.json.release.where", releaseWhere], 'Scrivi riga': ["$('Nome scheda').item.json.where", 1],
  };
  check('elenco: the writes are the lease, its renewal and release, the rows of recordings and of hosts',
    writes.map((n) => n.name).sort().join() === Object.keys(WANT).concat(['Riga host']).sort().join());
  for (const [nm, [src, k]] of Object.entries(WANT)) {
    check(`elenco: «${nm}» carries its where, Must Match from where.match`, fromWhere(node(nm), src, k));
  }
  check('elenco: the code nodes behind the writes are recording-state.js',
    ['Prendi?', 'Prendi? 2', 'Rinnova: prende?', 'Lascia', 'Scheda esistente', 'Scheda nuova'].every((nm) => node(nm).parameters.jsCode === file('recording-state.js')));
  const rh = node('Riga host').parameters;
  check('elenco: a host row is written on its ref alone', rh.matchType === 'allConditions' && rh.filters.conditions.length === 1 &&
    rh.filters.conditions[0].keyName === 'ref' && rh.filters.conditions[0].condition === 'eq');
  check('elenco: every write maps only the fields its Set gives (no other field reaches the table)',
    writes.every((n) => n.parameters.columns.mappingMode === 'autoMapInputData' && into(n.name).every((p) => node(p).parameters.mode === 'raw')));

  // A row is read by its ref, one per item, never with a list the node truncates at 50 rows.
  const reads = E.nodes.filter((n) => n.type === 'n8n-nodes-base.dataTable' && ['get', 'rowExists', 'rowNotExists'].includes(n.parameters.operation));
  check('elenco: every row is read by its ref', reads.length > 0 && reads.every((n) => n.parameters.filters.conditions.length === 1 &&
    n.parameters.filters.conditions[0].keyName === 'ref' && n.parameters.filters.conditions[0].condition === 'eq' &&
    n.parameters.matchType === 'allConditions' && !n.parameters.returnAll));

  // n8n v1 runs the upper branch of a node to its end before the lower one (WORKSTREAM_A, section 4,
  // «La presa»): the alert file before the host row, the record before its row, the renewal before
  // the request, the answer in originali/ before the next page.
  const y = (nm) => node(nm).position[1];
  const before = (parent, first, second) => out(parent).includes(first) && out(parent).includes(second) && y(first) < y(second);
  check('elenco: executionOrder v1', E.settings.executionOrder === 'v1');
  check('elenco: the alert file of a host comes before its row', before('Esito host', 'Avviso host?', 'Campi host') &&
    out('Campi host').join() === 'Riga host' && out('Salva avviso host').length === 0);
  check('elenco: a host stopped by a robots.txt or by a page has its alert and its row first',
    before('Regole', 'Esito host', 'Host fatto') && before('Guardia pagina', 'Esito host', 'Prepara lettura'));
  check('elenco: the lease is renewed before every request, and a lease lost stops the run',
    before('Prepara robots', 'Rinnova presa', 'Controlla robots') && before('Prepara pagina', 'Rinnova presa', 'Guardia pagina') &&
    out('Rinnova: si prende?', 1).join() === 'Presa persa' && out('Rinnova: tenuta?', 1).join() === 'Presa persa' &&
    node('Presa persa').type === 'n8n-nodes-base.stopAndError' && out('Rinnova: tenuta?', 0).length === 0);
  check('elenco: the record file comes before its row', before('Nome scheda', 'File scheda', 'Campi riga'));
  // A node that waits for two inputs runs after every other branch: with one, the lease was left and
  // the register written before the records (execution 1341, 16 November 2026).
  check('elenco: no node waits for two inputs', !E.nodes.some((n) => n.type === 'n8n-nodes-base.merge'));
  check('elenco: the records and their rows come before the lease is left and the register',
    before('Collega parti', 'Elenca schede', 'Lascia presa') && before('Parti', 'Rinnova presa', 'Collega parti'));
  check('elenco: new rows and rows already there go through the same writes, each kind capped',
    into('Scheda nuova').join() === 'Senza riga' && into('Scheda esistente').join() === 'Con riga' &&
    out('Scheda esistente').join() === 'Da scrivere esistente?' && out('Scheda nuova').join() === 'Da scrivere nuova?' &&
    out('Da scrivere esistente?', 0).join() === 'Al più esistenti' && out('Da scrivere nuova?', 0).join() === 'Al più nuove' &&
    into('Nome scheda').sort().join() === ['Al più esistenti', 'Al più nuove'].join());
  // The writes come after the last renewal, at «Parti»: the cap keeps them inside the lease, at the
  // about 3 seconds a Drive file took in execution 1341 (WORKSTREAM_A, section 4, «La presa»), with
  // no retry of a record's write.
  const cap = ['Al più esistenti', 'Al più nuove'].reduce((t, nm) => t + Number(node(nm).parameters.maxItems), 0);
  check('elenco: the capped writes of a run, at the measured pace, fit inside the lease', cap > 0 && cap * 4000 < state.LEASE_MS &&
    ['Al più esistenti', 'Al più nuove'].every((nm) => node(nm).type === 'n8n-nodes-base.limit'));
  check('elenco: a record is written without a retry of the whole node (a rerun finds it by name)',
    !node('Salva scheda').retryOnFail && !node('Aggiorna scheda').retryOnFail && out("Scheda c'è?", 1).join() === 'Salva scheda' && out("Scheda c'è?", 0).join() === 'Aggiorna scheda');
  const folders = expr(val('Inizio', 'folders'), {});
  const drives = E.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive' && n.parameters.folderId);
  check('elenco: every folder comes from «Inizio»', drives.length === 5 &&
    drives.every((n) => /^=\{\{ \$\('Inizio'\)\.first\(\)\.json\.folders\.(registrazioni|originali|letture) \}\}$/.test(n.parameters.folderId.value)) &&
    node('Elenca schede').parameters.queryString.includes("$('Inizio').first().json.folders.registrazioni") &&
    node('Salva scheda').parameters.folderId.value.endsWith('folders.registrazioni }}') && node('Salva originale').parameters.folderId.value.endsWith('folders.originali }}'));
  check('elenco: the register and the alerts go to letture/, the folder of staging_A_avviso',
    ['Salva registro', 'Salva avviso host', 'Salva avviso elenchi'].every((nm) => node(nm).parameters.folderId.value.endsWith('folders.letture }}')) &&
    AV.nodes.find((n) => n.type === 'n8n-nodes-base.googleDrive').parameters.folderId.value === folders.letture);

  // The stage each preparing node gives its code node, and the conditions that route the item.
  const STAGES = { 'Prepara presa': 'claim', 'Prepara presa 2': 'claim', 'Prepara attesa': 'claim', 'Rinnova: prepara': 'claim',
    'Prepara mia': 'holds', 'Prepara mia 2': 'holds', 'Rinnova: prepara mia': 'holds', 'Prepara lascia': 'release',
    'Con riga': 'listing', 'Senza riga': 'listing', 'Registro': 'log', 'Fonte saltata': 'log',
    'Prepara may': 'may', 'Prepara robots': 'fetch', 'Prepara regole': 'robots', 'Prepara pagina': 'fetch',
    'Prepara richiesta': 'request', 'Prepara lettura': 'page', 'Parti': 'links' };
  for (const [nm, st] of Object.entries(STAGES)) check(`elenco: «${nm}» gives the stage ${st}`, val(nm, 'stage') === st);
  check('elenco: the list claims as a list', ['Prepara presa', 'Prepara presa 2', 'Prepara attesa', 'Rinnova: prepara'].every((nm) => val(nm, 'who') === 'list'));
  const ifs = E.nodes.filter((n) => n.type === 'n8n-nodes-base.if');
  check('elenco: every IF has one condition, true when its expression is true', ifs.every((n) => {
    const c = n.parameters.conditions;
    return c.conditions.length === 1 && c.conditions[0].rightValue === true && c.conditions[0].operator.type === 'boolean' &&
      c.conditions[0].operator.operation === 'true' && c.conditions[0].operator.singleValue === true;
  }));
  const cond = (nm, json, extra) => expr(node(nm).parameters.conditions.conditions[0].leftValue, Object.assign({ $json: json }, extra || {}));
  check('elenco: a lease to take is written; one to wait for waits',
    cond('Si prende?', { lease: { action: 'take' } }) === true && cond('Si prende?', { lease: { action: 'wait' } }) === false &&
    cond('Si aspetta?', { lease: { action: 'wait' } }) === true && cond('Si aspetta?', { lease: { action: 'skip' } }) === false);
  check('elenco: robots.txt is fetched only for a host not readable now, and judged only when asked',
    cond('Da controllare?', { may_read: false }) === true && cond('Da controllare?', { may_read: true }) === false &&
    cond('Saltato?', { verdict: { outcome: 'skipped' } }) === true && cond('Saltato?', { verdict: null }) === false);
  check('elenco: only a page judged data goes to originali/, and a reading not done asks the next page',
    cond('Originale?', { verdict: { outcome: 'ok' } }) === true && cond('Originale?', { verdict: { outcome: 'block' } }) === false &&
    cond('Altra pagina?', { reading: { done: false } }) === true && cond('Altra pagina?', { reading: { done: true } }) === false);
  check('elenco: the loops go on while a host or a catalogue is left, and stop when none is',
    cond('Altro host?', { hosts_left: ['h'] }) === true && cond('Altro host?', { hosts_left: [] }) === false &&
    cond('Altro catalogo?', { catalogs_left: ['c'] }) === true && cond('Altro catalogo?', { catalogs_left: [] }) === false);
  check('elenco: only an upsert is written, of either kind',
    ['Da scrivere esistente?', 'Da scrivere nuova?'].every((nm) => cond(nm, { action: 'upsert' }) === true && cond(nm, { action: 'none' }) === false));
  check('elenco: the work goes on only with the lease read back as this run\'s',
    ['Presa mia?', 'Presa mia? 2', 'Rinnova: tenuta?'].every((nm) => cond(nm, { lease_ours: true }) === true && cond(nm, { lease_ours: false }) === false) &&
    ['Si prende? 2', 'Rinnova: si prende?'].every((nm) => cond(nm, { lease: { action: 'take' } }) === true && cond(nm, { lease: { action: 'skip' } }) === false));
  check('elenco: an alert is written only when there is one',
    ['Avviso host?', 'Avviso elenchi?'].every((nm) => cond(nm, { alert: { name: 'x' } }) === true && cond(nm, { alert: null }) === false));
  // A record already in registrazioni/ is found by its name and updated, never uploaded again.
  const files = [{ json: { id: 'f1', name: 'romatv__a.json' } }, { json: { id: 'f2', name: 'romatv__b.json' } }];
  const lookup = (name, listed) => expr(val('Nome scheda', 'file_id'), { $json: { record_file_name: name }, $: () => ({ all: () => listed }) });
  check('elenco: a record is found by its name', [lookup('romatv__b.json', files), lookup('romatv__c.json', files), lookup('romatv__a.json', [{ json: {} }])],
    ['f2', '', '']);
  check('elenco: a record found goes to the update', cond("Scheda c'è?", {}, { $: () => ({ item: { json: { file_id: 'f2' } } }) }) === true &&
    cond("Scheda c'è?", {}, { $: () => ({ item: { json: { file_id: '' } } }) }) === false);
  // The register: the rows written, new and changed, and those left to the next run by the cap.
  const it = (ref) => ({ json: { rec: { recording_ref: ref } } });
  // An IF's all(0) is its true output, all(1) its false one; a node that did not run is not executed.
  const registro = (fakes) => {
    const $ = (nm) => ({ isExecuted: nm in fakes || nm === 'Inizio' || nm === 'Collega parti',
      all: (branch) => { const f = fakes[nm] || []; return Array.isArray(f[0]) ? (f[branch || 0] || []) : f; },
      first: () => ({ json: nm === 'Inizio' ? {} : { robots_log: [], host_states: {}, readings: [], unbound: [], records: [], hosts_stopped: [] } }) });
    return expr(val('Registro', 'run'), { $ });
  };
  const run = registro({ 'Da scrivere nuova?': [[it('n1'), it('n2'), it('n3')], [it('x1')]], 'Al più nuove': [it('n1'), it('n2')],
    'Da scrivere esistente?': [[it('e1')], [it('x2'), it('x3')]], 'Al più esistenti': [it('e1')] });
  check('elenco: the register counts the rows written and those left to the next run, never the unchanged ones',
    [run.new_rows, run.updated_rows, run.deferred], [['n1', 'n2'], ['e1'], ['n3']]);
  const none = registro({ 'Da scrivere esistente?': [[], [it('x2')]], 'Scheda esistente': [it('x2')] });
  check('elenco: a run with nothing to write registers nothing written and nothing left',
    [none.new_rows, none.updated_rows, none.deferred], [[], [], []]);
  const fetchReq = expr(val('Prepara robots', 'request'), { $json: { host: 'streaming.comune.roma.it' } });
  check('elenco: the robots.txt request is that of its host, flagged for the robots stage',
    fetchReq.url === 'https://streaming.comune.roma.it/robots.txt' && fetchReq.robots === true);
  check('elenco: a page is kept in originali/ before the next one is asked', before('Pagina', 'Originale?', 'Altra pagina?'));

  // The lease (T-A2-11): the run works only with the lease it read back as its own; held by
  // another it waits once, then leaves the source and says so in the register.
  check('elenco: the work starts only from a lease read back as this run\'s',
    into('Host da leggere').sort().join() === ['Presa mia?', 'Presa mia? 2'].join() &&
    out('Presa mia?', 0).join() === 'Host da leggere' && out('Presa mia? 2', 0).join() === 'Host da leggere');
  check('elenco: a lease held by another waits, then a second claim with waiting',
    out('Si aspetta?', 0).join() === 'Attesa presa' && out('Attesa presa').join() === 'Presa 2' && val('Prepara presa 2', 'waiting') === true &&
    val('Prepara presa', 'waiting') === false && node('Attesa presa').parameters.unit === 'seconds');
  check('elenco: the wait lasts what the lease says, at least a second',
    expr(node('Attesa presa').parameters.amount, { $json: { lease: { wait_ms: 120500 } } }) === 121 &&
    expr(node('Attesa presa').parameters.amount, { $json: { lease: { wait_ms: 0 } } }) === 1);
  check('elenco: a source left goes to the register, with no request',
    into('Fonte saltata').sort().join() === ['Presa mia? 2', 'Si aspetta?', 'Si prende? 2'].join() && out('Fonte saltata').join() === 'Registro corsa');
  check('elenco: the lease is left before the register', out('Scrivi lascia').join() === 'Registro' && out('Registro').join() === 'Registro corsa');

  // The values of «Inizio» are those of the files.
  const hostsOf = expr(val('Inizio', 'hosts'), {});
  check('elenco: the user agent of «Inizio» is source-guard.js\'s', val('Inizio', 'user_agent') === guard.USER_AGENT);
  check('elenco: the hosts checked are the RomaTV sites of source-guard.js', hostsOf.join() ===
    Object.entries(guard.HOSTS).filter(([, h]) => h.source === 'romatv' && h.robots !== null).map(([k]) => k).join());
  check('elenco: the API host is that of romatv-list.js', val('Inizio', 'api_host') === guard.hostOf(list.API));
  check('elenco: the catalogues are those of romatv-list.js', expr(val('Inizio', 'catalogs'), {}).join() === list.CATALOGS.map((c) => c.catalogo).join());
  check('elenco: the portal headers are off (DEC-036, point 2)', val('Inizio', 'portal_headers') === false);

  // The schedule and the settings (CONTRATTI section 7 A, «Raccolta»; WORKSTREAM_A, section 4).
  const trig = E.nodes.filter((n) => /Trigger$/.test(n.type));
  check('elenco: one schedule, every 2 hours from 7 to 21 in Rome', trig.length === 1 && trig[0].type === 'n8n-nodes-base.scheduleTrigger' &&
    trig[0].parameters.rule.interval[0].expression === '0 7-21/2 * * *' && E.settings.timezone === 'Europe/Rome');
  check('elenco: the export carries no test deadline', val('Inizio', 'prova_fino') === '');
  const inTime = node('In tempo?').parameters.conditions.conditions[0].leftValue;
  const now = { toMillis: () => Date.parse('2026-11-16T12:00:00Z') };
  check('elenco: a test run past its deadline does nothing; a run with none goes on',
    expr(inTime, { $json: { prova_fino: '' }, $now: now }) === true && expr(inTime, { $json: { prova_fino: '2026-11-16T11:59:00.000Z' }, $now: now }) === false &&
    expr(inTime, { $json: { prova_fino: '2026-11-16T12:01:00.000Z' }, $now: now }) === true && out('In tempo?', 1).length === 0);
  check('elenco: an error reaches staging_A_avviso', E.settings.errorWorkflow === AV.id && AV.name === 'staging_A_avviso');
  check('elenco: no n8n timeout (the list touches no audio)', !('executionTimeout' in E.settings));

  // staging_A_avviso: the model of staging_D_avviso, writing to A's letture/.
  const avTrig = AV.nodes.filter((n) => /Trigger$/.test(n.type));
  const drive = AV.nodes.filter((n) => n.type === 'n8n-nodes-base.googleDrive');
  check('avviso: started only by an error', avTrig.length === 1 && avTrig[0].type === 'n8n-nodes-base.errorTrigger');
  check('avviso: one file, in A\'s letture/', drive.length === 1);
  check('avviso: its own successful runs are not kept', AV.settings.saveDataSuccessExecution === 'none');
}

// The canonical write of channel C (code-nodes/canonical-write.js; workflows/README.md, «The
// canonical write»): the write and the update are one flow under two webhooks, a call reserves
// before any canonical write, and every call that reserved writes its outcome and answers with it.
{
  const CW = load('staging_C_write_canonical');
  const CU = load('staging_C_update_canonical');
  const strip = (wf) => wf.nodes.map((n) => {
    const c = JSON.parse(JSON.stringify(n));
    delete c.id; delete c.position; delete c.webhookId;
    if (c.type === 'n8n-nodes-base.webhook') { delete c.parameters.path; delete c.parameters.options; }
    return c;
  });
  check('C canonical: the write and the update have the same nodes and connections',
    JSON.stringify(strip(CW)) === JSON.stringify(strip(CU)) && JSON.stringify(CW.connections) === JSON.stringify(CU.connections));
  const cw = fs.readFileSync(path.join(CODE, 'canonical-write.js'), 'utf8');
  const node = (name) => CW.nodes.find((n) => n.name === name) || { parameters: {} };
  const out = (name, o) => (((CW.connections[name] || {}).main || [])[o || 0] || []).map((x) => `${x.node}#${x.index}`).join();
  const stageOf = (name) => ((node(name).parameters.assignments || {}).assignments || []).find((a) => a.name === 'stage');
  const STAGES = { Richiesta: ['Prepara richiesta', 'request'], Turno: ['Prepara turno', 'turn'], Piano: ['Prepara piano', 'plan'], Esito: ['Prepara esito', 'outcome'] };
  check('C canonical: the four steps run canonical-write.js, each on the one item of its stage',
    Object.entries(STAGES).every(([code, [prep, stage]]) => node(code).parameters.jsCode === cw && node(code).parameters.mode === 'runOnceForAllItems' &&
      out(prep) === `${code}#0` && (stageOf(prep) || {}).value === stage) &&
    ['Prepara fermo', 'Prepara guasto prima', 'Prepara guasto dopo'].every((n) => (stageOf(n) || {}).value === 'outcome' && out(n) === 'Esito#0'));
  check('C canonical: the reservation is written, and read again after a pause, before the turn',
    out('Richiesta') === 'Testo prenotazione#0' && out('Testo prenotazione') === 'File prenotazione#0' && out('File prenotazione') === 'Salva prenotazione#0' &&
    out('Salva prenotazione') === 'Attesa conferma#0' && Number(node('Attesa conferma').parameters.amount) >= 5 &&
    out('Attesa conferma') === 'Prima della lettura#0' && out('Prima della lettura') === 'Prenotazioni#0' && out('Prenotazioni') === 'Elenco prenotazioni#0' && out('Elenco prenotazioni') === 'Prepara turno#0' &&
    out('Prepara turno') === 'Turno#0' && out('Turno') === 'Tocca a noi?#0');
  const scritture = node('Salva prenotazione').parameters.folderId.value;
  check('C canonical: reservations and outcomes share their folder, and the reading again covers it with the times of writing',
    node('Salva esito').parameters.folderId.value === scritture && scritture !== node('Carica').parameters.folderId.value &&
    node('Prenotazioni').parameters.queryString.startsWith(`='${scritture}' in parents and trashed = false and `) &&
    /\$\('Richiesta'\)\.first\(\)\.json\.reservations_query/.test(node('Prenotazioni').parameters.queryString) &&
    ['id', 'name', 'createdTime'].every((f) => node('Prenotazioni').parameters.options.fields.includes(f)));
  check('C canonical: the turn is the reservation the call wrote', ((node('Prepara turno').parameters.assignments.assignments.find((a) => a.name === 'reservation_id') || {}).value) === "={{ $('Salva prenotazione').first().json.id }}");
  // A create sent twice is two files on Drive: the reservation and the canonical upload are never retried.
  check('C canonical: nothing that creates a reservation or a canonical file is retried', !node('Salva prenotazione').retryOnFail && !node('Carica').retryOnFail);
  check('C canonical: the readings and the outcome are retried 5 times 5 seconds apart, the interval of D',
    ['Prenotazioni', 'Elenco C Eventi', 'Salva esito'].every((n) => node(n).retryOnFail === true && node(n).maxTries >= 5 && node(n).waitBetweenTries >= 5000));
  check('C canonical: the listing of C Eventi has the times of writing and the MD5 of each file',
    ['id', 'name', 'createdTime', 'md5Checksum'].every((f) => node('Elenco C Eventi').parameters.options.fields.includes(f)) &&
    node('Elenco C Eventi').parameters.folderId === undefined && node('Elenco C Eventi').parameters.queryString === `'${node('Carica').parameters.folderId.value}' in parents and trashed = false`);
  // The plan refuses a listing without scritture/ (canonical-write.js), so an empty item never plans a creation.
  check('C canonical: the folders of C Eventi come with its listing', node('Elenco C Eventi').parameters.options.fields.includes('mimeType'));
  // n8n leaves out a setting at its default: from version 1.1 of the Wait node the unit is seconds.
  check('C canonical: the pause after the reservation is in seconds',
    node('Attesa conferma').typeVersion === 1.1 && [undefined, 'seconds'].includes(node('Attesa conferma').parameters.unit) && node('Attesa conferma').parameters.resume === undefined);
  // Reachability: with the turn's "go on" branch cut, no canonical write is reachable.
  const reach = (from, cut) => {
    const seen = new Set([from]);
    const todo = [from];
    while (todo.length) {
      const n = todo.pop();
      ((CW.connections[n] || {}).main || []).forEach((br, o) => (br || []).forEach((t) => {
        if (cut && n === cut[0] && o === cut[1]) return;
        if (!seen.has(t.node)) { seen.add(t.node); todo.push(t.node); }
      }));
    }
    return seen;
  };
  const cut = reach('Webhook', ['Tocca a noi?', 0]);
  check('C canonical: no canonical write without the turn', !cut.has('Carica') && !cut.has('Aggiorna') && !cut.has('Elenco C Eventi'));
  check('C canonical: a call that stops still writes its outcome and answers', out('Tocca a noi?', 1) === 'Prepara fermo#0' && cut.has('Salva esito') && cut.has('Rispondi'));
  check('C canonical: create, update or leave each file, by its plan',
    out('Piano') === 'Da scrivere?#0' && out('Da scrivere?', 0) === 'Nuovo?#0' && out('Da scrivere?', 1) === 'Risultati#2' &&
    node('Da scrivere?').parameters.conditions.conditions[0].leftValue === "={{ $json.action === 'create' || $json.action === 'update' }}" &&
    out('Nuovo?', 0) === 'Carica#0' && out('Nuovo?', 1) === 'Aggiorna#0' && node('Aggiorna').parameters.operation === 'update' &&
    node('Aggiorna').parameters.fileId.value === '={{ $json.file_id }}' && node('Carica').parameters.name === '={{ $binary.data.fileName }}');
  // Each input of the merge has one parent: a node fed by two parents runs twice, and so would the merge.
  check('C canonical: a write that fails is a result too, so the outcome is written (T29)',
    node('Carica').onError === 'continueErrorOutput' && node('Aggiorna').onError === 'continueErrorOutput' &&
    out('Carica', 0) === 'Creato#0' && out('Aggiorna', 0) === 'Aggiornato#0' && out('Carica', 1) === 'Non caricato#0' && out('Aggiorna', 1) === 'Non aggiornato#0' &&
    out('Creato') === 'Risultati#0' && out('Aggiornato') === 'Risultati#1' && out('Non caricato') === 'Risultati#3' && out('Non aggiornato') === 'Risultati#4' &&
    Number(node('Risultati').parameters.numberInputs) === 5);
  const parents = (target) => Object.entries(CW.connections).flatMap(([k, v]) => (v.main || []).flatMap((br) => (br || []).filter((t) => t.node === target).map((t) => `${k}>${t.index}`)));
  check('C canonical: every input of the merge has a parent of its own', [0, 1, 2, 3, 4].every((i) => parents('Risultati').filter((p) => p.endsWith(`>${i}`)).length === 1));
  const field = (name, f) => ((node(name).parameters.assignments.assignments.find((a) => a.name === f) || {}).value);
  check('C canonical: the result of a write takes the Drive id the write returns (phase 5.2, step 3)', field('Creato', 'file_id') === "={{ $json.id || '' }}" && field('Aggiornato', 'file_id') === "={{ $json.id || '' }}");
  check('C canonical: the results read their file one step back, the item the Drive node was given',
    ['Creato', 'Aggiornato', 'Non caricato', 'Non aggiornato'].every((n) => /^=\{\{ \$\('Nuovo\?'\)\.item\.json\.name \}\}$/.test(field(n, 'name')) && /\$\('Nuovo\?'\)\.item\.json\.duplicates/.test(field(n, 'duplicates'))));
  // A step that fails after the reservation still leaves its outcome (specification v2.5, Part I, 4.2).
  const errTo = (name) => reach(((((CW.connections[name] || {}).main || [])[1] || [])[0] || {}).node || '-');
  check('C canonical: every step of code and write between the reservation and the outcome has an error route to it',
    ['Turno', 'Piano', 'Carica', 'Aggiorna'].every((n) => node(n).onError === 'continueErrorOutput' && errTo(n).has('Salva esito') && errTo(n).has('Rispondi')));
  // With an error output, n8n's alwaysOutputData adds an empty item to the main output beside the error item,
  // and both branches would write an outcome: the reading again keeps its error item on its one output,
  // where the turn throws it to its own error route (T29).
  check('C canonical: the reading again has one output, its error item goes to the turn',
    node('Prenotazioni').onError === 'continueRegularOutput' && node('Prenotazioni').alwaysOutputData === true &&
    ((CW.connections.Prenotazioni || {}).main || []).length === 1 && out('Prenotazioni') === 'Elenco prenotazioni#0' &&
    CW.nodes.every((n) => !(n.alwaysOutputData && n.onError === 'continueErrorOutput')));
  // T-C-elenco-vuoto: the listing of C Eventi takes the same shape, so that a listing Drive returns
  // empty reaches the plan. What reaches «Piano», as read in n8n-core 2.48.3 (workflow-execute.js):
  // processNodeOutput moves an error item to the error output, if the node has one, then
  // ensureAlwaysOutputData puts one empty item on an empty main output; a node that throws gives
  // back its input on its main output (handleNodeExecutionError).
  const plan = require(path.join(CODE, 'canonical-write.js')).plan;
  const thrownBy = (fn) => { try { fn(); return false; } catch (e) { return true; } };
  const outputs = (n, items, threw) => {
    if (threw) return [items];
    const isError = (j) => j.error !== undefined && Object.keys(j).every((k) => ['error', 'message', 'details'].includes(k));
    const o = n.onError === 'continueErrorOutput' ? [items.filter((j) => !isError(j)), items.filter(isError)] : [items];
    if (o[0].length === 0 && n.alwaysOutputData === true) o[0] = [{}];
    return o;
  };
  const routes = (items, threw) => outputs(node('Elenco C Eventi'), items, threw).flatMap((its, o) => {
    if (its.length === 0) return [];
    if (out('Elenco C Eventi', o) !== 'Elenco file#0') return [out('Elenco C Eventi', o)];
    const file = { name: 'roma__evt__facebook__1.json', content: '{}' };
    return [thrownBy(() => plan({ files: [file], listing: its })) ? out('Piano', 1) : out('Piano', 0)];
  });
  const SCR = { id: 'SCR', name: 'scritture', mimeType: 'application/vnd.google-apps.folder', createdTime: '2026-11-15T15:57:00.578Z' };
  const seen = { files: routes([SCR]), empty: routes([]), error: routes([{ error: 'Drive 503' }]), threw: routes([{ stage: 'turn', turn: { holds: true } }], true) };
  check('C canonical (T-C-elenco-vuoto, T29): the listing of C Eventi has one output; files, nothing, an error or its input given back reach the outcome by one route',
    node('Elenco C Eventi').onError === 'continueRegularOutput' && node('Elenco C Eventi').alwaysOutputData === true &&
    ((CW.connections['Elenco C Eventi'] || {}).main || []).length === 1 && out('Elenco file') === 'Prepara piano#0' &&
    seen.files.join() === 'Da scrivere?#0' && ['empty', 'error', 'threw'].every((k) => seen[k].join() === 'Prepara guasto dopo#0'), JSON.stringify(seen));
  // A Drive node that fails outside its handling of each item gives back its input (n8n-core,
  // handleNodeExecutionError): that input is the marker alone, never the call's own reservation (T27).
  check('C canonical (T27): the reading again is given the marker alone, which the turn refuses',
    node('Prima della lettura').type === 'n8n-nodes-base.set' && node('Prima della lettura').typeVersion >= 3.3 &&
    node('Prima della lettura').parameters.mode === 'manual' && node('Prima della lettura').parameters.includeOtherFields === false &&
    JSON.stringify(node('Prima della lettura').parameters.assignments.assignments.map((a) => [a.name, a.value, a.type])) === JSON.stringify([['reading_input', true, 'boolean']]) &&
    /r\.reading_input === true/.test(cw));
  check('C canonical: an error before the turn stops the call, one after it fails the call before any canonical write',
    out('Turno', 1) === 'Prepara guasto prima#0' && !('turn' in Object.fromEntries((node('Prepara guasto prima').parameters.assignments.assignments).map((a) => [a.name, 1]))) &&
    out('Piano', 1) === 'Prepara guasto dopo#0' && !errTo('Piano').has('Carica') && !errTo('Piano').has('Aggiorna'));
  check('C canonical: the outcome is saved, then sent back with its status',
    out('Esito') === 'Testo esito#0' && out('Testo esito') === 'File esito#0' && out('File esito') === 'Salva esito#0' && out('Salva esito') === 'Rispondi#0' &&
    node('Webhook').parameters.responseMode === 'responseNode' && node('Rispondi').type === 'n8n-nodes-base.respondToWebhook' &&
    /\$\('Esito'\)\.first\(\)\.json\.status_code/.test(node('Rispondi').parameters.options.responseCode));
  check('C canonical: the only webhook answers only through «Rispondi»',
    CW.nodes.filter((n) => n.type === 'n8n-nodes-base.webhook').length === 1 && CW.nodes.filter((n) => n.type === 'n8n-nodes-base.respondToWebhook').length === 1);
}

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

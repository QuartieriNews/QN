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
  check('C fetch: the request, the check of the run and the cost run apify-run.js',
    ['Build Apify input', 'Controlla corsa', 'Costo'].every((nm) => node(nm) && node(nm).parameters.jsCode === apify));
  check('C fetch: the run state goes to the check, never straight to the dataset', to('Get run') === 'Prepara controllo' && to('Prepara controllo') === 'Controlla corsa');
  check('C fetch: only a run to read reaches the dataset, and its cost is written beside it, not after it',
    to('Da leggere?', 0) === 'Get dataset items,Prepara costo' && !F.connections['Upload to C Eventi originali'] &&
    !node('Prepara costo').parameters.assignments.assignments.some((a) => a.name === 'events') &&
    Object.entries(F.connections).filter(([, v]) => (v.main || []).some((br) => (br || []).some((x) => x.node === 'Get dataset items'))).map(([k]) => k).join() === 'Da leggere?');
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

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

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
 * the reading under a timeout shorter than a day.
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
const day = 24 * 3600;
check('the reading times out in less than a day, so two scheduled runs never overlap',
  Number.isInteger(D.list.settings.executionTimeout) && D.list.settings.executionTimeout > 0 && D.list.settings.executionTimeout < day);
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

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

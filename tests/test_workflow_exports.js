#!/usr/bin/env node
/**
 * The n8n exports in workflows/ against the rule of code-nodes/README.md (CLAUDE.md): a Code
 * node whose text is a file of code-nodes/ (it opens with that file's header line, "name.js —")
 * must be byte-identical to the file. An export never carries staticData: a workflow's static
 * data holds the state of its runs (URLs seen, hosts stopped), and source data stays out of
 * the repository (DEC-109).
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

console.log('');
if (failures === 0) {
  console.log(`ALL PASS (${checks} checks)`);
  process.exit(0);
} else {
  console.log(`${failures} of ${checks} checks FAILED`);
  process.exit(1);
}

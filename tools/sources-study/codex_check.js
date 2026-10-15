#!/usr/bin/env node
// Codex control of the sources study (feasibility note §9.6, controls C1-C5): sends a mandate and
// the files to review to the Responses API and prints the verdict plus the usage the ledger needs.
// Not the Strategic Council tool: that one is council/cli.js, pinned to the reasoning model by
// DEC-008 and refusing coding models on purpose. This one is the code/method reviewer.
'use strict';
const fs = require('fs');

const MODEL = 'gpt-5.3-codex';
const ENDPOINT = 'https://api.openai.com/v1/responses';

function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  return i === -1 || i === process.argv.length - 1 ? fallback : process.argv[i + 1];
}
function args(name) {
  const out = [];
  process.argv.forEach((a, i) => { if (a === '--' + name) out.push(process.argv[i + 1]); });
  return out;
}

const control = arg('control');
const mandateFile = arg('mandate');
const files = args('file');
const out = arg('out');
const effort = arg('effort', 'high');
// Tetti chiusi (AGENTS.md, costo): oltre la soglia il controllo non parte.
const MAX_INPUT_CHARS = Number(arg('max-input-chars', 1500000));
const MAX_OUTPUT_TOKENS = Number(arg('max-output-tokens', 30000));
const dryRun = process.argv.includes('--dry-run');

if (!control || !mandateFile || files.length === 0) {
  console.error('usage: codex_check.js --control C1 --mandate <file> --file <file> [--file ...] [--out <file>] [--dry-run]');
  process.exit(2);
}
// Fail-closed: a missing key must never look like a reviewer that had nothing to say.
if (!dryRun && !process.env.OPENAI_API_KEY) {
  console.error('OPENAI_API_KEY is not set: refusing to call, so a missing key cannot be read as an empty review');
  process.exit(2);
}

const parts = [fs.readFileSync(mandateFile, 'utf8')];
for (const f of files) {
  parts.push(`\n\n===== FILE: ${f} =====\n` + fs.readFileSync(f, 'utf8'));
}
const input = parts.join('\n');
if (input.length > MAX_INPUT_CHARS) {
  console.error(`${input.length} caratteri: oltre il tetto di ${MAX_INPUT_CHARS} per controllo (--max-input-chars). Dividi gli allegati.`);
  process.exit(2);
}

const body = {
  model: MODEL,
  input,
  reasoning: { effort },
  store: false,
  max_output_tokens: MAX_OUTPUT_TOKENS,
};

if (dryRun) {
  console.log(JSON.stringify({ ...body, input: `[${input.length} caratteri, ${files.length} file]` }, null, 1));
  process.exit(0);
}

(async () => {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 900000);
  let res;
  try {
    res = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }
  const raw = await res.text();
  if (!res.ok) {
    // The key itself is never echoed: only the status and the provider's message.
    console.error(`HTTP ${res.status}: ${raw.slice(0, 600)}`);
    process.exit(1);
  }
  const data = JSON.parse(raw);
  const text = (data.output || [])
    .flatMap((o) => (o.content || []).filter((c) => c.type === 'output_text').map((c) => c.text))
    .join('\n');
  if (!text.trim()) {
    console.error('risposta vuota: il controllo non è stato eseguito');
    process.exit(1);
  }
  const u = data.usage || {};
  const usage = `\n\n---\nControllo ${control}, modello ${MODEL}, effort ${effort}, ` +
    `token ${u.input_tokens} in / ${u.output_tokens} out, ${new Date().toISOString()}\n`;
  if (out) fs.writeFileSync(out, text + usage);
  console.log(text);
  console.log(usage);
})().catch((e) => { console.error(String(e && e.message ? e.message : e)); process.exit(1); });

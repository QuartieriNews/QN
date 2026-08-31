#!/usr/bin/env node
/**
 * cli.js — how Claude Code reaches the strategist (Issue #5).
 *
 * One stage per invocation, so the independence rule stays visible in the
 * command that was run: a FIRST_PASS call accepts no Claude view, and the
 * transcript of the session shows it.
 *
 * Usage and tiers are documented in `council/README.md`.
 *
 *   node council/cli.js --stage FIRST_PASS --question "..." [--context-file F]
 *   node council/cli.js --stage CROSS_REVIEW --question "..." \
 *        --claude-view-file F --gpt-first-pass-file F
 *   node council/cli.js --stage FINAL_POSITION --question "..." \
 *        --claude-view-file F --gpt-first-pass-file F [--exchange-file F]
 *
 *   --effort high|xhigh|max   (default high)
 *   --dry-run                 print the request; make no API call
 *   --json                    print the full result as JSON
 *   --save                    write the session record under council/sessions/
 */

'use strict';

const fs = require('fs');
const path = require('path');

const {
  STAGES,
  DEFAULT_MODEL,
  DEFAULT_EFFORT,
  ALLOWED_EFFORTS,
  buildRequest,
  callStrategist,
} = require('./strategist');

const SESSIONS_DIR = path.join(__dirname, 'sessions');

const FLAGS_WITH_VALUES = new Set([
  '--stage', '--question', '--question-file', '--context', '--context-file',
  '--claude-view', '--claude-view-file', '--gpt-first-pass', '--gpt-first-pass-file',
  '--exchange', '--exchange-file', '--effort',
]);

function parseArgv(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '-h') {
      args.help = true;
    } else if (!token.startsWith('--')) {
      throw new Error(`unexpected argument '${token}'`);
    } else if (FLAGS_WITH_VALUES.has(token)) {
      const value = argv[i + 1];
      if (value === undefined || value.startsWith('--')) {
        throw new Error(`${token} needs a value`);
      }
      args[token.slice(2)] = value;
      i += 1;
    } else if (['--dry-run', '--json', '--save', '--help'].includes(token)) {
      args[token.slice(2)] = true;
    } else {
      throw new Error(`unknown flag '${token}'`);
    }
  }
  return args;
}

function readIfFile(inline, filePath, label) {
  if (inline !== undefined && filePath !== undefined) {
    throw new Error(`pass either --${label} or --${label}-file, not both`);
  }
  if (inline !== undefined) return inline;
  if (filePath === undefined) return undefined;
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch (cause) {
    throw new Error(`cannot read --${label}-file ${filePath}: ${cause.message}`);
  }
}

const USAGE = `council — the GPT strategist of the Strategic Council

  node council/cli.js --stage FIRST_PASS --question "..." [--context-file F]
  node council/cli.js --stage CROSS_REVIEW --question "..." \\
       --claude-view-file F --gpt-first-pass-file F
  node council/cli.js --stage FINAL_POSITION --question "..." \\
       --claude-view-file F [--gpt-first-pass-file F] [--exchange-file F]

  --effort ${ALLOWED_EFFORTS.join('|')}   (default ${DEFAULT_EFFORT})
  --dry-run                 print the request; make no API call
  --json                    print the full result as JSON
  --save                    write the session record under council/sessions/

The model is ${DEFAULT_MODEL}, fixed by DEC-008 and not selectable here.

FIRST_PASS accepts no Claude view: the two first-pass views are formed
independently. See council/README.md and docs/strategic-council/README.md.`;

function saveSession(record) {
  fs.mkdirSync(SESSIONS_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const file = path.join(SESSIONS_DIR, `${stamp}-${record.stage}.json`);
  fs.writeFileSync(file, `${JSON.stringify(record, null, 2)}\n`);
  return file;
}

async function main(argv = process.argv.slice(2)) {
  const args = parseArgv(argv);

  if (args.help || argv.length === 0) {
    process.stdout.write(`${USAGE}\n`);
    return 0;
  }

  const stage = args.stage;
  if (!stage || !Object.prototype.hasOwnProperty.call(STAGES, stage)) {
    throw new Error(
      `--stage must be one of ${Object.keys(STAGES).join(', ')}`
    );
  }

  const options = {
    stage,
    question: readIfFile(args.question, args['question-file'], 'question'),
    context: readIfFile(args.context, args['context-file'], 'context') || '',
    claudeView: readIfFile(args['claude-view'], args['claude-view-file'], 'claude-view'),
    gptFirstPass: readIfFile(args['gpt-first-pass'], args['gpt-first-pass-file'], 'gpt-first-pass'),
    exchange: readIfFile(args.exchange, args['exchange-file'], 'exchange'),
    effort: args.effort || DEFAULT_EFFORT,
  };

  if (!ALLOWED_EFFORTS.includes(options.effort)) {
    throw new Error(
      `--effort must be one of ${ALLOWED_EFFORTS.join(', ')}`
    );
  }

  if (args['dry-run']) {
    // Builds and validates the request — including the independence rule —
    // without a key and without a request.
    const body = buildRequest(options);
    process.stdout.write(`${JSON.stringify(body, null, 2)}\n`);
    return 0;
  }

  const result = await callStrategist(options);

  if (args.save) {
    const file = saveSession({
      stage: result.stage,
      model: result.model,
      id: result.id,
      usage: result.usage,
      question: options.question,
      text: result.text,
      at: new Date().toISOString(),
    });
    process.stderr.write(`session saved: ${path.relative(process.cwd(), file)}\n`);
  }

  if (args.json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } else {
    process.stdout.write(`${result.text}\n`);
    const u = result.usage;
    process.stderr.write(
      `\n[usage] model=${result.model} input=${u.input_tokens} ` +
      `output=${u.output_tokens} reasoning=${u.reasoning_tokens} total=${u.total_tokens}\n`
    );
  }
  return 0;
}

if (require.main === module) {
  main().then(
    (code) => process.exit(code),
    (error) => {
      process.stderr.write(`council: ${error.message}\n`);
      process.exit(1);
    }
  );
}

module.exports = { main, parseArgv, SESSIONS_DIR };

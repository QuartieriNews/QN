/**
 * test_council.js — executable acceptance for the Strategic Council MVP.
 *
 * Covers the seven acceptance tests of Issue #5. Numbered labels below map to
 * that list. No live OpenAI call is made anywhere in this file: the network is
 * reached only through an injected fetch, and every test that could touch it
 * asserts that it did not.
 *
 * Run:  node tests/test_council.js   (exit 0 and "ALL PASS" required)
 */

'use strict';

const path = require('path');
const fs = require('fs');

const REPO_ROOT = path.join(__dirname, '..');
const COUNCIL = path.join(REPO_ROOT, 'council', 'strategist.js');
const {
  DEFAULT_MODEL,
  DEFAULT_EFFORT,
  ALLOWED_EFFORTS,
  RESPONSES_ENDPOINT,
  STAGES,
  CLASSIFICATIONS,
  readRolePrompt,
  buildRequest,
  parseResponse,
  readApiKey,
  callStrategist,
  classifyCouncil,
} = require(COUNCIL);

let failures = 0;
let checks = 0;

function check(label, actual, expected) {
  checks += 1;
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a === e) {
    console.log(`  ok   ${label}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${label}\n       expected ${e}\n       got      ${a}`);
  }
}

/** Returns the thrown message, or null when the call did not throw. */
function threw(fn) {
  try {
    fn();
    return null;
  } catch (error) {
    return error.message;
  }
}

async function threwAsync(fn) {
  try {
    await fn();
    return null;
  } catch (error) {
    return error.message;
  }
}

/** A fetch that records that it was reached; reaching it is itself the failure. */
function forbiddenFetch(state) {
  return async () => {
    state.called = true;
    throw new Error('network was reached');
  };
}

const ROLE_PROMPT = '# stub strategist role prompt';
const QUESTION = 'Generalise the geography engine for many cities now, or optimise for Rome?';
const CLAUDE_VIEW = '### OPERATOR_VIEW\nRecommendation: optimise for Rome first.';

async function main() {
  console.log('acceptance 1 — a missing key fails clearly, before any request');
  {
    const msg = threw(() => readApiKey({}));
    check('empty env -> throws', typeof msg === 'string', true);
    check('names the variable', /OPENAI_API_KEY/.test(msg || ''), true);
    check('points at the setup doc', /council\/README\.md/.test(msg || ''), true);
    check('a blank key counts as missing',
      typeof threw(() => readApiKey({ OPENAI_API_KEY: '   ' })) === 'string', true);
    check('a set key is returned trimmed', readApiKey({ OPENAI_API_KEY: ' sk-test ' }), 'sk-test');
  }
  {
    const state = { called: false };
    const msg = await threwAsync(() => callStrategist(
      { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT },
      { env: {}, fetchImpl: forbiddenFetch(state) }
    ));
    check('callStrategist without a key throws', /OPENAI_API_KEY/.test(msg || ''), true);
    check('…and never reached the network', state.called, false);
  }

  console.log('acceptance 2 — FIRST_PASS cannot carry the Claude view (independence rule)');
  {
    const msg = threw(() => buildRequest({
      stage: STAGES.FIRST_PASS, question: QUESTION,
      claudeView: CLAUDE_VIEW, rolePrompt: ROLE_PROMPT,
    }));
    check('passing a Claude view to FIRST_PASS throws', /independence rule/.test(msg || ''), true);

    const body = buildRequest({
      stage: STAGES.FIRST_PASS, question: QUESTION,
      context: 'DEC-104 fixes the loop roles.', rolePrompt: ROLE_PROMPT,
    });
    const serialised = JSON.stringify(body);
    check('the built request contains no Claude view text',
      serialised.includes('optimise for Rome first'), false);
    check('the built request contains no operator-view field',
      /OPERATOR_VIEW|claudeView|claude_view/i.test(serialised), false);
    check('the question does reach the strategist', body.input.includes(QUESTION), true);
    check('the context does reach the strategist',
      body.input.includes('DEC-104 fixes the loop roles.'), true);
    check('the stage is stated in the body', body.input.includes('Stage: FIRST_PASS'), true);
  }
  {
    // The later stages are the ones that may see it, and they require it.
    check('CROSS_REVIEW without the Claude view throws',
      /requires the Claude view/.test(threw(() => buildRequest({
        stage: STAGES.CROSS_REVIEW, question: QUESTION,
        gptFirstPass: 'mine', rolePrompt: ROLE_PROMPT,
      })) || ''), true);

    const body = buildRequest({
      stage: STAGES.CROSS_REVIEW, question: QUESTION, claudeView: CLAUDE_VIEW,
      gptFirstPass: '### STRATEGY_VIEW\nmine', rolePrompt: ROLE_PROMPT,
    });
    check('CROSS_REVIEW does carry the Claude view',
      body.input.includes('optimise for Rome first'), true);
    check('FINAL_POSITION also requires it',
      /requires the Claude view/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION, rolePrompt: ROLE_PROMPT,
      })) || ''), true);
  }

  console.log('acceptance 3 — the model defaults to the general reasoning model');
  {
    const body = buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT });
    check('default model', body.model, 'gpt-5.6-sol');
    check('exported default agrees', DEFAULT_MODEL, 'gpt-5.6-sol');
    check('an explicit model is honoured',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: 'gpt-5.6-sol-mini', rolePrompt: ROLE_PROMPT,
      }).model, 'gpt-5.6-sol-mini');
    check('a Codex model is refused as strategic critic',
      /never a coding model/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, model: 'codex-max', rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    check('…case-insensitively',
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, model: 'GPT-5-CODEX', rolePrompt: ROLE_PROMPT,
      })) === 'string', true);
    check('the endpoint is the Responses API',
      RESPONSES_ENDPOINT, 'https://api.openai.com/v1/responses');
  }

  console.log('acceptance 4 — reasoning effort defaults to high and is validated');
  {
    const body = buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT });
    check('default effort', body.reasoning.effort, 'high');
    check('exported default agrees', DEFAULT_EFFORT, 'high');
    check('allowed tiers', ALLOWED_EFFORTS, ['high', 'xhigh', 'max']);
    for (const effort of ALLOWED_EFFORTS) {
      check(`'${effort}' is accepted`,
        buildRequest({
          stage: STAGES.FIRST_PASS, question: QUESTION, effort, rolePrompt: ROLE_PROMPT,
        }).reasoning.effort, effort);
    }
    check("'low' is refused (the Council does not reason cheaply)",
      /not allowed/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, effort: 'low', rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    check("'' is refused",
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, effort: '', rolePrompt: ROLE_PROMPT,
      })) === 'string', true);
  }

  console.log('acceptance 5 — a fixture response is parsed for text and usage, offline');
  {
    // Shape of a Responses API payload: a reasoning item carrying no text, then
    // the message. The parser must skip the first and read the second.
    const fixture = {
      id: 'resp_abc123',
      model: 'gpt-5.6-sol',
      status: 'completed',
      output: [
        { type: 'reasoning', id: 'rs_1', summary: [] },
        {
          type: 'message',
          id: 'msg_1',
          role: 'assistant',
          content: [{ type: 'output_text', text: '### STRATEGY_VIEW\nRecommendation: stay Rome-only.' }],
        },
      ],
      usage: {
        input_tokens: 1200,
        output_tokens: 800,
        total_tokens: 2000,
        output_tokens_details: { reasoning_tokens: 500 },
      },
    };
    const parsed = parseResponse(fixture);
    check('final text extracted', parsed.text, '### STRATEGY_VIEW\nRecommendation: stay Rome-only.');
    check('model echoed', parsed.model, 'gpt-5.6-sol');
    check('response id echoed', parsed.id, 'resp_abc123');
    check('usage extracted', parsed.usage,
      { input_tokens: 1200, output_tokens: 800, reasoning_tokens: 500, total_tokens: 2000 });

    const multi = parseResponse({
      output: [{
        type: 'message',
        content: [
          { type: 'output_text', text: 'part one' },
          { type: 'output_text', text: 'part two' },
        ],
      }],
    });
    check('multiple text parts are joined', multi.text, 'part one\npart two');
    check('absent usage becomes nulls, never invented', multi.usage,
      { input_tokens: null, output_tokens: null, reasoning_tokens: null, total_tokens: null });

    check('an empty output throws',
      /no output text/.test(threw(() => parseResponse({ output: [], status: 'incomplete' })) || ''), true);
    check('a non-object payload throws', typeof threw(() => parseResponse(null)) === 'string', true);
  }
  {
    // The whole call path, still offline: an injected fetch returns the fixture.
    const state = { called: false, seen: null };
    const fetchImpl = async (url, init) => {
      state.called = true;
      state.seen = { url, init };
      return {
        ok: true,
        status: 200,
        json: async () => ({
          model: 'gpt-5.6-sol',
          output: [{ type: 'message', content: [{ type: 'output_text', text: 'stub answer' }] }],
          usage: { input_tokens: 10, output_tokens: 5, total_tokens: 15 },
        }),
      };
    };
    const result = await callStrategist(
      { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT },
      { env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl }
    );
    check('the injected transport was used', state.called, true);
    check('it posted to the Responses endpoint', state.seen.url, RESPONSES_ENDPOINT);
    check('it sent the bearer key', state.seen.init.headers.Authorization, 'Bearer sk-test');
    check('the answer came back', result.text, 'stub answer');
    check('the stage is echoed on the result', result.stage, STAGES.FIRST_PASS);
    check('usage came back', result.usage.total_tokens, 15);

    const errorMsg = await threwAsync(() => callStrategist(
      { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT },
      {
        env: { OPENAI_API_KEY: 'sk-test' },
        fetchImpl: async () => ({ ok: false, status: 429, text: async () => 'rate limited' }),
      }
    ));
    check('an API error surfaces the status', /429/.test(errorMsg || ''), true);
    check('…and the body', /rate limited/.test(errorMsg || ''), true);
  }

  console.log('acceptance 6 — the routing docs state the mode cannot implement or use Codex');
  {
    const claudeMd = fs.readFileSync(path.join(REPO_ROOT, 'CLAUDE.md'), 'utf8');
    const councilReadme = fs.readFileSync(path.join(REPO_ROOT, 'council', 'README.md'), 'utf8');
    const architecture = fs.readFileSync(
      path.join(REPO_ROOT, 'docs', 'strategic-council', 'README.md'), 'utf8');

    check('CLAUDE.md names Strategic Council mode', /Strategic Council/.test(claudeMd), true);
    check('CLAUDE.md forbids implementing in that mode', /do not implement/i.test(claudeMd), true);
    check('CLAUDE.md forbids Codex as the strategic critic',
      /never (?:invoke )?Codex as the strategic critic/i.test(claudeMd), true);
    check('CLAUDE.md names the general reasoning model', claudeMd.includes(DEFAULT_MODEL), true);
    check('CLAUDE.md keeps builder rules outside the mode',
      /outside Strategic Council mode/i.test(claudeMd), true);
    check('council/README.md documents the key variable',
      councilReadme.includes('OPENAI_API_KEY'), true);
    check('council/README.md states the key is never committed',
      /never committed|never commit/i.test(councilReadme), true);
    check('council/README.md states the mode does not implement',
      /never implements|does not implement|do not implement/i.test(councilReadme), true);
    check('the architecture doc keeps the independence rule',
      /Independence rule/i.test(architecture), true);
    check('the architecture doc rules out n8n orchestration for the MVP',
      /no n8n orchestration in the MVP/i.test(architecture), true);
    check('…and no longer diagrams a Council Room UI pipeline',
      /Council Room UI ->/.test(architecture), false);
    check('…and puts the owner in one Claude Code conversation',
      /\*\*one Claude Code conversation\*\*/.test(architecture), true);
  }

  console.log('deterministic synthesis — classification and the owner gate');
  {
    const converged = classifyCouncil({
      claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN',
      sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
    });
    check('agreement with nothing missing -> strong convergence',
      converged.classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('…and no owner decision is forced', converged.owner_decision_required, 'NO');

    check('…unless the question commits something normative',
      classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: [], normativeImpact: true,
      }).owner_decision_required, 'YES');

    check('agreement with missing evidence -> weak convergence',
      classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: ['no cost data for a second city'],
      }).classification, CLASSIFICATIONS.WEAK_CONVERGENCE);

    check('a material disagreement outranks a shared recommendation',
      classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: ['sequencing of the venue registry'], missingEvidence: [],
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('different recommendations -> meaningful disagreement',
      classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: false,
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('either side short of information outranks everything',
      classifyCouncil({
        claudePosition: 'INSUFFICIENT_INFORMATION', gptPosition: 'MAINTAIN',
        sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
      }).classification, CLASSIFICATIONS.INSUFFICIENT_INFORMATION);
    check('…and forces the owner gate',
      classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'INSUFFICIENT_INFORMATION',
        sameRecommendation: true,
      }).owner_decision_required, 'YES');

    check('an unknown position throws',
      typeof threw(() => classifyCouncil({
        claudePosition: 'YES', gptPosition: 'MAINTAIN',
      })) === 'string', true);

    // "Do not manufacture a numeric confidence score" (Issue #5).
    check('the result carries no score-shaped key',
      Object.keys(converged).some((k) => /confidence|score|probability|percent/i.test(k)), false);
    check('the result carries no number at all',
      Object.values(converged).some((v) => typeof v === 'number'), false);
  }

  console.log('the CLI parses its flags without needing a key');
  {
    const { parseArgv } = require(path.join(REPO_ROOT, 'council', 'cli.js'));
    check('flags with values are read',
      parseArgv(['--stage', 'FIRST_PASS', '--question', 'q']),
      { stage: 'FIRST_PASS', question: 'q' });
    check('boolean flags are read', parseArgv(['--dry-run', '--json']), { 'dry-run': true, json: true });
    check('a value-less flag throws',
      /needs a value/.test(threw(() => parseArgv(['--stage'])) || ''), true);
    check('an unknown flag throws', /unknown flag/.test(threw(() => parseArgv(['--merge'])) || ''), true);
    check('a bare argument throws',
      /unexpected argument/.test(threw(() => parseArgv(['merge'])) || ''), true);
  }

  console.log('the committed strategist role prompt is the one that gets sent');
  {
    const onDisk = fs.readFileSync(
      path.join(REPO_ROOT, 'prompts', 'STRATEGIC_COUNCIL_CHATGPT.md'), 'utf8');
    check('read from the repo, not inlined', readRolePrompt(), onDisk);
    check('and it travels as the instructions',
      buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION }).instructions, onDisk);
    check('an unreadable prompt path throws',
      /not readable/.test(threw(() => readRolePrompt('/nonexistent/prompt.md')) || ''), true);
  }
}

main().then(
  () => {
    console.log('');
    if (failures === 0) {
      console.log(`ALL PASS (${checks} checks)`);
      process.exit(0);
    }
    console.log(`${failures} of ${checks} checks FAILED`);
    process.exit(1);
  },
  (error) => {
    console.log(`\nthe suite itself threw: ${error.stack || error.message}`);
    process.exit(1);
  }
);

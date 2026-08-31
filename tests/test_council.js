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
  TIER_3_EFFORTS,
  RESPONSES_ENDPOINT,
  STAGES,
  CLASSIFICATIONS,
  readRolePrompt,
  buildRequest,
  parseResponse,
  readApiKey,
  callStrategist,
  classifyCouncil,
  buildCouncilResult,
} = require(COUNCIL);

/**
 * The suite asserts its own size, as test_guards.py does: a count that drifts
 * silently stops being a missing-test signal. The root README states the same
 * number, and a check below holds the two together.
 */
const CHECKS_EXPECTED = 212;

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
// The role prompt is a prompt of record: overridable only through the test
// seams, never through the request options (cycle 7).
const SEAM = { rolePrompt: ROLE_PROMPT };
// Every classification input is required (cycle 7): a default would answer the
// question the Council was asked. Tests not about a particular field spread
// this complete, deliberately neutral base and override what they are testing.
const NEUTRAL = {
  sameRecommendation: true,
  materialDisagreements: [],
  missingEvidence: [],
  normativeImpact: false,
};
// Tier 1 has no final positions, so it carries insufficiency as its own field
// (cycle 8). Tiers 2-3 must not carry it: their positions say it.
const NEUTRAL_TIER_1 = { ...NEUTRAL, tier: 1, insufficientInformation: false };
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
      { stage: STAGES.FIRST_PASS, question: QUESTION }, 
      { rolePrompt: ROLE_PROMPT, env: {}, fetchImpl: forbiddenFetch(state) }
    ));
    check('callStrategist without a key throws', /OPENAI_API_KEY/.test(msg || ''), true);
    check('…and never reached the network', state.called, false);
  }

  console.log('acceptance 2 — FIRST_PASS cannot carry the Claude view (independence rule)');
  {
    const msg = threw(() => buildRequest({
      stage: STAGES.FIRST_PASS, question: QUESTION,
      claudeView: CLAUDE_VIEW
    }, SEAM));
    check('passing a Claude view to FIRST_PASS throws', /independence rule/.test(msg || ''), true);

    const body = buildRequest({
      stage: STAGES.FIRST_PASS, question: QUESTION,
      context: 'DEC-104 fixes the loop roles.'
    }, SEAM);
    const serialised = JSON.stringify(body);
    check('the built request contains no Claude view text',
      serialised.includes('optimise for Rome first'), false);
    check('the built request contains no operator-view field',
      /OPERATOR_VIEW|claudeView|claude_view/i.test(serialised), false);
    check('the question does reach the strategist', body.input.includes(QUESTION), true);
    check('the context does reach the strategist',
      body.input.includes('DEC-104 fixes the loop roles.'), true);
    check('the stage is stated in the body', body.input.includes('Stage: FIRST_PASS'), true);
    // Cycle 5: the record kept on disk is gitignored; provider-side retention
    // would put the same material somewhere neither side controls.
    check('the request asks the provider not to retain it', body.store, false);

    // context is free text, so the named parameter is not the only way in.
    check('a council view marker in the context is refused',
      /carries a council view marker/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        context: `background\n\n${CLAUDE_VIEW}`
      }, SEAM)) || ''), true);
    check('…and in the question',
      /carries a council view marker/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: `${QUESTION} ### STRATEGY_VIEW`
      }, SEAM)) || ''), true);
    check('ordinary context is unaffected',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        context: 'DEC-104 fixes the loop roles.'
      }, SEAM).input.includes('DEC-104'), true);
  }
  {
    // The later stages are the ones that may see it, and they require it.
    check('CROSS_REVIEW without the Claude view throws',
      /requires the Claude view/.test(threw(() => buildRequest({
        stage: STAGES.CROSS_REVIEW, question: QUESTION,
        gptFirstPass: 'mine'
      }, SEAM)) || ''), true);

    const body = buildRequest({
      stage: STAGES.CROSS_REVIEW, question: QUESTION, claudeView: CLAUDE_VIEW,
      gptFirstPass: '### STRATEGY_VIEW\nmine'
    }, SEAM);
    check('CROSS_REVIEW does carry the Claude view',
      body.input.includes('optimise for Rome first'), true);
    check('FINAL_POSITION also requires it',
      /requires the Claude view/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION
      }, SEAM)) || ''), true);
    // A position can only be maintained or revised if it was formed first.
    check('FINAL_POSITION requires the strategist own first pass too',
      /never formed/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION,
        claudeView: CLAUDE_VIEW
      }, SEAM)) || ''), true);
    // Only tiers 2 and 3 reach this stage, and both cross-review first.
    check('FINAL_POSITION requires the cross-review exchange',
      /critiques before it concludes/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
        gptFirstPass: '### STRATEGY_VIEW\nmine'
      }, SEAM)) || ''), true);
    const finalBody = buildRequest({
      stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
      gptFirstPass: '### STRATEGY_VIEW\nmine', exchange: 'the critique'
    }, SEAM);
    check('FINAL_POSITION builds when the whole protocol precedes it',
      finalBody.input.includes('Your first-pass STRATEGY_VIEW')
      && finalBody.input.includes('the critique'), true);
  }

  console.log('acceptance 3 — the model defaults to the general reasoning model');
  {
    const body = buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION }, SEAM);
    check('default model', body.model, 'gpt-5.6-sol');
    check('exported default agrees', DEFAULT_MODEL, 'gpt-5.6-sol');
    check('the model is pinned: another OpenAI model is refused (DEC-008)',
      /DEC-008 fixes the strategic critic/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: 'gpt-4.1'
      }, SEAM)) || ''), true);
    check('…including a near-miss variant',
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: 'gpt-5.6-sol-mini'
      }, SEAM)) === 'string', true);
    check('the decided model is accepted',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: DEFAULT_MODEL
      }, SEAM).model, DEFAULT_MODEL);
    check('a Codex model is refused as strategic critic',
      /never a coding model/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, model: 'codex-max'
      }, SEAM)) || ''), true);
    check('…case-insensitively',
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, model: 'GPT-5-CODEX'
      }, SEAM)) === 'string', true);
    check('the endpoint is the Responses API',
      RESPONSES_ENDPOINT, 'https://api.openai.com/v1/responses');
  }

  console.log('the tier governs the depth of a stage request');
  {
    check('tier 3 refuses the default effort',
      /tier 3 requires reasoning effort/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier: 3
      }, SEAM)) || ''), true);
    for (const effort of TIER_3_EFFORTS) {
      check(`tier 3 accepts '${effort}'`,
        buildRequest({
          stage: STAGES.FIRST_PASS, question: QUESTION, tier: 3, effort
        }, SEAM).reasoning.effort, effort);
    }
    check('tiers 1 and 2 are content with the default',
      [1, 2].every((tier) => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier
      }, SEAM).reasoning.effort === DEFAULT_EFFORT), true);
    check('buildRequest keeps its default when no tier is stated (the CLI requires one)',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION
      }, SEAM).reasoning.effort, DEFAULT_EFFORT);
    // Cycle 6: tier 1 stops after the two first-pass views, so a later stage
    // at tier 1 is a run whose positions the tier-1 synthesis would refuse.
    for (const stage of [STAGES.CROSS_REVIEW, STAGES.FINAL_POSITION]) {
      check(`tier 1 refuses ${stage}`,
        /tier 1 has no/.test(threw(() => buildRequest({
          stage, question: QUESTION, tier: 1, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, SEAM)) || ''), true);
      check(`…and tier 2 allows ${stage}`,
        buildRequest({
          stage, question: QUESTION, tier: 2, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, SEAM).reasoning.effort, DEFAULT_EFFORT);
    }
    check('tier 1 still allows the stage it does have',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier: 1
      }, SEAM).reasoning.effort, DEFAULT_EFFORT);
    check('an impossible tier is refused',
      /tier must be 1, 2 or 3/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier: 4
      }, SEAM)) || ''), true);
  }

  console.log('acceptance 4 — reasoning effort defaults to high and is validated');
  {
    const body = buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION }, SEAM);
    check('default effort', body.reasoning.effort, 'high');
    check('exported default agrees', DEFAULT_EFFORT, 'high');
    check('allowed tiers', ALLOWED_EFFORTS, ['high', 'xhigh', 'max']);
    for (const effort of ALLOWED_EFFORTS) {
      check(`'${effort}' is accepted`,
        buildRequest({
          stage: STAGES.FIRST_PASS, question: QUESTION, effort
        }, SEAM).reasoning.effort, effort);
    }
    check("'low' is refused (the Council does not reason cheaply)",
      /not allowed/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, effort: 'low'
      }, SEAM)) || ''), true);
    check("'' is refused",
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, effort: ''
      }, SEAM)) === 'string', true);
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
      /no output text/.test(threw(() => parseResponse({ output: [] })) || ''), true);
    // A truncated fragment is non-empty but is not a strategic view.
    check('an incomplete response throws rather than returning a fragment',
      /is 'incomplete'/.test(threw(() => parseResponse({
        status: 'incomplete',
        incomplete_details: { reason: 'max_output_tokens' },
        output: [{ type: 'message', content: [{ type: 'output_text', text: 'half a th' }] }],
      })) || ''), true);
    check('…and surfaces why',
      /max_output_tokens/.test(threw(() => parseResponse({
        status: 'incomplete',
        incomplete_details: { reason: 'max_output_tokens' },
        output: [{ type: 'message', content: [{ type: 'output_text', text: 'half a th' }] }],
      })) || ''), true);
    check("a 'completed' status parses normally", parseResponse({
      status: 'completed',
      output: [{ type: 'message', content: [{ type: 'output_text', text: 'done' }] }],
    }).text, 'done');
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
      { stage: STAGES.FIRST_PASS, question: QUESTION }, 
      { rolePrompt: ROLE_PROMPT, env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl }
    );
    check('the injected transport was used', state.called, true);
    check('it posted to the Responses endpoint', state.seen.url, RESPONSES_ENDPOINT);
    check('it sent the bearer key', state.seen.init.headers.Authorization, 'Bearer sk-test');
    check('the answer came back', result.text, 'stub answer');
    check('the stage is echoed on the result', result.stage, STAGES.FIRST_PASS);
    check('usage came back', result.usage.total_tokens, 15);

    // The role prompt requires one of three tokens from the final stage.
    const malformed = async () => ({
      ok: true, status: 200,
      json: async () => ({
        output: [{ type: 'message', content: [{ type: 'output_text', text: 'I think we should wait.' }] }],
      }),
    });
    check('a completed FINAL_POSITION with no position is refused',
      /exactly one of/.test(await threwAsync(() => callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, 
        { rolePrompt: ROLE_PROMPT, env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl: malformed }
      )) || ''), true);
    check('…and prose that merely uses the word does not count',
      /exactly one of/.test(await threwAsync(() => callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, 
        { rolePrompt: ROLE_PROMPT,
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'I maintain my earlier view.' }] }] }),
          }),
        }
      )) || ''), true);
    check('a declared position passes',
      (await callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, 
        { rolePrompt: ROLE_PROMPT,
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'MAINTAIN — Rome first.' }] }] }),
          }),
        }
      )).stage, STAGES.FINAL_POSITION);
    // Cycle 5: an unanchored search accepted "I cannot choose between MAINTAIN
    // and REVISE" by matching the first token. Two positions are no position.
    const ambiguous = await threwAsync(() => callStrategist(
      {
        stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
        gptFirstPass: 'mine', exchange: 'the critique'
      }, 
      { rolePrompt: ROLE_PROMPT,
        env: { OPENAI_API_KEY: 'sk-test' },
        fetchImpl: async () => ({
          ok: true, status: 200,
          json: async () => ({ output: [{ type: 'message', content: [
            { type: 'output_text', text: 'I cannot choose between MAINTAIN and REVISE.' }] }] }),
        }),
      }
    ));
    check('two positions in one answer are refused, not resolved by first match',
      /exactly one of/.test(ambiguous || ''), true);
    check('…and the refusal names both tokens it found',
      /MAINTAIN, REVISE|REVISE, MAINTAIN/.test(ambiguous || ''), true);
    check('one position repeated is still one position',
      (await callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique'
        }, 
        { rolePrompt: ROLE_PROMPT,
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'REVISE. To restate: REVISE, and here is why.' }] }] }),
          }),
        }
      )).stage, STAGES.FINAL_POSITION);
    check('a first pass is not held to that rule',
      (await callStrategist(
        { stage: STAGES.FIRST_PASS, question: QUESTION }, 
        { rolePrompt: ROLE_PROMPT,
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'Recommendation: stay Rome-only.' }] }] }),
          }),
        }
      )).text, 'Recommendation: stay Rome-only.');

    const errorMsg = await threwAsync(() => callStrategist(
      { stage: STAGES.FIRST_PASS, question: QUESTION }, 
      { rolePrompt: ROLE_PROMPT,
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
    check('the architecture doc keeps no second copy of the independence claim',
      /structurally cannot carry/.test(architecture), false);
    check('…nor the weaker restatement of the same guarantee',
      /no field that could carry/.test(architecture), false);
    check('…and it says the tool cannot enforce all of it',
      /cannot enforce/i.test(architecture), true);
    check('…and points at the file that owns it',
      /council\/README\.md/.test(architecture), true);
    check('neither doc promises a budget the tool does not enforce',
      /monthly hard budget and require owner approval/.test(architecture), false);
    check('the architecture doc puts the hard budget on the OpenAI account',
      /OpenAI account/.test(architecture), true);
    check('council/README.md agrees on where the budget lives',
      /hard budget lives on the OpenAI account/i.test(councilReadme), true);
    check('the architecture doc rules out n8n orchestration for the MVP',
      /no n8n orchestration in the MVP/i.test(architecture), true);
    check('…and no longer diagrams a Council Room UI pipeline',
      /Council Room UI ->/.test(architecture), false);
    check('…and puts the owner in one Claude Code conversation',
      /\*\*one Claude Code conversation\*\*/.test(architecture), true);
    // Cycle 8: the MVP flow listed the strategist call before the Operator
    // view, which in one conversation is the independence rule run backwards.
    check('the MVP flow forms the Operator view before the strategist call',
      architecture.indexOf('Operator\nview formed and retained')
        < architecture.indexOf('independent strategist view via council/cli.js'), true);
    check('…and no longer lists the GPT view first',
      /independent\nGPT view via council\/cli\.js -> independent Operator view/.test(architecture),
      false);
    check('…and says why the order is the rule, not a preference',
      /order is the independence rule/.test(architecture), true);
  }

  console.log('deterministic synthesis — classification and the owner gate');
  {
    const converged = classifyCouncil({ ...NEUTRAL,
      tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN',
      sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
    });
    check('agreement with nothing missing -> strong convergence',
      converged.classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('…and no owner decision is forced', converged.owner_decision_required, 'NO');

    check('…unless the question commits something normative',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: [], normativeImpact: true,
      }).owner_decision_required, 'YES');

    check('agreement with missing evidence -> weak convergence',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: ['no cost data for a second city'],
      }).classification, CLASSIFICATIONS.WEAK_CONVERGENCE);

    check('a material disagreement outranks a shared recommendation',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: ['sequencing of the venue registry'], missingEvidence: [],
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('different recommendations -> meaningful disagreement',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: false,
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('either side short of information outranks everything',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'INSUFFICIENT_INFORMATION', gptPosition: 'MAINTAIN',
        sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
      }).classification, CLASSIFICATIONS.INSUFFICIENT_INFORMATION);
    check('…and forces the owner gate',
      classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'INSUFFICIENT_INFORMATION',
        sameRecommendation: true,
      }).owner_decision_required, 'YES');

    check('an unknown position throws',
      typeof threw(() => classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'YES', gptPosition: 'MAINTAIN',
      })) === 'string', true);

    // Tier 1 stops after the two first-pass views, so there is no MAINTAIN or
    // REVISE to report and the synthesis must not demand one.
    check('tier 1 synthesises without any final position',
      classifyCouncil({ ...NEUTRAL_TIER_1 }).classification,
      CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('…and still separates disagreement',
      classifyCouncil({ ...NEUTRAL_TIER_1, sameRecommendation: false }).classification,
      CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    // Cycle 8: with no positions to carry it, tier 1 could only converge or
    // disagree — it had no way to report that the evidence ran out.
    check('tier 1 can report insufficient information',
      classifyCouncil({ ...NEUTRAL_TIER_1, insufficientInformation: true }).classification,
      CLASSIFICATIONS.INSUFFICIENT_INFORMATION);
    check('…and it forces the owner gate',
      classifyCouncil({ ...NEUTRAL_TIER_1, insufficientInformation: true })
        .owner_decision_required, 'YES');
    check('…even when both sides otherwise agreed',
      classifyCouncil({
        ...NEUTRAL_TIER_1, insufficientInformation: true, sameRecommendation: true,
      }).classification, CLASSIFICATIONS.INSUFFICIENT_INFORMATION);
    check('omitting it on tier 1 is an error, not a quiet false',
      /tier 1 requires insufficientInformation/.test(threw(() => classifyCouncil({
        ...NEUTRAL, tier: 1,
      })) || ''), true);
    check('…and a string is refused like the other booleans',
      /not string/.test(threw(() => classifyCouncil({
        ...NEUTRAL_TIER_1, insufficientInformation: 'false',
      })) || ''), true);
    check('tiers 2 and 3 refuse it: their positions say it',
      /the run did not follow the tier it reports/.test(threw(() => classifyCouncil({
        ...NEUTRAL, tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN',
        insufficientInformation: false,
      })) || ''), true);

    // Cycle 7: a default answers the question the Council was asked. An omitted
    // materialDisagreements read as "they did not disagree", which is a finding.
    for (const field of
      ['sameRecommendation', 'materialDisagreements', 'missingEvidence', 'normativeImpact']) {
      const partial = { ...NEUTRAL_TIER_1 };
      delete partial[field];
      check(`omitting ${field} is an error, not a silent gap`,
        new RegExp(`${field} is required`).test(threw(() => classifyCouncil(partial)) || ''), true);
      check(`…and the message says it was omitted, not mistyped`,
        /not omitted/.test(threw(() => classifyCouncil(partial)) || ''), true);
    }
    check('a wrong type is still distinguished from an omission',
      /not string/.test(threw(() => classifyCouncil({
        ...NEUTRAL_TIER_1, missingEvidence: 'none',
      })) || ''), true);

    // The tier is what makes the position rules enforceable at all.
    check('the tier is required, not inferred',
      /tier must be 1, 2 or 3/.test(threw(() => classifyCouncil({ ...NEUTRAL,
        claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
      })) || ''), true);
    check('a position on a tier-1 run is refused: it was not tier 1',
      /a position here means the run was not tier 1/.test(threw(() => classifyCouncil({
        ...NEUTRAL_TIER_1, claudePosition: 'MAINTAIN',
      })) || ''), true);
    check('a partial position pair is refused on tier 2',
      /both claudePosition and gptPosition are required; 1 of 2 supplied/.test(
        threw(() => classifyCouncil({ ...NEUTRAL,
          tier: 2, claudePosition: 'MAINTAIN', sameRecommendation: true,
        })) || ''), true);
    check('…and a tier-2 run missing both is refused rather than read as tier 1',
      /0 of 2 supplied/.test(threw(() => classifyCouncil({ ...NEUTRAL,
        tier: 2, sameRecommendation: true,
      })) || ''), true);
    check('an invalid position is still refused',
      /must be one of MAINTAIN/.test(threw(() => classifyCouncil({ ...NEUTRAL,
        tier: 2, claudePosition: 'PROBABLY', gptPosition: 'MAINTAIN', sameRecommendation: true,
      })) || ''), true);

    // "Do not manufacture a numeric confidence score" (Issue #5).
    check('the result carries no score-shaped key',
      Object.keys(converged).some((k) => /confidence|score|probability|percent/i.test(k)), false);
    check('the result carries no number at all',
      Object.values(converged).some((v) => typeof v === 'number'), false);
  }

  console.log('the council result the owner reads — produced, not described');
  {
    const judgements = {
      tier: 2,
      question: QUESTION,
      claudeRecommendation: 'Optimise for Rome; revisit at the second city.',
      gptRecommendation: 'Same, and record the trigger that would reopen it.',
      strongestAgreement: 'No second city is in evidence yet.',
      costAndReversibility: 'Low cost now; generalising later is a refactor, not a rewrite.',
      assumptions: ['the gazetteer stays Rome-shaped'],
      claudePosition: 'MAINTAIN',
      gptPosition: 'MAINTAIN',
      sameRecommendation: true,
      materialDisagreements: [],
      missingEvidence: [],
      normativeImpact: true,
    };
    const result = buildCouncilResult(judgements);
    for (const field of ['tier', 'question', 'claude_final_recommendation',
      'gpt_final_recommendation', 'strongest_agreement', 'meaningful_disagreement',
      'assumptions', 'failure_scenarios', 'reconsideration_triggers',
      'missing_evidence', 'cost_and_reversibility',
      'classification', 'OWNER_DECISION_REQUIRED']) {
      check(`the result carries '${field}'`,
        Object.prototype.hasOwnProperty.call(result, field), true);
    }
    check('it classifies', result.classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('it gates on the owner when the question is normative',
      result.OWNER_DECISION_REQUIRED, 'YES');
    check('it still manufactures no confidence score',
      Object.keys(result).some((k) => /confidence|score|probability|percent/i.test(k)), false);
    check('…and the only number is the tier, which is a label not a measure',
      Object.entries(result).filter(([, v]) => typeof v === 'number').map(([k]) => k),
      ['tier']);
    // A judgements file may be model-authored, and "false" is a truthy string.
    check('a string "false" is refused rather than coerced',
      /sameRecommendation is required and must be a boolean/.test(threw(() => buildCouncilResult({
        ...judgements, sameRecommendation: 'false',
      })) || ''), true);
    check('normativeImpact is type-checked too',
      /normativeImpact is required and must be a boolean/.test(threw(() => buildCouncilResult({
        ...judgements, normativeImpact: 'false',
      })) || ''), true);
    // Tier 3 is the foundational tier; its evidence is the contract.
    const tier3 = { ...judgements, tier: 3 };
    for (const field of ['assumptions', 'failureScenarios', 'reconsiderationTriggers']) {
      check(`tier 3 requires ${field}`,
        new RegExp(`tier 3 requires ${field}`).test(threw(() => buildCouncilResult({
          ...tier3,
          failureScenarios: ['the second city never materialises'],
          reconsiderationTriggers: ['a second city is funded'],
          [field]: [],
        })) || ''), true);
    }
    for (const blank of [[''], ['   '], [null], [{}]]) {
      check(`tier 3 refuses a content-free entry ${JSON.stringify(blank)}`,
        /a blank entry names nothing/.test(threw(() => buildCouncilResult({
          ...tier3,
          failureScenarios: ['the second city never materialises'],
          reconsiderationTriggers: ['a second city is funded'],
          assumptions: blank,
        })) || ''), true);
    }
    const founded = buildCouncilResult({
      ...tier3,
      failureScenarios: ['the second city never materialises'],
      reconsiderationTriggers: ['a second city is funded'],
    });
    // Cycle 8: tier 3 is the foundational tier by definition, so it always
    // reaches the owner. A model-authored normativeImpact: false must not clear
    // the gate on the most consequential class of question there is.
    const cleared = buildCouncilResult({
      ...tier3,
      failureScenarios: ['the second city never materialises'],
      reconsiderationTriggers: ['a second city is funded'],
      normativeImpact: false,
    });
    check('a tier-3 run with everything aligned still gates on the owner',
      cleared.OWNER_DECISION_REQUIRED, 'YES');
    check('…while still reporting the convergence honestly',
      cleared.classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('tier 2 in the same shape does not force the gate',
      buildCouncilResult({ ...judgements, normativeImpact: false }).OWNER_DECISION_REQUIRED,
      'NO');
    check('a complete tier 3 emits its evidence',
      [founded.failure_scenarios.length, founded.reconsideration_triggers.length,
        founded.assumptions.length], [1, 1, 1]);
    check('tier 2 does not demand tier-3 evidence',
      buildCouncilResult(judgements).failure_scenarios, []);

    check('a missing required field throws rather than emitting a gap',
      /strongestAgreement is required/.test(threw(() => buildCouncilResult({
        ...judgements, strongestAgreement: '',
      })) || ''), true);
  }
  {
    // The whole synthesis path through the CLI, offline and keyless.
    const os = require('os');
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'council-'));
    const file = path.join(tmp, 'judgements.json');
    fs.writeFileSync(file, JSON.stringify({
      tier: 2,
      question: 'q',
      claudeRecommendation: 'a',
      gptRecommendation: 'b',
      strongestAgreement: 'c',
      costAndReversibility: 'd',
      claudePosition: 'MAINTAIN',
      gptPosition: 'REVISE',
      sameRecommendation: false,
      materialDisagreements: [],
      missingEvidence: [],
      normativeImpact: false,
    }));
    const { main } = require(path.join(REPO_ROOT, 'council', 'cli.js'));
    const written = [];
    const realWrite = process.stdout.write.bind(process.stdout);
    process.stdout.write = (chunk) => { written.push(chunk); return true; };
    let code;
    try {
      code = await main(['--synthesis-file', file]);
    } finally {
      process.stdout.write = realWrite;
      fs.rmSync(tmp, { recursive: true, force: true });
    }
    check('the CLI synthesis path exits 0 with no key', code, 0);
    const printed = JSON.parse(written.join(''));
    check('…and prints the classification',
      printed.classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);
    check('…and the owner gate', printed.OWNER_DECISION_REQUIRED, 'YES');
  }

  console.log('the repository records that made this change legal');
  {
    const dec008 = fs.readFileSync(
      path.join(REPO_ROOT, 'decisions', 'DEC-008-three-layer-ai-model.md'), 'utf8');
    // decisions/README.md names the required fields of an entry.
    for (const field of ['Status:', 'Question:', 'Options:', 'Impact:', 'Blocks:',
      'Decided by:', 'Date:', 'recommendation:']) {
      check(`DEC-008 carries '${field}'`, dec008.includes(field), true);
    }
    check('DEC-008 is decided by the owner', /Decided by: Owner/.test(dec008), true);
    check('DEC-008 pins the strategist model', dec008.includes(DEFAULT_MODEL), true);

    const dec007 = fs.readFileSync(
      path.join(REPO_ROOT, 'decisions', 'DEC-007-review-archive-location.md'), 'utf8');
    // DEC-008 describes DEC-007 as fixed, which is only true once it is decided.
    check('DEC-007 is DECIDED, as DEC-008 states', /Status: DECIDED/.test(dec007), true);

    const changelog = fs.readFileSync(path.join(REPO_ROOT, 'prompts', 'CHANGELOG.md'), 'utf8');
    check('the council prompts are in the prompt changelog',
      changelog.includes('STRATEGIC_COUNCIL_CHATGPT.md')
      && changelog.includes('STRATEGIC_COUNCIL_CLAUDE.md'), true);
    check('…and the changelog states the revision handling',
      /Revision bumped/.test(changelog), true);
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
    check('--model is not a flag any more (DEC-008 pins it)',
      /unknown flag/.test(threw(() => parseArgv(['--model', 'gpt-4.1'])) || ''), true);
    check('-h is reachable and means help', parseArgv(['-h']), { help: true });

    // The rendered help must not advertise as optional what the code requires.
    const { execFileSync } = require('child_process');
    const help = execFileSync('node',
      [path.join(REPO_ROOT, 'council', 'cli.js'), '--help'], { encoding: 'utf8' });
    check('help does not call the first-pass file optional',
      /\[--gpt-first-pass-file/.test(help), false);
    check('help does not call the exchange file optional',
      /\[--exchange-file/.test(help), false);
    check('help documents the synthesis path', help.includes('--synthesis-file'), true);
    check('help states the tier is required on a stage request',
      /--tier[^\n]*required/.test(help), true);
    check('…and every stage example passes one',
      help.split('\n').filter((l) => l.includes('--stage'))
        .every((l) => l.includes('--tier')), true);

    // Cycle 5: a stage could run at the default depth and be reported as tier 3
    // by the synthesis afterwards. Omission is the one way to skip the rule.
    const { main } = require(path.join(REPO_ROOT, 'council', 'cli.js'));
    check('a stage request without --tier is refused',
      /--tier is required/.test(
        await threwAsync(() => main(['--stage', 'FIRST_PASS', '--question', 'q'])) || ''), true);
    check('a later stage at tier 1 is refused at the command line',
      /tier 1 has no CROSS_REVIEW/.test(
        await threwAsync(() => main([
          '--stage', 'CROSS_REVIEW', '--tier', '1', '--question', 'q',
          '--claude-view', 'theirs', '--gpt-first-pass', 'mine', '--dry-run',
        ])) || ''), true);
    check('…and the synthesis path still needs no tier flag',
      /cannot read --synthesis-file/.test(
        await threwAsync(() => main(['--synthesis-file', '/nonexistent.json'])) || ''), true);

    // Cycle 7: a session record logs a call that was paid for, so a second save
    // in the same millisecond must not silently replace the first.
    {
      const { saveSession } = require(path.join(REPO_ROOT, 'council', 'cli.js'));
      const os2 = require('os');
      const dir = fs.mkdtempSync(path.join(os2.tmpdir(), 'council-save-'));
      const now = new Date('2026-08-31T15:00:00.000Z');
      const first = saveSession({ stage: 'FIRST_PASS', text: 'one' }, { dir, now });
      const second = saveSession({ stage: 'FIRST_PASS', text: 'two' }, { dir, now });
      check('a same-millisecond save does not reuse the filename', first === second, false);
      check('…and both records survive', fs.readdirSync(dir).length, 2);
      check('…with the first one intact',
        JSON.parse(fs.readFileSync(first, 'utf8')).text, 'one');
      check('…and the second one too',
        JSON.parse(fs.readFileSync(second, 'utf8')).text, 'two');
      fs.rmSync(dir, { recursive: true, force: true });
    }

    // Cycle 5: process.exit() dropped whatever stdout had buffered, so a large
    // result was truncated at the pipe buffer. --dry-run makes no call, so the
    // whole path is exercised offline.
    const os = require('os');
    const bigDir = fs.mkdtempSync(path.join(os.tmpdir(), 'council-'));
    const bigFile = path.join(bigDir, 'context.md');
    fs.writeFileSync(bigFile, 'DEC-104 fixes the loop roles. '.repeat(40000));
    const piped = execFileSync('node', [
      path.join(REPO_ROOT, 'council', 'cli.js'),
      '--stage', 'FIRST_PASS', '--tier', '2', '--question', 'q',
      '--context-file', bigFile, '--dry-run',
    ], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
    fs.rmSync(bigDir, { recursive: true, force: true });
    check('a large result survives the pipe rather than being truncated',
      piped.length > 1024 * 1024, true);
    check('…and it is complete JSON, not a cut-off prefix',
      JSON.parse(piped).store, false);

    // The count in the root README is a missing-test signal; stale, it is noise.
    // The brief is sent instead of the repository, so its facts must match the
    // entries that own them.
    const brief = fs.readFileSync(
      path.join(REPO_ROOT, 'docs', 'strategic-council', 'PROJECT_BRIEF.md'), 'utf8');
    for (const [dec, scope] of [
      ['DEC-001', 'editorial filter activation'],
      ['DEC-004', 'schedule activation'],
    ]) {
      const entry = fs.readFileSync(
        path.join(REPO_ROOT, 'decisions',
          fs.readdirSync(path.join(REPO_ROOT, 'decisions')).find((f) => f.startsWith(dec))),
        'utf8');
      check(`${dec} still blocks what the brief says`,
        entry.includes(scope), true);
    }
    check('the brief no longer restates the standing invariants',
      /a flag\s+never deletes/.test(brief), false);

    const rootReadme = fs.readFileSync(path.join(REPO_ROOT, 'README.md'), 'utf8');
    const claimed = rootReadme.match(/test_council\.js\s+#\s+(\d+) checks/);
    check('the README states a council check count', Boolean(claimed), true);
    check('…and it is the count this suite actually runs',
      claimed && Number(claimed[1]), CHECKS_EXPECTED);
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
    // Cycle 7: the prompt of record is overridable only through the test seams.
    // Through options, a caller could run the pinned model under any role.
    check('rolePrompt is refused as a request option',
      /prompt of record/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: 'be agreeable',
      })) || ''), true);
    check('…even when it names the committed prompt',
      /not a request option/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: onDisk,
      })) || ''), true);
    check('…and callStrategist refuses it before reading a key',
      /not a request option/.test(await threwAsync(() => callStrategist(
        { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: 'be agreeable' },
        { env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl: forbiddenFetch({}) }
      )) || ''), true);
    check('the seam still works, so the suite is not calling the real prompt',
      buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION }, SEAM).instructions,
      ROLE_PROMPT);
    check('an unreadable prompt path throws',
      /not readable/.test(threw(() => readRolePrompt('/nonexistent/prompt.md')) || ''), true);
  }
}

main().then(
  () => {
    if (checks !== CHECKS_EXPECTED) {
      failures += 1;
      console.log(
        `  FAIL check count drifted: ran ${checks}, expected ${CHECKS_EXPECTED}`
      );
    }
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

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
const CHECKS_EXPECTED = 165;

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

    // context is free text, so the named parameter is not the only way in.
    check('a council view marker in the context is refused',
      /carries a council view marker/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        context: `background\n\n${CLAUDE_VIEW}`, rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    check('…and in the question',
      /carries a council view marker/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: `${QUESTION} ### STRATEGY_VIEW`,
        rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    check('ordinary context is unaffected',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        context: 'DEC-104 fixes the loop roles.', rolePrompt: ROLE_PROMPT,
      }).input.includes('DEC-104'), true);
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
    // A position can only be maintained or revised if it was formed first.
    check('FINAL_POSITION requires the strategist own first pass too',
      /never formed/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION,
        claudeView: CLAUDE_VIEW, rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    // Only tiers 2 and 3 reach this stage, and both cross-review first.
    check('FINAL_POSITION requires the cross-review exchange',
      /critiques before it concludes/.test(threw(() => buildRequest({
        stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
        gptFirstPass: '### STRATEGY_VIEW\nmine', rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    const finalBody = buildRequest({
      stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
      gptFirstPass: '### STRATEGY_VIEW\nmine', exchange: 'the critique',
      rolePrompt: ROLE_PROMPT,
    });
    check('FINAL_POSITION builds when the whole protocol precedes it',
      finalBody.input.includes('Your first-pass STRATEGY_VIEW')
      && finalBody.input.includes('the critique'), true);
  }

  console.log('acceptance 3 — the model defaults to the general reasoning model');
  {
    const body = buildRequest({ stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT });
    check('default model', body.model, 'gpt-5.6-sol');
    check('exported default agrees', DEFAULT_MODEL, 'gpt-5.6-sol');
    check('the model is pinned: another OpenAI model is refused (DEC-008)',
      /DEC-008 fixes the strategic critic/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: 'gpt-4.1', rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    check('…including a near-miss variant',
      typeof threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: 'gpt-5.6-sol-mini', rolePrompt: ROLE_PROMPT,
      })) === 'string', true);
    check('the decided model is accepted',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION,
        model: DEFAULT_MODEL, rolePrompt: ROLE_PROMPT,
      }).model, DEFAULT_MODEL);
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

  console.log('the tier governs the depth of a stage request');
  {
    check('tier 3 refuses the default effort',
      /tier 3 requires reasoning effort/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier: 3, rolePrompt: ROLE_PROMPT,
      })) || ''), true);
    for (const effort of TIER_3_EFFORTS) {
      check(`tier 3 accepts '${effort}'`,
        buildRequest({
          stage: STAGES.FIRST_PASS, question: QUESTION, tier: 3, effort,
          rolePrompt: ROLE_PROMPT,
        }).reasoning.effort, effort);
    }
    check('tiers 1 and 2 are content with the default',
      [1, 2].every((tier) => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier, rolePrompt: ROLE_PROMPT,
      }).reasoning.effort === DEFAULT_EFFORT), true);
    check('the tier stays optional on a stage request',
      buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT,
      }).reasoning.effort, DEFAULT_EFFORT);
    check('an impossible tier is refused',
      /tier must be 1, 2 or 3/.test(threw(() => buildRequest({
        stage: STAGES.FIRST_PASS, question: QUESTION, tier: 4, rolePrompt: ROLE_PROMPT,
      })) || ''), true);
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
      { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT },
      { env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl }
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
      /states no position/.test(await threwAsync(() => callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique', rolePrompt: ROLE_PROMPT,
        },
        { env: { OPENAI_API_KEY: 'sk-test' }, fetchImpl: malformed }
      )) || ''), true);
    check('…and prose that merely uses the word does not count',
      /states no position/.test(await threwAsync(() => callStrategist(
        {
          stage: STAGES.FINAL_POSITION, question: QUESTION, claudeView: CLAUDE_VIEW,
          gptFirstPass: 'mine', exchange: 'the critique', rolePrompt: ROLE_PROMPT,
        },
        {
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
          gptFirstPass: 'mine', exchange: 'the critique', rolePrompt: ROLE_PROMPT,
        },
        {
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'MAINTAIN — Rome first.' }] }] }),
          }),
        }
      )).stage, STAGES.FINAL_POSITION);
    check('a first pass is not held to that rule',
      (await callStrategist(
        { stage: STAGES.FIRST_PASS, question: QUESTION, rolePrompt: ROLE_PROMPT },
        {
          env: { OPENAI_API_KEY: 'sk-test' },
          fetchImpl: async () => ({
            ok: true, status: 200,
            json: async () => ({ output: [{ type: 'message', content: [
              { type: 'output_text', text: 'Recommendation: stay Rome-only.' }] }] }),
          }),
        }
      )).text, 'Recommendation: stay Rome-only.');

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
    check('the architecture doc keeps no second copy of the independence claim',
      /structurally cannot carry/.test(architecture), false);
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
  }

  console.log('deterministic synthesis — classification and the owner gate');
  {
    const converged = classifyCouncil({
      tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN',
      sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
    });
    check('agreement with nothing missing -> strong convergence',
      converged.classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('…and no owner decision is forced', converged.owner_decision_required, 'NO');

    check('…unless the question commits something normative',
      classifyCouncil({
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: [], normativeImpact: true,
      }).owner_decision_required, 'YES');

    check('agreement with missing evidence -> weak convergence',
      classifyCouncil({
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: true,
        materialDisagreements: [], missingEvidence: ['no cost data for a second city'],
      }).classification, CLASSIFICATIONS.WEAK_CONVERGENCE);

    check('a material disagreement outranks a shared recommendation',
      classifyCouncil({
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
        materialDisagreements: ['sequencing of the venue registry'], missingEvidence: [],
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('different recommendations -> meaningful disagreement',
      classifyCouncil({
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'REVISE', sameRecommendation: false,
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    check('either side short of information outranks everything',
      classifyCouncil({
        tier: 2, claudePosition: 'INSUFFICIENT_INFORMATION', gptPosition: 'MAINTAIN',
        sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
      }).classification, CLASSIFICATIONS.INSUFFICIENT_INFORMATION);
    check('…and forces the owner gate',
      classifyCouncil({
        tier: 2, claudePosition: 'MAINTAIN', gptPosition: 'INSUFFICIENT_INFORMATION',
        sameRecommendation: true,
      }).owner_decision_required, 'YES');

    check('an unknown position throws',
      typeof threw(() => classifyCouncil({
        tier: 2, claudePosition: 'YES', gptPosition: 'MAINTAIN',
      })) === 'string', true);

    // Tier 1 stops after the two first-pass views, so there is no MAINTAIN or
    // REVISE to report and the synthesis must not demand one.
    check('tier 1 synthesises without any final position',
      classifyCouncil({
        tier: 1, sameRecommendation: true, materialDisagreements: [], missingEvidence: [],
      }).classification, CLASSIFICATIONS.STRONG_CONVERGENCE);
    check('…and still separates disagreement',
      classifyCouncil({
        tier: 1, sameRecommendation: false, materialDisagreements: [], missingEvidence: [],
      }).classification, CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT);

    // The tier is what makes the position rules enforceable at all.
    check('the tier is required, not inferred',
      /tier must be 1, 2 or 3/.test(threw(() => classifyCouncil({
        claudePosition: 'MAINTAIN', gptPosition: 'MAINTAIN', sameRecommendation: true,
      })) || ''), true);
    check('a position on a tier-1 run is refused: it was not tier 1',
      /a position here means the run was not tier 1/.test(threw(() => classifyCouncil({
        tier: 1, claudePosition: 'MAINTAIN', sameRecommendation: true,
      })) || ''), true);
    check('a partial position pair is refused on tier 2',
      /both claudePosition and gptPosition are required; 1 of 2 supplied/.test(
        threw(() => classifyCouncil({
          tier: 2, claudePosition: 'MAINTAIN', sameRecommendation: true,
        })) || ''), true);
    check('…and a tier-2 run missing both is refused rather than read as tier 1',
      /0 of 2 supplied/.test(threw(() => classifyCouncil({
        tier: 2, sameRecommendation: true,
      })) || ''), true);
    check('an invalid position is still refused',
      /must be one of MAINTAIN/.test(threw(() => classifyCouncil({
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
      /sameRecommendation must be a boolean/.test(threw(() => buildCouncilResult({
        ...judgements, sameRecommendation: 'false',
      })) || ''), true);
    check('normativeImpact is type-checked too',
      /normativeImpact must be a boolean/.test(threw(() => buildCouncilResult({
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

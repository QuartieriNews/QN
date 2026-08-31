/**
 * strategist.js — the GPT side of the Strategic Council (Issue #5).
 *
 * Calls the OpenAI Responses API for the independent strategic view. The role
 * and the protocol live in `prompts/STRATEGIC_COUNCIL_CHATGPT.md` and
 * `docs/strategic-council/README.md`; this file does not restate them.
 *
 * No dependencies: Node's built-in fetch only, so the Council never touches the
 * dependency set the executable checks rely on (Issue #5, implementation req. 1).
 *
 * This module never decides anything and never writes to the repository. It
 * builds a request, sends it, and parses the answer.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.join(__dirname, '..');

/** The strategist is the general reasoning model, never a coding model. */
const DEFAULT_MODEL = 'gpt-5.6-sol';

/** Responses API. A chat/completions or Codex endpoint is a different contract. */
const RESPONSES_ENDPOINT = 'https://api.openai.com/v1/responses';

/**
 * Reasoning effort the Council is allowed to ask for. Strategic questions get
 * `high` at minimum; the two higher tiers are for foundational decisions.
 * Tier mapping is documented in `council/README.md`.
 */
const ALLOWED_EFFORTS = ['high', 'xhigh', 'max'];
const DEFAULT_EFFORT = 'high';

/** The foundational tier is the reason the higher efforts exist. */
const TIER_3_EFFORTS = ['xhigh', 'max'];

/**
 * Deadline for one strategist call, in milliseconds. Generous because the
 * Council reasons at 'high' or above and a foundational question legitimately
 * takes minutes — but finite, because the CLI is interactive and a stalled
 * connection would otherwise block until the runtime gave up, if it ever did.
 */
const REQUEST_TIMEOUT_MS = 10 * 60 * 1000;

/**
 * The first-pass output the role prompt requires, as a *heading* on its own
 * line. Cycle 10: the bare substring let "I cannot provide a STRATEGY_VIEW for
 * this question" through, which is a refusal that mentions the format.
 */
const STRATEGY_VIEW_MARKER = 'STRATEGY_VIEW';
const STRATEGY_VIEW_HEADING = /^\s{0,3}#{1,6}\s*STRATEGY_VIEW\s*$/m;

/**
 * The final position as *declared*, not as mentioned: the role prompt says to
 * return one of the three tokens and then explain, so the declaration is the
 * first thing said. Cycle 10: counting distinct tokens still accepted
 * "I have not reached a final position; MAINTAIN is one option".
 */
const FINAL_POSITION_DECLARED =
  /^[\s>*_#`-]*(MAINTAIN|REVISE|INSUFFICIENT_INFORMATION)\b/;

/** Protocol stages (Issue #5, implementation req. 2). */
const STAGES = {
  FIRST_PASS: 'FIRST_PASS',
  CROSS_REVIEW: 'CROSS_REVIEW',
  FINAL_POSITION: 'FINAL_POSITION',
};

/** The three positions the final stage may take, as the role prompt requires. */
const FINAL_POSITIONS_ALL = /\b(MAINTAIN|REVISE|INSUFFICIENT_INFORMATION)\b/g;

/** Council result classifications. Deliberately not a numeric score. */
const CLASSIFICATIONS = {
  STRONG_CONVERGENCE: 'STRONG_CONVERGENCE',
  WEAK_CONVERGENCE: 'WEAK_CONVERGENCE',
  MEANINGFUL_DISAGREEMENT: 'MEANINGFUL_DISAGREEMENT',
  INSUFFICIENT_INFORMATION: 'INSUFFICIENT_INFORMATION',
};

const ROLE_PROMPT_PATH = path.join(
  REPO_ROOT, 'prompts', 'STRATEGIC_COUNCIL_CHATGPT.md'
);

/** The fixed strategist role prompt is read from the repo, never inlined. */
function readRolePrompt(promptPath = ROLE_PROMPT_PATH) {
  let text;
  try {
    text = fs.readFileSync(promptPath, 'utf8');
  } catch (cause) {
    throw new Error(
      `strategist role prompt not readable at ${promptPath}: ${cause.message}`
    );
  }
  if (text.trim() === '') {
    throw new Error(`strategist role prompt is empty at ${promptPath}`);
  }
  return text;
}

/**
 * DEC-008 names the strategic critic: the general reasoning model
 * `gpt-5.6-sol`. It is pinned, not merely defaulted — running the Council on
 * another model would broaden a DECIDED entry silently, and widening it is an
 * owner decision, not a flag. A coding model gets its own message because that
 * is the mistake the three-layer split exists to prevent.
 */
function assertDecidedModel(model) {
  if (typeof model !== 'string' || model.trim() === '') {
    throw new Error('model must be a non-empty string');
  }
  if (model === DEFAULT_MODEL) {
    return;
  }
  if (/codex/i.test(model)) {
    throw new Error(
      `refusing model '${model}': the strategic critic is the general reasoning ` +
      'model, never a coding model'
    );
  }
  throw new Error(
    `refusing model '${model}': DEC-008 fixes the strategic critic as ` +
    `'${DEFAULT_MODEL}'. Using another model is a new owner decision, not a flag.`
  );
}

function assertAllowedEffort(effort) {
  if (!ALLOWED_EFFORTS.includes(effort)) {
    throw new Error(
      `reasoning effort '${effort}' is not allowed; use one of ` +
      ALLOWED_EFFORTS.join(', ')
    );
  }
}

/** Non-empty string, after trimming. Empty context is legitimate; empty question is not. */
function isPresent(value) {
  return typeof value === 'string' && value.trim() !== '';
}

/**
 * State the tier in the request, so the depth the run claims is one the
 * strategist was actually asked for.
 *
 * Cycle 10: the tier only validated the effort locally, so a tier-3 request was
 * a tier-2 request with more reasoning tokens — the strategist was never asked
 * for the assumptions, failure scenarios and reconsideration triggers the
 * tier-3 synthesis then requires of it.
 */
function renderTier(tier) {
  if (tier === undefined) return '';
  const lines = [`## Escalation tier: ${tier}`, ''];
  if (tier === 1) {
    lines.push(
      'Reversible: low cost, easy to undo. This runs the first pass only —',
      'there is no cross-review or final position after it. Say so plainly if',
      'the evidence does not support an answer; nothing later will ask again.'
    );
  } else if (tier === 2) {
    lines.push(
      'Material: meaningful cost, dependencies, weeks of downstream work.',
      'The full protocol follows — cross-review, then a final position.'
    );
  } else {
    lines.push(
      'Foundational: hard to reverse, or carrying lock-in, editorial policy,',
      'legal exposure or material recurring cost. Beyond the full protocol,',
      'this tier must name explicitly, and separately from the argument:',
      '',
      '- the assumptions the recommendation rests on;',
      '- the failure scenarios that would make it the wrong call;',
      '- the reconsideration triggers that should reopen it later.',
      '',
      'The synthesis requires all three and refuses a tier-3 result without',
      'them, so a recommendation that names none is incomplete, not concise.'
    );
  }
  return lines.join('\n');
}

function renderContext(context) {
  if (!isPresent(context)) {
    return '## Project context\n\n(none supplied)';
  }
  return `## Project context\n\n${context.trim()}`;
}

/**
 * FIRST_PASS body. The independence rule is structural: this builder takes no
 * Claude-view parameter at all, so there is no field through which Claude's
 * first answer could reach the strategist (Issue #5, independence rule).
 */
/**
 * The protocol's own section markers, refused in a first-pass request.
 *
 * This catches the realistic accident — a context file assembled from a
 * conversation that already holds the Operator view — and nothing more. A
 * caller who renames the heading defeats it, so the guarantee is stated
 * accordingly in council/README.md: the tool has no field for the other view
 * and rejects its markers; not pasting it in anyway is Claude's discipline,
 * which CLAUDE.md binds.
 */
const VIEW_MARKERS = /OPERATOR_VIEW|STRATEGY_VIEW/;

function buildFirstPassInput({ question, context }) {
  if (!isPresent(question)) {
    throw new Error('question is required');
  }
  for (const [name, value] of [['question', question], ['context', context]]) {
    if (isPresent(value) && VIEW_MARKERS.test(value)) {
      throw new Error(
        `independence rule: the ${name} of a ${STAGES.FIRST_PASS} request ` +
        'carries a council view marker. Neither view reaches the other before ' +
        'both exist.'
      );
    }
  }
  return [
    `# Stage: ${STAGES.FIRST_PASS}`,
    '',
    'Form your own independent view. You have not been shown any other',
    "council member's answer, and none exists in this request.",
    '',
    '## Question',
    '',
    question.trim(),
    '',
    renderContext(context),
  ].join('\n');
}

function buildCrossReviewInput({ question, context, claudeView, gptFirstPass }) {
  if (!isPresent(question)) {
    throw new Error('question is required');
  }
  if (!isPresent(claudeView)) {
    throw new Error(`${STAGES.CROSS_REVIEW} requires the Claude view`);
  }
  if (!isPresent(gptFirstPass)) {
    throw new Error(`${STAGES.CROSS_REVIEW} requires your own first-pass view`);
  }
  return [
    `# Stage: ${STAGES.CROSS_REVIEW}`,
    '',
    'Both first-pass views now exist and are shown below. Critique the',
    'Operator view on its merits. Do not oppose it to create disagreement.',
    '',
    '## Question',
    '',
    question.trim(),
    '',
    '## Your first-pass STRATEGY_VIEW',
    '',
    gptFirstPass.trim(),
    '',
    '## Claude OPERATOR_VIEW',
    '',
    claudeView.trim(),
    '',
    renderContext(context),
  ].join('\n');
}

function buildFinalPositionInput({ question, context, claudeView, gptFirstPass, exchange }) {
  if (!isPresent(question)) {
    throw new Error('question is required');
  }
  if (!isPresent(claudeView)) {
    throw new Error(`${STAGES.FINAL_POSITION} requires the Claude view`);
  }
  // MAINTAIN and REVISE are both relative to a position the strategist already
  // took. Without the first pass there is nothing to maintain or revise, and
  // the independence rule would be satisfied on paper only.
  if (!isPresent(gptFirstPass)) {
    throw new Error(
      `${STAGES.FINAL_POSITION} requires your own first-pass view: a position ` +
      'cannot be maintained or revised if it was never formed'
    );
  }
  // Only tier 2 and tier 3 reach this stage, and both run cross-review before
  // it. An absent exchange therefore means a skipped step, not a shorter tier.
  if (!isPresent(exchange)) {
    throw new Error(
      `${STAGES.FINAL_POSITION} requires the cross-review exchange: the ` +
      'protocol critiques before it concludes, and tier 1 stops before this stage'
    );
  }
  const parts = [
    `# Stage: ${STAGES.FINAL_POSITION}`,
    '',
    'State MAINTAIN, REVISE or INSUFFICIENT_INFORMATION, then your final',
    'recommendation. Changing position because the argument is better is the',
    'point; changing it to close the gap is not.',
    '',
    '## Question',
    '',
    question.trim(),
  ];
  parts.push('', '## Your first-pass STRATEGY_VIEW', '', gptFirstPass.trim());
  parts.push('', '## Claude OPERATOR_VIEW', '', claudeView.trim());
  parts.push('', '## Cross-review exchange', '', exchange.trim());
  parts.push('', renderContext(context));
  return parts.join('\n');
}

/**
 * Build the Responses API payload for one stage.
 *
 * `claudeView` is rejected outright at FIRST_PASS rather than ignored: a caller
 * that passes it has misunderstood the protocol, and silently dropping it would
 * hide that.
 *
 * The strategist role prompt is a prompt of record and is read from the
 * repository at call time. It is overridable only through `deps`, alongside the
 * other test seams, and never through `options` — a caller reaching for it in
 * the ordinary argument would be running the pinned model under an arbitrary
 * role, which is the one substitution the model pin exists to prevent.
 */
function buildRequest(options = {}, deps = {}) {
  const { rolePrompt } = deps;
  const {
    stage,
    question,
    context = '',
    claudeView,
    gptFirstPass,
    exchange,
    model = DEFAULT_MODEL,
    effort = DEFAULT_EFFORT,
    tier,
  } = options;

  if (Object.prototype.hasOwnProperty.call(options, 'rolePrompt')) {
    throw new Error(
      'rolePrompt is not a request option: the strategist prompt is a prompt ' +
      'of record, read from the repository at call time. Tests inject it ' +
      'through the second argument, alongside the other seams.'
    );
  }
  if (!Object.prototype.hasOwnProperty.call(STAGES, stage)) {
    throw new Error(
      `unknown stage '${stage}'; use one of ${Object.keys(STAGES).join(', ')}`
    );
  }
  assertDecidedModel(model);
  assertAllowedEffort(effort);

  // The tier governs both the depth and the length of the protocol. The CLI
  // requires it; here it stays optional, because a library caller building a
  // request may legitimately not have classified the question yet.
  if (tier !== undefined) {
    if (![1, 2, 3].includes(tier)) {
      throw new Error('tier must be 1, 2 or 3');
    }
    if (tier === 3 && !TIER_3_EFFORTS.includes(effort)) {
      throw new Error(
        `tier 3 requires reasoning effort ${TIER_3_EFFORTS.join(' or ')}, not ` +
        `'${effort}': a foundational question answered at a lower depth is not ` +
        'a tier-3 run'
      );
    }
    // Tier 1 stops after the two first-pass views. A later stage at tier 1 is
    // either a mis-stated tier or a run the tier-1 synthesis will refuse, and
    // both are cheaper to catch before the call than after it.
    if (tier === 1 && stage !== STAGES.FIRST_PASS) {
      throw new Error(
        `tier 1 has no ${stage} stage: it stops after the two first-pass ` +
        'views. Run this stage at tier 2 or 3, or run FIRST_PASS at tier 1'
      );
    }
  }

  let input;
  const tierBlock = renderTier(tier);
  if (stage === STAGES.FIRST_PASS) {
    if (isPresent(claudeView)) {
      throw new Error(
        'independence rule: FIRST_PASS must not carry the Claude view. ' +
        'Both first-pass views are formed before either is shown to the other.'
      );
    }
    input = buildFirstPassInput({ question, context });
  } else if (stage === STAGES.CROSS_REVIEW) {
    input = buildCrossReviewInput({ question, context, claudeView, gptFirstPass });
  } else {
    input = buildFinalPositionInput({
      question, context, claudeView, gptFirstPass, exchange,
    });
  }
  if (tierBlock) {
    input = `${input}\n\n${tierBlock}`;
  }

  return {
    model,
    instructions: rolePrompt === undefined ? readRolePrompt() : rolePrompt,
    input,
    reasoning: { effort },
    // Council material quotes repository content and the owner's own framing.
    // Session records are kept out of version control for that reason; leaving
    // provider-side retention on by default would undo the same care.
    store: false,
  };
}

/**
 * Settle with `work`, or reject as soon as the deadline aborts.
 *
 * `fetch` honours the signal while streaming a body, but a transport need not,
 * and the abort must bound the read either way — otherwise a stalled body is
 * an unbounded call with a timer that has already fired.
 */
function raceDeadline(work, controller) {
  if (controller.signal.aborted) return Promise.reject(new Error('aborted'));
  return Promise.race([
    work,
    new Promise((_, reject) => {
      controller.signal.addEventListener(
        'abort', () => reject(new Error('aborted')), { once: true }
      );
    }),
  ]);
}

/**
 * Pull the answer and the token usage out of a Responses API payload.
 * Usage is returned so cost can be measured later; it is never invented when
 * the API omits it.
 */
/**
 * Best-effort extraction, which never throws.
 *
 * A rejected response was still charged for, so the usage and whatever text
 * arrived must survive the rejection (cycle 11). `parseResponse` decides
 * whether the answer is usable; this only reads what is there.
 */
function salvageResponse(payload) {
  const object = payload !== null && typeof payload === 'object' ? payload : {};
  const chunks = [];
  const output = Array.isArray(object.output) ? object.output : [];
  for (const item of output) {
    if (item === null || typeof item !== 'object') continue;
    // Reasoning items carry no answer text; only message content is the answer.
    if (item.type !== 'message') continue;
    const content = Array.isArray(item.content) ? item.content : [];
    for (const part of content) {
      if (part && part.type === 'output_text' && typeof part.text === 'string') {
        chunks.push(part.text);
      }
    }
  }
  // Some payloads carry the convenience field; fall back to it only if the
  // structured walk found nothing.
  if (chunks.length === 0 && typeof object.output_text === 'string') {
    chunks.push(object.output_text);
  }

  const usage = object.usage && typeof object.usage === 'object' ? object.usage : {};
  const details = usage.output_tokens_details && typeof usage.output_tokens_details === 'object'
    ? usage.output_tokens_details
    : {};

  return {
    text: chunks.join('\n').trim(),
    model: typeof object.model === 'string' ? object.model : null,
    id: typeof object.id === 'string' ? object.id : null,
    status: typeof object.status === 'string' ? object.status : null,
    usage: {
      input_tokens: numberOrNull(usage.input_tokens),
      output_tokens: numberOrNull(usage.output_tokens),
      reasoning_tokens: numberOrNull(details.reasoning_tokens),
      total_tokens: numberOrNull(usage.total_tokens),
    },
  };
}

function parseResponse(payload) {
  if (payload === null || typeof payload !== 'object') {
    throw new Error('response payload is not an object');
  }

  // A truncated answer can still be non-empty, and a fragment that lost its
  // final position would enter cross-review looking like a real view. When the
  // API states a status, only 'completed' is an answer.
  if (typeof payload.status === 'string' && payload.status !== 'completed') {
    const details = payload.incomplete_details
      && typeof payload.incomplete_details === 'object'
      && typeof payload.incomplete_details.reason === 'string'
      ? `: ${payload.incomplete_details.reason}`
      : '';
    throw new Error(`strategist response is '${payload.status}'${details}`);
  }

  const { status, ...salvaged } = salvageResponse(payload);
  if (salvaged.text === '') {
    throw new Error(
      `response carried no output text${payload.status ? ` (status: ${payload.status})` : ''}`
    );
  }
  return salvaged;
}

function numberOrNull(value) {
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

/** Read the key at call time, never at import time, so tests can vary it. */
function readApiKey(env = process.env) {
  const key = env.OPENAI_API_KEY;
  if (!isPresent(key)) {
    throw new Error(
      'OPENAI_API_KEY is not set. Export it in your shell before invoking the ' +
      'Strategic Council; the key is never committed to this repository. ' +
      'See council/README.md.'
    );
  }
  return key.trim();
}

/**
 * Send one stage to the strategist.
 *
 * The key is read before the request is built, so a missing key fails without
 * reaching the network (Issue #5, acceptance test 1).
 */
async function callStrategist(options = {}, deps = {}) {
  const {
    env = process.env,
    fetchImpl = globalThis.fetch,
    endpoint = RESPONSES_ENDPOINT,
    timeoutMs = REQUEST_TIMEOUT_MS,
  } = deps;

  const apiKey = readApiKey(env);
  const body = buildRequest(options, deps);

  if (typeof fetchImpl !== 'function') {
    throw new Error('no fetch implementation available');
  }

  // A stalled connection would otherwise hold the interactive CLI open with no
  // deadline of its own. The deadline covers the body too (cycle 10): a server
  // that sends headers and then stalls the body hangs just as completely, and
  // clearing the timer when fetch resolved left exactly that gap. The timer is
  // cleared once the payload is in hand, on every path.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const deadlineExceeded = () => new Error(
    `strategist request exceeded its ${Math.round(timeoutMs / 1000)}s deadline ` +
    'and was aborted; nothing was returned'
  );
  let payload;
  try {
    let response;
    try {
      response = await fetchImpl(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
    } catch (cause) {
      if (controller.signal.aborted) throw deadlineExceeded();
      throw new Error(`strategist request failed to reach ${endpoint}: ${cause.message}`);
    }

    if (!response.ok) {
      let detail = '';
      try {
        detail = `: ${(await raceDeadline(response.text(), controller)).slice(0, 500)}`;
      } catch (cause) {
        if (controller.signal.aborted) throw deadlineExceeded();
        detail = '';
      }
      throw new Error(`strategist API error ${response.status}${detail}`);
    }

    try {
      payload = await raceDeadline(response.json(), controller);
    } catch (cause) {
      if (controller.signal.aborted) throw deadlineExceeded();
      throw new Error(`strategist response was not JSON: ${cause.message}`);
    }
  } finally {
    clearTimeout(timer);
  }

  // Every rejection below is of an answer the account was already charged for.
  // What arrived rides on the error so the CLI can still log the call, rather
  // than losing the usage along with the answer (cycles 10 and 11).
  const rejected = (message, response) => Object.assign(new Error(message), {
    response: {
      ...response,
      stage: options.stage,
      tier: options.tier === undefined ? null : options.tier,
      effort: body.reasoning.effort,
      valid: false,
    },
  });

  let parsed;
  try {
    parsed = parseResponse(payload);
  } catch (cause) {
    // An incomplete or empty response is still a paid one: salvage never
    // throws, so the usage survives even when there is no answer to keep.
    throw rejected(cause.message, salvageResponse(payload));
  }
  const invalid = (message) => rejected(message, parsed);

  // The role prompt requires the first pass to return a ### STRATEGY_VIEW. A
  // completed refusal is nonempty text, and the later stages only require the
  // first pass to be nonempty — so an unchecked one would be cross-reviewed and
  // concluded upon as though a view had been formed.
  if (options.stage === STAGES.FIRST_PASS && !STRATEGY_VIEW_HEADING.test(parsed.text)) {
    throw invalid(
      `${STAGES.FIRST_PASS} response returned no ### ${STRATEGY_VIEW_MARKER} ` +
      'heading: the role prompt requires one, and text that only mentions the ' +
      'format — a refusal naming it, say — is not a first-pass view'
    );
  }

  // The role prompt requires the final stage to return one of three tokens.
  // Uppercase and word-bounded, so ordinary prose like "I maintain my view"
  // does not count as a position that was never declared.
  if (options.stage === STAGES.FINAL_POSITION) {
    // The declaration is the first thing said, per the role prompt. Anywhere
    // else it is prose: "MAINTAIN is one option" declares nothing, and a
    // response weighing MAINTAIN against REVISE declares nothing either.
    const firstLine = parsed.text.split('\n').find((line) => line.trim() !== '') || '';
    const declaration = firstLine.match(FINAL_POSITION_DECLARED);
    const mentioned = new Set(parsed.text.match(FINAL_POSITIONS_ALL) || []);
    if (!declaration || mentioned.size !== 1) {
      throw invalid(
        `${STAGES.FINAL_POSITION} response must open by declaring exactly one ` +
        'of MAINTAIN, REVISE or INSUFFICIENT_INFORMATION; ' +
        (declaration
          ? `it opened with ${declaration[1]} but also names ` +
            `${[...mentioned].filter((t) => t !== declaration[1]).join(', ')}`
          : `it opens with none (${mentioned.size} mentioned later)`)
      );
    }
  }

  // The tier and effort travel with the answer, so the run's declared depth can
  // be checked later against the depth it was actually asked for (cycle 11).
  return {
    ...parsed,
    stage: options.stage,
    tier: options.tier === undefined ? null : options.tier,
    effort: body.reasoning.effort,
  };
}

/**
 * Deterministic synthesis (Issue #5, implementation req. 2).
 *
 * The judgements are the Council's; the classification of them is mechanical,
 * so the same inputs always yield the same label. No numeric confidence is
 * produced — the evidence does not support that precision.
 */
function classifyCouncil(input = {}) {
  const {
    tier,
    claudePosition,
    gptPosition,
    insufficientInformation,
    sameRecommendation,
    materialDisagreements,
    missingEvidence,
    normativeImpact,
  } = input;

  // The tier decides whether final positions exist at all: tier 1 stops after
  // the two first-pass views, tiers 2 and 3 run the full protocol. Without it
  // an absent position is indistinguishable from a forgotten one, so the tier
  // is required rather than inferred.
  if (![1, 2, 3].includes(tier)) {
    throw new Error('tier must be 1, 2 or 3 — the protocol run decides it, not the caller\'s mood');
  }

  const positions = ['MAINTAIN', 'REVISE', 'INSUFFICIENT_INFORMATION'];
  for (const [name, value] of [['claudePosition', claudePosition], ['gptPosition', gptPosition]]) {
    if (value !== undefined && !positions.includes(value)) {
      throw new Error(`${name} must be one of ${positions.join(', ')}`);
    }
  }

  const given = [claudePosition, gptPosition].filter((v) => v !== undefined).length;
  if (tier === 1) {
    if (given > 0) {
      throw new Error(
        'tier 1 has no final-position step, so it reports no MAINTAIN/REVISE; ' +
        'a position here means the run was not tier 1'
      );
    }
    // Without positions, tier 1 had no way to say the evidence did not support
    // an answer — it could only converge or disagree. This carries that, and is
    // required so its absence cannot mean "nobody thought to ask".
    if (typeof insufficientInformation !== 'boolean') {
      throw new Error(
        'tier 1 requires insufficientInformation as a boolean: with no final ' +
        'positions it is the only way either first-pass view can report that ' +
        'the evidence does not support an answer, not ' +
        `${insufficientInformation === undefined ? 'omitted' : typeof insufficientInformation}`
      );
    }
  } else if (insufficientInformation !== undefined) {
    throw new Error(
      `tier ${tier} carries insufficient information in the final positions, ` +
      'so insufficientInformation is not read here; supplying it means the ' +
      'run did not follow the tier it reports'
    );
  } else if (given !== 2) {
    // One position is the dangerous case: it looks like tier 1 and classifies
    // as though the other model never had to conclude.
    throw new Error(
      `tier ${tier} runs the full protocol, so both claudePosition and ` +
      `gptPosition are required; ${given} of 2 supplied`
    );
  }
  // Every field below drives the classification or the owner gate, so none may
  // be defaulted. A default answers the question the Council was asked: an
  // omitted materialDisagreements would read as "they did not disagree", which
  // is a finding, not a blank. An omitted field is an error, as the README says.
  for (const [name, value] of [
    ['materialDisagreements', materialDisagreements], ['missingEvidence', missingEvidence],
  ]) {
    if (!Array.isArray(value)) {
      throw new Error(
        `${name} is required and must be an array (empty means the Council ` +
        `found none), not ${value === undefined ? 'omitted' : typeof value}`
      );
    }
    // Length is what drives the classification, so a content-free entry is not
    // a cosmetic flaw: [null] would report a disagreement that names nothing
    // and reverse the meaning an empty array carries.
    if (!value.every(isPresent)) {
      throw new Error(
        `${name} carries a blank entry: its length decides the classification, ` +
        'so an entry that names nothing would report a finding there is none of'
      );
    }
  }
  // A judgements file may be written by a model, and "false" is a truthy string.
  // Coercing it would flip the owner gate silently, so the type is checked.
  for (const [name, value] of [
    ['sameRecommendation', sameRecommendation], ['normativeImpact', normativeImpact],
  ]) {
    if (typeof value !== 'boolean') {
      throw new Error(
        `${name} is required and must be a boolean, not ` +
        `${value === undefined ? 'omitted' : typeof value}`
      );
    }
  }

  let classification;
  if (insufficientInformation === true
    || claudePosition === 'INSUFFICIENT_INFORMATION'
    || gptPosition === 'INSUFFICIENT_INFORMATION') {
    classification = CLASSIFICATIONS.INSUFFICIENT_INFORMATION;
  } else if (!sameRecommendation || materialDisagreements.length > 0) {
    classification = CLASSIFICATIONS.MEANINGFUL_DISAGREEMENT;
  } else if (missingEvidence.length > 0) {
    classification = CLASSIFICATIONS.WEAK_CONVERGENCE;
  } else {
    classification = CLASSIFICATIONS.STRONG_CONVERGENCE;
  }

  // Agreement is evidence, never authority: convergence alone does not clear a
  // question that commits the project to something normative. Tier 3 is the
  // foundational tier by definition — hard to reverse, or carrying lock-in,
  // editorial policy, legal exposure or recurring cost — so it always reaches
  // the owner. Leaving that to a model-authored boolean would let the Council
  // clear its own most consequential questions.
  const ownerDecisionRequired = tier === 3
    || classification !== CLASSIFICATIONS.STRONG_CONVERGENCE
    || normativeImpact;

  return {
    classification,
    owner_decision_required: ownerDecisionRequired ? 'YES' : 'NO',
    material_disagreements: [...materialDisagreements],
    missing_evidence: [...missingEvidence],
  };
}

/**
 * Assemble the council result the owner sees (Issue #5, implementation req. 2).
 *
 * classifyCouncil answers "what kind of result is this"; this answers "what does
 * the owner read". Every field is supplied by the Council — nothing here is
 * inferred, and no numeric confidence is produced.
 */
/**
 * Check that the stages actually run match the tier the synthesis declares.
 *
 * Cycle 11: the tier reached the request but nothing carried it back, so three
 * stages run at tier 2 and a judgements file declaring tier 3 agreed with each
 * other by assertion only. Each stage record states the tier and effort it ran
 * (the CLI writes them with --save), and this refuses a mismatch rather than
 * reporting a depth the run did not have.
 */
function assertStagesMatchTier(tier, stages) {
  if (!Array.isArray(stages) || stages.length === 0) {
    throw new Error(
      'stages is required in a council result: an array of the stage runs ' +
      '({ stage, tier, effort }), so the tier reported here is the tier the ' +
      'strategist was actually asked for rather than an assertion about it'
    );
  }
  const expected = tier === 1
    ? [STAGES.FIRST_PASS]
    : [STAGES.FIRST_PASS, STAGES.CROSS_REVIEW, STAGES.FINAL_POSITION];

  for (const entry of stages) {
    if (entry === null || typeof entry !== 'object') {
      throw new Error('each entry of stages must be an object { stage, tier, effort }');
    }
    if (!expected.includes(entry.stage)) {
      throw new Error(
        `stages carries '${entry.stage}', which tier ${tier} does not run ` +
        `(expected ${expected.join(', ')})`
      );
    }
    if (entry.tier !== tier) {
      throw new Error(
        `stages: ${entry.stage} ran at tier ${entry.tier}, but this result ` +
        `reports tier ${tier}. A run is the tier it was asked for.`
      );
    }
    if (tier === 3 && !TIER_3_EFFORTS.includes(entry.effort)) {
      throw new Error(
        `stages: ${entry.stage} ran at effort '${entry.effort}', which is not ` +
        `a tier-3 depth (${TIER_3_EFFORTS.join(' or ')})`
      );
    }
    if (!ALLOWED_EFFORTS.includes(entry.effort)) {
      throw new Error(`stages: ${entry.stage} ran at unknown effort '${entry.effort}'`);
    }
  }

  const ran = new Set(stages.map((entry) => entry.stage));
  const missing = expected.filter((stage) => !ran.has(stage));
  if (missing.length > 0) {
    throw new Error(
      `tier ${tier} runs ${expected.join(', ')}; stages is missing ` +
      `${missing.join(', ')}. A skipped stage is a shorter protocol, not this one.`
    );
  }
}

function buildCouncilResult(input = {}) {
  const {
    tier,
    stages,
    question,
    claudeRecommendation,
    gptRecommendation,
    strongestAgreement,
    costAndReversibility,
    assumptions = [],
    failureScenarios = [],
    reconsiderationTriggers = [],
  } = input;

  const required = {
    question,
    claudeRecommendation,
    gptRecommendation,
    strongestAgreement,
    costAndReversibility,
  };
  for (const [name, value] of Object.entries(required)) {
    if (!isPresent(value)) {
      throw new Error(`${name} is required in a council result`);
    }
  }
  for (const [name, value] of [
    ['assumptions', assumptions],
    ['failureScenarios', failureScenarios],
    ['reconsiderationTriggers', reconsiderationTriggers],
  ]) {
    if (!Array.isArray(value)) {
      throw new Error(`${name} must be an array`);
    }
  }

  const classified = classifyCouncil(input);
  assertStagesMatchTier(tier, stages);

  // Tier 3 is the foundational tier, and the protocol requires it to say what
  // it assumed, how it could fail, and what would justify reopening it. An
  // empty array here would be a contract met on paper only.
  if (tier === 3) {
    for (const [name, value] of [
      ['assumptions', assumptions],
      ['failureScenarios', failureScenarios],
      ['reconsiderationTriggers', reconsiderationTriggers],
    ]) {
      // Length alone is not content: [""] and [null] would satisfy a count
      // while naming nothing, which is the same gap one level down.
      if (value.length === 0 || !value.every(isPresent)) {
        throw new Error(
          `tier 3 requires ${name}: a foundational decision that names none ` +
          'has not been examined as one, and a blank entry names nothing'
        );
      }
    }
  }

  return {
    tier,
    question: question.trim(),
    claude_final_recommendation: claudeRecommendation.trim(),
    gpt_final_recommendation: gptRecommendation.trim(),
    strongest_agreement: strongestAgreement.trim(),
    meaningful_disagreement: classified.material_disagreements,
    assumptions: [...assumptions],
    failure_scenarios: [...failureScenarios],
    reconsideration_triggers: [...reconsiderationTriggers],
    missing_evidence: classified.missing_evidence,
    cost_and_reversibility: costAndReversibility.trim(),
    classification: classified.classification,
    OWNER_DECISION_REQUIRED: classified.owner_decision_required,
  };
}

module.exports = {
  DEFAULT_MODEL,
  DEFAULT_EFFORT,
  ALLOWED_EFFORTS,
  TIER_3_EFFORTS,
  REQUEST_TIMEOUT_MS,
  RESPONSES_ENDPOINT,
  STAGES,
  CLASSIFICATIONS,
  ROLE_PROMPT_PATH,
  readRolePrompt,
  buildRequest,
  parseResponse,
  salvageResponse,
  readApiKey,
  callStrategist,
  classifyCouncil,
  buildCouncilResult,
};

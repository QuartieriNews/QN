'use strict';

/**
 * The deterministic lane gate.
 *
 * Pure: no network, no filesystem, no clock. It takes one snapshot of pull-request
 * state and returns the lane, the readiness and the reasons for both. Every rule it
 * applies is stated in `docs/autonomy/LANE_POLICY.md`; this file implements that
 * policy and never extends it. Where a comment cites a section, the policy owns the
 * rule and this code is the mechanism.
 *
 * The gate is the only positive classifier (DEC-010). A declaration by an agent is
 * checked against what the gate computed and can never replace it.
 */

const POLICY_VERSION = '1';

/** Lanes, in the order LANE_POLICY §2 evaluates them. The first that applies wins. */
const LANE = {
  PROHIBITED: 'PROHIBITED',
  UNCLASSIFIED: 'UNCLASSIFIED',
  RED: 'RED',
  GREEN: 'GREEN',
  AMBER: 'AMBER',
};

/** Readiness is a separate output and never alters the lane (LANE_POLICY §1). */
const READY = 'READY';

/**
 * Protected surfaces — always RED (LANE_POLICY §6). Matched against every path a
 * change touches, old and new, so a rename cannot launder a protected file.
 */
const PROTECTED_SURFACES = [
  '.github/',
  'autonomy/',
  'decisions/',
  'prompts/',
  'gazetteer/',
  'workflows/',
  'code-nodes/',
  'council/',
  'venue-registry/venues.json',
  'docs/autonomy/',
  'docs/REVIEW_QUEUE.md',
  'reviews/REVIEW_MANDATE_CODE.md',
  'AGENTS.md',
  'CLAUDE.md',
  'requirements.txt',
  '.gitignore',
];

/** Files whose modification means the pull request is rewriting its own judge. */
const SELF_REFERENTIAL = [
  'reviews/REVIEW_MANDATE_CODE.md',
  'AGENTS.md',
  'CLAUDE.md',
  'docs/autonomy/LANE_POLICY.md',
  'autonomy/',
  '.github/',
];

/** A merge is atomic with its evidence only under these (LANE_POLICY §9). */
const ATOMIC_MERGE_MODES = ['strict_base', 'merge_queue'];

const DEFAULT_POLICY = Object.freeze({
  // Empty by owner decision (DEC-010). No pull request can be GREEN until a category
  // is approved on evidence, so the gate's safe state is also its shipped state.
  greenAllowlist: [],
});

function fail(message) {
  throw new Error(`lane_gate: ${message}`);
}

/**
 * Normalise for comparison only. Case is folded because a case-only rename must not
 * escape a protected surface on a case-insensitive checkout (LANE_POLICY §6).
 */
function normalise(path) {
  return String(path).replace(/\\/g, '/').replace(/^\.\//, '').toLowerCase();
}

function underSurface(path, surface) {
  const p = normalise(path);
  const s = normalise(surface);
  return s.endsWith('/') ? p.startsWith(s) : p === s;
}

/** Both sides of a rename, and the symlink target when one is declared. */
function pathsOf(file) {
  const paths = [];
  if (file.path !== undefined && file.path !== null) paths.push(file.path);
  if (file.previousPath) paths.push(file.previousPath);
  if (file.symlinkTarget) paths.push(file.symlinkTarget);
  return paths;
}

function touchesAny(files, surfaces) {
  return files.some((f) => pathsOf(f).some((p) => surfaces.some((s) => underSurface(p, s))));
}

/**
 * PROHIBITED (LANE_POLICY §4). Not a lane: owner approval does not clear any of these,
 * so they are tested before anything else and never fall through to a lane.
 */
function evaluateProhibited(snapshot) {
  const reasons = [];

  if (snapshot.secretsDetected === true) {
    reasons.push('a credential or token appears in the diff');
  }
  // An incomplete enumeration presented as complete is the dangerous shape: a diff
  // that is merely known-incomplete is UNCLASSIFIED, not PROHIBITED.
  if (snapshot.filesComplete === true && snapshot.filesTruncated === true) {
    reasons.push('changed-file set is truncated but was reported complete');
  }
  if (snapshot.evaluatorConsumesPullRequestCode === true) {
    reasons.push('evaluation would consume code or workflow definitions the pull request controls');
  }
  // Self-referential: the mandate and policy applied must come from the default
  // branch. Unproven provenance is prohibited rather than RED, because a RED review
  // would itself be conducted under the instructions in question.
  if (touchesAny(snapshot.files || [], SELF_REFERENTIAL) &&
      snapshot.mandateSource !== 'default_branch') {
    reasons.push('pull request changes its own review mandate or policy and provenance is not the default branch');
  }

  return reasons;
}

/**
 * UNCLASSIFIED (LANE_POLICY §5). Classification did not happen. Deliberately not
 * AMBER: AMBER asserts the owner may approve the change, and nothing here justifies
 * asserting anything about a diff that was not fully read.
 */
function evaluateUnclassified(snapshot) {
  const reasons = [];

  if (snapshot.policyVersion !== POLICY_VERSION) {
    reasons.push(`evidence computed under policy version ${snapshot.policyVersion}, current is ${POLICY_VERSION}`);
  }
  if (snapshot.filesComplete !== true) {
    reasons.push('changed-file set is not known to be complete');
  }
  if (!Array.isArray(snapshot.files)) {
    reasons.push('no changed-file set');
  }
  if (!isFullSha(snapshot.headSha)) {
    reasons.push('head commit is not a full 40-character SHA');
  }
  if (!isFullSha(snapshot.baseSha)) {
    reasons.push('base commit is not a full 40-character SHA');
  }
  for (const f of snapshot.files || []) {
    if (f.unreadable === true) {
      reasons.push(`file could not be read: ${f.path}`);
    }
  }

  return reasons;
}

function isFullSha(value) {
  return typeof value === 'string' && /^[0-9a-f]{40}$/i.test(value);
}

/** RED (LANE_POLICY §6), plus any escalation, which is sticky and agent-proof. */
function evaluateRed(snapshot) {
  const reasons = [];
  const files = snapshot.files || [];

  for (const f of files) {
    for (const p of pathsOf(f)) {
      const hit = PROTECTED_SURFACES.find((s) => underSurface(p, s));
      if (hit) reasons.push(`protected surface touched: ${p} (${hit})`);
    }
  }

  // A new top-level path is an unknown surface and fails closed (LANE_POLICY §6).
  for (const f of files) {
    if (f.status === 'added') {
      const top = normalise(f.path).split('/')[0];
      if (top && !snapshot.knownTopLevelPaths?.includes(top)) {
        reasons.push(`new top-level path: ${top}`);
      }
    }
  }

  // An owner decision, once raised, is the owner's to clear (DEC-009).
  if (snapshot.ownerDecisionRequired === true) {
    reasons.push('an OWNER_DECISION_REQUIRED condition is open');
  }

  for (const e of snapshot.escalations || []) {
    if (e.toLane === LANE.RED) reasons.push(`escalated to RED by ${e.by}: ${e.reason}`);
  }

  return reasons;
}

/**
 * GREEN (LANE_POLICY §7). The whole pull request must satisfy exactly one approved
 * category. Absence of a reason to refuse is never GREEN: a category must match.
 */
function evaluateGreen(snapshot, policy) {
  const reasons = [];
  const files = snapshot.files || [];
  const allowlist = policy.greenAllowlist || [];

  if (allowlist.length === 0) {
    return { green: false, reasons: ['GREEN allowlist is empty: no category is approved'] };
  }
  if (snapshot.isFork === true) {
    reasons.push('pull request originates in a fork');
  }
  if (snapshot.baseRef !== snapshot.defaultBranch) {
    reasons.push('pull request does not target the default branch');
  }
  if (snapshot.authorIsAutomationIdentity !== true) {
    reasons.push('author is not the automation identity');
  }
  if (!snapshot.authorization || snapshot.authorization.mutableByThisPullRequest === true) {
    reasons.push('no owner authorisation, or one this pull request could alter');
  }
  for (const f of files) {
    if (f.isSymlink || f.isSubmodule || f.isBinary || f.modeChanged) {
      reasons.push(`file kind fails closed: ${f.path}`);
    }
  }
  if (reasons.length > 0) return { green: false, reasons };

  // Exactly one category must cover every file. Categories never combine
  // (LANE_POLICY §7) unless the combination is itself an approved category.
  const covering = allowlist.filter((c) => files.every((f) => categoryCovers(c, f)) &&
                                           satisfiesInvariants(c, snapshot));
  if (covering.length === 0) {
    return { green: false, reasons: ['no single approved category covers the whole pull request'] };
  }
  if (covering.length > 1) {
    return { green: false, reasons: ['more than one category matches; combinations are not approved'] };
  }
  return { green: true, reasons: [`category: ${covering[0].name}`] };
}

function categoryCovers(category, file) {
  return pathsOf(file).every((p) => (category.paths || []).some((s) => underSurface(p, s)));
}

function satisfiesInvariants(category, snapshot) {
  const files = snapshot.files || [];
  const limits = category.limits || {};
  const added = files.reduce((n, f) => n + (f.additions || 0), 0);
  const removed = files.reduce((n, f) => n + (f.deletions || 0), 0);
  if (limits.maxFiles !== undefined && files.length > limits.maxFiles) return false;
  if (limits.maxAdditions !== undefined && added > limits.maxAdditions) return false;
  if (limits.maxDeletions !== undefined && removed > limits.maxDeletions) return false;
  return true;
}

/**
 * Readiness (LANE_POLICY §1, §9). Transient evidence state. A failure here blocks and
 * is retried; it never moves the lane.
 */
function computeReadiness(snapshot) {
  const blockers = [];

  if (snapshot.mergeable !== true) blockers.push('BLOCKED_MERGE_CONFLICT');
  if (snapshot.baseIsCurrent !== true) blockers.push('BLOCKED_STALE_BASE');

  const required = snapshot.requiredChecks || [];
  if (required.length === 0) {
    // An empty required set must not pass vacuously (LANE_POLICY §9).
    blockers.push('BLOCKED_TESTS');
  } else {
    for (const name of required) {
      const run = (snapshot.checkRuns || []).find(
        (c) => c.name === name && sameSha(c.headSha, snapshot.headSha) && c.trustedProducer === true
      );
      if (!run || run.conclusion !== 'success') blockers.push(`BLOCKED_TESTS:${name}`);
    }
  }

  const review = snapshot.review || {};
  if (review.cleanForHead !== true) blockers.push('BLOCKED_REVIEW');
  else if (!sameSha(review.reviewedSha, snapshot.headSha)) blockers.push('BLOCKED_STALE_REVIEW');
  else if (review.laterThanLatestRequest !== true) blockers.push('BLOCKED_REVIEW');
  if (review.blockingFindingsOnHead > 0) blockers.push('BLOCKED_REVIEW');

  return blockers.length === 0 ? READY : blockers.join(',');
}

function sameSha(a, b) {
  return isFullSha(a) && isFullSha(b) && a.toLowerCase() === b.toLowerCase();
}

/**
 * Classify one pull request.
 *
 * Returns the lane, the readiness, the reasons, and whether a real auto-merge is
 * permitted. The last is a conjunction and defaults to false: no single condition
 * grants it (DEC-010, LANE_POLICY §9).
 */
function classify(snapshot, policy = DEFAULT_POLICY) {
  if (!snapshot || typeof snapshot !== 'object') fail('snapshot is required');

  const prohibited = evaluateProhibited(snapshot);
  if (prohibited.length > 0) {
    return result(LANE.PROHIBITED, 'BLOCKED_PROHIBITED', prohibited, snapshot, false);
  }

  const unclassified = evaluateUnclassified(snapshot);
  if (unclassified.length > 0) {
    return result(LANE.UNCLASSIFIED, 'BLOCKED_UNCLASSIFIED', unclassified, snapshot, false);
  }

  const readiness = computeReadiness(snapshot);

  const red = evaluateRed(snapshot);
  if (red.length > 0) return result(LANE.RED, readiness, red, snapshot, false);

  const green = evaluateGreen(snapshot, policy);
  if (!green.green) return result(LANE.AMBER, readiness, green.reasons, snapshot, false);

  // Every condition below must hold. The kill switch is read first and fails closed;
  // atomicity is required because a merge that is not atomic with its evidence merges
  // a state nothing reviewed (LANE_POLICY §9, §11).
  const autoMerge =
    readiness === READY &&
    snapshot.killSwitch?.readable === true &&
    snapshot.killSwitch?.autoMergeDisabled === false &&
    ATOMIC_MERGE_MODES.includes(snapshot.mergeAtomicity) &&
    declarationAgrees(snapshot, LANE.GREEN);

  const reasons = green.reasons.slice();
  if (!autoMerge) reasons.push('GREEN computed but auto-merge withheld');
  return result(LANE.GREEN, readiness, reasons, snapshot, autoMerge);
}

/**
 * A declaration never grants a lane; disagreeing with the computed one blocks and is
 * recorded (LANE_POLICY §3). A missing declaration is not agreement.
 */
function declarationAgrees(snapshot, computedLane) {
  const d = snapshot.declaration;
  if (!d) return false;
  return d.lane === computedLane && sameSha(d.headSha, snapshot.headSha);
}

function result(lane, readiness, reasons, snapshot, autoMergeAllowed) {
  const mismatch = snapshot.declaration &&
    snapshot.declaration.lane !== lane &&
    lane !== LANE.PROHIBITED &&
    lane !== LANE.UNCLASSIFIED;
  return {
    policyVersion: POLICY_VERSION,
    lane,
    readiness,
    reasons: mismatch
      ? reasons.concat([`declaration mismatch: declared ${snapshot.declaration.lane}, computed ${lane}`])
      : reasons,
    declarationMismatch: Boolean(mismatch),
    autoMergeAllowed: Boolean(autoMergeAllowed) && !mismatch,
    headSha: snapshot.headSha,
    baseSha: snapshot.baseSha,
  };
}

module.exports = {
  classify,
  computeReadiness,
  LANE,
  READY,
  POLICY_VERSION,
  PROTECTED_SURFACES,
  DEFAULT_POLICY,
};

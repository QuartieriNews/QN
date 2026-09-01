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
 *
 * One shape recurs and is deliberate: a condition is satisfied only by an explicit
 * value, never by the absence of its opposite. `x === true` used to *reject* would let
 * an omitted field pass as though it had been checked, which is the fail-open
 * LANE_POLICY §5 sends to UNCLASSIFIED instead.
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
  '.gitignore',
  // The suites that attest the gate are part of the gate: a change to them alone would
  // otherwise be AMBER and could match a future tests category (LANE_POLICY §6).
  'tests/test_lane_gate.js',
  'tests/test_workflow_safety.js',
];

/**
 * Dependency manifests and lockfiles, matched by file name at any depth. A manifest is
 * a supply-chain surface wherever it sits, so a path prefix would miss the ones that
 * are not at the repository root (LANE_POLICY §6).
 */
const DEPENDENCY_MANIFESTS = [
  'requirements.txt', 'requirements.in', 'constraints.txt', 'setup.py', 'setup.cfg',
  'pyproject.toml', 'pipfile', 'pipfile.lock', 'poetry.lock',
  'package.json', 'package-lock.json', 'npm-shrinkwrap.json', 'yarn.lock',
  'pnpm-lock.yaml', 'bun.lockb',
  'gemfile', 'gemfile.lock', 'go.mod', 'go.sum', 'cargo.toml', 'cargo.lock',
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

/**
 * The shipped policy. Empty by owner decision (DEC-010): no category is approved, so
 * `classify` cannot return an auto-mergeable result for any input. Frozen, because the
 * safe state must not be editable by a caller holding a reference to it.
 */
const SHIPPED_POLICY = Object.freeze({
  version: POLICY_VERSION,
  greenAllowlist: Object.freeze([]),
});

function fail(message) {
  throw new Error(`lane_gate: ${message}`);
}

function isNonEmptyString(v) {
  return typeof v === 'string' && v.trim() !== '';
}

function isFullSha(value) {
  return typeof value === 'string' && /^[0-9a-f]{40}$/i.test(value);
}

function sameSha(a, b) {
  return isFullSha(a) && isFullSha(b) && a.toLowerCase() === b.toLowerCase();
}

/**
 * Normalise for comparison only. Case is folded because a case-only rename must not
 * escape a protected surface on a case-insensitive checkout (LANE_POLICY §6).
 */
function normalise(path) {
  return String(path).replace(/\\/g, '/').replace(/^\.\//, '').toLowerCase();
}

function basename(path) {
  const p = normalise(path);
  return p.slice(p.lastIndexOf('/') + 1);
}

/**
 * Resolve a symlink target the way Git stores it: relative to the directory holding the
 * link, not to the repository root. `docs/notes/link -> ../../prompts/EDITORIAL_FILTER.md`
 * is a change to `prompts/`, and comparing the raw target string would have classified
 * it AMBER (LANE_POLICY §6 — "the resolved target of any symlink").
 *
 * Returns null when the target cannot be resolved inside the repository, which the
 * caller treats as unresolvable rather than safe.
 */
function resolveSymlinkTarget(linkPath, target) {
  if (!isNonEmptyString(target)) return null;
  const t = String(target).replace(/\\/g, '/');
  const segments = t.startsWith('/')
    ? t.slice(1).split('/')
    : normalise(linkPath).split('/').slice(0, -1).concat(t.split('/'));

  const out = [];
  for (const seg of segments) {
    if (seg === '' || seg === '.') continue;
    if (seg === '..') {
      // Escaping above the repository root is not a path this gate can reason about.
      if (out.length === 0) return null;
      out.pop();
      continue;
    }
    out.push(seg);
  }
  // Normalised on the way out, so a resolved target is directly comparable with the
  // surfaces and with the other paths of the same change.
  return out.length > 0 ? normalise(out.join('/')) : null;
}

/** Every repository path a change touches: both sides of a rename, plus link targets. */
function pathsOf(file) {
  const paths = [];
  if (isNonEmptyString(file.path)) paths.push(file.path);
  if (isNonEmptyString(file.previousPath)) paths.push(file.previousPath);
  if (file.symlinkTarget !== undefined) {
    const resolved = resolveSymlinkTarget(file.path, file.symlinkTarget);
    if (resolved) paths.push(resolved);
  }
  return paths;
}

function underSurface(path, surface) {
  const p = normalise(path);
  const s = normalise(surface);
  return s.endsWith('/') ? p.startsWith(s) : p === s;
}

function isProtectedPath(path) {
  if (PROTECTED_SURFACES.some((s) => underSurface(path, s))) return true;
  return DEPENDENCY_MANIFESTS.includes(basename(path));
}

function touchesAny(files, surfaces) {
  return files.some((f) => pathsOf(f).some((p) => surfaces.some((s) => underSurface(p, s))));
}

/**
 * A symlink whose target cannot be resolved is not evidence of anything: it might point
 * into a protected surface. Reported separately so it fails closed rather than passing
 * as a link to nowhere.
 */
function hasUnresolvableSymlink(files) {
  return files.some((f) => f.symlinkTarget !== undefined &&
                           resolveSymlinkTarget(f.path, f.symlinkTarget) === null);
}

/**
 * PROHIBITED (LANE_POLICY §4). Not a lane: owner approval does not clear any of these,
 * so they are tested before anything else and never fall through to a lane.
 */
function evaluateProhibited(snapshot) {
  const reasons = [];
  const files = Array.isArray(snapshot.files) ? snapshot.files : [];

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
  if (touchesAny(files, SELF_REFERENTIAL) && snapshot.mandateSource !== 'default_branch') {
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
  if (!isFullSha(snapshot.headSha)) reasons.push('head commit is not a full 40-character SHA');
  if (!isFullSha(snapshot.baseSha)) reasons.push('base commit is not a full 40-character SHA');

  // Each of these must be stated, not merely not-stated-otherwise. An omitted field is
  // a collector that did not run, which is different from one that found nothing.
  if (snapshot.filesComplete !== true) reasons.push('changed-file set is not known to be complete');
  if (snapshot.filesTruncated !== false) reasons.push('no evidence that changed-file enumeration was untruncated');
  if (snapshot.secretsDetected !== false) reasons.push('no evidence that the diff was scanned for credentials');
  if (snapshot.evaluatorConsumesPullRequestCode !== false) {
    reasons.push('no evidence that evaluation avoids pull-request-controlled code');
  }
  if (typeof snapshot.isFork !== 'boolean') reasons.push('fork provenance is not stated');

  if (!Array.isArray(snapshot.files)) {
    reasons.push('no changed-file set');
  } else if (snapshot.files.length === 0) {
    reasons.push('changed-file set is empty');
  } else {
    for (const f of snapshot.files) {
      if (f.unreadable === true) reasons.push(`file could not be read: ${f.path}`);
      if (!isNonEmptyString(f.path)) reasons.push('a changed file has no repository path');
      if (f.status === 'renamed' && !isNonEmptyString(f.previousPath)) {
        reasons.push(`a rename states no previous path: ${f.path}`);
      }
    }
    if (hasUnresolvableSymlink(snapshot.files)) {
      reasons.push('a symlink target cannot be resolved inside the repository');
    }
  }

  return reasons;
}

/** RED (LANE_POLICY §6), plus any escalation to RED, which is sticky and agent-proof. */
function evaluateRed(snapshot) {
  const reasons = [];
  const files = snapshot.files || [];

  for (const f of files) {
    for (const p of pathsOf(f)) {
      if (isProtectedPath(p)) reasons.push(`protected surface touched: ${p}`);
    }
  }

  // A new top-level path is an unknown surface and fails closed (LANE_POLICY §6).
  for (const f of files) {
    if (f.status === 'added') {
      const top = normalise(f.path).split('/')[0];
      if (top && !(snapshot.knownTopLevelPaths || []).includes(top)) {
        reasons.push(`new top-level path: ${top}`);
      }
    }
  }

  // An owner decision, once raised, is the owner's to clear (DEC-009).
  if (snapshot.ownerDecisionRequired !== false) {
    reasons.push('an OWNER_DECISION_REQUIRED condition is open or unreported');
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

  // An escalation to any less autonomous lane suppresses GREEN. Only RED escalations
  // were honoured before, so an escalation to AMBER was silently discarded
  // (LANE_POLICY §3).
  for (const e of snapshot.escalations || []) {
    if (e.toLane === LANE.AMBER) reasons.push(`escalated to AMBER by ${e.by}: ${e.reason}`);
  }

  if (snapshot.isFork !== false) reasons.push('pull request does not state same-repository provenance');
  if (snapshot.baseRef !== snapshot.defaultBranch) reasons.push('pull request does not target the default branch');
  if (snapshot.authorIsAutomationIdentity !== true) reasons.push('author is not the automation identity');

  // Positive evidence of an owner authorisation, not merely the absence of a flag
  // saying this pull request could rewrite it (LANE_POLICY §7).
  const auth = snapshot.authorization;
  if (!auth || !isNonEmptyString(auth.taskId) ||
      auth.ownerAuthorised !== true || auth.mutableByThisPullRequest !== false) {
    reasons.push('no owner authorisation naming one task and proven immutable by this pull request');
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
  const paths = pathsOf(file);
  // A file contributing no path cannot be covered: `every` over nothing is vacuously
  // true, which would have made a pathless entry match any category.
  if (paths.length === 0) return false;
  return paths.every((p) => (category.paths || []).some((s) => underSurface(p, s)));
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
 * The conclusion of one required check on this head.
 *
 * A name is not unique: GitHub emits a check run per triggering event and per re-run,
 * so a single name can carry several runs on one commit — a skipped duplicate beside a
 * successful one, or an old failure beside a new success. Picking one of them
 * arbitrarily would let the gate read a run that executed nothing as evidence that the
 * suite passed, which is the fail-open LANE_POLICY §9 forbids.
 *
 * The latest completed run decides, matching how GitHub resolves a required check.
 * When that cannot be established — no run, an unparseable or missing timestamp, or a
 * tie between runs that disagree — there is no verdict and the caller blocks.
 */
function latestCheckVerdict(snapshot, name) {
  const runs = (snapshot.checkRuns || []).filter(
    (c) => c.name === name && sameSha(c.headSha, snapshot.headSha) && c.trustedProducer === true
  );
  if (runs.length === 0) return null;
  if (runs.length === 1) return runs[0].conclusion;

  const timed = runs.map((c) => ({ run: c, at: Date.parse(c.completedAt) }));
  if (timed.some((t) => Number.isNaN(t.at))) return null;

  const newest = Math.max(...timed.map((t) => t.at));
  const winners = timed.filter((t) => t.at === newest);
  // A tie between runs that agree is not ambiguous; one between runs that disagree is.
  const conclusions = new Set(winners.map((t) => t.run.conclusion));
  return conclusions.size === 1 ? winners[0].run.conclusion : null;
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
      if (latestCheckVerdict(snapshot, name) !== 'success') blockers.push(`BLOCKED_TESTS:${name}`);
    }
  }

  const review = snapshot.review || {};
  const findings = review.blockingFindingsOnHead;
  if (!Number.isInteger(findings) || findings < 0) {
    // Codex evidence that is missing, ambiguous or unreadable blocks GREEN (DEC-010
    // rule 2). `undefined > 0` is false, so an omitted count used to read as clean.
    blockers.push('BLOCKED_REVIEW');
  } else if (findings > 0) {
    blockers.push('BLOCKED_REVIEW');
  }
  if (review.cleanForHead !== true) blockers.push('BLOCKED_REVIEW');
  else if (!sameSha(review.reviewedSha, snapshot.headSha)) blockers.push('BLOCKED_STALE_REVIEW');
  else if (review.laterThanLatestRequest !== true) blockers.push('BLOCKED_REVIEW');

  return blockers.length === 0 ? READY : blockers.join(',');
}

/**
 * A declaration never grants a lane; disagreeing with the computed one blocks and is
 * recorded (LANE_POLICY §3). A missing declaration is not agreement, and a declaration
 * without its reason is not a declaration — the reason is the audit trail DEC-010
 * rule 1 requires, not optional prose.
 */
function declarationAgrees(snapshot, computedLane) {
  const d = snapshot.declaration;
  if (!d) return false;
  return d.lane === computedLane &&
         sameSha(d.headSha, snapshot.headSha) &&
         isNonEmptyString(d.reason);
}

function result(lane, readiness, reasons, snapshot, autoMergeAllowed, policySource) {
  const mismatch = Boolean(snapshot.declaration) &&
    snapshot.declaration.lane !== lane &&
    lane !== LANE.PROHIBITED &&
    lane !== LANE.UNCLASSIFIED;
  return {
    policyVersion: POLICY_VERSION,
    policySource,
    lane,
    readiness,
    reasons: mismatch
      ? reasons.concat([`declaration mismatch: declared ${snapshot.declaration.lane}, computed ${lane}`])
      : reasons,
    declarationMismatch: mismatch,
    autoMergeAllowed: Boolean(autoMergeAllowed) && !mismatch,
    headSha: snapshot.headSha,
    baseSha: snapshot.baseSha,
  };
}

function evaluate(snapshot, policy, policySource) {
  if (!snapshot || typeof snapshot !== 'object') fail('snapshot is required');

  const prohibited = evaluateProhibited(snapshot);
  if (prohibited.length > 0) {
    return result(LANE.PROHIBITED, 'BLOCKED_PROHIBITED', prohibited, snapshot, false, policySource);
  }

  const unclassified = evaluateUnclassified(snapshot);
  if (unclassified.length > 0) {
    return result(LANE.UNCLASSIFIED, 'BLOCKED_UNCLASSIFIED', unclassified, snapshot, false, policySource);
  }

  const readiness = computeReadiness(snapshot);

  const red = evaluateRed(snapshot);
  if (red.length > 0) return result(LANE.RED, readiness, red, snapshot, false, policySource);

  const green = evaluateGreen(snapshot, policy);
  if (!green.green) return result(LANE.AMBER, readiness, green.reasons, snapshot, false, policySource);

  // Every condition must hold. The kill switch is read first and fails closed;
  // atomicity is required because a merge that is not atomic with its evidence merges
  // a state nothing reviewed (LANE_POLICY §9, §11).
  const autoMerge =
    readiness === READY &&
    snapshot.killSwitch !== undefined &&
    snapshot.killSwitch.readable === true &&
    snapshot.killSwitch.autoMergeDisabled === false &&
    ATOMIC_MERGE_MODES.includes(snapshot.mergeAtomicity) &&
    declarationAgrees(snapshot, LANE.GREEN);

  const reasons = green.reasons.slice();
  if (!autoMerge) reasons.push('GREEN computed but auto-merge withheld');
  return result(LANE.GREEN, readiness, reasons, snapshot, autoMerge, policySource);
}

/**
 * Classify one pull request under the shipped policy.
 *
 * This is the only entry point production uses, and it takes no policy argument: a
 * caller that could supply its own allowlist could grant itself GREEN, which is exactly
 * the promotion DEC-010 forbids any agent from performing. The shipped allowlist is
 * empty and frozen, so this function cannot return `autoMergeAllowed: true` for any
 * input whatsoever.
 */
function classify(snapshot) {
  return evaluate(snapshot, SHIPPED_POLICY, 'shipped');
}

/**
 * The fixture seam, for tests and for replaying a candidate category against history.
 *
 * It exists because a category that has never been evaluated cannot be approved, and
 * every result it produces is stamped `policySource: 'injected'` so an outcome reached
 * under a synthetic allowlist can never be mistaken for one the shipped policy allows.
 * Nothing in production calls it.
 */
function classifyUnderPolicy(snapshot, policy) {
  if (!policy || !Array.isArray(policy.greenAllowlist)) fail('a policy with a greenAllowlist is required');
  return evaluate(snapshot, policy, 'injected');
}

module.exports = {
  classify,
  classifyUnderPolicy,
  computeReadiness,
  resolveSymlinkTarget,
  LANE,
  READY,
  POLICY_VERSION,
  PROTECTED_SURFACES,
  DEPENDENCY_MANIFESTS,
  SHIPPED_POLICY,
};

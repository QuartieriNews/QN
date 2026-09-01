#!/usr/bin/env node
'use strict';

/**
 * Lane advisor — DEC-012.
 *
 * Reports how much owner attention a pull request needs. It never merges, never
 * reads an agent's declared lane, and holds no credentials. Every fact it uses is
 * computed from git rather than supplied by a caller, so a wrong answer here is a
 * wrong reading of the diff and not a false report about one.
 *
 * Two layers: `classify` is pure over a facts object; `readGitFacts` produces that
 * object by running git. The facts object is the forward contract DEC-012 requires,
 * so a later AUTO-GREEN policy can consume it without this file changing.
 */

const { execFileSync } = require('child_process');

const GATE_VERSION = '1.0.0';

const LANE = Object.freeze({ RED: 'RED', AMBER: 'AMBER', GREEN: 'GREEN' });

/** Prefixes whose contents are normative, executable or operational (DEC-012). */
const PROTECTED_SURFACES = Object.freeze([
  '.github/',
  'autonomy/',
  'code-nodes/',
  'council/',
  'decisions/',
  'docs/NEXT_SESSION_BRIEF.md',
  'docs/PROJECT_HANDOVER.md',
  'docs/REVIEW_QUEUE.md',
  'docs/SPEC_V25_WORKPLAN.md',
  'docs/START_HERE.md',
  'docs/WORKFLOW_FIXES.md',
  'docs/autonomy/',
  'docs/strategic-council/',
  'gazetteer/',
  'prompts/',
  'reviews/REVIEW_MANDATE_CODE.md',
  'tests/',
  'venue-registry/',
  'workflows/',
]);

/** Protected wherever they appear, not only at the root. */
const CONTROL_FILENAMES = Object.freeze([
  '.gitignore',
  'agents.md',
  'claude.md',
  'package-lock.json',
  'package.json',
  'requirements.txt',
]);

/** Paths that may be GREEN. Widening this list is RED (DEC-012). */
const GREEN_PREFIXES = Object.freeze(['docs/', 'reviews/']);

const GREEN_LIMITS = Object.freeze({ maxFiles: 10, maxLines: 200 });

/** DEC-012: the capability exists, no category is authorised, nothing can auto-merge. */
const AUTO_GREEN_CATEGORIES = Object.freeze([]);

const SYMLINK_MODE = '120000';
const SUBMODULE_MODE = '160000';
const ABSENT_MODE = '000000';

function fold(path) {
  return String(path).toLowerCase();
}

function basename(path) {
  const parts = String(path).split('/');
  return parts[parts.length - 1];
}

function topSegment(path) {
  return String(path).split('/')[0];
}

/** A path git should never emit; treated as unclassifiable rather than guessed at. */
function isWellFormed(path) {
  if (typeof path !== 'string' || path.length === 0) return false;
  if (path.startsWith('/')) return false;
  return path.split('/').every((seg) => seg.length > 0 && seg !== '.' && seg !== '..');
}

function underProtectedSurface(path) {
  const folded = fold(path);
  for (const surface of PROTECTED_SURFACES) {
    const target = fold(surface);
    if (target.endsWith('/') ? folded.startsWith(target) : folded === target) return surface;
  }
  return null;
}

function isControlFile(path) {
  return CONTROL_FILENAMES.includes(fold(basename(path)));
}

function underGreenPrefix(path) {
  const folded = fold(path);
  return GREEN_PREFIXES.some((prefix) => folded.startsWith(fold(prefix)));
}

function isUnusualKind(file) {
  const modes = [file.srcMode, file.dstMode];
  if (modes.some((m) => m === SYMLINK_MODE || m === SUBMODULE_MODE)) return true;
  // A change of mode on an existing file (the executable bit, most often).
  return (
    file.srcMode !== ABSENT_MODE &&
    file.dstMode !== ABSENT_MODE &&
    file.srcMode !== file.dstMode
  );
}

/** Every path a file touches: a rename is a claim about two of them. */
function pathsOf(file) {
  return file.previousPath ? [file.previousPath, file.path] : [file.path];
}

/**
 * @param {{files: Array, baseTopLevel: string[], isFork: boolean, escalated: boolean}} facts
 * @returns {{gateVersion, lane, reasons, files, newTopLevel, isFork, summary, autoGreen}}
 */
function classify(facts) {
  const files = Array.isArray(facts && facts.files) ? facts.files : null;
  const baseTopLevel = Array.isArray(facts && facts.baseTopLevel) ? facts.baseTopLevel : null;
  const reasons = [];

  // Uncertainty escalates: a fact that is absent is not a fact that is false.
  if (!files || !baseTopLevel) {
    return result(LANE.RED, [{ rule: 'UNCLASSIFIABLE', paths: [], detail: 'facts missing' }], facts, []);
  }

  const malformed = files.flatMap(pathsOf).filter((p) => !isWellFormed(p));
  if (malformed.length > 0) {
    return result(LANE.RED, [{ rule: 'UNCLASSIFIABLE', paths: malformed, detail: 'malformed path' }], facts, []);
  }

  const known = new Set(baseTopLevel);
  const newTopLevel = [
    ...new Set(files.map((f) => topSegment(f.path)).filter((seg) => !known.has(seg))),
  ].sort();

  const protectedHits = [];
  const controlHits = [];
  const unusualHits = [];
  for (const file of files) {
    for (const path of pathsOf(file)) {
      if (underProtectedSurface(path)) protectedHits.push(path);
      if (isControlFile(path)) controlHits.push(path);
    }
    if (isUnusualKind(file)) unusualHits.push(file.path);
  }

  if (protectedHits.length) reasons.push({ rule: 'PROTECTED_SURFACE', paths: unique(protectedHits) });
  if (controlHits.length) reasons.push({ rule: 'CONTROL_FILE', paths: unique(controlHits) });
  if (newTopLevel.length) reasons.push({ rule: 'NEW_TOP_LEVEL', paths: newTopLevel });
  if (unusualHits.length) reasons.push({ rule: 'UNUSUAL_FILE_KIND', paths: unique(unusualHits) });
  if (facts.isFork) reasons.push({ rule: 'FORK', paths: [] });
  if (facts.escalated) reasons.push({ rule: 'ESCALATED', paths: [] });

  if (reasons.length > 0) return result(LANE.RED, reasons, facts, newTopLevel);

  const green = greenReasons(files);
  if (green.length === 0) return result(LANE.GREEN, [], facts, newTopLevel);
  return result(LANE.AMBER, green, facts, newTopLevel);
}

/** Why a change that is not RED is nonetheless not GREEN. */
function greenReasons(files) {
  const reasons = [];
  const outside = files.flatMap(pathsOf).filter((p) => !underGreenPrefix(p));
  if (outside.length) reasons.push({ rule: 'OUTSIDE_GREEN_PREFIXES', paths: unique(outside) });

  const moved = files.filter((f) => f.status !== 'A' && f.status !== 'M').map((f) => f.path);
  if (moved.length) reasons.push({ rule: 'STATUS_NOT_ADD_OR_MODIFY', paths: unique(moved) });

  const binary = files.filter((f) => f.binary).map((f) => f.path);
  if (binary.length) reasons.push({ rule: 'BINARY', paths: unique(binary) });

  if (files.length > GREEN_LIMITS.maxFiles) {
    reasons.push({ rule: 'TOO_MANY_FILES', paths: [], detail: `${files.length} > ${GREEN_LIMITS.maxFiles}` });
  }
  const lines = totalLines(files);
  if (lines > GREEN_LIMITS.maxLines) {
    reasons.push({ rule: 'TOO_MANY_LINES', paths: [], detail: `${lines} > ${GREEN_LIMITS.maxLines}` });
  }
  return reasons;
}

function totalLines(files) {
  return files.reduce((sum, f) => sum + (f.additions || 0) + (f.deletions || 0), 0);
}

function unique(list) {
  return [...new Set(list)].sort();
}

function result(lane, reasons, facts, newTopLevel) {
  const files = Array.isArray(facts && facts.files) ? facts.files : [];
  return {
    gateVersion: GATE_VERSION,
    lane,
    reasons,
    files,
    newTopLevel,
    isFork: Boolean(facts && facts.isFork),
    escalated: Boolean(facts && facts.escalated),
    summary: {
      files: files.length,
      additions: files.reduce((s, f) => s + (f.additions || 0), 0),
      deletions: files.reduce((s, f) => s + (f.deletions || 0), 0),
    },
    // DEC-012: declared so consumers see the capability exists and is off.
    autoGreen: { enabled: AUTO_GREEN_CATEGORIES.length > 0, categories: AUTO_GREEN_CATEGORIES },
  };
}

/* ------------------------------------------------------------------ git layer */

/** `git diff --raw -z`: :srcMode dstMode srcSha dstSha STATUS \0 path [\0 newPath]. */
function parseRawZ(text) {
  const fields = text.split('\0');
  const out = [];
  let i = 0;
  while (i < fields.length) {
    const head = fields[i];
    if (!head) { i += 1; continue; }
    if (head[0] !== ':') throw new Error(`unexpected --raw record: ${head}`);
    const parts = head.slice(1).split(' ');
    if (parts.length < 5) throw new Error(`unexpected --raw record: ${head}`);
    const [srcMode, dstMode, , , statusField] = parts;
    const status = statusField[0];
    const renamed = status === 'R' || status === 'C';
    const previousPath = fields[i + 1];
    const path = renamed ? fields[i + 2] : previousPath;
    out.push({
      status,
      path,
      previousPath: renamed ? previousPath : null,
      srcMode,
      dstMode,
    });
    i += renamed ? 3 : 2;
  }
  return out;
}

/** `git diff --numstat -z`: adds \t dels \0 path [\0 newPath]. `-` means binary. */
function parseNumstatZ(text) {
  const fields = text.split('\0');
  const out = [];
  let i = 0;
  while (i < fields.length) {
    const head = fields[i];
    if (!head) { i += 1; continue; }
    const [adds, dels, inlinePath] = head.split('\t');
    const binary = adds === '-' || dels === '-';
    let path = inlinePath;
    let step = 1;
    if (path === '' || path === undefined) {
      // Rename form: the two paths follow as separate NUL-terminated fields.
      path = fields[i + 2];
      step = 3;
    }
    out.push({
      path,
      binary,
      additions: binary ? 0 : Number(adds),
      deletions: binary ? 0 : Number(dels),
    });
    i += step;
  }
  return out;
}

function mergeFacts(raw, numstat) {
  const byPath = new Map(numstat.map((n) => [n.path, n]));
  return raw.map((file) => {
    const counts = byPath.get(file.path);
    if (!counts) throw new Error(`no numstat record for ${file.path}`);
    return {
      status: file.status,
      path: file.path,
      previousPath: file.previousPath,
      srcMode: file.srcMode,
      dstMode: file.dstMode,
      additions: counts.additions,
      deletions: counts.deletions,
      binary: counts.binary,
    };
  });
}

function git(args) {
  return execFileSync('git', args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
}

function readGitFacts(base, head, options) {
  const opts = options || {};
  const range = `${base}...${head}`;
  return {
    files: mergeFacts(parseRawZ(git(['diff', '--raw', '-z', range])),
                      parseNumstatZ(git(['diff', '--numstat', '-z', range]))),
    baseTopLevel: git(['ls-tree', '--name-only', base]).split('\n').filter(Boolean),
    isFork: Boolean(opts.isFork),
    escalated: Boolean(opts.escalated),
  };
}

/* ---------------------------------------------------------------------- output */

function renderMarkdown(res) {
  const lines = [`## Lane: ${res.lane}`, ''];
  if (res.reasons.length === 0) {
    lines.push('No rule fired.');
  } else {
    lines.push('| Rule | Paths |', '| --- | --- |');
    for (const r of res.reasons) {
      const detail = r.detail ? ` _(${r.detail})_` : '';
      lines.push(`| \`${r.rule}\`${detail} | ${r.paths.map((p) => `\`${p}\``).join(', ') || '—'} |`);
    }
  }
  lines.push('', `${res.summary.files} files, +${res.summary.additions} −${res.summary.deletions}`, '');
  lines.push('| Status | Path | Modes | +/− |', '| --- | --- | --- | --- |');
  for (const f of res.files) {
    const name = f.previousPath ? `${f.previousPath} → ${f.path}` : f.path;
    const counts = f.binary ? 'binary' : `+${f.additions} −${f.deletions}`;
    lines.push(`| ${f.status} | \`${name}\` | ${f.srcMode}→${f.dstMode} | ${counts} |`);
  }
  lines.push('', 'The owner merges every pull request; the lane is advice, not authority (DEC-012).');
  return lines.join('\n');
}

function main(argv) {
  const args = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args.set(key, next); i += 1; } else { args.set(key, 'true'); }
    }
  }
  const base = args.get('base');
  const head = args.get('head');
  if (!base || !head) {
    process.stderr.write('usage: lane_gate.js --base <sha> --head <sha> [--fork] [--escalated]\n');
    return 2;
  }
  const res = classify(readGitFacts(base, head, {
    isFork: args.get('fork') === 'true',
    escalated: args.get('escalated') === 'true',
  }));
  process.stdout.write(`${JSON.stringify(res, null, 2)}\n`);
  if (process.env.GITHUB_STEP_SUMMARY) {
    require('fs').appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${renderMarkdown(res)}\n`);
  }
  return 0;
}

module.exports = {
  classify,
  readGitFacts,
  parseRawZ,
  parseNumstatZ,
  mergeFacts,
  renderMarkdown,
  GATE_VERSION,
  LANE,
  GREEN_LIMITS,
  PROTECTED_SURFACES,
  CONTROL_FILENAMES,
  GREEN_PREFIXES,
  AUTO_GREEN_CATEGORIES,
};

if (require.main === module) process.exit(main(process.argv.slice(2)));

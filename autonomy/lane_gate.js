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
  // A `.gitattributes` anywhere in the head changes how `git diff` reports the diff
  // that classifies it — `*.md diff` makes a file with NUL bytes count as text, so the
  // binary flag reads false. It configures the tool this gate reads from (cycle 1).
  '.gitattributes',
  '.gitignore',
  'agents.md',
  // GitHub reads CODEOWNERS from the root, `.github/` and `docs/`. Matching the
  // basename at any depth covers all three and anywhere it may be read next.
  'codeowners',
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

/** Every fact a file record must state. An omitted one is never read as a false one. */
const FILE_FACT_SCHEMA = Object.freeze({
  status: 'string',
  path: 'string',
  srcMode: 'string',
  dstMode: 'string',
  additions: 'number',
  deletions: 'number',
  binary: 'boolean',
});

/** The statuses that carry a source path, and the only ones that may. */
const RENAME_STATUSES = new Set(['R', 'C']);

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

/** What is missing or mistyped in the facts, named so the reason can say which. */
function factProblems(facts) {
  if (!facts || typeof facts !== 'object') return ['facts missing'];
  const problems = [];
  if (!Array.isArray(facts.files)) problems.push('files');
  if (!Array.isArray(facts.baseTopLevel)) problems.push('baseTopLevel');
  // Whether a pull request crosses repositories is a comparison of two identities.
  // `head.repo.fork` says only whether the head repository is itself a fork, which
  // would call every internal branch a fork if this repository were ever forked from
  // another. Either identity absent is unclassifiable, never "not a fork".
  for (const key of ['headRepoId', 'baseRepoId']) {
    if (typeof facts[key] !== 'string' || facts[key].length === 0) problems.push(key);
  }
  if (problems.length > 0) return problems;

  facts.files.forEach((rec, i) => {
    if (!rec || typeof rec !== 'object') { problems.push(`files[${i}]`); return; }
    for (const [field, type] of Object.entries(FILE_FACT_SCHEMA)) {
      // eslint-disable-next-line valid-typeof
      if (typeof rec[field] !== type) problems.push(`files[${i}].${field}`);
    }
    // An `R` or `C` record without its source path is a rename the gate cannot check
    // both ends of: the destination alone would miss a protected source (cycle 2).
    if (RENAME_STATUSES.has(rec.status)) {
      if (typeof rec.previousPath !== 'string' || rec.previousPath.length === 0) {
        problems.push(`files[${i}].previousPath`);
      }
    } else if (rec.previousPath !== null) {
      problems.push(`files[${i}].previousPath`);
    }
    if (!Number.isFinite(rec.additions) || !Number.isFinite(rec.deletions)) {
      problems.push(`files[${i}] counts`);
    }
  });
  return problems;
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

/** True only when both identities are known and differ. */
function crossesRepositories(facts) {
  const head = facts && facts.headRepoId;
  const base = facts && facts.baseRepoId;
  if (typeof head !== 'string' || typeof base !== 'string' || !head || !base) return false;
  return head !== base;
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
 * @param {{files: Array, baseTopLevel: string[], headRepoId: string, baseRepoId: string}} facts
 * @returns {{gateVersion, lane, reasons, files, newTopLevel, isFork, summary, autoGreen}}
 */
function classify(facts) {
  const reasons = [];

  // Uncertainty escalates: a fact that is absent is not a fact that is false. Every
  // field the schema declares must be stated before any rule is applied (cycle 1).
  const problems = factProblems(facts);
  if (problems.length > 0) {
    return result(LANE.RED,
      [{ rule: 'UNCLASSIFIABLE', paths: [], detail: `unstated or mistyped: ${problems.join(', ')}` }],
      facts, []);
  }
  const files = facts.files;
  const baseTopLevel = facts.baseTopLevel;

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
  if (crossesRepositories(facts)) reasons.push({ rule: 'FORK', paths: [] });

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
  // The record that failed validation is reported as it was supplied, but it must not
  // be dereferenced to build the very result that reports it unusable (cycle 1).
  const counted = files.filter((f) => f && typeof f === 'object');
  return {
    gateVersion: GATE_VERSION,
    lane,
    reasons,
    files,
    newTopLevel,
    isFork: crossesRepositories(facts),
    headRepoId: (facts && facts.headRepoId) || null,
    baseRepoId: (facts && facts.baseRepoId) || null,
    summary: {
      files: files.length,
      additions: counted.reduce((s, f) => s + (Number(f.additions) || 0), 0),
      deletions: counted.reduce((s, f) => s + (Number(f.deletions) || 0), 0),
    },
    // DEC-012: declared so consumers see the capability exists and is off.
    autoGreen: { enabled: AUTO_GREEN_CATEGORIES.length > 0, categories: AUTO_GREEN_CATEGORIES },
  };
}

/** A result for a diff that could not be read, keeping what the caller did state. */
function unclassifiable(detail, provenance) {
  const facts = {
    files: null,
    baseTopLevel: null,
    headRepoId: (provenance && provenance.headRepoId) || null,
    baseRepoId: (provenance && provenance.baseRepoId) || null,
  };
  const res = classify(facts);
  const reasons = [{ rule: 'UNCLASSIFIABLE', paths: [], detail }];
  if (crossesRepositories(facts)) reasons.push({ rule: 'FORK', paths: [] });
  res.reasons = reasons;
  return res;
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
    // Split at the first two tabs only: a pathname may itself contain tabs, and `-z`
    // does not quote them, so splitting on every tab truncates the path (cycle 1).
    const firstTab = head.indexOf('\t');
    const secondTab = head.indexOf('\t', firstTab + 1);
    if (firstTab < 0 || secondTab < 0) throw new Error(`unexpected --numstat record: ${head}`);
    const adds = head.slice(0, firstTab);
    const dels = head.slice(firstTab + 1, secondTab);
    const inlinePath = head.slice(secondTab + 1);
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
  const out = execFileSync('git', args, { encoding: 'buffer', maxBuffer: 64 * 1024 * 1024 });
  const text = out.toString('utf8');
  // Bytes that are not valid UTF-8 all decode to the same replacement character, so two
  // different pathnames become one string and their records alias. Refuse (cycle 2).
  if (!Buffer.from(text, 'utf8').equals(out)) {
    throw new Error(`git ${args.join(' ')} produced pathnames that are not valid UTF-8`);
  }
  return text;
}

function readGitFacts(base, head, options) {
  const opts = options || {};
  const range = `${base}...${head}`;
  return {
    files: mergeFacts(parseRawZ(git(['diff', '--raw', '-z', range])),
                      parseNumstatZ(git(['diff', '--numstat', '-z', range]))),
    // `-z`, because without it git C-quotes an unusual name and the inventory holds the
    // quoted text rather than the name it stands for (cycle 2).
    baseTopLevel: git(['ls-tree', '-z', '--name-only', base]).split('\0').filter(Boolean),
    headRepoId: opts.headRepoId,
    baseRepoId: opts.baseRepoId,
  };
}

/* ---------------------------------------------------------------------- output */

/**
 * A pathname may contain a newline, a backtick or a pipe, and the summary is what the
 * owner reads to decide. Unescaped, a filename can close its own code span and write a
 * row of its own — including one naming a different lane (cycle 1).
 */
function displayPath(value) {
  return String(value)
    .replace(/\\/g, '\\\\')
    // Encoded, not backslash-escaped: a backslash is literal text inside a code span, so
    // an escaped backtick still closes the span, and an escaped pipe still ends the cell
    // in some renderers. Anything that could end either is replaced outright (cycle 2).
    .replace(/[`|\u0000-\u001f\u007f]/g,
      (c) => `\\x${c.charCodeAt(0).toString(16).padStart(2, '0')}`);
}

function renderMarkdown(res) {
  const lines = [`## Lane: ${res.lane}`, ''];
  if (res.reasons.length === 0) {
    lines.push('No rule fired.');
  } else {
    lines.push('| Rule | Paths |', '| --- | --- |');
    for (const r of res.reasons) {
      const detail = r.detail ? ` _(${r.detail})_` : '';
      lines.push(`| \`${r.rule}\`${detail} | ${r.paths.map((p) => `\`${displayPath(p)}\``).join(', ') || '—'} |`);
    }
  }
  lines.push('', `${res.summary.files} files, +${res.summary.additions} −${res.summary.deletions}`, '');
  lines.push('| Status | Path | Modes | +/− |', '| --- | --- | --- | --- |');
  for (const f of res.files) {
    const name = f.previousPath
      ? `${displayPath(f.previousPath)} → ${displayPath(f.path)}`
      : displayPath(f.path);
    const counts = f.binary ? 'binary' : `+${f.additions} −${f.deletions}`;
    lines.push(`| ${f.status} | \`${name}\` | ${f.srcMode}→${f.dstMode} | ${counts} |`);
  }
  lines.push('', 'The owner merges every pull request; the lane is advice, not authority (DEC-012).');
  return lines.join('\n');
}

/**
 * Every flag here takes a value. An empty value is a value — reading it as the string
 * "true" turned two absent repository identities into two equal ones, and one absent
 * into a fork. A flag with no value is null, never a truthy string (cycle 1).
 */
function parseArgs(argv) {
  const args = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith('--')) continue;
    const key = argv[i].slice(2);
    const next = argv[i + 1];
    if (next !== undefined && !next.startsWith('--')) {
      args.set(key, next);
      i += 1;
    } else {
      args.set(key, null);
    }
  }
  return args;
}

function main(argv) {
  const args = parseArgs(argv);
  const base = args.get('base');
  const head = args.get('head');
  if (!base || !head) {
    process.stderr.write(
      'usage: lane_gate.js --base <sha> --head <sha> '
      + '--base-repo-id <id> --head-repo-id <id>\n');
    return 2;
  }
  // Reading the facts can fail on a shape git produces and this file does not expect.
  // The policy says that is RED with a reason, not an exception and no result at all.
  const provenance = {
    headRepoId: args.get('head-repo-id'),
    baseRepoId: args.get('base-repo-id'),
  };
  let res;
  try {
    res = classify(readGitFacts(base, head, provenance));
  } catch (error) {
    res = unclassifiable(`could not read the diff: ${error.message}`, provenance);
  }
  process.stdout.write(`${JSON.stringify(res, null, 2)}\n`);
  if (process.env.GITHUB_STEP_SUMMARY) {
    require('fs').appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${renderMarkdown(res)}\n`);
  }
  return 0;
}

module.exports = {
  classify,
  crossesRepositories,
  displayPath,
  factProblems,
  parseArgs,
  unclassifiable,
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

# council/ — the Strategic Council tool

The GPT side of the Strategic Council: one CLI that Claude Code calls to obtain
the independent strategic view. The roles, the protocol and the escalation tiers
are in `docs/strategic-council/README.md`; the role prompts are
`prompts/STRATEGIC_COUNCIL_CLAUDE.md` and `prompts/STRATEGIC_COUNCIL_CHATGPT.md`.
This file covers setup, invocation and what is kept.

The Council advises. It never implements, merges, deploys, or decides. Only the
owner decides (DEC-008).

## One-time setup

The strategist is reached through the OpenAI **Responses API** with an API key
you supply through the environment:

```bash
export OPENAI_API_KEY="sk-..."          # your shell profile, not this repository
```

**The key is never committed.** Nothing in this folder reads a key from a file,
and no key belongs in a commit, a session record, a PR or an issue. Without the
variable set, every call fails before a request is made — deliberately, so a
missing key can never be mistaken for a strategist that had nothing to say.

There is nothing to install: the tool uses Node's built-in `fetch` and no
dependencies, so it stays clear of the Python dependency the executable checks
use (`requirements.txt`).

## How the owner invokes the Council

From one Claude Code conversation. No separate UI, no n8n:

```
Strategic council: should we generalise the geography engine for multiple
cities now, or optimise only for Rome?
```

Claude Code recognises the request, switches to Operator / Product Architect
mode (`CLAUDE.md`), gathers only the relevant context, runs the protocol and
returns one council result.

## Calling the strategist directly

```bash
# Stage 1 — independent views. Accepts no Claude view, by construction.
node council/cli.js --stage FIRST_PASS --tier 2 --question "..." --context-file ctx.md

# Stage 2 — both first-pass views exist; the strategist critiques the Operator.
node council/cli.js --stage CROSS_REVIEW --tier 2 --question "..." \
     --claude-view-file operator.md --gpt-first-pass-file strategy.md

# Stage 3 — maintain, revise, or declare insufficient information. All three
# artefacts are required: the protocol critiques before it concludes.
node council/cli.js --stage FINAL_POSITION --tier 2 --question "..." \
     --claude-view-file operator.md --gpt-first-pass-file strategy.md \
     --exchange-file exchange.md
```

Useful flags:

| Flag | Effect |
|---|---|
| `--tier 1\|2\|3` | **required** on a stage request; tier 3 refuses `high`, tier 1 refuses the later stages |
| `--effort high\|xhigh\|max` | reasoning depth; default `high` |
| `--dry-run` | print the request and stop — no key needed, no call made |
| `--json` | full result including token usage |
| `--save` | write the session record under `council/sessions/` |

`--dry-run` is the cheap way to check what would be sent, including that a
FIRST_PASS request carries no Operator view.

**What the independence rule is, exactly.** A first-pass request has no field
for the other view, passing one throws, and the question and context are
refused if they carry a council view marker (`OPERATOR_VIEW`, `STRATEGY_VIEW`).
That catches the realistic accident — a context assembled from a conversation
that already holds the Operator view. It does **not** defeat a caller who
renames the heading: `context` is free text and no check on it can be complete.
The remaining guarantee is Claude's discipline, which `CLAUDE.md` binds. The
tool closes the accidental path and says plainly that it cannot close the
deliberate one.

A completed `FIRST_PASS` response is checked to carry the `### STRATEGY_VIEW`
heading the role prompt requires — the heading on its own line, not the words
anywhere in the text, so "I cannot provide a STRATEGY_VIEW for this question"
does not pass as one. A refusal or an off-format answer is nonempty text and
would otherwise be accepted, and the later stages only require the first pass to
be nonempty — so it would be cross-reviewed and concluded upon as though a view
had been formed.

A completed `FINAL_POSITION` response must **open by declaring exactly one** of
`MAINTAIN`, `REVISE` or `INSUFFICIENT_INFORMATION`, uppercase and word-bounded.
The role prompt returns the position first and explains afterwards, so the
declaration is the first thing said; anywhere else the token is prose. All three
of these are refused rather than resolved by first-match, because guessing which
token the strategist meant is the error the stage exists to prevent:

- prose that merely uses the word "maintain";
- an answer naming two ("I cannot choose between MAINTAIN and REVISE");
- an answer naming one without taking it ("I have not reached a final position;
  MAINTAIN is one option").

There is no `--model` flag. DEC-008 fixes the strategic critic as `gpt-5.6-sol`,
and the tool refuses any other model: running the Council on a different one
would widen a DECIDED entry, which is an owner decision rather than a flag.

There is no role-prompt flag either, and `rolePrompt` is refused as a request
option. `prompts/STRATEGIC_COUNCIL_CHATGPT.md` is a prompt of record, read from
the repository at call time and sent as the request instructions; substituting
it would run the pinned model under an arbitrary role, which is exactly what
pinning the model exists to prevent. The tests inject a stub through the same
argument that carries the fetch and env seams, so the seam is visible as one.

`FINAL_POSITION` requires the strategist's own first-pass view, the Operator's,
and the cross-review exchange. `MAINTAIN` and `REVISE` are both relative to a
position it already took, and the protocol critiques before it concludes — only
tiers 2 and 3 reach this stage, and both cross-review first.

## Closing the council

The synthesis is deterministic and makes no model call, so it needs no key:

```bash
node council/cli.js --synthesis-file judgements.json
```

`judgements.json` carries what the Council concluded. What the tool adds is the
classification and the `OWNER_DECISION_REQUIRED` gate, computed the same way
every time. Nothing is inferred and no confidence score is produced; a missing
required field is an error rather than a silent gap. The one number in the
result is `tier`, which is a label, not a measure.

| Field | Type | Required |
|---|---|---|
| `tier` | `1`, `2` or `3` | always |
| `question` | string | always |
| `claudeRecommendation`, `gptRecommendation` | string | always |
| `strongestAgreement` | string | always |
| `costAndReversibility` | string | always |
| `sameRecommendation` | boolean | always |
| `materialDisagreements` | array of non-empty strings | always — empty means the Council found none |
| `missingEvidence` | array of non-empty strings | always — empty means the Council found none |
| `normativeImpact` | boolean | always |
| `claudePosition`, `gptPosition` | `MAINTAIN` / `REVISE` / `INSUFFICIENT_INFORMATION` | tiers 2–3 only, both or neither |
| `insufficientInformation` | boolean | tier 1 only — tiers 2–3 say it in the positions |
| `assumptions`, `failureScenarios`, `reconsiderationTriggers` | array of non-empty strings | tier 3 |

Every field that drives the classification or the gate is required outright,
with **no default**. An omitted `materialDisagreements` is not an empty one: a
default would answer the question the Council was asked, and "they found no
material disagreement" is a finding, not a blank. Empty arrays and `false` say
that explicitly, and the error distinguishes an omitted field from a mistyped
one. A blank entry is refused for the same reason from the other side: the
length of these arrays decides the classification, so `[null]` would report a
disagreement that names nothing — the reverse of what an empty array says.

**The tier is required**, because it is what makes the rest enforceable:

- **Tier 1** supplies no `claudePosition`/`gptPosition` — it stops after the two
  first-pass views, so there is no `MAINTAIN` or `REVISE` to report. Supplying
  one is refused: it means the run was not tier 1. It supplies
  `insufficientInformation` instead, and must: without positions to carry it,
  a tier-1 council could otherwise only converge or disagree, never report that
  the evidence did not support an answer. Tiers 2–3 refuse the field, because
  there the positions say it.
- **Tiers 2 and 3** require *both* positions. A single position is the dangerous
  case — it reads like tier 1 and would classify as though the other model never
  had to conclude — so a partial pair is refused.
- **Tier 3** additionally requires non-empty `assumptions`, `failureScenarios`
  and `reconsiderationTriggers`. A foundational decision that names none has not
  been examined as one, and an empty array would meet the contract on paper
  only. A tier-3 result also **always** carries
  `OWNER_DECISION_REQUIRED: YES`, whatever `normativeImpact` says and however
  strongly the two converged: tier 3 is the foundational tier by definition, and
  letting a model-authored boolean clear the gate there would let the Council
  settle its own most consequential questions. The classification is still
  reported honestly — convergence is convergence — the gate simply does not
  follow from it at that tier.

## Choosing the tier

The tiers in `docs/strategic-council/README.md` set how much protocol a question
deserves; here is what each costs to run.

| Tier | When | Protocol | Effort |
|---|---|---|---|
| **1 — Reversible** | low cost, easy to undo, little architectural impact | one independent view each, then synthesis — no final-position step, so the synthesis takes no `MAINTAIN`/`REVISE` value | `high` |
| **2 — Material** | meaningful cost, dependencies, weeks of downstream work | full: first pass, cross-review, final position | `high` |
| **3 — Foundational** | hard to reverse, vendor or platform lock-in, editorial policy, legal exposure, material recurring cost | full protocol, plus explicit assumptions, failure scenarios and reconsideration triggers | `xhigh` or `max` |

Reasoning below `high` is not offered. A question that does not deserve `high`
does not deserve the Council; answer it in Builder mode.

The tier is also stated in the request itself, so the depth a run claims is one
the strategist was actually asked for: a tier-3 request tells it to name the
assumptions, failure scenarios and reconsideration triggers the tier-3 synthesis
will require of it, and a tier-1 request says the run stops after the first pass.
An unclassified request states no tier at all rather than implying one.

`--tier` is **required** on a stage request, so the mapping is enforced rather
than trusted: a tier-3 request refuses effort `high`, because a foundational
question answered at a lower depth and then reported as tier 3 is exactly what
the table exists to prevent. The tier governs the length of the protocol as well
as its depth: `CROSS_REVIEW` and `FINAL_POSITION` are refused at tier 1, which
stops after the two first-pass views — such a call is either a mis-stated tier
or a run the tier-1 synthesis would refuse afterwards, and both are cheaper to
catch before the call than after paying for it. Optional, it could be skipped by omission — the
stages run at the default depth, and the synthesis afterwards reports tier 3
regardless. A question not yet classified is not yet a Council question; classify
it, then run it.

## What is kept, and what is not

| | Where | Committed? |
|---|---|---|
| Session records (`--save`) | `council/sessions/` | **No** — gitignored |
| The question and the council result | the Claude Code conversation | No |
| An owner decision that comes out of a session | `decisions/DEC-NNN-*.md` | Yes |
| Stable strategic context | `docs/strategic-council/PROJECT_BRIEF.md` | Yes |

Conversation is working memory; GitHub is institutional memory. A council
session is not an artefact of record: only an explicit owner decision becomes a
`DEC` entry, drafted in the existing format and decided by the owner.

A record is never overwritten: two saves of the same stage within one
millisecond get distinct filenames rather than the second silently replacing the
first. A record logs a call that was paid for — including one whose answer the
stage validation rejected, which is written with `"valid": false` rather than
lost. The account was charged either way, and a log of successes only is not a
usage log.

A session record is a **response and usage log**, not a resume point: it keeps
the stage, the question, the answer and the token usage, and deliberately not
the context, the Operator view or the cross-review exchange. Resuming an
interrupted council is the Claude Code conversation's job — that is the working
memory — and copying those artefacts onto disk would put more of the owner's
framing there for no gain the MVP needs.

Records may still quote repository content and the question as asked, so they
stay out of version control.

Every request also sends `store: false`, so the provider is asked not to retain
the council material on its side either. Keeping the answer is the session
record's job, and it is gitignored; provider-side retention would put the same
material somewhere neither the owner nor this repository controls.

## When a call stalls

Every request carries a deadline — ten minutes, generous because the Council
reasons at `high` or above and a foundational question legitimately takes
minutes, but finite because the CLI is interactive. The deadline covers reading
the response body as well as opening the connection: a server that sends headers
and then stalls the body hangs just as completely. On expiry the request is
aborted and the error says so; nothing partial is returned. A stalled
connection therefore fails visibly instead of holding the conversation open.

## Cost

Every call returns the token usage the API reports — input, output, reasoning
and total. `--json` prints it; the plain form writes a `[usage]` line to stderr;
`--save` keeps it in the session record. Nothing is estimated or invented: when
the API omits a figure the field is `null` rather than a guess.

Usage is reported per call. **The hard budget lives on the OpenAI account**,
which is the only place a limit can actually be enforced; set it there. This
tool reports and does not enforce — adding a cumulative preflight limit would be
machinery the owner should choose, not a gap closed quietly. The architecture
doc's cost-control list says the same thing, so the two do not disagree.

## What this tool must never do

- commit a key, or read one from anywhere but the environment;
- use a Codex model or endpoint as the strategic critic — that is the Technical
  Council's job, and collapsing the two would defeat DEC-008;
- show the strategist Claude's first-pass view before it has formed its own;
- write to the repository, touch n8n, or change anything in production;
- manufacture a numeric confidence score.

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
| `--tier 1\|2\|3` | **required** on a stage request; tier 3 refuses `high` |
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

A completed `FINAL_POSITION` response is also checked to state **exactly one**
of `MAINTAIN`, `REVISE` or `INSUFFICIENT_INFORMATION`, uppercase and
word-bounded — prose that merely uses the word "maintain" is not a position, and
an answer that names two of them ("I cannot choose between MAINTAIN and REVISE")
has not taken one either. Both cases are refused rather than resolved by
first-match, because guessing which token the strategist meant is the error the
stage exists to prevent.

There is no `--model` flag. DEC-008 fixes the strategic critic as `gpt-5.6-sol`,
and the tool refuses any other model: running the Council on a different one
would widen a DECIDED entry, which is an owner decision rather than a flag.

`FINAL_POSITION` requires the strategist's own first-pass view, the Operator's,
and the cross-review exchange. `MAINTAIN` and `REVISE` are both relative to a
position it already took, and the protocol critiques before it concludes — only
tiers 2 and 3 reach this stage, and both cross-review first.

## Closing the council

The synthesis is deterministic and makes no model call, so it needs no key:

```bash
node council/cli.js --synthesis-file judgements.json
```

`judgements.json` carries what the Council concluded — the `tier` it ran, the
two final recommendations, the strongest agreement, the cost and reversibility
reading, the assumptions, any material disagreement and any missing evidence,
plus `normativeImpact` when the answer would commit the project to something.
What the tool adds is the classification and the `OWNER_DECISION_REQUIRED`
gate, computed the same way every time. Nothing is inferred and no confidence
score is produced; a missing required field is an error rather than a silent
gap. The one number in the result is `tier`, which is a label, not a measure.

**The tier is required**, because it is what makes the rest enforceable:

- **Tier 1** supplies no `claudePosition`/`gptPosition` — it stops after the two
  first-pass views, so there is no `MAINTAIN` or `REVISE` to report. Supplying
  one is refused: it means the run was not tier 1.
- **Tiers 2 and 3** require *both* positions. A single position is the dangerous
  case — it reads like tier 1 and would classify as though the other model never
  had to conclude — so a partial pair is refused.
- **Tier 3** additionally requires non-empty `assumptions`, `failureScenarios`
  and `reconsiderationTriggers`. A foundational decision that names none has not
  been examined as one, and an empty array would meet the contract on paper
  only.

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

`--tier` is **required** on a stage request, so the mapping is enforced rather
than trusted: a tier-3 request refuses effort `high`, because a foundational
question answered at a lower depth and then reported as tier 3 is exactly what
the table exists to prevent. Optional, it could be skipped by omission — the
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

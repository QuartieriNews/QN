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
node council/cli.js --stage FIRST_PASS --question "..." --context-file ctx.md

# Stage 2 — both first-pass views exist; the strategist critiques the Operator.
node council/cli.js --stage CROSS_REVIEW --question "..." \
     --claude-view-file operator.md --gpt-first-pass-file strategy.md

# Stage 3 — maintain, revise, or declare insufficient information. All three
# artefacts are required: the protocol critiques before it concludes.
node council/cli.js --stage FINAL_POSITION --question "..." \
     --claude-view-file operator.md --gpt-first-pass-file strategy.md \
     --exchange-file exchange.md
```

Useful flags:

| Flag | Effect |
|---|---|
| `--effort high\|xhigh\|max` | reasoning depth; default `high` |
| `--dry-run` | print the request and stop — no key needed, no call made |
| `--json` | full result including token usage |
| `--save` | write the session record under `council/sessions/` |

`--dry-run` is the cheap way to check what would be sent, including that a
FIRST_PASS request carries no Operator view.

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

`judgements.json` carries what the Council concluded — the two final
recommendations, the strongest agreement, the cost and reversibility reading,
the assumptions, any material disagreement and any missing evidence, plus
`normativeImpact` when the answer would commit the project to something. What
the tool adds is the classification and the `OWNER_DECISION_REQUIRED` gate,
computed the same way every time. Nothing is inferred and no confidence score
is produced; a missing required field is an error rather than a silent gap.

Tier 1 supplies no `claudePosition`/`gptPosition`: it stops after the two
first-pass views, so there is no `MAINTAIN` or `REVISE` to report.

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

## Cost

Every call returns the token usage the API reports — input, output, reasoning
and total. `--json` prints it; the plain form writes a `[usage]` line to stderr;
`--save` keeps it in the session record. Nothing is estimated or invented: when
the API omits a figure the field is `null` rather than a guess.

Usage is reported per call. Adding it up across a session, and setting a budget,
is the owner's; the tool does not enforce a spend limit.

## What this tool must never do

- commit a key, or read one from anywhere but the environment;
- use a Codex model or endpoint as the strategic critic — that is the Technical
  Council's job, and collapsing the two would defeat DEC-008;
- show the strategist Claude's first-pass view before it has formed its own;
- write to the repository, touch n8n, or change anything in production;
- manufacture a numeric confidence score.

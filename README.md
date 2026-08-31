# QN — Quartieri News

Hyperlocal news platform for Rome: 89 neighbourhood pages covering all 15 municipalities.
This repository is the **source of truth for everything executable or line-versioned** in
the project: the gazetteer build, the prompts, the tests and golden sets, the n8n workflow
exports and the code nodes.

It is **not** the source of truth for decisions and normative documents — those live in
Google Drive, folder **Progetto Quartieri News / QN Hub** (specifications in
`10 Specifications`, release packages in `20 Packages`, review reports in `30 Reviews`,
the decision log in `40 Decisions`). The collaboration model — four roles, who reviews
what, where every artefact lives — is `QN Operating Model — Four Roles` in
`QN Hub / 00 Governance`. When this README and that document disagree, that document wins.

Current baseline: **events package release 1.4.5** (28 August 2026), consolidated into
**specification v2.5** (in Drive, `10 Specifications`). Production is **n8n Cloud**,
shared project *QuartieriNews*; this repository mirrors and certifies what runs there —
pushing here deploys nothing.

This repository is worked by an **AI development loop** (DEC-104): **Claude builds,
ChatGPT reviews** (`reviews/REVIEW_MANDATE_CODE.md`), **the owner decides**
(`decisions/`) and operates the hands-on steps. Staging before production: pipeline
work runs against `staging_`-prefixed Drive folders and Firestore collections until
reviewed and verified. No DECIDED entry in `decisions/` is reopened by either AI.

## Layout

| Folder | Contents | Rule |
|---|---|---|
| `gazetteer/` | The master workbook, `build_gazetteer.py`, and its generated outputs (`gazetteer.json`, prompt list, Italian export, normalized map) | Edit **only** the workbook, then re-run the build. Never hand-edit a generated file. `gazetteer.json` is the contract: when any document disagrees with it, the JSON wins. |
| `venue-registry/` | `venues.json` — contract and seed for the Firestore `venues` collection | Learned at runtime, **never regenerated** by any build. |
| `prompts/` | `PROMPT_GEO_BLOCK.md`, `EDITORIAL_FILTER.md`, `CHANGELOG.md` | Every prompt change gets a changelog entry and bumps the relevant revision integer. Prompt text pasted into n8n must be byte-identical to the file here. |
| `tests/` | `test_guards.py` (37 checks, executably asserted), `zone_distribution.py`, the two golden sets | `test_guards.py` must exit 0 on every change. Golden sets are hand-marked expectations; a disagreement is first evidence the prompt is unclear. Raw samples are **not** committed (DEC-104): they live in the Drive release package; see `tests/samples/README.md`. |
| `workflows/` | n8n workflow JSON exports | One file per workflow. **No structural change in n8n without exporting and opening a PR** — see `workflows/README.md`. |
| `code-nodes/` | The JavaScript/Python of each n8n Code node, one file per node | Each node testable outside n8n. The node in production must match the file here. |
| `council/` | The Strategic Council tool: the CLI Claude Code calls for the independent strategic view | Advises only — never implements, merges, deploys or decides (DEC-008). No dependencies, and the API key lives in the environment, never in the repository. Setup and tiers in `council/README.md`. |
| `reviews/` | Review reports written by the reviewing AI, and its mandate | Where a code review is archived is the Code Review Rules' to state (`AGENTS.md`, pending `decisions/DEC-007`); reports that do live here are named `YYYY-MM-DD—<scope>—<verdict>.md`. The mandate to paste into the reviewer is `reviews/REVIEW_MANDATE_CODE.md`. |
| `docs/` | The narrative documents of the events package (release 1.4.5) | Working copies. The frozen release zip stays in Drive `20 Packages`. `docs/START_HERE.md` is the reading order; the version number lives only there. |
| `decisions/` | The decision log — one file per decision | **A decision exists only if it is written here.** DECIDED entries are never re-asked. Format and rules in `decisions/README.md`. |

## Running the checks

Install the Python dependencies first (`requirements.txt`, in the repository root —
`openpyxl`, needed by the gazetteer build and therefore by `test_guards.py`):

```bash
pip install -r requirements.txt
```

All scripts read paths relative to `gazetteer/`:

```bash
cd gazetteer
python build_gazetteer.py                                    # rebuild after editing the master
python ../tests/test_guards.py                               # 37 checks, must print ALL PASS
python ../tests/zone_distribution.py ../tests/samples/sample_107_direct_urls.json
```

`build_gazetteer.py` fails rather than warns on a broken invariant — a failing build means
the workbook edit is wrong, not that the build needs patching.

The Node suites run from the repository root and need no installation:

```bash
node tests/test_parse_duration.js                            # 58 checks, must print ALL PASS
node tests/test_council.js                                   # 217 checks, must print ALL PASS
```

`test_council.js` is fully offline: it never makes an OpenAI call, so it needs no
`OPENAI_API_KEY` and costs nothing to run.

## Pull request conventions

1. **One change per PR**, named for what it changes (`fix/duration-parser`,
   `prompt/editorial-tours-rule`, `workflow/phase3-geography`).
2. A PR that changes workflow behaviour **must include the re-exported workflow JSON** in
   `workflows/` — the diff of that file is what gets reviewed.
3. A PR that changes a prompt must update `prompts/CHANGELOG.md` and state which revision
   integer it bumps (`generation_revision` or `geo_logic_revision`).
4. Every PR is reviewed against **specification v2.5 and `gazetteer.json`** — never against
   memory. The review must exist before merge; where it is archived is stated by the Code
   Review Rules in `AGENTS.md` (pending `decisions/DEC-007`), not here.
5. Nothing normative is decided in a change. If it needs an owner decision, it points at
   the `decisions/DEC-NNN` entry (drafting it if missing) and waits for it.

## What must never happen here

- A hand edit to any generated file (`gazetteer.json`, `prompt_list_publication_zones.txt`,
  `it_strings.json`, `Mappa_Quartieri_Normalizzata.xlsx`).
- A regeneration of `venue-registry/venues.json` — venues are learned, not built.
- A second copy of a rule. Documents point at `gazetteer.json`; they do not restate it.
- A merge without a review, or a workflow change without its export.

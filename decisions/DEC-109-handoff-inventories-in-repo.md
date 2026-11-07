# DEC-109 — Per-item inventories of the source study kept in the repository

Status: DECIDED (15 October 2026, owner on pull request #15, review lotto 3).

Question: the source study of June 2026 committed nine per-item inventories in
`tools/sources-study/handoff_data/` (one row per item: URL, date, Municipio, zone, type,
duration, counts and the study's own labels) and nine of them carried columns with text taken
from the sources (titles of news items, acts and videos; descriptions with the agenda; in one
case a person's name inside an agenda). DEC-102 and DEC-104 keep per-item source data out of
the public repository and DEC-105 boundary 1 restates it. The Codex review of lotto 3 asked
whether these files could stay.

Options presented to the owner:

1. Move the nine CSVs to Drive and delete them from the repository.
2. Strip the columns that carry source text and keep the inventories (URL, metadata, counts,
   labels) in the repository; the full versions stay in git history.
3. Keep the files as they were and declare the exception.

Owner's words (pull request #15, 15 October 2026): «la decisione è la 2.»

Decision: the inventories of `tools/sources-study/handoff_data/` stay in the repository with
the text columns removed (list in `tools/sources-study/HANDOFF.md` §2-bis, commit `d3439d2`).
An inventory row may carry URL, dates, identifiers, durations, counts, place names and the
labels and short reasons written by the study's readers; never a text, a title or a person's
name taken from a source. This is the only exception to DEC-102 / DEC-104 / DEC-105 boundary
1 on where per-item data live; the data with texts stay on Drive. The full versions remain in
git history; whether to purge them is a separate owner decision, still open.

Decided by: Owner · Date: 15 October 2026 · Affected: `docs/sources/SOURCE_STUDY_METHOD.md`
§4.2, `tools/sources-study/HANDOFF.md` §2-bis, DEC-102, DEC-104, DEC-105 (pointer only; the
entries are not changed).

# workflows/

n8n workflow JSON exports, one file per workflow. Naming:
`scrape-fb-events-rome.json` for the definitive events workflow; add others as they exist.

**The rule that makes this folder worth having:** no structural change in n8n without
re-exporting the workflow and opening a PR with the new JSON. n8n Cloud keeps no readable
diff between versions; this folder is that diff. If production and this folder diverge,
the divergence is a defect — fix it by exporting, not by editing the JSON here.

How to export: n8n → open the workflow → menu (⋯) → *Download*. Commit the file unmodified.

`staging_*.json` are the staging workflows of the pilot (docs/pilota/CONTRATTI.md), exported
the same way but without their static data, which holds the state of the runs.
`tests/test_workflow_exports.js` checks that every Code node taken from `code-nodes/` is that
file byte for byte.

**`staging_C_*` are off, and stay off until the defects found in the review of their first export
(PR #48) are fixed.** They are in the workflows as they stand; the fix goes to n8n and comes back
here as a new export, in the pull request that turns channel C on again. Any other finding of that
review counts the same way, even if it is not listed here. Fixed so far:
`staging_C_write_canonical` and `staging_C_update_canonical` look each name up before they write
and write one call at a time (below, «The canonical write»); in `staging_C_fb_events_fetch` only a
`SUCCEEDED` run reaches the dataset, the wait ends after 75 minutes, and every run that ends,
failed or not, writes its settled cost (`code-nodes/apify-run.js`), a run that succeeded with the
count of its events. «Start Apify run» gives the run its own timeout (`APIFY_TIMEOUT_S` in
`apify-run.js`), so Apify stops a run before the wait ends and the wait reads its last state; on 16
November 2026 it is not yet tried with a run. The three Apify nodes use the credential «Bearer Auth
account»: until the owner shared it with the workflow's project, on 14 November 2026, the n8n API
refused a change to one of them; since then it saves one, as it saved this timeout. Still open:

- `staging_C_fusion`, «Cambiati»: the file name is rebuilt from `content_id`, which for a web
  series differs from `canonical_file_name` (`code-nodes/web-event-identity.js`); the listed name
  has to travel with each document.
- `staging_C_fusion`: nothing sets `pilot.review_pending` before «Fusione», as
  `docs/pilota/CONTRATTI.md` («C · La fusione dei doppioni») requires.
- `staging_C_fusion`: nothing reads `pilot.geo_recompute`, so an event whose venue, address or
  coordinates came from another source keeps its old geography; the gazetteer resolution has
  to run before «Aggiorna», leaving `human_verified` geography as it is.
- `staging_C_fusion` and the canonical write (below) can run at the same time, and fusion then
  writes back a copy older than the one the write wrote; the two have to run one after the
  other, or the write has to check the revision it read. Fusion does not take the write's
  reservation yet.
- `staging_C_fb_events_fetch`: a retried call starts a second paid run, because nothing that a
  second execution can see records the call before «Start Apify run» (the workflow's static data
  is saved only when an execution ends).
- `staging_C_fb_events_fetch`, «Carica costo»: the node that writes the cost file has no Google
  Drive credential yet. «Google Drive account» is shared with the workflow's project since 14
  November 2026, and «Scarica prova», added on 15 November 2026, carries it: it can be attached to
  «Carica costo» the same way, by the API or in the editor.
- `staging_C_fb_events_fetch`, «Get dataset items»: the cost of a run that succeeded comes after
  its dataset, for the count of its events (the owner's choice of 14 November 2026, PR #51), so a
  dataset read that fails stops the execution before the cost is written. The node has no retry
  yet.
- The cost of a run does not yet reach `pilot.costo` of the events it gave: the canonical writer
  has to read it from `C Eventi/costi/`.
- `staging_C_fusion`: every file of `C Eventi` is downloaded and compared on every run, with no
  bound on the files read or on the time of the execution.

**The canonical write.** `staging_C_write_canonical` and `staging_C_update_canonical` are one flow
under two webhooks, with the same nodes; what each accepts, and the rules, are in
`code-nodes/canonical-write.js`. A request it refuses stops before anything is written, with n8n's
own error. Any other call saves its reservation in `C Eventi/scritture/` before any canonical write
(`prenotazione_<day>_<start>_<execution>.json`, `<day>` being the UTC day of `<start>`, with the
names of its files and never their text), waits 5 seconds, reads the reservations again and goes on
only when no earlier one still holds and its own still does (a call resumed more than 120 minutes
after its reservation stops; one that pauses that long after its turn is not stopped, as Drive gives
no fencing token); otherwise it stops and answers 409, and a later retry is safe. The reading after 5 seconds sees the reservations Drive already lists: one saved just before
but not yet listed does not stop the call, and two calls may then write together; the
duplicate this can leave is found by the next call that writes that name (T24). Each file is then
looked up by its exact name (specification v2.5, phase 5.2) and created, updated or left unchanged,
and the outcome, `esito_<day>_<start>_<reservation id>.json` in the same folder, frees the calls
after it. The answer is that outcome, a body with `status`: 200 when every file is written or
unchanged, 500 when one is not, or when a reading or a step of code failed after the reservation,
which the outcome records. A call that dies outright, or whose outcome cannot be saved, holds the
calls after it for the 120 minutes of the rule. A long call may answer after its caller has given
up: its outcome is still in `scritture/`. The listing of `C Eventi/` reads the whole folder, so its
time grows with the archive that the folder keeps; reading only the names of the call, in batches,
changes the flow and is not done yet. Both were saved in n8n on 16 November 2026, with the
workflows off, and n8n kept every node and setting; since then the review has changed the code of
the four Code nodes, so n8n holds the earlier code until they are saved again from this export,
before the first trial. Not yet tried in n8n, with the workflows off: that the listing returns `md5Checksum` (without
it a file is updated, never duplicated), what the error outputs carry, whether a reading with both
a retry and an error output is retried before it takes the error output, that a failed
«Prenotazioni» gives only its error item although it keeps `alwaysOutputData`, the merge of five
inputs when some stay empty, `$('Nuovo?').item` after the Drive nodes, and the id that «Aggiorna»
returns. A listing of `C Eventi/` that does not show `scritture/` stops the call before any
canonical write.

### Prova senza Apify

`staging_C_fb_events_fetch` also takes, in place of `startUrls`, a request for a saved dataset, so
the channel can be tried without a paid run: `{"fixture": {"file_id": "<Drive file id>", "limit": 20}}`.
The file holds a dataset as Apify gives it, a non-empty JSON array of events, such as those saved
in `C Eventi/fixture/`; `limit`, a JSON number, may be left out, and it never goes past the events
one run can give (`MAX_FIXTURE_EVENTS` in `code-nodes/apify-run.js`). «Prova?» sends such a request to «Scarica
prova» before any paid call: it never reaches Apify and writes no cost, and its events reach «To
JSON file» and `C Eventi/originali/` where the dataset of a run would, in a file whose name ends in
`_prova`. A body with both `startUrls` and `fixture` stops before any call.

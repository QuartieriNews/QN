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
refused a change to one of them; since then it saves one, as it saved this timeout. «Carica costo», the
node that writes the cost file, carries «Google Drive account» like the other two Drive nodes of the
workflow since 18 November 2026 (T-C-costo). Still open:

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
workflows off, and n8n kept every node and setting; the four Code nodes were saved again from these
exports on 17 November 2026, still off, and n8n read back gave these exports node for node. On 18
November «Prenotazioni» lost its error output, «Prima della lettura» came before it and the four
Code nodes took the new turn: not yet saved in n8n. Read in the sources of n8n 2.48.4
(`n8n-core` and `n8n-nodes-base`), not tried: a
merge in append mode runs with the inputs that received data; a node with an error output and
`alwaysOutputData` sends an empty item to its main output beside the error item, so «Prenotazioni»
keeps its error item on its one output and «Turno» throws it to its error route (T29); a Drive
reading that fails gives an item with `error`, retried before it is given; the Wait node, version
1.1, counts in seconds. Not yet tried in n8n, with the workflows off: that the listing returns
`md5Checksum` (without it a file is updated, never duplicated), what the error item of a Code node
carries, `$('Nuovo?').item` after the Drive nodes, and the id that «Aggiorna» returns. «Aggiorna»
retried sends the same bytes to the same file again: a Drive revision more, no file more; n8n
retries on the error of its first item, and a later item that fails goes to «Non aggiornato». A Drive
node that fails outside its own handling of each item gives back its input on its main output:
«Prima della lettura» makes that input a marker, never the call's own reservation, and «Turno»
throws it to its error route (T27, T29). Known limit: a listing of `C Eventi/` that Drive returns
empty reaches no node, and the call dies without its outcome. A listing of `C Eventi/` that does not show `scritture/` stops the call before any
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

### Atti Web

`staging_D_attiweb_list` starts the night at 1:13, Rome time. Until 18 November 2026 it started at
4:13, and on 13, 16, 17 and 18 November the download stopped at 05:00 UTC, within a minute each
night; on 14 and 15 November it ran past 05:00 without error. On 16, 17 and 18 November Google Drive
answered 403 to «Salva PDF» or «Salva record», «Quota exceeded … Requests per minute», for the
consumer project of the credential (on 13 November only the stop is recorded, not its text). None of
our workflows starts at that minute, and the same credential writes every hour at :07 for the B
collection. A quota shared with others and full at that minute on some nights fits these facts; four
nights do not prove it. The night that starts at 1:13 ends, by the runs of November, at about 3:30
Rome time: before the weekly backup at 4:41 (CONTRATTI.md, «Lo storico»), and in winter and summer
before 05:00 UTC. 1:13 is also outside the hour from 2:00 to 3:00 that the change of time skips in
March and repeats in October, when a schedule there would not run or would run twice. If a night
stops again on a Drive 403, the next step is a Google credential with its own project, which is the
owner's to create.

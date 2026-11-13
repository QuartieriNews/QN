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

**`staging_C_*` are off, and stay off until the defects found in the review of their first
export (PR #48) are fixed.** They are in the workflows as they stand; the fix goes to n8n and
comes back here as a new export, in the pull request that turns channel C on again. Any other
finding of that review counts the same way, even if it is not listed here. Fixed so far: in
`staging_C_fb_events_fetch` only a `SUCCEEDED` run reaches the dataset, the wait ends after 75
minutes, and every run that ends, failed or not, writes its settled cost
(`code-nodes/apify-run.js`). Still open:

- `staging_C_write_canonical`: a retried call uploads the same file name again, and Drive keeps
  both; the write has to look the name up first.
- `staging_C_fusion`, «Cambiati»: the file name is rebuilt from `content_id`, which for a web
  series differs from `canonical_file_name` (`code-nodes/web-event-identity.js`); the listed name
  has to travel with each document.
- `staging_C_fusion`: nothing sets `pilot.review_pending` before «Fusione», as
  `docs/pilota/CONTRATTI.md` («C · La fusione dei doppioni») requires.
- `staging_C_fusion`: nothing reads `pilot.geo_recompute`, so an event whose venue, address or
  coordinates came from another source keeps its old geography; the gazetteer resolution has
  to run before «Aggiorna», leaving `human_verified` geography as it is.
- `staging_C_fusion` and `staging_C_update_canonical` can run at the same time, and fusion then
  writes back a copy older than the one the update wrote; the two have to run one after the
  other, or the write has to check the revision it read.
- `staging_C_fb_events_fetch`: a retried call starts a second paid run, because nothing that a
  second execution can see records the call before «Start Apify run» (the workflow's static data
  is saved only when an execution ends).
- `staging_C_fb_events_fetch`, «Carica costo»: the node that writes the cost file has no Google
  Drive credential yet; the n8n API cannot attach it, the owner does in the editor.
- `staging_C_fb_events_fetch`, «Start Apify run»: the URL needs `&timeout=3600`, so Apify itself
  stops a run after the hour (`APIFY_TIMEOUT_S` in `apify-run.js`) and the 75-minute wait reads its
  last state. The n8n API does not change a node that holds a credential: the owner adds it in the
  editor.
- The cost of a run does not yet reach `pilot.costo` of the events it gave: the canonical writer
  has to read it from `C Eventi/costi/`.
- `staging_C_update_canonical`: two calls at the same time for a name not yet on Drive both
  upload it, and Drive keeps both.
- `staging_C_fusion`: every file of `C Eventi` is downloaded and compared on every run, with no
  bound on the files read or on the time of the execution.

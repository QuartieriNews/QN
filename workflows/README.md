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
finding of that review counts the same way, even if it is not listed here:

- `staging_C_fb_events_fetch`, «Finished?»: an Apify run that ends `FAILED`, `ABORTED` or
  `TIMED-OUT` goes on as if it had succeeded; only `SUCCEEDED` may reach «Get dataset items».
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
- `staging_C_fb_events_fetch`: the wait for the Apify run has no limit of attempts or time, and
  the workflow has no execution timeout; and a retried call starts a second paid run, because
  nothing records the call before «Start Apify run».
- `staging_C_fb_events_fetch`: no step reads the cost of the Apify run or adds it to
  `costi.jsonl` and to `pilot.costo`, as `docs/pilota/CONTRATTI.md` («Costi») requires.
- `staging_C_update_canonical`: two calls at the same time for a name not yet on Drive both
  upload it, and Drive keeps both.
- `staging_C_fusion`: every file of `C Eventi` is downloaded and compared on every run, with no
  bound on the files read or on the time of the execution.

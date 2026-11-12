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

**`staging_C_*` are off, and stay off until four defects are fixed.** The review of their first
export (PR #48) found them in the workflows as they stand; the fix goes to n8n and comes back
here as a new export, in the pull request that turns channel C on again:

- `staging_C_fb_events_fetch`, «Finished?»: an Apify run that ends `FAILED`, `ABORTED` or
  `TIMED-OUT` goes on as if it had succeeded; only `SUCCEEDED` may reach «Get dataset items».
- `staging_C_write_canonical`: a retried call uploads the same file name again, and Drive keeps
  both; the write has to look the name up first.
- `staging_C_fusion`, «Cambiati»: the file name is rebuilt from `content_id`, which for a web
  series differs from `canonical_file_name` (`code-nodes/web-event-identity.js`); the listed name
  has to travel with each document.
- `staging_C_fusion`: nothing sets `pilot.review_pending` before «Fusione», as
  `docs/pilota/CONTRATTI.md` («C · La fusione dei doppioni») requires.

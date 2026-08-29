# code-nodes/

The source of each n8n Code node, one file per node, named after the node:
`compute-source-hash.js`, `parse-duration.js`, `validate-geo-response.js`, …

Two rules:

1. Each file must run outside n8n (plain function, explicit inputs/outputs), so it can be
   tested without the pipeline. The geography validation code already exists at the bottom
   of `prompts/PROMPT_GEO_BLOCK.md` — when wired, it is copied here as its own file.
2. The code inside the n8n node must be byte-identical to the file here. A PR that changes
   one must change both (the workflow export in `workflows/` carries the node's copy).

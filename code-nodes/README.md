# code-nodes/

The source of each n8n Code node, one file per node, named after the node:
`compute-source-hash.js`, `parse-duration.js`, `validate-geo-response.js`, …

Two rules:

1. Each file must run outside n8n (plain function, explicit inputs/outputs), so it can be
   tested without the pipeline. The geography validation code already exists at the bottom
   of `prompts/PROMPT_GEO_BLOCK.md` — when wired, it is copied here as its own file.
2. The code inside the n8n node must be byte-identical to the file here. A change that
   touches one must touch both (the workflow export in `workflows/` carries the node's
   copy). To make byte identity actually achievable, each file is ONE executable source
   for both contexts: it ends with a context switch — under plain Node
   (`typeof $input === 'undefined'`) it exports its functions and stops (top-level
   `return` is legal in CommonJS); inside the n8n Code node the same file runs its
   per-item adapter. Paste the whole file into the node, nothing less.
   Pattern established in cycle 1 (`parse-duration.js`); every future node follows it.

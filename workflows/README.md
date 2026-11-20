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

**`active` in an export** is the state the workflow had on n8n when it was exported, on the day of
the commit that brings the file: `true` if it was on, `false` if it was off. Switching a workflow
on or off is not a structural change; the export keeps the state of its day until the workflow is
exported again. An export taken with the API (`GET /workflows/{id}`, docs/pilota/WORKSTREAM_A.md,
section 8, point 9) takes `active` and `versionId` as n8n gives them, and each node with every key
n8n gives. The test checks that every export says `true` or `false` (T-WF-attivo). It does not
compare `active` across files: two exports can be of different days, so whether a workflow that is
on has its error workflow on too is checked on n8n, not here (docs/pilota/WORKSTREAM_A.md, section 8,
point 4).

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
Code nodes took the new turn: both were saved again from these exports that day, still off, after
n8n was found equal to the earlier exports, and n8n read back gave those exports node
for node, with the versionIds of that day. On 19 November «Elenco C Eventi» took the shape of
«Prenotazioni» and the four Code nodes the new plan: on 20 November, after the merge, both were
saved again from `main`, still off, after n8n was found equal to the exports of 18 November, and
n8n read back gives these exports node for node, with the versionIds they carry (`268bc318…` for
`staging_C_write_canonical`, `744ece96…` for `staging_C_update_canonical`). Read in the sources
of n8n 2.48.4 (`n8n-core` and `n8n-nodes-base`), not tried: a
merge in append mode runs with the inputs that received data; a node with an error output and
`alwaysOutputData` sends an empty item to its main output beside the error item, so «Prenotazioni»
keeps its error item on its one output and «Turno» throws it to its error route (T29); a Drive
search that finds nothing gives no item, and with `alwaysOutputData` one empty item; a Drive
reading that fails gives an item with `error`, retried before it is given; the Wait node, version
1.1, counts in seconds. Not yet tried in n8n, with the workflows off: that the listing returns
`md5Checksum` (without it a file is updated, never duplicated), what the error item of a Code node
carries, `$('Nuovo?').item` after the Drive nodes, and the id that «Aggiorna» returns. «Aggiorna»
retried sends the same bytes to the same file again: a Drive revision more, no file more; n8n
retries on the error of its first item, and a later item that fails goes to «Non aggiornato». A Drive
node that fails outside its own handling of each item gives back its input on its main output:
«Prima della lettura» makes that input a marker, never the call's own reservation, and «Turno»
throws it to its error route (T27, T29). «Elenco C Eventi», the listing of `C Eventi/`, has the
same shape as «Prenotazioni», one output and `alwaysOutputData`: a listing that Drive returns empty
reaches «Piano» as an empty item, one that fails as its error item, one that fails outside its
handling of each item as the input it was given. «Piano» throws each to its error route, the error
item with the error of the reading (T29): a listing of `C Eventi/` that does not show `scritture/`,
an empty one too, stops the call before any canonical write, with its outcome (T-C-elenco-vuoto).

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

The night of 19 November 2026 stopped at 02:03 UTC on a block signal of the portal, not on that
quota: «Controllo PDF» of `staging_D_attiweb_download` (execution 1903) had a 403 in answer to a
PDF, and the reading stopped (DEC-033, rule 4). `staging_D_attiweb_list` was then switched off,
and it stays off until the owner decides.

### La misura di GDELT

`staging_B_gdelt_misura` is the two-week measure of DEC-039, point 4, read as DEC-045 says
(`docs/pilota/CONTRATTI.md`, section 7 B, «Misura GDELT», holds its rules): every two hours, at :37
of the odd hours of Rome, thirteen searches of GDELT's free search service (DOC 2.0 API), one at a
time, in an order that turns by one place every two hours. Its Code nodes are
`code-nodes/news-gdelt.js`. A search is sent only after «Prima» has seen that the host did not stop,
answer 429, or fail to answer earlier in the run; it leaves the search it lets go in the static data
(`news_gdelt_request`), where «Dopo la risposta» takes it, so an answer never depends on reading an
earlier node of the loop back. The files of a run go to `B Notizie/letture/` one after the other,
rows, register, alert. Each Drive node retries five times, as in the B collection, and then goes on,
so the execution ends and n8n saves its static data. «Conferma» then makes the windows and the counts
of the run the state of the flow only if the rows and the register were written (every run that is
not past the end writes its rows file, empty when it kept no article, and no register is written
after rows that were not); a stop holds at once with the two counts that go with it, and names a file not written for the next run's register and
alert; a run whose files fail is read again by the next one. A stop holds at once, the one the
close decides on the sixth run with a 429 or the fifth with a server error included: a run whose
files fail is read again, but its stop is not undone. The register carries the
`workflow_version` of «Inizio», which changes with every change of the flow. The flow saves no data of
a successful execution, because the answers carry titles. Its error flow is `staging_B_avviso`, which
writes `AVVISO_B_<time>.json` in the same folder and stays on: n8n does not call an error flow that
is off. The alerts of both reach the owner through the coordinator, who reads `letture/`.

**It reads the search service, not the 15-minute files (DEC-045, point 1).** The owner's words, in
the night mandate of 19 November 2026 (`MANDATO_NOTTE_2026-11-19.md` on Drive): if the files do not
hold on n8n, «Sì, usa la ricerca», with the same data, title, link and hour only. The numbers, read
on 19 November 2026 between 22:45 and 23:10 UTC:
- the translation stream of GDELT, where Italian articles are, gives a GKG file every 15 minutes:
  the latest, 22:45 UTC, is 5.6 MB zipped and 17.7 MB unzipped; at 09:00, 12:00, 15:00 and 18:00
  UTC of the same day the files are 11.4–13.0 MB zipped, and 15.1 MB at 12:00 on 18 November: about
  35–48 MB of text for a daytime quarter of an hour, 96 a day. The title is there (`<PAGE_TITLE>` in
  `V2.1EXTRASXML`, 1,425 of the 1,446 rows of the 22:45 file);
- n8n Cloud, Starter plan, by n8n's documentation («Cloud data management»): 640 MiB of RAM for the
  instance, of which the software takes about 180 MiB, 10 millicore of CPU, and 2,500 executions a
  month for every flow of the pilot;
- of Node's modules, only `crypto` has been tried in a Code node here (`docs/pilota/WORKSTREAM_A.md`,
  section 3), so unzipping goes through n8n's own nodes, which hand the 35–48 MB of text on as JSON
  in the execution (a reading of how n8n works, not tried); one execution per file is 2,880 a month,
  more than the plan, and four files in one execution are 140–190 MB of text;
- an answer of the search service is a few kilobytes.

From this sandbox the service answered 200 twice and then 429 («Please limit requests to one every
5 seconds») with 8 seconds between requests: the limit counts the address, and the sandbox's is
shared. In October the source study had found the same (`docs/sources/CRONACA_PROCESSO_2026-10.md`,
section 5.2: the service «risponde 429 (troppe richieste da un indirizzo condiviso)»; section 5.3,
point 5: «GDELT da un indirizzo non condiviso»).

**The first run on n8n stopped the host (DEC-045, point 2, came after it).** On 19 November 2026 at
23:28 UTC (00:28 of 20 November in Rome), with a one-off schedule: robots.txt answered 404 (no rules),
and the first search, 10 seconds later, answered 429. The host stopped, as the rule of the collection
said then, the other twelve searches were not sent, no window moved, and the run wrote
`gdelt_20261119T232800Z.json` and `AVVISO_gdelt_20261119T232800Z.json` in `B Notizie/letture/`; the
execution was not saved, as its settings say. A 429 at the first request fits an address that n8n
Cloud shares with others, as the sandbox's is shared; one run does not prove it. The flow was then
off from 23:37 to 23:46 UTC. On 20 November 2026, at about 00:44 in Rome, the owner chose «Retry, stop
after 6» (DEC-045, point 2): the flow was saved again with that rule and with the stop cleared from its
static data, and it was switched on, on its schedule. The series of runs with a 429 starts at the first
run: the run of 23:28 UTC on 19 November is the first of the six. The run of 00:37 UTC on 20 November
read one search and then met a 429: it is the second, and the count was set to 2 in the static data at
00:40 UTC (the update kept the versionId). The runs count in a row: while the host is not stopped,
any run without a 429, one that asks nothing included, sets the count back to zero, and the count of
runs with a server error or no answer works the same way. Once the host is stopped, both counts stay
as they are until the restart.
A draft email asking GDELT for access is in the hand-off folder on Drive, for the owner to send.

**Restarting and ending.** A host that stopped, on six runs in a row with a 429, on five with a server
error or no answer, or on any other block signal, stays stopped until the owner says to restart it.
Only then does the coordinator clear `news_gdelt.host.stopped` in the flow's static data and set both
counts of runs in a row, `throttled_runs` and `errors_in_row`, to zero (n8n's API takes `staticData`
with an update of the workflow); the coordinator never restarts it alone. After the measure, from 02:00 in Rome on 4 December 2026, a run asks and writes nothing,
except the first, which writes `AVVISO_gdelt_fine_<start>.json` (if the notice is not written, the
next run writes it): the coordinator then switches the flow off, since every run is still an
execution of the plan. `staging_B_avviso` retries its Drive write five times, as the alert flows of A
and D do.

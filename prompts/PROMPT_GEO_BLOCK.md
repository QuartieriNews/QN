# Geography block — replacement for the current prompt section

Drop-in replacement for the `IMPORTANT FOR LOCATION ENRICHMENT` section of the
`Classify & Extract Event` node, plus the code that must run before and after it.

This file covers geography only. The editorial judgement — is this item worth publishing at
all — is a separate pass with its own prompt, in `EDITORIAL_FILTER.md`. Keeping them apart
is what makes a fall in the weekly number attributable to one or the other (I5).

The 89 allowed values are in `prompt_list_publication_zones.txt`, which is **generated**
from `gazetteer.json`. Do not maintain a second copy of that list.

---

## What changes and why

**Removed:** `NEVER leave municipio, urban_zone, or neighborhood empty for Rome addresses`
and `If exact match is uncertain, choose the MOST LIKELY and widely recognized area`.

Those two lines mandate a confident guess. They also make the reject queue impossible: a
model that always answers produces no rejects to review, only silent errors on published
pages. The whole bug-fixing loop depends on the model being allowed to say *unknown*.

**Removed:** the ~250-item neighbourhood list, replaced by the 89 publication zones. The
question changes from "which of 250 toponyms" to "which of 89 areas" — a coarser call the
model handles better, and the only one the site actually needs.

**Fixed in v1.2:** the prompt list no longer carries the municipality in brackets. The
previous list gave the model `Acilia  (Municipio X)` while the validator compared against
`Acilia`, so a model obeying the instruction *use the exact spelling from the list* would
have been rejected. The municipality stays in the JSON, where the site can read it.

**Added in v1.2:** the model is not always called twice. See *Conditional second pass*.

**Added:** `geo_basis`, recording how the answer was reached. Explicit addresses and
context inferences have very different error rates and must be countable separately.

**Fixed in v1.3:** `zone_not_published` was checked *after* the model. It could never fire
there — the model is only ever given the 89 pages, so it cannot return Agro Romano. The
real case (an alias hit on Corcolle, Fiorano or Torricola) happens at step 3, and that is
where the check now lives.

**Added in v1.3:** `geo_level`, and two guards that were listed in v1.2 without an
implementable rule or a reject code.

---

## Order of operations

The model sits between deterministic layers on both sides, and is skipped entirely
whenever something cheaper already knows the answer.

```
0. human_verified value on this item?          -> use it, stop. Never recompute.
0b. online? (isOnline AND no coords AND no id) -> zone empty, geo_level city, no reject
1. guards TIER A (coordinate validity)         -> reject before spending anything
2. venue registry (venues.json, location.id)   -> hit: zone known, skip to 6
                                               -> MISS IS NOT A REJECT: continue
3. guards TIER B (suspicion signals)           -> only reached on a registry miss
4. alias lookup (name_display + aliases)       -> exact match only
   4b. is the matched zone a page?             -> no: zone_not_published, stop
5. model, pass 1, and pass 2 under the rule    -> closed list of 89, empty permitted
6. validation                                  -> the code at the bottom of this file
```

**Two orderings changed in v1.4.** The guards are split — tier A asks whether the
coordinate is usable, tier B whether the record is suspicious, and a venue the registry
already knows makes suspicion moot. And a registry **miss is not a reject**: v1.3's
`WORKFLOW_FIXES` said it was, and with `location.id` present in 106 of 107 records that
would have queued essentially the whole corpus before the alias lookup ever ran.
`venue_unresolved` is terminal — it fires when the registry, the alias lookup and the model
have all failed.

Step 4b is new in v1.3 and is not cosmetic: 29 of the 440 neighbourhoods route to a zone
that is not a page, and a correct alias hit on one of them must be counted as
`zone_not_published`, not passed to the model as if unresolved.

Steps 1, 2, 3 and 6 cost nothing per item and their hit rate rises every week the reject
queue is worked. That is the whole economic argument for the operating model.

---

## Conditional second pass

The decision to keep two independent geographic passes stands. Running both on **every**
item does not: it doubles the AI cost across the whole volume to protect a segment that
`geo_basis` already isolates.

| First pass returns | Second pass | Why |
|---|---|---|
| `explicit_address` | no | The source states a street, piazza or venue. There is little for a second pass to disagree with. |
| `explicit_zone` | no | The source names one of the 89 areas outright. |
| `inferred` | **yes** | Deduced from context. This is where the errors are. |
| `unknown` | **yes** | Cheap second opinion before it goes to the reject queue. |

Run the second pass as well, whatever the first returned, when there was **no venue-registry
hit and no street address** on the source record. `location.streetAddress` was null in 94 of
107 measured records, so this is not a rare branch.

The second pass must be **independent**: same closed list, no sight of the first answer. A
pass that reviews the first one agrees with it.

Reconciliation:

| Outcome | Result |
|---|---|
| Same zone | accept · `geo_verification_status = ai_agreement` |
| Different zones | zone empty · `reject_reason = ai_disagreement` |
| One empty, one not | zone empty · `reject_reason = zone_unknown` |
| Both empty | zone empty · `reject_reason = zone_unknown` |

**Reopen this** if the weekly sample shows single-pass accuracy below 95% on
`explicit_address` items. Then the mode goes to `always` and the cost is justified by
measurement rather than by caution.

---

## Prompt text

```
LOCATION

Return the publication zone the event belongs to, using the list of allowed values
supplied below. Use the exact spelling from the list, and nothing else — no municipality,
no brackets, no qualifiers.

How to decide, in order:

1. If the post states a street address, a piazza, or a named venue, use it to determine
   the zone.
2. If the post names an area directly and that name appears in the list, use it.
3. Otherwise return an empty string.

Rules:

- An empty string is a correct answer. Do not choose the most likely zone when the source
  does not support one. A missing value is recoverable; a wrong one is published.
- Return only values from the allowed list. Never invent, abbreviate, or combine names.
- Online events are decided before you see the item. Do not classify them.
- If the event is outside Rome, set city accordingly and return an empty string for the
  publication zone.

Also return geo_basis, exactly one of:

  explicit_address  the post states a street, piazza or venue that determines the zone
  explicit_zone     the post names the area itself
  inferred          you deduced the zone from context rather than a stated location
  unknown           you could not determine it (publication_zone must then be empty)

Do not explain your reasoning. Return the field values only.

ALLOWED VALUES:
<paste the values from prompt_list_publication_zones.txt — the names only, without the
generated header>
```

---

## Validation after the model returns

A Code node. None of these checks is optional: without them the closed list is a
suggestion rather than a constraint.

Note that `is_page` and `resolvable` are **real booleans** in `gazetteer.json` v1.2. They
were the strings `"TRUE"` / `"FALSE"` in v1.1 and any code comparing against `"TRUE"` will
silently reject everything.

```js
// gazetteer.json, loaded once
const pages = new Map(                       // display name -> zone id
  gazetteer.publication_zones
    .filter(z => z.is_page === true)
    .map(z => [z.name_display, z.publication_zone_id])
);
const allZones = new Map(
  gazetteer.publication_zones.map(z => [z.name_display, z])
);

let zoneName = (ai.publication_zone || "").trim();
let zoneId = "";
let reject = null;

// 0. a human decision is final
if (item.geo_verification_status === "human_verified") {
  zoneId = item.publication_zone_id;
  if (zoneName && pages.get(zoneName) !== zoneId) item.geo_conflict = true;
  zoneName = "";                             // nothing below runs
}

// 1. the value must exist at all
else if (zoneName && !allZones.has(zoneName)) {
  reject = "zone_not_in_list";
}

// 2. a real zone that has no page. Unreachable from the model — it only ever sees the
//    89 pages — and kept as a belt-and-braces check in case the prompt list is ever
//    built from the wrong filter. The case that actually fires is in the alias lookup.
else if (zoneName && !pages.has(zoneName)) {
  reject = "zone_not_published";             // Agro Romano, Other
}

// 3. an inferred zone with no stated location is not evidence
else if (zoneName && ai.geo_basis === "inferred" && !ai.event_location) {
  reject = "zone_unknown";
}

else if (zoneName) {
  zoneId = pages.get(zoneName);
}

else {
  reject = reject || "zone_unknown";
}

return { publication_zone_id: reject ? "" : zoneId, reject_reason: reject };
```

### Alias lookup, steps 4 and 4b

Exact match on `name_display` and on the pipe-separated `aliases`, case- and
accent-insensitive. Three rules the implementation must not improvise:

- **Ambiguity is a reject, not a coin flip.** `Colle del Sole` is the name of two distinct
  neighbourhoods (Municipio VI and XI) and resolves to two different pages. On more than
  one match: zone empty, `reject_reason = ambiguous_alias`. The build script fails if a new
  ambiguous key appears without being declared.
- **`resolvable = false` is about the neighbourhood, not the zone.** Acilia, Ostia,
  Monteverde, Laurentino and Trigoria are containers as neighbourhoods *and* valid
  publication zones. A post that says *ad Acilia* resolves to zone `acilia` with
  `neighbourhood_id = null`. Rejecting it would reject the commonest phrasing in
  Municipio X.
- **A resolved zone is not necessarily a page — check it here.** 29 of the 440
  neighbourhoods map to `Agro Romano` or `Other`. A correct hit on Corcolle, Fiorano or
  Torricola is a real place with nowhere to publish: `reject_reason = zone_not_published`,
  and stop. Do not fall through to the model, which would either invent a nearby page or
  return empty and be logged as `zone_unknown` — both of which hide a case that has its
  own counter for a reason (I6).

```js
// step 4b, immediately after a successful alias match
const hood = gazetteer.neighbourhoods.find(n => n.neighbourhood_id === matchedId);
if (hood && hood.publishable === false) {
  return { publication_zone_id: "", neighbourhood_id: hood.neighbourhood_id,
           reject_reason: "zone_not_published" };
}
```

Note `publishable` is derived onto every neighbourhood row by `build_gazetteer.py`, so this
needs no second lookup.

### Matching inside free text

Matching a gazetteer key in `location.name` and matching it in a description are not the
same operation. `prati`, `talenti`, `eur`, `marconi` and `morena` are ordinary Italian
words, a price token and a surname. `gazetteer.json → free_text_stoplist` lists the keys
that must not be matched inside a title or a description; they remain matchable in
`location.name`, `location.streetAddress`, `location.address` and `address`, where a string
is a place by construction.

Do not substitute a minimum key length for this list: it excludes `EUR` and `AXA` — two
real zones, one of them in Municipio X — while still admitting every common word of five
letters or more.

### What to store

```json
{
  "publication_zone_id": "acilia",
  "neighbourhood_id": "acilia-nord",
  "geo_level": "neighbourhood",
  "municipality_code": "X",
  "geo_basis": "explicit_address",
  "geo_verification_status": "deterministic_alias",
  "geo_logic_revision": "1.4"
}
```

`municipality_code` is new in v1.4 and is not decoration. v1.3 said a municipality-level
item carries an empty zone and that the layout would use it for the fallback — while
storing nothing that said *which* municipality. That is a rule with no output field, the
defect this project's own principles forbid, and it would have surfaced only after the
institutional block had collected a corpus, i.e. as a migration. At zone level it is
derived from the zone's `primary_municipality`; at municipality level it is the only
routing key there is.

`geo_level` is new in v1.3: `neighbourhood` · `zone` · `municipality` · `city`. The events
block only ever writes the first two. It exists because the other blocks do not resolve to
a neighbourhood and must not be forced to — a municipal commission sits at municipality
level by nature — and because the page layout uses it to decide what a thin page falls back
to. The fallback is a rendering choice made from stored fields; an item is never
re-resolved to a coarser zone, which would write a false fact into the corpus.

`neighbourhood_id` is filled **only** when it is known deterministically — from the venue
registry or from an alias match. `null` when the zone came from the model. The model is
never asked to choose among 440 toponyms; but when the finer level is known for free, it is
kept, because maps, search and any future sub-page will want it and it costs nothing today.

---

## Online events — decided deterministically, step 0b

v1.3 had this in three places at once: the README made it a deterministic step, the prompt
asked the model, and `SOURCE_DATA_FINDINGS.md` had already measured `isOnline` as
unreliable — true on 1 of 50 records, and false on an event titled *Join our online
Meditation Community*. Nobody was actually deciding.

The rule, deliberately conservative:

> An item is online **only if** `isOnline` is true **and** there are no coordinates **and**
> there is no `location.id`. Anything with a physical venue is treated as physical whatever
> the flag says.

Result: `publication_zone_id` empty, `geo_level = city`, **no reject** — an online event is
a valid item with no zone, not a failure. The model is not asked, because it cannot see
`isOnline`, the coordinates or `location.id`, so any answer it gives is a guess about a
field it was never shown.

---

## Guards

Run `gazetteer.json → guards` first. They cost nothing and they catch failures the model
cannot catch, because it never sees the coordinates.

| Guard | Check | Reject |
|---|---|---|
| Rome bounding box | numeric | `outside_rome` |
| Centroid blocklist | numeric, tolerance 1e-6 | `centroid_detected` |
| `placeType: CITY` | string equality | `place_type_city` |
| Name/coordinate contradiction | string, see below | `name_coord_mismatch` |
| `countryCode` null with coordinates | null check | `country_code_missing` |

Two of these were incomplete in v1.2 and are now implementable.

**Name/coordinate contradiction is not a numeric comparison**, though v1.2 listed it among
them, and the rule it was given in v1.3 rejected valid Rome records. It is **two rules for
two different fields**, because the two fields are not the same kind of string.

**`location.city`** is genuinely composite and hierarchical — measured as
`"Rome, NY, United States"`, `"Brighton and Hove, United Kingdom"`. An allowlist on its
tail is right:

> Take the text after the **last comma** in `location.city`. Normalise: casefold, strip
> accents and punctuation, collapse runs of whitespace. Accept if the tail is in
> `guards.name_coordinate_mismatch.rule_location_city.accepted_tails` **or** is itself a
> gazetteer lookup key. Otherwise reject.

The second clause matters: `"Palazzo dei Congressi, EUR"` has the tail `EUR`, which is a
publication zone, and an allowlist alone rejected it in testing.

**`location.name` is a venue name, not an address.** The text after its comma is usually a
room, a floor or a street — this is where v1.3 went wrong, rejecting
`"Teatro Argentina, Sala Squarzina"` and `"Casa del Municipio, Sala Consiliare"`. No tail
parsing here at all:

> Split the normalised `location.name` on commas. Reject only if a **whole segment** equals
> an entry in `guards.name_coordinate_mismatch.rule_location_name.foreign_place_markers`.

Whole segments, not substrings: the first replacement attempt used a substring test and
rejected `"London Pub"`, which is a plausible Rome venue. `"London, U.K."` and a bare
`"Waterloo"` are still rejected, and Italian cities other than Rome are on the marker list
because `"Florence, Tuscany, Italy"` was observed carrying Rome coordinates — its country
tail is legitimately `italy`, so the city rule cannot catch it.

A blocklist here **fails open**: an unlisted foreign toponym publishes. That is the correct
direction for an unbounded field, because the bounding box, the centroid blocklist and the
`countryCode` guard cover the same case from other angles. An allowlist over venue names
would reject the valid majority.

`test_guards.py` checks both directions. The negative half is the one that matters: a guard
that fires on a valid record removes it silently and irreversibly.

**`countryCode` null with coordinates present** had an action in v1.2 — *route to the reject
queue* — but no code in the enum, so it landed under some other reason and corrupted the
weekly sort, which is the number the week's work is prioritised on. It now has
`country_code_missing`.

---

## The measurement that makes this safe

Errors here are silent: an event lands on the wrong page and nothing looks broken. The
reject queue shows what was blocked, never what was wrongly published.

Sample **20 published items per week** and check one thing: is the zone right? (The same
weekly review also samples **10 discarded items** — that sensor belongs to the editorial
filter, not to geography; see `REVIEW_QUEUE.md`.) Above 95%,
the approach holds and the deterministic street register was unnecessary. Around 70%, you
learn it from 80 checks instead of from eighty wrong pages. Start the sample with the first
published week, not once the system feels stable — only 82 of 440 gazetteer rows currently
carry an alias, so early accuracy is an open question, not a safe assumption.

Every error found becomes an alias in the gazetteer or a record in the venue registry, not
a one-off fix. That is what makes the cost of bug fixing fall over time instead of
repeating.

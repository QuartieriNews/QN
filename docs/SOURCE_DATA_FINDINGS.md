# Source Data Findings — Apify Facebook Events Scraper

Measured on three live samples, 19 August 2026. Actor: `apify/facebook-events-scraper`.
These are observations, not documentation claims — several contradict what the actor's
description implies.

---

## 1. Discovery method determines data quality

| | Keyword search `q=rome` | `explore/it-rome` | **Direct event URLs** |
|---|---|---|---|
| Sample size | 30 | 50 | 107 |
| `countryCode: IT` | 37% | 88% | 88% |
| Coordinates present | 70% | 96% | **99%** |
| Image present | 90% | 100% | **100%** |
| Description present | 97% | — | **100%** |
| `ticketsInfo` present | 20% | — | **50%** |
| Events in Municipio X | 0 | 0 | 1 |

**Direct URLs return systematically richer records** than search results, because the full
event page carries more fields than the search card. This is the reason the manual URL
collection strategy was adopted.

**Keyword search is unusable for Rome.** `rome` is an English word: the sample returned
Rome NY, Rome GA, Brighton, Boston, Denver, Culver City, Wayland and Bellaire MI. Only 11
of 30 were in Italy, and by editorial judgement only 5 were real local events.

---

## 2. Coordinates are present but not always true

The single most important finding for the geography design.

**When `location` exists, coordinates exist** — 106 of 107 in the direct-URL sample. But
three failure modes produce coordinates that look valid and are not:

**Centroid fallback.** Unrelated events share identical coordinates representing the city
rather than a venue. Point-in-polygon on these resolves confidently to the historic centre
and is always wrong. Observed pairs, now in `gazetteer.json → guards`:

```
41.900859832764 / 12.483275413513   ← seen in two separate samples
41.9009311      / 12.5012052
41.9            / 12.5
41.882726005483 / 12.490425109863
```

Detection heuristic: identical coordinates on unrelated events. Legitimate repeats also
occur (Terme di Caracalla, Auditorium Parco della Musica, Terrazza Borromini appeared
twice each), so the blocklist must be an explicit list, not a rule about repetition.

**`placeType: CITY`** returns the city centroid. City known, area unknowable.

**Name/coordinate contradiction.** Records were observed with:

| `location.name` | Coordinates | Reality |
|---|---|---|
| Rim Park, Room 207 | 41.909 / 12.456 | Waterloo, Ontario |
| London, U.K. | 41.902 / 12.506 | not Rome |
| Florence, Tuscany, Italy | 41.906 / 12.491 | not Rome |

Facebook appears to backfill the search city's coordinates when the venue is unresolved.
Two of the three also had `countryCode: null`, which is a usable suspicion signal.

---

## 3. Fields that do not behave as documented

**`location.city` is not a city name.** Null in 88 of 107 records; when present it is a
composite string (`"Rome, NY, United States"`, `"Brighton and Hove, United Kingdom"`).
Cannot be used as the primary `is_rome` signal. `countryCode` is clean and should be.

**`paidContent` is useless.** `false` on all 187 records across the three samples,
including a Candlelight concert with a live ticket-purchase link. `ticketsInfo.price` was
null in every case where `ticketsInfo` existed. Only `ticketsInfo.buyUrl` is reliable.
Implication: `cost_type` should default to `unknown`, `booking_url` from `buyUrl`.

**`isOnline` is unreliable.** True on 1 of 50 in one sample; an event literally titled
"Join our online Meditation Community" was `false` with a physical venue assigned.

**There is no end-date field.** Only `utcStartDate`, `duration` and `dateTimeSentence`.
`duration` is free text (`"5 days"`, `"1 hr 30 min"`) and null in 45 of 107.
`dateTimeSentence` renders in arbitrary timezones — a Rome event appeared with **SAST**
(South Africa).

*Consequence:* the rule `effective_end = end ?? start` means a three-day sagra is treated
as finished after day one — the exact defect the v1.1→v2.x correction was meant to prevent,
reintroduced by the source rather than by the logic. A `duration` parser is required, with
null plus a warning when unparseable. Never derive absolute times from `dateTimeSentence`.

---

## 4. Recurring events are 11% of the sample, and unhandled

11 of 107 records carry `hasChildEvents: true` — `eventFrequency` `WEEKLY` on 8, `CUSTOM`
on 3. Child counts are large: 52, 51, 47, 46 occurrences.

As currently designed the pipeline would produce **one article with a single date** for an
event running 52 times. This is reader-visible, not an internal defect. It also breaks the
`content_id` scheme: one `source_event_id`, fifty-two dates.

Useful detail: `duration` was present and parseable on **all 11** recurring events.

---

## 5. Near-duplicates that `source_event_id` does not catch

Observed in two separate samples: the same event published twice by the organiser, with
**different event ids**, identical `location.id` and identical `utcStartDate`.

- Sample 1: "Travel Talk - Rome" ×2
- Sample 2: Teatro Trastevere show, Ruby Giulia live set, "Meditation Community" — three
  pairs

Deduplication on `source_event_id` cannot see these. A soft key of
`location.id + utcStartDate` should **flag**, not delete.

---

## 6. `location.id` is the right gazetteer key

Present in 106 of 107 records with a location, and stable across events — St Georges Church
appeared in two different events with the same id `406634282835342`.

A venue gazetteer keyed on `location.id` resolves a place once and forever, with no fuzzy
name matching, no accent handling, no spelling variants. Preferable to name-based lookup
for the venues that are not street addresses (stations, parks, theatres, parish halls).

---

## 7. Other measured values

- **`placeType` distribution** (direct URLs): `TEXT` 86, `PLACE` 17, `CITY` 2,
  `GEO_ENTITY` 1, none 1. Free-text locations dominate.
- **`address` null** in 81 of 107; `location.streetAddress` null in 94 of 107. The
  address-based path is the exception, not the norm.
- **Image URLs** carry the CDN signing parameters `oh=`, `oe=`, `_nc_ohc=`, which expire.
  Confirms both the pre-hash normalisation requirement and the need to archive images
  rather than store links.
- **Cost**: 107 events billed 1.40 $ at the 13 $/1,000 base rate.
- **Language varies.** One event's description was entirely in Hungarian. Several records
  were commercial offerings (photo shoots, tours, cruises) rather than events — an
  editorial filter, not a geographic one.

---

## 8. Sample limitations

187 records total, collected on a single day in mid-August — the deadest week of the
Italian calendar. Field fill rates are probably representative; geographic and thematic
composition probably is not, and likely understates local community activity.


---

## 9. Addendum — measured on the raw samples, 21 August 2026

Section 8 above is unchanged: it is a record of what was observed on 19 August. This
addendum records what running `zone_distribution.py` on the raw files afterwards revealed,
and it corrects one claim made in §6.

### 9.1 `location.id` repeats far less than §6 implies

§6 concluded that a venue registry keyed on `location.id` "resolves a place once and
forever", generalising from one repeated id in the 30-event sample.

Counting every distinct event across all 187 records:

| | |
|---|---|
| distinct `location.id` values | 157 |
| ids carrying **more than one distinct event** | **8** |
| within the 107-event direct-URL sample alone | **0** |

Roughly **5%** of venues repeat, and none at all inside the largest sample. The apparent
16 duplicate ids in the union are mostly the same event appearing in two samples.

*What this changes.* The venue registry still costs almost nothing and still eliminates
fuzzy name matching where it hits. But `PROJECT_HANDOVER.md` §7 calls it "the highest
cost/benefit ratio of anything remaining", and this sample does not support that. Its
value depends entirely on repeat rate over months rather than days — a theatre programmes
all season — and one day in mid-August cannot measure that. Treat the ranking as unproven
and re-measure after four weeks of live collection.

### 9.2 `Italia` is a gazetteer row, and every Italian address ends with it

`Italia` is a legitimate neighbourhood in Municipio II publishing to the `Nomentano` zone.
Every Italian postal address ends in `, Italia` or `, Italy`.

Matching gazetteer keys inside location fields therefore assigned **30 of 107 events** to
Nomentano, making it the busiest zone in Rome by a factor of six. Corrected by a new
`never_substring` list in `gazetteer.json`: those keys resolve only on an exact whole-field
match. Events placed fell from 46 to 31 — the 15 lost were all false.

*The general lesson*, which cost more than the fix: v1.4 assumed a location field "is a
place by construction" and applied no stoplist there. An address contains its own street,
city, province and country, and any of those can collide with a toponym.

### 9.3 Deterministic matching alone covers very little

Without the model: **31 of 107** events placed, and only **2** by exact match. 87 of 89
pages have no exact hit at all.

This is the expected shape — `location.streetAddress` was null in 94 of 107 — and it
confirms rather than undermines the design: the model does the geographic work, and the
deterministic layers exist to remove the cases where it would be confidently wrong. But it
also means the alias layer contributes almost nothing today, and the reject queue will be
dominated by alias misses exactly as `GAZETTEER_README.md` §5 predicts.

### 9.4 Guards fire on 18 of 107

`country_code_missing` 11, `centroid_detected` 5, `place_type_city` 2. Then
`ambiguous` 8 and `zone_not_published` 2. Around **17%** of the sample is stopped before
the model — a real volume, and a real weekly review load from day one.

### 9.5 Municipio X: zero events

Not one of the 107 resolved to Acilia, Ostia, Casal Palocco, Infernetto, Dragona,
Vitinia, Giardino di Roma or Torrino. Consistent with §1, and the single strongest argument
for the Facebook **Posts** channel: the neighbourhoods this project exists for do not
publish Facebook Events at all.

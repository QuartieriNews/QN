# Editorial filter — what counts as a locally useful event

Configuration in `gazetteer.json → editorial`. Release version: see `START_HERE.md`.

**Corrected in v1.4:** the three tests ran in the wrong order. `explicit_promotion` was
last and could not be reached by any promotion carrying a proper noun — which is most of
them. It is now a gate that runs first.

`not_an_event` has existed in the reject enum since v1.1 with no rule that could produce
it. A reject code with no rule is a counter that stays at zero while the thing it names
goes to the page. This file is the missing rule.

---

## The question

The Apify sample contains photo shoots, guided tours, cruises and commercial offerings
alongside real events. It also contains, in 11 of 107 records, recurring series with up to
52 occurrences.

The tempting shortcut is to filter on recurrence. It is wrong in both directions:

- It catches a pub's Thursday karaoke and **misses the same pub's Friday aperitivo with a
  DJ**, published as a one-off. Identical in nature, different in form.
- It discards the farmers' market every Saturday, the committee meeting every first Monday,
  the reading group at the library. These recur, and they are more valuable than almost any
  one-off, because they are the fabric of a neighbourhood and because a reader can *use*
  them. A past event helps nobody; a standing appointment does.

Recurrence is a signal. It is not the axis.

---

## The criterion

> Does this item have a reason to exist beyond the ordinary trading of whoever hosts it?

Three tests. **The order is load-bearing** — this is the part v1.3 got wrong.

### 0. Explicit promotion — the gate, runs first

Is a product or a service being sold, with the event as framing? Photo shoots, guided
tours, cruises, discount offers, *book your session*, *limited places, contact us*.

Classify `promotion` and stop.

**Why first.** v1.3 ran this test last, after identified content, on the reasoning that
identified content is the strongest signal. It is — for the question *occasion or routine*.
It is useless for the question *occasion or product*, because products have names too.
`"Rome Sunset Photography Experience by XYZ"` has a company, a title and a theme: under the
v1.3 order it stopped at test 1 as `local_interest` and never reached the exclusion. The
main editorial addition of v1.3 was neutralised by its own ordering.

A named seller is still a seller. The exclusion has to run before the inclusion.

### 1. Identified content — dominant, among items that pass the gate

Is there a proper noun or a specific subject? A band, an author, a speaker, a title, a
theme, a date that means something.

**If yes, it is local interest.** A named band playing on Friday in a neighbourhood pub
qualifies — free entry or not, and whether or not that pub books a band every Friday. That
band plays tomorrow and then never again, and in a low-density area it is exactly the
content no other site aggregates.

This test decides the large majority of what survives the gate.

### 1.5 Community organiser — sufficient on its own

Is the organiser a community body? A neighbourhood committee, a parish, an association, a
school, a library, a social centre, the municipio.

**If yes, it is local interest, whatever the content.** *Assemblea del comitato di
quartiere* and *mercatino della parrocchia* name no band and no author. They fail test 1 on
a literal reading, and a monthly one could then have been read as routine by test 2 — which
would discard exactly the items this site exists to surface.

This test also gives `organizer_type` a definition. v1.4 listed it among the
`editorial_basis` values and never said when to use it, which would have produced a field
nobody could compare across weeks.

### 2. Substitutability — secondary

Only when test 1 finds nothing. Is this item distinguishable from the same venue's item
last week?

`Karaoke`, `aperitivo con DJ`, `musica dal vivo` with no act named — no. It is the normal
offering of the place. Classify `commercial_routine`.

### Price is not a criterion, in either direction

Free does not make an item an event; a ticket does not disqualify one. A five-euro concert
is a concert. Do not reintroduce `paidContent` as a signal — it was `false` on all 187
measured records, including a ticketed concert with a live purchase link.

---

## Output contract

Three fields, all returned by the same call.

```json
{
  "editorial_class": "local_interest",
  "editorial_basis": "identified_content",
  "content_type": "event"
}
```

**`editorial_class`** — `local_interest` · `commercial_routine` · `promotion` · `uncertain`

`uncertain` must exist and must be used. A classifier that always decides produces nothing
to review, only silent errors — the same reason `publication_zone` is allowed to be empty.
An `uncertain` item goes to the queue with `reject_reason = editorial_uncertain`; it is not
discarded.

**`editorial_basis`** — one value, and each one names the step that decided:

| Value | Set when |
|---|---|
| `explicit_promotion` | Excluded by the gate (step 0) |
| `identified_content` | Passed on a proper noun or a specific subject (step 1) |
| `organizer_type` | Passed because the organiser is a community body (step 1.5) |
| `venue_pattern` | Classified `commercial_routine` on substitutability (step 2) |
| `no_signal` | Nothing to go on. Normally accompanies `uncertain` |

Why the classifier decided. It makes the queue sortable by cause, and after a few weeks it
shows which judgements are reliable enough to promote to a deterministic rule — the same
mechanism by which the gazetteer fattens on its errors.

**`content_type`** — `event` · `recurring_appointment` · `course`

`course` is a placeholder for a real gap. A ten-lesson yoga course, a theatre workshop, an
Italian class run by an association: they pass test 1, they are not promotion, and they are
not events in the ordinary sense. How they are displayed is undecided. What matters today
is that they are not discarded indistinguishably from a cruise, because a decision made
later cannot recover items thrown away now.

---

## Run it as its own pass

Not merged into the geography prompt. Two judgements with different error rates must be
countable separately — invariant I5, applied to a second axis. Merged, a fall in the weekly
number cannot be attributed to either.

---

## Structural signals, and their proper weight

These narrow the field before the model is asked. None of them decides alone.

| Signal | Reading |
|---|---|
| `occurrence_count` | **Record it. Do not act on it yet.** v1.3 asserted a threshold of ~20 and a community range of 8–12 dates. Neither came from the data: the sample has 11 series in 107 records, 8 `WEEKLY` and 3 `CUSTOM`, and none of them has been classified. Correlate the count against the human decisions in the review archive after a few weeks, then decide whether it is a usable prior. |
| `eventFrequency: CUSTOM` | Leans towards a real calendar. |
| `venue_nature` from the venue registry | Context, not verdict. See below. |
| `ticketsInfo.buyUrl` present | Neutral. The only reliable tickets field, and not evidence either way. |

### `venue_nature` is a prior, not a shortcut

The venue registry gains `venue_nature`: `community` · `cultural` · `commercial` ·
`unknown`. It is passed to the classifier as context.

It is tempting to make it a shortcut — judge the pub once, skip 52 calls. Do not, in the
general case: a neighbourhood pub hosts both its ordinary programming and real gigs, and a
permanent verdict on the venue discards the gigs.

Only the extremes shortcut, and both are human acts:

- **whitelist** — parish, committee, library, association, school, municipio premises.
  Everything from here is local interest. A parish hall does not need its bingo night
  re-judged monthly.
- **blacklist** — earned, not assumed: three `promotion` classifications with no
  `local_interest` in between, then a person sets it.

Everything in the middle — most neighbourhood venues — is judged each time. Those calls are
cheap and they are where the value is.

---

## Prompt text

```
EDITORIAL CLASSIFICATION

Decide whether this item is worth publishing on a neighbourhood news page.

The question: does this item have a reason to exist beyond the ordinary trading of
whoever is hosting it?

Apply these tests in this order. The order matters.

0. PROMOTION — is a product or a service being sold, with the event as framing?
   Photo shoots, guided tours, cruises, boat trips, discount offers, "book your
   session", "limited places, contact us". If yes, classify promotion and stop.
   Do this FIRST. A promotion often has a company name, a title and a theme, so
   checking for those before checking for selling would let it through.

1. IDENTIFIED CONTENT — is there a proper noun or a specific subject? A band, an
   author, a speaker, a title, a theme. If yes, classify local_interest and stop.
   A named band in a small pub qualifies. Free entry or a ticket makes no
   difference.

1b. COMMUNITY ORGANISER — is the organiser a neighbourhood committee, a parish, an
   association, a school, a library, a social centre or the municipio? If yes,
   classify local_interest even if the content is generic. "Assemblea del comitato
   di quartiere" and "mercatino della parrocchia" belong on the page.

2. SUBSTITUTABILITY — only if test 1 found nothing. Could this item be swapped with
   the same venue's item from last week without anyone noticing? "Karaoke", "live
   music", "aperitivo with DJ" with no act named: yes, it could. Classify
   commercial_routine.

If you cannot tell, classify uncertain. Uncertain is a correct answer and a person
will look at it. Do not guess in order to produce a verdict.

Note: a recurring item is NOT automatically routine. A weekly market, a monthly
committee meeting and a library reading group are among the most useful items on
the page. Recurrence tells you nothing on its own — apply test 1.

Return, and nothing else:

  editorial_class   local_interest | commercial_routine | promotion | uncertain
  editorial_basis   identified_content | organizer_type | venue_pattern |
                    explicit_promotion | no_signal
  content_type      event | recurring_appointment | course

  course = enrolment-based and multi-session (a language course, a theatre
  workshop). Classify it by the tests above like anything else; content_type only
  records what kind of thing it is.

Do not explain your reasoning.
```

---

## Calibration, before it goes live

Hand-classify 30 items from the 107-event sample. Run the prompt on the same 30. Read the
disagreements.

**What this establishes and what it does not.** It tells you whether the criterion is
written clearly — a question about the prompt, not about the model — and the disagreements
are the examples to add to the prompt. It does **not** validate the filter against a normal
Roman calendar: the 107 records are from mid-August and are the same items the criterion
was written while looking at. Treat it as a clarity check, half a day, before any of this
is wired in. Real validation is the weekly discarded sample, over time.

---

## Start wide

Start permissive and tighten on evidence.

In a low-density area a strict filter empties the block, and there is no signal that it has
happened. Set the initial bar at *exclude only what is clearly the ordinary programming of
a commercial venue, or clearly a product being sold*. Everything else publishes. Tighten
only if the published sample shows commercial noise.

---

## The asymmetry that makes this dangerous

A geographic error puts an event on the wrong page. Visible, correctable, and the queue
shows it.

An error here makes the event **disappear**. The reject queue shows what the filter
excluded — it cannot show what it excluded *wrongly*. The parish sagra held at the oratory
bar, classified `commercial_routine`, is gone and nothing anywhere indicates that it should
not be.

This is why the weekly review samples **ten discarded items** alongside the twenty published
ones, with one question: *was this genuinely not worth publishing?* It is the only sensor
this filter has, and without it the filter is unmeasured for as long as it runs.

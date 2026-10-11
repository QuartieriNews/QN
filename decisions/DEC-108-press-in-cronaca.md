# DEC-108 — Role of newspapers in the Cronaca pipeline

Status: DECIDED for the MVP (11 October 2026). The posture for the public launch, as a
registered testata, is left to a later decision that will supersede this one.

Question: may the Cronaca pipeline use local newspapers (RomaToday, Il Messaggero, Abitare
a Roma…), and if so as what? The baseline (v0.6 §2.D) builds Cronaca on six official
sources only. On 9 October 2026 the owner kept "Solo fonti ufficiali" for the June table.
On 10 October the owner asked to measure how many facts the press reports and through
which outlets, and how an AI can reach those sources lawfully. Analysis and June
measurements: `docs/sources/CRONACA_PROCESSO_2026-10.md`.

Options presented:

- **A. Official sources only.** No change. The press is not read. The gap to one Cronaca
  item per page is closed with more official channels (press lists of the Questura,
  Carabinieri, Vigili del Fuoco, Polizia Locale and Procura, which need a registered
  testata) and with the thin-page fallback (DEC-006).
- **B. Press as a discovery signal.** Title, date and link from channels that the outlet's
  robots.txt allows. The signal opens a case; nothing is published until an official
  source confirms the fact. QN never publishes press text.
- **C. Press as an attributed source.** As B, and a fact reported by at least two
  independent outlets may be published without official confirmation, written in QN's own
  words with the outlets named and linked.
- **D. Licensed press content.** Agency or clipping-service licence that covers automated
  processing.

Names taken from newspapers (not covered by DEC-016, which concerns official sources):
A none; B automatic under conditions; C each name approved in a queue.

Recommendation (builder): A now, B after the registered testata and written permission
from the open outlets; C and D after the legal opinion (D12). For names, C for the first
month, then B if errors are rare.

Owner's words (chat, 11 October 2026):

> «in attesa di costruire un flusso veramente giornalistico quindi immagino che la ricerca
> delle fonti possa passare dall analisi ogni ora dei principali quotidiani, ogni notizia
> su Roma che interessa un quartiere viene salvata e appena la stessa notizia appare su un
> secondo notiziario, possiamo per il momento dare per scontato che ci sia stata un uscita
> stampa […] e creare un articolo nuovo che parla della notizia e che citi i giornali per
> quelle informazioni che sono esclusive dell articolo di una testata se ci sono dettagli
> unici.»

> «direi che B è la mia scelta. Aggiungo che il mio sito non uscira ancora come testata
> giornalistica e neanche sarà profit ma solamente un MVP noto a pochi quasi a nessuno e
> che quando sarò a rischio legale, sarà gia ampliamente cambiata la situazione del
> giornale, ci saranno collaboratori e sarà una testata. Pero per l MVP vorrei essere piu
> leggero»

Decision (MVP only):

1. **Press as an attributed source (option C), without waiting for the legal opinion.**
   News is collected every hour. A Rome fact that concerns a neighbourhood is kept; when a
   second outlet reports it, QN writes a new article in its own words. The article names
   and links the outlets. Details found in only one outlet are attributed to that outlet.
2. **Names from newspapers: option B.** A name is published when outlets of at least two
   different publishers report it, the person is an adult arrested or under
   investigation, the wording respects the presumption of innocence, and the second AI
   checks that name and role match in every source. The article attributes it ("secondo X
   e Y"). The name is updated or removed when the case changes or on request.

Limits that stay in the MVP. They are not a choice of rigour: the first comes from the
outlets' own reservations, the second from criminal law. Both apply whether or not the
site is a testata or for profit.

- Outlets that exclude AI agents or reserve text and data mining (RomaToday, Il
  Messaggero, ANSA, Corriere, Repubblica, Leggo, Today.it, Agenzia Nova) are read only as
  metadata (title, link, time) from a third-party index. They count as the second outlet
  and are linked, but QN's articles are written from open outlets and official sources.
- Identities of minors involved in criminal proceedings or as victims or witnesses, and of
  victims of sexual violence, are never published (art. 13 DPR 448/1988, art. 114 c.p.p.,
  art. 734-bis c.p.). The pipeline removes them; no queue is needed.

Builder recommendations for the MVP, not decided: article pages with names set to
`noindex` (a named person searching their own name is the realistic way a complaint
starts, and few readers do not lower that risk); a review of the MVP archive before the
public launch, since what is published now stays online then.

Impact: Cronaca stops depending only on the official websites. The June measure gives up to
387 facts instead of 177 (§4.5 of the analysis). Needs the hourly collector, the fact
grouping by outlet and the attribution rules in the writing step. DEC-016 is unchanged for
names in official sources.

Blocks: nothing for the MVP. The public launch needs the legal opinion on art. 101 l.
633/1941 (systematic reuse of news by a periodical for profit) and on names taken from
the press, and a new decision.

Decided by: Owner · Date: 11 October 2026 · Affected: baseline §2.D (Cronaca pipeline),
DEC-015, DEC-016 (extended to press-sourced names for the MVP), legal questions 4–6
(baseline §4.1), source registry.

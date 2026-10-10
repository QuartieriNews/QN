# DEC-108 — Role of newspapers in the Cronaca pipeline

Status: OPEN

Question: may the Cronaca pipeline use local newspapers (RomaToday, Il Messaggero, Abitare
a Roma…), and if so as what? The baseline (v0.6 §2.D) builds Cronaca on six official
sources only. On 9 October 2026 the owner kept "Solo fonti ufficiali" for the June table.
On 10 October the owner asked to measure how many facts the press reports and through
which outlets, and how an AI can reach those sources lawfully. Analysis and June
measurements: `docs/sources/CRONACA_PROCESSO_2026-10.md`.

Options:

- **A. Official sources only.** No change. The press is not read. The gap to one Cronaca
  item per page is closed with more official channels (press lists of the Questura,
  Carabinieri, Vigili del Fuoco, Polizia Locale and Procura, which need a registered
  testata) and with the thin-page fallback (DEC-006).
- **B. Press as a discovery signal.** Title, date and link from channels that the outlet's
  robots.txt allows (sitemaps, feeds, public APIs of outlets with no AI opt-out), or from
  licensed search and news APIs. The signal opens a case. Nothing is published until an
  official source confirms the fact (rule R-C02 a). QN never publishes press text.
- **C. Press as an attributed source.** As B, and a fact reported by at least two
  independent outlets may be published without official confirmation, written in QN's own
  words with the outlets named and linked (R-C02 b). Needs the legal opinion on
  articles 65, 101 and 43-bis of l. 633/1941. Needs explicit consent or a licence from
  every outlet that opts out of AI use or reserves text and data mining.
- **D. Licensed press content.** Agency or clipping-service licence that covers automated
  processing. Widest coverage, recurring cost.

Recommendation (builder): A now, B as the next step once two conditions hold: the
registered testata (which also opens the press lists of option A), and a written
permission from at least the open local outlets. C and D only after the legal opinion
(D12) and with a measured gain. Whatever is chosen, outlets that opt out of AI or reserve
TDM are not read by an automated agent without a licence.

Impact: A changes nothing. B adds a reading channel and a confirmation queue, but no new
publication rule. C changes the verification standard of DEC-015 for Cronaca and how
DEC-016 applies to names: DEC-016 covers names in official sources only. D is a budget
line.

Blocks: any adapter that reads newspapers, and the confirmation queue of option B. It
blocks neither the official-source pipeline nor its golden set.

Decided by: — · Date: — · Affected: baseline §2.D (Cronaca pipeline), DEC-015, DEC-016,
legal questions 4–6 (baseline §4.1), source registry.

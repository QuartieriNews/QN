# DEC-107 — Assigning one content item to two neighbourhood pages at a boundary

Status: DECIDED (16 October 2026): option B, double page at a boundary.

Question: when a place lies exactly where two QN pages meet (a street that *is* the
boundary, a square or park split between them), should the item be assigned to both
pages? The owner raised it on 9 October 2026: "in alcuni casi dove un luogo è
esattamente nella congiunzione di due aree potrebbe essere assegnato ad entrambe.
Rimane da valutare rischi ed opportunità".

Today the method says no: "Un'unica via con due possibili quartieri, senza il tratto,
produce D" (Metodo QN §10); M is for several real places, never for alternatives.

Options:

- **A. Never.** Boundary places stay D (or one page by majority). Simple, comparable with
  the 19 September benchmark; loses items that matter on both sides (in the blind test:
  via dei Cerchi, the Ardeatina at via della Fotografia).
- **B. Only by owner rule, place by place.** The doubt queue offers `slug1+slug2` for a
  place; the rule (`modo: doppia_confine`) is cited by every decision that uses it, and
  these presences are counted apart from full ones. Built and tested, unused until
  this entry is decided.
- **C. Automatic** for every street or zone touching two pages. Not recommended.

Opportunities: residents on both sides are really affected (a closed street, a
square, a park entrance); thin pages get content that is genuinely theirs; fewer items
lost to D.

Risks: coverage looks larger than it is (one item, two pages); a reader following
both pages sees it twice; precedent creep — every long street becomes a candidate,
which is option C by the back door; the comparison with the benchmark gets harder; a
reader may judge the item "not about my area" and trust the page less.

Recommendation (builder): B, with three limits — only places whose geometry is on or
across the boundary (not long streets: those stay "depends on the stretch"); boundary
presences reported in their own column of the matrix; a review after the first month
of real pages, looking at how many items each page receives through boundary rules.

Impact: B changes counts only where the owner writes a two-page decision; nothing
changes until then. Blocks: no work — the tools already accept and count the option;
it blocks only its use in the queue.

Decision (owner, 16 October 2026, review of pull request #15, question put by the builder
with the three options above): **B, double page at a boundary** — «Sì, doppia pagina ai
confini». A place whose geometry lies on or across the boundary between two QN pages may be
assigned to both through an owner rule (`modo: doppia_confine`), with the builder's three
limits: long streets stay "depends on the stretch"; boundary presences are reported in their
own column of the matrix; a review after the first month of real pages. Nothing changes until
the owner writes a two-page decision in the queue.

Follow-up (builder, separate work): remove the block on `doppia_confine` in
`tools/geo-assign/applica_decisioni.py` and `valida.py`, add the boundary column to the
matrix, update `PROTOCOLLO_REVISIONE.md` and `GEO_ASSEGNAZIONE_2026-10.md` §6.

Decided by: Owner · Date: 16 October 2026 · Affected: tools/geo-assign (applica_decisioni.py,
stage1.py, valida.py), matrix reporting, PROTOCOLLO_REVISIONE.md.

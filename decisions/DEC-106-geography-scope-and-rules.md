# DEC-106 — Geography: scope kept apart from place, and owner rules for doubtful places

Status: DECIDED (9 October 2026)

Question: after the blind test of 8 October (docs/sources/GEO_ASSEGNAZIONE_2026-10.md
§5), three points were raised to the owner: a desk opening its doors (identity-card open
day) — neighbourhood news or municipal news? A norm on the "centro storico" in the
planning sense — the Centro Storico page or city news? And who settles the raccordi
zone/place → QN page that the sources leave open?

Owner's words (chat, 9 October 2026):

- desk open day: "sono validi entrambi. Una notizia di un quartiere è anche una notizia
  nel municipio. Non capisco perché scegliere tra i due";
- "centro storico" norms: "direi cittadini";
- raccordi: "creare un processino che dove ci sono dei possibili dubbi, in un file o in
  un processo io assegno e diventa regola. Pian piano gli errori dovrebbero tendere
  allo 0".

Options considered: for the desk, page only (U) or level only (T) — the owner rejected
the choice itself; for the norms, the Centro Storico page, every page, or city news;
for the raccordi, the builder deciding case by case, or an owner-owned list of rules.

Rule:

1. **Scope is recorded apart from place.** Every geographic decision states its pages
   (where the fact happens, if anywhere) and its `livello_portata` — `quartiere`,
   `municipio`, `citta` — as two fields. A neighbourhood fact is also a municipal fact;
   neither erases the other. This is the same principle DEC-105 set for the people's
   territory ("the cited place yields both the Municipio and the quartiere").
   A service used in a place (desk open day, in-person enrolment) keeps the desk's page
   and has `livello_portata: municipio`.
2. **Norms on the "centro storico" in the planning sense are city news**
   (`livello_portata: citta`, no page). Whether city news is also *shown* on every
   neighbourhood page is a display question of the product, not an assignment, and it
   is not counted as neighbourhood coverage (Metodo QN §14).
3. **Doubtful places are settled by the owner once, then applied as rules.**
   `tools/geo-assign/dubbi.py` lists every doubt by place; the owner writes a decision
   in the queue; `applica_decisioni.py` turns it into a numbered rule in
   `tools/geo-assign/regole_geografiche.json`, which the tools apply and every
   decision cites. Rerunning `dubbi.py` measures how many doubts are left. A decision
   that changes where a *locality* goes (e.g. rione Monti) is a change to the owner's
   gazetteer table, rebuilt with `build_gazetteer.py`, never a rule: the gazetteer
   wins over every other file (AGENTS.md).

Recommendation recorded with the decision (builder): the seat of a sitting or of a
convocation is not a place where anyone goes for the fact, so it gives a level but no
page; only services actually used at the address take the page. Not yet confirmed by
the owner — if the owner wants convocations on the seat's page too, this entry is
superseded in that clause.

Impact: decisions carry one more field; the 126 blind decisions of 8 October predate
it (`valida.py --senza-livello`). Counts of municipal-level content with a page are
reported apart from neighbourhood-level content.

Blocks: nothing.

Decided by: Owner · Date: 9 October 2026 · Affected: tools/geo-assign (protocol,
validator, stage 1, rules), docs/sources/GEO_ASSEGNAZIONE_2026-10.md.

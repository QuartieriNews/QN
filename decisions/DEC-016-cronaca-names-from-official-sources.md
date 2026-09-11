# DEC-016 — Cronaca: operating rule on names present in official sources

Status: DECIDED

Question: how does QN treat the names of persons present in the press releases of
Polizia, Carabinieri and Procura, pending and after the legal opinion?

Options:
A. No identifier of natural persons until the opinion (Round 1).
B. **CHOSEN.** Automatic reproduction of names already present in an official source,
   with the procedural position unchanged and stated, verification by the second AI
   against the source, and manual review for minors, victims, witnesses, relatives,
   sensitive data and cases where the name is not essential.
C. Manual review of every item involving persons.
D. No Cronaca at launch.

Claude recommendation: Round 2 presented A–D as bridges without choosing; the Council's
reading remains "Cronaca with identifiers is a capability blocked until the opinion".
The owner chooses B as a declared risk assumption.

ChatGPT recommendation: the same.

## Rule

B is the operating rule of the MVP. It is a risk choice of the owner, not a general
legal opinion. The obligations applicable to the site and to sensitive cases remain to
be verified; incompatible obligations emerging from the opinion are adopted before the
affected capability is activated, and this rule is modified accordingly (DEC-014, "Legal
verifications and the launch").

Impact: makes legal questions 4, 5 and 6 of the Round 2 Reconciliation (§8) the most
urgent; requires as technical requirements a person flag with routing to the queue for
the sensitive categories, a `case_status` kept and visible, and per-item rectification
and suspension fields (DEC-020).

Blocks: nothing (this entry unblocks the Cronaca pipeline and the specification of the
fields above).

Decided by: Owner · Date: 11 September 2026 (Strategic Council Round 2 Reconciliation,
owner confirmation) · Affected: Cronaca pipeline, `docs/REVIEW_QUEUE.md`,
`docs/PROJECT_VISION.md` §6 (the named editorial responsibility stays with the legal
verification).

# DEC-002 — Colle del Sole ambiguity

Status: OPEN
Blocks: scoring of the geographic golden set

Question: the lookup key "Colle del Sole" matches two places (Municipio VI and
Municipio XI). Until decided, the alias lookup rejects rather than guesses.

Options:
A. Assign the key to the Municipio VI place; the other keeps a longer disambiguated alias.
B. Assign the key to the Municipio XI place; same in reverse.
C. Keep the key ambiguous permanently (always reject to queue; a human routes each).

Claude recommendation: decide from evidence, not preference — check which of the two
places actually produces events in the collected URLs; if only one does, it takes the
key (A or B accordingly). C only if both are genuinely active.

Impact: one lookup key; currently a guaranteed reject for any event at either place.

Decided by: — · Date: — · Affected: Rome_Neighbourhood_Gazetteer_EN.xlsx (then rebuild).

#!/usr/bin/env python3
"""
test_guards.py — the test that was missing from the v1.3 package.

    python test_guards.py

v1.3 verified that every guard fired on a record designed to trip it, and never that a
guard stayed silent on a valid one. That is how `name_coord_mismatch` shipped rejecting
"Teatro Argentina, Sala Squarzina": location.name is a venue name, and the rule read the
text after its last comma as if it were a country.

Both directions are checked here. The negative cases are the important half — a guard that
fires wrongly removes an item silently and irreversibly, and nothing downstream notices.
"""
import json
import sys
from pathlib import Path

from zone_distribution import build_index, guard_verdict, match_zone, norm

G = json.loads(Path("gazetteer.json").read_text(encoding="utf-8"))
INDEX = build_index(G)
STOPLIST = {norm(s) for s in G.get("free_text_stoplist", [])}
NEVER_SUB = {norm(s) for s in G.get("never_substring", [])}
GUARDS = G["guards"]

ROME = {"latitude": 41.89, "longitude": 12.47, "countryCode": "IT"}


def ev(**loc):
    base = dict(ROME)
    base.update(loc)
    return {"name": "Evento", "description": "", "location": base}


def verdict(e, registry_hit=False):
    """Tier A always; tier B only when the venue registry did not resolve the item."""
    v = guard_verdict(e, GUARDS, INDEX, tier="A")
    if v or registry_hit:
        return v
    return guard_verdict(e, GUARDS, INDEX, tier="B")


MUST_REJECT = [
    ("foreign city in venue name", ev(name="London, U.K."), "name_coord_mismatch"),
    ("foreign city, no comma", ev(name="Waterloo"), "name_coord_mismatch"),
    ("room number abroad", ev(name="Rim Park, Room 207", latitude=43.4, longitude=-80.5),
     "outside_rome"),
    ("city centroid", ev(name="Qualcosa", latitude=41.900859832764,
                         longitude=12.483275413513), "centroid_detected"),
    ("bare centroid", ev(name="Roma", latitude=41.9, longitude=12.5), "centroid_detected"),
    ("placeType CITY", ev(name="Roma", placeType="CITY"), "place_type_city"),
    ("outside the box", ev(name="Teatro", latitude=45.46, longitude=9.19), "outside_rome"),
    ("Italian city as a whole segment",
     ev(name="Florence, Tuscany, Italy"), "name_coord_mismatch"),
    ("composite foreign city field",
     ev(name="Some Venue", city="Rome, NY, United States"), "name_coord_mismatch"),
    ("null country code", ev(name="Bar Sport", countryCode=None), "country_code_missing"),
]

# The half v1.3 never wrote. Every one of these is a plausible real Rome record.
MUST_PASS = [
    ("venue with a room after the comma", ev(name="Teatro Argentina, Sala Squarzina")),
    ("municipal premises", ev(name="Casa del Municipio, Sala Consiliare")),
    ("venue with a street after the comma", ev(name="Libreria Tuba, Via del Pigneto 39")),
    ("venue named after a zone", ev(name="Palazzo dei Congressi, EUR")),
    ("floor in the name", ev(name="Centro Anziani, primo piano")),
    ("parish hall", ev(name="Parrocchia San Carlo da Sezze, salone")),
    ("plain venue", ev(name="Teatro del Lido di Ostia")),
    ("venue with an apostrophe", ev(name="Circolo Arci Sparwasser, Via del Pigneto")),
    ("Italian composite city field", ev(name="Sala X", city="Roma, Italia")),
    ("legitimate repeat venue", ev(name="Terme di Caracalla")),
    ("English word in an Italian venue name", ev(name="London Pub")),
    ("foreign word inside a longer name", ev(name="Bar America, Via Tuscolana")),
    ("Italian city inside a venue name", ev(name="Hotel Firenze Roma")),
]

# A venue the registry has already resolved must not be stopped by a tier-B suspicion.
REGISTRY_CASES = [
    ("resolved venue, null country code", ev(name="Bar Sport", countryCode=None), True, None),
    ("unresolved venue, null country code", ev(name="Bar Sport", countryCode=None), False,
     "country_code_missing"),
]

MATCHING = [
    ("exact field match", ev(name="Acilia"), "exact", "acilia"),
    ("contains, not exact", ev(name="Teatro Prati"), "field_contains", "prati"),
    ("stoplisted word in description",
     {"name": "Talent show", "description": "Alla ricerca di nuovi talenti, EUR 10 nei prati",
      "location": dict(ROME, name="Sala X")}, None, None),
    ("country suffix in a street address",
     {"name": "Concerto", "description": "",
      "location": dict(ROME, name="Via del Corso, 305, 00187 Roma RM, Italia")}, None, None),
    ("Italia as a whole field still resolves", ev(name="Italia"), "exact", "nomentano"),
    ("zone named in description",
     {"name": "Festa", "description": "Appuntamento ad Acilia con la banda",
      "location": dict(ROME, name="Centro Culturale")}, "text_contains", "acilia"),
]

failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label:<45} got={got!r}")
    if not ok:
        failures.append(f"{label}: expected {want!r}, got {got!r}")


print("\nGUARDS — must reject")
for label, e, want in MUST_REJECT:
    check(label, verdict(e), want)

print("\nGUARDS — must NOT reject (the half v1.3 was missing)")
for label, e in MUST_PASS:
    check(label, verdict(e), None)

print("\nGUARD ORDERING — tier B runs after the venue registry")
for label, e, hit, want in REGISTRY_CASES:
    check(label, verdict(e, registry_hit=hit), want)

print("\nMATCHING TIERS")
for label, e, want_tier, want_zone in MATCHING:
    zid, how, tier = match_zone(e, INDEX, STOPLIST, NEVER_SUB)
    check(label, (tier or None, zid or None), (want_tier, want_zone))

print("\nNORMALISATION — build and runtime must agree")
sys.path.insert(0, ".")
from build_gazetteer import norm as build_norm  # noqa: E402
for s in ["S. Angelo", "Tor de' Schiavi", "Città Test", "Conca d'Oro", "  EUR  "]:
    check(f"norm({s!r})", build_norm(s), norm(s))
check("no double spaces", "  " not in build_norm("S. Angelo"), True)

print(f"\n{'ALL PASS' if not failures else str(len(failures)) + ' FAILURE(S)'}")
for f in failures:
    print("  -", f)
sys.exit(1 if failures else 0)

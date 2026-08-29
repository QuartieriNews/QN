#!/usr/bin/env python3
"""
zone_distribution.py — how many of the 89 pages would actually have content.

    python zone_distribution.py sample.json
    python zone_distribution.py sample.json --resolved resolved.json --csv distribution.csv

This is the test to run before anything else is built. It costs nothing and it can
change the product: if supply is concentrated in Municipio I and II, thin pages need a
municipality-level fallback, and the developer needs to know that before starting.

INPUT
  sample.json   the raw Apify output (a JSON array of event objects), or a JSON object
                with an "items" key. The 107-event direct-URL sample is the right input.

  --resolved    optional. A JSON array of {"source_event_id": ..., "publication_zone": ...}
                produced by running the real resolver (guards + gazetteer + model) in n8n.
                Those values win; the deterministic pass below fills the rest.

WHAT IT DOES
  1. Runs the deterministic guards from gazetteer.json (bounding box, centroid blocklist,
     placeType CITY, name/coordinate tail check, countryCode null). These are the same
     checks the pipeline runs before the model.
  2. Deterministic name and alias matching, in two tiers — see MATCHING below.
  3. Counts per publication zone and prints every page, including the empty ones — the
     empty ones are the finding.

MATCHING — rewritten in v1.4
  A gazetteer key found in `location.name` is a place by construction. The same key found
  inside a description is a guess: `prati`, `talenti`, `eur` and `marconi` are ordinary
  Italian words, a price token and a surname. v1.2 guarded against this with a blunt
  `len(key) < 5` filter, which silently excluded EUR and AXA — two real zones, one of them
  in Municipio X — while still admitting every common word of five letters or more.

  Three tiers, counted and printed separately:
    exact           the whole normalised location field IS a gazetteer key. The ONLY tier
                    that matches the production resolver, which does exact matching.
    field_contains  a key found inside a location field. "Teatro Prati" lands in Prati this
                    way — usually right, but not the rule the pipeline runs. v1.3 called
                    this tier "strong" and told you to decide on it, which overstated it.
    text_contains   found in a title or description, with free_text_stoplist applied.

  Read exact as the floor and the total as the ceiling.

WHAT IT IS NOT
  Not the model. Without --resolved the unresolved bucket will be large, because
  location.streetAddress was null in 94 of 107 measured records. Read the output as a
  LOWER BOUND on coverage and an UPPER BOUND on how concentrated the supply is: every
  event the model later resolves lands in some zone, and on the measured samples that
  zone is disproportionately in Municipio I or II.
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


def norm(s):
    """Identical to build_gazetteer.norm(). Keep them identical: v1.3 did not, and the
    build's ambiguity guarantee was false as a result."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9 ]+", " ", s.casefold())
    return re.sub(r"\s+", " ", s).strip()


def load_events(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("items") or data.get("events") or data.get("data") or []
    if not isinstance(data, list):
        sys.exit("expected a JSON array of events")
    return data


def build_index(g):
    """lookup key -> set of publication_zone_id, over neighbourhood names, aliases and zone
    display names. This is the same key space build_gazetteer.py checks for ambiguity."""
    index = {}
    for n in g["neighbourhoods"]:
        keys = [n["name_display"]] + [a.strip() for a in n["aliases"].split("|") if a.strip()]
        for k in keys:
            index.setdefault(norm(k), set()).add(n["publication_zone_id"])
    for z in g["publication_zones"]:
        index.setdefault(norm(z["name_display"]), set()).add(z["publication_zone_id"])
    return index


def guard_verdict(ev, guards, index=None, tier="A"):
    """Tier A: is the coordinate usable at all. Tier B: is the record suspicious.

    v1.3 ran both before the venue registry, which meant a venue a person had already
    resolved stayed blocked forever if its records kept arriving with countryCode = null.
    This script has no registry, so it runs A then B and says so in the output."""
    loc = ev.get("location") or {}
    lat, lng = loc.get("latitude"), loc.get("longitude")
    has_coords = lat is not None and lng is not None

    if tier == "A":
        if (loc.get("placeType") or "").upper() == "CITY":
            return "place_type_city"
        if not has_coords:
            return None
        tol = guards["centroid_blocklist"].get("tolerance_degrees", 1e-6)
        for blat, blng in guards["centroid_blocklist"]["coordinates"]:
            if abs(lat - blat) < tol and abs(lng - blng) < tol:
                return "centroid_detected"
        bb = guards["rome_bbox"]
        if not (bb["min_lat"] <= lat <= bb["max_lat"]
                and bb["min_lng"] <= lng <= bb["max_lng"]):
            return "outside_rome"
        return None

    # tier B — suspicion. Skipped entirely when a venue registry hit resolved the item.
    if not has_coords:
        return None
    g = guards["name_coordinate_mismatch"]

    # location.city IS hierarchical and composite: allowlist on the tail after the comma.
    city = loc.get("city")
    if city and "," in str(city):
        accepted = {norm(x) for x in g["rule_location_city"]["accepted_tails"]}
        tail = norm(str(city).rsplit(",", 1)[1])
        if tail and tail not in accepted and tail not in (index or {}):
            return "name_coord_mismatch"

    # location.name is a VENUE name, not an address. No tail parsing: the tail is usually a
    # room or a floor. Blocklist of foreign markers as whole words, failing open.
    name = loc.get("name")
    if name:
        markers = {norm(m) for m in g["rule_location_name"]["foreign_place_markers"]}
        # whole comma-delimited segments only. A substring test rejects "London Pub".
        segments = [norm(s) for s in str(name).split(",")]
        if any(s in markers for s in segments if s):
            return "name_coord_mismatch"

    if loc.get("countryCode") in (None, ""):
        return "country_code_missing"
    return None


def match_zone(ev, index, stoplist, never_sub=frozenset()):
    """Returns (zone_id, how, tier) with tier in 'exact', 'field_contains', 'text_contains'.

    v1.3 reported two tiers and called the location-field one 'strong', which overstated
    it: a substring hit on `location.name = "Teatro Prati"` counted the same as an exact
    alias match, while the production resolver does exact matching only. Only the `exact`
    tier is comparable to what the pipeline will actually do."""
    loc = ev.get("location") or {}
    loc_fields = [loc.get("name"), loc.get("streetAddress"), loc.get("address"),
                  ev.get("address")]
    text_fields = [ev.get("name"), ev.get("description")]

    # 1. exact — the whole normalised field IS a key. This is the production rule.
    for f in loc_fields:
        k = norm(f)
        if k and k in index:
            hits = index[k]
            return (next(iter(hits)), "matched", "exact") if len(hits) == 1 \
                else (None, "ambiguous", "exact")

    def scan(fields, keys):
        hits = set()
        for f in fields:
            text = f" {norm(f)} "
            if not text.strip():
                continue
            for key in keys:
                if f" {key} " in text:
                    hits |= index[key]
        return hits

    # never_sub keys are excluded from EVERY substring tier. The exact pass above still
    # resolves them: "Italia" as a whole location.name is a real hit, ", Italia" at the end
    # of a street address is not. Measured: this one key put 30 of 107 events on Nomentano.
    all_keys = [k for k in index if k not in never_sub]
    safe_keys = [k for k in all_keys if k not in stoplist]

    for tier, fields, keys in (("field_contains", loc_fields, all_keys),
                               ("text_contains", text_fields, safe_keys)):
        hits = scan(fields, keys)
        if len(hits) == 1:
            return next(iter(hits)), "matched", tier
        if len(hits) > 1:
            return None, "ambiguous", tier
    return None, "unresolved", ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sample")
    ap.add_argument("--gazetteer", default="gazetteer.json")
    ap.add_argument("--resolved", default=None)
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()

    g = json.loads(Path(args.gazetteer).read_text(encoding="utf-8"))
    index = build_index(g)
    stoplist = {norm(s) for s in g.get("free_text_stoplist", [])}
    never_sub = {norm(s) for s in g.get("never_substring", [])}
    zones = [z for z in g["publication_zones"] if z["is_page"]]
    by_id = {z["publication_zone_id"]: z for z in g["publication_zones"]}

    override = {}
    if args.resolved:
        for r in json.loads(Path(args.resolved).read_text(encoding="utf-8")):
            zid = r.get("publication_zone_id")
            if not zid and r.get("publication_zone"):
                for z in g["publication_zones"]:
                    if z["name_display"] == r["publication_zone"]:
                        zid = z["publication_zone_id"]
            if zid:
                override[str(r.get("source_event_id") or r.get("id"))] = zid

    events = load_events(args.sample)
    counts, exact_counts, buckets = Counter(), Counter(), Counter()

    for ev in events:
        eid = str(ev.get("id") or ev.get("eventId") or ev.get("source_event_id") or "")
        if eid in override:
            counts[override[eid]] += 1
            exact_counts[override[eid]] += 1
            buckets["resolved (supplied)"] += 1
            continue
        verdict = (guard_verdict(ev, g["guards"], index, tier="A")
                   or guard_verdict(ev, g["guards"], index, tier="B"))
        if verdict:
            buckets[f"guard: {verdict}"] += 1
            continue
        zid, how, tier = match_zone(ev, index, stoplist, never_sub)
        if zid:
            if by_id[zid]["is_page"]:
                counts[zid] += 1
                if tier == "exact":
                    exact_counts[zid] += 1
                buckets[f"resolved ({tier})"] += 1
            else:
                buckets["zone_not_published"] += 1
        else:
            buckets[how if how != "unresolved" else "unresolved"] += 1

    rows = sorted(zones, key=lambda z: (-counts[z["publication_zone_id"]], z["name_display"]))
    width = max(len(z["name_display"]) for z in rows)

    print(f"\n{len(events)} events in {args.sample}\n")
    print("EVENTS PER PUBLICATION ZONE          (total / of which exact)")
    print("-" * (width + 30))
    for z in rows:
        zid = z["publication_zone_id"]
        n, s = counts[zid], exact_counts[zid]
        print(f"{z['name_display']:<{width}}  {n:>4} {s:>4}   {'#' * min(n, 40)}")

    empty = sum(1 for z in zones if counts[z["publication_zone_id"]] == 0)
    one = sum(1 for z in zones if counts[z["publication_zone_id"]] == 1)
    empty_exact = sum(1 for z in zones if exact_counts[z["publication_zone_id"]] == 0)
    placed = sum(counts.values())
    print("-" * (width + 30))
    print(f"pages with 0 events        : {empty} of {len(zones)}")
    print(f"pages with 0 EXACT events  : {empty_exact} of {len(zones)}")
    print(f"pages with 1 event         : {one}")
    print(f"events placed              : {placed} of {len(events)}")
    print("\nUNPLACED")
    for k, v in buckets.most_common():
        if k.startswith("resolved"):
            continue
        print(f"  {k:<28} {v}")
    print("\nPLACED, BY TIER")
    for k, v in buckets.most_common():
        if k.startswith("resolved"):
            print(f"  {k:<28} {v}")
    print("\n  exact          = the whole location field IS a gazetteer key. This is the only\n"
          "                   tier that matches what the production resolver does.\n"
          "  field_contains = a key found INSIDE a location field ('Teatro Prati'). Often\n"
          "                   right, but not the production rule — treat as indicative.\n"
          "  text_contains  = found in a title or description, free-text stoplist applied.\n"
          "                   The loosest tier and the one to discount.\n"
          "\n  Read the exact column as the floor and the total as the ceiling. Neither is\n"
          "  the answer: without --resolved this script does not run the model, and the\n"
          "  sample it is usually run on comes from mid-August.")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["publication_zone_id", "name_display", "primary_municipality",
                        "events", "events_strong"])
            for z in rows:
                zid = z["publication_zone_id"]
                w.writerow([zid, z["name_display"], z["primary_municipality"],
                            counts[zid], exact_counts[zid]])
        print(f"\nwrote {args.csv}")


if __name__ == "__main__":
    main()

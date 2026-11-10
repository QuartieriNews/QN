#!/usr/bin/env python3
"""Projection of canonical event files into the input of build_site.py.

Reads a folder of canonical event files (spec v2.5, canonical contract, schema_version
2.0) and writes the plain events JSON that build_site.py reads: {reference_date, events}.
The projection is derived when the pages are built and never stored in place of the
canonical fields (docs/pilota/CONTRATTI.md, section 2).

Dates in the projection are dates in Rome: every UTC instant is converted to
Europe/Rome before its day is taken (spec v2.5 T17).

    python tools/site/project_events.py --canonical <local copy of C Eventi/> \
        [--reference-date YYYY-MM-DD] --out <events.json>

The canonical files are not in the repository: they carry third-party titles (DEC-109).
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys
from zoneinfo import ZoneInfo

ROME = ZoneInfo("Europe/Rome")
SCHEMA_VERSION = "2.0"
GAZETTEER = os.path.join(os.path.dirname(__file__), "..", "..", "gazetteer", "gazetteer.json")


def parse_instant(instant):
    t = dt.datetime.fromisoformat(instant.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError(f"instant without an offset: {instant!r}")
    return t


def rome_date(instant):
    """The calendar day in Rome of a UTC instant ("2026-10-24T22:30:00Z" -> "2026-10-25")."""
    if not instant:
        return None
    return parse_instant(instant).astimezone(ROME).date().isoformat()


def next_occurrence_end(series, occurrences):
    """The end of the occurrence that next_occurrence points at, if it has one. An
    expired series (next_occurrence null) has none and drops out in publishable()."""
    if not series.get("next_occurrence"):
        return None
    nxt = parse_instant(series["next_occurrence"])
    for occ in occurrences or []:
        if occ.get("start_at_utc") and parse_instant(occ["start_at_utc"]) == nxt:
            return occ.get("end_at_utc")
    return None


def blocking_codes(gazetteer_path=GAZETTEER):
    """Reject codes that stop publication (gazetteer.json -> reject_reasons)."""
    g = json.load(open(gazetteer_path, encoding="utf-8"))
    return {r["code"] for r in g["reject_reasons"] if r["blocks_publication"]}


def publishable(doc, blocking):
    """Active and not stopped by a blocking reject. requires_review routes an item to
    the queue and does not gate publication (spec v2.5, operating model)."""
    if (doc.get("lifecycle") or {}).get("status") != "active":
        return False
    series = doc.get("series")
    if series and not series.get("next_occurrence"):
        # All occurrences past: drops out like a finished single event (Phase 3.4).
        return False
    if (doc.get("pilot") or {}).get("duplicate_of"):
        # A secondary copy of an event another source leads is never published alone
        # (DEC-025, rule 3); the element it duplicates carries the event.
        return False
    reason = (doc.get("quality") or {}).get("reject_reason")
    return reason is None or reason not in blocking


def project(doc):
    """One canonical file -> one item of build_site.py's events list."""
    event = doc.get("event") or {}
    series = doc.get("series")
    geo = doc.get("geography") or {}
    source = doc.get("source") or {}
    # An end the source did not give is an assumption (Phase 3.3): not shown.
    exact = event.get("date_precision") == "exact"
    if series:
        # A series is one item at its next occurrence, with that occurrence's end
        # (spec v2.5 Phase 3.4, T37; docs/WORKFLOW_FIXES.md 2.5).
        start = rome_date(series.get("next_occurrence"))
        end = rome_date(next_occurrence_end(series, doc.get("occurrences"))) if exact else None
    else:
        start = rome_date(event.get("start_at_utc"))
        end = rome_date(event.get("end_at_utc")) if exact else None
    cost = event.get("cost_type")
    return {
        "id": doc["content_id"],
        "title": (doc.get("article") or {}).get("title"),
        # A merged element publishes the link of the source that leads it (DEC-025 rule 1).
        "url": (doc.get("pilot") or {}).get("lead_url") or source.get("url"),
        "source": source.get("type"),
        "start": start,
        "end": end,
        "venue": event.get("venue"),
        "publication_zone_id": geo.get("publication_zone_id"),
        "municipality_code": geo.get("municipality_code"),
        "geo_level": geo.get("geo_level"),
        "editorial_class": (doc.get("editorial") or {}).get("editorial_class"),
        "content_type": doc.get("content_type"),
        "is_free": True if cost == "free" else False if cost == "paid" else None,
        "reported_by": [source.get("type")] if source.get("type") else [],
    }


def build(docs, reference_date, blocking):
    """The projection, plus counts of what was left out and why."""
    events, skipped = [], {"schema_version": 0, "not_publishable": 0}
    for doc in docs:
        if doc.get("schema_version") != SCHEMA_VERSION:
            skipped["schema_version"] += 1
        elif not publishable(doc, blocking):
            skipped["not_publishable"] += 1
        else:
            events.append(project(doc))
    events.sort(key=lambda e: (e["start"] or "9999", e["id"]))
    return {"reference_date": reference_date, "events": events}, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True, help="folder of canonical event files")
    ap.add_argument("--reference-date", default=dt.datetime.now(ROME).date().isoformat())
    ap.add_argument("--gazetteer", default=GAZETTEER)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    dt.date.fromisoformat(a.reference_date)
    if not os.path.isdir(a.canonical):
        # A missing folder must not look like an empty one (an empty site, no error).
        sys.exit(f"{a.canonical}: not a folder")
    docs, seen = [], {}
    out_path = os.path.realpath(a.out)
    for path in sorted(glob.glob(os.path.join(a.canonical, "*.json"))):
        if os.path.realpath(path) == out_path:
            # Our own output from an earlier run is not an input; a canonical file is,
            # and --out must never overwrite it.
            try:
                earlier = json.load(open(path, encoding="utf-8"))
            except (OSError, ValueError):
                earlier = None
            if not (isinstance(earlier, dict) and "events" in earlier and "content_id" not in earlier):
                sys.exit(f"{path}: --out would overwrite an input that is not an earlier projection")
            continue
        try:
            doc = json.load(open(path, encoding="utf-8"))
            if not isinstance(doc, dict) or not isinstance(doc.get("content_id"), str):
                raise ValueError("not a canonical file: no content_id")
            if doc.get("schema_version") == SCHEMA_VERSION:
                project(doc)  # fail here, with the file name, rather than mid-build
        except (OSError, ValueError, AttributeError, TypeError) as e:
            sys.exit(f"{path}: {e}")
        cid = doc["content_id"]
        if cid in seen:
            # One identity, one element (CONTRATTI.md, section 2): a duplicate is an error.
            sys.exit(f"{path}: content_id {cid} already in {seen[cid]}")
        seen[cid] = path
        docs.append(doc)
    out, skipped = build(docs, a.reference_date, blocking_codes(a.gazetteer))
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"{len(out['events'])} events, skipped {skipped}", file=sys.stderr)


if __name__ == "__main__":
    main()

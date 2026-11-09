#!/usr/bin/env python3
"""Executable acceptance for tools/site/project_events.py.

Rules under test: spec v2.5 T17 (UTC to Europe/Rome across the DST boundary), T37
(a series is one item at its next occurrence), Phase 3.3 (an assumed end is not
shown), the operating model (requires_review does not gate publication) and
gazetteer.json -> reject_reasons (only blocking codes stop an item). Every example is
invented (DEC-109).
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools", "site"))
import build_site as b  # noqa: E402
import project_events as p  # noqa: E402

BLOCKING = p.blocking_codes()

BASE = {
    "schema_version": "2.0",
    "content_id": "qn:roma:evt:facebook:111",
    "content_type": "event",
    "stream": "events",
    "article": {"title": "Evento inventato"},
    "event": {"start_at_utc": "2026-10-15T16:00:00Z", "end_at_utc": "2026-10-15T18:00:00Z",
              "date_precision": "exact", "venue": "Luogo inventato", "cost_type": "free"},
    "series": None,
    "source": {"type": "facebook_event", "url": "https://example.org/e/111"},
    "geography": {"publication_zone_id": "za", "municipality_code": "V", "geo_level": "zone"},
    "editorial": {"editorial_class": "local_interest"},
    "quality": {"requires_review": False, "reject_reason": None},
    "lifecycle": {"status": "active"},
}


def doc(**changes):
    d = copy.deepcopy(BASE)
    for path, value in changes.items():
        node = d
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    return d


def test_T17_autumn_dst_boundary():
    # 25 October 2026: CEST (+2) until 01:00 UTC, CET (+1) after.
    assert p.rome_date("2026-10-24T22:30:00Z") == "2026-10-25"
    assert p.rome_date("2026-10-25T00:30:00Z") == "2026-10-25"
    assert p.rome_date("2026-10-25T22:30:00Z") == "2026-10-25"
    assert p.rome_date("2026-10-25T23:30:00Z") == "2026-10-26"


def test_T17_spring_dst_boundary():
    # 29 March 2026: CET (+1) until 01:00 UTC, CEST (+2) after.
    assert p.rome_date("2026-03-28T22:30:00Z") == "2026-03-28"
    assert p.rome_date("2026-03-28T23:30:00Z") == "2026-03-29"
    assert p.rome_date("2026-03-29T21:30:00Z") == "2026-03-29"
    assert p.rome_date("2026-03-29T22:30:00Z") == "2026-03-30"


def test_T17_an_instant_without_offset_is_refused():
    try:
        p.rome_date("2026-10-15T16:00:00")
    except ValueError:
        return
    raise AssertionError("a naive instant was accepted")


def test_T17_projected_start_is_the_rome_day_not_the_utc_day():
    e = p.project(doc(event__start_at_utc="2026-10-24T22:30:00Z", event__end_at_utc="2026-10-24T23:30:00Z"))
    assert (e["start"], e["end"]) == ("2026-10-25", "2026-10-25"), e


def test_phase_3_3_assumed_end_is_not_shown():
    e = p.project(doc(event__date_precision="start_only"))
    assert (e["start"], e["end"]) == ("2026-10-15", None), e


def test_T37_series_is_one_item_at_its_next_occurrence():
    d = doc(content_id="qn:roma:evt:facebook:222-series",
            series={"is_series": True, "next_occurrence": "2026-10-31T23:15:00Z"})
    e = p.project(d)
    assert (e["id"], e["start"], e["end"]) == ("qn:roma:evt:facebook:222-series", "2026-11-01", None), e


def test_T37_series_takes_the_end_of_its_next_occurrence():
    d = doc(content_id="qn:roma:evt:facebook:333-series",
            series={"is_series": True, "next_occurrence": "2026-10-30T20:00:00Z"},
            occurrences=[{"start_at_utc": "2026-10-23T19:00:00.000Z", "end_at_utc": "2026-10-23T21:00:00Z", "status": "scheduled"},
                         {"start_at_utc": "2026-10-30T20:00:00.000Z", "end_at_utc": "2026-11-01T12:00:00Z", "status": "scheduled"}])
    e = p.project(d)
    assert (e["start"], e["end"]) == ("2026-10-30", "2026-11-01"), e
    e = p.project(dict(d, event=dict(d["event"], date_precision="start_only")))
    assert (e["start"], e["end"]) == ("2026-10-30", None), e


def test_T37_series_with_no_future_occurrence_drops_out():
    d = doc(series={"is_series": True, "next_occurrence": None})
    out, skipped = p.build([d], "2026-10-13", BLOCKING)
    assert out["events"] == [] and skipped["not_publishable"] == 1, (out, skipped)


def test_only_blocking_rejects_stop_an_item():
    assert "outside_rome" in BLOCKING and "no_image" not in BLOCKING
    docs = [doc(content_id="a", quality__reject_reason="outside_rome"),
            doc(content_id="b", quality__reject_reason="no_image"),
            doc(content_id="c", quality__requires_review=True)]
    out, skipped = p.build(docs, "2026-10-13", BLOCKING)
    assert [e["id"] for e in out["events"]] == ["b", "c"], out
    assert skipped == {"schema_version": 0, "not_publishable": 1}, skipped


def test_inactive_and_other_schema_versions_are_left_out():
    docs = [doc(content_id="a", lifecycle__status="removed"), doc(content_id="b", schema_version="1.4")]
    out, skipped = p.build(docs, "2026-10-13", BLOCKING)
    assert out["events"] == [] and skipped == {"schema_version": 1, "not_publishable": 1}, (out, skipped)


def test_cost_type_maps_to_is_free():
    assert p.project(doc(event__cost_type="free"))["is_free"] is True
    assert p.project(doc(event__cost_type="paid"))["is_free"] is False
    assert p.project(doc(event__cost_type="donation"))["is_free"] is None
    assert p.project(doc(event__cost_type="unknown"))["is_free"] is None


def test_a_missing_canonical_folder_is_an_error():
    import subprocess
    tool = os.path.join(os.path.dirname(__file__), "..", "tools", "site", "project_events.py")
    r = subprocess.run([sys.executable, tool, "--canonical", "/nonexistent/C Eventi", "--out", os.devnull],
                       capture_output=True, text=True)
    assert r.returncode != 0 and "not a folder" in r.stderr, (r.returncode, r.stderr)


def test_projection_feeds_the_prototype():
    zones = {"za": {"publication_zone_id": "za", "name_display": "Za", "primary_municipality": "V"}}
    out, _ = p.build([doc()], "2026-10-13", BLOCKING)
    assert out["reference_date"] == "2026-10-13"
    f, g, s, u, levels = b.events_block("za", zones, out["events"], "2026-10-13", "2026-10-27")
    assert [e["id"] for _, e in s] == ["qn:roma:evt:facebook:111"], s


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok", t.__name__)
    print(f"{len(tests)} passed")

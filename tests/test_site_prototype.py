#!/usr/bin/env python3
"""Executable acceptance for tools/site/build_site.py (prototype rules only).

Rules under test come from spec v2.5 Phase 2 (Events block) as restated in
tools/site/README.md; this is not a test of the final platform.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools", "site"))
import build_site as b  # noqa: E402

ZONES = {
    "za": {"publication_zone_id": "za", "name_display": "Za", "primary_municipality": "V"},
    "zb": {"publication_zone_id": "zb", "name_display": "Zb", "primary_municipality": "V"},
    "zc": {"publication_zone_id": "zc", "name_display": "Zc", "primary_municipality": "VI"},
}
REF, END = "2026-10-13", "2026-10-27"


def ev(i, zone, mun, level="zone", start="2026-10-15", end=None, venue=None, rep=("a",), cls="local_interest"):
    return {"id": i, "title": i, "url": "", "source": "x", "start": start, "end": end, "venue": venue,
            "publication_zone_id": zone, "municipality_code": mun, "geo_level": level,
            "editorial_class": cls, "content_type": "event", "is_free": None, "reported_by": list(rep)}


def ids(featured, groups, singles):
    return sorted([e["id"] for _, e in featured] + [e["id"] for _, es in groups for _, e in es] + [e["id"] for _, e in singles])


def test_zone_first_then_municipality_then_city():
    evs = [ev("z1", "za", "V"), ev("m1", "zb", "V"), ev("m2", "zb", "V"), ev("c1", None, None, "city"), ev("o1", "zc", "VI")]
    f, g, s, u, levels = b.events_block("za", ZONES, evs, REF, END)
    assert levels == ["zona", "municipio", "città"], levels
    assert ids(f, g, s) == ["c1", "m1", "m2", "z1"], ids(f, g, s)  # other municipality never leaks in


def test_enough_in_zone_stops_at_zone():
    evs = [ev(f"z{i}", "za", "V") for i in range(6)] + [ev("m1", "zb", "V")]
    f, g, s, u, levels = b.events_block("za", ZONES, evs, REF, END)
    assert levels == ["zona"], levels
    assert "m1" not in ids(f, g, s)


def test_window_14_days_and_multi_day_overlap():
    evs = [ev("in", "za", "V", start="2026-10-27"), ev("out", "za", "V", start="2026-10-28"),
           ev("span", "za", "V", start="2026-10-01", end="2026-10-14"), ev("past", "za", "V", start="2026-10-01", end="2026-10-12")]
    f, g, s, u, _ = b.events_block("za", ZONES, evs, REF, END)
    got = ids(f, g, s)
    assert "in" in got and "span" in got and "out" not in got and "past" not in got, got


def test_venue_collapses_above_three():
    evs = [ev(f"v{i}", "za", "V", venue="Teatro", start=f"2026-10-{14 + i}") for i in range(4)] + \
          [ev(f"w{i}", "za", "V", venue="Bar", start=f"2026-10-{14 + i}") for i in range(3)]
    f, g, s, u, _ = b.events_block("za", ZONES, evs, REF, END)
    assert [v for v, _ in g] == ["Teatro"] and len(g[0][1]) == 4
    assert len(s) == 3


def test_featured_is_multi_channel():
    evs = [ev("one", "za", "V"), ev("two", "za", "V", rep=("a", "b"))]
    f, g, s, u, _ = b.events_block("za", ZONES, evs, REF, END)
    assert [e["id"] for _, e in f] == ["two"]
    assert [e["id"] for _, e in s] == ["one"]


def test_non_local_classes_excluded_and_undated_listed():
    # the classes are the real ones of prompts/EDITORIAL_FILTER.md as they occur in the data
    evs = [ev("ad", "za", "V", cls="promotion"), ev("shop", "za", "V", cls="commercial_routine"),
           ev("unc", "za", "V", cls="uncertain"), ev("nd", "za", "V", start=None)]
    f, g, s, u, _ = b.events_block("za", ZONES, evs, REF, END)
    assert ids(f, g, s) == [] and [e["id"] for e in u] == ["nd"]


def test_every_item_carries_its_zone_label():
    # README: "ogni voce porta l'etichetta della propria zona" — the current zone's items too (cycle 1, item 3)
    html_zone = b.li("zona", ev("z1", "za", "V"), ZONES, "za")
    html_mun = b.li("municipio", ev("m1", "zb", "V"), ZONES, "za")
    html_city = b.li("città", ev("c1", None, None, "city"), ZONES, "za")
    assert '<span class="tag">Za</span>' in html_zone, html_zone
    assert '<span class="tag">Zb</span>' in html_mun, html_mun
    assert '<span class="tag">Roma</span>' in html_city, html_city


def test_featured_item_does_not_uncollapse_its_venue():
    # 4 dates at one venue, one of them featured: the venue still collapses (cycle 1, item 4)
    evs = [ev(f"v{i}", "za", "V", venue="Teatro", start=f"2026-10-{14 + i}", rep=("a", "b") if i == 0 else ("a",)) for i in range(4)]
    f, g, s, u, _ = b.events_block("za", ZONES, evs, REF, END)
    assert [e["id"] for _, e in f] == ["v0"], f
    assert [v for v, _ in g] == ["Teatro"] and sorted(e["id"] for _, e in g[0][1]) == ["v1", "v2", "v3"], g
    assert s == [], s



def test_neighbourhood_events_join_the_municipality_fallback():
    # PROMPT_GEO_BLOCK.md: the events block writes geo_level neighbourhood or zone; a
    # neighbourhood-level event elsewhere in the municipality is a municipio item, not lost (cycle 4)
    evs = [ev("z1", "za", "V"), ev("n1", "zb", "V", level="neighbourhood"), ev("c1", None, None, "city")]
    f, g, s, u, levels = b.events_block("za", ZONES, evs, REF, END)
    assert levels == ["zona", "municipio", "città"], levels
    assert ids(f, g, s) == ["c1", "n1", "z1"], ids(f, g, s)

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok", t.__name__)
    print(f"{len(tests)} passed")

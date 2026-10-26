#!/usr/bin/env python3
"""Executable acceptance for tools/fonti/valida_eventi.py (quality checks on the events page data).

- T-VE-1  dates: a missing or unreadable start, an end before the start and an event already over
          are grave; a start beyond the horizon and a period longer than 31 days are warnings.
- T-VE-2  time: a time that is not HH:MM, or 00:00, is a warning; a normal time passes.
- T-VE-3  geography: a page that is not a gazetteer page and a municipio outside I-XV are grave;
          a page in another municipio (outside its spans) and a row without a page are warnings.
- T-VE-4  link: a missing or non-http link is grave; a Roma Today link outside the Roma Today
          channel is grave (DEC-026); the same link in its own channel passes.
- T-VE-5  privacy: an email or a phone number in a published field is grave; a postcode, a year
          and a time are not phone numbers.
- T-VE-6  titles: an empty title is grave; a title that reads as a post (invitation, date first,
          cut with an ellipsis, link or hashtag, too long, emoji) is a warning; a plain name passes.
- T-VE-7  duplicates: the same title, day and page as an earlier row is a warning on the later row.
- T-VE-8  report: counts per rule and per channel, failing rows by index; --out refused inside the
          repository (rows carry titles, DEC-109); --severo exits 1 on a grave row.

Run:  python tests/test_valida_eventi.py   (exit 0 and "ALL PASS" required)
"""
import json
import os
import sys
import tempfile
from datetime import date

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "fonti"))
import valida_eventi as ve  # noqa: E402

checks = 0
failures = 0


def check(label, actual, expected):
    global checks, failures
    checks += 1
    if actual == expected:
        print(f"  ok   {label}")
    else:
        failures += 1
        print(f"  FAIL {label}\n       expected {expected!r}\n       got      {actual!r}")


OGGI = date(2026, 10, 26)
ZONES = {"monteverde": {"publication_zone_id": "monteverde", "primary_municipality": "XII", "spans_municipalities": ""},
         "eur": {"publication_zone_id": "eur", "primary_municipality": "IX", "spans_municipalities": "IX;VIII"}}
BASE = {"t": "Concerto d'autunno", "d1": "2026-11-02", "d2": None, "ora": "21:00", "luogo": "Teatro Prova", "ind": "Via Prova 1",
        "org": "Associazione Prova", "url": "https://prova.it/concerto", "src": "sito della fonte", "z": "monteverde", "m": "XII"}


def codes(**kw):
    return ve.check_row(dict(BASE, **kw), OGGI, 90, ZONES)


def main():
    print("T-VE-1 dates")
    check("T-VE-1 a clean row breaks no rule", codes(), [])
    check("T-VE-1 start missing", "V-DATA-1" in codes(d1=None), True)
    check("T-VE-1 start unreadable", "V-DATA-1" in codes(d1="sabato prossimo"), True)
    check("T-VE-1 end before start", "V-DATA-2" in codes(d2="2026-11-01"), True)
    check("T-VE-1 event already over", "V-DATA-3" in codes(d1="2026-10-20", d2="2026-10-25"), True)
    check("T-VE-1 a period still running is not over", "V-DATA-3" in codes(d1="2026-10-01", d2="2026-10-30"), False)
    check("T-VE-1 start beyond the horizon is a warning", "V-DATA-4" in codes(d1="2027-03-01"), True)
    check("T-VE-1 a period longer than 31 days is a warning", "V-DATA-5" in codes(d1="2026-10-01", d2="2026-12-31"), True)

    print("T-VE-2 time")
    check("T-VE-2 time not HH:MM", "V-ORA-1" in codes(ora="21"), True)
    check("T-VE-2 midnight placeholder", "V-ORA-1" in codes(ora="00:00"), True)
    check("T-VE-2 no time is fine", "V-ORA-1" in codes(ora=None), False)

    print("T-VE-3 geography")
    check("T-VE-3 page not in the gazetteer is grave", "V-GEO-1" in codes(z="zona-inventata"), True)
    check("T-VE-3 municipio outside I-XV is grave", "V-GEO-2" in codes(m="XVI"), True)
    check("T-VE-3 page in another municipio is a warning", "V-GEO-3" in codes(m="I"), True)
    check("T-VE-3 a municipio in the page's spans passes", "V-GEO-3" in codes(z="eur", m="VIII"), False)
    check("T-VE-3 no page is a warning", codes(z=None, m=None), ["V-GEO-4"])

    print("T-VE-4 link")
    check("T-VE-4 link missing", "V-LINK-1" in codes(url=None), True)
    check("T-VE-4 link not http", "V-LINK-1" in codes(url="mailto:x@y.it"), True)
    check("T-VE-4 Roma Today link outside its channel (DEC-026)", "V-LINK-2" in codes(url="https://www.romatoday.it/eventi/x.html"), True)
    check("T-VE-4 Roma Today link in its own channel", "V-LINK-2" in codes(url="https://www.romatoday.it/eventi/x.html", src="Roma Today"), False)

    print("T-VE-5 privacy")
    check("T-VE-5 email in the place", "V-PRIV-1" in codes(luogo="scrivere a info@prova.it"), True)
    check("T-VE-5 phone in the organiser", "V-PRIV-1" in codes(org="Associazione, tel. 333 123 4567"), True)
    check("T-VE-5 postcode, year, time and dotted date are not phones", "V-PRIV-1" in codes(ind="Via Roma 12, 00153 Roma", t="Festa 2026 alle 18.30 - 04.12.2026"), False)

    print("T-VE-6 titles")
    check("T-VE-6 empty title is grave", "V-TIT-1" in codes(t="  "), True)
    for label, t in (("invitation", "Vi aspettiamo numerosi al mercatino"), ("date first", "Domenica 2 novembre alle 10 nel parco"),
                     ("cut with an ellipsis", "Laboratorio per bambini e famiglie del quartiere..."), ("hashtag", "Festa d'autunno #roma"),
                     ("too long", "Concerto " + "molto " * 20), ("emoji", "🎉🎶 Concerto")):
        check(f"T-VE-6 sentence-like title: {label}", "V-TIT-2" in codes(t=t), True)
    check("T-VE-6 a plain name passes", "V-TIT-2" in codes(t="Mercatino di Natale di Monteverde"), False)

    print("T-VE-7 duplicates")
    rows = [dict(BASE), dict(BASE, t="Concerto d’Autunno!"), dict(BASE, z="eur", m="IX"), dict(BASE, d1="2026-11-03")]
    rep = ve.run(rows, OGGI, 90, ZONES)
    dup = [r["i"] for r in rep["righe_segnalate"] if "V-DUP-1" in r["regole"]]
    check("T-VE-7 same title, day and page: the later row is the duplicate", dup, [1])

    print("T-VE-8 report and command line")
    rows = [dict(BASE), dict(BASE, d1="2026-10-01", src="Facebook"), dict(BASE, t="Vi aspettiamo", src="Facebook")]
    rep = ve.run(rows, OGGI, 90, ZONES)
    check("T-VE-8 grave rows counted once each", (rep["righe"], rep["righe_con_errore_grave"], rep["gravi"]["V-DATA-3"]), (3, 1, 1))
    check("T-VE-8 counts per channel", (rep["per_canale"]["Facebook"]["righe"], rep["per_canale"]["Facebook"].get("V-TIT-2")), (2, 1))
    check("T-VE-8 failing rows by index", [r["i"] for r in rep["righe_segnalate"]], [1, 2])
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "eventi.json")
        gaz = os.path.join(tmp, "gaz.json")
        json.dump({"oggi": "2026-10-26", "eventi": rows}, open(src, "w"))
        json.dump({"publication_zones": [dict(z, is_page=True) for z in ZONES.values()]}, open(gaz, "w"))
        try:
            ve.main(["--eventi", src, "--gazetteer", gaz, "--out", os.path.join(os.path.abspath(ROOT), "tools", "x.json")])
            check("T-VE-8 --out inside the repository refused", True, False)
        except SystemExit as e:
            check("T-VE-8 --out inside the repository refused", "DEC-109" in str(e), True)
        out = os.path.join(tmp, "rep.json")
        ve.main(["--eventi", src, "--gazetteer", gaz, "--out", out])
        check("T-VE-8 report written outside the repository", json.load(open(out))["righe"], 3)
        try:
            ve.main(["--eventi", src, "--gazetteer", gaz, "--severo"])
            check("T-VE-8 --severo exits 1 on a grave row", True, False)
        except SystemExit as e:
            check("T-VE-8 --severo exits 1 on a grave row", e.code, 1)

    print(f"\n{checks} checks, {failures} failures")
    print("ALL PASS" if failures == 0 else "FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

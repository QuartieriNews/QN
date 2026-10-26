#!/usr/bin/env python3
"""Executable acceptance for tools/fonti/leggi_eventi_siti.py (reading event pages of the sources' sites).

- T-LS-1  schema.org events are read from ld+json (plain, @graph, list), with the date
          window applied: past events and events beyond the horizon are dropped; a time in
          UTC becomes Rome time (window included), a time with a local offset is kept.
- T-LS-2  dated text blocks become candidate rows ("data nel testo"); a day-month without
          a year is read as the next occurrence, and dropped when the weekday before it does
          not match or when the block's dated mentions are all from a past season (archive
          pages); --solo-jsonld drops them.
- T-LS-3  the page to check is chosen in order: events page of the site, page read at the
          source, site root; social networks and licensed aggregators are never fetched.
- T-LS-4  a source whose page cannot be fetched is counted and skipped, never fatal; one
          row per (title, start) even when the page repeats the event.
- T-LS-5  the output path must be outside the repository, anywhere in it and however written
          (event titles never enter the repository); a copy of the tool outside a repository
          has no repository to protect.
- T-LS-6  robots.txt is read once per host and obeyed: a disallowed page is skipped and
          counted, never fetched; a 401/403 on robots.txt closes the host; an absent or
          unreachable robots.txt does not block.

Run:  python tests/test_leggi_eventi_siti.py   (exit 0 and "ALL PASS" required)
"""
import json
import os
import sys
import tempfile
from datetime import date

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "fonti"))
import leggi_eventi_siti as ls  # noqa: E402

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


TODAY = date(2026, 10, 24)
PAGE_A = """<html><head>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"TheaterEvent","name":"Spettacolo Uno","startDate":"2026-11-02T21:00","endDate":"2026-11-02T23:00",
 "location":{"@type":"Place","name":"Teatro Prova","address":{"streetAddress":"Via Prova 1","postalCode":"00100","addressLocality":"Roma"}},"url":"https://teatroprova.it/uno"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Event","name":"Evento Passato","startDate":"2026-10-01"},
 {"@type":"Event","name":"Evento Lontano","startDate":"2027-05-01"},{"@type":"MusicEvent","name":"Concerto Due","startDate":"2026-11-20","location":"Sala Grande"}]}</script>
<script type="application/ld+json">{"@type":"TheaterEvent","name":"Spettacolo Uno","startDate":"2026-11-02T21:00"}</script>
</head><body>
<h2>Prossimi appuntamenti</h2>
<li>Laboratorio per bambini, sabato 7 novembre ore 16</li>
<p>Mostra fotografica dal 15/11/2026 al 30/11/2026 nel foyer</p>
<p>Ricordo della stagione passata: 3 ottobre, grande successo</p>
<p>Il 20 gennaio torna il cineforum</p>
<div>breve</div>
</body></html>"""

FONTI = [
    {"id": "S-EV-0001", "nome": "Teatro Prova", "municipio": "I", "zona": "testaccio",
     "dove_cercare": [{"url": "https://www.facebook.com/teatroprova/events", "cosa": "eventi della pagina Facebook"},
                      {"url": "https://teatroprova.it", "cosa": "sito"},
                      {"url": "https://teatroprova.it/eventi/", "cosa": "pagina eventi del sito"}]},
    {"id": "S-EV-0002", "nome": "Circolo Giù", "municipio": "II", "zona": None,
     "dove_cercare": [{"url": "https://circologiu.it/stagione/", "cosa": "pagina letta alla fonte (calendario)"}]},
    {"id": "S-EV-0003", "nome": "Solo Social", "municipio": "I", "zona": None,
     "dove_cercare": [{"url": "https://www.facebook.com/solosocial/events", "cosa": "eventi della pagina Facebook"}]},
    {"id": "S-EV-0004", "nome": "Aggregatore Vietato", "municipio": "I", "zona": None,
     "dove_cercare": [{"url": "https://www.romatoday.it/eventi/", "cosa": "sito"}]},
]


def fake_fetch(url):
    if url == "https://teatroprova.it/eventi/":
        return PAGE_A
    raise OSError("connection refused")


def main():
    print("T-LS-3 page to check")
    check("T-LS-3 events page of the site wins over root and Facebook", ls.page_to_check(FONTI[0]), "https://teatroprova.it/eventi/")
    check("T-LS-3 page read at the source when no events page", ls.page_to_check(FONTI[1]), "https://circologiu.it/stagione/")
    check("T-LS-3 social only: nothing to fetch", ls.page_to_check(FONTI[2]), None)
    check("T-LS-3 licensed aggregator never fetched", ls.page_to_check(FONTI[3]), None)
    check("T-LS-3 selection keeps only sources with a page, filters by municipio", [f["id"] for f in ls.select(FONTI, municipio="I")], ["S-EV-0001"])

    print("T-LS-1 schema.org events")
    rows = ls.read_page(FONTI[0], "https://teatroprova.it/eventi/", PAGE_A, TODAY, 60, solo_jsonld=True)
    check("T-LS-1 two events in window, one per (title, start)", [(r["evento"], r["inizio"]) for r in rows],
          [("Spettacolo Uno", "2026-11-02T21:00"), ("Concerto Due", "2026-11-20")])
    check("T-LS-1 location and address flattened", (rows[0]["luogo"], rows[0]["indirizzo"], rows[0]["url"]),
          ("Teatro Prova", "Via Prova 1, 00100, Roma", "https://teatroprova.it/uno"))
    check("T-LS-1 string location kept", rows[1]["luogo"], "Sala Grande")
    check("T-LS-1 past and beyond-horizon events dropped", any(r["evento"] in ("Evento Passato", "Evento Lontano") for r in rows), False)
    for label, v, want in (("UTC in winter", "2026-10-29T16:30:00.000Z", "2026-10-29T17:30"), ("UTC in summer", "2026-07-01T19:00:00Z", "2026-07-01T21:00"),
                           ("UTC as +00:00", "2026-11-02T20:00:00+00:00", "2026-11-02T21:00"), ("local offset kept", "2026-11-02T21:00:00+01:00", "2026-11-02T21:00"),
                           ("no offset kept", "2026-11-02T21:00", "2026-11-02T21:00"), ("date only", "2026-11-20", "2026-11-20"), ("missing", None, "")):
        check(f"T-LS-1 Rome time: {label}", ls.data_ora_roma(v), want)
    utc = ls.read_page(FONTI[0], "x", '<script type="application/ld+json">{"@type":"Event","name":"Notte","startDate":"2026-10-23T23:30:00Z"}</script>', TODAY, 60)
    check("T-LS-1 a UTC start late on the eve is today in Rome, kept in the window", [r["inizio"] for r in utc], ["2026-10-24T01:30"])

    print("T-LS-2 dated text blocks")
    rows = ls.read_page(FONTI[0], "https://teatroprova.it/eventi/", PAGE_A, TODAY, 60)
    testo = [r for r in rows if r["prova"] == "data nel testo"]
    check("T-LS-2 two dated blocks in window", [r["inizio"] for r in testo], ["2026-11-07", "2026-11-15"])
    check("T-LS-2 range keeps its end", testo[1]["fine"], "2026-11-30")
    check("T-LS-2 block text is the hint", testo[0]["evento"].startswith("Laboratorio per bambini"), True)
    check("T-LS-2 day-month without year, far in the past, is next year (beyond horizon here)", any("cineforum" in r["evento"] for r in testo), False)
    check("T-LS-2 past date in text dropped", any("stagione passata" in r["evento"] for r in rows), False)
    check("T-LS-2 --solo-jsonld drops text rows", [r["prova"] for r in ls.read_page(FONTI[0], "x", PAGE_A, TODAY, 60, solo_jsonld=True)], ["jsonld", "jsonld"])
    check("T-LS-2 next-year rule", ls.dates_in_block("il 20 gennaio torna", date(2026, 11, 15)), [date(2027, 1, 20)])
    check("T-LS-2 weekday that matches keeps the date", ls.dates_in_block("Vi aspettiamo giovedì 26 novembre in piazza", TODAY), [date(2026, 11, 26)])
    check("T-LS-2 weekday that does not match: an earlier year's post, dropped", ls.dates_in_block("Vi aspettiamo sabato 26 novembre in piazza", TODAY), [])
    check("T-LS-2 weekday check also after the next-year rule", ls.dates_in_block("Sabato, 9 gennaio concerto", date(2026, 11, 15)), [date(2027, 1, 9)])
    check("T-LS-2 archive block: the day-month without year is not this year",
          date(2026, 12, 31) in ls.dates_in_block("31 dicembre 2015 - 10 gennaio 2016 Capodanno (solo 31 dicembre fuori abbonamento)", TODAY), False)
    check("T-LS-2 a recent dated mention is not an archive", ls.dates_in_block("dal 31 dicembre 2026 al 6 gennaio", date(2027, 1, 2)),
          [date(2026, 12, 31), date(2027, 1, 6)])
    archivio = ls.read_page(FONTI[0], "x", "<p>Capodanno 31 dicembre 2015: replica il 31 dicembre</p><p>Notte bianca, sabato 26 novembre in piazza</p>", TODAY, 90)
    check("T-LS-2 archive entries give no rows", archivio, [])

    print("T-LS-4 run, errors, output")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "eventi.jsonl")
        stats = ls.run(ls.select(FONTI), out, TODAY, 60, fetcher=fake_fetch, pausa=0, log=lambda *_: None)
        lines = [json.loads(l) for l in open(out, encoding="utf-8")]
        check("T-LS-4 unreachable source counted, run continues", (stats["fonti"], stats["lette"], stats["non_raggiungibili"]), (2, 1, 1))
        check("T-LS-4 rows written for the readable source", (stats["righe"], len(lines), stats["con_eventi_jsonld"]), (4, 4, 1))
        check("T-LS-4 rows carry the source id and page", (lines[0]["fonte_id"], lines[0]["pagina"]), ("S-EV-0001", "https://teatroprova.it/eventi/"))

    print("T-LS-5 output outside the repository")
    repo = os.path.abspath(ROOT)
    for label, path in (("docs/", os.path.join(repo, "docs", "wiki", "fonti-eventi", "x.jsonl")), ("another folder", os.path.join(repo, "tools", "x.jsonl")),
                        ("written with ..", os.path.join(repo, "tools", "..", "x.jsonl"))):
        try:
            ls.main(["--out", path])
            check(f"T-LS-5 refused: {label}", True, False)
        except SystemExit as e:
            check(f"T-LS-5 refused: {label}", "DEC-022" in str(e), True)
    check("T-LS-5 a path outside the repository is accepted", ls.inside_repo(os.path.join(tempfile.gettempdir(), "x.jsonl")), False)
    with tempfile.TemporaryDirectory() as tmp:
        check("T-LS-5 a copy outside a repository has no repository", ls.repo_root(os.path.join(tmp, "leggi_eventi_siti.py")), None)

    print("T-LS-6 robots.txt")
    calls = []

    def robots_fetch(url):
        calls.append(url)
        if url == "https://teatroprova.it/robots.txt":
            return "User-agent: *\nDisallow: /eventi/\n"
        if url == "https://circologiu.it/robots.txt":
            raise ls.urllib.error.HTTPError(url, 403, "Forbidden", None, None)
        if url == "https://teatroprova.it/eventi/":
            return PAGE_A
        raise OSError("connection refused")
    due = FONTI[:2] + [dict(FONTI[0], id="S-EV-0005")]   # two sources on the same host
    with tempfile.TemporaryDirectory() as tmp:
        stats = ls.run(due, os.path.join(tmp, "e.jsonl"), TODAY, 60, fetcher=robots_fetch, pausa=0, log=lambda *_: None)
    check("T-LS-6 disallowed and 403-closed pages skipped and counted", (stats["fonti"], stats["robots_vieta"], stats["lette"]), (3, 3, 0))
    check("T-LS-6 a disallowed page is never fetched", "https://teatroprova.it/eventi/" in calls, False)
    check("T-LS-6 robots.txt read once per host", calls.count("https://teatroprova.it/robots.txt"), 1)
    cache = {}
    check("T-LS-6 unreachable robots.txt does not block", ls.robots_allows("https://altro.it/x", lambda u: (_ for _ in ()).throw(OSError("down")), cache), True)

    print(f"\n{checks} checks, {failures} failures")
    print("ALL PASS" if failures == 0 else "FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

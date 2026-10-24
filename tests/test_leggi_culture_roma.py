#!/usr/bin/env python3
"""Executable acceptance for tools/fonti/leggi_culture_roma.py (delta reading of culture.roma.it).

- T-CR-1  the listing asks the API for items modified after the state, oldest first, and
          pages through every page.
- T-CR-2  the page parser reads dates (single and range), time, venue, address, Municipio,
          coordinates, organiser, admission, contacts, manifestazione, free label.
- T-CR-3  new vs modified: an item published after the state is "nuovo", else "modificato".
- T-CR-4  a page that fails stops the run there: it is listed with `errore` and the state
          advances only to the last item read; nothing is fatal.
- T-CR-5  output and state must be outside docs/ (titles never enter the repository).

Run:  python tests/test_leggi_culture_roma.py   (exit 0 and "ALL PASS" required)
"""
import json
import os
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "fonti"))
import leggi_culture_roma as cr  # noqa: E402

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


PAGE = """<html><body><div class="slide_title"><span class=gratuito_container><span class="etichetta gratuito">GRATUITO</span></span>
<h1 class="page_title">TITOLO PROVA</h1><p class=page_subtitle>Dibattito teatralizzato</p>
<span
class=page_date><span
class=dates>03.10.2026 &#8212; 30.10.2026</span><span class=page_orario>ORE 18:00</span></span>
<span class=page_map><span class=luogo_title>Centro Polivalente Prova</span><br> <span class=location>Via Prova, 74</span></span>
<span class=page_map><span class=municipio_title>Municipio XI</span></span>
<p
class=page_manifestazione>Nell'ambito di <a href=/manifestazione/le-ali/ >LE ALI DELLA CITTÀ 2026</a></p>
<div class=widget><h2 class="mini_section_title">Contatti</h2><p>Telefono: <a href=tel:3421662800>3421662800</a></p><p>Email: <a href=mailto:info@prova.it>info@prova.it</a></p><p>Web: <a href="https://www.prova.it " target=_blank>www.prova.it</a></p></div>
<div class="widget widget_ingresso"><h2 class="mini_section_title">Ingresso</h2><p>gratuito</p></div>
<div class="widget widget_acuradi"><h2 class="mini_section_title">A cura di</h2><p>MRF 5 s.r.l.</p></div>
<script>var mapOptions = { center : new google.maps.LatLng(41.8499045,12.4139776), zoom : 16 };</script>
</body></html>"""

LIST = [{"id": 1, "link": "https://culture.roma.it/appuntamento/uno/", "title": {"rendered": "Uno &amp; due"}, "date": "2026-10-21T10:00:00", "modified": "2026-10-22T10:00:00", "status": "publish"},
        {"id": 2, "link": "https://culture.roma.it/appuntamento/due/", "title": {"rendered": "Due"}, "date": "2026-10-01T10:00:00", "modified": "2026-10-23T10:00:00", "status": "publish"},
        {"id": 3, "link": "https://culture.roma.it/appuntamento/tre/", "title": {"rendered": "Tre"}, "date": "2026-10-23T10:00:00", "modified": "2026-10-24T10:00:00", "status": "publish"}]
calls = []


def fake_get(url, timeout=30):
    calls.append(url)
    if url.startswith(cr.API):
        page = int(dict(__import__("urllib.parse").parse.parse_qsl(url.split("?", 1)[1]))["page"])
        return json.dumps(LIST[:2] if page == 1 else LIST[2:]), {"X-WP-TotalPages": "2"}
    if url.endswith("/due/"):
        raise OSError("connection reset")
    return PAGE, {}


def main():
    print("T-CR-2 page parser")
    d = cr.parse_page(PAGE)
    check("T-CR-2 dates and time", (d["inizio"], d["fine"], d["orario"]), ("2026-10-03", "2026-10-30", "18:00"))
    check("T-CR-2 venue, address, municipio", (d["luogo"], d["indirizzo"], d["municipio"]), ("Centro Polivalente Prova", "Via Prova, 74", "XI"))
    check("T-CR-2 coordinates", (d["lat"], d["lon"]), (41.8499045, 12.4139776))
    check("T-CR-2 organiser, admission, free label", (d["a_cura_di"], d["ingresso"], d["gratuito"]), ("MRF 5 s.r.l.", "gratuito", True))
    check("T-CR-2 contacts and site", (d["sito"], d["email"], d["telefono"]), ("https://www.prova.it", "info@prova.it", "3421662800"))
    check("T-CR-2 manifestazione and subtitle", (d["manifestazione"], d["sottotitolo"]), ("LE ALI DELLA CITTÀ 2026", "Dibattito teatralizzato"))
    check("T-CR-2 single date page, line break inside the tag", cr.parse_page('<span\nclass=dates>12.11.2026 </span>')["fine"], "2026-11-12")

    print("T-CR-1 listing, T-CR-3 novelty, T-CR-4 failure")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "delta.jsonl"); st = os.path.join(tmp, "stato.json")
        stats = cr.run("2026-10-20T00:00:00", out, st, fetcher=fake_get, pausa=0, log=lambda *_: None)
        api = [c for c in calls if c.startswith(cr.API)]
        check("T-CR-1 two listing pages asked", len(api), 2)
        check("T-CR-1 modified_after and ascending order in the query", ("modified_after=2026-10-20T00%3A00%3A00" in api[0], "order=asc" in api[0], "orderby=modified" in api[0]), (True, True, True))
        rows = [json.loads(l) for l in open(out, encoding="utf-8")]
        check("T-CR-3 first item new, title unescaped", (rows[0]["novita"], rows[0]["titolo"]), ("nuovo", "Uno & due"))
        check("T-CR-3 second item modified", rows[1]["novita"], "modificato")
        check("T-CR-4 failed page listed with errore and run stops there", (rows[1].get("errore", "")[:16], len(rows)), ("connection reset", 2))
        check("T-CR-4 state advances only to the last item read", json.load(open(st))["ultima_modifica_letta"], "2026-10-22T10:00:00")
        check("T-CR-4 stats", (stats["elencati"], stats["letti"], stats["errori"], stats["nuovi"]), (3, 1, 1, 1))
        check("T-CR-4 page fields merged into the row", rows[0]["municipio"], "XI")

    print("T-CR-5 paths outside the repository")
    try:
        cr.main(["--stato", "docs/x.json", "--out", "/tmp/x.jsonl"])
        check("T-CR-5 refused", True, False)
    except SystemExit as e:
        check("T-CR-5 refused", "DEC-022" in str(e), True)

    print(f"\n{checks} checks, {failures} failures")
    print("ALL PASS" if failures == 0 else "FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

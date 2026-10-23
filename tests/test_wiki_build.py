#!/usr/bin/env python3
"""Executable acceptance for tools/wiki/build_wiki.py and tools/wiki/render_html.py
(pull request #17, review cycle 1, finding 3). Rules under test: DEC-109 (what a
diary row may carry), the gazetteer-wins rule and the determinism the README claims
(tools/wiki/build_wiki.py docstring, docs/wiki/README.md). Offline, on a fixture.

Run:  python tests/test_wiki_build.py   (exit 0 and "ALL PASS" required)
"""
import csv
import json
import os
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "wiki"))
import build_wiki  # noqa: E402
import render_html  # noqa: E402

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


COLUMNS = ["id", "fonte", "tipo", "titolo", "municipio", "zona", "luoghi", "vicenda_id", "qualita",
           "dedup_stato", "data_fatto", "data_pubblicazione", "evidenza_url", "evidenza_locale"]
ROWS = [
    # id, fonte, tipo, titolo, municipio, zona, luoghi, vicenda, qualita, dedup, data_fatto, data_pub, url, locale
    ["N1", "E2", "evento", "Cinema al Parco della Cervelletta", "IV", "", "Parco della Cervelletta;Via della Cervelletta", "V1", "alta", "unica", "2026-06-04", "2026-06-01", "https://culture.roma.it/a", ""],
    ["N2", "E2", "evento", "Corti al Parco della Cervelletta", "IV", "", "Parco della Cervelletta", "V1", "media", "unica", "2026-06-05", "2026-06-01", "https://culture.roma.it/b", ""],
    ["N3", "A1", "avviso", "Avviso in Via Inventata <script>", "IV", "", "Via Inventata 1", "", "media", "unica", "", "2026-06-07", "", "pdf/locale.pdf"],
    ["N4", "A1", "avviso", "Copia di N3", "IV", "", "Via Inventata 1", "", "media", "duplicato", "2026-06-07", "2026-06-07", "", ""],
    ["N5", "A3", "seduta", "Seduta del Consiglio", "IV", "", "Municipio IV;Piazza Sempione", "V2", "bassa", "unica", "2026-06-10", "2026-06-10", "", ""],
]
GAZETTEER = {
    "publication_zones": [{"publication_zone_id": "tor-cervara", "name_display": "Tor Cervara"}],
    "neighbourhoods": [{"name_display": "Cervelletta", "aliases": "Parco della Cervelletta",
                        "publication_zone_id": "tor-cervara"}],
}
REGISTRY_COLUMNS = ["chiave", "nome", "tipo", "zona_qn", "municipio", "canale", "link", "facebook", "decisione"]
REGISTRY = [
    ["c1", "Comitato Cervelletta", "comitato", "tor-cervara", "IV", "facebook", "javascript:alert(1)", "", "tenere"],
    ["c2", "Biblioteca Vaccheria Nardi", "biblioteca", "", "IV", "sito", "https://example.org/b", "", "tenere"],
    ["c3", "Scartata", "altro", "", "IV", "", "", "", "scartare"],
]


def build(out):
    inp = os.path.join(out, "in")
    os.makedirs(inp)
    with open(os.path.join(inp, "Report1_notizie_test.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        w.writerows(ROWS)
    reg = os.path.join(inp, "registro_fonti.csv")
    with open(reg, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(REGISTRY_COLUMNS)
        w.writerows(REGISTRY)
    gaz = os.path.join(inp, "gazetteer.json")
    json.dump(GAZETTEER, open(gaz, "w", encoding="utf-8"))
    wiki = os.path.join(out, "wiki")
    sys.argv = ["build_wiki.py", "--input", inp, "--out", wiki, "--gazetteer", gaz, "--registry", reg]
    build_wiki.main()
    html_out = os.path.join(out, "anteprima.html")
    sys.argv = ["render_html.py", "--wiki", wiki, "--out", html_out]
    render_html.main()
    return (json.load(open(os.path.join(wiki, "schedario.json"), encoding="utf-8")),
            json.load(open(os.path.join(wiki, "diario.json"), encoding="utf-8")),
            open(os.path.join(wiki, "municipi", "IV.md"), encoding="utf-8").read(),
            open(html_out, encoding="utf-8").read(),
            open(os.path.join(wiki, "schedario.json"), "rb").read() + open(os.path.join(wiki, "diario.json"), "rb").read())


with tempfile.TemporaryDirectory() as tmp:
    sched, diary, page_iv, page_html, raw_a = build(os.path.join(tmp, "a"))
with tempfile.TemporaryDirectory() as tmp:
    _, _, _, _, raw_b = build(os.path.join(tmp, "b"))

voci = {e["id"]: e for e in diary["voci"]}
places = {p["nome"]: p for p in sched["luoghi"]}

print("Diary rows: what DEC-109 lets a row carry, and nothing else")
check("duplicates (dedup_stato = duplicato) are not diary rows", sorted(voci), ["N1", "N2", "N3", "N5"])
check("a row carries exactly the declared fields", sorted(voci["N1"]),
      sorted(["id", "data", "data_pubblicazione", "fonte", "tipo", "titolo", "municipio", "zona", "luoghi",
              "questione", "qualita", "dedup", "riferimento"]))
check("the reference is the evidence URL", voci["N1"]["riferimento"], "https://culture.roma.it/a")
check("a local evidence path is kept as reference text", voci["N3"]["riferimento"], "pdf/locale.pdf")
check("date falls back to the publication date when the fact has none", voci["N3"]["data"], "2026-06-07")
check("diary is sorted by date then id", [e["id"] for e in diary["voci"]], ["N1", "N2", "N3", "N5"])

print("Gazetteer wins: a place is linked to a zone only on a name or alias match")
check("alias match links the place to its zone", places["Parco della Cervelletta"]["zona"], "tor-cervara")
check("an unknown street stays unlinked", places["Via Inventata 1"]["zona"], None)
check("an item without zone inherits the zone of a linked place", voci["N1"]["zona"], "tor-cervara")
check("an item whose places are unlinked keeps no zone", voci["N3"]["zona"], "")
check("place ids are stable across spellings (one id per normalised name)",
      len({p["id"] for p in sched["luoghi"] if build_wiki.norm(p["nome"]) == "parco della cervelletta"}), 1)
check("an institution is classified as such", places["Municipio IV"]["tipo"], "istituzione")

print("Threads (questioni) and their coherence")
q = {x["vicenda"]: x for x in sched["questioni"]}
check("a thread with two rows is open", q["V1"]["stato"], "aperta")
check("a thread with one row is single", q["V2"]["stato"], "singola")
check("coherence: every row cites the main place -> alta", q["V1"]["coerenza"], "alta")
check("the thread title is the best-quality row's title", q["V1"]["titolo"], "Cinema al Parco della Cervelletta")
check("the main place is never an institution", q["V2"]["luogo_principale"], places["Piazza Sempione"]["id"])

print("Registry sources become soggetti")
ss = {s["nome"]: s for s in sched["soggetti"]}
check("only sources marked 'tenere' enter", "Scartata" in ss, False)
check("a registry source keeps its zone", ss["Comitato Cervelletta"]["zona"], "tor-cervara")
check("the corpus institution is a soggetto too", "Municipio IV" in ss, True)

print("Determinism: two builds of the same input are byte-identical")
check("schedario + diario identical across runs", raw_a == raw_b, True)

print("Rendering: Markdown page and HTML preview")
check("the municipio page lists the open thread", "Cinema al Parco della Cervelletta" in page_iv, True)
check("HTML escapes a title with markup", "&lt;script&gt;" in page_html and "<script>alert" not in page_html, True)
check("an http(s) registry link is clickable", 'href="https://example.org/b"' in page_html, True)
check("a non-http registry link is never an href (cycle 1, note 5)", 'href="javascript:' in page_html, False)
check("a local evidence reference is text, not a link", 'href="pdf/locale.pdf"' in page_html, False)

print("")
if failures == 0:
    print(f"ALL PASS ({checks} checks)")
    sys.exit(0)
print(f"{failures} of {checks} checks FAILED")
sys.exit(1)

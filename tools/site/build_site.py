#!/usr/bin/env python3
"""Throwaway prototype of the neighbourhood page, built from real events.

What it demonstrates (and nothing else):
- the page as four blocks — Eventi, Istituzionale, Notizie, Conversazione — where
  a block can be empty without the page being empty (PROJECT_VISION.md §2);
- the Events block as "intorno a te": the zone first, then the rest of the
  municipality, then city-wide events, each item tagged with its own zone;
- a 14-day window before any fixed cap; a venue with more than three dates in
  the window collapses to one line with "vedi tutti";
- "in evidenza" for items reported by more than one channel.

It decides nothing about the publishing platform: the input is a plain events
JSON in the shape of spec v2.5 fields (publication_zone_id, municipality_code,
geo_level, content_type, editorial_class) and the output is static HTML. Whatever
platform is chosen later consumes the same data and the same rules.

    python tools/site/build_site.py --events <local copy of events_2026-10.json> \
        [--wiki <path to schedario.json>] --out site/

The events file is not in the repository: it carries third-party titles, which
DEC-109 keeps out (owner, 23 October 2026, DEC-022). It lives on Drive, QN Hub /
20 Packages / Prototipo sito 2026-10, and in the private preview.
"""
import argparse
import datetime as dt
import html
import json
import os
from collections import defaultdict, Counter

WINDOW_DAYS = 14
MIN_ITEMS = 5
VENUE_COLLAPSE = 3
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
MONTHS = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]


def esc(s):
    return html.escape(s or "")


def fmt(d):
    if not d:
        return ""
    y, m, day = d.split("-")
    return f"{int(day)} {MONTHS[int(m) - 1]}"


def in_window(e, ref, end):
    if not e["start"]:
        return False
    s = e["start"]
    t = e["end"] or e["start"]
    return s <= end and t >= ref


def events_block(zone, zones, events, ref, end):
    """Return (featured, groups, singles, undated, levels_used) for one zone."""
    mun = zones[zone]["primary_municipality"]
    ok = [e for e in events if e["editorial_class"] == "local_interest"]
    levels = []
    picked = []
    for level, pred in (("zona", lambda e: e["publication_zone_id"] == zone),
                        ("municipio", lambda e: e["publication_zone_id"] != zone and e["municipality_code"] == mun and e["geo_level"] in ("neighbourhood", "zone", "municipality")),
                        ("città", lambda e: e["geo_level"] == "city")):
        cand = [e for e in ok if pred(e) and in_window(e, ref, end)]
        if cand or level == "zona":
            picked += [(level, e) for e in cand]
            levels.append(level if cand else "zona (0)")
        if len(picked) >= MIN_ITEMS and level != "zona":
            break
        if len(picked) >= MIN_ITEMS and level == "zona":
            break
    picked.sort(key=lambda le: (le[1]["start"], le[1]["title"]))
    featured = [le for le in picked if len(le[1].get("reported_by", [])) > 1][:3]
    fid = {le[1]["id"] for le in featured}
    rest = [le for le in picked if le[1]["id"] not in fid]
    # The collapse threshold counts every date of the venue in the window, featured
    # ones included, so taking an item into "in evidenza" cannot un-collapse its
    # venue (review cycle 1, item 4); the featured item itself is listed once, above.
    dates_per_venue = Counter(le[1].get("venue") or "" for le in picked)
    by_venue = defaultdict(list)
    for le in rest:
        by_venue[le[1].get("venue") or ""].append(le)
    groups, singles = [], []
    for v, les in by_venue.items():
        if v and dates_per_venue[v] > VENUE_COLLAPSE:
            groups.append((v, les))
        else:
            singles += les
    singles.sort(key=lambda le: (le[1]["start"], le[1]["title"]))
    undated = [e for e in ok if not e["start"] and e["publication_zone_id"] == zone][:5]
    return featured, groups, singles, undated, levels


def li(level, e, zones, zone):
    # Every item carries its own zone label, the current zone's items included
    # (README: "ogni voce porta l'etichetta della propria zona"; review cycle 1, item 3).
    zn = zones.get(e["publication_zone_id"], {}).get("name_display") if e["publication_zone_id"] else None
    tag = f' <span class="tag">{esc(zn or ("Municipio " + e["municipality_code"] if e["municipality_code"] else "Roma"))}</span>'
    when = fmt(e["start"]) + (f" – {fmt(e['end'])}" if e["end"] and e["end"] != e["start"] else "")
    where = f' <span class="venue">{esc(e["venue"])}</span>' if e.get("venue") else ""
    link = f'<a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["title"])}</a>' if e.get("url") else esc(e["title"])
    return f'<li><span class="when">{when}</span> {link}{where}{tag}</li>'


def page(zone, zones, events, wiki_threads, ref, end, out_dir):
    z = zones[zone]
    mun = z["primary_municipality"]
    featured, groups, singles, undated, levels = events_block(zone, zones, events, ref, end)
    parts = [f'<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>{esc(z["name_display"])} — Quartieri News</title><link rel="stylesheet" href="../site.css"></head><body>'
             f'<header><a class="home" href="../index.html">Quartieri News</a><h1>{esc(z["name_display"])}</h1><p class="sub">Municipio {mun} · prototipo, dati reali · oggi = {fmt(ref)}</p></header><main>']
    # --- Eventi
    parts.append('<section class="block"><h2>Eventi intorno a te</h2>')
    n = len(featured) + sum(len(g[1]) for g in groups) + len(singles)
    if n == 0:
        parts.append('<p class="empty">Nessun evento nei prossimi 14 giorni nelle fonti raccolte. Il blocco resta: gli altri blocchi riempiono la pagina.</p>')
    else:
        parts.append(f'<p class="hint">Prossimi {WINDOW_DAYS} giorni · raggio: {" → ".join(levels)}</p>')
        if featured:
            parts.append('<h3>In evidenza</h3><ul class="featured">' + "".join(li(l, e, zones, zone) for l, e in featured) + "</ul>")
        if groups or singles:
            parts.append("<h3>In programma</h3><ul>")
            for v, les in sorted(groups, key=lambda g: -len(g[1])):
                first = min(le[1]["start"] for le in les)
                last = max(le[1]["start"] for le in les)
                parts.append(f'<li class="group"><details><summary><span class="when">{fmt(first)} – {fmt(last)}</span> <b>{esc(v)}</b>: {len(les)} appuntamenti <span class="more">vedi tutti</span></summary><ul>'
                             + "".join(li(l, e, zones, zone) for l, e in sorted(les, key=lambda le: le[1]["start"])) + "</ul></details></li>")
            parts.append("".join(li(l, e, zones, zone) for l, e in singles))
            parts.append("</ul>")
    if undated:
        parts.append('<h3>In corso, senza data precisa</h3><ul class="undated">' + "".join(li("zona", e, zones, zone) for e in undated) + "</ul>")
    parts.append("</section>")
    # --- Istituzionale
    parts.append('<section class="block"><h2>Dal Municipio</h2>')
    th = wiki_threads.get(mun, [])
    if th:
        parts.append('<p class="hint">Dimostrativo: questioni aperte di giugno 2026 dal wiki di contesto, Municipio ' + mun + '</p><ul>')
        for q in th[:5]:
            parts.append(f'<li><span class="when">{fmt(q["dal"])}{" – " + fmt(q["al"]) if q["al"] != q["dal"] else ""}</span> {esc(q["titolo"])} <span class="tag">{q["voci"]} voci</span></li>')
        parts.append("</ul>")
    else:
        parts.append('<p class="empty">In preparazione.</p>')
    parts.append("</section>")
    parts.append('<section class="block"><h2>Notizie</h2><p class="empty">In preparazione — le fonti sono nello studio di giugno 2026 (PR #15).</p></section>')
    parts.append('<section class="block"><h2>Se ne parla</h2><p class="empty">In preparazione — gruppi Facebook di quartiere.</p></section>')
    parts.append('</main><footer>Prototipo da buttare: serve a guardare, non a pubblicare. Regole: finestra 14 giorni · zona → municipio → città · luoghi con più di 3 date raggruppati · in evidenza se riportato da più canali.</footer></body></html>')
    os.makedirs(os.path.join(out_dir, "q"), exist_ok=True)
    open(os.path.join(out_dir, "q", f"{zone}.html"), "w", encoding="utf-8").write("".join(parts))
    return n, levels


CSS = """:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--acc:#8a3b12;--line:#e4e0d8;--soft:#f1ede4}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151513;--fg:#ecebe6;--mut:#a09e97;--acc:#e0875a;--line:#2d2c29;--soft:#1f1e1b}}
:root[data-theme=dark]{--bg:#151513;--fg:#ecebe6;--mut:#a09e97;--acc:#e0875a;--line:#2d2c29;--soft:#1f1e1b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 Georgia,serif;padding:0 16px 40px;max-width:760px;margin-inline:auto}
header{padding:14px 0 6px;border-bottom:1px solid var(--line)}.home{color:var(--acc);text-decoration:none;font-size:13px;text-transform:uppercase;letter-spacing:.08em}
h1{margin:4px 0 2px;font-size:28px}.sub{margin:0;color:var(--mut);font-size:14px}
section.block{margin:22px 0;padding:14px;background:var(--soft);border-radius:10px}h2{margin:0 0 6px;font-size:20px}h3{margin:14px 0 4px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
.hint,.empty{color:var(--mut);font-size:14px;margin:4px 0}ul{list-style:none;padding:0;margin:0}li{padding:7px 0;border-top:1px solid var(--line)}li:first-child{border-top:0}
.when{color:var(--mut);font-variant-numeric:tabular-nums;font-size:14px;margin-right:4px}.venue{color:var(--mut);font-size:14px}.venue::before{content:" · "}
.tag{display:inline-block;background:var(--line);color:var(--fg);font-size:12px;padding:1px 7px;border-radius:999px;margin-left:6px}
a{color:var(--acc)}.featured li{font-size:17px}details summary{cursor:pointer;list-style:none}.more{color:var(--acc);font-size:13px;margin-left:6px}
li.group ul{margin-top:6px;padding-left:10px}footer{color:var(--mut);font-size:13px;border-top:1px solid var(--line);padding-top:10px;margin-top:30px}
.grid{columns:2;column-gap:16px}.grid h3{column-span:all}.grid li{break-inside:avoid;border:0;padding:3px 0}
"""


def select_pages(zones, wanted):
    """The pages to build: every page zone, or only the listed ones (the pilot pages,
    DEC-031). Labels of events from other zones still come from the full zones map."""
    if not wanted:
        return list(zones)
    unknown = [z for z in wanted if z not in zones]
    if unknown:
        raise ValueError(f"not page zones: {', '.join(unknown)}")
    return list(dict.fromkeys(wanted))


def clear_pages(out_dir):
    """Remove the pages of an earlier build, so a subset build leaves only its own
    pages behind (DEC-031: the rest does not enter the pilot)."""
    q = os.path.join(out_dir, "q")
    if os.path.isdir(q):
        for name in os.listdir(q):
            if name.endswith(".html"):
                os.remove(os.path.join(q, name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True)
    ap.add_argument("--gazetteer", default="gazetteer/gazetteer.json")
    ap.add_argument("--wiki", default=None, help="schedario.json of the context wiki (optional)")
    ap.add_argument("--out", default="site")
    ap.add_argument("--pages", default="", help="comma-separated zone ids to build (default: every page)")
    a = ap.parse_args()
    data = json.load(open(a.events, encoding="utf-8"))
    ref = data["reference_date"]
    end = (dt.date.fromisoformat(ref) + dt.timedelta(days=WINDOW_DAYS)).isoformat()
    g = json.load(open(a.gazetteer, encoding="utf-8"))
    # The pages are the gazetteer's publication zones with is_page = true (spec v2.5
    # Part I: 89 pages), not "everything but other" (review cycle 1, item 2).
    zones = {z["publication_zone_id"]: z for z in g["publication_zones"] if z.get("is_page") is True}
    try:
        pages = select_pages(zones, [p.strip() for p in a.pages.split(",") if p.strip()])
    except ValueError as e:
        raise SystemExit(str(e))
    wiki_threads = defaultdict(list)
    if a.wiki and os.path.exists(a.wiki):
        for q in json.load(open(a.wiki, encoding="utf-8"))["questioni"]:
            if q["stato"] == "aperta" and q.get("coerenza") == "alta" and q["municipio"]:
                wiki_threads[q["municipio"]].append(q)
    os.makedirs(a.out, exist_ok=True)
    clear_pages(a.out)
    open(os.path.join(a.out, "site.css"), "w", encoding="utf-8").write(CSS)
    counts = {}
    for zid in pages:
        counts[zid] = page(zid, zones, data["events"], wiki_threads, ref, end, a.out)
    by_mun = defaultdict(list)
    for zid in pages:
        by_mun[zones[zid]["primary_municipality"]].append(zid)
    idx = ['<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quartieri News — prototipo</title><link rel="stylesheet" href="site.css"></head><body>',
           f'<header><h1>Quartieri News</h1><p class="sub">Prototipo della pagina di quartiere con {len(data["events"])} eventi reali. Oggi = {fmt(ref)}. Niente è pubblicato: è una cosa da guardare.</p></header><main>',
           '<section class="block"><h2>Come leggerlo</h2><p class="hint">Ogni pagina ha quattro blocchi. Il blocco eventi mostra prima la zona, poi il resto del municipio, poi la città, finché non ci sono almeno 5 cose nei prossimi 14 giorni; ogni voce porta il nome della sua zona. I luoghi con più di tre date si raggruppano. "In evidenza" = riportato da più canali. Il blocco "Dal Municipio" usa le questioni di giugno dal wiki, solo per far vedere la forma.</p></section>',
           f'<section class="block"><h2>Le {len(pages)} pagine</h2>']
    for m in ROMAN:
        if not by_mun.get(m):
            continue
        idx.append(f'<h3>Municipio {m}</h3><ul class="grid">')
        for zid in sorted(by_mun.get(m, []), key=lambda z: zones[z]["name_display"]):
            n, levels = counts[zid]
            idx.append(f'<li><a href="q/{zid}.html">{esc(zones[zid]["name_display"])}</a> <span class="tag">{n} eventi</span></li>')
        idx.append("</ul>")
    idx.append("</section></main></body></html>")
    open(os.path.join(a.out, "index.html"), "w", encoding="utf-8").write("".join(idx))
    dist = Counter("0" if n == 0 else "1-4" if n < 5 else "5-15" if n <= 15 else ">15" for n, _ in counts.values())
    lv = Counter(" → ".join(l) for _, l in counts.values())
    print(f"{len(pages)} pagine → {a.out}; eventi per pagina: {dict(dist)}; raggio usato: {dict(lv)}")


if __name__ == "__main__":
    main()

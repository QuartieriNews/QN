#!/usr/bin/env python3
"""Read culture.roma.it (Roma Capitale's events agenda) by difference.

The agenda exposes the public WordPress REST API (`wp-json/wp/v2/event_calendar`,
20,000+ items). A full reading was done once on 20 October 2026 (Apify cheerio, 6,222
items, the point zero of the October workbook). From then on this tool reads only what
changed: items whose `modified` is after the last reading, pages through them, fetches each
one's page for the fields the API does not carry (dates, time, venue, address, Municipio,
organiser "a cura di", contacts, admission, coordinates) and writes one row per item.
Standard library only; the state (last reading) is one small JSON file; the output carries
event titles, so both must live outside the repository (DEC-022, DEC-109).

Usage:
    python tools/fonti/leggi_culture_roma.py --stato /lavoro/culture_stato.json --out /lavoro/culture_delta.jsonl
        [--da 2026-10-20T00:00:00]  (first run: the date of the point zero)  [--max 200]  [--pausa 1.0]

Rules: one request per second (the agenda is a public service, not a feed built for us),
a user agent with a contact, no retry storm (a failed page is listed in the output with
`errore`, the state advances only to the last item read successfully). Reuse clause of the
agenda still "da verificare (L11)" in the registry: this tool reads schede, keeps no texts
beyond title and fields, and is the delta feed for the editorial reading, not a mirror.
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

API = "https://culture.roma.it/wp-json/wp/v2/event_calendar"
UA = "QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace"), dict(r.headers)


def list_modified(since, per_page=100, fetcher=get, pausa=1.0, log=print):
    """Every item modified after `since` (ISO, site time), oldest first, as API dicts."""
    page, out = 1, []
    while True:
        q = urllib.parse.urlencode({"per_page": per_page, "page": page, "orderby": "modified", "order": "asc",
                                    "modified_after": since, "_fields": "id,slug,link,title,date,modified,status,municipio,sezioni,tipologia_evento"})
        body, headers = fetcher(f"{API}?{q}")
        items = json.loads(body)
        if not isinstance(items, list):
            raise RuntimeError(f"API answered with {str(items)[:120]}")
        out += items
        total_pages = int(headers.get("X-WP-TotalPages") or headers.get("x-wp-totalpages") or 1)
        log(f"  elenco pagina {page}/{total_pages}: {len(items)} voci")
        if page >= total_pages or not items:
            break
        page += 1
        time.sleep(pausa)
    return out


def text(s):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def span(doc, cls):
    m = re.search(r'<span\s+class="?' + cls + r'"?\s*>(.*?)</span>', doc, re.S)   # the theme breaks lines inside tags
    return text(m.group(1)) if m else None


def widget(doc, title):
    m = re.search(r'mini_section_title">' + re.escape(title) + r'</h2>(.*?)</div>', doc, re.S)
    return m.group(1) if m else None


def parse_page(doc):
    """Fields of one appuntamento page (classes of the cultureroma theme, October 2026)."""
    d = {}
    dates = span(doc, "dates") or ""
    ds = re.findall(r"(\d{2})\.(\d{2})\.(\d{4})", dates)
    d["inizio"] = f"{ds[0][2]}-{ds[0][1]}-{ds[0][0]}" if ds else None
    d["fine"] = f"{ds[-1][2]}-{ds[-1][1]}-{ds[-1][0]}" if len(ds) > 1 else d["inizio"]
    ora = span(doc, "page_orario")
    d["orario"] = re.sub(r"^ORE\s+", "", ora) if ora else None
    d["luogo"] = span(doc, "luogo_title")
    d["indirizzo"] = span(doc, "location")
    mun = span(doc, "municipio_title") or ""
    m = re.search(r"Municipio\s+([IVX]+)", mun)
    d["municipio"] = m.group(1) if m and m.group(1) in ROMAN else None
    m = re.search(r"LatLng\(([\d.]+),\s*([\d.]+)\)", doc)
    d["lat"], d["lon"] = (float(m.group(1)), float(m.group(2))) if m else (None, None)
    w = widget(doc, "A cura di")
    d["a_cura_di"] = text(w) if w else None
    w = widget(doc, "Ingresso")
    d["ingresso"] = text(w) if w else None
    w = widget(doc, "Contatti") or ""
    d["sito"] = next((u for u in re.findall(r'href="?(https?://[^"\s>]+)', w) if "culture.roma.it" not in u), None)
    d["email"] = next(iter(re.findall(r"mailto:([^\"'\s>]+)", w)), None)
    d["telefono"] = next(iter(re.findall(r"tel:([^\"'\s>]+)", w)), None)
    m = re.search(r'page_manifestazione\s*>\s*Nell\'ambito di\s*<a\s+href="?([^"\s>]+)"?[^>]*>(.*?)</a>', doc, re.S)
    d["manifestazione"] = text(m.group(2)) if m else None
    m = re.search(r'class="?page_subtitle"?\s*>(.*?)</p>', doc, re.S)
    d["sottotitolo"] = text(m.group(1)) if m else None
    d["gratuito"] = 'etichetta gratuito' in doc
    return d


def run(since, out_path, state_path, max_items=None, fetcher=get, pausa=1.0, log=print):
    items = list_modified(since, fetcher=fetcher, pausa=pausa, log=log)
    if max_items:
        items = items[:max_items]
    stats = {"da": since, "elencati": len(items), "letti": 0, "errori": 0, "nuovi": 0, "modificati": 0}
    last_ok = since
    with open(out_path, "w", encoding="utf-8") as fh:
        for it in items:
            row = {"id": it["id"], "url": it.get("link"), "titolo": text((it.get("title") or {}).get("rendered")), "pubblicato": it.get("date"),
                   "modificato": it.get("modified"), "stato": it.get("status"), "novita": "nuovo" if (it.get("date") or "") > since else "modificato"}
            try:
                doc, _ = fetcher(it["link"])
                row.update(parse_page(doc))
                stats["letti"] += 1
                stats["nuovi" if row["novita"] == "nuovo" else "modificati"] += 1
                last_ok = it.get("modified") or last_ok
            except Exception as e:  # listed, never fatal; the state does not pass this item
                row["errore"] = str(e)[:120]
                stats["errori"] += 1
                log(f"  x {it.get('link')} ({row['errore'][:60]})")
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                break
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            time.sleep(pausa)
    stats["ultima_modifica_letta"] = last_ok
    json.dump({"ultima_modifica_letta": last_ok, "aggiornato": datetime.now().isoformat(timespec="seconds"), "ultima_lettura": stats},
              open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return stats


def repo_root(start=None):
    """The repository holding this tool (the directory with .git), or None when run from a copy."""
    for d in Path(start or __file__).resolve().parents:
        if (d / ".git").exists():
            return d
    return None


def inside_repo(path, root=None):
    """True when path, resolved (symlinks, '..', relative to the working directory), falls inside the repository."""
    root = root or repo_root()
    p = Path(path).expanduser().resolve()
    return bool(root) and (p == root or root in p.parents)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stato", required=True, help="JSON state file (last modification read); outside the repository")
    ap.add_argument("--out", required=True, help="JSONL of the items read; outside the repository (carries titles)")
    ap.add_argument("--da", help="ISO date-time to start from when the state file does not exist yet")
    ap.add_argument("--max", type=int, help="read at most N items (trial runs)")
    ap.add_argument("--pausa", type=float, default=1.0)
    a = ap.parse_args(argv)
    if any(inside_repo(p) for p in (a.out, a.stato)):
        sys.exit("--out and --stato must point outside the repository (DEC-022, DEC-109)")
    since = json.load(open(a.stato, encoding="utf-8"))["ultima_modifica_letta"] if os.path.exists(a.stato) else a.da
    if not since:
        sys.exit("first run: pass --da <ISO date-time of the point zero>")
    stats = run(since, a.out, a.stato, a.max, pausa=a.pausa)
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()

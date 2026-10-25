#!/usr/bin/env python3
"""Read the event pages of the sources' own websites and list the events they announce.

The weekly reading of primary sources that the wiki of event sources points at
(`docs/wiki/fonti-eventi/fonti_eventi.json`, field `dove_cercare`): for every source with
a website, fetch the page to check (events page of the site, else the page read at the
source, else the site root), extract the events it publishes and write them out as rows.
Standard library only; nothing is written in the repository: the output carries event
titles, which are source text (DEC-022, DEC-109), so `--out` must point outside it.

What counts as an event, in order of confidence:
  jsonld   a schema.org Event (or subtype) in a <script type="application/ld+json">
           block: name, startDate, endDate, location, url. The reliable signal.
  data     a date written in the page text (Italian month names, dd/mm/yyyy, weekday +
           day) inside a text block (heading, list item, article): a candidate to read
           by a person, with the surrounding text as hint.
Only dates from today to --orizzonte days ahead are kept.

Usage:
    python tools/fonti/leggi_eventi_siti.py --schedario docs/wiki/fonti-eventi/fonti_eventi.json \
        --out /lavoro/eventi_siti.jsonl [--solo-jsonld] [--max 50] [--municipio I] [--zona monteverde]

Rules: one request per second per host, a user agent with a contact, the host's robots.txt
read once per run and obeyed (a page it disallows is skipped and counted), no aggregator with
a licence clause (Roma Today / Citynews are never fetched: project rule "nessun canale senza
licenza"), social networks never fetched (DEC-102: Facebook is read through the owner's
Apify runs, not from here).
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import date, datetime, timedelta
from pathlib import Path

UA = "QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
MESI = "gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre"
MESE_N = {m: i + 1 for i, m in enumerate(MESI.split("|"))}
GIORNI = r"luned[iì]|marted[iì]|mercoled[iì]|gioved[iì]|venerd[iì]|sabato|domenica"
DATA_TESTO = re.compile(r"\b(\d{1,2})\s+(" + MESI + r")(?:\s+(\d{4}))?\b|\b(\d{1,2})[/.](\d{1,2})[/.](\d{4})\b", re.I)
NEVER = re.compile(r"(romatoday|citynews|facebook\.com|instagram\.com|tiktok\.com|x\.com|twitter\.com|linkedin\.com|youtube\.com|t\.me|wa\.me)", re.I)
EVENT_TYPES = ("Event", "MusicEvent", "TheaterEvent", "ExhibitionEvent", "Festival", "SocialEvent", "EducationEvent",
               "ChildrensEvent", "ComedyEvent", "DanceEvent", "LiteraryEvent", "ScreeningEvent", "SportsEvent", "VisualArtsEvent",
               "BusinessEvent", "FoodEvent", "SaleEvent", "PublicationEvent")


def fetch(url, timeout=30):
    """Return the decoded body of url (text), or raise. Separate so tests can replace it."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(3_000_000)
        ct = r.headers.get("Content-Type", "")
    m = re.search(r"charset=([\w-]+)", ct) or re.search(rb"charset=[\"']?([\w-]+)", raw[:4000])
    enc = (m.group(1) if isinstance(m.group(1), str) else m.group(1).decode()) if m else "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def parse_iso_date(s):
    """Date part of a schema.org date/datetime string; None when unreadable."""
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})", str(s or ""))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def jsonld_events(doc):
    """Every schema.org Event object in the page's ld+json blocks (nested @graph and lists included)."""
    out = []
    for m in re.finditer(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", doc, re.S | re.I):
        txt = m.group(1).strip()
        try:
            data = json.loads(txt)
        except json.JSONDecodeError:
            try:
                data = json.loads(re.sub(r",\s*([}\]])", r"\1", txt))
            except json.JSONDecodeError:
                continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, list):
                stack.extend(x)
            elif isinstance(x, dict):
                t = x.get("@type")
                types = t if isinstance(t, list) else [t]
                if any(str(tt) in EVENT_TYPES for tt in types):
                    out.append(x)
                for k in ("@graph", "itemListElement", "item", "subEvent", "mainEntity"):
                    if k in x:
                        stack.append(x[k])
    return out


def event_row(ev, fonte, pagina):
    loc = ev.get("location")
    if isinstance(loc, list):
        loc = loc[0] if loc else None
    loc_name = loc.get("name") if isinstance(loc, dict) else (loc if isinstance(loc, str) else None)
    addr = loc.get("address") if isinstance(loc, dict) else None
    if isinstance(addr, dict):
        addr = ", ".join(str(addr.get(k)) for k in ("streetAddress", "postalCode", "addressLocality") if addr.get(k))
    return {"fonte_id": fonte["id"], "fonte": fonte["nome"], "pagina": pagina, "prova": "jsonld",
            "evento": str(ev.get("name") or "").strip(), "inizio": str(ev.get("startDate") or "")[:16], "fine": str(ev.get("endDate") or "")[:16],
            "luogo": loc_name, "indirizzo": addr, "url": ev.get("url") if isinstance(ev.get("url"), str) else None}


def text_blocks(doc):
    """Text of block-level elements, in document order, scripts and styles removed."""
    doc = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", doc, flags=re.S | re.I)
    parts = re.split(r"<(?:/?(?:p|div|li|h[1-6]|article|section|td|tr|br|dd|dt|header|footer)\b)[^>]*>", doc, flags=re.I)
    out = []
    for p in parts:
        t = html_mod.unescape(re.sub(r"<[^>]+>", " ", p))
        t = re.sub(r"\s+", " ", t).strip()
        if 8 <= len(t) <= 400:
            out.append(t)
    return out


def dates_in_block(t, today):
    found = []
    for m in DATA_TESTO.finditer(t):
        try:
            if m.group(2):
                y = int(m.group(3)) if m.group(3) else today.year
                d = date(y, MESE_N[m.group(2).lower()], int(m.group(1)))
                if not m.group(3) and d < today - timedelta(days=60):   # "15 gennaio" said in November means next year
                    d = date(y + 1, d.month, d.day)
            else:
                d = date(int(m.group(6)), int(m.group(5)), int(m.group(4)))
        except ValueError:
            continue
        found.append(d)
    return found


def read_page(fonte, pagina, doc, today, orizzonte, solo_jsonld=False):
    """Rows for one fetched page: schema.org events first, dated text blocks after."""
    rows = []
    seen = set()
    limite = today + timedelta(days=orizzonte)
    for ev in jsonld_events(doc):
        d = parse_iso_date(ev.get("startDate"))
        if d is None or d < today or d > limite:
            continue
        r = event_row(ev, fonte, pagina)
        key = (r["evento"], r["inizio"])
        if r["evento"] and key not in seen:
            seen.add(key)
            rows.append(r)
    if solo_jsonld:
        return rows
    for t in text_blocks(doc):
        ds = [d for d in dates_in_block(t, today) if today <= d <= limite]
        if not ds:
            continue
        key = ("testo", t[:80], ds[0].isoformat())
        if key in seen:
            continue
        seen.add(key)
        rows.append({"fonte_id": fonte["id"], "fonte": fonte["nome"], "pagina": pagina, "prova": "data nel testo",
                     "evento": t[:160], "inizio": ds[0].isoformat(), "fine": ds[-1].isoformat() if len(ds) > 1 else "",
                     "luogo": None, "indirizzo": None, "url": None})
    return rows


def page_to_check(fonte):
    """The one address to read for a source: events page of the site, else page read at the
    source, else the site root. Social and licensed aggregators are never returned."""
    order = ("pagina eventi del sito", "pagina letta alla fonte (calendario)", "sito")
    for cosa in order:
        for d in fonte.get("dove_cercare", []):
            if d.get("cosa") == cosa and d.get("url", "").startswith("http") and not NEVER.search(d["url"]):
                return d["url"]
    return None


def select(fonti, municipio=None, zona=None, ids=None):
    out = []
    for f in fonti:
        if municipio and f.get("municipio") != municipio:
            continue
        if zona and f.get("zona") != zona:
            continue
        if ids and f["id"] not in ids:
            continue
        if page_to_check(f):
            out.append(f)
    return out


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


def robots_allows(url, fetcher, cache, before_request=lambda host: None):
    """robots.txt of the url's host, read once per run (cache); absent or unreadable it does not block,
    as the robots convention says, except a 401/403 on robots.txt itself, which closes the host."""
    parts = urllib.parse.urlsplit(url)
    if parts.netloc not in cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            before_request(parts.netloc)
            rp.parse(fetcher(f"{parts.scheme}://{parts.netloc}/robots.txt").splitlines())
        except urllib.error.HTTPError as e:
            rp = False if e.code in (401, 403) else None
        except Exception:  # unreachable or absent: no rule to obey
            rp = None
        cache[parts.netloc] = rp
    rp = cache[parts.netloc]
    return rp is None or (rp is not False and rp.can_fetch(UA, url))


def run(fonti, out_path, today, orizzonte=60, solo_jsonld=False, max_fonti=None, fetcher=fetch, pausa=1.0, log=print):
    last_hit, robots = {}, {}
    stats = {"fonti": 0, "lette": 0, "non_raggiungibili": 0, "robots_vieta": 0, "con_eventi_jsonld": 0, "con_date": 0, "righe": 0}

    def before_request(host):   # one request per second per host, robots.txt included
        wait = last_hit.get(host, 0) + pausa - time.time()
        if wait > 0:
            time.sleep(wait)
        last_hit[host] = time.time()
    with open(out_path, "w", encoding="utf-8") as fh:
        for f in fonti[:max_fonti] if max_fonti else fonti:
            url = page_to_check(f)
            stats["fonti"] += 1
            if not robots_allows(url, fetcher, robots, before_request):
                stats["robots_vieta"] += 1
                log(f"  r {f['id']} {url} (robots.txt)")
                continue
            before_request(urllib.parse.urlsplit(url).netloc)
            try:
                doc = fetcher(url)
            except Exception as e:  # network errors of every kind: recorded, never fatal
                stats["non_raggiungibili"] += 1
                log(f"  x {f['id']} {url} ({str(e)[:60]})")
                continue
            stats["lette"] += 1
            rows = read_page(f, url, doc, today, orizzonte, solo_jsonld)
            if any(r["prova"] == "jsonld" for r in rows):
                stats["con_eventi_jsonld"] += 1
            elif rows:
                stats["con_date"] += 1
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            stats["righe"] += len(rows)
            log(f"  {len(rows):3d} {f['id']} {url}")
    return stats


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--schedario", default="docs/wiki/fonti-eventi/fonti_eventi.json")
    ap.add_argument("--out", required=True, help="JSONL of the events found; outside the repository (carries titles)")
    ap.add_argument("--orizzonte", type=int, default=60, help="days ahead to keep (default 60)")
    ap.add_argument("--solo-jsonld", action="store_true", help="keep only schema.org events, no dated text blocks")
    ap.add_argument("--max", type=int, help="read at most N sources (trial runs)")
    ap.add_argument("--municipio", help="only sources of this Municipio (Roman numeral)")
    ap.add_argument("--zona", help="only sources of this QN publication zone id")
    ap.add_argument("--id", action="append", help="only these source ids (repeatable)")
    ap.add_argument("--oggi", help="date to reason from, YYYY-MM-DD (default: today)")
    a = ap.parse_args(argv)
    if inside_repo(a.out):
        sys.exit("--out must point outside the repository: the output carries event titles (DEC-022, DEC-109)")
    sched = json.load(open(a.schedario, encoding="utf-8"))
    today = datetime.strptime(a.oggi, "%Y-%m-%d").date() if a.oggi else date.today()
    fonti = select(sched["fonti"], a.municipio, a.zona, set(a.id) if a.id else None)
    print(f"fonti con una pagina da leggere: {len(fonti)}")
    stats = run(fonti, a.out, today, a.orizzonte, a.solo_jsonld, a.max)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()

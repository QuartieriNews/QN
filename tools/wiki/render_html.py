#!/usr/bin/env python3
"""Render docs/wiki (schedario.json + diario.json) as one self-contained HTML page
for reading on a phone: a tab per municipio, open questions first, places and
registered actors after, the month's chronology at the end. A rendering only —
nothing here is a source of truth.

    python tools/wiki/render_html.py --wiki docs/wiki --out docs/wiki/anteprima.html
"""
import argparse
import html
import json
import os
from collections import Counter, defaultdict

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
SRC = {"A1": "Roma Capitale · notizie", "A2": "Atti Web", "A3": "RomaTV", "A4": "YouTube Municipi",
       "C1": "Questura", "C2": "Carabinieri", "C4": "Vigili del Fuoco", "C5": "Polizia Locale",
       "E2": "culture.roma.it", "E3": "Agenda eventi Comune"}


def esc(s):
    return html.escape(s or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="docs/wiki")
    ap.add_argument("--out", default="docs/wiki/anteprima.html")
    a = ap.parse_args()
    sched = json.load(open(os.path.join(a.wiki, "schedario.json"), encoding="utf-8"))
    diary = json.load(open(os.path.join(a.wiki, "diario.json"), encoding="utf-8"))["voci"]
    places = {p["id"]: p for p in sched["luoghi"]}
    threads = defaultdict(list)
    for e in diary:
        if e["questione"]:
            threads[e["questione"]].append(e)
    qs_by_m = defaultdict(list)
    for q in sched["questioni"]:
        if q["stato"] == "aperta":
            qs_by_m[q["municipio"]].append(q)

    parts = []
    for m in ROMAN:
        es = [e for e in diary if e["municipio"] == m]
        qs = qs_by_m.get(m, [])
        lp = Counter(p for e in es for p in e["luoghi"])
        ss = [s for s in sched["soggetti"] if s.get("municipio") == m]
        sec = [f'<section id="m{m}" class="mun"><h2>Municipio {m}</h2>',
               f'<p class="stat">{len(es)} voci · {len(qs)} questioni aperte · {len(lp)} luoghi · {len(ss)} soggetti registrati</p>',
               '<h3>Questioni aperte</h3><p class="note">Raggruppamento dello studio fonti (stessa data e luogo); la coerenza dice quanto le voci parlano davvero della stessa cosa.</p>']
        for q in qs:
            sec.append(f'<details class="q c-{q["coerenza"]}"><summary><span class="t">{esc(q["titolo"])}</span>'
                       f'<span class="meta">{q["voci"]} voci · {esc(q["dal"])}{" → " + esc(q["al"]) if q["al"] != q["dal"] else ""} · coerenza {q["coerenza"]}'
                       f'{" · " + esc(q["zona"]) if q["zona"] else ""}</span></summary>')
            if q["luoghi"]:
                sec.append('<p class="places">' + " · ".join(esc(places[p]["nome"]) for p in q["luoghi"]) + "</p>")
            sec.append("<ul>")
            for e in threads[q["vicenda"]]:
                ref = e["riferimento"]
                link = f' <a href="{esc(ref.split(" ")[0])}" target="_blank" rel="noopener">fonte</a>' if ref.startswith("http") else (f' <span class="ref">{esc(ref)}</span>' if ref else "")
                sec.append(f'<li><span class="d">{esc(e["data"])}</span> <span class="s">{esc(SRC.get(e["fonte"], e["fonte"]))}</span> {esc(e["titolo"])}{link}</li>')
            sec.append("</ul></details>")
        sec.append('<h3>Luoghi più citati</h3><table><tr><th>luogo</th><th>tipo</th><th>zona</th><th>n</th></tr>')
        for pid, n in lp.most_common(25):
            p = places[pid]
            sec.append(f'<tr><td>{esc(p["nome"])}</td><td>{p["tipo"]}</td><td>{esc(p["zona"] or "—")}</td><td>{n}</td></tr>')
        sec.append("</table>")
        sec.append('<h3>Soggetti registrati</h3><table><tr><th>soggetto</th><th>tipo</th><th>zona</th></tr>')
        for s in sorted(ss, key=lambda s: (s["tipo"], s["nome"])):
            name = f'<a href="{esc(s["link"])}" target="_blank" rel="noopener">{esc(s["nome"])}</a>' if s.get("link") else esc(s["nome"])
            sec.append(f'<tr><td>{name}</td><td>{esc(s["tipo"])}</td><td>{esc(s.get("zona") or "—")}</td></tr>')
        sec.append("</table>")
        sec.append('<details class="chrono"><summary>Cronologia del mese</summary><ul>')
        for e in es:
            sec.append(f'<li><span class="d">{esc(e["data"])}</span> <span class="s">{esc(e["fonte"])}</span> {esc(e["titolo"])}</li>')
        sec.append("</ul></details></section>")
        parts.append("\n".join(sec))

    nav = " ".join(f'<a href="#m{m}" data-m="{m}">{m}</a>' for m in ROMAN)
    tot_q = sum(len(v) for v in qs_by_m.values())
    page = f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>QN wiki giugno 2026</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--acc:#8a3b12;--line:#e4e0d8;--ok:#2f7a3d;--mid:#b07a12;--low:#a33a2f}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#151513;--fg:#ecebe6;--mut:#a09e97;--acc:#e0875a;--line:#2d2c29}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.45 Georgia,serif;padding:0 16px 48px}}
header{{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 0;z-index:2}}
h1{{font-size:20px;margin:0 0 6px}} nav a{{display:inline-block;padding:4px 8px;margin:2px;border:1px solid var(--line);border-radius:6px;text-decoration:none;color:var(--fg);font-size:14px}}
nav a.on{{background:var(--acc);color:#fff;border-color:var(--acc)}}
section.mun{{display:none;padding-top:12px}} section.mun.on{{display:block}}
h2{{font-size:22px;margin:8px 0 2px}} h3{{font-size:16px;margin:22px 0 6px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.stat,.note{{color:var(--mut);font-size:14px;margin:0 0 8px}}
details.q{{border-left:4px solid var(--line);padding:6px 10px;margin:8px 0;background:rgba(0,0,0,.02)}}
details.q.c-alta{{border-color:var(--ok)}} details.q.c-media{{border-color:var(--mid)}} details.q.c-bassa{{border-color:var(--low)}}
summary{{cursor:pointer;list-style:none}} summary .t{{display:block;font-weight:bold}} summary .meta{{display:block;color:var(--mut);font-size:13px}}
.places{{font-size:13px;color:var(--mut);margin:6px 0}}
ul{{padding-left:18px;margin:6px 0}} li{{margin:4px 0;font-size:15px}} .d{{color:var(--mut);font-variant-numeric:tabular-nums}} .s{{color:var(--acc);font-size:12px;text-transform:uppercase}}
.ref{{color:var(--mut);font-size:12px}} a{{color:var(--acc)}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{text-align:left;padding:4px 6px;border-bottom:1px solid var(--line);vertical-align:top}}
details.chrono summary{{color:var(--mut);margin-top:18px}}
</style></head><body>
<header><h1>Quartieri News — wiki di contesto, giugno 2026</h1>
<p class="stat">{len(diary)} voci di diario · {tot_q} questioni aperte · {len(places)} luoghi · {len(sched["soggetti"])} soggetti · generato da schedario.json + diario.json</p>
<nav>{nav}</nav></header>
{"".join(parts)}
<script>
const secs=[...document.querySelectorAll('section.mun')],links=[...document.querySelectorAll('nav a')];
function show(m){{secs.forEach(s=>s.classList.toggle('on',s.id==='m'+m));links.forEach(a=>a.classList.toggle('on',a.dataset.m===m));try{{localStorage.setItem('qnwiki.m',m)}}catch(e){{}}}}
links.forEach(a=>a.addEventListener('click',e=>{{e.preventDefault();show(a.dataset.m);window.scrollTo(0,0)}}));
let m='I';try{{m=location.hash.slice(2)||localStorage.getItem('qnwiki.m')||'I'}}catch(e){{}}
show(secs.some(s=>s.id==='m'+m)?m:'I');
</script></body></html>"""
    open(a.out, "w", encoding="utf-8").write(page)
    print(a.out, len(page), "bytes")


if __name__ == "__main__":
    main()

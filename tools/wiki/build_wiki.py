#!/usr/bin/env python3
"""Build the Quartieri News context wiki from the June 2026 source study.

Three outputs, in this order of authority:

1. schedario  — the registry of things that exist: luoghi (places), soggetti
   (institutions, committees, venues as actors) and questioni (threads). Every
   entry has a stable id, a canonical name and the spellings seen (aliases).
2. diario     — one dated entry per news item, attached to the schedario entries
   it concerns, with the source reference. Never rewritten; only appended to.
3. pagine     — per-municipio Markdown pages generated from 1 and 2. They are
   renderings, not the place where information lives.

Inputs: the per-item news files of the source study (Drive, QN Hub / 20 Packages /
Fonti 2026-06, `Report1_notizie_*.csv` and `Report2_notizie_*.csv`), the source
registry of 13 October 2026 (`registro_fonti.csv`) and `gazetteer/gazetteer.json`.
Nothing is fetched from the network; pass the folder that holds the CSVs.

Usage:
    python tools/wiki/build_wiki.py --input <folder-with-csv> --out docs/wiki

Rules this build honours:
- DEC-105: people appear only in a public role; the inputs are already
  anonymised and nothing here adds names.
- DEC-109: no source text enters the repository — the diary carries the study's
  own one-line titles and the source URL, never the article body.
- gazetteer.json wins: a place string is linked to a publication zone only when
  it matches a gazetteer name or alias; otherwise it stays unlinked.
"""
import argparse
import csv
import glob
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
SOURCE_LABEL = {
    "A1": "Roma Capitale, notizie dei Municipi",
    "A2": "Atti Web, delibere e atti dei Municipi",
    "A3": "RomaTV, commissioni e consigli in streaming",
    "A4": "YouTube dei Municipi",
    "C1": "Questura di Roma", "C2": "Carabinieri", "C4": "Vigili del Fuoco", "C5": "Polizia Locale",
    "E2": "culture.roma.it", "E3": "Roma Capitale, agenda eventi",
}
VENUE_WORDS = ("teatro", "cinema", "biblioteca", "museo", "parco", "villa", "mercato", "scuola", "liceo",
               "istituto", "auditorium", "arena", "centro", "casa ", "palazzo", "chiesa", "basilica",
               "stazione", "ospedale", "piscina", "stadio", "galleria", "oratorio", "casale", "circolo")
STREET_WORDS = ("via ", "viale ", "piazza", "piazzale", "largo ", "lungotevere", "corso ", "vicolo", "circonvallazione", "ponte ")
INSTITUTION_RE = re.compile(r"^(municipio( roma)? [ivx]+( [a-z ]+)?|roma capitale|regione lazio|acea|ama|atac|asl[ a-z0-9]*|questura|carabinieri|vigili del fuoco|polizia locale|polizia municipale|prefettura|demanio|sovrintendenza|soprintendenza|campidoglio|assemblea capitolina|giunta capitolina)$")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("’", "'").replace("`", "'")
    s = re.sub(r"\s+", " ", s).strip(" .,;:")
    s = re.sub(r"\bmunicipio roma ([ivx]+)\b", r"municipio \1", s)
    s = re.sub(r"\bmunicipio ([ivx]+) [a-z ]+$", r"municipio \1", s)  # "Municipio IX Eur" -> municipio ix
    return s


def load_gazetteer(path):
    g = json.load(open(path, encoding="utf-8"))
    zones = {z["publication_zone_id"]: z for z in g["publication_zones"]}
    alias_to_zone = {}
    for z in g["publication_zones"]:
        alias_to_zone[norm(z["name_display"])] = z["publication_zone_id"]
        alias_to_zone[norm(z["publication_zone_id"].replace("-", " "))] = z["publication_zone_id"]
    for n in g.get("neighbourhoods", []):
        zid = n.get("publication_zone_id")
        if not zid:
            continue
        alias_to_zone.setdefault(norm(n.get("name_display", "")), zid)
        for a in (n.get("aliases") or "").split(";"):
            if a.strip():
                alias_to_zone.setdefault(norm(a), zid)
    return zones, alias_to_zone


def classify_place(name):
    n = norm(name)
    if INSTITUTION_RE.match(n) or n.startswith("commissione") or n.startswith("consiglio del municipio"):
        return "istituzione"
    if n.startswith(STREET_WORDS):
        return "strada"
    if any(w in n for w in VENUE_WORDS):
        return "luogo"
    if n.startswith(("quartiere ", "rione ", "zona ", "quadrante ")):
        return "quartiere"
    return "luogo"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="docs/wiki")
    ap.add_argument("--gazetteer", default="gazetteer/gazetteer.json")
    ap.add_argument("--registry", default=None, help="registro_fonti.csv (13 Oct 2026)")
    a = ap.parse_args()

    zones, alias_to_zone = load_gazetteer(a.gazetteer)

    # ---- 1. read every news item --------------------------------------------------
    items = []
    for f in sorted(glob.glob(os.path.join(a.input, "*.csv"))):
        if "notizie" not in os.path.basename(f):
            continue
        with open(f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                items.append(r)
    items = [r for r in items if r.get("dedup_stato") != "duplicato"]

    # ---- 2. schedario: luoghi ---------------------------------------------------------
    place_index = {}   # norm -> id
    places = {}        # id -> record
    counter = Counter()

    def place_id(raw):
        n = norm(raw)
        if not n:
            return None
        if n in place_index:
            pid = place_index[n]
        else:
            pid = f"L-{len(places) + 1:04d}"
            place_index[n] = pid
            places[pid] = {"id": pid, "nome": raw.strip(), "alias": [], "tipo": classify_place(raw),
                           "zona": alias_to_zone.get(n), "municipi": Counter(), "n": 0}
        rec = places[pid]
        if raw.strip() != rec["nome"] and raw.strip() not in rec["alias"]:
            rec["alias"].append(raw.strip())
        return pid

    # ---- 3. diario -------------------------------------------------------------------
    diary = []
    threads = defaultdict(list)
    for r in items:
        pids = []
        for raw in (r.get("luoghi") or "").split(";"):
            pid = place_id(raw)
            if pid:
                pids.append(pid)
                places[pid]["n"] += 1
                if r.get("municipio"):
                    places[pid]["municipi"][r["municipio"]] += 1
        zona = r.get("zona") or ""
        if not zona:
            for pid in pids:
                if places[pid]["zona"]:
                    zona = places[pid]["zona"]
                    break
        date = r.get("data_fatto") or r.get("data_pubblicazione") or ""
        e = {
            "id": r["id"], "data": date, "data_pubblicazione": r.get("data_pubblicazione", ""),
            "fonte": r["fonte"], "tipo": r.get("tipo", ""), "titolo": r.get("titolo", ""),
            "municipio": r.get("municipio", ""), "zona": zona, "luoghi": pids,
            "questione": r.get("vicenda_id") or "", "qualita": r.get("qualita", ""),
            "dedup": r.get("dedup_stato", ""),
            "riferimento": (r.get("evidenza_url") or "") + ((" " + r["evidenza_locale"]) if r.get("evidenza_locale") else ""),
        }
        diary.append(e)
        if e["questione"]:
            threads[e["questione"]].append(e)
    diary.sort(key=lambda e: (e["data"], e["id"]))

    # ---- 4. schedario: questioni ---------------------------------------------------
    questioni = {}
    for vid, es in threads.items():
        es.sort(key=lambda e: (e["data"], e["id"]))
        best = sorted(es, key=lambda e: ({"alta": 0, "media": 1, "bassa": 2}.get(e["qualita"], 3), e["data"]))[0]
        mun = Counter(e["municipio"] for e in es if e["municipio"]).most_common(1)
        zon = Counter(e["zona"] for e in es if e["zona"]).most_common(1)
        lp = Counter(p for e in es for p in e["luoghi"])
        main_places = [p for p, _ in lp.most_common() if places[p]["tipo"] != "istituzione"]
        main = main_places[0] if main_places else None
        share = (sum(1 for e in es if main in e["luoghi"]) / len(es)) if main else 0.0
        coerenza = "alta" if share >= 0.75 else "media" if share >= 0.5 else "bassa"
        questioni[vid] = {
            "id": f"Q-{vid}", "vicenda": vid, "titolo": best["titolo"],
            "coerenza": coerenza, "luogo_principale": main,
            "tipo": Counter(e["tipo"] for e in es).most_common(1)[0][0],
            "municipio": mun[0][0] if mun else "", "zona": zon[0][0] if zon else "",
            "dal": es[0]["data"], "al": es[-1]["data"], "voci": len(es),
            "fonti": sorted({e["fonte"] for e in es}),
            "luoghi": [p for p, _ in lp.most_common(6)],
            "stato": "aperta" if len(es) >= 2 else "singola",
        }

    # ---- 5. schedario: soggetti -----------------------------------------------------
    soggetti = {}
    for pid, p in places.items():
        if p["tipo"] == "istituzione":
            soggetti[f"S-{pid[2:]}"] = {"id": f"S-{pid[2:]}", "nome": p["nome"], "alias": p["alias"],
                                        "tipo": "istituzione", "zona": None, "municipio": p["municipi"].most_common(1)[0][0] if p["municipi"] else "",
                                        "origine": "corpus giugno 2026", "n": p["n"]}
    if a.registry and os.path.exists(a.registry):
        with open(a.registry, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r.get("decisione") != "tenere":
                    continue
                sid = f"S-{r['chiave']}"
                soggetti[sid] = {"id": sid, "nome": r["nome"], "alias": [], "tipo": r["tipo"], "zona": r.get("zona_qn") or None,
                                 "municipio": r.get("municipio", ""), "canale": r.get("canale", ""), "link": r.get("link") or r.get("facebook") or "",
                                 "origine": "registro fonti 13 ott 2026", "n": 0}
                # link the registry source to a corpus place with the same normalised name
                n = norm(r["nome"])
                if n in place_index:
                    soggetti[sid]["luogo"] = place_index[n]

    # ---- 6. write data ---------------------------------------------------------------
    os.makedirs(a.out, exist_ok=True)
    for p in places.values():
        p["municipi"] = dict(p["municipi"].most_common())
    sched = {"versione": "2026-06.1", "fonte_dati": "studio fonti giugno 2026 (Drive, Fonti 2026-06) + registro fonti 13 ott 2026",
             "luoghi": sorted(places.values(), key=lambda p: -p["n"]),
             "soggetti": sorted(soggetti.values(), key=lambda s: (s["tipo"], s["nome"])),
             "questioni": sorted(questioni.values(), key=lambda q: (-q["voci"], q["dal"]))}
    json.dump(sched, open(os.path.join(a.out, "schedario.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"versione": "2026-06.1", "voci": diary}, open(os.path.join(a.out, "diario.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---- 7. pages per municipio -------------------------------------------------------
    pages_dir = os.path.join(a.out, "municipi")
    os.makedirs(pages_dir, exist_ok=True)
    index = ["# Wiki di contesto — giugno 2026 (generato)", "",
             "Pagine generate da `schedario.json` e `diario.json`; non modificare a mano, rigenerare con `tools/wiki/build_wiki.py`.", "",
             f"Voci di diario: {len(diary)} · questioni: {len(questioni)} (aperte, cioè con almeno due voci: {sum(1 for q in questioni.values() if q['stato']=='aperta')}) · luoghi: {len(places)} · soggetti: {len(soggetti)}", "",
             "| Municipio | voci | questioni aperte | luoghi citati | soggetti registrati |", "|---|---|---|---|---|"]
    for m in ROMAN:
        es = [e for e in diary if e["municipio"] == m]
        qs = [q for q in questioni.values() if q["municipio"] == m and q["stato"] == "aperta"]
        qs.sort(key=lambda q: (-q["voci"], q["dal"]))
        lp = Counter(p for e in es for p in e["luoghi"])
        ss = [s for s in soggetti.values() if s.get("municipio") == m]
        index.append(f"| [{m}](municipi/{m}.md) | {len(es)} | {len(qs)} | {len(lp)} | {len(ss)} |")
        out = [f"# Municipio {m} — contesto di giugno 2026", "",
               f"Voci di diario: {len(es)} · questioni aperte: {len(qs)} · luoghi citati: {len(lp)} · soggetti registrati: {len(ss)}", "",
               "## Questioni aperte", "",
               "Una questione è aperta quando più voci di diario la riguardano. Il raggruppamento è quello dello studio fonti (stessa data e stesso luogo, oggetto a volte incerto): la *coerenza* dice quanta parte delle voci cita lo stesso luogo principale. Ordine: per numero di voci.", ""]
        for q in qs[:40]:
            out.append(f"### {q['titolo']}  `{q['id']}`")
            out.append(f"*{q['tipo']}* · dal {q['dal']} al {q['al']} · {q['voci']} voci · fonti: {', '.join(q['fonti'])}" + (f" · zona: {q['zona']}" if q['zona'] else "") + f" · coerenza del raggruppamento: **{q['coerenza']}**")
            if q["luoghi"]:
                out.append("Luoghi: " + "; ".join(places[p]["nome"] for p in q["luoghi"]))
            out.append("")
            for e in threads[q["vicenda"]]:
                out.append(f"- {e['data'] or '—'} · [{e['fonte']}] {e['titolo']}" + (f" — {e['riferimento']}" if e['riferimento'] else ""))
            out.append("")
        out += ["## Luoghi più citati", "", "| luogo | tipo | zona | citazioni |", "|---|---|---|---|"]
        for pid, n in lp.most_common(30):
            p = places[pid]
            out.append(f"| {p['nome']} | {p['tipo']} | {p['zona'] or '—'} | {n} |")
        out += ["", "## Soggetti registrati (registro fonti, 13 ottobre 2026)", "", "| soggetto | tipo | zona | canale |", "|---|---|---|---|"]
        for s in sorted(ss, key=lambda s: (s["tipo"], s["nome"])):
            out.append(f"| {s['nome']} | {s['tipo']} | {s.get('zona') or '—'} | {s.get('canale','')} |")
        out += ["", "## Cronologia del mese", ""]
        for e in es:
            out.append(f"- {e['data'] or '—'} · [{e['fonte']}] {e['titolo']}" + (f" (→ {questioni[e['questione']]['id']})" if e['questione'] in questioni else ""))
        open(os.path.join(pages_dir, f"{m}.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    open(os.path.join(a.out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    print(f"diario {len(diary)} · questioni {len(questioni)} · luoghi {len(places)} · soggetti {len(soggetti)} → {a.out}")


if __name__ == "__main__":
    main()

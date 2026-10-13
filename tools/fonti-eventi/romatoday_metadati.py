"""Righe di RomaToday raccolte a mano dall'owner (titolo, data, link) e date ricavate dal link.

Uso: romatoday_metadati.py FOGLIO.csv DIR

RomaToday esclude gli agenti AI nel robots.txt e riserva l'estrazione di testi e dati: le sue
pagine non si aprono mai. Si usano solo titolo, data e link raccolti da una persona (DEC-108,
CRONACA_PROCESSO_2026-10.md §5.1). Scrive DIR/rt_items.json.
"""
import csv, json, re, sys

MESI = {m: i for i, m in enumerate(["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
                                    "agosto", "settembre", "ottobre", "novembre", "dicembre"], 1)}
_M = "|".join(MESI)
_DATA = re.compile(r"((?:\d{1,2}-)+)(" + _M + r")(?:-((?:\d{1,2}-)+)(" + _M + r"))?-(20\d\d)$")


def date_da_slug(slug):
    """('AAAA-MM-GG', 'AAAA-MM-GG') dal fondo dello slug, o (None, None).

    'pooh60-palazzo-dello-sport-15-16-ottobre-2026' -> 15 e 16 ottobre;
    'festa-autunno-31-ottobre-1-novembre-2026' -> 31 ottobre e 1 novembre."""
    m = _DATA.search(slug.lower())
    if not m:
        return None, None
    anno, g1, m1 = int(m.group(5)), [int(x) for x in m.group(1).strip("-").split("-")], MESI[m.group(2)]
    if m.group(4):
        g2, m2 = [int(x) for x in m.group(3).strip("-").split("-")], MESI[m.group(4)]
        return f"{anno}-{m1:02d}-{g1[0]:02d}", f"{anno}-{m2:02d}-{g2[-1]:02d}"
    return f"{anno}-{m1:02d}-{g1[0]:02d}", f"{anno}-{m1:02d}-{g1[-1]:02d}"


def righe(path):
    out, visti = [], set()
    for r in csv.reader(open(path, encoding="utf-8")):
        if len(r) < 3 or not r[2].startswith("http") or r[2] in visti:
            continue
        visti.add(r[2])
        slug = r[2].rstrip("/").rsplit("/", 1)[-1].removesuffix(".html")
        inizio, fine = date_da_slug(slug)
        out.append({"id": f"RT{len(out) + 1:03d}", "titolo": r[0].strip(), "slug": slug.lower(), "url": r[2].strip(),
                    "inizio_slug": inizio, "fine_slug": fine})
    return out


if __name__ == "__main__":
    rows = righe(sys.argv[1])
    json.dump(rows, open(sys.argv[2] + "/rt_items.json", "w"), ensure_ascii=False, indent=1)
    print(len(rows), "righe;", sum(1 for x in rows if x["inizio_slug"]), "con data nel link")

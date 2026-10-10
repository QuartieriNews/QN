"""Prepara i lotti di lettura delle due passate.

Uso: prepara_lotti.py DIR SCHEDE.jsonl [SCHEDE.jsonl ...]

- Passata in avanti: i fatti ufficiali nel Comune di Roma (esito diverso da F), divisi a
  pettine in 8 lotti -> DIR/avanti/lotto_N.json, letti secondo ISTRUZIONI_AVANTI.md.
- Passata inversa: i titoli candidati (DIR/censimento/candidati.json, da filtro.py) in tre
  decadi, ciascuna con i fatti ufficiali pubblicati da 3 giorni prima a 8 giorni dopo
  -> DIR/inverso/lotto_N.json, letti secondo ISTRUZIONI_INVERSO.md.

Le schede ufficiali sono quelle della tabella di giugno (runs/2026-10-09, su Drive).
"""
import datetime as dt, json, os, sys

FONTI = {"C1": "Questura di Roma", "C2": "Carabinieri", "C3": "Procura", "C4": "Vigili del Fuoco",
         "C5": "Polizia Locale", "C6": "Guardia di Finanza"}
LOTTI_AVANTI = 8
DECADI = [(1, 10), (11, 20), (21, 31)]


def fatti_ufficiali(paths):
    out = []
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if r["fuori_roma"] or r["esito"] == "F":
                continue
            out.append({"id": r["id"], "fonte": FONTI[r["fonte"]], "pubblicato": r["data_pubblicazione"],
                        "data_fatto": r["data_fatto"], "fatto": r["fatto"], "luoghi": r["luoghi_testo"],
                        "municipio": r["municipio"], "esito": r["esito"], "pagine": r["pagine"]})
    return out


def lotti_avanti(facts, n=LOTTI_AVANTI):
    return [facts[i::n] for i in range(n)]


def lotti_inversi(candidati, facts):
    day = dt.date.fromisoformat
    mese = candidati[0]["data"][:7] if candidati else "2026-06"
    out = []
    for a, b in DECADI:
        lo = day(f"{mese}-{a:02d}")
        hi = lo + dt.timedelta(days=b - a)
        tit = [c for c in candidati if lo <= day(c["data"]) <= hi]
        fu = [{k: f[k] for k in ("id", "fonte", "pubblicato", "data_fatto", "fatto", "luoghi", "pagine")}
              for f in sorted(facts, key=lambda f: f["pubblicato"])
              if lo - dt.timedelta(days=3) <= day(f["pubblicato"]) <= hi + dt.timedelta(days=8)]
        out.append({"titoli": tit, "fatti_ufficiali": fu})
    return out


def main(base, paths):
    facts = fatti_ufficiali(paths)
    for sub in ("avanti", "inverso"):
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    for i, lot in enumerate(lotti_avanti(facts), 1):
        json.dump(lot, open(f"{base}/avanti/lotto_{i}.json", "w"), ensure_ascii=False, indent=1)
    cand_path = f"{base}/censimento/candidati.json"
    if os.path.exists(cand_path):
        for i, lot in enumerate(lotti_inversi(json.load(open(cand_path)), facts), 1):
            json.dump(lot, open(f"{base}/inverso/lotto_{i}.json", "w"), ensure_ascii=False, indent=0)
    print(len(facts), "fatti ufficiali a Roma")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])

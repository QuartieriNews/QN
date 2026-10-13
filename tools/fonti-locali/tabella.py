"""Tabelle del rapporto dalle fonti verificate.

Uso: tabella.py RUN_DIR [--md]

Legge RUN_DIR/fonti_pagine.json (una voce per pagina o per Municipio, con le fonti e i
verdetti) e scrive RUN_DIR/riepilogo.json (conteggi per pagina e per verdetto). Con --md
stampa le tabelle Markdown per pagina, per Municipio e per fonte, pronte per il rapporto.
Nessun titolo e nessun nome di persona entrano qui: solo quello che gli agenti hanno
riportato (enti, siti, URL, date, conteggi).
"""
import collections
import json
import os
import sys

VERDETTI = ("usabile", "solo_metadati", "canale_chiuso", "da_verificare", "inattiva", "fuori_territorio", "non_raggiungibile")
ETICHETTA = {"usabile": "usabili", "solo_metadati": "solo metadati", "canale_chiuso": "solo social", "da_verificare": "da verificare",
             "inattiva": "inattive", "fuori_territorio": "fuori territorio", "non_raggiungibile": "non raggiungibili"}


def chiave_fonte(f):
    return f["url"].rstrip("/").lower().replace("http://", "https://").replace("https://www.", "https://")


def carica(run_dir):
    return json.load(open(os.path.join(run_dir, "fonti_pagine.json")))


def riepilogo(voci):
    per_pagina, per_verdetto, fonti = [], collections.Counter(), {}
    for v in voci:
        c = collections.Counter(f["verdetto"] for f in v.get("fonti", []))
        per_verdetto.update(c)
        per_pagina.append({"slug": v["slug"], "tipo": v.get("tipo", "pagina"), "municipio": v.get("municipio"), "fallito": v.get("fallito", False),
                           "ricerche": v.get("ricerche"), "candidate": len(v.get("fonti", [])), **{k: c.get(k, 0) for k in VERDETTI}})
        for f in v.get("fonti", []):
            k = chiave_fonte(f)
            fonti.setdefault(k, {"nome": f["nome"], "url": f["url"], "tipo": f["tipo"], "canale": f["canale"], "territorio": f["territorio"],
                                 "verdetti": {}, "conteggio_finestra": f.get("conteggio_finestra"), "marca": f.get("marca"), "ultima_data": f.get("ultima_data")})
            fonti[k]["verdetti"][v["slug"]] = f["verdetto"]
    trasversali = {k: f for k, f in fonti.items() if len(f["verdetti"]) > 1}
    return {"voci": len(voci), "pagine": sum(1 for v in voci if v.get("tipo", "pagina") == "pagina"),
            "pagine_con_usabile": sum(1 for p in per_pagina if p["tipo"] == "pagina" and p["usabile"] > 0),
            "pagine_senza_nulla": sum(1 for p in per_pagina if p["tipo"] == "pagina" and p["candidate"] == 0),
            "fonti_distinte": len(fonti), "fonti_trasversali": len(trasversali), "per_verdetto": dict(per_verdetto),
            "ricerche_totali": sum(p["ricerche"] or 0 for p in per_pagina), "per_pagina": per_pagina}


def md_pagine(voci, rp, tipo):
    righe = ["| Pagina | Mun. | Cand. | " + " | ".join(ETICHETTA[k].capitalize() for k in VERDETTI) + " | Fonti usabili (territorio) |", "|---|---|---|" + "---|" * len(VERDETTI) + "---|"]
    per_slug = {v["slug"]: v for v in voci}
    for p in sorted(rp["per_pagina"], key=lambda x: x["slug"]):
        if p["tipo"] != tipo:
            continue
        v = per_slug[p["slug"]]
        us = "; ".join(f"{f['nome']} ({f['territorio']})" for f in v.get("fonti", []) if f["verdetto"] == "usabile") or "—"
        nome = v.get("pagina") or p["slug"]
        if p["fallito"]:
            us = "*agente fallito*"
        righe.append(f"| {nome} | {p['municipio'] or ''} | {p['candidate']} | " + " | ".join(str(p[k]) for k in VERDETTI) + f" | {us} |")
    return "\n".join(righe)


def md_fonti(voci, verdetti_voluti=("usabile", "solo_metadati"), con_motivo=True):
    """Una riga per fonte distinta; con_motivo=False dà la tabella compatta (il motivo resta nel JSON)."""
    righe = ["| Fonte | Tipo | Canale | Territorio | Pagine | Verdetto | Post lug–set | Ultima data |" + (" Canale lecito / motivo |" if con_motivo else ""),
             "|---|---|---|---|---|---|---|---|" + ("---|" if con_motivo else "")]
    viste = {}
    for v in voci:
        for f in v.get("fonti", []):
            if f["verdetto"] not in verdetti_voluti:
                continue
            k = chiave_fonte(f)
            if k in viste:
                viste[k]["pagine"].append(v["slug"])
                continue
            viste[k] = {**f, "pagine": [v["slug"]]}
    for f in sorted(viste.values(), key=lambda x: (x["verdetto"], x["nome"].lower())):
        cont = f"{f['conteggio_finestra']} ({f['marca']})" if f.get("conteggio_finestra") is not None else f.get("marca", "—")
        motivo = (f.get("motivo") or "").replace("|", "/")
        terr = f"{f['territorio']}: {f['territorio_note'].replace('|', '/')}" if con_motivo else f["territorio"]
        righe.append(f"| [{f['nome']}]({f['url']}) | {f['tipo']} | {f['canale']} | {terr} | {', '.join(f['pagine'])} | {f['verdetto']} | {cont} | {f.get('ultima_data') or '—'} |" + (f" {motivo} |" if con_motivo else ""))
    return "\n".join(righe)


def main(argv):
    run_dir = argv[1]
    voci = carica(run_dir)
    rp = riepilogo(voci)
    json.dump(rp, open(os.path.join(run_dir, "riepilogo.json"), "w"), ensure_ascii=False, indent=1)
    if "--md" in argv:
        print("### Per pagina\n\n" + md_pagine(voci, rp, "pagina"))
        print("\n### Per Municipio\n\n" + md_pagine(voci, rp, "municipio"))
        print("\n### Fonti usabili o con i soli metadati\n\n" + md_fonti(voci))
        print("\n### Fonti da verificare\n\n" + md_fonti(voci, ("da_verificare",), con_motivo=False))
        print("\n### Canali social, per la raccolta manuale\n\n" + md_fonti(voci, ("canale_chiuso",), con_motivo=False))
        print("\n### Scartate: inattive, fuori territorio, non raggiungibili\n\n" + md_fonti(voci, ("inattiva", "fuori_territorio", "non_raggiungibile"), con_motivo=False))
    print(json.dumps({k: v for k, v in rp.items() if k != "per_pagina"}, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)

"""Lotti per l'abbinamento dei titoli delle testate chiuse ai fatti noti (ISTRUZIONI_CHIUSE.md).

Uso: prepara_chiuse.py DIR QN_PKG SCHEDE_UFFICIALI.jsonl... -- FATTI_APERTE.jsonl...

Titoli: DIR/chiuse/candidati.json (chiuse_filtro.py), a finestre di tre giorni. Per ogni
finestra i fatti noti dei giorni vicini: ufficiali (schede della tabella di giugno, esclusi i
fuori Roma) e delle testate aperte non già abbinati a un fatto ufficiale (passata inversa).
Scrive DIR/chiuse/lotto_N.json.
"""
import datetime as dt, json, os, sys

GIORNI = 3


def jl(paths):
    return [json.loads(l) for p in paths for l in open(p) if l.strip()]


def main(base, pkg, ufficiali, aperte):
    day = dt.date.fromisoformat
    titoli = json.load(open(f"{base}/chiuse/candidati.json"))
    aperti = jl(aperte)
    testate_di = {}
    for x in aperti:
        if x.get("ufficiale"):
            testate_di.setdefault(x["ufficiale"], set()).update(x["testate"])
    uff = [{"id": s["id"], "fonte": s["fonte"], "data": s["data_fatto"] or s["data_pubblicazione"],
            "pubblicato": s["data_pubblicazione"], "fatto": s["fatto"], "luoghi": s["luoghi_testo"],
            "pagine": s["pagine"], "testate_aperte": sorted(testate_di.get(s["id"], []))}
           for s in jl(ufficiali) if not s["fuori_roma"]]
    pr = [{"id": x["fid"], "data": x["data"], "tipo": x["tipo"], "fatto": x["fatto"], "luogo": x.get("luogo"),
           "pagina_qn": x.get("pagina_qn"), "testate": sorted(set(x["testate"]))} for x in aperti if not x.get("ufficiale")]
    d0, d1 = day(min(t["data"] for t in titoli)), day(max(t["data"] for t in titoli))
    n, a = 0, d0
    while a <= d1:
        b = a + dt.timedelta(days=GIORNI - 1)
        tit = [t for t in titoli if a <= day(t["data"]) <= b]
        if tit:
            n += 1
            f_u = [f for f in uff if a - dt.timedelta(days=4) <= day(f["data"]) <= b + dt.timedelta(days=4)
                   or a - dt.timedelta(days=3) <= day(f["pubblicato"]) <= b + dt.timedelta(days=8)]
            f_p = [f for f in pr if a - dt.timedelta(days=4) <= day(f["data"]) <= b + dt.timedelta(days=4)]
            lot = {"QN_PKG": pkg, "titoli": [{k: t[k] for k in ("cid", "testata", "editore", "data", "ora", "titolo", "link")}
                                            for t in tit], "fatti": f_u + f_p}
            json.dump(lot, open(f"{base}/chiuse/lotto_{n}.json", "w"), ensure_ascii=False, indent=0)
            print(n, a, b, len(tit), "titoli,", len(f_u), "ufficiali,", len(f_p), "aperte")
        a = b + dt.timedelta(days=1)
    return n


if __name__ == "__main__":
    if "--" not in sys.argv or len(sys.argv) < 5:
        sys.exit(__doc__)
    i = sys.argv.index("--")
    main(sys.argv[1], sys.argv[2], sys.argv[3:i], sys.argv[i + 1:])

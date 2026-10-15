"""Compila la prova: conteggi per il repository, righe per fatto per Drive.

Uso: compila.py DIR MATRICE.csv

Legge DIR/avanti/{lotto,risultati}_N, DIR/inverso/{fatti,scarti}_N e DIR/censimento/candidati.json;
MATRICE è il conteggio per pagina della tabella di giugno
(tools/geo-assign/runs/2026-10-09/matrice_giugno_conteggi.csv).
Scrive DIR/riepilogo.json (solo conteggi e nomi di testate: si può versionare),
DIR/righe_avanti.json e DIR/righe_inverso.json (titoli e link: solo Drive, DEC-102/104).
"""
import collections, csv, glob, json, os, re, sys, unicodedata

ENTE = re.compile(r"carabinier|polizia|poliziott|questura|commissariat|vigili|pompier|finanza|gdf|agenti|procura|nas\b|militari")
TUTTE = {"certa", "probabile"}


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def testate(r, livelli=TUTTE):
    return sorted({t["testata"] for t in r["testate"] if t["corrispondenza"] in livelli})


def cercato(r):
    """Una riga senza ricerche propria non conta come cercata, anche se un agente vi ha
    copiato risultati di un'altra ricerca: la misura resta per fatto cercato."""
    return bool(r.get("ricerche")) and not r.get("nota", "").startswith("NON CERCATO")


def pagine(xs, attive):
    s = set()
    for x in xs:
        if x.get("pagina_qn"):
            s |= {p.strip() for p in str(x["pagina_qn"]).split("+")}
    return s & attive


def presenze(xs):
    return sum(len(str(x["pagina_qn"]).split("+")) for x in xs if x.get("pagina_qn"))


def ripetuti(xs):
    return sorted({x for x in xs if xs.count(x) > 1})


def carica_avanti(base):
    """Fatti dei lotti e risultati dei lettori; un lotto letto due volte o un id ignoto fermano
    la compilazione invece di sovrascriversi in silenzio (ISTRUZIONI_AVANTI.md, AGENTS.md)."""
    lotti = [f for p in sorted(glob.glob(f"{base}/avanti/lotto_*.json")) for f in json.load(open(p))]
    if ripetuti([f["id"] for f in lotti]):
        sys.exit(f"compila: id ripetuti nei lotti avanti: {ripetuti([f['id'] for f in lotti])}")
    facts = {f["id"]: f for f in lotti}
    ris = [r for p in sorted(glob.glob(f"{base}/avanti/risultati_*.jsonl")) for r in jl(p)]
    if ripetuti([r["id"] for r in ris]):
        sys.exit(f"compila: risultati ripetuti (lotto letto due volte?): {ripetuti([r['id'] for r in ris])}")
    ignoti = sorted(r["id"] for r in ris if r["id"] not in facts)
    if ignoti:
        sys.exit(f"compila: risultati per id che non sono in nessun lotto: {ignoti}")
    return facts, {r["id"]: r for r in ris if cercato(r)}


def avanti(base):
    facts, res = carica_avanti(base)
    R = {"fatti_ufficiali_roma": len(facts), "fatti_cercati": len(res),
         "ricerche": sum(len(r["ricerche"]) for r in res.values()),
         "non_cercati_per_fonte": dict(collections.Counter(f["fonte"] for i, f in facts.items() if i not in res))}
    for nome, liv in (("certa_o_probabile", TUTTE), ("solo_certa", {"certa"})):
        dist, per_t = collections.Counter(), collections.Counter()
        for r in res.values():
            ts = testate(r, liv)
            dist[min(len(ts), 4)] += 1
            per_t.update(ts)
        R[nome] = {"distribuzione_n_testate": {("4+" if k == 4 else str(k)): v for k, v in sorted(dist.items())},
                   "fatti_con_almeno_una": sum(v for k, v in dist.items() if k), "per_testata": per_t.most_common()}
    cov = [r for r in res.values() if testate(r)]
    R["media_testate_per_fatto_ripreso"] = round(sum(len(testate(r)) for r in cov) / max(len(cov), 1), 2)
    for chiave, campo in (("per_fonte", "fonte"), ("per_esito", "esito")):
        c = collections.defaultdict(lambda: [0, 0])
        for i, r in res.items():
            c[facts[i][campo]][0] += 1
            c[facts[i][campo]][1] += bool(testate(r))
        R[chiave] = {k: {"cercati": v[0], "ripresi": v[1]} for k, v in sorted(c.items())}
    righe = [{"id": i, "fonte": f["fonte"], "pubblicato": f["pubblicato"], "fatto": f["fatto"], "esito": f["esito"],
              "pagine": "+".join(f["pagine"]), "cercato": i in res,
              "n_testate": len(testate(res[i])) if i in res else None,
              "n_testate_certe": len(testate(res[i], {"certa"})) if i in res else None,
              "testate": "; ".join(f"{t['testata']} ({t['corrispondenza']}{', ' + t['data'] if t.get('data') else ''})"
                                   for t in res[i]["testate"]) if i in res else "",
              "link": " ".join(t["url"] for t in res[i]["testate"]) if i in res else "",
              "nota": res[i].get("nota", "") if i in res else "non cercato: tetto di ricerche del turno"}
             for i, f in facts.items()]
    return R, righe


def inversa(base, attive, pagine_uff, presenze_uff, ufficiali=None):
    cand = {c["sid"]: c for c in json.load(open(f"{base}/censimento/candidati.json"))}
    fatti = [x for p in sorted(glob.glob(f"{base}/inverso/fatti_*.jsonl")) for x in jl(p)]
    scarti = [x for p in sorted(glob.glob(f"{base}/inverso/scarti_*.jsonl")) for x in jl(p)]
    # ogni sid esattamente una volta, in uno dei due file (ISTRUZIONI_INVERSO.md): doppioni, sid ignoti e
    # sid mancanti fermano la compilazione
    sids = [s for x in fatti for s in x["sid"]] + [x["sid"] for x in scarti]
    if ripetuti(sids) or ripetuti([x["fid"] for x in fatti]):
        sys.exit(f"compila: sid o fid ripetuti nella passata inversa (lotto letto due volte?): "
                 f"{ripetuti(sids) + ripetuti([x['fid'] for x in fatti])}")
    if [s for s in sids if s not in cand]:
        sys.exit(f"compila: sid che non sono fra i candidati: {sorted(s for s in sids if s not in cand)}")
    if set(cand) - set(sids):
        sys.exit(f"compila: candidati senza esito nella passata inversa: {sorted(set(cand) - set(sids))[:20]}")
    # «ufficiale» deve essere l'id di un fatto ufficiale del lotto (ISTRUZIONI_INVERSO.md, punto 3)
    if ufficiali is not None and {x["ufficiale"] for x in fatti if x.get("ufficiale")} - set(ufficiali):
        sys.exit(f"compila: fatti abbinati a id ufficiali ignoti: "
                 f"{sorted({x['ufficiale'] for x in fatti if x.get('ufficiale')} - set(ufficiali))}")
    solo = [x for x in fatti if not x.get("ufficiale")]
    due = [x for x in solo if len(set(x["testate"])) >= 2]
    tit = lambda x: " ".join(cand[s]["titolo"] for s in x["sid"] if s in cand)
    R = {"titoli_candidati": len(cand), "titoli_classificati": sum(len(x["sid"]) for x in fatti) + len(scarti),
         "classi": dict(collections.Counter(x["classe"] for x in scarti), cronaca_roma=sum(len(x["sid"]) for x in fatti)),
         "fatti_cronaca_roma": len(fatti),
         "con_fatto_ufficiale": {"totale": len(fatti) - len(solo),
                                 "certa": sum(1 for x in fatti if x.get("ufficiale") and x.get("corrispondenza") == "certa")},
         "fatti_ufficiali_ritrovati": len({x["ufficiale"] for x in fatti if x.get("ufficiale")}),
         "solo_stampa": len(solo),
         "solo_stampa_per_tipo": collections.Counter(x["tipo"] for x in solo).most_common(),
         "solo_stampa_per_livello": dict(collections.Counter(x["livello"] for x in solo)),
         "solo_stampa_con_ente_nel_titolo": sum(1 for x in solo if ENTE.search(norm(tit(x) + " " + x["fatto"]))),
         "solo_stampa_con_almeno_due_testate": len(due),
         "n_testate_per_fatto": {str(k): v for k, v in sorted(collections.Counter(min(len(set(x["testate"])), 3) for x in fatti).items())},
         "per_testata": collections.Counter(t for x in fatti for t in set(x["testate"])).most_common(),
         "solo_stampa_per_testata": collections.Counter(t for x in solo for t in set(x["testate"])).most_common()}
    R["scenari"] = {
        "A_ufficiali_pubbliche": {"fatti": None, "presenze": presenze_uff, "pagine_con_almeno_uno": len(pagine_uff)},
        "B_piu_testate_aperte_dopo_conferma_massimo": {"fatti_in_piu": len(solo), "presenze_in_piu": presenze(solo),
                                                       "pagine_con_almeno_uno": len(pagine_uff | pagine(solo, attive))},
        "C_piu_fatti_su_due_testate_aperte": {"fatti_in_piu": len(due), "presenze_in_piu": presenze(due),
                                              "pagine_con_almeno_uno": len(pagine_uff | pagine(due, attive))},
        "pagine_attive": len(attive)}
    righe = [{"fid": x["fid"], "data": x["data"], "tipo": x["tipo"], "fatto": x["fatto"], "luogo": x.get("luogo"),
              "pagina_qn": x.get("pagina_qn"), "livello": x.get("livello"), "testate": "; ".join(sorted(set(x["testate"]))),
              "n_testate": len(set(x["testate"])), "ufficiale": x.get("ufficiale"), "corrispondenza": x.get("corrispondenza"),
              "titoli": " | ".join(cand[s]["titolo"] for s in x["sid"] if s in cand),
              "link": " ".join(cand[s]["link"] for s in x["sid"] if s in cand)} for x in fatti]
    return R, righe


def notizie_uniche(base):
    """Una riga per notizia: i fatti ufficiali (testate dalle due passate, unite) più i fatti
    trovati solo sulle testate aperte. I fatti ufficiali senza ricerca restano a parte:
    il loro conteggio di testate è incompleto."""
    facts, res = carica_avanti(base)
    facts = list(facts)
    inv = [x for p in sorted(glob.glob(f"{base}/inverso/fatti_*.jsonl")) for x in jl(p)]
    uscite = {i: set(testate(res[i])) if i in res else set() for i in facts}
    for x in inv:
        if x.get("ufficiale") in uscite:
            uscite[x["ufficiale"]] |= set(x["testate"])
    fascia = lambda n: str(n) if n < 5 else "5+"
    conta = lambda ns: {k: v for k, v in sorted(collections.Counter(fascia(n) for n in ns).items())}
    solo = [len(set(x["testate"])) for x in inv if not x.get("ufficiale")]
    return {"totale": len(facts) + len(solo),
            "ufficiali_cercati": conta(len(uscite[i]) for i in facts if i in res),
            "ufficiali_non_cercati": conta(len(uscite[i]) for i in facts if i not in res),
            "solo_testate_aperte": conta(solo)}


def main(base, matrice):
    rows = list(csv.DictReader(open(matrice, encoding="utf-8-sig"), delimiter=";"))
    attive = {r["slug"] for r in rows}
    pagine_uff = {r["slug"] for r in rows if int(r["Cronaca propri"]) > 0}
    presenze_uff = sum(int(r["Cronaca propri"]) for r in rows)
    ra, righe_a = avanti(base)
    ri, righe_i = inversa(base, attive, pagine_uff, presenze_uff, set(carica_avanti(base)[0]))
    ri["scenari"]["A_ufficiali_pubbliche"]["fatti"] = ra["fatti_ufficiali_roma"]
    cens = {os.path.basename(p)[:-5]: len(json.load(open(p))) for p in sorted(glob.glob(f"{base}/censimento/*.json"))
            if not p.endswith("candidati.json")}
    R = {"censimento_titoli_del_mese": cens, "notizie_uniche": notizie_uniche(base), "avanti": ra, "inversa": ri}
    for nome, obj in (("riepilogo", R), ("righe_avanti", righe_a), ("righe_inverso", righe_i)):
        with open(f"{base}/{nome}.json", "w") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
    return R


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    print(json.dumps(main(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=1))

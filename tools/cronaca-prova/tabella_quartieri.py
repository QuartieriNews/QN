"""Notizie di cronaca del mese per quartiere, con la regola delle due fonti (DEC-108, MVP).

Uso: tabella_quartieri.py DIR MATRICE.csv SCHEDE_UFFICIALI.jsonl... -- FATTI_APERTE.jsonl...
     (il mese viene da QN_MESE, di default 2026-06: i fatti nuovi delle testate chiuse fuori dal mese non contano)

Mette insieme tre insiemi di fatti:
- ufficiali (schede della tabella di giugno): sempre pubblicabili, la fonte è l'ente;
- delle testate aperte (passata inversa), con le pagine corrette da DIR/luoghi/luoghi_esito.jsonl;
- visti solo sulle testate chiuse (DIR/chiuse/nuovi_*.jsonl).
Le testate chiuse che riprendono un fatto (DIR/chiuse/abbinamenti_*.jsonl) aggiungono fonti.

Le fonti si contano per editore: due testate dello stesso gruppo (Il Messaggero e Leggo,
RomaToday e Today.it, Il Tempo e il Giornale) valgono una. Categorie:
  ufficiale                fonte ufficiale (con o senza giornali)
  stampa_due_fonti         almeno due editori e almeno una testata aperta: si può scrivere
  stampa_una_fonte         un solo editore: in osservazione, non si pubblica
  chiuse_due_fonti         solo testate chiuse, almeno due editori: segnale, non scrivibile
  chiuse_una_fonte         solo testate chiuse, un editore
Scrive DIR/tabella/fatti.json (per Drive), DIR/tabella/per_pagina.csv e DIR/tabella/riepilogo.json
(solo conteggi: si possono versionare; `seconda_fonte` dice da dove viene la seconda fonte dei
fatti «stampa_due_fonti», `abbinamenti_a_fatti_esclusi` quanti abbinamenti puntano a un fatto noto
ma fuori tabella: fuori mese, fuori Roma, non cronaca).
Gli abbinamenti devono coprire ogni `cid` una volta sola e citare fatti noti, e ogni «ufficiale»
dei fatti delle testate aperte deve essere l'id di una scheda (ISTRUZIONI_CHIUSE.md,
ISTRUZIONI_INVERSO.md): altrimenti il programma si ferma.
"""
import collections, csv, glob, json, os, sys

EDITORE_APERTE = {"Abitare a Roma": "Abitare a Roma", "Roma Daily News": "Roma Daily News",
                  "Il Faro Online": "Il Faro Online", "VignaClaraBlog": "VignaClaraBlog", "Dire": "Dire",
                  "Il Tempo": "Angelucci"}
PUBBLICABILI = ("ufficiale", "stampa_due_fonti")
CLASSI_CHIUSE = {"cronaca_roma", "cronaca_fuori", "giudiziaria", "non_cronaca"}   # ISTRUZIONI_CHIUSE.md
CORRISPONDENZE = {"certa", "probabile", None}
CATEGORIE = ("ufficiale", "stampa_due_fonti", "stampa_una_fonte", "chiuse_due_fonti", "chiuse_una_fonte")


def jl(paths):
    return [json.loads(l) for p in paths for l in open(p) if l.strip()]


def pagine_di(v):
    if not v:
        return []
    if isinstance(v, list):
        return [p for p in v if p]
    return [p.strip() for p in str(v).split("+") if p.strip()]


def categoria(f):
    if f["ufficiale"]:
        return "ufficiale"
    if f["aperte"]:
        return "stampa_due_fonti" if len(f["editori"]) >= 2 else "stampa_una_fonte"
    return "chiuse_due_fonti" if len(f["editori"]) >= 2 else "chiuse_una_fonte"


def main(base, matrice, ufficiali, aperte, mese=None):
    mese = mese or os.environ.get("QN_MESE", "2026-06")
    rows = list(csv.DictReader(open(matrice, encoding="utf-8-sig"), delimiter=";"))
    pagine = [(r["slug"], r["pagina"], r["municipio"]) for r in rows]
    attive = {p for p, _, _ in pagine}
    chiuse = {c["cid"]: c for c in json.load(open(f"{base}/chiuse/candidati.json"))}
    abb = jl(sorted(glob.glob(f"{base}/chiuse/abbinamenti_*.jsonl")))
    nuovi = jl(sorted(glob.glob(f"{base}/chiuse/nuovi_*.jsonl")))
    luoghi = {x["fid"]: x for x in jl(glob.glob(f"{base}/luoghi/luoghi_esito.jsonl"))}
    fatti, noti, ids_uff = {}, set(), set()   # noti: ogni id che un abbinamento può citare, anche se escluso
    for s in jl(ufficiali):
        noti.add(s["id"])
        ids_uff.add(s["id"])
        if s["fuori_roma"]:
            continue
        fatti[s["id"]] = {"id": s["id"], "origine": "ufficiale", "data": s["data_fatto"] or s["data_pubblicazione"],
                          "fatto": s["fatto"], "esito": s["esito"], "livello": s["livello_portata"],
                          "pagine": pagine_di(s["pagine"]) if s["esito"] in ("U", "M") else [],
                          "ufficiale": True, "aperte": set(), "chiuse": set(), "editori": {"ente"}, "link": []}
    # doppioni fra i fatti delle testate aperte (DIR/aperte_fusioni.json) e fatti su più pagine (M) che la
    # rilettura dei testi ha individuato (DIR/luoghi/pagine_multiple.json)
    fus_aperte = json.load(open(f"{base}/aperte_fusioni.json")) if os.path.exists(f"{base}/aperte_fusioni.json") else {}
    multiple = (json.load(open(f"{base}/luoghi/pagine_multiple.json"))
                if os.path.exists(f"{base}/luoghi/pagine_multiple.json") else {})
    rimandati = []
    for x in jl(aperte):
        noti.add(x["fid"])
        testate = set(x["testate"])
        if x["fid"] in fus_aperte:
            rimandati.append((fus_aperte[x["fid"]], testate))
            continue
        if x.get("ufficiale"):
            if x["ufficiale"] not in ids_uff:   # ISTRUZIONI_INVERSO.md, punto 3: l'id di una scheda ufficiale
                sys.exit(f"tabella_quartieri: il fatto {x['fid']} cita un id ufficiale ignoto: {x['ufficiale']}")
            if x["ufficiale"] in fatti:
                f = fatti[x["ufficiale"]]
                f["aperte"] |= testate
                f["editori"] |= {EDITORE_APERTE.get(t, t) for t in testate}
            continue   # stesso evento di una scheda ufficiale fuori Roma: escluso con lei
        l = luoghi.get(x["fid"], {})
        livello = l.get("livello") or x.get("livello")
        if livello in ("fuori", "non_cronaca"):
            continue
        pg = pagine_di(l.get("pagina_qn") if l else x.get("pagina_qn"))
        if x["fid"] in multiple:
            pg, livello = multiple[x["fid"]], "quartiere"
        fatti[x["fid"]] = {"id": x["fid"], "origine": "aperte", "data": x["data"], "fatto": x["fatto"],
                           "livello": livello, "pagine": pg if livello == "quartiere" or pg else [],
                           "ufficiale": False, "aperte": testate, "chiuse": set(),
                           "editori": {EDITORE_APERTE.get(t, t) for t in testate}, "link": []}
    for destinazione, testate in rimandati:
        if destinazione in fatti:
            fatti[destinazione]["aperte"] |= testate
            fatti[destinazione]["editori"] |= {EDITORE_APERTE.get(t, t) for t in testate}
    # fatti nuovi doppi fra lotti vicini (stesso fatto ai bordi delle finestre): DIR/chiuse/fusioni.json
    fusioni = json.load(open(f"{base}/chiuse/fusioni.json")) if os.path.exists(f"{base}/chiuse/fusioni.json") else {}
    for n in nuovi:
        noti.add(n["nid"])
        if n["nid"] in fusioni or not str(n.get("data", "")).startswith(mese):
            continue
        fatti[n["nid"]] = {"id": n["nid"], "origine": "chiuse", "data": n["data"], "fatto": n["fatto"],
                           "livello": n["livello"], "pagine": pagine_di(n.get("pagina_qn")), "ufficiale": False,
                           "aperte": set(), "chiuse": set(), "editori": set(), "link": []}
    for a in abb:   # un refuso del lettore (es. «cronaca-roma») si ferma qui, non diventa «non cronaca»
        if a.get("classe") not in CLASSI_CHIUSE or a.get("corrispondenza") not in CORRISPONDENZE:
            sys.exit(f"tabella_quartieri: abbinamento {a.get('cid')}: classe o corrispondenza fuori contratto "
                     f"({a.get('classe')!r}, {a.get('corrispondenza')!r})")
    cids = [a["cid"] for a in abb]
    doppi = sorted({c for c in cids if cids.count(c) > 1})
    if doppi:
        sys.exit(f"tabella_quartieri: cid ripetuti negli abbinamenti (lotto letto due volte?): {doppi}")
    if [c for c in cids if c not in chiuse]:
        sys.exit(f"tabella_quartieri: cid ignoti negli abbinamenti: {sorted(c for c in cids if c not in chiuse)}")
    if set(chiuse) - set(cids):   # una riga per ogni cid, nessuno escluso (ISTRUZIONI_CHIUSE.md)
        sys.exit(f"tabella_quartieri: candidati senza abbinamento: {sorted(set(chiuse) - set(cids))[:20]}")
    senza = sorted(a["cid"] for a in abb if a.get("classe") == "cronaca_roma" and not a.get("fatto"))
    if senza:   # cronaca romana va a un fatto noto o a un fatto nuovo, mai a nulla
        sys.exit(f"tabella_quartieri: titoli cronaca_roma senza fatto: {senza}")
    esclusi = 0
    for a in abb:
        if a.get("classe") != "cronaca_roma":
            continue
        dest = fusioni.get(a["fatto"], fus_aperte.get(a["fatto"], a["fatto"]))
        f, c = fatti.get(dest), chiuse[a["cid"]]
        if not f:
            if dest not in noti:
                sys.exit(f"tabella_quartieri: l'abbinamento {a['cid']} cita un fatto ignoto: {a['fatto']}")
            esclusi += 1   # fatto noto ma fuori tabella: fuori mese (lotti di bordo), fuori Roma, non cronaca
            continue
        f["chiuse"].add(c["testata"])
        f["editori"].add(c["editore"])
        f["link"].append(c["link"])
    for f in fatti.values():
        f["pagine"] = [p for p in f["pagine"] if p in attive]
        f["categoria"] = categoria(f)
        f["n_editori"] = len(f["editori"] - {"ente"})
    # tabella per pagina
    conta = {p: collections.Counter() for p in attive}
    for f in fatti.values():
        for p in f["pagine"]:
            conta[p][f["categoria"]] += 1
            if f["categoria"] in PUBBLICABILI:
                conta[p]["pubblicabili"] += 1
    os.makedirs(f"{base}/tabella", exist_ok=True)
    with open(f"{base}/tabella/per_pagina.csv", "w", encoding="utf-8-sig", newline="") as fo:
        w = csv.writer(fo, delimiter=";")
        w.writerow(["slug", "pagina", "municipio", "pubblicabili", *CATEGORIE])
        for p, nome, mun in pagine:
            w.writerow([p, nome, mun, conta[p]["pubblicabili"], *[conta[p][c] for c in CATEGORIE]])
    tot = collections.Counter(f["categoria"] for f in fatti.values())
    livelli = {c: dict(collections.Counter(("con pagina" if f["pagine"] else f["livello"] or "senza") for f in fatti.values()
                                           if f["categoria"] == c)) for c in CATEGORIE}
    coperte = lambda cats: sorted(p for p in attive if sum(conta[p][c] for c in cats) > 0)
    R = {"fatti_per_categoria": {c: tot[c] for c in CATEGORIE},
         "pubblicabili": sum(tot[c] for c in PUBBLICABILI),
         "fatti_per_livello": livelli,
         "pagine_coperte": {"solo_ufficiali": len(coperte(["ufficiale"])),
                            "ufficiali_piu_stampa_due_fonti": len(coperte(PUBBLICABILI)),
                            "se_bastasse_una_fonte": len(coperte(PUBBLICABILI + ("stampa_una_fonte",))),
                            "con_anche_le_chiuse_non_scrivibili": len(coperte(PUBBLICABILI + ("chiuse_due_fonti",)))},
         "pagine_attive": len(attive),
         "pagine_scoperte": [p for p, _, _ in pagine if p not in set(coperte(PUBBLICABILI))],
         "seconda_fonte": {"anche_da_aperte": sum(1 for f in fatti.values() if f["categoria"] == "stampa_due_fonti"
                                                  and len({EDITORE_APERTE.get(t, t) for t in f["aperte"]}) >= 2),
                           "solo_da_chiuse": sum(1 for f in fatti.values() if f["categoria"] == "stampa_due_fonti"
                                                 and len({EDITORE_APERTE.get(t, t) for t in f["aperte"]}) < 2)},
         "abbinamenti_a_fatti_esclusi": esclusi}
    json.dump(R, open(f"{base}/tabella/riepilogo.json", "w"), ensure_ascii=False, indent=1)
    out = [{**{k: v for k, v in f.items() if k not in ("aperte", "chiuse", "editori")},
            "aperte": sorted(f["aperte"]), "chiuse": sorted(f["chiuse"]), "editori": sorted(f["editori"])}
           for f in fatti.values()]
    json.dump(out, open(f"{base}/tabella/fatti.json", "w"), ensure_ascii=False, indent=0)
    return R


if __name__ == "__main__":
    if "--" not in sys.argv or len(sys.argv) < 5:
        sys.exit(__doc__)
    i = sys.argv.index("--")
    print(json.dumps(main(sys.argv[1], sys.argv[2], sys.argv[3:i], sys.argv[i + 1:]), ensure_ascii=False, indent=1))

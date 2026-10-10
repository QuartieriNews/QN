"""Controlli degli strumenti della prova Cronaca (nessuna rete, dati sintetici).

Uso: python3 tools/cronaca-prova/test_cronaca_prova.py
"""
import json, os, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compila, filtro, prepara_lotti  # noqa: E402

FALLITI = []


def check(nome, cond):
    print(("ok   " if cond else "FAIL ") + nome)
    if not cond:
        FALLITI.append(nome)


def scrivi(path, obj, jsonl=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        if jsonl:
            f.write("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in obj))
        else:
            json.dump(obj, f, ensure_ascii=False)


# --- filtro: sezione dove la testata la dà, parole chiave altrimenti
r = lambda t, c=(): {"titolo": t, "categorie": list(c)}
check("filtro: Abitare a Roma per sezione, anche senza parola chiave",
      filtro.keep("abitarearoma", r("Festa finita male al parco", ["cronaca"])))
check("filtro: Abitare a Roma fuori sezione escluso",
      not filtro.keep("abitarearoma", r("Arrestato spacciatore", ["politica"])))
check("filtro: bollettino traffico di Roma Daily News escluso",
      not filtro.keep("romadailynews", r("traffico roma del 01 06 2026 incidente sulla tangenziale")))
check("filtro: parola chiave trovata in un titolo con accenti",
      filtro.keep("ilfaroonline", r("Ostia, perché è stato arrestato il ladro")))
check("filtro: Dire solo con sezione Roma o Lazio",
      not filtro.keep("dire", r("Rapina in banca a Milano", ["cronaca", "milano"]))
      and filtro.keep("dire", r("Rapina a Centocelle", ["roma"])))

# --- prepara_lotti: fuori Roma esclusi, pettine a 8 lotti, finestre delle decadi
with tempfile.TemporaryDirectory() as d:
    schede = [{"id": f"CR-C1_{i:03d}-1", "fonte": "C1", "data_pubblicazione": f"2026-06-{1 + i % 30:02d}",
               "data_fatto": "", "fatto": "x", "luoghi_testo": "", "municipio": "V", "fuori_roma": i % 10 == 0,
               "esito": "F" if i % 10 == 0 else "U", "pagine": ["centocelle"]} for i in range(40)]
    scrivi(f"{d}/schede.jsonl", schede, jsonl=True)
    facts = prepara_lotti.fatti_ufficiali([f"{d}/schede.jsonl"])
    check("prepara_lotti: i fatti fuori Roma (F) non entrano", len(facts) == 36 and all(f["esito"] != "F" for f in facts))
    lots = prepara_lotti.lotti_avanti(facts)
    check("prepara_lotti: 8 lotti che coprono tutti i fatti una volta",
          len(lots) == 8 and sorted(f["id"] for l in lots for f in l) == sorted(f["id"] for f in facts))
    cand = [{"sid": "S0001", "data": "2026-06-05", "testata": "Dire", "titolo": "a", "link": "u"},
            {"sid": "S0002", "data": "2026-06-30", "testata": "Dire", "titolo": "b", "link": "v"}]
    inv = prepara_lotti.lotti_inversi(cand, facts)
    check("prepara_lotti: tre decadi, il 30 nella terza",
          len(inv) == 3 and [len(l["titoli"]) for l in inv] == [1, 0, 1])
    check("prepara_lotti: la prima decade vede i comunicati fino a 8 giorni dopo",
          max(f["pubblicato"] for f in inv[0]["fatti_ufficiali"]) == "2026-06-18")

# --- compila: le righe non cercate non contano; scenari sulle pagine
with tempfile.TemporaryDirectory() as d:
    lot = [{"id": i, "fonte": "Questura di Roma", "pubblicato": "2026-06-02", "fatto": "x", "esito": "U",
            "pagine": ["centocelle"]} for i in ("A", "B", "C")]
    scrivi(f"{d}/avanti/lotto_1.json", lot)
    t = lambda n, c: {"testata": n, "url": "u", "titolo": "t", "data": None, "prova_data": "sconosciuta", "corrispondenza": c}
    scrivi(f"{d}/avanti/risultati_1.jsonl", [
        {"id": "A", "ricerche": ["q"], "testate": [t("RomaToday", "certa"), t("Abitare a Roma", "probabile")], "nota": ""},
        {"id": "B", "ricerche": ["q"], "testate": [], "nota": ""},
        {"id": "C", "ricerche": [], "testate": [t("RomaToday", "probabile")], "nota": "copiato da un'altra ricerca"},
    ], jsonl=True)
    scrivi(f"{d}/censimento/candidati.json", [{"sid": s, "titolo": "Carabinieri a Ostia", "link": "l"} for s in ("S1", "S2", "S3")])
    scrivi(f"{d}/inverso/fatti_1.jsonl", [
        {"fid": "P1-001", "sid": ["S1"], "testate": ["Il Faro Online"], "data": "2026-06-03", "tipo": "arresto", "fatto": "x",
         "luogo": "Ostia", "pagina_qn": "ostia", "livello": "quartiere", "ufficiale": None, "corrispondenza": None},
        {"fid": "P1-002", "sid": ["S2"], "testate": ["Il Faro Online", "Roma Daily News"], "data": "2026-06-03",
         "tipo": "furto", "fatto": "y", "luogo": None, "pagina_qn": "acilia", "livello": "quartiere", "ufficiale": None,
         "corrispondenza": None},
    ], jsonl=True)
    scrivi(f"{d}/inverso/scarti_1.jsonl", [{"sid": "S3", "classe": "non_cronaca"}], jsonl=True)
    with open(f"{d}/matrice.csv", "w", encoding="utf-8-sig") as f:
        f.write("slug;Cronaca propri\ncentocelle;2\nostia;0\nacilia;0\nprati;0\n")
    R = compila.main(d, f"{d}/matrice.csv")
    a, i = R["avanti"], R["inversa"]
    check("compila: una riga senza ricerche propria non è un fatto cercato", a["fatti_cercati"] == 2)
    check("compila: distribuzione delle testate per fatto cercato",
          a["certa_o_probabile"]["distribuzione_n_testate"] == {"0": 1, "2": 1}
          and a["solo_certa"]["distribuzione_n_testate"] == {"0": 1, "1": 1})
    check("compila: fatti solo stampa e con almeno due testate",
          i["solo_stampa"] == 2 and i["solo_stampa_con_almeno_due_testate"] == 1 and i["solo_stampa_con_ente_nel_titolo"] == 2)
    sc = i["scenari"]
    check("compila: scenari sulle pagine (A 1, B 3, C 2)",
          sc["A_ufficiali_pubbliche"]["pagine_con_almeno_uno"] == 1
          and sc["B_piu_testate_aperte_dopo_conferma_massimo"]["pagine_con_almeno_uno"] == 3
          and sc["C_piu_fatti_su_due_testate_aperte"]["pagine_con_almeno_uno"] == 2)
    check("compila: il riepilogo non contiene link né titoli",
          "http" not in json.dumps(R) and "Carabinieri a Ostia" not in json.dumps(R))

print("ALL PASS" if not FALLITI else f"{len(FALLITI)} FAILED")
sys.exit(1 if FALLITI else 0)

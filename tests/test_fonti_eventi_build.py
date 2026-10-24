#!/usr/bin/env python3
"""Executable acceptance for tools/wiki/build_fonti_eventi.py (wiki of event sources).

Rules under test, each named in the check label:
- T-FE-1  DEC-022 / DEC-109: no event title from the workbook reaches the output
          (JSON or pages); only source names, channels and counts.
- T-FE-2  DEC-105: no automatic anonymisation — a curator, a promoter or a Facebook
          organiser under their own name is a subject like any other; a Facebook
          personal profile keeps the name and drops the profile URL.
- T-FE-3  identity: the same venue seen in Facebook, culture.roma.it, Roma Today and
          the registry is one entry, with the registry key as id and the spellings as aliases.
- T-FE-4  gazetteer wins: the zone is the gazetteer publication_zone_id by majority of
          the source's events; an unknown zone string is never written.
- T-FE-5  where to look: the page read at the source comes first, a website is kept as
          its root, a Facebook page becomes its /events view; non-http links are dropped.
- T-FE-6  determinism: two builds of the same input give identical bytes.
- T-FE-7  census of Facebook pages (24 October 2026): a candidate page enters as organiser
          with its verdict carried (never a registry decision); the same Facebook page as a
          registry entry is one source; the events page of its site is where to look; dormant
          pages are counted only; no page text enters the output.

Run:  python tests/test_fonti_eventi_build.py   (exit 0 and "ALL PASS" required)
"""
import json
import os
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "wiki"))
import build_fonti_eventi as bfe  # noqa: E402

checks = 0
failures = 0


def check(label, actual, expected):
    global checks, failures
    checks += 1
    if actual == expected:
        print(f"  ok   {label}")
    else:
        failures += 1
        print(f"  FAIL {label}\n       expected {expected!r}\n       got      {actual!r}")


TITLE_FB = "Serata Jazz Segretissima Al Vascello"
TITLE_CR = "Mostra Che Non Deve Entrare Nel Repo"
TITLE_RT = "Articolo Roma Today Titolo Riservato"
INTRO_TXT = "Testo Di Presentazione Della Pagina Che Non Entra"

GAZ = {"publication_zones": [{"publication_zone_id": "monteverde", "name_display": "Monteverde", "primary_municipality": "XII", "is_page": True},
                             {"publication_zone_id": "testaccio", "name_display": "Testaccio", "primary_municipality": "I", "is_page": True}],
       "neighbourhoods": []}


def sheet(wb, name, header, rows):
    ws = wb.create_sheet(name)
    ws.append(header)
    for r in rows:
        ws.append(r)


def make_inputs(folder):
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    uh = ["fonte", "nome", "inizio", "url", "lat", "lon", "municipio_assegnato", "zona_qn", "zona_qn_metodo2", "geo_nota", "rintracciabile_alla_fonte"]
    sheet(wb, "Eventi unificati", uh, [
        ["Facebook", TITLE_FB, "2026-10-20", "https://www.facebook.com/events/1/", 41.88, 12.46, "XII", "monteverde", None, None, "solo social"],
        ["Facebook", TITLE_FB + " 2", "2026-10-21", "https://www.facebook.com/events/2/", 41.88, 12.46, "XII", "monteverde", None, None, "sito dell'organizzatore o dell'evento"],
        ["Comune di Roma (culture.roma.it)", TITLE_CR, "2026-10-22", "https://culture.roma.it/appuntamento/x/", 41.88, 12.46, "XII", None, "monteverde", None, "sito dell'organizzatore o dell'evento"],
        ["Romatoday (scheda)", TITLE_RT, "2026-10-23", "https://www.romatoday.it/eventi/a.html", 41.88, 12.46, "XII", "zona-inventata", None, None, "nessun riferimento esterno"],
        ["Romatoday (scheda)", TITLE_RT + " 2", "2026-10-24", "https://www.romatoday.it/eventi/b.html", 41.87, 12.47, "I", "testaccio", None, None, "sito dell'organizzatore o dell'evento"],
        ["Fonte locale: Teatro Vascello", "Spettacolo Letto Alla Fonte", "2026-10-25", "https://www.teatrovascello.it/stagione/", None, None, "XII", "monteverde", None, None, "letto alla fonte (sito del luogo)"],
    ])
    fh = ["url", "name", "isOnline", "location.id", "location.name", "location.url", "location.latitude", "location.longitude", "location.streetAddress", "address", "location.city",
          "organizators.name", "organizators.url", "externalLinks", "ticketsInfo.buyUrl"]
    sheet(wb, "Facebook", fh, [
        ["https://www.facebook.com/events/1/", TITLE_FB, "False", "105634906151016", "Teatro Vascello", None, 41.88, 12.46, "Via Giacinto Carini 78", None, "Roma",
         "Teatro Vascello", "https://www.facebook.com/teatrovascello", "https://www.teatrovascello.it/spettacoli/serata-jazz; javascript:alert(1)", None],
        ["https://www.facebook.com/events/2/", TITLE_FB + " 2", "False", "105634906151016", "Teatro Vascello Roma", None, 41.88, 12.46, None, None, "Roma",
         "Jazz Promoter APS; Giulia Conti", "https://www.facebook.com/jazzpromoter/; https://www.facebook.com/profile.php?id=100099", "https://www.jazzpromoter.it/eventi/2", "https://www.vivaticket.com/x"],
    ])
    ch = ["url", "title", "venue", "venueUrl", "address", "municipio", "aCuraDi", "contattiLinks", "social", "ingressoLinks"]
    sheet(wb, "Comune di Roma (culture)", ch, [
        ["https://culture.roma.it/appuntamento/x/", TITLE_CR, "Teatro Vascello", "https://culture.roma.it/luogo/teatro-vascello/", "Via Giacinto Carini, 78", "Municipio XII",
         "Mario Rossi", "https://www.teatrovascello.it/stagione/2026", "https://www.facebook.com/teatrovascello | https://www.instagram.com/teatrovascello", None],
    ])
    rh = ["url_romatoday", "titolo_romatoday", "dove", "promotore_dichiarato", "sito_web", "link_ufficiale", "tipo_link", "link_facebook", "link_instagram", "link_biglietti"]
    sheet(wb, "Romatoday → sorgente", rh, [
        ["https://www.romatoday.it/eventi/a.html", TITLE_RT, "Teatro Vascello Via Giacinto Carini, 78", "Anna Bianchi", "teatrovascello.it", None, "nessun link", None, None, None],
        ["https://www.romatoday.it/eventi/b.html", TITLE_RT + " 2", "Mattatoio Piazza Orazio Giustiniani, 4", "OFFICINE CULTURALI SRL", None, "https://www.mattatoioroma.it/eventi/b", "pagina evento sul sito ufficiale", None, None, None],
    ])
    lh = ["fonte", "nome_fonte", "tipo_fonte", "zona_qn", "municipio", "evento", "pagina_letta", "anche_su_romatoday"]
    sheet(wb, "Fonti locali 13-31 ott", lh, [
        ["FE-0100", "Teatro Vascello", "teatro", "monteverde", "XII", "Spettacolo Letto Alla Fonte", "https://www.teatrovascello.it/stagione/", "sì"],
    ])
    dh = ["gruppo", "tipo", "fonti"]
    sheet(wb, "Doppioni", dh, [[1, "tra fonti", "Comune di Roma + Fonte locale"], [1, "tra fonti", "Comune di Roma + Fonte locale"]])
    wb.save(os.path.join(folder, "eventi_unico.xlsx"))
    rwb = openpyxl.Workbook()
    ws = rwb.active
    ws.append(["chiave", "decisione", "nome", "tipo", "zona_qn", "municipio", "sotto_soglia", "canale", "link", "facebook", "instagram", "origine"])
    ws.append(["FE-0100", "tenere", "Teatro Vascello", "teatro", "monteverde", "XII", "no", "sito", "https://www.teatrovascello.it", None, None, "romatoday"])
    ws.append(["FE-0200", "scartare", "Comitato Fittizio", "comitato", None, "XII", "sì", "facebook", "javascript:alert(1)", "https://www.facebook.com/comitatofittizio", None, "pagine_fb"])
    rwb.save(os.path.join(folder, "registro_fonti.xlsx"))
    json.dump({"https://culture.roma.it/luogo/teatro-vascello/": {"lat": 41.881, "lon": 12.461, "indirizzo": "Via Giacinto Carini, 78"}},
              open(os.path.join(folder, "culture_luoghi.json"), "w"))
    cwb = openpyxl.Workbook()
    ws = cwb.active
    ws.title = "Pagine"
    ws.append(["url_pagina", "nome", "stato", "verdetto", "motivo", "fb_eventi_in_roma", "sito_date_future", "sito_date_ultimi_6_mesi", "municipio", "zona_qn",
               "indirizzo", "lat", "lon", "categoria_facebook", "sito", "sito_pagina_eventi", "nel_registro_13_ott", "intro"])
    ws.append(["https://facebook.com/comitatofittizio", "Comitato Fittizio", "letta", "rientra: eventi futuri su Facebook", "2 eventi futuri a Roma", 2, 0, 0, "XII", "monteverde",
               "Via Fittizia 1, Rome", 41.88, 12.46, "Nonprofit organisation", None, None, "scartare", INTRO_TXT])
    ws.append(["https://facebook.com/circolotestaccio", "Circolo Arci Testaccio", "letta", "rientra: attiva, calendario sul sito", "il sito mostra date future", 0, 4, 2, "I", "testaccio",
               "Via Galvani 2, Rome", 41.87, 12.47, "Community organisation", "https://www.circolotestaccio.it", "https://www.circolotestaccio.it/eventi/", None, INTRO_TXT])
    ws.append(["https://facebook.com/dormiente", "Associazione Dormiente", "letta", "dormiente: nessun evento futuro su Facebook né calendario sul sito", "—", 0, 0, 0, "I", "testaccio",
               None, None, None, "Nonprofit organisation", None, None, None, INTRO_TXT])
    cwb.save(os.path.join(folder, "associazioni_fonti.xlsx"))
    gaz = os.path.join(folder, "gazetteer.json")
    json.dump(GAZ, open(gaz, "w"))
    return gaz


def read_all(out):
    texts = {}
    for root, _, files in os.walk(out):
        for f in files:
            texts[os.path.relpath(os.path.join(root, f), out)] = open(os.path.join(root, f), encoding="utf-8").read()
    return texts


def main():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "in"); os.makedirs(inp)
        gaz = make_inputs(inp)
        out1 = os.path.join(tmp, "out1"); out2 = os.path.join(tmp, "out2")
        s = bfe.build(inp, out1, gaz)
        bfe.build(inp, out2, gaz)
        texts = read_all(out1)
        blob = "\n".join(texts.values())

        print("T-FE-1 no source text")
        for t in (TITLE_FB, TITLE_CR, TITLE_RT, "Spettacolo Letto Alla Fonte"):
            check(f"T-FE-1 title absent: {t[:24]}", t in blob, False)

        print("T-FE-2 names of persons")
        names = {e["nome"] for e in s["fonti"]}
        check("T-FE-2 curator and promoter under their own name are subjects", {"Anna Bianchi", "Mario Rossi"} <= names, True)
        check("T-FE-2 organisation kept", "OFFICINE CULTURALI SRL" in names, True)
        gc = [e for e in s["fonti"] if e["nome"] == "Giulia Conti"][0]
        check("T-FE-2 facebook personal profile: name kept", gc["ruoli"], ["organizzatore"])
        check("T-FE-2 facebook personal profile: profile url not written", gc["canali"]["facebook"], [])
        check("T-FE-2 personal profiles counted", s["profili_personali_senza_url"], 1)

        print("T-FE-3 identity")
        v = [e for e in s["fonti"] if e["nome"] == "Teatro Vascello"]
        check("T-FE-3 one entry for the venue", len(v), 1)
        v = v[0]
        check("T-FE-3 registry key as id", v["id"], "S-FE-0100")
        check("T-FE-3 spelling seen kept as alias", "Teatro Vascello Roma" in v["alias"], True)
        check("T-FE-3 roles", v["ruoli"], ["luogo", "organizzatore"])
        check("T-FE-3 events per aggregator", v["eventi_ott_2026"], {"comune": 1, "facebook": 2, "fonte_locale": 1, "romatoday": 1})
        check("T-FE-3 facebook location id among keys", "fb-location:105634906151016" in v["chiavi"], True)
        check("T-FE-3 fonte locale read count and romatoday flag", v["fonte_locale"], {"codice": "FE-0100", "eventi_letti": 1, "anche_su_romatoday": 1})
        check("T-FE-3 registry decision carried", v["registro"]["decisione"], "tenere")
        check("T-FE-3 traceability quota", v["rintracciabilita"], {"eventi_con_fonte_diretta": 3, "quota": 0.6})

        print("T-FE-4 gazetteer wins")
        check("T-FE-4 zone by majority is a gazetteer id", v["zona"], "monteverde")
        check("T-FE-4 unknown zone string never written", any(e["zona"] == "zona-inventata" for e in s["fonti"]), False)
        check("T-FE-4 municipality official roman numeral", v["municipio"], "XII")
        check("T-FE-4 coordinates from the culture venue page", (v["lat"], v["lon"]) == (41.881, 12.461) or abs(v["lat"] - 41.88) < 0.01, True)

        print("T-FE-5 where to look")
        dove = v["dove_cercare"]
        check("T-FE-5 page read at the source first", dove[0], {"url": "https://www.teatrovascello.it/stagione/", "cosa": "pagina letta alla fonte (calendario)"})
        check("T-FE-5 culture venue page second", dove[1]["url"], "https://culture.roma.it/luogo/teatro-vascello/")
        check("T-FE-5 facebook page becomes its events view", any(d["url"] == "https://www.facebook.com/teatrovascello/events" for d in dove), True)
        check("T-FE-5 website kept as root, event page dropped", "https://www.teatrovascello.it/spettacoli/serata-jazz" in blob, False)
        check("T-FE-5 javascript link dropped everywhere", "javascript:" in blob, False)
        jp = [e for e in s["fonti"] if e["nome"] == "Jazz Promoter APS"][0]
        check("T-FE-5 organiser website root", jp["canali"]["sito"], ["https://jazzpromoter.it"])
        check("T-FE-5 ticket seller as domain only", v["canali"]["biglietteria"], ["vivaticket.com"])
        comitato = [e for e in s["fonti"] if e["nome"] == "Comitato Fittizio"][0]
        check("T-FE-5 registry entry without events kept (decision visible)", comitato["registro"]["decisione"], "scartare")

        print("T-FE-7 census of Facebook pages")
        com = [e for e in s["fonti"] if e["nome"] == "Comitato Fittizio"]
        check("T-FE-7 same facebook page as the registry entry is one source", len(com), 1)
        check("T-FE-7 registry id kept, verdict carried, decision untouched", (com[0]["id"], com[0]["censimento"]["verdetto"], com[0]["registro"]["decisione"]),
              ("S-FE-0200", "rientra: eventi futuri su Facebook", "scartare"))
        check("T-FE-7 facebook page key among keys", "fb-page:comitatofittizio" in com[0]["chiavi"], True)
        check("T-FE-7 census geography reaches the entry", (com[0]["municipio"], com[0]["zona"]), ("XII", "monteverde"))
        circ = next(e for e in s["fonti"] if e["nome"] == "Circolo Arci Testaccio")
        check("T-FE-7 new candidate is an organiser with the facebook type mapped", (circ["ruoli"], circ["tipo"], circ["id"].startswith("S-EV-")), (["organizzatore"], "associazione", True))
        check("T-FE-7 events page of the site is where to look first, then site root, then facebook events",
              [d["url"] for d in circ["dove_cercare"]], ["https://www.circolotestaccio.it/eventi/", "https://circolotestaccio.it", "https://www.facebook.com/circolotestaccio/events"])
        check("T-FE-7 dormant page counted, not listed", (any(e["nome"] == "Associazione Dormiente" for e in s["fonti"]), s["censimento_pagine"]["dormiente: nessun evento futuro su Facebook né calendario sul sito"]), (False, 1))
        check("T-FE-7 page text never written", INTRO_TXT in blob, False)
        check("T-FE-7 census page generated with the candidate", "Circolo Arci Testaccio" in texts.get("censimento-pagine.md", ""), True)

        print("T-FE-6 determinism and pages")
        check("T-FE-6 two builds identical", read_all(out1) == read_all(out2), True)
        check("T-FE-6 municipio page lists the venue with its id", "`S-FE-0100`" in texts["municipi/XII.md"], True)
        check("T-FE-6 per-page view has the zone heading", "## Monteverde `monteverde`" in texts["per-pagina-qn.md"], True)
        check("T-FE-6 aggregator card carries counts", "| eventi letti (ottobre 2026) | 2 |" in texts["aggregatori.md"], True)
        check("T-FE-6 overlap groups counted once", s["doppioni"], {"tra fonti · Comune di Roma + Fonte locale": 1})

    print(f"\n{checks} checks, {failures} failures")
    print("ALL PASS" if failures == 0 else "FAILED")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

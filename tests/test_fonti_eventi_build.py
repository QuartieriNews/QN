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
- T-FE-9  census of third-sector entities (RUNTS, 24 October 2026): read through a column map;
          an entity also in the Facebook census stays one source with the first verdict; an entity
          without a Facebook page enters by name with its tax code as identity key and its site's
          events page as where to look; an entity without web presence is counted only.
- T-FE-8  merge proposals: two entries that are probably the same source are listed for a
          person in fusioni-proposte.md and never merged by the build.
- T-FE-10 promoters of the events (analysis on Drive, 25 October 2026): promotori.md lists them by
          our category with a one-line label description; emails, phone numbers (in the contact fields
          and inside any text), long descriptions and the promoters' own texts never reach the output
          (a contact is only "sì/no"); a personal profile
          (Facebook profile.php, LinkedIn /in/) keeps the name and drops the URL; the zone is written only
          if it is a gazetteer id; a promoter with a schedario id carries its category on that entry.
- T-FE-11 where to look per promoter (channel test, 26 October 2026): channel, evidence and check channel
          are enums, anything else is dropped; the page is never a personal profile or a licensed
          aggregator; a site page proven to carry the promoter's events enters the entry's where-to-look
          list after the pages already read, so the site reader reads it; a Facebook link is cut to its
          page (a video, post or photo path carries the source's text) everywhere in the output.

Run:  python tests/test_fonti_eventi_build.py   (exit 0 and "ALL PASS" required)
"""
import json
import os
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools", "wiki"))
import build_fonti_eventi as bfe  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "tools", "fonti"))
import leggi_eventi_siti as ls  # noqa: E402

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
AUTO_TXT = "Autodescrizione Del Promotore Che Resta Su Drive"
PHONE = "06 5550 1234"

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
        ["https://www.facebook.com/events/3/", TITLE_FB + " 3", "False", "99", "Teatro Vascelo", None, 41.88, 12.46, None, None, "Roma",
         "Jazz Promoter Associazione Culturale", None, None, None],
        ["https://www.facebook.com/events/4/", TITLE_FB + " 4", "False", None, None, None, None, None, None, None, "Roma",
         "segreteria@organizzatore-fittizio.it", None, None, None],
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
    rwb2 = openpyxl.Workbook()
    ws = rwb2.active
    ws.title = "Enti"
    ws.append(["codice_fiscale", "denominazione", "verdetto", "motivo", "facebook", "fb_eventi_futuri_roma", "sito_date_future", "sito_date_6_mesi", "municipio", "zona_qn",
               "indirizzo", "lat", "lon", "facebook_categoria", "sito", "sito_pagina_eventi", "gia_nella_wiki"])
    ws.append(["97000000001", "Circolo Arci Testaccio", "rientra: annuncia eventi nei post Facebook", "3 post", "https://www.facebook.com/circolotestaccio", 0, 0, 0, "I", "testaccio",
               None, None, None, None, None, None, None])
    ws.append(["97000000002", "Associazione Ponte Fittizio APS", "rientra: calendario sul sito", "5 date future", None, None, 5, 2, "XII", "monteverde",
               "Via Fittizia 9, 00152 Roma", 41.88, 12.46, None, "https://www.pontefittizio.it", "https://www.pontefittizio.it/eventi/", None])
    ws.append(["97000000004", "Associazione Recapito Fittizio APS", "rientra: calendario sul sito", "3 date future", None, None, 3, 0, "I", "testaccio",
               "contatti@recapito-fittizio.it , Rome, Italy", None, None, None, "https://info@recapito-fittizio.it", None, None])
    ws.append(["97000000003", "Ente Senza Rete ETS", "nessuna presenza web trovata", "", None, None, None, None, None, None, None, None, None, None, None, None, None])
    rwb2.save(os.path.join(folder, "enti_terzo_settore_fonti.xlsx"))
    json.dump([
        {"nome": "Teatro Vascello", "id": "S-FE-0100", "categoria": "Teatri, cinema e spazi di spettacolo", "sottocategoria": "teatro", "ambito": "di quartiere",
         "descrizione_breve": "Teatro di Monteverde (Municipio XII): teatro, danza, incontri.", "attivita": ["teatro", "danza"], "pubblico": [],
         "municipio": "XII", "zona": "monteverde", "eventi": 5, "canali": {"sito": "https://www.teatrovascello.it", "facebook": "https://www.facebook.com/teatrovascello/videos/una-serata-dal-titolo-fittizio/1234567890/"},
         "contatti": {"email": ["biglietteria@teatro-fittizio.it"], "telefono": PHONE}, "email": ["biglietteria@teatro-fittizio.it"], "telefono": PHONE,
         "descrizione_lunga": AUTO_TXT, "autodescrizione": AUTO_TXT, "diffusione": "diritti riservati (generico)", "diffusione_prova": "https://www.teatrovascello.it/note-legali/",
         "dove_cercare": {"canale": "calendario del sito (schema.org)", "prova": "confermato", "pagina": "https://www.teatrovascello.it/calendario/", "controllo": "eventi Facebook"}},
        {"nome": "Giulia Conti", "id": None, "categoria": "Persone (artisti, autori, guide)", "sottocategoria": "persona", "ambito": "cittadino",
         "descrizione_breve": "Artista: scrivete a giulia@persona-fittizia.it o chiamate il " + PHONE + " " + "x" * 400,
         "attivita": ["musica, tel. +39 " + PHONE], "municipio": "XIII", "zona": "zona-inventata", "eventi": 1,
         "canali": {"facebook": "https://www.facebook.com/profile.php?id=100099", "linkedin": "https://www.linkedin.com/in/giulia-conti-fittizia", "sito": "mailto:giulia@persona-fittizia.it"}, "contatti": {"email": True},
         "diffusione": "una etichetta inventata",
         "dove_cercare": {"canale": "eventi Facebook", "prova": "storico", "pagina": "https://www.facebook.com/profile.php?id=100099", "controllo": "un canale inventato"}},
    ], open(os.path.join(folder, "promotori.json"), "w"))
    gaz = os.path.join(folder, "gazetteer.json")
    json.dump(GAZ, open(gaz, "w"))
    return gaz


def sig_tokens_jp(name):
    return bfe.sig_tokens(name) == {"jazz", "promoter"}


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
        check("T-FE-7 dormant page counted, not listed", (any(e["nome"] == "Associazione Dormiente" for e in s["fonti"]), s["censimento_pagine"]["pagine Facebook di associazioni"]["dormiente: nessun evento futuro su Facebook né calendario sul sito"]), (False, 1))
        check("T-FE-7 page text never written", INTRO_TXT in blob, False)
        check("T-FE-7 no email address in any generated file (contacts stay on Drive)", bool(bfe.EMAIL_RX.search(blob)), False)
        check("T-FE-7 census page generated with the candidate", "Circolo Arci Testaccio" in texts.get("censimento-pagine.md", ""), True)

        print("T-FE-9 census of third-sector entities")
        circ2 = [e for e in s["fonti"] if e["nome"] == "Circolo Arci Testaccio"]
        check("T-FE-9 entity in both censuses is one source, first verdict kept, second noted",
              (len(circ2), circ2[0]["censimento"]["verdetto"], circ2[0]["censimento"].get("anche_in")), (1, "rientra: attiva, calendario sul sito", ["enti del terzo settore (RUNTS)"]))
        pf = next(e for e in s["fonti"] if e["nome"] == "Associazione Ponte Fittizio APS")
        check("T-FE-9 entity without facebook enters with tax code key and RUNTS origin", ("cf:97000000002" in pf["chiavi"], pf["censimento"]["origine"], pf["zona"]), (True, "enti del terzo settore (RUNTS)", "monteverde"))
        check("T-FE-9 its site's events page is where to look first", [d["url"] for d in pf["dove_cercare"]][:2], ["https://www.pontefittizio.it/eventi/", "https://pontefittizio.it"])
        check("T-FE-9 entity without web presence counted only", (any(e["nome"] == "Ente Senza Rete ETS" for e in s["fonti"]), s["censimento_pagine"]["enti del terzo settore (RUNTS)"]["nessuna presenza web trovata"]), (False, 1))
        check("T-FE-9 census page has a section per census", ("## Censimento: enti del terzo settore (RUNTS)" in texts.get("censimento-pagine.md", ""), "## Censimento: pagine Facebook di associazioni" in texts.get("censimento-pagine.md", "")), (True, True))

        print("T-FE-8 merge proposals")
        fp = s["fusioni_proposte"]
        check("T-FE-8 typo spelling of the venue proposed, not merged",
              (any(c["a_nome"] == "Teatro Vascello" and c["b_nome"] == "Teatro Vascelo" for c in fp), sum(1 for e in s["fonti"] if e["nome"] in ("Teatro Vascello", "Teatro Vascelo"))), (True, 2))
        jp_all = [e for e in s["fonti"] if sig_tokens_jp(e["nome"])]
        check("T-FE-8 legal form and generic words: same source already one entry by normalisation, so no proposal", (len(jp_all), any("Jazz Promoter" in c["a_nome"] for c in fp)), (1, False))
        check("T-FE-8 page lists the pairs", "Teatro Vascelo" in texts.get("fusioni-proposte.md", ""), True)
        check("T-FE-8 unrelated entries not paired", any("Comitato Fittizio" in (c["a_nome"], c["b_nome"]) and "Circolo Arci Testaccio" in (c["a_nome"], c["b_nome"]) for c in fp), False)

        print("T-FE-10 promoters of the events")
        prom = texts.get("promotori.md", "")
        check("T-FE-10 promoters page generated, both listed", ("Teatro Vascello" in prom, "Giulia Conti" in prom), (True, True))
        check("T-FE-10 no email, phone, long description or own text anywhere",
              (bool(bfe.EMAIL_RX.search(blob)), PHONE in blob, AUTO_TXT in blob), (False, False, False))
        gp = next(p for p in s["promotori"] if p["nome"] == "Giulia Conti")
        check("T-FE-10 contact is yes/no only", (sorted(gp["contatti"].items()), "email" in gp and not isinstance(gp.get("email"), bool)), ([("email", True), ("telefono", False)], False))
        check("T-FE-10 personal profiles (Facebook, LinkedIn): name kept, url dropped; non-web link dropped", gp["canali"], {})
        check("T-FE-10 short description capped and stripped of the address", (len(gp["descrizione_breve"]) <= bfe.PROMO_MAX, "persona-fittizia" in gp["descrizione_breve"]), (True, False))
        check("T-FE-10 unknown zone and unknown label never written", (gp["zona"], gp["diffusione"]), (None, "non verificabile"))
        check("T-FE-10 phone numbers stripped from free text, postcode, year and date kept",
              bfe.PHONE_RX.sub("§", "tel. 06 5550 1234 o +39 333 123 4567, Via Roma 12, 00153 Roma, dal 2026, il 05/11/2026 ore 18.30"),
              "tel. § o §, Via Roma 12, 00153 Roma, dal 2026, il 05/11/2026 ore 18.30")
        vas = next(e for e in s["fonti"] if e["id"] == "S-FE-0100")
        check("T-FE-10 schedario entry carries the promoter category", vas.get("promotore", {}).get("categoria"), "Teatri, cinema e spazi di spettacolo")
        check("T-FE-10 evidence link of the position kept", "[diritti riservati (generico)](https://www.teatrovascello.it/note-legali/)" in prom, True)
        check("T-FE-10 index links the page", "[promotori.md](promotori.md)" in texts["INDEX.md"], True)

        print("T-FE-11 where to look per promoter")
        gv = next(p for p in s["promotori"] if p["nome"] == "Teatro Vascello")
        check("T-FE-11 rule kept: channel, evidence, page, check channel", gv["dove_cercare"],
              {"canale": "calendario del sito (schema.org)", "prova": "confermato", "pagina": "https://www.teatrovascello.it/calendario/", "controllo": "eventi Facebook"})
        check("T-FE-11 personal profile as page dropped, unknown check channel dropped", gp["dove_cercare"],
              {"canale": "eventi Facebook", "prova": "storico", "pagina": None, "controllo": None})
        check("T-FE-11 unknown channel: no rule", bfe.dove_cercare_promotore({"canale": "un canale inventato", "pagina": "https://esempio.it"}), None)
        check("T-FE-11 licensed aggregator never the page", bfe.dove_cercare_promotore({"canale": "pagina eventi del sito", "pagina": "https://www.romatoday.it/eventi/x.html"})["pagina"], None)
        dove = vas["dove_cercare"]
        check("T-FE-11 proven site page after the pages already read, before the other site addresses",
              [d["cosa"] for d in dove[:3]], ["pagina letta alla fonte (calendario)", "pagina del luogo su culture.roma.it", "pagina eventi del sito"])
        check("T-FE-11 the site reader reads the proven page", ls.page_to_check(vas), "https://www.teatrovascello.it/calendario/")
        check("T-FE-11 a Facebook video link becomes its page, the slug never reaches the output",
              (gv["canali"]["facebook"], "titolo-fittizio" in blob + prom), ("https://www.facebook.com/teatrovascello", False))
        check("T-FE-11 Facebook page forms: old name/id, people, groups kept; event, story dropped; post cut to the page",
              [bfe.fb_page_url(u) for u in ("https://www.facebook.com/Nome-Pagina/1234567890", "https://www.facebook.com/people/Nome/61500000000000",
                                            "https://www.facebook.com/groups/gruppo", "https://www.facebook.com/events/1234567890", "https://www.facebook.com/story.php",
                                            "https://www.facebook.com/pagina/posts/987654321")],
              ["https://www.facebook.com/Nome-Pagina/1234567890", "https://www.facebook.com/people/Nome/61500000000000", "https://www.facebook.com/groups/gruppo",
               None, None, "https://www.facebook.com/pagina"])
        check("T-FE-11 a Facebook post as page to read is cut to its page, the events view is kept, a story is dropped",
              [bfe.dove_cercare_promotore({"canale": "post Facebook", "pagina": u})["pagina"] for u in
               ("https://www.facebook.com/pagina/posts/987654321", "https://www.facebook.com/pagina/videos/un-titolo-fittizio-lungo/123456/events",
                "https://www.facebook.com/pagina/events", "https://www.facebook.com/story.php")],
              ["https://www.facebook.com/pagina", "https://www.facebook.com/pagina/events", "https://www.facebook.com/pagina/events", None])
        check("T-FE-11 schedario entry carries the rule", vas["promotore"]["dove_cercare"]["canale"], "calendario del sito (schema.org)")
        check("T-FE-11 promoters page: rule column with link, evidence and check channel",
              "[calendario del sito (schema.org)](https://www.teatrovascello.it/calendario/) · confermato · controllo: eventi Facebook" in prom, True)
        check("T-FE-11 promoters page: summary by channel", "| eventi Facebook | 1 | storico 1 |" in prom, True)

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

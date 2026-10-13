"""Controlli degli strumenti del registro delle fonti degli eventi (nessuna rete, dati sintetici).

Uso: python3 tools/fonti-eventi/test_fonti_eventi.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune_eventi, meetup_roma, registro, robots, romatoday_metadati, verifica_canali  # noqa: E402

FALLITI = []


def check(nome, cond):
    print(("ok   " if cond else "FAIL ") + nome)
    if not cond:
        FALLITI.append(nome)


# --- robots: gruppi sommati, jolly, regola più lunga, esclusione per nome degli agenti AI
MEETUP = """User-agent: *
Disallow: /files/

User-agent: *
Disallow: /*?location=*
Disallow: /*&dateRange=*
Allow: /*?_locale=

User-agent: GPTBot
Disallow: /
"""
g = robots.parse(MEETUP)
check("robots: i parametri vietati con il jolly bloccano la ricerca di Meetup",
      not robots.ammesso(g, "*", "https://www.meetup.com/find/?location=it--rm--Roma&dateRange=next-week"))
check("robots: la pagina di città senza parametri è ammessa",
      robots.ammesso(g, "*", "https://www.meetup.com/it-IT/find/it--roma/"))
check("robots: due gruppi «*» si sommano", not robots.ammesso(g, "*", "https://www.meetup.com/files/x"))
check("robots: un agente nominato segue solo il suo gruppo", not robots.ammesso(g, "GPTBot", "https://www.meetup.com/it-IT/find/it--roma/"))
check("robots: a parità di lunghezza vince Allow",
      robots.ammesso(robots.parse("User-agent: *\nDisallow: /a\nAllow: /a\n"), "*", "https://x.it/a"))
check("robots: «$» chiude il percorso",
      robots.ammesso(robots.parse("User-agent: *\nDisallow: /*.pdf$\n"), "*", "https://x.it/a.pdf?x=1")
      and not robots.ammesso(robots.parse("User-agent: *\nDisallow: /*.pdf$\n"), "*", "https://x.it/a.pdf"))
ROMATODAY = "User-agent: *\nUser-agent: Googlebot\nAllow: /\n\nUser-agent: ClaudeBot\nDisallow: /\n"
check("robots: chi esclude ClaudeBot è 'esclude_agenti_ai' anche se ammette tutti gli altri (§5.1)",
      robots.stato(robots.parse(ROMATODAY), "https://www.romatoday.it/eventi/") == "esclude_agenti_ai")
check("robots: senza regole è ammesso", robots.stato([], "https://x.it/agenda") == "ammesso")

# --- RomaToday: date dal link, mai dalla pagina
d = romatoday_metadati.date_da_slug
check("romatoday: due giorni dello stesso mese", d("pooh60-la-nostra-storia-al-palazzo-dello-sport-15-16-ottobre-2026") == ("2026-10-15", "2026-10-16"))
check("romatoday: intervallo a cavallo di due mesi", d("festa-autunno-ciciliano-31-ottobre-1-novembre-2026") == ("2026-10-31", "2026-11-01"))
check("romatoday: un giorno solo", d("ottobrata-romana-pigneto-10-ottobre-2026") == ("2026-10-10", "2026-10-10"))
check("romatoday: nessuna data nel link", d("desert-films-jovinelli") == (None, None))
check("romatoday: un numero di catalogo non è una data", d("vintage-market-forte-trionfale-15273533") == (None, None))

# --- Comune: data italiana e schede dell'elenco
check("comune: data italiana", comune_eventi.it_date("7 ottobre 2026") == "2026-10-07" and comune_eventi.it_date("x") == "")
CARD = ('<p class="List-category"><span>Tematica: <a href="/web/it/eventi.page?temat=teatro">Teatro</a></span>'
        '<span>Da: <a href="/web/it/eventi.page?struttura=str_lb">Sovrintendenza</a></span></p>'
        '<p class="List-date">13 ottobre 2026</p><p class="List-title"> <a href="/web/it/evento/x.page">Scena &amp; quartiere</a></p>'
        '<img src="a.jpg" alt="a" class="sinistra"/> <p>Nel Municipio VIII.</p></div>')
s = comune_eventi.schede_elenco(CARD)
check("comune: una scheda con data, titolo, tematica e struttura",
      len(s) == 1 and s[0]["pubblicato"] == "2026-10-13" and s[0]["titolo"] == "Scena & quartiere"
      and s[0]["tematiche"] == ["Teatro"] and s[0]["struttura"] == "Sovrintendenza"
      and s[0]["url"] == "https://www.comune.roma.it/web/it/evento/x.page")

# --- Meetup: stato Apollo, riferimenti risolti, partecipanti scartati, fuso di Roma
ND = {"props": {"pageProps": {"__APOLLO_STATE__": {
    "Event:1": {"__typename": "Event", "id": "1", "title": "Lettura", "dateTime": "2026-10-25T18:00:00+01:00",
                "venue": {"__ref": "Venue:9"}, "group": {"__ref": "Group:5"}, "rsvps": {"edges": [{"node": {"member": {"name": "X"}}}]}},
    "Venue:9": {"__typename": "Venue", "id": "9", "name": "Casa", "city": "Roma"},
    "Group:5": {"__typename": "Group", "id": "5", "name": "Club"},
    "Event:2": {"__typename": "Event", "id": "2", "dateTime": "2026-10-21T12:00:00-04:00"}}}}}
ev = {e["id"]: e for e in meetup_roma.eventi(ND)}
check("meetup: luogo e gruppo risolti dai riferimenti", ev["1"]["luogo"] == "Casa" and ev["1"]["gruppo"] == "Club")
check("meetup: nessun nome di partecipante in uscita", "X" not in str(ev))
check("meetup: tenuti solo gli eventi con fuso di Roma", meetup_roma.di_roma(ev["1"]) and not meetup_roma.di_roma(ev["2"]))

# --- verifica canali: formati dell'agenda
check("verifica: feed e API WordPress riconosciuti",
      verifica_canali.formato('<link type="application/rss+xml" href="/feed"><link rel="https://api.w.org/">') == ["feed", "wp_api"])
check("verifica: dati Event schema.org", verifica_canali.formato('{"@type": "TheaterEvent"}') == ["jsonld_event"])
check("verifica: solo HTML", verifica_canali.formato("<html></html>") == ["html"])

# --- registro: doppioni per Facebook, dominio e nome; decisione più forte; canale
RIS = {"fonti": [
    {"cid": "S001", "nome": "Teatro India", "tipo": "teatro", "zona_qn": "ostiense-san-paolo", "municipio": "VIII", "indirizzo": "",
     "sito": "https://www.teatrodiroma.net/", "agenda_url": "", "facebook": "", "instagram": "", "decisione": "da_verificare",
     "motivo": "", "certezza": "media"},
    {"cid": "C09", "nome": "Teatro India", "tipo": "teatro", "zona_qn": "ostiense-san-paolo", "municipio": "VIII", "indirizzo": "",
     "sito": "https://teatrodiroma.net", "agenda_url": "", "facebook": "https://www.facebook.com/teatrodiroma/", "instagram": "",
     "decisione": "tenere", "motivo": "programma", "certezza": "alta"}],
    "pagine": [{"riga": 3, "url": "https://facebook.com/TeatroDiRoma", "nome": "Teatro di Roma", "tipo": "istituzione_cultura",
                "zona_qn": "", "municipio": "", "post_nel_periodo": 2, "eventi_campione": 1, "decisione": "tenere", "motivo": "x"},
               {"riga": 4, "url": "https://www.facebook.com/100066949447787", "nome": "Profilo", "tipo": "profilo_personale_probabile",
                "zona_qn": "", "municipio": "", "post_nel_periodo": -1, "eventi_campione": -1, "decisione": "scartare", "motivo": "y"}]}
u = registro.unisci(RIS, {"S001": {"robots": "ammesso", "http": 200, "formato": ["html"]}}, {"ostiense-san-paolo"})
check("registro: stesso dominio e stessa pagina Facebook diventano una riga", len(u) == 2)
t = next(x for x in u if x["nome"] == "Teatro India")
check("registro: vince la decisione più forte (tenere)", t["decisione"] == "tenere")
check("registro: origini e chiavi conservate", t["origine"] == "romatoday+comune+pagine_fb" and t["chiavi_origine"] == ["S001", "C09", "P003"])
check("registro: gli eventi visti si sommano fra le righe unite", t["eventi_visti"] == 2)
check("registro: canale sito quando il robots.txt lo ammette", t["canale"] == "sito" and t["pagina_sotto_soglia"] == "sì")
check("registro: senza sito resta la pagina Facebook", registro.canale({"facebook": "https://facebook.com/x"}) == "facebook")
check("registro: sito che esclude gli agenti AI e nessun social", registro.canale({"robots": "esclude_agenti_ai"}) == "sito_chiuso")
check("registro: un 403 a un user agent dichiarato è un sito chiuso", registro.canale({"robots": "ammesso", "http": 403}) == "sito_chiuso")
check("registro: sito irraggiungibile e nessun social: canale da trovare", registro.canale({"robots": "errore", "sito": "https://x.it"}) == "da_trovare")
check("registro: chiavi FE ordinate con le fonti da tenere prima", u[0]["chiave"] == "FE-0001" and u[0]["decisione"] == "tenere")

print()
print("ALL PASS" if not FALLITI else f"{len(FALLITI)} FAIL: {FALLITI}")
sys.exit(1 if FALLITI else 0)

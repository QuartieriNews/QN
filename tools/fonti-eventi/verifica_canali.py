"""Verifica dei canali del registro delle fonti degli eventi: robots.txt e formato dell'agenda.

Uso: verifica_canali.py REGISTRO.json USCITA.json

Per ogni fonte con un sito: legge il robots.txt dell'host (una volta per host), decide se la
pagina dell'agenda (o la home) è ammessa a tutti, esclusa agli agenti AI o vietata (robots.py),
e solo se è ammessa la scarica una volta per riconoscere il formato leggibile: feed RSS/Atom,
calendario ICS, API WordPress, dati schema.org Event, o solo HTML. Facebook e Instagram non si
aprono mai (robots.txt: Disallow / a tutti). Una richiesta alla volta per host, user agent
dichiarato, nessun ritentativo con indirizzi o intestazioni diversi.
"""
import concurrent.futures as cf, json, re, sys, time, urllib.error, urllib.parse, urllib.request
import robots

UA = "QuartieriNews-ricerca/0.1 (registro fonti eventi; contatto nel sito del progetto)"
SOCIAL = re.compile(r"(^|\.)(facebook|instagram|fb)\.com$")


def formato(pagina):
    f = []
    if re.search(r'type="application/(rss|atom)\+xml"', pagina): f.append("feed")
    if re.search(r'href="[^"]+\.ics[^"]*"|webcal:', pagina): f.append("ics")
    if re.search(r'https://api\.w\.org/|/wp-json/', pagina): f.append("wp_api")
    if re.search(r'"@type"\s*:\s*"(Event|MusicEvent|TheaterEvent|ExhibitionEvent)"', pagina): f.append("jsonld_event")
    return f or ["html"]


def _get(url, limite=600_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, r.geturl(), r.read(limite).decode("utf-8", "replace")


def verifica_host(host, fonti):
    risultati = {}
    try:
        gruppi = robots.parse(_get(f"https://{host}/robots.txt", 300_000)[2])
    except urllib.error.HTTPError as e:  # 4xx: nessuna regola; 5xx: sito da considerare chiuso (RFC 9309 §2.3.1)
        gruppi = [] if 400 <= e.code < 500 else None
    except Exception:  # host irraggiungibile o certificato non valido: non si forza nulla
        gruppi = None
    for f in fonti:
        url = f.get("agenda_url") or f.get("sito")
        r = {"robots": "errore" if gruppi is None else robots.stato(gruppi, url)}
        if r["robots"] == "ammesso":
            time.sleep(1.0)
            try:
                st, finale, pagina = _get(url)
                r.update(http=st, url_finale=finale, formato=formato(pagina))
            except Exception as e:
                r.update(http=getattr(e, "code", None), errore=str(e)[:120])
        risultati[f["cid"]] = r
    return risultati


def verifica(registro, paralleli=8):
    per_host = {}
    for f in registro:
        url = f.get("agenda_url") or f.get("sito")
        if not url or not url.startswith("http"):
            continue
        host = urllib.parse.urlsplit(url).hostname or ""
        if SOCIAL.search(host):
            continue
        per_host.setdefault(host, []).append(f)
    out = {}
    with cf.ThreadPoolExecutor(paralleli) as ex:
        for r in ex.map(lambda kv: verifica_host(*kv), per_host.items()):
            out.update(r)
    return out


if __name__ == "__main__":
    reg = json.load(open(sys.argv[1]))
    ris = verifica(reg)
    json.dump(ris, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    print(len(ris), "fonti verificate su", len(reg))

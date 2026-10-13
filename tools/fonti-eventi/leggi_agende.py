"""Lettura delle agende delle fonti da tenere con canale «sito» (robots.txt già verificato).

Uso: leggi_agende.py DIR/registro.json DIR/agende

Per ogni fonte scarica una volta la pagina dell'agenda e salva il testo visibile e gli eventuali
blocchi JSON-LD di tipo Event, per la lettura degli eventi con un agente (passo 9 del README).
Se il registro dà solo la home, segue il primo link dello stesso sito che porta a un'agenda
(eventi, agenda, calendario, programma, cartellone, spettacoli, mostre…) ammesso dal robots.txt:
nella prova del 13 ottobre la home mostrava solo gli eventi in evidenza. Ricontrolla il robots.txt prima di leggere; otto host in parallelo, una richiesta per
host, user agent dichiarato. Scrive un file DIR/agende/<chiave>.json per fonte.
"""
import concurrent.futures as cf, html, json, os, re, sys, urllib.parse, urllib.request
import robots

UA = "QuartieriNews-ricerca/0.1 (registro fonti eventi; contatto nel sito del progetto)"
PAROLE_AGENDA = re.compile(r"(eventi|events|agenda|calendario|calendar|programma|programmazione|cartellone|stagione|"
                           r"spettacoli|mostre|concerti|appuntamenti|in-programma|whats-on|upcoming)", re.I)


def link_agenda(pagina, url, quanti=3):
    """Link dello stesso host, diversi dalla pagina stessa, che portano a un'agenda (percorso o testo del link)."""
    host = urllib.parse.urlsplit(url).hostname
    trovati = []
    for href, testo in re.findall(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', pagina, re.S):
        u = urllib.parse.urljoin(url, html.unescape(href))
        if urllib.parse.urlsplit(u).hostname != host or u.rstrip("/") == url.rstrip("/"):
            continue
        if PAROLE_AGENDA.search(urllib.parse.urlsplit(u).path) or PAROLE_AGENDA.search(re.sub(r"<[^>]+>", " ", testo)):
            trovati.append(u)
    return list(dict.fromkeys(trovati))[:quanti]


def testo_e_eventi(pagina):
    """Testo visibile della pagina e blocchi JSON-LD che contengono un Event."""
    ld = [x.strip()[:4000] for x in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', pagina, re.S)
          if "Event" in x]
    pagina = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", pagina, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", pagina))).strip(), ld


def _get(url, limite):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=25) as r:
        return r.read(limite).decode("utf-8", "replace")


def leggi(fonte, out):
    url = fonte.get("url_finale") or fonte.get("agenda_url") or fonte.get("sito")
    host = urllib.parse.urlsplit(url).hostname
    try:
        gruppi = robots.parse(_get(f"https://{host}/robots.txt", 300_000))
    except Exception:
        gruppi = []  # robots.txt già verificato da verifica_canali.py; un errore qui non cambia l'esito
    if robots.stato(gruppi, url) != "ammesso":
        return fonte["chiave"], "robots"
    try:
        pagina = _get(url, 1_500_000)
        if urllib.parse.urlsplit(url).path in ("", "/"):
            for u in link_agenda(pagina, url):
                if robots.stato(gruppi, u) == "ammesso":
                    url, pagina = u, _get(u, 1_500_000)
                    break
        t, ld = testo_e_eventi(pagina)
    except Exception as e:
        return fonte["chiave"], f"errore: {str(e)[:80]}"
    json.dump({"chiave": fonte["chiave"], "nome": fonte["nome"], "zona_qn": fonte["zona_qn"], "url": url,
               "jsonld": ld, "testo": t[:14000]}, open(f"{out}/{fonte['chiave']}.json", "w"), ensure_ascii=False)
    return fonte["chiave"], "ok"


if __name__ == "__main__":
    reg, out = json.load(open(sys.argv[1])), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    fonti = [f for f in reg if f["decisione"] == "tenere" and f["canale"] == "sito"]
    with cf.ThreadPoolExecutor(8) as ex:
        esiti = list(ex.map(lambda f: leggi(f, out), fonti))
    print(len(fonti), "fonti;", sum(1 for _, e in esiti if e == "ok"), "agende salvate")
    for k, e in esiti:
        if e != "ok":
            print(" ", k, e)

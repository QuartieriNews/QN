"""Lettura delle agende delle fonti da tenere con canale «sito» (robots.txt già verificato).

Uso: leggi_agende.py DIR/registro.json DIR/agende

Per ogni fonte scarica una volta la pagina dell'agenda (o la home) e salva il testo visibile e gli
eventuali blocchi JSON-LD di tipo Event, per la lettura degli eventi con un agente (passo 9 del
README). Ricontrolla il robots.txt prima di leggere; otto host in parallelo, una richiesta per
host, user agent dichiarato. Scrive un file DIR/agende/<chiave>.json per fonte.
"""
import concurrent.futures as cf, html, json, os, re, sys, urllib.parse, urllib.request
import robots

UA = "QuartieriNews-ricerca/0.1 (registro fonti eventi; contatto nel sito del progetto)"


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
        if robots.stato(robots.parse(_get(f"https://{host}/robots.txt", 300_000)), url) != "ammesso":
            return fonte["chiave"], "robots"
    except Exception:
        pass  # robots.txt già verificato da verifica_canali.py; un errore qui non cambia l'esito
    try:
        t, ld = testo_e_eventi(_get(url, 1_500_000))
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

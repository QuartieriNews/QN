"""Testo degli articoli delle testate aperte, per le notizie che il solo titolo non localizza.

Uso: testi_aperti.py DIR ELENCO.json   (ELENCO: [{"sid": [...]}...] o una lista di sid)

Solo testate che non escludono gli agenti AI e solo dai canali che il loro robots.txt ammette:
l'API pubblica di WordPress dove il sito non la esclude, altrimenti la pagina dell'articolo.
Una richiesta al secondo per sito, user agent dichiarato. Il testo resta nella cartella di
lavoro (DIR/testi/<sid>.txt): è dato della fonte e non entra nel repository (DEC-102, DEC-104).
"""
import html, json, os, re, sys, time, urllib.parse, urllib.request

UA = "QuartieriNews-ricerca/0.1 (misura copertura cronaca)"
WP = {"abitarearoma.it", "www.vignaclarablog.it", "www.dire.it"}  # API WordPress ammessa dal robots.txt
MAX_TESTI = int(os.environ.get("QN_MAX_TESTI", "300"))  # tetto alle richieste per esecuzione (AGENTS.md: costo)
ultimo = {}


def get(url):
    host = urllib.parse.urlsplit(url).hostname
    attesa = 1.0 - (time.time() - ultimo.get(host, 0))
    if attesa > 0:
        time.sleep(attesa)
    ultimo[host] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def pulisci(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>|<aside.*?</aside>", "", h, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<(br|/p|/div|/h\d|/li)[^>]*>", "\n", h, flags=re.I))
    return re.sub(r"\n\s*\n+", "\n", re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", t))).strip()


def testo(link):
    u = urllib.parse.urlsplit(link)
    if u.hostname in WP:
        slug = [p for p in u.path.split("/") if p][-1]
        if u.hostname == "www.vignaclarablog.it" or u.hostname == "www.dire.it":
            slug = re.sub(r"^\d+-", "", slug)
        js = json.loads(get(f"https://{u.hostname}/wp-json/wp/v2/posts?slug={urllib.parse.quote(slug)}&_fields=title,content,date"))
        if js:
            return pulisci(js[0]["title"]["rendered"] + "\n" + js[0]["content"]["rendered"])
    h = get(link if link.startswith("http") else f"https://{u.hostname}{u.path}")
    m = re.search(r"<article.*?</article>", h, re.S | re.I)
    return pulisci(m.group(0) if m else h)


def sids_da_scaricare(voci, cand):
    """I sid dell'elenco, una volta sola e in ordine, entro il tetto; un sid ignoto è un errore."""
    sids = list(dict.fromkeys(s for v in voci for s in (v["sid"] if isinstance(v, dict) else [v])))
    ignoti = [s for s in sids if s not in cand]
    if ignoti:
        raise SystemExit(f"sid non presenti fra i candidati: {ignoti[:10]}")
    if len(sids) > MAX_TESTI:
        raise SystemExit(f"{len(sids)} testi richiesti, tetto {MAX_TESTI} (QN_MAX_TESTI): dividere l'elenco")
    return sids


def main(base, elenco):
    cand = {c["sid"]: c for c in json.load(open(f"{base}/censimento/candidati.json", encoding="utf-8"))}
    voci = json.load(open(elenco, encoding="utf-8"))
    sids = sids_da_scaricare(voci, cand)
    os.makedirs(f"{base}/testi", exist_ok=True)
    esito, letti = {}, {}
    for s in sids:
        c = cand[s]
        link = c["link"] if c["link"].startswith("http") else {
            "Roma Daily News": "https://www.romadailynews.it", "Il Faro Online": "https://www.ilfaroonline.it"}.get(c["testata"], "") + c["link"]
        try:
            t = letti[link] if link in letti else testo(link)   # lo stesso articolo si scarica una volta
            letti[link] = t
            ok = len(t) > 400
            with open(f"{base}/testi/{s}.txt", "w", encoding="utf-8") as f:
                f.write(t)
            esito[s] = "ok" if ok else "corto"
        except Exception as e:
            esito[s] = f"errore: {str(e)[:120]}"
    with open(f"{base}/testi/esito.json", "w", encoding="utf-8") as f:
        json.dump(esito, f, ensure_ascii=False, indent=1)
    print({k: sum(1 for v in esito.values() if v.startswith(k)) for k in ("ok", "corto", "errore")})


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

"""Censimento dei titoli di un mese sulle testate che non escludono gli agenti AI.

Uso: censimento.py DIR [testata ...]   (scrive DIR/censimento/<testata>.json)

Legge solo i canali che il robots.txt della testata ammette: sitemap e, dove il sito non
la esclude, l'API pubblica di WordPress. Solo metadati: data, link, titolo (o lo slug
dell'URL), categorie. Nessun testo degli articoli. Ritmo di una richiesta al secondo,
user agent dichiarato. Metodo e limiti: docs/sources/CRONACA_PROCESSO_2026-10.md §4-5.
"""
import html, json, os, re, sys, time, urllib.request

UA = "QuartieriNews-ricerca/0.1 (misura copertura cronaca; solo metadati)"
MESE = os.environ.get("QN_MESE", "2026-06")
ANNO, M = MESE.split("-")


def get(url, tries=3):
    err = None
    for _ in range(tries):
        time.sleep(1.0)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace"), {k.lower(): v for k, v in r.headers.items()}
        except Exception as e:  # rete instabile: si riprova, poi si segnala
            err = e
            time.sleep(3)
    print("ERR", url, err, file=sys.stderr)
    return "", {}


def wordpress(site):
    """API pubblica di WordPress: solo per siti il cui robots.txt non esclude /wp-json/."""
    cats, page = {}, 1
    while page <= 30:
        b, _ = get(f"https://{site}/wp-json/wp/v2/categories?per_page=100&page={page}&_fields=id,slug")
        try:
            arr = json.loads(b)
        except ValueError:
            break
        if not isinstance(arr, list) or not arr:
            break
        cats.update({c["id"]: c["slug"] for c in arr})
        if len(arr) < 100:
            break
        page += 1
    nxt = f"{ANNO}-{int(M) + 1:02d}" if M != "12" else f"{int(ANNO) + 1}-01"
    out, page = [], 1
    while True:
        b, h = get(f"https://{site}/wp-json/wp/v2/posts?after={MESE}-01T00:00:00&before={nxt}-01T00:00:00"
                   f"&per_page=100&page={page}&_fields=id,date,link,title,categories")
        try:
            arr = json.loads(b)
        except ValueError:
            break
        if not isinstance(arr, list) or not arr:
            break
        out += [{"data": p["date"][:10], "link": p["link"], "titolo": html.unescape(p["title"]["rendered"]),
                 "categorie": [cats.get(c, str(c)) for c in p.get("categories", [])]} for p in arr]
        if page >= int(h.get("x-wp-totalpages") or 1):
            break
        page += 1
    return out


def sitemap(site):
    """Sitemap Yoast: tutte le post-sitemap, perché l'ordine per data non è garantito."""
    b, _ = get(f"https://{site}/sitemap_index.xml")
    urls = []
    for loc in re.findall(r"<loc>([^<]+)</loc>", b):
        if "post-sitemap" in loc:
            urls += re.findall(r"<loc>([^<]+)</loc>", get(loc)[0])
    out = []
    for u in sorted(set(urls)):
        m = re.search(rf"/({ANNO})/({M})/(\d\d)/([^/]+)", u)
        if m:
            slug = re.sub(r"-?\d{5,}$", "", m.group(4))
            out.append({"data": f"{ANNO}-{M}-{m.group(3)}", "link": u, "titolo": slug.replace("-", " "), "categorie": []})
    return out


def iltempo():
    """Sitemap giornaliere (Arc XP); la sezione è il primo segmento dell'URL."""
    out = []
    for d in range(1, 32):
        day = f"{MESE}-{d:02d}"
        urls = []
        for n in ("sitemap", "sitemap2", "sitemap3", "sitemap4"):
            urls = re.findall(r"<loc>([^<]+)</loc>", get(f"https://www.iltempo.it/arc/outboundfeeds/{n}/{day}/?outputType=xml")[0])
            if urls:
                break
        for u in urls:
            m = re.search(r"iltempo\.it/([^/]+)/(\d{4})/(\d\d)/(\d\d)/news/([^/]+)", u)
            if m and f"{m.group(2)}-{m.group(3)}" == MESE:
                out.append({"data": f"{m.group(2)}-{m.group(3)}-{m.group(4)}", "link": u,
                            "titolo": re.sub(r"-\d+$", "", m.group(5)).replace("-", " "), "categorie": [m.group(1)]})
    return out


TESTATE = {
    "abitarearoma": lambda: wordpress("abitarearoma.it"),
    "vignaclarablog": lambda: wordpress("www.vignaclarablog.it"),
    "dire": lambda: wordpress("www.dire.it"),
    "romadailynews": lambda: sitemap("www.romadailynews.it"),  # API esclusa dal robots.txt del CDN
    "ilfaroonline": lambda: sitemap("www.ilfaroonline.it"),    # idem
    "iltempo": iltempo,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out_dir = os.path.join(sys.argv[1], "censimento")
    os.makedirs(out_dir, exist_ok=True)
    for k in sys.argv[2:] or TESTATE:
        rows = TESTATE[k]()
        with open(f"{out_dir}/{k}.json", "w") as f:
            json.dump(rows, f, ensure_ascii=False, indent=0)
        print(k, len(rows), flush=True)

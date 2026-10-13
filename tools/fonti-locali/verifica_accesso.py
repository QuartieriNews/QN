"""Verifica dell'accesso e dell'attività di una fonte locale candidata.

Uso: verifica_accesso.py --out ESITO.json [--da 2026-07-01 --a 2026-10-01] URL...

Per ogni URL (un sito, non una pagina Facebook) legge, con user agent dichiarato e una
richiesta al secondo per host:
- robots.txt: se esclude gli agenti AI per nome, o tutti i robot; se consente a noi la
  home, il feed e l'API;
- la home: intestazioni e meta di riserva TDM (`tdm-reservation`, `Content-Signal`,
  `noai`), il feed dichiarato, la piattaforma (WordPress, Blogger, altro);
- l'attività nella finestra [--da, --a): dall'API WordPress quando il robots.txt la
  ammette (conteggio completo, M), altrimenti dalle date del feed (limite inferiore, S),
  altrimenti dalla sitemap (limite inferiore, S).

Non apre articoli, non scarica testi, non memorizza titoli: solo date e conteggi. Rispetta
il robots.txt anche per il feed e l'API (CRONACA_PROCESSO_2026-10.md §5.1). `QN_RETE=0`
spegne la rete (per i test).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET

UA = "QuartieriNews-ricerca/0.1 (censimento fonti locali; solo metadati)"
AGENTI_AI = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "anthropic-ai",
             "CCBot", "Google-Extended", "PerplexityBot", "Bytespider", "Amazonbot", "Applebot-Extended",
             "cohere-ai", "Meta-ExternalAgent", "FacebookBot", "Diffbot", "ai2bot", "YouBot", "Omgilibot"]
_ULTIMA = {}


def rete():
    return os.environ.get("QN_RETE", "1") != "0"


def fetch(url, timeout=20, max_bytes=400_000):
    """GET con ritmo per host. Ritorna (status, headers, testo) o (None, {}, errore)."""
    if not rete():
        return None, {}, "rete spenta"
    host = urllib.parse.urlsplit(url).netloc
    attesa = 1.0 - (time.monotonic() - _ULTIMA.get(host, 0))
    if attesa > 0:
        time.sleep(attesa)
    _ULTIMA[host] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            corpo = r.read(max_bytes)
            cs = r.headers.get_content_charset() or "utf-8"
            return r.status, dict(r.headers), corpo.decode(cs, "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), ""
    except Exception as e:  # rete, TLS, timeout
        return None, {}, f"{type(e).__name__}: {e}"


def leggi_robots(testo):
    """Gruppi user-agent -> regole; esclusioni per agente AI; `*` chiuso."""
    gruppi, correnti = {}, []
    for riga in testo.splitlines():
        riga = riga.split("#", 1)[0].strip()
        if not riga or ":" not in riga:
            continue
        chiave, valore = [p.strip() for p in riga.split(":", 1)]
        k = chiave.lower()
        if k == "user-agent":
            if correnti and any(gruppi[a] for a in correnti):
                correnti = []
            correnti.append(valore)
            gruppi.setdefault(valore, [])
        elif k in ("disallow", "allow") and correnti:
            for a in correnti:
                gruppi[a].append((k, valore))
    bassi = {a.lower(): r for a, r in gruppi.items()}

    def chiuso(agente):
        regole = bassi.get(agente.lower())
        return bool(regole) and any(k == "disallow" and v == "/" for k, v in regole)

    ai_esclusi = [a for a in AGENTI_AI if chiuso(a)]
    sitemaps = re.findall(r"(?im)^\s*sitemap\s*:\s*(\S+)", testo)
    return {"agenti_ai_esclusi": ai_esclusi, "tutti_esclusi": chiuso("*"), "sitemap": sitemaps,
            "esclude_noi": chiuso("QuartieriNews-ricerca")}


def permesso(robots_txt, base, percorso):
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots_txt.splitlines())
    return rp.can_fetch(UA.split("/")[0], urllib.parse.urljoin(base, percorso))


def _data(s):
    """Data ISO o RFC 2822 -> date, altrimenti None."""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s[:31] if "%z" in fmt and s.endswith("Z") is False else s.replace("Z", "+0000"), fmt).date()
        except ValueError:
            continue
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return dt.date.fromisoformat(m.group(1)) if m else None


def date_feed(xml):
    """Date degli item di un feed RSS/Atom (solo date, mai titoli)."""
    try:
        radice = ET.fromstring(xml.encode("utf-8", "replace") if isinstance(xml, str) else xml)
    except ET.ParseError:
        return []
    date = []
    for el in radice.iter():
        tag = el.tag.split("}")[-1].lower()
        if tag in ("pubdate", "published", "updated", "date") and el.text:
            d = _data(el.text)
            if d:
                date.append(d)
    return date


def date_sitemap(xml):
    date = []
    try:
        radice = ET.fromstring(xml.encode("utf-8", "replace"))
    except ET.ParseError:
        return date
    for el in radice.iter():
        if el.tag.split("}")[-1].lower() == "lastmod" and el.text:
            d = _data(el.text)
            if d:
                date.append(d)
    return date


def conta_finestra(date, da, a):
    return sum(1 for d in date if da <= d < a)


def analizza_home(html, intestazioni):
    bassa = {k.lower(): v for k, v in intestazioni.items()}
    esito = {"tdm_header": bassa.get("tdm-reservation"), "content_signal": bassa.get("content-signal"),
             "tdm_meta": None, "noai_meta": False, "feed": [], "wp_json": None, "piattaforma": "altro"}
    m = re.search(r'<meta[^>]+name=["\']tdm-reservation["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        esito["tdm_meta"] = m.group(1)
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noai', html, re.I):
        esito["noai_meta"] = True
    for m in re.finditer(r'<link[^>]+type=["\']application/(?:rss|atom)\+xml["\'][^>]*>', html, re.I):
        h = re.search(r'href=["\']([^"\']+)', m.group(0))
        if h:
            esito["feed"].append(h.group(1))
    m = re.search(r'<link[^>]+rel=["\']https://api\.w\.org/["\'][^>]+href=["\']([^"\']+)', html, re.I)
    if m or "/wp-content/" in html or "/wp-json/" in html:
        esito["piattaforma"] = "wordpress"
        esito["wp_json"] = m.group(1) if m else None
    elif "blogger.com" in html or "blogspot" in html:
        esito["piattaforma"] = "blogger"
    elif "wix.com" in html or "wixstatic" in html:
        esito["piattaforma"] = "wix"
    return esito


def verifica(url, da, a):
    parti = urllib.parse.urlsplit(url if "://" in url else "https://" + url)
    base = f"{parti.scheme}://{parti.netloc}/"
    esito = {"url": url, "host": parti.netloc, "errori": []}
    st, _, robots_txt = fetch(urllib.parse.urljoin(base, "/robots.txt"))
    esito["robots"] = {"stato": st}
    if st == 200:
        esito["robots"].update(leggi_robots(robots_txt))
    else:
        robots_txt = ""
        esito["robots"].update({"agenti_ai_esclusi": [], "tutti_esclusi": False, "sitemap": [], "esclude_noi": False})
    if st is None:
        esito["errori"].append(f"robots: {robots_txt}")
    st, hdr, html = fetch(url if "://" in url else "https://" + url)
    esito["home"] = {"stato": st}
    if st == 200:
        esito["home"].update(analizza_home(html, hdr))
    elif st is None:
        esito["errori"].append(f"home: {html}")
        esito["home"].update(analizza_home("", {}))
    else:
        esito["home"].update(analizza_home("", hdr))
    # i feed dichiarati possono essere relativi o senza schema (`//host/rss`)
    esito["home"]["feed"] = [urllib.parse.urljoin(base, f) for f in esito["home"]["feed"]]
    st, _, well = fetch(urllib.parse.urljoin(base, "/.well-known/tdmrep.json"))
    esito["tdmrep_wellknown"] = st == 200 and well.lstrip().startswith(("{", "["))

    attivita = {"metodo": None, "conteggio_finestra": None, "ultima_data": None, "date_viste": 0, "marca": "—"}
    if esito["robots"]["esclude_noi"] or esito["robots"]["tutti_esclusi"]:
        attivita["metodo"] = "non letta: robots.txt esclude"
    elif esito["home"]["piattaforma"] == "wordpress" and permesso(robots_txt, base, "/wp-json/"):
        api = (esito["home"]["wp_json"] or urllib.parse.urljoin(base, "/wp-json/")).rstrip("/")
        q = f"{api}/wp/v2/posts?after={da.isoformat()}T00:00:00&before={a.isoformat()}T00:00:00&per_page=1&_fields=date"
        st, hdr, corpo = fetch(q)
        tot = {k.lower(): v for k, v in hdr.items()}.get("x-wp-total")
        if st == 200 and tot is not None:
            attivita.update(metodo="API WordPress (X-WP-Total nella finestra)", conteggio_finestra=int(tot), marca="M")
            st2, _, ultimo = fetch(f"{api}/wp/v2/posts?per_page=1&_fields=date")
            try:
                attivita["ultima_data"] = json.loads(ultimo)[0]["date"][:10] if st2 == 200 else None
            except (ValueError, KeyError, IndexError, TypeError):
                pass
            attivita["date_viste"] = int(tot)
        else:
            esito["errori"].append(f"wp-json: stato {st}")
    if attivita["metodo"] is None or attivita["marca"] == "—":
        candidati = list(esito["home"]["feed"]) + [urllib.parse.urljoin(base, "/feed/"), urllib.parse.urljoin(base, "/feed"), urllib.parse.urljoin(base, "/rss.xml")]
        for f in candidati:
            if not permesso(robots_txt, base, urllib.parse.urlsplit(f).path):
                continue
            st, _, xml = fetch(f)
            if st == 200 and "<" in xml:
                date = date_feed(xml)
                if date:
                    attivita.update(metodo=f"feed {f} (solo gli ultimi item: limite inferiore)",
                                    conteggio_finestra=conta_finestra(date, da, a), ultima_data=max(date).isoformat(),
                                    date_viste=len(date), marca="S")
                    break
    if attivita["marca"] == "—" and not (esito["robots"]["esclude_noi"] or esito["robots"]["tutti_esclusi"]):
        for sm in esito["robots"]["sitemap"][:3] + [urllib.parse.urljoin(base, "/sitemap.xml")]:
            if not permesso(robots_txt, base, urllib.parse.urlsplit(sm).path):
                continue
            st, _, xml = fetch(sm)
            if st == 200 and "<" in xml:
                date = date_sitemap(xml)
                if date:
                    attivita.update(metodo=f"sitemap {sm} (lastmod: limite inferiore, include pagine non notizie)",
                                    conteggio_finestra=conta_finestra(date, da, a), ultima_data=max(date).isoformat(),
                                    date_viste=len(date), marca="S")
                    break
    esito["attivita"] = attivita
    esito["canale_lecito"] = giudizio(esito)
    return esito


def giudizio(e):
    """Che cosa può fare un agente AI con questa fonte, dal robots.txt e dai segnali TDM."""
    r, h = e["robots"], e["home"]
    if r["tutti_esclusi"] or r["esclude_noi"]:
        return "nessuno: robots.txt chiude il sito ai robot"
    if r["agenti_ai_esclusi"]:
        return "solo titolo, link e data da un motore di ricerca: robots.txt esclude gli agenti AI"
    if h.get("tdm_header") or h.get("tdm_meta") or e.get("tdmrep_wellknown") or h.get("noai_meta") or (h.get("content_signal") and "ai-train=no" in h["content_signal"]):
        return "solo metadati: riserva TDM o segnale noai dichiarato"
    if h["stato"] in (401, 403):
        return "nessuno: il sito rifiuta la richiesta"
    if h["stato"] != 200:
        return f"da verificare: home con stato {h['stato']}"
    return "aperto: lettura ammessa dal robots.txt, nessuna riserva TDM vista"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--da", default="2026-07-01")
    ap.add_argument("--a", default="2026-10-01")
    ap.add_argument("url", nargs="+")
    a = ap.parse_args(argv)
    da, fino = dt.date.fromisoformat(a.da), dt.date.fromisoformat(a.a)
    esiti = []
    for u in a.url:
        if "facebook.com" in u or "instagram.com" in u or "whatsapp.com" in u or "t.me/" in u:
            esiti.append({"url": u, "canale_lecito": "canale chiuso agli agenti: solo raccolta manuale (DEC-102)", "attivita": {"marca": "—"}})
            continue
        try:
            esiti.append(verifica(u, da, fino))
        except Exception as e:  # un URL malformato non deve fermare gli altri
            esiti.append({"url": u, "canale_lecito": f"da verificare: errore {type(e).__name__}: {e}", "attivita": {"marca": "—"}, "errori": [str(e)]})
        print(u, "->", esiti[-1]["canale_lecito"], "|", esiti[-1].get("attivita", {}).get("conteggio_finestra"), file=sys.stderr)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump({"finestra": [a.da, a.a], "fonti": esiti}, open(a.out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

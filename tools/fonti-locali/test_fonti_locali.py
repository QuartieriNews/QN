"""Test senza rete di verifica_accesso.py (QN_RETE=0): robots.txt, segnali TDM, date, giudizio."""
import datetime as dt
import os
import sys

os.environ["QN_RETE"] = "0"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verifica_accesso as va  # noqa: E402

CHECKS = []


def check(nome, cond):
    CHECKS.append((nome, bool(cond)))
    print(("PASS " if cond else "FAIL ") + nome)


ROBOTS_CHIUSO = """User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
User-agent: anthropic-ai
Disallow: /

User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Sitemap: https://esempio.it/sitemap_index.xml
"""
r = va.leggi_robots(ROBOTS_CHIUSO)
check("robots: tre agenti AI esclusi per nome", sorted(r["agenti_ai_esclusi"]) == ["ClaudeBot", "GPTBot", "anthropic-ai"])
check("robots: `*` non chiuso", r["tutti_esclusi"] is False)
check("robots: sitemap letta", r["sitemap"] == ["https://esempio.it/sitemap_index.xml"])
check("robots: noi non esclusi per nome", r["esclude_noi"] is False)
check("permesso: /feed/ ammesso a noi", va.permesso(ROBOTS_CHIUSO, "https://esempio.it/", "/feed/"))
check("permesso: /wp-admin/ negato", not va.permesso(ROBOTS_CHIUSO, "https://esempio.it/", "/wp-admin/x"))

r2 = va.leggi_robots("User-agent: *\nDisallow: /\n")
check("robots: tutti esclusi", r2["tutti_esclusi"] and r2["agenti_ai_esclusi"] == [])
r3 = va.leggi_robots("")
check("robots vuoto: niente esclusioni", r3 == {"agenti_ai_esclusi": [], "tutti_esclusi": False, "sitemap": [], "esclude_noi": False})

HOME = """<html><head><meta name="tdm-reservation" content="1">
<link rel="alternate" type="application/rss+xml" href="//esempio.it/feed/">
<link rel="https://api.w.org/" href="https://esempio.it/wp-json/"></head><body></body></html>"""
h = va.analizza_home(HOME, {"Content-Signal": "ai-train=no, search=yes"})
check("home: riserva TDM nel meta", h["tdm_meta"] == "1")
check("home: Content-Signal letto", h["content_signal"] == "ai-train=no, search=yes")
check("home: WordPress riconosciuto con wp-json", h["piattaforma"] == "wordpress" and h["wp_json"] == "https://esempio.it/wp-json/")
check("home: feed dichiarato raccolto", h["feed"] == ["//esempio.it/feed/"])

FEED = """<?xml version="1.0"?><rss><channel><title>x</title>
<item><title>a</title><pubDate>Tue, 15 Sep 2026 10:00:00 +0200</pubDate></item>
<item><title>b</title><pubDate>Mon, 29 Jun 2026 10:00:00 +0200</pubDate></item>
<item><title>c</title><pubDate>Wed, 01 Jul 2026 00:30:00 +0200</pubDate></item>
</channel></rss>"""
date = va.date_feed(FEED)
check("feed: tre date lette", len(date) == 3)
check("feed: due nella finestra luglio-settembre (bordi inclusi/esclusi)", va.conta_finestra(date, dt.date(2026, 7, 1), dt.date(2026, 10, 1)) == 2)
SITEMAP = """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://e.it/a</loc><lastmod>2026-08-02T10:00:00+00:00</lastmod></url>
<url><loc>https://e.it/b</loc><lastmod>2025-08-02</lastmod></url></urlset>"""
ds = va.date_sitemap(SITEMAP)
check("sitemap: lastmod ISO con e senza ora", ds == [dt.date(2026, 8, 2), dt.date(2025, 8, 2)])
check("feed malformato: nessuna data, nessuna eccezione", va.date_feed("<rss><item><pubDate>x</pubDate>") == [])

base = {"robots": {"tutti_esclusi": False, "esclude_noi": False, "agenti_ai_esclusi": []}, "home": {"stato": 200}, "tdmrep_wellknown": False}
check("giudizio: aperto", va.giudizio(base).startswith("aperto"))
check("giudizio: agenti AI esclusi -> solo titolo e link", "solo titolo" in va.giudizio({**base, "robots": {**base["robots"], "agenti_ai_esclusi": ["GPTBot"]}}))
check("giudizio: TDM nel meta -> solo metadati", "solo metadati" in va.giudizio({**base, "home": {"stato": 200, "tdm_meta": "1"}}))
check("giudizio: Content-Signal ai-train=no -> solo metadati", "solo metadati" in va.giudizio({**base, "home": {"stato": 200, "content_signal": "ai-train=no"}}))
check("giudizio: 403 -> nessuno", va.giudizio({**base, "home": {"stato": 403}}).startswith("nessuno"))
check("giudizio: `*` chiuso -> nessuno", va.giudizio({**base, "robots": {**base["robots"], "tutti_esclusi": True}}).startswith("nessuno"))

e = va.verifica("https://esempio.it", dt.date(2026, 7, 1), dt.date(2026, 10, 1))
check("rete spenta: nessuna lettura, esito completo", e["robots"]["stato"] is None and e["attivita"]["marca"] == "—" and e["canale_lecito"].startswith("da verificare"))

# API WordPress dichiarata senza schema (`//host/wp-json/`): va risolta sulla base, non passata com'è
_fetch = va.fetch
va.fetch = lambda url, **k: (200, {}, '<link rel="https://api.w.org/" href="//esempio.it/wp-json/">') if url.rstrip("/") == "https://esempio.it" else (404, {}, "")
e2 = va.verifica("https://esempio.it/", dt.date(2026, 7, 1), dt.date(2026, 10, 1))
va.fetch = _fetch
check("wp-json senza schema risolto sulla base", e2["home"]["wp_json"] == "https://esempio.it/wp-json/")

import tabella  # noqa: E402

VOCI = [
    {"slug": "p1", "tipo": "pagina", "pagina": "P1", "municipio": "X", "ricerche": 4, "fonti": [
        {"nome": "CdQ A", "url": "https://a.it/", "tipo": "comitato_di_quartiere", "canale": "sito", "blocchi": ["cronaca"], "territorio": "quartiere", "territorio_note": "A", "verdetto": "usabile", "motivo": "ok", "canale_lecito": "aperto", "conteggio_finestra": 7, "marca": "M", "ultima_data": "2026-09-30", "piattaforma": "wordpress", "feed_o_api": True, "quota_locale_stimata": "tutte"},
        {"nome": "Blog Z", "url": "https://www.z.it", "tipo": "blog_locale", "canale": "sito", "blocchi": ["cronaca"], "territorio": "zona", "territorio_note": "litorale", "verdetto": "solo_metadati", "motivo": "robots", "canale_lecito": "solo titolo", "conteggio_finestra": None, "marca": "—", "ultima_data": None, "piattaforma": "altro", "feed_o_api": False, "quota_locale_stimata": "?"}]},
    {"slug": "p2", "tipo": "pagina", "pagina": "P2", "municipio": "X", "ricerche": 5, "fonti": [
        {"nome": "Blog Z", "url": "https://z.it/", "tipo": "blog_locale", "canale": "sito", "blocchi": ["cronaca"], "territorio": "zona", "territorio_note": "litorale", "verdetto": "usabile", "motivo": "ok", "canale_lecito": "aperto", "conteggio_finestra": 3, "marca": "S", "ultima_data": "2026-08-01", "piattaforma": "altro", "feed_o_api": True, "quota_locale_stimata": "1 su 4"}]},
    {"slug": "p3", "tipo": "pagina", "pagina": "P3", "municipio": "IX", "fallito": True},
    {"slug": "municipio-x", "tipo": "municipio", "pagina": "Municipio X", "municipio": "X", "ricerche": 3, "fonti": []},
]
rp = tabella.riepilogo(VOCI)
check("tabella: pagine e Municipi contati a parte", rp["pagine"] == 3 and rp["voci"] == 4)
check("tabella: pagine con almeno una fonte usabile", rp["pagine_con_usabile"] == 2)
check("tabella: la stessa fonte con www e senza è una", rp["fonti_distinte"] == 2 and rp["fonti_trasversali"] == 1)
check("tabella: conteggio per verdetto", rp["per_verdetto"] == {"usabile": 2, "solo_metadati": 1})
check("tabella: agente fallito segnalato", any(p["fallito"] for p in rp["per_pagina"] if p["slug"] == "p3"))
md = tabella.md_pagine(VOCI, rp, "pagina")
check("tabella md: una riga per pagina, fallito marcato", md.count("\n| ") == 3 and "*agente fallito*" in md)
mdf = tabella.md_fonti(VOCI)
check("tabella md fonti: fonte trasversale elencata una volta con due pagine", mdf.count("Blog Z") == 1 and "p1, p2" in mdf)

falliti = [n for n, ok in CHECKS if not ok]
print(f"{len(CHECKS) - len(falliti)}/{len(CHECKS)} checks; " + ("ALL PASS" if not falliti else "FAILED: " + ", ".join(falliti)))
sys.exit(1 if falliti else 0)

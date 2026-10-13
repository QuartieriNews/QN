"""Agenda eventi del portale di Roma Capitale (E3 del registro fonti): elenco e schede.

Uso: comune_eventi.py DIR AAAA-MM-GG

Legge l'elenco https://www.comune.roma.it/web/it/eventi.page (10 schede per pagina, ordinate per
data di pubblicazione) finché la data scende sotto la soglia, poi ogni scheda: Municipio
(meta search:municipio), luogo e coordinate dal marcatore della mappa, inizio del testo (dove
stanno le date). Il calendario «var events» della pagina contiene solo gli eventi in evidenza,
uguali su tutte le pagine: non si usa. Una richiesta ogni 1,5 s, user agent dichiarato.
Scrive DIR/comune_schede.json.
"""
import html, json, re, sys, time, urllib.request

UA = "QuartieriNews-ricerca/0.1 (progetto editoriale; contatto nel sito del progetto)"
BASE = "https://www.comune.roma.it"
MESI = {m: i for i, m in enumerate(["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
                                    "agosto", "settembre", "ottobre", "novembre", "dicembre"], 1)}


def it_date(s):
    m = re.match(r"(\d{1,2})\s+(\w+)\s+(\d{4})", s.strip())
    return f"{m.group(3)}-{MESI[m.group(2).lower()]:02d}-{int(m.group(1)):02d}" if m and m.group(2).lower() in MESI else ""


def schede_elenco(pagina_html):
    """Schede di una pagina dell'elenco: pubblicazione, url, titolo, tematiche, struttura, sommario."""
    out = []
    for b in pagina_html.split('<p class="List-category">')[1:]:
        d = re.search(r'<p class="List-date">([^<]+)</p>', b)
        a = re.search(r'<p class="List-title">\s*<a href="([^"]+)">(.*?)</a>', b, re.S)
        if not (d and a):
            continue
        testa = b.split("</p>")[0]
        da = re.findall(r'struttura=[^"]*">([^<]+)</a>', testa)
        summ = re.search(r'class="sinistra"/>\s*<p>(.*?)</p>', b, re.S)
        out.append({"pubblicato": it_date(d.group(1)), "url": BASE + html.unescape(a.group(1)),
                    "titolo": html.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip(),
                    "tematiche": [html.unescape(x).strip() for x in re.findall(r'temat=[^"]*">([^<]+)</a>', testa)],
                    "struttura": html.unescape(da[0]).strip() if da else "",
                    "sommario": html.unescape(re.sub(r"<[^>]+>", "", summ.group(1))).strip() if summ else ""})
    return out


def dettagli(scheda_html):
    meta = dict(re.findall(r'<meta[^>]+name="(search:[^"]+)"[^>]+content="([^"]*)"', scheda_html))
    mk = re.search(r"text: '([^']*)', descr: '[^']*', latLng: \[([\d.]+), ([\d.]+)\]", scheda_html)
    corpo = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", scheda_html)))
    i = corpo.find("Tematica:")
    return {"municipio": html.unescape(meta.get("search:municipio", "")),
            "indirizzo": html.unescape(mk.group(1)).strip(" |") if mk else "",
            "lat": float(mk.group(2)) if mk else None, "lon": float(mk.group(3)) if mk else None,
            "testo": corpo[i:i + 900] if i >= 0 else ""}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")


if __name__ == "__main__":
    out, soglia = sys.argv[1], sys.argv[2]
    schede, p = [], 1
    while p <= 40:
        pag = schede_elenco(get(BASE + "/web/it/eventi.page" + ("" if p == 1 else f"?pagina={p}")))
        schede += pag
        if not pag or pag[-1]["pubblicato"] < soglia:
            break
        p += 1
        time.sleep(1.5)
    schede = [s for s in schede if s["pubblicato"] >= soglia]
    for s in schede:
        s.update(dettagli(get(s["url"])))
        time.sleep(1.5)
    json.dump(schede, open(out + "/comune_schede.json", "w"), ensure_ascii=False, indent=1)
    print(len(schede), "schede pubblicate dal", soglia)

"""Raccoglitore dei comunicati ufficiali di un mese (C1–C6 del registro fonti).

Uso: fonti_ufficiali.py DIR [AAAA-MM] [fonte ...]   (di default 2026-06, tutte le fonti)

Per ogni fonte legge le pagine di elenco del mese, poi scarica ogni comunicato e controlla che
la risposta sia davvero il comunicato: non una pagina di blocco («Accesso negato» servito con
codice 200, come successo a settembre), non una vetrina generica, non un testo troppo corto.
Ritmo per ente, user agent dichiarato, ritentativi con attesa crescente; dopo cinque rifiuti di
fila sullo stesso ente si ferma e lo scrive, senza cambiare indirizzo né intestazioni
(SOURCE_REGISTRY.md, sezioni C1–C6, per gli elenchi; CRONACA_PROCESSO_2026-10.md §5.1).

Scrive DIR/ufficiali/inventario.json (un elemento per comunicato: fonte, url, data, titolo,
stato), DIR/ufficiali/raw/<id>.txt (testo) e DIR/ufficiali/rapporto.json (per fonte: pagine
di elenco lette, comunicati del mese, scaricati, rifiutati, errori, durata). Una passata su alcune
fonti sostituisce le loro voci; se l'elenco di una fonte non si legge, le voci del giro precedente
restano e il rapporto lo dice (voci_del_giro_precedente).
"""
import datetime as dt, html, json, os, re, sys, time, urllib.parse, urllib.request

UA = "QuartieriNews-ricerca/0.1 (raccolta comunicati ufficiali; contatto nel sito del progetto)"
RITMO = {"questure.poliziadistato.it": 4.0}  # secondi fra due richieste allo stesso host
RITMO_BASE = 2.0
BLOCCO = re.compile(r"accesso negato|access denied|forbidden|captcha|cf-chl|attention required|"
                    r"sistema .{0,20}temporaneamente non disponibile", re.I)  # anche il «temporaneamente non disponibile» dei Carabinieri (settembre)
MESI = {m: i for i, m in enumerate(["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
                                    "agosto", "settembre", "ottobre", "novembre", "dicembre"], 1)}


class Rifiuto(Exception):
    pass


class Cliente:
    def __init__(self):
        self.ultimo, self.rifiuti, self.fermi = {}, {}, set()

    def get(self, url, tries=3):
        host = urllib.parse.urlsplit(url).hostname
        if host in self.fermi:
            raise Rifiuto(f"{host} fermato dopo cinque rifiuti")
        err = None
        for i in range(tries):
            attesa = RITMO.get(host, RITMO_BASE) - (time.time() - self.ultimo.get(host, 0))
            if attesa > 0:
                time.sleep(attesa)
            self.ultimo[host] = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read().decode("utf-8", "replace")
                if BLOCCO.search(body[:20000]) and not re.search(r"<article|class=\"testo|tabellaD|elenco_notizie", body):
                    raise Rifiuto("pagina di blocco")
                self.rifiuti[host] = 0
                return body
            except Rifiuto as e:
                err = e
                self.rifiuti[host] = self.rifiuti.get(host, 0) + 1
                if self.rifiuti[host] >= 5:
                    self.fermi.add(host)
                    raise
                time.sleep(30 * (i + 1))
            except Exception as e:  # rete o server: si riprova con attesa crescente
                err = e
                time.sleep(5 * (i + 1))
        raise err


def testo(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>", "", h, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<(br|/p|/div|/h\d|/li)[^>]*>", "\n", h, flags=re.I))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\n\s*\n+", "\n", re.sub(r"[ \t]+", " ", t)).strip()


def pulito(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def nel_mese(d, mese):
    return d is not None and d.strftime("%Y-%m") == mese


# --- elenchi per fonte: ciascuno restituisce (voci del mese, pagine lette) -------------------------

def elenco_questura(c, mese):
    base = "https://questure.poliziadistato.it/it/Roma/archivio/category/5730dc9d86cad683338531"
    voci, p = [], 1
    while p < 200:
        h = c.get(f"{base}/{p}/")
        blocchi = re.findall(r'<h3><a href="(/it/Roma/articolo/[^"]+)">(.*?)</a></h3>.*?<em>(\d\d-\d\d-\d{4})</em>', h, re.S)
        if not blocchi:
            break
        date = [dt.datetime.strptime(d, "%d-%m-%Y") for _, _, d in blocchi]
        voci += [{"url": "https://questure.poliziadistato.it" + u, "titolo": pulito(ti), "data": d.date().isoformat()}
                 for (u, ti, _), d in zip(blocchi, date) if nel_mese(d, mese)]
        if max(date).strftime("%Y-%m") < mese:
            break
        p += 1
    return voci, p


def elenco_carabinieri(c, mese):
    d = mese.replace("-", "")
    base = "https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa"
    voci, nazionali, p = [], 0, 1
    while p < 40:
        h = c.get(f"{base}?d={d}" if p == 1 else f"{base}/!page/page/{p}?d={d}")
        righe = re.findall(r"<td class=tabella[DP]>(\d\d/\d\d/\d{4} \d\d:\d\d)<td class=tabella[DP]><a [^>]*href=([^\s>]+)>"
                           r"(?:<span[^>]*>([^<]*)</span>)?([^<]*)</a><td class=tabella[DP]><span[^>]*>([^<]*)</span>([^<]*)", h)
        if not righe:
            break
        for data, url, luogo, titolo, _, comando in righe:
            nazionali += 1
            luogo, comando = pulito(luogo), pulito(comando)
            if "(RM)" in luogo or re.search(r"\bRoma\b", comando):
                voci.append({"url": url.strip('"\''), "titolo": pulito(titolo), "luogo": luogo.rstrip(" -"), "comando": comando,
                             "data": dt.datetime.strptime(data, "%d/%m/%Y %H:%M").date().isoformat()})
        if f"!page/page/{p + 1}?" not in h:
            break
        p += 1
    return voci, {"pagine": p, "comunicati_nazionali": nazionali}


def elenco_procura(c, mese):
    voci, p, precedenti = [], 1, None
    while p <= 10:
        url = f"https://procura-roma.giustizia.it/it/news_e_comunicati.page?frame5_item={p}"
        h = c.get(url)
        righe = re.findall(r'<div class="col-sm-2"><b><b>(\d\d/\d\d/\d{4})\s*</b></b></div>\s*'
                           r'<div class="col-sm-3">(.*?)</div>\s*<div class="col-sm-7">(.*?)</div>', h, re.S)
        if not righe or righe == precedenti:
            break
        precedenti = righe
        date = []
        for d, tipo, titolo in righe:
            data = dt.datetime.strptime(d, "%d/%m/%Y").date()
            date.append(data)
            if data.strftime("%Y-%m") == mese:
                link = re.search(r'href="([^"]+)"', titolo)
                voci.append({"url": urllib.parse.urljoin(url, link.group(1)) if link else url,
                             "titolo": pulito(titolo), "tipologia": pulito(tipo), "data": data.isoformat()})
        if max(date).strftime("%Y-%m") < mese:
            break
        p += 1
    return voci, p


def elenco_vvf(c, mese):
    a = dt.date.fromisoformat(mese + "-01")
    b = (a.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    url = ("https://www.vigilfuoco.it/comando-vvf-roma/notizie-dal-territorio?provincia=244"
           f"&data%5Bmin%5D={a}&data%5Bmax%5D={b}")
    h = c.get(url)
    mesi = "|".join(MESI)
    voci = []
    for blocco in h.split("<article")[1:]:
        u = re.search(r'href="(?:https?://www\.vigilfuoco\.it)?((?:/media/notizie|/comando-vvf-roma/notizie)/[^"]+)"', blocco)
        d = re.search(rf"(\d{{1,2}}) ({mesi}) (\d{{4}})", blocco, re.I)
        t = re.search(r"<h2[^>]*>(.*?)</h2>", blocco, re.S)
        if not (u and d):
            continue
        data = dt.date(int(d.group(3)), MESI[d.group(2).lower()], int(d.group(1)))
        if data.strftime("%Y-%m") == mese and not any(v["url"].endswith(u.group(1)) for v in voci):
            voci.append({"url": "https://www.vigilfuoco.it" + u.group(1), "titolo": pulito(t.group(1)) if t else "",
                         "data": data.isoformat()})
    return voci, 1


def elenco_polizia_locale(c, mese):
    mesi = "|".join(MESI)
    voci, p, precedenti = [], 1, None
    while p < 40:
        h = c.get(f"https://www.comune.roma.it/web/it/notizie.page?struttura=str_sg&pagina={p}")
        # l'elenco della struttura (List-date / List-title); le schede «Card» in alto sono le notizie in
        # evidenza di tutto il portale, non della Polizia Locale
        schede = re.findall(rf'<p class="List-date">(\d{{1,2}}) ({mesi}) (\d{{4}})</p>\s*<p class="List-title">\s*'
                            r'<a href="(/web/it/notizia/[^"]+)">(.*?)</a>', h, re.S | re.I)
        if not schede or schede == precedenti:
            break
        precedenti = schede
        date = []
        for g, m, y, u, t in schede:
            d = dt.date(int(y), MESI[m.lower()], int(g))
            date.append(d)
            if d.strftime("%Y-%m") == mese and not any(v["url"].endswith(u) for v in voci):
                voci.append({"url": "https://www.comune.roma.it" + u, "titolo": pulito(t), "data": d.isoformat()})
        if max(date).strftime("%Y-%m") < mese:
            break
        p += 1
    return voci, p


def elenco_gdf(c, mese):
    a = dt.date.fromisoformat(mese + "-01")
    b = (a.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    q = urllib.parse.urlencode([("portal_type", "News Item"), ("effective.query", f"{a}T00:00:00"),
                                ("effective.query", f"{b}T00:00:00"), ("effective.range", "min:max"),
                                ("sort_on", "effective"), ("b_size", "200"), ("fullobjects", "1")])
    js = json.loads(c.get(f"https://www.gdf.gov.it/++api++/@search?{q}"))
    voci = []
    for it in js.get("items", []):
        blob = json.dumps(it, ensure_ascii=False)
        if re.search(r"Comando Provinciale (?:di )?Roma|comando-provinciale-roma", blob, re.I):
            voci.append({"url": it.get("@id", "").replace("/++api++", ""), "titolo": it.get("title", ""),
                         "data": (it.get("effective") or "")[:10]})
    return voci, {"pagine": 1, "notizie_nazionali_del_mese": js.get("items_total")}


ELENCHI = {"C1": elenco_questura, "C2": elenco_carabinieri, "C3": elenco_procura,
           "C4": elenco_vvf, "C5": elenco_polizia_locale, "C6": elenco_gdf}


def valida(h, voce):
    """Il comunicato è la pagina chiesta? Corpo abbastanza lungo e non la vetrina dell'elenco."""
    t = testo(h)
    if BLOCCO.search(t[:3000]):
        return False, "pagina di blocco", t
    if len(t) < 600:
        return False, "testo troppo corto", t
    if voce.get("titolo") and voce["titolo"][:40].lower() not in t.lower():
        return True, "titolo non trovato nel testo", t
    return True, "", t


def _scrivi_json(path, obj):
    """Stato scritto intero su un temporaneo e sostituito: un'interruzione non lascia un JSON
    troncato che blocchi la ripresa (AGENTS.md, idempotenza al ritentativo)."""
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main(base, mese="2026-06", fonti=None):
    out = os.path.join(base, "ufficiali")
    os.makedirs(f"{out}/raw", exist_ok=True)
    c = Cliente()
    fonti = fonti or list(ELENCHI)
    # una seconda passata su alcune fonti sostituisce solo le loro voci, e solo se ne rilegge l'elenco
    precedente = json.load(open(f"{out}/inventario.json", encoding="utf-8")) if os.path.exists(f"{out}/inventario.json") else []
    inventario = [v for v in precedente if v["fonte"] not in fonti]
    rapporto = json.load(open(f"{out}/rapporto.json", encoding="utf-8")) if os.path.exists(f"{out}/rapporto.json") else {}
    for fonte in fonti:
        t0, r = time.time(), {"errori": []}
        try:
            voci, pagine = ELENCHI[fonte](c, mese)
            r["elenco"] = pagine
        except Exception as e:  # elenco non letto: le voci del giro precedente restano (ritentativo senza perdite)
            r["errori"].append(f"elenco: {e}")
            tenute = [v for v in precedente if v["fonte"] == fonte]
            r["voci_del_giro_precedente"] = len(tenute)
            inventario.extend(tenute)
            voci = []
        r["comunicati_del_mese"] = len(voci)
        for n, v in enumerate(voci, 1):
            v.update(fonte=fonte, id=f"{fonte}_{n:03d}")
            try:
                ok, nota, t = valida(c.get(v["url"]), v)
                v["stato"] = "ok" if ok else "rifiutato"
                v["nota"] = nota
                v["caratteri"] = len(t)
                with open(f"{out}/raw/{v['id']}.txt", "w", encoding="utf-8") as f:
                    f.write(t)
            except Rifiuto as e:
                v["stato"], v["nota"] = "rifiutato", str(e)
            except Exception as e:
                v["stato"], v["nota"] = "errore", str(e)[:200]
            inventario.append(v)
        r.update(scaricati=sum(1 for v in voci if v.get("stato") == "ok"),
                 rifiutati=sum(1 for v in voci if v.get("stato") == "rifiutato"),
                 errori_scaricamento=sum(1 for v in voci if v.get("stato") == "errore"),
                 secondi=round(time.time() - t0))
        rapporto[fonte] = r
        print(fonte, json.dumps(r, ensure_ascii=False), flush=True)
        _scrivi_json(f"{out}/inventario.json", inventario)
        _scrivi_json(f"{out}/rapporto.json", rapporto)
    return inventario, rapporto


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "2026-06", sys.argv[3:] or None)

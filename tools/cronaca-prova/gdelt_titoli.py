"""Titoli, link e ora degli articoli romani nei file grezzi di GDELT (indice aperto di notizie).

Uso: gdelt_titoli.py DIR [DAL AL]   (date AAAA-MM-GG, di default 2026-05-29 2026-07-03)

Legge l'elenco dei file del flusso «translation» (articoli non in inglese) e, per ogni file da
15 minuti del periodo, tiene le righe delle testate in TESTATE: data, testata, link e titolo
(<PAGE_TITLE>), più un segnale «Roma» dalle località che GDELT ha riconosciuto. Non legge mai
le pagine delle testate: usa solo i metadati pubblicati da GDELT (DEC-108, testate chiuse
solo come titolo, link e ora). Scrive DIR/gdelt/titoli.jsonl e DIR/gdelt/registro.json
(file letti, mancanti, righe per testata), riprende da dove si era fermato.
"""
import concurrent.futures as cf, datetime as dt, io, json, os, re, sys, time, urllib.request, zipfile

ELENCO = "https://data.gdeltproject.org/gdeltv2/masterfilelist-translation.txt"
UA = "QuartieriNews-ricerca/0.1 (misura copertura cronaca; solo metadati)"
TESTATE = {
    # chiuse agli agenti AI o in abbonamento: solo metadati
    "romatoday.it", "ilmessaggero.it", "corriere.it", "repubblica.it", "ansa.it", "leggo.it",
    "fanpage.it", "today.it", "agenzianova.com", "rainews.it", "adnkronos.com", "lapresse.it",
    "tg24.sky.it", "ilgiornale.it", "ilfattoquotidiano.it", "affaritaliani.it", "romait.it",
    # aperte: servono a misurare quanto GDELT copre, contro il censimento completo
    "iltempo.it", "dire.it", "romadailynews.it", "ilfaroonline.it", "abitarearoma.it",
    "vignaclarablog.it", "ilcorrieredellacitta.com",
}
TITOLO = re.compile(r"<PAGE_TITLE>(.*?)</PAGE_TITLE>", re.S)


def testata(dominio):
    d = dominio.lower()
    for t in TESTATE:
        if d == t or d.endswith("." + t):
            return t
    return None


def scarica(url, tries=4):
    url = url.replace("http://", "https://")
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # rete instabile o file non ancora pubblicato
            err = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"{url}: {err}")


def _salva_registro(reg_path, reg):
    """Il registro è il checkpoint: scritto intero su un temporaneo e sostituito."""
    tmp = f"{reg_path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reg, f)
    os.replace(tmp, reg_path)


def _ripristina(tit_path, letti):
    """Alla ripresa tiene solo le righe dei file registrati come letti: una
    caduta fra la scrittura delle righe e il checkpoint non lascia doppioni."""
    if not os.path.exists(tit_path):
        return 0
    tenute, scartate = [], 0
    with open(tit_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                riga = json.loads(line)
            except ValueError:          # riga troncata da una caduta a meta' scrittura
                scartate += 1
                continue
            if riga.get("file") in letti:
                tenute.append(line)
            else:
                scartate += 1
    if scartate:
        tmp = f"{tit_path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(tenute)
        os.replace(tmp, tit_path)
    return scartate


def leggi(url):
    righe = []
    nome = url.rsplit("/", 1)[-1]
    with zipfile.ZipFile(io.BytesIO(scarica(url))) as z:
        testo = z.read(z.namelist()[0]).decode("utf-8", "replace")
    for line in testo.split("\n"):
        f = line.split("\t")
        if len(f) < 27:
            continue
        t = testata(f[3])
        if not t:
            continue
        m = TITOLO.search(f[26])
        righe.append({"ora": f[1], "testata": t, "dominio": f[3], "link": f[4],
                      "titolo": m.group(1).strip() if m else "",
                      "roma": "Rome, Lazio" in f[9] or "Roma, Lazio" in f[9], "file": nome})
    return righe


def main(base, dal="2026-05-29", al="2026-07-03"):
    out = os.path.join(base, "gdelt")
    os.makedirs(out, exist_ok=True)
    reg_path, tit_path = f"{out}/registro.json", f"{out}/titoli.jsonl"
    reg = json.load(open(reg_path, encoding="utf-8")) if os.path.exists(reg_path) else {"letti": [], "mancanti": {}}
    fatti = set(reg["letti"])
    orfane = _ripristina(tit_path, {u.rsplit("/", 1)[-1] for u in fatti})
    if orfane:
        print(orfane, "righe di file non registrati scartate alla ripresa", flush=True)
    a, b = dal.replace("-", ""), (dt.date.fromisoformat(al) + dt.timedelta(days=1)).isoformat().replace("-", "")
    elenco = scarica(ELENCO).decode()
    urls = sorted({l.split()[2] for l in elenco.splitlines()
                   if l.count(" ") >= 2 and ".translation.gkg.csv.zip" in l
                   and a <= l.split()[2].rsplit("/", 1)[1][:8] < b})
    todo = [u for u in urls if u not in fatti]
    print(len(urls), "file nel periodo,", len(todo), "da leggere", flush=True)
    with open(tit_path, "a", encoding="utf-8") as fo, cf.ThreadPoolExecutor(4) as ex:
        futs = {ex.submit(leggi, u): u for u in todo}
        for i, fu in enumerate(cf.as_completed(futs), 1):
            u = futs[fu]
            try:
                for r in fu.result():
                    fo.write(json.dumps(r, ensure_ascii=False) + "\n")
                fo.flush()
                reg["letti"].append(u)
                reg["mancanti"].pop(u, None)
            except Exception as e:
                reg["mancanti"][u] = str(e)[:200]
            # checkpoint per file: le righe sono su disco prima che il file risulti letto
            _salva_registro(reg_path, reg)
            if i % 100 == 0:
                print(i, "letti,", len(reg["mancanti"]), "mancanti", flush=True)
    _salva_registro(reg_path, reg)
    print("fine:", len(reg["letti"]), "letti,", len(reg["mancanti"]), "mancanti", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(*sys.argv[1:4])

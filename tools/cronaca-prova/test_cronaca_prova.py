"""Controlli degli strumenti della prova Cronaca (nessuna rete, dati sintetici).

Uso: python3 tools/cronaca-prova/test_cronaca_prova.py
"""
import glob, json, os, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compila, filtro, prepara_lotti  # noqa: E402

FALLITI = []


def check(nome, cond):
    print(("ok   " if cond else "FAIL ") + nome)
    if not cond:
        FALLITI.append(nome)


def scrivi(path, obj, jsonl=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        if jsonl:
            f.write("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in obj))
        else:
            json.dump(obj, f, ensure_ascii=False)


# --- filtro: sezione dove la testata la dà, parole chiave altrimenti
r = lambda t, c=(): {"titolo": t, "categorie": list(c)}
check("filtro: Abitare a Roma per sezione, anche senza parola chiave",
      filtro.keep("abitarearoma", r("Festa finita male al parco", ["cronaca"])))
check("filtro: Abitare a Roma fuori sezione escluso",
      not filtro.keep("abitarearoma", r("Arrestato spacciatore", ["politica"])))
check("filtro: bollettino traffico di Roma Daily News escluso",
      not filtro.keep("romadailynews", r("traffico roma del 01 06 2026 incidente sulla tangenziale")))
check("filtro: parola chiave trovata in un titolo con accenti",
      filtro.keep("ilfaroonline", r("Ostia, perché è stato arrestato il ladro")))
check("filtro: Dire solo con sezione Roma o Lazio",
      not filtro.keep("dire", r("Rapina in banca a Milano", ["cronaca", "milano"]))
      and filtro.keep("dire", r("Rapina a Centocelle", ["roma"])))

# --- prepara_lotti: fuori Roma esclusi, pettine a 8 lotti, finestre delle decadi
with tempfile.TemporaryDirectory() as d:
    schede = [{"id": f"CR-C1_{i:03d}-1", "fonte": "C1", "data_pubblicazione": f"2026-06-{1 + i % 30:02d}",
               "data_fatto": "", "fatto": "x", "luoghi_testo": "", "municipio": "V", "fuori_roma": i % 10 == 0,
               "esito": "F" if i % 10 == 0 else "U", "pagine": ["centocelle"]} for i in range(40)]
    scrivi(f"{d}/schede.jsonl", schede, jsonl=True)
    facts = prepara_lotti.fatti_ufficiali([f"{d}/schede.jsonl"])
    check("prepara_lotti: i fatti fuori Roma (F) non entrano", len(facts) == 36 and all(f["esito"] != "F" for f in facts))
    lots = prepara_lotti.lotti_avanti(facts)
    check("prepara_lotti: 8 lotti che coprono tutti i fatti una volta",
          len(lots) == 8 and sorted(f["id"] for l in lots for f in l) == sorted(f["id"] for f in facts))
    cand = [{"sid": "S0001", "data": "2026-06-05", "testata": "Dire", "titolo": "a", "link": "u"},
            {"sid": "S0002", "data": "2026-06-30", "testata": "Dire", "titolo": "b", "link": "v"}]
    inv = prepara_lotti.lotti_inversi(cand, facts)
    check("prepara_lotti: tre decadi, il 30 nella terza",
          len(inv) == 3 and [len(l["titoli"]) for l in inv] == [1, 0, 1])
    check("prepara_lotti: la prima decade vede i comunicati fino a 8 giorni dopo",
          max(f["pubblicato"] for f in inv[0]["fatti_ufficiali"]) == "2026-06-18")

# --- compila: le righe non cercate non contano; scenari sulle pagine
with tempfile.TemporaryDirectory() as d:
    lot = [{"id": i, "fonte": "Questura di Roma", "pubblicato": "2026-06-02", "fatto": "x", "esito": "U",
            "pagine": ["centocelle"]} for i in ("A", "B", "C")]
    scrivi(f"{d}/avanti/lotto_1.json", lot)
    t = lambda n, c: {"testata": n, "url": "u", "titolo": "t", "data": None, "prova_data": "sconosciuta", "corrispondenza": c}
    scrivi(f"{d}/avanti/risultati_1.jsonl", [
        {"id": "A", "ricerche": ["q"], "testate": [t("RomaToday", "certa"), t("Abitare a Roma", "probabile")], "nota": ""},
        {"id": "B", "ricerche": ["q"], "testate": [], "nota": ""},
        {"id": "C", "ricerche": [], "testate": [t("RomaToday", "probabile")], "nota": "copiato da un'altra ricerca"},
    ], jsonl=True)
    scrivi(f"{d}/censimento/candidati.json", [{"sid": s, "titolo": "Carabinieri a Ostia", "link": "l"} for s in ("S1", "S2", "S3", "S4")])
    scrivi(f"{d}/inverso/fatti_1.jsonl", [
        {"fid": "P1-001", "sid": ["S1"], "testate": ["Il Faro Online"], "data": "2026-06-03", "tipo": "arresto", "fatto": "x",
         "luogo": "Ostia", "pagina_qn": "ostia", "livello": "quartiere", "ufficiale": None, "corrispondenza": None},
        {"fid": "P1-002", "sid": ["S2"], "testate": ["Il Faro Online", "Roma Daily News"], "data": "2026-06-03",
         "tipo": "furto", "fatto": "y", "luogo": None, "pagina_qn": "acilia", "livello": "quartiere", "ufficiale": None,
         "corrispondenza": None},
        {"fid": "P1-003", "sid": ["S4"], "testate": ["Il Tempo"], "data": "2026-06-02", "tipo": "arresto", "fatto": "z",
         "luogo": None, "pagina_qn": "centocelle", "livello": "quartiere", "ufficiale": "B", "corrispondenza": "certa"},
    ], jsonl=True)
    scrivi(f"{d}/inverso/scarti_1.jsonl", [{"sid": "S3", "classe": "non_cronaca"}], jsonl=True)
    with open(f"{d}/matrice.csv", "w", encoding="utf-8-sig") as f:
        f.write("slug;Cronaca propri\ncentocelle;2\nostia;0\nacilia;0\nprati;0\n")
    R = compila.main(d, f"{d}/matrice.csv")
    a, i = R["avanti"], R["inversa"]
    check("compila: una riga senza ricerche propria non è un fatto cercato", a["fatti_cercati"] == 2)
    check("compila: distribuzione delle testate per fatto cercato",
          a["certa_o_probabile"]["distribuzione_n_testate"] == {"0": 1, "2": 1}
          and a["solo_certa"]["distribuzione_n_testate"] == {"0": 1, "1": 1})
    check("compila: fatti solo stampa e con almeno due testate",
          i["solo_stampa"] == 2 and i["solo_stampa_con_almeno_due_testate"] == 1 and i["solo_stampa_con_ente_nel_titolo"] == 2)
    sc = i["scenari"]
    check("compila: scenari sulle pagine (A 1, B 3, C 2)",
          sc["A_ufficiali_pubbliche"]["pagine_con_almeno_uno"] == 1
          and sc["B_piu_testate_aperte_dopo_conferma_massimo"]["pagine_con_almeno_uno"] == 3
          and sc["C_piu_fatti_su_due_testate_aperte"]["pagine_con_almeno_uno"] == 2)
    nu = R["notizie_uniche"]
    check("compila: notizie uniche con le testate delle due passate unite",
          nu["totale"] == 5 and nu["ufficiali_cercati"] == {"1": 1, "2": 1}
          and nu["ufficiali_non_cercati"] == {"0": 1} and nu["solo_testate_aperte"] == {"1": 1, "2": 1})
    check("compila: il riepilogo non contiene link né titoli",
          "http" not in json.dumps(R) and "Carabinieri a Ostia" not in json.dumps(R))

    def fallisce(parola, path, obj, jsonl=False):
        scrivi(path, obj, jsonl=jsonl)
        try:
            compila.main(d, f"{d}/matrice.csv"); esito = False
        except SystemExit as e:
            esito = parola in str(e)
        os.remove(path)
        return esito
    check("compila: un lotto avanti letto due volte ferma la compilazione",
          fallisce("ripetuti", f"{d}/avanti/risultati_2.jsonl", [{"id": "A", "ricerche": ["q"], "testate": [], "nota": ""}], True))
    check("compila: un risultato con id fuori dai lotti ferma la compilazione",
          fallisce("nessun lotto", f"{d}/avanti/risultati_2.jsonl", [{"id": "Z", "ricerche": ["q"], "testate": [], "nota": ""}], True))
    check("compila: un sid che non è fra i candidati ferma la compilazione",
          fallisce("candidati", f"{d}/inverso/scarti_2.jsonl", [{"sid": "S9", "classe": "non_cronaca"}], True))
    check("compila: un sid classificato due volte ferma la compilazione",
          fallisce("ripetuti", f"{d}/inverso/scarti_2.jsonl", [{"sid": "S3", "classe": "giudiziaria"}], True))
    os.rename(f"{d}/inverso/scarti_1.jsonl", f"{d}/scarti_via")
    try:
        compila.main(d, f"{d}/matrice.csv"); manc = False
    except SystemExit as e:
        manc = "senza esito" in str(e)
    os.rename(f"{d}/scarti_via", f"{d}/inverso/scarti_1.jsonl")
    check("compila: un candidato senza esito ferma la compilazione", manc)

# --- fonti_ufficiali: elenchi per fonte su pagine sintetiche, riconoscimento dei blocchi
import fonti_ufficiali as F  # noqa: E402


class Finto:
    def __init__(self, pagine):
        self.pagine, self.chieste = pagine, []

    def get(self, url):
        self.chieste.append(url)
        for chiave, h in self.pagine.items():
            if chiave in url:
                return h
        return ""


def q_item(n, data):
    return (f'<div class="elenco_notizie notizia"><h3><a href="/it/Roma/articolo/{n}">Arresto {n}</a></h3>'
            f'<div class="content"><p><em>{data}</em> </p></div></div>')


c = Finto({"/1/": q_item("a1", "02-07-2026") + q_item("a2", "30-06-2026"),
           "/2/": q_item("a3", "15-06-2026") + q_item("a4", "31-05-2026"),
           "/3/": q_item("a5", "20-05-2026")})
voci, pagine = F.elenco_questura(c, "2026-06")
check("fonti_ufficiali: Questura, solo giugno e stop alla prima pagina tutta di maggio",
      [v["url"][-2:] for v in voci] == ["a2", "a3"] and pagine == 3)

riga = ('<tr><td class=tabellaD>{d} 10:00<td class=tabellaD><a id=x href={u}><span id=l>{luogo} - </span>{t}</a>'
        '<td class=tabellaD><span id=f>Comando Provinciale di&nbsp;</span>{cmd} <br>')
cc = Finto({"d=202606": riga.format(d="30/06/2026", u="https://www.carabinieri.it/c/a", luogo="Roma", t="Arresto", cmd="Roma")
            + riga.format(d="29/06/2026", u="https://www.carabinieri.it/c/b", luogo="Este (PD)", t="Pusher", cmd="Padova")
            + riga.format(d="28/06/2026", u='"https://www.carabinieri.it/c/l\'x"', luogo="Velletri (RM)", t="Furto", cmd="Roma")})
voci, info = F.elenco_carabinieri(cc, "2026-06")
check("fonti_ufficiali: Carabinieri, filtro Roma e provincia fra i nazionali",
      [v["url"] for v in voci] == ["https://www.carabinieri.it/c/a", "https://www.carabinieri.it/c/l'x"]
      and info["comunicati_nazionali"] == 3)

vvf = ('<article class="node"><a href="http://www.vigilfuoco.it/media/notizie/uno"></a><h2>Uno</h2>'
       '<span>01 Giugno 2026</span></article><article><a href="/comando-vvf-roma/notizie/due"></a>'
       '<h2>Due</h2> 19 Giugno 2026</article><article><a href="/media/notizie/tre"></a> 30 Maggio 2026</article>')
voci, _ = F.elenco_vvf(Finto({"vigilfuoco": vvf}), "2026-06")
check("fonti_ufficiali: Vigili del Fuoco, una voce per articolo con la sua data",
      [(v["url"].rsplit("/", 1)[1], v["data"]) for v in voci] == [("uno", "2026-06-01"), ("due", "2026-06-19")])

pl = ('<span class="Card-date">8 ottobre 2026</span><a class="Card-titleLink" href="/web/it/notizia/portale.page">X</a>'
      '<p class="List-date">15 giugno 2026</p> <p class="List-title"> <a href="/web/it/notizia/pl-a.page">A</a> </p>'
      '<p class="List-date">2 maggio 2026</p> <p class="List-title"> <a href="/web/it/notizia/pl-b.page">B</a> </p>')
voci, _ = F.elenco_polizia_locale(Finto({"pagina=": pl}), "2026-06")
check("fonti_ufficiali: Polizia Locale dall'elenco della struttura, non dalle notizie in evidenza",
      [v["url"].rsplit("/", 1)[1] for v in voci] == ["pl-a.page"])

ok, nota, _ = F.valida("<html><title>Accesso negato | Polizia di Stato</title><body>Accesso negato</body></html>", {})
check("fonti_ufficiali: la pagina «Accesso negato» servita con 200 non vale come comunicato", not ok and "blocco" in nota)
ok, nota, _ = F.valida("<html><body><p>Il sistema è temporaneamente non disponibile ci scusiamo per il disagio...</p></body></html>", {})
check("fonti_ufficiali: la pagina «sistema temporaneamente non disponibile» servita con 200 è un rifiuto, non un comunicato",
      not ok and "blocco" in nota)
check("fonti_ufficiali: un elenco servito come «non disponibile» non vale come elenco vuoto (si ritenta, poi è un rifiuto)",
      F.BLOCCO.search("Il sistema è temporaneamente non disponibile ci scusiamo") is not None)
ok, nota, _ = F.valida("<p>" + "testo del comunicato " * 60 + "</p>", {"titolo": "Arresto a Centocelle"})
check("fonti_ufficiali: testo lungo senza il titolo resta valido ma annotato", ok and nota)


class Risposta:
    def __init__(self, testo):
        self.testo = testo

    def read(self):
        return self.testo.encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


sleep, urlopen = F.time.sleep, F.urllib.request.urlopen
F.time.sleep = lambda s: None
F.urllib.request.urlopen = lambda req, timeout=0: Risposta("<h1>Accesso negato</h1>")
cl = F.Cliente()
for _ in range(2):
    try:
        cl.get("https://questure.poliziadistato.it/x")
    except Exception:
        pass
check("fonti_ufficiali: dopo cinque rifiuti di fila l'ente viene fermato, senza altri tentativi",
      "questure.poliziadistato.it" in cl.fermi)
F.time.sleep, F.urllib.request.urlopen = sleep, urlopen

# stato scritto in modo atomico: nessun temporaneo residuo, file leggibili dopo ogni fonte
with tempfile.TemporaryDirectory() as d:
    elenchi, cliente = F.ELENCHI, F.Cliente
    F.ELENCHI = {"C9": lambda c, mese: ([], 1)}
    F.Cliente = lambda: Finto({})
    try:
        inv, rap = F.main(d, "2026-06", ["C9"])
    finally:
        F.ELENCHI, F.Cliente = elenchi, cliente
    u = os.path.join(d, "ufficiali")
    check("fonti_ufficiali: inventario e rapporto scritti per sostituzione, senza temporanei residui",
          sorted(f for f in os.listdir(u) if f != "raw") == ["inventario.json", "rapporto.json"]
          and json.load(open(os.path.join(u, "rapporto.json"), encoding="utf-8"))["C9"]["comunicati_del_mese"] == 0
          and json.load(open(os.path.join(u, "inventario.json"), encoding="utf-8")) == [])
    # ritentativo su una fonte: se l'elenco non si legge, le sue voci del giro precedente restano
    scrivi(os.path.join(u, "inventario.json"), [{"fonte": "C8", "id": "C8_001", "url": "https://x/8", "stato": "ok"},
                                                {"fonte": "C9", "id": "C9_001", "url": "https://x/9", "stato": "ok"}])
    def rotto(c, mese):
        raise RuntimeError("elenco giu'")
    F.ELENCHI = {"C8": rotto, "C9": lambda c, mese: ([{"url": "https://x/9b", "data": "2026-06-02", "titolo": "t"}], 1)}
    F.Cliente = lambda: Finto({})
    try:
        inv, rap = F.main(d, "2026-06", ["C8", "C9"])
    finally:
        F.ELENCHI, F.Cliente = elenchi, cliente
    check("fonti_ufficiali: elenco non letto al ritentativo: le voci precedenti della fonte restano, il rapporto lo dice",
          [v["id"] for v in inv if v["fonte"] == "C8"] == ["C8_001"] and rap["C8"]["voci_del_giro_precedente"] == 1
          and rap["C8"]["errori"] == ["elenco: elenco giu'"])
    check("fonti_ufficiali: elenco riletto al ritentativo: le voci precedenti della fonte sono sostituite",
          [v["url"] for v in inv if v["fonte"] == "C9"] == ["https://x/9b"] and "voci_del_giro_precedente" not in rap["C9"])

# --- gdelt_titoli: testate per dominio, righe dal file da 15 minuti
import gdelt_titoli as G, io, zipfile  # noqa: E402

check("gdelt_titoli: sottodomini ricondotti alla testata", G.testata("roma.corriere.it") == "corriere.it"
      and G.testata("notcorriere.it") is None)
riga_gkg = lambda dom, url, titolo, loc: "\t".join(["id", "20260610120000", "1", dom, url, *[""] * 4, loc, *[""] * 16,
                                                     f"<PAGE_TITLE>{titolo}</PAGE_TITLE>"])
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("x.csv", "\n".join([riga_gkg("romatoday.it", "https://www.romatoday.it/cronaca/a.html", "Furto a Prati",
                                            "4#Rome, Lazio, Italy#IT"),
                                   riga_gkg("lanazione.it", "https://www.lanazione.it/b", "Altro", "")]))
scarica = G.scarica
G.scarica = lambda url, tries=4: buf.getvalue()
righe = G.leggi("https://data.gdeltproject.org/x.zip")
G.scarica = scarica
check("gdelt_titoli: solo le testate seguite, con titolo e segnale Roma",
      len(righe) == 1 and righe[0]["titolo"] == "Furto a Prati" and righe[0]["roma"] and righe[0]["file"] == "x.zip")
with tempfile.TemporaryDirectory() as d:
    tit = f"{d}/titoli.jsonl"
    scrivi(tit, [{"link": "a", "file": "A.zip"}, {"link": "b", "file": "B.zip"}, {"link": "c", "file": "B.zip"}], jsonl=True)
    scartate = G._ripristina(tit, {"A.zip"})
    rest = [json.loads(l) for l in open(tit, encoding="utf-8")]
    check("gdelt_titoli: alla ripresa le righe di un file non registrato come letto vengono scartate (niente doppioni)",
          scartate == 2 and [r["file"] for r in rest] == ["A.zip"] and not [f for f in os.listdir(d) if f.endswith(".tmp")])
    with open(tit, "a", encoding="utf-8") as f:
        f.write('{"link": "d", "file": "A.z')          # caduta a meta' scrittura
    check("gdelt_titoli: una riga troncata da una caduta non blocca la ripresa, viene scartata",
          G._ripristina(tit, {"A.zip"}) == 1 and [json.loads(l)["link"] for l in open(tit, encoding="utf-8")] == ["a"])
    with open(tit, "a", encoding="utf-8") as f:
        f.write(json.dumps({"link": "legacy", "ora": "20260601000000"}) + "\n")   # riga della versione precedente
    check("gdelt_titoli: le righe senza campo file (formato precedente) restano alla ripresa",
          G._ripristina(tit, {"A.zip"}) == 0 and [json.loads(l)["link"] for l in open(tit, encoding="utf-8")] == ["a", "legacy"])
    G._salva_registro(f"{d}/registro.json", {"letti": ["A.zip"], "mancanti": {}})
    check("gdelt_titoli: il registro è scritto per intero e sostituito",
          json.load(open(f"{d}/registro.json"))["letti"] == ["A.zip"] and not [f for f in os.listdir(d) if f.endswith(".tmp")])

# --- censimento: una risposta 200 non interpretabile è un errore, non una testata vuota
import censimento as C  # noqa: E402

_get = C.get
C.get = lambda url, tries=3: ("<html>Access denied</html>", {})
try:
    C.wordpress("abitarearoma.it"); wp_err = False
except C.Censimento as e:
    wp_err = "non interpretabile" in str(e)
try:
    C.sitemap("www.romadailynews.it"); sm_err = False
except C.Censimento as e:
    sm_err = "post-sitemap" in str(e)
C.get = lambda url, tries=3: ("[]", {"x-wp-totalpages": "1"})
vuoto = C.wordpress("abitarearoma.it")
giorni = []
C.get = lambda url, tries=3: (giorni.append(url.split("/")[-2]) or "<loc>https://www.iltempo.it/roma/2026/06/15/news/x-1</loc>", {})
C.iltempo()
check("censimento: iltempo chiede solo i giorni che il mese ha (giugno: 30), non 31",
      sorted(set(giorni)) == [f"2026-06-{d:02d}" for d in range(1, 31)])
chiamate = []
def _get_cento(url, tries=3):
    chiamate.append(url)
    if "/categories?" in url:
        return (json.dumps([{"id": i, "slug": f"c{i}"} for i in range(100)]), {"x-wp-totalpages": "1"})
    return ("[]", {"x-wp-totalpages": "1"})
C.get = _get_cento
C.wordpress("abitarearoma.it")
C.get = _get
check("censimento: con esattamente 100 categorie non si chiede la pagina 2 (errore dell'API, non fine elenco)",
      sum("/categories?" in u for u in chiamate) == 1)
check("censimento: HTML servito con 200 al posto dell'API o della sitemap è un errore esplicito", wp_err and sm_err)
check("censimento: una lista JSON vuota è un mese senza articoli, non un errore", vuoto == [])

# --- testi_aperti: tetto alle richieste, un sid una volta, sid ignoti rifiutati
import testi_aperti as T  # noqa: E402

cand = {f"S{i:04d}": {"sid": f"S{i:04d}", "link": "https://x/a", "testata": "Dire"} for i in range(1, 400)}
check("testi_aperti: un sid ripetuto si scarica una volta",
      T.sids_da_scaricare([{"sid": ["S0001", "S0002"]}, "S0001"], cand) == ["S0001", "S0002"])
try:
    T.sids_da_scaricare([f"S{i:04d}" for i in range(1, 302)], cand); cap_ok = False
except SystemExit as e:
    cap_ok = "tetto" in str(e)
try:
    T.sids_da_scaricare(["S9999"], cand); ign_ok = False
except SystemExit as e:
    ign_ok = "non presenti" in str(e)
check("testi_aperti: oltre il tetto (QN_MAX_TESTI) e con sid ignoti ci si ferma prima di ogni richiesta", cap_ok and ign_ok)

# --- chiuse_filtro: sezioni romane, nomi di quartiere non ambigui, testate aperte escluse
import chiuse_filtro as K  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    scrivi(f"{d}/gaz.json", {"neighbourhoods": [{"name_display": "Centocelle", "aliases": ""},
                                                {"name_display": "Trieste", "aliases": ""}],
                             "publication_zones": [{"name_display": "Prati"}]})
    g = lambda dom, link, titolo, ora="20260610120000": {"ora": ora, "testata": dom, "dominio": dom, "link": link,
                                                         "titolo": titolo, "roma": False}
    scrivi(f"{d}/gdelt/titoli.jsonl", [
        g("romatoday.it", "https://www.romatoday.it/cronaca/a.html", "Arrestato pusher"),
        g("romatoday.it", "https://www.romatoday.it/cronaca/a.html", "Arrestato pusher"),
        g("ansa.it", "https://www.ansa.it/sito/notizie/b.html", "Rapina a Centocelle, preso"),
        g("ansa.it", "https://www.ansa.it/sito/notizie/c.html", "Trieste, rapina in centro"),
        g("ilmessaggero.it", "https://www.ilmessaggero.it/roma/d.html", "La nuova pista ciclabile"),
        g("dire.it", "https://www.dire.it/e", "Roma, arrestato ladro"),
        g("leggo.it", "https://www.leggo.it/roma/f.html", "Incendio a Prati", "20260801120000")], jsonl=True)
    out = K.main(d, f"{d}/gaz.json")
    check("chiuse_filtro: link una volta, sezione romana, quartiere non ambiguo, niente aperte né fuori periodo",
          sorted(o["link"].rsplit("/", 1)[1] for o in out) == ["a.html", "b.html"])
    check("chiuse_filtro: editore per testata",
          {o["testata"]: o["editore"] for o in out} == {"ANSA": "ANSA", "RomaToday": "Citynews"})
    scrivi(f"{d}/gdelt/titoli.jsonl", [
        g("ansa.it", "https://www.ansa.it/sito/notizie/n1.html", "Rapina a Centocelle", "20260630223000"),  # 1° luglio a Roma
        g("ansa.it", "https://www.ansa.it/sito/notizie/n2.html", "Rapina a Centocelle", "20260531220000"),  # 1° giugno a Roma
        g("ansa.it", "https://www.ansa.it/sito/notizie/n3.html", "Rapina a Centocelle", "20260703230000")], jsonl=True)  # 4 luglio: fuori
    out = K.main(d, f"{d}/gaz.json")
    check("chiuse_filtro: la data è il giorno di Roma, non quello UTC di GDELT, e DAL/AL valgono su quello",
          [(o["data"], o["ora"]) for o in out] == [("2026-06-01", "20260531220000"), ("2026-07-01", "20260630223000")])
    scrivi(f"{d}/gdelt/titoli.jsonl", [
        g("ansa.it", "https://www.ansa.it/sito/notizie/m.html", "Titolo senza luogo"),            # stesso link, scartata
        g("ansa.it", "https://www.ansa.it/sito/notizie/m.html", "Rapina a Centocelle, preso"),    # qualificata
        g("ansa.it", "https://www.ansa.it/sito/notizie/m.html", "Rapina a Centocelle, preso")], jsonl=True)
    out = K.main(d, f"{d}/gaz.json")
    check("chiuse_filtro: un'occorrenza scartata dello stesso link non blocca quella candidata; il link resta uno",
          [o["link"].rsplit("/", 1)[1] for o in out] == ["m.html"])
check("chiuse_filtro: cambio d'ora: le 23:30 UTC del 31 ottobre sono già il 1° novembre a Roma (+1), le 23:30 UTC del 30 giugno il 1° luglio (+2)",
      K.giorno_locale("20261031233000") == "2026-11-01" and K.giorno_locale("20260630223000") == "2026-07-01"
      and K.giorno_locale("20261031225900") == "2026-10-31")

# --- prepara_chiuse: senza candidati nessun lotto, non un errore
import prepara_chiuse as PC  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    scrivi(f"{d}/chiuse/candidati.json", [])
    scrivi(f"{d}/uff.jsonl", [], jsonl=True)
    scrivi(f"{d}/aperte.jsonl", [], jsonl=True)
    check("prepara_chiuse: con candidati.json vuoto non scrive lotti e torna 0",
          PC.main(d, "/pkg", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"]) == 0 and not glob.glob(f"{d}/chiuse/lotto_*.json"))

# --- tabella_quartieri: regola delle due fonti per editore, fusioni, mese
import tabella_quartieri as TQ  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    with open(f"{d}/matrice.csv", "w", encoding="utf-8-sig") as f:
        f.write("pagina;slug;municipio\nCentocelle;centocelle;V\nPrati;prati;I\nOstia;ostia;X\nTrieste;trieste;II\n")
    scheda = lambda i, esito, pagine: {"id": i, "fuori_roma": False, "data_fatto": "", "data_pubblicazione": "2026-06-05",
                                       "fatto": "x", "esito": esito, "livello_portata": "quartiere", "pagine": pagine}
    scrivi(f"{d}/uff.jsonl", [scheda("CR-1", "U", ["centocelle"]), scheda("CR-2", "D", [])], jsonl=True)
    ap = lambda fid, testate, pagina, uff=None: {"fid": fid, "data": "2026-06-06", "tipo": "furto", "fatto": "y",
                                                 "luogo": None, "pagina_qn": pagina, "livello": "quartiere",
                                                 "testate": testate, "ufficiale": uff, "sid": []}
    scrivi(f"{d}/aperte.jsonl", [ap("P1", ["Abitare a Roma"], "prati"),          # + RomaToday: due editori
                                 ap("P2", ["Il Tempo"], "ostia"),                 # + il Giornale: stesso editore
                                 ap("P3", ["Roma Daily News"], "trieste"),         # nessuna chiusa
                                 ap("P4", ["Dire"], None, uff="CR-1")], jsonl=True)
    scrivi(f"{d}/chiuse/candidati.json", [
        {"cid": "K1", "testata": "RomaToday", "editore": "Citynews", "link": "l1"},
        {"cid": "K2", "testata": "il Giornale", "editore": "Angelucci", "link": "l2"},
        {"cid": "K3", "testata": "ANSA", "editore": "ANSA", "link": "l3"},
        {"cid": "K4", "testata": "Il Messaggero", "editore": "Caltagirone", "link": "l4"},
        {"cid": "K5", "testata": "Leggo", "editore": "Caltagirone", "link": "l5"},
        {"cid": "K6", "testata": "RomaToday", "editore": "Citynews", "link": "l6"}])
    scrivi(f"{d}/chiuse/abbinamenti_1.jsonl", [
        {"cid": "K1", "classe": "cronaca_roma", "fatto": "P1", "corrispondenza": "certa"},
        {"cid": "K2", "classe": "cronaca_roma", "fatto": "P2", "corrispondenza": "certa"},
        {"cid": "K3", "classe": "cronaca_roma", "fatto": "N1-001", "corrispondenza": None},
        {"cid": "K4", "classe": "cronaca_roma", "fatto": "N1-002", "corrispondenza": None},
        {"cid": "K5", "classe": "cronaca_roma", "fatto": "N2-001", "corrispondenza": None},
        {"cid": "K6", "classe": "cronaca_roma", "fatto": "N2-002", "corrispondenza": None}], jsonl=True)
    nuovo = lambda nid, data, pagina: {"nid": nid, "cid": [], "data": data, "tipo": "rapina", "fatto": "z",
                                       "luogo": None, "pagina_qn": pagina, "livello": "quartiere"}
    scrivi(f"{d}/chiuse/nuovi_1.jsonl", [nuovo("N1-001", "2026-06-20", "trieste"), nuovo("N1-002", "2026-06-20", "trieste")],
           jsonl=True)
    scrivi(f"{d}/chiuse/nuovi_2.jsonl", [nuovo("N2-001", "2026-06-20", "trieste"), nuovo("N2-002", "2026-07-01", "ostia")],
           jsonl=True)
    scrivi(f"{d}/chiuse/fusioni.json", {"N2-001": "N1-002"})
    R = TQ.main(d, f"{d}/matrice.csv", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"])
    cat = {f["id"]: f["categoria"] for f in json.load(open(f"{d}/tabella/fatti.json"))}
    check("tabella_quartieri: testata aperta più una chiusa di altro editore = due fonti",
          cat["P1"] == "stampa_due_fonti")
    check("tabella_quartieri: Il Tempo e il Giornale sono lo stesso editore = una fonte", cat["P2"] == "stampa_una_fonte")
    check("tabella_quartieri: fatto ufficiale ripreso da una testata aperta resta uno", "P4" not in cat and cat["CR-1"] == "ufficiale")
    check("tabella_quartieri: fusione fra lotti e Il Messaggero + Leggo = un editore",
          "N2-001" not in cat and cat["N1-002"] == "chiuse_una_fonte" and cat["N1-001"] == "chiuse_una_fonte")
    check("tabella_quartieri: fatti nuovi fuori dal mese esclusi", "N2-002" not in cat)
    check("tabella_quartieri: pagine coperte (ufficiali 1, pubblicabili 2)",
          R["pagine_coperte"]["solo_ufficiali"] == 1 and R["pagine_coperte"]["ufficiali_piu_stampa_due_fonti"] == 2
          and R["pagine_scoperte"] == ["ostia", "trieste"])
    check("tabella_quartieri: la seconda fonte di P1 viene solo da una chiusa; l'abbinamento al fatto fuori mese è contato",
          R["seconda_fonte"] == {"anche_da_aperte": 0, "solo_da_chiuse": 1} and R["abbinamenti_a_fatti_esclusi"] == 1)

    def rifiuta(parola, righe):
        scrivi(f"{d}/chiuse/abbinamenti_2.jsonl", righe, jsonl=True)
        try:
            TQ.main(d, f"{d}/matrice.csv", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"]); esito = False
        except SystemExit as e:
            esito = parola in str(e)
        os.remove(f"{d}/chiuse/abbinamenti_2.jsonl")
        return esito
    check("tabella_quartieri: un cid ignoto negli abbinamenti ferma la tabella",
          rifiuta("ignoti", [{"cid": "K9", "classe": "cronaca_roma", "fatto": "P1"}]))
    check("tabella_quartieri: un cid abbinato due volte (lotto letto due volte) ferma la tabella",
          rifiuta("ripetuti", [{"cid": "K1", "classe": "cronaca_roma", "fatto": "P1"}]))
    orig = [json.loads(l) for l in open(f"{d}/chiuse/abbinamenti_1.jsonl", encoding="utf-8")]
    scrivi(f"{d}/chiuse/abbinamenti_1.jsonl", orig[:-1] + [{"cid": "K6", "classe": "cronaca_roma", "fatto": "X-999"}], jsonl=True)
    try:
        TQ.main(d, f"{d}/matrice.csv", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"]); ign = False
    except SystemExit as e:
        ign = "ignoto" in str(e)
    scrivi(f"{d}/chiuse/abbinamenti_1.jsonl", orig, jsonl=True)
    check("tabella_quartieri: un abbinamento a un fatto ignoto ferma la tabella (uno a un fatto escluso no, sopra)", ign)
    # doppione fra fatti delle testate aperte e fatto su più pagine
    scrivi(f"{d}/aperte.jsonl", [ap("P1", ["Abitare a Roma"], "prati"), ap("P2", ["Il Tempo"], "ostia"),
                                 ap("P3", ["Roma Daily News"], "trieste"), ap("P4", ["Dire"], None, uff="CR-1"),
                                 ap("P5", ["Il Faro Online"], None)], jsonl=True)
    scrivi(f"{d}/aperte_fusioni.json", {"P5": "P3"})
    scrivi(f"{d}/luoghi/pagine_multiple.json", {"P3": ["trieste", "ostia"]})
    R = TQ.main(d, f"{d}/matrice.csv", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"])
    fatti = {f["id"]: f for f in json.load(open(f"{d}/tabella/fatti.json"))}
    check("tabella_quartieri: il doppione delle testate aperte porta la sua testata al fatto che resta",
          "P5" not in fatti and fatti["P3"]["categoria"] == "stampa_due_fonti")
    check("tabella_quartieri: un fatto su più pagine conta su ciascuna", fatti["P3"]["pagine"] == ["trieste", "ostia"]
          and R["pagine_scoperte"] == [])
    # il mese viene da QN_MESE (README passo 12, mese diverso da giugno): i fatti nuovi di luglio entrano, quelli di giugno no
    os.environ["QN_MESE"] = "2026-07"
    try:
        TQ.main(d, f"{d}/matrice.csv", [f"{d}/uff.jsonl"], [f"{d}/aperte.jsonl"])
    finally:
        del os.environ["QN_MESE"]
    cat = {f["id"]: f["categoria"] for f in json.load(open(f"{d}/tabella/fatti.json"))}
    check("tabella_quartieri: QN_MESE sceglie il mese dei fatti nuovi delle testate chiuse",
          "N2-002" in cat and "N1-001" not in cat and "N1-002" not in cat)

print("ALL PASS" if not FALLITI else f"{len(FALLITI)} FAILED")
sys.exit(1 if FALLITI else 0)

"""Titoli delle testate chiuse (da GDELT) candidati alla cronaca romana del mese.

Uso: chiuse_filtro.py DIR GAZETTEER.json [DAL AL]   (date AAAA-MM-GG, di default 2026-05-29 2026-07-03)

Legge DIR/gdelt/titoli.jsonl (gdelt_titoli.py). Tiene le testate senza censimento proprio
(le sei aperte hanno il loro, completo), un link una volta sola, e i titoli che sono cronaca
romana per sezione dell'URL (le pagine romane delle testate nazionali) o, per le testate
nazionali, per nome di Roma o di un quartiere del gazetteer nel titolo; poi le parole chiave
di filtro.py. Il filtro è largo: decide la lettura (ISTRUZIONI_CHIUSE.md).
Scrive DIR/chiuse/candidati.json con editore, data, ora, titolo e link.
"""
import html, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filtro import KW, norm  # noqa: E402

EDITORE = {
    "romatoday.it": "Citynews", "today.it": "Citynews", "ilmessaggero.it": "Caltagirone", "leggo.it": "Caltagirone",
    "corriere.it": "RCS", "repubblica.it": "GEDI", "ansa.it": "ANSA", "agenzianova.com": "Agenzia Nova",
    "rainews.it": "RAI", "adnkronos.com": "Adnkronos", "lapresse.it": "LaPresse", "tg24.sky.it": "Sky",
    "ilgiornale.it": "Angelucci", "iltempo.it": "Angelucci", "ilfattoquotidiano.it": "SEIF",
    "affaritaliani.it": "Affaritaliani", "romait.it": "RomaIT", "fanpage.it": "Ciaopeople",
    "abitarearoma.it": "Abitare a Roma", "romadailynews.it": "Roma Daily News", "ilfaroonline.it": "Il Faro Online",
    "vignaclarablog.it": "VignaClaraBlog", "dire.it": "Dire",
}
NOME = {
    "romatoday.it": "RomaToday", "today.it": "Today.it", "ilmessaggero.it": "Il Messaggero", "leggo.it": "Leggo",
    "corriere.it": "Corriere della Sera Roma", "repubblica.it": "la Repubblica Roma", "ansa.it": "ANSA",
    "agenzianova.com": "Agenzia Nova", "rainews.it": "Rai News", "adnkronos.com": "Adnkronos", "lapresse.it": "LaPresse",
    "tg24.sky.it": "Sky TG24", "ilgiornale.it": "il Giornale", "ilfattoquotidiano.it": "il Fatto Quotidiano",
    "affaritaliani.it": "Affaritaliani", "romait.it": "RomaIT", "fanpage.it": "Fanpage",
}
APERTE = {"abitarearoma.it", "romadailynews.it", "ilfaroonline.it", "vignaclarablog.it", "dire.it", "iltempo.it",
          "ilcorrieredellacitta.com"}
# sezioni romane delle testate nazionali: l'URL basta a dire "Roma"
SEZIONE_ROMA = [("romatoday.it", r"romatoday\.it/(cronaca|zone|dossier|attualita)/"),
                ("ilmessaggero.it", r"ilmessaggero\.it/roma/"), ("corriere.it", r"roma\.corriere\.it/"),
                ("repubblica.it", r"roma\.repubblica\.it/"), ("ansa.it", r"ansa\.it/lazio/"),
                ("leggo.it", r"leggo\.it/roma/"), ("rainews.it", r"rainews\.it/tgr/lazio/"),
                ("fanpage.it", r"fanpage\.it/roma/"), ("romait.it", r"romait\.it/")]


# nomi di quartieri o località romane che nei titoli nazionali indicano quasi sempre altro
AMBIGUI = {"italia", "ponte", "certosa", "trieste", "colonna", "ripa", "regola", "monti", "trevi", "capitale",
           "marconi", "san giorgio", "san paolo", "san giovanni", "farnesina", "salario", "verbano", "europa",
           "nomentano", "flaminio", "vittoria", "della vittoria", "sallustiano", "castro pretorio", "pigna",
           "sant'andrea", "san lorenzo", "san basilio", "san saba", "esposizione", "belle arti", "giuliano", "campidoglio"}


def luoghi_romani(gazetteer):
    g = json.load(open(gazetteer))
    nomi = {"roma", "capitale", "campidoglio", "ostia", "fiumicino aeroporto"}
    for n in g["neighbourhoods"]:
        nomi.add(norm(n["name_display"]))
        nomi |= {norm(a) for a in (n.get("aliases") or "").split(";") if a.strip()}
    for z in g["publication_zones"]:
        nomi.add(norm(z["name_display"]))
    nomi = {n for n in nomi if len(n) >= 4} - AMBIGUI
    return re.compile(r"\b(" + "|".join(sorted(map(re.escape, nomi), key=len, reverse=True)) + r")\b")


def main(base, gazetteer, dal="2026-05-29", al="2026-07-03"):
    roma = luoghi_romani(gazetteer)
    visti, out = set(), []
    for line in open(f"{base}/gdelt/titoli.jsonl"):
        r = json.loads(line)
        t = r["testata"]
        if t in APERTE or r["link"] in visti:
            continue
        data = f"{r['ora'][:4]}-{r['ora'][4:6]}-{r['ora'][6:8]}"
        if not dal <= data <= al:
            continue
        visti.add(r["link"])
        titolo = html.unescape(r["titolo"])
        slug = re.sub(r"[-_/]+", " ", r["link"].split("/", 3)[-1])
        testo = norm(titolo + " " + slug)
        sezione = any(t == d and re.search(p, r["link"]) for d, p in SEZIONE_ROMA)
        if not (sezione or roma.search(norm(titolo))):
            continue
        if not KW.search(testo):
            continue
        out.append({"testata": NOME.get(t, t), "dominio": t, "editore": EDITORE.get(t, t), "data": data,
                    "ora": r["ora"], "titolo": titolo, "link": r["link"], "sezione_roma": sezione})
    out.sort(key=lambda x: (x["ora"], x["testata"]))
    for i, x in enumerate(out, 1):
        x["cid"] = f"K{i:05d}"
    os.makedirs(f"{base}/chiuse", exist_ok=True)
    json.dump(out, open(f"{base}/chiuse/candidati.json", "w"), ensure_ascii=False, indent=0)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    res = main(*sys.argv[1:5])
    import collections
    print(len(res), collections.Counter(x["testata"] for x in res).most_common())

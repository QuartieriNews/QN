"""Filtro per parole chiave dei titoli censiti: tiene i candidati alla cronaca romana.

Uso: filtro.py DIR   (legge DIR/censimento/*.json, scrive DIR/censimento/candidati.json)

Il filtro è largo apposta: la classificazione vera (cronaca a Roma, fuori Roma, non
cronaca) la fa la lettura dei titoli, secondo ISTRUZIONI_INVERSO.md.
"""
import collections, json, os, re, sys, unicodedata

NOMI = {"abitarearoma": "Abitare a Roma", "dire": "Dire", "vignaclarablog": "VignaClaraBlog",
        "iltempo": "Il Tempo", "romadailynews": "Roma Daily News", "ilfaroonline": "Il Faro Online"}

PAROLE = (
    "arrest|ferma|fermat|fermo |denunc|rapin|furt|ladr|scipp|aggre|accoltell|coltell|picchia|pestag|"
    "violenz|molest|stupr|abus|droga|spacc|cocaina|hashish|marijuana|crack|sequestr|incident|investit|"
    "schiant|scontr|travolt|mort|muore|morire|decess|ferit|incendi|fiamme|rogo|crollo|crolla|evacua|"
    "polizia|poliziott|carabinier|vigili del fuoco|pompier|vigili|polizia locale|truff|estors|usur|"
    "omicid|uccis|uccide|cadavere|corpo senza vita|suicid|annega|malore|soccors|blitz|controlli|sgomber|"
    "occupa|sigill|sanzion|multat|multe|pistol|arma|armi|bomba|ordigno|esplos|minacc|stalking|maltratt|"
    "evas|latitant|baby gang|rissa|vandal|danneggi|imbratt|writer|spari|sparator|colpi di|bracciante|"
    "caporal|borseggi|borsegg|refurtiva|ricettaz|aggredit|tentato|tentata|indagat|inchiesta|condann|"
    "processo|arrestat|denunciat|bloccat|fugge|fuga|inseguiment|questura|procura|gdf|"
    "guardia di finanza|finanza|nas |abusiv|degrado|allagament|voragine|albero cadut|alberi cadut|crollat"
)
KW = re.compile(rf"\b({PAROLE})")
SERVIZIO = re.compile(r"(traffico|meteo|almanacco|buon compleanno|oroscopo)")


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def keep(testata, r):
    """Vero se il titolo può essere cronaca romana: per sezione dove la testata la dà,
    altrimenti per parola chiave."""
    t = norm(r["titolo"])
    cats = set(r["categorie"])
    if testata == "abitarearoma":
        return bool(cats & {"cronaca", "sicurezza-e-ordine-pubblico"})
    if testata == "vignaclarablog":
        return "cronaca-di-roma-nord" in cats or bool(KW.search(t))
    if testata == "dire":
        return bool(cats & {"roma", "lazio"}) and ("cronaca" in cats or bool(KW.search(t)))
    if testata == "iltempo":
        return ("roma-capitale" in cats or "roma" in t) and bool(KW.search(t))
    if testata == "romadailynews":
        return not SERVIZIO.match(t) and bool(KW.search(t))
    if testata == "ilfaroonline":
        return bool(KW.search(t))
    return False


def main(base):
    d = os.path.join(base, "censimento")
    out = []
    for k, nome in NOMI.items():
        rows = json.load(open(f"{d}/{k}.json"))
        kept = [r for r in rows if keep(k, r)]
        print(k, len(rows), "->", len(kept))
        out += [{"testata": nome, "data": r["data"][:10], "titolo": r["titolo"], "link": r["link"]} for r in kept]
    out.sort(key=lambda r: (r["data"], r["testata"]))
    for i, r in enumerate(out, 1):
        r["sid"] = f"S{i:04d}"
    with open(f"{d}/candidati.json", "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print(len(out), dict(sorted(collections.Counter(r["data"][8:10] for r in out).items())))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")

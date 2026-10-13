"""Registro delle fonti degli eventi: unione, doppioni, canale di lettura, pagine scoperte.

Uso: registro.py RISOLTI.json [VERIFICHE.json] MATRICE.csv USCITA_DIR

RISOLTI.json è {"fonti": [...], "pagine": [...]}: «fonti» sono luoghi e organizzatori ricavati
dai titoli di RomaToday e dalle schede del Comune; «pagine» sono le pagine Facebook curate
dall'owner. Una fonte e una pagina con lo stesso indirizzo Facebook diventano una riga sola;
due fonti con lo stesso dominio o lo stesso nome normalizzato anche. Il canale di lettura è il
sito se il robots.txt lo ammette e la pagina risponde, altrimenti la pagina Facebook (estrazione
con un servizio terzo su URL scelti da una persona, DEC-102); un sito che esclude gli agenti AI o
risponde 401/403 a un user agent dichiarato è chiuso, e un blocco non si aggira. MATRICE.csv è la tabella di
giugno (soglia Eventi per pagina). Scrive USCITA_DIR/registro.json e registro.csv.
"""
import csv, io, json, re, sys, unicodedata, urllib.parse

ORDINE = {"tenere": 0, "da_verificare": 1, "sospeso_DEC001": 2, "scartare": 3}
CAMPI = ["chiave", "decisione", "nome", "tipo", "zona_qn", "municipio", "pagina_sotto_soglia", "canale",
         "formato", "robots", "sito", "agenda_url", "facebook", "instagram", "indirizzo", "origine",
         "eventi_visti", "post_nel_periodo", "eventi_campione", "certezza", "motivo"]


def norm_nome(s):
    s = unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()
    s = re.sub(r"\b(roma|di|del|della|dei|degli|delle|il|lo|la|i|gli|le|l|al|alla|the|teatro|museo|biblioteca)\b", " ", s)
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", s).split())


def norm_url(u):
    u = (u or "").strip()
    if not u.startswith("http"):
        return ""
    p = urllib.parse.urlsplit(u)
    host = (p.hostname or "").removeprefix("www.").removeprefix("m.")
    return host + p.path.rstrip("/").lower()


def dominio(u):
    h = (urllib.parse.urlsplit(u).hostname or "") if (u or "").startswith("http") else ""
    return h.removeprefix("www.")


def canale(r):
    if r.get("robots") == "ammesso" and r.get("http") == 200:
        return "sito"
    if r.get("facebook"):
        return "facebook"
    if r.get("robots") in ("esclude_agenti_ai", "vietato") or r.get("http") in (401, 403):
        return "sito_chiuso"
    if r.get("instagram"):
        return "solo_instagram"
    return "da_trovare" if r.get("sito") else "nessuno"


def unisci(risolti, verifiche, sotto_soglia):
    righe = []
    for f in risolti.get("fonti", []):
        righe.append({**f, "origine": "romatoday" if f["cid"].startswith("S") else "comune", "chiavi_origine": [f["cid"]],
                      "eventi_visti": f.get("eventi_visti", 1)})
    for p in risolti.get("pagine", []):
        righe.append({"cid": f"P{p['riga']:03d}", "nome": p["nome"], "tipo": p["tipo"], "zona_qn": p["zona_qn"],
                      "municipio": p["municipio"], "indirizzo": "", "sito": "", "agenda_url": "", "facebook": p["url"],
                      "instagram": "", "decisione": p["decisione"], "motivo": p["motivo"], "certezza": "media",
                      "post_nel_periodo": p["post_nel_periodo"], "eventi_campione": p["eventi_campione"],
                      "origine": "pagine_fb", "chiavi_origine": [f"P{p['riga']:03d}"], "eventi_visti": 0})
    unite, indice = [], {}
    for r in righe:
        chiavi = [k for k in (("fb", norm_url(r.get("facebook"))), ("dom", dominio(r.get("sito"))),
                              ("nome", norm_nome(r.get("nome") or ""))) if k[1] and k[1] not in ("facebook.com", "instagram.com")]
        dove = next((indice[k] for k in chiavi if k in indice), None)
        if dove is None:
            dove = len(unite)
            unite.append(dict(r))
        else:
            u = unite[dove]
            for k, v in r.items():
                if k == "chiavi_origine":
                    u[k] = u[k] + v
                elif k == "eventi_visti":
                    u[k] = u.get(k, 0) + v
                elif k == "origine" and v not in u[k]:
                    u[k] = u[k] + "+" + v
                elif not u.get(k) and v not in ("", None, -1):
                    u[k] = v
            if ORDINE.get(r["decisione"], 9) < ORDINE.get(u["decisione"], 9):
                u["decisione"], u["motivo"] = r["decisione"], r["motivo"]
        for k in chiavi:
            indice.setdefault(k, dove)
    for u in unite:
        u.update(verifiche.get(u["cid"], {}) if verifiche else {})
        u["formato"] = ",".join(u.get("formato") or []) if isinstance(u.get("formato"), list) else (u.get("formato") or "")
        u["canale"] = canale(u)
        u["pagina_sotto_soglia"] = "sì" if u.get("zona_qn") in sotto_soglia else ("no" if u.get("zona_qn") else "")
    unite.sort(key=lambda u: (ORDINE.get(u["decisione"], 9), u.get("zona_qn") or "~", u.get("nome") or ""))
    for i, u in enumerate(unite, 1):
        u["chiave"] = f"FE-{i:04d}"
    return unite


def sotto_soglia(matrice_csv):
    t = open(matrice_csv, encoding="utf-8-sig").read()
    return {r["slug"] for r in csv.DictReader(io.StringIO(t), delimiter=";") if r["Soglia Eventi >=10 (giugno + FB)"] != "sì"}


if __name__ == "__main__":
    args = sys.argv[1:]
    risolti = json.load(open(args[0]))
    verifiche = json.load(open(args[1])) if len(args) == 4 else {}
    unite = unisci(risolti, verifiche, sotto_soglia(args[-2]))
    json.dump(unite, open(args[-1] + "/registro.json", "w"), ensure_ascii=False, indent=1)
    with open(args[-1] + "/registro.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI, extrasaction="ignore")
        w.writeheader()
        w.writerows(unite)
    print(len(unite), "fonti nel registro")

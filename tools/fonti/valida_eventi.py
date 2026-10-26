#!/usr/bin/env python3
"""Quality checks on the events page data (eventi.json of the «Eventi dei quartieri» page).

Every published row is checked against rules grouped by family; a rule is either grave (the row
should not be published as it is) or a warning (counted, to be improved). The report gives counts
per rule and per channel; the list of failing rows goes to --out, outside the repository, because
rows carry event titles (DEC-022, DEC-109).

    python tools/fonti/valida_eventi.py --eventi /path/eventi.json [--oggi 2026-10-26] \
        [--orizzonte 90] [--out /path/fuori/report.json] [--severo]

Rules (codes in the report):
  grave   V-DATA-1 start missing or not a date      V-DATA-2 end before start
          V-DATA-3 event already over               V-GEO-1  page not a gazetteer page id
          V-GEO-2  municipio not I-XV               V-GEO-5  place online or outside the Comune
          V-LINK-1 link missing or not http(s)
          V-LINK-2 Roma Today link outside its channel (DEC-026)
          V-PRIV-1 email or phone number in a published field
          V-TIT-1  empty title
  avviso  V-DATA-4 start beyond the horizon         V-DATA-5 period longer than 31 days
          V-ORA-1  time not HH:MM, or 00:00         V-GEO-3  page and municipio disagree
          V-GEO-4  no page                          V-TIT-2  title is a sentence, not a name
          V-DUP-1  same title, day and page as an earlier row
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "wiki"))
from leggi_eventi_siti import inside_repo  # noqa: E402
from build_fonti_eventi import EMAIL_RX, PHONE_RX  # noqa: E402

GRAVI = ("V-DATA-1", "V-DATA-2", "V-DATA-3", "V-GEO-1", "V-GEO-2", "V-GEO-5", "V-LINK-1", "V-LINK-2", "V-PRIV-1", "V-TIT-1")
AVVISI = ("V-DATA-4", "V-DATA-5", "V-ORA-1", "V-GEO-3", "V-GEO-4", "V-TIT-2", "V-DUP-1")
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")
CITYNEWS = re.compile(r"(^|\.)(romatoday\.it|citynews\.it|today\.it)$", re.I)
GIORNI = r"luned[iì]|marted[iì]|mercoled[iì]|gioved[iì]|venerd[iì]|sabato|domenica"
# a title that reads as the opening of a post: an invitation, a date first, a cut, links or tags
FRASE = re.compile(
    r"vi aspettiamo|vi invitiamo|non mancate|siete tutti invitati|siete invitati|vi ricordiamo|partecipate|save the date|ci vediamo"
    r"|^\s*(?:" + GIORNI + r")\b|^\s*\d{1,2}\s+(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\b"
    r"|(?:\.\.\.|…)\s*$|https?://|www\.|#\w", re.I)
TITOLO_LUNGO = 90
# a place that is not a place in Rome: online, a postcode outside 001xx, a province code other than RM, a comune of the
# province without Roma, "<city>, <another region>, Italia"; streets named after cities are not places (T-VE-3)
ONLINE = re.compile(r"^\s*(?:(?:evento\s+)?on\s?line\b.*|(?:in |diretta )?streaming|webinar|zoom(?: meeting)?|google meet|(?:microsoft )?teams)\s*$", re.I)
COMUNI_PROVINCIA = re.compile(   # any case; Marino only capitalised, since «marino» is also an adjective
    r"(?<!Via )(?<!Viale )(?<!Piazza )(?<!Largo )(?<!Via di )(?<!San )(?<!del )\b(Albano Laziale|Albano|(?-i:Marino)|Frascati|Ciampino|Castel Gandolfo|Genzano|Ariccia"
    r"|Rocca di Papa|Rocca Priora|Grottaferrata|Monte Porzio|Monte Compatri|Fiumicino|Guidonia|Tivoli|Monterotondo|Pomezia|Ardea|Anzio"
    r"|Nettuno|Velletri|Ladispoli|Cerveteri|Bracciano|Mentana|Fonte Nuova|Zagarolo|Palestrina|Colleferro|Valmontone|Lariano|Nemi|Formello"
    r"|Sacrofano|Campagnano|Anguillara|Trevignano|Santa Marinella|Civitavecchia|Subiaco)\b", re.I)
SIGLA = re.compile(   # province codes other than RM, any case
    r"\((AG|AL|AN|AO|AP|AQ|AR|AT|AV|BA|BG|BI|BL|BN|BO|BR|BS|BT|BZ|CA|CB|CE|CH|CL|CN|CO|CR|CS|CT|CZ|EN|FC|FE|FG|FI|FM|FR|GE|GO|GR|IM|IS"
    r"|KR|LC|LE|LI|LO|LT|LU|MB|MC|ME|MI|MN|MO|MS|MT|NA|NO|NU|OR|PA|PC|PD|PE|PG|PI|PN|PO|PR|PT|PU|PV|PZ|RA|RC|RE|RG|RI|RN|RO|SA|SI|SO"
    r"|SP|SR|SS|SU|SV|TA|TE|TN|TO|TP|TR|TS|TV|UD|VA|VB|VC|VE|VI|VR|VT|VV)\)", re.I)
CAP = re.compile(r"(?<![\d.,])(\d{5})(?!\d)")
ALTRA_REGIONE = re.compile(
    r",\s*(?:Abruzzo|Basilicata|Calabria|Campania|Emilia[- ]Romagna|Friuli[- ]Venezia Giulia|Liguria|Lombardia|Lombardy|Marche|Molise"
    r"|Piemonte|Piedmont|Puglia|Apulia|Sardegna|Sardinia|Sicilia|Sicily|Toscana|Tuscany|Trentino[- ]Alto Adige|Umbria|Valle d'Aosta"
    r"|Aosta Valley|Veneto)\s*,\s*(?:Italy|Italia)\s*$", re.I)
ROMA = re.compile(r"\b(Roma|Rome)\b", re.I)


def luogo_fuori_roma(luogo, ind=None):
    """Why the place of an event is not in the Comune di Roma ("online", "CAP", "provincia", "comune"), or None."""
    parti = [str(x).strip() for x in (luogo, ind) if x and str(x).strip()]
    if any(ONLINE.search(x) for x in parti):
        return "online"
    testo = " ".join(parti)
    cap = CAP.findall(testo)
    if cap and not any("00100" <= c <= "00199" for c in cap):
        return "CAP"
    if SIGLA.search(testo):
        return "provincia"
    if any(ALTRA_REGIONE.search(x) for x in parti) or (COMUNI_PROVINCIA.search(testo) and not ROMA.search(testo)):
        return "comune"
    return None


def _date(s):
    try:
        return date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def _host(u):
    m = re.match(r"https?://([^/?#:]+)", str(u or ""))
    return m.group(1).lower() if m else ""


def _key(t):
    s = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)[:40]


def _emoji(t):
    return sum(1 for c in str(t or "") if unicodedata.category(c) == "So")


def titolo_frase(t):
    """True when the title reads as a sentence taken from a post rather than the name of the event."""
    t = str(t or "").strip()
    return len(t) > TITOLO_LUNGO or bool(FRASE.search(t)) or _emoji(t) >= 2


def check_row(e, oggi, orizzonte, zones):
    """Codes of the rules a row breaks."""
    out = []
    d1, d2 = _date(e.get("d1")), _date(e.get("d2")) if e.get("d2") else None
    if d1 is None:
        out.append("V-DATA-1")
    else:
        if d2 and d2 < d1:
            out.append("V-DATA-2")
        if max(d1, d2 or d1) < oggi:
            out.append("V-DATA-3")
        if d1 > oggi + timedelta(days=orizzonte):
            out.append("V-DATA-4")
        if d2 and (d2 - d1).days > 31:
            out.append("V-DATA-5")
    ora = e.get("ora")
    if ora and (not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", str(ora)) or ora == "00:00"):
        out.append("V-ORA-1")
    z, m = e.get("z"), e.get("m")
    if z and z not in zones:
        out.append("V-GEO-1")
    if m and m not in ROMAN:
        out.append("V-GEO-2")
    if z in zones and m in ROMAN:
        zz = zones[z]
        spans = [s.strip() for s in str(zz.get("spans_municipalities") or "").replace(";", ",").split(",") if s.strip()]
        if m != zz.get("primary_municipality") and m not in spans:
            out.append("V-GEO-3")
    if not z:
        out.append("V-GEO-4")
    if luogo_fuori_roma(e.get("luogo"), e.get("ind")):
        out.append("V-GEO-5")
    url = e.get("url")
    if not url or not str(url).startswith(("http://", "https://")):
        out.append("V-LINK-1")
    elif CITYNEWS.search(_host(url)) and e.get("src") != "Roma Today":
        out.append("V-LINK-2")
    if any(EMAIL_RX.search(str(e.get(k) or "")) or PHONE_RX.search(str(e.get(k) or "")) for k in ("t", "luogo", "ind", "org")):
        out.append("V-PRIV-1")
    if not str(e.get("t") or "").strip():
        out.append("V-TIT-1")
    elif titolo_frase(e.get("t")):
        out.append("V-TIT-2")
    return out


def run(eventi, oggi, orizzonte, zones):
    """Report: counts per rule and per channel, and the failing rows by index."""
    per_regola, per_canale = Counter(), defaultdict(Counter)
    righe, visti = [], set()
    for i, e in enumerate(eventi):
        codes = check_row(e, oggi, orizzonte, zones)
        k = (_key(e.get("t")), str(e.get("d1"))[:10], e.get("z"))
        if k[0] and k in visti:
            codes.append("V-DUP-1")
        visti.add(k)
        canale = e.get("src") or "senza canale"
        per_canale[canale]["righe"] += 1
        for c in codes:
            per_regola[c] += 1
            per_canale[canale][c] += 1
        if codes:
            righe.append({"i": i, "regole": codes})
    gravi = sum(1 for r in righe if any(c in GRAVI for c in r["regole"]))
    return {"righe": len(eventi), "righe_con_errore_grave": gravi,
            "gravi": {c: per_regola[c] for c in GRAVI}, "avvisi": {c: per_regola[c] for c in AVVISI},
            "per_canale": {k: dict(v) for k, v in sorted(per_canale.items())}, "righe_segnalate": righe}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--eventi", required=True, help="eventi.json of the events page (outside the repository)")
    ap.add_argument("--gazetteer", default=os.path.join(HERE, "..", "..", "gazetteer", "gazetteer.json"))
    ap.add_argument("--oggi", help="reference day (default: the file's «oggi», else today)")
    ap.add_argument("--orizzonte", type=int, default=90, help="days ahead beyond which a start is a warning")
    ap.add_argument("--out", help="full report with the failing rows, outside the repository")
    ap.add_argument("--severo", action="store_true", help="exit 1 when a row breaks a grave rule")
    a = ap.parse_args(argv)
    if a.out and inside_repo(a.out):
        sys.exit("--out must point outside the repository: the failing rows carry event titles (DEC-022, DEC-109)")
    data = json.load(open(a.eventi, encoding="utf-8"))
    eventi = data["eventi"] if isinstance(data, dict) else data
    oggi = _date(a.oggi or (data.get("oggi") if isinstance(data, dict) else None)) or date.today()
    g = json.load(open(a.gazetteer, encoding="utf-8"))
    zones = {z["publication_zone_id"]: z for z in g["publication_zones"] if z.get("is_page")}
    rep = run(eventi, oggi, a.orizzonte, zones)
    if a.out:
        json.dump(rep, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    summary = {k: v for k, v in rep.items() if k != "righe_segnalate"}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if a.severo and rep["righe_con_errore_grave"]:
        sys.exit(1)
    return rep


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the Quartieri News wiki of event sources (fonti eventi).

Extends the context wiki of DEC-022 (schedario / diario / generated pages) with the
registry of the *sources of events*: the places that host them, the organisers that
promote them and the aggregators that list them. Three outputs, in this order of
authority:

1. fonti_eventi.json — one entry per source with a stable id, a canonical name,
   the spellings seen in each aggregator (aliases), its role(s), type, geography
   (official municipality, QN publication zone, coordinates), channels (website,
   Facebook, Instagram, culture.roma.it page), presence in each aggregator as
   counts, how often its events can be traced back to it, and the registry
   decision of 13 October 2026 when the source is in the registry.
2. aggregatori.md — one card per aggregator (culture.roma.it, Facebook events via
   Apify, Roma Today) and one for the direct reading of local sources: access
   rules, what was measured, overlap with the others. Numbers, not items.
3. INDEX.md, municipi/*.md — per-municipio renderings of 1. Generated; never
   edited by hand.

Inputs (a folder, nothing fetched from the network):
    eventi_unico.xlsx        the October 2026 events workbook (Drive / private preview):
                             tabs "Eventi unificati", "Facebook", "Comune di Roma (culture)",
                             "Romatoday → sorgente", "Fonti locali 13-31 ott", "Doppioni"
    registro_fonti.xlsx      the source registry of 13 October 2026
    culture_luoghi.json      optional: coordinates of the culture.roma.it venue pages
    associazioni_fonti.xlsx  optional: the census of Facebook pages of 24 October 2026 (tab "Pagine":
                             one row per page with verdict, channels, geography and activity counts)
    gazetteer/gazetteer.json the gazetteer (publication zones win on names)

Usage:
    python tools/wiki/build_fonti_eventi.py --input <folder> --out docs/wiki/fonti-eventi

Rules this build honours:
- DEC-109 / DEC-022: no event title, description or other source text enters the
  output. A source is a *soggetto* (a venue, an institution, an association, a
  company): its name, address and public channels are the registry, not source text.
  Event-level data stay in the workbook on Drive.
- DEC-105: no automatic anonymisation. Whoever hosts or organises events is a subject
  of this registry, a person or an organisation alike (a guide, a promoter, a director
  working under their own name). The one content reason applied: a Facebook personal
  profile is not a publication channel, so its URL is not written; the name stays
  (counted under `profili_personali_senza_url`).
- gazetteer.json wins: a zone is written only when it is a publication_zone_id of the
  gazetteer; the zone of an event (method 1 or 2 of the October workbook) is
  aggregated per source by majority, never invented.
- Deterministic: same inputs, same bytes out (ids are assigned in sorted order).
"""
import argparse
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
AGGREGATORI = {"facebook": "Facebook (eventi, via Apify)", "comune": "culture.roma.it (Roma Capitale)",
               "romatoday": "Roma Today", "fonte_locale": "lettura diretta (fonti locali)"}
LEGAL = re.compile(r"\b(aps|asd|a\.s\.d\.|srl|s\.r\.l\.|srls|ets|onlus|odv|aps-ets|soc\. coop\.|coop|società cooperativa|associazione culturale|associazione|fondazione)\b")
VIE = r"(?:Via|Viale|Vle|Piazza|Piazzale|P\.za|Largo|Corso|Lungotevere|Vicolo|Borgo|Circonvallazione|Passeggiata|Salita|Scalo|Strada|Lungomare|Rampa|Clivo|Vialetto|Piazzetta)"
VENUE_WORDS = ("teatro", "cinema", "biblioteca", "museo", "parco", "villa", "mercato", "scuola", "auditorium", "arena",
               "centro", "casa", "palazzo", "chiesa", "basilica", "galleria", "club", "libreria", "circolo", "sala",
               "spazio", "studio", "bar", "caffe", "cafe", "pub", "hotel", "ristorante", "osteria", "enoteca", "fattoria",
               "ippodromo", "stadio", "piscina", "giardino", "orto", "castello", "forte", "complesso", "accademia",
               "istituto", "fondazione", "associazione", "comitato", "municipio", "parrocchia", "oratorio", "live", "lab")
SOCIAL = re.compile(r"(facebook\.com|instagram\.com|tiktok\.com|youtube\.com|youtu\.be|x\.com|twitter\.com|linkedin\.com|t\.me|wa\.me|whatsapp|threads\.net|telegram)", re.I)
TICKET = re.compile(r"(vivaticket|ticketone|ticketmaster|dice\.fm|eventbrite|boxol|ticketsms|clappit|liveticket|ciaotickets|xceed|mailticket|tickettailor|ticketnation|i-ticket|oooh\.events|tiqets|getyourguide|musement|coopculture|museiincomuneroma)", re.I)
CENSIMENTO_CANDIDATI = ("rientra", "locale", "da valutare")   # verdicts of the census that enter the registry as candidates
FB_CATEGORIA_TIPO = (("theat", "teatro"), ("cinema", "cinema"), ("librar", "biblioteca"), ("museum", "museo"), ("art gallery", "galleria"),
                     ("music", "club_musica"), ("dance", "scuola"), ("school", "scuola"), ("educat", "scuola"), ("church", "parrocchia"),
                     ("religio", "parrocchia"), ("sport", "associazione"), ("nonprofit", "associazione"), ("non-profit", "associazione"),
                     ("community", "associazione"), ("charity", "associazione"), ("politic", "organizzazione_politica"),
                     ("local business", "locale"), ("bar", "locale"), ("restaurant", "locale"), ("event", "organizzatore"))


def tipo_from_facebook(categoria, name):
    c = str(categoria or "").lower()
    for needle, tipo in FB_CATEGORIA_TIPO:
        if needle in c:
            return tipo
    return None


AGGR_DOMAINS = re.compile(r"(romatoday|citynews|culture\.roma\.it|060608|comune\.roma\.it|google\.|goo\.gl|maps\.app|forms\.gle|jotform|linktr\.ee|bit\.ly|apify)", re.I)


# ----------------------------------------------------------------------------- helpers
def norm(s):
    """Identity key of a name: accents off, lower, punctuation out, legal forms and a
    trailing 'roma' out, spaces collapsed."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace("’", "'").replace("`", "'")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    s = LEGAL.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip(" '.-")
    s = re.sub(r"\b(di|in|a) roma$", "", s).strip()
    s = re.sub(r"\s+roma$", "", s).strip()
    return s


def is_web_url(s):
    return bool(s) and str(s).startswith(("http://", "https://"))


def domain(u):
    m = re.match(r"https?://(?:www\.)?([^/?#]+)", str(u or ""))
    return m.group(1).lower() if m else None


def personal_profile(url):
    """A Facebook personal profile (profile.php?id=…). A people/ URL is not treated as
    one: Facebook uses it for pages without a username too."""
    return bool(url) and "facebook.com/profile.php" in str(url)


def fb_page_key(url):
    """Identity key of a Facebook page URL (strong key, like fb-location and the registry key)."""
    m = re.match(r"https?://(?:www\.|m\.)?facebook\.com/([A-Za-z0-9._-]+)/?$", str(url or "").strip())
    if not m or m.group(1).lower() in ("events", "profile.php", "groups", "pages", "people", "share", "hashtag"):
        return None
    return "fb-page:" + m.group(1).lower()


def name_tokens(name):
    return {w for w in norm(name).split() if len(w) >= 4}


def site_matches_name(url, name):
    """An external link counts as the organiser's own site only when its domain shares a
    token with the organiser's name (externalLinks of a Facebook event are links in the
    description, not the organiser's site)."""
    d = domain(url) or ""
    d = re.sub(r"\.(it|com|org|net|eu|info|roma)$", "", d).replace("www.", "")
    return any(t in d.replace("-", "").replace(".", "") for t in name_tokens(name))


FIRST_NAMES = set("""
alessandro alessandra alessia alberto alice andrea angela angelo anna annamaria antonella antonio arianna aurora barbara beatrice
benedetta bruno camilla carla carlo carlotta caterina chiara claudia claudio cristina cristiano daniela daniele dario davide debora deborah
diego domenico edoardo elena eleonora elisa elisabetta emanuele emma enrico enzo fabio fabrizio federica federico filippo flavia flavio
francesca francesco franco gabriele gaia giacomo giada gianluca gianni giorgia giorgio giovanna giovanni giulia giuliano giulio giuseppe
greta ilaria irene jacopo laura leonardo livia lorenzo luca lucia luciano luigi luisa manuela marco margherita maria marina mario marta
martina massimiliano massimo matteo mattia maurizio mauro michela michele monica nicola nicoletta paola paolo patrizia pietro raffaele
riccardo roberta roberto rosa rossella sabrina salvatore samuele sara serena silvia simona simone sofia stefania stefano tommaso umberto
valentina valeria valerio vincenzo vittoria vittorio viola walter
""".split())


def looks_like_person(name):
    """Two or three words, the first a common Italian first name, no legal form, no venue
    word, no digits: the shape of a person's name (DEC-105: kept out of the registry).
    A brand of two capitalised words ("Barley Arts") is not a person."""
    n = str(name or "").strip()
    if not n or LEGAL.search(n.lower()) or any(ch.isdigit() for ch in n):
        return False
    words = n.replace("-", " ").split()
    if not 2 <= len(words) <= 3:
        return False
    if any(w.lower().strip("'") in VENUE_WORDS for w in words):
        return False
    first = unicodedata.normalize("NFKD", words[0]).encode("ascii", "ignore").decode().lower().strip(".")
    return first in FIRST_NAMES and not n.isupper()


def clean_location_name(s):
    """A Facebook location name sometimes carries the address: keep the name only."""
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    s = re.split(r",\s*(?=" + VIE + r"\b)", s)[0]
    s = re.sub(r",?\s*\d{5}\s+Roma.*$", "", s)
    return s.strip(" ,")


def split_dove(s):
    """Roma Today 'Dove' card -> (venue name, street with number, town)."""
    s = re.sub(r"\s+", " ", str(s or "")).replace("Indirizzo non disponibile", " ").strip()
    m = re.search(r"\b(" + VIE + r"\s+.+)$", s)
    if not m:
        return (s.strip(" ,-") or None), None, "Roma"
    venue = s[: m.start()].strip(" ,-") or None
    rest = m.group(1)
    town = "Roma"
    mt = re.search(r",\s*\d+[/A-Za-z]*\s+([A-ZÀ-Ü][\w'’ ]{2,30})$", rest)
    if mt and mt.group(1).strip().lower() != "roma":
        town = mt.group(1).strip()
        rest = rest[: mt.start(1)].strip(" ,")
    rest = re.sub(r"\s+Roma\s*$", "", rest)
    return venue, rest.strip(" ,"), town


def cell(ws_rows, header, row, key):
    return row[header.index(key)] if key in header else None


def read_sheet(wb, name):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c) if c is not None else "" for c in rows[0]]
    return header, rows[1:]


# ----------------------------------------------------------------------------- registry of sources
class Registry:
    def __init__(self, zones):
        self.entries = {}        # key -> record
        self.keys = {}           # any alias key -> canonical key
        self.zones = zones

    def get(self, name, extra_keys=(), ruolo=None, tipo=None, aggregatore=None):
        n = norm(name)
        if not n or n in ("roma", "n d", "nd"):
            return None
        k = self.keys.get(n)
        for ek in extra_keys:
            if ek and ek in self.keys:
                k = self.keys[ek]
                break
        if k is None:
            k = n
            self.keys[n] = k
            self.entries[k] = {"nome": str(name).strip(), "alias": [], "ruoli": set(), "tipi": Counter(), "chiavi": set(),
                               "canali": {"sito": Counter(), "sito_eventi": Counter(), "facebook": Counter(), "instagram": Counter(), "biglietteria": Counter(), "culture_luogo": None},
                               "indirizzi": Counter(), "municipi": Counter(), "zone": Counter(), "punti": [], "citta": Counter(),
                               "eventi": Counter(), "rintracciabili": Counter(), "registro": None, "fonte_locale": None, "censimento": None, "aggregatori": set(), "pagine_lette": Counter()}
        rec = self.entries[k]
        self.keys.setdefault(n, k)
        for ek in extra_keys:
            if ek:
                self.keys.setdefault(ek, k)
                rec["chiavi"].add(ek)
        nm = str(name).strip()
        if nm != rec["nome"] and nm not in rec["alias"] and norm(nm) == n:
            rec["alias"].append(nm)
        elif nm != rec["nome"] and nm not in rec["alias"] and norm(nm) != norm(rec["nome"]):
            rec["alias"].append(nm)
        if ruolo:
            rec["ruoli"].add(ruolo)
        if tipo:
            rec["tipi"][str(tipo)] += 1
        if aggregatore:
            rec["aggregatori"].add(aggregatore)
        return k

    def channel(self, k, kind, url, keep_path=False):
        """Record a channel. A website is kept as its root (scheme + host): the page to
        check for new events is the site, not the page of one event; keep_path keeps
        the full URL (registry links, pages read at the source)."""
        if not k or not url or not is_web_url(url):
            return
        url = str(url).strip()
        if kind == "sito" and (SOCIAL.search(url) or TICKET.search(url) or AGGR_DOMAINS.search(url)):
            return
        if kind == "sito" and not keep_path:
            d = domain(url)
            if not d:
                return
            url = "https://" + d
        if kind == "facebook" and personal_profile(url):
            return   # a private profile is not a publication channel (same rule for every source)
        if kind in ("facebook", "instagram"):
            url = re.sub(r"[?#].*$", "", url).rstrip("/")
        if kind == "facebook":
            fk = fb_page_key(url)
            if fk:   # the same Facebook page seen later (registry, census) is the same source
                self.keys.setdefault(fk, k)
                self.entries[k]["chiavi"].add(fk)
        self.entries[k]["canali"][kind][url] += 1

    def geo(self, k, municipio=None, zona=None, lat=None, lon=None, indirizzo=None, citta=None):
        if not k:
            return
        rec = self.entries[k]
        if municipio:
            rec["municipi"][str(municipio)] += 1
        if zona and zona in self.zones:
            rec["zone"][zona] += 1
        if lat and lon:
            try:
                rec["punti"].append((float(lat), float(lon)))
            except (TypeError, ValueError):
                pass
        if indirizzo:
            rec["indirizzi"][str(indirizzo).strip()] += 1
        if citta:
            rec["citta"][str(citta).strip()] += 1

    def event(self, k, aggregatore, rintracciabile):
        if not k:
            return
        self.entries[k]["eventi"][aggregatore] += 1
        self.entries[k]["rintracciabili"][rintracciabile or "n.d."] += 1


def sig_tokens(name):
    """Significant tokens of a name for the merge proposals: no legal forms, no generic words."""
    stop = {"roma", "di", "del", "della", "dei", "degli", "delle", "il", "la", "le", "lo", "e", "ed", "a", "al", "in", "the", "of", "per", "con", "da", "dal",
            "italia", "italiana", "italiano", "lazio", "nazionale",
            "aps", "asd", "ets", "odv", "onlus", "srl", "srls", "snc", "sas", "spa", "ssd", "soc", "coop", "associazione", "culturale",
            "teatro", "centro", "museo", "galleria", "club", "circolo", "spazio", "casa", "fondazione", "comitato", "quartiere"}
    return {t for t in norm(name).split() if t not in stop and len(t) > 2}


def proposed_merges(entries):
    """Pairs of distinct entries that are probably the same source: a person decides, the
    build never merges them (README rule). Criteria, in order: same name after removing legal
    forms and generic words; one name's significant tokens inside the other's with at least
    two tokens; names within a small edit distance. Pairs with conflicting Municipi are skipped."""
    import difflib
    cands = []
    keyed = [(e, sig_tokens(e["nome"]), norm(e["nome"])) for e in entries if sig_tokens(e["nome"])]
    for i in range(len(keyed)):
        a, ta, na = keyed[i]
        for j in range(i + 1, len(keyed)):
            b, tb, nb = keyed[j]
            if a["municipio"] and b["municipio"] and a["municipio"] != b["municipio"]:
                continue
            if ta == tb:
                why = "stesso nome senza forme giuridiche e parole generiche"
            elif len(ta & tb) >= 2 and (ta <= tb or tb <= ta) and min(len(ta), len(tb)) / max(len(ta), len(tb)) >= 0.5:
                why = "un nome contiene l'altro"
            elif len(ta) >= 2 and len(tb) >= 2 and len(ta & tb) >= 2 and len(ta & tb) >= len(ta | tb) - 1 and difflib.SequenceMatcher(None, na, nb).ratio() >= 0.8:
                why = "nomi quasi uguali"
            elif abs(len(na) - len(nb)) <= 2 and len(na) >= 12 and difflib.SequenceMatcher(None, na, nb).ratio() >= 0.92:
                why = "grafie a distanza di un refuso"
            else:
                continue
            cands.append({"a": a["id"], "a_nome": a["nome"], "b": b["id"], "b_nome": b["nome"], "motivo": why,
                          "municipio": a["municipio"] or b["municipio"] or "", "ruoli": sorted(set(a["ruoli"]) | set(b["ruoli"]))})
    return sorted(cands, key=lambda c: (c["a"], c["b"]))


def load_gazetteer(path):
    g = json.load(open(path, encoding="utf-8"))
    return {z["publication_zone_id"]: z for z in g["publication_zones"]}


def build(input_dir, out_dir, gazetteer_path):
    import openpyxl  # declared in requirements.txt
    zones = load_gazetteer(gazetteer_path)
    reg = Registry(zones)
    wb = openpyxl.load_workbook(os.path.join(input_dir, "eventi_unico.xlsx"), read_only=True, data_only=True)

    # ---- unified events: geography and traceability per event url ----------------------------------
    uh, urows = read_sheet(wb, "Eventi unificati")
    geo_by_url = {}
    for r in urows:
        g = lambda key: cell(None, uh, r, key)
        url = g("url")
        zona = g("zona_qn") or g("zona_qn_metodo2")
        geo_by_url[url] = {"municipio": g("municipio_assegnato"), "zona": zona, "lat": g("lat"), "lon": g("lon"),
                           "rintracciabile": g("rintracciabile_alla_fonte"), "fuori_roma": str(g("geo_nota") or "").startswith("fuori")}
    dup_h, dup_rows = read_sheet(wb, "Doppioni") if "Doppioni" in wb.sheetnames else ([], [])

    # ---- Facebook: venues (location) and organisers --------------------------------------------------
    fh, frows = read_sheet(wb, "Facebook")
    profili_personali = [0]
    for r in frows:
        g = lambda key: cell(None, fh, r, key)
        geo = geo_by_url.get(g("url"), {})
        if str(g("isOnline")).lower() == "true":
            continue
        kv = None
        if g("location.name"):
            kv = reg.get(clean_location_name(g("location.name")), extra_keys=[f"fb-location:{g('location.id')}"] if g("location.id") else [], ruolo="luogo", aggregatore="facebook")
            reg.geo(kv, geo.get("municipio"), geo.get("zona"), g("location.latitude"), g("location.longitude"), g("location.streetAddress") or g("address"), g("location.city"))
            reg.event(kv, "facebook", geo.get("rintracciabile"))
            if g("location.url"):
                reg.channel(kv, "facebook", g("location.url"))
        names = str(g("organizators.name") or "").split("; ")
        urls = str(g("organizators.url") or "").split("; ")
        for i, nm in enumerate(names):
            nm = nm.strip()
            if not nm or nm == "None":
                continue
            u = urls[i].strip() if i < len(urls) else ""
            is_page = bool(re.match(r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9._-]+/?$", u or "")) and not personal_profile(u)
            ko = reg.get(nm, ruolo="organizzatore", aggregatore="facebook")
            if personal_profile(u):
                profili_personali[0] += 1   # the name stays (DEC-105); a private profile is not a publication channel, so no URL
                u = ""
            if ko == kv:
                reg.entries[ko]["ruoli"].add("organizzatore")
            else:
                reg.event(ko, "facebook", geo.get("rintracciabile"))
                reg.geo(ko, geo.get("municipio"), geo.get("zona"))
            if u and u != "None":
                reg.channel(ko, "facebook", u)
            for l in str(g("externalLinks") or "").split("; "):
                l = l.strip()
                if not l or l == "None":
                    continue
                if TICKET.search(l):
                    reg.channel(ko, "biglietteria", l)
                elif "instagram.com" in l and site_matches_name(l.replace("instagram.com/", "instagram.com/x."), nm) or ("instagram.com" in l and any(t in l.lower() for t in name_tokens(nm))):
                    reg.channel(ko, "instagram", l)
                elif not SOCIAL.search(l) and site_matches_name(l, nm):
                    reg.channel(ko, "sito", l)
        if g("ticketsInfo.buyUrl") and kv:
            reg.channel(kv, "biglietteria", g("ticketsInfo.buyUrl"))

    # ---- culture.roma.it: venues and organisers ------------------------------------------------------
    luoghi = {}
    lp = os.path.join(input_dir, "culture_luoghi.json")
    if os.path.exists(lp):
        luoghi = json.load(open(lp, encoding="utf-8"))
    ch, crows = read_sheet(wb, "Comune di Roma (culture)")
    for r in crows:
        g = lambda key: cell(None, ch, r, key)
        geo = geo_by_url.get(g("url"), {})
        kv = None
        if g("venue"):
            kv = reg.get(g("venue"), extra_keys=[f"culture:{g('venueUrl')}"] if g("venueUrl") else [], ruolo="luogo", aggregatore="comune")
            L = luoghi.get(g("venueUrl") or "", {})
            reg.geo(kv, geo.get("municipio"), geo.get("zona"), L.get("lat") or geo.get("lat"), L.get("lon") or geo.get("lon"), g("address") or L.get("indirizzo"), "Roma")
            reg.event(kv, "comune", geo.get("rintracciabile"))
            if g("venueUrl"):
                reg.entries[kv]["canali"]["culture_luogo"] = g("venueUrl")
        ko = None
        if g("aCuraDi"):
            ko = reg.get(g("aCuraDi"), ruolo="organizzatore", aggregatore="comune")
            if ko != kv:
                reg.event(ko, "comune", geo.get("rintracciabile"))
                reg.geo(ko, geo.get("municipio"), geo.get("zona"))
        for who in (ko or kv, kv):
            if not who:
                continue
            for l in str(g("contattiLinks") or "").split(" | "):
                if l.strip():
                    reg.channel(who, "sito", l.strip())
            for l in str(g("social") or "").split(" | "):
                l = l.strip()
                if "facebook.com" in l:
                    reg.channel(who, "facebook", l)
                elif "instagram.com" in l:
                    reg.channel(who, "instagram", l)
            for l in str(g("ingressoLinks") or "").split(" | "):
                if l.strip() and TICKET.search(l):
                    reg.channel(who, "biglietteria", l.strip())
            break

    # ---- Roma Today: venues from the card, declared promoters, websites ------------------------------
    rh, rrows = read_sheet(wb, "Romatoday → sorgente")
    for r in rrows:
        g = lambda key: cell(None, rh, r, key)
        geo = geo_by_url.get(g("link_ufficiale")) or geo_by_url.get(g("url_romatoday")) or {}
        venue, street, town = split_dove(g("dove"))
        kv = None
        if venue and not re.search(r"\b(vari|varie|diffus|location)\b", venue, re.I):
            kv = reg.get(venue, ruolo="luogo", aggregatore="romatoday")
            reg.geo(kv, geo.get("municipio"), geo.get("zona"), geo.get("lat"), geo.get("lon"), street, town)
            reg.event(kv, "romatoday", geo.get("rintracciabile"))
        ko = None
        if g("promotore_dichiarato"):
            ko = reg.get(g("promotore_dichiarato"), ruolo="organizzatore", aggregatore="romatoday")
            if ko != kv:
                reg.event(ko, "romatoday", geo.get("rintracciabile"))
                reg.geo(ko, geo.get("municipio"), geo.get("zona"))
        who = ko or kv
        if who:
            sw = g("sito_web")
            if sw and "://" not in str(sw):
                sw = "https://" + str(sw).strip()
            if g("tipo_link") in ("pagina evento sul sito ufficiale", "sito ufficiale (home o pagina indicata)") and g("link_ufficiale"):
                reg.channel(who, "sito", "https://" + domain(g("link_ufficiale")) if domain(g("link_ufficiale")) else None)
            elif sw:
                reg.channel(who, "sito", sw)
            if g("link_facebook"):
                reg.channel(who, "facebook", g("link_facebook"))
            if g("link_instagram"):
                reg.channel(who, "instagram", g("link_instagram"))
            if g("link_biglietti"):
                reg.channel(who, "biglietteria", g("link_biglietti"))

    # ---- direct reading of local sources (13-31 October 2026) ---------------------------------------
    lh, lrows = read_sheet(wb, "Fonti locali 13-31 ott")
    for r in lrows:
        g = lambda key: cell(None, lh, r, key)
        if not g("nome_fonte"):
            continue
        k = reg.get(g("nome_fonte"), extra_keys=[f"registro:{g('fonte')}"] if g("fonte") else [], ruolo="luogo", tipo=g("tipo_fonte"), aggregatore="fonte_locale")
        reg.geo(k, g("municipio"), g("zona_qn"))
        reg.event(k, "fonte_locale", "letto alla fonte (sito del luogo)")
        if g("pagina_letta") and is_web_url(g("pagina_letta")):
            reg.entries[k]["pagine_lette"][g("pagina_letta").strip()] += 1
            d = domain(g("pagina_letta"))
            if d and not SOCIAL.search(d):
                reg.channel(k, "sito", "https://" + d)
        if reg.entries[k]["fonte_locale"] is None:
            reg.entries[k]["fonte_locale"] = {"codice": g("fonte"), "eventi_letti": 0, "anche_su_romatoday": 0}
        fl = reg.entries[k]["fonte_locale"]
        fl["eventi_letti"] += 1
        fl["anche_su_romatoday"] += 1 if str(g("anche_su_romatoday")).lower() in ("sì", "si", "true") else 0

    # ---- registry of 13 October 2026 ----------------------------------------------------------------
    rp = os.path.join(input_dir, "registro_fonti.xlsx")
    if os.path.exists(rp):
        rwb = openpyxl.load_workbook(rp, read_only=True, data_only=True)
        gh, grows = read_sheet(rwb, rwb.sheetnames[0])
        for r in grows:
            g = lambda key: cell(None, gh, r, key)
            if not g("nome"):
                continue
            k = reg.get(g("nome"), extra_keys=[f"registro:{g('chiave')}"], tipo=g("tipo"))
            if not k:   # a registry row whose name is empty or just "Roma" is not a source
                continue
            reg.entries[k]["registro"] = {"chiave": g("chiave"), "decisione": g("decisione"), "canale": g("canale"), "origine": g("origine"),
                                          "tipo": g("tipo"), "zona_qn": g("zona_qn"), "municipio": g("municipio"), "sotto_soglia": g("sotto_soglia")}
            reg.geo(k, g("municipio"), g("zona_qn"))
            if is_web_url(g("link")):
                reg.channel(k, "sito", g("link"), keep_path=True)
            if is_web_url(g("facebook")):
                reg.channel(k, "facebook", g("facebook"))
            if is_web_url(g("instagram")):
                reg.channel(k, "instagram", g("instagram"))

    # ---- census of Facebook pages, 24 October 2026 --------------------------------------------------
    # One row per page read with Apify (pages scraper, upcoming events) and on its website. Pages whose
    # verdict starts with "rientra", "locale" or "da valutare" enter the registry as candidates (the owner
    # decides; the verdict is carried, never turned into a registry decision). Dormant and discarded pages
    # are counted only. No page text (intro) is written.
    censimento_conteggi = Counter()
    cp = os.path.join(input_dir, "associazioni_fonti.xlsx")
    if os.path.exists(cp):
        cwb = openpyxl.load_workbook(cp, read_only=True, data_only=True)
        ch_, crows = read_sheet(cwb, "Pagine")
        for r in crows:
            g = lambda key: cell(None, ch_, r, key)
            verdetto = str(g("verdetto") or "")
            censimento_conteggi[verdetto or "n.d."] += 1
            if not g("nome") or g("stato") != "letta" or not verdetto.startswith(CENSIMENTO_CANDIDATI):
                continue
            fb = re.sub(r"^https?://(www\.|m\.)?facebook\.com/", "https://www.facebook.com/", str(g("url_pagina") or "").strip())
            k = reg.get(g("nome"), extra_keys=[fb_page_key(fb)], ruolo="organizzatore", tipo=tipo_from_facebook(g("categoria_facebook"), g("nome")))
            if not k:
                continue
            reg.entries[k]["censimento"] = {
                "verdetto": verdetto, "motivo": g("motivo"), "categoria_facebook": g("categoria_facebook"),
                "eventi_futuri_facebook": int(g("fb_eventi_in_roma") or 0), "sito_date_future": int(g("sito_date_future") or 0),
                "sito_date_ultimi_6_mesi": int(g("sito_date_ultimi_6_mesi") or 0), "nel_registro_13_ott": g("nel_registro_13_ott")}
            reg.geo(k, g("municipio"), g("zona_qn"), g("lat"), g("lon"), g("indirizzo"))
            reg.channel(k, "facebook", fb)
            if is_web_url(g("sito")):
                reg.channel(k, "sito", g("sito"))
            if is_web_url(g("sito_pagina_eventi")):
                reg.channel(k, "sito_eventi", g("sito_pagina_eventi"), keep_path=True)

    # ---- finalise entries ----------------------------------------------------------------------------
    def finalize(k, rec, seq):
        tipo = rec["tipi"].most_common(1)[0][0] if rec["tipi"] else guess_tipo(rec["nome"])
        mun = rec["municipi"].most_common(1)[0][0] if rec["municipi"] else ""
        mun = re.sub(r"^Municipio\s+", "", str(mun))
        zona = rec["zone"].most_common(1)[0][0] if rec["zone"] else None
        pts = rec["punti"]
        lat = round(sum(p[0] for p in pts) / len(pts), 5) if pts else None
        lon = round(sum(p[1] for p in pts) / len(pts), 5) if pts else None
        tot = sum(rec["eventi"].values())
        diretti = sum(v for c, v in rec["rintracciabili"].items() if c and (c.startswith("sito") or c.startswith("letto")))
        chiave_reg = rec["registro"]["chiave"] if rec["registro"] else None
        ident = f"S-{chiave_reg}" if chiave_reg else f"S-EV-{seq:04d}"
        citta = rec["citta"].most_common(1)[0][0] if rec["citta"] else None
        dove = []
        for u, _ in rec["pagine_lette"].most_common(1):
            dove.append({"url": u, "cosa": "pagina letta alla fonte (calendario)"})
        if rec["canali"]["culture_luogo"]:
            dove.append({"url": rec["canali"]["culture_luogo"], "cosa": "pagina del luogo su culture.roma.it"})
        for u, _ in rec["canali"]["sito_eventi"].most_common(1):
            if not any(d["url"] == u for d in dove):
                dove.append({"url": u, "cosa": "pagina eventi del sito"})
        for u, _ in rec["canali"]["sito"].most_common(1):
            if not any(d["url"] == u for d in dove):
                dove.append({"url": u, "cosa": "sito"})
        for u, _ in [x for x in rec["canali"]["facebook"].most_common(1) if not personal_profile(x[0])]:
            m = re.match(r"https?://(?:www\.)?facebook\.com/([A-Za-z0-9._-]+)/?$", u)
            ok = bool(m) and m.group(1).lower() not in ("events", "profile.php", "groups", "pages", "people", "share", "hashtag")
            dove.append({"url": f"https://www.facebook.com/{m.group(1)}/events" if ok else u, "cosa": "eventi della pagina Facebook" if ok else "pagina Facebook"})
        for u, _ in rec["canali"]["instagram"].most_common(1):
            if re.search(r"instagram\.com/(p|reel|explore|date|accounts)(/|$)", u):
                continue
            dove.append({"url": u, "cosa": "Instagram"})
        return {
            "id": ident, "nome": rec["nome"], "alias": sorted(set(rec["alias"])),
            "ruoli": sorted(rec["ruoli"]) or ["soggetto"], "tipo": tipo,
            "municipio": mun if mun in ROMAN else "", "zona": zona, "zona_nome": zones[zona]["name_display"] if zona else None,
            "indirizzo": rec["indirizzi"].most_common(1)[0][0] if rec["indirizzi"] else None,
            "citta": citta if citta and citta != "Roma" else ("Roma" if mun in ROMAN or citta == "Roma" else citta),
            "lat": lat, "lon": lon,
            "canali": {"sito": [u for u, _ in rec["canali"]["sito"].most_common(2)],
                       "facebook": [u for u, _ in rec["canali"]["facebook"].most_common(1)],
                       "instagram": [u for u, _ in rec["canali"]["instagram"].most_common(1)],
                       "biglietteria": [domain(u) for u, _ in rec["canali"]["biglietteria"].most_common(1)],
                       "culture_luogo": rec["canali"]["culture_luogo"]},
            "dove_cercare": dove,
            "aggregatori": sorted(rec["aggregatori"]),
            "eventi_ott_2026": dict(sorted(rec["eventi"].items())), "eventi_totali": tot,
            "rintracciabilita": {"eventi_con_fonte_diretta": diretti, "quota": round(diretti / tot, 2) if tot else None},
            "registro": rec["registro"], "fonte_locale": rec["fonte_locale"], "censimento": rec["censimento"],
            "chiavi": sorted(rec["chiavi"]),
        }

    def guess_tipo(name):
        n = norm(name)
        for w in ("teatro", "cinema", "biblioteca", "museo", "galleria", "libreria", "parco", "villa", "mercato", "scuola",
                  "auditorium", "club", "circolo", "chiesa", "basilica", "parrocchia", "palazzo", "hotel", "ristorante",
                  "associazione", "comitato", "fondazione", "municipio", "accademia", "istituto", "centro"):
            if re.search(r"\b" + w + r"\b", n):
                return {"club": "club_musica", "circolo": "club_musica", "chiesa": "parrocchia", "basilica": "parrocchia",
                        "ristorante": "locale", "hotel": "locale", "villa": "parco", "galleria": "galleria"}.get(w, w)
        return "altro"

    ordered = sorted(reg.entries.items(), key=lambda kv: (kv[1]["nome"].lower(), kv[0]))
    seq = 0
    out_entries = []
    for k, rec in ordered:
        if not rec["registro"]:
            seq += 1
        out_entries.append(finalize(k, rec, seq))
    # drop entries that are neither in the registry nor carry any event (pure link noise)
    out_entries = [e for e in out_entries if e["registro"] or e["censimento"] or e["eventi_totali"] > 0]

    # ---- aggregator cards: numbers from the workbook ------------------------------------------------
    per_src = Counter(); traced = defaultdict(Counter); geo_ok = Counter(); fuori = Counter()
    for r in urows:
        g = lambda key: cell(None, uh, r, key)
        f = str(g("fonte") or "")
        src = "fonte_locale" if f.startswith("Fonte locale") else "romatoday" if f.startswith("Romatoday") else "comune" if f.startswith("Comune") else "facebook"
        per_src[src] += 1
        traced[src][g("rintracciabile_alla_fonte") or "n.d."] += 1
        if g("zona_qn") or g("zona_qn_metodo2"):
            geo_ok[src] += 1
        if str(g("geo_nota") or "").startswith("fuori"):
            fuori[src] += 1
    overlap = Counter()
    if dup_rows:
        gi = dup_h.index("gruppo"); ti = dup_h.index("tipo"); fi = dup_h.index("fonti")
        seen = set()
        for r in dup_rows:
            if r[gi] in seen:
                continue
            seen.add(r[gi])
            overlap[(r[ti], r[fi])] += 1

    sched = {
        "versione": "2026-10.1",
        "fonte_dati": "eventi_unico.xlsx (ottobre 2026: Facebook via Apify, culture.roma.it, Roma Today, lettura diretta 13-31 ottobre) + registro fonti 13 ott 2026"
                      + (" + censimento pagine Facebook 24 ott 2026" if censimento_conteggi else ""),
        "regole": ["DEC-022: nessun testo delle fonti; qui stanno soggetti, canali e conteggi",
                   "DEC-105: nessuna anonimizzazione; chi organizza o ospita eventi è un soggetto, persona o organizzazione che sia; di un profilo personale Facebook non si scrive l'URL",
                   "gazetteer vince: la zona è scritta solo se è una publication_zone_id"],
        "profili_personali_senza_url": profili_personali[0],
        "fonti": out_entries,
        "aggregatori": {s: {"nome": AGGREGATORI[s], "eventi_ott_2026": per_src[s], "con_pagina_qn": geo_ok[s], "fuori_roma": fuori[s],
                            "rintracciabilita": dict(traced[s].most_common())} for s in AGGREGATORI},
        "doppioni": {f"{t} · {f}": n for (t, f), n in sorted(overlap.items())},
        "censimento_pagine": dict(sorted(censimento_conteggi.items())),
        "fusioni_proposte": proposed_merges(out_entries),
    }
    os.makedirs(out_dir, exist_ok=True)
    json.dump(sched, open(os.path.join(out_dir, "fonti_eventi.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    write_pages(sched, out_dir, zones)
    return sched


# ----------------------------------------------------------------------------- pages
def md_link(u, label=None):
    return f"[{label or domain(u) or u}]({u})" if is_web_url(u) else (label or u or "")


def canali_md(e):
    c = e["canali"]
    parts = []
    if c["sito"]:
        parts.append(md_link(c["sito"][0], "sito"))
    if c["facebook"]:
        parts.append(md_link(c["facebook"][0], "Facebook"))
    if c["instagram"]:
        parts.append(md_link(c["instagram"][0], "Instagram"))
    if c["culture_luogo"]:
        parts.append(md_link(c["culture_luogo"], "culture.roma.it"))
    if c["biglietteria"]:
        parts.append(f"biglietti: {c['biglietteria'][0]}")
    return " · ".join(parts) or "—"


def dove_md(e):
    return " · ".join(md_link(d["url"], d["cosa"]) for d in e["dove_cercare"][:3]) or "—"


def eventi_md(e):
    ab = {"facebook": "FB", "comune": "CR", "romatoday": "RT", "fonte_locale": "FL"}
    return " ".join(f"{ab[s]} {n}" for s, n in e["eventi_ott_2026"].items()) or "—"


def write_pages(sched, out_dir, zones):
    fonti = sched["fonti"]
    pages_dir = os.path.join(out_dir, "municipi")
    os.makedirs(pages_dir, exist_ok=True)
    by_mun = defaultdict(list)
    for e in fonti:
        by_mun[e["municipio"] or "senza municipio"].append(e)
    reg_n = sum(1 for e in fonti if e["registro"])
    index = ["# Wiki delle fonti eventi — ottobre 2026 (generato)", "",
             "Pagine generate da `fonti_eventi.json`; non modificare a mano, rigenerare con `tools/wiki/build_fonti_eventi.py`. "
             "Una *fonte* è un luogo che ospita eventi, un organizzatore che li promuove o un aggregatore che li elenca. "
             "Qui stanno nomi, canali e conteggi; gli eventi restano nel foglio su Drive (DEC-022).", "",
             f"Fonti: {len(fonti)} · nel registro del 13 ottobre: {reg_n} · luoghi: {sum(1 for e in fonti if 'luogo' in e['ruoli'])} · "
             f"organizzatori: {sum(1 for e in fonti if 'organizzatore' in e['ruoli'])} · con sito web: {sum(1 for e in fonti if e['canali']['sito'])} · "
             f"con pagina QN: {sum(1 for e in fonti if e['zona'])}"
             + (f" · candidate dal censimento pagine del 24 ottobre: {sum(1 for e in fonti if e['censimento'])} (vedi [censimento-pagine.md](censimento-pagine.md))" if sched.get("censimento_pagine") else ""), "",
             "Aggregatori: vedi [aggregatori.md](aggregatori.md).", "",
             "| Municipio | fonti | luoghi | organizzatori | eventi ott 2026 | con sito | con pagina QN |", "|---|---|---|---|---|---|---|"]
    for m in ROMAN + ["senza municipio"]:
        es = by_mun.get(m, [])
        if not es and m == "senza municipio":
            continue
        label = f"[{m}](municipi/{m}.md)" if m in ROMAN else "[senza municipio](municipi/senza-municipio.md)"
        index.append(f"| {label} | {len(es)} | {sum(1 for e in es if 'luogo' in e['ruoli'])} | {sum(1 for e in es if 'organizzatore' in e['ruoli'])} | "
                     f"{sum(e['eventi_totali'] for e in es)} | {sum(1 for e in es if e['canali']['sito'])} | {sum(1 for e in es if e['zona'])} |")
        out = [f"# Municipio {m} — fonti eventi (ottobre 2026)" if m in ROMAN else "# Fonti senza municipio assegnato — fonti eventi (ottobre 2026)", "",
               f"Fonti: {len(es)} · eventi nel mese: {sum(e['eventi_totali'] for e in es)}. Sigle degli aggregatori: FB Facebook, CR culture.roma.it, RT Roma Today, FL lettura diretta. "
               "La *quota diretta* è la parte degli eventi della fonte che rimanda al sito dell'organizzatore o è stata letta lì.", ""]
        for zona_id, group in sorted(group_by_zone(es, zones).items(), key=lambda kv: (kv[0] == "—", zones.get(kv[0], {}).get("name_display", kv[0]))):
            title = zones[zona_id]["name_display"] if zona_id in zones else "Senza pagina QN"
            out += [f"## {title}" + (f" `{zona_id}`" if zona_id in zones else ""), "",
                    "| fonte | dove cercare | ruolo | tipo | eventi | quota diretta | registro | id |", "|---|---|---|---|---|---|---|---|"]
            for e in sorted(group, key=lambda e: (-e["eventi_totali"], e["nome"].lower())):
                reg_s = f"{e['registro']['decisione']} ({e['registro']['canale'] or '—'})" if e["registro"] else f"censimento: {e['censimento']['verdetto']}" if e["censimento"] else "—"
                q = e["rintracciabilita"]["quota"]
                out.append(f"| {e['nome']} | {dove_md(e)} | {', '.join(e['ruoli'])} | {e['tipo']} | {eventi_md(e)} | "
                           f"{'—' if q is None else f'{int(q*100)}%'} | {reg_s} | `{e['id']}` |")
            out.append("")
        name = f"{m}.md" if m in ROMAN else "senza-municipio.md"
        open(os.path.join(pages_dir, name), "w", encoding="utf-8").write("\n".join(out) + "\n")
    # the city-wide shortlist: where to look first
    top = sorted((e for e in fonti if e["dove_cercare"]), key=lambda e: (-e["eventi_totali"], e["nome"].lower()))[:60]
    index += ["", "## Dove cercare per primi: le 60 fonti più produttive con un indirizzo da controllare", "",
              "| fonte | dove cercare | municipio | pagina QN | eventi ott 2026 |", "|---|---|---|---|---|"]
    for e in top:
        index.append(f"| {e['nome']} | {dove_md(e)} | {e['municipio'] or '—'} | {e['zona_nome'] or '—'} | {eventi_md(e)} |")
    open(os.path.join(out_dir, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    # one view per QN page: the sources to check for that page
    per = ["# Dove cercare nuovi eventi, pagina per pagina (generato)", "",
           "Per ogni pagina QN, le fonti che a ottobre 2026 hanno prodotto eventi in quella zona, con l'indirizzo da controllare. "
           "Ordine: per numero di eventi. Le fonti senza indirizzo da controllare sono in fondo a ogni gruppo.", ""]
    by_zone = defaultdict(list)
    for e in fonti:
        if e["zona"] in zones:
            by_zone[e["zona"]].append(e)
    for z in sorted(by_zone, key=lambda z: zones[z]["name_display"]):
        es = sorted(by_zone[z], key=lambda e: (not e["dove_cercare"], -e["eventi_totali"], e["nome"].lower()))
        per += [f"## {zones[z]['name_display']} `{z}` — Municipio {zones[z].get('primary_municipality','')}", "",
                "| fonte | dove cercare | ruolo | eventi ott 2026 |", "|---|---|---|---|"]
        for e in es:
            per.append(f"| {e['nome']} | {dove_md(e)} | {', '.join(e['ruoli'])} | {eventi_md(e)} |")
        per.append("")
    open(os.path.join(out_dir, "per-pagina-qn.md"), "w", encoding="utf-8").write("\n".join(per) + "\n")
    write_aggregatori(sched, out_dir)
    if sched.get("censimento_pagine"):
        write_censimento(sched, out_dir, zones)
    write_fusioni(sched, out_dir)


def write_fusioni(sched, out_dir):
    out = ["# Fusioni proposte fra voci dello schedario (generato)", "",
           "Coppie di voci che probabilmente sono la stessa fonte scritta in due modi. Il build non le fonde "
           "(regola: le fusioni dubbie le decide una persona); chi decide registra la fusione nel registro fonti "
           "con la chiave forte comune (URL Facebook, pagina del luogo su culture.roma.it) e il build la applica "
           "alla rigenerazione successiva. Coppie con Municipi diversi non sono proposte.", "",
           f"Coppie proposte: {len(sched['fusioni_proposte'])}", "", "| voce A | voce B | motivo | municipio | ruoli |", "|---|---|---|---|---|"]
    for c in sched["fusioni_proposte"]:
        out.append(f"| {c['a_nome']} `{c['a']}` | {c['b_nome']} `{c['b']}` | {c['motivo']} | {c['municipio'] or '—'} | {', '.join(c['ruoli'])} |")
    open(os.path.join(out_dir, "fusioni-proposte.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def write_censimento(sched, out_dir, zones):
    """Candidates from the census of Facebook pages (24 October 2026), grouped by verdict then
    municipality: what the owner has to decide on, with the address to check for each."""
    cand = [e for e in sched["fonti"] if e["censimento"]]
    out = ["# Censimento delle pagine Facebook di associazioni — 24 ottobre 2026 (generato)", "",
           "Pagine lette con Apify (dati di pagina, eventi futuri) e sul loro sito. Qui stanno le candidate: il verdetto è "
           "della lettura automatica, la decisione (tenere / scartare) spetta all'owner e si registra nel registro fonti, non qui. "
           "Le pagine dormienti o scartate sono solo contate.", "", "| verdetto | pagine |", "|---|---|"]
    for v, n in sorted(sched["censimento_pagine"].items(), key=lambda kv: -kv[1]):
        out.append(f"| {v} | {n} |")
    out.append("")
    by_v = defaultdict(list)
    for e in cand:
        by_v[e["censimento"]["verdetto"]].append(e)
    for v in sorted(by_v, key=lambda v: (not v.startswith("rientra"), v)):
        es = sorted(by_v[v], key=lambda e: (ROMAN.index(e["municipio"]) if e["municipio"] in ROMAN else 99, e["nome"].lower()))
        out += [f"## {v} ({len(es)})", "", "| fonte | municipio | pagina QN | dove cercare | eventi futuri FB | date future sul sito | nel registro | id |", "|---|---|---|---|---|---|---|---|"]
        for e in es:
            c = e["censimento"]
            out.append(f"| {e['nome']} | {e['municipio'] or '—'} | {e['zona_nome'] or '—'} | {dove_md(e)} | {c['eventi_futuri_facebook'] or '—'} | "
                       f"{c['sito_date_future'] or '—'} | {e['registro']['decisione'] if e['registro'] else (c['nel_registro_13_ott'] or '—')} | `{e['id']}` |")
        out.append("")
    open(os.path.join(out_dir, "censimento-pagine.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def group_by_zone(es, zones):
    g = defaultdict(list)
    for e in es:
        g[e["zona"] if e["zona"] in zones else "—"].append(e)
    return g


def write_aggregatori(sched, out_dir):
    a = sched["aggregatori"]
    def card(key, titolo, accesso, misura):
        x = a[key]
        rows = ["| misura | valore |", "|---|---|", f"| eventi letti (ottobre 2026) | {x['eventi_ott_2026']} |",
                f"| con pagina QN assegnata | {x['con_pagina_qn']} |", f"| fuori Roma | {x['fuori_roma']} |"]
        for k, v in x["rintracciabilita"].items():
            rows.append(f"| rintracciabilità: {k} | {v} |")
        return [f"## {titolo}", "", f"**Accesso.** {accesso}", "", f"**Cosa misura.** {misura}", ""] + rows + [""]
    out = ["# Aggregatori di eventi — schede (generato, ottobre 2026)", "",
           "Un aggregatore è una fonte che elenca eventi di altri. Le schede dicono come vi si accede, che cosa è stato misurato a ottobre 2026 "
           "e quanto gli eventi che pubblica siano rintracciabili alla fonte originaria. Numeri, non eventi: i dati per evento stanno nel foglio su Drive.", ""]
    out += card("comune", "culture.roma.it — agenda di Roma Capitale",
                "API WordPress pubblica (`wp-json/wp/v2/event_calendar`) più la pagina di ogni appuntamento; nessuna clausola di riuso trovata (da verificare, L11). "
                "Letta con `apify/cheerio-scraper` il 20 ottobre 2026: 6.222 appuntamenti pubblicati dal luglio 2025; nel foglio quelli con fine dal 1° ottobre 2026.",
                "Luogo, indirizzo, Municipio, organizzatore (a cura di), ingresso, contatti. È l'aggregatore con la rintracciabilità più alta: quasi ogni scheda rimanda al sito del luogo o dell'organizzatore.")
    out += card("facebook", "Facebook — eventi, via Apify",
                "Nessun accesso diretto dall'ambiente (DEC-102): gli URL degli eventi li raccoglie l'owner, l'Actor `apify/facebook-events-scraper` li legge "
                "(0,01 $ per evento; 584 URL il 23 ottobre 2026, 567 eventi, 17 bloccati o rimossi).",
                "Nome, date, luogo con coordinate, organizzatore con pagina, biglietti, partecipanti. Metà degli eventi ha come unico riferimento la pagina Facebook dell'organizzatore.")
    out += card("romatoday", "Roma Today (Citynews)",
                "Il robots.txt vieta scraping, text and data mining e usi per AI senza licenza scritta; nel repository è registrato come «nessun canale senza licenza». "
                "A ottobre 2026 le 324 schede evento sono state lette una volta, su indicazione dell'owner, per i soli campi di scheda (Dove, Quando, Prezzo, Sito web), "
                "il promotore e i link esterni; nessun testo conservato. I titoli delle sue pagine sono testo della fonte e non entrano nel repository (DEC-022).",
                "Il promotore quando l'evento è inserito dall'organizzatore (20 su 324); altrimenti la redazione riscrive il comunicato e di norma non linka: 168 schede senza alcun riferimento esterno, "
                "di cui per 109 la fonte esiste altrove (nel testo, in un'altra fonte del file o nel registro) e per 14 l'organizzatore è raggiungibile solo per contatto diretto.")
    out += card("fonte_locale", "Lettura diretta delle fonti locali (13-31 ottobre 2026)",
                "Siti dei luoghi scelti nel registro fonti del 13 ottobre (62 fonti: teatri, musei, cinema, club). Letti alla fonte, due passate.",
                "Evento, date, luogo, zona QN e Municipio assegnati a mano; flag «anche su Roma Today» (35 su 358).")
    out += ["## Sovrapposizioni fra aggregatori", "",
            "Gruppi di eventi riconosciuti come lo stesso evento (titolo quasi identico e date compatibili, oppure titolo simile con stessa data e luogo). "
            "Candidati da scorrere, non sentenze.", "", "| tipo · fonti | gruppi |", "|---|---|"]
    for k, n in sched["doppioni"].items():
        out.append(f"| {k} | {n} |")
    out += ["", f"Organizzatori che su Facebook compaiono con un profilo personale: {sched['profili_personali_senza_url']} occorrenze; il nome resta nel registro (DEC-105: nessuna anonimizzazione), l'indirizzo del profilo no, perché non è un canale di pubblicazione.", ""]
    open(os.path.join(out_dir, "aggregatori.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="folder with eventi_unico.xlsx, registro_fonti.xlsx, culture_luoghi.json")
    ap.add_argument("--out", default="docs/wiki/fonti-eventi")
    ap.add_argument("--gazetteer", default="gazetteer/gazetteer.json")
    a = ap.parse_args()
    s = build(a.input, a.out, a.gazetteer)
    print(f"fonti {len(s['fonti'])} · nel registro {sum(1 for e in s['fonti'] if e['registro'])} · "
          f"con sito {sum(1 for e in s['fonti'] if e['canali']['sito'])} · con pagina QN {sum(1 for e in s['fonti'] if e['zona'])} · "
          f"profili personali senza url {s['profili_personali_senza_url']} → {a.out}")


if __name__ == "__main__":
    main()

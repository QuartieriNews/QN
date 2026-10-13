"""Eventi Meetup di Roma dalle sole pagine ammesse dal robots.txt.

Uso: meetup_roma.py SITEMAP.xml DIR

La ricerca di Meetup con parametri (?location=, &dateRange=, &eventType=, &source=) è vietata dal
robots.txt a tutti i robot: si leggono solo le pagine /find/it--roma/… elencate nella sitemap
internazionale (sw_find_international_sitemaps_1.xml.gz, da scaricare e decomprimere prima). Le
pagine tematiche localizzano per indirizzo IP e portano anche eventi di altre città: si tengono
solo gli eventi con fuso orario di Roma. Partecipanti e nomi delle persone non si salvano.
Scrive DIR/meetup_roma.json.
"""
import json, os, re, sys, time, urllib.request

UA = "QuartieriNews-ricerca/0.1 (progetto editoriale; contatto nel sito del progetto)"


def _unisci(store, chiave, obj):
    cur = store.setdefault(chiave, {})
    for k, v in obj.items():
        if v is not None and k != "rsvps":
            cur[k] = v


def eventi(next_data):
    """Eventi dai dati della pagina (__NEXT_DATA__): stato Apollo e oggetti annidati, riferimenti risolti."""
    ev, luoghi, gruppi = {}, {}, {}
    store = {"Event": ev, "Venue": luoghi, "Group": gruppi}
    pp = next_data.get("props", {}).get("pageProps", {})
    for k, v in (pp.get("__APOLLO_STATE__") or {}).items():
        tipo, _, ident = k.partition(":")
        if tipo in store:
            _unisci(store[tipo], ident, v)

    def walk(o):
        if isinstance(o, dict):
            t = o.get("__typename")
            if t in store and o.get("id"):
                _unisci(store[t], o["id"], o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(pp)

    def deref(x, store):
        if isinstance(x, dict) and "__ref" in x:
            return store.get(x["__ref"].split(":", 1)[1], {})
        if isinstance(x, dict) and x.get("id") in store:
            return {**store[x["id"]], **x}
        return x or {}
    out = []
    for i, e in ev.items():
        v, g = deref(e.get("venue"), luoghi), deref(e.get("group"), gruppi)
        out.append({"id": i, "titolo": e.get("title"), "url": e.get("eventUrl"), "tipo": e.get("eventType"),
                    "inizio": e.get("dateTime"), "fine": e.get("endTime"), "gruppo": g.get("name"),
                    "luogo": v.get("name"), "indirizzo": v.get("address"), "citta": v.get("city"),
                    "a_pagamento": bool(e.get("feeSettings"))})
    return out


def di_roma(e):
    return (e.get("inizio") or "")[-6:] in ("+01:00", "+02:00")


if __name__ == "__main__":
    smap, out = sys.argv[1], sys.argv[2]
    pagine = sorted(set(re.findall(r"<loc>([^<]*/find/it--roma/[^<]*)</loc>", open(smap, encoding="utf-8").read())))
    tutti = {}
    for u in pagine:
        assert "?" not in u
        t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
        if m:
            for e in eventi(json.loads(m.group(1))):
                if di_roma(e):
                    tutti[e["id"]] = {**tutti.get(e["id"], {}), **{k: v for k, v in e.items() if v}}
        time.sleep(2)
    json.dump(list(tutti.values()), open(out + "/meetup_roma.json", "w"), ensure_ascii=False, indent=1)
    print(len(pagine), "pagine;", len(tutti), "eventi di Roma")

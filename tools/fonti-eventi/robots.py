"""Lettura del robots.txt secondo RFC 9309: gruppi per user agent (gruppi con lo stesso agente si
sommano), regola più lunga, caratteri jolly «*» e fine «$». urllib.robotparser non gestisce i
jolly, che servono per regole come «Disallow: /*?location=*» (Meetup).

Uso come modulo: gruppi = parse(testo); ammesso(gruppi, "ClaudeBot", url).
"""
import re
import urllib.parse

AGENTI_AI = ("claudebot", "claude-web", "anthropic-ai", "gptbot", "ccbot")


def parse(testo):
    gruppi, agenti, regole, in_regole = [], [], [], False
    for riga in testo.splitlines():
        riga = riga.split("#", 1)[0].strip()
        if ":" not in riga:
            continue
        k, v = (x.strip() for x in riga.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if in_regole:
                gruppi.append((agenti, regole))
                agenti, regole, in_regole = [], [], False
            agenti.append(v.lower())
        elif k in ("allow", "disallow"):
            in_regole = True
            if agenti:
                regole.append((k == "allow", v))
    if agenti:
        gruppi.append((agenti, regole))
    return gruppi


def regole_per(gruppi, agente):
    a = agente.lower()
    if any(a in ag for ag, _ in gruppi):
        return [r for ag, rs in gruppi if a in ag for r in rs]
    return [r for ag, rs in gruppi if "*" in ag for r in rs]


def _pattern(p):
    fine = p.endswith("$")
    rx = ".*".join(re.escape(x) for x in (p[:-1] if fine else p).split("*"))
    return re.compile("^" + rx + ("$" if fine else ""))


def ammesso(gruppi, agente, url):
    """True se l'agente può leggere l'URL; senza regole applicabili è ammesso."""
    pu = urllib.parse.urlsplit(url)
    percorso = (pu.path or "/") + ("?" + pu.query if pu.query else "")
    migliore = None  # (lunghezza del pattern, allow)
    for allow, p in regole_per(gruppi, agente):
        if p and _pattern(p).match(percorso):
            if migliore is None or len(p) > migliore[0] or (len(p) == migliore[0] and allow):
                migliore = (len(p), allow)
    return True if migliore is None else migliore[1]


def stato(gruppi, url):
    """'ammesso', 'esclude_agenti_ai' (vietato agli agenti AI con il loro nome) o 'vietato' (a tutti).

    Le esclusioni rivolte agli agenti AI valgono anche per QN, che non le aggira cambiando nome
    (CRONACA_PROCESSO_2026-10.md §5.1)."""
    if not ammesso(gruppi, "*", url):
        return "vietato"
    if any(not ammesso(gruppi, a, url) for a in AGENTI_AI):
        return "esclude_agenti_ai"
    return "ammesso"

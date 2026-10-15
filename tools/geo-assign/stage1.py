#!/usr/bin/env python3
"""Stage 1 of the QN geography process: evidence and a proposal, never a verdict.

Reads only input/schede_input.jsonl, the gazetteer and the cartography of the
package. It never opens benchmark/, storico/ or risultati_*: the proposal is
blind by construction, so its agreement with the archive measures the code,
not a replay of old decisions (Metodo QN §12, §16).

For every record it writes one evidence packet: each place mention with its
source field, original and normalised form, role cues, GIS resolution and the
identifiers it rests on; scope and multi-site cues; same-vicenda siblings; a
proposed outcome with reason codes and a review priority. Stage 2 (contextual
reading) decides; stage 1 only prepares and flags.

  stage1.py --pkg PKG --out DIR [--ids N0001 N0002 ...]
writes DIR/evidenze.jsonl and DIR/proposte.jsonl (aggregator-compatible).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import Atlas, STREET_PREFIXES, norm, package_root, rules_path, _ascii  # noqa: E402

# Ambiguous locality names: a word, a person, a street part or a page name that
# is also a common noun. They count only with a locality cue in front of them
# or as a whole `luoghi` segment (gazetteer free_text_stoplist, plus the
# historical list of generic names, Metodo QN §7).
GENERIC = {'ponte', 'colonna', 'pigna', 'monti', 'salone', 'villini', 'certosa',
           'decima', 'acqua acetosa', 'san paolo', 'san francesco', 'san giorgio',
           'sant andrea', 'roma nord', 'torrino', 'alessandrino', 'salario', 'regola',
           'campo marzio', 'trevi', 'borgo', 'castro pretorio', 'sallustiano',
           'aurelio', 'tuscolano', 'ostiense', 'portuense', 'prenestino',
           'tiburtino', 'nomentano', 'appio', 'flaminio', 'trieste', 'labaro',
           'giuliano dalmata', 'medaglie d oro', 'villa ada', 'villa borghese',
           'gianicolense', 'europa', 'esquilino', 'centro', 'laurentino', 'cassia',
           'casilino', 'collatino', 'ardeatino', 'magliana', 'trionfale'}
LOC_CUE = {'quartiere', 'rione', 'zona', 'localita', 'borgata', 'frazione', 'a', 'ad',
           'al', 'nel', 'nella', 'nei', 'quadrante', 'area', 'territorio', 'abitanti',
           'residenti', 'tra', 'fra', 'verso', 'da'}
PROPER_NAME_HEADS = {'liceo', 'istituto', 'ic', 'scuola', 'stazione', 'fermata',
                     'metro', 'ospedale', 'policlinico', 'asl', 'parrocchia', 'chiesa',
                     'basilica', 'acquedotto', 'porta', 'teatro', 'cinema', 'mercato',
                     'circolo', 'associazione', 'comitato', 'polisportiva', 'asd',
                     'biblioteca', 'museo', 'deposito', 'consorzio', 'ufficio'}
SCOPE = re.compile(r"\b(tutto il (territorio del )?municipio|intero (territorio|municipio)|"
                   r"tutti i (quartieri|municipi)|tutto il territorio|in tutta (la )?citta|"
                   r"(intera|tutta la) citta|cittadin[oaie]|capitolin[oaie]|regional[ei]|"
                   r"regolamento|bilancio|rendiconto|assestamento|variazion[ei] di bilancio|"
                   r"linee guida|piano (sociale|triennale|di zona|del commercio|urbano)|"
                   r"statuto|nomin[ae]|dimission|surroga|calendario dei lavori|"
                   r"tutte le scuole|tutti gli istituti|ogni municipio|sull'intero)\b")
MULTI = re.compile(r"\b(due|tre|quattro|cinque|sei|sette|otto|nove|dieci|diverse|varie|piu)\s+"
                   r"(sedi|luoghi|scuole|plessi|parchi|aree|mercati|strade|tappe|quartieri|giardini|biblioteche)\b|"
                   r"\b(itinerante|corteo|parata|percorso|itinerario|passeggiata|staffetta|maratona|"
                   r"tour|in giro per|tappe|rassegna diffusa|diffus[oa])\b")
TRACT = re.compile(r"\b(?:tra|fra|da)\s+(?:via|viale|piazza|piazzale|largo|porta|ponte|corso)\b[^.;]{0,60}?"
                   r"\b(?:e|a|fino a)\s+(?:via|viale|piazza|piazzale|largo|porta|ponte|corso)\b")
CROSS = re.compile(r"\b(incrocio|angolo|all'altezza|altezza di|intersezione|crocevia|"
                   r"(?:tra|fra) via\b[^.;]{0,40}\be via)\b")
# DEC-106: a sitting's seat gives a level, not a page; a service used at an
# address (desk open day, in-person enrolment) gives both.
SITTING = re.compile(r"\b(convocat[oaie]|seduta|ordine del giorno|giunta (municipale|capitolina)|"
                     r"consiglio (municipale|straordinario)|aula consiliare|sala consiliare)\b")
SERVICE = re.compile(r"\b(sportell[oi]|open day|identity point|presentazione delle domande|prenotazion[ei]|"
                     r"preiscrizion[ei]|iscrizion[ei]|domande)\b")
ORGAN = re.compile(SITTING.pattern + "|" + SERVICE.pattern + r"|\b(bando|avviso pubblico|graduatori[ae])\b")
CITY = re.compile(r"\b(capitolin[oaie]|cittadin[oaie]|tutta (la )?citta|intera citta|roma capitale|regional[ei]|"
                  r"centro storico unesco|citta storica)\b")
SEAT = re.compile(r"\b(sede (del|della) (municipio|commissione|consiglio)|aula consiliare|"
                  r"via dei cerchi|piazza del campidoglio|palazzo senatorio)\b")


STOPWORDS = set('di del della dei degli delle dell da dal dalla in nel nella a al alla ai e ed il la le lo i gli un una per con su sul sulla tra fra che non si roma municipio via viale piazza largo'.split()) | set('i ii iii iv v vi vii viii ix x xi xii xiii xiv xv'.split())


def _sentences(text):
    return [s for s in re.split(r'(?<=[.;!?])\s+', text or '') if s.strip()]


def coreference(streets):
    """Resolve a short street form to the one full name of the same record
    that contains it. Two compatible full names are an ambiguity to keep
    (`coreferenza_ambigua`), never the last one met (Metodo QN §7)."""
    for m in streets:
        if m['livello_normalizzazione'] == 0 and len(m['chiavi']) == 1 and len(m['chiavi'][0].split()) > 2:
            continue
        short = set(m['variante'].split()) - {'via', 'viale', 'piazza', 'piazzale', 'largo'}
        if not short:
            continue
        full = set()
        for o in streets:
            if o is m:
                continue
            for k in o['chiavi']:
                if len(k.split()) > len(m['variante'].split()) and short <= set(k.split()) and k not in m['chiavi']:
                    full.add(k)
        if len(full) == 1:
            m['coreferenza'] = full.pop()
        elif full:
            m['coreferenza_ambigua'] = sorted(full)
    return streets


class Stage1:
    def __init__(self, pkg: Path):
        self.pkg = pkg
        self.at = Atlas(pkg)
        g = self.at.gaz
        self.stop = {norm(x) for x in g['free_text_stoplist']}
        self.never = {norm(x) for x in g['never_substring']}
        self.loc_keys = sorted((k for k in self.at.loc if k and k not in self.never),
                               key=lambda k: -len(k.split()))
        self.loc_first = collections.defaultdict(list)
        for k in self.loc_keys:
            self.loc_first[k.split()[0]].append(k)

    # ------------------------------------------------------------ mentions
    def localities(self, text, field, whole_segment=False):
        orig = _ascii(text)
        toks = [(m.group(), m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9]+', orig)]
        words = [t[0].lower() for t in toks]
        out, i = [], 0
        while i < len(words):
            best = None
            for k in self.loc_first.get(words[i], ()):
                kw = k.split()
                if words[i:i + len(kw)] == kw:
                    best = k
                    break
            if not best:
                i += 1
                continue
            n = len(best.split())
            prev = words[max(0, i - 3):i]
            reason = None
            if prev and (prev[-1] in STREET_PREFIXES or set(prev) & STREET_PREFIXES and prev[-1] in {'di', 'del', 'della', 'dei', 'delle', 'degli', 'dell', 'd', 'san', 'santa'}):
                reason = 'parte del nome di una strada'
            elif prev and prev[-1] in PROPER_NAME_HEADS | {'di', 'del', 'della'} and set(prev) & PROPER_NAME_HEADS:
                reason = 'parte del nome di una sede o istituto'
            elif 'municipio' in words[max(0, i - 4):i] and re.fullmatch(r'[ivx]+|roma', prev[-1]):
                # "Municipio Roma XIII Aurelio", "Municipio IX Eur": the name of
                # the administration, not the place of the fact.
                reason = 'nome del municipio'
            elif best in self.stop or best in GENERIC:
                cued = prev and prev[-1] in LOC_CUE
                capital = toks[i][0][:1].isupper()
                # whole_segment: the alias IS the luoghi entry ("Monti"), not a
                # word inside it ("Torretta di Ponte Emilio").
                whole = whole_segment and norm(text) in (best, 'rione ' + best, 'quartiere ' + best, 'zona ' + best)
                if not (whole or (cued and capital)):
                    reason = 'nome ambiguo senza indicazione di localita'
            out.append({'tipo': 'localita', 'campo': field, 'testo': text[toks[i][1]:toks[i + n - 1][2]],
                        'norm': best, 'pagine': sorted(self.at.loc[best]),
                        'scartata': reason})
            i += n
        return out

    def streets(self, text, field, municipi):
        out = []
        for h in self.at.match_streets(text, municipi):
            res = [self.at.strada(k, municipi) for k in h['chiavi']]
            out.append({'tipo': 'strada', 'campo': field, **h, 'risoluzione': res})
        return out

    def evidence(self, r, siblings):
        municipi = sorted(set(re.findall(r'\b[IVX]+\b', (r['municipio'] or '') + ' ' + (r['municipio_documento'] or ''))))
        mentions = []
        segs = [s.strip() for s in (r['luoghi'] or '').split(';') if s.strip()]
        for s in segs:
            mentions += self.streets(s, 'luoghi', municipi)
            mentions += self.localities(s, 'luoghi', whole_segment=True)
        for field in ('titolo', 'sintesi'):
            mentions += self.streets(r[field], field, municipi)
            mentions += self.localities(r[field], field)
        # Owner rules on named places (venues, monuments, parks): decided once,
        # reused everywhere, always cited by rule id.
        for rule in self.at.rules:
            if rule['tipo'] != 'luogo':
                continue
            for field in ('luoghi', 'titolo', 'sintesi'):
                if f" {rule['chiave']} " in f" {norm(r[field])} ":
                    mentions.append({'tipo': 'luogo_regola', 'campo': field, 'testo': rule['chiave'],
                                     'norm': rule['chiave'], 'pagine': rule['pagine'], 'regola': rule['id'],
                                     'modo': rule['modo'], 'scartata': None})
        # Record-level coreference: "via Aversa" in the title and "via Raffaele
        # Aversa" in the summary are one street; the short form must not open
        # a second, wrong candidate (case N2863).
        streets = [m for m in mentions if m['tipo'] == 'strada']
        coreference(streets)
        for m in streets:
            if m.get('coreferenza'):
                m['chiavi'] = [m['coreferenza']]
                m['risoluzione'] = [self.at.strada(m['coreferenza'], municipi)]
        # civic points and intersections
        for m in streets:
            if m['civico'] and len(m['chiavi']) == 1:
                c = self.at.civico(self.at.roads[m['chiavi'][0]]['name'], m['civico'])
                m['punto_civico'] = c
        text = ' '.join([r['titolo'], r['sintesi'], r['luoghi']])
        ntext = norm(text)
        crossings = []
        for sent in _sentences(r['titolo']) + _sentences(r['sintesi']) + segs:
            if not CROSS.search(norm(sent)) and not re.search(r'\b(incrocio|angolo)\b', norm(sent)):
                continue
            keys = []
            for h in self.at.match_streets(sent, municipi):
                if len(h['chiavi']) == 1 and h['chiavi'][0] not in keys:
                    keys.append(h['chiavi'][0])
            for a in range(len(keys)):
                for b in range(a + 1, len(keys)):
                    x = self.at.incrocio(keys[a], keys[b])
                    if x['trovato']:
                        crossings.append({'frase': sent[:200], **x})
        cues = {
            'portata': sorted({m.group(0) for m in SCOPE.finditer(ntext)}),
            'multisede': sorted({m.group(0) for m in MULTI.finditer(ntext)}),
            'tratto': [m.group(0) for m in TRACT.finditer(ntext)],
            'sede_istituzionale': sorted({m.group(0) for m in SEAT.finditer(ntext)}),
            'organo_o_sportello': sorted({m.group(0) for m in ORGAN.finditer(ntext)}),
            'municipi_nominati': sorted(set(re.findall(r'\bmunicipi?o? ([ivx]+)\b', ntext))),
        }
        # One entry per place, with every field it appears in.
        merged = collections.OrderedDict()
        for m in mentions:
            k = (m['tipo'], tuple(m.get('chiavi') or [m.get('norm')]), m.get('civico'), m.get('scartata'))
            if k in merged:
                if m['campo'] not in merged[k]['campi']:
                    merged[k]['campi'].append(m['campo'])
            else:
                merged[k] = {**m, 'campi': [m['campo']]}
        mentions = list(merged.values())
        for m in mentions:
            # Strength of the textual support, not of the geography: a name
            # read only in the generated summary, without civic number, is the
            # weakest kind (case N2550: "via di Francesco" is a pilgrim route).
            m['supporto'] = 'forte' if ({'luoghi', 'titolo'} & set(m['campi']) or m.get('civico')) else 'debole'
        # luoghi segments no mention explains: usually a venue to look up.
        unexplained = []
        for seg in segs:
            ns = norm(seg)
            if not any(norm(m['testo']) in ns or ns in norm(m['testo']) for m in mentions if not m.get('scartata')):
                unexplained.append(seg)
        # A QN locality inside a street name is not a locality mention, but if
        # the gazetteer routes it to another page the reader must choose (N3129).
        for m in mentions:
            if m['tipo'] == 'localita' and m.get('scartata') == 'parte del nome di una strada':
                street_pages = {p for o in mentions if o['tipo'] == 'strada' and norm(m['testo']) in norm(o['testo'])
                                for res in o.get('risoluzione', []) for p in res['pagine']}
                if street_pages and not set(m['pagine']) & street_pages:
                    cues.setdefault('localita_nel_nome_strada', []).append(
                        {'localita': m['testo'], 'pagine_gazetteer': m['pagine'], 'pagine_strada': sorted(street_pages)})
        return {'municipi_contesto': municipi, 'menzioni': mentions, 'incroci': crossings,
                'luoghi_non_risolti': unexplained, 'indizi': cues, 'stessa_vicenda': siblings}

    # ------------------------------------------------------------ proposal
    def propose(self, r, ev):
        active = self.at.active
        precise, alternatives, inactive, notes = [], [], set(), []
        for m in ev['menzioni']:
            if m['tipo'] in ('localita', 'luogo_regola'):
                if m['scartata']:
                    continue
                ps = set(m['pagine'])
                if not ps & active:
                    inactive.update(ps)
                elif m['tipo'] == 'localita' and len(ps & active) > 1:
                    # gazetteer resolution.on_ambiguous: never pick, never merge
                    alternatives.append((m, ps & active, 'alias del gazetteer su piu pagine (ambiguous_alias): serve il contesto'))
                else:
                    precise.append((m, ps & active))
                continue
            pc = m.get('punto_civico') or {}
            if pc.get('trovato'):
                ps = {p for pt in pc['punti'] for p in pt['pagine']}
                near = {p for pt in pc['punti'] for p in (pt.get('confine') or {}).get('pagine_vicine', [])}
                if any(pt.get('approssimato') for pt in pc['punti']):
                    # The register has no such number: a neighbour was used and said so (§7).
                    alternatives.append((m, ps | near, 'civico assente dal registro, punto approssimato: verificare il numero'))
                    continue
                if near - ps:
                    alternatives.append((m, ps | near, 'civico a pochi metri dal confine fra pagine (DEC-107 aperta)'))
                    continue
                if any(pt.get('discordanza') for pt in pc['punti']):
                    # Zone and toponymic subdivision disagree: the reader reads both (protocol).
                    alternatives.append((m, ps | near, 'cartografie discordanti sul punto del civico: leggere entrambe'))
                    continue
                if len(ps) == 1:
                    precise.append((m, ps))
                    continue
                if len(ps) > 1:
                    # Official points of the same number on several pages (letters,
                    # duplicates of the register): a doubt, not the whole street.
                    alternatives.append((m, ps, 'punti ufficiali del civico su piu pagine: verificare'))
                    continue
            if len(m['chiavi']) > 1:
                alternatives.append((m, set(), 'omonimia: piu strade con lo stesso nome'))
                continue
            res = m['risoluzione'][0] if m['risoluzione'] else None
            if not res or not res['pagine']:
                if res and (res.get('regola') or {}).get('modo') == 'senza_pagina':
                    inactive.add(f"regola {res['regola']['id']}: strada senza pagina per decisione dell'owner")
                elif res and res['zone_senza_pagina']:
                    inactive.add('zona senza pagina: ' + ', '.join(res['zone_senza_pagina']))
                continue
            ps = set(res.get('pagine_nel_municipio') or res['pagine'])
            if (res.get('regola') or {}).get('modo') == 'doppia_confine':
                # Owner rule: a place on the boundary belongs to both pages.
                precise.append(({**m, 'confine': True}, set(res['pagine']) & active))
                continue
            if not ps & active:
                inactive.update(ps)
                continue
            ps &= active
            if len(ps) == 1:
                precise.append((m, ps))
            else:
                alternatives.append((m, ps, 'strada su piu pagine senza tratto'))
        for x in ev['incroci']:
            near = {p for pt in x['punti'] for p in (pt.get('confine') or {}).get('pagine_vicine', [])}
            label = {'tipo': 'incrocio', 'testo': ' x '.join(x['strade'])}
            if near - set(x['pagine']):
                alternatives.append((label, set(x['pagine']) | near, 'incrocio sul confine fra pagine (DEC-107 aperta)'))
            elif not x.get('esatto', True):
                # The roads do not touch in the stradario copy: a midpoint within
                # tolerance is a lead, not a fact (protocol: never invent).
                alternatives.append((label, set(x['pagine']),
                                     f"incrocio non esatto: strade a {x.get('distanza_m', '?')} m nello stradario"))
            elif any(pt.get('discordanza') for pt in x['punti']):
                alternatives.append((label, set(x['pagine']), 'cartografie discordanti sul punto di incrocio: leggere entrambe'))
            elif len(x['pagine']) == 1:
                precise.append((label, set(x['pagine'])))
            elif x['pagine']:
                # Roads meeting more than once, on different pages: candidates, D not M.
                alternatives.append((label, set(x['pagine']), 'incrocio in piu punti su pagine diverse: scegliere dal contesto'))
        pages = set().union(*[p for _, p in precise]) if precise else set()
        title_pages = set().union(*[p for m, p in precise if 'titolo' in m.get('campi', [])]) if precise else set()
        cues = ev['indizi']
        reasons, priority = [], 'normale'
        if cues.get('localita_nel_nome_strada'):
            priority = 'alta'
            reasons.append('localita del gazetteer nel nome della strada con pagina diversa: scegliere il raccordo')
        weak_only = bool(precise) and all(m.get('supporto') == 'debole' for m, _ in precise)
        title = norm(r['titolo'])
        if SITTING.search(title) and not MULTI.search(title):
            # Convocations and sittings: the address is the organ's seat.
            return {'id': r['id'], 'esito_proposto': 'T?', 'pagine_proposte': [], 'livello_proposto': 'municipio',
                    'candidate': sorted(pages), 'priorita_revisione': 'alta',
                    'ragioni': ['seduta o convocazione: la sede istituzionale da il livello municipale, non una pagina (DEC-106)']}
        if SERVICE.search(title) and len(pages) == 1 and not MULTI.search(title):
            return {'id': r['id'], 'esito_proposto': 'U', 'pagine_proposte': sorted(pages), 'livello_proposto': 'municipio',
                    'candidate': [], 'priorita_revisione': 'alta',
                    'ragioni': ['servizio fruito nel luogo: pagina dello sportello e livello municipale (DEC-106); '
                                'verificare che non sia solo un recapito']}
        full = norm(r['titolo'] + ' ' + r['sintesi'] + ' ' + r['luoghi'])
        if re.search(r'\b(centr[oi] storic[oi]|citta storica)\b', full) and re.search(
                r'\b(norm[ae]|disciplin[ae]|regolament[oi]|delibera|variante|piano|liberalizzazion[ei]|contingentat[ei])\b', full):
            return {'id': r['id'], 'esito_proposto': 'T?', 'pagine_proposte': [], 'livello_proposto': 'citta',
                    'candidate': sorted(pages), 'priorita_revisione': 'alta',
                    'ragioni': ['norma sul centro storico in senso urbanistico: notizia cittadina (DEC-106); '
                                'verificare che non sia un intervento in un luogo preciso']}
        if len(pages) == 1:
            alt_out = [a for a in alternatives if a[1] and not a[1] & pages]
            esito, pagine = 'U', sorted(pages)
            reasons.append('riferimenti precisi convergenti su una pagina')
            if alt_out:
                reasons.append('altre strade ambigue fuori dalla pagina: verificare il ruolo')
                priority = 'alta'
            if cues['multisede'] or cues['tratto']:
                reasons.append('indizi di piu sedi o di un tratto: leggere la lista completa')
                priority = 'alta'
            if cues['portata'] and not title_pages:
                reasons.append('indizi di portata municipale/cittadina: luogo forse solo esemplificativo')
                priority = 'alta'
            if weak_only:
                reasons.append('sostenuto solo da menzioni deboli (sintesi, senza civico)')
                priority = 'alta'
            if ev['luoghi_non_risolti']:
                reasons.append('luoghi non spiegati dal codice (sedi?): ' + '; '.join(ev['luoghi_non_risolti'])[:120])
                priority = 'alta'
            if inactive:
                reasons.append('anche territori senza pagina attiva: ' + ', '.join(sorted(inactive))[:80])
        elif len(pages) > 1:
            esito, pagine = 'M?', sorted(pages)
            reasons.append('riferimenti precisi su piu pagine: distinguere sedi effettive, provenienze, confronti')
            priority = 'alta'
        elif alternatives:
            esito, pagine = 'D', []
            reasons.append(alternatives[0][2])
        elif inactive:
            esito, pagine = 'F?', []
            reasons.append('luogo riconosciuto senza pagina attiva: ' + ', '.join(sorted(inactive))[:120])
            priority = 'alta'
        elif cues['portata']:
            esito, pagine = 'T?', []
            reasons.append('nessun luogo riconosciuto e indizi di portata: ' + ', '.join(cues['portata'][:3]))
        else:
            esito, pagine = '?', []
            reasons.append('nessun luogo riconosciuto dal codice: leggere (sede da cercare, T, I)')
            priority = 'alta'
        cand = sorted(set().union(*[a[1] for a in alternatives]) - set(pagine)) if alternatives else []
        if esito.startswith('T'):
            level = 'citta' if CITY.search(norm(r['titolo'] + ' ' + r['sintesi'])) else 'municipio'
        else:
            level = 'quartiere'
        return {'id': r['id'], 'esito_proposto': esito, 'pagine_proposte': pagine, 'livello_proposto': level,
                'candidate': cand, 'ragioni': reasons, 'priorita_revisione': priority}


def load_input(pkg: Path):
    return [json.loads(l) for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines() if l.strip()]


def run(pkg: Path, out: Path, ids=None):
    s1 = Stage1(pkg)
    rows = load_input(pkg)
    by_v = collections.defaultdict(list)
    for r in rows:
        if r['vicenda_id']:
            by_v[r['vicenda_id']].append(r)
    out.mkdir(parents=True, exist_ok=True)
    want = set(ids) if ids else None
    ev_lines, prop_lines = [], []
    for r in rows:
        if want and r['id'] not in want:
            continue
        # Same vicenda_id often means only the same sitting: rank siblings by
        # shared place words and say which ones share nothing (reviewers' note).
        own = set(norm(r['luoghi'] + ' ' + r['titolo']).split()) - STOPWORDS
        sib = []
        for o in by_v.get(r['vicenda_id'], []):
            if o['id'] == r['id']:
                continue
            shared = sorted(own & (set(norm(o['luoghi'] + ' ' + o['titolo']).split()) - STOPWORDS))
            sib.append({'id': o['id'], 'documento_id': o['documento_id'], 'fonte': o['fonte'],
                        'titolo': o['titolo'], 'luoghi': o['luoghi'], 'parole_in_comune': shared,
                        'stesso_documento': o['documento_id'] == r['documento_id']})
        sib.sort(key=lambda x: -len(x['parole_in_comune']))
        sib = sib[:12]
        ev = s1.evidence(r, sib)
        pr = s1.propose(r, ev)
        ev_lines.append(json.dumps({'id': r['id'], **ev, 'proposta': pr}, ensure_ascii=False))
        prop_lines.append(json.dumps(pr, ensure_ascii=False))
    (out / 'evidenze.jsonl').write_text('\n'.join(ev_lines) + '\n', encoding='utf-8')
    (out / 'proposte.jsonl').write_text('\n'.join(prop_lines) + '\n', encoding='utf-8')
    # The owner rules these evidences were built with travel with them, so a
    # packet made later cites the same rules and not the current file (DEC-106).
    rp = rules_path()
    (out / 'regole_geografiche.json').write_text(
        rp.read_text(encoding='utf-8') if rp.is_file() else json.dumps({'regole': [], 'chiusi': []}), encoding='utf-8')
    return len(prop_lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--ids', nargs='*')
    a = ap.parse_args()
    n = run(package_root(a.pkg), a.out, a.ids)
    print(json.dumps({'schede': n, 'out': str(a.out)}))

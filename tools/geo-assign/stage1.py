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
from qngeo import Atlas, STREET_PREFIXES, norm, package_root, _ascii  # noqa: E402

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
ORGAN = re.compile(r"\b(convocat[oaie]|seduta|ordine del giorno|giunta (municipale|capitolina)|consiglio (municipale|straordinario)|"
                   r"aula consiliare|sala consiliare|sportello|presentazione delle domande|prenotazion[ei]|"
                   r"preiscrizion[ei]|iscrizion[ei]|bando|avviso pubblico|graduatori[ae])\b")
SEAT = re.compile(r"\b(sede (del|della) (municipio|commissione|consiglio)|aula consiliare|"
                  r"via dei cerchi|piazza del campidoglio|palazzo senatorio)\b")


def _sentences(text):
    return [s for s in re.split(r'(?<=[.;!?])\s+', text or '') if s.strip()]


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
        # Record-level coreference: "via Aversa" in the title and "via Raffaele
        # Aversa" in the summary are one street; the short form must not open
        # a second, wrong candidate (case N2863).
        streets = [m for m in mentions if m['tipo'] == 'strada']
        for m in streets:
            if m['livello_normalizzazione'] == 0 and len(m['chiavi']) == 1 and len(m['chiavi'][0].split()) > 2:
                continue
            short = set(m['variante'].split()) - {'via', 'viale', 'piazza', 'piazzale', 'largo'}
            for o in streets:
                if o is m or not short:
                    continue
                for k in o['chiavi']:
                    if len(k.split()) > len(m['variante'].split()) and short <= set(k.split()) and k not in m['chiavi']:
                        m['coreferenza'] = k
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
            if m['tipo'] == 'localita':
                if m['scartata']:
                    continue
                ps = set(m['pagine'])
                if ps & active:
                    precise.append((m, ps & active))
                else:
                    inactive.update(ps)
                continue
            pc = m.get('punto_civico') or {}
            if pc.get('trovato'):
                ps = {p for pt in pc['punti'] for p in pt['pagine']}
                if len(ps) == 1:
                    precise.append((m, ps))
                    continue
            if len(m['chiavi']) > 1:
                alternatives.append((m, set(), 'omonimia: piu strade con lo stesso nome'))
                continue
            res = m['risoluzione'][0] if m['risoluzione'] else None
            if not res or not res['pagine']:
                if res and res['zone_senza_pagina']:
                    inactive.add('zona senza pagina: ' + ', '.join(res['zone_senza_pagina']))
                continue
            ps = set(res.get('pagine_nel_municipio') or res['pagine'])
            if not ps & active:
                inactive.update(ps)
                continue
            ps &= active
            if len(ps) == 1:
                precise.append((m, ps))
            else:
                alternatives.append((m, ps, 'strada su piu pagine senza tratto'))
        for x in ev['incroci']:
            if len(x['pagine']) == 1:
                precise.append(({'tipo': 'incrocio', 'testo': ' x '.join(x['strade'])}, set(x['pagine'])))
        pages = set().union(*[p for _, p in precise]) if precise else set()
        title_pages = set().union(*[p for m, p in precise if 'titolo' in m.get('campi', [])]) if precise else set()
        cues = ev['indizi']
        reasons, priority = [], 'normale'
        if cues.get('localita_nel_nome_strada'):
            priority = 'alta'
            reasons.append('localita del gazetteer nel nome della strada con pagina diversa: scegliere il raccordo')
        weak_only = bool(precise) and all(m.get('supporto') == 'debole' for m, _ in precise)
        organ_title = bool(ORGAN.search(norm(r['titolo'])))
        if organ_title and cues['organo_o_sportello'] and not MULTI.search(norm(r['titolo'])):
            # Convocations, desks, applications: the address is where the organ
            # meets or where to apply, not the place of a local fact.
            return {'id': r['id'], 'esito_proposto': 'T?', 'pagine_proposte': [],
                    'candidate': sorted(pages), 'priorita_revisione': 'alta',
                    'ragioni': ['funzionamento di un organo o di uno sportello: indirizzo come recapito, verificare se esiste un luogo del fatto']}
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
        return {'id': r['id'], 'esito_proposto': esito, 'pagine_proposte': pagine,
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
        sib = [{'id': o['id'], 'documento_id': o['documento_id'], 'fonte': o['fonte'],
                'titolo': o['titolo'], 'luoghi': o['luoghi']}
               for o in by_v.get(r['vicenda_id'], []) if o['id'] != r['id']][:12]
        ev = s1.evidence(r, sib)
        pr = s1.propose(r, ev)
        ev_lines.append(json.dumps({'id': r['id'], **ev, 'proposta': pr}, ensure_ascii=False))
        prop_lines.append(json.dumps(pr, ensure_ascii=False))
    (out / 'evidenze.jsonl').write_text('\n'.join(ev_lines) + '\n', encoding='utf-8')
    (out / 'proposte.jsonl').write_text('\n'.join(prop_lines) + '\n', encoding='utf-8')
    return len(prop_lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--ids', nargs='*')
    a = ap.parse_args()
    n = run(package_root(a.pkg), a.out, a.ids)
    print(json.dumps({'schede': n, 'out': str(a.out)}))

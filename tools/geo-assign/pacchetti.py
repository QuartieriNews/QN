#!/usr/bin/env python3
"""Render stage-1 evidence as review packets, and build a blind workspace.

  pacchetti.py --pkg PKG --evidenze DIR/evidenze.jsonl --ids-file campione.json \
      --lotti 6 --out WORKDIR

WORKDIR receives: a copy of input/ and cartografia/ only (never benchmark/,
storico/, risultati_*), the tools, the review protocol, and one packet file
per batch. Reviewers point QN_PKG at WORKDIR/pkg, so the archived outcomes
are not on the path they can read (Metodo QN §16, 04_VERIFICA §"Per una
valutazione nuova").
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import package_root, rules_path  # noqa: E402

FIELDS = ['id', 'fonte', 'documento_id', 'titolo', 'sintesi', 'luoghi', 'municipio',
          'quartiere', 'municipio_documento', 'data_fatto', 'vicenda_id', 'blocco_editoriale_proposto',
          'url_fonte', 'timestamp']


def _mention(m):
    d = {'tipo': m['tipo'], 'testo': m['testo'], 'campi': m['campi'], 'supporto': m.get('supporto')}
    if m.get('scartata'):
        d['scartata_dal_codice'] = m['scartata']
    if m['tipo'] == 'localita':
        d['pagine_gazetteer'] = m['pagine']
        return d
    if m['tipo'] == 'luogo_regola':
        # An owner rule on a named place (DEC-106): pages, rule id and mode, no street keys.
        d['pagine_regola'] = m['pagine']
        d['regola'] = m['regola']
        d['modo'] = m['modo']
        return d
    d['chiavi_stradario'] = m['chiavi']
    if m.get('coreferenza'):
        d['coreferenza'] = m['coreferenza']
    if m.get('coreferenza_ambigua'):
        d['coreferenza_ambigua'] = m['coreferenza_ambigua']
    if m.get('livello_normalizzazione'):
        d['normalizzazione'] = {1: 'via/viale o piazza/piazzale scambiati',
                                2: 'iniziale o solo cognome: forma debole'}[m['livello_normalizzazione']]
    if m.get('civico'):
        d['civico'] = m['civico']
        pc = m.get('punto_civico') or {}
        # The marks a reader must see travel with the point: an approximated
        # number (§7) and a boundary case (DEC-107) are cautions, not evidence.
        d['civico_punti'] = [_point(p) for p in pc.get('punti', [])] if pc.get('trovato') else 'non trovato (copia offline, cache, WFS)'
        if pc.get('trovato'):
            d['civico_fonte'] = pc.get('fonte')
    d['strada'] = [{'chiave': r['chiave'], 'municipi': r['municipi'], 'pagine': r['pagine'],
                    'pagine_nel_municipio': r.get('pagine_nel_municipio'),
                    'zone': [(z['code_zu'], z['nome'], z['frazione'], z['pagine']) for z in r['zone']],
                    'zone_senza_pagina': r['zone_senza_pagina'],
                    # An owner rule decided these pages: the reader cites it (DEC-106).
                    **({'regola': r['regola'], 'pagine_geometria': r.get('pagine_geometria')} if r.get('regola') else {})}
                   for r in m.get('risoluzione', [])]
    return d


def _point(p):
    """A classified point as the reader sees it: pages and basis, plus every
    caution that must travel with it (approximated number, boundary, the two
    cartographies when they disagree: protocol, "leggi entrambe")."""
    d = {'pagine': p['pagine'], 'base': p['base']}
    if 'id_civico' in p:
        d['id_civico'] = p['id_civico']
    else:
        d['lat'], d['lon'] = round(p['lat'], 6), round(p['lon'], 6)
    for k in ('approssimato', 'confine'):
        if p.get(k):
            d[k] = p[k]
    if p.get('discordanza'):
        d['discordanza'] = True
        d['zona_urbanistica'] = [(z['code_zu'], z['nome'], z['pagine'], z.get('fonte_raccordo'))
                                 for z in p.get('zona_urbanistica', [])]
        d['suddivisione'] = [(t['tipo'], t['nome']) for t in p.get('suddivisione', [])]
    return d


def packet(row, ev):
    return {'scheda': {k: row[k] for k in FIELDS},
            'evidenze_codice': {
                'municipi_contesto': ev['municipi_contesto'],
                'menzioni': [_mention(m) for m in ev['menzioni']],
                'incroci': [{'strade': x['strade'], 'pagine': x['pagine'], 'esatto': x['esatto'],
                             **({'distanza_m': x['distanza_m']} if x.get('distanza_m') is not None else {}),
                             'punti': [_point(p) for p in x['punti']]} for x in ev['incroci']],
                'luoghi_non_spiegati': ev['luoghi_non_risolti'],
                'indizi': ev['indizi'],
                'stessa_vicenda': ev['stessa_vicenda'],
                'proposta_del_codice': ev['proposta']}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--evidenze', required=True)
    ap.add_argument('--ids-file', required=True)
    ap.add_argument('--lotti', type=int, default=6)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    pkg = package_root(a.pkg)
    ids = json.loads(Path(a.ids_file).read_text())['ids']
    rows = {json.loads(l)['id']: json.loads(l) for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines() if l.strip()}
    evs = {json.loads(l)['id']: json.loads(l) for l in Path(a.evidenze).read_text(encoding='utf-8').splitlines() if l.strip()}
    out = a.out
    blind = out / 'pkg'
    # Rebuilt from scratch on every run: a retry after a package update must
    # not leave old input/ or cartografia/ beside new packets, nor packets of
    # a previous batch count (AGENTS.md: idempotency under retry).
    for sub in ('input', 'cartografia'):
        if (blind / sub).exists():
            shutil.rmtree(blind / sub)
        shutil.copytree(pkg / sub, blind / sub)
    for stale in out.glob('lotto_*.jsonl'):
        stale.unlink()
    here = Path(__file__).resolve().parent
    tools = out / 'strumenti'
    tools.mkdir(parents=True, exist_ok=True)
    for f in ('qngeo.py', 'zone_qn_cross.json', 'valida.py', 'PROTOCOLLO_REVISIONE.md'):
        shutil.copy2(here / f, tools / f)
    # The owner rules qngeo.py applies (DEC-106) must be the ones stage 1 used:
    # stage1.py leaves a copy beside evidenze.jsonl; without it, the current
    # file is copied and the packet says so. rules_path() looks beside qngeo.py.
    snapshot = Path(a.evidenze).resolve().parent / 'regole_geografiche.json'
    rules_src = snapshot if snapshot.is_file() else rules_path()
    if rules_src.is_file():
        shutil.copy2(rules_src, tools / 'regole_geografiche.json')
    else:
        (tools / 'regole_geografiche.json').write_text(json.dumps({'regole': [], 'chiusi': []}), encoding='utf-8')
    batches = [ids[i::a.lotti] for i in range(a.lotti)]
    for n, batch in enumerate(batches, 1):
        (out / f'lotto_{n}.jsonl').write_text(''.join(json.dumps(packet(rows[i], evs[i]), ensure_ascii=False) + '\n'
                                                     for i in batch), encoding='utf-8')
    print(json.dumps({'lotti': [len(b) for b in batches], 'out': str(out),
                      'regole': 'istantanea della fase 1' if rules_src == snapshot else 'file corrente (nessuna istantanea con le evidenze)'}))


if __name__ == '__main__':
    main()

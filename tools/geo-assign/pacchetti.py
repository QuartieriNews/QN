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
from qngeo import package_root  # noqa: E402

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
    d['chiavi_stradario'] = m['chiavi']
    if m.get('coreferenza'):
        d['coreferenza'] = m['coreferenza']
    if m.get('livello_normalizzazione'):
        d['normalizzazione'] = {1: 'via/viale o piazza/piazzale scambiati',
                                2: 'iniziale o solo cognome: forma debole'}[m['livello_normalizzazione']]
    if m.get('civico'):
        d['civico'] = m['civico']
        pc = m.get('punto_civico') or {}
        d['civico_offline'] = [{'id_civico': p['id_civico'], 'pagine': p['pagine'], 'base': p['base']}
                               for p in pc.get('punti', [])] if pc.get('trovato') else 'non nella copia offline'
    d['strada'] = [{'chiave': r['chiave'], 'municipi': r['municipi'], 'pagine': r['pagine'],
                    'pagine_nel_municipio': r.get('pagine_nel_municipio'),
                    'zone': [(z['code_zu'], z['nome'], z['frazione'], z['pagine']) for z in r['zone']],
                    'zone_senza_pagina': r['zone_senza_pagina']} for r in m.get('risoluzione', [])]
    return d


def packet(row, ev):
    return {'scheda': {k: row[k] for k in FIELDS},
            'evidenze_codice': {
                'municipi_contesto': ev['municipi_contesto'],
                'menzioni': [_mention(m) for m in ev['menzioni']],
                'incroci': [{'strade': x['strade'], 'pagine': x['pagine'], 'esatto': x['esatto'],
                             'punti': [{'lat': round(p['lat'], 6), 'lon': round(p['lon'], 6), 'pagine': p['pagine'],
                                        'base': p['base']} for p in x['punti']]} for x in ev['incroci']],
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
    for sub in ('input', 'cartografia'):
        if not (blind / sub).exists():
            shutil.copytree(pkg / sub, blind / sub)
    here = Path(__file__).resolve().parent
    tools = out / 'strumenti'
    tools.mkdir(parents=True, exist_ok=True)
    for f in ('qngeo.py', 'zone_qn_cross.json', 'valida.py', 'PROTOCOLLO_REVISIONE.md'):
        shutil.copy2(here / f, tools / f)
    batches = [ids[i::a.lotti] for i in range(a.lotti)]
    for n, batch in enumerate(batches, 1):
        (out / f'lotto_{n}.jsonl').write_text(''.join(json.dumps(packet(rows[i], evs[i]), ensure_ascii=False) + '\n'
                                                     for i in batch), encoding='utf-8')
    print(json.dumps({'lotti': [len(b) for b in batches], 'out': str(out)}))


if __name__ == '__main__':
    main()

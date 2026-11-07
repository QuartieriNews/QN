#!/usr/bin/env python3
"""Compare assignments (stage-1 proposals or stage-2 decisions) with the
archived benchmark, per ID, on a chosen subset. Run only AFTER the
assignments are frozen: this is the one script that opens benchmark/.

  confronta.py --pkg PKG --assegnazioni FILE [--ids-file campione.json | --escludi campione.json]
               [--dettaglio OUT.jsonl]

Reports the status confusion matrix, exact agreement (status and page set),
and for U/M the page overlap. Proposals with a '?' status count by their
letter (M? as M) and '?' alone as its own row.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import package_root  # noqa: E402


def load(path):
    out = {}
    for l in Path(path).read_text(encoding='utf-8-sig').splitlines():
        if l.strip():
            r = json.loads(l)
            out[r['id']] = {'esito': r.get('esito', r.get('esito_proposto')),
                            'pagine': sorted(r.get('pagine', r.get('pagine_proposte', [])) or []),
                            'motivo': r.get('motivo', '; '.join(r.get('ragioni', [])))}
    return out


def compare(pkg, mine, ids):
    ref = load(pkg / 'benchmark' / 'assegnazioni_2026-09-19.jsonl')
    conf = collections.Counter()
    rows = []
    exact = 0
    for i in ids:
        a, b = mine[i], ref[i]
        sa = a['esito'].rstrip('?') or '?'
        conf[(b['esito'], sa)] += 1
        same = sa == b['esito'] and a['pagine'] == b['pagine']
        exact += same
        if not same:
            rows.append({'id': i, 'storico': b, 'nuovo': a})
    statuses = ['U', 'M', 'T', 'D', 'I', 'F', '?']
    matrix = {s: {t: conf[(s, t)] for t in statuses if conf[(s, t)]} for s in statuses[:-1]}
    um = [i for i in ids if ref[i]['esito'] in 'UM' and mine[i]['esito'].rstrip('?') in ('U', 'M')]
    pages_equal = sum(ref[i]['pagine'] == mine[i]['pagine'] for i in um)
    overlap = sum(bool(set(ref[i]['pagine']) & set(mine[i]['pagine'])) for i in um)
    return {'n': len(ids), 'identici': exact, 'diversi': len(rows),
            'matrice_storico_righe_nuovo_colonne': matrix,
            'entrambi_UM': len(um), 'UM_pagine_identiche': pages_equal, 'UM_pagine_sovrapposte': overlap}, rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--assegnazioni', required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--ids-file')
    g.add_argument('--escludi')
    ap.add_argument('--solo-mantenute', action='store_true')
    ap.add_argument('--dettaglio')
    a = ap.parse_args()
    pkg = package_root(a.pkg)
    mine = load(a.assegnazioni)
    ids = sorted(mine)
    if a.ids_file:
        ids = json.loads(Path(a.ids_file).read_text())['ids']
    if a.escludi:
        ex = json.loads(Path(a.escludi).read_text())
        drop = set(ex['ids']) | set(ex['esclusi_didattici']) | set(ex['esclusi_audit'])
        ids = [i for i in ids if i not in drop]
    if a.solo_mantenute:
        keep = {json.loads(l)['id'] for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines()
                if l.strip() and json.loads(l)['in_stock'] == 1}
        ids = [i for i in ids if i in keep]
    summary, rows = compare(pkg, mine, ids)
    if a.dettaglio:
        Path(a.dettaglio).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=1))

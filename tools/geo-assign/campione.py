#!/usr/bin/env python3
"""Held-out sample for the blind test, drawn before any look at the benchmark.

Stratified by source over retained records (in_stock=1), seeded, excluding
the 19 cases the method package uses to teach (03_CASI_RAGIONATI.md): those
were read while learning the method and cannot test it (Metodo QN §17).
Everything not in the sample is the development set; stage-1 rules may be
tuned on the development set only.

  campione.py --pkg PKG --n 120 --seed 20261008 > campione_test.json
"""
import argparse
import collections
import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qngeo import package_root  # noqa: E402

TEACHING = ['N0013', 'N1868', 'N1887', 'N1985', 'N2075', 'N2473', 'N1252', 'N2550', 'N2863',
            'N2591', 'N1921', 'N2150', 'N2969', 'N1870', 'N1929', 'N3129']
AUDIT = ['N3519', 'N2403', 'N2310', 'N2028']
MIN_PER_SOURCE = 2


def draw(rows, n, seed):
    pool = collections.defaultdict(list)
    for r in rows:
        if r['in_stock'] == 1 and r['id'] not in TEACHING + AUDIT:
            pool[r['fonte']].append(r['id'])
    total = sum(len(v) for v in pool.values())
    quota = {f: max(MIN_PER_SOURCE, round(n * len(v) / total)) for f, v in pool.items()}
    rng = random.Random(seed)
    out = []
    for f in sorted(pool):
        ids = sorted(pool[f])
        out += sorted(rng.sample(ids, min(quota[f], len(ids))))
    return out, quota


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pkg')
    ap.add_argument('--n', type=int, default=120)
    ap.add_argument('--seed', type=int, default=20261008)
    a = ap.parse_args()
    pkg = package_root(a.pkg)
    rows = [json.loads(l) for l in (pkg / 'input' / 'schede_input.jsonl').read_text(encoding='utf-8-sig').splitlines() if l.strip()]
    ids, quota = draw(rows, a.n, a.seed)
    json.dump({'seed': a.seed, 'n': len(ids), 'quote_per_fonte': quota,
               'esclusi_didattici': TEACHING, 'esclusi_audit': AUDIT, 'ids': ids},
              sys.stdout, indent=1)
    print()

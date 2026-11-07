# Riallinea la colonna municipio dei lotti letti prima della correzione (STATO 24).
# I lotti B07+ sono stati letti con il valore gia' corretto: qui si toccano solo B01-B06.
import csv, sys, os
base = os.path.dirname(os.path.abspath(__file__))
corr = {r['name']: r['municipio'] for r in csv.DictReader(open(os.path.join(base, '_municipio_corretto.csv')))}
tot = 0
for n in range(1, 7):
    p = os.path.join(base, 'out', 'B%02d_atti.csv' % n)
    rows = list(csv.DictReader(open(p)))
    if not rows:
        continue
    cambi = 0
    for r in rows:
        atteso = corr.get(r['name'])
        if atteso is not None and r['municipio'] != atteso:
            r['municipio'] = atteso
            cambi += 1
    if cambi:
        with open(p, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    mancanti = sum(1 for r in rows if r['name'] not in corr)
    print('B%02d: %d righe, %d corrette, %d senza riscontro' % (n, len(rows), cambi, mancanti))
    tot += cambi
print('totale correzioni:', tot)

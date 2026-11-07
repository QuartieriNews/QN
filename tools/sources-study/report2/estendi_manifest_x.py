# I lotti X leggono atti che stanno fuori dalla finestra 8-28 giugno e che quindi non sono nel
# manifest del Report 2. Senza una riga nel manifest `build_db.py` li scarta con "ATTO SENZA
# MANIFEST": questo programma gliela aggiunge.
# Le righe nuove vanno **in coda**, mai in mezzo: l'identificativo A2_NNNN segue l'ordine del
# manifest, e inserirle in ordine alfabetico rinumererebbe tutti gli atti gia' citati dai lotti.
import csv, os, re

NET = os.environ['QN_NET']
MAN = NET + '/report2/manifest_report2.csv'

rep = {}
for l in open(NET + '/A2_all/_list.tsv', encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) >= 4: rep[p[0]] = p

righe = list(csv.DictReader(open(MAN, encoding='utf-8')))
gia = {r['name'] for r in righe}
campi = list(righe[0])

def settimana(d):
    """Le settimane dello studio contano dall'8 giugno. Un atto dell'1-7 sta in una settimana che
    lo studio non numera: si dichiara 0 invece di inventare un numero."""
    m = re.match(r'(\d{2})/(\d{2})/(\d{4})', d or '')
    if not m: return ''
    g, mese, anno = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if (anno, mese) != (2026, 6): return '0'   # fuori giugno 2026: fuori perimetro, qualunque sia il giorno
    return str((g - 8) // 7 + 1) if 8 <= g <= 28 else '0'

nuovi = []
for f in sorted(os.listdir(NET + '/report2/out')):
    if not re.match(r'X\d\d_atti\.csv$', f): continue
    for r in csv.DictReader(open(NET + '/report2/out/' + f, encoding='utf-8')):
        n = r['name']
        if n in gia: continue
        gia.add(n)
        p = rep.get(n)
        if not p:
            print('ATTO SENZA RIGA IN _list.tsv:', n); continue
        parti = n.split('_')
        nuovi.append({'name': n, 'url': p[1], 'data': p[3], 'settimana': settimana(p[3]),
                      'tipologia': parti[1], 'municipio': parti[2],
                      'fonte_atto': parti[0],
                      'caratteri': os.path.getsize(NET + '/A2_text/' + n + '.txt')})

if nuovi:
    with open(MAN, 'a', newline='', encoding='utf-8') as fh:
        csv.DictWriter(fh, fieldnames=campi).writerows(nuovi)
print('righe gia nel manifest: %d | aggiunte in coda: %d' % (len(righe), len(nuovi)))

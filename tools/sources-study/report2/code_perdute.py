# Quante registrazioni perdono la coda senza dichiararlo.
# L'idea e' di un lettore: se l'ultimo marcatore di tempo della trascrizione e' molto prima della
# durata dichiarata nel manifest, quella parte di seduta non e' stata trascritta — e nessuna colonna
# lo dice, perche' `quota_ripetuta` misura la ripetizione e non il silenzio, e la confidenza mediana
# non sa niente di cio' che non c'e'. Nel suo lotto un item dichiarava 1:06 e finiva a [47:29].
# Qui la stessa domanda su tutto il corpus, con la soglia dichiarata invece che scelta a occhio.
import csv, os, re, sys, collections

NET = os.environ['QN_NET']
SOGLIA_MIN = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0   # minuti di scarto per contare

def minuti(hm):
    try:
        h, m = hm.split(':'); return int(h) * 60 + int(m)
    except Exception:
        return None

righe = list(csv.DictReader(open(NET + '/report2/manifest_video_rtv.csv', encoding='utf-8')))
rx = re.compile(r'\[(\d+):(\d\d)\]')
persi = []; senza = 0; ok = 0
for r in righe:
    p = NET + '/video/' + (r.get('file') or '')
    d = minuti(r.get('durata_hm') or '')
    if not r.get('file') or not os.path.exists(p) or d is None: senza += 1; continue
    ultimo = 0
    for m in rx.finditer(open(p, encoding='utf-8', errors='replace').read()):
        ultimo = max(ultimo, int(m.group(1)) + int(m.group(2)) / 60)
    scarto = d - ultimo
    if scarto >= SOGLIA_MIN: persi.append((r['item_id'], d, round(ultimo, 1), round(scarto, 1),
                                           r.get('quota_ripetuta') or '', r.get('lacuna') or ''))
    else: ok += 1

print('registrazioni esaminate: %d (saltate %d)' % (len(righe) - senza, senza))
print('con l\'ultimo marcatore almeno %.0f minuti prima della durata dichiarata: %d (%.1f%%)'
      % (SOGLIA_MIN, len(persi), 100 * len(persi) / max(len(righe) - senza, 1)))
dichiarate = sum(1 for x in persi if x[5].strip())
print('di queste, con la colonna `lacuna` compilata: %d' % dichiarate)
q = [x for x in persi if x[4] and x[4] not in ('0', '0.0') and float(x[4]) > 0.10]
print('di queste, gia\' segnalate dalla soglia sulla ripetizione: %d' % len(q))
print('\nle venti con lo scarto piu\' grande (item, durata, ultimo marcatore, scarto in minuti):')
for x in sorted(persi, key=lambda y: -y[3])[:20]:
    print('  %-8s durata %4d   ultimo %6.1f   scarto %5.1f   quota_ripetuta %-6s %s'
          % (x[0], x[1], x[2], x[3], x[4] or '-', 'lacuna dichiarata' if x[5].strip() else ''))
print('\nLo scarto non e\' sempre perdita: una seduta puo\' chiudere prima della fine del file, ed e\'')
print('il caso piu\' comune. Serve a dire **dove guardare**, non a contare i minuti persi.')

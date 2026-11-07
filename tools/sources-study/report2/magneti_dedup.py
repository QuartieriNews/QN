# Le righe scritte che attirano molti accostamenti sbagliano di piu'? Sembrava di si', e non regge.
#
# L'idea: una riga scritta e' un **documento**; se quel documento tocca dieci argomenti, dieci cose
# dette in aula gli somigliano per data e luogo e nessuna e' lo stesso fatto. Misurata sui giudizi
# del primo audit dava una scala pulita — 80% / 75% / 50% / 21% di accostamenti giusti per fasce
# crescenti — ma quei giudizi erano stati incrociati con un file di coppie **mal chiavato**
# (STATO §105): la scala era un artefatto dell'incrocio.
#
# Rifatta sui giudizi del rigiudizio, che sono legati alle coppie giuste, la scala sparisce: dentro
# la stessa forza di accostamento la differenza non e' stabilita (forti: 0 su 3 contro 14 su 20,
# tre casi; deboli: 0 su 18 contro 5 su 38, p = 0,16). Resta vero che **nessuno** dei 21
# accostamenti verso quelle righe e' stato giudicato lo stesso fatto, ma sono quasi tutti deboli, e
# i deboli sbagliano comunque nove volte su dieci: il conto complessivo (p = 0,002) misura la
# composizione, non l'effetto.
#
# Il programma resta perche' la domanda resta, e perche' su un campione piu' grande si rifa' in un
# minuto. Quello che **e'** stabilito sta nel rapporto §7 punto 8, e non viene da qui: cinque dei
# diciannove gemelli veri trovati dal rigiudizio sono invisibili sulle sintesi e si vedono solo
# aprendo il testo dell'atto.
import csv, collections, os
from math import comb

NET = os.environ['QN_NET']
coppie = list(csv.DictReader(open(NET + '/report2/coppie_parlato_scritto.csv', encoding='utf-8')))
quante = collections.Counter(c['scritta'] for c in coppie)
forza = {(c['parlata'], c['scritta']): c['forza'] for c in coppie}

GIUDIZI = NET + '/report2/out/AUDIT3_rigiudizio.csv'   # il solo insieme legato alle coppie giuste
giudicati = []
for r in csv.DictReader(open(GIUDIZI, encoding='utf-8')):
    k = (r['id_parlata'], r['id_scritta'])
    if k in forza:
        giudicati.append((quante[r['id_scritta']], forza[k], r['giudizio'].strip() == 'stesso fatto'))

def fascia(n): return '1-2' if n < 3 else '3-4' if n < 5 else '5-9' if n < 10 else "10 o piu'"

print('accostamenti giudicati e ritrovati nel file delle coppie: %d' % len(giudicati))
for sel, eti in ((lambda f: f == 'forte', 'forti'), (lambda f: f == 'debole', 'deboli')):
    t = collections.defaultdict(lambda: [0, 0])
    for n, f, vero in giudicati:
        if not sel(f): continue
        t[fascia(n)][0] += 1; t[fascia(n)][1] += vero
    print('\naccostamenti %s, per quanti ne attira la riga scritta:' % eti)
    for k in ('1-2', '3-4', '5-9', "10 o piu'"):
        n, v = t[k]
        if n: print('  %-10s %2d giudicati, %2d stesso fatto  (%.0f%%)' % (k, n, v, 100 * v / n))

def fisher(a, b, c, d):
    n = a + b + c + d
    oss = comb(a + b, a) * comb(c + d, c) / comb(n, a + c); tot = 0.0
    for x in range(0, min(a + b, a + c) + 1):
        y = a + b - x; z = a + c - x; w = c + d - z
        if y < 0 or z < 0 or w < 0: continue
        q = comb(a + b, x) * comb(c + d, z) / comb(n, a + c)
        if q <= oss + 1e-12: tot += q
    return tot

print('\nconfronto dentro la stessa forza (10 o piu\' contro il resto):')
for f in ('forte', 'debole'):
    s = [g for g in giudicati if g[1] == f]
    m = [g for g in s if g[0] >= 10]; nm = [g for g in s if g[0] < 10]
    if not m or not nm: continue
    a = sum(1 for g in m if g[2]); c = sum(1 for g in nm if g[2])
    print('  %-7s  %d su %d  contro  %d su %d   Fisher p = %.3f'
          % (f, a, len(m), c, len(nm), fisher(a, len(m) - a, c, len(nm) - c)))
print('\nNessuna delle due differenze e\' stabilita: la scala vista sul primo audit era un artefatto.')

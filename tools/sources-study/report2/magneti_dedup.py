# Dove sbaglia la deduplicazione: non a caso, ma sulle righe scritte che attirano molti
# accostamenti. Una riga scritta e' un **documento**; se quel documento tocca dieci argomenti,
# dieci cose dette in aula gli somigliano per data e luogo e nessuna e' lo stesso fatto. Il
# programma incrocia gli accostamenti con i giudizi dell'audit e stampa la precisione per classe.
# Non usa una soglia scelta a mano: mostra l'andamento per fasce, che e' monotono.
#
# ATTENZIONE, misura non ancora valida: i giudizi dell'audit sono stati dati su un campione in cui
# gli accostamenti mostrati erano in parte quelli di un'altra riga — il file delle coppie era
# scritto con gli identificativi posizionali mentre il database usa quelli del registro (STATO
# §105). Il programma e' corretto e girera' sui dati corretti; i numeri che stampa oggi non vanno
# nel rapporto finche' i casi toccati non sono rigiudicati sul campione rifatto.
import csv, collections, os

N = os.environ['QN_NET']
coppie = list(csv.DictReader(open(N + '/report2/coppie_parlato_scritto.csv', encoding='utf-8')))
quante = collections.Counter(c['scritta'] for c in coppie)
forza = {(c['parlata'], c['scritta']): c['forza'] for c in coppie}

GIUDIZI = N + '/report2/log/_r2/giudiziA.tsv'   # primo audit: caso, parlata, scritta, verdetto, prova
giudicati = []
for riga in open(GIUDIZI, encoding='utf-8'):
    c = riga.rstrip('\n').split('\t')
    if len(c) < 4 or forza.get((c[1], c[2])) != 'forte': continue
    giudicati.append((quante[c[2]], c[3].strip() == 'stesso fatto'))

def fascia(n): return '1-2' if n < 3 else '3-4' if n < 5 else '5-9' if n < 10 else '10 o piu\''

print('accostamenti totali: %d verso %d righe scritte distinte; i forti sono %d'
      % (len(coppie), len(quante), sum(1 for c in coppie if c['forza'] == 'forte')))
print('\nprecisione degli accostamenti forti, per quanti accostamenti attira la riga scritta')
print('(giudizi del primo audit, %d coppie forti giudicate)' % len(giudicati))
t = collections.defaultdict(lambda: [0, 0])
for n, vero in giudicati:
    t[fascia(n)][0] += 1
    t[fascia(n)][1] += vero
for k in ('1-2', '3-4', '5-9', "10 o piu'"):
    n, v = t[k]
    print('  %-10s %2d giudicate  %2d stesso fatto  %s' % (k, n, v, ('%.0f%%' % (100 * v / n)) if n else '-'))

soglia = 10
magneti = {k for k, v in quante.items() if v >= soglia}
forti = [c for c in coppie if c['forza'] == 'forte']
print('\nrighe scritte con %d o piu\' accostamenti: %d (%.1f%% di quelle accostate), '
      'assorbono %d accostamenti su %d e %d dei %d forti'
      % (soglia, len(magneti), 100 * len(magneti) / len(quante),
         sum(quante[k] for k in magneti), len(coppie),
         sum(1 for c in forti if c['scritta'] in magneti), len(forti)))

righe = {r['id']: r for r in csv.DictReader(open(N + '/report1/db/notizie_candidate.csv', encoding='utf-8'))}
def classe(r):
    d, u = (int(x) for x in (r['gemelli_scritti'] or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')
per_parlata = collections.defaultdict(list)
for c in coppie: per_parlata[c['parlata']].append(c)
for cl, etichetta in (('U', 'incerte'), ('D', 'date per non nuove')):
    ids = [i for i, r in righe.items() if r['fonte'] in ('A3', 'A4') and classe(r) == cl]
    solo = [i for i in ids if per_parlata.get(i) and all(c['scritta'] in magneti for c in per_parlata[i]
                                                         if cl == 'U' or c['forza'] == 'forte')]
    print('candidate %-18s %d, di cui %d (%.0f%%) solo per accostamenti a quelle righe'
          % (etichetta, len(ids), len(solo), 100 * len(solo) / len(ids) if ids else 0))

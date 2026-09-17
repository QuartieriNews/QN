# Le registrazioni pubblicate due volte, e quanto pesano sul numero principale.
# La regola che sembra ovvia — stesso titolo e stessa data — qui e' sbagliata: le registrazioni
# YouTube di piu' commissioni dello stesso giorno portano tutte il titolo generico «Commissione
# municipale del <data>», e quella regola ne accorpa 34 gruppi che sono sedute diverse. Il doppione
# vero si riconosce dal contenuto: due documenti le cui candidate hanno **lo stesso insieme di
# titoli**. Il programma stampa entrambe le misure, perche' la differenza fra le due e' il punto.
import csv, collections, os

N = os.environ['QN_NET']
righe = list(csv.DictReader(open(N + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
docs = {d['id']: d for d in csv.DictReader(open(N + '/report1/db/documenti.csv', encoding='utf-8'))}
PARLATO = {'A3', 'A4'}

per_doc = collections.defaultdict(set)
for r in righe:
    if r['fonte'] in PARLATO:
        per_doc[r['documento_id']].add(r['titolo'])

falsi = collections.defaultdict(list)
for d in docs.values():
    if d['fonte'] in PARLATO:
        falsi[(d['titolo'], d['data_pubblicazione'], d['municipi_meta'])].append(d['id'])
print('regola titolo+data+municipio: %d gruppi (la maggior parte sono sedute diverse)'
      % sum(1 for v in falsi.values() if len(v) > 1))

gruppi = collections.defaultdict(list)
for d, titoli in per_doc.items():
    if titoli: gruppi[frozenset(titoli)].append(d)
doppioni = sorted((sorted(v), len(k)) for k, v in gruppi.items() if len(v) > 1)
print('regola sull\'insieme dei titoli: %d gruppi' % len(doppioni))
scartati = set()
for ids, n in doppioni:
    print('  %s  %d candidate  %s' % (', '.join(ids), n, docs[ids[0]]['titolo'][:60]))
    for i in ids[1:]:
        print('     doppione: %s (%s)' % (i, docs[i]['url'].rsplit('/', 1)[-1]))
        scartati.add(i)

def classe(v):
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

def quota(titolo, rs):
    c = collections.Counter(classe(r['gemelli_scritti']) for r in rs)
    n = sum(c.values())
    if not n: return
    print('%-26s N=%d  S=%d U=%d D=%d  ->  [%.1f%% , %.1f%%]'
          % (titolo, n, c['S'], c['U'], c['D'], 100 * c['S'] / n, 100 * (c['S'] + c['U']) / n))

parl = [r for r in righe if r['fonte'] in PARLATO]
print()
quota('con i doppioni', parl)
quota('senza i doppioni', [r for r in parl if r['documento_id'] not in scartati])
print('righe in eccesso: %d su %d (%.1f%%)'
      % (sum(1 for r in parl if r['documento_id'] in scartati), len(parl),
         100 * sum(1 for r in parl if r['documento_id'] in scartati) / len(parl)))

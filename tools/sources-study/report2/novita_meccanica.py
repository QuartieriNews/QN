# La quota di novita' del parlato misurata dal confronto, non dal giudizio del lettore, e nella
# forma che il controllo C3 impone: un intervallo, non un punto, e solo parlato-contro-scritto.
#   S = nessun gemello fra le righe scritte           -> nuova con certezza
#   U = nessun duplicato ma almeno un dubbio          -> incerta
#   D = almeno un duplicato con una riga scritta      -> non nuova
# Quota di novita' = [ S/N , (S+U)/N ].
#
# Il conteggio viene dalle colonne `gemelli_scritti`, che `build_db.py` calcola provando tutte le
# coppie parlato-scritto. **Non** si ricava da `gemello_id`: quella e' la catena della
# deduplicazione, che consuma le righe (una riga gia' legata esce dai confronti successivi) e
# quindi non risponde alla domanda "questa cosa detta sta scritta da qualche parte". Misurato: la
# catena dava S=480 su 883, il confronto esaustivo ne da' molti meno. La differenza fra le due
# righe qui sotto e' il prezzo di quella confusione, e va lasciata in vista.
import csv, os, collections

D = os.environ['QN_NET'] + '/report1/db'
righe = list(csv.DictReader(open(D + '/notizie_candidate.csv', encoding='utf-8')))
PARLATO = {'A3', 'A4'}

def classe(v):
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

manifest = {}
for mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
    p = os.environ['QN_NET'] + '/report2/' + mf
    if os.path.exists(p):
        for m in csv.DictReader(open(p, encoding='utf-8')):
            manifest[m['item_id']] = m.get('origine_trascrizione', 'didascalie YouTube')

def stampa(titolo, conteggio):
    N = sum(conteggio.values())
    if not N: return
    S, U, Dd = conteggio['S'], conteggio['U'], conteggio['D']
    print('%s: N=%d  S=%d U=%d D=%d  ->  [%.1f%% , %.1f%%]'
          % (titolo, N, S, U, Dd, 100 * S / N, 100 * (S + U) / N))

parl = [r for r in righe if r['fonte'] in PARLATO]
tutto = collections.Counter(classe(r['gemelli_scritti']) for r in parl)
blocco = collections.Counter(classe(r['gemelli_scritti_blocco']) for r in parl)

print('QUOTA DI NOVITA\', confronto esaustivo parlato-contro-scritto')
stampa('  su tutto il corpus              ', tutto)
stampa('  dentro il blocco (metodo §4.1)  ', blocco)
print()
print('stratificata per origine della trascrizione (C3 §5.2), su tutto il corpus:')
per_origine = collections.defaultdict(collections.Counter)
for r in parl:
    it = r['documento_id'].replace('A4_', 'V4_').replace('A3_', 'V3_')
    per_origine[manifest.get(it, 'ignota')][classe(r['gemelli_scritti'])] += 1
for orig, c in sorted(per_origine.items()):
    stampa('  %-22s' % orig, c)

# Il confronto con la catena, che e' la misura sbagliata, tenuto in vista di proposito.
per_id = {r['id']: r for r in righe}
legami = collections.defaultdict(set)
for r in righe:
    g = r['gemello_id']
    if g in per_id and r['dedup_stato'] in ('duplicato', 'dubbio'):
        legami[r['id']].add((g, r['dedup_stato'])); legami[g].add((r['id'], r['dedup_stato']))
catena = collections.Counter()
for r in parl:
    stati = {s for (a, s) in legami[r['id']] if per_id[a]['fonte'] not in PARLATO}
    catena['D' if 'duplicato' in stati else ('U' if 'dubbio' in stati else 'S')] += 1
print()
stampa('per memoria, la catena della deduplicazione (misura sbagliata)', catena)

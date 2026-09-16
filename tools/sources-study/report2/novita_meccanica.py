# La quota di novita' del parlato misurata dal confronto, non dal giudizio del lettore, e nella
# forma che il controllo C3 impone: un intervallo, non un punto, e solo parlato-contro-scritto.
#   S = nessun gemello fra le righe scritte           -> nuova con certezza
#   U = nessun duplicato ma almeno un dubbio          -> incerta
#   D = almeno un duplicato con una riga scritta      -> non nuova
# Quota di novita' = [ S/N , (S+U)/N ].
# Un gemello fra due registrazioni non conta: la domanda e' che cosa il parlato aggiunge allo
# scritto, non quante volte due sedute dicono la stessa cosa.
import csv, os, collections
D = os.environ['QN_NET'] + '/report1/db'
righe = list(csv.DictReader(open(D + '/notizie_candidate.csv', encoding='utf-8')))
per_id = {r['id']: r for r in righe}
PARLATO = {'A3', 'A4'}

def scritta(r): return r['fonte'] not in PARLATO

# I legami sono diretti (b punta ad a): li rendo simmetrici, perche' la domanda non ha una direzione.
legami = collections.defaultdict(set)
for r in righe:
    g = r['gemello_id']
    if g and g in per_id and r['dedup_stato'] in ('duplicato', 'dubbio'):
        legami[r['id']].add((g, r['dedup_stato']))
        legami[g].add((r['id'], r['dedup_stato']))

conteggio = collections.Counter()
per_origine = collections.defaultdict(collections.Counter)
manifest = {}
for mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
    p = os.environ['QN_NET'] + '/report2/' + mf
    if os.path.exists(p):
        for m in csv.DictReader(open(p, encoding='utf-8')):
            manifest[m['item_id']] = m.get('origine_trascrizione', 'didascalie YouTube')

for r in righe:
    if scritta(r): continue
    stati = {s for (altro, s) in legami[r['id']] if scritta(per_id[altro])}
    cl = 'D' if 'duplicato' in stati else ('U' if 'dubbio' in stati else 'S')
    conteggio[cl] += 1
    # l'origine si ricava dall'item, che e' nel documento_id: A4_007 -> V4_007
    it = r['documento_id'].replace('A4_', 'V4_').replace('A3_', 'V3_')
    per_origine[manifest.get(it, 'ignota')][cl] += 1

N = sum(conteggio.values())
S, U, Dd = conteggio['S'], conteggio['U'], conteggio['D']
print('candidate dal parlato confrontate: %d' % N)
print('  S nessun gemello scritto: %d | U solo dubbi: %d | D almeno un duplicato: %d' % (S, U, Dd))
print('  QUOTA DI NOVITA'"'"': [%.1f%% , %.1f%%]' % (100 * S / N, 100 * (S + U) / N))
print('stratificata per origine della trascrizione (C3 §5.2):')
for orig, c in sorted(per_origine.items()):
    n = sum(c.values())
    if not n: continue
    print('  %-22s N=%3d  novita [%.1f%% , %.1f%%]' % (orig, n, 100 * c['S'] / n, 100 * (c['S'] + c['U']) / n))

# Rilievo 6.3 del controllo C3: un toponimo storpiato dal riconoscimento automatico non trova il
# suo gemello, e la candidata risulta nuova per un errore di trascrizione invece che per un fatto.
# Qui si misura quante candidate «senza gemello scritto» poggiano su un toponimo dichiarato incerto.
import csv, collections, os, json, glob
S = os.environ['QN_NET']
righe = list(csv.DictReader(open(S + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
per_id = {r['id']: r for r in righe}
PARLATO = {'A3', 'A4'}
legami = collections.defaultdict(set)
for r in righe:
    g = r['gemello_id']
    if g and g in per_id and r['dedup_stato'] in ('duplicato', 'dubbio'):
        legami[r['id']].add((g, r['dedup_stato'])); legami[g].add((r['id'], r['dedup_stato']))

# il flag sta nei JSON dei lettori, non nella tabella: lo rileggo da li'
incerto = {}
for f in glob.glob(S + '/report2/out_video/*.json'):
    try: j = json.load(open(f, encoding='utf-8'))
    except Exception: continue
    for k, c in enumerate(j.get('notizie_candidate') or []):
        incerto[(j['item_id'], c.get('titolo', '')[:40])] = (c.get('toponimo_da_verificare', 'no') or 'no').lower() in ('sì', 'si')

c = collections.Counter()
for r in righe:
    if r['fonte'] not in PARLATO: continue
    stati = {s for (a, s) in legami[r['id']] if per_id[a]['fonte'] not in PARLATO}
    cl = 'D' if 'duplicato' in stati else ('U' if 'dubbio' in stati else 'S')
    it = r['documento_id'].replace('A4_', 'V4_').replace('A3_', 'V3_')
    inc = incerto.get((it, r['titolo_anonimizzato'][:40]),
                      (r['toponimo_da_verificare'] or 'no').lower() in ('sì', 'si'))
    c[(cl, 'toponimo incerto' if inc else 'toponimo fermo')] += 1
tot = sum(c.values())
S_inc = c[('S', 'toponimo incerto')]; S_tot = c[('S', 'toponimo incerto')] + c[('S', 'toponimo fermo')]
print('candidate dal parlato: %d' % tot)
for k in sorted(c): print('  %-34s %d' % (' / '.join(k), c[k]))
print()
print('senza alcun gemello scritto: %d, di cui %d (%.1f%%) poggiano su un toponimo dichiarato incerto'
      % (S_tot, S_inc, 100 * S_inc / S_tot))
print('quota di novita certa se si scartano quelle righe: %.1f%% invece di %.1f%%'
      % (100 * (S_tot - S_inc) / tot, 100 * S_tot / tot))

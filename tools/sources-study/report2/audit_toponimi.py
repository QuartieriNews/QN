# Rilievo 6.3 del controllo C3: un toponimo storpiato dal riconoscimento automatico non trova il
# suo gemello, e la candidata risulta nuova per un errore di trascrizione invece che per un fatto.
# Qui si misura quante candidate «senza gemello scritto» poggiano su un toponimo dichiarato incerto.
import csv, collections, os, json, glob
S = os.environ['QN_NET']
righe = list(csv.DictReader(open(S + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
PARLATO = {'A3', 'A4'}

def classe(v):
    """La classe viene dal confronto esaustivo che `build_db.py` scrive in `gemelli_scritti`, non
    dalla catena `gemello_id`: la catena consuma le righe e non risponde alla domanda «questa cosa
    detta sta scritta da qualche parte»."""
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

# il flag sta nei JSON dei lettori, non nella tabella: lo rileggo da li'
incerto = {}; collisioni = []
for f in glob.glob(S + '/report2/out_video/*.json'):
    try: j = json.load(open(f, encoding='utf-8'))
    except Exception: continue
    for k, c in enumerate(j.get('notizie_candidate') or []):
        chiave = (j['item_id'], (c.get('titolo') or '').strip())
        valore = (c.get('toponimo_da_verificare', 'no') or 'no').lower() in ('sì', 'si')
        if chiave in incerto and incerto[chiave] != valore:
            collisioni.append(chiave)   # due candidate con lo stesso titolo nello stesso item e flag diverso
        incerto[chiave] = valore

c = collections.Counter()
for r in righe:
    if r['fonte'] not in PARLATO: continue
    cl = classe(r['gemelli_scritti'])
    it = r['documento_id'].replace('A4_', 'V4_').replace('A3_', 'V3_')
    inc = incerto.get((it, (r['titolo'] or '').strip()),
                      (r['toponimo_da_verificare'] or 'no').lower() in ('sì', 'si'))
    c[(cl, 'toponimo incerto' if inc else 'toponimo fermo')] += 1
tot = sum(c.values())
S_inc = c[('S', 'toponimo incerto')]; S_tot = c[('S', 'toponimo incerto')] + c[('S', 'toponimo fermo')]
print('candidate dal parlato: %d' % tot)
if collisioni:
    print('ATTENZIONE: %d coppie item/titolo con flag discordanti fra candidate omonime (vince l\'ultima letta)' % len(collisioni))
for k in sorted(c): print('  %-34s %d' % (' / '.join(k), c[k]))
print()
if not S_tot or not tot:
    print('senza alcun gemello scritto: %d su %d candidate: quote non definite' % (S_tot, tot))
else:
    print('senza alcun gemello scritto: %d, di cui %d (%.1f%%) poggiano su un toponimo dichiarato incerto'
          % (S_tot, S_inc, 100 * S_inc / S_tot))
    print('quota di novita certa se si scartano quelle righe: %.1f%% invece di %.1f%%'
          % (100 * (S_tot - S_inc) / tot, 100 * S_tot / tot))

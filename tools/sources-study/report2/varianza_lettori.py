# Quanto del campo `novita_rispetto_agli_atti` dipende dal materiale e quanto dal lettore.
# Il campo lo scrive un lettore; la classificazione S/U/D la calcola il confronto. Se la quota
# di `solo dal parlato` varia fra i lotti perche' varia il materiale, le due misure si muovono
# insieme; se varia perche' varia il lettore, divergono. E' il controllo che il C3 (§3.3, §6.1)
# chiede prima di mettere insieme lotti letti con definizioni diverse.
import csv, json, os, collections

NET = os.environ['QN_NET']
righe = list(csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
per_id = {r['id']: r for r in righe}
PARLATO = {'A3', 'A4'}

def classe(r):
    """S/U/D dalle colonne `gemelli_scritti` (confronto esaustivo parlato-contro-scritto di
    build_db.py), come in novita_meccanica.py; la catena `gemello_id` consuma le righe e
    misura un'altra cosa (novita_meccanica.py, in testa)."""
    d, u = (int(x) for x in (r.get('gemelli_scritti') or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

# il giudizio umano sta nei JSON, non nel database
umano = {}
for f in sorted(os.listdir(NET + '/report2/out_video')):
    j = json.load(open(NET + '/report2/out_video/' + f, encoding='utf-8'))
    for c in j.get('notizie_candidate', []):
        umano[(f[:-5], c.get('titolo', '').strip())] = c.get('novita_rispetto_agli_atti', '?')

def lotto(item):
    n = int(item.split('_')[1])
    return item[:3] + str((n - 1) // 12 * 12 + 1).zfill(3)

per_lotto = collections.defaultdict(lambda: collections.Counter())
mancanti = 0
for r in righe:
    if r['fonte'] not in PARLATO: continue
    item = r['documento_id'].replace('A4_', 'V4_').replace('A3_', 'V3_')
    k = (item, r['titolo'].strip())
    u = umano.get(k)
    if u is None:
        mancanti += 1
        continue
    c = per_lotto[lotto(item)]
    c['N'] += 1
    c['umano_solo'] += (u == 'solo dal parlato')
    c['umano_nonver'] += (u == 'non verificabile')
    c[classe(r)] += 1

print('candidate del parlato appaiate al giudizio del lettore: %d (non appaiate: %d)'
      % (sum(c['N'] for c in per_lotto.values()), mancanti))
print()
print('lotto      N   solo dal parlato   non verif.   S meccanico   (S+U)')
for k in sorted(per_lotto):
    c = per_lotto[k]; n = c['N']
    print('%-8s %3d      %5.1f%%          %5.1f%%        %5.1f%%      %5.1f%%'
          % (k, n, 100 * c['umano_solo'] / n, 100 * c['umano_nonver'] / n,
             100 * c['S'] / n, 100 * (c['S'] + c['U']) / n))

def escursioni(chiavi):
    u = [100 * per_lotto[k]['umano_solo'] / per_lotto[k]['N'] for k in chiavi]
    s = [100 * per_lotto[k]['S'] / per_lotto[k]['N'] for k in chiavi]
    return max(u) - min(u), max(s) - min(s)

# Il rapporto fra le due escursioni e' la misura che interessa: la meccanica non sa niente del
# lettore, quindi porta la sola eterogeneita' del materiale. Sopra 1 il lettore aggiunge
# dispersione al materiale, sotto 1 ne toglie.
print()
print('gruppo          lotti   escursione lettore   escursione meccanica   rapporto')
for nome, sel in (('tutti', lambda k: True),
                  ('V3 RomaTV', lambda k: k.startswith('V3')),
                  ('V4 YouTube', lambda k: k.startswith('V4'))):
    ks = [k for k in per_lotto if sel(k)]
    eu, es = escursioni(ks)
    print('%-14s %3d        %5.0f punti          %5.0f punti          %4.2f'
          % (nome, len(ks), eu, es, eu / es))

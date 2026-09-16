# I tre numeri del Report 2 poggiano sulla deduplicazione, e la qualita' della deduplicazione non
# e' mai stata misurata (rilievo C4 §6.4). Questo programma non la misura: prepara il campione che
# un lettore deve giudicare, perche' giudicare se due righe sono lo stesso fatto e' lettura, non
# calcolo.
# Due campioni, perche' i due errori costano cose diverse:
#   - PRECISIONE: coppie che il programma ha unito. Un falso accostamento abbassa la novita'.
#   - RICHIAMO: coppie che il programma NON ha unito ma che condividono data e toponimo. Un
#     accostamento mancato alza la novita', ed e' l'errore che gonfierebbe il numero principale.
import csv, os, random, re, unicodedata, collections

NET = os.environ['QN_NET']
SEME = '2026-06-dedup-audit'
PARLATO = {'A3', 'A4'}

righe = list(csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
per_id = {r['id']: r for r in righe}

def norm(s):
    s = unicodedata.normalize('NFKD', (s or '').lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9 ]', ' ', s).strip()

def toponimi(r):
    out = set()
    for t in (r['luoghi'] or '').split(';'):
        t = norm(t)
        if len(t) > 6 and 'municipio' not in t: out.add(t)
    return out

def giorno(r):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', r['data_fatto'] or '')
    return int(m.group(3)) + 31 * int(m.group(2)) if m else None

# --- precisione: le coppie unite che coinvolgono il parlato
unite = []
for r in righe:
    g = r['gemello_id']
    if r['dedup_stato'] == 'duplicato' and g in per_id:
        if r['fonte'] in PARLATO or per_id[g]['fonte'] in PARLATO:
            unite.append((r['id'], g))

# --- richiamo: coppie non unite, stesso toponimo, date a un giorno
scritte = [r for r in righe if r['fonte'] not in PARLATO]
per_top = collections.defaultdict(list)
for r in scritte:
    for t in toponimi(r): per_top[t].append(r)

legate = set()
for r in righe:
    if r['gemello_id']:
        legate.add(frozenset((r['id'], r['gemello_id'])))

vicine = []
for r in righe:
    if r['fonte'] not in PARLATO: continue
    d = giorno(r)
    if d is None: continue
    for t in toponimi(r):
        for s in per_top.get(t, []):
            ds = giorno(s)
            if ds is None or abs(ds - d) > 1: continue
            if frozenset((r['id'], s['id'])) in legate: continue
            vicine.append((r['id'], s['id'], t))

vicine = sorted(set(vicine))
random.Random(SEME).shuffle(vicine)
camp = vicine[:40]

def riga(rid):
    r = per_id[rid]
    return '  %s [%s, %s, %s] %s\n     luoghi: %s\n     %s' % (
        rid, r['fonte'], r['data_fatto'], r['municipio'] or '-',
        r['titolo_anonimizzato'], r['luoghi'], (r['sintesi'] or '')[:220])

out = [ '# Campione per l\'audit della deduplicazione',
        '',
        'Seme `%s`. Per ogni coppia scrivi **stesso fatto** o **fatti diversi**, e una riga di' % SEME,
        'motivo. Non e\' una domanda di somiglianza: due righe sono lo stesso fatto se un lettore',
        'che le trovasse entrambe direbbe che la seconda non aggiunge niente alla prima.',
        '',
        '## A. Coppie che il programma ha unito (`duplicato`): %d, tutte' % len(unite),
        '', 'Un errore qui abbassa la novita\'.', '']
for a, b in unite:
    out += ['### A%d' % (unite.index((a, b)) + 1), riga(a), riga(b), '']
out += ['## B. Coppie che il programma NON ha unito, stesso toponimo e date a un giorno: %d su %d'
        % (len(camp), len(vicine)), '',
        'Un errore qui **alza** la novita\', ed e\' quello che gonfierebbe il numero principale.', '']
for i, (a, b, t) in enumerate(camp, 1):
    out += ['### B%d — toponimo condiviso: %s' % (i, t), riga(a), riga(b), '']

open(NET + '/report2/campione_dedup.md', 'w', encoding='utf-8').write('\n'.join(out))
print('coppie unite che toccano il parlato: %d' % len(unite))
print('coppie non unite con stesso toponimo e date a un giorno: %d (campionate %d)'
      % (len(vicine), len(camp)))
print('scritto report2/campione_dedup.md')

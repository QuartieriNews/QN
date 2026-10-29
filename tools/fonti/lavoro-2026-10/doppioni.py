import sys, re, unicodedata, collections, difflib, itertools
import openpyxl
from openpyxl.styles import Font
UNICO = sys.argv[1]
wb = openpyxl.load_workbook(UNICO); ws = wb['Eventi unificati']; h = [c.value for c in ws[1]]; g = lambda r, k: r[h.index(k)]
rows = [list(r) for r in ws.iter_rows(min_row=2, values_only=True)]
STOP = set('a al alla alle allo ai agli di del della delle dello dei degli da dal dalla dalle in nel nella nelle con su per tra fra e ed il lo la le i gli un una uno the of and at teatro roma edizione spettacolo concerto evento mostra festival live presentazione libro visita guidata'.split())
def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9 ]+', ' ', s); return [w for w in s.split() if w not in STOP and len(w) > 2]
def day(v): return str(v or '')[:10]
def src(r): return g(r, 'fonte').split(':')[0].split(' (')[0].replace(' → sorgente', '')
recs = []
for idx, r in enumerate(rows):
    t = norm(g(r, 'nome')); recs.append({'i': idx, 'src': src(r), 'tok': set(t), 'title': ' '.join(t), 'day': day(g(r, 'inizio')), 'end': day(g(r, 'fine')), 'venue': set(norm(g(r, 'luogo'))), 'url': g(r, 'url'), 'nome': g(r, 'nome')})
def sim(a, b):
    if not a['tok'] or not b['tok']: return 0
    j = len(a['tok'] & b['tok']) / len(a['tok'] | b['tok'])
    d = difflib.SequenceMatcher(None, a['title'], b['title']).ratio()
    return max(j, d)
def dates_overlap(a, b):
    if not a['day'] or not b['day']: return None
    a0, a1 = a['day'], a['end'] or a['day']; b0, b1 = b['day'], b['end'] or b['day']
    return a0 <= b1 and b0 <= a1
# indice per giorno di inizio e per parole del titolo
by_tok = collections.defaultdict(set)
for r in recs:
    for w in r['tok']: by_tok[w].add(r['i'])
pairs = {}
for a in recs:
    cand = set()
    for w in a['tok']:
        if len(by_tok[w]) < 200: cand |= by_tok[w]
    for j in cand:
        if j <= a['i']: continue
        b = recs[j]; s = sim(a, b); ov = dates_overlap(a, b); vs = len(a['venue'] & b['venue']) / max(1, len(a['venue'] | b['venue'])) if a['venue'] and b['venue'] else 0
        same_url = a['url'] and a['url'] == b['url']
        if (s >= 0.85 and (ov or ov is None)) or (s >= 0.72 and ov and a['day'] == b['day'] and vs >= 0.5):
            kind = 'titolo quasi identico + date compatibili' if s >= 0.85 else 'titolo simile + stessa data + stesso luogo'
            pairs[(a['i'], j)] = (round(s, 2), kind)
# gruppi (unione)
parent = list(range(len(recs)))
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
for (i, j) in pairs: parent[find(i)] = find(j)
groups = collections.defaultdict(list)
for r in recs: groups[find(r['i'])].append(r['i'])
groups = {k: v for k, v in groups.items() if len(v) > 1}
inter = {k: v for k, v in groups.items() if len(set(recs[i]['src'] for i in v)) > 1}
intra = {k: v for k, v in groups.items() if len(set(recs[i]['src'] for i in v)) == 1}
print('coppie', len(pairs), 'gruppi', len(groups), 'tra fonti', len(inter), 'dentro una fonte', len(intra))
print('righe coinvolte', sum(len(v) for v in groups.values()), 'righe in eccesso (doppioni)', sum(len(v) - 1 for v in groups.values()))
comb = collections.Counter(tuple(sorted(set(recs[i]['src'] for i in v))) for v in inter.values()); print('combinazioni tra fonti:', comb.most_common())
intra_src = collections.Counter(recs[v[0]]['src'] for v in intra.values()); print('doppioni dentro una fonte:', intra_src.most_common())
# colonna gruppo + tab
if 'gruppo_doppione' not in h:
    ws.cell(1, len(h) + 1, 'gruppo_doppione').font = Font(bold=True); ws.cell(1, len(h) + 2, 'doppione_di').font = Font(bold=True); h += ['gruppo_doppione', 'doppione_di']
gid = {}
for n, (k, v) in enumerate(sorted(groups.items(), key=lambda kv: min(kv[1])), 1):
    for i in v: gid[i] = n
for r in recs:
    i = r['i']; ws.cell(i + 2, h.index('gruppo_doppione') + 1, gid.get(i))
    ws.cell(i + 2, h.index('doppione_di') + 1, '; '.join(sorted(set(recs[j]['src'] for j in groups[find(i)] if j != i))) if i in gid else None)
    if i not in gid: ws.cell(i + 2, h.index('gruppo_doppione') + 1, None)
if 'Doppioni' in wb.sheetnames: del wb['Doppioni']
wd = wb.create_sheet('Doppioni', 2); wd.append(['gruppo', 'tipo', 'fonti', 'n_righe', 'fonte', 'nome', 'inizio', 'fine', 'luogo', 'url', 'somiglianza_max', 'criterio'])
for c in wd[1]: c.font = Font(bold=True)
for k, v in sorted(groups.items(), key=lambda kv: min(kv[1])):
    srcs = sorted(set(recs[i]['src'] for i in v)); tipo = 'tra fonti' if len(srcs) > 1 else 'dentro una fonte'
    for i in v:
        best = max([pairs.get((min(i, j), max(i, j)), (0, ''))[0] for j in v if j != i]); crit = next((pairs[(min(i, j), max(i, j))][1] for j in v if (min(i, j), max(i, j)) in pairs), '')
        r = rows[i]; wd.append([gid[i], tipo, ' + '.join(srcs), len(v), g(r, 'fonte'), g(r, 'nome'), g(r, 'inizio'), g(r, 'fine'), g(r, 'luogo'), g(r, 'url'), best, crit])
for col, w in zip('ABCDEFGHIJKL', (8, 16, 34, 8, 30, 50, 20, 20, 32, 50, 10, 40)): wd.column_dimensions[col].width = w
wb.save(UNICO)
# esempi
import random; random.seed(2)
for k, v in random.sample(list(inter.items()), min(10, len(inter))):
    print('--'); [print('  ', recs[i]['src'][:12], '|', (recs[i]['nome'] or '')[:55], '|', recs[i]['day'], '|', (g(rows[i], 'luogo') or '')[:30]) for i in v]

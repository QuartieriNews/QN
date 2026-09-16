# Quanto della novita' che misuriamo e' la convenzione di verbalizzazione dell'organo?
# L'ipotesi viene da un lettore: fra organi diversi il fattore non e' l'oggetto della seduta ma
# **come quell'organo verbalizza** — ci sono organi quasi stenografici e organi il cui verbale
# dichiara che «la videoregistrazione sostituisce la trascrizione degli interventi». Se e' vero,
# dove i verbali sono piu' densi la quota di novita' dev'essere piu' bassa.
#
# Si misura con due grandezze indipendenti dal giudizio del lettore, per non ereditare le tre
# definizioni del campo `novita_rispetto_agli_atti`:
#   x = quota di verbali (tipologia MMV) sugli atti di quel Municipio
#   y = quota di candidate del parlato senza alcun gemello scritto (classe S)
# e si stampa anche la versione con il campo del lettore, che e' meno affidabile ma piu' diretta.
import csv, collections, json, glob, os, re, statistics

NET = os.environ['QN_NET']
atti = list(csv.DictReader(open(NET + '/report2/snapshot/confronto_atti.csv', encoding='utf-8')))
verbali = collections.Counter(r['municipio'] for r in atti if r['tipologia'] == 'MMV')
tutti = collections.Counter(r['municipio'] for r in atti)

righe = [r for r in csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8'))
         if r['fonte'] in ('A3', 'A4')]
def classe(r):
    d, u = (int(x) for x in (r['gemelli_scritti'] or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')
per = collections.defaultdict(collections.Counter)
for r in righe:
    m = (r['municipio'] or '').split(';')[0].strip()
    if m: per[m][classe(r)] += 1

lettore = collections.Counter(); lettore_tot = collections.Counter()
for f in glob.glob(NET + '/report2/out_video/V*.json'):
    j = json.load(open(f, encoding='utf-8'))
    m = re.search(r'Municipio\s+([IVX]+)', j.get('territorio') or '')
    if not m: continue
    for c in j.get('notizie_candidate') or []:
        lettore_tot[m.group(1)] += 1
        if c.get('novita_rispetto_agli_atti') == 'solo dal parlato': lettore[m.group(1)] += 1

MIN_CAND, MIN_ATTI = 25, 20
print('%-6s %8s %7s %7s %7s %9s' % ('mun', 'verbali', 'atti', 'cand', 'S%', 'lettore%'))
dati = []
for m, c in sorted(per.items(), key=lambda x: -sum(x[1].values())):
    n = sum(c.values())
    if n < MIN_CAND or tutti.get(m, 0) < MIN_ATTI: continue
    s = 100 * c['S'] / n
    l = 100 * lettore[m] / lettore_tot[m] if lettore_tot.get(m) else float('nan')
    dati.append((verbali.get(m, 0) / tutti[m], s, l))
    print('%-6s %8d %7d %7d %7.1f %9.1f' % (m, verbali.get(m, 0), tutti[m], n, s, l))

def erre(xs, ys):
    xs = [x for x, y in zip(xs, ys) if y == y]; ys = [y for y in ys if y == y]
    if len(xs) < 3: return float('nan')
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = (sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)) ** 0.5
    return num / den if den else float('nan')

xs = [d[0] for d in dati]
print('\nquota di verbali sugli atti contro quota di novita\':')
print('  misura meccanica (classe S):  r = %.2f su %d Municipi' % (erre(xs, [d[1] for d in dati]), len(dati)))
print('  campo del lettore:            r = %.2f' % erre(xs, [d[2] for d in dati]))
print("\nSegno atteso: negativo. Dieci Municipi non sono una dimostrazione, e la densita' di verbali")
print("e' un indicatore grossolano della convenzione: e' un segnale, e come tale va dichiarato.")

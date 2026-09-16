# L'audit ha trovato che dal lato parlato l'unita' di confronto e' il fatto e dal lato scritto il
# documento: ogni verbale produce **una riga**, la cui sintesi racconta un punto solo dell'ordine del
# giorno. Un fatto che nel verbale e' il terzo punto non puo' essere riconosciuto dal confronto fra
# righe, per costruzione.
# Il testo integrale degli atti ce l'abbiamo. Questo programma non deduplica e non tocca i numeri:
# misura **quante candidate date per nuove compaiono comunque nel testo di un atto**, cercandole
# dove hanno senso — stesso Municipio, pochi giorni di distanza — con il toponimo e una parola di
# contenuto. E' un limite superiore agli accostamenti mancati per l'asimmetria, non una nuova
# deduplicazione: un toponimo che compare in un atto non prova che sia lo stesso fatto.
import csv, os, re, sys, unicodedata, collections, datetime

NET = os.environ['QN_NET']
FINESTRA = int(sys.argv[1]) if len(sys.argv) > 1 else 3
PARLATO = {'A3', 'A4'}

def norm(s):
    s = unicodedata.normalize('NFKD', (s or '').lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s)

righe = list(csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8')))
man = {r['name']: r for r in csv.DictReader(open(NET + '/report2/manifest_report2.csv', encoding='utf-8'))}

def data(s):
    try: return datetime.date.fromisoformat((s or '')[:10])
    except ValueError: return None

# gli atti, con il testo normalizzato una volta sola
atti = []
for f in sorted(os.listdir(NET + '/A2_text')):
    n = f[:-4]; m = man.get(n)
    if not m: continue
    d = None
    mm = re.match(r'(\d{2})/(\d{2})/(\d{4})', m['data'] or '')
    if mm: d = datetime.date(int(mm.group(3)), int(mm.group(2)), int(mm.group(1)))
    atti.append((n, m['municipio'], d,
                 norm(open(NET + '/A2_text/' + f, encoding='utf-8', errors='replace').read())))

def classe(v):
    dd, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if dd else ('U' if u else 'S')

esse = [r for r in righe if r['fonte'] in PARLATO and classe(r['gemelli_scritti']) == 'S']
print('candidate date per nuove: %d | atti con testo e manifest: %d | finestra ±%d giorni'
      % (len(esse), len(atti), FINESTRA))

trovate, senza_toponimo, esempi = 0, 0, []
for r in esse:
    top = [norm(t) for t in (r['luoghi'] or '').split(';')]
    top = [t.strip() for t in top if len(t.strip()) > 8 and 'municipio' not in t]
    if not top:
        senza_toponimo += 1; continue
    d = data(r['data_fatto']); muns = {m.strip() for m in (r['municipio'] or '').split(';') if m.strip()}
    chiave = {w for w in norm(r['titolo_anonimizzato']).split() if len(w) > 6}
    hit = None
    for n, mun, da, testo in atti:
        if muns and mun and mun not in muns: continue
        if d and da and abs((da - d).days) > FINESTRA: continue
        if not any(t in testo for t in top): continue
        if chiave and not (chiave & set(testo.split())): continue
        hit = n; break
    if hit:
        trovate += 1
        if len(esempi) < 8: esempi.append((r['id'], r['titolo_anonimizzato'][:58], hit))

confrontabili = len(esse) - senza_toponimo
print('  senza un toponimo cercabile: %d (non misurabili cosi\')' % senza_toponimo)
print('  con toponimo **e** una parola del titolo dentro il testo di un atto vicino: %d su %d (%.1f%%)'
      % (trovate, confrontabili, 100 * trovate / confrontabili if confrontabili else 0))
print('\nesempi (il testo dell\'atto le contiene, il confronto fra righe non le ha viste):')
for i, t, n in esempi: print('   %s  %-58s -> %s' % (i, t, n))

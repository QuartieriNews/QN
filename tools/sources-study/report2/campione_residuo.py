# Il residuo non si misura con il detector che ha fatto il lavoro: allargare una regex trova
# sempre qualcosa in piu', e «zero risultati» non e' mai la prova di aver finito. Qui si estrae un
# campione casuale che una persona legge contro la fonte, e il numero che ne esce e' la misura.
# Seme fisso: lo stesso comando deve ritrovare lo stesso campione, o la misura non si rifa'.
import collections, csv, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lotti_ripristino as L

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
SEME = os.environ.get('SEME_RESIDUO', 'residuo-2026-09-17')
N = int(os.environ.get('N_RESIDUO', 50))


def main():
    documenti = list(csv.DictReader(open(DB + '/documenti.csv', encoding='utf-8')))
    notizie = list(csv.DictReader(open(DB + '/notizie_candidate.csv', encoding='utf-8')))
    percorso = L.sorgenti(documenti)

    pool = []
    for n in notizie:
        if not (n.get('sintesi') or n.get('titolo')):
            continue
        pool.append({'riga': n['id'], 'tabella': 'notizie', 'fonte': n['fonte'],
                     'documento': n['documento_id'], 'titolo': n.get('titolo', ''),
                     'sintesi': (n.get('sintesi') or '')[:600],
                     'evidenza_locale': n.get('evidenza_locale', ''),
                     'sorgente': percorso.get(n['documento_id'], '')})
    # Stratificato per fonte: un campione semplice su 50 righe lascerebbe fuori le fonti piccole,
    # e il residuo non e' lo stesso dappertutto - gli atti e il parlato sbagliano in modi diversi.
    per_fonte = collections.defaultdict(list)
    for r in pool:
        per_fonte[r['fonte']].append(r)
    totale = len(pool)
    quote = {f: N * len(v) / totale for f, v in per_fonte.items()}
    assegnate = {f: int(q) for f, q in quote.items()}
    resto = sorted(quote, key=lambda f: quote[f] - assegnate[f], reverse=True)
    i = 0
    while sum(assegnate.values()) < N and resto:
        assegnate[resto[i % len(resto)]] += 1
        i += 1
    rng = random.Random(SEME)
    campione = []
    for f in sorted(per_fonte):
        k = min(assegnate.get(f, 0), len(per_fonte[f]))
        if k:
            campione += rng.sample(sorted(per_fonte[f], key=lambda r: r['riga']), k)
    campione.sort(key=lambda r: (r['fonte'], r['riga']))

    campi = ['riga', 'tabella', 'fonte', 'documento', 'sorgente', 'titolo', 'sintesi',
             'evidenza_locale']
    fuori = DB + '/campione_residuo.csv'
    with open(fuori, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, campi, extrasaction='ignore')
        w.writeheader(); w.writerows(campione)
    print('campione: %d righe su %d, seme %r -> %s' % (len(campione), totale, SEME, fuori))
    print('per fonte: %s' % dict(collections.Counter(r['fonte'] for r in campione).most_common()))
    senza = [r for r in campione if not r['sorgente']]
    if senza:
        print('senza fonte locale: %d (%s) — si contano come non verificabili, non si sostituiscono'
              % (len(senza), ', '.join(r['riga'] for r in senza[:8])))


if __name__ == '__main__':
    main()

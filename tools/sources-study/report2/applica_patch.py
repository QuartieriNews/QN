# Applica al database i patch della passata di ripristino (DEC-105).
# I lettori consegnano patch invece di scrivere sui CSV: due che scrivono lo stesso file lo
# corrompono, e un passo unico si rivede. Qui si controlla tutto prima di toccare qualcosa.
import csv, glob, os, re, shutil, sys, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
PATCH = NET + '/report2/ripristino'
TABELLE = {'notizie': 'notizie_candidate.csv', 'documenti': 'documenti.csv'}

# La sostituzione lascia residui di spaziatura ("Alfonsi , con"): il lettore corregge il nome,
# la punteggiatura la sistema una regola, non una rilettura.
def ripulisci(s):
    s = re.sub(r"\s+([,;.:!?])", r"\1", s)
    s = re.sub(r"([«(])\s+", r"\1", s)
    s = re.sub(r"\s+([»)])", r"\1", s)
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def carica_patch():
    righe, visti = [], {}
    for f in sorted(glob.glob(PATCH + '/patch_*.csv')):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            r['_file'] = os.path.basename(f)
            chiave = (r['riga'], r['campo'])
            if chiave in visti and visti[chiave] != r.get('valore_nuovo', ''):
                print('CONFLITTO su %s %s: %s e %s divergono'
                      % (r['riga'], r['campo'], visti[chiave][:40], r.get('valore_nuovo', '')[:40]))
                sys.exit(1)
            visti[chiave] = r.get('valore_nuovo', '')
            righe.append(r)
    return righe


def main():
    patch = carica_patch()
    esiti = collections.Counter(r['esito'] for r in patch)
    per_tab = collections.defaultdict(list)
    for r in patch:
        per_tab[r['tabella']].append(r)

    fuori = [r for r in patch if r['esito'] == 'fuori_seduta']
    applicati = mancanti = 0
    for tab, elenco in per_tab.items():
        percorso = DB + '/' + TABELLE[tab]
        righe = list(csv.DictReader(open(percorso, encoding='utf-8')))
        campi = list(righe[0])
        indice = {r['id']: r for r in righe}
        for p in elenco:
            r = indice.get(p['riga'])
            if r is None:
                print('riga assente:', p['riga'], p['_file']); mancanti += 1; continue
            if p['esito'] == 'ripristinato' and p.get('valore_nuovo'):
                r[p['campo']] = ripulisci(p['valore_nuovo']); applicati += 1
            # La ragione si conserva sempre, non solo quando il nome resta fuori: un'attribuzione
            # fatta con un dubbio dichiarato deve portarsi dietro il dubbio, o il dubbio sparisce.
            nota = (p.get('ragione') or '').strip()
            if nota and 'note' in campi:
                r['note'] = ((r.get('note') or '') + ' | ' if r.get('note') else '') + \
                    ('%s: %s' % (p['esito'], nota))
            # I primi patch non avevano la colonna del flag: la ragione lo dice a parole.
            incerta = (p.get('trascrizione_incerta') or '').strip().lower() in ('sì', 'si') \
                or bool(re.search(r'trascri\w*\s+incert|forma udita|oscilla|mal trascritt', nota, re.I))
            if incerta:
                if 'trascrizione_incerta' in campi:
                    r['trascrizione_incerta'] = 'sì'
                elif 'note' in campi:
                    r['note'] = ((r.get('note') or '') + ' | ' if r.get('note') else '') + \
                        'trascrizione incerta sul nome'
        shutil.copy(percorso, percorso + '.prima_del_ripristino')
        with open(percorso, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore')
            w.writeheader(); w.writerows(righe)
        print('%s: %d righe riscritte' % (TABELLE[tab], len(righe)))

    print('patch: %s' % dict(esiti))
    print('campi sostituiti: %d, righe non trovate: %d' % (applicati, mancanti))
    if fuori:
        print('da escludere perche fuori seduta: %d' % len(fuori))
        for r in fuori:
            print('   %s %s %s' % (r['riga'], r['campo'], r.get('minutaggio', '')))


if __name__ == '__main__':
    main()

# Il conto che si mostra all'owner prima di consegnare (richiesta del 17 settembre).
# Tre grandezze che e' facile confondere e che qui restano separate: quante righe esistono,
# quanti nomi sono stati rimessi, e quanti casi restano irrisolti. Un numero solo le impasterebbe.
import csv, glob, os, collections

NET = os.environ['QN_NET']
DB = NET + '/report1/db'
PATCH = NET + '/report2/ripristino'


def leggi(nome):
    return list(csv.DictReader(open(DB + '/' + nome, encoding='utf-8')))


def patch():
    righe = []
    for f in sorted(glob.glob(PATCH + '/patch_*.csv')):
        righe += list(csv.DictReader(open(f, encoding='utf-8')))
    return righe


def si(v):
    return (v or '').strip().lower() in ('sì', 'si')


def main():
    notizie, documenti = leggi('notizie_candidate.csv'), leggi('documenti.csv')
    p = patch()
    esiti = collections.Counter(r['esito'] for r in p)
    coppie = {(r['riga'], r['campo']) for r in p}

    print('== righe ==')
    print('  notizie candidate      %5d' % len(notizie))
    print('  documenti              %5d' % len(documenti))
    print('  righe toccate dai patch%5d  (su %d campi distinti)'
          % (len({r['riga'] for r in p}), len(coppie)))

    print('\n== la passata di ripristino ==')
    for k in ('ripristinato', 'corretto', 'invariato', 'fuori_seduta'):
        print('  %-22s %5d' % (k, esiti.get(k, 0)))
    print('  totale campi lavorati  %5d' % sum(esiti.values()))

    print('\n== quello che resta irrisolto ==')
    inv = [r for r in p if r['esito'] == 'invariato']
    print('  campi senza il nome    %5d  (la fonte non lo dà)' % len(inv))
    print('  attribuzione incerta   %5d  (a chi attribuire il passaggio)'
          % sum(1 for n in notizie if si(n.get('attribuzione_incerta'))))
    print('  trascrizione incerta   %5d  (la forma del nome)'
          % sum(1 for d in documenti if si(d.get('trascrizione_incerta'))))
    print('  formule residue        %5d  (campi chiusi solo in parte)'
          % sum(1 for r in p if (r.get('formule_residue') or '').strip()))
    print('  fuori perimetro        %5d  (fuori dalla seduta aperta)'
          % sum(1 for n in notizie if si(n.get('fuori_perimetro'))))

    print('\n== territorio ==')
    with_q = [n for n in notizie if (n.get('quartiere') or '').strip()]
    print('  con quartiere          %5d su %d' % (len(with_q), len(notizie)))
    print('  con zona urbanistica   %5d' % sum(1 for n in with_q if (n.get('quartiere_zu') or '').strip()))
    print('  su più quartieri       %5d' % sum(1 for n in with_q if ';' in n['quartiere']))
    ded = collections.Counter((n.get('territorio_dedotto') or 'non attribuito') for n in notizie)
    for k in ('no', 'si', 'misto', 'non attribuito'):
        if k in ded:
            etichetta = {'no': 'letto dal testo', 'si': 'dedotto dal gazetteer',
                         'misto': 'testo e gazetteer discordi', 'non attribuito': 'nessun territorio'}[k]
            print('  %-24s %5d' % (etichetta, ded[k]))


if __name__ == '__main__':
    main()

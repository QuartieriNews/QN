# Il campione da rigiudicare dopo il difetto degli identificativi (STATO §105).
# Il campione originale mostrava, per le righe la cui posizione non coincideva piu' con il proprio
# numero, **gli accostamenti di un'altra riga**. Qui le stesse candidate tornano davanti a un
# lettore con i propri, presi dal file delle coppie riscritto da `build_db.py` con gli
# identificativi del registro. Non si estraggono casi nuovi: si rigiudicano quelli toccati, cosi'
# il confronto con il primo giudizio e' possibile.
import csv, os, collections

NET = os.environ['QN_NET']
righe = {r['id']: r for r in csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8'))}
toccati = list(csv.DictReader(open(NET + '/report2/out/DA_RIGIUDICARE.csv', encoding='utf-8')))

coppie = collections.defaultdict(list)
for c in csv.DictReader(open(NET + '/report2/coppie_parlato_scritto.csv', encoding='utf-8')):
    if c['scritta'] in righe: coppie[c['parlata']].append((righe[c['scritta']], c['forza']))

def riga(r, pref='  '):
    return ('%s%s [%s, %s, %s] %s\n%s   luoghi: %s\n%s   %s'
            % (pref, r['id'], r['fonte'], r['data_fatto'], r['municipio'] or '-',
               r['titolo'], pref, r['luoghi'], pref, (r['sintesi'] or '')[:200]))

out = ['# Campione da rigiudicare — accostamenti corretti', '',
       'Le stesse candidate del primo campione, con **i propri** accostamenti: la prima volta ne',
       'erano stati mostrati altri. La domanda non cambia: **stesso fatto** o **fatti diversi**,',
       'piu\' una riga di motivo. Sono lo stesso fatto se un lettore che le trovasse entrambe',
       'direbbe che la seconda non aggiunge niente alla prima.', '',
       'Il giudizio precedente **non si guarda**: sta nel file, ma leggerlo prima di giudicare',
       'toglie senso al confronto.', '']

for sez, etichetta, nota in (('A', 'Precisione', 'Un errore qui **abbassa** la novita\'.'),
                             ('C', 'Classe «dubbio»', 'Quante lo siano davvero decide l\'ampiezza dell\'intervallo.')):
    casi = [t for t in toccati if t['sezione'] == sez]
    out += ['## %s. %s — %d candidate' % (sez, etichetta, len(casi)), '', nota, '']
    for n, t in enumerate(casi, 1):
        r = righe.get(t['id_parlata'])
        if not r:
            out += ['### %s%d — %s: riga non piu\' nel database' % (sez, n, t['id_parlata']), '']
            continue
        out += ['### %s%d (era %s)' % (sez, n, t['caso_originale']), riga(r), '', '   accostata a:']
        acc = coppie.get(r['id'], [])
        if not acc: out += ['     nessun accostamento']
        for b, forza in acc:
            out += [riga(b, '     '), '        accostamento %s' % forza]
        out += ['']

p = NET + '/report2/campione_rigiudizio.md'
open(p, 'w', encoding='utf-8').write('\n'.join(out))
print('scritto %s: %d candidate, %d con accostamenti propri'
      % (p, len(toccati), sum(1 for t in toccati if coppie.get(t['id_parlata']))))
cambiati = sum(1 for t in toccati if t['sezione'] in ('A', 'C'))
print('sezione A: %d, sezione C: %d' % (sum(1 for t in toccati if t['sezione'] == 'A'),
                                        sum(1 for t in toccati if t['sezione'] == 'C')))

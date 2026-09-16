# I tre numeri del Report 2 poggiano sulla deduplicazione, e la sua qualita' non e' mai stata
# misurata (rilievo C4 §6.4). Questo programma non la misura: prepara il campione che un lettore
# deve giudicare, perche' dire se due righe sono lo stesso fatto e' lettura, non calcolo.
# Due campioni, perche' i due errori costano cose opposte:
#   - PRECISIONE: coppie che il confronto ha dato per gemelle (D). Un falso accostamento abbassa
#     la novita'.
#   - RICHIAMO: candidate del parlato classificate S, cioe' "nessun gemello scritto", accostate
#     alle righe scritte che un criterio piu' largo avvicina (stesso Municipio, data a tre giorni,
#     una parola lunga in comune). Un gemello mancato **alza** la novita', ed e' l'errore che
#     gonfia il numero principale: e' li' che il campione va guardato per primo.
import csv, os, random, re, collections

NET = os.environ['QN_NET']
SEME = '2026-06-dedup-audit'
PARLATO = {'A3', 'A4'}
righe = list(csv.DictReader(open(NET + '/report1/db/notizie_candidate.csv', encoding='utf-8')))

def classe(v):
    d, u = (int(x) for x in (v or '0/0').split('/'))
    return 'D' if d else ('U' if u else 'S')

def giorno(r):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', r['data_fatto'] or '')
    return int(m.group(3)) + 31 * int(m.group(2)) if m else None

def parole(r):
    testo = (r['titolo_anonimizzato'] or '') + ' ' + (r['luoghi'] or '')
    return {w for w in re.findall(r"[a-zA-Zàèéìòù']+", testo.lower()) if len(w) > 5}

# Le coppie non si ricalcolano qui: le scrive `build_db.py` in `coppie_parlato_scritto.csv` mentre
# fa il confronto esaustivo. Riscrivere `stesso_luogo` e `stesso_oggetto` in un secondo programma
# vorrebbe dire due copie di una regola di validazione, che divergono — in questa sessione e' gia'
# successo con due programmi lasciati indietro nella cartella dei dati.

parl = [r for r in righe if r['fonte'] in PARLATO]
scritte = [r for r in righe if r['fonte'] not in PARLATO]

# --- precisione: le candidate del parlato con almeno un gemello scritto forte
forti = [r for r in parl if classe(r['gemelli_scritti']) == 'D']

# --- richiamo: le S, e i loro vicini secondo un criterio deliberatamente piu' largo del nostro
esse = [r for r in parl if classe(r['gemelli_scritti']) == 'S']
per_mun = collections.defaultdict(list)
for s in scritte:
    for m in (s['municipio'] or '').split(';'):
        if m.strip(): per_mun[m.strip()].append(s)

vicini = []
for a in esse:
    ga = giorno(a); pa = parole(a)
    if ga is None or not pa: continue
    cand = []
    for m in (a['municipio'] or '').split(';'):
        for b in per_mun.get(m.strip(), []):
            gb = giorno(b)
            if gb is None or abs(gb - ga) > 3: continue
            com = pa & parole(b)
            if com: cand.append((len(com), b, com))
    cand.sort(key=lambda x: -x[0])
    if cand: vicini.append((a, cand[:2]))

random.Random(SEME).shuffle(vicini)
camp = vicini[:40]

def riga(r, pref='  '):
    return ('%s%s [%s, %s, %s] %s\n%s   luoghi: %s\n%s   %s'
            % (pref, r['id'], r['fonte'], r['data_fatto'], r['municipio'] or '-',
               r['titolo_anonimizzato'], pref, r['luoghi'], pref, (r['sintesi'] or '')[:200]))

out = ['# Campione per l\'audit della deduplicazione', '',
       'Seme `%s`. Per ogni coppia: **stesso fatto** o **fatti diversi**, piu\' una riga di motivo.' % SEME,
       'Non e\' una domanda di somiglianza: sono lo stesso fatto se un lettore che le trovasse',
       'entrambe direbbe che la seconda non aggiunge niente alla prima.', '',
       '## A. Precisione — coppie che il confronto ha dato per gemelle: %d' % len(forti),
       '', 'Un errore qui **abbassa** la novita\'.', '']
# La sezione A deve portare **tutte e due** le righe della coppia: la prima versione stampava solo
# quella parlata con il contatore d/u, e il revisore ha dovuto rieseguire il confronto per sapere
# con che cosa fosse stata accoppiata. Un campione che non mostra la coppia non e' un campione.
coppie = collections.defaultdict(list)
per_id = {r['id']: r for r in righe}
for c in csv.DictReader(open(NET + '/report2/coppie_parlato_scritto.csv', encoding='utf-8')):
    if c['scritta'] in per_id:
        coppie[c['parlata']].append((per_id[c['scritta']], c['forza']))

for i, r in enumerate(forti, 1):
    out += ['### A%d' % i, riga(r), '', '   accoppiata a:']
    for b, forza in coppie.get(r['id'], []):
        out += [riga(b, '     '), '        accostamento %s' % forza]
    out += ['']
out += ['', '## B. Richiamo — candidate date per nuove, con i vicini che un criterio piu\' largo trova',
        '', '%d candidate S su %d hanno almeno un vicino cosi\'; qui ne trovi %d.'
        % (len(vicini), len(esse), len(camp)),
        'Un errore qui **alza** la novita\'. Per ciascuna: qualcuno dei vicini e\' lo stesso fatto?', '']
for i, (a, cand) in enumerate(camp, 1):
    out += ['### B%d — data per nuova' % i, riga(a), '', '   vicini:']
    for n, b, com in cand:
        out += [riga(b, '     '), '        parole in comune: %s' % ', '.join(sorted(com))]
    out += ['']

# --- C. la classe U, che e' meta' del corpus parlato e non l'ha mai guardata nessuno.
# E' la classe che decide l'ampiezza dell'intervallo: se quasi nessun `dubbio` fosse un gemello
# vero, la novita' reale starebbe vicino al limite superiore invece che a quello inferiore. Il
# revisore della prima tornata l'ha segnalato guardando di sfuggita 41 accostamenti deboli e
# trovandone tre convincenti: un'indicazione, non una misura. Questa sezione la rende misurabile.
dubbi = [r for r in parl if classe(r['gemelli_scritti']) == 'U']
random.Random(SEME + '-U').shuffle(dubbi)
campU = dubbi[:40]
out += ['', '## C. La classe «dubbio» — candidate accostate a una riga scritta ma non allo stesso oggetto',
        '', '%d candidate su %d sono in questa classe; qui ne trovi %d, con tutti i loro accostamenti deboli.'
        % (len(dubbi), len(parl), len(campU)),
        'Sono le righe che l\'intervallo conta **una volta come nuove e una volta come gia\' scritte**:',
        'quante lo siano davvero decide se la risposta sta vicino al 48% o vicino al 97%.', '']
for i, r in enumerate(campU, 1):
    out += ['### C%d' % i, riga(r), '', '   accostata a:']
    for b, forza in coppie.get(r['id'], []):
        out += [riga(b, '     '), '        accostamento %s' % forza]
    out += ['']

open(NET + '/report2/campione_dedup.md', 'w', encoding='utf-8').write('\n'.join(out))
print('A. coppie gemelle (precisione): %d' % len(forti))
print('B. candidate S con almeno un vicino largo: %d su %d S (campionate %d)'
      % (len(vicini), len(esse), len(camp)))
print('C. classe dubbio: %d candidate (campionate %d)' % (len(dubbi), len(campU)))
print('scritto report2/campione_dedup.md')

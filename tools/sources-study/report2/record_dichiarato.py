# Quanti atti dichiarano, dentro il proprio testo, che il record completo della seduta non e' l'atto
# ma la registrazione. Il rapporto lo diceva citando due verbali: due verbali non reggono una tesi,
# un conteggio su tutto il corpus si'.
# Le formule sono quattro e non sono equivalenti: "sostituisce" e' la piu' forte (l'ente dichiara
# che il verbale non riporta gli interventi), "si rimanda" e "versione integrale sul portale" sono
# rinvii, "sommario" e' un'ammissione di incompletezza. Si contano separate.
import os, re, collections, unicodedata

NET = os.environ['QN_NET']
FORMULE = [
    ('la registrazione sostituisce il verbale', r'(video)?registrazione[^.]{0,80}sostituisce'),
    ('si rimanda alla registrazione', r'(si rimanda|si rinvia)[^.]{0,80}(registrazione|video|streaming|riunione integrale)'),
    ('il verbale e\' dichiarato sommario', r'verbale[^.]{0,60}(sommario|non integrale|per sintesi)'),
    ('versione integrale sul portale', r'(versione integrale|integrale audio video)[^.]{0,80}(portale|disponibile)'),
]

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'\s+', ' ', ''.join(c for c in s if not unicodedata.combining(c)))

atti = sorted(os.listdir(NET + '/A2_text'))
trovati = collections.defaultdict(set)
for f in atti:
    t = norm(open(NET + '/A2_text/' + f, encoding='utf-8', errors='replace').read())
    for nome, p in FORMULE:
        if re.search(p, t): trovati[nome].add(f[:-4])

tutti = set().union(*trovati.values()) if trovati else set()
print('atti letti: %d' % len(atti))
print('atti che dichiarano che il record completo e\' la registrazione: %d' % len(tutti))
for nome, _ in FORMULE:
    mun = sorted({x.split('_')[2] for x in trovati[nome]})
    print('  %-42s %3d  (Municipi %s)' % (nome, len(trovati[nome]), ', '.join(mun)))
print('Municipi che usano almeno una formula: %d su 15 — %s'
      % (len({x.split('_')[2] for x in tutti}), ', '.join(sorted({x.split('_')[2] for x in tutti}))))
print('per tipo di atto:', dict(collections.Counter(x.split('_')[1] for x in tutti)))

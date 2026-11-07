# Correzione singola, residuo n. 7 del controllo C2: il titolo di un'opera era stato sostituito
# da una perifrasi perche' coincide con il nome proprio di una persona. DEC-102 protegge le
# persone identificabili, non i titoli pubblicati: altrove nello stesso corpus i titoli ufficiali
# restano verbatim anche quando contengono un nome. L'anonimizzazione era anche inefficace, visto
# che l'URL di evidenza contiene il titolo.
# Il nome del regista resta fuori: quello e' una persona, e DEC-102 vale.
import csv, os, shutil

F = os.environ['QN_NET'] + '/report1/out/L14_notizie.csv'
shutil.copy(F, F + '.prima_del_fix_n0812')

SOST = [
    ('Proiezione di un film del 2016 e incontro con il regista',
     'Proiezione di «Jackie» (2016) e incontro con il regista'),
    ('proiezione gratuita di un film del 2016, cento minuti, dedicato alla vedova di un presidente americano,',
     'proiezione gratuita di «Jackie» (2016, cento minuti), dedicato alla vedova di un presidente americano,'),
    ('Il titolo del film coincide con il nome proprio di una persona reale: nei campi è sostituito da una descrizione (DEC-102).',
     'Titolo dell’opera verbatim; il nome del regista resta fuori dai campi (DEC-102, residuo C2 n. 7).'),
]

righe = list(csv.reader(open(F, encoding='utf-8')))
tocc = 0
for r in righe:
    if r and r[0] == 'E2_181':
        for i, v in enumerate(r):
            for a, b in SOST:
                if a in v:
                    r[i] = v.replace(a, b); tocc += 1; v = r[i]
with open(F, 'w', newline='', encoding='utf-8') as fh:
    csv.writer(fh).writerows(righe)
print('campi corretti:', tocc, '(attesi 3)')

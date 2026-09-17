# L'ultimo miglio, in un comando solo.
# Alla fine della lettura vanno rifatti, **in quest'ordine**, il database e tutti i numeri che il
# rapporto cita, poi i file da caricare e il congelamento. Farlo a mano significa dimenticarne uno:
# e' gia' successo di pubblicare un numero vecchio accanto a uno nuovo, che e' peggio di due numeri
# vecchi perche' il testo non torna con se' stesso.
# Non tocca Drive e non fa commit: quelli restano decisioni, non passi di uno script.
import os, subprocess, sys, time

NET = os.environ['QN_NET']
REPO = '/home/user/QN/tools/sources-study'
PASSI = [
    ('il database', 'report1/build_db.py'),
    # Il ripristino dei nomi (DEC-105) e' un passo della catena, non una correzione a valle:
    # build_db ricostruisce il database dai lotti di lettura, quindi una modifica fatta
    # direttamente sui CSV sparirebbe alla rigenerazione successiva.
    ('i nomi ripristinati', 'report2/applica_patch.py'),
    ('la risposta e la banda', 'report2/risposta.py'),
    ('i numeri del rapporto', 'report2/verifica_numeri_rapporto.py'),
    ('i toponimi incerti', 'report2/audit_toponimi.py'),
    ('il tetto della copertura', 'report2/copertura_testi_atti.py'),
    ('il motivo del non-alta', 'report2/motivo_non_alta.py'),
    ('la convenzione dell\'organo', 'report2/convenzione_organo.py'),
    ('i doppioni di pubblicazione', 'report2/doppioni_documenti.py'),
    ('le code perdute', 'report2/code_perdute.py'),
    ('i magneti della deduplicazione', 'report2/magneti_dedup.py'),
    ('i file compatti per Drive', 'report1/compatte.py'),
]
solo = sys.argv[1:] 
uscita = []
for titolo, prog in PASSI:
    if solo and not any(s in prog for s in solo): continue
    t0 = time.time()
    r = subprocess.run([sys.executable, REPO + '/' + prog], capture_output=True, text=True,
                       env={**os.environ, 'QN_NET': NET})
    stato = 'ok' if r.returncode == 0 else 'ERRORE'
    print('\n========== %s (%s, %s, %.0fs)' % (titolo, prog.split('/')[-1], stato, time.time() - t0))
    print(r.stdout.rstrip()[-4000:])
    if r.returncode != 0:
        print(r.stderr.rstrip()[-2000:])
        print('\nFermato qui: i passi successivi leggono quello che questo doveva scrivere.')
        sys.exit(1)
    uscita.append((titolo, prog))
print('\n\n========== fatto: %d passi' % len(uscita))
print('Restano tre cose che uno script non deve fare da solo:')
print('  1. rileggere il rapporto con i numeri nuovi e correggere quelli che non tornano;')
print('  2. `report2/congela_consegna.py`, che fotografa lo stato consegnato;')
print('  3. Drive, una sessione sola: caricare i compatti rigenerati e cestinare i file vecchi.')

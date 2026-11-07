# L'ultimo miglio, in un comando solo.
# Alla fine della lettura vanno rifatti, **in quest'ordine**, il database e tutti i numeri che il
# rapporto cita, poi i file da caricare e il congelamento. Farlo a mano significa dimenticarne uno:
# e' gia' successo di pubblicare un numero vecchio accanto a uno nuovo, che e' peggio di due numeri
# vecchi perche' il testo non torna con se' stesso.
# Non tocca Drive e non fa commit: quelli restano decisioni, non passi di uno script.
import glob, os, shutil, subprocess, sys, time

NET = os.environ['QN_NET']
REPO = '/home/user/QN/tools/sources-study'
PASSI = [
    ('il database', 'report1/build_db.py'),
    # Il ripristino dei nomi (DEC-105) e' un passo della catena, non una correzione a valle:
    # build_db ricostruisce il database dai lotti di lettura, quindi una modifica fatta
    # direttamente sui CSV sparirebbe alla rigenerazione successiva.
    ('i nomi ripristinati', 'report2/applica_patch.py'),
    # Gli accenti resi con l'apostrofo arrivano dai lettori e si rifanno a ogni rigenerazione:
    # vanno rimessi qui dentro, dopo le patch, o tornano puntualmente nel file consegnato.
    ('gli accenti', 'report2/accenti.py'),
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
    # Un controllo, non un passo: non scrive il database, lo rilegge. Se fallisce non ferma la
    # catena - non c'e' piu' niente dopo - ma il verdetto resta in fondo, dove si guarda.
    ('il territorio contro il gazetteer', 'report2/verifica_territori.py', True),
]
solo = sys.argv[1:] 
# I programmi si importano a vicenda da QN_NET (build_db fa `sys.path.insert(0, QN_NET)`), quindi
# una copia di lavoro vecchia esegue codice vecchio senza che niente lo dica: e' successo con
# geo_lookup, e le colonne del territorio sono uscite vuote da una catena che riportava "ok".
# Allineare prima di partire costa un secondo e toglie di mezzo tutta la classe di errore.
allineati = 0
for sorgente in glob.glob(REPO + '/**/*.py', recursive=True):
    if '__pycache__' in sorgente:
        continue
    destinazione = NET + '/' + os.path.relpath(sorgente, REPO)
    if not os.path.exists(destinazione) or open(sorgente, 'rb').read() != open(destinazione, 'rb').read():
        os.makedirs(os.path.dirname(destinazione), exist_ok=True)
        shutil.copy(sorgente, destinazione)
        allineati += 1
print('copia di lavoro allineata al repository: %d programmi' % allineati)

uscita = []
controlli_falliti = []
for passo in PASSI:
    titolo, prog = passo[0], passo[1]
    controllo = len(passo) > 2 and passo[2]
    if solo and not any(s in prog for s in solo): continue
    t0 = time.time()
    r = subprocess.run([sys.executable, REPO + '/' + prog], capture_output=True, text=True,
                       env={**os.environ, 'QN_NET': NET})
    stato = 'ok' if r.returncode == 0 else 'ERRORE'
    print('\n========== %s (%s, %s, %.0fs)' % (titolo, prog.split('/')[-1], stato, time.time() - t0))
    print(r.stdout.rstrip()[-4000:])
    if r.returncode != 0:
        print(r.stderr.rstrip()[-2000:])
        if not controllo:
            print('\nFermato qui: i passi successivi leggono quello che questo doveva scrivere.')
            sys.exit(1)
        controlli_falliti.append(titolo)
    uscita.append((titolo, prog))
print('\n\n========== fatto: %d passi' % len(uscita))
if controlli_falliti:
    print('CONTROLLI FALLITI: %s — da guardare prima di consegnare.' % ', '.join(controlli_falliti))
print('Restano tre cose che uno script non deve fare da solo:')
print('  1. rileggere il rapporto con i numeri nuovi e correggere quelli che non tornano;')
print('  2. `report2/congela_consegna.py`, che fotografa lo stato consegnato;')
print('  3. Drive, una sessione sola: caricare i compatti rigenerati e cestinare i file vecchi.')
if controlli_falliti:   # una chiusura con controlli falliti non e' una chiusura riuscita (AGENTS.md)
    sys.exit(1)

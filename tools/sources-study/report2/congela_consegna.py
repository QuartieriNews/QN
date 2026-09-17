# Il numero pubblicato va accompagnato dallo stato che lo ha generato (rilievo C5): senza, «83,9%»
# e' un'affermazione che nessuno puo' rifare, perche' il database cambia a ogni lotto che rientra.
# Questo programma congela in una cartella datata tutto quello che serve a rifare i conti, e scrive
# accanto i valori calcolati in quel momento. Si esegue alla consegna, non prima.
import csv, datetime, os, shutil, subprocess, sys

NET = os.environ['QN_NET']
REPO = '/home/user/QN/tools/sources-study'
oggi = datetime.date.today().isoformat()
dest = NET + '/report2/consegna_' + oggi
os.makedirs(dest, exist_ok=True)

DA_COPIARE = [
    'report1/db/notizie_candidate.csv', 'report1/db/documenti.csv', 'report1/db/fonti.csv',
    'report1/db/vicende.csv', 'report1/db/territori.csv', 'report1/db/registro_id.csv',
    'report2/coppie_parlato_scritto.csv', 'report2/manifest_video_rtv.csv',
    'report2/manifest_video_rtv_fuori_finestra.csv', 'report2/manifest_report2.csv',
    'report2/out/AUDIT_dedup.csv', 'report2/out/AUDIT_dubbi.csv', 'report2/out/AUDIT2_dedup.csv',
    # Il rigiudizio non e' un audit in piu': **sostituisce** i giudizi dati sul campione difettoso
    # (STATO §105), e senza di lui il 17,5% non si rifa'. Con l'elenco dei casi che ha ripreso.
    'report2/out/AUDIT3_rigiudizio.csv', 'report2/out/DA_RIGIUDICARE.csv',
    'report2/out/INDICE_EVIDENZE.csv', 'report2/t4_esito.csv',
]
copiati = 0
for f in DA_COPIARE:
    p = NET + '/' + f
    if os.path.exists(p):
        shutil.copy(p, dest + '/' + os.path.basename(p)); copiati += 1
    else:
        print('manca, e non e\' normale:', f)

# I programmi che producono i numeri vanno congelati con i dati: una riga cambiata in uno di loro
# cambia il risultato senza che i dati si muovano.
os.makedirs(dest + '/programmi', exist_ok=True)
for f in ('report1/build_db.py', 'report2/risposta.py', 'report2/novita_meccanica.py',
          'report2/audit_toponimi.py', 'report2/campione_dedup.py', 'report2/ricampiona_toccati.py',
          'report2/copertura_testi_atti.py', 'report2/motivo_non_alta.py',
          'report2/doppioni_documenti.py', 'report2/magneti_dedup.py',
          'report2/verifica_numeri_rapporto.py', 'report2/testo_documento.py',
          'report2/cerca_negli_atti.py', 'report2/record_dichiarato.py',
          'report2/link_verbali_video.py',
          # Il ripristino dei nomi (DEC-105) e' dentro la catena che produce il database, non una
          # correzione a valle: senza questi il congelato non si rifa'.
          'geo_lookup.py', 'report2/applica_patch.py', 'report2/accenti.py',
          'report2/lotti_ripristino.py', 'report2/verifica_territori.py',
          'report2/campione_residuo.py', 'report2/riconcilia_consegna.py'):
    p = REPO + '/' + f
    if os.path.exists(p): shutil.copy(p, dest + '/programmi/' + os.path.basename(p))

# I patch sono il dato di ingresso del ripristino: il database senza di loro non si ricostruisce,
# e la ragione riga per riga e' l'unica prova di perche' un nome c'e' o non c'e'.
os.makedirs(dest + '/ripristino', exist_ok=True)
import glob
patch = sorted(glob.glob(NET + '/report2/ripristino/patch_*.csv')) + \
    sorted(glob.glob(NET + '/report2/ripristino/misura_residuo.csv'))
for f in patch:
    shutil.copy(f, dest + '/ripristino/' + os.path.basename(f))
print('patch del ripristino congelati: %d' % len(patch))

with open(dest + '/COME_RIFARE_I_CONTI.md', 'w', encoding='utf-8') as fh:
    fh.write('# Lo stato che ha prodotto i numeri del Report 2\n\n')
    fh.write('Congelato il %s. Per rifare i conti: `QN_NET` a una cartella che contenga questi\n'
             'file nella stessa struttura, poi i programmi in `programmi/`.\n\n' % oggi)
    fh.write('Il commit del repository al momento della consegna:\n\n    %s\n\n'
             % subprocess.run(['git', '-C', '/home/user/QN', 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip())
    fh.write('I numeri calcolati in questo stato stanno in `numeri.txt`, prodotti dai programmi\n'
             'qui accanto e non riscritti a mano.\n\n')
    fh.write('`ripristino/` contiene i patch della passata DEC-105, con la ragione riga per riga:\n'
             'sono il dato di ingresso di `applica_patch.py` e la prova di perche\' un nome c\'e\'\n'
             'o non c\'e\'. Il database si ricostruisce da `build_db.py` e da quelli, in questo\n'
             'ordine: build_db, applica_patch, accenti.\n')

with open(dest + '/numeri.txt', 'w', encoding='utf-8') as fh:
    # `risposta.py` per primo: e' il numero principale, ed e' l'unico che legge i file dell'audit.
    for prog in ('risposta.py', 'novita_meccanica.py', 'audit_toponimi.py', 'motivo_non_alta.py',
                 'copertura_testi_atti.py', 'doppioni_documenti.py'):
        r = subprocess.run([sys.executable, REPO + '/report2/' + prog],
                           capture_output=True, text=True, env={**os.environ, 'QN_NET': NET})
        fh.write('=== %s\n%s\n' % (prog, r.stdout))
print('congelati %d file di dati in %s' % (copiati, os.path.basename(dest)))
print('programmi: %d' % len(os.listdir(dest + '/programmi')))
print('numeri.txt: %d righe' % sum(1 for _ in open(dest + '/numeri.txt', encoding='utf-8')))

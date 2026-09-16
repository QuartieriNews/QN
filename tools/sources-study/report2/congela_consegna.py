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
for f in ('report1/build_db.py', 'report2/novita_meccanica.py', 'report2/audit_toponimi.py',
          'report2/campione_dedup.py', 'report2/copertura_testi_atti.py',
          'report2/record_dichiarato.py', 'report2/link_verbali_video.py'):
    p = REPO + '/' + f
    if os.path.exists(p): shutil.copy(p, dest + '/programmi/' + os.path.basename(p))

with open(dest + '/COME_RIFARE_I_CONTI.md', 'w', encoding='utf-8') as fh:
    fh.write('# Lo stato che ha prodotto i numeri del Report 2\n\n')
    fh.write('Congelato il %s. Per rifare i conti: `QN_NET` a una cartella che contenga questi\n'
             'file nella stessa struttura, poi i programmi in `programmi/`.\n\n' % oggi)
    fh.write('Il commit del repository al momento della consegna:\n\n    %s\n\n'
             % subprocess.run(['git', '-C', '/home/user/QN', 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip())
    fh.write('I numeri calcolati in questo stato stanno in `numeri.txt`, prodotti dai programmi\n'
             'qui accanto e non riscritti a mano.\n')

with open(dest + '/numeri.txt', 'w', encoding='utf-8') as fh:
    for prog in ('novita_meccanica.py', 'audit_toponimi.py'):
        r = subprocess.run([sys.executable, REPO + '/report2/' + prog],
                           capture_output=True, text=True, env={**os.environ, 'QN_NET': NET})
        fh.write('=== %s\n%s\n' % (prog, r.stdout))
print('congelati %d file di dati in %s' % (copiati, os.path.basename(dest)))

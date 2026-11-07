# Che cosa va davvero ricaricato su Drive. Rigenerare tutte le parti e ricaricarle tutte costa
# cento chiamate e cancella la storia dei file che non sono cambiati; qui si confronta parte per
# parte con quelle gia' caricate e si carica solo la differenza.
# Uscita: tre elenchi - nuove, cambiate, sparite - piu' il conto delle identiche.
import filecmp, os, subprocess, sys

NET = os.environ['QN_NET']
SCRATCH = os.path.dirname(NET.rstrip('/'))
VECCHIE = SCRATCH + '/drive_parti'
NUOVE = SCRATCH + '/drive_parti_nuove'
DB = NET + '/report1/db'
PARTI = os.path.dirname(os.path.abspath(__file__)) + '/parti_drive.py'

# Il nome su Drive tiene il rapporto di origine della **fonte**, non del file: A3 e A4 sono le fonti
# del Report 2, tutte le altre del Report 1. E' la convenzione dei file gia' caricati e non si cambia
# in corsa, o l'owner si ritrova la stessa fonte sotto due nomi.
def rapporto(fonte):
    return 'Report2' if fonte in ('A3', 'A4') else 'Report1'

SORGENTI = []
for f in sorted(os.listdir(DB)):
    for prefisso_file, genere in (('notizie_compatte_', 'notizie'),
                                  ('documenti_compatti_', 'documenti'),
                                  ('notizie_testo_', 'testo')):
        if f.startswith(prefisso_file) and f.endswith('.csv'):
            fonte = f[len(prefisso_file):-4]
            SORGENTI.append((f, '%s_%s_%s_2026-06' % (rapporto(fonte), genere, fonte)))


def main():
    if os.path.exists(NUOVE):
        for f in os.listdir(NUOVE):
            os.remove(NUOVE + '/' + f)
    for sorgente, prefisso in SORGENTI:
        subprocess.run([sys.executable, PARTI, DB + '/' + sorgente, NUOVE, prefisso],
                       check=True, capture_output=True)
    nuove = set(os.listdir(NUOVE))
    vecchie = set(os.listdir(VECCHIE)) if os.path.isdir(VECCHIE) else set()
    da_caricare = sorted(nuove - vecchie)
    cambiate = sorted(f for f in nuove & vecchie
                      if not filecmp.cmp(NUOVE + '/' + f, VECCHIE + '/' + f, shallow=False))
    sparite = sorted(vecchie - nuove)
    uguali = len(nuove & vecchie) - len(cambiate)
    print('parti nuove (%d):' % len(da_caricare))
    for f in da_caricare: print('   ', f, os.path.getsize(NUOVE + '/' + f))
    print('parti cambiate (%d):' % len(cambiate))
    for f in cambiate: print('   ', f, os.path.getsize(NUOVE + '/' + f))
    print('parti sparite, da cestinare (%d): %s' % (len(sparite), sparite))
    print('parti identiche, da lasciare stare: %d' % uguali)
    print('totale da caricare: %d' % (len(da_caricare) + len(cambiate)))


if __name__ == '__main__':
    main()

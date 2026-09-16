# Confronta i file caricati su Drive con gli originali locali. Serve al passo di consegna
# descritto in HANDOFF §4, dopo `parti_drive.py` e il caricamento.
#
# Nasce da un errore vero (STATO §129): una trasposizione dentro un token base64 di un URL
# non cambia la lunghezza, quindi il confronto su `fileSize` la lascia passare. L'unica
# verifica che regge è il confronto del contenuto.
#
# Il contenuto scaricato da Drive resta già scritto su disco — nelle trascrizioni della
# sessione e dei sottoagenti, e nei file dei risultati troppo grandi per la risposta — e
# questo programma lo cerca lì invece di farselo ricopiare: una verifica eseguita a mano
# introduce la stessa classe di errore che dovrebbe trovare.
#
# Uso: python3 verifica_drive.py <cartella_parti> <cartella_tracce> [<cartella_tracce> ...]
import base64, glob, os, sys


def tracce(radici):
    """Ogni file che può contenere una risposta di download, letto una volta sola."""
    percorsi = []
    for r in radici:
        if os.path.isfile(r):
            percorsi.append(r)
        else:
            percorsi += [p for p in glob.glob(r + '/**/*', recursive=True) if os.path.isfile(p)]
    testi = []
    for p in percorsi:
        try:
            testi.append(open(p, encoding='utf-8', errors='replace').read())
        except OSError as e:
            print('non leggibile:', p, e)
    return testi


def confronta(cartella_parti, testi):
    identici, assenti = 0, []
    for nome in sorted(os.listdir(cartella_parti)):
        atteso = base64.b64encode(open(cartella_parti + '/' + nome, 'rb').read()).decode()
        if any(atteso in t for t in testi):
            identici += 1
        else:
            assenti.append(nome)
    return identici, assenti


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__ or 'uso: verifica_drive.py <cartella_parti> <cartella_tracce> ...')
    identici, assenti = confronta(sys.argv[1].rstrip('/'), tracce(sys.argv[2:]))
    print(f"contenuto identico all'originale: {identici} su {identici + len(assenti)}")
    for nome in assenti:
        print('  non confermato (da scaricare, o diverso):', nome)
    sys.exit(1 if assenti else 0)

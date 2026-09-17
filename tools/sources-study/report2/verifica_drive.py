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


def confronta(cartella_parti, testi, id_di=None):
    """`id_di` mappa nome -> id Drive. Quando c'e', la conferma richiede che il base64 stia
    **dentro la risposta di download di quel file**: la risposta ha la forma
    {"content":"<base64>","id":"<id>",...} e l'id segue subito il contenuto. Senza questo
    vincolo basterebbe che qualcuno avesse calcolato il base64 del file locale - cosa che un
    lettore puo' fare per conto suo - e la verifica confermerebbe sé stessa invece del
    caricamento. E' successo: tre file sono risultati "identici" prima di essere caricati."""
    identici, assenti = 0, []
    for nome in sorted(os.listdir(cartella_parti)):
        atteso = base64.b64encode(open(cartella_parti + '/' + nome, 'rb').read()).decode()
        trovato = False
        for t in testi:
            i = t.find(atteso)
            while i != -1:
                coda = t[i + len(atteso):i + len(atteso) + 200]
                # L'id, e non `"id":"..."`: nelle trascrizioni dei sottoagenti la risposta e'
                # una stringa JSON dentro un'altra, con le virgolette sfuggite, e la forma
                # letterale non si trova. L'id da solo e' gia' un legame forte: trentatre
                # caratteri unici subito dopo il contenuto.
                if id_di is None or id_di.get(nome, '\x00') in coda:
                    trovato = True
                    break
                i = t.find(atteso, i + 1)
            if trovato:
                break
        if trovato:
            identici += 1
        else:
            assenti.append(nome)
    return identici, assenti


def id_caricati(percorsi):
    """nome -> id Drive, dai file di registro del caricamento (nome, byte, id)."""
    out = {}
    for p in percorsi:
        if not os.path.exists(p):
            continue
        for riga in open(p, encoding='utf-8'):
            pezzi = riga.split()
            if len(pezzi) >= 3:
                out[pezzi[0]] = pezzi[2]
    return out


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__ or 'uso: verifica_drive.py <cartella_parti> <cartella_tracce> ...')
    # Solo i registri di **questo** caricamento: `drive_caricati.txt` senza suffisso e' quello
    # della consegna precedente, e per i dieci nomi che si ripetono darebbe l'id del file vecchio.
    registri = glob.glob(os.path.dirname(sys.argv[1].rstrip('/')) + '/drive_caricati[2_]*.txt')
    id_di = id_caricati(registri)
    print('id di caricamento noti: %d (da %d registri)' % (len(id_di), len(registri)))
    identici, assenti = confronta(sys.argv[1].rstrip('/'), tracce(sys.argv[2:]), id_di)
    print(f"contenuto identico all'originale: {identici} su {identici + len(assenti)}")
    for nome in assenti:
        print('  non confermato (da scaricare, o diverso):', nome)
    sys.exit(1 if assenti else 0)

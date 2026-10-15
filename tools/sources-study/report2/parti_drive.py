# Divide un CSV compatto nelle parti che il caricamento su Drive accetta.
# Serve al passo di consegna descritto in HANDOFF §4: i compatti per item
# vanno nella cartella Drive, e una chiamata sola non regge i file grandi.
# Ogni parte ripete l'intestazione, così ciascuna si apre da sola.
import csv, io, os, sys

LIMITE = int(os.environ.get('LIMITE_PARTE', 54000))

def parti(sorgente, destinazione, prefisso):
    with open(sorgente, newline='', encoding='utf-8') as f:
        righe = list(csv.reader(f))
    if not righe:
        sys.exit('parti_drive: %s e\' vuoto o non e\' un CSV' % sorgente)
    intestazione, corpo = righe[0], righe[1:]

    def serializza(rs):
        b = io.StringIO()
        w = csv.writer(b, lineterminator='\n')
        for r in rs:
            w.writerow(r)
        return b.getvalue()

    testa = serializza([intestazione])
    blocchi, corrente = [], []
    for r in corpo:
        if len(testa.encode()) + len(serializza([r]).encode()) > LIMITE:
            sys.exit('parti_drive: la riga %d da sola supera il limite di %d byte (%d): nessuna parte scritta'
                     % (corpo.index(r) + 2, LIMITE, len(testa.encode()) + len(serializza([r]).encode())))
        prova = corrente + [r]
        if corrente and len(testa.encode()) + len(serializza(prova).encode()) > LIMITE:
            blocchi.append(corrente)
            corrente = [r]
        else:
            corrente = prova
    if corrente:
        blocchi.append(corrente)

    os.makedirs(destinazione, exist_ok=True)
    scritti = []
    for i, b in enumerate(blocchi, 1):
        nome = (prefisso if len(blocchi) == 1
                else '%s_parte%ddi%d' % (prefisso, i, len(blocchi))) + '.csv'
        percorso = os.path.join(destinazione, nome)
        with open(percorso, 'w', encoding='utf-8', newline='') as f:
            f.write(testa + serializza(b))
        scritti.append((nome, os.path.getsize(percorso), len(b)))
    return scritti, len(corpo)

if __name__ == '__main__':
    sorgente, destinazione, prefisso = sys.argv[1], sys.argv[2], sys.argv[3]
    scritti, n = parti(sorgente, destinazione, prefisso)
    print('%s: %d righe -> %d parti' % (os.path.basename(sorgente), n, len(scritti)))
    for nome, dim, righe in scritti:
        print('  %-52s %7d B  %5d righe' % (nome, dim, righe))

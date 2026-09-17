# Confronta un file scaricato da Drive con l'originale locale, e dice **dove** differisce.
# Serve subito dopo un caricamento: il confronto dei byte non basta, perche' un carattere
# scambiato dentro un token di URL non cambia la lunghezza - e' successo due volte in questa
# consegna, l'ultima su tre righe di un file che il controllo dimensionale aveva approvato.
#
# Uso: python3 confronta_scaricato.py <file_del_risultato_di_download> <cartella_originali>
import base64, difflib, json, os, sys

risultato, cartella = sys.argv[1], sys.argv[2].rstrip('/')
j = json.load(open(risultato, encoding='utf-8'))
dati = base64.b64decode(j['content'])
percorso = cartella + '/' + j['title']
if not os.path.exists(percorso):
    sys.exit('originale non trovato: ' + percorso)
locale = open(percorso, 'rb').read()
print('%s | drive %d byte | locale %d byte | identici: %s'
      % (j['title'], len(dati), len(locale), dati == locale))
if dati == locale:
    sys.exit(0)
a = locale.decode('utf-8', 'replace').splitlines()
b = dati.decode('utf-8', 'replace').splitlines()
if len(a) != len(b):
    print('righe: locale %d, drive %d' % (len(a), len(b)))
diverse = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
print('righe diverse: %d %s' % (len(diverse), diverse[:10]))
for i in diverse[:5]:
    print('--- riga %d' % (i + 1))
    for l in difflib.unified_diff([a[i]], [b[i]], lineterm='', n=0):
        if l[:1] in '+-' and not l.startswith(('+++', '---')):
            print('   ', l[:300])
sys.exit(1)

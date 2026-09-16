# Cercare un toponimo negli atti con `grep` sottostima i riscontri, e sottostima **proprio sui nomi
# lunghi**: i PDF estratti vanno a capo dentro il nome, e "Angelo Musco" spezzato su due righe non
# si trova per riga. Cioe' l'errore cade esattamente sui toponimi, che sono quello che si cerca.
# Trovato da un lettore che ha costruito un indice appiattito e ha rifatto tutte le proprie ricerche.
# Qui l'indice si costruisce una volta e si riusa: senza, ogni lettore lo rifa' o non lo fa.
import os, re, sys, unicodedata, pickle

NET = os.environ['QN_NET']
CACHE = NET + '/report2/.indice_atti.pickle'

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]+', ' ', s)).strip()

def indice(ricostruisci=False):
    """Il testo di ogni atto, appiattito: niente a capo, niente doppi spazi, niente accenti."""
    if not ricostruisci and os.path.exists(CACHE):
        with open(CACHE, 'rb') as fh: return pickle.load(fh)
    out = {}
    for f in sorted(os.listdir(NET + '/A2_text')):
        if f.endswith('.txt'):
            out[f[:-4]] = norm(open(NET + '/A2_text/' + f, encoding='utf-8', errors='replace').read())
    with open(CACHE, 'wb') as fh: pickle.dump(out, fh)
    return out

def cerca(frase, idx=None):
    """Gli atti che contengono la frase, confrontata sul testo appiattito."""
    idx = idx if idx is not None else indice()
    q = norm(frase)
    return [n for n, t in idx.items() if q and q in t]

if __name__ == '__main__':
    idx = indice(ricostruisci='--ricostruisci' in sys.argv)
    termini = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not termini:
        print('indice: %d atti appiattiti' % len(idx))
        print('uso: cerca_negli_atti.py "Angelo Musco" "via Casali delle Cornacchiole"')
        sys.exit(0)
    for t in termini:
        r = cerca(t, idx)
        print('%-44s %d atti%s' % (t, len(r), ': ' + ', '.join(r[:4]) if r else ''))

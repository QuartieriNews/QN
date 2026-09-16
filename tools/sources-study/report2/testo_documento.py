# Il testo integrale di un documento, a partire dal suo identificativo.
# Serve a chi audita: giudicare due righe sulle sintesi da' una precisione del 31% dove leggere i
# testi la da' del 52%, perche' ogni atto produce **una riga sola** la cui sintesi racconta un punto
# solo dell'ordine del giorno.
# Il percorso non si ricava dall'url in un modo solo: gli item scaricati sono salvati con nomi che
# seguono convenzioni diverse a seconda della fonte, e dodici documenti su novantotto risultavano
# «testo non recuperabile» semplicemente perche' cercati con la regola sbagliata. La regola sullo
# slug l'ha trovata il revisore del secondo audit; qui e' portata dentro la pipeline, cosi' il
# prossimo non deve riscoprirla.
import csv, glob, html, os, re

NET = os.environ['QN_NET']
_ITEMDIRS = ['C1_items', 'C2_items', 'C4_items', 'C5_items', 'E2_items', 'E3_items',
             'A1_items', 'A1_pages', 'E3_pages', 'C1_bloccate']

def _tsv(p, k, v):
    if not os.path.exists(p): return {}
    out = {}
    for r in csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'):
        out[r[k]] = r[v]
    return out

_DOC = {d['id']: d for d in csv.DictReader(open(NET + '/report1/db/documenti.csv', encoding='utf-8'))}
_MAN = {m['url']: m['name'] for m in csv.DictReader(open(NET + '/report2/manifest_report2.csv', encoding='utf-8'))}
_A1 = _tsv(NET + '/A1_june_text.tsv', 'url', 'text')
_E3 = _tsv(NET + '/E3_all_text.tsv', 'url', 'text')
# Per le registrazioni il «testo» e' la trascrizione, che non sta in nessuna delle cartelle degli
# item: sta in video/, con il nome del video. Senza questa riga il risolutore dichiarava
# «non trovato» su tutte e 265 le registrazioni lette, che e' il caso in cui serve di piu'.
_VID = {}
for _mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
    _p = NET + '/report2/' + _mf
    if os.path.exists(_p):
        for _m in csv.DictReader(open(_p, encoding='utf-8')):
            _VID[_m['item_id']] = _m['file']
_indice = None

def _testo_html(p):
    h = open(p, encoding='utf-8', errors='replace').read()
    h = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    h = html.unescape(re.sub(r'(?s)<[^>]+>', ' ', h))
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', h)).strip()

def _slug(u):
    return re.sub(r'[^a-z0-9]+', '_', u.rstrip('/').split('/')[-1].lower()).strip('_')

def _idx():
    global _indice
    if _indice is None:
        _indice = {}
        for d in _ITEMDIRS:
            for p in glob.glob(NET + '/' + d + '/*'):
                _indice.setdefault(os.path.basename(p).rsplit('.', 1)[0].lower(), p)
    return _indice

def testo(documento_id):
    """Il testo del documento e da dove viene, oppure (None, motivo). Il motivo si restituisce
    sempre: «non trovato» senza il perche' manda a cercare a caso."""
    d = _DOC.get(documento_id)
    if not d: return None, 'documento %s assente dal database' % documento_id
    if d['fonte'] in ('A3', 'A4'):
        item = documento_id.replace('A3_', 'V3_').replace('A4_', 'V4_')
        f = _VID.get(item)
        if f:
            for base in ('/video/', '/'):
                p = NET + base + f
                if os.path.exists(p):
                    return open(p, encoding='utf-8', errors='replace').read(), os.path.relpath(p, NET)
        return None, 'trascrizione non trovata per %s (item %s)' % (documento_id, item)
    u = d['url']
    nome = _MAN.get(u)
    if nome and os.path.exists(NET + '/A2_text/' + nome + '.txt'):
        return open(NET + '/A2_text/' + nome + '.txt', encoding='utf-8').read(), 'A2_text/' + nome + '.txt'
    for tab, etichetta in ((_A1, 'A1_june_text.tsv'), (_E3, 'E3_all_text.tsv')):
        if u in tab and tab[u].strip(): return tab[u], etichetta
    idx = _idx()
    for chiave in (_slug(u), re.sub(r'[^a-z0-9]+', '_', u.lower()).strip('_')):
        if chiave in idx:
            return _testo_html(idx[chiave]), os.path.relpath(idx[chiave], NET)
    m = re.search(r'([A-Z]{3}\d+)', u)   # gli item con un codice nell'url, salvati con altro nome
    if m:
        for k, p in idx.items():
            if m.group(1).lower() in k:
                return _testo_html(p), os.path.relpath(p, NET)
    return None, 'nessun file per %s (%s)' % (documento_id, u)

if __name__ == '__main__':
    import collections
    c = collections.Counter(); senza = []
    for did in _DOC:
        t, src = testo(did)
        c['trovato' if t else 'non trovato'] += 1
        if not t: senza.append((did, src))
    print('documenti: %d | testo trovato: %d | non trovato: %d'
          % (len(_DOC), c['trovato'], c['non trovato']))
    for did, motivo in senza[:15]: print('   %s  %s' % (did, motivo[:100]))

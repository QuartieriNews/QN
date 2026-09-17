# Versioni compatte di notizie_candidate e documenti per il caricamento su Drive (DEC-102 §4.2):
# dati per item, senza testi integrali. Una per fonte, perche' il connettore carica contenuto e
# non file, e un CSV intero non entra in una sola risposta.
import csv, os, re, collections
S = os.environ['QN_NET']; D = S + '/report1/db'

# 'sintesi' e 'note' restano fuori: sono la parte lunga e il file deve poter essere caricato.
# 'evidenza_locale' e 'report_origine' ci sono: senza la pagina un atto non e' verificabile, e
# senza il rapporto di origine non si distingue una riga del Report 1 da una del Report 2.
COLONNE = ['id', 'documento_id', 'fonte', 'report_origine', 'titolo', 'tipo', 'luoghi',
           'municipio', 'municipio_testo', 'zona', 'quartiere', 'quartiere_zu',
           'territorio_dedotto', 'tier_localizzazione', 'toponimo_da_verificare',
           'attribuzione_incerta', 'fuori_perimetro',
           'evidenza_url', 'evidenza_locale', 'data_fatto', 'data_pubblicazione', 'qualita',
           'dedup_stato', 'gemello_id', 'ragione_dedup', 'prima_fonte', 'vicenda_id', 'settimana']
COL_DOC = ['id', 'fonte', 'tipo', 'url', 'data_pubblicazione', 'titolo', 'municipi_meta',
           'caratteri', 'formato_item', 'metodo_estrazione', 'ocr_incerto', 'esito_lettura',
           'settimana', 'report_origine', 'letto_da']

def scrivi(nome, righe, campi):
    p = f'{D}/{nome}.csv'
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore'); w.writeheader(); w.writerows(righe)
    print('  %-32s %6d righe  %7d byte' % (nome + '.csv', len(righe), os.path.getsize(p)))

# La radice degli URL degli atti sta in fonti.base_url (schema §1.1), non ripetuta 1.983 volte:
# 188 KB su 617 solo per quella colonna, e il file va caricato passando per una risposta.
BASE = {r['codice']: r['base_url'] for r in csv.DictReader(open(D + '/fonti.csv', encoding='utf-8'))}
def accorcia(righe, campo):
    for r in righe:
        b = BASE.get(r['fonte'], '')
        if b and r.get(campo, '').startswith(b): r[campo] = r[campo][len(b):]
    return righe

n = list(csv.DictReader(open(D + '/notizie_candidate.csv', encoding='utf-8')))
accorcia(n, 'evidenza_url')

# Lo schema vuole in 'evidenza_locale' un localizzatore: 'p. N' per gli atti, '[mm:ss]' per le
# registrazioni, vuoto per le pagine HTML. I lettori del Report 1 ci hanno messo invece la frase
# della fonte che sostiene la notizia, su tutte e 1.227 le righe. La citazione resta nella tabella
# intera nello scratchpad; nella versione da caricare resta solo il localizzatore, perche' e'
# quello che rende verificabile la riga e perche' le citazioni pesano 173 KB su 1.3 MB.
LOCALIZZATORE = re.compile(r'^\s*(p\.|pag|pagina|\[\d{1,2}:\d{2})', re.I)
citazioni = 0
for r in n:
    v = (r.get('evidenza_locale') or '').strip()
    if v and not LOCALIZZATORE.match(v):
        r['evidenza_locale'] = ''; citazioni += 1
print('righe in cui evidenza_locale conteneva una citazione e non un localizzatore:', citazioni)
print('notizie compatte:')
scrivi('notizie_compatte', n, COLONNE)
for fonte in sorted({r['fonte'] for r in n}):
    scrivi('notizie_compatte_' + fonte, [r for r in n if r['fonte'] == fonte], COLONNE)
d = accorcia(list(csv.DictReader(open(D + '/documenti.csv', encoding='utf-8'))), 'url')
print('documenti compatti:')
scrivi('documenti_compatti', d, COL_DOC)
for fonte in sorted({r['fonte'] for r in d}):
    scrivi('documenti_compatti_' + fonte, [r for r in d if r['fonte'] == fonte], COL_DOC)

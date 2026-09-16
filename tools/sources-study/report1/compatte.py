# Versioni compatte di notizie_candidate e documenti per il caricamento su Drive (DEC-102 §4.2):
# dati per item, senza testi integrali. Una per fonte, perche' il connettore carica contenuto e
# non file, e un CSV intero non entra in una sola risposta.
import csv, os, collections
S = os.environ['QN_NET']; D = S + '/report1/db'

# 'sintesi' e 'note' restano fuori: sono la parte lunga e il file deve poter essere caricato.
# 'evidenza_locale' e 'report_origine' ci sono: senza la pagina un atto non e' verificabile, e
# senza il rapporto di origine non si distingue una riga del Report 1 da una del Report 2.
COLONNE = ['id', 'documento_id', 'fonte', 'report_origine', 'titolo_anonimizzato', 'tipo', 'luoghi',
           'municipio', 'municipio_testo', 'zona', 'tier_localizzazione', 'toponimo_da_verificare',
           'evidenza_url', 'evidenza_locale', 'data_fatto', 'data_pubblicazione', 'qualita',
           'dedup_stato', 'gemello_id', 'ragione_dedup', 'prima_fonte', 'vicenda_id', 'settimana']
COL_DOC = ['id', 'fonte', 'tipo', 'url', 'data_pubblicazione', 'titolo_anonimizzato', 'municipi_meta',
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
print('notizie compatte:')
scrivi('notizie_compatte', n, COLONNE)
for fonte in sorted({r['fonte'] for r in n}):
    scrivi('notizie_compatte_' + fonte, [r for r in n if r['fonte'] == fonte], COLONNE)
d = accorcia(list(csv.DictReader(open(D + '/documenti.csv', encoding='utf-8'))), 'url')
print('documenti compatti:')
scrivi('documenti_compatti', d, COL_DOC)
for fonte in sorted({r['fonte'] for r in d}):
    scrivi('documenti_compatti_' + fonte, [r for r in d if r['fonte'] == fonte], COL_DOC)

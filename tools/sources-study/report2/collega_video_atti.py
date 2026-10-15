import sys
# Collega ogni registrazione ai suoi atti, in modo esatto dove si puo' e dichiarato dove non si puo'.
# La chiave e' che il valore par2 in base64 dentro verbale_match/convocazione_match del censimento
# e' l'ultimo segmento del `name` dell'atto: quando c'e', l'abbinamento e' esatto. Quando manca,
# si elencano gli atti compatibili per Municipio e data, senza sceglierne uno.
# Le colonne del censimento non vengono toccate: questa e' una tabella a fianco.
import csv, os, re, collections
S = os.environ['QN_NET']; R2 = S + '/report2'
VERBALI = {'MMV', 'CMV', 'GMV', 'CPV'}
CONVOCAZIONI = {'MMC', 'CMC', 'CPC'}

atti = list(csv.DictReader(open(R2 + '/confronto_atti.csv', encoding='utf-8')))
per_chiave = {a['name'].split('_')[-1]: a for a in atti}
per_cella = collections.defaultdict(list)
for a in atti:
    m = re.match(r'(\d{2})/(\d{2})/(\d{4})', a['data'] or '')
    if m:
        per_cella[(a['municipio'], f'{m.group(3)}-{m.group(2)}-{m.group(1)}', a['tipologia'])].append(a['name'])

def par2(u):
    m = re.search(r'par2=([^&]+)', u or '')
    return m.group(1).rstrip('=') if m else ''

def municipio(t):
    """Il territorio di una registrazione. Gli organi centrali non hanno un Municipio: i loro
    atti stanno nel corpus con fonte CEN e municipio 'non indicato', e cercarli per Municipio
    non trovava nulla. Un lettore se n'e' accorto trovando a mano tre verbali CEN_CPV_* che
    questo programma dava per inesistenti."""
    t = t or ''
    m = re.search(r'Municipio\s+([IVX]+)', t)
    if m: return m.group(1)
    if 'Capitolin' in t: return 'non indicato'
    return ''

def compatibili(mun, data, tipi):
    out = []
    for t in tipi:
        out += per_cella.get((mun, data, t), [])
    return sorted(out)

righe = []
for mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
    p = R2 + '/' + mf
    if not os.path.exists(p): continue
    for v in csv.DictReader(open(p, encoding='utf-8')):
        mun, data = municipio(v['territorio']), v['data_seduta']
        r = {'item_id': v['item_id'], 'fonte': v.get('fonte', ''), 'territorio': v['territorio'],
             'data_seduta': data}
        for campo, tipi in (('verbale', VERBALI), ('convocazione', CONVOCAZIONI)):
            k = par2(v.get(campo + '_match', ''))
            atto = per_chiave.get(k)
            r[campo + '_esatto'] = atto['name'] if atto else ''
            r[campo + '_esatto_municipio'] = atto['municipio'] if atto else ''
            r[campo + '_dichiarato_non_letto'] = 'sì' if (k and not atto) else 'no'
            poss = compatibili(mun, data, tipi)
            r[campo + '_compatibili_n'] = len(poss)
            r[campo + '_compatibili'] = ';'.join(poss[:6])
            r[campo + '_incoerente'] = ('sì' if atto and mun and atto['municipio'] != mun else 'no')
        righe.append(r)

if not righe:
    sys.exit('collega_video_atti: nessuna registrazione da collegare (manifest assenti o vuoti)')
campi = list(righe[0].keys())
with open(R2 + '/video_atti.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=campi); w.writeheader(); w.writerows(righe)

def conta(c):
    return collections.Counter(r[c] for r in righe)
print('registrazioni collegate:', len(righe))
for campo in ('verbale', 'convocazione'):
    esatti = sum(1 for r in righe if r[campo + '_esatto'])
    inc = sum(1 for r in righe if r[campo + '_incoerente'] == 'sì')
    fantasma = sum(1 for r in righe if r[campo + '_dichiarato_non_letto'] == 'sì')
    uno = sum(1 for r in righe if not r[campo + '_esatto'] and r[campo + '_compatibili_n'] == 1)
    molti = sum(1 for r in righe if not r[campo + '_esatto'] and r[campo + '_compatibili_n'] > 1)
    zero = sum(1 for r in righe if not r[campo + '_esatto'] and r[campo + '_compatibili_n'] == 0)
    print('%-13s esatti %3d (di cui di un altro Municipio %d) | dichiarati ma non fra gli atti letti %d'
          % (campo, esatti, inc, fantasma))
    print('%-13s senza abbinamento: %3d con un solo atto compatibile, %3d con piu di uno, %3d con nessuno'
          % ('', uno, molti, zero))

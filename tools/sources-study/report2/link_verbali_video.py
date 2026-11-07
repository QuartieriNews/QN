# Alcuni verbali scrivono dentro l'atto il link alla registrazione della seduta.
# Dove il link e' della forma .../watch/vod/<guid>, quel guid e' l'identificativo del video:
# l'abbinamento atto-registrazione e' dichiarato dalla fonte, non ricostruito da noi, e vale
# come riscontro indipendente per misurare il censimento e il collegamento per Municipio+data.
# Non tutti i link servono a questo: vedi FORMA piu' sotto.
#
# Attenzione alla chiave: nel manifest il video_id di una commissione e' 'comm_' + i primi 8
# esadecimali del guid, non il guid intero. Confrontare le due stringhe cosi' come sono da'
# zero riscontri su ogni item, che e' un difetto della chiave e non della fonte.
import csv, os, re, collections

S = os.environ['QN_NET']; R2 = S + '/report2'
GUID = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

def forma(prefisso):
    """Le tre forme trovate valgono cose diverse:
    vod     -> identificativo della singola seduta, l'unico che abbina atto e registrazione;
    catalog -> il catalogo del Municipio, sempre lo stesso: dice che la registrazione esiste,
               non quale sia;
    live    -> il canale della diretta, pubblicato nella convocazione: identifica l'organo,
               non la seduta."""
    if 'vod' in prefisso: return 'vod'
    if 'catalog' in prefisso: return 'catalogo'
    if 'live' in prefisso: return 'diretta'
    return 'altro'

def chiave(video_id):
    v = video_id or ''
    return (v[5:] if v.startswith('comm_') else v[:8]).lower()

corpus = {}
for r in csv.DictReader(open(R2 + '/manifest_video_rtv.csv', encoding='utf-8')):
    corpus[chiave(r['video_id'])] = r
collegamenti = {r['item_id']: r for r in csv.DictReader(open(R2 + '/video_atti.csv', encoding='utf-8'))}

righe = []
for f in sorted(os.listdir(S + '/A2_text')):
    testo = open(S + '/A2_text/' + f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'(\S*?)/?(' + GUID + r')', testo):
        g = m.group(2).lower()
        item = corpus.get(g[:8]) if forma(m.group(1)) == 'vod' else None
        righe.append({
            'atto': f[:-4],
            'municipio': f.split('_')[2],
            'tipologia': f.split('_')[1],
            'forma': forma(m.group(1)),
            'guid8': g[:8],
            'item_id': item['item_id'] if item else '',
            'data_seduta': item['data_seduta'] if item else '',
        })

with open(R2 + '/link_verbali_video.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['atto', 'municipio', 'tipologia', 'forma', 'guid8', 'item_id', 'data_seduta'])
    w.writeheader(); w.writerows(righe)

vod = [r for r in righe if r['forma'] == 'vod']
risolti = [r for r in vod if r['item_id']]
print('atti che scrivono un identificativo:', len(righe), 'su 1.983')
print('per forma:', collections.Counter(r['forma'] for r in righe))
print('per Municipio:', collections.Counter(r['municipio'] for r in righe))
print('guid distinti per forma:', {k: len({r['guid8'] for r in righe if r['forma'] == k})
                                   for k in {r['forma'] for r in righe}})
print('link di seduta risolti a un item del corpus:', len(risolti), 'su', len(vod))

# Il riscontro: sui casi in cui la fonte dichiara l'abbinamento, cosa dicevano censimento
# e collegamento per Municipio+data.
cens = sum(1 for r in risolti if (corpus[r['guid8']]['verbale_match'] or '').strip())
dentro = uniche = 0
for r in risolti:
    c = collegamenti.get(r['item_id'], {})
    comp = [x for x in (c.get('verbale_compatibili') or '').split(';') if x]
    if r['atto'] in comp:
        dentro += 1
        if len(comp) == 1: uniche += 1
print('  di questi, dichiarati dal censimento:', cens)
print('  con il verbale vero fra i compatibili per Municipio+data:', dentro)
print('  in cui il compatibile era gia\' unico:', uniche)

# Rigenera il manifest delle registrazioni RomaTV man mano che il driver ASR avanza.
# La regola che non si negozia: **gli identificativi gia' assegnati non cambiano mai**. I lotti letti
# citano V3_057 nei propri file e nel proprio log; rinumerare vorrebbe dire invalidare in silenzio
# tutto il lavoro fatto. Le registrazioni nuove prendono i numeri liberi, in coda.
# Il resto dei campi si rilegge dalle fonti ogni volta: il catalogo per i metadati, l'indice delle
# trascrizioni per le misure. Cosi' una correzione a monte arriva nel manifest senza modifiche a mano.
import csv, glob, json, os, re

NET = os.environ['QN_NET']
V = NET + '/video'
MAN = NET + '/report2/manifest_video_rtv.csv'
CAMPI = ['item_id', 'fonte', 'video_id', 'territorio', 'organo', 'data_seduta', 'data_pubblicazione',
         'durata_hm', 'parole', 'quota_ripetuta', 'url', 'file', 'origine_trascrizione',
         'grana_marcatore_s', 'confidenza_mediana', 'verbale_match', 'convocazione_match', 'lacuna']

# Le lacune note di una registrazione si dichiarano riga per riga, e sopravvivono alla
# rigenerazione perche' stanno qui e non nel file. Un lettore che non sa che mancano dieci secondi
# in coda li cerca, e non li trova, e non sa se e' colpa sua.
LACUNE = {
    '41e7b841': 'ultimi ~10 secondi assenti: il CDN non serve l\'ultimo segmento (58 su 59 scaricati)',
}
GUID = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')

def chiave(video_id):
    v = video_id or ''
    return (v[5:] if v.startswith('comm_') else v[:8]).lower()

# --- quello che c'e' gia': id e valori che nessuno deve toccare
# Gli identificativi si rileggono da **tutti e due** i file: quello in finestra e quello fuori.
# Leggendo solo il primo, una registrazione spostata fuori finestra perdeva il proprio numero e ne
# riceveva uno nuovo alla rigenerazione successiva — lo stesso difetto di posizione che il registro
# degli id ha appena tolto dal database, ricomparso qui.
vecchie = {}
for f_man in (MAN, NET + '/report2/manifest_video_rtv_fuori_finestra.csv'):
    if os.path.exists(f_man):
        for r in csv.DictReader(open(f_man, encoding='utf-8')):
            vecchie[chiave(r['video_id'])] = r
usati = {int(r['item_id'].split('_')[1]) for r in vecchie.values()}

# --- il catalogo: metadati della fonte
cat = {}
for f in glob.glob(V + '/rtv/cat/*.json'):
    terr = os.path.basename(f)[:-5].replace('_', ' ')
    for rec in json.load(open(f, encoding='utf-8')):
        g = (rec.get('guid') or '').lower()
        if g: cat[g[:8]] = (terr, rec)

# --- l'indice delle trascrizioni: le misure
idx = {}
p = V + '/rtv/indice_rtv.csv'
if os.path.exists(p):
    for r in csv.DictReader(open(p, encoding='utf-8')):
        idx[chiave(r['item'])] = r

def hm(d):
    m = re.match(r'(\d+):(\d+):', d or '')
    return '%d:%02d' % (int(m.group(1)), int(m.group(2))) if m else ''

def smil(rec):
    for s in rec.get('smilFiles') or []:
        if s.get('smilFileType') == 'AudioOnly': return s.get('url', '')
    return ''

# --- le trascrizioni presenti: sono loro a dire che cosa entra nel manifest
righe, nuovi = [], 0
for t in sorted(os.listdir(V + '/rtv/txt')):
    if not t.endswith('.txt'): continue
    vid = t[:-4]; k = chiave(vid)
    vecchia = vecchie.get(k)
    if vecchia:
        item = vecchia['item_id']
    else:
        n = 1
        while n in usati: n += 1
        usati.add(n); item = 'V3_%03d' % n; nuovi += 1
    terr, rec = cat.get(k, ('', {}))
    m = idx.get(k, {})
    riga = {
        'item_id': item, 'fonte': 'A3', 'video_id': vid,
        'territorio': terr or (vecchia or {}).get('territorio', ''),
        # `organo` resta com'era dove c'era: i lotti gia' letti lo citano.
        'organo': (vecchia or {}).get('organo') or (rec.get('title', '') if 'CONSIGLIO' in (rec.get('title') or '').upper() else ''),
        'data_seduta': (rec.get('referenceDate') or '')[:10] or (vecchia or {}).get('data_seduta', ''),
        'data_pubblicazione': (rec.get('insertDate') or '')[:10] or (vecchia or {}).get('data_pubblicazione', ''),
        'durata_hm': hm(rec.get('duration')) or (vecchia or {}).get('durata_hm', ''),
        'parole': m.get('parole', '') or (vecchia or {}).get('parole', ''),
        'quota_ripetuta': m.get('quota_ripetuta', '') or (vecchia or {}).get('quota_ripetuta', ''),
        'url': smil(rec) or (vecchia or {}).get('url', ''),
        'file': 'rtv/txt/' + vid + '.txt',
        'origine_trascrizione': m.get('origine', '') or (vecchia or {}).get('origine_trascrizione', ''),
        'grana_marcatore_s': m.get('grana_marcatore_s', '') or (vecchia or {}).get('grana_marcatore_s', ''),
        'confidenza_mediana': m.get('confidenza_mediana', '') or (vecchia or {}).get('confidenza_mediana', ''),
        # Le due colonne del censimento restano vuote come sono sempre state: il censimento RomaTV
        # non dichiara abbinamenti, e riempirle con una nostra deduzione le farebbe passare per
        # dichiarazioni della fonte. Il collegamento sta a fianco, in video_atti.csv.
        'verbale_match': (vecchia or {}).get('verbale_match', ''),
        'convocazione_match': (vecchia or {}).get('convocazione_match', ''),
        'lacuna': LACUNE.get(k, ''),
    }
    righe.append(riga)

# Il perimetro dello studio e' 8-28 giugno: le registrazioni fuori finestra non entrano nel
# manifest, ma non spariscono in silenzio — si scrivono a parte, cosi' chi guarda sa che esistono e
# perche' non sono state lette.
FUORI = NET + '/report2/manifest_video_rtv_fuori_finestra.csv'
dentro = [r for r in righe if '2026-06-08' <= (r['data_seduta'] or '')[:10] <= '2026-06-28']
fuori = [r for r in righe if r not in dentro]
if fuori:
    with open(FUORI, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPI); w.writeheader(); w.writerows(fuori)
righe = dentro

righe.sort(key=lambda r: (r['data_seduta'], r['item_id']))
if os.path.exists(MAN): os.replace(MAN, MAN + '.prima_della_rigenerazione')
with open(MAN, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=CAMPI); w.writeheader(); w.writerows(righe)

# Un avviso che non distingue fra «sparita» e «spostata fuori finestra» spaventa per niente: le
# righe uscite dal manifest perche' la seduta e' dell'1-7 giugno stanno nel file a parte, e non
# vanno confuse con una trascrizione che manca davvero.
fuori_chiavi = {chiave(r['video_id']) for r in fuori}
persi = set(vecchie) - {chiave(r['video_id']) for r in righe} - fuori_chiavi
print('registrazioni nel manifest: %d (prima %d) | identificativi nuovi: %d'
      % (len(righe), len(vecchie), nuovi))
if fuori:
    print('fuori dalla finestra 8-28 giugno, elencate a parte: %d' % len(fuori))
print('identificativi conservati: %d' % (len(righe) - nuovi))
if persi:
    print('ATTENZIONE: %d righe del manifest precedente non hanno piu\' una trascrizione: %s'
          % (len(persi), ', '.join(sorted(vecchie[k]['item_id'] for k in persi))))

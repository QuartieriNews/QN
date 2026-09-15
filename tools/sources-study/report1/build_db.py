# Builds the Report 1 database from the readers' output, per docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md
# (schema corrected after Codex control C1). Five tables in report1/db/: fonti, documenti,
# notizie_candidate, vicende, territori. Deterministic and re-runnable: no network, no model calls.
import csv, glob, os, re, sys, datetime, collections, random
sys.path.insert(0, os.environ['QN_NET'])
import geo_lookup as geo

S = os.environ['QN_NET']; R = S + '/report1'; D = R + '/db'
os.makedirs(D, exist_ok=True)

ORDINE_FONTI = ['A1', 'A2', 'C1', 'C2', 'C4', 'C5', 'E2', 'E3']
BLOCCO = {'A1': 'Amministrazione', 'A2': 'Amministrazione', 'C1': 'Cronaca', 'C2': 'Cronaca',
          'C4': 'Cronaca', 'C5': 'Cronaca', 'E2': 'Eventi', 'E3': 'Eventi'}

def settimana(iso):
    """Week of June 2026 by publication date, Europe/Rome (schema §1.2). W2-W4 = 8-28 June."""
    if not iso or not re.match(r'\d{4}-\d{2}-\d{2}', iso[:10]): return ''
    try: d = datetime.date.fromisoformat(iso[:10])
    except ValueError: return ''
    if (d.year, d.month) != (2026, 6): return ''
    return str(1 if d.day <= 7 else 2 if d.day <= 14 else 3 if d.day <= 21 else 4 if d.day <= 28 else 5)

# ---- documenti -------------------------------------------------------------
man = list(csv.DictReader(open(R + '/manifest_report1.csv', encoding='utf-8')))
documenti = {}
for r in man:
    documenti[r['id']] = {
        'id': r['id'], 'fonte': r['fonte'], 'tipo': r.get('tipo', ''), 'url': r['url'],
        'data_pubblicazione': r.get('data_pubblicazione', ''), 'timestamp_pubblicazione': '',
        'data_evento_inizio': r.get('data_evento_inizio', ''), 'data_evento_fine': r.get('data_evento_fine', ''),
        'titolo_anonimizzato': '', 'municipi_meta': r.get('municipi_meta', ''),
        'tematica': r.get('tematica', ''), 'caratteri': r.get('caratteri', ''),
        'formato_item': 'HTML', 'metodo_estrazione': 'nativo', 'ocr_incerto': '',
        'trascrizione_incerta': '', 'esito_lettura': 'completo',
        'settimana': settimana(r.get('data_pubblicazione', '')), 'report_origine': '1', 'letto_da': '',
    }
# A timestamp is only real where the inventory carried one (C2 does, the others do not).
for fn, fonte in (('C2_2026-06_items.csv', 'C2'),):
    for r in csv.DictReader(open(f'{S}/deliver/{fn}', encoding='utf-8')):
        m = re.match(r'(\d{2})/(\d{2})/(\d{4})\s+(\d{2}:\d{2})', r['data_pubblicazione'] or '')
        if not m: continue
        iso = f'{m.group(3)}-{m.group(2)}-{m.group(1)}T{m.group(4)}:00+02:00'
        for d in documenti.values():
            if d['fonte'] == fonte and d['url'] == r['url']: d['timestamp_pubblicazione'] = iso

# ---- notizie_candidate -----------------------------------------------------
letti = {}
for f in sorted(glob.glob(R + '/out/L*_notizie.csv')):
    if '_senza_' in f: continue
    lotto = os.path.basename(f)[:3]
    for r in csv.DictReader(open(f, encoding='utf-8')):
        letti.setdefault(r['documento_id'], []).append((lotto, r))

notizie = []
for doc_id in sorted(letti):
    for lotto, r in letti[doc_id]:
        doc = documenti.get(doc_id)
        if not doc: print('ORFANA', doc_id); continue
        doc['letto_da'] = lotto
        if not doc['titolo_anonimizzato']: doc['titolo_anonimizzato'] = r['titolo_anonimizzato']
        # Localisation (schema §2 rule 4): the source's Municipio prevails; a disagreement with the
        # text is recorded as a toponym to verify, never silently resolved.
        loc = geo.localise(' '.join([r.get('luoghi', ''), r.get('sintesi', ''), r.get('titolo_anonimizzato', '')]))
        mun_testo = [m for m in re.split(r'[;,]', r.get('municipio_testo', '')) if m.strip()]
        mun_meta = [m for m in re.split(r'[;,]', doc['municipi_meta']) if m.strip()]
        mun_fonte = [m.strip() for m in (mun_meta or mun_testo)]
        discorde = bool(mun_testo and mun_meta and {m.strip() for m in mun_testo} != {m.strip() for m in mun_meta})
        topo_v = r.get('toponimo_da_verificare', '').strip().lower() in ('sì', 'si') or discorde
        notizie.append({
            'id': '', 'documento_id': doc_id, 'fonte': r['fonte'],
            'titolo_anonimizzato': r['titolo_anonimizzato'], 'sintesi': r['sintesi'], 'tipo': r['tipo'],
            'luoghi': r.get('luoghi', ''), 'municipio': ';'.join(mun_fonte),
            'zona': loc.get('zone') or '' if isinstance(loc, dict) else '',
            'tier_localizzazione': (loc.get('tier') or 'assente') if isinstance(loc, dict) else 'assente',
            'toponimo_da_verificare': 'sì' if topo_v else 'no',
            'evidenza_url': r['evidenza_url'], 'evidenza_locale': r.get('evidenza_locale', ''),
            'data_fatto': r.get('data_fatto', ''), 'data_pubblicazione': r.get('data_pubblicazione', '') or doc['data_pubblicazione'],
            'disponibilita': r.get('disponibilita', ''), 'qualita': r['qualita'],
            'dedup_stato': 'unica', 'gemello_id': '', 'ragione_dedup': '', 'prima_fonte': 'sì',
            'vicenda_id': '', 'integra_gemello_id': '', 'campi_integrati': '',
            'settimana': settimana(r.get('data_fatto', '') or doc['data_pubblicazione']),
            'report_origine': '1', 'verifica_seconda_ai': 'non eseguita',
            'municipio_testo': ';'.join(m.strip() for m in mun_testo), 'note': r.get('note', ''),
        })
for k, n in enumerate(notizie, 1): n['id'] = f'N{k:04d}'
print(len(notizie), 'notizie candidate da', len(letti), 'documenti letti')
loc_t = collections.Counter(n['tier_localizzazione'] for n in notizie)
print('localizzazione:', dict(loc_t))
print('con Municipio:', sum(1 for n in notizie if n['municipio']), '| toponimo da verificare:', sum(1 for n in notizie if n['toponimo_da_verificare'] == 'sì'))

# ---- deduplicazione (metodo §4.1, schema §2 regola 2) ----------------------
# Three conditions, in order: (a) date within +/-1 day, (b) place, (c) object. (a)+(b) without (c)
# is a doubt, never a merge: the yield is then reported as a range.
TIPO_AFFINE = {'evento': 'evento', 'convegno': 'evento', 'avviso': 'avviso',
               'delibera': 'atto', 'mozione': 'atto', 'risoluzione': 'atto',
               'ordine del giorno': 'atto', 'interrogazione': 'atto'}

def giorno(n):
    d = n['data_fatto'] or n['data_pubblicazione']
    try: return datetime.date.fromisoformat(d[:10])
    except (ValueError, TypeError): return None

def toponimi(n):
    return {geo.norm(t) for t in re.split(r'[;,]', n['luoghi']) if len(geo.norm(t)) > 3}

def stesso_luogo(a, b):
    """Method §4.1 condition (b): same normalised toponym, or same Municipio *only when neither
    side has a finer toponym*. Falling back to the Municipio whenever the zone is empty made two
    unrelated events in the same Municipio on the same day look like the same fact."""
    za, zb = a['zona'].strip(), b['zona'].strip()
    if za and zb: return za == zb
    ta, tb = toponimi(a), toponimi(b)
    if ta and tb: return bool(ta & tb)
    if ta or tb: return False
    ma, mb = a['municipio'].strip(), b['municipio'].strip()
    return bool(ma) and ma == mb

def parole(s):
    return {w for w in geo.norm(s).split() if len(w) > 3}

def stesso_oggetto(a, b):
    if TIPO_AFFINE.get(a['tipo'], a['tipo']) != TIPO_AFFINE.get(b['tipo'], b['tipo']): return False
    pa, pb = parole(a['titolo_anonimizzato'] + ' ' + a['luoghi']), parole(b['titolo_anonimizzato'] + ' ' + b['luoghi'])
    if not pa or not pb: return False
    return len(pa & pb) / min(len(pa), len(pb)) >= 0.6

# Blocks under 300 items in the level-1 sources are deduplicated over the whole month and the
# yield is measured; above it, a sample of at least 60 per pair and the yield is estimated.
per_blocco = collections.Counter(BLOCCO[n['fonte']] for n in notizie)
coppie, dubbi = 0, 0
for blocco in sorted(per_blocco):
    gruppo = [n for n in notizie if BLOCCO[n['fonte']] == blocco]
    fonti_blocco = sorted({n['fonte'] for n in gruppo})
    item_blocco = len({n['documento_id'] for n in gruppo})
    campionato = item_blocco > 300 and len(fonti_blocco) > 1
    if campionato:
        # At least 60 items per pair of sources, seed recorded in the report (method §4.1).
        seed = '2026-06-' + 'x'.join(fonti_blocco)
        quota = max(60, 60 * (len(fonti_blocco) * (len(fonti_blocco) - 1) // 2))
        random.Random(seed).shuffle(gruppo)
        gruppo = gruppo[:max(quota, 0)]
        print(f'  campione seed={seed}, {len(gruppo)} notizie')
    for i, a in enumerate(gruppo):
        if a['dedup_stato'] != 'unica': continue
        ga = giorno(a)
        for b in gruppo[i + 1:]:
            if b['dedup_stato'] != 'unica' or b['documento_id'] == a['documento_id']: continue
            gb = giorno(b)
            if not ga or not gb or abs((ga - gb).days) > 1: continue
            if not stesso_luogo(a, b): continue
            if stesso_oggetto(a, b):
                b['dedup_stato'] = 'duplicato'; coppie += 1
                b['ragione_dedup'] = 'data ±1 giorno, stesso luogo, stesso oggetto'
            else:
                b['dedup_stato'] = 'dubbio'; dubbi += 1
                b['ragione_dedup'] = 'data ±1 giorno e stesso luogo; oggetto incerto'
                b['prima_fonte'] = 'non applicabile'
            b['gemello_id'] = a['id']
            if b['dedup_stato'] == 'duplicato': b['prima_fonte'] = 'no'
    print(f'{blocco}: {len(gruppo)} notizie, {"campione" if campionato else "intero mese"}')

# ---- vicende (schema §2 regola 3) -----------------------------------------
vicende = []
for n in notizie:
    if n['dedup_stato'] == 'unica' or not n['gemello_id']: continue
    capo = next((x for x in notizie if x['id'] == n['gemello_id']), None)
    if not capo: continue
    vid = capo['vicenda_id'] or f'V{len(vicende) + 1:03d}'
    if not capo['vicenda_id']:
        capo['vicenda_id'] = vid
        vicende.append({'id': vid, 'titolo_anonimizzato': capo['titolo_anonimizzato'], 'tipo': capo['tipo'],
                        'municipio': capo['municipio'], 'zona': capo['zona'],
                        'prima_pubblicazione': capo['data_pubblicazione'], 'ultima_pubblicazione': capo['data_pubblicazione'],
                        'n_notizie': 1, 'fonti': capo['fonte'],
                        'confidenza': 'media', 'solo_report2': 'no', 'stato': 'non verificato'})
    n['vicenda_id'] = vid
    v = next(x for x in vicende if x['id'] == vid)
    v['n_notizie'] += 1
    v['fonti'] = ';'.join(sorted(set(v['fonti'].split(';')) | {n['fonte']}))
    v['ultima_pubblicazione'] = max(v['ultima_pubblicazione'], n['data_pubblicazione'] or '')
    v['confidenza'] = 'alta' if n['dedup_stato'] == 'duplicato' else 'bassa'

# ---- territori -------------------------------------------------------------
territori = {}
for n in notizie:
    for mun in (n['municipio'].split(';') if n['municipio'] else ['non localizzato']):
        k = (mun.strip() or 'non localizzato', n['settimana'] or '')
        t = territori.setdefault(k, {'municipio': k[0], 'settimana': k[1], 'n_documenti': set(),
                                     'n_notizie': 0, 'n_notizie_alta': 0, 'n_notizie_media': 0,
                                     'n_notizie_bassa': 0, 'fonti_presenti': set(), 'ritardi': []})
        t['n_documenti'].add(n['documento_id']); t['n_notizie'] += 1
        t['n_notizie_' + n['qualita']] = t.get('n_notizie_' + n['qualita'], 0) + 1
        t['fonti_presenti'].add(n['fonte'])
        gf, gp = n['data_fatto'], n['data_pubblicazione']
        try: t['ritardi'].append((datetime.date.fromisoformat(gp[:10]) - datetime.date.fromisoformat(gf[:10])).days)
        except (ValueError, TypeError): pass

def scrivi(nome, righe, campi):
    with open(f'{D}/{nome}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore'); w.writeheader(); w.writerows(righe)
    print(f'  {nome}.csv: {len(righe)} righe')

fonti = []
for cod in ORDINE_FONTI:
    docs = [d for d in documenti.values() if d['fonte'] == cod]
    if not docs: continue
    fonti.append({'codice': cod, 'nome': cod, 'blocco': BLOCCO[cod], 'ente': '', 'url_elenco': '',
                  'base_url': 'https://www.comune.roma.it/web/it/' if cod == 'E3' else '',
                  'formato': 'HTML', 'item_giugno': len(docs), 'paginazione_completa': 'sì',
                  'data_lettura': '2026-09-15', 'report': '1', 'note': ''})

terr_righe = []
for k in sorted(territori):
    t = territori[k]; r = dict(t)
    r['n_documenti'] = len(t['n_documenti']); r['fonti_presenti'] = ';'.join(sorted(t['fonti_presenti']))
    rit = sorted(t['ritardi'])
    r['mediana_giorni_pubblicazione'] = rit[len(rit) // 2] if len(rit) >= 3 else ''
    r['lacuna'] = 'no'
    terr_righe.append(r)

print('tabelle scritte in report1/db/:')
scrivi('fonti', fonti, ['codice','nome','blocco','ente','url_elenco','base_url','formato','item_giugno','paginazione_completa','data_lettura','report','note'])
scrivi('documenti', list(documenti.values()), ['id','fonte','tipo','url','data_pubblicazione','timestamp_pubblicazione','data_evento_inizio','data_evento_fine','titolo_anonimizzato','municipi_meta','tematica','caratteri','formato_item','metodo_estrazione','ocr_incerto','trascrizione_incerta','esito_lettura','settimana','report_origine','letto_da'])
scrivi('notizie_candidate', notizie, ['id','documento_id','fonte','titolo_anonimizzato','sintesi','tipo','luoghi','municipio','municipio_testo','zona','tier_localizzazione','toponimo_da_verificare','evidenza_url','evidenza_locale','data_fatto','data_pubblicazione','disponibilita','qualita','dedup_stato','gemello_id','ragione_dedup','prima_fonte','vicenda_id','integra_gemello_id','campi_integrati','settimana','report_origine','verifica_seconda_ai','note'])
scrivi('vicende', vicende, ['id','titolo_anonimizzato','tipo','municipio','zona','prima_pubblicazione','ultima_pubblicazione','n_notizie','fonti','confidenza','solo_report2','stato'])
scrivi('territori', terr_righe, ['municipio','settimana','n_documenti','n_notizie','n_notizie_alta','n_notizie_media','n_notizie_bassa','fonti_presenti','mediana_giorni_pubblicazione','lacuna'])
d = collections.Counter(n['dedup_stato'] for n in notizie)
print('dedup:', dict(d), '| netta minima:', sum(1 for n in notizie if n['dedup_stato']=='unica'), '| netta massima:', sum(1 for n in notizie if n['dedup_stato'] in ('unica','dubbio')))

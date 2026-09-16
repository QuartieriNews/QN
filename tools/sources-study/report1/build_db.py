# Builds the Report 1 database from the readers' output, per docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md
# (schema corrected after Codex control C1). Five tables in report1/db/: fonti, documenti,
# notizie_candidate, vicende, territori. Deterministic and re-runnable: no network, no model calls.
import csv, glob, json, os, re, sys, datetime, collections, random
sys.path.insert(0, os.environ['QN_NET'])
import geo_lookup as geo

S = os.environ['QN_NET']; R = S + '/report1'; D = R + '/db'
os.makedirs(D, exist_ok=True)

A2_BASE = 'https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/showPdfDoc?fun=deliberazioniAtti&par1='
ORDINE_FONTI = ['A1', 'A2', 'A3', 'A4', 'C1', 'C2', 'C4', 'C5', 'E2', 'E3']
BLOCCO = {'A1': 'Amministrazione', 'A2': 'Amministrazione',
          'A3': 'Amministrazione', 'A4': 'Amministrazione', 'C1': 'Cronaca', 'C2': 'Cronaca',
          'C4': 'Cronaca', 'C5': 'Cronaca', 'E2': 'Eventi', 'E3': 'Eventi'}

ANNUNCIATI = {'avviso', 'ordine del giorno', 'convegno', 'interrogazione'}
def qualita(r):
    """An announced fact never reaches 'alta', and neither does one whose date the text did not
    give: the readers applied the scale by hand and drifted on exactly these two cases."""
    q = r['qualita']
    if q == 'alta' and (r['tipo'] in ANNUNCIATI or not r.get('data_fatto')): return 'media'
    return q

ROMANI = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV']
def norm_mun(valore):
    """Roman numerals only, as the schema requires: 'Municipio IX' and 'Roma IX' both give 'IX'."""
    out = []
    for pezzo in re.split(r'[;,]', valore or ''):
        t = re.sub(r'(?i)\b(municipio|roma)\b', ' ', pezzo).strip().upper()
        if t in ROMANI and t not in out: out.append(t)
    return out

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
# An item read twice keeps only its latest reading. The re-read batch (L26) applies rules that
# were decided after the first batches ran, so its rows supersede theirs; without this, every
# re-read item would contribute its news twice and inflate the whole database.
letti = {}
# I lotti si confrontano come stringhe, e questo vale **solo** perche' sono a due cifre con lo zero
# davanti (L01, non L1): con L9 e L10 vincerebbe il nono. Il C5 l'ha segnalato come difetto; sui
# nostri nomi non lo e', ma basta un lotto chiamato male per farlo diventare tale, quindi qui si
# controlla invece di fidarsi della convenzione.
for f in sorted(glob.glob(R + '/out/L*_notizie.csv')):
    if '_senza_' in f: continue
    lotto = os.path.basename(f)[:3]
    if not re.fullmatch(r'L\d\d', lotto):
        sys.exit('lotto con nome fuori convenzione: %s — l\'ordinamento fra lotti non sarebbe affidabile' % lotto)
    for r in csv.DictReader(open(f, encoding='utf-8')):
        prec = letti.get(r['documento_id'])
        if prec and prec[0][0] > lotto: continue      # an earlier file cannot override a later batch
        if prec and prec[0][0] < lotto: letti[r['documento_id']] = []   # later batch wins: drop the old rows
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
        mun_testo = norm_mun(r.get('municipio_testo', ''))
        mun_meta = norm_mun(doc['municipi_meta'])
        # The text's Municipio is about this news; the source's tag is about the page, and on A1 it
        # is often the portal's whole category list (up to all fifteen). So: the text wins when it
        # says something, and a tag naming more than three Municipi is a category, not a location.
        if mun_testo: mun_fonte = mun_testo
        elif len(mun_meta) <= 3: mun_fonte = mun_meta
        else: mun_fonte = []
        discorde = bool(mun_testo and mun_meta and set(mun_testo) != set(mun_meta))
        # geo_lookup returns 'zona' and 'municipio'. Reading a key that does not exist ('zone')
        # left the zone empty for the whole database and quietly denied the deduplication its
        # finest place key, and the gazetteer's own Municipio was never used at all.
        zona = loc.get('zona') or ''
        tier = loc.get('tier') or ''
        mun_gaz = loc.get('municipio') or ''
        if not mun_fonte and mun_gaz and not mun_gaz.startswith('multi'):
            mun_fonte = [mun_gaz]                      # the gazetteer localises where the source said nothing
            if not tier: tier = 'text_contains'
        if not tier: tier = 'assente'
        if tier == 'text_contains' and not zona and not mun_fonte: tier = 'ambiguous'
        irrisolto = bool(r.get('luoghi', '').strip()) and not zona and not mun_fonte
        topo_v = (r.get('toponimo_da_verificare', '').strip().lower() in ('sì', 'si')
                  or discorde or irrisolto)
        notizie.append({
            'id': '', 'documento_id': doc_id, 'fonte': r['fonte'],
            'titolo_anonimizzato': r['titolo_anonimizzato'], 'sintesi': r['sintesi'], 'tipo': r['tipo'],
            'luoghi': r.get('luoghi', ''), 'municipio': ';'.join(mun_fonte),
            'zona': zona, 'tier_localizzazione': tier,
            'toponimo_da_verificare': 'sì' if topo_v else 'no',
            'evidenza_url': r['evidenza_url'], 'evidenza_locale': r.get('evidenza_locale', ''),
            'data_fatto': r.get('data_fatto', ''), 'data_pubblicazione': r.get('data_pubblicazione', '') or doc['data_pubblicazione'],
            'disponibilita': r.get('disponibilita', ''), 'qualita': qualita(r),
            'dedup_stato': 'unica', 'gemello_id': '', 'ragione_dedup': '', 'prima_fonte': 'sì',
            'vicenda_id': '', 'integra_gemello_id': '', 'campi_integrati': '',
            # Lo schema §1.3 dice «come in documenti», cioe' dalla data di **pubblicazione**. Qui
            # usava la data del fatto: il rilievo e' del C5, verificato sullo schema. La settimana
            # dice quando la notizia e' stata resa disponibile, non quando il fatto e' accaduto, e
            # le lacune territoriali si leggono su quella.
            'settimana': settimana(doc['data_pubblicazione'] or r.get('data_fatto', '')),
            'report_origine': '1', 'verifica_seconda_ai': 'non eseguita',
            'municipio_testo': ';'.join(m.strip() for m in mun_testo), 'note': r.get('note', ''),
        })
for k, n in enumerate(notizie, 1): n['id'] = f'N{k:04d}'
print(len(notizie), 'notizie candidate da', len(letti), 'documenti letti')
loc_t = collections.Counter(n['tier_localizzazione'] for n in notizie)
print('localizzazione:', dict(loc_t))
print('con Municipio:', sum(1 for n in notizie if n['municipio']), '| toponimo da verificare:', sum(1 for n in notizie if n['toponimo_da_verificare'] == 'sì'))

# ---- Report 2: gli atti (fonte A2) ----------------------------------------
# Gli atti entrano nelle stesse cinque tabelle e passano per la stessa deduplicazione: il
# Report 2 non ha un database suo. Una regola di confronto tenuta in due copie diverge, e la
# domanda che il Report 2 deve poter rispondere — quali notizie gli atti aggiungono a quelle
# del Report 1 — si risponde solo se le due metà stanno nello stesso confronto.
R2 = S + '/report2'
ocr_a2 = corrotti_a2 = 0

# Il codice di tipologia della fonte non e' documentato: questa mappa e' ricavata leggendo un
# atto per ciascun codice (organo emittente e oggetto), non dedotta dalla sigla. I codici per
# cui nessun lotto ha ancora fornito un esempio finiscono in 'altro' e vengono stampati.
TIPO_ATTO = {
    'ACD': 'delibera', 'CMD': 'delibera', 'GCD': 'delibera', 'GMD': 'delibera', 'MCD': 'delibera',
    'OCD': 'delibera', 'CID': 'delibera',
    'AY': 'ordine del giorno', 'CMY': 'ordine del giorno',
    'CMC': 'ordine del giorno', 'CPC': 'ordine del giorno', 'MMC': 'ordine del giorno',
    'AZ': 'mozione', 'CMZ': 'mozione', 'CMR': 'risoluzione',
    'CMV': 'altro', 'CPV': 'altro', 'GMV': 'altro', 'MMV': 'altro',
    'GCM': 'altro', 'GMM': 'altro', 'GMT': 'altro', 'DMS': 'altro',
    'DDS': 'avviso',
}

def formato_atto(v):
    """I lettori hanno scritto il formato a parole, non con l'enum: otto formulazioni per due casi."""
    v = (v or '').lower()
    return 'PDF scansione' if ('ocr' in v or 'scansion' in v) else 'PDF testo'

def esito_atto(v):
    v = (v or '').lower()
    if not v or 'illeggibile' in v or 'non leggibile' in v or 'vuoto' in v: return 'fallito'
    if 'parzial' in v or 'in parte' in v: return 'parziale'
    return 'completo'

def sn(v):
    return 'sì' if (v or '').strip().lower() in ('sì', 'si', 'true', '1') else 'no'

CONVOCAZIONI_A2 = {'MMC', 'CMC', 'CPC'}

def data_del_fatto(tipologia, r, meta):
    """La data a cui il fatto appartiene, che per le convocazioni non e' quella di repertorio.
    Atti Web indicizza i verbali per la data della seduta e le convocazioni per la data del
    protocollo, che precede la seduta di giorni: usare il repertorio come data del fatto rende
    impossibile per costruzione l'accostamento fra una convocazione e la seduta che convoca,
    perche' la deduplicazione appaia a un giorno di distanza. Misurato sulle convocazioni gia'
    lette: 242 su 509 hanno una data di seduta diversa da quella di repertorio.
    Vale solo per le convocazioni: in altri tipi `validita_o_seduta` porta una validita', non una
    data di seduta, e leggerla come data del fatto sarebbe un errore peggiore di quello che
    corregge."""
    if tipologia in CONVOCAZIONI_A2:
        d = data_seduta(r.get('validita_o_seduta'))
        if d: return d
    return iso_it(r.get('data_repertorio')) or iso_it(meta['data'])

def data_seduta(v):
    """Una data sola dal campo della seduta, in qualunque delle due grafie i lettori l'abbiano
    scritta. Se il campo ne porta piu' d'una diversa non si sceglie: il fatto e' ambiguo e si
    ricade sul repertorio, dichiarandolo con il silenzio invece che con una scelta."""
    s = (v or '').strip()
    trovate = {f'{a}-{m}-{g}' for a, m, g in re.findall(r'(\d{4})-(\d{2})-(\d{2})', s)}
    trovate |= {f'{a}-{m}-{int(g):02d}' for g, m, a in re.findall(r'(\d{1,2})[/.](\d{2})[/.](\d{4})', s)}
    return trovate.pop() if len(trovate) == 1 else ''

def iso_it(v):
    m = re.match(r'(\d{2})/(\d{2})/(\d{4})', (v or '').strip())
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else ''

if os.path.isdir(R2 + '/out'):
    man2 = list(csv.DictReader(open(R2 + '/manifest_report2.csv', encoding='utf-8')))
    meta_atto = {r['name']: r for r in man2}
    # L'identificativo segue l'ordine del manifest, non quello dei lotti: cosi' non cambia
    # quando un lotto viene riletto.
    id_atto = {r['name']: f'A2_{k:04d}' for k, r in enumerate(man2, 1)}

    letti2 = {}
    for f in sorted(glob.glob(R2 + '/out/[BX]*_atti.csv')):
        lotto = os.path.basename(f)[:3]
        for r in csv.DictReader(open(f, encoding='utf-8')):
            letti2[r['name']] = (lotto, r)     # una rilettura successiva sostituisce la precedente

    sconosciuti = collections.Counter()
    n_r1 = len(notizie)
    for name in sorted(letti2, key=lambda x: id_atto.get(x, '')):
        lotto, r = letti2[name]
        meta = meta_atto.get(name)
        if not meta:
            print('ATTO SENZA MANIFEST', name); continue
        did = id_atto[name]
        tipo = TIPO_ATTO.get(meta['tipologia'])
        if tipo is None:
            tipo = 'altro'; sconosciuti[meta['tipologia']] += 1
        fmt = formato_atto(r.get('formato'))
        incerto = sn(r.get('ocr_incerto'))
        if incerto == 'sì':
            ocr_a2 += 1
            if fmt != 'PDF scansione': corrotti_a2 += 1
        documenti[did] = {
            'id': did, 'fonte': 'A2', 'tipo': 'atto', 'url': meta['url'],
            'data_pubblicazione': iso_it(meta['data']), 'timestamp_pubblicazione': '',
            'data_evento_inizio': '', 'data_evento_fine': '',
            'titolo_anonimizzato': r.get('oggetto_sintetico', ''),
            'municipi_meta': meta['municipio'] if meta['municipio'] != 'non indicato' else '',
            'tematica': meta['tipologia'], 'caratteri': meta.get('caratteri', ''),
            'formato_item': fmt, 'metodo_estrazione': 'OCR' if fmt == 'PDF scansione' else 'nativo',
            'ocr_incerto': incerto, 'trascrizione_incerta': '',
            'esito_lettura': esito_atto(r.get('esito_testo')), 'settimana': meta.get('settimana', ''),
            'report_origine': '2', 'letto_da': lotto,
        }
        if r.get('notizia_candidata', '').strip().lower() not in ('sì', 'si'): continue
        # Il Municipio del manifest e' il valore autorevole (regola 11 della specifica atti):
        # il gazetteer qui non lo sostituisce, aggiunge soltanto la zona.
        loc = geo.localise(' '.join([r.get('luoghi', ''), r.get('titolo_candidato', ''),
                                     r.get('oggetto_sintetico', '')]))
        mun = norm_mun(meta['municipio'])
        zona = loc.get('zona') or ''
        tier = loc.get('tier') or ''
        if not tier: tier = 'meta' if mun else 'assente'
        data_fatto = data_del_fatto(meta['tipologia'], r, meta)
        notizie.append({
            'id': '', 'documento_id': did, 'fonte': 'A2',
            'titolo_anonimizzato': r.get('titolo_candidato', ''), 'sintesi': r.get('contenuto', ''),
            'tipo': tipo, 'luoghi': r.get('luoghi', ''), 'municipio': ';'.join(mun),
            'zona': zona, 'tier_localizzazione': tier,
            'toponimo_da_verificare': 'sì' if (r.get('luoghi', '').strip() and not zona and not mun) else 'no',
            'evidenza_url': meta['url'], 'evidenza_locale': r.get('evidenza_pagina', ''),
            'data_fatto': data_fatto, 'data_pubblicazione': iso_it(meta['data']),
            'disponibilita': '', 'qualita': (r.get('qualita') or 'media').strip(),
            'dedup_stato': 'unica', 'gemello_id': '', 'ragione_dedup': '', 'prima_fonte': 'sì',
            'vicenda_id': '', 'integra_gemello_id': '', 'campi_integrati': '',
            'settimana': meta.get('settimana', ''), 'report_origine': '2',
            'verifica_seconda_ai': 'non eseguita', 'municipio_testo': '',
            'note': r.get('coerenza_organo_territorio_o_nota', ''),
        })
    # Gli identificativi del Report 1 non si rinumerano: il rapporto gia' consegnato li cita.
    for k, n in enumerate(notizie[n_r1:], n_r1 + 1): n['id'] = f'N{k:04d}'
    print(f'atti letti: {len(letti2)} di {len(man2)} nel manifest; '
          f'candidate dagli atti: {len(notizie) - n_r1}')
    if sconosciuti:
        print('  tipologie senza un esempio letto, portate a "altro":', dict(sconosciuti))
    lunghe = sum(1 for n in notizie[n_r1:] if len(n['sintesi'].split()) > 60)
    titoloni = sum(1 for n in notizie[n_r1:] if len(n['titolo_anonimizzato'].split()) > 12)
    print(f'  fuori schema, lasciate intatte: {lunghe} sintesi oltre 60 parole, '
          f'{titoloni} titoli oltre 12 parole')

# ---- Report 2: le registrazioni (fonti A3 e A4) -----------------------------
# Anche il parlato entra nelle stesse tabelle e nello stesso confronto: la domanda del Report 2
# — che cosa si sente in aula e non sta scritto da nessuna parte — si risponde solo mettendo
# le registrazioni accanto agli atti e alle fonti testuali, non in un database a parte.
ROMANI_DA_TERRITORIO = re.compile(r'Municipio\s+([IVX]+)', re.I)

def item_video(j, meta, lotto):
    """Una riga di documenti e le sue candidate, dallo schema del lotto A."""
    fonte = meta.get('fonte') or 'A4'
    did = '%s_%s' % (fonte, j['item_id'].split('_')[1])
    dur = j.get('durata_hm', '')
    # Dal sesto emendamento un lettore scrive `non attendibile` invece di zero dove la ripetizione
    # del modello supera il 10%: uno zero sarebbe indistinguibile da un conteggio vero. Qui quel
    # valore diventa una cella vuota, che nelle statistiche di volume non si somma.
    grezzo = str(j.get('parole') or '').strip()
    parole = int(grezzo) if grezzo.isdigit() else ''
    doc = {
        'id': did, 'fonte': fonte, 'tipo': 'registrazione', 'url': meta.get('url', ''),
        'data_pubblicazione': meta.get('data_pubblicazione', ''), 'timestamp_pubblicazione': '',
        'data_evento_inizio': '', 'data_evento_fine': '',
        'titolo_anonimizzato': '%s, %s del %s' % (j.get('territorio', ''), j.get('organo', ''),
                                                  j.get('data_seduta', '')),
        'municipi_meta': ';'.join(ROMANI_DA_TERRITORIO.findall(j.get('territorio', '') or '')),
        'tematica': '', 'caratteri': parole, 'formato_item': 'video',
        'metodo_estrazione': 'trascrizione piattaforma', 'ocr_incerto': '',
        # La piattaforma dichiara confidenza zero su ogni parola (STATO §43): non e' un giudizio
        # di bassa qualita', e' un campo non compilato, quindi la trascrizione resta incerta.
        'trascrizione_incerta': ('sì; confidenza mediana %s, marcatore ogni %s s'
                                 % (meta.get('confidenza_mediana') or 'non dichiarata',
                                    meta.get('grana_marcatore_s') or '10')),
        'esito_lettura': 'completo',
        'settimana': settimana(meta.get('data_pubblicazione', '') or j.get('data_seduta', '')),
        'report_origine': '2', 'letto_da': lotto,
    }
    righe = []
    for c in j.get('notizie_candidate') or []:
        ev = c.get('evidenza') or []
        loc = geo.localise(' '.join(list(c.get('luoghi') or []) + [c.get('titolo', '')]))
        mun = norm_mun(doc['municipi_meta'])
        zona = loc.get('zona') or ''
        tier = loc.get('tier') or ('meta' if mun else 'assente')
        righe.append({
            'id': '', 'documento_id': did, 'fonte': fonte,
            'titolo_anonimizzato': c.get('titolo', ''), 'sintesi': c.get('sintesi', ''),
            'tipo': c.get('tipo', 'altro'), 'luoghi': '; '.join(c.get('luoghi') or []),
            'municipio': ';'.join(mun), 'zona': zona, 'tier_localizzazione': tier,
            'toponimo_da_verificare': c.get('toponimo_da_verificare', 'no'),
            'evidenza_url': meta.get('url', ''), 'evidenza_locale': ev[0] if ev else '',
            'data_fatto': j.get('data_seduta', ''), 'data_pubblicazione': meta.get('data_pubblicazione', ''),
            'disponibilita': '', 'qualita': (c.get('qualita') or 'media').strip(),
            'dedup_stato': 'unica', 'gemello_id': '', 'ragione_dedup': '', 'prima_fonte': 'sì',
            'vicenda_id': '', 'integra_gemello_id': '', 'campi_integrati': '',
            'settimana': doc['settimana'], 'report_origine': '2',
            'verifica_seconda_ai': 'non eseguita', 'municipio_testo': '',
            # Il campo per cui il Report 2 esiste: che cosa il parlato aggiunge agli atti.
            'note': 'novita: ' + (c.get('novita_rispetto_agli_atti') or 'non verificabile'),
        })
    return doc, righe

if os.path.isdir(R2 + '/out_video'):
    meta_video = {}
    for mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
        if os.path.exists(R2 + '/' + mf):
            for r in csv.DictReader(open(R2 + '/' + mf, encoding='utf-8')):
                meta_video[r['item_id']] = r
    n_prima = len(notizie)
    letti_v = 0
    for f in sorted(glob.glob(R2 + '/out_video/*.json')):
        try:
            j = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('REGISTRAZIONE ILLEGGIBILE', os.path.basename(f), str(e)[:80]); continue
        meta = meta_video.get(j.get('item_id'), {})
        if not meta:
            print('REGISTRAZIONE SENZA MANIFEST', j.get('item_id')); continue
        doc, righe = item_video(j, meta, os.path.basename(f)[:6])
        documenti[doc['id']] = doc
        notizie.extend(righe)
        letti_v += 1
    for k, n in enumerate(notizie[n_prima:], n_prima + 1): n['id'] = f'N{k:04d}'
    nov = collections.Counter(n['note'] for n in notizie[n_prima:])
    print('registrazioni lette: %d; candidate dal parlato: %d' % (letti_v, len(notizie) - n_prima))
    print('  ', {k.replace('novita: ', ''): v for k, v in nov.most_common()})

# Gli identificativi si assegnano **qui**, prima di qualunque confronto: la deduplicazione,
# il confronto esaustivo e le integrazioni scrivono riferimenti da riga a riga, e se il
# registro arrivasse dopo quei riferimenti resterebbero posizionali mentre le righe hanno
# gia' cambiato numero. E' successo: 549 righe su 2.936 avevano un numero diverso dalla
# propria posizione, e `coppie_parlato_scritto.csv` — il file su cui si audita — era scritto
# con i numeri vecchi.
# ---- identificativi stabili -----------------------------------------------
# Fino a oggi l'identificativo di una notizia era la sua **posizione** nella lista: `N{k:04d}` da
# `enumerate`. Le righe del Report 1 restavano ferme perche' stanno in testa, ma bastava aggiungere
# un lotto di atti — che si inserisce in mezzo — per far scorrere di dodici posizioni tutte le righe
# delle registrazioni. Un revisore se n'e' accorto nel modo peggiore: il database e' stato riscritto
# mentre lavorava, e l'identificativo che stava giudicando indicava un'altra riga. Non un vuoto:
# **un'altra riga esistente**, cioe' una collisione silenziosa.
# Da qui in avanti l'identificativo sta in un registro, legato all'identita' della riga (documento e
# titolo) e non alla sua posizione. Le righe gia' viste tengono il proprio; le nuove prendono il
# primo numero libero. Il registro si versiona insieme ai dati.
REGISTRO = R + '/db/registro_id.csv'
chiave_id = lambda n: (n['documento_id'], (n['titolo_anonimizzato'] or '').strip())
registro = {}
if os.path.exists(REGISTRO):
    for r in csv.DictReader(open(REGISTRO, encoding='utf-8')):
        registro[(r['documento_id'], r['titolo'])] = r['id']
liberi = max([int(v[1:]) for v in registro.values()] or [0])
nuovi_id = 0
for n in notizie:
    k = chiave_id(n)
    if k in registro:
        n['id'] = registro[k]
    else:
        liberi += 1; n['id'] = f'N{liberi:04d}'; registro[k] = n['id']; nuovi_id += 1
doppi = len(notizie) - len({n['id'] for n in notizie})
if doppi:
    print('ATTENZIONE: %d righe condividono un identificativo (documento e titolo uguali)' % doppi)
os.makedirs(R + '/db', exist_ok=True)
with open(REGISTRO, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['id', 'documento_id', 'titolo'])
    for (d, ti), i in sorted(registro.items(), key=lambda x: x[1]): w.writerow([i, d, ti])
print('identificativi: %d dal registro, %d nuovi' % (len(notizie) - nuovi_id, nuovi_id))

# ---- deduplicazione (metodo §4.1, schema §2 regola 2) ----------------------
# Three conditions, in order: (a) date within +/-1 day, (b) place, (c) object. (a)+(b) without (c)
# is a doubt, never a merge: the yield is then reported as a range.
PARLATO_FONTI = {'A3', 'A4'}
TIPO_AFFINE = {'evento': 'evento', 'convegno': 'evento', 'avviso': 'avviso',
               'delibera': 'atto', 'mozione': 'atto', 'risoluzione': 'atto',
               'ordine del giorno': 'atto', 'interrogazione': 'atto'}

def giorno(n):
    d = n['data_fatto'] or n['data_pubblicazione']
    try: return datetime.date.fromisoformat(d[:10])
    except (ValueError, TypeError): return None

# Two strings that look like toponyms are not places the news is *about*, and letting them
# through defeats the Municipio safeguard below by pretending to be a finer match:
#   - the name of the Municipio itself ("Municipio Roma XII"), which is the organ, not a place;
#   - the room the organ sits in ("Sala …", "Aula …", "Sede …"), which is where the meeting
#     happens, not what it is about.
# Both arrived with the acts, where every convocation carries them, and they were pairing
# unrelated sittings of the same body on the same day.
SEDE = re.compile(r'^(sala|aula|sede|ufficio|sportello)\b')
def toponimi(n):
    out = set()
    for t in re.split(r'[;,]', n['luoghi']):
        t = geo.norm(t)
        if len(t) <= 3 or 'municipio' in t or SEDE.match(t): continue
        out.add(t)
    return out

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
    # Il tipo vale come filtro solo fra righe della stessa natura. Fra parlato e scritto i due
    # vocabolari descrivono cose diverse: dal lato parlato `tipo` dice **come** il fatto e' emerso
    # (un'audizione, un sopralluogo), dal lato scritto dice **che cosa e' il documento** (una
    # delibera, un avviso). Confrontarli come se fossero la stessa tassonomia rendeva la classe
    # "duplicato" irraggiungibile per il 42% delle candidate del parlato, qualunque cosa dicesse il
    # testo: `audizione` e `sopralluogo` dal lato scritto contano tre righe in tutto.
    # Trovato dal revisore della classe dubbio, misurando: 86 accostamenti su 102 venivano scartati
    # qui, prima che la soglia sulle parole fosse valutata, e quattro dei sei gemelli veri con loro.
    misto = (a['fonte'] in PARLATO_FONTI) != (b['fonte'] in PARLATO_FONTI)
    if not misto and TIPO_AFFINE.get(a['tipo'], a['tipo']) != TIPO_AFFINE.get(b['tipo'], b['tipo']):
        return False
    pa, pb = parole(a['titolo_anonimizzato'] + ' ' + a['luoghi']), parole(b['titolo_anonimizzato'] + ' ' + b['luoghi'])
    if not pa or not pb: return False
    return len(pa & pb) / min(len(pa), len(pb)) >= 0.6

# Blocks under 300 items in the level-1 sources are deduplicated over the whole month and the
# yield is measured; above it, a sample of at least 60 per pair and the yield is estimated.
per_blocco = collections.Counter(BLOCCO[n['fonte']] for n in notizie)
coppie, dubbi = 0, 0
campioni = {}
for blocco in sorted(per_blocco):
    gruppo = [n for n in notizie if BLOCCO[n['fonte']] == blocco]
    fonti_blocco = sorted({n['fonte'] for n in gruppo})
    item_blocco = len({n['documento_id'] for n in gruppo})
    # Method §4.1 samples above 300 items because it assumes the comparison is made by hand. Ours
    # is deterministic and costs nothing, so the whole month is compared and the yield is measured.
    # The prescribed sample is computed as well, on the same rows, so the report can show both and
    # the deviation stays visible instead of being a silent upgrade of someone else's method.
    if item_blocco > 300 and len(fonti_blocco) > 1:
        seed = '2026-06-' + 'x'.join(fonti_blocco)
        quota = max(60, 60 * (len(fonti_blocco) * (len(fonti_blocco) - 1) // 2))
        campione = list(gruppo); random.Random(seed).shuffle(campione)
        campioni[blocco] = {'seed': seed, 'quota': quota, 'ids': {n['id'] for n in campione[:quota]}}
        print(f'  campione prescritto dal metodo: seed={seed}, {quota} notizie; confronto eseguito su tutte e {len(gruppo)}')
    for i, a in enumerate(gruppo):
        if a['dedup_stato'] != 'unica': continue
        ga = giorno(a)
        for b in gruppo[i + 1:]:
            if b['dedup_stato'] != 'unica' or b['documento_id'] == a['documento_id']: continue
            gb = giorno(b)
            if not ga or not gb or abs((ga - gb).days) > 1: continue
            if not stesso_luogo(a, b): continue
            if stesso_oggetto(a, b) and not (blocco == 'Eventi' and ga != gb):
                b['dedup_stato'] = 'duplicato'; coppie += 1
                b['ragione_dedup'] = 'stessa data, stesso luogo, stesso oggetto'
            else:
                b['dedup_stato'] = 'dubbio'; dubbi += 1
                b['ragione_dedup'] = ('stesso luogo e stesso oggetto a un giorno di distanza: per gli Eventi'
                                      ' il metodo chiede la stessa data' if stesso_oggetto(a, b)
                                      else 'data ±1 giorno e stesso luogo; oggetto incerto')
                b['prima_fonte'] = 'non applicabile'
            b['gemello_id'] = a['id']
            if b['dedup_stato'] == 'duplicato': b['prima_fonte'] = 'no'
    print(f'{blocco}: {len(gruppo)} notizie confrontate sull\'intero mese')

# ---- il confronto esaustivo parlato-contro-scritto -------------------------
# La deduplicazione qui sopra segue il metodo §4.1 e **consuma** le righe: appena una riga prende
# un gemello esce dal confronto, come a mano. Va bene per contare la resa netta, non per dire se
# una cosa detta in aula sta scritta da qualche parte, che e' la domanda del Report 2. Con la
# catena, 111 candidate del parlato avevano come unico gemello un'altra registrazione e non sono
# mai state confrontate con lo scritto; e 537 righe scritte su 1.855, gia' legate, erano fuori da
# ogni confronto successivo. Entrambe le cose alzano la novita'.
# Questo passaggio non tocca la deduplicazione: aggiunge, per ogni riga del parlato, quanti
# gemelli scritti esistono **davvero**, provando tutte le coppie. Il conteggio e' fatto due volte,
# dentro il blocco come prescrive il metodo e su tutto il corpus, cosi' il costo della partizione
# in blocchi si vede invece di restare implicito.
coppie_ps = []
scritte_tutte = [n for n in notizie if n['fonte'] not in PARLATO_FONTI]
for n in notizie:
    n['gemelli_scritti'] = ''
    n['gemelli_scritti_blocco'] = ''
for a in notizie:
    if a['fonte'] in PARLATO_FONTI:
        ga = giorno(a)
        dup = dub = dup_b = dub_b = 0
        righe_coppia = []
        for b in scritte_tutte:
            # Il metodo §4.1 chiede **due criteri su tre** per il dubbio e tre per il duplicato.
            # La catena qui sopra invece pretende sempre data *e* luogo, e usa l'oggetto solo per
            # distinguere dubbio da duplicato: cosi' una coppia data+oggetto con luoghi scritti in
            # modo diverso, o luogo+oggetto a quattro giorni di distanza, non viene mai accostata.
            # Il rilievo e' del controllo C5. Qui i tre criteri si contano davvero.
            gb = giorno(b)
            d_ok = bool(ga) and bool(gb) and abs((ga - gb).days) <= 1
            l_ok = stesso_luogo(a, b)
            o_ok = stesso_oggetto(a, b)
            n = d_ok + l_ok + o_ok
            if n < 2: continue
            forte = n == 3
            dup += forte; dub += not forte
            # Le coppie si scrivono su file: chi deve auditarle non le ricalcola con una seconda
            # copia della regola, che divergerebbe.
            righe_coppia.append({'parlata': a['id'], 'scritta': b['id'],
                                 'forza': 'forte' if forte else 'debole',
                                 'criteri': ''.join(c for c, ok in (('d', d_ok), ('l', l_ok), ('o', o_ok)) if ok),
                                 'stesso_blocco': 'sì' if BLOCCO[a['fonte']] == BLOCCO[b['fonte']] else 'no'})
            if BLOCCO[a['fonte']] == BLOCCO[b['fonte']]:
                dup_b += forte; dub_b += not forte
        a['gemelli_scritti'] = f'{dup}/{dub}'
        a['gemelli_scritti_blocco'] = f'{dup_b}/{dub_b}'
        coppie_ps.extend(righe_coppia)
parl = [n for n in notizie if n['fonte'] in PARLATO_FONTI]
def classe(v):
    d, u = (int(x) for x in v.split('/'))
    return 'D' if d else ('U' if u else 'S')
cc = collections.Counter(classe(n['gemelli_scritti']) for n in parl)
cb = collections.Counter(classe(n['gemelli_scritti_blocco']) for n in parl)
with open(R2 + '/coppie_parlato_scritto.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['parlata', 'scritta', 'forza', 'criteri', 'stesso_blocco'])
    w.writeheader(); w.writerows(coppie_ps)
print('coppie parlato-scritto scritte in report2/coppie_parlato_scritto.csv: %d' % len(coppie_ps))
print('confronto esaustivo parlato-scritto, su tutto il corpus: %s' % dict(cc))
print('  dentro il blocco, come prescrive il metodo:            %s' % dict(cb))

# ---- che cosa una riga del Report 2 aggiunge alla sua gemella del Report 1 --
# Schema §1.3: quando una riga nuova **aggiunge o corregge** qualcosa alla gemella,
# `integra_gemello_id` ripete il gemello e `campi_integrati` elenca le colonne. Nessuno li riempiva
# (rilievo C5): senza, una vista che scarta i duplicati perde esattamente il contributo che il
# Report 2 esiste per misurare.
# Si confrontano solo i campi dove «pieno contro vuoto» o «diverso» significa qualcosa; il testo
# libero no, perche' due sintesi diverse dello stesso fatto non sono una correzione.
# `luoghi` e' testo libero: due grafie diverse dello stesso posto non sono una correzione, e
# contarle come tali dava 270 integrazioni su 270, cioe' un numero che misurava la varieta' della
# scrittura. Per quel campo conta solo il caso «prima vuoto, ora pieno».
SOLO_SE_VUOTO = {'luoghi'}
CAMPI_INTEGRABILI = ['data_fatto', 'municipio', 'zona', 'luoghi', 'tipo']
per_id_int = {n['id']: n for n in notizie}
integrate = 0
for n in notizie:
    g = per_id_int.get(n['gemello_id'])
    if not g or n['report_origine'] != '2' or g['report_origine'] != '1': continue
    campi = []
    for c in CAMPI_INTEGRABILI:
        a, b = (g.get(c) or '').strip(), (n.get(c) or '').strip()
        if b and not a: campi.append(c)                          # riempie un vuoto
        elif a and b and a != b and c not in SOLO_SE_VUOTO: campi.append(c)   # corregge
    if campi:
        n['integra_gemello_id'] = g['id']
        n['campi_integrati'] = ';'.join(campi)
        integrate += 1
print('righe del Report 2 che integrano una gemella del Report 1: %d' % integrate)

# ---- esito della seconda AI (prova T4) ------------------------------------
# Lo schema prevede il campo `verifica_seconda_ai` e finora nessuno lo riempiva (rilievo C5). Qui si
# legge l'esito della prova, se c'e'. Le righe non verificate restano `non eseguita`: un campo vuoto
# sarebbe indistinguibile da una verifica riuscita e senza rilievi.
t4 = {}
p_t4 = R2 + '/t4_esito.csv'
if os.path.exists(p_t4):
    for r in csv.DictReader(open(p_t4, encoding='utf-8')):
        t4[r['id']] = r
for n in notizie:
    e = t4.get(n['id'])
    if e:
        n['verifica_seconda_ai'] = e['verifica_seconda_ai']
        n['note'] = ((n['note'] + ' | ') if n['note'] else '') + 'T4 %s: %s' % (e['verifica_seconda_ai'], e['motivo'])
if t4:
    print('prova T4: %d righe verificate da una seconda AI, %d discordi'
          % (len(t4), sum(1 for e in t4.values() if e['verifica_seconda_ai'] == 'discorde')))

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
    # La confidenza di una vicenda non puo' dipendere dall'ultima riga processata (rilievo C5):
    # una vicenda tenuta insieme da un duplicato certo resta alta anche se dopo arriva un dubbio.
    if n['dedup_stato'] == 'duplicato': v['confidenza'] = 'alta'
    elif v['confidenza'] != 'alta': v['confidenza'] = 'bassa'

# Una vicenda e' "solo Report 2" quando nessuna delle notizie che la compongono viene dal
# Report 1: e' la colonna che dice quali storie gli atti hanno portato e le fonti testuali no.
for v in vicende:
    origini = {n['report_origine'] for n in notizie if n['vicenda_id'] == v['id']}
    v['solo_report2'] = 'sì' if origini == {'2'} else 'no'
print('vicende solo dagli atti:', sum(1 for v in vicende if v['solo_report2'] == 'sì'), 'su', len(vicende))

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

ANAGRAFE = {
    'A1': ('Avvisi e notizie dei Municipi', 'Roma Capitale — Municipi I–XV', 'https://www.comune.roma.it/web/it/municipio-<n>.page'),
    'A2': ('Atti degli organi capitolini e municipali', 'Roma Capitale — Albo Pretorio / Atti Web', 'https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/'),
    'A3': ('Registrazioni delle sedute su RomaTV', 'Roma Capitale — streaming istituzionale', 'https://streaming.comune.roma.it/'),
    'A4': ('Registrazioni delle sedute sui canali YouTube dei Municipi', 'Roma Capitale — Municipi', 'https://www.youtube.com/'),
    'C1': ('Comunicati della Questura di Roma', 'Polizia di Stato — Questura di Roma', 'https://questure.poliziadistato.it/it/Roma'),
    'C2': ('Comunicati stampa dei Carabinieri', 'Arma dei Carabinieri', 'https://www.carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa'),
    'C4': ('Notizie del Comando dei Vigili del fuoco di Roma', 'Corpo nazionale dei Vigili del fuoco', 'https://www.vigilfuoco.it/comando-vvf-roma/notizie'),
    'C5': ('Notizie di Roma Capitale', 'Roma Capitale', 'https://www.comune.roma.it/web/it/notizie.page'),
    'E2': ('Agenda eventi culturali', 'Roma Capitale — Sovrintendenza Capitolina / Zètema', 'https://culture.roma.it/appuntamenti/'),
    'E3': ('Agenda eventi del portale istituzionale', 'Roma Capitale', 'https://www.comune.roma.it/web/it/eventi.page'),
}
fonti = []
for cod in ORDINE_FONTI:
    docs = [d for d in documenti.values() if d['fonte'] == cod]
    if not docs: continue
    nome, ente, elenco = ANAGRAFE[cod]
    fonti.append({'codice': cod, 'nome': nome, 'blocco': BLOCCO[cod], 'ente': ente, 'url_elenco': elenco,
                  'base_url': ('https://www.comune.roma.it/web/it/' if cod == 'E3'
                               else A2_BASE if cod == 'A2' else ''),
                  'formato': 'PDF' if cod == 'A2' else 'video' if cod in ('A3', 'A4') else 'HTML',
                  'item_giugno': len(docs),
                  'paginazione_completa': 'sì',
                  'data_lettura': '2026-09-16' if cod == 'A2' else '2026-09-15',
                  'report': '2' if cod == 'A2' else '1',
                  'note': ('67 item su 79 rispondono con la pagina di blocco "Accesso negato" (HTTP 200): testo non disponibile' if cod == 'C1'
                           else 'l\'URL del singolo comunicato rimanda alla pagina-vetrina: nessun testo disponibile' if cod == 'C2'
                           else f'{ocr_a2} atti su {len(docs)} hanno il testo incerto; '
                                f'{corrotti_a2} portano lo strato di testo rovinato all\'origine, senza marcatore OCR' if cod == 'A2'
                           else '')})

# Every (Municipio, week) cell is emitted, including the empty ones: a gap is a cell with no
# news, and a table that only lists what exists cannot show one. This is what the report's
# "lacune" question asks for.
terr_righe = []
for mun in ROMANI + ['non localizzato']:
    for sett in ['1', '2', '3', '4', '5']:
        t = territori.get((mun, sett))
        if t is None:
            terr_righe.append({'municipio': mun, 'settimana': sett, 'n_documenti': 0, 'n_notizie': 0,
                               'n_notizie_alta': 0, 'n_notizie_media': 0, 'n_notizie_bassa': 0,
                               'fonti_presenti': '', 'mediana_giorni_pubblicazione': '', 'lacuna': 'sì'})
            continue
        r = dict(t)
        r['n_documenti'] = len(t['n_documenti']); r['fonti_presenti'] = ';'.join(sorted(t['fonti_presenti']))
        rit = sorted(t['ritardi'])
        r['mediana_giorni_pubblicazione'] = rit[len(rit) // 2] if len(rit) >= 3 else ''
        r['lacuna'] = 'no'
        terr_righe.append(r)
# Facts dated outside June keep their own row per Municipio, with the week left empty.
for (mun, sett), t in sorted(territori.items()):
    if sett: continue
    r = dict(t); r['n_documenti'] = len(t['n_documenti'])
    r['fonti_presenti'] = ';'.join(sorted(t['fonti_presenti']))
    rit = sorted(t['ritardi'])
    r['mediana_giorni_pubblicazione'] = rit[len(rit) // 2] if len(rit) >= 3 else ''
    r['lacuna'] = 'no'; terr_righe.append(r)
print('celle Municipio×settimana senza notizie:', sum(1 for r in terr_righe if r['lacuna'] == 'sì'))

print('tabelle scritte in report1/db/:')
scrivi('fonti', fonti, ['codice','nome','blocco','ente','url_elenco','base_url','formato','item_giugno','paginazione_completa','data_lettura','report','note'])
scrivi('documenti', list(documenti.values()), ['id','fonte','tipo','url','data_pubblicazione','timestamp_pubblicazione','data_evento_inizio','data_evento_fine','titolo_anonimizzato','municipi_meta','tematica','caratteri','formato_item','metodo_estrazione','ocr_incerto','trascrizione_incerta','esito_lettura','settimana','report_origine','letto_da'])
scrivi('notizie_candidate', notizie, ['id','documento_id','fonte','titolo_anonimizzato','sintesi','tipo','luoghi','municipio','municipio_testo','zona','tier_localizzazione','toponimo_da_verificare','evidenza_url','evidenza_locale','data_fatto','data_pubblicazione','disponibilita','qualita','dedup_stato','gemello_id','ragione_dedup','gemelli_scritti','gemelli_scritti_blocco','prima_fonte','vicenda_id','integra_gemello_id','campi_integrati','settimana','report_origine','verifica_seconda_ai','note'])
scrivi('vicende', vicende, ['id','titolo_anonimizzato','tipo','municipio','zona','prima_pubblicazione','ultima_pubblicazione','n_notizie','fonti','confidenza','solo_report2','stato'])
scrivi('territori', terr_righe, ['municipio','settimana','n_documenti','n_notizie','n_notizie_alta','n_notizie_media','n_notizie_bassa','fonti_presenti','mediana_giorni_pubblicazione','lacuna'])
for blocco, c in campioni.items():
    righe = [n for n in notizie if n['id'] in c['ids']]
    dd = collections.Counter(n['dedup_stato'] for n in righe)
    print(f"{blocco}: sul campione prescritto ({c['quota']} notizie, seed {c['seed']}) la resa sarebbe {dict(dd)}")
d = collections.Counter(n['dedup_stato'] for n in notizie)
print('dedup:', dict(d), '| netta minima:', sum(1 for n in notizie if n['dedup_stato']=='unica'), '| netta massima:', sum(1 for n in notizie if n['dedup_stato'] in ('unica','dubbio')))

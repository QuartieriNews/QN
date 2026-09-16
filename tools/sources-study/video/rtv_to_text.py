# Le registrazioni RomaTV in testo leggibile. Due origini, due grane di marcatore, e la
# differenza va dichiarata invece che nascosta:
#  - trascrizioni della piattaforma (rtv/speech): parola per parola con tempo e confidenza veri,
#    quindi marcatore ogni 10 secondi come chiede il metodo per il lotto A;
#  - trascrizioni a pagamento (rtv/trascrizioni): il modello non restituisce tempi interni, solo
#    il pezzo, quindi il marcatore cade all'inizio di ogni pezzo, circa ogni 5 minuti.
import csv, glob, json, os, statistics as st
BASE = os.path.dirname(os.path.abspath(__file__))
DEST = BASE + '/rtv/txt'; os.makedirs(DEST, exist_ok=True)

def hhmmss(s):
    return '%02d:%02d' % (int(s // 60), int(s % 60))

def secondi(t):
    h, m, s = t.split(':'); return int(h) * 3600 + int(m) * 60 + float(s)

righe = []
for p in sorted(glob.glob(BASE + '/rtv/speech/*.json')):
    guid = os.path.basename(p)[:-5]
    try:
        d = json.load(open(p))
    except Exception as e:
        righe.append({'item': guid, 'origine': 'piattaforma', 'errore': str(e)[:60]}); continue
    parole = [w for alt in (d.get('Alternatives') or []) for w in (alt.get('Words') or [])]
    if not parole:
        righe.append({'item': guid, 'origine': 'piattaforma', 'errore': 'nessuna parola'}); continue
    out = []; ultimo = -10.0
    for w in parole:
        t = secondi(w['StartTime'])
        if t - ultimo >= 10:
            out.append('\n[%s] ' % hhmmss(t)); ultimo = t
        out.append(w['Word'] + ' ')
    testo = ''.join(out).strip() + '\n'
    open('%s/%s.txt' % (DEST, guid), 'w', encoding='utf-8').write(testo)
    conf = [w['Confidence'] for w in parole if isinstance(w.get('Confidence'), (int, float))]
    righe.append({'item': guid, 'origine': 'piattaforma', 'parole': len(parole),
                  'durata_s': round(secondi(parole[-1]['EndTime']), 1),
                  'confidenza_mediana': round(st.median(conf), 3) if conf else '',
                  'quota_sotto_0_7': round(sum(1 for c in conf if c < 0.7) / len(conf), 3) if conf else '',
                  'grana_marcatore_s': 10, 'caratteri': len(testo), 'errore': ''})

for p in sorted(glob.glob(BASE + '/rtv/trascrizioni/*.json')):
    nome = os.path.basename(p)[:-5]
    try:
        j = json.load(open(p))
    except Exception as e:
        righe.append({'item': nome, 'origine': 'a pagamento', 'errore': str(e)[:60]}); continue
    pezzi = j.get('pezzi') or []
    testo = ''.join('\n[%s] %s' % (hhmmss(x['inizio_s']), (x.get('testo') or '').strip())
                    for x in pezzi).strip() + '\n'
    open('%s/%s.txt' % (DEST, nome), 'w', encoding='utf-8').write(testo)
    grana = round(st.median([x['fine_s'] - x['inizio_s'] for x in pezzi])) if pezzi else ''
    righe.append({'item': nome, 'origine': 'a pagamento', 'parole': len(testo.split()),
                  'durata_s': j.get('durata_s', ''), 'confidenza_mediana': '',
                  'quota_sotto_0_7': '', 'grana_marcatore_s': grana,
                  'caratteri': len(testo), 'errore': ''})

campi = ['item', 'origine', 'parole', 'durata_s', 'confidenza_mediana', 'quota_sotto_0_7',
         'grana_marcatore_s', 'caratteri', 'errore']
with open(BASE + '/rtv/indice_rtv.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=campi, extrasaction='ignore'); w.writeheader(); w.writerows(righe)
ok = [r for r in righe if not r.get('errore')]
for orig in ('piattaforma', 'a pagamento'):
    g = [r for r in ok if r['origine'] == orig]
    if g:
        print('%-12s %3d registrazioni, %6.1f ore, %8d parole' %
              (orig, len(g), sum(float(r['durata_s'] or 0) for r in g) / 3600, sum(r['parole'] for r in g)))
err = [r for r in righe if r.get('errore')]
if err: print('con errore:', len(err), err[:3])

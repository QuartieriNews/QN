# Le didascalie YouTube in testo leggibile, con i marcatori a 10 secondi che il metodo chiede
# per il lotto A (HANDOFF §4). La confidenza media dell'ASR, quando la piattaforma la dà, finisce
# in un indice: serve a dire quali trascrizioni sono incerte prima di leggerle, non dopo.
import csv, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from json3_to_text import convert
base = os.path.dirname(os.path.abspath(__file__))
dest = base + '/caps_txt'; os.makedirs(dest, exist_ok=True)
righe = []
for p in sorted(glob.glob(base + '/caps/*.json3')):
    vid = os.path.basename(p).split('.')[0]
    try:
        testo, st = convert(p, step=10)
    except Exception as e:
        righe.append({'video_id': vid, 'errore': str(e)[:80]}); continue
    open(f'{dest}/{vid}.txt', 'w', encoding='utf-8').write(testo.strip() + '\n')
    righe.append({'video_id': vid, 'parole': st['words'], 'durata_s': round(st['dur_s'], 1),
                  'confidenza_media': round(st['conf_mean'], 3) if st['conf_mean'] is not None else '',
                  'parole_con_confidenza': st['conf_n'], 'caratteri': len(testo), 'errore': ''})
with open(base + '/caps_indice.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['video_id', 'parole', 'durata_s', 'confidenza_media',
                                      'parole_con_confidenza', 'caratteri', 'errore'],
                       extrasaction='ignore')
    w.writeheader(); w.writerows(righe)
ok = [r for r in righe if not r.get('errore')]
print('didascalie convertite: %d di %d' % (len(ok), len(righe)))
print('ore totali: %.1f | parole: %d' % (sum(r['durata_s'] for r in ok)/3600, sum(r['parole'] for r in ok)))
conf = [r['confidenza_media'] for r in ok if r['confidenza_media'] != '']
if conf:
    conf.sort()
    print('confidenza media dichiarata su %d video: mediana %.3f, minimo %.3f' % (len(conf), conf[len(conf)//2], conf[0]))
vuoti = [r['video_id'] for r in ok if r['parole'] < 50]
if vuoti: print('quasi vuoti (meno di 50 parole): %d' % len(vuoti))

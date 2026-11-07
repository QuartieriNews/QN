# Il sesto emendamento fa scrivere `non attendibile` invece di `0` nei campi di volume quando la
# ripetizione del modello supera il 10%. I lotti letti prima dell'emendamento hanno scritto `0`, e
# nello stesso corpus convivono due codifiche per la stessa condizione — con la sbagliata piu'
# frequente. Un lettore se n'e' accorto applicando l'emendamento a meta' del proprio lotto.
# Questo programma normalizza all'indietro, e **solo** dove la condizione e' vera: uno zero su un
# item sotto soglia e' un conteggio, non un dato mancante, e non si tocca.
import csv, json, os, glob

NET = os.environ['QN_NET']
soglia = {}
for mf in ('manifest_video.csv', 'manifest_video_rtv.csv'):
    p = NET + '/report2/' + mf
    if not os.path.exists(p): continue
    for m in csv.DictReader(open(p, encoding='utf-8')):
        try: soglia[m['item_id']] = float(m.get('quota_ripetuta') or 0)
        except ValueError: pass

tocc = []
for f in sorted(glob.glob(NET + '/report2/out_video/*.json')):
    j = json.load(open(f, encoding='utf-8'))
    q = soglia.get(j.get('item_id'), 0)
    if q <= 0.10: continue
    cambiato = False
    if str(j.get('parole')).strip() in ('0', '0.0'):
        j['parole'] = 'non attendibile'; cambiato = True
    qt = j.get('qualita_trascrizione') or {}
    if str(qt.get('parole_al_minuto')).strip() in ('0', '0.0'):
        qt['parole_al_minuto'] = 'non attendibile'; j['qualita_trascrizione'] = qt; cambiato = True
    if cambiato:
        json.dump(j, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        tocc.append((j['item_id'], round(q, 3)))

print('item sopra il 10%% di testo duplicato: %d' % sum(1 for v in soglia.values() if v > 0.10))
print('item normalizzati da 0 a `non attendibile`: %d' % len(tocc))
for i, q in tocc: print('   %s  quota %.3f' % (i, q))

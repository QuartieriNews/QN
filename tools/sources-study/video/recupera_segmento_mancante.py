# Una registrazione pubblicata il cui ultimo segmento il CDN non serve: risponde vuoto, oggi come
# ieri, a ogni tentativo. Cinquantotto segmenti su cinquantanove sono integri.
# Scartare la seduta per una coda di dieci secondi sarebbe peggio che tenerla dichiarando la lacuna,
# quindi qui si ricostruisce la playlist locale con i soli segmenti che esistono. Non si aggira
# niente: si usa quello che il CDN ha servito.
# La chiave AES e le IV non si inventano: ogni segmento ha IV = MD5 del proprio indice, che e' come
# la playlist remota le scrive (verificato sui segmenti di un'altra registrazione, dove
# cfcd2084...= MD5("0") e c4ca4238...= MD5("1")).
import hashlib, os, re, sys

SEGDIR = sys.argv[1]
URI_CHIAVE = sys.argv[2] if len(sys.argv) > 2 else 'https://api-ovp.streamcloud.it/garavot/ac104/streaming/encryption/key'
DURATA = 10.0

# I segmenti da zero byte vanno tenuti **in vista**: sono la lacuna. Scartarli qui li rende
# invisibili, e la riga finale finirebbe per dichiarare «nessuna lacuna» proprio quando ce n'e' una
# in coda — che e' il caso per cui questo programma esiste.
seg, vuoti = {}, set()
for f in os.listdir(SEGDIR):
    m = re.match(r'(.*slen_)(\d+)\.aac$', f)
    if not m: continue
    i = int(m.group(2))
    if os.path.getsize(os.path.join(SEGDIR, f)) > 0: seg[i] = f
    else: vuoti.add(i)
if not seg: sys.exit('nessun segmento non vuoto in ' + SEGDIR)

primo = min(seg)
ultimo = max(list(seg) + list(vuoti))
buchi = [i for i in range(primo, ultimo + 1) if i not in seg]
# Si tiene la sequenza continua che parte dal primo segmento: un buco in mezzo spezzerebbe l'audio
# senza dirlo, e un file che salta un pezzo in silenzio e' peggio di un file piu' corto.
fine = buchi[0] - 1 if buchi else ultimo
righe = ['#EXTM3U', '#EXT-X-VERSION:3', '#EXT-X-TARGETDURATION:%d' % int(DURATA),
         '#EXT-X-MEDIA-SEQUENCE:%d' % primo]
for i in range(primo, fine + 1):
    iv = hashlib.md5(str(i).encode()).hexdigest()
    righe += ['#EXT-X-KEY:METHOD=AES-128,URI="%s",IV=0x%s' % (URI_CHIAVE, iv),
              '#EXTINF:%.1f,' % DURATA, seg[i]]
righe.append('#EXT-X-ENDLIST')
open(os.path.join(SEGDIR, 'local.m3u8'), 'w').write('\n'.join(righe) + '\n')

mancanti = sorted(set(range(primo, ultimo + 1)) - set(seg))
print('segmenti scritti: %d (da %d a %d)' % (fine - primo + 1, primo, fine))
print('segmenti che il CDN non ha servito: %s' % (mancanti or 'nessuno'))
if mancanti:
    print('LACUNA DA DICHIARARE NEL MANIFEST: %d segmenti, circa %.0f secondi, %s'
          % (len(mancanti), len(mancanti) * DURATA,
             'in coda' if min(mancanti) > fine else 'in mezzo alla registrazione'))

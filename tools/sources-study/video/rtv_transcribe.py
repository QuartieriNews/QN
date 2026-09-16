# Trascrive un mp3 mono con l'API OpenAI, tagliandolo in pezzi allineati ai silenzi
# in modo che ogni pezzo porti un marcatore temporale e nessuna parola cada a meta' del taglio.
# Non stampa mai la chiave: in errore riporta solo lo stato HTTP e il messaggio del fornitore.
import os, re, sys, json, time, subprocess
import imageio_ffmpeg, requests
FF = imageio_ffmpeg.get_ffmpeg_exe()
os.environ.setdefault('REQUESTS_CA_BUNDLE', '/root/.ccr/ca-bundle.crt')
URL = 'https://api.openai.com/v1/audio/transcriptions'
MODELLO = os.environ.get('QN_ASR_MODEL', 'gpt-4o-mini-transcribe')
PEZZO_S = float(os.environ.get('QN_ASR_PEZZO_S', '300'))
TOLLERANZA_S = 45.0

if not os.environ.get('OPENAI_API_KEY'):
    print('OPENAI_API_KEY non impostata: rifiuto di chiamare, perche una chiave assente '
          'non deve passare per una trascrizione vuota', file=sys.stderr)
    sys.exit(2)

def durata(path):
    s = subprocess.run([FF, '-hide_banner', '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', s)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0

def silenzi(path):
    s = subprocess.run([FF, '-hide_banner', '-i', path, '-af', 'silencedetect=noise=-35dB:d=0.4',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r'silence_end: ([\d.]+)', s)]

def tagli(d, sil):
    """Punti di taglio vicini ai multipli di PEZZO_S, spostati sul silenzio piu' vicino."""
    punti = [0.0]
    t = PEZZO_S
    while t < d - 30:
        vicini = [x for x in sil if abs(x - t) <= TOLLERANZA_S and x > punti[-1] + 30]
        punti.append(min(vicini, key=lambda x: abs(x - t)) if vicini else t)
        t = punti[-1] + PEZZO_S
    punti.append(d)
    return punti

def trascrivi(path, tmpdir, nome):
    d = durata(path)
    punti = tagli(d, silenzi(path))
    pezzi = []
    ses = requests.Session()
    for i in range(len(punti) - 1):
        ini, fin = punti[i], punti[i + 1]
        out = os.path.join(tmpdir, '%s_%03d.mp3' % (nome, i))
        subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(ini), '-t',
                        str(fin - ini), '-i', path, '-c', 'copy', out], capture_output=True, text=True)
        for tentativo in range(4):
            with open(out, 'rb') as f:
                r = ses.post(URL, headers={'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']},
                             files={'file': (os.path.basename(out), f, 'audio/mpeg')},
                             data={'model': MODELLO, 'language': 'it', 'response_format': 'json'},
                             timeout=600)
            if r.status_code == 200:
                break
            if r.status_code in (429, 500, 502, 503, 504) and tentativo < 3:
                time.sleep(5 * (tentativo + 1)); continue
            raise SystemExit('trascrizione fallita su %s: HTTP %d %s' % (out, r.status_code, r.text[:300]))
        j = r.json()
        pezzi.append({'i': i, 'inizio_s': round(ini, 1), 'fine_s': round(fin, 1),
                      'byte': os.path.getsize(out), 'testo': j.get('text', ''), 'usage': j.get('usage')})
        os.remove(out)
        print('  pezzo %d/%d  %.0f-%.0fs  %d caratteri' % (i + 1, len(punti) - 1, ini, fin,
              len(pezzi[-1]['testo'])), flush=True)
    return {'file': path, 'modello': MODELLO, 'durata_s': round(d, 1), 'pezzi': pezzi}

if __name__ == '__main__':
    destdir, files = sys.argv[1], sys.argv[2:]
    os.makedirs(destdir, exist_ok=True)
    tmpdir = os.path.join(destdir, '_pezzi'); os.makedirs(tmpdir, exist_ok=True)
    for p in files:
        nome = os.path.splitext(os.path.basename(p))[0]
        dest = os.path.join(destdir, nome + '.json')
        if os.path.exists(dest):
            print('gia fatto:', nome, flush=True); continue
        t0 = time.time()
        print('===', nome, flush=True)
        res = trascrivi(p, tmpdir, nome)
        res['secondi_di_lavoro'] = round(time.time() - t0, 1)
        json.dump(res, open(dest, 'w'), ensure_ascii=False, indent=1)
        print('%s: %.0f s di audio in %.0f s' % (nome, res['durata_s'], res['secondi_di_lavoro']), flush=True)

# Prepara l'audio RomaTV per la trascrizione: remux dei segmenti AES + riduzione a mono 32 kbps.
# Un file sopra i 25 MB viene spezzato in parti da 45 minuti (limite dell'API sulla dimensione).
import os, re, sys, json, shutil, subprocess
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
LIMITE_BYTE = 24 * 1024 * 1024
PARTE_S = 45 * 60

def remux(segdir, key):
    out = segdir[:-5] + '.m4a'
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return out
    shutil.copy(key, os.path.join(segdir, 'key.bin'))
    pl = os.path.join(segdir, 'local_key.m3u8')
    open(pl, 'w').write(re.sub(r'URI="[^"]+"', 'URI="key.bin"', open(os.path.join(segdir, 'local.m3u8')).read()))
    r = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-protocol_whitelist', 'file,crypto',
                        '-allowed_extensions', 'ALL', '-i', pl, '-c', 'copy', out], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('remux fallito su %s: %s' % (segdir, r.stderr[:300]))
    return out

def durata(path):
    s = subprocess.run([FF, '-hide_banner', '-i', path], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', s)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0

def comprimi(src, destdir):
    """mono 32 kbps; ritorna la lista delle parti pronte per l'API."""
    os.makedirs(destdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(src))[0]
    d = durata(src)
    parti = []
    n = max(1, int(d // PARTE_S) + (1 if d % PARTE_S else 0))
    for i in range(n):
        out = os.path.join(destdir, '%s_p%d.mp3' % (base, i))
        if not (os.path.exists(out) and os.path.getsize(out) > 0):
            args = [FF, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(i * PARTE_S)]
            if i < n - 1:
                args += ['-t', str(PARTE_S)]
            args += ['-i', src, '-ac', '1', '-ar', '16000', '-b:a', '32k', out]
            r = subprocess.run(args, capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError('compressione fallita su %s: %s' % (src, r.stderr[:300]))
        if os.path.getsize(out) > LIMITE_BYTE:
            raise RuntimeError('%s supera il limite dell API: %d byte' % (out, os.path.getsize(out)))
        parti.append({'file': out, 'byte': os.path.getsize(out),
                      'durata_s': round(min(PARTE_S, d - i * PARTE_S), 1)})
    return {'sorgente': src, 'durata_s': round(d, 1), 'parti': parti}

if __name__ == '__main__':
    key, destdir, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    base = os.path.dirname(os.path.abspath(__file__)) + '/rtv/audio'
    res = []
    for i in ids:
        res.append(comprimi(remux(os.path.join(base, 'comm_%s_segs' % i), key), destdir))
        print(json.dumps(res[-1], ensure_ascii=False), flush=True)
    json.dump(res, open(os.path.join(destdir, '_prep.json'), 'w'), ensure_ascii=False, indent=1)

# Trascrive le registrazioni RomaTV man mano che finiscono di scaricarsi.
# Si ferma da solo al tetto di spesa: il costo e' calcolato sui token che l'API restituisce,
# non stimato sui minuti (prova T1, STATO 35).
import os, sys, json, time, glob, shutil, subprocess
BASE = os.path.dirname(os.path.abspath(__file__))
AUD = BASE + '/rtv/audio'; MONO = BASE + '/rtv/mono'; TRA = BASE + '/rtv/trascrizioni'
KEY = os.environ['QN_KEY_AES']
TETTO_USD = float(os.environ.get('QN_ASR_TETTO_USD', '42'))
P = {'audio': 3.00 / 1e6, 'testo': 1.25 / 1e6, 'out': 5.00 / 1e6}
os.makedirs(MONO, exist_ok=True); os.makedirs(TRA, exist_ok=True)

def speso():
    tot = 0.0; ore = 0.0
    for f in glob.glob(TRA + '/*.json'):
        j = json.load(open(f)); ore += j['durata_s'] / 3600
        for p in j['pezzi']:
            u = p.get('usage') or {}; d = u.get('input_token_details') or {}
            tot += d.get('audio_tokens', 0) * P['audio'] + d.get('text_tokens', 0) * P['testo'] \
                 + u.get('output_tokens', 0) * P['out']
    return tot, ore

def pronti():
    fatti = set(l.split()[1] for l in open(AUD + '/_dl_w2w4.log') if l.startswith('DONE'))
    vivi = set()
    for l in subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout.splitlines():
        if 'rtv_audio.py' in l:
            for tok in l.split():
                if tok.startswith('rtv/audio/comm_'): vivi.add(tok.split('comm_')[1])
    out = []
    for l in open(AUD + '/_list_w2w4.tsv'):
        p = l.rstrip('\n').split('\t')
        d = AUD + '/comm_%s_segs' % p[1]
        # 'DONE' nel log non prova lo scaricamento: il rc registrato e' quello di date(1),
        # non quello di rtv_audio.py. La playlist locale si scrive solo a scaricamento finito,
        # quindi e' lei la prova.
        if p[1] in fatti and p[1] not in vivi and os.path.exists(d + '/local.m3u8'):
            out.append(p[1])
    return out

sys.path.insert(0, BASE)
from rtv_prep_audio import remux
from rtv_transcribe import trascrivi

giri_a_vuoto = 0
while True:
    c, ore = speso()
    if c >= TETTO_USD:
        print('TETTO RAGGIUNTO: $%.2f su %.1f ore. Mi fermo.' % (c, ore), flush=True); break
    resta = [i for i in pronti() if not os.path.exists(TRA + '/comm_%s.json' % i)]
    if not resta:
        giri_a_vuoto += 1
        if giri_a_vuoto > 240:
            print('Niente di nuovo da due ore: esco.', flush=True); break
        time.sleep(30); continue
    giri_a_vuoto = 0
    for i in resta:
        c, ore = speso()
        if c >= TETTO_USD:
            print('TETTO RAGGIUNTO: $%.2f su %.1f ore. Mi fermo.' % (c, ore), flush=True); sys.exit(0)
        segdir = AUD + '/comm_%s_segs' % i
        try:
            m4a = remux(segdir, KEY)
            mono = MONO + '/comm_%s.mp3' % i
            if not os.path.exists(mono):
                r = subprocess.run([__import__('imageio_ffmpeg').get_ffmpeg_exe(), '-hide_banner',
                                    '-loglevel', 'error', '-y', '-i', m4a, '-ac', '1', '-ar', '16000',
                                    '-b:a', '32k', mono], capture_output=True, text=True)
                if r.returncode != 0: raise RuntimeError(r.stderr[:200])
            shutil.rmtree(segdir, ignore_errors=True)
            res = trascrivi(mono, TRA, 'comm_%s' % i)
            json.dump(res, open(TRA + '/comm_%s.json' % i, 'w'), ensure_ascii=False, indent=1)
            if os.path.exists(m4a): os.remove(m4a)
            c, ore = speso()
            print('OK %s  %.0f min  | totale %.1f ore, $%.2f' % (i, res['durata_s'] / 60, ore, c), flush=True)
        except Exception as e:
            print('ERRORE %s: %s' % (i, str(e)[:300]), flush=True)
            time.sleep(10)

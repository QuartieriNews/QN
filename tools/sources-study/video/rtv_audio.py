# Download a RomaTV audio-only HLS stream segment by segment with curl (ffmpeg's own HTTPS crashes behind the proxy),
# rebuild a local playlist and measure it with the static ffmpeg (hls demuxer on local files).
import sys, subprocess, time, json, re, os
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
url, out = sys.argv[1].rstrip('/'), sys.argv[2]
def get(u, dest=None):
    for i in range(8):
        args = ['curl', '-sS', '--max-time', '120', '--retry', '3', '--retry-delay', '2', '--retry-all-errors', u] + (['-o', dest] if dest else [])
        r = subprocess.run(args, capture_output=True)
        if r.returncode == 0 and ((dest and os.path.exists(dest) and os.path.getsize(dest) > 0) or (not dest and r.stdout)): return r.stdout
        time.sleep(3 * (i + 1))
    raise SystemExit(f'curl failed {u}: {r.stderr[:200]}')
t0 = time.time()
pl = get(url + '/playlist.m3u8').decode()
variant = [l for l in pl.splitlines() if l and not l.startswith('#')][0]
cl = get(url + '/' + variant).decode()
segdir = out + '_segs'; os.makedirs(segdir, exist_ok=True)
local = []; nbytes = 0
for l in cl.splitlines():
    if l and not l.startswith('#'):
        name = l.split('?')[0].split('/')[-1]; dest = os.path.join(segdir, name)
        if not (os.path.exists(dest) and os.path.getsize(dest) > 0): get(url + '/' + l, dest)
        nbytes += os.path.getsize(dest); local.append(name)
    else: local.append(l)
dl = time.time() - t0
lp = os.path.join(segdir, 'local.m3u8'); open(lp, 'w').write('\n'.join(local) + '\n')
path = out + '.m4a'
r = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-protocol_whitelist', 'file', '-allowed_extensions', 'ALL', '-i', lp, '-c', 'copy', path], capture_output=True, text=True)
if r.returncode != 0: print('ffmpeg remux failed', r.stderr[:300]); path = lp
def ff(args):
    return subprocess.run([FF, '-hide_banner', '-protocol_whitelist', 'file', '-allowed_extensions', 'ALL', '-i', path] + args, capture_output=True, text=True).stderr
info = ff([])
m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info); dur = int(m[1])*3600 + int(m[2])*60 + float(m[3]) if m else None
vol = ff(['-af', 'volumedetect', '-f', 'null', '-'])
mean = re.search(r'mean_volume: ([-\d.]+)', vol); mx = re.search(r'max_volume: ([-\d.]+)', vol)
sil = ff(['-af', 'silencedetect=noise=-35dB:d=4', '-f', 'null', '-'])
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', sil)]
ends = [(float(a), float(b)) for a, b in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', sil)]
sils = [(round(s, 1), round(d, 1)) for s, (e, d) in zip(starts, ends)]
print(json.dumps({'file': path, 'segments': sum(1 for l in local if l and not l.startswith('#')), 'bytes': nbytes, 'download_s': round(dl, 1), 'duration_s': round(dur, 1) if dur else None,
    'kbps': round(nbytes * 8 / dur / 1000) if dur else None, 'mean_volume_dB': float(mean[1]) if mean else None, 'max_volume_dB': float(mx[1]) if mx else None,
    'silences_ge4s_n': len(sils), 'silence_total_s': round(sum(d for _, d in sils), 1), 'longest_silence': max(sils, key=lambda x: x[1]) if sils else None,
    'silences_ge60s': [x for x in sils if x[1] >= 60], 'stream': (re.search(r'Stream #0:0.*', info) or [None])[0]}, ensure_ascii=False))

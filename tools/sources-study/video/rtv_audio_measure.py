# Measure a downloaded RomaTV audio-only HLS stream: local playlist with the AES key fetched from the API host.
import sys, subprocess, re, os, json, shutil
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
segdir = sys.argv[1].rstrip('/'); key = sys.argv[2]
lp = os.path.join(segdir, 'local.m3u8'); txt = open(lp).read()
shutil.copy(key, os.path.join(segdir, 'key.bin'))
txt2 = re.sub(r'URI="[^"]+"', 'URI="key.bin"', txt)
lp2 = os.path.join(segdir, 'local_key.m3u8'); open(lp2, 'w').write(txt2)
out = segdir.replace('_segs', '') + '.m4a'
r = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-protocol_whitelist', 'file,crypto', '-allowed_extensions', 'ALL', '-i', lp2, '-c', 'copy', out], capture_output=True, text=True)
if r.returncode != 0: print('remux failed:', r.stderr[:400]); sys.exit(1)
def ff(args): return subprocess.run([FF, '-hide_banner', '-i', out] + args, capture_output=True, text=True).stderr
info = ff([]); m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info); dur = int(m[1])*3600 + int(m[2])*60 + float(m[3]) if m else None
vol = ff(['-af', 'volumedetect', '-f', 'null', '-']); mean = re.search(r'mean_volume: ([-\d.]+)', vol); mx = re.search(r'max_volume: ([-\d.]+)', vol)
sil = ff(['-af', 'silencedetect=noise=-35dB:d=4', '-f', 'null', '-'])
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', sil)]
ends = [(float(a), float(b)) for a, b in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', sil)]
sils = [(round(s, 1), round(d, 1)) for s, (e, d) in zip(starts, ends)]
nbytes = sum(os.path.getsize(os.path.join(segdir, f)) for f in os.listdir(segdir) if f.endswith('.aac') or f.endswith('.ts'))
print(json.dumps({'file': out, 'bytes': nbytes, 'duration_s': round(dur, 1) if dur else None, 'kbps': round(nbytes * 8 / dur / 1000) if dur else None,
    'mean_volume_dB': float(mean[1]) if mean else None, 'max_volume_dB': float(mx[1]) if mx else None, 'silences_ge4s_n': len(sils), 'silence_total_s': round(sum(d for _, d in sils), 1),
    'longest_silence': max(sils, key=lambda x: x[1]) if sils else None, 'silences_ge60s': [x for x in sils if x[1] >= 60], 'stream': (re.search(r'Stream #0:0.*', info) or [None])[0]}, ensure_ascii=False))

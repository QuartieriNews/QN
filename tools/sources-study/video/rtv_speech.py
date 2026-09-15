# Word-level confidence statistics of the RomaTV platform transcripts (speech-to-text JSON on ac104mp.streamcloud.it).
import sys, json, glob, os, subprocess, statistics as st, time, csv
items = {}
for f in glob.glob('rtv/cat/*.json'):
    for it in json.load(open(f)):
        if it.get('guid'): items[it['guid']] = it
def secs(d):
    h, m, s = d.split(':'); return int(h)*3600 + int(m)*60 + float(s)
def stats(guid):
    it = items[guid]
    src = next((t.get('speechToTextTrackSource') for t in it.get('tracks', []) if t.get('speechToTextTrackSource')), None)
    if not src: return None
    p = f'rtv/speech/{guid}.json'
    if not os.path.exists(p):
        r = subprocess.run(['curl', '-sS', '--max-time', '120', '-o', p, src], capture_output=True)
        if r.returncode != 0 or not os.path.exists(p): return {'guid': guid, 'errore': 'download'}
    try: d = json.load(open(p))
    except Exception: return {'guid': guid, 'errore': 'json'}
    words = []
    for alt in d.get('Alternatives', []): words += alt.get('Words', [])
    if not words: return {'guid': guid, 'errore': 'no words'}
    conf = [w['Confidence'] for w in words if isinstance(w.get('Confidence'), (int, float))]
    ts = sorted(secs(w['StartTime']) for w in words)
    gaps = [b - a for a, b in zip(ts, ts[1:]) if b - a > 60]
    dur = secs(it['duration'])
    return {'guid': guid, 'territorio': (it.get('parentNodes') or [''])[0] if isinstance(it.get('parentNodes'), list) else it.get('parentNodes'),
            'data_seduta': it['referenceDate'][:10], 'titolo': it['title'][:80], 'durata_s': round(dur), 'parole': len(words),
            'parole_al_minuto': round(len(words) / (dur / 60)) if dur else None, 'conf_media': round(st.mean(conf), 3), 'conf_mediana': round(st.median(conf), 3),
            'quota_conf_lt_0_7': round(sum(1 for c in conf if c < 0.7) / len(conf), 3), 'quota_conf_lt_0_5': round(sum(1 for c in conf if c < 0.5) / len(conf), 3),
            'ultima_parola_s': round(ts[-1]), 'pause_gt60s_n': len(gaps), 'pause_gt60s_tot_s': round(sum(gaps))}
if sys.argv[1] == '--all-june':
    guids = [g for g, it in items.items() if it.get('referenceDate', '').startswith('2026-06') and any(t.get('speechToTextTrackSource') for t in it.get('tracks', []))]
    out = 'rtv/speech/_stats_giugno.csv'; pause = 1.0
else:
    guids = sys.argv[1:]; out = 'rtv/speech/_stats_campione.csv'; pause = 0.3
rows = []
for g in guids:
    r = stats(g); rows.append(r or {'guid': g, 'errore': 'no track'}); print(json.dumps(rows[-1], ensure_ascii=False)); time.sleep(pause)
keys = sorted({k for r in rows for k in r}, key=lambda k: (k != 'guid', k))
with open(out, 'w', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
print('written', out, len(rows))

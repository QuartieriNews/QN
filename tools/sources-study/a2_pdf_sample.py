# Seeded sample of June Atti Web PDFs: 8 per Municipio (frame: deliver/A2_2026-06_items.csv), text vs scan, pages, chars. No AI, no OCR.
import csv, random, subprocess, os, json, time, collections, statistics as st
import fitz
rows = list(csv.DictReader(open('deliver/A2_2026-06_items.csv', encoding='utf-8')))
random.seed('2026-06-A2-pdf')
by_mun = collections.defaultdict(list)
for r in rows: by_mun[r['municipio']].append(r)
sample = []
for m in sorted(by_mun, key=lambda x: (len(x), x)):
    frame = sorted(by_mun[m], key=lambda r: (r['data_repertorio'][6:] + r['data_repertorio'][3:5] + r['data_repertorio'][:2], r['url']))
    sample += random.sample(frame, min(8, len(frame)))
os.makedirs('A2_pdf_sample', exist_ok=True)
out = []
for i, r in enumerate(sample):
    p = f"A2_pdf_sample/{r['tipologia']}_{r['municipio']}_{i}.pdf"
    if not os.path.exists(p):
        subprocess.run(['curl', '-sS', '--max-time', '60', '-o', p, r['url']], capture_output=True); time.sleep(0.3)
    try:
        doc = fitz.open(p); pages = doc.page_count; chars = sum(len(pg.get_text()) for pg in doc); doc.close()
        kind = 'testo' if pages and chars / pages >= 100 else 'scansione'
    except Exception as e:
        pages, chars, kind = None, None, 'errore'
    out.append({'municipio': r['municipio'], 'tipologia': r['tipologia'], 'data_repertorio': r['data_repertorio'], 'url': r['url'], 'kb': os.path.getsize(p) // 1024 if os.path.exists(p) else None, 'pagine': pages, 'caratteri': chars, 'formato': kind})
with open('deliver/A2_pdf_campione120.csv', 'w', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
S = {'n': len(out)}
S['per_formato'] = dict(collections.Counter(o['formato'] for o in out))
S['pagine_totali'] = sum(o['pagine'] or 0 for o in out)
S['pagine_scansione'] = sum(o['pagine'] or 0 for o in out if o['formato'] == 'scansione')
S['pagine_mediana'] = st.median([o['pagine'] for o in out if o['pagine']])
S['per_municipio'] = {m: dict(collections.Counter(o['formato'] for o in out if o['municipio'] == m)) for m in sorted({o['municipio'] for o in out})}
S['per_tipologia'] = {t: dict(collections.Counter(o['formato'] for o in out if o['tipologia'] == t)) for t in sorted({o['tipologia'] for o in out})}
S['pagine_medie_per_tipologia'] = {t: round(st.mean([o['pagine'] for o in out if o['tipologia'] == t and o['pagine']]), 1) for t in S['per_tipologia'] if any(o['pagine'] for o in out if o['tipologia'] == t)}
json.dump(S, open('deliver/summary_A2_pdf_campione120.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(S, ensure_ascii=False))

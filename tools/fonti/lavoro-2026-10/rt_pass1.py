# Passata 1: per ogni evento Romatoday salva l'HTML e legge scheda (Dove/Quando/Prezzo/Sito web), JSON-LD (NewsArticle/Event) e link esterni.
import sys, re, json, html, time, os, urllib.request, urllib.error, hashlib
S = sys.argv[1]; urls = json.load(open(f'{S}/rt/urls.json'))
UA = 'Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-eventi/1.0 (+contatto: redazione)'
def txt(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)))).strip()
SKIP = re.compile(r'(romatoday|citynews|today\.it|cibotoday|iabeurope|uspi\.it|google\.|gstatic|doubleclick|iubenda|onetrust|facebook\.com/(sharer|pages/RomaToday|dialog)|twitter\.com/(intent|share)|linkedin\.com/share|whatsapp|telegram\.me|t\.me/share|apple\.com|play\.google|microsoft\.com|w3\.org|schema\.org|creativecommons|adobe\.com|cloudflare|jquery|fonts\.)', re.I)
out = []; seen = set()
for i, u in enumerate(urls):
    if u in seen: continue
    seen.add(u); rec = {'url': u}
    f = f'{S}/rt/pages/{hashlib.md5(u.encode()).hexdigest()}.html'
    d = None
    if os.path.exists(f) and os.path.getsize(f) > 1000: d = open(f, encoding='utf-8', errors='replace').read(); rec['http'] = 200
    else:
        try:
            req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'it-IT,it;q=0.9'})
            with urllib.request.urlopen(req, timeout=40) as r: d = r.read().decode('utf-8', 'replace'); rec['http'] = r.status
            open(f, 'w', encoding='utf-8').write(d)
        except urllib.error.HTTPError as e: rec['http'] = e.code
        except Exception as e: rec['http'] = str(e)[:80]
        time.sleep(1.5)
    if d is None: out.append(rec); print(i, u, rec['http'], flush=True); continue
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', d); rec['titolo'] = html.unescape(m.group(1)) if m else None
    t = txt(d)
    m = re.search(r'\bDove\s+(.{1,300}?)\s+Quando\s+(.{1,120}?)\s+Prezzo\s+(.{1,150}?)\s+Altre informazioni\s+(.{0,300}?)\s+(?:Redazione|[A-ZÀ-Ü][^ ]{1,40}(?: [A-Za-zÀ-ü.\'’]{1,40}){0,4})\s+\d{1,2} \w+ \d{4} \d{2}:\d{2}', t)
    if m:
        rec['dove'], rec['quando'], rec['prezzo'], altre = m.group(1), m.group(2), m.group(3), m.group(4)
        ms = re.search(r'Sito web\s+(\S+)', altre); rec['sito_web'] = ms.group(1) if ms else None
        rec['altre_info'] = altre or None
    else:
        m = re.search(r'\bDove\s+(.{1,300}?)\s+Quando\s+(.{1,120}?)\s+Prezzo\s+(.{1,150}?)\s+Altre informazioni', t)
        if m: rec['dove'], rec['quando'], rec['prezzo'] = m.group(1), m.group(2), m.group(3)
        ms = re.search(r'Sito web\s+(\S+)', t); rec['sito_web'] = ms.group(1) if ms else None
    m = re.search(r'((?:[A-ZÀ-Ü][\wÀ-ü.\'’-]*\s){1,5})(\d{1,2} (?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre) \d{4} \d{2}:\d{2})', t); rec['firma'] = m.group(1).strip() if m else None
    for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', d, re.S):
        try: j = json.loads(mm.group(1))
        except Exception: continue
        for o in (j if isinstance(j, list) else [j]):
            if not isinstance(o, dict): continue
            if o.get('@type') == 'NewsArticle':
                a = o.get('author'); a = a[0] if isinstance(a, list) and a else a
                rec['promotore'] = a.get('name') if isinstance(a, dict) else a
                rec['pubblicato'] = o.get('datePublished'); rec['sommario'] = (o.get('description') or '')[:300]
            if o.get('@type') == 'Event':
                rec['ld_event'] = o
                org = o.get('organizer'); org = org[0] if isinstance(org, list) and org else org
                if isinstance(org, dict) and org.get('name') and not rec.get('promotore'): rec['promotore'] = org.get('name')
    links = []
    for l in re.findall(r'href="(https?://[^"#]+)', d):
        l = html.unescape(l)
        if SKIP.search(l) or l in links: continue
        links.append(l)
    rec['link_esterni'] = links[:20]
    out.append(rec); print(i, (rec.get('titolo') or '')[:45], '|', rec.get('promotore'), '|', rec.get('firma'), '|', rec.get('sito_web'), '|', len(links), '|', 'LD' if rec.get('ld_event') else '', flush=True)
json.dump(out, open(f'{S}/rt/pass1.json', 'w'), ensure_ascii=False, indent=1)
print('DONE', len(out))

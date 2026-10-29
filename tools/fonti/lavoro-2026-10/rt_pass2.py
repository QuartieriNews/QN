# Passata 2: per ogni evento sceglie il link ufficiale e legge l'evento alla sorgente (JSON-LD Event, Open Graph, testo).
import sys, re, json, html, time, urllib.request, urllib.error, urllib.parse, ssl, gzip
from concurrent.futures import ThreadPoolExecutor
S = sys.argv[1]; recs = json.load(open(f'{S}/rt/pass1.json'))
UA = 'Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-eventi/1.0 (+contatto: redazione)'
TICKET = re.compile(r'(vivaticket|ticketone|ticketmaster|dice\.fm|eventbrite|boxol|ticketsms|clappit|liveticket|ciaotickets|xceed|mailticket|tickettailor|ticketnation|i-ticket|oooh\.events|tiqets|getyourguide|musement|coopculture|museiincomuneroma|ticket)', re.I)
SOCIAL = re.compile(r'(facebook\.com|instagram\.com|tiktok\.com|youtube\.com|x\.com|twitter\.com|linkedin\.com|t\.me|wa\.me|whatsapp)', re.I)
def txt(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', re.sub(r'<[^>]+>', ' ', s), flags=re.S))).strip()
def dom(u):
    try: return urllib.parse.urlparse(u if '://' in u else 'https://' + u).hostname.lower().replace('www.', '')
    except Exception: return ''
def fetch(u):
    req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'it-IT,it;q=0.9', 'Accept': 'text/html,*/*'})
    with urllib.request.urlopen(req, timeout=35) as r:
        b = r.read(3_000_000)
        if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
        return r.status, r.geturl(), b.decode('utf-8', 'replace')
MESI = {m: i + 1 for i, m in enumerate(['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'])}
def date_guess(t):
    t = t[:20000]
    m = re.search(r'[Dd]al\s+(\d{1,2})(?:\s+(\w+))?\s+al\s+(\d{1,2})\s+(\w+)(?:\s+(\d{4}))?', t)
    if m and m.group(4).lower() in MESI:
        y = m.group(5) or '2026'; m1 = (m.group(2) or m.group(4)).lower()
        if m1 in MESI: return f'{y}-{MESI[m1]:02d}-{int(m.group(1)):02d}', f'{y}-{MESI[m.group(4).lower()]:02d}-{int(m.group(3)):02d}'
    m = re.search(r'\b(\d{1,2})\s+(' + '|'.join(MESI) + r')\s+(\d{4})', t, re.I)
    if m: return f'{m.group(3)}-{MESI[m.group(2).lower()]:02d}-{int(m.group(1)):02d}', None
    m = re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})', t)
    if m: return f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}', None
    return None, None
def ld_events(d):
    evs = []
    for mm in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', d, re.S | re.I):
        try: j = json.loads(mm.group(1).strip())
        except Exception:
            try: j = json.loads(re.sub(r',\s*([}\]])', r'\1', mm.group(1).strip()))
            except Exception: continue
        stack = j if isinstance(j, list) else [j]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                t = o.get('@type'); t = t if isinstance(t, str) else (t[0] if isinstance(t, list) and t else '')
                if t and 'Event' in t: evs.append(o)
                for v in o.values():
                    if isinstance(v, (dict, list)): stack.append(v)
            elif isinstance(o, list): stack.extend(o)
    return evs
def s(v):
    if isinstance(v, dict): return v.get('name') or v.get('url') or v.get('streetAddress') or json.dumps(v, ensure_ascii=False)[:200]
    if isinstance(v, list): return '; '.join(str(s(x)) for x in v)
    return v
def meta(d, name):
    m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']*)' % re.escape(name), d, re.I)
    if not m: m = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']%s["\']' % re.escape(name), d, re.I)
    return html.unescape(m.group(1)) if m else None
def choose(rec):
    links = rec.get('link_esterni') or []; site = (rec.get('sito_web') or '').replace('/span>', '').strip()
    sd = dom(site) if site else ''
    tickets = [l for l in links if TICKET.search(l)]
    fb = [l for l in links if 'facebook.com' in l]; ig = [l for l in links if 'instagram.com' in l]
    cand = [l for l in links if not SOCIAL.search(l) and not TICKET.search(l)]
    if sd:
        same = [l for l in cand if dom(l) == sd or dom(l).endswith('.' + sd)]
        if same: return max(same, key=len), 'pagina evento sul sito ufficiale', tickets, fb, ig
        if not SOCIAL.search(site) and not TICKET.search(site): return ('https://' + site if '://' not in site else site), 'sito ufficiale (home o pagina indicata)', tickets, fb, ig
    if cand: return cand[0], 'link esterno nell\'articolo', tickets, fb, ig
    if fb: return fb[0], 'facebook', tickets, fb, ig
    if tickets: return tickets[0], 'biglietteria', tickets, fb, ig
    if ig: return ig[0], 'instagram', tickets, fb, ig
    if sd: return 'https://' + site, 'sito ufficiale (social)', tickets, fb, ig
    return None, 'nessun link', tickets, fb, ig
def work(rec):
    o = dict(rec); link, tipo, tickets, fb, ig = choose(rec)
    o.update({'link_ufficiale': link, 'tipo_link': tipo, 'link_biglietti': tickets[0] if tickets else None, 'link_facebook': fb[0] if fb else None, 'link_instagram': ig[0] if ig else None})
    if not link or tipo in ('facebook', 'instagram', 'sito ufficiale (social)'):
        o['sorgente_esito'] = 'non letta: ' + tipo; return o
    try:
        st, final, d = fetch(link); o['sorgente_http'] = st; o['sorgente_url_finale'] = final
    except urllib.error.HTTPError as e: o['sorgente_http'] = e.code; o['sorgente_esito'] = f'HTTP {e.code}'; return o
    except Exception as e: o['sorgente_esito'] = 'errore: ' + str(e)[:80]; return o
    evs = ld_events(d)
    if evs:
        e = evs[0]; loc = e.get('location') or {}; loc = loc[0] if isinstance(loc, list) and loc else loc
        addr = loc.get('address') if isinstance(loc, dict) else None
        off = e.get('offers'); off = off[0] if isinstance(off, list) and off else off
        o.update({'sorgente_esito': 'JSON-LD Event', 'sorgente_titolo': s(e.get('name')), 'sorgente_inizio': s(e.get('startDate')), 'sorgente_fine': s(e.get('endDate')),
                  'sorgente_luogo': s(loc.get('name')) if isinstance(loc, dict) else s(loc), 'sorgente_indirizzo': (addr.get('streetAddress') if isinstance(addr, dict) else s(addr)),
                  'sorgente_organizzatore': s(e.get('organizer')), 'sorgente_prezzo': (s(off.get('price')) if isinstance(off, dict) else None), 'sorgente_biglietti': (s(off.get('url')) if isinstance(off, dict) else None),
                  'sorgente_descrizione': txt(str(s(e.get('description')) or ''))[:800], 'sorgente_immagine': s(e.get('image'))})
    else:
        t = txt(d); st_, en_ = date_guess(t)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', d, re.S)
        o.update({'sorgente_esito': 'pagina letta (senza JSON-LD Event)', 'sorgente_titolo': meta(d, 'og:title') or (txt(h1.group(1)) if h1 else None) or txt(re.search(r'<title>(.*?)</title>', d, re.S).group(1) if re.search(r'<title>(.*?)</title>', d, re.S) else ''),
                  'sorgente_inizio': st_, 'sorgente_fine': en_, 'sorgente_descrizione': (meta(d, 'og:description') or meta(d, 'description') or t[:600])[:800], 'sorgente_immagine': meta(d, 'og:image')})
    tk = [l for l in re.findall(r'href=["\'](https?://[^"\'#]+)', d) if TICKET.search(l)]
    if tk and not o.get('link_biglietti'): o['link_biglietti'] = tk[0]
    return o
out = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for i, o in enumerate(ex.map(work, recs)):
        out.append(o); print(i, o.get('tipo_link'), '|', o.get('sorgente_esito'), '|', (o.get('sorgente_titolo') or '')[:50], flush=True)
json.dump(out, open(f'{S}/rt/pass2.json', 'w'), ensure_ascii=False, indent=1)
print('DONE', len(out))

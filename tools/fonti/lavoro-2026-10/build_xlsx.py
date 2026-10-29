import json, sys, glob, re, os
from datetime import datetime, timedelta, timezone
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

pages_dir, urls_file, out_path = sys.argv[1:4]
items = []
for f in sorted(glob.glob(os.path.join(pages_dir, '*.json')), key=lambda p: int(re.search(r'(\d+)', os.path.basename(p)).group(1))):
    d = json.load(open(f))
    if isinstance(d, dict):
        d = d.get('items') or d.get('data') or d.get('content') or d
    items.extend(d)
print('items', len(items))
urls = json.load(open(urls_file))

def norm(u):
    m = re.search(r'/events/(\d+)', u or '')
    return m.group(1) if m else (u or '')

def end_date(it):
    s, dur = it.get('utcStartDate'), it.get('duration')
    if not s or not dur: return None
    try:
        h = m = 0
        mh = re.search(r'(\d+)\s*h', str(dur)); mm = re.search(r'(\d+)\s*m', str(dur))
        if mh: h = int(mh.group(1))
        if mm: m = int(mm.group(1))
        if not mh and not mm: return None
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return (dt + timedelta(hours=h, minutes=m)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    except Exception:
        return None

def flatten(obj, prefix='', out=None):
    out = {} if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f'{prefix}.{k}' if prefix else k
            if key.startswith('coverVideo') and key not in ('coverVideo.permalink_url', 'coverVideo.id'):
                continue
            flatten(v, key, out)
    elif isinstance(obj, list):
        if all(not isinstance(x, (dict, list)) for x in obj):
            out[prefix] = '; '.join('' if x is None else str(x) for x in obj) if obj else None
        else:
            # list of objects: one column per sub-field, values joined
            keys = []
            for x in obj:
                if isinstance(x, dict):
                    for k in x: 
                        if k not in keys: keys.append(k)
            for k in keys:
                out[f'{prefix}.{k}'] = '; '.join('' if (not isinstance(x, dict) or x.get(k) is None) else str(x.get(k)) for x in obj)
            out[f'{prefix}.count'] = len(obj)
    else:
        out[prefix] = obj
    return out

rows = [flatten(it) for it in items]
for r, it in zip(rows, items):
    r['utcEndDate (calcolata)'] = end_date(it)

preferred = ['inputUrl','url','id','name','description','dateTimeSentence','utcStartDate','startTime','utcEndDate (calcolata)','duration','eventFrequency',
 'address','location.name','location.contextualName','location.streetAddress','location.city','location.countryCode','location.placeType','location.latitude','location.longitude','location.url','location.id',
 'organizedBy','organizators.name','organizators.url','organizators.id','organizators.isVerified',
 'ticketsInfo.buyUrl','ticketsInfo.price','ticketsInfo.title','ticketsInfo.subtitle','ticketsInfo.ticketProvider','externalLinks',
 'usersGoing','usersInterested','usersResponded','imageUrl','imageCaption','eventType','privacyInfo','isCanceled','isPast','isOnline','paidContent','hasChildEvents',
 'childEvents.id','childEvents.url','childEvents.utcStartDate','childEvents.utcEndDate','childEvents.duration','childEvents.count',
 'discoveryCategories.label','discoveryCategories.url','error','errorDescription']
allkeys = []
for r in rows:
    for k in r:
        if k not in allkeys: allkeys.append(k)
cols = [c for c in preferred if c in allkeys] + sorted(k for k in allkeys if k not in preferred)

wb = Workbook(); ws = wb.active; ws.title = 'Facebook'
ws.append(cols)
for c in ws[1]: c.font = Font(bold=True)
for r in rows:
    vals = []
    for c in cols:
        v = r.get(c)
        if isinstance(v, (dict, list)): v = json.dumps(v, ensure_ascii=False)
        if isinstance(v, str):
            v = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v)
            if len(v) > 32000: v = v[:32000]
        vals.append(v)
    ws.append(vals)
for i, c in enumerate(cols, 1):
    ws.column_dimensions[get_column_letter(i)].width = 60 if c == 'description' else min(45, max(12, len(c) + 2))
ws.freeze_panes = 'A2'

# coverage report
got = {}
for it in items:
    k = norm(it.get('inputUrl')) or norm(it.get('url'))
    got.setdefault(k, []).append(it)
ok, failed, missing = [], [], []
for u in urls:
    k = norm(u); its = got.get(k, [])
    good = [i for i in its if i.get('name') and not i.get('error')]
    if good: ok.append(u)
    elif its: failed.append((u, '; '.join(str(i.get('error') or i.get('errorDescription') or 'item senza nome') for i in its)))
    else: missing.append(u)
extra = [k for k in got if k not in {norm(u) for u in urls}]
ws2 = wb.create_sheet('Mancanti'); ws2.append(['URL', 'Esito', 'Dettaglio']); 
for c in ws2[1]: c.font = Font(bold=True)
for u, e in failed: ws2.append([u, 'FALLITO', e])
for u in missing: ws2.append([u, 'MANCANTE', 'nessun item nel dataset'])
ws2.column_dimensions['A'].width = 55; ws2.column_dimensions['B'].width = 12; ws2.column_dimensions['C'].width = 80
wb.save(out_path)
print(f'URL totali {len(urls)} | con evento {len(ok)} | falliti {len(failed)} | mancanti {len(missing)} | item extra non richiesti {len(extra)}')
json.dump({'ok': ok, 'failed': failed, 'missing': missing, 'extra': extra, 'n_items': len(items), 'cols': cols}, open(os.path.join(os.path.dirname(out_path), 'report.json'), 'w'), indent=1)

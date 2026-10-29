# Costruisce il tab Romatoday → sorgente e lo integra nel file unico (Riepilogo, Eventi unificati).
import json, sys, re
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S, UNICO = sys.argv[1], sys.argv[2]
d = json.load(open(f'{S}/rt/pass2.json'))
def ld(r, k):
    e = r.get('ld_event') or {}; v = e.get(k)
    if isinstance(v, dict): v = v.get('name') or v.get('address') or v.get('url')
    return v
def iso_from_quando(q):
    m = re.search(r'Dal (\d{2})/(\d{2})/(\d{4}) al (\d{2})/(\d{2})/(\d{4})', q or '')
    return (f'{m.group(3)}-{m.group(2)}-{m.group(1)}', f'{m.group(6)}-{m.group(5)}-{m.group(4)}') if m else (None, None)
cols = ['url_romatoday','titolo_romatoday','firma','promotore_dichiarato','dove','quando','inizio','fine','prezzo','sito_web','link_ufficiale','tipo_link','link_biglietti','link_facebook','link_instagram','sorgente_esito','sorgente_http','sorgente_url_finale','sorgente_titolo','sorgente_inizio','sorgente_fine','sorgente_luogo','sorgente_indirizzo','sorgente_organizzatore','sorgente_prezzo','sorgente_biglietti','sorgente_descrizione','sorgente_immagine','pubblicato_romatoday']
rows = []
for r in d:
    ini, fin = iso_from_quando(r.get('quando')); ini = ini or ld(r, 'startDate'); fin = fin or ld(r, 'endDate')
    rows.append({'url_romatoday': r['url'], 'titolo_romatoday': r.get('titolo'), 'firma': r.get('firma'), 'promotore_dichiarato': r.get('promotore'), 'dove': r.get('dove') or ld(r, 'location'), 'quando': r.get('quando'), 'inizio': ini, 'fine': fin, 'prezzo': r.get('prezzo'), 'sito_web': r.get('sito_web'), 'pubblicato_romatoday': r.get('pubblicato'), **{k: r.get(k) for k in cols if k.startswith(('link_', 'tipo_', 'sorgente_'))}})
def clean(v):
    if isinstance(v, (dict, list)): v = json.dumps(v, ensure_ascii=False)
    if isinstance(v, str): v = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v)[:32000]
    return v
wb = openpyxl.load_workbook(UNICO)
for name in ('Romatoday (non analizzato)', 'Romatoday → sorgente'):
    if name in wb.sheetnames: del wb[name]
ws = wb.create_sheet('Romatoday → sorgente', 5); ws.append(cols)
for c in ws[1]: c.font = Font(bold=True)
for r in rows: ws.append([clean(r.get(c)) for c in cols])
for i, c in enumerate(cols, 1): ws.column_dimensions[get_column_letter(i)].width = 60 if c in ('sorgente_descrizione',) else (50 if 'url' in c or 'link' in c or 'titolo' in c else 18)
ws.freeze_panes = 'A2'
# Eventi unificati: aggiunge le righe Romatoday (dati della sorgente quando ci sono, altrimenti la scheda)
wu = wb['Eventi unificati']
for r in rows:
    src = r.get('sorgente_esito') == 'JSON-LD Event'
    wu.append([clean(v) for v in ['Romatoday → sorgente' if src else 'Romatoday (scheda)', (r.get('sorgente_titolo') if src else None) or r.get('titolo_romatoday'), (r.get('sorgente_inizio') if src else None) or r.get('inizio'), (r.get('sorgente_fine') if src else None) or r.get('fine'), r.get('quando'), (r.get('sorgente_luogo') if src else None) or r.get('dove'), r.get('sorgente_indirizzo') if src else None, 'Roma', None, None, None, (r.get('sorgente_organizzatore') if src else None) or r.get('promotore_dichiarato') or (r.get('sito_web')), r.get('link_biglietti') or r.get('sorgente_biglietti'), None, r.get('link_ufficiale') or r['url_romatoday'], r.get('sorgente_immagine')]])
# riordina Eventi unificati per data
hdr = [c.value for c in wu[1]]; data = [[c.value for c in row] for row in wu.iter_rows(min_row=2)]
data.sort(key=lambda x: (str(x[2] or '9999'), str(x[1] or '')))
wu.delete_rows(2, wu.max_row); 
for x in data: wu.append(x)
# Riepilogo
wr = wb['Riepilogo']
n_src = sum(1 for r in rows if r.get('sorgente_esito') == 'JSON-LD Event'); n_read = sum(1 for r in rows if (r.get('sorgente_esito') or '').startswith('pagina letta')); n_link = sum(1 for r in rows if r.get('link_ufficiale'))
for row in wr.iter_rows(min_row=2):
    if row[0].value == 'Romatoday':
        row[1].value = 'analizzato in due passate (23 ott 2026)'; row[2].value = len(rows)
        row[3].value = f'{len(rows)} pagine evento Romatoday lette per promotore, scheda (Dove/Quando/Prezzo) e link ufficiale; poi {n_link} sorgenti ufficiali lette'
        row[4].value = f'sorgente con dati strutturati (JSON-LD Event): {n_src}; sorgente letta senza dati strutturati: {n_read}; senza link ufficiale leggibile: {len(rows)-n_link}; scheda Romatoday disponibile per {sum(1 for r in rows if r.get("dove"))}'
wb.save(UNICO)
import collections
print('righe', len(rows)); print('esiti', collections.Counter(r.get('sorgente_esito') for r in rows).most_common()); print('tipo link', collections.Counter(r.get('tipo_link') for r in rows).most_common())

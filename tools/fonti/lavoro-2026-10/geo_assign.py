# Assegna municipio, quartiere (OSM) e pagina QN (gazetteer del repository) a ogni evento del file unico.
import sys, re, json, unicodedata, collections
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S, UNICO, GAZ = sys.argv[1], sys.argv[2], sys.argv[3]
geo = json.load(open(f'{S}/geo/geo.json')); gz = json.load(open(GAZ))
MUN = json.load(open(f'{S}/geo/municipi.json'))['features']
def _pip(x, y, poly):
    inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i][:2]; x2, y2 = poly[(i + 1) % n][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-300) + x1: inside = not inside
    return inside
def municipio_poligono(lat, lon):
    for f in MUN:
        g_ = f['geometry']; polys = g_['coordinates'] if g_['type'] == 'MultiPolygon' else [g_['coordinates']]
        for p in polys:
            if _pip(float(lon), float(lat), p[0]) and not any(_pip(float(lon), float(lat), h) for h in p[1:]): return f['properties'].get('numero_rom')
    return None
def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"\bs\.\s*", 'san ', s); s = re.sub(r'[^a-z0-9 ]+', ' ', s); return re.sub(r'\s+', ' ', s).strip()
names = {}
for n in gz['neighbourhoods']:
    for a in [n['name_display']] + re.split(r'[;|/]', n.get('aliases') or ''):
        a = norm(a)
        if a and a not in names: names[a] = n
        if a and a.replace(' ', '') not in names: names[a.replace(' ', '')] = n
zones = {z['publication_zone_id']: z for z in gz['publication_zones']}
for z in gz['publication_zones']:
    names.setdefault(norm(z['name_display']), {'neighbourhood_id': None, 'name_display': z['name_display'], 'publication_zone_id': z['publication_zone_id'], 'municipality_code': z['primary_municipality'], 'publishable': z['is_page']})
ROM = {'I':'I','II':'II','III':'III','IV':'IV','V':'V','VI':'VI','VII':'VII','VIII':'VIII','IX':'IX','X':'X','XI':'XI','XII':'XII','XIII':'XIII','XIV':'XIV','XV':'XV'}
def municipio_from(addr):
    for k, v in (addr or {}).items():
        m = re.match(r'Municipio Roma (\w+)', str(v))
        if m and m.group(1) in ROM: return m.group(1)
    return None
def quartiere_from(addr):
    for k in ('quarter', 'neighbourhood', 'suburb', 'hamlet', 'village', 'town', 'city_district', 'borough', 'residential'):
        v = (addr or {}).get(k)
        if v and not str(v).startswith('Municipio Roma'): return v
    return None
def zona_from(addr, mun):
    cands = [(addr or {}).get(k) for k in ('quarter', 'neighbourhood', 'suburb', 'hamlet', 'village', 'residential', 'city_district', 'town', 'borough', 'isolated_dwelling') if (addr or {}).get(k)]
    for c0 in cands:
        c0 = str(c0); forms = [norm(c0), norm(c0).replace(' ', '')]
        for part in re.split(r'\s*[-–/]\s*|\s+e\s+', c0): forms += [norm(part), norm(part).replace(' ', '')]
        w = norm(c0).split()
        for k in range(len(w) - 1, 0, -1): forms.append(' '.join(w[:k]))
        forms.append(re.sub(r'^(quartiere|rione|zona|borgata|lido di) ', '', norm(c0)))
        n = next((names[f] for f in forms if f in names), None); c = c0
        if n and (not mun or not n.get('municipality_code') or n['municipality_code'] == mun or 'spans' in str(n.get('spans_municipalities') or '')):
            return n['publication_zone_id'], n['name_display'], 'gazetteer: ' + c
    return None, None, None
from parse_dove import parse_dove, VIE
wb = openpyxl.load_workbook(UNICO); ws = wb['Eventi unificati']; h = [c.value for c in ws[1]]; g = lambda r, k: r[h.index(k)]
rows = [list(r) for r in ws.iter_rows(min_row=2, values_only=True)]
if 'municipio_assegnato' in h:   # rilancio: scarta le colonne geo precedenti
    cut = h.index('municipio_assegnato'); h = h[:cut]; rows = [r[:cut] for r in rows]
    ws.delete_cols(cut + 1, ws.max_column - cut)
rt = wb['Romatoday → sorgente']; rh = [c.value for c in rt[1]]; rtdove = {}
for rr in rt.iter_rows(min_row=2, values_only=True):
    for k in ('url_romatoday', 'link_ufficiale'):
        if rr[rh.index(k)] and rr[rh.index('dove')]: rtdove[rr[rh.index(k)]] = rr[rh.index('dove')]
newcols = ['municipio_assegnato', 'quartiere_osm', 'zona_qn', 'zona_qn_nome', 'geo_metodo', 'geo_nota']
stats = collections.Counter(); byurl = {}
for r in rows:
    f = g(r, 'fonte'); addr = None; metodo = None; nota = None; mun = None; lat = g(r, 'lat'); lon = g(r, 'lon')
    if lat and lon:
        addr = geo['points'].get(f'{round(float(lat),5)},{round(float(lon),5)}'); metodo = 'coordinate della fonte → reverse OSM'
    else:
        key = None
        if f.startswith('Comune') and g(r, 'indirizzo'): key = f'street|{g(r,"indirizzo")}|Roma'
        elif f.startswith('Romatoday') and (rtdove.get(g(r, 'url')) or g(r, 'luogo')):
            st, town, venue = parse_dove(rtdove.get(g(r, 'url')) or g(r, 'luogo'))
            if st and 'non disponibile' not in st.lower(): key = f'street|{st}|{town or "Roma"}'
            elif venue and venue.lower() not in ('roma', ''): key = f'q|{venue}, Roma|'
        elif f == 'Facebook' and (g(r, 'indirizzo') or g(r, 'luogo')): key = f'q|{g(r,"indirizzo") or g(r,"luogo")}, Roma|'
        hit = geo['addrs'].get(key) if key else None
        if hit:
            addr = hit['address']; metodo = 'indirizzo geocodificato OSM' if key.startswith('street') else 'nome del luogo geocodificato OSM (verificare)'
            if not lat: r[h.index('lat')] = float(hit['lat']); r[h.index('lon')] = float(hit['lon'])
        elif key: nota = 'indirizzo non trovato su OSM'
    mun = municipio_poligono(r[h.index('lat')], r[h.index('lon')]) if (r[h.index('lat')] and r[h.index('lon')]) else None
    if mun: metodo = (metodo or '') + ' + municipio dal poligono ufficiale (Geoportale)'
    elif addr: mun = municipio_from(addr)
    if not mun and addr and (addr.get('city') or addr.get('town') or addr.get('village')) and addr.get('city') != 'Roma':
        nota = 'fuori Roma: ' + str(addr.get('town') or addr.get('city') or addr.get('village'))
    quart = quartiere_from(addr)
    zona, zona_nome, zmet = zona_from(addr, mun)
    # dati già nella fonte
    mun_fonte = g(r, 'municipio'); mf = re.search(r'\b([IVX]+)\b', str(mun_fonte or ''))
    if not mun and mf: mun = mf.group(1); metodo = (metodo + '; ' if metodo else '') + 'municipio dalla fonte'
    elif mun and mf and mf.group(1) != mun: nota = (nota + '; ' if nota else '') + f'la fonte indica Municipio {mf.group(1)}'
    if f.startswith('Fonte locale'):
        metodo = 'municipio e zona dal foglio Fonti locali'
    if zona is None and f.startswith('Fonte locale') and g(r, 'municipio'): pass
    if not f.startswith('Fonte locale'): stats[(f.split(':')[0].split(' (')[0], 'mun' if mun else '-', 'zona' if zona else '-')] += 1
    r += [mun, quart, zona, zona_nome, metodo, nota]
    byurl[g(r, 'url')] = (mun, quart, zona, zona_nome)
# Fonti locali: zona_qn dal foglio originale
fl = wb['Fonti locali 13-31 ott']; fh = [c.value for c in fl[1]]
flz = {}
for rr in fl.iter_rows(min_row=2, values_only=True): flz[rr[fh.index('pagina_letta')]] = (rr[fh.index('zona_qn')], rr[fh.index('municipio')])
for r in rows:
    if g(r, 'fonte').startswith('Fonte locale') and g(r, 'url') in flz:
        z, m = flz[g(r, 'url')]
        if z: r[len(h) + 2] = z; r[len(h) + 3] = zones.get(z, {}).get('name_display', z)
        if m and not r[len(h)]: r[len(h)] = str(m)
        byurl[g(r, 'url')] = (r[len(h)], r[len(h)+1], r[len(h)+2], r[len(h)+3])
        stats[('Fonte locale', 'mun' if r[len(h)] else '-', 'zona' if r[len(h)+2] else '-')] += 1
for c in newcols:
    if c not in h: ws.cell(1, len(h) + newcols.index(c) + 1, c).font = Font(bold=True)
for i, r in enumerate(rows, 2):
    for j, v in enumerate(r, 1): ws.cell(i, j, v)
for j, c in enumerate(newcols, len(h) + 1): ws.column_dimensions[get_column_letter(j)].width = 22
# propaga ai tab di fonte tramite url
for tab, ucol in (('Facebook', 'url'), ('Comune di Roma (culture)', 'url'), ('Romatoday → sorgente', 'url_romatoday')):
    t = wb[tab]; th = [c.value for c in t[1]]
    if 'municipio_assegnato' in th: t.delete_cols(th.index('municipio_assegnato') + 1, t.max_column - th.index('municipio_assegnato')); th = th[:th.index('municipio_assegnato')]
    base = len(th) + 1
    for k, c in enumerate(['municipio_assegnato', 'quartiere_osm', 'zona_qn', 'zona_qn_nome']): t.cell(1, base + k, c).font = Font(bold=True)
    ui = th.index(ucol); n = 0
    for i, rr in enumerate(t.iter_rows(min_row=2, values_only=True), 2):
        v = byurl.get(rr[ui]) or (byurl.get(next((u for u in byurl if u and rr[ui] and (u == rr[ui])), None)))
        if v:
            for k, x in enumerate(v): t.cell(i, base + k, x)
            n += 1
    print(tab, 'righe geo-assegnate', n)
# Riepilogo
wr = wb['Riepilogo']; wr.cell(1, 6, 'Geografia').font = Font(bold=True)
tot = collections.defaultdict(lambda: [0, 0, 0])
for (f, m, z), v in stats.items(): tot[f][0] += v; tot[f][1] += v if m == 'mun' else 0; tot[f][2] += v if z == 'zona' else 0
for row in wr.iter_rows(min_row=2):
    for f, (n, m, z) in tot.items():
        if str(row[0].value).startswith(f): row[5].value = f'municipio assegnato a {m}/{n}, pagina QN a {z}/{n}'
wr.column_dimensions['F'].width = 45
wb.save(UNICO)
for k, v in sorted(stats.items()): print(v, k)

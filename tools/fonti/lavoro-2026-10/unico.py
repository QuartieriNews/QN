import json, sys, re
from datetime import datetime
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

S, OUT = sys.argv[1], sys.argv[2]
TODAY = '2026-10-23'
def clean(v):
    if isinstance(v, str):
        v = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v)
        return v[:32000]
    return v
def addsheet(wb, title, header, rows, widths=None):
    ws = wb.create_sheet(title); ws.append(header)
    for c in ws[1]: c.font = Font(bold=True)
    for r in rows: ws.append([clean(v) for v in r])
    for i, h in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, min(45, max(12, len(h) + 2)))
    ws.freeze_panes = 'A2'; return ws

# --- Facebook (from the run of today) ---
fb = openpyxl.load_workbook(f'{S}/../../../../../mnt/user-data/outputs/facebook_eventi.xlsx' if False else '/mnt/user-data/outputs/facebook_eventi.xlsx')
fb_rows = list(fb['Facebook'].iter_rows(values_only=True)); fb_h = list(fb_rows[0]); fb_rows = fb_rows[1:]
fb_missing = list(fb['Mancanti'].iter_rows(values_only=True))[1:]
# --- culture.roma.it (Apify run RBMmIabj8Sq1Ne6ge, 20 Oct) ---
cul = [x for x in json.load(open(f'{S}/culture/items.json')) if not x.get('seed')]
def gd(s):  # 20261022T193000 -> 2026-10-22T19:30:00
    return f'{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}:{s[13:15]}' if s and len(s) >= 15 else None
for x in cul:
    x['inizio'] = gd(x.get('gcalStart')); x['fine'] = gd(x.get('gcalEnd'))
cul_cur = [x for x in cul if (x.get('fine') or x.get('inizio') or '') >= '2026-10-01']
cul_cols = ['url','wpId','title','subtitle','datesText','inizio','fine','sezioni','labels','gratuito','venue','venueUrl','address','municipio','manifestazione','manifestazioneUrl','description','ingresso','ingressoLinks','aCuraDi','contatti','contattiLinks','accessibilita','accessibile','orari','social','tags','imageUrl','icalUrl','breadcrumb','wpPublished','wpModified','wpTagIds','wpMunicipioIds','wpSezioniIds','wpTipologiaIds','wpEstateRomanaIds','otherWidgets']
# --- Fonti locali (Drive sheet, 13 Oct) ---
fl = openpyxl.load_workbook(f'{S}/drive/Eventi_letti_alla_fonte_13_31_ottobre_2026_completo_due_pass.xlsx').worksheets[0]
fl_rows = list(fl.iter_rows(values_only=True)); fl_h = list(fl_rows[0]); fl_rows = fl_rows[1:]
# --- Romatoday URL list (Drive sheet "eventi /") ---
rt = [r[0] for r in openpyxl.load_workbook(f'{S}/drive/eventi_new.xlsx')['Romatoday'].iter_rows(values_only=True) if r[0]]

wb = Workbook(); wb.remove(wb.active)
# Riepilogo
riep = wb.create_sheet('Riepilogo')
riep.append(['Fonte', 'Stato', 'Eventi nel file', 'Origine dei dati', 'Note'])
for c in riep[1]: c.font = Font(bold=True)
riep.append(['Facebook', 'scaricato oggi (23 ott 2026)', len(fb_rows), 'Apify apify/facebook-events-scraper, run tOKJy9yqjegtpFbPV, dataset YHjmmtkesVV2LY3xF', f'584 URL in input: 567 eventi, 17 URL senza evento (tab "Facebook mancanti")'])
riep.append(['Comune di Roma (culture.roma.it)', 'già scaricato il 20 ott 2026', len(cul_cur), 'Apify apify/cheerio-scraper, run RBMmIabj8Sq1Ne6ge, dataset L0ppe0aPgOIqmiFGX', f'il dataset ha {len(cul)} appuntamenti pubblicati dal 1 lug 2025; nel file quelli con fine dal 1 ott 2026 in poi'])
riep.append(['Fonti locali 13-31 ottobre', 'già fatto il 13 ott 2026', len(fl_rows), 'Foglio Drive "Eventi letti alla fonte — 13-31 ottobre 2026 (completo, due passate)"', 'teatri, musei, cinema, club letti alla fonte; colonna anche_su_romatoday'])
riep.append(['Romatoday', 'NON analizzato', 0, f'{len(rt)} URL nel tab "Romatoday" del foglio Drive "eventi /"', 'nessun run Apify esistente; robots.txt di Citynews vieta scraping, data mining e uso per AI senza licenza scritta; nel repository è registrato come "nessun canale senza licenza"'])
for col, w in zip('ABCDE', (34, 30, 16, 70, 90)): riep.column_dimensions[col].width = w
# Eventi unificati
def fbget(r, k): return r[fb_h.index(k)] if k in fb_h else None
uni = []
for r in fb_rows:
    uni.append(['Facebook', fbget(r,'name'), fbget(r,'utcStartDate'), fbget(r,'utcEndDate (calcolata)'), fbget(r,'dateTimeSentence'), fbget(r,'location.name'), fbget(r,'location.streetAddress') or fbget(r,'address'), fbget(r,'location.city'), None, fbget(r,'location.latitude'), fbget(r,'location.longitude'), fbget(r,'organizators.name') or fbget(r,'organizedBy'), fbget(r,'ticketsInfo.buyUrl'), fbget(r,'usersInterested'), fbget(r,'url'), fbget(r,'imageUrl')])
for x in cul_cur:
    uni.append(['Comune di Roma (culture.roma.it)', x.get('title'), x.get('inizio'), x.get('fine'), x.get('datesText'), x.get('venue'), x.get('address'), 'Roma', x.get('municipio'), None, None, x.get('aCuraDi'), x.get('ingressoLinks'), None, x.get('url'), x.get('imageUrl')])
fi = {h: i for i, h in enumerate(fl_h)}
def d(v): return v.strftime('%Y-%m-%d') if isinstance(v, datetime) else v
for r in fl_rows:
    uni.append(['Fonte locale: ' + str(r[fi['nome_fonte']]), r[fi['evento']], d(r[fi['data_inizio']]), d(r[fi['data_fine']]), None, r[fi['luogo_indicato']] or r[fi['nome_fonte']], None, 'Roma', r[fi['municipio']], None, None, r[fi['nome_fonte']], None, None, r[fi['pagina_letta']], None])
uni.sort(key=lambda r: (r[2] or '9999', str(r[1] or '')))
addsheet(wb, 'Eventi unificati', ['fonte','nome','inizio','fine','data_testo','luogo','indirizzo','città','municipio','lat','lon','organizzatore','link_biglietti_o_ingresso','interessati_fb','url','immagine'], uni, {'nome': 50, 'luogo': 32, 'indirizzo': 30, 'url': 50, 'fonte': 30})
addsheet(wb, 'Facebook', fb_h, fb_rows, {'description': 60})
addsheet(wb, 'Comune di Roma (culture)', cul_cols, [[x.get(c) for c in cul_cols] for x in cul_cur], {'description': 60, 'title': 45, 'url': 50})
addsheet(wb, 'Fonti locali 13-31 ott', fl_h, [[d(v) for v in r] for r in fl_rows], {'evento': 45, 'pagina_letta': 50})
addsheet(wb, 'Romatoday (non analizzato)', ['url', 'stato'], [[u, 'non analizzato: robots.txt Citynews vieta scraping e uso AI senza licenza'] for u in rt], {'url': 70, 'stato': 70})
addsheet(wb, 'Facebook mancanti', ['URL', 'Esito', 'Dettaglio'], fb_missing, {'URL': 55, 'Dettaglio': 90})
wb.save(OUT)
print('facebook', len(fb_rows), 'culture tot', len(cul), 'culture dal 1 ott', len(cul_cur), 'fonti locali', len(fl_rows), 'romatoday url', len(rt), 'unificati', len(uni))

# Manifest delle immagini degli eventi (DEC-101: provenienza, credito, link all'evento, rimozione) + archivio zip per Drive
import json,os,zipfile,collections,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'; O='/mnt/user-data/outputs'
R=json.load(open(f'{P}/immagini.json'))
SL={r['host']:r for r in json.load(open(f'{P}/siti_letti.json'))}
PF={}
for p in json.load(open(f'{P}/promotori_finale.json')):
    for i in p['eventi_idx']: PF.setdefault(i,p)
GZ=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); PAGES={z['publication_zone_id']:z['name_display'] for z in GZ['publication_zones'] if z['is_page']}
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Immagini'
cols=['id','image_local_path','esito','titolo','inizio','pagina_qn','fonte','image_credit','url_evento','source_image_url','image_fetched_at','image_removed',
      'larghezza','altezza','larghezza_originale','altezza_originale','diffusione_promotore','nota']
ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
for r in sorted(R,key=lambda r:(r['esito']!='scaricata',r['inizio'] or '',r['titolo'] or '')):
    p=PF.get(r['evento_idx']) or {}
    nota=None
    if p.get('diffusione')=='riproduzione vietata': nota='la fonte vieta la riproduzione dei contenuti: usare la card generata'
    elif p.get('diffusione')=='licenza aperta': nota='la fonte dichiara una licenza aperta: verificare i termini (spesso non commerciale)'
    ws.append([r['id'],r.get('image_local_path'),r['esito'],r['titolo'],r['inizio'],PAGES.get(r.get('pagina_qn'),r.get('pagina_qn')),r['fonte'],r.get('image_credit'),r.get('url_evento'),
               r.get('source_image_url'),r.get('image_fetched_at'),r.get('image_removed'),r.get('larghezza'),r.get('altezza'),r.get('larghezza_originale'),r.get('altezza_originale'),p.get('diffusione'),nota])
W={'titolo':50,'url_evento':45,'source_image_url':45,'image_credit':35,'esito':40,'nota':50}
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=W.get(c,16)
ws.freeze_panes='B2'; ws.auto_filter.ref=ws.dimensions
m=wb.create_sheet('Regole')
for t in ['DEC-101: immagine scaricata alla prima acquisizione e servita in locale a risoluzione da card (qui lato lungo 800 px, JPEG), con cinque cautele: credito e link alla fonte (image_credit, url_evento); provenienza (source_image_url, image_fetched_at); risoluzione ridotta; rimozione su richiesta (image_removed = vero → card generata, l\'articolo resta); niente asset con watermark o commerciali.',
          'Non scaricate: Roma Today (licenza Citynews, DEC-026), eventi Fever (asset commerciali), blocchi di testo dei siti senza una pagina dell\'evento (l\'immagine sarebbe quella del sito, non dell\'evento).',
          'Le URL delle immagini Facebook sono firmate e scadono in pochi giorni: per questo il file locale è la copia di riferimento; source_image_url resta come provenienza, non come link da servire.',
          'Diffusione del promotore: posizione della fonte sui suoi contenuti (foglio promotori_eventi.xlsx, scheda «Diffusione per fonte»); dove la fonte vieta la riproduzione si usa la card generata.']:
    m.append([t])
m.column_dimensions['A'].width=170
wb.save(f'{O}/immagini_eventi_manifest.xlsx')
z=f'{O}/immagini_eventi.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_STORED) as zf:
    for r in R:
        if r.get('image_local_path') and os.path.exists(f"{O}/{r['image_local_path']}"): zf.write(f"{O}/{r['image_local_path']}",r['image_local_path'])
    zf.write(f'{O}/immagini_eventi_manifest.xlsx','immagini_eventi_manifest.xlsx')
print(collections.Counter(r['esito'] if not r['esito'].startswith('errore') else 'errore' for r in R).most_common(), round(os.path.getsize(z)/1e6,1),'MB')

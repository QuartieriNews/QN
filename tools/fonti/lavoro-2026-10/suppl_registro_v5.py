# Registro fonti v5 = v4 + soggetti nuovi della lista supplementare per le pagine deboli (candidati: decide l'owner)
import json,re,sys,collections,openpyxl
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/supplementare')
src=open(f'{S}/supplementare/eventi_suppl.py').read(); exec(src[src.index('ENTE=re.compile'):src.index('for o in L:')])   # ENTE, soggetto
L=json.load(open(f'{S}/supplementare/lista.json')); E=json.load(open(f'{S}/supplementare/eventi_suppl.json'))
SL={r['fonte']:r for r in json.load(open(f'{S}/supplementare/siti_letti.json'))}
def host(u): m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#]+)',str(u or '').strip().lower()); return m.group(1) if m else None
nev=collections.Counter(e['fonte'] for e in E)
def rtipo(o):
    t,n=o['tipo'],o['nome'].lower()
    if t=='comitato di quartiere o civico': return 'comitato_quartiere'
    if t=='parrocchia o chiesa cattolica': return 'parrocchia'
    if t=='centro anziani': return 'centro_anziani'
    if t=='centro sociale, anziani o di quartiere': return 'centro_anziani' if 'anzian' in n else 'centro_culturale'
    if t.startswith('luogo culturale'): return 'teatro' if 'teatr' in n else 'biblioteca' if 'bibliotec' in n else 'centro_culturale'
    if t=='comunità religiosa': return 'luogo_di_culto'
    return 'associazione_locale'
def entra(o):
    if o['gia_nota'] or not o['ente']: return False
    canale=bool(o.get('sito') or o.get('facebook'))
    if o['tipo'] in ('sport','comunità religiosa'): return nev.get(o['nome'],0)>0 or (canale and re.search(r'(?i)polisportiv|asd|ssd|a\.s\.d|circolo|oratori|comunit',o['nome']) is not None)
    return True
for o in L: o['ente']=soggetto(o)
rw=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v4.xlsx'); rs=rw.worksheets[0]; h=[c.value for c in rs[1]]
last=max(int(str(r[h.index('chiave')].value).split('-')[1]) for r in rs.iter_rows(min_row=2) if r[h.index('chiave')].value)
n=collections.Counter()
for o in sorted((o for o in L if entra(o)),key=lambda o:(o['pagina'],o['tipo'],o['nome'])):
    last+=1; sito=o.get('sito'); sito=sito if not sito or sito.startswith('http') else 'https://'+sito
    sl=SL.get(host(sito)) or {}
    dove=sl.get('pagina_eventi') or sito or o.get('facebook') or o.get('gruppo_facebook')
    canale='sito' if sito else 'facebook' if o.get('facebook') else 'da_trovare'
    zm='coordinate della sede' if o.get('lat') else 'toponimo cercato nel nome o nella descrizione'
    ev=nev.get(o['nome'],0)
    vals={'chiave':f'FE-{last:04d}','decisione':'candidata','nome':o['nome'][:120],'tipo':rtipo(o),'zona_qn':o['pagina'],'municipio':o['municipio'],'sotto_soglia':'sì',
          'canale':canale,'link':sito,'facebook':o.get('facebook'),'instagram':o.get('instagram'),'origine':'lista_supplementare_2026-10-25','eventi_visti':ev or None,
          'motivo':f"candidata: {o['tipo']} nella pagina debole ({o['origini']})"+(f" · {ev} eventi futuri trovati" if ev else '')+f" · zona: {zm}",'dove_cercare':dove}
    rs.append([vals.get(c) for c in h]); n[vals['tipo']]+=1
rw.save('/mnt/user-data/outputs/registro_fonti_v5.xlsx')
print('righe aggiunte',sum(n.values()),dict(n),'ultima chiave',f'FE-{last:04d}')

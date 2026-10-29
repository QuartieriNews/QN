# Fonti mirate per le pagine deboli: risultati Google per pagina/tipo + liste aperte (IC, mercati) + schedario wiki -> candidate per pagina e registro v2
import json,re,sys,collections,unicodedata,urllib.parse,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S=sys.argv[1]; OUT=sys.argv[2]; REG=sys.argv[3]
weak=json.load(open(f'{S}/mirate/pagine_deboli.json')); meta=json.load(open(f'{S}/mirate/query_meta.json'))
google=json.load(open(f'{S}/mirate/google.json')); import os
liste=(json.load(open(f'{S}/mirate/liste.json')) if os.path.exists(f'{S}/mirate/liste.json') else [])+(json.load(open(f'{S}/mirate/csa.json')) if os.path.exists(f'{S}/mirate/csa.json') else [])+(json.load(open(f'{S}/mirate/bib.json')) if os.path.exists(f'{S}/mirate/bib.json') else [])
sched=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); zones={z['publication_zone_id']:z for z in gz['publication_zones']}
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
names={}
for n in gz['neighbourhoods']:
    for a in [n['name_display']]+re.split(r'[;|/]',n.get('aliases') or ''):
        if norm(a): names.setdefault(norm(a),n)
for z in gz['publication_zones']: names.setdefault(norm(z['name_display']),{'publication_zone_id':z['publication_zone_id'],'municipality_code':z['primary_municipality'],'publishable':z['is_page']})
def match(sd,mun):
    if not sd: return None
    c=norm(re.sub(r'^(quartiere|rione|zona|suburbio|borgata) ','',sd,flags=re.I)); w=c.split()
    for f in [c]+[' '.join(w[:k]) for k in range(len(w)-1,0,-1)]:
        n=names.get(f)
        if n and n.get('publishable',True) and (not mun or not n.get('municipality_code') or n['municipality_code']==mun): return n['publication_zone_id']
    return None
AGG=re.compile(r'(romatoday|citynews|wikipedia|tripadvisor|paginegialle|paginebianche|virgilio|tuttocitta|cylex|misterimprese|infobel|yelp|google\.|youtube|tiktok|twitter|x\.com|linkedin|eventbrite|spotlightapp|vibeloop|eventivicino|zazoom|roma-o-matic|araundapp|experience-app|indeed|subito\.it|immobiliare|idealista|casa\.it|booking|airbnb|amazon|ebay|trovaprezzi|iltempo|ilmessaggero|corriere|repubblica|fanpage|leggo|romah24|abitarearoma|roma\.cityrumors|vignaclarablog|canaledieci|ilfaroonline|ostiatv|romaest|ilcaffe|ilcorrieredellacitta|lagone|ilmamilio|comune\.roma\.it/web/it/notizia|istruzione\.it|miur|cercalatuascuola|scuolainchiaro|tuttitalia|comuni-italiani|prolocoitalia|qn\.|quartierinews)',re.I)
TIPO_DOMINIO=[(r'facebook\.com','facebook'),(r'instagram\.com','instagram'),(r'bibliotechediroma\.it','biblioteca'),(r'\.edu\.it$','istituto_comprensivo'),(r'comune\.roma\.it','istituzione'),(r'culture\.roma\.it','luogo_culture')]
TIPO_Q={'parrocchia':'parrocchia','centro anziani':'centro_anziani','comitato di quartiere':'comitato_quartiere','biblioteca':'biblioteca','centro culturale':'centro_culturale','istituto comprensivo':'istituto_comprensivo','associazione eventi':'associazione_locale','pro loco OR consorzio':'pro_loco_consorzio'}
byq={m['query']:m for m in meta}
KEY={'parrocchia':r'parrocchi|chiesa|basilica|\bsan\b|\bsanta\b|\bsanti\b|\bss\.|oratorio|comunit[aà] pastorale',
     'centro_anziani':r'centro (sociale )?anziani|centro sociale|\bcsa\b|anziani',
     'comitato_quartiere':r'comitato|consulta|\bcdq\b|rete (di )?quartiere|cittadin',
     'biblioteca':r'bibliotec|biblio|libro|lettura',
     'centro_culturale':r'centro cultural|casa della cultura|polo cultural|spazio|teatro|casa del quartiere|centro civico|circolo|arci|officin|laborator',
     'istituto_comprensivo':r'istituto comprensivo|\bi\.?c\.?\b|scuola|liceo',
     'associazione_locale':r'associazion|\baps\b|\basd\b|\bodv\b|onlus|polisportiva|circolo|collettivo|gruppo',
     'pro_loco_consorzio':r'pro ?loco|consorzio|comprensorio'}
NOISE=re.compile(r'(casa di riposo|residenza|\brsa\b|villa .* anziani|badant|assistenza domiciliare|affitt|vendit|in vendita|lavoro|offerte|recension|orari di apertura|come arrivare|numero di telefono|mappa|cap \d{5}|^via |^viale |^piazza |^largo )',re.I)
NEWSHOST=re.compile(r'(dailymotion|vimeo|arte\.it|mipiaceroma|romatoday|8xmille|waze|aiutoanziani|dindondan|hospitalia|oraridiapertura|orarimesse|messe\.|trovachiesa|chiesedi|cultura\.gov|censimento|mapquest|moovit|yellow|trova|elenco|directory|guida|portale|annunci|prontopro|trustpilot|cercaparrocchie|parrocchiaonline|exibart|artribune|senato\.it|camera\.it|gazzetta|ansa\.it|romasette|ilgiornale|lastampa|tgcom|rainews|roma\.repubblica|info\.roma\.it|romapaese|romasegreta|romaierioggidomani|quartierisud|parrocchie\.it|parrocchiemap|chiesacattolica\.it|anzianionline|centrianziani|residenzeanziani|casediriposo|rsa|strutture|cercascuola|scuole\.it|skuola|studenti\.it|classeviva|orizzontescuola|tecnicadellascuola|miur|istruzione|nostrofiglio|famigliacristiana|avvenire|ilsussidiario|vaticannews|diocesi|tuttitalia|italiapedia|comuni-italiani|openstreetmap|mapcarta|cylex|hotfrog|infobel|wikimapia|foursquare|yelp|nextdoor|telegram|t\.me|wa\.me|issuu|slideshare|scribd|academia|researchgate|prezi|linktr|bit\.ly)',re.I)
cand=collections.defaultdict(dict)   # zona -> key -> record
GENERIC={'roma','associazione','comitato','parrocchia','biblioteca','centro','scuola','istituto','pro loco','consorzio','contatto','contatti','home','chi siamo','eventi','news'}
def add(z,rec):
    k=norm(rec['nome'])[:60] or rec.get('link') or rec.get('facebook')
    if not k or norm(rec['nome']) in GENERIC or len(norm(rec['nome']))<5: return
    cur=cand[z].get(k)
    if cur:
        for f in ('link','facebook','instagram','indirizzo','email'): cur[f]=cur.get(f) or rec.get(f)
        cur['prove']=sorted(set(cur['prove'])|set(rec['prove']))
    else: cand[z][k]=rec
for r in google:
    q=r.get('searchQuery',{}).get('term') if isinstance(r.get('searchQuery'),dict) else r.get('searchQuery'); m=byq.get(q)
    if not m: continue
    z=m['zona']; zn=norm(m['nome']); ztoks=[t for t in zn.split() if len(t)>2]
    for o in (r.get('organicResults') or [])[:10]:
        u=o.get('url') or ''; t=o.get('title') or ''; d=o.get('description') or ''
        if not u or AGG.search(u): continue
        blob=norm(t+' '+d)
        if not all(tok in blob for tok in ztoks): continue     # il nome del quartiere deve comparire nel titolo o nello snippet
        host=urllib.parse.urlsplit(u).netloc.lower().replace('www.','')
        if NEWSHOST.search(host) or NOISE.search(t): continue
        tipo=next((tp for rx,tp in TIPO_DOMINIO if re.search(rx,host)),None)
        tq=TIPO_Q[m['tipo']]; tt=norm(t)
        has_key=bool(re.search(KEY[tq],t,re.I)) or (tipo in ('biblioteca','istituto_comprensivo','luogo_culture'))
        has_zone=all(tok in tt for tok in ztoks)
        if not has_key and not (tipo in ('facebook','instagram') and has_zone): continue
        if tipo not in ('facebook','instagram','biblioteca','istituto_comprensivo','luogo_culture') and not has_zone: continue   # un sito senza il nome del quartiere nel titolo non è attribuibile
        if tipo in ('facebook','instagram'):
            mm=re.match(r'https?://(?:www\.|m\.)?facebook\.com/([^/?#]+)',u)
            if not mm or mm.group(1).lower() in ('events','groups','pages','people','profile.php','share','hashtag','public','watch','reel','photo','photos','story','posts','p','marketplace','login','help'): continue
            slug=mm.group(1); link=None; fb=f'https://www.facebook.com/{slug}'; ttl=re.sub(r'\s*[|\-–].*$','',t).strip()
            if len(ttl)>60 or re.search(r'[!…]|^\W|\b(nasce|apre|torna|ospita|inaugura|dal \d|il \d)\b',ttl,re.I): ttl=re.sub(r'[._-]+',' ',slug).strip().title() if not slug.isdigit() else ttl[:60]
            rec={'nome':ttl or slug,'tipo':TIPO_Q[m['tipo']],'canale':'facebook','link':None,'facebook':fb,'instagram':None,'prove':[f"ricerca «{m['tipo']}»"],'snippet':d[:200],'origine':'ricerca mirata 2026-10-24'}
        else:
            if tipo=='luogo_culture' and '/luogo/' not in u: continue
            ttl=re.sub(r'\s*[|\-–]\s*(Home|Sito ufficiale|Roma Capitale|Biblioteche di Roma).*$','',t).strip()
            if tipo=='istituto_comprensivo' and not re.search(r'istituto comprensivo|\bi\.?c\.?\b|scuola|liceo',ttl,re.I): ttl='IC '+re.sub(r'^ic|\.edu\.it$','',host).replace('-',' ').title()
            if tipo=='istituzione' and not re.search(r'municipio|biblioteca|centro|casa|mercato|parco|villa',ttl,re.I): continue
            rec={'nome':ttl[:90],'tipo':tipo if tipo in ('biblioteca','istituto_comprensivo','luogo_culture','istituzione') else TIPO_Q[m['tipo']],'canale':'sito','link':u if tipo in ('luogo_culture','biblioteca','istituzione') else f"https://{urllib.parse.urlsplit(u).netloc}",'facebook':None,'instagram':None,'prove':[f"ricerca «{m['tipo']}»"],'snippet':d[:200],'origine':'ricerca mirata 2026-10-24'}
        add(z,rec)
# liste aperte
for r in liste:
    z=match(r.get('sudd_nome'),r.get('municipio'))
    if z in weak: add(z,{'nome':r['nome'],'tipo':r['tipo'],'canale':'sito' if r.get('sito') else 'da_trovare','link':r.get('sito'),'facebook':None,'instagram':None,'indirizzo':r.get('indirizzo'),'email':r.get('email'),'prove':[r['origine']],'snippet':None,'origine':r['origine']})
# schedario esistente
already=collections.defaultdict(list)
for e in sched:
    if e['zona'] in weak: already[e['zona']].append(e)
# output
reg=openpyxl.load_workbook(REG,read_only=True).worksheets[0]; rr=list(reg.iter_rows(values_only=True)); rh=rr[0]; regrows=[dict(zip(rh,r)) for r in rr[1:]]
regnames={norm(r['nome']) for r in regrows}; regfb={str(r.get('facebook')).rstrip('/').lower() for r in regrows if r.get('facebook')}
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Candidate per pagina'
cols=['zona_qn','pagina','municipio','eventi_futuri_oggi','fonti_gia_in_wiki','nome','tipo','canale','dove_cercare','link','facebook','indirizzo','email','prove','snippet','gia_nel_registro']
ws.append(cols)
for c in ws[1]: c.font=Font(bold=True)
new_reg=[]; k=370; perpage=collections.Counter()
for z,v in sorted(weak.items(),key=lambda kv:(kv[1]['eventi_futuri'],kv[0])):
    recs=sorted(cand[z].values(),key=lambda r:(-len(r['prove']),r['tipo'],r['nome']))
    pertipo=collections.Counter(); kept=[]
    for r in recs:
        pertipo[r['tipo']]+=1
        if pertipo[r['tipo']]<=5: kept.append(r)
    recs=kept
    for r in recs:
        dove=(r['link'] if r['link'] and r['link']!=f"https://{urllib.parse.urlsplit(r['link']).netloc}" else None) or (r['facebook'].rstrip('/')+'/events' if r.get('facebook') else r['link'])
        inreg=norm(r['nome']) in regnames or ((r.get('facebook') or '').rstrip('/').lower() in regfb if r.get('facebook') else False)
        ws.append([z,v['nome'],v['municipio'],v['eventi_futuri'],len(already[z]),r['nome'],r['tipo'],r['canale'],dove,r['link'],r.get('facebook'),r.get('indirizzo'),r.get('email'),'; '.join(r['prove']),r.get('snippet'),'sì' if inreg else None])
        perpage[z]+=1
        if not inreg:
            k+=1; new_reg.append({'chiave':f'FE-{k:04d}','decisione':'candidata','nome':r['nome'],'tipo':r['tipo'],'zona_qn':z,'municipio':v['municipio'],'sotto_soglia':'sì','canale':r['canale'],'formato':None,'robots':None,'link':r['link'],'facebook':r.get('facebook'),'instagram':None,'origine':'fonti_mirate_2026-10-24','eventi_visti':None,'motivo':'; '.join(r['prove']),'dove_cercare':dove})
for i,c in enumerate(cols,1): ws.column_dimensions[get_column_letter(i)].width=45 if c in ('nome','dove_cercare','link','snippet','prove') else 14
ws.freeze_panes='A2'
wr=wb.create_sheet('Riepilogo per pagina'); wr.append(['zona_qn','pagina','municipio','eventi_futuri_oggi','fonti_gia_in_wiki','candidate_nuove','tipi_coperti','almeno_3'])
for c in wr[1]: c.font=Font(bold=True)
for z,v in sorted(weak.items(),key=lambda kv:(kv[1]['eventi_futuri'],kv[0])):
    tipi=sorted({r['tipo'] for r in cand[z].values()}); wr.append([z,v['nome'],v['municipio'],v['eventi_futuri'],len(already[z]),perpage[z],', '.join(tipi),'sì' if perpage[z]+len(already[z])>=3 else 'NO'])
wr.column_dimensions['G'].width=60
wb.save(OUT)
# registro v2
wb2=openpyxl.Workbook(); w2=wb2.active; w2.title='registro'; cols2=list(rh)+['dove_cercare']; w2.append(cols2)
for c in w2[1]: c.font=Font(bold=True)
for r in regrows: w2.append([r.get(c) for c in cols2])
for r in new_reg: w2.append([r.get(c) for c in cols2])
for i,c in enumerate(cols2,1): w2.column_dimensions[get_column_letter(i)].width=40 if c in ('nome','link','facebook','dove_cercare','motivo') else 14
w2.freeze_panes='A2'; wb2.save(OUT.replace('fonti_mirate','registro_fonti_v2'))
print('pagine',len(weak),'candidate',sum(perpage.values()),'nuove nel registro',len(new_reg),'pagine con >=3 fonti (wiki+nuove)',sum(1 for z in weak if perpage[z]+len(already[z])>=3))
print(collections.Counter(r['tipo'] for r in new_reg).most_common())

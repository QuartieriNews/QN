# Sintesi della rilettura «notizie dai dati»: unisce smistamento, schede, verifiche e fusione (journal del workflow)
# con il corpus e i metadati delle fonti; geografia dal luogo (toponimi del gazetteer) o dalla sede della fonte.
# Uscite: foglio per Drive (con le sintesi scritte da noi e i link alle fonti) e numeri aggregati per il repository.
import json,re,sys,collections,unicodedata
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
J=sys.argv[1]; OUT=sys.argv[2] if len(sys.argv)>2 else '/mnt/user-data/outputs/notizie_dai_dati_2026-10-26.xlsx'
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
exec(open(f'{S}/notizie/filtro.py').read().split("C=json.load(open(f'{S}/notizie/corpus_tutto.json'))")[0].split('TEMI={')[0])
import email.utils
def data_iso(s):
    s=str(s or '')
    if re.match(r'\d{4}-\d{2}-\d{2}',s): return s[:10]
    try: return email.utils.parsedate_to_datetime(s).date().isoformat()
    except Exception: return None
C={}
for i,it in enumerate(json.load(open(f'{S}/notizie/corpus_tutto.json'))): it['id']=f'N{i:05d}'; it['data']=data_iso(it['data']); C[it['id']]=it
A={};B={};V={};G=[]
for l in open(J):
    r=json.loads(l)
    if r.get('type')!='result' or not isinstance(r.get('result'),dict): continue
    res=r['result']
    if 'gruppi' in res: G+=res['gruppi']; continue
    for x in res.get('items',[]):
        if 'utile' in x: A.setdefault(x['id'],x)
        elif 'confermata' in x: V[x['id']]=x
        elif 'tema' in x: B[x['id']]=x
# ---- geografia: toponimi del gazetteer nel luogo, altrimenti sede della fonte ----
g=json.load(open('/home/user/QN/gazetteer/gazetteer.json'))
PZ={z['publication_zone_id']:z for z in g['publication_zones']}
STOP=set(g['free_text_stoplist'])|set(g['never_substring'])
NAMES=[]
for z in g['publication_zones']:
    if z.get('is_page'): NAMES.append((norm(z['name_display']),z['publication_zone_id']))
for n in g['neighbourhoods']:
    if not n.get('publication_zone_id') or n['publication_zone_id'] not in PZ: continue
    for a in [n['name_display']]+[x.strip() for x in str(n.get('aliases') or '').split(';') if x.strip()]:
        NAMES.append((norm(a),n['publication_zone_id']))
NAMES=sorted({(a,z) for a,z in NAMES if len(a)>=4 and a not in STOP},key=lambda t:-len(t[0]))
ROM={'i':'I','ii':'II','iii':'III','iv':'IV','v':'V','vi':'VI','vii':'VII','viii':'VIII','ix':'IX','x':'X','xi':'XI','xii':'XII','xiii':'XIII','xiv':'XIV','xv':'XV'}
def geo(scheda,meta):
    t=' '+norm(scheda.get('luogo'))+' '
    for a,z in NAMES:
        if f' {a} ' in t: return z,PZ[z]['primary_municipality'],'toponimo nel luogo'
    m=re.search(r'municipio (x{0,1}v?i{0,3}v?|[ivx]+)\b',t)
    if m and m.group(1) in ROM: return None,ROM[m.group(1)],'municipio nel luogo'
    if scheda.get('livello_geo') in ('citta',): return None,None,'tutta la città'
    if meta and meta.get('zona'): return meta['zona'],meta.get('municipio'),'sede della fonte'
    return None,(meta or {}).get('municipio'),'non assegnata'
# ---- righe ----
gruppo_di={}
for k,gr in enumerate(G):
    for i in gr['ids']: gruppo_di.setdefault(i,k)
righe=[]
for i,b in B.items():
    it=C.get(i); 
    if not it: continue
    v=V.get(i); m=it.get('meta') or {}
    z,mun,how=geo(b,m)
    stato='confermata' if v and v['confermata'] else ('scartata dalla verifica' if v else ('scheda senza verifica' if b['blocco']!='scarta' else 'scartata in scheda'))
    righe.append({'id':i,'stato':stato,'data':it['data'],'blocco':(v or {}).get('blocco_finale') or b['blocco'],'tema':b['tema'],'origine':b.get('origine'),'livello_geo':b['livello_geo'],
                  'luogo':b['luogo'],'zona':z,'pagina':PZ[z]['name_display'] if z in PZ else None,'municipio':mun,'geo_da':how,'attualita':b['attualita'],
                  'punteggio':(v or {}).get('punteggio_finale',b['punteggio']),'sensibile':b['sensibile'],'motivo_sensibile':b['motivo_sensibile'],
                  'sintesi':(v or {}).get('sintesi_finale') or b['sintesi'],'motivo_verifica':(v or {}).get('motivo'),'fonte':it['nome_fonte'],'canale':it['tipo'],'lotto':it['lotto'],
                  'link':it.get('url') or it.get('feed'),'fonte_id':m.get('id'),'tipo_fonte':m.get('categoria') or m.get('tipo'),'eventi_fonte':m.get('eventi'),
                  'registro':m.get('registro'),'censimento':m.get('verdetto'),'gruppo':gruppo_di.get(i)})
json.dump({'righe':righe,'A':A,'gruppi':G},open(f'{S}/notizie/sintesi.json','w'),ensure_ascii=False)
conf=[r for r in righe if r['stato']=='confermata']
# fatti unici: un gruppo di doppioni conta una volta
fatti={}
for r in conf:
    k=('g',r['gruppo']) if r['gruppo'] is not None else ('i',r['id'])
    fatti.setdefault(k,[]).append(r)
st={'smistate':len(A),'utili_smistamento':sum(1 for x in A.values() if x['utile'] and x['punteggio']>=3),'schede':len(B),'verificate':len(V),
    'confermate':len(conf),'fatti_unici':len(fatti),'gruppi_doppioni':len(G)}
st['smistamento_blocchi']=dict(collections.Counter(x['blocco'] for x in A.values()).most_common())
st['blocchi_confermate']=dict(collections.Counter(r['blocco'] for r in conf).most_common())
st['temi_confermate']=dict(collections.Counter(r['tema'] for r in conf).most_common())
st['origine_confermate']=dict(collections.Counter(r['origine'] for r in conf).most_common())
st['geo_confermate']=dict(collections.Counter(r['geo_da'] for r in conf).most_common())
st['canale_confermate']=dict(collections.Counter(r['canale'] for r in conf).most_common())
st['mesi_confermate']=dict(sorted(collections.Counter(r['data'][:7] for r in conf).items()))
st['sensibili_confermate']=sum(1 for r in conf if r['sensibile'])
st['pagine_con_notizie']=len({r['zona'] for r in conf if r['zona']})
st['municipi_confermate']=dict(sorted(collections.Counter(r['municipio'] or '—' for r in conf).items()))
json.dump(st,open(f'{S}/notizie/numeri.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(st,ensure_ascii=False,indent=1)[:3000])
# ---- fonti di notizie e pagine ----
utili=[r for r in righe if r['stato'] in ('confermata','scheda senza verifica')]
F=collections.defaultdict(lambda:{'confermate':0,'utili':0,'blocchi':collections.Counter(),'temi':collections.Counter(),'meta':None,'canale':None})
for r in utili:
    f=F[(r['fonte'],r['fonte_id'])]; f['utili']+=1; f['confermate']+=r['stato']=='confermata'; f['blocchi'][r['blocco']]+=1; f['temi'][r['tema']]+=1
    f['meta']=(r['tipo_fonte'],r['eventi_fonte'],r['registro'],r['censimento']); f['canale']=r['canale']
fonti=sorted(F.items(),key=lambda kv:(-kv[1]['confermate'],-kv[1]['utili'],kv[0][0].lower()))
st['fonti_con_notizie']=len(fonti); st['fonti_con_confermate']=sum(1 for _,f in fonti if f['confermate'])
st['fonti_senza_eventi_con_notizie']=sum(1 for _,f in fonti if f['confermate'] and not (f['meta'][1] or 0))
P=collections.defaultdict(lambda:[0,0])
for r in utili:
    if r['zona']: P[r['zona']][0]+=r['stato']=='confermata'; P[r['zona']][1]+=1
st['pagine_con_almeno_una_confermata']=sum(1 for v in P.values() if v[0])
json.dump(st,open(f'{S}/notizie/numeri.json','w'),ensure_ascii=False,indent=1)
import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
wb=openpyxl.Workbook(); BF=Font(bold=True); HF=PatternFill('solid',fgColor='DDEBF7')
def head(ws,h,w):
    ws.append(h)
    for c in ws[1]: c.font=BF; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
    for i,x in enumerate(w,1): ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width=x
    ws.freeze_panes='A2'
ORD={'notizia di quartiere':0,'istituzionale':1,'servizio o avviso utile':2,'segnalazione o tema dei residenti':3}
ws=wb.active; ws.title='Notizie confermate'
head(ws,['data','blocco','tema','pagina QN','municipio','luogo','geografia da','sintesi (parole nostre)','punteggio','attualità','origine','sensibile','fonti (stesso fatto)','n fonti','fonte principale','canale','link alla fonte','id'],
     [11,22,20,20,9,28,16,70,9,18,22,9,40,7,30,16,50,9])
for k,rs in sorted(fatti.items(),key=lambda kv:(ORD.get(kv[1][0]['blocco'],9),-max(r['punteggio'] for r in kv[1]),max(r['data'] or '' for r in kv[1])),reverse=False):
    rs=sorted(rs,key=lambda r:(-r['punteggio'],r['data'] or ''))
    r0=next((r for r in rs if k[0]=='g' and r['id']==G[k[1]]['rappresentante']),rs[0])
    ws.append([r0['data'],r0['blocco'],r0['tema'],r0['pagina'],r0['municipio'],r0['luogo'],r0['geo_da'],r0['sintesi'],r0['punteggio'],r0['attualita'],r0['origine'],
               'sì' if any(r['sensibile'] for r in rs) else None,' · '.join(sorted({r['fonte'] for r in rs})),len({r['fonte'] for r in rs}),r0['fonte'],r0['canale'],r0['link'],r0['id']])
ws=wb.create_sheet('Da vedere (non verificate)')
head(ws,['data','blocco','tema','pagina QN','municipio','luogo','sintesi (parole nostre)','punteggio','attualità','origine','sensibile','fonte','canale','link alla fonte','stato','id'],
     [11,22,20,20,9,28,70,9,18,22,9,30,16,50,22,9])
for r in sorted([r for r in righe if r['stato']!='confermata' and r['blocco']!='scarta'],key=lambda r:(-r['punteggio'],r['data'] or ''),reverse=False):
    ws.append([r['data'],r['blocco'],r['tema'],r['pagina'],r['municipio'],r['luogo'],r['sintesi'],r['punteggio'],r['attualita'],r['origine'],'sì' if r['sensibile'] else None,r['fonte'],r['canale'],r['link'],r['stato'],r['id']])
ws=wb.create_sheet('Fonti di notizie')
head(ws,['fonte','id schedario','tipo o categoria','canale','notizie confermate','notizie utili','blocchi','temi principali','eventi a ottobre','registro','censimento'],[40,13,30,18,10,10,40,50,9,14,14])
for (nome,fid),f in fonti:
    t,ev,reg,cen=f['meta']
    ws.append([nome,fid,t,f['canale'],f['confermate'],f['utili'],', '.join(f'{a} {b}' for a,b in f['blocchi'].most_common()),', '.join(f'{a} {b}' for a,b in f['temi'].most_common(3)),ev or 0,reg,cen])
ws=wb.create_sheet('Per pagina QN')
head(ws,['pagina QN','id','municipio','notizie confermate','notizie utili'],[26,26,9,12,12])
for z,zz in sorted(PZ.items(),key=lambda kv:kv[1]['name_display']):
    if not zz.get('is_page'): continue
    ws.append([zz['name_display'],z,zz['primary_municipality'],P[z][0],P[z][1]])
def gruppo(r):
    n=(r['fonte'] or '').lower(); t=(r['tipo_fonte'] or '').lower()
    if re.search(r'\bcdq\b|comitat|consulta|rete (di|dei) cittadin|residenti|abitanti',n): return 'comitati di quartiere e di cittadini'
    if re.search(r'municipio|consiglier|assessor|presidente|zevi|gualtieri|veloccia|politic',n) or 'politic' in t: return 'municipi, eletti e politica'
    if re.search(r'z[eè]tema|roma capitale|parco archeologico|sovrintendenza|auditorium|musica per roma|asl|ospedal|regione|atac|ama\b|biblioteche|museo|musei',n): return 'enti pubblici e culturali'
    if re.search(r'parrocchi|chiesa|diocesi|santuario|caritas',n) or 'parrocch' in t or 'relig' in t: return 'parrocchie e realtà religiose'
    if re.search(r'scuol|istituto comprensivo|liceo|\bic\b',n) or 'scuol' in t: return 'scuole'
    if re.search(r'villa|parco|verde|riserva|ambient|legambiente|wwf|caffarella|\borti\b',n) or 'ambient' in t: return 'associazioni per verde e ambiente'
    if re.search(r'trasport|mobilit|\bbus\b|metro',n): return 'pagine di cittadini su trasporti'
    if re.search(r'\bsport|calcio|\basd\b|polisportiv',n) or 'sport' in t: return 'sport'
    return 'altre associazioni e realtà'
st['tipo_fonte_confermate']=dict(collections.Counter(gruppo(r) for r in conf).most_common())
st['tipo_fonte_fonti']=dict(collections.Counter(gruppo(r) for r in {r['fonte']:r for r in conf}.values()).most_common())
json.dump(st,open(f'{S}/notizie/numeri.json','w'),ensure_ascii=False,indent=1)
ws=wb.create_sheet('Per tipo di fonte')
head(ws,['tipo di fonte','fonti con notizie confermate','notizie confermate','notizie utili'],[40,14,12,12])
U=collections.Counter(gruppo(r) for r in utili)
for k,v in st['tipo_fonte_confermate'].items(): ws.append([k,st['tipo_fonte_fonti'].get(k,0),v,U[k]])
ws=wb.create_sheet('Numeri')
head(ws,['voce','valore'],[50,80])
for k,v in st.items(): ws.append([k,json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v])
ws=wb.create_sheet('Leggimi',0); ws.column_dimensions['A'].width=150
for l in ["Notizie di quartiere dai dati già raccolti (rilettura a ritroso, 26 ottobre 2026)","",
          f"Voci rilette: {st['smistate']} (post Facebook di associazioni, comitati, parrocchie, scuole, enti e luoghi, e notizie dei loro siti), dal 24 aprile al 25 ottobre 2026. Nessuna lettura nuova, nessuna spesa Apify. Testate e media esclusi.",
          f"Tre passaggi: smistamento di tutte le voci; scheda per le {st['schede']} utili (blocco, tema, origine, luogo, attualità, sintesi scritta da noi); verifica scettica delle migliori ({st['verificate']}). Confermate {st['confermate']}, pari a {st['fatti_unici']} fatti dopo la fusione dei doppioni.",
          "Blocchi: Notizie di quartiere, Istituzionale, Servizi e avvisi utili, Segnalazioni e temi dei residenti. Gli eventi restano nel loro blocco.",
          "La sintesi è scritta da noi e non riproduce il testo della fonte; il link porta alla fonte. Prima di pubblicare vanno applicate le regole del blocco (DEC-108 per la cronaca, nomi, minori, presunzione di innocenza).",
          "Geografia: pagina QN dal luogo del fatto quando contiene un toponimo del gazetteer, altrimenti dalla sede della fonte (colonna «geografia da»). La sede della fonte è un'ipotesi da verificare: un eletto o un ente cittadino può parlare di un luogo lontano dalla sua sede.",
          f"Chi le produce: {st['fonti_con_confermate']} fonti con notizie confermate; {st['fonti_senza_eventi_con_notizie']} di queste non avevano dato nessun evento alla pagina degli eventi. Le voci sensibili (minori, salute, vittime, persone nominate) sono segnate: {st['sensibili_confermate']} fra le confermate.",
          "Esclusi a monte: testate e media; nello smistamento i rilanci di articoli di giornale senza fatti propri (DEC-108 resta la regola per la cronaca di stampa).",
          "Fogli: Notizie confermate (un fatto per riga), Da vedere (schede non verificate o declassate), Fonti di notizie, Per pagina QN, Numeri."]:
    ws.append([l])
ws['A1'].font=Font(bold=True,size=13)
wb.save(OUT); print('foglio',OUT)

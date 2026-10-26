# Modello della timeline: quante brevi al giorno per pagina QN, dai risultati del workflow «timeline-quartieri» (ottobre 2026).
# Correzione del troncamento (ultimi 10-15 post per pagina): brevi al giorno = quota di brevi della pagina × post al giorno misurati.
import json,re,sys,math,collections,unicodedata,datetime,statistics
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
J=sys.argv[1]
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
O={it['id']:it for it in json.load(open(f'{S}/timeline/ottobre.json'))}
A={};V={};G=[]
for l in open(J):
    r=json.loads(l)
    if r.get('type')!='result' or not isinstance(r.get('result'),dict): continue
    res=r['result']
    if 'gruppi' in res: G+=res['gruppi']; continue
    for x in res.get('items',[]):
        if 'ok' in x: A.setdefault(x['id'],x)
        elif 'confermata' in x: V[x['id']]=x
GIORNI=25   # 1-25 ottobre
# precisione dal campione verificato, per tipo
camp=[(A[i]['tipo'],v['confermata']) for i,v in V.items() if i in A]
prec_tot=sum(c for _,c in camp)/len(camp) if camp else 1
prec={t:(sum(c for tt,c in camp if tt==t)/n if (n:=sum(1 for tt,_ in camp if tt==t))>=8 else prec_tot) for t in {t for t,_ in camp}}
# doppioni: quota di brevi che sono copie di un'altra
dup_ids=set(); 
for g in G: dup_ids.update(g['ids'][1:])
brevi={i:x for i,x in A.items() if x['ok'] and x['portata']!='fuori Roma o nazionale'}
dup_share=len(dup_ids & set(brevi))/max(1,len(brevi))
# ritmo di pubblicazione per pagina Facebook
RITMO=json.load(open(f'{S}/canali/apify/ritmo_post.json'))
oss=collections.Counter(); okc=collections.defaultdict(list)
for i,it in O.items():
    oss[it['fonte']]+=1
    if i in brevi: okc[it['fonte']].append(i)
def rate(fonte):
    if fonte.startswith('fb:'):
        r=RITMO.get(fonte[3:])
        if r: return max(r[0],oss[fonte]/GIORNI)
    return oss[fonte]/GIORNI
# geografia
g=json.load(open('/home/user/QN/gazetteer/gazetteer.json'))
PZ={z['publication_zone_id']:z for z in g['publication_zones'] if z.get('is_page')}
STOP=set(g['free_text_stoplist'])|set(g['never_substring'])
NAMES=[(norm(z['name_display']),k) for k,z in PZ.items()]
for n in g['neighbourhoods']:
    if n.get('publication_zone_id') in PZ:
        for a in [n['name_display']]+[x.strip() for x in str(n.get('aliases') or '').split(';') if x.strip()]: NAMES.append((norm(a),n['publication_zone_id']))
NAMES=sorted({(a,z) for a,z in NAMES if len(a)>=4 and a not in STOP},key=lambda t:-len(t[0]))
ROM={'i':'I','ii':'II','iii':'III','iv':'IV','v':'V','vi':'VI','vii':'VII','viii':'VIII','ix':'IX','x':'X','xi':'XI','xii':'XII','xiii':'XIII','xiv':'XIV','xv':'XV'}
def dove(x,it):
    t=' '+norm(x['luogo'])+' '; m=it.get('meta') or {}
    zona=next((z for a,z in NAMES if f' {a} ' in t),None)
    mm=re.search(r'municipio ([ivx]+)\b',t); mun=ROM.get(mm.group(1)) if mm else None
    if x['portata']=='quartiere': zona=zona or m.get('zona'); return ('quartiere',zona,(PZ[zona]['primary_municipality'] if zona in PZ else m.get('municipio')))
    if x['portata']=='municipio': return ('municipio',None,mun or (PZ[zona]['primary_municipality'] if zona in PZ else m.get('municipio')))
    return ('citta',None,None)
# brevi al giorno attese, per fonte e per destinazione
Q=collections.Counter(); M=collections.Counter(); C=0.0; per_tipo=collections.Counter(); persi=0.0
for fonte,ids in okc.items():
    n=oss[fonte]; r=rate(fonte)
    for i in ids:
        x=brevi[i]; w=r/n*prec.get(x['tipo'],prec_tot)*(1-dup_share)   # ogni breve osservata vale r/n brevi al giorno
        per_tipo[x['tipo']]+=w
        liv,zona,mun=dove(x,O[i])
        if liv=='quartiere' and zona in PZ: Q[zona]+=w
        elif liv in ('quartiere','municipio') and mun: M[mun]+=w
        elif liv=='citta': C+=w
        else: persi+=w
pages=sorted(PZ)
q=[Q[p] for p in pages]; qm=[Q[p]+M[PZ[p]['primary_municipality']] for p in pages]; qmc=[v+C for v in qm]
# fasce di 2 ore fra le 7 e le 23 (8 fasce), con la distribuzione oraria dei post di ottobre (ora di Roma)
H=collections.Counter()
for it in O.values():
    if it['tipo']=='post Facebook' and it.get('ora_utc'):
        h=(int(it['ora_utc'][:2])+(2 if it['data']<'2026-10-25' else 1))%24; H[h]+=1
tot=sum(H.values()); fasce=[(H[h]+H[h+1])/tot for h in range(7,23,2)]
def copertura(lam): return sum(1-math.exp(-lam*f) for f in fasce)/len(fasce)
def descr(v): v=sorted(v); return {'mediana':round(statistics.median(v),2),'p25':round(v[len(v)//4],2),'p75':round(v[3*len(v)//4],2),'min':round(v[0],2),'max':round(v[-1],2),
                                   'pagine_>=8':sum(1 for x in v if x>=8),'pagine_>=1':sum(1 for x in v if x>=1),'copertura_fasce_mediana':round(copertura(statistics.median(v))*100)}
out={'voci_ottobre':len(O),'classificate':len(A),'brevi':len(brevi),'brevi_per_tipo_osservate':dict(collections.Counter(x['tipo'] for x in brevi.values()).most_common()),
     'brevi_per_portata_osservate':dict(collections.Counter(x['portata'] for x in brevi.values()).most_common()),
     'campione_verificato':len(camp),'precisione':round(prec_tot,3),'precisione_per_tipo':{k:round(v,3) for k,v in prec.items()},'quota_doppioni':round(dup_share,3),
     'brevi_al_giorno_citta_intera':round(sum(per_tipo.values()),1),'per_tipo_al_giorno':{k:round(v,1) for k,v in per_tipo.most_common()},
     'citta_al_giorno':round(C,2),'municipio_al_giorno':{k:round(v,2) for k,v in sorted(M.items())},'senza_destinazione_al_giorno':round(persi,2),
     'solo_quartiere':descr(q),'quartiere_piu_municipio':descr(qm),'quartiere_municipio_citta':descr(qmc),'fasce_2h_quota_post':[round(f,3) for f in fasce],
     'per_pagina':{PZ[p]['name_display']:{'quartiere':round(Q[p],2),'municipio':round(M[PZ[p]['primary_municipality']],2),'citta':round(C,2)} for p in pages}}
json.dump(out,open(f'{S}/timeline/modello.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='per_pagina'},ensure_ascii=False,indent=1))
# ---- foglio per Drive ----
import openpyxl
from openpyxl.styles import Font,PatternFill,Alignment
OUT=sys.argv[2] if len(sys.argv)>2 else None
if OUT:
    wb=openpyxl.Workbook(); BF=Font(bold=True); HF=PatternFill('solid',fgColor='DDEBF7')
    def head(ws,h,w):
        ws.append(h)
        for c in ws[1]: c.font=BF; c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='top')
        for i,x in enumerate(w,1): ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width=x
        ws.freeze_panes='A2'
    ws=wb.active; ws.title='Brevi di ottobre'
    head(ws,['data','titolo (parole nostre)','tipo','portata','luogo','validità','verifica a campione','fonte','canale','link','id'],[11,60,22,12,30,12,14,36,16,50,9])
    for i,x in sorted(brevi.items(),key=lambda kv:(O[kv[0]]['data'],kv[0]),reverse=True):
        it=O[i]; v=V.get(i)
        ws.append([it['data'],x['titolo'],x['tipo'],x['portata'],x['luogo'],x['validita'],('confermata' if v['confermata'] else 'non regge') if v else None,it['nome_fonte'],it['tipo'],it.get('url') or it.get('feed'),i])
    ws=wb.create_sheet('Per pagina QN')
    head(ws,['pagina QN','municipio','brevi al giorno: quartiere','+ municipio','+ città','totale','una ogni (ore di giornata 7-23)'],[24,9,14,12,10,10,16])
    for p in pages:
        q,m_=Q[p],M[PZ[p]['primary_municipality']]; t=q+m_+C
        ws.append([PZ[p]['name_display'],PZ[p]['primary_municipality'],round(q,2),round(m_,2),round(C,2),round(t,2),round(16/(q+m_),1) if q+m_ else None])
    wb.save(OUT); print('foglio',OUT)

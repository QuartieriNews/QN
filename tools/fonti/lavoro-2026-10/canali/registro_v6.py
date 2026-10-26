# Registro fonti v6: le righe del v5 restano com'erano (decisioni dell'owner intatte, DEC-024); ogni riga di un promotore
# riceve la regola «dove cercare» provata; i promotori con eventi ma senza voce nello schedario entrano come candidati
# (origine promotori_eventi_2026-10-26). Poi promotori.json per la wiki riceve la regola e l'id delle voci nuove.
import json,re,collections,unicodedata,openpyxl,shutil
from openpyxl.styles import Font,PatternFill,Alignment
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
R=json.load(open(f'{S}/canali/regola_promotori.json'))
P=json.load(open(f'{S}/promotori/promotori_finale.json'))
assert [r['key'] for r in R]==[p['key'] for p in P]
def norm(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower()).strip()
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#:]+)',str(u or '').strip().lower()); return m.group(1) if m else None
def fbk(u):
    m=re.search(r'facebook\.com/(?:profile\.php\?id=(\d+)|(?:pg/)?([^/?#]+))',str(u or ''),re.I)
    return (m.group(1) or m.group(2)).lower() if m else None
wb=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v5.xlsx')   # sempre dal v5: il v6 non si rigenera da sé stesso
ws=wb[wb.sheetnames[0]]
H=[c.value for c in ws[1]]; col={h:i for i,h in enumerate(H)}
NUOVE=['eventi_promotore_ott_2026','canale_da_leggere','prova_canale','pagina_da_leggere','controllo']
for h in NUOVE:
    ws.cell(row=1,column=len(H)+1,value=h); H.append(h); col[h]=len(H)-1
rows=list(ws.iter_rows(min_row=2))
by_key={};by_fb={};by_host={};by_name={}
for r in rows:
    v=lambda k:r[col[k]].value
    by_key[str(v('chiave'))]=r
    if fbk(v('facebook')): by_fb.setdefault(fbk(v('facebook')),r)
    if host(v('link')) and v('canale')=='sito': by_host.setdefault(host(v('link')),r)
    by_name.setdefault(norm(v('nome')),r)
def fill(r,x,p):
    r[col['eventi_promotore_ott_2026']].value=p['n_eventi']
    r[col['canale_da_leggere']].value=x['canale']; r[col['prova_canale']].value=x['prova']
    r[col['pagina_da_leggere']].value=x['pagina']; r[col['controllo']].value=x['controllo']
# voci già nello schedario (nome, alias, pagina Facebook): un promotore che ci sta già prende quell'id e non diventa una
# riga nuova del registro, che per nome si fonderebbe con la voce e farebbe scorrere la numerazione S-EV
import sys; sys.path.insert(0,'/home/user/QN/tools/wiki'); import build_fonti_eventi as bfe   # la stessa chiave di nome del build
OLD=json.load(open('/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad/canali/fonti_eventi_HEAD.json'))['fonti']
old_by={}
for e in OLD:
    for n in [e['nome']]+e.get('alias',[]): old_by.setdefault(('n',bfe.norm(n)),e['id'])
    for k in e.get('chiavi',[]):
        if k.startswith('fb-page:'): old_by.setdefault(('f',k[8:]),e['id'])
st=collections.Counter(); nuovi=[]; ids={}
for x,p in zip(R,P):
    w=p.get('wiki') or ''
    r=by_key.get(w[2:]) if w.startswith('S-') else None
    how='chiave' if r else None
    if not r and fbk(p.get('facebook')) in by_fb: r=by_fb[fbk(p['facebook'])]; how='facebook'
    if not r and host(p.get('sito')) in by_host: r=by_host[host(p['sito'])]; how='sito'
    if not r and norm(p['nome']) in by_name: r=by_name[norm(p['nome'])]; how='nome'
    if r:
        fill(r,x,p); st['nel registro: '+how]+=1
        if not w: ids[p['key']]='S-'+str(r[col['chiave']].value)
    elif w: st['solo nello schedario (censimento o eventi)']+=1
    elif old_by.get(('n',bfe.norm(p['nome']))) or old_by.get(('f',fbk(p.get('facebook')) or '')):
        ids[p['key']]=old_by.get(('n',bfe.norm(p['nome']))) or old_by[('f',fbk(p['facebook']))]; st['già nello schedario, id ritrovato']+=1
    elif not bfe.norm(p['nome']) or bfe.norm(p['nome']) in ('roma','n d','nd'): st['nome non utilizzabile come voce']+=1
    else: nuovi.append((x,p))
st['nuovi candidati']=len(nuovi)
CAN={'feed del sito':'sito','calendario del sito (schema.org)':'sito','pagina eventi del sito':'sito','notizie del sito (RSS)':'sito','agenda Biblioteche di Roma':'sito',
     'culture.roma.it':'sito','eventi Facebook':'facebook','post Facebook':'facebook','Instagram (non letto)':'da_trovare','solo aggregatore':'da_trovare','nessun canale':'da_trovare'}
nuovi.sort(key=lambda t:(norm(t[1]['nome']),t[1]['key']))
uniq={}
for x,p in nuovi: uniq.setdefault(bfe.norm(p['nome']),[]).append((x,p))
doppi={p['key']:grp[0][1]['key'] for grp in uniq.values() for x,p in grp[1:]}
nuovi=[grp[0] for grp in uniq.values()]
fill_new=PatternFill('solid',fgColor='FFF2CC')
for i,(x,p) in enumerate(nuovi,1):
    k=f'PR-{i:04d}'; ids[p['key']]='S-'+k
    vals={'chiave':k,'decisione':'candidata','nome':p['nome'],'tipo':p.get('tipo_registro') or p.get('tipo_wiki'),'zona_qn':p.get('zona_sede'),'municipio':p.get('municipio_sede'),
          'canale':'sito' if CAN[x['canale']]=='sito' and p.get('sito') else CAN[x['canale']],'link':p.get('sito'),'facebook':p.get('facebook'),'instagram':p.get('instagram'),
          'origine':'promotori_eventi_2026-10-26','eventi_visti':p['n_eventi'],'motivo':f"promotore di {p['n_eventi']} eventi della pagina (ottobre 2026) senza voce nello schedario",
          'dove_cercare':x['pagina'],'fonte_dati':'promotori_eventi.xlsx, prova del canale 26 ott 2026'}
    row=[None]*len(H)
    for h,v in vals.items(): row[col[h]]=v
    ws.append(row)
    r=list(ws.iter_rows(min_row=ws.max_row,max_row=ws.max_row))[0]
    fill(r,x,p)
    for c in r: c.fill=fill_new
for c in ws[1]: c.font=Font(bold=True)
ws3=wb.create_sheet('Leggimi v6')   # in fondo: il build legge il primo foglio
for l in ["Registro fonti v6 (26 ottobre 2026)","",
          "Le righe del v5 sono invariate: decisione, canale e note dell'owner non sono toccati (DEC-024).",
          "Colonne nuove in fondo: eventi del promotore a ottobre, canale da leggere, prova, pagina da leggere, controllo.",
          f"Righe nuove (in giallo, chiave PR-…): {len(nuovi)} promotori con eventi ma senza voce nello schedario, decisione «candidata»: tenere o scartare resta all'owner.",
          "L'elenco completo dei 1.246 promotori con la regola e i costi sta in promotori_dove_cercare_2026-10-26.xlsx. Ordine dei canali per costo: feed del sito, calendario schema.org, pagina eventi del sito, notizie del sito (RSS), agende già lette (culture.roma.it, Biblioteche di Roma), eventi Facebook, post Facebook.",
          "Prova: storico = eventi già arrivati da quel canale a ottobre; confermato = la prova del 26 ottobre ha ritrovato sul sito eventi noti (titolo e data vicini); probabile = il sito pubblica date future ma nessuno degli eventi noti; solo pagina = pagina Facebook senza eventi letti finora.",
          "Controllo: canale da guardare a cadenza più lenta quando quello gratuito non porta tutti gli eventi del promotore."]:
    ws3.append([l])
ws3.column_dimensions['A'].width=160; ws3['A1'].font=Font(bold=True,size=13)
wb.save('/mnt/user-data/outputs/registro_fonti_v6.xlsx'); wb.save(f'{S}/canali/registro_fonti_v6.xlsx')
for k,k0 in doppi.items(): ids[k]=ids[k0]
st['nuovi candidati']=len(nuovi); st['stesso nome di un nuovo candidato']=len(doppi)
print(dict(st))
# promotori.json per la wiki: regola e id delle voci nuove
Wp=json.load(open(f'{S}/wiki_in_v5_bak/promotori.json'))   # promotori.json del 26 ottobre prima della regola
assert [w['nome'] for w in Wp]==[p['nome'] for p in P]
for w,x,p in zip(Wp,R,P):
    w['dove_cercare']={'canale':x['canale'],'prova':x['prova'] if x['prova']!='—' else None,'pagina':x['pagina'],'controllo':x['controllo']}
    if not w['id'] and ids.get(p['key']): w['id']=ids[p['key']]
json.dump(Wp,open(f'{S}/canali/promotori_wiki.json','w'),ensure_ascii=False,indent=0)
print('id nuovi o ritrovati',len(ids))

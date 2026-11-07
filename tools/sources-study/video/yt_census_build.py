# Builds the June 2026 video census (A4 YouTube) and cross-references Atti Web verbali (MMV) / convocazioni (MMC).
import csv, json, re, html, os, glob, datetime as dt
from collections import Counter, defaultdict
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s or ''))).strip()
def mun_of(s):
    m=re.search(r'MUNIC(?:IPIO)?\.?\s*([IVX]+)', s or ''); return m.group(1) if m else ''
MESI={'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12}
def dates_in(s):
    """all dd/mm/yyyy-like and 'd mese yyyy' dates in a string -> set of iso dates"""
    out=set(); s=(s or '').lower()
    for m in re.finditer(r'(\d{1,2})[\s\.\-/_]+(\d{1,2})[\s\.\-/_]+(20\d{2}|\d{2})\b', s):
        d,mo,y=int(m.group(1)),int(m.group(2)),int(m.group(3)); y=y+2000 if y<100 else y
        try: out.add(dt.date(y,mo,d).isoformat())
        except: pass
    for m in re.finditer(r'(\d{1,2})[°ºo]?\s*(?:di\s+)?([a-z]{3,9})\.?\s*(20\d{2})?', s):
        if m.group(2) in MESI:
            y=int(m.group(3)) if m.group(3) else 2026
            try: out.add(dt.date(y,MESI[m.group(2)],int(m.group(1))).isoformat())
            except: pass
    return out
# --- Atti Web
A2='../A2_tip/'
mmv=json.load(open(A2+'MMV_full_0.json'))['elencoAtti']
mmc=json.load(open(A2+'MMC_full_0.json'))['elencoAtti']+json.load(open(A2+'MMC_full_500.json'))['elencoAtti']
cmv=json.load(open(A2+'CMV.json')).get('elencoAtti') or []
cmc=json.load(open(A2+'CMC.json')).get('elencoAtti') or []
def norm_rows(rows, kind):
    out=[]
    for r in rows:
        org=clean(r.get('dscStrOrg')); M=mun_of(org)
        sed=set()
        m=re.search(r'Seduta del (\d{2}/\d{2}/\d{4})', org)
        if m: sed|=dates_in(m.group(1))
        sed|=dates_in(clean(r.get('oggetto')))|dates_in(r.get('nomeFile'))
        out.append(dict(kind=kind, mun=M, org=org, sedute=sed, dtRpr=r.get('dtRpr'), dtPtg=r.get('dtPtg'), idDoc=r.get('idDoc'), oggetto=clean(r.get('oggetto'))[:160], url='https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/'+(r.get('urlFile') or '')))
    return out
atti=norm_rows(mmv,'MMV')+norm_rows(mmc,'MMC')+norm_rows(cmv,'CMV')+norm_rows(cmc,'CMC')
# --- verbali with embedded YouTube links (Municipi I and V, all June MMV PDFs read)
LINKMAP={}
VERB_INDEX=[]
if os.path.exists('verbali_all/MMV_I_V_index.csv'):
    for v in csv.DictReader(open('verbali_all/MMV_I_V_index.csv')):
        VERB_INDEX.append(v)
        for l in (v['link_youtube'] or '').split(';'):
            if l: LINKMAP[l]=v
# --- publication dates from the channels' RSS feeds (last 15 videos per channel, read 15 September)
RSSDATES={}
if os.path.exists('drive_out/A4_rss_ritardo_pubblicazione_2026-09-15.csv'):
    for v in csv.DictReader(open('drive_out/A4_rss_ritardo_pubblicazione_2026-09-15.csv')):
        RSSDATES[v['id']]=v['data_pubblicazione']
# --- videos
CH={'I':('Municipio I','UCEZtd0d0UV5e8ZCWkNOiNjw'),'V':('Municipio V','UCBuQMoXjwR8re80z3YdcCQQ'),'IX':('Municipio IX','UC6F3Fj68gnOeC1yXU2JOQEA'),'RC':('Roma Capitale','UCCQygqTutREYU9AbTHfHhTw'),'XIV':('Municipio XIV','UC_XtcIeCkpWjt3U5t_k7QVw')}
cands=list(csv.DictReader(open('yt_june_candidates.tsv'),delimiter='\t'))
rows=[]
def organo(t):
    tl=t.lower()
    if 'assemblea capitolina' in tl: return 'Assemblea Capitolina'
    if 'consiglio' in tl: return 'Consiglio municipale'
    if 'comm' in tl or 'congiunta' in tl: return 'Commissione municipale'
    return 'altro'
def keywords(t):
    tl=t.lower(); tl=re.sub(r'\b(comm\.?ne|commissione|congiunta|cong\.ta|comm\.|del|dell|il|di|e|la|le|del|al|-|–|municipio|registrazione|parte|i|ii|iii|iv|v|vi|vii|verbale|convocazione|seduta|giugno|maggio|luglio|della|delle|degli|con|per|sulla|ordine|giorno|lavori|ore|alle)\b',' ',tl)
    tl=re.sub(r'[\d/\.\-:]+',' ',tl); return set(w for w in re.findall(r'[a-zàèéìòù]{4,}',tl))
for c in cands:
    vid=c['id']; meta={}
    f=f'meta/{vid}.json'
    if os.path.exists(f):
        try: meta=json.load(open(f)) or {}
        except: meta={}
    title=c['title'] or ''
    sed=c['title_date'] if c['title_date'].startswith('2026-') and '?' not in c['title_date'] else ''
    up=meta.get('upload_date'); up_iso=f'{up[:4]}-{up[4:6]}-{up[6:]}' if up else ''
    if not up_iso and vid in RSSDATES: up_iso=RSSDATES[vid]
    dur=meta.get('duration') or (int(c['duration']) if c['duration'] else None)
    ac=meta.get('automatic_captions') or {}; subs=meta.get('subtitles') or {}
    auto_it='sì' if any(k.startswith('it') for k in ac) else ('no' if meta.get('duration') else 'n.d.')
    man_sub=','.join(subs.keys()) if subs else ('no' if meta.get('duration') else 'n.d.')
    desc=(meta.get('description') or '').strip().replace('\n',' ')
    M=c['ch'] if c['ch']!='RC' else ''
    org=organo(title)
    # cross-reference atti: same Municipio, session date in the act; then keyword overlap on commission name
    links=[]
    kw=keywords(title)
    if M and sed:
        for a in atti:
            if a['mun']==M and sed in a['sedute']:
                ov=len(kw & keywords(a['org']+' '+a['oggetto']))
                links.append((a['kind'],ov,a))
    verb=[l for l in links if l[0] in ('MMV','CMV')]; conv=[l for l in links if l[0] in ('MMC','CMC')]
    # exact match by YouTube link embedded in the verbale (Municipio I embeds it in every June verbale)
    lk=LINKMAP.get(vid)
    if lk: verb=[('MMV',99,dict(kind='MMV',url=lk['url'],oggetto=lk['oggetto'],mun=M))]+[l for l in verb if l[2].get('url')!=lk['url']]
    elif M=='I': verb=[(k,0,a) for (k,ov,a) in verb]  # every June verbale of Municipio I links its video: no link = no June verbale for this recording
    def best(ls):
        ls=sorted(ls,key=lambda x:-x[1]); return ls[0] if ls else None
    bv=best(verb); bc=best(conv)
    lead=None
    if up_iso and sed:
        lead=(dt.date.fromisoformat(up_iso)-dt.date.fromisoformat(sed)).days
    rows.append(dict(fonte='A4 YouTube '+CH.get(c['ch'],(c['ch'],''))[0], canale=CH.get(c['ch'],(c['ch'],''))[1], tab=c['tab'], id=vid, url='https://www.youtube.com/watch?v='+vid,
        organo=org, data_seduta=sed, data_pubblicazione=up_iso, ritardo_gg=lead if lead is not None else '', durata_s=dur, durata_hm=(f'{dur//3600}:{(dur%3600)//60:02d}' if dur else ''),
        territorio=('Municipio '+M) if M else 'Roma Capitale (città)', audio='sì' if dur else 'n.d.', sottotitoli_manuali=man_sub, trascrizione_auto_it=auto_it,
        n_verbali_stessa_data=len(verb), verbale_match=(bv[2]['url'] if bv and bv[1]>0 else ''), verbale_match_tipo=('link nel verbale' if (bv and bv[1]==99) else ('data e nome' if (bv and bv[1]>0) else ('solo data' if verb else ''))),
        n_convocazioni_stessa_data=len(conv), convocazione_match=(bc[2]['url'] if bc and bc[1]>0 else ''),
        meta_ok='sì' if meta.get('duration') else 'no', live=meta.get('live_status') or ''))
# titolo, descrizione e oggetti dei verbali non si esportano (HANDOFF §2-bis, DEC-104): servono solo all'abbinamento
rows.sort(key=lambda r:(r['territorio'],r['data_seduta'],r['id']))
with open('deliver_video/A4_youtube_giugno2026_censimento.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# summary
S={}
S['n_registrazioni']=len(rows)
S['per_territorio']=dict(Counter(r['territorio'] for r in rows))
S['per_organo']=dict(Counter((r['territorio'],r['organo']) for r in rows).items().__iter__()) if False else {f"{k[0]} / {k[1]}":v for k,v in Counter((r['territorio'],r['organo']) for r in rows).items()}
S['meta_ok']=sum(1 for r in rows if r['meta_ok']=='sì')
S['auto_it_si']=sum(1 for r in rows if r['trascrizione_auto_it']=='sì'); S['auto_it_no']=sum(1 for r in rows if r['trascrizione_auto_it']=='no')
S['sottotitoli_manuali']=sum(1 for r in rows if r['sottotitoli_manuali'] not in ('no','n.d.'))
S['con_data_seduta']=sum(1 for r in rows if r['data_seduta']); S['con_data_pubblicazione']=sum(1 for r in rows if r['data_pubblicazione'])
S['pubblicati_in_giugno']=sum(1 for r in rows if r['data_pubblicazione'].startswith('2026-06')); S['pubblicati_dopo_giugno']=sum(1 for r in rows if r['data_pubblicazione'] and r['data_pubblicazione']>'2026-06-30')
leads=[r['ritardo_gg'] for r in rows if r['ritardo_gg']!='']
if leads:
    ls=sorted(leads); S['ritardo_pubblicazione_gg']={'n':len(ls),'min':ls[0],'mediana':ls[len(ls)//2],'max':ls[-1],'entro_1gg':sum(1 for x in ls if x<=1),'entro_7gg':sum(1 for x in ls if x<=7)}
comm=[r for r in rows if r['organo']=='Commissione municipale']
S['commissioni_municipali']={'n':len(comm),'con_verbale_stessa_data_e_nome':sum(1 for r in comm if r['verbale_match']),'con_verbale_stessa_data_qualsiasi':sum(1 for r in comm if r['n_verbali_stessa_data']),'con_convocazione_match':sum(1 for r in comm if r['convocazione_match']),'con_convocazione_stessa_data':sum(1 for r in comm if r['n_convocazioni_stessa_data'])}
durs=[r['durata_s'] for r in rows if r['durata_s']]
S['durata']={'n':len(durs),'ore_totali':round(sum(durs)/3600,1),'mediana_min':round(sorted(durs)[len(durs)//2]/60),'min_min':round(min(durs)/60),'max_min':round(max(durs)/60)}
S['durata_commissioni_municipali']={'n':len([r for r in comm if r['durata_s']]),'ore_totali':round(sum(r['durata_s'] for r in comm if r['durata_s'])/3600,1)}
# verbali (MMV) of June per Municipio vs videos: coverage of acts by video for I, V, IX
byM=defaultdict(set)
for a in atti:
    if a['kind']=='MMV' and a['mun'] in ('I','V','IX'):
        for s in a['sedute']:
            if s.startswith('2026-06'): byM[a['mun']].add(s)
vidM=defaultdict(set)
for r in comm:
    if r['data_seduta']: vidM[r['territorio'].replace('Municipio ','')].add(r['data_seduta'])
S['giorni_seduta_giugno']={M:{'giorni_con_verbale_MMV':len(byM[M]),'giorni_con_video':len(vidM[M]),'giorni_video_senza_verbale':len(vidM[M]-byM[M]),'giorni_verbale_senza_video':len(byM[M]-vidM[M])} for M in ('I','V','IX')}
S['verbali_con_link_youtube']={'I':sum(1 for v in VERB_INDEX if v['municipio']=='I' and v['link_youtube']),'I_totale':sum(1 for v in VERB_INDEX if v['municipio']=='I'),'V':sum(1 for v in VERB_INDEX if v['municipio']=='V' and v['link_youtube']),'V_totale':sum(1 for v in VERB_INDEX if v['municipio']=='V')}
ids=set(r['id'] for r in rows)
S['link_verbali_I_verso_video_censiti']=sum(1 for l in LINKMAP if l in ids); S['link_verbali_I_verso_video_non_censiti']=sorted(l for l in LINKMAP if l not in ids)
S['match_verbale_per_tipo']=dict(Counter(r['verbale_match_tipo'] for r in comm))
json.dump(S,open('deliver_video/summary_A4_youtube.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False,indent=1))

import json, glob, csv, re, datetime as dt, random, os, requests
from collections import Counter, defaultdict
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
def dur_s(s):
    if not s: return None
    m=re.match(r'(\d+):(\d+):(\d+)', s); 
    return int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3)) if m else None
def organo(title, ctype, gb):
    if gb: return gb
    t=title.lower()
    if 'consiglio' in t or 'seduta' in t and 'commiss' not in t: return 'Consiglio municipale'
    if 'commiss' in t or 'comm.' in t or 'comm ' in t or 'congiunt' in t: return 'Commissione municipale'
    return 'altro'
rows=[]
for f in sorted(glob.glob('rtv/cat/*.json')):
    cat=os.path.basename(f)[:-5].replace('_',' ')
    for it in json.load(open(f)):
        rd=it.get('referenceDate') or ''; ins=it.get('insertDate') or ''
        if rd[:7]!='2026-06' and ins[:7]!='2026-06': continue
        tracks=it.get('tracks') or []
        vtt=next((t.get('speechToTextTrackWebVtt') for t in tracks if t.get('trackType')=='SpeechToTextTrack' and t.get('speechToTextTrackWebVtt')),'')
        d=dur_s(it.get('duration'))
        sed=rd[:10]; pub=ins[:10]
        lead=(dt.date.fromisoformat(pub)-dt.date.fromisoformat(sed)).days if sed and pub else ''
        ctype=it.get('contentType')
        route='commission' if ctype=='Commission' else 'vod'
        rows.append(dict(fonte='A3 RomaTV', territorio=cat, tipo=ctype, organo=organo(it.get('title') or '', ctype, it.get('governmentBody')), titolo=(it.get('title') or '').strip(), descrizione=(it.get('description') or '').strip()[:200], data_seduta=sed, ora_seduta=rd[11:16], data_pubblicazione=pub, ritardo_gg=lead, durata_s=d, durata_hm=(f'{d//3600}:{(d%3600)//60:02d}' if d is not None else ''), guid=it.get('guid'), url=f"https://streaming.comune.roma.it/portal/watch/{route}/{it.get('guid')}", trascrizione_piattaforma='sì' if vtt else 'no', vtt_url=vtt, in_giugno_per='seduta' if rd[:7]=='2026-06' else 'pubblicazione'))
rows.sort(key=lambda r:(r['territorio'],r['data_seduta'],r['ora_seduta'],r['titolo']))
os.makedirs('deliver_video',exist_ok=True)
with open('deliver_video/A3_romatv_giugno2026_censimento.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
june=[r for r in rows if r['in_giugno_per']=='seduta']
S={'n_giugno_per_seduta':len(june),'n_pubblicati_giugno_su_sedute_di_altri_mesi':sum(1 for r in rows if r['in_giugno_per']=='pubblicazione')}
S['per_territorio']={k:{'registrazioni':v,'ore':round(sum(r['durata_s'] or 0 for r in june if r['territorio']==k)/3600,1),'con_trascrizione':sum(1 for r in june if r['territorio']==k and r['trascrizione_piattaforma']=='sì'),'giorni_di_seduta':len(set(r['data_seduta'] for r in june if r['territorio']==k))} for k,v in sorted(Counter(r['territorio'] for r in june).items())}
S['per_tipo']=dict(Counter(r['tipo'] for r in june)); S['per_organo_municipi']=dict(Counter(r['organo'] for r in june if r['territorio'].startswith('Municipio')))
S['ore_totali']=round(sum(r['durata_s'] or 0 for r in june)/3600,1); S['con_trascrizione']=sum(1 for r in june if r['trascrizione_piattaforma']=='sì')
leads=sorted(r['ritardo_gg'] for r in june if r['ritardo_gg']!='')
S['ritardo_pubblicazione_gg']={'n':len(leads),'min':leads[0],'mediana':leads[len(leads)//2],'max':leads[-1],'entro_1gg':sum(1 for x in leads if x<=1),'entro_7gg':sum(1 for x in leads if x<=7)} if leads else None
S['commissioni_capitoline_per_organo']=dict(Counter(r['organo'] for r in june if r['territorio']=='Commissioni Capitoline').most_common())
durs=[r['durata_s'] for r in june if r['durata_s']]
S['durata']={'n':len(durs),'mediana_min':round(sorted(durs)[len(durs)//2]/60),'min_min':round(min(durs)/60),'max_min':round(max(durs)/60),'fino_a_5_min':sum(1 for x in durs if x<=300)}
json.dump(S,open('deliver_video/summary_A3_romatv.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False,indent=1))
# --- sample: one recording with platform transcript per Municipio not on YouTube, commissions preferred, 15-120 min
random.seed('2026-06-A3')
sel=[]
for M in ['Municipio II','Municipio III','Municipio VIII','Municipio X','Municipio XI','Municipio XII','Municipio XV']:
    pool=[r for r in june if r['territorio']==M and r['trascrizione_piattaforma']=='sì' and r['durata_s'] and 900<=r['durata_s']<=7200]
    pref=[r for r in pool if r['organo']=='Commissione municipale'] or pool
    if pref: sel.append(random.choice(pref))
print('== campione A3')
for r in sel: print(r['territorio'], r['data_seduta'], r['durata_hm'], r['organo'], '|', r['titolo'][:70], '|', r['guid'])
with open('deliver_video/A3_campione_selezione.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['territorio','data_seduta','organo','titolo','durata_hm','url','vtt_url']); w.writeheader()
    for r in sel: w.writerow({k:r[k] for k in ['territorio','data_seduta','organo','titolo','durata_hm','url','vtt_url']})
os.makedirs('rtv/vtt',exist_ok=True)
for r in sel:
    f=f"rtv/vtt/{r['guid']}.vtt"
    if not os.path.exists(f):
        x=requests.get(r['vtt_url'],timeout=120); open(f,'wb').write(x.content); print('VTT', r['guid'], x.status_code, len(x.content))

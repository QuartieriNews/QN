# Costo mensile della lettura degli eventi per canale, dalla regola per promotore (assegna.py) e dai prezzi misurati
# sul piano Apify dell'account (fascia BRONZE, 26 ottobre 2026) e sui ritmi misurati nelle esecuzioni di ottobre.
import json,re,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
R=json.load(open(f'{S}/canali/regola_promotori.json'))
RITMO=json.load(open(f'{S}/canali/apify/ritmo_post.json'))
PREZZO={'post':0.004+0.001,'avvio':0.001,'evento_fb':0.003}   # post + filtro data; avvio di un'esecuzione; evento futuro restituito
EV_PER_LETTURA=0.089      # eventi futuri per pagina a ogni lettura (4.813 letture di pagine, 24-25 ottobre)
POST_MEDIA=0.088          # post al giorno per pagina, media su 4.016 pagine (24-25 ottobre)
GIORNI=30; LETTURE={'ogni giorno':30,'ogni settimana':30/7,'ogni mese':1}
def slug(u):
    m=re.search(r'facebook\.com/(?:profile\.php\?id=(\d+)|(?:pg/)?([^/?#]+))',str(u or ''),re.I)
    return (m.group(1) or m.group(2)).lower() if m else None
def ritmo(u):
    r=RITMO.get(slug(u)); return (r[0],True) if r else (POST_MEDIA,False)
FB=('eventi Facebook','post Facebook')
def costo(scenario,cadenza):
    """dollari al mese; scenario: 'tutto Facebook' | 'regola' | 'regola + probabili'"""
    n_ev=n_post=0; usd_ev=usd_post=0.0; misurati=0; ctrl_post=ctrl_ev=0; usd_ctrl=0.0
    for p in R:
        if not p['facebook']: continue
        ch=p['canali_eventi']
        suo=['post Facebook'] if ch.get('fb_post',0)>ch.get('fb_eventi',0) else ['eventi Facebook']   # il canale Facebook da cui sono arrivati i suoi eventi
        if scenario=='tutto Facebook': canali=['eventi Facebook','post Facebook']
        else:
            libero=p['canale'] not in FB+('Instagram (non letto)','solo aggregatore','nessun canale') and (scenario=='regola + probabili' or p['prova']!='probabile')
            canali=[] if libero else ([p['canale']] if p['canale'] in FB else suo)
        for c in canali:
            if c=='eventi Facebook': n_ev+=1; usd_ev+=EV_PER_LETTURA*PREZZO['evento_fb']*LETTURE[cadenza]
            else:
                r,ok=ritmo(p['facebook']); misurati+=ok; n_post+=1; usd_post+=r*GIORNI*PREZZO['post']
        # controllo: eventi Facebook una volta al mese per chi ha un canale gratuito che non porta tutto
        if scenario!='tutto Facebook' and not canali and p['controllo']:   # i post si pagano a post: il controllo sui post costa come la lettura quotidiana
            if p['controllo']=='post Facebook': ctrl_post+=1; usd_ctrl+=ritmo(p['facebook'])[0]*GIORNI*PREZZO['post']
            else: ctrl_ev+=1; usd_ctrl+=EV_PER_LETTURA*PREZZO['evento_fb']*LETTURE['ogni mese']
    avvii=2*LETTURE[cadenza]*PREZZO['avvio']
    return {'pagine_eventi':n_ev,'pagine_post':n_post,'post_ritmo_misurato':misurati,'usd_eventi':round(usd_ev,2),'usd_post':round(usd_post,2),'usd_avvii':round(avvii,2),
            'controllo_pagine_post':ctrl_post,'controllo_pagine_eventi':ctrl_ev,'usd_controllo':round(usd_ctrl,2),'usd_totale':round(usd_ev+usd_post+avvii+usd_ctrl,2)}
out={}
for sc in ('tutto Facebook','regola','regola + probabili'):
    for cad in ('ogni giorno','ogni settimana'):
        out[f'{sc} · {cad}']=costo(sc,cad); print(sc,'·',cad,out[f'{sc} · {cad}'])
# quanto costa ogni canale per promotore (ogni giorno)
per=collections.defaultdict(lambda:[0,0.0])
for p in R:
    c=p['canale']; k=(c,p['prova'])
    per[k][0]+=1
    if c=='eventi Facebook' and p['facebook']: per[k][1]+=EV_PER_LETTURA*PREZZO['evento_fb']*30+ritmo(p['facebook'])[0]*30*PREZZO['post']
    if c=='post Facebook' and p['facebook']: per[k][1]+=ritmo(p['facebook'])[0]*30*PREZZO['post']+EV_PER_LETTURA*PREZZO['evento_fb']*30
json.dump({'prezzi':PREZZO,'eventi_per_lettura':EV_PER_LETTURA,'post_media':POST_MEDIA,'scenari':out,'per_canale':{f'{a} · {b}':[n,round(u,2)] for (a,b),(n,u) in per.items()}},open(f'{S}/canali/costi.json','w'),ensure_ascii=False,indent=1)

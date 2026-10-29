# Riepilogo: chi vieta la diffusione dei propri contenuti, quanti eventi del calendario ne dipendono
import json,collections,sys
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'; sys.path.insert(0,P)
import diritti as D
R=json.load(open(f'{P}/promotori_finale.json')); E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
SL=json.load(open(f'{P}/siti_letti.json'))
ev_lab=collections.Counter()
seen=collections.defaultdict(set)
for r in R:
    for i in r['eventi_idx']: seen[i].add(r['diffusione'])
ORDER=['riproduzione vietata','raccolta automatica vietata','licenza richiesta','termini della piattaforma','diritti riservati (generico)','licenza aperta','nessuna indicazione','non verificabile']
for i in range(len(E)):
    labs=seen.get(i) or {'senza promotore'}
    ev_lab[min(labs,key=lambda l:ORDER.index(l) if l in ORDER else 99)]+=1
src=collections.Counter(e['src'] for e in E)
# il canale da cui leggiamo l'evento ha una sua posizione, indipendente dal promotore
def canale(e):
    if e['src'] in ('Facebook','Facebook (post)'): return 'Facebook (termini di Meta)',D.MANUALE['facebook.com'][0]
    if e['src']=='Roma Today': return 'Roma Today (Citynews)',D.MANUALE['romatoday.it'][0]
    if e['src']=='culture.roma.it': return 'culture.roma.it (Roma Capitale)',D.MANUALE['culture.roma.it'][0]
    h=(e.get('url') or '').split('/')[2] if '://' in str(e.get('url')) else None
    if h and 'bibliotechediroma.it' in h: return 'Biblioteche di Roma',D.MANUALE['bibliotechediroma.it'][0]
    sr=next((x for x in SL if h and x['host'] in (h,h.replace('www.',''),'www.'+h)),None)
    return 'siti delle fonti',(D.position(sr)[0] if sr else 'non verificabile')
ch=collections.Counter(canale(e) for e in E)
out={'promotori_per_posizione':dict(collections.Counter(r['diffusione'] for r in R).most_common()),
     'eventi_per_posizione_piu_restrittiva':dict(ev_lab.most_common()),
     'siti_per_posizione':dict(collections.Counter(D.position(s)[0] for s in SL).most_common()),
     'siti_robots_vieta_tutto':sum(1 for s in SL if s.get('vieta_tutto')),'siti_che_bloccano_bot_IA':sum(1 for s in SL if s.get('bot_ia_bloccati')),
     'eventi_da_facebook':src.get('Facebook',0)+src.get('Facebook (post)',0),'eventi_totali':len(E),'eventi_per_canale':[[c,p,n] for (c,p),n in ch.most_common()],
     'promotori_riproduzione_vietata':[(r['nome'],r['n_eventi'],r['diffusione_prova']) for r in sorted(R,key=lambda r:-r['n_eventi']) if r['diffusione']=='riproduzione vietata'],
     'promotori_raccolta_vietata':[(r['nome'],r['n_eventi'],r['diffusione_prova']) for r in sorted(R,key=lambda r:-r['n_eventi']) if r['diffusione']=='raccolta automatica vietata'],
     'promotori_licenza_aperta':[(r['nome'],r['n_eventi']) for r in R if r['diffusione']=='licenza aperta']}
json.dump(out,open(f'{P}/diffusione_riepilogo.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False,indent=1)[:4000])

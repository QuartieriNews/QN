# Analisi dell'audit di qualità: tassi per strato con intervallo di Wilson al 95%, accordo fra i due revisori (kappa di Cohen sull'errore grave).
import json,sys,math,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
J=sys.argv[1]
C={f"E{e['_i']:04d}":e for e in json.load(open(f'{S}/qualita/campione.json'))}
runs=collections.defaultdict(list)
for l in open(J):
    r=json.loads(l)
    if r.get('type')!='result' or not isinstance(r.get('result'),dict): continue
    for x in r['result'].get('items',[]): runs[x['id']].append(x)
A={k:v[0] for k,v in runs.items()}; B={k:v[1] for k,v in runs.items() if len(v)>1}
def wilson(k,n,z=1.96):
    if not n: return (0,0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (round(100*(c-h)/d),round(100*(c+h)/d))
def rate(rows,cond): k=sum(1 for r in rows if cond(r)); return k,len(rows)
dims={'errore grave':lambda r:r['errore_grave'],'data sbagliata':lambda r:r['data']=='sbagliata','già passato o annullato':lambda r:r['stato'] in ('gia passato alla data di riferimento','annullato o rinviato'),
      'non è un evento':lambda r:r['natura']=='non e un evento','corso o attività ricorrente':lambda r:r['natura']=='corso o attivita ricorrente',
      'pagina QN incoerente':lambda r:r['pagina_qn']=='incoerente','fuori Roma o online':lambda r:r['fuori_roma_o_online'],
      'luogo sbagliato':lambda r:r['luogo']=='sbagliato','luogo mancante ma nella fonte':lambda r:r['luogo']=='mancante ma nella fonte',
      'ora sbagliata':lambda r:r['ora']=='sbagliata','ora mancante ma nella fonte':lambda r:r['ora']=='mancante ma nella fonte',
      'titolo: frase dal testo':lambda r:r['titolo']=='frase presa dal testo','titolo generico o troncato':lambda r:r['titolo']=='generico o troncato'}
out={'eventi_valutati':len(A),'doppio_revisore':len(B),'strati':{}}
per=collections.defaultdict(list)
for k,r in A.items(): per[C[k]['strato']].append(r)
tot=list(A.values())
out['totale']={d:{'casi':rate(tot,f)[0],'quota_%':round(100*rate(tot,f)[0]/len(tot)),'ic95':wilson(*rate(tot,f))} for d,f in dims.items()}
for s,rows in sorted(per.items()):
    out['strati'][s]={'n':len(rows),**{d:rate(rows,f)[0] for d,f in dims.items()}}
# peso della pagina: ogni strato pesa per la sua quota di eventi (Roma Today escluso)
E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
src=open(f'{S}/qualita/campione.py').read(); exec(src[src.index('def strato(e):'):src.index("QUOTA=")])
peso=collections.Counter(strato(e) for e in E if strato(e)); totp=sum(peso.values())
pond=sum(peso[s]/totp*(sum(1 for r in rows if r['errore_grave'])/len(rows)) for s,rows in per.items())
out['errore_grave_ponderato_%']=round(100*pond,1)
# accordo
if B:
    agree=sum(1 for k in B if A[k]['errore_grave']==B[k]['errore_grave'])/len(B)
    pa=sum(1 for k in B if A[k]['errore_grave'])/len(B); pb=sum(1 for k in B if B[k]['errore_grave'])/len(B)
    pe=pa*pb+(1-pa)*(1-pb); kappa=(agree-pe)/(1-pe) if pe<1 else 1
    out['accordo_errore_grave_%']=round(100*agree); out['kappa_errore_grave']=round(kappa,2)
    for f in ('data','titolo','natura','stato','pagina_qn'): out[f'accordo_{f}_%']=round(100*sum(1 for k in B if A[k][f]==B[k][f])/len(B))
json.dump(out,open(f'{S}/qualita/analisi.json','w'),ensure_ascii=False,indent=1)
json.dump({k:{'a':A[k],'b':B.get(k)} for k in A},open(f'{S}/qualita/giudizi.json','w'),ensure_ascii=False)
print(json.dumps(out,ensure_ascii=False,indent=1))

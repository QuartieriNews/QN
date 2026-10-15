import json,re,html,os,time,sys,requests,collections
os.environ.setdefault('REQUESTS_CA_BUNDLE','/root/.ccr/ca-bundle.crt')
from geo_lookup import localise
B='https://www.comune.roma.it/servizi2/deliberazioniAttiWeb/'
U=B+'data/filtro-dati!cerca.action'
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36','Accept':'application/json'}
tips=json.load(open('A2_api_caricaListaTipologie.json'))
lst=[x for x in next(v for v in tips.values() if isinstance(v,list)) if ',' not in x['codice']]
os.makedirs('A2_tip',exist_ok=True)
def q(params):
    p=dict(params); p.update({'hitCountRicerca':1,'firstResult':0})
    for meth in ('post','get'):
        try:
            time.sleep(1.3)   # Atti Web: una richiesta ogni 1,3 s (HANDOFF §2)
            r=getattr(requests,meth)(U,params=p,headers=H,timeout=90)
            if r.headers.get('content-type','').startswith('application/json') or r.text.lstrip().startswith('{'):
                return r.json(),None
            err=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',r.text))[:160]
        except Exception as e: err=str(e)[:160]
    return None,err
def clean(s): return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s or ''))).strip()
out=[]
for x in lst:
    c=x['codice']; f=f'A2_tip/{c}.json'
    if os.path.exists(f): d=json.load(open(f)); err=d.get('_err')
    else:
        d,err=q({'tipologia':c,'dtRprDa':'2026-06-01','dtRprA':'2026-06-30','itemsPerPage':200})
        json.dump(d if d else {'_err':err},open(f,'w'),ensure_ascii=False)
    if not d or err: out.append({'codice':c,'desc':x['descrizione'],'esito':'errore','err':err}); print(c,'ERR',err,flush=True); continue
    atti=d.get('elencoAtti') or []; tot=int(d.get('total') or 0)
    mun_org=collections.Counter(); mun_obj=0; zona=0; topo=0; ex=[]
    for a in atti:
        org=clean(a.get('dscStrOrg')); obj=clean(a.get('oggetto'))
        m=re.search(r'MUNIC\w*\.?\s*(?:ROMA\s*)?([IVX]+)\b',org.upper()); mun_org[m.group(1) if m else '-']+=1
        L=localise(obj)
        if L['municipio']: mun_obj+=1
        if L['zona']: zona+=1
        if L['toponimo']: topo+=1
        if (L['municipio'] or L['zona']) and len(ex)<4: ex.append((clean(a.get('dtRpr'))[:10],org[:50],obj[:150],L['municipio'],L['zona']))
    out.append({'codice':c,'desc':x['descrizione'],'esito':'con risultati' if tot else 'senza risultati','total':tot,'campione':len(atti),'strutture_municipali':sum(v for k,v in mun_org.items() if k!='-'),'oggetto_municipio':mun_obj,'oggetto_zona':zona,'oggetto_toponimo':topo,'esempi':ex})
    print(c,tot,len(atti),'mun_org',dict(mun_org) if len(mun_org)<6 else 'vari','obj mun/zona/topo',mun_obj,zona,topo,flush=True)
json.dump(out,open('A2_tip/summary.json','w'),ensure_ascii=False,indent=1)
# date-field check on one municipal and one central code
for c in ('CMD','GCD'):
    for df in ('dtRpr','dtProt','dtSeduta'):
        d,err=q({'tipologia':c,df+'Da':'2026-06-01',df+'A':'2026-06-30','itemsPerPage':1})
        print('DATEFIELD',c,df,(d or {}).get('total'),err,flush=True)
d,err=q({'tipologia':'CMD','annoAttoDa':'2026','annoAttoA':'2026','itemsPerPage':1}); print('DATEFIELD CMD anno 2026',(d or {}).get('total'),err)
print('DONE')

# Dati di base dei promotori da ciò che è già stato letto: profilo Facebook, RUNTS, censimento associazioni,
# lista supplementare, contatti degli eventi culture.roma.it, wiki. Poi: cosa manca e dove cercarlo.
import json,re,pickle,collections,sys
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
exec(open(f'{P}/base.py').read().split('E=json.load')[0])   # norm, fbk, host, lit, ukey
B=pickle.load(open(f'{P}/base.pkl','rb')); PR=B['PR']
E_=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
EMAIL=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
def emails(*vals):
    out=[]
    for v in vals:
        for x in (v if isinstance(v,(list,set,tuple)) else [v]):
            for m in EMAIL.findall(str(x or '')):
                m=m.strip('.').lower()
                if m not in out and not m.endswith(('.png','.jpg','.gif','.webp')) and 'example' not in m and 'sentry' not in m and 'wixpress' not in m: out.append(m)
    return out
def first(*vals):
    for v in vals:
        if isinstance(v,(list,tuple)): v=next((x for x in v if x),None)
        if v and str(v).strip() and str(v).strip().lower() not in ('none','nan'): return str(v).strip()
    return None
SOC=('instagram','youtube','x','tiktok','linkedin')
rows=[]
for k,p in PR.items():
    w,prof,ru,asr,su=p['_w'] or {},p['_prof'] or {},p['_ru'] or {},p['_as'] or {},p['_su'] or {}
    can=w.get('canali') or {}; ce=p['contatti_evento']
    fb=p['fb'] or first(can.get('facebook'),ru.get('facebook'),asr.get('url_pagina'),su.get('facebook'))
    sito=first(prof.get('website'),prof.get('websites'),can.get('sito'),ru.get('sito'),asr.get('sito'),su.get('sito'),list(ce['sito']))
    if sito and re.search(r'facebook\.com|instagram\.com',sito): sito=None
    ig=first(prof.get('instagram'),can.get('instagram'),ru.get('instagram'),su.get('instagram'))
    em=emails(prof.get('email'),ru.get('email_principale'),ru.get('email_altre'),asr.get('email'),su.get('email'),list(ce['email']))
    pec=emails(ru.get('pec'))
    em=[e for e in em if e not in pec]
    tel=first(prof.get('phone'),ru.get('telefono'),asr.get('telefono'),su.get('telefono'),list(ce['telefono']))
    ind=first(prof.get('address'),w.get('indirizzo'),ru.get('indirizzo'),asr.get('indirizzo'),su.get('indirizzo'))
    cats=prof.get('categories') or ([prof.get('category')] if prof.get('category') else [])
    cats=lit(cats) if isinstance(cats,str) else cats
    intro=first(prof.get('intro'),asr.get('intro'))
    nomi_ev=collections.Counter(E_[i].get('org') for i in p['eventi'] if E_[i].get('org') and E_[i]['src']=='Facebook (post)')
    r={'key':k,'nome':p['nome'],'titolo_facebook':prof.get('title'),'nomi_eventi':[n for n,_ in nomi_ev.most_common(3)],'altri_nomi':[n for n in p['nomi'] if n!=p['nome']][:5],'wiki':p['wiki'],'n_eventi':p['n_eventi'],
       'ruoli':dict(p['ruoli']),'via':dict(p['via']),'src':dict(p['src']),'pagine_qn':dict(p['pagine_qn']),'municipi':dict(p['municipi']),
       'tipo_wiki':w.get('tipo'),'tipo_registro':(w.get('registro') or {}).get('tipo'),'verdetto_censimento':(w.get('censimento') or {}).get('verdetto') or ru.get('verdetto') or asr.get('verdetto'),
       'sezione_runts':ru.get('sezione_runts'),'temi_runts':ru.get('temi'),'codice_fiscale':ru.get('codice_fiscale'),
       'categorie_facebook':[c for c in (cats or []) if c] if isinstance(cats,list) else [str(cats)],'categoria_google':su.get('categoria_google'),
       'intro_facebook':intro,'follower':prof.get('followers') or asr.get('follower') or ru.get('facebook_follower'),'pagina_creata':prof.get('creation_date'),
       'facebook':fb,'sito':sito,'instagram':ig,'youtube':first(prof.get('youtube')),'x':first(prof.get('x')),'tiktok':first(prof.get('tiktok')),'linkedin':first(prof.get('linkedin')),
       'email':em,'pec':pec,'telefono':tel,'indirizzo':ind,'zona_sede':w.get('zona') or ru.get('zona_qn') or asr.get('zona_qn') or su.get('pagina'),'municipio_sede':w.get('municipio') or ru.get('municipio') or asr.get('municipio') or su.get('municipio'),
       'lat':w.get('lat') or ru.get('lat') or asr.get('lat') or su.get('lat'),'lon':w.get('lon') or ru.get('lon') or asr.get('lon') or su.get('lon'),
       'eventi_idx':sorted(set(p['eventi'])),'link':p['link']}
    rows.append(r)
json.dump(rows,open(f'{P}/promotori_1.json','w'),ensure_ascii=False,indent=0)
n=len(rows); c=collections.Counter()
for r in rows:
    for f in ('facebook','sito','instagram','telefono','indirizzo','intro_facebook'): c[f]+=bool(r[f])
    c['email']+=bool(r['email']); c['categoria']+=bool(r['categorie_facebook'] or r['tipo_registro'] or r['categoria_google'] or r['sezione_runts'])
print('promotori',n,{k:f'{v} ({100*v//n}%)' for k,v in c.items()})
need_site=[r for r in rows if r['sito'] and (not r['email'] or not r['intro_facebook'])]
need_fb=[r for r in rows if r['facebook'] and not r['link']['profilo_facebook']]
nothing=[r for r in rows if not r['sito'] and not r['facebook']]
print('siti da leggere (email o descrizione mancanti)',len(need_site),'pagine Facebook senza profilo',len(need_fb),'senza sito né Facebook',len(nothing),'di cui con 2+ eventi',sum(1 for r in nothing if r['n_eventi']>=2))

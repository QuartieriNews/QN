# Promotori: unione dei dati (profili, siti, ricerca dei canali), categorie e descrizioni, posizione sulla diffusione,
# analisi per categoria e pagine deboli -> promotori_eventi.xlsx (Drive) + promotori.json per la wiki (senza contatti né testi)
import json,re,collections,sys,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'; sys.path.insert(0,P)
exec(open(f'{P}/base.py').read().split('E=json.load')[0])
import classifica as C
E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
GZ=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); PAGES={z['publication_zone_id']:z['name_display'] for z in GZ['publication_zones'] if z['is_page']}
PRIMARY={z['publication_zone_id']:z['primary_municipality'] for z in GZ['publication_zones'] if z.get('primary_municipality')}
R=json.load(open(f'{P}/promotori_1.json')); CG=json.load(open(f'{P}/canali_google.json'))
SL={r['host']:r for r in json.load(open(f'{P}/siti_letti.json'))}
T={r['id'] for r in json.load(open(f'{S}/supplementare/pagine_target.json'))}   # le 41 pagine deboli
PROV=re.compile(r'@(gmail|libero|yahoo|hotmail|outlook|live|tiscali|alice|virgilio|tin|fastwebnet|email|icloud|me|aruba|inwind|katamail|msn)\.',re.I)
BADMAIL=re.compile(r'nome@|name@|example|email@email|tuamail|youremail|info@sito|@dominio|privacy@|dpo@|webmaster@|wordpress@|noreply|no-reply|@sentry|@wix',re.I)
def clean_mails(ms,site_host):
    out=[]
    for m in ms:
        m=m.lower().strip('.')
        if BADMAIL.search(m) or m in out: continue
        out.append(m)
    sh=(site_host or '').split(':')[0]; base='.'.join(sh.split('.')[-2:]) if sh else None
    own=[m for m in out if base and m.split('@')[1].endswith(base)]; prov=[m for m in out if PROV.search(m)]; rest=[m for m in out if m not in own and m not in prov]
    return own+prov+rest
def platform_position(r):
    hs=collections.Counter(host(E[i].get('url')) for i in r['eventi_idx'])
    if r.get('facebook') and not r.get('sito'): return 'termini della piattaforma','https://www.facebook.com/legal/automated_data_collection_terms'
    if any('romatoday' in (h or '') for h in hs) and len(hs)==1: return 'licenza richiesta','https://www.romatoday.it'
    return None,None
import diritti as D
def site_position(sr): return D.position(sr)
SUFF=re.compile(r'\s*([|•·]\s*(Rome|Roma|Rom|Facebook|Instagram|Connect with friends|Ostia|Fiumicino|Ciampino)\b.*|\(@[^)]*\).*|\s+\|\s*[A-Z][a-zà-ù]+(, [A-Z][a-z]+)?)$')
def tidy(n): return SUFF.sub('',str(n or '')).strip(' -–|•')
GENERIC=re.compile(r'(associazione( culturale| di promozione sociale| sportiva dilettantistica| di volontariato)?|aps|asd|odv|ets|onlus|circolo|comitato|parrocchia)')
def display_name(r):
    # il nome umano: titolo della pagina Facebook, nome dato dal nostro registro o censimento, poi il resto; uno slug (senza spazi) mai per primo
    dom=re.fullmatch(r'(www\.)?[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}',str(r['nome']).strip().lower())
    if dom and not r.get('sito'): r['sito']='https://'+str(r['nome']).strip().lower()
    sr=SL.get(host(r.get('sito'))) or {}
    cands=[r.get('titolo_facebook')]+(r.get('nomi_eventi') or [])+([sr.get('og_site_name'),(sr.get('titolo') or '').split(' – ')[0].split(' | ')[0].split(' - ')[0]] if dom else [])+[r['nome']]+(r.get('altri_nomi') or [])
    cands=[tidy(c) for c in cands if c and tidy(c)]
    good=[c for c in cands if ' ' in str(c).strip()]
    out=(good or cands or [r['nome']])[0].strip()
    if GENERIC.fullmatch(norm(out)):   # solo una forma giuridica («Associazione Culturale»): il nome lo dà il dominio o la pagina Facebook
        out=(host(r.get('sito')) or str(r.get('facebook') or '').rstrip('/').split('/')[-1] or out)
    return out
PLATHOST=re.compile(r'(^|\.)(gofund\.me|gofundme\.com|linktr\.ee|linktree\.com|eventbrite\.[a-z.]+|bit\.ly|tinyurl\.com|urly\.it|forms\.gle|docs\.google\.com|wa\.me|t\.me|beacons\.ai|maps\.google\.[a-z.]+|goo\.gl|maps\.app\.goo\.gl|g\.page|whatsapp\.com|chat\.whatsapp\.com|mailchi\.mp|list-manage\.com|vivaticket\.(it|com)|ticketone\.it|taplink\.cc|ticketsms\.it|dice\.fm|xceed\.me|liveticket\.it|boxol\.it|clappit\.com|allmylinks\.com|carrd\.co|campsite\.bio|trustpilot\.com|threads\.(com|net)|instagram\.com|facebook\.com|tiktok\.com|youtube\.com|romatoday\.it|today\.it|ilmessaggero\.it|repubblica\.it|corriere\.it|ansa\.it|rainews\.it|romah24\.com|romadailynews\.it|ilfattoquotidiano\.it|wantedinrome\.com|funweek\.it|zero\.eu|06blog\.it)$')   # piattaforme e testate: non sono il sito del promotore
import ast,urllib.parse
SOCHOST={'facebook':r'facebook\.com|fb\.com','instagram':r'instagram\.com','youtube':r'youtube\.com|youtu\.be','x':r'x\.com|twitter\.com','tiktok':r'tiktok\.com','linkedin':r'linkedin\.com'}
SOCPATH={'instagram':r'/(?!(p|reel|reels|explore|stories|accounts|tv|direct|about|legal|developer)/?$)[A-Za-z0-9._]{2,30}/?',
         'x':r'/(?!(i|intent|share|home|hashtag|search|settings|login|signup|tos|privacy|en|it|widgets\.js)/?$)[A-Za-z0-9_]{2,15}/?',
         'youtube':r'/(channel/UC[\w-]{10,}|user/[\w.-]+|c/[\w.-]+|@[\w.-]+|(?!(watch|embed|playlist|results|channel|user|c|feed|shorts|iframe_api|t|about|howyoutubeworks)/?$)[\w.-]{3,})/?',
         'tiktok':r'/@[\w.]{2,}/?','linkedin':r'/(company|school|showcase|in)/[^/?#]{2,}/?',
         'facebook':r'/(?!(sharer|sharer\.php|share|dialog|plugins|tr|login|events|watch|help|policies|privacy)(/|$)).+'}
def soc_url(v):
    """dict o stringa di dict del lettore di profili ({'username':…,'url':…}), lista, URL semplice -> URL del profilo o None"""
    if isinstance(v,list): v=v[0] if v else None
    if isinstance(v,str) and v.strip().startswith('{'):
        try: v=ast.literal_eval(v.strip())
        except Exception: return None
    if isinstance(v,dict):
        un=str(v.get('username') or '').strip()
        v=('https://'+un if un.startswith('www.') else un) if re.match(r'(https?://|www\.)',un) else (v.get('url') or v.get('link'))
    return v.strip() if isinstance(v,str) and v.strip().startswith('http') else None
def social_ok(k,u):
    u=soc_url(u)
    if not u: return None
    sp=urllib.parse.urlsplit(u); h=sp.netloc.lower().split(':')[0]
    if not re.search(rf'(^|\.)({SOCHOST[k]})$',h): return None
    if k=='youtube' and h.endswith('youtu.be'): return None
    seg=[x for x in (sp.path or '').split('/') if x]
    if k in ('instagram','x','tiktok') and seg: u=f"{sp.scheme}://{sp.netloc}/{seg[0]}"; sp=urllib.parse.urlsplit(u)   # il profilo, non un suo contenuto
    return u if re.fullmatch(SOCPATH[k],sp.path or '/') else None
rows=[]
for r in R:
    dn=display_name(r)
    if dn!=r['nome']: r['altri_nomi']=[r['nome']]+[n for n in (r.get('altri_nomi') or []) if n!=dn]; r['nome']=dn
    cg=CG.get(r['key'],{})
    for k in ('sito','facebook','instagram'):
        if not r.get(k) and cg.get(k): r[k]=cg[k]; r.setdefault('canali_da_ricerca',[]).append(k)
    if r.get('sito') and PLATHOST.search(host(r['sito']) or ''): r.setdefault('altri_link',[]).append(r['sito']); r['sito']=None   # una piattaforma o una testata non è il sito del promotore
    h=host(r.get('sito')); sr=SL.get(h) if h else None
    if sr and sr.get('esito')=='letto':
        r['email']=clean_mails(list(r.get('email') or [])+list(sr.get('email') or []),h)
        if not r.get('telefono') and sr.get('telefono'): r['telefono']=sr['telefono'][0]
        so=sr.get('social') or {}
        for k,pre in (('facebook','https://www.facebook.com/'),('instagram','https://www.instagram.com/'),('youtube','https://www.youtube.com/'),('x','https://x.com/'),('tiktok','https://www.tiktok.com/'),('linkedin','https://www.linkedin.com/')):
            if not r.get(k) and so.get(k) and so[k][0] not in ('profile.php','sharer','share'):
                v=so[k][0]; r[k]=v if v.startswith('http') else pre+v.lstrip('/')
    else: r['email']=clean_mails(r.get('email') or [],h)
    for k in SOCHOST:
        if r.get(k): r[k]=social_ok(k,r[k])
    if re.search(r'itinerant|online|in tutta|varie sedi|non disponibile',str(r.get('indirizzo') or ''),re.I): r['indirizzo']=None; r['zona_sede']=None; r['municipio_sede']=None; r['lat']=r['lon']=None
    if r.get('zona_sede') in PRIMARY: r['municipio_sede']=PRIMARY[r['zona_sede']]   # zona e municipio dalla stessa fonte: il municipio è quello della zona
    C.describe(r,E,PAGES,sr if sr and sr.get('esito')=='letto' else None)
    lab,prova,testo=site_position(sr)
    if not lab or lab=='non verificabile':
        pl,pp=platform_position(r)
        if pl:
            lab,prova,testo=D.MANUALE['facebook.com' if pl=='termini della piattaforma' else 'romatoday.it']
        elif r.get('facebook') and sr:   # sito non leggibile (non raggiungibile o piattaforma): vale il canale da cui leggiamo gli eventi
            lab,prova,testo=D.MANUALE['facebook.com']; testo='(sito non leggibile: vale Facebook) '+testo
        elif not sr:   # nessun sito: la posizione del canale principale dei suoi eventi (culture.roma.it, siti aggregatori…)
            hs=collections.Counter(host(E[i].get('url')) for i in r['eventi_idx'] if host(E[i].get('url')))
            for hh,_ in hs.most_common(1):
                if PLATHOST.search(hh) and not any(hh==k or hh.endswith('.'+k) for k in D.MANUALE): continue
                hp=SL.get(hh) or {'host':hh,'esito':'non letto'}
                l2,p2,t2=D.position(hp)
                if l2 and l2!='non verificabile': lab,prova,testo=l2,p2,'(posizione del canale) '+str(t2 or '')
    r['diffusione']=lab or 'non verificabile'; r['diffusione_prova']=prova; r['diffusione_testo']=testo
    r['bot_ia_bloccati']=', '.join(sr.get('bot_ia_bloccati') or []) if sr else None
    r['in_pagine_deboli']=sum(v for z,v in r['pagine_qn'].items() if z in T)
    rows.append(r)
# canali social condivisi da promotori diversi (credito dell'agenzia web nel piè di pagina, ente sovraordinato): tolti se l'handle non è il promotore
tok=lambda x: re.sub(r'[^a-z0-9]','',str(x or '').lower())
cnt=collections.Counter((k,r[k].lower().rstrip('/')) for r in rows for k in SOCHOST if r.get(k))
for r in rows:
    for k in SOCHOST:
        u=r.get(k)
        if not u or cnt[(k,u.lower().rstrip('/'))]<3: continue
        hd=tok(urllib.parse.urlsplit(u).path.strip('/').split('/')[-1].lstrip('@'))
        nm=tok(norm(r['nome'])); hs_=(host(r.get('sito')) or '').split('.'); sh=tok(hs_[-2]) if len(hs_)>=2 else ''
        mine=hd and (hd==nm or hd==sh or (len(hd)>=6 and (hd in nm or hd in sh)) or (len(nm)>=6 and nm in hd) or (len(sh)>=6 and sh in hd))
        if not mine: r.setdefault('canali_scartati',[]).append(u); r[k]=None
# stesso promotore sotto due chiavi (pagina Facebook e nome): una riga sola, eventi uniti
groups=collections.OrderedDict()
for r in rows:
    k=norm(r['nome']); g=groups.get(k)
    same=g and (not g['sito'] or not r.get('sito') or host(g['sito'])==host(r.get('sito'))) and (not g.get('facebook') or not r.get('facebook') or fbk(g['facebook'])==fbk(r['facebook']))
    if g and same:
        g['eventi_idx']=sorted(set(g['eventi_idx'])|set(r['eventi_idx'])); g['n_eventi']=len(g['eventi_idx'])
        for f in ('pagine_qn','municipi','src','via','ruoli'):
            c=collections.Counter(g.get(f) or {}); c.update(r.get(f) or {}); g[f]=dict(c)
        for f,v in r.items():
            if not g.get(f) and v: g[f]=v
        g['email']=list(dict.fromkeys((g.get('email') or [])+(r.get('email') or [])))
        g['in_pagine_deboli']=sum(v for z,v in g['pagine_qn'].items() if z in T)
    else: groups[k if not g else k+'#'+r['key']]=r
rows=list(groups.values())
json.dump(rows,open(f'{P}/promotori_finale.json','w'),ensure_ascii=False,indent=0)
# per la wiki: solo campi ammessi (il build li ripulisce di nuovo)
def zona_of(r): return r.get('zona_sede') or (max(r['pagine_qn'],key=r['pagine_qn'].get) if r['pagine_qn'] else None)
W=[{'nome':r['nome'],'id':r['wiki'],'categoria':r['categoria'],'sottocategoria':r['sottocategoria'],'ambito':r['ambito'],'descrizione_breve':r['descrizione_breve'],
    'attivita':r['attivita'],'pubblico':r['pubblico'],'municipio':PRIMARY.get(zona_of(r)) or r.get('municipio_sede') or (max(r['municipi'],key=r['municipi'].get) if r['municipi'] else None),
    'zona':zona_of(r),'eventi':r['n_eventi'],
    'canali':{k:r[k] for k in ('sito','facebook','instagram','youtube','x','tiktok','linkedin') if r.get(k) and not (k=='linkedin' and '/in/' in r[k])},
    'contatti':{'email':bool(r['email']),'telefono':bool(r.get('telefono'))},'diffusione':r['diffusione'],'diffusione_prova':r['diffusione_prova']} for r in rows]
json.dump(W,open(f'{P}/promotori.json','w'),ensure_ascii=False,indent=0)
n=len(rows); cov=collections.Counter()
for r in rows:
    for f in ('facebook','sito','instagram','telefono','indirizzo'): cov[f]+=bool(r.get(f))
    cov['email']+=bool(r['email']); cov['autodescrizione']+=bool(r['autodescrizione_fonte'])
print('promotori',n,{k:f'{v} ({100*v//n}%)' for k,v in cov.items()})
print(collections.Counter(r['categoria'] for r in rows).most_common())
print(collections.Counter(r['diffusione'] for r in rows).most_common())

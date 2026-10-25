# Dai risultati Google per ente: candidati Facebook, Instagram, sito (poi verificati leggendo il sito)
import json,re,sys,glob,collections,unicodedata,urllib.parse,math
S=sys.argv[1]; W=f'{S}/runts/work'
E=json.load(open(f'{W}/enti.json'))
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
G={}
for f in glob.glob(f'{W}/g*_*.json'):
    if '/in_' in f: continue
    for r in json.load(open(f)):
        q=r['searchQuery']['term'] if isinstance(r.get('searchQuery'),dict) else r.get('searchQuery')
        G.setdefault(q,[]).extend(r.get('organicResults') or [])
AGG=re.compile(r'(ufficiocamerale|registroimprese|reteimprese|informazione-aziende|aziende\.it|paginegialle|paginebianche|guidamonaci|atoka|reportaziende|fatturatoitalia|companyreports|opencorporates|infobel|cylex|hotfrog|kompass|europages|misterimprese|trovaaziende|aziendeitalia|elenco|italianonprofit|cantiereterzosettore|terzosettore|lavoro\.gov|servizi\.lavoro|runts|agenziaentrate|5x1000|cinquepermille|donazioni|retedeldono|gofundme|ideaginger|produzionidalbasso|wikipedia|linkedin|youtube|tiktok|twitter|x\.com|google\.|maps\.|tripadvisor|yelp|romatoday|repubblica|corriere|ilmessaggero|iltempo|fanpage|ansa|vita\.it|redattoresociale|comune\.roma|regione\.lazio|gazzettaufficiale|anac|openpa|trasparenza|amministrazionetrasparente|issuu|scribd|calameo|academia|researchgate|amazon|ebay|subito|indeed|infojobs|jobrapido|glassdoor|eventbrite|spotlightapp|zazoom|abitarearoma|vignaclarablog|romah24|ilfaroonline|canaledieci|virgilio|tuttocitta|dove\.it|prontopro|groupon|booking|airbnb|telegram|t\.me|wa\.me|pinterest|flickr|vimeo|spotify|soundcloud|mixcloud|issuu|blogspot\.com/search|wordpress\.com/tag|unpli|csvlazio|rockol|info\.roma\.it|reddit|treccani|volontariatolazio|thesocialhub|nonsolocap|romacura|quora|wikiwand|paginemediche|miodottore|idealista|immobiliare|casa\.it|tuttitalia|comuni-italiani|nonsolocap|cap\.|codicepostale|volontariato\.lazio|csv\.|coni\.it|opes|uisp\.it|aics\.it|acsi\.it|csen\.it|endas|arci\.it$|federazione)',re.I)
FBSKIP={'events','groups','pages','people','profile.php','share','hashtag','public','watch','reel','photo','photos','story','posts','p','marketplace','login','help','dialog','sharer','plugins','media','video','videos','permalink.php','story.php','search','l.php'}
GENERIC={'associazione','culturale','sportiva','comitato','centro','gruppo','circolo','roma','di','del','della','dei','delle','il','la','le','lo','e','per','a','in','con','onlus','amici','fondazione','italia','italiana','nazionale','provinciale','regionale','lazio','sezione','territoriale','aps','odv','ets','asd','cooperativa','sociale','impresa','promozione','volontariato'}
def toks(s): return [t for t in norm(s).split() if t not in GENERIC and len(t)>1]
def score(sig,text):
    tx=set(norm(text).split()); tc=norm(text).replace(' ','')
    if not sig: return 0
    hit=sum(1 for t in sig if t in tx or (len(t)>3 and t in tc))
    return hit/len(sig)
def acronym(core): 
    w=[x for x in norm(core).split() if x not in ('di','del','della','dei','delle','e','per','il','la','le','lo','a','in','con')]
    return ''.join(x[0] for x in w) if len(w)>=3 else None
res={}
for e in E:
    rs=G.get(e['query'],[]); sig=[norm(t) for t in e['sig']]; sig=[t for s in sig for t in s.split() if t]
    ac=acronym(e['core']); cn=norm(e['core'])
    fb=[]; ig=[]; site=[]
    for o in rs[:10]:
        u=o.get('url') or ''; t=o.get('title') or ''; d=o.get('description') or ''
        host=urllib.parse.urlsplit(u).netloc.lower().replace('www.','').replace('m.facebook','facebook')
        m=re.match(r'https?://(?:www\.|m\.|it-it\.)?facebook\.com/([^/?#]+)',u)
        if m and not re.match(r'https?://(?:www\.|m\.|it-it\.)?facebook\.com/(?:people/[^/]+/\d+|profile\.php\?id=\d+|[^/?#]+)/?(?:about|events|community|reviews|photos)?/?(?:[?#].*)?$',u): continue   # post, foto, video: il titolo non è il nome della pagina
        if m:
            slug=m.group(1)
            if slug.lower() in FBSKIP: 
                m2=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:people|pages)/([^/]+)/(\d+)',u)
                if not m2: continue
                slug=f'{m2.group(1)}/{m2.group(2)}'; fu=f'https://www.facebook.com/people/{slug}'
            else: fu=f'https://www.facebook.com/{slug}'
            if re.fullmatch(r'[a-z]+(\.[a-z]+)+\.\d+',slug.lower()): continue   # profilo personale (nome.cognome.N): non è un canale di pubblicazione
            m3=re.match(r'https?://(?:www\.|m\.)?facebook\.com/profile\.php\?id=(\d+)',u)
            if m3: fu=f'https://www.facebook.com/profile.php?id={m3.group(1)}'
            tclean=norm(re.sub(r'\s*(\|.*|\(@[^)]*\)|-\s*Home|Facebook)\s*$','',t))
            sc=max(score(sig,t),score(sig,slug.replace('-',' ').replace('.',' ')))
            if e['generico']:
                strip=lambda x: re.sub(r'\b(aps|odv|ets|onlus|asd|ssd|roma|associazione|di promozione sociale|culturale)\b','',x).strip()
                sc=1.0 if cn and (strip(tclean)==strip(cn) or norm(slug).replace(' ','')==cn.replace(' ','')) else 0
            elif cn and cn in tclean: sc=max(sc,1.0)
            fb.append((sc,fu,t)); continue
        m=re.match(r'https?://(?:www\.)?instagram\.com/([^/?#]+)',u)
        if m and m.group(1).lower() not in ('p','reel','explore','stories','accounts','tv'):
            sc=max(score(sig,t),score(sig,m.group(1).replace('_',' ').replace('.',' ')))
            ig.append((sc,f'https://www.instagram.com/{m.group(1)}',t)); continue
        if AGG.search(host) or not host: continue
        dom=host.split(':')[0]; dn=re.sub(r'\.(it|com|org|eu|net|info|biz|roma\.it)$','',dom).replace('-','').replace('.','')
        sc_dom=sum(1 for t in sig if len(t)>3 and t in dn)/len(sig) if sig else 0
        if ac and len(ac)>=3 and ac in dn: sc_dom=max(sc_dom,0.8)
        sc=max(sc_dom,score(sig,t)*0.9)
        site.append((round(sc,2),f"https://{dom}",u,t,round(sc_dom,2)))
    thr=1.0 if e['generico'] else 0.6
    fb=sorted([x for x in fb if x[0]>=thr],key=lambda x:-x[0]); ig=sorted([x for x in ig if x[0]>=thr],key=lambda x:-x[0])
    site=sorted([x for x in site if x[0]>=0.5],key=lambda x:(-x[4],-x[0]))
    seen=set(); site=[x for x in site if not (x[1] in seen or seen.add(x[1]))]
    res[e['cf']]={'risultati':len(rs),'facebook':fb[0][1] if fb else None,'facebook_titolo':fb[0][2] if fb else None,'facebook_punteggio':fb[0][0] if fb else None,'instagram':ig[0][1] if ig else None,'siti_candidati':[{'sito':x[1],'pagina':x[2],'titolo':x[3],'punteggio':x[0],'punteggio_dominio':x[4]} for x in site[:4]]}
json.dump(res,open(f'{W}/match.json','w'),ensure_ascii=False,indent=1)
c=collections.Counter()
for v in res.values():
    c['con risultati']+=v['risultati']>0; c['facebook']+=bool(v['facebook']); c['instagram']+=bool(v['instagram']); c['sito candidato']+=bool(v['siti_candidati'])
print(len(res),dict(c))

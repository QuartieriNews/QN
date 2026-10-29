# Regola «dove cercare» per promotore, dalla prova del canale (prova_canale.py) e dagli eventi già letti a ottobre.
# Ordine di costo: feed del sito < calendario schema.org < pagina eventi del sito < notizie del sito (RSS)
#   < culture.roma.it / agenda delle biblioteche (gratis, già letti ogni giorno) < eventi Facebook < post Facebook < Instagram.
import sys,json,re,gzip,collections,datetime,unicodedata
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
sys.path.insert(0,'/home/user/QN/tools/fonti'); import leggi_eventi_siti as ls
TODAY=datetime.date(2026,10,26)
P=json.load(open(f'{S}/promotori/promotori_finale.json'))
E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
plan=json.load(open(f'{S}/canali/piano.json'))
pages={}
for l in gzip.open(f'{S}/canali/pagine.jsonl.gz','rt'):
    try: r=json.loads(l)
    except Exception: continue
    pages[r['host']]=r
# secondo giro (varianti, ricerca WordPress) e browser (siti in JavaScript): documenti aggiunti all'host
import os
for f in ('pagine2.jsonl.gz','pagine3.jsonl.gz'):
    if not os.path.exists(f'{S}/canali/{f}'): continue
    for l in gzip.open(f'{S}/canali/{f}','rt'):
        if not l.strip(): continue
        r=json.loads(l); d=pages.setdefault(r['host'],{'host':r['host'],'docs':[],'errori':[],'robots_vieta':0})
        for doc in r['docs']:
            if 'righe' not in doc:   # pagina aperta con il browser: schema.org dagli script, date dal testo visibile
                fake=''.join(f'<script type="application/ld+json">{x}</script>' for x in doc.get('ld') or [])
                righe=ls.read_page({'id':r['host'],'nome':r['host']},doc['url'],fake,TODAY,90)
                n=sum(1 for b in ls.dates_in_block(doc['testo'],TODAY) if TODAY<=b<=TODAY+datetime.timedelta(days=90))
                doc['righe']=righe+[{'prova':'data nel testo'}]*min(n,20)
            if all(x['url']!=doc['url'] for x in d['docs']): d['docs'].append(doc)
        d['robots_vieta']+=r.get('robots_vieta',0)
feedhost=set()
for l in open(f'{S}/giro3_feed/out/tutti.jsonl'):
    r=json.loads(l)
    if any('futuri' in k and isinstance(v,(int,float)) and v>0 for k,v in r.items()): feedhost.add(r['host'])
for l in open(f'{S}/giro3_feed/out/ical_tribe.jsonl'):
    r=json.loads(l); t=r.get('tribe_ical')
    if isinstance(t,list) and len(t)>1 and t[1]>0: feedhost.add(r['host'])
feedhost|={r['host'].removeprefix('www.') for r in json.load(open(f'{S}/feed/feed_eventi.json'))}
FEEDURL={}
for r in json.load(open(f'{S}/feed/feed_eventi.json')):
    h=r['host']; FEEDURL.setdefault(h.removeprefix('www.'),{'tribe_rest':f'https://{h}/wp-json/tribe/events/v1/events','tribe_ical':f'https://{h}/?post_type=tribe_events&ical=1','em_ical':f'https://{h}/events/ical/'}[r['feed']])
W={f['id']:f for f in json.load(open('/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad/canali/fonti_eventi_HEAD.json'))['fonti']}   # schedario del 26 ottobre prima di questa regola
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#:]+)',str(u or '').strip().lower()); return m.group(1) if m else None
def canale_evento(e):
    o=str(e.get('o') or ''); s=e.get('src')
    if o.startswith('feed iCal'): return 'feed'
    if o.startswith('Biblioteche di Roma'): return 'biblioteche'
    if s=='culture.roma.it': return 'culture'
    if s=='sito della fonte' or o.startswith('siti') or 'sito' in o: return 'sito' if not o.startswith('VisitLazio') else 'aggregatore'
    if o.startswith('VisitLazio'): return 'aggregatore'
    if s=='Facebook (post)': return 'fb_post'
    if s=='Facebook': return 'fb_eventi'
    if s=='Roma Today': return 'romatoday'
    return 'altro'
STOP=set('della dello delle degli dei del nella nelle negli nel alla alle agli allo con per tra fra una uno che non sono come dove quando anche presso roma evento eventi giornata incontro serata dalle ottobre novembre dicembre gennaio sabato domenica lunedi martedi mercoledi giovedi venerdi edizione nuovo nuova parte prima seconda terza grande insieme tutti tutte nostro nostra vostro ingresso libero gratuito gratuita info prenotazione'.split())
def norm(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',unicodedata.normalize('NFKC',str(s or ''))).encode('ascii','ignore').decode().lower()).strip()
def toks(s): return {w for w in norm(s).split() if len(w)>=4 and w not in STOP and not w.isdigit()}
MESI='gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split()
def date_rx(d):
    m=MESI[d.month-1]
    return re.compile(rf'\b0?{d.day}\s+(?:[a-z]+\s+)?{m[:3]}[a-z]*\b|\b0?{d.day}\s?[/.-]\s?0?{d.month}\b|\b{d.isoformat()}\b|\b{d.year}{d.month:02d}{d.day:02d}\b')
def match(ev,txt):
    """'confermato' se titolo e data stanno vicini nel testo; 'titolo' se il titolo c'è tutto ma senza data vicina."""
    tk=toks(ev['t'])
    if not tk: return None
    need=2 if len(tk)>=2 else 1
    d1=datetime.date.fromisoformat(ev['d1']); d=max(d1,TODAY) if ev['d2'] and ev['d2']>ev['d1'] else d1
    for dd in {d1,d}:
        for m in date_rx(dd).finditer(txt):
            if re.match(r'\s*(?:[a-z]+\s+)?(20[01]\d|202[0-5])\b',txt[m.end():m.end()+16]): continue   # stessa data di un anno passato
            w=set(txt[max(0,m.start()-500):m.end()+500].split())
            hit=tk&w
            if len(hit)>=need and len(hit)/len(tk)>=0.5 and (len(tk)>1 or len(next(iter(tk)))>=6): return 'confermato'
    w=set(txt.split()); hit=tk&w
    if len(tk)>=3 and len(hit)/len(tk)>=0.75: return 'titolo'
    return None
import urllib.parse
def _singolo(seg): return len(re.findall(r'[-_]',seg))>=3 or bool(re.fullmatch(r'\d+|\d+-[\w-]+',seg))
def indice(u):
    """La pagina indice al posto di quella di un singolo evento (lo slug ne porta il titolo, DEC-109): si risale il percorso
    finché l'ultimo pezzo non è uno slug, una data o un numero; la query cade sempre."""
    if not u: return u
    parts=urllib.parse.urlsplit(u); segs=[x for x in parts.path.split('/') if x]
    while segs and (_singolo(segs[-1]) or re.fullmatch(r'\d{1,4}',segs[-1])): segs.pop()
    if segs and re.fullmatch(r'\d{4}',segs[-1]): segs.pop()
    return f'{parts.scheme}://{parts.netloc}/'+('/'.join(segs)+'/' if segs else '')
pubbliche={d['url'] for f in W.values() for d in f.get('dove_cercare') or []}   # già nella wiki: nessuna esposizione nuova
out=[]; st=collections.Counter()
FB_RISERVATI={'profile.php','groups','events','watch','share','photo.php','permalink.php','story.php','hashtag','reel','login','sharer.php','media','plugins','help'}
def fbpage(u):
    """La pagina Facebook e basta: nome utente, people/<nome>/<id> (pagina senza nome utente), p/<nome-id>, pages/<nome>/<id>;
    video, post e altri percorsi cadono (portano testi della fonte), un profilo personale o un gruppo non è una pagina."""
    m=re.match(r'https?://(?:www\.|m\.|it-it\.|web\.)?facebook\.com/(people/[^/?#]+/\d+|pages/[^/?#]+/\d+|p/[^/?#]+|[^/?#]+)',str(u or ''))
    if not m or m.group(1).split('/')[0].lower() in FB_RISERVATI: return None
    return 'https://www.facebook.com/'+m.group(1)
for p in P:
    evs=[E[i] for i in p['eventi_idx'] if max(E[i]['d1'],E[i].get('d2') or E[i]['d1'])>=str(TODAY)]
    ch=collections.Counter(canale_evento(E[i]) for i in p['eventi_idx'])
    hosts=[h for h,d in plan.items() if p['key'] in d['promotori']]
    sitoh=host(p.get('sito'))
    hosts.sort(key=lambda h:(h!=sitoh,h))
    prova={'host':None,'trovati':0,'confermati':0,'titolo':0,'jsonld':0,'date_testo':0,'rss_voci':0,'rss_ultima':None,'pagina':None,'feed':False,'dinamico':False,'letto':False,'errori':0,'robots_vieta':0}
    best=None
    for h in hosts:
        r=pages.get(h)
        if not r: continue
        pr={'host':h,'feed':h in feedhost,'letto':bool(r['docs']),'errori':len(r['errori']),'robots_vieta':r['robots_vieta'],'jsonld':0,'date_testo':0,'confermati':0,'titolo':0,'rss_voci':0,'rss_ultima':None,'pagina':None,'dinamico':False,'canale_trovato':None}
        found={}
        for doc in r['docs']:
            if doc['kind']=='rss':
                pr['rss_voci']=len(doc['items'])
                if doc['items']: pr['rss_ultima']=doc['items'][0]['data']
                for i,ev in enumerate(evs):
                    for it in doc['items']:
                        m=match(ev,norm(it['titolo']+' '+it['testo']))
                        if m=='confermato' or (m=='titolo' and i not in found): found[i]=(m,'rss',doc['url'])
                continue
            if doc.get('dinamico'): pr['dinamico']=True
            jl=sum(1 for x in doc['righe'] if x['prova']=='jsonld'); tx=sum(1 for x in doc['righe'] if x['prova']!='jsonld')
            pr['jsonld']+=jl; pr['date_testo']+=tx
            if (jl or tx>=2) and (pr['pagina'] is None or doc['kind']=='pagina'): pr['pagina']=doc['url']
            t=norm(doc['testo'])
            for i,ev in enumerate(evs):
                m=match(ev,t)
                if m and (i not in found or (m=='confermato' and found[i][0]!='confermato') or (found[i][1]=='rss' and m==found[i][0])):
                    found[i]=(m,'wp' if doc.get('via') else 'jsonld' if jl else 'pagina',doc['url'])
        pr['confermati']=sum(1 for v in found.values() if v[0]=='confermato'); pr['titolo']=sum(1 for v in found.values() if v[0]=='titolo')
        if found:
            k=collections.Counter(v[1] for v in found.values()).most_common(1)[0][0]
            pr['canale_trovato']=k; pr['pagina']=next(v[2] for v in found.values() if v[1]==k)
        sc=(pr['confermati'],pr['titolo'],pr['feed'],pr['jsonld'],pr['date_testo'])
        if best is None or sc>best[0]: best=(sc,pr)
    if best: prova.update(best[1])
    fb=fbpage(p.get('facebook'))
    n=len(evs); trov=prova['confermati']+prova['titolo']
    # ---- regola ----
    if ch['feed'] or (prova['feed'] and (trov or ch['sito'])):
        canale,ev='feed del sito','storico' if ch['feed'] or ch['sito'] else 'confermato'
    elif ch['sito']:
        canale,ev=('calendario del sito (schema.org)' if prova['jsonld'] else 'pagina eventi del sito'),'storico'
    elif ch['biblioteche']:
        canale,ev='agenda Biblioteche di Roma','storico'
    elif prova['confermati'] or prova['titolo']>=1 and prova['confermati']+prova['titolo']>=max(1,n//2):
        k=prova['canale_trovato']
        canale={'rss':'notizie del sito (RSS)','wp':'notizie del sito (RSS)','jsonld':'calendario del sito (schema.org)'}.get(k,'pagina eventi del sito')
        ev='confermato'
    elif ch['culture']:
        canale,ev='culture.roma.it','storico'
    elif prova['feed']:
        canale,ev='feed del sito','probabile'
    elif prova['jsonld'] or prova['date_testo']>=3:
        canale,ev=('calendario del sito (schema.org)' if prova['jsonld'] else 'pagina eventi del sito'),'probabile'
    elif fb and ch['fb_eventi']>=ch['fb_post']:
        canale,ev='eventi Facebook','storico'
    elif fb and ch['fb_post']:
        canale,ev='post Facebook','storico'
    elif fb:
        canale,ev='eventi Facebook','solo pagina'
    elif p.get('instagram'):
        canale,ev='Instagram (non letto)','nessun canale gratuito'
    elif ch['aggregatore'] or ch['romatoday']:
        canale,ev='solo aggregatore','nessun canale proprio'
    else:
        canale,ev='nessun canale','—'
    # pagina da leggere
    w=W.get(p.get('wiki')) or {}
    letta=next((d['url'] for d in w.get('dove_cercare') or [] if d['cosa'] in ('pagina letta alla fonte (calendario)','pagina eventi del sito')),None)
    if canale=='feed del sito': pagina=FEEDURL.get(prova['host'] or '') or next((FEEDURL[host(E[i].get('url'))] for i in p['eventi_idx'] if host(E[i].get('url')) in FEEDURL),None)
    elif ev=='storico' and canale in ('calendario del sito (schema.org)','pagina eventi del sito'): pagina=letta or prova['pagina'] or p.get('sito')
    elif canale=='notizie del sito (RSS)' and prova['canale_trovato']=='wp': pagina=urllib.parse.urljoin(prova['pagina'],'/feed/')
    elif canale in ('calendario del sito (schema.org)','pagina eventi del sito','notizie del sito (RSS)'): pagina=prova['pagina']
    elif canale=='culture.roma.it': pagina=(w.get('canali') or {}).get('culture_luogo')
    elif canale=='eventi Facebook': pagina=(fb+'/events' if not re.search(r'facebook\.com/(people|pages)/',fb) else fb) if fb else None
    elif canale=='post Facebook': pagina=fb
    elif canale=='Instagram (non letto)': pagina=p.get('instagram')
    else: pagina=None
    if canale in ('calendario del sito (schema.org)','pagina eventi del sito') and pagina not in pubbliche: pagina=indice(pagina)
    # controllo: un canale gratuito che copre solo parte degli eventi noti tiene Facebook come controllo
    controllo=None
    gratis=canale not in ('eventi Facebook','post Facebook','Instagram (non letto)','solo aggregatore','nessun canale')
    fbn=ch['fb_eventi']+ch['fb_post']
    if gratis and fb and fbn:
        cop=(trov/n) if ev=='confermato' and n else None
        if ev=='probabile' or (cop is not None and cop<0.8) or ev=='storico' and fbn>sum(ch[c] for c in ('feed','sito','biblioteche','culture')):
            controllo='eventi Facebook' if ch['fb_eventi']>=ch['fb_post'] else 'post Facebook'
    out.append({'key':p['key'],'nome':p['nome'],'wiki':p.get('wiki'),'categoria':p.get('categoria'),'n_eventi':p['n_eventi'],'futuri_noti':n,
                'canali_eventi':dict(ch),'sito':p.get('sito'),'facebook':fb,'instagram':p.get('instagram'),
                'canale':canale,'prova':ev,'controllo':controllo,'pagina':pagina,
                'trovati':trov,'confermati':prova['confermati'],'jsonld':prova['jsonld'],'date_testo':prova['date_testo'],
                'rss_voci':prova['rss_voci'],'sito_letto':prova['letto'],'sito_dinamico':prova['dinamico'],'robots_vieta':prova['robots_vieta'],'errori_sito':prova['errori'],'host_provato':prova['host']})
    st[(canale,ev)]+=1
json.dump(out,open(f'{S}/canali/regola_promotori.json','w'),ensure_ascii=False,indent=0)
for k,v in sorted(st.items(),key=lambda x:-x[1]): print(v,k)
print('controllo FB',collections.Counter(o['controllo'] for o in out))

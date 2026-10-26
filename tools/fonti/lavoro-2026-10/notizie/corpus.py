# Corpus «notizie» dai dati già raccolti (nessuna lettura nuova): post Facebook del pool unificato, della lista
# supplementare e di Acilia; voci dei feed delle notizie dei siti (prova del canale del 26 ottobre); pagine
# istituzionali già scaricate. Testate e media esclusi. Il testo resta nello scratch (DEC-022, DEC-109).
import json,re,gzip,unicodedata,collections,glob,os,html as H
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
def norm(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFKD',unicodedata.normalize('NFKC',str(s or ''))).encode('ascii','ignore').decode().lower())
def fbk(u):
    m=re.search(r'facebook\.com/(?:profile\.php\?id=(\d+)|people/[^/]+/(\d+)|(?:pg/)?([^/?#]+))',str(u or ''),re.I)
    return (m.group(1) or m.group(2) or m.group(3)).lower() if m else None
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#:]+)',str(u or '').strip().lower()); return m.group(1) if m else None
# ---- metadati delle pagine e dei siti: schedario, promotori, censimenti ----
W=json.load(open(f'{S}/wiki_out_v6/fonti_eventi.json'))
META={}
for e in W['fonti']:
    m={'id':e['id'],'nome':e['nome'],'tipo':e.get('tipo'),'zona':e.get('zona'),'municipio':e.get('municipio'),
       'cat_fb':(e.get('censimento') or {}).get('categoria_facebook'),'registro':(e.get('registro') or {}).get('decisione'),
       'verdetto':(e.get('censimento') or {}).get('verdetto'),'eventi':e.get('eventi_totali',0),'categoria':(e.get('promotore') or {}).get('categoria')}
    for k in e.get('chiavi',[]):
        if k.startswith('fb-page:'): META.setdefault(('fb',k[8:]),m)
    for u in e['canali'].get('facebook',[]):
        if fbk(u): META.setdefault(('fb',fbk(u)),m)
    for u in e['canali'].get('sito',[]):
        if host(u): META.setdefault(('h',host(u)),m)
for p in json.load(open(f'{S}/promotori/promotori_finale.json')):
    m={'id':p.get('wiki'),'nome':p['nome'],'tipo':p.get('tipo_wiki'),'zona':p.get('zona_sede'),'municipio':p.get('municipio_sede'),'cat_fb':', '.join(p.get('categorie_facebook') or []) or None,
       'registro':None,'verdetto':None,'eventi':p['n_eventi'],'categoria':p.get('categoria')}
    if fbk(p.get('facebook')): META.setdefault(('fb',fbk(p['facebook'])),m); META[('fb',fbk(p['facebook']))]['categoria']=p.get('categoria')
    if host(p.get('sito')): META.setdefault(('h',host(p['sito'])),m)
MEDIA=re.compile(r'media|news|giornal|testata|magazine|newspaper|editor|publisher|radio|tv |televis|blog|notizi|quotidian|webzine|broadcast',re.I)
MEDIA_NOME=re.compile(r'news|today|messaggero|repubblica|corriere|abitare a roma|daily news|romah24|roma ?news|notizie|giornale|magazine|\btv\b|radio|zero\.eu|funweek|wanted in rome|06blog|ilfattoquotidiano|tg\b|quotidiano|cronaca',re.I)
def media(m,nome):
    return bool(m and m.get('cat_fb') and MEDIA.search(m['cat_fb'])) or bool(MEDIA_NOME.search(nome or '')) or (m or {}).get('categoria')=='Media e informazione'
items=[]; st=collections.Counter(); seen=set()
def add(it):
    k=it['url'] or (it['fonte'],it['data'],it['testo'][:60])
    if k in seen: st['doppione']+=1; return
    seen.add(k)
    if media(it['meta'],it['nome_fonte']): st['testata o media escluso']+=1; return
    if len(it['testo'])<100: st['troppo corto']+=1; return
    items.append(it)
# post Facebook
pool=json.load(open(f'{S}/l08_verifica/pool2.json'))
extra=[dict(x,_lot='lista supplementare',_k=fbk(x.get('facebookUrl') or x.get('inputUrl'))) for x in json.load(open(f'{S}/supplementare/posts_EaMAj9lFGNABIgkRP.json')) if x.get('text')]
extra+=[dict(x,_lot='Acilia',_k=fbk(x.get('facebookUrl'))) for x in json.load(open(f'{S}/post_eventi/acilia_posts.json')) if x.get('text')]
for x in pool+extra:
    k=(x.get('_k') or '').lower(); m=META.get(('fb',k))
    t=x.get('text') or ''
    if x.get('previewTitle'): t+=' [anteprima: '+str(x['previewTitle'])+']'
    add({'tipo':'post Facebook','url':x.get('url'),'fonte':'fb:'+k,'nome_fonte':(m or {}).get('nome') or k,'data':(x.get('time') or '')[:10],'testo':t[:2500],
         'lotto':x.get('_lot'),'evento':x.get('_why')=='ok','resoconto':x.get('_why')=='resoconto','meta':m})
# voci RSS dei siti (prova del canale)
for f in ('pagine.jsonl.gz','pagine2.jsonl.gz'):
    for l in gzip.open(f'{S}/canali/{f}','rt'):
        if not l.strip(): continue
        r=json.loads(l); m=META.get(('h',r['host']))
        for d in r['docs']:
            if d['kind']!='rss': continue
            for itx in d['items']:
                add({'tipo':'notizia del sito (RSS)','url':None,'fonte':'sito:'+r['host'],'nome_fonte':(m or {}).get('nome') or r['host'],'data':itx.get('data'),
                     'testo':(itx['titolo']+' — '+itx['testo'])[:2500],'lotto':'feed dei siti','evento':False,'resoconto':False,'meta':m,'feed':d['url']})
json.dump(items,open(f'{S}/notizie/corpus_tutto.json','w'),ensure_ascii=False)
print(dict(st)); print('voci',len(items),collections.Counter(i['tipo'] for i in items))
print('con metadati',sum(1 for i in items if i['meta']),'con zona',sum(1 for i in items if i['meta'] and i['meta'].get('zona')))

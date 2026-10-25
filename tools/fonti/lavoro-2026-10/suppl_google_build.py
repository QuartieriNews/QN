# Risultati Google «comitato di quartiere <toponimo>» / «associazione <toponimo> Roma eventi» -> candidati per la lista supplementare
import json,re,sys,urllib.parse,collections,unicodedata
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; sys.path.insert(0,f'{S}/supplementare')
from noti import nota,norm,fbk
src=open(f'{S}/ricerca_quartieri/analizza.py').read()
for v in ('AGGR','NEWS','INST','COMM','SKIPHOST'): exec(next(l for l in src.split('\n') if l.startswith(v+'=')))
Q={q[3]:q for q in json.load(open(f'{S}/supplementare/query2.json'))}
ENT=re.compile(r"\b(comitat\w*|associazion\w*|\baps\b|\bodv\b|\basd\b|\bssd\b|circol\w*|centro anziani|centro sociale|centro culturale|pro ?loco|parrocchi\w*|oratori\w*|polisportiv\w*|comunit\w*|scout|agesci|biblioteca|teatro|consulta|social street|retake|gruppo|consorzio|cooperativ\w*|banda|coro|corale|onlus|volontar\w*|cittadin\w*)\b",re.I)
def host(u): return urllib.parse.urlsplit(u).netloc.lower().replace('www.','').split(':')[0]
def clean_title(t): return re.sub(r'\s*[|\-–·]\s*(Facebook|Instagram|Home|Homepage|Pagina iniziale|Roma)\s*$','',re.sub(r'\s*\|\s*Facebook$','',str(t or ''))).strip()
C={}; st=collections.Counter()
for item in json.load(open(f'{S}/supplementare/google_suppl.json')):
    q=(item.get('searchQuery') or {}).get('term'); meta=Q.get(q)
    if not meta: st['query sconosciuta']+=1; continue
    kind,page,topo,_=meta
    for r in item.get('organicResults') or []:
        u=r.get('url') or ''; h=host(u); t=r.get('title') or ''; d=r.get('description') or ''
        if SKIPHOST.search(h): st['scartati: motori, mappe, social generici']+=1; continue
        isfb='facebook.com' in h; isig='instagram.com' in h
        if isfb and '/groups/' in u: canale='gruppo Facebook'
        elif isfb: canale='pagina Facebook'
        elif isig: canale='Instagram'
        else:
            if AGGR.search(h) or NEWS.search(h): st['scartati: aggregatori e testate']+=1; continue
            if INST.search(h): st['scartati: istituzionali (già letti altrove)']+=1; continue
            canale='sito'
        if COMM.search(t+' '+d): st['scartati: commerciali']+=1; continue
        if not ENT.search(t+' '+d+' '+u): st['scartati: non un soggetto associativo']+=1; continue
        tn=norm(topo); inn=f' {tn} ' in f' {norm(t)} ' or f' {tn} ' in f' {norm(u.replace("-"," ").replace("/"," "))} '
        ind=f' {tn} ' in f' {norm(d)} '
        if not (inn or ind): st['scartati: il toponimo non compare']+=1; continue
        k=('fb:'+fbk(u)) if isfb and canale=='pagina Facebook' else ('ig:'+u.split('instagram.com/')[-1].split('/')[0].lower()) if isig else u.split('?')[0].rstrip('/') if canale=='gruppo Facebook' else h
        if not k or k in ('fb:None',): continue
        c=C.setdefault(k,{'nome':clean_title(t)[:120],'canale':canale,'url':u.split('?')[0],'pagina':page,'toponimo':topo,'ricerca':kind,
                          'zona_da':'toponimo nel nome' if inn else 'toponimo nella descrizione','descrizione':d[:240],'gia_nota':nota(clean_title(t),None if (isfb or isig) else u,u if isfb else None),'risultati':0})
        c['risultati']+=1
json.dump(list(C.values()),open(f'{S}/supplementare/google_cand.json','w'),ensure_ascii=False,indent=0)
print(dict(st)); print(len(C),'nuovi',sum(1 for c in C.values() if not c['gia_nota'])); print(collections.Counter((c['canale'],bool(c['gia_nota'])) for c in C.values()).most_common())

# Eventi futuri dei soggetti nuovi della lista supplementare: post Facebook (estrattore dei post) e siti (lettore della ricerca per quartiere)
import json,re,sys,glob,collections
from datetime import date
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
for p in ('supplementare','post_eventi','pagina_eventi'): sys.path.insert(0,f'{S}/{p}')
from noti import fbk
from estrai import estrai,norm
src=open(f'{S}/pagina_eventi/collect.py').read(); exec(src[:src.index('ev=[]; seen=set()')])   # zone_from_text, pages
TODAY=date(2026,10,25)
L=json.load(open(f'{S}/supplementare/lista.json')); byfb={}; byhost={}
def host(u): m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#]+)',str(u or '').strip().lower()); return m.group(1) if m else None
ENTE=re.compile(r"(?i)^\W*(associazion|ass\.|a\.?s\.?d|asd|ssd|aps|odv|onlus|ets|comitat|cdq|c\.d\.q|parrocchi|chiesa|oratori|circolo|centro|polisportiv|pro ?loco|coro|banda|gruppo|scout|agesci|biblioteca|teatro|casa|comunit|cooperativ|fondazion|consulta|rete|social street|retake|amici|club|accademia|scuola|compagnia|laboratorio|spazio|polo)")
def soggetto(o):   # un risultato Google che non è un ente (articolo, blog, testata) non conta come fonte di eventi
    return o['origini']!='ricerca Google' or bool(ENTE.search(o['nome'])) or bool(o.get('facebook') and not o.get('sito'))
for o in L:
    if o['gia_nota'] or not soggetto(o): continue
    if fbk(o.get('facebook')): byfb.setdefault(fbk(o['facebook']),o)
    if host(o.get('sito')): byhost.setdefault(host(o['sito']),o)
out=[]; seen=set(); st=collections.Counter(); per=collections.Counter()
for f in glob.glob(f'{S}/supplementare/posts_*.json'):
    for p in json.load(open(f)):
        k=fbk(p.get('inputUrl') or p.get('facebookUrl') or p.get('url')); o=byfb.get(k)
        if not o or p.get('error') or not p.get('text') or not p.get('time'): continue
        per[k]+=1
        if per[k]>15: continue
        st['post letti']+=1
        e=estrai(p['text'],p['time'],TODAY)
        if not e or e['fine']<TODAY.isoformat(): continue
        kk=(k,norm(e['titolo'] or '')[:40],e['inizio'] if not e['ricorrente'] else e['ricorrente'])
        if kk in seen: continue
        seen.add(kk); zt,_=zone_from_text((e.get('luogo') or '')+' '+(e.get('titolo') or ''))
        out.append({**e,'fonte':o['nome'],'tipo_fonte':o['tipo'],'zona':zt or o['pagina'],'municipio':o['municipio'],'zona_metodo':'luogo nominato nel post' if zt else 'sede della fonte (lista supplementare)','url':p.get('url'),'canale':'Facebook (post)'})
st['pagine con post']=len(per)
for r in json.load(open(f'{S}/supplementare/siti_letti.json')):
    o=byhost.get(r['fonte'])
    if not o: continue
    if sum(1 for x in r['eventi'] if x['prova']!='jsonld')>20: st['siti esclusi: troppe date (blog o aggregatore)']+=1; continue
    for x in r['eventi']:
        if (x.get('fine') or x['inizio'])<TODAY.isoformat(): continue
        if re.search(r"\((?:RM|Rm)\)",x['evento']) and not re.search(r"\bRoma\b",x['evento']): st['blocchi in provincia (RM)']+=1; continue
        if x['prova']!='jsonld' and not estrai(x['evento'],TODAY.isoformat()+'T00:00:00Z',TODAY): st['blocchi datati scartati dai filtri']+=1; continue   # stessi filtri dei post
        kk=(r['fonte'],norm(x['evento'])[:40],x['inizio'])
        if kk in seen: continue
        seen.add(kk); zt,_=zone_from_text(x['evento']) if x['prova']!='jsonld' else (None,None)
        out.append({'titolo':x['evento'][:160],'inizio':x['inizio'][:10],'fine':(x.get('fine') or x['inizio'])[:10],'ora':None,'luogo':x.get('luogo'),'ricorrente':None,'testo':x['evento'][:220],'fonte':o['nome'],'tipo_fonte':o['tipo'],
                    'zona':zt or o['pagina'],'municipio':o['municipio'],'zona_metodo':'luogo nominato nel testo' if zt else 'sede della fonte (lista supplementare)','url':x.get('url') or x.get('pagina'),'canale':'sito della fonte','prova':x['prova']})
json.dump(out,open(f'{S}/supplementare/eventi_suppl.json','w'),ensure_ascii=False,indent=0)
print(dict(st),'eventi futuri',len(out),collections.Counter(e['canale'] for e in out),'pagine QN',len({e['zona'] for e in out if e['zona'] in pages}))
print(sorted(collections.Counter(e['zona'] for e in out).items(),key=lambda x:-x[1])[:45])

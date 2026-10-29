# Biblioteche di Roma: le news dell'OPAC sono eventi schema.org (data, immagine, descrizione); una per appuntamento.
# Scansione per numero (una richiesta al secondo, il sito non ha robots.txt), solo eventi con data dal 25 ottobre 2026.
import json,re,time,html,urllib.request,sys,os,collections
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
UA="QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
TODAY='2026-10-25'
opts=open(f'{P}/bib_news.html',errors='replace').read()
SEDI={c:html.unescape(n).strip() for c,n in re.findall(r'<option value="(RMB[^"]*)"\s*>([^<]+)</option>',opts)}
out=[]; st=collections.Counter()
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for i in range(hi,lo-1,-1):
    try:
        req=urllib.request.Request(f'https://www.bibliotechediroma.it/opac/news/x/{i}',headers={'User-Agent':UA})
        with urllib.request.urlopen(req,timeout=30) as r: h=r.read().decode('utf-8','replace')
    except Exception as e: st['errore']+=1; time.sleep(1); continue
    time.sleep(1)
    m=re.search(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',h,re.S)
    if not m: st['senza evento']+=1; continue
    try: d=json.loads(m.group(1))
    except Exception: st['json illeggibile']+=1; continue
    sd,ed=str(d.get('startDate') or '')[:10],str(d.get('endDate') or d.get('startDate') or '')[:10]
    if not sd: st['senza data']+=1; continue
    if max(sd,ed)<TODAY: st['passato']+=1; continue
    sedi=[]; codes=[]
    for c,n in re.findall(r'class="luogo sede">\s*<a[^>]+href="[^"]*/opac/library/[^"/]*/([^"/]+)"[^>]*>([^<]+)</a>',h):
        if c not in codes: codes.append(c); sedi.append(html.unescape(n).strip())
    dm=re.search(r'<div class="data">\s*([^<]+?)\s*</div>',h); quando=html.unescape(dm.group(1)).strip() if dm else None
    se=d.get('subEvent') or []
    out.append({'id':i,'titolo':d.get('name'),'inizio':sd,'fine':ed,'url':d.get('url') or f'https://www.bibliotechediroma.it/opac/news/x/{i}','immagine':d.get('image'),
                'descrizione':str(d.get('description') or '')[:600],'sedi':sedi,'codici_sede':codes,'quando':quando,'sotto_eventi':len(se) if isinstance(se,list) else 0})
    st['futuro']+=1
    if st['futuro']%25==0: json.dump(out,open(f'{P}/biblioteche_eventi.json','w'),ensure_ascii=False,indent=0); print(dict(st),flush=True)
json.dump(out,open(f'{P}/biblioteche_eventi.json','w'),ensure_ascii=False,indent=0)
print('fine',dict(st))

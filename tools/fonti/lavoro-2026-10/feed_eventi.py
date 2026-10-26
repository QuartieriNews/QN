# Feed strutturati dei siti delle fonti (leve L18, L20, L51 del giro del 26 ottobre): iCal di The Events Calendar e di
# Events Manager, REST di The Events Calendar. Interfacce pubbliche pensate per i lettori di calendario; robots.txt
# verificato sull'URL esatto; campi di contatto (ORGANIZER, ATTENDEE, email, telefoni) mai conservati; riti privati esclusi.
import json,re,time,html,urllib.request,urllib.parse,urllib.robotparser,datetime,collections,sys
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
UA="QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
TODAY=datetime.date(2026,10,26)
sys.path.insert(0,f'{S}/post_eventi'); import estrai as X   # OTHERC: città e comuni fuori Roma
OTHERC=X.OTHERC
# sede delle fonti per host (wiki e promotori): nome, zona, municipio, coordinate
def host(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s?#:]+)',str(u or '').strip().lower()); return m.group(1) if m else None
SEAT={}
for f in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']:
    for u in (f.get('canali') or {}).get('sito') or []:
        h=host(u)
        if h and h not in SEAT: SEAT[h]={'nome':f['nome'],'zona':f.get('zona'),'municipio':f.get('municipio'),'lat':f.get('lat'),'lon':f.get('lon')}
for p in json.load(open(f'{S}/promotori/promotori_finale.json')):
    h=host(p.get('sito'))
    if h and h not in SEAT: SEAT[h]={'nome':p['nome'],'zona':p.get('zona_sede'),'municipio':p.get('municipio_sede'),'lat':p.get('lat'),'lon':p.get('lon'),'ambito':p.get('ambito')}
    elif h: SEAT[h]['ambito']=p.get('ambito')
# candidati: host con feed e futuri>0 nel censimento del 25 ottobre
cand={}
for l in open(f'{S}/giro3_feed/out/ical_tribe.jsonl'):
    r=json.loads(l); t=r.get('tribe_ical')
    if isinstance(t,list) and len(t)>1 and t[1]>0: cand.setdefault(r['host'],set()).add('tribe_ical')
for l in open(f'{S}/giro3_feed/out/tutti.jsonl'):
    r=json.loads(l)
    for k,v in r.items():
        if 'futuri' in k and isinstance(v,(int,float)) and v>0:
            if 'tribe' in k: cand.setdefault(r['host'],set()).add('tribe_rest')
            elif k.startswith('em'): cand.setdefault(r['host'],set()).add('em_ical')
cand['teatriincomune.roma.it']={'em_ical'}
print('host candidati',len(cand),collections.Counter(k for v in cand.values() for k in v))
ROB={}
def robots_ok(u):
    p=urllib.parse.urlsplit(u)
    if p.netloc not in ROB:
        rp=urllib.robotparser.RobotFileParser()
        try:
            req=urllib.request.Request(f'{p.scheme}://{p.netloc}/robots.txt',headers={'User-Agent':UA})
            with urllib.request.urlopen(req,timeout=20) as r: rp.parse(r.read(200000).decode('utf-8','replace').splitlines())
        except Exception: rp=None
        ROB[p.netloc]=rp
    rp=ROB[p.netloc]; return rp is None or rp.can_fetch(UA,u)
def get(u):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'text/calendar,application/json,*/*;q=0.5'})
    with urllib.request.urlopen(req,timeout=30) as r: return r.read(3_000_000).decode('utf-8','replace')
def unfold(txt): return re.sub(r'\r?\n[ \t]','',txt).split('\n')
def ical_events(txt):
    ev=None
    for line in unfold(txt):
        line=line.rstrip('\r')
        if line=='BEGIN:VEVENT': ev={}
        elif line=='END:VEVENT' and ev is not None: yield ev; ev=None
        elif ev is not None and ':' in line:
            k,v=line.split(':',1); name=k.split(';')[0].upper()
            if name in ('SUMMARY','DTSTART','DTEND','LOCATION','URL','CATEGORIES'): ev[name]=v.replace('\\,',',').replace('\\;',';').replace('\\n',' ').strip()
def idate(v):
    m=re.match(r'(\d{4})(\d{2})(\d{2})(?:T(\d{2})(\d{2}))?',v or '')
    return (f'{m.group(1)}-{m.group(2)}-{m.group(3)}',f'{m.group(4)}:{m.group(5)}' if m.group(4) else None) if m else (None,None)
PRIV=re.compile(r'\b(battesim\w*|matrimon\w*|funeral\w*|esequie|cresim\w*|prima comunion\w*|confession\w*|anniversari\w* di matrimonio|colloqui\w*)\b',re.I)
# enti nazionali: un evento senza luogo nel loro feed non è a Roma (campi, assemblee, gare in tutta Italia)
NAZ={'agesci.it','masci.it','archeoclubitalia.org','federkarate.it','assobersaglieri.it','amnesty.it','associazionegeotecnica.it'}
FUORI=re.compile(r'\((?!RM\))[A-Z]{2}\)|,\s*(Italy|Italia|Peru|Chile|Spain|Espa\w+|France|Francia|Germany|Germania|Portugal|Greece|Grecia|Switzerland|Svizzera|UK|USA|Austria|Belgi\w+)\b|\b(Toscana|Lombardia|Veneto|Piemonte|Sicilia|Sardegna|Puglia|Campania|Emilia|Liguria|Marche|Umbria|Abruzzo|Calabria|Basilicata|Molise|Friuli|Trentino|Caporetto)\b|\b(online|zoom|webinar|streaming|piattaforma)\b',re.I)
TIC={'Villa Pamphilj':('monteverde','XII'),'Tor Bella Monaca':('tor-bella-monaca','VI'),'Lido':('ostia','X'),'Quarticciolo':('centocelle','V')}
out=[]; st=collections.Counter(); last=0; SERIE=set()
def row(h,kind,titolo,d1,d2,ora,luogo,url,cats=''):
    if not titolo or not d1: st['senza titolo o data']+=1; return
    d2=d2 or d1
    if max(d1,d2)<str(TODAY): st['passati']+=1; return
    if (datetime.date.fromisoformat(d2)-datetime.date.fromisoformat(d1)).days>31: st['oltre 31 giorni (corsi, stagioni)']+=1; return
    if PRIV.search(titolo): st['riti privati']+=1; return
    seat=SEAT.get(h) or SEAT.get('www.'+h) or {}
    zona=mun=lat=lon=None
    if h=='teatriincomune.roma.it':
        k=next((k for k in TIC if k.lower() in (cats+' '+(luogo or '')).lower()),None)
        if not k: st['teatro non riconosciuto']+=1; return
        zona,mun=TIC[k]; luogo=luogo or f'Teatro {k}' if k!='Lido' else 'Teatro del Lido di Ostia'
    elif luogo and (OTHERC.search(luogo) or FUORI.search(luogo)) and not re.search(r'\bRom[ae]\b',luogo): st['fuori Roma o online (luogo)']+=1; return
    elif not luogo or not re.search(r'\bRom[ae]\b|\b001\d\d\b',luogo):
        if not luogo and (h in NAZ or seat.get('ambito')=='nazionale o internazionale'): st['ente nazionale senza luogo']+=1; return
        if not seat.get('lat'): st['senza luogo e senza sede nota']+=1; return
        lat,lon=seat['lat'],seat['lon']   # pagina dalla sede della fonte
    if (h,re.sub(r'\W','',titolo.lower())[:40]) in SERIE: st['serie: contata una volta']+=1; return   # stesso titolo ripetuto nel feed: una riga sola
    SERIE.add((h,re.sub(r'\W','',titolo.lower())[:40]))
    out.append({'host':h,'feed':kind,'titolo':html.unescape(titolo)[:160],'inizio':d1,'fine':d2,'ora':ora,'luogo':luogo,'org':seat.get('nome') or h,'url':url,'zona':zona,'municipio':mun,'lat':lat,'lon':lon})
    st['tenuti']+=1
for h,kinds in sorted(cand.items()):
    urls=[]
    if 'tribe_rest' in kinds: urls.append(('tribe_rest',f'https://{h}/wp-json/tribe/events/v1/events?start_date={TODAY}&per_page=50'))
    if 'tribe_ical' in kinds: urls.append(('tribe_ical',f'https://{h}/?post_type=tribe_events&ical=1'))
    if 'em_ical' in kinds: urls.append(('em_ical',f'https://{h}/events/ical/'))
    seen=set()
    for kind,u in urls:
        if not robots_ok(u): st['robots vieta']+=1; continue
        w=last+1.0-time.time()
        if w>0: time.sleep(w)
        last=time.time()
        try: txt=get(u)
        except Exception as e: st['errore']+=1; continue
        if kind=='tribe_rest':
            try: d=json.loads(txt)
            except Exception: st['json illeggibile']+=1; continue
            for e in d.get('events') or []:
                v=e.get('venue') or {}; luogo=', '.join(x for x in (v.get('venue'),v.get('address'),v.get('city')) if x) if isinstance(v,dict) else None
                d1=str(e.get('start_date') or '')[:10]; d2=str(e.get('end_date') or '')[:10]; ora=str(e.get('start_date') or '')[11:16]
                key=(re.sub(r'\W','',str(e.get('title') or '').lower())[:40],d1)
                if key in seen: continue
                seen.add(key); row(h,kind,html.unescape(re.sub(r'<[^>]+>','',str(e.get('title') or ''))),d1,d2,ora if ora and ora!='00:00' else None,luogo,e.get('url'))
        else:
            if 'BEGIN:VCALENDAR' not in txt: st['non è un calendario']+=1; continue
            for e in ical_events(txt):
                d1,ora=idate(e.get('DTSTART')); d2,_=idate(e.get('DTEND'))
                if d2 and d2>d1 and not ora and e.get('DTEND','').find('T')<0: d2=(datetime.date.fromisoformat(d2)-datetime.timedelta(days=1)).isoformat()   # DTEND esclusivo nelle date intere
                key=(re.sub(r'\W','',(e.get('SUMMARY') or '').lower())[:40],d1)
                if key in seen: continue
                seen.add(key); row(h,kind,e.get('SUMMARY'),d1,d2,ora if ora and ora!='00:00' else None,e.get('LOCATION'),e.get('URL'),e.get('CATEGORIES',''))
json.dump(out,open(f'{S}/feed/feed_eventi.json','w'),ensure_ascii=False,indent=0)
print(dict(st)); print('eventi',len(out),'host',len({r['host'] for r in out}),collections.Counter(r['host'] for r in out).most_common(12))

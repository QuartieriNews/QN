# Risultati Google «evento + quartiere»: classifica ogni risultato, raggruppa per dominio, separa le fonti nuove da quelle note
import json,re,glob,collections,urllib.parse,unicodedata,openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; D=f'{S}/ricerca_quartieri'
meta=json.load(open(f'{D}/query_meta.json'))
qpages=collections.defaultdict(list)
gz=json.load(open('/home/user/QN/gazetteer/gazetteer.json')); pages={z['publication_zone_id']:z for z in gz['publication_zones'] if z.get('is_page')}
for z,p in pages.items():
    for nm in [x.strip() for x in re.split(r'\s*[-–/]\s*|\s+e\s+',p['name_display']) if x.strip()]:
        for pre in ('evento','eventi','festa'): qpages[f'{pre} {nm} Roma'].append(z)
def host(u): return urllib.parse.urlsplit(u).netloc.lower().replace('www.','').split(':')[0]
def fbslug(u):
    m=re.match(r'https?://(?:www\.|m\.|it-it\.)?facebook\.com/(?:p/|people/)?([^/?#]+)',u or '')
    if not m: return None
    s=m.group(1).lower()
    m2=re.match(r'https?://(?:www\.|m\.)?facebook\.com/(?:p|people)/[^/]*?-?(\d{8,})/?',u or '')
    return m2.group(1) if m2 else s
def igslug(u):
    m=re.match(r'https?://(?:www\.)?instagram\.com/([^/?#]+)',u or ''); s=m.group(1).lower() if m else None
    return None if s in (None,'p','reel','reels','explore','stories','tv','accounts') else s
# fonti note
known_dom=set(); known_fb=set()
def addsite(u):
    if u and str(u).startswith('http'): known_dom.add(host(str(u)))
sched=json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']
for e in sched:
    for u in e['canali']['sito']: addsite(u)
    for d in e['dove_cercare']: 
        if 'facebook' not in d['url']: addsite(d['url'])
    for k in e['chiavi']:
        if k.startswith('fb-page:'): known_fb.add(k[8:])
for r in json.load(open(f'{S}/runts/work/rows.json')):
    addsite(r.get('sito')); s=fbslug(r.get('facebook')); s and known_fb.add(s)
for r in json.load(open(f'{S}/assoc/rows.json')):
    addsite(r.get('sito')); s=fbslug(str(r.get('url_pagina')).replace('facebook.com/','www.facebook.com/')); s and known_fb.add(s)
wb=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v3.xlsx',read_only=True); rr=list(wb.worksheets[0].iter_rows(values_only=True)); h=rr[0]
for r in rr[1:]:
    d=dict(zip(h,r)); addsite(d.get('link')); s=fbslug(d.get('facebook')); s and known_fb.add(s)
known_dom.discard('')
AGGR=re.compile(r'(romatoday|eventbrite|allevents|evensi|eventivicino|spotlightapp|vibeloop|zero\.eu|2night|funweek|romaeventi|eventiaroma|eventi-roma|roma-o-matic|araundapp|experience-app|zazoom|wantedinrome|romeing|inrome|turismoroma|060608|dove\.it|ticketone|vivaticket|dice\.fm|xceed|feverup|tiqets|getyourguide|musement|tripadvisor|songkick|bandsintown|residentadvisor|mymovies|comingsoon|teatro\.it|teatrionline|cittando|romalike|lazioeventi|cosasuccedearoma|trovasagre|iltaccodibacco|ezrome|oggiroma|romaweekend|romadavivere|romaggiano|happeningnext|eventsfy|eventseeker|concertful|jambase|ra\.co|meetup\.com|ticketsms|boxol|ciaotickets|ticketmaster|eventim|liveticket|clappit|dalvivo|sagritaly|eventiesagre|weekend|agenda|virgilio|anyplans|romapop|rockol|concertiaroma|italia\.it|convoca\.la|gancio|eventiesagre|sagre|eventi\.|eventiroma|romaturismo|visitlazio|lazionauta|guidaroma|romaiuta|tuttoroma|romasegreta|romaexplorer|ilovesagre|festeesagre|dovevado|wherevent|eventsinrome|rome\.info|whatsupinrome|romanabeat|2d2web|ticket\.it|aivents|eventland|liveofficialrome|castellinforma|guidalocation|eventiecultura|eventinsieme|cosafarea|eventi-a|fiere|tuttofiere|festivalfinder)',re.I)
NEWS=re.compile(r'(abitarearoma|buonaseraroma|lungoiltevereroma|litoraleonline|romaest|romasud|romanord|zonaroma|quartiere|periferie|repubblica|corriere|messaggero|iltempo|fanpage|leggo|ansa|adnkronos|agi\.it|askanews|dire\.it|rainews|tgcom|today\.it|abitarearoma|vignaclarablog|romah24|ilfaroonline|ostiatv|canaledieci|ilcaffe|ilcorrieredellacitta|urlo|romasette|romanotizie|zerododici|lagone|notizie|giornale|cronaca|news|quotidiano|gazzetta|magazine|blog|press|tv\b|radio|weeklyroma|metropolitano|romadailynews|roma\.it/news|lifegate|ilpost|huffingtonpost|open\.online|wired|vanityfair|dissapore|gamberorosso|agrodolce|zero\.eu|reportage)',re.I)
INST=re.compile(r'(comune\.roma\.it|culture\.roma\.it|bibliotechediroma|sovraintendenzaroma|museiincomuneroma|zetema|regione\.lazio|cultura\.gov\.it|beniculturali|\.gov\.it|\.edu\.it|uniroma|sapienza|diocesidiroma|vicariatusurbis|cittametropolitanaroma|romamobilita|atac\.roma|060608)',re.I)
COMM=re.compile(r'(sala feste|sale feste|sala per feste|catering|location per|location eventi|spazio eventi|affitto|noleggio|animazione|animatori|matrimon|meeting|team building|feste per bambini|compleann|banqueting|wedding|allestiment|service audio|dj per|feste private|ristorante per|addio al celibato)',re.I)
SKIPHOST=re.compile(r'(google\.|youtube|youtu\.be|wikipedia|wikiwand|tiktok|twitter|x\.com|linkedin|pinterest|reddit|quora|amazon|booking|airbnb|idealista|immobiliare|subito|paginegialle|paginebianche|tuttocitta|moovit|waze|maps)',re.I)
rows=[]
for f in glob.glob(f'{D}/google*.json'):
    for r in json.load(open(f)):
        q=r['searchQuery']['term'] if isinstance(r.get('searchQuery'),dict) else r.get('searchQuery'); pg=r['searchQuery'].get('page',1) if isinstance(r.get('searchQuery'),dict) else 1
        for o in r.get('organicResults') or []:
            u=o.get('url') or ''; hst=host(u); fs=fbslug(u)
            if re.match(r'https?://(?:www\.|m\.)?facebook\.com/events/\d+',u): cat='Facebook: evento'
            elif 'facebook.com' in hst: cat='Facebook: pagina' if fs and fs not in ('groups','events','pages','people','profile.php','watch','share','hashtag') else ('Facebook: gruppo' if '/groups/' in u else 'Facebook: altro')
            elif 'instagram.com' in hst: cat='Instagram' if igslug(u) else 'Instagram: post'
            elif SKIPHOST.search(hst): cat='non pertinente'
            elif AGGR.search(hst): cat='aggregatore di eventi'
            elif INST.search(hst): cat='istituzionale'
            elif NEWS.search(hst) or NEWS.search(u): cat='testata o blog'
            elif COMM.search((o.get('title') or '')+' '+(o.get('description') or '')+' '+hst): cat='commerciale (sale, catering, location)'
            else: cat='sito'
            nota = (fs in known_fb) if cat.startswith('Facebook: pagina') else (hst in known_dom or any(hst.endswith('.'+k) for k in known_dom)) if cat in ('sito','istituzionale','testata o blog') else None
            rows.append({'query':q,'pagine_qn':', '.join(qpages.get(q,[])),'posizione':(int(pg)-1)*10+int(o.get('position') or 0),'categoria':cat,'gia_nota':'sì' if nota else ('no' if nota is False else None),'dominio':hst,'url':u,'titolo':o.get('title'),'snippet':(o.get('description') or '')[:300]})
by=collections.defaultdict(lambda:{'n':0,'q':set(),'z':set(),'urls':[],'titoli':[]})
for r in rows:
    k=('fb:'+fbslug(r['url'])) if r['categoria']=='Facebook: pagina' else ('ig:'+igslug(r['url'])) if r['categoria']=='Instagram' else (re.sub(r'(groups/[^/?#]+).*$',r'\1',r['url']) if r['categoria']=='Facebook: gruppo' else (r['url'] if r['categoria']=='Facebook: evento' else r['dominio']))
    b=by[k]; b['n']+=1; b['q'].add(r['query']); b['z'].update(x for x in r['pagine_qn'].split(', ') if x); b['cat']=r['categoria']; b['nota']=r['gia_nota']
    if r['url'] not in b['urls'] and len(b['urls'])<5: b['urls'].append(r['url'])
    if r['titolo'] and len(b['titoli'])<2: b['titoli'].append(r['titolo'])
dom=[{'fonte':k,'categoria':v['cat'],'gia_nota':v['nota'],'risultati':v['n'],'ricerche':len(v['q']),'pagine_qn':', '.join(sorted(v['z'])),'url_esempio':' · '.join(v['urls'][:3]),'titolo_esempio':' | '.join(v['titoli'])} for k,v in by.items()]
dom.sort(key=lambda d:(d['categoria'],-d['ricerche'],-d['risultati']))
json.dump(rows,open(f'{D}/risultati.json','w'),ensure_ascii=False); json.dump(dom,open(f'{D}/domini.json','w'),ensure_ascii=False)
c=collections.Counter(r['categoria'] for r in rows); print('risultati',len(rows),dict(c))
cd=collections.Counter((d['categoria'],d['gia_nota']) for d in dom); print('fonti distinte per categoria e note',sorted(cd.items(),key=lambda x:-x[1]))

# Indice delle fonti già note (wiki fonti-eventi, registro v4, censimenti RUNTS e associazioni) per riconoscere i doppioni
import json,re,unicodedata,openpyxl,math
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()
STOP=set('associazione ass asd aps odv onlus ets a s d centro circolo comitato di del della dei degli delle e il la lo le gli i in roma rome parrocchia parroc chiesa san santa santo s ss sant culturale sportiva quartiere sociale per a da al alla'.split())
def toks(s): return {w for w in norm(s).split() if w not in STOP and len(w)>2}
def dom(u):
    m=re.match(r'(?:https?://)?(?:www\.)?([^/\s]+)',str(u or '').strip().lower()); d=m.group(1) if m else None
    return None if not d or any(x in d for x in ('facebook.','instagram.','google.','wikipedia','youtube','linktr')) else d
def fbk(u):
    u=str(u or ''); m=re.search(r'profile\.php\?id=(\d+)',u)
    if m: return m.group(1)
    m=re.match(r'(?:https?://)?(?:www\.|m\.)?facebook\.com/(?:p/|people/[^/]+/)?([^/?#]+)',u)
    k=m.group(1).lower() if m else None
    return None if k in ('groups','events','pages','watch','share','sharer','story.php','permalink.php','photo.php','hashtag','profile.php') else k   # un gruppo non è una pagina
K={'dom':{},'fb':{},'nome':[]}
def add(nome,sito=None,fb=None,lat=None,lon=None,orig=''):
    for s in (sito if isinstance(sito,list) else [sito]):
        d=dom(s)
        if d: K['dom'].setdefault(d,(nome,orig))
    for f in (fb if isinstance(fb,list) else [fb]):
        k=fbk(f)
        if k: K['fb'].setdefault(k,(nome,orig))
    t=toks(nome)
    if t: K['nome'].append((t,nome,lat,lon,orig))
for f in json.load(open('/home/user/QN/docs/wiki/fonti-eventi/fonti_eventi.json'))['fonti']:
    c=f.get('canali') or {}; add(f['nome'],c.get('sito') or [],c.get('facebook') or [],f.get('lat'),f.get('lon'),'wiki '+f['id'])
wb=openpyxl.load_workbook('/mnt/user-data/outputs/registro_fonti_v4.xlsx',read_only=True); rr=list(wb.worksheets[0].iter_rows(values_only=True)); h=rr[0]
for r in rr[1:]:
    d=dict(zip(h,r)); add(d['nome'],d.get('link'),d.get('facebook'),orig='registro v4 '+str(d.get('chiave')))
for r in json.load(open(f'{S}/runts/work/rows.json')): add(r['denominazione'],r.get('sito'),r.get('facebook'),orig='RUNTS')
def d_m(a,b,c,d): return math.hypot((a-c)*111000,(b-d)*111000*math.cos(math.radians(a)))
def nota(nome,sito=None,fb=None,lat=None,lon=None):
    d=dom(sito)
    if d and d in K['dom']: return 'sito già noto: '+K['dom'][d][0]
    k=fbk(fb)
    if k and k in K['fb']: return 'Facebook già noto: '+K['fb'][k][0]
    t=toks(nome)
    if len(t)>=1:
        for tt,n,la,lo,o in K['nome']:
            j=len(t&tt)/len(t|tt)
            if (j>=0.8 and len(t)>=2) or (j==1 and la and lat and d_m(float(la),float(lo),lat,lon)<400): return 'nome già noto: '+n
    return None

# Immagini degli eventi della pagina «Eventi dei quartieri» (DEC-101): scaricate una volta, salvate a risoluzione da card
# (lato lungo 800 px, JPEG), con provenienza: source_image_url, image_fetched_at, image_local_path, image_credit, image_removed.
# Roma Today no (licenza Citynews, DEC-026); asset commerciali (Fever) no; le pagine dei siti una richiesta al secondo per host.
import json,re,pickle,hashlib,io,time,datetime,collections,urllib.request,urllib.parse,html,sys,os,threading
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
OUT='/mnt/user-data/outputs/immagini_eventi'; os.makedirs(OUT,exist_ok=True)
exec(open(f'{P}/base.py').read().split('E=json.load')[0])
B=pickle.load(open(f'{P}/base.pkl','rb')); RAW,POSTS=B['RAW'],B['POSTS']
E=json.load(open(f'{S}/pagina_eventi/eventi.json'))['eventi']
EP=json.load(open(f'{P}/eventi_promotori.json'))['eventi_promotori']
UA="QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)"
def eid(e): return hashlib.sha1(f"{e.get('url') or ''}|{e['t']}|{e['d1']}".encode()).hexdigest()[:12]
PREV={}
if os.path.exists(f'{P}/immagini.json'):
    for r in json.load(open(f'{P}/immagini.json')): PREV[r['id']]=r
def get(url,timeout=30,maxb=12_000_000,accept='image/*,*/*;q=0.5'):
    url=urllib.parse.quote(url,safe=":/?&=%#+,;@!$*()~'[]")   # URL con caratteri non ASCII
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':accept})
    with urllib.request.urlopen(req,timeout=timeout) as r: return r.geturl(),r.headers.get('Content-Type',''),r.read(maxb)
BIBIMG={}
if os.path.exists(f'{P}/biblioteche_eventi.json'):
    for x in json.load(open(f'{P}/biblioteche_eventi.json')):
        if x.get('immagine'): BIBIMG[x['url']]=x['immagine']
last={}; lock=threading.Lock()
def polite(u):
    h=urllib.parse.urlsplit(u).netloc
    if 'fbcdn.net' in h: return
    with lock:
        w=last.get(h,0)+1.0-time.time(); last[h]=max(time.time(),last.get(h,0)+1.0)
    if w>0: time.sleep(w)
def og_image(page):
    polite(page); f,ct,b=get(page,accept='text/html'); d=b.decode('utf-8','replace')
    m=re.search(r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]*content=["\']([^"\']+)',d,re.I) or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:image',d,re.I)
    if not m:
        j=re.search(r'"image"\s*:\s*(?:\[\s*)?"([^"]+)"',d)
        return urllib.parse.urljoin(f,html.unescape(j.group(1))) if j else None
    return urllib.parse.urljoin(f,html.unescape(m.group(1)))
def job(i):
    e=E[i]; u=ukey(e.get('url')); rec={'id':eid(e),'evento_idx':i,'titolo':e['t'],'inizio':e['d1'],'pagina_qn':e.get('z'),'fonte':e['src'],'url_evento':e.get('url'),
       'image_credit':e.get('org'),'image_removed':False,'image_local_path':None,'source_image_url':None,'image_fetched_at':None,'esito':None}
    pr=PREV.get(rec['id'])
    if pr and pr.get('esito')=='scaricata' and os.path.exists(f"{OUT}/{rec['id']}.jpg"):
        return {**pr,'evento_idx':i,'pagina_qn':e.get('z'),'image_credit':e.get('org')}   # già scaricata: provenienza conservata
    if e['src']=='Roma Today': rec['esito']='non scaricata: Roma Today, licenza Citynews (DEC-026)'; return rec
    if re.search(r'fever',str(e.get('org'))+str(e.get('url')),re.I): rec['esito']='non scaricata: asset commerciale (DEC-101)'; return rec
    src=(POSTS.get(u) or {}).get('image') if e['src']=='Facebook (post)' else (RAW.get(u) or {}).get('image')
    if not src and 'bibliotechediroma.it/opac/news' in str(e.get('url')): src=BIBIMG.get(str(e.get('url')))
    try:
        if not src and e.get('url') and 'facebook.com' not in str(e['url']) and e['src'] in ('culture.roma.it','sito della fonte'):
            if e['src']=='sito della fonte' and e.get('dv'): rec['esito']='non scaricata: blocco di testo senza pagina dell\'evento'; return rec
            src=og_image(e['url'])
        if not src: rec['esito']='nessuna immagine alla fonte'; return rec
        rec['source_image_url']=src; polite(src)
        try: f,ct,b=get(src)
        except Exception as ex1:
            if 'fbcdn.net' not in src: raise
            alt=urllib.parse.urlunsplit(urllib.parse.urlsplit(src)._replace(netloc='scontent.xx.fbcdn.net'))   # nodo CDN non raggiungibile da qui: stesso file da un nodo generico
            f,ct,b=get(alt)
        im=Image.open(io.BytesIO(b)); w,h=im.size
        if min(w,h)<120: rec['esito']='non scaricata: immagine troppo piccola (logo o icona)'; return rec
        im=im.convert('RGB'); im.thumbnail((800,800))
        path=f'{OUT}/{rec["id"]}.jpg'; im.save(path,'JPEG',quality=82,optimize=True)
        rec.update(image_local_path=f'immagini_eventi/{rec["id"]}.jpg',image_fetched_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                   larghezza_originale=w,altezza_originale=h,larghezza=im.size[0],altezza=im.size[1],esito='scaricata')
    except Exception as ex: rec['esito']=f'errore: {str(ex)[:70]}'
    return rec
if __name__=='__main__':
    order=sorted(range(len(E)),key=lambda i:{'Facebook (post)':0,'Facebook':1,'culture.roma.it':2,'sito della fonte':3}.get(E[i]['src'],4))   # prima le URL firmate che scadono
    with ThreadPoolExecutor(max_workers=12) as ex: res=list(ex.map(job,order))
    res.sort(key=lambda r:r['evento_idx'])
    json.dump(res,open(f'{P}/immagini.json','w'),ensure_ascii=False,indent=0)
    print(collections.Counter((r['fonte'],r['esito'] if not r['esito'].startswith('errore') else 'errore') for r in res).most_common())

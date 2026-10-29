# Filtro delle candidate: fuori Roma, aggregatori e testate non riconosciuti -> filtro.json {fonte: verdetto corretto}
import json,re,html,gzip,urllib.request
from concurrent.futures import ThreadPoolExecutor
D='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad/ricerca_quartieri'
O=json.load(open(f'{D}/fonti_classificate.json')); C=[o for o in O if o['verdetto'].startswith('candidata')]
UA='Mozilla/5.0 (X11; Linux x86_64) QuartieriNews-fonti/1.0 (+contatto redazione)'
OTHER=re.compile(r'(trieste(?!-salario)|bologna|milano|torino|napoli|firenze|venezia|genova|castelliromani|castelli-romani|alexala|piemonte|veneto|unicatt|chioggia|fiumicino|ciampino|frascati|marino\.|velletri|tivoli|anzio|nettuno|pomezia|ardea|latina|viterbo|rieti|frosinone|guidonia|monterotondo|fiano|castelnuovo|sacrofano|formello|campagnano|bracciano|ladispoli|cerveteri)',re.I)
AGG2=re.compile(r'(trainline|trovafestival|diario|insideart|sagr\.|sagre|eventiglobo|myguide|oazis|busforfun|18tickets|tickettando|tripplus|romeinternational|guide|guida|turismo|visit|welcome|tickets|biglietti|ticket|eventi|events|happening|agenda|calendario|cosafare|weekend|explore|tour|viaggi|travel|booking|annunci|offerte|directory|elenco|portale|magazine|mag\.|news|notizie|agenzia|agr|stampa|press|giornale|blog|luceverde|aboutart|dizona|vivereroma|romadavivere|today|online\.it|radio|tv\.)',re.I)
def home_text(fonte):
    try:
        req=urllib.request.Request('https://'+fonte,headers={'User-Agent':UA,'Accept':'text/html'})
        with urllib.request.urlopen(req,timeout=15) as r:
            b=r.read(1_000_000)
            if r.headers.get('Content-Encoding')=='gzip': b=gzip.decompress(b)
        return html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',b.decode('utf-8','replace'),flags=re.S|re.I)))
    except Exception: return ''
def judge(o):
    f=o['fonte']
    if f.startswith('fb:'): return f,None
    if OTHER.search(f): return f,'fuori Roma'
    if AGG2.search(f) and o['categoria']!='istituzionale': return f,'aggregatore o testata (dal dominio)'
    if o['ricerche']>=4 and o['categoria']!='istituzionale': return f,'aggregatore o testata (compare per molti quartieri)'
    if not o.get('indirizzo'):
        t=home_text(f)
        if t:
            roma=len(re.findall(r'\bRoma\b|\bRome\b',t)); other=len(OTHER.findall(t))
            if roma==0 or other>roma: return f,'fuori Roma'
    return f,None
with ThreadPoolExecutor(max_workers=16) as ex: res=dict(ex.map(judge,C))
fil={k:v for k,v in res.items() if v}
json.dump(fil,open(f'{D}/filtro.json','w'),ensure_ascii=False,indent=1)
import collections; print('candidate',len(C),'escluse',len(fil),collections.Counter(fil.values()))

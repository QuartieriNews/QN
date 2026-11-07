import sys, re, json
sys.path.insert(0,'..')
from geo_lookup import localise
from collections import Counter
STOP=set('della delle dello degli nella nelle sulla sulle quindi anche perché questo questa quello quella essere stato stata sono siamo hanno avere fatto fare come dove quando poi però allora ecco cioè grazie prego presente presidente consigliere consigliera consiglieri commissione municipio seduta verbale ordine giorno lavori approvazione varie eventuali punto punti tutto tutti tutte molto ancora sempre adesso oggi proprio parte parole parola dire detto abbiamo avete siete state stati stiamo quella queste questi altro altra altri altre'.split())
def words(t): return [w for w in re.findall(r"[a-zàèéìòù]{5,}", t.lower()) if w not in STOP]
for guid in sys.argv[1:]:
    t=open(f'rtv/vtt/{guid}.txt').read()
    stamps=re.findall(r'\[(\d+):(\d+)\]',t)
    last=int(stamps[-1][0])*60+int(stamps[-1][1]) if stamps else 0
    body=re.sub(r'\[\d+:\d+\]','',t)
    n=len(body.split())
    loc=localise(body) if callable(localise) else None
    print(json.dumps({'guid':guid,'words':n,'min':round(last/60,1),'wpm':round(n/(last/60)) if last else None,'luoghi':loc,'termini':[w for w,_ in Counter(words(body)).most_common(25)]},ensure_ascii=False,default=str))

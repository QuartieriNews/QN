# Analysis helper for one recording: transcript stats, places (gazetteer lookup), comparison with verbale/convocazione text, A1 overlaps.
import sys, os, json, re, csv, datetime as dt
sys.path.insert(0,'..')
from geo_lookup import localise
from json3_to_text import convert
from collections import Counter
STOP=set('della delle dello degli nella nelle sulla sulle quindi anche perché questo questa quello quella essere stato stata sono siamo hanno avere fatto fare come dove quando poi però allora ecco cioè grazie prego presente presidente consigliere consigliera consiglieri commissione municipio seduta verbale ordine giorno lavori approvazione varie eventuali punto punti tutto tutti tutte molto ancora sempre adesso oggi proprio parte parole parola dire detto abbiamo avete siete state stati stiamo quella queste questi altro altra altri altre'.split())
def words(t): return [w for w in re.findall(r"[a-zàèéìòù]{5,}", t.lower()) if w not in STOP]
def main(vid):
    rows={r['id']:r for r in csv.DictReader(open('deliver_video/A4_youtube_giugno2026_censimento.csv'))}
    r=rows.get(vid) or {'titolo':'(fuori censimento)','territorio':'','data_seduta':'','durata_hm':''}
    out={'id':vid,'titolo':r['titolo'],'territorio':r['territorio'],'data_seduta':r['data_seduta'],'durata_hm':r['durata_hm']}
    cap=f'caps/{vid}.it.json3'
    if not os.path.exists(cap): out['trascrizione']='assente'; print(json.dumps(out,ensure_ascii=False)); return
    text,st=convert(cap); open(f'caps/{vid}.it.txt','w').write(text)
    out['trascrizione']=st; out['parole_al_minuto']=round(st['words']/(st['dur_s']/60)) if st['dur_s'] else None
    # places in transcript
    loc=localise(text) if text else {}
    out['luoghi_trascrizione']=loc if not isinstance(loc,dict) else {k:(v if not isinstance(v,(set,list)) else sorted(v)[:15]) for k,v in loc.items()}
    # verbale / convocazione text
    for kind in ('MMV','MMC'):
        f=f'verbali/{vid}_{kind}.txt'
        if os.path.exists(f):
            vt=open(f).read(); out[f'{kind}_parole']=len(vt.split())
            if len(vt.split())>30:
                out[f'{kind}_luoghi']=localise(vt)
                # keywords in transcript not in verbale (top 25 by frequency) and shared
                tw=Counter(words(text)); vw=set(words(vt))
                out[f'{kind}_termini_condivisi']=[w for w,_ in tw.most_common(200) if w in vw][:20]
                out[f'{kind}_termini_solo_video']=[w for w,c in tw.most_common(400) if w not in vw and c>=3][:30]
        else: out[f'{kind}_parole']=None
    # A1 overlaps: same Municipio, ±10 days, shared keywords in title
    M=r['territorio'].replace('Municipio ','')
    a1=list(csv.DictReader(open('../A1_june_text.tsv'),delimiter='\t'))
    tw=Counter(words(text)); top=set(w for w,_ in tw.most_common(150))
    ov=[]
    for a in a1:
        if M and not re.search(r'Municipio '+M+r'(?![IVX])', a.get('municipi') or '') and a.get('mun_filter','')!=('municipio_'+M.lower()): continue
        tt=(a.get('title') or '')+' '+(a.get('text') or '')[:1500]
        shared=[w for w in set(words(tt)) if w in top]
        if len(shared)>=5: ov.append({'data':a.get('date'),'tipo':a.get('kind'),'titolo':(a.get('title') or '')[:90],'termini':shared[:8]})
    out['A1_sovrapposizioni_candidate']=ov[:8]
    # top terms
    out['termini_frequenti']=[w for w,_ in tw.most_common(40)]
    print(json.dumps(out,ensure_ascii=False,indent=1))
if __name__=='__main__':
    for v in sys.argv[1:]: main(v)

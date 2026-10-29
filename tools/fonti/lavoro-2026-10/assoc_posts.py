# Aggrega i post Facebook (ultimi 6 mesi) per pagina -> assoc/posts.json: quanti post, ultimo post, quanti annunciano un evento.
import json,sys,re,glob,collections
S=sys.argv[1]
def slug(u): return re.sub(r'^https?://(www\.|m\.)?facebook\.com/','',str(u or '')).strip('/').lower().split('?')[0]
pages=json.load(open(f'{S}/assoc/pages.json')); byslug={slug(p['url']):p['url'] for p in pages}
MESI=r'gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre'
GIORNI=r'luned|marted|mercoled|gioved|venerd|sabato|domenica'
DATA=re.compile(r'(\b\d{1,2}\s*(?:'+MESI+r')\b|\b\d{1,2}[/.]\d{1,2}(?:[/.]\d{2,4})?\b|\b(?:'+GIORNI+r')\w*\s+\d{1,2}\b|\bore\s+\d{1,2}[.:,]?\d{0,2}\b|\balle\s+\d{1,2}[.:,]?\d{0,2}\b|\bh\.?\s?\d{1,2}[.:]\d{2}\b)',re.I)
EVENTO=re.compile(r'\b(evento|eventi|incontro|incontri|presentazione|festa|laboratorio|laboratori|concerto|mostra|spettacolo|assemblea|conferenza|seminario|workshop|corso|corsi|visita guidata|passeggiata|camminata|torneo|gara|proiezione|cineforum|reading|dibattito|iniziativa|appuntamento|vi aspettiamo|ti aspettiamo|ingresso|prenotazione|iscrizioni|open day|mercatino|sagra|inaugurazione|convegno|tavola rotonda|aperitivo|cena|pranzo sociale|giornata|manifestazione|sit-in|presidio|fiaccolata|marcia|raccolta)\b',re.I)
out=collections.defaultdict(lambda:{'post':0,'ultimo':None,'post_eventi':0,'esempi':[]})
for f in sorted(glob.glob(f'{S}/assoc/posts_data/*.json')):
    for it in json.load(open(f)):
        u=byslug.get(slug(it.get('inputUrl')))
        if not u: continue
        if it.get('error'):
            out[u]; continue
        r=out[u]; r['post']+=1; t=it.get('time') or ''
        if t and (not r['ultimo'] or t>r['ultimo']): r['ultimo']=t
        txt=it.get('text') or ''
        if DATA.search(txt) and EVENTO.search(txt):
            r['post_eventi']+=1
            if len(r['esempi'])<2: r['esempi'].append(it.get('url'))
json.dump(out,open(f'{S}/assoc/posts.json','w'),ensure_ascii=False,indent=1)
c=collections.Counter('post con eventi' if v['post_eventi'] else 'post senza eventi' if v['post'] else 'nessun post' for v in out.values())
print('pagine lette',len(out),c)

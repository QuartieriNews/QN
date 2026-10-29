# Schede delle parrocchie dall'annuario della Diocesi di Roma (una richiesta al secondo)
import json,re,time,subprocess,os
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; D=f'{S}/supplementare/parr'
L=json.load(open(f'{S}/supplementare/parrocchie_lista.json')); out=[]
def txt(h):
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S); t=re.sub(r'<[^>]+>','|',t); t=re.sub(r'&nbsp;',' ',t); t=re.sub(r'&#8211;','–',t); return re.sub(r'\s*\|[\s|]*',' | ',t)
for p in L:
    f=f"{D}/{p['id']}.html"
    if not os.path.exists(f):
        subprocess.run(['curl','-sSL','-m','30','-o',f,f"https://www.diocesidiroma.it/phpenti/ente/?ID={p['id']}"]); time.sleep(1)
    t=txt(open(f,errors='replace').read())
    i=t.find(p['nome'][:20]); seg=t[i:i+2500] if i>=0 else ''
    m=re.search(r'\|\s*([^|]*?\d{5}[^|]*?)\s*\|',seg); ind=m.group(1).strip() if m else None
    sito=re.search(r'\|\s*((?:https?://)?(?:www\.)?[a-z0-9.-]+\.[a-z]{2,}(?:/[^\s|]*)?)\s*\|',seg.split('Incaricati')[0].split('Sito WEB')[-1]) if 'Sito WEB' in seg else None
    mail=re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+',seg.split('Incaricati')[0])
    tel=re.search(r'telefono\s*–\s*([\d ./]+)',seg)
    strade=re.findall(r'•\s*([^|]*?)\s*–\s*(\d{5})\s*–\s*ROMA',t)
    out.append({**p,'indirizzo':ind,'sito':sito.group(1) if sito else None,'email':mail.group(0) if mail else None,'telefono':tel.group(1).strip() if tel else None,'n_strade':len(strade),'strade':[s for s,_ in strade][:400],'cap':sorted({c for _,c in strade})})
json.dump(out,open(f'{S}/supplementare/parrocchie.json','w'),ensure_ascii=False,indent=0)
print(len(out),sum(1 for o in out if o['indirizzo']),sum(1 for o in out if o['sito']),sum(1 for o in out if o['email']))

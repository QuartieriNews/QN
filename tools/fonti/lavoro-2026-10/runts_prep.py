# RUNTS Roma: pulizia dei nomi e query di ricerca, una per ente
import openpyxl,re,json,collections,unicodedata,sys
S=sys.argv[1]
wb=openpyxl.load_workbook(f'{S}/runts/in/enti.xlsx',read_only=True); rows=list(wb['Sheet1'].iter_rows(values_only=True)); h=rows[0]
E=[dict(zip(['cf','repertorio','denominazione','cognome','nome_lr','sezione','rete','comune','prov','x5','data'],r)) for r in rows[1:]]
bench=[dict(zip(['denominazione','sito','facebook','descrizione'],r)) for r in list(wb['Foglio1'].iter_rows(values_only=True))[1:] if r[0]]
LEGAL=[r"associazione di promozione sociale",r"organizzazione di volontariato",r"ente del terzo settore",r"societa'? cooperativa sociale(?: a r\.?l\.?| onlus)?",r"cooperativa sociale(?: a r\.?l\.?| onlus)?",r"impresa sociale",r"in forma abbreviata.*$",r"in sigla.*$",r"siglabile.*$",r"o in breve.*$",
       r"\ba\.?\s?p\.?\s?s\.?\b",r"\bo\.?\s?d\.?\s?v\.?\b",r"\be\.?\s?t\.?\s?s\.?\b",r"\bo\.?\s?n\.?\s?l\.?\s?u\.?\s?s\.?\b",r"\ba\.?\s?s\.?\s?d\.?\b",r"\bs\.?\s?s\.?\s?d\.?\b",r"\bs\.?\s?r\.?\s?l\.?s?\b",r"\bs\.?\s?c\.?\s?s\.?\b",r"\bs\.?\s?c\.?\s?r\.?\s?l\.?\b",r"\bi\.?\s?s\.?\b",r"\ba\s?r\.?\s?l\.?\b",r"\bdilettantistica\b"]
def core(n):
    s=str(n).lower().replace('’',"'")
    s=re.sub(r'\([^)]*\)',' ',s)
    for rx in LEGAL: s=re.sub(rx,' ',s,flags=re.I)
    s=re.sub(r'["“”«»]',' ',s); s=re.sub(r'\s*[-–,;:/]+\s*$','',s); s=re.sub(r'^\s*[-–,;:/]+\s*','',s)
    s=re.sub(r'\s+[-–]\s+$','',s); s=re.sub(r'\s+',' ',s).strip(' -–,.;')
    return s
GENERIC={'associazione','culturale','sportiva','comitato','centro','gruppo','circolo','roma','di','del','della','dei','delle','il','la','le','lo','e','per','a','in','con','onlus','amici','fondazione','italia','italiana','nazionale','provinciale','regionale','lazio','sezione','territoriale'}
def sig(s): return [t for t in re.sub(r"[^a-z0-9àèéìòù' ]",' ',s).split() if t not in GENERIC and len(t)>1]
out=[]
for e in E:
    c=core(e['denominazione']); toks=sig(c)
    q=f'"{c}" Roma' if len(toks)>=1 else f'"{c}" Roma {e["sezione"].split()[0].lower()}'
    e.update(core=c,sig=toks,query=q,generico=len(toks)<=1)
    out.append(e)
json.dump(out,open(f'{S}/runts/work/enti.json','w'),ensure_ascii=False,indent=1); json.dump(bench,open(f'{S}/runts/work/bench.json','w'),ensure_ascii=False,indent=1)
print(len(out),'nomi generici (<=1 parola significativa):',sum(1 for e in out if e['generico']))
print(collections.Counter(e['sezione'] for e in out))
for e in out[:3]+out[1000:1004]+out[4000:4003]: print(' ',e['denominazione'],'→',e['query'])
qs=[e['query'] for e in out]; print('query distinte',len(set(qs)))

# Estrazione di eventi dal testo dei post Facebook: annuncio + data (anche relativa alla data del post) + ora + luogo + titolo
import re,unicodedata
from datetime import date,datetime,timedelta
MESI={'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12,
      'gen':1,'feb':2,'mar':3,'apr':4,'mag':5,'giu':6,'lug':7,'ago':8,'set':9,'sett':9,'ott':10,'nov':11,'dic':12}
GIORNI={'lunedi':0,'martedi':1,'mercoledi':2,'giovedi':3,'venerdi':4,'sabato':5,'domenica':6}
WD=['lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica']
MRX='gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre|gen|feb|mar|apr|mag|giu|lug|ago|sett|set|ott|nov|dic'
GRX='lunedi|martedi|mercoledi|giovedi|venerdi|sabato|domenica'
EVENTO=re.compile(r"\b(appuntament\w*|ci vediamo|vi aspettiamo|ti aspettiamo|vi aspetto|unitevi|unisciti|partecipa\w*|incontr\w+|assemblea|festa|feste|passeggiat\w+|visita|visite|laborator\w+|concert\w+|spettacol\w+|mostra|presentazion\w+|torneo|gara|corsa|camminat\w+|raccolt\w+|donazion\w+|mercatin\w+|sagra|cena|pranzo|aperitiv\w+|proiezion\w+|cineforum|reading|conferenz\w+|convegn\w+|seminari\w*|workshop|corso|lezion\w+|open day|inaugurazion\w+|manifestazion\w+|presidio|fiaccolata|pulizia|retake|decoro|volontariato|festival|rassegna|serata|evento|eventi|messa|processione|tombola|ballo|danza|teatro|musica|letture?|gioc\w+|caccia al tesoro|halloween|castagnata|merenda)\b",re.I)
REPORT=re.compile(r"\b(ringrazi\w+|grazie (a|di cuore|mille)|è stat[oa] (un|una)|si è svolt\w+|si è concluso|ieri|eravamo|siamo stati|è andat[oa]|scors[oa]|abbiamo (fatto|vissuto|trascorso))",re.I)
def clean(t):
    out=[]
    for ch in str(t or ''):
        o=ord(ch); cat=unicodedata.category(ch)
        if cat in ('So','Cs','Co') or o>0xFFFF or 0x2190<=o<=0x2BFF: out.append('\n')      # le emoji separano le parti del post
        elif 0xFE00<=o<=0xFE0F or o==0x200D or cat=='Sk': continue
        else: out.append(ch)
    t=re.sub(r'[ \t]+',' ',''.join(out))
    return re.sub(r'\s*\n[\s\n]*','\n',t).strip()
def norm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
def fix_year(d0,month,day):
    best=None
    for y in (d0.year-1,d0.year,d0.year+1):
        try: c=date(y,month,day)
        except ValueError: continue
        diff=(c-d0).days
        if -90<=diff<=330 and (best is None or abs(diff)<abs((best-d0).days)): best=c
    return best
def dates_in(t,d0):
    out=[]; tn=norm(t)
    for m in re.finditer(r"\bdal(?:l[a']?)?\s+(\d{1,2})(?:\s+("+MRX+r"))?\s+al(?:l[a']?)?\s+(\d{1,2})\s+("+MRX+r")\b(?:\s+(\d{4}))?",tn):
        mo2=MESI[m.group(4)]; mo1=MESI[m.group(2)] if m.group(2) else mo2
        a=fix_year(d0,mo1,int(m.group(1))); b=fix_year(d0,mo2,int(m.group(3)))
        if a and b and b>=a: out.append((a,b,m.start()))
    for m in re.finditer(r"\b(\d{1,2})\s*(?:°|º)?\s+("+MRX+r")\b(?:\s+(\d{4}))?",tn):
        if any(abs(m.start()-p)<25 for _,_,p in out): continue
        mo=MESI[m.group(2)]; day=int(m.group(1))
        try: c=date(int(m.group(3)),mo,day) if m.group(3) else fix_year(d0,mo,day)
        except ValueError: c=None
        if c: out.append((c,c,m.start()))
    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b",tn):
        d,mo=int(m.group(1)),int(m.group(2))
        if not (1<=d<=31 and 1<=mo<=12): continue
        try:
            if m.group(3): y=int(m.group(3)); y=y+2000 if y<100 else y; c=date(y,mo,d)
            else: c=fix_year(d0,mo,d)
        except ValueError: c=None
        if c: out.append((c,c,m.start()))
    if not out:   # una data scritta vince su «domani» e «oggi»
        for m in re.finditer(r"\b(oggi|stasera|stamattina|stamani|questa sera|domani|dopodomani)\b",tn):
            k=m.group(1); c=d0+timedelta(days=2 if k=='dopodomani' else 1 if k=='domani' else 0); out.append((c,c,m.start()))
    if not out:
        for m in re.finditer(r"\b(?:(?:questo|questa|prossim[oa])\s+)?("+GRX+r")\b",tn):
            pre=tn[max(0,m.start()-12):m.start()]; post=tn[m.end():m.end()+10]
            if re.search(r"\b(ogni|tutti i|tutte le|il)\s*$",pre) or re.match(r"\s*scors",post): continue
            wd=GIORNI[m.group(1)]; c=d0+timedelta(days=(wd-d0.weekday())%7); out.append((c,c,m.start())); break
    return sorted(out,key=lambda x:x[2])
def recurring(t):
    tn=norm(t)
    m=re.search(r"\b(?:ogni|tutti i|tutte le)\s+("+GRX+r")",tn) or re.search(r"\bil\s+("+GRX+r")\s+(?:pomeriggio|mattina|sera|dalle|alle)\b",tn)
    return m.group(1) if m else None
def ora(t):
    m=re.search(r"\b(?:ore|alle|dalle|h\.?)\s*(\d{1,2})(?:[.:,](\d{2}))?\b",t,re.I)
    if not m: return None
    h=int(m.group(1)); mi=int(m.group(2) or 0)
    return f'{h:02d}:{mi:02d}' if 0<=h<=23 and 0<=mi<=59 else None
CUT=re.compile(r"\s+(?:per|dove|con|vi|ci|nella|nel|tutti|ore|alle|dalle|dal|che|a partire|a dare|a ripristinare|e nei|e nel|nella locandina)\b|[,;:\n]",re.I)
def luogo(t):
    for rx in (r"(?:📍\s*(?:dove\s*:?)?|\bdove\s*:|\bluogo\s*:|presso(?: il| la| lo| l')?|c/o|si terr[aà] (?:a|in|presso))\s*([^\n.;!?]{4,80})",
               r"\b((?:via|viale|piazza|piazzale|largo|parco|parchetto|villa|giardin[oi]|biblioteca|parrocchia|chiesa|teatro|centro anziani|centro sociale|oratorio|scuola|istituto)\s+[^\n.;!?]{2,60})"):
        m=re.search(rx,t,re.I)
        if m:
            v=clean(CUT.split(m.group(1))[0]).split('\n')[0]; v=re.sub(r"^(?:la|il|lo|l')\s+nostra\s+|^nostra\s+","",v.strip(),flags=re.I)
            v=re.sub(r"\s+",' ',v).strip(" -–:,'")
            if re.match(r"(?i)(via|viale|piazza|piazzale|largo|parco|parchetto|villa|giardin[oi])\s",v) and not re.match(r"\S+\s+(?:[Dd](?:egli|ella|elle|ell'|ei|el|i|e)\s*)?[A-ZÀ-Ý0-9]",v): continue   # «via ad una nuova avventura» non è un indirizzo
            if len(v)>=4 and v.lower() not in ('dove','luogo','quando'): return v[:70]
    return None
def titolo(t):
    lines=[l.strip(" -–:|_*#") for l in t.split('\n') if len(l.strip())>=5 and not re.fullmatch(r"(?:#\w+\s*)+",l.strip())]   # una riga di soli hashtag non è un titolo
    if len(lines)>1 and re.fullmatch(r"\w{10,}",lines[0]): lines=lines[1:]   # hashtag senza # in testa (#AMAILTUOQUARTIERE)
    if not lines: return None
    first=lines[0]; letters=[c for c in first if c.isalpha()]
    tt=first if letters and sum(c.isupper() for c in letters)/len(letters)>0.6 else re.split(r"(?<=[.!?])\s",first)[0]
    if REPORT.search(tt):   # resoconto con un prossimo appuntamento: il titolo è la frase dell'appuntamento
        ls=t.split('\n'); i=next((k for k,l in enumerate(ls) if re.search(r"\bprossim\w+",l,re.I)),None)
        if i is not None:
            x=ls[i]+(' '+ls[i+1] if i+1<len(ls) and not re.search(r"[.!?]\s*$",ls[i]) else '')   # la data spesso va a capo dopo un'emoji
            tt=next(y for y in re.split(r"(?<=[.!?])\s+",x) if re.search(r"\bprossim\w+",y,re.I))
    tt=re.sub(r"#(\w+)",r"\1",tt); tt=re.sub(r"\s+",' ',tt).strip(" -–:|_*")
    return tt[:100] if len(tt)>=5 else None
OTHERC=re.compile(r"\b(Milano|Torino|Genova|Bologna|Firenze|Napoli|Venezia|Mestre|Verona|Padova|Trieste|Trento|Bolzano|Bari|Palermo|Catania|Cagliari|Perugia|Ancona|Pescara|L'Aquila|Rimini|Parma|Modena|Brescia|Bergamo|Pisa|Siena|Lucca|Salerno|Lecce|Reggio Calabria|Messina|Viterbo|Rieti|Latina|Frosinone|Tivoli|Frascati|Fiumicino|Ciampino|Civitavecchia|Cesena|Forlì|Ravenna|Ferrara|Piacenza|Cremona|Lodi|Pavia|Como|Varese|Novara|Asti|Cuneo|Alessandria|Vicenza|Treviso|Udine|Bassano del Grappa|Reggio Emilia|Arezzo|Livorno|Prato|Pistoia|Grosseto|Terni|Foligno|Spoleto|Assisi|Orvieto|Macerata|Pesaro|Teramo|Chieti|Caserta|Avellino|Benevento|Potenza|Matera|Taranto|Brindisi|Foggia|Cosenza|Catanzaro|Siracusa|Trapani|Agrigento|Sassari|Olbia|Aosta|Mantova|Caselle Landi|Sambuci|Regione Siciliana|Cervara di Roma|Rocca di Papa|Castel Gandolfo|Monte ?Compatri|Monte Porzio|Zagarolo|Palestrina|Guidonia|Fonte Nuova|Mentana|Monterotondo|Anguillara|Bracciano|Cerveteri|Ladispoli|Ardea|Pomezia|Anzio|Velletri|Albano Laziale|Genzano|Ariccia|Grottaferrata|Rocca Priora|Subiaco|Formello|Sacrofano|Campagnano|Trevignano|Riano|Capena|Fiano Romano|Morlupo|Colleferro|Valmontone|Lariano|Artena|Santa Marinella|Tolfa|Bracciano|Manziana|Castel Madama|Vicovaro|San Cesareo|Bruxelles|Parigi|Londra|Madrid|Berlino)\b")
OTHERC_UP=re.compile(OTHERC.pattern.upper().replace(r"\B",r"\b"))   # post tutti in maiuscolo («CASELLE LANDI»)
NOEV=re.compile(r"\b(rottamazion\w*|scadenz\w*|bando|bandi|candidatur\w*|servizio civile|offerta di lavoro|cerchiamo|webinar|zoom|in diretta|diretta streaming|streaming|dichiarazione dei redditi|5x1000|5 per mille|sondaggio|petizion\w*|online|promozione valida|codice sconto|sconto|scontat\w+|sciopero|ddl|agevolazion\w*|espositor\w*|nostro stand|rimarremo chiusi|resteremo chiusi|siamo chiusi|orari della settimana)\b",re.I)
def estrai(text,post_time,today):
    raw=str(text or ''); t=clean(raw)
    if len(t)<25 or not EVENTO.search(t): return None
    if ((OTHERC.search(t) or OTHERC_UP.search(t)) and not re.search(r"\b(?:Roma|ROMA)\b",re.sub(r"(?i)Cervara di Roma","",t))) or NOEV.search(t[:400]): return None
    d0=datetime.fromisoformat(str(post_time).replace('Z','+00:00')).date()
    rec=recurring(t); ds=dates_in(t,d0)
    if REPORT.search(t[:250]) and not [x for x in ds if x[1]>d0]: return None
    fut=[x for x in ds if x[1]>=d0-timedelta(days=1)]
    if rec and not [x for x in fut if x[1]>=today]:
        wd=WD.index(rec); nxt=today+timedelta(days=(wd-today.weekday())%7); fut=[(nxt,nxt,0)]
    if not fut: return None
    a,b,_=fut[0]
    return {'titolo':titolo(t),'inizio':a.isoformat(),'fine':b.isoformat(),'ora':ora(t),'luogo':luogo(raw) or luogo(t),'ricorrente':rec,'data_post':d0.isoformat(),'testo':re.sub(r'\s+',' ',t)[:220]}

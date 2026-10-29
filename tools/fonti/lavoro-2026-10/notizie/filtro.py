# Filtro deterministico dei segnali di notizia (prima dell'analisi con l'AI): lessico per tema, finestra di date.
import json,re,unicodedata,collections,email.utils,datetime
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'
def norm(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFKD',unicodedata.normalize('NFKC',str(s or ''))).encode('ascii','ignore').decode().lower())
TEMI={
 'lavori e cantieri':r'cantier|lavori (?:in corso|di|stradal|sul|sulla|per)|rifaciment|riqualific|manutenzion|asfaltatur|\bbuche\b|marciapied|illuminazione pubblica|lampion|potatur|abbattiment|messa in sicurezza|transenn',
 'mobilita e trasporti':r'\batac\b|autobus|\blinea \d|\bmetro\b|metropolitana|\btram\b|fermata|deviazion|chiusura (?:di |della |del )?(?:strada|via)|\bztl\b|parcheggi|ciclabil|viabilita|cotral|stazione|navetta|sciopero',
 'rifiuti e decoro':r'\bama\b|rifiuti|cassonett|spazzatur|discaric|degrado|sporcizia|decoro|abbandon|\bratti\b|\btopi\b|disinfest|derattizz|erba alta|sfalci',
 'sicurezza e emergenze':r'\bfurt|rapin|aggression|vandal|incendi|\brogo\b|allagament|crollo|crollat|emergenza|spaccio|occupazion|sgomber|ladri|scippo|polizia locale|carabinieri|vigili del fuoco',
 'municipio e istituzioni':r'municipio|consiglio municipale|commissione|assemblea pubblica|delibera|mozione|ordinanza|assessor|presidente del municipio|roma capitale|campidoglio|sindaco|giunta|bilancio partecipativo|consulta',
 'servizi, bandi e scadenze':r'\bbando\b|avviso pubblico|sportello|iscrizion|scadenz|domande? entro|contribut|\bbonus\b|graduatori|\bcaf\b|anagrafe|carta d.identita|patronato|servizio civile|assunzion|selezione',
 'scuola':r'\bscuola|scuole|istituto comprensivo|\bliceo|\bmensa\b|plesso|dirigente scolastic|asilo nido|nidi|materna|anno scolastico',
 'sanita e salute':r'\basl\b|ospedal|vaccin|screening|consultorio|guardia medica|medico di base|medici di famiglia|pronto soccorso|casa della comunita|prevenzione',
 'attivismo e partecipazione':r'raccolta firme|petizion|protest|presidio|mobilitazion|manifestazione|segnalazion|appello|diffida|ricorso al tar|esposto|vertenza|\blotta\b|occupat',
 'aperture e chiusure':r'inaugura|nuova sede|apre (?:il|la|a|in|al)|apertura (?:del|della|di)|riapre|riapertura|chiude|chiusura definitiva|sfratt|trasferiment|ha chiuso|abbiamo aperto',
 'solidarieta e sociale':r'raccolta (?:alimentare|fondi|di beneficenza|vestiti)|donazion|banco alimentare|senza dimora|senzatetto|emergenza freddo|volontari cercasi|cerchiamo volontari|distribuzione (?:pasti|viveri)|povert',
 'lutti e ricordi':r'\blutto\b|scompars|ci ha lasciat|ci hanno lasciat|cordoglio|addio a|in memoria|riposa in pace|anniversario della (?:morte|scomparsa)',
 'premi e storie':r'premio|premiat|riconosciment|\bvinto\b|vincitor|campion|record|centenario|\banni di attivita|compie \d+ anni|storia del quartiere|traguardo|onorificenz',
 'ambiente e verde':r'\bparco\b|riserva|inquinament|amianto|antenn|alberi|cinghial|colonia felina|canile|\bverde pubblico|giardino|orti urbani|alluvion|frana|fiume|tevere|aniene',
 'casa e urbanistica':r'case popolari|\bater\b|alloggi|urbanistic|cementificaz|nuove costruzion|piano regolatore|rigenerazione|\bpnrr\b|giubileo|centro commerciale|lottizzaz|stadio',
}
TX={k:re.compile(v) for k,v in TEMI.items()}
def data_iso(s):
    s=str(s or '')
    if re.match(r'\d{4}-\d{2}-\d{2}',s): return s[:10]
    try: return email.utils.parsedate_to_datetime(s).date().isoformat()
    except Exception: pass
    m=re.search(r'(\d{4})-(\d{2})-(\d{2})',s); return m.group(0) if m else None
C=json.load(open(f'{S}/notizie/corpus_tutto.json'))
out=[]; st=collections.Counter(); bytema=collections.Counter()
for i,it in enumerate(C):
    it['id']=f'N{i:05d}'
    d=data_iso(it['data']); it['data']=d
    if not d: st['senza data']+=1; continue
    if d<'2026-04-24': st['prima del 24 aprile (fuori dalla finestra dei post)']+=1; continue
    t=norm(it['testo'])
    t=re.sub(r'(patrocini\w*|collaborazione|sostegno|contributo|partnership|sponsor\w*)\s+(?:\w+\s+){0,5}?(del |della |di )?(municipio|roma capitale|comune|regione|asl)\b',' ',t)   # il patrocinio non è una notizia
    t=re.sub(r'premiazion\w*|in palio|vinci (?:un|una)|concorso fotografico','',t)
    temi=[k for k,rx in TX.items() if rx.search(t)]
    if it['evento'] and len(temi)<2: st['annuncio di evento senza segnali forti']+=1; continue
    it['temi']=temi
    if not temi: st['nessun segnale di notizia']+=1; continue
    out.append(it); bytema.update(temi)
json.dump(out,open(f'{S}/notizie/candidati.json','w'),ensure_ascii=False)
print(dict(st)); print('candidati',len(out),collections.Counter(i['tipo'] for i in out)); print(bytema.most_common())
print('per mese',sorted(collections.Counter(i['data'][:7] for i in out).items()))
print('caratteri',sum(len(i['testo']) for i in out))

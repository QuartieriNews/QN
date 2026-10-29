# Categorie, ambito, attività e descrizioni dei promotori. La descrizione breve è scritta da regole (etichette nostre, nessun
# testo della fonte): può andare nella wiki. La lunga aggiunge l'autodescrizione del soggetto tra virgolette: resta su Drive.
import json,re,collections,unicodedata
S='/tmp/claude-0/-home-user-QN/6ddd5f5b-029a-56ef-ba4a-9ebf9ede2447/scratchpad'; P=f'{S}/promotori'
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower())).strip()

MACRO=['Istituzioni pubbliche','Grandi istituzioni culturali e fondazioni','Teatri, cinema e spazi di spettacolo','Musei, gallerie e spazi espositivi',
       'Associazioni culturali e artistiche','Comitati di quartiere e reti civiche','Parrocchie e realtà religiose','Centri sociali, centri anziani e spazi di comunità',
       'Terzo settore sociale e sanitario','Sport e movimento','Ambiente, natura e animali','Turismo e visite guidate','Scuole, università e formazione',
       'Locali e attività commerciali','Intermediari: biglietterie, aggregatori e media','Politica e sindacati','Persone (artisti, autori, guide)','Non classificato']
# (macro, sottocategoria, regex sul nome) — la prima che corrisponde vince
NAME_RULES=[
 (14,'pagina che raccoglie eventi',r'\b(sagre ?e? ?eventi|sagreeventi|eventi(nel|a|di)|eventi nel lazio|eventi roma|roma eventi|agenda|cosa fare|weekend|what.?s on|events in rome|guida (agli )?eventi|bimbilandia|kids ?(roma|events)|mamme a roma|roma ?bambini|roma per bambini)\b'),
 (14,'biglietteria o aggregatore',r'\b(fever|tuttoteatro|bellaroma|capodanno ?roma|eventi ?(a )?roma|roma ?eventi|inverno romano|estate romana eventi|romeing|wanted in rome|ticketone|vivaticket|eventbrite|dice\b|xceed|ticketsms|mercatini ?di ?roma)\b'),
 (14,'media',r'\b(tv ?2000|tv\b|radio|magazine|giornale|notizie|news|blog|quotidiano|testata|vice\b|rai\b|mediaset)\b'),
 (6,'parrocchia',r'\b(parrocchi\w*|chiesa (di|parrocchiale)|basilica|santuario|rettoria)\b'),
 (6,'oratorio, Caritas, gruppi religiosi',r'\b(oratori\w*|diocesi|vicariato|caritas|cappellania|monaster\w*|convento|suore|frati|missionar\w*|azione cattolica|agesci|acli|comunione e liberazione|focolar\w*|rinnovamento nello spirito)\b'),
 (6,'altre confessioni',r'\b(chiesa (evangelica|valdese|battista|avventista|ortodossa|cristiana)|comunit[aà] (cristiana|evangelica|ebraica|islamica|buddista)|moschea|sinagoga|centro islamico|buddhist\w*|soka gakkai|sikh|induist\w*|pentecostal\w*)\b'),
 (5,'comitato di quartiere',r'\b(comitato (di )?quartiere|comitati di quartiere|cdq|c\.?d\.?q\b|comitato cittadin\w*|comitato (spontaneo|civico|residenti|per|inquilini|genitori)|comitato \w+ (nord|sud|est|ovest)|comitato acilia|comitato \w+ attiva)\b'),
 (5,'rete civica',r'\b(retake|social street|consulta|rete civica|reti civiche|polo civico|cittadinanza attiva|osservatorio|coordinamento (dei )?(comitati|cittadini))\b'),
 (0,'Municipio o Comune',r'\b(municipio|roma capitale|comune di|citt[aà] metropolitana|regione lazio|ministero|prefettura|dipartimento (cultura|politiche|attivit))\b'),
 (0,'biblioteca pubblica',r'\b(biblioteca|biblioteche di roma|bibliopoint)\b'),
 (0,'beni culturali pubblici',r'\b(sovrintendenza|soprintendenza|musei in comune|zetema|parco archeologico|polo museale)\b'),
 (0,'servizio pubblico (sanità, ambiente, trasporti, sicurezza)',r'\b(asl|ospedale|policlinico|casa della comunit[aà]|ente parco|parco regionale|roma ?natura|acea|atac|\bama\b|polizia|carabinieri|vigili del fuoco|protezione civile|croce rossa)\b'),
 (12,'università',r'\b(universit\w*|dipartimento|politecnico|luiss|lumsa|roma ?tre|sapienza|tor ?vergata|unint|link campus|istituto (superiore|nazionale))\b'),
 (12,'scuola',r'\b(liceo|istituto (comprensivo|tecnico|professionale|scolastico)|scuola (primaria|secondaria|statale|media|elementare|dell.infanzia)|\bi\.?c\.? |plesso|conservatorio|accademia di belle arti)\b'),
 (1,'grande istituzione culturale',r'\b(fondazione musica per roma|auditorium parco della musica|fondazione cinema per roma|festa del cinema|romaeuropa|teatro di roma|teatro nazionale|teatro dell.opera|palazzo delle esposizioni|accademia nazionale|santa cecilia|maxxi|galleria nazionale|scuderie del quirinale|casa del cinema|casa della memoria|casa delle letterature|casa del jazz|casa delle traduzioni|fondazione roma|fondazione \w+ \w+|bioparco)\b'),
 (3,'museo',r'\b(museo|musei|museum|pinacoteca)\b'),
 (3,'galleria o spazio espositivo',r'\b(galleria d.arte|art gallery|gallery|spazio espositivo|studio d.arte)\b'),
 (2,'teatro',r'\b(teatro|teatri|theatre|theater|teatrale)\b'),
 (2,'cinema',r'\b(cinema|cineclub|cinefor\w*|multisala|film festival)\b'),
 (2,'musica dal vivo e club',r'\b(live club|jazz club|music club|club\b|locale live|arena|anfiteatro|spazio live)\b'),
 (8,'cooperativa o impresa sociale',r'\b(cooperativa sociale|coop\.? sociale|impresa sociale|consorzio sociale)\b'),
 (8,'volontariato e assistenza',r'\b(odv|o\.d\.v|onlus|sant.egidio|casa famiglia|antiviolenza|centro antiviolenza|banco alimentare|misericordia|volontariato|solidariet\w*|assistenza|accoglienza|migranti|rifugiati|senza dimora)\b'),
 (8,'salute e disabilità',r'\b(disabil\w*|sordi|ciechi|autismo|alzheimer|malati|pazienti|sclerosi|tumor\w*|cancro|oncolog\w*|donatori|avis|admo|fidas|diabet\w*|salute|sanit\w*|psicolog\w*|psicoanali\w*|famiglie)\b'),
 (7,'centro anziani',r'\b(centro (sociale )?anziani|centro sociale anziani|\bcsa\b|terza et[aà]|over 60|seniores|anziani)\b'),
 (7,'centro sociale o spazio occupato',r'\b(csoa|centro sociale|spazio sociale|laboratorio sociale|casa del popolo|ex lavanderia|forte prenestino|kollatino)\b'),
 (7,'circolo e casa di quartiere',r'\b(circolo arci|arci\b|casa (del|di) quartiere|centro di aggregazione|centro giovani|centro giovanile|ludoteca|centro famiglie|casale)\b'),
 (9,'società o associazione sportiva',r'\b(a\.?s\.?d\.?|s\.?s\.?d\.?|polisportiv\w*|calcio|basket|pallavolo|volley|rugby|nuoto|tennis|padel|atletica|podistic\w*|running|marathon|maratona|ciclismo|bike|ciclist\w*|yoga|palestra|fitness|arti marziali|karate|judo|scherma|golf|equitazione|sportiv\w*|federazione italiana|pesca sportiva|tiro a segno|uisp|csi\b|aics)\b'),
 (10,'ambiente e natura',r'\b(wwf|legambiente|lipu|italia nostra|orto|orti|giardin\w*|natura|ambient\w*|verde|riserva|ecolog\w*|sostenibil\w*|clima|plastic)\b'),
 (10,'animali',r'\b(animali|enpa|\blav\b|oipa|canile|gattile|cani|gatti|bird)\b'),
 (11,'visite guidate e turismo',r'\b(visite guidate|visita guidata|guide turistiche|guida turistica|tour|tours|roma sotterranea|bellezze di roma|turismo|travel|viaggi|itinerari|walking|trekking|archeologia|roma segreta|romaexplorer)\b'),
 (15,'partito o lista',r'\b(partito|\bpd\b|partito democratico|\blega\b|fratelli d.italia|forza italia|movimento 5 stelle|\bm5s\b|alleanza verdi|sinistra italiana|rifondazione|italia viva|giovani democratici|lista civica|circolo pd)\b'),
 (15,'sindacato o associazione di categoria',r'\b(cgil|cisl|uil|ugl|sindacato|\busb\b|cobas|federconsumatori|codacons|confcommercio|confesercenti|cna\b|coldiretti|camera di commercio|ordine degli)\b'),
 (13,'locale (bar, ristorante, pub)',r'\b(bar|pub|bistrot|ristorante|trattoria|osteria|pizzeria|enoteca|birreria|caff[eè]|gelateria|pasticceria|cocktail)\b'),
 (13,'libreria o negozio',r'\b(libreria|bookshop|store|shop|negozio|bottega|vinile|dischi)\b'),
 (13,'impresa',r'\b(srl|s\.r\.l|spa\b|s\.p\.a|srls|snc|sas|centro commerciale|outlet|hotel|agenzia|studio\b|eventi srl|production|produzioni|management)\b'),
 (4,'compagnia, coro, banda o ensemble',r'\b(compagnia|coro|corale|banda|orchestra|ensemble|quartetto|trio|band\b|gruppo musicale|cantori)\b'),
 (4,'scuola di musica, danza o arte',r'\b(scuola di (musica|danza|teatro|ballo|canto|arte)|accademia|danza|ballet|balletto|tango|swing)\b'),
 (4,'festival o rassegna',r'\b(festival|fest\b|rassegna|premio|biennale)\b'),
 (4,'associazione culturale',r'\b(associazione culturale|ass\.? culturale|a\.?p\.?s\.?|aps\b|ets\b|circolo|collettivo|laboratorio|atelier|cultural\w*|arte|arts?\b|letter\w*|libr\w*|poesia|fotograf\w*|cinema|musica|storia|memoria|anpi|partigian\w*)\b'),
 (4,'associazione',r'\b(associazione|ass\.|associazion\w*|fondazione|ente|movimento|unione|federazione|rete|gruppo|amici d\w+|insieme|progetto)\b'),
]
FB_RULES=[
 (6,'parrocchia',r'chiesa cattolica|parrocchia|chiesa\b|luogo di culto|organizzazione religiosa|religious|church|santuario'),
 (0,'ente pubblico',r'ente (governativo|pubblico)|government|organizzazione governativa|servizio pubblico|municipio|politica.*ufficio'),
 (0,'biblioteca pubblica',r'biblioteca|library'),
 (12,'scuola o università',r'universit|scuola|college|school|istruzione|education'),
 (3,'museo o galleria',r'museo|museum|galleria d.arte|art gallery|art museum'),
 (2,'teatro, cinema o club',r'teatro|theat|cinema|movie|locale (per concerti|con musica)|concert venue|music venue|night ?club|discoteca|sala concerti|arts? centre|centro (culturale|artistico)|performance'),
 (9,'sport',r'sport|squadra|palestra|fitness|yoga|gym|stadio|campo|atlet|club sportivo'),
 (10,'ambiente e natura',r'ambient|natura|parco|park|giardin|garden|animal|environment|conservazione'),
 (11,'turismo',r'tour|turis|viaggi|travel|guida|guide'),
 (13,'locale o negozio',r'\bbar\b|ristorante|restaurant|pub\b|caff|libreria|book ?store|negozio|shop|store|pizzeria|vineria|enoteca|birreria|hotel|centro commerciale|shopping'),
 (14,'media',r'media|notizie|news|editoria|giornal|rivista|magazine|radio|tv\b|televis|emittente|blog|sito web di'),
 (15,'politica',r'partito|politic|sindacat|candidat|ufficio governativo'),
 (16,'persona',r'personaggio pubblico|artista|musicista|cantante|autore|scrittore|attore|attrice|fotografo|blogger|giornalista|creator|band\b|dj\b|regista|comico|insegnante|coach|personal'),
 (8,'terzo settore sociale',r'beneficenza|no profit|non ?profit|organizzazione di (beneficenza|volontariato)|servizio sociale|servizi sociali|charity|comunit|assistenza|salute|sanitari|medic|sostegno'),
 (4,'associazione culturale',r'organizzazione|associazione|club|comunit|arte|cultur|eventi|event|festival|produzione'),
]
RUNTS_TEMI={'cultura':4,'arte':4,'sport':9,'ambiente':10,'sociale':8,'sanit':8,'salute':8,'disabil':8,'istruzione':12,'formazione':12,'turismo':11,'religio':6,'animali':10}
REG={'comitato_quartiere':(5,'comitato di quartiere'),'parrocchia':(6,'parrocchia'),'centro_anziani':(7,'centro anziani'),'centro_culturale':(4,'associazione culturale'),
     'teatro':(2,'teatro'),'biblioteca':(0,'biblioteca pubblica'),'museo':(3,'museo'),'galleria':(3,'galleria o spazio espositivo'),'istituzione':(0,'ente pubblico'),
     'politico':(15,'partito o lista'),'mercato_rionale':(13,'mercato'),'pro_loco_consorzio':(5,'pro loco o consorzio'),'istituto_comprensivo':(12,'scuola'),
     'luogo_di_culto':(6,'altre confessioni'),'ente_nazionale_o_regionale':(8,'ente nazionale'),'associazione_locale':(4,'associazione'),'associazione':(4,'associazione'),
     'luogo_pubblico':(0,'luogo pubblico'),'tematico_non_locale':(4,'associazione tematica')}
def classify(r):
    nm=' '.join([r['nome']]+r.get('altri_nomi',[])); n=norm(nm)
    for m,sub,rx in NAME_RULES:
        if re.search(rx,n) and not (m==13 and re.search(r'impresa sociale|cooperativa sociale',n)) and not (m==3 and 'alberto sordi' in n):
            if sub=='associazione': break   # generico: si prova con categorie e registro prima di accettarlo
            return MACRO[m],sub,'nome'
    cats=' '.join(str(c) for c in (r.get('categorie_facebook') or [])+[r.get('categoria_google') or '']).lower()
    if cats.strip():
        for m,sub,rx in FB_RULES:
            if re.search(rx,cats): return MACRO[m],sub,'categoria Facebook o Google'
    t=r.get('tipo_registro') or r.get('tipo_wiki')
    if t in REG: m,sub=REG[t]; return MACRO[m],sub,'tipo nel registro fonti'
    tm=norm(r.get('temi_runts'))
    for k,m in RUNTS_TEMI.items():
        if k in tm: return MACRO[m],'ente del terzo settore','temi RUNTS'
    if r.get('sezione_runts'): return MACRO[8] if re.search(r'volontariato|odv',norm(r['sezione_runts'])) else MACRO[4],'ente del terzo settore','sezione RUNTS'
    if re.search(r'\b(associazione|ass\.|associazion\w*|fondazione|movimento|unione|federazione|rete|gruppo|amici|progetto)\b',n): return MACRO[4],'associazione','nome'
    about=norm(' '.join(str(x) for x in [r.get('intro_facebook'),r.get('_site_desc')] if x))
    if about:
        for m,sub,rx in NAME_RULES:
            if sub in ('associazione',): continue
            if re.search(rx,about): return MACRO[m],sub,'testo di presentazione'
        for m,sub,rx in FB_RULES:
            if re.search(rx,about): return MACRO[m],sub,'testo di presentazione'
    toks=[w for w in re.findall(r"[A-ZÀ-Ý][a-zà-ÿ']+",r['nome'])]
    if 2<=len(r['nome'].split())<=3 and len(toks)==len(r['nome'].split()): return MACRO[16],'persona (nome e cognome)','forma del nome'
    return MACRO[17],'','nessun segnale'

ATT=[('teatro',r'\b(teatr\w*|spettacol\w*|prosa|commedia|monologo|drammaturg\w*|messa in scena|marionett\w*|burattin\w*)'),
     ('musica',r'\b(concert\w*|musica\w*|coro|corale|orchestra|band|jazz|live|dj\b|cantautor\w*|recital|lirica|opera\b|canzon\w*|rock|blues)'),
     ('cinema',r'\b(cinema|film|proiezion\w*|cineforum|documentari\w*|cortometragg\w*)'),
     ('arte e mostre',r'\b(mostr[ae]|esposizion\w*|arte|artist\w*|pittur\w*|fotografi\w*|scultur\w*|vernissage|installazion\w*|illustrazion\w*)'),
     ('libri e letture',r'\b(libr[oi]|letteratur\w*|lettur[ae]|reading|presentazion\w*|autor[ei]|poesi\w*|book|scrittor\w*|biblioteca|romanzo)'),
     ('incontri e dibattiti',r'\b(incontr[oi]|conferenz\w*|dibattit\w*|convegn\w*|seminari\w*|talk|tavola rotonda|assemblea|lezion[ei] apert\w*)'),
     ('laboratori e corsi',r'\b(laborator\w*|workshop|cors[oi]|lezion\w*|formazion\w*|masterclass)'),
     ('danza',r'\b(danz\w*|ball[oi]|tango|swing|balletto|coreograf\w*)'),
     ('sport e movimento',r'\b(sport\w*|torne[oi]|gar[ae]\b|corsa|camminat\w*|yoga|calcio|basket|bici\w*|pedalat\w*|maratona|partita|ginnastica|nuoto|tennis|padel)'),
     ('ambiente e natura',r'\b(ambient\w*|natur\w*|verde|pulizi\w*|orto|alber\w*|piantumazion\w*|clima|rifiuti|riciclo|plastic\w*|parco)'),
     ('visite e passeggiate',r'\b(visit[ae]|passeggiat\w*|tour|itinerar\w*|trekking|escursion\w*|archeolog\w*)'),
     ('feste e mercatini',r'\b(fest[ae]\b|sagr[ae]|carnevale|halloween|natal\w*|befana|mercatin\w*|fiera|patronal\w*|capodanno|street food)'),
     ('religione e spiritualità',r'\b(mess[ae]\b|preghier\w*|catechesi|veglia|liturgi\w*|ritiro|novena|rosario|adorazion\w*|spiritual\w*|vangelo|santo\b)'),
     ('solidarietà e sociale',r'\b(solidal\w*|raccolt[ae]|volontar\w*|donazion\w*|sangue|inclusion\w*|migrant\w*|povert\w*|beneficenz\w*|fondi\b|accoglienz\w*)'),
     ('salute e benessere',r'\b(salute|benessere|prevenzion\w*|screening|psicolog\w*|medic\w*|sanitar\w*|terapi\w*|mindfulness|meditazion\w*)'),
     ('storia e memoria',r'\b(stori[ac]\w*|memoria|resistenza|anpi|liberazione|commemorazion\w*|anniversari\w*|shoah)'),
     ('partecipazione civica',r'\b(comitat\w*|cittadin\w*|quartier\w*|consulta|municipio|partecipazion\w*|bene comune|decoro|riqualificazion\w*|petizion\w*)'),
     ('cibo e degustazioni',r'\b(degustazion\w*|cena|pranzo|aperitiv\w*|vin[oi]\b|enogastronom\w*|polentata|cucina|food)'),
     ('scienza e tecnologia',r'\b(scienz\w*|tecnolog\w*|astronom\w*|digital\w*|coding|robot\w*|maker)')]
PUB=[('bambini e famiglie',r'\b(bambin\w*|famigli\w*|ragazz\w*|infanzia|kids|genitor\w*|piccol[ie])\b'),('anziani',r'\b(anzian\w*|terza et|over ?60|nonn\w*|senior)'),
     ('giovani',r'\b(giovan\w*|student\w*|adolescent\w*|universitar\w*)'),('donne',r'\b(donn[ae]|femminil\w*|femminism\w*)'),('persone con disabilità',r'\b(disabil\w*|sordi|ciechi|autism\w*|inclusiv\w*)'),
     ('migranti e nuovi cittadini',r'\b(migrant\w*|rifugiat\w*|stranier\w*|intercultur\w*|italiano per stranieri)')]
def families(text,weight,c):
    t=text.lower()
    for k,rx in ATT:
        n=len(re.findall(rx,t))
        if n: c[k]+=min(n,5)*weight
def legal_form(r):
    n=norm(r['nome']); s=norm(r.get('sezione_runts'))
    for rx,lab in [(r'\bodv\b|o d v|organizzazione di volontariato|volontariato',"organizzazione di volontariato"),(r'\baps\b|a p s|promozione sociale',"associazione di promozione sociale"),
                   (r'\basd\b|a s d|ssd\b|s s d|sportiva dilettantistica',"associazione o società sportiva dilettantistica"),(r'cooperativa sociale|coop sociale','cooperativa sociale'),
                   (r'impresa sociale','impresa sociale'),(r'\bonlus\b','onlus'),(r'\bfondazione\b','fondazione'),(r'\bets\b|terzo settore','ente del terzo settore'),
                   (r'\bsrl\b|s r l|srls|\bspa\b|s p a|\bsnc\b|\bsas\b','impresa'),(r'\bparrocchia\b','parrocchia'),(r'\bmunicipio\b','Municipio di Roma Capitale')]:
        if re.search(rx,n) or re.search(rx,s): return lab
    return None
ART={'Istituzioni pubbliche':'un ente pubblico','Grandi istituzioni culturali e fondazioni':'una grande istituzione culturale','Teatri, cinema e spazi di spettacolo':'uno spazio di spettacolo',
     'Musei, gallerie e spazi espositivi':'uno spazio espositivo','Associazioni culturali e artistiche':'una realtà associativa culturale','Comitati di quartiere e reti civiche':'una realtà civica di quartiere',
     'Parrocchie e realtà religiose':'una realtà religiosa','Centri sociali, centri anziani e spazi di comunità':'uno spazio di comunità','Terzo settore sociale e sanitario':'un ente del terzo settore sociale',
     'Sport e movimento':'una realtà sportiva','Ambiente, natura e animali':'una realtà ambientalista','Turismo e visite guidate':'un operatore di visite guidate e turismo',
     'Scuole, università e formazione':'una scuola o istituzione formativa','Locali e attività commerciali':'un\'attività commerciale','Intermediari: biglietterie, aggregatori e media':'un intermediario (biglietteria, aggregatore o media)',
     'Politica e sindacati':'una realtà politica o sindacale','Persone (artisti, autori, guide)':'una persona (artista, autore o guida)','Non classificato':'un promotore'}
def nice_zone(z,PAGES): return PAGES.get(z,z) if z else None
def ad(x): return 'ad' if str(x or '')[:1].lower()=='a' else 'a'   # d eufonica: «ad Acilia»
def describe(r,E,PAGES,site):
    r['_site_desc']=' '.join(x for x in [(site or {}).get('descrizione_meta'),(site or {}).get('og_description'),(site or {}).get('titolo')] if x)
    macro,sub,why=classify(r); r['categoria'],r['sottocategoria'],r['categoria_da']=macro,sub,why
    r.pop('_site_desc',None)
    evs=[E[i] for i in r['eventi_idx']]
    c=collections.Counter(); families(' '.join(e['t'] for e in evs),2,c)
    about=' '.join(x for x in [r.get('intro_facebook'),(site or {}).get('descrizione_meta'),(site or {}).get('og_description'),(site or {}).get('testo_chi_siamo')] if x)
    families(about,1,c); families(' '.join(str(x) for x in (r.get('categorie_facebook') or [])+[r.get('temi_runts') or '',r.get('categoria_google') or '']),2,c)
    att=[k for k,v in c.most_common(4) if v>=2][:3] or [k for k,v in c.most_common(2)]
    pub=[k for k,rx in PUB if re.search(rx,(about+' '+' '.join(e['t'] for e in evs)).lower())]
    r['attivita']=att; r['pubblico']=pub
    pq=collections.Counter(r['pagine_qn']); mu=collections.Counter(r['municipi'])
    nat=re.search(r'\b(nazional\w*|italian[ao]|italia|europe\w*|internazional\w*)\b',norm(r['nome'])) or 'nazionale' in norm(r.get('verdetto_censimento'))
    if nat: amb='nazionale o internazionale'
    elif macro in ('Istituzioni pubbliche','Grandi istituzioni culturali e fondazioni','Intermediari: biglietterie, aggregatori e media') or len(mu)>=3: amb='cittadino'
    elif macro=='Comitati di quartiere e reti civiche' or len(pq)<=1: amb='di quartiere'
    else: amb='di più quartieri'
    r['ambito']=amb
    lf=legal_form(r)
    has_seat=bool(r.get('indirizzo')) and bool(r.get('zona_sede'))
    sede=nice_zone(r.get('zona_sede') if has_seat else (pq.most_common(1)[0][0] if pq else r.get('zona_sede')),PAGES); mun=(r.get('municipio_sede') if has_seat else None) or (mu.most_common(1)[0][0] if mu else None)
    if amb in ('cittadino','nazionale o internazionale') and not has_seat: sede=None
    dove=(f" di {sede}" if amb=='di quartiere' else f" con sede {ad(sede)} {sede}") if sede and has_seat else (f" attivo {ad(sede)} {sede}" if sede else '')
    dove+=f" (Municipio {mun})" if mun and dove else ''
    generic=sub in ('associazione','ente del terzo settore','terzo settore sociale','') or macro=='Non classificato'
    if generic and lf: chi=lf[0].upper()+lf[1:]
    elif sub: chi=sub[0].upper()+sub[1:]+(f" ({lf})" if lf and lf.split()[0] not in sub else '')
    else: chi=macro
    breve=f"{chi}{dove}"+(f": {', '.join(att)}" if att else '')+(f"; per {', '.join(pub[:2])}" if pub else '')+'.'
    r['descrizione_breve']=re.sub(r'\s+',' ',breve)[:220]
    tipi=collections.Counter(); [families(e['t'],1,tipi) for e in evs]
    srcs=collections.Counter(e['src'] for e in evs)
    canali_ev={'Facebook':'eventi Facebook','Facebook (post)':'post Facebook','culture.roma.it':'culture.roma.it','sito della fonte':'il proprio sito','Roma Today':'Roma Today'}
    d1=min((e['d1'] for e in evs),default=None); d2=max((e['d2'] for e in evs),default=None)
    parts=[f"{r['nome']} è {ART.get(macro,'un promotore')}"+(f" ({lf})" if lf else '')+(f", {sub}" if sub and sub not in (lf or '') else '')+((f", con sede {ad(sede)} {sede}" if has_seat else f", attivo soprattutto {ad(sede)} {sede}") if sede else '')+(f" (Municipio {mun})" if mun and sede else '')+(f", {r['indirizzo']}" if has_seat else '')+'.']
    if att: parts.append(f"Si occupa soprattutto di {', '.join(att)}"+(f", con un'attenzione a {', '.join(pub)}" if pub else '')+'.')
    if r.get('temi_runts') and norm(r['temi_runts']) not in ('altro','altri','n d'): parts.append(f"Nel Registro unico del terzo settore dichiara: {r['temi_runts']}.")
    parts.append(f"Ambito {amb}. Nel calendario noto al 25 ottobre 2026 ha {r['n_eventi']} event{'o' if r['n_eventi']==1 else 'i'}"+(f" tra il {d1} e il {d2}" if d1 and d2 and d1!=d2 else (f" il {d1}" if d1 else ''))
                 +(f" ({', '.join(k for k,_ in tipi.most_common(3))})" if tipi else '')+(f", nelle pagine {', '.join(nice_zone(z,PAGES) for z,_ in pq.most_common(4))}" if pq else '')
                 +f"; li annuncia con {', '.join(canali_ev.get(s,s) for s,_ in srcs.most_common())}.")
    on=[x for x,k in (('sito web','sito'),('Facebook','facebook'),('Instagram','instagram'),('YouTube','youtube'),('X','x'),('TikTok','tiktok'),('LinkedIn','linkedin')) if r.get(k)]
    if on: parts.append('Presente online con '+', '.join(on)+(f" ({r['follower']} follower su Facebook)" if r.get('follower') else '')+'.')
    auto=r.get('intro_facebook') or (site or {}).get('descrizione_meta') or (site or {}).get('og_description') or (site or {}).get('testo_chi_siamo')
    if auto: parts.append(f"Come si presenta: «{re.sub(chr(10),' ',str(auto)).strip()[:600]}»"+(' (profilo Facebook)' if r.get('intro_facebook') else ' (sito)')+'.')
    r['descrizione_lunga']=' '.join(parts)
    r['autodescrizione_fonte']='profilo Facebook' if r.get('intro_facebook') else ('sito' if auto else None)
    return r

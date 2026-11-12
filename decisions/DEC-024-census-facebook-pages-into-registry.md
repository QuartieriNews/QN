# DEC-024 — Censimento delle pagine Facebook di associazioni: cosa entra nel registro e come si continua a cercare su Facebook

Status: DECIDED (11 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: la schedulazione della rilettura del punto 3, finché DEC-004 (il tetto di eventi per
corsa, ancora aperta) non è decisa. Mentre era aperta bloccava la promozione delle candidate del
censimento del 24 ottobre 2026 nel registro fonti v2, il flusso continuo di ricerca eventi su
Facebook e la rilettura delle pagine dormienti.

Context: il 24 ottobre 2026 le 1.169 pagine Facebook di associazioni fornite dall'owner
sono state lette con Apify (dati di pagina, eventi futuri, post degli ultimi sei mesi) e
sul loro sito. Esito nella wiki delle fonti eventi (`docs/wiki/fonti-eventi/censimento-pagine.md`, nella
PR #21) e nel foglio `associazioni_fonti.xlsx` su Drive. Solo 19 pagine su 1.169 pubblicano eventi
futuri su Facebook (verificato con due lettori diversi); 186 annunciano eventi nei post;
83 siti mostrano date future; 275 pagine sono dormienti. Il verdetto automatico propone,
non decide: la decisione tenere/scartare è del registro e quindi dell'owner (DEC-102 per
la raccolta manuale; DEC-104 per i ruoli).

Question 1 — Quali verdetti del censimento entrano nel registro fonti come «tenere»?
  Options:
  a) tutti i «rientra» (390 pagine: eventi futuri su Facebook, calendario sul sito, date
     recenti sul sito, pagina eventi sul sito, annunci di eventi nei post) entrano come
     «tenere», con `dove_cercare` già compilato; i «da valutare» restano in coda;
  b) solo i «rientra» con una prova forte (eventi futuri su Facebook, date future sul sito:
     68 pagine) entrano subito; gli altri «rientra» (322) entrano dopo un mese di lettura
     dei siti che ne confermi l'attività;
  c) nessuna promozione automatica: l'owner scorre `censimento-pagine.md` e decide pagina
     per pagina.
  Claude recommendation: b). La prova forte vale la promozione; «pagina eventi sul sito
  senza date leggibili» e «annunci nei post» sono indizi, e un mese di lettura con
  `tools/fonti/leggi_eventi_siti.py` li conferma o li smentisce senza costo.

Question 2 — Le 24 pagine di organizzazioni politiche e le 54 attività commerciali locali.
  Options:
  a) politiche: entrano solo per iniziative pubbliche aperte (assemblee, presidi, feste),
     mai per propaganda; commerciali: entrano solo se la pagina annuncia eventi (8 lo
     fanno nei post) — regola editoriale esplicita in `prompts/EDITORIAL_FILTER.md`;
  b) politiche escluse in blocco; commerciali escluse in blocco;
  c) tutte in coda «da valutare» fino a una regola generale sulle fonti di parte.
  Claude recommendation: a); è coerente con l'EDITORIAL_FILTER (organizzatore di
  comunità = interesse locale) e lascia fuori la propaganda per contenuto, non per
  categoria.

Question 3 — Facebook come canale continuo di scoperta.
  DEC-102 prevede la raccolta manuale degli URL. Il 24 ottobre gli eventi futuri delle
  1.169 pagine del censimento sono stati letti con l'Actor `unseenuser/fb-events`
  (`pageUrls`, a pagamento per evento restituito, 0,18 $ in tutto per le 1.169 pagine) senza accesso diretto dall'ambiente del
  progetto; la stessa lettura per parole chiave ha reso pochissimo.
  Options:
  a) lettura mensile per parole chiave via Apify, con gli organizzatori nuovi che entrano
     nel censimento come candidate (stesso percorso del 24 ottobre); gli URL degli eventi
     restano raccolti dall'owner per la pubblicazione (DEC-102 invariata nella parte
     «chi raccoglie»);
  b) nessuna lettura per parole chiave: solo le pagine già nel registro, lette con
     `pageUrls` ogni due settimane (0,18 $ per 1.169 pagine);
  c) entrambe: parole chiave una volta al mese per scoprire, `pageUrls` ogni due settimane
     per seguire.
  Claude recommendation: b), con una lettura per parole chiave al massimo trimestrale come
  controllo. La prova del 24 ottobre (139 ricerche con due lettori, 60 eventi romani, 0
  organizzatori nuovi con almeno due eventi a Roma; `docs/sources/FONTI_EVENTI_STATO_2026-10-24.md`, nella PR #21
  §5) dice che il motore di ricerca eventi di Facebook non scopre quasi nulla: la
  scoperta passa dagli organizzatori citati dagli eventi già letti, dagli elenchi
  istituzionali e dalle liste raccolte a mano. Tetto di spesa mensile scritto nel
  workflow (DEC-004 insegna: il tetto va deciso prima che la schedulazione parta).

Question 4 — Le 275 pagine dormienti.
  Options: a) rilettura a marzo 2027 (sei mesi); b) mai, salvo segnalazione; c) rilettura
  a gennaio 2027.
  Claude recommendation: a).

Impact: Q1 decide quante fonti nuove entrano nella wiki come «tenere» (68 o 390) e
quindi quante pagine QN guadagnano una fonte: oggi 41 zone QN hanno almeno una pagina
che rientra. Q3 decide il costo mensile (meno di 1 $ per le pagine seguite, circa 1 $ per
una lettura per parole chiave) e il rapporto con DEC-102.

Owner's answers (sessione del builder, 11 novembre 2026, una domanda alla volta con le
opzioni qui sopra): Q1 «Solo prova forte», Q2 «Escludile tutte», Q3 «Rileggere le pagine»,
Q4 «Mai». Domande successive, nella revisione della PR #46:
- dopo il secondo giro: 4 comitati di quartiere e 1 associazione locale che Facebook classifica
  come organizzazione politica o attività commerciale; risposta «Tienili dentro» (conta che cosa
  è l'organizzazione, non l'etichetta di Facebook);
- dopo il terzo giro: un evento organizzato da un bar o da un partito, con l'URL raccolto a mano
  dall'owner; risposta «Solo il registro», con questa spiegazione: «Le pagine restano fuori dal
  registro e non le rileggiamo. Un evento che raccogli tu lo giudica il filtro, come oggi: il
  concerto nel pub può uscire. Il filtro non cambia.»;
- dopo il quarto giro: le pagine «rientra» che il registro segna `locale` sono associazioni che
  Facebook chiama «Local business»; risposta «Quinto giro», cioè correggere la decisione:
  un'attività commerciale si esclude per quello che è, non per l'etichetta di Facebook;
- nello stesso giro: 7 pagine «tenere» del registro con il `tipo` `politico` scritto a ottobre,
  che il censimento non ha letto (3 comitati elettorali o di un candidato, 4 comitati su un
  tema); risposta «Tutte e 7» (vale il `tipo` `politico` scritto a ottobre).

Decision:
1. **Q1 — b).** Entrano subito come «tenere» le pagine con una prova forte (eventi futuri
   su Facebook, date future sul sito); le altre «rientra» entrano dopo un mese di lettura dei
   loro siti, se la lettura ne conferma l'attività. L'esclusione del punto 2 vale prima di
   questo punto, e prima di promuovere una pagina si controlla che cosa è l'organizzazione
   (punto 2). Contate nel registro della PR #21 (`docs/wiki/fonti-eventi/fonti_eventi.json`,
   388 «rientra»): 68 hanno una prova forte e 320 no. Delle 68 il punto 2 non ne esclude
   nessuna: le 5 che il registro segna `locale` sono associazioni; entrano subito 68 pagine.
   Delle 320 sono politiche due: `S-FE-0369`, un comitato referendario che è anche fra le 28
   del punto 2, e `S-EV-0912`, un'associazione di area politica che il registro segna `locale`.
   Le altre 11 segnate `locale` sono associazioni: le candidate dopo il mese sono 318.
   La lettura del mese parte dagli indirizzi del sito in `dove_cercare`
   (`tools/fonti/leggi_eventi_siti.py`, nella PR #21). Delle 318, 36 non ne hanno nessuno: sono
   «rientra» solo per gli annunci nei post di Facebook. La lettura dei siti non le può
   confermare: restano candidate e non entrano come «tenere», finché l'owner non sceglie per
   loro un'altra conferma.
   La tabella del censimento conta 390 «rientra» perché conta le righe dell'elenco letto, non le
   pagine: tre pagine vi compaiono due volte e il registro ne tiene una sola, con la prima
   lettura (`S-EV-0575`, `S-EV-0777`, `S-EV-0855`); le due righe «rientra» in più sono seconde
   letture di queste pagine. Una pagina segue un percorso solo, con quello che hanno trovato
   tutte le sue letture: è «rientra» se una lettura lo è, e ha una prova forte se una lettura ne
   ha una. `S-EV-0575` è già fra le 318.
   `S-EV-0777` e `S-EV-0855` il registro le segna «da valutare»; se la loro seconda lettura nel
   foglio del censimento è «rientra», `S-EV-0777`, che ha date future sul sito, entra subito (69
   pagine) e `S-EV-0855` si aggiunge alle candidate del mese (319).
2. **Q2 — b).** Restano fuori dal registro le organizzazioni politiche (partiti, liste,
   candidati, comitati elettorali e referendari) e, fra le pagine del censimento, le attività
   commerciali (negozi, bar, palestre). Conta che cosa è l'organizzazione, non l'etichetta di
   Facebook (prima e terza domanda successiva): i comitati di quartiere e le associazioni restano
   fonti anche quando Facebook li chiama politici o commerciali.
   - **Pagine del censimento.** Il `tipo` del registro non basta, perché lo strumento lo copia
     dalla categoria di Facebook (`FB_CATEGORIA_TIPO` in `tools/wiki/build_fonti_eventi.py`,
     nella PR #21: «Local business» diventa `locale`, le categorie politiche
     `organizzazione_politica`): che cosa è l'organizzazione si controlla sul nome e sul sito.
     All'11 novembre nel censimento non c'è nessuna attività commerciale. Sono due gruppi
     distinti di associazioni o comitati che Facebook chiama «Local business»: le 54 pagine con
     il verdetto «locale» del censimento, e le 17 con un verdetto «rientra» e il `tipo` `locale`
     (il punto 1 le conta già fra le 68 e le 320). Quelli politici si escludono come politici
     (`S-EV-0912`; `S-FE-0343` e `S-FE-0366`, che sono fra le 28 qui sotto). Delle 54, tolte le
     2 politiche, 6 sono già «tenere». Le altre 46 non sono «rientra»: il censimento non ha
     trovato eventi futuri, né su Facebook né sul sito, né date sul sito negli ultimi sei mesi,
     e 40 non hanno nemmeno post recenti. Hanno la sorte delle pagine lette allo stesso modo: 40
     quella delle dormienti (punto 4), 6 quella delle «attive su Facebook, senza annunci di
     eventi». Nessuna entra come «tenere» e la rilettura del punto 3 non le legge.
   - **Pagine già «tenere».** Vale il `tipo` scritto nel registro del 13 ottobre
     (`registro.tipo`, quarta domanda successiva): le 28 con il `tipo` `politico` passano a
     «scartare» con il motivo «DEC-024 Q2», non si cancellano e tengono la loro storia. Nessuna
     ha il `tipo` `locale`. I luoghi e gli organizzatori commerciali che il registro ha da altre
     fonti (club, cinema, fiere, un mercato, una libreria) non erano nella domanda Q2, che
     parlava delle pagine del censimento, e restano: il luogo non decide da solo
     (`prompts/EDITORIAL_FILTER.md`, «`venue_nature` is a prior, not a shortcut»).
   - **Rilettura ed eventi.** La rilettura del punto 3 salta le pagine escluse. L'esclusione vale
     per il registro, non per gli eventi (seconda domanda successiva): un evento che l'owner
     raccoglie a mano (DEC-102) lo giudica `prompts/EDITORIAL_FILTER.md`, che non cambia, anche
     quando l'organizzatore è un partito o un'attività commerciale.
3. **Q3 — b), con il controllo trimestrale della raccomandazione.** All'owner l'opzione è
   stata posta così: «Ogni due settimane rileggo le pagine del registro. Una volta ogni tre
   mesi faccio una ricerca per parole chiave, solo come controllo». Le pagine del registro si
   rileggono ogni due settimane con `pageUrls`; una lettura per parole chiave al massimo ogni
   tre mesi, come controllo. Tetto di spesa mensile scritto nel workflow prima che la
   schedulazione parta; la schedulazione aspetta anche DEC-004, ancora aperta, che fissa il
   tetto di eventi per corsa (Blocks, qui sopra). DEC-102 resta com'è, come diceva la domanda all'owner («Gli URL degli
   eventi da pubblicare restano raccolti da te, come prevede DEC-102»): la rilettura e la
   ricerca dicono quali pagine sono attive e quali eventi annunciano, aggiornano lo stato delle
   pagine nel registro e arrivano all'owner come elenco. Non alimentano il canale C: un evento
   si pubblica solo dagli URL che l'owner raccoglie a mano (DEC-102; `docs/pilota/CONTRATTI.md`,
   «C · Eventi da Facebook», URL delle fonti).
4. **Q4 — b).** Le 275 pagine dormienti non si rileggono, salvo segnalazione. Il README della
   wiki nella PR #21 (`docs/wiki/fonti-eventi/README.md`) dice ancora che si rileggono a marzo
   2027, che era l'opzione a): quando la #21 si aggiorna, quel paragrafo rimanda a questo punto.

Decided by: Owner · Date: 11 novembre 2026 · Affected components: registro fonti v2, `docs/wiki/fonti-eventi`,
`workflows/scrape-fb-events-rome.json` (Q3),
`tools/fonti/leggi_eventi_siti.py` (Q1b).

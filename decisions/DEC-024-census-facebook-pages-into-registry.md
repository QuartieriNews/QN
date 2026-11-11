# DEC-024 — Censimento delle pagine Facebook di associazioni: cosa entra nel registro e come si continua a cercare su Facebook

Status: DECIDED (11 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: registro fonti v2 (promozione delle candidate del censimento del 24 ottobre 2026);
il flusso continuo di ricerca eventi su Facebook; la rilettura delle pagine dormienti.

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
  (`pageUrls`, 0,0035 $ l'uno, 0,18 $ in tutto) senza accesso diretto dall'ambiente del
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
  organizzatori nuovi con almeno due eventi a Roma; `docs/sources/FONTI_EVENTI_STATO_2026-10-24.md`
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
Q4 «Mai».

Decision:
1. **Q1 — b).** Entrano subito come «tenere» le 68 pagine con una prova forte (eventi futuri
   su Facebook, date future sul sito). Le altre 322 «rientra» entrano dopo un mese di
   lettura dei loro siti, se la lettura ne conferma l'attività.
2. **Q2 — b).** Le pagine di organizzazioni politiche (24) e le attività commerciali (54)
   restano fuori dal registro in blocco, eventi compresi.
3. **Q3 — b).** Le pagine del registro si rileggono ogni due settimane con `pageUrls`; una
   lettura per parole chiave al massimo ogni tre mesi, come controllo. Tetto di spesa
   mensile scritto nel workflow prima che la schedulazione parta. DEC-102 resta com'è: gli
   URL degli eventi da pubblicare li raccoglie l'owner.
4. **Q4 — b).** Le 275 pagine dormienti non si rileggono, salvo segnalazione.

Decided by: Owner · Date: 11 novembre 2026 · Affected components: registro fonti v2, `docs/wiki/fonti-eventi`,
`prompts/EDITORIAL_FILTER.md` (Q2), `workflows/scrape-fb-events-rome.json` (Q3),
`tools/fonti/leggi_eventi_siti.py` (Q1b).

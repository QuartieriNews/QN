# DEC-045 — Canale B: come si legge GDELT nella misura di due settimane (DEC-039, punto 4)

Status: DECIDED (19 novembre 2026, owner nella sessione del coordinatore, il servizio di ricerca
al posto dei file, punto 1; 20 novembre 2026, verso le 00:44 di Roma, owner nella sessione del
coordinatore, il 429, punto 2; registrata dal builder del canale B nella notte fra il 19 e il 20
novembre 2026)
Supersedes in part: DEC-039, punto 4, solo nel modo di leggere GDELT. «GDELT, dai suoi file pubblici
ogni 15 minuti, solo per titolo, link e ora» diventa il servizio di ricerca gratuito di GDELT, con
gli stessi dati. Il resto del punto 4 resta valido: la prova gratuita, la misura di due settimane,
i numeri che il coordinatore porta all'owner, la scelta dell'owner se pagare, Google News escluso,
nessun browser automatico. DEC-039 non si riapre; riceve un rimando sotto la riga `Status:`
(`decisions/README.md`, regola 2). Il punto 2 (il 429) non tocca DEC-039, che di 429 non parla: è
un'eccezione, per GDELT soltanto, alla regola della raccolta (`docs/pilota/CONTRATTI.md`, sezione
7 B, «Raccolta»), che per tutte le altre fonti resta com'è.
Blocks: niente. La misura è in staging dalla notte del 19 novembre 2026.

Question: DEC-039, punto 4, fa leggere GDELT «dai suoi file pubblici ogni 15 minuti, solo per
titolo, link e ora (DEC-108)». Che cosa si legge se quei file non reggono su n8n? E quando GDELT
risponde 429, la misura si ferma come una fonte della raccolta?

Contesto:
- I file da 15 minuti di GDELT dove stanno gli articoli in italiano (il flusso «translation») sono di
  5,6 MB compressi la notte (17,7 MB di testo) e di 11–15 MB di giorno, cioè di giorno 35–48 MB di
  testo per ogni quarto d'ora, 96 file al giorno. Il piano Starter di n8n ha 640 MiB di memoria
  per tutta l'istanza, di cui circa 180 per il programma, e 2.500 esecuzioni al mese per tutti i
  canali. I numeri e la loro data arrivano con la PR di B che segue questa, in `workflows/README.md`,
  «La misura di GDELT».
- La prima corsa di `staging_B_gdelt_misura`, il 19 novembre 2026 alle 23:28 UTC, ha avuto un 429
  alla prima ricerca, dieci secondi dopo `robots.txt`. Per la regola della raccolta l'host si è
  fermato, e la misura con lui. Lo stesso servizio aveva risposto 429 anche dalla sandbox, a 8
  secondi fra due richieste. Già a ottobre `docs/sources/CRONACA_PROCESSO_2026-10.md`, sezione 5.2,
  registrava che il servizio «risponde 429 (troppe richieste da un indirizzo condiviso)»; la sezione
  5.3, punto 5, suggeriva «GDELT da un indirizzo non condiviso».

Options:
1. 19 novembre, verso le 23:50 di Roma, la domanda del coordinatore all'owner: «La tua scelta del
   18/11 dice di leggere GDELT dai suoi file pubblici, che escono ogni 15 minuti. Quei file
   contengono le notizie di tutto il mondo e possono pesare decine di megabyte ciascuno: il nostro
   motore dei flussi potrebbe non reggerli ogni quarto d'ora. GDELT ha anche un servizio di ricerca
   gratuito, con gli stessi dati (titolo, link, ora), a cui si chiedono direttamente le testate
   italiane e i nomi dei quartieri. Se i file non reggono, posso usare la ricerca?». Le opzioni:
   - «Sì, usa la ricerca (Consigliato)»: «Stessi dati e stessa regola (solo titolo, link e ora),
     letti in modo più leggero. Lo scrivo nella decisione come lettura tua di stanotte.»;
   - «No, solo i file»: «Se i file non reggono mi fermo e domattina ti porto le opzioni. La misura
     parte più tardi.»
2. 20 novembre, verso le 00:44 di Roma, la domanda del coordinatore all'owner, in inglese come la
   sessione: «News measure: the GDELT reader is built, but on its first run GDELT answered "too
   many requests" (429) to the very first search, after a 10-second wait. Under the news rules, a
   429 stops that source until you say otherwise, so the measure is switched off. It is probably a
   limit GDELT counts per address: the flows' server is shared with many other customers, and our
   own sandbox got the same answer. How do we go on?». Le opzioni:
   - «Retry, stop after 6 (Recommended)»: «For GDELT only, a 429 ends that run instead of stopping
     the source. The source stops only after 6 runs in a row with a 429, and you get an alert. A
     small code change in the same PR. I would also draft a short email for you to ask GDELT for
     access.»;
   - «Ask GDELT first»: «The measure stays off. I draft an email to GDELT asking for access, and
     you send it. It starts when they answer.»;
   - «Read the big files instead»: «The 15-minute files work without the search limit, but are too
     heavy for our flows plan (35-48 MB per quarter hour). Only with a bigger plan, or run outside
     the flows.»;
   - «Drop GDELT»: «No second source from closed newspapers for now. Mostly official news stay
     publishable.»

Claude recommendation:
- Punto 1: «Sì, usa la ricerca» era l'opzione consigliata dal coordinatore.
- Punto 2: «Retry, stop after 6» era consigliata. Il builder l'aveva proposta nella sua bozza di
  `OWNER_DECISION_REQUIRED` («Per GDELT un 429 chiude la corsa, non ferma l'host»), da fare insieme a
  una richiesta a GDELT.

Owner's words:
- 19 novembre 2026: l'owner ha scelto «Sì, usa la ricerca (Consigliato)». Il mandato della notte
  (`MANDATO_NOTTE_2026-11-19.md` su Drive, nella cartella di passaggio) la registra con parole del
  coordinatore: «GDELT, se i file ogni 15 minuti non reggono su n8n: «Sì, usa la ricerca» (il
  servizio di ricerca gratuito di GDELT, stessi dati: solo titolo, link, ora). Lettura dell'owner di
  DEC-039, punto 4, da scrivere nella PR di B.»
- 20 novembre 2026, verso le 00:44 di Roma: l'owner ha scelto «Retry, stop after 6 (Recommended)».

## Regola

1. **Il servizio di ricerca al posto dei file.** La misura di DEC-039, punto 4, legge il servizio
   di ricerca gratuito di GDELT (DOC 2.0 API), non i file da 15 minuti: stessi dati, solo titolo,
   link e ora, e mai l'articolo (DEC-108). Le ricerche, il ritmo, le finestre, i file e la fine
   della misura li fissa la riga «Misura GDELT» di `docs/pilota/CONTRATTI.md`, sezione 7 B, che
   arriva con la PR di B che segue questa.
2. **Il 429 di GDELT.** Per GDELT soltanto, un 429 chiude la corsa invece di fermare la fonte. La
   fonte si ferma solo dopo 6 corse di fila con un 429, con l'avviso. Gli altri segnali di blocco
   della riga «Raccolta» la fermano subito, come per ogni fonte.
   - Lettura del builder: vale anche un 429 di `robots.txt`. Una corsa che chiede e non ha 429
     rimette il conto a zero; una che non chiede niente lo lascia com'è. Alla ripartenza della
     notte il conto è partito da zero: la prima corsa, con la regola di prima, non conta.
   - Lettura del builder: «you get an alert» è `AVVISO_gdelt_<inizio>.json` in
     `B Notizie/letture/`, che il coordinatore legge e porta all'owner, come gli avvisi degli altri
     canali.
   - Lettura del builder: una fonte ferma la riaccende il coordinatore, che ne riceve l'avviso
     (CONTRATTI, sezione 7 B, «Raccolta»); toglie la fermata e azzera i conti delle corse di fila nei
     dati statici del flusso, quello dei 429 e quello degli errori del server della riga
     «Raccolta».

Impact:
- DEC-039: il rimando sotto la riga `Status:` (`decisions/README.md`, regola 2).
- Con la PR del canale B che segue questa: `docs/pilota/CONTRATTI.md`, sezione 7 B, riga «Misura
  GDELT»; `code-nodes/news-gdelt.js`, con i test in `tests/test_news_gdelt.js`; il flusso
  `staging_B_gdelt_misura`, esportato in `workflows/`, con «La misura di GDELT» in
  `workflows/README.md`. Il flusso è in staging dalla notte del 19 novembre.
- Spesa: zero. Una bozza di email a GDELT, per chiedere un accesso, è nella cartella di passaggio
  (`GDELT_email_bozza_2026-11-20.md`): la manda l'owner, se vuole.
- DEC-039, a parte il modo di leggere GDELT, DEC-108 e la riga «Raccolta» per le altre fonti
  restano invariate. Niente in produzione; gazetteer, prompt, registro dei venue, lane gate e CI
  invariati.

Decided by: owner · Date: 19 e 20 novembre 2026 · Affected components: canale B del pilota (la
misura dell'indice delle testate chiuse), `docs/pilota/CONTRATTI.md` (sezione 7 B),
`code-nodes/news-gdelt.js`, `staging_B_gdelt_misura`, DEC-039 (il rimando).

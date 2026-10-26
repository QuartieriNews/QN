# Qualità della pagina «Eventi dei quartieri»: controllo a campione, correzioni e test (M, 26 ottobre 2026)

**La richiesta dell'owner.** Serve un controllo di qualità della pagina degli eventi, anche per migliorarne la struttura, e
«almeno qualche testing». I titoli che sono frasi e non nomi sono un tema di UX da affrontare dopo. Il controllo sugli
eventi passati dei sei mesi precedenti non si fa.

Qui ci sono solo metodo e numeri. Le righe del campione, con i titoli e i testi delle fonti, restano fuori dal repository
(DEC-022, DEC-109).

**In breve.**

| | Prima delle correzioni | Dopo le correzioni automatiche |
|---|---|---|
| eventi con un errore grave, campione | 44 su 155: 28% (IC 95% 22-36%) | 32 su 143: 22% (16-30%) |
| stessa quota pesata per canale sulla pagina | 31% | 26% |
| senza gli annunci estratti dai post | 29 su 120: 24% (17-33%) | 17 su 108: 16% (10-24%) |
| eventi Facebook con l'ora sbagliata, campione | 37 su 45 | 1 su 36, secondo le note dei revisori (un orario segnaposto nella fonte) |
| righe gravi per il validatore, pagina intera | 49 su 2.585 | 32 su 2.489, tutte schede di Roma Today senza link |

L'errore più diffuso era sistematico: tutti gli orari degli eventi Facebook erano in UTC, quindi una o due ore indietro. Il
canale più debole resta quello degli annunci estratti dai post, con il 43% di errori gravi.

## 1. Come è stato misurato

- **Campione.** 155 eventi della pagina del 25 ottobre, estratti a caso con seme fisso e divisi per canale. Le schede di Roma
  Today sono escluse (DEC-026).

  | Canale | Eventi nel campione | Eventi sulla pagina |
  |---|---|---|
  | annunci nei post Facebook | 35 | 954 |
  | eventi Facebook raccolti dall'owner | 25 | 377 |
  | pagine dei siti delle fonti | 25 | 322 |
  | eventi Facebook delle pagine lette | 20 | 245 |
  | culture.roma.it | 20 | 356 |
  | feed iCal e REST dei siti | 15 | 139 |
  | agenda delle Biblioteche di Roma | 15 | 110 |

- **Testo della fonte.** Ogni evento è stato confrontato con la sua fonte:
  - 73 pagine rilette, rispettando robots.txt;
  - 40 eventi Facebook con i dati già raccolti;
  - 35 testi di post;
  - 7 eventi senza testo: 5 eventi Facebook non trovati nei dati, una pagina in errore 429, un canale che non leggiamo.
- **Giudizio.** Un revisore (modello AI) giudica per ogni evento data, ora, luogo, pagina QN, titolo, natura (evento,
  corso o attività ricorrente, non evento), stato e se l'evento è fuori Roma o solo online. Un secondo revisore
  indipendente rilegge 47 eventi, uno ogni quattro di ogni lotto.
- **Errore grave.** Un evento ha un errore grave se ha almeno uno di questi difetti:
  - data sbagliata;
  - evento già passato o annullato;
  - non è un evento;
  - fuori Roma o solo online;
  - pagina QN incoerente.

  Sono errori che rendono la riga sbagliata per un lettore. La data di riferimento del controllo è il 26 ottobre, ma la
  pagina è del 25: tre attività del 25, segnate gravi solo perché passate, non sono contate.
- **Accordo fra i due revisori:**
  - 91% sull'errore grave, kappa di Cohen 0,78;
  - 100% sulla data, 98% sul titolo, 94% su natura e pagina QN.
- **Limiti.**
  - 27 date non erano verificabili, perché la fonte manca o non riporta l'evento.
  - Quattro annunci da post sono stati confrontati con il testo di un altro post, per un errore del campionatore sui link
    `permalink.php`. Due di questi sono gravi per difetti visibili nella riga stessa: un luogo in Sardegna, un albergo in
    un altro quartiere. Gli altri due non sono gravi.

## 2. Che cosa è venuto fuori

**Per canale.** Il «dopo» è lo stesso campione dopo le correzioni del §3, che tolgono 12 eventi, tutti con un errore grave.

| Canale | Errori gravi prima | Errori gravi dopo |
|---|---|---|
| annunci nei post Facebook | 15 su 35 (43%) | 15 su 35 (43%) |
| eventi Facebook delle pagine lette | 8 su 20 (40%) | 4 su 16 (25%) |
| eventi Facebook raccolti dall'owner | 8 su 25 (32%) | 3 su 20 (15%) |
| agenda delle Biblioteche di Roma | 4 su 15 (27%) | 4 su 15 (27%) |
| feed iCal e REST dei siti | 3 su 15 (20%) | 3 su 15 (20%) |
| pagine dei siti delle fonti | 4 su 25 (16%) | 1 su 22 (5%) |
| culture.roma.it | 2 su 20 (10%) | 2 su 20 (10%) |

**Difetti nel campione di 155 eventi, prima delle correzioni.** Un evento può averne più di uno.

| Difetto | Eventi | Note |
|---|---|---|
| ora sbagliata | 43 (28%) | 37 sono eventi Facebook: l'ora era in UTC |
| titolo che è una frase presa dal testo | 37 (24%) | 30 dei 35 annunci da post |
| corso o attività ricorrente | 29 (19%) | non è un errore: serve una regola di conteggio |
| pagina QN incoerente | 20 (13%) | sede dell'organizzatore al posto del luogo, indirizzi geocodificati male |
| fuori Roma o solo online | 20 (13%) | 9 eventi Facebook (8 con le coordinate) e 8 annunci da post |
| luogo mancante, ma presente nella fonte | 16 (10%) | |
| ora mancante, ma presente nella fonte | 15 (10%) | |
| non è un evento | 13 (8%) | 10 sono annunci da post: campagne, resoconti, scadenze |
| data sbagliata | 10 (6%) | due pagine d'archivio riportate all'anno in corso |
| luogo sbagliato | 10 (6%) | |

## 3. Correzioni automatiche e test

| Difetto | Correzione | Dove | Test |
|---|---|---|---|
| ora in UTC | Le date in UTC (`Z`, `+00:00`) diventano ora di Roma, anche per la finestra delle date. Le date con un altro fuso restano come sono. | `leggi_eventi_siti.data_ora_roma`, usata dal lettore dei siti e dal raccoglitore della pagina | T-LS-1 |
| pagine d'archivio ridatate | Un giorno e mese senza anno sono scartati in due casi: il giorno della settimana scritto prima non torna, oppure tutte le date con l'anno dello stesso blocco hanno più di 180 giorni. | `leggi_eventi_siti.dates_in_block` | T-LS-2 |
| fuori Roma o solo online | Il luogo è controllato con una sola regola, usata dal raccoglitore e dal validatore: online, CAP fuori da 001xx, sigla di provincia diversa da RM, comune della provincia senza Roma, «città, altra regione, Italia». Le vie che portano il nome di una città restano a Roma. | `valida_eventi.luogo_fuori_roma` (V-GEO-5) | T-VE-3 |
| eventi Facebook fuori dal Comune | Sono scartati gli eventi con le coordinate fuori dalle 155 zone urbanistiche e una città diversa da Roma. Fa eccezione un titolo che nomina Roma senza un comune della provincia: sono le visite guidate con la pagina dell'organizzatore come luogo. | raccoglitore della pagina | prima e dopo, sotto |
| fine prima dell'inizio; telefoni o email nei campi | L'evento diventa di un giorno solo; il recapito è tolto. | raccoglitore della pagina | validatore (V-DATA-2, V-PRIV-1) |
| eventi finiti ancora in pagina | La pagina nasconde da sola gli eventi finiti, in base alla data del giorno, anche se i dati non sono stati rigenerati. | pagina pubblicata | controllo del rendering |

**Effetto sulla pagina**, con la stessa data di riferimento del 25 ottobre:
- 97 eventi tolti:
  - 71 con le coordinate fuori dal Comune;
  - 15 con il luogo online o fuori Roma;
  - 11 blocchi di testo d'archivio.
- L'ora di 540 eventi Facebook su 541 è stata convertita all'ora di Roma; 11 cambiano anche giorno.
- Le pagine QN con almeno un evento restano 84, quelle con almeno 10 eventi restano 49.
- Al 26 ottobre la pagina mostra 2.183 eventi in corso o futuri, sui 2.489 raccolti al 25.

**Test.** Il validatore `tools/fonti/valida_eventi.py` controlla ogni riga pubblicata. Le regole sono in testa al file e
dividono gli errori in gravi e avvisi.
- `--severo` termina con un errore se c'è anche una sola riga grave.
- L'elenco delle righe segnalate va fuori dal repository.

I test di accettazione sono `tests/test_valida_eventi.py` (T-VE-1…8, 57 controlli) e `tests/test_leggi_eventi_siti.py`
(T-LS-1…6, 42 controlli).

| Validatore, pagina intera (per regola: una riga può romperne più d'una) | Prima | Dopo |
|---|---|---|
| righe | 2.585 | 2.489 |
| righe con un errore grave | 49 | 32 |
| — luogo online o fuori dal Comune (V-GEO-5) | 15 | 0 |
| — senza link alla fonte (V-LINK-1, Roma Today) | 33 | 32 |
| — fine prima dell'inizio, recapito in un campo | 2 | 0 |
| avviso: senza pagina QN | 485 | 400 |
| avviso: titolo che è una frase | 496 | 477 (343 dagli annunci da post) |
| avviso: periodo oltre 31 giorni | 181 | 179 |
| avviso: inizio oltre 90 giorni | 114 | 112 |

## 4. Che cosa resta

Questi difetti non si correggono con una regola sul testo. Nel campione dopo le correzioni restano 32 eventi gravi; un evento può avere più di un difetto:
- **18 con la pagina QN incoerente.** Si correggono con il luogo vero dell'evento al posto della sede dell'organizzatore, e
  controllando i geocodici dubbi.
- **12 che non sono eventi**, quasi tutti annunci da post. Serve un'estrazione migliore o una revisione.
- **10 fuori Roma o online senza coordinate**, soprattutto annunci da post e feed.
- **8 con la data sbagliata.**
- **4 già passati o annullati** secondo la fonte.

Poi ci sono due difetti che non sono errori gravi:
- **Corsi e attività ricorrenti: 19% del campione.** Non sono errori, ma gonfiano i conteggi per pagina.
- **Titoli che sono frasi: 477 righe.** Restano al tema di UX successivo.

## 5. OWNER_DECISION_REQUIRED

1. **Annunci estratti dai post.** Sono 951 righe, il 38% della pagina, e hanno il 43% di errori gravi. Opzioni:
   - (a) toglierli dalla pagina finché non c'è un'estrazione migliore;
   - (b) tenerli come oggi, segnati «da verificare»;
   - (c) rifarne l'estrazione con un modello AI e una verifica scettica, come per le notizie, e pubblicare solo quelli
     confermati.
2. **Regola di conteggio di corsi e attività ricorrenti** (19% del campione). Opzioni:
   - contarli come eventi;
   - mostrarli in un blocco a parte;
   - escluderli dai conteggi per pagina.
3. **Schede di Roma Today senza link alla fonte** (32). Si decidono con DEC-026, ancora aperta.

Il builder non sceglie.

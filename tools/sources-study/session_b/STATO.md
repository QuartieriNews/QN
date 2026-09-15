# STATO — sessione B (Opus 5), ricostruzione una tantum di giugno 2026

Stato operativo della sessione B. Aggiornato a ogni passo rilevante; la conversazione non è
stato, questo file sì.

## 1. Verifica della chiave OpenAI (HANDOFF §2, §4.1)

| Controllo | Esito |
|---|---|
| Variabile `OPENAI_API_KEY` presente nell'ambiente | sì |
| Codice HTTP di `GET https://api.openai.com/v1/models` | 200 |
| Orario del controllo | 15 settembre 2026, 20:07 (Europe/Rome) — 18:07 UTC |

Il valore della chiave non è stato stampato, registrato, hashato né citato in alcuna forma,
qui o altrove. È stato usato solo come intestazione `Authorization` della richiesta di verifica,
il cui output è stato ridotto al solo codice HTTP.

Conseguenza: le chiamate a pagamento previste dal piano sono sbloccate, entro il tetto e con
la prova T1 di misura del prezzo effettivo prima di qualunque lotto di trascrizione
(HANDOFF §4.4). Nessuna chiamata a pagamento è ancora stata effettuata in questa sessione.

## 2. Budget

| Voce | Valore |
|---|---|
| Tetto complessivo | 78,86 € |
| Speso prima della sessione B | 0,86 € |
| Speso nella sessione B | 0,00 € |
| Disponibile | 78,00 € |

Nessun "extra usage", nessun abbonamento, nessun automatismo mensile: studio una tantum.

## 3. Quota Opus

Al massimo 2 subagenti Opus in parallelo oltre alla sessione principale. Lettura della pagina
Utilizzo da chiedere all'owner alla fine del primo giorno pieno (HANDOFF §2); letture della
sessione A in `quota_sessione_A.md`.

## 4. Avanzamento

| Passo (HANDOFF §4) | Stato |
|---|---|
| 0. Setup ambiente di lavoro | fatto |
| 1. Verifica chiave + primo commit di STATO.md | fatto |
| 2. Recuperi lenti (RomaTV, YouTube, Atti Web) | in corso: A2 958/2669 PDF, YouTube 18/131, RomaTV 17/318 |
| 3. Report 1 — consegna 17 settembre ore 19:00 | fonti testuali recuperate (985 item), estrazione fatta, lettura in corso |
| 4. Report 2 — consegna 20 settembre ore 19:00 | non iniziato |

## 5. Registro

- 15/09 20:07 — verifica chiave: presente, HTTP 200.
- 15/09 20:17 — controllo Codex C1 concluso, CHANGES_REQUESTED, 12 rilievi accettati, 0,16 €.
- 15/09 20:40 — canale di notifica push verificato non disponibile (§6).
- 15/09 21:22 — VM ritirata e riavviata; scratchpad intatto, job riavviati (§7).
- 15/09 21:30 — estrazione del Report 1 completata (985 item), lettura avviata su 2 lotti (§8).
- 15/09 21:55 — primi due lotti letti e verificati; specifica corretta su due punti (§9); D1 aperta.

## 6. Avvisi all'owner: canale push non disponibile (15 settembre, 20:30–20:40)

L'owner ha chiesto di ricevere una notifica sull'app Claude del cellulare quando serve
davvero una sua risposta. **Non è recapitabile da questa sessione**, e la causa è strutturale.

| Prova | Esito |
|---|---|
| Strumento di notifica diretto | "Mobile push requested", nessuna consegna |
| Routine `trig_01AumwmAXm4KtQxGuNYnh7kS` con `push` ed `email`, prima accensione (`cse_013YbniMrRaLLCbxszJbk9y4`, 20:33:15 → 20:33:34) | sessione conclusa con le etichette `routine_notify_push` e `routine_notify_email`, nessuna consegna |
| Stessa Routine, seconda accensione con contenuto che richiede una decisione (`cse_013b6EbYyZyhRfCWjEPT3n4g`, 20:35:12 → 20:35:29) | idem, nessuna consegna |

Causa: il recapito al telefono passa da Remote Control, che collega l'app a una sessione di
Claude Code in esecuzione sulla macchina dell'owner. Questa è una sessione cloud e non ha una
sessione locale a cui agganciarsi. Le notifiche dell'app dell'owner erano già attive: non era
una sua impostazione mancante. La seconda prova esclude anche l'ipotesi che il filtro
"degno di nota" stesse sopprimendo un avviso senza decisione dentro.

Conseguenze operative, fino a indicazione contraria dell'owner:

- Ogni richiesta all'owner vive **in chat e in questo file**, mai solo nella conversazione.
- Un blocco che richiede l'owner resta fermo finché non si riaffaccia. I recuperi lenti e il
  lavoro indipendente non si fermano: si ferma solo ciò che dipende dalla sua risposta.
- Per questo ogni richiesta porta con sé la **scelta di default** che applico da solo, come
  chiede il piano (§9.6): una richiesta senza default trasformerebbe l'assenza dell'owner in
  un'interruzione dello studio.
- La Routine resta creata ma inerte: non ha pianificazione e non parte da sola. Va cancellata
  o riusata solo se il canale diventasse disponibile.

Resta aperto per l'owner, senza urgenza: una Routine oraria di presidio creata da lui da
`claude.ai/code/routines` renderebbe robusto il presidio notturno (la creazione di Routine
ricorrenti da dentro la sessione è negata dal controllo permessi, "Unauthorized Persistence").
Non serve al recapito delle notifiche, serve a tenere viva la VM e a riavviare i recuperi.

## 7. Prova di ripresa dopo il ritiro della VM (15 settembre, 21:21): riuscita

La nota di fattibilità §9.3 lasciava aperta questa prova: la ripresa dopo la chiusura del turno
era dimostrata, quella dopo il **ritiro della VM** no. Ora c'è, e non perché sia stata
provocata: è successa da sola mentre la sessione era ferma in attesa dell'owner.

| Fatto | Rilievo |
|---|---|
| Ultimo segno di vita dei job | 18:47 UTC (A2), 18:44 UTC (RomaTV) |
| `uptime` al risveglio | `up 0 min` alle 19:22 UTC: la VM è stata ritirata e riavviata |
| Sveglia | promemoria `send_later` delle 19:21 UTC, arrivato e lavorato senza alcun intervento dell'owner |
| Scratchpad | **sopravvissuto**: 950 PDF, 18 sottotitoli, 17 cartelle di segmenti audio, tutti i testi delle fonti testuali |
| Processi in background | **tutti terminati**: 0 attivi al risveglio |
| Dipendenze (tesseract, pymupdf, yt-dlp, requests) | sopravvissute |
| Ripresa | i tre recuperi riavviati e ripresi dal punto esatto (A2 da 950 a 958 in venti secondi) |

Conclusione per il calendario: il ritiro della VM **non** costa il lavoro già fatto, costa il
tempo fra il ritiro e la sveglia successiva. Con il promemoria orario quel costo è al massimo
un'ora di scaricamento perso, come stimava §8.4. La riga di rischio 6 della nota (§9.5) si può
declassare: non serve un riavvio manuale dell'owner.

Il limite che resta: la catena di promemoria singoli è l'unico meccanismo di risveglio, perché
la Routine ricorrente è negata dal controllo permessi. Se un anello salta, i recuperi restano
fermi fino al messaggio successivo dell'owner.

## 8. Report 1: estrazione completata, lettura avviata

`report1_extract.py` ha prodotto 985 item con testo pulito e manifesto, esattamente i volumi
attesi dai censimenti: A1 365, E2 407, E3 104, C1 79, C2 20, C4 8, C5 2 (Cronaca 109 in tutto).
Mediana 1.566 caratteri per item; 26 item sotto i 200 caratteri, che i lettori tratteranno come
pagine senza notizia dichiarandone la ragione.

Due difetti dello script trovati e corretti prima della lettura:

1. **C5 non era contemplata**: due item di Cronaca sarebbero spariti dal Report 1 senza che
   nulla lo segnalasse.
2. **Abbinamento fra file e inventario per sottostringa**: falliva su ogni slug lungo o
   accentato, perché i nomi dei file sono troncati a 120 caratteri e conservano la codifica
   percentuale (`%C3%A0` → `c3_a0`). Dieci item C2 restavano senza data di pubblicazione e senza
   metadati. Ora l'abbinamento ricalcola la stessa trasformazione dall'URL dell'inventario, che
   è esatta: **0 item non abbinati**.

Lettura: 25 lotti (`report1/batches/`), al massimo 2 subagenti Opus in parallelo come prescrive
la regola di quota. Primo giro avviato alle 21:30 su L01 (A1, 50 item) e L14 (E2, 50 item): due
tipi di materiale diversi, per misurare tempi e qualità su entrambi prima di scalare.

## 9. Primi due lotti letti: rese, tempi e rilievi (15 settembre, 21:30–21:55)

| Lotto | Fonte | Item | Notizie | Tempo | Token |
|---|---|---|---|---|---|
| L14 | E2 eventi | 50 | 53 (53 media) | 9 min | 149.330 |
| L01 | A1 municipi | 50 | 74 (2 alta, 67 media, 5 bassa) | 11 min | 144.204 |
| L15+L16 | E2 eventi | 100 | 137 (tutte media) | 14,7 min | 226.649 |

| L17+L18 | E2 eventi | 100 | 106 (105 media, 1 bassa) | 11,5 min | 230.335 |
| L02+L03 | A1 municipi | 100 | 151 | 35,5 min | 317.127 |

**Difetto trovato e corretto nell'estrazione di A1.** `a1_items.py` tagliava il testo a 6.000
caratteri, a metà parola: scelta sensata per il censimento, dove contava solo l'inizio, dannosa
per la lettura. Otto item su 365 toccavano il tetto (mediana del corpus: 1.170 caratteri), e uno
perdeva metà del contenuto (A1_003: 6.110 → 11.938 caratteri). Il tetto è ora 15.000 come per le
altre fonti. Gli otto testi sono stati rigenerati **in posto**, senza rinumerare: i lotti già
letti puntano a quegli identificativi, e spostarli avrebbe silenziosamente disallineato tutto il
lavoro fatto. Vanno riletti solo quegli otto.

Totale a 22:30: **300 item letti su 985, 370 notizie candidate, zero senza evidenza**, 23 con
toponimo da verificare al conteggio precedente. Tipi: 222 evento, 17 avviso, 8 ordine del giorno, 6 risoluzione, 3
delibera, 2 audizione (da normalizzare), 6 altro.

Controlli fatti dall'Operator su entrambi: schema rispettato, **zero notizie senza evidenza**,
zero sintesi oltre le 60 parole, nessun nome di persona in quanto persona. Il tasso misurato è
di 11–13 s per item contro gli 81 s stimati in §9.5: quella stima veniva da trascrizioni di
Consigli, non da pagine HTML, e non va estesa ai lotti testuali.

**Due difetti della specifica, corretti prima dei lotti successivi** (una regola cambiata a metà
produce un database non confrontabile):

1. `municipio_testo` ammetteva un solo Municipio. Un item del lotto A1 ne riguardava due
   (`V;XI`): imporne uno avrebbe inventato una precisione che il testo non ha. Ora il campo
   ammette più valori separati da `;`.
2. **I due lotti hanno interpretato DEC-102 diversamente fra loro**: il lettore E2 ha riportato i
   nomi delle sedi alla lettera, quello A1 ha reso in forma generica sale, aule e scuole
   intitolate a persone. Nessuna delle due letture è sbagliata — la specifica non decideva. Ora
   decide, nella forma del default D1, e le due letture vanno riallineate prima del database.

**Rilievo per il rapporto, non per il metodo: le fonti cambiano sotto i piedi.** L'item A1_018
risulta pubblicato il 4 giugno ma è stato letto in una versione aggiornata il 25 giugno, e
contiene rinvii che al 4 giugno non esistevano. Non è un errore di lettura: è una proprietà della
fonte, e tocca direttamente la domanda sulla tempestività. Quattro altri item A1 dichiarano nel
testo una data di pubblicazione diversa da quella dell'elenco. Il Report 1 deve dire che la data
di pubblicazione di questa fonte **non è stabile** e che la colonna `disponibilita` esiste per
questo. Da verificare se il fenomeno riguarda anche E2 ed E3.

**Normalizzazioni da fare prima del database** (registrate qui perché si dimenticano):
1. DEC-102: riallineare L01 (sale e aule rese generiche) alla regola D1, che le vuole verbatim.
2. `tipo`: due righe E2 hanno `audizione` per convegni, forzatura dichiarata dal lettore quando la
   voce `convegno` non esisteva. Vanno portate a `convegno`.
3. D2.b: tre righe con nomi di gruppi musicali resi con il ruolo (E2_096, E2_074, E2_334) vanno
   riportate alla lettera: un gruppo è un'organizzazione, non una persona.
4. D2.c: verificare nei lotti L17–L18 gli autori delle opere resi con il ruolo e riportarli.
5. D3: riportare i nomi nelle intitolazioni e commemorazioni (A1_056, A1_011, A1_128) e
   ricomporre le evidenze troncate prima dei nomi (A1_012, A1_008).
6. **Rilettura di 9 item** (8 A1 più E2_231) (`report1/batches/_da_rileggere.txt`): A1_002, A1_003, A1_017,
   A1_031, A1_046, A1_093, A1_114, A1_115.

**Regole aggiuntive da scrivere nella specifica appena i lotti in corso rientrano** (il divieto
di modificarla a lotti aperti vale anche per me): il discrimine dell'indirizzo per gli avvisi con
più sedi; i punti all'ordine del giorno con esito; la data del fatto degli avvisi con termine;
D3 e il corollario sull'evidenza non troncata. Intanto viaggiano nei prompt dei lotti.

**Errore di processo dell'Operator, da non ripetere.** Ho modificato la specifica mentre due lotti
erano in lettura; il lettore L15/L16 se n'è accorto dal timestamp e l'ha segnalato invece di
tacere. Le sue letture sono coerenti perché la regola nuova era anche nel suo prompt, ma la
sequenza era sbagliata. La specifica ora vieta esplicitamente di modificarla a lotti aperti: una
correzione urgente va nel prompt dei lotti in corso e nel documento solo dopo il rientro.

**Materiale per la deduplicazione**: il lotto A1 ha già trovato tre coppie di item che
raccontano lo stesso fatto (A1_280/A1_281, A1_061/A1_209, A1_106/A1_107). I lettori non li
uniscono e non ne saltano nessuno: li schedano entrambi annotando il gemello, perché la
deduplicazione è un passo successivo che ha bisogno di vedere tutte e due le righe.

## 10. Database: costruttore scritto e provato sui lotti già letti (15 settembre, 22:45)

`report1/build_db.py` costruisce le cinque tabelle dello schema dai file dei lettori, senza
rete e senza chiamate a modelli: è rieseguibile e deterministico, quindi si rilancia a ogni
lotto che rientra. Prova sui 9 lotti disponibili (447 documenti letti, 591 notizie):

| Tabella | Righe |
|---|---|
| `fonti` | 7 |
| `documenti` | 985 (tutti, anche quelli non ancora letti) |
| `notizie_candidate` | 591 |
| `vicende` | 108 |
| `territori` | 114 |

Deduplicazione provvisoria: 431 uniche, 117 duplicati, 43 dubbi → resa netta fra **431 e 474**.
Localizzazione: 220 a `text_contains`, 29 ambigue, 342 senza toponimo risolto; 581 notizie su 591
hanno un Municipio, quasi sempre da quello dichiarato dalla fonte.

**Difetto mio, trovato e corretto sui numeri.** La prima versione dava 37 duplicati e 106 dubbi:
un rapporto invertito e implausibile. La causa era la condizione (b) del metodo: ripiegavo sul
Municipio ogni volta che la zona era vuota, e così due eventi diversi nello stesso Municipio lo
stesso giorno diventavano un dubbio. Il metodo §4.1 ammette il Municipio **solo quando nessuna
delle due notizie ha un toponimo più fine**. Corretto: ora si confrontano prima le zone, poi i
toponimi normalizzati, e il Municipio solo se nessuna delle due ne ha. Esito 117 duplicati e 43
dubbi. Corretto anche il campionamento, che usava una frazione inventata invece dei 60 item per
coppia di fonti con seed registrato che il metodo prescrive.

I numeri restano provvisori: mancano 16 lotti su 25, fra cui tutta la Cronaca e E3.

## 11. Secondo difetto di troncamento, e un controllo mio sbagliato

Un lettore ha segnalato `E2_231` tagliato a 15.000 caratteri, cioè al tetto dell'estrazione del
Report 1. Avevo escluso questo caso poche ore prima, ma il mio controllo era sbagliato: contavo
**byte**, non caratteri, e con gli accenti i due non coincidono — un testo di 15.000 caratteri
può pesare 15.265 byte e passare inosservato. Rifatta la misura sui caratteri: **un solo testo su
985** tocca il tetto. Rigenerato (21.289 caratteri reali, quasi un terzo perso) e aggiunto alla
rilettura.

Il caso è piccolo, la lezione no: due volte su due il troncamento è stato trovato da un lettore
che leggeva il testo, non dai miei controlli aggregati. I lettori vanno ascoltati quando
segnalano un'anomalia sul materiale, anche quando un mio conteggio dice il contrario.

| Lotto | Fonte | Item | Notizie | Tempo |
|---|---|---|---|---|
| L19+L20 | E2 eventi | 100 | 165 | 21 min |

Avanzamento: **547 item letti su 985**, 756 notizie candidate. In lettura: L04+L05 (A1) e tutta
la Cronaca (L09–L13, 109 item), che è il blocco dove DEC-102 conta davvero e dove si misura la
sovrapposizione fra Questura, Carabinieri, Vigili del fuoco e Comune.

## 12. Il blocco Cronaca è in gran parte inaccessibile (15 settembre, 22:45–23:00)

Il rilievo più grave della giornata, e nasce da un mio errore di acquisizione.

**Che cosa è successo.** Su 109 item di Cronaca, la lettura ha prodotto 33 notizie invece delle
~100 attese, perché il corpus era vuoto:

| Fonte | Item | Stato reale del materiale |
|---|---|---|
| C1 Questura | 79 | **67 identici**, byte per byte: la pagina "Accesso negato | Polizia di Stato", servita con codice **200**. 12 buoni |
| C2 Carabinieri | 20 | **tutti e 20** sono la stessa pagina-vetrina "Comunicati Stampa" (ASP.NET, `__VIEWSTATE`): l'URL del singolo comunicato rimanda all'elenco. Zero comunicati leggibili |
| C4 Vigili del fuoco | 8 | integri |
| C5 Roma Capitale | 2 | integri |

**La causa del mio errore, in una riga**: ho validato sul codice HTTP e sulla dimensione, non sul
contenuto. Novantanove risposte "200 OK" lunghe decine di migliaia di byte, e nessuna conteneva
l'articolo richiesto. Il mio log diceva "79 ok, 0 falliti". Se ne è accorto un lettore.

**Correzione strutturale.** `report1/page_checks.py` decide se una risposta è la pagina chiesta:
marcatori di blocco, titoli generici, corpo troppo corto. Lo usano sia `fetch_items.py` sia
`retry_c1.py`, perché una regola di validazione in due copie diverge. Provato sui tre casi:
riconosce il blocco della Questura, riconosce la vetrina dei Carabinieri, lascia passare A1.

**Ritentativo in corso, senza aggiramenti.** La sessione A quelle 79 pagine le aveva lette —
l'inventario ha Municipio, zona e toponimo per ciascuna — quindi il blocco è probabilmente una
conseguenza del mio ritmo (79 richieste in due minuti). `retry_c1.py` ritenta **una ogni 90
secondi** e si ferma dopo cinque rifiuti consecutivi: serve a capire se il blocco era il nostro
ritmo, non a forzare una fonte che sta dicendo di no. Nessun cambio di IP, nessun trucco sugli
header. Il primo tentativo è stato rifiutato.

**Se il ritentativo fallisce, è un risultato, non una sconfitta.** Il Report 1 dovrà dire che la
Questura nega l'accesso automatico e che i Carabinieri servono pagine costruite dal browser: per
lo studio è la risposta alla domanda se quelle fonti siano utilizzabili da QN. Gli inventari
restano (URL, titolo, data, Municipio), quindi i conteggi del mese reggono; manca il testo, e
questo va detto in chiaro e non nascosto in una nota.

**Conseguenza da dichiarare nel rapporto**: con C2 vuota e l'85% di C1 mancante, **la
sovrapposizione fra Questura e Carabinieri su giugno 2026 non è misurabile** con questo corpus.
Tutte le coppie di duplicati trovate finora sono interne alla stessa fonte.

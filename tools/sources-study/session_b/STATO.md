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
| Speso nella sessione B | 34,43 € |
| **Disponibile** | **44,43 €** |

Voci della sessione B (cambio usato 1 $ = 0,92 €, dichiarato perché il tetto è in euro e il
listino in dollari):

| Quando | Voce | Costo |
|---|---|---|
| 15/09 20:17 | controllo Codex C1 sullo schema del database | 0,16 € |
| 16/09 00:20 | controllo Codex C2 sulla specifica di lettura | 0,20 € |
| 16/09 05:55 | prova T1: 2,12 ore di audio RomaTV trascritte | 0,30 € |
| 16/09 08:50 | controllo Codex C3 sulla specifica delle registrazioni (3.835 token in, 8.737 out) | 0,22 € |
| 16/09 10:19 | trascrizione, 260 registrazioni su 275, 184,7 ore ($ 29,13, ancora in corso) | 26,80 € |
| 16/09 11:49 | controllo Codex C4 sul rapporto scritto (12.831 token in, 12.283 out) | 0,22 € |
| 16/09 13:35 | trascrizione **finita**, 318 registrazioni su 318, 227,7 ore ($ 35,76) | 32,90 € |
| 16/09 12:35 | controllo Codex C5 sul database e sul programma (16.508 token in, 19.378 out) | 0,29 € |
| 16/09 12:42 | prova T4, seconda AI su 30 candidate, due passate | 0,14 € |

Gli orari di questa tabella sono ora di Roma; le intestazioni delle sezioni sono in UTC. Andava
detto: due fusi nello stesso file si leggono male.

La riga della trascrizione **ha superato la stima** di 22,49 €: il driver è a $ 29,13 con quindici
registrazioni ancora da fare, e si fermerebbe da solo al suo tetto di $ 42. Fine previsto intorno a
$ 30,6, cioè **28,2 €**. La stima precedente era ferma a 154,9 ore quando le ore sono 184,7.

Impegno previsto ancora da spendere: **circa 2 €** per le registrazioni che restano, più i
controlli Codex C4 e C5 (~0,2 € l'uno) e la seconda AI sulle candidate. Il tetto regge con
ampio margine.

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
| 3. Report 1 — consegna 17 settembre ore 19:00 | **consegnato** in `docs/sources/RICOSTRUZIONE_2026-06_REPORT1.md` |
| 4. Report 2 — consegna 20 settembre ore 19:00 | atti: 1.250 di 1.983 letti; video: 141 di 318 registrazioni scaricate, prova T1 fatta |

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

**Esito del ritentativo (23:02): fallito, e la risposta è netta.** Cinque richieste a 90 secondi
di distanza, cinque "Accesso negato". Il processo si è fermato da solo come previsto. **Non era
il nostro ritmo**: la fonte nega l'accesso automatico. Nessun ulteriore tentativo, perché il
passo successivo sarebbe aggirare un controllo, e l'HANDOFF §2 lo vieta.

Bilancio del blocco Cronaca: **22 item leggibili su 109** (12 Questura su 79, 0 Carabinieri su
20, 8 Vigili del fuoco, 2 Roma Capitale), 33 notizie candidate. L'80% del blocco non ha testo.

**Se il ritentativo fallisce, è un risultato, non una sconfitta.** Il Report 1 dovrà dire che la
Questura nega l'accesso automatico e che i Carabinieri servono pagine costruite dal browser: per
lo studio è la risposta alla domanda se quelle fonti siano utilizzabili da QN. Gli inventari
restano (URL, titolo, data, Municipio), quindi i conteggi del mese reggono; manca il testo, e
questo va detto in chiaro e non nascosto in una nota.

**Conseguenza da dichiarare nel rapporto**: con C2 vuota e l'85% di C1 mancante, **la
sovrapposizione fra Questura e Carabinieri su giugno 2026 non è misurabile** con questo corpus.
Tutte le coppie di duplicati trovate finora sono interne alla stessa fonte.

## 13. Avanzamento alle 23:05

| Flusso | Stato |
|---|---|
| Lettura Report 1 | **709 item letti su 985**, 859 notizie candidate, zero senza evidenza |
| In lettura | L06–L08 (A1, 115 item) e L23–L25 (E3, 104 item) |
| Mancano dopo questi | L21, L22 (E2, 57 item) e le 9 riletture |
| Atti Web (Report 2) | **2.669 PDF su 2.669 scaricati**; estrazione del testo e OCR a 1.903 |
| YouTube | 63 sottotitoli su 131 |
| RomaTV | 51 registrazioni su 318 |

Atti Web è completo con un giorno e mezzo di anticipo sulla consegna del Report 2: era la voce
più a rischio del piano dopo le trascrizioni.

## 14. Rilettura finale invece di rattoppi (15 settembre, 23:25)

Le regole D1–D3 e la voce `convegno` sono nate mentre i lotti leggevano: i primi lotti hanno
quindi applicato criteri che sono cambiati dopo. Le normalizzazioni elencate in §9 si potevano
fare con sostituzioni automatiche sui CSV, ma una regola applicata da chi legge il testo non è la
stessa cosa di una regex applicata a un riassunto di 60 parole: il testo dice se un nome è un
toponimo, una dedica o una persona presente, il riassunto no.

Lotto **L26**, 78 item (`report1/batches/L26.txt`, motivi in `_riletture_motivi.csv`):

| Motivo | Item |
|---|---|
| Caso DEC-102 letto prima che D1–D3 esistessero | 49 |
| Intitolazione o commemorazione letta prima di D3 | 19 |
| Testo troncato e rigenerato | 8 |
| `tipo` forzato su `audizione` prima che esistesse `convegno` | 2 |

75 sono A1, 3 sono E2. Le righe vecchie di questi item vanno scartate e sostituite dalle nuove. Avevo scritto che
`build_db.py` prendeva già l'ultima lettura di ogni documento: **non era vero**, accumulava tutte
le letture, e i 78 item riletti avrebbero prodotto righe doppie gonfiando l'intero database.
Corretto: a parità di documento vince il lotto con il numero più alto, quindi L26 sostituisce le
letture precedenti.
Il criterio di selezione è volutamente largo — meglio rileggere un item che non ne aveva bisogno
che lasciarne fuori uno che sì.

## 15. Deduplicazione sull'intero mese, con il campione del metodo accanto (15 settembre, 23:35)

Il metodo §4.1 campiona sopra i 300 item perché **assume che il confronto lo faccia una persona**.
Il nostro è deterministico e costa nulla, quindi il confronto gira sull'intero mese e la resa è
*misurata*. Il campione prescritto viene però calcolato lo stesso, sulle stesse righe, così la
deviazione resta visibile: non volevo migliorare in silenzio il metodo di qualcun altro.

Ed è servito, perché i due numeri non coincidono:

| | Duplicati | Dubbi | Uniche |
|---|---|---|---|
| Campione prescritto (60 notizie, seed `2026-06-E2xE3`) | 18 (30%) | 5 | 37 |
| Confronto sull'intero blocco Eventi (613 notizie) | — | — | — |
| Totale su tutti i blocchi (1.138 notizie) | 179 (16%) | 110 | 849 |

Il campione avrebbe stimato una duplicazione **circa doppia** di quella reale. È un dato che vale
per il rapporto e forse per il metodo: su questo corpus, 60 notizie non bastano a stimare la resa
netta di un blocco.

Resa netta attuale: fra **849 e 959** notizie distinte su 1.138 candidate, da 820 documenti letti.
Numeri ancora provvisori: mancano L21, L22 e la rilettura L26.

**Altro difetto mio, da ricordare**: `python3 build_db.py | head -4` uccideva il processo prima
che scrivesse le tabelle, e la verifica successiva leggeva i file vecchi credendoli nuovi. Mai
incanalare in `head` un programma che scrive file.

## 16. E3 letta: due difetti attribuiti alla fonte, e un'ipotesi che vale il rapporto

E3 completata: 104 item, 152 notizie, 19 minuti. Nessun item senza notizie.

**Due segnalazioni di codifica, verificate: sono della fonte, non dell'estrazione.** Il lettore
aveva ipotizzato un difetto dell'estrattore. Controllati i byte dell'HTML di partenza:

- `E3_090`: la sequenza `\xc2\xbf` (`¿`) è **già nel file scaricato**, dentro l'elenco degli
  artisti. Difetto del gestore di contenuti della fonte.
- `E3_093`: l'HTML contiene **zero caratteri ebraici**; la parola è già sostituita da otto `¿`.
  Il portale non rappresenta gli alfabeti non latini.

Il lettore aveva ragione a segnalarli e torto sulla causa: l'estrattore non tocca nulla. Va nel
rapporto fra i difetti della fonte, non fra i nostri.

**La data di pubblicazione instabile è ora confermata su due fonti.** Dopo A1, anche E3: pagine
con "Ultimo aggiornamento: 17 agosto" su una pubblicazione dell'8 giugno, una "Segnalazione del
17 luglio" su una pagina del 24 giugno, una rassegna annunciata il 16 giugno e inaugurata il 14.
Non è un caso isolato di una fonte: è il modo in cui il portale funziona, e tocca in pieno la
domanda sulla tempestività.

**Ipotesi da verificare con la deduplicazione, e potenzialmente il risultato più utile del
Report 1.** Il lettore di E3 segnala che 128 righe su 152 (84%) sono probabilmente sovrapposte a
E2, perché promosse o ospitate dallo stesso circuito (Sovrintendenza, Zètema, Musei Civici,
Teatro di Roma, Auditorium). Le 24 righe senza sovrapposizione apparente sono quelle in cui **E3
smette di essere un'agenda di spettacoli e diventa comunicazione amministrativa**: conclusione di
lavori PNRR su un museo, restauro della Loggia dei Vini, riconsegna di un auditorium,
prolungamento d'orario del Bioparco, chiusura di uno spazio per il caldo, calendario
istituzionale della banda della Polizia Locale.

Se il passo automatico la conferma, la conclusione per QN è netta: **fra le due agende eventi il
contributo unico non sta negli spettacoli ma nella comunicazione amministrativa**, che è anche
ciò che un lettore di quartiere usa davvero. Otto di quei riconoscimenti sono fondati su un
rimando esplicito dentro la pagina E3 a culture.roma.it, non su impressione.

**Da uniformare prima di chiudere il database** (il lettore lo chiede esplicitamente): artisti
che espongono resi con il ruolo, ma sarti storici degli abiti in mostra lasciati alla lettera
perché non partecipano al fatto; denominazioni di formazione mantenute. Sono distinzioni sottili
e vanno verificate contro D1–D3 sul campione del controllo C2.

## 17. A1 completa; controllo dell'Operator su tutti i lotti (16 settembre, 00:05)

A1 chiusa: 365 item, 150 notizie negli ultimi tre lotti. Il lettore ha dichiarato di aver
corretto a fine lavoro 111 righe che superavano i limiti della specifica. **Controllo mio su
tutti i 23 lotti, 1.161 righe**: titoli ≤ 12 parole, sintesi ≤ 60 parole, `tipo` e `qualita`
dentro gli elenchi, evidenza sempre presente. **Zero violazioni.** Il controllo è cheap e va
rifatto dopo L21, L22 e L26.

**Uniformità DEC-102 su E3, verificata invece che richiesta.** Il lettore di E3 chiedeva conferma
su tre distinzioni sottili. Confrontate con D1–D3: sono già coerenti. Artisti che espongono →
ruolo, perché partecipano al fatto (D1). Sarti storici degli abiti in mostra → alla lettera,
perché sono autori delle opere e non partecipano (D2.c). Denominazioni di formazione → alla
lettera, perché sono organizzazioni (D2.b). Nessuna rilettura necessaria per E3.

**Materiale per la deduplicazione che i lettori hanno già trovato in A1**: presidio di Saxa Rubra
su due item, sciopero del 30 giugno su tre, rinvio Acea su tre più uno che lo annulla, open day
delle carte d'identità su quattro, e soprattutto **lo stesso avviso 0–3 anni ripubblicato da sei
Municipi diversi**. Quest'ultimo è il caso che mette alla prova la regola del luogo: stesso
oggetto, stessa data, sei Municipi. La condizione (b) del metodo lo tratta correttamente come sei
fatti distinti, perché il luogo è diverso — ed è la risposta giusta per un giornale di quartiere,
dove l'avviso del Municipio VII non è la notizia del Municipio II.

Stato lettura: **restano solo L21, L22 (57 item E2) e L26 (78 riletture)**, entrambi in corso.

## 18. E2 completa; campione e mandato per il controllo C2 pronti (16 settembre, 00:25)

E2 chiusa: 407 item. **Tutte e 985 le schede del Report 1 sono state lette almeno una volta**;
resta in corso la sola rilettura L26.

Rilievo dell'ultimo lotto che vale la pena isolare: `E2_354` è una **pagina di prova** pubblicata
in produzione dalla fonte («test rox 1»). Va nel rapporto fra i difetti della fonte, accanto ai
caratteri corrotti e ai refusi: un'agenda che pubblica pagine di test è un'agenda su cui una
pipeline automatica inciampa.

Buona decisione del lettore su `E2_297`, che merita di restare a verbale: una pagina del Planetario
annuncia insieme la **sospensione** e il programma completo di quattro giornate. Scomporla per
data avrebbe prodotto quattro notizie che annunciano spettacoli che la fonte stessa dichiara
annullati. Una riga sola, `avviso`, scelta motivata: è esattamente il tipo di giudizio che una
regola meccanica non può dare.

**Pronti per il controllo C2** (`tools/sources-study/report1/campione_c2.py`, mandato in
`$QN_NET/mandate_C2.md`): campione stratificato di 45 notizie con seed fisso `2026-06-C2`, quote
per fonte (almeno 5 ciascuna) e per esito di deduplicazione (almeno 5 per `unica`, `duplicato`,
`dubbio`). Il seed e le quote servono a impedire che il campione sia scelto per fare bella figura.
Vanno rigenerati dopo L26, perché le righe cambiano.

## 19. Lettura chiusa, database costruito, controllo C2 concluso (16 settembre, 00:30)

**Tutte e 985 le schede lette**, rilettura compresa. La rilettura si è ripagata: 17 item hanno
recuperato nomi che la regola vecchia cancellava, e 6 degli 8 testi troncati hanno rivelato fatti
che prima non si vedevano — circa 12 notizie nate dal tratto finale mancante.

| Misura | Valore |
|---|---|
| Documenti letti | 985 (891 con notizie, 94 senza) |
| Notizie candidate | 1.227 |
| Resa netta | **882–1.158** distinte |
| Con Municipio | 1.131 |
| Con zona del gazetteer | 448, su 63 zone distinte |
| Senza data del fatto | 151 |
| Qualità | 14 alta, 1.180 media, 33 bassa |

**Controllo C2**: CHANGES_REQUESTED, 3 bloccanti e 6 non bloccanti, tutti accettati e applicati
tranne tre residui dichiarati. Rapporto in `reviews/2026-09-16—report1-campione—CHANGES_REQUESTED.md`.

**Il difetto più grave l'ha fatto emergere il controllo per via indiretta.** Un rilievo su
un'incoerenza di superficie (`tier = text_contains` senza zona) ha mostrato che *tutte* le righe
erano così. La causa non era quella segnalata: `build_db.py` leggeva dal localizzatore la chiave
`zone`, che non esiste — la chiave giusta è `zona`. **La zona è stata vuota per l'intero
database fin dalla prima costruzione**: la deduplicazione non ha mai usato la chiave di luogo più
fine e il Municipio dedotto dal gazetteer non è mai stato usato. Corretto, e la localizzazione
ora esiste davvero.

Il revisore non poteva vedere questo difetto, perché non vede il codice. È la terza volta in
questa sessione che un difetto grave emerge da chi guarda i dati e non da chi li ha prodotti.

Restano da fare per la consegna: rapporto `docs/sources/RICOSTRUZIONE_2026-06_REPORT1.md`,
caricamento dei CSV su Drive, aggiornamento del ledger (fatto).

## 20. Report 1 scritto (16 settembre, 00:35)

`docs/sources/RICOSTRUZIONE_2026-06_REPORT1.md`. Risultati principali:

- **Resa netta 882–1.158** notizie distinte su 1.227 candidate, da 985 item.
- **Sono annunci, non cronaca**: 896 notizie su 1.075 pubblicate *prima* del fatto, mediana
  **sette giorni di anticipo**. Le fonti testuali dicono cosa succederà, non cosa è successo.
- **Tre quarti sono eventi culturali**; l'attività deliberativa è quasi assente e sta negli atti.
- **Tutti e 15 i Municipi coperti**, ma il I ha quasi quattro volte le notizie del III. Solo **2
  celle Municipio×settimana vuote**, entrambe nella settimana parziale del 29–30 giugno.
- **La sovrapposizione fra le due agende eventi è minima**: 8 duplicati certi e 23 dubbi su 640
  notizie, al massimo il 5%. **Contraddice l'impressione del lettore di E3** (84% di
  sovrapposizione percepita), che nasceva dal circuito culturale comune e non dai fatti. Dichiarato
  come **limite inferiore**: due lettori scrivono titoli diversi per lo stesso evento, quindi un
  confronto più permissivo troverebbe altre coppie. La direzione regge, la cifra esatta no.
- **Cronaca**: 22 item leggibili su 109; la sovrapposizione Questura–Carabinieri non è misurabile.
- **Difetti della fonte** documentati: data di pubblicazione instabile su due fonti, contraddizioni
  interne, caratteri corrotti e alfabeti non latini persi, pagine di prova in produzione, e il
  Municipio dichiarato dal portale che non è il luogo della notizia.

Correzioni all'ultimo giro: anagrafe delle fonti compilata (nome, ente, URL di elenco, e la nota
sul blocco per C1 e C2); `territori.csv` ora emette **anche le celle vuote**, perché una lacuna è
una cella senza notizie e una tabella che elenca solo ciò che esiste non può mostrarla.

## 21. Caricamento su Drive: fatto a metà, e quello che resta

Cartella `QN Hub / 20 Packages / Fonti 2026-06/`. Il connettore fa passare il contenuto dalla
conversazione, quindi ogni file costa contesto: i grandi vanno caricati a contesto fresco, uno o
due per risveglio, mai tutti insieme — una compattazione a metà lascerebbe un caricamento parziale
senza che nulla lo segnali.

| File | Stato |
|---|---|
| `Report1_fonti_2026-06.csv` | **caricato** |
| `Report1_notizie_C1_2026-06.csv` (14 righe) | **caricato** |
| `Report1_notizie_C4_2026-06.csv` (8 righe) | **caricato** |
| `Report1_notizie_C5_2026-06.csv` (11 righe) | **caricato** |
| `Report1_territori_2026-06.csv` (96 celle, con le 2 lacune) | **caricato** |
| `Report1_vicende_2026-06.csv` (218 vicende) | **caricato** |
| `notizie_compatte_E3.csv` (44 KB) | **caricato** (`Report1_notizie_E3_2026-06.csv`, 43.577 byte) |
| `notizie_compatte_A1.csv` (161 KB) | **caricato in tre parti** (53.927 + 52.857 + 54.363 byte, §38) |
| `notizie_compatte_E2.csv` (161 KB) | da caricare |
| `documenti_compatti.csv` (164 KB) | da caricare |

Il segnaposto da 10 byte creato per provare il connettore è stato **cestinato**.

**Correzione alla versione compatta.** La prima versione ometteva il titolo, e due notizie diverse
tratte dallo stesso comunicato diventavano righe indistinguibili (successo davvero su `C1_079`:
il piano di sicurezza e le navette per lo stesso concerto). Un titolo non è né un nome di persona
né un testo integrale, quindi rientra in §4.2: ora c'è, insieme ai `luoghi`.

## 22. Da fare al prossimo risveglio

1. Completare il caricamento su Drive (§21), uno o due file per volta.
2. Rileggere `N0812` per il titolo d'opera anonimizzato per errore (residuo C2 n. 7).
3. Report 2: gli atti sono pronti (2.669 PDF con testo e OCR); mancano trascrizioni RomaTV e
   sottotitoli YouTube.

## 23. Report 2 avviato (16 settembre, 02:30)

Gli atti delle tre settimane sono pronti e in lettura: **1.983 atti con testo** su 8–28 giugno
(689 nella settimana 2, 663 nella 3, 631 nella 4), divisi in 40 lotti da 50, ordinati per tipologia
in modo che ogni lotto veda un mix e non cinquanta convocazioni di fila.

Tipologie: DDS 682 determinazioni dirigenziali, MMC 386 convocazioni di commissione, MMV 312
verbali di commissione, DMS 131, CPC 76, AY 60, CMC 47 delibere di Consiglio, CMR 30, CMD 28,
GCD 27, e code minori.

`tools/sources-study/report2/SPECIFICA_ATTI.md`: deriva dallo schema del lotto B già collaudato,
con i confini D1–D3 dentro. La regola che conta di più è scritta in chiaro nel prompt dei lettori:
**la maggior parte degli atti non è una notizia, ed è un risultato da misurare, non un fallimento
da evitare.** Un lotto che producesse notizie da quasi tutti gli atti avrebbe sbagliato la soglia.
Gli atti non notiziabili restano comunque nel CSV, perché la quota di atti notiziabili è una delle
domande del Report 2.

Primi due lotti tripli avviati (B01–B03 e B04–B06), i due subagenti Opus consentiti.

## 24. Primi 150 atti letti, e un difetto che toccava tutti e 40 i lotti (16 settembre, 03:00)

**B01–B03: 150 atti, 22 notizie candidate, 14,7%.** La quota non è omogenea e la differenza fra i
lotti è il dato interessante, non un problema: B03 al 4% (47 convocazioni su 50), B01 al 10%,
B02 al 30% (quasi tutta produzione di indirizzo di tre sedute d'Aula).

Il lettore ha dichiarato la regola che ha applicato e **l'alternativa più severa**: un atto di
indirizzo è notizia solo se nomina un luogo identificabile e ne cambia la prospettiva
amministrativa; con la lettura stretta — un atto non vincolante non cambia nulla — B02 andrebbe
vicino a zero e il totale intorno al 5%. Il rapporto potrà dare entrambe le cifre, perché **tutte
le righe `no` restano nel CSV**: il dato grezzo per decidere c'è.

**Difetto che toccava tutti e 40 i lotti, trovato dal lettore.** Il manifesto ricavava il Municipio
dal nome del file, dove `X` è il **ripiego per "Municipio assente"** scelto da `a2_list_all.py` —
indistinguibile dal Municipio X. Verificato sugli inventari di origine: gli atti municipali e le
determinazioni hanno sempre il Municipio, mentre **272 atti centrali su 322 non ce l'hanno**.
Manifesto ricostruito dagli inventari invece che dal nome del file: **218 righe corrette** da `X` a
`non indicato`, e restano 65 atti davvero del Municipio X. Aggiunta anche la colonna `fonte_atto`
(A2 1.056, DDS 682, CEN 245). I sei lotti già letti portano ancora il valore vecchio: la mappa di
correzione è in `report2/_municipio_corretto.csv` e va applicata in aggregazione.

**Autocorrezione del lettore, verificata.** Aveva inizialmente riportato i cognomi dei Consiglieri
firmatari, se n'è accorto, ha rigenerato due lotti e ha dichiarato l'audit. Controllo mio sulle 150
righe: gli unici nomi rimasti sono odonimi (via Federico Torre, via Alberto Mario, via Andrea
Doria). L'autocorrezione ha tenuto.

**Deviazione dalla specifica, giusta.** Otto atti delle Biblioteche non portano il marcatore
`(OCR Tesseract)` ma hanno errori di riconoscimento inequivocabili: il lettore li ha marcati
`ocr_incerto = sì` contro la lettera della specifica, dichiarandolo. Ha ragione — certi PDF
portano uno strato di testo già corrotto all'origine, che la nostra estrazione copia senza passare
da Tesseract, e marcare `no` un testo palesemente corrotto sarebbe falso. La specifica ora lega il
campo **al testo, non al marcatore**.

**Contraddizioni notevoli fra gli atti**, dichiarate e non risolte: due ordini del giorno approvati
nella stessa seduta che chiedono cose opposte sullo stesso parcheggio; una convocazione del 9
giugno che mette in approvazione un verbale del 14; un verbale con 18 votanti, 17 favorevoli e
0 contrari; la Bibliocard a 10 euro a pagina 3 e gratuita nel deliberato.

## 25. B04–B06 letti; una violazione DEC-102 trovata cercando altro (16 settembre, 03:40)

**B04–B06: 150 atti, 44 notizie candidate, 29,3%.** La forbice si conferma e si spiega con la
composizione: 20% in un lotto fatto per metà di pareri su proposte capitoline (atti consultivi che
non cambiano nulla), 42% dove ci sono verbali di Consiglio con voti divisi e sopralluoghi, 26% fra
le convocazioni di Commissione Capitolina. Totale sui sei lotti: **66 notizie su 300, il 22%**.

**Lo stesso difetto del Municipio, trovato in modo indipendente.** Questo lettore ha segnalato i 49
atti `CEN_CPC_X_*` con `municipio = X` che sono dell'Assemblea Capitolina, e ha fatto di più: ha
indicato nella nota il Municipio **effettivo dell'oggetto** (Olgiata → XV, Palmarola → XIV, Torrino
Nord → IX, Villa Gordiani → V). Quelle note valgono più della correzione automatica, perché
localizzano l'atto dove sta il fatto.

**Una violazione DEC-102 trovata per caso, mentre cercavo altro.** Cercando il nome della ditta
individuale, il filtro ha agganciato la sottostringa dentro `Corbucci`: e lì c'era una nota che
riportava **il cognome di un consigliere capitolino**, finito nell'output proprio mentre il lettore
segnalava che la fonte lo scrive in due grafie diverse. È il caso in cui la regola è più facile da
dimenticare: si sta documentando un difetto della fonte, non raccontando un fatto. Corretto in "il
cognome di un consigliere compare in due grafie diverse", e la regola è ora esplicita nel prompt
dei lotti successivi. Audit allargato su tutti e sette i lotti: nessun altro nome dopo una
qualifica.

**D4 applicata a valle** sulle due righe lette prima che esistesse (B03, B04). Il lotto B07, partito
dopo, la applica già da sé.

**Incoerenza dichiarata dal lettore stesso**: una riga di B04 è stata classificata notizia con un
criterio che lui stesso ha poi stretto in B05; non ha riscritto un lotto chiuso e l'ha segnalata
come la classificazione più fragile dei tre. Resta così, dichiarata: riscriverla a posteriori
sarebbe peggio, perché nasconderebbe che la soglia si è assestata leggendo.

**Materiale per il rapporto**: l'aritmetica delle votazioni della fonte è sbagliata di frequente —
unanimità proclamate con astenuti o contrari, un atto con 16 voti dichiarati e 22 nomi elencati,
due mozioni distinte con lo stesso numero; e gli identificatori dello stesso procedimento divergono
fra atti (una proposta è `RC/14716/2026` in un atto e `RC/0017442/2026` in un altro).

## 26. Struttura delle vicende (16 settembre, 03:30)

Caricata `vicende.csv`: 218 vicende, cioè insiemi di due o più notizie sullo stesso fatto. La
forma dice qualcosa che i conteggi non dicevano:

- **21 vicende attraversano le due agende eventi** (`fonti = E2;E3`). Sono più delle 8 coppie di
  duplicati certi, perché una vicenda tiene insieme anche i legami marcati `dubbio`. Il quadro del
  rapporto regge: la sovrapposizione fra E2 ed E3 esiste ma è piccola, e sta soprattutto nelle
  aperture straordinarie e nelle mostre dei musei civici — non nelle proiezioni di quartiere.
- **Il resto sono ripetizioni interne alla stessa fonte**: E2 che riannuncia lo stesso film in date
  diverse, A1 che ripubblica lo stesso avviso.
- **Nessuna vicenda attraversa Cronaca e Amministrazione**, e non è un caso: con l'80% della
  Cronaca illeggibile non c'era materiale per trovarne.
- Le vicende di confidenza `alta` — legame accertato — sono una minoranza; la maggioranza è `bassa`,
  cioè poggia su continuità di luogo e oggetto. Il rapporto le conta separatamente, come prescrive
  lo schema.

Il verbale dei numeri legali caduti nel Municipio XII (V053, V055, V056: tre sedute in tre
settimane) è il caso in cui la struttura per vicende mostra un fatto che le singole notizie non
mostravano.

## 27. Un nome non è l'unico modo di identificare una persona (16 settembre, 03:50)

**B07–B09: 150 atti, 20 notizie, 13,3%.** Totale a 450 atti su 1.983: **86 notizie, 19%**. Il
lettore ha fatto la cosa più utile possibile per il rapporto: ha dato la **sensibilità della
soglia**, non solo il numero. Con una soglia più larga sulle discipline di traffico si andrebbe
intorno al 20%, con una più stretta al 7%. E ha dichiarato che i suoi tre lotti non sono un
campione qualsiasi: 108 atti su 150 sono determinazioni di traffico, la categoria strutturalmente
meno notiziabile dell'archivio.

**Il problema di riservatezza più serio trovato finora, e non riguarda i nomi.** Due atti di revoca
di stalli riservati descrivevano, senza nominare nessuno:

- indirizzo **con numero civico**, condizione di **disabilità**, e il fatto che una titolare
  «risulta deceduta e l'altra trasferita»;
- indirizzo con civico, disabilità, e la **data esatta del decesso** del titolare.

Il lettore aveva applicato DEC-102 come la conosceva — nessun nome, ruoli al loro posto — e
formalmente aveva ragione. Ma **la combinazione di via, civico, condizione personale e data
identifica una persona meglio di un nome**, e per giunta rivela dati sanitari. Corretto in posto:
via sì, civico no, nessuna data personale, nessun numero di contrassegno. **Il fatto amministrativo
resta per intero**, compreso il dato che davvero interessa allo studio: fra il venir meno del
diritto e la revoca passano due anni e otto mesi, durante i quali lo stallo è rimasto riservato.

La regola è ora scritta nella specifica degli atti e nel prompt dei lotti successivi. Verificato
che nessun numero di contrassegno fosse mai stato trascritto: nei sette lotti non ce n'è uno.

**Materiale per il rapporto** da questi lotti: intervalli scoperti fra l'avvio di un cantiere e il
titolo di traffico che dovrebbe autorizzarlo (via Cilicia due mesi e mezzo, Pincio undici giorni,
due buchi in una catena di otto proroghe); anni sbagliati nei dispositivi (`12/06/2025` per una
festa del 2026, un protocollo datato 2027 su una seduta di giugno 2026); oggetto e dispositivo che
si contraddicono in una dozzina di atti.

## 28. Il difetto di riservatezza era sistematico, non isolato (16 settembre, 04:10)

Dopo aver corretto i due atti trovati ieri, ho passato un controllo su **tutti** i lotti letti
cercando la combinazione «numero civico + condizione personale» invece dei soli nomi. Ne sono
usciti **altri 19**: tutte determinazioni dirigenziali per stalli di sosta riservati, ciascuna con
via, civico esatto e condizione di disabilità del titolare.

Non era un errore di un lettore: **era sistematico**, perché la fonte scrive così e la regola che
avevo dato parlava solo di nomi. Corretto in blocco su tutti e dodici i lotti, con la nota riga per
riga; controllo finale: **nessun residuo**. Indirizzo ridotto alla via, che serve alla
localizzazione; civico, numero di contrassegno, date personali e rapporti di parentela omessi.

**Un caso che ho invece lasciato**, e vale la pena dire perché: una mozione municipale chiede di
inserire un incrocio fra i *black point* ed elenca gli incidenti mortali avvenuti lì, con date e
età. È un atto politico pubblico, senza nomi, e quegli incidenti sono la ragione stessa della
mozione: toglierli svuoterebbe la notizia e non proteggerebbe nessuno che l'atto già non protegga.
La differenza con gli stalli riservati è che lì l'atto riguarda **una persona determinata alla sua
residenza**, qui riguarda **un luogo pericoloso per tutti**.

**Avanzamento**: 650 atti letti su 1.983, 126 notizie candidate, **19,4%**; 82 atti con OCR
incerto. B10–B12, tutti determinazioni di traffico, hanno dato il 17,3%.

**Trovato dai lettori, materiale per il rapporto**: due cortei del 13 giugno con finalità opposte
autorizzati sulla base dello stesso protocollo della Questura, con percorsi e orari sovrapposti;
due atti gemelli il cui oggetto dice «abbattimento» e la premessa «lavori di stabilità» sulle stesse
alberature; per tre Municipi compaiono due Gruppi di Polizia Locale con serie di repertorio diverse.

## 29. La correzione in blocco ha fatto danni, e li ho dovuti riparare a mano

La sostituzione automatica del paragrafo precedente **era sbagliata due volte**, e me ne sono
accorto solo controllando una riga a campione dopo averla eseguita:

1. **Ha colpito atti che non erano individuali.** Un evento a Villa Miani, un cantiere in via
   Minghetti, riprese in via Merulana: citano la disabilità solo come **deroga** al divieto di
   sosta. Lì il civico è un cancello carrabile o un tratto di strada, non la residenza di qualcuno.
   Ripristinati.
2. **Ha spezzato le frasi.** «sul lato destro subito prima del,» — la regex toglieva il civico e
   lasciava l'articolo. Tre campi resi incomprensibili.
3. **E aveva mancato il plurale**: «civici 6 e 18» non corrispondeva al modello, quindi cinque
   campi erano rimasti esposti.

Riparato a mano, leggendo ogni campo per intero e riscrivendolo: gli atti individuali veri perdono
il civico dappertutto, gli atti generali lo riprendono. Controllo finale: nessun atto individuale
con civico, nessuna frase spezzata, nessuna nota di omissione su un atto che non la richiede.

**È esattamente l'errore contro cui mi ero espresso poche ore fa** scegliendo la rilettura invece
del rattoppo automatico per il Report 1: una regex applicata a un riassunto non è una regola
applicata al testo. Avevo ragione allora e l'ho dimenticato adesso, con l'attenuante che qui il
difetto era di riservatezza e la fretta era giustificata — ma la fretta è il motivo per cui il
controllo va fatto **dopo** ogni sostituzione automatica, non al posto suo.

Regola che porto avanti: **dopo ogni modifica in blocco, rileggere almeno una riga toccata per
intero.** Il campione di una riga avrebbe mostrato subito tutti e tre i difetti.

**La coda della riparazione, perché non finisce dove sembra.** Il primo controllo dopo la
riparazione ne ha trovati altri sette, il secondo altri quattro, il terzo altri due. Ogni giro
restringeva il filtro e scopriva un caso che il giro prima non vedeva. Il bilancio: 12 campi
mutilati riscritti a mano, 4 numeri civici **recuperati dai testi di partenza** invece che dalla
memoria, 7 note di omissione tolte da atti che non erano individuali.

**E due cose che i giri successivi hanno trovato e che il primo non cercava**: in due atti il campo
`luoghi` conteneva **l'indirizzo di abitazione del richiedente** — «via Luigi Chiarelli 6
(abitazione indicata nell'istanza)», «via Valtravaglia 6 (abitazione indicata nell'istanza)». Non
era il civico dello stallo: era **casa sua**, scritta perché la fonte la scrive. Rimossi.

Audit definitivo sulle 700 righe lette: nessun atto individuale con civico, nessun indirizzo di
abitazione, nessun campo spezzato. L'unico residuo segnalato era un falso positivo («2,60 metri di
altezza, 2,30 di larghezza»).

## 30. 800 atti letti; la quota dipende dalla composizione, non dalla soglia (16 settembre, 04:40)

**B13–B15: 150 atti, 43 notizie, 28,7%** — sopra la fascia 13–29% dei lotti precedenti, e il
lettore ha spiegato perché prima che glielo chiedessi: i suoi tre lotti sono **interamente
discipline di traffico**, ed è lì che finisce tutto ciò che di concreto succede in strada. Due
voragini, alberi pericolanti, un sospetto dissesto del sottosuolo con i bus esclusi da aprile,
quattro cantieri giubilari, i varchi della Fascia Verde, il GRAB, tre bonifiche di rete lunghe mesi.

Il suo giudizio: 28–30% è il valore vero per un lotto di solo traffico, non un allargamento del
criterio; e ha indicato **quali due scelte irrigidire** per riportarlo a 24%. Ha anche dichiarato
la sua incoerenza interna più netta — scavi notturni su tre strade a San Lorenzo classificati `sì`,
tre strade per quattro settimane a Prati classificate `no` — segnalando che uniformarli sposta la
quota di ±2 punti. Vale più della cifra.

**Totale: 800 atti su 1.983, 166 notizie candidate, 20,8%.**

**Audit di riservatezza ripassato su tutti gli 800**: pulito. Le 15 segnalazioni del filtro erano
tutte **falsi positivi** — numeri di concessione edilizia o di occupazione di suolo, che sono atti
e non persone, e note dei lettori che dichiaravano di *non* aver riportato i numeri personali. Il
filtro va letto, non creduto: è lo stesso errore che stanotte mi ha fatto mutilare dodici campi.
La regola è ora nel prompt: i numeri di concessione edilizia restano, quelli personali no.

**Materiale nuovo per il rapporto**: pareri datati dopo l'atto che li richiama; un'autorizzazione
valida «dal 19.06.2026 al 22.02.2026», cioè che finisce prima di cominciare; determinazioni
prorogate da atti di numero inferiore dello stesso anno; una stessa nota di protocollo che avvia
due procedimenti per titolari diversi; catene di proroghe con scoperti fino a ventidue giorni; e
un atto la cui data finale è il 14 luglio 2027, quasi certamente un refuso per il 2026 — riportato
come sta, perché correggerlo sarebbe inventare.

## 31. 950 atti; la fonte anonimizza se stessa in modo incoerente (16 settembre, 05:00)

**B16–B18: 150 atti, 45 notizie, 30%** (22%, 34%, 34%). Totale: **950 su 1.983, 211 notizie, 22,2%**.

Il lettore ha aggiunto la cosa che al rapporto serviva e che nessuno gli aveva chiesto: **la quota
va confrontata a parità di composizione**. Nei suoi tre lotti la parte fatta di set cinematografici,
traslochi e stalli riservati sta sotto il 20% in tutti e tre; a far salire B17 e B18 sono quattro
atti del piano di illuminazione pubblica, il cantiere del GRAB, un intervento giubilare, «100
Parchi per Roma», una bonifica idrica di tre mesi e tre discipline definitive che riscrivono una
piazza e due strade. Ha dato anche la **forbice per lotto** (B16 12–36%, B17 24–48%, B18 26–50%) e
ha fissato un criterio uniforme sugli atti-evento: `sì` solo se chiudono al **transito**, `no` se
vietano la sola sosta.

**Un rilievo che riguarda direttamente DEC-102, ma dal lato della fonte.** Gli atti di Roma
Capitale **anonimizzano in modo incoerente**: in cinque atti usano le sole iniziali, in altri
nominano per esteso la stessa categoria di persone. Non è un difetto del nostro metodo, è un dato
sulla fonte: chi costruisse una pipeline fidandosi dell'anonimizzazione a monte pubblicherebbe nomi
in chiaro senza accorgersene. Va nel rapporto.

**Verifica che nessuno aveva chiesto e che il lettore ha fatto comunque**: ha controllato i toponimi
del dispositivo di tutti e 150 gli atti contro il Municipio del manifesto. Nessun atto colloca
l'oggetto fuori dal Municipio dichiarato. È il controllo che nei lotti precedenti aveva trovato i
49 atti capitolini marcati Municipio X.

**Anomalie di tempo, che stanno diventando il tema del Report 2**: venti mesi fra istanza e atto;
un atto retroattivo di due giorni; quattro giorni di transennamento dei Vigili del fuoco senza
alcun atto di traffico; **nove mesi fra la scadenza del titolo e la revoca** di uno stallo
riservato; e **otto anni di cantiere del mercato Alberone**, dal 2020 al 2028 previsto. Due
proroghe della stessa concessione lasciano scoperti il 27 e 28 giugno e citano date di concessione
diverse; un cantiere ai Parioli resta scoperto quasi due mesi.

## 32. 1.100 atti; la contraddizione che si vede solo incrociando due lotti (16 settembre, 05:20)

**B19–B21: 150 atti, 34 notizie, 22,7%.** Totale: **1.100 su 1.983, 245 notizie, 22,3%.**

Il lettore ha formulato il criterio che tiene insieme tutti i lotti meglio di come l'avevo scritto
io: quando un atto cade insieme in un `sì` e in un `no`, **si guarda se il fatto nasce con
quell'atto**. Da qui le proroghe restano `no` anche quando prorogano assetti pesantissimi, perché
la notizia stava nella determinazione originaria. L'ho messo nella regola 5 dei lotti successivi.

**La contraddizione più grave della fonte trovata finora si vede solo incrociando due lotti**: due
determinazioni prorogano la **stessa** disciplina per l'ex Mattatoio, con dispositivo identico, una
fino al 31 luglio e l'altra fino al 31 agosto, **a un giorno di distanza e senza citarsi**. Una
delle due dichiara per giunta che un atto è stato prorogato da se stesso. Nessun lettore di un solo
lotto avrebbe potuto vederla: è un argomento per l'aggregazione, non solo per la lettura.

**Una revoca in autotutela emessa per correggere un errore di data ne conserva un secondo e ne
introduce un terzo**, datando l'atto revocato al 26 giugno **2028**.

**Un identificativo che la mia regola non copriva**: in un atto la fonte identifica la richiedente
**nel nome di un allegato** citato nel testo. Il lettore l'ha segnalato senza riprodurlo — la scelta
giusta. Verificato: negli output non compare.

**E un errore mio, trovato dal mio stesso controllo**: in una nota di un lotto precedente le
iniziali di una persona erano riprodotte *mentre si spiegava di averle tolte*. Stesso schema del
cognome «Corbucci» di qualche ora fa. Corretto; la regola è ora esplicita nel prompt: non
riprodurre l'identificativo mentre dichiari di averlo rimosso, perché sembra documentazione ed è
pubblicazione. Audit su 1.100 righe: nessuna iniziale di persona residua.

**Il resto delle sigle puntate negli output — U.I.T.S.S., D.P.R., S.R.L., A.M.A., G.I.P., P.N.R.R.
— sono amministrative**, e il filtro le segnalava tutte: un altro caso in cui il filtro va letto e
non creduto.

## 33. 1.250 atti; il livello deliberativo è un'altra fonte (16 settembre, 05:40)

**B22–B24: 150 atti, 46 notizie, 31%** — ma le tre quote sono **10%, 32% e 50%**, e il lettore ha
isolato la ragione strutturale che il Report 2 dovrà spiegare: **una delibera di Giunta che approva
un progetto nomina quasi sempre un luogo, una determinazione di liquidazione quasi mai.** La prova
interna è la più solida vista finora: i 5 atti di liquidazione *dentro* il lotto al 50% si
comportano come il lotto al 10% — 1 su 5. Non è la soglia che si muove, è il materiale.

Totale: **1.250 atti su 1.983, 300 notizie, 24,0%.**

**Un quinto di un lotto è inutilizzabile oltre il titolo.** Le memorie di Giunta hanno 3–4 pagine
di cui **solo il frontespizio contiene testo**; una non ha nemmeno la riga dell'oggetto, ed è
l'unico atto di cui non si può dire di che cosa parli. Tutte e 27 le delibere di Giunta del lotto
hanno lo strato di testo corrotto all'origine, senza marcatore Tesseract; sette hanno leggibile
solo il frontespizio, in un caso su 158 pagine.

**Verificato di persona il caso più notevole**: in una delibera il testo è **cifrato per
scorrimento di tre lettere** — `Sala GHOO$UD]]R` diventa `Sala dell'Arazzo`. Il lettore **non l'ha
ricostruito**, nemmeno dove l'atto gemello della stessa seduta lo rendeva banale. È la disciplina
giusta: ricostruire un testo cifrato è indovinare, e uno studio sulle fonti deve dire che quel
testo è illeggibile, non fingere di averlo letto.

**L'incoerenza dell'anonimizzazione della fonte, con prova interna.** Nello stesso lotto: un atto
anonimizza i bambini con codici numerici **motivando la scelta**, altri pubblicano cognomi e
persino **codici fiscali** di legali rappresentanti, due indicano minori con le sole iniziali.
Audit sui nostri 27 lotti: **nessun codice fiscale, nessuna partita IVA**, tutto reso con il ruolo.

**Due tensioni dichiarate e non risolte** dal lettore, che restano tali: nominare il datore di
lavoro accanto alla carica di consigliere restringe comunque il campo anche senza il cognome; e il
cognome di un collezionista, che resta perché identifica la collezione, compare anche nel nome
della donante, resa con il ruolo.

## 34. Il Municipio dei primi sei lotti riallineato (16 settembre, 05:50)

I lotti B01–B06 erano stati letti prima della correzione descritta in §24 e portavano ancora il
Municipio vecchio. `report2/fix_municipio_b01_b06.py` riscrive quella sola colonna dal file
`_municipio_corretto.csv`, che è la trascrizione del manifest, e lascia intatto tutto il resto:
**140 righe su 300 cambiate** (B01 47, B02 42, B03 2, B04 0, B05 0, B06 49). Nessuna riga senza
riscontro nel manifest: i 300 `name` sono tutti presenti.

Applicata la regola presa a caro prezzo in §29 — dopo una modifica in blocco si rilegge per intero
almeno una riga toccata — ho poi cercato, su tutti e sei i lotti, le note di coerenza che citano un
Municipio diverso dalla colonna. Ne restano **due**, ed entrambe sono giuste: un verbale del
Municipio IX che dice esso stesso che i tratti stradali chiusi ricadono nell'VIII, e un ordine del
giorno del Municipio V su un corteo previsto nel I. Non sono incoerenze introdotte dalla correzione,
sono esattamente la cosa che la colonna `coerenza_organo_territorio_o_nota` serve a registrare.

Una cosa che ho sbagliato e che vale la pena scrivere: ho riscritto i sei file **senza copiarli
prima**. La verifica è riuscita lo stesso, ma se la mappa di correzione fosse stata sbagliata non
avrei avuto il valore precedente per accorgermene. Da qui in avanti una modifica in blocco si fa
su una copia, non sull'originale.

## 35. Prova T1: quanto costa davvero trascrivere (16 settembre, 06:00)

Prima di qualunque lotto a pagamento, la prova prescritta da HANDOFF §4 su due ore di audio.
Scelte **4 registrazioni di 4 organi diversi e 2 settimane diverse** (Municipio XII, Commissioni
Capitoline, Municipio VIII, Municipio XV), per 2,12 ore complessive: una sola registrazione lunga
avrebbe misurato quella, non il corpus.

Catena: segmenti HLS cifrati → remux con la chiave AES → mono 16 kHz a 32 kbps → tagli allineati
ai silenzi vicino ai multipli di 5 minuti → `gpt-4o-mini-transcribe`.

| Misura | Valore |
|---|---|
| Audio trascritto | 127,0 minuti (2,12 ore), 26 pezzi |
| Token audio in ingresso | 76.199, cioè **600 al minuto, costanti** |
| Token di testo in uscita | 20.478 (161 al minuto) |
| Testo prodotto | 80.864 caratteri (636 al minuto) |
| Tempo di lavoro | 169 secondi, **45 volte più veloce del tempo reale** |
| Costo a token (3,00 / 1,25 / 5,00 $ per milione) | 0,331 $, cioè **0,00261 $ al minuto** |
| Costo allo stesso audio al listino a minuto (0,003 $) | 0,381 $ |

Il prezzo effettivo misurato è **il 13% sotto il listino a minuto**, perché la fatturazione a token
segue il parlato e non l'orologio. I 600 token audio al minuto sono identici su tutti e 26 i pezzi:
è una tariffa a durata, non a densità di parole.

Proiezioni: **35,6 $ (≈ 33 €)** per le 227,6 ore già in coda di scaricamento, **41,4 $ (≈ 38 €)**
per tutte le 328 sedute dell'8–28 giugno prive di trascrizione della piattaforma (264,6 ore). Il
tetto regge in entrambi i casi; il driver si ferma comunque da solo a 42 $.

**Due limiti da dichiarare nel rapporto, non da nascondere.**

1. La spesa reale non è leggibile da qui: l'API di fatturazione richiede una chiave di
   amministrazione che questa sessione non ha. Il costo sopra è calcolato sui token che l'API
   restituisce, moltiplicati per le tariffe di listino: è una misura del consumo, non della
   fattura.
2. `gpt-4o-mini-transcribe` non dà marcatori temporali. Li ricavo dal taglio: ogni pezzo porta il
   suo inizio in secondi, quindi l'evidenza è **al pezzo (circa 5 minuti)**, non ai 10 secondi che
   il metodo chiede per il lotto A. Il modello che li darebbe (`whisper-1`, `verbose_json`) costa
   il doppio, 82 $ sulle stesse ore, e sfonderebbe il tetto. Ho scelto la copertura completa con
   evidenza grossolana invece della copertura parziale con evidenza fine, e lo scrivo nel rapporto.

Il taglio sui silenzi funziona: alla giunzione fra il primo e il secondo pezzo la frase prosegue
intera, nessuna parola spezzata.

**Riservatezza.** Le trascrizioni sono piene di nomi — l'appello nominale apre ogni seduta. Restano
nello scratchpad come tutti i testi integrali (DEC-102); i lettori applicano l'anonimizzazione di
`SPECIFICA_ATTI.md` §nomi, che vale parola per parola anche qui.

## 36. 1.400 atti; una quota a zero che non significa una settimana vuota (16 settembre, 06:10)

Lotti B25–B27 rientrati: 150 atti su 150, **25 candidate (16,7%)**. Le tre quote singole sono
40%, 10% e **zero**, e la spiegazione non è nella soglia ma nella composizione: B26 e B27 sono
fatti per due terzi di convocazioni (47) e verbali (16). Un lotto di convocazioni produce zero
notizie perché convoca, non perché la settimana fosse povera — è la stessa cosa vista in §30,
ora nella sua forma estrema. La forbice spostando i casi limite: B25 32–44%, B26 8–20%,
B27 0–12%, complessivo 13,3–25,3%.

**Un atto che si legge solo insieme a un altro.** `A2_GMD_VIII_NDk5NA` conserva la sola pagina di
attestazione: la delibera è sparita, restano gli estremi. Il contenuto — otto strade nominate —
sta nel verbale di Giunta `A2_GMV_VIII_MzY1Mg`, che è in un lotto diverso. Il collegamento è
annotato in tutte e due le righe. È il secondo caso (dopo §32) in cui un difetto della fonte si
vede solo incrociando due lotti, e conferma che leggere gli atti a uno a uno non basta: il
database deve poterli mettere accanto.

**Aritmetica e tempo della fonte, ancora.** Municipio XIII dichiara 2.260.000 € a pagina 4 e
2.660.000 € in ogni altro punto dello stesso atto; un Commissario ad acta apre alle 14,35 e firma
«alle ore 11,35»; un percorso partecipativo si svolge otto mesi prima dell'assemblea che lo avvia;
un verbale del 17 giugno 2026 risulta approvato «der 20/4/2025»; tre atti della stessa seduta del
Municipio II nominano tre segretari diversi. Niente è stato conciliato: le due cifre stanno
entrambe nella riga.

**La fonte continua a contraddire la propria anonimizzazione.** In un atto i ricorrenti sono
coperti con «XXX» e in due punti dello stesso testo due dipendenti sono scritti per esteso. Il
lettore non li ha riprodotti, nemmeno in iniziali — la regola presa in §28 ha retto. Omessi anche
lotto, civico, scala e interni di due appartamenti con muffa che la fonte pubblica per intero:
restano le vie, che bastano a dire dove.

**Dove la soglia è una scelta.** Il lettore ha dichiarato otto coppie di atti simili con esito
diverso. La più istruttiva: un parere contrario motivato su un parcheggio è `sì`, un parere
favorevole a un restauro è `no` — perché il fatto nasce con il dissenso e non con l'adesione. E i
verbali di Giunta sono `sì` solo quando portano l'elenco delle strade che la delibera non porta.
Sono scelte difendibili, ma sono scelte, e stanno nei log perché il rapporto le possa mostrare.

## 37. La trascrizione è partita, con un tetto che si ferma da solo (16 settembre, 06:15)

`rtv_asr_driver.py` gira in sottofondo: prende le registrazioni man mano che finiscono di
scaricarsi, remuxa, riduce a mono, trascrive, e **cancella i segmenti e il file intermedio**
tenendo solo il mono a 32 kbps e il JSON. Senza questo il disco non basterebbe: 227,6 ore di
segmenti sono circa 10 GB, gli stessi minuti in mono ne occupano 3,3.

Il tetto è nel driver, non nella mia attenzione: ricalcola la spesa dai token restituiti
dall'API prima di ogni registrazione e si ferma a 42 $. Non è una stima sui minuti — è la somma
di quello che l'API ha detto di aver consumato.

## 38. Perché A1 è in tre parti, e come ho verificato che siano fedeli (16 settembre, 06:25)

Il connettore Drive carica **contenuto**, non file: il testo deve passare per la mia risposta, e una
risposta ha un tetto di lunghezza. `notizie_compatte_A1.csv` sta sotto quel tetto solo diviso in
tre. Non è una scelta editoriale: è il limite del canale, e lo scrivo perché l'owner non pensi che
il file sia stato tagliato per qualche criterio di contenuto.

- `Report1_notizie_A1_2026-06_parte1di3.csv` — N0001–N0175, 53.927 byte
- `Report1_notizie_A1_2026-06_parte2di3.csv` — N0176–N0350, 52.857 byte
- `Report1_notizie_A1_2026-06_parte3di3.csv` — N0351–N0524, 54.363 byte

Ogni parte porta la sua riga di intestazione, quindi ciascuna si apre da sola; concatenandole
saltando le due intestazioni ripetute si riottiene il file intero.

**La verifica.** Ricopiare 525 righe a mano è esattamente il modo di introdurre un errore
silenzioso, quindi non mi sono fidato della rilettura. Drive restituisce `fileSize`: ho confrontato
quel numero con i byte della porzione corrispondente del file locale. Tutte e tre coincidono **al
byte**.

Nel farlo è saltata fuori una differenza che valeva la pena capire: il file locale è scritto con
fine riga CRLF, il caricato con LF, e la differenza è esattamente **un byte per riga**. Non è un
danno — un CSV è valido in entrambi i modi — ma spiega perché `Report1_notizie_E3_2026-06.csv`
risulta su Drive di 43.577 byte contro i 43.730 locali: 153 righe, 153 byte. Anche quel
caricamento, fatto prima che me ne accorgessi, è fedele.

Il metodo vale per i due file grandi che restano (`notizie_compatte_E2.csv`, `documenti_compatti.csv`):
tre parti ciascuno, e il confronto sui byte come prova.

## 39. 1.650 atti, e una regola che ho cambiato mentre qualcuno stava leggendo (16 settembre, 06:45)

Lotti B31–B33 rientrati: 150 atti su 150, tutti `MMC`, **43 candidate (28,7%)**. Con questi il
totale è **1.650 atti letti e 396 candidate, il 24,0%** — la media che regge da venti lotti.

**Quello che ho fatto io, e che secondo le mie stesse regole non si fa.** La specifica di lettura
non si modifica mentre un lotto è in lettura: l'ho scritto in `SPECIFICA_LETTURA.md` dopo averlo
imparato sul Report 1. Qui l'ho violato: ho aggiunto l'emendamento MMC alla specifica e l'ho
mandato a un lettore **già in corsa**, che aveva chiuso i tre lotti con un criterio suo più largo.

Non me ne pento, ma va scritto perché è una scelta fra due danni. L'alternativa era lasciare che
sei lotti dello stesso identico tipo di atto — 300 convocazioni di commissione — fossero letti con
due soglie diverse: le percentuali non sarebbero state confrontabili fra loro né con il resto dello
studio, e la tabella del rapporto avrebbe mostrato una differenza di composizione dove c'era solo
una differenza di lettore. Ho preferito l'incoerenza dichiarata all'incomparabilità nascosta.

L'effetto è misurato, non stimato: il lettore ha **declassato 32 righe su 75** (9 in B31, 9 in B32,
14 in B33), **nessuna promossa**, scrivendo il motivo dentro la riga e l'elenco nei log. Da 50% a
28,7%. B33 è il più colpito perché conteneva i bandi scolastici e i punti sui centri estivi, che
l'emendamento tratta come temi generali senza luogo. Chi legge il rapporto deve sapere che quei tre
lotti sono stati letti due volte e che la seconda vale.

**La coppia che spiega meglio di ogni tabella quanto la quota dipenda dalla fonte e non dal
metodo.** Due atti della stessa commissione del Municipio VIII, gravemente mutili dallo stesso
scanner: in uno la riga che nomina il Polo Civico Ostiense ha retto l'OCR, nell'altro no. Il primo
è `sì`, il secondo `no`. Non è il merito dell'atto a decidere: è quale riga è sopravvissuta alla
scansione. Su 150 atti, **74 hanno il testo incerto** e solo 66 portano il marcatore OCR: gli altri
8 hanno lo strato di testo corrotto all'origine, tutti del Municipio XII.

**Dove il lettore ha forzato di più**, e ha fatto bene a dirlo: un atto che nomina la ciclabile
Colosseo-Ostia, i tratti, i parchi e l'unico importo dei tre lotti (18 milioni) è finito a `no`
perché si dichiara «posticipata», e l'emendamento esclude i posticipi. La differenza con il `sì`
gemello sta nella formula dell'oggetto, non nel fatto. È una regola che andrà discussa nel rapporto,
non nascosta in un log.

**La fonte continua a contraddirsi.** Giorni inesistenti (`139.06.2026`, `44/06/2026`,
`36/06/2026`), timbri datati 2006, 2008, 2020, 2025 e 2028 su atti del 2026, un protocollo che
contiene se stesso duplicato, due commissioni ancora intitolate al «Giubileo 2025» convocate nel
giugno 2026. Tre coppie di duplicati veri, lasciate separate e dichiarate. E due atti che
pubblicano **indirizzi di posta elettronica nominativi** al posto dei soggetti invitati: non
riprodotti da nessuna parte, come tutti gli altri identificatori.

Lanciati i quattro lotti finali B37–B40; con quelli la lettura degli atti si chiude.

## 40. Un solo database per i due rapporti, e un difetto che è rientrato da un'altra porta (16 settembre, 07:00)

Gli atti sono entrati nelle **stesse cinque tabelle** del Report 1, non in un database parallelo.
Ho esteso `report1/build_db.py` invece di scriverne un secondo, per la ragione già pagata una
volta: una regola di confronto tenuta in due copie diverge. E perché la domanda che il Report 2
deve poter rispondere — *quali notizie gli atti aggiungono a quelle delle fonti testuali* — si
risponde solo se le due metà stanno dentro lo stesso confronto.

Stato con 1.900 atti su 1.983 (mancano i lotti B36 e B40, in lettura):

| | righe |
|---|---|
| `documenti` | 2.885 (985 del Report 1 + 1.900 atti) |
| `notizie_candidate` | 1.734 (1.227 + **507 dagli atti**) |
| `vicende` | 304, di cui **52 solo dagli atti** |

Gli identificativi del Report 1 **non sono stati rinumerati**: il rapporto consegnato li cita, e
una rinumerazione silenziosa avrebbe reso false tutte le sue citazioni. Le candidate degli atti
partono da dove finivano quelle del Report 1.

**Il difetto.** La prima esecuzione ha dato 462 dubbi contro i 276 del Report 1 da solo: 186 dubbi
nuovi su 507 righe. Non era il ripiego sul Municipio che avevo già corretto — solo 10 coppie su
535 si appaiavano su quello. Guardando **quali toponimi tenevano insieme le coppie** è venuto
fuori: `municipio roma xii`, `municipio roma viii`, `sala fabio grossi`. I lettori scrivono in
`luoghi` anche **il nome del Municipio** e **l'aula in cui l'organo si riunisce**, e la regola li
prendeva per toponimi fini — scavalcando proprio la garanzia che avevo messo perché il Municipio
non appaiasse fatti diversi. Lo stesso difetto, rientrato da un'altra porta.

La correzione è stretta e sta nella regola, non nei dati: il nome di un Municipio non è un
toponimo, e `Sala…`, `Aula…`, `Sede…`, `Ufficio…`, `Sportello…` sono il posto dove l'organo si
riunisce, non ciò di cui l'atto parla. Dubbi fra atti da 186 a **142**.

**Conseguenza sul Report 1, che dichiaro invece di nasconderla.** La regola è condivisa, quindi
anche il Report 1 cambia: la resa netta passa da **882–1.158 a 885–1.161**, tre item su 1.227
(0,3%), tutti nella direzione di meno falsi duplicati. Gli atti non c'entrano: il confronto marca
sempre la riga successiva, e tutte le righe del Report 1 precedono quelle degli atti, quindi un
atto non può declassare una notizia del Report 1. È il solo effetto della regola nuova.

**Tre cose che ho trovato costruendo, e che vanno nel rapporto.**

1. **Il codice di tipologia della fonte non è documentato.** Ventisette sigle (DDS, MMC, MMV, CPC,
   AY, AZ, CMZ, CMY…). Non le ho dedotte dalle lettere: ho letto **un atto per ciascuna sigla** e
   costruito la mappa su organo emittente e oggetto. Quattro sigle (OCD, PMO, PMT, SO) non hanno
   ancora un esempio nei lotti letti: vanno in `altro` e il programma le stampa, invece di fingere
   di saperle.
2. **I lettori hanno scritto il formato a parole, non con l'enum della specifica**: otto
   formulazioni diverse per due soli casi reali («nativo», «PDF nativo», «PDF con testo», «PDF
   testo nativo», «testo nativo», «OCR», «PDF scansione (OCR Tesseract)», «PDF testo»). Stessa
   deriva su `esito_testo`. Normalizzati in modo deterministico, con la regola scritta nel codice.
3. **35 sintesi superano le 60 parole e 17 titoli le 12** che lo schema prescrive. Non le ho
   troncate: un taglio a metà frase è un danno peggiore di un limite superato, e la lezione di §29
   vale anche qui. Sono contate e dichiarate.

## 41. Tutti e 1.983 gli atti letti, e un esperimento naturale sui lettori (16 settembre, 07:20)

Lotti B34–B36 rientrati e lotti B37–B40 scritti: **1.983 atti su 1.983, nessuno saltato,
544 candidate (27,4%)**. Il database sta a **2.968 documenti, 1.771 candidate, 311 vicende** (58
nate solo dagli atti), resa netta **1.266–1.700**.

**La quota dipende dal tipo di atto, non dalla soglia**, e ora si può misurare invece di dirlo:

| sigla | che cos'è | atti | quota |
|---|---|---|---|
| `MMV` | verbali di commissione municipale | 312 | **46%** |
| `CMR` | risoluzioni di Consiglio municipale | 30 | 40% |
| `MMC` | convocazioni di commissione | 386 | 24% |
| `DDS` | determinazioni di traffico | 682 | 23% |
| `DMS` | determinazioni municipali | 131 | 21% |
| `CPC` | convocazioni di commissione capitolina | 76 | 17% |
| `AY` | ordini del giorno dell'Assemblea | 60 | 8% |
| `CMC` | convocazioni di Consiglio municipale | 47 | **4%** |

Fra il 4% delle convocazioni di Consiglio e il 46% dei verbali ci sono 42 punti, e non è una
differenza di lettore: una convocazione annuncia una seduta, un verbale dice che cosa vi è
successo. Chi misura «quante notizie contengono gli atti di Roma» senza dire *quali* atti ha letto
non sta misurando niente.

**L'esperimento naturale.** La specifica non aveva una regola per i verbali `MMV` — come non
l'aveva per le convocazioni. Stavolta però **due lettori diversi ci sono arrivati
indipendentemente**, senza che io passassi niente dall'uno all'altro: B34–B36 ha prodotto 46%, 54%,
50%; B37–B39 ha prodotto 38%, 40%, 44%. Media 50% contro 40,7%.

Questo è il numero che mancava allo studio: **lo scarto fra due lettori sullo stesso tipo di atto
è di circa 9 punti**, mentre lo scarto fra tipi di atto è di 42. La composizione conta quattro
volte più del lettore — ma il lettore non conta zero, e la forbice del rapporto deve dirlo. Qui
**non ho imposto un criterio comune a posteriori**: rileggere per uniformare avrebbe distrutto
l'unica misura indipendente che ho della variabilità fra lettori. Il prezzo è che i verbali sono
letti con due soglie leggermente diverse, e lo dichiaro.

**Il lettore ha omesso più di quanto l'owner abbia deciso, e va rimesso a posto.** Oltre ai civici
ha tolto **i nomi degli artisti in cartellone** e **i nomi delle persone commemorate nelle
intitolazioni**. Le decisioni D1 e D3 dicono l'opposto: il nome dentro un toponimo, un locale o
un'opera resta, e una dedica o una commemorazione conserva il nome, perché è il fatto. È una
perdita di precisione dichiarata dal lettore stesso — da segnare fra i limiti del Report 2, non da
correggere a mano riga per riga senza rileggere gli atti.

**Quello che la fonte fa a chi ci finisce dentro.** Un verbale di Commissione Pari Opportunità
nomina per esteso la persona audita, un suo familiare, il titolo del libro che identifica
entrambi e l'esito giudiziario a carico del familiare, dentro il racconto di una violenza
domestica. Un altro riporta la condizione di salute di un alunno di una classe individuata in una
scuola nominata. Tre verbali scrivono «Omissis» per una persona e poi la descrivono in modo che
l'omissis non serva a niente («titolare di un asilo nido in prossimità dell'area verde»). Nulla di
tutto questo è nelle colonne. Ma è pubblicato, e il rapporto deve dirlo: **la fonte non protegge
le persone che nomina, e chi la riusa eredita il problema.**

**Difetti di forma, invariati per volume.** 73 atti su 150 con testo incerto nei soli B34–B36, di
cui **20 senza marcatore OCR e tutti e venti del Municipio XII**: in tre lotti non c'è un solo
verbale di quel municipio con lo strato di testo integro. Timbri datati 2025 e 2028 su atti del
2026; una seduta aperta alle 14,00 e chiusa alle 11.33; «con tre (4) voti favorevoli»; elenchi di
voto che comprendono chi non risulta presente; due verbali distinti della stessa commissione per
lo stesso giorno, con segretari e ordini del giorno diversi, lasciati separati.

## 42. La notizia che non possiamo scrivere perché la fonte l'ha pubblicata male (16 settembre, 07:35)

Consegna dei lotti B37–B40: 183 atti, 73 candidate (39,9%), forbice 32,2–53,6%. I numeri sono già
in §41; qui sta la cosa che non avevo ancora visto in nessun lotto.

**Tre ordinanze del Sindaco pubblicate all'Albo Pretorio** (`CEN_SO_X_NzQ5NA`, `NzQ5NQ`, `NzQ5Ng`)
riportano, per ciascun destinatario: nome, luogo e data di nascita, codice fiscale, indirizzo con
civico, scala, piano e interno, la condizione personale e — in un caso — un procedimento di tutela
di persone fragili. Una quarta (`CEN_SO_X_NzUwMQ`) porta anagrafica, residenza e riferimenti
catastali; lì il lettore non ha riportato **nemmeno le denominazioni delle due società**, perché
sono formate sui nomi delle persone parti del procedimento. È la scelta giusta e va oltre la
lettera di D2: una ragione sociale che è il nome di chi ci sta dentro non è un'organizzazione, è
una persona con un'altra etichetta.

**Quello che ne segue per il metodo, e che va nel rapporto.** Le tre ordinanze di bonifica sono
dello stesso giorno, sulla stessa strada, dentro un progetto di rigenerazione nominato. Lette in
serie **sono un fatto di quartiere**. Il lettore le ha tenute a `no` per due ragioni: la regola
chiede un cambiamento per chi abita il quartiere e qui l'effetto si ferma a un alloggio; e DEC-102
rende quel racconto non scrivibile senza re-identificare persone fragili. Da sole spostano B40 dal
36,4% al 45,5%.

Qui la nostra regola di riservatezza e il difetto della fonte si sommano: **una notizia esiste,
è pubblica, ed è fuori dal nostro conteggio perché la fonte l'ha pubblicata in un modo che non si
può anonimizzare restando una notizia.** Non è una perdita da nascondere in una forbice: è un
risultato dello studio. Un giornale che volesse quella storia dovrebbe raccoglierla altrove, non
dall'Albo.

**Due limiti del database emersi dallo stesso lotto.**

1. `A2_MMV_I_NjE3ODI` e `A2_MMV_I_NjEyNjE` sono **lo stesso verbale con lo stesso protocollo**,
   pubblicato due volte. Nessuno dei due è candidata, quindi la deduplicazione non li vede mai:
   il duplicato esiste solo a livello di `documenti`. La resa netta non ne risente, ma
   l'inventario del mese conta due volte un atto che è uno solo, e il rapporto deve dirlo.
2. I verbali gemelli della stessa seduta congiunta (`VIII_NjExMzg` / `VIII_NjI1MDk`) producono due
   candidate che il confronto lega entrambe a una terza riga precedente, non l'una all'altra:
   finiscono nella stessa vicenda, ma `gemello_id` non punta al gemello più vicino. È come
   funziona la regola — si ferma al primo riscontro utile — e va letto sapendolo.

**Aritmetica della fonte, nuova forma.** Quattro verbali del Municipio XIV dichiarano
«unanimità dei votanti» **in presenza di astenuti**; uno proclama un parere non favorevole senza
un solo voto contrario; due elencano meno cognomi dei voti dichiarati. E in un verbale del XII la
direzione municipale attribuisce un'area giochi al dipartimento e il dipartimento al municipio,
mentre l'area resta pericolosa: la contraddizione non è formale, è la ragione per cui non ci
mette mano nessuno.

## 43. Le registrazioni: 97 sedute in finestra, e un indicatore di qualità che vale zero (16 settembre, 06:45)

*(Nota sulle ore: i §§41 e 42 portano un orario di Roma sbagliato di una quarantina di minuti,
scritto a occhio invece che letto. Da qui in avanti è preso dall'orologio.)*

Chiusa la lettura degli atti, la seconda metà del Report 2 sono le registrazioni. Stato:

- **130 didascalie YouTube convertite in testo** con i marcatori a **10 secondi** che il metodo
  chiede per il lotto A (`caps_to_text.py`): 128,6 ore, 769.226 parole. Incrociate con il
  censimento e ristrette alla finestra 8–28 giugno restano **97 sedute, 607.627 parole**, in
  `report2/manifest_video.csv`. Le 33 fuori finestra restano disponibili ma non entrano nel
  rapporto.
- **Trascrizioni della piattaforma RomaTV**: 50 delle 82 scaricate, il resto in corso.
- **Trascrizione a pagamento delle commissioni RomaTV**: 77 registrazioni, 55,6 ore, 8,02 €.

**L'indicatore di qualità di YouTube è inservibile, e va detto.** Il formato `json3` porta un campo
di confidenza per parola (`acAsrConf`). Su 129 video su 130 la mediana è **0,000** — e guardando
dentro il primo file il campo c'è su tutti e 1.245 i segmenti e vale **zero su tutti**. Non è
«bassa confidenza»: è un campo compilato a zero. Chi lo usasse come filtro scarterebbe tutto, chi
lo usasse come soglia non filtrerebbe niente. È lo stesso schema del marcatore OCR negli atti: il
marcatore non dice la verità sul testo, quindi **si giudica il testo**. Le trascrizioni RomaTV, al
contrario, portano confidenze vere (media 0,84–0,87 sui primi campioni).

**La specifica di lettura** è `report2/SPECIFICA_VIDEO.md`, derivata dallo schema del lotto A con
tre aggiunte: marcatori a 10 secondi; **ogni candidata deve portare almeno un `[mm:ss]`**, perché
senza il punto della registrazione non è verificabile; e il campo
`novita_rispetto_agli_atti` — `solo dal parlato` / `anche negli atti` / `non verificabile` — che è
la domanda per cui il Report 2 esiste: che cosa si sente in aula e non sta scritto da nessuna
parte. Il controllo si fa sui materiali locali, senza rete.

Una regola in più rispetto agli atti, perché un'aula non è un fascicolo: **il parlato personale che
attraversa una seduta — liti, stati di salute, vicende private citate da chi interviene — non entra
nei file nemmeno in forma anonimizzata**, a meno che non sia esso stesso l'oggetto di una decisione
dell'organo. Negli atti il problema era la fonte che pubblica troppo; qui è il microfono acceso.

Avviati i primi due lotti di lettura (V4_001–V4_024).

## 44. 32 notizie su 42 esistono solo nel parlato (16 settembre, 07:10)

Primo lotto di registrazioni rientrato, V4_013–V4_024: 12 sedute, 6 ore e 21 minuti, 48.766 parole,
**42 candidate di cui 32 `solo dal parlato`**. Il lettore ha verificato che **tutti e 111 i
marcatori `[mm:ss]` citati come evidenza esistono davvero** nelle trascrizioni: un'evidenza
inventata sarebbe peggio di una notizia mancata, e il controllo va chiesto sempre.

**Il mio errore, e la correzione.** La specifica mandava a verificare `novita_rispetto_agli_atti`
su `deliver/A2_2026-06_items.csv`, che **non porta l'oggetto degli atti**: solo tipologia,
municipio e data. Con quel materiale il riscontro è strutturalmente impossibile per quasi ogni
affermazione — il lettore lo ha segnalato invece di far finta di aver verificato, ed è la cosa
giusta che poteva fare. Nel frattempo però esistono i 1.983 atti letti: ho generato
`report2/confronto_atti.csv` (organo, oggetto, luoghi, titolo della candidata) e ho emendato la
specifica perché i lotti successivi usino quello e `notizie_candidate.csv`. **I primi due lotti e i
seguenti non sono confrontabili su quel campo, e il rapporto deve dirlo**: il 76% di
`solo dal parlato` di V4_013–V4_024 è un valore ottenuto con un riscontro debole, quindi un limite
superiore.

**Quello che si vede solo ascoltando.** È la parte che nessun atto contiene, e da sola giustifica
il Report 2: numero legale mancato due volte nello stesso consiglio (sei presenti al primo appello,
undici al secondo, la seduta si apre al terzo) mentre negli atti resta **un solo verbale**; un
appello che non torna, con «sette presenti, sette favorevoli» e un cognome verbalizzato due volte;
**due consiglieri che votano senza sapere su che cosa** — uno chiede a votazione in corso di quale
delibera si tratti e poi vota a favore; presenze e voti dati in chat; verbali approvati dopo una
sospensione chiesta da chi non li aveva letti; **la verbalizzante che dichiara in diretta di non
riuscire a verbalizzare un'audizione di un'ora e un quarto perché non sente.**

**La trascrizione automatica sbaglia dove conta.** Lo stesso rione in tre grafie in dieci minuti;
una sigla sanitaria in quattro forme in quattro minuti; un importo di spesa con un numero
appiccicato in coda; un requisito ISEE fuori scala; anni a quattro cifre troncati a tre; il nome di
un'azienda fuso con la sigla della municipalizzata, così che **dal solo testo non si sa chi doveva
fare il lavoro**; una sigla compitata lettera per lettera in aula perché nessuno la capiva, e
trascritta lo stesso in due modi diversi.

**Riservatezza: il microfono è il problema, come previsto.** Il lettore ha tolto — e non ha
riprodotto nemmeno nel log — il civico e il nome di una richiedente privata letti ad alta voce in
aula, **con la presidenza che dichiarava la privacy «ridondante»**; un malore in diretta; dove vive
oggi una persona citata in un elenco commemorativo. Ha però segnalato un punto in cui la regola
toglie precisione senza proteggere nessuno: il divieto di civici applicato a una **sede pubblica**.
Ha ragione, e va deciso: un civico che indica uno sportello comunale non identifica una persona.

**Una discrepanza del manifest** da verificare: per tre spezzoni del Consiglio del Municipio I il
`convocazione_match` punta a un documento la cui numerazione non compare fra le convocazioni di
giugno.

## 45. Le prime 24 sedute, e un difetto del censimento misurato (16 settembre, 07:25)

Rientrato anche V4_001–V4_012: 12 sedute, 12 ore e 56 minuti, 73.511 parole, **64 candidate, 56
`solo dal parlato` (87,5%)**. Con il lotto precedente: **24 sedute, 106 candidate, 88 solo dal
parlato**.

**Quel 87,5% è un limite superiore, e il lettore lo ha detto prima che glielo chiedessi.** Con
`A2_2026-06_items.csv` — nessun titolo di atto — il «non compare negli atti» è *un'assenza di
prova, non una prova di assenza*. Due lettori diversi sono arrivati alla stessa conclusione
indipendentemente. Dal terzo lotto in avanti il riscontro si fa su `confronto_atti.csv`, che porta
l'oggetto di tutti e 1.983 gli atti: il numero che ne uscirà sarà più basso e più difendibile, e i
due gruppi di lotti vanno tenuti separati nel rapporto.

**Il censimento sbaglia ad abbinare le convocazioni, e ora so di quanto.** Un lettore ha notato che
due registrazioni dell'8 giugno condividono la stessa convocazione pur essendo commissioni diverse.
Il primo controllo che ho scritto non l'ha visto, perché la colonna `organo` del manifest dice
«Commissione» per tutte e non distingue quale. Rifatto il controllo **sui titoli del censimento**:
su 78 registrazioni con una convocazione abbinata, **4 abbinamenti su 8 registrazioni sono
sbagliati** — Lavori Pubblici con la congiunta Cultura-Ambiente, Commercio con la congiunta
Cultura-Commercio, Politiche Sociali con la congiunta Pari Opportunità. Gli altri quattro gruppi
condivisi sono legittimi: sono sedute spezzate in più video (primo, secondo e terzo appello dello
stesso consiglio). Circa il **5% degli abbinamenti automatici è falso**, e va dichiarato invece di
lasciarlo usare.

**L'Assemblea Capitolina del mese, ascoltata.** Tre appelli falliti di fila — 7 presenti su 49, poi
14, poi 20 — e il numero legale raggiunto solo al quarto, **dopo 2 ore e 23 minuti**, con 28
presenti. La discussione generale sul piano degli arenili viene poi sospesa e chiusa **senza voto,
«visto l'orario»**; più ordini del giorno decadono perché i firmatari non ci sono. Nell'atto
pubblicato di tutto questo resta una riga.

**E dentro le commissioni:** un parere che non passa perché 3 favorevoli, 3 astenuti e 2 non
partecipanti su 8, con la presidenza che se ne accorge facendo i conti a voce; una commissione che
si chiude constatando che alla domanda su quella scuola **nessuno ha risposto**, perché il
dipartimento invitato non si è presentato; una seduta convocata per errore su un parere assegnato
ad altra commissione; l'esame delle determinazioni dirigenziali, che era l'oggetto della seduta,
svolto nei 22 minuti in cui il microfono è muto.

**Aperta la decisione D5** in `DECISIONI_OWNER.md`: tre lettori diversi hanno segnalato che il
divieto di civici, applicato alle **sedi pubbliche**, toglie precisione senza proteggere nessuno —
due immobili comunali contigui messi a bando diventano indistinguibili. La raccomandazione è tenere
il civico quando individua una sede o un immobile pubblico. Fino alla decisione i lettori applicano
il divieto senza eccezioni.

## 46. Il parlato nel confronto, e una misura che non dipende dal giudizio del lettore (16 settembre, 07:45)

Anche le registrazioni entrano nelle stesse cinque tabelle, per la stessa ragione degli atti: la
domanda del Report 2 — *che cosa si sente in aula e non sta scritto* — si risponde solo mettendo il
parlato dentro lo stesso confronto, non in un database accanto. Con 47 sedute lette il database sta
a **3.015 documenti, 2.019 candidate, 340 vicende**, netta 1.404–1.944.

**E qui viene la cosa interessante.** Il lettore dichiara riga per riga se una notizia sia `solo dal
parlato`, `anche negli atti` o `non verificabile`: è un giudizio. La deduplicazione invece confronta
meccanicamente date, luoghi e oggetti contro tutte le altre 1.771 candidate. Sono due misure
indipendenti della stessa cosa, e si possono incrociare.

Sulle 248 candidate uscite finora dalle registrazioni:

| dichiarazione del lettore | senza riscontro nel confronto | con un gemello per data e luogo |
|---|---|---|
| `solo dal parlato` (168) | 102 | **66** |
| `anche negli atti` (48) | **24** | 24 |
| `non verificabile` (32) | 12 | 20 |

I due metodi **non dicono la stessa cosa**, e in entrambe le direzioni: 66 notizie che il lettore
dà per nuove hanno comunque un candidato della stessa data e dello stesso luogo fra gli atti (58)
o fra le fonti testuali (22); e 24 che il lettore dà per già scritte non hanno alcun gemello.

Non è un errore di nessuno dei due. Un `dubbio` dice «stessa data, stesso luogo, oggetto incerto»:
è un motivo per andare a guardare, non una prova che sia la stessa notizia. Ma permette di dare al
rapporto **un intervallo che non dipende dal giudizio di chi legge**: fra le candidate dal parlato,
quelle senza alcun riscontro altrove sono **102 su 248 (41%)**; quelle che il lettore giudica nuove
sono 168 (68%). La verità sta in mezzo e i due estremi sono entrambi misurati.

**Una scelta di sequenza.** I caricamenti su Drive sono sospesi fino a quando il database non è
fermo. Ho già caricato A1 una volta e l'ho reso obsoleto due volte in mezza giornata — prima
cambiando le colonne, poi togliendo le citazioni da `evidenza_locale`; e adesso l'ingresso delle
registrazioni cambia lo stato di deduplicazione anche delle righe del Report 1. Caricare a database
in movimento significa mettere sul Drive dell'owner file che si contraddicono fra loro. Si carica
una volta sola, alla fine, con la verifica sui byte parte per parte.

## 47. Il verbale che esiste ed è vuoto (16 settembre, 08:00)

Rientrato V4_025–V4_036, il primo lotto letto con il riscontro vero sui 1.983 atti: 12 sedute,
17 ore e 17 minuti, 87.699 parole, **85 candidate di cui 61 `solo dal parlato` (72%)**, forbice
65–103. Il numero non è crollato passando dal riscontro debole a quello vero — era 87,5% e 67,7%
nei primi due lotti, è 72% qui — ma adesso **si può sostenere invece di supporre**.

**E si può sostenere per una ragione che non avevo previsto.** Il lettore ha guardato non solo *se*
il verbale della stessa seduta esista, ma *se contenga qualcosa*. Per due commissioni del Municipio
I del 12 giugno il verbale risulta agli atti **privo di qualsiasi contenuto verbalizzato**. Quindi
le date di riapertura dei tre nidi, la variante che elimina il pavimento radiante e i diecimila
euro di bilancio per le pari opportunità **esistono solo nella registrazione**, e non perché non
abbiamo cercato: perché l'atto che dovrebbe contenerli è una scatola vuota. Lo stesso per un
verbale troncato e per una seduta senza alcun verbale.

Dove invece il verbale è pieno — la commissione sport del Municipio IX, la trasparenza del IX — il
lettore ha dovuto scrivere `anche negli atti` quasi ovunque. **Il riscontro vero funziona in
entrambe le direzioni, ed è questo che lo rende una misura.**

**Gli atti registrano solo ciò che passa.** Nell'Assemblea Capitolina del lotto sono stati votati
**138 ordini del giorno**, e solo **47 sono diventati atti**: i respinti non lasciano traccia
documentale. Chi ricostruisse il mese dai soli atti vedrebbe le decisioni e non le proposte, e non
avrebbe modo di accorgersene.

**La stessa seduta, misurata.** 6 ore e 21 minuti dichiarate per 10.551 parole: **28 parole al
minuto**, contro le 109–155 delle sedute normali. Almeno 2 ore e 20 di silenzio in tredici buchi,
il più lungo di **41 minuti**. Primo appello: sette presenti su quarantotto; secondo diciotto;
lavori aperti solo al terzo, un'ora dopo. Alle 15 la seduta è tolta con il piano degli arenili
fermo agli emendamenti. E durante i voti: «Votanti 24, favorevoli 25», corretto nella stessa frase;
un esito ribaltato dopo l'annuncio, con richiesta di mettere a verbale un voto sbagliato; la
numerazione degli ordini del giorno che salta da 28 a 30, da 48 a 50, da 58 a 63; e un voto tenuto
lo stesso dopo che la presidenza ha chiesto a voce **«Deliberato di che? Eh, c'è un problema»**.

**Un titolo sbagliato alla fonte.** Il canale istituzionale pubblica una registrazione intitolata
«Assemblea Capitolina giovedì 11 giugno 2026»; dentro c'è la conferenza nazionale dei presidenti
dei consigli comunali, e chi apre dice «oggi il 12 giugno». Il nostro manifest riporta fedelmente
quello che il canale ha pubblicato: **l'errore è della fonte, non del censimento**, e il lettore ha
fatto la cosa giusta lasciando i valori del manifest e segnalando la discordanza invece di
correggerla da sé.

**Una nota sul mestiere.** Il lettore ha verificato tutti e 291 i marcatori `[mm:ss]` citati come
evidenza, e nel farlo ha scoperto che **il suo stesso verificatore sbagliava** su un'espressione
regolare che non contemplava i minuti a tre cifre: falsi allarmi su una seduta di sei ore. Ha
corretto il verificatore, non i dati. È esattamente il modo in cui questi controlli vanno fatti —
quando un controllo e un dato non concordano, il primo sospettato è il controllo.

Database con 48 registrazioni dentro: **3.016 documenti, 2.025 candidate, 340 vicende**; delle 254
candidate dal parlato, **144 non hanno alcun riscontro nel confronto meccanico**.

## 48. Quattro lotti, quattro risposte diverse alla stessa domanda (16 settembre, 08:20)

Rientrato V4_037–V4_048: 12 sedute, 13 ore e 58 minuti, 75.815 parole, **63 candidate di cui 25
`solo dal parlato` (40%)**, forbice 53–78.

**Quel 40% contro il 72% del lotto precedente non è una differenza di territorio: è una differenza
di lettura, e il lettore l'ha isolata lui stesso.** Il caso in discussione è preciso: *esiste il
verbale della stessa seduta, ma il luogo di cui si parla non è fra quelli che l'atto elenca*. Questo
lettore ha scelto `non verificabile` — «non rivendico una novità che senza rete non posso
dimostrare» — e sono **undici notizie**; con la lettura opposta il `solo dal parlato` salirebbe da
25 a 31 su 63.

Messi in fila i quattro lotti: **87,5% — 67,7% — 72% — 40%**. I primi due con riscontro debole, gli
ultimi due con quello vero; e fra gli ultimi due la differenza è tutta in questa scelta. Ne seguono
due cose per il rapporto:

1. **Il numero dichiarato dai lettori non è una misura stabile.** Va dato come intervallo e va detto
   da che cosa dipende.
2. **La misura stabile è quella meccanica**: quante candidate dal parlato non hanno alcun gemello
   per data e luogo in tutto il corpus. Non dipende dal giudizio di chi legge, e oggi dice
   **144 su 254**.

Al lotto successivo ho dato la regola esplicita — se il verbale esiste ed elenca i suoi oggetti e
il luogo non c'è, è `solo dal parlato`, perché *l'atto ha avuto l'occasione di dirlo e non l'ha
detto* — chiedendo di **contare a parte** quante notizie ci cadono. Così la differenza fra i lotti
resta misurabile invece di sparire in una media.

**Il censimento trova meno di metà dei verbali che esistono.** Il lettore ha notato tre
registrazioni con `verbale_match` vuoto nel manifest il cui verbale però sta negli atti. Misurato:
per **34 registrazioni esiste un solo verbale possibile** (stesso Municipio, stessa data, nessuna
ambiguità), e il manifest **non ne dichiara 26**. Tre su quattro dei casi facili, mancati. Per altre
55 registrazioni ci sono più verbali lo stesso giorno e l'abbinamento non è decidibile così; per 8
non c'è alcun verbale. Il collegamento automatico fra registrazione e atto, quindi, **sbaglia
quando abbina (4 casi su 78, §45) e soprattutto non abbina quando potrebbe**.

**La prova più netta del lotto.** Per una seduta il verbale è registrato «di sola presenza, senza
sintesi degli interventi»: le sei notizie che ne escono — 483 domande per 652 posti nelle scuole
dell'infanzia, 505 domande per 348 posti nei nidi con 136 bambini in lista d'attesa, una scuola
dell'infanzia che scende da due sezioni a una, un nido chiuso circa 200 giorni, sette nidi ridotti o
sfollati, due strutture restituite a fine settembre — sono **tutte solo nella registrazione**. E
quaranta minuti di discussione unanime contro una proposta capitolina stanno in un verbale «senza
contenuto verbalizzato».

**Una data che non torna, verificata.** In aula si dice «commissione trasparenza del 13 luglio
2026», il manifest dice 13 giugno; tutti i riferimenti interni («venerdì 24», «fino al 7 che è il
venerdì», «buon inizio settimana») concordano con luglio. Ho controllato il calendario: **il 13
giugno 2026 è un sabato, il 13 luglio un lunedì**. Il lettore ha lasciato il valore del manifest e
segnalato la discordanza, che è la regola giusta; ma il dato del censimento qui è quasi certamente
sbagliato.

**E il resto delle sedute.** Un consiglio municipale che **decade** perché un gruppo resta in aula
ma fuori dal numero legale, e la mozione passa alla seduta successiva «senza discussione»;
presenze registrate in chat senza voce; un'interrogazione discussa dopo cinque settimane invece che
entro quindici giorni; tre verbali approvati dichiarando che non c'erano modifiche e poi approvati
«con le modifiche» di cui il presidente aveva appena detto di non avere contezza; tre debiti fuori
bilancio approvati senza un solo intervento, con il sistema di voto che si guasta e una votazione
annullata.

## 49. RomaTV in testo: 206 sedute e due gradi di verificabilità (16 settembre, 08:30)

Convertite in testo tutte le registrazioni RomaTV disponibili (`rtv_to_text.py`): **82 dalla
piattaforma** (73,8 ore) e **143 trascritte da noi** (101,4 ore). Ristrette alla finestra 8–28
giugno restano **206 sedute, 157,7 ore, 958.809 parole**, in `report2/manifest_video_rtv.csv`.
Con le 97 di YouTube il corpus parlato del Report 2 sta a **303 registrazioni e circa 1,57 milioni
di parole** — e crescerà, perché lo scaricamento è a 198 su 318.

**Le due origini non danno la stessa evidenza, e la differenza è scritta nel manifest.** La
piattaforma restituisce parola per parola con tempo e confidenza veri: marcatore **ogni 10
secondi**, come chiede il metodo, e una confidenza utilizzabile (mediana 0,84–0,87), all'opposto
dello zero di YouTube. Il modello che abbiamo pagato non restituisce tempi interni: il marcatore
cade all'inizio di ogni pezzo, **circa ogni 5 minuti**. Su quelle registrazioni l'evidenza
individua un intervallo, non un punto.

Non è un difetto da nascondere in una nota: è il prezzo della scelta fatta in §35 — copertura
completa con evidenza grossolana invece di copertura parziale con evidenza fine. La specifica ora
lo dice, il manifest porta `grana_marcatore_s` riga per riga, e i lettori devono dichiarare
separatamente le candidate delle due origini, perché **non sono verificabili allo stesso modo**.

Ledger aggiornato: 14,96 € spesi, **63,04 € disponibili**.

## 50. Otto giorni di istruttoria che esistono solo nel parlato (16 settembre, 08:45)

Rientrato V4_049–V4_060: 12 sedute, 7 ore e 24 minuti misurate sui marcatori, 58.222 parole,
**43 candidate di cui 30 `solo dal parlato`**, forbice 34–53.

**Il caso del dossier librerie.** Il Municipio I ne discute il 16, il 17, il 23 e il 24 giugno. Dei
quattro verbali, **tre non hanno contenuto** e uno solo — quello del voto contrario del 24 — dice
qualcosa. Otto giorni di istruttoria pubblica, con sopralluoghi e audizioni, **sopravvivono solo
nelle registrazioni**. Non è un caso isolato del lotto: in sei sedute su dodici l'unica traccia
scritta è la presenza o l'esito, e per due sedute non esiste alcun verbale fra i 1.983 atti di
giugno, pur esistendo quelli di altre commissioni degli stessi giorni.

**Una notizia che nasce da una smentita, e che gli atti confermano.** In una commissione
l'assessorato apre dicendo che il cantiere chiude «venerdì»; una residente obietta; a fine seduta
l'assessorato si corregge, dopo aver sentito l'impresa. **L'atto `DDS_DDS_I_NzEwODg` del 25 giugno,
che proroga quella disciplina di traffico, dà ragione alla residente.** È il primo caso in cui il
parlato e l'atto si controllano a vicenda invece di ripetersi: la notizia non è il cantiere, è la
smentita — e non esiste in nessun atto.

**La trascrizione sbaglia proprio dove sta la notizia.** Otto grafie per Porta Asinaria in
cinquantadue minuti, nessuna corretta. **Dieci grafie per via del Casale di Zola**, che è l'oggetto
stesso della seduta. «Palestre nei parchi del municipio €9» per «municipio 9». Le compensazioni
arboree lette come «166 e più alberi qui sono essenze le 166 gli alberi sono 15». E dentro i
silenzi la piattaforma inventa: il primo appello di un consiglio si apre su «schifo».

**Il collegamento fra registrazione e atto, ora esatto.** Il lettore ha trovato la chiave: il
`par2` in base64 dentro `verbale_match` è **l'ultimo segmento del `name` dell'atto**. Ho scritto
`collega_video_atti.py`, che produce `report2/video_atti.csv` a fianco del censimento senza toccarlo,
e il quadro su tutte e 303 le registrazioni è questo:

| | convocazioni | verbali |
|---|---|---|
| abbinamento esatto dal censimento | 70 | 38 |
| di cui puntano a un atto **di un altro Municipio** | **6** | 0 |
| di cui puntano a un atto **che non è fra i 1.983 di giugno** | **8** | 0 |
| senza abbinamento, ma con **un solo** atto compatibile | 43 | **63** |
| senza abbinamento, con più atti compatibili nello stesso giorno | 82 | 129 |

Quattordici abbinamenti su settantotto, il **18%**, sono sbagliati o non verificabili; e per 63
registrazioni esiste un verbale univoco che il censimento non dichiara. Da ora i lettori hanno il
collegamento esatto dove c'è e l'elenco dei compatibili dove non c'è, **senza che il programma ne
scelga uno**.

**Una durata che falsa una misura.** Per tre registrazioni il manifest dichiara `0:01` a fronte di
circa un minuto e mezzo reale: le parole al minuto risultano gonfiate del 40–70%. È un dato del
censimento che entra nelle nostre statistiche, e va corretto o dichiarato prima di pubblicarle.

**E il mestiere, di nuovo.** Il lettore ha verificato 204 marcatori nei file e **115 nel proprio
log**, trovando e correggendo due proprie citazioni sbagliate. Ha inoltre fatto la scansione DEC-102
su novanta cognomi sentiti in aula: zero occorrenze nei file, e i quattro allarmi erano toponimi
(«Santa Croce in Gerusalemme», «Santo Stefano Rotondo», «via Bonelli») e la parola «Primo appello».

## 51. La regola che avevo scritto io era sbagliata, e si vedeva nei numeri (16 settembre, 09:00)

Rientrato V4_061–V4_072: 12 sedute, 10 ore e 27 minuti, 79.075 parole, 48 candidate. Ma delle 48,
**solo 8 sono `solo dal parlato` e 33 sono `non verificabile`** — contro il 72% e il 40% dei lotti
precedenti. Non è il territorio che cambia: è la regola che ho scritto io.

**Che cosa avevo sbagliato.** Nel prompt del lotto avevo messo due frasi che si contraddicono: una
elencava il verbale «di sola presenza» fra i casi da marcare `non verificabile`, l'altra diceva che
proprio lì il `solo dal parlato` è dimostrato. Il lettore l'ha isolata, ha applicato quella che gli
avevo ordinato di applicare, e **ha misurato anche l'altra lettura**: con quella, le sue 8
diventerebbero 12.

Ma il difetto vero è più profondo di una contraddizione. La mia regola faceva dipendere il giudizio
**dall'esistenza del verbale della seduta**, e la domanda non è quella. Come ha scritto il lettore:
sette sedute su dodici non hanno verbale negli atti di giugno, quindi 33 candidate risultano
`non verificabile` **benché il fatto non compaia in nessuno dei 1.983 atti** — che è esattamente la
definizione di `solo dal parlato`. La sua coppia numero 6 lo dice meglio di me: due fatti ugualmente
documentati, entrambi assenti da tutti gli atti, uno finisce `non verificabile` e l'altro `solo dal
parlato`, e l'unica differenza è che la seconda seduta ha un verbale e la prima no.

**Correzione, nella specifica.** `solo dal parlato` = il fatto non compare in nessun atto né fra le
notizie estratte, **a prescindere dallo stato del verbale**. `non verificabile` = soltanto per
documenti fuori dal nostro corpus: sentenze, pareri di soprintendenza, carteggi d'ufficio, atti di
un altro mese. Lo stato del verbale si registra **a parte** — `assente`, `di sola presenza`,
`troncato`, `con sintesi` — perché è un difetto della fonte da contare, non un motivo per non
rispondere alla domanda. Mandata al lettore in corsa e messa nel prompt degli ultimi tredici.

**La conseguenza per il rapporto.** I lotti sono stati letti con tre formulazioni diverse di questo
campo, e **il campo dichiarato dai lettori non è quindi una serie omogenea**: va pubblicato lotto
per lotto, con la formulazione usata accanto. La misura che resta confrontabile su tutto è quella
meccanica — quante candidate dal parlato non hanno alcun gemello per data e luogo in tutto il corpus
— ed è quella che il rapporto darà come numero principale.

**Intanto la fonte conferma se stessa.** Per il Municipio I, **12 dei 23 verbali di commissione di
giugno sono «di sola presenza» o senza alcun contenuto verbalizzato**, e di Commissione Trasparenza
**non esiste alcun verbale in tutto il mese**, pur essendoci due sedute registrate. Per una seduta
esistono **due verbali identici e vuoti**. E circa **70 minuti di seduta non sono stati registrati**
in quattro casi, sempre dove si approvano verbali o si guarda una struttura.

**Un parere votato da quattro consiglieri su otto**, con il presidente che dichiara a verbale
«verificherò per mio scrupolo personale se quattro vanno bene»; un commissario che deve dire «esisto
anch'io» perché il conto dei presenti sbaglia due volte; una delibera votata cinque a due mentre un
consigliere dice «non credo che si possa votare una delibera così sostanziosa e tecnica in un'ora di
commissione», con il termine che scade il giorno dopo. E il consenso alla registrazione raccolto a
voce, perché i moduli non erano arrivati.

## 52. Controllo C3: quattro rilievi bloccanti, e il numero principale diventa un intervallo (16 settembre, 08:50)

Mandato il controllo Codex C3 sulla specifica delle registrazioni, chiedendo esplicitamente di
cercare «dove questa specifica produce numeri che non reggono». Verdetto in
`reviews/C3_specifica_video.md`: **non pubblicabile come numero unico** la quota di novità del
parlato. Quattro rilievi bloccanti, tutti fondati.

**1. «Compare negli atti» non era definito.** Se in aula si dice che un cantiere è fermo e l'atto
dice che è avviato, il tema è lo stesso e il contenuto opposto: marcarlo `anche negli atti`
significa contare una contraddizione come sovrapposizione. **Corretto nella specifica**: quel caso
è `solo dal parlato`, con la parola `contraddice` nella nota, perché la notizia *è* la
contraddizione.

**2. «Atto di un altro mese» non è incertezza nostra, è un confine del corpus.** Finiva in
`non verificabile` e gonfiava quella casella abbassando la novità. Ora è una categoria a sé,
`fuori perimetro`. E `non verificabile` va sempre qualificato — `esterno`, `generico`,
`fuori perimetro` — perché tre cause diverse in un solo valore non si leggono.

**3. Il `dubbio` non è prova di sovrapposizione.** Lo dicevo io stesso in §46 e poi lo stavo usando
come se lo fosse. Il revisore impone la forma giusta: **un intervallo, non un punto**, e solo
parlato-contro-scritto, non «tutto il corpus» (due sedute che dicono la stessa cosa non c'entrano
con la domanda). Scritto `novita_meccanica.py`, che classifica ogni candidata dal parlato in
**S** (nessun gemello scritto), **U** (solo dubbi), **D** (almeno un duplicato):

| | |
|---|---|
| candidate dal parlato confrontate | 310 |
| S — nessun gemello fra le righe scritte | **202** |
| U — solo dubbi | 104 |
| D — almeno un duplicato | 4 |
| **quota di novità** | **[65,2% , 98,7%]** |

L'intervallo è largo perché i dubbi sono un terzo del totale, e questa larghezza **è il risultato**:
dire «il 68%» sarebbe stato finto rigore. Il 65,2% è la parte che non ha alcun riscontro scritto; il
resto è quanto al massimo potrebbe sovrapporsi.

**4. Che cosa misura davvero questo numero.** La soglia di notiziabilità esclude per costruzione i
regolamenti senza luogo, il numero legale mancato, l'organizzazione interna degli organi — e più
lettori hanno segnalato che il fatto più rilevante della seduta finiva fuori. Il revisore: se il
titolo è «quanto aggiunge il parlato» è un difetto; se è dichiaratamente territoriale è una scelta.
**Ho scelto di dichiararla invece di cambiare la soglia a metà studio**: la colonna misura la
novità *territoriale*, la parte politico-istituzionale sta nella relazione fra i difetti visibili
solo ascoltando. Cambiare la soglia ora avrebbe prodotto una quarta definizione e reso i lotti
ancora meno confrontabili; l'informazione non si perde, perché quei casi stanno nei log e nel
massimo della forbice di ogni lotto.

**Congelato il materiale di riscontro** in `report2/snapshot/` (rilievo 6.2): la novità non deve
dipendere dal giorno in cui un lotto è stato letto.

**Resta da fare, e lo scrivo perché non si perda**: la ricodifica ex post del campo dichiarato sui
JSON già prodotti, sullo snapshot congelato — recupera la coerenza dell'etichetta, non la
completezza dell'estrazione, e questa differenza va dichiarata. Da dichiarare anche: che il KPI è
«atti + pipeline del Report 1» e non solo atti; che l'unità di conteggio è la candidata e non il
fatto, quindi due lettori possono spezzare lo stesso fatto in modo diverso; e che un toponimo
sbagliato dall'ASR produce un falso `solo dal parlato`, per cui le righe con
`toponimo_da_verificare = sì` vanno controllate a parte.

## 53. Corpus YouTube chiuso: 97 sedute, e la regola per cui passa solo chi vince (16 settembre, 09:15)

Rientrato V4_085–V4_097, l'ultimo lotto YouTube: 13 sedute, 17 ore e 34 minuti, 100.256 parole, 59
candidate. **Il corpus YouTube è completo: 97 registrazioni, 469 candidate dal parlato.** Database:
3.065 documenti, 2.240 candidate. Quota di novità meccanica: **[61,4% , 98,9%]**.

**Il risultato strutturale, ora con i nomi.** Nell'Assemblea Capitolina di quel lotto le mozioni
**approvate** diventano atti e stanno tutte nel corpus — Stardust Village, bus notturno per Ostia,
poli civici, servitù Terna, due debiti fuori bilancio. Le due mozioni **respinte** — piazza Addis
Abeba e Tor Tre Teste — **non lasciano alcun atto**, e la registrazione è l'unica traccia che siano
mai state discusse e votate. È il §47 confermato su casi nominati: *negli atti passa solo chi
vince*. Chi ricostruisse il mese dai soli atti vedrebbe un consiglio che approva e mai uno che
respinge.

**Il lettore ha fatto meglio di quello che gli avevo chiesto**, e l'ho adottato per i lotti RomaTV:
invece di fermarsi all'oggetto sintetico degli atti è andato a leggere **il testo integrale OCR** in
`A2_text/`, perché «un riassunto non regge la domanda *sta scritto da qualche parte?*». Ha ragione,
e il riscontro dei lotti precedenti è più debole per questo.

**Un effetto collaterale della correzione di ieri, misurato.** Avere ristretto `non verificabile`
ai soli documenti fuori corpus sposta **otto fatti** fuori dal conteggio della novità: solleciti
all'Agenzia del Demanio, 135 offerte e i criteri di un bando, pareri di soprintendenza annunciati,
una risposta scritta della polizia locale, un trasferimento fondato su una determina di novembre.
Nessuno di questi compare negli atti di giugno. Quindi **chi legge il solo numero dei `solo dal
parlato` sottostima quanto la registrazione aggiunge** — l'opposto del rischio che temevo, e va
dichiarato accanto al numero.

**La seduta che non riprende.** Nell'Assemblea: sette minuti di nulla in apertura, prova tecnica
del sistema di voto, tre appelli (10, 13, 25 presenti), aula aperta dopo un'ora e trentotto, buchi
di 54, 27, 15, 14 e 13 minuti. Dopo la pausa pranzo **la seduta non riprende**: viene tolta, e la
registrazione resta accesa su un'aula vuota per oltre un'ora. Nel lotto ci sono **5 ore e 34 minuti
di silenzio** oltre i dieci secondi; senza quella sola registrazione, 95 minuti.

**E circa un'ora di seduta pubblica non registrata affatto**, misurata confrontando gli orari detti
in aula con la durata dei file: in un caso la registrazione si interrompe tre volte e di una seduta
di 79 minuti restano 51 minuti di file.

**Dodici grafie per «Pratone di via Teulada»**, che è l'oggetto unico di tre registrazioni:
«Platone», «Gatulada», «prodotone», «Agolata», «Peulata». L'inno d'Italia diventa una filastrocca.
E in una commissione un minuto di silenzio non è una pausa: è l'aula che cerca un file su Drive e
**scopre di non avere la licenza per aprirlo**.

**Dove il lettore ha forzato, e lo ha scritto.** Un incendio che rende inagibili più appartamenti di
un complesso nominato: la regola sul parlato personale, letta alla lettera, lo escluderebbe perché
l'aula ha solo espresso solidarietà. Lo ha tenuto dopo aver tolto ogni elemento riferibile a una
persona, e ha dichiarato che con la lettura stretta quella riga uscirebbe.

Avviata la lettura del corpus RomaTV: **248 item** (185 trascritti da noi, 63 dalla piattaforma),
1.150.875 parole, primo lotto in corso.

## 54. La parte di seduta che sta fuori dal record, per regola (16 settembre, 09:30)

Rientrato V4_073–V4_084: 12 sedute, 15 ore e 23 minuti, 84.283 parole, **65 candidate, 45 `solo dal
parlato`**. Il lettore ha ricevuto in corsa la correzione della regola e ha **riallineato cinque
righe** già scritte, dichiarando quali.

**La divisione che avevo chiesto, e che sarà la colonna portante del rapporto.** Delle 45
`solo dal parlato`: **33 vengono da sedute il cui verbale è assente, vuoto o di sola presenza; 12 da
sedute con verbale pieno.** Queste dodici sono le più solide che lo studio abbia prodotto finora: il
verbale c'è, ha una sintesi, elenca i suoi oggetti — e il fatto non c'è lo stesso.

**Tre reperti che riguardano il record pubblico in quanto tale.**

1. **Una parte dell'audizione è fuori dal record per regola.** In una commissione una libraia
   collegata dichiara di essere stata invitata e non ottiene la parola; la presidenza spiega che chi
   non è formalmente convocato parla **solo a registrazione interrotta**, e che quegli interventi
   «per motivi di privacy non vengono inseriti». La seduta si chiude interrompendo la registrazione
   per ascoltarla. Non è un guasto tecnico: è una procedura, e produce un buco sistematico.
2. **Il verbale si scrive in diretta, decidendo a voce che cosa lasciarci.** In un'altra commissione
   due interventi vengono saltati esplicitamente e un capoverso rinegoziato per due minuti. Alla
   domanda se gli assessori correggano mai i verbali che ricevono: **«no, non lo fanno mai».**
3. **I buchi della trascrizione cadono sulle votazioni.** In una seduta i due tratti muti maggiori —
   49 e 24 secondi — coincidono con le votazioni elettroniche. Il momento in cui si vota è quello
   che la trascrizione non copre.

**Il censimento sbaglia in modo sistematico, non casuale.** Una convocazione del Municipio IX del 24
giugno è attribuita a **due sedute sbagliate** e tolta a quella giusta: tre item coinvolti. Si
aggiunge ai 6 abbinamenti a un altro Municipio e agli 8 a un atto fuori giugno già misurati in §50.

**Un dato che l'atto contraddice.** In aula si legge un verbale che stima il Ponte dei Congressi
«circa 300 milioni»; l'atto della stessa seduta parla di un appalto da 211 milioni. Il lettore ha
lasciato la cifra detta e segnalato lo scarto — che è la regola giusta, e che secondo la definizione
corretta rende quella riga `solo dal parlato`, perché la notizia è la discordanza.

**Una registrazione che non è una registrazione.** Cinque ore e quarantasei, di cui **quattro ore e
sei minuti di silenzio**, e i primi tredici minuti senza alcun sottotitolo; la seduta diventa valida
solo al **quarto appello, dopo due ore e un quarto** (10, 11, 18 e infine 33 presenti su 48). Le 28
parole al minuto che il manifest lascia calcolare sono un artefatto, e il lettore lo ha scritto nel
file invece di lasciarlo dedurre.

**E la trascrizione, ancora.** Nove grafie per il toponimo che è l'oggetto della seduta; quattro per
la libreria che è il caso centrale della discussione, nessuna corretta; importi che saltano di tre
ordini di grandezza («€3.280.000 000», «€200.000 000 a box»); un articolo di legge che da «35 comma
2» diventa «35,1».

Avviato il secondo lotto RomaTV. Corpus parlato: 97 sedute YouTube lette, 248 RomaTV in coda.

## 55. «La videoregistrazione sostituisce la trascrizione degli interventi» (16 settembre, 09:45)

Primo lotto RomaTV rientrato, V3_001–V3_012: 12 sedute, 9 ore e 17 minuti, 52.298 parole, **30
candidate di cui 16 `solo dal parlato`** (13 da sedute con verbale assente o di sola presenza, 3 da
sedute con verbale pieno). Tutte e dodici sono trascrizioni a pagamento, quindi il confronto fra le
due origini su questo lotto è degenere e va rifatto sul primo lotto con item della piattaforma.

**Due verbali portano scritta la formula che chiude il cerchio dello studio: «la videoregistrazione
sostituisce la trascrizione degli interventi».** Non è un'omissione, è una norma. L'ente dichiara
per iscritto che il record di ciò che si è detto **è il video**, non l'atto. Tutto quello che questo
rapporto ha misurato — verbali di sola presenza, istruttorie che vivono solo nelle registrazioni,
mozioni respinte senza traccia — discende da lì, ed è la frase che il Report 2 deve citare per
prima.

**Un difetto del mio programma, trovato da un lettore.** `collega_video_atti.py` dava zero verbali
compatibili per le sedute delle Commissioni Capitoline. Il motivo: cercavo il Municipio nel nome del
territorio, e gli organi centrali non ne hanno — i loro atti stanno nel corpus sotto il prefisso
`CEN_` con `municipio = non indicato`. Il lettore ha trovato a mano tre verbali (`CEN_CPV_*`) che il
mio programma dichiarava inesistenti. Corretto: le registrazioni con **un solo verbale compatibile**
passano da 63 a **76**, quelle senza alcun verbale scendono da 73 a 53. Chi legge i prossimi lotti
ha l'avvertenza nel prompt.

**Una segnalazione che ho verificato e ridimensionato.** Il lettore riferisce che la trascrizione a
pagamento «ripete blocchi interi ai bordi dei pezzi», citando ~200 parole duplicate in una
registrazione. Ho cercato: su **1.540 giunzioni fra pezzi**, zero ripetizioni identiche di almeno 8
parole; con un confronto tollerante, **42 giunzioni (2,7%) con un blocco simile, la più lunga di 25
parole**. Nella registrazione citata non c'è nessuna ripetizione. Il fenomeno esiste ma è un
ventesimo di quanto riferito: lo dichiaro come 2,7% e avverto i lettori, invece di propagare il
numero grande.

**Il difetto opposto delle due origini, questo sì confermato.** Dove non si parla, la trascrizione a
pagamento lascia il pezzo **letteralmente vuoto**; la piattaforma YouTube **inventa parole** («Prova
Bra», «Och», «Ja»). Il primo errore si vede, il secondo no: una trascrizione che riempie i silenzi è
più pericolosa di una che li lascia.

**E le sedute.** Un'audizione chiesta a ottobre e ottenuta a giugno, con l'ospite rintracciato
tramite un social; venti minuti bruciati perché il link è andato alla commissione sbagliata e senza
modulo privacy la seduta non è pubblicabile; una presidenza che non riesce ad aprire la posta dove
sta il regolamento da leggere; un atto che scopre in aula di non avere il Sindaco fra i destinatari;
verbali del novembre 2024 e del luglio 2025 approvati a giugno 2026.

**Una cifra che non è colpa della trascrizione.** In una seduta si dicono «566» e poi «556»
domande — e **il verbale riporta entrambe le cifre**. Non è l'ASR che sbaglia: è la fonte che non
sa quante siano.

## 56. Correzione a §55: avevo misurato la cosa sbagliata (16 settembre, 10:00)

In §55 ho scritto che la ripetizione di blocchi nella trascrizione a pagamento era «un ventesimo di
quanto riferito». **Era sbagliato, e il lettore aveva ragione.** Avevo cercato le ripetizioni
**solo alle giunzioni fra due pezzi consecutivi**: una domanda più stretta di quella giusta. Il
lettore del lotto successivo l'ha misurata come andava misurata — blocchi ripetuti ovunque nel
testo — e i suoi numeri (18,9% e 17,2% su due registrazioni) sono confermati.

Misura corretta, su tutte le 211 trascrizioni a pagamento, contando le parole che stanno dentro
blocchi di dodici parole presenti più di una volta:

| | trascrizioni della piattaforma | trascrizioni a pagamento |
|---|---|---|
| mediana della quota ripetuta | 0,0% | 0,5% |
| registrazioni sopra il 10% | **0** | **39** |
| massimo | 1,7% | **86,6%** |

**È un difetto del modello che abbiamo pagato, non del materiale.** Sulle stesse sedute, con lo
stesso audio istituzionale, la piattaforma non supera l'1,7% e il nostro modello arriva a
riscrivere quattro volte lo stesso passaggio: in una registrazione da 9.902 parole il 67,9% del
testo sta dentro blocchi duplicati. Succede sulle registrazioni lunghe e silenziose, che è
esattamente il profilo delle sedute municipali.

Conseguenze, tutte da dichiarare nel rapporto:
1. **Il conteggio delle parole è gonfiato** su quelle registrazioni, e con esso le parole al minuto
   e qualunque statistica di volume.
2. Un lettore che trova la stessa frase tre volte può prenderla per insistenza dell'oratore.
3. Chi ripetesse questo studio con lo stesso modello troverebbe lo stesso difetto: va scritto.

Ho aggiunto `quota_ripetuta` all'indice e al manifest RomaTV, riga per riga, e l'avvertenza nel
prompt dei lettori. Gli identificativi `V3_*` già assegnati **non sono cambiati** — i lotti letti li
citano — e i 26 item nuovi hanno preso i numeri liberi: il corpus RomaTV è ora a **274 item**.

**Un limite che il lettore ha isolato e che vale per tutte le misure sui silenzi.** Con il marcatore
ogni 300 secondi, qualunque silenzio più corto di cinque minuti è invisibile: scrivere «zero tratti
muti» su una trascrizione a pagamento è **un artefatto della grana, non una misura**. Le due origini
non sono confrontabili su questo, e i numeri sui silenzi valgono solo per le registrazioni della
piattaforma.

## 57. Sette verbali trovati a orecchio, e un atto che sbaglia i propri conti (16 settembre, 10:00)

Il lotto V3_013–V3_024 ha prodotto 52 candidate, **34 `solo dal parlato`, di cui 13 da sedute con
verbale pieno**. E ha fatto due cose che valgono più delle percentuali.

**Ha trovato sette verbali che il censimento non assegna**, identificandoli **per ora di apertura,
ordine del giorno ed esiti di voto** invece che per metadati. È il metodo che funziona quando
l'abbinamento automatico manca, e l'ho messo nel prompt dei lotti successivi. Ha inoltre verificato
che nel corpus **non esiste alcun verbale di Consiglio del Municipio V** — zero su 1.983 — per cui
quelle sedute hanno il verbale davvero assente, non solo non abbinato.

**E ha trovato un difetto dentro un atto, non nella registrazione.** Una risoluzione del Municipio V
proclama «Favorevoli: 16» ed elenca **22 nomi**, con 22 presenti, 22 votanti, zero contrari e zero
astenuti. In aula si dice «all'unanimità». **Ha ragione l'aula**: è l'atto a sbagliare il proprio
conteggio. Finora avevamo trovato registrazioni che aggiungono agli atti; questa è una
registrazione che **corregge** un atto.

**La votazione che non lascia traccia.** In una seduta, fra due marcatori si passa da «possiamo
votare, posso procedere?» agli interventi che la danno per avvenuta: che il voto ci sia stato, e che
un sostituto si sia astenuto, **si deduce solo dalle repliche**. Nessun verbale nel corpus.

**E un dettaglio che dice molto sull'epoca.** In una commissione si discute a lungo di un
partecipante non identificato collegato alla seduta: risulta essere **un servizio automatico di
trascrizione**, attivato da qualcuno e rimasto lì.

## 58. Il toponimo storpiato che fabbrica novità (16 settembre, 10:10)

Eseguito il rilievo 6.3 del controllo C3: un toponimo sbagliato dal riconoscimento automatico non
trova il suo gemello, e la candidata risulta nuova **per un errore di trascrizione invece che per un
fatto**. Con 126 registrazioni lette e 573 candidate dal parlato:

| | toponimo fermo | toponimo dichiarato incerto |
|---|---|---|
| nessun gemello scritto (**S**) | 217 | **125** |
| solo dubbi (U) | 150 | 75 |
| almeno un duplicato (D) | 2 | 4 |

**Il 36,5% delle candidate «certamente nuove» poggia su un toponimo che il lettore stesso ha
marcato incerto.** Scartandole, la novità certa scende **dal 59,7% al 37,9%**.

Il rapporto avrà quindi una scala a tre gradini, non un numero:

- **37,9%** — nuove con un toponimo fermo: il pavimento, quello che regge a qualunque obiezione;
- **59,7%** — nuove, cioè senza alcun gemello fra le righe scritte, toponimi incerti compresi;
- fino a **oltre il 98%** se si contano come nuove anche tutte quelle che hanno solo un `dubbio`.

Tre numeri, tre domande diverse, tutti e tre misurati. È la forma che il controllo C3 chiedeva, e a
questo punto la larghezza non è più un'incertezza da nascondere: **è il risultato**, perché dice che
la risposta dipende da quanto si è disposti a fidarsi di una trascrizione automatica.

Nota di metodo: il flag `toponimo_da_verificare` sta nei JSON dei lettori, non nella tabella, e il
programma lo rilegge da lì incrociando item e titolo. È fragile — se un titolo cambia, l'incrocio
salta — e lo dichiaro invece di farlo passare per esatto.

Ledger: trascrizione a **219 registrazioni, 154,9 ore, 22,49 €**; disponibili **54,93 €**.

## 59. Un minuto di registrazione su mezz'ora di seduta, e altri due errori miei (16 settembre, 10:30)

Rientrato V3_037–V3_048: 12 sedute, 13,1 ore, **54 candidate, 35 `solo dal parlato`**, di cui
**7 da sedute con verbale pieno**. Forbice 20–66.

**Due errori miei, trovati dal lettore.** Il terzo emendamento si contraddiceva: il punto 2 diceva
che un fatto in un atto di un altro mese è `fuori perimetro`, il punto 3 elencava `fuori perimetro`
fra le qualificazioni di `non verificabile`. Non è un quarto valore, è una qualificazione, e l'avevo
scritto in modo da far credere il contrario. Secondo errore: gli emendamenti rendono obbligatorio un
campo `nota` che **lo schema non prevedeva**; il lettore l'ha aggiunto da sé su otto candidate.
Entrambi corretti nel quarto emendamento. È la seconda volta che un lettore trova una
contraddizione nelle mie regole applicandole invece di aggirarle, ed è il motivo per cui la
specifica chiede di dichiarare le regole dubbie invece di correggerle.

**Un'insidia che avrei potuto propagare.** Nei nomi degli atti centrali (`CEN_...`) il segmento che
sembra un Municipio **è un segnaposto**: `CEN_CPV_X_...` può riguardare il Municipio XI. Chi
deducesse il territorio dal nome dell'atto sbaglierebbe sistematicamente. Ora è scritto nella
specifica.

**Il caso che batte tutti i precedenti.** Una seduta ha **un solo minuto di registrazione**, dalle
09:08 alle 09:09: l'audio si interrompe alla sospensione e tutta la parte deliberativa — otto
verbali arretrati e un progetto di depavimentazione dei cortili scolastici — **non esiste
nell'audio**, almeno una trentina di minuti. Finora avevamo verbali vuoti con la registrazione a
supplire; qui mancano tutti e due.

**La duplicazione del modello, vista da vicino.** In una registrazione una frase è ripetuta **circa
cento volte di fila** e il 54% dei token sta dentro blocchi duplicati: il conteggio delle parole e
le 55 parole al minuto **non misurano più niente**. Ho messo nella specifica la regola: sopra il 10%
di `quota_ripetuta` il dato di volume non si riporta, si dichiara.

**La misura dei silenzi, fatta bene una volta.** Sull'unica registrazione a grana 10 secondi del
lotto il lettore ha potuto misurare davvero: **76,8 minuti di silenzio su 288**, in quattro tratti
di 29, 30, 8 e 9 minuti — e **tutti e quattro coincidono al minuto con le sospensioni verbalizzate**.
La registrazione non è tagliata: il silenzio è la seduta sospesa. È il contrario di quello che si
potrebbe concludere dai vuoti delle trascrizioni a pagamento, dove non si sa.

**E due sedute che gli atti raccontano diversamente da come sono andate.** Una fallisce per ragioni
acustiche — richieste di ripetere, un consigliere che esce perché non sente, la presidenza che
rinuncia e chiude — e **il verbale descrive un sopralluogo regolare, senza farne parola**. In
un'altra il parere sulla delibera è messo ai voti **prima** che l'assessore risponda; una consigliera
obietta che «le risposte sono funzionali al parere» e il presidente procede lo stesso. Nessun atto
registra la sequenza.

## 60. La novità si paga in certezza, e io ho sbagliato la terza misura di fila (16 settembre, 10:45)

Rientrato V3_025–V3_036: 12 sedute, 7 ore e 17 minuti, **36 candidate, 21 `solo dal parlato`** di
cui **17 da sedute con verbale pieno** (13 al netto di una duplicazione). Corpus parlato letto:
**641 candidate**.

**Un'osservazione del lettore che ho verificato su tutto il corpus, ed è un risultato.** Nel suo
lotto *nessuna* candidata `solo dal parlato` arrivava a qualità `alta`, mentre tutte le `alta` erano
`anche negli atti`. La sua spiegazione: è l'atto che permette di accertare che un fatto sia
compiuto, datato e localizzato. Misurato su tutte e 641:

| | qualità alta | media | bassa |
|---|---|---|---|
| anche negli atti (166) | **92 — 55,4%** | 72 | 2 |
| solo dal parlato (390) | **99 — 25,4%** | 265 | 26 |
| non verificabile (85) | 15 | 59 | 11 |

Non è zero come nel suo lotto, ma il rapporto è netto: **una notizia nuova ha metà probabilità di
essere di qualità alta rispetto a una che gli atti confermano**. Nel parlato la novità si paga in
certezza, e il rapporto deve dirlo accanto ai tre numeri della novità: la parte più nuova è anche la
meno verificabile.

**La mia terza misura sbagliata di fila.** Il lettore ha trovato che due suoi item sono **la stessa
seduta pubblicata due volte**. Ho cercato la cosa su tutto il corpus e ho trovato **zero** coppie.
Sbagliato: per andare più veloce avevo campionato i blocchi ogni tre parole, e il campionamento
faceva mancare proprio il caso noto. Rifatta senza scorciatoia, la coppia condivide il **52%** dei
blocchi da dodici parole, e sul corpus ce n'è **una seconda** (V3_259 / V3_261, Municipio V, 19
giugno, 57%). **Quattro item su 274 sono due sedute pubblicate due volte.**

Tre volte in una mattina una mia verifica rapida ha contraddetto un lettore e tre volte aveva
ragione il lettore: la ripetizione dei blocchi, il conteggio giusto, e ora questa. La regola che
me ne viene: **quando una mia misura smentisce chi ha letto il materiale, il primo sospettato è la
mia misura.**

**Altri due reperti del lotto.** Una registrazione a pagamento ripete lo stesso blocco di 150 parole
**undici volte**: il 47% del file, e le «157 parole al minuto» che ne risultano sono un numero
falso — il ritmo reale è 95. E una volta è **l'atto a sbagliare e la registrazione ad aver ragione**:
l'aula cita correttamente una deliberazione «n. 35 del 16 marzo 2010», l'OCR del verbale scrive
«n. 3».

**Una seduta che esiste solo perché è stata ripresa.** Un Consiglio municipale che non riesce ad
aprirsi: appello, scrutatori, tre minuti per votare la procedibilità, due gruppi che dichiarano di
non partecipare, rinvio al giorno dopo. **Il verbale di quella seduta non esiste nel corpus**: senza
la registrazione, quella seduta non è mai avvenuta.

**E la parte tecnica tenuta fuori, con il motivo dichiarato in aula.** In un'altra seduta le due
sospensioni «a microfoni spenti senza registrazione» sono esattamente i minuti in cui intervengono
polizia locale e azienda sanitaria, gli unici due soggetti tecnici presenti; il motivo detto è che
gli ospiti esterni non avevano firmato il consenso. Si aggiunge al caso di §54: **la parte più
informativa è quella che per procedura non viene registrata.**

## 61. Perché la novità si paga in certezza: il meccanismo (16 settembre, 11:10)

Rientrato V3_061–V3_072: 12 registrazioni, 6 ore e 44 minuti, **62 candidate, 38 `solo dal parlato`
di cui 27 da sedute con verbale pieno**. Ma la cosa che conta è un'altra.

**Avevo chiesto a questo lettore di verificare l'osservazione sul rapporto fra novità e qualità, e
lui ha trovato il meccanismo.** Nel suo lotto la forbice è ancora più larga della media: 5,3% di
qualità alta fra le `solo dal parlato` contro il 45% fra le `anche negli atti`. Le **uniche due**
`solo dal parlato` arrivate ad alta sono casi in cui **chi parla sta leggendo ad alta voce un
documento che esiste ma è fuori dal corpus di giugno**: un verbale di maggio, i tabulati di un
ufficio.

Da cui la sua conclusione, che ho messo nel rapporto al posto della mia: **non è l'atto a conferire
la qualità alta, è l'esistenza di un documento.** Quando il parlato porta un documento dentro
l'aula può arrivare ad alta; quando porta un'impressione, un ricordo o una stima, no. E il
corollario ribalta la lettura del numero: **quel 25% non misura la debolezza del parlato, misura
quanto raramente il parlato è documentale.**

**Un terzo meccanismo che produce buchi nel record.** Finora avevamo la prassi (chi non è convocato
parla a registrazione spenta) e il consenso mancante (gli ospiti esterni senza modulo). Qui c'è la
norma: la registrazione è interrotta su richiesta **in applicazione dell'articolo 32 comma 3 del
regolamento**, e l'intervento del comitato e il voto finale non esistono in video. Che l'ordine del
giorno sia passato con 18 voti all'unanimità si sa solo dall'atto — per una volta nel verso opposto.

**Un atto che dispone il contrario di quanto deciso.** L'atto depositato conteneva nel dispositivo
**la soluzione che la commissione aveva scartato**; l'emendamento è stato scritto in aula, senza
nemmeno le copie. L'atto pubblicato dice soltanto «così come emendata»: dell'errore resta traccia
solo nella registrazione. Aggiunto al rapporto.

**E altre due sedute che nessun atto racconta.** Una commissione convocata **in urgenza alle 19:22
per le 8:30 del mattino dopo**, con i curricula inviati la stessa sera e un consigliere che dichiara
di aver saputo della seduta dal telefono; il verbale non esiste. E un Consiglio intero **senza
nessun assessore in aula**, con la contestazione che attraversa maggioranza e opposizione e resta
senza risposta.

**Una precisazione sul mio conteggio dei duplicati.** In §60 avevo detto «quattro item su 274 sono
due sedute pubblicate due volte». Il lettore ha trovato un'altra cosa: **tre item che sono tre
spezzoni consecutivi della stessa seduta**, e due che sono Parte 1 e Parte 2. La mia misura cerca
registrazioni *ripubblicate*, che condividono il testo; **gli spezzoni non condividono niente**, e
il mio metodo non li vede per costruzione. Sono due difetti diversi del corpus e vanno contati
separatamente.

**Un difetto nuovo della trascrizione**: in due registrazioni compaiono parole **sostituite da
asterischi** dalla piattaforma. Una censura automatica che rende illeggibili dei passaggi, e che va
messa accanto alle invenzioni nei silenzi e ai blocchi duplicati.

## 62. Il link dentro il verbale: la mia misura era sbagliata due volte (2026-09-16 08:15Z)

Un lettore aveva detto: «i verbali del Municipio XI chiudono con il link di streaming, e quel link
contiene l'identificativo del video … se altri Municipi fanno lo stesso il censimento si può rifare
in automatico». Avevo cercato e riferito: 17 atti, **zero** risolti al nostro corpus, 3
identificativi rovinati dall'OCR. Conclusione che avevo tratto: prassi reale ma inutilizzabile.

Entrambi i numeri erano miei difetti, non della fonte.

1. Cercavo la stringa `vod/<guid>`. Cercando l'identificativo dovunque compaia, gli atti sono **40**
   e i Municipi **quattro**, non uno.
2. Risolvevo i guid contro la colonna `video_id` del manifest. Per le commissioni quel campo è
   `comm_` + **i primi 8 esadecimali** del guid, non il guid: nessuna stringa poteva mai
   coincidere. Lo zero non misurava la fonte, misurava la mia chiave.

Misurato bene (`report2/link_verbali_video.py`), il quadro è un altro. Le forme sono tre e valgono
cose diverse:

| forma | dove | atti | guid distinti | che cosa identifica |
|---|---|---|---|---|
| `watch/vod/<guid>` | verbali XI (15) e X (2) | 17 | 17 | **la singola seduta** |
| `search/catalog/<guid>` | verbali XV | 21 | **1** | il catalogo del Municipio |
| `watch/live/<guid>` | convocazioni IX | 2 | 1 | il canale della diretta |

Solo la prima abbina un atto a una registrazione. La seconda dice che la registrazione esiste, non
quale: lo stesso identificativo in tutti e 21 i verbali. La terza sta nella convocazione e identifica
l'organo, non la seduta. Dei due link di diretta del IX, **uno è corrotto dall'OCR di un carattere**
(`…a43aa6e7` contro `…a43aabe7`): il difetto che avevo attribuito a tre identificativi esiste, su uno.

Dei 17 identificativi di seduta, **7 risolvono a un item del nostro corpus** e 9 altri a
registrazioni che esistono sul portale ma che non abbiamo scaricato; uno solo non risolve a niente.

### Il vero valore: 7 abbinamenti dichiarati dalla fonte

Quei 7 non sono un matcher, sono un **banco di prova**: sono gli unici casi in cui l'abbinamento
atto-registrazione lo dichiara la fonte e non lo ricostruiamo noi. Su di essi:

- il **censimento della piattaforma ne dichiara 0 su 7**. Tutti e sette hanno `verbale_match` vuoto;
- il nostro collegamento per Municipio+data contiene il verbale vero **7 volte su 7**, e in **4 casi
  su 7** il compatibile era già unico (negli altri tre erano 2, 2 e 3).

È poco (n=7, un solo Municipio) e va scritto come tale. Ma è la sola verifica esterna che abbiamo del
collegamento, e dice due cose coerenti con tutto il resto: il censimento della fonte è il pezzo
debole, e l'euristica Municipio+data non ha mai perso il verbale giusto dove si poteva controllare.

### Che cosa non dice

Che il censimento si possa rifare in automatico: 17 atti su 1.983, due Municipi su quindici. È una
buona prassi da nominare — un verbale che cita la registrazione a cui si riferisce —, non un
meccanismo su cui una pipeline possa contare.

Terza volta in questa sessione che una mia misura smentisce chi ha letto il materiale e la mia misura
è quella sbagliata (§56, §60, questa). La regola di §60 ha retto: ho ricontrollato prima di
pubblicare il risultato negativo. Ma l'avevo già scritto una volta, come risultato.

## 63. Quanto costa cambiare la regola sotto i lettori (2026-09-16 08:19Z)

Il C3 dice (§3.3) che i lotti letti con definizioni diverse non sono confrontabili su
`novita_rispetto_agli_atti`, e chiede la ricodifica ex-post. Prima di ricodificare ho misurato
**quanto** sono incomparabili, con `report2/varianza_lettori.py`.

Il controllo è questo: il campo lo scrive un lettore, la classificazione S/U/D la calcola il
confronto. La misura meccanica non sa niente del lettore, quindi porta la sola eterogeneità del
materiale. Il rapporto fra le due escursioni dice chi disperde.

| gruppo | lotti | escursione del lettore | escursione meccanica | rapporto |
|---|---|---|---|---|
| V4 YouTube, letti sotto tre definizioni successive | 9 | **71 punti** | 49 punti | **1,46** |
| V3 RomaTV, letti a specifica ferma | 6 | **12 punti** | 23 punti | **0,52** |

*Aggiornamento del 16/09 09:16Z, con due lotti in più (otto invece di sei): l'escursione del lettore
sale a **22 punti**, quella meccanica a 30, il rapporto a **0,74**. La direzione regge — a regola
ferma il lettore disperde meno del materiale — ma il **0,52 era un numero da sei lotti**, e con due
in più si muove di venti punti percentuali. Da citare come 0,74 e da rifare alla consegna: su
numeri così piccoli l'escursione massima è una statistica fragile.*

Sopra 1 il lettore aggiunge dispersione al materiale; sotto 1 ne toglie. A regola ferma i lettori
concordano più di quanto vari il materiale (12 punti, vicino ai ~9 punti misurati fra due lettori
sullo stesso tipo di atto); a regola che cambia sotto di loro la dispersione **supera** quella del
materiale. La correlazione fra giudizio umano e misura meccanica sui 15 lotti è +0,22: nulla.

Il caso estremo è V4_061: `solo dal parlato` al **16,7%** e `non verificabile` al **68,8%**, mentre
la misura meccanica sullo stesso lotto dà S al 58,3%. Quel lettore non stava leggendo peggio, stava
applicando una definizione diversa — e infatti è uno dei lotti letti prima dell'emendamento che ha
tolto dal `non verificabile` il fuori-perimetro.

Da tenere fermo: **non è una misura della variabilità fra LLM**. È la misura di che cosa costa
cambiare il contratto mentre il lavoro è in corso, ed è un costo che ho creato io emendando la
specifica tre volte. La regola «non si modifica mentre un lotto è in lettura» era scritta nella
specifica dalla prima riga; l'ho rispettata sul singolo lotto e violata sulla serie.

*(Timestamp corretto: avevo scritto 08:47Z a occhio invece di leggerlo dall'orologio, che diceva
08:19Z. Stessa svista già annotata in questa sessione; l'orologio si legge, non si stima.)*

## 64. Il corpus è ancora in crescita: il manifest non è la verità (2026-09-16 08:22Z)

Misurando i link (§62) mi sono accorto che `rtv/txt` contiene **293** trascrizioni e
`manifest_video_rtv.csv` ne elenca **274**: diciannove registrazioni sono trascritte ma non nel
manifest, perché il driver ASR sta ancora lavorando (260 item su 275 audio preparati, $ 29,13).

Conseguenze da tenere presenti e non dimenticare alla consegna:

1. Il manifest va **rigenerato** quando il driver finisce, conservando gli id già assegnati; i
   lettori leggono dal manifest, quindi finché non lo rigenero quei diciannove item non li legge
   nessuno.
2. I conteggi che passano dal manifest — «274 item», i 7 link risolti di §62, la stratificazione per
   origine della trascrizione — sono **fotografie di uno stato intermedio** e vanno rifatti, non
   citati come definitivi. Nessuno dei dieci identificativi ancora non risolti di §62 è fra i
   trascritti fuori manifest, quindi quel 7 su 17 per ora non cambia; ma va ricontrollato dopo.
3. Lo stesso vale per `build_db.py`: non lo rieseguo mentre due lettori scrivono dentro
   `out_video/`, per non assegnare id a candidate di file scritti a metà.

Correzione anche al registro (§2): la trascrizione era annotata a 22,49 € su 154,9 ore; è a 26,80 €
su 184,7 ore e non è finita. La stima era vecchia di ore, non sbagliata all'origine — ma lasciata
ferma in tabella diventa un numero falso.

## 65. Due registrazioni perse in silenzio dal driver ASR (2026-09-16 08:41Z)

Controllo di routine della VM (driver attivo, 261 item, $ 29,13, disco 26 G liberi, quattro
scaricamenti in parallelo come da limite). Nel log due sole righe `ERRORE`. Guardate da vicino, non
erano due intoppi: erano **due registrazioni che il driver non avrebbe mai ripreso**.

**Il difetto.** Il driver cancellava i segmenti scaricati *prima* di chiamare l'API:

```
shutil.rmtree(segdir, ...)      # <- prima
res = trascrivi(mono, ...)      # <- poi
```

Se la chiamata falliva, i segmenti non c'erano più; e la coda di lavoro si costruisce da
`pronti()`, che pretende la playlist locale dentro quei segmenti. Item scomparso, senza che nulla
lo dicesse: nel log resta una riga `ERRORE` che sembra un intoppo passeggero.

È successo a **2bff8cd6** (timeout di lettura dopo 600 s). L'audio mono è ancora lì, 10,8 MB: la
trascrizione si recupera senza riscaricare niente.

**Correzione applicata** (`video/rtv_asr_driver.py`, copia di sicurezza `.prima_del_fix_perdita`):
i segmenti si cancellano solo a trascrizione riuscita; la coda di lavoro parte anche dagli mp3 mono
senza trascrizione; `remux` si salta se il mono esiste già. Il processo in corso ha il vecchio
codice in memoria, quindi la correzione vale dal prossimo avvio — che farò a driver fermo, non
interrompendolo a metà di un item.

**Il secondo caso è un difetto della fonte, non mio.** In **41e7b841** l'ultimo dei 59 segmenti
(`slen_58`) è un **file di zero byte**: il CDN risponde vuoto, e ha continuato a rispondere vuoto a
ogni tentativo. Gli altri 58 sono integri. La registrazione non è irrecuperabile: manca la coda.
Riproverò lo scaricamento del solo segmento quando la pozza dei quattro scaricamenti si svuota —
non ora, perché un quinto processo in parallelo violerebbe il limite. Se il segmento resta vuoto, la
registrazione va tenuta **dichiarando la lacuna**, non scartata.

**Che cosa mi insegna.** Ho guardato quel log tre volte contando le righe `OK` e non ho mai letto le
due righe `ERRORE`. Un conteggio di successi non è un controllo. Poi ho fatto il conto giusto —
**item attesi meno item con trascrizione** — e ha mostrato una cosa che il log non diceva:

| | |
|---|---|
| attesi dalla lista di scaricamento | **318** |
| con trascrizione | 262 |
| scaricamento ancora in corso | 53 |
| in lavorazione adesso | 1 |
| **fermi con l'audio pronto e nessuno che li riprenda** | **2** |

I due fermi sono `2bff8cd6` e **`494cc3af`**. Del secondo nel log **non c'è nessuna riga**: né `OK`
né `ERRORE`. L'mp3 è delle 04:09, l'errore di `41e7b841` delle 04:11; nel mezzo il driver è morto o
è stato riavviato, e quell'item è uscito dalla coda senza lasciare traccia. Quindi le righe `ERRORE`
non sono nemmeno il limite superiore delle perdite: **un item può sparire senza comparire nel log in
nessuna forma**. L'unico conto che tiene è quello per differenza, e va rifatto alla consegna.

## 66. Il numero principale poggia su un insieme di confronto incompleto (2026-09-16 08:47Z)

Partito da tutt'altro — controllare chi produce la colonna `verbale_match` — sono arrivato al
difetto più serio trovato finora, ed è mio.

**Primo: «il censimento» non è della fonte, è nostro.** In §45, §52 e nel rapporto ho scritto che
«il censimento abbina la registrazione al suo atto in modo inaffidabile», mettendolo fra i *difetti
delle fonti*. Quel censimento lo costruisce `video/yt_census_build.py`: abbina per Municipio, data e
sovrapposizione di parole chiave. Le sue sviste sono **nostre**, e attribuirle alla fonte in un
rapporto sarebbe una falsa accusa. Da correggere ovunque compaia.

**Secondo: il meccanismo del link non l'ho scoperto io.** In §62 ho presentato il link dentro il
verbale come un reperto nuovo. Lo stesso programma lo usa già da prima: `LINKMAP`, con il commento
«Municipio I embeds it in every June verbale», e **28 dei 131 item YouTube sono abbinati proprio
così** — più dei 23 abbinati per data e nome. Di nuovo c'è solo che la pratica esiste anche in
RomaTV (XI e X) e che due forme simili (`catalog`, `live`) non servono a questo. §62 va letto con
questa correzione davanti.

**Terzo, e serio: contro che cosa abbiamo misurato la novità.** Scomponendo gli abbinamenti per
origine:

| origine dell'abbinamento | n | punta a un altro Municipio | punta a un atto fuori dai 1.983 |
|---|---|---|---|
| link scritto nel verbale (lo dichiara la fonte) | 28 | **0** | 7 |
| data e nome (lo deduciamo noi) | 23 | 0 | 6 |
| convocazioni, per data e nome (noi) | 102 | **6** | 25 |

Il «18% sbagliato» di §52 mescolava due cose diverse: gli abbinamenti **errati** sono 6, tutti sulle
convocazioni dedotte da noi; gli altri 38 sono *fuori perimetro*, ed è la distinzione che il C3 §1.2
imponeva di non confondere.

Ma il «fuori perimetro» non regge neanche lui. Ho controllato tre di quegli atti: **li abbiamo**, in
`A2_text/`, e due portano una data di giugno. Il motivo è un altro:

- atti che abbiamo scaricato e teniamo in `A2_text/`: **2.668**
- atti dentro `confronto_atti.csv`, cioè l'insieme contro cui è misurata tutta la novità: **1.983**
- differenza mai confrontata: **685**, di cui **275 verbali e convocazioni**

I 1.983 sono gli atti *letti*, non gli atti *che abbiamo*. Un verbale di seduta di giugno
repertoriato a luglio sta fuori per costruzione — ed è esattamente il documento che conterrebbe il
gemello scritto di ciò che si è detto in quella seduta.

**Quanto pesa.** Misura grossolana ma sufficiente a non ignorarla: delle **422** candidate del
parlato classificate S («nessun gemello scritto»), **151 — il 36% — nominano un luogo che compare in
un atto che non abbiamo mai confrontato**. La compresenza di un toponimo non è un gemello (viale
Palmiro Togliatti compare ovunque), quindi 151 è un tetto, non una stima. Ma il limite inferiore
pubblicato, **58,0%, non è difendibile** finché quei 275 atti non sono letti e confrontati.

**Che cosa faccio.** Leggere i 275 verbali e convocazioni mancanti con la specifica degli atti, già
in perimetro e senza costo di rete, e rifare la misura. Se la scelta fosse fra estendere l'insieme
di confronto e leggere altre registrazioni, viene prima l'insieme di confronto: una registrazione in
più aggiunge un aneddoto, un atto mancante sposta il numero su cui poggia tutto il rapporto.

**Come ci sono arrivato.** Non guardando la novità, ma chiedendomi chi scrivesse una colonna. Le tre
correzioni di oggi (§62, §64, questa) nascono tutte dalla stessa domanda — *questo numero da dove
viene?* — e nessuna da un controllo della cosa che stavo misurando.

## 67. V3_073–V3_084: il parlato non è debole, è il residuo (2026-09-16 08:50Z)

Dodici registrazioni dell'11 giugno, 10,75 ore, 75 candidate, zero saltate. Il lettore ha dichiarato
la forbice (54–94, centro 75) e le otto coppie di passaggi simili con esito diverso, come chiesto.

**Un meccanismo migliore di quello che avevo messo nel rapporto.** Avevo scritto che la qualità alta
la dà la documentalità: non è l'atto, è l'esistenza di un documento. Il lettore lo ha verificato sul
proprio lotto e regge **tre casi su cinque**; ma propone una spiegazione che li contiene tutti e
cinque e spiega anche perché il documentale sia l'eccezione.

Le `solo dal parlato` di qualità alta sono il **9,1%** (5 su 55) contro il **73,7%** delle `anche
negli atti`. Guardando le altre cinquanta, sono quasi tutte **fatti negativi o non ancora accaduti**:
annunci senza data, proposte non deliberate, lavori fermi, assenze, risposte mancate. E allora:

> un fatto compiuto, datato e localizzato tende **per costruzione a generare un atto**, e appena lo
> genera esce da `solo dal parlato`.

Non è il parlato a essere debole: è un **effetto di selezione alla fonte**. Ciò che resta solo nel
parlato è il residuo che non è ancora diventato atto. Con una sola eccezione strutturale — **un
documento compiuto che esiste ma sta fuori dal perimetro del corpus**: un verbale di maggio, i
questionari di un ufficio dietetico, un messaggio dell'azienda sanitaria letto ad alta voce.

**E qui il lotto incontra §66 senza saperlo.** La prova più netta è `V3_077 [00:00]`: la stessa
frase, lo stesso lettore, lo stesso documento letto ad alta voce produce due righe con esito
opposto. La risoluzione su viale Palmiro Togliatti è `anche negli atti` perché l'atto dell'8 giugno
è nel corpus; gli stalli di via Antonio Tempesta sono `non verificabile / fuori perimetro` perché il
verbale di maggio non c'è. **Cambia solo il confine del corpus.** È esattamente il difetto che ho
misurato in §66 da tutt'altra parte, e che due misure indipendenti trovino la stessa cosa è il
motivo per cui vale la pena chiuderlo prima della consegna.

Sostituisco nel rapporto il meccanismo della documentalità con questo, che lo include.

**Previsione che il lettore lascia ai prossimi lotti** (e che va verificata, non citata): le
`solo dal parlato` di qualità alta dovrebbero concentrarsi in due nicchie — letture di documenti
extra-giugno e atti compiuti dall'organo in aula (commemorazioni, inaugurazioni, sopralluoghi
appena svolti) — e mancare quasi del tutto dalla discussione politica generale.

**Una contestazione sua che ho verificato, e che è metà giusta.** Dice che `quota_ripetuta` del
manifest sottostima: in V3_080 un intero periodo è ripetuto due volte mentre la quota dichiara
0,008. Misurato: la mia misura **quel blocco lo vede**, marca 68 parole su 8.345, cioè proprio lo
0,8%. Non è una sottostima, è una **quota globale**: dice quanta parte del testo è duplicata, non se
un passaggio lo è. Ma il rilievo resta, in altra forma — la soglia a dodici parole è una scelta, e a
sei parole la stessa registrazione passa da 0,8% a **2,9%**. Va dichiarato: la quota non è una
bandierina sul singolo passaggio, e dipende dalla lunghezza del blocco.

**Difetti nuovi da tenere.** V3_077: lo stesso periodo sull'articolo 16 ripetuto **quattordici
volte** (`quota_ripetuta` 0,212, parole del manifest inutilizzabili). V3_078 `[02:20]`: «13 giugno
**2027**» dentro la lettura di un atto. Appelli nominali integrali illeggibili in tre registrazioni:
**i voti individuali non sono ricostruibili dall'audio**, solo i totali proclamati — limite da
scrivere nel rapporto. V3_076 dura 31 secondi e il manifest dichiara `0:00`. Fra V3_076 e V3_078,
stessa seduta, **mancano ventiquattro minuti** fra l'appello fallito e quello valido.

**E un atto che dichiara di non contenere la sostanza**: il verbale di V3_080 rinvia esplicitamente
alla registrazione per gli elementi non riportati.

**Dieci item su dodici abbinati a mano** a verbali che il censimento non assegna (è vuoto per tutti
e dodici). Anche questo lettore ha ritrovato da solo il link nel verbale del Municipio XI: terza
volta che il meccanismo emerge dal basso.

## 68. V3_085–V3_096: tre strade indipendenti allo stesso difetto (2026-09-16 08:51Z)

Dodici registrazioni, 41 candidate (31 `solo dal parlato`, 10 `anche negli atti`), tutte a
pagamento, quindi **tutte e 41 con evidenza a grana di cinque minuti**: vanno dichiarate in blocco
come verificabilità grossolana, non mescolate alle altre.

**Il lettore ha trovato §66 da solo, dall'interno della lettura.** Mentre io ci arrivavo chiedendomi
chi scrivesse la colonna `verbale_match`, lui ci è arrivato cercando la convocazione di una seduta:
`A2_MMC_XII_NDUxNjI` esiste in `A2_text/` e **non ha una riga** in `confronto_atti.csv`. Chi si
fosse fidato del foglio avrebbe scritto «convocazione: no».

Verificati i suoi numeri, perché vanno verificati: dice 111 file contro 78 righe sulla famiglia
`A2_MMC_XII`; sono **56 file contro 33 righe**, −41%. Il rapporto è persino peggiore di quello che
riferisce, l'assoluto è sbagliato. Il fatto — la convocazione c'è e il foglio non la contiene — è
confermato.

Quindi lo stesso difetto è emerso oggi da **tre strade indipendenti**: la mia sui link (§62→§66), la
frase di V3_077 che cambia esito solo per il confine del corpus (§67), e questa. È il difetto da
chiudere prima della consegna, e i due lotti di lettura degli atti mancanti sono partiti.

**Un problema di comparabilità che ne nasce.** Questo lettore, accortosi del buco, ha verificato
ogni candidata anche con `grep` sui testi integrali e ha letto per intero i verbali corrispondenti.
Le sue 31 `solo dal parlato` reggono un controllo **più severo** di quello degli altri lotti. Ha
ragione a dirlo: non sono confrontabili con chi ha usato il solo foglio. Un lotto in più con una
definizione diversa, e stavolta l'ha creato la diligenza di un lettore, non un mio emendamento.

**Il meccanismo che propone, e che è più preciso del mio.** Non è che i verbali manchino: è che
**quando ci sono riassumono via esattamente ciò che ha valore**.
- V3_088: il verbale scrive «descrivendo poi tutte le caratteristiche dei 4 quadranti», e in quella
  frase spariscono il 15% di posti riservati a bambini con disabilità con operatore uno-a-uno, il
  10% ai segnalati dai servizi sociali, i 485 posti e lo spostamento di Saxa Rubra di quadrante.
- V3_095: il verbale è di trenta righe, elenca i presenti al minuto e dichiara che «la
  videoregistrazione della seduta sostituisce la trascrizione a verbale degli interventi». I 135.000
  euro per due assistenti sociali alla tutela minori esistono **solo** nella registrazione.
- V3_089: la proposta sui cinghiali diventa una riga, e sparisce tutto il dispositivo — piano in 30
  giorni, tavolo permanente, rendicontazione trimestrale, numero verde 24 ore.

Con il corollario che chiude il ragionamento: **nelle sedute-monologo il verbale è quasi verbatim e
non c'è nulla di nuovo** (V3_085). La novità nasce dove c'è dialogo, e il dialogo è precisamente la
parte che il verbale comprime. Va nel rapporto accanto al meccanismo di §67: uno dice perché il
parlato è il residuo, questo dice come il residuo viene prodotto.

**Contraddizioni fra livelli che nessuna delle due carte mostra da sola.** Il 12 giugno in
commissione capitolina si dice che sul Casale Zola il municipio «ha avviato un rilevamento interno»
e che non c'è cantiere; il 17 giugno un verbale municipale presenta una delibera di Giunta che
**adotta un progetto di fattibilità da 600.000 euro**. Il centro non sa quello che il municipio ha
già fatto. E la stessa proposta capitolina sui defibrillatori è letta **250 mq nel XV e 200 mq nel
III** nella stessa settimana.

**Un difetto suo che ho verificato e ridimensionato.** Dice che `grana_marcatore_s` non corrisponde
(V3_085 dichiara 209 s, i marcatori distano 298 s). Vero per quell'item; misurato su tutte le
registrazioni con almeno tre marcatori, la grana dichiarata coincide con la mediana reale entro il
10% in **259 casi su 260**. Il difetto esiste dove i marcatori sono due — registrazioni di pochi
minuti — e lì il valore dichiarato è privo di senso, non dove la registrazione è lunga.

**Due rilievi sulla soglia che vanno risolti, non archiviati.** In V3_094 l'unica cosa decisa —
una risoluzione approvata 6-1 che impegna il Municipio ad applicare la regola 3-30-300 a tutte le
riqualificazioni — **resta fuori** perché non nomina un bene, mentre entra una citazione di
passaggio a una via. E la proposta sui cinghiali entra solo perché il proponente ha messo molti
toponimi nelle premesse: «la discriminante non è il peso dell'atto ma la prosa». È il rilievo 4.1
del C3, che avevo chiuso dichiarando il claim come territoriale; due lettori indipendenti ora lo
riportano dal campo. La dichiarazione regge, ma va scritta nel rapporto con questi esempi, non in
astratto.

**E una decisione di riservatezza che il lettore ha preso meglio di come la specifica la impone**:
riportando l'insediamento oggetto di decisione ha **omesso la designazione etnica usata in aula**,
non vietata da DEC-102 ma inutile al fatto e stigmatizzante. Va aggiunto alla specifica come regola.

## 69. Correzione a §66: l’allarme era sbagliato, il difetto vero è un altro e più piccolo (2026-09-16 09:07Z)

In §66 ho scritto che l'insieme di confronto sono «gli atti letti, non gli atti che abbiamo», e che
il 58,0% non era difendibile. **Il lettore del lotto X01 ha smontato la premessa**, e ricontrollando
ha ragione lui.

Misurato sul repertorio di Atti Web, senza margine di dubbio:

| | |
|---|---|
| atti in `confronto_atti.csv` con repertorio **8–28 giugno** | 1.983 su 1.983 |
| atti mai confrontati con repertorio **di giugno fuori dall'8–28** | 685 su 685 |

I 1.983 **non sono gli atti che qualcuno ha letto: sono esattamente il perimetro dello studio**,
8–28 giugno, che l'HANDOFF prescrive. I 685 non sono stati dimenticati, sono fuori finestra. E la
mia misura del rischio — «151 candidate, il 36%, nominano un luogo che compare in un atto mai
confrontato» — contava **compresenze di toponimo con atti dell'1–7 e del 29–30 giugno**, cioè fuori
perimetro per costruzione. **La ritiro.**

**Che cosa resta, ed è preciso.** Il lettore ha isolato il meccanismo che nessuno aveva guardato:

- per i **verbali** (MMV, GMV, CMV) la data di repertorio **è** la data della seduta. Verificato sul
  suo lotto: 21 verbali su 21. Quindi il verbale di una seduta dell'8–28 giugno sta sempre dentro i
  1.983, e da quel lato non manca niente;
- per le **convocazioni** (MMC) la data di repertorio è la data del **protocollo**, che precede la
  seduta. Verificato: 12 su 12, protocolli del 3–5 giugno per sedute dell'8–15 giugno.

Da cui il difetto vero, sistematico e tutto mio: **ogni seduta dei primi giorni della finestra la cui
convocazione è stata protocollata prima dell'8 giugno ha la convocazione fuori dall'insieme di
confronto.** Non è un caso sfortunato, è una conseguenza necessaria di aver definito il perimetro
sulla data di repertorio quando per un tipo di atto quella data non è la data del fatto.

Pesa meno di quanto pesava l'allarme che ho scritto: una convocazione annuncia, raramente contiene
il fatto. Tocca il collegamento registrazione-convocazione, non il gemello scritto di una notizia.
Ma va chiuso, e i due lotti X01/X02 lo stanno chiudendo: X01 ne ha già lette 12.

**E una cosa che va detta a parte perché è vera e sopravvive a tutto il resto.** Il verbale di una
seduta di fine giugno, repertoriato a luglio, **non ce l'abbiamo affatto**: `A2_text/` contiene solo
atti di giugno. Lì non è questione di insieme di confronto, è che il documento non è mai stato
scaricato. Da verificare quanto pesa, ed è la sola parte di §66 che potrebbe ancora spostare il
numero principale.

**Quarta volta oggi.** Quattro volte una mia misura ha smentito chi aveva letto il materiale, e
quattro volte era la mia misura a essere sbagliata (§56, §60, §62, questa). La regola di §60 regge
solo se la applico *prima* di scrivere, non dopo: qui l'ho scritta nel rapporto e poi corretta.
L'unica difesa che ha funzionato è stata far leggere il materiale a qualcuno.

## 70. X01 e X02: il buco misurato, e quanto grande è (2026-09-16 09:11Z)

Due lotti indipendenti, 65 atti, stesso meccanismo trovato da entrambi senza sapere l'uno dell'altro:

> **Atti Web indicizza i verbali per la data della seduta e le convocazioni per la data del
> protocollo.**

Verificato: X01, 21 verbali su 21 con repertorio = seduta, 12 convocazioni su 12 con protocollo che
precede; X02, 11 verbali su 11 e 21 convocazioni, **19 delle quali convocano una seduta dentro
l'8–28 giugno** pur essendo repertoriate fra l'1 e il 5. In totale 31 convocazioni su 33 (94%)
riguardano sedute della finestra.

**Quanto è grande il buco, adesso che so come contarlo.** Fra i 685 atti fuori finestra, quelli
repertoriati **1–7 giugno** sono candidati a riguardare sedute dentro la finestra:

| | 1–7 giugno | 29–30 giugno |
|---|---|---|
| convocazioni (MMC, CMC, CPC) | **127** | 33 |
| verbali (MMV, CMV, GMV, CPV) | 95 | 20 |
| altro | 333 | 77 |

I 95 verbali dell'1–7 **non servono**: se il repertorio è la data della seduta, quelle sedute sono
dell'1–7 e stanno fuori dal perimetro dei fatti, non solo da quello degli atti. Servono le **127
convocazioni**, di cui 31 già lette: ne restano **96**, e i lotti X03, X04 e X05 le coprono tutte.

Con questo il difetto smette di essere un allarme e diventa un lavoro con una fine.

**Un difetto di fonte che vale il rapporto.** X02: venti righe `ocr_incerto`, ma **solo nove portano
il marcatore Tesseract**. Le altre undici sono **PDF nativi con lo strato di testo corrotto
all'origine**, e non sono sparse: sono **tutti e dieci gli atti del Municipio XII** del lotto, più
uno. `ROMA CM'IT~LE`, `Prot. ca-l'Io`, `RCl16286I2026` dove `l` e `I` stanno per `/`. Un Municipio
pubblica sistematicamente PDF con testo inservibile e la nostra estrazione lo copia senza passare da
Tesseract: è una fonte difettosa, non rumore casuale, ed è la conferma sul campo della regola della
specifica (`ocr_incerto` vale sul testo, non sul marcatore).

**Perché i verbali arrivano tardi, detto da un verbale.** Il 30 giugno una commissione del Municipio
X **non riesce ad approvare** i verbali delle sedute dell'1, 9, 10 e 23 giugno per mancanza del
numero legale. Il ritardo del record non è disorganizzazione: è la stessa mancanza di numero legale
che blocca le decisioni.

**E un precedente su DEC-102 che viene dall'amministrazione.** In `A2_MMV_X_NjIwNzc` **la fonte
anonimizza da sola**, scrivendo `Omissis` al posto dei nomi degli ospiti esterni. Su quei verbali
l'ente fa già quello che noi facciamo: da citare, perché smentisce l'idea che la protezione delle
persone sia un'invenzione nostra imposta alla fonte.

**Due rilievi dei lettori che restano aperti per l'owner o per me.**
1. I civici dei **beni pubblici**: X02 li ha tenuti (Parco Clemente Riva, Salaria Sport Village, ex
   scuola Quartararo) e ha tolto quelli legati a persone, incluso il **numero di banco di un
   mercato**, che è di fatto un numero di concessione. È esattamente la D5 aperta; il lettore ha
   applicato la linea che la D5 propone. Se l'owner decide diversamente è una passata automatica
   sulla colonna `luoghi`.
2. L'emendamento sulle convocazioni non copre i `CPC` capitolini: X02 l'ha esteso per non avere due
   metri per lo stesso oggetto, dichiarandolo e rendendolo reversibile in blocco. Scelta giusta.

## 71. La data del fatto per le convocazioni: difetto reale, effetto minimo (2026-09-16 09:14Z)

Continuando su §70 ho guardato che cosa `build_db.py` usa come data del fatto per un atto:
`data_repertorio`, sempre. Il campo `validita_o_seduta`, che i lettori compilano da quattro lotti,
**non era letto da nessuna parte**.

Misurato sulle convocazioni già dentro il database (B01–B40):

| | |
|---|---|
| la data di seduta **diverge** da quella di repertorio | **242** |
| la data di seduta non è scritta | 221 |
| coincidono | 46 |

Per 242 convocazioni la data del fatto nel database era quindi sbagliata, a volte di settimane
(repertorio 12 giugno, seduta 1 luglio). Siccome la deduplicazione appaia a **un giorno** di
distanza, l'accostamento fra una convocazione e la seduta che convoca era impossibile **per
costruzione** — e non ai bordi del perimetro, dentro.

Corretto: `data_del_fatto()` legge la data di seduta per le sole convocazioni (MMC, CMC, CPC), in
entrambe le grafie, e se il campo ne porta più d'una diversa non sceglie e ricade sul repertorio.
Per gli altri tipi il campo porta una *validità*, non una seduta: leggerlo lì sarebbe un errore
peggiore di quello che corregge.

**Effetto sul numero principale, misurato isolando la sola correzione** (stessi ingressi, due
esecuzioni):

| | senza correzione | con correzione |
|---|---|---|
| S (nessun gemello scritto) | 478 | 476 |
| D (almeno un duplicato) | 10 | 12 |
| quota di novità | [55,4% , 98,8%] | **[55,2% , 98,6%]** |

**Due candidate su 863. Due decimi di punto.** Il difetto era reale, la correzione resta perché una
data sbagliata è sbagliata, ma non sposta niente — e conferma per misura quello che in §69 avevo
solo asserito: *una convocazione annuncia, raramente contiene il fatto*.

**Il che vuol dire anche questo, e va detto senza giri.** La catena partita stamattina da §66 —
allarme, ritiro, meccanismo, correzione — è costata quattro lotti di lettura e mezza giornata per
due decimi di punto sul numero principale. I lotti non sono sprecati (danno fatti territoriali, il
collegamento delle convocazioni e la misura del meccanismo), ma chi legge il rapporto deve sapere
che il buco esisteva e **non era dove pensavo, e non pesava quanto temevo**. Quando arriveranno
X03–X05 con le altre 96 convocazioni, l'attesa ragionevole è che spostino altrettanto poco: lo
scrivo prima di vederlo, così è una previsione e non una razionalizzazione.

**Numeri aggiornati a 193 registrazioni lette su 415** (96 RomaTV + 97 YouTube):
quota di novità **[55,2% , 98,6%]**, e **37,5%** scartando le righe che poggiano su un toponimo
dichiarato incerto (31,9% delle S). La scala dei tre numeri diventa **37,5 / 55,2 / 98,6**, da
rifare ancora alla consegna.

## 72. X03 e X04: la mia stima del buco era generosa del doppio (2026-09-16 09:24Z)

Avevo scritto nel mandato dei due lotti che le convocazioni repertoriate 1–7 giugno sono «quasi
tutte per sedute dentro l'8–28», con scarto 3–11 giorni. **Tutti e due i lettori hanno misurato e
mi hanno smentito**, ciascuno per conto suo.

| | X03 | X04 | insieme |
|---|---|---|---|
| convocano una seduta **dentro** l'8–28 | 12 | 13 | **25 su 64 (39%)** |
| convocano una seduta **prima** dell'8 | 15 | 18 | 33 |
| data di seduta illeggibile | 5 | 1 | 6 |

Lo scarto protocollo→seduta ha **mediana 3 giorni**, non 3–11. La mia stima nasceva dai 33 atti dei
lotti X01/X02, che però venivano da un elenco **già filtrato** su chi portava una data dell'8–28 nel
testo: ho estrapolato da un campione selezionato e non me ne sono accorto.

Controprova aritmetica sulle 127 convocazioni, senza leggerle: sono repertoriate 29 il 1°, 42 il 3,
28 il 4, 28 il 5. Con scarto 3 ne cadrebbero dentro 28; con scarto 4, 56. Il 39% misurato ci sta in
mezzo. **Il buco vero è di circa cinquanta convocazioni, non di centoventisette.**

**Due risultati dei lettori che valgono per il rapporto.**

1. **Lo scarto massimo è 14 giorni** (protocollo 1° giugno, seduta 15), e **non è uniforme fra
   Municipi**: il V protocolla e convoca a uno-due giorni di distanza, il XII protocolla in blocco a
   inizio mese sedute anche di due settimane dopo. Quindi **allargare la finestra di repertorio non
   è una soluzione**: qualunque ampiezza si scelga tratta i Municipi in modo diseguale. La soluzione
   è quella che ho messo in `build_db.py`, cioè leggere la data della seduta.
2. Delle 10 notizie candidate di X04, **solo 2 cadono dentro l'8–28**. Il valore del lotto sta in
   sedute appena fuori finestra: correggere il perimetro le recupera solo in parte.

**Difetti della fonte, nuovi e ripetuti.** I **moduli prestampati compilati a mano del Municipio
VIII**: Tesseract non legge la grafia proprio dove stanno data, ora e ordine del giorno — cioè il
campo che il lotto doveva misurare (`08-96 n Lo ZG alle ore v4 : 30`), e un atto è illeggibile per
intero. Il **Municipio XII** conferma il difetto di X02: `Municipio Roma Xli` per XII in tutti i
suoi atti, testo nativo corrotto all'origine. Un atto nativo del VII esce dall'estrazione con **due
colonne interlacciate**, frasi rimontate fuori ordine. E cinque atti del Municipio V **convocano in
modalità online su Teams una seduta il cui ordine del giorno è un sopralluogo in strada**: da nessun
atto si può dedurre che il sopralluogo si sia svolto.

**Tre scelte dei lettori che vanno decise, non archiviate.**
1. **I civici dei beni pubblici**: X04 li ha tenuti (sedi, parco, uffici anagrafici) perché non
   identificano nessuno; X03 li ha omessi tutti per prudenza; B28 li omette. **La pratica non è
   uniforme**, e i lettori lo dichiarano entrambi. È la D5 aperta: finché l'owner non decide,
   i lotti divergono. Ho messo nel mandato di X05 la linea D5 (civici pubblici sì, civici di
   persone no) per non allargare la divergenza.
2. **Le particelle catastali**: X04 ha omesso `foglio 423, particella 178` ragionando che una
   particella identifica un fondo e quindi il proprietario, come un civico identifica
   un'abitazione. La specifica non le elencava. **Ha ragione**, e l'ho aggiunta al mandato.
3. **L'emendamento sulle convocazioni non copre le `CMC` di Consiglio**: X03 l'ha esteso per
   analogia, 6 righe su 7 ne dipendono. Va scritto nella specifica o quelle righe vanno riviste.

**Un rilievo sul quale il lettore ha applicato la lettera e ha ragione a segnalarlo**: un atto
nativo con le colonne interlacciate non ha errori di *riconoscimento*, quindi `ocr_incerto = no`
per la lettera della regola; ma se quel campo misura «quanto testo è inaffidabile», quel testo lo è.
Da sistemare nella specifica prima della consegna: o la regola cambia nome, o cambia definizione.

**Quinta e sesta smentita della giornata**, e stavolta la mia non era una misura ma una **stima
messa in un mandato**, dove pesa di più: due lettori hanno lavorato con in testa un'aspettativa
sbagliata. Entrambi l'hanno misurata invece di confermarla. Nel mandato di X05 ho scritto la stima
corretta **e** l'istruzione di misurarla comunque.

## 73. I lotti X dentro il database: la previsione regge (2026-09-16 09:37Z)

X05 chiuso: **17 su 32** dentro la finestra (15 se si pretende che l'anno della seduta sia letto e
non dedotto: due atti scrivono giorno e mese e non l'anno, e il lettore ha messo `non verificato`
invece di dedurlo — regola applicata bene). Con X03 e X04 fa **42 su 96**, il 44%, vicino al 39%
misurato prima e lontano dal «quasi tutte» che avevo scritto io.

**X05 smentisce anche un'ipotesi di X04.** X04 aveva detto che il Municipio XII protocolla in blocco
a inizio mese; in X05 il XII ha scarti di 2 e 7 giorni, e lo scarto massimo del lotto (14 giorni)
viene dal **Municipio XI**. La regolarità per Municipio non generalizza: quello che resta è che gli
scarti **variano molto**, fra 0 e 14 giorni, e questo basta a dire che allargare la finestra non
funziona. Le **commissioni capitoline** sono la parte più produttiva del recupero, 10 su 14 dentro,
con scarti regolari di 4-9 giorni.

**Integrazione nel database.** `estendi_manifest_x.py` aggiunge gli atti dei lotti X al manifest del
Report 2 — **in coda, mai in mezzo**, perché l'identificativo `A2_NNNN` segue l'ordine del manifest
e inserirli in ordine alfabetico avrebbe rinumerato ogni atto già citato dai lotti. 161 righe
aggiunte, zero «ATTO SENZA MANIFEST». Il glob di `build_db.py` passa da `out/B*_atti.csv` a
`out/[BX]*_atti.csv`.

**Effetto misurato isolando i soli lotti X** (stesse 199 registrazioni, 883 candidate, due
esecuzioni consecutive):

| | senza i lotti X | con i lotti X |
|---|---|---|
| S | 491 | 480 |
| U | 378 | 389 |
| quota di novità | [55,6% , 98,4%] | **[54,4% , 98,4%]** |

**Undici candidate passano da «certamente nuova» a «incerta»: 1,2 punti.** In §71 avevo scritto,
prima di vedere, che avrebbero spostato pochissimo. Regge — e stavolta la previsione l'avevo messa
per iscritto prima della misura, che è l'unico modo perché valga qualcosa.

**Numeri correnti, 199 registrazioni lette su 415:** scala **36,8 / 54,4 / 98,4**, con il 32,3%
delle righe «certamente nuove» che poggia su un toponimo dichiarato incerto. Stratificata: didascalie
YouTube [59,3 , 98,5], a pagamento [55,6 , 98,4], piattaforma [28,2 , 98,1].

**Recupero delle due registrazioni perse** (§65) avviato dall'mp3 già pronto, senza riscaricare
nulla; il segmento vuoto di `41e7b841` resta in attesa che la pozza dei quattro scaricamenti si
liberi.

**E un rilievo di X05 che non va perso.** Il lettore ha lasciato `municipio = non verificato` su 9
righe `CEN_` su 14 «anche dove il toponimo lo renderebbe ovvio». È l'applicazione giusta della
regola (un dedotto non si scrive come letto) e insieme una perdita: quelle nove righe non entrano in
nessuna statistica per Municipio. Va deciso se il territorio dei `CEN_` si ricava dal toponimo
dichiarando la deduzione, o se resta vuoto. Lo aggiungo alle decisioni aperte.

## 74. C4 e V3_097–V3_108: sette bocciature e un’ipotesi smentita misurando (2026-09-16 09:53Z)

### Il controllo C4 sul rapporto scritto

Sette rilievi **BLOCCANTI**, tutti fondati. I quattro che cambiano il testo:

1. **«Contro i 1.983 atti» era falso.** `novita_meccanica.py` confronta il parlato contro **tutte le
   righe scritte**, atti *più* notizie del Report 1. Il nome del campo
   (`novita_rispetto_agli_atti`) dice meno di quello che il numero misura. Corretto nel rapporto e
   dichiarato come difetto di nome.
2. **Il 36,8% non esce dal programma che calcola gli altri due.** Lo calcola `audit_toponimi.py`, e
   scrivere «da cui la scala» faceva credere a una sola formula. Corretto.
3. **«È il pavimento: regge a qualunque obiezione»**: falso. Regge all'obiezione sulla trascrizione,
   non a quella sulla deduplicazione. Riscritto.
4. **La dispersione fra lotti**: il testo diceva «lotti letti a regola mobile contro regola ferma»,
   il programma divide per corpus (YouTube contro RomaTV). I due gruppi differiscono per la regola
   **e** per il materiale, e la misura non separa le cause. Riscritto come segnale, non come misura.

E un rilievo che ha trasformato un aneddoto in una misura. Il §1 diceva che la frase «la
videoregistrazione sostituisce la trascrizione» sta «in due verbali» e che «tutto il resto discende
da qui». Due verbali non reggono una tesi, e il C4 aveva ragione a bocciarla. Misurato invece con
`record_dichiarato.py` su tutti e 2.668 gli atti:

| formula | atti | Municipi |
|---|---|---|
| la registrazione **sostituisce** il verbale | 21 | II |
| si rimanda alla registrazione | 37 | VIII, XI, XII |
| il verbale è dichiarato **sommario** | 15 | IX |
| versione integrale sul portale | 34 | I, XV |
| **totale** | **107** | **7 Municipi su 15** |

Centosette atti, quasi tutti verbali, in sette Municipi su quindici, dichiarano **dentro il proprio
testo** che il record completo della seduta non è l'atto ma la registrazione. Non è una nostra tesi:
è l'amministrazione che lo scrive. Ora il §1 dice questo.

Restano aperti dal C4: l'audit di precisione e richiamo della deduplicazione (mai fatto, e i tre
numeri ci poggiano sopra) e l'indice delle evidenze per i casi narrativi. Ho aggiunto al rapporto la
**mappa numero→programma** e tre punti nuovi alle incertezze, fra cui le **tre condizioni che
smentirebbero** il meccanismo del §2, scritte perché qualcuno le verifichi.

### Il lotto V3_097–V3_108

**Ipotesi 2 smentita per metà, e la variabile vera è un'altra.** Non è monologo contro dibattito: è
**la forma del verbale**. I verbali scritti in prosa narrativa estesa — redatti riascoltando —
tengono tutto, comprese le cifre che la trascrizione storpia (un verbale scrive 17.182,05 euro dove
la registrazione dice «17.000»); i verbali a elenco puntato tengono intestazione e presenze e basta.
Il caso estremo: un verbale registra «Intervengono il presidente, il consigliere X e il consigliere
Y» e nient'altro, mentre l'intera discussione esiste solo nella registrazione.

**Una terza nicchia, non prevista**: l'**esito di un accesso agli atti letto ad alta voce** —
autovelox chiesto nel 2022 e mai autorizzato, attraversamenti illuminati chiesti nel 2023 con un
atto di giunta e mai installati. Nasce dentro uno scontro politico, cioè esattamente dove le prime
due nicchie dicevano che non si trova niente.

**E una precisazione che corregge la nicchia della lettura ad alta voce**: leggere un documento
**che è nel corpus** produce corrispondenze, non novità. La novità è **ciò che i presenti aggiungono
attorno al documento** — i plessi che la delibera non nomina, il sopralluogo ricordato a memoria.

**Il difetto della ripetizione è peggiore di come l'avevo scritto.** Non gonfia il conteggio delle
parole: **cancella il parlato del tratto in cui si innesca**. In un item sparisce l'illustrazione
dell'atto da parte della proponente, in un altro l'inizio dell'intervento critico. `quota_ripetuta`
misura quanto, non che cosa. Emendata la specifica, e con essa la regola che faceva scrivere `0` nei
campi di volume: uno zero è indistinguibile da un dato vero, ora si scrive `non attendibile`.

**Un errore in un atto trovato dall'incrocio con l'audio**: un verbale dichiara la chiusura alle
12:35 di una seduta che la registrazione chiude alle 9:33. Tre ore di scarto, visibili solo mettendo
insieme le due fonti.

**E il costo della riservatezza, detto dal lettore meglio di come lo dice la specifica**: in una
seduta il fatto è che la titolare di un banco non ha mai protocollato una domanda; il verbale
municipale lo scrive con numero di banco e tipo di attività, noi no. «Chi volesse contestare la
notizia non ha abbastanza per farlo.» È il prezzo di DEC-102, ed è giusto pagarlo, ma va scritto nel
rapporto invece di far finta che non ci sia.

## 75. La deduplicazione consumava le righe, e il numero principale ne usciva gonfio di sette punti (2026-09-16 09:58Z)

Il C4 aveva scritto, in astratto, che i tre numeri poggiano su una deduplicazione mai misurata
(§6.4). Sono andato a guardare il codice invece di preparare solo il campione, e il difetto era lì.

`build_db.py` deduplica come il metodo §4.1 descrive il lavoro a mano: scorre le righe e, appena una
prende un gemello, **la toglie dai confronti successivi**.

```python
for i, a in enumerate(gruppo):
    if a['dedup_stato'] != 'unica': continue        # a e' gia' legata: esce
    for b in gruppo[i + 1:]:
        if b['dedup_stato'] != 'unica' ...: continue # b e' gia' legata: esce
```

Va bene per contare la resa netta, che è a cosa serve. **Non va bene per la domanda del Report 2**,
che è: *questa cosa detta in aula sta scritta da qualche parte?* Misurato:

- **111 candidate del parlato** avevano come unico gemello **un'altra registrazione**, e dopo quel
  legame non sono mai state confrontate con nessuna riga scritta;
- **537 righe scritte su 1.855 (29%)**, già legate a qualcosa, erano fuori da ogni confronto
  successivo: una candidata del parlato che arrivava dopo non poteva più incontrarle.

Entrambe le cose fanno risultare «nuovo» ciò che non è stato confrontato.

**Correzione.** Non ho toccato la deduplicazione: aggiungere una seconda regola di validazione in
due copie è il modo di farle divergere. Ho aggiunto in `build_db.py` un **passaggio esaustivo** che
prova tutte le coppie parlato-contro-scritto e scrive per ogni riga del parlato quanti gemelli
scritti esistono davvero (`gemelli_scritti`), usando le **stesse** funzioni `stesso_luogo` e
`stesso_oggetto`. `novita_meccanica.py` e `audit_toponimi.py` ora leggono quella colonna.

**Effetto, su 923 candidate del parlato:**

| misura | S | U | D | quota di novità |
|---|---|---|---|---|
| catena della deduplicazione (quella che usavo) | 503 | 405 | 15 | [54,5% , 98,4%] |
| **confronto esaustivo** | **435** | **459** | **29** | **[47,1% , 96,9%]** |
| esaustivo dentro il blocco, come prescrive il metodo | 455 | 439 | 29 | [49,3% , 96,9%] |

**Sette punti e mezzo di novità in meno.** È la correzione più grande della giornata, ed è di gran
lunga più grande di tutto quello per cui mi ero allarmato stamattina: la data del fatto delle
convocazioni valeva 0,2 punti, i 161 atti recuperati 1,2, questo 7,4.

La riga «dentro il blocco» va tenuta in vista: il metodo confronta dentro i blocchi tematici, e
confrontare su tutto il corpus è una nostra deviazione che **abbassa** la novità di due punti.
Dichiarare entrambe è l'unico modo onesto: la deviazione si vede invece di essere un miglioramento
silenzioso del metodo di qualcun altro.

**Scala aggiornata: 32,1 / 47,1 / 96,9** (il 32,1% scarta le righe che poggiano su un toponimo
dichiarato incerto, che sono il 32,0% delle S).

**Resta da fare, e il campione è pronto** (`report2/campione_dedup.py` → `campione_dedup.md`): far
giudicare a un lettore 17 coppie unite (precisione) e 40 coppie non unite che condividono toponimo e
data a un giorno (richiamo), su 283 trovate. Giudicare se due righe sono lo stesso fatto è lettura,
non calcolo, e il programma prepara il campione senza pretendere di rispondere.

**E una cosa che il mio stesso emendamento ha rotto.** Il sesto emendamento fa scrivere
`non attendibile` invece di `0` nei campi di volume; il builder faceva `int(...)` e si è fermato al
primo lotto che l'ha applicato. Corretto: quel valore diventa una cella vuota, che nelle statistiche
di volume non si somma. Cambiare un contratto costa sempre da qualche parte, e stavolta il costo si
è visto subito.

## 76. V3_109–V3_120: una segnalazione DEC-102 che viene da un altro ramo (2026-09-16 10:12Z)

Dodici registrazioni, 34 candidate, cronometraggio item per item (il lettore lo dichiara e si vede:
da 44 s a 209 s). Due item a zero candidate, entrambi di pura procedura.

### La segnalazione che ho verificato per prima

Il lettore ha escluso dai propri file tre vicende personali di una commissione capitolina, **e poi
si è accorto che una rientrava dal ramo atti**: la notizia N1296, estratta dallo stesso verbale,
portava fra i `luoghi` il nome di un liceo. Ha scritto: «il rispetto di DEC-102 sul ramo video non
serve se la stessa informazione entra dal ramo atti».

Verificato nell'atto. Il verbale racconta per esteso un caso che riguarda **uno studente minorenne**
— un principio di sospensione per il mancato riconoscimento della carriera alias —, con la scuola
nominata. La nostra riga **non racconta quella vicenda**: dice che gli sportelli hanno riaperto in
tre Municipi, con sedi e accessi. Quindi non era una violazione in atto, e la conclusione del
lettore («la stessa informazione entra dal ramo atti») è più forte di quello che i dati mostrano.

Ma il nome della scuola in quella colonna **non serviva al fatto che la riga afferma** — la scuola
non è una sede di sportello, è il luogo dell'episodio — e accostato a un episodio pubblico
contribuisce a identificare un minore. DEC-102 lo dice per esteso: *un nome non è l'unico modo di
identificare una persona*. Tolto, con `fix_b07_scuola_minore.py` e copia di sicurezza; nessun'altra
riga del corpus lo portava (l'unica altra occorrenza di quel nome è il commediografo, in un evento).

**La lezione vera è la sua, non la mia correzione**: le regole di riservatezza applicate ramo per
ramo non proteggono nessuno, perché un fatto escluso da una fonte rientra dall'altra. Va scritto nel
rapporto come limite del metodo, non come incidente.

### Le ipotesi, smentite di nuovo e meglio

**Ipotesi 1**: delle tre `solo dal parlato` di qualità alta **una sola** sta nelle nicchie previste.
Le altre due sono un tecnico che risponde in audizione ordinaria e una consigliera che illustra un
ordine del giorno — cioè «discussione politica generale», che l'ipotesi dava per vuota. La
riformulazione del lettore regge sui suoi dati: una `solo dal parlato` nasce quando in sala c'è
**qualcuno che deve rispondere di un luogo nominato**, e le sorgenti sono due — un tecnico che dà un
numero su un sito (11 su 19) e un eletto che riporta una segnalazione su una via (8 su 19).

E una regolarità netta, in negativo: **la discussione su un testo senza territorio produce zero
candidate, sempre**. Un regolamento d'aula per 37 minuti: zero. Un regolamento sui defibrillatori
per quasi un'ora di dibattito competente: zero. Un regolamento sugli animali per 80 minuti: una
sola, e arriva fuori ordine del giorno negli ultimi dieci minuti.

**Ipotesi 2**: smentita, e il predittore non è la forma del verbale ma **l'organo che lo redige**. I
verbali delle commissioni capitoline sono quasi verbatim e tengono tutte le cifre — anche quello
della seduta più conflittuale del lotto, 59 KB; quelli del Municipio II sono di sola presenza, 3 KB,
e l'intera audizione sta in una frase. Con il corollario operativo rovesciato: **il video vale meno
dove il verbale è pieno**, e si misura — `solo dal parlato` allo **0% con verbale pieno** (0 su 5),
**50% con verbale di sola presenza** (4 su 8), **71% con verbale assente** (15 su 21).

E i verbali di sola presenza non sono inutili: **sono complementari**. Uno dà i due voti contrari
nome per nome, e nella registrazione non si sentono affatto.

### Il difetto di fonte più grave finora

Un verbale capitolino dichiara la seduta **chiusa alle 14.44**; la registrazione dura fino alle
15.24 e dopo le 14.44 contiene tutta la parte sui Municipi III e VI e la conclusione politica. Negli
ultimi secondi del file la segreteria lo spiega da sé: **dalle 14.46 era rimasta una sola
consigliera**. Quaranta minuti di lavoro pubblico senza numero legale, verbalizzati come se il
numero legale ci fosse stato. Lo stesso, più corto, in un secondo item.

### Normalizzazione retroattiva, che il lettore ha chiesto e che serviva

Il sesto emendamento (`non attendibile` invece di `0`) è comparso **mentre lui leggeva**: ha
applicato la regola nuova a due item e i lotti precedenti avevano scritto `0` per la stessa
condizione. Due codifiche nello stesso corpus, con la sbagliata più frequente — di nuovo il costo di
§63, e di nuovo creato da me. `normalizza_volumi.py` ha riscritto **13 item** (di 39 sopra soglia:
gli altri 26 non avevano messo zero), e solo dove la condizione è vera: uno zero su un item sotto
soglia è un conteggio, non un dato mancante.

**Numeri dopo tutto questo, 226 registrazioni lette su 415**: novità **[48,0% , 97,0%]** su tutto il
corpus, **[50,1% , 97,0%]** dentro il blocco.

## 77. V3_121–V3_132: il meccanismo del rapporto potrebbe essere un artefatto della nostra scala (2026-09-16 10:25Z)

Il rilievo più serio della giornata, e non riguarda un numero: riguarda la tesi.

**Il lettore sostiene che la scala di qualità premia strutturalmente i fatti che stanno negli atti.**
`alta` richiede che il fatto sia *datato*; il parlato d'aula dice «l'anno scorso», «da vent'anni»,
«tre settimane fa». Un fatto che ha una data precisa, in aula, quasi sempre ce l'ha perché **qualcuno
stava leggendo l'atto che la porta** — e quel fatto finisce in `anche negli atti`. Quindi la
differenza di qualità fra nuove e confermate misurerebbe la nostra regola di punteggio, non il
parlato.

Misurato su tutto il corpus letto, dentro il solo parlato (stessi lettori, stesse trascrizioni):

| | alta | media | bassa | quota alta |
|---|---|---|---|---|
| `anche negli atti` | 147 | 115 | 2 | **55,7%** |
| `solo dal parlato` | 120 | 452 | 43 | **19,5%** |
| `non verificabile` | 18 | 67 | 12 | 18,6% |

Il divario è reale e grande — trentasei punti — **dentro lo stesso materiale**. Ma le due spiegazioni
sono entrambe compatibili con questo numero:

- la mia (§67, §2 del rapporto): ciò che resta solo nel parlato è il **residuo**, cioè quello che non
  è ancora diventato fatto compiuto, datato e localizzato;
- la sua: la scala **richiede** la data, e la data in aula la porta l'atto letto ad alta voce.

Non sono alternative, sono lo stesso meccanismo visto da due lati — in entrambe è l'atto a fornire la
data. Ma la sua versione dice una cosa in più che la mia nascondeva: **una parte del divario la
produciamo noi**, con la definizione di `alta`. Il 19,5% non si può leggere come «il parlato è meno
affidabile». Va scritto nel rapporto, e il prossimo lotto ha il compito di contare quante candidate
mancano l'`alta` **solo** per la data.

### Ipotesi 3: due lettori, risultati opposti

Il lotto precedente aveva concluso che il predittore è la forma del verbale (prosa estesa conserva,
elenco puntato no). Questo lettore ha confrontato parola per parola quattro verbali **tutti in prosa
estesa**: **cifre conservate 0 su 23**. E l'unico atto **a tabella** le conserva tutte, perché la
tabella ha una colonna «esito» da riempire. La sua spiegazione: conta **che cosa il verbale è** — un
registro di *chi ha parlato* non ha posto per la cifra, un registro di *decisioni* sì.

Due lettori, stesso metodo, conclusioni incompatibili. **Non scelgo**: la contraddizione va nel
rapporto così com'è, e il lotto successivo ha il compito di misurarla senza sapere quale risposta
farebbe comodo. Una regolarità che due lettori competenti misurano al contrario non è una
regolarità: è una domanda aperta.

### Altre cose che restano

- **Il foglio da solo sovrastima `solo dal parlato` di circa il 15%**: due riscontri decisivi su
  dodici item stavano in `A2_text/` e non nel foglio. Ora è nel mandato di ogni lettore.
- **`anche negli atti` a volte vuol dire «l'atto esisterà»**: una risoluzione letta il 15 giugno è
  repertoriata il 18, una colonnina discussa il 15 compare nel verbale del 19. Il campo è sensibile
  alla data di chiusura del corpus, e va dichiarato.
- **Leggere un atto non basta a produrre luoghi**: in un item la commissione legge un verbale di
  Giunta pieno di toponimi e non ne aggiunge nessuno. Ciò che genera l'aggiunta non è la lettura ma
  **l'esserci stati** — il sopralluogo, l'abitare il quadrante.
- **La trascrizione sbaglia esattamente le parole che valgono**: Eataly→«Ital», Parco Pisino→«parco
  Bisino», protocollo `CF 96796/2026`→«CF 90 6726». E le ripetizioni del modello **si concentrano
  dove le voci si accavallano**: la parte più conflittuale della seduta è la meno leggibile.
- **Un verbale che smentisce la registrazione**: scrive orti «in fase di completamento» e passerella
  «entro fine giugno» mentre in aula si era detto che l'ASL ha interdetto l'area.
- **Un atto ritirato non lascia traccia**: la deroga sul «progetto di vita» che gli uffici facevano
  firmare ai genitori, poi ritirata, esiste solo nella registrazione.
- E `assente` **significa assente dal corpus, non mai scritto**: un verbale di questo lotto risulta
  approvato altrove come «n. 52 del 15.06.2026».

## 78. Ho quasi lanciato un secondo driver ASR sopra il primo (2026-09-16 10:27Z)

Controllo di routine del driver di trascrizione. Ho scritto `pgrep -c '[r]tv_asr_driver.py'` e ho
letto **0**: driver morto, 303 item su 318, si riavvia. L'ho riavviato.

`pgrep` **senza `-f` confronta solo il nome del processo**, che qui è `python3`: il nome dello script
non lo guarda nemmeno. Lo zero non diceva «il driver è morto», diceva «nessun processo si chiama
`rtv_asr_driver.py`», che è sempre vero. Il driver era vivo da sei ore.

Per qualche secondo ne sono girati **due**, sugli stessi item e sulla stessa API a pagamento. Me ne
sono accorto perché la riga dopo, con `ps -eo pid,etimes,args`, ne mostrava due — uno di 22.622
secondi e uno di 17. Ucciso il nuovo per PID (non per pattern: uccidere per pattern in questa
sessione mi è già costato la shell). Nessun doppione scritto, nessuna spesa doppia.

**Terza volta oggi che un conteggio di processi mi inganna**, e sempre nello stesso modo: `pgrep -c`
sui download mostrava 9 processi dove ce n'erano 4 (contava i wrapper `bash -c`), e qui ne mostrava
0 dove ce n'era 1. La regola che mi do: **per contare processi si usa `ps -eo args` e si guarda la
riga**, non un contatore che non so esattamente che cosa confronti. Un numero che non so come è
calcolato non è una misura, e oggi ne ho già sbagliate abbastanza.

Stato vero: driver vivo, **303 item su 318**, $ 34,07 (31,34 €), quattro scaricamenti in parallelo
come da limite.

## 79. L’audit della deduplicazione, e due difetti miei che ha scoperto strada facendo (2026-09-16 10:31Z)

### Quello che ha trovato prima ancora di cominciare

**Due copie dei programmi, divergenti.** Il revisore ha eseguito `report2/novita_meccanica.py` e ha
ottenuto **[55,1% , 98,4%]** invece del [48,0% , 97,0%] che pubblico, e ne ha dedotto che «due
meccanismi diversi convivono nel database». Aveva ragione sul sintomo e la causa era peggiore: nella
cartella dei dati c'erano **copie vecchie** di `novita_meccanica.py` e `audit_toponimi.py`, ferme a
prima della correzione di §75. Lui ha eseguito quelle.

È esattamente la frase che ripeto dall'inizio dello studio — *una regola di validazione in due copie
diverge* — applicata a me. Risolto sostituendo tutte le copie nella cartella dei dati con
**collegamenti** ai file del repository: ora i due percorsi sono lo stesso file e non possono più
separarsi.

**Il campione era fatto male.** La sezione A elencava la riga parlata e un contatore `1/2`, **senza
la riga scritta con cui era stata accoppiata**. Il revisore ha dovuto rieseguire il confronto per
sapere che cosa stesse giudicando. Un campione che non mostra la coppia non è un campione. Corretto,
e corretto nel modo giusto: le coppie ora le scrive `build_db.py` mentre le calcola
(`coppie_parlato_scritto.csv`, 1.197 righe), così chi le audita non le ricalcola con una seconda
copia della regola.

### I risultati

**Precisione degli accostamenti forti: 15 su 29 sono davvero lo stesso fatto (52%, IC 34–69%).**
Nove dei dodici errori sono lo stesso accostamento: **una convocazione contro l'esito della seduta
che convoca**. «Il Consiglio discuterà la mozione X» e «il Consiglio ha respinto la mozione X con
quattro favorevoli e sette astenuti» condividono quasi tutte le parole e non sono lo stesso fatto.
Ma l'effetto sul numero è **+0,1 punti**: quasi tutti quegli errori scivolano da D a U, che
nell'intervallo c'è già.

**Richiamo: 2 candidate su 40 date per nuove avevano davvero un gemello.** Una persa per tre giorni
di scarto e per «casale della Torricella» contro «Parco della Torricella»; una perché il parlato
nomina lo stabilimento e lo scritto scrive «stabilimento balneare non indicato», che è un
non-toponimo trattato come toponimo. Stima: 5,0% [1,4% , 16,5%] → **16 falsi «nuove»** sulle 324 con
vicini, banda [4 , 53].

> **Quota di novità inferiore corretta ≈ 46,5%, banda [42,7% , 47,7%].** Il 48,0% è gonfiato di
> circa un punto e mezzo, al massimo cinque.

### Il difetto che conta più di tutti i numeri

**L'unità su cui la regola lavora non è la stessa dalle due parti: dal lato parlato è il fatto, dal
lato scritto è il documento.** Ogni verbale produce **una riga sola**, il cui titolo copre l'intera
seduta ma la cui sintesi racconta **un punto solo** dell'ordine del giorno. Il revisore l'ha
verificato riaprendo gli atti: in **sei casi su sei** il fatto parlato stava davvero nel verbale, ma
non nella sintesi della riga che lo rappresenta.

Due conseguenze. Giudicare sulle sintesi senza aprire gli atti avrebbe dato precisione **31% invece
di 52%**. E, più grave: **il richiamo è compromesso a monte** — un fatto che nel verbale è il terzo
punto dell'ordine del giorno non ha alcuna possibilità di essere riconosciuto, perché la riga che
rappresenta quel verbale parla d'altro. Non è una soglia da ritoccare: è perdita di informazione
prima del confronto, e la stima del richiamo la eredita.

### Il pezzo che manca davvero, e che ho appena messo in lavorazione

Il revisore ha chiuso indicando dove sta il vero problema del numero: **non nel limite inferiore, ma
nell'ampiezza dell'intervallo**. Le 480 candidate della classe `dubbio` — metà del corpus parlato —
sono contate come nuove in alto e come già scritte in basso, e **nessuno le ha mai guardate**. Dalla
sua osservazione di sfuggita su 41 accostamenti deboli, tre gli sono parsi veri; se la precisione di
U fosse davvero del 5–10%, **la risposta del rapporto starebbe vicino al 97%, non al 48%**.

Lo dice come indicazione e non come misura, ed è corretto così. Ho aggiunto al generatore la
**sezione C** — 40 candidate `dubbio` con tutti i loro accostamenti — e lanciato l'audit. È la
misura che decide come si legge l'intero rapporto.

### E un rilievo sul mio criterio

Il criterio che ho dato è **asimmetrico** («la seconda non aggiunge niente alla prima») ma applicato
a coppie non ordinate: in un caso il parere di commissione non aggiunge nulla alla delibera, mentre
la delibera aggiunge molto al parere, e il giudizio si rovescia a seconda di quale riga si chiami
«seconda». Il revisore ha dichiarato la convenzione che ha scelto e dove sta scritta, così chiunque
può spostarla e ricalcolare. Da sistemare nel criterio prima della consegna.

## 80. Il controllo C5, e la misura che l'audit non poteva fare (2026-09-16 10:38Z)

Ultimo dei cinque controlli Codex, sul codice e sullo schema — che nessuno aveva mai guardato.
Undici rilievi sul programma, cinque sullo schema. Due sono importanti.

**BLOCCANTE, e ha ragione: la deduplicazione non applicava la regola «due su tre».** Il metodo §4.1
dice che due criteri su tre (data ±1 giorno, luogo, oggetto) danno `dubbio` e tre danno `duplicato`.
Il codice invece pretendeva **sempre data e luogo**, e usava l'oggetto solo per distinguere dubbio da
duplicato: una coppia data+oggetto con i luoghi scritti in modo diverso, o luogo+oggetto a quattro
giorni di distanza, non veniva mai accostata. I tre criteri ora si contano davvero, nel confronto
esaustivo, e le coppie portano quali criteri hanno soddisfatto.

Effetto: S da 470 a **469**, U da 480 a **493**. Un decimo di punto. La regola era sbagliata e la
correzione va fatta comunque, ma va detto che non sposta niente: la quasi totalità delle coppie che
condividono data e oggetto condivide anche il luogo.

**E il rilievo che vale più di tutti gli altri messi insieme**, che il C5 formula come proposta:
riparare l'asimmetria dell'unità di confronto introducendo una tabella di «fatti», spezzando i
documenti scritti sui punti dell'ordine del giorno. **La sua proposta non funziona sui nostri dati**:
propone di spezzare i campi già letti (`oggetto_sintetico`, `contenuto`), ma quei campi sono
riassunti di un punto solo — l'informazione si è persa alla lettura, non allo spezzettamento.

Però il testo integrale degli atti ce l'abbiamo. Quindi ho fatto la misura che l'audit non poteva
fare (`copertura_testi_atti.py`): per ogni candidata data per nuova, cercarla **dentro il testo** di
un atto plausibile — stesso Municipio, tre giorni di distanza — con il suo toponimo **e** una parola
del titolo.

> **140 candidate su 394 — il 35,5% — compaiono nel testo di un atto vicino.**

Un toponimo che compare in un atto non prova che sia lo stesso fatto: **35,5% è un tetto, non una
stima**. Ma va messo accanto al 5% che l'audit sul confronto fra righe aveva misurato, perché i due
numeri dicono cose diverse: il 5% è quello che il confronto fra righe **poteva ancora vedere e non ha
visto**, il 35,5% è quello che per costruzione **non poteva vedere**. Fra i 140 c'è N1873, uno dei
due gemelli veri che il revisore aveva trovato a mano: il metodo sul testo integrale lo ritrova.

**Quindi il limite inferiore del 48% è molto più molle di quanto l'audit da solo lasciasse credere**,
e va scritto così. Con la complicazione che le due misure aperte tirano in direzioni opposte: questa
abbassa il limite inferiore, l'audit della classe `dubbio` (in corso) potrebbe alzare il superiore
fino a renderlo la risposta. Il rapporto deve dire questo, non un numero.

**Gli altri rilievi del C5, da fare prima della consegna**: la scelta del «lotto più recente» confronta
stringhe (`L9` contro `L10`); `settimana` è calcolata sulla data del fatto invece che su quella di
pubblicazione, e falsa le tabelle territoriali; `integra_gemello_id` e `campi_integrati` non sono mai
riempiti, quindi il contributo informativo dei duplicati del Report 2 non è misurabile;
`vicende.confidenza` dipende dall'ultima riga processata; lo schema ammette **un solo** `gemello_id`
mentre una notizia può averne molti; e i nomi delle colonne nello schema non coincidono con quelli
prodotti (`titolo` contro `titolo_anonimizzato`), per cui un programma conforme allo schema non
leggerebbe i nostri file.

Registro: C5 16.508 token in, 19.378 out, 0,29 €.

## 81. Prova T4: la prima misura misurava la mia finestra, non le candidate (2026-09-16 10:44Z)

La seconda AI indipendente sulle candidate — prova T4 del metodo, mai fatta, prescritta dall'HANDOFF
§4. Prima ho verificato che fosse lecita: il metodo la blocca finché la chiave OpenAI non è ruotata
(regola *fail-closed*), e l'HANDOFF dice che **l'owner ha inserito la nuova chiave la sera del 15
settembre**. Rotazione fatta, blocco caduto, T4 autorizzata.

**Che cosa le ho mandato, e perché proprio quello.** Alle candidate dalle registrazioni ho allegato
il tratto di trascrizione attorno al marcatore citato: quell'audio **è già stato mandato alla stessa
API per essere trascritto**, quindi non esce da dove non fosse già uscito. Alle candidate dagli atti
ho mandato la sola riga anonimizzata: i testi degli atti alla API non sono mai stati mandati, e
alcuni contengono dati personali che questo studio ha già documentato. L'asimmetria è voluta e va
dichiarata: sulle dieci righe da atti la seconda AI ha potuto giudicare solo la coerenza interna.

**Primo risultato: 12 discordi su 20.** Un sessanta per cento di disaccordo avrebbe cambiato la
lettura di tutto il lavoro dei lettori. Ma i motivi erano quasi tutti della stessa forma: *«X non
compare nell'evidenza allegata»*. L'evidenza allegata era la mia: **duemila caratteri attorno al
primo marcatore**. Una candidata con più marcatori, o il cui dettaglio arriva più avanti dentro un
blocco da cinque minuti, risultava non sostenuta **per costruzione**.

Rifatta con l'estratto attorno a **tutti** i marcatori citati, con margini larghi (7.400 caratteri in
media invece di 2.000):

| | estratto stretto | estratto ampio |
|---|---|---|
| discordi sulle 12 ricontrollate | 12 | **4** |

**Otto discordanze su dodici erano mie.** Esito finale su 30 casi: **25 concordi, 5 discordi**, cioè
un disaccordo del **21%** sulle candidate dove una verifica vera era possibile — e le cinque che
restano sono sostanziali: «l'estratto sostiene solo una parte della sintesi», «il tipo è sbagliato:
è una discussione, non un ordine del giorno trattato».

**La lezione vale più del numero, e va nel rapporto**: se si dà al verificatore **meno contesto di
quanto ne avesse il lettore originale**, non si misura la qualità della lettura, si misura la
propria troncatura. Vale per qualunque pipeline che usi una seconda AI come controllo: la finestra
di evidenza è un parametro del risultato, non un dettaglio implementativo.

Un caso (`N2530`) non è stato restituito dalla seconda passata: resta contato come discorde, che è
la lettura prudente.

L'esito è ora nel database: `build_db.py` legge `t4_esito.csv` e riempie `verifica_seconda_ai`, che
era uno dei campi mai popolati segnalati dal C5. Le righe non verificate restano `non eseguita` —
un campo vuoto sarebbe indistinguibile da una verifica riuscita.

Registro: T4 16.212 + 25.687 token in, 2.904 + 1.991 out, **0,14 €** in tutto.

## 82. L'audit della classe «dubbio» cambia la risposta del rapporto (2026-09-16 10:51Z)

Il pezzo che mancava, e sposta tutto.

**Su 40 candidate della classe `dubbio`, 6 avevano davvero un gemello scritto: il 15,0%**, Wilson
[7,1% ; 29,1%]. Sui 102 accostamenti i veri sono 6, cioè una precisione del **5,9% per
accostamento**. L'ipotesi «5-10%» del primo revisore era giusta sugli accostamenti e bassa sulle
candidate — una candidata con dieci accostamenti resta una candidata.

Il revisore ha lavorato aprendo **il testo integrale** di ognuno dei 102 documenti scritti, non
confrontando sintesi. Ha pagato: **in 3 dei 6 gemelli veri la sintesi della riga scritta racconta un
altro punto dell'ordine del giorno.** È la conferma sul campo dell'asimmetria di unità, misurata da
chi la stava subendo.

**Una scoperta strutturale che vale quanto il numero**: tutti e sei i gemelli veri sono **la
registrazione scritta della stessa seduta** — cinque verbali e una deliberazione. Nessuno è una
fonte scritta indipendente. La classe `dubbio` non nasconde notizie già pubblicate altrove: nasconde,
in un caso su sei o sette, **il verbale della stessa riunione**.

### E un difetto mio che il revisore ha isolato misurando

`stesso_oggetto` **restituisce falso appena i tipi differiscono**, prima ancora di guardare le
parole. Nel suo campione **86 accostamenti su 102 venivano scartati lì**, e con loro quattro dei sei
gemelli veri — due dei quali avrebbero superato la soglia sulle parole (0,714 e 0,600).

La causa è che i due vocabolari descrivono cose diverse: dal lato parlato `tipo` dice **come** il
fatto è emerso (un'audizione, un sopralluogo), dal lato scritto dice **che cosa è il documento**.
Misurato: **416 candidate parlate su 993 (42%)** hanno tipo `audizione`, `sopralluogo` o
`interrogazione`, e dal lato scritto quei tipi contano **tre righe in tutto**. Per il 42% del parlato
la classe «duplicato» era irraggiungibile qualunque cosa dicesse il testo.

Corretto: il tipo resta un filtro fra righe della stessa natura e non si applica fra parlato e
scritto. Effetto: **D da 31 a 76**, S da 486 a 470.

### La risposta, adesso

| | |
|---|---|
| intervallo grezzo | **[46,1% , 92,5%]** |
| con la precisione dei dubbi misurata (15,0%) | **85,6%** |
| agli estremi dell'intervallo di confidenza (7,1% – 29,1%) | fra **79,0%** e **89,2%** |

**L'intervallo si stringe da quarantasei punti a dieci, e la risposta sta vicino al limite
superiore, non a quello inferiore.** Per mesi il numero che avevo in testa era il 48%.

Tre avvertenze da pubblicare insieme al numero, tutte del revisore:
1. è una stima su **40 candidate**: l'intervallo va scritto, non tolto;
2. la precisione misurata è **per difetto** — ha misurato i gemelli *fra gli accostamenti proposti*,
   e i difetti strutturali perdono gemelli **prima** della proposta;
3. il denominatore è gonfiato dai doppioni del parlato già noti.

E la misura sul testo integrale degli atti tira in senso opposto: **144 candidate su 391 (36,8%)**
date per nuove compaiono comunque nel testo di un atto vicino. Le due misure vanno pubblicate
insieme: una dice che i dubbi sono quasi tutti falsi accostamenti, l'altra che i gemelli veri si
nascondono dove il confronto fra righe non guarda.

### Il problema di dato più grave della sessione

**`notizie_candidate.csv` è stato riscritto mentre il revisore lavorava, e 18 delle 40 candidate del
campione hanno cambiato identificativo**: il blocco delle registrazioni è scalato di **+12**. Il caso
peggiore è una **collisione silenziosa**: l'identificativo che lui stava giudicando indicava, dopo la
riscrittura, **un'altra riga esistente** — non un vuoto, che si sarebbe visto.

La causa è mia e la conoscevo a metà: l'identificativo era la **posizione** nella lista
(`enumerate`). Le righe del Report 1 restavano ferme perché stanno in testa, e da lì la mia
convinzione — ripetuta anche nei mandati — che gli identificativi non cambiassero mai. Bastava
aggiungere un lotto di atti, che si inserisce **in mezzo**, per far scorrere tutte le righe delle
registrazioni.

Corretto: gli identificativi stanno ora in un **registro** (`db/registro_id.csv`, 2.874 righe)
legato all'identità della riga — documento e titolo — non alla sua posizione. Verificato eseguendo
il builder due volte di seguito: **zero identificativi cambiati**. Il registro si versiona con i
dati.

Ma il danno di oggi resta: **gli identificativi citati in questo file prima delle 11:00 possono
indicare righe diverse**. Non li riscrivo a mano — sarebbe un altro modo di sbagliare —; chi li
rilegge deve sapere che valgono come riferimenti al momento in cui sono stati scritti, e che il
registro da ora impedisce che succeda di nuovo.

## 83. V3_133–V3_144: due ipotesi smentite contando, e la terza che regge (2026-09-16 10:54Z)

### Che cosa fa conservare le cifre a un verbale: la domanda si chiude

Il lettore ha contato, sui nove verbali del suo lotto, le cifre pronunciate in aula e quelle
sopravvissute nel verbale. **Le prime due spiegazioni sono smentite dai suoi stessi dati**:

| | |
|---|---|
| l'unico verbale **a elenco puntato** | **4 cifre su 4 — 100%** |
| gli otto verbali **in prosa estesa** | da **0%** a 50% |

La prima ipotesi (la prosa estesa conserva, l'elenco no) è quindi **rovesciata**. La seconda (conta
se il verbale registri *chi ha parlato*) non discrimina: tutti e otto i verbali in prosa registrano
chi ha parlato, turno per turno, e fra loro c'è un fattore cinquanta.

**Il predittore che regge è il terzo, ed è una proprietà del documento, non della sua forma:**

> sopravvive la cifra che è **parte dell'atto o della procedura che il verbale ha il compito di
> certificare**; muore la cifra usata come argomento, contesto o colore.

Il verbale al 100% conserva tutto perché tutto era procedura: protocollo, articoli, quattro
favorevoli, due astenuti. Uno conserva l'intera catena decisionale — cinque maggio, quattro giugno,
primo luglio, tre turni, due settimane — e perde lo sfondo tecnico: 58 scuole, il decreto, i venti
giorni. I due a zero sono **audizioni senza decisione**, dove ogni cifra era contesto.

**E un fatto che nessuna delle tre ipotesi prevedeva**: il verbale non si limita a perdere, a volte
**aggiunge e contraddice**. Scrive che gli accessi sono «limitati, **ma in crescita**» quando in aula
la crescita non è mai detta; cambia l'anno di apertura di uno sportello; scrive «due strutture
accessorie» dove l'aula dice «più annessi». Il verbale **ha una fonte propria** — i documenti
d'ufficio — e la usa per correggere il parlato. Il che spiega perché la cifra procedurale sia più
solida nel verbale che nella registrazione.

Tre lettori, tre risposte, e la terza sopravvive al conteggio delle prime due. Vale la pena dirlo nel
rapporto così: la regolarità non l'ha trovata nessuno dei tre da solo.

### La scala di qualità: il vizio è misurato, e non spiega tutto

Il conteggio che avevo chiesto. **21 candidate su 43 (il 49% del lotto, il 64% delle non-`alta`) non
arrivano ad `alta` esclusivamente perché manca la data**: sono compiute e localizzate. **Diciotto di
quelle ventuno sono `solo dal parlato`.**

Se a quelle diciotto si assegnasse `alta`, le `solo dal parlato` passerebbero dal **16,7% al 76,7%**,
**superando** le `anche negli atti` (45,5%). E la ragione per cui le confermate sono datate è che **è
l'atto a datarle**: il lettore dichiara di aver preso le date dal verbale, non dall'audio. Quindi il
requisito «datato» funziona come **un test sull'esistenza dell'atto travestito da test sul fatto**.

**Ma il lettore argomenta contro la propria tesi, ed è la parte che vale di più.** Delle dodici
non-`alta` che restano, dieci lo sono per ragioni proprie: il fatto è annunciato e non compiuto, o il
toponimo è storpiato, o la trascrizione lascia dubbi. Quindi azzerando il vizio della data **un
residuo di divario resterebbe**, perché *il parlato d'aula annuncia più di quanto certifichi*.

Ho aggiunto alla specifica il **settimo emendamento**: ogni candidata non-`alta` dichiara in una
parola perché (`data`, `luogo`, `non compiuto`, `trascrizione`). Non cambia la scala — cambiarla in
corsa è l'errore di §63 — serve a misurarla su tutto il corpus invece che su un lotto.

### Altro

**Un falso positivo della mia misura sulle ripetizioni**: in un item la `quota_ripetuta` è 6% e non è
un guasto del modello — **è la delibera letta due volte da chi presiede**. Chi aggrega quella colonna
senza guardare il testo scambia una prassi d'aula per un difetto. Aggiunto ai mandati.

**Un limite della fonte che non dipende da noi**: la **deissi su schermo condiviso**. Dieci minuti di
commento su una mappa lasciano «qua», «questo pezzo», «fino all'altro carrozziere». Non è la
trascrizione: è che la fonte è **solo audio**.

**Sostituzioni lessicali che rovesciano il senso**, oltre ai toponimi: «per i gatti ci sono 5
articoli, mentre per i gatti ce ne stanno 18» — la prima volta era «cani».

E il rilievo che la soglia esclude i regolamenti cittadini senza luogo: **tre item su dodici**
producono zero o due candidate pur contenendo fatti veri (200.000 cani microchippati a Roma, il
divieto di animali nei circhi scritto e inapplicabile). Il rapporto **sottostima strutturalmente le
sedute dedicate a norme cittadine**, e in questo lotto erano un terzo.

## 84. I rilievi del C5 sistemati, e uno che non si applicava (2026-09-16 11:02Z)

**Il rilievo sull'ordinamento dei lotti non vale sui nostri dati.** Il C5 dice che confrontare `L9`
con `L10` come stringhe fa vincere il nono. Verificato: i lotti sono **a due cifre con lo zero
davanti** (`L01`…`L26`, `B01`…`B40`, `X01`…`X05`), quindi il confronto è corretto. Non ho cambiato
la logica; ho aggiunto un **controllo che si ferma** se un lotto arriva con un nome fuori
convenzione, perché la correttezza dipendeva da un'abitudine e non da una regola.

**`settimana` era calcolata sulla data sbagliata, ed è vero.** Lo schema §1.3 dice «come in
`documenti`», cioè dalla data di **pubblicazione**; il codice usava la data del fatto per le notizie
del Report 1 e la data di seduta per le registrazioni. Corretto. Effetto sulle lacune territoriali:
**nessuno** — due celle vuote prima, due dopo. La deviazione c'era e non distorceva il risultato; se
non l'avessi misurata avrei scritto che l'avevo corretta lasciando credere che cambiasse qualcosa.

**`vicende.confidenza` dipendeva dall'ultima riga processata**: ora una vicenda tenuta insieme da un
duplicato certo resta `alta` anche se dopo arriva un dubbio.

**E il campo che nessuno riempiva, che era il più interessante dei cinque.** Lo schema prevede
`integra_gemello_id` e `campi_integrati` per dire che cosa una riga del Report 2 **aggiunge o
corregge** alla sua gemella del Report 1 — senza, una vista che scarta i duplicati perde esattamente
il contributo che il Report 2 esiste per misurare. Ora sono riempiti:

> **263 righe del Report 2 integrano una gemella del Report 1.** Per campo: `tipo` 242,
> `data_fatto` 191, `municipio` 59, `luoghi` 29, `zona` 20.

**Prima versione dava 270 su 270, e il numero era falso.** Contavo come «correzione» anche due grafie
diverse dello stesso posto in `luoghi`, che è testo libero: misuravo la varietà della scrittura. Per
quel campo ora conta solo il caso «prima vuoto, ora pieno», e le integrazioni di `luoghi` scendono da
270 a 29. Il numero da pubblicare è **263**, e il campo che gli atti e le registrazioni aggiungono
più spesso non è il luogo: è **il tipo dell'atto e la data del fatto**.

Restano aperti del C5: i nomi delle colonne nello schema (`titolo` contro `titolo_anonimizzato`),
che vanno allineati prima della consegna; la cardinalità di `gemello_id`, che ammette un solo gemello
mentre le coppie stanno già in `coppie_parlato_scritto.csv`; e la tabella degli accostamenti che il
C5 vorrebbe dentro le cinque tabelle.

## 85. La registrazione che il CDN non serve per intero (2026-09-16 11:06Z)

Gli scaricamenti sono finiti (pozza libera), il driver ASR era morto su un errore dell'API («Audio
file might be corrupted or unsupported») e l'ho riavviato con il codice corretto: restano 12 item su
318, dieci con i segmenti completi e uno con il mono pronto.

Il dodicesimo è `41e7b841`, quello di §65. **Riprovato oggi, a distanza di ore: il segmento 58 è
ancora vuoto.** Non è un intoppo di rete, è un difetto della fonte — una registrazione pubblicata di
cui il CDN non serve l'ultimo pezzo.

Scartare una seduta pubblica per una coda di dieci secondi sarebbe peggio che tenerla dichiarando la
lacuna. `video/recupera_segmento_mancante.py` ricostruisce la playlist locale con i **58 segmenti su
59** che esistono. Niente di aggirato: si usa quello che il CDN ha servito. Le IV non si inventano —
ogni segmento ha IV uguale all'MD5 del proprio indice, verificato sui segmenti di un'altra
registrazione dove `cfcd2084…` è MD5("0").

**E il programma, alla prima esecuzione, ha dichiarato «nessuna lacuna».** Perché scartavo i file da
zero byte prima di contare: il segmento mancante spariva dalla lista, l'ultimo diventava il 57, e
non c'era più nessun buco da vedere. Un programma scritto **apposta** per dichiarare una lacuna che
non riusciva a vederla — la stessa forma di difetto che oggi ho trovato nel conteggio dei processi,
nel log del driver e nella prima misura del T4. Corretto: i segmenti vuoti si contano come mancanti,
e ora dice *«1 segmento, circa 10 secondi, in coda»*.

La regola che ne ricavo, e che vale più della correzione: **quando scrivo un programma per misurare
una mancanza, la prima cosa da provare è che la mancanza la veda**. Filtrare i dati difettosi
all'ingresso è il modo più naturale di renderli invisibili proprio alla misura che li cerca.

## 86. La causa vera delle registrazioni perse: `SystemExit` (2026-09-16 11:08Z)

Riavviato il driver, è morto di nuovo in pochi minuti. Stavolta ho guardato **perché**, invece di
riavviarlo e basta.

`rtv_transcribe.py`, sulla risposta di errore dell'API, faceva:

```python
raise SystemExit('trascrizione fallita su %s: HTTP %d %s' % ...)
```

**`SystemExit` non deriva da `Exception`, deriva da `BaseException`**: passa attraverso l'
`except Exception` del driver come se non ci fosse. Quindi **un solo file audio rifiutato dall'API
uccideva il programma che ne stava trascrivendo trecento**, lasciando a metà l'item in lavorazione.

È la causa vera delle registrazioni perse di §65. Lì avevo trovato il secondo anello — i segmenti
cancellati prima della trascrizione, che rendevano l'item irripetibile — e l'avevo corretto
credendo di aver chiuso il caso. Il primo anello era questo, e in §65 avevo persino scritto che il
driver «logga l'errore e continua»: lo credevo perché il codice ha un `except`, non perché avessi
visto un errore seguito da una ripresa. **Un `except` che non cattura è indistinguibile da un
`except` che funziona, finché non guardi che cosa succede dopo.**

Corretto: `RuntimeError` al posto di `SystemExit`. E il driver ora **mette da parte un item che
fallisce due volte** (`rtv_item_rinunciati.txt`) invece di ricominciare sempre da lui: senza, la coda
si incastrava sul primo file corrotto e gli altri non arrivavano mai.

Il file che lo uccideva è `e7f9ea9a`, che l'API rifiuta come «Audio file might be corrupted or
unsupported» — un audio davvero difettoso, che ora viene dichiarato invece di fermare tutto.

**Tre difetti diversi, una sola forma.** Oggi ho trovato: un conteggio di processi che non vedeva il
processo, un programma per dichiarare le lacune che scartava le lacune prima di contarle, una prima
misura T4 che misurava la mia finestra, e ora un gestore di errori che non gestiva. Tutti e quattro
si comportano bene finché non succede la cosa che dovrebbero intercettare. **La prova di un
meccanismo di sicurezza non è che il programma funzioni: è che fallisca come previsto quando lo si
rompe apposta.** Nessuno di questi quattro era mai stato messo alla prova con un guasto vero.

## 87. Il secondo giro di audit è pronto, e c’è un pezzo nuovo da controllare (2026-09-16 11:11Z)

Il numero principale del rapporto — **85,6%** — poggia su **quaranta casi giudicati da un solo
revisore**. È poco per la cosa su cui si regge tutto, e il revisore stesso l'ha scritto. Ho preparato
il secondo giro: `campione_dedup.py` accetta un seme da riga di comando, **esclude le candidate già
giudicate** (109) e ne estrae altre quaranta, disgiunte dalle prime.

**E c'è un pezzo che nessuno ha ancora guardato, creato da una mia correzione di oggi.** Togliendo il
filtro sul tipo (§82) gli accostamenti forti sono passati da 31 a **76**: quarantacinque
classificazioni «duplicato» nuove, mai verificate da nessuno. La precisione misurata era **52%** su
un campione estratto *prima* di quella correzione. Se i quarantacinque nuovi fossero peggiori, la
classe D sarebbe gonfia e la novità sottostimata — cioè un errore nella **direzione opposta** a
quello che l'audit dei dubbi ha corretto. Il secondo campione ne contiene la sezione di precisione
su tutti e 77.

**Un difetto del generatore, trovato usandolo.** Scriveva sempre su `campione_dedup.md`, quindi il
secondo giro **cancellava il file che il primo revisore aveva davanti**. Il seme da solo non lo
ricostruisce, perché il database intanto è cambiato — e oggi è cambiato parecchio. Ora il nome porta
il seme.

**E il criterio di giudizio è stato corretto** (`report2/CRITERIO_AUDIT.md`): era asimmetrico — «la
seconda non aggiunge niente alla prima» — ma applicato a coppie che non hanno un ordine, e il
giudizio si rovesciava a seconda di quale riga si chiamasse seconda. Ora si guarda in **tutte e due
le direzioni**: se una delle due porta un fatto che l'altra non ha, non sono lo stesso fatto. Il
difetto si è visto solo perché il revisore ha **dichiarato la convenzione che aveva scelto** invece
di applicarla in silenzio.

Stato: 154 registrazioni V3 lette, 310 trascritte su 318, driver vivo, nessun item messo da parte.

## 88. Drive: ho guardato e ho deciso di non caricare adesso (2026-09-16 11:17Z)

Controllata la cartella Drive `Fonti 2026-06`: le tre parti di A1 sono lì con gli identificativi che
avevo annotato, caricate stamattina alle 03:15–03:25. Rigenerato il file compatto: **162.926 byte
contro i 161.147 delle tre parti**, quindi il contenuto è davvero cambiato — le colonne di oggi
(`settimana` ricalcolata, i campi di integrazione) e le correzioni.

**Non le sostituisco adesso.** Il database non è fermo: due lotti stanno ancora scrivendo, e oggi ho
cambiato il builder cinque volte. Caricare ora vorrebbe dire rifare tutto alla consegna, ed è
esattamente la giostra per cui in §46 avevo sospeso i caricamenti. Sostituisco e cestino le vecchie
**una volta sola**, a lettura finita.

Il rischio che resta e che va detto all'owner alla consegna: **su Drive ci sono tre file che
sembrano correnti e non lo sono**. Non li tolgo prima di avere il sostituto pronto — una cartella con
un buco è peggio di una con un file vecchio — ma non devono arrivare al 20 settembre così.

## 89. L'indice delle evidenze: il compito è pronto, non l'ho fatto a mano (2026-09-16 11:17Z)

Il rilievo **bloccante** del C4 §6.2: i casi raccontati nei §3 e §4 non portano un identificativo, e
senza riferimento valgono come aneddoti.

Ho provato a compilarlo da solo cercando in STATO e **non si può**: quando ho riassunto gli hand-back
dei lettori ho tenuto i fatti e lasciato cadere gli identificativi. Sono nei log dei lettori e nei
JSON, non qui. Fare l'indice significa tornare a quelle fonti, ed è lavoro di lettura, non di
memoria — se lo facessi «ricordando» produrrei riferimenti plausibili e sbagliati, che è la cosa
peggiore che possa finire in un indice delle evidenze.

`report2/COMPITO_INDICE_EVIDENZE.md` estrae le **dieci affermazioni** dal rapporto, dice dove
cercare, e — la parte che conta — stabilisce che **un'affermazione che nessuno ritrova va tolta dal
rapporto**, e che questo è un esito utile quanto l'altro. Assegnato al primo lettore libero.

Le dieci: *negli atti passa solo chi vince*; *il verbale c'è ma è vuoto*; *la parte più informativa è
quella che per procedura non si registra*; *il verbale si scrive in diretta*; *a volte il verbale
racconta una seduta diversa da quella avvenuta*; *un atto che dispone il contrario di quanto
deciso*; *qualche volta è la registrazione a correggere l'atto*; *come il residuo viene prodotto*;
*quale cifra sopravvive in un verbale*; *che cosa il Report 2 aggiunge al Report 1*.

## 90. V3_145–V3_168: la regola sulle cifre è confermata due volte, e il parlato sbaglia (2026-09-16 11:24Z)

Due lotti, ventiquattro registrazioni, e per la prima volta due misure indipendenti che **confermano**
invece di smentire.

### Le cifre nei verbali: contate due volte, stessa risposta

| lotto | cifre pronunciate | sopravvissute | controesempi |
|---|---|---|---|
| V3_145–156 | 72 | 29 (40%) | **0** |
| V3_157–168 | ~80 | 47 (59%) | 4 |

Delle morte, tutte meno quattro sono **argomento, contesto o colore**: 137 aziende e 7.000 addetti,
8 milioni nel 2016, il 50% di differenziata, 9″99 sui cento metri, il Giro d'Italia 2018.

**Il caso che chiude la questione**: un assessore legge dieci statistiche sull'arresto cardiaco —
60.000 casi l'anno, 58%, 7,5% europeo — dicendo «tutto questo è presente nell'atto che stiamo
discutendo». Nel documento **non ce n'è nessuna**. Sopravvivono tutte e sole le cifre che *sono* la
norma: 250 mq, 350 dispositivi, 16.500 esercizi, 31 dicembre 2026.

La formulazione finale, raffinata da entrambi i lettori: **sopravvive la cifra di cui quel verbale è
il documento probatorio**. Le quattro eccezioni del secondo lotto sono cifre procedurali **di un
altro organo** o di un passaggio futuro — cioè confermano la regola specificandola.

### E il parlato sbaglia, non solo il verbale

Il contrappeso alla tesi del rapporto, e viene dai lettori:

- una consigliera **annuncia il proprio voto contrario**; nel verbale i contrari sono due e lei non
  c'è, perché aveva lasciato la seduta. **Chi si fidasse del solo parlato sbaglierebbe il conteggio.**
- il verbale corregge l'oratore **contro la sua stessa voce**: «oltre sei mesi dalla chiusura»
  diventa «a più di cinque mesi», e cinque è il numero giusto;
- il verbale porta l'importo esatto di un debito, **17.182,05**, dove in aula si sentono 21.000,
  17.000, 2.182, 1.224,30;
- gli orari di entrata e uscita al minuto **in registrazione non esistono**: nessuno li annuncia,
  vengono dal foglio presenze.

E una volta è lo scritto a sbagliare e la voce ad avere ragione: una convocazione elenca un «verbale
n. 20 del 14/06/2026», data impossibile; il parlato dice 14/05 e il verbale lo conferma.

**Sulle trascrizioni a pagamento i numeri pronunciati non sono affidabili**: «250.000 metri quadrati»
per 250, «venerdì scorso 22 giugno» per il 12. Per uno studio che conta cifre è il difetto peggiore,
e la conseguenza operativa è netta: **quando il verbale c'è, la cifra si prende dal verbale**.

### Il foglio di riscontro: 26%, non 15%

Il secondo lettore ha dato il numero esatto: **685 testi su 2.668 (il 26%) non hanno una riga nel
foglio**. Il primo ha misurato l'effetto: otto item su dodici hanno trovato un atto fuori foglio, e
con il solo foglio avrebbe scritto `solo dal parlato` su **undici candidate che invece stanno
scritte**.

### Due difetti nuovi, e uno riguarda una persona

**La duplicazione corrompe le cifre anche sotto la soglia.** Lo stesso passaggio trascritto due volte
dà numeri **diversi**: «non sono 113. 5.14, 235, 64» contro «non sono 116. 5145, 235, 64». Stesso
audio, due trascrizioni, cifre discordi. Dove il modello cicla le quantità vanno considerate perse
**anche a `quota_ripetuta` bassa**: è un difetto che quella colonna non misura.

**E una registrazione pubblicata prosegue per tredici minuti dopo la chiusura dei lavori**, con
parlato privato di natura personale catturato a microfono aperto. Il lettore non ha fatto entrare
nulla nei nostri file, nemmeno anonimizzato, e nel log non ha riprodotto né contenuto né
identificativi: **dalla nostra parte è chiuso**. Ma quel materiale è ancora online, pubblicato
dall'amministrazione, e riguarda persone che non sapevano di essere registrate. **Aperta la D7**: la
segnalazione, se si fa, la fa l'owner — va mandata da chi ha un nome e un indirizzo, non da una
sessione automatica.

### Una divergenza fra letture che non credo isolata

La risoluzione sulla titolazione di un parco è `notizia_candidata = no` per chi ha letto l'atto e
qualità `alta` per chi ha ascoltato la seduta. Chi leggeva il dispositivo ha visto una
regolarizzazione; chi ascoltava ha sentito che un parco **intitolato e inaugurato con una targa non
era mai stato intitolato**, e che gli uffici l'avevano messo per iscritto a novembre 2025. È la
differenza fra leggere il dispositivo e leggere la premessa.

### Il limite che il primo lettore nomina meglio di come l'avevo scritto io

«Quando il verbale della seduta stessa esiste ed è *con sintesi*, tutto il detto sta scritto e la
colonna della novità collassa»: 4 `solo dal parlato` su 11 dove il verbale c'è, 20 su 31 dove manca.
**Così la colonna misura la verbalizzazione, non la novità territoriale.** È la stessa cosa che il
numero principale dice dall'alto, vista dal basso di un lotto.

## 91. Trascrizione finita: 318 su 318, e il corpus è più grande di come lo contavo (2026-09-16 11:33Z)

**L'ultimo item non era corrotto: era tagliato male da me.** Il driver aveva rinunciato a `e7f9ea9a`
perché l'API rispondeva «Audio file might be corrupted or unsupported». L'mp3 invece è sano:
trentanove minuti, 9,6 MB, stream valido. Il difetto stava nei tagli: `tagli()` metteva l'ultimo
punto esattamente sulla durata del file, e quando il taglio precedente cadeva a un soffio dalla fine
usciva un pezzo da **0,1 secondi e 467 byte**. Quello l'API lo rifiuta — e un file da 467 byte
faceva fallire la trascrizione di una registrazione da quaranta minuti perfettamente in ordine.

Corretto: una coda più corta di mezzo minuto si attacca al pezzo precedente. Recuperato l'item e
tolto dalla lista dei rinunciati. **318 registrazioni su 318 trascritte**, $ 35,76 (32,90 €).

Vale la pena notare la forma, perché è la quinta volta oggi: il messaggio d'errore diceva «file
corrotto» e il file era sano; a essere sbagliato era **quello che gli mandavo**. Un errore che
descrive il dato invece di descrivere la richiesta manda a cercare dalla parte sbagliata.

### Il corpus RomaTV è di 400 registrazioni, non 318

Rigenerato il manifest: **400 righe**, cioè 318 a pagamento (trascritte da noi) **più 82 della
piattaforma** (trascritte dalla fonte). Non si sovrappongono: ogni registrazione ha una sola origine.
Delle 400, **381 sono dentro la finestra 8–28 giugno** e 19 fuori.

Quindi il corpus del Report 2 è **381 RomaTV + 97 YouTube = 478 registrazioni**, non 415 come
scrivevo. Ne sono lette 265. Ne restano **213**, cioè diciotto lotti: con due lettori in parallelo
sono cinque o sei ore, e alla consegna mancano quattro giorni. Regge, ma il margine non è quello che
credevo.

Le 19 fuori finestra **non spariscono in silenzio**: vanno in
`manifest_video_rtv_fuori_finestra.csv`, con i loro identificativi, così chi guarda sa che esistono e
perché non sono state lette.

### E nel rigenerare il manifest ho rifatto lo stesso errore di stamattina

Alla seconda esecuzione il programma ha assegnato **identificativi nuovi a 19 registrazioni che ne
avevano già uno**: rileggeva gli id dal solo manifest in finestra, e le righe spostate nel file
«fuori finestra» risultavano sconosciute. È **lo stesso difetto di posizione** che il registro degli
id aveva appena tolto dal database, ricomparso in un altro programma poche ore dopo. Corretto — gli
id si rileggono da tutti e due i file — e verificato eseguendo due volte di seguito: zero id nuovi.

Aver capito un difetto in un posto non lo toglie dagli altri posti dove ho scritto la stessa logica.

## 92. La notiziabilità di un atto dipende da chi lo legge, e il fattore è due (2026-09-16 11:36Z)

Rinfrescando i numeri del rapporto ho controllato la quota di atti notiziabili e ho trovato una cosa
che non stavo cercando.

| | atti | notiziabili |
|---|---|---|
| i 1.983 atti della finestra (lotti B) | 1.983 | 544 — **27,4%** |
| i 161 atti fuori finestra (lotti X) | 161 | 84 — **52,2%** |

Poteva essere il materiale, visto che i lotti X sono quasi tutti convocazioni. **Non lo è**:
confrontando **lo stesso tipo di atto**, le convocazioni,

> lotti B: **21,0%** notiziabili su 509 · lotti X: **44,2%** su 129.

Stesso tipo di documento, stessa regola scritta, **il doppio di notizie**.

**La causa più probabile è mia.** Ai lettori dei lotti X ho spiegato *perché* il lotto esisteva e ho
chiesto nel mandato «quali fatti territoriali contengono». Ai lettori dei lotti B avevo dato la sola
specifica. Non ho cambiato la soglia: ho cambiato **che cosa il lettore stava cercando**, e la resa
è raddoppiata.

Va nel rapporto, perché tocca un numero che ci sta dentro: **il 27,4% non è una proprietà degli
atti**, è una proprietà della coppia atto-lettore. Chi rifacesse questo studio con un mandato scritto
un po' diversamente troverebbe il doppio delle notizie negli stessi documenti — e non saprebbe di
averlo fatto, se non confrontasse due lotti come qui.

È anche un limite di tutte le percentuali di notiziabilità che il Report 2 pubblica, comprese quelle
per tipo di atto, e va detto **accanto a quei numeri** e non in una nota in fondo.

Nota metodologica per la consegna: il rapporto dice «1.983 atti letti». Sono diventati **2.144** —
1.983 nella finestra più 161 fuori, letti per chiudere il buco delle convocazioni. Le due cifre
vanno tenute distinte: 1.983 è **il perimetro del confronto**, 2.144 è **quanto abbiamo letto**.

## 93. Un programma che dice quali numeri del rapporto sono vecchi (2026-09-16 11:40Z)

Rinfrescando i numeri ne ho trovati **quattro vecchi in un colpo solo** — 19,5%, 35,5%, 85,6%,
32,1% — dopo averli già «rinfrescati» due volte oggi. Cercarli a occhio in un testo di quattrocento
righe non funziona, e non funzionerà nemmeno il 20 settembre a mezzanotte.

`report2/verifica_numeri_rapporto.py` ricalcola dal database i nove valori che il rapporto cita e
dice, per ciascuno, se il testo li contiene. **Non corregge**: dire a un programma di riscrivere il
rapporto è il modo di perdere il controllo di che cosa afferma. Stampa e basta; correggo io.

Ha anche un limite che dichiara da sé: se un numero non compare, il programma non sa distinguere fra
«il rapporto è vecchio» e «quel numero il rapporto non lo cita». Lo dice invece di fingere di saperlo.

Tutti e nove tornano, ai valori di adesso: 1.081 candidate dal parlato, 1.983 atti in finestra, 544
candidate da quegli atti, 265 registrazioni lette, 284 integrazioni, intervallo [45,1% , 92,2%],
qualità alta 53,3% contro 19,0%.

### I numeri di oggi, aggiornati

| | |
|---|---|
| S / U / D | 487 / 510 / 84 su 1.081 |
| intervallo grezzo | [45,1% , 92,2%] |
| con la precisione dei dubbi (15,0%) | **85,2%**, fra 78,5% e 88,9% |
| scartando i toponimi incerti | 31,0% |
| divario di qualità dentro il parlato | 53,3% contro 19,0% |

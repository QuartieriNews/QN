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

**Materiale per la deduplicazione**: il lotto A1 ha già trovato tre coppie di item che
raccontano lo stesso fatto (A1_280/A1_281, A1_061/A1_209, A1_106/A1_107). I lettori non li
uniscono e non ne saltano nessuno: li schedano entrambi annotando il gemello, perché la
deduplicazione è un passo successivo che ha bisogno di vedere tutte e due le righe.

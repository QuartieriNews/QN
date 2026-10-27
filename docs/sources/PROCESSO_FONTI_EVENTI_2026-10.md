# Fonti degli eventi: tutto il processo dal 20 al 27 ottobre 2026

**La richiesta dell'owner (27 ottobre).** «Vorrei che mi passassi un documento con tutto quello che hai fatto per arrivare a
questo risultato. Vorrei che mi evidenziassi dove sono le informazioni che hai usato o non usato di Apify e tutte le scelte. Se
sono presenti in qualche report GitHub dammi il link. Vorrei passare tutto il processo a Codex e dirgli di rifarlo anche lui così
da avere qualche dato in più di supporto.»

Questo documento ricostruisce il lavoro passo per passo.
- **Fonti della ricostruzione:**
  - il registro completo della sessione, dal 20 ottobre;
  - i rapporti e i commit del ramo;
  - l'elenco dei run letto dall'API di Apify il 27 ottobre.
- **Un limite della ricostruzione.** Il registro condensato usato per la prima stesura non mostrava i messaggi dell'owner arrivati
  mentre il builder lavorava: dodici, fra cui le autorizzazioni di spesa. Le tre verifiche indipendenti li hanno ritrovati nel
  registro completo e le attribuzioni sono state corrette; dove resta un dubbio, vale il registro completo della sessione.
- **Per Codex** c'è un mandato a parte, senza i nostri risultati: `docs/sources/REPLICA_CODEX_FONTI_EVENTI.md`. Il pacchetto con
  i dati di partenza sta fuori dal repository (§1).
- **Che cosa non c'è qui:** titoli di eventi, testi delle fonti, email o telefoni (DEC-102, DEC-104, DEC-109; DEC-022 sta sul ramo `wiki/giugno-2026`). Quelle righe stanno
  nei fogli consegnati e nel pacchetto.

## 1. Dove sta ogni cosa

| Che cosa | Dove |
|---|---|
| Ramo e pull request | ramo [`claude/ecstatic-shannon-mjzxvq`](https://github.com/QuartieriNews/QN/tree/claude/ecstatic-shannon-mjzxvq), pull request [QuartieriNews/QN#15](https://github.com/QuartieriNews/QN/pull/15); commit e revisioni nelle appendici B e C |
| Rapporto di stato, sezione per sezione | [`docs/sources/FONTI_EVENTI_STATO_2026-10-24.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/FONTI_EVENTI_STATO_2026-10-24.md) (§1-§1 terdecies, §2-§7) |
| Altri rapporti | [`FLUSSO_EVENTI_A_Z.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/FLUSSO_EVENTI_A_Z.md), [`NOTIZIE_DAI_DATI_2026-10-26.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/NOTIZIE_DAI_DATI_2026-10-26.md), [`TIMELINE_BREVI_2026-10-26.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/TIMELINE_BREVI_2026-10-26.md), [`QUALITA_EVENTI_2026-10-26.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/QUALITA_EVENTI_2026-10-26.md) |
| Wiki delle fonti eventi | [`docs/wiki/fonti-eventi/`](https://github.com/QuartieriNews/QN/tree/claude/ecstatic-shannon-mjzxvq/docs/wiki/fonti-eventi): schedario `fonti_eventi.json`, pagine per Municipio e per pagina QN, censimento, promotori, fusioni proposte |
| Decisioni aperte scritte dal builder | [`DEC-023`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/decisions/DEC-023-event-sources-wiki.md), [`DEC-024`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/decisions/DEC-024-census-facebook-pages-into-registry.md), [`DEC-025`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/decisions/DEC-025-source-precedence-for-duplicate-events.md), [`DEC-026`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/decisions/DEC-026-roma-today-position.md) |
| Strumenti con test | `tools/fonti/leggi_eventi_siti.py` (T-LS), `tools/fonti/leggi_culture_roma.py` (T-CR), `tools/fonti/valida_eventi.py` (T-VE), `tools/wiki/build_fonti_eventi.py` (T-FE); test in `tests/` |
| Script di lavoro, passo per passo | [`tools/fonti/lavoro-2026-10/`](https://github.com/QuartieriNews/QN/tree/claude/ecstatic-shannon-mjzxvq/tools/fonti/lavoro-2026-10): il `README.md` ha la tabella passo → script → ingresso e uscita. Sono copie di sicurezza, senza test, con i percorsi dell'area di lavoro scritti dentro |
| Fogli consegnati all'owner | 26 fogli Excel, più `culture_luoghi.json` e l'archivio `immagini_eventi.zip`, scritti nella cartella dei file consegnati della sessione (`/mnt/user-data/outputs`) ed elencati nel §7. Il 27 ottobre una ricerca su Drive di sei di questi nomi ha trovato solo `eventi_dai_post_facebook.xlsx`, caricato il 25 ottobre; gli altri non sono stati cercati uno per uno. Tutti sono anche nel pacchetto |
| Dati di partenza dell'owner | foglio Drive «eventi /» (584 URL di eventi Facebook, 324 di Roma Today); fogli Drive del 13 ottobre «Eventi letti alla fonte 13-31 ottobre» e «Registro fonti eventi»; file allegati in chat: 1.169 pagine di associazioni, 6.247 enti RUNTS; le 220 pagine verificate, incollate come testo nel messaggio del 24 ottobre alle 19:09 |
| Dati grezzi Apify | dataset sull'account dell'organizzazione, conservati 31 giorni: fino a circa il 24 novembre 2026; id nell'appendice A. Copia completa nel pacchetto |
| Pacchetto per la replica | `pacchetto_replica_fonti_eventi_2026-10.zip`, consegnato all'owner come file, **riservato** (dati personali e testi delle fonti): dataset Apify, input di ogni run, file dell'owner, letture dei siti, passi intermedi, pagina prima e dopo l'audit, fogli consegnati, listini Apify letti il 27 ottobre. I dati presi da Roma Today sono stati tolti (`PULIZIA_ROMA_TODAY.json`). Il suo `LEGGIMI.md` descrive ogni cartella |
| Pagina «Eventi dei quartieri» | pagina privata su claude.ai: https://claude.ai/artifact/1rJVeiqCg7xY1qKaXn1H52 (versione del 26 ottobre) |

## 2. Il risultato in breve

| Voce | Valore |
|---|---|
| Eventi in corso o futuri raccolti al 25 ottobre (pagina corretta il 26) | 2.489; al 26 ottobre la pagina ne mostra 2.183, perché nasconde quelli finiti |
| Pagine QN con almeno un evento / con almeno 10 | 84 / 49 su 89 |
| Pagine QN a zero | 5: La Rustica, La Storta, Lunghezza, Marcigliana, Vitinia |
| Fonti nello schedario della wiki | 5.238 voci; il registro v6, che ne è uno degli ingressi, ha 1.759 righe (1.620 del v5 e 139 promotori candidati) |
| Promotori degli eventi | 1.246, tutti con una regola su dove leggere i prossimi eventi |
| Costo mensile della lettura con la regola | 15,49 $ leggendo ogni giorno, 13,19 $ ogni settimana (tutto da Facebook: 33,94 e 26,17 $) |
| Spesa Apify del lavoro | 177,50 $ sull'account dell'organizzazione (56 run); circa 12,3 $ sull'account del connettore, dentro un consumo del ciclo di 21,01 $ che comprende run avviati fuori da questa sessione (§4) |
| Qualità della pagina (campione di 155 eventi) | errori gravi dal 28% al 22% dopo le correzioni automatiche; gli annunci estratti dai post restano al 43% |
| Lavori collegati | 402 notizie confermate dai dati già raccolti; una breve ogni 2 ore per quartiere non c'è (§3, 26 ottobre) |

## 3. Il processo, giorno per giorno

Ogni riga dice che cosa ha chiesto l'owner, che cosa è stato fatto e dove sta il risultato. I numeri sono quelli del momento: molti
sono cambiati nei passi successivi.

### 20 e 23 ottobre: il foglio unificato degli eventi di ottobre

| Quando | Passo | Che cosa è stato fatto | Dove |
|---|---|---|---|
| 20 ott | Richiesta: dettagli dei 584 eventi Facebook con Apify | Bloccato: il connettore Apify non era autenticato e gli allegati non erano arrivati. Lo stesso giorno, fuori da questa sessione, sull'account del connettore sono partiti 8 run di apify/facebook-events-scraper (7,95 $) e il run Cheerio su culture.roma.it (§4) | — |
| 23 ott 11:27 | Run sui 584 URL | Gli URL sono stati trovati nel foglio Drive «eventi /». Il run `tOKJy9yqjegtpFbPV` (apify/facebook-events-scraper, account del connettore) ha dato 567 eventi; 17 URL sono falliti (13 bloccati, 4 errori HTTP 400) | `facebook_eventi.xlsx`, `eventi_scraping.xlsx` |
| 23 ott 11:46 | Foglio unico | Unite quattro fonti: Facebook (567); culture.roma.it, dal run Cheerio del 20 ottobre già sull'account, 708 eventi con fine dal 1° ottobre; fonti locali (foglio Drive del 13 ottobre, 358 eventi); Roma Today (324 URL). Roma Today non è stato letto con Apify: il suo robots.txt vieta scraping e uso per l'AI | `eventi_unico.xlsx` |
| 23 ott 13:16 | Roma Today, su richiesta dell'owner | Due passate dal container sulle 324 schede, una richiesta ogni 1,5 secondi: promotore e link ufficiale, poi lettura della sorgente. È la lettura una tantum autorizzata; la posizione su Roma Today resta aperta in DEC-026 | `eventi_unico.xlsx`, foglio «Romatoday → sorgente» |
| 23 ott 13:45-15:24 | Geografia | Metodo 1: coordinate o indirizzo geocodificato con Nominatim, poligoni ufficiali dei Municipi, quartiere da OpenStreetMap. Metodo 2: suddivisioni toponomastiche ufficiali e toponimo del gazetteer più vicino nello stesso Municipio. Più la rintracciabilità alla fonte diretta | `eventi_unico.xlsx`; script `geocode.py`, `geo_assign.py`, `metodo2.py`, `rintracciabilita.py` |
| 23 ott 15:19 | Doppioni | 97 gruppi, 127 righe in eccesso su 1.957; nessuna riga cancellata | foglio «Doppioni»; `doppioni.py` |
| 23 ott 15:53-16:11 | Wiki delle fonti eventi | Builder dello schedario con test; poi tolto il filtro sui nomi di persona (DEC-105): resta escluso solo l'URL di un profilo personale | commit `0dd6de8`, `a86149c` |

### 24 ottobre: censimenti e nuove fonti

| Quando | Passo | Che cosa è stato fatto | Dove |
|---|---|---|---|
| 12:06 | Situazione | Su 1.957 righe: 792 eventi futuri con pagina; 23 pagine con almeno 10 eventi, 27 a zero | messaggio all'owner; FONTI_EVENTI_STATO §1 |
| 12:23-13:19 | Censimento delle 1.169 pagine di associazioni (file dell'owner) | Prima prova sull'account del connettore, fermata dal suo tetto mensile (19 $, superato a 21,01 $); poi token dell'organizzazione dato dall'owner. Lette pagine, eventi futuri e post degli ultimi 6 mesi; letti i siti delle pagine; verdetto per pagina | `associazioni_fonti.xlsx`; wiki `censimento-pagine.md`; commit `a644165`, `2530db8`; §2 |
| 13:36-13:37 | Autonomia per 3 ore | L'owner la chiede con una sola condizione: poter tornare indietro. Il builder conferma con le sue garanzie (commit separati, niente merge né produzione, testi delle fonti fuori dal repository, spesa di pochi dollari); un minuto dopo l'owner autorizza l'uso pieno di Apify, «hai 200 dollari di credito» | — |
| 13:38-15:26 | Ricerca uno a uno dei 176 eventi senza fonte | Prima con Google (176 ricerche), poi rifatta nell'ordine giusto: prima il sito del luogo già nello schedario, poi il web. 30 fonti dirette trovate | `eventi_senza_fonte_ricerca.xlsx`; §3; commit `97ea556`, `4797d8d` |
| 13:40 | Scoperta di organizzatori per parole chiave | 109 ricerche con unseenuser/fb-events e 30 con apify/facebook-events-scraper (lo stesso meccanismo del workflow n8n): nessun organizzatore nuovo con almeno 2 eventi a Roma | `facebook_scoperta_organizzatori.xlsx`; §5; DEC-024; commit `d08f873` |
| 13:45 | Lettore settimanale dei siti | `leggi_eventi_siti.py` con test; prima lettura: 675 siti letti, 12 con eventi schema.org | §4 bis; commit `2bdead3`, `d336977` |
| 13:46-13:49 | Decisioni aperte e riga principale | DEC-024 (censimento nel registro) e DEC-025 (precedenza fra fonti nei doppioni), con la colonna `riga_principale_proposta` | commit `75fd77a` |
| 14:06 | culture.roma.it per differenza | `leggi_culture_roma.py` sull'API pubblica WordPress, senza Apify | §4 ter; commit `438418c`, `62cc43a`, `509349a` |
| 14:51-15:25 | Fonti mirate per le 58 pagine deboli | 423 ricerche Google per tipo e quartiere, elenchi pubblici (scuole, mercati, centri anziani, biblioteche): 463 candidate | `fonti_mirate_pagine_deboli.xlsx`, registro v2; §1 bis; commit `d3a9958` |
| 15:26-15:29 | Workflow n8n, DEC-023, DEC-026, script versionati | Il workflow Facebook di produzione è inattivo nell'export e cerca «Italy Roma»; sull'account dell'organizzazione non ci sono schedulazioni | §1; commit `8bc2b09`, `5e63c78` |
| 16:57-20:00 | Censimento RUNTS (6.247 enti, file dell'owner) | Ricerca Google per nome e poi per codice fiscale; siti verificati (codice fiscale in home, o dominio e nome); pagine Facebook, eventi futuri e post; email ufficiali. Tetto di spesa portato a 100 $ dall'owner, poi a 150 $ | `enti_terzo_settore_fonti.xlsx`; §1 ter; commit `084cdb2`, `0c05930`, `05874ea` |
| 19:09 | 220 pagine verificate dall'owner | Tutte già nel registro: ora con decisione «tenere» | registro v3 |
| 19:41-19:50 | Simulazione, flusso A-Z, prima pagina HTML | Simulazione «un evento per ente»; proposta di flusso con cadenze per livello; prima pagina «Eventi dei quartieri» (1.402 eventi) | §1 quater; `FLUSSO_EVENTI_A_Z.md` (commit `1965c62`) |
| 20:14 | Ricerca «evento / eventi / festa + quartiere» | 288 ricerche, 1.380 fonti distinte, 129 candidate | `fonti_ricerca_quartieri.xlsx`, registro v4; §1 quinquies; commit `1a3997d` |

### 25 ottobre: eventi nei post, abitanti, lista supplementare, promotori

| Quando | Passo | Che cosa è stato fatto | Dove |
|---|---|---|---|
| 10:20 | Comitato Acilia Nord | I suoi eventi stanno solo nel testo dei post: il sistema contava solo eventi strutturati | messaggio all'owner |
| 10:24-10:50 | Eventi dentro i post Facebook | Estrattore a regole (data anche relativa, ora, luogo, titolo, ricorrenze) sui post già letti e sulle 220 pagine dell'owner; secondo giro su 662 pagine salvate e mai lette (12 $ approvati dall'owner) | `eventi_dai_post_facebook.xlsx`; §1 sexies; commit `58dde9e`, `9132fb3` |
| 11:33-11:42 | Eventi contro abitanti | Griglia statistica di Roma Capitale e zone urbanistiche ufficiali; la stessa geografia per gli eventi; 85 eventi fuori Roma tolti | `eventi_per_abitanti.xlsx`; §1 septies; commit `cf197be` |
| 12:00-12:31 | Lista supplementare per le 41 pagine sotto la mediana | OpenStreetMap, annuario della Diocesi (fermato dal captcha), Google per toponimo, Google Maps, albo della cittadinanza attiva; per questa ricerca l'owner porta il tetto mensile a 190 $; post e siti dei soggetti nuovi | `lista_supplementare_quartieri_deboli.xlsx`, registro v5; §1 octies; commit `cbc1f6c` |
| 14:06-15:24 | Promotori | Promotore per ogni evento; contatti, categorie, posizione sulla diffusione dai siti; immagini a risoluzione da card (DEC-101); agenda delle Biblioteche di Roma (110 eventi); eventi delle pagine mai lette; pagina dei promotori nella wiki | `promotori_eventi.xlsx`, `immagini_eventi_manifest.xlsx`; §1 nonies; commit `626f0fc` |
| 18:05 | Geografia della pagina | Su decisione dell'owner la pagina passa alle zone urbanistiche, la stessa geografia degli abitanti; i numeri aggiornati sono nel §1 nonies | §1 nonies «Geografia»; commit `8000716` |
| 18:11-18:52 | Prima revisione Codex del blocco | Canale nativo muto, canale API: 4 rilievi, corretti, poi APPROVED | appendice C; commit `5e5c51c` |
| 19:09-01:26 | Leve per aumentare gli eventi | Workflow di 60 leve, verifiche di resa e liceità, classifica | `leve_eventi_2026-10-26.xlsx`; §1 decies; commit `db98b9a` |

### 26 ottobre: leve gratuite, regola per promotore, notizie, timeline, qualità

| Quando | Passo | Che cosa è stato fatto | Dove |
|---|---|---|---|
| 00:26-06:39 | Leve a costo zero | Feed iCal e REST dei siti (139 eventi in pagina), normalizzazione NFKC dei post, recupero geografico, pagine evento WordPress, link dei post, RSS di enti, VisitLazio | §1 decies; commit `49fb36b`, `d63c241`, `79af2f2` |
| 07:14-07:52 | Dove cercare per promotore e costi | Prova del canale sui siti (0 $), regola per ognuno dei 1.246 promotori, registro v6, costi mensili | `promotori_dove_cercare_2026-10-26.xlsx`, `registro_fonti_v6.xlsx`; §1 undecies; commit `a48b9cf`, `8ea3b08` |
| 08:38-10:56 | Notizie dai dati già raccolti | 14.779 voci rilette con modelli AI: 402 notizie confermate | `notizie_dai_dati_2026-10-26.xlsx`; `NOTIZIE_DAI_DATI_2026-10-26.md`; commit `d95572b`, `e98d5aa` |
| 11:12-12:13 | Timeline di brevi | 9.643 voci di ottobre: una breve ogni 2 ore per quartiere non c'è | `timeline_brevi_2026-10-26.xlsx`; `TIMELINE_BREVI_2026-10-26.md`; commit `d75fdea` |
| 14:07-15:19 | Qualità della pagina | Audit di 155 eventi, validatore con test, correzioni automatiche, pagina che nasconde gli eventi finiti | `QUALITA_EVENTI_2026-10-26.md`; commit `ab96501`, `3a7af96`, `abfce0b` |

### 27 ottobre: questo documento

Ricostruzione del processo; elenco dei run letto dall'API di Apify; copia dei 56 dataset per il pacchetto; mandato per Codex.

## 4. Apify: che cosa è stato letto, che cosa è stato usato, dove sono i dati

**Due account.**

| Account | Come è stato usato | Quando | Spesa |
|---|---|---|---|
| Account del connettore Apify (piano con tetto mensile di 19 $, ciclo 20 ottobre - 19 novembre) | strumenti `mcp__apify__` della sessione | 23-24 ottobre, fino al tetto (il 20 ottobre il connettore non era autenticato in questa sessione) | 21,01 $ di consumo del ciclo al 24 ottobre: circa 12,3 $ di questa sessione (5,67 $ del run sui 584 eventi, circa 6,6 $ di prove e lotti del 24) e 8,69 $ di run già presenti sull'account. L'elenco dei 24 run fino al 23 ottobre alle 11:47 è nel registro della sessione; quello successivo non si può rileggere perché oggi il connettore non è autenticato |
| Account dell'organizzazione (piano Starter, tetto 200 $, conservazione 31 giorni) | API con curl e il token dato dall'owner il 24 ottobre alle 12:46, salvato in un file fuori dal repository e mai stampato | 24 ottobre 12:47 - 25 ottobre 14:29 | 177,50 $ in 56 run (177,84 $ di consumo del mese) |

**Run dell'account del connettore.**

| Run | Attore | Che cosa | Esito | Usato in | Non usato |
|---|---|---|---|---|---|
| `RBMmIabj8Sq1Ne6ge` (20 ott, dataset `L0ppe0aPgOIqmiFGX`) | apify/cheerio-scraper | agenda di culture.roma.it dall'API WordPress, dal luglio 2025 | 6.222 eventi | foglio unico (708 con fine dal 1° ottobre), pagina, punto zero della lettura per differenza | 5.514 eventi: 5.513 finiti prima di ottobre e 1 senza data |
| `tOKJy9yqjegtpFbPV` (23 ott) | apify/facebook-events-scraper | i 584 eventi Facebook della lista dell'owner | 567 eventi, 17 URL falliti | `facebook_eventi.xlsx`, foglio unico, pagina | i 17 URL falliti non sono stati ritentati; 144 eventi fuori Roma restati nel foglio senza pagina: quelli futuri sono usciti dalla pagina con il filtro sulle coordinate del 26 ottobre |
| `ZzvHOWtNNhKGhu4xY`, `TGkZjEtPqCWMOa47o` (24 ott) | unseenuser/fb-events, apify/facebook-pages-scraper | prova su 8 pagine | il lettore eventi scaricava tutto lo storico dal 2018: fermato | solo per scegliere i parametri (`onlyUpcoming`) | tutti i dati |
| `wWo0fYlgwviazdpzC`, `HBPhkpRaHNNi7RFcQ`, `lqhMW0JyIIvsl4dex`, `Qb5zSRsiFnvv2P4DX` (24 ott) | apify/facebook-pages-scraper | 4 lotti delle 1.169 pagine di associazioni | fermati dal tetto mensile: 722 pagine lette | censimento associazioni | le pagine non lette, rilette dall'account dell'organizzazione |
| `aTzsQ7e9xdC9bHpu8` (24 ott) | unseenuser/fb-events | eventi futuri, lotto 1 | fermato dal tetto, 0 righe; lotti 2-4 rifiutati | — | — |
| altri run trovati sull'account il 23 ottobre, non avviati da questa sessione | apify/facebook-events-scraper (8 run del 20 ottobre: 2 dalla console, fermati, e 6 via connettore, 7,95 $ in tutto); unseenuser/fb-events (1 run del 20 ottobre con URL di eventi Facebook in `cityUrls`, 0 $); apify/cheerio-scraper (3 prove del 20 ottobre, una fallita); apify/rag-web-browser (6 run); apify/playwright-scraper (4 run del 23 ottobre) | i run Facebook del 20 ottobre riguardano eventi, ma i loro dati non sono stati letti; Playwright misura le homepage delle testate | — | — | tutto: nessuno è stato letto né usato |

**Run dell'account dell'organizzazione, per fase.** L'elenco completo, run per run, è nell'appendice A.

| Fase | Run | Attori | Righe | Spesa | Usato in | Che cosa non è stato usato |
|---|---|---|---|---|---|---|
| A. Censimento delle 1.169 pagine di associazioni | 11 | pagine 1, eventi futuri 6, ricerca eventi 1, post 3 | 3.911 | 21,54 $ | `associazioni_fonti.xlsx`, wiki `censimento-pagine.md`; i post sono stati riletti il 25 per estrarre eventi (§1 sexies) e il 26 per notizie e timeline | 37 pagine non disponibili; i 200 eventi della prova su 5 pagine note; gli eventi passati della verifica dello zero; la pagina «eventi della città» (3 eventi) |
| B. Ricerca dei 176 eventi senza fonte | 1 | Google | 176 | 0,44 $ | `eventi_senza_fonte_ricerca.xlsx` | risultati su aggregatori; candidati oltre i primi 3 |
| C. Scoperta per parole chiave | 2 | eventi futuri per ricerca, ricerca eventi | 167 | 1,19 $ | `facebook_scoperta_organizzatori.xlsx`, DEC-024 | gli organizzatori nuovi: nessuno con almeno 2 eventi a Roma |
| D. Fonti mirate per le 58 pagine deboli | 2 | Google | 457 | 1,14 $ | `fonti_mirate_pagine_deboli.xlsx`, registro v2 | da 1.274 a 463 candidate: aggregatori, testate, RSA, elenchi, nome del quartiere assente |
| E. Censimento RUNTS (6.247 enti) | 22 | Google 7, pagine 5, eventi futuri 6, post 4 | 26.490 | 111,32 $ | `enti_terzo_settore_fonti.xlsx`; i post riletti il 25 e il 26 come per la fase A | 7,55 $ per un run che leggeva la pagina di una biglietteria abbinata per errore a un ente (2.498 eventi tolti); 16 pagine non lette dei post per il tetto; risultati Google di aggregatori; siti non verificati |
| F. Le 220 pagine verificate dall'owner | 2 | pagine 1, post 1 | 1.311 | 7,26 $ | registro v3; eventi dai post (§1 sexies) | email, Instagram e sito indicati dalle pagine non copiati nel registro |
| G. Ricerca «evento + quartiere» | 3 | Google 2, eventi futuri 1 | 666 | 1,67 $ | `fonti_ricerca_quartieri.xlsx`, registro v4, 3 eventi in pagina | aggregatori, testate, servizi commerciali, gruppi Facebook, profili Instagram: classificati, non letti |
| H. Diagnosi del Comitato Acilia Nord | 2 | eventi futuri 1, post 1 | 25 | 0,13 $ | risposta all'owner | — |
| I. Post, secondo giro | 2 | post | 2.484 | 12,40 $ | eventi dai post (§1 sexies) | 259 elementi in errore (224 + 35); post senza annunci o scartati dai filtri |
| J. Lista supplementare per le 41 pagine deboli | 6 | Google 2, Google Maps 3, post 1 | 3.865 | 16,38 $ | `lista_supplementare_quartieri_deboli.xlsx`, registro v5, eventi in pagina | il primo run Maps (ricerche sovrapposte, rifatto); 1.418 luoghi fuori dalle pagine deboli, attività commerciali e non pertinenti |
| K. Promotori | 3 | pagine 1, Google 1, eventi futuri 1 | 630 | 4,04 $ | `promotori_eventi.xlsx`, wiki `promotori.md`, 30 eventi in pagina | 365 pagine non lette (run fermato: i promotori erano già nel calendario); email e autodescrizioni solo nel foglio, mai nella wiki |
| **Totale** | **56** | | **40.182** | **177,50 $** | | |

**Tutti i dati letti e non usati.** L'elenco completo è nell'allegato
[`PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md) §B.
Sono 106 voci in cinque gruppi, ognuna con il perché e dove si trova ancora il dato:
- dati Apify non usati o scartati;
- dati di siti e liste pubbliche non usati;
- letture fallite o bloccate;
- idee e leve provate e scartate;
- dati tenuti fuori dal repository per regola.

**Fonti lette senza Apify (0 $).** Una richiesta al secondo per host e lo user agent dichiarato (una ogni 1,5 secondi per Roma
Today). Il robots.txt è letto e rispettato dai lettori scritti dal 24 ottobre sera in poi, e da `leggi_eventi_siti.py` dal 25
ottobre; alcuni lettori dei primi giorni non lo leggevano (§6), e Roma Today è stato letto su richiesta dell'owner benché il suo
robots.txt lo vieti (DEC-026). Le scelte di ammissione sono nel §5.

| Fonte | Strumento | Rapporto |
|---|---|---|
| Siti delle fonti: pagine eventi, schema.org, date nel testo | `tools/fonti/leggi_eventi_siti.py` | §4 bis |
| culture.roma.it per differenza (API WordPress) | `tools/fonti/leggi_culture_roma.py` | §4 ter |
| Feed iCal e REST (The Events Calendar, Events Manager, Teatri in Comune), pagine evento WordPress, link dei post, RSS di enti, VisitLazio | `feed_eventi.py`, `fonti_gratis.py` | §1 decies |
| Agenda OPAC delle Biblioteche di Roma | `promotori/biblioteche.py` | §1 nonies |
| Siti dei promotori: contatti, note legali, prova del canale | `promotori/siti.py`, `canali/` | §1 nonies, §1 undecies |
| Geoportale di Roma Capitale (Municipi, suddivisioni, zone urbanistiche, griglia statistica), Nominatim, OpenStreetMap (Overpass), dati aperti (scuole, mercati), elenchi PDF dei centri anziani, albo della cittadinanza attiva | script di geografia e della lista supplementare | §1 bis, §1 septies, §1 octies |
| Roma Today: 324 schede, una volta sola, su richiesta dell'owner del 23 ottobre | `rt_pass1.py`, `rt_pass2.py` | DEC-026 |

## 5. Le scelte

Qui ci sono le scelte che hanno pesato di più sui risultati. L'elenco completo, 257 scelte divise in 22 temi, ciascuna con la data,
chi l'ha presa, il motivo e dove è scritta, è nell'allegato
[`PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md) §A.
Trenta di quelle scelte sono scritte solo nel registro della sessione: l'allegato le segnala.

**Perimetro e regole**
- **Roma Today** (owner e builder). Nessun canale regolare. Il 23 ottobre l'owner ha autorizzato una sola lettura delle 324
  schede, per ricavare promotore e link ufficiale; il testo degli articoli non è stato conservato. La posizione resta aperta in
  DEC-026; il builder raccomanda di chiedere la licenza.
- **Social** (builder; owner il 26 ottobre per questa fase). Facebook si legge solo con Apify (pagine, eventi, post), mai dal
  container. Instagram, i gruppi Facebook e le biglietterie sono esclusi in questa fase anche per decisione dell'owner.
- **Aggregatori, testate, biglietterie** (builder). Esclusi come fonti. Le biglietterie dopo il caso Fever: una sua pagina,
  abbinata per errore a un ente, aveva prodotto 2.498 eventi e 7,5 $ di spesa.
- **Siti** (builder):
  - una richiesta al secondo per host e user agent dichiarato;
  - robots.txt letto e rispettato dai lettori scritti dal 24 ottobre sera; alcuni lettori dei primi giorni non lo leggevano (§6);
  - nessun captcha aggirato: l'annuario della Diocesi si è fermato dopo 22 schede su 342 parrocchie.
- **Repository** (regole del progetto, owner il 23 ottobre per i nomi):
  - solo metodo e numeri; titoli, testi e contatti stanno nei fogli (DEC-102, DEC-104, DEC-109);
  - i nomi delle organizzazioni si scrivono; gli URL dei profili personali no (DEC-105).

**Apify**
- **Attori** (builder):
  - `unseenuser/fb-events` per gli eventi futuri, con `onlyUpcoming`: senza, la prova scaricava tutto lo storico dal 2018;
  - `apify/facebook-pages-scraper` per l'anagrafica delle pagine;
  - `apify/facebook-posts-scraper` per i post: 10 post negli ultimi 6 mesi per i censimenti, 15 post dal 10 settembre per
    estrarre gli eventi;
  - `apify/google-search-scraper` e `compass/crawler-google-places` per scoprire le fonti.
- **Tetti di spesa**: per run (`maxTotalChargeUsd`) e per mese (`budget.sh`). Il tetto mensile dello script è salito così:

  | Quando | Tetto | Chi |
  |---|---|---|
  | 24 ott 13:37 | 200 $ di credito | owner: «puoi usare apify in maniera massima (hai 200 dollari di credito)» |
  | 24 ott 18:01 | 100 $ | owner: «Se superi i 100 dollari di spesa, fermati» |
  | 24 ott 18:02 | 150 $ | owner: «allora vai anche fino a 150 dollari, tanto abbiamo 200 dollari di spesa inclusi questo mese» |
  | 25 ott 10:41 | 157 $ | owner: «spendiamo i 12 dollari» |
  | 25 ott 10:48 | 159 $ | owner alle 10:47: «se non finisci con 12 dollari fallo terminare se la differenza è minima» (run da 0,40 $) |
  | 25 ott 12:06 | 190 $ | owner: «spingimi fino a 190 dollari» |
  | 25 ott 14:14 | 198,67 $ | owner: 25 $ per i promotori |
- **Post troncati.** 10 post negli ultimi 6 mesi per i censimenti (builder); 15 post per estrarre gli eventi (owner, 25 ottobre:
  «per avere un'idea di cosa c'è»), dal 10 settembre (builder). 239 pagine su 4.016 restano troncate. La rilettura a 6 mesi di
  circa 970 pagine (circa 160 $) l'ha scartata il builder per costo; l'alternativa degli eventi Facebook passati (circa 5 $) l'ha
  rifiutata l'owner il 26 ottobre.
- **Parole chiave** (builder, in DEC-024). La ricerca di eventi per parole chiave resta solo un controllo: non ha scoperto
  organizzatori nuovi con almeno 2 eventi a Roma.

**Geografia**
- **Metodi**:
  - metodo 1, scelto dal builder dopo una domanda dell'owner: OpenStreetMap e Municipi;
  - metodo 2, chiesto dall'owner il 23 ottobre: suddivisioni toponomastiche e toponimo più vicino;
  - dal 25 ottobre, su decisione dell'owner: zone urbanistiche e toponimo del gazetteer più vicino, la stessa geografia degli
    abitanti;
  - in produzione resta il pacchetto Metodo QN.
- **Fonti trovate cercando un quartiere** (builder). Non ereditano quel quartiere: la zona vale solo se il nome della fonte o il
  testo la provano.
- **Fuori dal Comune** (builder). L'evento si toglie per CAP, sigla di provincia, comune della provincia, altra regione, coordinate
  fuori dalle zone urbanistiche o luogo online.

**Eventi e pagina**
- **Doppioni** (builder). Marcati, mai cancellati. La riga principale va alla fonte più vicina alla primaria: è l'opzione a) di
  DEC-025, ancora proposta.
- **Annunci nei post** (builder). Estrattore a regole, senza modelli AI; gli annunci sono pubblicati come «da verificare». Sui
  blocchi di testo con una data dei siti valgono gli stessi filtri; i siti con più di 20 blocchi datati sono esclusi.
- **Data di riferimento** (builder). La pagina è calcolata al 25 ottobre; dal 26 nasconde da sola gli eventi finiti.
- **Corsi e attività ricorrenti** (builder). Contati come eventi; la regola di conteggio è una decisione aperta (§9).

**Censimenti e registro**
- **RUNTS** (builder):
  - un sito vale solo con il codice fiscale nella home, oppure con dominio e nome coerenti;
  - un ente «rientra» solo con due segnali, con un segnale solo è «da verificare».
- **Registro** (builder, DEC-024). Le candidate nuove entrano come «candidata», senza decisioni prese al posto dell'owner. Le 220
  pagine indicate dall'owner sono tutte «tenere», senza verificarne gli eventi, come chiesto.

**Promotori**
- **Promotore di un evento** (builder). È l'host dell'evento Facebook, la pagina che pubblica il post, il «a cura di» di
  culture.roma.it o il sito della fonte.
- **Diffusione** (builder). A un evento va la posizione più restrittiva fra i suoi promotori. Il fatto va tenuto distinto da
  testi e immagini e dal canale: la separazione fra la posizione del promotore e la regola del canale è stata proposta all'owner
  ma non è applicata nei file (§9).
- **Immagini** (DEC-101). Risoluzione da card, lato lungo di 800 pixel, provenienza registrata, mai nel repository.
- **Dove cercare** (regola dell'owner, prova del builder):
  - il canale più economico, con una prova per promotore;
  - la pagina da leggere è sempre una pagina indice, mai quella di un singolo evento;
  - i link Facebook sono ridotti alla pagina.

**Costi**
- **Cadenza** (builder). I post si pagano a post: leggere ogni giorno costa quasi come leggere ogni settimana.

**Qualità e revisione**
- **Errore grave** (builder):
  - definizione: data sbagliata, già passato, non è un evento, fuori Roma o online, pagina incoerente;
  - campione con seme fisso e Roma Today escluso;
  - un secondo revisore su un evento ogni quattro.
- **Revisione Codex** (owner il 16 ottobre). Sul canale API quando il canale nativo tace per 10 minuti; il rapporto integrale va
  sulla PR (DEC-007).
- **Notizie e timeline**. Solo dati già raccolti, senza Apify né letture nuove e senza testate (owner); modelli AI con verifica
  scettica (builder).

## 6. Errori trovati e corretti

Qui ci sono gli errori che hanno cambiato numeri, spesa o regole. L'elenco completo, 144 voci con quando, come è stato trovato e
corretto e dove, è nell'allegato [`PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md) §C.

| Quando | Errore | Correzione |
|---|---|---|
| 23-25 ott | **robots.txt.** Alcuni lettori dei primi giorni non lo leggevano: ricerca dei 176 eventi senza fonte, pagine dei luoghi di culture.roma.it, siti del censimento delle associazioni, verifica dei siti e delle email RUNTS, schede della Diocesi (robots.txt controllato a mano, ma senza user agent dichiarato) e la prima prova di `leggi_eventi_siti.py` | Trovato nella verifica di questo documento; le letture sono già fatte. I lettori scritti dal 24 ottobre sera lo leggono, `leggi_eventi_siti.py` dal 25 ottobre (`5e5c51c`) |
| 24 ott 19:11 | Una pagina di biglietteria (Fever) abbinata per errore a un ente RUNTS è stata letta senza tetto: 2.498 eventi e 7,55 $ | Run fermato, eventi tolti, biglietterie escluse da tutte le letture successive |
| 24-25 ott | Le fonti trovate cercando un quartiere ereditavano quel quartiere (un teatro di Mestre sulla Magliana, un Municipio su un altro quartiere) | La zona vale solo se il nome della fonte o il testo la provano |
| 23 ott 16:03 - 24 ott 20:05 | Indirizzi email nei file pubblicati della wiki, dal primo commit della wiki (`0dd6de8`); trovati il 24 ottobre alle 20:01 | Build corretto e coperto da un test (`0c05930`), wiki rigenerata senza email (`05874ea`); le email restano nella storia del ramo da `0dd6de8` (§9) |
| 24 ott 19:19 | Un ente RUNTS «rientrava» con un solo segnale: 1.517 enti | Servono due segnali: 954 |
| 25 ott 11:41 | 85 eventi fuori Roma nella pagina: 44 negli Stati Uniti da un widget di un sito, eventi Fever all'estero | Tolti; filtri per CAP, provincia e siti di altri comuni |
| 25 ott 14:13 | Togliendo la query dai link `permalink.php` i post finivano alla pagina sbagliata | Chiave che conserva `story_fbid`; lo stesso errore nel campionatore dell'audit, corretto il 26 ottobre |
| 25 ott 15:18 | La lista supplementare aveva letto tre blocchi da Roma Today, presi come «sito» di una polisportiva: contrario a DEC-026 | Blocchi tolti; esclusione di Roma Today in tutti i lettori |
| 25 ott 18:30 | Revisione Codex: il lettore dei siti non leggeva robots.txt (la prima prova del 24 ottobre era stata fatta senza); il confine del repository valeva solo per `docs/`; i telefoni passavano nei promotori | Corretti con test in `5e5c51c` |
| 26 ott 07:36-07:45 | Registro v6: gli id dello schedario scorrevano (18 scomparsi, 3.412 rinominati); il foglio «Leggimi» era il primo e lo schedario scendeva a 3.715 voci; il registro si rigenerava da sé stesso; lo schedario pubblicato aveva link Facebook a video e post con il titolo nell'indirizzo | Id riusati per nome, alias o pagina; «Leggimi» in fondo; ricostruzione sempre dal v5; link ridotti alla pagina |
| 26 ott 10:57 | «Senza eventi» calcolato con lo schedario del 13 ottobre: 176 organizzazioni su 194, sovrastimato | Ricalcolato sulla pagina eventi: 111 su 194 (`e98d5aa`), dopo una domanda dell'owner |
| 26 ott 14:24 | Le ore degli eventi Facebook erano in UTC, una o due ore indietro (37 su 45 nel campione); pagine d'archivio ridatate all'anno in corso; eventi fuori Roma con le coordinate; la pagina avrebbe mostrato eventi finiti | Correzioni con test (`3a7af96`, `abfce0b`); errori gravi dal 28% al 22% |
| 26 ott 01:32 | Il workflow pesante di verifica delle leve ha consumato circa 6 milioni di token per due verifiche | Fermato, sostituito da un giro leggero |

## 7. File prodotti

**Fogli consegnati all'owner** (`/mnt/user-data/outputs` della sessione; copie nel pacchetto, cartella `uscite/`, senza le parti prese da Roma Today).

| Data | Foglio | Che cosa contiene | Rapporto |
|---|---|---|---|
| 23 ott | `facebook_eventi.xlsx`, `eventi_scraping.xlsx` | i 567 eventi Facebook e gli URL falliti | §1 |
| 24 ott | `eventi_unico.xlsx` | foglio unificato: Facebook, culture.roma.it, fonti locali, Roma Today, geografia, doppioni, riga principale | §1 |
| 23 ott | `culture_luoghi.json` | coordinate dei luoghi di culture.roma.it, per la geografia e come ingresso del build della wiki | §1 |
| 24 ott | `culture_roma_delta_2026-10-24.xlsx` | prima lettura per differenza di culture.roma.it | §4 ter |
| 24 ott | `associazioni_fonti.xlsx` | censimento delle 1.169 pagine di associazioni | §2 |
| 24 ott | `eventi_senza_fonte_ricerca.xlsx` | ricerca uno a uno dei 176 eventi senza fonte | §3 |
| 24 ott | `eventi_siti_prova_2026-10-24.xlsx` | prima lettura dei siti delle fonti | §4 bis |
| 24 ott | `facebook_scoperta_organizzatori.xlsx` | scoperta per parole chiave | §5 |
| 24 ott | `fonti_mirate_pagine_deboli.xlsx`, `registro_fonti_v2_pagine_deboli.xlsx` | fonti mirate per le 58 pagine deboli e registro v2 | §1 bis |
| 24 ott | `enti_terzo_settore_fonti.xlsx` | censimento RUNTS (email solo qui) | §1 ter |
| 24 ott | `simulazione_eventi_quartieri.xlsx` | simulazione «un evento per ente» | §1 quater |
| 24 ott | `registro_fonti_v3.xlsx`, `fonti_ricerca_quartieri.xlsx`, `registro_fonti_v4.xlsx` | 220 pagine dell'owner; ricerca evento + quartiere | §1 quinquies |
| 25 ott | `eventi_per_abitanti.xlsx` | eventi ogni 10.000 abitanti per pagina | §1 septies |
| 25 ott | `lista_supplementare_quartieri_deboli.xlsx`, `registro_fonti_v5.xlsx` | lista supplementare e registro v5 | §1 octies |
| 26 ott | `eventi_dai_post_facebook.xlsx` | annunci di eventi nei post (unico già su Drive) | §1 sexies |
| 26 ott | `promotori_eventi.xlsx`, `immagini_eventi_manifest.xlsx`, `immagini_eventi.zip` | promotori, diffusione, immagini (le immagini non sono nel pacchetto) | §1 nonies |
| 26 ott | `leve_eventi_2026-10-26.xlsx` | 60 leve, verifiche e classifica | §1 decies |
| 26 ott | `promotori_dove_cercare_2026-10-26.xlsx`, `registro_fonti_v6.xlsx` | regola per promotore, costi, registro v6 | §1 undecies |
| 26 ott | `notizie_dai_dati_2026-10-26.xlsx`, `timeline_brevi_2026-10-26.xlsx` | notizie e brevi con sintesi scritte da noi | `NOTIZIE_DAI_DATI`, `TIMELINE_BREVI` |

**Nel repository** (ramo della PR): i rapporti del §1, la wiki, i quattro strumenti con test, gli script di lavoro, questo
documento con il suo allegato `PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md` e il mandato per Codex.

## 8. Revisioni e commit su GitHub

Il canale nativo (`@codex review` sulla PR) non ha mai risposto in questo periodo: ogni revisione è passata sul canale API
(`tools/sources-study/codex_check.js`, gpt-5.3-codex, DEC-007), con il rapporto integrale pubblicato sulla PR. L'elenco con i link è
nell'appendice C; tutti i commit sono nell'appendice B.

**Un buco.** I quattro commit delle leve del 26 ottobre (`49fb36b`, `db98b9a`, `d63c241`, `79af2f2`, perimetro `5e5c51c..79af2f2`)
non sono passati da nessuna revisione: la richiesta successiva è partita da `79af2f2`. Toccano script di lavoro senza test
(`feed_eventi.py`, `fonti_gratis.py`, `leve_classifica.py`, `pagina_collect.py`, `pagina_template.html`, `post_estrai.py`, il
README della cartella), il rapporto §1 decies e la wiki rigenerata (`fonti_eventi.json`, `promotori.md`, README). Vanno rivisti
con il prossimo controllo.

| Perimetro | Primo verdetto | Rilievi | Esito |
|---|---|---|---|
| `e9c01a9..8000716` (commit dal 23 al 25 ottobre; `e9c01a9` è la base già rivista) | CHANGES REQUESTED | 1 blocking, 2 defect, 1 note: confine del repository, robots.txt, telefoni, Roma Today | corretti in `5e5c51c`, APPROVED |
| `a48b9cf` (dove cercare per promotore) | CHANGES REQUESTED | 2 blocking: pagina Facebook della regola, rifiuti 401/403 e ritmo del browser | corretti in `8ea3b08`, APPROVED |
| `d95572b`, `e98d5aa` (notizie) | APPROVED | nessuno | — |
| `d75fdea` (timeline) | APPROVED | nessuno | — |
| `ab96501`, `3a7af96` (qualità) | CHANGES REQUESTED | 1 defect: comuni e sigle in minuscolo | corretto in `abfce0b`, APPROVED |

## 9. Decisioni aperte

Le decisioni restano all'owner; il builder non sceglie. L'elenco completo, con le opzioni, dove sono scritte e i costi via via
approvati, è nell'allegato [`PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md`](https://github.com/QuartieriNews/QN/blob/claude/ecstatic-shannon-mjzxvq/docs/sources/PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md) §D.

| Tema | Che cosa decidere | Dove |
|---|---|---|
| Roma Today | Nessuna lettura, licenza da chiedere, o letture una tantum caso per caso; riguarda anche le 32 schede senza link ancora in pagina | DEC-026 |
| Wiki delle fonti eventi | Ramo della wiki di contesto o strumento a sé | DEC-023 |
| Censimento delle pagine Facebook | Quali verdetti entrano come «tenere»; pagine politiche e commerciali; Facebook come canale continuo; rilettura delle dormienti | DEC-024 Q1-Q4 |
| Doppioni | Precedenza fra le fonti: l'opzione a) di DEC-025, oppure la regola «Comune o Facebook prima» proposta dal builder e ricopiata dall'owner il 24 ottobre; alla domanda su quale valga non c'è stata risposta | DEC-025 |
| Annunci estratti dai post | Toglierli, tenerli «da verificare», o rifarli con un modello e una verifica | `QUALITA_EVENTI_2026-10-26.md` §5 |
| Regola di conteggio | Corsi e attività ricorrenti (19% del campione); doppioni fusi e serie contate una volta (leva L16) | `QUALITA_EVENTI_2026-10-26.md` §5; §1 decies |
| Pagine sottili | Decisa dall'owner in chat il 26 ottobre: le pagine a zero o sotto i 10 eventi avranno un blocco con i quartieri limitrofi. Resta da scriverla: DEC-006 (OPEN) parla di un ripiego a livello di Municipio, quindi serve una voce nuova o una modifica, più una mappa dei confini fra pagine che il gazetteer non ha | DEC-006 |
| Cadenza e budget | Il 26 ottobre in chat l'owner ha indicato la lettura giornaliera; resta da fissare il tetto mensile di spesa, da scrivere in configurazione prima di schedulare le letture | §1 undecies |
| Candidate dei registri v2-v6 | Tenere o scartare; il nome generico della riga FE-1216; i contatti delle 220 pagine dell'owner nel registro; separare la posizione del promotore dalla regola del canale nei file della diffusione | §7 punti 2 e 8 del rapporto di stato |
| Notizie e timeline | Fonti non giornalistiche per Notizie e Segnalazioni; forma della timeline; misura delle pagine politiche (circa 4 $) | `NOTIZIE_DAI_DATI` §6; `TIMELINE_BREVI` §5 |
| Contatti e licenze | Invio ai promotori (testi del builder, invio dell'owner); licenza a Roma Capitale per l'agenda; permessi per Zero.eu e Diocesi | `FLUSSO_EVENTI_A_Z.md` §5; §1 nonies |
| Workflow n8n Facebook | Se gira e con quale account Apify; nell'export scrive con nomi di produzione | §4 e §7 del rapporto di stato |
| Consegna e sicurezza | Caricare su Drive i fogli consegnati; ruotare il token Apify incollato in chat il 24 ottobre; riscrivere o no la storia del ramo per le 3 email; far rivedere i quattro commit delle leve (§8); merge delle PR 15 e 17 | — |

## Appendice A. I 56 run dell'account dell'organizzazione

Le fasi sono quelle del §4. Gli input completi sono nel pacchetto (`apify_org/input/`); i dataset restano su Apify fino a circa il
24 novembre 2026.

| Fase | Inizio (UTC) | Attore | Run | Dataset | Stato | Input | Righe | $ |
|---|---|---|---|---|---|---|---|---|
| A | 2026-10-24 12:47 | `apify/facebook-pages-scraper` | `danHMaCdbPdPIyFMS` | `B6o6YmMMIfAwK3HhR` | finito | 447 startUrls | 447 | 3,67 |
| A | 2026-10-24 12:47 | `unseenuser/fb-events` | `2ruTebBWAZ5Rw9Frb` | `MQh9p9dgh25AEEsdz` | finito | 293 pageUrls, maxResults 4000 | 12 | 0,04 |
| A | 2026-10-24 12:47 | `unseenuser/fb-events` | `cTOkvbmVHLcHkMAU0` | `plFwzc2ntCtefQtXn` | finito | 293 pageUrls, maxResults 4000 | 15 | 0,04 |
| A | 2026-10-24 12:47 | `unseenuser/fb-events` | `aCShgbn0dB4ZOD2MY` | `EQX7CfvfBmeIDLudz` | finito | 293 pageUrls, maxResults 4000 | 2 | 0,01 |
| A | 2026-10-24 12:47 | `unseenuser/fb-events` | `dYdSFLqGUFkbqmEQq` | `7VyHfuInDAd0g1wdq` | finito | 290 pageUrls, maxResults 4000 | 31 | 0,09 |
| A | 2026-10-24 12:49 | `unseenuser/fb-events` | `f9lKeg1xU83YKxSKa` | `lduS17x9eYItnQAnS` | finito | 5 pageUrls, maxResults 200 | 200 | 0,6 |
| A | 2026-10-24 13:19 | `apify/facebook-events-scraper` | `nIqnFUJbRhLoyJGyD` | `g23PRVlKYHFw2fpA7` | finito | 12 startUrls, maxEvents 30 | 216 | 2,16 |
| A | 2026-10-24 13:38 | `unseenuser/fb-events` | `h5y6FYXwthGVeCsn6` | `aWI5JkwYi60rRgUgk` | finito | 1 cityUrls, maxResults 15000 | 3 | 0,01 |
| A | 2026-10-24 13:38 | `apify/facebook-posts-scraper` | `LQ6RVAQfuIdGlijvc` | `4nnKxJaSiCcyXeW7g` | finito | 250 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 838 | 4,19 |
| A | 2026-10-24 13:38 | `apify/facebook-posts-scraper` | `MjYgXjMeuuEM0KXQr` | `kV1dbkyAk4uEgpRmY` | finito | 250 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 1111 | 5,56 |
| A | 2026-10-24 13:38 | `apify/facebook-posts-scraper` | `JhhohLsLRtsXE1H4O` | `fmbFkAxmZdbyfNp1V` | finito | 234 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 1036 | 5,18 |
| B | 2026-10-24 13:38 | `apify/google-search-scraper` | `eCImUi6uiC1B2AfIo` | `bV9AtnoyUGQTHZMrb` | finito | maxPagesPerQuery 1 | 176 | 0,44 |
| C | 2026-10-24 13:40 | `unseenuser/fb-events` | `IwYTqrUGkgYhVFjNa` | `rhw409bhcxwRAb20K` | finito | 109 queries, maxResults 15000 | 69 | 0,21 |
| C | 2026-10-24 13:52 | `apify/facebook-events-scraper` | `ebhbeaieApGkNkDfS` | `zazeH9k2jF7NqDvHO` | finito | 30 searchQueries, maxEvents 150 | 98 | 0,98 |
| D | 2026-10-24 14:55 | `apify/google-search-scraper` | `8ImUFsJtwZJMPMYuu` | `fiQeuVtFZ4c74lsQo` | finito | maxPagesPerQuery 1 | 423 | 1,06 |
| D | 2026-10-24 15:17 | `apify/google-search-scraper` | `sXGKDORsEt4kMJL99` | `BDK2MAeTIqjdHdkDC` | finito | maxPagesPerQuery 1 | 34 | 0,09 |
| E | 2026-10-24 16:59 | `apify/google-search-scraper` | `5VKskuRcK6PwV1Pq3` | `f8KwtPIKZhhoi5ZWu` | finito | maxPagesPerQuery 1 | 1243 | 3,11 |
| E | 2026-10-24 16:59 | `apify/google-search-scraper` | `lp74CnLyKfaJIHONY` | `uuqAWMcz6bINmMne9` | finito | maxPagesPerQuery 1 | 1243 | 3,11 |
| E | 2026-10-24 16:59 | `apify/google-search-scraper` | `nbS3Pe8CZoN0R6wQH` | `JHjwPGLf4GADo5cNH` | finito | maxPagesPerQuery 1 | 1243 | 3,11 |
| E | 2026-10-24 16:59 | `apify/google-search-scraper` | `9eVkmYWLwlzdM1DQT` | `kXVDaAmvFfLmg16C8` | finito | maxPagesPerQuery 1 | 1243 | 3,11 |
| E | 2026-10-24 16:59 | `apify/google-search-scraper` | `N0Y5KNfWsnVeSfspj` | `W2MlSjP73d6cPEYn5` | finito | maxPagesPerQuery 1 | 1242 | 3,1 |
| E | 2026-10-24 17:22 | `apify/facebook-pages-scraper` | `88CQXZtE09sF0ShYk` | `2eql1A7C0aQkgmGrF` | finito | 556 startUrls | 556 | 4,56 |
| E | 2026-10-24 17:22 | `apify/facebook-pages-scraper` | `mZpSEgV1V8Cl96hvg` | `N96cymXRw6xFgkbh2` | finito | 556 startUrls | 556 | 4,56 |
| E | 2026-10-24 17:22 | `apify/facebook-pages-scraper` | `oAftX9kO92yRCDH2E` | `Z8ORnvbqINYXREk8X` | finito | 556 startUrls | 556 | 4,56 |
| E | 2026-10-24 17:22 | `apify/facebook-pages-scraper` | `Zd1dFx2iSJ81Hg7iv` | `Pnencf3QSeuNgqrNd` | finito | 555 startUrls | 555 | 4,55 |
| E | 2026-10-24 17:22 | `unseenuser/fb-events` | `pvGaRHQtqgAG6g93c` | `RUcYGbU5wJ0tGCmIE` | finito | 556 pageUrls, maxResults 5000 | 44 | 0,13 |
| E | 2026-10-24 17:22 | `unseenuser/fb-events` | `aH4hgJjPwSv1DVw9w` | `MhQXxxDfdRbFf5hdM` | finito | 556 pageUrls, maxResults 5000 | 78 | 0,23 |
| E | 2026-10-24 17:22 | `unseenuser/fb-events` | `FRz45jjOWOfJTVvXh` | `G0gJmqRkygCu7aKPe` | fermato | 556 pageUrls, maxResults 5000 | 2515 | 7,54 |
| E | 2026-10-24 17:22 | `unseenuser/fb-events` | `Jf1S4i4AIg19tThXa` | `rNhYaAnZMvDKO43Lg` | finito | 555 pageUrls, maxResults 5000 | 45 | 0,14 |
| E | 2026-10-24 18:02 | `apify/google-search-scraper` | `7yU9ZggAm0rHL8NJW` | `8C6bihJjzn2BDagOv` | finito | maxPagesPerQuery 1 | 1835 | 4,59 |
| E | 2026-10-24 18:02 | `apify/google-search-scraper` | `elOowZqTSyrr5K6Pe` | `L3oc8NUDFfzArsChS` | finito | maxPagesPerQuery 1 | 1834 | 4,58 |
| E | 2026-10-24 18:02 | `apify/facebook-pages-scraper` | `PpTM6mgfisFIYxFjE` | `LGE4gq1awquY9XfI3` | finito | 720 startUrls | 719 | 5,9 |
| E | 2026-10-24 18:03 | `unseenuser/fb-events` | `lpnudrpqOPouhpIfX` | `qukBtWzPgA5toCAqF` | finito | 720 pageUrls, maxResults 3000 | 95 | 0,28 |
| E | 2026-10-24 18:26 | `apify/facebook-posts-scraper` | `aXQQbKgstPgQ7dWH6` | `S8sjFj7icfbvYkWh2` | finito | 658 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 2999 | 15 |
| E | 2026-10-24 18:26 | `apify/facebook-posts-scraper` | `0j56mSWalVI7RJsSd` | `LB5KRyhTWTeMmUYnb` | finito | 658 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 3010 | 15 |
| E | 2026-10-24 18:26 | `apify/facebook-posts-scraper` | `rEfhQTPt8VfTP0idj` | `mX1VFv5nf6rZYw2N7` | finito | 656 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 3009 | 15 |
| F | 2026-10-24 19:11 | `apify/facebook-pages-scraper` | `CtiPR9HhGywSYUtPU` | `TPzOG3Jg11fGGMGP7` | finito | 220 startUrls | 220 | 1,8 |
| E | 2026-10-24 19:12 | `unseenuser/fb-events` | `83e8bFnyBcK4y35zr` | `yYOxHJyTkT2Hphhg2` | finito | 472 pageUrls, maxResults 400 | 51 | 0,15 |
| E | 2026-10-24 19:12 | `apify/facebook-posts-scraper` | `RyOmMBS8FeyMw1Y6x` | `hjRAB3YcLTYArkbds` | finito | 472 startUrls, resultsLimit 10, onlyPostsNewerThan 2026-04-24 | 1819 | 9 |
| G | 2026-10-24 20:14 | `apify/google-search-scraper` | `ojqWLaXFQn7VoaLEn` | `VcC3YPOACifz5eXHs` | finito | maxPagesPerQuery 3 | 278 | 0,69 |
| G | 2026-10-24 20:21 | `apify/google-search-scraper` | `jo7Gvnxe76dtIjUis` | `F0U00QwCpQ10aIpkR` | finito | maxPagesPerQuery 2 | 382 | 0,95 |
| G | 2026-10-24 20:30 | `unseenuser/fb-events` | `GQhjcOhJCqLYtekhc` | `gjlPUJyQMbjn5VMGa` | finito | 181 pageUrls, maxResults 600 | 6 | 0,02 |
| H | 2026-10-25 10:21 | `unseenuser/fb-events` | `rKZI4JCvmjKi8zKAd` | `WgZVxJSSaXN4EOCaQ` | finito | 1 pageUrls, maxResults 50 | 0 | 0 |
| H | 2026-10-25 10:21 | `apify/facebook-posts-scraper` | `GWa0Z9k5Jec3x3F83` | `Gh6aoWI8nHoEAp36u` | finito | 1 startUrls, resultsLimit 25, onlyPostsNewerThan 2026-07-25 | 25 | 0,13 |
| F | 2026-10-25 10:24 | `apify/facebook-posts-scraper` | `p3lejt42zobSuGhAX` | `EOxqjMVD7l3m9dBQp` | finito | 220 startUrls, resultsLimit 15, onlyPostsNewerThan 2026-09-10 | 1091 | 5,46 |
| I | 2026-10-25 10:42 | `apify/facebook-posts-scraper` | `FadEFHWhEl42NFiVT` | `ZjpfnYGBG1E3VKRD6` | finito | 662 startUrls, resultsLimit 15, onlyPostsNewerThan 2026-09-10 | 2404 | 12 |
| I | 2026-10-25 10:48 | `apify/facebook-posts-scraper` | `D5bDaof7cafKpI3L5` | `wa0yravbdRAq3odoy` | finito | 42 startUrls, resultsLimit 15, onlyPostsNewerThan 2026-09-10 | 80 | 0,4 |
| J | 2026-10-25 12:05 | `apify/google-search-scraper` | `SdbpiNrdKcQHQmOjX` | `xbuMDvzOomW6ZKaaj` | finito | maxPagesPerQuery 1 | 336 | 0,84 |
| J | 2026-10-25 12:07 | `compass/crawler-google-places` | `Pa5pkaJcI4qIccpy7` | `Mme9vO47raZuQpeFt` | finito | 276 startUrls, maxCrawledPlacesPerSearch 15 | 60 | 0,24 |
| J | 2026-10-25 12:08 | `apify/google-search-scraper` | `xWW8HLLcKn4qVFfmE` | `eiUqb5UuJAhmwgj5O` | finito | 30 queries (albi delle associazioni dei Municipi), maxPagesPerQuery 1 | 30 | 0,07 |
| J | 2026-10-25 12:11 | `compass/crawler-google-places` | `ev3qMwWp2KWkZWV9l` | `0j1qTHPcsYreFuxOr` | finito | 276 startUrls, maxCrawledPlacesPerSearch 15 | 1696 | 6,78 |
| J | 2026-10-25 12:15 | `compass/crawler-google-places` | `nkNIOPu4foQIsLxka` | `qYvnZlllReEGd1Cus` | finito | 69 startUrls, maxCrawledPlacesPerSearch 12 | 280 | 1,12 |
| J | 2026-10-25 12:27 | `apify/facebook-posts-scraper` | `hlQbfdDdXXMt2MMTM` | `EaMAj9lFGNABIgkRP` | finito | 227 startUrls, resultsLimit 15, onlyPostsNewerThan 2026-09-10 | 1463 | 7,32 |
| K | 2026-10-25 14:14 | `apify/facebook-pages-scraper` | `UAKW1ZmcRxUy8BqVJ` | `uIqSVDb7OoQYnP2Vw` | finito | 428 startUrls | 428 | 3,51 |
| K | 2026-10-25 14:14 | `apify/google-search-scraper` | `WuxNjC2P9iui78LQb` | `mPPl2BEmNMY6YxX6y` | finito | maxPagesPerQuery 1 | 154 | 0,39 |
| K | 2026-10-25 14:29 | `unseenuser/fb-events` | `UeOVLyOohYE9IJjkU` | `vNfq2SA2f5j0CDtEh` | fermato | 604 pageUrls, maxResults 2500 | 48 | 0,14 |

## Appendice B. Commit del lavoro sulle fonti degli eventi

| Data (UTC) | Commit | Oggetto |
|---|---|---|
| 10-23 16:03 | [`0dd6de8`](https://github.com/QuartieriNews/QN/commit/0dd6de8254c57c6689af4f8c2449a98e089af63b) | Wiki delle fonti eventi: schedario delle fonti, schede degli aggregatori, pagine "dove cercare" |
| 10-23 16:11 | [`a86149c`](https://github.com/QuartieriNews/QN/commit/a86149cba1f1a869e940b0e96ce0fa14b0ba1e8f) | Wiki fonti eventi: nessuna anonimizzazione (DEC-105), via il filtro sui nomi di persona |
| 10-23 16:11 | [`3e06376`](https://github.com/QuartieriNews/QN/commit/3e0637606435255603af897a887452b89cbb64d8) | Wiki fonti eventi: refuso nel README (virgola nel conteggio) |
| 10-24 12:49 | [`2965b2c`](https://github.com/QuartieriNews/QN/commit/2965b2c2a1c2821b927731c742b2547f5586fbac) | Storico dei quartieri: stato del wiki di contesto e piano «una settimana, un mese» (fuori tema: commit di un'altra sessione sullo stesso ramo, compreso nel perimetro della prima revisione) |
| 10-24 13:42 | [`a644165`](https://github.com/QuartieriNews/QN/commit/a6441651bf4f9950dbdc060d3e6ef2fd440780f2) | Wiki fonti eventi: censimento delle pagine Facebook del 24 ottobre come candidate |
| 10-24 13:43 | [`2530db8`](https://github.com/QuartieriNews/QN/commit/2530db86f9a15b34b7a89d656026879161b1110f) | Wiki fonti eventi: censimento rigenerato con i post Facebook degli ultimi sei mesi |
| 10-24 13:44 | [`8dd4c49`](https://github.com/QuartieriNews/QN/commit/8dd4c492e9d07a8269d3047a783aac06cb791f02) | Wiki fonti eventi: README, conteggi allineati allo schedario rigenerato |
| 10-24 13:46 | [`2bdead3`](https://github.com/QuartieriNews/QN/commit/2bdead348bda18bb1db48a2ba8e326c12d6a6128) | Lettura settimanale dei siti delle fonti: tools/fonti/leggi_eventi_siti.py |
| 10-24 13:47 | [`75fd77a`](https://github.com/QuartieriNews/QN/commit/75fd77aeb13831014b9577888e521c5afd4e8361) | Decisioni aperte: censimento pagine Facebook (DEC-024) e precedenza fra fonti per i doppioni (DEC-025) |
| 10-24 13:52 | [`31fde6a`](https://github.com/QuartieriNews/QN/commit/31fde6abaa78c1865664530724e1f052450757e5) | Fonti eventi: stato al 24 ottobre 2026 e flusso continuo proposto per canale |
| 10-24 13:56 | [`d08f873`](https://github.com/QuartieriNews/QN/commit/d08f8731a65c05df80271904e35c5c65b8b21e5b) | Fonti eventi: esito della scoperta per parole chiave su Facebook nel rapporto e in DEC-024 |
| 10-24 13:58 | [`d336977`](https://github.com/QuartieriNews/QN/commit/d336977230de666a7c4abe696617a47dddb453ad) | Fonti eventi: esito della prima lettura dei siti nel rapporto di stato |
| 10-24 14:09 | [`438418c`](https://github.com/QuartieriNews/QN/commit/438418c49addc1dd82af747db9ab07a62eaf70b1) | Lettura per differenza di culture.roma.it: tools/fonti/leggi_culture_roma.py |
| 10-24 14:11 | [`593bb7c`](https://github.com/QuartieriNews/QN/commit/593bb7c0bd8f65def3adf128d579ef1836e8f225) | Wiki fonti eventi: fusioni proposte fra voci dello schedario (pagina generata, mai applicate) |
| 10-24 14:12 | [`62cc43a`](https://github.com/QuartieriNews/QN/commit/62cc43a386c761197e9c8979dfca884986b432e8) | Lettura culture.roma.it: il tema spezza le righe dentro i tag, il parser li accetta |
| 10-24 14:14 | [`509349a`](https://github.com/QuartieriNews/QN/commit/509349aec2e29ccf8d59a7142b856498ad10f22a) | Fonti eventi: esito della prima lettura per differenza di culture.roma.it, domini morti, fusioni proposte |
| 10-24 15:22 | [`b93e14a`](https://github.com/QuartieriNews/QN/commit/b93e14ac2c11f8bd73040f26d81f4dd251372d85) | Wiki fonti eventi: una riga del registro senza nome utile non è una fonte |
| 10-24 15:25 | [`d3a9958`](https://github.com/QuartieriNews/QN/commit/d3a995817962cedbaf849c131ee5ce6ec31fcce0) | Wiki fonti eventi rigenerata dal registro v2: 445 candidate mirate per le 58 pagine QN deboli |
| 10-24 15:27 | [`8bc2b09`](https://github.com/QuartieriNews/QN/commit/8bc2b09c8051a55b0d1509dd0b0cc62a875856c3) | Decisioni aperte DEC-023 (wiki fonti eventi) e DEC-026 (Roma Today); valutazione del workflow n8n nel rapporto |
| 10-24 15:28 | [`97ea556`](https://github.com/QuartieriNews/QN/commit/97ea556e88e85f1e7aed1ece5f922d901f98949f) | Fonti eventi: ricerca puntuale completata nell'ordine previsto (sito del luogo, poi web): 30 fonti dirette |
| 10-24 15:28 | [`4797d8d`](https://github.com/QuartieriNews/QN/commit/4797d8de44ba0194f4083ee297f23cc5ec68ea9c) | Fonti eventi: conteggi della ricerca puntuale allineati al foglio |
| 10-24 15:29 | [`5e63c78`](https://github.com/QuartieriNews/QN/commit/5e63c78bb1c4e43071868548b5a02f2fcfd5757d) | Script di lavoro del blocco eventi di ottobre 2026, versionati come copia di sicurezza (non prodotti) |
| 10-24 19:20 | [`084cdb2`](https://github.com/QuartieriNews/QN/commit/084cdb2f615a624eea787635324455058e9d5a24) | Wiki fonti eventi: il build legge anche il censimento degli enti del terzo settore (RUNTS) |
| 10-24 20:05 | [`0c05930`](https://github.com/QuartieriNews/QN/commit/0c05930b7047ed556715a336eb0af3c83e432d54) | Wiki fonti eventi: nessun indirizzo email nelle pagine generate |
| 10-24 20:05 | [`05874ea`](https://github.com/QuartieriNews/QN/commit/05874eaa0f9ec9c3ad8af433430295986188915d) | Wiki fonti eventi rigenerata dal registro v3 e dai censimenti del 24 ottobre (pagine Facebook e RUNTS) |
| 10-24 20:05 | [`1965c62`](https://github.com/QuartieriNews/QN/commit/1965c62f0427ce8240d11c5daffd4c945825bd85) | Flusso eventi da A a Z: fonti, cadenze per livello di produttività, passi fino alla home del quartiere (proposta) |
| 10-24 21:05 | [`1a3997d`](https://github.com/QuartieriNews/QN/commit/1a3997db350529ef49b2a07eadfeae623cb221ca) | Wiki fonti eventi rigenerata dal registro v4: 129 candidate dalla ricerca «evento / eventi / festa + quartiere» |
| 10-25 10:37 | [`58dde9e`](https://github.com/QuartieriNews/QN/commit/58dde9e4d8aef44c294dcebe5d09679d39459d69) | Eventi dai post Facebook delle fonti: rapporto §1 sexies e copia degli script di lavoro |
| 10-25 10:52 | [`9132fb3`](https://github.com/QuartieriNews/QN/commit/9132fb347c82728c93cd8da0598fb492bad7cdf1) | Post Facebook, secondo giro: 657 pagine mai lette e zona solo con prove |
| 10-25 11:43 | [`cf197be`](https://github.com/QuartieriNews/QN/commit/cf197becbf3527caf1b65ecfc43ea9df9670d17a) | Eventi contro abitanti per pagina QN: rapporto §1 septies e script |
| 10-25 12:35 | [`cbc1f6c`](https://github.com/QuartieriNews/QN/commit/cbc1f6cf3df965e741c60c2484d3c7c49bf0d366) | Lista supplementare per le 41 pagine deboli: registro fonti v5 e wiki rigenerata |
| 10-25 15:24 | [`626f0fc`](https://github.com/QuartieriNews/QN/commit/626f0fce2d8b1e1472ddf7a4e730b494eb3c8d98) | Promotori degli eventi: pagina della wiki, categorie, diffusione e rapporto §1 nonies |
| 10-25 18:11 | [`8000716`](https://github.com/QuartieriNews/QN/commit/8000716fdac70da76943a1829bdd0cb110eb82a2) | Pagina degli eventi di quartiere con la geografia delle zone urbanistiche |
| 10-25 18:36 | [`5e5c51c`](https://github.com/QuartieriNews/QN/commit/5e5c51c2dcc07e743ee0b29176771581af89e7fa) | Revisione PR 15, canale API: confine del repository, robots.txt, telefoni, Roma Today |
| 10-26 00:45 | [`49fb36b`](https://github.com/QuartieriNews/QN/commit/49fb36b35193f74dddab05b80ce6c96d82799a78) | Leve del 26 ottobre: feed iCal e REST dei siti, post corretti, recupero geografico |
| 10-26 01:51 | [`db98b9a`](https://github.com/QuartieriNews/QN/commit/db98b9ade4097bcf6f338dd9ab251e7a9d3037b4) | Leve del 26 ottobre: classifica della sera dopo la verifica delle leve L31-L60 |
| 10-26 06:55 | [`d63c241`](https://github.com/QuartieriNews/QN/commit/d63c241f132b81953ab6bfa21af52d4946e4372c) | Leve gratuite della sera: tipi evento di WordPress, link dei post, VisitLazio, luoghi per nome |
| 10-26 06:55 | [`79af2f2`](https://github.com/QuartieriNews/QN/commit/79af2f2d77791c3dd44807f563f868730abbd601) | Rapporto §1 decies e README della wiki: virgole tornate al loro posto nei numeri |
| 10-26 07:53 | [`a48b9cf`](https://github.com/QuartieriNews/QN/commit/a48b9cfd21b15ed61dbe11180b21b46813078821) | Dove cercare per promotore: prova del canale sui siti, registro v6, costi mensili |
| 10-26 08:18 | [`8ea3b08`](https://github.com/QuartieriNews/QN/commit/8ea3b08e645d4f904b02a86eb19e727975230e1c) | Revisione PR 15, canale API: pagina Facebook della regola ridotta, rifiuti e ritmo del browser |
| 10-26 10:48 | [`d95572b`](https://github.com/QuartieriNews/QN/commit/d95572bdae83143ec277e518e42c7daa6180c278) | Notizie di quartiere nei dati già raccolti: rilettura a ritroso di 14.779 voci |
| 10-26 10:58 | [`e98d5aa`](https://github.com/QuartieriNews/QN/commit/e98d5aaee6f76501ebded6cd7570569f6056725a) | Notizie dai dati: incrocio eventi/notizie con il criterio giusto |
| 10-26 12:13 | [`d75fdea`](https://github.com/QuartieriNews/QN/commit/d75fdea093692dbbc9288bc9e365f9eb501c61a2) | Timeline di brevi per quartiere: misura sulle voci di ottobre |
| 10-26 14:18 | [`ab96501`](https://github.com/QuartieriNews/QN/commit/ab965012eaf9ab26f3f94d2f81ee6940b060d740) | Validatore dei dati della pagina eventi, con test; date con i punti non sono telefoni |
| 10-26 14:42 | [`3a7af96`](https://github.com/QuartieriNews/QN/commit/3a7af96cbb96c8f860674294a55bb7278ebf3e02) | Qualità della pagina eventi: audit a campione, correzioni con test |
| 10-26 15:02 | [`abfce0b`](https://github.com/QuartieriNews/QN/commit/abfce0bdd444927ad30ce9b0f3bb2e460027c56d) | Validatore: comuni e sigle di provincia riconosciuti anche in minuscolo |

## Appendice C. Revisioni e richieste sulla PR 15

| Quando (UTC) | Che cosa | Verdetto | Link |
|---|---|---|---|
| 2026-10-25 18:12 | @codex review | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6401297267) |
| 2026-10-25 18:38 | Revisione dei commit `e9c01a9..8000716`: canale API (DEC-007), controllo PR15-ottobre | CHANGES REQUESTED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6401579626) |
| 2026-10-25 18:52 | Revisione dei commit `e9c01a9..8000716`, secondo passaggio: canale API (DEC-007), testa `5e5c51c` | APPROVED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6401736122) |
| 2026-10-26 07:53 | Richiesta di revisione: commit `a48b9cf` (dove cercare per promotore) | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6410981213) |
| 2026-10-26 08:18 | Revisione del commit `a48b9cf`: canale API (DEC-007), controllo PR15-dove-cercare | CHANGES REQUESTED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6411402716) |
| 2026-10-26 08:33 | Revisione del commit `a48b9cf`, secondo passaggio: canale API (DEC-007), testa `8ea3b08` | APPROVED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6411662692) |
| 2026-10-26 10:48 | Richiesta di revisione: commit `d95572b` (notizie di quartiere nei dati già raccolti) | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6414164124) |
| 2026-10-26 11:05 | Revisione dei commit `d95572b` e `e98d5aa`: canale API (DEC-007), controllo PR15-notizie | APPROVED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6414474499) |
| 2026-10-26 12:13 | Richiesta di revisione: commit `d75fdea` (timeline di brevi per quartiere) | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6415714021) |
| 2026-10-26 12:38 | Revisione del commit `d75fdea`: canale API (DEC-007), controllo PR15-timeline | APPROVED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6416199243) |
| 2026-10-26 14:43 | @codex review | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6418868316) |
| 2026-10-26 15:02 | Revisione dei commit `ab96501` e `3a7af96`: canale API (DEC-007), controllo PR15-qualita | CHANGES REQUESTED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6419340569) |
| 2026-10-26 15:02 | @codex review | — | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6419342185) |
| 2026-10-26 15:19 | Revisione del commit `abfce0b`: canale API (DEC-007), controllo PR15-qualita-2 | APPROVED | [commento](https://github.com/QuartieriNews/QN/pull/15#issuecomment-6419756738) |

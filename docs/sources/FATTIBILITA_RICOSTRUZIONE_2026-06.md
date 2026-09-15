# Ricostruzione di giugno 2026 attraverso le fonti di QN — analisi di fattibilità (costi, tempi, copertura)

| Campo | Valore |
|---|---|
| Stato | **Analisi di fattibilità** su richiesta dell'owner del 15 settembre 2026 (pomeriggio). Nessuna esecuzione del mese completo è autorizzata né avviata: questo documento serve a decidere. |
| Base | Registro fonti (`SOURCE_REGISTRY.md`), rapporto intermedio (`SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md`), note A2 (`A2_ATTIWEB_TIPOLOGIE.md`) e video (`VIDEO_RICOGNIZIONE_2026-06.md`), più le misure aggiuntive di oggi (§1.3), tutte a costo zero |
| Tetto prove | 50 € autorizzati; spesi 0,86 € (S); residuo **49,14 €**; oggi 0,00 € |
| Convenzioni | **M** misurato, **S** stimato con ipotesi dichiarata, **—** mancante. Prezzi unitari: listini di terze parti raggiunti con la ricerca web il 15 settembre (§4.1), convertiti a 0,92 €/$ (ipotesi prudente, come nel ledger). Nessun prezzo è stato misurato in una prova (T1, T3, T4 ferme) |
| Vincoli | Chiave OpenAI dell'ambiente non confermata: nessuna chiamata AI (metodo §7, fail-closed); nessun abbonamento né ricarica; Facebook fuori dal perimetro dell'Operator (DEC-102); dati per item su Drive `Fonti 2026-06/`, aggregati nel repository (metodo §4.2) |

## 0. Risposta in breve

- **Cosa riesco a fare davvero, oggi, a costo zero**: ho già in mano gli elenchi completi di giugno di tutte le fonti leggibili (A1 365, A2 1.426 + 921 + 46, Cronaca 109, E2 407, E3 104, RomaTV 496, YouTube 131), i testi di A1, Cronaca, E2, E3, 209 PDF di A2, 16 trascrizioni YouTube, 82 trascrizioni RomaTV dei Consigli con le confidenze per parola, e da oggi anche l'audio di RomaTV e l'API di 060608 (E1). Posso costruire il database (§3.4), collegare in modo deterministico convocazioni, verbali e registrazioni della stessa seduta, fare l'OCR locale delle scansioni di A2 (provato oggi: 6 secondi a pagina, 0 €), classificare e localizzare con il gazetteer, e produrre le notizie candidate **leggendo io** le fonti, al ritmo misurato di 10–25 minuti per registrazione e 1–5 minuti per atto o notizia.
- **Cosa non riesco a fare senza di lei**: (1) qualunque elaborazione AI (estrazione, classificazione, verifica, trascrizione a pagamento, OCR via modello): ferma finché la chiave OpenAI non è confermata distinta da quella esposta o ruotata (S0); (2) la trascrizione locale a costo zero: i modelli non sono scaricabili dall'ambiente (host bloccati), ma è eseguibile sul suo PC; (3) l'ascolto dell'audio per la verifica umana; (4) Facebook (accesso personale); (5) la verifica a campione delle notizie candidate e le decisioni di perimetro.
- **Quanto costa**: il mese completo, con AI, costa in denaro poco: scenario centrale **≈ 80 €** una tantum (trascrizione delle commissioni RomaTV 46 €, estrazione e verifica AI 30 €, controlli Codex 1–2 €, OCR 0 €), basso ≈ 10 € (senza trascrizione a pagamento, perimetro ridotto), alto ≈ 200 € (modelli più cari e Assemblee incluse). Il costo vero è il tempo: 30–45 ore mie e 10 ore sue nello scenario centrale (dettaglio in §3.4.1: 1 ora di configurazione, 7,5 di verifica del campione, 1,5 di decisioni). A regime, 30–80 €/mese oltre l'abbonamento n8n esistente (29,28 €/mese), 10–15 ore mie e circa 4 ore sue al mese, Facebook a parte.
- **In quanto tempo**: senza chiave, entro una settimana una prima ricostruzione "a costo zero" (database, collegamenti, disponibilità online, notizie candidate dal materiale già letto e da ciò che leggo a mano nel perimetro ridotto). Con la chiave confermata e l'autorizzazione di spesa, il mese completo verificato in **3–4 settimane** di calendario (dipendenze in §4.4).
- **Raccomandazione**: **esecuzione per fasi** (§6): fase 0 subito a costo zero; fase 1 le prove T1/T3/T4 entro il residuo di 49,14 € appena la chiave è confermata; fase 2 il mese completo su un perimetro che esclude le Assemblee Capitoline, C3/C5/C6/R1 e Facebook (non ricostruibile per giugno), con le commissioni RomaTV trascritte a pagamento o sul suo PC.

## 1. Perimetro e capacità effettiva

### 1.1 Quantità, materiali già acquisiti, capacità

Legenda dello stato di capacità: **provata** (eseguita nel mese di studio), **plausibile** (strumento e accesso ci sono, non ancora eseguita su tutto), **bloccata** (dipende dalla chiave, da un accesso o da un intervento dell'owner).

| Fonte | Materiali di giugno 2026 | Già acquisito e riutilizzabile | Cosa riesco a recuperare e analizzare | Strumenti, accessi, prerequisiti | All'owner | Completezza raggiungibile e lacune | Capacità |
|---|---|---|---|---|---|---|---|
| **A1** notizie e informazioni di servizio dei Municipi | 365 item (M): 135 notizie, 230 avvisi; per Municipio da 7 (IV) a 39 (XIII); per settimana ISO 82, 91, 88, 87, 17 | testo di tutti i 365 (locale), CSV per item su Drive, localizzazione deterministica, dedup con A2 | tutto: lettura, classificazione con gazetteer, collegamento alle sedute (35 convocazioni gemelle in A2) | nessuno oltre la rete; estrazione AI per tema e luogo: chiave | licenza L11 | completa; zona nel 33–38%, resto a Municipio | provata |
| **A2** atti municipali (15 tipologie) | 1.426 atti (M): convocazioni 571, verbali 456, delibere e atti politici 208, determinazioni 191; ≈ 4.200 pagine (S: pagine medie per tipologia dal campione di 120) | elenchi completi con URL; 209 PDF già scaricati (58 verbali I e V, 31 dell'approfondimento, 120 del campione di oggi); testo estratto per i testuali | download completo (≈ 1 ora macchina); testo dal 58% dei documenti (M, 69/120) e OCR locale sul 42% (M, 51/120, tutti in 7 Municipi: III, IV, VI, VIII, IX, XI, XIII); lettura e classificazione | PyMuPDF e RapidOCR (PyPI, 0 €; OCR provato oggi su 3 pagine: 2.400–2.900 caratteri a pagina, 3–9 s, confidenza 0,96–0,98, spazi fra le parole in parte persi); estrazione AI: chiave | decisione sul perimetro (DDS, centrali) | completa sugli atti; **disponibilità a giugno parziale**: fra i 407 verbali di commissione solo 125 risultano pubblicati entro il 30 giugno, 86 a luglio, 45 da agosto, 151 senza data (M, campo `dtPtg`); verbali di Consiglio 2 su 24 entro giugno | provata (testo, OCR), bloccata (AI) |
| **A2-DDS** discipline di traffico (Polizia Locale) | 921 atti (M), 9 Municipi; ≈ 4.100 pagine (S) | elenco completo; 10 PDF letti | tutti testuali (M, 10/10); vie e date di validità estraibili con regole, senza AI | rete; dizionario di vie per la zona (assente nel gazetteer) | perimetro | completa; zona solo per 4 su 10 con il gazetteer attuale | plausibile |
| **A2 centrali** con ricaduta territoriale (GCD, ACD, AY, AZ, GCM) | 46 atti, 24 vicende, 20 possibili notizie (M/S, nota A2 §7.3) | elenco e classificazione già fatti; 5 PDF letti | tutto | rete | perimetro | completa | provata |
| **A3** RomaTV, commissioni municipali | 305 registrazioni, **214,3 ore** (M), 14 Municipi | catalogo con date di seduta e pubblicazione, durate, URL; audio: download provato oggi (§1.3) | audio scaricabile (48 kbps, ≈ 45 MB/ora, ≈ 6 minuti di rete per ora di audio: 214 h ≈ 22 h di download in background); **nessuna trascrizione della piattaforma**; trascrizione a pagamento ferma; trascrizione locale impossibile qui (modelli non scaricabili) | host media consentiti dalle 17:09 di oggi; chiave per l'API di trascrizione; in alternativa il suo PC con un modello locale | scelta fra API e PC; ascolto per la verifica | senza trascrizione: solo date, organi e durate; con trascrizione: come i Consigli | bloccata (testo), provata (audio) |
| **A3** RomaTV, Consigli municipali | 86 registrazioni, 78,0 ore (M): 82 con trascrizione della piattaforma (76,8 h), 4 senza | 82 trascrizioni JSON con confidenza per parola già scaricate (418.151 parole); 7 lette per intero | tutto: confidenza media per parola 0,897 (mediana 0,918; quota di parole sotto 0,7 in media 5,1%); 11,0 ore su 76,8 sono pause oltre il minuto (sospensioni, appelli) | nessuno | ascolto per la verifica | completa; 5 Consigli su 7 letti non hanno verbale in Atti Web | provata |
| **A3** Commissioni Capitoline | 75 sedute, 51,6 ore (M), 16 organi | catalogo | come le commissioni municipali (audio sì, testo no) | come sopra | perimetro (organi cittadini con ricaduta di quartiere: 2 verbali su 5 letti nella nota A2) | senza trascrizione: solo ordini del giorno da CPC/CPV | bloccata (testo) |
| **A3** Assemblee Capitoline e "altro" | 7 Assemblee (41,3 h) + 23 registrazioni "altro" (19,6 h, per lo più Teams del III senza titolo) | catalogo | audio; le Assemblee sono duplicate dalle dirette YouTube (8 video, 37,1 h) | — | esclusione consigliata (§6) | fuori perimetro proposto | — |
| **A4** YouTube Municipi I, V, IX | 131 video (M): 107 commissioni (82,1 h), 16 Consigli (16,3 h), 8 dirette dell'Assemblea (37,1 h) | censimento completo; 22 metadati; 16 sottotitoli automatici (15 del campione) e 15 registrazioni lette; incrocio con verbali e convocazioni | sottotitoli automatici di tutti i 131 (22 su 22 letti li hanno), a ritmo forzato dall'anti-bot: 1 file al minuto con pause, ≈ 3–4 ore macchina in background; date di pubblicazione da metadati | rete; l'IP di uscita è già segnalato da YouTube | ascolto per la verifica | completa sul testo; XIV assente; V fermo al 12 giugno | provata (campione), plausibile (tutto) |
| **C1, C2, C4, C5** Cronaca | 109 item (M): Questura 79, Carabinieri 20, Vigili del Fuoco 8, Polizia Locale 2 | testi completi, localizzazione, dedup (0–1 doppioni) | tutto | rete | licenze L11 | completa; localizzabili a Municipio 30 su 109 | provata |
| **C3, C6, R1** | 0 item a giugno (M) | — | — | — | esclusione | — | — |
| **E2** culture.roma.it | 407 appuntamenti (M) di giugno; 917 pubblicati dopo per lo stock futuro | dati strutturati completi (date evento, luogo, Municipio) | tutto; stock "visibile" giorno per giorno ricostruibile dalle date di pubblicazione | rete | — | completa per il pubblicato; eventi cancellati o modificati dopo giugno non distinguibili | provata |
| **E3** portale istituzionale, eventi | 104 item (M), 7 doppioni con E2 | testo e metadati completi | tutto; periodo dell'evento in testo libero da normalizzare | rete | — | completa; Municipio nel 66% | provata |
| **E1** 060608 | — per giugno (conteggio non eseguito); archivio di **57.132 entità** di tutte le categorie (M, letto oggi alle 17:34) | oggi: host `ws.comune.roma.it` raggiungibile; API `POST public/entita/ricerca` letta: schede con categoria, date, indirizzo, coordinate e zona toponomastica; schema dei filtri letto (`entita/filtroType/<categoria>`: categoria, area, zona, tipologia, calendario), quattro formati di filtro provati senza risultati | plausibile: conteggio di giugno con il formato corretto dei filtri, 1–2 ore di lavoro | rete (ora consentita) | — | da misurare; probabile sovrapposizione alta con E2 (stessi eventi cittadini) | plausibile |
| **Facebook** (eventi e post) | non censito dall'Operator; stima dell'owner: 107 eventi in una raccolta di prova | nessuno nel mio ambiente | **nulla** dall'ambiente (DEC-102: accesso personale, nessuna automazione autenticata); per giugno non ricostruibile a posteriori (gli eventi passati non sono più cercabili con la stessa procedura) | raccolta manuale dell'owner (1 ora a settimana) + Apify sugli URL (servizio esistente; 1,40 $ per 107 eventi nella prova dell'owner) | tutto | a regime sì; per giugno no | bloccata per giugno |

### 1.2 Sovrapposizioni fra piattaforme (prima di stimare il volume)

| Coppia | Misura | Effetto sul volume |
|---|---|---|
| A1 ↔ A2 | 35 avvisi di convocazione con gemello certo in A2, 12 dubbi (M) | le convocazioni si contano una volta come "seduta" |
| A3 ↔ A4, Municipio IX | le 12 registrazioni RomaTV di giugno sono i 3 Consigli del 16, 23 e 30 giugno spezzati in parti: stessi giorni dei 3 video YouTube (M) | −5,4 ore RomaTV, già con trascrizione su entrambe |
| A3 ↔ A4, Municipio V | 39 RomaTV e 9 YouTube; 13 RomaTV hanno un video YouTube lo stesso giorno, 6 con lo stesso organo (S, per titolo) | −≈ 4 ore |
| A3 ↔ A4, Assemblea Capitolina | 7 registrazioni RomaTV (41,3 h) e 8 dirette YouTube (37,1 h) sulle stesse date | una sola copia; proposta: fuori perimetro |
| A2 verbali ↔ video | nel Municipio I ogni verbale di giugno cita il video (30 su 30); altrove abbinamento per data e organo (2 errori su 4 verificati) | stessa seduta, non duplicato: il verbale è l'atto, il video il contenuto |
| E3 ↔ E2 | 7 doppioni certi su 104 (M) | −7 |
| E1 ↔ E2/E3 | non misurabile prima del conteggio di E1 | da misurare |
| Cronaca | 0 certi, 1 dubbio (M) | nessuno |

Volume netto da elaborare per il mese (S): **documenti** ≈ 2.400 (A2 1.426, DDS 921, centrali 46) più 365 item A1, 109 di Cronaca, 511 eventi (E1 esclusa); **registrazioni** 627 lorde (A3 496, A4 131) → ≈ 600 sedute nette dopo le parti spezzate e i doppioni IX e Assemblee; **ore di audio**: con trascrizione gratuita già disponibile ≈ 175 h (RomaTV Consigli 77 h, YouTube 98 h senza le Assemblee), **da trascrivere ≈ 280 h** (RomaTV commissioni municipali 214 h, capitoline 52 h, "altro" 20 h, meno i doppioni con YouTube), fuori perimetro proposto 78 h di Assemblee.

### 1.3 Misure aggiuntive fatte oggi (M, costo 0 €)

1. **Scansioni A2**: campione con seed `2026-06-A2-pdf` di 120 PDF (8 per Municipio): 69 testuali e 51 scansioni; 332 pagine, 114 scansionate; mediana 2 pagine; 2.402 caratteri per pagina nei testuali. Le scansioni dipendono dal Municipio, non dalla tipologia: III, IV, VI, VIII, IX, XI, XIII scansionano quasi tutto (50 su 57), gli altri otto pubblicano testo. Pagine medie: convocazioni 1–2, verbali di commissione 2,5, determinazioni 7,2, verbali di Consiglio 10. Dati su Drive `A2_pdf_campione120.csv`.
2. **OCR locale**: RapidOCR (modelli inclusi nel pacchetto PyPI, CPU) su 3 pagine di un verbale scansionato del IX: 3–9 secondi a pagina a 200 dpi, testo leggibile con confidenza 0,96–0,98, spazi fra le parole in parte persi (utilizzabile per ricerca ed estrazione AI, da rileggere prima di citare). Per ≈ 1.400 pagine scansionate al mese: ≈ 2,5 ore di CPU, 0 €.
3. **Date di pubblicazione in Atti Web** (`dtPtg`, M sulle liste di giugno): verbali di commissione MMV 125 entro giugno, 86 a luglio, 45 da agosto, 151 senza data; verbali di Consiglio CMV 2, 12, 1, 9; determinazioni DMS 76, 24, 0, 91; verbali di Giunta GMV 14, 8, 0, 3; delibere e mozioni municipali per lo più senza data. La nota "documento pubblicato dopo il mese" è quindi misurabile per una parte degli atti e va dichiarata mancante per il resto.
4. **Trascrizioni RomaTV**: il JSON del riconoscimento vocale (parola, tempi, confidenza) è scaricabile dall'host media per gli 82 Consigli: confidenza media per registrazione da 0,70 a 0,95; sotto 0,88 solo spezzoni brevi (40–700 secondi) e un Consiglio dell'VIII; per Municipio da 0,873 (V) a 0,931 (IV). Dati su Drive con questa nota (`A3_speech_confidenza_giugno.csv`).
5. **Audio RomaTV**: dalle 17:09 gli host media rispondono; gli stream audio-only HLS sono cifrati AES-128 con chiave sull'host API (letta) e si scaricano a segmenti con `curl` (il Consiglio del II del 18 giugno: 200 segmenti, 23,9 MB, 145–192 secondi; la Commissione Permanente II del 3 giugno: 178 segmenti, 24,9 MB, 204 secondi). Rimontati in locale con `ffmpeg` statico: durate uguali al catalogo (1.991 e 1.770 secondi), il Consiglio con 27 secondi di silenzio in tutto e la commissione con 212 secondi di silenzio su 1.770 (12%): parlato presente e trascrivibile. Dettagli nel rapporto video §5.
6. **E1**: l'API di 060608 risponde (`POST public/entita/ricerca`, 57.132 entità, pagine da 10 con categoria, date, indirizzo, coordinate e zona toponomastica); lo schema dei filtri è leggibile per categoria, ma i quattro formati di corpo provati danno 0 risultati: il conteggio di giugno richiede ancora di capire il formato (1–2 ore).
7. **Modelli locali di trascrizione**: `pip` funziona, ma i modelli (Hugging Face, GitHub releases, alphacephei, PyTorch) non sono scaricabili: la trascrizione locale è **bloccata qui e plausibile sul PC dell'owner** (4 CPU e 15 GB di RAM in questo ambiente; sul PC dipende dalla macchina: da 0,3 a 1 volta il tempo reale con un modello piccolo, S).

## 2. Lavoro necessario

### 2.1 Processo, passo per passo

1. **Raccolta** (per lo più fatta): elenchi completi con URL e date (tutte le fonti); da completare: i PDF di A2 non ancora scaricati (≈ 2.200 municipali e DDS: 1 ora macchina), i sottotitoli YouTube dei 116 video non ancora letti (3–4 ore macchina a ritmo forzato), gli 82 JSON RomaTV (fatti), l'audio delle commissioni RomaTV (≈ 22 ore di rete in background, solo se si trascrive), E1 (conteggio e schede).
2. **Testo**: estrazione locale dai PDF testuali (fatta per 209, meno di 2 s per file); OCR locale delle scansioni (≈ 1.400 pagine, 2,5 h CPU); sottotitoli e JSON convertiti in testo con tempi (script già scritti).
3. **Trascrizione** dove manca il testo: commissioni RomaTV (280 h). Tre modalità: API a pagamento (ferma), modello locale sul PC dell'owner (0 €, tempo macchina), esclusione (le commissioni RomaTV restano con date e ordini del giorno da MMC/CPC).
4. **Estrazione delle informazioni**: per ogni documento, registrazione o item una scheda con organo, data della seduta, data del fatto se citata, luoghi (via, quartiere, Municipio), tema, decisioni e voti, eventi futuri annunciati, nomi di persona (contati, non copiati), e le notizie candidate con il puntatore all'evidenza. Con AI: un modello economico per tutto, un secondo modello sulle sole notizie candidate (schema di DEC-015 e T4). Senza AI: lettura mia con la scheda a mano (ritmi in §4).
5. **Collegamento**: chiave deterministica **Municipio + data della seduta + organo** per unire convocazione, verbale, registrazione e avviso A1 nella stessa **seduta** (nel Municipio I il link nel verbale rende il legame certo); le parti spezzate di una registrazione si uniscono per titolo e ora; le **vicende** (stessa vicenda in più sedute o fonti: il Regolamento animali in tre Municipi, la variante delle norme tecniche, le librerie) si formano per proposta dell'AI o mia e sono confermate a mano; ogni notizia candidata rimanda a una vicenda e a un'evidenza.
6. **Localizzazione**: gazetteer deterministico (zone e alias, con i falsi positivi noti da rivedere: "Santa Cecilia", "Monte Mario"), Municipio dalla fonte, coordinate e zona toponomastica da E1 quando ci sono; le vie richiedono un dizionario di vie che oggi non esiste: senza, la localizzazione a quartiere resta al 30–40% per i testi e più bassa per le discipline di traffico.
7. **Notizie candidate**: una per fatto utile a un lettore di quartiere, con tempestività (alta se il fatto o la decisione è entro un mese), utilità, territorio, evidenza (URL con pagina o secondo), stato (candidata, verificata, scartata) e la distinzione fra "disponibile a giugno" e "documentata solo dopo" (§5).
8. **Verifica**: controllo di Codex sul metodo e sulla consegna (come per lo studio), verifica a campione dell'owner sulle notizie candidate (quote del metodo §4.3), ascolto di alcuni passaggi audio da parte dell'owner.

### 2.2 Cosa si distingue nel database

| Entità | Definizione | Esempi di giugno |
|---|---|---|
| **Documento** | un file o pagina di fonte con URL: atto A2, avviso A1, comunicato, scheda evento, trascrizione | verbale MMV n. 19/26 del IX; avviso di convocazione del Consiglio del X del 25 giugno |
| **Registrazione** e **parte** | un video o audio pubblicato; una seduta può avere più parti (RomaTV: 18 sedute spezzate; YouTube: appelli separati) | Consiglio del III dell'11 giugno, parte 1 e 2 |
| **Seduta** | riunione di un organo in un giorno: unisce convocazione, verbale, registrazioni, avviso | Commissione LLPP del I del 25 giugno: convocazione MMC sì, verbale no, video sì |
| **Vicenda** | un tema che attraversa più sedute, atti o fonti | Regolamento animali: commissioni del I e del IX, Consiglio del XV, sei convocazioni di luglio |
| **Notizia candidata** | un fatto distinto, localizzato, con evidenza e valutazione | "Cassonetti di via della Stazione di Castel Fusano spostati verso la stazione" (Consiglio X del 25 giugno, minuto 54) |
| **Territorio** | Municipio certo; zona del gazetteer quando riconosciuta; via quando citata | — |

Date tenute separate per ogni riga: **data del fatto** (se nel testo), **data della seduta**, **data di repertorio o dell'atto**, **data di pubblicazione online** (misurata: RomaTV `insertDate`, YouTube `upload_date` per 22 video, E2/E3, A2 `dtPtg` dove presente) e **data di lettura**. La copertura "a giugno" si calcola solo sulle righe con pubblicazione online entro il 30 giugno o con seduta pubblica nel mese; il resto conta come "documentato dopo" (§5).

### 2.3 Database semplice, nelle sedi già concordate

- **Sede**: un foglio Google `QN_giugno2026_ricostruzione` nella cartella Drive `QN Hub / 20 Packages / Fonti 2026-06/` (stessa sede dei dati per item: metodo §4.2), con una scheda per entità (`fonti`, `documenti`, `registrazioni`, `sedute`, `vicende`, `notizie_candidate`, `territori`) e le stesse tabelle esportate in CSV accanto; nessun nome di persona, nessun testo integrale (DEC-102, DEC-104): il testo resta nell'ambiente di lavoro e nelle fonti. Il repository riceve solo lo schema e gli aggregati. Se in seguito serve interrogarlo dal pipeline, le tabelle si importano nelle collezioni `staging_` di Firestore senza ridisegnarle. Nessuna applicazione dedicata.
- **Chiavi**: `doc_id` (fonte + identificativo della fonte), `reg_id` (piattaforma + id video), `seduta_id` (Municipio + data + organo normalizzato), `vicenda_id`, `notizia_id`; ogni notizia porta `evidenza_url`, `evidenza_rif` (pagina del PDF, oppure secondo del video: `?t=1234` su YouTube, offset sul portale RomaTV), `data_fatto`, `data_seduta`, `data_pubblicazione_online`, `disponibile_a_giugno` (sì/no/non misurabile), `tempestivita`, `utilita`, `territorio`, `fonte_prima` (chi ha pubblicato per primo), `sovrapposizioni` (id gemelli), `stato_verifica`.
- **Consultazione**: filtri del foglio per Municipio, zona, settimana, fonte, stato; una scheda di riepilogo con le tabelle di §5. Costruzione: 3–4 ore mie per struttura e caricamento iniziale dai CSV esistenti.

## 3. Costi e tempi

### 3.1 Prezzi unitari usati (S, listini di terze parti, 15 settembre; 0,92 €/$)

| Voce | Prezzo | Fonte |
|---|---|---|
| Trascrizione API `gpt-4o-mini-transcribe` | 0,003 $/min = 0,18 $/h | [costgoat](https://costgoat.com/pricing/openai-transcription), [diyai](https://diyai.io/ai-tools/speech-to-text/openai-whisper-api-pricing-2026/) |
| Trascrizione API `whisper-1` / `gpt-4o-transcribe` | 0,006 $/min = 0,36 $/h | [costbench](https://costbench.com/software/ai-transcription-apis/openai-whisper/), [tokenmix](https://tokenmix.ai/blog/gpt-4o-transcribe-speech-to-text-api-guide-2026) |
| Testo, modello economico (`gpt-4.1-mini`) | 0,40 $/M token in ingresso, 1,60 $/M in uscita; Batch API −50% | [pecollective](https://pecollective.com/tools/openai-api-pricing/), [benchlm](https://benchlm.ai/openai/api-pricing) |
| Testo, seconda fascia (`gpt-5.6-terra`) | 2 $/M in ingresso, 12 $/M in uscita | [cloudzero](https://www.cloudzero.com/blog/openai-pricing/) |
| Codex, controlli | 0,10–0,21 € per controllo (S, ledger) | `TRIAL_LEDGER.md` |

I prezzi vanno **misurati** con T1, T3 e T4 prima dell'autorizzazione del mese completo; il listino ufficiale non è raggiungibile dall'ambiente.

### 3.2 Ipotesi di volume (S)

- Token in ingresso: A1 0,55 M; A2 municipali 3,3 M (4.200 pagine × 2.400 caratteri, 3 caratteri per token); DDS 3,3 M; centrali 0,3 M; Cronaca 0,1 M; eventi 0,65 M (E1 compresa, 500 schede); trascrizioni gratuite 1,7 M (RomaTV Consigli 418.000 parole, YouTube 98 h a 7.000 parole/ora, 1,5 token per parola); trascrizioni delle commissioni RomaTV 2,5 M (280 h a 6.000 parole/ora). Totale ≈ 12,4 M, più il 30% di istruzioni ripetute ≈ **16 M**; in uscita ≈ **2,5 M** (schede da 300–1.500 token).
- Verifica con seconda AI sulle sole notizie candidate: ≈ 1.500 candidate × 3.000 token in ingresso, 500 in uscita.
- Ripetizioni, errori e riprove: +25% sulle voci AI (S; nessuna misura propria).

### 3.3 Costo una tantum per ricostruire giugno (€, S)

| Voce | Basso | Centrale | Alto | Ipotesi |
|---|---|---|---|---|
| Raccolta (rete, PDF, sottotitoli, audio) | 0 | 0 | 0 | strumenti locali; tempo macchina in background |
| OCR scansioni A2 (≈ 1.400 pagine) | 0 | 0 | 3 | basso e centrale: RapidOCR locale; alto: OCR via modello visivo |
| Trascrizione commissioni RomaTV | 0 | 46 | 106 | basso: escluse (alternativa da valutare a parte: trascrizione sul PC dell'owner, §3.4.1); centrale: 280 h a 0,18 $/h; alto: 321 h (Assemblee comprese) a 0,36 $/h |
| Estrazione AI | 3 | 10 | 57 | basso: modello economico via Batch, perimetro ridotto; centrale: `gpt-4.1-mini`; alto: seconda fascia sulle trascrizioni |
| Verifica con seconda AI | 0 | 14 | 20 | basso: solo campione umano; centrale: seconda fascia sulle 1.500 candidate |
| Ripetizioni ed errori (+25% sulle voci AI) | 1 | 18 | 46 | — |
| Controlli Codex | 1 | 2 | 3 | 4–8 controlli da 0,10–0,21 € (metodo e consegna, PR) |
| **Totale una tantum** | **≈ 5** | **≈ 90** | **≈ 235** | il centrale supera il residuo di 49,14 €: richiede autorizzazione |
| Già sostenuti | 0,86 (Codex) | | | ledger |
| Abbonamenti esistenti, non aggiuntivi | n8n Starter 29,28 €/mese; account Apify (solo Facebook); chiave OpenAI (da confermare) | | | nessun nuovo abbonamento |

### 3.4 Ore (S)

| Voce | Basso | Centrale | Alto | Ipotesi |
|---|---|---|---|---|
| Elaborazione macchina (download, OCR, cicli AI) | 8 h | 40 h | 60 h | audio 22 h, sottotitoli 4 h, OCR 2,5 h, cicli AI 4–8 h; in background, non blocca |
| Lavoro operativo mio (script, database, collegamenti, controllo delle schede AI, lettura dove non c'è AI, rapporti) | 15 h | 35 h | 55 h | senza AI la lettura completa non è sostenibile: ≈ 600 sedute × 15 min = 150 h; con AI controllo le schede a 1–2 min ciascuna |
| Ore richieste all'owner | 4 h | 10 h | 17 h | dettaglio in §3.4.1: configurazione iniziale, verifica del campione (quote del metodo §4.3 sulle notizie candidate, dedup, localizzazione, disponibilità online, audio e OCR), decisioni residue; la trascrizione sul PC dell'owner non è inclusa (alternativa valutata a parte); Facebook a regime fuori da questo conto |
| Durata di calendario | 1–2 settimane | 3–4 settimane | 6 settimane | §3.5 |

### 3.4.1 Le ore dell'owner nel dettaglio

Modello concordato: l'Operator esegue lo studio e prepara le evidenze; l'owner controlla un campione e decide sui punti residui. Ogni riga dice perché serve l'owner, cosa faccio da solo prima e cosa trova già pronto. Minuti per unità: stimati (S) dai tempi misurati oggi sui materiali reali (un passaggio di trascrizione con link al secondo: 3–4 minuti; una pagina di PDF: 2; un avviso o un comunicato: 1). Le quantità seguono il metodo §4.3 (minimo di audit, quote mirate su deduplicazione e localizzazione, raddoppiate per le fonti con più di 100 item) applicate al nuovo oggetto, le notizie candidate.

**A. Ricostruzione di giugno, scenario centrale: 600 minuti = 10 ore**

| Blocco | Attività | Quantità | Min/unità | Totale | Perché serve l'owner | Cosa faccio da solo e cosa presento pronto |
|---|---|---|---|---|---|---|
| A. Configurazione iniziale | A1. Chiave OpenAI: conferma scritta che è distinta da quella esposta, oppure rotazione (S0-03) | 1 | 30 | 30 min | solo l'owner detiene e ruota le credenziali (DEC-104); senza, tutta la parte AI resta ferma | checklist dei punti d'uso (ambiente dell'Operator, credenziali n8n, Council) e prova funzionale che eseguo io dopo la conferma; riga del ledger |
| A. Configurazione iniziale | A2. Decisioni di avvio: perimetro (Assemblee, DDS, "altro" RomaTV), modalità per le commissioni RomaTV (API a pagamento, esclusione, o l'alternativa del PC), sede del database, quote del campione | 6 decisioni | 5 | 30 min | perimetro e spesa sono scelte dell'owner e cambiano copertura e costo | un pacchetto di una pagina per decisione: domanda, opzioni, evidenze, conseguenze su costo e copertura, raccomandazione |
| B. Verifica del campione | B1. Notizie candidate contro l'evidenza: il fatto è nell'evidenza indicata; luogo, data e classe di tempestività sono giusti; è utile per un lettore di quartiere | 100 candidate, stratificate (almeno 3 per fonte con candidate, almeno 1 per Municipio, sovrappeso alla classe "tempestività alta") | 3 | 300 min | è il giudizio editoriale su cui poggia il risultato e va dato da chi non l'ha prodotto; per i passaggi video occorre leggere la trascrizione con i nomi e, dove serve, ascoltare | scheda `verifica_campione` con una riga per candidata: testo, fonte, Municipio e zona, link all'evidenza con pagina o secondo, passaggio pertinente (al massimo 40 parole, senza nomi di persona), la mia classificazione; colonne da compilare: confermo sì/no/dubbio, nota |
| B. Verifica del campione | B2. Coppie di deduplicazione | 30 coppie: 10 duplicati certi, 10 dubbi, 10 distinti con gemello (se una classe ha meno casi, tutti i casi esistenti, come nel metodo) | 1,5 | 45 min | la regola (c) del metodo è un giudizio sul "stesso fatto" e nel rapporto intermedio ha già mostrato un caso limite nella Cronaca | scheda `dedup_coppie`: i due link, le tre condizioni (data, luogo, oggetto) come le ho valutate, il verdetto proposto |
| B. Verifica del campione | B3. Localizzazione | 40 item: 20 assegnati a una zona, 20 solo a Municipio o non localizzati | 1 | 40 min | conoscenza dei quartieri che il gazetteer non ha (alias, vie, confini); i falsi positivi noti vanno confermati da una persona | scheda `localizzazione`: toponimo trovato, zona assegnata, alias del gazetteer usato, motivo del "solo Municipio" |
| B. Verifica del campione | B4. Disponibilità online a giugno | 20 item fra quelli classificati "disponibile a giugno" e "documentato dopo" | 1,5 | 30 min | è la distinzione che l'owner ha chiesto di tenere e che decide il conteggio "a giugno"; la lettura dei campi data va confermata sui portali | riga con la data letta, il campo e la pagina dove si legge (`dtPtg` in Atti Web, data di pubblicazione RomaTV, data di caricamento YouTube) |
| B. Verifica del campione | B5. Qualità di trascrizioni e OCR | 6 passaggi audio da 2 minuti (3 RomaTV, 3 YouTube) e 5 pagine scansionate | 4 (audio), 2 (OCR) | 35 min | l'Operator non può ascoltare: la verifica delle trascrizioni sull'audio, richiesta dall'owner, è possibile solo a una persona con l'audio; la lettura di una scansione contro l'OCR conferma l'uso del testo | secondo esatto di inizio, righe della trascrizione, domande precise (nome, toponimo, numero); pagina scansionata e testo OCR affiancati |
| C. Decisioni editoriali residue | C1. Punti residui emersi durante la ricostruzione (`OWNER_DECISION_REQUIRED`): soglie minime per zona, alias del gazetteer da correggere, trattamento dei "documentati dopo", categorie di viabilità, esclusioni finali | ≈ 6 | 10 | 60 min | decidere resta dell'owner (DEC-104); l'accordo fra modelli è evidenza, non autorità | bozza di voce `decisions/` per ciascuno: domanda, opzioni, evidenze dal database, raccomandazione |
| C. Decisioni editoriali residue | C2. Approvazione della consegna dopo il controllo di Codex | 1 | 30 | 30 min | la consegna è approvata dall'owner, non dal builder | riepilogo di due pagine, tabelle di copertura per quartiere e settimana, esito del controllo di Codex, elenco delle lacune |
| | **Totale** | | | **600 min = 10 h** | | |

Come cambia negli altri scenari: basso ≈ 4 h (40 candidate, 10 coppie, 10 localizzazioni, 5 disponibilità, 2 passaggi audio e 2 pagine, 4 decisioni); alto ≈ 17 h (170 candidate, 60 coppie, 80 localizzazioni, 40 disponibilità, 12 passaggi e 10 pagine, 10 decisioni). Il tempo di calendario dell'owner è distribuito: A nella prima settimana, B nella terza e quarta, C alla fine.

**Alternativa non inclusa: trascrizione sul PC dell'owner.** Se scelta al posto dell'API (voce da 46 € nello scenario centrale): circa 1 ora di configurazione una tantum (installazione di un modello locale, prova su una registrazione) più tempo macchina non presidiato (≈ 280 ore di audio al mese: da 3 a 10 giorni di calcolo continuo su un PC medio, S); nessuna ora ricorrente se il processo è automatizzato, altrimenti circa 15 minuti a settimana per avviarlo e consegnare i file. Va valutata a parte con una prova su una registrazione.

**B. A regime, per mese, scenario centrale: ≈ 4 ore (Facebook a parte)**

| Attività | Quantità al mese | Min/unità | Totale | Perché serve l'owner | Cosa presento pronto |
|---|---|---|---|---|---|
| R1. Campione settimanale (modello DEC-103): candidate pubblicate e auto-escluse | 4,3 settimane × (20 pubblicate + 10 escluse) | 1 | ≈ 130 min | controllo editoriale su ciò che esce e su ciò che il filtro scarta; ogni correzione va nel gazetteer, nel registro delle sedi o delle fonti, mai nell'item | scheda settimanale con evidenza e passaggio per ogni riga; le correzioni le applico io |
| R2. Coda delle eccezioni (disaccordo fra prima e seconda AI, DEC-015) | ≈ 15 min a settimana | — | ≈ 65 min | decisione su casi che le regole non risolvono | coda ordinata per motivo strutturato, con evidenza |
| R3. Decisioni residue del mese (alias, soglie, nuove fonti) | 2–3 | 10 | 30 min | come C1 | bozze di voce `decisions/` |
| R4. Lettura del rapporto mensile (copertura, duplicazioni, costi, ore) | 1 | 20 | 20 min | approvazione | rapporto di una pagina con tabelle |
| | | | **≈ 245 min ≈ 4 h** | | |

Scenari: basso ≈ 2,5 h (campione dimezzato), alto ≈ 6 h (campione raddoppiato). La raccolta Facebook (1 ora a settimana, ≈ 4,3 ore al mese) è un impegno già previsto dal modello di raccolta (DEC-102) e non è contata qui.

### 3.5 Dipendenze e parallelismo

- **Gate 1 (owner)**: conferma o rotazione della chiave OpenAI (S0-03). Blocca trascrizione, estrazione e verifica AI, cioè la parte veloce del lavoro. Tutto il resto (fase 0) può partire subito.
- **Gate 2 (owner)**: autorizzazione della spesa oltre il residuo (scenario centrale ≈ 90 €).
- **Parallelo**: raccolta dei PDF, OCR, sottotitoli YouTube, audio RomaTV e costruzione del database procedono insieme e in background; le prove T1/T3/T4 (≤ 49,14 €) subito dopo il gate 1; l'estrazione completa dopo il gate 2; i controlli Codex sul metodo del database prima dell'estrazione, sulla consegna alla fine.
- **Sequenza**: settimana 1 fase 0 e prove; settimane 2–3 estrazione, collegamento e verifica; settimana 4 controllo Codex, verifica a campione dell'owner, consegna.

### 3.6 Costo mensile a regime (S)

| Voce | Basso | Centrale | Alto |
|---|---|---|---|
| Trascrizione commissioni RomaTV (≈ 280 h/mese) | 0 (PC dell'owner) | 46 | 106 |
| AI di estrazione e verifica, con ripetizioni | 5 | 30 | 90 |
| Controlli Codex (campione mensile) | 0,5 | 1 | 2 |
| n8n Starter (esistente) | 29,28 | 29,28 | 29,28 |
| Apify per Facebook (esistente; S dalla prova dell'owner: 1,40 $ per 107 eventi) | 2 | 5 | 10 |
| **Nuove spese mensili** (senza n8n) | **≈ 8** | **≈ 82** | **≈ 210** |
| Ore mie al mese | 6 | 12 | 20 |
| Ore dell'owner al mese: campione settimanale, coda delle eccezioni, decisioni residue, rapporto (§3.4.1) | 2,5 | 4 | 6 |
| Facebook: raccolta settimanale dell'owner (impegno già previsto dal modello DEC-102, non aggiuntivo) | 4,3 | 4,3 | 4,3 |

Sufficienza del piano n8n: le raccolte e le estrazioni vanno organizzate a lotti (un'esecuzione elabora molti item); con un'esecuzione per fonte al giorno più i lotti AI si resta sotto le 2.500 esecuzioni mensili; un'esecuzione per item (3.000–4.000 al mese) non ci starebbe.

## 4. Prove preliminari

Misure ancora mancanti per una previsione affidabile e come ottenerle entro il residuo di 49,14 €:

| Prova | Cosa misura | Costo (S) | Stato |
|---|---|---|---|
| T1 trascrizione API su 3 registrazioni RomaTV (≈ 2–3 h) | costo e qualità per ora, confronto con il JSON della piattaforma sui Consigli | 0,5–1,1 € | **ferma** (chiave) |
| T3 estrazione su 60 item (20 per blocco) | costo per item, precisione di luogo e tema, quota incerta | 0,1–0,3 € | ferma (chiave) |
| T4 seconda AI su 30 candidate | costo per item, quota in coda | 0,3–0,6 € | ferma (chiave) |
| OCR via modello su 10 pagine, contro RapidOCR | qualità e costo per pagina | 0,05 € | ferma (chiave) |
| E1: conteggio di giugno e dedup con E2/E3 | volume e sovrapposizione | 0 € | eseguibile ora (1–2 h) |
| Sottotitoli YouTube per tutti i 131 video | copertura e date di pubblicazione | 0 € | eseguibile ora (3–4 h macchina) |
| Audio RomaTV: 3 registrazioni, silenzi e durata contro la trascrizione | qualità dell'audio, tempo di download | 0 € | in corso |
| Modello locale di trascrizione sul PC dell'owner, 1 registrazione | fattibilità a costo zero, tempo reale | 0 € | richiede l'owner |

Le prove ferme si sbloccano tutte con la conferma della chiave; nessuna richiede abbonamenti. Spesa complessiva prevista delle prove: 1–2 €, ben dentro il residuo.

## 5. Risultato atteso e limiti della validazione

- **Copertura per quartiere e settimana**: tabella zone × settimane ISO 23–27 con notizie candidate distinte, per fonte e per stato di verifica; a parte le righe "solo Municipio" e "non localizzato". Ordine di grandezza atteso (S, dai tassi misurati sui campioni): A1 ≈ 150 notizie localizzate, A2 ≈ 300 (verbali, delibere, mozioni, determinazioni), video ≈ 400 (0,7 per seduta su ≈ 600), Cronaca ≈ 60, eventi ≈ 450 distinti; in tutto 900–1.400 candidate, con forte concentrazione (centro, EUR, Ostia, Montesacro) e decine di zone sotto 3 al mese.
- **Contributo aggiuntivo per fonte**: candidate presenti solo in quella fonte (regole di dedup del metodo §4.1); oggi il video dà 41 candidate su 44 assenti da A1 e Cronaca (S, campione).
- **Duplicazioni**: gemelli registrati per riga con la ragione; intervallo minimo–massimo per i dubbi.
- **Tempestività**: per ogni candidata la distanza fra data del fatto o della seduta e prima pubblicazione online; la classe "disponibile a giugno" solo con pubblicazione misurata entro il 30 giugno.
- **Affidabilità**: confidenza dell'ASR per registrazione (misurata sui Consigli RomaTV; per YouTube non esposta), quota di scansioni con OCR, esito della verifica a campione; nomi di persona e toponimi da confermare sempre su un atto o sul sito.
- **Carico umano**: minuti registrati per fase (mio) e per verifica (owner), come nel ledger.
- **Limiti**: (1) un documento pubblicato dopo giugno (86 + 45 verbali di commissione, 13 di Consiglio, 24 determinazioni, gli atti senza `dtPtg`) aiuta a verificare ma non prova che la notizia fosse disponibile nel mese: la ricostruzione lo segna e lo esclude dal conteggio "a giugno"; (2) le convocazioni provano la seduta, non l'esito; (3) per RomaTV senza trascrizione la disponibilità è del video, non dell'informazione; (4) per gli Eventi lo stock futuro visibile in un giorno di giugno è ricostruibile per E2 ed E3 dalle date di pubblicazione ed evento (con E1 da verificare), ma non per gli eventi cancellati o modificati dopo, né per Facebook; (5) i falsi positivi del gazetteer e l'assenza di un dizionario di vie limitano la localizzazione a quartiere; (6) i prezzi sono di listini terzi finché le prove non li misurano.

## 6. Raccomandazione

**Esecuzione per fasi, con perimetro ridotto nella prima fase.** Motivazione: la parte costosa in denaro è piccola (≈ 90 € centrale) ma dipende da un gate che non controllo (la chiave); la parte costosa in tempo (lettura senza AI) non è sostenibile sull'intero mese; una fase a costo zero produce già il database, le misure di disponibilità online e una prima mappa di copertura, e riduce l'incertezza delle stime prima di spendere.

1. **Fase 0, subito, 0 €, ≈ 1 settimana, 8–10 ore mie**: database (§2.3) caricato con tutti gli elenchi e i testi già acquisiti; sedute collegate (convocazione, verbale, registrazione, avviso); flag di disponibilità online; OCR locale delle scansioni di A2; sottotitoli YouTube di tutti i 131 video; JSON RomaTV degli 82 Consigli; conteggio di E1 e dedup Eventi; notizie candidate dal materiale già letto (44 dal video, 20 dagli atti centrali, DDS con regole) e da ciò che leggo a mano nel perimetro ridotto (verbali testuali di I, V e dei Consigli; Cronaca; A1). Consegna: mappa quartiere × settimana "a costo zero" con le lacune dichiarate. All'owner: 1 ora (decisioni di §7).
2. **Fase 1, appena la chiave è confermata, ≤ 2 €**: T1, T3, T4 e il confronto OCR; prezzi e qualità misurati; stima di §3 aggiornata. All'owner: 1 ora (chiave), più l'eventuale prova del modello locale sul PC.
3. **Fase 2, su autorizzazione (≈ 90 € centrale, 3–4 settimane)**: estrazione AI dell'intero perimetro, trascrizione delle commissioni RomaTV (API, oppure sul suo PC a 0 €), verifica con seconda AI, controllo Codex, verifica a campione dell'owner (7,5 ore, §3.4.1). Esclusi, con motivazione: Assemblee Capitoline (78 h fra le due piattaforme, livello cittadino già coperto dagli atti ACD/AY), C3, C5, C6, R1 (0–2 item), Facebook per giugno (non ricostruibile a posteriori: resta la raccolta settimanale a regime), "altro" di RomaTV (23 registrazioni senza titolo del III, da classificare prima).

Un risultato verificato è quindi possibile in circa **4–5 settimane** dalla conferma della chiave e dell'autorizzazione; senza chiave, in una settimana si ha la fase 0, che vale come base del database e come misura di ciò che le fonti rendono disponibile nel mese.

## 7. Decisioni richieste all'owner

1. Conferma scritta che la chiave OpenAI dell'ambiente è distinta da quella esposta, oppure rotazione (S0-03): sblocca fase 1 e 2.
2. Autorizzazione della fase 0 (0 €) e, dopo la fase 1, della fase 2 con il tetto dello scenario scelto.
3. Perimetro: esclusioni proposte in §6; DDS come categoria "viabilità" con estrazione a regole; commissioni RomaTV trascritte via API o sul suo PC.
4. Collocazione del database: foglio Google in `Fonti 2026-06/` (proposta) o altra sede.
5. Verifica a campione: quote del metodo §4.3 (5 per fonte più le quote mirate) e disponibilità all'ascolto di alcuni passaggi audio.

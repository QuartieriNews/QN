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
- **Aggiornamento delle 19:45 (§9)**: lotto di misura su Opus 5 eseguito con due subagenti (10 Consigli RomaTV e 30 atti in 18 minuti di orologio, 0,6 ore-subagente, 56 notizie candidate, 0 correzioni di fatto nei campioni, 1 toponimo da verificare); quota: finestra di 5 ore +3 punti, settimana +1, sessione principale compresa; ripresa dopo chiusura del turno dimostrata, dopo ritiro della VM rinviata; calendario centrale 3–4 giorni, prudente 6–7; costi esterni con lettura dentro Max ≈ 78 € con le commissioni, ≈ 21 € senza; piano a cinque giorni con due consegne (17 e 20 settembre) in §9.6.
- **Aggiornamento del 15 settembre, sera (§8)**: ricostruzione una tantum con esecuzione e verifiche a carico di Operator e Codex; owner solo per accessi, autorizzazioni, decisioni non risolvibili e valutazione finale (≈ 2,5–3 ore); calendario minimo di 2,5–3,5 giorni di orologio dai prerequisiti in esercizio continuo, allungabile fino a 2–3 settimane solo dalla quota del piano, che da qui non è visibile (§8.4; le "5 ore al giorno" erano un'ipotesi organizzativa, non un vincolo); costo centrale ≈ 91 € (≈ 33 € entro il residuo rinviando la trascrizione delle commissioni RomaTV); strumenti di verifica accertati e limiti dichiarati in §8.1.

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
5. **Audio RomaTV**: dalle 17:09 gli host media rispondono; gli stream audio-only HLS sono cifrati AES-128 con chiave sull'host API (letta) e si scaricano a segmenti con `curl` (il Consiglio del II del 18 giugno: 200 segmenti, 23,9 MB, 145–192 secondi; la Commissione Permanente II del 3 giugno: 178 segmenti, 24,9 MB, 204 secondi). Rimontati in locale con `ffmpeg` statico: durate uguali al catalogo (1.991 e 1.770 secondi), il Consiglio con 27 secondi di silenzio in tutto e la commissione con 212 secondi di silenzio su 1.770 (12%): parlato presente e trascrivibile. Terzo stream, il Consiglio del XV del 30 giugno (82 minuti, 59 MB): durata uguale al catalogo e nessun silenzio sotto −35 dB, quindi i 24 minuti senza parole nella trascrizione sono la sospensione con rumore d'aula, non un taglio. Dettagli nel rapporto video §5.
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

> Superata dall'indicazione dell'owner della sera del 15 settembre: le verifiche del campione passano all'Operator e ai controlli di Codex (§8). La sezione resta come riferimento delle quantità e dei minuti per unità.

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

## 8. Preventivo aggiornato (15 settembre, sera): ricostruzione una tantum con esecuzione a carico di Operator e Codex

Indicazione dell'owner: la ricostruzione di giugno è **una tantum** e serve a validare fonti, copertura, qualità, complessità e costi; le proiezioni a regime (§3.6) restano un risultato dello studio, non un processo da avviare. Recupero, lettura, classificazione, collegamenti, deduplicazione, localizzazione e verifiche documentali sono a carico dell'Operator, con controlli indipendenti di Codex; all'owner restano accessi e autorizzazioni indispensabili, decisioni editoriali non risolvibili e valutazione finale. Nessuna ora di controllo è assegnata all'owner; ciò che non è verificabile è dichiarato come limite. Questa sezione sostituisce §3.4 (riga dell'owner), §3.4.1 e §3.5 per la ripartizione e i tempi; i costi in denaro di §3.3 non cambiano, perché il lavoro passa da una persona a un'altra, non da un servizio a un altro.

### 8.1 Strumenti di verifica accertati (M, 15 settembre)

| Materiale | Strumento utilizzabile qui | Cosa verifica | Limite dichiarato |
|---|---|---|---|
| Scansioni A2 (≈ 1.400 pagine) | **Tesseract 5.3.4 con lingua italiana** (installato oggi dai repository di sistema): 2,9 s a pagina a 300 dpi, spaziatura conservata, testo leggibile; **RapidOCR** (PyPI) come secondo motore indipendente: 5,3 s a pagina, perde spazi e righe nelle pagine dense | accordo fra i due motori (su 5 pagine di prova: dal 63% al 97% delle parole di Tesseract ritrovate nel testo di RapidOCR, in media 80%; `ocr_confronto_tesseract_rapidocr.json` su Drive); coerenza con i metadati dell'API (oggetto, data, numero di verbale); lettura di Codex su un campione di pagine con il testo OCR a fronte | nessuna lettura umana della scansione; le pagine in disaccordo fra i motori sono marcate "OCR incerto" e non contano come verificate |
| Trascrizioni RomaTV dei Consigli (82) | confidenza per parola del riconoscimento della piattaforma (letta per tutte); controlli acustici sull'audio scaricato (durata, silenzi, livello); coerenza documentale con verbali e convocazioni (ordini del giorno, esiti dei voti); con la chiave confermata: **seconda trascrizione indipendente via API su un campione di passaggi** (2 ore di audio ≈ 1 €) e tasso di accordo parola per parola | qualità media e per registrazione; passaggi con accordo basso marcati "trascrizione incerta" | nessun ascolto umano: nessuna trascrizione è "verificata all'ascolto"; senza chiave manca il confronto indipendente |
| Commissioni RomaTV (305 + 75 + 23) | audio scaricabile (provato su 3 registrazioni); trascrizione solo via API con la chiave (oppure alternativa sul PC dell'owner, da valutare a parte) | come sopra sulla trascrizione ottenuta | senza chiave: solo metadati e ordini del giorno (MMC, CPC); contenuto non ricostruibile |
| Sottotitoli YouTube (131) | nessun accesso all'audio (`googlevideo.com` bloccato): niente controlli acustici né seconda trascrizione; coerenza documentale con i verbali (nel Municipio I ogni verbale cita il video: presenze, orari, voti) e con le convocazioni | coerenza di date, organi, esiti | **limite**: i sottotitoli YouTube non sono verificabili sull'audio in questo ambiente; restano "testo indicativo" con coerenza documentale |
| Estrazione AI (schede e notizie candidate) | seconda AI su tutte le candidate (schema T4); controllo documentale dell'Operator sul campione del metodo §4.3 (100 candidate, 30 coppie, 40 localizzazioni, 20 disponibilità); controllo indipendente di Codex sullo stesso campione con le evidenze | fatto presente nell'evidenza, luogo, date, classi | i casi di disaccordo restano "candidata non confermata" |

### 8.2 Perimetro di giugno completabile

| Livello | Fonti e materiali | Condizione |
|---|---|---|
| **Completo, a 0 €, con gli strumenti attuali** | A1 365; A2 municipali 1.426 (testo per 8 Municipi, OCR Tesseract per 7); DDS 921 con estrazione a regole (vie, date di validità); atti centrali 46; Cronaca 109; E2 407 e stock futuro; E3 104; RomaTV: metadati di tutte le 496 voci e trascrizioni degli 82 Consigli con confidenza; YouTube: metadati e sottotitoli automatici di tutti i 131 (ciclo lento, ≈ 4 ore macchina); sedute collegate (convocazione, verbale, registrazione, avviso); database e misure di disponibilità online | nessuna |
| **Completo solo con chiave e autorizzazione** | testo delle commissioni RomaTV (280 ore: 10 Municipi senza YouTube più le Commissioni Capitoline) via API, ≈ 46 €; estrazione AI di tutto il perimetro e seconda AI sulle candidate, ≈ 24 € più ripetizioni | chiave OpenAI confermata; spesa oltre il residuo autorizzata |
| **Senza chiave: lettura umana parziale** | con circa 50 ore dell'Operator si leggono per intero A1, Cronaca, atti centrali, DDS a regole, delibere, mozioni, risoluzioni e determinazioni municipali (≈ 400 atti) e i 22 Consigli e commissioni già letti; i verbali di commissione (407), gli 82 Consigli RomaTV e i 131 video YouTube si leggono a campione (≈ 1 su 4); il resto è "non letto" e dichiarato | perimetro dichiarato come parziale |
| **Probabile, da confermare** | E1: API raggiungibile, formato dei filtri da individuare (1–2 ore); "altro" di RomaTV (23 registrazioni senza titolo, da classificare) | — |
| **Escluso, con motivazione** | Assemblee Capitoline (78 ore, livello cittadino coperto da ACD/AY); C3, C5, C6, R1 (0–2 item); Facebook (non ricostruibile a posteriori: DEC-102) | decisione dell'owner |

### 8.3 Ore di lavoro e di elaborazione (S; scenario centrale con chiave)

| Voce | Ore | Note |
|---|---|---|
| Operator: raccolta residua e conversioni (PDF, OCR, sottotitoli, audio, cicli di trascrizione) | 6 | script già scritti in gran parte; supervisione dei cicli |
| Operator: database (schema, chiavi, caricamento, collegamento sedute e parti, vicende) | 8 | struttura in §2.3 |
| Operator: estrazione AI (schema delle schede, prompt, cicli, controllo del 10% degli esiti) | 12 | ≈ 400 schede controllate a 1–2 minuti |
| Operator: deduplicazione, localizzazione, consolidamento delle candidate | 6 | regole del metodo §4.1; gazetteer |
| Operator: verifiche documentali del campione (100 candidate, 30 coppie, 40 localizzazioni, 20 disponibilità; OCR e trascrizioni con gli strumenti di §8.1) | 8 | le quantità di §3.4.1 passano all'Operator |
| Operator: rapporto finale, risposte ai controlli di Codex, correzioni | 8 | — |
| Operator: riserva per errori e ripetizioni (15%) | 7 | — |
| **Operator, totale** | **≈ 55** (tetto prudente; 35–40 alla velocità di sessione misurata, §8.3.1) | ore di attività della sessione, non ore di una persona; senza chiave ≈ 50 ore su un perimetro più piccolo (§8.2) |
| Elaborazione macchina, in parallelo con l'Operator | 20–60 h di orologio (S da tassi M) | scaricamento audio delle commissioni (280 h): 4–24 min per ora di audio misurati su 3 registrazioni (la misura lenta è avvenuta durante prove in parallelo e con errori di rete ripetuti), cioè 26–110 h in sequenza e ≈ 10–45 h con 4 scaricamenti in parallelo (×2,6, M), ripresumibile a segmenti; trascrizione API in coda allo scaricamento: 4–9 h con richieste concorrenti, fino a 35 h in sequenza (S: il tasso reale lo misura T1); OCR di 1.400 pagine ≈ 1 h su 4 CPU (M: 2,9 + 5,3 s a pagina); sottotitoli dei 116 video YouTube residui ≈ 10 h in un solo flusso (M: 78 min per 15, controllo anti-bot); cicli AI sincroni 3–6 h (S); con il Batch (costo −50%) ogni ciclo può richiedere fino a 24 h (S, dichiarato dal fornitore). I processi in background continuano fra un turno e l'altro finché la VM è attiva (M, oggi: ciclo dei sottotitoli 15:41–16:38 attraverso due turni) e si perdono solo con il ritiro della VM per inattività (§8.4) |
| Codex: controlli indipendenti | 5 controlli | (1) schema del database e regole di collegamento prima dell'estrazione; (2) campione di 100 candidate con evidenze; (3) campione di deduplicazione e localizzazione; (4) consegna finale (rapporto, aggregati, lacune); (5) revisione della PR del rapporto |
| Owner | ≈ 2,5–3 | solo §8.6 |

### 8.3.1 Su quali misure poggiano le 55 ore

Le 55 ore sono ore di attività della sessione dell'Operator (chiamate agli strumenti, lettura, scrittura), non ore di una persona e non ore di orologio. La base, voce per voce (orari in ora italiana):

| Voce di §8.3 | Ore | Base | Misura (M) o ipotesi (S) |
|---|---|---|---|
| Raccolta residua e conversioni | 6 | S su tassi M | M: gli script di scaricamento, misura acustica e statistiche delle confidenze sono stati scritti e provati oggi in 41 minuti di sessione (17:09–17:50, tre registrazioni); il ciclo dei sottotitoli e il batch audio sono corsi in background. S: l'estensione a 280 ore di audio e 1.400 pagine con gli errori di rete visti oggi (curl 35 e 56, ffmpeg) |
| Database | 8 | S | nessuna misura diretta. Analogia M: censimento di due piattaforme video, incrocio con Atti Web e selezione del campione in circa 40 minuti. Il database ha 7 tabelle e circa 3.500 righe da caricare e collegare |
| Estrazione AI e controllo del 10% degli esiti | 12 | S | S: schema e prompt 2 h, cicli 2 h, ≈ 400 esiti controllati a 1–2 min l'uno. M, più veloce: oggi 11 registrazioni lette e schedate in 30 minuti di sessione, aggiornamento della nota compreso (≈ 3 min l'una) |
| Deduplicazione, localizzazione, consolidamento | 6 | S | regole del metodo §4.1 e gazetteer; nessuna misura di sessione |
| Verifiche documentali del campione | 8 | S | 190 unità (100 candidate, 30 coppie, 40 localizzazioni, 20 disponibilità) a ≈ 2,5 min l'una. M parziale: 4 verifiche di nomi e 12 di date fatte oggi dentro le analisi, senza tempo separato |
| Rapporto finale, risposte a Codex, correzioni | 8 | S | M: questa nota (≈ 9.000 parole) è stata scritta in 39 minuti di sessione (17:08–17:47) e aggiornata tre volte in 6–16 minuti; il 14 settembre i cicli 2 e 3 della revisione Codex del piano (revisione e correzioni) si sono chiusi 5 e 4 minuti dopo il precedente (commit delle 17:56, 18:01 e 18:05) |
| Riserva 15% | 7 | S | convenzione |

Lettura: dove esiste una misura, la velocità di sessione è più alta di quella ipotizzata (≈ 3 minuti per registrazione contro i 6–13 impliciti nella voce dell'estrazione; una nota in 40 minuti contro 8 ore per il rapporto). Le 55 ore sono quindi un tetto prudente: alla velocità misurata oggi il lavoro vale **35–40 ore** di attività di sessione, e l'intervallo dichiarato diventa **35–55**. Il calendario di §8.4 usa il tetto; la differenza si registra a consuntivo nel ledger, non si promette.

### 8.4 Calendario minimo realistico, fondato sui vincoli dell'ambiente (aggiornamento delle 18:30)

**Da dove veniva "5 ore di sessione al giorno".** Era un'ipotesi organizzativa mia, modellata su una giornata di lavoro umana (una sessione per giorno lavorativo), non un vincolo tecnico né un limite del piano. La coincidenza con la finestra di cinque ore del piano (tabella sotto) è casuale: quella finestra limita il volume di utilizzo in cinque ore mobili, non la durata delle sessioni. Il calendario che segue non assume una giornata lavorativa.

**Vincoli verificati oggi (M).**

| Vincolo | Natura | Evidenza |
|---|---|---|
| Durata massima di un turno o di una sessione | nessun limite documentato | pagina "Claude Code on the web" (letta oggi): nessuna durata massima dichiarata. Oggi: sessione attiva per 8 h 03 min su 8 h 03 min di orologio (10:22–18:25), 9 turni, turno più lungo 1 h 54 min, nessuna attesa dell'owner (i messaggi sono arrivati mentre lavoravo) |
| Ritiro della VM per inattività | tecnico, documentato | "Cloud sessions stop after a period of inactivity and the session's VM is reclaimed": la durata dell'inattività non è dichiarata; alla riapertura tornano la conversazione e il repository (riclonato dal branch), non i processi in background né lo scratchpad (script e file temporanei, 583 MB oggi) |
| Processi in background fra un turno e l'altro | tecnico, misurato | continuano finché la VM è attiva: ciclo dei sottotitoli 15:41–16:38 attraverso due turni; batch audio in background durante la scrittura di questa nota |
| Quota di utilizzo del piano | limite del piano, dimensione non visibile da qui | metadati di sessione: `rateLimitType: five_hour`, stato `allowed`, "extra usage" non in uso; nessun blocco nel log di oggi; consumo di oggi 1,40 M token in uscita e 94,8 M in lettura di cache, controvalore API 168 $ per 8 ore di attività. Quale frazione della quota (finestra di 5 ore e settimana) sia stata consumata oggi la vede solo l'owner nella pagina Utilizzo di claude.ai |
| Esecuzione in parallelo | tecnico, documentato e misurato | subagenti e sessioni parallele disponibili; "Running multiple tasks in parallel consumes more rate limits proportionately"; 4 scaricamenti in parallelo ×2,6 (M); 4 CPU, 15 GB di RAM, ≈ 30 GB di disco |
| Contesto della conversazione | tecnico, misurato | 1 M di token; oggi 4 compattazioni automatiche, ognuna perde dettaglio: lo stato del lavoro deve stare nei file (repository, Drive, ledger), non nella memoria della conversazione |
| Riavvio senza presidio | tecnico, disponibile | promemoria programmati verso questa stessa sessione (`send_later`, "delivery survives container restarts") e Routine a orario (intervallo minimo un'ora); il promemoria riapre la sessione anche dopo il ritiro della VM |
| Permessi | tecnico | modalità `auto`; oggi nessuna chiamata rifiutata o sospesa (log della sessione); una richiesta di conferma, se emergesse, ferma quel turno fino alla risposta dell'owner |
| Turno di Codex | misurato | chiamate API, non giornate: il 14 settembre i cicli di revisione del piano si sono chiusi a 4–5 minuti l'uno dall'altro, correzioni comprese; 0,10–0,21 € l'uno |

**Flussi in parallelo e percorso critico** (ore di orologio da t0; scenario centrale con chiave; chiamate AI sincrone; t0 = chiave confermata, scenario di spesa scelto, sei decisioni di perimetro prese).

| Flusso | Da → a (ore da t0) | Dipende da |
|---|---|---|
| M1 scaricamento audio delle commissioni (4 in parallelo), poi trascrizione API in coda | 0 → 10–45 → 14–50 | host consentiti (fatto), chiave; il tasso di scaricamento misurato varia da 4 a 24 min per ora di audio (n = 3) |
| M2 OCR delle scansioni; sottotitoli dei 116 video YouTube residui | 0 → 1; 0 → 10 | nessuna |
| O1 prove T1/T3/T4/T5 con prezzi misurati; schema del database e caricamento di ciò che esiste | 0 → 2 → 10 | chiave, scenario di spesa |
| C1 controllo Codex 1 (schema e regole) e correzioni | 10 → 11 | O1 |
| O2 estrazione AI sulle fonti testuali (macchina 2–4 h dentro le ore dell'Operator) | 11 → 17 | C1, M2 |
| O3 estrazione sulle trascrizioni; collegamenti, deduplicazione, localizzazione | 17 → 29, oppure dall'arrivo delle trascrizioni | M1 |
| M3 seconda AI sulle candidate | 29 → 30 | O3 |
| O4 verifiche documentali del campione; controlli Codex 2 e 3 in parallelo | 30 → 39 | M3 |
| O5 rapporto; controllo Codex 4; PR e revisione 5; correzioni | 39 → 48 | O4 |
| riserva (7 h) | → 55 | |

Il percorso critico è la sequenza O1–O5 (le ore di attività dell'Operator) finché M1 consegna le trascrizioni entro l'ora 17; se lo scaricamento va al tasso lento misurato, M1 diventa il percorso critico e O3 parte all'ora 45–50. Risultato in esercizio continuo, senza blocchi di quota:

| Caso | Ore di orologio da t0 | Giorni di calendario |
|---|---|---|
| tasso di scaricamento buono, tetto delle 55 ore | ≈ 55 | 2,5 |
| tasso buono, velocità di sessione misurata (35–40 h) | ≈ 40 | meno di 2 |
| tasso lento (M1 = 45 h di scaricamento) | ≈ 80 | 3,5 |
| trascrizione API una richiesta alla volta | + 20–30 | + 1 |
| Batch API (costo AI −50%, ≈ 12 € in meno) | + 24 per ciclo, 2 cicli | + 1–2 |

I subagenti possono accorciare O2–O4 dividendo letture e verifiche, senza ridurre l'utilizzo complessivo; li userei solo se la quota lo consente.

**Cosa allunga davvero il calendario.**

1. **La quota del piano**: è l'unico vincolo che può trasformare 2,5–3,5 giorni in settimane, e la sua dimensione non è visibile da qui. Regola di calcolo: se una giornata come oggi (8 ore di sessione, 168 $ di controvalore) consuma una frazione f della quota settimanale, le ore di sessione disponibili in una settimana sono 8/f.

| f (frazione della quota settimanale consumata da una giornata come oggi) | Ore di sessione a settimana | Calendario per 55 ore |
|---|---|---|
| 1/20 o meno | 160 o più | 2,5–3,5 giorni (esercizio continuo) |
| 1/7 | 56 | ≈ 1 settimana |
| 1/5 | 40 | ≈ 1,5 settimane |
| 1/3 | 24 | ≈ 2,5 settimane |

   Il valore di f si legge nella pagina Utilizzo di claude.ai dopo la giornata di oggi; senza quel dato non prometto meno di 2,5 giorni né più di 3 settimane. L'"extra usage" a pagamento resta fuori dai vincoli concordati (nessun servizio a pagamento senza decisione dell'owner).
2. **Le attese dell'owner**: t0 (chiave, scenario, sei decisioni: ≈ 70 minuti del suo tempo, ma il calendario parte quando arrivano); le 3–5 decisioni editoriali durante il lavoro non fermano gli altri flussi (l'item resta "in attesa" con un segnaposto) ma fermano la consegna se restano aperte; la valutazione finale.
3. **Il ritiro della VM**: ripartenza di M1 e M2 dai segmenti già scaricati (script ripresumibili), perdita al più di un'ora di lavoro macchina se lo stato è nei file. Prerequisito: gli script oggi vivono nello scratchpad (35 file) e vanno versionati nel repository prima di t0 (1 ora dell'Operator, dentro le 55).
4. **Errori di rete e di API**: visti oggi (curl 35 e 56, ffmpeg, timeout di PyPI); tentativi automatici e ripresa, nessuna ripartenza umana.

**Posso proseguire senza presidio?** Sì, a due condizioni verificate: (a) prima di chiudere ogni turno programmo il promemoria che riapre il successivo (strumento disponibile in questa sessione; oggi non è servito perché l'owner era presente); (b) lo stato del lavoro è nei file, così ogni ripresa parte dai file e non dalla memoria della conversazione.

| Interruzione | Effetto | Chi riavvia |
|---|---|---|
| fine del turno senza promemoria | fermo fino al messaggio successivo | Operator (promemoria programmato prima di chiudere) o owner |
| ritiro della VM per inattività | processi in background e scratchpad persi; conversazione conservata | Operator, al primo promemoria: riclona, riprende gli script dai file su Drive e nel repository |
| quota del piano esaurita (finestra di 5 ore o settimana) | il turno si ferma fino al reset; un promemoria che scatta durante il blocco non produce lavoro | reset automatico; una Routine oraria riprova da sola; se il blocco è settimanale decide l'owner (attendere, oppure l'"extra usage" a pagamento, oggi disattivato) |
| richiesta di permesso in modalità auto | quel turno attende la risposta | owner |
| decisione editoriale o autorizzazione | l'item resta in attesa; gli altri flussi continuano | owner |
| errore di rete, di API o di script | il ciclo si ferma o salta l'item | Operator (tentativi automatici, ripresa dai segmenti) |
| compattazione del contesto | nessun fermo; perdita di dettaglio della conversazione | nessuno: si riparte dai file |
| sessione archiviata, ambiente modificato, rete negata | fermo completo | owner |

### 8.5 Da cosa derivavano le 3–4 settimane e le "5 ore al giorno", e cosa resta

Erano tutte ipotesi organizzative, nessuna tecnica: (a) una sessione dell'Operator per giorno lavorativo (le "5 ore"); (b) un giorno di attesa per ogni turno di Codex, che invece dura minuti; (c) la verifica a campione dell'owner distribuita sulla terza e quarta settimana (§3.4.1, oggi caduta); (d) il gate della chiave fra le prove e il mese, che ora sta dentro le prime due ore del calendario. Tolte le ipotesi, restano tre cose reali: le ore di attività dell'Operator (35–55, §8.3.1) come percorso critico; la quota del piano come unico vincolo che può allungarlo a settimane; gli interventi dell'owner a t0 e alla consegna (§8.7). Risultato: **2,5–3,5 giorni di orologio in esercizio continuo**, fino a 2–3 settimane se la quota consente una giornata come oggi ogni due o tre giorni. Il tempo macchina allunga il calendario solo nel caso del tasso di scaricamento lento (§8.4).

### 8.6 Costo, controlli Codex compresi (S)

| Voce | Senza chiave | Centrale entro il residuo | Centrale | Alto |
|---|---|---|---|---|
| Trascrizione commissioni RomaTV | 0 (escluse) | 0 (escluse, rinviate) | 46 | 106 |
| Estrazione AI | 0 | 10 | 10 | 57 |
| Seconda AI sulle candidate | 0 | 14 | 14 | 20 |
| Seconda trascrizione di verifica (campione, 2 h) | 0 | 1 | 1 | 2 |
| OCR (Tesseract e RapidOCR locali) | 0 | 0 | 0 | 0 |
| Ripetizioni ed errori (+25% sulle voci AI) | 0 | 6 | 18 | 46 |
| Controlli Codex (5, da 0,2 a 0,7 € l'uno secondo i token) | 2 | 2 | 2 | 4 |
| **Totale una tantum** | **≈ 2 €** | **≈ 33 €** (dentro i 49,14 € residui) | **≈ 91 €** | **≈ 235 €** |

Lo scenario "centrale entro il residuo" fa tutto tranne il testo delle commissioni RomaTV, che resta la lacuna dichiarata più grande (10 Municipi senza YouTube); la trascrizione può essere autorizzata dopo, con i prezzi misurati dalla prova T1.

### 8.7 Interventi che restano indispensabili da parte dell'owner

| Intervento | Quando | Tempo (S) |
|---|---|---|
| Conferma scritta o rotazione della chiave OpenAI (S0-03); io eseguo la prova funzionale | t0 | 30 min |
| Scelta dello scenario di spesa (§8.6) e autorizzazione oltre il residuo, se serve | t0 | 10 min |
| Sei decisioni di perimetro (§7, punti 3–5) con i pacchetti di una pagina già pronti | t0 | 30 min |
| Decisioni editoriali non risolvibili dal metodo né dal confronto con Codex, emerse durante il lavoro (stima 3–5, con bozza di voce `decisions/`) | durante il lavoro (ore 10–40 del calendario di §8.4); non fermano gli altri flussi | 30–50 min |
| Valutazione finale: rapporto (riepilogo di due pagine più tabelle), esito dei controlli di Codex, lacune, decisione sui passi successivi | alla consegna (ora ≈ 50–80 da t0 in esercizio continuo) | 60 min |
| **Totale** | | **≈ 2,5–3 ore**, nessuna ora di verifica a campione |

Non richiesti e non conteggiati: ascolto di passaggi audio, lettura di scansioni, trascrizione sul PC dell'owner (alternativa da valutare a parte, §3.4.1).

### 8.8 Consegna

Un database consultabile (foglio Google e CSV in `QN Hub / 20 Packages / Fonti 2026-06/`, schema di §2.3, senza nomi di persona né testi integrali) e un rapporto finale nel repository (`docs/sources/RICOSTRUZIONE_2026-06_RAPPORTO.md`) con: copertura per quartiere e settimana, contributo per fonte, duplicazioni, tempestività con la distinzione fra "disponibile a giugno" e "documentato dopo", affidabilità misurata (confidenze, accordo OCR, accordo fra trascrizioni, esito delle verifiche), ore e costi registrati nel ledger, raccomandazioni per fonte e le lacune dichiarate (almeno: commissioni RomaTV senza testo se non trascritte; sottotitoli YouTube non verificati sull'audio; nessun ascolto umano; Facebook assente; E1 se non conteggiata). I controlli di Codex sono archiviati in `reviews/`. Questa sezione aggiorna il preventivo e non autorizza la spesa per il mese.

## 9. Configurazione Opus 5 con Codex verificatore (richiesta dell'owner del 15 settembre, sera): valutazione e lotto di misura

Stato: **preliminare**, in attesa delle misure del lotto (§9.3). Perimetro, criteri di qualità, budget esterno e prerequisiti restano quelli di §8; questa sezione non autorizza spese né "extra usage".

### 9.1 Cosa cambia con Opus 5 e cosa no

| Aspetto | Fable 5.1 (oggi) | Opus 5 (proposta) | Base |
|---|---|---|---|
| Modello che esegue | `claude-fable-5-1` | `claude-opus-5` (contesto 1 M, thinking adattivo) | M: tabella dei modelli di riferimento (24 giugno 2026) |
| Prezzo API di listino per milione di token, ingresso / uscita | 10 $ / 50 $ | 5 $ / 25 $ | M: stesso riferimento. **Non è il peso sulla quota Max**: il rapporto fra i due modelli sulla quota lo misura solo il lotto, con le letture della pagina Utilizzo |
| Quota di utilizzo | condivisa a livello di account: finestra di 5 ore e limite settimanale, valori non visibili da qui | uguale: stessa quota, che conta anche ciò che Fable e le altre sessioni hanno già consumato | M: documentazione ("shares rate limits with all other Claude and Claude Code usage within your account") |
| Velocità per item | ≈ 3 min per registrazione letta e schedata; 39 min per una nota di 9.000 parole (M, oggi) | non assunta: misurata dal lotto, anche sui 2 item di taratura già letti da Fable | lotto |
| Qualità | nel campione video: 2 errori su 4 nomi, 12 date su 12 corrette (M) | misurata dal lotto: differenze sui 2 item di taratura, controlli documentali sui nuovi | lotto |
| Verificatore | Codex, 5 controlli, 0,10–0,21 € l'uno | invariato | — |
| Vincoli d'ambiente (§8.4) | ritiro della VM, compattazioni, promemoria, permessi, quota | identici | — |
| Modalità operativa consigliata | sessione attuale (contesto usato al 78%) | **nuova sessione su Opus 5** avviata dai file del repository, non un cambio di modello in corsa: contesto pulito e misura netta della quota | S |

### 9.2 Protocollo del lotto rappresentativo (attività già autorizzate, 0 € di costi esterni)

- **Lotto A**: 10 trascrizioni di Consigli municipali RomaTV (8 nuove, sedute diverse di 8 Municipi; 2 di taratura già lette da Fable: Municipio II del 18 giugno e Municipio VIII del 4 giugno), 44.860 parole; schede nel formato di §6 della nota video più un JSON per registrazione con evidenze `[mm:ss]`.
- **Lotto B**: 30 atti di Atti Web dal campione di 120 (17 di testo, 13 scansioni con OCR Tesseract), stratificati: 12 verbali di commissione, 10 fra delibere, mozioni e risoluzioni, 4 convocazioni, 4 determinazioni e atti di Giunta; classificazione con le colonne dell'approfondimento di stamattina più notizia candidata ed evidenza di pagina.
- **Esecuzione**: due subagenti Opus 5 in parallelo dentro questa sessione, che registrano il modello dichiarato dal proprio system prompt, i tempi per item e i problemi; specifica e manifesti in `tools/sources-study/lotto_opus5/`.
- **Misure**: item completati e tempo di orologio per lotto; errori e correzioni trovati dall'Operator con controlli documentali (differenze sui 2 item di taratura; 10 evidenze temporali e 10 pagine verificate a campione); tempi macchina (conversione JSON→testo 3,2 s per 83 trascrizioni, estrazione del testo 1,1 s per 17 atti, OCR misurato per file); attese; **quota: valori della pagina Utilizzo forniti dall'owner prima e dopo il lotto, non dedotti dal controvalore dei token**.
- **Ripresa senza presidio**: promemoria programmato alla chiusura del turno che precede il lotto; ora di programmazione, ora di arrivo e prima azione eseguita registrate in §9.3.

### 9.3 Risultati del lotto (M, 15 settembre, 18:49–19:09 ora italiana)

**Ripresa senza presidio.** Promemoria programmato alle 18:47:10 per le 18:52, accodato alle 18:52:47 e lavorato alle 18:53:22 senza alcun intervento dell'owner: la ripresa **dopo la chiusura del turno** è dimostrata. La ripresa **dopo il ritiro della VM** non lo è: la VM è rimasta attiva per tutto il pomeriggio. Prova programmata: promemoria alle 07:00 del 16 settembre, dopo una notte di inattività; l'esito (VM ritirata o no, scratchpad presente o perso, ripresa riuscita o no) va registrato qui prima di contare quella ripresa nel calendario.

**Lavoro completato.**

| Misura | Lotto A: 10 Consigli RomaTV | Lotto B: 30 atti di Atti Web |
|---|---|---|
| Modello dichiarato dal subagente | Opus 5, `claude-opus-5` (1 M) | Opus 5, `claude-opus-5` (1 M) |
| Materiale | 44.860 parole di trascrizione | 17 testi, 13 scansioni con OCR |
| Orologio, dalla prima all'ultima azione | 1.067 s (17,8 min) | 1.073 s (17,9 min), in parallelo con A |
| Tempo sommato per item | 815 s: da 70 a 104 s l'uno | 748 s: da 14 a 42 s l'uno, mediana 25 |
| Item completati | 10 su 10 | 30 su 30 |
| Notizie candidate | 38 (11 alte, 23 medie, 4 basse) | 18 (10 alte, 6 medie, 2 basse) |
| Token del subagente, chiamate agli strumenti | 267.633, 51 | 248.387, 60 |
| Tempo macchina a monte | conversione delle 83 trascrizioni 3,2 s | estrazione del testo 1,1 s; OCR di 13 scansioni ≈ 2 min |

**Qualità** (controlli dell'Operator su Fable, eseguiti dopo la lettura "dopo" della quota):

- Taratura, Consiglio del Municipio II del 18 giugno: le 5 notizie candidate di Opus sono tutte presenti nella lettura di Fable di oggi (chioschi ed emendamento sul parco Don Baldoni; chiusura notturna di Villa Leopardi, Villa Paganini e Villa Mercede da gennaio con Villa Chigi esclusa; recinzione del parco Don Baldoni dopo sei anni; orario dei chioschi; Consulta del Verde non interpellata). Nessuna contraddizione.
- Taratura, Consiglio del Municipio VIII del 4 giugno: 3 notizie su 3 coerenti (stanza per il centro anziani dei Granai di Nerva in una scuola; intitolazione di un luogo al fondatore di un club di via Libetta, 15 favorevoli; appello a scegliere il luogo insieme). Un toponimo diverge: la via della scuola è "via Dazio Molari 250" per Opus e "via Tazio Nuvolari 250" per Fable, storpiatura del riconoscimento vocale; nessuna delle due letture è verificata, il gazetteer non contiene le vie: **toponimo da verificare**.
- 10 evidenze temporali a campione nel lotto A: 7 esatte alla riga citata, 3 approssimate (il marcatore indica l'inizio del passaggio, non la frase: effetto dei blocchi di 30 secondi scelti dall'Operator nella conversione, non del modello). Nessuna evidenza inventata.
- 10 atti a campione nel lotto B: 10 su 10 coerenti con la pagina citata per oggetto, luoghi e date.
- Nomi di persona: nessuno negli output (controllo con grep sui nomi presenti nelle trascrizioni e nelle pagine, che i subagenti avevano sotto gli occhi).
- Segnalazioni spontanee dei subagenti: 5 contraddizioni lasciate aperte nel lotto A (un conteggio di voto, due date, un orario, un oggetto illeggibile), 3 registrazioni interrotte prima del voto con notizie declassate, 7 incoerenze interne negli atti, 8 scansioni su 13 con OCR incerto: dichiarare senza risolvere, come chiede il metodo.
- Correzioni necessarie trovate nei campioni: **0 di fatto**, 1 toponimo da verificare, 1 regola da cambiare (marcatori a 10 secondi, o doppio marcatore, nella conversione delle trascrizioni). Un secondo controllo indipendente di Codex sul lotto costerebbe ≈ 0,2 € e resta a disposizione dell'owner.

**Durata a confronto.** 40 item in 18 minuti di orologio con due subagenti in parallelo. Fable oggi: ≈ 3 minuti per registrazione letta e schedata, nota compresa (misura non identica: Fable faceva anche l'incrocio con Atti Web e A1 e scriveva la nota). Il rapporto misurato per item, 81 s contro ≈ 180 s, non va letto come "Opus è due volte più veloce": i compiti non coincidono e Opus non ha svolto l'incrocio con gli atti (il CSV locale non ha l'oggetto).

**Variazione della quota** (pagina Utilizzo, granularità di 1 punto; nessun reset fra le due letture; crediti 0 €):

| Riga | Prima (18:50) | Dopo (19:12) | Variazione |
|---|---|---|---|
| Sessione corrente (finestra di 5 ore, reset 20:20) | 40% | 43% | +3 |
| Questa settimana (tutti i modelli) | 2% | 3% | +1 |
| Fable questa settimana (limite separato) | 4% | 5% | +1 |

Attribuzione (corretta il 15 settembre sera su rilievo dell'owner): i due subagenti hanno lavorato 17,8 e 17,9 minuti, cioè **0,6 ore-subagente in tutto**, non 1,2. La variazione comprende anche i 4 turni brevi della sessione principale su Fable (8 chiamate agli strumenti, nessuna lettura dei risultati), che con questa granularità non sono separabili: il punto in più della riga Fable può essere arrotondamento oppure quell'attività. Quindi: **al più 2–4 punti della finestra di 5 ore per 0,6 ore-subagente** (3,3–6,7 punti per ora-subagente, centrale 5, tetto perché una parte spetta alla sessione principale) e **0–2 punti settimanali**, non risolvibili. I consumi successivi alla seconda lettura (controlli dell'Operator su Fable, caricamenti su Drive, questa nota) **non sono misurati** e non vanno attribuiti al lotto. Fable, per confronto: 40 punti della finestra in 3,5 ore di sessione principale (11,4 per ora), ma con un contesto di 250–800 k token riletto dalla cache a ogni chiamata; i subagenti partono con un contesto piccolo. Il rapporto di 4–5 volte mescola il prezzo del modello e la dimensione del contesto: **non è il "peso di Opus"**. Contatori di sessione, tutti i modelli: +171.516 token in uscita, +19,9 M letti dalla cache, +17,19 $ di controvalore API (registrato, non usato per la quota).

Conversione dalla finestra alla settimana: per Fable, 2 punti settimanali contro ≈ 96 punti-finestra nella giornata (rapporto ≈ 48 a 1). Applicato a Opus: ≈ 0,1 punti settimanali per ora-subagente; se invece i punti settimanali in più fossero tutti reali e tutti di Opus, da 1,7 a 3,3. La forbice si chiude solo con una lettura dopo la prima giornata piena di lavoro su Opus, che per questo è un checkpoint vincolante del piano (§9.6).

### 9.4 Preventivo con Opus 5: incluso in Max e costi esterni

| Voce | Incluso nell'abbonamento Max 20× | Costo esterno (€, S, invariato da §8.6) |
|---|---|---|
| Attività dell'Operator su Opus 5 (35–55 ore di sessione), subagenti compresi | sì, dentro la quota | 0 |
| Verifiche documentali, rapporto, database | sì | 0 |
| Trascrizione API delle commissioni RomaTV (280 h) | no | 46 nello scenario centrale; 0 se rinviata |
| Estrazione AI e seconda AI sulle candidate | no | 24 |
| Ripetizioni ed errori | no | 18 |
| Controlli Codex (5) | no | 2 |
| **Totale esterno** | | **≈ 91** centrale; ≈ 33 entro il residuo; ≈ 2 senza chiave |

Nessun "extra usage": il limite di lavoro è la quota inclusa; quando è esaurita si aspetta il reset.

### 9.5 Calendario aggiornato con le misure del lotto: previsione centrale e prudente

Le equivalenze di §8.4 fra quota giornaliera e giorni necessari sono superate dalle misure: con Opus 5 la quota non è il vincolo che governa il calendario, entro due regole operative (sotto). Il calendario si costruisce sui tassi misurati per item, sul parallelismo e sui flussi macchina.

**Volumi del perimetro centrale con chiave, al tasso misurato (S da M):**

| Attività | Quantità | Tasso (M, lotto) | Ore-subagente Opus |
|---|---|---|---|
| Lettura e schedatura delle registrazioni: 82 Consigli RomaTV, 131 YouTube, ≈ 380 commissioni RomaTV trascritte | ≈ 590 | 81 s l'una (Consigli di 30–65 min); le commissioni durano fino a 2–3 ore: ×1,5 | ≈ 20 |
| Classificazione dei documenti: A2 1.426, DDS 921, A1 365, Cronaca 109, E2 407, E3 104, centrali 46 | ≈ 3.400 | 25 s l'uno (atti); DDS, A1, E2, E3 più semplici | ≈ 18–24 |
| Riserva per item lunghi, errori, ripetizioni | +30% | S | ≈ 12–13 |
| **Totale lettura e classificazione** | | | **≈ 50–57**, in parallelo su 2–3 flussi: **≈ 17–28 ore di orologio** |

Lavoro della sessione principale, sequenziale (S, invariato da §8.3 salvo l'estrazione, che passa ai subagenti): database 8, collegamenti, deduplicazione e localizzazione 6, verifiche documentali del campione 8, rapporto e risposte a Codex 8: **30 ore**, più i turni di Codex (minuti).

**Percorso critico da t0** (t0 = chiave confermata, scenario scelto, sei decisioni prese):

| Ore da t0 | Sessione principale | Subagenti Opus (≤ 3 in parallelo) | Macchina |
|---|---|---|---|
| 0 → 10 | prove T1/T3/T4/T5 con la chiave (2 h); database (8 h) | fonti testuali: ≈ 24 ore-subagente in 8–12 ore | scaricamento audio (10–45 h) e trascrizione in coda; OCR (1 h); sottotitoli (10 h) |
| 10 → 30 | controllo Codex 1; collegamenti, deduplicazione, localizzazione (6 h) | Consigli RomaTV e YouTube subito (≈ 5 ore-subagente); commissioni man mano che le trascrizioni arrivano | trascrizioni complete fra l'ora 14 e l'ora 50 secondo il tasso |
| 30 → 46 | verifiche (8 h), controlli Codex 2 e 3; rapporto (8 h), controlli 4 e 5 | seconda lettura indipendente sulle candidate, se affidata a Opus | — |
| **≈ 46–50** | **consegna**, se le trascrizioni arrivano entro l'ora 30 | | |
| ≈ 75 | consegna con il tasso di scaricamento lento (trascrizioni all'ora 50, commissioni lette entro l'ora 58) | | |

**Previsioni** (giorni di calendario dai prerequisiti, esercizio continuo con promemoria, senza presidio):

| | Centrale | Prudente |
|---|---|---|
| Orologio di lavoro | 46–50 ore | 75 ore |
| Attese dell'owner (decisioni editoriali, valutazione) | ≤ 0,5 giorno | 1–1,5 giorni |
| Pause per quota, permessi, ritiro della VM | nessuna | 1 giorno |
| **Calendario** | **3–4 giorni** | **6–7 giorni** |

Confronto con le ipotesi dell'owner: la sua ipotesi centrale (5–7 giorni) coincide con la previsione prudente; il suo scenario favorevole (2–4 giorni) coincide con la centrale, che non scende sotto i 3 giorni perché le 30 ore della sessione principale sono sequenziali e la consegna aspetta le trascrizioni. Nessuna promessa di velocità: le due previsioni poggiano sui tassi del lotto, che vanno riconfermati alla fine della prima giornata piena (item lunghi, commissioni di 2–3 ore, quota).

**Regole operative che tengono la quota fuori dal percorso critico** (M/S, corrette con le 0,6 ore-subagente): al massimo **2 subagenti Opus in parallelo** oltre alla sessione principale (fino a 5 punti-finestra per ora-subagente ciascuno; sessione principale stimata 3–6 punti per ora con contesto piccolo, da misurare il primo giorno: insieme 13–16 punti per ora, 65–80 per finestra di 5 ore, quindi con margine ma senza spazio per un terzo flusso continuo); **lettura della pagina Utilizzo alla fine del primo giorno pieno** per fissare il consumo settimanale: la forbice attuale, da 0,1 a 3,3 punti per ora-subagente, vale fra 5 e 190 punti settimanali per le 50–57 ore-subagente del perimetro, e l'estremo alto supererebbe la settimana. Se la lettura del primo giorno indica più di 3 punti settimanali per ora-subagente, il parallelismo scende a un flusso e il calendario prudente diventa quello di riferimento; nessun "extra usage".

**Cosa può far slittare la consegna, in ordine di probabilità:**

1. Chiave OpenAI non confermata a t0: trascrizioni delle commissioni e seconda AI ferme; il calendario parte quando arriva.
2. Tasso di scaricamento lento dell'audio (misurato da 4 a 24 minuti per ora di audio): +1 giorno.
3. API di trascrizione che accetta una richiesta alla volta: +1 giorno.
4. Decisioni editoriali dell'owner aperte alla consegna: +1 giorno per ogni decisione non risolta (gli altri flussi non si fermano).
5. Toponimi da verificare più frequenti del previsto (1 su 8 candidate nella taratura): verifiche più lunghe, +0,5 giorno.
6. Ritiro della VM con scaricamento in corso: ripresa dai segmenti, al più 1 ora; se la prova del 16 settembre fallisse, riavvio manuale dell'owner (+ il tempo fino al suo intervento).
7. Richieste di permesso in modalità auto non risposte: il turno aspetta.
8. Quota settimanale: se il consumo reale per ora-subagente fosse all'estremo alto della forbice (§9.3), il lavoro non entra in una settimana e la consegna slitta al reset del martedì; la lettura del primo giorno lo dice per tempo.

**Costi esterni con la lettura dentro Max (corretti il 15 settembre sera).** Il lotto mostra che lettura e classificazione possono farle i subagenti Opus dentro l'abbonamento; ciò elimina la prima estrazione via API di OpenAI e le sue ripetizioni, e lascia esterni i servizi che Opus non può sostituire qui (trascrizione dell'audio) e quelli che devono restare indipendenti dal modello che ha letto (seconda AI sulle candidate, schema T4; controlli di Codex). La cifra di 67 € indicata in chat applicava la riserva del 25% alle sole voci AI: la cifra coerente con il metodo di §8.6, che applica il 25% a tutte le voci API, è 78 €.

| Voce (€, S) | Centrale con trascrizione | Entro il residuo (trascrizione rinviata) | Che cosa è |
|---|---|---|---|
| Prima estrazione via API (OpenAI) | 0, era 10 | 0, era 10 | **eliminata**: la fanno i subagenti Opus dentro Max |
| Trascrizione API delle commissioni RomaTV (≈ 228 h nelle tre settimane, 280 h nel mese) | 46 | 0 | resta esterna: Opus non trascrive l'audio in questo ambiente; rinviabile |
| Seconda AI indipendente sulle candidate (≈ 2.000, con le evidenze) | 14 | 14 | resta esterna per indipendenza dal modello che ha letto; chiave OpenAI necessaria |
| Seconda trascrizione di verifica (campione di 2 h) | 1 | 1 | resta esterna; chiave necessaria |
| Ripetizioni ed errori, 25% delle voci API | 15 | 4 | convenzione di §8.6 |
| Controlli Codex (5, da 0,2 a 0,7 € l'uno) | 2 | 2 | verifica indipendente; usa la chiave su disposizione dell'owner |
| **Totale esterno** | **≈ 78** | **≈ 21** | |

**Che cosa significa 21 €**: è il costo esterno della ricostruzione completa (Report 1 e Report 2) senza il testo delle commissioni RomaTV, che resta la lacuna dichiarata; sta dentro il residuo autorizzato di 49,14 € e non richiede un nuovo tetto, ma richiede la chiave OpenAI confermata per la seconda AI (14 €) e la verifica di trascrizione (1 €). Senza la chiave la spesa esterna scende ai soli controlli di Codex (2 €) e la seconda AI diventa una lacuna dichiarata: la verifica indipendente resta quella documentale di Codex sui campioni. **Tetto totale da approvare per l'esecuzione completa con le commissioni: 78 €**, cioè 28,86 € oltre il residuo. Nessuna spesa è autorizzata da questa nota.

### 9.6 Piano operativo a cinque giorni (16–20 settembre) e due consegne

**Avvio (t0)**: 16 settembre alle 07:00 ora italiana, con il promemoria già programmato. I cinque giorni finiscono il 20 settembre alle 19:00. Nella notte fra il 15 e il 16 girano i recuperi lenti, avviati la sera del 15 (19:30–19:40) e presidiati da un promemoria orario che tiene attiva la VM e riavvia ciò che si ferma: questo rinvia la prova di ripresa dopo il ritiro della VM, che si farà in una finestra senza job dopo il Report 1.

**Tre settimane per il Report 2, scelte ora, prima dell'analisi**: **8–28 giugno** (settimane intere da lunedì a domenica, W2–W4). Motivazione dai calendari e dalla disponibilità dei materiali (M, censimenti dell'intero mese, che restano disponibili):

| Settimana | Consigli RomaTV | Commissioni RomaTV (n, ore) | YouTube | Atti A2 | A1 |
|---|---|---|---|---|---|
| 1–7 giugno (festa del 2 giugno) | 9 | 68, 47,8 h | 25 | 295 | 82 |
| **8–14** | 18 | 93, 66,1 h | 38 | 356 | 91 |
| **15–21** | 26 | 115, 83,5 h | 29 | 354 | 88 |
| **22–28** | 23 | 110, 78,0 h | 31 | 346 | 87 |
| 29–30 (parziale) | 10 | 17, 10,0 h | 8 | 75 | 17 |

Le tre settimane centrali contengono il 78% dei Consigli, il 79% delle ore di commissione, il 75% dei video YouTube e il 74% degli atti; la prima settimana è spezzata dalla festività e l'ultima è di due giorni. Il Report 1 copre l'intero mese e viene anche filtrato sulle stesse tre settimane per il confronto.

**Consegne.**

| Consegna | Termine | Contenuto | Materiali |
|---|---|---|---|
| **Report 1: fonti testuali** | 17 settembre, 19:00 (giorno 2) | giugno intero e filtro 8–28 giugno: notizie candidate distinte (deduplicate fra fonti), copertura per Municipio e settimana, tempestività (data del fatto, pubblicazione, disponibilità), lacune; atti e video esclusi | A1 365, Cronaca 109, E2 407, E3 104, già in mano; E1 solo se il formato dei filtri si trova in al più 1 ora di tentativi |
| **Report 2: contributo di atti e video** | 20 settembre, 19:00 (giorno 5) | sulle tre settimane: informazioni nuove rispetto al Report 1, vicende approfondite, lacune colmate, difficoltà introdotte (OCR, trascrizioni, toponimi, sedute spezzate); confronto con il Report 1 filtrato | A2 1.056 atti e DDS delle tre settimane (PDF in scaricamento, testo e OCR locali), 67 Consigli RomaTV con trascrizione, 98 video YouTube (sottotitoli in recupero lento), 318 registrazioni di commissione RomaTV (audio in scaricamento; testo solo con chiave e tetto) |

Ogni consegna comprende: database consultabile (foglio e CSV in `Fonti 2026-06/`, schema di §2.3), rapporto nel repository con evidenze (pagina o `[mm:ss]`), esito dei controlli di Codex (2 per report, ≈ 0,2 € l'uno, su disposizione dell'owner), lacune dichiarate. Le decisioni editoriali residue arrivano all'owner raggruppate in un solo messaggio per report, con la scelta di default che applico se non risponde; nessuna ora di controllo manuale a suo carico.

**Recuperi lenti avviati la sera del 15** (ripresumibili; nessun cambio di IP, ritmi come nelle prove): sottotitoli YouTube dei 115 video senza testo, prima quelli delle tre settimane (86), un video al minuto con pause dopo due errori; PDF di Atti Web dei 2.669 atti di giugno (A2, DDS, centrali), prima le tre settimane (1.983), una richiesta ogni 1,3 secondi, poi estrazione del testo e OCR delle scansioni; audio RomaTV delle commissioni delle tre settimane, 4 scaricamenti in parallelo, in ordine di settimana.

**Prerequisiti a carico dell'owner** (nessuno blocca il Report 1): (1) conferma o rotazione della chiave OpenAI (S0-03): serve alla seconda AI, alla verifica di trascrizione e alla trascrizione delle commissioni; (2) tetto di spesa: 21 € entro il residuo, oppure 78 € con le commissioni; (3) disposizione dei controlli Codex (4, ≈ 1 €). Senza (1) e (2) il Report 2 esce lo stesso, sul perimetro ridotto dichiarato.

**Completabile entro il termine** (M/S): Report 1 intero; nel Report 2 gli atti delle tre settimane con testo e OCR, i 67 Consigli RomaTV, i video YouTube che il ritmo lento consente (stima 86 su 86 in 3–8 ore, se il controllo anti-bot non blocca), le convocazioni e i verbali delle commissioni RomaTV come metadati e ordini del giorno.
**A rischio**: il testo delle 318 commissioni RomaTV (chiave, tetto, 228 ore di audio da scaricare al tasso misurato di 4–24 minuti per ora: da 8 a 45 ore con 4 flussi; poi trascrizione API); i sottotitoli YouTube se l'anti-bot blocca (allora parziali e dichiarati); la seconda AI indipendente (chiave); E1 (formato dei filtri); il tempo di lettura delle commissioni lunghe (2–3 ore ciascuna).
**Consegnato comunque**: inventari dell'intero mese, database con i collegamenti fra convocazioni, verbali e registrazioni, i due rapporti con le lacune dichiarate e le etichette "non verificato" dove restano incertezze. Nessuna riduzione tacita del perimetro: ogni parte mancante è elencata nel rapporto con la causa.

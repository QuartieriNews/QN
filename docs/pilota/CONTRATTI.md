# Pilota: i contratti comuni dei workstream

Status: in vigore per DEC-031 (9 novembre 2026). Li fissa il coordinatore; un cambiamento
passa da una PR del coordinatore. Valgono per i quattro workstream: A Amministrazione,
B Notizie, C Eventi e D Storico.

## 1. Le pagine pilota

| Pagina | `publication_zone_id` | Municipio | Difficoltà |
|---|---|---|---|
| Acilia | `acilia` | X | difficile |
| Centocelle | `centocelle` | V | media |
| Prati | `prati` | I | facile |

Gli id sono quelli di `gazetteer/gazetteer.json`, che vince su tutto. Un elemento che
riguarda un'altra zona si registra con la sua zona vera, perché il sito può mostrarlo come
quartiere vicino (DEC-023, regola 4). Non si forza mai su una pagina pilota.

## 2. La forma di un elemento

**Si usa il contratto canonico del progetto, senza ridefinirlo.** I documenti elencati qui
vincono su questa pagina, che contiene solo i rimandi e le poche aggiunte del pilota.

| Che cosa | Dove è definito | Campi |
|---|---|---|
| Forma comune ai quattro blocchi | `gazetteer/gazetteer.json` → `editorial.cross_block_contract`; `docs/PROJECT_VISION.md` | un livello geografico, un campo di freschezza, una classificazione editoriale con valori propri del blocco |
| Geografia | `gazetteer/gazetteer.json` → `resolution.store`, `geo_basis_values`, `verification_status_values`; `prompts/PROMPT_GEO_BLOCK.md` | `publication_zone_id`; `neighbourhood_id` quando è noto in modo deterministico; `geo_level`; `municipality_code` (sempre, quando noto: è l'unica chiave a livello di municipio); `geo_basis`; `geo_verification_status`, dove `human_verified` ferma ogni ricalcolo |
| Classificazione editoriale | `gazetteer/gazetteer.json` → `editorial`; `prompts/EDITORIAL_FILTER.md` | `editorial_class` per ogni blocco delle pagine; per gli eventi anche `editorial_basis` e `content_type`. I valori per `institutional`, `news` e `conversation` sono un'estensione per blocco: si aggiungono con una PR del coordinatore prima che quel blocco abbia elementi. I record dello storico non hanno classificazione editoriale (qui sotto, «Lo storico») |
| Scarti e coda di revisione | `gazetteer/gazetteer.json` → `reject_reasons`, `review`; `docs/REVIEW_QUEUE.md` | `reject_reason` con i codici canonici e la loro regola `blocks_publication`. Quali elementi entrano nella coda di lavoro e quali vanno direttamente nell'archivio con `decision = auto_excluded` lo stabilisce `docs/REVIEW_QUEUE.md`; il pilota non lo ridefinisce |
| Eventi | specifica v2.5, fasi 1–2 (Drive, `QN Hub / 10 Specifications`); `code-nodes/` | `source_event_id` valido per DEC-027; `start_at_utc`, `end_at_utc`, `date_precision`; `source_hash` (`code-nodes/compute-source-hash.js`) |
| Freschezza | specifica v2.5, parte III | il campo con il nome della specifica; il pilota non ne inventa uno |

Il prototipo del sito (`tools/site/`) legge una proiezione più semplice (`start`, `end`,
`title`…). La ricava il codice che costruisce le pagine, e non si salva al posto dei campi
canonici. Le sue date sono date di Roma: ogni istante UTC si converte in `Europe/Rome` prima
di prenderne il giorno (la specifica ha già `timezone` e `local_date`), e il codice che lo fa
ha un test a cavallo del cambio dell'ora.

**L'identità di un elemento** è il `content_id` della specifica v2.5 (fase 2.1), lo stesso
che la coda di revisione usa come chiave. Per gli eventi da Facebook la sua forma è quella
della specifica, serie comprese. Per gli altri canali la forma del `content_id` e la
procedura di `source_hash` le fissa la PR del coordinatore che apre il canale, con i test di
idempotenza. Tre regole valgono da subito:
- la geografia e `registro_id` non entrano nel `content_id` (specifica, fase 2.1);
- il `content_id` identifica l'elemento pubblicato, non il record della fonte. Una
  registrazione può dare più notizie (`tools/sources-study/report2/SPECIFICA_VIDEO.md`,
  `notizie_candidate`), e lo stesso fatto raccontato da più testate resta un fatto solo
  (`docs/sources/CRONACA_PROCESSO_2026-10.md`, R-C01 e la fase di fusione con `fatto_id`).
  Gli id delle registrazioni e gli URL dei pezzi restano provenienza;
- quando il contenuto della fonte cambia, cambia `source_hash`, non il `content_id`.

**Le aggiunte e le convenzioni del pilota.** `block` e le colonne `source_*` sono colonne
canoniche della coda: qui si fissa solo come il pilota le riempie. Gli altri campi il
contratto canonico non li ha.

| Campo | Contenuto |
|---|---|
| `workstream` | `A`, `B`, `C` o `D` |
| `block` | la colonna canonica della coda (nel file canonico lo stesso valore sta in `stream`); il pilota usa `events`, `institutional`, `news` e `conversation`, i quattro blocchi di `docs/PROJECT_VISION.md`. Un record dello storico non ha `block` (qui sotto, «Lo storico») |
| `source_channel`, `source_id`, `source_url` | le colonne canoniche della coda, con il significato di `docs/REVIEW_QUEUE.md`: `source_id` è l'id che la piattaforma dà a chi pubblica (la pagina o il gruppo Facebook, il canale YouTube); per un sito, il suo host in minuscolo senza `www.`. I valori nuovi di `source_channel` arrivano con la PR del coordinatore che apre il canale |
| `registro_id` | l'id della fonte nel registro (`S-…`), quando c'è. Non sostituisce `source_id` e non entra in nessuna chiave |
| `archive_id` | quando l'elemento nasce da un record dello storico |
| `attribuzioni` | le testate e le fonti citate, ciascuna con un link (DEC-108) |
| `nomi` | le persone nominate, ognuna con la decisione che lo consente: DEC-105 per le fonti amministrative ufficiali, DEC-108 per la stampa (sezione 6) |
| `costo` | servizio, unità (minuti, eventi, token) ed euro, quando c'è una spesa |

`title` e il testo pubblicabile sono sempre scritti da noi. L'`excerpt` della fonte e gli
originali restano nello staging su Drive (sezione 3).

### Lo storico (workstream D)

Il workstream D non produce elementi delle pagine: produce i record dello storico,
l'archivio privato e in sola aggiunta di DEC-023 (regola 2). Un record non ha `block`, non
ha `content_id` e non entra nella coda di revisione. Quando un record serve a un elemento
pubblicabile, l'elemento nasce a parte, con il suo blocco e il suo `content_id`, e porta
l'`archive_id` del record.

| Campo | Contenuto |
|---|---|
| `archive_id` | stabile: `qn:roma:arc:<source_id>:<chiave>`, con il prefisso costante. Si costruisce da `source_id` e dalla chiave che la fonte dà al documento, normalizzati (Unicode NFC, spazi tolti ai bordi e ridotti a uno all'interno); mai dalla geografia né da `registro_id`. Per Atti Web la chiave è `<tipologia>:<idDoc>`, la coppia con cui il portale indirizza il PDF; una chiave di forma diversa ferma la lettura invece di diventare un id (`code-nodes/archive-record.js`, test di idempotenza e di normalizzazione in `tests/test_archive_record.js`) |
| `versione` | 1 alla prima scrittura (vedi la correzione, qui sotto) |
| `source_id`, `registro_id`, `source_url` | come per gli elementi |
| `data_documento` | la data dell'atto o della seduta, `YYYY-MM-DD` |
| `municipality_code` | il campo canonico della geografia, quando è noto |
| `tipo` | il tipo di documento. Per Atti Web è il codice della tipologia del portale, fra le 48 del menu al 15 settembre 2026, tutte lette per DEC-033 (`docs/sources/A2_ATTIWEB_TIPOLOGIE.md`, sezione 3, con le denominazioni): l'elenco sta in `code-nodes/archive-record.js`, e un codice fuori elenco ferma la lettura |
| `provenienza` | come il record è stato ottenuto: l'URL letto, l'ora della lettura (`retrieved_at`, UTC), il workflow `staging_` e la sua versione, la pagina dell'elenco salvata in `originali/` da cui viene la riga (`elenco`), e il campo della fonte da cui viene `data_documento` (`data_documento_da`) |
| `originale` | il percorso del file in `originali/`, che non si modifica mai: `originali/<radice>__<primi 16 caratteri dello SHA-256>.pdf`, dove la radice è l'`archive_id` senza `qn:` e con `__` al posto dei due punti |
| `originale_sha256` | lo SHA-256 dell'originale, che decide se una nuova lettura aggiunge una versione |
| `derivato` | il testo estratto o la trascrizione, con lo strumento e la versione che li hanno prodotti |
| `etichette` | le nostre etichette (zona, argomenti…), ciascuna con chi o che cosa l'ha messa |
| `costo` | come per gli elementi |

- **Correzione.** Niente si sovrascrive e niente si cancella. Una correzione è una versione
  nuova con lo stesso `archive_id`, la `versione` aumentata di uno e un campo `motivo`;
  vale la versione più alta. Una nuova lettura che trova lo stesso originale della versione
  più alta (lo stesso SHA-256 del file) non aggiunge versioni; un originale diverso ne
  aggiunge una, con il `motivo` «originale cambiato alla fonte».
- **Il file.** Un file JSON per versione, `D Storico/<radice>__v<versione>.json`, scritto una
  volta e mai riscritto; la versione più alta è quella che vale.
- **Copia di riserva.** Una volta alla settimana un job di copia duplica i file dello
  storico; nessun altro workflow scrive in `D Storico/riserva/`. In staging è
  `staging_D_riserva`, la domenica alle 4:41 di Roma, e cerca solo in «Il mio Drive».
  - **Record.** I record `__v<versione>.json` vanno in `riserva/<data>/`, con `<data>` il giorno
    di Roma. La copia del giorno è completa solo quando nella sua cartella c'è `COMPLETA.json`,
    scritto dopo l'ultima copia; un giro che trova la cartella senza quel file copia i record
    che mancano e poi lo scrive.
  - **Originali.** Ogni file di `originali/`, PDF degli atti e pagine della ricerca, si copia una
    volta sola in `riserva/originali/`: non cambia mai, e uno perso alla fonte non si potrebbe
    riavere. La copia porta nella descrizione l'id del file da cui viene, e un giro copia solo
    i file che lì non ci sono ancora.
  - **Una cartella sola.** Se due giri insieme creano due volte `riserva/`, la cartella del
    giorno o `riserva/originali/`, vale la più vecchia, che tutti e due riempiono; l'altra resta
    vuota.

**La lettura di Atti Web (DEC-033).** DEC-033 fissa perimetro, ritmo, stop e completezza; qui
c'è il modo di leggere il portale, che `code-nodes/archive-record.js` applica con i suoi test
(`docs/sources/A2_ATTIWEB_TIPOLOGIE.md` descrive il portale).
- **Tipologie.** All'inizio della lettura si legge l'elenco delle tipologie che il portale
  offre; se non si legge, la lettura non parte, e un codice che non è un valore di `tipo`
  la ferma finché una PR non lo aggiunge (`planTipologie`). La ricerca si fa una tipologia
  alla volta, perché il portale non filtra per struttura e anche le tipologie degli organi
  centrali contengono atti di strutture municipali (sezione 3, `ACD`).
- **Periodo.** Il filtro è la data di repertorio (`dtRpr`), l'unico che il portale accetta,
  dal 1° dicembre 2025 al giorno della lettura: il mese in più serve alle convocazioni
  protocollate prima di una seduta di gennaio.
- **Pagine e passate.** Per ogni tipologia le pagine si leggono da 500 righe fino al totale
  dichiarato. Il portale pubblica in ritardo (sezione 2), quindi ogni tipologia si legge due
  volte di seguito e vale quando le due passate danno lo stesso totale e lo stesso insieme di
  `idDoc`; altrimenti si legge ancora, fino a tre passate, poi la tipologia si scrive nel
  registro come incompleta (`mergePasses`). Le righe si uniscono per la coppia `tipologia` e
  `idDoc`, la stessa dell'`archive_id`: `idDoc` da solo non è unico fra le tipologie.
- **Risposta vuota.** L'errore «Index: 0, Size: 0» vale come tipologia vuota nel periodo
  solo se la stessa tipologia, interrogata sull'intervallo storico, restituisce atti
  (sezione 7.1); altrimenti è un dato mancante (al 15 settembre, `XMO`) e la lettura si
  dichiara incompleta. Per questo ogni passata vuota porta il totale storico della tipologia
  (`mergePasses`).
- **Data del record.** `data_documento` è `dtSeduta` quando c'è, altrimenti `dtRpr`, come
  giorno di Roma; il record dice da quale campo viene (`data_documento_da`). Si tengono gli
  atti con `data_documento` fra il 1° gennaio 2026 e il giorno della lettura: una
  convocazione per una seduta futura si prende a una lettura successiva.
- **Municipio.** Un atto è di una struttura del Municipio quando `dscStrOrg` dice «MUNIC…»,
  poi «ROMA» se c'è, poi il numero romano, confrontato per intero (X non è IX né XI);
  un'annotazione fra parentesi come «(EX MUNICIPIO V)» nomina il Municipio di prima e non
  conta. È la forma che lo studio di settembre ha riconosciuto su tutte le 1.426 righe delle
  tipologie municipali (`tools/sources-study/a2_tipologie.py`). Gli atti dei gruppi della Polizia
  Locale (`P.L. - <numero> GRUPPO …`) restano fuori, con il motivo `polizia_locale`.
- **File della lettura.** Le risposte della ricerca si salvano come arrivano, una per pagina, in
  `originali/attiweb_elenco_<giorno>_<inizio>_<tipologia>_p<passata>_<pagina>.json`, con l'inizio
  della lettura, così due letture dello stesso giorno non danno mai lo stesso nome; ogni riga
  dello storico rimanda alla sua (`provenienza.elenco`). Il registro di ogni lettura sta in
  `D Storico/letture/attiweb_lettura_<inizio>.json`: per ogni tipologia se è completa, le
  passate, il totale, il dato mancante, gli errori, le righe tenute e quelle lasciate fuori per
  motivo. Le righe tenute vanno in `attiweb_righe_<inizio>.json`, da cui legge il download.
  Ogni giro di download scrive, prima della prima richiesta, la prenotazione
  `attiweb_download_<giorno>_n<documenti>_<inizio>.json`, con i documenti che chiederà: il tetto
  del giorno si conta da quei nomi, e un giro che si ferma a metà conta per intero. Scritta la
  prenotazione, il giro rilegge prenotazioni ed esiti del giorno nell'ordine in cui Drive li ha
  scritti, e riconosce la sua dall'id del file. Si ferma prima di ogni richiesta se con la sua il
  totale supera il tetto, o se una prenotazione scritta prima, con dei documenti, non ha ancora il
  suo esito: due giri non scaricano mai insieme, e nessun record si scrive due volte. Un giro che
  si ferma, o che non ha niente da scaricare, scrive comunque l'esito, con zero documenti, e la sua
  prenotazione resta e conta. Un giro interrotto senza esito ferma i giri seguenti del giorno
  finché il coordinatore non legge il suo avviso. A fine giro
  scrive l'esito, documento per documento, in
  `attiweb_scaricati_<giorno>_n<letti>_<inizio>_<id>.json`, con l'id del file della sua
  prenotazione: l'esito si lega alla prenotazione da quell'id, e non conta per il tetto. Prima di
  ogni richiesta il giro controlla il giorno di Roma: se non è più quello della prenotazione, non
  chiede più niente, e i documenti rimasti vanno nell'esito come non richiesti, per un giro del
  giorno nuovo. `<inizio>` è l'ora UTC
  d'inizio, `YYYYMMDDTHHMMSSZ`.
- **Segnali di blocco.** Oltre a 403, 429, captcha e pagina di accesso, fermano la lettura
  anche 401 e qualunque rinvio: il portale non rinvia nelle risposte normali. La ferma anche
  una pagina HTML servita con 200 dove il portale manda dati (l'elenco, il PDF), fuori dalla
  risposta vuota: una pagina che controlla il browser con uno script non dice «captcha». Una
  risposta che non è un PDF si legge come testo, così la si riconosce anche al posto del
  documento. Se un workflow D si ferma, per un segnale di blocco o per un
  errore, `staging_D_avviso` scrive `AVVISO_attiweb_<ora>.json` in `D Storico/letture/` con il
  workflow, l'esecuzione, il nodo e il messaggio: è il registro della lettura o del giro
  interrotto, che resta incompleto, e il coordinatore avvisa l'owner. Il workflow d'avviso resta
  attivo: n8n non chiama un workflow d'errore non pubblicato.
- **Righe illeggibili.** Una riga che non si legge si conta nel registro e lascia incompleta la
  sua tipologia, quindi la lettura (DEC-033, regola 5).
- **PDF.** Il portale manda i PDF come `application/octet-stream` con un nome `.pdf`: valgono
  come originali. Un file vuoto, un altro tipo di file o un codice diverso da 200 si contano
  nel registro del download e non si scrivono; una pagina HTML ferma il giro (segnali di
  blocco), anche se il portale la usasse per un documento che manca.
- **Versioni.** Gli `archive_id` nuovi si scaricano per primi; con il tetto che resta nel
  giorno si riscaricano quelli già nello storico, da quello verificato da più tempo, così ogni
  documento si ricontrolla nel tempo. Lo stesso originale (stesso SHA-256) non aggiunge
  versioni, un originale diverso ne aggiunge una. Il riscaricamento arriva con la PR del
  registro delle verifiche: finché non c'è, il download prende solo gli `archive_id` nuovi.

## 3. Dove sta che cosa

| Che cosa | Dove |
|---|---|
| Elementi del giorno | Drive, `QN Hub / 30 Staging pilota 2026-11 / <workstream>/` (cartella privata), nel file fissato dalla PR che apre il canale (qui sotto e sezione 7) |
| Record dello storico (DEC-023) | Drive, `D Storico/` nella stessa cartella, in sola aggiunta; la copia di riserva in `D Storico/riserva/` |
| Originali delle fonti: testi, trascrizioni, PDF degli atti | Drive, sottocartella `originali/` dello stesso workstream o dello storico |
| Registri delle letture dello storico | Drive, `D Storico/letture/` |
| Registro fonti (fonte di verità, DEC-023) | Drive, `Registro fonti/`, foglio Google |
| Codice, test con esempi inventati, contratti, decisioni | GitHub |

**Il file degli elementi** (formato, nome, chiavi di primo livello, versione dello schema)
lo fissa la PR del coordinatore che apre il canale, insieme alla forma del `content_id`:
finché quella PR non c'è, il canale non scrive elementi. Il JSON canonico comune a tutti i
blocchi è ancora un compito aperto (`docs/START_HERE.md`), e la prima PR che apre un canale
lo affronta. Il prototipo legge un'altra cosa, la proiezione della sezione 2: un oggetto con
`reference_date` ed `events` (`tools/site/build_site.py`).

**Su GitHub non entra mai un testo di notizia**: né un campione, né un contenuto del sito,
né un caso di test preso da una fonte vera. Il supporto GitHub ha indicato le parole chiave
nel contenuto come causa dei blocchi (audit, sezione F), e la cronaca ne è piena.

**I file grandi** (PDF degli atti, audio, trascrizioni lunghe) non passano dal connettore
Drive degli agenti, che accetta solo contenuti piccoli. Li sposta n8n in staging, che ha già
le credenziali Google. I workstream preparano e provano i workflow `staging_`; quelli di
produzione non si toccano (`CLAUDE.md`).

## 4. GitHub e revisioni

- Scrive su GitHub solo il coordinatore (DEC-030, DEC-031).
- Un workstream consegna il codice al coordinatore come bundle git del proprio branch,
  caricato nella sua cartella Drive. Il coordinatore lo verifica, fa girare i test e apre
  la PR.
- Le PR sono piccole (protocollo, sezione 2, punto 4). La revisione segue il protocollo,
  sezione 4, e DEC-032.

## 5. Costi

Il budget del pilota e le regole per superarlo sono in DEC-031, punto 6, e valgono per il
totale del mese. La suddivisione qui sotto è un'allocazione interna, che il coordinatore può
spostare fra i workstream:

| Workstream | Quota mensile | Voci principali |
|---|---|---|
| A Amministrazione | 20 € | trascrizione delle sedute che non hanno già una trascrizione |
| B Notizie | 10 € | modelli per scrivere le bozze |
| C Eventi | 10 € | Apify (circa 0,01 $ a evento) e modelli |
| D Storico | 5 € | download ed estrazione del testo |
| Riserva | 5 € | del coordinatore |

Ogni spesa entra nel campo `costo` dell'elemento o del record dello storico e in
`costi.jsonl` della cartella del workstream. Il coordinatore somma le spese di tutti i
workstream e applica DEC-031, punto 6, al totale del mese, non a ogni singola quota.

## 6. Regole delle fonti che restano in vigore

Le regole stanno nelle decisioni, che qui non si riassumono: questa sezione dice solo dove
si applicano.

- **Facebook:** DEC-102.
- **Stampa:** DEC-108, per intero: quali testate si leggono, quali non si aprono mai e quando
  un nome si pubblica.
- **Fonti amministrative ufficiali**, atti e documenti compresi: DEC-105. Per le
  registrazioni delle sedute vale anche il suo confine della seduta aperta.
- **Siti:** prima di leggere una fonte si controllano `robots.txt` e le condizioni d'uso.

## 7. I canali aperti

Un canale si apre con una PR del coordinatore, che lo aggiunge qui. Un canale che non è in
questa sezione non scrive elementi (sezione 3).

### B · Notizie (`news`)

Il canale si apre in due tempi. Questa sezione fissa l'elemento, la sua identità e la raccolta.
La geografia, il filtro editoriale, la scrittura in parole nostre e la seconda verifica
(DEC-108) arrivano con le PR successive. Finché non ci sono, il canale salva solo gli
originali in `B Notizie/originali/` e non scrive elementi.

| Che cosa | Regola |
|---|---|
| Elemento | il fatto, non l'articolo della fonte: lo stesso fatto da più fonti è un elemento solo (sezione 2). Se un comunicato di riepilogo dia più elementi, uno per fatto, lo decide l'owner con DEC-034 (R-C01): l'identità ha già il posto per il numero del fatto |
| File | un JSON per fatto in `B Notizie/`, `roma__nws__<chiave>[-f<n>].json`. Le chiavi di primo livello sono quelle degli eventi, con `news` al posto di `event`: `schema_version` (`pilot-news-0.1`), `content_id`, `content_type` e `stream` (`news`), `source`, `news`, `geography`, `editorial`, `quality`, `lifecycle`, `pilot` |
| Identità | `content_id` = `qn:roma:nws:<chiave>`, con la chiave dai primi 16 caratteri dello SHA-256 dell'URL canonico del record che ha aperto il fatto, con le regole di `web-event-identity.js`. Se quel record contiene più fatti, si aggiunge `-f<n>`, con `n` il posto del fatto nel record (un intero da 1), fissato alla prima divisione. La calcola `code-nodes/news-identity.js`, con i test in `tests/test_news_identity.js` |
| `source_hash` | lo SHA-256 di titolo, testo, ora di pubblicazione e luogo dichiarato del record che ha aperto il fatto, normalizzati (`news-identity.js`). Se la fonte dà solo il giorno, l'ora è il giorno, con `date_precision: day` |
| Capofila | da decidere: DEC-034 (R-C02). Finché la decisione non c'è, il canale non scrive elementi; il `source_hash` si calcola sul record che ha aperto il fatto |
| Colonne della coda | `block = news`; `source_channel` è `news_official` (Questura, Carabinieri), `news_press` (testata aperta) o `news_index` (solo titolo, link e ora di una testata chiusa, da un indice terzo) |
| Pubblicabile | lo decide DEC-108; come si contano gli editori sta in `docs/sources/CRONACA_PROCESSO_2026-10.md`, sezione 4.6. Il canale scrive per ogni fatto le fonti che quella regola conta, nelle `attribuzioni` (sezione 2), e non pubblica niente prima della PR che applica la regola |
| Fonti al 10 novembre 2026 | ufficiali: l'elenco dei comunicati della Questura di Roma e quello dei Carabinieri (le pagine di elenco: il feed dei Carabinieri è escluso da `robots.txt`). Testate aperte: Abitare a Roma e Il Faro Online, dai loro feed. Il sito del Comune oggi rinvia `robots.txt` alla pagina di accesso: non si legge finché il rinvio resta (sezione 6) |
| Raccolta | ogni ora; una richiesta alla volta, almeno 5 secondi fra due, di più dove `robots.txt` chiede un `Crawl-delay`. Si legge la prima pagina dell'elenco o del feed. Un host si ferma al primo 401, 403 o 429, captcha, pagina di accesso, rinvio verso un altro host o pagina di blocco servita con 200. Il blocco non si aggira; si avvisa il coordinatore. Un errore del server o una richiesta senza risposta lasciano l'host non letto in quella corsa; cinque di fila lo fermano. `robots.txt` si ricontrolla una volta al giorno; una pagina HTML al suo posto non vale come regole, e l'host si ferma |
| Originali | le risposte come arrivano, una per file, in `B Notizie/originali/notizie_<host>_<inizio>_<n>.<estensione>`, con `<n>` il numero della risposta di quell'host nella corsa, da 1: nessun file si sovrascrive; il registro di ogni corsa in `B Notizie/letture/notizie_<inizio>.json`, con le richieste, gli esiti e gli host fermati per host, e l'esito della lettura di ogni pagina salvata, anche quando non c'è niente di nuovo. `<inizio>` è l'ora UTC d'inizio, `YYYYMMDDTHHMMSSZ` |

### C · Eventi da Facebook (`fb_event`)

| Che cosa | Regola |
|---|---|
| File | il JSON canonico della specifica v2.5 (contratto canonico, `schema_version` 2.0): un file per evento, e un file solo per una serie (fase 3.4) |
| Nome del file | `canonical_file_name` della specifica, fase 2.1 |
| Cartella | `QN Hub / 30 Staging pilota 2026-11 / C Eventi/`, piatta come nella specifica |
| `content_id`, `source_hash` | specifica, fasi 2.1 e 2.2; `code-nodes/compute-source-hash.js` |
| Colonne della coda | `source_channel = fb_event`; le altre come in `docs/REVIEW_QUEUE.md` |
| Aggiunte del pilota | un oggetto `pilot` al primo livello del file, con `workstream` (`C`), `registro_id` quando c'è, `costo`, `source_title`, il nome dell'evento alla fonte (`event_name` dell'evento sorgente) su cui lavora la fusione dei doppioni (DEC-025, regola 1), e `first_written_at`, l'ora UTC della prima scrittura del file, che poi non cambia (regola 3). Le chiavi della specifica non cambiano |
| Fusione dei doppioni | con il canale `web_event`, qui sotto, «La fusione dei doppioni» |
| URL delle fonti | raccolti a mano (DEC-102) |
| Proiezione per il prototipo | `tools/site/project_events.py`, con i test in `tests/test_project_events.py` |

### C · Eventi dalle pagine web (`web_event`)

Il canale scrive elementi solo nelle corse in cui gira anche la fusione dei doppioni di DEC-025
(qui sotto, «La fusione dei doppioni»): senza la fusione lo stesso evento, arrivato anche da
Facebook o da un'altra fonte, comparirebbe due volte.

| Che cosa | Regola |
|---|---|
| Fonti | i siti del registro fonti (colonna `sito`) dei municipi del pilota. Prima di leggere un sito si controllano `robots.txt` e le condizioni d'uso (sezione 6), e l'esito si scrive con la data nella riga del registro. Un sito che non permette la lettura, o le cui regole non si riescono a leggere, non si legge |
| File | il JSON canonico della specifica v2.5, come per Facebook, con `source.type = "web_page"`: un file per evento, un file solo per una serie |
| Identità | `content_id`, nome del file e segnalazione li calcola `code-nodes/web-event-identity.js`, con i test in `tests/test_web_event_identity.js`. Se l'evento ha una pagina sua, l'identità viene dall'URL canonico di quella pagina; se compare solo in un elenco, dall'URL dell'elenco, dal giorno di inizio a Roma e dal titolo normalizzato, e il file porta `identity_from_listing` in `quality.review_flags` |
| `source_hash` | `code-nodes/compute-source-hash.js`, sui campi della fase 2.2 letti dalla pagina |
| Colonne della coda | `source_channel = web_event`; `source_id` è l'host del sito (sezione 2) |
| Aggiunte del pilota | lo stesso oggetto `pilot` di Facebook, con `source_title` il nome dell'evento letto sulla pagina (`event_name` dell'evento sorgente) e `first_written_at` |
| Cartella | `C Eventi/`, come per Facebook; le pagine lette restano in `C Eventi/originali/` |
| Proiezione per il prototipo | `tools/site/project_events.py`, la stessa dei file di Facebook |



### C · La fusione dei doppioni (DEC-025)

DEC-025 fissa le scelte: l'ordine delle fonti, i campi mancanti, l'identità e la prudenza.
Qui c'è il modo di applicarle; lo esegue `code-nodes/merge-duplicate-events.js`, su tutti gli
elementi della corsa insieme, e ogni regola ha un test in `tests/test_merge_duplicate_events.js`.
Un cambio che fa fondere da soli casi che oggi vanno in coda richiede una decisione dell'owner
(DEC-025, regola 4).

**Che cosa legge.** In `pilot`: `source_title`, il nome dell'evento alla fonte; `first_written_at`,
l'ora UTC della prima scrittura del file, che poi non cambia (i file scritti prima ricevono
l'ora di creazione del file su Drive); `review_pending`, che il flusso mette a `true` prima
della fusione quando l'elemento ha nella coda una riga non ancora decisa. Un file senza
`source_title` o senza `first_written_at` ferma la fusione con il suo `content_id`. Il `title`
dell'articolo non entra mai nel confronto.

**Lo stesso evento.** I criteri partono da quelli stretti del foglio di ottobre
(`tools/fonti/lavoro-2026-10/doppioni.py`, PR #21):
- titoli normalizzati: scomposizione Unicode NFKD, via i caratteri non ASCII, minuscole, ogni
  segno che non è lettera o cifra diventa spazio, via le parole di due lettere o meno e le
  parole vuote dello script;
- somiglianza: la maggiore fra la sovrapposizione delle parole (Jaccard) e il rapporto di
  `difflib.SequenceMatcher` sui titoli normalizzati. Il rapporto dipende dall'ordine dei due
  titoli: si prende il minore dei due ordini, così il risultato non dipende dall'arrivo e non
  è mai più largo di ottobre;
- identificativi corti: un numero di una o due cifre, un numero romano fino a C («XXV»,
  «XLVI», anche la forma additiva «XXXXV»), o una lettera sola, tranne le parole e le
  elisioni italiane con cui si confonderebbero (a, e, i, o, ci, li; c, d, l). Se due titoli,
  o due luoghi, non hanno gli stessi identificativi («Corso 1» e «Corso 2», «Sala A» e
  «Sala B») la coppia non si fonde;
- date: il giorno di inizio a Roma e, se la fine è data dalla fonte, il giorno di fine; due
  eventi sono compatibili se i loro intervalli si toccano;
- luoghi che coincidono: tutti e due noti, con almeno metà delle parole in comune (Jaccard
  almeno 0,5) e, se tutti e due hanno le coordinate, a non più di 1 km;
- si fondono da soli due eventi i cui luoghi coincidono, con gli stessi identificativi, con
  l'ora di inizio tutti e due e a non più di 60 minuti, e con somiglianza almeno 0,85 e date
  compatibili oppure almeno 0,72 e lo stesso giorno di inizio;
- vanno in coda senza fondersi: ogni altra coppia con somiglianza almeno 0,72 e date
  compatibili, per esempio la replica pomeridiana e quella serale; un evento senza data; una
  serie confrontata con qualunque altro evento; una coppia in cui un evento ha solo il giorno
  (la fonte lo segna con `start_time_unknown` in `quality.review_flags`); due titoli che
  normalizzati restano vuoti, lo stesso giorno, nello stesso luogo;
- un gruppo di tre o più elementi si fonde solo se ogni sua coppia è lo stesso evento,
  altrimenti va in coda tutto il gruppo.

Un gruppo si forma anche sulle coppie in coda, così una terza copia dubbia tiene in coda le
altre due. Una fonte senza grado nell'ordine di DEC-025 non si fonde mai: è un caso non
previsto e va in coda. Ogni elemento che va in coda per la fusione riceve `duplicate_doubt` in
`quality.review_flags` e `requires_review`.

**Corse ripetute.** I collegamenti (`duplicate_of`, `duplicates`, `lead`, `lead_url`) e i
segnali della fusione (`duplicate_suspected`, `duplicate_doubt`, `merge_deferred`,
`geo_verified_conflict`) si ricalcolano a ogni corsa: un collegamento non sopravvive al
confronto che l'ha creato. Lo stesso vale per i campi presi: quando la fusione riempie o
sostituisce un campo, conserva il valore proprio dell'elemento in `pilot.native` e quello
che ha messo in `pilot.derived`; la corsa dopo rimette il valore proprio solo se il campo
vale ancora quello messo dalla fusione (altrimenti l'ha riscritto la fonte dell'elemento, e
resta); i campi che vanno insieme (inizio e fine, latitudine e longitudine) si giudicano e si
rimettono insieme, e riprende i campi dalle fonti come sono allora, così un valore cambiato alla
fonte arriva e un campo preso da una coppia che non c'è più se ne va. Un elemento con
`review_pending` non cambia, come il suo gruppo («La coda»). Quando è la fusione a mettere `requires_review`, segna in
`pilot.merge_review` le ragioni che c'erano in quel momento; la corsa dopo lo toglie solo se
la ragione della fusione non c'è più e nessun'altra fase ne ha aggiunta una. L'ordine di `first_written_at` si confronta come istante, non
come testo. `filled_from` conserva le voci delle corse precedenti, perché i valori presi restano
nel file. `source_title` vuoto o fatto di soli spazi, o `first_written_at` che non è un istante
UTC vero (niente 30 febbraio), fermano la fusione.

**Chi comanda e chi resta.** Nel gruppo comanda la fonte di grado più alto (DEC-025, regola
1); a parità di grado comanda la pagina propria dell'evento rispetto a un elenco
(`identity_from_listing`), poi il `content_id` in ordine alfabetico. Resta l'elemento con la
`first_written_at` più vecchia; a parità, quello che comanda. L'elemento che resta riceve in
`pilot` `lead` (il `content_id` di chi comanda), `duplicates` e `filled_from`; ogni copia
riceve `duplicate_of` e `duplicate_suspected` in `quality.review_flags`, e non si pubblica da
sola (`tools/site/project_events.py`).

**I campi.** L'elemento che resta prende da chi comanda le date, il luogo, il link di
prenotazione e il nome alla fonte, e pubblica il link di chi comanda (`pilot.lead_url`, che la
proiezione usa al posto di `source.url`): l'elemento tiene il suo `content_id` e il suo
`source`, che dice da dove viene il file. Da Roma Today, anche quando comanda, si prendono
solo nome, ora e link; un campo che gli manca ancora lo prende dalla prima fonte successiva che lo ha, mai da
Roma Today. Inizio, fine e precisione della data si prendono sempre insieme da una fonte, e
così latitudine e longitudine. `pilot.filled_from` dice, per ogni campo preso così, il suo
percorso e il `content_id` da cui viene. La geografia non si copia: un luogo cambiato porta
`geo_recompute`, e il gazetteer ricalcola zona e municipio. Una geografia `human_verified`
non prende prove del luogo né si ricalcola; se le prove del luogo di una qualunque copia del
gruppo sono diverse, l'elemento riceve `geo_verified_conflict` e va in coda.

**La coda.** La fusione non scrive nella coda, che si scrive solo in aggiunta
(`docs/REVIEW_QUEUE.md`). Un elemento con `review_pending` resta com'è, campi e collegamenti
compresi, e un gruppo con un elemento in coda aspetta tutto: nessun campo si muove e nessuna
copia si nasconde fino alla decisione, ogni elemento del gruppo riceve `merge_deferred`, e la
prima corsa dopo la decisione fonde il gruppo. Una riga che una copia ha già in coda si decide
`discard` con `fix_target = none`, perché l'evento vive nell'elemento che resta.

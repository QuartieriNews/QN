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
  storico in `D Storico/riserva/<data>/`; nessun altro workflow scrive lì.

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
  dichiara incompleta.
- **Data del record.** `data_documento` è `dtSeduta` quando c'è, altrimenti `dtRpr`, come
  giorno di Roma; il record dice da quale campo viene (`data_documento_da`). Si tengono gli
  atti con `data_documento` fra il 1° gennaio 2026 e il giorno della lettura: una
  convocazione per una seduta futura si prende a una lettura successiva.
- **Municipio.** Un atto è di una struttura del Municipio quando `dscStrOrg` dice «MUNIC…»,
  poi «ROMA» se c'è, poi il numero romano, confrontato per intero (X non è IX né XI): la
  forma che lo studio di settembre ha riconosciuto su tutte le 1.426 righe delle tipologie
  municipali (`tools/sources-study/a2_tipologie.py`). Gli atti dei gruppi della Polizia
  Locale (`P.L. - <numero> GRUPPO …`) restano fuori, con il motivo `polizia_locale`.
- **Versioni.** Gli `archive_id` nuovi si scaricano per primi; con il tetto che resta nel
  giorno si riscaricano quelli già nello storico, da quello verificato da più tempo, così ogni
  documento si ricontrolla nel tempo. Lo stesso originale (stesso SHA-256) non aggiunge
  versioni, un originale diverso ne aggiunge una.

## 3. Dove sta che cosa

| Che cosa | Dove |
|---|---|
| Elementi del giorno | Drive, `QN Hub / 30 Staging pilota 2026-11 / <workstream>/` (cartella privata), nel file fissato dalla PR che apre il canale (qui sotto e sezione 7) |
| Record dello storico (DEC-023) | Drive, `D Storico/` nella stessa cartella, in sola aggiunta; la copia di riserva in `D Storico/riserva/` |
| Originali delle fonti: testi, trascrizioni, PDF degli atti | Drive, sottocartella `originali/` dello stesso workstream o dello storico |
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

### C · Eventi da Facebook (`fb_event`)

| Che cosa | Regola |
|---|---|
| File | il JSON canonico della specifica v2.5 (contratto canonico, `schema_version` 2.0): un file per evento, e un file solo per una serie (fase 3.4) |
| Nome del file | `canonical_file_name` della specifica, fase 2.1 |
| Cartella | `QN Hub / 30 Staging pilota 2026-11 / C Eventi/`, piatta come nella specifica |
| `content_id`, `source_hash` | specifica, fasi 2.1 e 2.2; `code-nodes/compute-source-hash.js` |
| Colonne della coda | `source_channel = fb_event`; le altre come in `docs/REVIEW_QUEUE.md` |
| Aggiunte del pilota | un oggetto `pilot` al primo livello del file, con `workstream` (`C`), `registro_id` quando c'è e `costo`. Le chiavi della specifica non cambiano |
| URL delle fonti | raccolti a mano (DEC-102) |
| Proiezione per il prototipo | `tools/site/project_events.py`, con i test in `tests/test_project_events.py` |


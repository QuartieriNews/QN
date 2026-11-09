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
| Geografia | `gazetteer.json` → `resolution.store`, `geo_basis_values`, `verification_status_values`; `prompts/PROMPT_GEO_BLOCK.md` | `publication_zone_id`; `neighbourhood_id` quando è noto in modo deterministico; `geo_level`; `municipality_code` (sempre, quando noto: è l'unica chiave a livello di municipio); `geo_basis`; `geo_verification_status`, dove `human_verified` ferma ogni ricalcolo |
| Classificazione editoriale | `gazetteer.json` → `editorial`; `prompts/EDITORIAL_FILTER.md` | `editorial_class` per ogni blocco; per gli eventi anche `editorial_basis` e `content_type`. I valori per notizie, amministrazione e storico sono un'estensione per blocco: si aggiungono con una PR del coordinatore prima che quel workstream produca elementi |
| Scarti e coda di revisione | `gazetteer.json` → `reject_reasons`, `review`; `docs/REVIEW_QUEUE.md` | `reject_reason` con i codici canonici e la loro regola `blocks_publication`. Quali elementi entrano nella coda di lavoro e quali vanno direttamente nell'archivio con `decision = auto_excluded` lo stabilisce `docs/REVIEW_QUEUE.md`; il pilota non lo ridefinisce |
| Eventi | specifica v2.5, fasi 1–2 (Drive, `QN Hub / 10 Specifications`); `code-nodes/` | `source_event_id` valido per DEC-027; `start_at_utc`, `end_at_utc`, `date_precision`; `source_hash` (`code-nodes/compute-source-hash.js`) |
| Freschezza | specifica v2.5, parte III | il campo con il nome della specifica; il pilota non ne inventa uno |

Il prototipo del sito (`tools/site/`) legge una proiezione più semplice (`start`, `end`,
`title`…). La si ricava dai campi canonici al momento di costruire le pagine; non si
salva al loro posto.

**L'identità di un elemento** è il `content_id` della specifica v2.5 (fase 2.1), lo stesso
che la coda di revisione usa come chiave. Per gli eventi da Facebook la sua forma è quella
della specifica, serie comprese. Per gli altri canali (eventi dalle pagine web, sedute, atti,
notizie) la forma del `content_id` e la procedura di `source_hash` le fissa la PR del
coordinatore che apre quel canale, sullo schema della specifica e con queste regole:
- la geografia non entra nel `content_id` (specifica, fase 2.1), e nemmeno `registro_id`;
- si costruisce dalla chiave della fonte, che non cambia mai:
  - per un evento, il `source_event_id` normalizzato secondo DEC-027;
  - per una seduta, l'id della registrazione (il `guid` di RomaTV, l'id del video YouTube);
  - per un atto, l'ufficio che lo emette, il tipo, il numero e l'anno, in minuscolo e
    separati da `/`; l'URL canonico dell'atto solo per le fonti che non numerano gli atti.
    La scelta si fa per fonte, non per singolo atto;
  - per una notizia, l'URL canonico del pezzo (`https`, host minuscolo, senza parametri di
    tracciamento né frammento).

Quando il contenuto della fonte cambia, cambia `source_hash`, non il `content_id`.

**Le aggiunte e le convenzioni del pilota.** `block` e le colonne `source_*` sono colonne canoniche della coda: qui si fissa solo come il pilota le riempie. Gli altri campi il contratto canonico non li ha.

| Campo | Contenuto |
|---|---|
| `workstream` | `A`, `B`, `C` o `D` |
| `block` | la colonna canonica della coda (nel file canonico lo stesso valore sta in `stream`); il pilota usa `events`, `institutional`, `news` e `conversation`, i quattro blocchi di `docs/PROJECT_VISION.md`. Un record dello storico non ha `block` (qui sotto, «Lo storico») |
| `source_channel`, `source_id`, `source_url` | le colonne canoniche della coda, con il significato di `docs/REVIEW_QUEUE.md`: `source_id` è l'id che la piattaforma dà a chi pubblica (la pagina o il gruppo Facebook, il canale YouTube); per un sito, il suo host in minuscolo senza `www.`. I valori nuovi di `source_channel` (sedute, atti, stampa) arrivano con la PR del coordinatore che apre il blocco |
| `registro_id` | l'id della fonte nel registro (`S-…`), quando c'è. Non sostituisce `source_id` e non entra in nessuna chiave |
| `archive_id` | quando l'elemento nasce da un record dello storico |
| `attribuzioni` | le testate e le fonti citate, ciascuna con un link (DEC-108) |
| `nomi` | le persone nominate, ognuna con la regola che lo consente (sezione 6): DEC-105 per le fonti amministrative ufficiali, atti e documenti compresi, con il confine della seduta aperta per le sole registrazioni delle sedute; DEC-108 per la stampa |
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
| `archive_id` | stabile: `sto-` seguito dai primi 16 caratteri esadecimali dello SHA-256 della stringa UTF-8 `<source_id>\|<chiave della fonte>`, con la chiave definita qui sopra |
| `versione` | 1 alla prima scrittura (vedi la correzione, qui sotto) |
| `source_id`, `registro_id`, `source_url` | come per gli elementi |
| `data_documento` | la data dell'atto o della seduta, `YYYY-MM-DD` |
| `municipality_code` | il campo canonico della geografia, quando è noto |
| `tipo` | il tipo di documento; i valori li fissa una PR del coordinatore prima che D scriva record |
| `provenienza` | come il record è stato ottenuto: l'URL letto, l'ora della lettura (`retrieved_at`, UTC), il workflow `staging_` e la sua versione |
| `originale` | il percorso del file in `originali/`, che non si modifica mai |
| `derivato` | il testo estratto o la trascrizione, con lo strumento e la versione che li hanno prodotti |
| `etichette` | le nostre etichette (zona, argomenti…), ciascuna con chi o che cosa l'ha messa |
| `costo` | come per gli elementi |

- **Correzione.** Niente si sovrascrive e niente si cancella. Una correzione è una riga
  nuova con lo stesso `archive_id`, la `versione` aumentata di uno e un campo `motivo`;
  vale la versione più alta.
- **Copia di riserva.** Una volta alla settimana un job di copia duplica i file dello
  storico in `D Storico/riserva/<data>/`; nessun altro workflow scrive lì.

## 3. Dove sta che cosa

| Che cosa | Dove |
|---|---|
| Elementi del giorno | Drive, `QN Hub / 30 Staging pilota 2026-11 / <workstream>/` (cartella privata) |
| Record dello storico (DEC-023) | Drive, `D Storico/` nella stessa cartella, in sola aggiunta; la copia di riserva in `D Storico/riserva/` |
| Originali delle fonti: testi, trascrizioni, PDF degli atti | Drive, sottocartella `originali/` dello stesso workstream o dello storico |
| Registro fonti (fonte di verità, DEC-023) | Drive, `Registro fonti/`, foglio Google |
| Codice, test con esempi inventati, contratti, decisioni | GitHub |

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
- Le PR sono piccole (protocollo, sezione 2). La revisione la chiede l'owner, circa quattro
  volte al giorno, non di più (DEC-031, punto 7).

## 5. Costi

Il budget del pilota è di 50 € al mese (DEC-031, punto 6). Suddivisione iniziale:

| Workstream | Tetto mensile | Voci principali |
|---|---|---|
| A Amministrazione | 20 € | trascrizione delle sedute che non hanno già una trascrizione |
| B Notizie | 10 € | modelli per scrivere le bozze |
| C Eventi | 10 € | Apify (circa 0,01 $ a evento) e modelli |
| D Storico | 5 € | download ed estrazione del testo |
| Riserva | 5 € | del coordinatore |

Ogni spesa entra nel campo `costo` dell'elemento o del record dello storico e in
`costi.jsonl` della cartella del workstream. Il coordinatore somma le spese e avvisa l'owner
prima di superare il tetto. Un lavoro quasi finito si chiude anche se servono 10–15 € in più.

## 6. Regole delle fonti che restano in vigore

- **Facebook:** si legge solo sugli URL raccolti a mano, con un servizio terzo (DEC-102).
- **Stampa: si applica DEC-108 per intero.** Qui sotto c'è un promemoria; in caso di dubbio
  vale la decisione.
  - Un fatto riportato da una seconda testata diventa un articolo scritto con parole nostre,
    con le testate nominate e linkate. Un dettaglio presente in una sola testata si
    attribuisce a quella testata.
  - Le testate che escludono gli agenti di IA o riservano l'estrazione di testi e dati
    (Roma Today, Il Messaggero, ANSA, Corriere, Repubblica, Leggo, Today.it, Agenzia Nova)
    non si aprono mai. Di loro si usano solo titolo, link e ora, presi da un indice di
    terzi. Contano come seconda testata e si linkano, ma gli articoli di QN si scrivono da
    testate aperte e fonti ufficiali.
  - Un nome preso dalla stampa si pubblica solo se valgono tutte queste condizioni:
    - lo riportano testate di almeno due editori diversi;
    - la persona è maggiorenne, arrestata o indagata;
    - il testo rispetta la presunzione di innocenza;
    - una seconda IA verifica che nome e ruolo coincidano in ogni fonte;
    - l'articolo attribuisce la notizia («secondo X e Y»).

    Il nome si aggiorna o si toglie quando il caso cambia o su richiesta.
  - Non si pubblicano mai le identità di minori coinvolti in procedimenti penali, come
    vittime o come testimoni, né quelle delle vittime di violenza sessuale.
- **Fonti amministrative ufficiali: si applica DEC-105.** Qui sotto c'è un promemoria; in
  caso di dubbio vale la decisione.
  - Negli atti e nei documenti come nelle sedute, i nomi pertinenti al fatto restano,
    verificati sulla fonte. Un nome si omette solo per una ragione concreta, scritta caso
    per caso.
  - Per le registrazioni delle sedute vale in più il confine della seduta aperta (DEC-105,
    confine 2): ciò che sta fuori, sospensioni comprese, non entra né nell'analisi né nelle
    notizie.
- **Siti:** prima di leggere una fonte si controllano `robots.txt` e le condizioni d'uso.

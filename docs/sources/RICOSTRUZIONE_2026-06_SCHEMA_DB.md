# Ricostruzione di giugno 2026 — schema del database e regole di collegamento

Stato: **proposto**, in attesa del controllo Codex C1 (nota di fattibilità §9.6, tabella dei
controlli). Vale per il Report 1 (fonti testuali, intero mese) e per il Report 2 (atti e video,
8–28 giugno), che scrivono nelle stesse tabelle: il Report 2 aggiunge righe e riempie campi, non
cambia lo schema.

Perimetro, conteggio, cutoff, deduplicazione, campionamento e collocazione dei dati per item
sono quelli di `SOURCE_STUDY_METHOD.md` §4.1–§4.3: questo documento non li ridefinisce, definisce
le tabelle che li applicano e le regole di collegamento che il metodo lascia all'esecuzione.

## 1. Tabelle

Cinque CSV, codifica UTF-8, intestazione obbligatoria, separatore virgola, valori vuoti ammessi
solo dove la colonna lo dichiara. Vivono in `QN Hub / 20 Packages / Fonti 2026-06/` (DEC-102,
DEC-104 regola 2). Se il connettore Drive non è disponibile restano nello scratchpad della
sessione e il rapporto dichiara la consegna come incompleta con la causa: **non entrano nel
repository**, che è pubblico e che DEC-104 regola 2 tiene libero dai dati per item. Nel
repository entrano solo gli aggregati e il riferimento alla cartella Drive.

### 1.1 `fonti.csv` — una riga per fonte

| Colonna | Contenuto | Vuoto |
|---|---|---|
| `codice` | A1, A2, C1, C2, C4, C5, E2, E3, A3, A4 | no |
| `nome` | nome della fonte | no |
| `blocco` | Amministrazione, Cronaca, Eventi | no |
| `ente` | ente che pubblica | no |
| `url_elenco` | URL dell'elenco percorso | no |
| `base_url` | radice da anteporre agli URL relativi di `documenti` (E3); vuoto se `documenti.url` è assoluto | sì |
| `formato` | HTML, PDF, JSON, video | no |
| `item_giugno` | item del mese secondo il cutoff §4.1 | no |
| `paginazione_completa` | sì/no: la paginazione copre tutto il mese | no |
| `data_lettura` | data e ora della lettura, Europe/Rome | no |
| `report` | 1, 2, o "1;2" | no |
| `note` | anomalie dichiarate | sì |

### 1.2 `documenti.csv` — una riga per item letto

| Colonna | Contenuto | Vuoto |
|---|---|---|
| `id` | `<codice fonte>_<progressivo a 4 cifre>`: 4 bastano al volume massimo del mese (A2, 2.669 atti) | no |
| `fonte` | `fonti.codice` | no |
| `tipo` | news, avviso, atto, evento, registrazione, video | no |
| `url` | URL dell'item (per E3 relativo, con `base_url` nella riga di `fonti`) | no |
| `data_pubblicazione` | ISO `AAAA-MM-GG`; vuoto → gruppo "senza data" (§4.1) | sì |
| `timestamp_pubblicazione` | ISO con ora e fuso quando la fonte la dà (C2 la dà, C1 no): è il primo criterio del tie-break §4.1 | sì |
| `data_evento_inizio`, `data_evento_fine` | solo blocco Eventi | sì |
| `titolo_anonimizzato` | titolo della pagina con i nomi di persona sostituiti dal ruolo (DEC-102): il titolo grezzo non lascia lo scratchpad | no |
| `municipi_meta` | Municipi dichiarati dalla fonte, separati da `;` | sì |
| `tematica` | tematica dichiarata dalla fonte | sì |
| `caratteri` | caratteri del testo estratto | no |
| `formato_item` | HTML, PDF testo, PDF scansione, JSON, audio, video | no |
| `metodo_estrazione` | `nativo`, `OCR`, `trascrizione piattaforma`, `trascrizione API` | no |
| `ocr_incerto` | sì/no; vuoto se `metodo_estrazione` ≠ `OCR` | sì |
| `trascrizione_incerta` | sì/no con la confidenza media quando c'è; vuoto se non è una trascrizione | sì |
| `esito_lettura` | completo, parziale, fallito | no |
| `settimana` | 1, 2, 3, 4, 5 (W2–W4 = 8–28 giugno), da `data_pubblicazione` letta in Europe/Rome | sì |
| `report_origine` | 1 o 2: il rapporto che ha portato dentro la riga | no |
| `letto_da` | identificativo del lotto di lettura | no |

### 1.3 `notizie_candidate.csv` — una riga per notizia candidata

Una riga per notizia candidata estratta da un documento. Un documento può produrne zero o più;
una riga appartiene sempre a un solo documento (l'unione fra documenti sta in `vicende`).

| Colonna | Contenuto | Vuoto |
|---|---|---|
| `id` | `N<progressivo a 4 cifre>` | no |
| `documento_id` | `documenti.id` | no |
| `fonte` | `fonti.codice`, ridondante per la lettura diretta | no |
| `titolo_anonimizzato` | ≤ 12 parole, senza nomi di persona (DEC-102) | no |
| `sintesi` | ≤ 60 parole, senza nomi di persona | no |
| `tipo` | delibera, mozione, risoluzione, ordine del giorno, interrogazione, sopralluogo, audizione, arresto, sequestro, incendio, incidente, controllo, evento, avviso, altro | no |
| `luoghi` | toponimi citati, separati da `;`, come compaiono nel testo | sì |
| `municipio` | I–XV o vuoto | sì |
| `zona` | zona del gazetteer o vuoto | sì |
| `tier_localizzazione` | `meta`, `text_contains`, `titolo`, `ambiguous`, `assente` | no |
| `toponimo_da_verificare` | sì/no (§9.3: 1 candidata su 8 nella taratura) | no |
| `evidenza_url` | URL della pagina che sostiene la notizia | no |
| `evidenza_locale` | pagina `p. N` per gli atti, `[mm:ss]` per le registrazioni, vuoto per le pagine HTML | sì |
| `data_fatto` | ISO; vuoto se il testo non la dà | sì |
| `data_pubblicazione` | ISO, dalla fonte | sì |
| `disponibilita` | ISO: quando il testo è diventato leggibile, se diverso dalla pubblicazione | sì |
| `qualita` | alta, media, bassa | no |
| `dedup_stato` | `unica`, `duplicato`, `dubbio` | no |
| `gemello_id` | `notizie_candidate.id` del gemello; obbligatorio se `dedup_stato` ≠ `unica` | sì |
| `ragione_dedup` | condizioni (a)(b)(c) di §4.1 verificate e quella incerta | sì |
| `prima_fonte` | sì/no: esito del tie-break §4.1; `non applicabile` quando `dedup_stato = dubbio`, dove il gemello non è accertato | no |
| `vicenda_id` | `vicende.id` o vuoto | sì |
| `integra_gemello_id` | riga del Report 1 che questa integra o corregge; vuoto se non integra nulla | sì |
| `campi_integrati` | colonne che l'integrazione riempie o corregge, separate da `;` | sì |
| `settimana` | come in `documenti` | sì |
| `report_origine` | ereditato da `documenti.report_origine` | no |
| `verifica_seconda_ai` | `concorde`, `discorde`, `non eseguita` (schema T4) | no |

### 1.4 `vicende.csv` — una riga per vicenda

Vicenda = insieme di notizie candidate che seguono lo stesso fatto nel tempo o fra fonti diverse
(§2 sotto). Serve al confronto fra Report 1 e Report 2 ("vicende approfondite").

| Colonna | Contenuto | Vuoto |
|---|---|---|
| `id` | `V<progressivo a 3 cifre>` | no |
| `titolo_anonimizzato` | ≤ 12 parole, senza nomi di persona | no |
| `tipo` | come `notizie_candidate.tipo` | no |
| `municipio`, `zona` | come sopra | sì |
| `prima_pubblicazione`, `ultima_pubblicazione` | ISO | no |
| `n_notizie` | righe collegate | no |
| `fonti` | codici separati da `;` | no |
| `confidenza` | `alta`, `media`, `bassa`: come il legame fra le notizie è stato stabilito (§2 regola 3) | no |
| `solo_report2` | sì/no: emersa solo da atti e video | no |
| `stato` | `aperta`, `conclusa`, `non verificato` | no |

### 1.5 `territori.csv` — una riga per Municipio e settimana

| Colonna | Contenuto |
|---|---|
| `municipio` | I–XV, `non localizzato` |
| `settimana` | 1–5 |
| `n_documenti`, `n_notizie` | conteggi |
| `n_notizie_alta`, `n_notizie_media`, `n_notizie_bassa` | per qualità |
| `fonti_presenti` | codici separati da `;` |
| `mediana_giorni_pubblicazione` | mediana di `data_pubblicazione − data_fatto`, vuoto se meno di 3 casi |
| `lacuna` | sì/no: nessuna notizia nella cella |

## 2. Regole di collegamento

1. **Documento → notizia**: ogni riga di `notizie_candidate` cita il documento da cui è stata
   letta e almeno un'evidenza (`evidenza_url`, più `evidenza_locale` dove il formato la
   consente). Una notizia senza evidenza non entra nel database: entra nell'elenco delle
   lacune del rapporto.
2. **Notizia ↔ notizia (deduplicazione)**: le tre condizioni (a) data, (b) luogo, (c) oggetto di
   §4.1, verificate in quest'ordine. Il tie-break §4.1 assegna `prima_fonte`: primo criterio
   `timestamp_pubblicazione`, poi l'ordine predefinito delle fonti, poi l'URL.
   L'estensione segue la soglia di §4.1 senza eccezioni: **intero mese** quando il blocco ha al
   massimo 300 item nelle fonti di livello 1, e allora la resa è *misurata*; **campione di almeno
   60 item per coppia di fonti** oltre quella soglia, e allora la resa è *stimata* con la
   dimensione del campione dichiarata. A giugno: Cronaca 109 item (C1, C2, C4, C5) → intero mese;
   Eventi 511 item (E2 407, E3 104) → campione, coppia E2×E3, seed `2026-06-E2xE3`;
   Amministrazione nel Report 1 la sola A1, 365 item, nessuna coppia da deduplicare fra fonti →
   solo deduplicazione interna alla fonte, sull'intero mese. Il frame del campione è quello di
   §4.1: elenco completo del mese ordinato per data di pubblicazione, poi per ordine predefinito
   delle fonti, poi per URL; seed registrato nel rapporto e lista campionata salvata accanto ai
   dati per item.
3. **Notizia → vicenda**: due notizie stanno nella stessa vicenda quando seguono **lo stesso
   fatto o lo stesso procedimento** e hanno stesso `municipio` (o stesso toponimo normalizzato).
   Il `tipo` non deve coincidere: una vicenda cambia forma lungo il suo corso — un'interrogazione
   diventa sopralluogo e poi delibera — e legarla al tipo perderebbe proprio gli
   approfondimenti che il Report 2 deve misurare. Serve invece un **legame esplicito nel testo**:
   stesso atto, stessa seduta, stesso procedimento, oppure una notizia cita l'altra.
   `vicende.confidenza` registra come il legame è stato stabilito: `alta` quando le due notizie
   citano lo stesso identificativo (atto, protocollo, seduta), `media` quando il legame è
   nominato ma non identificato, `bassa` quando poggia solo su continuità di luogo e oggetto —
   e una vicenda di confidenza `bassa` è dichiarata come tale nel rapporto, mai contata fra le
   vicende accertate. La ripetizione dello stesso tema in luoghi diversi **non** è una vicenda.
   Una vicenda esiste da due notizie in su; una notizia isolata ha `vicenda_id` vuoto.
4. **Localizzazione**: `geo_lookup.py` sul testo dell'item; il tier registra come si è arrivati
   al luogo. Il Municipio dichiarato dalla fonte prevale sul toponimo dedotto dal testo solo
   quando i due concordano o il testo non ne offre uno più fine; se discordano, `municipio` resta
   quello della fonte, `toponimo_da_verificare = sì` e il rapporto lo conta fra gli incerti.
5. **Report 1 → Report 2**: il Report 2 non riscrive le righe del Report 1. Una notizia trovata
   in un atto o in una registrazione che coincide con una del Report 1 secondo (a)(b)(c) è una
   riga nuova con `report_origine = 2`, `dedup_stato = duplicato` e `gemello_id` che punta alla
   riga del Report 1: è così che si misurano copertura, sovrapposizioni e lacune colmate senza
   toccare la prima consegna. Quando la riga nuova **aggiunge o corregge** qualcosa alla gemella —
   una data del fatto che il Report 1 non aveva, un Municipio diverso, un esito di voto —
   `integra_gemello_id` ripete il `gemello_id` e `campi_integrati` elenca le colonne interessate.
   Senza questi due campi l'integrazione resterebbe invisibile: una vista che scarta i duplicati
   perderebbe esattamente il contributo che il Report 2 esiste per misurare. Le viste nette del
   rapporto scartano i duplicati **che non integrano nulla**.

## 3. Regole di qualità

- `qualita = alta` quando il testo dà fatto, luogo e data ed esiste un'evidenza puntuale;
  `media` quando uno dei tre è dedotto; `bassa` quando due lo sono. Una notizia il cui fatto è
  solo annunciato (convocazione, ordine del giorno) non supera `media`.
- Nessun nome di persona in nessuna colonna (DEC-102): ruoli al loro posto. Vale anche per le
  colonne copiate dalla fonte, `titolo_anonimizzato` in testa: il titolo grezzo della pagina resta
  nello scratchpad e non viene mai caricato. Controllo con `grep` sui nomi presenti nei testi di
  partenza prima di ogni caricamento.
- Le contraddizioni si dichiarano, non si risolvono: `non verificato` nelle colonne interessate e
  una riga nell'elenco delle incertezze del rapporto.
- Un valore dedotto non è mai scritto come letto: le colonne di data vuote restano vuote.

## 4. Verifica dello schema

Prima dell'estrazione, controllo Codex C1 su questo documento (tabelle, regole di collegamento,
regole di qualità) e sul manifesto della prima lettura. Dopo l'estrazione, controllo C2 su un
campione del Report 1 secondo le quote di §4.3. Esiti in `reviews/`, costi nel ledger.


## 1.6 `coppie_parlato_scritto.csv` — ogni accostamento fra una riga del parlato e una scritta

Aggiunta il 16 settembre su rilievo del controllo C5: il numero principale del Report 2 si calcola da
qui, e lasciarlo fuori dalle tabelle rendeva il database non autosufficiente. `gemello_id` ne ammette
uno solo, mentre una riga può averne molti: quella colonna resta la catena della deduplicazione, e
questa tabella è il confronto esaustivo.

| colonna | valori | obbligatoria |
|---|---|---|
| `parlata` | `notizie_candidate.id` di una riga con fonte A3 o A4 | sì |
| `scritta` | `notizie_candidate.id` di una riga di fonte scritta | sì |
| `forza` | `forte` (tre criteri su tre) o `debole` (due su tre) | sì |
| `criteri` | quali criteri hanno tenuto: `d` data, `l` luogo, `o` oggetto | sì |
| `stesso_blocco` | sì/no: se le due righe stanno nello stesso blocco tematico | sì |

## 1.7 `registro_id.csv` — l'identificativo di una notizia, e perché non è la sua posizione

Aggiunta il 16 settembre. Fino a quel giorno `notizie_candidate.id` era la **posizione** della riga
nella costruzione: aggiungere un lotto di atti, che entra in mezzo, faceva scorrere tutti gli
identificativi delle registrazioni, e un audit in corso si è trovato a giudicare righe diverse da
quelle che aveva davanti — con una collisione silenziosa, non un vuoto. Ora l'identificativo sta in
questo registro, legato all'identità della riga.

| colonna | valori | obbligatoria |
|---|---|---|
| `id` | `N` + quattro cifre, assegnato una volta sola | sì |
| `documento_id` | il documento da cui la riga viene | sì |
| `titolo` | il titolo della riga, che insieme al documento la identifica | sì |

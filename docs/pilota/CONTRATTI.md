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

Ogni workstream produce elementi in JSON Lines (un oggetto per riga, UTF-8), un file al
giorno: `<cartella del workstream>/AAAA-MM-GG.jsonl`. Campi comuni:

| Campo | Contenuto |
|---|---|
| `id` | stabile: `<workstream>-<fonte_id>-<hash breve dell'URL o del fatto>` |
| `workstream` | `A`, `B`, `C` o `D` |
| `tipo` | `notizia`, `evento`, `seduta` o `atto` |
| `blocco` | `dal_municipio`, `notizie`, `eventi` o `se_ne_parla` |
| `fonte_id`, `fonte_nome` | id del registro fonti (`S-…`) quando c'è, e il nome |
| `url_fonte` | il link alla fonte originale, sempre |
| `data_fatto`, `data_fonte`, `raccolto_il` | ISO 8601, ora di Roma |
| `municipio` | `I`…`XV` |
| `publication_zone_id`, `geo_level` | dal gazetteer; `geo_level` è `neighbourhood`, `zone`, `municipality` o `city` (`prompts/PROMPT_GEO_BLOCK.md`) |
| `titolo_qn`, `testo_qn` | scritti da noi, mai copiati dalla fonte |
| `attribuzioni` | testate e fonti citate, ciascuna con un link (DEC-108) |
| `nomi` | le persone nominate, ognuna con la regola che lo consente (DEC-105 seduta aperta, DEC-108 due testate) |
| `stato` | `raccolto`, `bozza`, `verificato`, `pubblicabile` o `scartato`, con `motivo` |
| `revisione` | chi, quando, esito, quando una persona lo guarda |
| `costo` | servizio, unità (minuti, eventi, token) ed euro, quando c'è una spesa |

Gli eventi aggiungono i campi della specifica v2.5 che il prototipo già legge (`start`,
`end`, `title`, `venue`, `url`, `editorial_class`, `municipality_code`). Nel pilota
`title` è il titolo scritto da noi.

## 3. Dove sta che cosa

| Che cosa | Dove |
|---|---|
| Elementi del giorno | Drive, `QN Hub / 30 Staging pilota 2026-11 / <workstream>/` (cartella privata) |
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

Ogni spesa entra nel campo `costo` dell'elemento e in `costi.jsonl` della cartella del
workstream. Il coordinatore somma le spese e avvisa l'owner prima di superare il tetto. Un
lavoro quasi finito si chiude anche se servono 10–15 € in più.

## 6. Regole delle fonti che restano in vigore

- Facebook: si legge solo sugli URL raccolti a mano, con un servizio terzo (DEC-102).
- Stampa: regola dell'MVP di DEC-108 (due testate, testo nostro, testate che escludono l'IA
  lette solo come titolo e link, mai identità di minori o di vittime di violenza sessuale).
- Sedute: solo quanto detto a seduta aperta (DEC-105, confine 2).
- Siti: prima di leggere una fonte si controllano `robots.txt` e le condizioni d'uso.

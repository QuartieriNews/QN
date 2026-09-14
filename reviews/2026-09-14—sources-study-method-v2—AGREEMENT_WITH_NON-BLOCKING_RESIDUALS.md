AGREEMENT WITH NON-BLOCKING RESIDUALS

**Council:** Technical Council (DEC-008, modello AI a tre livelli), secondo controllo circoscritto del **metodo dello studio delle fonti**, giustificato dai due finding BLOCKING del primo (risposta dell'owner del 14 settembre 2026 §3: ulteriori passaggi solo per problemi sostanziali, senza cicli indefiniti). Con questo il controllo del metodo è chiuso; il prossimo controllo di Codex è sulla consegna dello studio, prima delle decisioni dell'owner.

**Reviewer:** Codex (`gpt-5.3-codex`, OpenAI Responses API, reasoning `high`, `store: false`). Risposta id `resp_02a9bfe70e7c6b5e016aa86b172cd487d1967f8facd9d45d45`; usage: input 12.680, output 6.020 (di cui reasoning 4.966), totale 18.700 token.

**Versione esaminata:** `docs/sources/SOURCE_STUDY_METHOD.md`, versione M-0.2, sha256 `964c14715f20ac5756f8d2c47a2dd4e40e385a0c1530b127285e9d307c193c31`, commit `8f2e2da`. **Il verdetto vale per M-0.2.**

## Finding di Codex (testo integrale)

### VERDETTO — **AGREEMENT WITH NON-BLOCKING RESIDUALS** (metodo **M-0.2**, sha256 `964c14715f20ac5756f8d2c47a2dd4e40e385a0c1530b127285e9d307c193c31`, commit `8f2e2da`)

Il metodo, nella versione M-0.2, è **eseguibile** per estendere lo studio, con residui non bloccanti da chiudere per aumentare la riproducibilità.

---

### FINDING

1) **IMPORTANT — Dedup su campione: riproducibilità non ancora completamente deterministica**  
- **Dove**: `SOURCE_STUDY_METHOD.md` §4.1 (“campione casuale di almeno 60 item per coppia di fonti”; “attribuito alla prima fonte che lo ha pubblicato”).  
- **Cosa non va**: è definita la regola sostanziale di dedup, ma non la procedura tecnica di estrazione casuale (seed/frame) né un tie-break esplicito quando due fonti hanno stessa data (o solo data senza ora). Questo può produrre risultati leggermente diversi tra esecuzioni/reviewer.  
- **Fonte**: mandato owner §3 (conteggi riproducibili; duplicazioni definite e misurabili) + metodo §4.1.  
- **Correzione suggerita**: aggiungere in §4.1:  
  - frame di campionamento (insieme preciso degli item eleggibili),  
  - seed fisso registrato,  
  - salvataggio della lista campionata su Drive,  
  - tie-break deterministico (es. timestamp completo → ordine fonte predefinito → URL).

2) **MINOR — Quote del campione audit troppo rigide nei casi a bassa incidenza**  
- **Dove**: `SOURCE_STUDY_METHOD.md` §4.3 (“10 duplicati e 10 distinti… 10 localizzati zona e 10 solo Municipio/non localizzati”).  
- **Cosa non va**: in blocchi/fonti con pochi duplicati o pochi non-localizzati la quota fissa può essere irrealistica e indurre selezione opportunistica.  
- **Fonte**: owner §3 (campione per conclusioni “sicure”, con ricontrollo su errore sistematico) + metodo §4.3.  
- **Correzione suggerita**: rendere la quota “fino a N, se disponibili”; se non disponibili, prendere **tutti** i casi esistenti e dichiarare la numerosità effettiva.

---

### CONVERGENZE — cosa del metodo è corretto e non va ripetuto

- I 2 finding **BLOCKING** del primo controllo risultano corretti:  
  - dedup ora definita con regole, dubbi e intervallo min/max (§4.1),  
  - dati per-item fuori repo pubblico, aggregati nel repo (§4.2), coerente con DEC-104/DEC-102.
- Corretto il punto su evidenze: tri-stato **misurato/stimato/mancante** esplicito (header + §3.8), in linea col mandato owner §1/§3.
- Conteggio mese ora molto più riproducibile: cutoff, fuso Europe/Rome, “senza data”, paginazione e timestamp lettura (§4.1).
- Campione rafforzato rispetto a M-0.1: minimo per fonte + quote mirate + regola di ricontrollo su errore sistematico (§4.3).
- Complessità proporzionata e limiti espliciti su fonti difficili (tetto tempo/prova, stop & decisione owner, alternative con costi/benefici) (§5), coerente con owner §2.
- Vincoli rispettati: niente automazione autenticata Facebook (DEC-102), niente raw nel repo pubblico (DEC-104), gate credenziali fail-closed per T1/T3/T4 (§7/§9), budget 50 € con ledger e stop prima del tetto (§7).

---

### RESIDUI PER L’OWNER — ciò che nessuno dei due può risolvere dalle fonti

- Conferma scritta su chiave OpenAI (distinta o rotazione verificata) per sbloccare T1/T3/T4 (owner §7; metodo §7/§9).  
- Apertura domini e verifica accesso reale post-modifica (owner §4; metodo §6).  
- Conferma finale della collocazione Drive dei dati per-item (§4.2).  
- Eventuale deposito dei 3 file audio su Drive se stream/video non acquisibili dall’ambiente (§5).  
- Verifiche legali sui termini di riuso (owner §1 e §3).
## Risposta dell'Operator e correzioni applicate in M-0.3 — NON riverificate da Codex

| # | Severità | Risposta | Correzione (M-0.3) | Controverifica |
|---|---|---|---|---|
| 1 | IMPORTANT | Accettato | §4.1: frame di campionamento (elenco completo del mese ordinato per data, ordine predefinito delle fonti, URL), seed fisso registrato per fonte, lista campionata salvata su Drive, tie-break deterministico per "prima fonte" (timestamp → ordine delle fonti → URL) registrato con il gemello | non riverificata |
| 2 | MINOR | Accettato | §4.3: quote "fino a N, se disponibili"; se una categoria ha meno casi, si prendono tutti e la numerosità effettiva è dichiarata | non riverificata |

I cinque finding del primo controllo (M-0.1) sono stati controverificati in questo passaggio e trovati conformi.

Residui per l'owner confermati (invariati): conferma scritta sulla chiave OpenAI (distinta o rotazione verificata) per sbloccare T1/T3/T4; apertura dei domini e verifica reale dell'accesso; collocazione su Drive dei dati per item; eventuali tre file audio su Drive; verifiche legali sui termini di riuso.

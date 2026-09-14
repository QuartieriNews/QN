NO AGREEMENT

**Council:** Technical Council (DEC-008, modello AI a tre livelli), controllo circoscritto del **metodo dello studio delle fonti**, concordato dall'owner il 14 settembre 2026 (risposta dell'owner §3: "controllo del metodo all'inizio e della consegna prima delle decisioni"). Non è una review del piano esecutivo e non riapre la baseline.

**Reviewer:** Codex (`gpt-5.3-codex`, OpenAI Responses API, reasoning `high`, `store: false`). Risposta id `resp_09e4b333f7a926d1016aa86a3d79c087d1aac654ecbf46e47e`; usage: input 13.262, output 9.668 (di cui reasoning 8.198), totale 22.930 token.

**Versione esaminata:** `docs/sources/SOURCE_STUDY_METHOD.md`, versione M-0.1, sha256 `9d5666b8e8c045f37c3d742c10306efd94a9567ac345f2708391eb30da69984e`, commit `ab12827`. Input inviato: risposta dell'owner del 14 settembre (integrale), baseline v0.6 §2.A, DEC-102, DEC-104, DEC-014, step S2 e §11 del piano B-0.6, il metodo.

## Finding di Codex (testo integrale)

### VERDETTO — **NO AGREEMENT** (sul metodo **M-0.1**, sha256 `9d5666b8e8c045f37c3d742c10306efd94a9567ac345f2708391eb30da69984e`, commit `ab12827`)

### FINDING

1) **BLOCKING — Deduplicazione non ancora abbastanza definita per essere misurabile/riproducibile**  
- **Dove**: `SOURCE_STUDY_METHOD.md` §3 punto 4 (“stesso giorno ±1, stesso toponimo, stesso oggetto”, “misurata sul campione”) + §8 (“resa dopo la deduplicazione”).  
- **Cosa non va**: il criterio “stesso oggetto” resta interpretativo; mancano protocollo operativo, dimensione minima del campione dedup e regola di trasformazione in resa complessiva. Così il numero chiave “resa dopo dedup” non è verificabile in modo consistente.  
- **Fonte**: mandato owner §1 e §3 (controllo su “duplicazioni” definita/misurabile; sintesi con resa post-dedup).  
- **Correzione suggerita**: aggiungere una procedura dedup esplicita (campi confrontati, tie-break, gestione casi dubbi, output “misurato” vs “stimato”, formula usata).

2) **BLOCKING — Collocazione dei CSV per-item nel repo pubblico in conflitto con DEC-104/DEC-102 (da chiudere prima di estendere)**  
- **Dove**: metodo §4 (“CSV in `docs/sources/samples/<fonte>_2026-06.csv` con una riga per item e URL”).  
- **Cosa non va**: il metodo prevede dataset per-item nel repository pubblico; DEC-104 impone che i raw sampled source data stiano fuori repo (Drive package), e DEC-102 ribadisce che i dati fonte non vadano ridistribuiti come dataset.  
- **Fonte**: DEC-104, regola 2; DEC-102, “Consequence inside this repository”.  
- **Correzione suggerita**: tenere per-item CSV/campioni fuori repo (Drive), e mettere su repo solo aggregati, metriche e riferimenti minimi necessari all’audit.

3) **IMPORTANT — Campione “5 item per fonte” non basta da solo per convalidare le conclusioni “sicure”**  
- **Dove**: metodo §4 (campione Codex/owner: 5 item/fonte).  
- **Cosa non va**: utile per controllo rapido, ma debole per validare claims su localizzazione e sovrapposizioni nelle fonti ad alto volume/eterogenee.  
- **Fonte**: owner §3 (campione con passaggi pertinenti, conclusioni sicure, ricontrollo su errore sistematico).  
- **Correzione suggerita**: mantenere i 5 come minimo audit, ma aggiungere quota mirata per claim critici (duplicato/non duplicato, localizzato/non localizzato, formati diversi).

4) **IMPORTANT — Gate credenziali OpenAI non “fail-closed”**  
- **Dove**: metodo §7 (nota chiave OpenAI) e §9 (T1/T3/T4 dopo conferma o rotazione).  
- **Cosa non va**: finché non c’è conferma owner, il metodo lascia una zona grigia operativa; il vincolo owner è che prove con credenziali esposte restano subordinate alla rotazione/verifica.  
- **Fonte**: owner §7; piano esecutivo §11 “Sicurezza” (S0 gate aperto).  
- **Correzione suggerita**: regola esplicita “T1/T3/T4 bloccate finché owner non conferma chiave distinta o rotazione completata”.

5) **MINOR — Incoerenza numerica nel “primo insieme” + dettaglio riproducibilità conteggio migliorabile**  
- **Dove**: metodo §2 (“dodici sezioni” livello 1) vs elenco (A1, A2, C1–C6, E1, E2 = 10); §4 (conteggio senza convenzione esplicita su cutoff temporale).  
- **Cosa non va**: la discordanza può creare ambiguità di avanzamento; manca una convenzione univoca di cutoff (timestamp/fuso) per replicare conteggi nel tempo.  
- **Fonte**: metodo §2/§4; owner §3 (conteggi riproducibili e completi).  
- **Correzione suggerita**: correggere cardinalità livello 1 e fissare regola di cutoff temporale per ogni conteggio.

---

### CONVERGENZE — cosa del metodo è corretto e non va ripetuto

- Impianto generale coerente col mandato: metodo separato dallo studio, con controllo Codex iniziale/finale (`§8`), come richiesto dall’owner §3.  
- Buona disciplina su **misurato/stimato/mancante** (`stato dati` iniziale, §3 punto 8), in linea con S2-05.  
- Buona gestione della complessità: priorità livelli 1→2→3 e limiti su fonti difficili (`§2`, `§5`), coerente con owner §2.  
- Vincolo Facebook rispettato: fuori perimetro operativo dell’Operator, niente automazione autenticata (`§1`, `§6`; DEC-102).  
- Budget ben impostato: ledger, tetto 50 €, no abbonamenti, T6 separata e subordinata ad autorizzazione (`§7`), coerente con owner §5.  
- Dipendenze tecniche ben esplicitate (`§6`, `§9`), utile per evitare stalli impliciti.

---

### RESIDUI PER L’OWNER — ciò che nessuno dei due può risolvere dalle fonti

- Conferma formale sulla chiave OpenAI (distinta vs esposta) o esito rotazione, per sbloccare T1/T3/T4.  
- Apertura domini di rete e verifica accesso reale post-modifica (§6).  
- Decisione esplicita su dove tenere i dati per-item (interpretazione operativa DEC-104/DEC-102 per i CSV di conteggio).  
- Eventuale deposito dei 3 file audio su Drive se streaming/video non è acquisibile dall’ambiente (§5).  
- Verifiche legali sui termini di riuso che il metodo può solo segnalare come “da verificare” (owner §1, §3; L11).
## Risposta dell'Operator e correzioni applicate in M-0.2

| # | Severità | Risposta | Correzione (M-0.2) | Controverifica |
|---|---|---|---|---|
| 1 | BLOCKING | Accettato | §4.1: procedura di deduplicazione esplicita (tre condizioni: data ±1, luogo normalizzato con il gazetteer, oggetto per tipo di fatto; casi dubbi marcati e resa riportata come intervallo; gemello e ragione registrati); estensione: intero mese fino a 300 item per blocco (misurato), altrimenti campione ≥ 60 per coppia di fonti (stimato); formula lorda/duplicati/dubbi/netta | attesa nel secondo controllo |
| 2 | BLOCKING | Accettato | §4.2: i dati per item stanno su Drive (`QN Hub / 20 Packages / Fonti 2026-06/`), senza nomi né testi; nel repository solo aggregati, metriche e riferimento alla cartella; collocazione da confermare dall'owner | attesa |
| 3 | IMPORTANT | Accettato | §4.3: 5 item per fonte come minimo, più quote mirate per blocco (20 per la deduplicazione, 20 per la localizzazione, raddoppiate per fonti oltre 100 item), casi sicuri e dubbi indicati, ricontrollo integrale su errore sistematico | attesa |
| 4 | IMPORTANT | Accettato | §7 e §9: regola fail-closed: T1, T3, T4 bloccate fino a conferma scritta di chiave distinta o rotazione verificata; senza conferma la chiave si considera esposta; i controlli di Codex proseguono solo per disposizione esplicita dell'owner | attesa |
| 5 | MINOR | Accettato | §2: livello 1 = dieci sezioni; §4.1: cutoff per data di pubblicazione in Europe/Rome, 1–30 giugno inclusi, gruppo "senza data", ora di lettura e copertura della paginazione registrate | attesa |

Residui per l'owner confermati: conferma scritta sulla chiave OpenAI; apertura dei domini e verifica reale dell'accesso; collocazione dei dati per item; eventuali file audio su Drive; verifiche legali sui termini di riuso (L11).

# Mandato per Codex: rifare in modo indipendente il lavoro sulle fonti degli eventi (ottobre 2026)

**Chi lo chiede e perché.** Il 27 ottobre 2026 l'owner ha chiesto di «passare tutto il processo a Codex e dirgli di rifarlo anche
lui così da avere qualche dato in più di supporto». In questo mandato Codex lavora come **secondo builder indipendente**, non come
revisore: non approva e non rivede il lavoro del builder, produce numeri propri con un metodo proprio e solo alla fine li confronta.

**Ruolo.** Su richiesta dell'owner del 27 ottobre 2026, per questo solo mandato e sul solo ramo `codex/replica-fonti-eventi`,
Codex scrive nel repository in deroga ad `AGENTS.md` («the reviewer ... never holds the pen»). La deroga e il nome di chi rivede
la pull request di Codex li conferma l'owner prima dell'avvio (`OWNER_DECISION_REQUIRED`); il merge resta dell'owner.

**Da dove partire.** Dal ramo `claude/ecstatic-shannon-mjzxvq`, al commit che aggiunge questo mandato o a uno successivo: `main`
non ha DEC-023…026, DEC-105…109 né `tools/fonti/`.

Il processo del builder, con tutti i numeri, le scelte, i run Apify e i link, è in `docs/sources/PROCESSO_FONTI_EVENTI_2026-10.md`.
**Leggilo solo dopo aver fissato i tuoi numeri** (§1).

## 1. Regola di indipendenza

1. **Ordine di lavoro e commit.**
   - Commit A: i numeri di R1, R3, R4 e R5, fatti solo con le letture permesse al punto 2.
   - Commit B: i numeri di R2. Solo dopo il commit A apri `pagina/` del pacchetto; solo dopo il commit B apri `qualita/`.
   - Commit C: R6 e il confronto. Solo dopo il commit B apri `uscite/`, i tre risultati di `elaborazioni_builder/` e i
     documenti del punto 3.
   - Fai il push dopo ciascuno dei tre commit e scrivi nel rapporto, per ogni commit, i file del pacchetto e del repository che hai
     aperto prima di farlo.
2. **Prima del commit A leggi solo:**
   - questo mandato;
   - le decisioni citate nel §4 (non DEC-023, DEC-024, DEC-025: vedi il punto 3);
   - il gazetteer (`gazetteer/`);
   - i dati del §2, tranne `pagina/`, `qualita/`, `uscite/` e i tre file di `elaborazioni_builder/` indicati come risultati.
3. **Non leggere prima del commit B** i documenti che contengono i risultati del builder:
   - `docs/sources/PROCESSO_FONTI_EVENTI_2026-10.md` e `docs/sources/PROCESSO_FONTI_EVENTI_2026-10_DETTAGLIO.md`;
   - `docs/sources/FONTI_EVENTI_STATO_2026-10-24.md`;
   - `docs/sources/QUALITA_EVENTI_2026-10-26.md`;
   - `docs/sources/NOTIZIE_DAI_DATI_2026-10-26.md`;
   - `docs/sources/TIMELINE_BREVI_2026-10-26.md`;
   - `docs/sources/FLUSSO_EVENTI_A_Z.md`;
   - tutta la cartella `docs/wiki/fonti-eventi/` (`README.md`, `INDEX.md`, `per-pagina-qn.md`, `promotori.md`, `municipi/`,
     `censimento-pagine.md`, `aggregatori.md`, `fusioni-proposte.md`, `fonti_eventi.json`);
   - `decisions/DEC-023`, `DEC-024` e `DEC-025`, che portano conteggi del builder. È una deroga ad `AGENTS.md`, che chiede di
     leggere tutte le decisioni: vale fino al commit B;
   - `tools/fonti/lavoro-2026-10/README.md`.
4. **Codice, commit e pull request.**
   - Puoi leggere il codice del repository, ma i commenti, le stringhe e il README di `tools/fonti/lavoro-2026-10/` citano numeri
     del builder: apri solo il codice del passo che riusi.
   - Se riusi uno script o un'estrazione del builder invece di rifare il passo, dichiaralo nel rapporto: un passo riusato non è una
     conferma indipendente.
   - Prima del commit B non leggere i messaggi dei commit del ramo `claude/ecstatic-shannon-mjzxvq` (usa `git log --format=%h`) né
     la discussione della pull request #15.
5. **Indipendenza non piena: dichiaralo.** Le tue revisioni della pull request #15 del 25 e 26 ottobre (commit `a48b9cf`,
   `d95572b`, `e98d5aa`, `d75fdea`, `ab96501`, `3a7af96`, `abfce0b`) hanno visto parte dei risultati del builder. Se ne hai
   memoria, scrivilo nel rapporto.

## 2. Dati di ingresso

**Pacchetto privato, in tre parti.**
- Lo consegna l'owner fuori dal repository, in tre zip che si estraggono nella stessa cartella
  `pacchetto_replica_fonti_eventi_2026-10/`:
  - `pacchetto_replica_1_subito.zip`: tutto ciò che si apre «subito» nella tabella qui sotto;
  - `pacchetto_replica_2_dopo_commit_A.zip`: `pagina/`;
  - `pacchetto_replica_3_dopo_commit_B.zip`: `qualita/`, `uscite/` e i tre risultati di `elaborazioni_builder/`.
- Estrai le parti **fuori** dalla copia del repository, nel percorso che ti indica l'owner: `.gitignore` non le protegge e il
  repository è pubblico. Non fare mai `git add` di un file del pacchetto.
- Contiene dati personali (email, telefoni e indirizzi di enti, nomi dei legali rappresentanti degli enti RUNTS e dei titolari di
  profili Facebook personali) e testi delle fonti, quindi non va mai nel repository (DEC-102, DEC-104).
- Il suo `LEGGIMI.md` descrive ogni cartella.

| Cartella | Contenuto | Quando si apre |
|---|---|---|
| `apify_org/` | i 56 dataset dell'account Apify dell'organizzazione (24-25 ottobre), uno per run, con `MANIFEST.json` (attore, run, dataset, input, righe, costo), l'input di ogni run in `input/` e i listini degli attori letti il 27 ottobre (`LISTINI_2026-10-27.json`) | subito |
| `apify_connettore/` | i dati letti con l'account del connettore Apify: 567 eventi Facebook dai 584 URL della lista dell'owner (23 ottobre; 17 URL senza evento), 722 pagine di associazioni (24 ottobre), l'agenda di culture.roma.it (run del 20 ottobre, 6.222 voci) | subito |
| `input_owner/` | i file dati dall'owner: il foglio «eventi /» (URL di eventi Facebook e di Roma Today), il foglio «Eventi letti alla fonte 13-31 ottobre», il registro del 13 ottobre, le 1.169 pagine di associazioni, gli enti RUNTS, le 220 pagine verificate dall'owner (trascritte dal builder) | subito |
| `letture_web/` | letture senza Apify già fatte. Sono uscite dei lettori del builder (eventi già estratti, senza l'HTML delle pagine) e alcune portano campi calcolati dal builder: `zona` e `municipio` in `feed_feed_eventi.json`; `zona`, `pubblicabile` e `mun_poligono` in `geo_gazetteer_punti.json`. Ignora quei campi. `canali/pagine*.jsonl.gz` ha il testo delle home, delle pagine e dei feed RSS dei siti dei promotori letti il 26 ottobre. `siti_eventi_siti_tutti.json` viene dal lettore dei siti del 24 ottobre, che non controllava ancora robots.txt (corretto il 25) | subito; usare un'estrazione già fatta è un passo riusato da dichiarare |
| `elaborazioni_builder/` | passi intermedi del builder. `promotori_promotori_finale.json` (promotori, R3), `canali_apify_ritmo_post.json` (ritmi dei post, R4) e `post_eventi_eventi_post_futuri.json` (eventi dai post con pagina, R1) sono risultati | i tre risultati dopo il commit B; gli altri file solo per il passo che scegli di riusare, dichiarandolo |
| `pagina/` | `eventi_prima_audit.json` (pagina del 25 ottobre prima delle correzioni del 26) ed `eventi.json` (dopo), con il modello `template.html`. Contengono la geografia e i conteggi del builder | dopo il commit A, per R2 |
| `qualita/` | il campione e i giudizi dell'audit del builder | dopo il commit B |
| `uscite/` | i fogli e il JSON consegnati dal builder | dopo il commit B, per R6 e per il confronto |

**Roma Today.**
- Il pacchetto non contiene le pagine di Roma Today lette il 23 ottobre. Ne sono stati tolti anche i dati presi da quelle pagine:
  gli eventi con `src` «Roma Today» di `pagina/`, i fogli e le righe di Roma Today di `uscite/`, i risultati Google con host
  romatoday.it, citynews.it o today.it di `apify_org/`. L'elenco è in `PULIZIA_ROMA_TODAY.json`.
- Restano menzioni come etichetta di origine (per esempio «Romatoday» nelle colonne `doppione_di` e `fonti`, «Roma Today
  (promotore)» in `elaborazioni_builder/`) e citazioni dentro post Facebook. Salta tutto ciò che viene da Roma Today.
- I dataset Google sull'account Apify contengono ancora quei risultati: se li rileggi da Apify, saltali.

**Apify.**
- I dataset dell'account dell'organizzazione restano sull'account fino a circa il 24 novembre 2026 (conservazione di 31 giorni);
  gli id sono in `MANIFEST.json`.
- Per rileggerli serve il token, che dà l'owner.
- Un run nuovo solo con un tetto di spesa approvato dall'owner.

**Web pubblico.**
- robots.txt sempre letto e rispettato;
- una richiesta al secondo per host;
- user agent «QuartieriNews-fonti/1.0 (+https://github.com/quartierinews/qn; contatto: redazione)»;
- nessun captcha o 403 aggirato.

## 3. Che cosa rifare, in ordine di valore

Per ogni compito scrivi metodo, numeri e **ogni scelta** che fai (soglie, filtri, geografia, conteggio) con il motivo: il confronto
con le scelte del builder serve a capire da dove vengono le differenze.

**R1. Eventi futuri per pagina QN al 25 ottobre 2026.**
- Dai dati di ingresso costruisci l'elenco degli eventi in corso o futuri al 25 ottobre 2026 a Roma e assegnali alle 89 pagine
  QN del gazetteer.
- Togli doppioni, eventi passati, fuori dal Comune o solo online.
- Roma Today resta fuori (§2 e §4).
- Geografia: quella decisa dall'owner il 25 ottobre per l'anteprima.
  - Un evento con coordinate va nella zona urbanistica che lo contiene (`letture_web/popolazione_zu.json`, 155 zone ufficiali),
    poi nella pagina QN del toponimo più vicino fra quelli della zona.
  - Se la zona non ha toponimi, va al toponimo più vicino dello stesso Municipio.
  - Se l'evento non cade in nessuna zona, è fuori dal Comune.
  - `gazetteer.json` non ha coordinate: i punti dei toponimi sono in `letture_web/geo_gazetteer_punti.json` (geocodifica
    Nominatim del builder). Usarli è un passo riusato da dichiarare; in alternativa geocodifica tu i toponimi.
  - Senza coordinate, scegli e dichiara il tuo metodo.
- Canali da riportare: eventi Facebook, post Facebook, sito della fonte (pagina, feed, agenda), culture.roma.it, altro. Dichiara come
  vi riconduci le tue fonti.
- Uscita:
  - eventi per pagina e per canale;
  - pagine a zero, pagine con almeno 10 eventi;
  - eventi senza pagina, con il motivo.

**R2. Qualità della pagina.** Dopo il commit A.
- Campione indipendente di almeno 150 eventi dalla pagina del builder (`pagina/eventi_prima_audit.json`):
  - stratificato per canale;
  - con un seme diverso da 20261026.
- I campi di `pagina/*.json`: `z` pagina QN (id del gazetteer; vuoto = evento senza pagina), `m` Municipio, `t` titolo, `d1` e
  `d2` data di inizio e di fine, `ora`, `luogo`, `ind` indirizzo, `org` organizzatore o fonte, `url` link alla fonte, `src` canale,
  `o` lettura da cui viene l'evento, `free` gratuito dichiarato, `dp` estratto da un post, `ric` ricorrenza dichiarata nel post,
  `dv` data trovata nel testo di una pagina senza dati strutturati. `oggi` è la data della pagina, `pagine` l'elenco delle 89 pagine.
- Confronta ogni evento con la sua fonte e conta gli errori gravi: data sbagliata, già passato o annullato, non è un evento, fuori
  Roma o solo online, pagina QN incoerente. Puoi proporre una definizione tua in più.
- La fonte:
  - per gli eventi e i post Facebook e per culture.roma.it è nei dataset del pacchetto;
  - per il «sito della fonte» il pacchetto ha solo gli eventi estratti dal lettore del builder e, per una parte dei siti, il testo
    letto il 26 ottobre (`letture_web/canali/`). Altrimenti rileggi la pagina oggi con le regole del web pubblico, annota la data
    della lettura e conta a parte le pagine sparite o cambiate;
  - un evento concluso dopo il 25 ottobre non è un errore.
- Ripeti la misura sullo stesso campione dopo le correzioni (`pagina/eventi.json`):
  - lo stesso evento nei due file si riconosce dalla terna (`url`, `t`, `d1`); se manca, confronta titolo e data a mano e
    dichiaralo;
  - un evento del campione assente da `eventi.json` conta come tolto dalle correzioni: esce dal denominatore della misura dopo e
    lo riporti a parte, distinguendo i tolti che avevano un errore grave dagli altri.
- Uscita: tassi con intervallo di confidenza al 95%, per canale.

**R3. Promotori e canale più economico.**
- Dagli eventi di R1 ricava i promotori: chi organizza o pubblica.
- Per ognuno, scegli il canale da leggere che costa meno, con una prova:
  - pagina eventi del sito, feed, agenda;
  - eventi o post Facebook.
- Per la prova sui siti vale l'avvertenza di R2: il testo del 26 ottobre c'è solo per una parte dei siti, il resto si rilegge oggi.
- Uscita: promotori per canale e per tipo di prova; quanti restano solo su Facebook.

**R4. Costo mensile della lettura.**
- Dai listini degli attori Apify (piano Starter, che nei `pricingInfos` è la fascia `BRONZE`: `apify_org/LISTINI_2026-10-27.json`;
  vale per ogni attore l'ultimo listino già in vigore) e dai ritmi misurati nei dataset (post al giorno per pagina, eventi futuri per lettura) calcola il costo mensile.
- In alternativa ricava il costo per riga da `apify_org/MANIFEST.json` (`usd` diviso `righe`), dichiarando che comprende avvii e
  filtri. Non usare i prezzi scritti in `tools/fonti/lavoro-2026-10/canali/costi.py`.
- `apify/cheerio-scraper` non ha listino: si paga a consumo di piattaforma. Per culture.roma.it dichiara un'ipotesi, oppure
  conta la lettura senza Apify (`tools/fonti/leggi_culture_roma.py` legge l'API pubblica).
- Due cadenze: lettura ogni giorno e ogni settimana.
- Due scenari: tutto Facebook, oppure la regola di R3.

**R5, facoltativo. Notizie e brevi dai dati già raccolti.**
- Su un campione indipendente dei post Facebook (dataset `facebook-posts-scraper` di `apify_org/`) e delle voci RSS dei siti
  (`letture_web/canali/`, documenti con `kind` «rss»), misura quante voci sono notizie di quartiere (non eventi, non promozioni, non
  testate) e quante sarebbero brevi da timeline.
- «Breve da timeline»: definiscila tu prima di misurare e dichiara la definizione.

**R6, facoltativo. Fonti scartate.** Dopo il commit B.
- R6 parte dalla classificazione del builder, che sta solo in `uscite/associazioni_fonti.xlsx` e
  `uscite/enti_terzo_settore_fonti.xlsx`: dichiaralo.
- Leggi solo le colonne di identità e di verdetto ed estrai il campione prima di guardare i conteggi.
- Ricontrolla il campione delle pagine e degli enti classificati senza eventi («dormienti», «nessuna presenza web»).

## 4. Regole del repository che valgono anche qui

| Regola | Che cosa dice |
|---|---|
| DEC-102, DEC-104, DEC-109 | Il repository è pubblico (DEC-104) e il dato per evento ne resta fuori (DEC-102, DEC-104): nessun titolo, testo di post o di pagina, email, telefono o nome di persona preso da una fonte. DEC-109 ammette inventari per item senza testo solo in `tools/sources-study/handoff_data/`. Per questo lavoro nel repository vanno solo metodo e numeri aggregati; le righe vanno fuori, nel pacchetto o su Drive. |
| DEC-022 (non è su questo ramo: `git show origin/wiki/giugno-2026:decisions/DEC-022-context-wiki.md`) | I titoli riscritti dai lettori dello studio sono etichette e possono stare nel repository; i titoli di Roma Today sono testo di fonte e ne restano fuori; quei dati restano solo nell'anteprima privata e su Drive. |
| DEC-105 | Nessuna anonimizzazione automatica: i nomi di persone e organizzazioni pertinenti al fatto restano, ma il dato per evento resta fuori dal repository (confine 1). Regola del builder, non di DEC-105: di un organizzatore con profilo Facebook personale si scrive il nome, non l'URL del profilo (T-FE-2, `tests/test_fonti_eventi_build.py`). |
| DEC-026 (aperta) | Finché l'owner non decide vale l'opzione a): nessuna lettura di Roma Today e Citynews senza licenza scritta. L'unica eccezione è stata la lettura una tantum del 23 ottobre autorizzata dall'owner. Tu non leggi Roma Today né Citynews, neanche attraverso i risultati di Google o le righe derivate. |
| DEC-101 | Un'immagine di evento si usa solo a risoluzione da card, con credito, link alla fonte e provenienza registrata. Nel repository le immagini non entrano perché sono dati di fonte (DEC-102, DEC-104). |
| DEC-106 | La portata di una notizia è separata dal luogo; il luogo decide la pagina. |
| `CLAUDE.md`, applicato a Codex come builder | Un cambiamento per ramo; test prima di ogni commit; mai marcare APPROVED il proprio lavoro; niente produzione n8n; dati di lavoro solo in staging. |
| `AGENTS.md` | Gerarchia normativa e verdetti; per il ruolo vale la deroga in testa a questo mandato. |

## 5. Che cosa consegnare

1. Un ramo proprio, `codex/replica-fonti-eventi`, partito come detto in testa, con:
   - `docs/sources/REPLICA_CODEX_FONTI_EVENTI_<data>.md`: per ogni compito, metodo, scelte con motivo, numeri aggregati e limiti;
   - gli script in `tools/fonti/replica-codex/`, se ne scrivi;
   - le righe con titoli o testi nella cartella privata fuori dal repository che ti indica l'owner, mai nel ramo (è pubblico).
2. I commit A, B e C del §1, nello stesso documento. Il commit C contiene il confronto:
   - una tabella con i tuoi numeri accanto a quelli del builder. I numeri del builder senza Roma Today si ricavano da
     `pagina/eventi.json` del pacchetto, da cui gli eventi di Roma Today sono già stati tolti: le cifre del suo rapporto li
     includono;
   - per ogni differenza oltre il 10%, la causa che trovi (scelta diversa, dato diverso, errore tuo o del builder);
   - un elenco delle scelte del builder che faresti diversamente, con il motivo.
3. La pull request si apre solo con la base indicata dall'owner (`OWNER_DECISION_REQUIRED`): contro `main` si porterebbe dietro
   tutta la PR #15, che non è ancora unita. Senza indicazione, lascia solo il ramo.
4. Nessuna decisione: le differenze di metodo che cambiano il perimetro vanno come `OWNER_DECISION_REQUIRED`.

## 6. Istruzioni pratiche

**Rete.**
- Se l'ambiente non ha accesso al web, fai R2 e R3 solo sui dataset del pacchetto e sul testo del 26 ottobre
  (`letture_web/canali/`). Conta a parte, come «non verificati», gli eventi e i siti senza testo, e dichiaralo.
- Senza rete, in R1 usa i punti del gazetteer di `letture_web/geo_gazetteer_punti.json` e dichiaralo come passo riusato.

**Apify.** Nessun token e nessun run: il tetto è 0 $, salvo un'indicazione scritta dell'owner. Il pacchetto contiene già tutti i
dataset e tutti gli input.

**Strumenti del builder.**
- `tools/fonti/leggi_eventi_siti.py` legge per impostazione predefinita `--schedario docs/wiki/fonti-eventi/fonti_eventi.json`.
  Quel file è vietato prima del commit B e contiene la scelta del canale del builder: passagli un elenco di siti ricavato da te.
- Gli script di `tools/fonti/lavoro-2026-10/` sono un archivio: contengono i percorsi dell'area di lavoro del builder e import di
  moduli rinominati. Per riusarli adatta percorsi e import, e dichiaralo.
- `tools/fonti/valida_eventi.py` e `tools/fonti/leggi_culture_roma.py` prendono i percorsi come argomenti.

**Test prima di ogni commit.**
- Ambiente: `pip install -r requirements.txt` (serve anche `openpyxl` per i fogli del pacchetto) e `npm ci`.
- Suite:
  - `cd gazetteer && python ../tests/test_guards.py`;
  - `node tests/test_parse_duration.js`, `node tests/test_council.js`, `node tests/test_lane_gate.js`,
    `node tests/test_workflow_safety.js`;
  - `python tests/test_fonti_eventi_build.py`, `python tests/test_leggi_culture_roma.py`, `python tests/test_leggi_eventi_siti.py`,
    `python tests/test_valida_eventi.py`;
  - `python tools/geo-assign/test_geo_assign.py`, `python tools/cronaca-prova/test_cronaca_prova.py`;
  - i test dei tuoi script in `tools/fonti/replica-codex/`, se ne scrivi.
- Incolla l'esito nella pull request.

**Pull request e commit.**
- Non chiedere `@codex review` sulla tua pull request: sarebbe una revisione di te stesso. La revisione la chiede l'owner.
- La specifica v2.5 citata in `CLAUDE.md` non serve per questo lavoro di analisi.
- Compila il modulo della pull request e dichiara il lane atteso, come chiede `AGENTS.md`: con script in `tools/` non è GREEN
  (`autonomy/lane_gate.js`).
- Chiudi ogni messaggio di commit con la riga «Autore: Codex (replica fonti eventi)».

**Lingua.** Rapporto e messaggi di commit in italiano, con i termini di questo mandato (pagina QN, canale, promotore, errore
grave).

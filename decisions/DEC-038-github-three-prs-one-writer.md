# DEC-038 — GitHub: più PR nel giro, un solo scrittore, il ramo aggiornato non più obbligatorio

Status: DECIDED (15 novembre 2026, owner, sulle proposte del builder), in prova fino al 30 novembre 2026 (punto 2)
Supersedes in part: DEC-028, domanda 2, nella sola regola «Una PR alla volta»; DEC-032,
punto 4, dove dice che quella regola resta; DEC-031, Impact, nella sola espressione «una
alla volta»; DEC-013, «What is unchanged», nella sola riga del ramo aggiornato con `main`.
Le quattro decisioni restano invariate e non si riaprono; ciascuna riceve un rimando sotto
la riga `Status:` (`decisions/README.md`, regola 2). Il resto di DEC-028 e di
`docs/github/PROTOCOLLO.md` resta in vigore.
Blocks: nothing.

Question: come si accorcia la coda delle PR su GitHub, dove ogni lavoro aspetta che il
precedente abbia finito il suo giro, senza tornare alle raffiche di scritture che hanno
preceduto le restrizioni dell'account?

Contesto:
- **La coda.**
  - Fino a questa decisione nel giro di revisione stava una PR alla volta, per i quattro
    workstream e per il coordinatore insieme (`docs/github/PROTOCOLLO.md`, sezione 2,
    punto 3, com'era).
  - Delle ultime cinque PR unite, dalla #50 alla #54, due hanno fatto quattro o cinque giri
    di Codex con rilievi: la #53 cinque, con 5, 3, 5, 3 e 1 rilievi; la #51 quattro (3, 3,
    2 e 2), cioè il tetto, e poi, con il permesso dell'owner, una quinta revisione
    sull'ultima testa, senza rilievi nuovi. Le altre tre ne hanno fatto uno o nessuno: un
    rilievo la #50 e la #54, nessuno la #52.
  - La #53 è durata circa 4 ore (aperta il 14 novembre alle 17:20 UTC, unita alle 21:09) e
    la #51 quasi due giorni (primo commit il 12 novembre alle 23:57 UTC, unita il 14 alle
    17:16); la #50 e la #52 circa dieci minuti. Numeri letti su GitHub il 15 novembre 2026.
  - Intanto il resto aspetta: la #53 ha aspettato la #51 e la #54 la #53; il timeout di C
    ha aspettato la #53 e poi la #54, e la decisione su YouTube dall'audio, che arriva con
    la PR dopo questa, la #54.
- **Il riallineamento.** Il ruleset `main-pr-only` chiede il ramo aggiornato con `main`:
  dopo ogni merge la PR seguente va riallineata, con un push in più, la CI e di solito
  un giro di Codex in più. Nel log di `main`: cinque «Merge main into … after #…» il
  12 novembre e tre «Merge main into … the branch was behind» il 14 e il 15. Togliere
  quell'obbligo era già fra le scelte aperte dell'owner (`PASSAGGIO_2026-11-14.md`,
  scelta 5, nella cartella di passaggio su Drive).
- **Perché ci sono le regole.**
  - DEC-028 le ha fissate dopo le restrizioni dell'account di ottobre.
  - Il 5 novembre il supporto di GitHub ha indicato come causa alcune parole chiave nel
    contenuto del repository, non il ritmo (intestazione di PROTOCOLLO;
    `docs/github/AUDIT_2026-10-30.md`, sezione F). Le regole sono rimaste come prudenza.
  - L'audit del 30 ottobre però ha visto raffiche prima dei blocchi: il 29 ottobre, in
    circa dieci minuti, quattro PR tolte dalla bozza e quattro revisioni di Codex partite
    insieme (DEC-028, Context). Da qui le salvaguardie del punto 2.
- **Un solo scrittore c'è già.** Scrive su GitHub solo il coordinatore; un workstream
  consegna il branch come bundle git nella sua cartella Drive (DEC-031, punto 4;
  `docs/pilota/CONTRATTI.md`, sezione 4).
- **La rete dopo il merge.** La CI gira su ogni PR e su ogni push su `main`
  (`.github/workflows/checks.yml`).

Options: le quattro proposte del builder nella sessione «Stato workflow aperti», che non si
escludono. Sono i
quattro punti della Regola, nell'ordine della bozza che l'owner ha approvato: 1, il ramo
aggiornato non più obbligatorio; 2, fino a tre PR nel giro; 3, la revisione interna; 4, il
lavoro in parallelo fuori da GitHub.

Claude recommendation: le quattro opzioni sono proposte del builder; il passaggio della
sessione non registra una preferenza fra loro.

Owner's words, 15 novembre 2026: «Sì, prepara la decisione per le opzioni 1 e 2 ma anche
3 e 4.»

## Regola

Dove una regola va oltre le parole dell'owner o la proposta accolta, lo dice: è una
lettura del builder, che l'owner conferma con il merge.

1. **Il ramo aggiornato non è più obbligatorio.**
   - L'owner toglie dal ruleset `main-pr-only` l'opzione «Require branches to be up to date
     before merging» (Settings → Rules → Rulesets → `main-pr-only`, dentro «Require status
     checks to pass»). È un'impostazione dell'owner, che non aspetta questa PR. Finché
     GitHub chiede ancora il ramo aggiornato per il merge, il coordinatore riallinea come
     prima e lo dice all'owner.
   - Resta tutto il resto: PR obbligatorie, CI verde, nessun thread aperto, e GitHub che
     non unisce una PR in conflitto.
   - Prima di dire all'owner che una PR è pronta, il coordinatore fa girare in locale le
     suite sulla PR unita al `main` di quel momento. Riallinea il ramo solo se c'è un
     conflitto, se quella prova fallisce o finché GitHub lo chiede ancora.
   - Se la CI su `main` si rompe dopo un merge, la correzione è la prima PR a passare.
2. **Fino a tre PR nel giro insieme, una per workstream.**
   - Nel giro sta al più una PR per workstream (A, B, C, D) e una del coordinatore
     (decisioni e contratti), e al più tre in tutto.
   - Lettura del builder, sulle parole «nel giro» e «aperta»: una PR è nel giro da quando
     si apre a quando revisione e CI sono finite sulla sua ultima testa, come nel
     protocollo di prima. «Aperta» vuol dire aperta su GitHub e non fermata dall'owner,
     fino al merge, anche a giro finito. Una PR che l'owner ha fermato (oggi la #16 e la
     #21, in bozza) non è nel giro e non tiene i file comuni, finché l'owner non la rimette
     in lavoro: era già così con una PR alla volta.
   - Due PR nel giro insieme non cambiano gli stessi file. I file comuni stanno in una sola
     PR aperta alla volta: `docs/pilota/CONTRATTI.md`, `decisions/`, `CLAUDE.md`,
     `AGENTS.md`, `docs/github/`. Lettura del builder: `package.json` fa eccezione e non è
     fra i file comuni, perché quasi ogni PR vi aggiunge il suo test, sulla stessa riga, e
     il conflitto è banale. Lo risolve il coordinatore riallineando il ramo (punto 1),
     nello stesso push delle correzioni quando ce n'è uno in attesa.
   - **Un solo scrittore.** Nel pilota la sessione del coordinatore è l'unica che scrive su
     GitHub (DEC-031, punto 4); resta la regola di una sola sessione alla volta sull'account
     (PROTOCOLLO, sezione 2, punto 1, invariato). Le chat dei workstream non scrivono su
     GitHub: consegnano il branch come bundle git nella loro cartella Drive (CONTRATTI,
     sezione 4), e il coordinatore lo verifica, fa girare i test e apre la PR.
   - **Scaglionate**, così le revisioni di Codex non partono a raffica:
     - fra l'apertura, o il passaggio da bozza a pronta, di due PR diverse almeno 15 minuti;
     - mai due PR tolte dalla bozza insieme;
     - fra due push su PR diverse almeno 5 minuti.
   - I tetti orari di PROTOCOLLO, sezione 3, restano per sessione, quindi valgono per
     tutte le PR insieme.
   - Il merge resta dell'owner, su notifica. Dopo ogni merge il coordinatore controlla che
     le altre PR aperte non siano in conflitto, prima di segnalare la successiva come
     pronta. Lettura del builder: se è in conflitto una PR già segnalata, il coordinatore
     dice all'owner che quella notifica non vale più.
   - **Ritorno indietro.** Al primo segnale di restrizione (PROTOCOLLO, sezione 5) si
     torna a una PR alla volta, oltre agli stop già previsti, e si avvisa l'owner. Lettura
     del builder: ci si resta finché l'owner non dice altrimenti; le PR già aperte restano
     aperte, senza chiuderle né riportarle in bozza, si riprende a lavorare su una alla
     volta, prima le fusioni pronte, e non se ne apre un'altra finché quelle nel giro non
     hanno finito.
   - **Prova fino al 30 novembre 2026.** Il coordinatore riporta all'owner le PR unite al
     giorno, i giri di Codex per PR e ogni segnale. L'owner conferma o torna alla regola di
     prima. Lettura del builder: in prova è la regola di questo punto, le tre PR nel giro,
     e un ritorno riguarda questo punto; i punti 1, 3 e 4 restano finché l'owner non li
     cambia. L'esito, conferma o ritorno, si registra con una entry nuova, e finché non c'è
     vale questa decisione (`decisions/README.md`, regola 2).
   - Lettura del builder, per i repository dell'account senza workstream (DEC-030; oggi
     `QuartieriNews/ComitatoAciliaNord`): la proposta parla solo dei workstream del
     pilota, quindi lì resta una PR alla volta nel giro, e quella PR conta fra le tre.
3. **Una revisione interna prima di aprire.**
   - Chi prepara il lavoro lo fa rivedere, prima di consegnarlo, da un revisore interno che
     non l'ha scritto: un subagent che riceve il diff e i contratti, non le conclusioni di
     chi ha scritto. Le correzioni vanno nello stesso commit.
   - Il coordinatore non apre una PR senza quella revisione. La revisione e le sue risposte
     stanno nel bundle o nel passaggio, non su GitHub. Lettura del builder: «nel bundle»
     vuol dire nella consegna, in un file accanto al bundle nella cartella Drive del
     workstream, non in un commit del branch, che finirebbe su GitHub. È materiale di
     lavoro della PR che segue, non una revisione nel senso di DEC-007 né un rapporto di
     `reviews/`: l'archivio della revisione di Codex resta la PR.
   - Non è un ciclo di Codex, che resta il revisore della PR, e il tetto dei quattro cicli
     resta (`AGENTS.md`, DEC-012).
   - Obiettivo: le PR che oggi fanno 4–5 giri di Codex ne fanno 2–3. La prova del punto 2
     lo misura.
4. **Il lavoro che non ha bisogno di GitHub va avanti in parallelo.**
   - Le chat dei workstream costruiscono e provano senza aspettare la coda: prove e sonde
     in staging su n8n e Drive, bozze delle pagine, preparazione delle PR successive.
   - Lettura del builder, per le regole di consumo (`CLAUDE.md`, «Consumption»): due o tre
     chat di lavoro insieme, oltre a quella del coordinatore. Ognuna chiude con il suo
     passaggio.

Impact:
- `docs/github/PROTOCOLLO.md`: l'intestazione; sezione 2, il punto 3 (le PR nel giro) e un
  punto 5 nuovo (la revisione interna); sezione 3, gli intervalli fra PR diverse e i tetti
  orari per tutte le PR insieme; sezione 4, la prova prima della notifica e il controllo
  delle altre PR aperte dopo un merge; sezione 5, il ritorno a una PR alla volta;
  sezione 6, i dati della prova.
- `CLAUDE.md`: le chat dei workstream non scrivono su GitHub e consegnano un bundle; la
  revisione interna prima di aprire.
- `docs/pilota/CONTRATTI.md`, sezione 4: i rimandi a questa decisione e al protocollo, e la
  consegna del bundle dopo la revisione interna.
- `docs/pilota/WORKSTREAM_A.md`, sezione 5: la riga sulla PR alla volta dice che vale per
  le PR di A, con il rimando al punto del protocollo.
- I rimandi sotto `Status:` in DEC-028, DEC-032, DEC-031 e DEC-013. Lettura del builder:
  gli ultimi tre non erano nella proposta; entrano per `decisions/README.md`, regola 2.
- `AGENTS.md` e DEC-007 non cambiano: `AGENTS.md` non ripete la regola di una PR alla
  volta, e la revisione interna non è una revisione di DEC-007 (punto 3).
  `docs/autonomy/IDENTITY_AND_PERMISSIONS.md` non cambia: rimanda a DEC-013, che porta il
  rimando.
- Il ruleset `main-pr-only`: un'impostazione dell'owner (punto 1).
- Il punto 4 non entra in altri file: vale da questa entry.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n, lane gate o CI.

Decided by: owner · Date: 15 novembre 2026 · Affected components: `docs/github/PROTOCOLLO.md`,
`CLAUDE.md`, `docs/pilota/CONTRATTI.md` (sezione 4), `docs/pilota/WORKSTREAM_A.md`
(sezione 5), DEC-028, DEC-032, DEC-031, DEC-013, il ruleset `main-pr-only` del repository
QN, le sessioni del coordinatore e dei workstream.

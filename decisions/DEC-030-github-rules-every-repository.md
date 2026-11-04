# DEC-030 — Le regole di GitHub valgono per ogni repository dell'account, non solo per QN

Status: DECIDED (4 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Supersedes in part: DEC-028, punto 1 («app GitHub di Claude sul solo repository QN»), e
DEC-029, punto 3 («collaborator with the Write role on QN only») con il passo «Install the
Claude GitHub App on QN only». Le due decisioni restano invariate e non si riaprono; ricevono
un rimando sotto la riga `Status:` (`decisions/README.md`, regola 2).
Blocks: nothing.

Question: il protocollo di DEC-028 e l'account macchina di DEC-029 valgono anche per gli
altri repository dell'account `QuartieriNews` in cui scrivono gli agenti? Oggi ce n'è uno,
`QuartieriNews/ComitatoAciliaNord`, il sito del Comitato di Quartiere Acilia Nord.

Contesto (fatti del 4 novembre 2026):
- **GitHub limita l'account, non il repository.** Una restrizione di `QuartieriNews` ferma
  tutti i suoi repository, e le scritture su ciascuno contano per l'account intero.
- **Il repository.** Sito Astro pubblicato su Cloudflare. La sua storia sono 12 commit di
  sessioni Claude, tutti del 29 ottobre fra le 16:48 e le 23:24 ora italiana, scritti
  direttamente su `main` senza pull request. Uno serviva solo a far ripartire la
  pubblicazione su Cloudflare. Sono stati spinti prima del passaggio a `QN-Builder`, quindi
  con la connessione di Claude di allora; quale account risulti va letto nel registro
  attività del repository, che il builder di QN non ha letto.
- **L'audit non lo conosce.** Il 30 ottobre GitHub ha risposto 403 al builder di QN, e
  `docs/github/AUDIT_2026-10-30.md` non nomina questo repository: le scritture della sera del
  29 non sono fra i suoi fatti.
- **Un'automazione ci scrive già.** Il workflow `notizie-facebook.yml` gira sei volte al
  giorno. Quando trova post nuovi fa un commit e un push come `github-actions[bot]`, con il
  token del workflow; se fallisce apre una issue, al massimo una aperta alla volta. Sono
  scritture di un'app, non dell'account dell'owner né di `QN-Builder`.
- **Lo stato.** L'owner ha già reso `QN-Builder` collaboratore di `ComitatoAciliaNord` e il
  collegamento di Claude ci arriva con permesso di push; `QN-Builder` non ci ha ancora
  scritto.
- **Un secondo account macchina non è un'opzione.** I Termini di GitHub (B.3) ammettono un
  solo account macchina gratuito oltre all'account personale.

Options:
A. **CHOSEN.** Un solo regime per tutto l'account. Protocollo e account macchina valgono per
   ogni repository dell'account in cui scrivono gli agenti. Una sola sessione di agente
   scrive alla volta su tutto l'account, non per repository. `QN-Builder` è collaboratore, e
   l'app Claude è installata, su ognuno di quei repository. Il testo resta uno, in QN; gli
   altri repository hanno un `CLAUDE.md` breve che lo richiama.
B. A, ma ogni repository tiene una propria copia del protocollo.
C. `ComitatoAciliaNord` resta fuori: ci scrive l'account dell'owner, con le sole regole di
   ritmo.

Claude recommendation: A. Con B nascono due testi che si allontanano a ogni modifica. C
lascia scritture automatiche sull'account dell'owner, contro DEC-029 punto 4, e tiene il
rischio sull'account che è già stato limitato.

Owner's words, 4 novembre 2026: «DEC-030: A».

## Regola

1. **Ambito.** `docs/github/PROTOCOLLO.md` e DEC-029 valgono per ogni repository
   dell'account `QuartieriNews` in cui scrivono gli agenti. Il testo del protocollo è uno
   solo, in QN.
2. **Uno scrittore alla volta, sull'account.** Più sessioni possono lavorare insieme, anche
   su repository diversi, ma una sola alla volta scrive su GitHub. Le altre lavorano in
   locale e scrivono dopo. Una sessione che sta per scrivere e sa di un'altra attiva si
   ferma e lo chiede all'owner.
3. **Prima di ogni nuovo repository.** Prima della prima scrittura di un agente, l'owner
   rende `QN-Builder` collaboratore del repository e lo aggiunge all'accesso dell'app Claude.
4. **Un segnale vale per tutti.** Un segnale di restrizione su un repository dell'account
   ferma le scritture su tutti (protocollo, sezione 5).
5. **I siti si pubblicano a blocchi.** Su un repository che pubblica a ogni push, come
   `ComitatoAciliaNord` su Cloudflare, le modifiche si raccolgono, si mostrano all'owner in
   anteprima e si pubblicano con un push per blocco, non uno per ritocco. Se la
   pubblicazione non parte, la si rilancia dal pannello del servizio, mai con un commit
   vuoto. Non servono pull request né revisioni Codex per ogni modifica del sito.
6. **Ogni repository richiama il protocollo.** Un `CLAUDE.md` breve, aperto da
   `QN-Builder` con una pull request, rimanda a questa decisione e al protocollo e ne
   riassume le regole; dove il riassunto e il protocollo differiscono, vale il protocollo.
7. **Le automazioni con identità propria restano.** `notizie-facebook.yml` scrive come
   `github-actions[bot]` e non cambia. Per il protocollo, sezione 2 punto 1, conta come job
   pianificato solo mentre gira.

Impact:
- **Owner.**
  - Collaboratore e app su `ComitatoAciliaNord`: già fatti.
  - La bio di `QN-Builder` nomina i repository dell'account, non più il solo QN.
  - Per ogni nuovo repository: i due passi del punto 3.
  - Il costo: a volte una sessione aspetta l'altra, e durante il lavoro sul sito le
    modifiche si vedono prima in anteprima e solo dopo online.
- **Repository QN.**
  - `docs/github/PROTOCOLLO.md`: l'ambito, lo scrittore unico sull'account e il segnale di
    restrizione su un repository dell'account.
  - I rimandi sotto `Status:` in DEC-028 e DEC-029.
- **Repository `ComitatoAciliaNord`.** Il `CLAUDE.md` del punto 6, con una pull request di
  `QN-Builder` dopo la fusione di questa decisione.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n, lane gate o CI di QN.

Decided by: owner · Date: 4 novembre 2026 · Affected components: account GitHub
`QuartieriNews`, `QuartieriNews/ComitatoAciliaNord`, profilo di `QN-Builder`,
`docs/github/PROTOCOLLO.md`, DEC-028, DEC-029.

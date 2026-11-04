# DEC-030 — Le regole di GitHub valgono per ogni repository dell'account, non solo per QN

Status: OPEN (4 novembre 2026, aperta dal builder su richiesta dell'owner)
Supererebbe in parte: DEC-028, punto 1 («app GitHub di Claude sul solo repository QN»), e
DEC-029, punto 3 («collaborator with the Write role on QN only») con il passo «Install the
Claude GitHub App on QN only». Le due decisioni restano invariate e non si riaprono; alla
decisione ricevono un rimando sotto la riga `Status:` (`decisions/README.md`, regola 2).
Blocks: le scritture degli agenti su `QuartieriNews/ComitatoAciliaNord`, finché non è decisa.

Question: il protocollo di DEC-028 e l'account macchina di DEC-029 valgono anche per gli
altri repository dell'account `QuartieriNews` in cui scrivono gli agenti? Oggi ce n'è uno,
`QuartieriNews/ComitatoAciliaNord`, il sito del Comitato di Quartiere Acilia Nord.

Contesto (fatti del 4 novembre 2026):
- **GitHub limita l'account, non il repository.** Una restrizione di `QuartieriNews` ferma
  tutti i suoi repository, e le scritture su ciascuno contano per l'account intero.
- **Il repository.** Sito Astro pubblicato su Cloudflare. La sua storia sono 12 commit di
  sessioni Claude, tutti del 29 ottobre fra le 16:48 e le 23:24 ora italiana, scritti direttamente su
  `main` senza pull request. Sono stati spinti prima del passaggio a `QN-Builder`, quindi con
  la connessione di Claude di allora; quale account risulti va letto nel registro attività
  del repository, che il builder di QN non ha letto.
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
A. **Un solo regime per tutto l'account.** Protocollo e account macchina valgono per ogni
   repository dell'account in cui scrivono gli agenti. Una sola sessione di agente scrive
   alla volta su tutto l'account, non per repository. `QN-Builder` è collaboratore, e l'app
   Claude è installata, su ognuno di quei repository. Il testo resta uno, in QN; gli altri
   repository hanno un `CLAUDE.md` breve che lo richiama.
B. A, ma ogni repository tiene una propria copia del protocollo.
C. `ComitatoAciliaNord` resta fuori: ci scrive l'account dell'owner, con le sole regole di
   ritmo.

Claude recommendation: A. Con B nascono due testi che si allontanano a ogni modifica. C
lascia scritture automatiche sull'account dell'owner, contro DEC-029 punto 4, e tiene il
rischio sull'account che è già stato limitato.

Impact (con A):
- **Owner.**
  - Collaboratore e app su `ComitatoAciliaNord`: già fatti.
  - La bio di `QN-Builder` nomina i repository dell'account, non più il solo QN.
  - Per ogni nuovo repository in cui scrivono gli agenti: gli stessi due passi, prima della
    prima scrittura.
- **Repository QN.**
  - `docs/github/PROTOCOLLO.md`: l'ambito, cioè ogni repository dell'account in cui scrivono
    gli agenti, e la regola dello scrittore unico estesa all'account.
  - I rimandi sotto `Status:` in DEC-028 e DEC-029.
- **Repository `ComitatoAciliaNord`.**
  - Un `CLAUDE.md` che richiama il protocollo di QN e ne riassume le regole, con una pull
    request di `QN-Builder`.
  - Le modifiche al sito si raggruppano: un push per gruppo di modifiche provate in locale,
    non un push per ritocco. Niente commit vuoti per riavviare la pubblicazione su
    Cloudflare.
  - `notizie-facebook.yml` resta com'è. Per il protocollo, sezione 2 punto 1, conta come job
    pianificato solo mentre gira.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n, lane gate o CI di QN.

Decided by: — · Date: — · Affected components: account GitHub `QuartieriNews`,
`QuartieriNews/ComitatoAciliaNord`, profilo di `QN-Builder`, `docs/github/PROTOCOLLO.md`,
DEC-028, DEC-029.

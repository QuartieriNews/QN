# DEC-028 — Con quale identità e con che ritmo l'automazione lavora su GitHub

Status: OPEN (OWNER_DECISION_REQUIRED)
Blocks: la ripresa del lavoro sulle pull request dopo lo sblocco dell'account; ogni nuova
automazione che scrive su GitHub (sessioni degli agenti, canale API delle revisioni, job
settimanali).

Context:
- **Due blocchi.** L'account `QuartieriNews` è finito due volte sotto i controlli
  anti-abuso di GitHub.
  - Dal 9 ottobre 2026: revisione manuale; Codex nativo e GitHub Actions sono rimasti
    fermi fino al 29 ottobre.
  - Il 29 ottobre sera, poco dopo lo sblocco: repository e pull request rispondono 404
    a chi non è autenticato.
  - Il motivo preciso non è noto e lo può dire solo il supporto GitHub.
- **Chi agisce.** Tutta l'automazione scrive come l'account personale dell'owner, perché
  DEC-013 ha sospeso la separazione delle identità:
  - push, commenti e modifiche delle sessioni di Claude Code;
  - i rapporti del canale API (`tools/sources-study/codex_check.js`), pubblicati per
    intero come commenti dell'owner;
  - il job settimanale «AI QN Watch», che pusha sul branch
    `technical-council/ai-watch-2026-09-14` e non è un'attività pianificata di Claude.
- **Volumi.**
  - La PR #15 ha 359 commit e circa 420.000 righe prima della separazione.
  - I lotti di revisione hanno prodotto decine di commenti lunghi in poche ore.
  - Il 29 ottobre, in circa dieci minuti, il builder ha fatto 13 scritture: quattro PR
    tolte dalla bozza, una chiusura e riapertura, due push, una PR nuova, due descrizioni
    riscritte, un commento e una chiusura. In più sono partite quattro revisioni Codex
    in contemporanea.
- **Pagare non cambia le regole.** Nessun piano a pagamento esonera dai controlli
  anti-abuso: valgono per tutti i piani.
- **Audit del 30 ottobre** (`docs/github/AUDIT_2026-10-30.md`, sola lettura).
  - Nessun codice del repository scrive su GitHub e la CI è in sola lettura.
  - La CI non è partita dal 16 settembre al 14 ottobre.
  - Le raffiche di scritture: il 16 settembre (160 commit), l'8 ottobre (15 commit via API
    in tre minuti dal job di watch), il 15 ottobre (101 commenti e risposte, fino a 12 in
    un minuto) e il 29 ottobre.
  - Ci sono state 27 richieste di revisione senza risposta.
  - Due sblocchi su due sono stati seguiti entro poche ore da una raffica e da un nuovo
    blocco.
  - I limiti ufficiali dell'API non sono mai stati avvicinati.
  - La causa resta non dimostrata.

Question 1 — Con quale identità agisce l'automazione?

Options:
A. Come oggi: l'account personale dell'owner, con le regole di ritmo della domanda 2.
B. Un'organizzazione GitHub (gratuita) diventa proprietaria del repository.
   - L'owner resta amministratore con il proprio account.
   - Gli agenti scrivono attraverso app installate sull'organizzazione (l'app GitHub di
     Claude, il connettore Codex già in uso), non con il token personale dell'owner.
   - Prima va verificato che la revisione Codex parta sulle PR aperte da un'app. Con
     `QN-Builder` l'integrazione era autorizzata per account, e quel limite ha portato a
     DEC-013.
C. Torna un account macchina per il builder, cioè la separazione di DEC-010 sospesa da
   DEC-013, con il costo che DEC-013 ha misurato.

B e C riprendono, in due forme diverse, la separazione che DEC-013 ha sospeso. La
decisione che sceglie una delle due supera DEC-013 in parte, con i due collegamenti
richiesti da `decisions/README.md`, regola 2. In entrambi i casi l'owner tornerebbe a
poter approvare le PR degli agenti. Il gate di approvazione che DEC-013 ha perso diventa
quindi di nuovo possibile, ma resta un'impostazione che decide l'owner.

Claude recommendation: B, dopo la risposta del supporto e dopo la verifica su Codex.
Fino ad allora A, con le regole della domanda 2.

Question 2 — Regole di ritmo per ogni agente che scrive su GitHub.

Le regole sono in `docs/github/PROTOCOLLO.md`, richiamato da `CLAUDE.md`. I numeri
sono prudenziali: le soglie anti-spam di GitHub non sono pubbliche, e i limiti ufficiali
dell'API (80 contenuti al minuto, 500 all'ora) sono molto più alti.
- Almeno 5 secondi fra due scritture qualsiasi.
- Almeno 60 secondi fra due scritture di contenuto (commento, risposta, review, richiesta
  di revisione, PR nuova), e al massimo 10 in un'ora per sessione.
- Al massimo 30 scritture di stato in un'ora (push, risoluzioni, modifiche, bozza o pronta,
  chiusure).
- Tetti dimezzati nelle prime 24 ore dopo uno sblocco.
- Una PR alla volta. Si toglie dalla bozza, si apre o si chiede la revisione di una PR
  solo quando la precedente ha finito il suo giro (revisione e CI).
- Niente chiusure e riaperture e niente commit vuoti per far ripartire la CI. Se la CI
  non parte, lo si dice all'owner.
- Una sola sessione di agente scrive su un repository alla volta.
- I controlli periodici leggono poco: nessun polling, si aspettano le notifiche.

Options: a) adottarle così; b) adottarle con numeri diversi; c) nessuna regola scritta.

Claude recommendation: a).

Question 3 — Il canale API delle revisioni (`codex_check.js`).

Options:
A. Resta come ripiego, ma solo quando il canale nativo non risponde per un'ora (oggi il
   limite è di dieci minuti), con un commento per ciclo.
B. Resta, ma nel commento vanno solo il verdetto e i rilievi; il rapporto integrale va in
   un file. Questo tocca DEC-007, perché la PR è l'archivio della revisione, e la
   supererebbe in parte.
C. Si dismette ora che il canale nativo risponde di nuovo.

Claude recommendation: A.

Question 4 — Il job settimanale «AI QN Watch».

La PR #14 è chiusa dal 29 ottobre e il job continua a pushare sul suo branch.

Options: a) sospenderlo fino alla decisione sul Council (PR #16); b) farlo scrivere su
Drive invece che su GitHub; c) lasciarlo com'è.

Claude recommendation: b), oppure a) se il Council non ne ha bisogno.

Question 5 — Che cosa contiene la copia di riserva del repository.

La copia settimanale fuori da GitHub (`docs/github/CONTINUITA.md`) serve a lavorare
durante una restrizione. Un `git bundle` porta tutta la storia, e la storia contiene dati
che le decisioni hanno poi tolto dai file: i campioni di DEC-104, le colonne di DEC-109, il
file eventi della PR #18. La storia non è mai stata riscritta ed è già pubblica.

Options:
a) bundle completo, solo nella cartella privata di QN Hub su Drive, dove DEC-102 vuole i
   dati delle fonti;
b) solo l'ultima versione dei branch (`git archive`), senza storia: il lavoro fatto
   durante una restrizione torna su GitHub come patch;
c) nessuna copia.

Claude recommendation: a).

Impact:
- **Domanda 1, B.** Trasferimento del repository all'organizzazione. GitHub reindirizza i
  vecchi indirizzi. Il ruleset e le impostazioni del repository vanno riverificati dopo
  il trasferimento. Le app vanno installate sull'organizzazione.
  `docs/autonomy/IDENTITY_AND_PERMISSIONS.md` va riscritto per lo stato nuovo.
- **Domanda 2.** Una sezione in `AGENTS.md` e una riga in `CLAUDE.md`.
- **Domanda 3, A.** Una costante e il README di `tools/sources-study/`.
- **Domanda 4.** Nessun file del repository: il job non è qui.
- **Domanda 5.** Una procedura settimanale per l'owner o per il builder, e una cartella
  su Drive.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n, lane gate o CI.

Decided by: — · Date: — · Affected components: account e repository GitHub, `AGENTS.md`,
`CLAUDE.md`, `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`,
`tools/sources-study/codex_check.js`, `docs/github/`, DEC-007, DEC-013.

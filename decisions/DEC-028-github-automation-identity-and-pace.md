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

Le regole andrebbero in `AGENTS.md` e `CLAUDE.md`. I numeri sono prudenziali: GitHub non
pubblica soglie.
- Al massimo una scrittura al minuto e dieci in un'ora per sessione. Contano come
  scritture: push, commenti, risposte, modifiche e cambi di stato delle PR.
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

Impact:
- **Domanda 1, B.** Trasferimento del repository all'organizzazione. GitHub reindirizza i
  vecchi indirizzi. Il ruleset e le impostazioni del repository vanno riverificati dopo
  il trasferimento. Le app vanno installate sull'organizzazione.
  `docs/autonomy/IDENTITY_AND_PERMISSIONS.md` va riscritto per lo stato nuovo.
- **Domanda 2.** Una sezione in `AGENTS.md` e una riga in `CLAUDE.md`.
- **Domanda 3, A.** Una costante e il README di `tools/sources-study/`.
- **Domanda 4.** Nessun file del repository: il job non è qui.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n, lane gate o CI.

Decided by: — · Date: — · Affected components: account e repository GitHub, `AGENTS.md`,
`CLAUDE.md`, `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`,
`tools/sources-study/codex_check.js`, DEC-007, DEC-013.

# DEC-032 — Revisione automatica di Codex, e nessun tetto a PR e merge

Status: DECIDED (9 novembre 2026, owner nella sessione del builder)
Supersedes in part: DEC-031, punto 7 (la revisione chiesta dall'owner, circa quattro volte al
giorno). DEC-031 resta invariata e non si riapre; riceve un rimando sotto la riga `Status:`
(`decisions/README.md`, regola 2).
Blocks: nothing.

Question: con la revisione automatica di Codex attiva, chi chiede la revisione e quante PR
e merge al giorno sono ammessi?

Contesto:
- Il 9 novembre l'owner ha attivato sul repository QN la revisione automatica di Codex:
  tutte le PR, a ogni push, in modalità esaustiva.
- La PR #24, aperta da `QN-Builder` alle 17:05 UTC, pochi minuti dopo l'impostazione,
  non è stata rivista né all'apertura né dopo un push: il connettore chiedeva un account
  Codex. DEC-031, punto 7, l'ha registrato.
- La PR #25, aperta da `QN-Builder` alle 17:18 UTC, è stata rivista da sola all'apertura
  (innesco «PR opened»), e di nuovo dopo il push delle 17:26 UTC (innesco «New
  commits»). L'impostazione funziona anche per le PR di `QN-Builder`.
- In tutto la #25 ha avuto cinque revisioni automatiche: una all'apertura e una per
  ciascuno dei quattro push. La quinta, oltre il tetto dei quattro giri, l'ha concessa
  l'owner ed è tornata senza rilievi; l'owner ha fatto il merge alle 20:40 UTC.
- La PR #26, aperta da `QN-Builder` alle 20:42 UTC con questa decisione, non è stata
  rivista all'apertura: il connettore ha risposto chiedendo un account Codex, come sulla
  #24. Quindi per le PR di `QN-Builder` l'avvio automatico succede spesso ma non sempre, e la
  causa non è nota.

Owner's words, 9 novembre 2026: «imamgino che avendo le code review automatizzate possiamo
rimuovo il limite delle 4 e ottimizzare all interno dei limiti che ci siamo dati per il ban»;
«per le PR non metterei limiti. Posso farle dal cellulare. Se mi mandi una notifica e nella
notifica c'è il link corretto e devo solo fare merge. E' davvero un secondo». Sul caso
della #26, fra le opzioni poste dal builder: «Fix DEC-032, then review».

## Regola

1. **La revisione parte da sola,** all'apertura di ogni PR e a ogni push. Nessuno scrive
   `@codex review`, tranne nei due casi del punto 3.
2. **Un push per ciclo di correzioni.** Ogni push avvia una revisione, quindi la regola del
   protocollo (sezione 2, punto 2) conta ancora di più.
3. **Quando Codex non parte, la richiesta è dell'owner,** perché `QN-Builder` non è
   collegato a Codex. Se il connettore risponde chiedendo un account Codex, il builder lo
   dice subito all'owner, in una riga con il link alla PR, e l'owner scrive
   `@codex review`. Se invece Codex tace per più di un'ora dopo un push, il builder lo dice
   all'owner e l'owner sollecita una volta.
4. **Nessun tetto al numero di PR e di merge al giorno.** Restano il ritmo del protocollo
   (sezione 3), una PR alla volta nel giro di revisione (sezione 2, punto 3) e il tetto di
   quattro giri di revisione per lavoro (`AGENTS.md`, DEC-012), che solo l'owner può
   superare.
5. **Merge su notifica.** Quando una PR è pronta (CI verde, nessun rilievo aperto, nessun
   conflitto), il coordinatore manda all'owner una notifica con il link alla PR, e l'owner
   fa il merge. Il merge resta dell'owner (DEC-012, DEC-029).

Impact:
- `docs/github/PROTOCOLLO.md`, sezione 4: la revisione automatica e il sollecito dell'owner.
- `CLAUDE.md`: la regola della ri-revisione.
- Il rimando sotto `Status:` in DEC-031.
- `docs/pilota/CONTRATTI.md`, sezione 4: il rimando passa da DEC-031, punto 7, a DEC-032.
- Nessun cambiamento a pipeline, gazetteer, prompt, n8n o CI.

Decided by: owner · Date: 9 novembre 2026 · Affected components: `docs/github/PROTOCOLLO.md`,
`CLAUDE.md`, DEC-031, `docs/pilota/CONTRATTI.md`, impostazioni di Codex del repository QN.

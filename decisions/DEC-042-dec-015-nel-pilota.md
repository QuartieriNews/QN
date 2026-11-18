# DEC-042 — DEC-015 vale nel pilota privato, con Claude come seconda AI

Status: DECIDED (18 novembre 2026, owner al coordinatore)
Blocks: la pubblicazione nel prototipo di ogni canale del pilota, finché quel canale non ha la
seconda verifica; la chiave Anthropic su n8n, che porta l'owner.

Question: DEC-015 (11 settembre 2026) fissa il modello di pubblicazione di ogni blocco: una prima
AI produce, una seconda AI funzionalmente indipendente verifica sulla fonte, e si pubblica solo se
passano tutte e due e i controlli deterministici. Il pilota privato (DEC-031) l'applica? Se sì, a
quali canali, e con quale seconda AI? `docs/pilota/WORKSTREAM_A.md` (sezione 9) e
`docs/pilota/CONTRATTI.md` (sezione 7 A), come DEC-036, la danno per valida «se l'owner la
conferma per il pilota».

Contesto:
- Su n8n oggi l'unico modello è di OpenAI (credenziale `openAiApi`). La seconda AI deve essere di
  un'altra famiglia: la richiesta di DEC-015 è l'indipendenza funzionale fra produzione e
  verifica.
- Nel pilota i canali A e B non scrivono ancora elementi: la seconda verifica è già nelle loro PR
  successive (CONTRATTI, sezione 7 A e 7 B). Il canale C scrive eventi che il prototipo
  (`tools/site/`) mostra, con la coda e il campione di DEC-103.

Options:
- A. DEC-015 vale solo per il canale A, da A5.
- B. DEC-015 vale per ogni canale del pilota: A, B e C.
- C. DEC-015 vale per A e B; gli eventi di C restano con DEC-103.

Claude recommendation: nessuna data prima della scelta; la domanda aperta era quella di
`WORKSTREAM_A.md`, sezione 9.

Owner's words, 17 novembre 2026: «DEC-015 vale per il pilota: SÌ»; «qui chiaramente la seconda AI
è Claude». 18 novembre 2026, alla domanda su quali canali: «A, B e C».

## Regola

1. **DEC-015 vale nel pilota privato per ogni canale: A, B e C.** Un elemento si pubblica nel
   prototipo solo se passano la prima AI, la seconda e i controlli deterministici del canale; nel
   dubbio va in coda (`docs/REVIEW_QUEUE.md`).
2. **La seconda AI è Claude** (Anthropic), di un'altra famiglia rispetto al modello della prima
   (OpenAI). Quale modello di Claude, con quale prompt e a che costo lo fissa la PR che porta la
   verifica in ciascun canale, dentro la quota del canale (CONTRATTI, sezione 5).
3. **Le soglie sono quelle di DEC-015:** zero errori critici, al più un errore materiale ogni 50
   elementi del campione, campione stratificato per canale.
4. **La chiave.** La credenziale Anthropic su n8n la crea l'owner, prima della prima PR che la
   usa. Finché non c'è, nessun canale ha la seconda verifica.
5. **Il canale C.** [DA CONFERMARE CON L'OWNER: che cosa mostra il prototipo degli eventi di C
   finché C non ha la seconda verifica.]

Impact:
- `docs/pilota/CONTRATTI.md`, sezione 7 A: la seconda verifica di DEC-015 non è più «se l'owner la
  conferma»; sezione 7 B: la seconda verifica comprende quella di DEC-015; sezione 7 C: la riga
  del punto 5.
- `docs/pilota/WORKSTREAM_A.md`: la riga della chiave (sezione 2) e il punto aperto della sezione
  9 per DEC-015; DEC-014 e DEC-020 restano aperte lì.
- DEC-015 e DEC-036 non cambiano: questa entry risponde alla condizione che DEC-036 pone.
- Nessun cambiamento a gazetteer, prompt, n8n di produzione, lane gate o CI.

Decided by: owner · Date: 18 novembre 2026 · Affected components: canali A, B e C del pilota,
`docs/pilota/CONTRATTI.md` (sezione 7), `docs/pilota/WORKSTREAM_A.md`, credenziali di n8n.

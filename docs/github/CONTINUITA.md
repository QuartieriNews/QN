# Continuità: copia del repository e lavoro durante una restrizione

Status: in vigore per DEC-028, punto 5 (bundle completo, solo su Drive privato). Le evidenze sono in
`docs/github/AUDIT_2026-10-30.md`.

## Perché

Il 30 ottobre GitHub ha risposto 403 alla sessione del builder. Il lavoro preparato la sera
prima esisteva solo nel container della sessione, che è temporaneo. Una copia completa
fuori da GitHub permette di continuare in locale e di rimettere il lavoro su GitHub dopo,
senza perderlo e senza aggirare il blocco.

## La copia settimanale

Si fa da un clone completo, con tutti i branch scaricati:

```bash
git fetch --all --prune
git bundle create "QN-$(date +%Y-%m-%d).bundle" --all
git bundle verify "QN-$(date +%Y-%m-%d).bundle"
```

- **Dove va.** Il file va su Drive, in una cartella privata di QN Hub (per esempio
  `90 Backup`). Ne bastano le ultime quattro.
- **Chi la carica.** L'owner, oppure il builder con il connettore Drive e il permesso
  dell'owner.
- **Quando.** Settimanalmente, e in più alla fine di ogni sessione che lascia commit non
  pushati: per quelli basta un bundle dei soli branch toccati.

**Cosa non contiene.** Il repository non contiene segreti: le chiavi stanno
nell'ambiente, non nei file (`council/README.md`). Il bundle porta solo ciò che è nei
branch.

Verifica del 30 ottobre: nella storia di tutti i branch scaricati nessuna corrispondenza
con i formati delle chiavi OpenAI, GitHub, Google, Slack, Apify e delle chiavi private.
Quattro branch remoti non sono stati scaricati, fra cui `claude/openai-api-key-check-7n6dfz`.
Vanno controllati allo stesso modo prima della prima copia.

**Cosa contiene.** Il bundle porta **la storia**. La storia contiene dati che le
decisioni hanno poi tolto dai file:
- i campioni rimossi per DEC-104;
- le colonne di testo tolte da `handoff_data/` per DEC-109;
- `tools/site/events_2026-10.json` nel branch della PR #18.

La storia non è stata riscritta: è una scelta dell'owner, ed è già pubblica su GitHub.
Sul Drive privato quei dati stanno dove DEC-102 vuole i dati delle fonti. Per questo il
bundle va solo nella cartella privata di QN Hub, mai altrove (DEC-028, punto 5).

## Lavorare durante una restrizione

1. **Non si scrive su GitHub**, nemmeno per provare (`PROTOCOLLO.md`, sezione 5).
2. **Si riparte dal bundle.**
   - Per una sessione nuova: carica nella sessione l'ultimo bundle da Drive e lancia
     `git clone QN-AAAA-MM-GG.bundle QN`.
   - Per una sessione esistente: lancia `git fetch <bundle> <branch>:<branch>`.
3. **Si lavora e si fa commit in locale.** Prima di chiudere la sessione si crea un bundle
   dei branch toccati, `git bundle create lavoro.bundle <branch>... ^origin/main`, e lo si
   consegna all'owner.
4. **A restrizione finita** si rimettono i branch su GitHub una PR alla volta, con il ritmo
   del protocollo. Prima vanno le fusioni pronte.

**Cosa non si fa.** Niente mirror attivi, altri account o altri provider usati per
continuare a collaborare «al posto» di GitHub, e niente ricaricamenti ripetuti per vedere
se il blocco è finito. Un mirror in sola lettura come copia di riserva è una scelta futura
(P2-3) e richiede una decisione.

## Ricorso e conformità

Le mitigazioni tecniche non sostituiscono il ricorso. Durante una restrizione:
- l'owner apre o aggiorna il ticket con il supporto GitHub;
- descrive in modo veritiero chi scrive sull'account e come;
- chiede quale attività ha causato la restrizione.

La risposta del supporto prevale su questo documento.

# DEC-044 — Canale A: le eccezioni dell'owner al tetto di 1 € della prova (DEC-037, punto 4)

Status: DECIDED (16 novembre 2026, owner nelle sessioni del builder del canale A, punti 1 e 2;
19 novembre 2026, owner nella sessione del coordinatore, punto 3; registrata dal coordinatore
nella notte fra il 19 e il 20 novembre 2026)
Supersedes in part: DEC-037, punto 4, la sola frase «il tetto della prova resta 1 €», per le sole
spese e prove della Regola (punti 1–3): la prova di confronto l'ha passata il 16 novembre per
scelta dell'owner, e due prove nuove sui luoghi hanno un tetto loro. Non è un cambio generale del
tetto. DEC-037 resta invariata e non si riapre; riceve un rimando sotto la riga `Status:`
(`decisions/README.md`, regola 2). Per tutto il resto DEC-037 resta in vigore, compresi i punti 5
e 6.
Blocks: niente. Lo stress test dei luoghi continua dentro il suo tetto (Regola, punto 3).

Question: DEC-037, punto 4, tiene a 1 € il tetto della prova di confronto della trascrizione. Fra
il 16 e il 19 novembre l'owner ha chiesto di spendere di più su quella prova e ha dato un tetto a
sé a due prove nuove sui luoghi, che i passaggi chiamano eccezioni a quel tetto e chiedono al
coordinatore di registrare. Quali sono, con quali cifre, e che cosa cambiano?

Contesto:
- DEC-037, punto 4: la prova di confronto (`docs/pilota/WORKSTREAM_A.md`, sezione 6) si allarga a
  più modelli, con e senza guida, giudicati prima sui nomi di luogo; «il tetto della prova resta
  1 €». Punto 6: la spesa si tiene sotto controllo e non ferma un flusso; una prova fatta da una
  chat dichiara prima la spesa prevista e dopo quella fatta.
- Il tetto di 2 € delle «prove in staging» di `WORKSTREAM_A.md`, sezione 7, è un altro tetto:
  questa entry non lo tocca.
- Le spese, dai passaggi del canale A nella cartella dei passaggi su Drive, in dollari come le
  addebitano OpenAI e Groq (per il mese vale DEC-035):

| Giorno | Che cosa | Spesa | Passaggio |
|---|---|---|---|
| 15/11 | il confronto su 7 finestre, OpenAI poi Groq | ≤ 0,73 $ + 0,120 $, «circa 0,85 $»; «Resto del tetto circa 0,23 $» | `PASSAGGIO_2026-11-15_prova-groq.md`, sezione 1 |
| 16/11 | due sedute intere, 117 minuti | «circa 0,99 $»; «In tutto la prova ha speso circa 1,84 $ (≈ 1,7 €)» | `PASSAGGIO_2026-11-16_sedute-intere.md`, sezione 2 |
| 16/11 | due passate di Groq su una seduta nuova | «circa 0,04 $»; poi «La spesa di tutta la prova è circa 1,9 $» | `PASSAGGIO_2026-11-16_due-passate.md`; `PASSAGGIO_2026-11-16_luoghi-geografia.md`, «Da non perdere» |
| 16/11 | i luoghi decisi con la geografia, tre sedute | «circa 0,12 $, sotto il tetto di 0,20 $» | `PASSAGGIO_2026-11-16_geografia-prove.md`, `…_geografia-terza.md`, `…_geografia-quarta.md`, sezione 4 |
| 16/11 | i luoghi decisi da un modello (sonde 1390–1391, corsa 1396) | 0,0514 $; caso peggiore stimato prima 0,19 $ | `PASSAGGIO_2026-11-16_luoghi-modello-prova.md`, sezione 4 |
| 17/11 | la seduta del Municipio V (corse 1561–1572) | Groq «circa 0,038 $», OpenAI 0,0007 $ | `PASSAGGIO_2026-11-17_luoghi-municipio-V.md`, sezione 4 |
| 19/11 | lo stress test, passi 1 e 2 | 0 | `PASSAGGIO_2026-11-19_stress-test-luoghi-passi-1-2.md`, sezione 5 |

- Chi abbia fissato il tetto di 0,20 $ delle prove della geografia i passaggi non lo dicono. Del
  piano di quelle prove il suo passaggio dice «Viene dall'owner, 16/11» (`…_luoghi-geografia.md`),
  e stimava le due passate della seduta nuova in «circa 0,05 $».
- Il passaggio del coordinatore del 19/11 (`PASSAGGIO_2026-11-19_luoghi-verdetto-3-4-novembre.md`,
  sezione 7) nomina due eccezioni da registrare: «1 € del 16/11, 2 € dello stress test». Due
  passaggi del 16/11 ne chiedono una terza, il tetto di DEC-037 passato
  (`…_sedute-intere.md`, sezione 1: «Il coordinatore lo registra»; `…_luoghi-geografia.md`: «Il
  coordinatore la registra»). Il coordinatore le registra tutte e tre (Regola, punti 1–3).

Options: nessuna fra opzioni scritte. La spesa del punto 1 viene da una richiesta dell'owner senza
cifra; i tetti dei punti 2 e 3 da piani che l'owner ha approvato. I passaggi non riportano opzioni
poste all'owner.

Claude recommendation:
- Punto 1: non registrata. La richiesta è dell'owner; il builder ne ha riportato la spesa.
- Punto 2: non registrata. Il piano del 16/11 è del builder, ma il tetto vi sta fra le «Decisioni
  dell'owner», e chi l'abbia proposto il passaggio non lo dice.
- Punto 3: non registrata come consiglio. Il piano dello stress test sta nel passaggio del
  coordinatore del 19/11 (sezioni 5 e 6), e l'owner l'ha approvato con il tetto. Se i 2 € fossero
  la proposta del coordinatore o una scelta dell'owner fra opzioni, il passaggio non lo dice: la
  sua versione delle 11:21 UTC parla di «piano e scelte dell'owner nella chat del 19/11», e il
  testo della domanda non c'è.

Owner's words. Sulla spesa e sui tetti, le sole parole dell'owner fra virgolette nei passaggi sono
quelle del 19 novembre, «sì, va bene così, procedi». Il resto è come lo riportano i passaggi del
builder e del coordinatore, copiato com'è; nelle citazioni il grassetto dei passaggi è tolto.
- 16 novembre, mattina, sessione del builder (`PASSAGGIO_2026-11-16_sedute-intere.md`, sezione 1):
  «In chat, il 16/11, l'owner ha chiesto:», fra l'altro, «di mettere a confronto gpt-transcribe (il
  top di gamma) e Groq turbo con guida (il migliore per costi e benefici) su almeno una seduta
  intera di 30 minuti, aumentando la spesa»; e poi: «Il tetto di 1 € di DEC-037, punto 4, è quindi
  superato per scelta dell'owner». Il passaggio del pomeriggio (`…_luoghi-geografia.md`, «Da non
  perdere»): «La spesa di tutta la prova è circa 1,9 $, sopra il tetto di DEC-037 per scelta
  dell'owner».
- 16 novembre, pomeriggio, sessione del builder (`PASSAGGIO_2026-11-16_luoghi-modello.md`,
  «Decisioni dell'owner (16/11)», punto 3): «Tetto di spesa: 1 € per tutta la prova (eccezione
  dell'owner al tetto di DEC-037; il coordinatore la registra). L'owner considera questa parte
  importante.»
- 19 novembre, sessione del coordinatore (`PASSAGGIO_2026-11-19_luoghi-verdetto-3-4-novembre.md`,
  sezione 3): l'owner ha risposto «sì, va bene così, procedi». Il passaggio riassume così che cosa
  ha approvato: il piano della sezione 5, «tre sedute nuove più quella del Municipio V già passata
  dal piccolo, tetto di spesa 2 € per tutto lo stress test (trascrizione più modello; eccezione a
  DEC-037 da registrare dal coordinatore), e il criterio di successo della sezione 6».

## Regola

1. **La prova di confronto oltre 1 € (16 novembre, mattina).** La richiesta dell'owner di
   confrontare i modelli su sedute intere «aumentando la spesa» è un'eccezione a DEC-037, punto 4,
   per quella prova. Una cifra dell'owner i passaggi non la riportano. A fine giornata la prova e
   le sue prosecuzioni del 16/11 avevano speso circa 2,0 $: circa 1,9 $ fino alle due passate, più
   circa 0,12 $ delle prove della geografia (somma del coordinatore sulle cifre del Contesto).
   Lettura del coordinatore, che l'owner conferma con il merge: l'eccezione copre quella spesa.
   Le sedute intere e le due passate i passaggi del 16/11 le contano nella stessa prova («La spesa
   di tutta la prova è circa 1,9 $»); le prove della geografia sono state fatte sul piano che
   «Viene dall'owner», con un tetto loro di 0,20 $, di cui i passaggi non dicono l'autore. Per la
   spesa che viene dopo, il tetto di DEC-037, punto 4, resta com'è: questa entry non lo alza e non
   ne fissa uno nuovo per la prova di confronto.
2. **I luoghi decisi da un modello: tetto 1 € (16 novembre, pomeriggio).** Un tetto a sé, di 1 €
   per tutta la prova, che i passaggi chiamano eccezione al tetto di DEC-037. Spesa: 0,052 $
   di OpenAI (0,0514 $ il 16/11, 0,0007 $ il 17/11). La trascrizione della seduta del Municipio V
   del 17/11 (Groq, circa 0,038 $) il passaggio la riporta a parte, senza dire su quale tetto
   conta; anche contata qui, la prova resta sotto 0,10 $. Quella seduta stava nei prossimi passi del
   passaggio prima, «con l'approvazione dell'owner sulla spesa», con le stime «circa 0,05 $» per
   Groq e «circa 0,002 $» per il modello piccolo (`PASSAGGIO_2026-11-17_luoghi-accordo.md`,
   «Prossimi passi», 2); il passaggio della seduta si apre con «L'owner ha chiesto una seduta di un
   altro Municipio». Una risposta dell'owner sulla cifra i passaggi non la citano.
3. **Lo stress test dei luoghi: tetto 2 € (19 novembre).** Per tutto lo stress test (sezioni 4–6
   del passaggio del coordinatore del 19/11), trascrizione più modello. Prima di ogni chiamata, la
   stima del caso peggiore contro il tetto (stesso passaggio, sezione 5); che cosa si fa se la stima
   non ci sta, il passaggio non lo dice. Al passaggio dei passi 1 e 2 la spesa era 0; il passo 3 lo
   fa una chat a sé, e la sua spesa la dichiara il suo passaggio (DEC-037, punto 6).
4. **Che cosa non cambia.**
   - Sono cifre una tantum, per queste prove sole: non alzano la quota mensile di A (DEC-037,
     punto 5; la divisione di oggi è in CONTRATTI, sezione 5) né le altre quote, e il budget del
     pilota resta 50 € al mese (DEC-031, punto 6).
   - La loro spesa conta nel mese di A e nel totale del pilota come ogni altra, con il suo file in
     `costi/` (CONTRATTI, sezione 5); il totale del mese si converte come dice DEC-035.
   - Le cifre in euro di questa entry, come quelle dei passaggi che cita, sono al cambio prudente di
     DEC-037, punto 6 (1,84 $ ≈ 1,7 €).
   - DEC-037, punto 6, resta com'è: la spesa si tiene sotto controllo, una prova dichiara prima la
     spesa prevista e dopo quella fatta, e gli avvisi del coordinatore non cambiano.

Impact:
- DEC-037: il rimando sotto la riga `Status:` (`decisions/README.md`, regola 2).
- Nessun altro file. `docs/pilota/WORKSTREAM_A.md` dice ancora «Il tetto resta 1 €» (sezione 6) e
  conta «il confronto (tetto 1 €)» fra le spese una tantum (sezione 7): un rimando lì è un lavoro
  a sé, fuori da questa entry.
- Spesa: nessuna nuova. Le cifre sono già spese o già autorizzate; questa entry non apre spesa.
  Il tetto della notte del 19→20 novembre (`MANDATO_NOTTE_2026-11-19.md`) non è fra queste
  eccezioni e questa entry non lo tocca.
- DEC-031, punto 6, DEC-035, DEC-036, punto 6, e DEC-037, punti 5 e 6, restano invariate. Niente
  in produzione; gazetteer, prompt, registro dei venue, flussi n8n e CI invariati.

Decided by: owner · Date: 16 e 19 novembre 2026 · Affected components: canale A del pilota (le
prove di confronto e dei luoghi in staging, flussi `staging_A_confronto*`), `costi/` di A,
DEC-037 (il rimando).

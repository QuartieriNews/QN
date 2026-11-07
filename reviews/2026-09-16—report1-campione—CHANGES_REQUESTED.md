# Controllo C2 — campione del Report 1 (notizie candidate, evidenze, copertura)

Verdetto del revisore: **CHANGES_REQUESTED** (3 rilievi bloccanti, 6 non bloccanti, 1 conferma).
Revisore: Codex, `gpt-5.3-codex`, effort `high`, Responses API con `store: false`.
Data: 16 settembre 2026, 00:12 (Europe/Rome). Costo stimato: 0,20 € (25.345 token in / 12.308 out).

## Cosa è stato rivisto

Campione stratificato di 45 notizie candidate su 1.227 (`report1/campione_c2.py`, seed
`2026-06-C2`, almeno 5 per fonte e 5 per esito di deduplicazione), più gli aggregati, contro
`SPECIFICA_LETTURA.md`, `RICOSTRUZIONE_2026-06_SCHEMA_DB.md` e il registro delle decisioni
D1–D3. Mandato: controllo C2 della nota di fattibilità §9.6.

Criteri di accettazione esercitati: `tests/test_guards.py` e `tests/test_parse_duration.js`
passano; validazione dell'Operator su tutte le 1.370 righe prodotte dai lettori (titoli ≤ 12
parole, sintesi ≤ 60, vocabolario, qualità, evidenza presente): zero violazioni.

## Risposta ai rilievi

| # | Rilievo | Esito |
|---|---|---|
| 1 | **Bloccante.** `municipio` non normalizzato, con forme `Municipio IX` e fino a 15 Municipi su una notizia | **accettato**, e peggiore di come appariva: 524 righe su 1.227 portavano l'etichetta di categoria del portale al posto del luogo del fatto. Ora il campo è normalizzato ai soli numeri romani; il Municipio scritto nel testo prevale su quello della fonte, e un'etichetta che nomina più di tre Municipi è trattata come categoria, non come luogo. Righe non normalizzate: **0** |
| 2 | **Bloccante.** Scala di qualità incoerente: `alta` su fatti annunciati o con data dedotta | **accettato**. Regola meccanica: un `avviso`, un ordine del giorno, un convegno o un'interrogazione non superano `media`, e nemmeno una riga senza `data_fatto`. Le `alta` scendono da 46 a 14 |
| 3 | **Bloccante.** `N0832` marcata duplicato pur essendo una replica con data propria | **accettato**. Per gli Eventi il duplicato ora richiede la **stessa data**; stesso luogo e stesso oggetto a un giorno di distanza diventano `dubbio`, che è il trattamento che il metodo §4.1 prescrive quando (a) e (b) valgono e (c) è incerto |
| 4 | Non bloccante. Evidenza più corta della sintesi in tre righe | **accettato come residuo dichiarato**. Le sintesi restano sostenute dal testo dell'item, ma la frase citata non porta tutti i numeri. Non lo correggo riscrivendo le sintesi a valle: sarebbe l'Operator che riscrive il lavoro del lettore senza rileggere il testo |
| 5 | Non bloccante. `N0539` con Municipio I e toponimi extra-urbani | **accettato**. Un toponimo che il gazetteer non risolve e che non trova un Municipio ora marca `toponimo_da_verificare = sì` |
| 6 | Non bloccante. `tier = text_contains` senza Municipio né zona | **accettato**, e ha portato alla scoperta sotto |
| 7 | Non bloccante. `N0812` anonimizza il titolo di un'opera, contro D2 | **accettato come residuo dichiarato**: una riga, segnalata, da correggere con la rilettura dell'item e non con una sostituzione a valle |
| 8 | Non bloccante. `N0421` ha in nota "deduplicazione rinviata" ma stato `unica` | **accettato come residuo dichiarato**: la nota è del lettore ed è vera al momento della lettura, perché la deduplicazione è un passo successivo. La formula va cambiata nella specifica, non la nota |
| 9 | Aggregati coerenti; esplicitare l'intervallo di resa | **accettato**: il rapporto riporterà l'intervallo con le percentuali e la base del campione |
| 10 | Conferma che i nomi dentro toponimi, sedi, titoli e URL sono in linea con D1–D3 | preso atto |

## Un difetto che il controllo ha fatto emergere per via indiretta

Il rilievo 6 ha mostrato che dopo la correzione **ogni** riga `text_contains` restava senza zona.
La causa non era quella corretta: `build_db.py` leggeva dal localizzatore la chiave `zone`, che
non esiste — quella giusta è `zona`. **La zona è stata vuota per l'intero database fin dalla
prima costruzione**, la deduplicazione non ha mai potuto usare la chiave di luogo più fine, e il
Municipio dedotto dal gazetteer non è mai stato usato. Corretto: 448 notizie hanno ora una zona
su 63 zone distinte, e le righe con Municipio salgono a 1.131 su 1.227.

Il revisore non ha segnalato questo difetto e non poteva: non vedeva il codice. L'ha reso
visibile un rilievo su un'incoerenza di superficie.

## Residui aperti

Tre, tutti non bloccanti e dichiarati sopra (4, 7, 8). Non marco questo lavoro APPROVED: il
verdetto è del revisore e la fusione è dell'owner.

## Testo integrale del controllo

CHANGES_REQUESTED

1. **Bloccante — localizzazione/schema (`municipio`)**: in più righe A1 il campo `municipio` non rispetta lo schema (`I–XV`), usa forme miste (`Municipio IX`) e in **N0070** contiene addirittura più Municipi non pertinenti alla singola notizia (III;V;VI;VIII;XI) mentre `municipio_testo=VIII`. **Correzione**: normalizzare `municipio` a solo numero romano, un valore per notizia (qui `VIII`), lasciando eventuali pluralità solo in `municipio_testo`/`note`.

2. **Bloccante — scala qualità applicata in modo incoerente**: **N0152** è `alta` ma la data è dedotta da “questa mattina” + pubblicazione (quindi almeno `media`); **N0208** è `alta` pur essendo avviso di intervento programmato (da regola non oltre `media`); **N0638** è `bassa` ma fatto/luogo/data sono espliciti (resta `media` perché annunciato). **Correzione**: ricalcolare `qualita` con regola meccanica e aggiornare gli aggregati per qualità.

3. **Bloccante — deduplicazione probabilmente errata (falso duplicato)**: **N0832** è marcata `duplicato` (gemello `N0560`) ma la riga descrive una replica con **data/orario propri** e la nota stessa dice “una riga per data”; qui il rischio è collassare fatti distinti. **Correzione**: verificare il gemello e impostare `unica` (o `dubbio` solo se il gemello è la stessa data in altra fonte), poi audit di tutti i duplicati con regola “data ±1 giorno”.

4. **Non bloccante — evidenza locale troppo corta rispetto alla sintesi**: in **N0151**, **N0201**, **N0532** la sintesi porta numeri/dettagli non coperti dalla frase riportata in `evidenza_locale` (pur plausibilmente presenti nel testo completo). **Correzione**: o estendere `evidenza_locale` includendo i dati numerici chiave, o alleggerire la sintesi ai soli elementi coperti.

5. **Non bloccante — localizzazione dubbia**: **N0539** assegna `municipio=I` ma i toponimi in `luoghi` sono extra-urbani (Vicovaro/Roccagiovine/Monti Lucretili), anche se `toponimo_da_verificare=sì`. **Correzione**: impostare `municipio` a vuoto/non localizzato finché non c’è un aggancio territoriale coerente.

6. **Non bloccante — coerenza `tier_localizzazione`**: casi come **N1112** (`tier=text_contains`, `municipio` e `zona` vuoti, `toponimo_da_verificare=no`) sono poco interpretabili. **Correzione**: quando `text_contains` non porta a Municipio/zona, usare `ambiguous` o segnare `toponimo_da_verificare=sì`.

7. **Non bloccante — confine DEC-102 applicato in modo disomogeneo**: **N0812** anonimizza il titolo dell’opera (“Jackie”), mentre D1/D2 consente i titoli ufficiali anche se coincidono con un nome di persona; altrove (es. “Giulio Regeni – …”) il criterio è applicato correttamente. **Correzione**: mantenere verbatim i titoli di opere in modo uniforme.

8. **Non bloccante — dedup post-lettura da completare/pulire note**: **N0421** riporta in nota “stessa apertura descritta in A1_071: deduplicazione rinviata” ma lo stato è `unica`; la nota suggerisce lavoro sospeso o non riallineato. **Correzione**: rieseguire dedup interna A1 e rimuovere dalle note formule “rinviata” se il passaggio è concluso.

9. **Non bloccante (verifica aggregati)**: i totali allegati sono internamente coerenti (`1227 = 909+197+121`; somme per fonte/qualità/tier tornano). **Correzione**: nel Report esplicitare chiaramente l’intervallo di resa netta sostenibile dai dati (`909–1030`, cioè `74,1%–83,9%`, a seconda del trattamento dei `dubbio`) e la base campionaria usata per stime Eventi.

10. **Non bloccante (corretto, non segnalo difetto)**: ho evitato di segnalare come violazione DEC-102 i nomi dentro toponimi/sedi/titoli opere/URL (es. “Largo Marcello Mastroianni”, “Giulio Regeni – …”), perché in questo campione sono in linea con D1–D3.

---
Controllo C2, modello gpt-5.3-codex, effort high, token 25345 in / 12308 out, 2026-09-15T22:12:00.556Z

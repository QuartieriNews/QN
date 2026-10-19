# Wiki di contesto — che cos'è e come si usa

Il wiki è il retrobottega che dà contesto ai blocchi *istituzionale* e *notizie*
della pagina di quartiere. Non è un quinto blocco e non è una raccolta di schede
sulle persone (DEC-105: le persone compaiono solo nel ruolo pubblico). Arriva al
lettore come una riga sotto la notizia: «è la terza seduta saltata in un mese».

Tre pezzi, in quest'ordine di autorità:

| Pezzo | File | Cosa contiene | Chi lo scrive |
|---|---|---|---|
| **Schedario** | `schedario.json` | le cose che esistono: *luoghi* (id `L-`), *soggetti* (id `S-`: istituzioni, comitati, biblioteche, teatri…) e *questioni* (id `Q-`: fili che attraversano più voci). Ogni voce ha un id stabile, un nome canonico e le grafie viste (`alias`). | il build, dai dati dello studio fonti e dal registro fonti; le fusioni/divisioni di identità le decide una persona |
| **Diario** | `diario.json` | una voce datata per ogni notizia, agganciata alle schede che riguarda, con il riferimento alla fonte. Mai riscritto, solo esteso. | il build, dai per-item dello studio fonti |
| **Pagine** | `INDEX.md`, `municipi/*.md`, `anteprima.html` | stampe leggibili dello schedario e del diario, una per municipio | generate; non modificare a mano |

Rigenerare:

```bash
python tools/wiki/build_wiki.py --input <cartella con i Report*_notizie_*.csv> \
       --registry <registro_fonti.csv> --out docs/wiki
python tools/wiki/render_html.py --wiki docs/wiki --out docs/wiki/anteprima.html
```

I CSV di ingresso stanno su Drive (`QN Hub / 20 Packages / Fonti 2026-06` e il
registro fonti del 13 ottobre 2026) e non entrano nel repository. Nel repository
entra solo il derivato: titoli di una riga scritti dallo studio, mai il testo delle
fonti (DEC-109).

## Cosa dice questa prima versione (giugno 2026)

- 3.224 voci di diario da dieci fonti (notizie dei Municipi, atti, commissioni e
  consigli in streaming, YouTube dei Municipi, comunicati, eventi), al netto dei
  duplicati certi.
- 524 questioni, di cui 472 con almeno due voci. Il raggruppamento è quello dello
  studio fonti (stessa data e stesso luogo, oggetto a volte incerto); il campo
  `coerenza` (alta 266 · media 125 · bassa 81) dice quanta parte delle voci cita
  davvero lo stesso luogo principale. Le questioni a coerenza bassa sono sedute
  con più argomenti e vanno divise da una persona.
- 3.471 luoghi citati; sono agganciati a una zona di pubblicazione solo quando il
  nome coincide con il gazetteer (il gazetteer vince).
- 212 soggetti: le istituzioni che compaiono nel corpus più le 193 sorgenti
  «da tenere» del registro fonti.

## Cosa manca, deliberatamente

- Non c'è ancora un passaggio di giudizio sulle questioni: titolo, oggetto e
  confini vengono dallo studio, non da una lettura editoriale. È il lavoro che
  una persona (o un modello, con revisione) fa dopo, scheda per scheda.
- Maggio 2026 non c'è. Aggiungerlo allunga le questioni all'indietro ed è il modo
  per capire se il wiki vale: si decide dopo aver letto queste pagine.
- Non sono inclusi (file non scaricati in questa prima versione): RomaTV parte 5,
  YouTube Municipi parte 2, comunicati di Questura/Vigili del Fuoco/Polizia Locale.

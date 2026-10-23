# Wiki delle fonti eventi — che cos'è e come si usa

Risponde a una domanda sola: **dove andare a cercare nuovi eventi nelle fonti
primarie**. Per ogni fonte dice che cos'è, dove sta, su quale pagina QN pubblica,
quale indirizzo controllare e quanto rende. È il ramo "fonti" della wiki di contesto
(DEC-022): stessa logica, dati strutturati prima e pagine generate dopo, nessun testo
delle fonti nel repository.

Una **fonte** è un soggetto che produce eventi: un *luogo* che li ospita (teatro,
museo, club, parco), un *organizzatore* che li promuove (fondazione, associazione,
promoter) o un *aggregatore* che li elenca (culture.roma.it, Facebook, Roma Today).
Molte fonti sono luogo e organizzatore insieme.

| Pezzo | File | Cosa contiene | Chi lo scrive |
|---|---|---|---|
| **Schedario** | `fonti_eventi.json` | una voce per fonte: id stabile (`S-FE-…` se è nel registro del 13 ottobre 2026, altrimenti `S-EV-…`), nome e grafie viste (`alias`), ruoli, tipo, Municipio ufficiale, pagina QN, indirizzo e coordinate, canali (sito, Facebook, Instagram, pagina del luogo su culture.roma.it, biglietteria), **`dove_cercare`** (gli indirizzi da controllare, in ordine), eventi per aggregatore a ottobre 2026, quota di eventi rintracciabili alla fonte, decisione del registro | il build, dal foglio degli eventi di ottobre 2026 e dal registro fonti; le fusioni di identità le decide una persona |
| **Aggregatori** | `aggregatori.md` | una scheda per aggregatore: regole di accesso, cosa è stato misurato, rintracciabilità, sovrapposizioni | generato; i numeri vengono dal foglio |
| **Pagine** | `INDEX.md`, `municipi/*.md`, `per-pagina-qn.md` | stampe leggibili dello schedario: per Municipio, per pagina QN, e la lista delle fonti più produttive | generate; non modificare a mano |

## Come si usa

- Devo riempire la pagina di un quartiere: apro `per-pagina-qn.md`, cerco la pagina,
  seguo i link della colonna *dove cercare* in ordine (prima la pagina calendario già
  letta alla fonte, poi la pagina del luogo su culture.roma.it, poi il sito, poi gli
  eventi della pagina Facebook).
- Devo decidere quali fonti leggere ogni settimana: `INDEX.md`, tabella «Dove cercare
  per primi», ordinata per eventi prodotti nel mese.
- Devo capire se un aggregatore vale la pena: `aggregatori.md`.

## Rigenerare

```bash
python tools/wiki/build_fonti_eventi.py --input <cartella> --out docs/wiki/fonti-eventi
python tests/test_fonti_eventi_build.py
```

La cartella di ingresso contiene `eventi_unico.xlsx` (il foglio degli eventi di
ottobre 2026: Facebook via Apify, culture.roma.it, Roma Today, lettura diretta 13-31
ottobre, con geografia, rintracciabilità e doppioni), `registro_fonti.xlsx` (registro
del 13 ottobre 2026) e, facoltativo, `culture_luoghi.json` (coordinate delle pagine dei
luoghi di culture.roma.it). Stanno su Drive (`QN Hub / 20 Packages / Fonti 2026-06`) e
nell'anteprima privata, non nel repository: portano titoli di eventi, che sono testo
delle fonti (DEC-022, decisione dell'owner del 23 ottobre 2026 sulla PR 18).

## Regole che il build rispetta

- **Nessun testo delle fonti** (DEC-109, DEC-022): nello schedario entrano nomi di
  organizzazioni, indirizzi, canali e conteggi; mai un titolo o una descrizione di
  evento. Il test `T-FE-1` lo verifica con titoli sentinella.
- **Nomi di persone** (DEC-105): il build non ne aggiunge. Un promotore di Roma Today
  con la forma di un nome di persona è omesso e contato (`promotori_omessi`).
- **Il gazetteer vince**: la pagina QN di una fonte è la `publication_zone_id` più
  frequente fra i suoi eventi (metodo 1 o 2 del foglio); una stringa che non è nel
  gazetteer non viene scritta.
- **Identità**: due grafie sono la stessa fonte se coincidono dopo normalizzazione
  (accenti, punteggiatura, forme giuridiche, «Roma» in coda) o se condividono una
  chiave forte (id del luogo Facebook, pagina del luogo su culture.roma.it, chiave del
  registro). Le fusioni dubbie non si fanno: restano due voci, e le decide una persona.
- **Deterministico**: stessi ingressi, stessi byte.

## Cosa dice questa prima versione (ottobre 2026)

I numeri sono in `INDEX.md`. In sintesi: 1.465 fonti, di cui 370 dal registro del 13
ottobre; 650 luoghi e 596 organizzatori; 402 con un sito web; 1.023 con una pagina QN.
Le fonti senza Municipio sono per lo più organizzatori che a ottobre hanno prodotto
eventi fuori Roma o registrazioni del registro senza geografia.

## Cosa manca, deliberatamente

- Le fusioni di identità fra grafie diverse dello stesso soggetto (per esempio un
  teatro come luogo e la sua fondazione come organizzatore) non sono automatiche.
- La produttività è misurata su un mese solo; con il secondo mese si vedrà quali
  fonti pubblicano con regolarità.
- Roma Today resta un aggregatore letto una volta su indicazione dell'owner; non è un
  canale di lettura regolare (robots.txt e licenza Citynews).

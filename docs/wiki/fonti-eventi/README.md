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
| **Fusioni proposte** | `fusioni-proposte.md` | coppie di voci che probabilmente sono la stessa fonte scritta in due modi (stesso nome senza forme giuridiche, un nome dentro l'altro, refusi); il build non le fonde | generato; la fusione la decide una persona e si registra con una chiave forte comune |
| **Censimento** | `censimento-pagine.md` | le candidate uscite dal censimento delle pagine Facebook di associazioni del 24 ottobre 2026, raggruppate per verdetto della lettura automatica, con l'indirizzo da controllare; le pagine dormienti e scartate sono solo contate | generato; la decisione tenere/scartare spetta all'owner e va nel registro fonti |

## Come si usa

- Devo riempire la pagina di un quartiere: apro `per-pagina-qn.md`, cerco la pagina,
  seguo i link della colonna *dove cercare* in ordine (prima la pagina calendario già
  letta alla fonte, poi la pagina del luogo su culture.roma.it, poi il sito, poi gli
  eventi della pagina Facebook).
- Devo decidere quali fonti leggere ogni settimana: `INDEX.md`, tabella «Dove cercare
  per primi», ordinata per eventi prodotti nel mese.
- Devo capire se un aggregatore vale la pena: `aggregatori.md`.
- Devo decidere quali associazioni entrano nel registro: `censimento-pagine.md`, un verdetto alla
  volta (prima i «rientra», poi i «locale» e i «da valutare»).

## Rigenerare

```bash
python tools/wiki/build_fonti_eventi.py --input <cartella> --out docs/wiki/fonti-eventi
python tests/test_fonti_eventi_build.py
```

La cartella di ingresso contiene `eventi_unico.xlsx` (il foglio degli eventi di
ottobre 2026: Facebook via Apify, culture.roma.it, Roma Today, lettura diretta 13-31
ottobre, con geografia, rintracciabilità e doppioni), `registro_fonti.xlsx` (registro
fonti versione 4 del 24 ottobre 2026: le 370 voci del 13 ottobre, con le 220 pagine Facebook
verificate dall'owner portate a «tenere» e la decisione precedente conservata, più le candidate
della ricerca mirata per le 58 pagine QN con meno di cinque eventi futuri e della ricerca
«evento / eventi / festa + quartiere», decisione «candidata» finché l'owner non la cambia) e, facoltativo, `culture_luoghi.json` (coordinate delle pagine dei
luoghi di culture.roma.it) e, facoltativi, i due censimenti del 24 ottobre 2026: `associazioni_fonti.xlsx` (1.169 pagine
Facebook di associazioni) e `enti_terzo_settore_fonti.xlsx` (6.247 enti del terzo settore di Roma
iscritti al RUNTS); per ciascun soggetto dati di pagina, eventi futuri e post via Apify, sito
verificato, indirizzo geocodificato, verdetto automatico. Le email dei soggetti stanno solo in
questi file: il build non le legge e il test verifica che nessun indirizzo arrivi nelle pagine. Stanno su Drive (`QN Hub /
20 Packages / Fonti 2026-06`) e nell'anteprima privata, non nel repository: portano titoli
di eventi e testi di presentazione delle pagine, che sono testo delle fonti (DEC-022,
decisione dell'owner del 23 ottobre 2026 sulla PR 18).

## Regole che il build rispetta

- **Nessun testo delle fonti** (DEC-109, DEC-022): nello schedario entrano nomi di
  organizzazioni, indirizzi, canali e conteggi; mai un titolo o una descrizione di
  evento. Il test `T-FE-1` lo verifica con titoli sentinella.
- **Nessuna anonimizzazione** (DEC-105): chi ospita o organizza eventi è un soggetto del
  registro, persona o organizzazione che sia: una guida, un promoter, un regista o un
  curatore che lavorano a proprio nome stanno qui come un teatro. L'unica regola di
  contenuto: di un profilo personale Facebook (`profile.php`) non si scrive l'indirizzo,
  perché non è un canale di pubblicazione; il nome resta e il caso è contato
  (`profili_personali_senza_url`). Attori, registi e artisti di un singolo evento non
  sono fonti: stanno nei dati dell'evento, su Drive.
- **Il gazetteer vince**: la pagina QN di una fonte è la `publication_zone_id` più
  frequente fra i suoi eventi (metodo 1 o 2 del foglio); una stringa che non è nel
  gazetteer non viene scritta.
- **Identità**: due grafie sono la stessa fonte se coincidono dopo normalizzazione
  (accenti, punteggiatura, forme giuridiche, «Roma» in coda) o se condividono una
  chiave forte (id del luogo Facebook, URL della pagina Facebook, pagina del luogo su
  culture.roma.it, chiave del registro). Le fusioni dubbie non si fanno: restano due voci,
  e le decide una persona.
- **Il censimento propone, non decide**: una pagina del censimento entra come candidata
  con il suo verdetto automatico (`censimento.verdetto`); la decisione del registro resta
  quella del 13 ottobre finché l'owner non la cambia. Test `T-FE-7`.
- **Deterministico**: stessi ingressi, stessi byte.

## Cosa dice questa prima versione (ottobre 2026)

I numeri sono in `INDEX.md`. In sintesi: 5.099 fonti, di cui 1.606 nel registro versione 5
(370 del 13 ottobre, con le 220 pagine verificate dall'owner portate a «tenere»; 445 candidate della
ricerca mirata per le pagine deboli; 129 candidate della ricerca «evento / eventi / festa + quartiere»
del 24 ottobre; 676 candidate della lista supplementare del 25 ottobre per le 41 pagine con meno
eventi rispetto agli abitanti), 1.928 candidate dal censimento degli enti del terzo settore (RUNTS)
e 598 dal censimento delle pagine Facebook (le coincidenze con voci del registro sono fuse); 644
luoghi e 3.112 organizzatori; 3.213 con un sito web; 3.585 con una pagina QN; 376 fusioni proposte
da decidere.

La ricerca mirata del 24 ottobre ha dato a 56 delle 58 pagine QN deboli almeno tre fonti
da controllare (parrocchie, centri sociali anziani dagli elenchi ufficiali dei Municipi,
comitati di quartiere, biblioteche dall'elenco di Biblioteche di Roma, istituti comprensivi
dall'anagrafe MIUR, mercati rionali dai dati aperti, centri culturali, pro loco e consorzi);
restano scoperte Dragona-Dragoncello e Muratella.

Il censimento ha detto una cosa netta: di 1.169 pagine di associazioni, solo 19 hanno
eventi futuri su Facebook (verificato con due lettori diversi); gli eventi li annunciano
nei post (186 pagine con post datati di annuncio negli ultimi sei mesi) o sul sito (823
pagine ne espongono uno, 277 hanno una sezione eventi, 83 mostrano date future). Le 275
pagine dormienti restano fuori e si rileggono a marzo 2027.

## Cosa manca, deliberatamente

- Le fusioni di identità fra grafie diverse dello stesso soggetto (per esempio un
  teatro come luogo e la sua fondazione come organizzatore) non sono automatiche.
- La produttività è misurata su un mese solo; con il secondo mese si vedrà quali
  fonti pubblicano con regolarità.
- Roma Today resta un aggregatore letto una volta su indicazione dell'owner; non è un
  canale di lettura regolare (robots.txt e licenza Citynews).

# Registro fonti — template (S2-01)

Una scheda per fonte, compilata secondo `docs/sources/SOURCE_STUDY_METHOD.md` (M-0.3). Nel
repository stanno solo aggregati e metriche; i dati per item e il campione di originali
stanno su Drive, `QN Hub / 20 Packages / Fonti 2026-06/` (metodo §4.2, DEC-104: loop di
sviluppo AI con i campioni fuori dal repository). Nessun nome di persona, nessun testo
integrale. Ogni numero è marcato **M** (misurato), **S** (stimato) o **—** (mancante).

Stato: **vuoto** — compilazione dopo l'apertura dei domini (metodo §6).

| Campo | Valori ammessi / note |
|---|---|
| `id` | codice del metodo §2 (A1, A2, …, C1–C6, E1–E3, R1) |
| `blocco` | amministrazione · cronaca · eventi |
| `ente` | nome dell'ente o del portale |
| `sezione` | URL della pagina di elenco o del feed usato per il conteggio |
| `territorio` | città · Municipio N · quartiere |
| `argomenti` | tag liberi, pochi |
| `accesso` | web aperto · feed RSS · login · API |
| `formati` | HTML · PDF testo · PDF scansione · audio · video (più valori) |
| `riuso` | pagina licenza/termini trovata (sì/no), cosa dice in una riga, link; "da verificare (L11)" se manca |
| `mese` | 2026-06 (o 2026-05 con motivo) |
| `item_mese` | conteggio (M) — data e ora della lettura, paginazione completa sì/no |
| `frequenza` | item per settimana (M) |
| `ritardo_mediano_giorni` | fra fatto e pubblicazione, dove la data del fatto è nel testo (M o —) |
| `anticipo_eventi_giorni` | solo eventi: mediana fra pubblicazione e data dell'evento (M) |
| `eventi_futuri_30gg` | solo eventi: eventi con data nei 30 giorni dalla lettura (M) |
| `quota_toponimo` | % item con toponimo (M) |
| `quota_zona` | % item assegnabili deterministicamente a una delle 89 zone (M) |
| `quota_municipio` | % item assegnabili almeno al Municipio (M) |
| `duplicati` | % item già pubblicati da un'altra fonte del blocco; intervallo min–max se ci sono dubbi (M o S con n del campione) |
| `contributo_unico` | % item non presenti altrove (M o S) |
| `estrazione` | esito della prova: testo ottenuto sì/no; qualità leggibile / con errori / inutilizzabile |
| `costo_item` | tempo e costo per item dalla prova (M) |
| `intervento_umano` | minuti per item prevedibili (S) |
| `raccomandazione` | usare · integrare · riserva · escludere, con la ragione e la condizione che la cambierebbe |
| `drive` | link alla cartella dei dati per item e del campione |

## Schede

*(nessuna ancora)*

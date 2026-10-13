# Fonti locali per le pagine senza cronaca

Strumenti dello studio del 13 ottobre 2026 sulle fonti alternative (comitati, associazioni,
parrocchie, blog e periodici di zona, notiziari di Municipio) per le pagine QN che a giugno
2026 restano senza cronaca anche con la regola delle due fonti (DEC-108). Il rapporto, con
il metodo e i limiti, è `docs/sources/FONTI_PAGINE_SCOPERTE_2026-10.md`; serve a DEC-006.

Libreria standard di Python 3.10+, nessuna dipendenza.

| Passo | Comando | Che cosa fa | Limiti voluti |
|---|---|---|---|
| 1 Scoperta | agenti, uno per pagina e uno per Municipio, con ricerca web (modalità estesa, al massimo 5 ricerche per pagina) | candidate con tipo, canale, blocchi, territorio, evidenza di attività | nessun articolo aperto; social registrati solo come indirizzo; testate che escludono gli agenti AI non proposte |
| 2 Verifica | `verifica_accesso.py --out ESITO.json [--da 2026-07-01 --a 2026-10-01] URL…` | robots.txt (agenti AI esclusi per nome, tutti esclusi), riserva TDM (`tdm-reservation`, `Content-Signal`, `noai`, `tdmrep.json`), piattaforma, feed, attività nella finestra e giudizio sul canale lecito | una richiesta al secondo per host, user agent dichiarato; feed e API letti solo se il robots.txt li ammette; conteggio **M** dall'API WordPress, **S** (limite inferiore) da feed o sitemap; nessun titolo memorizzato |
| 3 Scettico | agente, un WebFetch per fonte | tenta di confutare attività, territorio e accesso delle fonti dichiarate usabili; in dubbio → `da_verificare` | — |
| 4 Tabella | `tabella.py RUN_DIR` | `fonti_pagine.json` → tabelle per pagina e per fonte del rapporto | — |

Verdetti: `usabile` (aperta, attiva, copre la pagina), `solo_metadati` (robots.txt o TDM
chiudono agli agenti: titolo, link e data da un motore), `inattiva`, `fuori_territorio`,
`canale_chiuso` (solo social: raccolta manuale, DEC-102), `non_raggiungibile`, `da_verificare`.

Test: `python3 tools/fonti-locali/test_fonti_locali.py` (nessuna rete).

`runs/2026-10-13/`: `verifica_<slug>.json` (esito dello strumento per pagina),
`fonti_pagine.json` (candidate, verdetti e motivi). Nomi di enti e di siti, URL, date e
conteggi: nessun titolo, nessun nome di persona.

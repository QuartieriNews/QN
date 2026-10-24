# Script di lavoro del blocco eventi, ottobre 2026 (non prodotti)

Copia di sicurezza degli script con cui sono stati costruiti, fra il 20 e il 24 ottobre
2026, il foglio unificato degli eventi (`eventi_unico.xlsx`), il censimento delle pagine
Facebook (`associazioni_fonti.xlsx`), la ricerca puntuale degli eventi senza fonte, la
ricerca mirata per le pagine QN deboli e il registro fonti versione 2. I file di dati che
leggono e scrivono stanno su Drive (`QN Hub / 20 Packages / Fonti 2026-06`) e nell'area di
lavoro della sessione (`$S`, passato come primo argomento), mai qui: portano titoli e testi
delle fonti (DEC-022, DEC-109).

Non sono strumenti del repository: niente test, percorsi dell'area di lavoro scritti
dentro, dipendenze da `openpyxl` e dalla rete (Nominatim, Apify, siti delle fonti). Sono
versionati perché l'area di lavoro è effimera e perché ogni numero del rapporto
`docs/sources/FONTI_EVENTI_STATO_2026-10-24.md` deve restare riproducibile. Gli strumenti
veri, con test, sono `tools/fonti/leggi_eventi_siti.py`, `tools/fonti/leggi_culture_roma.py`
e `tools/wiki/build_fonti_eventi.py`; i passi qui sotto che meritano di diventare strumenti
(geografia, doppioni, rintracciabilità) aspettano DEC-025 e la decisione sulla geografia
(pacchetto Metodo QN, `tools/geo-assign/qngeo.py punto`).

| Passo | Script | Ingresso → uscita |
|---|---|---|
| Foglio eventi Facebook da Apify | `build_xlsx.py` | dataset Apify → `facebook_eventi.xlsx` |
| Foglio unificato | `unico.py` | Facebook, culture.roma.it, Roma Today, fonti locali → `eventi_unico.xlsx` |
| Roma Today, scheda e sorgente | `rt_pass1.py`, `rt_pass2.py`, `rt_build.py`, `parse_dove.py` | 324 schede (lettura una tantum autorizzata) → campi di scheda, promotore, link |
| Geografia, metodo 1 e 2 | `geocode.py`, `geo_assign.py`, `metodo2.py`, `geocode_gaz.py`, `culture_luoghi.py` | indirizzi → Nominatim (cache) → poligoni ufficiali dei Municipi e delle suddivisioni → zona QN; metodo 2: suddivisione ufficiale e toponimo più vicino |
| Doppioni e riga principale | `doppioni.py`, `riga_principale.py` | gruppi di doppioni; colonna `riga_principale_proposta` (DEC-025, proposta) |
| Rintracciabilità | `rintracciabilita.py` | colonna `rintracciabile_alla_fonte` |
| Censimento pagine Facebook | `assoc_merge.py`, `assoc_sites.py`, `assoc_geo.py`, `assoc_events.py`, `assoc_posts.py`, `assoc_build.py` | dataset Apify (pagine, eventi, post) + siti + geocodifica → `associazioni_fonti.xlsx` |
| Scoperta organizzatori su Facebook | `nuovi_organizzatori.py` | dataset Apify per parole chiave → `facebook_scoperta_organizzatori.xlsx` |
| Ricerca puntuale eventi senza fonte | `ricerca_verifica.py`, `ricerca_luoghi.py` | risultati Google + siti dei luoghi → `eventi_senza_fonte_ricerca.xlsx`, `link_fonte_diretta` |
| Fonti mirate per le pagine deboli | `mirate_liste.py`, `csa_parse.py`, `bib_parse.py`, `mirate_build.py` | risultati Google per pagina e tipo + elenchi (MIUR, mercati, centri anziani, biblioteche) → `fonti_mirate_pagine_deboli.xlsx`, `registro_fonti_v2_pagine_deboli.xlsx` |
| Apify | `apify_dl.py`, `poll_any.sh`, `poll_runs.sh` | scarico paginato dei dataset, attesa dei run; il token sta in un file fuori dal repository |

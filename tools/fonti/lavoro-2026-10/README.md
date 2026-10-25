# Script di lavoro del blocco eventi, ottobre 2026 (non prodotti)

Copia di sicurezza degli script con cui sono stati costruiti, fra il 20 e il 25 ottobre
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
| Apify | `apify_dl.py`, `poll_any.sh`, `poll_runs.sh`, `budget.sh` | scarico paginato dei dataset, attesa dei run, controllo del tetto di spesa mensile prima di ogni run; il token sta in un file fuori dal repository |
| Censimento RUNTS (6.247 enti) | `runts_prep.py`, `runts_match.py`, `runts_cf_cands.py`, `runts_fbsite_cands.py`, `runts_verify_sites.py`, `runts_fb_list.py`, `runts_merge.py`, `runts_geo.py`, `runts_emails.py`, `runts_build.py` | elenco RUNTS + risultati Google + siti + pagine Facebook → `enti_terzo_settore_fonti.xlsx` (email solo lì, mai qui) |
| Simulazione «un evento per ente» | `runts_simula.py` | censimenti + eventi noti → `simulazione_eventi_quartieri.xlsx` |
| Ricerca «evento + quartiere» | `quartieri_analizza.py`, `quartieri_filtro.py`, `quartieri_leggi_fonti.py`, `quartieri_report.py` | 288 ricerche Google → fonti classificate, siti letti → `fonti_ricerca_quartieri.xlsx`, registro v4 |
| Eventi dai post Facebook | `post_lista_giro2.py`, `post_estrai.py`, `post_build.py` | pagine salvate mai lette (secondo giro); ultimi 15 post per pagina (dataset Apify) → annunci con data futura → `eventi_dai_post_facebook.xlsx` |
| Pagina «Eventi dei quartieri» | `pagina_collect.py`, `pagina_template.html` | tutte le fonti → `eventi.json` → pagina HTML privata (il segnaposto `__DATA__` riceve i dati); geografia delle zone urbanistiche, come gli abitanti (decisione dell'owner del 25 ottobre 2026), le suddivisioni toponomastiche con `GEO=sudd` |
| Eventi e abitanti per pagina | `popolazione_assegna.py`, `popolazione_punto_pagina.py`, `popolazione_confronto.py` | griglia statistica di Roma Capitale (celle di 1 km) e zone urbanistiche ufficiali dal geoportale → abitanti per pagina QN; eventi con la stessa geografia (`pagina_collect.py`, che scrive anche `eventi_zu.json`) → `eventi_per_abitanti.xlsx` |
| Lista supplementare per le pagine deboli | `suppl_osm.overpass`, `suppl_osm_build.py`, `suppl_maps_build.py`, `suppl_albo_build.py`, `suppl_google_build.py`, `suppl_parr_get.py`, `suppl_noti.py`, `suppl_unisci.py`, `suppl_siti_check.py`, `suppl_eventi_suppl.py`, `suppl_foglio.py`, `suppl_registro_v5.py` | OpenStreetMap, Google Maps, albo della cittadinanza attiva e albi municipali, ricerca Google per toponimo, annuario diocesano → soggetti nelle 41 pagine deboli, doppioni uniti, già noti segnati → siti e post Facebook letti → `lista_supplementare_quartieri_deboli.xlsx`, `registro_fonti_v5.xlsx`, eventi nella pagina (blocco 9 di `pagina_collect.py`) |
| Promotori degli eventi, ricerche integrative, immagini e diffusione | `promotori/` (stessi nomi dell'area di lavoro, perché gli script si importano a vicenda): `base.py`, `arricchisci.py`, `siti.py`, `classifica.py`, `diritti.py`, `finale.py`, `idee.py`, `diffusione_riepilogo.py`, `foglio.py`, `rapporto.py`, `biblioteche.py`, `immagini.py`, `manifest.py` | eventi della pagina → promotori (host dell'evento Facebook, pagina che annuncia nel post, «a cura di», sede della biblioteca) → profili Facebook, RUNTS, censimenti, siti letti (contatti, note legali, robots.txt, riserva TDM), canali da Google → categorie, descrizioni, posizione sulla diffusione → `promotori_eventi.xlsx` e `promotori.json` per la wiki; agenda delle Biblioteche di Roma (blocco 10 di `pagina_collect.py`) ed eventi delle pagine Facebook mai lette (blocco 11); immagini degli eventi a risoluzione da card con manifest (DEC-101) → `immagini_eventi.zip`, `immagini_eventi_manifest.xlsx` |

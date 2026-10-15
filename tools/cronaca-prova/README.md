# Prova Cronaca: fatti ufficiali e testate in un mese

Strumenti della prova del 10 ottobre 2026 su giugno 2026. Perché è fatta così, che cosa ha
misurato e quali problemi apre: `docs/sources/CRONACA_PROCESSO_2026-10.md`. Il ruolo
della stampa nella Cronaca è una decisione aperta (DEC-108): questi strumenti misurano,
non costruiscono una pipeline.

Libreria standard di Python 3.10+ (più `openpyxl` per il solo `foglio.py`). Tutto si
scrive in una cartella di lavoro `DIR` fuori dal repository: titoli e link delle testate
sono dati delle fonti e vanno su Drive (DEC-102, DEC-104). Qui si versionano solo i
conteggi (`runs/`).

| Passo | Comando | Che cosa fa | Limiti voluti |
|---|---|---|---|
| 1 Censimento | `censimento.py DIR` | tutti i titoli del mese (`QN_MESE`, di default 2026-06) delle sei testate che non escludono gli agenti AI | solo canali ammessi dal robots.txt (sitemap, API WordPress dove non esclusa); solo metadati; una richiesta al secondo, user agent dichiarato |
| 2 Filtro | `filtro.py DIR` | candidati alla cronaca romana, per sezione o parola chiave | largo apposta: decide la lettura del passo 4 |
| 3 Lotti | `prepara_lotti.py DIR SCHEDE.jsonl…` | lotti della passata in avanti (fatti ufficiali) e inversa (titoli per decade, con i comunicati vicini) | le schede ufficiali sono quelle della tabella di giugno, su Drive |
| 4 Lettura | un agente per lotto, con `ISTRUZIONI_AVANTI.md` o `ISTRUZIONI_INVERSO.md` | avanti: quali testate hanno ripreso ogni fatto ufficiale (ricerca web, solo titoli e URL); inversa: fatti di cronaca romana sulle testate aperte e confronto con i fatti ufficiali | nessun articolo aperto; la ricerca web ha un tetto per turno e non vede tre testate |
| 5 Conti | `compila.py DIR MATRICE.csv` | `riepilogo.json` (conteggi, scenari sulle pagine) e righe per fatto per Drive | una riga senza ricerche proprie non conta come cercata |
| 6 Foglio | `foglio.py DIR` | `cronaca_testate.xlsx` da caricare su Drive | — |
| 7 Verifica (facoltativa) | un agente per lotto, con `ISTRUZIONI_TESTATA_UNICA.md` | per un campione delle notizie viste su una sola testata aperta, se sono uscite anche altrove | come il passo 4 |

### Il mese con la regola delle due fonti (DEC-108, MVP)

| Passo | Comando | Che cosa fa | Limiti voluti |
|---|---|---|---|
| 8 Fonti ufficiali | `fonti_ufficiali.py DIR [AAAA-MM] [C1…C6]` | elenchi del mese di Questura, Carabinieri, Procura, Vigili del Fuoco, Polizia Locale, Guardia di Finanza; scarica ogni comunicato e controlla che sia il comunicato | una richiesta ogni 4 s alla Questura e ogni 2 s agli altri; riconosce le pagine di blocco servite con 200; si ferma dopo cinque rifiuti di fila; nessun cambio di indirizzo |
| 9 Testate chiuse | `gdelt_titoli.py DIR` poi `chiuse_filtro.py DIR GAZETTEER` | titolo, link e ora dai file grezzi di GDELT (indice aperto; ora in UTC, data nel giorno di Roma), poi i candidati alla cronaca romana | nessuna pagina delle testate aperta |
| 10 Testi aperte | `testi_aperti.py DIR ELENCO` e lettura con `ISTRUZIONI_LUOGHI.md` | testo degli articoli delle testate aperte per le notizie che il titolo non localizza | solo testate senza esclusione degli agenti AI, canali ammessi dal robots.txt |
| 11 Abbinamento | `prepara_chiuse.py`, un agente per lotto con `ISTRUZIONI_CHIUSE.md`, poi `ISTRUZIONI_FUSIONI.md` | ogni titolo chiuso abbinato a un fatto noto o a un fatto nuovo; doppioni fra lotti fusi | solo titoli |
| 12 Tabella | `tabella_quartieri.py DIR MATRICE UFFICIALI… -- APERTE…` (mese da `QN_MESE`) e `foglio_quartieri.py DIR [MESE]` | fonti contate per editore; notizie pubblicabili per quartiere; foglio con i quartieri in colonna | le testate dello stesso gruppo valgono una |

`MATRICE.csv` è `tools/geo-assign/runs/2026-10-09/matrice_giugno_conteggi.csv`.

Test: `python3 tools/cronaca-prova/test_cronaca_prova.py` (nessuna rete).

`runs/2026-10-10/riepilogo.json` è il risultato della prova su giugno 2026: 177 fatti
ufficiali, 131 cercati sulle testate; 5.030 titoli censiti sulle testate aperte, 272
fatti di cronaca romana.

`runs/2026-10-11/` è giugno 2026 con la regola delle due fonti: raccolta ufficiale (109 su 109,
nessun blocco), copertura di GDELT, abbinamento dei titoli chiusi, tabella per pagina
(`per_pagina.csv`) e riepilogo (352 fatti pubblicabili, 64 pagine coperte su 89). Solo
conteggi: il foglio con i fatti e i link è su Drive.

`runs/2026-09/` è settembre 2026, raccolta soltanto (passi 1–2 e 8–9, 13 ottobre): comunicati
ufficiali per fonte, file GDELT letti e copertura delle testate aperte, titoli candidati delle
testate chiuse, censimento e candidati delle testate aperte. La lettura dei titoli e la tabella
per quartiere (passi 10–12) non sono state fatte perché mancava il pacchetto «Metodo QN»
(`QN_PKG`): `CRONACA_PROCESSO_2026-10.md` §4.7. Titoli e link su Drive, `Fonti 2026-09`.

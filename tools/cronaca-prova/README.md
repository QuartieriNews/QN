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

`MATRICE.csv` è `tools/geo-assign/runs/2026-10-09/matrice_giugno_conteggi.csv`.

Test: `python3 tools/cronaca-prova/test_cronaca_prova.py` (nessuna rete).

`runs/2026-10-10/riepilogo.json` è il risultato della prova su giugno 2026: 177 fatti
ufficiali, 131 cercati sulle testate; 5.030 titoli censiti sulle testate aperte, 272
fatti di cronaca romana.

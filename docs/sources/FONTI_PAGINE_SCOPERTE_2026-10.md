# Fonti locali per le pagine senza cronaca — studio del 13 ottobre 2026

| Campo | Valore |
|---|---|
| Stato | bozza del builder, non rivista (Codex non risponde, `CONSEGNA_2026-10-13.md` §2) |
| Perimetro | le 25 pagine QN che a giugno 2026 restano senza cronaca anche con la regola delle due fonti (`CONSEGNA_2026-10-13.md` §5.4; `tools/cronaca-prova/runs/2026-10-11/per_pagina.csv`), più i Municipi che le contengono |
| Domanda | esistono fonti di altro tipo — comitati, associazioni, parrocchie, blog e periodici di zona, notiziari di Municipio — che pubblichino su quei quartieri, e che cosa può farne un agente AI? |
| Finestra di attività | 1 luglio – 30 settembre 2026 |
| Strumenti | `tools/fonti-locali/` (README, `verifica_accesso.py`, `tabella.py`); esiti in `tools/fonti-locali/runs/2026-10-13/` |
| Dati nel repository | nomi di enti e di siti, URL, date, conteggi. Nessun titolo, nessun nome di persona (DEC-102, DEC-105) |
| Serve a | DEC-006 (ripiego per le pagine sottili), candidate per `SOURCE_REGISTRY.md`, il punto 3 dei passi proposti in `CONSEGNA_2026-10-13.md` §8 |
| Marche | **M** misurato (API WordPress, conteggio completo nella finestra) · **S** stimato (feed o sitemap: limite inferiore) · **—** non misurabile |

## 0 In breve

<!-- IN_BREVE -->

## 1 Perché

Con la regola delle due fonti (DEC-108) giugno 2026 copre 64 pagine su 89. Le 25 scoperte
sono quartieri di cui, in quel mese, non scrive nessuna delle fonti del registro: né i
comunicati ufficiali, né le sei testate aperte, né le testate chiuse viste da GDELT. Prima
di decidere il ripiego (DEC-006) conviene sapere se esistono fonti di altro tipo — quelle
che `CRONACA_PROCESSO_2026-10.md` §5.3 chiama «fonti ufficiali aggiuntive» e che qui si
allargano al tessuto associativo — e che cosa un agente può farne lecitamente.

Il criterio di lettura è lo stesso del resto del progetto: una fonte vale se è **aperta**
(il robots.txt non la chiude agli agenti e non c'è riserva TDM), **viva** (pubblica nella
finestra) e **locale** (parla dei quartieri della pagina). Una fonte social vale per la
raccolta manuale dell'owner (DEC-102), non per la pipeline.

## 2 Metodo

Quattro passi, con agenti dove serve giudizio e con uno strumento dove serve ripetibilità.

1. **Scoperta**, un agente per pagina e uno per Municipio, in parallelo. Ricerca web in
   modalità estesa, al massimo cinque ricerche per voce, con query diverse (quartiere +
   «comitato di quartiere» / «associazione» / «parrocchia» / «notizie»; Municipio +
   «notizie»); al massimo otto letture di home o pagine di elenco, mai di articoli. Le
   testate che escludono gli agenti AI e le fonti già nel registro non si propongono.
   Ogni candidata esce con tipo, canale, blocchi QN che potrebbe alimentare, territorio
   (quartiere · pagina · municipio · zona · città), evidenza di attività e ultima data vista.
2. **Verifica**, con `verifica_accesso.py` su ogni sito (non sui social): robots.txt per
   nome e per tutti, riserva TDM (`tdm-reservation`, `Content-Signal`, `noai`,
   `tdmrep.json`), piattaforma, feed, attività nella finestra. Il conteggio è **M** quando
   l'API WordPress risponde (il robots.txt lo ammette), altrimenti **S** da feed o sitemap.
   L'agente verificatore legge poi una sola pagina di elenco per stimare quale quota delle
   voci riguarda i quartieri della pagina e assegna il verdetto: `usabile`, `solo_metadati`,
   `inattiva`, `fuori_territorio`, `canale_chiuso`, `non_raggiungibile`, `da_verificare`
   (regole nel README).
3. **Scettico**, un agente per voce, che tenta di confutare ogni fonte `usabile` o
   `solo_metadati` su tre punti — attiva nella finestra, copre la pagina, accesso davvero
   quello dichiarato — con una sola lettura per fonte. In dubbio, `da_verificare`: meglio
   un dubbio scritto di un'approvazione tacita.
4. **Tabella**, con `tabella.py`: conteggi per pagina e per verdetto, fonti distinte, fonti
   che tornano su più pagine.

Tutto con user agent dichiarato, una richiesta al secondo per host, nessun aggiramento di
robots.txt, paywall o riserve TDM (`CRONACA_PROCESSO_2026-10.md` §5.1).

## 3 Risultati per pagina

<!-- PER_PAGINA -->

## 4 Risultati per Municipio

<!-- PER_MUNICIPIO -->

## 5 Le fonti

<!-- FONTI -->

## 6 Che cosa dice per DEC-006 e per il registro

<!-- LETTURA -->

## 7 Limiti e secondo passaggio

<!-- LIMITI -->

## 8 Candidate per il registro fonti

<!-- REGISTRO -->

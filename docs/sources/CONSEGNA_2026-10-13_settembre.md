# Consegna alla prossima sessione — settembre 2026 (13 ottobre, pomeriggio)

Nota di una sessione sola, 16:30–17:50 Europe/Rome, in parallelo a un'altra che lavorava sulle
fonti per le 25 pagine scoperte (`docs/sources/FONTI_PAGINE_SCOPERTE*`, `tools/fonti-locali/`, non
toccati qui). Vale insieme a `docs/sources/CONSEGNA_2026-10-13.md`, che resta la consegna generale:
regole, decisioni e stato del progetto non si ripetono.

## 0 Come ripartire

1. Leggere `CONSEGNA_2026-10-13.md` §0–§1, poi `CRONACA_PROCESSO_2026-10.md` §4.6–4.7 e
   `tools/cronaca-prova/README.md`.
2. Branch `claude/ecstatic-shannon-mjzxvq`, PR #15 non toccata. Commit di questa sessione:
   `504e6e7` (mese da `QN_MESE`), `d5e9cc0` (README), `70aa0e2` (conteggi e §4.7), `f8aa7bb`
   (questa nota), `b48478e` (pagina «temporaneamente non disponibile», Carabinieri rilanciati) e
   il commit che aggiorna questa riga.
3. I dati di settembre sono su Drive, `QN Hub / 20 Packages / Fonti 2026-09`
   (id `1Dk7PcPk27t4V0dqytpM9_H4gbdXvP5B1`), con un `README_Fonti_2026-09.md` che elenca i file.
4. Per finire la misura serve il pacchetto «Metodo QN» (`QN_PKG`): l'owner lo carica nella nuova
   chat o su Drive (§3).

## 1 Compito ricevuto e che cosa è stato fatto

**Compito.** Ripetere su settembre 2026 la misura della cronaca con la regola delle due fonti
(DEC-108, MVP): passi 8→12 del README di `tools/cronaca-prova`, `QN_MESE=2026-09`, finestra
1–30 settembre. Con la clausola: se il pacchetto «Metodo QN» non è su Drive, fermarsi ai passi
1–3 e ai conteggi per fonte.

**Fatto (passi 1–3 del compito).**

| Passo | Strumento | Esito |
|---|---|---|
| 1 Fonti ufficiali | `fonti_ufficiali.py DIR 2026-09` | 111 comunicati (Questura 81, Carabinieri 19, Vigili del Fuoco 6, Guardia di Finanza 5), 0 rifiuti, 0 errori; i Carabinieri rilanciati dopo una pagina «temporaneamente non disponibile» |
| 2 Testate chiuse | `gdelt_titoli.py DIR 2026-08-29 2026-10-03` + `chiuse_filtro.py` | 3.456 file GDELT, 0 mancanti; 2.009 titoli candidati (1.704 di settembre) |
| 3 Testate aperte | `QN_MESE=2026-09 censimento.py DIR` + `filtro.py DIR` | 5.101 titoli, 745 candidati alla cronaca romana |

**Non fatto (passi 4–5), e perché.** Il pacchetto «Metodo QN» non è su Drive: la ricerca per
titolo («Metodo») sull'intero Drive dell'owner non trova nulla e la cartella `Fonti 2026-06` non lo
contiene; non è nemmeno negli upload dell'ambiente. Senza `QN_PKG` lo strumento cartografico
`qngeo.py` non assegna la pagina QN, quindi: niente schede ufficiali di settembre con le pagine,
niente lettura dei titoli aperti e chiusi (ISTRUZIONI_INVERSO, _CHIUSE, _FUSIONI, _LUOGHI), niente
`tabella_quartieri.py` e `foglio_quartieri.py`. La clausola del compito prevedeva esattamente questo
caso.

**Nel repository.**
- `tools/cronaca-prova/runs/2026-09/`: `raccolta_ufficiale.json`, `gdelt.json`, `chiuse.json`,
  `censimento.json`. Solo conteggi, nessun titolo, link o nome.
- `CRONACA_PROCESSO_2026-10.md` §4.7: la raccolta di settembre e il confronto con giugno per quanto
  si può dire senza la lettura (fatti pubblicabili e pagine coperte/scoperte restano «non misurato»).
- `tabella_quartieri.py` legge il mese da `QN_MESE` (prima era fisso a giugno), con test; README
  passo 12 aggiornato.
- `fonti_ufficiali.py` riconosce la pagina «Il sistema è temporaneamente non disponibile» servita
  con 200 (Carabinieri) come rifiuto temporaneo, con test: prima troncava l'elenco in silenzio
  (§4.7, «errore trovato e corretto»).

**Su Drive (`Fonti 2026-09`) e in chat.** Dal connettore della sessione sono stati caricati il
`README_Fonti_2026-09.md` e `ufficiali_rapporto.json`. Tutto il resto (inventario e testi dei
comunicati, censimento delle sei testate aperte e candidati, candidati delle testate chiuse, registro
GDELT, log) è nell'archivio `fonti_2026-09_dati.zip` (0,8 MB), mandato in chat il 13 ottobre perché
troppo grande per il connettore: **l'owner lo carica nella cartella**. I titoli grezzi di GDELT
(25 MB, 72.807 righe) non sono nell'archivio: si rigenerano in circa 30 minuti.

## 2 Numeri chiave di settembre, accanto a giugno

| Misura | Giugno | Settembre |
|---|---|---|
| comunicati ufficiali (Questura, Carabinieri, VVF, Polizia Locale) | 109 | 111 (Questura 81, Carabinieri 19, Vigili del Fuoco 6, Guardia di Finanza 5) |
| titoli delle sei testate aperte | 5.030 | 5.101 |
| candidati cronaca sulle aperte dopo il filtro | 659 | 745 |
| titoli chiusi candidati (GDELT + filtro) | 2.023 | 2.009 |
| file GDELT letti / mancanti | 3.456 / 0 | 3.456 / 0 |
| fatti pubblicabili | 352 | non misurato |
| pagine coperte | 64 / 89 | non misurato |

le fonti ufficiali danno 111 comunicati contro 109 (Questura 81 contro 79, Carabinieri 19 contro 20, Vigili del Fuoco 6 contro 8, Guardia di Finanza 5 contro 0); le testate aperte producono lo stesso volume (5.101 titoli contro 5.030) con più candidati al filtro (745 contro 659, per la crescita di Il Faro Online e Roma Daily News); le testate chiuse danno lo stesso ordine di grandezza (2.009 candidati contro 2.023). La materia prima di settembre non è più povera di quella di giugno; se la lettura confermasse le stesse proporzioni, i fatti pubblicabili sarebbero dell'ordine dei 350 e le pagine coperte intorno ai due terzi. È un'attesa, non una misura.

## 3 Da dove riprendere

1. **Con `QN_PKG` disponibile**, nell'ordine di giugno:
   - schede ufficiali di settembre: lettura dei 111 comunicati (testi su Drive) con il
     protocollo di `tools/geo-assign/PROTOCOLLO_REVISIONE.md` e `qngeo.py`, nel formato delle
     `schede_lotto_*.jsonl` di giugno (id `CR-C1_001-1`…, `fatto`, `esito`, `livello_portata`,
     `pagine`, `luoghi_testo`, `fuori_roma`);
   - `prepara_lotti.py DIR SCHEDE…` e lettura inversa dei 745 candidati aperti
     (ISTRUZIONI_INVERSO, tre decadi);
   - `testi_aperti.py` + ISTRUZIONI_LUOGHI per i fatti che il titolo non localizza;
   - `prepara_chiuse.py DIR QN_PKG SCHEDE… -- FATTI…` e lettura dei 2.009 titoli chiusi
     (ISTRUZIONI_CHIUSE, finestre di tre giorni, 12 lotti stimati), poi
     ISTRUZIONI_FUSIONI;
   - `QN_MESE=2026-09 tabella_quartieri.py DIR MATRICE SCHEDE… -- FATTI…` e
     `foglio_quartieri.py DIR "settembre 2026"`; la matrice è quella di giugno
     (`tools/geo-assign/runs/2026-10-09/matrice_giugno_conteggi.csv`, le pagine sono le stesse).
   - Stima: la lettura di giugno ha richiesto circa una giornata con gli assistenti in parallelo.
2. **Senza `QN_PKG`** si può comunque classificare i titoli (cronaca a Roma, fuori, non cronaca) e
   contare i fatti unici per numero di editori, senza pagine: dà i «fatti pubblicabili» ma non le
   «pagine coperte». Non è stato fatto perché il compito chiedeva di fermarsi.
3. Caricare su Drive, in `Fonti 2026-09`, l'archivio `fonti_2026-09_dati.zip` mandato in chat; e il
   pacchetto «Metodo QN», così la clausola non si ripete.

## 4 Regole seguite

- Rete: user agent `QuartieriNews-ricerca/0.1`, una richiesta al secondo (una ogni 4 alla Questura),
  solo canali ammessi dal robots.txt; testate chiuse solo come titolo, link e ora dall'indice GDELT.
- Test prima di ogni commit: `test_guards.py` (ALL PASS, 37), `test_parse_duration.js` (ALL PASS),
  `test_cronaca_prova.py` (ALL PASS). Nessuna PR aperta.
- Nel repository nessun dato per item, quindi nessun testo, titolo, link o nome preso dalle fonti; i nomi delle persone nei dati su Drive seguono DEC-105.

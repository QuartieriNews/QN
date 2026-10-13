# Consegna — fonti locali per le pagine senza cronaca (13 ottobre 2026, pomeriggio)

Sessione parallela a quella della cronaca di settembre. Branch
`claude/focused-galileo-4hm3iw`, che parte dalla testa della PR #15
(`claude/ecstatic-shannon-mjzxvq`, commit `ece63ef`) e aggiunge solo file nuovi: nessun
conflitto previsto con il lavoro sulla cronaca.

## Che cosa c'è

| Cosa | Dove |
|---|---|
| Il rapporto: metodo, risultati per pagina e per Municipio, le fonti con i verdetti, la lettura per DEC-006 e per il registro, le candidate | `docs/sources/FONTI_PAGINE_SCOPERTE_2026-10.md` |
| Lo strumento di verifica (robots.txt, TDM, feed/API, attività nella finestra) e le tabelle | `tools/fonti-locali/` (README, `verifica_accesso.py`, `tabella.py`, test: 32 controlli, nessuna rete) |
| Gli esiti: candidate, verdetti, motivi, note di scoperta per voce; esito dello strumento per voce | `tools/fonti-locali/runs/2026-10-13/fonti_pagine.json`, `verifica_<slug>.json`, `riepilogo.json` |
| La decisione aperta: comitati e parrocchie come fonte primaria o come testata nella regola delle due fonti | `decisions/DEC-109-fonti-associative-nella-cronaca.md` (OPEN) |

Perimetro studiato: le 25 pagine senza cronaca a giugno, i Municipi che le contengono (§4
del rapporto dice quanti sono arrivati in tempo), e 15 pagine coperte a giugno con uno o
due fatti (Balduina, Cesano, Colle Prenestino, Corviale, Marconi, Ponte Galeria,
Portuense, Rebibbia, San Basilio, Settecamini, Torrevecchia, Boccea, Bravetta, Colli
Portuensi, Lunghezza). **Le altre 49 pagine non sono state studiate.**

## Come è stato fatto

Dieci workflow in parallelo, tre agenti per voce (scoperta con ricerca web estesa,
verifica con lo strumento più una lettura della pagina di elenco, scettico che tenta di
confutare), più lo scettico ha corretto verdetti sbagliati (es. il comitato di Settebagni
proposto per Marcigliana). Regole rispettate: user agent dichiarato, una richiesta al
secondo, nessun aggiramento di robots.txt, paywall o riserve TDM; social solo come
indirizzo; nessun titolo e nessun nome di persona nel repository. Dettagli nel rapporto §2
e §7.

Due difetti dello strumento trovati dagli agenti e corretti durante lo studio (link
all'API senza schema; redirect della home verso un social letto come sito aperto): gli
esiti già scritti sono stati riletti a mano dagli agenti, le note lo dicono voce per voce.

## Che cosa aspetta l'owner

1. Leggere §0 e §6 del rapporto; decidere se adottare le testate di Municipio di §8.1 nel
   censimento della cronaca (`tools/cronaca-prova/censimento.py`): è il passo con la resa
   più alta.
2. DEC-109: fonte primaria, testata, o primaria solo per gli Eventi (raccomandazione C).
3. I blog personali con il nome dell'autore nel dominio (rapporto §7): tenerli nel
   registro come editori, o no.
4. I 52 canali social di §5.3: sono il canale reale dei comitati; valgono solo per la
   raccolta manuale (DEC-102).
5. Le 83 fonti «da verificare» delle 25 pagine: residuo di un passaggio automatico, con le
   ricerche consigliate voce per voce in `fonti_pagine.json` → `note_scoperta`.

## Prossimi passi proposti dal builder

1. **Le altre 49 pagine**, stesso strumento e stesso workflow (`tools/fonti-locali/README.md`
   descrive i passi; gli argomenti sono le voci di `gazetteer.json → publication_zones`
   con `is_page`). Mezz'ora per gruppo di cinque pagine con due agenti alla volta.
2. **Conteggio per sezione** in `verifica_accesso.py`: oggi l'API WordPress è interrogata
   alla radice, quindi il conteggio M è dell'intero sito; il filtro per categoria o il
   feed di sezione darebbe il numero che serve alle testate di Municipio.
3. **Ripetere la verifica su settembre** (`--da 2026-09-01 --a 2026-10-01`) sulle fonti
   usabili, per la stessa finestra della cronaca di settembre.
4. **Riaprire** le inattive con API leggibile (comitati e parrocchie in pausa estiva) alla
   finestra successiva, invece di cancellarle.

## Numeri chiave

I numeri definitivi sono in §0 del rapporto e in `runs/2026-10-13/riepilogo.json`; qui
quelli stabili delle 25 pagine scoperte: 21 con almeno una fonte aperta, viva e locale;
4 senza nulla (La Giustiniana, La Rustica, Marcigliana, Pisana); 270 candidate, 43 fonti
usabili distinte, 52 canali social, 83 da verificare, 14 verdetti corretti dallo scettico,
114 ricerche web.

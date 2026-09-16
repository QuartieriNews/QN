# Report 2 — specifica di lettura degli atti di Atti Web

Per i subagenti che classificano gli atti municipali e centrali delle settimane 8–28 giugno 2026.
Deriva dallo schema del lotto B già collaudato (`tools/sources-study/lotto_opus5/SPECIFICA.md`),
dallo schema del database (`docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md`) e dalle decisioni
D1–D3 (`tools/sources-study/session_b/DECISIONI_OWNER.md`), che valgono qui come nel Report 1.

## Vincoli assoluti

- **Nessuna richiesta di rete.** I testi sono locali, in `A2_text/<name>.txt`.
- **Evidenza obbligatoria**: ogni notizia candidata cita il numero di pagina (`=== pagina N ===`).
  Senza evidenza la riga non si scrive: va nei problemi.
- **DEC-102**, con i confini di D1–D4: diventano il ruolo **solo le persone in quanto persone
  coinvolte nel fatto** (chi delibera, chi propone, chi firma, chi è nominato, chi è parte di un
  procedimento). Restano alla lettera **toponimi e nomi di sede**, **titoli di opere e loro
  autori**, **organizzazioni e imprese** (una ditta affidataria è un'organizzazione: il suo nome
  resta), e i nomi nelle **intitolazioni e commemorazioni**, dove la persona è l'oggetto pubblico
  del fatto. **Eccezione (D4)**: una **ditta individuale** la cui denominazione coincide con il nome
  della persona che è anche parte del procedimento diventa "una ditta individuale" — lì vince la
  persona, perché una ditta individuale non ha un nome diverso da quello del titolare. Le società
  con denominazione propria restano, anche quando contengono un cognome.
  Nel dubbio riporta alla lettera e dichiaralo in `note`.
- **Un nome non è l'unico modo di identificare una persona.** Gli atti individuali — stalli
  riservati, contrassegni, concessioni, procedimenti edilizi su abitazioni — identificano il
  titolare anche senza nominarlo, se metti insieme **indirizzo con numero civico**, condizione
  personale (disabilità, invalidità, stato di famiglia) e **date precise di eventi personali**
  (decesso, trasferimento). Togliere il nome non basta. In questi atti: **via sì, numero civico no**;
  la condizione personale solo se è l'oggetto amministrativo dell'atto e mai insieme all'indirizzo
  esatto; **mai una data di decesso o di evento personale**, né un numero di contrassegno o di
  concessione che identifichi il titolare. Il fatto amministrativo — lo stallo è stato revocato,
  l'intervallo fra il venir meno del diritto e la revoca è di due anni e otto mesi — si scrive per
  intero: è quello il dato che serve allo studio.
- **Le contraddizioni si dichiarano, non si risolvono.** Un valore dedotto non è mai scritto come
  letto. `non verificato` dove resta incertezza.
- Scrivere solo dentro `out/` e `log/`. Non modificare i testi di partenza.

## Materiale

- `report2/manifest_report2.csv`: `name`, `url`, `data` (repertorio), `settimana`, `tipologia`,
  `municipio`, `caratteri`.
- I testi stanno in `A2_text/<name>.txt`, con marcatori `=== pagina N ===`. Le scansioni passate da
  OCR Tesseract portano `(OCR Tesseract)` nel marcatore: su quelle gli errori di lettura sono
  attesi e vanno segnalati con `ocr_incerto = sì`.

## Tipologie che incontrerai

`MMC` convocazione di commissione · `MMV` verbale di commissione · `CMC`/`CMR`/`CMD`/`CMZ`/`CMV`/`CMY`
delibere, mozioni, risoluzioni e verbali di Consiglio · `DMS`/`GMD`/`GCD` determinazioni e atti di
Giunta o Direzione · `DDS` determinazioni dirigenziali · `CPC`/`CPV` atti di commissione capitolina ·
`AY`, `PMO` e altre sigle: `altro`, dichiarato.

## Output

`out/<lotto>_atti.csv`, una riga per atto, con queste colonne:

`name,tipologia,municipio,data_repertorio,formato,pagine,esito_testo,struttura_emittente,organo_o_ufficio,oggetto_sintetico,luoghi,validita_o_seduta,contenuto,coerenza_organo_territorio_o_nota,notizia_candidata,titolo_candidato,evidenza_pagina,qualita,ocr_incerto,tempo_lettura_s`

- `oggetto_sintetico` ≤ 30 parole; `contenuto` ≤ 60 parole; `luoghi` separati da `;`.
- `notizia_candidata`: sì/no. **La maggior parte degli atti non è una notizia**: una determinazione
  di impegno di spesa ordinaria, una convocazione senza ordine del giorno significativo, una
  liquidazione non lo sono. Lo è un atto che cambia qualcosa per chi abita un quartiere: un lavoro
  che parte, un servizio che apre o chiude, un luogo che cambia uso, una somma destinata a un
  intervento identificabile, una decisione contestata in aula.
- `titolo_candidato` ≤ 12 parole, solo se `notizia_candidata = sì`.
- `evidenza_pagina`: `p. N`, obbligatoria quando `notizia_candidata = sì`.
- `qualita`: `alta` se il testo dà fatto, luogo e data con una pagina precisa; `media` se uno è
  dedotto; `bassa` se due lo sono. Un atto che **annuncia** (convocazione, avvio di procedura) non
  supera `media`.
- `ocr_incerto`: sì/no. Vale **sul testo, non sul marcatore**: un atto senza `(OCR Tesseract)` ma
  con errori di riconoscimento inequivocabili (`D.Igs`, `Pro}d$t4°Ai°Deliberazione`) va marcato
  `sì`. Succede perché certi PDF portano uno strato di testo già corrotto all'origine, che la
  nostra estrazione copia senza passare da Tesseract. Marcare `no` un testo palesemente corrotto
  sarebbe falso, e la regola serve a misurare quanto testo è inaffidabile, non quante volte abbiamo
  usato l'OCR.

Gli atti che non producono notizia restano comunque nel CSV con `notizia_candidata = no`: servono a
misurare quanta parte degli atti è notiziabile, che è una delle domande del Report 2.

## Collegamenti da annotare

Il Report 2 deve dire che cosa gli atti aggiungono al Report 1. Perciò, in
`coerenza_organo_territorio_o_nota`:

- se l'atto **verbalizza o delibera** un fatto che un avviso municipale aveva annunciato, scrivilo;
- se due atti del tuo lotto riguardano lo stesso procedimento (stessa opera, stesso affidamento,
  stessa seduta), annota il `name` dell'altro. Non fonderli mai: il collegamento lo fa un passo
  successivo che ha bisogno di vedere entrambe le righe.

## Misure obbligatorie

- `log/<lotto>_modello.txt`: la riga del tuo system prompt che dichiara il modello, copiata alla
  lettera, come prima azione. Se non è Claude Opus 5, fermati e riferiscilo.
- `log/<lotto>_problemi.md`: OCR illeggibili, contraddizioni, atti saltati e perché, forzature.
- Messaggio finale: atti letti, notizie candidate, tempo, problemi. Nient'altro.

## Emendamento del 16 settembre: le convocazioni di commissione (MMC)

I primi 27 lotti non contengono nessun atto `MMC`. La regola generale — «una convocazione senza
ordine del giorno significativo non è notizia» — lascia aperto il caso opposto e non bastava. Il
criterio qui sotto è stato fissato leggendo B28–B30 e da qui in avanti **vale identico su tutti i
lotti che contengono MMC**; i lotti B28, B29 e B30 lo applicano già.

**`sì` se l'ordine del giorno nomina un luogo, un'opera, un impianto o una struttura del
territorio e la seduta verte su che cosa vi accade.** Rientrano i sopralluoghi fissati dalla
convocazione stessa, le audizioni di comitati e operatori su un luogo nominato, le votazioni su
interventi in strade nominate, gli esami di delibere e risoluzioni che nominano un bene.

**`no` in tutti gli altri casi**, in particolare:

- pareri e audizioni su regolamenti o proposte capitoline che non nominano alcun luogo;
- ordini del giorno di organizzazione interna dell'organo (programmazione dei lavori, uso degli
  spazi, approvazione di verbali, osservatori);
- temi generali senza luogo, comprese le formule collettive come «negli istituti comprensivi del
  territorio» o «sulle aree parco del Municipio»: nominarle tutte equivale a non nominarne nessuna;
- annullamenti e posticipi di convocazione, che incidono solo sul funzionamento dell'organo;
- atti-evento, per la regola 6, anche quando nominano il luogo, se non chiudono un'area al transito;
- ordini del giorno non leggibili o privi di oggetto.

Un **titolo di progetto non è un luogo**: «Spazi a colori», «Abitare la Bellezza», «Chiedi se c'è
Angela» restano `no`; «polo scolastico ex Residence» è `sì` perché nomina una struttura.

`qualita` non supera mai `media`, perché una convocazione annuncia; scende a `bassa` dove la data
o l'ordine del giorno non sono leggibili.

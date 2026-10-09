# Assegnazione dei contenuti ai quartieri QN: riproduzione, nuovo processo, prova cieca

8 ottobre 2026 · builder: Claude Code · materiale: pacchetto `Metodo_QN_per_Claude_Code_2026-10-08`,
preparato con Codex sul corpus congelato al 19 settembre 2026 (3.529 schede). Gli strumenti sono in
`tools/geo-assign/`; gli ID del campione e i risultati aggregati in `tools/geo-assign/runs/2026-10-08/`.
Nessun testo delle fonti è versionato qui (DEC-102).

Il lavoro ha due parti da non confondere:

1. **Riproduzione.** Ricostruisce le decisioni già prese e motivate, con gli strumenti del pacchetto.
   Dimostra che il risultato storico si ricalcola, non che sia esatto.
2. **Nuova analisi.** Costruisce un processo che parte solo da schede, gazetteer e cartografia, lo
   prova alla cieca su un campione e confronta l'esito con lo storico scheda per scheda. Come
   richiesto non ho rianalizzato tutto il corpus: ho lavorato sul processo.

## 1 Riproduzione del 19 settembre

`verify_package.py`: 69 file, nessuna impronta diversa. `replay_historical.py` ricostruisce le
3.529 schede e confronta ciascun ID (esito, pagine, motivazione) e ciascuna delle 267 celle della
matrice: **0 differenze**. I file prodotti coincidono con `risultati_reference` nel contenuto; differiscono
solo nei byte di serializzazione.

| Misura | Valore |
|---|---:|
| Schede / mantenute | 3.529 / 3.375 |
| U · M · T · D · I · F (mantenute) | 2.500 · 192 · 554 · 99 · 7 · 23 |
| ID mantenuti assegnati a pagine | 2.692 |
| Presenze scheda–pagina | 3.006 |
| Pagine attive | 89 |

| Blocco | ID distinti | Presenze |
|---|---:|---:|
| Amministrazione | 1.882 | 2.159 |
| Cronaca | 16 | 25 |
| Eventi | 794 | 822 |
| Social | ND | ND |

La matrice completa, con i quartieri in colonna e i blocchi in riga, è
`runs/2026-10-08/riproduzione/matrice_blocchi_quartieri.csv`. Le copertura per fasce e i conteggi
per fonte sono nella stessa cartella. Questa resta **la matrice di riferimento**: la nuova analisi
non ha coperto tutto il corpus e non la sostituisce.

Il replay rigioca anche 1.031 decisioni contestuali e le revisioni ereditate da `reviewed.json`.
Anche la funzione «automatica» storica (`initial()`) le incorpora, quindi nello storico non esiste una
misura di quanto il codice da solo sapesse fare.

## 2 Il nuovo processo

| Fase | Strumento | Novità rispetto allo storico |
|---|---|---|
| 1 Evidenze | `stage1.py` | Cieca per costruzione: non apre benchmark, storico, decisioni. Una menzione per luogo con campo d'origine, forza del supporto (debole se solo nella sintesi e senza civico) e identificativi GIS. Segnala luoghi non spiegati, nomi di Municipio («Municipio Roma XIII Aurelio» non è Aurelio), località dentro il nome di una strada con pagina diversa, organi e sportelli, indizi di più sedi e di tratto. Le strade omonime restano ambigue invece di essere scartate in silenzio. |
| — Cartografia | `qngeo.py` | Strada, civico, **incrocio calcolato geometricamente**, punto, località, ricerca per parole, tutto offline. Ogni risposta cita chiave stradale, zona, suddivisione e coordinate: la prova diventa ripetibile invece del generico «Geoportale». Le zone senza pagina o con più pagine si risolvono campionando i punti della strada. |
| — Raccordo | `zone_qn_cross.json` | La tabella `cross` del codice storico (45 zone urbanistiche che `urban_mapped.json` lascia senza pagina) diventa un file versionato con provenienza. |
| 2 Lettura | `PROTOCOLLO_REVISIONE.md`, `pacchetti.py` | Area di lavoro cieca, che contiene solo input, cartografia e strumenti. Decisione strutturata (§13 del manuale): fatto, ruolo di ogni luogo, risoluzione ripetibile, riscontri, portata, dubbio e verifica necessaria, confidenza. |
| — Controllo | `valida.py` | Rifiuta una pagina che non discende da un luogo effettivo usato, una T senza portata, una D senza tipo e senza verifica, una M con meno di due sedi effettive. |
| 3 Confronto | `confronta.py`, `aggregate_qn.py` | Confronto per ID, eseguito solo dopo il congelamento (impronta sha256 registrata). |
| — Campione | `campione.py` | Campione di controllo estratto prima di qualsiasi confronto: le regole della fase 1 sono state messe a punto solo sulle altre 3.230 schede. |

Casi didattici che il codice ora risolve o segnala da solo:

- **N1887:** l'incrocio Togliatti–Prenestina viene calcolato dentro la zona 7A, cioè Centocelle, senza
  bisogno di leggere il contesto.
- **N2863:** «via Aversa» nel titolo viene letta come via Raffaele Aversa della sintesi.
- **N3129:** la località dentro il nome della strada viene segnalata.
- **N2150:** una strada lunga senza tratto produce D, con le pagine messe tra le candidate.

Sono test eseguibili in `test_geo_assign.py`.

## 3 Prova cieca

**Disegno.** Il campione è di 126 schede mantenute, stratificate per fonte con seed 20261008, esclusi
i 19 casi del pacchetto. Le schede sono state divise in sei lotti da 21, ciascuno affidato a un
revisore separato (un sottoagente). Ogni revisore aveva solo il protocollo, i pacchetti di evidenze,
la cartografia, la ricerca web e comune.roma.it; nessuno ha dichiarato di aver visto esiti storici.

Io ho letto il manuale, i casi didattici e le note sui quattro casi da riesaminare, e ho messo a punto
la fase 1 confrontandola con lo storico sulle schede fuori campione. Per questo **l'arbitrato delle
differenze qui sotto non è cieco**.

I revisori hanno usato la versione di `qngeo.py` precedente alla guardia sulle forme abbreviate e al
comando `cerca`. Le decisioni sono state congelate prima del confronto: sha256
`7da2cab9…4f014233a`.

| | Coincide con lo storico (esito e insieme di pagine) |
|---|---:|
| Fase 1, solo codice | 64 / 126 (51%) |
| Fase 1 + lettura cieca | **95 / 126 (75%)** |

Confronto degli esiti, con lo storico in riga e il nuovo in colonna:

| storico \ nuovo | U | M | T | D | I |
|---|---:|---:|---:|---:|---:|
| U (95) | 79 | | 6 | 10 | |
| M (7) | 3 | 3 | 1 | | |
| T (23) | | | 20 | 2 | 1 |
| D (1) | | | | 1 | |

Dove entrambi assegnano a pagine (85 schede), le pagine coincidono in 74 casi e si sovrappongono
in 78.

- **Per fonte:** E2 17/18, E3 5/5, A2 19/22, A3 29/41, A1 10/18, A4 10/16.
- **Per blocco:** Eventi 30/33, Amministrazione 62/89.
- **Presenze nel campione:** 91 contro 115.

**La confidenza dichiarata dal revisore è informativa:**

| Confidenza | Coincide | Schede |
|---|---:|---:|
| Alta | 64 (90%) | 71 |
| Media | 31 (60%) | 52 |
| Bassa | 0 | 3 |

È il criterio naturale per decidere quali decisioni mandare a un controllo umano.

**Costo.** Circa 795.000 token di modello per 126 schede (circa 6.300 a scheda) e 5–7 minuti per
lotto. Sul corpus intero la stima è dell'ordine di 22 milioni di token. Restano esclusi l'arbitrato
e il controllo umano.

### Arbitrato delle 31 differenze

L'arbitrato è non cieco, del builder; il dettaglio per ID è in `runs/2026-10-08/arbitrato_differenze.json`.

| Esito dell'arbitrato | N. | Casi |
|---|---:|---|
| Nuova decisione preferibile: correzione proposta dello storico | 9 | N0407, N0425, N2307: atti o verifiche municipali che lo storico localizzava sull'indirizzo della seduta o del recapito. N2454: via Niccolini a Monteverde, non l'omonima all'Infernetto (confermata dall'incrocio). N1427: via Antonino Parato è in zona Trionfale, non Prati. N3290: il conteggio del testo esclude la quinta sede. N2897: un incrocio calcolato al posto di una M di confine. N2147: I invece di T. N2265: una pista concreta invece di una T di ripiego. |
| Storico preferibile: prova trovata dallo storico e non dal processo cieco | 8 | N0388, N1459, N1897, N2127, N2049: sedi di cui lo storico aveva trovato l'indirizzo. N2474, N1981, N2101: indirizzo preso da un atto della stessa vicenda. |
| Storico preferibile: errore del processo nuovo | 3 | N0026, N0843: zona urbanistica o tabella `cross` contro una località nominata dalla fonte (Quadraro, Torrevecchia). N1529: otto strade nominate trattate come T invece che M. |
| Aperto: serve una regola o una decisione sul raccordo QN | 11 | Sportelli in open day (N0070, N0311). Norma per il «centro storico» (N2749). Budget municipale con una sede nota (N2558). «Fra A e B» (N0525). Strade di confine (N0049, N3303). Porta Asinaria e Mura (N2407, N2652). Zone 11C e 11E (N2052, N0370). |

Effetto sulla matrice, limitatamente al campione:

- **Correzioni giustificate:** spostano circa 5 presenze su 115 (circa 4%) e cambiano pagina in 2 schede.
- **Perdite di richiamo:** valgono 8 presenze. Non sono errori di giudizio: indicano dove il processo
  deve recuperare le prove che lo storico aveva (§5).

Non estrapolo questi numeri a una nuova matrice: 126 schede non bastano. Mostrano però dove i
risultati si spostano.

### I quattro casi da riesaminare (analisi del builder, non cieca)

| ID | Storico | Proposta | Ragione |
|---|---|---|---|
| N3519 | U Prima Porta | M prima-porta, la-storta, cesano (Villa di Livia e Labaro, Malborghetto e Isola, Cesano); Parco di Veio in `territori_senza_pagina`; Torretta di Ponte Emilio non identificata. Se la redazione considera il programma «dei beni del territorio» di portata municipale, T. | Le mete sono effettive e plurime; il titolo non le riduce a una. Il codice storico leggeva anche «Ponte» dentro «Torretta di Ponte Emilio» come rione Ponte (ora corretto e testato). |
| N2403 | U Testaccio | M testaccio, centro-storico; candidate appio-latino e ostiense-san-paolo | Il tratto Porta San Paolo–Porta Metronio tocca le zone 1C Aventino (Testaccio), 1X e 1G Celio (Centro Storico) e lambisce 9D Appio. Il solo primo estremo non basta. |
| N2310 | M Centro Storico, Esquilino | T | È una risoluzione municipale di sostegno: striscione, patrocinio, bandiera sulla sede. Le piazze compaiono solo nel campo luoghi e sono il percorso della manifestazione, non l'oggetto dell'atto. |
| N2028 | U Nomentano | T, confidenza media | È la ricognizione municipale dei cortili scolastici; le due scuole sono il confronto che la motiva (`confronto_o_esempio`). U resta sostenibile solo se l'oggetto editoriale è il cortile della Fratelli Bandiera. |

## 4 Problemi del metodo emersi, con proposte

1. **Il raccordo zona → pagina è la prima fonte di errore residuo.** Lo è anche per luoghi ben
   identificati (N0026, N0843, N0370, N2052). Sono 45 zone su 155 senza pagina, e la tabella `cross`
   ne assegna diverse a più pagine.
   - *Proposta:* dare alle località QN che contano (Quadraro, Torrevecchia, Tor Marancia, Ottavo Colle…)
     un punto o un poligono di riferimento versionato, e usarlo prima della zona urbanistica.
   - L'ordine di precedenza è ora scritto nel protocollo.
2. **Il richiamo dipende dall'identificazione delle sedi, che dipende dalla rete.** Da questo
   ambiente il Geoportale (civici WFS) e i siti ASL, CRI e Wikipedia sono bloccati; la copia offline
   ha 257 civici.
   - *Proposta:* consentire `geoportale.comune.roma.it` nella politica di rete. È un'impostazione
     dell'ambiente cloud, la decide il proprietario.
   - *Proposta:* tenere un registro delle sedi verificate con provenienza (indirizzo, URL, data,
     omonimie), riusabile fra esecuzioni. Le 145 sedi storiche di `storico/venues.json` vanno
     ricontrollate prima di entrare in quel registro, perché alcune sono state costruite caso per caso.
3. **`vicenda_id` raggruppa spesso solo la stessa seduta.** I revisori l'hanno segnalato
   all'unanimità. Ora le schede sorelle sono ordinate per parole di luogo in comune. Lo storico ha
   ottenuto tre assegnazioni corrette proprio da atti collegati (N2474, N1981, N2101).
   - *Proposta:* collegare video e atti per numero di proposta (RC/…) e per oggetto, non per seduta.
4. **Il riconoscimento delle vie sbaglia sulle forme abbreviate e sugli omonimi.** Esempi: «via
   Nicolini», «via Bruno», «via Veneto» presa per Castelfranco Veneto, «via di Francesco» (un
   cammino), viale Venezia di Brescia.
   - Ora le forme deboli valgono solo se il nome visibilmente finisce lì, ed è disponibile `qngeo.py cerca`.
   - Restano i numeri scritti in cifre o in lettere («Largo 3 Giugno 1849») e le vie mancanti nella
     copia dello stradario (via Gianna Pederzini, Lungotevere Vittorio Gassman).
5. **Le regole mancanti producono decisioni diverse fra revisori.** Ho aggiunto al protocollo i casi
   che il manuale già decide:
   - atto con più strade nominate → M;
   - strada di confine senza tratto → D;
   - «fra A e B» → alternativa.

   Gli altri casi richiedono una decisione del proprietario (§6).
6. **I riscontri web sono deboli per costruzione.** La ricerca restituisce riassunti, non il
   passaggio della pagina: nel campo `riscontri` i revisori hanno spesso parafrasato. Un riscontro
   deve citare un passaggio letto. Con la rete attuale questo è possibile solo per comune.roma.it.
7. **Il processo nuovo è più prudente dello storico.** Ha 85 schede U/M contro 102 nel campione:
   più D dove manca la prova, più T dove la fonte è un atto municipale. È coerente con il manuale
   («non inseguire il 96,2%»), ma la copertura misurata scenderà a meno che i punti 1–3 non
   recuperino il richiamo.

Le correzioni introdotte dopo la prova riguardano la guardia sulle forme deboli, `cerca`, l'ordine
delle schede sorelle e le regole del protocollo. **Non sono ancora misurate alla cieca:** il prossimo
campione deve usare un seed diverso.

## 5 OWNER_DECISION_REQUIRED

Il builder non decide nessuno di questi punti.

1. **Sportello in apertura straordinaria** (open day della carta d'identità, iscrizioni ai centri
   estivi): è la sede di un evento di quartiere (U) o il recapito di un servizio municipale (T)? Lo
   storico ha deciso in entrambi i modi (U in N0070 e N0311, T in N0254).
2. **Norme sul «centro storico» urbanistico**, cioè la città storica e la disciplina del 2010: pagina
   Centro Storico o T?
3. **Raccordi QN da confermare o versionare:**
   - rione Monti → Esquilino-Termini, che manda Porta Asinaria, Laterano e i Mercati di Traiano fuori
     da Centro Storico e San Giovanni;
   - zona 18C → Montespaccato;
   - zona 11E → Ardeatino o Montagnola;
   - zona 8A (Municipio VI) → Cinecittà (Municipio VII);
   - piazza dei Tribuni, cioè Quadraro/Monte del Grano, → Cinecittà per zona.
4. **Rete:** consentire il Geoportale di Roma nell'ambiente, per i civici puntuali.
5. **Passo successivo:** un secondo campione cieco (circa 120 schede, seed nuovo) per misurare le
   correzioni, oppure l'esecuzione sul corpus intero (circa 22 milioni di token) con controllo umano
   delle decisioni a confidenza media e bassa.

## 6 Come rieseguire

```text
export QN_PKG=/percorso/Metodo_QN_per_Claude_Code_2026-10-08
python $QN_PKG/scripts/verify_package.py
python $QN_PKG/scripts/replay_historical.py --out risultati_reference_nuovo
python tools/geo-assign/stage1.py --out /tmp/fase1
python tools/geo-assign/pacchetti.py --evidenze /tmp/fase1/evidenze.jsonl \
    --ids-file tools/geo-assign/runs/2026-10-08/campione_test.json --lotti 6 --out /tmp/cieco
# revisione: un revisore per lotto, con PROTOCOLLO_REVISIONE.md; poi
python tools/geo-assign/valida.py decisioni.jsonl
python tools/geo-assign/confronta.py --assegnazioni decisioni.jsonl \
    --ids-file tools/geo-assign/runs/2026-10-08/campione_test.json
```

Per il corpus intero, le decisioni devono coprire tutti i 3.529 ID. Poi:

```text
python $QN_PKG/scripts/aggregate_qn.py --assignments decisioni.jsonl --out risultati_claude \
    --compare $QN_PKG/benchmark/assegnazioni_2026-09-19.jsonl
```

## 7 Dopo le risposte dell'owner (9 ottobre)

Decisioni registrate in `decisions/DEC-106` (decisa) e `decisions/DEC-107` (aperta).

- **Portata separata dal luogo (DEC-106).** Ogni decisione ha ora `livello_portata`
  (`quartiere`, `municipio`, `citta`) oltre alle pagine.
  - L'open day di uno sportello tiene la pagina dello sportello e ha livello municipale.
  - La sede di una seduta dà il livello ma non la pagina (raccomandazione del builder,
    da confermare).
  - Le norme sul centro storico urbanistico sono notizie cittadine.

  Sul corpus intero, la fase 1 propone così 53 servizi (pagina + Municipio), 85 sedute
  (solo Municipio) e 17 norme sul centro storico (città). Il validatore richiede il
  campo; le decisioni cieche dell'8 ottobre sono anteriori e si validano con
  `--senza-livello`.
- **Un errore trovato nel raccordo.** Confrontando le tre fonti zona → pagina, la
  tabella `cross` storica prevaleva sul gazetteer e aggiungeva Montagnola alla zona
  11E (Tor Marancia) e Giardino di Roma alla 13A (Malafede). La tabella dell'owner
  dice Ardeatino e Acilia. Ora il gazetteer prevale: il caso Tor Marancia si chiude
  con la tabella dell'owner, senza bisogno di una regola.
- **La coda dei dubbi (`dubbi.py`).** Prima versione sul corpus del 19 settembre:
  269 dubbi, che coinvolgono 333 schede diverse tra quelle mostrate come esempio.

  | Tipo | Dubbi | Con proposta del builder | Schede coinvolte |
  |---|---:|---:|---:|
  | ZONA | 47 | 31 | 1.927 |
  | LUOGO | 24 | 21 | 29 |
  | STRADA (≤ 1,5 km) | 91 | 83 | 199 |
  | SENZA pagina attiva | 11 | 11 | 33 |
  | TRATTO (strade lunghe) | 96 | 96 («tratto») | 497 |

  Le schede di righe diverse si sovrappongono. Il lavoro vero per l'owner è nelle zone
  senza proposta e nelle righe LUOGO e STRADA; le altre si chiudono in blocco con `ok`.
  - Cinque righe vengono dall'arbitrato della prova cieca: Monte del Grano, Parco
    Commendone, Porta Asinaria, Casale Ceribelli e il rione Monti (quest'ultimo è un
    cambio della tabella, non una regola).
  - Tre zone (7G, 8A, 10I) hanno candidate di un altro Municipio e sono segnalate.
- **Convergenza.** Ogni decisione chiude il suo dubbio; rieseguire `dubbi.py` dà il
  numero residuo. Sulla copia di prova sei decisioni simulate hanno portato la coda da
  269 a 263. Non sono applicate al file reale: le regole le scrive solo l'owner.
- **Doppia assegnazione ai confini (DEC-107, aperta).** Lo strumento la supporta
  (`slug1+slug2`, regola `doppia_confine`, presenze contate a parte), ma
  `applica_decisioni.py` la rifiuta finché la decisione non è presa.
- **Rete aperta (Full) e civici dal Geoportale.** `qngeo.py civico` interroga dal vivo
  `DIPCUL:GeoromaCiviciLocator` quando la copia offline non ha il numero, con una cache
  locale. Ogni punto conserva `ID_CIVICO`, query e data di lettura.
  - Gestisce l'apostrofo, che lo stradario e il registro dei civici scrivono in modo
    diverso, e i nomi diversi della stessa strada («piazza Campidoglio» / «piazza del
    Campidoglio»).
  - Quando il numero non esiste nel registro usa il civico più vicino sullo stesso
    lato, dichiarandolo come approssimazione.

  Sul corpus, delle 481 citazioni di un civico:

  | Esito | Citazioni |
  |---|---:|
  | Punto ufficiale, una sola pagina | 425 |
  | Punto ufficiale, due pagine (confine o fonti in disaccordo) | 18 |
  | Senza punto | 38 |

  Il guadagno su questo corpus è piccolo (31 punti in più, 29 approssimati), perché lo
  studio storico aveva già scaricato i civici che gli servivano. Il valore è per i
  contenuti nuovi. Con `QN_RETE=0` gli strumenti restano offline, per rigiocare una
  prova cieca nelle stesse condizioni.

# Assegnazione geografica QN — processo in quattro fasi

Strumenti per assegnare le schede (notizie, atti, video) alle pagine-quartiere QN
secondo il «Metodo QN» preparato con Codex l'8 ottobre 2026 (pacchetto
`Metodo_QN_per_Claude_Code_2026-10-08`, non ridistribuito qui: contiene testi delle
fonti, DEC-102). Il rapporto che spiega perché il processo è fatto così e cosa ha
misurato è `docs/sources/GEO_ASSEGNAZIONE_2026-10.md`.

Solo libreria standard di Python 3.10+. Un solo comando usa la rete: `qngeo.py
civico`, per un numero assente dalla copia offline, interroga il WFS del
Geoportale (cache in `QN_CACHE`; `QN_RETE=0` vieta la chiamata). Ogni comando
legge il pacchetto da `--pkg` o dalla variabile `QN_PKG`; nessuno scrive nel
pacchetto.

| Fase | Comando | Cosa produce | Cosa NON fa |
|---|---|---|---|
| 0 Riproduzione | `python scripts/verify_package.py` e `python scripts/replay_historical.py --out DIR` (nel pacchetto) | le 3.529 decisioni archiviate ricostruite, 0 differenze per ID e per cella | non misura l'accuratezza: rigioca decisioni già prese |
| 1 Evidenze | `stage1.py --out DIR` | `evidenze.jsonl` (menzioni con campo, forma, ruolo-indizio, risoluzione GIS e identificativi) e `proposte.jsonl` (esito proposto, motivi, priorità) | non decide; non legge benchmark né storico |
| 2 Lettura contestuale | `pacchetti.py` crea un'area di lavoro cieca e i lotti; il revisore segue `PROTOCOLLO_REVISIONE.md`, usa `qngeo.py`, scrive `decisioni.jsonl`; `valida.py` lo controlla | decisioni con fatto, ruoli dei luoghi, risoluzione ripetibile, riscontri | non vede esiti storici |
| 3 Conteggio e confronto | `aggregate_qn.py` del pacchetto (file completo) o `confronta.py` (campione) | matrice blocco × pagina, conteggi, differenze per ID | non corregge nulla per avvicinarsi ai totali |

`qngeo.py` è lo strumento cartografico offline (stradario, zone urbanistiche,
suddivisioni toponomastiche, civici salvati):

```text
qngeo.py strada "via raffaele aversa" --mun IX
qngeo.py incrocio "viale palmiro togliatti" "via prenestina"
qngeo.py civico "via cassia" 472
qngeo.py punto 41.8949 12.5747
qngeo.py localita "quarticciolo"
```

## Dubbi → decisione dell'owner → regola (DEC-106)

```text
dubbi.py --evidenze DIR/evidenze.jsonl --out /lavoro/coda_dubbi.csv --semi runs/*/semi_dubbi.json \
         --decisioni /lavoro/decisioni.jsonl             # --out fuori dal repository: contiene titoli
# l'owner compila la colonna "decisione" (Excel, separatore ;)
applica_decisioni.py --coda /lavoro/coda_dubbi.csv --prova     # controlla senza scrivere
applica_decisioni.py --coda /lavoro/coda_dubbi.csv             # scrive regole_geografiche.json
dubbi.py ...                                                   # la coda si accorcia
```

`dubbi.py` raggruppa per luogo tutti i punti in cui la geografia è incerta: zone
urbanistiche senza pagina o con fonti in disaccordo (ZONA), luogo nominato contro la
pagina della via (LUOGO), strade brevi su più pagine (STRADA), località instradate
a pagine non attive (SENZA), strade lunghe (TRATTO, di norma «dipende dal tratto»).
Valori della colonna `decisione`: uno slug; `slug1+slug2` (entrambe, solo dopo
DEC-107, con `--consenti-confine`); `tratto` (solo per una strada); `nessuna`;
`ok` (accetta la proposta); `ignora` (falso allarme); vuoto = aperto. Una riga
`C-R-0012` è una regola contestata da un revisore di fase 2 (`nota_geografia`,
letta con `--decisioni`): la decisione la sostituisce con una regola nuova e la
vecchia resta nel file come storia (`sostituita_da`), mai applicata. Lo stesso
dubbio due volte nella coda, o due dubbi sulla stessa chiave, sono errori: una
chiave ha una regola viva sola. Una riga destinata al gazetteer si chiude solo
se la decisione coincide con ciò che la tabella risolve oggi; altrimenti va in
`modifiche_gazetteer.csv`.

Ogni decisione diventa una regola numerata in `regole_geografiche.json`, che
`qngeo.py` e `stage1.py` applicano e citano (`R-0001`); `stage1.py` ne lascia
una copia accanto a `evidenze.jsonl` e `pacchetti.py` porta quella copia, non il
file corrente, nell'area cieca. Precedenza: gazetteer
(`zu_code`, tabella dell'owner) > regola dell'owner > `urban_mapped.json` >
`zone_qn_cross.json`. Una decisione che sposta una località (es. rione Monti) non
diventa regola: finisce in `modifiche_gazetteer.csv`, da applicare nella tabella e
rigenerare il gazetteer. La coda contiene titoli delle fonti: resta fuori dal
repository (DEC-102); qui si versionano solo le regole.

Civici: `qngeo.py civico` usa prima la copia offline, poi il servizio WFS del
Geoportale (`DIPCUL:GeoromaCiviciLocator`), con cache in `~/.cache/qn-geo/` (o
`QN_CACHE`). `QN_RETE=0` spegne le chiamate di rete, non la cache: la cache è
l'istantanea dei punti già letti, e con essa una prova si rigioca nelle stesse
condizioni; per un replay senza civici dal vivo si punta `QN_CACHE` a un file vuoto,
come fanno i test. La cache si scrive con lock e sostituzione atomica: più lotti in
parallelo possono condividerla.

`zone_qn_cross.json` è la tabella di raccordo zona urbanistica → pagina QN per le
45 zone che `urban_mapped.json` lascia senza pagina: è la tabella `cross` del
codice storico, resa un file versionato. Una voce con più pagine è
un'ambiguità, non un'assegnazione multipla. Fino al 9 ottobre la tabella prevaleva
anche sul gazetteer: per 11E (Tor Marancia) e 13A (Malafede) aggiungeva una seconda
pagina che la tabella dell'owner non prevede. Ora il gazetteer viene prima.

`tabella_giugno.py` compone la tabella di giugno 2026 (89 pagine x blocchi, con i
contenuti di ogni cella): riferimento del 19 settembre con le correzioni di
`runs/2026-10-09/correzioni_giugno.json`, cronaca di giugno riletta per intero, eventi
Facebook della raccolta dell'owner come stima dichiarata. Il foglio con i contenuti va
su Drive; qui restano i conteggi (`runs/2026-10-09/matrice_giugno_conteggi.csv`).

`campione.py` estrae il campione di controllo (seed fisso, stratificato per
fonte, esclusi i casi didattici): le regole della fase 1 si mettono a punto solo
sulle altre schede. Ogni nuova misura cieca usa un seed nuovo: il campione
dell'8 ottobre è stato visto durante le correzioni e vale solo come replay.
Un punto (civico o incrocio) a meno di 15 m dal confine della sua zona porta il
campo `confine` con le pagine al di là della linea: la fase 1 lo tratta come
candidato, non come prova precisa (DEC-107 aperta). `runs/2026-10-08/` contiene gli ID del campione e i
risultati aggregati della prova, senza testi delle fonti.

Test: `python3 tools/geo-assign/test_geo_assign.py` (con `QN_PKG` impostato
esegue anche i controlli sui casi didattici).

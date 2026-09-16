# Specifica di lettura delle registrazioni (Report 2, lotto A)

Deriva dallo schema del lotto A in `lotto_opus5/SPECIFICA.md`, con i marcatori a **10 secondi**
invece di 30 (HANDOFF §4). **Non si modifica mentre un lotto è in lettura.** Se una regola sembra
sbagliata, si applica e lo si scrive nel log.

## Che cosa si legge

`report2/manifest_video.csv` elenca gli item: `item_id`, `fonte`, `video_id`, `territorio`,
`organo`, `data_seduta`, `data_pubblicazione`, `durata_hm`, `parole`, `url`, `file`,
`verbale_match`, `convocazione_match`. Il testo sta nel percorso indicato da `file`, relativo a
`video/`. Le righe portano un marcatore `[mm:ss]` ogni dieci secondi.

**La trascrizione è automatica.** Nomi propri e toponimi sono spesso storpiati, le sigle quasi
sempre. `>>` segna un cambio di voce. Non si ricostruisce nulla: un toponimo incerto si scrive
come si sente e si segna `toponimo_da_verificare`. La piattaforma dichiara una confidenza per
parola: su YouTube **vale zero per ogni parola**, quindi non se ne tiene conto e si giudica il
testo.

## Che cosa si produce

Per ogni registrazione un file `report2/out_video/<item_id>.json`:

```
{"item_id":"V4_001","video_id":"…","territorio":"…","organo":"…","data_seduta":"AAAA-MM-GG",
 "durata_hm":"…","parole":0,
 "qualita_trascrizione":{"parole_al_minuto":0,"note":"≤ 30 parole su che cosa rende incerta la lettura"},
 "argomenti":["…"],
 "atti_collegati":{"convocazione":"sì|no|non verificato","verbale":"sì|no|non verificato","riferimento":"…"},
 "notizie_candidate":[{"titolo":"≤ 12 parole","sintesi":"≤ 60 parole","luoghi":["…"],
   "evidenza":["[mm:ss]","[mm:ss]"],
   "tipo":"delibera|mozione|risoluzione|ordine del giorno|interrogazione|sopralluogo|audizione|altro",
   "qualita":"alta|media|bassa",
   "novita_rispetto_agli_atti":"solo dal parlato|anche negli atti|non verificabile",
   "toponimo_da_verificare":"sì|no"}],
 "scheda_narrativa":"≤ 200 parole, senza nomi di persona",
 "tempo_lettura_s":0}
```

Ogni notizia candidata porta **almeno un marcatore** `[mm:ss]` in `evidenza`: senza il punto della
registrazione la notizia non è verificabile e non si scrive.

## Quando una cosa detta è una notizia candidata

Vale la stessa soglia degli atti: **un fatto che nasce lì**, su un luogo, un'opera, un impianto o
un servizio nominati, e che cambia qualcosa per chi abita quel territorio.

- `sì`: un voto su un atto che nomina un bene; un'audizione che accerta lo stato di un cantiere o
  di un servizio; un sopralluogo riferito in aula; un dato nuovo detto a voce e non scritto negli
  atti; una decisione contestata; un impegno con data o somma.
- `no`: discussione di regolamenti cittadini senza luogo; organizzazione interna dell'organo;
  approvazione di verbali; temi generali; formule collettive («le scuole del territorio», «i parchi
  del Municipio»): nominarle tutte equivale a non nominarne nessuna; un titolo di progetto non è
  un luogo.
- `qualita` = `alta` solo se il fatto è compiuto, datato e localizzato; `media` se annunciato o
  senza data; `bassa` se la trascrizione lascia dubbi sul fatto stesso.

`novita_rispetto_agli_atti` è il campo che questo rapporto esiste per riempire: **`solo dal
parlato`** quando la cosa detta non compare in nessun atto di giugno, `anche negli atti` quando il
verbale o la convocazione la riportano, `non verificabile` quando non si può stabilire senza
uscire dai materiali locali. Il controllo documentale si fa **senza rete**, su
`deliver/A2_2026-06_items.csv` e `deliver/A1_2026-06_items.csv`.

## Riservatezza (DEC-102, vincolante)

Nessun nome di persona nelle colonne, nel titolo, nella sintesi o nella scheda narrativa: al loro
posto il ruolo. **Un nome non è l'unico modo di identificare una persona**: niente numero civico
(la via sì), niente scala o interno, niente recapiti, niente dati anagrafici, niente condizioni
personali o di salute, niente date di evento personale.

Restano, perché sono fatti e non identificatori: **toponimi**, denominazioni di sedi, locali,
opere, associazioni, comitati e imprese — anche quando contengono un cognome — e **i nomi dentro
le intitolazioni e le commemorazioni**, perché lì il nome è la notizia (decisioni D1 e D3).

Quando nel log si documenta una rimozione, **non si riproduce l'identificatore rimosso**: né per
esteso, né con le iniziali, né nella forma storpiata dalla trascrizione.

Un'aula pubblica è piena di parlato personale che non è notizia: liti, stati di salute, vicende
private citate da chi interviene. Non entra nei file, nemmeno in forma anonimizzata, a meno che
non sia esso stesso l'oggetto di una decisione dell'organo.

## Emendamento del 16 settembre: su che cosa si verifica `novita_rispetto_agli_atti`

I primi due lotti (V4_001–V4_024) hanno usato come riscontro `deliver/A2_2026-06_items.csv`, che
**non porta l'oggetto degli atti**: solo tipologia, municipio e data. Con quel materiale il
riscontro è strutturalmente impossibile per quasi tutte le affermazioni, e il lettore del secondo
lotto lo ha segnalato. Da qui in avanti si usano i materiali che nel frattempo sono stati prodotti:

- `report2/confronto_atti.csv` — **tutti e 1.983 gli atti di giugno letti**, con organo, oggetto
  sintetico, luoghi, e il titolo della notizia candidata quando c'è. È il riscontro vero.
- `report1/db/notizie_candidate.csv` — le notizie già estratte da fonti testuali e atti: titolo,
  luoghi, date, fonte.

La regola resta quella: `anche negli atti` quando la stessa cosa compare in un atto o in una
notizia già estratta; `solo dal parlato` quando non compare da nessuna parte; `non verificabile`
quando l'atto potrebbe esistere ma non è isolabile. La differenza è che ora il `solo dal parlato`
si può sostenere invece di supporre. **Nella relazione va detto su quale dei due materiali è stato
fatto il riscontro**, perché i primi due lotti e i successivi non sono confrontabili su questo
campo.

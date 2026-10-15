# Studio delle fonti — metodo (Fase 0, step S2)

| Campo | Valore |
|---|---|
| Stato | **Metodo concordato, versione M-0.3.** Secondo controllo di Codex su M-0.2 (commit `8f2e2da`): **AGREEMENT WITH NON-BLOCKING RESIDUALS**, metodo eseguibile (`reviews/2026-09-14—sources-study-method-v2—AGREEMENT_WITH_NON-BLOCKING_RESIDUALS.md`). M-0.3 applica i due residui (frame di campionamento con seed e tie-break deterministico; quote del campione "fino a N, se disponibili"): correzioni **non riverificate** da Codex. Il primo controllo (M-0.1) era NO AGREEMENT (`reviews/2026-09-14—sources-study-method—NO_AGREEMENT.md`). Non è lo studio: è il modo in cui lo studio verrà condotto |
| Mandato | Risposta dell'owner del 14 settembre 2026 (§1–§5): ricerca, lettura, analisi e classificazione delle fonti pubbliche accessibili affidate all'Operator; studio che permetta di scegliere le fonti e stimare il prodotto alimentabile; budget di 50 € per prove rappresentative; nessun lavoro sproporzionato sulle fonti marginali |
| Cornice | `docs/PHASE_0_EXECUTION.md` step S2 e S6-D3; baseline v0.6 §2.A (flusso A); DEC-102 (posizione sulle fonti e sulla raccolta: nessuna automazione autenticata); DEC-104 (loop di sviluppo AI: repository pubblico, campioni fuori, decisioni dentro); DEC-014 (perimetro pubblico dell'MVP: 89 pagine, tre blocchi, stock minimi con fallback) |
| Stato dei dati | Ogni numero dello studio è marcato **misurato** (contato su materiale reale, con link), **stimato** (derivato con ipotesi dichiarate) o **mancante** |

## 1. Scopo e domande a cui lo studio risponde

Lo studio serve a decidere quali fonti alimentano i tre blocchi obbligatori del lancio
(Amministrazione, Cronaca, Eventi) e a stimare quanto prodotto ne deriva per pagina e per
mese. Risponde a cinque domande: quanto produce ogni fonte in un mese completo; quanto di
quel prodotto è localizzabile a Municipio e a quartiere; quanto è duplicato fra fonti;
cosa costa estrarlo (formato, affidabilità, intervento umano); quale copertura risulta per
le 89 pagine e dove restano i gap. Le 89 pagine e i minimi di DEC-014 restano il riferimento:
lo studio mostra le evidenze, non li modifica.

Fuori dallo studio: i gruppi e le pagine Facebook (accesso personale dell'owner, DEC-102:
la classificazione del censimento resta a S2-04, owner); le testate terze (RomaToday, ANSA,
Il Messaggero, Abitare a Roma e simili, elencate in *Next Step*): escluse dal riuso per
diritti (baseline §2.A, R), citate solo come confronto di copertura se serve.

## 2. Perimetro delle fonti e primo insieme da esaminare

Ordine: prima le fonti più accessibili e produttive; le difficili con prove limitate (§5).
Le fonti sono quelle di *Next Step* (Drive) e della baseline §2.A, integrate con gli
indirizzi ufficiali trovati il 14 settembre.

| # | Blocco | Fonte | Sezione di partenza | Formato atteso | Priorità |
|---|---|---|---|---|---|
| A1 | Amministrazione | Roma Capitale, portale istituzionale: pagine dei 15 Municipi, convocazioni di Consiglio e Commissioni, notizie | `comune.roma.it/web/it/municipio-N.page`, `…/informazione-di-servizio.page`, `…/notizie.page` | HTML, PDF | 1 |
| A2 | Amministrazione | Atti e verbali (Delibere e Atti Web) per i Municipi IV, VI, VII, XIII (e gli altri, per confronto) | `comune.roma.it/servizi2/deliberazioniAttiWeb/` | PDF testuale o scansione | 1 |
| A3 | Amministrazione | RomaTV streaming: commissioni dei Municipi II, III, VIII, X, XI, XII, XV e Commissioni Capitoline | `streaming.comune.roma.it/portal/…` (cataloghi in *Next Step*) | video | 2 (prova limitata) |
| A4 | Amministrazione | Canali YouTube dei Municipi I, V, IX, XIV | link in *Next Step* | video | 2 (prova limitata) |
| C1 | Cronaca | Questura di Roma, archivio comunicati | `questure.poliziadistato.it/it/Roma/archivio/…` | HTML | 1 |
| C2 | Cronaca | Carabinieri, comunicati stampa (filtro Roma e provincia) | `carabinieri.it/in-vostro-aiuto/informazioni/comunicati-stampa` | HTML | 1 |
| C3 | Cronaca | Procura di Roma, news e comunicati | `procura-roma.giustizia.it/it/news_e_comunicati.page` | HTML, PDF | 1 (volume da verificare: la sezione sembra contenere soprattutto circolari) |
| C4 | Cronaca | Vigili del Fuoco, Comando di Roma, interventi e notizie dal territorio | `vigilfuoco.it/comando-vvf-roma/interventi-roma` | HTML | 1 |
| C5 | Cronaca | Polizia Locale di Roma Capitale, notizie | `comune.roma.it/web/it/corpo-di-polizia-locale-di-roma-capitale.page`, notizie con filtro | HTML | 1 |
| C6 | Cronaca | Guardia di Finanza, comunicati del Comando regionale Lazio / Roma | `gdf.gov.it/it/gdf-comunica/notizie-ed-eventi/comunicati-stampa/territorio/comando-regionale-lazio/…` | HTML, PDF | 1 |
| E1 | Eventi (extra-Facebook) | 060608, manifestazioni ed eventi, con feed RSS | `060608.comune.roma.it/eventi`, `…/rss` | HTML, RSS | 1 |
| E2 | Eventi | culture.roma.it (Roma Culture, Sovrintendenza) | `culture.roma.it` | HTML | 1 |
| E3 | Eventi | Eventi dei Municipi sul portale istituzionale e agenda Roma Capitale | `comune.roma.it/web/it/eventi.page` | HTML | 2 |
| R1 | Regionale (riserva) | Consiglio regionale del Lazio, comunicati; BUR | `consiglio.regione.lazio.it`, `regione.lazio.it` | HTML, PDF | 3 |

Il primo insieme è tutto il livello 1 (A1, A2, C1–C6, E1, E2): dieci sezioni, tutte
pubbliche e senza login. Il livello 2 entra dopo il primo rapporto intermedio; il livello 3
solo se il livello 1 lascia gap dichiarati.

## 3. Cosa si misura per ogni fonte (scheda)

Una scheda per fonte, nel registro `docs/sources/SOURCE_REGISTRY.md` (template di S2-01),
con questi campi obbligatori:

1. **Utilità editoriale**: territorio coperto (città, Municipio, quartiere), argomenti,
   blocco alimentato.
2. **Produzione nel mese di osservazione** (§4): numero di item, frequenza osservata
   (per giorno/settimana), ritardo mediano fra fatto e pubblicazione dove la data del
   fatto è nel testo; per gli Eventi anche anticipo dell'annuncio e numero di eventi futuri
   nella finestra di 30 giorni.
3. **Localizzabilità**: quota di item con toponimo (via, piazza, quartiere, Municipio) e
   quota assegnabile deterministicamente a Municipio e a una delle 89 zone con gli alias del
   gazetteer (`gazetteer/gazetteer.json`, lookup deterministico come in
   `tests/zone_distribution.py`); il resto è "livello Municipio" o "non localizzato".
4. **Contenuto aggiuntivo e sovrapposizioni**: quota di item che riguardano lo stesso fatto
   di un'altra fonte del blocco, con la procedura di deduplicazione di §4.1; contributo
   unico della fonte (item non presenti in nessun'altra fonte del blocco).
5. **Formati e accesso**: HTML, PDF testuale, PDF scansione, audio, video; feed RSS; login;
   condizioni di riuso documentate (pagina licenza/termini trovata: sì/no, cosa dice, link)
   e verifiche ancora necessarie (per il legale, L11 dell'elenco dell'owner).
6. **Estrazione**: esito della prova sul materiale reale (§5): testo ottenuto sì/no, qualità
   (leggibile / con errori / inutilizzabile), tempo e costo per item, intervento umano
   prevedibile per item.
7. **Raccomandazione motivata**: usare / integrare / tenere in riserva / escludere, con la
   ragione e con la condizione che la cambierebbe.
8. **Stato del dato** per ogni numero: misurato / stimato / mancante.

## 4. Mese di osservazione, conteggio, deduplicazione e campione

### 4.1 Regole di conteggio e di deduplicazione

- **Mese comune: giugno 2026** (l'ultimo mese completo prima della pausa estiva delle
  istituzioni; agosto è escluso per regola, DEC-006 (fallback al Municipio per pagine
  sottili, residuo aperto)). Dove giugno è anomalo per una fonte (archivio incompleto,
  interruzione), si conta anche maggio 2026 e si dichiara quale mese vale.
- **Eventi**: oltre a giugno (volume e anticipo), la finestra corrente di 30 giorni in avanti
  dalla data della lettura (eventi futuri disponibili), perché è la grandezza che DEC-014
  usa per il pavimento di dieci eventi.
- **Cutoff**: un item appartiene al mese se la sua **data di pubblicazione** sulla fonte,
  letta nel fuso Europe/Rome, cade fra il 1° e il 30 giugno 2026 inclusi; item senza data di
  pubblicazione vanno nel gruppo "senza data" e non entrano nel conteggio del mese. Ogni
  conteggio registra la data e l'ora della lettura (Europe/Rome), l'URL di elenco usato e
  se la paginazione è stata percorsa fino a coprire tutto il mese (sì/no); un nuovo conteggio
  con le stesse regole deve dare lo stesso numero salvo modifiche della fonte, che vanno
  annotate.
- **Deduplicazione fra fonti dello stesso blocco** (stesso fatto pubblicato da due fonti):
  due item sono lo *stesso fatto* quando valgono tutte e tre le condizioni: (a) la data del
  fatto (o, se assente, di pubblicazione) coincide a ±1 giorno; (b) il luogo coincide —
  stesso toponimo normalizzato con le regole del gazetteer (alias, via/piazza) oppure stesso
  Municipio quando nessuna delle due fonti ha un toponimo più fine; (c) l'oggetto coincide —
  stesso tipo di fatto (per la Cronaca: arresto, sequestro, incendio, incidente, controllo;
  per l'Amministrazione: stesso atto o stessa seduta; per gli Eventi: stesso titolo
  normalizzato o stesso organizzatore con stessa data e luogo). Se (a) e (b) valgono ma (c)
  è incerto, l'item è marcato **dubbio** e la resa è riportata come intervallo
  (dedup minima = dubbi contati come distinti; dedup massima = dubbi contati come
  duplicati). Ogni duplicato o dubbio registra l'URL dell'item gemello e la ragione.
- **Estensione della deduplicazione**: sull'intero mese quando il blocco ha al massimo
  300 item complessivi nelle fonti di livello 1 (atteso per Cronaca ed Eventi); oltre, su
  un campione casuale di almeno 60 item per coppia di fonti, e la resa è marcata
  **stimata** con la dimensione del campione. Sull'intero mese la resa è **misurata**.
- **Campionamento riproducibile** (quando si campiona): il frame è l'elenco completo degli
  item del mese della fonte, ordinato per data di pubblicazione, poi per ordine
  predefinito delle fonti (A1, A2, …, C1, …, E1, …), poi per URL; l'estrazione usa un
  generatore pseudo-casuale con **seed fisso registrato** nel rapporto (uno per fonte, ad
  esempio `2026-06-<codice fonte>`); la lista campionata è salvata su Drive accanto ai
  dati per item, così che una ripetizione dia lo stesso campione.
- **Tie-break per "prima fonte che ha pubblicato"**: timestamp completo di pubblicazione
  se disponibile; a parità o in assenza dell'ora, l'ordine predefinito delle fonti; a
  parità residua, l'URL in ordine alfabetico. La regola applicata a ogni duplicato è
  registrata con il gemello.
- **Formula**: resa lorda del blocco = somma degli item delle fonti; resa netta = resa lorda
  − item già contati in un'altra fonte (un fatto è attribuito alla prima fonte che lo ha
  pubblicato); contributo unico di una fonte = suoi item non presenti altrove. Il rapporto
  riporta lorda, duplicati, dubbi, netta (minima e massima) per blocco e per fonte.

### 4.2 Dove stanno i dati per item (DEC-104, DEC-102)

I dati per item (una riga per item con URL, date, tag, flag, formato, esito della
deduplicazione) sono un dataset di fonte e **non entrano nel repository pubblico** (DEC-104,
regola 2; DEC-102: i dati di fonte non sono ridistribuiti come dataset). Stanno su Drive in
`QN Hub / 20 Packages / Fonti 2026-06/` (un CSV per fonte, senza testi integrali: URL, date,
Municipio, zona, tema, flag toponimo, flag nomi presenti, formato, gemello e ragione; i nomi
delle persone secondo DEC-105, cioè scritti quando sono pertinenti al fatto). Nel repository entrano solo gli aggregati e le metriche (conteggi per
fonte, Municipio, zona, tema e formato; quote; intervalli di dedup) e il riferimento alla
cartella Drive. Collocazione confermata dall'owner il 15 ottobre 2026 (DEC-109: inventari senza testi nel repository, dati con i testi su Drive).

**Nota del 15 ottobre 2026 (inventari in `handoff_data/`).** Gli inventari per item di
`tools/sources-study/handoff_data/` stanno nel repository per DEC-109 (decisione dell'owner
nella revisione della PR #15, lotto 3), che ne fissa il perimetro: URL, date, identificativi,
durate, conteggi, toponimi ed etichette dello studio, mai testi, titoli o nomi presi dalle
fonti. È l'unica eccezione a questo paragrafo; i dati con i testi restano su Drive.

**Nota del 15 ottobre 2026 (DEC-105).** «Senza nomi di persona» qui sopra era la regola dello
studio fino al 17 settembre; DEC-105 l'ha superata: nei dati per item su Drive i nomi pertinenti al
fatto si scrivono (`tools/sources-study/report2/SPECIFICA_NOMI_E_TERRITORIO.md`). Il confine di
questo paragrafo non cambia: i dati per item non entrano nel repository pubblico.

### 4.3 Campione per il controllo di Codex e dell'owner

- **Minimo di audit**: 5 item per fonte, con almeno uno per formato incontrato.
- **Quote mirate per le affermazioni critiche**, per blocco: fino a 20 item per la
  deduplicazione (fino a 10 giudicati duplicati e fino a 10 distinti, con i gemelli) e fino
  a 20 per la localizzazione (fino a 10 localizzati a zona e fino a 10 solo a Municipio o
  non localizzati), **se disponibili**: quando una categoria ha meno casi della quota, si
  prendono tutti i casi esistenti e il rapporto dichiara la numerosità effettiva, senza
  selezione opportunistica; per una fonte con più di 100 item nel mese le quote che la
  riguardano raddoppiano.
- I casi giudicati "sicuri" e quelli "dubbi" sono indicati come tali; se il controllo trova
  un errore sistematico, la parte di studio interessata è ricontrollata per intero prima
  della consegna.
- Il campione (link e passaggi pertinenti) vive con i dati per item su Drive; il rapporto
  nel repository rimanda alla cartella e riporta solo gli URL delle fonti ufficiali usate
  come esempio, senza passaggi.
- **Stagionalità e limiti**: un mese non è trasformato in previsione annuale; la stima annua,
  se serve, è dichiarata come stima con il fattore usato e i mesi di confronto disponibili in
  *Next Step* (gennaio–marzo 2026).

## 5. Prove sui formati e limiti sulle fonti difficili

| Formato | Prova | Strumento | Limite di sforzo | Dipendenza |
|---|---|---|---|---|
| HTML, RSS | lettura di 20 item per fonte, estrazione testo e date | fetch + parser locale | nessuno oltre il tempo | accesso di rete ai domini (§6) |
| PDF testuale | 5 verbali/delibere per fonte | estrazione locale con `pypdf`/`pdfplumber` (installabili da PyPI, raggiungibile: verificato il 14 settembre; `pdftotext` assente) | 1 h per fonte | accesso di rete |
| PDF scansione | 3 documenti | `tesseract` assente nell'ambiente (verificato): rendering delle pagine con PyMuPDF (installabile) e OCR via modello visivo API su 3 pagine per documento | 1 h; se la qualità è inutilizzabile, la fonte va in "riserva" con motivazione | accesso di rete; chiave OpenAI (nota in §7) |
| Video (RomaTV, YouTube) | 3 video di commissione, 20–60 min ciascuno, formati diversi | trascrizione API (due modelli: `gpt-4o-mini-transcribe` e `whisper-1`) e, come terza modalità a costo zero, `faster-whisper` su CPU se installabile da PyPI (`ffmpeg` è assente: la decodifica passa da PyAV); misura di costo, tempo e qualità per ora di video | 3 video in tutto (≈ 2–3 h di audio); nessun altro video prima della decisione D3 | audio da procurare: il download da `streaming.comune.roma.it`/YouTube richiede accesso di rete (probabilmente insufficiente per lo stream); in alternativa l'owner deposita i 3 file audio su Drive (`QN Hub / 20 Packages / prove`), che l'Operator legge già oggi |
| Audio senza video | come sopra | come sopra | idem | idem |

Regole per le fonti difficili (risposta dell'owner §2): **tetto di 2 ore di Operator e una
sola prova per fonte**; oltre, la fonte è classificata "riserva" o "da decidere" con esempi,
il contributo aggiuntivo stimato e le alternative (ricerca aggiuntiva, ampliamento del
bacino geografico, riduzione dei minimi, rinvio di alcune pagine) con costi, benefici e
perdita di copertura, e la decisione va all'owner. Una quota sotto il 5% non esclude da sola
una fonte che copra un quartiere altrimenti scoperto: si dichiara il quartiere.

## 6. Accesso alle fonti: domini da consentire e verifica

Verificato il 14 settembre: l'egress dell'ambiente Claude Code blocca `comune.roma.it`,
`questure.poliziadistato.it`, `facebook.com` e `quartierinews.app.n8n.cloud`; la ricerca
web e Drive funzionano. I risultati del motore di ricerca non valgono come accesso.

**Dal 9 ottobre 2026 l'ambiente QN ha accesso di rete Full** (qualunque dominio; scelta
dell'owner, verificata con il Geoportale di Roma, ASL Roma 1 e Wikipedia). L'elenco qui
sotto resta come registro dei domini che lo studio usa, e come configurazione da
ripristinare se l'ambiente torna a un elenco Custom.

**Domini da consentire nell'ambiente** (politica di rete personalizzata; documentazione:
https://code.claude.com/docs/en/claude-code-on-the-web; la modifica vale per le sessioni
avviate dopo):

| Dominio | Serve per |
|---|---|
| `www.comune.roma.it`, `comune.roma.it` | A1, A2, C5, E3 |
| `streaming.comune.roma.it` | A3 (cataloghi e, se fattibile, stream) |
| `060608.comune.roma.it` | E1 (pagine e RSS) |
| `culture.roma.it` | E2 |
| `questure.poliziadistato.it` | C1 |
| `www.carabinieri.it` | C2 |
| `procura-roma.giustizia.it` | C3 |
| `www.vigilfuoco.it`, `vigilfuoco.it` | C4 |
| `www.gdf.gov.it` | C6 |
| `www.youtube.com` (solo elenchi e metadati) | A4 |
| `consiglio.regione.lazio.it`, `www.regione.lazio.it` | R1 (riserva) |
| `pypi.org`, `files.pythonhosted.org` (se non già consentiti) | installazione di `pypdf`/OCR locale, se necessari |

Non richiesti: `facebook.com` (accesso personale, DEC-102), testate terze.

**Verifica dopo la modifica** (prima di considerare l'accesso risolto): lettura di una
pagina HTML per ciascun dominio, download di un PDF da `deliberazioniAttiWeb`, lettura del
feed RSS di 060608, esito riportato nel registro con data e URL. Se un dominio resta
bloccato, la fonte è "accesso mancante" e passa all'owner con la stessa scheda.

## 7. Programma di misure entro 50 €

Il budget copre tutte le prove preliminari, incluse ripetizioni, conversioni e imposte;
nessun abbonamento, nessuna ricarica automatica. Spesa e quantità sono registrate in
`docs/sources/TRIAL_LEDGER.md` (data, prova, quantità, costo, residuo) e lo studio si ferma
prima di superare il tetto.

| Prova | Quantità | Costo stimato | Cosa misura | Dipendenza |
|---|---|---|---|---|
| T1 Trascrizione video | 3 video × 2 modelli API (≈ 2–3 h di audio) | 1–3 € | costo, tempo e qualità per ora di video (input di D3) | audio disponibile (§5); chiave OpenAI: vedi nota |
| T2 OCR su scansioni | 3 documenti (≈ 15 pagine) | 0–1 € (0 se OCR locale) | leggibilità e costo per pagina | accesso di rete |
| T3 Estrazione e classificazione AI | 60 item (20 per blocco) con un modello economico | 1–3 € | precisione di localizzazione e tema, costo per item, quota `uncertain` | accesso di rete per gli item; chiave OpenAI |
| T4 Verifica con seconda AI | 30 item già classificati (modello diverso da T3) | 2–5 € | costo per item della verifica, quota inviata in coda (input per DEC-015 e D9) | come T3 |
| T5 Prova Apify su 5 URL | 1 run | < 0,1 € | funzionamento dello staging (P0-S1-02) | credenziali ruotate (S0) e staging pronto |
| T6 Quattro raccolte settimanali (lotto operativo) | 4 run, ~100–200 URL ciascuno | 5–12 € | M1 | **non in questo budget senza autorizzazione successiva** (risposta dell'owner §5) e subordinate a S0 |
| Riserva per ripetizioni e conversioni | — | 5–10 € | — | — |

Totale pianificato delle prove T1–T5: circa 5–12 €, ben sotto il tetto; T6 è preventivato,
non autorizzato. **Regola sulla chiave OpenAI (fail-closed)**: T1, T3 e T4 sono **bloccate**
finché l'owner non conferma per iscritto che la chiave presente nell'ambiente dell'Operator
è distinta da quella esposta in R0, oppure la rotazione è completata e verificata (S0-03).
In assenza di conferma la chiave si considera esposta. I controlli di Codex proseguono solo
perché l'owner li ha esplicitamente disposti (risposta del 14 settembre §3), e restano
l'unico uso della chiave fino alla conferma.

**Previsione dei costi del progetto** (consegna dello studio): distingue costi iniziali e
mensili a regime; raccolta, OCR, trascrizione, AI di produzione e di verifica, errori e
ripetizioni, ore umane; tre scenari (basso, centrale, alto) con quantità e ipotesi
esplicite prese dai conteggi di giugno e dai prezzi misurati nelle prove; l'incertezza
residua è dichiarata, non nascosta in una cifra. Include la verifica della sufficienza del
piano n8n Cloud Starter (2.500 esecuzioni/mese, dato dell'owner del 14 settembre) contando
le esecuzioni previste per workflow e cadenza, non il numero di notizie.

## 8. Consegne, verifica e passaggi all'owner

1. **Registro fonti** (S2-05) con una scheda per fonte e gli aggregati di conteggio; i CSV
   per item su Drive (§4.2).
2. **Rapporto dello studio** (previsto come `docs/sources/SOURCE_STUDY_2026-09.md`; consegnato come `SOURCE_STUDY_2026-09_RAPPORTO_INTERMEDIO.md`, `FATTIBILITA_RICOSTRUZIONE_2026-06.md`, `RICOSTRUZIONE_2026-06_REPORT1.md` e `RICOSTRUZIONE_2026-06_REPORT2.md`): copertura per
   Municipio e per zona e per argomento; resa dopo la deduplicazione; gap e complessità
   attese; raccomandazione per fonte; costi misurati; i tre scenari; le proposte, i problemi
   residui e le domande circoscritte per l'owner, ciascuna con prove, esempi, alternative,
   conseguenze e raccomandazione.
3. **Campione per il controllo** (§4.3) con link e passaggi pertinenti, su Drive con i dati
   per item; il rapporto rimanda alla cartella.
4. **Controlli di Codex**, come concordato dall'owner: (a) questo metodo, prima di estendere
   lo studio; (b) la consegna, prima delle decisioni dell'owner — evidenze, conteggi,
   duplicazioni, campione di originali, complessità proposta, alternative trascurate. Nessun
   ciclo intermedio salvo problemi sostanziali. Se un errore sistematico emerge dal campione,
   la parte interessata dello studio è ricontrollata prima della consegna.
5. **Rapporto intermedio** dopo il livello 1 (§2): decide se il livello 2 serve.

Cosa resta all'owner in questo step: l'accesso di rete (§6); gli eventuali file audio su
Drive (§5); i gruppi Facebook (S2-04); la conferma scritta sulla chiave OpenAI (§7); la
conferma della collocazione dei dati per item (§4.2); le decisioni che lo studio rende
visibili (fonti di record: D3; minimi e pagine: solo su evidenze).

## 9. Attività immediatamente eseguibili e attività dipendenti

**Subito, con gli strumenti attuali**: schede e priorità delle fonti da *Next Step* e dalle
ricerche (senza conteggi); template del registro e dei CSV; script di conteggio e di
localizzazione deterministica pronti sul gazetteer; ledger delle prove; lettura dei
documenti Drive già accessibili; preparazione delle richieste all'owner (domini, audio,
chiave).

**Dopo l'apertura dei domini** (§6): conteggi di giugno per A1, A2, C1–C6, E1, E2; prove
HTML/PDF/OCR (T2); campione.

**Solo dopo la conferma scritta sulla chiave OpenAI o la rotazione verificata**: T1, T3, T4
(bloccate fino ad allora, §7).

**Dopo la rotazione delle credenziali e lo staging** (S0, S1-02): T5; T6 solo con
autorizzazione sulla previsione.

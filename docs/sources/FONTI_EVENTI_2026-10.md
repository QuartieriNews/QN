# Fonti degli Eventi: aggregatori, Apify e registro delle fonti dirette (13 ottobre 2026)

Che cosa è stato misurato il 13 ottobre sulle fonti degli Eventi, che cosa ne segue e che cosa
resta da decidere. Strumenti: `tools/fonti-eventi/`. Nel repository stanno solo metodo e
conteggi; titoli, nomi dei luoghi e indirizzi delle pagine sono su Drive, cartella
`QN Hub / 20 Packages / Fonti 2026-06` (DEC-102, DEC-104).

Il punto di partenza è la tabella di giugno (`tools/geo-assign/runs/2026-10-09/`): solo 27
pagine su 89 arrivano a 10 eventi contando giugno e la raccolta Facebook dell'owner. Gli Eventi
sono il blocco più scoperto.

## 1 Apify e Claude Code

- **Il collegamento.** Dal 24 settembre la directory di Anthropic offre il plugin ufficiale
  Apify per Claude Code: server MCP `mcp.apify.com`, un agente e cinque skill. Il plugin
  funziona solo in Claude Code locale. In una sessione cloud servono un connettore
  personalizzato con l'URL del server, oppure un token Apify nelle impostazioni dell'ambiente.
  Il 13 ottobre nessuno dei due era attivo in questa sessione: `mcp.apify.com` risponde 401
  senza token. L'API pubblica del negozio di Apify invece risponde.
- **Prezzi letti dall'API pubblica**, piano gratuito, per elemento restituito:

  | Actor | Prezzo |
  |---|---|
  | Facebook Events Scraper | 0,013 $ a evento più 0,001 $ ad avvio (agosto: 107 eventi per 1,40 $) |
  | Facebook Posts Scraper | 0,005 $ a post, più 0,002 $ con il filtro di data |
  | Facebook Groups Scraper | 0,005 $ a post (solo gruppi pubblici) |
  | Facebook Pages Scraper | 0,012 $ a pagina |
  | Facebook Search Scraper | 0,006 $ a risultato; 0,012 $ con la ricerca predefinita via Google, che QN non usa |

  Il piano gratuito include 5 $ al mese.
- **Trappole tecniche.**
  - Nel Website Content Crawler `respectRobotsTxtFile` vale `false` quando l'Actor è chiamato
    via API o MCP. Il `true` del modulo della console è solo precompilato. Va passato
    esplicitamente.
  - Il proxy di Apify è acceso di default.
  - Secondo i loro README, gli Actor Facebook di Apify girano su proxy residenziali. L'uso per
    gli eventi resta quello deciso in DEC-102; il §5.1 di `CRONACA_PROCESSO_2026-10.md`
    esclude i proxy residenziali per le testate.
- **Modalità di estrazione per gli Eventi.**

  | Modalità | Rendimento | Stato |
  |---|---|---|
  | Ricerca per parola (`searchQueries`) | 5 eventi locali su 30 (agosto) | da scartare |
  | Explore Roma | spinto verso eventi grandi e turistici | rete di sicurezza |
  | URL di eventi raccolti a mano | la qualità migliore, circa un'ora a settimana | modalità attuale |
  | Calendario delle pagine (`/PAGINA/upcoming_hosted_events`) | da misurare | ammesso dall'Actor senza login |
  | Post delle pagine più lettura con l'AI | nella prova manuale del 16 settembre: 220 pagine, 56 con post nella settimana, 109 post, 69 eventi, circa 0,011 $ a evento | — |

  Nei 69 eventi della prova del 16 settembre la data c'è nel 94% dei casi, l'ora nel 70%, il
  luogo nominato nell'87%, l'indirizzo solo nel 19%; il 57% non dice il quartiere. Il calendario
  delle pagine cambierebbe la scoperta da «URL raccolti da una persona» a «pagine scelte da una
  persona»: serve una decisione dell'owner (spec: `discovery_strategy: manual_url_collection`).
- **Gruppi Facebook** (campione pubblico del 16 settembre): su 91 gruppi, 9 leggibili senza
  login, 81 rimandano al login, 1 privato. Ne escono 27 post, di cui 2 annunciano un evento.
  Per gli Eventi non servono. La Conversazione resta legata a S2-04 e alla questione legale 9.

## 2 Tre aggregatori a confronto (finestra 13–31 ottobre)

| | Comune (agenda di Roma Capitale) | Meetup | RomaToday |
|---|---|---|---|
| Accesso | sito aperto, letto | ricerca con parametri vietata dal robots.txt; lette solo le pagine di città della sitemap | esclude gli agenti AI nel robots.txt e riserva l'estrazione: mai aperto; titolo, data e link raccolti a mano dall'owner |
| Elementi letti | 51 schede pubblicate dal 13 settembre | 27 eventi di Roma (26 pagine) | 324 link |
| Nella finestra, a Roma | 32 | 24 | 116 link, 109 eventi |
| Nuovi rispetto alle altre due | — | — | 98 (11 già sul Comune, 0 su Meetup) |
| Rilevanti per QN | soprattutto gli eventi dei Municipi e delle biblioteche (4 su 16 schede nuove della settimana) | circa 2 a settimana | 70: 49 di quartiere, 21 cittadini in un luogo di quartiere |
| In pagine sotto la soglia dei 10 eventi | — | — | 10 eventi, 9 pagine |

**Dettaglio di RomaToday.** Dei 324 link:
- 113 erano già passati: la pagina mostrava anche eventi recenti;
- 33 sono fuori Roma;
- 85 non hanno data nel titolo né nel link;
- 7 sono doppioni dello stesso evento.

La classificazione si basa solo su titolo e link: finestra, Roma o no, zona QN, filtro
editoriale di `prompts/EDITORIAL_FILTER.md`, rilevanza, corrispondenze. L'hanno fatta cinque
agenti, con un secondo agente per lotto che ha corretto 49 campi. La rilettura dell'operatore
ha riguardato le 116 righe nella finestra. Meetup, a Roma, è socialità per stranieri e
networking: rende poco ai quartieri.

**Conclusione.** RomaToday ha il volume, ma come testata chiusa vale solo come segnale
(DEC-108). Il Comune è ammesso, ma è soprattutto agenda culturale del centro. Nessuno dei tre
copre la periferia scoperta.

## 3 Il registro delle fonti dirette

Proposta del builder, approvata dall'owner il 13 ottobre: usare RomaToday come **mappa degli
organizzatori**, non come fonte. Si costruisce l'elenco dei luoghi e degli organizzatori e poi
QN legge loro: siti, pagine Facebook (DEC-102), newsletter.

**Ingressi:**
- i luoghi delle righe di RomaToday pertinenti e a Roma, passate comprese: 278 righe, 193 con
  un luogo, 139 luoghi candidati;
- le 51 schede del Comune;
- le 220 pagine Facebook curate dall'owner, con la prova del 16 settembre.

**Validazione.** L'owner ha delegato la validazione per questa sessione. Regole applicate:
- **tenere:** luogo o organizzatore a Roma con un programma pubblico ricorrente e almeno un
  canale pubblico;
- **scartare:** fuori Roma; promozioni di marchi, negozi, alberghi e ristoranti; organizzatori
  occasionali; aree generiche; enti nazionali, politici o tematici senza programma locale;
  probabili profili personali;
- **sospeso DEC-001:** visite guidate a pagamento;
- **da verificare:** identità o luogo incerti.

**Canale di lettura:**
- il sito, se il robots.txt ammette la pagina dell'agenda (verifica automatica, `robots.py`
  secondo RFC 9309);
- altrimenti la pagina Facebook;
- altrimenti nessuno.

Un sito che esclude gli agenti AI per nome conta come chiuso (§5.1).

**Risultato** (conteggi in `tools/fonti-eventi/runs/2026-10-13/registro_conteggi.json`; il
registro con nomi e link è su Drive, «Registro fonti eventi — 13 ottobre 2026»):

| | Fonti |
|---|---|
| Righe del registro, doppioni uniti (stessa pagina Facebook, stesso dominio o stesso nome) | 370 |
| Da tenere | 193 |
| Da verificare | 39 |
| Da scartare | 138 |

**Le 193 da tenere.**
- **Canale:**
  - sito ammesso dal robots.txt: 94;
  - pagina Facebook: 84;
  - sito che nega l'accesso (un robots.txt «vietato», un 403): 2;
  - sito non raggiunto da questo ambiente, o che risponde con un errore, senza social: 12;
  - nessun canale: 1.
- **Formato dei 94 siti:** 60 offrono un formato leggibile da una macchina (feed, API
  WordPress, dati schema.org Event); 34 sono solo HTML.
- **Tipo:** biblioteche 40, comitati di quartiere 30, musei 28, teatri 24, poi associazioni,
  istituzioni, centri culturali, gallerie e club.
- **Zona:** 169 hanno una zona QN, in 53 zone. 53 stanno in pagine oggi sotto la soglia dei 10
  eventi.

**Pagine sotto la soglia.** Delle 62, 32 hanno almeno una fonte nel registro. Le altre 30 non
ne hanno nessuna (elenco nel file dei conteggi). Sono soprattutto periferia: litorale,
quadrante nord-ovest e quadrante est. Lì servono Municipi, parrocchie e comitati cercati
apposta.

**Pagine Facebook curate dall'owner (220).**
- 86 da tenere;
- 15 da verificare;
- 119 da scartare: 41 tematiche non locali, 26 politiche, 16 enti nazionali o regionali, e
  comitati fermi da anni, comitati genitori di una scuola o comitati su un solo tema. L'attività
  delle pagine viene dalla prova del 16 settembre.

**Limiti.**
- **Che cosa è stato verificato.** Nomi, zone e siti vengono dagli assistenti, con al più
  dieci ricerche web ciascuno. Ogni sito è stato verificato da `verifica_canali.py`; i social
  no.
- **Siti non raggiunti.** 14 siti, quasi tutti di enti noti (anche statali, `beniculturali.it`),
  non rispondono da questo ambiente: risposta 000 dal proxy. Non sono chiusi; vanno
  ricontrollati da una rete italiana.
- **Righe rimaste fuori.** 70 righe di RomaToday senza luogo non hanno dato fonti.
- **Facebook manca ancora.** Gli organizzatori dei 297 eventi raccolti su Facebook il 13 ottobre
  entreranno quando Apify li avrà estratti.

## 4 Prima lettura alla fonte (13 ottobre, una sola istantanea)

**Come è stata fatta:**
1. le 94 fonti da tenere con canale «sito» sono state lette una volta ciascuna, alla pagina
   dell'agenda o alla home, con `leggi_agende.py`: 93 lette;
2. otto agenti hanno estratto gli eventi della finestra 13–31 ottobre dai soli testi salvati;
3. un agente ha confrontato quegli eventi con i 109 eventi di RomaToday nella stessa finestra.
   Ne ha confrontati 108; uno è rimasto fuori.

Conteggi: `tools/fonti-eventi/runs/2026-10-13/copertura_conteggi.json`.

| Misura | Valore |
|---|---|
| Pagine con un'agenda datata leggibile | 47 |
| Pagine con pochi eventi in evidenza | 23 |
| Pagine senza eventi | 16 |
| Pagine non utili | 7 |
| Eventi della finestra letti alla fonte | 281, da 60 fonti |
| Eventi di RomaToday trovati alla fonte | **33 su 108 (31%)**: 11 di quartiere, 12 cittadini in un luogo di quartiere, 10 del centro |
| Eventi letti alla fonte che RomaToday non ha | circa 248 |
| Zone dei 281 eventi | 19 |
| Eventi in pagine sotto la soglia | 16, in 4 pagine |

**Perché mancano i 75 eventi di RomaToday non trovati:**

| Motivo | Eventi |
|---|---|
| Il luogo non è nel registro (luogo non nel titolo, o generico) | 37 |
| La fonte ha un sito, ma la pagina letta (spesso la home) non mostrava l'evento | 18 |
| La fonte è da verificare | 7 |
| La fonte ha un sito non raggiunto | 7 |
| La fonte è stata scartata | 4 |
| La fonte ha un sito chiuso | 1 |
| La fonte è solo su Facebook | 1 |

**Lettura.**
- **Più eventi di RomaToday, e diversi.** Leggere alla fonte dà molti più eventi di quanti
  RomaToday ne mostri, ma non gli stessi: un terzo dei suoi.
- **Dove sono i buchi.** Mancano soprattutto organizzatori non ancora nel registro e agende
  lette dalla home. Non dipendono dai canali chiusi.
- **La periferia resta scoperta.** I 281 eventi stanno nel centro e nel semicentro, come le fonti
  che RomaToday ha fatto scoprire. Fra i 281, i 51 dei cinema sono in gran parte proiezioni.
- **Le 84 fonti solo Facebook non sono ancora lette**, soprattutto biblioteche e comitati di
  periferia: aspettano Apify.

## 5 Che cosa resta all'owner

1. **Apify.** Collegamento con un connettore o un token dedicato, con tetto di spesa per run.
   Budget della prova comparativa, circa 9–10 $: oltre il piano gratuito.
2. **Calendario delle pagine (modalità 4).** Se è ammesso: cambia `discovery_strategy`.
3. **Altre superfici Meta.** Instagram e gruppi non sono coperti da DEC-102: per le fonti che
   pubblicano solo lì serve una decisione.
4. **Domanda per il parere legale (D12).** L'uso periodico di un aggregatore chiuso per
   scoprire organizzatori, e non per riprenderne l'agenda, rispetto al diritto sulle banche
   dati (art. 102-bis l. 633/1941).
5. **Prova di due settimane.** Si raccoglie dalle fonti del registro e si confronta con
   l'agenda di RomaToday, solo per titolo e data. La misura è la quota di eventi di RomaToday
   che QN trova da solo.

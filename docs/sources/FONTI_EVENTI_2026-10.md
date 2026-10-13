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

<!-- REGISTRO -->

## 4 Che cosa resta all'owner

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

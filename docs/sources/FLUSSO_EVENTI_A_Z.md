# Flusso eventi da A a Z: dalle fonti alla home del quartiere (proposta, 24 ottobre 2026)

Proposta del builder (DEC-104) per il blocco eventi in esercizio continuo: quali fonti si
leggono, ogni quanto, con quale strumento, e i passi da una riga letta alla pubblicazione
nella home della pagina di quartiere. Non decide nulla: le scelte aperte sono DEC-023,
DEC-024, DEC-025 e DEC-026; i contratti di fase restano quelli della specifica v2.5 (Drive,
QN Hub / 10 Specifications), qui citati per numero e mai riscritti. Il punto di partenza
misurato è `docs/sources/FONTI_EVENTI_STATO_2026-10-24.md`.

## 1. Le fonti, in quattro famiglie

| Famiglia | Che cosa contiene oggi | Dove sta |
|---|---|---|
| **Aggregatore istituzionale** | culture.roma.it, l'agenda di Roma Capitale: circa dieci schede nuove al giorno, quasi tutte con organizzatore, sito e coordinate | `tools/fonti/leggi_culture_roma.py` |
| **Siti delle fonti** | i siti verificati di luoghi, organizzatori e enti: registro fonti v3, censimento delle pagine Facebook, censimento RUNTS, elenchi istituzionali (biblioteche, centri anziani, istituti comprensivi, mercati) | schedario della wiki, `dove_cercare`; `tools/fonti/leggi_eventi_siti.py` |
| **Pagine Facebook delle fonti** | le pagine di organizzatori e luoghi: pochi eventi Facebook, molti annunci nei post | registro v3 (220 pagine verificate dall'owner), censimenti del 24 ottobre |
| **Aggregatori non letti** | Roma Today (licenza Citynews, DEC-026); aggregatori commerciali (Fever, Spotlight, Eventivicino e simili) | nessun canale: un evento visto solo lì si cerca alla fonte |

## 2. Ogni quanto si legge che cosa

La cadenza non è per famiglia ma per **livello di produttività**, misurato e rivisto ogni mese
(§4, passo M). I livelli partono dai verdetti dei censimenti del 24 ottobre.

| Livello | Chi ci sta | Canale e strumento | Cadenza | Costo stimato |
|---|---|---|---|---|
| **0 — agenda** | culture.roma.it | API per differenza (`modified_after`), scheda per ogni voce nuova | ogni giorno | 0 $ |
| **1 — calendario** | fonti con calendario sul sito (date future, schema.org Event), le 62 fonti lette alla fonte a ottobre, Biblioteche di Roma e Casa delle Letterature, teatri e musei del registro | pagina eventi del sito (lettore dei siti); pagina Facebook `/events` | ogni settimana | 0 $ |
| **2 — annunci** | fonti che annunciano nei post o hanno eventi futuri su Facebook; fonti «da verificare» con un solo segnale | eventi delle pagine (`pageUrls`, solo futuri) ogni due settimane; post degli ultimi 30 giorni una volta al mese | due settimane / mese | circa 1 $ + 10-15 $ al mese |
| **3 — presenza** | fonti presenti sul web senza segnali di eventi; elenchi istituzionali (centri anziani, istituti comprensivi, mercati, comitati delle pagine deboli) | pagina da controllare dello schedario | ogni mese | 0 $ |
| **4 — dormienti** | pagine e enti senza eventi, post o date negli ultimi sei mesi | rilettura completa | ogni sei mesi (prossima: marzo 2027) | 2-5 $ |
| **Scoperta** | organizzatori nuovi | «a cura di» delle schede nuove di culture.roma.it; organizzatori degli eventi Facebook delle pagine note; liste dell'owner; ricerca per parole chiave su Facebook solo come controllo | continua; parole chiave ogni tre mesi | 1 $ a trimestre |
| **Segnalazioni in entrata** | organizzatori che rispondono all'avviso del passo L | modulo «segnala il tuo evento» | continua | 0 $ |

Spesa Apify a regime: circa 15-20 dollari al mese, contro i 138 dei censimenti di ottobre.
Il tetto mensile va scritto nella configurazione prima che la schedulazione parta (DEC-004).

## 3. Chi esegue

Ogni lettore è uno strumento con test nel repository (`tools/fonti/`); la schedulazione è un
workflow n8n che gira in **staging** (cartelle Drive e collezioni Firestore con prefisso
`staging_`) finché il passaggio non è APPROVED e non c'è uno smoke test verificato (CLAUDE.md).
Il workflow `scrape-fb-events-rome.json` resta la base di produzione pre-refactor finché
l'owner non decide (DEC-024 Q3).

## 4. Da A a Z: una riga letta diventa un evento nella home del quartiere

| Passo | Che cosa succede | Regola che lo governa |
|---|---|---|
| **A. Registro** | Il registro fonti (Drive) dice per ogni fonte: id, decisione, livello, cadenza, `dove_cercare`, canale. È l'unico elenco che i lettori seguono | DEC-024; wiki `docs/wiki/fonti-eventi/` come stampa del registro |
| **B. Calendario** | Lo scheduler lancia per ogni livello il lettore giusto, con il tetto di spesa | §2 di questo file |
| **C. Lettura** | Ogni lettore scrive righe grezze con `fonte_id`, URL della fonte e data di lettura, fuori dal repository (Firestore `staging_`) | DEC-022, DEC-109: i titoli sono testo delle fonti |
| **D. Normalizzazione** | Titolo, inizio e fine in `Europe/Rome`, luogo, indirizzo, prezzo, organizzatore, link alla fonte primaria | Spec v2.5, contratto canonico (Parte III) |
| **E. Geografia** | Luogo noto (registro dei luoghi) → coordinate → Municipio e suddivisione ufficiali → pagina QN; il gazetteer vince; fuori Roma o online: flag, non scarto | `prompts/PROMPT_GEO_BLOCK.md`, `gazetteer.json`; `tools/geo-assign/qngeo.py punto` |
| **F. Doppioni** | Gli eventi uguali da fonti diverse diventano un gruppo con una riga principale | DEC-025 (aperta) |
| **G. Filtro editoriale** | Interesse locale sì, propaganda e pubblicità no; i casi dubbi vanno in coda | `prompts/EDITORIAL_FILTER.md` |
| **H. Rintracciabilità** | Ogni evento pubblicato porta il link alla fonte primaria; se la fonte è solo un aggregatore, l'evento aspetta una ricerca alla fonte | DEC-102 (credito e link) |
| **I. Arricchimento** | Categoria, gratuito o a pagamento, età; immagine solo secondo la politica delle immagini | DEC-101 |
| **J. Revisione** | Coda unica per geografia incerta, doppioni dubbi, fonti candidate, filtro editoriale incerto; campione settimanale | `docs/REVIEW_QUEUE.md` |
| **K. Pubblicazione** | L'evento compare nel blocco eventi della **home della pagina di quartiere**, in ordine di data, senza pagina propria; sparisce da solo dopo la fine | Spec v2.5: la pagina decide che cosa mostrare al momento dell'impaginazione |
| **L. Avviso all'organizzatore** | Email all'indirizzo ufficiale dell'ente (censimento RUNTS, colonna `email_principale`) con il link alla pagina del quartiere e l'invito a segnalare i prossimi eventi; un solo avviso al mese per ente; link per non ricevere più avvisi | invii a piccoli lotti, prima agli enti con eventi pubblicati; base giuridica e testo da decidere con l'owner |
| **M. Misura e ritorno** | Ogni mese: eventi futuri per pagina (soglia di DEC-014), fonti che hanno prodotto, quota rintracciabile alla fonte; una fonte con almeno due eventi nel mese sale di livello, una senza eventi per due cicli scende; la wiki si rigenera | `tools/wiki/build_fonti_eventi.py` |

## 5. Che cosa manca per farlo girare

1. Le decisioni DEC-023, DEC-024, DEC-025, DEC-026.
2. Il lettore dei post con finestra di 30 giorni come strumento con test (oggi è uno script di
   lavoro in `tools/fonti/lavoro-2026-10/`).
3. Geografia, doppioni e rintracciabilità come strumenti con test (oggi script di lavoro).
4. Il pacchetto Metodo QN nell'ambiente, per `qngeo.py punto`.
5. Il modulo di segnalazione e il testo dell'avviso agli organizzatori.
6. Il workflow n8n di staging con i lettori del §2 e i tetti di spesa.

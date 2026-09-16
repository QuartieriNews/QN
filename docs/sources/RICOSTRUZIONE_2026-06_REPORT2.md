# Ricostruzione di giugno 2026 — Report 2: gli atti e le registrazioni

Bozza in lavorazione. I materiali sono letti per intero sul lato atti e per circa metà sul lato
registrazioni; **i conteggi qui dentro sono quelli al 16 settembre e vanno rigenerati prima della
consegna** con `report1/build_db.py`, `report2/novita_meccanica.py` e `report2/audit_toponimi.py`.
Le conclusioni qualitative non dipendono dai lotti che mancano: si ripetono identiche da otto lotti.

Perimetro: **8–28 giugno 2026**, come prescrive il metodo. Il Report 1 aveva letto 985 item
testuali e ne aveva ricavato 1.227 notizie candidate.

## 1. In breve

- Letti **1.983 atti amministrativi** — tutti quelli con data di repertorio fra l'8 e il 28 giugno,
  che è il perimetro dello studio — e **415 registrazioni di sedute**, 97 dai canali YouTube dei
  Municipi e 318 da RomaTV. Alla data di questa bozza le registrazioni lette sono **193**.
- Gli atti danno **544 notizie candidate** (27,4%), le registrazioni **863** finora.
- La domanda del rapporto — *quanto aggiunge il parlato a ciò che è scritto* — non ha una risposta
  sola. Ne ha tre, misurate: **37,5%** di novità certa con un toponimo affidabile, **55%** di novità
  certa, fino al **99%** come limite superiore.
- La scoperta che regge tutto il resto non è un numero ma una frase, scritta in due verbali:
  **«la videoregistrazione sostituisce la trascrizione degli interventi».** L'ente dichiara che il
  record di ciò che si dice è il video, non l'atto. Tutto il resto discende da qui.

## 2. La risposta, e perché sono tre numeri

Il campo che i lettori compilano riga per riga (`novita_rispetto_agli_atti`) è un giudizio, e nel
corso dello studio è stato definito **tre volte in modo diverso** — due delle quali per errori miei,
corretti e dichiarati. Non è quindi una serie omogenea, e non può essere il numero principale.

Il numero principale è meccanico: ogni candidata che viene dal parlato è confrontata, con la stessa
deduplicazione usata per tutto il corpus, contro **tutte le righe che vengono da fonti scritte**.
Tre esiti:

| | |
|---|---|
| **S** — nessun gemello fra le righe scritte | 476 |
| **U** — nessun duplicato, ma almeno un accostamento dubbio | 375 |
| **D** — almeno un duplicato certo | 12 |

Da cui la scala:

- **37,5%** — nuove, con un toponimo che il lettore non ha marcato incerto. È il pavimento: regge
  a qualunque obiezione.
- **55,2%** — nuove, cioè senza alcun gemello scritto, toponimi incerti compresi.
- **98,6%** — limite superiore, se si contano come nuove anche quelle che hanno solo un
  accostamento dubbio.

**Contro che cosa sono misurati, detto con precisione.** Contro i 1.983 atti con data di repertorio
fra l'8 e il 28 giugno, che è il perimetro dello studio. Gli altri 685 atti di giugno che abbiamo in
archivio sono dell'1–7 e del 29–30: fuori finestra per costruzione, non dimenticati.

C'è però un punto in cui il perimetro, definito sulla data di repertorio, **non coincide con il
perimetro dei fatti**. Per i verbali la data di repertorio è la data della seduta, e allora il
verbale di una seduta dell'8–28 giugno sta sempre dentro. Per le **convocazioni** la data di
repertorio è quella del protocollo, che precede la seduta: la convocazione di una seduta dei primi
giorni della finestra, protocollata prima dell'8, **resta fuori**. È una conseguenza necessaria
della definizione, la stiamo chiudendo leggendo quelle convocazioni, e tocca il collegamento fra
registrazione e atto, non il gemello scritto di una notizia.

Resta un limite che non si chiude e va dichiarato: **il verbale di una seduta di fine giugno
repertoriato a luglio non è nella raccolta.** Non è un problema di insieme di confronto — è un
documento che non abbiamo.

La larghezza non è un'incertezza da nascondere: **è il risultato**. Dice che la risposta dipende da
quanto ci si fida di una trascrizione automatica, e che un terzo delle notizie «certamente nuove»
poggia su un toponimo che il lettore stesso ha segnalato come dubbio.

**Che cosa misura questo numero, detto una volta per tutte.** Misura la novità **territoriale**: un
fatto su un luogo nominato che non sta scritto. Non misura la novità politico-istituzionale — il
numero legale che salta, la seduta che decade, l'ufficio che non si presenta — che la soglia di
notiziabilità esclude per costruzione. Quella parte sta nel §4 e non è meno importante.

**E una notizia nuova è meno verificabile di una confermata.** Fra le candidate che gli atti
confermano, il 55,4% è di qualità alta; fra quelle nuove, il 25,4%.

Il perché è un effetto di selezione, e non riguarda la qualità del parlato. Un fatto compiuto,
datato e localizzato **tende per costruzione a generare un atto**; e appena lo genera esce dalla
colonna «solo dal parlato». Quello che resta nel parlato è allora, per definizione, il **residuo**:
annunci senza data, proposte non deliberate, lavori fermi da mesi, assenze, risposte mancate —
fatti negativi o non ancora accaduti, che nessun atto registra perché non c'è niente da registrare.

Con una sola eccezione strutturale: **chi parla sta leggendo ad alta voce un documento che esiste
ma sta fuori dal perimetro del corpus** — un verbale di maggio, i questionari di un ufficio, un
messaggio dell'azienda sanitaria. Lì il fatto ha tutte e tre le coordinate e resta comunque fuori
dagli atti, non perché sia debole ma perché il corpus finisce dove finisce giugno.

La prova sta in una sola frase di una commissione del Municipio V, dove lo stesso lettore, leggendo
lo stesso elenco ad alta voce, ha prodotto due righe di esito opposto: la risoluzione su viale
Palmiro Togliatti è «anche negli atti», perché l'atto è di giugno; gli stalli di via Antonio
Tempesta sono «non verificabile», perché il verbale che li contiene è di maggio. **Cambia solo il
confine del corpus.**

Quel 25%, quindi, non misura la debolezza del parlato: misura **dove passa il confine di ciò che
abbiamo raccolto**.

## 3. Che cosa gli atti registrano, e che cosa no

**Negli atti passa solo chi vince.** In una seduta dell'Assemblea Capitolina sono stati votati 138
ordini del giorno e solo 47 sono diventati atti: i respinti non lasciano traccia documentale. In
un'altra, le mozioni approvate diventano tutte atti e le due respinte — piazza Addis Abeba e Tor
Tre Teste — non esistono da nessuna parte. Chi ricostruisse il mese dai soli atti vedrebbe un
consiglio che approva e mai uno che respinge.

**Il verbale c'è ma è vuoto.** Per il Municipio I, 12 dei 23 verbali di commissione di giugno sono
«di sola presenza» o senza alcun contenuto verbalizzato, e di Commissione Trasparenza non esiste
alcun verbale in tutto il mese pur essendoci sedute registrate. Su un dossier discusso quattro
volte in otto giorni, tre verbali su quattro non dicono nulla: l'istruttoria sopravvive solo nelle
registrazioni.

**La parte più informativa è quella che per procedura non si registra.** In una commissione chi non
è formalmente convocato parla **solo a registrazione interrotta**, e quegli interventi «per motivi
di privacy non vengono inseriti». In un'altra le due sospensioni «a microfoni spenti» sono
esattamente i minuti in cui intervengono polizia locale e azienda sanitaria, gli unici soggetti
tecnici presenti. E in un Consiglio la registrazione è **interrotta su richiesta, in
applicazione dell'articolo 32 comma 3 del regolamento**: l'intervento del comitato e il voto finale
non esistono in video, e che l'ordine del giorno sia passato con 18 voti all'unanimità si sa solo
dall'atto. Sono tre meccanismi diversi — la prassi, il consenso mancante, la norma — che producono
lo stesso buco.

**Il verbale si scrive in diretta, decidendo a voce che cosa lasciarci** — due interventi saltati
esplicitamente, un capoverso rinegoziato per due minuti. E alla domanda se gli assessori correggano
mai i verbali che ricevono: «no, non lo fanno mai».

**A volte il verbale racconta una seduta diversa da quella avvenuta.** Una seduta fallisce per
ragioni acustiche — richieste di ripetere, un consigliere che esce perché non sente, la presidenza
che rinuncia — e il verbale descrive un sopralluogo regolare. In un'altra il parere è messo ai voti
prima che l'assessore risponda, e nessun atto registra la sequenza.

**Un atto che dispone il contrario di quanto deciso.** In un Consiglio l'atto depositato conteneva
nel dispositivo **la soluzione scartata dalla commissione**; l'emendamento è stato scritto in aula,
senza nemmeno le copie. L'atto pubblicato dice soltanto «così come emendata»: dell'errore resta
traccia **unicamente nella registrazione**.

**E qualche volta è la registrazione a correggere l'atto.** Una risoluzione proclama «Favorevoli:
16» ed elenca 22 nomi, con 22 presenti e zero contrari: in aula si dice «all'unanimità», e ha
ragione l'aula. Un verbale, per un errore di riconoscimento ottico, cita una deliberazione «n. 3»
dove l'aula dice correttamente «n. 35 del 16 marzo 2010».

**Come il residuo viene prodotto.** Non è che i verbali manchino: è che, quando ci sono,
**riassumono via esattamente ciò che ha valore**. Un verbale di commissione scuola segue la seduta
minuto per minuto e poi scrive «descrivendo poi tutte le caratteristiche dei 4 quadranti»: in quella
frase spariscono il 15% dei posti riservati a bambini con disabilità con operatore uno-a-uno, il
10% ai segnalati dai servizi sociali, i 485 posti e lo spostamento di un quartiere da un quadrante
all'altro. Una proposta sui cinghiali diventa «150 interventi, 200 mila euro» e perde tutto il
dispositivo — piano in trenta giorni, tavolo permanente, rendicontazione trimestrale in aula,
numero verde ventiquattr'ore al posto della sola casella di posta.

Il corollario chiude il ragionamento: **nelle sedute-monologo il verbale è quasi verbatim, e non
c'è nulla di nuovo.** La novità nasce dove c'è dialogo, e il dialogo è precisamente la parte che il
verbale comprime.

## 4. Che cosa si vede solo ascoltando

Questa parte resta fuori dal conteggio delle candidate **di proposito**, perché la soglia chiede un
luogo nominato. È materiale del rapporto, non della tabella.

- Un'Assemblea Capitolina con tre appelli falliti — 7 presenti su 49, poi 14, poi 20 — e il numero
  legale raggiunto al quarto dopo due ore e ventitré; la discussione sul piano degli arenili chiusa
  senza voto «visto l'orario»; dopo la pausa la seduta non riprende e la registrazione resta accesa
  su un'aula vuota per oltre un'ora.
- Consiglieri che votano chiedendo a votazione in corso di quale delibera si tratti; un parere
  votato da quattro consiglieri su otto con il presidente che mette a verbale «verificherò per mio
  scrupolo personale se quattro vanno bene»; «Votanti 24, favorevoli 25», corretto nella stessa
  frase.
- Un consiglio municipale che decade perché un gruppo resta in aula ma fuori dal numero legale; un
  Consiglio che non riesce ad aprirsi e **il cui verbale non esiste**: senza la registrazione,
  quella seduta non è mai avvenuta.
- La verbalizzante che dichiara in diretta di non riuscire a verbalizzare un'audizione di un'ora e
  un quarto perché non sente; una commissione che si chiude constatando che alla domanda su una
  scuola nessuno ha risposto, perché il dipartimento invitato non si è presentato.

## 5. Difetti delle fonti che una pipeline deve aspettarsi

**Negli atti.** Il 44–49% dei testi ha lo strato di testo incerto, e una parte non porta alcun
marcatore OCR: il marcatore non dice la verità sul testo, quindi **si giudica il testo**. Date
impossibili (`139.06.2026`, `44/06/2026`), timbri datati 2006, 2008, 2020, 2025 e 2028 su atti del
2026, una seduta aperta alle 14,00 e chiusa alle 11.33, «con tre (4) voti favorevoli», «unanimità
dei votanti» in presenza di astenuti. Un intero strato di testo cifrato con uno scorrimento di tre
lettere. Due atti identici con lo stesso protocollo pubblicati due volte.

**Nelle registrazioni.** Lo stesso toponimo compare fino a **dodici grafie nella stessa seduta**,
anche quando è l'oggetto della discussione; le sigle saltano quasi sempre; gli importi slittano di
tre ordini di grandezza. In due registrazioni la piattaforma **sostituisce parole con asterischi**.
Quattro item su 274 sono **due sedute pubblicate due volte**; altri cinque sono **spezzoni
consecutivi della stessa seduta** pubblicati come registrazioni distinte — due difetti diversi, che
si contano separatamente perché le ripubblicazioni condividono il testo e gli spezzoni no.

**Nel collegamento fra i due.** Il censimento abbina la registrazione al suo atto in modo
inaffidabile: su 78 abbinamenti dichiarati, 6 puntano a un atto di un altro Municipio e 8 a un atto
che non è di giugno; e per 63 registrazioni esiste un verbale univoco che il censimento **non**
dichiara. Tre lettori hanno recuperato a mano più di venti verbali identificandoli per ora di
apertura, ordine del giorno ed esiti di voto.

Il controllo esterno lo offre la fonte stessa, in un solo punto. **Diciassette verbali scrivono
dentro l'atto l'identificativo della registrazione** della seduta (`…/watch/vod/<identificativo>`):
quindici del Municipio XI, due del X. Sono gli unici casi in cui l'abbinamento lo dichiara chi ha
redatto l'atto invece di ricostruirlo noi. Sette di quei diciassette cadono su registrazioni del
nostro corpus, e su quei sette: il censimento **ne dichiara zero**; il nostro collegamento per
Municipio e data contiene il verbale giusto **sette volte su sette**, ed era già univoco in quattro.
Sono sette casi di un Municipio solo — troppo pochi per una percentuale, abbastanza per dire da che
parte sta il difetto.

Altri due Municipi scrivono un link che sembra la stessa cosa e non lo è: ventuno verbali del XV
rimandano al **catalogo** del Municipio, sempre con lo stesso identificativo, e due convocazioni del
IX al **canale della diretta**. Il primo dice che la registrazione esiste, non quale; il secondo
identifica l'organo, non la seduta. E uno dei due link del IX è **corrotto dall'OCR di un carattere**:
anche dove la fonte scrive l'identificativo, il testo può consegnarlo rotto. Quaranta atti su 1.983,
quattro Municipi su quindici: è una buona prassi da nominare, non un meccanismo su cui una pipeline
possa contare.

**Nella fonte, verso le persone.** Tre ordinanze pubblicate all'Albo Pretorio riportano nome, luogo
e data di nascita, codice fiscale, indirizzo con civico, scala, piano e interno, la condizione
personale e un procedimento di tutela di persone fragili. Un verbale di Commissione Pari
Opportunità nomina la persona audita, un familiare, il titolo del libro che identifica entrambi e
l'esito giudiziario a carico del familiare, dentro il racconto di una violenza domestica. **La
fonte non protegge le persone che nomina, e chi la riusa eredita il problema.**

## 6. La trascrizione automatica come strumento

Lo studio ha usato due origini, e sbagliano in modo diverso. Va saputo da chiunque ripeta questo
lavoro.

| | trascrizione della piattaforma | trascrizione a pagamento (`gpt-4o-mini-transcribe`) |
|---|---|---|
| grana del marcatore | 10 secondi | ~5 minuti (il modello non dà tempi interni) |
| confidenza dichiarata | reale, mediana 0,84–0,94 | assente |
| testo dentro blocchi duplicati | mediana 0,0%, mai sopra il 10% | mediana 0,5%, **39 registrazioni su 211 sopra il 10%, massimo 86,6%** |
| comportamento nei silenzi | **inventa parole** | lascia il blocco vuoto |

Sulle didascalie YouTube la confidenza per parola **vale zero su ogni parola**: è un campo
compilato a zero, non una misura, e chi lo usasse come filtro scarterebbe tutto.

Il modello a pagamento **entra in loop** sulle registrazioni lunghe e silenziose — in un caso una
frase ripetuta cento volte di fila, in un altro un blocco di 150 parole ripetuto undici volte, il
47% del file. Dove succede, il conteggio delle parole e le parole al minuto non misurano nulla.

**Costo effettivo misurato** (prova T1 su 2,12 ore, poi confermato sul corpus): 600 token audio al
minuto, costanti; **0,00261 $ al minuto**, il 13% sotto il listino a minuto. La spesa reale non è
leggibile senza una chiave di amministrazione: il dato è il consumo dichiarato dall'API, non la
fattura.

## 7. Incertezze dichiarate

1. Il campo `novita_rispetto_agli_atti` è stato definito tre volte: i lotti non sono confrontabili
   su quel campo e vanno pubblicati con la formulazione accanto. Il numero principale è quello
   meccanico, che non ne dipende. Quanto costi, si può misurare: i lotti letti mentre la regola
   cambiava si distendono su **71 punti** di `solo dal parlato`, quelli letti a regola ferma su
   **22**. Il metro è la misura meccanica, che del lettore non sa niente e porta la sola
   eterogeneità del materiale: nei primi la dispersione del lettore vale **1,46 volte** quella del
   materiale, nei secondi **0,74**. A regola ferma i lettori concordano più di quanto vari il
   materiale; a regola mobile no. Il costo non è dei lettori, è di chi ha cambiato il contratto in
   corsa.
2. Il confronto è contro «gli atti **più** le notizie già estratte dal Report 1»: eredita gli errori
   e le omissioni di quella pipeline.
3. L'unità di conteggio è la candidata, non il fatto: due lettori possono spezzare lo stesso fatto
   in modo diverso.
4. Un accostamento `dubbio` non prova una sovrapposizione: per questo il numero è un intervallo.
5. I dati di volume (parole, parole al minuto) sono inaffidabili dove la duplicazione supera il 10%.
6. Le misure sui silenzi valgono solo per le registrazioni con marcatore a 10 secondi: sulle altre
   un silenzio più corto di cinque minuti è invisibile.
7. Il materiale di riscontro è **congelato** in `report2/snapshot/`, così la novità non dipende dal
   giorno in cui un lotto è stato letto.

## 8. Decisioni editoriali in attesa dell'owner

**D5 — il numero civico di una sede pubblica.** Tre lettori hanno segnalato che il divieto di
civici, applicato alle sedi pubbliche, toglie precisione senza proteggere nessuno: due immobili
comunali contigui messi a bando diventano indistinguibili per indirizzo. Raccomandazione: tenere il
civico quando individua una sede o un immobile pubblico. Fino alla decisione i lettori applicano il
divieto senza eccezioni.

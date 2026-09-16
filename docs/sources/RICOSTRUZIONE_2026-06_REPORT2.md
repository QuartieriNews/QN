# Ricostruzione di giugno 2026 — Report 2: gli atti e le registrazioni

Bozza in lavorazione. Gli atti sono letti per intero, le registrazioni per poco più di metà; **i conteggi qui dentro sono quelli al 16 settembre e vanno rigenerati prima della
consegna** — `report1/build_db.py`, poi `report2/risposta.py`, `verifica_numeri_rapporto.py`,
`audit_toponimi.py`, `copertura_testi_atti.py`, `motivo_non_alta.py`, `convenzione_organo.py`.
I meccanismi descritti nei §3 e §4 ricorrono in tutti i lotti letti finora; quanto siano stabili
è però un'impressione di lettura e non una misura, e come tale va presa.

Perimetro: **8–28 giugno 2026**, come prescrive il metodo. Il Report 1 aveva letto 985 item
testuali e ne aveva ricavato 1.227 notizie candidate.

## 1. In breve

- Letti **1.983 atti amministrativi** — tutti quelli con data di repertorio fra l'8 e il 28 giugno,
  che è il perimetro dello studio — e censite **478 registrazioni di sedute** nella stessa finestra,
  97 dai canali YouTube dei Municipi e 381 da RomaTV. Di queste, 318 le abbiamo trascritte noi e 82
  portavano già la trascrizione della piattaforma. Alla data di questa bozza le registrazioni lette
  sono **305**.
- Gli atti letti sono in realtà **2.144**: i 1.983 della finestra più 161 fuori, letti per chiudere
  un buco che il perimetro lasciava aperto. I 1.983 danno **544 notizie candidate**, il **27,4%**;
  le registrazioni ne danno **1.185** finora.
- **Quel 27,4% non è però una proprietà degli atti.** Gli stessi documenti — le convocazioni — sono
  giudicati notiziabili nel **21,0%** dei casi da un gruppo di lettori e nel **44,2%** da un altro.
  Stessa regola scritta, il doppio di notizie. La differenza sta nel mandato: al secondo gruppo era
  stato chiesto esplicitamente quali fatti territoriali cercare. **La notiziabilità è una proprietà
  della coppia documento-lettore**, e chiunque rifaccia questo studio con un mandato scritto un po'
  diversamente troverà numeri diversi dagli stessi atti.
- La domanda del rapporto — *quanto aggiunge il parlato a ciò che è scritto* — ha una risposta, e
  arriva tardi: **circa l'84%** delle notizie che nascono in una seduta non sta in nessun atto.
  Il confronto meccanico da solo dava un intervallo largo, fra il 45% e il 92%; è un audit su
  campione della classe incerta — l'unico modo di sapere da che parte stesse — a restringerlo. Con
  la banda di confidenza di quell'audit la risposta sta **fra il 79,2% e l'87,0%**.
- **107 verbali su 2.668 atti, in sette Municipi su quindici, dichiarano dentro il proprio testo
  che il record completo della seduta non è l'atto ma la registrazione** — con quattro formule di
  forza diversa, dalla più netta («la videoregistrazione sostituisce la trascrizione degli
  interventi», 21 atti del Municipio II) al semplice rinvio al portale. Non è una tesi nostra: è
  l'amministrazione che lo scrive. È il fatto da cui parte questo rapporto, non la causa di tutto
  ciò che segue.

## 2. La risposta, e perché ci è voluto un audit per averla

Il campo che i lettori compilano riga per riga (`novita_rispetto_agli_atti`) è un giudizio, e nel
corso dello studio è stato definito **tre volte in modo diverso** — due delle quali per errori miei,
corretti e dichiarati. Non è quindi una serie omogenea, e non può essere il numero principale.

Il numero principale è meccanico: ogni candidata che viene dal parlato è confrontata, con la stessa
deduplicazione usata per tutto il corpus, contro **tutte le righe che vengono da fonti scritte**.
Tre esiti:

| | |
|---|---|
| **S** — nessun gemello fra le righe scritte | 528 |
| **U** — nessun duplicato, ma almeno un accostamento dubbio | 564 |
| **D** — almeno un duplicato certo | 93 |

Da cui l'intervallo grezzo **[44,6% , 92,2%]**: largo quarantotto punti, cioè una risposta che
non risponde. E fino all'audit davamo per buono che il valore vero stesse in basso.

**Sta in alto, e lo si sa solo dopo averlo misurato — tre volte.** Due lettori, indipendentemente,
hanno giudicato a mano quaranta candidate ciascuno della classe incerta, aprendo il testo integrale
di ogni documento accostato: **6 su 40 (15,0%)** il primo, **9 su 40 (22,5%)** il secondo. Gli
intervalli si sovrappongono largamente e la differenza non è significativa. Poi un difetto nostro
(§7 punto 15) ci ha costretti a rifare il campione e a far **rigiudicare da un terzo lettore le 28
candidate incerte** che la prima volta erano state mostrate senza i loro accostamenti: ne ha trovate
gemelle vere 3 invece di 4. Sulla base congiunta, con il rigiudizio che sostituisce il giudizio dato
sul campione difettoso, **14 su 80 = 17,5%** delle candidate incerte ha davvero un gemello scritto.

Riportando quella proporzione, la novità reale è **83,8%**, banda 95% **[79,2% ; 87,0%]**. La
calcola `report2/risposta.py`, che legge i file dell'audit invece di ricevere il numero a mano.

I due giri hanno anche prodotto, per un difetto del generatore, venti coppie giudicate da entrambi:
**accordo 19 su 20**. L'unica divergenza è il caso limite per cui il criterio di giudizio era stato
riscritto.

Con una scoperta che vale quanto il numero: nel primo giro **tutti e sei i gemelli veri erano la
registrazione scritta della stessa seduta** — cinque verbali e una deliberazione —, nessuno una fonte
indipendente. La classe incerta non nascondeva notizie già pubblicate altrove: nascondeva, in un caso
su cinque o sei, il verbale della riunione stessa.

Da cui la scala:

- **30,6%** circa — nuove, con un toponimo che il lettore non ha marcato incerto. È il valore più
  conservativo che sappiamo calcolare, e **non viene dallo stesso programma degli altri due**: lo
  calcola `report2/audit_toponimi.py` scartando le righe che poggiano su un toponimo dichiarato
  dubbio. Regge all'obiezione sulla trascrizione, non a tutte: se la deduplicazione sbaglia a non
  accostare, anche questo numero è alto.
- **44,6%** — nuove, cioè senza alcun gemello scritto, toponimi incerti compresi.
- **92,2%** — limite superiore, se si contano come nuove anche quelle che hanno solo un
  accostamento dubbio.

**Contro che cosa sono misurati, detto con precisione.** Non contro i soli atti: contro **tutte le
righe che vengono da fonti scritte**, cioè i 1.983 atti con repertorio 8–28 giugno *più* le notizie
già estratte dalle fonti testuali del Report 1. Il nome del campo (`novita_rispetto_agli_atti`) dice
meno di quello che il numero misura, ed è un difetto di nome che va tenuto presente: una candidata
del parlato è «nuova» quando non ha gemelli **né negli atti né nel già raccolto**. Gli atti sono
quelli con data di repertorio fra l'8 e il 28 giugno, che è il perimetro dello studio. Gli altri 685
atti di giugno che abbiamo in archivio sono dell'1–7 e del 29–30: fuori finestra per costruzione,
non dimenticati.

C'è però un punto in cui il perimetro, definito sulla data di repertorio, **non coincide con il
perimetro dei fatti**, e lo abbiamo chiuso leggendo 161 atti in più. Per i verbali la data di
repertorio è la data della seduta, e allora il verbale di una seduta dell'8–28 giugno sta sempre
dentro. Per le **convocazioni** la data di
repertorio è quella del protocollo, che precede la seduta: la convocazione di una seduta dei primi
giorni della finestra, protocollata prima dell'8, **resta fuori**. È una conseguenza necessaria
della definizione; l'abbiamo chiusa leggendo quelle convocazioni, e tocca il collegamento fra
registrazione e atto, non il gemello scritto di una notizia.

Resta un limite che non si chiude e va dichiarato: **il verbale di una seduta di fine giugno
repertoriato a luglio non è nella raccolta.** Non è un problema di insieme di confronto — è un
documento che non abbiamo.

**Come questi numeri sono cambiati, perché conta più dei numeri.** Fino a ieri il confronto usava la
catena della deduplicazione, che — seguendo il metodo, che descrive un lavoro fatto a mano — *toglie*
una riga dai confronti appena questa ha trovato un gemello. Per contare quante notizie distinte
restano va bene. Per chiedere *se una cosa detta in aula sta scritta da qualche parte* no: 111
candidate del parlato avevano come unico gemello un'altra registrazione e non sono mai state
confrontate con un atto, e 537 righe scritte su 1.855 erano già uscite dal confronto. Entrambe le
cose fanno risultare nuovo ciò che non è stato guardato. Con il confronto esaustivo la novità certa
scende di **sette punti e mezzo**, che erano un difetto nostro.

Una scelta va dichiarata: il metodo confronta dentro i blocchi tematici, noi confrontiamo su tutto
il corpus. È una deviazione, e **abbassa** la novità di due punti (46,4% dentro i blocchi contro
44,6% su tutto). Diciamo entrambe le cifre invece di scegliere quella che ci comoda.

**Perché l'intervallo grezzo è così largo.** Perché **564 candidate su 1.185 — quasi metà del
corpus parlato — sono «dubbie»**: accostate a una riga scritta per data e luogo ma non per oggetto, e
quindi contate come nuove nel limite alto e come già scritte in quello basso. Da che parte stessero
davvero decideva se la risposta fosse vicina al 45% o al 92%, e la larghezza non era un'incertezza da
nascondere: era il fatto che nessuno le avesse guardate. È quello che i due audit hanno fatto.

**Una cosa che i due audit hanno trovato e che cambia come si legge la classe incerta.** Dei quaranta
accostamenti giudicati «fatti diversi», **diciassette nascono da verbali della stessa seduta che
registrano solo le presenze e rimandano alla registrazione**. Cioè: **il verbale della stessa seduta
non è di per sé una fonte scritta del fatto**, e contarlo come tale era il modo più frequente in cui
il confronto meccanico dichiarava «già scritto» qualcosa che scritto non era.

**Delle due incertezze che tenevano largo l'intervallo, una è stata chiusa e l'altra no, e tirano in
direzioni opposte.** Chiusa: le candidate «dubbie» sono in larga parte falsi accostamenti — l'82,5% —,
e questo porta la risposta vicino al limite alto. Aperta: il confronto fra righe **non vede** i fatti
sepolti dentro atti che ne raccontano altri, e questo tira in basso, fino a un tetto del 37,1% di
candidate date per nuove che nel testo di un atto vicino compaiono comunque. L'83,8% va quindi letto
come la risposta migliore che sappiamo dare **con la seconda incertezza ancora aperta e dichiarata**.

E resta vero che **il 31,2% delle notizie «certamente nuove» poggia su un toponimo che il lettore
stesso ha segnalato come dubbio**: la risposta dipende anche da quanto ci si fida di una trascrizione
automatica.

**Che cosa misura questo numero, detto una volta per tutte.** Misura la novità **territoriale**: un
fatto su un luogo nominato che non sta scritto. Non misura la novità politico-istituzionale — il
numero legale che salta, la seduta che decade, l'ufficio che non si presenta — che la soglia di
notiziabilità esclude per costruzione. Quella parte sta nel §4 e non è meno importante.

La soglia ha anche un effetto che va detto senza attenuarlo: **tratta allo stesso modo un regolamento
senza effetti e un obbligo con effetti diffusi**. Il parere su una proposta che imporrebbe il
defibrillatore a ogni esercizio di somministrazione di Roma sopra una certa superficie — discusso in
due Municipi, in uno dei quali la commissione arriva a chiedere il ritiro dell'atto — resta fuori dal
conteggio perché è «un regolamento cittadino senza luogo». Tre registrazioni su dodici, in un lotto,
escono con zero candidate per questo motivo, non perché in aula non sia successo niente.

**E una notizia nuova è meno verificabile di una confermata.** Il confronto va fatto **dentro il
parlato**, con gli stessi lettori e le stesse trascrizioni: fra le candidate che gli atti confermano
il **54,5%** è di qualità alta, fra quelle nuove il **18,2%**. Trentasei punti.

**Ma gran parte di quel divario la produciamo noi, ed è stato misurato.** La nostra scala assegna
`alta` solo a un fatto *datato*; il parlato d'aula dice «l'anno scorso», «da vent'anni», «tre
settimane fa». Contato riga per riga su tutte le candidate che dichiarano il motivo — 233 —, **121 mancano l'alta
esclusivamente per la data**: sono compiute e localizzate, il 52% di quelle che non ci arrivano. E
**centodue di quelle centoventuno, l'84%, sono notizie nuove**. Su uno dei lotti, se la data non
fosse richiesta, le nuove passerebbero dal 16,7% al 76,7% di qualità alta, **superando le
confermate**.

Il motivo è che a datare un fatto, in aula, è quasi sempre **l'atto che qualcuno sta leggendo**: il
lettore dichiara di aver preso le date dal verbale, non dall'audio. Il requisito «datato» funziona
quindi come **un test sull'esistenza dell'atto travestito da test sul fatto**.

Un lettore l'ha messo alla prova nel modo che serviva, cioè guardando le eccezioni: nel suo lotto le
cinque candidate bloccate dalla data che **non** erano nuove venivano tutte dalle due sole sedute il
cui verbale riporta davvero la discussione. Altri due lotti hanno ripetuto il controllo e l'hanno
**corretto**: non conta che esista un verbale, conta che esista **un documento che porti il merito** —
può essere l'atto letto ad alta voce in aula, o il verbale di un'altra seduta. Con quella
formulazione le eccezioni si riducono a una su tredici.

**Il controllo speculare, invece, si rompe, ed è la cosa più istruttiva del capitolo.** Doveva dire
che le candidate nuove bloccate dalla data vengono sempre da verbali assenti o vuoti; un lotto ne ha
trovate **due su cinque** che vengono da sedute il cui verbale **esiste ed è pieno** — solo, è
selettivo. Il caso più netto non entra nemmeno nel conteggio, perché ha superato la soglia di
qualità: il cancello divelto del cantiere di un impianto è «solo dal parlato», e il verbale di quella
seduta, letto e approvato in aula, non ne fa parola. Quindi la distinzione utile non è fra verbale
che c'è e verbale che manca, ma fra tre casi: **verbale assente, verbale vuoto, e verbale che ha
scelto di non scrivere**. È la stessa selezione editoriale che governa le cifre (§3), vista da un
altro lato.

Resta un controesempio che va detto, perché è il caso in cui la regola dovrebbe funzionare meglio:
una seduta il cui verbale esiste ed è fedele — riporta perfino gli orari al minuto — e le cui tre
candidate sono tutte «solo dal parlato». Un verbale può essere accurato su tutto tranne che sul
merito.

Resta un divario vero sotto quello artificiale, e va detto: delle altre candidate che non arrivano
ad alta, la maggior parte manca perché il fatto è **annunciato e non compiuto**, o perché il toponimo
è storpiato. **Il parlato d'aula annuncia più di quanto certifichi** — ma molto meno di quanto il
18,2% lasciasse credere.

Il perché è un effetto di selezione, e non riguarda la qualità del parlato. Un fatto compiuto,
datato e localizzato **tende per costruzione a generare un atto**; e appena lo genera esce dalla
colonna «solo dal parlato». Quello che resta nel parlato è allora, per definizione, il **residuo**:
annunci senza data, proposte non deliberate, lavori fermi da mesi, assenze, risposte mancate —
fatti negativi o non ancora accaduti, che nessun atto registra perché non c'è niente da registrare.

Con una sola eccezione strutturale: **chi parla sta leggendo ad alta voce un documento che esiste
ma sta fuori dal perimetro del corpus** — un verbale di maggio, i questionari di un ufficio, un
messaggio dell'azienda sanitaria. Lì il fatto ha tutte e tre le coordinate e resta comunque fuori
dagli atti, non perché sia debole ma perché il corpus finisce dove finisce giugno.

L'esempio più netto — uno solo, quindi illustrativo e non probante — è una frase di una commissione
del Municipio V, dove lo stesso lettore, leggendo lo stesso elenco ad alta voce, ha prodotto due
righe di esito opposto: la risoluzione su viale
Palmiro Togliatti è «anche negli atti», perché l'atto è di giugno; gli stalli di via Antonio
Tempesta sono «non verificabile», perché il verbale che li contiene è di maggio. **Cambia solo il
confine del corpus.**

Se il meccanismo è giusto, quel 18,2% non misura la debolezza del parlato ma **dove passa il confine
di ciò che abbiamo raccolto**. È un'ipotesi coerente con i casi letti, non una conclusione
dimostrata: per dimostrarla servirebbe scomporre il divario nelle sue cause, e ne abbiamo scomposta
una sola — la data, che ne spiega quasi metà.

## 3. Che cosa gli atti registrano, e che cosa no

**Negli atti passa solo chi vince.** In una seduta dell'Assemblea Capitolina sono stati **presentati
138 ordini del giorno** su una sola proposta, otto sono stati dichiarati inammissibili, la seduta è
stata tolta senza esaurirli, e **47 sono diventati atti**: i respinti non lasciano traccia
documentale. In
un'altra, le mozioni approvate diventano tutte atti e le due respinte — piazza Addis Abeba e Tor
Tre Teste — non esistono da nessuna parte. Chi ricostruisse il mese dai soli atti vedrebbe un
consiglio che approva e mai uno che respinge.

**A volte il verbale non c'è perché l'organo non lo approva da anni.** Un presidente di Consiglio
municipale dice in aula che i verbali del proprio Consiglio **non vengono approvati dal 2021**: ne
porta venti per seduta e quel giorno approva senza osservazioni, in venti secondi, i numeri da 1 a 20
del **2022**. Spiega da solo perché nel corpus di giugno non esista un verbale di Consiglio di quel
Municipio: non è un buco della nostra raccolta, è un arretrato di quattro anni. Tre Consigli
municipali su tre, in un lotto, non hanno verbale nel corpus, e la sola traccia sono gli atti
approvati, che al posto della discussione portano `(omissis)`.

**Il verbale c'è ma è vuoto.** Per il Municipio I, **17 dei 23** verbali di commissione di giugno sono
«di sola presenza» o senza alcun contenuto verbalizzato, e di Commissione Trasparenza non esiste
alcun verbale in tutto il mese pur essendoci sedute registrate. Su un dossier discusso quattro
volte in otto giorni, tre verbali su quattro non dicono nulla: l'istruttoria sopravvive solo nelle
registrazioni.

**E c'è una parte che non viene registrata quasi per definizione: quella del pubblico.** Nelle due
sedute di un lotto in cui interviene il pubblico, l'intervento del pubblico non esiste in nessuna
forma: nella prima la registrazione continua ma la trascrizione è **vuota per 4 minuti e 21 secondi**,
perché i microfoni d'aula sono spenti; nella seconda chi presiede dice «interrompiamo la registrazione
per consentire un intervento da parte dei cittadini» e **il file finisce lì** — e per quella seduta
un verbale non esiste. In un terzo caso i cittadini e un comitato di quartiere ai quali viene negata
la parola, e la sospensione che ne segue, nel verbale diventano «chiarimenti inerenti lo svolgimento
della seduta».

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

**E non servono due documenti perché un'ammissione sparisca: basta il verbale della stessa seduta.**
In aula l'assessorato dichiara che la soprintendenza aveva chiesto di **bloccare l'iter** di una
variante e che il parere prescrittivo nelle aree tutelate era stato **negato**; il verbale di quella
seduta scrive che l'incontro «ha consentito di chiarire i rispettivi ambiti di competenza».

**A volte la smentita attraversa il tempo, e riguarda una notizia che avevamo già pubblicato.** L'8 giugno una commissione dichiara
«concluso il giro degli sfalci nei parchi» — è una delle notizie che il Report 1 aveva già estratto —
e il 22 giugno, nella stessa commissione, un commissario parla di «enorme ritardo, una giungla nei
parchi». Senza la registrazione della seconda seduta, la prima resterebbe l'ultima parola.

**Il caso generale, però, è che le due fonti non si completino: si smentiscano.** In dodici
registrazioni lette di seguito ce ne sono quattro casi. Il verbale di una commissione scuola scrive che il trasferimento
temporaneo di alcune sezioni di una materna è stato revocato per «criticità organizzative, in
particolare legate alla **mensa**»; due giorni dopo, in commissione trasparenza, l'assessora dice due
volte che non si tratta di ragioni tecniche e che **«la mensa non c'entra niente»** — il trasferimento
è saltato perché la comunità scolastica ospitante lo ha rifiutato. La versione scritta è la versione
presentabile. Nella stessa seduta la direzione tecnica dichiara che «oggi siamo ancora a 17 e non
abbiamo in mano la determina di subappalto»: quella determina porta **la data di quel giorno stesso**.
La stessa determina data la richiesta di subappalto al 2024 con un protocollo del 2026, e qui è la
registrazione ad avere ragione. E il verbale di una commissione delle 10.35 racconta al passato che
«in commissione commercio si è votato il documento»: quella commissione si riunisce **un'ora più
tardi** e il parere non lo esprime — né quel giorno né dopo.

Il caso inverso più semplice è che la registrazione non ci sia, pur essendoci il file: in una seduta
di trentadue minuti la presidenza «lascia in pausa» e **venti minuti corrono muti** — il punto
sostanziale, l'elenco delle opere giubilari, esiste solo nei verbali. E in un'altra un voto proclamato
**non torna né con le chiamate né con sé stesso**, e non esiste né verbale né atto per riscontrarlo:
il lettore l'ha lasciato non riscontrato e non l'ha usato, che è l'unica cosa corretta da fare.

Il caso inverso più netto è di un altro lotto, e ribalta la gerarchia: un verbale scrive che a
un'ora precisa **la registrazione audio fu sospesa** per mancato consenso della funzionaria tecnica
che stava per rispondere. Tutte le risposte di quel passaggio — le interlocuzioni con il gestore
idrico, l'assenza di cedimenti, la verifica di allacci non autorizzati, il passaggio della
manutenzione a una società in house — **esistono solo sulla carta**. È il meccanismo del consenso
mancante visto nella sua forma più netta: non microfoni spenti in una pausa, ma la registrazione
fermata su richiesta di chi sta per rispondere — e lì il verbale non è una copia più povera, è
l'unica.

Nel senso opposto, in quelle stesse dodici, un caso solo: un verbale contiene un fatto che l'audio
non ha («i terreni vanno ancora acquisiti»), e insieme **anonimizza** — dove la registrazione nomina
l'agenzia capitolina che ha redatto il progetto, il verbale scrive «professionisti».

**Il documento che viaggia può essere quello sbagliato.** Di uno stesso sopralluogo esistono due
documenti: una risoluzione scrive che la società ha versato il materiale prima della chiusura del
cantiere e senza dispositivi antiodore, «per non mancare le scadenze del PNRR»; il verbale dello
stesso sopralluogo — **già approvato** — scrive «si constata» dove il fatto era solo dichiarato, e
omette entrambe le ammissioni. La commissione se ne accorge leggendolo in diretta, e un commissario
dichiara di averlo votato senza averlo letto. Quel verbale era destinato agli enti esterni:
**quello che esce dal Municipio è la versione senza le ammissioni**.

E in un terzo sopralluogo l'omissione si sente accadere: un'ammissione tecnica del progettista fatta
sul posto non arriva nel verbale, e nella registrazione **si sente la commissione decidere di non
scriverla**. Specularmente, un verbale può riportare tutte le cifre del merito **e sbagliarle tutte**,
perché è fedele a chi parlava e non all'atto: l'accuratezza del verbale non è una proprietà unica,
dipende da che cosa il verbalizzante considera la fonte.

Succede, non è una legge: in un altro sopralluogo i due documenti **conservano entrambi
l'ammissione**, e la versione approvata aggiunge dettagli — e aggiunge anche un divieto di riprese e
fotografie concordato con la società, che nella bozza letta in aula non c'era. Il rischio non è che
la versione ufficiale ometta sempre: è che ometta **senza che si possa saperlo**, se non
confrontandola con la registrazione.

**Nelle dodici successive il rapporto si rovescia: due volte ha ragione il parlato, quattro la
carta.** Non è una smentita del capoverso precedente, è la sua condizione: in quel secondo gruppo
**nove item su dodici hanno un verbale**, e dove il verbale c'è è lui a correggere — il toponimo
storpiato dalla trascrizione, la risoluzione che in aula diventa «la scorsa settimana» e ha due
settimane, i conteggi di voto. Il caso più netto va nella stessa direzione: su un parco un Consiglio
dichiara in aula di non avere il progetto e di volerlo chiedere «da domani», mentre una determina di
sei giorni prima **ha già aperto il cantiere** con inizio il giorno stesso della seduta. La carta era
in anticipo sull'organo che avrebbe dovuto saperlo.

**Come il residuo viene prodotto.** Non è che i verbali manchino: è che, nei casi letti, quando
ci sono **riassumono via le cifre e i dispositivi**. Non è una misura sistematica — nessuno ha
confrontato verbale e registrazione riga per riga su un campione — ma il modo in cui accade è
sempre lo stesso. Un verbale di commissione scuola segue la seduta
minuto per minuto e poi scrive «descrivendo poi tutte le caratteristiche dei 4 quadranti»: in quella
frase spariscono il 15% dei posti riservati a bambini con disabilità con operatore uno-a-uno, il
10% ai segnalati dai servizi sociali, i 485 posti e lo spostamento di un quartiere da un quadrante
all'altro. Una proposta sui cinghiali diventa «150 interventi, 200 mila euro» e perde tutto il
dispositivo — piano in trenta giorni, tavolo permanente, rendicontazione trimestrale in aula,
numero verde ventiquattr'ore al posto della sola casella di posta.

**Quale cifra sopravvive in un verbale, e quale no.** Tre letture indipendenti hanno proposto tre
spiegazioni, e le prime due sono state smentite contando. Non è la forma: l'unico verbale a elenco
puntato del campione conserva **quattro cifre su quattro**, mentre i verbali in prosa estesa vanno
dallo 0% al 50%. Non è che il verbale registri chi ha parlato: lo fanno tutti, e fra loro c'è
cinquanta punti di differenza. Quella che regge al conteggio è la terza:

> sopravvive la cifra che è **parte dell'atto o della procedura che il verbale ha il compito di
> certificare**; muore la cifra usata come argomento, contesto o colore.

Due letture successive l'hanno contata su altri verbali e l'hanno confermata: **72 cifre pronunciate
e 29 sopravvissute in un caso, circa 80 e 47 nell'altro**, e delle morte quasi tutte erano argomento
o contesto — 137 aziende e settemila addetti, otto milioni nel 2016, il 35% di un milione e
settecentomila tonnellate, 9″99 sui cento metri. Il caso che chiude la questione: un assessore legge dieci statistiche sull'arresto
cardiaco — 60.000 casi l'anno, 58%, 7,5% europeo — dicendo «tutto questo è presente nell'atto che
stiamo discutendo». Nel documento **non ce n'è nessuna**. Sopravvivono tutte e sole le cifre che
*sono* la norma: 250 metri quadri, 350 dispositivi, 16.500 esercizi, 31 dicembre 2026.

La formulazione che regge su tutti i conteggi è quindi più stretta: **sopravvive la cifra di cui quel
verbale è il documento probatorio**.

**È una tendenza forte, non una legge, e i controesempi sono istruttivi.** Una lettura successiva ne
ha trovati due nello stesso verbale: cinque frazioni di suolo concedibile che erano **il dispositivo
dell'atto in votazione** e che il verbale non riporta affatto; e uno stesso numero — il 100% di una
zona — che **muore come norma e sopravvive dentro l'obiezione di una consigliera**, cioè esattamente
al contrario di come la regola prevede. Quella sopravvivenza per la via sbagliata è anche l'unico
modo per capire che una cifra storpiata dalla trascrizione non era un errore.

**Due controesempi successivi spostano la spiegazione, e la rendono più semplice.** In un verso: una
mozione scrive nelle premesse «L'amministrazione ne ha individuati **175**» — cifra di puro contesto,
ripresa da una pagina web, di cui quella mozione non è in nessun senso il documento probatorio — e la
cifra **sopravvive intatta**, mentre «di fatto a terra ce ne sono una trentina», detto nello stesso
intervento, muore. Nell'altro verso: il mandato dell'**8 giugno 2026** di un dipartimento capitolino
a un'agenzia comunale per lo studio di fattibilità su un incrocio dove si continua a morire — atto
amministrativo datato, con nota di trasmissione, esattamente il tipo di cifra che la regola dà per
salva — **non sopravvive**: il verbale liquida l'intervento con «L'Assessore interviene per la
replica», e di quel mandato non c'è traccia né nei 1.983 atti né nei 2.668 testi integrali.

La discriminante, allora, **non è probatoria: è redazionale**. Sopravvive quello che è già scritto
dentro un atto che il verbale trascrive; muore quello che sta nella discussione, qualunque ne sia lo
statuto. Una cifra probatoria pronunciata in dibattito muore come le altre — ed è una formulazione
più utile, perché dice dove cercare quello che manca: non fra le cifre deboli, ma **nel dibattito**.

Due lotti successivi l'hanno stretta ancora, e nella stessa direzione. Sopravvive **ciò che il
verbale considera il proprio oggetto**: in una commissione che dà un parere l'oggetto è l'atto, e le
cifre del merito muoiono anche quando sono scritte dentro altri atti; in un **sopralluogo** l'oggetto
è quello che si è visto, e allora le cifre dette sul posto sopravvivono tutte, nessuna delle quali
sta in un documento precedente. Da lì anche i due controesempi che la formulazione precedente non
spiegava: muoiono cifre che negli atti ci sono — i documenti pervenuti, le osservazioni accolte, le
soglie di un tessuto urbanistico — e sopravvive una cifra **nata nella discussione**, una premialità
ipotizzata lì per lì, perché era diventata il punto su cui si decideva. E quando l'aula, invece di
riassumere, **legge l'atto ad alta voce**, le cifre passano tutte intere. La perdita non è nella
prova: è nella redazione del riassunto.

**Sopra l'oggetto della seduta c'è un livello che conta di più: come quell'organo verbalizza.**
Un lettore l'ha notato confrontando organi diversi — ce ne sono di quasi stenografici e ce ne sono i
cui verbali dichiarano che «la videoregistrazione sostituisce la trascrizione degli interventi» —, e
si può controllare sui dati: **dove i verbali pesano di più sugli atti di un Municipio, la novità del
parlato è più bassa**. La correlazione fra le due quote, sui dieci Municipi con abbastanza materiale,
è **−0,60** sulla misura meccanica e **−0,50** sul giudizio dei lettori. Dieci Municipi non sono una
dimostrazione, e c'è un limite che un lettore ha visto prima di me: **densità non è fedeltà**. Il
Municipio più verboso del suo lotto è anche quello che perde più cifre, e i verbali **a elenco**
conservano i dati meglio di quelli in prosa, che riscrivono. La quota di verbali misura quanto un
organo verbalizza, non quanto bene; ma il segno è quello atteso su due misure indipendenti, e dice una cosa scomoda: **una parte di quello che chiamiamo novità è la
convenzione di verbalizzazione dell'organo che stiamo ascoltando.** L'oggetto della seduta spiega le
differenze *dentro* uno stesso organo; la convenzione spiega quelle *fra* organi.
(`report2/convenzione_organo.py`.)

C'è poi una perdita che nessuna delle due direzioni prevedeva: **i verbali cancellano i luoghi**. In
una commissione sei verbali arretrati vengono letti a voce con il loro oggetto — una scala pubblica,
un parco regionale, una villa comunale, una stazione — e nel verbale di quella seduta diventano sei
date e sei numeri di protocollo. **Quattro di quei luoghi esistono solo nell'audio.** Per uno studio
che misura la novità territoriale è il caso peggiore: non si perde un dettaglio, si perde
esattamente la coordinata che rende un fatto un fatto locale.

Un secondo lettore, su un altro Municipio, ha trovato la stessa cosa nella forma più netta: un
verbale pieno — nomi, orari al minuto, il voto 6-0 — riduce il fatto territoriale più grosso della
seduta, gli sfalci fermi con **cinque strade nominate a voce** e la richiesta di convocare
l'assessore, a «uno scambio d'informazioni sui luoghi ove è necessario provvedere allo sfalcio».
I cinque toponimi spariscono tutti. Nello stesso lotto, i cittadini ai quali viene negata la parola e
la sospensione che ne segue diventano «chiarimenti inerenti lo svolgimento della seduta». **Il
verbale che ha scelto di non scrivere si è presentato in tutte e quattro le sedute del lotto che un
verbale ce l'avevano**: non è il caso raro, è il caso normale.

L'obiezione ovvia è che decida il redattore, cioè che sia una questione di persone e di uffici. È
stata controllata e non regge: **lo stesso ufficio, nello stesso mese**, conserva importo, numero di
partecipanti e fascia d'età di un progetto già finanziato, e di un'iniziativa civica senza atto non
registra **nessuna** cifra — né i firmatari, né le due date. Non cambia chi scrive: cambia se la
cifra esista già scritta da qualche altra parte.

**E il verbale non si limita a perdere: a volte aggiunge, e a volte ha ragione lui.** Ha una fonte
propria — i documenti d'ufficio — e la usa contro il parlato. Porta l'importo esatto di un debito,
`17.182,05`, dove in aula si sentono 21.000, 17.000, 2.182 e 1.224,30. Corregge l'oratore contro la
sua stessa voce: «oltre sei mesi dalla chiusura» diventa «a più di cinque mesi», e cinque è il numero
giusto. Porta gli orari di entrata e uscita al minuto, che **nella registrazione non esistono**
perché nessuno li annuncia.

E in un caso corregge l'aula su un fatto: una consigliera **annuncia il proprio voto contrario**,
ma nel verbale i contrari sono due e lei non c'è, perché aveva lasciato la seduta. **Chi si fidasse
del solo parlato sbaglierebbe il conteggio.** È il contrappeso a tutto questo capitolo, e va scritto
con la stessa forza: la registrazione è più completa, l'atto è più esatto.

Il fatto grosso su cui tutte le letture concordano: **dove il verbale è pieno il video aggiunge
poco, dove è di sole presenze aggiunge quasi tutto** — notizie solo dal parlato allo 0% con verbale
pieno, 50% con verbale di sola presenza, 71% con verbale assente.

**E che cosa il Report 2 aggiunge a quello che il Report 1 aveva già.** Non solo notizie nuove:
anche pezzi mancanti di notizie vecchie. **316 righe di questo rapporto completano o correggono una
riga del precedente** — e il campo che aggiungono più spesso non è il luogo, è **il tipo dell'atto e la data del fatto**. Un avviso municipale dice che una cosa succederà; l'atto o la
seduta dicono *quando* e *con quale strumento*. È il contributo che si perderebbe del tutto in una
vista che scarta i duplicati.

## 4. Che cosa si vede solo ascoltando

Questa parte resta fuori dal conteggio delle candidate **di proposito**, perché la soglia chiede un
luogo nominato. È materiale del rapporto, non della tabella.

- Un'Assemblea Capitolina con due appelli falliti — 7 presenti su 48, poi 18 — e il numero
  legale raggiunto al terzo, con 26, dopo due ore e ventitré; la discussione sul piano degli arenili chiusa
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
- Un Consiglio in cui il numero legale salta sul quarto punto — dieci votanti, poi quattordici
  presenti — e gli atti che ne escono, mozione e ordine del giorno, portano **la data del giorno
  dopo**. Chi ha solo le carte vede due sedute; la registrazione mostra che è una sola, decaduta e
  ripresa.

## 5. Difetti delle fonti che una pipeline deve aspettarsi

**Negli atti.** Il 44–49% dei testi ha lo strato di testo incerto, e una parte non porta alcun
marcatore OCR: il marcatore non dice la verità sul testo, quindi **si giudica il testo**. Date
impossibili (`139.06.2026`, `44/06/2026`), timbri datati 2006, 2008, 2020, 2025 e 2028 su atti del
2026, una seduta aperta alle 14,00 e chiusa alle 11.33, «con tre (4) voti favorevoli», «unanimità
dei votanti» in presenza di astenuti. Un intero strato di testo cifrato con uno scorrimento di tre
lettere. Due atti identici con lo stesso protocollo pubblicati due volte.

**Nella pubblicazione delle registrazioni** — difetti di chi pubblica. Su 274 item censiti al
momento della misura, quattro sono **due sedute pubblicate due volte**; altri cinque sono **spezzoni
consecutivi della stessa seduta** pubblicati come registrazioni distinte. Sono due difetti diversi e
si contano separatamente, perché le ripubblicazioni condividono il testo e gli spezzoni no: una
misura che cerca testo condiviso vede i primi e **per costruzione** non vede i secondi.

Un terzo caso, trovato leggendo, non è nessuno dei due e nessuna misura automatica lo vedrebbe: due
item che il censimento dà come sedute distinte dello stesso giorno sono **la stessa seduta**, spezzata
perché a metà è migrata su un'altra piattaforma — stessi presenti, stesso guasto, apertura alle 10.11
nel primo e chiusura alle 11.02 nel secondo — e la data del censimento è sbagliata di un giorno: la
convocazione, protocollata il 18, convoca per il 19. Il primo item porta dodici minuti, il secondo i
quaranta dell'audizione. Una lacuna reale, in una colonna che per quegli item è vuota.

**Nella trascrizione, e qui la distinzione conta.** Una parte delle registrazioni porta la
trascrizione automatica *della piattaforma*, che è un difetto della fonte; per le altre la
trascrizione **l'abbiamo fatta noi** con `gpt-4o-mini-transcribe`, e i suoi difetti sono nostri.
Non si somigliano:

| | trascrizione della piattaforma (fonte) | trascrizione nostra (pipeline) |
|---|---|---|
| blocchi di testo ripetuti, mediana | 0,0% | 0,5% |
| registrazioni sopra il 10% di testo duplicato | **0** | **39** |
| massimo | 1,7% | **86,6%** |
| parole inventate dentro i silenzi | sì | no |
| parole sostituite da asterischi | sì, 2 casi | no |
| silenzi lasciati vuoti | no | sì |

Il difetto più grave — un passaggio riscritto fino a quattro volte, in un caso il 67,9% di una
registrazione da 9.902 parole — **è del modello che abbiamo pagato noi**, non della fonte, e su
quelle registrazioni rende inutilizzabile il conteggio delle parole. Lo storpiamento dei nomi
propri invece è di entrambe: lo stesso toponimo compare fino a **dodici grafie nella stessa
seduta**, anche quando è l'oggetto della discussione; le sigle saltano quasi sempre; gli importi
slittano di tre ordini di grandezza.

**Un altro che è nostro: il foglio di riscontro riassume, e un riassunto contiene numeri.** Un
lettore ha notato che il nostro `confronto_atti.csv` descrive un atto come «parere favorevole con
**nove** emendamenti», mentre in aula e nell'allegato del verbale gliene risultano **undici**.
Contandoli sul testo integrale dell'atto ne vengono nove o dieci secondo dove si taglia un
emendamento dall'altro. Nessuno dei tre conteggi è sbagliato per sciatteria: **contare gli
emendamenti è già un'interpretazione**, e un numero dentro un riassunto non è un dato solo perché è
scritto in una tabella. Vale per il nostro foglio come per i verbali di cui parla questo capitolo.

**Un difetto che è nostro, non della fonte.** La mascheratura automatica dei nomi di persona ha
colpito **un toponimo**: l'oggetto di una mozione votata all'unanimità esce come `spostamento
mercato *********`, e solo l'atto di Consiglio dice che quegli asterischi sono il nome di un
quartiere. Senza il riscontro documentale quella candidata sarebbe stata scartata per «luogo
mancante»: la tutela della riservatezza, applicata a macchina, cancella anche ciò che riservato non
è. Dalla parte della fonte, il caso simmetrico: un verbale sottoscritto data la propria seduta a
«martedì 09 di maggio», e il 9 maggio 2026 è un sabato.

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
Sono sette casi di un Municipio solo: troppo pochi per una percentuale e per una conclusione
generale. Quello che si può dire è solo questo: **in quei sette casi** il censimento fallisce sette
volte su sette e il collegamento per Municipio e data riesce sette volte su sette.

Altri due Municipi scrivono un link che sembra la stessa cosa e non lo è: ventuno verbali del XV
rimandano al **catalogo** del Municipio, sempre con lo stesso identificativo, e due convocazioni del
IX al **canale della diretta**. Il primo dice che la registrazione esiste, non quale; il secondo
identifica l'organo, non la seduta. E uno dei due link del IX è **corrotto dall'OCR di un carattere**:
anche dove la fonte scrive l'identificativo, il testo può consegnarlo rotto. Quaranta atti su 1.983,
quattro Municipi su quindici: è una buona prassi da nominare, non un meccanismo su cui una pipeline
possa contare.

**Il verbale sbaglia anche le cose che dovrebbe saper fare.** Su sei verbali confrontati con la
registrazione, **due sbagliano l'orario di chiusura** — 13:47 contro le 10.07 reali, 14:14 contro le
11.05 — cioè attribuiscono ore di lavori a sedute di mezz'ora. Chi misurasse la durata delle sedute
sui verbali otterrebbe numeri privi di senso. Ma non è generale: su altri sette verbali, di un altro
Municipio, gli orari di chiusura sono **giusti sette volte su sette**. Anche qui la variabile è
l'organo, non «il verbale».

Un lettore ha segnalato tre verbali di sedute diverse con lo stesso identico link alla registrazione;
**verificato sui 2.668 testi, non è così**: venti atti portano un identificativo di registrazione e
sono **tutti distinti**. La duplicazione che esiste davvero è quella già descritta sopra — i ventuno
verbali che rimandano al *catalogo* del Municipio —, ed è una cosa diversa.

Il boilerplate però esiste, e sta nel testo del verbale, non nel link: di una commissione congiunta
esistono due verbali, di due organi diversi, con due segretarie e protocolli a due mesi di distanza,
e il racconto del punto congiunto è **identico carattere per carattere**. Misurato: **1.786 caratteri
coincidenti in blocchi da quaranta in su, sei dei quali oltre i cento**, su verbali lunghi 3.338 e
4.014 caratteri. Più di metà di uno dei due è copiato dall'altro, o entrambi da una terza fonte.

Due casi dicono quanto costa, e nessuno dei due supera la soglia. A **0,061** — sotto il 10%, dove
nessuno andrebbe a guardare — una decina di righe duplicate dentro l'appello di voto **si portano via
il voto di una presidenza di commissione**, mentre la seduta si chiude dichiarando l'unanimità. E in
una seduta telematica due voti passano **in chat**, perché i microfoni non funzionano: lì una parte
del verbale reale non è nell'audio, e nessuna colonna lo segnala.

**Tre difetti diversi, e la nostra colonna ne vede uno solo.** La quota di testo duplicato intercetta
la ripetizione; non vede il **silenzio** (trentacinque minuti muti a quota 0,0, e una commissione che
fa 87 parole al minuto contro 120-133 perché scorre allegati in silenzio) e non vede la **linea che
cade** — passaggi di un assessore che semplicemente non arrivano, sei volte nella stessa seduta,
senza ripetizione, senza silenzio e senza lacuna dichiarata. Un lettore ha anche misurato **quanto
costa** un ciclo: dove il modello entra in loop il blocco raddoppia, e il parlato reale che sparisce
è pari al duplicato — 1.315 parole scritte dove ne erano state dette circa 600.

**La percentuale di testo duplicato non dice dove si perde.** Misurato su due registrazioni dello
stesso lotto: a **8,5%** di testo duplicato mancano cinque commi di un regolamento — la lettura
riprende dal quattordicesimo dopo essersi interrotta all'ottavo; a **44,8%** non manca niente,
perché il presidente legge lo stesso articolo due volte, nelle premesse e nel dispositivo. La soglia
che ci eravamo dati — non fidarsi dei conteggi sopra il 10% — dà quindi il verdetto giusto per il
motivo sbagliato e quello sbagliato nel caso più estremo. **Quello che va misurato è la perdita, non
la ripetizione**: cercare il punto di innesco e verificare se il testo riprende da dove si era
interrotto. Lo scriviamo come correzione per chi rifarà questo lavoro, non come qualcosa che abbiamo
già applicato.

**E un difetto della nostra trascrizione che non è rumore ma perdita.** Quando il modello entra in
ciclo non aggiunge testo inutile: **riscrive lo stesso passaggio al posto di quello che si stava
dicendo**. In una registrazione sparisce così l'illustrazione dell'atto da parte della proponente,
in un'altra l'inizio dell'intervento critico. La percentuale di testo duplicato dice *quanto*, non
*che cosa* è andato perduto — e per saperlo bisogna andare al punto di innesco e guardare.

**E un limite del nostro metodo, non della fonte.** Le regole di riservatezza si applicano fonte per
fonte, e un fatto escluso da un ramo **rientra dall'altro**: un lettore delle registrazioni aveva
scartato per intero la vicenda personale di uno studente minorenne, e la stessa seduta, letta come
atto, aveva portato il nome della scuola in una nostra riga — non la vicenda, ma il nome. L'abbiamo
tolto. Vale come avvertimento generale: **proteggere le persone ramo per ramo non protegge
nessuno**, e in una pipeline che incrocia fonti il controllo va fatto sull'uscita, non sull'ingresso.

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

**Il difetto peggiore, però, non è perdere: è inventare.** In un item la trascrizione riporta **nove
«Favorevole» di fila** dove l'aula ha votato 2 favorevoli, 2 contrari e 2 astenuti, e il parere è
stato **respinto**: chi leggesse la sola trascrizione registrerebbe l'opposto di quello che è
successo, senza alcun segnale che qualcosa non torna. È il motivo per cui in questo studio un voto va
sempre riscontrato sul verbale o sull'atto prima di essere scritto — e per cui un conteggio di voti
preso da una trascrizione automatica, in qualunque pipeline, non è un dato.

Sulle didascalie YouTube la confidenza per parola **vale zero su ogni parola**: è un campo
compilato a zero, non una misura, e chi lo usasse come filtro scarterebbe tutto.

Il modello a pagamento **entra in loop** sulle registrazioni lunghe e silenziose — in un caso una
frase ripetuta cento volte di fila, in un altro un blocco di 150 parole ripetuto undici volte, il
47% del file. Dove succede, il conteggio delle parole e le parole al minuto non misurano nulla.

**Sbaglia anche i numeri, senza lasciare il segno che li ha sbagliati.** La stessa soglia della stessa
proposta capitolina, nello stesso Municipio, la stessa mattina, esce **«150 metri quadri»** in una
commissione delle 10.35 e **«250 metri quadri»** in un'altra delle 11.34; gli atti danno 250, con tre
riscontri indipendenti. Nessuna delle due trascrizioni è marcata come incerta — il modello a
pagamento non dichiara confidenza — e quindi, **senza un riscontro esterno, la cifra sbagliata è
indistinguibile da quella giusta**. È il motivo per cui in questo studio le cifre pronunciate si
prendono dall'atto quando l'atto c'è.

**Costo effettivo misurato** (prova T1 su 2,12 ore, poi confermato sul corpus): 600 token audio al
minuto, costanti; **0,00261 $ al minuto**, il 13% sotto il listino a minuto. La spesa reale non è
leggibile senza una chiave di amministrazione: il dato è il consumo dichiarato dall'API, non la
fattura.

## 7. Incertezze dichiarate

1. Il campo `novita_rispetto_agli_atti` è stato definito tre volte: i lotti non sono confrontabili
   su quel campo e vanno pubblicati con la formulazione accanto. Il numero principale è quello
   meccanico, che non ne dipende. Quanto costi si può stimare, con una cautela. `report2/varianza_lettori.py` divide i lotti in
   due gruppi — le registrazioni YouTube, lette mentre la definizione cambiava, e quelle RomaTV,
   lette a definizione ferma — e misura per ciascuno quanto si distende il giudizio del lettore
   (71 punti contro 22) rispetto a quanto si distende la misura meccanica, che del lettore non sa
   niente (49 contro 30). Il rapporto fra le due dispersioni è **1,46** nel primo gruppo e **0,74**
   nel secondo. **La cautela è che i due gruppi non differiscono solo per la regola**: sono anche
   due corpora diversi, e la misura non sa separare le due cause. Il dato regge come segnale, non
   come misura pulita dell'effetto di aver cambiato il contratto in corsa.
2. Il confronto è contro «gli atti **più** le notizie già estratte dal Report 1»: eredita gli errori
   e le omissioni di quella pipeline.
3. L'unità di conteggio è la candidata, non il fatto: due lettori possono spezzare lo stesso fatto
   in modo diverso.
4. Un accostamento `dubbio` non prova una sovrapposizione: per questo il numero è un intervallo.
5. I dati di volume (parole, parole al minuto) sono inaffidabili dove la duplicazione supera il 10%
   — **e la regola che li invalida è stata applicata in tre modi diversi**, perché dice «i campi di
   volume» al plurale e i lettori hanno letto il plurale in modi diversi. Sui 45 item sopra la
   soglia: 21 hanno entrambi i campi dichiarati inattendibili, 16 solo le parole al minuto, 8
   nessuno dei due. In pratica **il 10,9% delle parole del corpus viene da registrazioni sopra la
   soglia e conserva un conteggio numerico**: chi sommasse quel campo sommerebbe anche testo
   duplicato. È un difetto nostro, di una regola scritta in modo ambiguo e non di chi l'ha applicata.
   La soglia però **non vede il difetto opposto**: una registrazione di 5h07 in cui il primo parlato
   arriva a `[85:57]`, con due sospensioni di 17 e 43 minuti e circa due ore e mezza di aula parlante,
   ha duplicazione 0,0% e trentaquattro parole al minuto — un dato di volume altrettanto privo di
   senso, che nessun controllo intercetta. Il difetto peggiore della fonte non è la ripetizione: è il
   silenzio.
6. Le misure sui silenzi valgono solo per le registrazioni con marcatore a 10 secondi: sulle altre
   un silenzio più corto di cinque minuti è invisibile.
7. Il materiale di riscontro è **congelato** in `report2/snapshot/`, così la novità non dipende dal
   giorno in cui un lotto è stato letto.
8. **La qualità della deduplicazione, misurata su campioni giudicati da tre lettori.** La
   precisione degli accostamenti forti è **58,1%** (54 su 93, con il rigiudizio che sostituisce i
   giudizi dati sul campione difettoso del punto 15): l'errore dominante è sempre lo stesso — una
   *convocazione* accostata all'*esito* della seduta che convoca, che condivide protocollo, oggetto e
   quasi tutto il testo. Nel rigiudizio sono **21 accostamenti su 79**, e 19 di quei 21 sono fatti
   diversi. Il richiamo, su 40 candidate date per nuove, perde **2 gemelli veri** (5%, IC
   [1,4% , 16,5%]). Applicando le due correzioni — `S × (1 − perso) + D × (1 − precisione)`, che è
   la formula che `report2/risposta.py` scrive per esteso — la novità certa passa da 44,6% a
   **45,6%**: sale, perché gli accostamenti forti sbagliati restituiscono più righe di quante il
   richiamo ne tolga.
   Il difetto più profondo non è una soglia: **l'unità di confronto non è la stessa dalle due
   parti**. Dal lato parlato l'unità è il fatto, dal lato scritto è il documento — ogni verbale
   produce una riga sola, la cui sintesi racconta un punto solo dell'ordine del giorno. Un fatto che
   nel verbale è il terzo punto **non ha modo di essere riconosciuto**, e il richiamo è compromesso
   prima del confronto. Il rigiudizio lo conferma nei due versi: **cinque dei diciannove gemelli veri
   che ha trovato sono invisibili sulle sintesi** e si vedono solo aprendo il testo dell'atto — uno
   sta in «varie ed eventuali» —, e lo stesso verbale viene accostato a due candidate diverse della
   stessa seduta, che lo stesso fatto non sono.
   Quanto pesi si può misurare, perché il testo integrale degli atti ce l'abbiamo: cercando ogni
   candidata data per nuova **dentro il testo** di un atto plausibile — stesso Municipio, tre giorni
   di distanza, con il suo toponimo e una parola del titolo — se ne ritrovano **164 su 442, il
   37,1%**. Una parola che compare in un atto non prova che sia lo stesso fatto: 37,1% è un **tetto**,
   non una stima. Ma dice che il 5% misurato sul confronto fra righe è solo la parte visibile: quello
   è ciò che il confronto poteva vedere e non ha visto, questo è ciò che **per costruzione non
   poteva vedere**.
9. **Il denominatore contiene cinque righe di troppo** — lo 0,5% —, perché una seduta è stata
   pubblicata due volte e le sue notizie sono state estratte due volte. È l'unico caso nel corpus, e
   toglierle sposta l'intervallo grezzo di uno o due decimi: da [44,6% , 92,2%] a [44,7% , 92,4%].
   Vale la pena dire **come** si trova, perché la regola ovvia è sbagliata: cercare i doppioni per
   titolo e data ne produce 34, quasi tutti falsi, dato che più commissioni dello stesso giorno sono
   pubblicate con lo stesso titolo generico. Il doppione vero si riconosce dal contenuto — due
   documenti le cui candidate hanno lo stesso insieme di titoli — e così contati sono uno.
10. **L'unità di misura della dispersione fra lotti** (§7.1) confronta due gruppi che differiscono
   per la regola di lettura *e* per il corpus: il segnale c'è, la separazione delle due cause no.
11. **Il meccanismo del §2 è un'ipotesi**, e queste sono le tre cose che la smentirebbero: una quota
   alta di candidate «compiute, datate e localizzate» che restano senza gemello anche estendendo il
   corpus ai mesi vicini; nessuna differenza di qualità fra candidate nuove e confermate, o una
   differenza di segno opposto; molti casi «residuali» che si scoprono già formalizzati in atti
   dello stesso perimetro. Nessuno dei tre è stato testato: vanno fatti prima di trattare il
   meccanismo come acquisito.

12. **L'insieme di confronto non è omogeneo fra i Municipi, e dove manca un tipo di atto la novità
   sale.** Le convocazioni di commissione sono nel corpus per undici Municipi e **per quattro no** —
   II, III, IV e XV: zero atti di quel tipo. Non è una scelta, è come li pubblicano. L'effetto si
   misura: nei quattro Municipi senza convocazioni la quota di candidate con un duplicato certo è
   **4,0%**, negli altri **9,6%** — meno della metà —, e la novità certa è 46,3% contro 42,2%.
   Accanto all'assenza c'è una causa diversa e molto più rara, da non confondere con quella:
   l'**illeggibilità**. Undici atti su 1.983 hanno un testo sotto i 400 byte — scansioni di moduli
   manoscritti che non restituiscono né la data né l'ordine del giorno: il documento c'è e non dice
   niente. La direzione è quella che ci si aspetta e la causa non è separabile dalle differenze reali
   fra Municipi, ma va detta: **una parte della novità che misuriamo è la forma in cui un'amministrazione
   pubblica i propri atti**. Con un'ironia utile: le convocazioni sono anche il tipo di documento che
   produce **quasi tutti gli accostamenti sbagliati** (21 su 79 nel rigiudizio, 19 dei quali fatti
   diversi), perché condividono protocollo e oggetto con il verbale della seduta che convocano.
13. **Un'obiezione che ci siamo fatti da soli, e che non regge: «i verbali mancano perché non li
   avete raccolti».** Un lettore l'ha sollevata trovando una commissione di cui il corpus ha il
   verbale 53 e il 56 ma non il 54 e il 55. È verificabile, perché ogni verbale ne cita un altro
   quando lo approva: prendendo tutti i riferimenti «verbale n. X del …» presenti nei testi e
   tenendo quelli che puntano a sedute **dentro la finestra**, ne risultano 41 — e **40 sono nel
   corpus**. Ne manca uno. Quindi l'assenza di un verbale, dove la si osserva, è quasi sempre una
   proprietà di come quell'organo verbalizza, non della nostra raccolta. Vale per i verbali; per le
   convocazioni il punto 12 dice il contrario, ed è per questo che i due casi vanno tenuti separati.
14. **Una deviazione dallo schema, voluta e mai dichiarata finora.** Lo schema dice che il Municipio
   dichiarato dalla fonte prevale sul toponimo dedotto dal testo; il programma fa il contrario —
   **quando il testo nomina un Municipio, vince il testo**. La ragione sta nei dati: l'etichetta della
   fonte descrive la *pagina*, e sul portale municipale è spesso l'elenco delle categorie, fino a
   tutti e quindici i Municipi insieme. Quanto pesa: **886 righe** hanno un Municipio ricavato dal
   testo, e in **336 casi (37,9%)** quel Municipio non è fra quelli dichiarati dalla fonte. È una
   deviazione grossa, e va detto che l'abbiamo scelta noi: chi rifacesse i conti seguendo lo schema
   alla lettera otterrebbe una distribuzione territoriale diversa.
15. **Un difetto nostro, trovato tre giorni prima della consegna, e quanto pesa.** Gli
   identificativi delle righe sono stabili — legati a documento e titolo, non alla posizione — ma
   fino a oggi venivano assegnati **dopo** i confronti. Il file su cui si audita, che elenca le
   coppie parlato-scritto, era quindi scritto con i numeri vecchi: **612 righe su 1.429** puntavano
   a un'altra riga. Non tocca i conteggi — le classi S, U e D si calcolano sugli oggetti, e
   ricostruito il database col programma corretto i conteggi per riga e il file delle coppie
   coincidono esattamente — ma tocca **gli audit**: per una parte delle candidate il campione
   elencava la riga e poi, sotto «accoppiata a:», **niente**. Nel campione congelato sono 25 casi su
   117. I lettori se ne sono accorti e hanno ricostruito la coppia dai dati, ma il rischio si misura:
   nella classe incerta, dove il campione mostrava gli accostamenti i gemelli veri erano 9 su 30, dove
   non mostrava niente **0 su 10**: il rischio dichiarato era che la risposta scendesse di circa un
   punto e mezzo.
   **È stato chiuso rifacendo il campione e facendo rigiudicare quei casi a un terzo lettore**, che
   non ha visto i giudizi precedenti. Sulle 28 candidate incerte rigiudicate i gemelli veri sono **3**
   (erano 4), e per **nessuna** delle nove che restano senza accostamenti esiste una riga scritta con
   lo stesso fatto: cercate una per una nei 2.668 testi integrali, zero occorrenze. Lo zero non era un
   effetto del campione difettoso, era il dato. La quota di gemelli veri fra le incerte passa quindi da
   18,8% a **17,5%** e la risposta da 83,9% a **83,8%**: il difetto era reale, l'effetto sul numero
   principale è di un decimo di punto. Resta vero per gli altri usi di quel file — chiunque risolva
   quegli identificativi come se fossero del database ottiene righe sbagliate, ed è successo a noi.

## 6-bis. Una seconda AI sulle candidate, e che cosa ha insegnato il primo tentativo

Il metodo prescrive che un modello di un'altra famiglia rilegga un campione di candidate già
classificate e dica se è d'accordo. Su 30 candidate — 20 dalle registrazioni, con il tratto di
trascrizione allegato, 10 dagli atti, con la sola riga — l'esito è **25 concordi e 5 discordi**: un
disaccordo del 21% dove una verifica vera era possibile. Le cinque discordanze che restano sono
sostanziali: l'estratto sostiene solo una parte della sintesi, oppure il tipo dichiarato è sbagliato.

**Il primo tentativo però ne aveva trovate dodici su venti**, e quel 60% sarebbe stato un risultato
falso. I motivi erano quasi tutti della stessa forma — «X non compare nell'evidenza allegata» — e
l'evidenza allegata era duemila caratteri attorno al **primo** marcatore: una candidata con più
marcatori, o il cui dettaglio arriva più avanti dentro un blocco da cinque minuti, risultava non
sostenuta **per costruzione**. Allargando l'estratto a tutti i marcatori citati, otto discordanze su
dodici sono sparite.

Vale la pena scriverlo perché riguarda chiunque usi una seconda AI come controllo: **se il
verificatore riceve meno contesto di quanto ne avesse il lettore originale, non si misura la qualità
della lettura, si misura la propria troncatura.** La finestra di evidenza è un parametro del
risultato, non un dettaglio di implementazione.

Un limite dichiarato: alle candidate che vengono dagli atti non è stato allegato il testo dell'atto,
perché i testi degli atti non sono mai stati trasmessi a un servizio esterno e alcuni contengono dati
personali. Su quelle dieci righe la seconda AI ha potuto giudicare **solo la coerenza interna**.

## 7-bis. Da dove viene ogni numero

Perché chiunque possa rifarli invece di crederci. Tutti girano su `report2/snapshot/`, che è
congelato, con `QN_NET` puntato alla cartella dei dati.

| numero | programma |
|---|---|
| 44,6% e 92,2% (intervallo grezzo di novità) | `report2/novita_meccanica.py` |
| 17,5% di gemelli veri fra le incerte, e da lì l'83,8% | `report2/risposta.py`, che legge i file dell'audit |
| il campione degli audit, e quello del rigiudizio | `report2/campione_dedup.py`, `report2/ricampiona_toccati.py` |
| 30,6% (scartando i toponimi incerti) | `report2/audit_toponimi.py` |
| dispersione fra lotti, 1,46 e 0,74 | `report2/varianza_lettori.py` |
| 107 atti che rinviano alla registrazione | `report2/record_dichiarato.py` |
| 17 identificativi di seduta negli atti, 7 risolti | `report2/link_verbali_video.py` |
| collegamento registrazione-atto | `report2/collega_video_atti.py` |
| tutte le tabelle del database | `report1/build_db.py` |
| 25 concordi e 5 discordi della seconda AI | `report2/seconda_ai.js` |
| 37,1% delle nuove presenti nel testo di un atto | `report2/copertura_testi_atti.py` |
| i doppioni di pubblicazione e quanto spostano l'intervallo | `report2/doppioni_documenti.py` |
| la convenzione dell'organo contro la novità, r = −0,60 | `report2/convenzione_organo.py` |

Alla consegna, `report2/congela_consegna.py` mette accanto al rapporto lo **stato che ha prodotto
questi numeri**: i dati, i programmi che li calcolano, il commit del repository e un file di numeri
generato eseguendo i programmi, non ricopiato a mano. Senza, «83,8%» è un'affermazione che nessuno
può rifare, perché il database cambia a ogni lotto che rientra.

E un programma, `report2/verifica_numeri_rapporto.py`, ricalcola tutti questi valori dal database e
dice quali il testo non contiene più: serve perché a ogni lotto che rientra i numeri invecchiano, e
cercarli a occhio in quattrocento righe non funziona — quattro erano vecchi anche dopo due giri di
correzione a mano.

Quello che **non** è riproducibile da un programma sta nei §3 e §4: sono letture, non misure, e ogni
caso porta l'identificativo dell'atto o della registrazione con il marcatore, così che chiunque
possa andare a vedere.

**Quello che la riservatezza ci costa, detto per intero.** In una seduta il fatto è che la titolare
di un banco di mercato non ha mai protocollato una domanda. Il verbale municipale lo scrive con il
numero del banco e il tipo di attività; noi no, perché il banco è uno solo e quei due dati
identificano una persona privata quanto un nome. Il fatto amministrativo resta nei nostri file,
l'attribuzione no — e **chi volesse contestare quella notizia non avrebbe abbastanza per farlo**. È
il prezzo di DEC-102. Va pagato, e va scritto che lo si sta pagando.

## 8. Decisioni editoriali in attesa dell'owner

**D5 — il numero civico di una sede pubblica.** Tre lettori hanno segnalato che il divieto di
civici, applicato alle sedi pubbliche, toglie precisione senza proteggere nessuno: due immobili
comunali contigui messi a bando diventano indistinguibili per indirizzo. Raccomandazione: tenere il
civico quando individua una sede o un immobile pubblico. Fino alla decisione i lettori applicano il
divieto senza eccezioni.

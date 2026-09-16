# Ricostruzione di giugno 2026 — Report 2: gli atti e le registrazioni

Bozza in lavorazione. I materiali sono letti per intero sul lato atti e per circa metà sul lato
registrazioni; **i conteggi qui dentro sono quelli al 16 settembre e vanno rigenerati prima della
consegna** con `report1/build_db.py`, `report2/novita_meccanica.py` e `report2/audit_toponimi.py`.
I meccanismi descritti nei §3 e §4 ricorrono in tutti i lotti letti finora; quanto siano stabili
è però un'impressione di lettura e non una misura, e come tale va presa.

Perimetro: **8–28 giugno 2026**, come prescrive il metodo. Il Report 1 aveva letto 985 item
testuali e ne aveva ricavato 1.227 notizie candidate.

## 1. In breve

- Letti **1.983 atti amministrativi** — tutti quelli con data di repertorio fra l'8 e il 28 giugno,
  che è il perimetro dello studio — e **415 registrazioni di sedute**, 97 dai canali YouTube dei
  Municipi e 318 da RomaTV. Alla data di questa bozza le registrazioni lette sono **226**.
- Gli atti danno **628 notizie candidate**, le registrazioni **964** finora.
- La domanda del rapporto — *quanto aggiunge il parlato a ciò che è scritto* — non ha una risposta
  sola. Ne ha tre, misurate: **32%** di novità certa con un toponimo affidabile, **48%** di novità
  certa, fino al **97%** come limite superiore.
- **107 verbali su 2.668 atti, in sette Municipi su quindici, dichiarano dentro il proprio testo
  che il record completo della seduta non è l'atto ma la registrazione** — con quattro formule di
  forza diversa, dalla più netta («la videoregistrazione sostituisce la trascrizione degli
  interventi», 21 atti del Municipio II) al semplice rinvio al portale. Non è una tesi nostra: è
  l'amministrazione che lo scrive. È il fatto da cui parte questo rapporto, non la causa di tutto
  ciò che segue.

## 2. La risposta, e perché sono tre numeri

Il campo che i lettori compilano riga per riga (`novita_rispetto_agli_atti`) è un giudizio, e nel
corso dello studio è stato definito **tre volte in modo diverso** — due delle quali per errori miei,
corretti e dichiarati. Non è quindi una serie omogenea, e non può essere il numero principale.

Il numero principale è meccanico: ogni candidata che viene dal parlato è confrontata, con la stessa
deduplicazione usata per tutto il corpus, contro **tutte le righe che vengono da fonti scritte**.
Tre esiti:

| | |
|---|---|
| **S** — nessun gemello fra le righe scritte | 463 |
| **U** — nessun duplicato, ma almeno un accostamento dubbio | 472 |
| **D** — almeno un duplicato certo | 29 |

Da cui la scala:

- **32,1%** — nuove, con un toponimo che il lettore non ha marcato incerto. È il valore più
  conservativo che sappiamo calcolare, e **non viene dallo stesso programma degli altri due**: lo
  calcola `report2/audit_toponimi.py` scartando le righe che poggiano su un toponimo dichiarato
  dubbio. Regge all'obiezione sulla trascrizione, non a tutte: se la deduplicazione sbaglia a non
  accostare, anche questo numero è alto.
- **48,0%** — nuove, cioè senza alcun gemello scritto, toponimi incerti compresi.
- **97,0%** — limite superiore, se si contano come nuove anche quelle che hanno solo un
  accostamento dubbio.

**Contro che cosa sono misurati, detto con precisione.** Non contro i soli atti: contro **tutte le
righe che vengono da fonti scritte**, cioè i 1.983 atti con repertorio 8–28 giugno *più* le notizie
già estratte dalle fonti testuali del Report 1. Il nome del campo (`novita_rispetto_agli_atti`) dice
meno di quello che il numero misura, ed è un difetto di nome che va tenuto presente: una candidata
del parlato è «nuova» quando non ha gemelli **né negli atti né nel già raccolto**. Gli atti sono
quelli con data di repertorio fra l'8 e il 28 giugno, che è il perimetro dello studio. Gli altri 685 atti di giugno che abbiamo in
archivio sono dell'1–7 e del 29–30: fuori finestra per costruzione, non dimenticati.

C'è però un punto in cui il perimetro, definito sulla data di repertorio, **non coincide con il
perimetro dei fatti**, e lo abbiamo chiuso leggendo 161 atti in più. Per i verbali la data di repertorio è la data della seduta, e allora il
verbale di una seduta dell'8–28 giugno sta sempre dentro. Per le **convocazioni** la data di
repertorio è quella del protocollo, che precede la seduta: la convocazione di una seduta dei primi
giorni della finestra, protocollata prima dell'8, **resta fuori**. È una conseguenza necessaria
della definizione, la stiamo chiudendo leggendo quelle convocazioni, e tocca il collegamento fra
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
il corpus. È una deviazione, e **abbassa** la novità di due punti (50,1% dentro i blocchi contro
48,0% su tutto). Diciamo entrambe le cifre invece di scegliere quella che ci comoda.

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

L'esempio più netto — uno solo, quindi illustrativo e non probante — è una frase di una
commissione del Municipio V, dove lo stesso lettore, leggendo
lo stesso elenco ad alta voce, ha prodotto due righe di esito opposto: la risoluzione su viale
Palmiro Togliatti è «anche negli atti», perché l'atto è di giugno; gli stalli di via Antonio
Tempesta sono «non verificabile», perché il verbale che li contiene è di maggio. **Cambia solo il
confine del corpus.**

Se il meccanismo è giusto, quel 25% non misura la debolezza del parlato ma **dove passa il confine
di ciò che abbiamo raccolto**. È un'ipotesi coerente con i casi letti, non una conclusione
dimostrata: per dimostrarla servirebbe scomporre il 25% nelle sue cause, e non l'abbiamo fatto.

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

Quanto un verbale conservi non dipende però da quanto la seduta sia stata vivace: **dipende da come
il verbale è scritto**. I verbali in prosa narrativa estesa — quelli redatti riascoltando — tengono
tutto, comprese cifre che la trascrizione automatica storpia: uno scrive `17.182,05 euro` dove la
registrazione dice «17.000». I verbali a elenco puntato tengono l'intestazione e le presenze. Il
caso estremo è un verbale che registra «Intervengono il presidente, il consigliere X e il
consigliere Y» e nient'altro, mentre l'intera discussione — chi non voterà e perché, quali risorse
non sono arrivate — esiste solo nella registrazione.

Questa correzione viene da un lettore a cui era stata chiesta la verifica dell'ipotesi opposta, e
che l'ha smentita misurando. Vale come sono state scritte tutte le regolarità di questo rapporto:
finché un lotto non le smentisce.

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

**Nella pubblicazione delle registrazioni** — difetti di chi pubblica. Su 274 item censiti al
momento della misura, quattro sono **due sedute pubblicate due volte**; altri cinque sono **spezzoni
consecutivi della stessa seduta** pubblicati come registrazioni distinte. Sono due difetti diversi e
si contano separatamente, perché le ripubblicazioni condividono il testo e gli spezzoni no: una
misura che cerca testo condiviso vede i primi e **per costruzione** non vede i secondi.

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
5. I dati di volume (parole, parole al minuto) sono inaffidabili dove la duplicazione supera il 10%.
6. Le misure sui silenzi valgono solo per le registrazioni con marcatore a 10 secondi: sulle altre
   un silenzio più corto di cinque minuti è invisibile.
7. Il materiale di riscontro è **congelato** in `report2/snapshot/`, così la novità non dipende dal
   giorno in cui un lotto è stato letto.
8. **La qualità della deduplicazione è assunta, non misurata.** I tre numeri dipendono da quanto
   bene la regola (data ±1 giorno, luogo, oggetto) accosta ciò che va accostato: un audit di
   precisione e richiamo su un campione non è stato fatto, e senza quello l'intervallo dichiara
   l'incertezza sugli accostamenti dubbi ma non quella sugli accostamenti mancati.
9. **L'unità di misura della dispersione fra lotti** (§7.1) confronta due gruppi che differiscono
   per la regola di lettura *e* per il corpus: il segnale c'è, la separazione delle due cause no.
10. **Il meccanismo del §2 è un'ipotesi**, e queste sono le tre cose che la smentirebbero: una quota
   alta di candidate «compiute, datate e localizzate» che restano senza gemello anche estendendo il
   corpus ai mesi vicini; nessuna differenza di qualità fra candidate nuove e confermate, o una
   differenza di segno opposto; molti casi «residuali» che si scoprono già formalizzati in atti
   dello stesso perimetro. Nessuno dei tre è stato testato: vanno fatti prima di trattare il
   meccanismo come acquisito.

## 7-bis. Da dove viene ogni numero

Perché chiunque possa rifarli invece di crederci. Tutti girano su `report2/snapshot/`, che è
congelato, con `QN_NET` puntato alla cartella dei dati.

| numero | programma |
|---|---|
| 48,0% e 97,0% (intervallo di novità) | `report2/novita_meccanica.py` |
| 32,1% (scartando i toponimi incerti) | `report2/audit_toponimi.py` |
| dispersione fra lotti, 1,46 e 0,74 | `report2/varianza_lettori.py` |
| 107 atti che rinviano alla registrazione | `report2/record_dichiarato.py` |
| 17 identificativi di seduta negli atti, 7 risolti | `report2/link_verbali_video.py` |
| collegamento registrazione-atto | `report2/collega_video_atti.py` |
| tutte le tabelle del database | `report1/build_db.py` |

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

# Nomi e territorio — specifica di lettura (DEC-105)

Sostituisce la regola di anonimizzazione che lo studio aveva costruito sopra la DEC-102.
Vale per ogni nuova lettura e per la passata di ripristino sui lotti già letti.
Il nucleo della DEC-102 non cambia: i dati per item non entrano nel repository pubblico,
si consegnano su Drive.

## 1. I nomi si conservano

**La regola.** Il nome della persona di cui parla la notizia **si scrive**. Assessori,
consiglieri, funzionari, cittadini, rappresentanti di comitati, professionisti, imprese e
ditte individuali: nome, ruolo e organizzazione stanno insieme, perché è la terna che
permette di capire chi risponde di che cosa nel quartiere. Non esiste più la sostituzione
automatica con il ruolo.

**Il criterio è la pertinenza al fatto**, non la categoria della persona. Pertinente è chi
agisce, decide, propone, chiede, risponde, testimonia o subisce il fatto raccontato. Non è
pertinente chi compare per ragioni che con il fatto non c'entrano.

Un chiarimento su un caso che torna spesso: **le autorità presenti a una cerimonia pubblica sono
pertinenti**. Un'inaugurazione, un'intitolazione, una commemorazione *sono* l'occasione in cui chi
governa si mostra, e per un giornale di quartiere chi c'era è spesso la notizia. Vale il criterio
generale: togliere un nome vuole una ragione concreta, e «compare in un elenco di presenze» non lo
è quando il fatto è la presenza.

**Un'omissione va motivata.** Se un nome si toglie, in `note` va scritta la ragione
**concreta e legata al contenuto** («il verbale attribuisce la frase a due persone diverse»,
«compare solo come recapito del richiedente»). *Non* sono ragioni: che la stringa sia un nome
di persona, che la persona sia un privato cittadino, la prudenza in sé. Nel dubbio si scrive
il nome e si dichiara il dubbio.

**La forma.** Il nome torna nella prosa italiana corrente, con la carica accanto dove aiuta a
capire — «l'assessore Petracca», «il direttore del Dipartimento Tutela Ambientale Giuseppe
Sorrentino» — non `Nome Cognome (ruolo)` fra parentesi, che spezza le frasi in cui la carica è già
scritta per esteso. La parentesi si usa solo dove senza si leggerebbe male. Se il campo cita già la
persona poco prima, la seconda occorrenza si riduce al cognome invece di ripetere tutto.

**Una fonte per il fatto, non per la riga.** Il nome deve comparire in una fonte **di quel fatto**.
Due registrazioni della stessa seduta sono due fonti dello stesso fatto: se il nome si sente in una
sola delle due, vale, e si dichiara in `note` da quale. Resta vietato prenderlo da un'altra seduta,
da un altro atto o da quello che si sa del Municipio.

**Anche le organizzazioni erano state perifrasate.** Nessuna regola lo chiedeva, ma i lettori hanno
reso «Fondazione Piccolo America» come «una fondazione cinematografica romana», «Witch Post» come
«un duo indie-pop». La DEC-105 nomina le imprese fra ciò che si conserva, e un'organizzazione senza
nome non si può né cercare né verificare: **si rimettono**, con la stessa verifica sulla fonte.

**Che cosa è una formula da correggere.** È una formula quella che sta al posto di **una persona
che ha agito**: «il presidente», «il direttore», «la referente», «un consigliere». **Non** è una
formula l'attribuzione a un **organo o a un ente** che agisce come tale: «la presidenza», «la
giunta», «la polizia locale», «l'associazione», «il Municipio». Quelle restano, perché sono
l'organizzazione, che la DEC-105 tiene accanto al nome e non al posto del nome. Nel dubbio conta chi
compie l'atto: se a parlare, decidere o rispondere è una persona, il nome va cercato.

Non è una formula nemmeno il ruolo che non designa nessuno: «un direttore dedicato» in un assetto
d'ufficio, «un professionista» che un'associazione dovrà incaricare. Lì non c'è una persona da
nominare, e si dichiara.

**La fonte vince anche sul ruolo, non solo sul genere.** Se la formula dice «il direttore audito» e
la fonte dice che quella persona sostituisce il direttore, si scrive quello che la fonte sostiene e
si dichiara lo scarto. Vale il limite di sempre: si corregge con quello che la fonte dà, non si
inventa una carica per far tornare la frase.

**Quando la fonte dà solo il nome di battesimo.** In commissione ci si chiama per nome e l'appello
elenca i cognomi: spesso non c'è modo di ricongiungerli dentro la stessa fonte. «Il consigliere
Andrea» **conta come ripristino**, non come identificazione insufficiente: è quello che la fonte
dice, ed è più di «un consigliere». Si dichiara che il cognome non c'è. Toglierlo richiederebbe una
ragione concreta, e «è solo il nome di battesimo» non lo è.

**Il genere lo detta la fonte, non la formula.** Dove la formula anonimizzata dice «una consigliera»
e la fonte dice «il consigliere Guerrini», vince la fonte, e lo scarto si dichiara. La formula è
quello che va corretto: non può essere la prova di sé stessa.

**Due incertezze diverse, due posti diversi.** `trascrizione_incerta` riguarda **la forma udita**:
il cognome che si sente in due modi — **o una volta sola**. Un cognome pronunciato un'unica volta in
una trascrizione automatica è il caso più fragile che ci sia, non il più sicuro: niente lo conferma.
Il flag si alza anche lì. Quando invece è fragile **l'attribuzione** — la voce non è
etichettata, il ricongiungimento fra nome e cognome poggia su un solo scambio — si alza
`attribuzione_incerta` e si spiega in `ragione`. Sono cose che un lettore del dato deve poter
distinguere senza leggere la prosa: un cognome incerto si verifica riascoltando, un'attribuzione
incerta si verifica ricostruendo chi parlava.

**Il minutaggio dell'evidenza si corregge.** Se `evidenza_locale` punta a un blocco che non contiene
il passaggio, si scrive quello giusto e si dichiara lo scarto. La frase dell'evidenza non si
accorcia mai; il puntatore invece va tenuto giusto, perché è con quello che un altro verifica la
notizia, e un puntatore sbagliato disfa il metodo.

**Verifica sulla fonte.** Un nome ripristinato va **riletto sulla fonte**, non ricostruito a
memoria né dedotto dal ruolo. Se la fonte è una trascrizione e il nome è incerto, si scrive
la forma udita e si alza `trascrizione_incerta`; se la fonte non permette di stabilirlo, resta
il ruolo con la ragione in `note`.

**Che cosa non cambia.** Restano alla lettera, come già erano: toponimi, titoli di opere e di
sedi, nomi in intitolazioni e commemorazioni, denominazioni di organizzazioni, URL delle
pagine pubbliche. La colonna si chiama ora `titolo`: `titolo_anonimizzato` era il nome di una
regola che non c'è più.

## 2. Il confine della seduta

Vale per le registrazioni. **Entra nell'analisi e nelle notizie solo ciò che sta dentro la
seduta formalmente aperta.** Restano fuori: tutto ciò che precede l'apertura, tutto ciò che
segue la chiusura, e **le sospensioni**, per intero, dall'annuncio della sospensione alla
ripresa dichiarata.

I riferimenti sono gli atti formali che si sentono in aula: **apertura, sospensione, ripresa,
chiusura**. Si segnano i minutaggi e si usano quelli.

**«Fuori verbale» non sospende la seduta.** È un'intenzione di chi parla, non un atto del
presidente: se la seduta è aperta, quel passaggio è dentro il perimetro e si tratta come tutto
il resto, nomi compresi. Vale anche per formule equivalenti («questo non mettetelo a verbale»,
«a telecamere spente» detto a telecamere accese).

**La ripresa può non essere dichiarata a parole.** Capita che il presidente sospenda e che nessuno
annunci la ripresa, mentre la seduta riprende di fatto: si dà il benvenuto a un ospite, si dà la
parola, si approva un verbale, si dichiara la chiusura. In quel caso **i lavori si considerano
ripresi dal primo atto formale che li riprende**, e lo si scrive. Leggere la regola alla lettera
butterebbe fuori l'intera registrazione, che non è quello che la regola vuole: il perimetro esclude
ciò che seduta non è, non la seduta che nessuno ha riaperto a voce.

Attenzione a non confondere il tema con l'atto: «lavori sospesi del cantiere», «piattaforma
sospesa», «direttiva sospesa» sono argomenti di discussione, non sospensioni della seduta.

Il materiale fuori seduta non entra nei file, nemmeno anonimizzato, e non si riproduce nei
log: se ne dichiara solo l'esistenza, il minutaggio e la durata.

## 3. Il territorio: Municipio e quartiere

Dal luogo citato si ricavano **due attribuzioni distinte**, verificando che corrispondano
geograficamente:

- `municipio` — il Municipio.
- `quartiere` — il **quartiere d'uso comune**, quello con cui chi ci abita chiama il posto
  (`name_display` del gazetteer).
- `quartiere_zu` — la **suddivisione amministrativa** corrispondente, quando esiste
  (`zu_code`). Non tutti i quartieri d'uso comune ne hanno uno: dove manca, il campo resta
  vuoto e questo non è un difetto.

Le due cose non vanno confuse né fuse: un quartiere d'uso comune può non coincidere con
nessuna zona urbanistica, e una zona urbanistica può non avere un nome che qualcuno usi.

**Dedotto va dichiarato.** `territorio_dedotto` dice se l'attribuzione viene dal testo che la
afferma (`no`) o dal gazetteer a partire dai luoghi nominati (`sì`). Una deduzione dichiarata
è un dato utilizzabile; una deduzione spacciata per lettura non lo è.

**L'ambiguità resta ambigua.** Se il luogo sta a cavallo di più territori, o se i luoghi
nominati portano a territori diversi, si scrivono **tutti** i valori separati da `;` e non se
ne sceglie uno. Se il luogo non basta a decidere, `municipio` e `quartiere` restano
`non verificato` e il toponimo va in `toponimo_da_verificare`. Forzare un valore unico su un
caso a cavallo è l'errore che questa regola esiste per evitare.

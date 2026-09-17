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
pertinente chi compare per ragioni che con il fatto non c'entrano — chi è citato di sfuggita
in un elenco di presenze quando la notizia non riguarda le presenze, per dire.

**Un'omissione va motivata.** Se un nome si toglie, in `note` va scritta la ragione
**concreta e legata al contenuto** («il verbale attribuisce la frase a due persone diverse»,
«compare solo come recapito del richiedente»). *Non* sono ragioni: che la stringa sia un nome
di persona, che la persona sia un privato cittadino, la prudenza in sé. Nel dubbio si scrive
il nome e si dichiara il dubbio.

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

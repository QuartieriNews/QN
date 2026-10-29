# Timeline di brevi per quartiere: ce ne sarebbero abbastanza? (M, 26 ottobre 2026)

**La domanda dell'owner.** Si pensa a uno snippet come la striscia «Intanto» del Post: nella pagina del quartiere i titoli; cliccando, una
timeline verticale con titolo e breve di 2-4 frasi con i dettagli. Le voci sarebbero mini notizie, informazioni utili e dichiarazioni
politiche. La domanda è se ce ne sarebbero abbastanza per avere almeno una voce ogni 2 ore per quartiere, monitorando anche le pagine di
assessori, giunta e figure di spicco.

**In breve: no per il singolo quartiere, sì solo se la timeline mescola quartiere, municipio e città.**

| | Con le fonti che leggiamo oggi | Con le pagine di sindaco, giunta, presidenti, assessori e consiglieri (stima) |
|---|---|---|
| quartiere | 0,07 brevi al giorno | — |
| quartiere + municipio | 0,25 al giorno (una ogni 4 giorni); 3% delle fasce di 2 ore coperte | da 1,3 a 3,9 al giorno; 15-36% delle fasce coperte |
| quartiere + municipio + città | 8,2 al giorno; 60% delle fasce coperte | da 15 a 29 al giorno; 79-93% delle fasce coperte |

I valori sono mediane sulle 89 pagine. Le fasce sono le otto di 2 ore fra le 7 e le 23.

Il foglio con le brevi (titoli scritti da noi, tipo, portata, luogo, link alla fonte) e i valori per pagina sta su Drive:
`timeline_brevi_2026-10-26.xlsx`. Qui solo numeri e metodo (DEC-022, DEC-109).

## 1. Come è stato misurato

- **Corpus.** Tutte le 9.643 voci dall'1 al 25 ottobre già raccolte: 8.618 post Facebook (pool unificato, lista supplementare, Acilia) e
  1.025 notizie dei siti, comprese 686 voci corte che le analisi precedenti scartavano. Testate escluse. Nessuna lettura nuova e nessuna
  spesa Apify.
- **Smistamento.** Per ogni voce, se è una breve da timeline (abbastanza per un titolo e 2-4 frasi, utile per un quartiere, un municipio o
  la città, pubblicabile entro 48 ore). Poi il tipo, la portata, il luogo, la validità e un titolo scritto da noi.
- **Verifica.** Uno scettico rilegge un campione regolare di 381 brevi, fino a 12 per lotto, e conferma solo quelle che reggono. Poi si
  raggruppano i doppioni, cioè lo stesso fatto da fonti diverse.
- **Correzione del troncamento.** Di ogni pagina abbiamo solo gli ultimi 10-15 post. Le brevi al giorno di una fonte sono quindi la sua
  quota di brevi moltiplicata per i post al giorno misurati nelle letture del 24-25 ottobre. Il risultato si moltiplica per la precisione
  per tipo e si toglie la quota dei doppioni.
- **Geografia.**
  - Quartiere: dal toponimo del gazetteer nel luogo, altrimenti dalla sede della fonte.
  - Municipio: condiviso da tutte le pagine di quel municipio.
  - Città: condiviso da tutte le 89 pagine.
- **Fasce orarie.** Dalla distribuzione delle ore dei post di ottobre. Fra le 9 e le 13 escono due volte più post che fra le 21 e le 23.

## 2. Che cosa c'è oggi

| Voce | Valore |
|---|---|
| brevi trovate allo smistamento | 787 su 9.643 voci (8%) |
| precisione nel campione verificato | 62% (avvisi utili 75%, dichiarazioni politiche 77%, mini notizie 63%, segnalazioni 59%, eventi del giorno 51%) |
| doppioni | 25% delle brevi |
| brevi al giorno in tutta Roma, corrette | 21,7 |
| — di cui di portata cittadina | 8,0 (soprattutto Roma Capitale) |
| — di cui di portata municipale | 1,9 (in tutti i 15 municipi insieme) |
| — di cui di un quartiere | 10,3 (in tutte le 89 pagine insieme) |
| — senza destinazione | 1,5 |

| Tipo | Brevi al giorno, Roma |
|---|---|
| mini notizia | 7,1 |
| avviso utile | 6,4 |
| evento di oggi o domani | 4,3 |
| dichiarazione politica | 1,9 |
| segnalazione dei residenti | 1,7 |

**Per pagina.**
- **Solo il quartiere:** mediana 0,07 brevi al giorno; la pagina più ricca arriva a 0,64.
- **Quartiere più municipio:** mediana 0,25 al giorno. Nessuna pagina arriva a una breve al giorno.
- **Aggiungendo le brevi della città:** ogni pagina sale a circa 8 al giorno, ma sono le stesse 8 su tutte le 89 pagine.

**Eventi del giorno.** La pagina «Eventi dei quartieri» darebbe in più, per pagina, una mediana di 0,27 eventi che iniziano ogni giorno
(0,53 al 75° percentile), se si volesse scriverne una breve.

## 3. Le pagine di politici e istituzioni

Nei dati ci sono 26 pagine politiche o istituzionali: Roma Capitale, la Città metropolitana, nove Municipi, il sindaco, due assessori e
alcuni presidenti e consiglieri. Sono molto più dense delle altre:
- il 53% dei loro post è una breve, contro l'8% generale;
- per portata, le brevi si dividono quasi in terzi fra quartiere, municipio e città.

**Il loro ritmo invece non si può misurare con i dati che abbiamo.** La lettura di ottobre ne ha restituito pochi post: dalla pagina del
sindaco 6 in tutto ottobre, quasi certamente meno di quelli pubblicati. Per questo la tabella iniziale usa due ipotesi:
- **Ritmo:** 0,3 post al giorno (basso) e 1 al giorno (alto).
- **Pagine per municipio:** 19 (presidente, sei assessori, una dozzina di consiglieri attivi).
- **Pagine cittadine:** 60 (sindaco, giunta, consiglieri capitolini attivi, figure di spicco).
- **Resto:** precisione 70% e doppioni 25%, come misurati.

**Costo di lettura.** I post si pagano a post (0,005 dollari con il filtro data), non a lettura. Leggere ogni ora per avere brevi fresche
costa quindi quasi come leggere ogni giorno: 0,7 dollari al mese di avvii. Le 345 pagine politiche ipotizzate costerebbero da 15 a 52
dollari al mese, in aggiunta ai circa 15 della lettura dei promotori.

## 4. Che cosa dice

- **Una breve ogni 2 ore per quartiere non c'è.** Con le fonti attuali il singolo quartiere ha in mediana una breve ogni due settimane, e una
  ogni quattro giorni contando il municipio.
- **Con le pagine politiche si arriva a 1-4 brevi al giorno** di quartiere e municipio. Restano coperte solo il 15-36% delle fasce di 2 ore,
  perché le voci si concentrano fra le 9 e le 19.
- **Una timeline piena è soprattutto cittadina.** Il ritmo di una voce ogni 2 ore, con il 90% delle fasce coperte, richiede circa 23 voci al
  giorno per pagina. Ci si arriva solo mescolando quartiere, municipio e città, cioè con le stesse voci cittadine su tutte le pagine.
- **La leva per il quartiere sono gli avvisi ufficiali strada per strada:** chiusure e deviazioni, interruzioni di acqua e luce, lavori,
  ordinanze. Non sono stati misurati: le pagine provate (Roma Mobilità, ATAC, Acea, Areti) erano costruite in JavaScript o con indirizzi
  diversi. Il sito di Roma Capitale pubblica 3-8 notizie al giorno, di portata cittadina.

## 5. OWNER_DECISION_REQUIRED

1. **Forma della timeline.** Opzioni:
   - (a) solo voci del quartiere, con il ritmo che c'è (raro);
   - (b) quartiere, municipio e città insieme, con l'etichetta del livello su ogni voce;
   - (c) una timeline del municipio, filtrabile per quartiere.
2. **Fonti politiche.** Se monitorare le pagine di sindaco, giunta, presidenti, assessori e consiglieri, e con quali regole per le
   dichiarazioni (attribuzione, par condicio nei periodi elettorali).
3. **Misura prima di decidere.** Leggere le ultime due settimane di circa 40 pagine politiche (giunta e presidenti di municipio) per
   misurarne il ritmo vero: circa 4 dollari di Apify. E provare con un browser le pagine degli avvisi ufficiali, senza costi.

Il builder non sceglie.

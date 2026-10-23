# Aggregatori di eventi — schede (generato, ottobre 2026)

Un aggregatore è una fonte che elenca eventi di altri. Le schede dicono come vi si accede, che cosa è stato misurato a ottobre 2026 e quanto gli eventi che pubblica siano rintracciabili alla fonte originaria. Numeri, non eventi: i dati per evento stanno nel foglio su Drive.

## culture.roma.it — agenda di Roma Capitale

**Accesso.** API WordPress pubblica (`wp-json/wp/v2/event_calendar`) più la pagina di ogni appuntamento; nessuna clausola di riuso trovata (da verificare, L11). Letta con `apify/cheerio-scraper` il 20 ottobre 2026: 6.222 appuntamenti pubblicati dal luglio 2025; nel foglio quelli con fine dal 1° ottobre 2026.

**Cosa misura.** Luogo, indirizzo, Municipio, organizzatore (a cura di), ingresso, contatti. È l'aggregatore con la rintracciabilità più alta: quasi ogni scheda rimanda al sito del luogo o dell'organizzatore.

| misura | valore |
|---|---|
| eventi letti (ottobre 2026) | 708 |
| con pagina QN assegnata | 615 |
| fuori Roma | 2 |
| rintracciabilità: sito dell'organizzatore o dell'evento | 658 |
| rintracciabilità: solo biglietteria | 26 |
| rintracciabilità: solo social | 17 |
| rintracciabilità: nessun riferimento esterno | 7 |

## Facebook — eventi, via Apify

**Accesso.** Nessun accesso diretto dall'ambiente (DEC-102): gli URL degli eventi li raccoglie l'owner, l'Actor `apify/facebook-events-scraper` li legge (0,01 $ per evento; 584 URL il 23 ottobre 2026, 567 eventi, 17 bloccati o rimossi).

**Cosa misura.** Nome, date, luogo con coordinate, organizzatore con pagina, biglietti, partecipanti. Metà degli eventi ha come unico riferimento la pagina Facebook dell'organizzatore.

| misura | valore |
|---|---|
| eventi letti (ottobre 2026) | 567 |
| con pagina QN assegnata | 414 |
| fuori Roma | 144 |
| rintracciabilità: solo social | 256 |
| rintracciabilità: sito dell'organizzatore o dell'evento | 255 |
| rintracciabilità: solo biglietteria | 55 |
| rintracciabilità: nessun riferimento esterno | 1 |

## Roma Today (Citynews)

**Accesso.** Il robots.txt vieta scraping, text and data mining e usi per AI senza licenza scritta; nel repository è registrato come «nessun canale senza licenza». A ottobre 2026 le 324 schede evento sono state lette una volta, su indicazione dell'owner, per i soli campi di scheda (Dove, Quando, Prezzo, Sito web), il promotore e i link esterni; nessun testo conservato. I titoli delle sue pagine sono testo della fonte e non entrano nel repository (DEC-022).

**Cosa misura.** Il promotore quando l'evento è inserito dall'organizzatore (20 su 324); altrimenti la redazione riscrive il comunicato e di norma non linka: 168 schede senza alcun riferimento esterno, di cui per 109 la fonte esiste altrove (nel testo, in un'altra fonte del file o nel registro) e per 14 l'organizzatore è raggiungibile solo per contatto diretto.

| misura | valore |
|---|---|
| eventi letti (ottobre 2026) | 324 |
| con pagina QN assegnata | 239 |
| fuori Roma | 28 |
| rintracciabilità: nessun riferimento esterno | 168 |
| rintracciabilità: sito dell'organizzatore o dell'evento | 122 |
| rintracciabilità: solo social | 27 |
| rintracciabilità: solo biglietteria | 7 |

## Lettura diretta delle fonti locali (13-31 ottobre 2026)

**Accesso.** Siti dei luoghi scelti nel registro fonti del 13 ottobre (62 fonti: teatri, musei, cinema, club). Letti alla fonte, due passate.

**Cosa misura.** Evento, date, luogo, zona QN e Municipio assegnati a mano; flag «anche su Roma Today» (35 su 358).

| misura | valore |
|---|---|
| eventi letti (ottobre 2026) | 358 |
| con pagina QN assegnata | 330 |
| fuori Roma | 0 |
| rintracciabilità: letto alla fonte (sito del luogo) | 358 |

## Sovrapposizioni fra aggregatori

Gruppi di eventi riconosciuti come lo stesso evento (titolo quasi identico e date compatibili, oppure titolo simile con stessa data e luogo). Candidati da scorrere, non sentenze.

| tipo · fonti | gruppi |
|---|---|
| dentro una fonte · Comune di Roma | 12 |
| dentro una fonte · Facebook | 11 |
| dentro una fonte · Fonte locale | 4 |
| dentro una fonte · Romatoday | 3 |
| tra fonti · Comune di Roma + Facebook + Fonte locale | 2 |
| tra fonti · Comune di Roma + Facebook + Fonte locale + Romatoday | 2 |
| tra fonti · Comune di Roma + Fonte locale | 45 |
| tra fonti · Comune di Roma + Fonte locale + Romatoday | 5 |
| tra fonti · Comune di Roma + Romatoday | 2 |
| tra fonti · Facebook + Fonte locale | 3 |
| tra fonti · Fonte locale + Romatoday | 8 |

Organizzatori che su Facebook compaiono con un profilo personale: 0 occorrenze; il nome resta nel registro (DEC-105: nessuna anonimizzazione), l'indirizzo del profilo no, perché non è un canale di pubblicazione.


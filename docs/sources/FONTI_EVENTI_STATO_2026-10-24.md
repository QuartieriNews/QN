# Fonti eventi — stato al 24 ottobre 2026 e flusso continuo proposto

Rapporto di lavoro del builder (DEC-104) sul blocco eventi: cosa è stato letto, cosa è
stato trovato, cosa è pronto nel repository e cosa aspetta una decisione dell'owner. Ogni
numero è **M** (misurato) salvo dove è scritto **S** (stimato). I dati per evento e per
pagina (titoli, testi di presentazione) stanno su Drive e nell'anteprima privata, non qui
(DEC-022, DEC-109): `eventi_unico.xlsx`, `associazioni_fonti.xlsx`,
`eventi_senza_fonte_ricerca.xlsx`.

## 1. Dove siamo

| Cosa | Stato | Dove |
|---|---|---|
| Foglio unificato degli eventi di ottobre 2026 (Facebook via Apify, culture.roma.it, Roma Today, lettura diretta 13-31 ottobre) | 1.957 righe, geografia a due metodi, rintracciabilità, doppioni segnalati, colonna `riga_principale_proposta` (DEC-025 aperta) | Drive / anteprima |
| Wiki delle fonti eventi | 2.405 fonti (807 nel registro v2, 598 candidate dal censimento del 24 ottobre), pagine per Municipio e per pagina QN, «dove cercare» per ogni fonte, 181 fusioni proposte | `docs/wiki/fonti-eventi/` |
| Registro fonti versione 2 | 370 voci del 13 ottobre più 445 candidate della ricerca mirata per le 58 pagine QN deboli, ciascuna con tipo, zona, canale e dove cercare; decisione «candidata» | Drive (`registro_fonti_v2_pagine_deboli.xlsx`), ingresso del build della wiki |
| Censimento di 1.169 pagine Facebook di associazioni | letto al 99,9%: dati di pagina, eventi futuri, post degli ultimi sei mesi, sito, indirizzo geocodificato, verdetto automatico | `censimento-pagine.md` + foglio su Drive |
| Lettura settimanale dei siti delle fonti | strumento pronto e testato (`tools/fonti/leggi_eventi_siti.py`, T-LS-1..5); prima prova fatta sulle 809 fonti con un sito (§4 bis) | repository |
| Ricerca uno a uno dei 176 eventi senza fonte | fatta in due passaggi (sito del luogo nel registro, poi ricerca web): 30 fonti dirette trovate, `link_fonte_diretta` compilato | fogli su Drive |
| Decisioni aperte | DEC-023 (wiki fonti eventi), DEC-024 (censimento → registro, Facebook come canale), DEC-025 (precedenza fra fonti), DEC-026 (Roma Today) | `decisions/` |
| Censimento RUNTS (6.247 enti) | sito, Facebook, email, eventi e verdetto per ente; 955 rientrano (§1 ter) | Drive (`enti_terzo_settore_fonti.xlsx`) |
| Flusso continuo da A a Z | proposta per fonte, cadenza e passi fino alla home del quartiere | `docs/sources/FLUSSO_EVENTI_A_Z.md` |

## 1 bis. Fonti mirate per le 58 pagine QN deboli (M, 24 ottobre 2026)

Perimetro: le 89 pagine del gazetteer con meno di cinque eventi futuri nel foglio (31 a
zero, 27 fra uno e quattro). Metodo: per ogni pagina una ricerca per tipo di fonte
(parrocchia, centro anziani, comitato di quartiere, biblioteca, centro culturale, istituto
comprensivo, associazione; pro loco e consorzio per le 17 pagine di frontiera), 423 ricerche
Google via Apify (1,06 $), risultati tenuti solo se il nome del quartiere e la parola del
tipo compaiono nel titolo e il dominio non è un elenco, un aggregatore o una testata; più
quattro elenchi istituzionali letti per intero e geocodificati: centri sociali anziani dai
PDF ufficiali dei Municipi III, IV, X, XI, XII (39), biblioteche dall'elenco di Biblioteche
di Roma (45), istituti comprensivi dall'anagrafe MIUR 2026/27 (177), mercati rionali dai
dati aperti di Roma Capitale (69). Esito nel foglio `fonti_mirate_pagine_deboli.xlsx`.

| Misura | Valore |
|---|---|
| Candidate per le 58 pagine | 463 (sito 284, pagina Facebook 159, solo indirizzo 20); 443 con un indirizzo da controllare |
| Per tipo | istituti comprensivi 110 · comitati 72 · parrocchie 65 · centri anziani 61 · associazioni 39 · biblioteche 34 · centri culturali 31 · pro loco e consorzi 15 · mercati 13 |
| Pagine con almeno tre fonti (wiki + nuove) | 56 su 58; scoperte Dragona-Dragoncello (0) e Muratella (1) |
| Nuove nel registro v2 | 445 (17 coincidevano con voci del 13 ottobre) |

Limiti: le liste ufficiali dei centri anziani esistono solo per cinque Municipi; la
diocesi (parrocchie) e Overpass (OpenStreetMap) non sono raggiungibili dall'ambiente, le
parrocchie vengono dalla ricerca. Le candidate sono da leggere una volta a mano: la
ricerca garantisce il nome del quartiere nel titolo, non che la fonte pubblichi eventi.

## 1 ter. Censimento degli enti del terzo settore di Roma (RUNTS, M, 24 ottobre 2026)

6.247 enti iscritti al RUNTS con sede legale a Roma (file dell'owner: nome, codice fiscale,
sezione, 5x1000). Metodo: una ricerca Google per nome e una per codice fiscale sugli enti
rimasti senza nulla; un sito vale solo se la home contiene il codice fiscale, o se il dominio
somiglia al nome e la pagina contiene il nome; la pagina Facebook vale se il sito verificato
la linka o se Google la restituisce col nome dell'ente nel titolo; poi dati di pagina, eventi
futuri e post degli ultimi sei mesi via Apify, email dalla home e dalla pagina contatti dei
siti, indirizzi geocodificati. Esito nel foglio `enti_terzo_settore_fonti.xlsx` su Drive.

| Misura | Enti |
|---|---|
| Sito verificato | 2.958 (1.990 per nome, 815 per codice fiscale, 153 indicati dalla pagina Facebook) |
| Pagina Facebook | 2.632 (1.930 linkate dal sito verificato) |
| Nessuna presenza web trovata | 2.842 |
| Email ufficiale | 2.653 (2.044 dal sito, 609 dalla pagina Facebook); più di una 497; PEC a parte 553 |
| Rientrano come fonti di eventi (almeno due segnali) | 955 (annunci nei post 420, date recenti sul sito 285, calendario sul sito 133, eventi futuri su Facebook 55, enti nazionali da controllare 62); più 56 imprese sociali o servizi con gli stessi segnali |
| Da verificare (un solo segnale, o sezione eventi senza date) | 1.118; più 92 imprese sociali o servizi |
| Con pagina QN, fra quelli che rientrano | 536 (Municipio I da solo il 36%) |

Costo Apify: circa 111 dollari (post 54; ricerche Google 24,7; dati di pagina 24,1; eventi 8,6,
di cui 7,5 per una pagina di biglietteria abbinata per errore a un ente, run fermato e pagina
esclusa). Dal secondo giro ogni run è partito con un tetto di spesa; il mese si chiude a 137,6
dollari sul conto dell'organizzazione. Il foglio di confronto da 68 righe allegato al file RUNTS non è stato usato:
contiene handle inventati.

## 1 quater. Simulazione: se ogni ente facesse un evento nella pagina della sua sede (M)

Base: tutti gli eventi futuri noti al 24 ottobre (1.402, di cui 1.109 con pagina QN). Scenario
A: più un evento per ogni ente RUNTS che rientra; B: anche per quelli da verificare; C: A più
le pagine del censimento Facebook che rientrano. Foglio `simulazione_eventi_quartieri.xlsx`.

| Pagine QN (89) per eventi futuri | oggi | A | B | C |
|---|---|---|---|---|
| nessuno | 25 | 20 | 19 | 19 |
| 1-4 | 30 | 28 | 22 | 25 |
| 5-9 | 8 | 9 | 14 | 11 |
| 10 o più | 26 | 32 | 34 | 34 |

Lettura: **il buco non si chiude**. Gli enti del terzo settore stanno dove stanno gli altri
eventi: Municipio I e II, Esquilino, Centro storico, Parioli; la sede è spesso quella legale,
non il luogo delle attività. Anche nello scenario più largo restano a zero 19 pagine, tutte di
periferia o di frontiera (Balduina, Boccea, Bufalotta, Casal Lumbroso, Colle Prenestino,
Dragona-Dragoncello, Giardino di Roma, Infernetto, La Rustica, Morena, Muratella, Olgiata,
Pisana, Romanina, Tor Bella Monaca, Torraccia, Trigoria, Vigna Clara, Vitinia). Per quelle
pagine le fonti utili sono quelle mirate del §1 bis (parrocchie, centri anziani, comitati,
biblioteche, scuole), che non pubblicano calendari leggibili: servono la segnalazione in
entrata e il contatto diretto (passo L di `FLUSSO_EVENTI_A_Z.md`), non altra lettura automatica.

## 1 quinquies. Ricerca «evento / eventi / festa + quartiere» (M, 24 ottobre 2026)

288 ricerche Google (tre forme per ognuno dei 96 nomi delle 89 pagine QN; i nomi doppi, come
Dragona-Dragoncello, cercati separatamente), 6.266 risultati, 1.380 fonti distinte. Ogni fonte è
classificata (già nota, aggregatore, testata, commerciale, istituzionale, social, sito); i siti
nuovi sono letti rispettando il robots.txt, le pagine Facebook nuove con il lettore degli eventi
futuri. Esito nel foglio `fonti_ricerca_quartieri.xlsx` su Drive. Costo Apify 1,7 dollari.

| Esito | Fonti |
|---|---|
| Già note (registro, censimenti, wiki) | 182 |
| Aggregatori, testate e blog (non letti: licenza o natura di notizia) | 206, più 58 riconosciuti alla lettura |
| Servizi commerciali (sale feste, catering, location) | 143 |
| Gruppi Facebook (non leggibili) e profili Instagram (da valutare a mano) | 97 e 108 |
| Pagine Facebook nuove | 181, di cui 4 con eventi futuri |
| Siti nuovi letti | 449: 415 letti, 27 non raggiungibili, 7 vietati dal robots.txt; 74 risultati fuori Roma |
| **Candidate nel registro v4** | **129** (date future sul sito 71, pagina eventi 49, eventi strutturati 5, eventi futuri su Facebook 4); 119 con pagina QN, 61 su pagine deboli, 35 pagine deboli toccate |

Eventi nuovi: 96 (18 strutturati, 75 blocchi di testo con data, 3 Facebook); solo 14 hanno una
pagina QN con prove sufficienti (indirizzo della fonte per gli eventi strutturati, un luogo del
gazetteer nel testo per i blocchi), gli altri stanno in «senza quartiere». Le pagine a zero restano
25. Lettura: la ricerca per quartiere trova **fonti** (parrocchie, centri di iniziativa popolare,
associazioni, festival di quartiere) più che **eventi**: le fonti di periferia pubblicano poco e
male, e vanno lette nel tempo o contattate (passo L del flusso).

## 1 sexies. Eventi dentro i post Facebook delle fonti (M, 25 ottobre 2026)

Gli ultimi 15 post (dal 10 settembre) di ogni pagina Facebook salvata, letti per capire quanto
annunciano le fonti fuori dagli eventi Facebook. Primo giro: i post dei censimenti, già letti
(costo nei §1 ter e §2), e le 220 pagine verificate dall'owner (5,5 dollari). Secondo giro: le
662 pagine salvate e mai lette (fonti mirate e ricerca per quartiere nel registro v4, pagine
«rientra» o «da verificare» dei censimenti, pagine nuove della ricerca), 657 lette, 12,4 dollari
approvati dall'owner oltre il tetto del mese. Un post vale come annuncio se ha parole da evento
e una data futura (anche relativa al giorno del post, o un giorno della settimana ricorrente);
sono scartati resoconti senza data futura, bandi, scadenze, dirette, promozioni commerciali,
scioperi e atti parlamentari, orari d'apertura, e gli appuntamenti fuori Roma (città italiane e
comuni della provincia, anche scritti in maiuscolo).

| Lotto | Pagine | Post letti | Post con un annuncio |
|---|---|---|---|
| Censimento RUNTS | 2.391 | 8.710 | 1.959 |
| Censimento associazioni | 716 | 2.069 | 466 |
| Pagine verificate dall'owner | 213 | 615 | 247 |
| Secondo giro: fonti mirate e ricerca per quartiere (registro v4) | 195 | 817 | 224 |
| Secondo giro: censimento associazioni | 161 | 448 | 101 |
| Secondo giro: censimento RUNTS | 136 | 80 | 11 |
| Secondo giro: pagine nuove della ricerca per quartiere | 164 | 572 | 152 |
| **Totale** | **3.977** | **13.311** | **3.160** |

Annunci distinti 2.971; futuri dal 25 ottobre 888 (124 ricorrenti), da 555 pagine; con pagina QN
559 su 71 pagine QN. Il secondo giro aggiunge 187 annunci futuri, 92 con pagina QN.

La pagina QN di un annuncio viene, in quest'ordine, da un luogo del gazetteer nominato nel post
(nomi di strada esclusi: 92), dalla sede della fonte (417) o, per le fonti trovate cercando un
quartiere, dal quartiere solo se il nome della fonte o il post lo nominano (50). La zona della
ricerca da sola non basta: assegnava al quartiere cercato anche pagine di un Municipio intero,
testate di Roma Nord, una televisione nazionale e una sagra di Cervara di Roma. Con questa regola
Boccea torna a zero: i suoi eventi venivano da una pagina di notizie di Roma Nord e ora stanno a
Prati e a Roma Nord.

Nella pagina degli eventi di quartiere entrano 866 annunci (gli altri sono doppioni di eventi già
noti o senza titolo): sono la prima fonte, 38% dei 2.269 eventi futuri, davanti agli eventi
Facebook (28%), culture.roma.it (16%), i siti delle fonti (15%) e Roma Today (4%). Le pagine QN a
zero scendono da 25 a 10: Boccea, Bufalotta, Casal Lumbroso, Colle Prenestino, La Rustica,
Lunghezza, Morena, Muratella, Tor Cervara, Vitinia. Escono dallo zero, fra le altre, Balduina,
Giardino di Roma, Olgiata, Pisana, Romanina, Trigoria e Vigna Clara.

Precisione su due campioni di 30 annunci futuri (uno per giro, dopo i filtri): circa tre su
quattro sono appuntamenti veri a Roma con la data giusta; il resto sono resoconti con una data
citata, programmi televisivi o radiofonici, fiere professionali e avvisi di servizio. Gli
annunci restano candidati «da verificare» (passo di verifica del flusso, `FLUSSO_EVENTI_A_Z.md`).
Lettura: le fonti piccole (comitati, biblioteche, parrocchie) annunciano nei post, non negli
eventi Facebook. Il Comitato Acilia Nord ha zero eventi Facebook e un incontro settimanale in
sede nei post. Le pagine trovate con la ricerca rendono meno di quelle dei censimenti: molte
sono testate, servizi commerciali o pagine nazionali.

## 1 septies. Eventi contro abitanti per pagina QN (M, 25 ottobre 2026)

A grandi numeri: quali pagine hanno meno eventi di quanti ne giustificherebbero i loro abitanti.
Esito nel foglio `eventi_per_abitanti.xlsx` su Drive.

**Abitanti.** Griglia statistica di Roma Capitale sul geoportale (celle di 1 km con il numero di
abitanti, 2,82 milioni in tutto). Ogni cella è divisa in 25 punti; ogni punto va nella sua zona
urbanistica ufficiale (155) e poi alla pagina del toponimo del gazetteer più vicino fra quelli di
quella zona. Il totale per zona urbanistica coincide con il dato del gazetteer (rapporto mediano
0,96); la divisione di una zona fra più pagine è una stima. La popolazione del gazetteer da sola
non bastava: copre 1,85 milioni di abitanti e lascia 25 pagine vuote.

**Eventi.** Gli eventi futuri noti al 25 ottobre. Il controllo ha trovato 85 eventi fuori Roma
nella pagina degli eventi di quartiere (un sito di fonte che riporta un widget di eventi negli
Stati Uniti, eventi Fever all'estero): tolti, gli eventi sono 2.184. La pagina pubblicata
assegna i punti con le suddivisioni toponomastiche, che accorpano quartieri diversi (San Giovanni
nel Tuscolano, Centocelle nel Prenestino, Tor Bella Monaca in Torre Angela); per il confronto gli
eventi con coordinate, o con la sede della fonte geolocalizzata, sono riassegnati con la stessa
geografia degli abitanti (1.659 eventi con pagina invece di 1.532).

**Riferimento.** Le pagine fuori dal centro (escluso il Municipio I e Parioli-Flaminio) con almeno
5.000 abitanti: la mediana fa 2,4 eventi ogni 10.000 abitanti, il quartile alto («quartiere
attivo») 4,5. Centro Storico, Esquilino, Testaccio, Trastevere e Parioli-Flaminio ne fanno 33-48. Per Municipio i più bassi sono XV (1,5), VI (1,9), XIV
(2,0), III (2,2) e IX (2,4).

| Pagina | Abitanti (stima) | Eventi | Ogni 10.000 | Mancanti per «quartiere attivo» | Fonti note |
|---|---|---|---|---|---|
| Morena (VII) | 82.000 | 6 | 0,7 | 31 | 5 |
| Ponte di Nona (VI) | 53.000 | 3 | 0,6 | 21 | 12 |
| Monte Mario (XIV) | 51.000 | 4 | 0,8 | 19 | 40 |
| Borghesiana (VI) | 49.000 | 6 | 1,2 | 16 | 22 |
| Tor Vergata (VI) | 47.000 | 7 | 1,5 | 14 | 19 |
| Bufalotta (III) | 31.000 | 0 | 0 | 14 | 6 |
| Ostia (X) | 106.000 | 35 | 3,3 | 13 | 9 |
| Laurentino (IX) | 48.000 | 9 | 1,9 | 13 | 7 |
| Cinecittà (VII) | 72.000 | 21 | 2,9 | 12 | 29 |
| Montesacro (III) | 101.000 | 35 | 3,5 | 11 | 56 |
| Selva Candida, Torrino, Fidene-Settebagni | 36.000-38.000 ciascuna | 5-6 | 1,4-1,6 | 11 ciascuna | 13-24 |

Per portare ogni pagina al livello «quartiere attivo» mancano circa 450 eventi nel calendario
noto, circa 130 per arrivare alla mediana. Le pagine sotto il livello sono di due tipi: con poche
fonti note (Morena, Bufalotta, Colle Prenestino, Dragona-Dragoncello, Laurentino, Infernetto,
Ostia), dove servono fonti nuove; con molte fonti ma pochi eventi (Monte Mario, Ardeatino,
Tuscolano, Prenestino), dove le fonti ci sono e vanno lette più spesso o contattate (passo L del
flusso). Le fonti note sono contate con la geografia della wiki, quindi sono indicative.

## 1 octies. Lista supplementare per le 41 pagine deboli (M, 25 ottobre 2026)

Per le 41 pagine sotto la mediana di eventi ogni 10.000 abitanti (§1 septies): associazioni,
parrocchie, comitati, centri anziani e culturali con sede nella pagina, cercati in sei fonti.
Esito nel foglio `lista_supplementare_quartieri_deboli.xlsx` su Drive (con telefoni ed email, che
qui non stanno: DEC-109).

| Fonte | Soggetti nelle pagine deboli |
|---|---|
| Google Maps («associazione», «centro anziani», «comitato di quartiere», «centro culturale», «parrocchia» + toponimo, 69 punti) | 611, tolte le attività commerciali |
| OpenStreetMap (luoghi di culto, centri sociali, culturali e per anziani, associazioni, circoli, scout, biblioteche, teatri) | 415 |
| Albo della cittadinanza attiva di Roma Capitale | 31 |
| Ricerca Google «"comitato di quartiere" / associazione + toponimo» (207 toponimi) | 311 risultati utili |
| Annuario della Diocesi di Roma | 22 schede: il sito chiede un captcha dopo poche pagine e la lettura si è fermata lì |
| Albi e registri delle associazioni dei Municipi III, IV e VII (PDF) | 167 nomi, quasi tutti senza indirizzo: restano un elenco da incrociare |

Uniti i doppioni (stesso sito, stessa pagina Facebook, nome simile a meno di 250 m): 1.153
soggetti, 847 enti nuovi rispetto a wiki, registro v4 e censimento RUNTS (233 parrocchie e
chiese, 190 associazioni, 186 realtà sportive, 83 luoghi culturali, 65 comitati di quartiere o
civici, 61 centri anziani o sociali); 412 con telefono, 319 con sito, 219 con pagina Facebook.
676 entrano nel **registro fonti v5** come candidate (FE-0945…FE-1620; le realtà sportive e
religiose solo con eventi trovati o un canale da leggere); la wiki è rigenerata: 5.099 fonti,
1.606 nel registro.

Letti i siti dei nuovi (336 su 385, robots.txt rispettato; 83 con date future) e i post Facebook
delle loro 227 pagine (116 con post dal 10 settembre): 89 eventi futuri dopo gli stessi filtri
dell'estrattore dei post, 88 entrati nella pagina degli eventi di quartiere. Pagine QN a zero
nella pagina pubblicata: da 10 a 5 (Casal Lumbroso, La Rustica, Lunghezza, Muratella, Vitinia).
Con la geografia degli abitanti, eventi ogni 10.000 abitanti: Laurentino da 1,9 a 3,9,
Bufalotta da 0 a 2,6, Primavalle da 2,4 a 4,5, Tor Vergata da 1,5 a 2,6; Morena (0,9), Ponte di
Nona (0,8), Monte Mario (1,0) e Ardeatino (0,7) restano molto sotto anche con molte più fonti
note (Morena da 5 a 38): lì le fonti ci sono, gli eventi vanno chiesti o letti nel tempo (passo L
del flusso). Eventi che mancano per portare ogni pagina al livello «quartiere attivo»: da circa
450 a circa 380. Costo Apify della lista: circa 16 dollari (Google Maps 8,1, post Facebook 7,3,
ricerca Google 0,9).

## 1 nonies. Promotori degli eventi, categorie, ricerche integrative, immagini e diffusione (M, 25 ottobre 2026)

**Promotori.** Chi organizza i 2.384 eventi futuri della pagina degli eventi di quartiere: host degli
eventi Facebook (con il link alla pagina), pagina che annuncia nel post, «a cura di» di culture.roma.it, la
sede per l'agenda delle Biblioteche di Roma, la fonte per i siti; i co-organizzatori sono separati. 1.206 promotori; per 908 c'è un'email
(75%), per 862 un sito, per 1.122 una pagina Facebook, per 707 un profilo
Instagram, per 635 un telefono. Dati da: profili Facebook già letti nei censimenti e 425 letti ora,
RUNTS, censimento associazioni, lista supplementare, contatti per evento di culture.roma.it, siti dei
promotori letti ora (homepage, contatti, chi siamo, note legali; robots.txt rispettato) e una ricerca Google
dei canali per chi non ne aveva. Ogni promotore ha una categoria, un ambito, le attività prevalenti, una
descrizione breve scritta da regole con le nostre etichette e una descrizione lunga che aggiunge, tra
virgolette, come il soggetto si presenta. Il foglio completo (`promotori_eventi.xlsx`) sta su Drive; la wiki
ha la pagina generata `docs/wiki/fonti-eventi/promotori.md` con categoria, descrizione breve, canali, se
esiste un contatto e la posizione sulla diffusione, senza email, telefoni né testi delle fonti (DEC-102,
DEC-109; test T-FE-10).

**Geografia.** Dal 25 ottobre, per decisione dell'owner, la pagina pubblicata usa la geografia delle zone
urbanistiche, la stessa degli abitanti (§1 septies): un evento con coordinate va nella pagina del toponimo
del gazetteer più vicino dentro la sua zona urbanistica ufficiale. Cambiano pagina 410 eventi su 2.384;
quelli con una pagina QN sono 1.866 (1.700 con le suddivisioni toponomastiche), le pagine con 10 o più eventi
46 (38), quelle a zero 5 (La Rustica, La Storta, Lunghezza, Marcigliana, Vitinia). Le quote qui sotto usano questa geografia. È la
geografia dell'anteprima: quella di produzione resta il pacchetto Metodo QN (`tools/geo-assign/qngeo.py punto`).

| Categoria | Promotori | Eventi | Quota nelle 41 pagine deboli |
|---|---|---|---|
| Associazioni culturali e artistiche | 273 | 544 | 10% |
| Terzo settore sociale e sanitario | 160 | 254 | 10% |
| Teatri, cinema e spazi di spettacolo | 76 | 251 | 10% |
| Istituzioni pubbliche | 69 | 242 | 13% |
| Grandi istituzioni culturali e fondazioni | 32 | 197 | 2% |
| Persone (artisti, autori, guide) | 135 | 158 | 8% |
| Non classificato | 92 | 140 | 9% |
| Intermediari: biglietterie, aggregatori e media | 36 | 115 | 3% |
| Turismo e visite guidate | 53 | 104 | 7% |
| Sport e movimento | 63 | 87 | 28% |
| Parrocchie e realtà religiose | 42 | 71 | 45% |
| Scuole, università e formazione | 43 | 70 | 9% |
| Musei, gallerie e spazi espositivi | 20 | 59 | 0% |
| Locali e attività commerciali | 39 | 56 | 9% |
| Centri sociali, centri anziani e spazi di comunità | 15 | 43 | 9% |
| Comitati di quartiere e reti civiche | 24 | 40 | 25% |
| Ambiente, natura e animali | 27 | 39 | 8% |
| Politica e sindacati | 7 | 10 | 0% |

**Lettura per categoria.** Quota degli eventi di ogni categoria che cade nelle 41 pagine deboli:
le più legate alle periferie sono parrocchie e realtà religiose (45%), sport e movimento (28%), comitati di quartiere e reti civiche (25%); le meno musei, gallerie e spazi espositivi (0%), grandi istituzioni culturali e fondazioni (2%), intermediari: biglietterie, aggregatori e media (3%). Nelle 41 pagine deboli la lista supplementare (§1 octies) ha trovato 283 parrocchie e realtà religiose, 397 associazioni, 196 realtà sportive, 98 comitati, 73 centri anziani o sociali; i promotori di quelle categorie con almeno un evento nel calendario in quelle pagine sono 21 (7%), 38 (10%), 21 (11%), 9 (9%), 2 (3%). Il buco non è di soggetti: è di eventi che arrivano online.

**Ricerche integrative** (spesa massima approvata 25 dollari):

| Idea | Stato | Costo | Esito |
|---|---|---|---|
| Agenda delle Biblioteche di Roma (news dell'OPAC, eventi schema.org per sede) | eseguita | 0 $ (lettura del sito, una richiesta al secondo; il sito non ha robots.txt) | 110 eventi futuri nella pagina, 15 nelle 41 pagine deboli, da 30 sedi |
| Eventi futuri delle pagine Facebook mai lette (lista supplementare e promotori) | eseguita | 0,14 $ | lette tutte le 226 pagine della lista supplementare e 13 delle 384 dei promotori (lettura interrotta: circa 5 pagine al minuto, e i promotori sono già nel calendario); 36 eventi letti, 32 futuri a Roma: 2 dalle 226 pagine dei quartieri deboli, 30 dalle 13 dei promotori; 30 entrati nella pagina dopo filtri e doppioni. Conferma che i piccoli soggetti annunciano nei post, non negli eventi Facebook |
| Profili Facebook dei promotori senza dati (descrizione, email, sito, Instagram) | eseguita | 3,51 $ | 425 profili letti: 367 con email, 403 con descrizione |
| Ricerca Google dei canali per i promotori senza sito né Facebook | eseguita | 0,39 $ | canali trovati per 56 promotori: 45 siti, 34 pagine Facebook, 27 Instagram |
| Eventi dei Municipi su comune.roma.it | provata e scartata | 0 $ | Municipi VI e VII: 11 eventi in elenco, quasi tutti dell'estate e in parte già noti; l'elenco non è un calendario aggiornato |
| Calendario delle gare podistiche (calendariopodismo.it, pagina Lazio) | provata e scartata | 0 $ (4 pagine dell'elenco; robots.txt aperto) | 98 gare nel Lazio fino a dicembre, 7 a Roma e quasi tutte grandi corse del centro già note; per le periferie meglio i calendari delle società e dei comitati (UISP, CSI) |
| Bollettini e avvisi parrocchiali (pagine avvisi dei siti, foglio domenicale in PDF) | proposta | 0 $ (lettura dei siti e dei PDF; da scrivere un lettore di PDF) | — |
| Calendario della Diocesi di Roma (sito con calendario eventi) | proposta | 0 $ | il sito chiede un captcha dopo poche richieste: va chiesto alla Diocesi un feed o un permesso di lettura |
| Calendari dei tornei e delle gare delle società (UISP Roma, CSI Roma) | proposta | 0-1 $ | — |
| Centri anziani e centri sociali | proposta (contatto, non ricerca) | 0 $ | contatto diretto con i telefoni della lista supplementare o con l'ufficio centri anziani di ogni Municipio |
| Gruppi Facebook di quartiere («Sei di … se») | proposta (manuale) | 0 $ | non leggibili in automatico (gruppi chiusi): iscrizione della redazione e lettura settimanale |
| Instagram dei promotori senza eventi su Facebook | proposta | 2-5 $ per un giro | resa attesa bassa nelle pagine deboli: da fare dopo i bollettini parrocchiali |

**Correzioni alla lista supplementare.** Un post pubblicato da una pagina diversa dal soggetto non prende
più la zona della sede del soggetto, e i post di pagine non collegate a un soggetto della lista
supplementare sono scartati. Il lettore dei siti aveva seguito come «sito» di un soggetto un articolo di
Roma Today e ne aveva letto anche la home e la pagina degli eventi: contro DEC-026, che fuori dalla lettura
una tantum del 23 ottobre non ammette letture di Roma Today. I tre blocchi datati presi da lì sono tolti
dalla pagina e dal foglio della lista supplementare, e Roma Today è escluso nel lettore dei siti, nel lettore della lista
supplementare e nella raccolta degli eventi. Gli eventi della lista supplementare nella pagina sono ora
83 (88 nel §1 octies).

**Immagini (DEC-101).** Per ogni evento della pagina l'immagine della fonte è scaricata una volta e
salvata a risoluzione da card (lato lungo 800 px), con `source_image_url`, `image_fetched_at`,
`image_local_path`, `image_credit` e `image_removed`: 1.978 immagini. Non scaricate: Roma Today
(licenza Citynews, DEC-026), eventi Fever (asset commerciali), blocchi di testo dei siti senza pagina
dell'evento; 189 eventi non hanno immagine alla fonte. Archivio e manifest su Drive
(`immagini_eventi.zip`, `immagini_eventi_manifest.xlsx`), mai nel repository.

**Diffusione.** Posizione di ogni fonte sui propri contenuti, dal sito (note legali, termini, piè di
pagina, robots.txt, riserva di estrazione TDM) o dai termini della piattaforma:

| Posizione | Promotori | Eventi (posizione più restrittiva fra i promotori dell'evento) |
|---|---|---|
| riproduzione vietata | 5 | 36 |
| raccolta automatica vietata | 2 | 2 |
| licenza richiesta | 0 | 0 |
| termini della piattaforma | 377 | 490 |
| diritti riservati (generico) | 463 | 964 |
| licenza aperta | 10 | 13 |
| nessuna indicazione | 329 | 785 |
| non verificabile | 20 | 15 |

Gli stessi eventi per canale da cui li leggiamo (la posizione del canale vale anche quando il promotore non dice nulla):

| Canale | Posizione | Eventi |
|---|---|---|
| Facebook (termini di Meta) | termini della piattaforma | 1536 |
| culture.roma.it (Roma Capitale) | diritti riservati (generico) | 356 |
| siti delle fonti | diritti riservati (generico) | 144 |
| siti delle fonti | nessuna indicazione | 136 |
| Biblioteche di Roma | nessuna indicazione | 110 |
| Roma Today (Citynews) | licenza richiesta | 82 |
| siti delle fonti | non verificabile | 14 |
| siti delle fonti | riproduzione vietata | 4 |
| siti delle fonti | licenza aperta | 2 |

Vietano esplicitamente la riproduzione dei contenuti: Romaeuropa Festival (26 eventi), Teatro Degli Audaci (6 eventi), VignaClaraBlog.it Il primo quotidiano on line di Roma Nord (2 eventi), Indipendente Concerti (1 evento), Azione Cattolica Italiana (1 evento)
(clausole rilette una per una: Romaeuropa non consente di usare contenuti e marchi del sito per scopi diversi da quelli del sito; il Teatro degli Audaci vieta riproduzione e diffusione senza autorizzazione scritta, ma ammette un estratto fino al 15% del testo con link all'originale e nome dell'autore; VignaClaraBlog vieta la riproduzione anche parziale senza approvazione scritta; il sito di riferimento è quello di Live Nation, i cui termini vietano di copiare o distribuire parti del sito senza autorizzazione scritta; Azione Cattolica consente solo usi personali dei contenuti).
Vietano la raccolta automatica (termini o robots.txt): Intersos Lab, Le Nuove Chimere CooperativaSociale. Facebook e Instagram
(termini di Meta: raccolta automatica vietata senza permesso) portano 1.536 eventi su 2.384; Roma Today
richiede licenza (DEC-026); le note legali di Roma Capitale (anche per culture.roma.it) riservano i diritti
sui contenuti senza licenza di riuso; il sito delle Biblioteche di Roma non dice nulla sui contenuti (il suo
«copyright» riguarda il software del catalogo). Nessuna delle clausole lette vieta di dare notizia di un evento: i fatti (cosa,
quando, dove, chi) non sono protetti; lo sono testi e immagini, e la banca dati contro estrazioni
sistematiche. Conseguenza operativa, già nelle regole: scriviamo i nostri testi con credito e link
(DEC-102), e per le fonti che vietano la riproduzione si usa la card generata invece dell'immagine
(DEC-101); la posizione sulla raccolta automatica di Facebook resta quella di DEC-102.

## 2. Cosa ha detto il censimento delle pagine Facebook (M)

| Misura | Pagine |
|---|---|
| Pagine fornite | 1.169 |
| Lette (dati di pagina) | 1.131; non disponibili 37; non restituite 1 |
| Con eventi futuri su Facebook | 19 (60 eventi, 42 a Roma) — verificato con un secondo lettore su 12 pagine grandi: solo eventi passati |
| Con post negli ultimi sei mesi (lette 734 pagine senza eventi futuri) | 335; di cui 186 con almeno un post datato che annuncia un evento |
| Con un sito | 823; raggiungibili 602; con sezione eventi 277; con date future leggibili 83; con date negli ultimi sei mesi 178 |
| Con Municipio assegnato | 787 (indirizzo Facebook 778, geocodifica OSM 31, coordinate degli eventi 3); con pagina QN 672 |
| Verdetto «rientra» | 390 (eventi futuri FB 11 · calendario sul sito 57 · date recenti sul sito 81 · pagina eventi sul sito 103 · annunci nei post 138) |
| «locale» (attività commerciali) | 54 · «da valutare» 157 (24 politiche) · «attiva senza annunci» 110 · dormienti 275 · servizi/tematiche/fuori Roma/non disponibili 182 |

Lettura: queste associazioni **non usano gli eventi Facebook**; annunciano nei post o sul
sito. La prova di attività più economica e più affidabile è il sito (sezione eventi), la
seconda sono i post. Il lettore di eventi Facebook per pagina costa 0,18 $ per 1.169 pagine
e serve come controllo, non come scoperta.

## 3. Cosa ha detto la ricerca uno a uno dei 176 eventi senza fonte (M)

168 schede Roma Today, 7 culture.roma.it, 1 Facebook. Una ricerca Google per evento (titolo
+ luogo + Roma), esclusi gli aggregatori noti, i primi tre candidati letti e confermati se
almeno il 60% delle parole del titolo compare nella pagina.

| Esito | Eventi |
|---|---|
| Nessuna pagina non-aggregatore che citi l'evento | 127 |
| Sito terzo da verificare a mano | 30 |
| Menzione di terzi (stampa, blog, cataloghi editoriali) | 8 |
| Altro aggregatore con scheda strutturata | 7 |
| Fonte primaria probabile (sito del luogo o dell'ente) | 4 |

Secondo passaggio, nell'ordine giusto: per i 132 eventi il cui luogo è nel registro, il
sito del luogo (la pagina già letta dal lettore dei siti, altrimenti la pagina da
controllare dello schedario) è stato cercato per le parole del titolo: 26 eventi ritrovati
sul sito del luogo (musei civici, Colosseo, MACRO, Villa Giulia, Palazzo Bonaparte), contro
i 4 della ricerca web. Esito finale: 30 con fonte diretta (`link_fonte_diretta` compilato
nel foglio unificato, metodo in `fonte_diretta_metodo`), 27 con un sito terzo da verificare a
mano, 81 con il luogo noto ma l'evento assente dal suo sito, 37 senza luogo noto né traccia.

Conferma la lettura del 23 ottobre: per queste schede la fonte primaria di norma **non
esiste sul web** come pagina dell'evento; l'organizzatore comunica per comunicato stampa, pagina
Facebook (post) o non comunica affatto. La ricerca ha anche censito gli altri aggregatori
che Google propone per Roma (spotlightapp.eu, vibeloop.it, eventivicino.it, araundapp.it,
roma-o-matic.com, estateromana.com, bibliotechediroma.it): due sono fonti istituzionali da
aggiungere al registro (Estate Romana, Biblioteche di Roma), gli altri sono aggregatori da
valutare per licenza prima di ogni lettura.

## 4. Flusso continuo proposto (per canale)

| Canale | Come | Cadenza | Costo (S) | Stato |
|---|---|---|---|---|
| Siti delle fonti (809 con un sito, 277 con sezione eventi) | `tools/fonti/leggi_eventi_siti.py` sullo schedario; schema.org Event come prova forte, date nel testo come candidati; uscita fuori dal repository | settimanale | 0 $ | pronto; prima prova fatta (§4 bis) |
| culture.roma.it | `tools/fonti/leggi_culture_roma.py`: API WordPress (`event_calendar`, `modified_after`) letta per differenza, scheda letta per ogni voce nuova o modificata, stato in un file fuori dal repository | ogni 2 giorni | 0 $ | pronto e provato (§4 ter) |
| Facebook, pagine note | `unseenuser/fb-events` con `pageUrls` di tutte le pagine del registro e del censimento, `onlyUpcoming` | ogni 2 settimane | ~0,5 $ | provato il 24 ottobre; schedulazione dipende da DEC-024 Q3 |
| Facebook, scoperta | lettura per parole chiave (89 nomi di pagina QN + termini generici); organizzatori nuovi → censimento | mensile | ~1 $ | provato il 24 ottobre: rende pochissimo (§5); da tenere solo come controllo |
| Facebook, post delle pagine | `apify/facebook-posts-scraper` sulle pagine «attive senza eventi» (10 post, ultimi 30 giorni) | mensile | ~3 $ | provato il 24 ottobre (2.985 post) |
| Roma Today | nessuna lettura regolare: robots.txt e licenza Citynews («nessun canale senza licenza») | — | — | chiuso salvo licenza |
| Il workflow n8n `scrape-fb-events-rome.json` | export nel repository: `active: false`, schedulazione ogni due notti alle 3 (`0 0 3 */2 * *`), ricerca «Italy Roma» con 200 eventi al massimo, scrittura in Firestore `roma-pipeline` / `facebook-posts` / `events` e nel foglio «QuartieriNews _ Events and Posts File»: nomi di produzione, nessun prefisso `staging_`; arricchimento con OpenAI. Sul conto Apify dell'organizzazione non c'è nessuna schedulazione né run precedente al 24 ottobre: se gira, gira dal vecchio conto. La ricerca «Italy Roma» è il canale che il 24 ottobre ha reso meno di tutti (§5) | — | — | da verificare dall'owner su n8n (gira? con quale conto?); sostituto candidato: lettura per pagine note |

Regola comune: ogni lettura produce righe con `fonte_id` dello schedario, così gli eventi
nuovi si contano per fonte e per pagina QN e la wiki si aggiorna dai conteggi, mai dai testi.

## 4 bis. Prima prova della lettura dei siti (M, 24 ottobre 2026)

`tools/fonti/leggi_eventi_siti.py` su tutte le fonti dello schedario con una pagina da
leggere, orizzonte 60 giorni, otto processi in parallelo per host diversi. Esito nel foglio
`eventi_siti_prova_2026-10-24.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Fonti con una pagina da leggere | 809; lette 675; non raggiungibili 137 |
| Fonti con eventi schema.org nei prossimi 60 giorni (prova forte) | 12, per 157 eventi (teatri e un paio di associazioni) |
| Fonti con date nel testo (candidati da leggere a mano) | 196, per 1.089 blocchi datati |
| Costo | 0 $ |

Lettura: i siti delle fonti romane raramente pubblicano eventi strutturati; la lettura
settimanale produce poche righe certe e molte righe candidate, che una persona (o un
passaggio di lettura con modello) deve confermare. Il valore della lettura automatica è
dire **quali** fonti hanno pubblicato qualcosa di datato questa settimana, non estrarne
la scheda. Dei 137 siti non raggiungibili, 61 sono domini che non esistono più (il nome non
si risolve: indirizzi vecchi lasciati sulle pagine Facebook), 26 chiudono la connessione, 23
hanno certificati non validi, 11 rispondono 403: da togliere o correggere nel registro, non
da riprovare.

## 4 ter. Prima lettura per differenza di culture.roma.it (M, 24 ottobre 2026)

`tools/fonti/leggi_culture_roma.py` dal punto zero del 20 ottobre (la lettura completa con
Apify). Esito nel foglio `culture_roma_delta_2026-10-24.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Schede modificate o pubblicate dal 20 ottobre | 74 (43 nuove, 31 modificate), tutte lette, 0 errori |
| Con date lette | 74; con fine da oggi in poi 72 |
| Con «a cura di» (organizzatore) | 69; con sito esterno 73; con coordinate 67; con Municipio 65 |
| Costo e tempo | 0 $; circa due minuti a una richiesta al secondo |

Lettura: quattro giorni di agenda valgono 43 schede nuove, cioè circa dieci al giorno, quasi
tutte con organizzatore e sito: è il canale a più alto rendimento per euro speso e il
primo da mettere in calendario. Gli organizzatori «a cura di» delle schede nuove sono il
modo naturale di scoprire fonti nuove (§5): entrano nel censimento come candidate.

## 5. Scoperta di organizzatori nuovi su Facebook per parole chiave (M)

Due lettori, stesso giorno: `unseenuser/fb-events` con 109 parole chiave (89 nomi di pagina
QN + 20 termini generici) e `apify/facebook-events-scraper` con 30 ricerche (lo stesso
meccanismo del workflow n8n di produzione, che usa «Italy Roma»), 150 eventi al massimo per
ricerca. Esito nel foglio `facebook_scoperta_organizzatori.xlsx` su Drive.

| Misura | Valore |
|---|---|
| Eventi futuri distinti trovati (i due lettori insieme) | 95 |
| A Roma (Municipio assegnato dalle coordinate) | 60; con pagina QN 49; zone QN toccate 21 |
| Organizzatori distinti | 99; nuovi rispetto allo schedario 75; nuovi con almeno due eventi a Roma 0 |
| Costo | 0,19 $ + 0,98 $ |

Lettura: **la ricerca per parole chiave su Facebook non scopre quasi nulla**. Il motore di
ricerca eventi di Facebook risponde con poche decine di risultati per termine, molti passati
o fuori Roma; con 139 ricerche si trovano 60 eventi romani, cioè meno di quanti ne produce
in un mese una sola fonte media del registro. Lo stesso vale per la pagina «eventi della
città» (3 risultati). Per la scoperta di organizzatori nuovi restano tre strade che
funzionano: gli organizzatori citati dagli eventi già letti (culture.roma.it «a cura di»,
host degli eventi Facebook delle pagine note), gli elenchi istituzionali (albo delle
associazioni dei Municipi, Biblioteche di Roma, Estate Romana) e le liste raccolte a mano
dall'owner come quella del 24 ottobre. Il workflow n8n di produzione, che si affida alla
ricerca «Italy Roma», va considerato un canale debole: conferma, non scoperta.

## 6. Problemi rilevati

1. **Facebook eventi ≠ attività.** Il verdetto «dormiente» basato sui soli eventi Facebook
   avrebbe scartato 186 pagine attive: la lettura dei post ha corretto il tiro. Ogni
   giudizio di attività deve usare almeno due segnali (sito, post, eventi).
2. **Gli aggregatori si copiano.** La ricerca Google per evento restituisce quasi solo altri
   aggregatori; la rintracciabilità alla fonte non migliora cercando di più, migliora solo
   leggendo prima la fonte (sito, pagina Facebook dell'organizzatore).
3. **Identità delle fonti.** 72 candidate del censimento coincidono con voci del registro
   per URL Facebook; altre coincidono per nome con grafie diverse e restano doppie finché
   una persona non le fonde (regola della wiki: le fusioni dubbie non si fanno). La wiki
   genera ora `fusioni-proposte.md`: 85 coppie da decidere.
4. **Geografia dai soli indirizzi Facebook.** 778 pagine hanno coordinate da Facebook, ma
   l'indirizzo di una pagina è la sede, non il luogo degli eventi; per 3 pagine la geografia
   viene dagli eventi. Il Metodo QN (`tools/geo-assign/qngeo.py punto`) non è stato usato
   perché il pacchetto cartografico sta su Drive (`_ZZ Metodo QN`) e non nel repository:
   portarlo nell'ambiente è il passo per rendere la geografia degli eventi uguale a quella
   delle notizie.
5. **Doppioni.** 132 gruppi, 324 righe secondarie con la regola proposta (DEC-025 a): contando
   solo le righe principali le pagine QN con almeno dieci eventi futuri scendono da 23 a 20.

## 7. Prossimi passi, in ordine

1. Owner: DEC-023, DEC-024, DEC-025, DEC-026; verificare su n8n se il workflow Facebook gira
   e con quale conto Apify.
2. Decidere le candidate del registro v2 (445 della ricerca mirata, 598 del censimento)
   secondo DEC-024 Q1; aggiungere Estate Romana come fonte istituzionale.
3. Mettere in calendario la lettura settimanale dei siti (§4) e misurare per quattro settimane
   quante fonti producono davvero; poi rileggere le candidate «pagina eventi senza date».
4. Scrivere la lettura per differenza di culture.roma.it.
5. Portare il pacchetto Metodo QN nell'ambiente e riassegnare la geografia degli eventi con
   `qngeo.py punto`.
6. Rimisurare a fine novembre: eventi futuri per pagina QN con le sole righe principali.
7. Promotori (§1 nonies): per le fonti che vietano la riproduzione usare la card generata e i
   nostri testi; prossime ricerche gratuite: calendari dei tornei delle società (UISP, CSI) e
   bollettini parrocchiali; per i centri anziani, contatto diretto.

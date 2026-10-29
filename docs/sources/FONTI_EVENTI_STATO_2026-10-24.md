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

**Promotori.** Chi organizza i 2.585 eventi futuri della pagina degli eventi di quartiere: host degli
eventi Facebook (con il link alla pagina), pagina che annuncia nel post, «a cura di» di culture.roma.it, la
sede per l'agenda delle Biblioteche di Roma, la fonte per i siti; i co-organizzatori sono separati. 1.246 promotori; per 938 c'è un'email
(75%), per 898 un sito, per 1.157 una pagina Facebook, per 732 un profilo
Instagram, per 657 un telefono. Dati da: profili Facebook già letti nei censimenti e 425 letti ora,
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
del gazetteer più vicino dentro la sua zona urbanistica ufficiale. Cambiano pagina 457 eventi su 2.585;
quelli con una pagina QN sono 2.100 (1.942 con le suddivisioni toponomastiche), le pagine con 10 o più eventi
49 (41), quelle a zero 5 (La Rustica, La Storta, Lunghezza, Marcigliana, Vitinia). Le quote qui sotto usano questa geografia. È la
geografia dell'anteprima: quella di produzione resta il pacchetto Metodo QN (`tools/geo-assign/qngeo.py punto`).

| Categoria | Promotori | Eventi | Quota nelle 41 pagine deboli |
|---|---|---|---|
| Associazioni culturali e artistiche | 286 | 606 | 10% |
| Istituzioni pubbliche | 74 | 295 | 11% |
| Teatri, cinema e spazi di spettacolo | 79 | 272 | 12% |
| Terzo settore sociale e sanitario | 168 | 269 | 11% |
| Grandi istituzioni culturali e fondazioni | 34 | 207 | 2% |
| Non classificato | 95 | 158 | 9% |
| Persone (artisti, autori, guide) | 134 | 157 | 8% |
| Intermediari: biglietterie, aggregatori e media | 36 | 115 | 3% |
| Turismo e visite guidate | 53 | 114 | 6% |
| Sport e movimento | 63 | 87 | 28% |
| Parrocchie e realtà religiose | 45 | 76 | 43% |
| Scuole, università e formazione | 44 | 72 | 8% |
| Musei, gallerie e spazi espositivi | 21 | 64 | 0% |
| Locali e attività commerciali | 39 | 56 | 9% |
| Ambiente, natura e animali | 29 | 43 | 7% |
| Centri sociali, centri anziani e spazi di comunità | 15 | 43 | 12% |
| Comitati di quartiere e reti civiche | 24 | 42 | 24% |
| Politica e sindacati | 7 | 10 | 0% |

**Lettura per categoria.** Quota degli eventi di ogni categoria che cade nelle 41 pagine deboli:
le più legate alle periferie sono parrocchie e realtà religiose (43%), sport e movimento (28%), comitati di quartiere e reti civiche (24%); le meno musei, gallerie e spazi espositivi (0%), grandi istituzioni culturali e fondazioni (2%), intermediari: biglietterie, aggregatori e media (3%). Nelle 41 pagine deboli la lista supplementare (§1 octies) ha trovato 283 parrocchie e realtà religiose, 397 associazioni, 196 realtà sportive, 98 comitati, 73 centri anziani o sociali; i promotori di quelle categorie con almeno un evento nel calendario in quelle pagine sono 22 (8%), 44 (11%), 21 (11%), 9 (9%), 3 (4%). Il buco non è di soggetti: è di eventi che arrivano online.

**Ricerche integrative** (spesa massima approvata 25 dollari):

| Idea | Stato | Costo | Esito |
|---|---|---|---|
| Agenda delle Biblioteche di Roma (news dell'OPAC, eventi schema.org per sede) | eseguita | 0 $ (lettura del sito, una richiesta al secondo; il sito non ha robots.txt) | 110 eventi futuri nella pagina, 16 nelle 41 pagine deboli, da 30 sedi |
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
85 (88 nel §1 octies).

**Immagini (DEC-101).** Per ogni evento della pagina l'immagine della fonte è scaricata una volta e
salvata a risoluzione da card (lato lungo 800 px), con `source_image_url`, `image_fetched_at`,
`image_local_path`, `image_credit` e `image_removed`: 2.166 immagini. Non scaricate: Roma Today
(licenza Citynews, DEC-026), eventi Fever (asset commerciali), blocchi di testo dei siti senza pagina
dell'evento; 200 eventi non hanno immagine alla fonte. Archivio e manifest su Drive
(`immagini_eventi.zip`, `immagini_eventi_manifest.xlsx`), mai nel repository.

**Diffusione.** Posizione di ogni fonte sui propri contenuti, dal sito (note legali, termini, piè di
pagina, robots.txt, riserva di estrazione TDM) o dai termini della piattaforma:

| Posizione | Promotori | Eventi (posizione più restrittiva fra i promotori dell'evento) |
|---|---|---|
| riproduzione vietata | 6 | 37 |
| raccolta automatica vietata | 1 | 1 |
| licenza richiesta | 0 | 0 |
| termini della piattaforma | 394 | 513 |
| diritti riservati (generico) | 466 | 1029 |
| licenza aperta | 9 | 12 |
| nessuna indicazione | 331 | 839 |
| non verificabile | 39 | 80 |

Gli stessi eventi per canale da cui li leggiamo (la posizione del canale vale anche quando il promotore non dice nulla):

| Canale | Posizione | Eventi |
|---|---|---|
| Facebook (termini di Meta) | termini della piattaforma | 1576 |
| culture.roma.it (Roma Capitale) | diritti riservati (generico) | 356 |
| siti delle fonti | diritti riservati (generico) | 195 |
| siti delle fonti | nessuna indicazione | 180 |
| Biblioteche di Roma | nessuna indicazione | 110 |
| Roma Today (Citynews) | licenza richiesta | 82 |
| siti delle fonti | non verificabile | 79 |
| siti delle fonti | riproduzione vietata | 5 |
| siti delle fonti | licenza aperta | 2 |

Vietano esplicitamente la riproduzione dei contenuti: Romaeuropa Festival (26 eventi), Teatro Degli Audaci (6 eventi), VignaClaraBlog.it Il primo quotidiano on line di Roma Nord (2 eventi), Indipendente Concerti (1 evento), CREI Cooperativa Sociale — Interpretariato LIS, formazione e accessibilità (1 evento), Azione Cattolica Italiana (1 evento)
(clausole rilette una per una: Romaeuropa non consente di usare contenuti e marchi del sito per scopi diversi da quelli del sito; il Teatro degli Audaci vieta riproduzione e diffusione senza autorizzazione scritta, ma ammette un estratto fino al 15% del testo con link all'originale e nome dell'autore; VignaClaraBlog vieta la riproduzione anche parziale senza approvazione scritta; il sito di riferimento è quello di Live Nation, i cui termini vietano di copiare o distribuire parti del sito senza autorizzazione scritta; Azione Cattolica consente solo usi personali dei contenuti).
Vietano la raccolta automatica (termini o robots.txt): Intersos Lab. Facebook e Instagram
(termini di Meta: raccolta automatica vietata senza permesso) portano 1.576 eventi su 2.585; Roma Today
richiede licenza (DEC-026); le note legali di Roma Capitale (anche per culture.roma.it) riservano i diritti
sui contenuti senza licenza di riuso; il sito delle Biblioteche di Roma non dice nulla sui contenuti (il suo
«copyright» riguarda il software del catalogo). Nessuna delle clausole lette vieta di dare notizia di un evento: i fatti (cosa,
quando, dove, chi) non sono protetti; lo sono testi e immagini, e la banca dati contro estrazioni
sistematiche. Conseguenza operativa, già nelle regole: scriviamo i nostri testi con credito e link
(DEC-102), e per le fonti che vietano la riproduzione si usa la card generata invece dell'immagine
(DEC-101); la posizione sulla raccolta automatica di Facebook resta quella di DEC-102.

## 1 decies. Secondo giro di leve per aumentare gli eventi in tutte le pagine (M, 26 ottobre 2026)

Otto esploratori AI indipendenti hanno proposto 60 leve (dati già raccolti, categorie di fonti, feed e API, social, canali diretti, cadenza e conteggio, enti pubblici, estrazione con modelli). Ogni leva è passata da scettici che ne hanno ricontato la resa e controllato la liceità: le prime 30 con due verifiche ciascuna, le altre 30 con una verifica più leggera. Quasi tutte sono state ridimensionate, spesso di 2-5 volte. Le leve deterministiche migliori sono state eseguite subito, senza spesa Apify; la classifica completa è nel foglio `leve_eventi_2026-10-26.xlsx` su Drive.

**Risultato delle leve eseguite la mattina.** Eventi futuri nella pagina da 2.384 a 2.563, con pagina QN da 1.866 a 2.081; pagine con 10 o più eventi da 46 a 49; pagine a zero ferme a 5 (La Rustica, La Storta, Lunghezza, Marcigliana, Vitinia).

| Leva | Che cosa | Esito misurato |
|---|---|---|
| L18 | Feed iCal e REST di The Events Calendar (Tribe) sui siti WordPress delle fonti | 158 eventi letti da 28 siti con feed iCal o REST (41 host provati, robots.txt rispettato, campi di contatto scartati, serie contate una volta); 139 entrati nella pagina dopo i doppioni |
| L20 | iCal di Events Manager: Teatri in Comune (Tor Bella Monaca, Lido di Ostia, Villa Pamphilj, Quarticciolo) e altri siti con il plugin | Teatri in Comune (Tor Bella Monaca, Lido di Ostia, Villa Pamphilj, Quarticciolo): 53 eventi dal feed iCal, compresi nei 139; Ostia +20, Tor Bella Monaca +14 |
| L51 | Parchi e riserve: calendari WordPress con iCal di RomaNatura, Parco regionale dell'Appia Antica e Parco archeologico dell'Appia | RomaNatura: feed iCal e REST vuoti al 26 ottobre; i parchi con The Events Calendar sono compresi nella lettura dei feed |
| L08 | Correzioni deterministiche alle regole dei post (estrai.py/build.py): Unicode NFKC, ricorrenze, parola «online», post condivisi, anteprime, date parziali, vie di città | normalizzazione NFKC del testo dei post (grassetto matematico): annunci futuri da 888 a 930, nella pagina da 914 a 954 |
| L01 | Recupero della pagina QN per i 518 eventi senza pagina con regole sui dati già in casa | 11 eventi senza pagina assegnati per luogo già visto con una sola pagina |
| L02 | Geocodifica degli indirizzi stradali residui (Nominatim con cache o pacchetto Metodo QN) e scarto dei luoghi fuori Roma | 89 eventi senza pagina assegnati geocodificando l'indirizzo con civico (Nominatim, cache, una richiesta al secondo; 7 fuori dal Comune, 11 non risolti); attribuzione ODbL nella pagina |
| L17 | culture.roma.it: lettore per differenza in calendario ogni 2 giorni, esteso a manifestazioni, tassonomia Municipio e luoghi | lettura per differenza dal 23 ottobre: 0 schede nuove o modificate in tre giorni (fine settimana); da ripetere a cadenza |
| L59 | Regione Lazio: eventi JSON-LD di VisitLazio (LazioCrea) filtrati su Roma | VisitLazio: 68 eventi futuri nella pagina, 2 nel Comune di Roma, entrati entrambi |
| L06 | Doppioni: fondere invece di scartare, chiave con il luogo e dedupe semantico fra canali con arricchimento | i doppioni completano il gemello invece di sparire: 23 campi e 2 pagine completati; la fusione dei quasi-doppioni resta da decidere (DEC-025) |
| L43 | Avvisi parrocchiali: lettura settimanale a modello di 39 pagine avvisi HTML, 6 calendari iCal e 3 PDF (i bollettini PDF sono rari) | prova su 16 parrocchie fuori dal centro: 9 pagine avvisi lette, nessun appuntamento datato riconoscibile con le regole; serve la lettura con un modello |
| L03 | Gazetteer dei luoghi (open data + luoghi già visti + luoghi di culture.roma.it) con modello per i nomi di sede | luoghi di culture.roma.it e biblioteche per nome: 6 eventi senza pagina assegnati |
| L40 | Pagine Facebook ufficiali dei 15 Municipi (e di 3 presidenti) lette ogni settimana | 12 delle 15 pagine dei Municipi già lette il 25 ottobre: una seconda lettura oggi renderebbe quasi nulla; il valore è la cadenza settimanale (budget) |
| L56 | Musei civici e statali, parchi archeologici, MAXXI e Bioparco: calendari letti dai siti e dalle API | compresa in L19: MAXXI, Bioparco e Teatro di Documenti letti dalle pagine evento; quasi tutti già in calendario |
| L05 | Scarti a monte di collect.py: eventi Facebook senza luogo, coordinate prima del testo, scoperta per parole chiave, voce wiki S-EV-1383 | non eseguita: resa 4-24 una tantum |
| L19 | Tipi di contenuto «evento» via WordPress REST con after/modified_after (MEC, EventON, CPT personalizzati) | tipi evento di WordPress di 33 siti, 401 pagine evento lette in schema.org (MAXXI e Bioparco compresi, L56): 106 righe, 16 eventi nuovi in pagina dopo doppioni e filtri; ilparioli.it escluso (aggregatore) |
| L49 | Cinema: rassegne e appuntamenti speciali delle 47 sale romane (8 nella wiki) | non eseguita: separare rassegne e incontri dalle proiezioni richiede un modello |
| L48 | Università e accademie: agende dei 4 atenei statali, Santa Cecilia, privati e pontifici | feed RSS di Tor Vergata (ottobre-dicembre): 1 candidato con data futura, senza luogo: non in pagina |
| L57 | ASL Roma 1-2-3, ospedali, Croce Rossa e Caritas: notizie e feed letti ogni settimana per open day, screening e incontri pubblici | feed RSS di ASL Roma 3 e Caritas: 4 candidati con data futura, senza luogo: non in pagina |
| L11 | Seguire i link esterni dei post alle pagine evento ufficiali (biglietterie, biblioteche, culture.roma.it, teatri) | 256 link esterni dei post con un evento futuro, 237 pagine lette (biglietterie, social e Roma Today esclusi): 16 righe, 4 eventi nuovi |

**Classifica.** 16 eseguite, 0 da eseguire subito (costo zero o quasi), 38 da verificare con l'owner, 6 scartate. Nessuna delle 30 leve verificate la sera cambia l'ordine di grandezza: le migliori sono fonti strutturate gratuite e piccole.

| Da eseguire subito | Probabilità | Resa dopo verifica | Apify |
|---|---|---|---|

**Da verificare con l'owner**, in ordine di probabilità: L16 Definizione onesta di evento contato; L04 Fascia «altri eventi nel Municipio» per gli eventi con il so; L26 Ricerca degli eventi Facebook per luogo e parola chiave (Api; L13 Lettura settimanale dei post Facebook per differenza; L12 Coda settimanale di verifica dei candidati con modello; L40 Pagine Facebook ufficiali dei 15 Municipi lette ogni settima; L05 Scarti a monte di collect.py: eventi FB senza luogo, coordin; L49 Cinema: rassegne e appuntamenti speciali delle sale romane; L14 Livelli di cadenza per produttività misurata; L38 Iscrizione alle newsletter dei promotori e delle reti, lettu; L07 Blocchi datati dei siti del registro promossi a candidati; L09 Lettura dei post Facebook con un modello; L15 Modello a regime: fabbisogno settimanale e cadenze per canal; L47 Centri commerciali di periferia con calendario eventi; L52 Accademie straniere e istituti di cultura; L10 Visione sulle locandine dei post senza data nel testo; L21 Post dei siti via WordPress REST e RSS; L23 Zero.eu: sitemap mensile e schema.org Event; L53 Locali live e club: siti dei locali; L35 Invito ai promotori già pubblicati, con lettura delle rispos; L37 Modulo pubblico «segnala il tuo evento» e numero WhatsApp di; L44 CSV Lazio e reti del terzo settore come moltiplicatori; L30 Canali Telegram pubblici letti dall'anteprima web; L32 Gruppi Facebook di quartiere: sonda Apify sui gruppi pubblic; L50 Librerie: presentazioni annunciate sui social; L54 Mercati rionali, mercati contadini e fiere; L55 Teatri non ancora censiti; L25 Meetup: iCal pubblico per gruppo; L27 Instagram delle fonti censite letto con Apify; L28 Instagram via API ufficiale Meta (Business Discovery); L31 Canali e community WhatsApp (lettura umana); L41 Accordo con l'Istituzione Biblioteche di Roma; L46 Scuole statali: open day e feste dall'anagrafe MIM; L39 Accordo con i 15 Municipi: elenco mensile delle manifestazio; L42 Diocesi di Roma: calendario in formato dati; L36 Invito ai soggetti attivi dei censimenti (RUNTS, associazion; L45 Scambio con le testate e i blog di quartiere; L58 Richieste di licenza a Roma Capitale e a Citynews.

**Leve gratuite eseguite la sera.** Tipi evento di WordPress (33 siti, MAXXI e Bioparco compresi), link esterni dei post, VisitLazio, feed RSS di Tor Vergata, ASL Roma 3 e Caritas, prova degli avvisi parrocchiali, luoghi noti per nome, doppioni che completano il gemello: eventi futuri da 2.563 a 2.585, con pagina QN da 2.081 a 2.100. Rendono poco, come aveva previsto la verifica: le pagine evento dei grandi enti erano già in calendario, i feed delle istituzioni sono notizie più che eventi, gli avvisi parrocchiali senza un modello non danno appuntamenti riconoscibili. Le pagine dei Municipi non sono state rilette: 12 su 15 erano già state lette il 25 ottobre.

**Cosa dice la verifica sul lungo periodo.** Lo stock di oggi è una foto: una parte viene da letture una tantum che non si ripetono, e senza rileggere i canali Facebook scende verso 1.700-1.900 a metà novembre. Con letture settimanali di tutti i canali (75-95 dollari al mese di Apify) lo stock a regime stimato è 1.100-1.300 eventi (L15), non 2.000; una lettura ridotta alle circa 200 pagine che hanno prodotto il 60% degli annunci futuri costa 8-12 dollari al mese e coglie il 30-45% del flusso fresco dei post (L14). Le decisioni che servono all'owner: budget Apify mensile, regola di conteggio (doppioni fusi, orizzonte di 60 giorni, serie contate una volta: sulla foto del mattino 2.384 diventano circa 1.940), letture automatiche settimanali di siti e feed pubblici, contatto in uscita con i promotori (prima i canali a consenso: modulo e newsletter), permesso scritto per Zero.eu.

**Rischi.** Ogni fonte nuova porta doppioni (la fusione dei doppioni va fatta prima di misurare le leve nuove); le fonti strutturate si concentrano nei Municipi I e II; le 5 pagine a zero non sono toccate da nessuna leva misurata; parrocchie, scuole e ASL contengono nomi di persone (in estrazione si tengono solo data, ora, luogo ed ente).

## 1 undecies. Dove cercare i prossimi eventi di ogni promotore, e quanto costa (M, 26 ottobre 2026)

La domanda dell'owner: tutti i promotori che hanno dato un evento utile sono schedati? E per
ognuno c'è una regola che dice dove cercare i prossimi eventi al costo più basso, per esempio
sul sito invece che su Facebook quando l'evento sta su entrambi? Il passo successivo è il costo
mensile di cercare eventi ogni giorno.

**Prova del canale (0 dollari).**
- **Primo giro.** Per i 931 promotori con un sito (942 siti) sono state lette la home, la pagina
  eventi e il feed delle notizie. La pagina eventi è quella dello schedario o, se manca, la
  prima trovata nei link della home. Il robots.txt è rispettato (35 siti saltati), con una
  richiesta al secondo per sito: 847 siti letti.
- **Secondo giro.** Sui promotori rimasti su Facebook:
  - varianti dell'indirizzo per i siti non raggiungibili (39);
  - ricerca interna di WordPress con le parole dei titoli (214 siti);
  - Chromium per i siti fatti in JavaScript (56; 13 con robots.txt che vieta, saltati).
- **Riscontro.** Un evento futuro già noto del promotore è stato ritrovato sul sito con titolo e
  data vicini per 136 promotori, con il titolo intero per 84. Su un campione di 25 controllato a
  mano, 24 riscontri sono veri. L'unico falso era una data di un anno passato scritta senza
  anno, e ora è escluso.
- **Pagina scritta.** È sempre una pagina indice, mai quella di un singolo evento, perché lo slug
  porta il titolo (DEC-109). Un link Facebook è ridotto alla pagina: un video o un post ne porta
  il testo. La correzione vale anche per i canali dello schedario, che ne contenevano alcuni.

**La regola.** Il canale da leggere è il più economico che porta gli eventi del promotore. La
prova dice perché:
- **storico**: a ottobre gli eventi sono arrivati da quel canale;
- **confermato**: la prova del 26 ottobre li ha ritrovati sul sito;
- **probabile**: il sito pubblica date future, ma nessuno degli eventi noti.

Il **controllo** è il canale Facebook da guardare a cadenza lenta quando quello gratuito non porta
tutti gli eventi.

| Canale da leggere | Promotori | Prova | Eventi di ottobre |
|---|---|---|---|
| feed del sito (iCal, REST) | 36 | storico 30, confermato 2, probabile 4 | 204 |
| calendario del sito (schema.org) | 28 | storico 15, confermato 3, probabile 10 | 133 |
| pagina eventi del sito | 344 | storico 92, confermato 169, probabile 83 | 898 |
| notizie del sito (RSS) | 46 | confermato 46 | 70 |
| agenda Biblioteche di Roma | 30 | storico 30 | 156 |
| culture.roma.it | 27 | storico 27 | 124 |
| eventi Facebook | 308 | storico 308 | 472 |
| post Facebook | 346 | storico 346 | 540 |
| solo Instagram (non letto) | 17 | — | 22 |
| solo aggregatore | 6 | — | 6 |
| nessun canale proprio | 58 | — | 61 |

In sintesi:
- **Canale gratuito con prova: 414 promotori.** Per 194 la prova è storica, per 220 è confermata.
  Di questi ultimi, 196 a ottobre arrivavano solo da Facebook: ora si leggono sul sito.
- **Sito «probabile»: 97.** Pubblica date future ma non ancora i loro eventi: resta Facebook più
  il sito in prova.
- **Facebook: 654.**
  - 248 non hanno un sito;
  - 285 hanno un sito senza date;
  - 62 hanno un sito con date ma non i loro eventi;
  - 20 hanno un sito che vieta la lettura;
  - 39 hanno un sito irraggiungibile.
- **Nessun canale proprio: 81.** Soprattutto persone (artisti, guide) e co-organizzatori senza
  pagina: i loro eventi arrivano dalle pagine dei luoghi che li ospitano.

Un evento con più promotori conta per ciascuno: i totali per canale fanno 2.686, non 2.585.

**Lista completa.** I promotori con una voce nello schedario passano da 1.064 a 1.245 su 1.246:
- 139 entrano nel registro v6 come candidati (chiave `PR-…`, origine `promotori_eventi_2026-10-26`);
  tenerli o scartarli resta all'owner (DEC-024);
- 21 c'erano già sotto un'altra grafia del nome;
- 22 erano già righe del registro;
- uno resta senza voce, perché la sua riga del registro (FE-1216) ha il nome generico
  «Associazione culturale», da correggere.

Il registro v6 ha 1.759 righe. Le 1.620 del v5 sono invariate (decisione, canale, note); in fondo
ci sono cinque colonne nuove: eventi del promotore, canale da leggere, prova, pagina da leggere,
controllo. Nessun id dello schedario cambia: le voci nuove sono 139, nessuna scompare o cambia
nome.

**Costo mensile.** Prezzi dell'account (piano Apify Starter, fascia BRONZE), letti via API il 26
ottobre:
- post Facebook: 0,004 dollari a post più 0,001 di filtro data;
- eventi Facebook: 0,003 dollari a evento restituito;
- avvio di un'esecuzione: 0,001 dollari.

Ritmi misurati nelle esecuzioni del 24-25 ottobre:
- 0,088 post al giorno per pagina in media, su 4.016 pagine;
- 0,089 eventi futuri per pagina a ogni lettura, su 4.813 letture.

I post si pagano a post, non a lettura: con il filtro «solo post dal giorno prima», leggerli
ogni giorno o ogni settimana costa quasi uguale. La cadenza pesa solo sugli eventi Facebook.

| Scenario | Ogni giorno | Ogni settimana |
|---|---|---|
| Oggi, tutto da Facebook: 1.123 pagine, eventi e post | 33,94 $ | 26,17 $ |
| Regola: canale gratuito dove c'è la prova, Facebook per gli altri (327 pagine eventi, 423 post), controllo compreso | 15,49 $ | 13,19 $ |
| Regola con anche i siti «probabili» al posto di Facebook | 15,34 $ | 13,17 $ |

Che cosa dice la tabella:
- **Siti, feed, notizie, culture.roma.it e Biblioteche di Roma costano 0 dollari** a qualsiasi
  cadenza: circa 420 pagine al giorno, una richiesta al secondo per sito.
- **Il controllo sui post costa 2,25 dollari**, perché i post si pagano a post anche a cadenza
  lenta. Il controllo con gli eventi Facebook una volta al mese costa pochi centesimi.
- **Spostare i siti «probabili» quasi non risparmia**, perché tengono il controllo Facebook.
- **La regola sta dentro il consumo incluso nel piano Starter** (29 dollari al mese).
- **Il ciclo Apify in corso** (24 ottobre - 23 novembre) ha già 177,76 dollari consumati dai
  censimenti, con un tetto di 200.
- **Restano fuori dalla tabella** la scoperta di promotori nuovi su Facebook per parole chiave
  (circa 1 dollaro a trimestre) e Instagram, oggi non letto.

**Confronto con le stime del §1 decies.** I 75-95 dollari al mese del §1 decies riguardano la
lettura settimanale di tutti i canali censiti, circa 4.000 pagine. Qui ci sono solo le pagine
dei 1.246 promotori che hanno dato eventi. Le due cifre misurano cose diverse e non si
sommano.

**Limiti.**
- La prova è di un giorno: un promotore che a fine ottobre non aveva eventi sul sito può
  averli a novembre. La prova si ripete ogni mese.
- 84 riscontri si reggono sul solo titolo.
- I ritmi di post ed eventi sono quelli di fine ottobre: dicembre sarà più fitto.
- La lettura di Facebook dipende da attori Apify di terzi, che cambiano prezzi e
  comportamento.

Uscite su Drive (cartella delle uscite della sessione):
- `promotori_dove_cercare_2026-10-26.xlsx`: i 1.246 promotori con la regola, il riepilogo, i
  costi, i prezzi e le misure;
- `registro_fonti_v6.xlsx`.

Gli script sono in `tools/fonti/lavoro-2026-10/canali/`.

## 1 duodecies. Notizie di quartiere nei dati già raccolti (M, 26 ottobre 2026)

Le 14.779 voci già raccolte sono state rilette a ritroso, senza letture nuove: post Facebook di associazioni, comitati,
parrocchie, scuole, enti e luoghi, comprese le fonti scartate per gli eventi, e notizie dei loro siti. Lo scopo era trovare
notizie per gli altri blocchi del sito.

- 402 notizie confermate, pari a 347 fatti; 237 sono di ottobre.
- 75 pagine QN su 89 ne hanno almeno una.
- 194 organizzazioni le producono. 111 di queste non hanno dato nessun evento alla pagina e portano 217 notizie.
- Delle 1.898 fonti rilette senza eventi, 1.660 non hanno nemmeno notizie.

Metodo, numeri, fonti e decisione aperta sono in `docs/sources/NOTIZIE_DAI_DATI_2026-10-26.md`. Il foglio con le sintesi
scritte da noi e il link alla fonte è su Drive.

## 1 terdecies. Qualità della pagina «Eventi dei quartieri» (M, 26 ottobre 2026)

Un campione di 155 eventi, diviso per canale, è stato confrontato con il testo della fonte da un revisore AI; un secondo
revisore indipendente ne ha riletti 47 (kappa 0,78 sull'errore grave).

- Errori gravi (data sbagliata, già passato, non è un evento, fuori Roma o online, pagina incoerente): 28% del campione
  prima delle correzioni, 22% dopo.
- L'ora degli eventi Facebook era in UTC: ora è convertita all'ora di Roma.
- Sono tolti 97 eventi fuori dal Comune, online o presi da pagine d'archivio.
- La pagina nasconde da sola gli eventi finiti.
- Il validatore `tools/fonti/valida_eventi.py` e i suoi test controllano ogni riga pubblicata. Restano gravi solo le 32 schede
  di Roma Today senza link (DEC-026).
- Gli annunci estratti dai post restano al 43% di errori gravi.

Metodo, numeri, correzioni e decisioni aperte sono in `docs/sources/QUALITA_EVENTI_2026-10-26.md`.

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
`eventi_siti_prova_2026-10-24.xlsx` su Drive. Questa prova non controllava il robots.txt: dal
25 ottobre lo strumento lo legge una volta per host e lo rispetta (revisione della PR 15, test
T-LS-6).

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
4. Portare il pacchetto Metodo QN nell'ambiente e riassegnare la geografia degli eventi con
   `qngeo.py punto`.
5. Rimisurare a fine novembre: eventi futuri per pagina QN con le sole righe principali.
6. Promotori (§1 nonies): per le fonti che vietano la riproduzione usare la card generata e i
   nostri testi; prossime ricerche gratuite: calendari dei tornei delle società (UISP, CSI) e
   bollettini parrocchiali; per i centri anziani, contatto diretto.
7. Leve del 26 ottobre (§1 decies): lettura settimanale dei feed iCal e REST dei siti e del
   delta di culture.roma.it; dopo il giro della sera 16 leve eseguite, nessuna da eseguire subito, 38 da verificare con
   l'owner e 6 scartate (§1 decies), nel foglio `leve_eventi_2026-10-26.xlsx`.
8. Dove cercare (§1 undecies). Owner:
   - cadenza (ogni giorno o ogni settimana) e budget mensile Apify della lettura dei promotori;
   - decidere i 139 candidati `PR-…` del registro v6;
   - correggere il nome della riga FE-1216.

   Builder: ripetere la prova del canale ogni mese, e portare la regola nel workflow n8n di
   staging quando le decisioni ci sono.
9. Notizie dai dati (§1 duodecies). Owner: decidere se un post di un comitato o di
    un'associazione può essere fonte dei blocchi Notizie e Segnalazioni (OWNER_DECISION_REQUIRED
    in `NOTIZIE_DAI_DATI_2026-10-26.md`).
10. Timeline di brevi per quartiere (`TIMELINE_BREVI_2026-10-26.md`). Owner: forma della timeline
    (solo quartiere; quartiere, municipio e città insieme; timeline del municipio), monitoraggio delle
    pagine politiche, misura del loro ritmo prima di decidere.
11. Qualità della pagina eventi (§1 terdecies). Owner: annunci estratti dai post (toglierli, tenerli «da verificare»,
    rifarne l'estrazione con verifica), regola di conteggio di corsi e attività ricorrenti (OWNER_DECISION_REQUIRED in
    `QUALITA_EVENTI_2026-10-26.md`). Builder: far girare il validatore con `--severo` prima di ogni pubblicazione.

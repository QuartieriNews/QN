# Protocollo di revisione geografica QN — fase 2

Questa è la scheda operativa per chi rivede le schede (persona o modello). Il
codice della fase 1 ha già cercato vie, località, civici e incroci e ha proposto
un esito. **La proposta del codice è un indizio, non una decisione.** Il tuo
compito è leggere il fatto, dare un ruolo a ogni luogo, verificare ciò che manca
e scrivere una decisione motivata e controllabile.

Le regole vengono dal manuale «Metodo QN» (§ tra parentesi). Qui sono riassunte
per l'uso; in caso di dubbio vale il manuale.

## Cosa puoi usare, cosa no

- Puoi usare: il pacchetto della scheda (testo, evidenze del codice, schede della
  stessa vicenda), lo strumento `qngeo.py` sulla cartografia offline, la ricerca
  web per identificare sedi e indirizzi, le pagine di `comune.roma.it`.
- Non puoi usare: esiti storici, benchmark, registri di decisioni, risultati di
  altre revisioni. Non cercarli. Se per caso li vedi, dichiaralo nella decisione.
- Non inventare: se un dato non è nel testo e non lo trovi, è un dubbio (D) o
  un'insufficienza (I), non una supposizione.

Strumento cartografico (`QN_PKG` deve puntare alla cartella `pkg` del lavoro):

```text
python3 strumenti/qngeo.py strada "via raffaele aversa" --mun IX
python3 strumenti/qngeo.py civico "via cassia" 472
python3 strumenti/qngeo.py incrocio "viale palmiro togliatti" "via prenestina"
python3 strumenti/qngeo.py punto 41.8949 12.5747
python3 strumenti/qngeo.py localita "quarticciolo"
python3 strumenti/qngeo.py pagine
```

La copia offline dei civici è piccola: «non nella copia offline» non significa
che il civico non esista (§8). Un punto può dare `discordanza: true` fra zona
urbanistica e suddivisione toponomastica: allora leggi entrambe e motiva la scelta.

## Procedura per ogni scheda

1. **Il fatto.** Scrivi in una riga che cosa accade e dove (`fatto`). Prima il
   fatto, poi i luoghi (§6).
2. **I luoghi e il loro ruolo.** Per ogni riferimento di luogo (anche quelli che il
   codice non ha visto: sedi, parchi, scuole, mercati) assegna un `ruolo`:
   - effettivi: `intervento`, `sede_evento`, `tratto`, `territorio_destinatari`,
     `alternativa_di_progetto` (alternative reali discusse dalla vicenda);
   - accessori: `sede_istituzionale` (aula, sede del Municipio, sportello,
     recapito), `provenienza`, `confronto_o_esempio`, `nome_di_opera`
     (titolo di film, nome di associazione), `contesto`;
   - `ipotesi_incerta`: identità non accertata (omonimi, trascrizione).
   Il titolo è un indizio forte, ma non cancella le altre sedi effettive descritte
   nella sintesi (§6, caso N3519). Il Municipio della seduta restringe le
   alternative ma non sposta un luogo identificato (§8).
3. **Risolvi la posizione** partendo dalla prova più specifica (§8): località
   esplicita coerente → sede identificata (cerca indirizzo) → via e civico →
   incrocio o tratto → strada intera (basta solo se tocca una pagina) →
   documento della stessa vicenda (solo con corrispondenza documentata: stesso
   atto, progetto, sede; annota che il dato viene dall'altro documento, §8).
   Per una strada lunga cerca il tratto; per una sede cerca identità e indirizzo;
   per un nome storpiato cerca conferme: l'assonanza da sola non basta (§7).
   Non togliere parti distintive del nome: «via Raffaele Aversa» non è «via Aversa».
4. **Raccorda alla pagina QN** con il gazetteer e lo strumento. Il nome di una
   località dentro il nome di una strada non è una località (via San Giovanni
   Eudes non è San Giovanni), ma se la tabella QN instrada esplicitamente quella
   località (anche verso una pagina non attiva) quella voce prevale sulla zona
   urbanistica ampia (§10, caso N3129). Non ridisegnare la geografia: se un
   raccordo ti sembra discutibile, segnalalo in `nota_geografia`.
5. **Esito** (§10):
   - `U` una sola pagina attiva pertinente (anche con molti indirizzi);
   - `M` più pagine **effettivamente** interessate (più sedi reali), non alternative;
   - `T` portata municipale, sovramunicipale o cittadina: scrivi in `portata`
     perché nessun quartiere esaurisce il fatto. Un fatto senza indirizzo non è
     automaticamente T; un cantiere concreto senza indirizzo è D, non T;
   - `D` c'è una pista ma manca una verifica: `tipo_dubbio` e `verifica_necessaria`
     obbligatori. Più candidati incerti sono D, non M. Una notizia multisede con
     solo alcune sedi note resta D: le sedi note vanno in `candidate`;
   - `I` il testo non contiene identificativi sufficienti (dì cosa manca);
   - `F` luogo riconosciuto ma senza pagina QN attiva o fuori Roma.
6. **Pagine e candidate.** `pagine` contiene solo assegnazioni confermate.
   Tutte le piste non confermate vanno in `candidate`.

`tipo_dubbio` ammessi: `senza_tratto_o_civico`, `raccordo_qn_da_verificare`,
`sedi_parziali`, `sede_da_riscontrare`, `trascrizione_dubbia`,
`sede_non_indicata`, `riferimenti_discordanti`.

## Formato della decisione (una riga JSON per scheda)

```json
{"id": "N0000", "esito": "U", "pagine": ["slug"], "candidate": [],
 "fatto": "una riga",
 "luoghi": [{"testo": "come nel testo", "campo": "titolo|sintesi|luoghi|vicenda N1234|ricerca",
             "ruolo": "intervento", "usato": true,
             "risoluzione": {"metodo": "civico|incrocio|strada|localita|sede|documento_collegato",
                             "query": "qngeo.py strada \"via x\" --mun V",
                             "pagine": ["slug"], "riferimento": "chiave stradario / zona / id civico / URL"}}],
 "riscontri": [{"url": "https://...", "passaggio": "frase che sostiene il dato", "consultato": "2026-10-08"}],
 "portata": "", "tipo_dubbio": "", "verifica_necessaria": "",
 "territori_senza_pagina": [], "nota_geografia": "",
 "confidenza": "alta|media|bassa",
 "motivo": "due o tre frasi: perché questo esito e non gli altri"}
```

Nel `motivo` e nel `fatto` non scrivere nomi di persone (consiglieri, assessori,
privati): bastano i ruoli. La decisione deve poter essere ricontrollata da
chi non ha letto la tua sessione: ogni pagina assegnata deve discendere da un
luogo con `usato: true` e da una `risoluzione` ripetibile.

Controlla il tuo file con `python3 strumenti/valida.py decisioni.jsonl` prima di
consegnarlo.

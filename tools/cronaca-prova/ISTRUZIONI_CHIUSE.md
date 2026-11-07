# Testate chiuse: a quale fatto corrisponde ogni titolo

Il tuo lotto (`lotto_N.json`) contiene:
- `titoli`: titoli di testate che escludono gli agenti AI o sono in abbonamento (RomaToday, Il
  Messaggero, Corriere Roma, Repubblica Roma, ANSA, Leggo, Agenzia Nova…), presi dall'indice
  aperto GDELT: testata, editore, data e ora, titolo, link. Il filtro è largo: molti NON sono
  cronaca romana.
- `fatti`: i fatti di cronaca romana già noti negli stessi giorni:
  - quelli con `id` che inizia per `CR-` vengono dalle fonti ufficiali (Questura, Carabinieri,
    Vigili del Fuoco, Polizia Locale);
  - quelli con `id` che inizia per `P` vengono dalle sei testate aperte (`testate` dice quali).

Non aprire nessun link e non cercare sul web: lavori solo su titoli e fatti (DEC-108: delle
testate chiuse si usano solo titolo, link e ora).

## Compiti

1. **Classifica ogni titolo** (`cid`):
   - `cronaca_roma`: reato, arresto, denuncia, controllo con esiti, incidente, incendio,
     soccorso, crollo, morte violenta o accidentale, sequestro, sgombero, truffa, aggressione…
     avvenuto nel Comune di Roma, Ostia compresa;
   - `cronaca_fuori`: stesso tipo di fatto fuori dal Comune (provincia, altre città);
   - `giudiziaria`: processi, sentenze, inchieste su fatti non recenti, indagini nazionali con
     sede a Roma ma senza un fatto in città (es. «la Procura di Roma indaga su…»);
   - `non_cronaca`: politica, economia, eventi, servizi, meteo, sport, commenti.
   Una notizia su un fatto romano ma raccontata da Roma per un fatto altrove (es. un ferito
   portato in elicottero a Roma da un incidente in provincia) è `cronaca_fuori`.
2. **Abbina ogni titolo `cronaca_roma`**:
   - a un fatto della lista `fatti`, se è lo stesso evento: `certa` quando tipo, luogo e almeno
     un dettaglio concordano (età, numero di persone, oggetto, modalità); `probabile` con tipo
     e luogo ma senza dettagli verificabili. Data compatibile: entro 3 giorni dal fatto; i
     comunicati ufficiali possono uscire anche qualche giorno dopo i giornali. Gli aggiornamenti
     (convalida, funerali, indagini successive dello stesso caso) vanno sullo stesso fatto;
   - altrimenti a un **fatto nuovo**, visto solo sulle testate chiuse: raggruppa i titoli che
     raccontano lo stesso evento, anche di testate diverse e di giorni vicini.
3. **Luogo e pagina dei fatti nuovi**: il luogo più specifico citato. Per la pagina QN usa lo
   strumento cartografico, senza rete:
   `QN_RETE=0 python3 /home/user/QN/tools/geo-assign/qngeo.py localita "centocelle"`
   oppure `... strada "via tuscolana"` (con `QN_PKG` impostato come indicato nel lotto).
   Strada lunga o luogo su più pagine: `pagina_qn` null e `livello` "municipio" o "dubbio";
   «Roma» generico: livello "citta".

## Uscita (nella stessa cartella)

`abbinamenti_N.jsonl`, una riga per ogni `cid` del lotto, nessuno escluso:

{"cid": "K00012", "classe": "cronaca_roma", "fatto": "CR-C1_049-1" | "P2-014" | "N3-001" | null,
 "corrispondenza": "certa" | "probabile" | null}

`nuovi_N.jsonl`, una riga per fatto nuovo (id `N<lotto>-<progressivo>`):

{"nid": "N3-001", "cid": ["K00012", "K00031"], "data": "2026-06-07", "tipo": "arresto|rapina|
 furto|aggressione|droga|truffa|incidente|incendio|soccorso|morte|controlli|sgombero|sequestro|
 altro", "fatto": "una riga, senza nomi di persona", "luogo": "testo o null", "pagina_qn":
 "slug o null", "livello": "quartiere|municipio|citta|dubbio"}

Nei campi `fatto` e `luogo` non scrivere nomi di persona. Prima di rispondere controlla con
un piccolo script che ogni `cid` del lotto compaia una volta in `abbinamenti_N.jsonl` e che
ogni fatto nuovo citato lì esista in `nuovi_N.jsonl`. Alla fine una riga: titoli, quanti
cronaca_roma, quanti abbinati a fatti noti, quanti fatti nuovi.

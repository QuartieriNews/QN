# Passata inversa: fatti di cronaca romana sulle testate aperte, giugno 2026

Il tuo lotto (`lotto_N.json`) contiene:
- `titoli`: titoli (o slug dell'URL, senza accenti) pubblicati a giugno 2026 da sei testate
  che non escludono gli agenti AI: Abitare a Roma, Dire, VignaClaraBlog, Il Tempo, Roma Daily
  News, Il Faro Online. Sono già filtrati per parole chiave: molti NON sono cronaca.
- `fatti_ufficiali`: i fatti pubblicati nello stesso periodo da Questura, Carabinieri, Vigili
  del Fuoco e Polizia Locale di Roma (con le pagine-quartiere QN già assegnate).

Non aprire nessun URL e non cercare sul web: lavori solo sui titoli e sui fatti ufficiali.

## Compiti

1. **Classifica ogni titolo** (`sid`) in una sola classe:
   - `cronaca_roma`: un fatto di cronaca (reato, arresto, denuncia, controllo di polizia con
     esiti, incidente, incendio, soccorso, crollo, morte violenta o accidentale, sequestro,
     sgombero, truffa, aggressione…) avvenuto nel Comune di Roma, Ostia compresa;
   - `cronaca_fuori`: stesso tipo di fatto ma fuori dal Comune di Roma (Fiumicino, Guidonia,
     Tivoli, Pomezia, Castelli, Ladispoli, Anzio, altre città…);
   - `cronaca_giudiziaria`: processi, sentenze, inchieste su fatti non di giugno;
   - `non_cronaca`: politica, eventi, servizi, meteo, sport, commenti, opinioni, appelli.
   Se il luogo non si capisce dal titolo e la testata è romana (Abitare a Roma, Roma Daily
   News, VignaClaraBlog), considera Roma; per Il Faro Online, Dire e Il Tempo senza luogo
   romano riconoscibile usa `cronaca_fuori` solo se c'è un luogo esterno, altrimenti
   `cronaca_roma` con `luogo: null`.
2. **Raggruppa** i titoli `cronaca_roma` in fatti: lo stesso evento riportato da più testate
   o in più giorni (anche aggiornamenti) è un solo fatto.
3. **Confronta ogni fatto con `fatti_ufficiali`**: se è lo stesso evento indica l'`id`, con
   `certa` (tipo, luogo e almeno un dettaglio concordi) o `probabile`; se un comunicato
   ufficiale raccoglie più arresti, il fatto corrisponde a quella scheda solo se è uno di quelli.
4. **Luogo e pagina QN**: il luogo più specifico citato (via, piazza, quartiere, località).
   Per la pagina usa lo strumento cartografico del progetto, per esempio:
   `QN_RETE=0 python3 tools/geo-assign/qngeo.py localita "centocelle"` (con `QN_PKG` impostato)
   oppure `qngeo.py strada "via tuscolana"` (strade lunghe = più pagine: allora `pagina_qn`
   null e `livello` "municipio" o "dubbio"). Se non è risolvibile, `pagina_qn: null`.

## Uscita

`fatti_N.jsonl` nella stessa cartella, una riga per fatto `cronaca_roma`:

{"fid": "P<N>-001", "sid": ["S0012", "S0040"], "testate": ["Abitare a Roma", "Roma Daily News"],
 "data": "2026-06-03", "tipo": "arresto|rapina|furto|aggressione|droga|truffa|incidente|incendio|
 soccorso|morte|controlli|sgombero|sequestro|altro", "fatto": "una riga, senza nomi di persona",
 "luogo": "testo o null", "pagina_qn": "slug o null", "livello": "quartiere|municipio|citta|dubbio",
 "ufficiale": "CR-... o null", "corrispondenza": "certa|probabile|null"}

`scarti_N.jsonl`: una riga per ogni altro titolo: {"sid": "S0001", "classe": "non_cronaca"}.

Ogni `sid` del lotto deve comparire esattamente una volta, in uno dei due file. Alla fine
rispondi con una riga: titoli, fatti cronaca_roma, quanti corrispondono a fatti ufficiali.

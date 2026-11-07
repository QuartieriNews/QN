# Passata in avanti: quali testate hanno riportato i fatti ufficiali di giugno 2026

Ogni riga del tuo lotto (`lotto_N.json`) è un fatto di cronaca pubblicato a giugno 2026
da una fonte ufficiale romana (Questura, Carabinieri, Vigili del Fuoco, Polizia Locale).
Per ciascun fatto devi scoprire quali testate giornalistiche lo hanno riportato.

## Strumento e limiti (vincolanti)

- Usa SOLO lo strumento WebSearch, `mode: "standard"`, sempre con questo `allowed_domains`:
  ["romatoday.it","ilmessaggero.it","corriere.it","repubblica.it","iltempo.it","fanpage.it",
   "leggo.it","romadailynews.it","ilfaroonline.it","dire.it","ansa.it","agenzianova.com",
   "abitarearoma.it","vignaclarablog.it","adnkronos.com","lapresse.it","today.it","rainews.it",
   "romait.it","affaritaliani.it","tg24.sky.it","ilgiornale.it","ilfattoquotidiano.it"]
  Nella prova del 10 ottobre 2026 lo strumento ha rifiutato corriere.it, repubblica.it e
  rainews.it (non accessibili al suo agente): le ricerche sono girate sugli altri 20 domini.
- NON aprire le pagine degli articoli (niente WebFetch, niente curl): molte testate escludono
  gli agenti AI nel robots.txt o sono in abbonamento. Lavori solo su titolo, URL e il testo
  che la ricerca restituisce.
- Al massimo 2 ricerche per fatto. Prima ricerca: tipo di fatto + luogo più specifico
  (via/quartiere) + un dettaglio distintivo (età, oggetto, numero di persone) + "Roma".
  Seconda ricerca solo se la prima non trova nulla di pertinente, con parole diverse
  (sinonimi: arrestato/fermato/bloccato, rapina/scippo, ecc.) o il quartiere più noto.
- Non scrivere mai nomi di persone nei tuoi campi `nota`.

## Quando un risultato è lo stesso fatto

- `certa`: stesso tipo di fatto, stesso luogo (via o quartiere) e almeno due dettagli
  specifici concordi (età, numero di persone, oggetto, modalità, ora), e data compatibile.
- `probabile`: stesso tipo di fatto e stesso luogo con un solo dettaglio concorde, oppure
  dettagli concordi ma data non verificabile.
- Data compatibile: articolo uscito fra 7 giorni prima della pubblicazione ufficiale e
  5 giorni dopo. La data si ricava dall'URL (ANSA, Dire, Il Tempo, Roma Daily News,
  VignaClaraBlog la contengono), dal testo restituito dalla ricerca, o non si conosce:
  allora scrivi `null` e `prova_data: "sconosciuta"`.
- Un articolo di un altro anno, di un'altra città o di un fatto simile ma diverso NON va
  registrato. Nel dubbio fra fatto simile e stesso fatto, non registrarlo e scrivilo in `nota`.
- Un articolo che raccoglie più fatti (es. "raffica di arresti nel weekend") conta se
  il fatto è riconoscibile dentro il riassunto restituito.

## Nomi delle testate (usa questi)

RomaToday, Il Messaggero, Corriere della Sera Roma, la Repubblica Roma, Il Tempo, Fanpage,
Leggo, Roma Daily News, Il Faro Online, Dire, ANSA, Agenzia Nova, Abitare a Roma,
VignaClaraBlog, Adnkronos, LaPresse, Today.it, Rai News, RomaIT, Affaritaliani,
Sky TG24, il Giornale, il Fatto Quotidiano.

## Uscita

Scrivi un file `risultati_N.jsonl` (stessa N del lotto) nella stessa cartella, una riga
JSON per fatto, nell'ordine del lotto, anche quando non trovi nulla:

{"id": "CR-C1_049-1", "ricerche": ["..."], "testate": [{"testata": "RomaToday", "url": "...",
 "titolo": "...", "data": "2026-06-05" | null, "prova_data": "url" | "ricerca" | "sconosciuta",
 "corrispondenza": "certa" | "probabile"}], "nota": "breve, senza nomi di persona"}

Più URL della stessa testata per lo stesso fatto: tieni solo il più pertinente.
Alla fine rispondi con una riga: quanti fatti, quanti con almeno una testata, quante
ricerche hai fatto.

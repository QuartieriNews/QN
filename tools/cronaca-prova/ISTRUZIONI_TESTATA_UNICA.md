# Notizie viste su una sola testata aperta: sono anche su altre testate?

Ogni riga del tuo lotto (`lotto_N.json`) è una notizia di cronaca romana di giugno 2026 che,
fra sei piccole testate aperte, compare su una sola (`testate`). Hai il suo titolo e il link.
Devi scoprire se la stessa notizia è uscita anche su ALTRE testate.

## Strumento e limiti (vincolanti)

- Solo WebSearch, `mode: "standard"`, con questo `allowed_domains`:
  ["romatoday.it","ilmessaggero.it","iltempo.it","fanpage.it","leggo.it","romadailynews.it",
   "ilfaroonline.it","dire.it","ansa.it","agenzianova.com","abitarearoma.it","vignaclarablog.it",
   "adnkronos.com","lapresse.it","today.it","romait.it","affaritaliani.it","tg24.sky.it",
   "ilgiornale.it","ilfattoquotidiano.it"]
  (corriere.it, repubblica.it e rainews.it sono rifiutati dallo strumento: non metterli.)
- Non aprire nessuna pagina (niente WebFetch, niente curl). Solo titolo, URL e testo della ricerca.
- Al massimo 2 ricerche per notizia: tipo di fatto + luogo + un dettaglio + "Roma"; la seconda
  con parole diverse solo se la prima non trova nulla.
- Non scrivere nomi di persona nel campo `nota`.

## Quando è la stessa notizia

Stesso tipo di fatto, stesso luogo, almeno un dettaglio concorde (età, oggetto, numero di
persone, modalità) e data compatibile (entro 3 giorni da `data`). `certa` se ci sono due
dettagli e la data è verificabile; altrimenti `probabile`. La testata di partenza non conta:
registra solo le ALTRE. Nel dubbio fra fatto simile e stesso fatto, non registrare e spiega in `nota`.

## Uscita

`risultati_N.jsonl` nella stessa cartella, una riga per notizia, nell'ordine del lotto:

{"fid": "P1-012", "ricerche": ["..."], "altre_testate": [{"testata": "RomaToday", "url": "...",
 "corrispondenza": "certa" | "probabile"}], "nota": "breve"}

Nomi delle testate: RomaToday, Il Messaggero, Il Tempo, Fanpage, Leggo, Roma Daily News,
Il Faro Online, Dire, ANSA, Agenzia Nova, Abitare a Roma, VignaClaraBlog, Adnkronos, LaPresse,
Today.it, RomaIT, Affaritaliani, Sky TG24, il Giornale, il Fatto Quotidiano.
Alla fine una riga: notizie, quante con almeno un'altra testata, ricerche fatte.

# Fatti nuovi delle testate chiuse: doppioni fra lotti vicini

I titoli delle testate chiuse sono stati letti a finestre di tre giorni. Un fatto raccontato a
cavallo di due finestre può essere diventato due «fatti nuovi» con id diversi (es. `N4-012` e
`N5-003`). Il file `nuovi_tutti.json` li elenca tutti, in ordine di data, con tipo, fatto,
luogo, pagina e titoli.

Compito: trova i doppioni, cioè coppie (o gruppi) di fatti di **lotti diversi** che raccontano
lo stesso evento: stesso tipo, stesso luogo, date entro 3 giorni, dettagli compatibili. Nel
dubbio non fondere. Non fondere fatti dello stesso lotto (lì i raggruppamenti sono già fatti).

Non aprire link e non cercare sul web.

Uscita `fusioni.json`: un oggetto che manda ogni doppione nell'id che resta (il primo per
data): {"N5-003": "N4-012", ...}. Se non ci sono doppioni, `{}`. Alla fine una riga: fatti
letti, doppioni trovati.

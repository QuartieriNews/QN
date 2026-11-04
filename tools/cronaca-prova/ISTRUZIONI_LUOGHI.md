# Testate aperte: pagina QN delle notizie che il titolo non localizza

Il lotto (`luoghi.json`) elenca i fatti delle testate aperte rimasti senza pagina dopo la
lettura dei soli titoli: per ciascuno `fid`, il fatto, il luogo già trovato, il livello e i
`sid` dei titoli. Il testo degli articoli è in `testi/<sid>.txt` (solo testate che non
escludono gli agenti AI; non aprire altri link e non cercare sul web).

Per ogni fatto:

1. Leggi il testo e trova il luogo **del fatto** (via, civico, piazza, parco, stazione,
   quartiere), non la sede del reparto che è intervenuto né la residenza delle persone.
2. Assegna la pagina con il protocollo del progetto
   (`/home/user/QN/tools/geo-assign/PROTOCOLLO_REVISIONE.md`) e lo strumento cartografico:
   `python3 /home/user/QN/tools/geo-assign/qngeo.py localita|strada|civico|incrocio ...`
   (con `QN_PKG` impostato come indicato nel lotto; `civico` interroga il Geoportale).
3. Se il fatto risulta fuori dal Comune di Roma, `livello: "fuori"`. Se non è un fatto di
   cronaca, `livello: "non_cronaca"`.

Uscita `luoghi_esito.jsonl`, una riga per fatto:

{"fid": "P1-012", "luogo": "via ... 12", "pagina_qn": "slug o null", "livello":
 "quartiere|municipio|citta|dubbio|fuori|non_cronaca", "come": "comando qngeo usato o motivo"}

Niente nomi di persona nei campi. Alla fine una riga: fatti, quanti con pagina, quanti ancora
senza.

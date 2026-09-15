# Lotto rappresentativo su Opus 5 (studio fonti, Fase 0, metodo M-0.3)

Scopo: misurare su Claude Opus 5 quantità di lavoro, tempo, errori e attese su attività già autorizzate dello studio fonti, riutilizzando materiali già raccolti. Perimetro e criteri di qualità identici a quelli usati finora (nota `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md` §6 per le registrazioni; CSV `A2_approfondimento_pdf_campione.csv` per gli atti).

## Vincoli assoluti
- Nessuna richiesta di rete: tutti i materiali sono locali (cartella `lotto_opus5/`). Nessuna API a pagamento, nessuna chiave, nessuna installazione.
- Nessun nome di persona negli output (DEC-102): usare i ruoli ("la presidente della commissione", "un consigliere di opposizione", "l'assessora").
- Ogni notizia candidata cita l'evidenza: per le registrazioni il marcatore `[mm:ss]` della riga di trascrizione; per gli atti il numero di pagina (`=== pagina N ===`).
- Scrivere solo dentro `out/` e `log/`. Non modificare i materiali. Non rileggere materiali già schedati.
- Lingua: italiano. Stile delle schede: quello di §6 della nota video (sintesi densa, "Aggiunte rispetto agli atti", "Sovrapposizioni", "Possibile notizia" con qualità alta/media/bassa).

## Lotto A: registrazioni (10 Consigli municipali RomaTV)
Elenco: `manifest_A.csv` (colonne: n, ruolo nuovo/taratura, territorio, organo, data_seduta, data_pubblicazione, durata_hm, parole, guid, url, file). Trascrizioni: `trascrizioni/<guid>.txt`, righe con marcatore `[mm:ss]` ogni 30 secondi (riconoscimento automatico della piattaforma: nomi propri e toponimi spesso storpiati; segnalare i dubbi).
Controllo documentale locale (facoltativo, senza rete): `../deliver/A2_2026-06_items.csv` (atti di Atti Web di giugno: tipologia, municipio, date, oggetto), `../deliver/A1_2026-06_items.csv` (avvisi e notizie dei Municipi).
Per ogni registrazione produrre `out/A_<n>.json` con:
```
{"n":1,"guid":"…","territorio":"…","organo":"…","data_seduta":"…","durata_hm":"…","parole":0,
 "qualita_trascrizione":{"parole_al_minuto":0,"note":"…"},
 "argomenti":["…"],
 "atti_collegati":{"convocazione":"sì|no|non verificato","verbale":"sì|no|non verificato","riferimento":"…"},
 "notizie_candidate":[{"titolo":"…","sintesi":"≤ 60 parole","luoghi":["…"],"evidenza":["[mm:ss]","[mm:ss]"],
   "tipo":"delibera|mozione|risoluzione|ordine del giorno|interrogazione|sopralluogo|audizione|altro",
   "qualita":"alta|media|bassa","novita_rispetto_agli_atti":"solo dal parlato|anche negli atti|non verificabile"}],
 "scheda_narrativa":"≤ 200 parole, stile §6, senza nomi",
 "tempo_lettura_s":0}
```
Al termine scrivere `out/A_schede.md` (una scheda narrativa per registrazione, intestazione "**<n>. RomaTV, <territorio>, <organo> del <data> (<durata>; <parole> parole)**").

## Lotto B: atti di Atti Web (30 PDF del campione di giugno)
Elenco: `manifest_B.csv` (n, municipio, tipologia, data_repertorio, formato testo/scansione, pagine, url, pdf, testo). Testi: `atti/NN.txt` con marcatori di pagina; per le scansioni il testo viene dall'OCR Tesseract (possibili errori: segnalare `ocr_incerto`). Tipologie: MMC convocazione di commissione, MMV verbale di commissione, CMC/CMR/CMD/CMZ/CMV/CMY delibere, mozioni, risoluzioni e verbali di Consiglio, DMS/GMD determinazioni e atti di Giunta/Direzione, PMO altro.
Produrre `out/B_classificazione.csv` con colonne:
`n,tipologia,municipio,data_repertorio,formato,pagine,esito_testo,struttura_emittente,organo_o_ufficio,oggetto_sintetico,luoghi,validita_o_seduta,contenuto,coerenza_organo_territorio_o_nota,notizia_candidata,titolo_candidato,evidenza_pagina,qualita,ocr_incerto,tempo_lettura_s`
(oggetto ≤ 30 parole; contenuto ≤ 60 parole; luoghi separati da `;`; notizia_candidata sì/no; qualità alta/media/bassa; ocr_incerto sì/no).

## Misure da registrare (obbligatorie)
- `log/<A|B>_modello.txt`: la riga del proprio system prompt che dichiara il modello, copiata alla lettera, come prima azione. Se il modello non è Claude Opus 5, fermarsi e riferirlo.
- `log/<A|B>_tempi.csv`: `n,inizio_epoch,fine_epoch,secondi` per ogni item (usare `date +%s` prima e dopo).
- `log/<A|B>_problemi.md`: errori, dubbi, item saltati e perché, correzioni fatte in corso d'opera.
- Rapporto finale (nel messaggio di chiusura): item completati, tempo totale, problemi, e nient'altro.

# Script dello studio fonti (Fase 0, metodo M-0.3)

Strumenti di lavoro dell'Operator per lo studio delle fonti di giugno 2026
(`docs/sources/`). Sono versionati qui perché l'ambiente cloud perde lo
scratchpad quando la VM viene ritirata per inattività: senza questi file una
ripresa senza presidio dovrebbe riscriverli (nota di fattibilità §8.4).

Non sono code node della pipeline (`code-nodes/`): non girano in n8n, non hanno
il pattern one-source/two-contexts e non producono dati di produzione. Girano
dallo scratchpad della sessione, con il proxy dell'ambiente (`REQUESTS_CA_BUNDLE`)
e senza credenziali: nessun file contiene chiavi o token. I dati che producono
restano nello scratchpad e, in forma aggregata e senza nomi di persona, in
`QN Hub / 20 Packages / Fonti 2026-06/` (DEC-102, DEC-104).

| Gruppo | File | Cosa fanno |
|---|---|---|
| A1, E2, E3 | `a1_walker.py`, `a1_items.py`, `a1_agg.py`, `e2_walker.py`, `e2_walker2.py`, `e3_walker.py`, `e3_items.py`, `e3_agg.py` | elenchi mensili dei portali municipali e delle agende eventi, aggregati per Municipio |
| A2 Atti Web | `a2_deep.py`, `a2_tipologie.py`, `a2_pdf_sample.py` | tipologie, approfondimento sui PDF, campione con seed dei 120 PDF |
| Gazetteer | `geo_lookup.py`, `peek.py` | localizzazione dei toponimi nei testi, ispezione rapida |
| RomaTV (A3) | `video/rtv_census.py`, `video/rtv_build.py`, `video/rtv_speech.py`, `video/rtv_audio.py`, `video/rtv_audio_batch.sh`, `video/rtv_audio_measure.py`, `video/rtv_analyse.py`, `video/killaudio.sh`, `video/vtt_to_text.py` | censimento dell'API, statistiche delle confidenze, scaricamento a segmenti dell'audio HLS (ripresumibile), misure acustiche, analisi delle trascrizioni |
| YouTube (A4) | `video/yt_*.sh`, `video/yt_census_build.py`, `video/yt_parse_flat.py`, `video/json3_to_text.py`, `video/analyse_rec.py` | censimento dei canali, metadati, sottotitoli automatici a ritmo lento (anti-bot), analisi |

Uso tipico: copiare la cartella nello scratchpad della sessione e lanciare gli
script da lì; `rtv_audio.py` riprende dai segmenti già scaricati se la cartella
`<out>_segs/` esiste.

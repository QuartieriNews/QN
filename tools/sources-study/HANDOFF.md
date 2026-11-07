# Consegna alla sessione B (Opus 5): ricostruzione una tantum di giugno 2026

Scritta dalla sessione A (Fable) la sera del 15 settembre 2026, quando l'owner ha inserito la nuova chiave
OpenAI nelle variabili dell'ambiente: le sessioni in corso non rileggono la configurazione, quindi il lavoro
riparte in una nuova sessione dello stesso ambiente. Tutto lo stato utile è in questa cartella e nei documenti.

## 1. Cosa leggere prima (in quest'ordine)
`CLAUDE.md`, `AGENTS.md`; `docs/sources/FATTIBILITA_RICOSTRUZIONE_2026-06.md` §8–§9 (piano a cinque giorni,
tetto, consegne, regole sulla quota: §9.6); `docs/sources/SOURCE_STUDY_METHOD.md`; `docs/sources/SOURCE_REGISTRY.md`;
`docs/sources/TRIAL_LEDGER.md` (tetto e controlli Codex); `docs/sources/VIDEO_RICOGNIZIONE_2026-06.md` §6 (stile
delle schede); `tools/sources-study/README.md`; `tools/sources-study/lotto_opus5/SPECIFICA.md` (schemi di output e
regole di qualità già collaudati su Opus 5); `reviews/README.md` e `council/README.md` (come si eseguono i
controlli Codex).

## 2. Vincoli
- Tetto complessivo 78,86 €, spesi 0,86 €: **78,00 € disponibili**. Ogni spesa va nel ledger con i token. Nessun
  "extra usage", nessun abbonamento, nessun automatismo mensile: è uno studio una tantum.
- **Chiave OpenAI**: variabile `OPENAI_API_KEY` dell'ambiente (nuova). Prima di qualunque chiamata a pagamento:
  `curl -sS -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models`
  e registra **solo il codice HTTP** in `tools/sources-study/session_b/STATO.md`. Mai stampare, loggare o
  hashare il valore. Se il codice non è 200: nessuna chiamata a pagamento, prosegui con il lavoro indipendente
  e scrivilo in STATO.md.
- Rete: tutto passa dal proxy dell'ambiente (`REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`, `CURL_CA_BUNDLE`,
  `SSL_CERT_FILE`). Host già consentiti: comune.roma.it, api-ovp/identity-ovp/ac103mp/ac104mp.streamcloud.it,
  ovp2-live.akamaized.net, ws.comune.roma.it, culture.roma.it, questure.poliziadistato.it, carabinieri.it,
  youtube.com (googlevideo.com no); Hugging Face, GitHub releases, PyTorch, alphacephei bloccati (nessun ASR
  locale). Ritmi: YouTube un video al minuto con pause dopo due errori; Atti Web una richiesta ogni 1,3 s;
  RomaTV al massimo 4 scaricamenti in parallelo. Nessun cambio di IP, nessun aggiramento dei controlli.
- DEC-102 e DEC-104: testi integrali, PDF, audio e trascrizioni restano nello scratchpad; dati per item (CSV
  compatti) su Drive `QN Hub / 20 Packages / Fonti 2026-06/` (id cartella `1JQYkyES0zAGBNtiekXkVgWCS0Ee1RrIa`).
  Se il connettore Drive non è disponibile restano nello scratchpad e la consegna si dichiara incompleta
  con la causa: **mai nel repository** (metodo §4.2), salvo gli inventari senza testi di `handoff_data/` (DEC-109, §2-bis). La versione precedente di questo punto indicava
  `session_b/out/` nel repository come ripiego: era contraria alla regola ed è superata.
- Nomi delle persone: DEC-105 (17 settembre) supersede la regola «nessun nome di persona» che lo studio aveva
  costruito sopra la DEC-102: nei dati su Drive i nomi pertinenti al fatto si scrivono
  (`report2/SPECIFICA_NOMI_E_TERRITORIO.md`); nel repository i dati per item non entrano comunque.
- Quota: al massimo **2 subagenti Opus in parallelo** oltre alla sessione principale. Alla fine del primo giorno
  pieno chiedi all'owner la sola lettura della pagina Utilizzo e registrala in STATO.md; se il consumo supera
  3 punti settimanali per ora-subagente, un solo flusso (nota §9.5).
- All'owner arrivano solo: accessi e autorizzazioni indispensabili, decisioni editoriali irrisolte (raggruppate,
  con esempi e una raccomandazione che vale come default), consegne. Nessuna ora di controllo a suo carico.
- Ripresa senza presidio: prima di chiudere ogni turno programma un promemoria (`send_later`) o una Routine
  oraria durante i job lunghi; lo stato sta nei file, mai solo nella conversazione.
- Git: branch `claude/ecstatic-shannon-mjzxvq` (`git pull --rebase` prima di ogni push); prima di ogni commit
  tutte le suite di AGENTS.md: `cd gazetteer && python ../tests/test_guards.py`, `node tests/test_parse_duration.js`,
  `node tests/test_council.js`, `node tests/test_lane_gate.js`, `node tests/test_workflow_safety.js` (dopo `npm ci`),
  più `python3 tools/geo-assign/test_geo_assign.py` e `python3 tools/cronaca-prova/test_cronaca_prova.py`; righe di attribuzione
  della tua sessione nei messaggi di commit. Nessuna PR se l'owner non la chiede.

## 2-bis. Colonne tolte da `handoff_data/` il 15 ottobre 2026 (DEC-104, DEC-105 §1; decisione registrata in DEC-109)

Revisione Codex della PR #15, lotto 3: nove CSV portavano testo per item delle fonti
(titoli di notizie, atti e video; descrizioni con gli ordini del giorno; in un caso un nome
di persona dentro un ordine del giorno). Decisione dell'owner: togliere le colonne, senza
copia su Drive; le versioni complete restano nella storia git (commit `33a12d6` e
precedenti). Colonne rimosse: `A4_youtube_giugno2026_censimento.csv` (`titolo`,
`argomento_descrizione`, `verbale_match_oggetto`, `convocazione_match_oggetto`);
`A3_romatv_giugno2026_censimento.csv` (`titolo`, `descrizione`); `A3_speech_stats_giugno.csv`,
`A3_campione_selezione.csv` (`titolo`); `A4_campione_selezione.csv` (`titolo`, `tema`);
`A1xA2_campione60.csv` (`A1_titolo`, `A2_oggetto`); `DDSxA1_campione30.csv` (`A1_titolo`);
`A2_approfondimento_pdf_campione.csv` (`contenuto`); `A2_centrali_candidati_giugno.csv`
(`vicenda`, `possibile_notizia`). ID, URL, date, durate, conteggi ed etichette dello studio
restano: gli item si ritrovano dall'URL o dal `guid`.

## 2-ter. Testo derivato dalle fonti che resta nel repository per decisione dell'owner (16 ottobre 2026)

La revisione della PR #15 (lotto 6) ha segnalato quattro file versionati con testo derivato
dalle fonti. L'owner ha deciso di lasciarli come sono, con questa eccezione dichiarata:
- `session_b/STATO.md` e `session_b/DECISIONI_OWNER.md`: verbali di sessione, documenti storici
  non normativi, con citazioni ed esempi che sono il ragionamento dietro DEC-105;
- `reviews/T4_seconda_ai.md` e `reviews/T4_seconda_ai_larghi.md`: esiti per caso della prova T4
  (id, esito, campo, motivo), archivio della prova, non review nel senso di DEC-007;
- `docs/sources/RICOSTRUZIONE_2026-06_REPORT2.md` §§5–8: frasi brevi dalle registrazioni e dai
  verbali come prove delle conclusioni, e tre nomi pertinenti ai difetti illustrati (DEC-105).
Nessun altro file versionato può portare testi, titoli o nomi presi dalle fonti (DEC-102,
DEC-104, DEC-105 confine 1, DEC-109 per gli inventari).

## 3. Stato al passaggio (15 settembre, 20:15 ora italiana)
- Fatti: censimenti dell'intero mese per tutte le fonti (`handoff_data/`: A1, A2, DDS, centrali, C1–C5, E2, E3,
  A3 RomaTV, A4 YouTube, campioni di audit, confidenze delle 82 trascrizioni RomaTV); lotto di misura su Opus 5
  (§9.3); costi, calendario e piano (§9.5–§9.6); script in questa cartella; letture della quota in
  `session_b/quota_sessione_A.md`.
- Persi con la VM della sessione A, tutti riscaricabili: pagine HTML delle fonti testuali (A1 365, C1 79, C2 20,
  C4 8, E2 407, E3 104), PDF di Atti Web, audio RomaTV (appena iniziato), 18 sottotitoli YouTube, gli 82 JSON
  delle trascrizioni RomaTV, i cataloghi RomaTV.

## 4. Sequenza operativa
0. Setup (10 minuti): `export QN_NET=<tuo scratchpad>/net` (percorso dal tuo system prompt); `mkdir -p $QN_NET
   && cp -r tools/sources-study/* $QN_NET/ && cp gazetteer/gazetteer.json $QN_NET/` (geo_lookup.py lo cerca nel repository, con `QN_REPO_ROOT`, o accanto a sé); `mkdir -p $QN_NET/deliver $QN_NET/video/deliver_video`; copia i CSV
   di `handoff_data/` che iniziano per A1, A2, C, E, DDSxA1 in `$QN_NET/deliver/` e quelli che iniziano per A3,
   A4 in `$QN_NET/video/deliver_video/`; `apt-get install -y tesseract-ocr tesseract-ocr-ita`;
   `pip install pymupdf imageio-ffmpeg yt-dlp requests`.
1. Verifica della chiave (§2) e primo commit di `session_b/STATO.md` entro 15 minuti dall'avvio.
2. Recuperi lenti, tutti con `setsid nohup … &` e log: (a) RomaTV: `cd $QN_NET/video && python3 rtv_census.py`
   (30 richieste, salva `rtv/cat/*.json`), poi `python3 rtv_list_w2w4.py`, poi `./rtv_dl_w2w4.sh` (318 registrazioni,
   227,6 ore, ripresumibile a segmenti); gli 82 JSON delle trascrizioni dei Consigli sono in
   `tracks[].speechToTextTrackSource` degli item dei cataloghi (`https://ac104mp.streamcloud.it/speech/<file>.json`);
   (b) YouTube: `python3 yt_ids_all.py` poi `./yt_all_pass.sh 5`; (c) Atti Web: `python3 a2_list_all.py` poi
   `python3 a2_fetch_all.py` (scarica, estrae il testo, OCR delle scansioni in `A2_text/`).
3. **Report 1, entro il 17 settembre alle 19:00**: riscarica le fonti testuali (`a1_walker.py`, `a1_items.py`,
   `e2_walker.py`, `e3_walker.py`, `e3_items.py`; C1, C2, C4 con curl dagli URL delle inventari, cartelle
   `C1_items/` ecc.); `python3 report1/report1_extract.py`; lettura con subagenti Opus (2 in parallelo, lotti di
   40–60 item, output per item come il lotto A: notizie candidate con titolo, sintesi ≤ 60 parole, luoghi,
   evidenza = URL e data, tipo, qualità, data del fatto, data di pubblicazione, disponibilità); deduplicazione
   fra fonti; localizzazione con `geo_lookup.py`; database (CSV: fonti, documenti, notizie_candidate, vicende,
   territori; foglio Google se Drive è disponibile); copertura per Municipio e settimana, tempestività, lacune;
   filtro 8–28 giugno; rapporto `docs/sources/RICOSTRUZIONE_2026-06_REPORT1.md`; controlli Codex C1 (schema e
   regole, prima dell'estrazione) e C2 (campione) archiviati in `reviews/`; ledger aggiornato.
4. **Report 2, entro il 20 settembre alle 19:00, settimane 8–28 giugno**: atti (`A2_text/`) con lo schema del
   lotto B; 67 Consigli RomaTV e video YouTube con lo schema del lotto A (marcatori a 10 secondi, non 30);
   commissioni RomaTV: audio → `rtv_audio_measure.py <segdir> key.bin` per il remux (chiave AES da
   `https://api-ovp.streamcloud.it/garavot/ac104/streaming/encryption/key`, salvata come `key.bin` nello
   scratchpad) → trascrizione via API (`gpt-4o-mini-transcribe`, 0,003 $/min di listino; prima la prova T1 su
   2 ore per misurare il prezzo effettivo e registrarlo nel ledger; spezzoni sotto i 25 MB) → lettura con
   subagenti Opus → confronto con il Report 1 sulle stesse settimane: notizie distinte, copertura, sovrapposizioni,
   vicende approfondite, lacune colmate, difficoltà, costi effettivi; seconda AI indipendente sulle candidate
   (modello OpenAI, schema T4 del metodo); controlli Codex C3, C4, C5; rapporto
   `docs/sources/RICOSTRUZIONE_2026-06_REPORT2.md`.
5. Consegna comunque alle scadenze: inventari del mese, database con i collegamenti, rapporti con il materiale
   analizzato, mancante e incerto distinti; nessuna riduzione tacita del perimetro; "non verificato" dove resta
   incertezza.

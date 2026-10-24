# Storico dei quartieri: stato del wiki di contesto e piano «una settimana, un mese»

Richiesta dell'owner (24 ottobre 2026): recuperare il wiki storico delle notizie dei
quartieri, dire se è strutturato bene, e proporre un piano settimanale per scaricare le
commissioni e arricchire ogni settimana lo storico di un mese, usando come riserva la quota
Claude che a fine settimana resta inutilizzata (un'esecuzione di 24 ore l'ultimo giorno, dopo
approvazione). Con la domanda di fondo: ha senso, o il passato va cercato altrove, per esempio
nei soli atti e non nei video?

Questo è un documento di analisi del builder, non una decisione: ciò che cambia perimetro o
spesa sta in §7 come `OWNER_DECISION_REQUIRED`. Tutti i numeri sono **M** (misurati, con la
fonte) o **S** (stimati, con l'ipotesi). I dati per item restano su Drive (DEC-102, DEC-104,
DEC-109); qui stanno conteggi e procedure.

## 1. Dove sta il wiki e che cos'è

Il lavoro esiste: è la **pull request #17**, branch `wiki/giugno-2026`, decisa con
**DEC-022** il 23 ottobre (opzione A: il wiki resta nel repository, `docs/wiki/` costruito da
`tools/wiki/build_wiki.py`; i titoli di una riga scritti dai lettori dello studio sono
etichette, non testo delle fonti). Non è ancora fusa su `main` (M, 24 ottobre: aspetta lo
sblocco dei check di GitHub Actions; tre cicli Codex sul canale API, l'ultimo APPROVED).

Tre strati, in ordine di autorità: lo **schedario** (`schedario.json`: luoghi `L-`, soggetti
`S-`, questioni `Q-`), il **diario** (`diario.json`: una voce datata per notizia, con fonte,
Municipio, zona, luoghi, questione, qualità, esito di deduplicazione e riferimento alla
fonte) e le **pagine generate** (`INDEX.md`, `municipi/*.md`, `anteprima.html`). Ingresso: i
`Report*_notizie_*.csv` dello studio delle fonti di giugno 2026 (Drive, `Fonti 2026-06`) e il
registro fonti del 13 ottobre. Il wiki delle fonti eventi (`docs/wiki/fonti-eventi/`, sul
branch di questa PR) è un secondo ramo dello stesso impianto, non lo storico.

Il contenuto della prima versione, misurato sui JSON del branch (M):

| Misura | Valore |
|---|---|
| Voci di diario | 3.224, da sei fonti: A3 RomaTV 1.136, A2 atti 622, E2 496, A1 492, A4 YouTube 334, E3 144 |
| Mese coperto | giugno 2026 (2.758 pubblicate a giugno, 159 a luglio, 296 senza data di pubblicazione) |
| Questioni | 524, di cui 472 con almeno due voci; coerenza alta 316 · media 125 · bassa 83 |
| Luoghi | 3.471; 2.379 citati una volta sola; 209 agganciati a una zona del gazetteer; 56 coppie di grafie quasi uguali |
| Soggetti | 212, ma solo 19 ricorrono nel corpus: 193 vengono dal registro fonti con zero voci |
| Deduplicazione | 1.959 uniche, 1.265 dubbie (39%), nessun duplicato certo |

## 2. È strutturato bene? Sì come impianto, no ancora come storico

L'impianto è giusto e va tenuto: dati strutturati prima e pagine dopo, nessun testo delle
fonti, build deterministico con test (`tests/test_wiki_build.py`, 26 controlli), ogni voce con
l'evidenza (URL più pagina o `[mm:ss]`). È lo stesso principio che regge il gazetteer e il
wiki delle fonti eventi. DEC-022 lo ha già fissato, e non si riapre.

Ma l'obiettivo dell'owner — la storia completa di una vicenda, i progressi, da quanto tempo
va avanti — il wiki **oggi non lo serve**, per quattro ragioni misurate sui dati, tutte
correggibili nel build senza cambiare l'impianto:

1. **Le «questioni» sono sedute, non vicende.** Delle 524 questioni, 198 durano un giorno e
   326 da uno a tre giorni; **nessuna supera i tre giorni** (M). Il raggruppamento è quello
   ereditato dallo studio (stessa data e stesso luogo), cioè *la seduta* e i suoi atti. Lo
   strato che dice «la rotatoria dell'ex Dazio è in commissione da tre anni» non esiste: lo
   schema del database (`RICOSTRUZIONE_2026-06_SCHEMA_DB.md` §2 regola 3) prevedeva il legame
   esplicito fra notizie — stesso atto, stesso procedimento, citazione — con una confidenza
   dichiarata, ma il wiki non lo ha ricostruito. Finché manca, aggiungere mesi produce altre
   sedute isolate, non storia.
2. **Gli identificativi non reggono un secondo mese.** `L-` è la posizione del luogo nel
   build (`len(places)+1`), `N` e `Q-V` sono i progressivi dello studio di giugno: lo studio di
   maggio avrà di nuovo `N0001` e `V001`, e la rigenerazione rinumera tutti i luoghi. È lo
   stesso difetto che lo studio aveva già pagato e risolto per le notizie con `registro_id.csv`
   (schema §1.7). Il README promette «mai riscritto, solo esteso»; il codice ricostruisce da
   zero ad ogni esecuzione.
3. **Il collegamento alla fonte è rotto per il 59% delle voci.** 766 riferimenti (24%) sono
   URL troncati di Atti Web (`TU1W&par2=… p. 1`, senza host né percorso) e 1.136 (35%) puntano
   allo stream audio di Akamai (`…_audio_only.smil`) invece che alla pagina del portale
   RomaTV, che il censimento ha per ogni `guid` (`A3_romatv_giugno2026_censimento.csv`,
   colonna `url`). «Andare alla fonte» è la funzione per cui il wiki esiste, e per atti e
   registrazioni oggi non funziona.
4. **Un mese non è chiuso quando lo si legge.** Il 15 settembre i verbali di commissione
   (MMV) con repertorio a giugno erano 407; il 24 ottobre sono **503** (M, stessa
   interrogazione): un quarto dei verbali arriva uno-tre mesi dopo la seduta, e 159 voci del
   diario hanno già data di pubblicazione a luglio. Un piano mensile che non torna sui mesi
   precedenti lascia fuori proprio i verbali, che per la storia sono l'atto che chiude.

Due note minori: le 1.265 voci dubbie di deduplicazione entrano nelle pagine senza
distinzione dalle uniche; i soggetti del corpus sono 19, quindi lo strato «chi» (comitati,
uffici, gestori che ricorrono) è di fatto vuoto e per ora lo portano i luoghi.

**Correzioni proposte, tutte nel build** (una PR dopo la fusione della #17, prima di
aggiungere maggio): registro degli identificativi con chiave stabile (luogo: nome
normalizzato; voce: `<fonte>_<mese>_<progressivo>`; questione: registro proprio) e modalità
*append* con un file di diario per mese; riferimenti completi (URL del PDF per A2, pagina del
portale per A3, join sul `guid`); strato **vicende** sopra le sedute, costruito con le tre
regole dello schema (stesso identificativo di atto o seduta → alta; legame nominato → media;
sola continuità di luogo e oggetto → bassa) e mostrato nelle pagine con la confidenza; passata
di «ripasso» che riallinea i mesi aperti. Nessuna di queste richiede una decisione: sono
difetti rispetto a quello che il README già promette.

## 3. Che cosa c'è da scaricare, e quanto indietro

Archivi raggiungibili, misurati il 24 ottobre 2026 dall'ambiente (M):

| Fonte | Profondità | Volume al mese | Come si legge |
|---|---|---|---|
| **Atti Web, commissioni municipali** (MMC convocazioni, MMV verbali) | almeno **giugno 2018** (392 e 456 atti); il portale conserva serie dal 2010 | 2026-06 516 e 503 · 2025-06 541 e 624 · 2024-06 570 e 671 · 2022-06 473 e 663 | API di elenco; PDF testuali o scansioni (OCR Tesseract locale, provato); una richiesta ogni 1,3 s |
| **Atti Web, Consiglio e Giunta** (CMV, CMD, CMZ, CMR, GMD…) | idem | CMV 30–54 · CMD 26–72 al mese | idem |
| **Atti Web, DDS** (discipline di traffico) | errore sul 2018, presente dal 2022 | 2026-06 199 · 2022-06 308 (solo DMS; DDS 921 a giugno 2026) | idem; livello di strada |
| **RomaTV** (A3) | Municipio II 3.239 registrazioni dal **dic. 2021**; III 1.475 dal nov. 2021; VIII 2.431 dall'apr. 2022; XI 1.414 dall'apr. 2022; XII 2.553 dal dic. 2021; XV 1.958 dall'ott. 2021; X 667 dal nov. 2021; **Commissioni Capitoline 5.562 dal giu. 2020**; Assemblee 489 dall'apr. 2021 | giugno 2026: 496 registrazioni, 405 ore, di cui 82 Consigli con trascrizione della piattaforma | API del tenant; audio HLS cifrato scaricabile a segmenti (5–6 minuti di rete per ora di audio); commissioni **senza** trascrizione: serve l'API a pagamento |
| **YouTube** (A4) | Municipio I attivo (600 voci lette da gennaio 2026); IX attivo dal 2025; V fermo al 12 giugno 2026; IV, VI, VII, X, XIV, XV fermi dal 2020–2022 | giugno 2026: 131 registrazioni, 135 ore, 107 commissioni | sottotitoli automatici a costo zero, un video al minuto per il controllo anti-bot; nessun audio |
| **Notizie dei Municipi** (A1) | archivio paginato del portale | 365 al mese | HTML, già strumentato |

Due conseguenze per il piano. Gli **atti coprono tutti e quindici i Municipi per almeno otto
anni** e costano solo rete e OCR. I **video coprono otto Municipi su RomaTV da fine 2021,
due su YouTube**, e il loro testo per le commissioni costa 0,00261 $ al minuto (M, prova T1):
circa 280 ore al mese, cioè **≈ 40 € al mese** di trascrizione, più 23–28 ore di rete per
scaricare l'audio.

## 4. Atti soltanto, o anche i video? Atti sempre, video a tre velocità

Lo studio ha già risposto alla domanda di merito, e la risposta non è «uno o l'altro»:

- **Il parlato aggiunge quello che gli atti non hanno**: l'84,8% delle notizie nate in una
  seduta non sta in nessun atto (banda 80–88%, Report 2 §2); 107 verbali dichiarano che il
  record della seduta è la registrazione; nel Municipio I 17 verbali di commissione su 23 sono
  fogli di presenza; negli atti passa solo chi vince (le mozioni respinte non esistono). Per
  la *storia* di una vicenda il parlato porta proprio i fatti negativi — lavori fermi, risposte
  mai arrivate, pareri ritirati — che nessun atto registra.
- **Ma la trascrizione automatica non è un record**: inventa voti (nove «favorevole» dove
  l'aula ha respinto), storpia nomi e cifre senza segnalarlo, entra in loop (Report 2 §6). Le
  date, gli esiti di voto e gli identificativi — ciò che lega una vicenda nel tempo — vanno
  presi dall'atto. E la convocazione (MMC) porta già l'ordine del giorno: *di che cosa* ha
  parlato una commissione lo dice l'atto a costo zero; *che cosa è stato detto* lo dice il
  video a 40 € al mese.

Quindi, per mese storico:

| Livello | Che cosa | Costo esterno | Ore-subagente (S da M) | Quando |
|---|---|---|---|---|
| **A — scheletro** | tutti gli atti municipali (≈ 1.400–1.700) più le tipologie centrali con ricaduta territoriale (A2 §6) e, se decisa, DDS (≈ 900); Consigli RomaTV con trascrizione della piattaforma (≈ 80); sottotitoli YouTube (≈ 100–130); notizie A1 (365); **censimento di tutte le registrazioni** come voci di diario «registrazione disponibile» con data, organo, durata, convocazione abbinata e URL del portale | 0 € | ≈ 18–24 atti + ≈ 5 registrazioni + riserva ≈ **30** | ogni mese del piano |
| **B — merito** | trascrizione e lettura delle commissioni RomaTV (≈ 300 registrazioni, 230–280 ore) | ≈ 40 € + 23–28 h di rete | ≈ 20–25 | i mesi recenti, dove le vicende sono vive (proposta: gli ultimi dodici) |
| **C — a richiesta** | la singola commissione che una vicenda aperta richiede (il build la indica: voce «registrazione disponibile» non letta dentro una vicenda con più di N voci) | ≈ 0,15 € l'ora | minuti | sempre, su qualunque mese |

Il livello A da solo non è «meglio degli atti»: *è* gli atti più il parlato gratuito. Il
livello C è quello che rende sostenibile il passato lontano: la registrazione esiste nel
diario dal giorno del censimento, e si trascrive solo quando serve a una storia.

## 5. Il ciclo settimanale

Vincoli misurati che lo disegnano: il Report 2 (1.983 atti e 478 registrazioni) è stato
letto in **15,5 ore di orologio** con al più due subagenti (STATO §23→§126, 16 settembre); i
tassi per item sono 25 s per atto e 81 s per registrazione (×1,5 per le commissioni lunghe); la
ripresa dopo il ritiro della VM è dimostrata (STATO §7); lo scaricamento dell'audio e i
sottotitoli hanno ritmi imposti dalle fonti e non consumano quota. Il consumo settimanale di
quota per ora-subagente è **ancora non misurato**: il lotto del 15 settembre dà una forbice da
0,1 a 3,3 punti settimanali per ora-subagente (granularità di 1 punto), e il checkpoint «lettura
della pagina Utilizzo dopo il primo giorno pieno» previsto dal piano di settembre non è mai
stato registrato. Il primo ciclo serve anche a questo.

| Giorno | Chi | Che cosa | Quota |
|---|---|---|---|
| **1** (dopo il reset) | owner | sceglie il mese M, conferma il livello (A, A+B) e la spesa; due righe in chat | — |
| 1 | builder, pochi minuti | avvia in background, con stato nei file: elenco e PDF di Atti Web per M, OCR delle scansioni; censimento RomaTV e YouTube per M; audio delle commissioni (se B) a segmenti ripresumibili; sottotitoli YouTube a un video al minuto; promemoria orario (`send_later`) per sorvegliare | trascurabile |
| **2–5** | macchina | scaricamento (fino a 28 h di audio), trascrizione via API in coda con tetto di spesa; ogni mattina un controllo di un minuto dello stato | trascurabile |
| **6**, mattina | owner | legge la quota rimasta e dice sì o no all'esecuzione di 24 ore | — |
| **6–7** | builder, 24 h | lettura con **due** subagenti (atti in lotti da 50 con la specifica degli atti; registrazioni con la specifica dei video a marcatori di 10 s); `build_db.py` sul mese; `build_wiki.py` in append; campione di 30 righe verificato dalla sessione principale contro l'evidenza; consegna dei per-item compatti; commit dei soli derivati (`docs/wiki/`), PR | tutta quella che resta, entro le regole di §6 |
| **ripasso** (ogni 4 settimane) | builder, 1–2 h | rielenca M-1, M-2, M-3 su Atti Web: i verbali repertoriati dopo entrano nel diario e, se chiudono una vicenda, la chiudono | bassa |

**Ordine dei mesi**: a ritroso da **maggio 2026** (è quello che DEC-022 indica per primo e
l'unico mese in cui atti e video possono essere letti con lo stesso metodo di giugno senza
aspettare nulla), poi aprile, marzo… Nei primi dodici mesi livello A+B; dal tredicesimo in
poi livello A, con C a richiesta. A questo ritmo un anno di storico in dodici settimane,
quattro anni di video e otto di atti entro la profondità degli archivi.

**Un ciclo produce**: per il mese M, un file di diario (`docs/wiki/diario/AAAA-MM.json`),
lo schedario aggiornato in append, le pagine rigenerate, e su Drive i per-item con le sintesi;
in chat due numeri soltanto: voci aggiunte e vicende toccate.

Per il ciclo si usano gli strumenti già esistenti (`tools/sources-study/`: `a2_list_all.py`,
`a2_fetch_all.py`, `video/rtv_census.py`, `rtv_dl_w2w4.sh`, `rtv_transcribe.py`, `yt_*`,
`report1/build_db.py`, `report2/SPECIFICA_ATTI.md`, `SPECIFICA_VIDEO.md`) parametrizzati sul
mese invece che cablati su giugno; è lavoro di builder, una PR per strumento.

## 6. È una buona idea come riserva per la quota? Sì, a sei condizioni

Sì: la lettura è il lavoro che consuma quota, è parallelizzabile, riparte da sola dai file,
e una quota settimanale non spesa si azzera al reset — non c'è un uso più economico. Ma solo se:

1. **Il materiale è già a terra prima delle 24 ore.** Lo scaricamento dell'audio (fino a 28 h)
   e i sottotitoli YouTube (un video al minuto) non possono stare dentro la finestra di lettura:
   partono il giorno 1. Un'esecuzione di 24 ore che aspetta la rete spreca la quota aspettando.
2. **Due subagenti, non tre**, e nessun «extra usage»: è la regola già misurata (fino a 5
   punti della finestra di 5 ore per ora-subagente; un terzo flusso continuo non ci sta).
   Soglia di arresto scritta prima di partire (per esempio: fermarsi al 10% settimanale
   residuo), controllata dalla sessione principale a ogni lotto.
3. **Il primo ciclo misura la quota**: lettura della pagina Utilizzo prima e dopo le 24 ore,
   registrata nel repository. Senza, «un mese a settimana» è un'ipotesi: la forbice attuale va
   da 5 a 160 punti settimanali per 48 ore-subagente.
4. **La consegna dei per-item non passa dal connettore Drive.** La consegna di giugno è costata
   ≈ 5 milioni di token per 4,6 MB (1,15 token per byte, STATO §134): a regime sarebbe una delle
   voci più pesanti del ciclo. Alternativa a costo quasi zero: un archivio compresso mandato
   all'owner in chat (`SendUserFile`), che lo carica su Drive; oppure un percorso deciso
   dall'owner (§7).
5. **Il protocollo è quello di produzione, non dello studio.** Lo studio ha fatto audit a
   campione a tre lettori, seconda AI, cinque controlli Codex: serviva a misurare il metodo.
   Il ciclo mensile fa una lettura, un campione di 30 righe verificato dalla sessione
   principale, e un controllo Codex a campione **ogni quattro mesi**, non ogni mese.
6. **Il lavoro di giudizio non cresce con la quota.** DEC-022 condiziona l'uso del wiki alla
   divisione delle questioni a coerenza bassa da parte di una persona: sono 83 su giugno, cioè
   ≈ 80 al mese. Con lo strato vicende di §2 il problema si riduce (una seduta multi-argomento
   non è più una «questione»), ma la coda resta e va misurata al primo ciclo; se supera quello
   che l'owner può leggere, la divisione la fa un subagente con verifica a campione, e lo si
   decide allora.

Quello che il piano **non** fa: non legge Roma Today né altre testate (DEC-108: solo titolo,
link e ora), non aggira il controllo anti-bot di YouTube né i blocchi di Questura e
Carabinieri, non mette per-item nel repository pubblico, non tocca la produzione n8n. E non
promette velocità: il primo ciclo è una misura.

## 7. Decisioni richieste all'owner (`OWNER_DECISION_REQUIRED`)

| # | Domanda | Opzioni | Raccomandazione (vale come default se non c'è risposta) |
|---|---|---|---|
| D1 | Fusione della PR #17 così com'è, con le correzioni di §2 in una PR successiva, o correzioni prima della fusione? | (a) fondere ora, correggere dopo; (b) correggere nella #17 | (a): DEC-022 è decisa sulle pagine reali e la review è chiusa; le correzioni sono un cambiamento a sé, da rivedere da solo |
| D2 | Ordine e profondità dei mesi | (a) a ritroso da maggio 2026, dodici mesi A+B poi solo A; (b) solo gli ultimi sei mesi; (c) altro | (a) |
| D3 | Livello B (trascrizione delle commissioni, ≈ 40 € al mese) | (a) sì per i mesi recenti; (b) mai, solo C a richiesta; (c) sempre | (a), con un tetto mensile scritto nel ledger prima di ogni ciclo |
| D4 | Dove vanno i per-item di ogni mese | (a) archivio in chat caricato dall'owner su Drive; (b) connettore Drive dal builder (≈ 5 M token al mese); (c) altro percorso | (a) |
| D5 | Tipologie centrali e DDS nel livello A (A2 §6, ancora «da decidere») | (a) GCD, AZ, AY, GCM, ACD con ricaduta territoriale sì, DDS sì; (b) solo municipali | (a): le DDS sono l'unica fonte a livello di strada e la storia di una strada è quella |
| D6 | Regola della quota per le 24 ore | (a) via libera dell'owner ogni volta, dopo la lettura della quota; soglia di arresto al 10% residuo; due subagenti | (a) |

Nessuna spesa e nessuna esecuzione è autorizzata da questo documento.

## 8. Da dove viene ogni numero

| Numero | Fonte |
|---|---|
| contenuto del wiki (3.224 voci, 524 questioni, durate 0–3 giorni, riferimenti troncati 766 e stream 1.136, luoghi 3.471) | `schedario.json` e `diario.json` del branch `wiki/giugno-2026` a `f8a547a`, contati il 24 ottobre 2026 |
| MMV di giugno 2026: 407 → 503 | `A2_ATTIWEB_TIPOLOGIE.md` §3 (15 settembre) e interrogazione del 24 ottobre, stesso filtro `dtRpr` |
| volumi mensili di Atti Web 2018–2026 | interrogazioni del 24 ottobre a `filtro-dati!cerca.action` (`hitCountRicerca=1`, `itemsPerPage=1`) |
| profondità dei cataloghi RomaTV | `contents/search_frontend` del 24 ottobre, ordinamento per `ReferenceDate` ascendente, una voce per catalogo |
| 496 registrazioni, 405 ore, 82 trascrizioni; 131 e 135 ore su YouTube; stato dei canali | `VIDEO_RICOGNIZIONE_2026-06.md` §3; `handoff_data/A4_canali_youtube_stato.csv` |
| 84,8% [80,2; 88,0]; 107 verbali; 17 su 23; trascrizione che inventa voti; 0,00261 $/min | `RICOSTRUZIONE_2026-06_REPORT2.md` §1, §2, §3, §6 |
| 25 s per atto, 81 s per registrazione; 3,3–6,7 punti-finestra per ora-subagente; 0–2 punti settimanali per 0,6 ore | `FATTIBILITA_RICOSTRUZIONE_2026-06.md` §9.3; `session_b/quota_sessione_A.md` |
| 15,5 ore per Report 2; ripresa dopo il ritiro della VM; 1,15 token per byte su Drive | `session_b/STATO.md` §7, §23, §126, §134 |
| 5–6 minuti di rete per ora di audio; un video al minuto; una richiesta ogni 1,3 s | `VIDEO_RICOGNIZIONE_2026-06.md` §2; `tools/sources-study/HANDOFF.md` §2 |

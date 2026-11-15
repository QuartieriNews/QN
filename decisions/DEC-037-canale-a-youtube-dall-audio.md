# DEC-037 — Canale A: le sedute di YouTube dall'audio, e la spesa tenuta sotto controllo

Status: DECIDED (15 novembre 2026, owner, sulle proposte del builder)
Supersedes in part: DEC-036, punto 3 (YouTube del Municipio I: il feed e i sottotitoli
automatici, mai l'audio); nel punto 4 la sola cifra della quota di A; nel punto 5 il «solo»
per il testo dei sottotitoli di ultima riserva, che prima di `temporanei/` passa dallo
storage di una corsa di Apify (punto 3). DEC-036 resta invariata e non si riapre; riceve un
rimando sotto la riga `Status:` (`decisions/README.md`, regola 2). Per tutto il resto
DEC-036 resta in vigore.
Blocks: nothing.

Question: dopo il blocco del 14 novembre, da dove viene il testo delle sedute del
Municipio I, che stanno solo su YouTube, e come si tiene sotto controllo la spesa che ne
segue?

Contesto:
- Il 14 novembre la pagina del video di YouTube ha dato a n8n la pagina di consenso UE; per
  DEC-036, punto 3, era un segnale di blocco, e Prati è rimasto senza testo
  (`docs/pilota/WORKSTREAM_A.md`, sezione 2, com'era).
- YouTube blocca soprattutto per provenienza (i server dei centri dati), non per numero di
  richieste: da n8n direttamente lo scaricamento non è una strada affidabile.
- Giugno 2026 (CSV A4 di `tools/sources-study/handoff_data/`): il canale del Municipio I ha
  77 registrazioni, 42,1 ore (commissioni 38,6, Consiglio 3,5), circa 2–3 video al giorno. A
  regime anche le commissioni del Municipio IX sono solo su YouTube (38,2 ore).
- Prezzi di listino letti sulle pagine di due Actor di Apify il 15 novembre, da verificare
  alla prova: `datapipe/youtube-video-downloader` 0,006 $ a video scaricato, un prezzo solo
  anche per il solo audio; `lurkapi/youtube-to-mp3-audio-downloader` 0,002 $ al minuto di
  audio. Sono di due sviluppatori diversi; il primo dichiara di usare proxy residenziali.
  Il prezzo di un Actor per l'elenco dei video di un canale non è stato letto: si legge
  prima della prova.
- La trascrizione nostra delle 42 ore di Prati costa circa 6 € al mese (0,157 $ l'ora,
  misura di giugno), fuori dalla stima di `WORKSTREAM_A.md`, sezione 7, com'era, che
  contava sui sottotitoli.
- Stima del builder a regime (15 Municipi, commissioni capitoline, Assemblea; giugno):
  circa 410 ore al mese da trascrivere noi (RomaTV circa 330, YouTube circa 80; 77 ore di
  Consigli già trascritte dalla piattaforma), circa 80 € al mese per il canale A al modello
  di oggi, prima della scrittura. Il grosso è la trascrizione, non Apify.
- DEC-036 registra nel suo contesto che scaricare l'audio va contro le condizioni di
  YouTube; il suo punto 3 diceva «mai l'audio» e vietava di aggirare un blocco con client
  finti o proxy.
- Le regole di YouTube per chi usa l'interfaccia ufficiale (YouTube API Services Developer
  Policies, III.E.1 e III.I.7, lette il 15 novembre 2026) vietano a chi la usa di scaricare
  o conservare copie dei contenuti, di isolarne l'audio e di aiutare altri a farlo. La
  proposta prendeva l'elenco dei video da quell'interfaccia, con una chiave di un progetto
  Google Cloud dell'owner, che così restava esposto.

Options: le proposte del builder nella sessione «Stato workflow aperti», che l'owner ha
accolto; sono i punti della Regola. Sull'elenco dei video il builder ha poi posto due
opzioni, nella sessione del coordinatore dello stesso giorno, dopo aver letto le regole
dell'interfaccia ufficiale (Contesto):
A. Dall'interfaccia ufficiale di YouTube, come nella proposta, con il rischio scritto e la
   chiave in un progetto Google Cloud a sé.
B. **CHOSEN.** Da un Actor di Apify, come l'audio, senza nessuna chiave di Google.

Claude recommendation: per il resto le proposte sono del builder, e il passaggio della
sessione non registra altro. Sull'elenco: B, perché toglie l'account Google dell'owner da un
uso che le regole dell'interfaccia vietano.

Owner's words, 15 novembre 2026:
- «La qualità dell'audio e la successiva trascrizione è fondamentale per la riuscita del
  progetto. Informazioni sbagliate portano a vie capite male e geografia del quartiere
  sballata. Quindi confermo che si lavora sempre sugli audio di buona qualità.»
- «Non mi preoccupa usare Apify». Lo preoccupano i costi a regime e la dipendenza da Apify.
- «Sì, scrivi la decisione, i 6 € prendili da C. Le tue proposte sono accordate. Le regole
  di spesa anche, ma non come blocco ma come cosa da tenere sotto controllo.»
- Sull'elenco dei video, fra le opzioni A e B (sessione del coordinatore): «Da Apify».

## Regola

Qui stanno le scelte; il modo di leggere le fonti sta in CONTRATTI, sezione 7,
«A · Amministrazione», e si corregge con una PR, purché resti dentro queste regole. Dove
una regola va oltre le parole dell'owner o la proposta accolta, lo dice: è una lettura del
builder, che l'owner conferma con il merge.

1. **Sempre l'audio, di buona qualità.** Per tutte le fonti delle sedute, YouTube compreso,
   il testo viene dalla nostra trascrizione dell'audio, scaricato nella qualità migliore
   disponibile per la sola traccia audio. I sottotitoli automatici di YouTube non sono più
   la strada principale: restano solo l'ultima riserva (punto 3). Lettura del builder: dove
   la piattaforma ha già la sua trascrizione (oggi i Consigli su RomaTV) si usa ancora
   quella, come in CONTRATTI, sezione 7 A, «Testo»: la stima accolta (Contesto) lascia
   fuori le 77 ore di Consigli già trascritte dalla piattaforma.
2. **YouTube, nel pilota solo il canale del Municipio I** (`UCEZtd0d0UV5e8ZCWkNOiNjw`):
   - l'elenco dei video da un Actor di Apify, al posto del feed e senza nessuna chiave di
     Google (Options, B): deve coprire la finestra di 100 giorni di CONTRATTI, sezione 7 A,
     così un video non si perde se lo scaricamento si ferma per qualche giorno; che l'Actor
     la copra lo dice la prova;
   - l'audio da un Actor di Apify, chiamato da n8n; pochi video al giorno (al più 5), uno
     alla volta;
   - mai un login con un nostro account Google o YouTube, né cookie nostri;
   - l'audio resta su Apify solo il tempo della trascrizione, poi si cancella, insieme allo
     storage della corsa; non va mai su Drive né altrove. Il testo
     resta privato in `originali/`, con il confine della seduta, come per RomaTV (DEC-036).

   Lettura del builder, che l'owner conferma con il merge: è un'eccezione alla sezione 6
   di CONTRATTI, al posto di quella di DEC-036, punto 3, e vale solo per questo canale.
   Scaricare l'audio resta contro le condizioni di YouTube, e un Actor raggiunge YouTube
   con mezzi suoi, proxy compresi, anche per l'elenco: è quello che DEC-036, punto 3,
   vietava (Contesto).
   L'owner lo accetta per questo canale; la scelta è sua, anche sul piano legale. Di quel
   divieto resta solo la parte su un nostro login e cookie nostri. n8n non chiede più
   niente a YouTube, né al sito né all'interfaccia ufficiale: l'elenco, l'audio e i
   sottotitoli di riserva arrivano da Apify.

   Lettura del builder, sull'audio: «non va mai su Drive né altrove» vuol dire che non lo
   conserviamo in nessun altro posto. Per essere trascritto l'audio passa dalla memoria di
   una corsa di n8n, che non salva i dati di quelle esecuzioni, e va a pezzi al servizio di
   trascrizione, come quello di RomaTV (DEC-036, punti 2 e 5). Che cosa quel servizio
   conserva lo dicono le sue condizioni, che si leggono prima di fissare il modello
   (punto 4). «Il tempo della trascrizione» può durare più corse: lo storage della corsa di
   Apify resta finché il testo non è completo, poi si cancella.
3. **Principale e riserva.** Se il principale fallisce si usa la riserva; se fallisce
   anche la riserva, i sottotitoli automatici; se non si ottiene niente, il video resta da
   fare, si riprova nelle corse dopo dentro la finestra e si avvisa l'owner.
   - La riserva vera sta **fuori da Apify**: un piccolo programma su un computer con
     connessione di casa, o un servizio di un'altra azienda. Il builder propone le opzioni,
     l'owner sceglie (serve hardware o un account nuovo).
   - Finché non c'è, la riserva è un secondo Actor di Apify di un altro sviluppatore.
   - Gli Actor precisi, anche quello dell'elenco, li sceglie il builder dopo la prova,
     preferendo un prezzo fisso a risultato. Per quello dell'elenco è una lettura del
     builder: l'opzione B dice «come l'audio».
   - Lettura del builder: anche i sottotitoli di ultima riserva arrivano da un Actor, non
     da n8n verso `www.youtube.com`; come, lo fissa la PR del testo (A3). Il loro testo
     passa quindi dallo storage di quella corsa, che si cancella come quello dell'audio
     (punto 2).
4. **La qualità dei nomi di luogo.** La prova di confronto della trascrizione
   (`WORKSTREAM_A.md`, sezione 6) si allarga:
   - modelli: `gpt-4o-mini-transcribe`, `whisper-1` e i servizi più economici basati su
     Whisper (per esempio `whisper-large-v3-turbo` di Groq, prezzo da verificare);
   - ognuno con e senza una guida dei nomi;
   - si giudica prima sulla correttezza dei nomi di luogo (vie, piazze, luoghi del
     Municipio), poi sul resto, poi sul costo;
   - si sceglie un modello che non si spenga a pilota in corso; il tetto della prova resta
     1 €.

   Lettura del builder: «si allarga» vuol dire che nel confronto resta anche
   `gpt-transcribe`, se il suo prezzo ci sta, come nel brief. I modelli accettano una guida
   corta (poche centinaia di parole),
   quindi i nomi si prendono dall'ordine del giorno della seduta (atti del canale D) e dai
   luoghi principali del Municipio nel gazetteer. In A5, prima di pubblicare, ogni luogo si
   controlla sul gazetteer e sugli atti. Un testo che viene dai sottotitoli automatici
   (`transcript_source` = `youtube_asr`) porta i suoi fatti in coda di revisione.
5. **Quote** (CONTRATTI, sezione 5): 6 € al mese da C ad A. Le quote diventano A 33 €,
   B 8 €, C 4 €, D 3 €, Riserva 2 €; il totale resta 50 € (DEC-031, punto 6).
6. **La spesa si tiene sotto controllo, non si blocca.** Nessuna regola di questa decisione
   ferma un flusso per la spesa.
   - Ogni chiamata ad Apify, come ogni spesa, ha il suo file in `costi/` (CONTRATTI,
     sezione 5).
   - Il coordinatore riporta all'owner la spesa del mese per workstream e il totale di
     Apify, e lo avvisa quando una quota o il totale del pilota (50 €) passano il 50 % e
     l'80 %. Lettura del builder: per questi avvisi, durante il mese, i dollari si contano
     al cambio prudente delle stime, 0,92 € per dollaro (`docs/sources/TRIAL_LEDGER.md`);
     il totale del mese resta quello di DEC-035, con il tasso della BCE.
   - Una prova fatta da una chat dichiara prima la spesa prevista e dopo quella fatta.
   - Il limite mensile dell'account Apify è un'impostazione dell'owner su Apify: questa
     decisione non lo tocca.

Impact:
- `docs/pilota/CONTRATTI.md`: sezione 5, le quote e la riga del 15 novembre; sezione 6, la
  voce «Sedute registrate»; sezione 7 A, le righe «Fonti», «Raccolta», «Testo», «Confine
  della seduta» e «Costi».
- `docs/pilota/WORKSTREAM_A.md`: Prati, i mezzi e gli stati (sezioni 3 e 4), l'elenco (A2)
  e l'audio (A3) da Apify, la prova allargata, la stima con Prati e la nota a regime, i
  punti aperti.
- Il rimando sotto `Status:` in DEC-036.
- Canale C: la sua quota scende a 4 € al mese (punto 5).
- Dall'owner: la credenziale Apify di n8n usabile dai flussi `staging_A`
  (`docs/pilota/WORKSTREAM_A.md`, sezione 3); la scelta della riserva fuori da Apify, sulle
  opzioni che porta il builder. Nessuna chiave di Google.
- Niente in produzione; gazetteer, prompt, registro dei venue e CI invariati. DEC-031,
  punto 6, e DEC-035 restano invariate.

Decided by: owner · Date: 15 novembre 2026 · Affected components: canale A del pilota,
canale C (quota a 4 €), `docs/pilota/CONTRATTI.md` (sezioni 5, 6 e 7 A),
`docs/pilota/WORKSTREAM_A.md`, DEC-036, flussi `staging_A_*`, l'account Apify.

# DEC-035 — Canale A: le sedute registrate per il blocco «Dal Municipio»

Status: DECIDED (14 novembre 2026, owner nella sessione del builder, sulle opzioni poste dal builder)
Blocks: nothing.

Question: come si apre il canale A del pilota (DEC-031, punto 2A) sulle sedute registrate: da
quali fonti, come si leggono, che cosa si trascrive, che cosa si conserva e con quale spesa?

Contesto:
- Giugno 2026, in ore (`docs/sources/VIDEO_RICOGNIZIONE_2026-06.md`, sezione 3.7; i CSV A3 e
  A4 in `tools/sources-study/handoff_data/`): Consigli di I, V e X 16,3; commissioni del I
  38,6 (YouTube), del V 18,3 e del X 12,1; commissioni capitoline 51,6; Assemblea capitolina
  41,3. La piattaforma trascrive solo i Consigli municipali (82 su 86); alcuni Consigli del V
  sono usciti fino a 36 giorni dopo la seduta.
- Sonde del builder su n8n Cloud, 14 novembre (flussi `staging_A_sonda_*`, spenti dopo le
  corse di prova; circa 0,20 $): l'elenco di RomaTV risponde senza login; l'audio delle commissioni è
  HLS cifrato AES-128, con la chiave che il portale dà a ogni spettatore senza login; farne un
  M4A in un nodo Code e trascriverlo con OpenAI funziona. Le esecuzioni 919 (audio dei primi
  6 minuti, nessun testo: OpenAI ha rifiutato l'ADTS grezzo), 921 e 922 (audio e testo dei
  primi 10 minuti) sono state cancellate su n8n per il confine della seduta, e con loro le copie
  nei file di lavoro della sessione.
- Regole degli host, lette da n8n il 14 novembre (la seconda volta alle 13:23 UTC). L'HTML
  della home del portale, un'applicazione JavaScript, non ha link a condizioni d'uso; la
  pagina disegnata non è stata vista. Le note legali del Comune, lette per DEC-033, non hanno
  una regola sull'accesso automatico.

| Host | `robots.txt` | A che cosa serve |
|---|---|---|
| `streaming.comune.roma.it` | `Allow: /` | il portale; il WebVTT dei Consigli |
| `api-ovp.streamcloud.it` | 503 due volte: illeggibile | l'elenco e la chiave dell'audio |
| `ac104mp.streamcloud.it` | `Allow: /` | il riconoscimento vocale dei Consigli |
| `ovp2-live.akamaized.net` | una pagina HTML al posto delle regole | l'audio |
| `identity-ovp.streamcloud.it` | `Disallow: /` | niente |
| `www.youtube.com` | vieta `/feeds/videos.xml` e `/api/` | il feed, la pagina del video e i sottotitoli automatici |

- Il Municipio I pubblica le sedute solo su YouTube (su RomaTV due voci, del 2021); il canale
  del V non ha sedute dopo il 12 giugno 2026 (VIDEO_RICOGNIZIONE, sezioni 3.1 e 3.5), quello
  del X è fermo da febbraio 2025. Scaricare
  l'audio è contro le condizioni di YouTube. A settembre i sottotitoli automatici sono
  arrivati solo tramite client di yt-dlp che imitano le app e i lettori di YouTube, e il
  controllo anti-bot è scattato dopo circa 20 estrazioni di video in 5 minuti
  (VIDEO_RICOGNIZIONE, sezione 2). Il 14 novembre, da n8n, il feed del canale risponde; la
  pagina del video dà la pagina di consenso UE, senza la lista dei sottotitoli.
- I marcatori del confine della seduta (DEC-105) stanno nella trascrizione completa, ma il
  fuori seduta non entra nei file né nei log
  (`tools/sources-study/report2/SPECIFICA_NOMI_E_TERRITORIO.md`, sezione 2).
- Prima di questa decisione la quota di A era 20 € al mese, per la trascrizione, e le quote
  dei workstream e della riserva sommavano i 50 € di DEC-031, punto 6
  (`docs/pilota/CONTRATTI.md`, sezione 5). Il 14 novembre l'owner ha condiviso le
  credenziali n8n «OpenAI account» e «Google Drive account» (progetto QuartieriNews) con il
  progetto personale dei flussi `staging_`.

Owner's words, 14 novembre 2026: «Apriamo io Canale, definiamo i mezzi che ci servono per
costruire su N8N i flusso completi e per testarlo. Non dobbiamo creare lo storico ma il flusso
per le sedute futuro.partendo da quelle che sono ora disponibili. Abbiamo commissioni
Capitoline che finiscono in parte in quartieri specifici e quelle municipali che andranno
sicuramente a toccare quartieri. Prepara il workstream.» e «Io sono qui per supportarti con
accessi, credito o approvazioni ma prendi decisioni per tutto ciò che prevede costi inferiori
ai 5 euro».

Il builder ha poi posto quattro domande, con le opzioni qui sotto.

**1. RomaTV.** Il portale permette tutto; l'host dell'elenco risponde 503 a `robots.txt`,
quello dei media dà una pagina HTML al posto delle regole; l'audio delle commissioni è cifrato
AES-128, con una chiave che il portale dà a ogni spettatore senza login. Per le regole dei
canali già aperti un host senza regole leggibili non si legge. Che cosa autorizza l'owner per
le sedute aperte?

Options:
A. **CHOSEN.** Sì, lettura lenta: elenco e audio letti come fa il lettore del portale, una
   richiesta alla volta, con pause. L'audio non si conserva mai: resta solo il testo della
   seduta aperta, con credito e link alla registrazione. È l'unica via al parlato delle
   commissioni; la decisione resta dell'owner anche sul piano legale.
B. Solo trascrizioni ufficiali: niente audio, solo le trascrizioni che il portale pubblica
   già, cioè i Consigli di V e X. Le commissioni, municipali e capitoline, restano fuori.
C. Prima chiedere a Roma Capitale: si scrive all'ufficio della Web TV e si aspetta la
   risposta. Intanto il canale A non legge nulla.

Claude recommendation: A, l'unica via al parlato delle commissioni.

Owner's answer: «Sì, lettura lenta».

**2. Prati.** Il Municipio I pubblica le sedute solo su YouTube. `robots.txt` di YouTube vieta
il feed dei video e i sottotitoli automatici (`/feeds/videos.xml` e `/api/`), e scaricare
l'audio va contro le condizioni di YouTube. Come si tratta Prati?

Options:
A. Senza parlato per ora: nessuna lettura da YouTube. Si chiede al Municipio I di pubblicare
   anche sulla Web TV di Roma Capitale, come ha fatto il X; intanto «Dal Municipio» di Prati
   viene dagli atti dello storico.
B. Elenco con la YouTube Data API: l'owner crea una chiave gratuita; le sedute si elencano e
   si collegano, senza testo parlato, e le notizie vengono solo dall'ordine del giorno.
C. Sottotitoli nonostante `robots.txt`: un'eccezione dell'owner alla sezione 6 di CONTRATTI,
   per leggere i sottotitoli automatici, con il rischio anti-bot e la questione delle
   condizioni d'uso. Sconsigliata.

Claude recommendation: A; C sconsigliata per il rischio anti-bot e le condizioni d'uso.

Owner's answer, scritta al posto delle opzioni: «Scarichiamo il testo lo stesso, con cautela
per evitare ban». Nessuna delle tre opzioni è scelta come posta; come il builder legge la
risposta lo dice il punto 3 della Regola.

**3. Assemblea capitolina.** Le commissioni capitoline si trascrivono tutte, circa 52 ore e
8 € al mese, e se ne tengono solo i fatti che cadono nei Municipi I, V e X; con le commissioni
municipali di V e X si arriva a circa 15 € al mese, dentro i 20 € della quota A. L'Assemblea
vale altre 41 ore al mese, circa 6,5 €, e quasi sempre parla della città intera. Si include?

Options:
A. Fuori per ora: si parte con le commissioni capitoline e municipali; l'Assemblea si
   rivaluta dopo il primo mese, con i costi veri.
B. **CHOSEN.** Dentro, quota A a circa 27 €: si trascrive anche l'Assemblea; la quota A sale a
   circa 27 € al mese, e il totale del pilota resta sotto i 50 €.
C. Solo i punti sui Municipi pilota: si trascrivono solo i punti dell'ordine del giorno che
   riguardano I, V e X. Costa meno, ma serve prima leggere l'ordine del giorno di ogni seduta.

Claude recommendation: A, per decidere sull'Assemblea con i costi del primo mese.

Owner's answer: «Dentro, quota A a ~27 €». Sul resto della domanda (le commissioni capitoline
tutte, con i soli fatti di I, V e X) l'owner non ha obiettato. Che cosa l'opzione B non
diceva sulle altre quote è in Impact.

**4. Fuori seduta.** Per trovare apertura, sospensioni e chiusura di una seduta bisogna
trascrivere tutta la registrazione, compreso il parlato fuori seduta. DEC-105 tiene fuori
dall'analisi ciò che non sta nella seduta aperta; la specifica di giugno aggiunge che non entra
in file o registri. Come si gestisce la trascrizione intera?

Options:
A. **CHOSEN.** Temporanea, poi cancellata: la trascrizione intera sta in una cartella privata
   temporanea su Drive solo finché i confini sono fissati, poi si cancella. Resta solo il
   testo della seduta aperta, e n8n non conserva i dati delle esecuzioni riuscite.
B. Mai scritta: i confini si cercano pezzo per pezzo mentre si trascrive, e su Drive va solo
   il testo dentro la seduta. È più complesso, con il rischio di tagliare male una ripresa
   non dichiarata.
C. Conservata in privato: la trascrizione intera resta in `originali/`, privata, ed esclusa
   dall'analisi. È la via più semplice, ma va contro la specifica di giugno.

Claude recommendation: A; B rischia di tagliare male una ripresa non dichiarata, C va contro
la specifica.

Owner's answer: «Temporanea, poi cancellata».

## Regola

Qui stanno le scelte; il modo di leggere le fonti sta in CONTRATTI, sezione 7,
«A · Amministrazione», e si corregge con una PR, purché resti dentro queste regole. Dove una
regola va oltre le parole dell'owner o l'opzione scelta, lo dice: è una lettura del builder,
che l'owner conferma con il merge.

1. **Sedute future.** Il canale non costruisce lo storico: legge le sedute future, partendo da
   quelle già pubblicate. Lettura del builder, che l'owner conferma con il merge: entrano le
   sedute dal 1° novembre 2026; fino alle PR della lettura dei fatti, della geografia, delle
   classi editoriali, della scrittura e della seconda verifica (DEC-015, se l'owner la
   conferma per il pilota: `docs/pilota/WORKSTREAM_A.md`, sezione 9) il canale non scrive
   elementi, come B (#36): solo record delle registrazioni, originali, testo della seduta
   aperta, registri delle corse e spese in `costi/`; il testo intero sta in `temporanei/` solo
   finché serve (punto 5). L'elenco esatto è in CONTRATTI, sezione 7 A.
2. **RomaTV, lettura lenta** (domanda 1, opzione A). Elenco e audio si leggono come fa il
   lettore del portale, una richiesta alla volta, con pause. L'audio non si conserva mai:
   resta il testo della seduta aperta, con credito e link alla registrazione (DEC-102).
   Lettura del builder, che l'owner conferma con il merge: si legge solo da
   `streaming.comune.roma.it`, `api-ovp.streamcloud.it`, `ac104mp.streamcloud.it` e
   `ovp2-live.akamaized.net`, mai da `identity-ovp.streamcloud.it`; l'audio si apre solo con
   la chiave che il portale dà a ogni spettatore, senza account. È un'eccezione alla sezione 6
   di CONTRATTI per gli host dell'API e dei media, le cui regole non si leggono, solo per le
   sedute del punto 4; se le regole di un host diventano leggibili, valgono quelle. Al primo
   segnale di blocco (401, 403, 429, captcha, pagina di accesso) la lettura si ferma, non si
   aggira e si avvisa l'owner. Le regole dei canali B e C non cambiano.
3. **YouTube, solo il canale del Municipio I** (`UCEZtd0d0UV5e8ZCWkNOiNjw`). L'owner, sulla
   domanda 2: «Scarichiamo il testo lo stesso, con cautela per evitare ban». Lettura del
   builder, che l'owner conferma con il merge: è un'eccezione alla sezione 6 di CONTRATTI, per
   questo canale e per due cose sole, il feed (l'elenco) e i sottotitoli automatici; mai
   l'audio. «Con cautela» vuol dire: ritmo lento, poche richieste al giorno, una alla volta,
   un'identificazione onesta, stop al primo segnale di blocco (429, captcha, pagina di
   consenso o di controllo anti-bot, pagina di accesso). Non si aggira mai: niente client o
   user agent finti, niente proxy, niente token o cookie, nostri o di altri, che saltino una
   pagina di consenso o un controllo. Solo `www.youtube.com`, e lì solo il feed del canale
   (`/feeds/videos.xml?channel_id=…`), la pagina del video (`/watch?v=…`) per la lista dei
   sottotitoli, i sottotitoli automatici (`/api/timedtext`) e `/robots.txt`, per ricontrollare
   le regole; nessun altro host o percorso di YouTube. Se così il testo non si ottiene, si avvisa l'owner e non si forza.
4. **Perimetro e quota** (domanda 3, opzione B). Consigli e commissioni dei Municipi V e X
   (RomaTV) e del Municipio I (YouTube); tutte le commissioni capitoline, trascritte per
   intero, tenendo solo i fatti che cadono nei Municipi I, V e X; l'Assemblea capitolina.
   Quali fatti diventano elementi, e su quale pagina, lo fissano le PR della lettura e della
   geografia (DEC-106, DEC-107). La quota mensile di A sale a circa 27 €; il totale del pilota
   resta i 50 € di DEC-031, punto 6. Come le quote si dividono fra i workstream lo dice
   CONTRATTI, sezione 5. Lettura del builder, che l'owner conferma con il merge: le commissioni
   capitoline tutte, con i soli fatti di I, V e X, vengono dalla premessa della domanda, su cui
   l'owner non ha obiettato; il totale resta 50 €, non «sotto», perché le quote sommavano già
   50 € (Impact).
5. **Fuori seduta: temporaneo, poi cancellato** (domanda 4, opzione A). La trascrizione
   completa di una registrazione, nostra, della piattaforma o di YouTube, sta solo nella
   cartella privata `A Amministrazione/temporanei/` finché il confine della seduta aperta non è
   fissato, poi si cancella. Negli originali resta solo il testo della seduta aperta; del
   fuori seduta solo l'esistenza, il minutaggio e la durata, e niente nei registri
   (SPECIFICA_NOMI_E_TERRITORIO, sezione 2). n8n non salva i dati delle esecuzioni
   riuscite dei flussi che trattano audio o trascrizioni. Lettura del builder, che l'owner
   conferma con il merge: «solo» vuol dire in nessun altro posto, nemmeno nei file di lavoro
   di una sessione, dove non si scaricano i dati di un'esecuzione con audio o testo; la
   trascrizione completa si cancella anche se il confine non si può fissare, e allora la
   registrazione non dà testo; i dati di un'esecuzione fallita si cancellano su n8n appena
   letto l'errore.
6. **Le spese sotto i 5 €.** Vale la seconda frase dell'owner citata sopra. Lettura del
   builder, che l'owner conferma con il merge: il builder decide da solo una scelta che costa
   meno di 5 €, come spesa una tantum o come aumento mensile, dentro le quote di CONTRATTI,
   sezione 5, e di DEC-031, punto 6, e la registra (la spesa in `costi/`, la scelta nella PR o
   nel rapporto all'owner). Non copre le scelte editoriali o normative, che restano all'owner.

Impact:
- `docs/pilota/CONTRATTI.md`: sezione 5, le quote; sezione 6, il rimando alle eccezioni dei
  punti 2 e 3; sezione 7, «A · Amministrazione».
- Quote. Le quote sommavano già 50 €: una A a circa 27 € chiede di togliere 7 € alle altre.
  L'opzione B della domanda 3 diceva il contrario («il totale del pilota resta sotto i 50 €»):
  era sbagliata. Le cifre della domanda erano dollari (0,157 $ l'ora): 8 e 6,5
  sono in euro circa 7,5 e 6; i circa 15 con le commissioni municipali erano circa 13 $ di
  trascrizione più la lettura. Il 14 novembre il coordinatore ha spostato i 7 € su A, come gli
  consente CONTRATTI, sezione 5, dove sta la divisione.
- Drive: `QN Hub / 30 Staging pilota 2026-11 / A Amministrazione/`. n8n: i flussi `staging_A_*`.
- Niente in produzione; gazetteer, prompt, registro dei venue e CI invariati. Non supera
  nessuna decisione: DEC-031, punto 6, resta invariato.

Decided by: owner · Date: 14 novembre 2026 · Affected components: canale A del pilota,
`docs/pilota/CONTRATTI.md` (sezioni 5, 6 e 7), `A Amministrazione/` su Drive, flussi `staging_A_*`.

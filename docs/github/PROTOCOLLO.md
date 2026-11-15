# Protocollo delle operazioni su GitHub

Status: in vigore per DEC-028 (decisa il 4 novembre 2026). `CLAUDE.md` lo richiama. Le
evidenze sono in `docs/github/AUDIT_2026-10-30.md`. Vale per ogni repository dell'account
`QuartieriNews` in cui scrivono gli agenti, non solo per QN (DEC-030). Le regole su più PR
nel giro, sulla revisione interna e sul ramo aggiornato con `main`, che smette di essere
obbligatorio, sono di DEC-038 (15 novembre 2026); la regola delle tre PR è in prova fino al
30 novembre 2026.

Nessuna di queste regole garantisce che GitHub non segnali più l'account. Servono a togliere
le scritture superflue e il ritmo da macchina, e a fermarsi subito quando qualcosa non va.
Il 5 novembre il supporto ha indicato come causa dei blocchi alcune parole chiave nel
contenuto del repository, non il ritmo; le regole restano come buona pratica (audit,
sezione F).

## 1. Che cosa conta come scrittura

- **Contenuto:** commento, risposta in un thread, review, richiesta `@codex review`, PR
  nuova.
- **Stato:** push, risoluzione di un thread, modifica di titolo o descrizione, bozza ↔
  pronta, chiusura, cambio di base.

Le letture non sono scritture, ma si fanno solo quando servono: niente polling, si
aspettano le notifiche, al massimo una lettura di stato per PR a ogni evento.

## 2. Prima di scrivere

1. **Un solo scrittore, con la sua identità.** Una sola sessione di agente alla volta
   scrive sui repository dell'account, e scrive come `QN-Builder`, l'account macchina
   dichiarato (DEC-029), mai con l'account dell'owner. Se un'altra sessione è attiva, su
   questo o su un altro repository dell'account, o c'è un job pianificato in corso, si
   aspetta e lo si dice all'owner (DEC-030).
2. **Tutto verde in locale.** Le suite di `AGENTS.md` e quelle della PR passano in locale
   prima del push. Un push per ciclo di correzioni, con tutte le correzioni dentro.
3. **Fino a tre PR nel giro di revisione, una per workstream** (DEC-038, punto 2). Una PR è
   nel giro da quando si apre a quando è pronta (sezione 4, «Merge su notifica») sulla sua
   ultima testa: una PR con rilievi ancora da correggere tiene il suo posto. Un push su una
   PR già pronta la rimette nel giro, e si fa solo se nel giro c'è posto, per il numero e
   per il workstream.
   Una PR che l'owner ha fermato non è nel giro e non tiene i file comuni. Quando l'owner la
   rimette in lavoro, il coordinatore la riprende solo se nel giro c'è posto e, se cambia
   file comuni, solo quando nessun'altra PR aperta li tiene; altrimenti lo dice all'owner e
   aspetta.
   - Nel giro sta al più una PR per workstream del pilota (A, B, C, D) e una del
     coordinatore (decisioni e contratti), e al più tre in tutto. In un repository
     dell'account senza workstream resta una PR alla volta, che conta fra le tre.
   - Due PR nel giro insieme non cambiano gli stessi file, tranne `package.json`. I file
     comuni stanno in una sola PR aperta alla volta, dall'apertura al merge:
     `docs/pilota/CONTRATTI.md`, `decisions/`, `CLAUDE.md`, `AGENTS.md`, `docs/github/`. In
     `package.json` quasi ogni PR aggiunge il suo test sulla stessa riga: il conflitto lo
     risolve il coordinatore riallineando il ramo (sezione 4), nello stesso push delle
     correzioni quando ce n'è uno in attesa (punto 2).
   - Le PR entrano nel giro scaglionate, con gli intervalli della sezione 3.
   - Nel pilota la sessione che scrive (punto 1) è quella del coordinatore. Le chat dei
     workstream non scrivono su GitHub: consegnano un bundle (`docs/pilota/CONTRATTI.md`,
     sezione 4).
4. **PR piccole.** L'obiettivo è stare entro 20 file e 1.000 righe cambiate, esclusi i
   file generati. I file generati e i dati vanno in un commit separato. Una PR più grande
   si divide prima di aprirla (una modifica per PR). La si apre in bozza e la si toglie
   dalla bozza una sola volta, quando è completa.
5. **Una revisione interna prima di aprire** (DEC-038, punto 3). Chi prepara il lavoro lo fa
   rivedere, prima di consegnarlo, da un revisore interno che non l'ha scritto: un subagent
   che riceve il diff e i contratti, non le conclusioni di chi ha scritto. Le correzioni
   entrano nello stesso commit. Il coordinatore non apre una PR senza quella revisione. La
   revisione interna e le sue risposte stanno accanto al bundle, nella cartella Drive del
   workstream, o nel passaggio di fine sessione (`CLAUDE.md`, «Consumption»): mai in un
   commit e mai su GitHub. Non è un ciclo di Codex e non ne prende il posto (sezione 4):
   l'archivio della revisione di Codex resta la PR (DEC-007).

## 3. Ritmo, per sessione

| Regola | Valore |
|---|---|
| Intervallo minimo fra due scritture qualsiasi | 5 secondi |
| Intervallo minimo fra due scritture di contenuto | 60 secondi |
| Scritture di contenuto in un'ora | al massimo 10 |
| Scritture di stato in un'ora | al massimo 30 |
| Intervallo minimo fra l'apertura, o il passaggio da bozza a pronta, di due PR diverse | 15 minuti |
| Intervallo minimo fra due push su PR diverse | 5 minuti |
| Cambi di stato in blocco (più PR pronte, chiuse o modificate insieme) | mai |
| Chiudere e riaprire, commit vuoti, push di sole correzioni di forma | mai |

Nelle prime 24 ore dopo la fine di una restrizione i tetti orari si dimezzano. Le
fusioni pronte si fanno prima del resto.

I tetti orari sono per sessione: valgono per tutte le PR insieme, non per ciascuna
(DEC-038). Due PR non si tolgono mai dalla bozza insieme: è un cambio di stato in blocco.

I limiti ufficiali sono molto più alti: 80 richieste che generano contenuti al minuto e
500 all'ora. Questo ritmo è una misura interna, non una soglia di GitHub.

## 4. Revisioni

- **La revisione parte da sola.** Dal 9 novembre Codex rivede ogni PR all'apertura e a
  ogni push (impostazione dell'owner, DEC-032). Per le PR di `QN-Builder` succede spesso ma
  non sempre. Nessuno chiede `@codex review`, salvo i due casi qui sotto. Ogni push è una revisione, quindi un push per ciclo di correzioni
  (sezione 2, punto 2) conta ancora di più.
- **Quando Codex non parte, chiede l'owner,** perché `QN-Builder` non è collegato a
  Codex. Se il connettore risponde chiedendo un account Codex, il builder lo dice subito
  all'owner, in una riga con il link, e l'owner scrive `@codex review`. Se Codex tace per
  più di un'ora dopo un push, il builder lo dice all'owner e l'owner sollecita una volta.
  Poi ci si ferma.
- **Merge su notifica.** Quando una PR è pronta (CI verde, nessun rilievo aperto, nessun
  conflitto), il builder manda all'owner una notifica con il link; il merge è dell'owner.
  Non c'è un tetto di PR o di merge al giorno (DEC-032).
- **Prima della notifica** (DEC-038, punto 1). In QN l'owner toglie dal ruleset l'obbligo
  del ramo aggiornato con `main`; finché GitHub lo chiede ancora, il coordinatore riallinea
  come prima e lo dice all'owner. Prima di dire all'owner che una PR è pronta, il
  coordinatore fa girare in locale le suite sulla PR unita al `main` di quel momento. Tolto
  l'obbligo, riallinea il ramo solo se c'è un conflitto o se quella prova fallisce.
- **Dopo ogni merge** il coordinatore controlla che le altre PR aperte non siano in
  conflitto, prima di segnalare la successiva come pronta, e rifà in locale, sul nuovo
  `main`, la prova di ogni PR già segnalata. Se una PR già segnalata è in conflitto o la
  prova fallisce, dice all'owner che quella notifica non vale più, e la segnala di nuovo
  solo quando è di nuovo pronta. Se la CI su `main` si rompe dopo un merge, la correzione è
  la prima PR a passare.
- **Ripiego sul canale API.** Solo dopo un'ora di silenzio del canale nativo, con un
  commento per ciclo (DEC-028, punto 3).
- **Risposte nei thread.** Le risposte stanno nei thread dei rilievi (DEC-007), voce per
  voce. Quando lo strumento lo permette, le risposte di un ciclo partono insieme in una
  sola review invece che una per volta. I thread si risolvono dopo il push che li corregge.
- **Rapporti del canale API.** Un commento per ciclo, con il rapporto integrale in un
  blocco `<details>`.
- **Il tetto dei quattro cicli resta** (AGENTS.md, DEC-012). Contano i cicli di revisione,
  non i commenti.

## 5. Errori e stop

**Segnali di restrizione.** Fermano subito ogni scrittura; poi si avvisa l'owner:
- 404 su un repository dell'account, o pagina non visibile da non autenticati: il
  segnale ferma le scritture su tutti i repository dell'account (DEC-030);
- 403 che non si spiega con un permesso mancante;
- Actions che non parte entro dieci minuti da un evento che un workflow del repository
  ascolta. In QN sono l'apertura, la riapertura e i push di una PR, e i push su `main`
  (`.github/workflows/checks.yml`). Segnare pronta una PR, modificarne la descrizione o
  commentare non avviano Actions: dopo queste scritture un run nuovo non è atteso, e i
  controlli già conclusi sulla testa restano validi;
- un messaggio di GitHub sull'account;
- Codex nativo che tace per più di un'ora **insieme** a uno dei segnali qui sopra.

Da solo, il silenzio di Codex non è un segnale di restrizione: porta al ripiego sul canale
API (sezione 4), non allo stop.

**Ritorno a una PR alla volta.** Al primo segnale di restrizione, oltre allo stop, nel giro
di revisione torna a stare una PR alla volta, finché l'owner non dice altrimenti: si apre,
si toglie dalla bozza o si chiede la revisione di una PR solo quando la precedente ha
finito il suo giro (DEC-028, domanda 2). Le PR già aperte restano aperte, senza chiuderle
né riportarle in bozza: si riprende a lavorare su una alla volta, prima le fusioni pronte
(sezione 3), e non se ne apre un'altra finché quelle nel giro non hanno finito (DEC-038,
punto 2).

**Limiti di frequenza** (403 o 429 con `retry-after`, `x-ratelimit-remaining: 0`, oppure
il messaggio «secondary rate limit»):
1. si rispetta `retry-after`, oppure si aspetta fino a `x-ratelimit-reset`, oppure almeno
   60 secondi;
2. al massimo due nuovi tentativi, con attesa doppia ogni volta;
3. poi ci si ferma e si riporta.

**Nessun nuovo tentativo alla cieca.** Prima di ripetere una scrittura di contenuto si
legge se la prima è arrivata.

**Mai aggirare.** Nessuna identità alternativa, nessun proxy, nessun mirror per scrivere al
posto di GitHub. Durante una restrizione si lavora in locale (`docs/github/CONTINUITA.md`).

## 6. Report di fine sessione

Ogni sessione che ha scritto su GitHub chiude con un riepilogo per l'owner, nel messaggio
finale e non come commento su GitHub:
- scritture per tipo, contenuto e stato;
- intervallo minimo fra due scritture e massimo in dieci minuti;
- revisioni chieste e revisioni concluse;
- nuovi tentativi ed errori (codice e `retry-after`);
- segnali di restrizione visti e ore di lavoro ferme;
- fino al 30 novembre 2026, per la prova di DEC-038: le PR unite nel giorno e i cicli di
  revisione di ciascuna.

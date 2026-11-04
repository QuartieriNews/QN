# Protocollo delle operazioni su GitHub

Status: in vigore per DEC-028 (decisa il 4 novembre 2026). `CLAUDE.md` lo richiama. Le
evidenze sono in `docs/github/AUDIT_2026-10-30.md`.

Nessuna di queste regole garantisce che GitHub non segnali più l'account. Servono a togliere
le scritture superflue e il ritmo da macchina, e a fermarsi subito quando qualcosa non va.

## 1. Che cosa conta come scrittura

- **Contenuto:** commento, risposta in un thread, review, richiesta `@codex review`, PR
  nuova.
- **Stato:** push, risoluzione di un thread, modifica di titolo o descrizione, bozza ↔
  pronta, chiusura, cambio di base.

Le letture non sono scritture, ma si fanno solo quando servono: niente polling, si
aspettano le notifiche, al massimo una lettura di stato per PR a ogni evento.

## 2. Prima di scrivere

1. **Un solo scrittore.** Una sola sessione di agente scrive sul repository. Se un'altra è
   attiva, o c'è un job pianificato in corso, si aspetta e lo si dice all'owner.
2. **Tutto verde in locale.** Le suite di `AGENTS.md` e quelle della PR passano in locale
   prima del push. Un push per ciclo di correzioni, con tutte le correzioni dentro.
3. **Una PR alla volta nel giro di revisione.** Si apre, si toglie dalla bozza o si chiede
   la revisione di una PR solo quando la precedente ha finito il suo giro, cioè revisione
   e CI.
4. **PR piccole.** L'obiettivo è stare entro 20 file e 1.000 righe cambiate, esclusi i
   file generati. I file generati e i dati vanno in un commit separato. Una PR più grande
   si divide prima di aprirla (una modifica per PR). La si apre in bozza e la si toglie
   dalla bozza una sola volta, quando è completa.

## 3. Ritmo, per sessione

| Regola | Valore |
|---|---|
| Intervallo minimo fra due scritture qualsiasi | 5 secondi |
| Intervallo minimo fra due scritture di contenuto | 60 secondi |
| Scritture di contenuto in un'ora | al massimo 10 |
| Scritture di stato in un'ora | al massimo 30 |
| Cambi di stato in blocco (più PR pronte, chiuse o modificate insieme) | mai |
| Chiudere e riaprire, commit vuoti, push di sole correzioni di forma | mai |

Nelle prime 24 ore dopo la fine di una restrizione i tetti orari si dimezzano. Le
fusioni pronte si fanno prima del resto.

I limiti ufficiali sono molto più alti: 80 richieste che generano contenuti al minuto e
500 all'ora. Questo ritmo è una misura interna, non una soglia di GitHub.

## 4. Revisioni

- **Una richiesta per testa.** Si chiede `@codex review` una volta dopo il push che chiude
  un ciclo. Non si chiede:
  - se la scrittura stessa avvia la revisione (PR aperta per la revisione, bozza resa
    pronta);
  - su una testa già richiesta;
  - mentre una revisione è in corso (riepilogo del bot «Running»).
- **Un solo sollecito.** Se il canale nativo tace, si sollecita al massimo una volta dopo
  un'ora. Poi ci si ferma e lo si dice all'owner.
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
- 404 sul proprio repository, o pagina non visibile da non autenticati;
- 403 che non si spiega con un permesso mancante;
- Actions che non parte entro dieci minuti da un evento della PR;
- un messaggio di GitHub sull'account;
- Codex nativo che tace per più di un'ora **insieme** a uno dei segnali qui sopra.

Da solo, il silenzio di Codex non è un segnale di restrizione: porta al ripiego sul canale
API (sezione 4), non allo stop.

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
- segnali di restrizione visti e ore di lavoro ferme.

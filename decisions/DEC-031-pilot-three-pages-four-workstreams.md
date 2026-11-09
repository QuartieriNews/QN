# DEC-031 — Pilota su tre pagine, con quattro workstream e un coordinatore

Status: DECIDED (9 novembre 2026, owner nella sessione del builder)
Blocks: nothing.

Question: come arrivare in fretta a qualcosa di concreto da guardare, un sito anche solo
privato, senza aspettare che la fase fonti sia completa (DEC-023)?

Contesto:
- Esistono gli elenchi di giugno su Drive (`QN Hub / 20 Packages / Fonti 2026-06`), con le
  versioni senza testi in `tools/sources-study/handoff_data/`: 2.669 atti, 534 registrazioni
  RomaTV (449 ore, 96 delle quali già trascritte dalla piattaforma) e 131 video YouTube
  (135 ore). In `main` ci sono i nodi di deduplicazione (#19, #20) e il prototipo del sito (#18).
- La regola per la stampa nella cronaca è già decisa per l'MVP (DEC-108).
- Il supporto GitHub ha indicato come causa dei blocchi alcune parole chiave nel contenuto
  del repository (audit, sezione F).
- La verifica fatta dall'owner con Codex il 9 novembre sulla revisione automatica (impostazioni
  «All PRs») dice due cose. La funzione esiste, ma la documentazione non garantisce che copra
  le PR di un account non collegato a Codex. Le condizioni d'uso di OpenAI vogliono account
  ChatGPT individuali usati dal titolare, quindi un account ChatGPT intestato a un agente non
  è previsto.

Owner's words, 9 novembre 2026: «Creerei 3 workstream separati che viaggiano da soli con una
finestra che le coordina» (amministrazione dagli streaming, notizie, eventi), più uno per lo
storico; «Acilia mi piace ma il centro ha troppo materiale, ci darebbe indicazioni non
replicabili. Propongo di farne almeno 3, uno difficile (acilia è ok), uno medio (centocelle)
e uno facile (prati)»; il coordinatore unico scrittore su GitHub «ok»; il sito privato
«benissimo basta che vediamo materializzarsi il sito anche se privato per il pubblico»; il
budget «ok per 50 ma se è maggiore avvisami e valutiamo se aumentare. Se la task è quasi
finita e quindi sai che spenderai ancora 10,15 euro per concludere il lavoro non fermarti».

## Regola

1. **Tre pagine pilota.** Acilia (Municipio X, difficile), Centocelle (V, media) e Prati
   (I, facile). Il resto del centro non entra nel pilota.
2. **Quattro workstream, ciascuno in una sessione propria:**
   - A, **Amministrazione**: sedute da RomaTV, YouTube e lo streaming del Comune, per il
     blocco «Dal Municipio», solo dalle sedute aperte (DEC-105);
   - B, **Notizie**: Carabinieri, Polizia, Comune e testate aperte, per il blocco
     «Notizie», secondo DEC-108;
   - C, **Eventi**: Facebook via Apify sugli URL raccolti a mano (DEC-102), siti e
     culture.roma.it, per il blocco «Eventi»; dalle pagine possono venire anche notizie;
   - D, **Storico**: atti e documenti scaricati dalle fonti, archiviati su Drive (DEC-023).
3. **Un coordinatore,** una sessione propria. Fissa i contratti comuni: forma di una notizia
   e di un evento, zona dal gazetteer, dove si salva. Dà i compiti e riferisce all'owner.
4. **Solo il coordinatore scrive su GitHub** (DEC-030). I workstream lavorano in locale e su
   Drive e consegnano al coordinatore. Nessun testo di notizia entra nel repository: né
   campioni, né contenuti del sito, né test, che usano esempi inventati.
5. **Prima il sito privato.** Si parte dal prototipo della #18, che legge dallo staging su
   Drive. L'apertura al pubblico la decide l'owner più avanti.
6. **Budget del pilota: 50 € al mese** per trascrizioni, Apify e modelli. Prima di superarlo
   si avvisa l'owner. Un lavoro quasi finito si chiude anche se servono 10–15 € in più.
7. **La revisione di Codex.** Il 9 novembre l'owner ha attivato sul repository QN la
   revisione automatica: tutte le PR, a ogni push, in modalità esaustiva. La verifica sulla
   PR #24 mostra che, all'apertura di una PR di `QN-Builder`, il connettore non avvia la
   revisione e chiede un account Codex: l'impostazione vale per gli account collegati.
   Finché non c'è un'altra soluzione, la revisione la chiede l'owner con `@codex review`,
   una volta per testa (DEC-029, punto 4), e il coordinatore raccoglie il lavoro in poche PR
   per non moltiplicare le richieste. Una revisione via API in GitHub Actions, con una chiave
   tecnica e costi a consumo, è l'alternativa da valutare con una decisione a sé, perché
   tocca `.github/` e i segreti del repository.

Impact:
- Drive: le cartelle di staging del pilota, una per workstream più lo storico.
- Repository: i contratti comuni in un documento; il codice dei workstream arriva in PR del
  coordinatore, una alla volta.
- Nessun cambiamento a gazetteer, prompt o n8n di produzione. La pipeline resta in staging.

Decided by: owner · Date: 9 novembre 2026 · Affected components: sessioni del builder,
staging su Drive, `tools/site/`, DEC-030 (applicata), DEC-108 (applicata), DEC-023.

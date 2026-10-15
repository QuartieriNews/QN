Di seguito il controllo, secco.

## 1) La definizione corrente di `novita_rispetto_agli_atti` **non regge senza chiarimenti forti**

1.1 **“La stessa cosa compare” non è definito operativamente**  
Testo: *“`anche negli atti` — il fatto compare…”* (Emendamento 16 settembre, secondo).  
Problema: non è specificato se “compare” significa **stesso tema** o **stessa affermazione fattuale**.  
Caso critico che hai chiesto: se in aula si dice “cantiere fermo” e un atto dice “cantiere avviato”, tema uguale ma contenuto opposto.  
- Se lo marchi `anche negli atti`, stai contando come sovrapposizione una **contraddizione**.  
- Se lo marchi `solo dal parlato`, stai misurando davvero la novità informativa del parlato.  
**Verdetto:** così com’è è ambiguo e produce numeri instabili tra lettori. **BLOCCANTE**.

1.2 **“Atti di altro mese” messi in `non verificabile` mescolano fuori-perimetro e incertezza**  
Testo: *“`non verificabile` … atti di un altro mese”*.  
Caso che hai chiesto: fatto di giugno che compare in un atto di luglio.  
- Con questa regola finisce in `non verificabile`.  
- Ma metodologicamente non è “non verificabile”: è **fuori perimetro temporale del corpus**.  
Effetto: gonfi `non verificabile` e abbassi/artificialmente `solo dal parlato`.  
**Verdetto:** categoria concettualmente sbagliata per il KPI principale. **BLOCCANTE**.

1.3 **`non verificabile` è un contenitore eterogeneo**  
Testo: *“riferimento troppo generico per essere cercato”* + documenti esterni + altro mese.  
Tre cause diverse (genericità, esterno, tempo) con impatti diversi vengono fuse in un solo valore. Non è analiticamente leggibile.  
**Verdetto:** **DA CORREGGERE PRIMA DELLA CONSEGNA**.

1.4 **“Rispetto agli atti” ma confronto anche con “notizie già estratte”**  
Testo: *“anche negli atti quando… in un atto o in una notizia già estratta”*.  
Questo introduce dipendenza da errori/omissioni a monte (estrazione Report 1), non solo dagli atti.  
**Verdetto:** KPI nominalmente “atti” ma operativamente “atti + pipeline precedente”. **DA DICHIARARE NEL RAPPORTO** (o rinominare KPI).

---

## 2) La misura meccanica non è pienamente indipendente; usare `dubbio` come overlap certo è scorretto

2.1 **Non è indipendente in senso forte**  
Dipende comunque da campi umani (`data`, `luogo`, `oggetto`) estratti dalla stessa pipeline, con trascrizioni rumorose. È indipendente dal campo `novita_rispetto_agli_atti`, non dal processo di codifica.  
**Verdetto:** **DA DICHIARARE NEL RAPPORTO**.

2.2 **`dubbio` non è prova di sovrapposizione**  
Hai scritto: 2 su 3 criteri ⇒ `dubbio`. Quindi per definizione è incertezza sull’oggetto.  
Se lo usi come “gemello” in conteggio secco, converti incertezza in certezza numerica.  
**Verdetto:** **BLOCCANTE** se usato per headline unica.

2.3 **Se devi pubblicare un numero principale, dev’essere un intervallo, non un punto**  
Usa solo confronti parlato-vs-scritto (non “tutto il corpus”).  
Definisci:  
- **D** = almeno un `duplicato` con scritto (non novel certo)  
- **U** = nessun duplicato ma almeno un `dubbio` (incerto)  
- **S** = nessun match (novel certo)  
Allora quota novità = **[S/N , (S+U)/N]**.  
Unico numero puntuale senza intervallo = finto rigore.  
**Verdetto:** **BLOCCANTE** se non intervallato.

---

## 3) Otto lotti con tre definizioni: recuperabile solo parzialmente senza rilettura completa

3.1 **Sì, recuperabile il campo, ma non “gratis”**  
Puoi ricodificare `novita_rispetto_agli_atti` ex-post sui JSON già prodotti + confronto strutturato con `confronto_atti.csv` e `report1/db/notizie_candidate.csv`, senza riascoltare tutto.  
Servirà ascolto mirato solo dei casi ambigui (`non verificabile`, `qualita=bassa`, `toponimo_da_verificare`, conflitti).  
**Verdetto:** **DA CORREGGERE PRIMA DELLA CONSEGNA**.

3.2 **No, non recuperi la completezza di estrazione senza rilettura**  
Se un lettore con vecchia soglia non ha proprio creato la candidata, non la ricrei da tavolino.  
Quindi recuperi coerenza di etichettatura, non recall piena.  
**Verdetto:** **DA DICHIARARE NEL RAPPORTO**.

3.3 **Percentuali aggregate attuali dei lotti sono non pubblicabili come se fossero omogenee**  
Lo dice la stessa specifica: *“i lotti … non sono confrontabili su questo campo”*.  
**Verdetto:** **BLOCCANTE** per qualsiasi confronto diretto tra lotti non ricodificati.

---

## 4) Soglia di notiziabilità: oggi è una scelta forte, ma falsifica se venduta come misura generale

4.1 **La soglia esclude classi che in seduta sono spesso “la notizia”**  
Testo `no`: *“regolamenti cittadini senza luogo”, “organizzazione interna dell’organo”, …*  
Conseguenza: misuri solo novità territoriali localizzate, non novità politico-istituzionali del parlato.  
**Verdetto:** se il claim è generale (“quanto aggiunge il parlato”), è **DA CORREGGERE PRIMA DELLA CONSEGNA**; se il claim è esplicitamente territoriale, **DA DICHIARARE**.

4.2 **Correzione minima non soggettiva (senza riscrivere tutto):**  
serve almeno una classe ammissibile per **esiti procedurali/formali con effetto pubblico** anche senza luogo (es. mancanza numero legale che blocca decisioni, rinvio atto con impatto su tempi/risorse).  
Altrimenti hai un bias strutturale contro proprio ciò che il parlato spesso aggiunge.  
**Verdetto:** **DA CORREGGERE PRIMA DELLA CONSEGNA** se vuoi KPI credibile sul parlato.

---

## 5) Grana evidenza 10s vs ~5min: una colonna non basta per metriche aggregate

5.1 **Falsa equivalenza di verificabilità**  
Testo: *“Va usato lo stesso: meglio un’evidenza grossolana…”* e *“dichiara separatamente…”*.  
Giusto separare, ma se poi confluiscono in un unico numeratore/denominatore senza stratificazione, il confronto è distorto.  
**Verdetto:** **DA CORREGGERE PRIMA DELLA CONSEGNA**.

5.2 **Minimo necessario**  
Non basta “dichiarare la colonna”: i KPI principali (`solo dal parlato`, tasso novità, qualità) vanno riportati **separati per origine_trascrizione / grana_marcatore_s** e con totale combinato solo come secondario.  
**Verdetto:** **DA CORREGGERE PRIMA DELLA CONSEGNA**.

---

## 6) Altri punti dove sembra misura ma non lo è

6.1 **Unità di conteggio instabile (candidate, non fatti)**  
Un lettore può spezzare un fatto in 3 candidate, un altro in 1. Le percentuali su 254 cambiano senza cambiare realtà.  
**Classificazione:** **DA DICHIARARE NEL RAPPORTO**.

6.2 **Comparabilità temporale non congelata**  
Se il materiale di riscontro cresce/si pulisce durante i lotti, `novita` dipende dalla data di lettura, non solo dal contenuto.  
**Classificazione:** **DA CORREGGERE PRIMA DELLA CONSEGNA** (freeze snapshot unico per ricodifica).

6.3 **Toponimi incerti influiscono direttamente sul matching**  
Regola: toponimo incerto si scrive “come si sente” + flag. Ma dedup richiede stesso luogo: errore ASR ⇒ falso `solo dal parlato`.  
**Classificazione:** **DA DICHIARARE NEL RAPPORTO** (e audit su `toponimo_da_verificare=sì`).

---

### Sintesi netta
- **Non pubblicabile così com’è** un numero unico di novità del parlato.  
- I blocchi veri: ambiguità su contraddizioni, gestione “altro mese”, uso improprio dei `dubbio`, aggregazione lotti eterogenei.  
- Pubblicabile solo dopo ricodifica ex-post + KPI a intervallo + stratificazione per qualità della trascrizione/origine.

---
Controllo C3, modello gpt-5.3-codex, effort high, token 3835 in / 8737 out, 2026-09-16T06:29:49.892Z

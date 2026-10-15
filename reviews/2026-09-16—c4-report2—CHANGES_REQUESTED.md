Di seguito i rilievi, nell’ordine richiesto.

## 1) Affermazioni del rapporto non sostenute dai dati (o non sostenute **così come scritte**)

1. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   **Frase:** «Le conclusioni qualitative non dipendono dai lotti che mancano: si ripetono identiche da otto lotti.» (incipit)  
   **Per sostenerla serve:** tabella per lotto con indicatori qualitativi predefiniti e loro stabilità (non aneddoti).  
   **Azione:** correggere (o togliere).

2. **[BLOCCANTE]**  
   **Frase:** «La scoperta che regge tutto il resto ... “la videoregistrazione sostituisce la trascrizione...” ... Tutto il resto discende da qui.» (§1)  
   **Per sostenerla serve:** evidenza normativa/operativa ampia (più Municipi/organi) + nesso dimostrato coi risultati quantitativi. Due verbali non bastano per “regge tutto”.  
   **Azione:** ridurre drasticamente la portata, o togliere la causalità totale.

3. **[BLOCCANTE]**  
   **Frase:** «Contro i 1.983 atti ... detto con precisione.» (§2)  
   **Per sostenerla serve:** che il calcolo usi solo atti.  
   **Problema:** `novita_meccanica.py` confronta il parlato contro **tutte le righe scritte** in `notizie_candidate.csv` (non solo atti). Inoltre §7.2 dice esplicitamente “atti + notizie Report 1”.  
   **Azione:** correggere definizione del confronto.

4. **[BLOCCANTE]**  
   **Frase:** «Da cui la scala: 36,8 / 54,4 / 98,4.» (§2)  
   **Per sostenerla serve:** formula/script riproducibile per tutti e tre i numeri.  
   **Problema:** `novita_meccanica.py` calcola solo due estremi `[S/N, (S+U)/N]`; il 36,8 non viene da quel codice.  
   **Azione:** aggiungere calcolo esplicito del 36,8 o togliere il legame “da cui”.

5. **[BLOCCANTE]**  
   **Frase:** «36,8% ... È il pavimento: regge a qualunque obiezione.» (§2)  
   **Per sostenerla serve:** dimostrare che è lower bound rispetto **a tutte** le incertezze rilevanti (dedup, copertura corpus, OCR/STT, ecc.).  
   **Azione:** togliere “qualunque obiezione”; chiamarlo al massimo “stima conservativa sotto ipotesi X”.

6. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   **Frase:** «La prova sta in una sola frase ... Cambia solo il confine del corpus.» (§2)  
   **Per sostenerla serve:** non un caso singolo, ma test sistematico su un campione di casi analoghi.  
   **Azione:** presentarlo come esempio illustrativo, non “prova”.

7. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   **Frase:** «Quel 25%, quindi, non misura la debolezza del parlato: misura dove passa il confine...» (§2)  
   **Per sostenerla serve:** decomposizione quantitativa delle cause del 25% (confine corpus vs altri fattori).  
   **Azione:** attenuare (ipotesi plausibile, non conclusione chiusa).

8. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   **Frase:** «Negli atti passa solo chi vince.» (§3)  
   **Per sostenerla serve:** audit completo degli esiti votati vs atti pubblicati, non 2 esempi.  
   **Azione:** riformulare come evidenza in alcuni casi.

9. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   **Frase:** «La parte più informativa è quella che per procedura non si registra.» (§3)  
   **Per sostenerla serve:** metrica comparativa “informatività registrata/non registrata” su campione ampio.  
   **Azione:** riformulare come pattern osservato in casi documentati.

10. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
    **Frase:** «...riassumono via esattamente ciò che ha valore» e «nelle sedute-monologo ... non c’è nulla di nuovo.» (§3)  
    **Per sostenerla serve:** analisi sistematica, non inferenza narrativa.  
    **Azione:** attenuare o togliere assoluti (“esattamente”, “nulla”).

11. **[DA DICHIARARE NEL RAPPORTO]**  
    **Frase:** «Quattro item su 274 ... altri cinque ...» (§5)  
    **Per sostenerla serve:** specificare chiaramente denominatore (quale sottoinsieme è 274) e script/query.  
    **Azione:** dichiarare metodo/denominatore nel testo.

12. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
    **Frase:** «... abbastanza per dire da che parte sta il difetto.» (§5, riscontro 7 link)  
    **Per sostenerla serve:** campione più ampio e multi-Municipio, o linguaggio più prudente.  
    **Azione:** limitare a “in questi sette casi”.

13. **[BLOCCANTE]**  
    **Frase:** §7.1 (71 punti / 22 punti; rapporto 1,46 e 0,74).  
    **Per sostenerla serve:** script che riproduca **esattamente** quel confronto “regola mobile vs regola ferma”.  
    **Problema:** `varianza_lettori.py` fornito non segmenta così; segmenta “tutti / V3 / V4”.  
    **Azione:** allineare testo e codice, oppure togliere i numeri.

14. **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
    **Frase:** tabella S/U/D e percentuali associate (§2).  
    **Per sostenerla serve:** coerenza aritmetica interna (S+U+D, N, percentuali).  
    **Azione:** sincronizzare numeri/percentuali con output script.

---

## 2) Meccanismo del §2 (“fatto compiuto... residuo”): spiegazione o storia a posteriori?

1. **Valutazione:** **[DA DICHIARARE NEL RAPPORTO]**  
   È una **ipotesi esplicativa plausibile**, ma nel testo è presentata come conclusione dimostrata. Così è post-hoc.

2. **Che cosa la falsificherebbe (test chiari):**
   - quota alta di candidate “compiuto, datato, localizzato” che restano S anche estendendo il corpus a mesi adiacenti;
   - nessuna differenza (o differenza opposta) tra qualità delle candidate nuove vs confermate;
   - molti casi “residuali” che risultano invece già formalizzati in atti nello stesso perimetro.

3. **È stata falsificata coi dati disponibili?**  
   **No**, ma soprattutto **non è stata testata in modo falsificabile** nel materiale fornito (c’è evidenza aneddotica + una differenza di qualità, non un test causale).

---

## 3) I tre numeri (36,8 / 54,4 / 98,4)

1. **Il programma calcola quello che il testo dice?**  
   - **54,4 e 98,4:** **[VA BENE, con riserva]** — sono coerenti con la logica di `novita_meccanica.py` (`S/N` e `(S+U)/N`).  
   - **36,8:** **[BLOCCANTE]** — non è calcolato da quel programma; richiede filtro ulteriore (toponimo incerto) non mostrato qui.

2. **L’intervallo è onesto o nasconde una scelta?**  
   **[DA DICHIARARE NEL RAPPORTO]**  
   Onesto **solo** rispetto all’incertezza U (dubbio dedup). Nasconde scelte forti: qualità del dedup assunta, copertura corpus assunta, unità=candidata.

3. **Il “pavimento” 36,8 è davvero pavimento?**  
   **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   È un punto conservativo sotto una scelta specifica, non un lower bound assoluto.

---

## 4) §5 difetti: fonte vs pipeline

1. **Censimento che sbaglia abbinamenti:** **[VA BENE]**  
   Attribuzione corretta alla pipeline vostra.

2. **Errori “nelle registrazioni” (grafie toponimi, sigle, importi):** **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   Va separato:
   - difetto della **trascrizione della piattaforma** (fonte secondaria),
   - difetto della **trascrizione fatta da voi** (`gpt-4o-mini-transcribe`, quindi pipeline vostra).  
   Ora sono mescolati.

3. **Link corrotto da OCR:** **[DA DICHIARARE NEL RAPPORTO]**  
   Questo è difetto dello strato testo/OCR (pipeline di estrazione), non necessariamente dell’atto sorgente.

4. **Duplicazioni/spezzoni pubblicati come item distinti:** **[VA BENE]**  
   Attribuzione alla pubblicazione sorgente plausibile.

---

## 5) Riscontro dei 7 link (§5): basta o no?

1. **Per la frase attuale:** **[DA CORREGGERE PRIMA DELLA CONSEGNA]**  
   n=7, un solo Municipio, campione non casuale: non basta per inferenza generale “da che parte sta il difetto” sull’intero sistema.

2. **Che cosa può dire legittimamente:** **[VA BENE se riformulato]**  
   “Nei 7 casi con identificativo di seduta risolto nel corpus, il censimento fallisce 0/7 e il collegamento Municipio+data prende 7/7.”

---

## 6) Cosa manca perché un esterno giudichi l’attendibilità

1. **[BLOCCANTE]** Mappa di riproducibilità numero→script/query→file snapshot per **ogni** numero in rapporto.  
2. **[BLOCCANTE]** Indice evidenze per i casi narrativi (§3–§4): ID atto/video + timestamp/citazione verificabile.  
3. **[DA CORREGGERE PRIMA DELLA CONSEGNA]** Definizione univoca del “confronto scritto” (solo atti vs atti+altre fonti) coerente in tutto il testo.  
4. **[DA CORREGGERE PRIMA DELLA CONSEGNA]** Audit qualità dedup (almeno precision/recall su campione) perché i tre numeri dipendono da quello.  
5. **[DA DICHIARARE NEL RAPPORTO]** Copertura e missingness per `varianza_lettori.py` (quante candidate appaiate/non appaiate e impatto).  
6. **[DA DICHIARARE NEL RAPPORTO]** Analisi di sensibilità del 36,8 (e perché quel taglio è scelto rispetto ad altri possibili tagli conservativi).  

Se vuoi, nel prossimo passaggio ti faccio una checklist “pubblicabile/non pubblicabile” riga per riga del report con semaforo rapido.

---
Controllo C4, modello gpt-5.3-codex, effort high, token 12831 in / 12283 out, 2026-09-16T09:49:16.357Z

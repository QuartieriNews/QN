AGREEMENT WITH NON-BLOCKING RESIDUALS

**Council:** Technical Council (DEC-008, modello AI a tre livelli), sessione "Piano esecutivo della Fase 0" — review 1 di 3 autorizzate dal mandato dell'owner del 14 settembre 2026. Livello A: accordo sui macro-step.

**Reviewer:** Codex (`gpt-5.3-codex`, OpenAI Responses API, reasoning `high`, `store: false` — lo stesso collegamento delle sei iterazioni sulla baseline, `docs/PROJECT_BASELINE.md` §7). Risposta id `resp_0366dea37ca543cd016aa81712e9d887d1a71d31d65d876720`; usage: input 36.284, output 11.780 (di cui reasoning 10.154), totale 48.064 token; 106 s.

**Versione esaminata:** proposta dei macro-step "proposal_A_v0.1.md", versione A-0.1, sha256 `fc8b953d67a4fcb782ef9e6c17e512b3dcabdd3fdf20c5772984ef466346b435` (documento di lavoro dell'Operator; il suo contenuto corretto è la §3 di `docs/PHASE_0_EXECUTION.md` dalla versione B-0.2). Input inviato con la proposta: mandato dell'owner, evidence pack (stato verificato di repository e Drive, senza segreti), testo integrale della baseline v0.6 al commit `7873b11`, DEC-014…021 e modifiche a DEC-006/DEC-103 (commit `9fcb896`), decisioni aperte e storiche su `main` (`1459812`).

**Verificato contro:** baseline v0.6 (commit `7873b11`), registro `decisions/` (`main` + branch dell'11 settembre), mandato dell'owner. Nessuna review di codice; nessun T-case esercitato (documento di pianificazione). Suite su `main` eseguite dall'Operator prima della sessione: 37 / 58 / 273 / 123 / 13, tutte ALL PASS.

## Finding di Codex (testo integrale della review)

### VERDETTO — AGREEMENT WITH NON-BLOCKING RESIDUALS  
(Valido per `proposal_A_v0.1.md`, versione **A-0.1**, sha256 `fc8b953d67a4fcb782ef9e6c17e512b3dcabdd3fdf20c5772984ef466346b435`.)

### FINDING
1. **IMPORTANT — S4 / Gate #5 / §5.1 (specifica v2.5)**
   - **Dove:** Step **S4**, criteri di chiusura al punto 5 del gate, sezione contraddizioni §5.1.
   - **Cosa non va:** il piano assume come esito operativo “sign-off + delta senza riscrivere la spec”, ma la baseline approvata descrive in Fase 0 un “consolidamento della spec v2.5” con PR/merge dedicati. Così lo step resta ambiguo e di fatto restringe la baseline senza una scelta owner già formalizzata.
   - **Fonte normativa:** baseline §2.B (“**consolidare la spec v2.5**”), baseline §4 riga Fase 0 (“**spec consolidata**”), Appendice A.2 settimana 2/4 (“PR di consolidamento...”, “spec v2.5 approvata e mergiata”); mandato §2 (“isolare contraddizioni materiali, non modificarle silenziosamente”).
   - **Correzione suggerita:** rendere S4 esplicitamente **biforcato**: default = consolidamento come baseline; alternativa “sign-off + delta” solo dopo indicazione esplicita owner tracciata.

2. **IMPORTANT — S0 / Gate #1 (sicurezza)**
   - **Dove:** Step **S0** e gate di chiusura punto 1.
   - **Cosa non va:** il criterio “secret scanning di repository + cronologia pulito” è reso requisito di chiusura Fase 0, ma non è richiesto come gate dalla baseline R0; introduce possibile scope creep (bonifiche extra) non pianificato.
   - **Fonte normativa:** baseline §1, R0 (rotazione immediata, custodia corretta, rimozione/svuotamento documento esposto); mandato (no espansioni opzionali fuori perimetro operativo del piano).
   - **Correzione suggerita:** mantenere lo scanning come **verifica raccomandata** e rilevazione rischi; il gate minimo resta rotazione/custodia + operatività con nuove credenziali.

3. **MINOR — §3 Dipendenze (S7a)**
   - **Dove:** sezione **§3**, dipendenza “S7(a) baseline su main → ogni documento su main che cita DEC-014…021”.
   - **Cosa non va:** formulata come dipendenza “reale” generalizzata, ma è soprattutto vincolo di ordine di merge/pubblicazione, non di produzione degli artefatti in branch.
   - **Fonte normativa:** mandato §5 Livello A (distinguere dipendenze effettive da preferenze di sequenza); baseline Appendice A.2 mostra attività in parallelo già dalla settimana 1.
   - **Correzione suggerita:** riclassificarla come vincolo di **merge finale** su `main`, lasciando il drafting parallelo in branch.

---

### RISPOSTE ALLE DOMANDE DELL'OPERATOR
1. **Attività mancanti/fuori perimetro:** copertura complessiva buona rispetto a riga Fase 0 e Appendice A. Residui: chiarire S4 (finding 1). **S8** è coerente con la sovrapposizione prevista dalla baseline e correttamente escluso dal gate. La nota M1 è accettabile se resta metodo, non nuovo mini-progetto.

2. **Dipendenze reali vs preferenze:** reali: S0→primo run S1; 4° run S1→tabella M1; S2→D3; disponibilità Reconciliation→pacchetto S5; D12→incarico legale; fotografia n8n→D14. Preferenza principale: S7(a) come hard dependency generale (finding 3).

3. **Duplicazioni/rinvii:** non vedo duplicazioni materiali bloccanti; S2 alimenta D3 (non duplica), S8 alimenta D9 (non duplica). Solo attenzione a non sdoppiare allineamenti documentali tra S4 e S7 nella stessa settimana (coordinamento editoriale).

4. **Passaggi owner (completezza/tempo):** in gran parte completi e ben collocati (D1, D2, D3, D8, D9, D12, D14; autorizzazioni spesa D3/S5). Va solo esplicitata la scelta owner sulla lettura di S4 (finding 1).

5. **Coerenza criteri di uscita con baseline §4 e §6:** quasi allineati. Da correggere: gate S4 ambiguo (finding 1) e gate S0 troppo esteso (finding 2). Il resto è coerente con “conteggi M1 + decisioni fase 0 + spec”.

6. **Letture delle contraddizioni §5:** non sono uniche.  
   - Spec v2.5: lettura A = consolidamento pieno come baseline; lettura B = sign-off + delta (se owner conferma “già consolidata”).  
   - n8n: lettura A = prevale self-hosted baseline; lettura B = coesistenza/trasferimento già avviato verso Cloud.  
   - Reconciliation mancante: nessuna lettura alternativa risolutiva senza intervento owner (localizzazione fonte).

---

### CONVERGENZE
- Struttura a macro-step **coerente** con Livello A (obiettivo/input/output/dipendenze/responsabili/criteri).
- Perimetro Fase 0 rispettato: sicurezza, M1, inventario fonti, registro fonti, residui Eventi, legale, decision-pack D2/D3/D8/D9/D12/D14, governance.
- Distinzione corretta tra **M1** (Fase 0) e **M2/M3** (metodo preparato ora, misura in Fase 1).
- Corretta esclusione dalla Fase 0 di build sito/pipeline/refactor pieno, D4/D5/D7/DEC-001/DEC-004.
- Ruoli allineati al mandato (owner decide/autoriza; operator prepara; Codex verifica PR).
- Buona gestione delle contraddizioni come elementi da isolare, non da “sanare” tacitamente.

### RESIDUI PER L'OWNER
- Confermare la corrispondenza ufficiale tra `QN_Impianto_di_Progetto_v0.6.md` (mandato) e `docs/PROJECT_BASELINE.md` commit `7873b11` (baseline usata nel piano).
- Fornire/localizzare il documento “Round 2 Reconciliation” (in particolare §5 requisiti lancio e §8 13 questioni legali).
- Sciogliere la lettura operativa di S4 (consolidamento pieno vs sign-off+delta).
- Confermare lo stato reale infrastrutturale n8n (self-hosted, Cloud, o coesistenza) come base del pacchetto D14.
## Risposta dell'Operator, correzione applicata, esito della controverifica

| # | Severità | Risposta | Correzione (in `docs/PHASE_0_EXECUTION.md` B-0.2) | Controverifica |
|---|---|---|---|---|
| 1 | IMPORTANT | Accettato | S4 biforcato: lettura A default = consolidamento come da baseline (PR, review, approvazione, merge; versione successiva con il delta delle DEC-014…021; sede del sorgente da confermare); lettura B = sign-off + delta, solo su indicazione esplicita e tracciata dell'owner. Gate 5 cita la lettura scelta; la scelta è in §6 al momento dell'approvazione | review 2: verificata, conforme |
| 2 | IMPORTANT | Accettato | Gate di S0 ridotto al minimo di R0: rotazione, custodia, documento rimosso, operatività con le nuove credenziali. Secret scanning = verifica raccomandata (P0-S0-05), fuori dal gate | review 2: verificata, conforme |
| 3 | MINOR | Accettato | S7(a) riclassificata come vincolo di ordine di merge su `main`; stesura in branch parallela dalla settimana 1 (§5) | review 2: verificata, conforme |

Residui per l'owner riportati in `docs/PHASE_0_EXECUTION.md` §6 e §9: corrispondenza fra `QN_Impianto_di_Progetto_v0.6.md` e il commit `7873b11`; localizzazione della Round 2 Reconciliation; lettura di S4; stato reale di n8n per D14.

## Fuori dallo scopo di questa review

Le sottotask (Livello B), esaminate nella review 2. Nessun file del repository è stato modificato da Codex; l'unico artefatto di questo ciclo è questo report e la versione B-0.2 del piano.

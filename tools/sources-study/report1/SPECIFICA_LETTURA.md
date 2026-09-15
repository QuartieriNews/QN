# Report 1 — specifica di lettura degli item testuali

Per i subagenti che leggono le fonti testuali di giugno 2026 (A1, C1, C2, C4, C5, E2, E3).
Deriva dallo schema `docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, corretto dopo il
controllo Codex C1, e dallo stile del lotto già collaudato
(`tools/sources-study/lotto_opus5/SPECIFICA.md`): quella specifica vale per registrazioni e
atti, questa per le pagine HTML.

## Vincoli assoluti

- **Nessuna richiesta di rete.** Tutto il materiale è locale, in `report1/texts/`. Nessuna API,
  nessuna chiave, nessuna installazione.
- **Nessun nome di persona in nessun campo** (DEC-102): al loro posto il ruolo ("la presidente
  del Municipio", "un consigliere di opposizione", "il comandante provinciale"). Vale anche per
  il titolo copiato dalla pagina, che va riscritto anonimizzato.
  **Eccezione, decisa e uniforme** (`session_b/DECISIONI_OWNER.md`, D1): un nome dentro un
  **toponimo** o dentro il **nome ufficiale di una sede** si riporta alla lettera — vie, piazze,
  ville, teatri, sale, aule, scuole, biblioteche, centri (`Largo Marcello Mastroianni`,
  `Teatro all'aperto Ettore Scola`, `Aula Giulio Cesare`). Sono luoghi, e la localizzazione è lo
  scopo dello studio: renderli generici la distrugge. Lo stesso vale per il **titolo ufficiale di
  un'opera** (un film, una mostra, un premio). La regola sui nomi riguarda le persone in quanto
  persone: chi decide, chi parla, chi viene arrestato, chi presenta. Non lasciarla all'intuito del
  lotto: due lotti che la interpretano diversamente producono un database disomogeneo.
- **Ogni notizia candidata cita l'evidenza**: l'URL dell'item (colonna `url` del manifesto) e,
  quando il testo lo consente, la frase o il dato che la sostiene. Una notizia senza evidenza
  non si scrive: si annota in `log/<lotto>_problemi.md`.
- Scrivere solo dentro `out/` e `log/`. Non modificare i testi di partenza. Non rileggere item
  già schedati.
- **Le contraddizioni si dichiarano, non si risolvono**: `non verificato` nel campo, e una riga
  nei problemi. Un valore dedotto non è mai scritto come letto.
- Lingua italiana.

## Materiale

- `report1/manifest_report1.csv`: una riga per item, con `id`, `fonte`, `url`,
  `data_pubblicazione`, `titolo`, `municipi_meta`, `tematica`, `caratteri`.
- `report1/texts/<id>.txt`: il testo pulito dell'item, al massimo 15.000 caratteri.
- Il proprio lotto è l'elenco di `id` passato nella richiesta: 40–60 item.

## Output

Un file `out/<lotto>_notizie.csv` con una riga per **notizia candidata** (zero, una o più per
item) e queste colonne, nell'ordine:

`documento_id,fonte,titolo_anonimizzato,sintesi,tipo,luoghi,municipio_testo,evidenza_url,evidenza_locale,data_fatto,data_pubblicazione,disponibilita,qualita,toponimo_da_verificare,note`

- `titolo_anonimizzato`: ≤ 12 parole, scritto da te, senza nomi di persona.
- `sintesi`: ≤ 60 parole, densa, senza nomi di persona.
- `tipo`: delibera, mozione, risoluzione, ordine del giorno, interrogazione, sopralluogo,
  audizione, arresto, sequestro, incendio, incidente, controllo, evento, avviso, altro.
- `luoghi`: toponimi **come compaiono nel testo**, separati da `;`. Vuoto se il testo non ne dà.
  Non dedurre un toponimo da quello che sai di Roma: la localizzazione la fa dopo il gazetteer.
- `municipio_testo`: il Municipio **se il testo lo dice** (numero romano I–XV). Vuoto altrimenti:
  il manifesto ha già quello dichiarato dalla fonte e il confronto fra i due è un dato, non un
  dettaglio da appianare. Un fatto che riguarda davvero più Municipi ne porta più d'uno, separati
  da `;` (`V;XI`): sceglierne uno solo inventerebbe una precisione che il testo non ha.
- `evidenza_locale`: la frase breve del testo che sostiene la notizia, o vuoto.
- `data_fatto`: ISO, **solo se il testo la dà**; vuoto se il fatto non è datato.
- `disponibilita`: ISO, solo se il testo dice che il documento è diventato leggibile in una data
  diversa dalla pubblicazione (albo pretorio, atti allegati); di norma vuoto.
- `qualita`: `alta` quando il testo dà fatto, luogo e data con un'evidenza puntuale; `media`
  quando uno dei tre è dedotto; `bassa` quando due lo sono. Un fatto solo annunciato
  (convocazione, ordine del giorno, evento futuro) non supera `media`.
- `toponimo_da_verificare`: `sì` quando il toponimo è storpiato, ambiguo o assente dal gazetteer.
- `note`: contraddizioni, dubbi, testo troncato, pagina vuota. Vuoto se non c'è nulla da dire.

Un item che non contiene alcuna notizia (pagina di servizio, elenco, errore, testo vuoto) **non
produce righe**: va in `out/<lotto>_senza_notizie.csv` con `documento_id,fonte,ragione`.

## Cosa conta come notizia candidata

Un fatto **verificabile, localizzabile e databile** che un lettore del quartiere troverebbe
utile: una decisione presa, un lavoro che parte o finisce, un servizio che cambia orario o sede,
un intervento delle forze dell'ordine, un evento con data e luogo, una chiusura, un bando.

**Non** sono notizie candidate: il commento politico senza un fatto, la rassegna di ciò che si
farà "prossimamente" senza data, la ripetizione di un fatto già raccontato nello stesso testo,
la presentazione istituzionale di un ufficio, il saluto celebrativo.

Un testo può contenere più notizie: separale se hanno luogo o data diversi, tienile insieme se
sono lo stesso fatto raccontato in più paragrafi.

## Misure obbligatorie

- `log/<lotto>_modello.txt`: la riga del tuo system prompt che dichiara il modello, copiata alla
  lettera, come prima azione. Se non è Claude Opus 5, fermati e riferiscilo.
- `log/<lotto>_tempi.csv`: `documento_id,inizio_epoch,fine_epoch,secondi`.
- `log/<lotto>_problemi.md`: errori, dubbi, item saltati e perché, correzioni in corso d'opera.
- Messaggio finale: item completati, notizie prodotte, tempo totale, problemi. Nient'altro.

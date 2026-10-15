# Report 1 — specifica di lettura degli item testuali

> **Nomi delle persone: regola superata.** Le righe «nessun nome di persona» di questa specifica valgono per le letture fatte prima del 17 settembre 2026. Da quella data vale DEC-105 e `tools/sources-study/report2/SPECIFICA_NOMI_E_TERRITORIO.md`: i nomi pertinenti al fatto si scrivono. Il resto della specifica è in vigore.

Per i subagenti che leggono le fonti testuali di giugno 2026 (A1, C1, C2, C4, C5, E2, E3).
Deriva dallo schema `docs/sources/RICOSTRUZIONE_2026-06_SCHEMA_DB.md`, corretto dopo il
controllo Codex C1, e dallo stile del lotto già collaudato
(`tools/sources-study/lotto_opus5/SPECIFICA.md`): quella specifica vale per registrazioni e
atti, questa per le pagine HTML.

## Regola sulle modifiche a questo documento

Questa specifica **non si modifica mentre un lotto è in lettura**: due lotti letti con regole
diverse producono un database non confrontabile, ed è un difetto che si scopre tardi e si paga
rileggendo. Una correzione urgente va messa nel prompt dei lotti in corso e scritta qui solo
dopo che sono rientrati. Ogni modifica è datata nel registro in fondo.

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
  un'opera** (un film, una mostra, un premio), per gli **autori** delle opere messe in scena o
  proiettate (attribuzione bibliografica, non dati di una persona coinvolta nel fatto), per i nomi
  di **gruppi, collettivi e organizzazioni** (che DEC-102 impone anzi di accreditare) e per
  l'**URL** dell'evidenza, che resta intero anche se lo slug contiene un nome: è l'indirizzo
  pubblico che rende verificabile la notizia, e mutilarlo svuoterebbe il metodo.
  La regola sui nomi riguarda le persone in quanto persone **coinvolte nel fatto**: chi decide,
  chi parla, chi viene arrestato, chi dirige, recita, cura, modera, presenta. Non lasciarla
  all'intuito del lotto: due lotti che la interpretano diversamente producono un database
  disomogeneo. Nel dubbio riporta alla lettera e dichiaralo in `note`: una dichiarazione si
  corregge con una passata sui CSV, un'informazione cancellata si recupera solo rileggendo.
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

`documento_id,fonte,titolo,sintesi,tipo,luoghi,municipio_testo,evidenza_url,evidenza_locale,data_fatto,data_pubblicazione,disponibilita,qualita,toponimo_da_verificare,note`

- `titolo`: ≤ 12 parole, scritto da te, senza nomi di persona.
- `sintesi`: ≤ 60 parole, densa, senza nomi di persona.
- `tipo`: delibera, mozione, risoluzione, ordine del giorno, interrogazione, sopralluogo,
  audizione, convegno, arresto, sequestro, incendio, incidente, controllo, evento, avviso, altro.
  `convegno` copre convegni, conferenze, incontri pubblici e presentazioni: prima non c'era e un
  lotto ha dovuto forzarli su `audizione`, che è un atto d'aula e significa un'altra cosa. Se
  nemmeno questo elenco basta, usa `altro` e dillo in `note`: una forzatura silenziosa su una
  voce vicina è peggio di un `altro` dichiarato.
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

## Registro delle modifiche

| Quando | Che cosa | Nato da |
|---|---|---|
| 15/09 21:50 | `municipio_testo` ammette più Municipi separati da `;` | un item A1 che ne riguardava due |
| 15/09 21:50 | DEC-102: eccezione esplicita per toponimi, sedi e titoli di opere (D1) | due lotti che avevano interpretato la regola diversamente |
| 15/09 22:10 | `tipo`: aggiunto `convegno`; istruzione di preferire `altro` dichiarato a una forzatura | un lotto E2 che aveva forzato due convegni su `audizione` |
| 15/09 22:30 | DEC-102: confini estesi a autori delle opere, organizzazioni e URL (D2); regola del dubbio | quattro casi di confine isolati dal lettore di L17–L18 |
| 15/09 22:30 | Un blocco di rassegna ripetuto in coda a molte pagine va in `note`, non genera una riga per pagina | lo stesso lettore, che l'ha trovato in coda a 93 pagine |

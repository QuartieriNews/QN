# Registro delle fonti degli eventi

Strumenti del 13 ottobre 2026 per costruire l'elenco delle fonti dirette degli Eventi: i luoghi e
gli organizzatori da leggere alla fonte, invece di riprendere gli aggregatori. Metodo, conteggi e
decisioni: `docs/sources/FONTI_EVENTI_2026-10.md`.

Libreria standard di Python 3.10+. Tutto si scrive in una cartella di lavoro `DIR` fuori dal
repository: titoli, nomi dei luoghi e indirizzi delle pagine sono dati delle fonti e vanno su
Drive, `QN Hub / 20 Packages / Fonti 2026-06` (DEC-102, DEC-104).

| Passo | Comando | Che cosa fa | Limiti voluti |
|---|---|---|---|
| 1 Comune | `comune_eventi.py DIR AAAA-MM-GG` | schede dell'agenda di Roma Capitale pubblicate dalla data in poi, con Municipio, luogo e inizio del testo | una richiesta ogni 1,5 s; il calendario «in evidenza» della pagina non si usa |
| 2 Meetup | `meetup_roma.py SITEMAP.xml DIR` | eventi di Roma dalle pagine `/find/it--roma/…` della sitemap | la ricerca con parametri è vietata dal robots.txt e non si usa; solo eventi con fuso di Roma; nessun nome di partecipante |
| 3 RomaToday | `romatoday_metadati.py FOGLIO.csv DIR` | titolo, data e link raccolti a mano dall'owner, date ricavate dal link | le pagine di RomaToday non si aprono mai: esclude gli agenti AI e riserva l'estrazione (DEC-108) |
| 4 Classificazione | un agente per lotto, con un secondo agente che controlla | per ogni riga: finestra di date, Roma o no, zona QN, filtro editoriale (`prompts/EDITORIAL_FILTER.md`), rilevanza, corrispondenza con Comune e Meetup | solo titolo e link |
| 5 Fonti | un agente per lotto di luoghi; due per le 220 pagine Facebook curate dall'owner | nome, tipo, zona, sito, pagina dell'agenda, social, decisione (tenere, scartare, sospeso DEC-001, da verificare) | al più dieci ricerche web per agente; Facebook, Instagram e RomaToday mai aperti |
| 6 Registro | `registro.py RISOLTI.json MATRICE.csv DIR` | unione per pagina Facebook, dominio e nome; canale di lettura; pagine sotto la soglia degli eventi | — |
| 7 Verifica | `verifica_canali.py DIR/registro.json VERIFICHE.json`, poi di nuovo `registro.py RISOLTI.json VERIFICHE.json MATRICE.csv DIR` | robots.txt di ogni sito (ammesso, esclude gli agenti AI, vietato) e formato dell'agenda (feed, ICS, API WordPress, dati Event, HTML) | una richiesta alla volta per host; l'agenda si apre solo se il robots.txt la ammette; i social mai |

`robots.py` legge il robots.txt secondo RFC 9309, con i caratteri jolly che `urllib.robotparser`
ignora; un sito che esclude gli agenti AI per nome conta come chiuso anche se ammette gli altri
robot (`CRONACA_PROCESSO_2026-10.md` §5.1).

Controlli: `python3 tools/fonti-eventi/test_fonti_eventi.py` (nessuna rete, dati sintetici).

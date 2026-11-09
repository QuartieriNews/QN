# tools/site — prototipo da buttare della pagina di quartiere

Scopo: **guardare** la pagina di quartiere con dati veri, prima di scegliere la
piattaforma. Non è il sito, non decide la piattaforma, non va pubblicato.

Cosa fa vedere (PROJECT_VISION.md §2, spec v2.5 Phase 2 "Events block"):

- i quattro blocchi — Eventi, Dal Municipio, Notizie, Se ne parla — e il fatto
  che un blocco può essere vuoto senza che la pagina sia vuota;
- il blocco eventi "intorno a te": prima la zona, poi il resto del municipio,
  poi la città, finché non ci sono almeno 5 voci nei prossimi 14 giorni; ogni
  voce porta l'etichetta della propria zona;
- i luoghi con più di 3 date nella finestra si raggruppano in una riga
  ("vedi tutti");
- "in evidenza" = riportato da più canali (`reported_by` con più voci).

File:

- i dati **non** sono nel repository. `events_2026-10.json` — 649 eventi reali
  di ottobre 2026 nella forma dei campi della spec (publication_zone_id,
  municipality_code, geo_level, content_type, editorial_class) — sta su Drive,
  `QN Hub / 20 Packages / Prototipo sito 2026-10`, e nell'anteprima privata.
  Porta i titoli delle pagine eventi di Roma Today e delle sorgenti del
  registro: testo di terzi, che DEC-109 tiene fuori dal repository (decisione
  dell'owner del 23 ottobre 2026, DEC-022). Fonti: Roma Today (ottobre,
  classificati a mano, zona dedotta dal testo) e "eventi letti alla fonte"
  (registro fonti, zona dal metadato della fonte). Gli eventi Facebook non sono
  inclusi nemmeno lì (il campione FB è solo nel foglio di lavoro dell'owner).
- `build_site.py` — generatore statico: `index.html` + una pagina per zona.
- `project_events.py` — dai file canonici degli eventi (specifica v2.5, uno per
  evento, nella cartella `C Eventi` dello staging) ricava il JSON che legge
  `build_site.py`, con le date in ora di Roma (`docs/pilota/CONTRATTI.md`,
  sezioni 2 e 7). Anche i file canonici restano su Drive.
- `README.md` — questo file.

Uso, dallo staging del pilota:

    python tools/site/project_events.py --canonical <copia locale di C Eventi/> \
        --out /tmp/events.json
    python tools/site/build_site.py --events /tmp/events.json \
        --pages acilia,centocelle,prati --out /tmp/site

Uso, con il file di ottobre:

    python tools/site/build_site.py --events <copia locale di events_2026-10.json> \
        [--wiki docs/wiki/schedario.json] --out /tmp/site

I test (`tests/test_site_prototype.py`, `tests/test_project_events.py`) non usano
dati veri: girano su esempi inventati.

Il blocco "Dal Municipio" è dimostrativo: usa le questioni aperte di giugno del
wiki di contesto (PR #17) se gli si passa `--wiki`; altrimenti resta "in
preparazione". Notizie e Se ne parla sono segnaposto.

Cosa **non** è deciso da questo prototipo: la piattaforma, la grafica, il
numero fisso di voci (qui 5 è una soglia di comodo), il peso relativo dei
canali. Tutte domande aperte da portare in `decisions/` quando si sceglierà la
piattaforma.

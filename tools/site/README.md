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

- `events_2026-10.json` — 649 eventi reali di ottobre 2026 nella forma dei campi
  della spec (publication_zone_id, municipality_code, geo_level, content_type,
  editorial_class). Fonti: Roma Today (ottobre, classificati a mano, zona
  dedotta dal testo) e "eventi letti alla fonte" (registro fonti, zona dal
  metadato della fonte). Gli eventi Facebook **non** sono inclusi (DEC-109:
  niente testi di terzi nel repo; il campione FB è solo nel foglio di lavoro
  dell'owner).
- `build_site.py` — generatore statico: `index.html` + una pagina per zona.
- `README.md` — questo file.

Uso:

    python tools/site/build_site.py --events tools/site/events_2026-10.json \
        [--wiki docs/wiki/schedario.json] --out /tmp/site

Il blocco "Dal Municipio" è dimostrativo: usa le questioni aperte di giugno del
wiki di contesto (PR #17) se gli si passa `--wiki`; altrimenti resta "in
preparazione". Notizie e Se ne parla sono segnaposto.

Cosa **non** è deciso da questo prototipo: la piattaforma, la grafica, il
numero fisso di voci (qui 5 è una soglia di comodo), il peso relativo dei
canali. Tutte domande aperte da portare in `decisions/` quando si sceglierà la
piattaforma.

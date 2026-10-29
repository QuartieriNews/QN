# DEC-023 — Estensione della wiki di contesto alle fonti degli eventi

Status: OPEN (OWNER_DECISION_REQUIRED)
Blocks: nulla di operativo; registra se `docs/wiki/fonti-eventi/` è un ramo della wiki di
contesto (DEC-022) con le stesse regole, o un prodotto separato.

Context: DEC-022 ha fissato la wiki di contesto (schedario, diario, pagine generate; dati
strutturati prima e pagine dopo; nessun testo delle fonti nel repository). Dal 23 ottobre
2026 esiste `docs/wiki/fonti-eventi/`: schedario `fonti_eventi.json`, schede degli
aggregatori, pagine per Municipio e per pagina QN, censimento delle pagine Facebook,
fusioni proposte; costruito da `tools/wiki/build_fonti_eventi.py` con ingressi su Drive
(foglio degli eventi, registro fonti, censimento) e test `tests/test_fonti_eventi_build.py`.
È stato costruito applicando le regole di DEC-022 per analogia, senza un'entrata che lo dica.

Question: la wiki delle fonti eventi è parte della wiki di contesto?
  Options:
  a) sì: stesse regole (DEC-022, DEC-109, DEC-105), stesso ciclo di rigenerazione mensile,
     stessa cartella `docs/wiki/`; il registro fonti (Drive) è l'ingresso che decide, la
     wiki è la sua stampa;
  b) no: è lo strumento di lavoro del blocco eventi; resta in `docs/wiki/fonti-eventi/` ma
     con regole proprie da scrivere (per esempio sulle candidate non decise);
  c) sì, e il registro fonti si sposta nel repository come file strutturato (senza testi
     delle fonti), così la wiki non dipende da Drive.
  Claude recommendation: a). Nulla di quanto costruito contraddice DEC-022; c) è attraente
  ma il registro contiene decisioni dell'owner e note, e spostarlo è una decisione a sé.

Impact: a) non cambia file; b) richiede un README di regole; c) richiede di versionare il
registro e di cambiare l'ingresso del build.

Decided by: — · Date: — · Affected components: `docs/wiki/fonti-eventi/`,
`tools/wiki/build_fonti_eventi.py`, DEC-022.

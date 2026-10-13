"""Pagina di lettura per l'owner: grafici e tabelle dalle fonti verificate.

Uso: rapporto_html.py RUN_DIR USCITA.html [--autonomo]

Legge RUN_DIR/fonti_pagine.json (e, se c'è, la tabella della cronaca di giugno
tools/cronaca-prova/runs/2026-10-11/per_pagina.csv per il confronto) e scrive una pagina
HTML: numeri in testa, grafici in SVG disegnati dal browser, tabelle ordinabili e
filtrabili. Senza `--autonomo` la pagina è un frammento da pubblicare come Artifact (che
aggiunge il proprio scheletro); con `--autonomo` ha doctype, lingua, charset e viewport e
si apre da file. Nessuna dipendenza, nessun titolo di articolo, nessun nome di persona:
solo quello che sta già nel JSON.

Una fonte è contata una volta per sito (host) e una volta per indirizzo quando è una
pagina social; i siti ospitati su una piattaforma comune (Google Sites, Issuu) contano
per percorso. Tipo, territorio, accesso e feed di una fonte vengono dalle sole voci in
cui è usabile.
"""
import collections
import csv
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tabella  # noqa: E402

VERDETTI = [("usabile", "Usabile"), ("solo_metadati", "Solo metadati"), ("da_verificare", "Da verificare"),
            ("canale_chiuso", "Solo social"), ("inattiva", "Inattiva"), ("fuori_territorio", "Fuori territorio"),
            ("non_raggiungibile", "Non raggiungibile")]
TIPI = {"testata_locale": "Testata locale", "blog_locale": "Blog locale", "periodico_cartaceo": "Periodico cartaceo",
        "comitato_di_quartiere": "Comitato di quartiere", "parrocchia": "Parrocchia", "associazione": "Associazione",
        "pro_loco": "Pro loco", "consulta": "Consulta", "notiziario_municipio": "Notiziario del Municipio",
        "newsletter": "Newsletter", "biblioteca_centro_culturale": "Biblioteca / centro culturale",
        "scuola_universita": "Scuola / università", "gruppo_social": "Gruppo social", "altro": "Altro"}
TERR = {"quartiere": "Quartiere", "pagina": "Pagina", "municipio": "Municipio", "zona": "Zona", "citta": "Città"}
ORD_MUN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
PIATTAFORME = ("sites.google.com", "issuu.com", "linktr.ee")


def chiave(f):
    """Un sito è uno per host; un social è uno per indirizzo; su una piattaforma comune conta il percorso."""
    kf = tabella.chiave_fonte(f)
    parti = kf.split("/")
    if f["canale"] != "sito" or len(parti) < 3:
        return kf
    host = parti[2]
    if host in PIATTAFORME:
        return "/".join(parti[:5])
    return host


def giugno(repo):
    p = os.path.join(repo, "tools", "cronaca-prova", "runs", "2026-10-11", "per_pagina.csv")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8-sig") as f:
        return {r["slug"]: int(r["pubblicabili"]) for r in csv.DictReader(f, delimiter=";")}


def piu_frequente(valori):
    c = collections.Counter(v for v in valori if v)
    return c.most_common(1)[0][0] if c else ""


def dati(run_dir, repo):
    voci = tabella.carica(run_dir)
    g = giugno(repo)
    nomi = {v["slug"]: v.get("pagina") or v["slug"] for v in voci}
    pagine, municipi = [], []
    for v in voci:
        fonti = v.get("fonti", [])
        c = collections.Counter(f["verdetto"] for f in fonti)
        usabili, viste = [], set()
        for f in fonti:
            if f["verdetto"] == "usabile" and chiave(f) not in viste:
                viste.add(chiave(f))
                usabili.append(f)
        riga = {"slug": v["slug"], "nome": nomi[v["slug"]], "mun": v.get("municipio") or "",
                "giugno": g.get(v["slug"]), "candidate": len(fonti), "fallito": bool(v.get("fallito")),
                **{k: c.get(k, 0) for k, _ in VERDETTI}, "usabile": len(usabili),
                "nomi_usabili": [{"n": f["nome"], "t": TERR.get(f["territorio"], f["territorio"]), "u": f["url"]} for f in usabili]}
        (municipi if v.get("tipo") == "municipio" else pagine).append(riga)
    ordine_mun = lambda m: ORD_MUN.index(m.split("/")[0]) if m.split("/")[0] in ORD_MUN else 99  # noqa: E731
    pagine.sort(key=lambda r: (ordine_mun(r["mun"]), r["nome"]))
    municipi.sort(key=lambda r: ordine_mun(r["mun"]))
    studiate = [r for r in pagine if not r["fallito"]]

    # fonti distinte: attributi dalle sole voci usabili
    host = {}
    for v in voci:
        e_pagina = v.get("tipo", "pagina") == "pagina"
        for f in v.get("fonti", []):
            h = host.setdefault(chiave(f), {"canale": f["canale"], "verdetti": set(), "pagine": set(), "municipi": set(), "usabili": []})
            h["verdetti"].add(f["verdetto"])
            if f["verdetto"] == "usabile":
                (h["pagine"] if e_pagina else h["municipi"]).add(v["slug"])
                h["usabili"].append(f)
    usabili_distinte = {k: h for k, h in host.items() if h["usabili"]}
    for h in usabili_distinte.values():
        u = h["usabili"]
        h["nome"] = min((f["nome"] for f in u), key=len)
        urls = {f["url"] for f in u}
        if len(urls) > 1:  # più sezioni dello stesso sito: nome della testata, link alla home
            for sep in (" - ", " – ", " ("):
                h["nome"] = h["nome"].split(sep)[0].strip()
            h["url"] = "https://" + tabella.chiave_fonte(u[0]).split("/")[2] + "/"
        else:
            h["url"] = next(iter(urls))
        h["tipo"] = piu_frequente(f["tipo"] for f in u)
        h["territorio"] = piu_frequente(f["territorio"] for f in u)
        h["accesso"] = piu_frequente((f.get("canale_lecito") or "").split(":")[0] for f in u)
        h["api"] = any(f.get("feed_o_api") for f in u)
        conti = [(f.get("conteggio_finestra"), f.get("marca"), f.get("ultima_data")) for f in u if f.get("conteggio_finestra") is not None]
        h["cont"], h["marca"], h["ultima"] = max(conti) if conti else (None, "—", None)
    tipi = collections.Counter(TIPI.get(h["tipo"], h["tipo"]) for h in usabili_distinte.values())
    terr = collections.Counter(TERR.get(h["territorio"], h["territorio"]) for h in usabili_distinte.values())
    verdetti_tot = collections.Counter()
    for v in voci:
        verdetti_tot.update(f["verdetto"] for f in v.get("fonti", []))
    isto = collections.Counter(min(r["usabile"], 5) for r in studiate)
    per_mun = []
    for m in ORD_MUN:
        pp = [r for r in studiate if r["mun"].split("/")[0] == m]
        if pp:
            per_mun.append({"mun": m, "con": sum(1 for r in pp if r["usabile"] > 0), "senza": sum(1 for r in pp if r["usabile"] == 0)})
    trasversali = sorted([h for h in usabili_distinte.values() if len(h["pagine"]) >= 2], key=lambda h: (-len(h["pagine"]), h["nome"].lower()))
    mun_studiati = sorted({r["mun"] for r in municipi}, key=ordine_mun)
    return {
        "pagine": pagine, "municipi": municipi,
        "testa": {"pagine": len(pagine), "studiate": len(studiate), "non_studiate": len(pagine) - len(studiate),
                  "con_usabile": sum(1 for r in studiate if r["usabile"] > 0), "senza": sum(1 for r in studiate if r["usabile"] == 0),
                  "fonti_distinte": len(host), "usabili_distinte": len(usabili_distinte),
                  "social": sum(1 for h in host.values() if "canale_chiuso" in h["verdetti"]),
                  "da_verificare": sum(1 for h in host.values() if "da_verificare" in h["verdetti"] and not h["usabili"]),
                  "segnalazioni": sum(verdetti_tot.values()), "giugno_scoperte": sum(1 for r in pagine if r["giugno"] == 0),
                  "municipi_studiati": mun_studiati, "municipi_mancanti": [m for m in ORD_MUN if m not in mun_studiati]},
        "isto": [{"k": ("5+" if k == 5 else str(k)), "v": isto.get(k, 0)} for k in range(6)],
        "verdetti": [{"k": et, "v": verdetti_tot.get(k, 0)} for k, et in VERDETTI],
        "tipi": [{"k": k, "v": v} for k, v in tipi.most_common()],
        "terr": [{"k": k, "v": v} for k, v in terr.most_common()],
        "per_mun": per_mun,
        "trasversali": [{"nome": h["nome"], "url": h["url"], "tipo": TIPI.get(h["tipo"], h["tipo"]), "terr": TERR.get(h["territorio"], h["territorio"]),
                         "n": len(h["pagine"]), "pagine": [nomi[s] for s in sorted(h["pagine"], key=lambda s: nomi[s])],
                         "municipi": [nomi[s] for s in sorted(h["municipi"])], "cont": h["cont"], "marca": h["marca"], "ultima": h["ultima"],
                         "api": h["api"], "accesso": h["accesso"]} for h in trasversali],
    }


SCHELETRO = '<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'

PAGINA = r"""<title>Fonti locali QN</title>
<style>
/* Layout: una colonna di lettura larga 1100px; numeri, legenda, grafici a coppie, tabelle. */
:root { --bg:#f7f6f2; --surface:#fcfcfb; --fg:#161512; --fg2:#52514e; --muted:#6f6e68; --grid:#e1e0d9; --axis:#c3c2b7; --line:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#eb6834; --link:#1d66bd; --crit:#d03b3b;
  --font:"Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#121211; --surface:#1a1a19; --fg:#f0efec; --fg2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --line:rgba(255,255,255,.10); --s1:#3987e5; --s2:#d95926; --link:#3987e5; color-scheme:dark } }
:root[data-theme="dark"] { --bg:#121211; --surface:#1a1a19; --fg:#f0efec; --fg2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --line:rgba(255,255,255,.10); --s1:#3987e5; --s2:#d95926; --link:#3987e5; color-scheme:dark }
body { background:var(--bg); color:var(--fg); font-family:var(--font); font-size:16px; line-height:1.45; margin:0; padding-block:24px 48px; padding-inline:16px; }
main { max-width:1100px; margin-inline:auto; display:grid; gap:28px; }
h1 { font-size:clamp(26px,4vw,34px); line-height:1.15; margin:0; text-wrap:balance; }
h2 { font-size:20px; margin:0 0 4px; text-wrap:balance; }
p { margin:0; max-width:72ch; }
.sub { color:var(--fg2); }
.eyebrow { font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); font-weight:600; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(150px,100%),1fr)); gap:12px; }
.tile { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px 16px; min-width:0; }
.tile .v { font-size:34px; font-weight:600; line-height:1.1; margin-top:4px; }
.tile .l { color:var(--fg2); font-size:14px; }
.tile.hero .v { font-size:48px; }
.due { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr)); gap:20px; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px; min-width:0; display:grid; gap:8px; align-content:start; }
.card p { font-size:14px; color:var(--fg2); }
svg { max-width:100%; height:auto; display:block; font-family:var(--font); }
.bar { fill:var(--s1); } .bar2 { fill:var(--s2); } .bar.zero { fill:var(--crit); }
.lbl { fill:var(--fg); font-size:13px; } .val { fill:var(--fg2); font-size:12px; font-variant-numeric:tabular-nums; } .ax { stroke:var(--axis); stroke-width:1; }
.legend { display:flex; gap:16px; flex-wrap:wrap; font-size:13px; color:var(--fg2); } .legend span::before { content:""; display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:6px; vertical-align:-1px; background:var(--s1); } .legend span.b::before { background:var(--s2); } .legend span.z::before { background:var(--crit); }
.tip { position:fixed; pointer-events:none; background:var(--fg); color:var(--bg); font-size:13px; padding:6px 8px; border-radius:4px; z-index:9; display:none; max-width:280px; }
.tabwrap { max-height:70vh; overflow:auto; border:1px solid var(--line); border-radius:8px; background:var(--surface); }
table { border-collapse:collapse; width:100%; font-size:14px; } th, td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--grid); vertical-align:top; } th { position:sticky; top:0; background:var(--surface); color:var(--fg2); font-weight:600; white-space:nowrap; } th.num, td.num { text-align:right; font-variant-numeric:tabular-nums; }
th[aria-sort] { cursor:pointer; user-select:none; } th[aria-sort]::after { content:" ↕"; color:var(--muted); } th[aria-sort="ascending"]::after { content:" ↑"; } th[aria-sort="descending"]::after { content:" ↓"; }
tr.zero td:first-child::before { content:"● "; color:var(--crit); }
td.fonti { min-width:260px; max-width:520px; color:var(--fg2); }
.tools { display:flex; gap:12px; flex-wrap:wrap; align-items:center; } input[type=search], select { font:inherit; font-size:14px; padding:6px 10px; border:1px solid var(--axis); border-radius:6px; background:var(--surface); color:var(--fg); min-width:0; } input[type=search] { flex:1 1 220px; }
.pill { display:inline-block; font-size:12px; padding:1px 7px; border-radius:999px; border:1px solid var(--line); color:var(--fg2); margin-right:4px; white-space:nowrap; }
dl { display:grid; grid-template-columns:max-content 1fr; gap:6px 14px; margin:0; font-size:14px; } dt { font-weight:600; } dd { margin:0; color:var(--fg2); }
@media (max-width:480px) { dl { grid-template-columns:1fr; } dd { margin-bottom:6px; } }
a { color:var(--link); } a:focus-visible, th:focus-visible { outline:2px solid var(--link); outline-offset:2px; }
footer { color:var(--muted); font-size:13px; }
@media (prefers-reduced-motion: no-preference) { .bar, .bar2 { transition: opacity .15s } }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&display=swap">
<main>
<header style="display:grid;gap:8px">
  <div class="eyebrow">Quartieri News · studio del 13 ottobre 2026</div>
  <h1>Fonti locali per le %PAGINE% pagine di quartiere</h1>
  <p class="sub">Per ogni pagina: quali siti di quartiere o di Municipio pubblicano davvero (luglio–settembre 2026) e quali di questi i programmi di Quartieri News possono leggere in automatico. Una fonte è <strong>usabile</strong> quando non vieta la lettura automatica, ha pubblicato fra luglio e settembre e parla del territorio della pagina.</p>
</header>

<section>
  <div class="tiles" id="tiles"></div>
</section>

<section class="card">
  <h2>Come leggere</h2>
  <dl>
    <dt>Candidata</dt><dd>sito o pagina social trovato dalla ricerca per una pagina; ognuna riceve poi uno dei verdetti qui sotto. Una stessa fonte può essere candidata per più pagine.</dd>
    <dt>Usabile</dt><dd>sito che non vieta la lettura automatica, con pubblicazioni fra luglio e settembre 2026, che parla dei quartieri della pagina.</dd>
    <dt>Solo metadati</dt><dd>il sito vieta la lettura automatica: si possono usare solo titolo, link e data trovati da un motore di ricerca.</dd>
    <dt>Solo social</dt><dd>esiste solo una pagina o un gruppo Facebook, Instagram, WhatsApp o Telegram: non si apre in automatico, si segue a mano.</dd>
    <dt>Da verificare</dt><dd>il controllo automatico non ha potuto decidere: sito senza date leggibili, testata cittadina con pochissime voci locali, scheda al posto di un sito. Nel file dei dati c'è il motivo per ognuna.</dd>
    <dt>Inattiva</dt><dd>aperta ma ferma da prima di luglio 2026 (spesso comitati in pausa: da ricontrollare).</dd>
    <dt>Fuori territorio</dt><dd>sito aperto e vivo, ma parla di un'altra zona o di tutta Roma senza una sezione sul quartiere.</dd>
    <dt>Non raggiungibile</dt><dd>il sito non ha risposto al controllo (errore del server, certificato non valido, attesa scaduta): da riprovare.</dd>
    <dt>Territorio</dt><dd>Pagina = tutto il territorio della pagina; Quartiere = uno solo dei suoi quartieri; Municipio o Zona = più pagine insieme; Città = testata di tutta Roma con una sezione sul quartiere.</dd>
    <dt>Post lug–set</dt><dd>articoli pubblicati da tutto il sito fra luglio e settembre 2026; «almeno N» quando si è potuta contare solo una parte; «—» quando non si è potuto contare.</dd>
    <dt>Feed</dt><dd>il sito offre un elenco automatico dei nuovi articoli (RSS o API): la raccolta automatica è più semplice.</dd>
    <dt>Come è stato fatto</dt><dd>per ogni pagina tre passaggi automatici: uno cerca, uno verifica l'accesso e legge la pagina di elenco, uno prova a confutare. Nessun articolo aperto, nessun nome di persona, nessun titolo memorizzato.</dd>
  </dl>
</section>

<section class="due">
  <div class="card"><h2>Quante fonti usabili ha ogni pagina</h2><p>Quante pagine hanno 0, 1, 2… fonti usabili proprie. In rosso le pagine senza nessuna fonte: da lì si riparte.</p><div class="legend"><span>pagine con fonti usabili</span><span class="z">pagine senza</span></div><div id="c-isto"></div></div>
  <div class="card"><h2>Pagine per Municipio</h2><p>Pagine con almeno una fonte usabile propria e pagine senza. Le fonti trovate per l'intero Municipio non sono contate qui.</p><div class="legend"><span>con fonte usabile</span><span class="b">senza</span></div><div id="c-mun"></div></div>
</section>

<section class="card">
  <h2>Tutto quello che è stato trovato, per verdetto</h2>
  <p>Ogni sito o pagina social trovato dalla ricerca riceve un verdetto. Qui è contato una volta per ogni pagina o Municipio che lo ha proposto (%SEGNALAZIONI% segnalazioni in tutto): una stessa fonte può comparire più volte. Le tessere in testa contano invece ogni fonte una volta sola.</p>
  <div id="c-verdetti"></div>
</section>

<section class="due">
  <div class="card"><h2>Che tipo di fonti sono quelle usabili</h2><p>Fonti distinte: un sito contato una volta anche se serve più pagine.</p><div id="c-tipi"></div></div>
  <div class="card"><h2>Che territorio coprono</h2><p>Pagina = tutto il territorio della pagina; Quartiere = uno solo dei suoi quartieri; Municipio o Zona = più pagine insieme; Città = testata di tutta Roma con una sezione sul quartiere.</p><div id="c-terr"></div></div>
</section>

<section style="display:grid;gap:10px">
  <h2>Le fonti usabili per più pagine</h2>
  <p class="sub">Testate di Municipio o di zona e comitati di area: ognuna è usabile per almeno due pagine. Sono le prime da aggiungere all'elenco delle fonti della cronaca. Quando la stessa fonte è stata trovata anche cercando per l'intero Municipio, il Municipio è indicato a parte.</p>
  <div class="tabwrap"><table id="t-trasv"><thead><tr><th>Fonte</th><th>Tipo</th><th>Territorio</th><th class="num">Pagine</th><th>Quali pagine</th><th>Accesso</th><th class="num">Post lug–set</th><th>Feed</th></tr></thead><tbody></tbody></table></div>
</section>

<section style="display:grid;gap:10px">
  <h2>Pagina per pagina</h2>
  <p class="sub">Cerca una pagina, un Municipio o una fonte; ordina cliccando le intestazioni. I numeri contano solo le fonti trovate per la pagina; quelle trovate per l'intero Municipio sono nella tabella seguente e valgono anche per le sue pagine. «Fatti a giugno» = quanti fatti di cronaca la pagina poteva pubblicare a giugno 2026 con le fonti di allora: 0 vuol dire pagina rimasta senza cronaca. Le righe con il punto rosso non hanno nessuna fonte usabile propria.</p>
  <div class="tools"><input type="search" id="cerca" placeholder="Cerca pagina, Municipio o fonte…" aria-label="Cerca"><select id="filtro" aria-label="Filtro"><option value="tutte">Tutte le pagine</option><option value="zero">Senza fonte usabile propria</option><option value="giugno0">Senza cronaca a giugno</option></select><span class="sub" id="conta"></span></div>
  <div class="tabwrap"><table id="t-pagine"><thead><tr><th>Pagina</th><th>Mun.</th><th class="num">Fatti a giugno</th><th class="num">Candidate</th><th class="num">Usabili</th><th class="num">Solo social</th><th class="num">Da verificare</th><th>Fonti usabili (territorio)</th></tr></thead><tbody></tbody></table></div>
</section>

<section style="display:grid;gap:10px">
  <h2>Fonti trovate per l'intero Municipio</h2>
  <p class="sub" id="nota-mun">Fonti cercate per l'intero Municipio: valgono per tutte le sue pagine, ma non sono contate nei numeri per pagina qui sopra.</p>
  <div class="tabwrap"><table id="t-mun"><thead><tr><th>Municipio</th><th class="num">Candidate</th><th class="num">Usabili</th><th class="num">Solo social</th><th class="num">Da verificare</th><th>Fonti usabili (territorio)</th></tr></thead><tbody></tbody></table></div>
</section>

<footer>Dati: <code>tools/fonti-locali/runs/2026-10-13/fonti_pagine.json</code> · rapporto completo: <code>docs/sources/FONTI_PAGINE_SCOPERTE_2026-10.md</code> · branch <code>claude/focused-galileo-4hm3iw</code>. Generato il %DATA%.</footer>
</main>
<div class="tip" id="tip" role="status"></div>
<script id="dati" type="application/json">%JSON%</script>
<script>
const D = JSON.parse(document.getElementById('dati').textContent);
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const tip = $('#tip');
function mostraTip(e, html) { tip.innerHTML = html; tip.style.display = 'block'; tip.style.left = Math.min(e.clientX + 12, innerWidth - 300) + 'px'; tip.style.top = Math.min(e.clientY + 12, innerHeight - tip.offsetHeight - 8) + 'px'; }
function nascondiTip() { tip.style.display = 'none'; }
document.addEventListener('scroll', nascondiTip, { passive: true }); document.addEventListener('touchstart', nascondiTip, { passive: true });

// tessere
const T = D.testa;
$('#tiles').innerHTML = [
  ['hero', T.studiate, 'pagine studiate' + (T.non_studiate ? ' (' + T.non_studiate + ' non studiate)' : '')],
  ['', T.con_usabile, 'con almeno una fonte usabile propria'],
  ['', T.senza, 'senza fonte usabile propria (quelle di Municipio sono a parte)'],
  ['', T.usabili_distinte, 'siti e canali usabili, uno per sito (su ' + T.fonti_distinte + ' esaminati)'],
  ['', T.social, 'pagine social da seguire a mano'],
  ['', T.da_verificare, 'siti e canali da controllare a mano (mai usabili altrove)'],
].map(([c, v, l]) => `<div class="tile ${c}"><div class="l">${esc(l)}</div><div class="v">${v}</div></div>`).join('');
if (T.municipi_mancanti.length) $('#nota-mun').textContent += ' I Municipi ' + T.municipi_mancanti.join(', ') + ' non hanno una ricerca di Municipio in questo studio.';

// larghezza reale del contenitore: scala 1:1, testo e barre sempre della stessa misura
const larghezza = el => Math.min(720, Math.max(300, el.clientWidth || 520));
const tondo = (x, y, L, bh) => L > 0 ? `M${x},${y} h${Math.max(0, L - 4)} a4,4 0 0 1 4,4 v${bh - 8} a4,4 0 0 1 -4,4 h${-Math.max(0, L - 4)} z` : '';

// barre orizzontali: una serie, etichette a sinistra, valore alla punta
function barre(sel, righe, opt = {}) {
  const el = $(sel), w = larghezza(el), rh = 30, bh = 20, left = opt.left || 150, right = 44, h = righe.length * rh + 8;
  const max = Math.max(1, ...righe.map(r => r.v)), sx = v => (w - left - right) * v / max;
  let s = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opt.aria || '')}">`;
  s += `<line class="ax" x1="${left}" y1="2" x2="${left}" y2="${h - 2}"/>`;
  righe.forEach((r, i) => {
    const y = 4 + i * rh + (rh - bh) / 2, L = sx(r.v), cls = (opt.zero && i === 0) ? 'bar zero' : 'bar';
    s += `<text class="lbl" x="${left - 8}" y="${y + bh / 2 + 4}" text-anchor="end">${esc(r.k)}</text>`;
    if (L > 0) s += `<path class="${cls}" d="${tondo(left, y, L, bh)}" data-k="${esc(r.k)}" data-v="${r.v}"/>`;
    s += `<text class="val" x="${left + L + 6}" y="${y + bh / 2 + 4}">${r.v}</text>`;
  });
  el.innerHTML = s + '</svg>';
  el.querySelectorAll('path').forEach(p => { p.addEventListener('mousemove', e => mostraTip(e, `<b>${esc(p.dataset.k)}</b>: ${p.dataset.v}`)); p.addEventListener('mouseleave', nascondiTip); });
}

// barre impilate per Municipio: con / senza, gap di 2px fra i segmenti, estremità tonda sull'ultimo segmento
function barreMunicipi() {
  const righe = D.per_mun, el = $('#c-mun'), w = larghezza(el), rh = 26, bh = 18, left = 60, right = 40, h = righe.length * rh + 8;
  const max = Math.max(1, ...righe.map(r => r.con + r.senza)), sx = v => (w - left - right) * v / max;
  let s = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="Pagine con e senza fonte usabile per Municipio">`;
  s += `<line class="ax" x1="${left}" y1="2" x2="${left}" y2="${h - 2}"/>`;
  righe.forEach((r, i) => {
    const y = 4 + i * rh + (rh - bh) / 2, a = sx(r.con), b = sx(r.senza), t = `Municipio ${r.mun}: ${r.con} pagine con fonte usabile, ${r.senza} senza`;
    s += `<text class="lbl" x="${left - 8}" y="${y + bh / 2 + 4}" text-anchor="end">${r.mun}</text>`;
    if (a > 0) s += b > 0 ? `<rect class="bar" x="${left}" y="${y}" width="${Math.max(1, a - 2)}" height="${bh}" data-t="${t}"/>` : `<path class="bar" d="${tondo(left, y, a, bh)}" data-t="${t}"/>`;
    if (b > 0) s += `<path class="bar2" d="${tondo(left + a, y, b, bh)}" data-t="${t}"/>`;
    s += `<text class="val" x="${left + a + b + 6}" y="${y + bh / 2 + 4}">${r.con + r.senza}</text>`;
  });
  el.innerHTML = s + '</svg>';
  el.querySelectorAll('[data-t]').forEach(p => { p.addEventListener('mousemove', e => mostraTip(e, esc(p.dataset.t))); p.addEventListener('mouseleave', nascondiTip); });
}

function disegnaGrafici() {
  barre('#c-isto', D.isto.map(r => ({ k: r.k === '0' ? '0 fonti' : r.k + (r.k === '1' ? ' fonte' : ' fonti'), v: r.v })), { left: 80, zero: true, aria: 'Pagine per numero di fonti usabili' });
  barreMunicipi();
  barre('#c-verdetti', D.verdetti, { left: 150, aria: 'Segnalazioni per verdetto' });
  barre('#c-tipi', D.tipi, { left: 190, aria: 'Fonti usabili per tipo' });
  barre('#c-terr', D.terr, { left: 100, aria: 'Fonti usabili per territorio' });
}
disegnaGrafici();
let attesa; window.addEventListener('resize', () => { cancelAnimationFrame(attesa); attesa = requestAnimationFrame(disegnaGrafici); });

// tabelle
const fontiHtml = r => r.nomi_usabili.length ? r.nomi_usabili.map(f => `<a href="${esc(f.u)}" target="_blank" rel="noopener">${esc(f.n)}</a> <span class="pill">${esc(f.t)}</span>`).join('<br>') : '—';
const post = r => r.cont == null || (r.marca === 'S' && r.cont === 0) ? '—' : r.marca === 'S' ? 'almeno ' + r.cont : String(r.cont);
function righePagine(rows) {
  return rows.map(r => `<tr class="${r.usabile === 0 && !r.fallito ? 'zero' : ''}"><td>${esc(r.nome)}${r.fallito ? ' <span class="pill">non studiata</span>' : ''}</td><td>${esc(r.mun)}</td><td class="num">${r.giugno ?? '—'}</td><td class="num">${r.candidate}</td><td class="num"><b>${r.usabile}</b></td><td class="num">${r.canale_chiuso}</td><td class="num">${r.da_verificare}</td><td class="fonti">${fontiHtml(r)}</td></tr>`).join('');
}
let ordine = { col: null, asc: true };
const CHIAVI = ['nome', 'mun', 'giugno', 'candidate', 'usabile', 'canale_chiuso', 'da_verificare', 'usabile'];
function disegnaPagine() {
  const q = ($('#cerca').value || '').toLowerCase().trim(), f = $('#filtro').value;
  let rows = D.pagine.filter(r => (f !== 'zero' || (r.usabile === 0 && !r.fallito)) && (f !== 'giugno0' || r.giugno === 0));
  if (q) rows = rows.filter(r => (r.nome + ' ' + r.mun + ' ' + r.nomi_usabili.map(x => x.n).join(' ')).toLowerCase().includes(q));
  if (ordine.col !== null) {
    const k = CHIAVI[ordine.col];
    rows = [...rows].sort((a, b) => { const x = a[k] ?? -1, y = b[k] ?? -1; const c = typeof x === 'number' ? x - y : String(x).localeCompare(String(y), 'it'); return ordine.asc ? c : -c; });
  }
  $('#t-pagine tbody').innerHTML = righePagine(rows);
  $('#conta').textContent = rows.length + ' di ' + D.pagine.length + ' pagine';
}
$('#cerca').addEventListener('input', disegnaPagine); $('#filtro').addEventListener('change', disegnaPagine);
document.querySelectorAll('#t-pagine th').forEach((th, i) => { th.setAttribute('aria-sort', 'none'); th.tabIndex = 0; const f = () => { ordine = { col: i, asc: ordine.col === i ? !ordine.asc : true }; document.querySelectorAll('#t-pagine th').forEach(t => t.setAttribute('aria-sort', 'none')); th.setAttribute('aria-sort', ordine.asc ? 'ascending' : 'descending'); disegnaPagine(); }; th.addEventListener('click', f); th.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); f(); } }); });
disegnaPagine();
$('#t-mun tbody').innerHTML = D.municipi.map(r => `<tr class="${r.usabile === 0 ? 'zero' : ''}"><td>${esc(r.nome)}</td><td class="num">${r.candidate}</td><td class="num"><b>${r.usabile}</b></td><td class="num">${r.canale_chiuso}</td><td class="num">${r.da_verificare}</td><td class="fonti">${fontiHtml(r)}</td></tr>`).join('');
$('#t-trasv tbody').innerHTML = D.trasversali.map(r => `<tr><td><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.nome)}</a></td><td>${esc(r.tipo)}</td><td>${esc(r.terr)}</td><td class="num"><b>${r.n}</b></td><td class="fonti">${r.pagine.map(esc).join(', ')}${r.municipi.length ? ' <span class="pill">+ ' + r.municipi.map(esc).join(', ') + '</span>' : ''}</td><td>${esc(r.accesso)}</td><td class="num">${post(r)}</td><td>${r.api ? 'sì' : 'no'}</td></tr>`).join('');
</script>
"""


def main(argv):
    run_dir, out = argv[1], argv[2]
    repo = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    d = dati(run_dir, repo)
    html = (PAGINA.replace("%JSON%", json.dumps(d, ensure_ascii=False).replace("</", "<\\/"))
            .replace("%DATA%", dt.date.today().isoformat()).replace("%PAGINE%", str(d["testa"]["pagine"]))
            .replace("%SEGNALAZIONI%", str(d["testa"]["segnalazioni"])))
    if "--autonomo" in argv:
        html = SCHELETRO + html
    open(out, "w", encoding="utf-8").write(html)
    print(json.dumps({k: v for k, v in d["testa"].items() if k not in ("municipi_studiati",)}, ensure_ascii=False), file=sys.stderr)
    print("isto", d["isto"], "tipi", d["tipi"], "terr", d["terr"], "trasversali", len(d["trasversali"]), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)

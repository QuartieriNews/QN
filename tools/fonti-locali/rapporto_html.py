"""Pagina di lettura per l'owner: grafici e tabelle dalle fonti verificate.

Uso: rapporto_html.py RUN_DIR USCITA.html

Legge RUN_DIR/fonti_pagine.json (e, se c'è, la tabella della cronaca di giugno
tools/cronaca-prova/runs/2026-10-11/per_pagina.csv per il confronto) e scrive una pagina
HTML autonoma: numeri in testa, grafici in SVG disegnati dal browser, tabelle ordinabili e
filtrabili. Nessuna dipendenza, nessun titolo di articolo, nessun nome di persona: solo
quello che sta già nel JSON.
"""
import collections
import csv
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


def giugno(repo):
    p = os.path.join(repo, "tools", "cronaca-prova", "runs", "2026-10-11", "per_pagina.csv")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8-sig") as f:
        return {r["slug"]: int(r["pubblicabili"]) for r in csv.DictReader(f, delimiter=";")}


def dati(run_dir, repo):
    voci = tabella.carica(run_dir)
    g = giugno(repo)
    pagine, municipi = [], []
    for v in voci:
        fonti = v.get("fonti", [])
        c = collections.Counter(f["verdetto"] for f in fonti)
        usabili = [f for f in fonti if f["verdetto"] == "usabile"]
        riga = {"slug": v["slug"], "nome": v.get("pagina") or v["slug"], "mun": v.get("municipio") or "",
                "giugno": g.get(v["slug"]), "candidate": len(fonti), "fallito": bool(v.get("fallito")),
                **{k: c.get(k, 0) for k, _ in VERDETTI},
                "nomi_usabili": [{"n": f["nome"], "t": f["territorio"], "u": f["url"]} for f in usabili]}
        (municipi if v.get("tipo") == "municipio" else pagine).append(riga)
    pagine.sort(key=lambda r: (ORD_MUN.index(r["mun"].split("/")[0]) if r["mun"].split("/")[0] in ORD_MUN else 99, r["nome"]))

    # fonti distinte per host: quante pagine le giudicano usabili
    host = {}
    for v in voci:
        for f in v.get("fonti", []):
            # un sito è uno per host (le sue sezioni sono la stessa fonte); una pagina social è una per indirizzo
            kf = tabella.chiave_fonte(f)
            k = kf.split("/")[2] if f["canale"] == "sito" and kf.count("/") >= 2 else kf
            h = host.setdefault(k, {"nome": f["nome"], "url": f["url"], "tipo": f["tipo"], "canale": f["canale"], "territorio": f["territorio"],
                                    "usabile_in": [], "altri": [], "cont": f.get("conteggio_finestra"), "marca": f.get("marca"), "ultima": f.get("ultima_data"),
                                    "accesso": f.get("canale_lecito") or "", "api": bool(f.get("feed_o_api"))})
            if len(f["nome"]) < len(h["nome"]):
                h["nome"], h["url"] = f["nome"], f["url"]
            (h["usabile_in"] if f["verdetto"] == "usabile" else h["altri"]).append(v["slug"])
            if (f.get("conteggio_finestra") or 0) > (h["cont"] or 0):
                h["cont"], h["marca"], h["ultima"] = f["conteggio_finestra"], f.get("marca"), f.get("ultima_data")
    usabili_distinte = [h for h in host.values() if h["usabile_in"]]
    tipi = collections.Counter(TIPI.get(h["tipo"], h["tipo"]) for h in usabili_distinte)
    terr = collections.Counter(TERR.get(h["territorio"], h["territorio"]) for h in usabili_distinte)
    verdetti_tot = collections.Counter()
    for v in voci:
        verdetti_tot.update(f["verdetto"] for f in v.get("fonti", []))
    isto = collections.Counter(min(r["usabile"], 5) for r in pagine)
    per_mun = []
    for m in ORD_MUN:
        pp = [r for r in pagine if r["mun"].split("/")[0] == m]
        if pp:
            per_mun.append({"mun": m, "con": sum(1 for r in pp if r["usabile"] > 0), "senza": sum(1 for r in pp if r["usabile"] == 0)})
    social = len({k for k, h in host.items() if h["canale"] != "sito"})
    trasversali = sorted([h for h in usabili_distinte if len(h["usabile_in"]) >= 2], key=lambda h: (-len(h["usabile_in"]), h["nome"].lower()))
    return {
        "pagine": pagine, "municipi": municipi,
        "testa": {"pagine": len(pagine), "con_usabile": sum(1 for r in pagine if r["usabile"] > 0), "senza": sum(1 for r in pagine if r["usabile"] == 0),
                  "fonti_distinte": len(host), "usabili_distinte": len(usabili_distinte), "social": social,
                  "da_verificare": verdetti_tot.get("da_verificare", 0), "giugno_scoperte": sum(1 for r in pagine if r["giugno"] == 0)},
        "isto": [{"k": ("5+" if k == 5 else str(k)), "v": isto.get(k, 0)} for k in range(6)],
        "verdetti": [{"k": et, "v": verdetti_tot.get(k, 0)} for k, et in VERDETTI],
        "tipi": [{"k": k, "v": v} for k, v in tipi.most_common()],
        "terr": [{"k": k, "v": v} for k, v in terr.most_common()],
        "per_mun": per_mun,
        "trasversali": [{"nome": h["nome"], "url": h["url"], "tipo": TIPI.get(h["tipo"], h["tipo"]), "terr": TERR.get(h["territorio"], h["territorio"]),
                         "n": len(h["usabile_in"]), "pagine": sorted(set(h["usabile_in"])), "cont": h["cont"], "marca": h["marca"], "ultima": h["ultima"],
                         "api": h["api"], "accesso": h["accesso"].split(":")[0]} for h in trasversali],
    }


PAGINA = r"""<title>Fonti locali QN</title>
<style>
/* Layout: una colonna di lettura larga 1100px, numeri in testa, poi grafici a coppie, poi le tabelle. */
:root { --bg:#f7f6f2; --surface:#fcfcfb; --fg:#161512; --fg2:#52514e; --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7; --line:rgba(11,11,11,.10);
  --s1:#2a78d6; --s2:#eb6834; --s1soft:#cde2fb; --crit:#d03b3b; --good:#0ca30c; --warn:#fab219;
  --font:"Source Sans 3", system-ui, -apple-system, "Segoe UI", sans-serif; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#121211; --surface:#1a1a19; --fg:#f0efec; --fg2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --line:rgba(255,255,255,.10); --s1:#3987e5; --s2:#d95926; --s1soft:#184f95; color-scheme:dark } }
:root[data-theme="dark"] { --bg:#121211; --surface:#1a1a19; --fg:#f0efec; --fg2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --line:rgba(255,255,255,.10); --s1:#3987e5; --s2:#d95926; --s1soft:#184f95; color-scheme:dark }
body { background:var(--bg); color:var(--fg); font-family:var(--font); font-size:16px; line-height:1.45; margin:0; padding-block:24px 48px; padding-inline:16px; }
main { max-width:1100px; margin-inline:auto; display:grid; gap:28px; }
h1 { font-size:clamp(26px,4vw,34px); line-height:1.15; margin:0; text-wrap:balance; }
h2 { font-size:20px; margin:0 0 4px; text-wrap:balance; }
h3 { font-size:16px; margin:0; font-weight:600; }
p { margin:0; max-width:70ch; }
.sub { color:var(--fg2); }
.eyebrow { font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); font-weight:600; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; }
.tile { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px 16px; min-width:0; }
.tile .v { font-size:34px; font-weight:600; line-height:1.1; margin-top:4px; }
.tile .l { color:var(--fg2); font-size:14px; }
.tile.hero .v { font-size:48px; }
.due { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:20px; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px; min-width:0; display:grid; gap:8px; align-content:start; }
.card p { font-size:14px; color:var(--fg2); }
svg { max-width:100%; height:auto; display:block; font-family:var(--font); }
.bar { fill:var(--s1); } .bar2 { fill:var(--s2); } .bar.zero { fill:var(--crit); }
.lbl { fill:var(--fg); font-size:13px; } .val { fill:var(--fg2); font-size:12px; font-variant-numeric:tabular-nums; } .ax { stroke:var(--axis); stroke-width:1; }
.legend { display:flex; gap:16px; flex-wrap:wrap; font-size:13px; color:var(--fg2); } .legend span::before { content:""; display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:6px; vertical-align:-1px; background:var(--s1); } .legend span.b::before { background:var(--s2); } .legend span.z::before { background:var(--crit); }
.tip { position:fixed; pointer-events:none; background:var(--fg); color:var(--bg); font-size:13px; padding:6px 8px; border-radius:4px; z-index:9; display:none; max-width:280px; }
.tabwrap { overflow-x:auto; border:1px solid var(--line); border-radius:8px; background:var(--surface); }
table { border-collapse:collapse; width:100%; font-size:14px; } th, td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--grid); vertical-align:top; } th { position:sticky; top:0; background:var(--surface); color:var(--fg2); font-weight:600; cursor:pointer; white-space:nowrap; user-select:none; } th.num, td.num { text-align:right; font-variant-numeric:tabular-nums; }
th[aria-sort]::after { content:" ↕"; color:var(--muted); } th[aria-sort="ascending"]::after { content:" ↑"; } th[aria-sort="descending"]::after { content:" ↓"; }
tr.zero td:first-child::before { content:"● "; color:var(--crit); }
td.fonti { min-width:260px; max-width:520px; color:var(--fg2); }
.tools { display:flex; gap:12px; flex-wrap:wrap; align-items:center; } input[type=search], select { font:inherit; font-size:14px; padding:6px 10px; border:1px solid var(--axis); border-radius:6px; background:var(--surface); color:var(--fg); min-width:0; } input[type=search] { flex:1 1 220px; }
.pill { display:inline-block; font-size:12px; padding:1px 7px; border-radius:999px; border:1px solid var(--line); color:var(--fg2); margin-right:4px; white-space:nowrap; }
dl { display:grid; grid-template-columns:max-content 1fr; gap:6px 14px; margin:0; font-size:14px; } dt { font-weight:600; } dd { margin:0; color:var(--fg2); }
a { color:var(--s1); } a:focus-visible, th:focus-visible, button:focus-visible { outline:2px solid var(--s1); outline-offset:2px; }
footer { color:var(--muted); font-size:13px; }
@media (prefers-reduced-motion: no-preference) { .bar, .bar2 { transition: opacity .15s } }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&display=swap">
<main>
<header style="display:grid;gap:8px">
  <div class="eyebrow">Quartieri News · studio del 13 ottobre 2026</div>
  <h1>Fonti locali per le 89 pagine di quartiere</h1>
  <p class="sub">Per ogni pagina: quali siti di quartiere o di Municipio pubblicano davvero (luglio–settembre 2026) e che cosa un agente può leggerne. Una fonte è <strong>usabile</strong> quando è aperta agli agenti, viva nel trimestre e parla del territorio della pagina.</p>
</header>

<section>
  <div class="tiles" id="tiles"></div>
</section>

<section class="due">
  <div class="card"><h2>Quante fonti usabili ha ogni pagina</h2><p>Numero di pagine per numero di fonti usabili trovate. Le pagine a zero sono quelle da cui ripartire.</p><div id="c-isto"></div></div>
  <div class="card"><h2>Pagine per Municipio</h2><p>Pagine con almeno una fonte usabile e pagine senza.</p><div class="legend"><span>con fonte usabile</span><span class="b">senza</span></div><div id="c-mun"></div></div>
</section>

<section class="due">
  <div class="card"><h2>Che tipo di fonti sono quelle usabili</h2><p>Fonti distinte (un sito contato una volta anche se serve più pagine).</p><div id="c-tipi"></div></div>
  <div class="card"><h2>Che territorio coprono</h2><p>Quartiere = la singola pagina; Municipio o zona = più pagine insieme.</p><div id="c-terr"></div></div>
</section>

<section class="card">
  <h2>Tutte le candidate, per verdetto</h2>
  <p>Ogni candidata trovata dagli agenti ha un verdetto. «Solo social» = esiste solo una pagina Facebook/Instagram/WhatsApp: utile alla raccolta manuale, non alla pipeline. «Solo metadati» = il sito esclude gli agenti AI: se ne può usare titolo, link e data da un motore. «Da verificare» = l'automa non ha potuto decidere.</p>
  <div id="c-verdetti"></div>
</section>

<section style="display:grid;gap:10px">
  <h2>Le fonti che servono più pagine</h2>
  <p class="sub">Testate di Municipio o di zona e comitati di area: ognuna copre più pagine insieme. Sono il primo gruppo da aggiungere al censimento della cronaca. «Post lug–set» è il volume dell'intero sito: <strong>M</strong> misurato, <strong>S</strong> stimato per difetto.</p>
  <div class="tabwrap"><table id="t-trasv"><thead><tr><th>Fonte</th><th>Tipo</th><th>Territorio</th><th class="num">Pagine</th><th>Quali pagine</th><th>Accesso</th><th class="num">Post lug–set</th><th>Feed/API</th></tr></thead><tbody></tbody></table></div>
</section>

<section style="display:grid;gap:10px">
  <h2>Pagina per pagina</h2>
  <p class="sub">Cerca una pagina o un Municipio, ordina cliccando le intestazioni. «Giugno» = fatti di cronaca pubblicabili a giugno 2026 con la regola delle due fonti (prima di questo studio). Le righe con il punto rosso non hanno nessuna fonte usabile.</p>
  <div class="tools"><input type="search" id="cerca" placeholder="Cerca pagina, Municipio o fonte…" aria-label="Cerca"><select id="filtro" aria-label="Filtro"><option value="tutte">Tutte le pagine</option><option value="zero">Senza fonte usabile</option><option value="giugno0">Senza cronaca a giugno</option></select><span class="sub" id="conta"></span></div>
  <div class="tabwrap"><table id="t-pagine"><thead><tr><th>Pagina</th><th>Mun.</th><th class="num">Giugno</th><th class="num">Candidate</th><th class="num">Usabili</th><th class="num">Solo social</th><th class="num">Da verificare</th><th>Fonti usabili (territorio)</th></tr></thead><tbody></tbody></table></div>
</section>

<section style="display:grid;gap:10px">
  <h2>I Municipi come voce a sé</h2>
  <p class="sub">Fonti cercate a livello di intero Municipio: valgono per tutte le sue pagine.</p>
  <div class="tabwrap"><table id="t-mun"><thead><tr><th>Municipio</th><th class="num">Candidate</th><th class="num">Usabili</th><th class="num">Solo social</th><th class="num">Da verificare</th><th>Fonti usabili (territorio)</th></tr></thead><tbody></tbody></table></div>
</section>

<section class="card">
  <h2>Come leggere</h2>
  <dl>
    <dt>Usabile</dt><dd>sito aperto (robots.txt senza esclusioni per gli agenti AI, nessuna riserva TDM), con pubblicazioni fra luglio e settembre 2026, che parla dei quartieri della pagina.</dd>
    <dt>Solo metadati</dt><dd>il sito esclude gli agenti AI per nome: si possono usare solo titolo, link e data trovati da un motore di ricerca.</dd>
    <dt>Solo social</dt><dd>esiste solo una pagina o un gruppo Facebook, Instagram, WhatsApp o Telegram: non si apre, si registra l'indirizzo per la raccolta manuale.</dd>
    <dt>Da verificare</dt><dd>l'automa non ha potuto decidere: sito senza date leggibili, testata cittadina con pochissime voci locali, scheda al posto di un sito. Nel JSON c'è il motivo per ognuna.</dd>
    <dt>Inattiva</dt><dd>aperta ma ferma prima di luglio 2026 (spesso comitati in pausa: da ricontrollare).</dd>
    <dt>M / S</dt><dd>conteggio misurato dall'API del sito (intero sito) / stimato per difetto da feed o sitemap.</dd>
    <dt>Come è stato fatto</dt><dd>per ogni pagina tre agenti: uno cerca, uno verifica con lo strumento e legge la pagina di elenco, uno prova a confutare. Nessun articolo aperto, nessun nome di persona, nessun titolo memorizzato.</dd>
  </dl>
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
function mostraTip(e, html) { tip.innerHTML = html; tip.style.display = 'block'; const x = Math.min(e.clientX + 12, innerWidth - 300), y = e.clientY + 12; tip.style.left = x + 'px'; tip.style.top = y + 'px'; }
function nascondiTip() { tip.style.display = 'none'; }

// tessere
const T = D.testa;
$('#tiles').innerHTML = [
  ['hero', T.pagine, 'pagine studiate'],
  ['', T.con_usabile, 'con almeno una fonte usabile'],
  ['', T.senza, 'senza nessuna fonte usabile'],
  ['', T.usabili_distinte, 'fonti usabili distinte (su ' + T.fonti_distinte + ' candidate)'],
  ['', T.social, 'canali social per la raccolta manuale'],
  ['', T.da_verificare, 'candidate da verificare a mano'],
].map(([c, v, l]) => `<div class="tile ${c}"><div class="l">${esc(l)}</div><div class="v">${v}</div></div>`).join('');

// barre orizzontali: una serie, etichette a sinistra, valore alla punta
function barre(sel, righe, opt = {}) {
  const w = 520, rh = 30, bh = 20, left = opt.left || 150, right = 44, h = righe.length * rh + 8;
  const max = Math.max(1, ...righe.map(r => r.v));
  const sx = v => (w - left - right) * v / max;
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(opt.aria || '')}">`;
  s += `<line class="ax" x1="${left}" y1="2" x2="${left}" y2="${h - 2}"/>`;
  righe.forEach((r, i) => {
    const y = 4 + i * rh + (rh - bh) / 2, L = sx(r.v), cls = (opt.zero && r.k === '0') ? 'bar zero' : 'bar';
    const path = L > 0 ? `M${left},${y} h${Math.max(0, L - 4)} a4,4 0 0 1 4,4 v${bh - 8} a4,4 0 0 1 -4,4 h${-Math.max(0, L - 4)} z` : '';
    s += `<text class="lbl" x="${left - 8}" y="${y + bh / 2 + 4}" text-anchor="end">${esc(r.k)}</text>`;
    if (path) s += `<path class="${cls}" d="${path}" data-k="${esc(r.k)}" data-v="${r.v}"/>`;
    s += `<text class="val" x="${left + L + 6}" y="${y + bh / 2 + 4}">${r.v}</text>`;
  });
  s += '</svg>';
  const el = $(sel); el.innerHTML = s;
  el.querySelectorAll('path').forEach(p => { p.addEventListener('mousemove', e => mostraTip(e, `<b>${esc(p.dataset.k)}</b>: ${p.dataset.v}`)); p.addEventListener('mouseleave', nascondiTip); });
}
barre('#c-isto', D.isto.map(r => ({ k: r.k === '0' ? '0 fonti' : (r.k + (r.k === '1' ? ' fonte' : ' fonti')), v: r.v, ...(r.k === '0' ? { k0: true } : {}) })).map(r => ({ ...r, k: r.k })), { left: 80, aria: 'Pagine per numero di fonti usabili' });
// colora di rosso la barra delle pagine a zero
(() => { const p = $('#c-isto path'); if (p && p.dataset.k.startsWith('0')) p.classList.add('zero'); })();
barre('#c-tipi', D.tipi, { left: 190, aria: 'Fonti usabili per tipo' });
barre('#c-terr', D.terr, { left: 100, aria: 'Fonti usabili per territorio' });
barre('#c-verdetti', D.verdetti, { left: 150, aria: 'Candidate per verdetto' });

// barre impilate per Municipio: con / senza, gap di 2px fra i segmenti
(() => {
  const righe = D.per_mun, w = 520, rh = 26, bh = 18, left = 60, right = 40, h = righe.length * rh + 8;
  const max = Math.max(1, ...righe.map(r => r.con + r.senza)), sx = v => (w - left - right) * v / max;
  let s = `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="Pagine con e senza fonte usabile per Municipio">`;
  s += `<line class="ax" x1="${left}" y1="2" x2="${left}" y2="${h - 2}"/>`;
  righe.forEach((r, i) => {
    const y = 4 + i * rh + (rh - bh) / 2, a = sx(r.con), b = sx(r.senza);
    s += `<text class="lbl" x="${left - 8}" y="${y + bh / 2 + 4}" text-anchor="end">${r.mun}</text>`;
    if (a > 0) s += `<rect class="bar" x="${left}" y="${y}" width="${Math.max(1, a - (b > 0 ? 2 : 0))}" height="${bh}" data-t="Municipio ${r.mun}: ${r.con} pagine con fonte usabile, ${r.senza} senza"/>`;
    if (b > 0) s += `<path class="bar2" d="M${left + a},${y} h${Math.max(0, b - 4)} a4,4 0 0 1 4,4 v${bh - 8} a4,4 0 0 1 -4,4 h${-Math.max(0, b - 4)} z" data-t="Municipio ${r.mun}: ${r.con} pagine con fonte usabile, ${r.senza} senza"/>`;
    s += `<text class="val" x="${left + a + b + 6}" y="${y + bh / 2 + 4}">${r.con + r.senza}</text>`;
  });
  s += '</svg>';
  const el = $('#c-mun'); el.innerHTML = s;
  el.querySelectorAll('[data-t]').forEach(p => { p.addEventListener('mousemove', e => mostraTip(e, esc(p.dataset.t))); p.addEventListener('mouseleave', nascondiTip); });
})();

// tabelle
const fontiHtml = r => r.nomi_usabili.length ? r.nomi_usabili.map(f => `<a href="${esc(f.u)}" target="_blank" rel="noopener">${esc(f.n)}</a> <span class="pill">${esc(f.t)}</span>`).join('<br>') : '—';
function righePagine(rows) {
  return rows.map(r => `<tr class="${r.usabile === 0 ? 'zero' : ''}"><td>${esc(r.nome)}${r.fallito ? ' <span class="pill">agente fallito</span>' : ''}</td><td>${esc(r.mun)}</td><td class="num">${r.giugno ?? '—'}</td><td class="num">${r.candidate}</td><td class="num"><b>${r.usabile}</b></td><td class="num">${r.canale_chiuso}</td><td class="num">${r.da_verificare}</td><td class="fonti">${fontiHtml(r)}</td></tr>`).join('');
}
let ordine = { col: null, asc: true };
function disegnaPagine() {
  const q = ($('#cerca').value || '').toLowerCase().trim(), f = $('#filtro').value;
  let rows = D.pagine.filter(r => (f !== 'zero' || r.usabile === 0) && (f !== 'giugno0' || r.giugno === 0));
  if (q) rows = rows.filter(r => (r.nome + ' ' + r.mun + ' ' + r.nomi_usabili.map(x => x.n).join(' ')).toLowerCase().includes(q));
  if (ordine.col !== null) {
    const chiavi = ['nome', 'mun', 'giugno', 'candidate', 'usabile', 'canale_chiuso', 'da_verificare', 'nome'];
    const k = chiavi[ordine.col];
    rows = [...rows].sort((a, b) => { const x = a[k] ?? -1, y = b[k] ?? -1; const c = typeof x === 'number' ? x - y : String(x).localeCompare(String(y), 'it'); return ordine.asc ? c : -c; });
  }
  $('#t-pagine tbody').innerHTML = righePagine(rows);
  $('#conta').textContent = rows.length + ' di ' + D.pagine.length + ' pagine';
}
$('#cerca').addEventListener('input', disegnaPagine); $('#filtro').addEventListener('change', disegnaPagine);
document.querySelectorAll('#t-pagine th').forEach((th, i) => { th.setAttribute('aria-sort', 'none'); th.tabIndex = 0; const f = () => { ordine = { col: i, asc: ordine.col === i ? !ordine.asc : true }; document.querySelectorAll('#t-pagine th').forEach(t => t.setAttribute('aria-sort', 'none')); th.setAttribute('aria-sort', ordine.asc ? 'ascending' : 'descending'); disegnaPagine(); }; th.addEventListener('click', f); th.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); f(); } }); });
disegnaPagine();
$('#t-mun tbody').innerHTML = D.municipi.map(r => `<tr class="${r.usabile === 0 ? 'zero' : ''}"><td>${esc(r.nome)}</td><td class="num">${r.candidate}</td><td class="num"><b>${r.usabile}</b></td><td class="num">${r.canale_chiuso}</td><td class="num">${r.da_verificare}</td><td class="fonti">${fontiHtml(r)}</td></tr>`).join('');
$('#t-trasv tbody').innerHTML = D.trasversali.map(r => `<tr><td><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.nome)}</a></td><td>${esc(r.tipo)}</td><td>${esc(r.terr)}</td><td class="num"><b>${r.n}</b></td><td class="fonti">${r.pagine.map(esc).join(', ')}</td><td>${esc(r.accesso)}</td><td class="num">${r.cont == null ? '—' : r.cont + ' (' + r.marca + ')'}</td><td>${r.api ? 'sì' : 'no'}</td></tr>`).join('');
</script>
"""


def main(argv):
    run_dir, out = argv[1], argv[2]
    repo = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    d = dati(run_dir, repo)
    import datetime as dt
    html = PAGINA.replace("%JSON%", json.dumps(d, ensure_ascii=False).replace("</", "<\\/")).replace("%DATA%", dt.date.today().isoformat())
    open(out, "w", encoding="utf-8").write(html)
    print(json.dumps(d["testa"], ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)
